#!/usr/bin/env python3
"""c2-count — frozen counter for round 46 claim C2 (calibration).

Predicate R46-C2, the same sentence as corpus/evidence/round46/claims.md:
every committed gate entry point of the lane is named by its repo-relative
path inside a Gates row of SKILL.md, where an entry point is

  A. every file directly under `tools/`; or
  B. every file under `corpus/evidence/round*/` named `c<N>-count*.py`,
     `verify-receipts.py` or `errata-count.py` (the round-45 set, unchanged);
  or
  C. every EXISTING repo-relative `*.py` or `*.sh` path that SCORECARD.md or a
     `corpus/evidence/round*/claims*.md` names as a counting command — the
     executable verifiers outside the frozen name pattern (round-45 closure
     D8, wave-2 `CritC2Framing`; e.g. `corpus/evidence/round34/self-audit.py`).

A Gates row is a line of the `## Gates` section (up to the next `## ` heading)
that starts with `|`, carries at least 8 `|` separators and contains the word
`exit`.

Prints `ENTRY_POINTS=n (tools=nA counters=nB named=nC) GATES_ROWS=k
REGISTERED=n/n UNREGISTERED=k C2=PASS|FAIL`. Exit 0 iff UNREGISTERED=0;
1 otherwise; 2 usage/env (no entry points).

Cheapest gate that would score full marks without the work (QUALITY 60):
pasting the bare paths anywhere in SKILL.md, or into a one-cell row — both are
refused, because the path must sit inside a Gates row and a row needs eight
separators and an exit-code verdict. A plausible row whose verdict map is
wrong still passes; that is a reader's check, named, not hidden.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
COUNTER = re.compile(r"^(c\d+-count[\w.-]*\.py|verify-receipts\.py|errata-count\.py)$")
NAMED = re.compile(r"(?:tools|corpus)/[A-Za-z0-9_./-]+\.(?:py|sh)")


def entry_points(root: pathlib.Path) -> tuple[list[str], int, int, int]:
    a: list[str] = []
    tools = root / "tools"
    if tools.is_dir():
        a = [f"tools/{p.name}" for p in tools.iterdir() if p.is_file()]
    b: list[str] = []
    ev = root / "corpus" / "evidence"
    if ev.is_dir():
        for d in ev.glob("round*"):
            if d.is_dir():
                b += [f"corpus/evidence/{d.name}/{p.name}" for p in d.iterdir()
                      if p.is_file() and COUNTER.match(p.name)]
    sofas: list[pathlib.Path] = []
    sc = root / "SCORECARD.md"
    if sc.is_file():
        sofas.append(sc)
    sofas += sorted(ev.glob("round*/claims*.md")) if ev.is_dir() else []
    seen: set[str] = set()
    for f in sofas:
        for m in NAMED.finditer(f.read_text(encoding="utf-8", errors="replace")):
            p = m.group(0).rstrip(".)")
            if (root / p).is_file():
                seen.add(p)
    c = sorted(seen)
    union = sorted(set(a) | set(b) | set(c))
    return union, len(a), len(b), len(c)


def gates_rows(skill: pathlib.Path) -> list[str]:
    """Rows of the `## Gates` section, fence-aware (round-46 `MutC2Forge`).

    A fenced line is literal Markdown source, not a rendered row, so it never
    registers a path; an HTML comment is stripped before the row test. Both
    were latent cheap gates under the first implementation, which read the
    frozen sentence's "a line that starts with |" literally.
    """
    if not skill.is_file():
        return []
    rows, inside, fence = [], False, False
    text = re.sub(r"<!--.*?-->", "", skill.read_text(encoding="utf-8"), flags=re.S)
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        if line.startswith("## "):
            inside = line.strip() == "## Gates"
            continue
        # The row test runs on the RAW line first: a comment prefix can never
        # manufacture a row (`MutC2More` N1), while an inline comment inside a
        # real row is stripped before the cell test.
        if inside and line.startswith("|"):
            bare = re.sub(r"<!--.*?-->", "", line)
            # Nine separators = the table's eight cells. Eight separators (a
            # seven-cell line) let a single row hold every path in one cell and
            # score UNREGISTERED=0 (`RevInherited`).
            if bare.count("|") >= 9 and "exit" in bare:
                rows.append(bare)
    return rows


def names(row: str, path: str) -> bool:
    """Path membership at a delimiter boundary, never as a suffix of another name."""
    return re.search(r"(?<![A-Za-z0-9_./-])(?:\./)?" + re.escape(path) + r"(?![A-Za-z0-9_./-])",
                     row) is not None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--skill", default=None)
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    skill = pathlib.Path(a.skill) if a.skill else root / "SKILL.md"
    eps, na, nb, nc = entry_points(root)
    if not eps:
        print("C2=FAIL no-entry-points")
        return 2
    rows = gates_rows(skill)
    unreg = [p for p in eps if not any(names(r, p) for r in rows)]
    if a.list:
        for p in unreg:
            print("UNREGISTERED_PATH", p)
    print(f"ENTRY_POINTS={len(eps)} (tools={na} counters={nb} named={nc})")
    print(f"GATES_ROWS={len(rows)}")
    print(f"REGISTERED={len(eps) - len(unreg)}/{len(eps)}")
    print(f"UNREGISTERED={len(unreg)}")
    ok = not unreg
    print("C2=PASS" if ok else "C2=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
