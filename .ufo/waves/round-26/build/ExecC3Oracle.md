# ExecC3Oracle — round 26 advisory

## Files and behavior
- Private clone base observed: `f361d12e44687841e30ec35710ddb366c6f795e0`; clone: `/tmp/chousa-r26-ExecC3Oracle-3`.
- Added `/tmp/chousa-r26-ExecC3Oracle-3/corpus/evidence/round26-registry-oracle.py` (SHA-256 `6b2d135c01a8f41b914fb248af35567828336a1a69190560c5df4a07b40f1d78`). It applies the L1 ID/token and exact root-relative used-by rules, parses contract-valid pipe tables literally, retains first duplicate IDs, and parses fence-aware header values/continuations (`:12-18`, `:21-61`, `:64-144`).
- Added `/tmp/chousa-r26-ExecC3Oracle-3/corpus/evidence/round26-registry-differential.sh` (SHA-256 `852a764870f71e7247005f2b91d6864cbe0ba6527098f2c35536466117e676e9`). It compares the base-frozen five, all 29 entries, and 14 generated valid adversarial entries; it guards suite presence and 5/29/14 counts, rejects empty oracle results, gate rc>1, oracle rc!=0, and non-exact output entries (`:31-57`, `:97-165`, `:174-265`). Optional first argument selects the gate tree.
- Patch: `/tmp/chousa-r26-ExecC3Oracle-3/r26-ExecC3Oracle-3.patch`, SHA-256 `0ca86d18a313a71785159bc4d841bc7868c01816d99a363dc7730898cb75bcc9`.

## Evidence and results
- The registered C3 spec is `corpus/evidence/round26-claims.md:90-105`. L1's later addendum supersedes conflicting v1 details: IDs are `S` + 3-or-more digits with ASCII alnum/underscore boundaries (`S0001` valid, `xS001` not); `used-by` must equal the entry's root-relative path after trimming comma tokens and normalizing leading `./` only. The oracle and valid fixtures follow that addendum.
- **Pre-run scope correction for the corrected differential (not a response to observed gate behavior):** `CORPUS.md:89` says “No `|` inside any cell.” The requested escaped-pipe cell `escaped\|pipe` is outside supported registry grammar, so it is excluded from the core differential. The valid core table uses `pipe-token` (`round26-registry-differential.sh:97-129`). A separate out-of-contract registry/entry is retained only in scratch generation and never compared (`:150-164`). Oracle table parsing now uses literal splitting per the contract (`round26-registry-oracle.py:21-26`).
- Earlier run command: `bash /tmp/chousa-r26-ExecC3Oracle-3/corpus/evidence/round26-registry-differential.sh /tmp/chousa-r26-ExecC3Registry-3`. Recorded output was `r24plus 5/5`, `pop29 5/29`, `adversarial 8/14`, `REGISTRY_DIFF_AGREE=18/48`, exit 1. **Invalid, not a gate verdict:** this run preceded the comparator-regex fix and the contract scope correction; its `finding_re` used doubled `\\b`/`\\s` escapes, so it failed to collect finding lines. Its escaped-pipe fixture was outside the supported grammar and is no evidence about gate behavior. The current comparator is `round26-registry-differential.sh:175-181`; no post-correction run was made.
- Oracle predictions for the five frozen entries with the base registry: `citation-chain-fidelity-r24.md=[]` (header `:3`; rows `S003/S005` in `corpus/SOURCES.md:13,15`); `claim-support-states-r24.md=[]` (header `:3`; `S006/S007` at `:16-17`); `contextual-source-admission-r24.md=[]` (header `:2`; `S002-S004` at `:12-14`); `json-delimiter-r24.md=[]` (header `:3`; `S001/S013` at `:11,23`); `metadata-screen-r25.md=[]` (header `:3`; `S029/S033` at `:39,43`). These empty sets are inferred from the implementation plus the cited header/registry rows; per-entry JSON was cleaned from the earlier run.

## Risks and blockers
- The intentional broken-gate-copy demonstration was not run. L1 instructed finalization without further test/build/formatter runs; rerun the corrected core differential and a deliberately broken gate copy after integration. Do not treat the earlier 18/48 output as calibrated evidence.
- No tools installed or updated.

VERDICT: Scope-corrected oracle and differential artifacts are present; five-entry base prediction is clean, but corrected differential and broken-copy behavior remain unverified.

## Recovery preservation of late seat revision (2026-10-21)

The checkpoint report above is retained byte-for-byte. The original seat later
revised its uncommitted report in place. Recovery preserves that complete late
revision below instead of replacing the filed checkpoint or discarding evidence.
This addendum is evidence, not a new seat or a replacement identity.

# ExecC3Oracle — round 26 advisory

