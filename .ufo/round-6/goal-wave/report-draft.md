# chousa — round 6: `verify-all` composes one verdict + the record's verification state in the lane manifest (operability/composition move)

<!-- SCRIBE DRAFT — MEASURED FINAL. Before: gate sha256
     55adb92d0ba5ac958907fac6c4d5d6b0b50129703e866a5befbd9a32789f2ff2
     (== `git show HEAD:tools/research-gate.sh`), lane HEAD 1d1f56c. After:
     gate sha256
     0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8
     (+450 lines vs HEAD; stable ≥9 min through this seat's battery, sha
     identical before and after it; the wave's two earlier transient
     revisions that were functionally defective on the record path are
     documented in the r6 note, not measured by this seat). Lane HEAD still
     1d1f56c; no commits by any seat. Every after-value below is a verbatim
     fresh-process receipt from this seat. Scribe scratch
     /tmp/chousa-scribe-r6/ (declared ephemeral, cleaned at end of run).
     [PARENT] markers mark parent-only bindings. The Debt section keeps
     receipt identity OPEN per the mission contract. -->

Status: **DRAFT — measured, awaiting parent integration/admission**. Baseline:
lane HEAD `1d1f56c` (round-5 records). Wave: one 32-seat flash call. Report
time: 2026-10-16 ~02:10Z.

## Work performed

- Round 6 selects the move round 5 registered: **operability/composition** —
  one `verify-all <record> --root PATH` run composes every applicable mode
  into ONE verdict (DRIFT iff any run section drifts); claims/chains/sweeps
  surfaces are OPTIONAL (absent = reported, NOT drift — the omission limit
  is the named r7 candidate); `--json <path>` appends the record's
  verification state (record+gate SHA-256, UTC, per-section tallies,
  composed verdict) to a lane manifest (append-only JSONL).
- Scribe independent work: before-state probes and the solo-mode battery at
  the r5 gate; the after-state battery at the settled gate (composed
  verdicts on all three r6 records + the r5 fixture, per-section tally
  equality vs the solo modes, 5 manifest appends with prefix-sha proofs,
  well-formedness and field checks, regression battery, selftest
  byte-stability, 8 exit-contract probes, strace); note/lesson/receipt
  cross-checks; these drafts.

## Landed changes (all uncommitted, at draft time)

- `tools/research-gate.sh` → sha256 `0c3d51ed…` (+450/−0 vs HEAD): fifth mode
  `verify-all` (dispatch `:3102`; contract `:101-117`; usage `:179-182`,
  `:211-218`) with helpers `json_escape` `:1654`, `json_counts` `:1674`,
  `verify_all_section` `:1692`, `verify_all` `:1724`; claims binding
  (`:1758-1786`: input-JSONL, `--claims`, Meta row); manifest append `>>`
  `:1846`; selftest 54 → 64 (new block `:2906-3084`). Two transient
  revisions the wave passed through were defective on the record path
  (`4f1c62f5…` aborted on every Markdown input; `ea3283f1…` matched table
  column names so the canonical Meta row did not bind) — fixed by
  `0c3d51ed…`; documented in `corpus/knowledge/verify-all-r6.md`.
- Fixtures `corpus/fixtures/full-r6.md` (`878c2c50…`), `-broken.md`
  (`0f7e498c…`, exactly 3 lines differ: 2 defects + its own `claims_file`
  row), `-absent.md` (`39cdb2d7…`), companions `full-r6.claims.jsonl` /
  `full-r6-broken.claims.jsonl` (one sha `45eb6ac2…`; the two alias names
  were pruned by their author once the Meta-row binding settled),
  `full-r6.README.md` (`f56ef337…`) with pre-registered expectations,
  inventory shas and a composed-run section.
