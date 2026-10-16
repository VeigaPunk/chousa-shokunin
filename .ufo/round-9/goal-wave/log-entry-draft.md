# LOG.md — round-9 entry draft (parent-owned file; integrate under [PARENT] markers)

<!-- SCRIBE DRAFT — MEASURED FINAL as of the fixture landings (records 01:35,
     claims fixture 01:31, archives-r9 README 01:37 local; receipts, note,
     SKILL/README rows integrate as landed). Gate sha256
     46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd on both
     sides (== HEAD `f11073a` blob; working-tree sha identical before and after
     the battery; `git diff --numstat tools/research-gate.sh` EMPTY —
     fixture-led round, no gate change by design; a change without a reported
     defect would itself be a finding). Lane HEAD still `f11073a`; no commits
     by any seat. Scribe scratch $HOME/.cache/chousa-tmp/scribe-r9/ (declared
     ephemeral, cleaned at end of run). [PARENT] marks parent-only bindings.
     The debts section keeps the receipt-identity debt OPEN per the mission
     contract. -->

## 2026-10-16 — round-9 coverage (fixture-led): the three archived inputs through verify-all as records

Round 9 executes the move round 8 registered: **fixture-depth coverage** — the
three archived research inputs run through `verify-all` end to end as RECORDS,
with expanded claim/hop fixtures. The operator dispatched this wave directly
in-session (same routing as rounds 2–8; **no Sighting step was invoked**);
receipt identity from round 1 remains open and untouched by this round. The
round is fixture-led by design: **no `tools/research-gate.sh` change** —
measured, not assumed (working-tree sha == HEAD blob, diff empty before and
after the battery).

**Before (MEASURED at gate `46f5ddb3…`, lane HEAD `f11073a`):**

```text
$ git show HEAD:tools/research-gate.sh | sha256sum → 46f5ddb3… (== working tree; git diff EMPTY)
$ bash tools/research-gate.sh --selftest           → RESEARCH_GATE_SELFTEST: PASS (85 cases) exit=0
$ ls corpus/fixtures/ | grep -i archive            → (none)

$ r1 observable (verify, --root ..): A/B/C each exit=1 with exactly one
  RESEARCH_GATE: DRIFT line (findings=6 drift=5); counting command → VERDICT_BEARING_EXPORTS=3/3

$ verify-all on a raw archive → DRIFT (sections=5 run=2 absent=3 drift-sections=1 findings=6 drift=5):
  structure DRIFT (RECORD_SCHEMA_INVALID, EXPORT_CHROME_PRESENT info, NO_QUESTION,
  SOURCE_TABLE_ABSENT, CLAIM_TABLE_ABSENT, REJECTION_DROPPED); claims/chain/sweeps absent;
  integrity CLEAN refs=0 — an export is not a record, so nothing composes.

$ verify-claims corpus/fixtures/claims-r2.jsonl → VERDICT_BEARING_CLAIMS=17/17 CLEAN exit=0
  archive-citing claims: A 6 · B 5 · C 6
$ verify-chain corpus/fixtures/chain-r3.md → RESOLVED_HOPS=17/22 CLEAN exit=0 (all hops cite S1/S2/S3)

archive byte pins: A 9033857d… (6474 B) · B 6d8dbddd… (5364 B) · C e48fe70f… (8922 B)
```

**The move.** Fixture-led; no gate change. Landed under
`corpus/fixtures/archives-r9/`: the three records — `A-r9.md` (7210 B, sha256
`338918fcb8ed5d6c5f15dc64e5eb8a3ae7a005d51b5c03e7e377c1dab9173c78`), `B-r9.md`
(7118 B, `abfa5290deda4d1708ba97028853b8a770f16ecda6f377dddda53d49cb2e3e86`),
`C-r9.md` (8021 B, `97be0e69ccfb8a701bc5556f738553be8e7179c9b41110fe61c4a3cab4f2d1da`)
— each `research-record v1` (Meta window loopback / fetch none / claims_file
binding / archive + archive_sha256 pins; Question; Sources with the archive as
S1 tier `export` and the external works as named-only `secondary` rows; Chain
A 7 / B 7 / C 8 hops; Claims A 5 / B 6 / C 8 rows with span cells; Negatives
N1; Sweeps SW1; Rejections A 4 / B 3 / C 4 with reason + flip_condition), plus
`README.md` (pins, re-run recipe, coverage before→after, the reframing-risk
section, authoring notes). Also landed: `corpus/fixtures/claims-r9.jsonl`
(+ README; `f6f0d1ab…`, 3601 B) — 10 new archive-citing claims beyond r2's 17
(A07–A11, B06–B08, C07–C08).

**Measurements after the move** (gate `46f5ddb3…`; fresh processes; verbatim):

