#!/usr/bin/env python3
"""search-rerun.py — re-run a search record's expressions as run and compare what they found (round 95).

A search record (PRISMA-S, `knowledge/search-rerun-record-r95.md`) files each search's strategy "copied and
pasted exactly as run" (item 8), the date it ran (item 13) and the number of records it identified (item 15).
In this lane, `research-gate verify-sweeps` re-checks only that a NEGATIVE sweep's named glob set is empty; no
lane instrument re-executes a recorded expression or compares the count it recorded (sibling lanes hold
count re-checks of their own — tameshi `tools/count-recheck.py`, kagi `corpus/recheck-replay.py` — which re-run one
pinned command; this tool reads a search record's table). This tool does, for local searches over committed lane
files:

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
              compared with `grep -P`); both match line by line, as GNU grep does on text: a line is the bytes
              between `\\n`, and a final `\\n` ends the last line rather than opening an empty one (an empty file
              has no lines); a file is a hit when at least one of its lines matches, as `grep -l`
  where       comma-separated globs relative to ROOT, matched segment by segment as bash matches them without
              `globstar`: `*`, `?` and `[...]` stay inside one segment and never match a leading `.` (a dotfile is
              matched only by a segment that itself starts with `.`); `**` is refused (it is not a bash glob
              without globstar); no absolute path, no `..`, no `.`, no empty segment, no backslash
  expression  wrapped in one pair of backticks; never empty. A `|` inside the cell is written `\\|` (the Markdown
              table escape): the bytes run are the cell with every `\\|` read as `|`, so a record can file an
              alternation but not a literal backslash-pipe
  rev         the full 40-hex commit the search ran against
  searched    the date the search ran, `YYYY-MM-DD`
  hits        the number of matching files, decimal
  hit_set     `-` when hits is 0; otherwise the comma-separated matching paths (a path containing a comma cannot
              be listed — use the digest), or `sha256:<64 hex>` of the matching paths as bytes, byte-sorted, each
              followed by `\\n` (what `grep -l … | LC_ALL=C sort | sha256sum` prints)

Usage:
    python3 tools/search-rerun.py verify RECORD [--root LANE] [--strict]
    python3 tools/search-rerun.py --selftest

`--selftest` (round 96, extended in round 97) runs in-memory cases against expectations fixed in the tool — the
round-96 32 (14 parse, 8 matching, 10 judgement cases that call `evaluate`, the function `verify` also calls) plus
round-97 cases `r01`-`r16` (signed hits, bad date, uppercase rev, `Q0`, empty expression, empty glob segment,
trailing comma, a 7-cell separator, an uppercase digest read as a path, glob longer than path, regex mid-line and
non-UTF-8 lines, a literal-filename static directory, all three `git_env` guards and the full `GIT_*` scrub, a
two-code row, a digest row judged at the revision) — and prints `SELFTEST <case> ok|FAIL`, then
`SEARCH_RERUN_SELFTEST: PASS|FAIL cases=<k>/<n>`; exit 0 PASS, 1 FAIL. Every case runs inside a guard, and the
shared fixture set-up runs inside an outer guard, so an exception becomes a FAIL line and the summary still prints.
It is written to read no file, run no git and open no socket (observed by seats, not enforced by a battery leg). It
does not exercise the git and disk readers, nor whether `verify` uses `evaluate`'s verdict; the round-95 battery
does both through the CLI.

Output, one line per search, then a summary and a verdict:
    SEARCH_RERUN <id> rev=<MATCH|DRIFT> tree=<SAME|CHANGED> recorded=<n> at_rev=<n> at_tree=<n> [codes]
    SEARCH_RERUN_SUMMARY searches=<n> rev_match=<k>/<n> tree_same=<m>/<n> findings=<f>
    SEARCH_RERUN: CLEAN | DRIFT
Exit: 0 every search matches at its rev (tree changes allowed unless --strict); 1 any COUNT_DRIFT or SET_DRIFT
(or TREE_CHANGED under --strict); 2 setup — `SEARCH_RERUN_ERROR <code> <detail>` on stderr for a missing or
unreadable record, no `## Searches` section, a wrong header, a malformed or duplicate row, a table line after the
first table ends (a second table, or a row after a blank line), an unknown engine, an empty or uncompilable
expression, a regex using a POSIX bracket class (`[[:alpha:]]` — PCRE syntax that Python reads as a different
set), an unsafe glob, a rev that is not a commit of ROOT's repository, a symlink or non-regular file matched by a
glob, or a ROOT that is not a git toplevel.

Named limits: the regex engine is Python `re`, not PCRE — beyond the refused POSIX classes, a pattern whose
meaning differs between them is compared under Python's meaning, and PCRE-only syntax Python cannot compile
(e.g. `\\K`) is a setup refusal; `\\w`, `\\s` and `\\b` follow Python's Unicode rules, which agree with GNU grep
under a UTF-8 locale and not under `LC_ALL=C`; a file containing NUL bytes is matched as text, while GNU grep
switches to binary mode on it and may split lines differently; a match never spans a newline; the tree re-run reads
the files on disk, tracked or not; the tool proves the record agrees with what the expression finds, not that the
expression was the right one to run (recall is not measured).

Reads the RECORD named on the command line (a relative RECORD is resolved against ROOT; a symlinked RECORD is
refused, `RECORD_TYPE`), ROOT's files under each glob's static directory, and ROOT's git objects through read-only
`git ls-tree`/`git cat-file` run with every caller `GIT_*` variable removed, replace refs off and lazy fetch off —
so a partial clone's missing blob is a setup error, not a network fetch. Objects reached through ROOT's own
`objects/info/alternates` (a `--shared` clone) are ROOT's objects by its own configuration. No writes.
Python 3.13+ standard library only.
"""
import argparse
import fnmatch
import hashlib
import os
import re
import subprocess
import sys

