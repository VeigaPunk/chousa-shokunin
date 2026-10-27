# CounterAudit — round 60

## Findings by severity

### High — C1 predicate has a false-positive injection arm

The current frozen-claim bytes require an output-injection mutant that prints `=PASS` to be scored as failure (`corpus/evidence/round60-claims.md:7-11`). The counter instead seeds a foreign file, then marks any child returning zero while leaving that file intact as `candidate_safe` (`corpus/evidence/round60/c1-count.py:32-44`). Its generated `forged.py` only prints `=PASS` and exits 0 (`:58-63`); therefore `forge_blocked` is true for that successful no-op, since it rejects only state `forged_safe`. This does not establish the claimed negative-control condition.

I ran the declared counter against the current builder with isolated scratch: `python3 .../c1-count.py --builder .../tools/build-spans.py --work /fast/scratch/hyaku/chousa-r60/CounterAudit/c1 --seed 6001`. Output: `INJECTION_REJECTED=1/1`, `BASELINE_DISCRIMINATES=1/1`, `CANDIDATE_REFUSAL=0/1`, `C1=FAIL`; exit 1. Thus the frozen target is not met even independently of the flawed injection arm. Prior attack evidence `.ufo/waves/round-60/w1/C1CounterCritic.md` and `CounterProbe.md` reproduces the no-op false-positive mechanism. Minimum correction: require a meaningful expected result for candidate-safe and make the injection mutant fail an independently observed leg; assert its failure state, not merely “not destructive.”

### High — C2 counter accepts the pre-existing entry and does not enforce the frozen admission condition

Claim C2 requires a new round-60 note, exact observation/no overreach checks, and a base that fails because that note does not yet exist (`corpus/evidence/round60-claims.md:13-17`). But `corpus/evidence/round60/c2-count.py:8,13` selects the pre-existing `corpus/knowledge/citation-count-semantics-r37.md`; its checks at `:15-21` test source/form pins, one quote, broad metadata substrings, and two scope substrings, without requiring a round-60 entry, exact proposed observation, overreach prohibition, or scorecard disposition. I ran it with `/fast/scratch/hyaku-r60/CounterAudit/c2` as work: it printed `RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1`, `C2=PASS`, exit 0. This cannot verify the frozen base-fails or new-entry predicate. Also, `--root` roots raw and entry at the supplied root but `form` is script-global `ROOT/.ufo/waves/round-60/s101-open.txt` (`:7,13`), so an isolated root run mixes evidence roots. Do not treat this PASS as admission evidence; bind all inputs to the selected root and test the declared base and new note.

### High — immutable-claim hash provenance unresolved

Dispatch task text in `.ufo/waves/round-60/w1-dispatch.json` names expected SHA-256 `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`. The current `corpus/evidence/round60-claims.md` hashes to `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1` (`sha256sum`); SHA-1 is `5befe799a08ea80be4676bab99a359f5373b8fd3`, and Git blob ID is `5ea0acf0881f950be640754a21408a71ebd95e5e`. It is untracked against the declared base `b379919a873e7080a31ef92c7002f55f5374e2c6`, with no `git log` history for this path. I did not modify it. Evidence does not establish whether the file changed after dispatch or the provided expected digest was wrong; preserve this as unresolved freeze-integrity/provenance risk and do not silently substitute the observed hash for the claimed one.

## Residual risk and verification gaps

This was a bounded audit of current C1/C2 counters, claims bytes, prior wave counter attacks, and local executions only. No source edits, external fetches, commits, or Git/jj mutations were made. The C1 counter execution and C2 counter execution are observed results; no repair or post-repair verification was performed. Scratch was created under `/fast/scratch/hyaku/chousa-r60/CounterAudit/` and removed before completion.