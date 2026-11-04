# Round-78 closure-removal twins — measured verdict table

Battery under mutation: `corpus/evidence/round78/matrix-battery-v5.py`
(sha256 `5545a4718690a80e5d3d6611e43132fdd5cb4dcd67e87be9a27ed44c032b5af0`, the frozen digest).
Detector, unchanged and frozen: `python3 -B corpus/evidence/round78/forge-battery.py
--battery <twin> --work DIR` (sha256 `ba98db41e0c82ba0ff3b7cb4259764fcfb85c54b17137da02655ee751f1c5143`).
`--runs 1`, `SETTLE=26` for every row (forge-battery defaults; no per-twin tuning).

| twin | mutation (diff lines) | twin sha256 | forge-battery exit | a1 | a2 | a7 | a5d | positive | handled | `FORGE_BATTERY=` |
|---|---|---|---|---|---|---|---|---|---|---|
| PRISTINE | none (frozen bytes) | `5545a471…b5af0` | 0 | REFUSED | REFUSED | REFUSED | DETECTED | ACCEPTED | 4/4 | PASS |
| M1 | `--print-order` forced on, quiet leg intact (1) | `e335d708…a2dac2` | 0 | REFUSED | REFUSED | REFUSED | DETECTED | ACCEPTED | 4/4 | PASS |
| M1B | M1 + ORDER line written when produced, flushed (5) | `f0844665…37cddd` | 0 | REFUSED | REFUSED | REFUSED | DETECTED | ACCEPTED | 4/4 | PASS |
| **M2** | interior inert statement → round-77 trailing `# salt <hex>` (3) | `a34b4de0…57ab59` | 1 | **FORGED** | **FORGED** | REFUSED | DETECTED | ACCEPTED | **2/4** | FAIL |
| **M3** | `RECEIPT_LINES` trailer removed (1) | `842a8210…18f06` | 1 | REFUSED | REFUSED | REFUSED | **FORGED** | ACCEPTED | **3/4** | FAIL |
| M4 | per-subject RUN lines written when produced, flushed (4) | `0f6b1600…aa204` | 0 | REFUSED | REFUSED | REFUSED | DETECTED | ACCEPTED | 4/4 | PASS |
| **M5** | M1 + ORDER **and** RUN lines written when produced (7) | `33f55b23…e538f` | 1 | REFUSED | REFUSED | **FORGED** | DETECTED | ACCEPTED | **3/4** | FAIL |

Full hashes: `mutants/SHA256SUMS`. Diffs: `mutants/<twin>.diff`. Raw detector output:
`receipts/<twin>.txt`; per-forger receipts: `forger-receipts/<twin>--*.receipt`; forger call
logs: `logs/<twin>-forger-calls.log`.

## Load-bearing attribution (a7 channel, from `logs/*-forger-calls.log`)

| twin | a7 `no ORDER line readable` | permutation recovered (`perm digest=`) | a7 subject calls classified positive=True/False |
|---|---|---|---|
| PRISTINE | 13 | 0 | 0 / 13 |
| M1 | 13 | 0 | 0 / 13 |
| M1B | 0 | 1 (8.4 s) | 0 / 26 (every call read `position=0`, `subject=constant-fail`) |
| M2 | 13 | 0 | 0 / 13 (the 2 `positive=True` lines are a2's, not a7's) |
| M3 | 13 | 0 | 0 / 13 |
| M4 | 13 | 0 | 0 / 13 |
| M5 | 0 | 1 (8.9 s) | 2 / 24 (positions 0…12 recovered in order) |

## Frozen v5 closure-removal flags (direct, not through forge-battery)

| command | exit | predicate line |
|---|---|---|
| `matrix-battery-v5.py --matrix corpus/evidence/round76/loader-matrix-v3.py --work DIR --no-permute` | 1 | `BATTERY=FAIL forgers_rejected=11/11 positive=2/2 oracle=MISS` |
| `matrix-battery-v5.py --matrix corpus/evidence/round76/loader-matrix-v3.py --work DIR --no-content` | 0 | `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` |

`--no-permute` oracle detail: `ORACLE block-position MISS positive=2/2 forgers_rejected=11/11`.
`--no-content` repeated 3×, exit 0 each time, identical predicate line
(`receipts/flags-no-content.txt`, `flags-no-content-2.txt`, `flags-no-content-3.txt`);
oracle detail includes `ORACLE block-position REJECTED positive=0/2 forgers_rejected=8/11`
(refused on the marks leg, not on content).
