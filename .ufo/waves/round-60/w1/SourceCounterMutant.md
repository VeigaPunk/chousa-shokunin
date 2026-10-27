# SourceCounterMutant — C1 counter mutation probe

## Mutant
In an isolated copy of `corpus/evidence/round60/c1-count.py`, changed only the injection-arm predicate from `forge_blocked = forge_state != "forged_safe"` to `forge_blocked = forge_state != "candidate_safe"`. This flips the behavior for the actual generated `forged.py`: it prints `=PASS`, exits 0, and preserves the seeded foreign file, so `run()` classifies it `candidate_safe`. The mutant therefore treats that injected child as not blocked.

## Expected detector
Run the same bounded command against pristine and mutated bytes: `python3 <copy>/c1-count.py --work /fast/scratch/hyaku/chousa-r60/SourceCounterMutant/<pristine-work-or-mutant-work>`. A killing detector should make pristine succeed and mutant fail, or otherwise demonstrate an output change that isolates injection-arm behavior. The frozen claims specify `C1=PASS`/exit 0 only when injection is rejected and both builder-control legs pass (`corpus/evidence/round60-claims.md:7-11`).

## Actual outputs
Pristine counter SHA-256: `66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7`.

```text
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=0/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
pristine_exit=1
```

Mutant SHA-256: `fd8f0a57de77ad2d2cf6ed138d0a60d7fc96088f5497e6e3b511442347a8a0c0`.

```text
INJECTION_REJECTED=0/1
BASELINE_DISCRIMINATES=0/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
mutant_exit=1
```

## Verdict and evidence
**Inconclusive (not killed).** Output differs at `INJECTION_REJECTED`, so the probe reaches the mutated branch. However the pristine baseline itself exits 1 (`C1=FAIL`), since neither pinned baseline discrimination nor candidate refusal passes. Per mutation protocol, this baseline failure makes a kill inconclusive; it cannot establish that the frozen end-to-end detector passes on the unmutated code. The behavior aligns with the already-recorded source-level observation in `.ufo/waves/round-60/w1/CounterProbe.md:5-14`: the test forge prints the token but its return code plus intact-file state maps to `candidate_safe`, while the current predicate calls any state except `forged_safe` blocked. This probe did not run another runtime or modify lane source.

Frozen claim SHA expected: `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`; observed file SHA-256: `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1` (mismatch; no change made). Scratch was removed before completion. Restoration evidence: pristine and restored copies both hashed `66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7`; scratch removal check printed `scratch_removed=1`.
