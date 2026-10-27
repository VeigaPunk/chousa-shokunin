# Round 60 claims — frozen before wave data

Claim base: lane branch tip `b379919a873e7080a31ef92c7002f55f5374e2c6` (round-59 non-author review). The prior two honest-stop rounds identify two frozen, unsatisfiable predicates; this round claims one narrow correction to the frozen C1 verdict derivation, not that the current span builder is secure or that the entire C1 is fixed. No live external fetch; L0 `8d77e6c1` stays open.

## C1 — operability (lowest numeric axis, historical 3/10)

**Claim.** Replace C1's forgeable aggregate verdict with per-leg structured states such that captured builder stdout/stderr cannot satisfy a refusal leg, a failing leg cannot produce the exact PASS predicate by output injection, and the counter exits 0 only when the frozen safe and hazard legs meet their declared requirements. This is specifically the round-58 C1 counter's measurement integrity; it does not claim the builder itself meets all hazard legs.

**Frozen predicate.** Run `python3 corpus/evidence/round60/c1-count.py --builder <builder> --work <fresh-absolute-dir> --seed 6001`. It must print `C1=PASS` and exit 0 iff (a) the candidate reaches the independently observed safe path without deleting the foreign file, (b) the pinned r55 builder provides the known unsafe control by deleting it, and (c) the output-injection mutant prints `=PASS` but is scored as a failure. The counter captures child output only for diagnosis; output bytes cannot establish a leg state. Round-58 bytes remain frozen.

**Before → after.** Before: frozen round-58 C1 permits forged target-token output from the builder to satisfy refusal checks; W1 `R59Executor09.md` independently demonstrated C1=PASS with all seven hazards failing. After target: the new counter's structured result path accepts the safe candidate, demonstrates the unsafe pinned-base control, and rejects the same exact-token forge. Kill rule: candidate fails the safe path, any child output injection passes target, or the baseline control does not prove the intended destructive behavior. No numeric score change is presumed; report the measured verdict honestly.

## C2 — depth (sourced S101)

**Claim.** Add one scoped, source-grounded correction note that separates what S101's offline capture states about the bibliographic type/carrier notation from any present-day validity or CNKI implementation claim, and explicitly records the existing knowledge entry's S101 source-quote limit. This repairs no broken R58 counter and does not claim new ground unless a non-author gate confirms the proposed note clears QUALITY.

**Frozen predicate.** `python3 corpus/evidence/round60/c2-count.py --root <lane-copy> --work <fresh-absolute-dir>` must establish source digest and quote locations from committed S101 raw capture using the pinned capture-text form, verify the new entry's exact observation and no overreach against those source bytes, verify its S101 citation and metadata, and require the scorecard's declared disposition. Base must fail because no round-60 entry exists. Before any entry is admitted, re-open source S101 offline and record the located quote, URL, access date in Gate; external truth remains explicitly unknown. If the source quote/capture or QUALITY test is unavailable, do not admit and declare unprovable. This claim is causally independent of C1's counter edits.
