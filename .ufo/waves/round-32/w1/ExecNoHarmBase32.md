# ExecNoHarmBase32 — round-31 routed defect R3 + round-32 no-harm baseline

Seat: `ChousaR32A2.ExecNoHarmBase32`, WAVE 1 (pre-data controls). Lane
`/home/vgpnk/Projects/shokunin/chousa-shokunin`, HEAD `4111607c857bc29ff31883bc095ae00afb527e50`
(unchanged before and after this run). Gate `tools/research-gate.sh` SHA-256
`0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258` — equals the lane gate and the
claims.md base gate. Every log in `ExecNoHarmBase32/` carries that sha and that revision in its
first two header lines. No counters in `corpus/evidence/round32/` were run (control rule); no
candidate build was touched.

## What R3 asks

`corpus/lessons/round-31-verifier-spotcheck.md:214-217`: "**R3 (no-harm revision).**
`falsify/NoHarmAfter31.md` measured gate `c23d7537` (ee1024fd), not landed gate `0bc318b3`. No
committed selftest receipt names `0bc318b3`, so the 'PASS (228)' on the final gate in SCORECARD is
unreceipted. Re-run the battery on the landed gate and name that revision." This directory is that
receipt.

## Setup

- `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; git clone -q <lane> /fast/scratch/hyaku/chousa-r32/w1/ExecNoHarmBase32/lane`;
  `git -C lane checkout -q 4111607c…` → detached HEAD `4111607c…`, `git -C lane status --porcelain`
  → 0 lines (clean) after all runs. `sha256sum lane/tools/research-gate.sh` → `0bc318b3…`.
- Fixtures at that revision: `claims-r2.jsonl` `23d078cb…`, `chain-r3.md` `06115f2f…`,
  `chain-r3-broken.md` `b66222a1…` (sha256, from `lane/corpus/fixtures/`).
- Root convention: the fixtures' `source` values are fleet-root-relative
  (`research/deep-research-2026-09-28/…`), so their lane invocation is `--root ..` with the fleet
  root as parent. Required-subset runs were made **both** ways and agree: (a) `--root ..` in the
  clone after `cp -a` of the 28 K `research/deep-research-2026-09-28` tree to the clone's parent
  (canonical invocation shape; logs `claims-r2-dotdot.log` `ce6151e0…` rc 0 / 17/17,
  `chain-r3-dotdot.log` `c228a8ea…` rc 0 / 17/22, `chain-r3-broken-dotdot.log` `8d0aa45f…` rc 1 /
  1/2; `summary-dotdot.tsv` `1ac34439…`), and (b) `--root /home/vgpnk/Projects/shokunin`
  read-only (the whole battery table below; round-31's `ExecNoHarmBase.md` used the same
  convention). Tallies and summary lines are identical both ways. Runs with `--root .`, or with a *symlink* to the
  fleet `research/`, refuse all 17 claims (`FINDING CLAIM_SOURCE_OUT_OF_CORPUS …
  outside allowed roots`, `VERDICT_BEARING_CLAIMS=0/17`): a root-convention artifact (realpath
  escapes the root), not a gate change — recorded so later seats do not misread it.
- Timeouts: `timeout 1800` selftest, `timeout 900` every other run; no run came near its cap.
  `C1_TMP`/`C2_TMP`/`TMPDIR` pointed at the scratch dir for the counters.

## Battery on gate `0bc318b3` at `4111607c` (`summary.tsv`, one log per row)

| run | exit | wall | key output |
|---|---:|---:|---|
| `--selftest` | 0 | 31326 ms | `RESEARCH_GATE_SELFTEST: PASS (228 cases, 0 skipped)`; 228 `ok-case` lines, 0 `FAIL-case` |
| `verify-claims claims-r2.jsonl` | 0 | 244 ms | `VERDICT_BEARING_CLAIMS=17/17`; `RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 … drift=0)` |
| `verify-chain chain-r3.md` | 0 | 825 ms | `RESOLVED_HOPS=17/22`; `RESEARCH_GATE: CLEAN (hops=22 verified=17 exempt=5 … drift=0)` |
| `verify-chain chain-r3-broken.md` | 1 | 129 ms | `RESOLVED_HOPS=1/2`; `RESEARCH_GATE: DRIFT (hops=2 verified=1 anchor-missing=1 findings=1 drift=1)` |
| round-1 observable (SCORECARD `## Planned`, verbatim) | 0 | 79 ms | `VERDICT_BEARING_EXPORTS=3/3` |
| round-31 `c1-count.py --seed 32` / `--seed 33` | 0 / 0 | — | `LINE_BINDING_MATCH=120/120` both |
| round-31 `c2-count.py --seed 32` / `--seed 33` | 0 / 0 | — | `REVISION_BINDING_MATCH=120/120` both |

