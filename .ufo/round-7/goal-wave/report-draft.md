# chousa — round 7: reference integrity — `verify-integrity` and the fifth composed section (coverage-of-integrity move)

<!-- SCRIBE DRAFT — MEASURED FINAL. Before: gate sha256
     0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8
     (== `git show 4835426:tools/research-gate.sh`; lane HEAD 4835426, round-6
     records), measured through an extracted copy to stay race-free. After:
     gate sha256
     3ba718bf9207eed70c66b8c849ac43b44c76890785e1576eeb5e795a604166b2
     (+536/−20 vs HEAD; stable ≥2 min before the battery per an independent
     watcher, and sha identical before and after the whole battery; the
     revision moved through ~11 hashes during the wave — see Defect 2).
     Lane HEAD still 4835426; no commits by any seat. The r7 fixture pair was
     revised mid-wave (first landing shas e2dfc7de…/7af72514…, settled
     4310ce86…/fd4e213f…; the README records the reshape). Scribe scratch
     $HOME/.cache/chousa-tmp/scribe-r7/ (declared ephemeral, cleaned at end of
     run). [PARENT] markers mark parent-only bindings. The Debt section keeps
     receipt identity OPEN per the mission contract. -->

Status: **DRAFT — measured, awaiting parent integration/admission**. Baseline:
lane HEAD `4835426` (round-6 records). Wave: one 32-seat flash call. Report
time: 2026-10-16 ~03:05Z.

## Work performed

