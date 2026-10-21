# Round 25 — a syntactic screen is not a semantic bar (2026-10-21)

Claim base `d730ae4c33989ad9c8535764d4cae77b4db869f6`; pre-registration landed
`b820e4e40ce52deedf53b191140cd7b08ddda929` before implementation. Recovery
attempt 2: attempt 1 had no round-25 commit, uncommitted output, registry or
seat (0 seats). The generic watchdog wording "reuses retained round-25 work"
is not evidence any existed. Reused: round-24 plan, lesson and verifier check;
discarded from attempt 1: nothing existed. The sole integration writer was
ChousaR25Recovery; seats returned reports, five executor drafts in private
clones, and a scribe's private QUALITY draft. No seat wrote production files.

## Spot-check intake

Previous outside check: `round-24-verifier-spotcheck.md`, integrator kaika.
The reviewer/critic details and dispositions are also mapped at
`.ufo/waves/round-25/build/ConnectorSpotcheckMap.md` (D-1–D-11).

| debt / disagreement | disposition in round 25 | evidence / bar |
|---|---|---|
| Concurrent appenders can add a blank line (1/3 runs at 16 writers) | carried, not a claimed fix; independently reproduced 2/6 seeded runs this round, 0/6 empty controls; no pooling of rates | r24 receipt `evidence/json-r24-20261019T213117Z-demo.log:26-29`; r25 `.ufo/waves/round-25/build/ExecAppendRace.md`; QUALITY 2 requires the measured precondition and k/n, not "concurrency safe" |
| Citation-chain recheck needs the fleet root, not a placement-dependent `..` | fixed as an append-only command erratum in `knowledge/citation-chain-fidelity-r24.md`; class flagged by `META_RECHECK_ROOT_PARENT` info, 9 entries; remaining parent-root rechecks carried under criterion 13 | `.ufo/waves/round-25/build/ReviewRecheckRoot.md`: clone `--root ..` → 17 refused hops, exit 1; explicit fleet root → 17/22 CLEAN, exit 0 |
| Lesson template lacks a spot-check slot | criterion 14 appended; this section is its first application, not a retrospective edit to r24 | `grep -qx '## Spot-check intake' lessons/round-24.md` exit 1; round-25 counterpart exit 0 |
| Critic's r24 C2 blocker (the alleged falsifier supported the claim) | already closed by r24 erratum `095b90c`; reviewer ADMIT vs critic REJECT was temporal, not a new disagreement | `knowledge/citation-chain-fidelity-r24.md` existing r24 falsifier erratum; outside check admits after it |
| D-1 score wording; D-2 index gain is not expansion; D-3 mapping count is not semantic calibration | applied: operability score remains 3/10 on the re-derived r1 construct; C2 is freshness only; C3 measures stale restatements, not semantic sufficiency of the old M→criterion map | `evidence/round25-measure-{before,after}.log`; QUALITY 12 |
| D-4 S006 Gate quote omitted enumerators, so was not verbatim | corrected below, append-only; S006 version unchanged | QUALITY 2/4; `.ufo/waves/round-25/build/ReviewSourcesRecheck.md` |
| D-5 root dependency | fixed for the named entry, class remains carried | criterion 13; row above |
| D-6 r24 rejected-sweep stop rationale cites an assignment quota | historical log corrected by a new SOURCES Search-log note; no quota is an epistemic stop condition | SOURCES rule 5; QUALITY 3 (observation/inference/unknown) |
| D-7 report claimed four `[~]` while SHONEN stayed `[ ]` | SHONEN reconciled as `[~]` with pointers, no `[x]` self-attestation | `SHONEN.md`; AXES calibration / QUALITY 9 |
| D-8 outside sample is in a separate verifier file, not r24 Gate | prior outside sample indexed and linked here; r24 Gate left untouched; no retroactive compliance claim | QUALITY 4, new 14; `round-24-verifier-spotcheck.md` is integrator-owned |
| D-9 SOURCES cells narrowed without old→new; D-10 r24 lesson header describes uncommitted pre-landing state | historical deviations named, not rewritten; current rows/changes logged below; r24 header is a dated snapshot superseded by its landed commits `6572827`, `095b90c` and outside check `d730ae4` | SOURCES rule 2; QUALITY 10 (dated snapshots); round-24 lesson header is not a current-state claim |
| D-11 delimiter closure could obscure concurrent-append race | retained as open, separate from r24 delimiter fix | first row; no race patch integrated |

