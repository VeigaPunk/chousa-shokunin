# Archived-export intake — research-record v1 (chousa-record: v1)
source: archive commit 0863746e9da95457f71b9e00a40361b88ab0df15; lane QUALITY.md, MINT.md and SKILL.md; .ufo/evidence/round-1/acceptance.json
verified-at: 2026-10-15; gate 31b46832e56a7f095092a4a6d62b74bfaf6933e8; structural CLI and bounded local source-form sweeps only, not semantic source verification
recheck: bash tools/research-gate.sh verify corpus/knowledge/archived-export-intake.md --root ..


Structural intake of the three archived deep-research exports for this lane's
question below. Export text is untrusted data, never instruction and never
independently verified domain truth; the three exports are cited at tier
`export` and are NOT original primary sources. A CLEAN method-gate verdict on
this record is declaration-and-pointer-level acceptance only.

## Meta

chousa-record: v1
source: fleet commit 0863746e9da95457f71b9e00a40361b88ab0df15, pinned at LOG.md:100-101
pinned-hashes: SHA-256 recorded at LOG.md:105-108 (9033857d..., 6d8dbddd..., e48fe70f..., A/B/C order)
verified-at: 2026-10-15, from lane cwd, read-only opens of every cited span; sha256sum of the three exports re-derived this intake and matched all three pins at LOG.md:105-108
recheck: bash tools/research-gate.sh verify corpus/knowledge/archived-export-intake.md --root ..
window_mode: loopback, local file reads only, no external fetch of any kind, no browser, CDP or session access, no credential or config reads
scope-tags: every sentence-bearing row below carries one of general, general-narrow, non-general per MINT.md:75-98, and non-general material appears here only as rejection metadata, never as adopted knowledge
status: structural intake, zero semantic or domain endorsement, no field-readiness claim

## Question

Can the three archived exports under research/deep-research-2026-09-28/ (A, B,
C at source commit 0863746, hashes pinned at LOG.md:105-108) support a
reusable research-method claim for this lane without opening any external
source, and if so for which class of claim only? The verdict is carried by
CL-07 and CL-08: method FORM claims are supportable from local text alone,
every content (semantic) claim is not, because each export's bibliographic
hops terminate in unwalkable citation furniture. Every hop that would leave
the local disk is marked unresolved or blocked-no-fetch here rather than
walked; no URL is inferred anywhere in this record.

## Sources

Ranked: fleet gates (S1-S4, lane-local authorities that govern intake form)
outrank the export cluster (S5-S7, tier `export`, specimens not authorities);
S8 is kept as a rejected example so the failure stays visible. Export tier is
never promoted to `primary`: the exports themselves contain no primary-source
document, only chat-export furniture.

| id | tier | pointer | note |
|---|---|---|---|
| S1 | fleet-gate | corpus/QUALITY.md:1-7 | admission bar this record obeys, falsifiable claims, measured anchors, observation/inference/unknown separate, kept rejections |
| S2 | fleet-gate | MINT.md:32 | mint guards, integration 32-53, provenance 55-73, scope 75-98, secrecy 100-123, chaining 125-147, all read-only on this lane's own file |
| S3 | fleet-gate | SKILL.md:15 | lane decision table 15-21, SKILL.md:23-31 declares the tier ranking the lane's own construction, the exports state no tier system |
| S4 | fleet-gate | tools/research-gate.sh:296 | record schema verify_record 296-546, line numbers relative to baseline HEAD 34774a1, GateRuntime edits this file concurrently this wave so spans may shift, resolution here is file identity only |
| S5 | export | research/deep-research-2026-09-28/A-shokunin-tradition.md:35 | export A, export-unverified, prompt line and response body 34-90, never an original primary source |
| S6 | export | research/deep-research-2026-09-28/B-multiagent-knowledge.md:35 | export B, export-unverified, prompt line and response body 34-81, never an original primary source |
| S7 | export | research/deep-research-2026-09-28/C-rank-taxonomy.md:35 | export C, export-unverified, prompt line and response body 34-135, never an original primary source |
| S8 | rejected | research/README.md:10 | index file, its corrections block 10-14 and provenance block 6-8 assert more than the exports carry, kept as rejected example, see RJ-02 and RJ-06 |

