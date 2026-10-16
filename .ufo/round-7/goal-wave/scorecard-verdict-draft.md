# SCORECARD.md — round-7 draft sections (parent-owned file; [PARENT] binds)

<!-- SCRIBE DRAFT — MEASURED FINAL. Before: gate sha256
     0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8
     (== `git show 4835426:tools/research-gate.sh`; lane HEAD 4835426).
     After: gate sha256
     3ba718bf9207eed70c66b8c849ac43b44c76890785e1576eeb5e795a604166b2
     (+536/−20 vs HEAD; stable ≥2 min before this seat's battery, sha
     identical before and after it; the wave's revision history and the
     fixture reshape are documented in the report draft's Defect 2 and the
     fixture README). Lane HEAD still 4835426; no commits by any seat.
     Verdict vocabulary only: improved / unchanged / harmed /
     unprovable-but-better. No scalar scores. [PARENT] marks parent-only
     bindings. The admission section keeps the receipt-identity debt OPEN,
     per the mission contract. -->

Rounds 1–6 sections stay as written. These are the round-7 sections to
append, plus the admission/`Planned` refresh.

## Round-7 per-axis verdicts

Measurements: both sides measured fresh-process by the scribe seat; the
before side through an extracted copy of the committed r6 gate (race-free
while the working gate was mid-landing), the after side at the settled
revision with the sha identical before and after the whole battery.
Falsifiable claim: before, cross-section references are unvalidated and
dangling ids pass; after, a new `integrity` section inside `verify-all`
extracts every reference token (claim ids, source ids, sweep row ids) and
requires each to resolve to a DECLARED row/id or the Sources table —
`REF_UNRESOLVED` (drift) when not, counted when resolved, exempt classes
stay exempt-but-counted; `INTEGRITY refs=N resolved=M unresolved=K` joins
the composed verdict; selftest covers dangling-claim/dangling-source/
consistent/exempt/counting; all 64 prior cases byte-stable; zero network.

**Before** (gate `0c3d51ed…`, lane HEAD `4835426`): the r7 fixture twin
`integrity-r7-broken.md` (row 4 `from=S9`, SW3 `claim_id=C9`) composes CLEAN
`sections=4 run=4 drift-sections=0` — both dangling ids pass all six r1–r6
modes; four scratch single-cell dangling variants of `full-r6.md` likewise
compose CLEAN (`d1` Sweeps `claim_id`→Z9; `d2` hop `from`→C9; `d4` Claims
`sweep`→SW9; `d5` Negatives `sweep`→SW9), while the adjacent controls
`d3` (hop `to`→S9: structure+chain) and `d6` (sweep `where`→S9: sweeps)
already drift. No `INTEGRITY` string, no `REF_UNRESOLVED` finding id exists
at `0c3d51ed…` (both `grep -c` = 0).

**After** (gate `3ba718bf…`, selftest 74): `integrity-r7.md` composes CLEAN
`sections=5 run=5 drift-sections=0`, `SECTION integrity … tally=INTEGRITY
refs=16 resolved=15 unresolved=0` (exempt=1 measured in place: N2
`sweep=SW2` `observed=exempt … status=unresolved`); `integrity-r7-broken.md`
composes DRIFT `drift-sections=1 findings=2 drift=2` where integrity is the
ONLY drifting section and the two findings are exactly the planted ids
(`REF_UNRESOLVED kind=source id=S9 section=chain row=4 cell=from`;
`kind=claim id=C9 section=sweeps row=SW3 cell=claim_id`); the scratch classes
drift as named (d2/d3/d4/d5/d6 name their ids; d1 stays CLEAN because Z9 is
not id-SHAPED — the shape boundary, named) and non-local namings measure
exempt (`reason=non-local`: URL, `local://`); prior fixtures hold (full-r6
CLEAN; full-r6-broken DRIFT chain+sweeps with integrity CLEAN; full-r6-absent
CLEAN run=4 absent=1); regressions all held (claims 17/17 · chain 17/22 +
broken 1/2 · sweeps 1/2+3/3 + broken 0/1+0/1 · r1 archives 3/3); selftest
`PASS (74 cases)` with case lines 1–64 byte-identical; exit contract 0/1/2;
manifest append-only with `sections_run=5` and the integrity tallies; zero
network (strace: 0 of 7976 traced lines).

