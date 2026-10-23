# ExecPriorCounters — prior-counter no-harm check (round-35 w2)

Seat: `ExecPriorCounters` (leaf executor). Lane: chousa deep-research method.
Date: 2026-10-23. Read-only on all lane production files; no `git`/`jj` write.

## Verdict

**No-harm holds on every assigned prior counter.** All six committed counters
printed exactly their expected label on one fresh seed each against the landed
gate at the wave base revision `e87c5d7ea2dbf3730b36a3961de3f06261d015e4`, with
**zero misses by class** (`per_class` all `n/n`, `misses: []`, `predicate_holds:
true`). The round-35 C1 (grep pin) and C2 (mechanism witness) landings did not
regress any earlier round's counter.

Additional evidence in the same run set:

* **Second seed set** (3701–3706): identical labels, zero misses.
* **Base-gate differential**: the round-34 base gate
  (`a6307edf…`) scores the *same* label and the *same* per-class breakdown as the
  landed gate on all six counters, i.e. the round-35 change is behaviour-neutral
  on these surfaces (no hidden win, no hidden loss).
* **Discrimination check**: five cheap mutants of the landed gate, one per
  counter surface, each drive that counter **below** its total. No counter is
  vacuously passing.

## Assigned counters and results (landed gate, clone at `e87c5d7`)

Gate scored: `tools/research-gate.sh`, sha256
`1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` — the
landed gate named in the round-35 contract. Clone head
`e87c5d7ea2dbf3730b36a3961de3f06261d015e4`.

| counter | expected | printed label | seed | rc | receipt |
|---|---|---|---|---|---|
| `corpus/evidence/round31/c1-count.py` | 120/120 | `LINE_BINDING_MATCH=120/120` | 3601 | 0 | `receipts/r31c1v2.json` |
| `corpus/evidence/round31/c2-count.py` | 120/120 | `REVISION_BINDING_MATCH=120/120` | 3602 | 0 | `receipts/r31c2v2.json` |
| `corpus/evidence/round32/c2-count-v2.py` | 132/132 | `EXEMPT_AUDIT_MATCH=132/132` | 3603 | 0 | `receipts/r32c2v2.json` |
| `corpus/evidence/round32/c2-count-v3.py` | 132/132 | `EXEMPT_AUDIT_MATCH=132/132` | 3604 | 0 | `receipts/r32c2v3.json` |
| `corpus/evidence/round33/c1-count-v2.py` | 156/156 | `TOPLEVEL_FIELD_MATCH=156/156` | 3605 | 0 | `receipts/r33c1v2.json` |
| `corpus/evidence/round34/c2-count.py` | 37/37 | `DEADZONE_MATCH=37/37` | 3606 | 0 | `receipts/r34c2.json` |

