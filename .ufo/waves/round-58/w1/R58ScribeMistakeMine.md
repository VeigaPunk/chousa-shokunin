# R58ScribeMistakeMine — one mined mistake (chousa round 58, seat leaf)

Base: lane HEAD `9e73a031ab1ac3bac343de008850d7d87f9e5634` (freeze commit). Frozen bytes re-hashed, not
trusted from prose: `sha256sum corpus/evidence/round58/c1-count.py` =
`65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`, and
`git show 9e73a03:corpus/evidence/round58/c1-count.py | sha256sum` = the same digest (no tracked file
modified; untracked at write time: `.ufo/waves/round-58/` and `corpus/evidence/round58/controls/c2-before-frozen.txt`,
neither written by this seat).

## The mined mistake — exact row

- **Class.** *Vacuous gate by AND-leg masking*: a frozen counter emits its credit string in one token and
  matches it in another, so the top-line verdict is unreachable for **every** input, while a deny-only
  control battery (which is all this freeze scores) cannot distinguish an unpassable gate from a
  discriminating one. Inherited, not invented this round: round-57 wave 2 recorded the same masking mode
  as a *coverage finding* rather than a freeze blocker — `R57W2MutC3Counter.md:46` "all 8 single-edit
  mutants of the frozen C3 counter SURVIVE … every weakened leg is masked by sibling AND-legs on the
  passing state"; `corpus/lessons/round-57.md` "Counter kills" addendum kept it non-blocking. Its
  criterion is already in the lane: `corpus/QUALITY.md:915` (criterion 86, positive control seeded with
  the class the counter must credit) with `QUALITY.md` criterion 24 (controls scored before data).
- **Evidence pointer (frozen bytes, current HEAD).** `corpus/evidence/round58/c1-count.py:51-52`
  (`PASS = "pass"`, `FAIL = "fail"`); every refusal-leg emitter uses that constant —
  `:160` `f"{name}={PASS}(refused)"`, `:223` `f"FOREIGN={PASS}(refused)"`, `:234`
  `f"SYMLINK_OUT={PASS}(refused)"`; the gate matches the other token — `:391`
  `ref_pass = all(("=PASS" in l) for l in ref_legs)`; the printed tally repeats it — `:399`
  `REFUSE={sum('=PASS' in l …)}`; verdict `:394`, exit `:402`. The docstring at `:22` promises
  "`C1=PASS|FAIL` line; exit 0 iff PASS".
- **Behavioural consequence.** Six of the seven refusal legs come only from `expect_refuse` (`:160`), the
  seventh from `FOREIGN`'s pass branch (`:223`). No builder can produce `=PASS` in a refusal leg, so
  `ref_pass` is always `False` and `C1=PASS` is unreachable — not builder-dependent, a code invariant.
- **Second instance, same file, same class.** `:233-236` overwrites the leg whenever the symlink target is
  empty: `legs[-1] = f"SYMLINK_OUT={PASS}(refused)"`, discarding the `FAIL` that `expect_refuse` returned
  when the declared reason class (`["SYMLINK"]`) was absent. The reason check on that leg is not
  load-bearing.
- **Captured-by.** None at freeze. The freeze scored only deny controls (`controls/c1-controls.txt:17-18`:
  `DENIED=2/2`, controls `REFUSEALL.py` + the pinned r55 builder), and a deny-only battery is *satisfied*
  by an unpassable gate, so the receipt is vacuous on the credit path. This seat is the first to run a
  must-pass builder against the frozen counter.
- **Fix format.** (a) One token on both sides: `ref_pass = all(l.split("=",1)[1].startswith(PASS) …)`,
  same for the `REFUSE=` tally; (b) delete the `:234` rewrite or apply it only when `expect_refuse`
  already returned a pass; (c) add a must-pass control builder to `controls/` and require its receipt to
  contain `C1=PASS` **and** exit 0 at freeze — freeze rule: *the PASS string must appear in at least one
  pre-data receipt*; (d) until re-freeze, the L1 must not apply the C1 kill rule to a builder, because no
  builder can print `C1=PASS` under these bytes.

## Probe (scratch only; frozen bytes copied, never edited)

Scratch `S=/fast/scratch/hyaku/chousa-r58/R58ScribeMistakeMine` (removed before yield). Copy of the
frozen counter plus `controls/{build-spans-r55.py,REFUSEALL.py}`; a scratch mock builder
(`$S/mock/mock-builder.py`, ~110 lines) that refuses the declared hazard classes by `lstat`
(SYMLINK / NOT_REGULAR / FIFO / REGTYPE), `st_size > 64 MiB` (SIZE), `>100000` quote rows
(C1_QUOTES_ROWS_CAP), `..` in the entry column (ENTRY_ESCAPE), and foreign `spans/*` files (FOREIGN),
deriving spans from the cache `.txt` or, when present, the `.raw` through the pinned
`tools/capture-text.py`. It writes only under `--out`. It is a probe, **not** the round-58 deliverable and
not a proposal for it.