```text
$ bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/A-r9.md --root ..
  SECTION structure state=run verdict=CLEAN findings=0 drift=0
  SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=10/10
  SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=6/7
  SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=4/4
  SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=13 resolved=12 unresolved=0
  VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0
  RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0) exit=0
$ B-r9.md → CLEAN sections=5 run=5; chain 6/7; REJECTIONS_OK=3/3; integrity refs=14 resolved=13 unresolved=0; exit=0
$ C-r9.md → CLEAN sections=5 run=5; chain 7/8; REJECTIONS_OK=4/4; integrity refs=15 resolved=14 unresolved=0; exit=0
  (the round predicted CLEAN "modulo documented integrity findings"; measured: no integrity
  finding exists on any record — each record's 1 exempt ref is its blocked-no-fetch chip hop:
  コトバンク / arxiv.org / jstage.jst.go.jp)

$ verify-claims claims-r9.jsonl → VERDICT_BEARING_CLAIMS=10/10
  RESEARCH_GATE: CLEAN (claims=10 supported=7 contradicted=2 unsupported=1 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0) exit=0

independent re-checks (python on raw bytes; separate mechanism):
  claims JSONL: 27 spans (17 r2 + 10 r9) — 24 byte-present; the 3 misses are exactly the
    by-design unsupported controls (A06, B05, C07); zero r2–r9 span overlap; totals A 11 · B 8 · C 8
  record content: 19/19 chain anchors + 19/19 claims-table span cells byte-verbatim, zero misses
    (the claims-table span column is outside every gate check)
  inter-archive hops: 5 (A hop5→B, A hop6→C, B hop6→A, C hop6→A, C hop7→B) all verified
  README's no-cross-citation check re-derived: grep -cE 'deep-research|archive [ABC]|export [ABC]|
    A-shokunin|B-multiagent|C-rank' → 0/0/0 in the three archives
  coverage stats: 46 total claim-surface rows (17 + 10 + 19; round-9 delta 29); 22 hops
    (19 verified + 3 exempt); 3/3 sweeps verified; 11/11 rejections complete; integrity 42 = 39 + 3 + 0

regressions held (fresh processes, unchanged gate):
  claims-r2 17/17 CLEAN · chain-r3 17/22 CLEAN · r1 observable VERDICT_BEARING_EXPORTS=3/3 ·
  selftest PASS (85 cases) · tools/research-gate.sh sha 46f5ddb3… unchanged after the battery

note + lesson: corpus/knowledge/archives-verified-r9.md (observed `cf94795b…` at 01:47 local,
  revised once after first landing — use the landed sha) reproduces every tally
  above from the same record bytes; corpus/lessons/2026-10-16-verifying-conversion-not-original.md
  (`eb3fb817…`). One real fixture defect named by both and confirmed here: A-r9.md:50 (row C3)
  pointer :76 while its span occurs at A:86 (claims-r9 A11 pins :86) — no gate mode pairs a
  row's path:line with its span's occurrence line.
```

**Named limits.** The reframing risk (record-format distortion) is named and
mitigated in `corpus/fixtures/archives-r9/README.md` §"Reframing risk" and
re-derived by this seat: a CLEAN verify-all "certifies record-format integrity
against archive bytes — not the external truth of anything the archives cite,
and not the completeness of their arguments"; mitigations include text-level
claims with verbatim spans, machine-extracted spans/anchors, `export`-capped
tiers, blocked chips unopened, corrections kept as rejections, convergences
labeled as such (no cross-citation measured 0/0/0). Residual distortion named,
not fixed: `text` cells paraphrase (read span+pointer, not prose); the exports
are cut mid-response; tallies grade anchor existence, not argument strength.
Two further observations from this seat: the record-format authoring
constraint measured by the fixture seats (`path#quote:text` in a `to` cell
drifts structure mode; the records use source ids/clean paths plus
`anchor_kind`/`anchor` columns instead), and the records' claims-table `span`
column resting on authoring discipline plus this seat's independent byte check
(no gate check covers it). A third, a real **fixture defect** at the measured
revision: `corpus/fixtures/archives-r9/A-r9.md:50` (row C3) cites
`…A-shokunin-tradition.md:76` while its span occurs at A:86 (verified here;
`claims-r9.jsonl` A11 and its README pin A:86) — found by the note/lesson's
independent 19-row audit (18/19), confirmed by this seat, invisible to every
gate mode (no mode pairs a row's `path:line` with its span's occurrence
line); a patch by the fixture seat moves the record sha and requires
re-measuring.

**Admission.** [PARENT: ADMIT/REJECT line + commit hashes; no scalar; axis
verdicts live in SCORECARD.md's round-9 sections.]

**Debt.** Receipt identity (round 1) STILL OPEN — no authentic queue
taskKey/expected receipt bag exists; mission acceptance is integrator-owned,
no `task_…` value was invented, proven receipt-backed completed rounds remain
0, operator target unchanged (≥100). New after round 9: the record-format
claims-table span outside gate verification; the `path#quote:text`
structure-mode drift quirk (documented, unfixed); the reframing residual
(named, not fixable within record fidelity). Carried debts: absent!=drift
omission limit (r6); non-vacuous flip screening (r5); id-shape boundary (r7);
manifest schema growth; nested execution cost; non-author spot-check
(integrator/operator); usage/outside-path pin blind spot (r8); masked-set
blind spots (r8); re-pin policy (r8); carried residuals (in-root hardlinks, no
source size cap, token-aligned shortening, non-ASCII-adjacent fail-closed
edges, scope-refusal finding IDs, frozen-replay comparator). Artifacts at draft time (uncommitted): records
`338918fc…`/`abfa5290…`/`97be0e69…`, archives-r9 README (`ec312657…`),
claims-r9 `f6f0d1ab…` + README (`64b63db6…`), lesson (`eb3fb817…`), note
`corpus/knowledge/archives-verified-r9.md` (observed `cf94795b…` at 01:47
local; revised once — use the landed sha) [PARENT: receipts,
`SKILL.md` rows, `corpus/README.md` row — integrate only what lands]. Lane
hygiene: no commits by seats.