- `corpus/knowledge/verify-all-r6.md` (`9b9711cb…`, 18403 B); lesson
  `corpus/lessons/2026-10-16-verify-all-composition.md` (`d55bb183…`,
  22585 B); `SKILL.md` verify-all row + prose (`834c9707…`); receipts
  manifest `corpus/evidence/verify-all-manifest.jsonl` (`2ed28f9f…`,
  3627 B, 3 lines, gate `0c3d51ed…`, ts 02:04:09–14Z) and five receipt logs
  `compose-r6-20261016T020330Z-{selftest,full,broken,json,live}.log`
  (`e3b94e1c…`/`c96ac4f5…`/`83d7aef6…`/`1db37149…`/`ac4d3f8e…`);
  `corpus/README.md` round-6 rows (`499d5f3a…`) and the
  `corpus/evidence/README.md` round-6 receipts section (`ed94b72d…`) — the
  last three landed after this seat's battery and agree with it wherever
  they overlap (same composed verdicts and tallies; manifest 0→3 lines with
  prefix compares YES; selftest 64 with the first 54 case lines
  byte-identical; 0 network syscalls).

## Before → after measurements

**Before (this seat, fresh process, gate `55adb92d…`):**

```text
verify-all corpus/fixtures/sweeps-r5.md --root ..
  → exit 2, stdout empty, stderr "research-gate: multiple record paths" (no such mode)
verify corpus/fixtures/sweeps-r5.md --root .. --json /tmp/…/manifest.jsonl
  → exit 2, "research-gate: unknown flag: --json"
no manifest file exists anywhere in the lane (find); all verify modes zero-write
solo modes, same bytes:
  verify  sweeps-r5.md / -broken.md   → CLEAN findings=0 drift=0 ; exit 0 (both)
  verify-chain sweeps-r5.md           → RESOLVED_HOPS=2/3 CLEAN ; exit 0
  verify-sweeps sweeps-r5.md          → VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3 CLEAN ; exit 0
  verify-sweeps sweeps-r5-broken.md   → 0/1 + 0/1 DRIFT (SWEEP_REJECTION_INCOMPLETE,
                                        SWEEP_CLAIM_FALSE) ; exit 1
  verify-claims claims-r2.jsonl       → VERDICT_BEARING_CLAIMS=17/17 CLEAN ; exit 0
  selftest                            → PASS (54 cases) ; exit 0
  r1 archives A/B/C                   → each DRIFT exit 1 (3/3)
```

**After (gate `0c3d51ed…`, sha identical before/after battery, stable ≥9 min;
fresh processes; verbatim):**

```text
$ verify-all corpus/fixtures/full-r6.md --root ..            (exit 0)
research-gate research-gate-r1 — ts=2026-10-16T02:01:33Z — mode=verify-all — record=corpus/fixtures/full-r6.md — claims=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/full-r6.claims.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=3/3
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/2 REJECTIONS_OK=2/2
VERIFY_ALL sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0)

$ verify-all corpus/fixtures/full-r6-broken.md --root ..     (exit 1)
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=DRIFT findings=1 drift=1 tally=RESOLVED_HOPS=2/3
FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=2 source=research/deep-research-2026-09-28/B-multiagent-knowledge.md anchor=quote:"Track five axes separately: task competence, retention, evid" nearest_line=57 context=The strongest design implication is to make knowledge changes—not agent self-a
SECTION sweeps state=run verdict=DRIFT findings=1 drift=1 tally=VERIFIED_SWEEPS=1/2 REJECTIONS_OK=1/2
FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R2 missing=flip
VERIFY_ALL sections=4 run=4 absent=0 drift-sections=2 findings=2 drift=2
RESEARCH_GATE: DRIFT (sections=4 run=4 absent=0 drift-sections=2 findings=2 drift=2)

$ verify-all corpus/fixtures/full-r6-absent.md --root ..     (exit 0)
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=absent
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=1/1
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1
VERIFY_ALL sections=4 run=3 absent=1 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=4 run=3 absent=1 drift-sections=0 findings=0 drift=0)

$ verify-all corpus/fixtures/full-r6.claims.jsonl --root ..  (exit 0)
SECTION structure state=absent / claims run tally=VERDICT_BEARING_CLAIMS=3/3 / chain absent / sweeps absent
VERIFY_ALL sections=4 run=1 absent=3 drift-sections=0 findings=0 drift=0
```

