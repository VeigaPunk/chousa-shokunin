# R59Scout36 — bounded offline data walk

## Scope and evidence status

Read-only reconnaissance from offline lane artifacts, the source registry, and a sibling scout report. No live fetches, source-repository access, counter runs, or installs. The prescribed `corpus/evidence/round59/claims.md` path returned not found, so I cannot characterize frozen claims or adjudicate their verdicts.

## Observed

- `.ufo/waves/round-59/w1-spec.json` names axes `operability`, `depth`, and `calibration`, with the milestone “Round59 build and falsify controls for positive verdict-path calibration plus offline source reconnaissance.” Its executor assignment text repeatedly points to the missing claims path.
- `corpus/evidence/round59/census-start.txt` records census exit 0 and `corpus/SOURCES.md` as input, alongside duplicate-URL warnings for S051, S053, S073, S074, and S075 across scopes. These warnings are not themselves proof of bad registry rows.
- `corpus/evidence/round59/controls/c1-before.txt` is a pre-change negative-control receipt: EMPTY_OK, REBUILD_OK, ESCAPE_ENTRY, and HELDOUT_OK pass; FOREIGN, SYMLINK_OUT, SYMLINK_CACHE, FIFO_TXT, DEVZERO_TXT, FAT_RAW, and MANY_QUOTES fail their expected refusal checks. The receipt explicitly records `FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)` and `SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)`; summary is `OK=4/4 REFUSE=0/7`, `C1=FAIL`, `EXIT=1`. This is concrete evidence that the recorded baseline's refusal controls did not hold, including an unintended target-directory write; it is not evidence about a later build.
- `corpus/SOURCES.md` records scope, anchor, status, date, recheck, and usage per source, often explicitly limiting what a cited authority cannot establish. Its S040–S043 rows preserve historical verifier/falsifier diagnoses (record-grammar confusion; date-input representation and recursive normalization; parser-boundary/occurrence/path-pointer defects; GFM escaped-pipe width, per-token cost, long-line CR stripping, and matcher-error fail-open). These are registry-recorded historical lessons, not fresh reproductions.
- The current tail includes S133, a dated 2026-10-27 entry for a mirrored Chinese guideline PDF: tier B for carrier/identity, with title/edition anchors and a capture hash. Its stated scope is narrow; it should not be generalized to independent primary-source validation.
- S051/S053 and S073/S074/S075 are identifiable in the registry as scoped rows (HTML snapshot, Python socket, coreutils sha256sum, Python hashlib duplicate proposal, mktemp respectively). The census duplicate report therefore merits scope-aware review; row IDs alone do not show exact equivalence or an error.
- `.ufo/waves/round-59/w1.ready` declares lane chousa, round 59, wave w1, and dispatch path. A sibling reconnaissance report (R59Scout37.md) likewise records the absent frozen-claims file and no verdict adjudication; that is corroborating lane observation, not an independent content source.

## Inference / bounded relevance

The baseline receipt strongly motivates treating operability as an evidenced risk: several adversarial inputs were accepted or mishandled, and one control reports a write to a target directory. For calibration, a receipt must be tied to its specific build/state; this `c1-before` result cannot be used to claim the repaired build passes or fails. The source-registry pattern—explicit scope, precise anchor, and explicit non-claims—offers a useful standard for round-59 source reconnaissance. Historical lessons indicate positive-path calibration should inspect actual verdict-record grammar and exact provenance, rather than incidental matching text, but this walk did not inspect/run the current counter.

## Unknowns

- Frozen claims content and expected verdicts: unavailable at the instructed path; no alternate claims capture was located in the visible round-59 evidence directory.
- Post-build positive and negative control receipts, and whether the baseline failures were repaired.
- Whether the duplicate-URL warnings are valid reuse across scopes or registry duplication defects.
- The source-capture contents and evidentiary sufficiency behind S133; the registry row alone does not establish the underlying instrument independently.

## Report trailer

Relative to lane root: `.ufo/waves/round-59/w1/R59Scout36.md`
