# R59Scout30 — bounded offline data walk

## Observed evidence

- The requested frozen `corpus/evidence/round59/claims.md` is absent: direct read failed and the round-59 evidence directory listing exposes `census-start.txt` and `controls/c1-before.txt`, not claims.md. Therefore round-59 claim-to-source mapping cannot be made from frozen claim text.
- `corpus/evidence/round58/claims.md` provides historical context only: its C1 is an operability battery for `tools/build-spans.py` and C2 adds a sourced knowledge entry using pinned builder/capture tools. It explicitly limits its claims to tested surfaces and states no external fetch. Do not impute this contract to round 59.
- `corpus/SOURCES.md` rows 83–85 record three duplicate-URL census hits with materially different statuses/scopes: S073 corrects S070's anchor label while retaining its sha256sum semantics; S074 is rejected as a duplicate proposal to S059 for Python digest-input semantics; S075 is a distinct `mktemp` source for safe creation, explicitly not uniqueness or hostile-path guarantees. Thus URL collision alone is not a substantive duplication finding.
- `corpus/SOURCES.md` row 143 describes S133 as a tier-B evidence-centre mirror carrier for the 2021 guideline's identity/title/edition, not as an origin or broader normative proof. Nearby source-registry conventions separate carrier reliability and claim scope.
- Search-log line 293 in `corpus/SOURCES.md` records the installed-manual-only Round 41 inquiry about `mktemp` and `sed`; it says L0 fetch-scope question `8d77e6c1` remained unanswered, and no URL was fetched. This supports an offline-only boundary, not an answer to whether future external fetches are permitted.

## Bounded relevance / inference

[INFERENCE] For operability (the stated low-scored axis), available prior evidence suggests separating builder behavior demonstrated by a pinned local battery from generalized security claims. The round-58 C1 predicate, for example, explicitly limits itself to listed hazard classes and does not claim broader race or size guarantees. Round-59 evidence presently visible does not establish equivalent coverage or a verdict.

The census duplicate-URL observations warrant semantic comparison by source ID/scope, not automatic deduplication. In particular S073 is a correction and S074 an explicitly rejected proposal, while S075 contributes a different tool contract despite sharing a coreutils manual URL with S073.

## Remaining unknowns

- The intended location/content of frozen round-59 claims and its claim/source bindings.
- Full round-59 capture inventory and whether its controls support positive verdict-path calibration.
- Whether any other duplicate URL pair shares substantive scope; URL match alone cannot resolve this.
- The disposition of L0 question `8d77e6c1`; no external fetch was attempted.