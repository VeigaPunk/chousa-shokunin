# ExecMetaMode — round 25
Base: clone HEAD from `git rev-parse HEAD` = `b820e4e40ce52deedf53b191140cd7b08ddda929`.
Behavior: `tools/research-gate.sh:305,2285-2437,5548,5619-22`; header scan, metadata findings, sorted entries, completion/verdict, and CLI help/dispatch.
LSP unavailable (no LSP tool route exposed); no installs. Risk: syntactic screen per v1, not semantic source validation; blockers: none.
Checks: clone selftest `PASS (151 cases, 0 skipped)`; base-vs-new case-line diff for 1–136: `diff` rc=0; measurement command `bash corpus/evidence/round25-measure.sh /tmp/chousa-r25-ExecMetaMode` completed.
Clone files written (SHA-256):
- `/tmp/chousa-r25-ExecMetaMode/tools/research-gate.sh` `149f8b02575a5ac0a2ddfc7dbc963b007420234ef8e08592a661c803836ee25a`
- `/tmp/chousa-r25-ExecMetaMode/base-selftest.log` `b53891717e8d00fcc47f6e69439063c07e97193bc4be7c6934f13c121979c19f`
- `/tmp/chousa-r25-ExecMetaMode/meta-selftest.log` `54870b1d74c981b700980b3d2fd737d6fac03f2ef073169ee52920080569581b`
- `/tmp/chousa-r25-ExecMetaMode/r25-meta.patch` `8ab2ec183e7353c9af4b3e18116afe9ae543dca269a070092b66b9da265546a7`
Claim 1 measurement block:
```text
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
```
Holds:
```text
RESEARCH_GATE_SELFTEST: PASS (151 cases, 0 skipped)
GATE_DRIFT: none
drift rc=0
VERDICT_BEARING_EXPORTS=3/3
```
VERDICT: Scoped implementation and requested measurement complete in the private clone; only the assigned report was written in the lane.