| Axis | Verdict | Evidence boundary |
|---|---|---|
| coverage | **improved** | The lane's last unchecked reference class is now verdict-bearing: claim ids, source ids and sweep row ids in cross-section cells resolve fail-closed (`REF_UNRESOLVED` on the id shapes; exempt classes counted), as a solo mode AND a fifth composed section — the twin's two dangling bindings that four r6 sections + structure pass now compose DRIFT through one run (before: CLEAN `run=4` on the same bytes measured through the committed r6 gate). |
| operability | **improved** | `verify-integrity <record>` (solo) + `SECTION integrity` in `verify-all` (`sections=5`); selftest 54→64→74 with case lines 1–64 byte-identical to the r6 receipt; priors byte-stable; exit contract 0/1/2 held (incl. `--json` path refusals); manifest line carries the integrity tallies + native string; zero network. |
| depth | **improved** [PARENT: r2–r6 precedent — each admitted scorecard credited the landed knowledge note under depth; the lesson landed (`corpus/lessons/2026-10-16-reference-integrity.md`, 19506 B, `8c047145…`), the note had not by 03:03Z when this seat last checked] | This seat re-derived the load-bearing observables independently (both fixture contracts, the class probes, the exempt-status boundary, counting arithmetic, the manifest record, selftest byte-stability) and they agree with the fixture README; the semantics (shape rule, resolution classes, exempt-status counting, non-local exemption) are documented in the gate header `:98-135`, the fixture README `:65-76`, and the round lesson. |
| freshness | **unchanged** | No drift detector added; the manifest records verification state (now 5 sections), it does not compare revisions. |
| calibration | **unchanged** [PARENT: the exempt-status semantics and the id-shape boundary are named, selftest-pinned (case 70) and measured; if integration reads that boundary-pinning plus the reshape record as a calibration gain, re-judge] | The boundary is named rather than hidden: exempt-status rows are counted exempt (`status=…`), non-local namings exempt (`reason=non-local`), non-id-shaped tokens not counted at all (d1 measured); the mid-wave reshape of the fixture pair (exempt hop → non-exempt `from` cell) is recorded in the fixture README `:65-76`, not silently tolerated. |
| adjacency | **unchanged** | Zero network (strace `-f -e trace=network`: 0 network lines of 7976); corpus read-only; no new write surface (verify-integrity is read-only; the `--json` append-only manifest is unchanged); seats wrote only in-lane. |

Scribe-found limits (measured; candidates for `Planned`/future rounds):

- **Id-shape boundary.** Only `S<digit>…` / `C|N<digit>…` / `SW<digit>…`
  tokens are references; `Z9` in a Sweeps `claim_id` cell is not counted
  (d1: CLEAN, refs drops by one). A dangling token that does not wear an id
  shape is invisible to integrity — named, not hidden.
- **Exempt-status semantics (pinned, was contested in-wave).** Exempt-status
  rows count their tokens exempt rather than requiring resolution (selftest
  case 70; N2 `sweep=SW2` measured in place). The first fixture shaping put
  the source defect behind such a row and measured one finding, not two; the
  fixture author re-shaped the pair to a non-exempt `resolved` hop, so both
  defect classes are now verdict-bearing regardless of that boundary.
- **Manifest schema growth.** `sections_run` is 5 and each integrity section
  object carries `tallies{refs,resolved,unresolved,exempt,findings,drift}`
  under the same `chousa-verify-all/v1` schema; round-6 prose/README rows
  that pinned `sections=4` read stale [PARENT].
- **Nested execution cost (carried).** A composed run now spawns up to five
  fresh gate processes.
- **Cosmetic (carried).** The banner still reads `research-gate-r1`.

