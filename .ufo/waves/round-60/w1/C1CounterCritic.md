# C1CounterCritic — round-60 frozen-counter attack

## Counterexample

The claimed output-injection rejection is false for a builder whose complete behavior is to print the exact token and return success. Reproduced locally against the current round-60 counter:

```text
builder (/fast/scratch/hyaku/chousa-r60/C1CounterCritic/forge.py): print('=PASS')
command: python3 corpus/evidence/round60/c1-count.py --builder /fast/scratch/hyaku/chousa-r60/C1CounterCritic/forge.py --work /fast/scratch/hyaku/chousa-r60/C1CounterCritic/work --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
exit 0
```

The probe writes no files. `run()` seeds the foreign file, then computes `candidate_safe = (returncode == 0 and intact)` (current `c1-count.py:35-44`). This token-printing builder returns zero and leaves the foreign file intact, so it is classified `candidate_safe`. The forge probe is called `forged_safe` only when `run()` returns that state, but it does not: `forge_blocked` therefore becomes true (`:60-63`). `candidate_ok` also becomes true from the same state (`:68-70`). The counter emits `C1=PASS` (`:71-75`). Output bytes are not themselves establishing the verdict; rather, the mutant's unverified successful no-op is mistaken for safe candidate behavior, so the frozen claim's required mutant-fails predicate is still violated.

This is especially material because the frozen claim says the exact-token injection mutant “is scored as a failure” and requires `C1=PASS` iff the candidate reaches the safe path, the pinned unsafe control deletes the foreign file, and the output-injection mutant is rejected (`corpus/evidence/round60-claims.md:7-11`; frozen SHA declared by assignment: `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`). The probe currently awards the candidate leg based solely on return code plus one foreign-file observation. It does not establish that a candidate generated the expected output or that an output-injection-only implementation is not being credited.

## Prior evidence

The round-59 positive-path attack already showed the old frozen R58 counter's aggregate token scan could be forged via child stderr, and that a candidate could write through a symlink then be accepted after a case-only needle fix (`.ufo/waves/round-59/w1/R59Executor09.md:92-99,130-161,215-260`). The round-60 counter is a new implementation and avoids that exact stderr substring scan, but this replay identifies a distinct false acceptance in its state classification. Prior critic evidence also calls out the historical counter's inverted honest-builder result and false-positive path (`.ufo/waves/round-59/w1/R59Critic57.md:5-14`).

## Impacted axes

- **Operability (primary; frozen claim axis):** fails the stated target—an injection mutant does not fail, despite `INJECTION_REJECTED=1/1` and exit 0.
- **Calibration (secondary):** the displayed 1/1 rejection metric is not calibrated to the predicate it names; it means only “not classified as the destructive state.”

## Smallest safe correction

Make the negative-control assertion distinguish an output-only mutant from a genuinely successful candidate path. At minimum, require an independently checked expected artifact/result for `candidate_safe`, and define the mutant's expected state explicitly (e.g. child returns failure or an independently observed invalid/missing result) rather than treating “not destructive to the one sentinel” as safe. Add this exact print-token/return-zero/no-output builder as a regression control; require it to fail the injection-rejection predicate and make the top-level counter exit nonzero. Re-run the frozen command and retain the output as evidence before claiming C1 PASS. Do not infer from this narrow probe that the underlying builder meets the broader frozen hazard battery.

No source changes, frozen-claim edits, external fetches, installs, or git/jj mutations. Scratch was created at the assigned path for this probe and removed before report write.