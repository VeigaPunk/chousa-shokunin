# ExecNoHarmBase33 — round-33 W1 no-harm baseline + routed defect D3 (battery revision header)

Seat `ChousaR33.ExecNoHarmBase33`, WAVE 1 (pre-data controls). Lane
`/home/vgpnk/Projects/shokunin/chousa-shokunin`. Lane `master` was `3b528b9a…` when this seat
started and `e3e24ec86449e50b089845fef563b7e15c927b40` (round-33 design v2) when the retained run
executed; the gate did not change: `tools/research-gate.sh` SHA-256
`f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` throughout
(`git log --name-only e3e24ec` touches only `corpus/evidence/round33/claims.md`,
`corpus/evidence/round33/c1-count-v2.py` and `L1-design-v2/` receipts). The retained transcript's
header records both the lane revision and the gate hash, so the measurement is bound by hash, not by
the moving branch name. No candidate gate was built or scored; the round-33 counter
(`corpus/evidence/round33/c1-count.py`, still `ab6b2ae2…`) was never run — control rule observed.

## Deliverable

`.ufo/waves/round-33/w1/ExecNoHarmBase33/battery.sh` (mode 0755, 10760 bytes, SHA-256
`f24c56cc9d7db3f502d22d56feda2790bbad6bbff31d2a615a23b73f57e0cf37`), invoked as
`battery.sh GATE OUTDIR`. Its first output is the D3 header:

```
# round-33 W1 no-harm battery (D3 revision-bound header)
lane=/home/vgpnk/Projects/shokunin/chousa-shokunin
lane_revision=e3e24ec86449e50b089845fef563b7e15c927b40
gate=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
gate_sha256=f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0
gate_tree_revision=e3e24ec86449e50b089845fef563b7e15c927b40
counter=…/corpus/evidence/round31/c1-count-v3.py sha256=0efbd172…
counter=…/corpus/evidence/round31/c2-count-v3.py sha256=654183e1…
counter=…/corpus/evidence/round32/c2-count-v2.py sha256=8ec1a1ed…
fixture=…/claims-r2.jsonl sha256=23d078cb…
fixture=…/chain-r3.md sha256=06115f2f…
fixture=…/chain-r3-broken.md sha256=b66222a1…
battery_script=…/battery.sh sha256=f24c56cc…
utc=2026-10-23T08:36:30Z
hostname=plazir27
scratch=/fast/scratch/hyaku/chousa-r33/w1/ExecNoHarmBase33
seeds=r31-c1:3601,3602 r31-c2:3611,3612 r32-c2:3621,3622
```

Every run is wrapped in `timeout -k 5` (1800 s selftest, 900 s otherwise), writes its own log in
OUTDIR, and prints `exit`/`want`, wall ms, log path + sha256, and the run's key lines. The script
asserts the expected value of every row and exits 0 only if all match (`ROWS=12`,
`BATTERY_RESULT=PASS`). Counters are asserted through their receipts (`predicate_holds` is a receipt
field, not stdout): `matched=total=132`, empty `misses` (and empty `record_fails` where present),
`gate_timed_out=false`, and `gate_sha256` / `counter_sha256` equal to the header values.

Base run (one retained invocation):

```
bash .ufo/waves/round-33/w1/ExecNoHarmBase33/battery.sh \
  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh \
  /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ExecNoHarmBase33 \
  > .ufo/waves/round-33/w1/ExecNoHarmBase33/battery-base.out 2>&1
exit 0, BATTERY_RESULT=PASS, ROWS=12
```

Transcript `battery-base.out`, 12117 bytes, SHA-256
`40bbb3c6a111c3422f9773ebb640e82a03c3503650d59ea8ab5bdb4bfc119c56`.

## Runs on the base gate (transcript rows)

