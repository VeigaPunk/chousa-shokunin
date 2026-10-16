# chousa — round 10: archive-scale negative controls + the limit-disposition ledger (hardening/calibration move)

<!-- SCRIBE DRAFT — MEASURED through the controls battery, the exempt audit and
     the ledger reconciliation; receipts/SKILL/README integrate as landed.
     Gate sha256
     46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd on both
     sides — == HEAD `d5c99c2` blob (`git show HEAD:tools/research-gate.sh`),
     working-tree sha identical, `git diff --numstat tools/research-gate.sh`
     EMPTY. Fixture-led: no gate change; a gate change
     without a reported defect is itself a finding — measured none. Lane
     HEAD `d5c99c2` (round-9 records); no commits by seats. Scribe scratch
     $HOME/.cache/chousa-tmp/ (`scribe-r10-*.log`; declared ephemeral, cleaned
     at end of run). [PARENT] markers mark parent-only bindings. The Debt
     section keeps receipt identity OPEN per the mission contract. -->
<!-- STATUS: `corpus/fixtures/archives-r9/controls/` landed 2026-10-16 05:41Z
     local (controls-author); this seat measured all six defect classes at
     05:43Z and independently re-derived every base diff — all six DRIFT
     naming exactly their class (part 1 below). `corpus/knowledge/hardening-r10.md`
     landed 05:45:38Z (`f5dc8889…`); this seat's completeness check found THREE
     carried residual classes without rows while §3.9 claims completeness →
     finding (part 3). Lesson `92656ca2…` and controls README `23f47722…`
     landed; receipts/SKILL/README integrate as landed. -->

Status: **DRAFT — before-state, controls, exempt audit and ledger reconciliation
measured (one ledger-completeness finding); receipts/SKILL/README integrate as
landed**. Baseline: lane HEAD `d5c99c2` (round-9 records). Wave: one 32-seat
flash call. Draft time: 2026-10-16 ~05:56Z.

## Work performed

- Round 10 executes the move round 9 registered: **residual hardening** —
  (a) negative controls at archive scale (broken archive records per defect
  class), (b) the exempt-hop audit, (c) disposition of every r2–r9 named
  limit. Falsifiable claim: before, no negative controls exist at archive
  scale (defect classes are only covered by small fixtures), the exempt items
  in the archive records are unaudited, and the limits named across rounds 2–9
  have no single disposition ledger. After, one broken archive record per
  defect class (span-not-found, anchor-missing, dangling-ref,
  rejection-missing-flip, false-sweep, structure-break) each DRIFTs verify-all
  naming exactly its class; every exempt item in the archive records is
  justified by source bytes (or is a finding); `corpus/knowledge/hardening-r10.md`
  carries the complete disposition ledger.
- **Fixture-led by design: no gate change.** Measured, not assumed: the
  working-tree gate sha equals the HEAD blob (`46f5ddb3…`) and the diff is
  empty before the battery, and re-derived identical after all runs at 05:49Z
  (no seat wrote the gate). A gate change without a reported defect would
  itself be a finding; none exists.
- Scribe independent work: the before-state battery at the settled gate
  (selftest, `--drift` vs the r8 baseline, verify-all on the three archive
  records, r2/r3 fixture regressions, the r1 observable, control-absence
  check); the **controls battery** (all six re-run fresh; base diffs
  re-derived; two full runs quoted verbatim); the **exempt-item audit**
  (6/6 items captured verbatim solo and justified against the archive source
  bytes, below); the **ledger reconciliation** against this seat's enumeration
  (68 rows re-counted; one finding: three carried residuals unmapped); this
  draft set.

## Before-state (MEASURED at gate `46f5ddb3…`, lane HEAD `d5c99c2`)

