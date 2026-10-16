# LOG.md — round-6 entry draft (parent-owned file; integrate under [PARENT] markers)

<!-- SCRIBE DRAFT — MEASURED FINAL. Before: round-5 gate sha256
     55adb92d0ba5ac958907fac6c4d5d6b0b50129703e866a5befbd9a32789f2ff2
     (== `git show HEAD:tools/research-gate.sh`), lane HEAD 1d1f56c. After:
     round-6 gate sha256
     0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8
     (+450 lines vs HEAD; stable ≥9 min, identical before and after this
     seat's battery). The wave moved through transient revisions (two of
     them functionally defective on the record path — the r6 note documents
     them); this seat's measurements cover only `55adb92d…` → `0c3d51ed…`.
     Lane HEAD still 1d1f56c; no commits by any seat. Scribe scratch
     /tmp/chousa-scribe-r6/ (declared ephemeral, cleaned at end of run).
     [PARENT] marks parent-only bindings. The debts section keeps the
     receipt-identity debt OPEN per the mission contract. -->

## 2026-10-16 — round-6 operability: `verify-all` composes one verdict; the record's state lands in the lane manifest

Round 6 executes the move round 5 registered: composition. Before it, a
record's full verification state required running `verify` / `verify-chain` /
`verify-sweeps` (and, for claims files, `verify-claims`) separately and
eyeballing four outputs; nothing composed them into one verdict and nothing
durable recorded them. The operator dispatched this wave directly in-session
(same routing as rounds 2–5; **no Sighting step was invoked**); receipt
identity from round 1 remains open and untouched by this round.

**Before.** At the round-5 revision (sha256 `55adb92d…`, lane HEAD `1d1f56c`),
measured by this seat, fresh-process CLI runs:

- `bash tools/research-gate.sh verify-all corpus/fixtures/sweeps-r5.md --root
  ..` → exit 2, stdout empty (0 bytes), stderr `research-gate: multiple
  record paths` + usage — the mode does not exist; `verify-all` parses as a
  positional record path and the fixture path is a second one.
- `bash tools/research-gate.sh verify corpus/fixtures/sweeps-r5.md --root ..
  --json /tmp/chousa-scribe-r6/manifest.jsonl` → exit 2,
  `research-gate: unknown flag: --json`. No manifest facility exists.
- No manifest: a lane-wide `find . -name '*manifest*' -not -path './.git/*'`
  returns nothing but interactive-session log noise (the word inside session
  JSONL). All four verify modes are zero-write at this revision: the only
  file redirections sit inside `run_selftest`'s mktemp dir
  (`tools/research-gate.sh:1634-1703`). `.ufo/round-5/chousa-goalwave.md:41`
  registers the manifest step as future work.
- The same fixture bytes through the solo modes (fresh process, this seat):
  `verify` on `sweeps-r5.md` and `sweeps-r5-broken.md` → both CLEAN
  `findings=0 drift=0`, exit 0; `verify-chain sweeps-r5.md` → `2/3` CLEAN
  exit 0; `verify-sweeps sweeps-r5.md` → `VERIFIED_SWEEPS=1/2
  REJECTIONS_OK=3/3` CLEAN exit 0; `verify-sweeps sweeps-r5-broken.md` →
  `0/1 + 0/1` DRIFT exit 1 (`SWEEP_REJECTION_INCOMPLETE` +
  `SWEEP_CLAIM_FALSE`); `verify-claims claims-r2.jsonl` → 17/17 CLEAN exit 0;
  selftest → `PASS (54 cases)` exit 0; A/B/C archives → each DRIFT exit 1
  (3/3).