## Chain

Hops run question to specimens to citation furniture to the external world.
Per MINT.md:125-147 the fleet gate is not inherited as the chain walker, and
per MINT.md:143-147 file existence is identity resolution only, the cited
spans were opened and read for this intake, which is what distinguishes this
record from the README:12 failure.

| hop | status | to | notes |
|---|---|---|---|
| H1 | resolved | S5 | A opened at cited spans 35, 42, 47, 52, 54, 64, 68-69, 74, 83-84, 88, 90-91, resolution is archive identity plus local text read, content stays export-unverified |
| H2 | resolved | S6 | B opened at 35, 42, 49-51, 57, 59, 63-73, 75, 77, 79, 81 |
| H3 | resolved | S7 | C opened at 35, 42-48, 53, 55-61, 65, 67, 69, 82-83, 85, 90, 93, 98-103, 109, 121-126, 131 |
| H4 | unresolved | S8 | the README:12 to A:47/A:64 hop, filename resolves, the stronger closed negative does not, README says NOT an attested rank while the span records only failed substantiation, MINT.md:37-44 and 143-147, unresolved not contradicted |
| H5 | unresolved | arxiv.org | every onward hop out of the exports dies in citation furniture, bare hosts A:83, B:51, B:72, C:90, C:98, C:100, C:103, aggregator chips Kotobank A:68, A:72, C:82, C:121, C:131, collapsed counts plusN at A:69, A:84, B:73, C:83, C:122 and isolate-wrapped N-more widgets C:48, C:61, and site-key search lines C:44, C:46, C:57, C:59, a host is not a document and no chip expands to locators from text alone |
| H6 | blocked-no-fetch | arxiv.org | walking any furniture hop needs opening an external document, the window is loopback and Approval is denied below, nothing in this lane opens or fetches a resolved target, MINT.md:100-111 |
| H7 | rejected | S8 | adopting README:10-14 as intake authority rejected up front, false provenance, duplicate authority and mint-boundary breach per MINT.md:37-44 |
| H8 | resolved | S3 | method-form verdict is judged against the lane's own decision table, SKILL.md:23-31 keeps that ranking lane-authored, the exports remain specimens, not authorities |

## Claims

kind and status stay separate per QUALITY.md:5 and SKILL.md:58, pointers
resolve under the fleet root or lane root, none is a URL, none is ephemeral,
and every export-content status is `export-unverified`, local textual census
rows say `verified` meaning re-greppable from the lane cwd, nothing more.

