# Round-6 lesson — one composed verdict: absence is reported, not clean, and the manifest only appends (2026-10-16 UTC; lane-local 2026-10-15)

Round: chousa-shokunin round 6, one operability/composition move:
`verify-all <record> --root PATH` runs every applicable mode as fresh gate
calls and composes ONE verdict (DRIFT iff any RUN section drifts; absent
sections reported, never drifting), and `--json PATH` appends the record's
verification state to a lane manifest (append-only jsonl). Lane HEAD `1d1f56c`
(unchanged; no commits by this seat). Gate under test — before:
`tools/research-gate.sh` sha256
`55adb92d0ba5ac958907fac6c4d5d6b0b50129703e866a5befbd9a32789f2ff2`
(committed at HEAD; recoverable as `git show HEAD:tools/research-gate.sh`);
after: sha256
`0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8`
(working tree, uncommitted, +450 lines vs HEAD; observed moving across the
wave `ae1e749e…`/`c5dafcfd…`/`e02bf859…`/`4f1c62f5…`/`ea3283f1…`/`3ff911dc…`
→ `0c3d51ed…`, sha-stable across my whole battery and re-checked at writing —
see Defects). Fixtures under test, all uncommitted: `corpus/fixtures/full-r6.md`
sha256 `878c2c50ec9efba5a103644bbc002a7029c9cbead9b95ec369913760d158212a`,
twin `full-r6-broken.md`
`0f7e498cf1f6f6192a2660b14e41a025dbf47972d3c37ffd414df008bb6b320f`, omission
probe `full-r6-absent.md`
`39cdb2d727c5f2e26093c7099f501ab21a8fae6ac9d2fa458161614ad4953d6c`, companions
`full-r6.claims.jsonl` / `full-r6-broken.claims.jsonl` (four alias names, one
sha256 `45eb6ac2cde9e3c33dd4d753e4da2cb660308dad8f00475a382a2881b89ddc40`),
README `full-r6.README.md` sha256 `f56ef337aa41137af6db3624066947d29bcf4364a228dfdcdc8cc0e701646216`
(pre-registered expectations; see its Honest boundaries). The receipts seat's
real lane manifest `corpus/evidence/verify-all-manifest.jsonl` (3 lines, gate
`0c3d51ed…`) was written during my battery and is cross-checked below.
verified-at: 2026-10-15/16 ~01:57-02:03Z, from the lane cwd; fresh-process CLI
runs; read-only local opens only; nothing was fetched or executed. Local date
at writing is 2026-10-15; the file name follows the dispatch's UTC-date form —
the earlier lessons use the local form (`2026-10-15-*`), so the integrating
parent may rename without touching content.
recheck:
`bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.md --root ..`
· `bash tools/research-gate.sh verify-all corpus/fixtures/full-r6-broken.md --root ..`
· `bash tools/research-gate.sh verify-all corpus/fixtures/full-r6-absent.md --root ..`
· `bash tools/research-gate.sh --selftest`

Raw probe outputs and scratch: `/tmp/chousa-lessons-r6/` (`gate-before.sha`,
`gate-settled.sha`, `before-*.out`, `smoke-positive.out`, `after-all-broken.out`,
`after-all-absent.out`, `all-claimsjsonl.out`, `all-absent-explicitclaims.out`,
`all-min2.out`, `rec2.md`/`rec3.md` under `root/`, `manifest.jsonl`,
`manifest-sentinel.jsonl`, `strace-verify-all.log`, `before-ok-cases.txt`,
`after-ok-cases.txt`). This seat wrote no lane file outside `corpus/lessons/`.
All script line numbers below are relative to `0c3d51ed…` unless stated.

## The claim, and the hole it names

Rounds 2-5 landed four verdict-bearing modes (structure, claims, chains,
sweeps) under one boundary policy and a 0/1/2 exit contract, but a record's
FULL verification state required running four modes by hand and eyeballing
four separate summaries, and nothing durable recorded that state. Round 6's
falsifiable claim: **before**, `verify-all` does not exist and `--json` is an
unknown flag; **after**, `verify-all <record> --root PATH` composes one verdict
whose per-section tallies equal the solo modes' tallies, the broken fixture
composes DRIFT naming exactly its two dirty sections while the other two stay
green, absent sections are reported (`state=absent`) and never drift,
`--json <path>` appends a well-formed line (record+gate SHA-256, UTC,
per-section tallies, composed verdict) with no rewrite path, all 54 prior
selftest cases stay byte-stable, and zero network.

## Before — measured at `55adb92d` (this seat)

