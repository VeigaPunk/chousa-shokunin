#!/usr/bin/env python3
"""c1-count — frozen counter for round 49 claim C1 (operability, capability).

Predicate R49-C1, the same sentence as corpus/evidence/round49/claims.md:
`tools/assimilate-rows.py` turns a frozen set of staged campaign entries into
an append block and rewritten entries that pass the fleet census on a scratch
mirror of the lane registry at BASE_REV, renumbering every cited staged id BY
DOCUMENT (held URL -> the lane's existing id; new URL -> the next lane id, in
ascending staged-id order, contiguous from the base maximum) with one
simultaneous substitution, appending exactly the rows the entries cite, each
with status `mined`, the given opened date, a census-valid recheck and a
`used-by` naming exactly the citing entries; it reports the section-10 id
collisions with the 0-3-space pattern (an indented registry row collides);
and it rewrites an escaped-pipe staged cell so the appended row parses as 11
cells. Three package sets (A: this round's theme, B: a collision-chain entry,
C: an entry with held rows) plus the GUARD and PIPE fixtures must all pass.

Tool interface (frozen):

    python3 tools/assimilate-rows.py --staged FILE --knowledge DIR \
        --registry FILE --opened YYYY-MM-DD --out DIR [--entry REL ...]

writes into DIR: `reg-ids`, `staged-ids`, `collisions` (sorted ids, one per
line); with at least one --entry also `renumber.tsv` (header
`staged_id lane_id action url`, action `append` or `held`), `append.md` (the
appended rows only, in lane-id order), `stripped.tsv` (header
`lane_id column stripped`) and every entry rewritten at DIR/REL. Exit 0 done,
1 refused, 2 usage.

Usage: python3 corpus/evidence/round49/c1-count.py [--tool PATH] [--root LANE]
Exit codes: 0 every leg holds · 1 a leg failed · 2 env (package changed, no git).
"""
from __future__ import annotations

import argparse
import hashlib
import io
import pathlib
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[3]
FLEET = pathlib.Path("/home/vgpnk/Projects/shokunin")
CENSUS = FLEET / "scripts" / "sources-census.sh"
PKG = pathlib.Path("/home/vgpnk/Projects/shokuknow/merge/chousa")
STAGED = PKG / "SOURCES.append.md"
KNOW = PKG / "knowledge"
BASE_REV = "414a2ec6cde05a921dbdd9e02e7ae56b0db647ef"
OPENED = "2026-10-25"
PINS = {
    "SOURCES.append.md": "a6dec4a0086d3cf767d638d7e52fdda08f78d22b0b376049b0ad14ff0f8aa696",
    "knowledge/corpus/knowledge/aggregator-vs-source-r36.md": "29b9ad256f30af2de305a3a5a3616f615690c89e0a05b72441d963c6a3f22156",
    "knowledge/corpus/knowledge/citation-count-semantics-r37.md": "68a8db1a34fd0dcdada465c5d69be14798cdab90af4b177c8c8c3574cd6db5ea",
    "knowledge/corpus/knowledge/search-log-fields-r36.md": "1396d827b9e06f3ad84a51afb6ddadc92487b1d30000618babd5f7190e7c2549",
    "knowledge/corpus/knowledge/grey-literature-and-chinese-search-record-r40.md": "200d30711656b3e310470526873975d32ee44f064646d33a22c1975209617cb8",
}
SETS = {
    "A": ["corpus/knowledge/aggregator-vs-source-r36.md",
          "corpus/knowledge/citation-count-semantics-r37.md"],
    "B": ["corpus/knowledge/search-log-fields-r36.md"],
    "C": ["corpus/knowledge/grey-literature-and-chinese-search-record-r40.md"],
}
ROW_RE = re.compile(r"^ {0,3}\|[ \t]*(S\d{3,})[ \t]*\|")
GREP_RE = re.compile(r"^ {0,3}\|[ \t\r\f\v]*(S[0-9]{3,})")  # the section-10 grep, whole file
TOKEN_RE = re.compile(r"\bS\d{3,}\b")
RECHECK_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}|\d+d|[A-Za-z][A-Za-z0-9 _-]*)$")
ESC_SPLIT = re.compile(r"(?<!\\)\|")


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def url_of(source: str) -> str:
    """The census's url_of(): first http(s) URL, fragment and trailing slash
    dropped, scheme dropped, host lower-cased."""
    m = re.search(r"https?://[^\s|]+", source)
    if not m:
        return ""
    u = m.group(0)
    u = re.sub(r"#[^ ]*$", "", u)
    u = re.sub(r"/$", "", u)
    u = re.sub(r"^[A-Za-z]+://", "", u)
    n = u.find("/")
    return (u[:n].lower() + u[n:]) if n >= 0 else u.lower()