```text
$ git show HEAD:tools/research-gate.sh | sha256sum → 46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd
$ sha256sum tools/research-gate.sh                 → 46f5ddb3… (identical; git diff --numstat tools/research-gate.sh EMPTY)
$ bash tools/research-gate.sh --selftest           → RESEARCH_GATE_SELFTEST: PASS (85 cases) exit=0
$ bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r8-20261016T033757Z.json
                                                   → GATE_DRIFT: none exit=0
$ ls corpus/fixtures/archives-r9/controls/         → No such file or directory (no archive-scale negative control exists)

$ verify-all corpus/fixtures/archives-r9/A-r9.md --root .. (claims bound via Meta claims_file)
  SECTION structure state=run verdict=CLEAN findings=0 drift=0
  SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=10/10
  SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=6/7
  SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=4/4
  SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=13 resolved=12 unresolved=0
  VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0
  RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0) exit=0
$ … B-r9.md → CLEAN sections=5 run=5; chain 6/7; sweeps 1/1 3/3; integrity refs=14 resolved=13 unresolved=0; exit=0
$ … C-r9.md → CLEAN sections=5 run=5; chain 7/8; sweeps 1/1 4/4; integrity refs=15 resolved=14 unresolved=0; exit=0

$ regressions (fresh processes):
  verify-claims claims-r2.jsonl → VERDICT_BEARING_CLAIMS=17/17 CLEAN exit=0
  verify-claims claims-r9.jsonl → VERDICT_BEARING_CLAIMS=10/10 CLEAN exit=0
  verify-chain chain-r3.md      → RESOLVED_HOPS=17/22 CLEAN exit=0
  r1 observable counting command → VERDICT_BEARING_EXPORTS=3/3
```

The hole, exactly (three parts): (1) every negative control in the lane is
small-fixture scale (`chain-r3-broken.md`, `sweeps-r5-broken.md`,
`integrity-r7-broken.md`, `full-r6-broken.md`) — **no broken archive record
exists**, so no defect class is demonstrated against the archive corpus the
lane's research actually verifies; (2) the archive records carry 6 exempt
items (3 `blocked-no-fetch` chain hops + 3 integrity tokens on those rows)
that every mode counts but never resolves — no audit exists saying the
exemptions are truthful; (3) the named limits live scattered across nine
knowledge notes (r2–r9) and two SCORECARD debt paragraphs — **no single
disposition ledger** existed at this revision.

## The move, part 1 — archive-scale negative controls (MEASURED)

`corpus/fixtures/archives-r9/controls/` landed 2026-10-16 05:41Z local
(controls-author: 6 controls + 1 claims copy + README). Each control is a
scripted byte-copy of a clean archive record with exactly one defect cell (or
one section) mutated, plus the record's Meta `note` row — this seat
independently re-derived every base diff from the bytes, so single-defect
isolation is confirmed, not assumed:

