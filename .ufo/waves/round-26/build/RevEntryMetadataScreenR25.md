# Freshness re-verification — `metadata-screen-r25.md`

- Reviewed `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/metadata-screen-r25.md` against QUALITY criteria 2, 7, 8, 13 and the cited artifacts. No installs.
- Recheck clone: `/tmp/chousa-r26-RevEntryMetadataScreenR25-3`; observed base `f361d12e44687841e30ec35710ddb366c6f795e0` (`git rev-parse HEAD`).

## Recheck commands

- cwd clone root; `bash tools/research-gate.sh --selftest` → exit 0; `RESEARCH_GATE_SELFTEST: PASS (161 cases, 0 skipped)`. Observed all cases 137–161, including the metadata controls.
- cwd clone root; `bash corpus/evidence/round25-meta-differential.sh` → exit 0; `AGREE=54/54 (fixtures=27, modes normal+strict)`.
- Root context: the selftest takes no research-root argument. The differential's fixture checks invoke the gate with `--root .`; its documented cwd is lane root. The entry also states the lane-root layout at lines 127–130, so no fleet-root substitution applies to these two commands.

## Source and claim checks

- `corpus/SOURCES.md:39`: S029 is tier A, mined, opened 2026-10-21, and `used-by` includes this entry; anchor is Chapter IV §IV.1. Reopened https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv (access 2026-10-21): §IV.1 still contains verbatim “All Cochrane reviews should be assessed periodically to determine whether an update is needed.” This supports periodic assessment, not a prescribed metadata schedule. The schedule is labelled an inference in entry lines 20–27 and 87–93.
- `corpus/SOURCES.md:43`: S033 is tier A, mined, opened 2026-10-21, and `used-by` includes this entry; its scopes/anchors identify §3.1 derivation and §3.2 entity lifetime, not verification policy. Reopened https://www.w3.org/TR/2013/REC-prov-o-20130430/ (access 2026-10-21): §3.1 describes `prov:wasDerivedFrom` as a derivation relation; §3.2 says “The properties prov:generatedAtTime and prov:invalidatedAtTime can be used to bound the starting and ending moments of an Entity's existence.” The cited terms and entity-lifetime teaching remain present. Entry lines 24–27, 96–99, and 124–125 correctly label mapping these facts to `source:` / `verified-at:` as lane inference, not PROV-O verification semantics.
- The registered result matches its evidence: `round25-measure-before.log:3–4` records the absent mode (`verify-metadata rc=2`); `round25-claims.md:12–15` states that base result. `round25-measure-after.log:3,8–9,37–39` records exit 1, `METADATA_COMPLETE=25/28`, and exactly the three named `META_RECHECK_ABSENT` entries. `lessons/round-24.md:24` lists those same legacy headers under M-13.
- `round25-final-measure.log:37–39,52–56` confirms unchanged 25/28 population result and 161-case pass. `round25-final-differential.log:1–3` records 54/54 and exit 0. `round25-final-holds.log:1–14` records the holds battery passing. The final-reader correction at entry lines 103–112 appropriately limits the 27-fixture differential claim; selftest supplies the refusal-branch controls.
- QUALITY 7/8: cited S029/S033 row scopes cover only the source propositions stated; the entry distinguishes source facts from its inferences and does not claim either source establishes the header convention or truth of the lane’s claims.
- QUALITY 13: entry lines 127–130 state the required cwd/layout. `recheck: 90d` is an allowed cadence; both commands reproduced from the private clone.

## Findings, residual risk, gaps

- Findings: none. No stale or false claim found.
- Residual risk: web-source freshness is observed as of 2026-10-21 only. The sources do not prescribe this metadata header; the entry correctly treats the mapping as local inference.
- Verification gap: no LSP device is mounted (`xd://lsp` returned “No such tool”); this was a source/evidence review, not a semantic caller/definition audit.

VERDICT: re-verifies — commands pass at the preregistered base, cited S029/S033 anchors remain present, and the entry’s claims stay within their cited scopes.