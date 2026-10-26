# R52ExecPointerAnchor — content anchor for pointer corrections (round-51 routed defect 4)

Seat: R52ExecPointerAnchor (executor). No installs (tooling directive: none performed; no tool added).
Scratch: `/fast/scratch/hyaku/chousa-r52/R52ExecPointerAnchor` (TMPDIR exported for every run; removed at end).
Lane files read only; my only write is this report. No mutating git/jj command was run (the only git call was
c3-count.py's read-only `git show` of its BASE_REV) and no fleet-root file touched.
Nothing here changes a frozen predicate: C1/C2 counters and `claims.md` (37468ead) were not read for enforcement
and not executed.

## 1. The defect and the tightening

QUALITY.md:880 (criterion 83; named limit at :890) binds a dangling self-assessment pointer to "a later
`correction: SCORECARD.md:<row line> <pointer> -> <path>` line … an existing non-empty `<path>`", and names the
limit itself: "existence, not truth". Round-51 spot-check section 6 defect 4 (`corpus/lessons/round-51-verifier-spotcheck.md:103`):
"C3 reads corrections in any order and only for SCORECARD rows; pointers to files that exist but do not show the
behaviour pass. Add a content-anchor check, not just existence."

`corpus/evidence/round51/c3-count.py:100` maps `corr[(line, ptr)] = path` and `:108` accepts it when `real(root/tgt)`
(a non-empty file or a directory holding a file) — no content is read. The successor check below requires a trailing
` anchor: "<text>"` on the governing `correction:` line and tests that text against the target's bytes.

Append-only files cannot gain the anchor by editing the four older lines, so the check resolves **last-wins per key**
`(file, line, pointer)` — the same map shape c3-count.py already uses — and is green only when the newest line naming
each key carries an anchor present in its target.

## 2. The checker (intended lane path `corpus/evidence/round52/pointer-anchor-check.py`, 74 lines)

```python
#!/usr/bin/env python3
"""pointer-anchor-check — round-52 successor read of `correction:` pointer redirects.

Round-51 spot-check defect 4: c3-count.py accepts a `correction:` pointer to ANY
non-empty file, so a redirect to a file that does not show the claimed behaviour
passes (QUALITY 83 "existence, not truth"). This check reads every
`correction: <file>:<line> <ptr> -> <path>[ anchor: "<text>"]` line in
SCORECARD.md and corpus/README.md. Files are append-only, so the LAST line naming a
key (file, line, ptr) governs: that line must carry a trailing ` anchor: "<text>"`
whose text is non-empty and occurs in <path> (a file read as UTF-8, or any file
under a directory). Prints one UNANCHORED line per unsatisfied key, then
`ANCHORED=a/n`; exit 0 all anchored · 1 a<n · 2 no correction line (vacuous).
Named limits: text occurrence, not meaning — an anchor that also sits in an
unrelated line of the target passes; a directory target is searched as a flat text
pool; an anchor text may not contain `"`; `correction:` prose without `-> <path>`
is not a redirect and is not read.
Usage: python3 corpus/evidence/round52/pointer-anchor-check.py [--root LANE]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
FILES = ("SCORECARD.md", "corpus/README.md")
HEAD = re.compile(r"^correction: (\S+):(\d+) (\S+) -> (\S+)(.*)$")
ANC = re.compile(r'^ anchor: "(.*)"\s*$')


def text_of(p: pathlib.Path) -> str:
    """The target's UTF-8 text: the file, or every file under a directory."""
    if p.is_file():
        return p.read_text(encoding="utf-8", errors="replace")
    if p.is_dir():
        return "\n".join(q.read_text(encoding="utf-8", errors="replace")
                         for q in sorted(p.rglob("*")) if q.is_file())
    return ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(LANE))
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    keys: dict[tuple[str, int, str], tuple[str, str | None]] = {}
    for name in FILES:
        f = root / name
        if not f.is_file():
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            m = HEAD.match(line)
            if not m:
                continue
            rest = m.group(5)
            am = ANC.match(rest)
            anchor = am.group(1) if am else None
            keys[(m.group(1), int(m.group(2)), m.group(3))] = (m.group(4), anchor)
    if not keys:
        print("NO_CORRECTION_LINES")
        return 2
    bad = []
    for (fname, ln, ptr), (target, anchor) in sorted(keys.items()):
        if not anchor or not anchor.strip() or anchor not in text_of(root / target):
            bad.append(f'UNANCHORED {fname}:{ln} {ptr} -> {target} anchor={anchor!r}')
    for b in bad:
        print(b)
    print(f"ANCHORED={len(keys) - len(bad)}/{len(keys)}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
```

## 3. Red-before on the lane (observed)

```
$ export TMPDIR=$S; python3 pointer-anchor-check.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin
UNANCHORED SCORECARD.md:1843 measure/final/ -> .ufo/waves/round-32/measure/final/ anchor=None
UNANCHORED SCORECARD.md:2073 measure-l1/c1-s36361.json -> .ufo/waves/round-36/measure-l1/c1-s36361.json anchor=None
UNANCHORED SCORECARD.md:2074 measure-l1/c2-s36371.json -> .ufo/waves/round-36/measure-l1/c2-s36371.json anchor=None
UNANCHORED SCORECARD.md:2616 c1-supplement.py -> corpus/evidence/round50/c1-supplement.py anchor=None
ANCHORED=0/4
rc=1
```

n=4 is the complete redirect population: `grep -c '^correction:' SCORECARD.md` → 4 (lines 2626-2629);
`corpus/README.md` holds two `correction:` lines (1083, 1111) but they are supersede prose with no `-> <path>`
(`grep -n -- '->' corpus/README.md` → lines 25, 732 only, both unrelated), so they are not redirects and are not read.
c3-count.py today also resolves all four (`RESOLVED_BY_CORRECTION=4`, `DANGLING=0`, `C3=PASS`), i.e. the old check is
green on inputs that show nothing.

## 4. The successor lines, and anchor verification

Intended lane file `SCORECARD.md`, appended after line 2629 (append-only; the four older lines stay). Each anchor was
verified with `grep -cF` in the target **before** being written (no anchor holds the checker's `"` delimiter, so no
escaping is needed):