```text
A-r9-anchor-missing.md        A-r9.md: hop 2 anchor quote `not a universal rank ladder` → `…certification ladder`
A-r9-span-not-found.md        A-r9.md: Meta claims_file rebound; its claims copy differs in exactly one span (A07 `four`→`five`)
B-r9-rejection-missing-flip.md  B-r9.md: R2 flip_condition cell emptied
B-r9-false-sweep.md           B-r9.md: SW1 where → research/deep-research-2026-09-28/*.md (a glob the archive dir satisfies: 3 hits)
C-r9-dangling-ref.md          C-r9.md: hop 1 from `C1` → the undeclared claim id `C9`
C-r9-structure-break.md       C-r9.md: the `## Question` section (heading + body) removed
```

Pins (sha256; re-computed by this seat, agree with the controls README):
`A-r9-span-not-found.md 5dedb73b…` + `.claims.jsonl 0edb78ee…`,
`A-r9-anchor-missing.md e3490cf4…`, `B-r9-rejection-missing-flip.md b0d488aa…`,
`B-r9-false-sweep.md 69b7b08f…`, `C-r9-dangling-ref.md b24be0f0…`,
`C-r9-structure-break.md 21d77e6c…` (full shas in the controls README §Pins).

All six composed runs (this seat, fresh processes 05:43Z, `--root ..`; the
controls README's own runs 05:40–05:42Z reproduce every line modulo `ts=` —
two independent executions of the same bytes):

| control | defect class | section dirty | finding id (verbatim obs) | tally | exit |
|---|---|---|---|---|---|
| `A-r9-span-not-found` | span-not-found | claims | `CLAIM_SPAN_NOT_FOUND … obs=id=A07` | `VERDICT_BEARING_CLAIMS=9/10` | 1 |
| `A-r9-anchor-missing` | anchor-missing | chain | `CHAIN_ANCHOR_NOT_FOUND … obs=hop=2` | `RESOLVED_HOPS=5/7` | 1 |
| `B-r9-rejection-missing-flip` | rejection-missing-flip | sweeps | `SWEEP_REJECTION_INCOMPLETE … obs=id=R2 missing=flip` | `REJECTIONS_OK=2/3` | 1 |
| `B-r9-false-sweep` | false-sweep | sweeps | `SWEEP_CLAIM_FALSE … obs=id=SW1 … hits=3` | `VERIFIED_SWEEPS=0/1` | 1 |
| `C-r9-dangling-ref` | dangling-ref | integrity | `REF_UNRESOLVED … obs=kind=claim id=C9 section=chain row=1 cell=from` | `refs=15 resolved=13 unresolved=1` | 1 |
| `C-r9-structure-break` | structure-break | structure | `NO_QUESTION severity=crit surface=question` | (structure: findings=1) | 1 |

Every run: `VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1
drift=1`, `RESEARCH_GATE: DRIFT`, and **the other four sections CLEAN** — each
control's drift names exactly its class and nothing else drifted. Verbatim,
two full runs of the six (all six captured in the controls README §Measured
outputs and this seat's fresh re-runs):

```text
$ bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/controls/A-r9-span-not-found.md --root ..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=DRIFT findings=1 drift=1 tally=VERDICT_BEARING_CLAIMS=9/10
FINDING CLAIM_SPAN_NOT_FOUND severity=warn surface=claims obs=id=A07 nearest_line=35 context=Deep research: The shokunin (職人) concept in Japanese artisan tradition — a
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=6/7
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=4/4
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=13 resolved=12 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1
RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1)
exit=1

$ bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/controls/C-r9-structure-break.md --root ..
SECTION structure state=run verdict=DRIFT findings=1 drift=1
FINDING NO_QUESTION severity=crit surface=question obs=missing ## Question section
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=10/10
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=7/8
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=4/4
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=15 resolved=14 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1
RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1)
exit=1
```

The span-not-found control's claims copy, run direct: `verify-claims
A-r9-span-not-found.claims.jsonl --root ..` → `VERDICT_BEARING_CLAIMS=9/10`,
`RESEARCH_GATE: DRIFT (claims=10 supported=6 contradicted=2 unsupported=2
mismatched=1 unproven=0 refused=0 invalid=0 findings=1 drift=1)` **exit=1**
(the composed section and the solo run agree). The controls README's
§"Why structure-break is `NO_QUESTION`" also records the author's probe that
`RECORD_SCHEMA_INVALID` cannot fire alone (it drags 3 further structure
findings); removing `## Question` is the smallest edit isolating exactly one
structure finding — an authoring note, no gate matter.

## The move, part 2 — the exempt-item audit (MEASURED, this seat)

The archive records' exempt items, captured verbatim from solo runs at the
unchanged gate (`verify-chain` / `verify-integrity`, `--root ..`; the
composed runs carry the same tallies by construction):

```text
A-r9.md: CHAIN hop=7 status=blocked-no-fetch observed=exempt source=コトバンク anchor=- at=- verdict=exempt
          REF kind=claim id=C1 section=chain row=7 cell=from observed=exempt verdict=exempt status=blocked-no-fetch
B-r9.md: CHAIN hop=7 status=blocked-no-fetch observed=exempt source=arxiv.org anchor=- at=- verdict=exempt
          REF kind=claim id=C3 section=chain row=7 cell=from observed=exempt verdict=exempt status=blocked-no-fetch
C-r9.md: CHAIN hop=8 status=blocked-no-fetch observed=exempt source=jstage.jst.go.jp anchor=- at=- verdict=exempt
          REF kind=claim id=C8 section=chain row=8 cell=from observed=exempt verdict=exempt status=blocked-no-fetch
```

**6/6 exempt items audited; 6/6 justified by source bytes; 0 findings.**
Per-item justification (the exemption's claim: the hop cannot resolve locally
because the target is citation furniture, and nothing external is opened):