def staged_rows(text: str) -> dict[str, list[str]]:
    out = {}
    for line in text.splitlines():
        m = ROW_RE.match(line)
        if m:
            cells = [c.strip() for c in ESC_SPLIT.split(line.strip())[1:-1]]
            out.setdefault(m.group(1), cells)
    return out


def registry_rows(text: str) -> dict[str, list[str]]:
    out, inside = {}, False
    for line in text.splitlines():
        s = line.lstrip(" ")
        if len(line) - len(s) <= 3 and s.startswith("## "):
            inside = s[3:].strip() == "Registry"
            continue
        if len(line) - len(s) <= 3 and s.startswith("# "):
            inside = False
            continue
        m = ROW_RE.match(line)
        if inside and m:
            out.setdefault(m.group(1), [c.strip() for c in s.strip().split("|")[1:-1]])
    return out


def grep_ids(text: str) -> list[str]:
    return sorted({m.group(1) for line in text.splitlines() if (m := GREP_RE.match(line))})


def num(sid: str) -> int:
    return int(sid[1:])


def insert_rows(reg_text: str, rows: list[str]) -> str:
    lines = reg_text.splitlines()
    inside, last = False, None
    for i, line in enumerate(lines):
        s = line.lstrip(" ")
        if s.startswith("## "):
            inside = s[3:].strip() == "Registry"
            continue
        if inside and s.startswith("|"):
            last = i
    if last is None:
        return reg_text
    return "\n".join(lines[:last + 1] + rows + lines[last + 1:]) + "\n"


def census(file: pathlib.Path) -> tuple[int, str]:
    p = subprocess.run(["bash", str(CENSUS), "validate", "--file", str(file)],
                       capture_output=True, text=True)
    errs = [l for l in p.stdout.splitlines() if re.search(r"\tE\d\d\t", l)]
    return p.returncode, ";".join(l.split("\t", 1)[1] for l in errs)[:300]


def make_mirror(base: pathlib.Path, dest: pathlib.Path) -> None:
    """A scratch lane mirror: the base registry copied (writable), every
    knowledge file linked into a real directory (so new entries can be added),
    every other path linked to the base tree (the census E11 check is an
    existence test)."""
    dest.mkdir()
    for top in base.iterdir():
        if top.name != "corpus":
            (dest / top.name).symlink_to(top)
    (dest / "corpus").mkdir()
    for item in (base / "corpus").iterdir():
        if item.name == "SOURCES.md":
            shutil.copyfile(item, dest / "corpus" / "SOURCES.md")
        elif item.name != "knowledge":
            (dest / "corpus" / item.name).symlink_to(item)
    (dest / "corpus" / "knowledge").mkdir()
    for item in (base / "corpus" / "knowledge").iterdir():
        (dest / "corpus" / "knowledge" / item.name).symlink_to(item)


def place(mirror: pathlib.Path, rel: str, src: pathlib.Path) -> None:
    dst = mirror / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.is_symlink():
        dst.unlink()
    shutil.copyfile(src, dst)


def run_tool(tool: pathlib.Path, staged: pathlib.Path, know: pathlib.Path,
             registry: pathlib.Path, out: pathlib.Path, entries: list[str]) -> int:
    cmd = [sys.executable, str(tool), "--staged", str(staged), "--knowledge", str(know),
           "--registry", str(registry), "--opened", OPENED, "--out", str(out)]
    for e in entries:
        cmd += ["--entry", e]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=120).returncode
    except subprocess.TimeoutExpired:
        return 124