HEADER = ["id", "engine", "where", "expression", "rev", "searched", "hits", "hit_set"]
ENGINES = ("fixed", "regex")
ID_RE = re.compile(r"Q[1-9][0-9]*\Z")
REV_RE = re.compile(r"[0-9a-f]{40}\Z")
DATE_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\Z")
HITS_RE = re.compile(r"(0|[1-9][0-9]*)\Z")
DIGEST_RE = re.compile(r"sha256:[0-9a-f]{64}\Z")
SPLIT_RE = re.compile(r"(?<!\\)\|")
POSIX_CLASS_RE = re.compile(r"\[:[A-Za-z]+:\]")


class Setup(Exception):
    def __init__(self, code, detail):
        super().__init__(f"{code} {detail}")
        self.code = code
        self.detail = detail


def git_env():
    """The caller's environment without any GIT_* variable (GIT_DIR, GIT_OBJECT_DIRECTORY, GIT_ALTERNATE_OBJECT_
    DIRECTORIES, GIT_CONFIG_* … would point the re-run at another object store), with replace refs and lazy
    (promisor) fetches switched off: a missing object is a setup error, never a network fetch into ROOT
    (round 95, R95SentinelScope findings 1, 2, 4)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"GIT_NO_REPLACE_OBJECTS": "1", "GIT_NO_LAZY_FETCH": "1", "GIT_TERMINAL_PROMPT": "0"})
    return env


def git(root, *args):
    p = subprocess.run(["git", "-C", root, *args], capture_output=True, env=git_env())
    return p.returncode, p.stdout


def cells(line):
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")) or len(s) < 2:
        return None
    return [c.strip().replace("\\|", "|") for c in SPLIT_RE.split(s[1:-1])]


def parse_record(path):
    try:
        if os.path.islink(path):
            raise Setup("RECORD_TYPE", f"{path}: the record must be a regular file, not a symlink")
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        raise Setup("RECORD_UNREADABLE", f"{path}: {exc}")
    return parse_text(text)


def parse_text(text):
    """Parse a record's text (the `## Searches` table) into rows; raises Setup on any malformed part."""
    lines = text.split("\n")
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
    while i < len(lines) and not lines[i].startswith("## "):
        if lines[i].strip().startswith("|"):
            raise Setup("TABLE", f"line {i + 1}: a table line after the first table ends (a second table or a row "
                                 "after a break would never be re-run)")
        i += 1
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
            if POSIX_CLASS_RE.search(r["expr"]):
                raise Setup("EXPRESSION", f"{r['id']}: POSIX bracket class (PCRE syntax Python reads differently)")
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
            if "**" in g:
                raise Setup("WHERE", f"{r['id']}: '**' is not a bash glob without globstar: {g!r}")
        r["globs"] = globs
        rows.append(r)
    return rows


