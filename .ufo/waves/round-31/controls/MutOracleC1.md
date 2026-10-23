# MutOracleC1 — C1 feasibility and sensitivity

Disclosed Python feasibility reference only; **not a candidate**. Axes: contract fidelity, counter feasibility, mutation sensitivity, exact restoration.

## Seeds

- **S1** = `1809031821823329027`
- **S2** = `17643931508402779931`
- **S3** = `3147732890219402351`
- **S4** = `16353979551065984066`
- **S5** = `5012544795469142677`

## Control scores

All scores are actual `LINE_BINDING_MATCH=k/120` outputs of the frozen C1 counter. Every run used `timeout --kill-after=5 900`, lane-root cwd, 1 GiB address-space/120 s CPU/4096 shared-UID-task limits; one counter at a time. Temporary fixtures stayed in the assigned sandbox.

| Control | Counter | Seeds | Score(s) | Receipts |
|---|---|---|---|---|
| Full-contract oracle | C1 | S1–S5 | 120/120 each | [S1](MutOracleC1/oracle-s1.json), [S2](MutOracleC1/oracle-s2.json), [S3](MutOracleC1/oracle-s3.json), [S4](MutOracleC1/oracle-s4.json), [S5](MutOracleC1/oracle-s5.json) |
| `no-strict-grammar` | C1 | S1–S3 | 116/120, 116/120, 116/120 | [S1](MutOracleC1/no-strict-grammar-s1.json), [S2](MutOracleC1/no-strict-grammar-s2.json), [S3](MutOracleC1/no-strict-grammar-s3.json) |
| `first-occurrence-only` | C1 | S1–S3 | 108/120, 108/120, 108/120 | [S1](MutOracleC1/first-occurrence-only-s1.json), [S2](MutOracleC1/first-occurrence-only-s2.json), [S3](MutOracleC1/first-occurrence-only-s3.json) |
| `substring-no-boundaries` | C1 | S1–S3 | 108/120, 108/120, 108/120 | [S1](MutOracleC1/substring-no-boundaries-s1.json), [S2](MutOracleC1/substring-no-boundaries-s2.json), [S3](MutOracleC1/substring-no-boundaries-s3.json) |
| `range-start-only` | C1 | S1–S3 | 115/120, 117/120, 115/120 | [S1](MutOracleC1/range-start-only-s1.json), [S2](MutOracleC1/range-start-only-s2.json), [S3](MutOracleC1/range-start-only-s3.json) |
| `mislocated-before-unsupported` | C1 | S1–S3 | 112/120, 112/120, 112/120 | [S1](MutOracleC1/mislocated-before-unsupported-s1.json), [S2](MutOracleC1/mislocated-before-unsupported-s2.json), [S3](MutOracleC1/mislocated-before-unsupported-s3.json) |
| `off-by-one-lines` | C1 | S1–S3 | 85/120, 83/120, 84/120 | [S1](MutOracleC1/off-by-one-lines-s1.json), [S2](MutOracleC1/off-by-one-lines-s2.json), [S3](MutOracleC1/off-by-one-lines-s3.json) |

## Kill matrix

| Mutant | Expected detector | Actual failures S1 / S2 / S3 | Verdict |
|---|---|---|---|
| `no-strict-grammar` | I1 | I1 8/12 / I1 8/12 / I1 8/12 | killed 3/3 |
| `first-occurrence-only` | B2 | B2 0/12 / B2 0/12 / B2 0/12 | killed 3/3 |
| `substring-no-boundaries` | M2 | M2 0/12 / M2 0/12 / M2 0/12 | killed 3/3 |
| `range-start-only` | M4 | M4 3/8 / M4 5/8 / M4 3/8 | killed 3/3 |
| `mislocated-before-unsupported` | U1 | U1 0/8 / U1 0/8 / U1 0/8 | killed 3/3 |
| `off-by-one-lines` | B1, B2, B3, M1, M4, M6 | B1 0/12, B3 0/12, B2 1/12 / B1 0/12, B2 0/12, M3 11/12, B3 0/12 / B3 0/12, B1 0/12, B2 0/12 | killed 3/3 |

## Findings

- **Feasibility passes:** the complete C1 reference reached 120/120 on all five fresh seeds; no counter class rejects it. It enforces JSON-string/ASCII-decimal grammar, enumerates all (including overlapping) occurrences, copies both byte-level token-edge functions, checks both line endpoints, and keeps absent-span precedence.
- **All six defects killed on all three seeds.** Closest wrong control: `range-start-only`, **117/120** on S2 (97.5%). Only 3/8 M4 cases reject it on that seed: start-line-only/widened-end pointers are accepted incorrectly; end/late pointers still fail the start check. This is a narrow sensitivity margin, not a 120/120 escape. Grammar relaxation reaches 116/120 by misclassifying four invalid forms (`07`, ` 4`, `4 `, `4-4`).
- No observed fixture leak permits these assigned mutants to satisfy P1. Source review also shows only ASCII syllable words with space/newline/comma/period context: this probe does **not** establish sensitivity to joiner-specific, non-ASCII-edge, or overlapping-occurrence defects.

## Restoration and evidence