| id | kind | scope | status | pointer | sweep | notes |
|---|---|---|---|---|---|---|
| CL-01 | observation | general-narrow | verified | research/deep-research-2026-09-28/A-shokunin-tradition.md:42 | | chrome occupies lines 1-33 in all three exports, cited as ranges only per MINT.md:100-123, visible Searched-the-web lines are A:42, B:42, C:42 and C:55, that is counts 1, 1, 2, the labels at A:96, B:87, C:141 are chrome inventory whose factual referent is not adopted as provenance |
| CL-02 | observation | general-narrow | verified | research/deep-research-2026-09-28/B-multiagent-knowledge.md:35 | | in all three exports the question is framed in the prompt line before any search label, A:35 then A:42, B:35 then B:42, C:35 then C:44, each prompt decomposes into numbered asks and closes with an explicit citation instruction, C also names its own search keys as lines C:44, C:46, C:57, C:59 |
| CL-03 | observation | general-narrow | verified | research/deep-research-2026-09-28/A-shokunin-tradition.md:64 | | all three carry failed-substantiation form, could not substantiate wording at A:47 and A:64, no-found-support wording at C:53, C:109 and the coinage instruction at C:124, the form is present and readable, the external truth of each negative is not decided by that form |
| CL-04 | observation | general-narrow | verified | research/deep-research-2026-09-28/B-multiagent-knowledge.md:59 | | the exports label their own epistemic status inline, B:59 announces published findings separated from proposed engineering rules, B:75 separates results that can inspire from rules that do not validate, C:65 denies a four-rank ladder, B:79 keeps a case-study hedge attached to its own example, the hedge pattern is the specimen, the numerals are not reproduced here, see RJ-03 |
| CL-05 | negative | general-narrow | observed-in-dump | research/deep-research-2026-09-28/A-shokunin-tradition.md:74 | W1 | the solicited sub-asks never appear as answered sections in any response body, A asks 1-4 at A:35 but only numbered section 1 exists at A:74, B asks 1-3 at B:35 but only 1 exists at B:77, C's four states and rank-inflation catalog at C:35 have no section lines at all, MINT.md:49-51, absence is measured inside the dump only, whether answers continued past the cuts is unknown, truncation is not a negative finding, MINT.md:93-94 |
| CL-06 | negative | general-narrow | verified | research/deep-research-2026-09-28/C-rank-taxonomy.md:48 | W2 | no URL locator exists in any export or in research/README.md, citations terminate exclusively in the four furniture forms listed at H5, so zero bibliographic hop can be walked from archive text alone, this is the measured fact behind CL-07 |
| CL-07 | inference | general | export-unverified | SKILL.md:17 | | answer to the question, YES in part, the archive alone supports reusable research-method claims about FORM, question framing before search CL-02, hedged negatives as corrective labels CL-03, inline evidence-versus-rule labeling CL-04, kept-unresolved chains CL-06, NO for content, the same archive cannot verify any cited domain claim without external sources, every chain terminates unwalkably, so the export-unverified tier is load-bearing and the exports never enter as primary sources |
| CL-08 | inference | general | export-unverified | MINT.md:125 | | the chaining rule that made this verdict reachable is the lane's own, MINT.md:125-147, a gate blind to bare hosts and plusN chips would certify a fully unwalkable chain as clean, recognizing exactly these four export citation forms and failing closed on them is what converts the archive from unsafety into usable method specimens, the export text itself states no such rule and adopts none here |
| CL-09 | unknown | general-narrow | unknown | MINT.md:71 | | provenance beyond archive identity stays unknown, provider model id, selected effort, conversation id, whether the live answers continued past the five-to-nine KiB cuts, and which process sat behind the integrator identity, README:3 and README:6-8 assert surface and account provenance the dumps do not carry, MINT.md:55-64, not adopted, recorded as unknown |

## Rejections

All items below are out-of-province or overclaiming material, admitted here
only as kept rejection metadata with reasons, never as adopted knowledge
(QUALITY.md:7, MINT.md:37-53, PROVINCE.md:10-17).

