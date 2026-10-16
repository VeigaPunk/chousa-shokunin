# chousa-shokunin — corpus/evidence

Receipts for the chousa moves: rounds 2-7 — claim-vs-source verification
(round 2), chain-hop resolution (round 3), token-boundary matching semantics
(round 4), rejection/sweep verification (round 5), verify-all composition
(round 6), reference integrity (round 7). Each
receipt is a machine-cut capture of public-CLI runs: UTC stamp, exact command,
exit code, pinned gate SHA-256, and the verbatim stdout. Local files only — no
external fetch, no network.

## Round-2 claim-verification receipts — stamp 20261015T233027Z

Revision under test: `tools/research-gate.sh` sha256
`03a3324455852ea0025115cb0e3ba9c8cdea10da5edc051c4738854a27c14be0`
(lane HEAD `6344569`). Fixture `corpus/fixtures/claims-r2.jsonl` sha256
`23d078cbfd032ec5ee7de5c21de65eba3a3cd2989a78281ff61bc6db62188802`; its
contract is `corpus/fixtures/claims-r2.README.md` sha256
`44d8a890406f0802986adb7b92c653c53d2548ffe7976911250f01c76c48e3e7`.

| Receipt (sha256) | Shows | Key result |
|---|---|---|
| `claims-r2-20261015T233027Z-fixture.log` (`cef0297a…`) | fixture inventory, pinned inputs, two independent byte-checks | `counts {'supported': 13, 'contradicted': 2, 'unsupported': 2} bad []`; independent span check 17/17 ok |
| `claims-r2-20261015T233027Z-selftest.log` (`b202d835…`) | full `--selftest` | `RESEARCH_GATE_SELFTEST: PASS (30 cases)`, exit 0; case lines 1–20 byte-identical to the r1 baseline |
| `claims-r2-20261015T233027Z-gate.log` (`5b8c9880…`) | round-1 regression over the three archived inputs (frozen clock) | each exit 1 with one `RESEARCH_GATE: DRIFT` summary; `VERDICT_BEARING_EXPORTS=3/3`; all three byte-identical to the frozen r1 baseline |
| `claims-r2-20261015T233027Z-live.log` (`672797bb…`) | before-state (r1 gate on the claims file), live `verify-claims`, four negative controls | live `VERDICT_BEARING_CLAIMS=17/17` + `RESEARCH_GATE: CLEAN (claims=17 … mismatched=0)`, exit 0; each control DRIFT, exit 1 |

Before → after in one line: the r1 gate on the same claims file is
structure-only (`FINDING RECORD_SCHEMA_INVALID`, `… CLAIM_TABLE_ABSENT`, DRIFT
findings=5); the new `verify-claims` mode adjudicates each claim's verbatim span
against its cited source and closes CLEAN with `claims=17 verified=17`.

### Negative controls (recorded in the live receipt)

Each control is a scratch copy of the fixture (deltas are printed in the
receipt); every one drifts with exit 1.

| Control | Delta | Finding | Summary |
|---|---|---|---|
| tampered span | A03 `nine years` → `ten years` | `CLAIM_SPAN_NOT_FOUND` | 16/17, DRIFT |
| external URL source | X01 `https://example.invalid/x.md` appended | `CLAIM_SOURCE_EXTERNAL` (crit), refused, never fetched | 17/18, DRIFT |
| out-of-corpus source | X02 `/etc/hostname` appended | `CLAIM_SOURCE_OUT_OF_CORPUS` (crit) | 17/18, DRIFT |
| contradicted without marker | A05 `marker` removed | `CONTRADICTION_MARKER_ABSENT` | 16/17, unproven=1, DRIFT |

## Round-1 evidence

- `round-1/expected.json`: archive content digests and expected CLI verdicts
  for the three baseline inputs.

The round-1 acceptance and final-intake JSON live under
`../.ufo/evidence/round-1/` (lane evidence dir).

## Re-run recipe

From the lane root, local only. Exit contract for every run: 0 CLEAN,
1 DRIFT, 2 setup/usage.

```bash
# 0. pin the revision (receipts were cut at this sha)
sha256sum tools/research-gate.sh
#   03a3324455852ea0025115cb0e3ba9c8cdea10da5edc051c4738854a27c14be0

# 1. fixture + live claim verification
bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..
#   expect: 17 CLAIM lines all verdict=match, VERDICT_BEARING_CLAIMS=17/17,
#   RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0), exit 0

# 2. selftest (honours ${TMPDIR:-/tmp}; set TMPDIR if /tmp is crowded)
bash tools/research-gate.sh --selftest
#   expect: RESEARCH_GATE_SELFTEST: PASS (30 cases), exit 0

# 3. round-1 regression count (the scorecard observable)
python3 -c 'import subprocess; names=("A-shokunin-tradition.md","B-multiagent-knowledge.md","C-rank-taxonomy.md"); rows=[subprocess.run(["bash","tools/research-gate.sh","verify","../research/deep-research-2026-09-28/"+n,"--root",".."],capture_output=True,text=True) for n in names]; print("VERDICT_BEARING_EXPORTS=%d/3" % sum(r.returncode==1 and sum(s.startswith("RESEARCH_GATE: DRIFT (") for s in r.stdout.splitlines())==1 for r in rows))'
#   expect: VERDICT_BEARING_EXPORTS=3/3

# 4. fixture provenance byte-check without the gate
#   run the python block in corpus/fixtures/claims-r2.README.md §Re-run
#   expect: counts {'supported': 13, 'contradicted': 2, 'unsupported': 2} bad []
```

### Notes

- Receipts pin gate revision `03a33244…`. If `tools/research-gate.sh` is edited
  again, re-run the recipe above and re-cut; a superseded receipt is not a
  claim about the later revision.
- The receipts were machine-cut by `cut-receipts.sh` (seat scratch, retained
  during the wave at `/home/vgpnk/.cache/chousa-r2/cut-receipts.sh`; not a lane
  file). The recipe above is self-contained and needs no scratch dir.
- Where a receipt records a path under `/home/vgpnk/.cache/chousa-r2/`, that is
  the seat scratch dir: the host `/tmp` intermittently returned `Disk quota
  exceeded`, so scratch and the gate's `TMPDIR` were pointed there. The
  receipts' own runs resolve all sources inside the fleet root.
