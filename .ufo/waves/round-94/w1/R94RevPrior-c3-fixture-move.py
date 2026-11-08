#!/usr/bin/env python3
"""Seat-R94RevPrior C3 before-state fixture: move the `215` tail tally into the Round 36 section.

Usage: python3 fixture-c3-move.py TREE move|restore
`move` deletes the exact 215-tally line from the Round27 subsection and re-inserts it (same bytes) under
the Round 36 heading; `restore` is done by `git -C TREE checkout -- SKILL.md` instead (this script only
asserts the reverse move would be identical).
"""
import sys

SKILL = "SKILL.md"
OWNER215 = "### Round27 repair/status correction — 2026-10-21"
ALIEN = "### Round 36 — the engine-swap canary and per-record attribution (2026-10-23)"
TAIL215_LINE = "`PASS (215 cases, 0 skipped)` under the host UTF-8 locale; original187"
SUFFIX = "Moved for the fixture."


def main():
    tree, mode = sys.argv[1], sys.argv[2]
    path = tree + "/" + SKILL
    text = open(path, encoding="utf-8").read()
    assert mode == "move", "restore is git checkout"
    lines = text.split("\n")
    frm_i = lines.index(OWNER215)
    idx = None
    for i in range(frm_i + 1, len(lines)):
        if lines[i].startswith("#"):
            break
        if lines[i] == TAIL215_LINE:
            idx = i
            break
    assert idx is not None, "215 tally not under its declared owner"
    del lines[idx]
    to_i = lines.index(ALIEN)
    lines[to_i + 1:to_i + 1] = ["", SUFFIX + " " + TAIL215_LINE]
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    print(f"FIXTURE mode=move from={OWNER215!r} to={ALIEN!r}")


if __name__ == "__main__":
    main()