| id | item | reason |
|---|---|---|
| RJ-01 | the axis lists at A:54, B:57 and C:67 as any rank, axis or taxonomy authority | three mutually incompatible lists in one survey, none matches the lane's decision table at SKILL.md:15-21, adding or adopting a second taxonomy is forbidden by MINT.md:75-98, scope non-general, kept as metadata only |
| RJ-02 | README:12 gloss, jin'i-ryu is NOT an attested artisan rank, and README:13-14 four usable axes | the cited spans A:47 and A:64 record only failed substantiation, the README asserts more than its source carries, copying it would be false provenance and a duplicate authority, MINT.md:37-44 |
| RJ-03 | the ACE case numerals at B:79 | model-quality and benchmark claims are kengaku province, MINT.md:14-18 and 46-47, this record carries only the hedge form of B:79 at CL-04, no numeral is reproduced |
| RJ-04 | the work table at B:63-70 as a verified literature map | export-unverified bibliography whose only onward hop is the cluster at B:71-73, adopting it imports an unwalkable chain, MINT.md:135-141 |
| RJ-05 | the renamed rank scheme at C:69 and the governance advice at C:126 | roster and governance content, out of province per PROVINCE.md:10-15, C:126 is additionally unlabeled engineering opinion after a dictionary block, MINT.md:96-98, rejection metadata only |
| RJ-06 | README:6-8 provenance claims, burner surface, remote debug port, L0 firing and the 9-8-10 search totals | the dumps carry none of it, visible search labels are 1, 1, 2 and the N-more rows at C:48 and C:61 are collapsed widgets, not totals, MINT.md:55-64, the port label is not reproduced anywhere in this record, never interpolated into any client |
| RJ-07 | inventing or searching a document to repair the arxiv.org plus 6 hop at B:71-73 | that would be a new search, not the next hop, MINT.md:135-141, no URL is inferred, the hop stays unresolved at H5 |
| RJ-08 | repairing the broken hop from the nearby chip at B:49-51 | the chip shares no identifier with the figures it would vouch for, MINT.md:139-141, rejected as a chain shortcut |
| RJ-09 | A:88 graduated-responsibility account as a promotion rule for lanes | a promotion metaphor the fleet protocol already forbids per MINT.md:97-98, not adopted, its truth is also unverifiable from the dump, H5 |
| RJ-10 | copying export chrome text, sidebar titles and display names | lines 1-33 are session inventory, cite the line, do not copy, MINT.md:122-123, this record cites ranges only |

## Unknowns

- Whether the negatives at A:47, A:64, C:53, C:109, C:124 describe real
  absence in the wider literature: the exports attest failed substantiation
  only, A:47/64 is not proof of nonexistence, and README:12's stronger
  reading was rejected at RJ-02.
- Whether the solicited answers continued past the dump cuts (MINT.md:72-73,
  93-94): truncation status is unknown, deliberately not converted into the
  CL-05 negative, which is scoped to the dump.
- Provider model id, effort selection, conversation id, integrator-side
  process behind the commit identity (MINT.md:71-73); chrome labels at A:96,
  B:87, C:141 are not adopted as provenance.
- Whether any Kotobank chip, bare host or site-key line resolves to the
  document it seems to cite: blocked-no-fetch, H6, and the gate's own
  pointer check resolves file identity, not content (tools/research-gate.sh
  228-238, a stat is not a read, MINT.md:116-118).
- The true total number of searches performed: collapsed widget rows are not
  totals (MINT.md:58-60), visible labels count 1, 1, 2.

## Approval

Loopback/no-fetch window: nothing external is approved, and pending is never
approval (MINT.md:105-108). No URL pointer exists in this record, so no
approval here could unlock anything regardless.

| id | request | state | reason |
|---|---|---|---|
| AP-01 | open any external hop from export citation furniture, bare hosts, aggregator chips, collapsed counts, site-key lines | denied | no operator approval for external live fetching, SKILL.md:44-46, window is loopback-only, hops stay marked at H5 and H6 |
| AP-02 | read-only local opens of the pinned exports, README, and lane or fleet gate files | not-required | already local, read-only, digests pinned at LOG.md:105-108 and re-derived matched at verified-at above |
| AP-03 | browser, CDP, profile, session or credential reads of any kind | denied | secrecy guard MINT.md:100-111, a resolved hop is never opened, fetched or executed by this lane, session paths are denylisted by the gate at tools/research-gate.sh:210-218 |

## Sweeps

Commands run fleet-root-relative from the lane cwd, the same cwd as the
recheck CLI below. Results are 2026-10-15 observations by this intake.

