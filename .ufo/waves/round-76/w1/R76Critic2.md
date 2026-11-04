# R76Critic2 — attack on matrix-battery-v3 (round 76, wave 1)

Scope: the battery itself (`corpus/evidence/round76/matrix-battery-v3.py`), not the matrix, as assigned. Leaf seat; no subagents, no network, no production edits, no lane/fleet git mutation. Frozen instruments were not edited (sha256 below). Scratch under `/fast/scratch/hyaku/chousa-r76/R76Critic2/` was deleted before yield; receipts and subject sources are copied to `.ufo/waves/round-76/w1/R76Critic2/`.

**BATTERY_SURVIVORS=4** (definition and members in §5).

## 0. Frozen baseline and instrument digests

- `sha256sum corpus/evidence/round76/matrix-battery-v3.py` = `217ae367c7e6e4ed23d1e6c1412de50370f309ba12d4a1703eaff386b7094360` (matches claims.md).
- `sha256sum corpus/evidence/round76/loader-matrix-v3.py` = `b79d6441057a01b27eb465c6b0625cd46502114f8b622b370c2cd2805c81913f` (matches claims.md).
- Baseline, unmodified battery: `python3 -B corpus/evidence/round76/matrix-battery-v3.py --matrix corpus/evidence/round76/loader-matrix-v3.py --work <scratch>/work/baseline` → **exit 0**, `BATTERY=PASS forgers_rejected=11/11 positive=2/2` (receipt `receipts/r0-baseline.txt`). The frozen predicate reproduces; the attacks below are outside its frozen subject set.
- Attack harness: `chain/mkchain.py` writes a scratch copy of the frozen battery whose only change is an appended override of `POSITIVES`/`FORGERS` (`receipts/chain-diff-vs-frozen.txt`, diff exit 1 = the override lines only). Process tree is the real one: battery → matrix (`loader-matrix-v3.py`, env `LOADER_MATRIX_CHILD_TIMEOUT=3`) → subject. Every chain run uses the frozen `run_matrix`, scoring and predicate.
- Tools: none installed or upgraded (python 3.14.8 already present). No pacman use.

## 1. Can a subject detect the battery? Yes — and the premise needs one correction

Probe `subjects/probe-channels.py` (behaves as constant-PASS) run through the chain. Receipt `receipts/r1-probe-chain.txt` (exit 0, `BATTERY=PASS forgers_rejected=1/1`, probe 4/12 both runs); records `receipts/probe-records.jsonl` (24 = 12 cases × 2 runs).

Observed by the subject:
- `env LOADER_MATRIX_CHILD_TIMEOUT=3` — inherited; set only by the battery's `run_matrix`. Human runs leave it unset (matrix default 20 s).
- **Direct parent is the matrix, not the battery.** `ppid_cmdline` = `python3 -B …/loader-matrix-v3.py --counter …/<hexdir>/subject.py --work …`. The battery is the **grandparent** (`gppid_cmdline` = `python3 -B …/matrix-battery-v3.py --matrix …`). The claim that "the parent cmdline names matrix-battery-v3.py" is incorrect; the grandparent does.
- `argv` exposes the random hex dir and the matrix path, not the forger name (the salt/hex hygiene holds against naming).
- Stdout of the parent is a pipe.

So a subject can key on either the env fingerprint, the grandparent command line, or the direct parent command line. QUALITY 126 already lists "parent or any process's command line" and env keys as forger channels; round 76's forger set uses the parent-cmdline channel only in `forge-harness-source` (reads the matrix's own `CASES`), and does not test a parent-keyed honest/forger split.

## 2. Does it behave differently watched vs unwatched? Yes — three subjects built and scored

- `subjects/w-battery.py`: honest (real round-74 counter) iff env `LOADER_MATRIX_CHILD_TIMEOUT=3` or grandparent cmdline names `matrix-battery-v3.py`; constant-PASS otherwise.
- `subjects/w-matrix.py`: honest iff the direct parent cmdline names `loader-matrix-v3.py`; constant-PASS otherwise.
- `subjects/w-battery-inverse.py`: forger when the battery watches it; honest otherwise.

