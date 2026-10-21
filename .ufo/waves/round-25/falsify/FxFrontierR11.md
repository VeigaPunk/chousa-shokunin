# FxFrontierR11 — freshness review

Axes: (1) claim/count accuracy, (2) receipt provenance, (3) preservation of limits.
Reviewed the full integrated Frontier block at private pin `e93ac711f885a10d44fdd80a1734997419595b5a` (observed HEAD).

## Findings

- **P2 — R1 hold receipt gaps were dropped; the erratum overstates preservation.** `corpus/README.md:548-550` (r12), `:565-568` (r13), `:706-710` (r20), `:730-733` (r21), and `:751-753` (r22) state `r1 3/3` without saying the round-specific receipts do not contain the tally. The round-25 drafts explicitly found this: `.ufo/waves/round-25/build/FrontierR12R13.md:36` (r12/r13 tally absent; r13 drift receipt absent), `FrontierR20R21.md:42` (both tallies absent), and `FrontierR22R23.md:16` (r22 tally absent). Search for `VERDICT_BEARING_EXPORTS` across `corpus/evidence/` returned no r12–r23 receipt hits; scorecard/log assertions and draft re-runs are not round receipts. Correct fact: retain these as asserted/re-run holds, not receipted holds; r13 `GATE_DRIFT: none` is likewise not separately receipted. R14, R16, and R18 gaps are qualified in the text; R23 omits the unreceipted 3/3 claim.
- **P2 — blanket erratum is false as written.** `corpus/README.md:795-802` says the new Frontier paragraphs “preserve each receipt gap,” contradicted by the omitted gaps above. Narrow this to the gaps actually called out, or add the missing qualifiers at the cited paragraphs.

## Verified / no disagreement

- Round 11 paragraph `corpus/README.md:508-535` matches `SCORECARD.md:425-459`, `LOG.md:500-512`, and `corpus/knowledge/audit-r11.md:1-7,38-60,73-77,190-200,225-252,304-340`: gate `46f5ddb3…`, HEAD `44cbad6…`, 85 cases, baseline `1c81a6cb…`, 3/3, 71 rows/queue 30, 28 findings, D1–D5, verdict, 8-line manifest SHA, 0/10 receipt-backed, SHONEN 0/4. The seat-count conflict and missing r11-named receipt are explicitly qualified; the round-12 gate transition is correct. The round-11 receipt absence also matches the draft’s findings.
- The specified historic battery and renumbering limits survive: `corpus/README.md:603-608,647-650,765-772,795-802` states `root=.` DRIFT is not CLEAN and identifies cases 130–133 as the post-r23 denylist cases. The r23 selftest confirms case 129 is `chain-fence-anchor`, cases 130–133 are the denylist cases (`corpus/evidence/round25-selftest.log:129-133`). The r15/r17-r23 battery logs inspected show `root=.` and `drift-sections=3 findings=13` where the erratum says they do.
- Freshness re-derivation at the full pin: `bash corpus/evidence/round25-measure.sh /tmp/chousa-r25-FxFrontierR11` → `STALE_INDEX_ITEMS=0`, `STALE_RESTATEMENTS=0`, `METADATA_COMPLETE=25/28`, selftest `PASS (154 cases, 0 skipped)`, `GATE_DRIFT: none`, `VERDICT_BEARING_EXPORTS=3/3`. Before receipt: `round25-measure-before.log` records 66 index items and 15 restatements.

## Checkpoint / residual risk

`0fc037e` is not a valid final proof pin: `git show 0fc037e:tools/research-gate.sh | sha256sum` → `752e4e382ed77c06ac5030ce2179c7ca524934f86fd2a6b25ef946ab027ac553` (old gate). `d8c8cff` fixes the gate but not the evidence index; its gate SHA equals e93’s `63a39282a15f19f5b0443212e66ad2dfc8ce0315e65697e479a7206879a598b2`. `LOG.md:882-896` records both packaging failures; all freshness/count conclusions above use full pin e93, not either intermediate.

Verification gap: no independent non-author closure was run by this seat. Installs/updates: none.

VERDICT: Round 11 claims are grounded; recommend correcting the omitted r12/r13/r20/r21/r22 receipt caveats and narrowing the “each receipt gap” erratum; freshness counts re-derived at e93ac71.