def seg_match(name, pat):
    """One path segment against one glob segment, as bash without dotglob: a leading `.` is never wildcard-matched."""
    if name.startswith(".") and not pat.startswith("."):
        return False
    return fnmatch.fnmatchcase(name, pat)


def matches(path, globs):
    segs = path.split("/")
    for g in globs:
        pats = g.split("/")
        if len(pats) == len(segs) and all(seg_match(s, p) for s, p in zip(segs, pats)):
            return True
    return False


def lines_of(data):
    """GNU grep's text lines: a final newline ends the last line; an empty file has none."""
    lines = data.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()
    return lines


def hit(data, r):
    for line in lines_of(data):
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
        p = subprocess.run(["git", "-C", root, "cat-file", "blob", obj], capture_output=True, env=git_env())
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
    """sha256 of the paths as bytes, byte-sorted, each followed by a newline: what `LC_ALL=C sort | sha256sum` prints
    for `grep -l` output, also for a path that is not valid UTF-8 (read with surrogateescape)."""
    keys = sorted(p.encode("utf-8", "surrogateescape") for p in paths)
    return hashlib.sha256(b"".join(k + b"\n" for k in keys)).hexdigest()


def evaluate(rows, at_rev_of, at_tree_of, strict):
    """Judge every row from its two re-runs; `at_rev_of(r)` and `at_tree_of(r)` return sorted matching paths.
    Shared by `verify` (git and disk re-runs) and `--selftest` (in-memory re-runs), so the selftest scores the same
    decision code the CLI runs (round 96)."""
    findings, rev_ok, tree_same = 0, 0, 0
    lines = []
    for r in rows:
        at_rev = at_rev_of(r)
        at_tree = at_tree_of(r)
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
    return findings, rev_ok, tree_same, lines


def verify(record, root, strict):
    top_rc, top = git(root, "rev-parse", "--show-toplevel")
    if top_rc != 0 or os.path.realpath(top.decode().strip()) != os.path.realpath(root):
        raise Setup("ROOT", f"{root} is not a git toplevel")
    rows = parse_record(record)
    cache = {}
    listing = tree_files(root, sorted({g for r in rows for g in r["globs"]}))

    def at_rev_of(r):
        at_rev = run_at_rev(root, r, cache)
        return at_rev

    def at_tree_of(r):
        return run_on_tree(root, r, listing)

    findings, rev_ok, tree_same, lines = evaluate(rows, at_rev_of, at_tree_of, strict)
    n = len(rows)
    for ln in lines:
        print(ln)
    print(f"SEARCH_RERUN_SUMMARY searches={n} rev_match={rev_ok}/{n} tree_same={tree_same}/{n} findings={findings}")
    print("SEARCH_RERUN: " + ("CLEAN" if findings == 0 else "DRIFT"))
    return 0 if findings == 0 else 1


ST_HEAD = ("## Searches\n\n| id | engine | where | expression | rev | searched | hits | hit_set |\n"
           "|---|---|---|---|---|---|---|---|\n")
ST_REV = "a" * 40
ST_AB_DIGEST = "1f89e694bffa56052d9fb134ec6d9fbd05d1fdb27003772c06ad4ba8175ecd50"  # sha256 of b"corpus/a.txt\ncorpus/b.txt\n"
ST_AC_DIGEST = "b5ffc9674501cd88b9070cfa973f489c13bae3e6ace1a78054de8f0789ff64ea"  # sha256 of b"corpus/a.txt\ncorpus/c.txt\n"


def st_row(qid="Q1", engine="fixed", where="corpus/*.txt", expr="`PRESS`", rev=ST_REV, hits="1",
           hit_set="corpus/a.txt", searched="2026-11-09"):
    return f"| {qid} | {engine} | {where} | {expr} | {rev} | {searched} | {hits} | {hit_set} |\n"


