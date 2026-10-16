# SCORECARD.md — round-9 draft sections (parent-owned file; [PARENT] binds)

<!-- SCRIBE DRAFT — MEASURED FINAL as of the fixture landings (records 01:35,
     claims fixture 01:31, archives-r9 README 01:37 local; receipts, note,
     SKILL/README rows integrate as landed). Gate sha256
     46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd on both
     sides (== HEAD `f11073a` blob; working-tree sha identical before and after
     the battery; `git diff --numstat tools/research-gate.sh` EMPTY —
     fixture-led round, no gate change by design; a gate change without a
     reported defect would be a finding — measured none). Lane HEAD still
     `f11073a`; no commits by any seat. Verdict vocabulary only: improved /
     unchanged / harmed / unprovable-but-better. No scalar scores. [PARENT]
     marks parent-only bindings. The admission section keeps the
     receipt-identity debt OPEN, per the mission contract. -->

Rounds 1–8 sections stay as written. These are the round-9 sections to
append, plus the admission/`Planned` refresh. **This round is fixture-led and
executes the move round 8 registered** (fixture-depth coverage — the archived
inputs through verify-all as records). The falsifiable claim, in the round's
own words: before, the archives have only structural verification (r1's 3/3
observable) and pointwise claims/chains (r2–r3 fixtures); no archive has
passed through verify-all as a RECORD, and claim coverage is ~17 claims.
After, the three archives exist as gate-format records under
`corpus/fixtures/archives-r9/` (every span/anchor verbatim from the archive
bytes; inter-archive hops resolve); verify-all is CLEAN on each (modulo
documented integrity findings); `claims-r9.jsonl` adds 10 new verbatim claims
beyond r2's set; coverage stats are measured; the reframing risk
(record-format distortion) is named and mitigated in the READMEs.

**Before** (gate `46f5ddb3…`, lane HEAD `f11073a`): MEASURED —
`ls corpus/fixtures/ | grep -i archive` → none; the r1 observable holds (A/B/C
each exit 1 with exactly one `RESEARCH_GATE: DRIFT` line; findings=6 drift=5;
counting command `VERDICT_BEARING_EXPORTS=3/3`); `verify-all` on a raw archive
→ `DRIFT (sections=5 run=2 absent=3 drift-sections=1 findings=6 drift=5)`
(structure drift on the export chrome + missing record sections; claims/chain/
sweeps absent; integrity refs=0); `verify-claims claims-r2.jsonl` →
`VERDICT_BEARING_CLAIMS=17/17` CLEAN with archive-citing claims A 6 · B 5 ·
C 6; `verify-chain chain-r3.md` → `RESOLVED_HOPS=17/22` CLEAN, all 22 hops
citing the three archives; archive bytes pinned (A `9033857d…` 6474 B, B
`6d8dbddd…` 5364 B, C `e48fe70f…` 8922 B).

