# ExecNoHarmBase — no-harm baseline at frozen base d78d188 (round 31, WAVE 1 BUILD)

Seat: ChousaR31.ExecNoHarmBase. Scope: capture the no-harm baseline the falsify wave
compares the landed revision against. Pre-data control: no c1-count.py / c2-count.py run
(any candidate). No counters run at all. No network. No git/jj writes.

## Setup (sandbox clone)

- Lane source: /home/vgpnk/Projects/shokunin/chousa-shokunin (read-only; jj-colocated).
  Clone: `git clone --no-hardlinks <lane> /fast/scratch/hyaku/chousa-r31/w1/ExecNoHarmBase/lane`
  (GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset); `git checkout d78d18893849cecb710f3b691ec986e1321d39ee`
  → detached HEAD, status clean. Both exit 0.
- Gate at base: `sha256sum tools/research-gate.sh` =
  `ac1315ddaa12e79b68069d1a9866b9b1b55e3a43efef3ba0cb5ca5e665835765` — matches claims.md line 4.
- Root convention: all runs from clone cwd with `--root /home/vgpnk/Projects/shokunin`
  (fleet root, read-only). Fixture `source` paths are fleet-root-relative
  (`research/deep-research-2026-09-28/...`, claims-r2.README.md line 30); the gate resolves
  ROOT first, LANE_ROOT fallback (research-gate.sh lines 1154-1164), so the fleet root
  reproduces the lane's `--root ..` convention. Fleet tree only read.
- No tool installs/updates (timeout, coreutils, python3, git already present).

## Battery results (runs/ dir in this folder; summary.tsv has exit+wall per run)

| run | command | exit | wall s | key output |
|---|---|---|---|---|
| selftest | `timeout 1800 bash tools/research-gate.sh --selftest` | 0 | 26.680 | `RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)` |
| claims-r2 | `timeout 600 bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root $FLEET` | 0 | 0.250 | `VERDICT_BEARING_CLAIMS=17/17`; `RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)` |
| claims-r9 | same, `claims-r9.jsonl` | 0 | 0.151 | `VERDICT_BEARING_CLAIMS=10/10`; CLEAN (supported=7 contradicted=2 unsupported=1) |
| chain-r3 | `timeout 600 bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root $FLEET` | 0 | 0.849 | `RESOLVED_HOPS=17/22`; CLEAN (verified=17 exempt=5) |
| chain-r3-broken | same, `chain-r3-broken.md` | 1 | 0.139 | `RESOLVED_HOPS=1/2`; `RESEARCH_GATE: DRIFT (hops=2 verified=1 exempt=0 anchor-missing=1 … findings=1 drift=1)` |
| sweeps-r5 | `timeout 600 bash tools/research-gate.sh verify-sweeps corpus/fixtures/sweeps-r5.md --root $FLEET` | 0 | 0.160 | `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3`; CLEAN (sweeps=2 verified=1 exempt=1 hit=0) |
| integrity-r7 | `timeout 600 bash tools/research-gate.sh verify-integrity corpus/fixtures/integrity-r7.md --root $FLEET` | 0 | 0.631 | `INTEGRITY refs=16 resolved=15 unresolved=0`; CLEAN (exempt=1 findings=0 drift=0) |
| all-r7 | `timeout 600 bash tools/research-gate.sh verify-all corpus/fixtures/integrity-r7.md --claims corpus/fixtures/integrity-r7.claims.jsonl --root $FLEET` | 0 | 1.453 | `VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0`; `RESEARCH_GATE: CLEAN`; section tallies: claims 3/3, chain 4/4, sweeps 2/3 + rejections 2/2 |
| drift-r12 | `timeout 600 bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r12-20261019T115519Z.json` | 0 | 0.691 | `GATE_DRIFT: none` |
| drift-r8 | `timeout 600 bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r8-20261016T033757Z.json` | 1 | 0.724 | `GATE_DRIFT: GATE record_sha256` |
| observable | `timeout 600 python3 observable.py` (replica of SCORECARD.md lines 28-30) | 0 | 0.076 | `VERDICT_BEARING_EXPORTS=3/3`; each row rc=1 with exactly one `RESEARCH_GATE: DRIFT (…` line |

All commands ran under `timeout` (1800 s selftest, 600 s others); all finished far inside.
No process trees left; battery total wall ≈ 32 s.

## Evidence

- stdout/stderr per run, plus summary.tsv, copied verbatim to
  `.ufo/waves/round-31/build/ExecNoHarmBase/runs/` (this dir).
- Selftest printout: 217 case lines, final line `RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)`.
- Headers confirm base gate: `research-gate v2 — ts=2026-10-23T04:26:32Z — mode=claims …` / `mode=verify-all … root=/home/vgpnk/Projects/shokunin`.
- Observable replica: SCORECARD.md lines 28-30 run `verify ../research/... --root ..` from lane
  cwd; sandbox clone's parent is scratch, so the replica uses the absolute fleet path for the
  same record bytes; predicate unchanged (`rc==1` and exactly one `RESEARCH_GATE: DRIFT (`
  line per row).

## Findings vs frozen claims text

1. claims.md (line 122) predicts selftest "PASS (154 cases at base)"; measured at the pinned
   base sha: 215 cases, 0 skipped. Discrepancy recorded, not resolved ([INFERENCE] the
   selftest case list grew after the claims text's count was written).
2. Committed baseline `gate-baseline-r8-20261016T033757Z.json` currently drifts
   (`GATE_DRIFT: GATE record_sha256`, exit 1); `gate-baseline-r12-…` passes
   (`GATE_DRIFT: none`). The falsify wave should expect r8 drift runs to exit 1 under current
   gate rules.
3. All other baseline values match the claims.md "No harm" expectations
   (17/17 claims, 17/22 hops, 3/3 exports; broken fixture drifts).

## Limits

- No counters (C1/C2) executed — per wave rule.
- Drift/pin runs exercise the gate's internal hermetic canonical invocation; no lane files
  written (no `--json` passed).
- Nothing written to the fleet repo, lane production files, or git/jj state; only this
  report and the runs/ artifacts in my own build dir.
