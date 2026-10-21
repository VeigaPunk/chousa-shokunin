# FxCapR15 — capability-row freshness review

Axes: freshness; exact capability scope; current selftest/evidence-pointer integrity.

## Findings

None in the assigned SCORECARD row. Retain the round-15 row: it states the demonstrated narrow capability—reading a same-device absolute claim source under `--root /` instead of falsely refusing it as out-of-corpus—and labels first-working round 15 accurately.

Evidence:
- `SCORECARD.md:1316` distinguishes historical receipt cases 107–110 from current cases 107–109 and 111. `LOG.md:613,621-626` records the pre-fix refusal, landed fix, four original r15 tests, and `Capabilities +1`; `SCORECARD.md:743-778` records the before/after and r15 ADMIT verdict. This is a historical first-working claim, not a new r25 acquisition.
- Private clone base observed: `e93ac711f885a10d44fdd80a1734997419595b5a` (live-lane and clone `git rev-parse HEAD` both returned this hash). The earlier `0fc037e` pin omitted the gate; `d8c8cff` added the gate but omitted `corpus/evidence/README.md`; reviewed the full corrected e93ac checkpoint.
- `corpus/knowledge/root-slash-boundary-r15.md:3-5` resolves the source and four receipt paths; `corpus/evidence/README.md:946-949` indexes all four. The historic selftest receipt is present at `corpus/evidence/root-r15-20261019T152000Z-selftest.log:107-111`; the before/after demo at `corpus/evidence/root-r15-20261019T152000Z-demo.log:1-12` shows `OUT_OF_CORPUS` before and `CLEAN` `1/1` after for `/etc/hostname`.
- The knowledge entry's named limits (`root-slash-boundary-r15.md:61-74`) and round-25 lesson's out-of-population warning (`corpus/lessons/round-25.md:50-58`) do not negate this scoped claim; I do not treat historical battery “ALL IDENTICAL” as proof of CLEAN.

Assigned verification, in the private clone only: `bash tools/research-gate.sh --selftest` → `RESEARCH_GATE_SELFTEST: PASS (154 cases, 0 skipped)`. Relevant output only:

```text
ok-case  107 claims-root-slash-absent     exit=1
ok-case  108 claims-root-slash-read       exit=0
ok-case  109 claims-root-slash-xdev       exit=1
ok-case  111 sweeps-root-slash            exit=0
ok-case  129 chain-fence-anchor           exit=1
ok-case  130 claims-config-start          exit=1
ok-case  131 claims-omp-start             exit=1
ok-case  132 claims-localstate-start      exit=1
ok-case  133 claims-config-adjacent       exit=0
RESEARCH_GATE_SELFTEST: PASS (154 cases, 0 skipped)
```

This confirms current r15 IDs 107–109,111 and the adjacent r22/r23 mappings in `SCORECARD.md:1322-1323` (r22 130–133; r23 129). The gate's inline case comments retain round-era labels; the executed output is the current-index authority (current 110 is `claims-root-dslash`, current 111 is the r15 sweep case). No full battery or drift run was assigned. No LSP device/route was mounted; grep was used only to locate text, not as semantic proof. Only the requested report was written under the live lane; no source files were edited and no tools installed.

VERDICT: Retain the r15 capability row; its scope, first-working round, current case mapping, and knowledge/evidence pointers resolve.