| run | cwd / command | exit (want) | wall ms | key output | log sha256 |
|---|---|---:|---:|---|---|
| selftest | lane; `bash tools/research-gate.sh --selftest` | 0 (0) | 28921 | `RESEARCH_GATE_SELFTEST: PASS (241 cases, 0 skipped)`; 0 `FAIL-case` | `202702b4…` |
| claims-lane-root | lane; `verify-claims corpus/fixtures/claims-r2.jsonl --root .` | 1 (1) | 154 | `VERDICT_BEARING_CLAIMS=0/17`; `DRIFT (… refused=17 … findings=17 …)` | `1983f400…` |
| claims-fleet-root | lane; `verify-claims corpus/fixtures/claims-r2.jsonl --root /home/vgpnk/Projects/shokunin` | 0 (0) | 246 | `VERDICT_BEARING_CLAIMS=17/17`; `CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 … drift=0)` | `73264301…` |
| chain-r3 | lane; `verify-chain corpus/fixtures/chain-r3.md --root <fleet>` | 0 (0) | 921 | `RESOLVED_HOPS=17/22`; `CLEAN (hops=22 verified=17 exempt=5 …)` | `e18b71ee…` |
| chain-r3-broken | lane; `verify-chain corpus/fixtures/chain-r3-broken.md --root <fleet>` | 1 (1) | 126 | `RESOLVED_HOPS=1/2`; `DRIFT (hops=2 verified=1 exempt=0 anchor-missing=1 … findings=1 drift=1)` | `159d56aa…` |
| observable | lane; `python3 -c` block extracted from `SCORECARD.md` `## Planned` | 0 (0) | 81 | `VERDICT_BEARING_EXPORTS=3/3` | `2ae02592…` |
| r31-c1-v3 a/b | lane; `c1-count-v3.py --gate <gate> --seed 3601/3602 --receipt …` | 0/0 (0) | 2394/2126 | `LINE_BINDING_MATCH=132/132`; receipt `predicate_holds=True matched=132/132` | `2406fc73…` (both) |
| r31-c2-v3 a/b | lane; `c2-count-v3.py --seed 3611/3612 --receipt …` | 0/0 (0) | 1560/1586 | `REVISION_BINDING_MATCH=132/132`; receipt ok | `d2c70fea…` (both) |
| r32-c2-v2 a/b | lane; `c2-count-v2.py --seed 3621/3622 --receipt …` | 0/0 (0) | 4894/5109 | `EXEMPT_AUDIT_MATCH=132/132`; `RECORD_CHECKS=ok`; receipt ok | `91ac37bc…` (both) |

`<fleet>` = `/home/vgpnk/Projects/shokunin`. The observable is extracted at run time by awk from the
first `## Planned` bash block, not copied, so the candidate's own `SCORECARD.md` drives it.

### Selftest receipt

`selftest.cases` holds the 241 `ok-case` lines (0 `FAIL-case`), SHA-256
`7ee6b24c03eaa1e9cbdc9da30241a8792d1c3b47645dd300b7cf974b3cf43daa`. That is the same full-list
hash round 32 recorded for its 241-case selftest (`.ufo/waves/round-32/w2/NoHarmAfter32.md:16`), so
the base gate's case lines are byte-identical to the landed round-32 list.

### Counter receipts (all in this directory)

`r31-c1-v3-a.json` `7068a8df…`, `r31-c1-v3-b.json` `26374e2c…`, `r31-c2-v3-a.json` `4c878e15…`,
`r31-c2-v3-b.json` `22737e57…`, `r32-c2-v2-a.json` `a5b40a39…`, `r32-c2-v2-b.json` `cced28f7…`.
Every receipt carries `"gate_sha256": "f4731885…"`, the receipt's own `counter_sha256` equal to the
header counter hash, `seed` equal to the row seed, and `"predicate_holds": true`. The counters
report `gate_rc=1` in the receipt; that is expected, not a failure: their fixtures include records
whose truth is `mislocated`/`stale`, so the gate drifts by contract. The battery asserts the
counter's own exit (0) and every receipt field above, not `gate_rc`.

## Comparison with `.ufo/waves/round-32/measure/final/battery.out`

Comparator SHA-256 `f9ca8ae9180569e1a6d2aa5045c1647a0f2698b3bf3fb0f45fd6ef92fb694be8` (16 lines).
`compare-round32.txt` (`f80a7f95…`) tests each comparator line against the transcript, normalising
leading indentation: 10 exact-line matches, 2 substring matches, 4 absent.

- Exact-line MATCH: the claims CLEAN line, `RESOLVED_HOPS=17/22` + chain CLEAN, `RESOLVED_HOPS=1/2`
  + broken-chain DRIFT (including `exempt=0`), `VERDICT_BEARING_EXPORTS=3/3`,
  `EXEMPT_AUDIT_MATCH=132/132` (twice), `LINE_BINDING_MATCH=132/132`, `REVISION_BINDING_MATCH=132/132`.