Manifest (5 appends to `/tmp/chousa-scribe-r6/after/manifest-test.jsonl`,
verbatim line 1 at the settled gate):

```json
{"schema":"chousa-verify-all/v1","ts":"2026-10-16T02:02:23Z","record":"corpus/fixtures/full-r6.md","record_sha256":"878c2c50ec9efba5a103644bbc002a7029c9cbead9b95ec369913760d158212a","gate_sha256":"0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8","sections":[…structure/claims/chain/sweeps with tallies…],"verdict":"CLEAN","sections_run":4,"sections_absent":0,"drift_sections":0}
```

line 1 sha256 `9da468d8…` byte-stable across every append; head-4 prefix
`01fd1ccf…` byte-stable across the 5th append; every line `json.loads`-valid
(python3) and every `record_sha256`/`gate_sha256` re-verified against the
files; `>>` (`:1846`) is the only write site. The lane's own cut
`corpus/evidence/verify-all-manifest.jsonl` (`2ed28f9f…`) holds 3 lines at
gate `0c3d51ed…`.

Regression battery (this seat):

| Check | Before (`55adb92d…`) | After (`0c3d51ed…`) | Exit |
|---|---|---|---|
| selftest | `PASS (54 cases)` | `PASS (64 cases)`, cases 1–54 byte-identical; +10 verify-all cases | 0 |
| claims fixture | 17/17 CLEAN | 17/17 CLEAN, byte-identical modulo `ts=` | 0 |
| chain fixture | 17/22 CLEAN | 17/22 CLEAN, byte-identical modulo `ts=` | 0 |
| broken chain control | 1/2 DRIFT | 1/2 DRIFT, byte-identical modulo `ts=` | 1 |
| sweeps fixture | 1/2 + 3/3 CLEAN | held, byte-identical modulo `ts=` | 0 |
| broken sweeps control | 0/1 + 0/1 DRIFT | held, byte-identical modulo `ts=` | 1 |
| r1 `verify` on sweeps-r5 pair | CLEAN, findings=0 both | held, byte-identical modulo `ts=` | 0 |
| r1 archives A/B/C | 3/3 DRIFT | 3/3 DRIFT, byte-identical modulo `ts=` | 1 |
| exit contract (verify-all) | mode absent → 2 | CLEAN 0 / DRIFT 1 / 8 setup probes 2 (incl. read-only manifest → `manifest append failed`) | 0/1/2 |
| zero network | — | strace `-f -e trace=network` on the composed+manifest run: 0 network lines | 0 |

## Defects found by the scribe seat

1. **None blocking; no regression found.** Every prior observable held
   byte-stable; the composed tallies equal the solo modes' on the same
   bytes; the twin's two defects are named by section.
2. **Wave convergence (historical, resolved):** when `verify-all` first
   landed, bare invocation left `claims state=absent` on the positive
   fixture (binding needed `--claims`/Meta row) and the receipts seat's
   first manifest cut (gate `ea3283f1…`) was pulled; during the wave the
   fixture author added the Meta `claims_file` rows and the mode's binding
   was fixed/hardened (`0c3d51ed…`), the alias companion names were pruned,
   and the receipts manifest was re-cut at the settled gate (3 lines). No
   residual divergence observed: the receipts seat's independent cut at
   stamp `20261016T020330Z` (five logs) agrees with this seat's battery
   wherever they overlap, and both README round-6 rows landed by ~02:07Z.
