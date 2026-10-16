# verify-all — round-6 composition mode + lane manifest (research-gate)

source: lane HEAD `1d1f56c…` (round-5 records; no commits by any seat at write
time — the round-6 gate, fixtures, receipts and this note are uncommitted
working-tree files). The round-6 gate revision is `tools/research-gate.sh`
sha256
`0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8` (observed
identical before and after the battery below, and stable >2 min while it ran);
the round-5 revision it replaces is
`55adb92d0ba5ac958907fac6c4d5d6b0b50129703e866a5befbd9a32789f2ff2`, still
recoverable as `git show HEAD:tools/research-gate.sh`. Two transient revisions
during this wave are on the record because they were real at their revisions:
`4f1c62f5…` — the RECORD path aborted on every Markdown input
(`load_sections` resetting the same-named `SEC_ORDER` the composing function
had set); `ea3283f1…` — the record path ran, but the documented `## Meta`
claims binding matched table COLUMN names, so the canonical `| key | value |`
row did not bind (measured then: `SECTION claims state=absent` on the positive
control). `0c3d51ed…` fixes both. The fixture README records the same
revisions (`corpus/fixtures/full-r6.README.md` §Composed run).

Fixtures (fixture-author seat, `corpus/fixtures/`): `full-r6.md` sha256
`878c2c50ec9efba5a103644bbc002a7029c9cbead9b95ec369913760d158212a`,
`full-r6-broken.md`
`0f7e498cf1f6f6192a2660b14e41a025dbf47972d3c37ffd414df008bb6b320f`,
`full-r6-absent.md`
`39cdb2d727c5f2e26093c7099f501ab21a8fae6ac9d2fa458161614ad4953d6c`,
companions `full-r6.claims.jsonl` / `full-r6-broken.claims.jsonl` (four alias
names, one sha256
`45eb6ac2cde9e3c33dd4d753e4da2cb660308dad8f00475a382a2881b89ddc40`);
`full-r6.README.md` sha256
`f56ef337aa41137af6db3624066947d29bcf4364a228dfdcdc8cc0e701646216` when this
note was checked. All script line numbers below are relative to the gate
revision above.
verified-at: 2026-10-15/16 ~01:57-01:59Z, from the lane cwd, fresh processes,
`--root ..`, local reads only; nothing fetched; the only processes run are the
gate's own section subprocesses; zero
network (strace below).
recheck:
`bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.md --root ..`
· `bash tools/research-gate.sh verify-all corpus/fixtures/full-r6-broken.md --root ..`
· `bash tools/research-gate.sh verify-all corpus/fixtures/full-r6-absent.md --root ..`
· `bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.claims.jsonl --root ..`
· `bash tools/research-gate.sh --selftest`

## The move

Before (gate `55adb92d…`): five modes existed (`verify`, `verify-claims`,
`verify-chain`, `verify-sweeps`, `--selftest`) under one boundary policy and a
0/1/2 exit contract, but a record's FULL verification state required running
four of them by hand and eyeballing four separate summaries; `verify-all`
degraded to a record argument (`research-gate: multiple record paths`, exit 2,
empty stdout — reproduced), `--json` was an unknown flag (exit 2), and no
manifest file existed anywhere in the lane.

After (gate `0c3d51ed…`): `verify-all [RECORD] [--claims PATH] [--json PATH]
[--root PATH]` runs every applicable mode as fresh gate calls and composes ONE
verdict — `RESEARCH_GATE: CLEAN|DRIFT` with per-section lines and composed
counters — and `--json PATH` appends the record's verification state to a
lane manifest (append-only JSONL). The composed verdict is DRIFT iff any RUN
section drifts; absent sections are reported, not counted (semantics and the
omission limit below).

## Composition semantics (as landed)

CLI and applicability (`:1746-1787`; usage text `:211-218`; parser `:3094-3125`):

- `structure` — always, for a Markdown-shaped input (any input that is not a
  claims JSONL: no `## ` heading lines and at least one line starting `{`,
  `:1752-1756`).
- `claims` — when a claims surface is BOUND: `--claims PATH` wins; else a
  `## Meta` row whose key cell is `claims`/`claims_file`/`claims-file`/
  `claimset` (canonical `| key | value |` row or `key: value` line, `:1764-1774`)
  resolves through the same corpus boundary as claim sources
  (`claim_source_path`, canonicalized, session/URL/out-of-corpus refused — the
  r2 policy); else, when the input itself is the claims JSONL, it is its own
  claims surface. A Meta declaration that cannot resolve does NOT fall back to
  absent: the claims section RUNS and drifts with `FINDING
  VERIFY_ALL_CLAIMS_UNRESOLVED severity=warn` (`:1780-1787`; selftest
  `all-meta-missing`, exit 1).