- Every mutant was applied only to the isolated `work-c1.sh`, archived with a minimal diff, then restored byte-for-byte in `finally`; the identical counter and S1–S3 were rerun after **each** restoration: all 18 restored scores were 120/120.
- Pristine/before/final/restored SHA-256: `c1ebbf61e4efaf9168cce0812f0bfb8368e2acdf492a2bc4fccab64b270bf078`.
- Per-mutant before/mutated/restored hashes, all 41 successful detector invocations, commands, actual stdout/stderr, and explicit restored-receipt paths: [manifest](MutOracleC1/probe-manifest.json); [machine kill matrix](MutOracleC1/kill-matrix.json). Counter/gate/claims source hashes remained unchanged.
- Initial RLIMIT_NPROC=64 setup attempts exited 125 before the counter could fork because the shared UID already had more tasks; they are recorded as inconclusive setup failures, never mutant kills. The corrected bounded runs above used 4096. No tools installed; no network, candidate, VCS writes, or other runtime used. All started detector process groups were reaped/terminated.

design holds

## v2 re-score

Frozen design `8070f92bac6ba1f2dfb6c29d66303d60a1e7dac7`; every one of the **39** new counter receipts was checked against C1 SHA-256 `c3aca35da30ee47edc3402daa559f43320e44a82d3a0143b5ea283ec8c49b427`. V1 artifacts/receipts are unchanged. Same bounds as above; only isolated v2 scratch bytes were mutated.

Fresh seeds: **V2S1**=`1974160508405359465`, **V2S2**=`6996389439849219100`, **V2S3**=`5268895580782469426`.

The v2 oracle and every mutant now emit `FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=<id> at=<at>` exactly for their **own** `mislocated` verdicts; this strengthens the controls rather than killing them for missing findings. The only shared v1→v2 source change is the [finding-emitter format](MutOracleC1/v2/oracle-v1-to-v2.diff). The oracle remains a disclosed feasibility reference, not a candidate.

| Control | Counter | Seeds | Score(s) | Expected detector / verdict | Receipts |
|---|---|---|---|---|---|
| Full-contract oracle | C1 | V2S1–V2S3 | 120/120 each | feasible 3/3 | [1](MutOracleC1/v2/oracle-s1.json), [2](MutOracleC1/v2/oracle-s2.json), [3](MutOracleC1/v2/oracle-s3.json) |
| `no-strict-grammar` | C1 | V2S1–V2S3 | 116/120 each | I1 8/12; killed 3/3 | [1](MutOracleC1/v2/no-strict-grammar-s1.json), [2](MutOracleC1/v2/no-strict-grammar-s2.json), [3](MutOracleC1/v2/no-strict-grammar-s3.json) |
| `first-occurrence-only` | C1 | V2S1–V2S3 | 108/120 each | B2 0/12; killed 3/3 | [1](MutOracleC1/v2/first-occurrence-only-s1.json), [2](MutOracleC1/v2/first-occurrence-only-s2.json), [3](MutOracleC1/v2/first-occurrence-only-s3.json) |
| `substring-no-boundaries` | C1 | V2S1–V2S3 | 108/120 each | M2 0/12; killed 3/3 | [1](MutOracleC1/v2/substring-no-boundaries-s1.json), [2](MutOracleC1/v2/substring-no-boundaries-s2.json), [3](MutOracleC1/v2/substring-no-boundaries-s3.json) |
| `range-start-only` | C1 | V2S1–V2S3 | 116/120 each | M4 4/8; killed 3/3 | [1](MutOracleC1/v2/range-start-only-s1.json), [2](MutOracleC1/v2/range-start-only-s2.json), [3](MutOracleC1/v2/range-start-only-s3.json) |
| `mislocated-before-unsupported` | C1 | V2S1–V2S3 | 112/120 each | U1 0/8; killed 3/3 | [1](MutOracleC1/v2/mislocated-before-unsupported-s1.json), [2](MutOracleC1/v2/mislocated-before-unsupported-s2.json), [3](MutOracleC1/v2/mislocated-before-unsupported-s3.json) |
| `off-by-one-lines` | C1 | V2S1–V2S3 | 81/120, 78/120, 80/120 | B1/B2/B3 and shifted-location false positives; killed 3/3 | [1](MutOracleC1/v2/off-by-one-lines-s1.json), [2](MutOracleC1/v2/off-by-one-lines-s2.json), [3](MutOracleC1/v2/off-by-one-lines-s3.json) |

- **New wrong-control max: 116/120**, tied by grammar relaxation and start-only binding. Fixed M4 sub-variants now force four range-mutant misses on every seed (v1 max was 117/120). No assigned mutant reaches P1; all 18 mutant trials are killed. The complete oracle reaches 120/120 on all three seeds, including the finding rule.
- Every mutation was restored in `finally`, then the identical detector/seeds were rerun: all **18 restored runs scored 120/120**. Exact pristine/before/restored/final SHA-256: `bfc0b02b83f554d134c6bb2c87610963a743f2e917a7d325611d844addf8c617`.
- Oracle, six mutant scripts/diffs, actual outputs, all counter pins, before/mutated/restored hashes, and explicit restoration receipts: [v2 manifest](MutOracleC1/v2/probe-manifest.json), [v2 kill matrix](MutOracleC1/v2/kill-matrix.json). All started detector process groups were reaped/terminated; no tools installed, network, VCS writes, or candidate runs.

design holds
