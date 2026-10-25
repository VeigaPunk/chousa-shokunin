#!/usr/bin/env python3
"""c3-count — frozen counter for round 51 claim C3 (calibration).

Predicate R51-C3, the same sentence as corpus/evidence/round51/claims.md: every
repo-path pointer a self-assessment names resolves at the tip. The
self-assessment is (a) the evidence-pointer cell (third cell) of every data row
of every table under a `## Capabilities` heading of `SCORECARD.md` and (b) every
indented evidence line of `SHONEN.md`; a pointer is every whitespace- or
`;`-separated token of a backtick span in those places that, after stripping a
leading or trailing `,;:()`, a trailing `.` (never a leading one: `.ufo/...` is a
path) and a trailing `:N` or `:N-M` line suffix, contains
a `/` or ends in `.py .sh .md .json .jsonl .txt .tsv .log`, does not start with
`-` or `http`, and holds none of `<>*=$|{}[]` or `...`. A pointer RESOLVES when
`<lane>/<pointer>` exists and is a non-empty file or a directory holding a file, or when a later line of `SCORECARD.md` reads
`correction: SCORECARD.md:<row line> <pointer> -> <path>` naming that row's line
number and that exact pointer, and `<lane>/<path>` is likewise non-empty. The count: at the tip
`DANGLING=0`, and neither the capability-row count nor the pointer count is
below its value at BASE_REV (a row or a pointer deleted is not a repair).

Output: `CAP_ROWS=n (base b)`, `POINTERS=n (base b)`, `RESOLVED_BY_CORRECTION=n`,
one `DANGLING <file>:<line> <pointer>` per unresolved pointer, `DANGLING=n`,
`C3=PASS|FAIL`. Exit 0 pass · 1 fail · 2 env (BASE_REV unreadable).
Usage: python3 corpus/evidence/round51/c3-count.py [--root LANE]
Named limits: existence, not truth — a pointer to a file that exists but does not
show the claimed behaviour passes; pointers outside backtick spans are not read;
cells of the Axes table are not read.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
BASE_REV = "9ec1751a24231e899ceea4688e21c8edf6046d35"
EXT = (".py", ".sh", ".md", ".json", ".jsonl", ".txt", ".tsv", ".log")
BAD = set("<>*=$|{}[]")
SUFFIX = re.compile(r":\d+(?:-\d+)?$")
CORR = re.compile(r"^correction: SCORECARD\.md:(\d+) (\S+) -> (\S+)")


def real(p: pathlib.Path) -> bool:
    """A non-empty file, or a directory holding at least one file."""
    if p.is_file():
        return p.stat().st_size > 0
    return p.is_dir() and any(q.is_file() for q in p.rglob("*"))


def pointers(cell: str) -> list[str]:
    out = []
    for span in re.findall(r"`([^`]+)`", cell):
        for tok in re.split(r"[\s;]+", span):
            tok = SUFFIX.sub("", tok.strip(",;:()").rstrip("."))
            if (not tok or tok.startswith(("-", "http")) or "..." in tok or any(c in BAD for c in tok)
                    or not ("/" in tok or tok.endswith(EXT))):
                continue
            out.append(tok)
    return out


def scorecard_rows(text: str) -> list[tuple[int, list[str]]]:
    rows, inside = [], False
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            inside = line.startswith("## Capabilities")
            continue
        if inside and line.startswith("|") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 3 and cells[0] != "Capability":
                rows.append((i, pointers(cells[2])))
    return rows


def shonen_lines(text: str) -> list[tuple[int, list[str]]]:
    return [(i, pointers(l)) for i, l in enumerate(text.splitlines(), 1) if l.startswith("  ") and l.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    base = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE_REV}:SCORECARD.md"], capture_output=True, text=True)
    base_sh = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE_REV}:SHONEN.md"], capture_output=True, text=True)
    if base.returncode != 0 or base_sh.returncode != 0:
        print("NO_BASE")
        return 2
    sc = (root / "SCORECARD.md").read_text(encoding="utf-8")
    sh = (root / "SHONEN.md").read_text(encoding="utf-8")
    rows, shl = scorecard_rows(sc), shonen_lines(sh)
    brows, bshl = scorecard_rows(base.stdout), shonen_lines(base_sh.stdout)
    n_ptr = sum(len(p) for _l, p in rows) + sum(len(p) for _l, p in shl)
    b_ptr = sum(len(p) for _l, p in brows) + sum(len(p) for _l, p in bshl)
    corr: dict[tuple[int, str], str] = {}
    for line in sc.splitlines():
        m = CORR.match(line)
        if m:
            corr[(int(m.group(1)), m.group(2))] = m.group(3)
    dangling, by_corr = [], 0
    for fname, items in (("SCORECARD.md", rows), ("SHONEN.md", shl)):
        for ln, ptrs in items:
            for p in ptrs:
                if real(root / p):
                    continue
                tgt = corr.get((ln, p)) if fname == "SCORECARD.md" else None
                if tgt and real(root / tgt):
                    by_corr += 1
                else:
                    dangling.append(f"{fname}:{ln} {p}")
    print(f"CAP_ROWS={len(rows)} (base {len(brows)})")
    print(f"POINTERS={n_ptr} (base {b_ptr})")
    print(f"RESOLVED_BY_CORRECTION={by_corr}")
    for d in dangling:
        print(f"DANGLING {d}")
    print(f"DANGLING={len(dangling)}")
    ok = not dangling and len(rows) >= len(brows) and n_ptr >= b_ptr
    print("C3=PASS" if ok else "C3=FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