def read_tsv(p: pathlib.Path, header: list[str]) -> list[list[str]] | None:
    if not p.is_file():
        return None
    lines = p.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].split("\t") != header:
        return None
    return [l.split("\t") for l in lines[1:] if l.strip()]


def check_set(name: str, tool: pathlib.Path, staged: pathlib.Path, know: pathlib.Path,
              base_reg: pathlib.Path, mirror_src: pathlib.Path, entries: list[str],
              tmp: pathlib.Path) -> bool:
    out = tmp / f"out-{name}"
    rc = run_tool(tool, staged, know, base_reg, out, entries)
    base_text = base_reg.read_text(encoding="utf-8")
    base = registry_rows(base_text)
    st_text = staged.read_text(encoding="utf-8")
    st = staged_rows(st_text)
    base_urls: dict[str, str] = {}
    for sid in sorted(base, key=num):
        u = url_of(base[sid][1]) if len(base[sid]) > 1 else ""
        if u:
            base_urls.setdefault(u, sid)
    texts = {e: (know / e).read_text(encoding="utf-8") for e in entries}
    cited = sorted({t for tx in texts.values() for t in TOKEN_RE.findall(tx) if t in st}, key=num)
    # expected mapping, by document
    nxt = max(num(s) for s in base) + 1
    want: dict[str, tuple[str, str]] = {}
    for sid in cited:
        u = url_of(st[sid][1])
        if u and u in base_urls:
            want[sid] = (base_urls[u], "held")
        else:
            want[sid] = (f"S{nxt:03d}", "append")
            nxt += 1
    users = {sid: sorted(e for e, tx in texts.items() if sid in TOKEN_RE.findall(tx)) for sid in cited}

    ren = read_tsv(out / "renumber.tsv", ["staged_id", "lane_id", "action", "url"]) or []
    got = {r[0]: (r[1], r[2]) for r in ren if len(r) == 4}
    by_doc = sum(1 for sid in cited if got.get(sid) == want[sid])
    extra = sorted(set(got) - set(cited))
    sub = {sid: want[sid][0] for sid in cited}
    rew_ok = 0
    for e, tx in texts.items():
        exp = TOKEN_RE.sub(lambda m: sub.get(m.group(0), m.group(0)), tx)
        p = out / e
        rew_ok += p.is_file() and p.read_text(encoding="utf-8") == exp
    app_path = out / "append.md"
    app_lines = [l for l in app_path.read_text(encoding="utf-8").splitlines() if l.strip()] if app_path.is_file() else []
    n_append = sum(1 for v in want.values() if v[1] == "append")
    app_rows = {}
    shape = 0
    for l in app_lines:
        cells = [c.strip() for c in l.strip().split("|")[1:-1]]
        if len(cells) == 11 and "\\|" not in l and l.lstrip(" ").startswith("|"):
            shape += 1
            app_rows[cells[0]] = cells
    want_app = [v[0] for v in sorted(want.values(), key=lambda v: num(v[0])) if v[1] == "append"]
    contiguous = [r for r in app_rows] == want_app
    used = norm = url_ok = 0
    for sid in cited:
        lid, act = want[sid]
        if act != "append":
            continue
        cells = app_rows.get(lid)
        if not cells:
            continue
        url_ok += url_of(cells[1]) == url_of(st[sid][1]) and url_of(cells[1]) != ""
        used += [c.strip() for c in cells[10].split(",")] == users[sid]
        norm += (cells[7] == "mined" and cells[8] == OPENED and bool(RECHECK_RE.match(cells[9])))
    held_ok = sum(1 for sid in cited if want[sid][1] == "held"
                  and url_of(base[want[sid][0]][1]) == url_of(st[sid][1]))
    n_held = sum(1 for v in want.values() if v[1] == "held")
    coll_want = sorted(set(grep_ids(base_text)) & set(grep_ids(st_text)))
    coll_p = out / "collisions"
    coll_got = [l.strip() for l in coll_p.read_text(encoding="utf-8").splitlines() if l.strip()] if coll_p.is_file() else None
    # scratch mirror census
    mirror = tmp / f"mirror-{name}"
    make_mirror(mirror_src, mirror)
    reg = mirror / "corpus" / "SOURCES.md"
    reg.write_text(insert_rows(reg.read_text(encoding="utf-8"), app_lines), encoding="utf-8")
    for e in entries:
        src = out / e
        if src.is_file():
            place(mirror, e, src)
    crc, cerr = census(reg)
    ok = (rc == 0 and crc == 0 and by_doc == len(cited) and not extra
          and rew_ok == len(entries) and len(app_lines) == n_append and shape == n_append
          and contiguous and url_ok == n_append and used == n_append and norm == n_append
          and held_ok == n_held and coll_got == coll_want)
    print(f"SET_{name} TOOL_EXIT={rc} CITED={len(cited)} APPEND={len(app_lines)}/{n_append} HELD={held_ok}/{n_held} "
          f"BY_DOC={by_doc}/{len(cited)} EXTRA={len(extra)} REWRITE={rew_ok}/{len(entries)} SHAPE={shape}/{n_append} "
          f"CONTIGUOUS={'yes' if contiguous else 'no'} URL={url_ok}/{n_append} USED_BY={used}/{n_append} "
          f"NORMALIZED={norm}/{n_append} COLLISIONS={'match' if coll_got == coll_want else 'differ'} "
          f"CENSUS={'ok' if crc == 0 else f'exit{crc}'}{(' ' + cerr) if cerr else ''} -> {'PASS' if ok else 'FAIL'}")
    return ok


