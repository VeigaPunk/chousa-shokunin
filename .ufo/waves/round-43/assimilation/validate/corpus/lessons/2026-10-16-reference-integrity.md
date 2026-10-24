# Round-7 lesson — reference integrity: an id-shaped cross-section reference must resolve to a declared row, and the exempt-status boundary is where that stops (2026-10-16 UTC)

Round: chousa-shokunin round 7, one coverage-of-integrity move: cross-section
reference integrity — a new `integrity` section inside `verify-all` extracts
reference tokens (claim ids, source ids, sweep row ids) and requires each
id-shaped token to resolve to a DECLARED row/id (Sources/Claims+Negatives/
Sweeps declarations, or the Sources table); an undeclared one is
`REF_UNRESOLVED` (drift); resolved and exempt references are counted;
`INTEGRITY refs=N resolved=M unresolved=K` joins the composed verdict. Lane
HEAD `4835426` (round-6 records; no commits by this seat). Gate under test —
before: `tools/research-gate.sh` sha256
`0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8`
(committed at HEAD, recoverable as `git show HEAD:tools/research-gate.sh`);
after: sha256
`3ba718bf9207eed70c66b8c849ac43b44c76890785e1576eeb5e795a604166b2`
(working tree, uncommitted). Fixtures under test: `corpus/fixtures/integrity-r7.md`
sha256 `4310ce86aa45f3d7d4b7d04c4ebf480a7b59748510ab0f132c5411dd8acd1b1b`,
twin `integrity-r7-broken.md`
`fd4e213f03faf9a76bbca3896b11fe6530878e727fefb974043ffb4a9f9a05b8`,
companions byte-identical `8e83b23d04e92961f7781e556d600b94a313e083c79d32a517fcb16ec17dabb3`;
pre-registration `integrity-r7.README.md` (its before-state excerpt matches
this seat's independent r6 runs below). An earlier revision of the pair
(source defect behind an exempt hop, shas `e2dfc7de…`/`7af72514…`) was
re-shaped by the fixture seat after the exempt reading below was measured —
the shas above are the bytes this lesson measures.
verified-at: 2026-10-15/16 ~02:36-03:02Z, from the lane cwd, fresh processes,
`--root ..`, local reads only; nothing fetched; the only subprocesses are the
gate's own section invocations; zero network (strace below). Gate sha
re-checked before and after every battery block below.
recheck:
`bash tools/research-gate.sh verify-all corpus/fixtures/integrity-r7.md --root ..`
· `bash tools/research-gate.sh verify-all corpus/fixtures/integrity-r7-broken.md --root ..`
· `bash tools/research-gate.sh verify-integrity corpus/fixtures/integrity-r7-broken.md --root ..`
· `bash tools/research-gate.sh --selftest`

Raw probe outputs, pinned r6 gate copy (`gate-r6.sh`), before/after case
lists and manifest scratch: `/tmp/chousa-lessons-r7/`. This seat wrote no
lane file outside `corpus/lessons/`. All script line numbers below are
relative to `3ba718bf…` unless the revision is named at the point.

## The claim, and the hole it names

**Before**, a record's cross-section references were checked only where a
mode happened to read the cell, and several cells were read in one direction
only. Measured at `0c3d51ed…` (each probe a copy of `full-r6.md` with one
cell edited, composed run `verify-all --root ..`):

| # | dangling reference (single-cell edit) | at `0c3d51ed…` |
|---|---|---|
| 1 | Sweeps `SW1 claim_id` `N1` → `N99` (undeclared) | CLEAN exit 0 |
| 2 | Sweeps `SW1 claim_id` `N1` → `C9` (undeclared claim id) | CLEAN exit 0 |
| 3 | Chain hop 1 `from` `C1` → `C99` (undeclared) | CLEAN exit 0 |
| 4 | Negatives `N1 sweep` `SW1` → `SW9` (undeclared) | CLEAN exit 0 |
| 5 | Claims `C1 sweep` `` → `SW9` (undeclared) | CLEAN exit 0 |
| 6 | Chain hop 1 `to` `S1` → `S9`, status `resolved` (control) | DRIFT exit 1 — already checked by r3/r5 (`CHAIN_HOP_UNRESOLVED` + `CHAIN_SOURCE_MISSING`) |
| 7 | Chain hop 1 `to` → `S9`, status `resolved` → `blocked-no-fetch` (exempt) | CLEAN exit 0 |

Reading the mechanism at `0c3d51ed…` (observation, matches the measurements):
the sweeps mode never reads a sweep row's `claim_id`
(`tools/research-gate.sh:1600-1614` at that revision), the chain mode reads
`to=` but not `from=` (`:1236`), the negatives/claims pass checks only that
the sweep cell is non-empty (`:631`; `:587-608` link claim→sweep, never
validate the sweep's value), and an exempt chain status skips the row
entirely (`:1287-1289`) including its `to=`. The round's own fixture pair
pins the hole: at `0c3d51ed…` BOTH pair records compose CLEAN, exit 0,
sections=4, with identical tallies (chain `RESOLVED_HOPS=4/4`, sweeps
`VERIFIED_SWEEPS=2/3 REJECTIONS_OK=2/2`) — the twin's two planted dangling
references are invisible to all six landed modes, and its hop-4 anchor even
VERIFIES (`verify-chain`: `CHAIN hop=4 status=resolved observed=verified
source=chousa-shokunin/corpus/knowledge/archived-export-intake.md
anchor=line:"this record is declaration-and-pointer-level acceptance only"
at=line:11 verdict=match`).

Verbatim (before, the twin, current pair bytes, pinned r6 gate):

```text
$ bash /tmp/chousa-lessons-r7/gate-r6.sh verify-all corpus/fixtures/integrity-r7-broken.md --root ..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=4/4
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=2/3 REJECTIONS_OK=2/2
VERIFY_ALL sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0)
exit=0
```

## What landed — the rule at `3ba718bf…`

A new mode `verify-integrity <record> --root …` (usage `:212`; header docs
`:101-150`) and a fifth composed section. Semantics as landed:

- **Declared sets** (`:1782-1801`): `SRC_IDS` from `## Sources` ids,
  `CLAIM_IDS` from `## Claims` ids plus `## Negatives` ids, `SWEEP_IDS`
  from `## Sweeps` ids.
- **Classification** (`integ_token`, `:1733-1748`): a token that is in a
  declared set is `resolved` (the kind names which set matched); else an
  id-shaped token is `unresolved` by shape (`^[CN][0-9]…` claim,
  `^SW[0-9]…` sweep, `^S[0-9]…` source, `:1738-1740`); else a non-local
  location token (`sweep_token_class` nonlocal — URLs etc.) is `exempt`
  with `reason=non-local` (`:1741`); anything else (prose, local paths,
  globs, sentinels) is not a reference token and is not counted.
- **Exempt status** (`:1743-1745`): a token on a row whose status is in
  {`unresolved`, `blocked-no-fetch`, `rejected`, `labelled-dead`,
  `not-applicable`} is counted `exempt verdict=exempt status=<st>` — even
  when it is id-shaped and undeclared. This is the named boundary: it is
  the ONE place the fail-closed reading is deliberately relaxed (below).
- **Emission** (`integ_emit_ref`, `:1717-1731`): one
  `REF kind=… id=… section=… row=… cell=… observed=resolved|unresolved|exempt verdict=…`
  line per token; `unresolved` additionally emits
  `FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=… id=…
  section=… row=… cell=…` (`:1727-1728`).
- **Cells read** — chain `from`, `claim`/`claim_id`/`claim-id`, and `to`
  (fragment cut) (`:1816-1819`); claims `sweep`, `source`/`src`/`source_id`,
  `ref`/`reference`/`cite`, and `pointer` (`:1828-1831`); negatives `sweep`
  and `where` (`:1845-1846`); sweeps `claim_id` and `where` (`:1860-1861`);
  rejections `ref` (`:1870`). Path-shaped pointer/where cells classify as
  local → not tokens (so the pair's 16 refs are all id/non-local tokens).
- **Summaries** (`:1877-1879`): `INTEGRITY refs=N resolved=M unresolved=K`
  and `RESEARCH_GATE: CLEAN|DRIFT (refs=N resolved=M unresolved=K exempt=E
  findings=F drift=D)`; DRIFT iff `K>0`. Counting identity:
  **refs = resolved + unresolved + exempt**.
- **Composition** (`:1952`, `:1980`, `:2030-2034`, `:2044`):
  `VA_ORDER=(structure claims chain sweeps integrity)`; integrity runs when
  at least one other section has a surface (so a claims-JSONL input still
  runs it); its native tally is the `INTEGRITY refs=…` line; the composed
  line becomes `VERIFY_ALL sections=5 run=N absent=N drift-sections=N …`.
  The composed run prints the integrity section's SECTION line plus its
  FINDING lines only — the per-`REF` detail lines appear in the solo mode's
  stdout.
- **Exit contract unchanged**: 0 CLEAN / 1 DRIFT / 2 setup; `--claims`/
  `--json` remain verify-all-only (`:3636`).
- **Selftest family** (`:3363-3595`; runners `:2319`, `:3246`): cases 65-74.

## Evidence (battery at `3ba718bf…`, sha re-checked identical before and after)

The pair, after — the twin composes DRIFT with the integrity section the
ONLY drifting section and exactly the two pre-registered findings:

```text
$ bash tools/research-gate.sh verify-all corpus/fixtures/integrity-r7-broken.md --root ..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=4/4
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=2/3 REJECTIONS_OK=2/2
SECTION integrity state=run verdict=DRIFT findings=2 drift=2 tally=INTEGRITY refs=16 resolved=13 unresolved=2
FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=source id=S9 section=chain row=4 cell=from
FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=claim id=C9 section=sweeps row=SW3 cell=claim_id
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=2 drift=2
RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=2 drift=2)
exit=1
```

The positive composes CLEAN with every reference resolved:

```text
$ bash tools/research-gate.sh verify-all corpus/fixtures/integrity-r7.md --root ..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=4/4
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=2/3 REJECTIONS_OK=2/2
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=16 resolved=15 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0)
exit=0
```

Every before-hole probe now drifts, each naming its exact cell (composed
findings, `ts=` elided; solo `REF` detail for the exempt probe below):

| probe | after verdict | `REF_UNRESOLVED` obs |
|---|---|---|
| 1 sweep `claim_id=N99` | DRIFT, drift-sections=1 | `kind=claim id=N99 section=sweeps row=SW1 cell=claim_id` |
| 3 hop `from=C99` | DRIFT, drift-sections=1 | `kind=claim id=C99 section=chain row=1 cell=from` |
| 4 negative `sweep=SW9` | DRIFT, drift-sections=1 | `kind=sweep id=SW9 section=negatives row=N1 cell=sweep` |
| 6 hop `to=S9` (resolved) | DRIFT, drift-sections=3 (structure + chain + integrity) | `kind=source id=S9 section=chain row=1 cell=to` |
| 7 hop `to=S9` behind `blocked-no-fetch` | **CLEAN**, `refs=13 resolved=10 unresolved=0` | none — `REF kind=source id=S9 … observed=exempt verdict=exempt status=blocked-no-fetch` |

The untouched r6 material and the two r6 controls keep their verdicts; the
integrity section is additive:

| input | composed at `3ba718bf…` | r6 sections' tallies |
|---|---|---|
| `full-r6.md` | CLEAN, `run=5`, integrity `refs=13 resolved=12 unresolved=0` | unchanged |
| `full-r6-broken.md` | DRIFT, `drift-sections=2` (chain + sweeps), integrity CLEAN | unchanged (2 findings as at r6) |
| `full-r6-absent.md` | CLEAN, `run=4 absent=1`, integrity runs `refs=2 resolved=2` | unchanged |

Selftest: `RESEARCH_GATE_SELFTEST: PASS (74 cases)` exit 0; the first 64
`ok-case` lines are BYTE-IDENTICAL to the pinned before-run
(`/tmp/chousa-lessons-r7/before-ok-cases.txt` sha256
`f881211943fc8cdaaed9c2056c4bf3013fe55228b57a94afb262c30336d2806d`; `cmp`
clean). New cases: 65 `integrity-pass` 0, 66 `integrity-fail-dangling-claim`
1, 67 `integrity-fail-dangling-source` 1, 68 `integrity-fail-dangling-chain-claim`
1, 69 `integrity-fail-dangling-sweep` 1, 70 `integrity-exempt-counted` 0, 71
`integrity-fail-counting` 1, 72 `setup-integrity-no-path` 2, 73
`setup-integrity-missing-file` 2, 74 `all-dangling.md` 1 (composed
`SECTION integrity state=run verdict=DRIFT … tally=INTEGRITY refs=4
resolved=3 unresolved=1` with the four r6 sections CLEAN).

Manifest (`--json`, append-only, unchanged schema `chousa-verify-all/v1`):
the line now carries the integrity tallies
(`{'refs': 13, 'resolved': 12, 'unresolved': 0, 'exempt': 1, 'findings': 0, 'drift': 0}`)
alongside the five sections. Zero network: `strace -f -e trace=network`
around a composed run — **0** socket/connect/sendto/recvfrom lines in 7976
trace lines, exit 0. Gate sha stable at `3ba718bf…` across the whole battery
and re-checked at writing.

## What held unchanged

- The four r6 sections' verdicts and tallies for every fixture run here are
  identical to the r6 receipt (`corpus/evidence/compose-r6-20261016T020330Z-*`,
  `sweeps-r5-…`, the r6 lesson's table); the selftest's 64 prior cases are
  byte-stable — including the claims `17/17`, chain `17/22`, sweeps
  `1/2 REJECTIONS_OK=3/3` regressions carried inside them.
- Boundary policy, exit contract, secrecy scanning, and the absent-not-drift
  composition rule are untouched; zero network; corpus read-only; no commits
  by this seat.

## Method statement — what an integrity CLEAN establishes, and what it does not

An integrity CLEAN establishes: every id-shaped token in the cells the
extractor reads either names a declared row in THIS record's sections or is
exempt by a named class, and the counters account for every extracted
reference (`refs = resolved + unresolved + exempt`); no declared row was
invented to satisfy a reference, and no reference was silently dropped.

It does NOT establish:

- **Name resolution, not type correctness.** The check is membership in the
  union of declared ids. A sweeps row's `claim_id` cell holding a SOURCE id
  resolves (`REF kind=source id=S1 section=sweeps row=SW1 cell=claim_id
  observed=resolved` — the impl's own selftest case 70 pins exactly this).
  Naming the wrong kind of row is not drift.
- **Truth of the referenced rows.** A declared row can be wrong; integrity
  re-reads nothing. The twin's hop-4 anchor still VERIFIES while its `from`
  reference drifts — reference integrity is orthogonal to anchor existence,
  which is why the composed run can name both a CLEAN chain section and an
  integrity finding on the same row.
- **The exempt-status class — the named boundary.** A token on a row whose
  status is exempt is counted exempt even when undeclared (probe 7: an
  undeclared `S9` behind `blocked-no-fetch` composes CLEAN,
  `unresolved=0`). The round's pair deliberately carries its two defects on
  NON-exempt rows and its README records that an earlier pair revision put
  the source defect behind an exempt hop and was re-shaped after the exempt
  reading was measured. The relaxed class is visible in the count
  (`exempt=`), not hidden; a future move could require exempt rows'
  references to resolve too, at the cost of forcing source ids onto rows
  whose probe is honestly skipped.
- **Cell coverage beyond the extractor's list.** Only the cells listed above
  are read; a reference token placed in a cell no extractor names (e.g. a
  notes column) is not counted at all. The `## Rejections ref` cell is read
  (`:1870`) but a path there is not a token.
- **Anything about the schema's other obligations.** Absence semantics,
  omissions, and record-type obligations remain as r6 named them.

## Defects and follow-ups noted (outside this seat's write scope)

- **Writing-window churn (acceptance-timing discipline, again).** After the
  integrity section first appeared, the gate moved through at least six
  revisions while this wave ran: `cbd14302…` → `7ad8f8a6…` → `f79b40ad…` →
  `b7f6ddd5…` → `6dc7fba4…` → `3ba718bf…` (plus earlier WIP revisions
  `9dcc83d5…`/`99d74d45…` where the composed run printed NO integrity line
  and `--selftest` failed 1/64 on case 55 — transient states, recorded
  because they were real at their revisions, not defects of the settled
  revision). Acceptance must pin `3ba718bf…`; this lesson measures only that
  revision.
- **Fixture re-shaping (attribution: fixture seat, recorded in the README).**
  The pair's earlier revision (shas `e2dfc7de…`/`7af72514…`, exempt-hop
  defect) is superseded; this seat's before-measurements of the FINAL bytes
  are the ones quoted above. The README's own before-excerpt agrees with
  them.
- **Carried residuals from earlier rounds (unchanged here):** in-root
  hardlinks bypass path canonicalization; no source size cap; the banner
  still reads `research-gate-r1` (cosmetic).
- **Receipt identity (round 1) — STILL OPEN.** These are lane-local evidence
  runs, not queue taskKey/expected-receipt bags; no `task_…` value may be
  invented and no Sighting is claimed. No scalar score, no promotion, no
  field-readiness claim. No commits by this seat.

## Gate

### Candidates

1. This lesson.
2. The reading "an integrity CLEAN proves the record's cross-section
   references are type-correct".
3. The reading "an exempt status excuses a dangling reference" (or its
   inverse, "nothing behind an exempt status is checked").
4. The reading "`refs=N` counts every reference in the record".
5. A new `corpus/QUALITY.md` criterion from this round's rejections.
6. Promotion marks / SHONEN boxes.

### Admitted

- Candidate 1, this note
  (`corpus/lessons/2026-10-16-reference-integrity.md`).

### Rejected, with reasons

- Candidate 2 — overclaim; measured: a `claim_id` cell resolving to a source
  id is `observed=resolved` (selftest case 70, `REF kind=source id=S1
  section=sweeps row=SW1 cell=claim_id`). The check is membership, not type.
- Candidate 3 — half-true and therefore misleading in both directions: an
  exempt STATUS row's tokens are counted exempt even when undeclared (probe
  7, CLEAN), but the row's anchor is still probed by its own mode (the
  twin's hop-4 anchor verifies while its reference drifts), and non-exempt
  rows are fully required to resolve. The precise statement is the
  exempt-status boundary above.
- Candidate 4 — overclaim; `refs` counts only id-shaped and non-local tokens
  in the extractor's cells: the pair records carry 16 refs while dozens of
  path cells (pointers, where-globs, rejection refs) are not tokens at all.
- Candidate 5 — no QUALITY-bar miss produced this round's rejections.
- Candidate 6 — refused; this seat grants nothing and no non-author
  spot-check exists.

### Spot-check

**Unavailable — measured outcome, not omission** (as in rounds 1-6: every
reviewer is a lane seat; no non-author sampled an admit and a reject).
Discernment remains unchanged.

## Verification boundary (parent-owned)

Integration counts, commit hashes, the round report/SCORECARD/LOG entries and
any frozen-replay evidence are parent-owned; nothing here pre-claims them. The
before/after pair measured here is `0c3d51ed…` (committed at HEAD `4835426`)
→ `3ba718bf…` (working tree, uncommitted at this writing, sha-stable across
the battery and re-checked at writing). Mission acceptance remains blocked on
round-1 receipt identity (still open); no `task_…` value is invented and no
receipt was counted. Later corrections land as append-only errata blocks
(`QUALITY.md:4`).