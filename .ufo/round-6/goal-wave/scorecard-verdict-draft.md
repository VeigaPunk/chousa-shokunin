# SCORECARD.md — round-6 draft sections (parent-owned file; [PARENT] binds)

<!-- SCRIBE DRAFT — MEASURED FINAL. Verdict vocabulary only: improved /
     unchanged / harmed / unprovable-but-better. No scalar scores.
     Before: round-5 gate sha256
     55adb92d0ba5ac958907fac6c4d5d6b0b50129703e866a5befbd9a32789f2ff2
     (== `git show HEAD:tools/research-gate.sh`), lane HEAD 1d1f56c. After:
     round-6 gate sha256
     0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8
     (+450 lines vs HEAD; stable ≥9 min through this seat's whole battery,
     identical before and after it; earlier transient revisions in the wave
     were functionally defective on the record path and are documented in
     the round-6 note). Lane HEAD still 1d1f56c; no commits by any seat.
     Fixtures: `full-r6.md` 878c2c50…, `full-r6-broken.md` 0f7e498c…,
     `full-r6-absent.md` 39cdb2d7…, companions 45eb6ac2… (both),
     `full-r6.README.md` f56ef337…. Scribe scratch /tmp/chousa-scribe-r6/
     (declared ephemeral, cleaned at end of run). [PARENT] marks parent-only
     bindings. The report draft's debts section keeps the receipt-identity
     debt OPEN, per the mission contract. -->

Rounds 1–5 sections stay as written. These are the round-6 sections to
append, plus the admission/`Planned` refresh.

## Round-6 per-axis verdicts

Measurements: both sides measured fresh-process by the scribe seat.
Falsifiable claim: before, no composed verdict exists — a record's full
verification state requires running four modes separately and eyeballing
them, and no durable manifest records any of it. **Before** (gate
`55adb92d…`, lane HEAD `1d1f56c`): `verify-all <record> --root ..` → exit 2,
empty stdout, stderr `research-gate: multiple record paths` (the keyword
parses as a positional record path, then a second positional arrives — the
mode does not exist); `--json` → exit 2, `research-gate: unknown flag:
--json`; no manifest file exists anywhere in the lane; every verify mode is
zero-write at that revision (the only file redirections are inside
`run_selftest`'s mktemp dir, `tools/research-gate.sh:1634-1703`). The same
fixture bytes ran solo: r1 `verify` CLEAN `findings=0` on both
`sweeps-r5.md` and `sweeps-r5-broken.md`; `verify-chain` on `sweeps-r5.md`
`2/3` CLEAN; `verify-sweeps` `1/2 + 3/3` CLEAN (broken control DRIFT naming
both classes); `verify-claims claims-r2.jsonl` 17/17 CLEAN; selftest
`PASS (54 cases)`. **After** (`0c3d51ed…`): `verify-all` composes one
verdict over four sections (structure/claims/chain/sweeps). `full-r6.md`
(bare; its Meta `claims_file` row binds the companion) → CLEAN exit 0,
`VERIFY_ALL sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0`,
sections structure CLEAN · claims CLEAN tally `VERDICT_BEARING_CLAIMS=3/3` ·
chain CLEAN tally `RESOLVED_HOPS=3/3` · sweeps CLEAN tally
`VERIFIED_SWEEPS=1/2 REJECTIONS_OK=2/2`; `full-r6-broken.md` → DRIFT exit 1,
`run=4 absent=0 drift-sections=2 findings=2 drift=2`, naming exactly
`chain` (`CHAIN_ANCHOR_NOT_FOUND` hop=2 `nearest_line=57`) and `sweeps`
(`SWEEP_REJECTION_INCOMPLETE` id=R2 missing=flip) while structure and
claims stay CLEAN (3/3); `full-r6-absent.md` → CLEAN exit 0, `run=3
absent=1`, `SECTION claims state=absent`, sweeps run with tally
`VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1`; the claims JSONL passed as input →
CLEAN `run=1 absent=3`. Per-section tallies EQUAL the solo modes' outputs on
the same bytes (measured on all three records + `sweeps-r5.md` as an extra).
`--json` appended 5 lines to a scratch manifest: line 1 byte-stable across
every append (sha256 `9da468d8…`), the head-4 prefix byte-stable across the
5th append (`01fd1ccf…` before and after), every line `json.loads`-valid,
`record_sha256`/`gate_sha256` re-verified equal to the files, and `>>`
(`:1846`) is the only write site in any verify path. Selftest
`PASS (64 cases)` with the first 54 case lines byte-identical; every
prior-mode output byte-identical modulo `ts=`; exit contract 0/1/2 held (8
probes, including manifest-path refusals); zero network (strace
`-f -e trace=network`: 0 network lines). The lane receipt manifest
`corpus/evidence/verify-all-manifest.jsonl` (3 lines, gate `0c3d51ed…`,
sha256 `2ed28f9f…`) is the receipts seat's cut at the settled gate; the
receipts seat's five-log cut (`compose-r6-20261016T020330Z-*` under
`corpus/evidence/`) agrees with this seat's battery wherever they overlap —
same composed verdicts and per-section tallies, manifest lines 0→3 with
prefix compares YES, `PASS (64 cases)` with the first 54 case lines
byte-identical, 0 network syscalls.

