# FxCapR22 — capability-row falsification

Checkpoint used: private clone at `e93ac711f885a10d44fdd80a1734997419595b5a` (observed final HEAD). No production files changed.

## Findings

- **No row-level defect.** `SCORECARD.md:1322` accurately limits the capability to claim sources beginning `.config/`, `.omp/`, and `.local/state/`, plus the `.config-adjacent/` control. This matches the round-22 tests in `tools/research-gate.sh:5300-5325` and the knowledge note's named limits (`corpus/knowledge/denylist-r22.md:23-31`). The current case IDs are correct, and the knowledge/evidence paths resolve.
- **Historical first-working attribution does not overclaim.** Round 21 explicitly left direct `.config/foo` path-start citations as debt (`corpus/knowledge/pointer-boundary-r21.md:25-29`); round 22's original claim and verdict record the before-CLEAN / after-`CLAIM_SOURCE_SESSION` demonstration and all three path-start tests plus adjacent-path control (`LOG.md:796-800`; `SCORECARD.md:1142-1167`). The demo itself exercises `.config` (`corpus/evidence/deny-r22-20261019T190000Z-demo.log:1-12`); the round-22 selftest receipt covers the three classes and control (`...-selftest.log:129-133`).

## Current selftest evidence

Ran `bash tools/research-gate.sh --selftest` in the private full-checkpoint clone. Relevant output only:

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

`SCORECARD.md:1316-1323` correctly maps r15 to current 107–109,111; r22 to current 130–133 (historical r22 receipt 129–132); and r23 to current 129. `corpus/evidence/README.md:1021-1033` indexes all four r22 receipt files, and each referenced demo, selftest, battery, and drift file is present in the clone.

## Residual risk / verification gaps

The linked historical note's `recheck:` text still names r22-era cases 129–132 (`corpus/knowledge/denylist-r22.md:5`); current numbering is 130–133 because current case 129 is r23. This is historical numbering, not a row error; the SCORECARD row explicitly disambiguates it. The gate's comment at `tools/research-gate.sh:5295-5299` likewise labels the r22-era range. No LSP device was exposed, so no LSP status/references/definition/diagnostics were available; grep was used only to locate code, with conclusions grounded in direct reads and the executed selftest.

Packaging history: the initial `0fc037e6b07f3820ead8c9207a8034ac854197a1` omitted the gate and had old 136-case bytes despite prose claiming 154; `d8c8cff3923f10481ac9ced66d0af7c41d38130c` corrected the gate but omitted `corpus/evidence/README.md`; the full pin used here is `e93ac711f885a10d44fdd80a1734997419595b5a`. The two omissions are documented in `corpus/lessons/round-25.md:109-133`.

Installs: none.

VERDICT: Retain the r22 capability row; it is accurate, non-overclaiming, and uses the correct current selftest case numbers.