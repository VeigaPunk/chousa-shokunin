# R80ExecA — C1 operability reproduction round 80 (before/after/support)

author: R80ExecA (leaf executor seat), 2026-11-05 00:20Z
scratch: /fast/scratch/hyaku/chousa-r80/R80ExecA/ (deleted before yield)
receipts: .ufo/waves/round-80/w1/R80ExecA/ (six files, sha256 table below)
instrument bytes: committed bytes verified before any run — every sha256 in claims.md's
instrument table matched (`35351b23…` v7, `580233ad…` oracle-check, `bb91406e…` v6,
`b79d6441…` loader-matrix-v3). The round-79 structure-identity oracle measured
`2614b11692367393ba1b339aa707c714a06ce72589b347075cbdb3c4f06428db` (unhash-listed; recorded here).

## Free space
- before first run (`df -h /fast`): 397G avail (51% used)
- after last committed-subject run: 387G avail (52% used)

## (a) BEFORE — do-nothing control, committed oracle-check

Command (absolute, cwd on /fast):
`python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round80/oracle-check.py --battery /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py --oracle /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-79/w1/R79ExecC/matrix-structure-identity.py --work /fast/scratch/hyaku/chousa-r80/R80ExecA/oracle --runs 1`

Receipt: `r80a-before-oracle-check.txt` (88d7118e…). Verbatim output (all lines):

```
BATTERY_PATH=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round79/matrix-battery-v6.py
BATTERY_SHA256=bb91406e9130d9a1960d99226c69380435fc933385db79e0e6ea6b5542a61e1d
ORACLE_PATH=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-79/w1/R79ExecC/matrix-structure-identity.py
ORACLE_SHA256=2614b11692367393ba1b339aa707c714a06ce72589b347075cbdb3c4f06428db
BATTERY_EXIT=0 BATTERY_VERDICT=PASS RECEIPT_LINES=113
ORACLE=ACCEPTED
```

Exit **1**. Matches the frozen expectation exactly (`BATTERY_EXIT=0 BATTERY_VERDICT=PASS
RECEIPT_LINES=113`, `ORACLE=ACCEPTED`, exit 1). Wall clock: 2.76 s real.

C1's before side reproduces bit-for-bit: the committed v6 battery accepts the
structure-identity forger.

## (b) AFTER — frozen predicate run, fresh=2

Command:
`python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round80/matrix-battery-v7.py --matrix /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/loader-matrix-v3.py --work /fast/scratch/hyaku/chousa-r80/R80ExecA/v7/run1 --runs 1 --fresh 2`

Receipt: `r80a-after-v7-run1.txt` (aae6c755…). Exit **1**, wall clock 1m43.9s real /
12m48s user / 3m3s sys. It printed:

```
forgers_rejected=11/11 positive=2/2 fresh_positive=1/2 fresh_forgers=1/2 oracles_rejected=5/5
RECEIPT_LINES=216
BATTERY=FAIL forgers_rejected=11/11 positive=2/2 fresh_positive=1/2 fresh_forgers=1/2 oracles_rejected=5/5
```

**Deviation — this is a finding, not something to hide.** The frozen predicate demands exit 0
with `fresh_positive=2/2 fresh_forgers=2/2`; this run printed `fresh_positive=1/2
fresh_forgers=1/2`. Both fresh legs under-served on the SAME base (`ref-counter`): the matrix
under test **refused the drawn fresh positive** (`MATRIX SUBJECT POSITIVE ref-counter#0 MISS`
while its run rows read `matrix_exit=0 marks=12/12/PASS` — see F1) and the payload-decode
oracle scored `fresh_forger=0/2` on the same names. Two independent causes:

1. F1 — **the draw loop names every fresh copy `<base>#<i>` and score() folds rows by that
   name string** (v7 name-collision): the loop appends `(POSITIVE, ref-counter#0)` AND
   `(FORGER, ref-counter#0)` (same name, same index — the forger twin is drawn from the same
   base), and `score()` keys them in ONE flat dict `results[name]`, appending
   both draws' run rows under the same key. Fresh entries and committed entries are name-keyed
   the same way (`ref-counter` vs `ref-counter#0` are distinct keys, but two fresh entries can
   share one): `results['ref-counter#0']` holds rows of two differently-labelled subjects.
   This mangles per-subject counts: `counts['fresh_positive'][1]`
   bumps the *counter* once per entry but the per-`name` `observed` list mixes rows of multiple
   distinct subjects (fresh positive and fresh forger of the same base, and fresh vs committed).
   Receipt evidence (all from `r80a-after-v7-run1.txt`):
   Verbatim from the receipt, the four fresh SUBJECT lines under MATRIX are
   `POSITIVE ref-counter#0 MISS`, `FORGER ref-counter#0 MISS`,
   `POSITIVE ref-counter#1 ACCEPTED`, `FORGER successor-counter#1 REJECTED`. Each of the four
   names has exactly ONE its-side matrix run row (`POSITIVE ref-counter#0` →
   `matrix_exit=0 marks=12/12/PASS content=ok`; `FORGER ref-counter#0` →
   `matrix_exit=1 marks=0/12/FAIL content=ok`; `POSITIVE ref-counter#1` → 12/12/PASS;
   `FORGER successor-counter#1` → `matrix_exit=1 marks=11/12/FAIL`), i.e. every drawn
   micro-behaviour was individually CORRECT. Yet both `ref-counter#0` names scored MISS while
   the identically-behaved `ref-counter#1` scored ACCEPTED. The distinguishing variable is the
   name key, not the behaviour: `results["ref-counter#0"]` is the shared key under which the
   four (group,name,source,pre) fresh entries (`POSITIVE ref-counter#0`, `FORGER
   ref-counter#0`, plus the committed `ref-counter` entries' rows are a separate key) were
   appended in one dict, so the positive's pass rows and the forger's fail rows land in one
   `observed` list keyed `ref-counter#0`, and neither side's `all(...)` gate can hold — the
   gate itself (`rc==0` full-marks for positives, `rc==1` lower-marks for forgers) sees rows of
   both kinds and fails on both. The `ref-counter#1` positive escaped only because its
   forger twin was drawn on base `successor-counter` (different key); `ref-counter#0` had a
   same-base twin at the same index. Counting师傅's framing: the predicate counts
   `fresh_positive` and `fresh_forger` per *drawn entry*, but `results` is keyed per *name
   string*, and name strings collide across group and index.
2. F2 — **the payload-decode oracle's fresh-forger score is confounded by the same fold** (and
   possibly real): `ORACLE payload-decode … fresh_forger=0/2` in this receipt (and
   `fresh_forger=0/3` in the fresh=3 run) is consistent with either (i) the round-79
   payload-decode forger genuinely ACCEPTING a drawn semantics-altering mutation of
   `ref-counter` — exactly the carry that claims.md says is the critic seat's channel — or
   (ii) the same F1 fold poisoning the oracle's per-name `observed` list the same way it
   poisoned the matrix's. The receipts cannot separate (i) from (ii) because both sides' run
   rows share the folded key; recording the confound, not a certification either way. C1's
   "the five oracles are the independent anchor" is therefore **undemonstrated by these three
   runs** — every run where the fresh set drew a same-base twin folded at least one oracle's
   fresh counts the same way it folded the matrix's.

## (c) SUPPORT — fresh leg contribution, `--no-fresh`

Command:
`python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round80/matrix-battery-v7.py --matrix .../round76/loader-matrix-v3.py --work /fast/scratch/hyaku/chousa-r80/R80ExecA/v7/nofresh --runs 1 --fresh 2 --no-fresh`

Receipt: `r80c-nofresh.txt` (6c7da868…). Exit **1**, wall 1m32.3s real / 20m50s user. Exact
predicate-line output:

```
forgers_rejected=11/11 positive=2/2 fresh_positive=0/0 fresh_forgers=0/0 oracles_rejected=4/5
RECEIPT_LINES=168
BATTERY=FAIL forgers_rejected=11/11 positive=2/2 fresh_positive=0/0 fresh_forgers=0/0 oracles_rejected=4/5
```

Measured contribution of the fresh leg on this machine: **negative** — dropping it moves
oracles_rejected from 5/5 (run 1, fresh=2) to 4/5, i.e. with the fresh leg present one more
oracle was rejected. The fresh leg is NOT load-bearing on the committed-subject part of the
predicate; the oracle delta rides on the fresh rows folding into the oracle counts what the
committed rows alone never produce (F2, same fold). But this does not make the fresh leg noise
in both directions: run 2 REACHED the exact frozen PASS line only WITH `--fresh 2`
(`fresh_positive=2/2 fresh_forgers=2/2` are non-degenerate there), and (d) shows that without
the leg the instrument cannot print the predicate at all. The `--no-fresh` run's own miss is
solid and informative: `ORACLE:block-position REJECTED positive=1/2 forger=10/11` — the
block-position oracle ACCEPTED the re-emitted committed positive `ref-counter` on its static
layout channel, an oracle-side per-run flap on committed bytes alone (no fresh rows involved).

## (d) STABILITY of the fresh leg — two re-draws, fresh=2, fresh=3