| Axis | Verdict | Evidence boundary |
|---|---|---|
| operability | **improved** | One command composes the modes' verdicts into ONE `CLEAN\|DRIFT` under the existing 0/1/2 exit contract; `--json` appends the record's verification state (record+gate SHA-256, UTC, per-section state/verdict/tallies, composed verdict) to a manifest, making it durable instead of eyeballed; selftest 54 → 64 (+10 verify-all cases, 55–64) with cases 1–54 byte-identical; prior-mode outputs byte-identical modulo `ts=`; exit contract held |
| coverage | unchanged [PARENT: re-judge if integration counts one composed run over all four surfaces as expanded verified coverage; this seat reads the move as composition of existing checks, not a new assertion surface] | The composition runs the same predicates as the solo modes (the header's own rule: each section tally is that solo mode's tally by construction); the manifest records state, it checks no new content |
| depth | **improved** [PARENT: r2–r5 precedent — each admitted scorecard credited the landed knowledge note under depth] | `corpus/knowledge/verify-all-r6.md` (18403 B, sha `9b9711cb…`) documents the mode, the composition semantics, the manifest schema, the absence semantics/omission limit and the open items; lesson `corpus/lessons/2026-10-16-verify-all-composition.md` (22585 B, `d55bb183…`) adds the method statement and its own defect notes. This seat re-derived the load-bearing observables independently (composed verdicts + tallies on 3 records + `sweeps-r5.md`, 5 manifest appends, selftest 64, regressions, exit contract, strace); note/lesson agree with them |
| freshness | unchanged [PARENT: the manifest pins record+gate SHA-256 and UTC per run — if integration reads durable per-record pins as a freshness gain, re-judge; this seat reads SHA capture as state, not a cross-revision drift detector] | No drift detector added; the manifest records, it does not compare revisions |
| calibration | unchanged | The omission limit is named, not hidden: absent sections are reported (`SECTION <name> state=absent`) and never drift; the claims-surface omission and sweeps-with-only-rejections granularity are the fixture's named r7 questions. `VERIFY_ALL_SECTION_UNAVAILABLE` (sub-mode rc∉{0,1}) is a defensive path not triggered by the selftest or this seat's probes; no prior surface re-measured |
| adjacency | unchanged | Zero network (strace `-f -e trace=network`, 0 network lines on a composed `--json` run); corpus read-only; the ONE new write surface (`--json`) appends (`>>` only, `:1846`; no rewrite path) to any writable regular file whose dirname exists — no root/lane confinement inside the gate; the lane's receipts discipline keeps the manifest in `corpus/evidence/`. No locking/fsync/rotation (concurrent-append interleaving unmeasured) |

Scribe-found limits (measured; candidates for `Planned`/future rounds):

- **Omission limit (the r7 candidate).** Absence is reported, never drift —
  and the record's own `## Claims` rows are NOT the claims section: the
  claims section verifies the BOUND claims surface (itself for a claims
  JSONL, `--claims PATH`, or a Meta `claims`/`claims_file`/`claims-file`/
  `claimset` row). A record with Claims rows but no bound companion composes
  `claims state=absent` CLEAN (measured on `sweeps-r5.md` → CLEAN `run=3
  absent=1`). Nothing asserts an absent section should have been present.
- **Sweeps granularity nuance.** `sweeps` runs whenever `## Rejections`
  exists, even with zero sweep/negative rows (`full-r6-absent.md` → sweeps
  run, tally `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1`). The fixture README's
  absent-record bullet says "claims and sweeps reported absent" while its own
  pre-registered table matches this run behavior — wording nuance in the
  README, non-blocking.
- **Manifest write semantics.** The append happens before the verdict
  stdout; on append failure the run exits 2 with the gate's own
  `research-gate: manifest append failed: <path>` and prints no verdict
  (measured on a read-only target, plus bash's own `Permission denied`
  line). No path confinement, locking, fsync or rotation (above).