- `bash tools/research-gate.sh verify-all corpus/fixtures/claims-r2.jsonl --root ..`
  → exit 2, stdout 0 bytes, stderr `research-gate: multiple record paths` plus
  the usage text listing five modes (`verify`, `verify-claims`, `verify-chain`,
  `verify-sweeps`, `--selftest`) — there is no `verify-all` mode; it degrades
  to a second positional record argument.
- `bash tools/research-gate.sh verify corpus/fixtures/sweeps-r5.md --root .. --json /tmp/m.jsonl`
  → exit 2, stderr `research-gate: unknown flag: --json`.
- `git show HEAD:tools/research-gate.sh | grep -c manifest` → 0;
  `… | grep -c -- "--json"` → 0. No manifest concept exists anywhere in the
  gate; no manifest file exists in the lane.
- Solo tallies at this revision (the comparison baseline): `verify` on
  `sweeps-r5.md` CLEAN exit 0; claims `VERDICT_BEARING_CLAIMS=17/17` CLEAN;
  chain `RESOLVED_HOPS=17/22` CLEAN; sweeps `VERIFIED_SWEEPS=1/2
  REJECTIONS_OK=3/3` CLEAN; `--selftest` → `RESEARCH_GATE_SELFTEST: PASS
  (54 cases)` exit 0, whose 54 `ok-case` lines are the byte-stability baseline.

## What landed — the rule at `0c3d51ed` (this seat)

The mode is documented in the file header (`:101-117`): every applicable mode
runs over one input as fresh gate calls (`verify_all_section` executes
`bash "$SELF" "$mode" …` — `:1692-1722`, call `:1696`), so each section tally
is that solo mode's tally by construction. Applicability is computed BEFORE
anything runs (`:1752-1791`):

- `structure` — always, for a Markdown record; a claims-JSONL input (no `##`
  headings, at least one JSON-object line, `:1752-1756`) makes it absent;
- `claims` — only when a claims surface binds: the input itself when it is a
  claims JSONL, else `--claims PATH`, else a `## Meta` row named
  `claims`/`claims_file`/`claims-file`/`claimset` whose value resolves under
  the corpus boundary like a source (`:1764-1789`); a declared-but-unresolvable
  binding is `VERIFY_ALL_CLAIMS_UNRESOLVED` (`:1787`) and runs the section as
  DRIFT rather than silently absent;
- `chain` — only when the record declares `## Chain` (`:1760`);
- `sweeps` — only when the record declares `## Sweeps`, `## Negatives` or
  `## Rejections` (`:1761-1763`).

Each RUN section is a subprocess; rc∉{0,1} or a missing/unparsable
`RESEARCH_GATE:` line makes that section DRIFT with a crit
`VERIFY_ALL_SECTION_UNAVAILABLE` finding (`:1700-1711`) — a section that
cannot be evaluated cannot compose to CLEAN. The composed rule (`:1810-1818`,
printed `:1868-1871`): absent sections are counted and reported; the verdict is
DRIFT iff any RUN section is DRIFT; exit 0/1 mirrors the verdict; exactly one
`RESEARCH_GATE:` line and one `VERIFY_ALL` line per run.

Verbatim composed runs (lane cwd, `--root ..`):

```text
$ bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.md --root ..
research-gate research-gate-r1 — ts=2026-10-16T01:57:52Z — mode=verify-all — record=corpus/fixtures/full-r6.md — claims=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/full-r6.claims.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=3/3
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/2 REJECTIONS_OK=2/2
VERIFY_ALL sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0)
exit=0

$ bash tools/research-gate.sh verify-all corpus/fixtures/full-r6-broken.md --root ..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=DRIFT findings=1 drift=1 tally=RESOLVED_HOPS=2/3
FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=2 source=research/deep-research-2026-09-28/B-multiagent-knowledge.md anchor=quote:"Track five axes separately: task competence, retention, evid" nearest_line=57 context=The strongest design implication is to make knowledge changes—not agent self-a
SECTION sweeps state=run verdict=DRIFT findings=1 drift=1 tally=VERIFIED_SWEEPS=1/2 REJECTIONS_OK=1/2
FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R2 missing=flip
VERIFY_ALL sections=4 run=4 absent=0 drift-sections=2 findings=2 drift=2
RESEARCH_GATE: DRIFT (sections=4 run=4 absent=0 drift-sections=2 findings=2 drift=2)
exit=1

$ bash tools/research-gate.sh verify-all corpus/fixtures/full-r6-absent.md --root ..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=absent
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=1/1
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1
VERIFY_ALL sections=4 run=3 absent=1 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=4 run=3 absent=1 drift-sections=0 findings=0 drift=0)
exit=0
```