## Files and behavior
- Private clone base observed: `f361d12e44687841e30ec35710ddb366c6f795e0`; clone: `/tmp/chousa-r26-ExecC3Oracle-3`.
- Added `/tmp/chousa-r26-ExecC3Oracle-3/corpus/evidence/round26-registry-oracle.py` (SHA-256 `dc40700e83ce71c9e5c451bbada1fc5e6acf7bd6ee5911420a12f8e2a04d8969`). It uses C-locale ASCII-six whitespace, literal single-outer-pipe splitting, all-leading-`./` removal only, outside-root `META_SOURCE_USEDBY_MISSING` semantics, and the unchanged standalone-ID regex; finding lists retain per-token multiplicity (`:12-18`, `:22-31`, `:33-65`, `:70-153`).
- Added `/tmp/chousa-r26-ExecC3Oracle-3/corpus/evidence/round26-registry-differential.sh` (SHA-256 `3f2133b1748fed3c84474ff9a8ed0ebd197fb967427f1a8807f5bef7619e9429`). The original 14 valid core fixtures stay unchanged; it adds a 7-entry edge suite and a 1-entry outside-root suite, for fixed populations 5/29/14/7/1 (total 56), exact output entries, and finding-multiplicity comparison (`:31-57`, `:97-165`, `:167-239`, `:247-337`).
- Patch: `/tmp/chousa-r26-ExecC3Oracle-3/r26-ExecC3Oracle-3.patch`, SHA-256 `c45cd301c0b77739b4c14589f35ceebbe709a5b4ec33db143922813d1c605156`.

## Evidence and results
- The registered C3 spec is `corpus/evidence/round26-claims.md:90-105`. L1's later addendum supersedes conflicting v1 details: IDs are `S` + 3-or-more digits with ASCII alnum/underscore boundaries (`S0001` valid, `xS001` not); `used-by` must equal the root-relative path after trimming comma tokens and removing every leading `./` only.
- **Pre-run scope correction for the corrected differential:** `CORPUS.md:89` forbids `|` inside cells. The requested `escaped\|pipe` case is outside supported grammar; it remains as a separate scratch-only registry/entry and is never compared. Core cells use literal `pipe-token` (`round26-registry-differential.sh:97-129`, `:150-164`); this is contract scoping, not a gate-driven oracle adjustment.
- Falsifier inputs prompted rule alignment: `FRegistryIdBoundary.md:30-46,76-82` reports the terminal-ID occurrence-cut defect; the oracle keeps its ASCII-boundary regex and now retains token multiplicity (`round26-registry-oracle.py:13,126-153`; driver compares sorted finding lists at `round26-registry-differential.sh:317-329`). `FRegistryDuplicateId.md:89,95-109` identifies Unicode trimming, repeated outer-pipe trimming and second-separator divergence; the oracle uses ASCII six, removes at most one pipe per side, and skips later separator rows (`:12-31`, `:51-65`). `FRegistryBareVerified.md:18-33` motivates ASCII whitespace for metadata/fence/date parsing (`:16-18`, `:79-113`, `:148-153`). `FRegistrySameBasename.md:93-101` motivates repeated `./` removal and treating out-of-root entries as lacking an authorizing path (`:116-153`).
- Added edge cases: terminal valid ID after glued IDs; repeated `./`; ASCII VT/FF date-only versus Unicode NBSP tail/prefix; doubled-pipe row; second separator before a valid row; and one outside-root mined-source entry. The fixed counts are guarded in `round26-registry-differential.sh:247-337`.
- Earlier run command: `bash /tmp/chousa-r26-ExecC3Oracle-3/corpus/evidence/round26-registry-differential.sh /tmp/chousa-r26-ExecC3Registry-3`. Its recorded `r24plus 5/5`, `pop29 5/29`, `adversarial 8/14`, `REGISTRY_DIFF_AGREE=18/48`, exit 1 is **invalid**, because it used the doubled-escape comparator and the out-of-contract cell. No post-tightening run was made; it is not evidence about the gate.
- Oracle predictions for the five base-registry entries remain `[]` each: `citation-chain-fidelity-r24.md`, `claim-support-states-r24.md`, `contextual-source-admission-r24.md`, `json-delimiter-r24.md`, `metadata-screen-r25.md`. Inferred from their source headers and base rows at `corpus/SOURCES.md:11-17,23,39,43`; the prior per-entry JSON was cleaned from temporary storage.

## Risks and blockers
- No current differential or broken-gate-copy run was made; L1 explicitly prohibited further test runs. Do not report a gate pass or calibrated result until integration reruns the corrected driver.
- No tools installed or updated.

VERDICT: Oracle and differential are tightened against the four reported falsifiers; no corrected-run or broken-copy result is claimed.