- **Display (cosmetic).** `structure`/`claims` SECTION lines carry no tally
  (the full counter dict lives in the manifest's `tallies`); the sweeps
  `where=` cell keeps the r5 80-character display cap.

## Round-6 learning trends

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | improved | New admitted specimens: `corpus/fixtures/full-r6.md` + `-broken.md` + `-absent.md` + two claims companions (sha `45eb6ac2…`) + `full-r6.README.md` (pre-registered expectations, inventory shas, composed-run section); the round-6 note and lesson; the `SKILL.md` `research-gate verify-all` row; the lane manifest specimen `corpus/evidence/verify-all-manifest.jsonl` (3 lines at the settled gate); the receipts seat's five receipt logs (`compose-r6-20261016T020330Z-*`) and the `corpus/README.md` + `corpus/evidence/README.md` round-6 rows/sections |
| quality | improved | The broken twin composes DRIFT naming exactly the two dirtied sections from ONE run (`chain` + `sweeps`) while r1 `verify` stays CLEAN on the same bytes — those defects previously required separate runs eyeballed together; before/after on the same fixture bytes, twin diff exactly 3 lines (2 planted defects + the companion `claims_file` row) |
| discernment | unchanged | No non-author admit/reject spot-check exists; no criterion added |

## Admission and continuation (round-6 replacement text)

[PARENT: refresh the round-5 admission paragraphs after integration.]

Local axis result: operability improved (one composed verdict over the four
modes + a durable append-only manifest + selftest 54→64 with prior cases
byte-stable); depth improved under the r2–r5 note precedent (landed note +
lesson) [PARENT]; coverage/freshness/calibration/adjacency unchanged
[PARENT: cells above]; none harmed. Accepted limit, named rather than
hidden: absent claims/chains/sweeps surfaces are reported and do not drift —
the omission limit — registered as the round-7 candidate; plus the manifest
boundaries and the untriggered `VERIFY_ALL_SECTION_UNAVAILABLE` path named
above. No scalar substitute, no promotion. [PARENT: adjust the axis cells if
integration finds a landed artifact disagreeing with a measured value, or if
the gate moves past `0c3d51ed…`.]

Mission acceptance is separate and remains blocked on the round-1 receipt
identity: the interactive launch has no authentic queue taskKey/expected
receipt bag, so no `task_…` value may be manufactured, no shape-only receipt
counted, and no Sighting marked complete. Receipt-backed verified rounds
remain **0**; the operator target remains at least 100. Routing for this wave
was satisfied by the operator's in-session direct dispatch; no Sighting was
invoked. The round-6 manifest lines are lane evidence, not a mission receipt.

Debt after round 6: receipt identity (integrator, still open); the omission
limit — absent sections pass as reported-not-drifted, named r7 candidate;
nested execution cost (one composed run spawns up to four fresh gate
processes — the note's design note); manifest boundary facts (no
confinement, no locking; named above); non-vacuous flip screening (r5 note
candidate, carried); non-author spot-check (integrator/operator); carried
residuals (in-root hardlinks, no source size cap, token-aligned shortening,
non-ASCII-adjacent fail-closed edges, scope-refusal finding IDs,
frozen-replay comparator, Claims-cell sweep references in `verify-sweeps`).
Artifact ledger at draft time (uncommitted, at the settled gate): gate
`0c3d51ed…` (+450), fixtures + README (shas above; alias companion names
pruned by their author), note `9b9711cb…`, lesson `d55bb183…`, `SKILL.md`
rows `834c9707…`, receipts manifest `2ed28f9f…` (3 lines) and the five
receipt logs `compose-r6-20261016T020330Z-{selftest,full,broken,json,live}.log`
(`e3b94e1c…`/`c96ac4f5…`/`83d7aef6…`/`1db37149…`/`ac4d3f8e…`), plus
`corpus/README.md` round-6 rows (`499d5f3a…`) and the
`corpus/evidence/README.md` round-6 receipts section (`ed94b72d…`) — the
last three landed after this seat's battery and agree with it where they
overlap. Integrate only what lands. See
`.ufo/round-6/goal-wave/report-draft.md` for owners.

## Planned (round-6 refresh)

[PARENT: replace the round-5 `Planned` paragraph.] Round 6's registered move
(composition: one `verify-all` verdict across the modes + the record's
verification state in the lane manifest) ran in the operator's in-session
wave and is measured. Round 7 registered: the omission limit — sections
absent from a record are reported but never drift, so a record can compose
CLEAN by omission; the next move must make omission itself reviewable under
a declared policy. Any next round must again declare its own falsifiable
single move and genuine scope before dispatch; do not rerun this round's
wave. Standing lane candidates: the r5 residuals named under Debt.