1. **A hop7 `コトバンク`** — `grep -n コトバンク A-shokunin-tradition.md` → 68, 72;
   the record's note names the A:68 chip (line 68 is the bare chip alone on its
   line; the audit also finds a second コトバンク chip at A:72 — the note's
   "the A:68 chip" is not an exhaustiveness claim, no contradiction). A bare
   aggregator name on its own line is not a URL and not a local path — no local
   resolution is possible, so `blocked-no-fetch` is the truthful status.
2. **B hop7 `arxiv.org`** — `grep -n arxiv.org B-multiagent-knowledge.md` → 51, 72;
   the record's note says "the B:51 and B:72 chips" — both lines are the bare
   host alone on its line. Same justification.
3. **C hop8 `jstage.jst.go.jp`** — `grep -n jstage.jst.go.jp C-rank-taxonomy.md`
   → 103; the note names the C:103 chip; bare host alone on its line. Same
   justification.
4. **A `REF C1` (chain row 7 `from`)**, 5. **B `REF C3`**, 6. **C `REF C8`** —
   the integrity exemption is the r7 blanket rule (an exempt-status row's
   reference tokens count exempt, never required to resolve). Audit: each token
   is a DECLARED claim id in its record (A ## Claims declares C1; B C3; C C8) —
   so no undeclared/dangling id is hiding behind the exemption; the exemption
   covers a token that would have resolved anyway.

Supporting re-derivations (fresh runs, lane cwd): each record's sweep re-runs
empty — `ls ../research/deep-research-2026-09-28/saved-* ../research/deep-research-2026-09-28/*-snapshot-*`
→ both No such file or directory (exit 2), matching `VERIFIED_SWEEPS=1/1` on
all three records; the three archives carry no other exempt class (claims
10/10 CLEAN with refused=0; rejections all complete: 4/4, 3/3, 4/4; structure
findings=0).

## The move, part 3 — the disposition ledger (MEASURED; one finding)

`corpus/knowledge/hardening-r10.md` landed 2026-10-16 05:45:38Z (note-writer;
sha256 `f5dc8889534a8527d5fd010c1f9e2493d4214f358566d0f1fea0e91ae1f3a2f0`,
30317 B): a 68-row disposition ledger — by-design 38 · carried 22 · closed 3 ·
finding 1 · operator 4 — each row with evidence, plus a 27-item round-11 audit
queue (cheapest-first). Its §1 controls map and §2 exempt audit reproduce this
seat's measurements; its row count and disposition counts re-derive by grep;
its queue arithmetic closes for its own 68 rows; its single `finding` (row 53)
matches this seat's re-verified `A-r9.md:50` state.

**Completeness check (this seat's reconciliation; measured item-by-item against
the enumeration in Named limits):** every enumerated class maps to a row —
r2 semantic / binding / contradicted-structural / source-truth / external /
adoption / text-files → rows 1–7; r3 chain classes → 16–19 (+ the
to-fragment seam at 22); r4 boundary
residues → 10–15; r5 → 23–27; r6 → 29–33; r7 → 35–44; r8 → 44–52; r9 → 53–59;
r1/debts → 64–68 — **except three carried residuals that the r2–r8 knowledge
notes and the landed lesson name** (the lesson
`corpus/lessons/2026-10-16-archive-scale-controls-and-ledger.md:110-112` lists
them in its own enumeration): **in-root hardlink bypass of path
canonicalization, no source size cap on reads, and the cosmetic banner string
`research-gate-r1`. None of the three has a row anywhere in §3.1–§3.9**, while
§3.9 (`corpus/knowledge/hardening-r10.md:306-313`) claims "checked
item-by-item: every enumerated class has a row above". **FINDING
(ledger-side — the note-writer's file, reported not fixed):** the ledger is
three rows short of its own completeness claim (a 71-row total and a 30-item
queue would close it if the three were added as `carried`/`by-design`; the
disposition wording is the note-writer's call). Everything else in the ledger
re-checks clean.

[PARENT: if a separate `limit-ledger`-named artifact lands at integration,
reconcile it against `hardening-r10.md` §3 — the ledger's §5 records that the
dispatch named such a seat but no artifact under that name was observed on
disk at 05:44Z; this seat observed none either (its own enumeration in Named
limits was the only on-disk one).]

**Measurements after the move** (gate `46f5ddb3…`; fresh processes; verbatim):

```text
Controls, all six (this seat 05:43Z; controls README's runs 05:40–05:42Z reproduce modulo ts=):
  A-r9-span-not-found      claims    DRIFT CLAIM_SPAN_NOT_FOUND id=A07      9/10         exit=1
  A-r9-anchor-missing      chain     DRIFT CHAIN_ANCHOR_NOT_FOUND hop=2    5/7          exit=1
  B-r9-rejection-missing-flip sweeps DRIFT SWEEP_REJECTION_INCOMPLETE id=R2 missing=flip  REJECTIONS_OK=2/3 exit=1
  B-r9-false-sweep         sweeps    DRIFT SWEEP_CLAIM_FALSE id=SW1 hits=3  0/1          exit=1
  C-r9-dangling-ref        integrity DRIFT REF_UNRESOLVED kind=claim id=C9 chain row=1 from  refs=15 resolved=13 unresolved=1 exit=1
  C-r9-structure-break     structure DRIFT NO_QUESTION crit                 findings=1   exit=1
  each: sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1; other four sections CLEAN;
        clean bases still CLEAN exit=0 in the same run window
  companion direct: verify-claims A-r9-span-not-found.claims.jsonl → 9/10 DRIFT exit=1

Exempt audit: 6/6 items justified by source bytes, 0 findings (above).

Holds at the unchanged gate (re-run this battery): selftest PASS (85 cases) · GATE_DRIFT: none ·
claims-r2 17/17 · claims-r9 10/10 · chain-r3 17/22 · r1 observable 3/3 ·
tools/research-gate.sh sha 46f5ddb3… unchanged (== HEAD blob; diff EMPTY).
```

The ledger reconciliation is part 3 above (one finding: the three unmapped
carried residuals); nothing further pending in this section. [PARENT: if the
note-writer adds the three rows, re-derive the counts (68 → 71; queue 27 → 30)
and clear the finding.]

## Landed changes (at integration time)

- `corpus/fixtures/archives-r9/controls/` (controls-author; landed 05:41Z) —
  6 controls + 1 claims copy + README (`23f47722…`); control shas in part 1.
- `corpus/knowledge/hardening-r10.md` (note-writer; landed 05:45:38Z;
  `f5dc8889…`, 30317 B) — the 68-row disposition ledger + 27-item round-11
  queue; the 3-row completeness finding is in part 3.
- `corpus/lessons/2026-10-16-archive-scale-controls-and-ledger.md`
  (lessons-distiller; `92656ca2…`, 15334 B) — its §5 lists the same named
  residuals the ledger finding concerns.
- [PARENT: receipts (receipts-writer, `corpus/evidence/`), `SKILL.md` rows
  (skill-row-updater), `corpus/README.md` row (corpus-readme-updater) — not
  observed landed at this seat's last check (~05:52Z); integrate only what
  lands; record sha256 for each.]

## Named limits

- **Ledger completeness target (this seat's enumeration to check the note
  against):** r2 note (semantic support not proven; location binding/
  uniqueness; source truth; external verification; adoption boundary;
  text-files/whole-memory; in-root hardlinks; no source size cap; banner
  cosmetic; fixture spans are byte controls not knowledge; refused never
  opened) — r3 note (substring semantics [partially closed r4]; exempt ≠
  verified; cross-input co-anchors; no transitivity; heading kind unusable on
  headingless sources; carried residuals) — r4 note (token-aligned shortening;
  non-ASCII boundary false negatives; `_`-adjacent gluing; outer-edges-only
  checking; only resolved hops affected) — r5 note (flip-condition semantic
  vacuity; sweeps-mode section absence; recorded command never re-run) — r6
  note (omission limit; sweeps-only-rejections representation; nested
  execution cost) — r7 note (case-sensitive id shapes; non-id-shape variants;
  duplicate declarations; unscanned columns; companion-only ids; exempt-status
  blanket exemption; prose over-extraction; to-fragment r1-vs-r3 seam) — r8
  note (exit-code-only regressions; behavior outside canonical invocation;
  oracle strength; semantic drift inside stable fields; masked fields;
  per-row movement outside pinned surface; `LANE_ROOT` env caveat) — r9 note
  (reframing risk; claims-table `span` column outside every gate check;
  `path#quote:text` structure quirk; `A-r9.md:50` pointer-line defect;
  coverage-is-selection; chain-of-custody stops at the export; cut exports) —
  plus r1/SCORECARD debts (receipt identity; scope-refusal finding IDs;
  non-author spot-check; frozen-replay comparator; export-unverified).
- **`A-r9.md:50` (row C3) pointer-line defect — STILL PRESENT at this
  measurement** (record sha `338918fc…` unchanged): the row cites
  `…A-shokunin-tradition.md:76` while its span occurs at A:86 (re-verified:
  span greps at A:86; A:76 is the "relevant distinction" sentence). No gate
  mode pairs a row's `path:line` with its span's occurrence line, so every
  composed verdict stays CLEAN; `claims-r9.jsonl` A11 pins A:86. A patch would
  move the record sha and require re-measuring. Named, not silently fixed.
- **Exempt items:** the 6 archive-record exemptions are justified (above);
  the general r3 limit stands — an exemption remains the author's declaration
  and the mode cannot check that a DIFFERENT exemption is truthful; this round
  audits exactly the archive records' instances.
- Carried debts apply (see Debt).

## Admission

[PARENT: ADMIT/REJECT line + commit hashes; no scalar; axis verdicts live in
SCORECARD.md's round-10 sections.]

## Debt

- **Receipt identity (round 1): STILL OPEN.** No authentic queue
  taskKey/expected receipt bag exists; mission acceptance is integrator-owned;
  no `task_…` value was invented, no shape-only receipt counted, proven
  receipt-backed completed rounds remain 0, operator target unchanged (≥100).
  Routing for this wave was satisfied by the operator's in-session direct
  dispatch; no Sighting step was invoked. Round-10 artifacts are lane evidence,
  not a mission receipt.
- **Controls:** landed within the polling window (first poll 05:41Z; measured
  05:43Z) — no gap to report; six controls, all six naming exactly their class
  (part 1 above). The controls README's own runs and this seat's fresh re-runs
  agree modulo `ts=`.
- Carried (unchanged by this round): absent!=drift omission limit (r6);
  non-vacuous flip screening (r5); id-shape boundary (r7); manifest schema
  growth; nested execution cost; non-author spot-check (integrator/operator);
  carried residuals (in-root hardlinks, no source size cap, token-aligned
  shortening, non-ASCII-adjacent fail-closed edges, scope-refusal finding IDs,
  frozen-replay comparator); usage/outside-path pin blind spot (r8);
  masked-set blind spots (r8); re-pin policy (r8); record claims-table `span`
  column outside every gate check (r9); `path#quote:text` structure-mode
  quirk (r9); reframing residual (r9); `A-r9.md:50` pointer-line defect (r9).
- **Ledger completeness (new, round 10):** `corpus/knowledge/hardening-r10.md`
  (sha `f5dc8889…`) is three rows short of its §3.9 completeness claim —
  in-root hardlink bypass, no source size cap, and the cosmetic banner
  `research-gate-r1` are named in the r2–r8 notes and the lesson
  (`…archive-scale-controls-and-ledger.md:110-112`) but have no row in
  §3.1–§3.9 while the claim sits at `:306-313`. Ledger-side, note-writer's
  file; fix = three rows + the counts/queue arithmetic (68 → ~71 rows; queue
  27 → ~30). Reported, not fixed.
- The full r2–r9 disposition otherwise lives in `corpus/knowledge/hardening-r10.md`
  (`f5dc8889…`); this section carries the round's own debts only.

## SHONEN

[PARENT: all four `[ ]` unless a named non-author verifier is bound this
round.]

Boundaries held: no gate change (sha identical to HEAD blob; diff empty);
corpus read-only (the archives are quoted, never written); seats write only in
owned paths; no commits by seats.