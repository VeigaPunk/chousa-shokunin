# R75Mutation — kill matrix (round 75, W1, leaf seat)

Frozen revision `43a7a0db52c8aabdf32735f58e09610e05200e79`. Instruments under test:
`corpus/evidence/round75/loader-matrix-v2.py` (sha256 `95bdd49363e4…0268ee7`) and
`corpus/evidence/round75/matrix-battery.py` (sha256 `c35e937b4b7c…d2377ac4e`).
Scratch: `/fast/scratch/hyaku/chousa-r75/R75Mutation/` (removed after the run).

Detector for every matrix mutant: the frozen battery, exact predicate line
`BATTERY=PASS forgers_rejected=5/5 positive=2/2` / `BATTERY=FAIL …`, exit 0/1.
Baseline (pristine v2, frozen battery): `PASS forgers_rejected=5/5 positive=2/2`, exit 0.
Relocated pristine battery over a scratch copy of v2: same, exit 0 (relocation control).

## Battery kill matrix

| # | Mutant (single hunk) | sha256[:12] | Expected detection | Observed (2 matrix seeds per battery run) | Battery exit | Verdict |
|---|---|---|---|---|---|---|
| M1 | drop the three content cases (`dup-*`) | `c270c230b84a` | diff-only and naive-grep accepted → `forgers_rejected<5` | `BATTERY=FAIL forgers_rejected=3/5 positive=2/2`; diff-only `9/9 exit0`, naive-grep `9/9 exit0` | 1 | **KILLED** |
| M2 | restore declared order (no shuffle) | `ca1fc14dbe9c` | a source-blind declared-order oracle reaches full marks; battery cannot see it | `BATTERY=PASS forgers_rejected=5/5 positive=2/2` (twice); r74 oracle 9/12; v2-aware oracle **12/12 exit 0** | 0 | **SURVIVED** |
| M3 | treat exit 2 as satisfying `expected_rc` | `6f9cb0d635f1` | exit-2 subject scored in its favour | `BATTERY=PASS forgers_rejected=5/5 positive=2/2` (twice); exit-2 full-pass probe 0/12 pristine → **4/12** mutant | 0 | **SURVIVED** |
| M4 | compare exit codes only, ignore check ids | `8c208f0de2d4` | wrong check ids accepted | `BATTERY=PASS forgers_rejected=5/5 positive=2/2` (twice); constant-fail 4/12 → **8/12**; all-FAIL/rc1 probe 0/12 → **8/12** | 0 | **SURVIVED** |
| M5 | skip restoring fixture bytes between cases | `9b980993bf9f` | correct counters fail | `BATTERY=FAIL forgers_rejected=5/5 positive=0/2`; successor 4–5/12, ref 4–5/12; direct successor 2/12 | 1 | **KILLED** |
| M6 | receipt fixture/case points at an unmonitored path (`…-wrong.txt`) | `f2e5c346c8db` | correct counters fail on `receipt-change` | `BATTERY=FAIL forgers_rejected=5/5 positive=0/2`; both positives 11/12 both runs; direct successor 11/12, only `receipt-change` fails | 1 | **KILLED** |
| M7 | battery: forger "rejected" when its exit is 0 | `8eec053895f9` | battery's own predicate/positive control breaks | over pristine v2: `BATTERY=FAIL forgers_rejected=0/5 positive=2/2`; all five forgers labelled `ACCEPTED` | 1 | **KILLED** |

Matrix-mutant score: 3 killed / 3 survived. Overall: 4 killed / 3 survived / 0 inconclusive.

## Direct-matrix probes (what the battery cannot see)

| Probe (scratch counter, reads no repo bytes unless stated) | Pristine v2 | Mutant |
|---|---|---|
| `probe-order-oracle-v2.py` (12-entry script, declared order) | `3/12 FAIL` exit 1 | M2: `12/12 PASS` exit 0 |
| frozen `forge-order-oracle.py` (r74 9-entry script) | `3/12 FAIL` exit 1 (battery runs 4–6/12) | M2: `9/12 FAIL` exit 1 |
| `probe-exit2-fullpass.py` (full marks, exits 2) | `0/12 FAIL` exit 1 | M3: `4/12 FAIL` exit 1 — PASS on unchanged + 3 appends with `actual_rc=2` |
| `probe-all-fail-rc1.py` (all checks FAIL, exits 1) | `0/12 FAIL` exit 1 | M4: `8/12 FAIL` exit 1 — every `expected_rc=1` case accepted |
| `correction-count.py` (positive) | `12/12 PASS` exit 0 | M5: `2/12` exit 1; M6: `11/12` exit 1 (`receipt-change` only) |

## Survivor findings (coverage findings, not contract changes)

- **F1 (M2).** Forger rejection is `rc==1 and marks<total`. The three content cases keep every
  source-blind subject below full marks, so removing order randomisation is invisible: the
  battery passes while a 12-entry declared-order oracle that reads no repository bytes scores
  12/12 exit 0. The battery's only order subject is the frozen 9-entry r74 script, which tops
  out at 9/12 under M2. The frozen v2 matrix does shuffle; QUALITY 120 is implemented but not
  battery-covered.
- **F2 (M3).** No battery subject ever exits 2, so the documented rule "an exit of 2 is never
  scored in the matrix's favour" is untested: M3 scores exit-2 subjects as PASS on all four
  `expected_rc=0` cases and the battery still prints PASS.
- **F3 (M4).** Rejection needs only fewer than full marks, so dropping check-id/summary
  comparison is invisible: constant-fail doubles 4→8/12 and the all-FAIL probe gains 8 free
  passes, while the battery still rejects every forger (8<12) and prints PASS.

## Restoration

- Frozen instrument digests before == after (diff empty).
- Restored/pristine rerun: `BATTERY=PASS forgers_rejected=5/5 positive=2/2`, exit 0,
  `MATRIX_SHA256=95bdd493…`.
- No production or lane writes; `git rev-parse HEAD` still `43a7a0db…`. Read-only
  `git status --porcelain -- corpus/evidence/round75 corpus/evidence/round74` shows only two
  untracked files created by sibling seats during this wave
  (`controls/battery-stability-r75.txt`, `controls/mutation-battery-parser-slip.txt`), not by
  this seat.
- Scratch root removed.