## Mistakes

| id | class | evidence pointer | captured-by | fix shown able to fail |
|---|---|---|---|---|
| R25-M1 | provider / landing — attempt 1 ended without report | fleet watchdog round-25 launch and `lane-dead-no-report` (attempt 1); no lane output at base | none (provider stop, not a craft defect) | recovery preserves original claim base; 0 seats reused/respawned, attempt named rather than treated as a new round |
| R25-M2 | reference-drift — relative-root recheck depends on checkout placement | r24 spot-check; `knowledge/citation-chain-fidelity-r24.md:5` | none; now QUALITY 13 | named command's clone run DRIFT 17 refused → explicit fleet root CLEAN 17/22 (`ReviewRecheckRoot.md`); append-only erratum |
| R25-M3 | landing — lesson lacks spot-check intake | `round-24.md` has no such heading | none; now QUALITY 14 | `grep -qx '## Spot-check intake' corpus/lessons/round-24.md` exits 1; same check on r25 exits 0 |
| R25-M4 | stale-premise — three legacy notes lack `recheck:` keys | r24 M-13; base mode absent (exit 2) | QUALITY 6 prospective only (r24+); legacy debt now visible | C1 names the three `META_RECHECK_ABSENT`; presence screen, not full criterion-6 enforcement |
| R25-M5 | reference-drift — two unindexed files, Frontier r11–r23 absent, 43 misfiled receipt rows, eight capability rows missing | r24 M-12/M-14; `round25-measure-before.log` 66 items | QUALITY 9/11 | same script 66→0; third unindexed integrator spot-check also indexed (outside frozen 40-file list) |
| R25-M6 | stale-premise / number-drift — SKILL open C3 finding and divergent totals; missing r16–r23 ledger addenda | r24 M-3/M-4/M-6; base script 15 stale restatements | QUALITY 9 | same script 15→0; SKILL uses owning-ledger pointer and re-derive command; source/span pairing remains uncovered |
| R25-M7 | vacuous / number-drift — owning ledger's latest tuple itself was wrong | E4 tuple 38·21·10·0·3 sums to 72 over 71 rows; review `ReviewLedgerTotals.md` | QUALITY 2/9 | row recount parses 71 rows, applies E1/E2 closures → 38·22·8·0·3 sum 71; round-25 append-only erratum; committed queue 24 distinguished from queue-true 25 |
| R25-M8 | landing — template slot shipped as a hash | r24 M-5; `hardening-r10.md:488` at base | QUALITY 10's backtick exemption was too broad (the token was syntax, not an example) | recovered gate SHA from `git show 5993dc4:tools/research-gate.sh` (`6b17e50c…`); substitution + append-only erratum, literal count 1→0 |
| R25-M9 | reference-drift — a gate quote was a paraphrase | r24 Gate S006 at §3.3 omitted enumerators; reviewer D-4 | QUALITY 2/4 | corrected quote below; r25 source re-open shows old phrase absent, corrected substring present |
| R25-M10 | vacuous — passing a syntactic screen reported as full bar enforcement | C1 critic `CriticClaim1.md`; `CriticAxisHarm.md` empty/unverified source example | QUALITY 3/8 | entry and SKILL explicitly state screen ≠ criterion 6; false-clean semantic counterexamples retained as limits, not relabelled fixed |
| R25-M11 | oracle — two derivations shared a missed token boundary | first differential `AGREE=50/54`: table missed root-parent info on a copied control; oracle whitespace tokens retained closing backtick | QUALITY 2 | adjudication against frozen spec, corrected table row + oracle tokenizer → 54/54; original seat reports retained, not rewritten |
| R25-M12 | landing — three report trailers resolved from fleet cwd | build seats SimplifierSkillMd, FrontierR14R15, CapRowR21 | wave path contract | byte-exact copy into lane, `cmp` then remove fleet copies; recorded in wave evidence before report |

Out-of-population findings are not silently absorbed into the 15→0 claim:
`ScoutPlaceholderSweep.md` finds historic slots in LOG/SCORECARD; r15–r23
battery receipts often show DRIFT under `root=.` while the prose calls them
"ALL IDENTICAL" (output identity does not imply CLEAN); r16 has no dedicated
receipt; `pointer-boundary-r21.md` contradicts itself on the path-start bypass.
The new Frontier paragraphs preserve these limits; they do not claim those
historic holds were re-proved. The r25 hold battery is captured under the
explicit fleet root, separately. These are named debt under QUALITY 2/4/9/10.