**After** (gate `46f5ddb3…`, unchanged — fixture-led): MEASURED — three
records `corpus/fixtures/archives-r9/{A,B,C}-r9.md` (shas `338918fc…`,
`abfa5290…`, `97be0e69…`); **`verify-all` on each is fully CLEAN**
(`sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0`, exit 0;
tallies: A chain `RESOLVED_HOPS=6/7` · sweeps `1/1 REJECTIONS_OK=4/4` ·
integrity `refs=13 resolved=12 unresolved=0`; B chain 6/7 · 3/3 · refs=14/13;
C chain 7/8 · 4/4 · refs=15/14) — the round predicted "CLEAN (modulo
documented integrity findings)"; measured, no integrity finding exists on any
record (each record's 1 exempt reference is its `blocked-no-fetch` chip hop:
`コトバンク` / `arxiv.org` / `jstage.jst.go.jp`). `claims-r9.jsonl`
(`f6f0d1ab…`, 3601 B) → `VERDICT_BEARING_CLAIMS=10/10` CLEAN exit 0.
Independent re-checks (mechanisms separate from the gate): 27 JSONL spans —
24 byte-present, exactly the 3 by-design `unsupported` controls (A06, B05,
C07) byte-absent, zero r2–r9 overlap; **19/19 record chain anchors + 19/19
record claims-table `span` cells byte-verbatim** (the latter outside every
gate check); 5 inter-archive hops (A→B, A→C, B→A, C→A, C→B) all verified;
README's "no archive cites another" re-derived (`grep -cE …` → 0/0/0).
Coverage stats re-derived: 46 total claim-surface rows (17 r2 + 10 r9 JSONL +
19 in-record; round-9 delta 29); 22 hops (19 verified + 3 exempt); 11/11
rejections complete; integrity 42 = 39 resolved + 3 exempt + 0 unresolved.
Reframing risk named and mitigated in `corpus/fixtures/archives-r9/README.md`
(re-derived here; see the report's Named limits). The note (note-writer,
landed 04:45Z, revised once; observed `cf94795b…` at 01:47 local — use the
landed sha) reproduces every tally from the same record
bytes; its §5 (echoing the lesson's 19-row audit) names one real fixture
defect, confirmed by this seat at the measured revision: `A-r9.md:50` (row
C3) cites `…A-shokunin-tradition.md:76` while its span occurs at A:86 — no
gate mode pairs a row's `path:line` with its span's occurrence line, so the
composed CLEAN stands while the pointer line is wrong; `claims-r9.jsonl` A11
pins the correct A:86. Regressions held: claims-r2 17/17 · claims-r9 10/10 ·
chain-r3 17/22 · r1 3/3 · selftest `PASS (85 cases)`; gate sha unchanged
before and after the battery.

| Axis | Verdict | Evidence boundary |
|---|---|---|
| coverage | **improved** | The round's selected axis, measured both sides: no archive record existed before; after, three records compose fully CLEAN through all five verify-all sections with solo-equal tallies, claim coverage rose 17 → 27 on the JSONL surface (46 total claim-surface rows incl. in-record claims, delta 29), 5 inter-archive hops resolve, and every claim/anchor was byte-re-verified by an independent mechanism (24 present + 3 by-design absent on JSONL; 19/19 + 19/19 on records). The archives' deepest pre-existing verification was pointwise. |
| depth | **improved** [PARENT: r2–r8 precedent — each admitted round with a landed knowledge note credited depth; the note `corpus/knowledge/archives-verified-r9.md` (note-writer, landed 04:45Z, revised once; observed `cf94795b…`, 17749 B, 267 lines at 01:47 local — use the landed sha) and its tallies reproduce this seat's runs exactly] | The note + `corpus/fixtures/archives-r9/README.md` carry the semantics this seat re-derived: the reframing-risk statement and its mitigations, the residual-distortion list (`text` cells paraphrase; cut exports; tallies grade anchor existence), the coverage accounting, the measured authoring probe (`path#quote:text` drifts structure mode), and the note's §5 limit list — including the independently found `A-r9.md:50` pointer-line defect. |
| operability | **unchanged** | By design: no gate file changed (sha `46f5ddb3…` before and after the battery; diff vs HEAD blob EMPTY). The fixture battery exercised all five composed sections and the solo modes on the new records — all CLEAN, tallies agreeing with the composed sections — but no new mode/flag/branch landed, so the tool's operability boundary is unmoved; regressions held (claims-r2 17/17, claims-r9 10/10, chain-r3 17/22, r1 3/3, selftest 85). |
| freshness | **unchanged** | No new drift detector or pinned artifact; [PARENT: receipts/manifest lines (receipts-writer) pending — when they land they are receipts at the unchanged SHA]. |
| calibration | **PENDING [PARENT: judgment call — r8 precedent marked calibration improved for declaring exactly what the tool's `none` does not look at; here the README declares exactly what a CLEAN verify-all on a record does NOT certify (external truth, completeness) and lists the residual distortion; mark improved under that precedent, or unchanged if integration reads it as fixture documentation]** | The README's reframing-risk section + residual-distortion list, re-derived by this seat; the records' text/span distinction ("read span+pointer, not prose") is named, not hidden. |
| adjacency | **unchanged** | Corpus boundaries held: the archives were quoted read-only from the fleet root and never written; zero network at the gate (no fetch paths used; the blocked chip hops stayed unopened); seats wrote only in owned paths; no commits. Zero cross-archive citations in the archives themselves (0/0/0 re-derived); cross-archive hops are labeled convergence, not absorbed as citation. |

## Round-9 learning trends

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | **improved** | New admitted specimens: `corpus/fixtures/archives-r9/{A,B,C}-r9.md` (`338918fc…`/`abfa5290…`/`97be0e69…`); `corpus/fixtures/archives-r9/README.md`; `corpus/fixtures/claims-r9.jsonl` (`f6f0d1ab…`) + `claims-r9.README.md`; lesson `…verifying-conversion-not-original.md` (`eb3fb817…`); note `corpus/knowledge/archives-verified-r9.md` (observed `cf94795b…` at 01:47 local, revised once — use the landed sha); [PARENT: receipts, `SKILL.md` rows, `corpus/README.md` row — integrate as landed]. |
| quality | **improved** | The falsifiable claim measured on both sides (records absent → fully CLEAN composed verification; claim coverage 17 → 27/46 rows; inter-archive hops resolve), with byte-verbatimness independently re-derived by a second mechanism and the reframing residual named rather than smoothed over. |
| discernment | **unchanged** | No non-author admit/reject spot-check exists; no criterion added. |

## Admission and continuation (round-9 replacement text)

[PARENT: refresh the round-8 admission paragraphs after integration.]

Local axis result: coverage improved (the archives' first full deep
verification as records — three records fully CLEAN through five composed
sections, claim coverage 17 → 27 on the JSONL surface / 46 total rows,
inter-archive hops resolved, all spans/anchors byte-re-verified
independently); depth improved under the r2–r8 note precedent [PARENT];
operability unchanged (fixture-led by design — the gate sha held before and
after the battery, exactly as the round declared; no gate change without a
reported defect); calibration per the flagged judgment [PARENT]; freshness
unchanged; adjacency unchanged. Named limits carried into the record: the
reframing risk and residual distortion (README §"Reframing risk", re-derived
here), the record-format authoring constraint (`path#quote:text` structure
drift), and the new observation that the records' claims-table `span` column
rests on authoring discipline plus this seat's independent byte check, not on
a gate check, and the confirmed fixture defect at `A-r9.md:50` (pointer-line
mismatch, invisible to every mode). No scalar substitute, no promotion.
[PARENT: adjust the axis cells if integration finds a landed artifact
disagreeing with a measured value.]

Mission acceptance is separate and remains blocked on the round-1 receipt
identity: the interactive launch has no authentic queue taskKey/expected
receipt bag, so no `task_…` value may be manufactured, no shape-only receipt
counted, and no Sighting marked complete. Receipt-backed verified rounds
remain **0**; the operator target remains at least 100. Routing for this wave
was satisfied by the operator's in-session direct dispatch; no Sighting was
invoked. The round-9 artifacts are lane evidence, not a mission receipt.

Debt after round 9: receipt identity (integrator) — **STILL OPEN**; new —
(a) record-format claims-table `span` outside gate verification (authoring
discipline + independent byte check only; candidate for a future round),
(b) the `path#quote:text` structure-mode drift quirk (named by the README's
measured probe; usably documented, unfixed), (c) reframing residual (text
cells paraphrase; cut exports — named, not fixable within record fidelity),
(d) the `A-r9.md:50` (row C3) pointer-line mismatch — a fixture defect at the
measured revision `338918fc…` (pointer :76, span occurs at A:86;
`claims-r9.jsonl` A11 pins :86), found by the note/lesson's 19-row audit and
confirmed by this seat, invisible to every gate mode (a patch moves the
record sha and requires re-measuring);
carried — absent!=drift omission limit (r6), non-vacuous flip screening (r5),
id-shape boundary (r7), manifest schema growth, nested execution cost,
non-author spot-check (integrator/operator), usage/outside-path pin blind
spot (r8), masked-set blind spots (r8), re-pin policy (r8), carried residuals
(in-root hardlinks, no source size cap, token-aligned shortening,
non-ASCII-adjacent fail-closed edges, scope-refusal finding IDs,
frozen-replay comparator). [PARENT: artifact ledger with shas at integration
time.] See `.ufo/round-9/goal-wave/report-draft.md` for owners.

## Planned (round-9 refresh)

[PARENT: replace the round-8 `Planned` paragraph.] Round 9's registered move
(fixture-depth coverage — the archived inputs as records through verify-all)
ran in the operator's in-session wave and is measured (fully CLEAN on all
three records, claims coverage 17 → 27/46 rows, all anchor/span bytes
independently re-checked). Round 10 registered: [PARENT: proposed candidates —
(a) make record-format claims-table spans verdict-bearing (gate or a
sanctioned fixture-level check for the surface this round left on authoring
discipline); (b) the absent!=drift omission limit (r6, carried); (c)
non-vacuous flip screening (r5, carried); (d) manifest schema versioning.
Choose one falsifiable move.] Any next round must again declare its own
falsifiable single move and genuine scope before dispatch; do not rerun this
round's wave. Standing lane candidates: the residuals named under Debt.