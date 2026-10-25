#!/usr/bin/env python3
"""c2-count — frozen counter for round 47 claim C2 (calibration).

Predicate R47-C2, the same sentence as corpus/evidence/round47/claims.md:
the lane's gate registry (the `## Gates` rows of SKILL.md) agrees with the
tree its own checks depend on, measured as MISMATCHES = UNREGISTERED +
DANGLING = 0 with ENTRY_POINTS >= FLOOR, where

  ENTRY_POINTS is the union of
    A–C. the round-46 set, unchanged (`corpus/evidence/round46/c2-count.py`,
         imported and pinned by sha256);
    D.   DEPENDENCE: every existing repo-relative `*.py`/`*.sh` path named as
         a literal inside the source of an entry point (closed under the
         relation: a script a gate reads or runs is itself a gate input);
    E.   CHECK-NAMED: every existing repo-relative `*.py`/`*.sh` path named in
         `corpus/QUALITY.md` or in `SKILL.md` outside its `## Gates` section
         (a criterion's `Check:` line is a gate the registry must carry —
         round-46 `RevC2TagCount`: `corpus/evidence/round45/tag-count.py`);
  UNREGISTERED is an entry point no Gates row names IN ITS `entry` CELL (the
  third cell) of a row whose `verdict map` cell (the fourth) names an exit
  code — the round-46 row rule plus cell roles (round-46 closure routed
  defect 4: a path anywhere in an eight-pipe row with `exit` anywhere
  registered);
  DANGLING is a repo-relative `*.py`/`*.sh` path a Gates row names that does
  not exist in the tree (the registry asserts a gate the tree does not hold);
  FLOOR is the freeze-tree ENTRY_POINTS (enforced in code — round-46 closure
  routed defect 2: the round-46 floor was prose only).

Prints `ENTRY_POINTS=n (abc=n dependence=+n check_named=+n) FLOOR=f
GATES_ROWS=k REGISTERED=n/n UNREGISTERED=k DANGLING=k MISMATCHES=k
C2=PASS|FAIL`. Exit 0 iff MISMATCHES=0 and ENTRY_POINTS >= FLOOR; 1
otherwise; 2 usage/env (round-46 instrument missing or changed).

Cheapest gates that would score full marks without the work (QUALITY 60):
the round-46 counter itself (it never reads legs D/E, so it prints C2=PASS on
the base tree while this counter prints UNREGISTERED>0); deleting a QUALITY
`Check:` path or a dependence literal shrinks the set below FLOOR and fails.
A Gates row whose verdict map is wrong still passes: row truth stays a
reader's check, named.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import pathlib
import re
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
R46 = pathlib.Path("corpus/evidence/round46/c2-count.py")
R46_SHA = "f93cb10795ef7402848ea355680a6b0bd25ad68c8913c24944ef92029c81046f"
FLOOR = 92  # the freeze-tree ENTRY_POINTS (round 47 freeze)


def load_r46(root: pathlib.Path):
    p = root / R46
    if not p.is_file():
        return None, "absent"
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    if sha != R46_SHA:
        return None, f"changed {sha[:12]}"
    spec = importlib.util.spec_from_file_location("c2_r46", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, "ok"


def existing_named(root: pathlib.Path, text: str, rx) -> set[str]:
    out = set()
    for m in rx.finditer(text):
        p = m.group(0).rstrip(".)")
        if p.startswith("./"):
            p = p[2:]
        if (root / p).is_file():
            out.add(p)
    return out


# A cell boundary is an UNESCAPED pipe: `\|` renders as a literal pipe inside
# a cell, so splitting on it misplaces cells (round-47 `MutC2Forge` b2).
CELL_SPLIT = re.compile(r"(?<!\\)\|")
COMMENT = re.compile(r"<!--.*?-->")
# "names an exit code": `exit 0`, `exit` `1`, or a backticked code `0`/`1`/`2`
# (round-47 `ReviewerC2Set` F2: the substring `exit` let "no exit code
# documented" register a path and dropped `` `0` clean · `1` failed ``).
EXIT_CODE = re.compile(r"\bexit\b\W{0,4}`?\d|`[0-9]{1,3}`")
# A bare script name inside an entry point's source resolves against that
# file's own directory (`ORACLE=$SCRIPT_DIR/round26-registry-oracle.py`).
BARE = re.compile(r"(?<![\w.-])[A-Za-z0-9_][A-Za-z0-9_.-]*\.(?:py|sh)\b")


def gates_table_rows(skill: pathlib.Path) -> list[str]:
    """Every table row of the `## Gates` section, as a reader sees it.

    Stricter than the round-46 reader it replaces here (round-47 `MutC2Forge`):
    both ``` and ~~~ fences are literal, every inline HTML comment on a line is
    stripped (not only the first), and a row needs no `exit` word to be read —
    the `exit` requirement applies to the verdict-map cell when registering,
    while DANGLING reads every row.
    """
    if not skill.is_file():
        return []
    rows, inside, fence, in_comment = [], False, None, False
    for raw in skill.read_text(encoding="utf-8").splitlines():
        s = raw.lstrip()
        if fence is None and (s.startswith("```") or s.startswith("~~~")):
            fence = s[:3]
            continue
        if fence is not None:
            if s.startswith(fence):
                fence = None
            continue
        line = raw
        if in_comment:
            if "-->" not in line:
                continue
            line = line.split("-->", 1)[1]
            in_comment = False
        line = COMMENT.sub("", line)
        if "<!--" in line:
            line, in_comment = line.split("<!--", 1)[0], True
        if line.startswith("## "):
            inside = line.strip() == "## Gates"
            continue
        if inside and raw.startswith("|") and len(CELL_SPLIT.findall(line)) >= 9:
            rows.append(line)
    return rows