def _selftest_cases(case):
    """The self-test's cases (round 96 p/m/j, round 97 r01-r16), each registered through `case`; the shared fixtures
    below are built here, inside the caller's outer guard."""
    def refused(text):
        try:
            parse_text(text)
        except Setup as exc:
            return exc.code
        return None

    def refusal(code, text):
        return lambda: (lambda got: (got == code, f"want={code} got={got}"))(refused(text))

    good = ST_HEAD + st_row()
    case("p01-parse-good", lambda: len(parse_text(good)) == 1)
    for cid, text, code in (
        ("p02-no-section", good.replace("## Searches", "## Search"), "SECTION"),
        ("p03-header", good.replace("| hits | hit_set |", "| count | hit_set |"), "HEADER"),
        ("p04-engine", ST_HEAD + st_row(engine="pcre"), "ENGINE"),
        ("p05-globstar", ST_HEAD + st_row(where="corpus/**/*.txt"), "WHERE"),
        ("p06-dotdot", ST_HEAD + st_row(where="corpus/../x/*.txt"), "WHERE"),
        ("p07-posix-class", ST_HEAD + st_row(engine="regex", expr="`[[:alpha:]]+`"), "EXPRESSION"),
        ("p08-backtick", ST_HEAD + st_row(expr="`a`b`"), "EXPRESSION"),
        ("p09-short-rev", ST_HEAD + st_row(rev="abc"), "REV"),
        ("p10-zero-with-set", ST_HEAD + st_row(hits="0"), "HIT_SET"),
        ("p11-dup-id", ST_HEAD + st_row() + st_row(), "ROW"),
        ("p12-row-after-break", ST_HEAD + st_row() + "\n" + st_row(qid="Q2"), "TABLE"),
        ("p13-absolute-glob", ST_HEAD + st_row(where="/corpus/*.txt"), "WHERE"),
        # round 97: inputs the round-96 cases never supplied (R96MutantsC1 class C)
        ("r01-signed-hits", ST_HEAD + st_row(hits="-1"), "HITS"),
        ("r02-bad-date", ST_HEAD + st_row(searched="2026-11-9"), "DATE"),
        ("r03-upper-rev", ST_HEAD + st_row(rev="A" * 40), "REV"),
        ("r04-q0-id", ST_HEAD + st_row(qid="Q0"), "ROW"),
        ("r05-empty-expression", ST_HEAD + st_row(expr="``"), "EXPRESSION"),
        ("r06-empty-segment", ST_HEAD + st_row(where="corpus//*.txt"), "WHERE"),
        ("r07-trailing-comma", ST_HEAD + st_row(hits="1", hit_set="corpus/a.txt,"), "HIT_SET"),
        ("r16-sep-width", good.replace("|---|---|---|---|---|---|---|---|", "|---|---|---|---|---|---|---|"), "TABLE"),
    ):
        case(cid, refusal(code, text))

    def p14():
        alt = parse_text(ST_HEAD + st_row(engine="regex", expr="`^(x\\|b)$`"))[0]
        return alt["expr"] == "^(x|b)$" and hit(b"a\nb\n", alt), repr(alt["expr"])
    case("p14-escaped-pipe", p14)

    def r08():
        r = parse_text(ST_HEAD + st_row(hit_set="sha256:" + "A" * 64))[0]
        return "digest" not in r and r.get("set") == ["sha256:" + "A" * 64], repr(sorted(r))
    case("r08-upper-digest-is-a-path", r08)

    case("m01-lines", lambda: lines_of(b"a\n") == [b"a"] and lines_of(b"") == [] and lines_of(b"a\n\n") == [b"a", b""])
    case("m02-dotfile", lambda: not matches("d/.x.txt", ["d/*.txt"]) and matches("d/.x.txt", ["d/.*.txt"]))
    case("m03-segment", lambda: not matches("d/e/f.txt", ["d/*.txt"]) and matches("d/f.txt", ["d/*.txt"]))
    case("r09-glob-longer", lambda: not matches("d/f.txt", ["d/*/*.txt"]) and not matches("d", ["d/*"]))

    def needles():
        blank = parse_text(ST_HEAD + st_row(engine="regex", expr="`^$`"))[0]
        needle = parse_text(ST_HEAD + st_row(expr="`PRESS`"))[0]
        rx = parse_text(ST_HEAD + st_row(engine="regex", expr="`PRESS`"))[0]
        return blank, needle, rx
    case("m04-per-line", lambda: (lambda b, n, _: not hit(b"a\n", b) and hit(b"a\n\nb\n", b)
                                  and not hit(b"PRE\nSS\n", n) and hit(b"x\nPRESS y\n", n))(*needles()))
    case("m05-case", lambda: not hit(b"press\n", needles()[1]))
    case("r10-regex-mid-line", lambda: hit(b"x PRESS\n", needles()[2]) and not hit(b"x press\n", needles()[2]))
    case("r11-regex-non-utf8", lambda: hit(b"\xff\xfe PRESS\n", needles()[2]))
    case("m06-digest", lambda: digest(["corpus/b.txt", "corpus/a.txt"]) == ST_AB_DIGEST)
    case("m07-static-dir", lambda: static_dir("corpus/captures/*.txt") == "corpus/captures"
         and static_dir("*/x.txt") == "" and static_dir("a/b?/c/d.txt") == "a")
    case("r12-static-dir-literal", lambda: static_dir("corpus/a.txt") == "corpus" and static_dir("a.txt") == "")

    planted = {"GIT_DIR": "/nonexistent", "GIT_OBJECT_DIRECTORY": "/nonexistent/objects",
               "GIT_ALTERNATE_OBJECT_DIRECTORIES": "/nonexistent/alt", "GIT_CONFIG_PARAMETERS": "'core.x=1'",
               "GIT_WORK_TREE": "/nonexistent", "GIT_NO_REPLACE_OBJECTS": "0", "GIT_NO_LAZY_FETCH": "0"}
    saved = {k: os.environ.get(k) for k in planted}
    os.environ.update(planted)
    try:
        env = git_env()
    finally:
        for k, v in saved.items():
            if v is None:
                del os.environ[k]
            else:
                os.environ[k] = v
    case("m08-env-scrub", lambda: "GIT_DIR" not in env and env.get("GIT_NO_LAZY_FETCH") == "1")
    case("r13-env-guards", lambda: (sorted(k for k in env if k.startswith("GIT_")) ==
                                    ["GIT_NO_LAZY_FETCH", "GIT_NO_REPLACE_OBJECTS", "GIT_TERMINAL_PROMPT"]
                                    and env["GIT_NO_REPLACE_OBJECTS"] == "1" and env["GIT_TERMINAL_PROMPT"] == "0",
                                    repr(sorted(k for k in env if k.startswith("GIT_")))))

    base = {"corpus/a.txt": b"PRESS here\n", "corpus/b.txt": b"no\n", "corpus/c.txt": b"PRESS too\n",
            "corpus/.d.txt": b"PRESS hidden\n", "corpus/e/f.txt": b"PRESS nested\n"}
    moved = dict(base, **{"corpus/b.txt": b"PRESS now\n"})
    swapped = dict(base, **{"corpus/b.txt": b"PRESS now\n", "corpus/c.txt": b"gone\n"})

    def mem(files):
        return lambda r: sorted(p for p in files if matches(p, r["globs"]) and hit(files[p], r))

    def judge(row, tree, strict=False):
        rows = parse_text(ST_HEAD + row)
        f, ok, same, lines = evaluate(rows, mem(base), mem(tree), strict)
        codes = lines[0].split()[7].split(",") if len(lines[0].split()) > 7 else []
        return f, ok, same, codes

    exact = st_row(hits="2", hit_set="corpus/a.txt, corpus/c.txt")
    for cid, row, tree, strict, want in (
        ("j01-exact", exact, base, False, (0, 1, 1, [])),
        ("j02-count", st_row(hits="3", hit_set="corpus/a.txt, corpus/c.txt"), base, False, (1, 0, 1, ["COUNT_DRIFT"])),
        ("j03-set", st_row(hits="2", hit_set="corpus/a.txt, corpus/b.txt"), base, False, (1, 0, 1, ["SET_DRIFT"])),
        ("j04-digest", st_row(hits="2", hit_set="sha256:" + ST_AB_DIGEST), base, False, (1, 0, 1, ["SET_DRIFT"])),
        ("j05-dup-path", st_row(hits="2", hit_set="corpus/a.txt, corpus/c.txt, corpus/a.txt"), base, False,
         (1, 0, 1, ["SET_DRIFT"])),
        ("j06-tree-moved", exact, moved, False, (0, 1, 0, ["TREE_CHANGED"])),
        ("j07-tree-strict", exact, moved, True, (1, 1, 0, ["TREE_CHANGED"])),
        ("j08-tree-swap", exact, swapped, False, (0, 1, 0, ["TREE_CHANGED"])),
        ("j09-zero", st_row(expr="`absent`", hits="0", hit_set="-"), base, False, (0, 1, 1, [])),
        # round 97: a row with two bad codes counts two findings; a digest row judged at the revision, not the tree
        ("r14-two-codes", st_row(hits="3", hit_set="corpus/a.txt, corpus/b.txt"), moved, True,
         (3, 0, 0, ["COUNT_DRIFT", "SET_DRIFT", "TREE_CHANGED"])),
        ("r15-digest-at-rev", st_row(hits="2", hit_set="sha256:" + ST_AC_DIGEST), moved, False,
         (0, 1, 0, ["TREE_CHANGED"])),
    ):
        case(cid, lambda row=row, tree=tree, strict=strict, want=want:
             (lambda got: (got == want, f"want={want} got={got}"))(judge(row, tree, strict)))

    def j10():
        ab = parse_text(ST_HEAD + st_row(hits="2", hit_set="corpus/a.txt, corpus/c.txt")
                        + st_row(qid="Q2", expr="`no`", hits="1", hit_set="corpus/a.txt"))
        f, ok, same, _ = evaluate(ab, mem(base), mem(base), False)
        return (f, ok, same) == (1, 1, 2), f"got={(f, ok, same)}"
    case("j10-tally", j10)