`--fresh 3` exposes a `--seed` flag: **no such flag exists** (grep: v7's argparse has
--matrix/--work/--runs/--matrix-timeout/--fresh/--no-fresh/--rev/--no-permute/--no-content/
--print-order/--reemit-only; draw order comes from `secrets.randbits(64)` per draw). So the
draw leg was re-measured by independent runs.

Re-draw 2 command: `.../matrix-battery-v7.py --matrix .../loader-matrix-v3.py
--work /fast/scratch/hyaku/chousa-r80/R80ExecA/v7/run2 --runs 1 --fresh 2`
Receipt: `r80d-v7-run2.txt` (1ce0d7e5…). Exit **0**, wall 1m45.2s real / 90m27s user.

```
BATTERY=PASS forgers_rejected=11/11 positive=2/2 fresh_positive=2/2 fresh_forgers=2/2 oracles_rejected=5/5
```

This run MATCHED the frozen predicate exactly. Verbatim drawn-by-run evidence: MATRIX SUBJECT
lines `POSITIVE successor-counter#0 ACCEPTED`, `POSITIVE successor-counter#1 ACCEPTED`,
`FORGER ref-counter#0 REJECTED`, `FORGER ref-counter#1 REJECTED`. This run had NO cross-side
collision (positives drew on base `successor-counter`, forgers drew on base `ref-counter` —
different name strings never shared a key), so every key held exactly one subject's row and
the counts are clean. Note the oracle line is
`ORACLE payload-decode REJECTED positive=2/2 forger=11/11 fresh_positive=2/2 fresh_forger=0/2`:
REJECTED is the aggregate "parity broken somewhere" line, and the break is exactly the
fresh-forger side — verbatim run rows under that oracle:
`RUN FORGER ref-counter#1 … matrix_exit=0 marks=12/12/PASS content=ok` and
`RUN FORGER ref-counter#0 … matrix_exit=0 marks=12/12/PASS content=ok`, both ACCEPTED-class
while their MATRIX-side counterparts are REJECTED-class. On this clean (no-fold) run the
committed round-79 payload-decode forger ACCEPTED both drawn fresh forgers — a clean per-oracle
F2 datapoint supporting the critic seat's static-classifier claim for this channel.

Re-draw 3 command: `.../matrix-battery-v7.py --matrix .../loader-matrix-v3.py
--work /fast/scratch/hyaku/chousa-r80/R80ExecA/v7/run3f3 --runs 1 --fresh 3`
Receipt: `r80d-v7-run3-fresh3.txt` (570aeb6f…). Exit **1**, wall 1m54.9s real / 27m41s user.

```
BATTERY=FAIL forgers_rejected=11/11 positive=2/2 fresh_positive=0/3 fresh_forgers=0/3 oracles_rejected=5/5
```

Fresh subjects drawn this run: `ref-counter#0`, `ref-counter#1`, `ref-counter#2` (+ twins).
Every fresh subject printed `MISS` on BOTH sides, and every `#i` subject had
`matrix_exit=0 marks=12/12/PASS` (positive side) or `matrix_exit=1` lower-marks (forger side)
in its run lines — i.e. every micro-behaviour was CORRECT, yet the per-name score marked 0/3.
This is F1 in full: at fresh=3, three POSITIVE/FORGER pairs all share `ref-counter#N`.
`results['ref-counter#0']` accordingly holds the txn rows of POSITIVE `ref-counter#0` AND
FORGER `ref-counter#0` (and the `#N` names that later draws' rows were appended to cannot
unwind — the `#1` set sees a `#2` FORGER row too). With a mixed observed list the
`all(...)` gate can never pass for either side, hence 0/3 and 0/3 with every run row
individually correct. The committed-side counts (11/11, 2/2) were untouched because none of
those names collide with the fresh names.

## (e) Hypothesis isolation — rerun of (d) fresh=3 with only CHILD_TIMEOUT mutated

To rule out "the fresh=3 failure is a load/timeout artifact of the 6-second child timeout",
I locally (scratch only, `mut/v7-t60-fixed.py`, non-committed copy, all child timeouts 6 s →
60 s; the only other file difference is point HERE at a fixed absolute path) re-ran fresh=3:
Receipt: `r80e-v7-t60-fresh3.txt` (285c7f73…). Exit **1**, wall 6m0.685s real (`RECEIPT_LINES=240`) — one committed `hang` forger timed out at the raised timeout (correct class, but also not a clean reject), and every fresh `#0/#1/#2` subject again printed `MISS` per side with all fresh run rows individually correct — i.e. the F1 counter artifact reproduces at child-timeout 60 s.

