#!/usr/bin/env python3
"""c2-count — frozen counter for round 45 claim C2 (calibration).

Predicate R45-C2, the same sentence as corpus/evidence/round45/claims.md:
every committed gate entry point of the lane — each file directly under
tools/, and each corpus/evidence/round*/ file named c<N>-count*.py,
verify-receipts.py or errata-count.py — is named by its repo-relative path
inside a Gates row of SKILL.md, a Gates row being a line of the `## Gates`
section (up to the next `## ` heading) that starts with `|`, carries at
least 8 `|` separators and contains the word `exit`.

Cheapest gate that would score full marks without the work (QUALITY 60):
pasting the bare paths anywhere in SKILL.md, or into a one-cell row. Both
are refused: the path must sit inside a Gates row, and a row needs eight
separators and an exit-code verdict. A plausible-looking row whose verdict
map is wrong still passes; that is a reader's check, named, not hidden.

Exit codes: 0 UNREGISTERED=0 · 1 any entry point unregistered · 2 usage/env.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
COUNTER = re.compile(r"^(c\d+-count[\w.-]*\.py|verify-receipts\.py|errata-count\.py)$")


def entry_points(root: pathlib.Path) -> list[str]:
    out = []
    tools = root / "tools"
    if tools.is_dir():
        out += [f"tools/{p.name}" for p in tools.iterdir() if p.is_file()]
    ev = root / "corpus" / "evidence"
    if ev.is_dir():
        for d in ev.glob("round*"):
            if d.is_dir():
                out += [f"corpus/evidence/{d.name}/{p.name}" for p in d.iterdir()
                        if p.is_file() and COUNTER.match(p.name)]
    return sorted(out)


def gates_rows(skill: pathlib.Path) -> list[str]:
    if not skill.is_file():
        return []
    rows, inside = [], False
    for line in skill.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Gates"
            continue
        if inside and line.startswith("|") and line.count("|") >= 8 and "exit" in line:
            rows.append(line)
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE), help="lane tree to measure")
    ap.add_argument("--skill", default=None, help="SKILL.md to read (default <root>/SKILL.md)")
    ap.add_argument("--list", action="store_true", help="print each unregistered path")
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    skill = pathlib.Path(a.skill) if a.skill else root / "SKILL.md"
    eps = entry_points(root)
    if not eps:
        print("C2=FAIL no-entry-points")
        return 2
    rows = gates_rows(skill)
    unreg = [p for p in eps if not any(p in r for r in rows)]
    if a.list:
        for p in unreg:
            print("UNREGISTERED_PATH", p)
    print(f"ENTRY_POINTS={len(eps)}")
    print(f"GATES_ROWS={len(rows)}")
    print(f"REGISTERED={len(eps) - len(unreg)}/{len(eps)}")
    print(f"UNREGISTERED={len(unreg)}")
    ok = not unreg
    print("C2=PASS" if ok else "C2=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
