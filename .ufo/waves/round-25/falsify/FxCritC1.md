# Round 25 — Claim 1 falsification (advisory)

Axes: **operability** (primary); **calibration** is harmed only if the screen is presented as Criterion-6 enforcement. No judgment/admission.

## Checkpoint and count

- Pre-registration: `corpus/evidence/round25-claims.md:10-50`; frozen 28-entry population and predicted result are explicit (`:17-18,44-49`). Source rows for the new entry are `SOURCES.md:29-30` (S019/S020 mined; `used-by` names `metadata-screen-r25.md`).
- First private clone at `0fc037e6b07f3820ead8c9207a8034ac854197a1`: `bash corpus/evidence/round25-measure.sh <clone>` observed `gate 752e4e38`, `verify-metadata rc=2`, no named findings, selftest PASS (136 cases). **C1 was not delivered at 0fc037e**; the committed prose/receipt could not prove the claimed gate behavior.
- Corrected gate checkpoint `d8c8cff3923f10481ac9ced66d0af7c41d38130c` still omitted `corpus/evidence/README.md`; the same full script there observed `2c EVIDENCE_MISFILED_ROWS=43` / `STALE_INDEX_ITEMS=43`. This is the second packaging omission, C2-only, not a C1 failure. Lesson R25-M13 records both omissions and says d8 is gate-only (`round-25.md:111-133`); `LOG.md:882-896` agrees.
- Final full integration pin used for the final rerun: `e93ac711f885a10d44fdd80a1734997419595b5a`; `sha256sum tools/research-gate.sh` = `63a39282a15f19f5b0443212e66ad2dfc8ce0315e65697e479a7206879a598b2`.
- Full `round25-measure.sh` at e93: Claim 1 `rc=1`, `METADATA_COMPLETE=25/28`, `RESEARCH_GATE: DRIFT (entries=28 complete=25 findings=33 drift=3)`, named set exactly `archives-verified-r9.md`, `audit-r11.md`, `gate-baseline-r8.md`, each `META_RECHECK_ABSENT`. Holds observed: selftest PASS (154 cases), `GATE_DRIFT: none`, `VERDICT_BEARING_EXPORTS=3/3`. This matches `round25-measure-after.log:1-39` and the registered prediction. The full e93 run also gave `STALE_INDEX_ITEMS=0`; the d8 count is not the final receipt.
- Direct directory run at d8 (same gate bytes as e93) included the new `metadata-screen-r25.md`: `source=present verified_at=dated recheck=scheduled verdict=clean`; whole directory `26/29`, drift only the three legacy missing-recheck records. The frozen 28-file measurement intentionally excludes the new entry.

## Counterexample and scope

Observed disposable fixture:
```text
source: S999 — https://example.invalid/x — §missing
verified-at: 2026-10-21
recheck: 7d
## Claim
```
`S999` has no match in `SOURCES.md`. On the final gate: `META entry=bad.md source=present verified_at=dated recheck=scheduled verdict=clean`; `METADATA_COMPLETE=1/1`; `RESEARCH_GATE: CLEAN`; exit 0. Yet QUALITY 6 requires a mined/used-by source with URL/path and exact anchor, `verified-at` plus what was checked, and only its listed cadences/date (`QUALITY.md:17-23`). This is a decisive false-clean **if interpreted as Criterion-6 compliance**.

This is a documented scoped limitation, not code/spec divergence or failure of the narrow registered acceptance: v1 tests key presence/date prefix and accepts any `<N>d`, with unscheduled/root-parent findings info-only (`round25-claims.md:29-40`). The build critic's semantic attacks are borne out (`build/CriticClaim1.md:9-34`), but the integrated entry explicitly says it is a key/value-shape screen, not Criterion 6, and names source-row, checked-what, command-only, and header-prose false-cleans (`metadata-screen-r25.md:69-83`). Lesson M10 and M4 preserve that boundary (`round-25.md:40,46`). Pre-r24 legacy entries are not Criterion-6 violations because the bar applies to entries admitted from r24 (`QUALITY.md:17`; `metadata-screen-r25.md:76-78`).

SCORECARD's C1 verdict is correctly qualified **improved (syntactic screen, not full QUALITY 6)**, with operability score unchanged 3→3 (`SCORECARD.md:1329,1341-1345`); LOG likewise calls it a syntactic screen, not semantic compliance (`LOG.md:840-848`). Do not promote the 25/28 count or `METADATA_COMPLETE` to a Criterion-6 pass.

Smallest safe correction: the e93 gate/count needs no C1 scope expansion; retain the existing qualification. Treat 0fc as a packaging failure, d8 as gate-only/incomplete, and e93 as the authoritative full pin. Any future Criterion-6 claim needs separately registered semantic checks/negative tests for source-row identity/anchor, checked-what, allowed cadence, and prose lookalikes.

Installs: none.
VERDICT: Advisory — operability improved only on the corrected final pin; 0fc failed C1 delivery, while the documented false-cleans bar any broader Criterion-6 compliance claim.