| key | anchor text | `grep -cF` observed | what it binds |
|---|---|---|---|
| SCORECARD.md:1843 `measure/final/` | `APPEND_SERIALIZED=24/24` | `grep -rcF` over the target dir → `battery.out:2`, `c1-s32101.json:1`, `c1-s32102.json:1` | the row's `24/24` |
| SCORECARD.md:2073 `measure-l1/c1-s36361.json` | `ENGINE_SWAP_CANARY=14/14` | 1 | the row's `14/14` |
| SCORECARD.md:2074 `measure-l1/c2-s36371.json` | `WITNESS_PER_RECORD=5/5` | 1 | the row's `5/5` |
| SCORECARD.md:2616 `c1-supplement.py` | `SUPPLEMENT_LEGS={n}/{len(res)}` | 1 | the supplement's tally print (`:78`) |

```
$ grep -cF 'ENGINE_SWAP_CANARY=14/14' .ufo/waves/round-36/measure-l1/c1-s36361.json
1
$ grep -cF 'WITNESS_PER_RECORD=5/5' .ufo/waves/round-36/measure-l1/c2-s36371.json
1
$ grep -rcF 'APPEND_SERIALIZED=24/24' .ufo/waves/round-32/measure/final/ | grep -v ':0$'
.ufo/waves/round-32/measure/final/battery.out:2
.ufo/waves/round-32/measure/final/c1-s32101.json:1
.ufo/waves/round-32/measure/final/c1-s32102.json:1
$ grep -cF 'SUPPLEMENT_LEGS={n}/{len(res)}' corpus/evidence/round50/c1-supplement.py
1
```

```
correction: SCORECARD.md:1843 measure/final/ -> .ufo/waves/round-32/measure/final/ anchor: "APPEND_SERIALIZED=24/24"
correction: SCORECARD.md:2073 measure-l1/c1-s36361.json -> .ufo/waves/round-36/measure-l1/c1-s36361.json anchor: "ENGINE_SWAP_CANARY=14/14"
correction: SCORECARD.md:2074 measure-l1/c2-s36371.json -> .ufo/waves/round-36/measure-l1/c2-s36371.json anchor: "WITNESS_PER_RECORD=5/5"
correction: SCORECARD.md:2616 c1-supplement.py -> corpus/evidence/round50/c1-supplement.py anchor: "SUPPLEMENT_LEGS={n}/{len(res)}"
```

