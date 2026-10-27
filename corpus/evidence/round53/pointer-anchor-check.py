#!/usr/bin/env python3
"""pointer-anchor-check — round-53 content-anchored read of `correction:` redirects.

Round-51 spot-check defect 4, still open after round 52 (lesson round-52 §6.4):
`corpus/evidence/round51/c3-count.py:100-110` maps `correction: SCORECARD.md:<line>
<ptr> -> <path>` and accepts the redirect when `real(root/path)` — existence, not
truth — so a pointer to ANY non-empty file passes. This check reads every redirect
line in SCORECARD.md and corpus/README.md and requires a trailing
` anchor: "<text>"` whose text is >= 12 characters and occurs EXACTLY ONCE in the
target's UTF-8 text (a file, or the newline-joined pool of a directory's files).
Files are append-only, so the LAST line naming a key (file, line, ptr) governs.
The anchor is read with a GREEDY trailing quote, so its text may itself contain
`"` (written `anchor: "seed": 32101,"`, anchor text `seed": 32101,`).
Prints one line per unsatisfied key, then `ANCHORED=a/n UNANCHORED=u BAD=b`, where
BAD counts unsatisfied keys that DID supply an anchor failing the length or
exactly-once test (a wrong anchor, as against none).
Exit 0 all anchored · 1 a<n (a `correction:` line carrying an ASCII `->` that does
not parse is a pseudo-key, always unanchored) · 2 no redirect at all (nothing
measured is not a pass). A `correction:` line with no ASCII `->` is prose: unread.
Named limits: occurrence, not meaning — an anchor that also sits in an unrelated
line of the target passes; a directory target is a flat text pool; >= 12
characters is no proof the target SHOWS the behaviour, only that it carries it.
Usage: python3 corpus/evidence/round53/pointer-anchor-check.py [--root LANE]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
FILES = ("SCORECARD.md", "corpus/README.md")
HEAD = re.compile(r"^correction: (\S+):(\d+) (\S+) -> (\S+)(.*)$")
ANCHOR = re.compile(r'^ anchor: "(.*)"\s*$')
MIN = 12


def text_of(p: pathlib.Path) -> str:
    if p.is_file():
        return p.read_text(encoding="utf-8", errors="replace")
    if p.is_dir():
        return "\n".join(q.read_text(encoding="utf-8", errors="replace")
                         for q in sorted(p.rglob("*")) if q.is_file())
    return ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    root = pathlib.Path(ap.parse_args().root)
    keys: dict[tuple[str, int, str], tuple[str, str | None]] = {}
    for name in FILES:
        f = root / name
        if not f.is_file():
            continue
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if not line.startswith("correction:") or "->" not in line:
                continue
            m = HEAD.match(line)
            if not m:
                keys[(name, i, f"<malformed:{i}>")] = ("", None)
                continue
            am = ANCHOR.match(m.group(5))
            keys[(m.group(1), int(m.group(2)), m.group(3))] = (
                m.group(4), am.group(1) if am else None)
    if not keys:
        print("ANCHORED=0/0 UNANCHORED=0 BAD=0")
        return 2
    text: dict[str, str] = {}
    n = a = b = 0
    for (fname, ln, ptr), (target, anchor) in sorted(keys.items()):
        n += 1
        if target not in text:
            text[target] = text_of(root / target) if target else ""
        hits = text[target].count(anchor) if anchor else 0
        if anchor is not None and len(anchor) >= MIN and hits == 1:
            a += 1
        elif anchor is None:
            print(f"UNANCHORED {fname}:{ln} {ptr} -> {target} anchor=None")
        else:
            b += 1
            print(f"BAD_ANCHOR {fname}:{ln} {ptr} -> {target} "
                  f"anchor={anchor!r} len={len(anchor)} occurrences={hits}")
    print(f"ANCHORED={a}/{n} UNANCHORED={n - a} BAD={b}")
    return 0 if a == n else 1


if __name__ == "__main__":
    sys.exit(main())