### Selftest receipt (the R3 gap)

- `selftest.log`: header names gate `0bc318b3…` and revision `4111607c…`; final line
  `RESEARCH_GATE_SELFTEST: PASS (228 cases, 0 skipped)`, exit 0.
- Case-line list `selftest.cases`: 228 lines, sha256
  `a88730646704c3567c51258c9ed892b715b441b224f003a239d086ca1e44d924`. Two independent selftest
  runs (28.6 s and 31.3 s) produced byte-identical case lines (`cmp` → identical). Later builds
  must keep every one of those lines byte-identical; this hash is the base list.

### Round-31 counters (`python3 corpus/evidence/round31/{c1,c2}-count.py --seed N --receipt …`)

| run | receipt | matched | predicate_holds | counter_sha256 |
|---|---|---:|---|---|
| c1 seed 32 | `r31-c1-s32.json` (`9600164c…`) | 120/120 | true | `c3aca35d…` |
| c1 seed 33 | `r31-c1-s33.json` (`338f51ff…`) | 120/120 | true | `c3aca35d…` |
| c2 seed 32 | `r31-c2-s32.json` (`7e3dc85f…`) | 120/120 | true | `1064fdb3…` |
| c2 seed 33 | `r31-c2-s33.json` (`10c87c2c…`) | 120/120 | true | `1064fdb3…` |

Each receipt records `gate_sha256=0bc318b3…` and its seed; stdout logs (`r31-c1-s32.log` etc.)
carry the gate sha and `lane_rev=4111607c…`. Both predicates' frozen `120/120` hold on the landed
gate and revision.

### Rest of the round-31 battery (same gate, `--root` = fleet root; all match `NoHarmAfter31.md`)

| run | exit | key output |
|---|---:|---|
| `verify-claims claims-r9.jsonl` | 0 | `VERDICT_BEARING_CLAIMS=10/10`; CLEAN |
| `verify-sweeps sweeps-r5.md` | 0 | `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3`; CLEAN |
| `verify-integrity integrity-r7.md` | 0 | `INTEGRITY refs=16 resolved=15 unresolved=0`; CLEAN |
| `verify-all integrity-r7.md --claims …` | 0 | `VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0`; CLEAN |
| `--drift gate-baseline-r12-…json` | 0 | `GATE_DRIFT: none` |
| `--drift gate-baseline-r8-…json` | 1 | `GATE_DRIFT: GATE record_sha256` (expected; round-31 finding 2) |

## Verdict

R3's receipt gap is closed: gate `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`
at lane revision `4111607c857bc29ff31883bc095ae00afb527e50` now has a committed-path receipt naming
both, with `--selftest` PASS (228 cases, 0 skipped) and the base case-line list
`a8873064…`. Every no-harm value matches claims.md §No harm and round-31's battery table; the only
non-matching exit is `drift-r8` = 1, which the round-31 baseline already recorded as expected. No
unexplained difference, so this base is usable for the comparators of wave 2.

## Limits and disclosures

- No `corpus/evidence/round32/*` counter was run (binding control rule) and no candidate patch was
  read or applied. No `--json` run was made (it appends), so manifest-append behaviour is left to
  C1's counter.
- `bc` is absent on the host; wall times use shell integer arithmetic, not `bc`.
- No tools installed or updated; no network used.
- Lane writes: this report plus the artifact copies in
  `.ufo/waves/round-32/w1/ExecNoHarmBase32/` only. `git status` in the lane lists only untracked
  wave artifacts (HEAD unchanged, no production file modified); the scratch clone stayed clean.
- Scratch lives in `/fast/scratch/hyaku/chousa-r32/w1/ExecNoHarmBase32/` (`out/`, `research/` copy,
  `tmp*`); no process trees left running (`pgrep` cwd check → 0 of mine). Gate + counter time
  totals under 2 minutes.
