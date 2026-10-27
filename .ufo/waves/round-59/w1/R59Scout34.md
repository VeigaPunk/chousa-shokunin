# R59Scout34 — bounded offline data walk

## Scope / evidence status

Read the round-59 wave spec and dispatch record, round-59 evidence directory, round-58 frozen claims and receipts, round-58 closure spot-check, and the lane source registry. No external fetches, tool installs, counter executions, or source/claim edits. The mandated `corpus/evidence/round59/claims.md` was not found at that path; I do not claim to have read its frozen assertions. Evidence below is limited to files read and their recorded contents.

## Observed

- `.ufo/waves/round-59/w1-spec.json` identifies axes operability, depth, calibration and the milestone as positive verdict-path calibration plus offline source reconnaissance. Dispatch JSON records 66 spawned tasks. These are artifact facts, not an evaluation of their work.
- The round-59 evidence directory exposes `census-start.txt` and `controls/c1-before.txt`; no positive/built after receipt appeared in the directory listing. Census start records exit 0 and five cross-scope duplicate-URL warnings for S051, S053, S073, S074, S075.
- `c1-before.txt` provides a concrete operability defect receipt: `FOREIGN` deleted a foreign span file; symlink output/cache were accepted; FIFO/device and oversized raw legs failed for reasons other than the required refusal categories; `MANY_QUOTES` was accepted. The summary is `OK=4/4 REFUSE=0/7 ... C1=FAIL`, exit 1. This is a baseline receipt, not evidence of the later counter state.
- `corpus/evidence/round58/claims.md` froze C1 operability and C2 depth. The C1 claim explicitly bounds itself to a fixture battery, while C2 claims an entry grounded in S101’s captured document and exact quote bindings. The round-58 closure (`corpus/lessons/round-58-verifier-spotcheck.md`, lines 15–17, 34–38) independently reports both claims unprovable: C1 compared uppercase `=PASS` against lowercase refusal tokens; C2’s span-start offsets could not satisfy both occurrence-offset binding and byte-identical rebuild. It routes next round to freeze positive controls that exercise the exact final predicate, repair those defects, and preserve reachable after receipts.
- `corpus/SOURCES.md` lines 141–143 describe S131–S133, mined on 2026-10-27 and used by `normative-reference-chain-china-r57.md`: S131 is a tier-B association repost of the 2019 notice; S132 is a tier-B association repost of the 2021 notice; S133 is a tier-B evidence-centre mirror of the 2021 guideline attachment. Their scopes concern identity/wording and the registry gives capture names, anchors and hashes/lengths. This is useful offline source-chain context, but registry descriptions alone do not independently re-open or validate capture bytes.
- Round-58 closure lines 23–27 records a separate source-boundary example: S101’s committed document supports only the document’s own statement about `[文献类型标识/载体类型标识]`; present status/legal force was rejected absent approved fetch scope and current authority. It also records the quote-length/location check and unchanged census warnings.

## Bounded relevance / inference

The most directly relevant calibration lesson is operational: a control called positive is meaningful only if it reaches the same final predicate and evidence-binding path as the target; baseline refusal outputs or helper-level success do not establish that. The round-58 closure records specific counter contradictions and requires positive controls plus reachable after receipts, while the round-59 visible C1 receipt remains a failing before-state. [INFERENCE] A round-59 verdict should therefore be withheld until exact positive and falsifying receipts are available and checked against the frozen predicate; this walk did not run them.

For depth/reconnaissance, the S131–S133 chain is traceable as lane-held descriptions with explicit carrier tiers and limited scopes. It supports investigating those captured sources offline, not upgrading their authority or asserting current legal/standard status. Duplicate URL warnings are evidence of repeated URLs across scopes, not proof of duplicate-source error.

## Unknowns

- Whether the frozen round-59 claims are stored elsewhere; the required path was unavailable.
- Contents/results of any round-59 positive controls, after counters, or later source captures; none were present in the inspected round-59 evidence listing.
- Whether S131–S133 captures’ bytes and quote offsets satisfy the relevant predicates; not re-opened here.
- Whether the five cross-scope duplicate-URL warnings are intentional reuse or defects.

## Report trailer

Relative to lane root: `.ufo/waves/round-59/w1/R59Scout34.md`