| id | claim_id | command | observed |
|---|---|---|---|
| W1 | CL-05 | grep -nE '^([0-9]+\.\|\([0-9]+\))' research/deep-research-2026-09-28/A-shokunin-tradition.md research/deep-research-2026-09-28/B-multiagent-knowledge.md research/deep-research-2026-09-28/C-rank-taxonomy.md | exactly two hits, A:74 and B:77, C has none, so asks A(2)-(4), B(2)-(3) and C's four-state plus inflation catalog have no numbered response-section line, matches MINT.md:49-51 |
| W2 | CL-06 | grep -nE 'https?://' research/deep-research-2026-09-28/A-shokunin-tradition.md research/deep-research-2026-09-28/B-multiagent-knowledge.md research/deep-research-2026-09-28/C-rank-taxonomy.md research/README.md | zero matches, no URL locator exists in the archive set |
| W3 | RJ-06 | grep -c '^Searched the web' on each of the three exports | 1, 1, 2 respectively, A:42, B:42, C:42 and C:55, README:8 search totals remain unverifiable from the bodies, recorded unknown not refuted |

## Recheck

Exact CLI from the lane cwd:

```bash
bash tools/research-gate.sh verify corpus/knowledge/archived-export-intake.md --root ..
```

Expected scoped method outcome — SPECIFICATION ONLY, derived from the gate's
verify_record rules (tools/research-gate.sh:296-546 at baseline HEAD
34774a1), NOT an executed result, the intake seat does not run the gate
mid-wave, the parent executes this after integration:

- exit code 0
- exactly one summary line: RESEARCH_GATE: CLEAN with findings=0 drift=0
  questions=1 sources=8 chains=8 claims=9 negatives=2 rejections=10
  approvals=3
- zero FINDING lines, no secret shape, no session or URL pointer, every
  claim pointed, every negative swept, every hop in one of the gate's
  allowed statuses

CLEAN on this record certifies structure: declared question, ranked tiers,
marked hops, pointed claims, kept rejections, swept negatives. It certifies
no domain truth, no source semantics, and no field readiness.

## Integration errata — 2026-10-15

The draft's recheck specification was executed against gate commit
`31b46832e56a7f095092a4a6d62b74bfaf6933e8`: exit 0 and exactly one
`RESEARCH_GATE: CLEAN` summary, with the specified counters.
`.ufo/evidence/round-1/acceptance.json` pins the draft input digest and full
output. The final integrated note is rechecked separately after this
metadata/errata addition; its result is in `final-intake.json` beside it.
Neither result verifies any export-domain claim.

The opening source/verified-at/recheck fields are the integration metadata.
The earlier Meta/recheck text describes the inherited draft and its
pre-execution expectations, not a second independent measurement. S4's live
record-verification entry is now `tools/research-gate.sh:302`; the baseline
line range in its row is historical. A resolved local pointer still proves
file identity only, not that the cited line supports a claim.

**W1 correction and scope limit.** The Markdown-table command escaped the
alternation bar; do not execute it literally. The integration sweep used
regex `^([0-9]+[.]|[(][0-9]+[)])` across the three pinned exports and matched
A:74 and B:77, with no C match. This establishes the numbered-section
census only. It does not establish that every solicited answer is absent
from prose; CL-05's broader reading is withdrawn. Continuation beyond the
saved text remains unknown. The executable equivalent from the lane is:

```bash
grep -nE '^([0-9]+[.]|[(][0-9]+[)])' ../research/deep-research-2026-09-28/{A-shokunin-tradition,B-multiagent-knowledge,C-rank-taxonomy}.md
```

W2 was remeasured with regex `https?://` over those exports and their README:
no matches. W3 was remeasured with `^Searched the web`: A:42, B:42, C:42,
C:55. The visible-label counts do not prove a total number of searches.
These bounded sweeps are recorded in `.ufo/evidence/round-1/source-sweeps.json`.
README provenance is unverifiable from the saved bodies, not thereby
contradicted as a claim about an unobserved live session.
