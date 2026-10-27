# CounterProbe — frozen C1 counter review

## Finding

**C1's output-injection arm is not discriminating as implemented.** In `corpus/evidence/round60/c1-count.py:37-44, 60-63`, the synthetic `forged.py` only prints `=PASS` and exits 0. It does not delete/alter the seeded foreign file, so `run()` computes `candidate_safe=True` and returns `candidate_safe`; `forge_blocked` nevertheless becomes true because it rejects only the state string `forged_safe`. The frozen criterion at `corpus/evidence/round60-claims.md:7-11` requires that this output-injection mutant be scored as a failure. Instead, the exact test child satisfies the candidate's safe-path state. The aggregate can still fail for the current candidate leg, but that does not prove injection was rejected.

The flaw is in the counter/test classification, not a claim that the counter trusts printed output in its predicates: `run()` explicitly excludes captured output from derivation (`c1-count.py:38-44`). The test conflates “not destructive” with “not injected”; its boolean is true for a child that prints the targeted token and succeeds while preserving the fixture.

## Evidence chain

- Frozen contract and its three arms: `corpus/evidence/round60-claims.md:7-11`; specifically arm (c) requires the injection mutant to be scored as failure.
- Current implementation: `corpus/evidence/round60/c1-count.py:37-44` assigns `candidate_safe` on return code 0 plus intact foreign file, independent of stdout/stderr; lines 60-63 generate the injected `=PASS` child and set rejection by comparing only against `forged_safe`.
- Prior committed evidence establishes the risk model: `.ufo/waves/round-59/w1/R59Executor03.md:83-106` records an output-token forger accepted by the round-58 aggregate while all seven refusals fail and the symlink target is written; `R59Critic57.md:10-14` independently reports the forged stderr path. The new counter avoids that old substring mechanism, but its current synthetic arm does not demonstrate rejection of an otherwise failing leg.
- The selected frozen pre-work observation is `.ufo/waves/round-60/c1-before.txt:1-8`: injection flag 1/1 and pinned baseline discrimination 1/1, but candidate refusal 0/1 and `C1=FAIL`. This supports the measured baseline stop, not a claim that the arm-(c) semantics are sound.

## Scope and gaps

This is a source-level counter audit against the frozen claim and committed prior evidence; no candidate counter or builder was executed. Inference: a useful mutant needs to emit the forged token while independently failing the exact foreign-file-preservation leg (e.g. deleting the seeded file), and the test must require that it be classified as failure rather than merely “not the special destructive-output state.” No mutation or repair was made. The immutable claim file's expected SHA is `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`; another round-60 report observed a different SHA, so freeze-byte identity remains unresolved here. Scratch was created and removed at `/fast/scratch/hyaku/chousa-r60/CounterProbe/`.
