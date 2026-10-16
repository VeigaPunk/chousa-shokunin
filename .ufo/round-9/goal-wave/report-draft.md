# chousa — round 9: the three archived inputs as gate-format records (coverage move, fixture-led)

<!-- SCRIBE DRAFT — MEASURED FINAL as of the fixture landings (records 01:35,
     README 01:37, claims fixture 01:31, lesson 01:44, note observed 01:47 local);
     receipts (receipts-writer), SKILL/README rows integrate as landed. Gate sha256
     46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd on both
     sides — == HEAD `f11073a` blob (`git show HEAD:tools/research-gate.sh`),
     working-tree sha identical, `git diff --numstat tools/research-gate.sh`
     EMPTY. THIS ROUND IS FIXTURE-LED: no gate change expected; a gate change
     without a reported defect is itself a finding — measured none. Lane HEAD
     `f11073a` (round-8 records); no commits by seats. Scribe scratch
     $HOME/.cache/chousa-tmp/scribe-r9/ (declared ephemeral, cleaned at end of
     run). [PARENT] markers mark parent-only bindings. The Debt section keeps
     receipt identity OPEN per the mission contract. -->

Status: **DRAFT — measured; receipts/note/SKILL/README rows integrate as
landed**. Baseline: lane HEAD `f11073a` (round-8 records). Wave: one 32-seat
flash call. Draft time: 2026-10-16 ~04:40Z.

## Work performed