(The first line of each run is abridged only in the header's `ts=`/`claims=`
fields where elided above; every SECTION/FINDING/VERIFY_ALL/RESEARCH_GATE line
is verbatim. The broken twin's chain defect is `…operating costs.` — an added
`s` the target never carries at `full-r6-broken.md:28`; the sweeps defect is
the empty `flip_condition` at `:58`; both named, both isolated to their
sections.)

Exit-contract and scope probes (all fresh processes):

| probe | exit | stderr |
|---|---|---|
| `verify-all` (no args) | 2 | `record path required (verify-all RECORD, --record, or CHOUSA_RECORD)` |
| `verify-all` missing record file | 2 | `record not found: …` |
| `--json` into nonexistent dir | 2 | `manifest directory not found: … (--json)` |
| `--json` pointing at a directory | 2 | `manifest path is not a regular file: … (--json)` |
| `--json` on a solo mode (`verify … --json`) | 2 | `--claims/--json are only valid with verify-all` (`:3123`) |

Claims-JSONL input composes as claims-only: `verify-all
corpus/fixtures/claims-r2.jsonl --root ..` → `VERDICT_BEARING_CLAIMS=17/17`,
`SECTION structure state=absent`, chain/sweeps absent, `run=1 absent=3`,
CLEAN exit 0. An explicit `--claims` on the omission probe turns the absent
section into a RUN one: `run=4 absent=0`, CLEAN exit 0.

## Tally equality — measured, not asserted

The header claims equality "by construction" (same CLI paths); I re-derived it
key by key from the manifest line's `tallies` against the solo `RESEARCH_GATE:`
summary lines at the same revision, for all ten run sections across the three
records: every shared key equal (e.g. composed sweeps
`hit=0 refused=0 invalid=0 rejections-ok=2 …` = solo; composed structure
counters `questions/sources/chains/claims/negatives/rejections/approvals` =
solo `verify` summary), and the `native` strings byte-equal
(`VERDICT_BEARING_CLAIMS=3/3`, `RESOLVED_HOPS=3/3` / `2/3`,
`VERIFIED_SWEEPS=1/2 REJECTIONS_OK=2/2` / `1/2`). A composed verdict with a
tally that diverges from the solo mode for the same bytes under the same root
would falsify this fixture pair; none did.

## The manifest — append-only, and only append-only

`--json PATH` writes one JSON line per run (`:1820-1849`): `schema`
`chousa-verify-all/v1`, UTC `ts`, `record`, `record_sha256`, `gate_sha256`
(both re-hashed at write time, `:1822-1823`), the per-section array (each
entry `state=run` with verdict/findings/drift/tallies/native, or
`{"name":…,"state":"absent"}`), and the composed
`verdict`/`sections_run`/`sections_absent`/`drift_sections`. The ONLY write to
the path is `printf '%s\n' "$line" >>"$JSON_ARG"` (`:1846`); every other
`JSON_ARG` use is a pre-check (`:1737-1743`). An append failure exits 2 with a
diagnostic (`:1847-1848`); if `sha256sum` is unavailable nothing is written
and the run exits 2 (`:1824-1827`). The manifest line is written before the
stdout summary, so a DRIFT run records before the exit-1.

Measured, four appends over one file (positive → broken → absent → positive
again): 4 lines, each `json.loads`-valid; `record_sha256` at each line equals
`sha256sum` of the record named; `gate_sha256` = the settled revision; `ts`
UTC; same inode throughout; the first three lines byte-identical to the
pre-append snapshot after the fourth append (`cmp` clean). A pre-seeded
foreign line (`{"sentinel":"foreign-line-must-survive"}`) survived as line 1
with the new line appended after it — the flag appends to whatever file is
named and validates nothing already in it. The selftest closes the same door
in its own terms: it memoizes line 1's sha256 across two appends and FAILs on
`line1-rewritten` (`:3008-3012`).

Verbatim first manifest line (line 1 of `/tmp/chousa-lessons-r6/manifest.jsonl`,
the positive run):