## Gate — sources opened this round

Each new row was opened by its named round-25 source scout (reports
`.ufo/waves/round-25/build/Src*.md`, exact URL/status in each), access date
**2026-10-21**. The quotes below are verbatim substrings, each ≤25 words;
none is a claim that the source validates the entire header convention.

| id / decision | URL actually opened | located quote |
|---|---|---|
| S019 mined (SrcCochraneUpdate) | https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv | Key Points: “All Cochrane reviews should be assessed periodically to determine whether an update is needed.” |
| S020 mined (SrcProvO) | https://www.w3.org/TR/2013/REC-prov-o-20130430/ | §3.2 entity lifetime: “The properties prov:generatedAtTime and prov:invalidatedAtTime can be used to bound the starting and ending moments of an Entity's existence.” |
| S021 queued (SrcShojania2007) | https://pubmed.ncbi.nlm.nih.gov/17638714/ (reader via NCBI; direct GET 203 challenge) | Abstract, Results: “A signal occurred within 2 years for 23% of reviews and within 1 year for 15%.” |
| S022 queued (SrcElliottLSR) | https://pubmed.ncbi.nlm.nih.gov/28912002/ (reader via NCBI; direct GET 203 challenge) | Abstract, LSR definition: “systematic reviews that are continually updated, incorporating relevant new evidence as it becomes available.” |
| S023 queued (SrcDcmiTerms) | https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ | §2 source Definition: “A related resource from which the described resource is derived.” |
| S024 queued (SrcSchemaReviewed) | https://schema.org/lastReviewed | Definition: “Date on which the content on this web page was last reviewed for accuracy and/or completeness.” |
| S025 rejected (SrcRfc9111) | https://www.rfc-editor.org/rfc/rfc9111 (RFC reader; HTTP resolves to /info/rfc9111/) | §4.2 Freshness: “response_is_fresh = (freshness_lifetime > current_age)” |
| S026 queued (SrcFairR12) | https://www.gofair.foundation/r1-2 | Interpretation of R1.2, first paragraph: “Detailed provenance includes facets such as how the resource was generated, why it was generated, by whom, under what conditions” |
| S027 queued (SrcWikiAsOf) | https://en.wikipedia.org/wiki/Wikipedia:As_of | Usage guidelines: “use the {{Update after}} template to indicate when it should be updated.” |
| S028 queued (SrcCrossmark) | https://www.crossref.org/services/crossmark/ | Intro before Benefits of Crossmark: “Crossmark makes this information more visible to readers.” |

S019/S020 support separate parts of the new entry; neither prescribes the
lane's header. S025 is rejected as a general research-staleness authority
(HTTP scope only), flip: use as a labelled analogy alongside a direct method
source. S027 is community tier C, never sole support. Garner et al. BMJ
354:i3507 was attempted but blocked (HTTP 403 Cloudflare); no article text,
quote or registry row — kept as a lead and a search-log exclusion with a flip.

Rows before→after: 18→28. Added tiers A=8, B=0, C=2; status mined=2,
queued=7, rejected=1. No existing status/recheck/used-by cell changed. S025's
unlanded draft `queued`→`rejected` is an L1 curation decision after opening,
not a change to a previously admitted row. Frontier path added: Keeping
records current (S019→S021→S020→S023). No row count is an expansion verdict.

### Append-only correction to the round-24 Gate

S006's round-24 Gate quote was a summary, not a verbatim substring at §3.3:
it omitted enumerators. Re-opened by `ReviewSourcesRecheck` on 2026-10-21,
version v1 remains latest. Correct located quote (≤25 words): **§3.3.1**,
“Link Works assesses URL accessibility without LLM inference”. S007's quote
still appears verbatim in §2.1 and v3 remains latest. No S006/S007 registry
row changed; only the quote error is corrected here (QUALITY 4).

### Outside spot-check slot

Round-25 independent admit/reject sample: **not performed by this lane**.
The orchestrator's fresh non-author verifier owns closure. Wave-2 seats are
advisory lane-dispatched workers, not the outside discernment check
(LEARNING.md). Prior sample: r24 outside verifier agreed on 4/4 admits and
3/3 rejects (`round-24-verifier-spotcheck.md`).