- Round 7 selects the move round 6 registered: **coverage-of-integrity —
  reference integrity**. Before it, `verify-all` composed four sections that
  each checked their own rows, but nothing checked the REFERENCES between
  sections: a Sweeps row could name an undeclared `claim_id`, a Chain hop an
  undeclared `from` id, a Claims/Negatives `sweep` cell an undeclared sweep
  row id, and the composed verdict still read CLEAN (the round-6
  omission-hunter's demonstration; re-measured by this seat below).
- The move: a new SOLO mode `verify-integrity <record>` and a fifth
  `verify-all` section `integrity`. It resolves every cross-section reference
  token against the rows that declare it — source ids from `## Sources`,
  claim ids from `## Claims` and `## Negatives`, sweep ids from `## Sweeps` —
  read from chain `from`/`claim`/`to` (fragment cut), claims
  `sweep`/`source`/`src`/`ref`/`cite`/`pointer`, negatives `sweep`/`where`,
  sweeps `claim_id`/`where`, rejections `ref`/`reference`. An undeclared
  id-SHAPED token (`S<digit>…`, `C|N<digit>…`, `SW<digit>…`) is
  `REF_UNRESOLVED` (warn → drift); declared ids resolve; non-local namings
  (URLs, `local://…`, `artifact://…`, `agent://…`, `proc://…`, `history://…`,
  `external:`/`web:`/`live:`/`chat:`/`session:`) stay exempt
  (`reason=non-local`); local paths/glob/prose tokens are not references and
  are not counted; tokens of an EXEMPT-STATUS row
  (unresolved|blocked-no-fetch|rejected|labelled-dead|not-applicable; plus
  negatives/sweeps without `rejected`) are counted exempt, not required to
  resolve. Summary `INTEGRITY refs=N resolved=M unresolved=K` (exempt =
  N−M−K) becomes the section's native tally and joins the composed verdict;
  `verify-all` now prints `sections=5` and runs `integrity` whenever at least
  one other section runs. Selftest 64 → 74 (+10); cases 1–64 byte-identical;
  zero network.
- Scribe independent work: before-side probes at the extracted r6 gate
  (eight single-cell dangling/exempt variants — six of `full-r6.md`, two of
  the first `integrity-r7.md` bytes — plus the r7 fixture pair); the after-side
  battery at the settled gate (composed
  verdicts on the pair + all variants, solo `verify-integrity` REF-line
  captures, selftest byte-stability vs the r6 receipt, the full regression
  battery, exit-contract probes, manifest double-append, strace); these
  drafts.

## Landed changes (uncommitted, at draft time)

- `tools/research-gate.sh` → sha256 `3ba718bf…` (+536/−20 vs HEAD): solo mode
  `verify-integrity` (dispatch `:3390-3392`; helpers `integ_trim` `:1698`,
  `integ_emit_ref` `:1717`, `integ_token` `:1733`, `integ_cell` `:1750`,
  `verify_integrity` `:1764-1883`); finding id `REF_UNRESOLVED` in the header
  list `:27`; usage `:209`, `:242-254`; `verify-all` five-section order
  `VA_ORDER=(structure claims chain sweeps integrity)` `:1980`, applicability
  `:2027-2034` (runs whenever ≥1 other section runs), section subprocess
  `:2044`, `verify-integrity` native tally `:1952`, composed counters
  `sections=5` `:2109-2115`; selftest cases `:3336-3594` (7 `tintegrity` +
  2 `tsetup` + `tall all-dangling.md`). Banner still `research-gate-r1`
  (cosmetic, carried).
- Fixtures `corpus/fixtures/integrity-r7.md` (sha256 `4310ce86…`),
  `integrity-r7-broken.md` (`fd4e213f…`, twin — differs in 5 lines: two
  dangling cells + `claims_file`/`note`/`question` text),
  companions `integrity-r7.claims.jsonl` / `-broken` (`8e83b23d…`, one sha),
  `integrity-r7.README.md` (`df06b293…`) with the pre-registered contract,
  the before-state block, and the reshape note (Defect 2).
- Lesson `corpus/lessons/2026-10-16-reference-integrity.md` (19506 B, sha256
  `8c047145…`) — the round lesson (declared-id classes, the shape rule, the
  exempt-status boundary, the fixture reshape). `SKILL.md` r7 rows:
  `research-gate verify-integrity` added and `research-gate verify-all`
  updated to `PASS (74 cases)` / five-section ground truth (file sha
  `99930459…` at check).
- [PARENT: note `corpus/knowledge/reference-integrity-r7.md`, receipts, the
  `corpus/README.md` / `corpus/evidence/README.md` r7 rows — not landed by
  03:03Z when this seat last checked; integrate only what lands.]

## Before → after measurements

**Before (race-free, extracted copy `git show 4835426:tools/research-gate.sh`
= `0c3d51ed…`, sha re-verified on the copy):**

```text
$ r6-gate verify-all corpus/fixtures/integrity-r7.md --root ..            → CLEAN (sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0) exit=0
$ r6-gate verify-all corpus/fixtures/integrity-r7-broken.md --root ..     → CLEAN (sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0) exit=0
  twin sections: structure CLEAN / claims 3/3 CLEAN / chain RESOLVED_HOPS=4/4 CLEAN / sweeps VERIFIED_SWEEPS=2/3 REJECTIONS_OK=2/2 CLEAN
  the hole: BOTH planted dangling cells (chain row 4 from=S9; sweeps SW3 claim_id=C9) pass all six r1-r6 modes
  chain alone on the twin: CHAIN hop=4 status=resolved observed=verified source=chousa-shokunin/corpus/knowledge/archived-export-intake.md anchor=line:"this record is declaration-and-pointer-level acceptance only" at=line:11 verdict=match — the `from` cell is not read

scratch single-cell dangling variants of full-r6.md through the same r6 gate (one cell each; diffs verified):
$ r6-gate verify-all …/d1-sweep-claimid.md   → CLEAN run=4   (Sweeps SW1 claim_id: N1 → Z9)
$ r6-gate verify-all …/d2-hop-from.md        → CLEAN run=4   (Chain hop 3 from: C3 → C9)
$ r6-gate verify-all …/d4-claims-sweep.md    → CLEAN run=4   (Claims C1 sweep cell: '' → SW9)
$ r6-gate verify-all …/d5-neg-sweep.md       → CLEAN run=4   (Negatives N1 sweep cell: SW1 → SW9)
controls the r6 gate already catches:
$ r6-gate verify-all …/d3-hop-to.md          → DRIFT drift-sections=2 (structure CHAIN_HOP_UNRESOLVED + chain CHAIN_SOURCE_MISSING on to=S9)
$ r6-gate verify-all …/d6-sweep-where.md     → DRIFT drift-sections=1 (sweeps SWEEP_LOCATION_UNRESOLVED on where=S9)
$ grep -c 'INTEGRITY' tools/research-gate.sh → 0 ; grep -c 'REF_UNRESOLVED' → 0 at 0c3d51ed…
```

**After (gate `3ba718bf…`; sha stable ≥2 min before the battery and identical
before/after it; fresh processes; `ts=` elided):**

```text
$ verify-all corpus/fixtures/integrity-r7.md --root ..        (exit 0)
SECTION structure  state=run verdict=CLEAN findings=0 drift=0
SECTION claims     state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain      state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=4/4
SECTION sweeps     state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=2/3 REJECTIONS_OK=2/2
SECTION integrity  state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=16 resolved=15 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0)

$ verify-all corpus/fixtures/integrity-r7-broken.md --root ..  (exit 1)
SECTION structure  state=run verdict=CLEAN findings=0 drift=0
SECTION claims     state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain      state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=4/4
SECTION sweeps     state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=2/3 REJECTIONS_OK=2/2
SECTION integrity  state=run verdict=DRIFT findings=2 drift=2 tally=INTEGRITY refs=16 resolved=13 unresolved=2
FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=source id=S9 section=chain row=4 cell=from
FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=claim id=C9 section=sweeps row=SW3 cell=claim_id
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=2 drift=2
RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=2 drift=2)
  → the integrity section is the ONLY drifting section; the two planted ids are the only findings; the pair's pre-registered broken contract is met.

$ verify-integrity corpus/fixtures/integrity-r7.md --root ..   (exit 0; 16 REF lines; decisive rows verbatim)
REF kind=claim id=C3 section=chain row=4 cell=from observed=resolved verdict=match
REF kind=source id=S4 section=chain row=4 cell=to observed=resolved verdict=match
REF kind=sweep id=SW2 section=negatives row=N2 cell=sweep observed=exempt verdict=exempt status=unresolved
REF kind=claim id=C2 section=sweeps row=SW3 cell=claim_id observed=resolved verdict=match
INTEGRITY refs=16 resolved=15 unresolved=0
RESEARCH_GATE: CLEAN (refs=16 resolved=15 unresolved=0 exempt=1 findings=0 drift=0)

$ verify-integrity corpus/fixtures/integrity-r7-broken.md --root ..  (exit 1)
REF kind=source id=S9 section=chain row=4 cell=from observed=unresolved verdict=mismatch
REF kind=claim id=C9 section=sweeps row=SW3 cell=claim_id observed=unresolved verdict=mismatch
FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=source id=S9 section=chain row=4 cell=from
FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=claim id=C9 section=sweeps row=SW3 cell=claim_id
INTEGRITY refs=16 resolved=13 unresolved=2
RESEARCH_GATE: DRIFT (refs=16 resolved=13 unresolved=2 exempt=1 findings=2 drift=2)

scratch class probes at the settled gate (composed section line unless noted):
base (full-r6 bytes)                       → integrity CLEAN refs=13 resolved=12 (exempt=1: N2.sweep)
d1 Sweeps claim_id → Z9                    → integrity CLEAN refs=12 resolved=11 — Z9 is NOT id-shaped: not a reference, not counted (shape rule)
d2 Chain hop 3 from → C9                   → integrity DRIFT 1 finding: kind=claim id=C9 section=chain row=3 cell=from
d3 Chain hop 3 to → S9                     → DRIFT drift-sections=3 — structure + chain + integrity all name S9 (integrity: kind=source id=S9 row=3 cell=to)
d4 Claims C1 sweep → SW9                   → integrity DRIFT 1 finding: kind=sweep id=SW9 section=claims row=C1 cell=sweep
d5 Negatives N1 sweep → SW9                → integrity DRIFT 1 finding: kind=sweep id=SW9 section=negatives row=N1 cell=sweep
d6 Sweeps SW2 where → S9                   → DRIFT drift-sections=2 — sweeps SWEEP_LOCATION_UNRESOLVED + integrity kind=source id=S9 row=SW2 cell=where
d7 Sweeps SW3 claim_id → https URL         → integrity CLEAN: REF kind=location id=https://example.com/some-census … observed=exempt verdict=exempt reason=non-local
d8 Chain hop 4 to → local://artifact-x     → integrity CLEAN: REF kind=location id=local://artifact-x … observed=exempt verdict=exempt reason=non-local
prior fixtures at the settled gate: full-r6.md CLEAN (integrity 13/12); full-r6-broken.md DRIFT drift-sections=2 (chain+sweeps as before; integrity CLEAN 13/12); full-r6-absent.md CLEAN run=4 absent=1 (integrity 2/2)
```

Regression battery (this seat; before = r6 receipt values, after = settled
gate):

| Check | Before (`0c3d51ed…`) | After (`3ba718bf…`) | Exit |
|---|---|---|---|
| selftest | `PASS (64 cases)` | `PASS (74 cases)`, case lines 1–64 BYTE-IDENTICAL (`cmp` vs the r6 receipt's first 64); 65–74 new: `integrity-pass`, `integrity-fail-dangling-claim`, `…-source`, `…-chain-claim`, `…-sweep`, `integrity-exempt-counted`, `integrity-fail-counting`, `setup-integrity-no-path`, `setup-integrity-missing-file`, `all-dangling.md` | 0 |
| claims `claims-r2.jsonl` | 17/17 CLEAN | 17/17 CLEAN (`VERDICT_BEARING_CLAIMS=17/17`) | 0 |
| chain `chain-r3.md` | 17/22 CLEAN | 17/22 CLEAN | 0 |
| chain control | 1/2 DRIFT | 1/2 DRIFT (`CHAIN_ANCHOR_NOT_FOUND`) | 1 |
| sweeps `sweeps-r5.md` | 1/2 + 3/3 CLEAN | 1/2 + 3/3 CLEAN | 0 |
| sweeps control | 0/1 + 0/1 DRIFT | 0/1 + 0/1 DRIFT | 1 |
| r1 `verify` on the r6 pair | CLEAN findings=0 | CLEAN findings=0 (both) | 0 |
| r1 archives A/B/C | 3/3 DRIFT | 3/3 DRIFT (each exit 1) | 1 |
| exit contract | 0/1/2 | 0 CLEAN / 1 DRIFT as above; `missing record`→2, `unknown flag`→2, `--json` dir missing→2, `--json` path is a dir→2, `--json`/`--claims` outside verify-all→2, solo `verify-integrity` CLEAN→0 | 0/1/2 |
| manifest `--json` | 4 sections | 5 sections; one line per run; line 1 byte-stable across append 2 (sha identical); CLEAN line integrity `{refs:16,resolved:15,unresolved:0,exempt:1,findings:0,drift:0}` + native `INTEGRITY refs=16 resolved=15 unresolved=0`; DRIFT line `{16,13,2,1,2,2}` | — |
| zero network | 0 (r6) | strace `-f -e trace=network` on a composed run: **0** network lines of 7976 | 0 |

## Defects found by the scribe seat

1. **None blocking; no regression found at the settled revision.** All prior
   observables held (cases 1–64 byte-identical; every r1–r6 mode unchanged;
   the r1 archive observable 3/3; zero network). The new section is the only
   source of new findings on the twin, exactly as pre-registered.
2. **Wave convergence (historical, RESOLVED in-wave).** The first landed
   integrity revision exempted id-SHAPED tokens behind exempt row statuses
   (design pinned by selftest case 70 `integrity-exempt-counted`). The first
   version of the fixture pair pinned the source defect behind an exempt hop
   (`blocked-no-fetch`), which under that semantic measured `observed=exempt
   … status=blocked-no-fetch` — one finding instead of two; this seat
   measured that interim mismatch at gate `3ba718bf…` on the first fixture
   shas (`e2dfc7de…`/`7af72514…`). The fixture author then re-shaped the pair
   (settled `4310ce86…`/`fd4e213f…`): the dangling `from=S9` now sits on a
   non-exempt `resolved` hop, the README names the class boundary and the
   reshape, and the settled measurement shows exactly the pre-registered two
   findings. Scribe confirmed the settled contract. The exempt class remains
   measured in place (N2 `sweep=SW2`, `status=unresolved`) and by case 70.
3. **Shape boundary (named limit, not a defect).** Only id-SHAPED tokens are
   references: `Z9` in a sweep cell is not counted (d1: refs drops, CLEAN) —
   a token that names nothing but does not look like an id is invisible to
   integrity. This is the fail-closed shape rule (S/C|N/SW + digit), not a
   silent pass: it is the same shapes the fixture README pins, and
   non-id-shaped naming remains the sweeps/claims/chain modes' business.
4. **Manifest/schema growth (integration note).** `sections_run` is now 5 and
   the integrity section carries `tallies{refs,resolved,unresolved,exempt,findings,drift}`
   + `native` in the same `chousa-verify-all/v1` schema. Consumers that pinned
   `sections=4` (round-6 README rows, prose) read stale; [PARENT: if the
   parent wants a schema version bump or a README pointer, it is a
   parent-owned edit; this seat only names it.]
5. **Cosmetic (carried):** the banner still reads `research-gate-r1`.

## SHONEN

[PARENT: re-check against SHONEN.md at integration.] All four tripwires
remain `[ ]` (no named non-author verifier; wave seats are the lane per
protocol). Boundaries held: zero network (strace, 0 of 7976 lines); corpus
read-only; seats committed nothing; scratch under `$HOME/.cache/chousa-tmp/`
declared ephemeral (no EDQUOT; cleaned at end of run — `/tmp` was left
untouched this round).

## Per-axis and learning verdicts

See `.ufo/round-7/goal-wave/scorecard-verdict-draft.md` (verdict vocabulary
only, no scalar scores): coverage **improved**; operability **improved**
(selftest 64→74, 1–64 byte-identical; solo mode + fifth section; manifest
carries the integrity tallies); depth **improved** under the r2–r6 note
precedent [PARENT]; freshness/calibration/adjacency **unchanged** [PARENT:
cells in the scorecard draft]; none harmed. Trends: expansion **improved**,
quality **improved**, discernment **unchanged**.

## Debt, cross-domain handoff and admission

- **Receipt identity (round 1) — STILL OPEN** (integrator/operator side). No
  authentic queue taskKey/expected receipt bag exists; no `task_…` value may
  be manufactured, no shape-only receipt counted, no Sighting marked
  complete. Proven receipt-backed completed rounds remain **0**; operator
  target unchanged (≥100). Routing for this wave is the operator's in-session
  direct dispatch; no Sighting was invoked. Lane evidence from this round is
  not a mission receipt.
- Named limits carried/created: the id-SHAPE boundary (Defect 3); exempt-class
  semantics pinned (Defect 2 — closed by reshape; the boundary stays named and
  selftest-cased);
  manifest `sections=5` schema growth (Defect 4); nested execution cost — a
  composed run now spawns up to five fresh gate processes; absent!=drift
  omission limit (r6, still open); non-vacuous flip screening (r5 candidate);
  non-author spot-check (integrator/operator); carried residuals (in-root
  hardlinks, no source size cap, token-aligned shortening, non-ASCII-adjacent
  fail-closed edges, scope-refusal finding IDs, frozen-replay comparator).
- Round 8 registered candidate [PARENT]: record-type obligations / the
  omission limit's finer half (a record that SHOULD carry a section but does
  not), plus the named shape-boundary and schema-growth items above.
- Artifact ledger at draft time (uncommitted): gate `3ba718bf…` (+536/−20),
  fixtures + README (shas above), [PARENT: note/lesson/receipts/SKILL row/
  corpus rows when they land]. Integrate only what lands.

## Fresh-session continuation

Measured state at draft time: gate `3ba718bf…` (uncommitted; the r6 revision
is recoverable as `git show 4835426:tools/research-gate.sh` = `0c3d51ed…`;
lane HEAD `4835426`). Open items for a next round (all named with evidence
above): the id-shape boundary; record-type obligations; manifest schema
growth; nested execution cost; carried residuals. Any next round must
declare its own falsifiable single move; do not rerun this wave. Receipt
identity remains the standing integrator-side blocker (target ≥100).