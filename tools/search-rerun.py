#!/usr/bin/env python3
"""search-rerun.py — re-run a search record's expressions as run and compare what they found (round 95).

A search record (PRISMA-S, `knowledge/search-rerun-record-r95.md`) files each search's strategy "copied and
pasted exactly as run" (item 8), the date it ran (item 13) and the number of records it identified (item 15).
The lane's `research-gate verify-sweeps` re-checks only that a NEGATIVE sweep's named glob set is empty; nothing
re-executes a recorded expression or compares the count it recorded. This tool does, for local searches over
committed lane files:

  - it re-runs every recorded expression at the revision the record says it ran against (`rev`) and compares the
    number of matching files and the set of matching paths with the recorded `hits` and `hit_set`. A difference
    there is a fault of the RECORD (the expression, the count or the set was not what was run): `COUNT_DRIFT`,
    `SET_DRIFT`.
  - it re-runs the same expression over the current working tree under ROOT and reports whether the result
    moved since `rev`: `TREE_CHANGED`. PRISMA-S item 15 names both causes of a different count on a re-run —
    "errors in the published search or major changes to a database"; the two re-runs keep them apart. A tree
    change is information (exit 0) unless `--strict`.

Record form — a section headed exactly `## Searches` holding one Markdown table with exactly these columns:

  | id | engine | where | expression | rev | searched | hits | hit_set |

  id          `Q<n>`, unique in the record
  engine      `fixed` (the expression is a literal byte string, as `grep -F`) or `regex` (a Python `re` pattern,
              compared with `grep -P`); both match line by line (a line is the bytes between `\\n`), and a file
              is a hit when at least one of its lines matches, as `grep -l`
  where       comma-separated globs relative to ROOT; `*` and `?` stay inside one path segment and `**` spans
              segments (Python `PurePosixPath.full_match`); no absolute path, no `..`, no backslash
  expression  wrapped in one pair of backticks; `\\|` stands for `|`; never empty
  rev         the full 40-hex commit the search ran against
  searched    the date the search ran, `YYYY-MM-DD`
  hits        the number of matching files, decimal
  hit_set     `-` when hits is 0; otherwise the comma-separated matching paths, or `sha256:<64 hex>` of the
              sorted matching paths each followed by `\\n` (what `grep -l … | LC_ALL=C sort | sha256sum` prints)

Usage:
    python3 tools/search-rerun.py verify RECORD [--root LANE] [--strict]

Output, one line per search, then a summary and a verdict:
    SEARCH_RERUN <id> rev=<MATCH|DRIFT> tree=<SAME|CHANGED> recorded=<n> at_rev=<n> at_tree=<n> [codes]
    SEARCH_RERUN_SUMMARY searches=<n> rev_match=<k>/<n> tree_same=<m>/<n> findings=<f>
    SEARCH_RERUN: CLEAN | DRIFT
Exit: 0 every search matches at its rev (tree changes allowed unless --strict); 1 any COUNT_DRIFT or SET_DRIFT
(or TREE_CHANGED under --strict); 2 setup — `SEARCH_RERUN_ERROR <code> <detail>` on stderr for a missing or
unreadable record, no `## Searches` section, a wrong header, a malformed or duplicate row, an unknown engine, an
empty or uncompilable expression, an unsafe glob, a rev that is not a commit of ROOT's repository, a symlink or
non-regular file matched by a glob, or a ROOT that is not a git toplevel.

Named limits: the regex engine is Python `re`, not PCRE — a pattern whose meaning differs between them is
compared under Python's meaning; a match never spans a newline; the tree re-run reads the files on disk,
tracked or not; the tool proves the record agrees with what the expression finds, not that the expression was
the right one to run (recall is not measured).

Reads only ROOT's files and its git objects (read-only `git ls-tree`/`git cat-file`). No network, no writes.
Python 3.13+ standard library only.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys
from pathlib import PurePosixPath

HEADER = ["id", "engine", "where", "expression", "rev", "searched", "hits", "hit_set"]
ENGINES = ("fixed", "regex")
ID_RE = re.compile(r"Q[1-9][0-9]*\Z")
REV_RE = re.compile(r"[0-9a-f]{40}\Z")
DATE_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\Z")
HITS_RE = re.compile(r"(0|[1-9][0-9]*)\Z")
DIGEST_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")
SPLIT_RE = re.compile(r"(?<!\\)\|")


class Setup(Exception):
    def __init__(self, code, detail):
        super().__init__(f"{code} {detail}")
        self.code = code
        self.detail = detail


def git(root, *args):
    p = subprocess.run(["git", "-C", root, *args], capture_output=True)
    return p.returncode, p.stdout


def cells(line):
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")) or len(s) < 2:
        return None
    return [c.strip().replace("\\|", "|") for c in SPLIT_RE.split(s[1:-1])]


def parse_record(path):
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().split("\n")
    except (OSError, UnicodeDecodeError) as exc:
        raise Setup("RECORD_UNREADABLE", f"{path}: {exc}")
    starts = [i for i, ln in enumerate(lines) if ln.rstrip() == "## Searches"]
    if len(starts) != 1:
        raise Setup("SECTION", f"expected exactly one '## Searches' heading, found {len(starts)}")
    i = starts[0] + 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    table = []
    while i < len(lines) and lines[i].strip().startswith("|"):
        table.append(lines[i])
        i += 1
    if len(table) < 3:
        raise Setup("TABLE", "the section holds no table with a header, a separator and at least one row")
    head = cells(table[0])
    if head != HEADER:
        raise Setup("HEADER", f"columns {head!r} != {HEADER!r}")
    sep = cells(table[1])
    if sep is None or len(sep) != len(HEADER) or not all(re.fullmatch(r":?-{3,}:?", c) for c in sep):
        raise Setup("TABLE", "second table line is not a separator row")
    rows, seen = [], set()
    for ln in table[2:]:
        c = cells(ln)
        if c is None or len(c) != len(HEADER):
            raise Setup("ROW", f"row width != {len(HEADER)}: {ln!r}")
        r = dict(zip(HEADER, c))
        if not ID_RE.match(r["id"]) or r["id"] in seen:
            raise Setup("ROW", f"bad or duplicate id {r['id']!r}")
        seen.add(r["id"])
        if r["engine"] not in ENGINES:
            raise Setup("ENGINE", f"{r['id']}: {r['engine']!r} not in {ENGINES}")
        e = r["expression"]
        if len(e) < 3 or not (e.startswith("`") and e.endswith("`")) or "`" in e[1:-1]:
            raise Setup("EXPRESSION", f"{r['id']}: expression must be one backtick-wrapped non-empty span")
        r["expr"] = e[1:-1]
        if r["engine"] == "regex":
            try:
                r["pattern"] = re.compile(r["expr"])
            except re.error as exc:
                raise Setup("EXPRESSION", f"{r['id']}: {exc}")
        else:
            r["needle"] = r["expr"].encode("utf-8")
        if not REV_RE.match(r["rev"]):
            raise Setup("REV", f"{r['id']}: rev must be 40 lowercase hex")
        if not DATE_RE.match(r["searched"]):
            raise Setup("DATE", f"{r['id']}: searched must be YYYY-MM-DD")
        if not HITS_RE.match(r["hits"]):
            raise Setup("HITS", f"{r['id']}: hits must be a decimal count")
        r["n"] = int(r["hits"])
        hs = r["hit_set"]
        if r["n"] == 0:
            if hs != "-":
                raise Setup("HIT_SET", f"{r['id']}: hits 0 needs hit_set '-'")
            r["set"] = []
        elif DIGEST_RE.match(hs):
            r["digest"] = hs[len("sha256:"):]
        elif hs and hs != "-":
            r["set"] = [p.strip() for p in hs.split(",")]
            if any(not p for p in r["set"]):
                raise Setup("HIT_SET", f"{r['id']}: empty path in hit_set")
        else:
            raise Setup("HIT_SET", f"{r['id']}: hits {r['n']} needs a path list or a sha256 digest")
        globs = [g.strip() for g in r["where"].split(",")]
        for g in globs:
            parts = g.split("/")
            if not g or g.startswith("/") or "\\" in g or ".." in parts or "" in parts or "." in parts:
                raise Setup("WHERE", f"{r['id']}: unsafe or empty glob {g!r}")
        r["globs"] = globs
        rows.append(r)
    return rows


def matches(path, globs):
    pp = PurePosixPath(path)
    return any(pp.full_match(g) for g in globs)


def hit(data, r):
    for line in data.split(b"\n"):
        if r["engine"] == "fixed":
            if r["needle"] in line:
                return True
        elif r["pattern"].search(line.decode("utf-8", "surrogateescape")):
            return True
    return False


def files_at_rev(root, rev, cache):
    if rev not in cache:
        rc, _ = git(root, "cat-file", "-e", rev + "^{commit}")
        if rc != 0:
            raise Setup("REV", f"{rev} is not a commit in {root}")
        rc, out = git(root, "ls-tree", "-r", "-z", "--full-tree", rev)
        if rc != 0:
            raise Setup("REV", f"git ls-tree failed for {rev}")
        entries = {}
        for rec in out.split(b"\0"):
            if not rec:
                continue
            meta, path = rec.split(b"\t", 1)
            mode, kind, obj = meta.split(b" ")
            entries[path.decode("utf-8", "surrogateescape")] = (mode.decode(), kind.decode(), obj.decode())
        cache[rev] = entries
    return cache[rev]


def blob(root, obj, blobs):
    """One read-only `git cat-file blob` per distinct object per run; the bytes are shared by every search."""
    if obj not in blobs:
        p = subprocess.run(["git", "-C", root, "cat-file", "blob", obj], capture_output=True)
        if p.returncode != 0:
            raise Setup("REV", f"blob {obj} unreadable")
        blobs[obj] = p.stdout
    return blobs[obj]


def run_at_rev(root, r, cache):
    entries = files_at_rev(root, r["rev"], cache)
    found = []
    tops = tuple(sorted({(static_dir(g) + "/") if static_dir(g) else "" for g in r["globs"]}))
    for path, (mode, kind, obj) in sorted(entries.items()):
        if not path.startswith(tops) or not matches(path, r["globs"]):
            continue
        if kind != "blob" or mode not in ("100644", "100755"):
            raise Setup("WHERE_TYPE", f"{r['id']}: {path} at {r['rev'][:12]} is mode {mode} ({kind})")
        if hit(blob(root, obj, cache.setdefault("blobs", {})), r):
            found.append(path)
    return found


def static_dir(glob):
    """The directory part of a glob before its first wildcard segment ('' for the root)."""
    segs = glob.split("/")[:-1]
    out = []
    for s in segs:
        if any(ch in s for ch in "*?["):
            break
        out.append(s)
    return "/".join(out)


def tree_files(root, globs):
    """Files on disk under each glob's static directory; a symlink on the way in is refused, a symlink inside is
    listed (so a glob matching it is a WHERE_TYPE error, never a followed read)."""
    out = set()
    for top in sorted({static_dir(g) for g in globs}):
        cur = root
        for seg in [s for s in top.split("/") if s]:
            cur = os.path.join(cur, seg)
            if os.path.islink(cur):
                raise Setup("WHERE_TYPE", f"{os.path.relpath(cur, root)} on a glob's path is a symlink")
        if not os.path.isdir(cur):
            continue
        for dirpath, dirnames, filenames in os.walk(cur):
            rel_dir = os.path.relpath(dirpath, root)
            dirnames[:] = sorted(d for d in dirnames if not (rel_dir == "." and d in (".git", ".jj")))
            for name in filenames + [d for d in dirnames if os.path.islink(os.path.join(dirpath, d))]:
                rel = name if rel_dir == "." else f"{rel_dir}/{name}"
                out.add(rel.replace(os.sep, "/"))
    return sorted(out)


def run_on_tree(root, r, listing):
    found = []
    for rel in listing:
        if not matches(rel, r["globs"]):
            continue
        full = os.path.join(root, rel)
        if os.path.islink(full) or not os.path.isfile(full):
            raise Setup("WHERE_TYPE", f"{r['id']}: {rel} in the tree is a symlink or not a regular file")
        with open(full, "rb") as fh:
            if hit(fh.read(), r):
                found.append(rel)
    return found


def digest(paths):
    return hashlib.sha256("".join(p + "\n" for p in sorted(paths)).encode("utf-8")).hexdigest()


def verify(record, root, strict):
    top_rc, top = git(root, "rev-parse", "--show-toplevel")
    if top_rc != 0 or os.path.realpath(top.decode().strip()) != os.path.realpath(root):
        raise Setup("ROOT", f"{root} is not a git toplevel")
    rows = parse_record(record)
    cache = {}
    listing = tree_files(root, sorted({g for r in rows for g in r["globs"]}))
    findings, rev_ok, tree_same = 0, 0, 0
    lines = []
    for r in rows:
        at_rev = run_at_rev(root, r, cache)
        at_tree = run_on_tree(root, r, listing)
        codes = []
        if len(at_rev) != r["n"]:
            codes.append("COUNT_DRIFT")
        if "digest" in r:
            if digest(at_rev) != r["digest"]:
                codes.append("SET_DRIFT")
        elif sorted(r["set"]) != at_rev:
            codes.append("SET_DRIFT")
        changed = at_tree != at_rev
        if changed:
            codes.append("TREE_CHANGED")
        bad = [c for c in codes if c != "TREE_CHANGED" or strict]
        findings += len(bad)
        rev_ok += 0 if ("COUNT_DRIFT" in codes or "SET_DRIFT" in codes) else 1
        tree_same += 0 if changed else 1
        lines.append(
            f"SEARCH_RERUN {r['id']} rev={'DRIFT' if ('COUNT_DRIFT' in codes or 'SET_DRIFT' in codes) else 'MATCH'}"
            f" tree={'CHANGED' if changed else 'SAME'} recorded={r['n']} at_rev={len(at_rev)}"
            f" at_tree={len(at_tree)}" + ("" if not codes else " " + ",".join(codes)))
    n = len(rows)
    for ln in lines:
        print(ln)
    print(f"SEARCH_RERUN_SUMMARY searches={n} rev_match={rev_ok}/{n} tree_same={tree_same}/{n} findings={findings}")
    print("SEARCH_RERUN: " + ("CLEAN" if findings == 0 else "DRIFT"))
    return 0 if findings == 0 else 1


def main(argv):
    ap = argparse.ArgumentParser(prog="search-rerun.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("verify")
    v.add_argument("record")
    v.add_argument("--root", default=".")
    v.add_argument("--strict", action="store_true")
    a = ap.parse_args(argv)
    try:
        return verify(a.record, os.path.abspath(a.root), a.strict)
    except Setup as exc:
        print(f"SEARCH_RERUN_ERROR {exc.code} {exc.detail}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
