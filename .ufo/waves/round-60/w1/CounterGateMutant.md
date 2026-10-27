# CounterGateMutant — round-60 bounded mutation probe

## Scope and pins

- Frozen claim: `corpus/evidence/round60-claims.md`, SHA-256 `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`. The claim specifies the C1 counter should derive verdict from structured observed behavior rather than child output. Frozen claim bytes were read only.
- Counter under probe: `corpus/evidence/round60/c1-count.py`, pristine SHA-256 `66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7`.
- Relevant prior committed evidence: `.ufo/waves/round-59/w1/R59Executor09.md:215-260` demonstrates the old counter's injected `=PASS` false positive; `:254-260` identifies child-controlled output scanning and calls for typed results. The current counter explicitly says output is diagnostic-only (`corpus/evidence/round60/c1-count.py:2-6,38-44`).

## Mutant and expected detector

In an isolated scratch copy, changed only the `forged_safe` gate at counter line 43 from `p.returncode == 0 and not intact` to `p.returncode == 0 and intact`. This deliberately classifies a successful child that leaves the protected foreign file intact as a forged-success state, weakening the gate separating the forged-output fixture from a genuinely destructive baseline. Expected detector: the existing C1 driver should print `INJECTION_REJECTED=0/1` and/or `BASELINE_DISCRIMINATES=0/1`, end `C1=FAIL`, exit 1; pristine and restored runs establish the detector baseline.

## Actual bounded detector outputs

All invocations used the same candidate builder (`tools/build-spans.py`) and the same counter entry point; work directories were fresh absolute paths under the mandated seat scratch.

Pristine:
```
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
BASE_EXIT=1
```
Mutated:
```
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=0/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
MUT_EXIT=1
```
Restored:
```
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=0/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
RESTORE_EXIT=1
```

## Verdict and restoration

**INCONCLUSIVE (baseline failure), not killed.** Pristine counter already fails the bounded detector because the candidate refusal leg is not accepted (`CANDIDATE_REFUSAL=0/1`, `C1=FAIL`). The mutation additionally destroys the baseline-control discrimination (`1/1` to `0/1`), but since pristine detector exit is already nonzero this is not a valid kill under the mutation protocol. Restored execution remains nonzero and shows baseline control no longer discriminates in this run; this is consistent with the mutated `forged_safe` branch having become the scratch copy's restored state? No: restored bytes hash exactly match source below, so the repeated output indicates a detector/work-state difference between pristine and later runs; do not infer a cause from these observations.

Hashes: pristine source `66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7`; mutant scratch `152eb340df97c88cfd230bd964903d9313b1836ac1f2b66beca6dff3e7f84f23`; restored scratch `66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7` (byte-identical to source). Source and frozen claim were not modified. Scratch `/fast/scratch/hyaku/chousa-r60/CounterGateMutant` removed before yield.