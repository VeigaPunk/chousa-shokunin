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

## Falsify-wave packaging correction (round 25, same attempt)

R25-M13 — **landing / reference-drift**: the L1 omitted
`tools/research-gate.sh` from the helper's integration path list. Checkpoint
`0fc037e6b07f3820ead8c9207a8034ac854197a1` contained prose claiming 154 cases
but gate SHA `752e4e38…` with 136. The fresh mutation seats caught this before
any round report. QUALITY 11 and protocol measured-revision duty should have
caught it; now criterion 15 names the content-digest check explicitly.

Fix: helper-landed `d8c8cff3923f10481ac9ced66d0af7c41d38130c` includes the
gate and canonical SHONEN form. `git show <rev>:tools/research-gate.sh |
sha256sum` differs from the measured gate for `0fc037e`, matches for `d8c8cff`.
The same 68 live falsify seats were sent an additive checkpoint correction
(`.ufo/waves/round-25/falsify-checkpoint-correction.json`); none respawned.
Reports must distinguish the failed initial packaging from corrected-checkpoint
measurements. No result observed only in the working tree counts as committed
proof. The original falsify spec remains unchanged as dispatch history.

The same defect also omitted `corpus/evidence/README.md` from `0fc037e` and
`d8c8cff`; FxScribeEvidence caught the unchanged blob before the final report.
Thus d8c8cff is a corrected **gate** checkpoint, not yet a complete C2
checkpoint. The next helper landing includes the evidence index and all
current errata, and is the authoritative full integration pin. Criterion15
must cover every changed production path, not just the executable. Both
omissions remain recorded; repeated packaging correction is not two claims.

## Falsify integration — corrections, not a clean first pass

The fresh wave attacked checkpoint e93ac711 after two packaging omissions
were corrected. Its reports are `.ufo/waves/round-25/falsify/*.md`; they are
advisory lane workers, never the outside closure. The following supersedes
stronger earlier wording in this lesson and the initial checkpoint records:

- **C1 security/grammar:** FxSentinelMeta found hardlink aliases, pathname
  reopen races, a read-before-cap stat fallback, raw token echo and symlink
  size misclassification. The final metadata reader binds stat + one bounded
  NUL-delimited snapshot read to an opened fd, checks its resolved pathname,
  refuses multilinks/stat failure, then parses the snapshot. It never emits
  recheck token contents and shell-quotes displayed paths. An exact literal
  `## ` ends the header (not a tab); recheck dates must be calendar-valid.
  Duplicate keys are clarified last-key-wins, and an empty source key remains
  presence-only (not semantic support). Seven added pinning cases cover the
  symlink, multilink, stat-failure, calendar, tab, token-echo and held-object
  branches. Original 154-case checkpoint results remain historical.
- **C2 measurements:** FxCritC2 deleted a receipt row and the old counter
  stayed zero. The corrected counter freezes the exact 43 receipt identities
  and counts absent, duplicate or misfiled rows; original before=43/after=0 is
  unchanged. Empty/missing LOG/index/SKILL/population inputs now fail instead
  of returning a vacuous zero; set-e/pipefail propagates Python failures.
- **C3 append-only:** FxCritC3 correctly rejected the in-place GSHA fill.
  The original Round-13 line is restored; the appended disposition resolves
  it with gate6b17e50c. Raw historical token count remains1, unresolved1→0.
  The raw-token-zero prediction is withdrawn as incompatible with the
  append-only requirement; `STALE_RESTATEMENTS` still measures the same
  finding, now by explicit unresolved disposition, not deletion of history.
- **Freshness:** Frontier r12–r23 paragraphs now explicitly qualify raw-r1
  receipt gaps and DRIFT `root=.` batteries. R16's new case is110, not111
  (the sweeps case shifted to111); r20's case123 was absorbed prior work.
  Ledger addenda distinguish §3.9 round11 queue from later named-debt queues,
  acknowledge r20's independent recheck append, and give r24 its own heading.
  README's stale18-source count is replaced by its owning registry pointer.
- **D6/D10 intake precision:** D6's old source-search stop is not retroactively
  repaired; a new note qualifies it as a convenience sample, never saturation.
  D10 remains a historical snapshot limitation, not a re-derived commit-window
  fix; carried under QUALITY10. Neither is counted as a new closed defect.
