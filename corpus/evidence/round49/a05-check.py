#!/usr/bin/env python3
"""a05-check — round-49 fix for the mined mistake "a held-out label accepted on
charity and propagated as a measured figure" (round-48 closure ruling (a)).

Every line of a lane lesson (corpus/lessons/*.md) that carries the figure
`3/12` together with `a05` is a propagation of the ruled-false label, unless the same line already
states the true figure as `2/12 (p03, p04)` (the closure's own ruling lines). Lessons
are append-only and the verifier spot-checks are not lane-owned, so the
correction lives elsewhere: each propagation `<file>:<line>` must be named,
with the true figure `2/12`, on one line of `corpus/lessons/round-49.md`'s
`## Mistakes` or `## Spot-check intake` section. The round-49 lesson itself is
not scanned for propagations.

Exit 0 every propagation corrected · 1 an uncorrected propagation · 2 usage.
"""
from __future__ import annotations

import pathlib
import re
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
PROP = re.compile(r"(?i)3/12[^\n]*a05|a05[^\n]*3/12")
TRUE = re.compile(r"2/12 \(p03, p04\)")


def main() -> int:
    lessons = LANE / "corpus" / "lessons"
    fix = lessons / "round-49.md"
    if not lessons.is_dir():
        return 2
    corr: list[str] = []
    if fix.is_file():
        keep = False
        for line in fix.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                keep = line.strip() in ("## Mistakes", "## Spot-check intake")
                continue
            if keep and "2/12" in line:
                corr.append(line)
    bad = ok = 0
    for p in sorted(lessons.glob("*.md")):
        if p.name == "round-49.md":
            continue
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if PROP.search(line) and not TRUE.search(line):
                ref = f"{p.name}:{n}"
                if any(re.search(re.escape(ref) + r"(?!\d)", c) for c in corr):
                    ok += 1
                    print(f"CORRECTED {ref}")
                else:
                    bad += 1
                    print(f"UNCORRECTED {ref}")
    print(f"A05_PROPAGATIONS={ok + bad} CORRECTED={ok}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