3. **Fixture README wording nuance:** the absent-record composed bullet says
   "claims and sweeps reported absent" while the settled mode reports
   `sweeps state=run` with tally `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1`
   (its own pre-registered table matches the mode). Wording only; owner:
   fixture README, if the parent wants byte-exact alignment.
4. **Manifest boundary facts (design, not defect):** `--json` appends to any
   writable regular file whose dirname exists — no root/lane confinement
   inside the gate; the append is pre-verdict, so failure exits 2 without a
   verdict; no locking/fsync/rotation, and concurrent-append interleaving is
   unmeasured. The lane's receipts discipline keeps the manifest in
   `corpus/evidence/`.
5. **Untriggered defensive path:** `VERIFY_ALL_SECTION_UNAVAILABLE`
   (sub-mode rc∉{0,1} or unparsable verdict) is not exercised by the
   selftest or this seat's probes; named as untested rather than claimed
   covered.
6. **Cosmetic:** `structure`/`claims` SECTION lines carry no tally (the full
   counter dict lives in the manifest's `tallies`); the sweeps `where=`
   display keeps the r5 80-character cap.

## SHONEN

[PARENT: re-check against SHONEN.md at integration.] All four tripwires
remain `[ ]` (no named non-author verifier; wave seats are the lane per
protocol).

Boundaries held: zero network (strace, 0 network lines); corpus read-only;
seats committed nothing; /tmp quota respected (no EDQUOT; scratch cleaned at
end of run by this seat).

## Per-axis and learning verdicts

See `.ufo/round-6/goal-wave/scorecard-verdict-draft.md` (verdict vocabulary
only, no scalar scores): operability **improved**; depth **improved** under
the r2–r5 note precedent (landed note + lesson; [PARENT]); coverage /
freshness / calibration / adjacency **unchanged** [PARENT: cells in the
scorecard draft]; none harmed. Trends: expansion **improved**, quality
**improved**, discernment **unchanged**.

## Debt, cross-domain handoff and admission

- **Receipt identity (round 1) — STILL OPEN** (integrator/operator side). No
  authentic queue taskKey/expected receipt bag exists; no `task_…` value may
  be manufactured, no shape-only receipt counted, no Sighting marked
  complete. Proven receipt-backed completed rounds remain **0**; operator
  target unchanged (≥100). Routing for this wave was the operator's
  in-session direct dispatch; no Sighting was invoked. The round-6 manifest
  lines are lane evidence, not a mission receipt.
- The **omission limit** is the round's named r7 candidate: absent surfaces
  are reported, not drifted, so a record can compose CLEAN by omission
  (measured: claims absent on `sweeps-r5.md` → CLEAN; claims/sweeps
  granularity on `full-r6-absent.md` → CLEAN). Nothing asserts an absent
  section should have been present.
- Other named debts carried: nested execution cost (up to 4 subprocesses per
  composed run — the note's design note); manifest boundary facts (no
  confinement/locking); non-vacuous flip screening (r5 candidate); non-author
  spot-check (integrator/operator); carried residuals (in-root hardlinks, no
  source size cap, token-aligned shortening, non-ASCII-adjacent fail-closed
  edges, scope-refusal finding IDs, frozen-replay comparator, Claims-cell
  sweep references in `verify-sweeps`).
- No cross-domain handoff changes known at draft time.

## Fresh-session continuation

Measured state at draft time: gate `0c3d51ed…` (uncommitted; the r5 revision
is still recoverable as `git show HEAD:tools/research-gate.sh` =
`55adb92d…`; lane HEAD `1d1f56c`). Open items for a next round (all named
with evidence above): the omission limit (r7 candidate), the manifest
boundary/locking facts, the untriggered `VERIFY_ALL_SECTION_UNAVAILABLE`
path, non-vacuous flip screening, and the carried residuals. Any next round
must declare its own falsifiable single move; do not rerun this wave.
Receipt identity remains the standing integrator-side blocker (target ≥100).