- `chain` — when the record declares `## Chain` (`:1760`).
- `sweeps` — when the record declares `## Sweeps`, `## Negatives` or
  `## Rejections` (`:1761-1763`).

Section execution (`verify_all_section`, `:1692-1722`): each section is run as
a fresh subprocess — `bash "$SELF" <mode> … --root "$ROOT"` (`:1696`) — so each
section's tally IS that solo mode's tally for the same bytes by construction,
and the r1-r5 boundary policy, exit contract and matching semantics are
inherited rather than re-implemented. A section whose subprocess returns rc ∉
{0,1} or prints ≠1 verdict line becomes `FINDING
VERIFY_ALL_SECTION_UNAVAILABLE severity=crit` and drifts the composed run
(`:1699-1711`).

Output (one composed run, `:1851-1871`):

```text
research-gate research-gate-r1 — ts=… — mode=verify-all — record=… — claims=… — root=…
SECTION <name> state=absent
SECTION <name> state=run verdict=… findings=N drift=N [tally=<native summary>]
…that section's FINDING lines…
VERIFY_ALL sections=4 run=N absent=N drift-sections=N findings=N drift=N
RESEARCH_GATE: CLEAN|DRIFT (sections=4 run=N absent=N drift-sections=N findings=N drift=N)
```

`tally=` appears for claims/chain/sweeps (the mode's native summary:
`VERDICT_BEARING_CLAIMS=`, `RESOLVED_HOPS=`, `VERIFIED_SWEEPS=… REJECTIONS_OK=`);
the structure section has no native summary. Composed `findings`/`drift` are
sums of the run sections' own counters; `drift-sections` counts sections whose
verdict is DRIFT (`:1803-1811`). Exit contract: 0 CLEAN / 1 DRIFT / 2
setup-usage (missing record → 2, missing manifest directory → 2, non-regular
manifest path → 2; `--claims`/`--json` outside verify-all → 2, `:3123-3125`).

## The manifest schema (`--json`)

Append-only: the only write to the manifest path is

```bash
if ! printf '%s\n' "$line" >>"$JSON_ARG"; then   # :1846-1849
```

a single `>>` append; there is no truncating open anywhere (`JSON_ARG` appears
only in validation `:1737-1744` and this append). Preconditions: the directory
must exist and an existing path must be a regular file (both `die_usage`, exit
2). One run appends exactly one JSON line — schema `chousa-verify-all/v1`:

| field | value |
|---|---|
| `schema` | `chousa-verify-all/v1` |
| `ts` | UTC (`%Y-%m-%dT%H:%M:%SZ`) |
| `record` | the record path as given |
| `record_sha256` | sha256 of the record bytes |
| `gate_sha256` | sha256 of `$SELF` (the gate that ran) |
| `sections` | fixed order structure, claims, chain, sweeps; absent → `{"name":…,"state":"absent"}`; run → `{name,state:"run",verdict,findings,drift,tallies{…}}`, plus `native` for the three summarised modes |
| `verdict` | composed `CLEAN`/`DRIFT` |
| `sections_run` / `sections_absent` / `drift_sections` | composed counters |

`tallies` are the parsed `k=v` pairs of that mode's parenthetical summary
(integers stay bare, strings quoted; `json_counts` `:1674`), so a manifest
line is a superset of the four solo summaries. Measured line (from this seat's
scratch manifest; elisions inside the JSON are marked `…` and make the
rendering below non-parseable as shown — the raw line parses, verified below):

```json
{"schema":"chousa-verify-all/v1","ts":"2026-10-16T01:58:07Z","record":"corpus/fixtures/full-r6.md",
 "record_sha256":"878c2c50…158212a","gate_sha256":"0c3d51ed…bfd5f8",
 "sections":[{"name":"structure","state":"run","verdict":"CLEAN","findings":0,"drift":0,
   "tallies":{"findings":0,"drift":0,"questions":1,"sources":4,"chains":3,"claims":3,"negatives":2,"rejections":2,"approvals":1}},
  {"name":"claims","state":"run","verdict":"CLEAN","findings":0,"drift":0,
   "tallies":{"claims":3,"supported":3,…,"drift":0},"native":"VERDICT_BEARING_CLAIMS=3/3"},
  {"name":"chain","state":"run","verdict":"CLEAN","findings":0,"drift":0,
   "tallies":{"hops":3,"verified":3,…,"drift":0},"native":"RESOLVED_HOPS=3/3"},
  {"name":"sweeps","state":"run","verdict":"CLEAN","findings":0,"drift":0,
   "tallies":{"sweeps":2,"verified":1,"exempt":1,…,"rejections-ok":2,…},"native":"VERIFIED_SWEEPS=1/2 REJECTIONS_OK=2/2"}],
 "verdict":"CLEAN","sections_run":4,"sections_absent":0,"drift_sections":0}
```

