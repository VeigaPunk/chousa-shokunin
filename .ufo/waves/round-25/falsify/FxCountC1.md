# FxCountC1 — independent Claim 1 reproduction
Pins observed: initial 0fc037e6b07f3820ead8c9207a8034ac854197a1; authoritative full checkpoint e93ac711f885a10d44fdd80a1734997419595b5a; base d730ae4c33989ad9c8535764d4cae77b4db869f6.
Measured helper SHA-256: `8613a8488b164b867b00f5edd14c80cd06fde8c392914addb1dcb6a4ea0cd247` in e93 and at the assigned lane path; e93 gate SHA-256 `63a39282a15f19f5b0443212e66ad2dfc8ce0315e65697e479a7206879a598b2`.
## Findings
- LOW — `corpus/evidence/round25-measure.sh:15-20` does not fail closed on a missing frozen C1 member: `cp` errors are suppressed, the loop only prints a warning, and the reduced directory is measured. On a scratch e93 archive with clean `verify-all-r6.md` absent, exact helper output included `missing population member: verify-all-r6`, `METADATA_COMPLETE=24/27`, the same three named drifts, and `MISSING_INPUT_MEASURE_SCRIPT_RC=0`. Thus output is visibly noncanonical, but an automated consumer trusting process status or only the named list can accept an incomplete population; enforce the 28-member denominator before treating the helper as a pass/fail check.
## Reproduction
Base C1: `== tree /tmp/chousa-r25-FxCountC1-base gate 752e4e38`; `== claim 1 (operability): metadata screen over the frozen 28-entry population`; `verify-metadata rc=2`; `META_NAMED_DRIFT_ENTRIES=[]`. Base totals/holds matched `round25-measure-before.log:1-21`: `STALE_INDEX_ITEMS=66`, `STALE_RESTATEMENTS=15`, selftest `PASS (136 cases, 0 skipped)`, `GATE_DRIFT: none` / `drift rc=0`, exports `3/3`, helper rc=0.
Initial 0fc pin also has gate SHA prefix `752e4e38`; Claim 1 `verify-metadata rc=2`, selftest 136. This is the omitted-gate packaging failure, not the final result.
Intermediate d8c8cff3923f10481ac9ced66d0af7c41d38130c has the corrected gate and Claim 1 result below, but the same helper measured `2c EVIDENCE_MISFILED_ROWS=43` / `STALE_INDEX_ITEMS=43`; it is not the full C2 checkpoint.
Authoritative e93 run (same helper; private archive of the commit):
== tree /tmp/chousa-r25-FxCountC1 gate 63a39282
== claim 1 (operability): metadata screen over the frozen 28-entry population
verify-metadata rc=1
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=anchor-boundaries-r4.md key=recheck first-token=`bash
FINDING META_RECHECK_ROOT_PARENT severity=info surface=metadata obs=entry=anchor-boundaries-r4.md recheck uses --root ..
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=archived-export-intake.md key=recheck first-token=bash
FINDING META_RECHECK_ROOT_PARENT severity=info surface=metadata obs=entry=archived-export-intake.md recheck uses --root ..
FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=archives-verified-r9.md key=recheck absent
FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=audit-r11.md key=recheck absent
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=chain-resolution-r3.md key=recheck first-token=`bash
FINDING META_RECHECK_ROOT_PARENT severity=info surface=metadata obs=entry=chain-resolution-r3.md recheck uses --root ..
FINDING META_RECHECK_ROOT_PARENT severity=info surface=metadata obs=entry=citation-chain-fidelity-r24.md recheck uses --root ..
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=claim-verification-r2.md key=recheck first-token=`bash
FINDING META_RECHECK_ROOT_PARENT severity=info surface=metadata obs=entry=claim-verification-r2.md recheck uses --root ..
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=denylist-r22.md key=recheck first-token=`bash
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=fenced-anchor-r23.md key=recheck first-token=`bash
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=fenced-heading-r17.md key=recheck first-token=`bash
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=gate-baseline-r12.md key=recheck first-token=`bash
FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=gate-baseline-r8.md key=recheck absent
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=hardening-r10.md key=recheck first-token=`bash
FINDING META_RECHECK_ROOT_PARENT severity=info surface=metadata obs=entry=hardening-r10.md recheck uses --root ..
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=hardlink-alias-r13.md key=recheck first-token=re-run
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=html-comment-r20.md key=recheck first-token=`bash
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=mount-alias-r14.md key=recheck first-token=the
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=pointer-boundary-r21.md key=recheck first-token=`bash
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=reference-integrity-r7.md key=recheck first-token=`bash
FINDING META_RECHECK_ROOT_PARENT severity=info surface=metadata obs=entry=reference-integrity-r7.md recheck uses --root ..
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=root-slash-boundary-r15.md key=recheck first-token=`bash
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=scope-phrase-gap-r18.md key=recheck first-token=`bash
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=scope-refusal-r12.md key=recheck first-token=re-run
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=sweep-symlink-r19.md key=recheck first-token=`bash
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=sweeps-rejections-r5.md key=recheck first-token=`bash
FINDING META_RECHECK_ROOT_PARENT severity=info surface=metadata obs=entry=sweeps-rejections-r5.md recheck uses --root ..
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=verification-r16.md key=recheck first-token=`bash
FINDING META_RECHECK_UNSCHEDULED severity=info surface=metadata obs=entry=verify-all-r6.md key=recheck first-token=`bash
FINDING META_RECHECK_ROOT_PARENT severity=info surface=metadata obs=entry=verify-all-r6.md recheck uses --root ..
METADATA_COMPLETE=25/28
RESEARCH_GATE: DRIFT (entries=28 complete=25 findings=33 drift=3)
META_NAMED_DRIFT_ENTRIES=[entry=archives-verified-r9.md entry=audit-r11.md entry=gate-baseline-r8.md]
Holds on e93: `RESEARCH_GATE_SELFTEST: PASS (154 cases, 0 skipped)`; `GATE_DRIFT: none`; `drift rc=0`; `VERDICT_BEARING_EXPORTS=3/3`; `MEASURE_SCRIPT_RC=0`.
This matches `round25-measure-after.log:1-56`; e93 also reproduces `STALE_INDEX_ITEMS=0` and `STALE_RESTATEMENTS=0`. Lesson `round-25.md:111-133` records both packaging omissions: the gate at 0fc, then `corpus/evidence/README.md` absent at 0fc and d8; only e93 is the full integration pin.
Residual risk: this mode is a syntactic metadata screen, not full QUALITY criterion 6 enforcement (`knowledge/metadata-screen-r25.md:69-83`; `QUALITY.md:17-23`); this is already named, not a new regression. LSP status route is unavailable (`xd://lsp_status` returned “No such tool”); `grep` was used only as the literal fallback to locate the definition, and run outputs above are direct observations.
Verification gaps: no checks beyond the assigned measure script/holds; no installs.
VERDICT: Claim 1’s 25/28 result and named drift set reproduce on full pin e93; the helper has a low-severity missing-member fail-open risk.