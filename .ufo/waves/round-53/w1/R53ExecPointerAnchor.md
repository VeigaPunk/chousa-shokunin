# R53ExecPointerAnchor — content-anchored `correction:` redirects (round-51 routed defect 4, landed in round 53)

Seat: R53ExecPointerAnchor (executor, leaf). No install performed or needed (no pacman — the host-wide guard holds it
paused — no uv/npx/binary). Scratch `/fast/scratch/hyaku/chousa-r53/R53ExecPointerAnchor` (TMPDIR exported for every
run; removed at the end). No git/jj command ran, so no fixture repo was needed; lane files read only, this report is
my only write. `claims.md` (frozen, `a6ff732c`) was read for scope only — C1/C2 predicates, counters, controls and
`tools/assimilate-rows.py` were not touched, run or re-proposed.

## 1. The defect, restated from the lane, and what a successor must add

- Routed: `corpus/lessons/round-51-verifier-spotcheck.md:103` — "C3 reads corrections in any order and only for
  SCORECARD rows; pointers to files that exist but do not show the behaviour pass. Add a content-anchor check, not
  just existence." Still open after round 52: `corpus/lessons/round-52-verifier-spotcheck.md:95` (§6 item 4).
- Code: `corpus/evidence/round51/c3-count.py:100-108` builds `corr[(line, ptr)] = path` from `correction:` lines and
  accepts it iff `real(root/tgt)` — a non-empty file, or a directory holding one; no content is read.
- Population measured: `grep -c '^correction:' SCORECARD.md` → `4` (lines 2626-2629); `grep -c '^correction:'
  corpus/README.md` → `2` (lines 1083, 1111), both supersede prose with no ASCII `->` (`grep -n -- '->'
  corpus/README.md` → lines 25, 732 only, unrelated), so the redirect population is n=4.
- Successor rule: same key `(file, line, ptr)`, last-wins (append-only, no older line edited), governing line must
  carry ` anchor: "<text>"` of ≥12 characters occurring EXACTLY ONCE in the target's UTF-8 text.

## 2. The checker — intended lane path `corpus/evidence/round53/pointer-anchor-check.py` (90 lines)

```python
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
```

## 3. Red-before on the lane (observed)

```
$ export TMPDIR=/fast/scratch/hyaku/chousa-r53/R53ExecPointerAnchor
$ python3 pointer-anchor-check.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin
UNANCHORED SCORECARD.md:1843 measure/final/ -> .ufo/waves/round-32/measure/final/ anchor=None
UNANCHORED SCORECARD.md:2073 measure-l1/c1-s36361.json -> .ufo/waves/round-36/measure-l1/c1-s36361.json anchor=None
UNANCHORED SCORECARD.md:2074 measure-l1/c2-s36371.json -> .ufo/waves/round-36/measure-l1/c2-s36371.json anchor=None
UNANCHORED SCORECARD.md:2616 c1-supplement.py -> corpus/evidence/round50/c1-supplement.py anchor=None
ANCHORED=0/4 UNANCHORED=4 BAD=0
rc=1
```

n=4 with `corpus/README.md` present (two `correction:` lines) proves prose lines are not counted; c3-count.py is
green on this input by existence alone.

## 4. Successor lines, each anchor verified by `grep -c` before writing

Intended lane file `SCORECARD.md`, appended after line 2690 (the round-53 planned section); the four incumbents at
2626-2629 stay. Keys and targets are byte-identical to the incumbents, so c3's `(line, ptr) -> path` map is unchanged.

```
correction: SCORECARD.md:1843 measure/final/ -> .ufo/waves/round-32/measure/final/ anchor: "seed": 32101,"
correction: SCORECARD.md:2073 measure-l1/c1-s36361.json -> .ufo/waves/round-36/measure-l1/c1-s36361.json anchor: "ENGINE_SWAP_CANARY=14/14"
correction: SCORECARD.md:2074 measure-l1/c2-s36371.json -> .ufo/waves/round-36/measure-l1/c2-s36371.json anchor: "WITNESS_PER_RECORD=5/5"
correction: SCORECARD.md:2616 c1-supplement.py -> corpus/evidence/round50/c1-supplement.py anchor: "SUPPLEMENT_LEGS={n}/{len(res)}"
```

```
$ grep -cF 'seed": 32101,' green/.ufo/waves/round-32/measure/final/*        # 8 zeros, c1-s32101.json:1
$ grep -cF 'ENGINE_SWAP_CANARY=14/14' green/.ufo/waves/round-36/measure-l1/c1-s36361.json      # 1
$ grep -cF 'WITNESS_PER_RECORD=5/5' green/.ufo/waves/round-36/measure-l1/c2-s36371.json        # 1
$ grep -cF 'SUPPLEMENT_LEGS={n}/{len(res)}' green/corpus/evidence/round50/c1-supplement.py     # 1
$ parse of both files  # incumbent redirects: 4, new: 4, target_same=True for all four keys
```

## 5. Green-after on a scratch copy (observed)

`$S/green` = lane copies of both files and the four targets, plus the four lines above appended by `printf >>`.

```
$ python3 pointer-anchor-check.py --root $S/green
ANCHORED=4/4 UNANCHORED=0 BAD=0
rc=0
```