## Absence semantics and the omission limit

The rule (`:108-111`, `:1750`, `:1803-1811`): an ABSENT section is reported
`state=absent` and never drifts by itself; the composed verdict is DRIFT iff
any RUN section drifts. Rationale: a section the input does not carry is a
scope property, not evidence of dirty verification — "not bound / no such rows"
is not the same failure as "checked and found dirt", and composition must not
invent an obligation no mode ever had. The omission is made visible in the
manifest (`sections_absent`, per-section `state`), which is what bounds the
composed CLEAN.

Measured reach at `0c3d51ed…`:

- `claims` absent, CLEAN: `full-r6-absent.md` (structurally complete, carries
  its `## Claims` table, but no claims surface is bound and no companion
  exists) composes `run=3 absent=1`, CLEAN, exit 0 — section states:
  structure run CLEAN, claims absent, chain run `RESOLVED_HOPS=1/1`, sweeps run
  `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1`.
- Inputs that are themselves claims JSONL compose `run=1 absent=3` (structure/
  chain/sweeps absent), CLEAN, exit 0.
- Structure's own r1 findings are NOT waived by an absent section state
  (measured with this seat's scratch records outside the lane): a record
  missing `## Claims` composes DRIFT via `FINDING CLAIM_TABLE_ABSENT`
  (structure run), and a record with claim rows but no `## Chain` composes
  DRIFT via `FINDING CHAIN_ABSENT` — while those sections read `state=absent`.
  So in practice chain-absent and sweeps-absent cannot compose CLEAN (r1
  requires a Claims section and a Rejections section), and the CLEAN-preserving
  omission observed here is the claims-surface omission. The fixture README's
  omission probe records the same classes.
- A DECLARED but unresolvable binding is not an omission: it runs the claims
  section and drifts (`VERIFY_ALL_CLAIMS_UNRESOLVED`, table above); a bound
  claims file containing non-JSON lines drifts the section too (measured: 13 ×
  `CLAIM_RECORD_INVALID`, composed DRIFT).

The named r7 candidate (the omission limit): verify-all never asserts that an
absent section SHOULD have been present. A record can compose CLEAN while
carrying no bound claims surface, no sweep/negative rows, or — as measured
above — no Chain; omission shrinks what the composed CLEAN covers, and only
the manifest's per-section `state`/counters make the shrink visible. How
fine-grained the omission reporting should be, and how a Chain-less record
should be treated, is explicitly left named, not closed (`full-r6.README.md`
§The omission probe). One representation seam found while measuring: a record
whose only sweep-relevant rows are rejections reports sweeps as a RUN section
with an empty sweep set (`VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1`, as on
`full-r6-absent.md`) rather than reporting the sweep/negative omission — the
fixture's pre-registration prose says "`sweeps` reported absent" for that
record; the verdict (CLEAN, no drift) is the same either way, and the
representation question belongs to the r7 discussion.

## Evidence (this seat's battery, single pinned revision)

Everything below was run fresh-process from the lane cwd against gate
`0c3d51ed…`, re-checked identical before and after the battery; stdout verbatim
except `ts=` and elisions marked `…`.

Composed positive, default discovery binding the companion through the
record's own `## Meta` row (note the resolved `claims=` path in the header):

```text
$ bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.md --root ..
research-gate research-gate-r1 — ts=… — mode=verify-all — record=corpus/fixtures/full-r6.md — claims=/…/chousa-shokunin/corpus/fixtures/full-r6.claims.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=3/3
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/2 REJECTIONS_OK=2/2
VERIFY_ALL sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0)
exit=0
```

The same run with an explicit
`--claims corpus/fixtures/full-r6.claims.jsonl` differs only in the header's
`claims=` spelling (path as given vs resolved absolute) and `ts=`; every
SECTION line and the composed verdict are identical. Solo
reference runs for the same inputs print exactly the same tallies
(`VERDICT_BEARING_CLAIMS=3/3`; `RESOLVED_HOPS=3/3`; `VERIFIED_SWEEPS=1/2
REJECTIONS_OK=2/2`; structure counts `findings=0 drift=0 questions=1 sources=4
chains=3 claims=3 negatives=2 rejections=2 approvals=1`, which the manifest's
structure `tallies` object carries verbatim) — so the composed per-section
tallies are equal to the solo modes' by construction and by measurement.

Composed broken twin (two single-line defects, chain and sweeps):

```text
$ bash tools/research-gate.sh verify-all corpus/fixtures/full-r6-broken.md --root ..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=DRIFT findings=1 drift=1 tally=RESOLVED_HOPS=2/3
FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=2 … nearest_line=57 context=…
SECTION sweeps state=run verdict=DRIFT findings=1 drift=1 tally=VERIFIED_SWEEPS=1/2 REJECTIONS_OK=1/2
FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R2 missing=flip
VERIFY_ALL sections=4 run=4 absent=0 drift-sections=2 findings=2 drift=2
RESEARCH_GATE: DRIFT (sections=4 run=4 absent=0 drift-sections=2 findings=2 drift=2)
exit=1
```

The composed DRIFT names exactly the two dirty sections; structure and claims
stay green — the structure mode alone (r1 `verify`) closes this twin CLEAN
(fixture README §The tampered twin), so the composition is what found the
dirt.

Other checks in the same battery:

- Omission: `full-r6-absent.md` → CLEAN `run=3 absent=1` (verbatim above).
- Manifest append-only: three runs appended three lines; after each append the
  previous byte prefix was compared against its snapshot — `prefix1 preserved:
  YES`, `prefix2 preserved: YES`; python3 parsed every line, every line carried
  the schema, and each `record_sha256` matched the file bytes on disk (True ×3).
- Setup exits: missing manifest directory → exit 2; manifest path a directory →
  exit 2; `--json` missing its value → exit 2; a bound claims file that is not
  JSONL → claims section DRIFT (13 `CLAIM_RECORD_INVALID`), composed exit 1.
- Zero network: `strace -f -e trace=network` around one composed run (exit 0):
  **0** socket/connect/sendto/recvfrom lines in 4217 trace lines.
- Selftest: `RESEARCH_GATE_SELFTEST: PASS (64 cases)`, exit 0. Case lines 1-54
  are BYTE-IDENTICAL to the round-5 receipt
  (`corpus/evidence/sweeps-r5-20261016T011543Z-selftest.log`; `cmp` on the
  extracted case lines found no difference); the ten new cases (55-64) are the
  `tall` family: composed positive, tampered claims, structure-dirty, no
  claims binding (absent), claims JSONL as input, two manifest appends (line
  1 hash stability asserted by the runner), Meta-bound claims, Meta-declared
  but missing claims (`VERIFY_ALL_CLAIMS_UNRESOLVED`), and missing-record
  setup (exit 2) — `:3024-3084`.
- Second witness: the fixture README's own composed-run section independently
  records the same three composed outputs and the same `gate_sha256` at
  `0c3d51ed…` (`full-r6.README.md` §Composed run), and the receipts seat's
  lane manifest `corpus/evidence/verify-all-manifest.jsonl` holds the first
  real lane manifest lines: three appends at `0c3d51ed…` — `full-r6.md`
  CLEAN run=4 drift_sections=0, `full-r6-broken.md` DRIFT run=4
  drift_sections=2, `full-r6-absent.md` CLEAN run=3 absent=1 — each line valid
  JSON, matching the three composed states this note measures from scratch
  (the receipts seat owns that file and its `corpus/evidence/README.md` index
  entry, which were still being finalised when this note was last checked).

## What the composed CLEAN does not prove

The composition is a summary, not a stronger check: it inherits exactly the
limits of the four modes it runs — span fidelity is not claim truth (r2 note),
hop resolution is anchor existence (r3), the shared token-boundary matcher
still admits token-aligned shortening and non-ASCII-adjacent edges (r4), and a
CLEAN sweep is presence + local emptiness re-run, not command re-execution or
flip-condition quality (r5). The manifest adds durability and per-section
tallies, not new verification.

## Open items

- **Omission limit (r7 candidate, named above):** no assertion that an absent
  section should have been present; the claims-surface omission is the one
  measured to compose CLEAN here, and the sweeps-with-only-rejections
  representation is the fixture's named granularity question.
- **Nested execution cost (design, not debt):** one composed run spawns up to
  four fresh gate processes (one per run section); this buys tally identity by
  construction at a per-run process cost.
- Carried residuals from earlier rounds (unchanged here): in-root hardlinks
  bypass path canonicalization; no source size cap; the banner still reads
  `research-gate-r1` (cosmetic).
- **Receipt identity (round 1) — STILL OPEN.** These are lane-local evidence
  runs, not queue taskKey/expected-receipt bags; no `task_…` value may be
  invented and no Sighting is claimed. No scalar score, no promotion, no
  field-readiness claim. No commits by this seat.