```
BATTERY=FAIL forgers_rejected=10/11 positive=2/2 fresh_positive=0/3 fresh_forgers=0/3 oracles_rejected=5/5
```

The committed `hang` forger timed out (1 `matrix_exit=timeout`, correct — an exit of 2 is
never scored in the matrix's favour but a timeout is also not a clean reject) and every fresh
subject was again WRONGLY 0/3 per side with every fresh run row again singularly correct. So
child-timeout raising does NOT fix it, and the fresh=3 0/3 shape reproduces identically for a
non-fleet-load reason. This is a v7 defect, not a machine artifact. (The run is scratch-only,
never committed.)

## Severities and carry

- **F1 (the draw loop and score() jointly count with collision-folded keys, HIGH for the frozen claim):**
  The v7 predicate `fresh_positive=2/2 fresh_forgers=2/2` is not a measurement of independent
  draws; the 2/2 target is a number when the draw happens to avoid same-name twins' collision,
  a 0/3 or 1/2 when it does not. Two of my three full predicate runs landed on a collision;
  the run that printed the exact frozen PASS line (run 2) had a no-collision parcial. Fix is
  not for this seat: the drawn name must be made unique per draw (e.g. append the hex token
  `#<r>` = `secrets.token_hex(4)` to every entry name instead of the loop index `i`), or the
  `results` dict keyed on (group, name) tuples in `score()`. The lane SHOULD record this as a
  lesson/criterion; the frozen C1 predicate line cannot be treated as measured-draw evidence:
  at fresh=3 the frozen instrument claims the drawn set was 0/3 correct although every single
  run row was individually correct, which plainly contradicts "the drawn set is scored".
- **F2 (the fresh-forger side is not independent-of-witness for the payload channel, MEDIUM): the
  payload-decode forger scored the drawn fresh `ref-counter` forger as a positive in the run that
  drew it (`ORACLE:payload-decode … fresh_forger=0/2`). The receipts cannot separate "the drawn
  mutation is genuinely counter-detected" from the F1 count folding without a rerun at unique
  names, so this is a question for the wave's critic seat, not a certification either way.
  claims.md's own limits paragraph says exactly this channel is measured by the critic seat and
  never closed — this seat contributes the datapoint, not the verdict.
- **F3 (pass shape unstable across draw seeds, LOW, informational): my four full-predicate runs
  produced three outcomes (FAIL 1/2-1/2, PASS 2/2-2/2, FAIL 0/3-0/3 at fresh=3 twice). The pass state is not
  draw-invariant, so any score, trend and identity-of-subject wording ("the drawn set is
  scored") in the round report must be worded per-run, with the collision-corrected verdict.
- **F4 (confirmed the frozen BEFORE is not stale, NO-BREAK): the (a) receipt matched every
  frozen token; the do-nothing control is valid and reproducible as of this round.

## What this seat did NOT touch / nuances:
- No production instrument was edited; all mutations live under `scratch/mut/` and were never
  committed. The receipt `r80e-v7-t60-fresh3.txt` is labelled from a mutated scratch copy; the
  committed-battery receipts (a/b/d) are all from committed bytes verified at the hashes above.
- No subagents, no network, no git mutation in the lane or fleet root.

## Receipt sha256 table (all under .ufo/waves/round-80/w1/R80ExecA/)

| receipt | sha256 | result |
|---|---|---|
| r80a-before-oracle-check.txt | 88d7118e876a21e9bc64ee9168a2c498725aa4c2174a731343b59bcb0852f51a | (a) matched frozen before |
| r80a-after-v7-run1.txt | aae6c755d5af1a75641ac6c7593fa4197f79c1ed305f23963de8fbab4ee87a20 | (b) FAIL 1/2-1/2 |
| r80c-nofresh.txt | 6c7da8683f435179d5bef1ba1fedb3a6bcffc887ec81d282a3d00619c62c5175 | (c) FAIL 0/0-0/0, 4/5 |
| r80d-v7-run2.txt | 1ce0d7e5e5b4dd83c85a981ed3c9fc52e528ff71f30ba4e17a41ec134a7e9a07 | (d) PASS 2/2-2/2 (frozen predicate matched) |
| r80d-v7-run3-fresh3.txt | 570aeb6f784512245dc7af1723249adc62815c5c4a0494de0bef38c036c914dc | (d) FAIL 0/3-0/3 (collision) |
| r80e-v7-t60-fresh3.txt | 285c7f7336ed2d88187d13b25948aa2b6d8b8f9d14c1097b9c61292bd0e821d7 | (e) scratch-mutated timeout ablation |