**The move.** `tools/research-gate.sh` (uncommitted working tree, +450 lines
vs HEAD, gate `0c3d51ed…`): a fifth mode `verify-all <record> [--claims
PATH] [--json PATH] --root ..` (dispatch `:3102`; contract `:101-117`; usage
`:179-182`, `:211-218`). It runs every applicable mode as a FRESH gate
subprocess (`bash "$SELF" <mode>` — helpers `json_escape` `:1654`,
`json_counts` `:1674`, `verify_all_section` `:1692`, `verify_all` `:1724`)
over ONE input and composes one verdict: sections `structure` (always, for a
Markdown record) · `claims` (bound surface: the input itself when it is a
claims JSONL — no `##` section lines + ≥1 JSON-object line; else `--claims
PATH`; else a `## Meta` row named `claims`/`claims_file`/`claims-file`/
`claimset`, boundary-checked like a source, `:1758-1786`) · `chain` (when
`## Chain` exists) · `sweeps` (when `## Sweeps`, `## Negatives` or
`## Rejections` exists). An ABSENT section is printed `SECTION <name>
state=absent` and never drifts by itself; the composed roll is DRIFT iff any
RUN section drifts; run sections print `SECTION <name> state=run verdict=…
findings=… drift=… [tally=…]` (native tally lines: `VERDICT_BEARING_CLAIMS=`,
`RESOLVED_HOPS=`, `VERIFIED_SWEEPS=… REJECTIONS_OK=`), then `VERIFY_ALL
sections=4 run=N absent=N drift-sections=N findings=N drift=N` and exactly
one closing `RESEARCH_GATE:` line; exit 0/1/2 as before. `--json PATH`
appends (>>, never rewrites; the only write site, `:1846`) one JSON line —
schema `chousa-verify-all/v1`, UTC, record + gate SHA-256, per-section
state/verdict/tallies (+ native), composed verdict, run/absent/drift-section
counts. `--claims`/`--json` outside `verify-all` are refused (exit 2).

**Fixtures.** `corpus/fixtures/full-r6.md` (sha `878c2c50…`): every
gate-known section carried correctly, `## Meta` `claims_file` row binding
`full-r6.claims.jsonl`; `full-r6-broken.md` (`0f7e498c…`): differs in
exactly 3 lines — its own `claims_file` row, hop 2's anchor gaining an `s`
(`…operating costs.`), and R2's flip_condition cell emptied; `full-r6-absent.md`
(`39cdb2d7…`): no Sweeps/Negatives rows, no claims companion and no binding
(omission probe); companions `full-r6.claims.jsonl` /
`full-r6-broken.claims.jsonl` (one sha `45eb6ac2…`); `full-r6.README.md`
(`f56ef337…`) carries the pre-registered solo/composed expectations, the
inventory shas and a composed-run section. The earlier alias companion names
were pruned by their author mid-wave once the binding convention settled on
the Meta row.

**Selftest.** 54 → 64 cases, all PASS; the first 54 case lines byte-identical
(diff empty). New cases 55–64: `all-pass.md` claims-bound CLEAN (0), claims
tamper DRIFT (1), structure DRIFT via stubbed record (1), claims absent (0),
a claims JSONL as its own input (0), two manifest-append runs proving line 1
is never rewritten and the JSON parses (0), Meta-declared claims binding (0),
unresolvable Meta declaration `VERIFY_ALL_CLAIMS_UNRESOLVED` (1), and
no-such-record setup (2).

**Measurements after the move** (gate `0c3d51ed…`, sha identical before and
after the battery, stable ≥9 min; all fresh-process by this seat; verbatim):

```text
$ bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.md --root ..
research-gate research-gate-r1 — ts=2026-10-16T02:01:33Z — mode=verify-all — record=corpus/fixtures/full-r6.md — claims=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/full-r6.claims.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=3/3
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=3/3
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/2 REJECTIONS_OK=2/2
VERIFY_ALL sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0)
exit=0

$ bash tools/research-gate.sh verify-all corpus/fixtures/full-r6-broken.md --root ..
… (header; claims binds full-r6-broken.claims.jsonl)
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
… (header; claims=-)
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=absent
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=1/1
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1
VERIFY_ALL sections=4 run=3 absent=1 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=4 run=3 absent=1 drift-sections=0 findings=0 drift=0)
exit=0

$ bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.claims.jsonl --root ..
SECTION structure state=absent / SECTION claims state=run … tally=VERDICT_BEARING_CLAIMS=3/3 / SECTION chain state=absent / SECTION sweeps state=absent
VERIFY_ALL sections=4 run=1 absent=3 drift-sections=0 findings=0 drift=0   (CLEAN, exit 0)

solo modes, same bytes, tallies EQUAL the composed sections:
  verify full-r6.md          → CLEAN findings=0 drift=0 (q=1 src=4 ch=3 cl=3 neg=2 rej=2 appr=1)
  verify-claims companion    → VERDICT_BEARING_CLAIMS=3/3 CLEAN
  verify-chain full/broken   → RESOLVED_HOPS=3/3 CLEAN / 2/3 DRIFT
  verify-sweeps full/broken  → 1/2+2/2 CLEAN / 1/2+1/2 DRIFT
  verify-all sweeps-r5.md    → CLEAN run=3 absent=1 (claims absent; chain 2/3; sweeps 1/2+3/3)

manifest, 5 appends to a scratch file (/tmp/chousa-scribe-r6/after/manifest-test.jsonl):
  line 1 sha256 9da468d8… byte-stable across every append; head-4 prefix
  01fd1ccf… byte-stable across the 5th; all lines json.loads-valid; every
  record_sha256/gate_sha256 re-verified against the files; `>>` (:1846) the
  only write site; lane cut: corpus/evidence/verify-all-manifest.jsonl
  (3 lines, 2ed28f9f…, gate 0c3d51ed…, ts 02:04:09–14Z)

selftest                               → RESEARCH_GATE_SELFTEST: PASS (64 cases) ; exit 0 ; 1–54 byte-identical
regressions (all byte-identical modulo ts=):
  claims 17/17 CLEAN · chain 17/22 CLEAN + broken 1/2 DRIFT · sweeps
  1/2+3/3 CLEAN + broken 0/1+0/1 DRIFT · r1 verify on sweeps-r5 pair CLEAN ·
  A/B/C each DRIFT exit 1 (3/3)
exit contract probes                   → 8 probes exit 2 (no-record, missing-file,
  claims-missing, json-dir-missing, json-path-is-dir, json/claims outside
  verify-all, read-only manifest: "manifest append failed" + exit 2);
  CLEAN 0 / DRIFT 1 as above
zero network (strace -f -e trace=network, composed+manifest run)
                                       → 0 socket/connect/sendto/recvfrom lines (4339 traced) ; exit 0
```

