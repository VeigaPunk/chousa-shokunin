# R79ReviewA — independent attack on C1 (operability)

Seat: R79ReviewA (leaf reviewer). Base `ee70e6df19fe43b1b384166cf5d360c3b99dafe2`; controls
commit `e2bf2bbb5ca66f06b6571cbcaa15554d1a74a67c`; lane HEAD at review `b58a02dbc8876dd1ad7647d88ca2c9cb2ae51ff9`.
Receipts live in `receipts/` of this folder (copies of the outputs cited below; v5 and v6 forge
receipts in separate subfolders). Scratch dir was `$HYAKU_SCRATCH/chousa-r79/R79ReviewA/` and was deleted;
every copy cited is reproducible with `--reemit-only` / `salted_copy`.

## Verdict on C1

**Agree.** Every predicate line, exit code and derivative count reproduces from my own commands.
No channel of the textual sentence was found false. One residual channel (structure identity) is
recorded by the claim itself and was not measured by me (see Residual risk).

## Checks

### 0. Digests (frozen instruments)
`sha256sum` over the nine frozen files matches `claims.md` table exactly (v6 `bb91406e…`, forge-battery
`5761edc5…`, derivative-check `af6fbe72…`, a9 `851222ed…`, a8 `65f590af…`, v5 `5545a471…`). Receipt: stdout
recorded in session; table values match the claim.

### 1. Predicate, v6 (`forge-battery.py --battery matrix-battery-v6.py`)
- Command: `TMPDIR=… python3 -B corpus/evidence/round79/forge-battery.py --battery corpus/evidence/round79/matrix-battery-v6.py --work <scratch>/v6work`
- Receipt: `receipts/forge-v6.out`, `receipts/v6/*.receipt`
- Observed: `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1`, `EXIT=0`
- Per-forger lines: a1 REFUSED, a2 REFUSED, a7 REFUSED, a5d DETECTED (integrity=BAD), a8 REFUSED, a9 REFUSED; positive legit-matrix ACCEPTED.
- **Agree** with the frozen predicate line and exit code.

### 1b. Before, v5 (`--battery matrix-battery-v5.py`)
- Command: same driver with `--battery corpus/evidence/round78/matrix-battery-v5.py`
- Receipt: `receipts/forge-v5.out`, `receipts/v5/*.receipt`
- Observed: `FORGE_BATTERY=FAIL forgers_handled=5/6 positive=1/1`, `EXIT=1`; `FORGER a8-v5-salt-normalizer rc=0 … verdict=FORGED`.
- **Agree** with the before receipt.

### 2. Independent 40-byte window measurement (own code, set intersection)
- Script: `receipts/win40.py` (my own `{src[i:i+40]}` ∩ `{copy[i:i+40]}`; copies made via the battery's own copy function, not `derivative-check.py`).
- v6 command: `python3 -B win40.py v6` → `receipts/win40-v6.out`. Observed `DERIVATIVE_COPIES=0/13 WINDOW=40 battery=v6`, `EXIT=0`. Every `shared40=0`.
- v5 command: `python3 -B win40.py v5` → `receipts/win40-v5.out`. Observed `DERIVATIVE_COPIES=13/13 WINDOW=40 battery=v5`, `EXIT=0`. `shared40` ranges 551 (constant-pass) to 9148 (successor-counter).
- Longest shared window (`receipts/maxwin.py`, `receipts/maxwin.out`, bisection on window length): every v6 subject copy and every v6 oracle copy has `maxwin=23`. Matches the frozen `MAX_WINDOW=23`; the 23 bytes are the shared shebang line `#!/usr/bin/env python3\n`. `MAXWIN_SUBJECTS_DERIVATIVE40=0/13`. Oracles (`forge-order-matrix*.py`) `shares40=False`.
- The lane's own `derivative-check.py` was not used for these numbers; I ran the v6 `reemit` and v5 `salted_copy` directly.
- **Agree.**

### 2b. v5 byte-for-byte recovery (the "one four-line normalizer" claim for round 78)
- Script: `receipts/recover.py`, output `receipts/recover.out`. Deletes lines matching the `_r78<hex>` salt regex from each `salted_copy`, compares to source.
- Observed `V5_RECOVERED=13/13`, `EXIT=0`. **Agree**: the round-78 subject copy is a textual derivative recovered exactly.

### 3. Behaviour preservation (committed source vs re-emitted copy, same CLI)
- Positives, identical arguments `--lane <fixture> --base ee70e6df19fe43b1b384166cf5d360c3b99dafe2 --rev <rev>`, fixture = `git clone --shared` checked out at `b58a02db` (`git rev-parse --show-toplevel` asserted).
  - `receipts/beh-successor-src-e2bf2bbb.out` vs `receipts/beh-successor-copy-e2bf2bbb.out`: both end `C2=PASS checks=7/7 rev=e2bf2bbb5ca6 base=ee70e6df19fe`, `EXIT=0`, `diff` empty.
  - Same for `--rev HEAD`: `beh-successor-*-HEAD.out`, both `C2=PASS checks=7/7 rev=b58a02dbc887`, exit 0, `diff` empty.
  - `ref-counter`: `beh-ref-*` both `C2=PASS checks=7/7 ref`, exit 0, `diff` empty, for both revs.
- All 13 subjects (`receipts/beh13.py`, `receipts/beh13.out`): `BEH13 divergences=0/13`. Each committed run and copy run gives identical stdout (after path redaction) and identical exit code. Subjects with a non-PASS verdict agree too (`constant-fail` rc=1, `tree-identity` rc=1, `hang` times out at 20 s on both sides).
- Fixture state caveat (for transparency): the first pass reported one divergence, `order-twelve`, and a committed-vs-committed self-repeat DIFF. Cause was the forger's own `.forge-order` counter file in the fixture, not the copy. Rerun with `.forge-*` deleted before every invocation: `0/13`. Recorded in `receipts/beh13.out` (final pass) only.
- **Agree**: no behaviour divergence across the 13 subjects on the arguments used. The copy's `__file__` differs and nothing in the subject set depends on it (grep: only `__name__` guards, plus `forge-harness-source` which reads the *matrix's* `CASES`, not its own).