## 5. Green-after on a scratch copy (observed)

`$S/green` = copies of lane `SCORECARD.md`, `corpus/README.md` and the four target paths, with the four lines above
appended to `SCORECARD.md` by `cat >>`.

```
$ grep -c '^correction:' $S/green/SCORECARD.md
8
$ python3 pointer-anchor-check.py --root $S/green
ANCHORED=4/4
rc=0
```

Eight `correction:` lines, n=4: the anchored successor governs each key (last-wins). This is the append-only form;
no older line is edited.

## 6. Falsifiers (observed, each rc=1)

Forged anchor — a successor naming the same key with text absent from the target (target still non-empty, so the old
existence test would pass it):

```
$ echo "forged text hits: $(grep -cF 'AAA_FORGED_TEXT_ABSENT_FROM_TARGET' $S/forge/.ufo/waves/round-36/measure-l1/c1-s36361.json)"
forged text hits: 0
$ echo "target non-empty (the old c3 existence test passes it): $(stat -c '%s bytes' $S/forge/.ufo/waves/round-36/measure-l1/c1-s36361.json)"
target non-empty (the old c3 existence test passes it): 7039 bytes
$ python3 pointer-anchor-check.py --root $S/forge
UNANCHORED SCORECARD.md:2073 measure-l1/c1-s36361.json -> .ufo/waves/round-36/measure-l1/c1-s36361.json anchor='AAA_FORGED_TEXT_ABSENT_FROM_TARGET'
ANCHORED=3/4
rc=1
```

Misredirect to *any* non-empty file (defect 4's literal shape): `c1-supplement.py` pointed at `corpus/README.md`
(151130 bytes, non-empty) with the true anchor text, which README does not hold:

```
$ python3 pointer-anchor-check.py --root $S/misdirect
UNANCHORED SCORECARD.md:2616 c1-supplement.py -> corpus/README.md anchor='SUPPLEMENT_LEGS={n}/{len(res)}'
ANCHORED=3/4
rc=1
```

## 7. Integration notes for the L1

1. Land the checker at `corpus/evidence/round52/pointer-anchor-check.py` (executable, 74 lines) and append the four
   lines of section 4 to `SCORECARD.md` — nothing else. Green on the lane then holds against the real tree.
2. QUALITY criterion 83's named limit ("existence, not truth") is answered only for these four redirects; its
   correction branch sentence still reads "non-empty `<path>`" and should be tightened in the same append.
3. The checker is not a claim counter: it reads no C1/C2 input and never touches `claims.md`.

## 8. Risks and named limits (not blockers)

- Anchor text is bound to current target bytes. Regenerating `battery.out` or the two receipts with a different count
  turns the check red — intended, since the anchor is the count the row claims; the fix is a new successor line, not
  an edit.
- Directory targets are a flat text pool: `APPEND_SERIALIZED=24/24` sits in three files under
  `.ufo/waves/round-32/measure/final/`, so deleting `battery.out` alone would still anchor. A stricter form would
  require `path#member` targets; not built here.
- Text occurrence is not meaning: an anchor that also appears in an unrelated comment of the target passes. All four
  anchors here are output strings of the run the row cites, not comments.
- A `correction:` line with trailing prose after the closing quote is read as unanchored (strict), and a redirect with
  no anchor at all is unanchored (red). A line whose shape does not match `-> <path>` is not counted, so n can shrink
  if a redirect is rewritten as prose; the four older lines and the two README prose lines are accounted for above.

VERDICT — Built and falsified `pointer-anchor-check.py` (content-anchored successor to c3-count.py's existence-only correction read): lane red-before `ANCHORED=0/4` rc 1, scratch green-after `ANCHORED=4/4` rc 0 with four grep-verified anchors, forged anchor and misredirect to a non-empty file both `ANCHORED=3/4` rc 1.