## Round-7 learning trends

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | improved | New admitted specimens: `corpus/fixtures/integrity-r7.md` + `-broken.md` + `integrity-r7.claims.jsonl`/`-broken` + `integrity-r7.README.md` (pre-registered contract, before-state, reshape note); selftest +10 cases (65–74); lesson `corpus/lessons/2026-10-16-reference-integrity.md` (`8c047145…`); `SKILL.md` r7 rows (`99930459…` at check); [PARENT: note/`corpus/README.md`/receipts — not landed by 03:03Z when this seat last checked]. |
| quality | improved | The twin's two planted dangling bindings, invisible to all six r1–r6 modes (composed CLEAN, `run=4`, measured through the committed r6 gate), compose DRIFT through the integrity section alone with exactly two named findings; the exempt-class boundary is measured in place and case-pinned; the pre-registered contract is met at the settled revision. |
| discernment | unchanged | No non-author admit/reject spot-check exists; no criterion added. |

## Admission and continuation (round-7 replacement text)

[PARENT: refresh the round-6 admission paragraphs after integration.]

Local axis result: coverage improved (cross-section reference resolution is
now verdict-bearing as a solo mode + fifth composed section), operability
improved (selftest 64→74 with 1–64 byte-identical; `sections=5` composition;
manifest carries the integrity tallies), depth improved under the r2–r6 note
precedent [PARENT]; freshness/calibration/adjacency unchanged [PARENT: cells
above]; none harmed. Accepted limits, named rather than hidden: the id-shape
boundary; the exempt-status counting semantics (pinned by case 70 and
measured on N2's token) with the fixture reshape recorded; the manifest
`sections=5` schema growth; nested execution cost. No scalar substitute, no
promotion. [PARENT: adjust the axis cells if integration finds a landed
artifact disagreeing with a measured value, or if the gate moves past
`3ba718bf…`.]

Mission acceptance is separate and remains blocked on the round-1 receipt
identity: the interactive launch has no authentic queue taskKey/expected
receipt bag, so no `task_…` value may be manufactured, no shape-only receipt
counted, and no Sighting marked complete. Receipt-backed verified rounds
remain **0**; the operator target remains at least 100. Routing for this wave
was satisfied by the operator's in-session direct dispatch; no Sighting was
invoked. The round-7 artifacts are lane evidence, not a mission receipt.

Debt after round 7: receipt identity (integrator) — **STILL OPEN**; the
id-shape boundary; manifest schema growth [PARENT]; nested execution cost;
the absent!=drift omission limit (r6, still open); non-vacuous flip
screening (r5); non-author spot-check (integrator/operator); carried
residuals
(in-root hardlinks, no source size cap, token-aligned shortening,
non-ASCII-adjacent fail-closed edges, scope-refusal finding IDs,
frozen-replay comparator). Artifact ledger at draft time (uncommitted, at
the settled gate): gate `3ba718bf…` (+536/−20), fixtures + README (shas
above), lesson `8c047145…`, `SKILL.md` rows `99930459…` [PARENT: note
`corpus/knowledge/reference-integrity-r7.md`, receipts, `corpus/README.md` /
`corpus/evidence/README.md` rows when they land]. Integrate only what lands.
See `.ufo/round-7/goal-wave/report-draft.md` for owners.

## Planned (round-7 refresh)

[PARENT: replace the round-6 `Planned` paragraph.] Round 7's registered move
(binding integrity — cross-section references resolve fail-closed) ran in the
operator's in-session wave and is measured (the two-side contract above).
Round 8 registered: [PARENT: proposed candidates — (a) record-type
obligations / the omission limit's finer half (a record that SHOULD carry a
section but does not; named since r6); (b) the id-shape/reference-syntax
boundary (d1 measured) and path-form references; (c) manifest schema
versioning for future sections. Choose one falsifiable move.] Any next round
must again declare its own falsifiable single move and genuine scope before
dispatch; do not rerun this round's wave. Standing lane candidates: the
residuals named under Debt.