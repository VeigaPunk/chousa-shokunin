# Round 25 — connector separability

**Axes:** operability (C1), freshness (C2), calibration (C3) [round25-claims.md:10,52,62].

## Read sets and observed base

- **C1** hashes `tools/research-gate.sh`, copies the fixed 28-file `POP1` from `corpus/knowledge/`, then invokes `verify-metadata` on those copies [round25-measure.sh:11,13-21]. `hardening-r10.md` is in that population [round25-measure.sh:14].
- **C2** reads `corpus/README.md`, `corpus/evidence/README.md`, `LOG.md`, and `SCORECARD.md`; 2d extracts `Capabilities +1` rounds from LOG and counts only four-cell rows with numeric final cells inside `## Capabilities` sections [round25-measure.sh:23-54].
- **C3** reads `SKILL.md` and `corpus/knowledge/hardening-r10.md`; it counts one exact phrase, SKILL ledger/queue tuples, `${GSHA}`, and missing addendum headings [round25-measure.sh:57-78].
- The holds are separate: gate selftest, `--drift` against the r12 baseline, and the three fleet exports [round25-measure.sh:81-85]. Drift captures the gate's own temporary fixture and runs `verify-all` there [research-gate.sh:2636-2650]; the registered metadata mode is expressly not composed into `verify-all` [round25-claims.md:41-49].
- Recorded base output: `round25-measure-before.log` reports C1 rc=2; C2 `2+13+43+8=66`; C3 `1+3+2+1+8=15`; selftest PASS (136), drift none, exports 3/3 [round25-measure-before.log]. This is the supplied before receipt; I did not rerun the gate/selftest.

## Separability findings

- **Registered claim edits do not move another claim's count, with one shared-file condition.** C2 files are outside C1's POP1 and C3's two-file set. C3's hardening edits do share a physical file with C1's POP1, but C1 reads only its metadata header: `verify-metadata`'s registered header ends at the first out-of-fence `## ` [round25-claims.md:24-28]. In base `hardening-r10.md`, metadata is lines 3-22 and that boundary is line 31; C3's `${GSHA}` is line 488 and appendices start at line 470 [hardening-r10.md:3-31,470-492]. So append-only C3 work leaves C1's result stable; editing lines 1-30 would not. Base header SHA-256 (lines 1-30): `850745f7293996ba6c9b1f9d7880a76df96512d92ecd8640b4f50f04c726a9dd` [base archive d730ae4, local hash observation].
- **C1→C2 has a semantic freshness seam that the count misses.** C1 adds a knowledge entry [round25-claims.md:50,74-76], while C2's 2a is frozen to base filenames [round25-measure.sh:27-33]. Therefore, C2 can reach zero before that new entry exists and stay zero afterward without indexing it. Run C1 before C2 and include the new entry (and round-25 lesson) in the coverage map.
- **C3→C2 has a second-order index seam.** The base coverage row for `hardening-r10.md` still describes the 71-row / 38·25·3·1·4 / queue-30 snapshot [corpus/README.md:30], while the current hardening addenda already end at 38·21·10·0·3 / queue 24 [hardening-r10.md:549-551]. C2's 2a tests only whether the path occurs, not whether that summary is current [round25-measure.sh:27-33]. After C3's r16-r23 addenda, C2 should refresh the row or explicitly mark its figures historical; otherwise the count can be zero while the freshness description remains stale.
- **SCORECARD verdict edits are count-disjoint only outside Capabilities.** Verdict tables are separate sections [SCORECARD.md:1254-1267]; 2d ignores them unless an edit changes a four-cell numeric-round row under a Capabilities heading [round25-measure.sh:45-53]. The LOG side is dynamic: if the landing records round 25 as `Capabilities +1`, 2d will require a round-25 capabilities row in the same landing [round25-measure.sh:43-53; C1 is registered as capability acquisition at round25-claims.md:10].
- **SKILL prose cleanup can false-pass 3a.** The count is only the literal `remains open pending fix-or-absorb` [round25-measure.sh:60-63], but C3 requires a replacement pointer plus re-deriving command and an appended erratum [round25-claims.md:68-70]. Deleting/rewording that sentence alone zeroes 3a; overlapping edits to SKILL tuples also move 3b [round25-measure.sh:65-70].
- **C3 has an internal ordering dependency:** 3b compares SKILL totals to the last tuple/queue found in hardening [round25-measure.sh:65-70]. Append all r16-r23 addenda first, then set SKILL to the final revision (or land them atomically).

## Bounded proposal and handoff

Add a small cross-claim guard to `round25-measure.sh`: assert the hardening header hash above is unchanged when C3 is evaluated, and make 3a require a positive replacement pointer/command plus erratum, not phrase deletion alone. Keep 2d's existing dynamic check; ensure the round-25 LOG capability claim has its four-cell SCORECARD row. This guards the only count-level file overlap and the SKILL false-pass, without adding a new measurement convention.

**Landing order:** C1 first (before any backfill of the three named `recheck:` headers); C3 next (addenda before final SKILL totals/pointer, after other SKILL edits); C2 last (so it can index C1's new entry and refresh/label the hardening summary after C3). Put the round-25 capability row alongside any matching LOG line, then rerun the full measure at final landing.

**Isolated verification vectors:** C1-only should show its registered 25/28 and three named drifts, while C2=66 and C3=15; C2-only should show C2=0, C3=15, and C1 rc=2 as expected with the new mode reverted; C3-only should show C3=0, C2=66, and C1 rc=2. Combined landing should show C1=25/28, C2=0 (including any round-25 LOG capability row), C3=0, and the registered holds. Run gate/selftest scenarios only in the permitted private checkout.

Installs: none.
VERDICT: The three counters are separable under registered scopes if C3 preserves the metadata header; land C1 → C3 → C2 and guard the SKILL replacement so measurement cannot reward deletion or leave a stale index unnoticed.