- Round 9 executes the move round 8 registered: **fixture-depth coverage** —
  the three archived research inputs run through `verify-all` end-to-end as
  RECORDS, with expanded claim/hop fixtures. Falsifiable claim: before, the
  archives have only structural verification (r1's 3/3 observable) and
  pointwise claims/chains (r2–r3 fixtures); no archive has passed through
  verify-all as a record, and claim coverage is the r2 set of 17. After, the
  three archives exist as gate-format records under
  `corpus/fixtures/archives-r9/` (every span/anchor verbatim from the archive
  bytes; inter-archive hops resolve), `verify-all` composes CLEAN on each
  (modulo documented integrity findings), `claims-r9.jsonl` adds 10 new
  verbatim claims beyond r2's set, coverage stats are measured, and the
  reframing risk (record-format distortion) is named and mitigated in the
  READMEs. **All of these are measured below; the composed runs came back
  fully CLEAN (no integrity findings needed), stronger than the claim's
  conditional — reported as measured.**
- **Fixture-led by design: no gate change.** Measured, not assumed: the
  working-tree gate sha equals the HEAD blob (`46f5ddb3…`) and the diff is
  empty before and after the battery. A gate change without a reported defect
  would itself be a finding; none exists.
- Scribe independent work: the before-state battery at the settled gate
  (selftest, r1 observable, verify-all on the raw archives, the r2/r3
  fixtures, archive byte pins, fixture-absence check); the after-state battery
  (verify-all per record, the claims fixture, the record-content byte checks, the
  inter-archive hops, coverage stats, the regression set); this draft set.

## Before-state (MEASURED at gate `46f5ddb3…`, lane HEAD `f11073a`)

```text
$ git show HEAD:tools/research-gate.sh | sha256sum → 46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd
$ sha256sum tools/research-gate.sh                 → 46f5ddb3… (identical; git diff --numstat tools/research-gate.sh EMPTY)
$ bash tools/research-gate.sh --selftest           → RESEARCH_GATE_SELFTEST: PASS (85 cases) exit=0
$ ls corpus/fixtures/ | grep -i archive            → (none: no archive record exists)

$ r1 observable (verify, one fresh process each, --root ..):
  A-shokunin-tradition → exit=1, exactly one RESEARCH_GATE: DRIFT line (findings=6 drift=5)
  B-multiagent-knowledge → exit=1, exactly one RESEARCH_GATE: DRIFT line (findings=6 drift=5)
  C-rank-taxonomy → exit=1, exactly one RESEARCH_GATE: DRIFT line (findings=6 drift=5)
  counting command → VERDICT_BEARING_EXPORTS=3/3

$ bash tools/research-gate.sh verify-all ../research/deep-research-2026-09-28/A-shokunin-tradition.md --root ..
  → RESEARCH_GATE: DRIFT (sections=5 run=2 absent=3 drift-sections=1 findings=6 drift=5) exit=1
  structure DRIFT: RECORD_SCHEMA_INVALID (warn) + EXPORT_CHROME_PRESENT (info) + NO_QUESTION (crit) +
    SOURCE_TABLE_ABSENT + CLAIM_TABLE_ABSENT + REJECTION_DROPPED (warn);
  claims/chain/sweeps state=absent; integrity run CLEAN tally=INTEGRITY refs=0 resolved=0 unresolved=0.
  (the raw archive is an export, not a record: verify-all has nothing to compose)

$ bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..
  → VERDICT_BEARING_CLAIMS=17/17
    RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0) exit=0
  archive-citing claims: A 6 · B 5 · C 6 (by source path; total 17)

$ bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..
  → RESOLVED_HOPS=17/22
    RESEARCH_GATE: CLEAN (hops=22 verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0) exit=0
  all 22 hops cite the three archives as declared sources S1/S2/S3

archive bytes pinned (read-only source of truth for every span/anchor):
  A-shokunin-tradition.md  9033857d4625555c7b778dfad6df80e3e1b24ed8bffa3fee2fd445b9c5540b85  6474 B (110 lines, 109 NL)
  B-multiagent-knowledge.md 6d8dbddd3e2d2f47dcb153c5a3347cc6321db4afc72cf07da40f0f7fe5022006  5364 B (101 lines, 100 NL)
  C-rank-taxonomy.md        e48fe70ff92055c217ac6ca6ce68e403aa5689fee8717f3bd0ccf5badc92321b  8922 B (155 lines, 154 NL)
```

The hole, exactly: the three inputs are verified pointwise (17 claims, 22
hops) and structurally (r1's 3/3), but **no archive has passed through
verify-all as a record** — there is nothing to compose, because no
record-format encoding of any archive exists. The record's sections (Sources,
Chain, Claims, Sweeps, Rejections, integrity's cross-references) have never
been exercised against the actual archive bytes end to end; claim coverage is
the r2 set of 17.

## The move (fixture-led — three records + claims fixture landed; measured)

**Three archive records under `corpus/fixtures/archives-r9/`** (landed
2026-10-16 01:35 local):

- `A-r9.md` (7210 B, sha256 `338918fcb8ed5d6c5f15dc64e5eb8a3ae7a005d51b5c03e7e377c1dab9173c78`)
- `B-r9.md` (7118 B, sha256 `abfa5290deda4d1708ba97028853b8a770f16ecda6f377dddda53d49cb2e3e86`)
- `C-r9.md` (8021 B, sha256 `97be0e69ccfb8a701bc5556f738553be8e7179c9b41110fe61c4a3cab4f2d1da`)

Each is `research-record v1` shaped for the gate: Meta (window loopback,
fetch none, `claims_file` binding to claims-r9.jsonl, `archive` +
`archive_sha256` pins, note); Question; Sources (S1 the archive as tier
`export`, S2–S6/S7 named-only `secondary` rows pointing at the archive line
where the external item is named); Chain (A 7 / B 7 / C 8 hops); Claims (A 5 /
B 6 / C 8 rows, each with a `span` column); Negatives (N1 each); Sweeps (SW1
each); Rejections (A 4 / B 3 / C 4, each with reason + flip_condition).

**`corpus/fixtures/claims-r9.jsonl`** (+ `claims-r9.README.md`; sha256
`f6f0d1ab6b6cbd045035951c7eb4653406dc0853234a8077a8685509bfc94ff5`, 3601 B,
2026-10-16 01:31 local): 10 new archive-citing claims beyond r2's 17 —
A07–A11 (5), B06–B08 (3), C07–C08 (2). `verify-claims` →
`VERDICT_BEARING_CLAIMS=10/10`,
`RESEARCH_GATE: CLEAN (claims=10 supported=7 contradicted=2 unsupported=1
mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)` exit=0.

## Measurements after the move (gate `46f5ddb3…`; fresh processes; verbatim)

**Composed `verify-all` on each record** (claims section bound via each
record's Meta `claims_file`):

```text
$ bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/A-r9.md --root .. --json <scratch>/manifest-scribe-r9.jsonl
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=10/10
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=6/7
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=4/4
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=13 resolved=12 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0) exit=0

$ … B-r9.md → CLEAN sections=5 run=5 drift-sections=0; chain RESOLVED_HOPS=6/7;
  sweeps REJECTIONS_OK=3/3; integrity refs=14 resolved=13 unresolved=0; exit=0
$ … C-r9.md → CLEAN sections=5 run=5 drift-sections=0; chain RESOLVED_HOPS=7/8;
  sweeps REJECTIONS_OK=4/4; integrity refs=15 resolved=14 unresolved=0; exit=0
```

The round predicted "verify-all is CLEAN on each (modulo documented integrity
findings)". MEASURED: **fully CLEAN, no integrity findings on any record** —
each record's single exempt reference is its blocked-no-fetch chip hop
(A `コトバンク`, B `arxiv.org`, C `jstage.jst.go.jp`), counted exempt
(unresolved=0). The stronger-than-predicted result is reported as measured,
not adjusted toward the plan.

**Independent re-checks (mechanisms separate from the gate's bash matcher):**

- Claims JSONL spans, python on raw bytes: all 27 (17 r2 + 10 r9) — 24
  byte-present, exactly the 3 by-design `unsupported` controls (A06, B05, C07)
  byte-absent; contradicted markers co-occur inside their spans; zero r2–r9
  overlap; per-archive totals A 11 · B 8 · C 8.
- Record content, python on raw bytes: **19 resolved chain anchors + 19
  claims-table `span` cells — every one byte-verbatim in its cited target,
  zero misses.** The claims-table `span` column is NOT checked by structure
  mode (the gate checks pointers there, not span fidelity), so this is the
  independent confirmation of each record's Meta claim "every span and anchor
  below was extracted byte-verbatim from the archive". **Byte presence is not
  pointer-line pairing, though — one real fixture defect exists at the
  measured revision:** `A-r9.md:50` (row C3) cites
  `…A-shokunin-tradition.md:76` while its span occurs at A:86 (verified here:
  the span greps at A:86; A:76 is the section's opening sentence;
  `claims-r9.jsonl` A11 and its README pin A:86). Found by the note/lesson's
  independent 19-row audit (18/19 pointer-line agreement) and confirmed by
  this seat; no gate mode compares a row's `path:line` against its span's
  occurrence line (structure mode checks the pointer file's existence only;
  claims mode reads the JSONL surface), so the composed CLEAN stands while
  the pointer line is wrong. Named in Named limits and Debt.
- Inter-archive hops (the round's "inter-archive hops resolve"): 5 —
  A hop5→B, A hop6→C, B hop6→A, C hop6→A, C hop7→B — all verified; each row's
  notes name them as cross-archive convergence (no citation), which the gate
  verifies as anchor resolution, not as citation.
- Coverage stats re-derived: 3 records × 5 run sections, all CLEAN; 22 hops
  (19 verified + 3 exempt); 3/3 sweeps verified (each the same
  `saved-*`/`*-snapshot-*` local emptiness probe under the archive dir); 11/11
  rejections complete; integrity refs 42 = 39 resolved + 3 exempt + 0
  unresolved; claim coverage 17 → 27 on the JSONL surface, and the README's
  fuller count independently re-derived — 46 total claim-surface rows over the
  archive corpus (17 r2 + 10 r9 JSONL + 19 in-record), round-9 delta 29.
  (The in-record rows are the records' own ## Claims cells; their `span`
  column is the authoring-side surface this seat byte-checked independently.)

**Regressions held (unchanged gate; fresh processes):**

```text
$ verify-claims claims-r2.jsonl → VERDICT_BEARING_CLAIMS=17/17 CLEAN exit=0
$ verify-claims claims-r9.jsonl → VERDICT_BEARING_CLAIMS=10/10 CLEAN exit=0
$ verify-chain chain-r3.md      → RESOLVED_HOPS=17/22 CLEAN exit=0
$ r1 observable counting command → VERDICT_BEARING_EXPORTS=3/3
$ bash tools/research-gate.sh --selftest → RESEARCH_GATE_SELFTEST: PASS (85 cases) exit=0
$ sha256sum tools/research-gate.sh → 46f5ddb3… (unchanged; diff vs HEAD blob EMPTY)
```

## Landed changes (at integration time)

- `corpus/fixtures/archives-r9/{A,B,C}-r9.md` (shas above; records-impl-fixture-lead).
- `corpus/fixtures/archives-r9/README.md` (landed 2026-10-16 01:37 local;
  records the same pins, the re-run recipe, the coverage before→after, the
  reframing-risk section, and authoring notes incl. the measured
  `path#quote:text` structure-mode drift probe).
- `corpus/fixtures/claims-r9.jsonl` (`f6f0d1ab…`) + `claims-r9.README.md`
  (`64b63db6…`) — fixture-expander, landed 01:31 local.
- Lesson `corpus/lessons/2026-10-16-verifying-conversion-not-original.md`
  (`eb3fb817…`, 11989 B; lessons-distiller) — landed 01:44 local; its
  "fixture shas at measurement" (records/claims/README shas and the arms of
  the before/after measurement) agree with this seat's independently taken
  values.
- Note `corpus/knowledge/archives-verified-r9.md` (note-writer) — landed
  04:45 local; its composed tallies reproduce this seat's runs exactly from
  the same record bytes, and its §5 names the `A-r9.md:50` C3 pointer-line
  defect (independently confirmed by this seat; Named limits below). Observed
  sha256 `cf94795bf623d49a47e5c0ea0fbe8002d84a36b3e3d280eeb7d0130690c0f4a2`
  (17749 B, 267 lines) at 01:47 local — the note was revised once after its
  first landing, so [PARENT: use the landed sha].
- [PARENT: integrate only what lands — evidence receipts (receipts-writer),
  `SKILL.md` rows, `corpus/README.md` row; not confirmed at this seat's last
  check.]

## Named limits

- **Reframing risk (record-format distortion) — named and mitigated in
  `corpus/fixtures/archives-r9/README.md` §"Reframing risk", re-derived by
  this seat.** The README's statement: a CLEAN `verify-all` on these records
  "certifies record-format integrity against archive bytes — not the external
  truth of anything the archives cite, and not the completeness of their
  arguments." Its named mitigations, each independently re-checked here:
  claims scoped as text-level observations with verbatim spans; spans/anchors
  machine-extracted, gate-verified (chain) plus byte-checked (record spans,
  19/19 by this seat); tiers never promote the exports above `export`; bare
  chips stay `blocked-no-fetch` and unopened; inter-archive hops are labeled
  convergences — and the README's "no archive cites another" check
  independently re-derived (`grep -cE 'deep-research|archive [ABC]|export
  [ABC]|A-shokunin|B-multiagent|C-rank'` → 0/0/0 across the three archives);
  corrections kept as rejections (4/3/4, all complete); the sweep proves only
  its own local re-run. Residual distortion, named in the README and
  confirmed: `text` cells paraphrase — only `span` cells and chain anchors are
  verbatim ("read span+pointer, not prose"); the exports are cut mid-response,
  so a record structures what survived; tallies grade anchor existence, not
  argument strength.
- **Record-format authoring constraint (measured by the fixture seats, noted
  here):** a `to` cell written as `path#quote:text` drifts structure mode
  (`CHAIN_HOP_UNRESOLVED`, because the structure check cuts a pointer at its
  first `:` and sees the file as `path#quote`); the records therefore use a
  declared source id or a clean local path plus `anchor_kind`/`anchor`
  columns. This is consistent with this seat's verify-all battery (all chain
  hops CLEAN, 19/19 anchors byte-verbatim).
- **Fixture defect at the measured revision — `corpus/fixtures/archives-r9/A-r9.md:50`
  (row C3):** the pointer cell cites `…A-shokunin-tradition.md:76` while the
  row's span occurs at A:86 (verified here; `claims-r9.jsonl` A11 and its
  README pin A:86). Found by the note/lesson's independent 19-row audit
  (18/19 pointer-line agreement) and confirmed by this seat; no gate mode
  compares a row's `path:line` against its span's occurrence line, so every
  composed verdict remains CLEAN. A patch by the fixture seat would change
  the record sha (`338918fc…`) and require re-running this seat's battery.
- **New gate-coverage observation (not a defect):** the records' claims-table
  `span` column is outside every current gate check (structure mode checks
  `pointer`, not `span`); its verbatimness rests on authoring discipline plus
  this seat's independent byte check (19/19). A candidate for a future round
  if record-format claims spans should be verdict-bearing.
- Carried debts apply (see Debt).

## Admission

[PARENT: ADMIT/REJECT line + commit hashes; no scalar; axis verdicts live in
SCORECARD.md's round-9 sections.]

## Debt

- **Receipt identity (round 1): STILL OPEN.** No authentic queue
  taskKey/expected receipt bag exists; mission acceptance is integrator-owned;
  no `task_…` value was invented, no shape-only receipt counted, proven
  receipt-backed completed rounds remain 0, operator target unchanged (≥100).
  Routing for this wave was satisfied by the operator's in-session direct
  dispatch; no Sighting step was invoked. Round-9 artifacts are lane evidence,
  not a mission receipt.
- Carried (unchanged by this round): absent!=drift omission limit (r6);
  non-vacuous flip screening (r5); id-shape boundary (r7); manifest schema
  growth; nested execution cost; non-author spot-check (integrator/operator);
  carried residuals (in-root hardlinks, no source size cap, token-aligned
  shortening, non-ASCII-adjacent fail-closed edges, scope-refusal finding IDs,
  frozen-replay comparator); usage/outside-path pin blind spot (r8); masked-set
  blind spots (r8); re-pin policy (r8).
- New after round 9 (named in Named limits; candidates for `Planned`):
  (a) the records' claims-table `span` column is outside every gate check —
  authoring discipline plus this seat's independent byte check only;
  (b) the `path#quote:text` structure-mode drift quirk (documented by the
  README's measured probe, unfixed);
  (c) the reframing residual (`text` cells paraphrase; cut exports) — named,
  not fixable within record fidelity.

## SHONEN

[PARENT: all four `[ ]` unless a named non-author verifier is bound this
round.]

Boundaries held: no gate change (sha identical to HEAD blob; diff empty);
corpus read-only (the archives are quoted, never written); seats write only in
owned paths; no commits by seats.