## 6. Falsifiers (all observed, all rc=1)

Each `$S/<case>` is a full copy of the green root plus one later line for a key (last-wins supersede):

```
# round-52's candidate set: its directory anchor is not unique (4 hits over 3 files)
BAD_ANCHOR SCORECARD.md:1843 measure/final/ -> .ufo/waves/round-32/measure/final/ anchor='APPEND_SERIALIZED=24/24' len=23 occurrences=4
ANCHORED=3/4 UNANCHORED=1 BAD=1
# forged anchor, absent text; target 7039 bytes and grep -cF → 0, so c3's existence test passes it
BAD_ANCHOR SCORECARD.md:2073 measure-l1/c1-s36361.json -> .ufo/waves/round-36/measure-l1/c1-s36361.json anchor='AAA_FORGED_TEXT_ABSENT_FROM_TARGET' len=34 occurrences=0
ANCHORED=3/4 UNANCHORED=1 BAD=1
# too-short anchor: grep -cF '14/14' → 1 (occurrence-only would admit it), 5 characters
BAD_ANCHOR SCORECARD.md:2073 measure-l1/c1-s36361.json -> .ufo/waves/round-36/measure-l1/c1-s36361.json anchor='14/14' len=5 occurrences=1
ANCHORED=3/4 UNANCHORED=1 BAD=1
# misdirect to a non-empty file that does not show the behaviour (defect 4's literal shape; README 155482 bytes)
BAD_ANCHOR SCORECARD.md:2616 c1-supplement.py -> corpus/README.md anchor='SUPPLEMENT_LEGS={n}/{len(res)}' len=30 occurrences=0
ANCHORED=3/4 UNANCHORED=1 BAD=1
# vacuous root (empty SCORECARD.md): refusing a green that read nothing
ANCHORED=0/0 UNANCHORED=0 BAD=0   → rc=2
# garbled redirect (arrow, then nothing): a pseudo-key cannot silently leave n
UNANCHORED SCORECARD.md:1 <malformed:1> ->  anchor=None
ANCHORED=1/2 UNANCHORED=1 BAD=0   → rc=1
```

## 7. Findings for the L1 (the append is the L1's, not mine)

1. **The directory key cannot carry its own count anchor under exactly-once.** Row 1843 claims 24/24 appends, and
   `APPEND_SERIALIZED=24/24` occurs 4 times across 3 of the 9 members of
   `.ufo/waves/round-32/measure/final/` (twice in `battery.out`, once in each `c1-s3210{1,2}.json` label line).
   Every quote-free single-line string that is unique in that pool is a gate or binding tally (`RESOLVED_HOPS=17/22`,
   `VERDICT_BEARING_EXPORTS=3/3`, three `RESEARCH_GATE:` lines) — none the append count. My successor therefore
   anchors the *receipt instance* (`seed": 32101,`, unique to `c1-s32101.json`, the file whose
   `"label": "APPEND_SERIALIZED=24/24"` line carries the count) rather than pretend the count is unique. Anchoring
   the count itself requires naming the member file, which narrows what the row's `measure/final/` pointer resolves
   to — a semantics change the L1 owns; I did not make it.
2. **Anchor syntax has one quote exception.** ` anchor: "seed": 32101,"` parses (greedy trailing quote) to
   `seed": 32101,`; a non-greedy reader would take `seed`. Documented in the docstring; prose after the closing quote
   reads as unanchored, and an anchor may not end in whitespace.
3. **Rate the earlier build down, not just land it.** Round-52's four lines pass an occurrence test but score 3/4
   here: its `grep -c` table never applied the exactly-once rule to the directory target.
4. **Append point.** `SCORECARD.md` ends at line 2690; append the four lines of §4 after it and nothing else.
   `corpus/README.md`'s two prose lines need no anchor.

## 8. Risks and named limits (not blockers)

- Occurrence is not meaning: an anchor that also sits in an unrelated target line passes, and ≥12 characters does
  not prove the target *shows* the behaviour — existence-only acceptance closes, not entailment (round-52's limit).
- A directory target is a flat newline-joined pool, so two receipts legitimately printing one count are
  unanchorable there (finding 1).
- Anchors bind current bytes: regenerating a receipt turns the key red; the fix is a new successor line, not an edit.
- Only `SCORECARD.md` and `corpus/README.md` are read; `SHONEN.md` pointers still resolve by existence, out of scope.
- `rc=2` on a root with no redirect goes beyond "exit 1 when a<n"; it refuses a vacuous green, never masks a red.

VERDICT — Built and falsified `corpus/evidence/round53/pointer-anchor-check.py` (90 lines, content-anchored successor
to c3-count.py's existence-only read): lane red-before `ANCHORED=0/4` rc 1, scratch green-after `ANCHORED=4/4` rc 0
with four `grep -c`-verified anchors, and four red probes — round-52's own set 3/4 (`occurrences=4`), forged anchor
3/4 (`occurrences=0`, target non-empty), too-short anchor 3/4 (`len=5`), misdirect to a non-empty README 3/4
(`occurrences=0`) — plus vacuous rc 2 and garbled-line rc 1.
