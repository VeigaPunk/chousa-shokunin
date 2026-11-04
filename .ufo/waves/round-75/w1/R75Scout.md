# R75Scout — forger-class coverage reconnaissance for the r75 loader matrix

Seat: author-lane scout, round 75 wave 1. No admission/promotion authority.
Frozen revision observed: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD` =
`43a7a0db52c8aabdf32735f58e09610e05200e79` (matches the task's frozen revision).
Skill `/skill:godspeed` read first with `claims.md`. Leaf seat: no subagents, no
network, no production edits, no lane/fleet git mutation, no commits/pushes.

## Axis naming

1. **Coverage of the forger space** — which forger classes does the frozen r75
   `matrix-battery.py` actually discriminate, and which survive it?
2. **Detection channel availability** — the r62 battery's twelve F-classes each
   rest on a channel the *child* can observe (cwd, env, argv, `/proc`, stdin,
   stdout, rlimit). Does the r75 matrix close those channels or leave them open?
3. **Child-run bounding** — QUALITY 120 requires the ordering seed to be one the
   candidate cannot read, and requires each child run to be bounded.
4. **Provenance of the verdict** — the r74 critic's F4 (provenance blindness) and
   the r74 fix (digest receipt) still hold; is the digest actually checkable?

## Baseline reproduction (frozen bytes, unmodified)

| command (cwd = lane root) | exit | key line |
|---|---|---|
| `python3 -B corpus/evidence/round75/matrix-battery.py --matrix corpus/evidence/round75/loader-matrix-v2.py --work $S/work/final-batt --runs 2` | 0 | `BATTERY=PASS forgers_rejected=5/5 positive=2/2` |
| `python3 -B corpus/evidence/round75/matrix-battery.py --matrix corpus/evidence/round74/loader-matrix.py --work … --runs 2` | — | not re-run by this seat; committed receipt `controls/before-battery-r74-matrix.txt` records `BATTERY=FAIL forgers_rejected=2/5 positive=2/2`, exit 1 |
| `python3 -B corpus/evidence/round75/loader-matrix-v2.py --counter corpus/evidence/round73/c2-count.py --work …` | 1 | `LOADER_MATRIX=3/12 MATRIX=FAIL` (matches committed `controls/negative-r73-counter-on-v2.txt`) |

Frozen digests recomputed and matched the values printed in `claims.md`:
`loader-matrix-v2.py` = `95bdd49363e47531…`, `matrix-battery.py` =
`c35e937b4b7c1b91…`, `round74/loader-matrix.py` = `979638251845071c…`,
`round74/correction-count.py` = `9334721a5e7a4080…`, `round75/ref-counter.py` =
`909987ce9f762398…`. The frozen battery file was **not** edited; the extended
battery used for the gap evidence is a *copy* under the seat's scratch
(`logs/matrix-battery-extended.py`, sha256 `e33bae6babae28ee…`).

---

## Forger-class table

`matrix-battery.py` covers a class only when a frozen subject of that class is
scored REJECTED. "Receipt" is the exact line from
`corpus/evidence/round75/controls/after-battery-v2-matrix.txt` (frozen) or from
this seat's own re-run (`frozen-battery-v2-rerun.txt`).

| # | Forger class | Concrete detector / behaviour | Covered by `matrix-battery.py`? | Receipt line (frozen) |
|---|---|---|---|---|
| F1 | **constant-pass** | prints all-PASS, reads nothing | **yes** | `SUBJECT FORGER constant-pass sha256=0dbd573c87eb6d28 REJECTED` |
| F2 | **constant-fail** | always exits 1 with `C2-6` failing | **yes** | `SUBJECT FORGER constant-fail sha256=d515585003abebf0 REJECTED` |
| F3 | **invocation-order oracle** (r74 bytes unchanged) | counts its own invocations, replays the scripted answers | **yes** (5/12, 2/12) | `SUBJECT FORGER order-oracle sha256=180d1a3d92be9e13 REJECTED` |
| F4 | **diff-only oracle** | reads only `git diff --numstat` / `--name-only`, never a protected file | **yes** (9/12 both runs) | `SUBJECT FORGER diff-only sha256=6691c74c88efdb88 REJECTED` |
| F5 | **naive presence-grep** | opens protected files but greps for presence, not anchored count / last-section scope | **yes** (9/12 both runs) | `SUBJECT FORGER naive-grep sha256=e5fc4104d56c8162 REJECTED` |
| F6 | **label oracle** — commit-subject oracle | `git log -1 --format=%s <rev>` names the case outright (the matrix commits each case with `-qm <case name>`); replays the per-case expected verdict | **NO** | gap: frozen battery has no such subject; this seat's probe reaches `LOADER_MATRIX=12/12 MATRIX=PASS`, exit 0 |
| F7 | **harness-source oracle** | detects the invoking matrix through `/proc/<ppid>/cmdline`, imports it, and reads its own `CASES` table (the expected verdict per case); uses **no** commit metadata | **NO** | gap: probe reaches `LOADER_MATRIX=12/12 MATRIX=PASS`, exit 0 |
| F8 | **memorized-fixture oracle** | reads the protected content at `rev` (a legitimate public-path read), hashes the observed state, and looks it up in a memorized table of the twelve known fixture states | **NO** | gap: probe reaches `LOADER_MATRIX=12/12 MATRIX=PASS`, exit 0 |
| F9 | **seed-leak order oracle** | reads the matrix's own `SEED=<n>` line from `/proc/<ppid>/fd/1` (when matrix stdout is a regular file, i.e. the mode every lane receipt is produced in), recomputes the shuffle, and replays the r74 order-oracle script | **NO** | gap: probe reaches `LOADER_MATRIX=12/12 MATRIX=PASS`, exit 0 when matrix stdout is a file; under a **pipe** stdout the same read **blocks** (see F11) |
| F10 | **hang / unbounded child** | the candidate never exits | **NO** (matrix has no child timeout) | gap: `timeout 45 python3 -B corpus/evidence/round75/loader-matrix-v2.py --counter <hang-child> --work …` → exit **124** (killed by the outer `timeout`), i.e. the matrix itself never bounded the child. `grep -nE "timeout|RLIMIT|setrlimit" corpus/evidence/round75/loader-matrix-v2.py` → no match |
| F11 | **blocking-parent-fd read** | the candidate opens `/proc/<ppid>/fd/1` for reading while the parent's stdout is a pipe and blocks forever | **NO** | gap: matrix does not bound the child, so a candidate that blocks on the parent's stdout stalls the whole matrix (observed: `subprocess.run(..., capture_output=True)` on the matrix timed out after 50 s, outer `TimeoutExpired`) |
| F12 | **harness-source detection, no content read** | a candidate that only needs to *detect* the harness to know the expected table exists at a known path — the r62 F-class family transplanted to a matrix | **NO** | gap: the r62 battery's twelve F-classes exist only for the r61 *counter* battery (`corpus/evidence/round62/c1v2-battery.py`); **no** r74/r75 instrument runs a structural sweep (`grep -rn "sniff-sweep\|sniff_sweep" corpus/evidence/round74/ corpus/evidence/round75/` → no match) |

**F6–F9 are the load-bearing gaps.** Each reaches 12/12 — full marks, exit 0 —
against the frozen `loader-matrix-v2.py`, deterministically across independent
seeds, and each is scored **ACCEPTED** (not rejected) by the frozen battery's
own acceptance rule when added as a subject.

### Gap evidence (this seat's re-runs; the frozen battery file was not edited)

Extended battery = verbatim copy of `corpus/evidence/round75/matrix-battery.py`
with three subjects appended to `FORGERS` (scratch copy
`logs/matrix-battery-extended.py`), run against the frozen v2 matrix:

```
SUBJECT FORGER constant-pass sha256=0dbd573c87eb6d28 REJECTED
SUBJECT FORGER constant-fail sha256=d515585003abebf0 REJECTED
SUBJECT FORGER order-oracle sha256=180d1a3d92be9e13 REJECTED
SUBJECT FORGER diff-only sha256=6691c74c88efdb88 REJECTED
SUBJECT FORGER naive-grep sha256=e5fc4104d56c8162 REJECTED
SUBJECT FORGER NEW-label-oracle sha256=250d22b41dafc0ac ACCEPTED
SUBJECT FORGER NEW-pure-harness-detection-oracle sha256=d5017f6dc30a4a95 ACCEPTED
SUBJECT FORGER NEW-memorized-fixture-oracle sha256=4f06911a3f408152 ACCEPTED
forgers_rejected=5/8 positive=2/2
BATTERY=FAIL forgers_rejected=5/8 positive=2/2
```

(The frozen battery's own predicate is reproduced verbatim in substance at
`probes/battery-rule-sim.py`; it yields the same `forgers_rejected=5/8`.)

Per-class matrix evidence, two independent runs each (`class-matrix-evidence.txt`):

```
label-oracle                    run1 matrix_exit=0 LOADER_MATRIX=12/12 MATRIX=PASS
                                run2 matrix_exit=0 LOADER_MATRIX=12/12 MATRIX=PASS