```text
{"schema":"chousa-verify-all/v1","ts":"2026-10-16T01:58:12Z","record":"corpus/fixtures/full-r6.md","record_sha256":"878c2c50ec9efba5a103644bbc002a7029c9cbead9b95ec369913760d158212a","gate_sha256":"0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8","sections":[{"name":"structure","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"findings":0,"drift":0,"questions":1,"sources":4,"chains":3,"claims":3,"negatives":2,"rejections":2,"approvals":1}},{"name":"claims","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"claims":3,"supported":3,"contradicted":0,"unsupported":0,"mismatched":0,"unproven":0,"refused":0,"invalid":0,"findings":0,"drift":0},"native":"VERDICT_BEARING_CLAIMS=3/3"},{"name":"chain","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"hops":3,"verified":3,"exempt":0,"anchor-missing":0,"refused":0,"invalid":0,"findings":0,"drift":0},"native":"RESOLVED_HOPS=3/3"},{"name":"sweeps","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"sweeps":2,"verified":1,"exempt":1,"hit":0,"refused":0,"invalid":0,"rejections":2,"rejections-ok":2,"findings":0,"drift":0},"native":"VERIFIED_SWEEPS=1/2 REJECTIONS_OK=2/2"}],"verdict":"CLEAN","sections_run":4,"sections_absent":0,"drift_sections":0}
```

The receipts seat's lane manifest `corpus/evidence/verify-all-manifest.jsonl`
(3 lines, written 02:00:58-02:01:04Z during my battery) is a second, real
instance: all three lines parse, name the fixture trio, carry the settled
`gate_sha256`, and reproduce the composed exposure above (line 2 DRIFT
`drift_sections=2`, line 3 CLEAN `sections_absent=1`).

## What held unchanged

- `--selftest` → `RESEARCH_GATE_SELFTEST: PASS (64 cases)`, exit 0; the first
  54 `ok-case` lines are byte-identical to the before run (`cmp` clean) —
  every r1-r5 case still passes verbatim. The 10 new cases (`:2906-3084`,
  runner `tall` `:2976`) exercise: all-run composed CLEAN with exact SECTION
  lines (55), a tampered claims companion DRIFTing only `claims` (56), a
  structurally missing Question DRIFTing only `structure` (57), claims-absent
  `run=3 absent=1` (58), claims-JSONL input `run=1 absent=3` (59), manifest
  append 1→2 lines with the line-1 hash memo (60/61), Meta-declared binding
  (62), unresolvable binding → `VERIFY_ALL_CLAIMS_UNRESOLVED` DRIFT (63),
  missing record → exit 2 (64).
- Regressions at the new revision: claims `17/17` CLEAN exit 0; chain `17/22`
  CLEAN exit 0; chain control `1/2` DRIFT exit 1; sweeps `1/2 REJECTIONS_OK=3/3`
  CLEAN exit 0; sweeps control DRIFT exit 1; r1 archive observable
  `VERDICT_BEARING_EXPORTS=3/3`.
- Zero network: `strace -f -e trace=network` around `verify-all full-r6.md
  --json …` → 0 `socket(`/`connect(`/`sendto(`/`recvfrom(` lines in a
  4,339-line trace; exit 0.
- Gate sha stable at `0c3d51ed…` through the whole battery and re-checked at
  writing; inode and prefix tests above.

## Method statement — what a composed CLEAN establishes, and what it does not

A composed CLEAN establishes: every RUN section's solo-mode verdict is CLEAN
for the same bytes under the same root, with tallies equal to that solo run;
no section is unavailable; the absent sections are exactly those reported
`state=absent`. What it does NOT establish, stated wherever a composed CLEAN
is cited:

- **Not coverage of absent sections — the omission limit (named r7
  candidate).** `claims` absent means the record's `## Claims` rows were
  checked only structurally (the r1 counter) and NO span was verified against
  any source. Reachability, measured: r1 structure itself requires a
  `## Claims` table (`CLAIM_TABLE_ABSENT`, probe `rec3.md`) and a
  `## Rejections` section (`REJECTION_DROPPED`), and refuses claims-without-
  chain (`CHAIN_ABSENT`, probe `rec2.md`); so for a structurally-CLEAN
  Markdown record the only reachable absence is `claims` (no binding) — chain
  and sweeps always run, and a claims-JSONL input is the other absent-heavy
  class (`run=1 absent=3`). A future move could require a claims binding when
  the table is non-empty, or expose row-count-vs-verified-count more loudly in
  the composed line; today the exposure is `state=absent` plus the structure
  counter. This lesson records the limit as measured, not as a defect against
  the landed contract.
- **No new verification semantics.** Every bound of rounds 1-5 stands per
  section unchanged (bytes exist at token boundaries; anchors resolve;
  rejections carry reason+flip; named local sweeps re-run empty; structure is
  shape). Composition adds a rollup, not a check.
- **Not atomic.** Sections are sequential subprocesses; a crash mid-run leaves
  a partial stdout with no composed verdict line (the section-level
  `VERIFY_ALL_SECTION_UNAVAILABLE` path covers rc∉{0,1} and unparsable
  verdicts, `:1700-1711`). The manifest line is written only after all
  sections have run, and written before the stdout summary.