**Misses by class: none.** Every `per_class` entry is `n/n` in all six receipts
(12, 9, 16, 16, 15 and 17 classes respectively) and `misses` is `[]` in all six.
`predicate_holds` is `true` in all six; `gate_rc=1` and `gate_timed_out=false`
in all six (exit 1 is the counters' expected drift-exit).

Class-by-class (landed gate, seed set 1), all full:
`r31c1v2`: B1 12/12, B2 12/12, B3 12/12, B4 6/6, M1 12/12, M2 12/12, M3 12/12,
M4 8/8, M5 6/6, M6 8/8, I1 12/12, U1 8/8.
`r31c2v2`: R1 24/24, R2 10/10, S1 16/16, S2 12/12, S3 10/10, S4 10/10, S5 8/8,
I1 14/14, N1 16/16.
`r32c2v2`/`v3`: R1 12/12, R2 12/12, R3 12/12, F1 12/12, E1 12/12, E2 6/6, E3 6/6,
E4 6/6, E5 12/12, E6 6/6, E7 6/6, E8 6/6, E9 6/6, E10 6/6, E11 6/6, E12 6/6,
`RECORD_CHECKS=ok`.
`r33c1v2`: N1 12/12, N2 12/12, N3 12/12, N4 12/12, N5 12/12, N6 12/12, N7 6/6,
N8 6/6, N9 6/6, N10 6/6, N11 6/6, D1 24/24, S1 12/12, S2 6/6, F1 12/12.
`r34c2`: dz-verbatim-ml 3/3, dz-verbatim-1l 2/2, dz-edge 2/2, dz-mut-head 2/2,
dz-mut-tail 2/2, dz-mut-center 2/2, dz-decoys 5/5, dz-decoys-exact 2/2,
dz-decoys-line-wrong 2/2, dz-split 2/2, dz-glued-left 2/2, dz-glued-right 2/2,
dz-glued-then-valid 1/1, dz-line-bound 2/2, dz-line-wrong 2/2, short-verbatim
2/2, short-mut 2/2.

### Supplementary (same surface, not in the assigned list)

`corpus/evidence/round31/c1-count-v3.py` → `LINE_BINDING_MATCH=132/132`
(seed 3801, `receipts/r31c1v3.json`), including the new class
`I2_nonstring_line_value 12/12`.
`corpus/evidence/round31/c2-count-v3.py` → `REVISION_BINDING_MATCH=132/132`
(seed 3802, `receipts/r31c2v3.json`), including `I2_nonstring_sha_value 12/12`.

## Commands (quoted)

Clone (scratch, `/tmp` only):

```
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
git clone -q /home/vgpnk/Projects/shokunin/chousa-shokunin \
  /tmp/hyaku/chousa-r35/w2/ExecPriorCounters/clone
git -C …/clone checkout -q e87c5d7ea2dbf3730b36a3961de3f06261d015e4
# => e87c5d7ea2dbf3730b36a3961de3f06261d015e4
sha256sum …/clone/tools/research-gate.sh
# => 1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617
```

Counter invocation (one per counter; run in parallel; `timeout 1700`):

```
cd …/clone && C1_TMP=$SCRATCH C2_TMP=$SCRATCH TMPDIR=$SCRATCH \
  timeout 1700 python3 corpus/evidence/round31/c1-count.py \
    --gate …/clone/tools/research-gate.sh --seed 3601 \
    --receipt …/w2/ExecPriorCounters/receipts/r31c1v2.json
```

Driver scripts (all under `/tmp/hyaku/chousa-r35/w2/ExecPriorCounters/`, outside
the lane): `run-prior.sh` (landed, seed set 1), `run-prior-seed2.sh` (seed set 2),
`run-base-diff2.sh` (round-34 base gate), `mutants.sh`, `mutants2.sh`,
`mutants3.sh`, `mutate.py`.

Receipt dirs (this seat's directory only):
`.ufo/waves/round-35/w2/ExecPriorCounters/receipts/` (landed, seed set 1),
`receipts-seed2/` (landed, seed set 2), `receipts-base/` (base gate),
`receipts-mutants/` (mutant gates).

Counter file hashes — the clone's copies are byte-identical to the lane's
committed counters, so the scored counters are the committed ones:
`r31c1v2 c3aca35da30ee47edc3402daa559f43320e44a82d3a0143b5ea283ec8c49b427`,
`r31c2v2 1064fdb356e25440c64bb4d4d5363acb9c1bbc32c687c8ea50096d74c849d500`,
`r32c2v2 8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a`,
`r32c2v3 6f362ece2e5e04c92212ee5a3547a69a6742c5658fd7ebc41688b68043e5a9fa`,
`r33c1v2 cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514`,
`r34c2 8c0def4d377cdf1a1e4bd2c9151bb0846216658ff14d725d15ac037c12212173`.

## Base-gate differential (round-34 gate, same seeds)

Gate: `.ufo/waves/round-35/repairs/base-gate.sh`, sha256
`a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`.
Same six counters, same seeds, same `per_class` breakdown: **all six labels
identical to the landed gate, `per_class` diff `IDENTICAL` for all six receipts.**
Receipts in `receipts-base/`.

Reproduction note: the r32 c2 counters carry a layout guard
(`corpus/evidence/round32/c2-count-v2.py:290-293`) that exits 2 when the
fixture temp dir lies inside the gate's lane root, where
`lane_root = dirname(dirname(realpath(gate)))`. Placing the base gate directly
at `<dir>/base-gate.sh` therefore makes `lane_root` the scratch parent and the
guard fires (`c2-count: fixture dir … lies inside the gate's lane root …`,
rc=2). The base gate must be placed at `<dir>/tools/research-gate.sh` for the
comparison to be a measurement of the gate rather than of the harness layout.
This is a harness-path sensitivity, not a gate finding.

## Discrimination check (mutants, /tmp only)

Each mutant is a copy of the landed gate with one surface broken, run through
the matching counter on the same seed. A counter that still prints its full
total would be vacuous.

| mutant | gate change | counter | label | imperfect classes |
|---|---|---|---|---|
| `m1_lineabsent` (gate `2510d276…`) | `json_has_key "$line" line` → `false` | r31 c1 v2 | `50/120` | M1,M2,M3,M4,M5,M6,I1 (all 0) |
| `m2_shaabsent` (gate `10fab263…`) | `json_has_key "$line" sha256` → `false` | r31 c2 v2 | `50/120` | S1,S2,S3,S4,S5,I1 (all 0) |
| `m3c_noexempt` (gate `1aa18b51…`) | the `CHAIN_EXEMPT_RESOLVABLE` `emit_finding` call removed (valid bash, `bash -n` ok) | r32 c2 v2 / v3 | `0/132` | all 16 classes 0; `RECORD_CHECKS=fail:gate-rc=0,drift-summary-lines=0` |
| `m4b_nodup` (gate `f8f93b19…`) | `json_dup` → always "no duplicate" | r33 c1 v2 | `132/156` | `D1_duplicate_top_level 0/24` |
| `m5_directmax` (gate `3ceacd2c…`) | `TOK_DIRECT_SPAN_MAX 32764` → `32768` | r34 c2 | `21/37` | 8 dead-zone classes 0 (dz-verbatim-ml/-1l, dz-edge, dz-line-bound, dz-line-wrong, dz-decoys-exact, dz-decoys-line-wrong, dz-glued-then-valid) |

Every counter drops below its total under a surface-breaking mutant, so the
full scores on the landed gate are informative, not vacuous.

Two first-attempt mutants were rejected as invalid harness artefacts, not
findings: `m3_noexempt` (`gate-rc=127`, dangling line continuation) and
`m4_nodup` (`gate-rc=2`, `bash -n` syntax error). Both were rebuilt
(`m3c_noexempt`, `m4b_nodup`) with `bash -n`-clean gates before use.

## Limits

* One seed per counter was required by the assignment; a second seed set
  (3701–3706) was run as free robustness and reproduced the labels exactly.
* This seat measures **no-harm of the prior counters only**. It does not
  re-score C1 or C2 of round 35, and it does not judge the round-35 witness or
  grep-pin claims (other seats own those).
* The base-gate differential reuses the round-35 repair copy of the round-34
  gate; it is a comparison of two gate blobs, not an independent re-derivation
  of the round-34 gate's provenance.
* `receipts-base` and `receipts-mutants` are extra artifacts beyond the
  assigned `receipts/` set; all are inside this seat's own directory
  `.ufo/waves/round-35/w2/ExecPriorCounters/`.
* No production file was created or modified by this seat; the only writes are
  this report and the receipt directories above. No packages were installed.

## Files

* Report: `.ufo/waves/round-35/w2/ExecPriorCounters.md`
* Receipts: `.ufo/waves/round-35/w2/ExecPriorCounters/receipts/` (8),
  `receipts-seed2/` (6), `receipts-base/` (6), `receipts-mutants/` (9: 6 valid
  + the 3 harness-invalid first attempts `m3_noexempt`, `m3b_noexempt`,
  `m4_nodup`, kept for the audit trail).
  These receipt files were already picked up by a sibling commit
  (`git ls-files .ufo/waves/round-35/w2/ExecPriorCounters/` lists all 29 at
  `7d21a33`); their content is unchanged by this seat.
* Scratch (logs, clone, mutant trees; 245 MiB):
  `/tmp/hyaku/chousa-r35/w2/ExecPriorCounters/`
  (`log-r3*.log`, `log-base-r3*.log`, `log-mut-*.log`, `clone/`, `mut-*/`)