- **Captured-by corrections (FxLessonMistakes):** M5/M6 QUALITY9/11 are the
  current repair policy, not historical capture (they were prospective at r24).
  M7 was captured by **none**: QUALITY2/9 did not require owning-row arithmetic;
  new16 does. M9's direct bar is SOURCES contractv1 rule1 (verbatim located
  quote), not QUALITY2/4 alone. M11 was captured by **none** (a shared oracle
  blind spot); new17 requires an independent failure-capable control. M12's
  byte-copy/cmp was observed by the integrator, not independently certified;
  fresh seats verified the three destination reports exist, not byte equality
  to now-removed originals. No independent copy proof is invented.

### Gate correction rows — opened again, 2026-10-21

These new rows correct teachings without editing old immutable row cells.
S019 mined→queued and used-by `corpus/knowledge/metadata-screen-r25.md`→`—`;
S020 likewise mined→queued and used-by→`—`. S029/S033 now ground the entry.
Other old status/recheck/used-by cells unchanged. Final rows18→33 (15 added:
A13/B0/C2); status totals mined10/queued19/rejected4. Old 18→28 statements
above describe the first integration, not the final census.

| new row / supersedes | URL (access 2026-10-21) | located quote (≤25 words) |
|---|---|---|
| S029 / S019 | https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv | §IV.1 Introduction: “All Cochrane reviews should be assessed periodically to determine whether an update is needed.” |
| S030 / S022 | https://pubmed.ncbi.nlm.nih.gov/28912002/ | Abstract: “systematic reviews that are continually updated, incorporating relevant new evidence as it becomes available.” |
| S031 / S024 | https://schema.org/lastReviewed | Definition: “Date on which the content on this web page was last reviewed for accuracy and/or completeness.” |
| S032 / S021 | https://pubmed.ncbi.nlm.nih.gov/17638714/ | Abstract Results: “A signal occurred within 2 years for 23% of reviews and within 1 year for 15%.” |
| S033 / S020 | https://www.w3.org/TR/2013/REC-prov-o-20130430/ | §3.2 entity lifetime: “The properties prov:generatedAtTime and prov:invalidatedAtTime can be used to bound the starting and ending moments of an Entity's existence.” |

S029 was re-opened by FxSrcCochrane and the L1; S030/FxSrcElliott,
S031/FxSrcSchema and S032/FxSrcShojania; S033's exact HTML sentence was
re-opened by L1 after FxSrcProvO died. S026 was also re-opened by L1 after
FxSrcFAIR died; its quoted R1.2 sentence is present. Supersession removes
unsupported “recorded schedule”, unlabelled cadence comparison, date-property
comparison and signal→actual-update implications; PROV entity lifetime is
not verification validity. This is scoped curation, not new medical/HTTP/
ontology province adoption.

## Replacement-writer reconciliation (same attempt)

`ChousaR25` inherited the verified wave registries (build68, falsify68),
checkpoint `e93ac711` and uncommitted final corrections after the coordinator
session ended. Re-measured rather than respawned: final counter, differential,
ledger and explicit-root hold battery; receipts
`corpus/evidence/round25-final-{measure,differential,ledger,holds,census}.log`.
Final selftest161/161 supersedes checkpoint154; original 27-fixture54/54
still holds. Old raw-token-zero prediction discarded in favor of restoring
the historical line and resolving its slot append-only (raw1/unresolved0).
No dead seat was replaced; three residual reviewers check the new corrections.

The final fleet-root misroot sweep (`git -C /home/vgpnk/Projects/shokunin
status --porcelain`) found only driver runtime (`.ufo/watchdog.log` and
`.ufo/state/*.report-baseline`), no new chousa seat output to relocate.
The earlier three-copy incident remains the original integrator's observation,
not fresh proof of byte equality to removed originals.

### Residual counter review — R25-M14

Class **vacuous / stale-premise**; evidence
`.ufo/waves/round-25/residual-final-measures.md`; captured-by QUALITY2/9.
The original C3 counter could reward deletion and README retained an
undated handoff tuple. The current note explicitly dates that tuple.
Counter guards require the recount pointer, exact historical slot and
marker inside its appended correction, and E/case-bearing addendum bodies.
`corpus/evidence/round25-final-counter-controls.json` preserves exact Python
programs and observed exits: clean0, slot-deleted1, marker-relocated1,
empty-addendum1, recount-deleted1. The differential's population parser
also gives clean0/table-row-deleted1. These guards are shown able to fail;
they are not semantic proof of every paragraph or index cell.

`round25-measure.sh` is a counting **probe**, not an admission gate. Its
exit0 only means it ran; compare the recorded 25/28, exact three drift
names, zero counters and 3/3 hold to the frozen predictions. C2 syntax
counts still require the retained per-entry/receipt/capability reviews.
The differential is documented from the lane root, not an arbitrary cwd.