The receipts seat's independent cut (stamp `20261016T020330Z`, five logs
under `corpus/evidence/`: selftest `e3b94e1c…`, full `c96ac4f5…`, broken
`83d7aef6…`, json `1db37149…`, live `ac4d3f8e…`) agrees with this seat's
battery wherever they overlap: same composed verdicts and per-section
tallies; manifest lines 0→3 with prefix compares YES; `PASS (64 cases)` with
the first 54 case lines byte-identical (`cmp` YES); `VERDICT_BEARING_EXPORTS=3/3`;
0 network syscalls.

**Named limits (measured by this seat; the note names the first).**
Absence is reported, never drift — and the claims section verifies the BOUND
surface, not the record's own Claims rows: `sweeps-r5.md` (Claims rows, no
companion) composes `claims state=absent` CLEAN. `sweeps` runs whenever
`## Rejections` exists even with zero sweep rows (`full-r6-absent.md` →
`0/0 + 1/1`); the fixture README's absent bullet says "claims and sweeps
reported absent" while its own table matches this run behavior (wording
nuance, non-blocking). The manifest append happens before the verdict; on a
read-only target the run exits 2 with `research-gate: manifest append
failed: <path>` and no verdict. No path confinement on `--json` (any
writable regular file whose dirname exists), no locking/fsync/rotation.
`VERIFY_ALL_SECTION_UNAVAILABLE` (sub-mode rc∉{0,1}) is defensive and was not
triggered by the selftest or this seat's probes. Cosmetic: `structure`/
`claims` SECTION lines carry no tally (the full counter dict is in the
manifest), and the sweeps `where=` display keeps the r5 80-char cap.

**Admission.** [PARENT: ADMIT/REJECT line + commit hashes; no scalar; axis
verdicts live in SCORECARD.md's round-6 sections.]

**Debt.** Receipt identity (round 1) STILL OPEN — no authentic queue
taskKey/expected receipt bag exists; mission acceptance is integrator-owned,
no `task_…` value was invented, proven receipt-backed completed rounds remain
0, operator target unchanged (≥100). Round-6 artifacts at draft time
(uncommitted): gate `0c3d51ed…` (+450), fixtures + README (shas above),
note `corpus/knowledge/verify-all-r6.md` (`9b9711cb…`), lesson
`corpus/lessons/2026-10-16-verify-all-composition.md` (`d55bb183…`),
`SKILL.md` verify-all row/prose (`834c9707…`), receipts manifest
`corpus/evidence/verify-all-manifest.jsonl` (`2ed28f9f…`, 3 lines) and the
five receipt logs `compose-r6-20261016T020330Z-*.log` (`e3b94e1c…` selftest /
`c96ac4f5…` full / `83d7aef6…` broken / `1db37149…` json / `ac4d3f8e…`
live), plus the `corpus/README.md` round-6 rows (`499d5f3a…`) and the
`corpus/evidence/README.md` round-6 receipts section (`ed94b72d…`) — the
last three landed after this seat's battery and agree with it where they
overlap. Integrate only what lands. Lane hygiene: no commits by seats.