def outside_gates(text: str) -> str:
    keep, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Gates"
        if not inside:
            keep.append(line)
    return "\n".join(keep)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    r46, why = load_r46(root)
    if r46 is None:
        print(f"R46_INSTRUMENT={why}")
        print("C2=FAIL")
        return 2
    abc, _na, _nb, _nc = r46.entry_points(root)
    # `./tools/x.py` and `tools/x.py` are one path (round-47 `ReviewerC2Set` F3).
    abc_set = {p[2:] if p.startswith("./") else p for p in abc}
    rx = r46.NAMED

    check_named: set[str] = set()
    q = root / "corpus" / "QUALITY.md"
    if q.is_file():
        check_named |= existing_named(root, q.read_text(encoding="utf-8", errors="replace"), rx)
    sk = root / "SKILL.md"
    if sk.is_file():
        check_named |= existing_named(root, outside_gates(sk.read_text(encoding="utf-8", errors="replace")), rx)

    eps = set(abc_set) | check_named
    frontier = sorted(eps)
    while frontier:
        nxt = []
        for p in frontier:
            f = root / p
            try:
                src = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            deps = existing_named(root, src, rx)
            for m in BARE.finditer(src):
                q = (f.parent / m.group(0)).resolve()
                try:
                    rel = str(q.relative_to(root.resolve()))
                except ValueError:
                    continue
                if q.is_file() and rel != p:
                    deps.add(rel)
            for d in deps:
                if d not in eps:
                    eps.add(d)
                    nxt.append(d)
        frontier = nxt
    dep = eps - abc_set - check_named
    chk = check_named - abc_set

    rows = gates_table_rows(sk)
    entry_cells = []
    for r in rows:
        cells = CELL_SPLIT.split(r.strip().strip("|"))
        if len(cells) >= 8 and EXIT_CODE.search(cells[3]):
            entry_cells.append(cells[2])
    unreg = sorted(p for p in eps if not any(r46.names(c, p) for c in entry_cells))
    dangling = set()
    for r in rows:
        for m in rx.finditer(r):
            p = m.group(0).rstrip(".)")
            if p.startswith("./"):
                p = p[2:]
            if not (root / p).is_file():
                dangling.add(p)
    dangling = sorted(dangling)
    if a.list:
        for p in unreg:
            print("UNREGISTERED_PATH", p)
        for p in dangling:
            print("DANGLING_PATH", p)
    mism = len(unreg) + len(dangling)
    print(f"ENTRY_POINTS={len(eps)} (abc={len(abc_set)} dependence=+{len(dep)} check_named=+{len(chk)})")
    print(f"FLOOR={FLOOR}")
    print(f"GATES_ROWS={len(rows)}")
    print(f"REGISTERED={len(eps) - len(unreg)}/{len(eps)}")
    print(f"UNREGISTERED={len(unreg)}")
    print(f"DANGLING={len(dangling)}")
    print(f"MISMATCHES={mism}")
    ok = mism == 0 and len(eps) >= FLOOR
    print("C2=PASS" if ok else "C2=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