- **The manifest is not an audit trail of history.** It appends exactly what a
  caller logged, to exactly the file named; pre-existing foreign lines are
  preserved unvalidated (sentinel probe) and nothing ever reads back prior
  lines. `ts` is the write time, `record_sha256`/`gate_sha256` bind the bytes
  and the gate that produced the line; a later edit to the record falsifies
  the recorded state (the r5 time-stability bound, now in JSON).
- **Not source truth, semantics, or promotion.** Nothing in a composed CLEAN
  or a manifest line adjudicates meaning, authorship, or adequacy; no scalar
  score, no SHONEN box, no receipt.

## Defects and follow-ups noted (outside this seat's write scope)

- **Companion alias files.** Four byte-identical claims companions exist
  (`full-r6.claims.jsonl`, `full-r6-broken.claims.jsonl` and the two
  `-claims` aliases); the landed binding is the fixture's `## Meta`
  `claims_file` row (not filename auto-discovery), so the README's "prune the
  other" instruction is fixture-author scope. The mode reads only what binds.
- **Writing-window churn (acceptance-timing discipline).** The gate moved
  across 8+ revisions in ~15 minutes; my polling observed
  `ae1e749e…`→`c5dafcfd…`→`e02bf859…`→`4f1c62f5…`→`ea3283f1…`→`3ff911dc…`→
  `0c3d51ed…`. The note-writer's record (`corpus/knowledge/verify-all-r6.md`)
  states two transient revisions were functionally defective on the RECORD
  path (`4f1c62f5…` aborted on every Markdown input; `ea3283f1…`'s Meta
  binding matched table column names) — I observed those shas but did not
  re-run them (gone from the tree), so that pair is attributed to the
  note-writer, not measured here. The settled `0c3d51ed…` closes PASS
  (64 cases) across my battery; acceptance must pin the sha (the fixture
  README pins its authoring revision `55adb92d…` and pre-registers the
  composed verdict; the note and this lesson pin the settled `0c3d51ed…`).
- **Display shape (cosmetic).** The composed stdout's `structure`/`claims`
  SECTION lines carry only findings/drift (the full counter dict lives in the
  manifest's `tallies`); the sweeps `where=` cells keep the r5 80-character
  display cap.
- **Round-1 receipt identity remains open** (receipts-writer's lane manifest
  lines are lane evidence, not a mission receipt); nothing in this lesson
  mints or counts a receipt.

## Gate

### Candidates

1. This lesson.
2. The reading "a composed CLEAN proves the record is fully verified".
3. The reading "the manifest is a complete audit trail of a record's
   verification history".
4. The reading "an absent section is a passed section".
5. A new `corpus/QUALITY.md` criterion from this round's rejections.
6. Promotion marks / SHONEN boxes.

### Admitted

- Candidate 1, this note
  (`corpus/lessons/2026-10-16-verify-all-composition.md`; sibling lessons use
  the lane-local `2026-10-15-*` form, so the integrating parent may rename).

### Rejected, with reasons

- Candidate 2 — overclaim; falsified by the omission probe: `full-r6-absent.md`
  composes CLEAN with `claims state=absent` and no span ever verified, and by
  the reachability probes (`rec2.md` `CHAIN_ABSENT`, `rec3.md`
  `CLAIM_TABLE_ABSENT`/`REJECTION_DROPPED`).
- Candidate 3 — overclaim; the manifest appends caller-supplied lines, keeps
  foreign lines unvalidated (sentinel probe), is never read back, and binds
  only what a run records, not what happened before or after it.
- Candidate 4 — category error; `state=absent` is reported and never drift,
  but it is also never verification — the composed line exposes
  `sections_absent`, and the structure mode independently counts the
  unverified `## Claims` rows.
- Candidate 5 — no QUALITY-bar miss produced this round's rejections.
- Candidate 6 — refused; this seat grants nothing and no non-author spot-check
  exists.

### Spot-check

**Unavailable — measured outcome, not omission** (as in rounds 1-5: every
reviewer is a lane seat; no non-author sampled an admit and a reject).
Discernment remains unchanged.

## Verification boundary (parent-owned)

Integration counts, commit hashes, the round report/SCORECARD/LOG entries and
any frozen-replay evidence are parent-owned; nothing here pre-claims them. The
before/after pair measured here is: `55adb92d…` (committed at HEAD `1d1f56c`)
→ `0c3d51ed…` (working tree, uncommitted at this writing, sha-stable across the
battery). Mission acceptance remains blocked on round-1's receipt identity
(still open); no `task_…` value is invented and no receipt was counted. Later
corrections land as append-only errata blocks (`QUALITY.md:4`).