HEADER = ("| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
          "|---|---|---|---|---|---|---|---|---|---|---|\n")


def guard_leg(tool: pathlib.Path, tmp: pathlib.Path) -> bool:
    g = tmp / "guard"
    (g / "know").mkdir(parents=True)
    reg = g / "SOURCES.md"
    reg.write_text("# guard\n\n## Registry\n\n" + HEADER +
                   "| S001 | Alpha — https://guard.example/a | docs | A | s | a | t | queued | 2026-10-01 | 30d | — |\n"
                   "  | S002 | Beta — https://guard.example/b | docs | A | s | a | t | queued | 2026-10-01 | 30d | — |\n",
                   encoding="utf-8")
    st = g / "staged.md"
    st.write_text(HEADER + "| S002 | Gamma — https://guard.example/c | docs | A | s | a | t | mined | 2026-10-01 | 30d | x |\n"
                  "| S003 | Delta — https://guard.example/d | docs | A | s | a | t | mined | 2026-10-01 | 30d | x |\n",
                  encoding="utf-8")
    rc = run_tool(tool, st, g / "know", reg, g / "out", [])
    p = g / "out" / "collisions"
    got = [l.strip() for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.is_file() else None
    ok = rc == 0 and got == ["S002"]
    print(f"GUARD TOOL_EXIT={rc} COLLISIONS={got} -> {'PASS' if ok else 'FAIL'}")
    return ok


def pipe_leg(tool: pathlib.Path, base_reg: pathlib.Path, mirror_src: pathlib.Path, tmp: pathlib.Path) -> bool:
    g = tmp / "pipe"
    ent = "corpus/knowledge/pipe-fixture-r49.md"
    (g / "know" / "corpus" / "knowledge").mkdir(parents=True)
    (g / "know" / ent).write_text("# pipe fixture\n\nsource: S990 — https://pipe.example/page\n", encoding="utf-8")
    st = g / "staged.md"
    st.write_text(HEADER + "| S990 | Pipe page — https://pipe.example/page | docs | B | pipe fixture | "
                  "section a \\| b, char 10 | a cell that held an escaped pipe | mined | 2026-10-23 | "
                  "90d — re-open the page and confirm a \\| b | corpus/knowledge/elsewhere.md |\n", encoding="utf-8")
    rc = run_tool(tool, st, g / "know", base_reg, g / "out", [ent])
    app = g / "out" / "append.md"
    lines = [l for l in app.read_text(encoding="utf-8").splitlines() if l.strip()] if app.is_file() else []
    cells = [c.strip() for c in lines[0].strip().split("|")[1:-1]] if len(lines) == 1 else []
    stripped = read_tsv(g / "out" / "stripped.tsv", ["lane_id", "column", "stripped"]) or []
    mirror = g / "mirror"
    make_mirror(mirror_src, mirror)
    reg = mirror / "corpus" / "SOURCES.md"
    reg.write_text(insert_rows(reg.read_text(encoding="utf-8"), lines), encoding="utf-8")
    src = g / "out" / ent
    if src.is_file():
        place(mirror, ent, src)
    crc, cerr = census(reg)
    ok = (rc == 0 and len(cells) == 11 and "\\|" not in "".join(lines) and cells[9] == "90d"
          and cells[10] == ent and any(r[0] == cells[0] and r[1] == "recheck" for r in stripped if len(r) == 3)
          and crc == 0)
    print(f"PIPE TOOL_EXIT={rc} ROWS={len(lines)} CELLS={len(cells)} RECHECK={cells[9] if len(cells) == 11 else '-'} "
          f"STRIPPED_LOGGED={'yes' if any(len(r) == 3 and r[1] == 'recheck' for r in stripped) else 'no'} "
          f"CENSUS={'ok' if crc == 0 else f'exit{crc}'}{(' ' + cerr) if cerr else ''} -> {'PASS' if ok else 'FAIL'}")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--tool", default=None)
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    tool = pathlib.Path(a.tool).resolve() if a.tool else root / "tools" / "assimilate-rows.py"
    for rel, digest in PINS.items():
        p = PKG / rel
        if not p.is_file() or sha(p) != digest:
            print(f"PACKAGE_CHANGED {rel}")
            return 2
    if not CENSUS.is_file():
        print("NO_CENSUS")
        return 2
    print(f"BASE_REV={BASE_REV}")
    if not tool.is_file():
        print("TOOL=absent")
        print("C1=FAIL")
        return 1
    print(f"TOOL=present sha256={sha(tool)}")
    with tempfile.TemporaryDirectory(prefix="chousa-r49-c1-") as td:
        tmp = pathlib.Path(td)
        # base tree at BASE_REV: corpus/ real bytes; every other tracked path an
        # empty placeholder (the census only tests used-by paths for existence)
        arch = subprocess.run(["git", "-C", str(LANE), "archive", BASE_REV, "corpus"],
                              capture_output=True)
        names = subprocess.run(["git", "-C", str(LANE), "ls-tree", "-r", "-z", "--name-only", BASE_REV],
                               capture_output=True, text=True)
        if arch.returncode != 0 or names.returncode != 0:
            print("NO_BASE_REV")
            return 2
        mirror_src = tmp / "base"
        mirror_src.mkdir()
        with tarfile.open(fileobj=io.BytesIO(arch.stdout)) as tf:
            tf.extractall(mirror_src, filter="data")
        for rel in names.stdout.split("\0"):
            if not rel or rel.startswith("corpus/"):
                continue
            p = mirror_src / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.touch()
        base_reg = tmp / "base-SOURCES.md"
        shutil.copyfile(mirror_src / "corpus" / "SOURCES.md", base_reg)
        make_mirror(mirror_src, tmp / "mirror-base")
        brc, berr = census(tmp / "mirror-base" / "corpus" / "SOURCES.md")
        print(f"BASE_CENSUS={'ok' if brc == 0 else f'exit{brc} ' + berr}")
        if brc != 0:
            return 2
        passed = 0
        for name, entries in SETS.items():
            passed += check_set(name, tool, STAGED, KNOW, base_reg, mirror_src, entries, tmp)
        g = guard_leg(tool, tmp)
        p = pipe_leg(tool, base_reg, mirror_src, tmp)
    print(f"SETS_PASS={passed}/{len(SETS)}")
    ok = passed == len(SETS) and g and p
    print("C1=PASS" if ok else "C1=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