pure-harness-detection-oracle   run1 matrix_exit=0 LOADER_MATRIX=12/12 MATRIX=PASS
                                run2 matrix_exit=0 LOADER_MATRIX=12/12 MATRIX=PASS
memorized-fixture-oracle        run1 matrix_exit=0 LOADER_MATRIX=12/12 MATRIX=PASS
                                run2 matrix_exit=0 LOADER_MATRIX=12/12 MATRIX=PASS
seed-leak-order-oracle          run1 matrix_exit=0 LOADER_MATRIX=12/12 MATRIX=PASS   (matrix stdout = regular file)
                                run2 matrix_exit=0 LOADER_MATRIX=12/12 MATRIX=PASS   (matrix stdout = regular file)
--- contrast: the five frozen forgers ---
forge-constant-pass matrix_exit=1 LOADER_MATRIX=4/12 MATRIX=FAIL
forge-constant-fail matrix_exit=1 LOADER_MATRIX=4/12 MATRIX=FAIL
forge-order-oracle matrix_exit=1 LOADER_MATRIX=7/12 MATRIX=FAIL
forge-diff-only    matrix_exit=1 LOADER_MATRIX=9/12 MATRIX=FAIL
forge-naive-grep   matrix_exit=1 LOADER_MATRIX=9/12 MATRIX=FAIL
```

### Why the five frozen forgers miss F6–F9

- The frozen subjects all read **the fixture repository** (or nothing). F6–F9
  read the **harness** — the matrix program, its stdout, or a memorized answer
  key — which the frozen battery never varies. The matrix is a *black box* to
  the five frozen forger classes by construction.
- The r74 order oracle is killed **only** by the v2 shuffle
  (`random.Random(seed).shuffle(order)`, `loader-matrix-v2.py:107-109`). F9
  defeats that same shuffle by reading the seed the matrix itself prints
  (`loader-matrix-v2.py:106`, `print(f"SEED={seed}")`).
- QUALITY 120 requires the seed to be one *"the candidate cannot read"*. Under
  the receipt-production mode (matrix stdout redirected to a file — how every
  lane receipt, including this lane's own `controls/*.txt`, was produced) the
  child **can** read it: measured `INVOCATION=0 VISIBLE_BYTES=106
  HAS_SEED=True CASE_LINES_SEEN=0` (`logs/parent-stdout-dump.txt`) — the seed
  and the `COUNTER_SHA256=` line are already flushed and visible to the *first*
  child, and by invocation 11 the child sees all 11 prior `CASE … expected_rc=
  … expected_failed=…` lines. That is the matrix's own expected-answer
  table, verbatim, delivered to the candidate.
- Measured directly: the recovered shuffle order equals the actual case order
  in the same run — matrix `SEED=1744755338301644282`, actual order
  `dup-card-heading delete-0 receipt-change delete-1 append-0 append-2
  replace-equal append-1 dup-log-heading delete-2 unchanged
  dup-lesson-heading`, probe verdict `LOADER_MATRIX=12/12 MATRIX=PASS`.

### Detection-channel availability to the candidate (r62 F-family, transplanted)

Measured from inside the child, under the frozen v2 matrix
(`logs/f-channels.txt`, `logs/child-channels-under-matrix.txt`):

| r62 class | channel | available to the r75 candidate? |
|---|---|---|
| F01 | cwd name | yes — `cwd=/home/vgpnk/Projects/shokunin/chousa-shokunin`, `F01_cwd_name_available='chousa-shokunin'` |
| F02 | env keys | yes — full environment inherited, `env_len=274` |
| F04 | argv names | yes — `['…', '--lane', 'loader-matrix-v2-…', '--base', '…', '--rev', '…']` |
| F06 | parent cmdline | yes — `parent_cmdline='python3 -B corpus/evidence/round75/loader-matrix-v2.py --counter … --work …'` |
| F07 | LANG / LC_ALL | yes — `LANG='en_US.UTF-8'` |
| F08 | RLIMIT_FSIZE | yes — `(-1, -1)`, i.e. unlimited (no limit is set) |
| F09 | stdin type | yes — `stdin_kind=chr`, and it is `/dev/null` (the battery passes `stdin=subprocess.DEVNULL` to the *matrix*, which the matrix passes on unchanged) |
| F10 | any process cmdline | yes — 5 `/proc` pids matched `loader-matrix`/`matrix-battery` |
| F11 | stdout type | yes — `stdout_kind=fifo` (the matrix captures the child's stdout) |
| — | seed | yes — see F9 |

The v2 matrix spawns the candidate with a bare `subprocess.run([...])`
(`loader-matrix-v2.py:128-129`): no `env=`, no `cwd=`, no `start_new_session`,
no `stdin=`, no `timeout=`, no `RLIMIT`. The r62 battery closed each of these
channels with an explicit control (`corpus/evidence/round62/controls/c1v2-controls.txt`,
`CONTROL X01-no-neutral` … `X08-no-url-vary`, `CONTROLS_UNEXPECTED=0`). The r75
matrix closes **none** of them, and the r75 battery subjects on **none** of them.

### The structural sweep that would have caught F7/F9 exists but is not run

`corpus/evidence/round61/sniff-sweep.py` (an AST allowlist sweep for
test-detection) flags all four probes of this seat:

```
--- label-oracle sweep_exit=1
10:0 import subprocess
SNIFF_SWEEP findings=1
--- pure-harness-detection-oracle sweep_exit=1
19:0 import subprocess
26:14 path-constant /proc/%d/cmdline
26:35 attribute getppid
37:4 attribute argv
SNIFF_SWEEP findings=4
--- memorized-fixture-oracle sweep_exit=1
15:0 import json
17:0 import subprocess
SNIFF_SWEEP findings=2
--- seed-leak-order-oracle sweep_exit=1
20:0 import random
21:0 import subprocess
43:18 path-constant /proc/%d/fd/1
43:36 attribute getppid
SNIFF_SWEEP findings=4
```

No r74/r75 instrument invokes it (`grep -rn "sniff-sweep\|sniff_sweep"
corpus/evidence/round74/ corpus/evidence/round75/` → no match). QUALITY 123
requires that where a counter cannot tell a builder from a detector of the
counter, the landed bytes **also** pass a structural source sweep and that the
sweep's limits are recorded. The r75 lane has the sweep available and does not
run it.

### The r74 digest mitigation still holds — and is still unused by the matrix

The r74 critic's F4 named provenance blindness and its mitigation as the
`COUNTER_SHA256=` receipt (`loader-matrix-v2.py:105` prints it, verified
present in every run log). The matrix prints the digest but **does not verify
it against any expected value**, and the battery does not either — it only
prints `SUBJECT … sha256=<16 hex>`. So a candidate that emits a *correct*
verdict from a memorized table is indistinguishable, by digest, from the real
counter. This is the same gap class the r74 critic recorded, still open in the
successor.

---

## The three concrete forger classes the lane still misses

Ranked by how much of the claim's own scope they defeat. Each is a *full-mark*
forge (12/12, exit 0) against the frozen matrix, deterministically.

### 1. Commit-subject (label) oracle — QUALITY 126 / 119
**Spec.** One `git log -1 --format=%s <rev>` names the case outright, because
the matrix commits each case with the case name as the commit subject
(`loader-matrix-v2.py:123`, `commit --allow-empty -qm <name>`); a candidate
that maps that label to the expected `(rc, failed-set)` reaches 12/12 without
opening a protected file or implementing a check.
**Criterion served.** QUALITY 126 — a battery that passes must *discriminate*;
this subject would have to be in the battery and be REJECTED, and today no
subject of this class exists. QUALITY 119 — a base that already reaches the
target is a failed matrix; a matrix that a label-reading stub reaches 12/12 is
such a base. **Measured:** `LOADER_MATRIX=12/12 MATRIX=PASS`, exit 0, twice;
`SUBJECT FORGER NEW-label-oracle … ACCEPTED` under the frozen battery's own
rule. **Sibling overlap:** seat R75Critic independently reached the same class
as `forge-meta-subject` (`12/12`; sibling receipts at
`.ufo/waves/round-75/w1/R75Critic/logs/forge-meta-subject-run{0,1}.txt`); this
seat's finding is the same class observed independently.

### 2. Harness-source (self-inspecting) oracle — QUALITY 126 / 123
**Spec.** A candidate that reads `/proc/<ppid>/cmdline`, finds the matrix
program that invoked it, imports it, and reads the matrix's own `CASES` table
for the expected verdict per case — using **no** commit metadata, no protected
content, and no invocation counting; it identifies the case from the observed
`rev` content against the harness's own published `FILES`/`mutate()`.
**Criterion served.** QUALITY 126 (the battery must reject a forge that detects
the harness) and QUALITY 123 (the landed bytes must also pass a structural
source sweep when the counter cannot tell a builder from a detector — the
r61 `sniff-sweep.py` flags this class with `SNIFF_SWEEP findings=4`, but no
r74/r75 instrument runs it). **Measured:** `LOADER_MATRIX=12/12 MATRIX=PASS`,
exit 0, twice; `SUBJECT FORGER NEW-pure-harness-detection-oracle … ACCEPTED`.
**Note:** this is the r62 F06/F10 family transplanted from "a builder detects
its counter" to "a counter detects its matrix" — the r62 battery covered that
family for the r61 counter and the r75 battery covers it for neither.

### 3. Seed-leak order oracle — QUALITY 120
**Spec.** The matrix prints `SEED=<n>` to its own stdout before spawning any
child; when that stdout is a regular file — the mode in which every receipt in
this lane, including `corpus/evidence/round75/controls/*.txt`, was produced —
the candidate reads it from `/proc/<ppid>/fd/1`, recomputes the exact shuffled
case order, and replays the r74 order-oracle script to 12/12.
**Criterion served.** QUALITY 120 — *"orders its legs by a seed the candidate
cannot read"* and *"a call-counting forge must not reach full marks"*. The v2
shuffle satisfies the letter of the second clause (the r74 order oracle scores
7/12 or less and is rejected) but not its purpose: the seed is printed where
the candidate can read it, so the order is recoverable. **Measured:**
`LOADER_MATRIX=12/12 MATRIX=PASS`, exit 0, twice, with the recovered order
equal to the actual case order in the same run. **Scope limit, stated plainly:**
under a **pipe** stdout (the frozen battery's own `capture_output=True` mode)
the same read **blocks** rather than leaks — which is a *different* defect
(F10/F11: the matrix does not bound the child, so a blocking candidate stalls
the whole run; observed `TimeoutExpired` after 50 s). The leak is real in the
file-redirect receipt mode; the block is real in the battery mode.

---

## Supporting observations (not forger classes)

- **The five frozen forgers are correctly rejected** — the r75 battery does
  what it claims for the classes it covers (F1–F5). The gap is coverage, not
  correctness.
- **`ref-counter.py` is a genuine independent positive.** Both positives are
  ACCEPTED at 12/12 (`SUBJECT POSITIVE successor-counter … ACCEPTED`,
  `SUBJECT POSITIVE ref-counter … ACCEPTED`).
- **The r73 counter is still rejected** — 3/12, exit 1, matching the committed
  `controls/negative-r73-counter-on-v2.txt`. The r74 repair stands.
- **The three dup-heading content cases are the load-bearing addition.** With
  them, the diff-only and naive-grep forgers drop to 9/12; the r74 matrix
  (nine cases) accepted all three at 9/9.
- **`claims.md`'s own recorded limits are accurate but understated.** It states
  "a forge that fully re-implements the seven checks is, for these inputs, a
  correct counter" and "order randomisation is probabilistic … a lucky
  permutation is not excluded". Both understate the surface: F6–F9 do not
  re-implement the checks at all, and F9 removes the randomisation entirely
  rather than merely risking a lucky permutation. The r75 `claims.md` limits
  paragraph should record these three classes before C1 binds.

## Boundaries observed

- Read-only against the lane's frozen artifacts; `git rev-parse HEAD` =
  `43a7a0db52c8aabdf32735f58e09610e05200e79`; no lane file was modified (the
  frozen battery and matrix were only read and copied).
- All fixture writes were confined to `/fast/scratch/hyaku/chousa-r75/R75Scout/`.
  The only git mutation in this seat was inside the matrix's own disposable
  fixture repositories, which the frozen matrix creates under `--work` and
  removes; the matrix itself asserts `git rev-parse --show-toplevel` equals the
  fixture root before committing (`loader-matrix-v2.py:113-114`), and this seat
  did not create any fixture repository of its own.
- No network, no package install, no `uv`/`npx`/`cargo` invocation; no tool
  was installed or upgraded this round (no new tooling was needed: python3
  3.14 and git suffice). Per `/home/vgpnk/.omp/agent/RULES.md`, no pacman
  transaction was attempted; the pacman guard was never approached.
- No task tool, no subagent dispatch, no `agent://all`, no lane/fleet git or
  jj mutation, no commit, no push. Sibling seats' outputs were read only.

## Evidence index (all under this seat's folder)

- `probes/label-oracle.py` — F6 (commit-subject oracle)
- `probes/pure-harness-detection-oracle.py` — F7 (harness-source oracle)
- `probes/memorized-fixture-oracle.py` — F8 (memorized-fixture oracle)
- `probes/seed-leak-order-oracle.py` — F9 (seed-leak order oracle)
- `probes/battery-rule-sim.py` — the frozen battery's acceptance rule, replayed
- `probes/f-channel-prober.py` — r62 F-channel enumeration from inside the child
- `probes/hang-child.py` — F10 (unbounded child)
- `probes/dump-parent-stdout.py` — per-invocation parent-stdout visibility
- `probes/gen-fingerprint-table.py` — the frozen matrix's twelve fixture states
- `probes/SHA256SUMS.txt` — digests of every probe above
- `logs/` — every raw log cited in this report
  (`frozen-battery-v2-rerun.txt`, `extended-battery-v2.txt`,
  `class-matrix-evidence.txt`, `battery-rule-sim2.log`, `f-channels.txt`,
  `parent-stdout-dump.txt`, `child-channels-under-matrix.txt`, `hang.log`,
  `hang-battery.log`, `matrix-battery-extended.py`, …)

Report: `.ufo/waves/round-75/w1/R75Scout.md`