```
$ cd $S && TMPDIR=$S/work PYTHONDONTWRITEBYTECODE=1 python3 -B evidence/c1-count.py \
    --builder mock/mock-builder.py --work $S/work/run2 --seed 7 ; echo EXIT=$?
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=pass(refused)
SYMLINK_OUT=pass(refused)
SYMLINK_CACHE=pass(refused)
FIFO_TXT=pass(refused)
DEVZERO_TXT=pass(refused)
FAT_RAW=pass(refused)
MANY_QUOTES=pass(refused)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

All eleven legs the counter checks behave as the claim requires — including `HELDOUT_OK`, where the
counter derives the defined form itself from `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`
(raw sha256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`, re-opened this seat) and
compares digest+offset+span bytes — yet `REFUSE=0/7` and `C1=FAIL`. The frozen receipt for the *base*
builder, `controls/c1-controls.txt:16-18`, prints the byte-identical `SUMMARY OK=4/4 REFUSE=0/7 …` line
(differing only in `DENIED=2/2`). Healthy and failing states are indistinguishable in the receipt.

Second probe (reason masking), same scratch, one line changed in the mock's symlink-out branch
(`die("OUT_UNRESOLVED …")` — no `SYMLINK` token, nothing written to the target):

```
$ cd $S && TMPDIR=$S/work python3 -B evidence/c1-count.py \
    --builder mock/mock-builder-nosymlink.py --work $S/work/run3 --seed 7 | grep -E "SYMLINK_OUT|SUMMARY|C1="
SYMLINK_OUT=pass(refused)
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
```

`expect_refuse` returned `SYMLINK_OUT=fail(reason … absent)`; `:234` replaced it with `pass(refused)`.

## Gates

- Frozen predicate as written (`claims.md` C1): `python3 corpus/evidence/round58/c1-count.py --builder
  <builder> --work <fresh> ` must print `C1=PASS` and exit 0. Observed: unreachable at the frozen bytes
  for any builder → the C1 after-measurement (`c1-measure-after.txt`, not yet present) cannot be produced.
- Kill rule side effect: a correctly hardened builder would be killed for a counter defect ("any missing
  refusal reason … kills C1"), because `:391` reports every refusal as missing.
- Do-nothing-control clause (`claims.md`: "Do-nothing controls must not reach `C1=PASS`") is true only
  vacuously; `DENIED=2/2` carries no information under an unpassable gate.
- Untouched: `c2-count.py` (its verdict path uses uppercase literals at `:156`; no same-token defect seen),
  `controls/`, `tools/build-spans.py`, all git state. No install performed.

## Out of scope / unrun

- The round-58 hardened builder itself was not written or measured here; my mock only demonstrates that a
  builder can satisfy the battery and still be refused by the gate.
- Not run: `c2-count.py` end-to-end; the C1 builder legs beyond the battery (text-size caps, broader
  races — expressly not claimed by C1); any fetch (none authorized).
- I did not test whether a *false PASS* is reachable by other routes; that is `R58ReviewC1Counter`'s
  surface, not this row.

## Touched surfaces

Writes: this report only. Reads: `claims.md`, `corpus/evidence/round58/{c1-count.py,c2-count.py}`,
`corpus/evidence/round58/controls/*`, `corpus/QUALITY.md`, `corpus/lessons/round-57.md`,
`.ufo/waves/round-57/w2/R57W2MutC3Counter.md`, `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`.
Scratch `/fast/scratch/hyaku/chousa-r58/R58ScribeMistakeMine` removed before yield.

VERDICT: The attacked surface — *satisfiability of the frozen C1 predicate at 9e73a03* — **falsified**:
a builder satisfying all 11 declared legs (`OK=4/4`, 7/7 refusals, integrity leg, held-out capture) still
prints `C1=FAIL` with `REFUSE=0/7`, because refusal legs emit `=pass` while `c1-count.py:391` credits
`=PASS`; the `SYMLINK_OUT` leg additionally passes with its declared reason absent (`:234`). The mined
mistake is the inherited AND-leg-masking/vacuous-gate class (round-57 `R57W2MutC3Counter.md:46` recorded
it as coverage; `QUALITY.md:915` is the criterion that should have forced a must-pass control at freeze).
The counter's own deny-controls survive scrutiny (`DENIED=2/2`) but prove nothing about the credit path.