def selftest():
    """In-memory self-test (round 96; round 97 adds cases r01-r16 and two guards): parse refusals, matching rules,
    the digest form, the `git_env` guards and the decision code of `evaluate`, each case against an expectation fixed
    in this file. Every case runs inside a guard, so an exception inside a case (a parse that raises, a decode error)
    is that case's FAIL; the shared fixture set-up runs inside an outer guard, so an exception there (or in `case`
    itself) is a `setup` FAIL — never a traceback that ends the run without a summary line (round-96 `R96MutantsC1`
    class B; round-97 `R97ScribeLesson` F3). No file, git or network access; exit 0 PASS, 1 FAIL. It does not
    exercise the git and disk readers (`run_at_rev`, `run_on_tree`, `tree_files`) — the round-95 battery
    `corpus/evidence/round95/rerun-controls-r95.py` does, through the CLI."""
    results = []

    def case(cid, fn):
        try:
            got = fn()
            ok, detail = got if isinstance(got, tuple) else (got, "")
        except Exception as exc:  # a crash inside a case is that case's failure
            ok, detail = False, f"raised {type(exc).__name__}: {exc}"
        results.append((cid, bool(ok)))
        print(f"SELFTEST {cid} {'ok' if ok else 'FAIL'}" + (f" {detail}" if detail else ""))

    try:
        _selftest_cases(case)
    except Exception as exc:  # a crash in shared set-up (or in `case`) fails the run with a summary
        results.append(("setup", False))
        print(f"SELFTEST setup FAIL raised {type(exc).__name__}: {exc}")

    n, k = len(results), sum(1 for _, ok in results if ok)
    bad = [cid for cid, ok in results if not ok]
    print(f"SEARCH_RERUN_SELFTEST: {'PASS' if k == n else 'FAIL'} cases={k}/{n}" + (f" failed={','.join(bad)}" if bad else ""))
    return 0 if k == n else 1




def main(argv):
    ap = argparse.ArgumentParser(prog="search-rerun.py")
    ap.add_argument("--selftest", action="store_true", help="run the in-memory self-test and exit")
    sub = ap.add_subparsers(dest="cmd")
    v = sub.add_parser("verify")
    v.add_argument("record")
    v.add_argument("--root", default=".")
    v.add_argument("--strict", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        if a.cmd:
            ap.error("--selftest takes no subcommand")
        return selftest()
    if not a.cmd:
        ap.error("a subcommand (verify) or --selftest is required")
    try:
        root = os.path.abspath(a.root)
        record = a.record if os.path.isabs(a.record) else os.path.join(root, a.record)
        return verify(record, root, a.strict)
    except Setup as exc:
        print(f"SEARCH_RERUN_ERROR {exc.code} {exc.detail}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
