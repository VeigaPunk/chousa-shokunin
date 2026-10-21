# Round 25 residual final-sources review

Reviewer: `ChousaR25.R25FinalSources`. Same round / attempt 2; advisory lane worker, not an outside admission reviewer or replacement for a dead seat. Review date: 2026-10-21.

Axes: source-quote fidelity and scope; immutable provenance; mutable-cell transition accounting; consistency of current prose with its corrections. This review does not redefine the round's axes, routes, claims, or acceptance criteria.

## Findings, by severity

### P2 — The current study path retains the stronger teaching that the new rows expressly withdraw

Location: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md:60-63`.

The diff retargets this current path to S029/S032/S033, but leaves its explanation as “schedule the currency check (a recheck is a periodic, recorded act)” and “expect early staleness for a real minority of findings”. S029 at line 39 expressly says its sentence does **not** prescribe a recorded schedule; S032 at line 42 carefully distinguishes a potential update signal from an actual update. The path does not label the stronger operationalization as a lane inference, unlike `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/metadata-screen-r25.md:85-99`.

Evidence: the Cochrane reopening below supports periodic assessment, not that recorded-schedule requirement; the newly corrected S032 teaching is narrower than the path's unqualified staleness restatement. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-25.md:204-207` says those stronger implications were removed. This current path is not merely an immutable historical row: its source sequence was actively changed in the reviewed diff. It therefore leaves the source-precision correction incomplete at a current learner-facing consumer. The applicable admission distinction is stated in `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/QUALITY.md:24-27`.

Recommendation: qualify the path's schedule as the lane's own inference/convention and describe potential update signals rather than treating them as established staleness. An explicit path-specific correction can do this without rewriting old immutable registry cells or dated search history.

No critical/high finding in this bounded source review.

## Evidence and supported checks

### Actual checkpoint comparison and immutability

Read-only commands inspected the actual scoped diff against `e93ac711`, not just reports:

```sh
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --no-ext-diff --no-textconv --unified=5 e93ac711 -- /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/metadata-screen-r25.md /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-25.md
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/chousa-shokunin show e93ac711:corpus/SOURCES.md
```

The registry diff changes only `status` and `used-by` on existing S019/S020 and appends S029-S033. The existing rows' `id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, and `opened` cells are unchanged; **no old `recheck` cell changes**. S021-S028 are unchanged in full. No silent immutable-cell rewrite was found relative to this checkpoint. This is the precise interval reviewed, not a claim about earlier history.

Observed transitions:

| Row | status old → new | used-by old → new | recheck |
|---|---|---|---|
| S019 | mined → queued | `corpus/knowledge/metadata-screen-r25.md` → `—` | on-release, unchanged |
| S020 | mined → queued | `corpus/knowledge/metadata-screen-r25.md` → `—` | 365d, unchanged |

The relative strings above are literal registry cell contents. Both transitions are logged at `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-25.md:186-191`; S020's “likewise” refers to the same old used-by value shown for S019. The matching registry explanations are at `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md:126-135`.

All five appended rows begin their teaching with the required `supersedes S… —` linkage. S029/S033 are mined and both name the existing metadata entry; its current header cites those new IDs. S030/S031/S032 remain queued with no used-by claim. The source-cell allowance and old→new requirement are in `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md:112-118`.

### S029 — Cochrane reopening agrees with the narrowed row

Opened [Chapter IV: Updating a review](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv). The returned chapter identifies Cumpston/Flemyng, chapter last updated August 2023, Handbook version 6.5 (2024).

Under **IV.1 Introduction**, the exact sentence is:

> All Cochrane reviews should be assessed periodically to determine whether an update is needed.

This matches `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-25.md:195` and grounds S029's scoped periodic-assessment teaching. The Key Points contain a similar sentence without its initial “All”; the correction to the exact locator is justified. Neither the quoted sentence nor the row establishes a required recorded schedule for arbitrary research records. The metadata entry explicitly identifies its scheduled-recheck extension as a lane inference at lines 91-92.

### S033 — W3C reopening agrees with entity lifetime, not verification validity

