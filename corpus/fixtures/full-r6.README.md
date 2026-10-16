# full-r6.md / full-r6-broken.md / full-r6.claims.jsonl — all-section record + two-defect twin (chousa round 6)

Round-6 composition move (dispatch 2026-10-16): the r5 gate carries five modes
(`verify`, `verify-claims`, `verify-chain`, `verify-sweeps`, `--selftest`) under
one boundary policy and a 0/1/2 exit contract, but a record's FULL verification
state can only be obtained by running four of them by hand and eyeballing four
separate summaries, and nothing durable records that state. `verify-all <record>
--root PATH` composes ONE verdict (DRIFT iff any section drifts) and `--json
<path>` appends the record's verification state to a lane manifest. This fixture
pair pre-registers, as fixed local inputs with fixed expected outputs, the
composed verdict the mode must produce: `full-r6.md` carries every gate-known
section correctly and must compose CLEAN with per-section tallies equal to the
solo modes', `full-r6-broken.md` carries exactly two defects in two different
sections and must compose DRIFT naming both while the other two sections stay
green.

## Authoring state

Lane HEAD `1d1f56c…`; gate revision `55adb92d0ba5ac958907fac6c4d5d6b0b50129703e866a5befbd9a32789f2ff2`
(sha256; same as the round-5 receipt), where `verify-all` does NOT exist yet —
the composition mode landed from a parallel seat during this wave, so the
composed verdict below is PRE-REGISTERED, not measured; every per-mode input it
composes over is measured here. The fixtures are uncommitted under
`corpus/fixtures/`; no commits by this seat.

Measured "before" state at that revision, lane cwd (fresh processes):

```text
$ bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.md --root ..
stderr: research-gate: multiple record paths   (+ usage)
exit=2, stdout_bytes=0        # verify-all is not a mode; it degrades to a record argument
$ bash tools/research-gate.sh verify corpus/fixtures/full-r6.md --json /dev/null --root ..
stderr: research-gate: unknown flag: --json
exit=2, stdout_bytes=0
$ grep -rln manifest corpus/ tools/ ; find . -name '*manifest*' -not -path './.git/*'
(no output)                   # no manifest file exists anywhere in the lane
```

## What each file is

| file | role |
|---|---|
| `full-r6.md` | positive control — one record carrying every gate-known section, all resolvable against pinned local inputs |
| `full-r6-broken.md` | tampered twin — differs from `full-r6.md` in exactly three lines: two planted defects (one section each) plus its `claims_file` row naming its own companion; the third difference is not a defect |
| `full-r6.claims.jsonl` | the claims companion of `full-r6.md` — 3 claims, all `expect=supported`, all resolving in pinned exports; bound to the record by its `## Meta` `claims_file` row |
| `full-r6-broken.claims.jsonl` | the claims companion of `full-r6-broken.md` — byte-identical to the positive's (claims stay GREEN in the tampered run, by design) |
| `full-r6-absent.md` | omission probe — optional inputs genuinely absent: no `## Sweeps`, no `## Negatives`, no `claims_file` Meta row and no companion file for it (deliberately) |

## The positive control

`full-r6.md` carries: Meta (loopback / fetch none), Question, Sources (4 rows,
tiers `export` x3 + `fleet-gate`), Chain (3 resolved hops), Claims (3 pointed
rows), Negatives (2 rows, both carrying a sweep id), Sweeps (2 rows: one local
path set, one declared source-id set), Rejections (2 rows, each reason +
flip_condition), Approval (not-required).

The three hops exercise the three anchor kinds that are exercisable against
these inputs — no `^#` heading line exists in any of the three exports
(measured: `grep -c '^#'` = 0 each), so `quote`, `quote`, `line` are used, with
the whole-line anchor taken from C's plain section line:

| hop | claim | target | kind | anchor | measured resolution |
|---|---|---|---|---|---|
| 1 | C1 | S1 A:64 | quote | `I could not substantiate this spelling as an established artisan rank in the Japanese or English sources searched.` | `at=line:64 verdict=match` |
| 2 | C2 | S2 B:57 | quote | `Track five axes separately: task competence, retention, evidence fidelity, cross-domain transfer, and operating cost.` | `at=line:57 verdict=match` |
| 3 | C3 | S3 C:107 | line | `“Jin’i-ryū” does not support the proposed literal translation` | `at=line:107 verdict=match` |