Scored through the frozen battery (both roles, chain) and through the frozen matrix run directly (no battery env, default bound — the lane's binding run). Human-direct output compared on a scratch deployed fixture where the real counter returns the correct FAIL (`fixture-del`: LOG.md sentinel line deleted; real counter `C2=FAIL checks=6/7`, exit 1, `receipts/r3-real-on-deletion.txt`).

| subject | battery as positive | battery as forger | matrix run directly (lane binding) | human run on deletion fixture |
|---|---|---|---|---|
| w-battery | ACCEPTED 12/12 ×2 (exit 0) | MISS → `BATTERY=FAIL` (exit 1) | 4/12 FAIL (exit 1) — caught | `C2=PASS checks=7/7 const` (wrong) |
| w-matrix | ACCEPTED 12/12 ×2 (exit 0) | MISS → `BATTERY=FAIL` (exit 1) | **12/12 PASS (exit 0) — bound** | `C2=PASS checks=7/7 const` (wrong) |
| w-battery-inverse | MISS 4/12 → `BATTERY=FAIL` (exit 1) | REJECTED 4/12 → `BATTERY=PASS` (exit 0) | 12/12 PASS (exit 0) — honest | honest |

Receipts: `receipts/chain-w-*-{positive,forger}.txt`, `receipts/direct-matrix-w-*.txt`, `receipts/r3-human-w-matrix.txt`.

Reading:
- **Coverage hole (w-matrix).** Every battery subject is launched by the matrix, so a subject keyed to the matrix's direct parent is observationally identical inside the battery and inside the lane's binding run. Only a human direct run differs, and the battery never does one. The matrix therefore binds a counter that is a constant-PASS forger when a human runs it. Had w-matrix been placed in the forger row, the frozen battery would correctly report `BATTERY=FAIL` (`chain-w-matrix-forger.txt`). The frozen 11-forger set simply does not contain it, so `BATTERY=PASS` is silent on this class. This is coverage, not a scoring bug in the battery.
- **Observation-dependent credit (w-battery-inverse).** The forger row awards REJECTED for a subject that is honest in deployment (lane run 12/12). `BATTERY=PASS` is evidence only about watched runs.
- w-battery is caught by the lane run (env is not set there) and by the battery's own forger row. The battery and lane gate are safe against battery-keyed subjects, not against matrix-keyed ones.

## 3. Acceptance rule (`run_matrix` / `run()` predicate) — attacks

Rule: a case passes iff `not timed_out and rc == expected_rc and len(checks)==7 and failed == expected_failed and any(line.startswith("C2=<PASS|FAIL> checks="))`; the CHECK parse is last-wins; battery positive needs rc 0 and full marks in both runs; forger needs rc 1 and marks < full in both runs.

| subject | what it does | battery result | lane binding run | scored |
|---|---|---|---|---|
| slow-correct 2.8 s (total ≈2.85 s) | correct, sleeps 2.8 s | positive ACCEPTED ×2 | 12/12 PASS | correct |
| slow-correct 2.95 s | correct, sleeps 2.95 s | positive ACCEPTED ×2 | 12/12 PASS | correct (just under bound) |
| slow-correct 3.2 s | correct, sleeps 3.2 s → child killed at 3 s | positive **MISS** → `BATTERY=FAIL`; forger **REJECTED** (0/12) → `BATTERY=PASS` | 12/12 PASS (default 20 s bound) | **false reject** in the positive slot; the same correct subject earns forger credit for the timeout reason. Reason-blind. |
| exit2-correct (correct output, process exits 2) | nonconforming exit | positive MISS; forger REJECTED | 0/12 FAIL | scored per contract (exit must be 0/1); not a survivor |
| extra-c2-first (`C2=PASS checks=7/7 extra` printed before the real summary) | contradictory summary | positive ACCEPTED ×2 | **12/12 PASS** | **wrongly accepted**: on the deletion fixture it prints `C2=PASS` before the true `C2=FAIL` |
| extra-c2-last (same line printed after) | contradictory summary | positive ACCEPTED ×2 | **12/12 PASS** | **wrongly accepted**: deletion fixture ends with `C2=PASS checks=7/7 extra` |
| extra-c2-contradict (`C2=FAIL checks=0/7 stray` appended, unconditional) | contradictory summary | positive ACCEPTED ×2 | **12/12 PASS** | **wrongly accepted**: count contradicts the real `checks=6/7` on the deletion fixture; the rule uses `any()` and never vetoes a stray line |
| extra-check-flip (correct, plus trailing `CHECK C2-6 PASS stray`) | last-wins CHECK parse | positive MISS; forger REJECTED (8/12) | 8/12 FAIL | **false reject** of a correct counter (last-wins overwrites C2-6) |

Answer to the assigned question: stray `C2=` lines are **not** scored wrongly when they only add lines beside a matching summary, but the rule is existence-based (`any`), so a counter that prints a contradictory `C2=PASS` (or `C2=FAIL`) alongside the true summary is accepted 12/12 in both runs. The CHECK channel is last-wins, so an extra trailing CHECK line makes a correct counter fail. A slow-but-correct counter is scored correctly only below about 3 s; at 3.2 s it is rejected as a stall and, in the forger slot, counted as a rejected forger.

## 4. Other channels checked

- Ordering: the 2 × 12 battery chain runs produced only exact-battery verdicts; no battery-level flakiness observed in the baseline or chain runs (every chain run exit code matched its expected verdict except where the attacks themselves intend otherwise).
- Forger randomness: a subject that is honest in exactly one of the two runs gives MISS (battery FAIL), so intermittence cannot evade the forger row. Confirmed by the rule, not separately exercised.
- Runtime: the real round-74 counter takes ~36 ms per invocation (`receipts/r2-real-counter-lane-head.txt`, exit 0), so the 3 s bound leaves a wide margin for honest counters; the boundary sits between 2.95 s and 3.2 s of subject sleep.

## 5. BATTERY_SURVIVORS

Definition used: a subject whose human-run output is wrong on the deployed fixture (a verdict/count/exit line disagrees with the real counter on `fixture-del`) and which the lane binding run (frozen matrix, no battery env, default bound) passes 12/12.

Members (n=4):
1. `w-matrix` — human run prints `C2=PASS checks=7/7` where truth is FAIL; bound 12/12. (strict: the whole verdict is wrong.)
2. `extra-c2-first` — human output contains a PASS verdict line before the true FAIL; bound 12/12.
3. `extra-c2-last` — human output ends with a PASS verdict line; bound 12/12.
4. `extra-c2-contradict` — human output contains `C2=FAIL checks=0/7 stray` beside the true `checks=6/7`; bound 12/12.

Not survivors: `w-battery` (lane run 4/12 FAIL), `extra-check-flip` (lane 8/12 FAIL), `exit2-correct` (lane 0/12 FAIL), the slow subjects (correct; the 3.2 s one is a false reject, not a survivor). `w-battery-inverse` is battery over-credit (forger row REJECTED while honest in deployment; BATTERY=PASS), counted separately as **BATTERY_OVERCREDIT=1**. Likewise slow-3.2 forger REJECTED is over-credit for the timeout reason.

## 6. Verdict on the claim

- The frozen predicate `BATTERY=PASS forgers_rejected=11/11 positive=2/2` reproduces (exit 0). The frozen 13 subjects and their verdicts are not refuted.
- C1's kill rule is about the frozen set and passes; the attacks show a gap the battery does not cover: a candidate keyed to the matrix's direct parent (w-matrix) is bound by the matrix's lane run while being a constant-PASS forger for a human. QUALITY 126 names this channel class; the frozen battery does not test it.
- Acceptance-rule defects (stray contradictory summaries accepted 12/12; last-wins CHECK flip rejects a correct counter; 3 s bound rejects a correct 3.2 s counter) are real but outside the frozen set.
- Recommendation for a successor (not applied; frozen bytes must not be amended after scoring): add a parent-cmdline-keyed subject to the forger row, add a "stray summary line" forger and a "contradictory summary must veto" check, and report a bound-timeout separately from a stall. Per the claims' kill rule, any change is a new claim.

## 7. Receipts (`.ufo/waves/round-76/w1/R76Critic2/receipts/`)

- `frozen-sha256.txt` — digests of the two frozen instruments.
- `r0-baseline.txt` — frozen battery, exit 0, `BATTERY=PASS forgers_rejected=11/11 positive=2/2`.
- `r1-probe-chain.txt` (exit 0) and `probe-records.jsonl` — channel probe.
- `r2-real-counter-lane-head.txt` (exit 0) — real counter timing.
- `r3-real-on-deletion.txt` (exit 1, `C2=FAIL checks=6/7`), `fixture-del-revs.txt`, `r3-human-{w-matrix,extra-c2-first,extra-c2-last,extra-c2-contradict}.txt` — human-run outputs on the deployed fixture.
- `chain-<subject>-{positive,forger}.txt` — battery chain runs; each ends with `EXIT=<battery exit>`. Battery exits: w-battery 0/1 (positive/forger), w-matrix 0/1, w-battery-inverse 1/0, exit2-correct 1/0, extra-c2-first 0/1, extra-c2-last 0/1, extra-c2-contradict 0/1, extra-check-flip 1/0, slow-2.8 0/1, slow-2.95 0/1, slow-3.2 1/0.
- `direct-matrix-<subject>.txt` — frozen matrix run directly (no battery env, default bound), each ends with `EXIT=`: w-battery 1, w-matrix 0, w-battery-inverse 0, exit2-correct 1, extra-c2-first 0, extra-c2-last 0, extra-c2-contradict 0, extra-check-flip 1, slow-correct 2.8/2.95/3.2 all 0.
- `chain-diff-vs-frozen.txt` — chain copy differs from the frozen battery only by the override.
- `subjects/*.py` — all probe and attack subjects; `chain/mkchain.py` — chain builder.

Commands with exit codes are recorded in each receipt's `EXIT=` line. The scratch tree (`/fast/scratch/hyaku/chousa-r76/R76Critic2/`) was removed after copying.
