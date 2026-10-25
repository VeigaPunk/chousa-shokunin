# RevC2TagCount — the tag-count gate is invisible to C2 (confirmed)

seat: L1Chousa46.RevC2TagCount (wave 2, falsify)
target: lane commit `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a`
trees: HEAD bytes extracted with
`git -C …/chousa-shokunin archive d09fc8e… | tar -x -C /tmp/chousa-r46w2-RevC2TagCount`
(authoritative) and the live lane worktree (moving: `SCORECARD.md` is dirty,
+46 uncommitted lines = the round-46 verdict). Installs: none.

## Item, verdict

Item: verify the "invisible gate" — a real committed gate whose removal from the
registry C2 cannot see. **Confirmed at HEAD.** The counter's *binding* step is
sound; its *domain* is the gap. C2 is not falsified as declared (its predicate
quantifies over a defined union), but `REGISTERED=72/72` does not mean "every
gate is registered".

## 1. Does `corpus/evidence/round45/tag-count.py` have a Gates row? Yes

`SKILL.md:111` at HEAD, sole occurrence in SKILL.md (`grep -c tag-count SKILL.md`
→ `1`), 9 pipes, contains `exit`, so it *is* a row under the counter's own rule:

```
| `tag-count` (QUALITY 64, r45) | check | `python3 corpus/evidence/round45/tag-count.py [--scorecard PATH] [--from N] [--to N]` (default rounds ≥ 45) | `TAGGED=k/n`; exit `0` … 
```

row sha256 `8a6e450391d8a490327669d22639a4603a9abc8b7249492f229706b4d12ee794`;
gate file sha256 `99f5e637c948819b02e6ce8107dc9e8660eb1569a6fe9c336f2a84610268f8af`;
pinned control `corpus/evidence/round45/controls/tag-control-r35-r44.txt` present.
It is a real gate: `corpus/QUALITY.md:589` names its full path as the QUALITY 64
check, `SCORECARD.md:2420` (HEAD) calls its row load-bearing.

Yet it is **not an entry point**: `TAGCOUNT_IN_ENTRY_POINTS=False` at HEAD, because
set B's name pattern excludes `tag-count.py`, and set C only reads SCORECARD.md +
`corpus/evidence/round*/claims*.md` for `tools/`- or `corpus/`-prefixed paths —
HEAD SCORECARD has `0` occurrences of the repo-relative form (only bare
`` `tag-count` `` at :2420), no claims file mentions it at all
(`grep -rln tag-count corpus/evidence/*/claims*.md` → NONE), and `corpus/QUALITY.md`
is not scanned.

## 2. Delete the row → C2 still passes (mutation, /tmp copy at HEAD)

Baseline, HEAD copy:
`ENTRY_POINTS=72 (tools=8 counters=50 named=70) GATES_ROWS=35 REGISTERED=72/72 UNREGISTERED=0 C2=PASS` exit 0

After `sed -i '111d' SKILL.md` (row gone; `grep -c tag-count SKILL.md` → `0`):
```
ENTRY_POINTS=72 (tools=8 counters=50 named=70)
GATES_ROWS=34
REGISTERED=72/72
UNREGISTERED=0
C2=PASS
EXIT=0
```
A documented, executable gate now has **no registry row at all** and C2 reports a
clean registry. Same result for a sibling: removing every
`corpus/evidence/round46/build-spans.py` token from its Gates row (one occurrence)
also left `UNREGISTERED=0` at HEAD.

Two-cell isolation — the blindness is the domain, not the detector. In the same
copy, append `corpus/evidence/round45/tag-count.py` to `corpus/evidence/round46/claims.md`
(set C now collects it):
```
row PRESENT : ENTRY_POINTS=73 … REGISTERED=73/73 UNREGISTERED=0 C2=PASS exit 0
row DELETED : UNREGISTERED_PATH corpus/evidence/round45/tag-count.py
              ENTRY_POINTS=73 … REGISTERED=72/73 UNREGISTERED=1 C2=FAIL exit 1
```
And a worktree copy where `build-spans.py` is in-domain (the uncommitted
round-46 SCORECARD names it repo-relatively): baseline `73/73 PASS`; after
removing its Gates mention `REGISTERED=72/73 UNREGISTERED=1 C2=FAIL` exit 1.
So: in-domain path → row deletion is caught; out-of-domain path → silent.