- Substring MATCH: `RECORD_CHECKS=ok` (twice; the transcript prints it inside its `CHECK` lines).
- Absent, deliberately not rerun: `APPEND_SERIALIZED=24/24` (twice; that is round-32's C1 counter,
  not among the counters this assignment names, and it measures `verify-all --json` append
  serialization, a surface C1's field reader does not touch) and the round-31 v1 120/120 counters
  (their v3 successors are run here; v3 is v2 plus 12 non-string-`line` claims,
  `c1-count-v3.py:11-13`, so the 132-total runs are strictly stronger).

D3 context: `battery.out` itself names no gate and no revision — that is the defect. The receipts in
the same `final/` directory all carry `gate_sha256=f4731885…` (`c1-s32101.json`, `c2-s32111.json`,
`r31-c1-count-v3-s3210.json`, `r31-c2-count-v3-s3210.json`), so [INFERENCE] the comparator's values
were measured on the same base gate this battery measured; the value comparison is on equal footing,
but only the file's own header would have proved it. The retained transcript now proves it for this
run.

## Claims `--root .` (assigned invocation) versus the comparable form

Run from the lane root, `verify-claims corpus/fixtures/claims-r2.jsonl --root .` exits 1 with
`refused=17` and 17 `CLAIM_SOURCE_OUT_OF_CORPUS` findings: the fixture `source` values are
fleet-root-relative (`research/deep-research-2026-09-28/…`), so under the lane root they resolve to
`./research/…` and fall outside the allowed root. Round-32 recorded the identical root-convention
artifact (`.ufo/waves/round-32/w1/ExecNoHarmBase32.md:34-37`: "Runs with `--root .` … refuse all 17
claims … a root-convention artifact (realpath escapes the root), not a gate change"). The battery
therefore runs the assigned form as a base fingerprint (exit 1, `0/17`) and the round-32-comparable
form (`--root <fleet>`) as the no-harm row (`17/17`, CLEAN). A candidate that changes either row is
surfaced by a row mismatch.

## Verdict

- **D3 repaired.** Every battery transcript now opens with lane revision, gate path + SHA-256, each
  counter path + SHA-256, fixture hashes, the battery-script hash, UTC and hostname; counter receipts
  bind `gate_sha256` and `counter_sha256`, and the script fails if they do not match. Future battery
  outputs (base and candidate) are self-binding.
- **No-harm baseline established on base gate `f4731885…`.** All 12 rows matched their expected
  values (`BATTERY_RESULT=PASS`, exit 0): selftest PASS (241, 0 skipped, case list `7ee6b24c…`),
  claims 17/17 CLEAN, chain 17/22 CLEAN, broken chain 1/2 DRIFT, observable 3/3, and the three frozen
  counters at 132/132 on two seeds each with `predicate_holds=true`. Every line of the round-32
  comparator that this assignment covers matches.
- No candidate was scored; the round-33 counter was not run.

## How L1 reruns on the candidate

```
LANE=<candidate checkout> FLEET=/home/vgpnk/Projects/shokunin \
SCRATCH=/fast/scratch/hyaku/chousa-r33/<seat> \
bash <candidate checkout>/.ufo/waves/round-33/w1/ExecNoHarmBase33/battery.sh \
     <candidate checkout>/tools/research-gate.sh <outdir> > <outdir>/battery-candidate.out 2>&1
```

Defaults (`LANE`, `FLEET`, `SCRATCH` under `/fast/scratch/hyaku/chousa-r33/w1/ExecNoHarmBase33`) are
correct for an in-place lane run. For a scratch clone, set `LANE` to that clone so counters,
fixtures and `SCORECARD.md` come from the candidate tree; the header prints the resolved paths and
hashes, so the binding is visible either way. The candidate gate hash will differ by design; all
other header lines and all 12 rows must match (`BATTERY_RESULT=PASS`).

## Limits and risks

- Three battery invocations were made. Invocation 1 exited 1 on my own wrong assertion (I expected
  `predicate_holds=true` on counter stdout; it is a receipt field); I fixed the script to assert
  receipts. Invocation 2 passed but the transcript named an interim script hash (`8f5668ff…`), and a
  comment-only clarification then changed the script; invocation 3 (retained) passes with the final
  hash `f24c56cc…`. The two superseded transcripts were overwritten, not retained; no value changed
  between them.
- Selftest wall time varied with shared-host load (28.9 s in the retained run, 36.2 s and 235.2 s in
  earlier ones) while the 241 case lines and their hash were identical each time.
- The comparator is unbound (D3); the comparison above is value-level plus receipt-hash inference,
  not a re-measurement of round-32's transcript.
- `APPEND_SERIALIZED` (round-32 C1 v2) and round-31 v1's 120-total counters are not in this battery
  (assignment scope); no harm criterion for those surfaces is claimed here.
- Process hygiene (D5): no process was signalled by name or pattern; no background job was left
  running (the one backgrounded battery job completed before this report). Nothing was killed.
- Writes: only this directory, `battery.sh`, its logs/receipts/`compare-round32.txt`, and this
  report. `git status --porcelain` shows 6 untracked wave paths (this wave's `w1/`, `measure/`,
  `controls/L1-v2-rescore/`, spec/dispatch files — not lane production files, and not all mine);
  no lane production file, Git/jj state or fleet file was modified. Scratch use: 24 K under
  `/fast/scratch/hyaku/chousa-r33/w1/ExecNoHarmBase33`; this directory 124 K; no installs were made.
- The lane-root claims row is an asserted base fingerprint (root-convention artifact), not a
  correctness bar; see the run table for both root forms.