Opened [PROV-O Recommendation, 2013-04-30](https://www.w3.org/TR/2013/REC-prov-o-20130430/). The default reader returned only specification metadata, so it was insufficient for a quote check. Reopened the same URL as raw HTML and inspected **§3.1 Starting Point Terms** and **§3.2 Expanded Terms**.

§3.1 describes provenance chains using `prov:wasDerivedFrom`. The §3.2 entity-lifetime paragraph contains, after removing presentation markup:

> The properties prov:generatedAtTime and prov:invalidatedAtTime can be used to bound the starting and ending moments of an Entity's existence.

This is the exact sentence at `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-25.md:199`. Its surrounding example concerns a painting before creation and after destruction. S033's restriction to entity-lifetime facts is supported; the passage does not define verification time or truth-validity. The explicit limitation/inference at `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/metadata-screen-r25.md:96-99,124-125` preserves that distinction. Both sampled Gate quotations are within the 25-word cap.

### S025 — Sample rejection remains justified for its stated scope

Opened [RFC 9111, HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111), including **§4.2 Freshness**. Its exact equation is `response_is_fresh = (freshness_lifetime > current_age)`, matching `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-25.md:74`. The section defines cached-response lifetime and age and expressly restricts freshness to cache operation.

Thus `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md:35` appropriately rejects the RFC as authority for general research-record validity while retaining its possible use as a labelled analogy paired with a relevant method source. This does not reject the RFC's authority within HTTP caching.

### Consumers, census, and historical wording

Literal reference tracing covered the corpus and the lane's SKILL/LOG/SCORECARD records. The current metadata header and `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/README.md:58` point to the corrected source IDs. `/home/vgpnk/Projects/shokunin/chousa-shokunin/LOG.md:920-925` and `/home/vgpnk/Projects/shokunin/chousa-shokunin/SCORECARD.md:1413-1414` record the new grounding. Earlier Gate/search-log uses of S019/S020 and the original 18→28 census are explicitly superseded historical integration records, not additional findings requiring history to be rewritten.

The existing receipt `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round25-final-census.log:1-9` reports 33 rows; tiers A=27/B=1/C=5; statuses mined=10/queued=19/rejected=4; malformed=0; empty duplicate/enum/missing-used-by lists; exit 0. Those totals are consistent with the displayed registry and the lesson's round-base 18→33 / added A13/B0/C2 statement. The checkpoint-to-worktree addition is five rows, not fifteen. This review **read** that receipt; it did not rerun its command.

The quota-based historical rejection-sweep rationale is expressly qualified as a bounded convenience sample, not saturation, at `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md:102-108` and `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-25.md:170-173`. No new search or row-count-based expansion verdict is claimed by the correction.

## Advisory recommendation

The sampled source quotes/scopes, S025 rejection, immutable-cell preservation, and mutable-cell transition logs are supported. One current-prose inconsistency remains at the study path above; recommend reconciling it before describing source precision as fully corrected. This is a recommendation only, not round admission, a trend judgment, or an independent outside spot-check closure.

## Residual risk and verification gaps

- Only S029/S033 and the requested S025 rejection were independently reopened here. S030/S031/S032 supersession structure and logged scope were inspected, but their primary pages were not independently reopened in this review.
- The `lsp` device is unavailable in this session: device discovery returned `No such tool: xd://lsp` and no mounted LSP route. References/definition/diagnostics could not be requested. Text searches are literal consumer discovery, not semantic-reference proof.
- This is a working-tree review against `e93ac711`, not verification of a subsequently landed/pushed revision. Concurrent additions to the metadata note and lesson were encountered and read; their historical/final-reader qualifications are not misreported as missing.
- No builds, lint, tests, census reruns, mutations, new runtime, live-target probing, or delegation were performed. Canonical-runtime uniqueness, same-identity rerouting, and `resume_continuity_v1` failed-preflight zero-mutation behavior were not exercised or asserted by this source-only assignment.
- No tools were installed or updated. No production, git/jj, fleet, sibling, or host writes were made; the review report is the sole filesystem output.

## Post-review disposition — P2 resolved in current prose

After the integration owner's correction notice, re-read only `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md:60-64`. The current path now distinguishes periodic currency assessment, measured update signals **“not actual updates”**, and derivation/entity-time properties. It explicitly states that scheduling and recording the next verification is the lane's inference, not a Cochrane or PROV requirement, and retains S025 only as a rejected HTTP analogy.

This resolves the P2 finding above. The original finding and recommendation remain as review history, not current unresolved debt. **Updated advisory recommendation: no actionable finding remains in the assigned final-source scope.** The supported quote/scope, immutable-cell, and transition-log checks remain as recorded; all residual-risk and verification-gap qualifications still apply. No suite or other check was run for this disposition.