Invisible-at-HEAD set (existing files documented in `SKILL.md`, outside A∪B∪C):
`corpus/evidence/round45/tag-count.py` (proper Gates row, real gate);
`corpus/evidence/round46/build-spans.py` (proper Gates row, not named in HEAD
SCORECARD/claims); `corpus/evidence/round25-meta-oracle.py` (a Gates *table* line,
`SKILL.md:85`, that lacks the word `exit`, so `gates_rows()` discards the whole row).

The lane advanced mid-seat to `3807537` (wave-2 corrections; round-46 verdict
committed). Re-check on those bytes: `ENTRY_POINTS=73 (tools=8 counters=50
named=71) GATES_ROWS=35 REGISTERED=73/73 UNREGISTERED=0 C2=PASS`, tag-count still
`TAGCOUNT_IN_SET=False`; deleting `SKILL.md:111` gives `GATES_ROWS=34 …
REGISTERED=73/73 UNREGISTERED=0 C2=PASS` exit 0 — same blindness on current bytes.
The domain is mutable by verdict prose: `build-spans.py` entered set C only
because the round-46 SCORECARD now names it repo-relatively, with no gate-row
change. Conversely the recorded round-47 fix writes `` `round45/tag-count.py` ``
without the `corpus/evidence/` prefix (`SCORECARD.md:2489`), a form `NAMED` would
not collect; it must be written repo-relative to take effect.

## 3. `python3 corpus/evidence/round45/tag-count.py` (default range)

At `d09fc8e`: `TAGGED=3/3` / `TAG=PASS` / exit 0 (round 45's three claim rows; the
round-46 verdict section is not in that commit). At `3807537`, where the verdict is
committed: `TAGGED=6/6` / `TAG=PASS` / exit 0. (Earlier in this wave the live
worktree returned `3/3` before that section was written — the number tracks tree
state, not a frozen value.) Self-test reproduced exactly on both trees:
`--from 35 --to 44` →
`TAGGED=0/22` / `TAG=FAIL` / exit 1, byte-identical to the pinned control file
(`corpus/evidence/round45/controls/tag-control-r35-r44.txt`, modulo the harness
`exit=1` trailer the counter does not print). Domain probe: no claim row in rounds
≥45 that the row rule (`^ {0,3}\| C\d`) should match is missed.

## Consequence for C2's claim

C2 can print `UNREGISTERED=0 C2=PASS` while a documented executable gate
(`corpus/evidence/round45/tag-count.py`, the QUALITY 64 check, with a full Gates
row and a pinned control) carries no Gates row at all, because set C is the set of
paths *mentioned repo-relatively* in SCORECARD/claims rather than the set of gates
the registry documents — so `REGISTERED=72/72` certifies membership of a
mention-derived set, not gate-registry coverage.

## Residual risk / gaps

- Overlaps wave 1's already-reported mention-based framing (`CritC2Framing`); the
  new material is the demonstrated single-row deletion with zero signal, the
  three-path invisible set at HEAD, and the `round25-meta-oracle.py` case where a
  Gates-section line lacking `exit` is not a "Gates row" for any purpose.
- Not measured: whether every *other* lane gate documented only in
  `QUALITY.md`/`LOG.md`/`corpus/lessons/` is also outside the domain (spot check
  found no additional unique existing path in QUALITY.md beyond those above).
- All mutations confined to `/tmp/chousa-r46w2-RevC2TagCount`; lane bytes untouched
  (only this report written). Scratch deleted below.
