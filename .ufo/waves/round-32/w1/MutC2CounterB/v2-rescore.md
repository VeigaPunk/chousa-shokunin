# MutC2CounterB — design-v2 re-score

Read `claims.md` Design v2. Re-scored **all ten previously built wrong-output controls**, plus the unchanged BASE baseline; no oracle or candidate was built/scored. Frozen `c2-count-v2.py` SHA-256: `8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a`.

Every row used both fresh seeds **320260230401** and **320260230419**. Counts and RECORD_CHECKS below were identical on both seeds; every counter exit was **1**. **No control reached 132/132.**

| Control | Gate SHA-256 | Count on each seed | RECORD_CHECKS | Verdict |
|---|---|---:|---|---|
| unique | `77033ae59a13d6e63133755752f42e31d30485b81c11c7aa3f74c53fbe2e2a91` | 0/132 | ok | MISSES |
| observed | `cc16c479e920a1587802d4c10fc3c44112a70c54ecc11bb1cfcb2ba924095ead` | 0/132 | ok | MISSES |
| findings | `a3aebd9a8083f248133c8811b3f966760ecb47ce4aae7ca320c8ed0a34da5654` | 96/132 | ok | MISSES |
| stray-known | `d5022219705ffc0a6dccb1801cade13325df324f52c57f25780ea6f848e9444a` | 36/132 | ok | MISSES |
| exit | `f8576812142eeac5e35542cdd800477b90e44bebf944984e9a31803323d3d1ff` | 0/132 | fail:gate-rc=2 | MISSES |
| scrub | `346de1ab533113a9fc572adf651699a330b9c2cf65f5fbc5d9a8a28a831fac7a` | 0/132 | ok | MISSES |
| stray-unknown | `097adc9a9656d457e574b94794576312eb6ab8e0bcd29d0fbe488c1bfd92155a` | 0/132 | fail:stray-finding-hops=1 | MISSES |
| no-verdict | `5b77f3380fba86d44c9714f7101d27152ea941cb493bb31743f3e6ec1d45c079` | 0/132 | fail:drift-summary-lines=0 | MISSES |
| clean-exit | `d1da62bebfbeb9037f02af570a27981a8f1bbb903f110f9160cf8491c4cc2a6a` | 0/132 | fail:gate-rc=0,drift-summary-lines=0 | MISSES |
| duplicate-finding | `c70319a925c8c1b351721d4b802b0d6afe64c2363bb0ae758b68157f93ea3fb2` | 96/132 | ok | MISSES |
| base (intentionally pristine baseline) | `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258` | 0/132 | fail:gate-rc=0,drift-summary-lines=0 | MISSES |

All gates are at `/fast/scratch/hyaku/chousa-r32/w1/MutC2CounterB/v2/<control>/tools/research-gate.sh`. C1_TMP/C2_TMP/TMPDIR point to the disjoint sibling `v2/fixtures/`; no layout-guard refusal occurred. Each wrong-control SHA was checked to differ from BASE before scoring. Source gate hashes/mappings are in `v2/source-gates.json`.

The white-box emitter's **only behavioral accommodation** was fixture size 120→132 (including its summary denominator); its same deliberate defects were retained. Routing uses a separate v2 helper and truth sidecar generated from the frozen v2 generator for the two new seeds. These remain truth-fed parser-isolation controls, not citation readers. Original v1 helper/control bytes and restored counter copies were left untouched. Neither frozen counter was edited or mutated during this re-score.

Receipts: `v2/<control>-s<seed>.json`. Exact commands, exit codes, all 16 per-class printed lines and RECORD_CHECKS are in the corresponding `.output.json`. Consolidated evidence: `v2/results.tsv`, `v2/results.json`, and `v2/hashes.json` (counter, every gate, helper and truth-payload hashes).

Executed from the lane root, outer exit **0**:

```text
timeout 330s prlimit --as=1073741824 --nproc=8192 python3 /fast/scratch/hyaku/chousa-r32/w1/MutC2CounterB/rescore-v2.py score
```

The driver invokes the committed counter with `--gate`, `--seed` and `--receipt` on each of the 22 trials, each bounded at 120 seconds. Actual final output: `RESCORE_COMPLETE controls=11 trials=22 MEETS_TARGET=0`. No installations, network access, production edits, persistent processes or candidate scores.