- The round-2 scribe draft referred to `corpus/evidence/round-2/`; these
  receipts live directly under `corpus/evidence/` as
  `claims-r2-<UTCstamp>-{fixture,selftest,gate,live}.log`, per the
  receipts-writer seat directive. Parent integration can move them, but the
  receipt contents pin their own names.

## Round-3 chain-resolution receipts — stamp 20261015T235623Z

Revision under test: `tools/research-gate.sh` sha256
`67daf85ecc49c4c7accbee9534c31b0734061b7f329e8de7a98254a57f9d6084`
(lane HEAD `0aa794d`; the fixtures' README pins the same revision). Fixtures:
`corpus/fixtures/chain-r3.md` sha256
`06115f2f8e6db3c60034411dc6be42c4e0887352b09ab9cbd7f760801237ba07`,
`corpus/fixtures/chain-r3-broken.md` sha256
`b66222a16d4c5323ee6932839ff5746af5f716f36372af506755aed18e0f5c6a`;
contract `corpus/fixtures/chain-r3.README.md` sha256
`72dbee4e1d8c22df898842f2edf406769c8aa7894fcaecdfe5922137f867292a`.

| Receipt (sha256) | Shows | Key result |
|---|---|---|
| `chain-r3-20261015T235623Z-fixture.log` (`14f24aa3…`) | fixture inventory, pinned inputs, the README-documented byte-check extracted verbatim, the receipts-writer independent record checker | README check: `chain-r3.md: RESOLVED_HOPS=17/22 bad_hops=[]`, `chain-r3-broken.md: RESOLVED_HOPS=1/2 bad_hops=['2']`; independent checker exit 0 (22 hops re-derived: 17 resolved anchors present, near-miss bytes absent from C, jin'i form present at C:118) |
| `chain-r3-20261015T235623Z-selftest.log` (`db48f070…`) | full `--selftest` | `RESEARCH_GATE_SELFTEST: PASS (40 cases)`, exit 0; case lines 1–30 byte-identical to the r2 selftest stdout |
| `chain-r3-20261015T235623Z-gate.log` (`8d29babb…`) | round-1 regression over the three archived inputs + the intake record (frozen clock) | each archived input exits 1 with one `RESEARCH_GATE: DRIFT` summary, all three byte-identical to the frozen r1 baseline; `VERDICT_BEARING_EXPORTS=3/3`; intake `CLEAN`, byte-identical to the r1 acceptance row (ts-normalized) |
| `chain-r3-20261015T235623Z-live.log` (`8fc99012…`) | before-state (r2 gate on both records), live `verify-chain`, four negative controls, strace, verify-claims byte-stability | live `chain-r3.md`: `RESOLVED_HOPS=17/22` + `RESEARCH_GATE: CLEAN (hops=22 verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0)`, exit 0; broken control: `RESOLVED_HOPS=1/2` + `CHAIN_ANCHOR_NOT_FOUND`, DRIFT, exit 1; controls as tabulated below; strace: 0 network syscalls; `verify-claims` byte-identical to the r2 stdout after ts normalization |

Before → after in one line: the r2 gate passes both chain records structurally
(`RESEARCH_GATE: CLEAN`, exit 0) — including the broken one whose hop claims
`resolved` while citing anchor bytes the target never carries; `verify-chain`
adjudicates every resolved hop's anchor bytes (line/quote) against its cited
source under the corpus boundary, reports the miss with
`nearest_line`/`context`, keeps unresolved/marked hops exempt-but-counted, and
closes DRIFT.

### Negative controls (recorded in the live receipt)

| Control | Delta | Result (exit) |
|---|---|---|
| tampered quote anchor | hop 3 `kiwami semantics` → `kiwami semanticsX` | `CHAIN_ANCHOR_NOT_FOUND` on hop 3, `RESOLVED_HOPS=16/22`, DRIFT (1) |
| out-of-corpus source | hop 1 `S1` → `/etc/hostname` | `CHAIN_SOURCE_OUT_OF_CORPUS` severity=crit, refused, `RESOLVED_HOPS=16/22`, DRIFT (1) |
| external URL source | hop 1 `S1` → `https://example.invalid/x.md` | `CHAIN_SOURCE_EXTERNAL` severity=crit, "url source refused (no external fetch)", refused, DRIFT (1) |
| resolved hop marked unresolved | hop 2 `resolved` → `unresolved` | exempt but counted: `RESOLVED_HOPS=16/22`, `CLEAN (hops=22 verified=16 exempt=6)`, exit 0 |

### Re-run recipe

From the lane root, local only. Exit contract: 0 CLEAN, 1 DRIFT, 2 setup.

```bash
sha256sum tools/research-gate.sh
#   67daf85ecc49c4c7accbee9534c31b0734061b7f329e8de7a98254a57f9d6084
bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..
#   expect: RESOLVED_HOPS=17/22; CLEAN (hops=22 verified=17 exempt=5 …); exit 0
bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3-broken.md --root ..
#   expect: RESOLVED_HOPS=1/2; DRIFT (… anchor-missing=1 …); exit 1
bash tools/research-gate.sh verify corpus/fixtures/chain-r3-broken.md --root ..
#   expect (pre-move hole): CLEAN, exit 0
bash tools/research-gate.sh --selftest
#   expect: RESEARCH_GATE_SELFTEST: PASS (40 cases), exit 0
# the fixture README's gate-free byte-check (see corpus/fixtures/chain-r3.README.md §Re-run)
#   expect: chain-r3.md: RESOLVED_HOPS=17/22 bad_hops=[];
#           chain-r3-broken.md: RESOLVED_HOPS=1/2 bad_hops=['2']
```

### Notes

- Receipts pin gate revision `67daf85e…`; a later gate edit supersedes them —
  re-run the recipe above and re-cut.
- Scratch for this cut lived at `/home/vgpnk/.cache/chousa-r3/` (cut script,
  control copies, `TMPDIR`) because the host `/tmp` is a quota-limited tmpfs;
  the receipts' runs resolve all sources inside the fleet root.
- The receipts-writer independent record checker is
  `/home/vgpnk/.cache/chousa-r3/adapter-chaincheck.py`, separate from the
  fixture README's own gate-free checker; both agree on both records.
- Receipt identity for this round remains a lane-local log; no `task_…` value
  is invented and the round-1 receipt blocker stands (operator-side).

## Round-4 boundary-hardening receipts — stamp 20261016T003332Z

Revision under test: `tools/research-gate.sh` sha256
`6b83705b02fe11e98b8b4aeb43fe718ff9910d21cee16d87366cef648a3960b2` (lane HEAD
`09153d1`; a stable revision — sampled unchanged across the cut). Before-state
runs use the round-3 revision `67daf85e…`, taken as a scratch snapshot that is
reproducible from git:
`git show cc9fe8f:tools/research-gate.sh | sha256sum` → `67daf85e…`.
Fixtures unchanged from round 2/3: `corpus/fixtures/claims-r2.jsonl` sha256
`23d078cbfd032ec5ee7de5c21de65eba3a3cd2989a78281ff61bc6db62188802`,
`corpus/fixtures/chain-r3.md` sha256
`06115f2f8e6db3c60034411dc6be42c4e0887352b09ab9cbd7f760801237ba07`,
`corpus/fixtures/chain-r3-broken.md` sha256
`b66222a16d4c5323ee6932839ff5746af5f716f36372af506755aed18e0f5c6a`.
Attack/legit copies are single-delta scratch rewrites under `/tmp/chousa-r4/att/`
(sha256 pinned inside each receipt; declared ephemeral scratch).

| Receipt (sha256) | Shows | Key result |
|---|---|---|
| `boundary-r4-20261016T003332Z-selftest.log` (`897e969c…`) | full `--selftest`, case-line stability vs the r3 stdout | `RESEARCH_GATE_SELFTEST: PASS (44 cases)`, exit 0; case lines 1–40 byte-identical to the r3 selftest; new cases 41–44 = `claims-boundary-pass`/`-fail`, `chain-pass-boundary`/`-fail` on the gate's own `lib/boundary.md` fixture |
| `boundary-r4-20261016T003332Z-claims.log` (`b37c2ca5…`) | canonical fixture, three attack controls, two legit controls | canonical `VERDICT_BEARING_CLAIMS=17/17` + `CLEAN` exit 0 (unchanged); each attack DRIFT `16/17` with one `CLAIM_SPAN_NOT_FOUND` at the line-aware report; legit controls `19/19` CLEAN |
| `boundary-r4-20261016T003332Z-chain.log` (`e3935a26…`) | canonical fixture, broken control, four attack controls, legit control | canonical `RESOLVED_HOPS=17/22` + `CLEAN` exit 0 and broken control `1/2` DRIFT (both unchanged); each attack DRIFT `16/22` with `CHAIN_ANCHOR_NOT_FOUND`/`anchor-missing`; legit control `18/23` CLEAN |
| `boundary-r4-20261016T003332Z-attacks.log` (`40e02b6b…`) | every attack copy under both gates + shared-rule evidence + gate-free checker | each attack closes CLEAN/exit 0 under the r3 revision and DRIFT/exit 1 under the landed one; helper block `tok_word_char`/`tok_left_ok`/`tok_right_ok`/`tok_span_at` printed verbatim with both call sites (`:907` claims span, `:1060` chain quote); independent checker: all 11 copies classified without the gate, `BOUNDCHECK_SUMMARY: all copies agree`, exit 0 |
| `boundary-r4-20261016T003332Z-live.log` (`c0d187f9…`) | pre-move structural hole, r1 archive observable, intake, cross-round stability, strace | r3 gate still passes the broken chain record structurally (`RESEARCH_GATE: CLEAN`, exit 0); archives each exit 1, `VERDICT_BEARING_EXPORTS=3/3`, stdout byte-identical to the r3 gate receipt (ts-normalized); intake CLEAN exit 0; claims/chain stdout byte-identical to the r2/r3 live receipts; `strace` 0 network syscalls |

Before → after in one line: under the round-3 substring semantics a citation
span or quote anchor that is a truncated, padded or glued variant of real source
text still resolved (seven single-delta demonstrably-CLEAN attack copies); under
the landed revision both `verify-claims` spans and `verify-chain` quote anchors
match only at a documented token boundary, so every one of those copies now
drifts with the line-aware report while the canonical fixtures, the broken
control, the r1 archive observable and the legit boundary controls are unchanged.

### Attack controls (recorded in the attacks receipt and re-run in claims/chain)

| Control (copy) | Delta | r3 gate (before) | landed gate (after) |
|---|---|---|---|
| claims/trunc-midtoken | A03 span cut mid-token: `…for nine yea` | CLEAN 17/17 (0) | DRIFT 16/17 (1), A03 `unsupported`, `nearest_line=81` |
| claims/glue-pad | A03 span glued both edges: `r carver’s career: … independentl` | CLEAN 17/17 (0) | DRIFT 16/17 (1), A03 `unsupported`, `nearest_line=81` |
| claims/trunc-hyphen | C06 span ends `…translating “jin’i` (next byte `-`) | CLEAN 17/17 (0) | DRIFT 16/17 (1), C06 `unsupported`, `nearest_line=53` |
| chain/trunc-midtoken | hop 3 anchor `…kiwami semantic` (one byte dropped) | CLEAN 17/22 (0) | DRIFT 16/22 (1), hop 3 `anchor-missing`, `nearest_line=35` |
| chain/trunc-hyphen | hop 14 anchor ends `…shokunin → jin’i` | CLEAN 17/22 (0) | DRIFT 16/22 (1), hop 14 `anchor-missing`, `nearest_line=52` |
| chain/trunc-apostrophe | hop 14 anchor ends `…shokunin → jin` | CLEAN 17/22 (0) | DRIFT 16/22 (1), hop 14 `anchor-missing`, `nearest_line=52` |
| chain/glue-start | hop 6 anchor prefixed `n. Track …` (glued into `evaluation`) | CLEAN 17/22 (0) | DRIFT 16/22 (1), hop 6 `anchor-missing`, `nearest_line=57` |
| claims legit L1+L2 | span followed by `,` (B:79) · span bounded by `(` `)` with slashes/apostrophe/hyphen inside (A:35) | CLEAN 19/19 (0) | CLEAN 19/19 (0) |
| chain legit hop 23 | quote followed by `,` (B:79) | CLEAN 18/23 (0) | CLEAN 18/23 (0) |

### Re-run recipe

From the lane root, local only. Exit contract for every run: 0 CLEAN,
1 DRIFT, 2 setup/usage.

```bash
sha256sum tools/research-gate.sh
#   6b83705b02fe11e98b8b4aeb43fe718ff9910d21cee16d87366cef648a3960b2
bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..
#   expect: 17/17, CLEAN, exit 0
bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..
#   expect: RESOLVED_HOPS=17/22, CLEAN, exit 0
bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3-broken.md --root ..
#   expect: RESOLVED_HOPS=1/2, DRIFT, exit 1
bash tools/research-gate.sh --selftest
#   expect: RESEARCH_GATE_SELFTEST: PASS (44 cases), exit 0
# before-state gate for the attack pairs (round-3 revision, from git):
git show cc9fe8f:tools/research-gate.sh > /tmp/chousa-r4/research-gate-r3-67daf85e.sh
sha256sum /tmp/chousa-r4/research-gate-r3-67daf85e.sh
#   expect: 67daf85ecc49c4c7accbee9534c31b0734061b7f329e8de7a98254a57f9d6084
# rebuild the single-delta copies and re-derive their classification without the gate:
python3 /tmp/chousa-r4/make-fixtures.py   # prints each delta and sha256
python3 /tmp/chousa-r4/boundcheck.py "$PWD" /tmp/chousa-r4/att
#   expect: BOUNDCHECK_SUMMARY: all copies agree, exit 0
```

### Notes

- Receipts pin gate revision `6b83705b…`; a later gate edit supersedes this
  stamp — re-run the recipe above and re-cut.
- Scratch for this cut lived at `/tmp/chousa-r4/` (generator, checker, the r3
  snapshot, the single-delta copies, `TMPDIR`): this round's `/tmp` writes
  succeeded, so no `$HOME/.cache/chousa-tmp` fallback was needed. The receipts
  are self-contained; the before-state gate is recoverable from git as shown.
- The gate-free checker `/tmp/chousa-r4/boundcheck.py` re-implements the
  documented rule independently of the gate; the canonical fixture's expect
  fields are its ground truth and the attack/legit copies carry explicit
  expected classifications for their single deltas.
- The boundary rule and its character class are documented in the gate header
  and in the helper comment block (`tools/research-gate.sh:68-86, 765-831`);
  the same helper serves both modes, so there is one rule, not two.
- Receipt identity for this round remains a lane-local log; no `task_…` value
  is invented and the round-1 receipt blocker stands (operator-side).

## Round-5 rejection/sweep receipts — stamp 20261016T011543Z

Revision under test: `tools/research-gate.sh` sha256
`55adb92d0ba5ac958907fac6c4d5d6b0b50129703e866a5befbd9a32789f2ff2` (lane HEAD
`45f8f65`; the sha was sampled stable before and after every run in these
receipts — 26 pinned runs, no mid-run change). Before-state runs use the
round-4 revision, recoverable from git:
`git show 45f8f65:tools/research-gate.sh` → sha256
`6b83705b02fe11e98b8b4aeb43fe718ff9910d21cee16d87366cef648a3960b2`,
executed from a lane shadow (`/tmp/chousa-r5-evidence/lane-shadow`, symlinks
`corpus/` → lane corpus and `research/` → fleet research) so the records'
lane- and fleet-root-relative pointers resolve exactly as they do in place —
a `/tmp` copy of the gate changes its own `LANE_ROOT` and would misreport
lane-relative pointers as unresolved. Fixtures: `corpus/fixtures/sweeps-r5.md`
sha256 `025352b75b7b109147fee8b8eb13b4f74eaa1550489e83166ce1dd59cfb14907`,
`corpus/fixtures/sweeps-r5-hit.md` sha256
`89650988074e4c371aada8e1fe77cd02d4fa85bc0c3d0a40dc21e12e1a0f78cd`,
`corpus/fixtures/sweeps-r5-broken.md` sha256
`f74ea3247e069e711278bb81addda468045053cfe556d8f5a204f3b9ff7abc0c`; contract
`corpus/fixtures/sweeps-r5.README.md` sha256
`e9178651254841b86e46e98ba4566b568df662ed8c541197ae150f5aba1ebbca`.
Control copies were single-delta rewrites of `sweeps-r5.md` under
`/tmp/chousa-r5-evidence/ctl/` (sha256 in the live receipt); the independent
checker is `/tmp/chousa-r5-evidence/sweepcheck.py` (scratch, gate-free).

| Receipt (sha256) | Shows | Key result |
|---|---|---|
| `sweeps-r5-20261016T011543Z-selftest.log` (`052b15da…`) | full `--selftest`; case-line stability vs the round-4 selftest stdout | `RESEARCH_GATE_SELFTEST: PASS (54 cases)`, exit 0; the first 44 ok-case lines are **byte-identical** to the round-4 receipt (`cmp` YES); new cases 45–54 = `sweeps-pass`/`-fail-planted-hit`/`-fail-rejection-incomplete`/`-fail-unnamed`/`-fail-out-of-corpus`/`-fail-unresolved-id`/`-fail-counting`/`-pass-cell-command` + two setup exits |
| `sweeps-r5-20261016T011543Z-fixture.log` (`b00b54ac…`) | fixture inventory (3 rejections + 2 sweeps; 1 + 1 broken); the archive set empty of URLs (`grep` exit 1, zero matches); the record's own W1 re-run by glob from the fleet root (zero hits); the planted hit file on disk with `ghost-sweep-token`; export pins matching the README; a README-vs-record block printing the record's Sweeps rows; independent gate-free re-derivation | independent verdicts `canonical=CLEAN broken=DRIFT`; exports `9033857d…/6d8dbddd…/e48fe70f…` match the README |
| `sweeps-r5-20261016T011543Z-broken.log` (`061c1d00…`) | the tampered control under the old and the landed revision | r4 `verify` CLEAN exit 0 (the hole, both broken cells invisible) → landed `verify-sweeps` DRIFT exit 1 with `SWEEP_REJECTION_INCOMPLETE` on R1 (`missing=flip`) and `SWEEP_CLAIM_FALSE` on W1 naming `chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md` |
| `sweeps-r5-20261016T011543Z-live.log` (`c58b309c…`) | before-state (no `verify-sweeps` mode; structural pass on the canonical record), live canonical run, seven negative controls, cross-round byte-stability, zero-network strace | r4 CLI has no `verify-sweeps` (usage, exit 2); r4 `verify` on the canonical record CLEAN exit 0 (the hole); landed canonical `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3`, `RESEARCH_GATE: CLEAN`, exit 0; all seven controls below; claims `17/17` CLEAN and chain `17/22` CLEAN with chain-broken `1/2` DRIFT (all six stdout pairs **byte-identical** to the round-4 gate after ts normalization: YES); archives 3/3 exit 1; `strace -f -e trace=network`: 992 trace lines, **0 network syscalls** |

Before → after in one line: under the round-4 gate the kept rejections passed
with only a non-empty `reason` (no flip-condition) and negative sweeps were
never adjudicated at all — both `sweeps-r5.md` and `sweeps-r5-broken.md` closed
`RESEARCH_GATE: CLEAN`, exit 0, structurally; the landed `verify-sweeps` mode
requires each kept rejection to carry reason **and** flip-condition and re-runs
each named local path/glob set, so the canonical record closes CLEAN
(`verified=1 exempt=1`) while the broken control drifts naming both cells, and
a record that names nowhere, names a false emptiness, escapes the root, or
cites an undeclared source id drifts too.

### Negative controls (recorded in the live receipt)

Each control is a single-delta copy of `sweeps-r5.md` (sha256 printed in the
receipt); every delta is one cell.

| Control | Delta | Result (exit) |
|---|---|---|
| `ctl-01-rej-flip-empty` | R1 `flip_condition` emptied | `SWEEP_REJECTION_INCOMPLETE id=R1 missing=flip`, `REJECTIONS_OK=2/3`, DRIFT (1) |
| `ctl-02-rej-reason-empty` | R2 `reason` emptied | `SWEEP_REJECTION_INCOMPLETE id=R2 missing=reason`, `REJECTIONS_OK=2/3`, DRIFT (1) |
| `ctl-03-sweep-false-hit` | W1 `where` → the planted hit file | `SWEEP_CLAIM_FALSE … hits=1 first=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md`, `VERIFIED_SWEEPS=0/2`, DRIFT (1) |
| `ctl-04-sweep-nonlocal` | W1 `where` → `https://kotobank.jp/` | exempt but counted (`verified=0 exempt=2 hit=0`), CLEAN (0) — a content sweep carries no probe the gate could re-run |
| `ctl-05-sweep-nowhere` | W1 `where` emptied | `SWEEP_LOCATION_ABSENT id=W1 no location named`, `invalid=1`, DRIFT (1) |
| `ctl-06-sweep-out-of-corpus` | W1 `where` → `../research/README.md` | `SWEEP_LOCATION_OUT_OF_CORPUS severity=crit … refused unopened`, `refused=1`, DRIFT (1) |
| `ctl-07-sweep-unresolved-id` | W1 `where` → `S9` (undeclared) | `SWEEP_LOCATION_UNRESOLVED … S9 not in ## Sources`, `refused=1`, DRIFT (1) |

### Re-run recipe

From the lane root, local only. Exit contract for every run: 0 CLEAN,
1 DRIFT, 2 setup/usage.

```bash
sha256sum tools/research-gate.sh
#   55adb92d0ba5ac958907fac6c4d5d6b0b50129703e866a5befbd9a32789f2ff2
bash tools/research-gate.sh verify-sweeps corpus/fixtures/sweeps-r5.md --root ..
#   expect: VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3; CLEAN (sweeps=2 verified=1 exempt=1
#   hit=0 refused=0 invalid=0 rejections=3 rejections-ok=3 …); exit 0
bash tools/research-gate.sh verify-sweeps corpus/fixtures/sweeps-r5-broken.md --root ..
#   expect: VERIFIED_SWEEPS=0/1 REJECTIONS_OK=0/1; DRIFT with FINDING SWEEP_REJECTION_INCOMPLETE
#   (id=R1 missing=flip) and FINDING SWEEP_CLAIM_FALSE naming the planted hit; exit 1
bash tools/research-gate.sh verify corpus/fixtures/sweeps-r5-broken.md --root ..
#   expect (pre-move hole): CLEAN, exit 0
bash tools/research-gate.sh --selftest
#   expect: RESEARCH_GATE_SELFTEST: PASS (54 cases), exit 0
# before-state gate for the hole pair (round-4 revision, from git):
git show 45f8f65:tools/research-gate.sh > /tmp/r5/r4-gate.sh   # sha256 6b83705b…
#   run it from a shadow dir whose corpus/ and research/ resolve to the lane and
#   fleet roots (a bare /tmp copy changes LANE_ROOT and misreports lane pointers)
# the fixture README's own gate-free check (see corpus/fixtures/sweeps-r5.README.md §Re-run)
grep -nE 'https?://' -- ../research/deep-research-2026-09-28/A-shokunin-tradition.md \
  ../research/deep-research-2026-09-28/B-multiagent-knowledge.md \
  ../research/deep-research-2026-09-28/C-rank-taxonomy.md ../research/README.md
#   expect: zero matches, exit 1
```

### Notes

- Receipts pin gate revision `55adb92d…`; a later gate edit supersedes this
  stamp — re-run the recipe above and re-cut.
- Scratch for this cut lived at `/tmp/chousa-r5-evidence/` (cut script,
  r4-gate snapshot, lane shadow, control copies, `TMPDIR`, strace log). `/tmp`
  writes succeeded; the `$HOME/.cache/chousa-tmp` fallback was not needed.
- Cut discipline: the receipts were first cut at stamp `20261016T011103Z`
  while the fixture author was still converging `sweeps-r5-hit.md` and the
  fixture README (a pre-convergence `command`-column record then read as
  `SWEEP_LOCATION_ABSENT`). That set was removed and re-cut at stamp
  `20261016T011543Z` against the settled bytes; the receipts pin the fixture
  shas listed above, and a later fixture edit supersedes them — re-run the
  recipe and re-cut. The fixture README (`e9178651…`) now carries its own
  Execution record whose verbatim runs agree with these receipts
  (canonical CLEAN, broken DRIFT with the same two findings, PASS 54).
- The `verify-sweeps` mode's honest boundaries are its header's
  (`tools/research-gate.sh:70-98`): a CLEAN sweep proves the named location set
  re-measured empty by glob, not that the sweep was the right one; non-local
  sweeps stay exempt-but-counted; a sweep whose named paths do not exist under
  the root is the verified case by construction, so an emptiness claim cannot
  be verified beyond its naming.
- Receipt identity for this round remains a lane-local log; no `task_…` value
  is invented and the round-1 receipt blocker stands (operator-side).

## Round-6 composition receipts — stamp 20261016T020330Z

Revision under test: `tools/research-gate.sh` sha256
`0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8`
(lane HEAD `1d1f56c`). Before-state gate: the round-5 revision
`55adb92d…` (lane HEAD; `verify-all` absent — it exits 2 with usage text).
Fixtures: `corpus/fixtures/full-r6.md` sha256 `878c2c50…`,
`corpus/fixtures/full-r6-broken.md` sha256 `0f7e498c…`,
`corpus/fixtures/full-r6-absent.md` sha256 `39cdb2d7…`,
`corpus/fixtures/full-r6.claims.jsonl` = `full-r6-broken.claims.jsonl`
sha256 `45eb6ac2…`; contract `corpus/fixtures/full-r6.README.md` sha256
`f56ef337…`.

| Receipt (sha256) | Shows | Key result |
|---|---|---|
| `compose-r6-20261016T020330Z-selftest.log` (`e3b94e1c…`) | full `--selftest`; case-line stability vs the round-5 selftest stdout | `RESEARCH_GATE_SELFTEST: PASS (64 cases)`, exit 0; the first 54 case lines are **byte-identical** to the round-5 receipt (`cmp` YES); new cases 55–64 = `all-pass`/`all-structure`/`all-meta`/`all-meta-missing` + the claims-JSONL-as-input case + two setup exits |
| `compose-r6-20261016T020330Z-full.log` (`c96ac4f5…`) | the four solo modes on `full-r6.md`, then composed `verify-all`, then the side-by-side tally comparison | composed `VERIFY_ALL sections=4 run=4 absent=0 drift-sections=0 findings=0 drift=0` + `RESEARCH_GATE: CLEAN`, exit 0; per-section composed tallies equal the solo summaries (`VERDICT_BEARING_CLAIMS=3/3`, `RESOLVED_HOPS=3/3`, `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=2/2`) |
| `compose-r6-20261016T020330Z-broken.log` (`83d7aef6…`) | the twin's diff, composed `verify-all`, the solo modes localizing the two defects, the round-5 before-state | composed `drift-sections=2` naming exactly `chain` (`RESOLVED_HOPS=2/3`, `CHAIN_ANCHOR_NOT_FOUND` hop=2) and `sweeps` (`REJECTIONS_OK=1/2`, `SWEEP_REJECTION_INCOMPLETE` id=R2 missing=flip), `structure`/`claims` green; DRIFT exit 1; round-5 `verify` on the twin CLEAN exit 0 (the hole) |
| `compose-r6-20261016T020330Z-json.log` (`1db37149…`) | manifest before-state (0 lines), the three appended `--json` lines verbatim, append-only prefix compares, JSON well-formedness, boundary refusals | lines 0 → 3; prefix run1==before / run2==after1 / run3==after2 all YES; each line a well-formed JSON `chousa-verify-all/v1` object with ts, record + gate sha256, per-section tallies, composed verdict; missing-dir and dir-as-path controls exit 2 |
| `compose-r6-20261016T020330Z-live.log` (`ac4d3f8e…`) | composed runs on all three fixtures, the omission probe, the `--claims` binding, cross-round no-harm, the r1 archive observable, setup controls, zero-network strace | full CLEAN (run=4), broken DRIFT (drift-sections=2), absent CLEAN (run=3 absent=1, `SECTION claims state=absent`); `--claims` binding runs all 4 sections CLEAN; r5-gate vs r6-gate stdout **byte-identical** on claims17/chain/chain-broken/sweeps/sweeps-broken/archive-A (frozen clock); `VERDICT_BEARING_EXPORTS=3/3`; `strace -f -e trace=network`: 4237 trace lines, **0 network syscalls** |

Before → after in one line: at the round-5 revision a record's full
verification state required running up to four modes by hand and eyeballing
four summaries, and `verify-all` did not exist (exit 2 with usage); the landed
mode composes ONE verdict over the applicable sections (DRIFT iff a run
section drifts; an absent section is reported, never drift by itself), and
`--json` appends the record's state (ts, record + gate sha256, per-section
tallies, composed verdict) to the lane manifest with `>>` — no rewrite path.

### The lane manifest

`corpus/evidence/verify-all-manifest.jsonl` sha256
`2ed28f9ffd772ab9b67690a16ae0127e0ac06b48ec0d1a14c83119c117810ea9` — three
lines, one per fixture run, appended by the cut itself (the first real
manifest lines in the lane):

| line | record | verdict | sections |
|---:|---|---|---|
| 1 | `full-r6.md` | CLEAN | run=4 absent=0 drift-sections=0 |
| 2 | `full-r6-broken.md` | DRIFT | run=4 absent=0 drift-sections=2 |
| 3 | `full-r6-absent.md` | CLEAN | run=3 absent=1 drift-sections=0 |

### Omission rule (the round's absent-section claim)

`full-r6-absent.md` carries no `## Sweeps`, no `## Negatives`, no `claims_file`
Meta row and no companion claims file. Composed: `SECTION claims state=absent`,
`SECTION sweeps state=run verdict=CLEAN … VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1`,
one CLEAN verdict exit 0 — an omission is reported, not drift. Measured limit
(fixture README, named r7 candidate): a record cannot compose CLEAN once the
sections the structure mode demands are gone, and `chain` absent is not
exercised as a CLEAN case.

### Re-run recipe

From the lane root, local only. Exit contract: 0 CLEAN, 1 DRIFT, 2 setup/usage.

```bash
sha256sum tools/research-gate.sh
#   0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8
bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.md --root ..
#   expect: SECTION x4 all state=run CLEAN; VERIFY_ALL sections=4 run=4 absent=0
#   drift-sections=0; CLEAN, exit 0
bash tools/research-gate.sh verify-all corpus/fixtures/full-r6-broken.md --root ..
#   expect: SECTION chain DRIFT + SECTION sweeps DRIFT (findings 1+1);
#   VERIFY_ALL sections=4 run=4 absent=0 drift-sections=2 findings=2; DRIFT, exit 1
bash tools/research-gate.sh verify-all corpus/fixtures/full-r6-absent.md --root ..
#   expect: SECTION claims state=absent; run=3 absent=1; CLEAN, exit 0
bash tools/research-gate.sh --selftest
#   expect: RESEARCH_GATE_SELFTEST: PASS (64 cases), exit 0
# manifest append (append-only; adds one line per run):
bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.md --root .. \
  --json corpus/evidence/verify-all-manifest.jsonl
```

### Notes

- Receipts pin gate revision `0c3d51ed…`; a later gate edit supersedes this
  stamp — re-run the recipe and re-cut.
- Scratch for this cut lived at `$HOME/.cache/chousa-r6-evidence/` (cut and
  assembler scripts, captures, `TMPDIR`, frozen r5-gate snapshot). `/tmp` was
  not required.
- Cut discipline: the fixture family converged during the wave (the records
  gained their `claims_file` Meta rows, the README kept being polished); the
  receipts were re-cut at stamp `20261016T020330Z` against the settled bytes
  (all fixture shas above re-checked identical before and after the cut), and
  a pre-settle rehearsal set was discarded. The earlier uncommitted
  `verify-all-manifest.jsonl` rehearsal lines were replaced by this cut's
  three lines.
- The composed run shells out to the same CLI paths (`bash "$SELF" <mode>`), so
  each section tally is that solo mode's tally by construction; the receipts
  also measure every solo mode separately for the reader to compare, and the
  live receipt holds a r5-gate-vs-r6-gate byte-identical comparison (frozen
  clock) across the six prior-mode/archive runs.
- Honest boundaries of the new mode: a section that cannot run (rc outside
  0/1 or an unparsable summary) is `VERIFY_ALL_SECTION_UNAVAILABLE severity=crit`
  and drifts the composition; a manifest line is appended with `>>` and never
  deduplicated, so a replayed line is information, not a rewrite — replay
  handling is not part of this round. How fine-grained the omission reporting
  should be is the named r7 candidate.
- Receipt identity for this round remains a lane-local log; no `task_…` value
  is invented and the round-1 receipt blocker stands (operator-side).## Round-7 reference-integrity receipts — stamp 20261016T030552Z

Revision under test: `tools/research-gate.sh` sha256
`3ba718bf9207eed70c66b8c849ac43b44c76890785e1576eeb5e795a604166b2` (lane HEAD
`4835426`; the cut script asserts the gate and fixture shas identical before
and after the whole battery). Before-state gate: the round-6 revision
`0c3d51ed…`, recoverable from git as `git show 4835426:tools/research-gate.sh`
→ `0c3d51ed1a131146ac33eebf24eefe5830ecaaf3e59a1b03e6c91cd8debfd5f8`.
Fixtures: `corpus/fixtures/integrity-r7.md` sha256
`4310ce86aa45f3d7d4b7d04c4ebf480a7b59748510ab0f132c5411dd8acd1b1b`,
`integrity-r7-broken.md`
`fd4e213f03faf9a76bbca3896b11fe6530878e727fefb974043ffb4a9f9a05b8`,
companions `integrity-r7.claims.jsonl` = `integrity-r7-broken.claims.jsonl`
`8e83b23d04e92961f7781e556d600b94a313e083c79d32a517fcb16ec17dabb3`; contract
`corpus/fixtures/integrity-r7.README.md`
`2ef59df319d78072a8fa15d2cca052ca0520c22f4083dcaa3f2343d3bdfc93a2`.

| Receipt (sha256) | Shows | Key result |
|---|---|---|
| `integrity-r7-20261016T030552Z-selftest.log` (`12309c03…`) | full `--selftest`; case-line stability vs the round-6 selftest stdout | `RESEARCH_GATE_SELFTEST: PASS (74 cases)`, exit 0; the first 64 case lines are **byte-identical** to the round-6 receipt (`cmp` YES); new cases 65-74 = `integrity-pass` / `-fail-dangling-claim` / `-fail-dangling-source` / `-fail-dangling-chain-claim` / `-fail-dangling-sweep` / `-exempt-counted` / `-fail-counting` + two setup exits + `all-dangling.md` |
| `integrity-r7-20261016T030552Z-fixture.log` (`ea0a1a16…`) | inventory, twin delta, independent gate-free checker, reconciliation, positive runs | positive `INTEGRITY refs=16 resolved=15 unresolved=0` CLEAN; composed `SECTION integrity state=run verdict=CLEAN … tally=INTEGRITY refs=16 resolved=15 unresolved=0` and `sections=5 run=5 absent=0 drift-sections=0`, exit 0; twin delta = 5 changed lines (18 diff lines); companion `cmp` identical; the independent checker re-derives all 16 refs and reconciles with the gate (diff EMPTY) |
| `integrity-r7-20261016T030552Z-broken.log` (`1b2979d8…`) | the two dangling refs, the hole, four single-delta controls | broken `INTEGRITY refs=16 resolved=13 unresolved=2` with exactly two `REF_UNRESOLVED` — `kind=source id=S9 section=chain row=4 cell=from` and `kind=claim id=C9 section=sweeps row=SW3 cell=claim_id`; composed `drift-sections=1 findings=2 drift=2` DRIFT while structure/claims/chain/sweeps stay CLEAN with the positive's tallies (3/3, 4/4, 2/3); all four r1-r6 modes still pass the twin; controls below |
| `integrity-r7-20261016T030552Z-live.log` (`91a84a6b…`) | before-state, cross-round no-harm, composition regression, archives, manifest, strace | round-6 gate on both fixtures CLEAN `sections=4 run=4` (the hole) and `verify-integrity` absent (usage, exit 2); nine solo-mode pairs (claims/chain/chain-broken/sweeps/sweeps-broken/structure/archives A-C) at r7 vs r6 gate are **byte-identical** after ts normalization with matching rc; `VERDICT_BEARING_EXPORTS=3/3`; manifest 3 → 5 lines, first 3 preserved byte-for-byte, both new lines parse and pin record+gate shas; `strace -f -e trace=network`: 8991 trace lines, **0 network syscalls** |

Before → after in one line: at the round-6 gate both fixtures compose CLEAN
with four sections — a sweep cell naming an undeclared claim id (`C9`) and a
hop `from` cell naming an undeclared source id (`S9`) were read by no mode —
and the landed `integrity` section (the fifth composed section for any record
with at least one other run section) extracts every cross-section reference
token and resolves it against the DECLARED rows (Sources ids; Claims and
Negatives ids; Sweeps ids), so the twin composes DRIFT naming exactly the
integrity section while the positive composes CLEAN `unresolved=0`, and exempt
classes (non-local namings; the tokens of an exempt-status row) stay
exempt-but-counted.

### Negative controls (recorded in the broken receipt)

Each control is a single-delta scratch copy of `integrity-r7.md` (declared
ephemeral, under `$HOME/.cache/chousa-r7-evidence/ctl/`).

| Control | Delta | Result (exit) |
|---|---|---|
| ctl-01 claims-sweep | Claims C1 `sweep` cell → `SW9` (undeclared sweep id) | `REF_UNRESOLVED … kind=sweep id=SW9 section=claims row=C1 cell=sweep`, `refs=17 resolved=15 unresolved=1`, DRIFT (1) |
| ctl-02 rejection-ref | Rejections R1 `ref` → `S9` (undeclared source id) | `REF_UNRESOLVED … kind=source id=S9 section=rejections row=R1 cell=ref`, `refs=17 resolved=15 unresolved=1`, DRIFT (1) |
| ctl-03 exempt-dangling | Negatives N2 `sweep` → `SW9`, row status `unresolved` | `REF kind=sweep id=SW9 … observed=exempt verdict=exempt status=unresolved`, `refs=16 resolved=15 unresolved=0`, CLEAN (0) |
| ctl-04 non-local | Negatives N1 `sweep` → `https://example.invalid/x.md` | `REF kind=location id=https://example.invalid/x.md … observed=exempt verdict=exempt reason=non-local`, `refs=16 resolved=14 unresolved=0`, CLEAN (0) |

### The lane manifest (append point 2)

`corpus/evidence/verify-all-manifest.jsonl` now has 5 lines (sha256
`9620946f8c2740d28cc908215d4ffd63cd3caabcef7e565cf7189cd799ba54f0`): the three
round-6 lines are byte-preserved (prefix compare YES) and this cut appended
two integrity-family lines using the gate's own `--json`:

| line | record | verdict | sections |
|---:|---|---|---|
| 4 | `integrity-r7.md` | CLEAN | run=5 absent=0 drift_sections=0; integrity `INTEGRITY refs=16 resolved=15 unresolved=0` |
| 5 | `integrity-r7-broken.md` | DRIFT | run=5 absent=0 drift_sections=1; integrity `INTEGRITY refs=16 resolved=13 unresolved=2` |

### Re-run recipe

From the lane root, local only. Exit contract: 0 CLEAN, 1 DRIFT, 2 setup/usage.

```bash
sha256sum tools/research-gate.sh
#   3ba718bf9207eed70c66b8c849ac43b44c76890785e1576eeb5e795a604166b2
bash tools/research-gate.sh verify-integrity corpus/fixtures/integrity-r7.md --root ..
#   expect: INTEGRITY refs=16 resolved=15 unresolved=0; CLEAN, exit 0
bash tools/research-gate.sh verify-integrity corpus/fixtures/integrity-r7-broken.md --root ..
#   expect: two REF_UNRESOLVED (S9 chain/from, C9 sweeps/claim_id); DRIFT, exit 1
bash tools/research-gate.sh verify-all corpus/fixtures/integrity-r7.md --root ..
#   expect: SECTION integrity tally=INTEGRITY refs=16 resolved=15 unresolved=0;
#   sections=5 run=5; CLEAN, exit 0
bash tools/research-gate.sh verify-all corpus/fixtures/integrity-r7-broken.md --root ..
#   expect: drift-sections=1 findings=2; DRIFT, exit 1
bash tools/research-gate.sh --selftest
#   expect: RESEARCH_GATE_SELFTEST: PASS (74 cases), exit 0
# before-state gate for the hole (round-6 revision, from git):
bash <(git show 4835426:tools/research-gate.sh) verify-all corpus/fixtures/integrity-r7-broken.md --root ..
#   expect (pre-move hole): CLEAN sections=4, the dangling refs pass, exit 0
```

### Notes

- Receipts pin gate revision `3ba718bf…`; a later gate edit supersedes this
  stamp — re-run the recipe above and re-cut.
- Scratch for this cut lived at `$HOME/.cache/chousa-r7-evidence/` (cut
  script, r6-gate snapshot, control copies, `TMPDIR`, strace log, and the
  receipts-writer independent checker `integcheck.py`); `/tmp` was not
  required.
- Cut discipline: the gate revision moved through at least twelve landed shas
  during the wave (first observed `e9ab5141…`, settled `3ba718bf…`) and the
  fixture pair was re-shaped mid-wave — its README records that an earlier
  twin put the source defect behind an exempt hop status, was measured as
  exempt at the first landed integrity revision, and was re-shaped to
  non-exempt cells so both dangling ids are verdict-bearing. These receipts
  were cut only against the settled set.
- One cosmetic fixture-side observation, not fixed here (not this seat's
  file): `corpus/fixtures/integrity-r7.README.md:240` carries a stray closing
  fence after the Re-run block's already-closed fence.
- The independent checker is
  `/home/vgpnk/.cache/chousa-r7-evidence/integcheck.py` (scratch, gate-free:
  re-derives declared ids, token extraction and dispositions from the record
  bytes); its REF lines reconcile with the gate's on both fixtures
  (diff EMPTY), and both agree with the fixture README's after-state block.
- Receipt identity for this round remains a lane-local log; no `task_…` value
  is invented and the round-1 receipt blocker stands (operator-side).