### 4. a8 and a9 run directly as matrices against v6
- `python3 -B matrix-battery-v6.py --matrix forgers/a8-v5-salt-normalizer.py --work …` → `receipts/m-a8.out`.
  - Lines: `MATRIX RUN POSITIVE successor-counter 0 matrix_exit=1 marks=11/12/FAIL content=ok`, `MATRIX SUBJECT POSITIVE successor-counter MISS`, `MATRIX SUBJECT POSITIVE ref-counter MISS`, `ORACLE block-position REJECTED positive=0/2 forgers_rejected=7/11`, `forgers_rejected=11/11 positive=0/2 oracle=REJECTED`, `BATTERY=FAIL forgers_rejected=11/11 positive=0/2 oracle=REJECTED`, `EXIT=1`.
- `--matrix forgers/a9-v6-wrapper-normalizer.py` → `receipts/m-a9.out`: same shape. `BATTERY=FAIL forgers_rejected=11/11 positive=0/2 oracle=REJECTED`, `EXIT=1`. `MATRIX SUBJECT POSITIVE ref-counter MISS`.
- Neither reaches full marks. **Agree.** (Positive 0/2 for both: a8 and a9 print fabricated tables, and their digests match no v6 copy.)

### 5. Positive control, legitimate matrix, default `--runs`
- `python3 -B matrix-battery-v6.py --matrix corpus/evidence/round76/loader-matrix-v3.py --work …` → `receipts/m-legit.out`.
- Observed (lines 163–166): `forgers_rejected=11/11 positive=2/2 oracle=REJECTED`, `RECEIPT_LINES=165`, `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`, `EXIT=0`.
- **Agree**: the legit matrix is accepted and the battery is not blanket-refusing.

## Residual risk and limits

1. **Structure-identity channel (not measured by me; claim itself records it as a limit).** A normaliser that unmarshals the wrapper payload and canonicalises the fresh identifier table would recover the module's structure, because re-emission preserves behaviour. Not built here. [INFERENCE] Such an answer-key forger that hardcodes canonical digests of the two positives would likely reach full marks on v6 as a `--matrix`, exactly as a8/a9 reach full marks on v5 textually. That does not falsify the textual sentence in `claims.md`; it bounds what the 6/6 predicate measures.
2. **The a8/a9 "handled" cells are constructive, not evaluative.** Both normalisers refuse because their hardcoded digests match no copy, so REFUSED is the expected outcome for *any* text-level normaliser that cannot recognise a v6 copy. The 6/6 is a strong statement only together with the 0/13 derivative measurement: together they say no textual window survives, so no text normaliser can recognise a positive. Reading the predicate alone overstates what it measures about forgers in general.
3. **Positive-control determinism:** one default-run pass with the legit matrix gave 2/2. I did not run repeated seeds; the battery permutes and re-emits per run, so the outcome is seed-dependent in principle.
4. **Scratch copies deleted.** The copy paths in the `win40-*.out` and `beh-*` receipts point to a scratch directory that was removed at yield. Regenerate with `--reemit-only` (v6) or `salted_copy` (v5) to recover the same bytes shape; the specific random names differ per run.

## Tooling
No tools installed or upgraded. Used the host's `python3` (3.14), `cc` (GCC 16.2.1) for the battery's C-compiled matrices, `git` (clone --shared only; no lane or fleet git mutations).

## Report-path note
The spawn spec named `.ufo/waves/round-79/w1/R79ReviewA.md`. The same spec limits writes to `.ufo/waves/round-79/w1/<seat>/` plus scratch, so this report is written at `.ufo/waves/round-79/w1/R79ReviewA/R79ReviewA.md` and not at the `w1/` level.