The claims companion mirrors the three observations (span bytes identical to
hops 1-3's anchors, so a reader sees one rule governing both modes): FC1 at
A:64, FC2 at B:57, FC3 at C:107, all `observed=supported verdict=match`.

The kept rejections are the intake's own RJ-02 (`corpus/knowledge/archived-export-intake.md:102`)
and RJ-03 (line 103), reduced to the fixture row shape; the flip-conditions are
this fixture's formulation of what those reasons imply. The two negatives restate
the intake's CL-05/CL-06 and its W1/W2 sweep rows (lines 87-88, 150-151). SW1
re-runs the path-set half of the "nothing external was cached" negative
(`research/deep-research-2026-09-28/saved-*,research/deep-research-2026-09-28/*-snapshot-*`,
zero matches); SW2 is a content sweep inside declared sources, which the gate
counts exempt and never re-runs. The record contains no URL string at all — the
zero-network posture is byte-visible, not just protocol.

## The tampered twin — one defect in each of two sections

`diff full-r6.md full-r6-broken.md` is exactly three lines: two planted defects
(one per section) and the twin's `claims_file` row naming its OWN companion
(a path rename, not a defect — the companion bytes are identical).

| path:line | section | defect | expected finding |
|---|---|---|---|
| `corpus/fixtures/full-r6-broken.md:29` | Chain | hop 2's anchor gains an `s`: `…cross-domain transfer, and operating costs.` — bytes the target never carries | `CHAIN_ANCHOR_NOT_FOUND` on hop 2 (`nearest_line=57`, `RESOLVED_HOPS=2/3`) |
| `corpus/fixtures/full-r6-broken.md:59` | Sweeps/Rejections | R2's flip_condition cell is empty while its reason stays present | `SWEEP_REJECTION_INCOMPLETE` on R2 (`missing=flip`, `REJECTIONS_OK=1/2`) |

Both defects are invisible to the r1 `verify` structure path — the resolved
hop's `to` still names a declared source, and R2 still has a reason — so
`verify` stays CLEAN on the twin (measured below). That is the point: the
composed verdict must find dirt that the structure mode cannot, and it must
name exactly `chain` and `sweeps` as dirty while `structure` and `claims` stay
green.

## The omission probe

`full-r6-absent.md` is the third record: a structure-complete record whose
OPTIONAL inputs are genuinely absent — no `## Sweeps`, no `## Negatives`, and no
claims companion file exists for it. The round's rule is that an absent section
is REPORTED, not drift, so this probe's composed expectation is CLEAN with its
`claims` and `sweeps` sections reported absent/empty. Measured solo at the
authoring revision:

- `verify` → CLEAN (questions=1 sources=1 chains=1 claims=1 negatives=0 rejections=1 approvals=1), exit 0
- `verify-chain` → `RESOLVED_HOPS=1/1` CLEAN, exit 0
- `verify-sweeps` → `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1` CLEAN, exit 0

The omission rule has a measured limit, and it is worth stating because the
round's "absent-section records stay CLEAN" claim depends on it: a record cannot
compose CLEAN once the sections the STRUCTURE mode demands are gone. A scratch
probe outside the lane (not a fixture: Question/Sources/Approval only) measures

```text
verify        → FINDING CLAIM_TABLE_ABSENT … FINDING REJECTION_DROPPED … RESEARCH_GATE: DRIFT (findings=2 drift=2 …), exit 1
verify-chain  → RESEARCH_GATE: DRIFT (… findings=1 drift=1)   # a missing ## Chain drifts the chain mode itself (CHAIN_ABSENT)
verify-sweeps → RESEARCH_GATE: CLEAN (sweeps=0 … rejections=0 …), exit 0
```

so "absent = reported, not drift" can only hold for the OPTIONAL inputs (a
missing claims surface; absent sweep/negative rows), and a composing mode must
SKIP a section it cannot run rather than compose a mode's own `*_ABSENT` drift.
How fine-grained that omission reporting should be — and how a Chain-less
record should be treated — is the named r7 candidate, not a round-6 claim.

## Cited sources (pinned, read-only)

The three archived deep-research exports under `research/deep-research-2026-09-28/`
(fleet root, read-only), pinned to fleet commit `0863746e9da95457f71b9e00a40361b88ab0df15`;
sha256 re-derived 2026-10-16, matching the round-5 receipt pins:

```text
9033857d4625555c7b778dfad6df80e3e1b24ed8bffa3fee2fd445b9c5540b85  A-shokunin-tradition.md
6d8dbddd3e2d2f47dcb153c5a3347cc6321db4afc72cf07da40f0f7fe5022006  B-multiagent-knowledge.md
e48fe70ff92055c217ac6ca6ce68e403aa5689fee8717f3bd0ccf5badc92321b  C-rank-taxonomy.md
```

The record also cites the lane's own round-1 intake
`chousa-shokunin/corpus/knowledge/archived-export-intake.md` (S4) and the fleet
index `research/README.md:12` (R1's ref). Pointer cells are fleet-root-relative;
every run below passes `--root ..` from the lane cwd (the round-1 convention).
No file outside the fleet root is opened; no URL is fetched.

## Pre-registered expectations

Solo modes, measured at gate `55adb92d…` (verbatim outputs in the next section):

| record | structure | claims | chain | sweeps |
|---|---|---|---|---|
| `full-r6.md` | CLEAN, findings=0 drift=0 q=1 src=4 ch=3 cl=3 neg=2 rej=2 appr=1 | `VERDICT_BEARING_CLAIMS=3/3` CLEAN | `RESOLVED_HOPS=3/3` CLEAN | `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=2/2` CLEAN |
| `full-r6-broken.md` | CLEAN, same tallies | `VERDICT_BEARING_CLAIMS=3/3` CLEAN | `RESOLVED_HOPS=2/3` DRIFT | `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=1/2` DRIFT |
| `full-r6-absent.md` | CLEAN, findings=0 drift=0 q=1 src=1 ch=1 cl=1 neg=0 rej=1 appr=1 | companion file does not exist (claims reported absent) | `RESOLVED_HOPS=1/1` CLEAN | `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1` CLEAN |

Composed expectation for `verify-all corpus/fixtures/<record> --root ..`
(PRE-REGISTERED; the mode is not at the authoring revision — any landed mode
whose composed verdict differs falsifies this fixture's contract):

- `full-r6.md` → one composed verdict CLEAN, exit 0; per-section tallies equal
  to the solo columns above; no section reported dirty.
- `full-r6-broken.md` → one composed verdict DRIFT, exit 1; dirty sections named
  `chain` and `sweeps` (with the two findings above); `structure` and `claims`
  reported clean. A composed verdict that reports DRIFT without naming both
  dirty sections, or that fails the positive control, is a mismatch.
- `full-r6-absent.md` → one composed verdict CLEAN, exit 0; `claims` and
  `sweeps` reported absent (no claims surface is bound, no sweep or negative
  rows exist) while `structure` and `chain` run CLEAN. A composed verdict that
  turns either omission into DRIFT is a mismatch against the round's rule.
- `chain` absent is NOT exercised as a CLEAN case: measured, a Chain-less
  record drifts at the structure level the moment it carries any claim row (and
  the chain mode's own `CHAIN_ABSENT` fires regardless), so no such record can
  compose CLEAN — see the omission probe above. The manifest half (`--json`) is
  the receipts seat's artifact, not this fixture's.

## Execution record

Gate revision `55adb92d0ba5ac958907fac6c4d5d6b0b50129703e866a5befbd9a32789f2ff2`
(sha256, re-checked identical before and after every run below), lane cwd,
fresh processes, `--root ..`, no network. Verbatim stdout:

```text
$ bash tools/research-gate.sh verify corpus/fixtures/full-r6.md --root ..
research-gate research-gate-r1 — ts=2026-10-16T01:46:00Z — mode=verify — record=corpus/fixtures/full-r6.md
RESEARCH_GATE: CLEAN (findings=0 drift=0 questions=1 sources=4 chains=3 claims=3 negatives=2 rejections=2 approvals=1)
exit=0

$ bash tools/research-gate.sh verify corpus/fixtures/full-r6-broken.md --root ..
research-gate research-gate-r1 — ts=2026-10-16T01:46:01Z — mode=verify — record=corpus/fixtures/full-r6-broken.md
RESEARCH_GATE: CLEAN (findings=0 drift=0 questions=1 sources=4 chains=3 claims=3 negatives=2 rejections=2 approvals=1)
exit=0

$ bash tools/research-gate.sh verify-claims corpus/fixtures/full-r6.claims.jsonl --root ..
research-gate research-gate-r1 — ts=2026-10-16T01:46:07Z — mode=claims — claims=corpus/fixtures/full-r6.claims.jsonl
CLAIM id=FC1 expected=supported observed=supported source=research/deep-research-2026-09-28/A-shokunin-tradition.md at=line:64 verdict=match
CLAIM id=FC2 expected=supported observed=supported source=research/deep-research-2026-09-28/B-multiagent-knowledge.md at=line:57 verdict=match
CLAIM id=FC3 expected=supported observed=supported source=research/deep-research-2026-09-28/C-rank-taxonomy.md at=line:107 verdict=match
VERDICT_BEARING_CLAIMS=3/3
RESEARCH_GATE: CLEAN (claims=3 supported=3 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
exit=0

$ bash tools/research-gate.sh verify-claims corpus/fixtures/full-r6-broken.claims.jsonl --root ..
CLAIM id=FC1 … at=line:64 verdict=match
CLAIM id=FC2 … at=line:57 verdict=match
CLAIM id=FC3 … at=line:107 verdict=match
VERDICT_BEARING_CLAIMS=3/3
RESEARCH_GATE: CLEAN (claims=3 supported=3 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
exit=0

$ bash tools/research-gate.sh verify-chain corpus/fixtures/full-r6.md --root ..
CHAIN hop=1 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"I could not substantiate this spelling as an established art" at=line:64 verdict=match
CHAIN hop=2 status=resolved observed=verified source=research/deep-research-2026-09-28/B-multiagent-knowledge.md anchor=quote:"Track five axes separately: task competence, retention, evid" at=line:57 verdict=match
CHAIN hop=3 status=resolved observed=verified source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=line:"“Jin’i-ryū” does not support the proposed literal tra" at=line:107 verdict=match
RESOLVED_HOPS=3/3
RESEARCH_GATE: CLEAN (hops=3 verified=3 exempt=0 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0)
exit=0

$ bash tools/research-gate.sh verify-chain corpus/fixtures/full-r6-broken.md --root ..
CHAIN hop=2 status=resolved observed=anchor-missing source=research/deep-research-2026-09-28/B-multiagent-knowledge.md anchor=quote:"Track five axes separately: task competence, retention, evid" at=- verdict=mismatch
FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=2 source=research/deep-research-2026-09-28/B-multiagent-knowledge.md anchor=quote:"Track five axes separately: task competence, retention, evid" nearest_line=57 context=The strongest design implication is to make knowledge changes—not agent self-a
RESOLVED_HOPS=2/3
RESEARCH_GATE: DRIFT (hops=3 verified=2 exempt=0 anchor-missing=1 refused=0 invalid=0 findings=1 drift=1)
exit=1

$ bash tools/research-gate.sh verify-sweeps corpus/fixtures/full-r6.md --root ..
SWEEP id=SW1 where=research/deep-research-2026-09-28/saved-*,research/deep-research-2026-09-28/*-sn looked=local hits=0 at=- observed=verified verdict=match
SWEEP id=SW2 where=S1,S2,S3 looked=source-ids hits=- at=- observed=exempt verdict=exempt
REJECTION id=R1 ref=research/README.md:12 reason=present flip=present observed=complete verdict=match
REJECTION id=R2 ref=research/deep-research-2026-09-28/B-multiagent-knowledge.md:79 reason=present flip=present observed=complete verdict=match
VERIFIED_SWEEPS=1/2 REJECTIONS_OK=2/2
RESEARCH_GATE: CLEAN (sweeps=2 verified=1 exempt=1 hit=0 refused=0 invalid=0 rejections=2 rejections-ok=2 findings=0 drift=0)
exit=0

$ bash tools/research-gate.sh verify-sweeps corpus/fixtures/full-r6-broken.md --root ..
SWEEP id=SW1 … looked=local hits=0 at=- observed=verified verdict=match
SWEEP id=SW2 where=S1,S2,S3 looked=source-ids hits=- at=- observed=exempt verdict=exempt
REJECTION id=R1 … observed=complete verdict=match
REJECTION id=R2 ref=research/deep-research-2026-09-28/B-multiagent-knowledge.md:79 reason=present flip=absent observed=incomplete verdict=mismatch
FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R2 missing=flip
VERIFIED_SWEEPS=1/2 REJECTIONS_OK=1/2
RESEARCH_GATE: DRIFT (sweeps=2 verified=1 exempt=1 hit=0 refused=0 invalid=0 rejections=2 rejections-ok=1 findings=1 drift=1)
exit=1
```

The `where=` display is cut at the mode's own 80-character cap (`…/*-sn`); the
cell itself names both globs. Lines shown as `…` above are elided duplicates of
the full positive-control lines (same bytes, same verdicts); every non-elided
line is verbatim.

## Composed run (`verify-all`)

The mode landed mid-wave from a parallel seat, and its sha moved while it was
written (`55adb92d…` → `4f1c62f5…` → `ea3283f1…` → `0c3d51ed…`). Two transient
defects were observed and diagnosed on the way; they are recorded here because
they were real at their revisions. At `4f1c62f5…` the RECORD path aborted on
every Markdown input (`line 1788: SEC_STATE[$name]: unbound variable`, exit 1,
empty stdout — `load_sections` resetting the same-named `SEC_ORDER` the
composing function had set). At `ea3283f1…` the record path ran, but the
documented `## Meta` claims binding matched table COLUMN names, so the r1
`| key | value |` row did not bind (measured then: `claims state=absent` for the
row idiom, bound for a column-header variant). The revision measured below,
`0c3d51ed…`, binds the row.

Composed verdicts at gate sha256 `0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8`
(re-checked identical before and after every run below), lane cwd, fresh
processes, `--root ..`, no network:

```text
$ bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.md --root ..
research-gate research-gate-r1 — ts=2026-10-16T01:55:53Z — mode=verify-all — record=corpus/fixtures/full-r6.md — claims=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/full-r6.claims.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=3/3
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/2 REJECTIONS_OK=2/2
VERIFY_ALL sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0)
exit=0        # positive control: composed CLEAN, per-section tallies equal to the solo modes

$ bash tools/research-gate.sh verify-all corpus/fixtures/full-r6-broken.md --root ..
research-gate research-gate-r1 — ts=2026-10-16T01:55:56Z — mode=verify-all — record=corpus/fixtures/full-r6-broken.md — claims=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/full-r6-broken.claims.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=DRIFT findings=1 drift=1 tally=RESOLVED_HOPS=2/3
FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=2 source=research/deep-research-2026-09-28/B-multiagent-knowledge.md anchor=quote:"Track five axes separately: task competence, retention, evid" nearest_line=57 context=The strongest design implication is to make knowledge changes—not agent self-a
SECTION sweeps state=run verdict=DRIFT findings=1 drift=1 tally=VERIFIED_SWEEPS=1/2 REJECTIONS_OK=1/2
FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R2 missing=flip
VERIFY_ALL sections=4 run=4 absent=0 drift-sections=2 findings=2 drift=2
RESEARCH_GATE: DRIFT (sections=4 run=4 absent=0 drift-sections=2 findings=2 drift=2)
exit=1        # twin: DRIFT naming exactly the two dirty sections; structure and claims stay green

$ bash tools/research-gate.sh verify-all corpus/fixtures/full-r6-absent.md --root ..
research-gate research-gate-r1 — ts=2026-10-16T01:55:59Z — mode=verify-all — record=corpus/fixtures/full-r6-absent.md — claims=- — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=absent
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=1/1
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1
VERIFY_ALL sections=4 run=3 absent=1 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=4 run=3 absent=1 drift-sections=0 findings=0 drift=0)
exit=0        # omission probe: an absent section is reported, not drift
```

Manifest half at the same revision: four runs — the three records above plus the
claims companion passed as its own claims input — appended exactly four lines to
a scratch manifest outside the lane (no rewrite; every line valid JSON): in
order composed CLEAN (run=4), DRIFT (run=4, drift_sections=2), CLEAN (run=3,
absent=1), CLEAN (claims-only input, run=1, absent=3), each carrying
`record_sha256` (`878c2c50…`, `0f7e498c…`, `39cdb2d7…`, `45eb6ac2…` for the
four inputs), `gate_sha256` (`0c3d51ed…`), the per-section
state/verdict/findings/drift/tallies, and the composed verdict. The LANE
manifest is the receipts seat's artifact, not this fixture's.

**Resolved during the wave — the `## Meta` claims binding.** At `ea3283f1…` the
documented row binding (`chain_cell "$crow" claims claims_file …`) matched table
COLUMN names, so the r1 `| key | value |` row did not bind: measured then,
`verify-all full-r6.md --root ..` reported `SECTION claims state=absent`, while a
copy with a `| window | claims_file |` column header bound
(`state=run … 3/3`) and explicit `--claims corpus/fixtures/full-r6.claims.jsonl`
bound. At `0c3d51ed…` the row binds — see the `claims=` field in the positive
run's header line above — so the pre-registration's run=4 expectation is met
with no flag; a record with no such row (the omission probe) still reports
`claims state=absent`.

## Honest boundaries

- The composed verdicts above were PRE-REGISTERED before the composing mode
  existed (the four solo runs were the measured inputs), and are measured in the
  Composed run section at the pinned revision `0c3d51ed…`; that mode's sha moved
  three times during the wave, so a later revision that changes its composition
  rule should reproduce this fixture's contract from the record bytes and the
  pre-registration, not from the quoted run.
- SW1 re-checks a path-set EMPTINESS under two saved-copy naming globs, not a
  content census: a saved copy named outside those two patterns would not be
  caught, and the record's SW2 content sweep is exempt by the mode's own
  contract, not re-run.
- The twin's chain defect is one tampered quote; that the twin also contains the
  positive's other 2 good hops and 2 good claims is the composition test (a
  mode that blanket-fails the record also fails this fixture's contract, since
  the pre-registration names exactly two dirty sections).
- Both records are RESOLVED_CLEAN-shaped at the pinned revision only: SW1's
  emptiness is a property of `research/deep-research-2026-09-28/` at the pinned
  sha256s, and hop/claim anchors are properties of the pinned export bytes.
  Under a different `--root` the fleet-root-relative pointers do not resolve and
  every mode reports refused/unresolved — the re-run command is pinned for this
  reason.
- The claims companions are bound to their records by the records' own `## Meta`
  `claims_file` rows (the landed `verify-all` contract), not by a filename
  convention; the companion's being bound is what makes the record's claims
  section verdict-bearing under a composing mode at all. `full-r6-absent.md`
  deliberately carries no such row.
- No scalar score, no promotion, no field-readiness claim.

## Inventory sha256 (2026-10-16)

```text
45eb6ac2cde9e3c33dd4d753e4da2cb660308dad8f00475a382a2881b89ddc40  full-r6.claims.jsonl
45eb6ac2cde9e3c33dd4d753e4da2cb660308dad8f00475a382a2881b89ddc40  full-r6-broken.claims.jsonl
```

Record sha256s at the composed-run revision:

```text
878c2c50ec9efba5a103644bbc002a7029c9cbead9b95ec369913760d158212a  full-r6.md
0f7e498cf1f6f6192a2660b14e41a025dbf47972d3c37ffd414df008bb6b320f  full-r6-broken.md
39cdb2d727c5f2e26093c7099f501ab21a8fae6ac9d2fa458161614ad4953d6c  full-r6-absent.md
```

## Re-run

```bash
cd chousa-shokunin
bash tools/research-gate.sh verify-all    corpus/fixtures/full-r6.md --root ..          # composed CLEAN, run=4
bash tools/research-gate.sh verify-all    corpus/fixtures/full-r6-broken.md --root ..   # composed DRIFT, drift-sections=2
bash tools/research-gate.sh verify-all    corpus/fixtures/full-r6-absent.md --root ..   # composed CLEAN, claims absent
bash tools/research-gate.sh verify        corpus/fixtures/full-r6.md --root ..
bash tools/research-gate.sh verify-claims corpus/fixtures/full-r6.claims.jsonl --root ..
bash tools/research-gate.sh verify-chain  corpus/fixtures/full-r6.md --root ..
bash tools/research-gate.sh verify-sweeps corpus/fixtures/full-r6.md --root ..
bash tools/research-gate.sh verify-chain  corpus/fixtures/full-r6-broken.md --root ..
bash tools/research-gate.sh verify-sweeps corpus/fixtures/full-r6-broken.md --root ..
```

`--json <manifest>` may be appended to any `verify-all` line; the lane manifest
path is the receipts seat's choice, and the scratch manifests used here lived
outside the lane.