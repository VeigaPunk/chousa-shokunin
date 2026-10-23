# MutC1Gate — round 32 attempt 2, wave 2

**Verdict: HOLDS within this C1 mutation probe.** The frozen v2 counter killed all five non-equivalent requested mutants. Mutant (e), the expected-equivalent fresh append open under the still-held lock, survived. The native selftest has reproduced coverage gaps: (b) early unlock and (d) probe-before-lock both passed. This is not a C1 candidate failure or a C2 result.

Axes: **operability** (serialized manifest append) and **coverage** (which detector kills which mutant).

## Inputs, isolation, and detector commands

Read `corpus/evidence/round32/claims.md:119-159` before probing; C1 contract is at `:23-28`. Landed revision assigned: `5d8a170795dcf48c3746a4f03dee9cfe32812834`. Copied only the gate and its selftest's `PROVINCE.md` dependency into seven private roots under `/fast/scratch/hyaku/chousa-r32/w2/MutC1Gate/{pristine,a,b,c,d,e,f}/`; every gate occupied `tools/research-gate.sh` below its root. No production gate/corpus, index, jj state, sibling source, or fleet source was edited.

Pristine gate SHA-256, denoted **H** below:
`10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098`.
Unmodified committed counter SHA-256:
`e6bf95313ad603ff75e03bb64fbe5a2689a9dfe9bc4c0715a21012383508d891`.

All runs used seed **323200**, making one shared pristine baseline usable for all six probes. Each mutated copy was subsequently restored and rerun with both detectors and that same seed. There were **26 detector invocations: 13 counters and 13 full selftests**; none timed out, no captured output was truncated, and no baseline/restored invocation failed. At most two counters overlapped; batches were synchronous, without subagent dispatch or persistent jobs.

Exact expanded commands, environments, durations, exit codes, and before/after detector hashes are in [`MutC1Gate/results.json`](MutC1Gate/results.json) and each `MutC1Gate/<phase>-<name>-<detector>.run.json`. Reproduction templates (substitute the recorded name/phase):

```sh
prlimit --nproc=8000 --fsize=33554432 timeout --signal=TERM --kill-after=10s 900s python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count-v2.py --gate /fast/scratch/hyaku/chousa-r32/w2/MutC1Gate/<name>/tools/research-gate.sh --seed 323200 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w2/MutC1Gate/<phase>-<name>-counter.json
prlimit --nproc=8000 --fsize=33554432 timeout --signal=TERM --kill-after=10s 1800s bash /fast/scratch/hyaku/chousa-r32/w2/MutC1Gate/<name>/tools/research-gate.sh --selftest
```

For both commands, cwd was the selected private lane root; all `CHOUSA_*`, `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` variables were unset. `TMPDIR`, `C1_TMP`, and `C2_TMP` were `/fast/scratch/hyaku/chousa-r32/w2/MutC1Gate/tmp`, outside every private lane root. [`MutC1Gate/run-probes.py`](MutC1Gate/run-probes.py) records the runner; it does not edit gates or counters. Mutation receipts are labelled `mutated-*`, never candidates; companion run receipts explicitly classify them as controls.

## Results

Expected detector: the counter must reject (a), (b), (c), (d), and (f) because each violates the exclusive probe-through-write critical section. An equivalent implementation need not be killed. Native selftest outcomes below are measured, not inferred.

| Mutant | Small behavior change | Counter count; exit | Full selftest; exit | Killed-by |
|---|---|---|---|---|
| (a) | Remove acquisition/error block at landed `tools/research-gate.sh:3296-3299` | [0/24; 1](MutC1Gate/mutated-a-counter.json) | [FAIL 1/241; 1](MutC1Gate/mutated-a-selftest.stdout) | Counter + selftest |
| (b) | Add `flock -u "$jfd"` immediately before write at `:3306` | [0/24; 1](MutC1Gate/mutated-b-counter.json) | [PASS 241; 0](MutC1Gate/mutated-b-selftest.stdout) | Counter only |
| (c) | Change exclusive `flock -x` to shared `flock -s` at `:3296` | [0/24; 1](MutC1Gate/mutated-c-counter.json) | [FAIL 1/241; 1](MutC1Gate/mutated-c-selftest.stdout) | Counter + selftest |
| (d) | Move last-byte probe `:3300-3302` before acquisition | [0/24; 1](MutC1Gate/mutated-d-counter.json) | [PASS 241; 0](MutC1Gate/mutated-d-selftest.stdout) | Counter only |
| (e) | Write with fresh `>>"$JSON_ARG"` instead of `>&"$jfd"` at `:3306`, retaining lock | [24/24; 0](MutC1Gate/mutated-e-counter.json) | [PASS 241; 0](MutC1Gate/mutated-e-selftest.stdout) | Neither; expected equivalent |
| (f) | Replace acquisition/error block by `flock -n "$jfd" || true` | [0/24; 1](MutC1Gate/mutated-f-counter.json) | [FAIL 1/241; 1](MutC1Gate/mutated-f-selftest.stdout) | Counter + selftest |

Every failing selftest reported `c1lk-holder-blocks-append` with `gate-not-blocked-on-lock`; its summary was `RESEARCH_GATE_SELFTEST: FAIL (1/241 cases)`. Every passing selftest reported `RESEARCH_GATE_SELFTEST: PASS (241 cases, 0 skipped)`. The second-append case passed for all mutants. Full stdout/stderr and exit codes are retained for every invocation.

All counter runs on landed bytes, including every restored copy, are disclosed here:

| Phase/name | Counter; exit | Full selftest; exit |
|---|---|---|
| Shared pristine | [24/24; 0](MutC1Gate/pristine-pristine-counter.json) | [PASS 241; 0](MutC1Gate/pristine-pristine-selftest.stdout) |
| Restored a | [24/24; 0](MutC1Gate/restored-a-counter.json) | [PASS 241; 0](MutC1Gate/restored-a-selftest.stdout) |
| Restored b | [24/24; 0](MutC1Gate/restored-b-counter.json) | [PASS 241; 0](MutC1Gate/restored-b-selftest.stdout) |
| Restored c | [24/24; 0](MutC1Gate/restored-c-counter.json) | [PASS 241; 0](MutC1Gate/restored-c-selftest.stdout) |
| Restored d | [24/24; 0](MutC1Gate/restored-d-counter.json) | [PASS 241; 0](MutC1Gate/restored-d-selftest.stdout) |
| Restored e | [24/24; 0](MutC1Gate/restored-e-counter.json) | [PASS 241; 0](MutC1Gate/restored-e-selftest.stdout) |
| Restored f | [24/24; 0](MutC1Gate/restored-f-counter.json) | [PASS 241; 0](MutC1Gate/restored-f-selftest.stdout) |

## What the detectors observed

Receipts retain every trial's failed checks:
- (a) and (f): all 12 held-lock trials appended under the cooperating lock; 16 trials also reported blank/invalid JSON lines, and eight failed the expected-prefix check.
- (b) and (c): every trial reported both `blank-line` and `invalid-json-line`.
- (d): every trial reported `invalid-json-line`; 16 also reported `blank-line`.
- (e): no failed checks; all four classes matched fully.

The selftest's holder writes its fragment **before** launching the gate (`tools/research-gate.sh:7123,7131-7144`), then releases the lock for a single gate writer (`:7161-7163`); its second-append checks are sequential (`:7193-7194`). The frozen counter instead appends a cooperating unterminated fragment while holding the lock after writers reach it (`corpus/evidence/round32/c1-count-v2.py:245-273`) and delays manifest writes (`:85-93`). [INFERENCE] These fixture differences explain the native selftest's survival of both early unlock and pre-lock probing. The selftest's waiter matcher specifically requires `WRITE` (`tools/research-gate.sh:7149`), so mutant (c)'s diagnostic is an exclusive-waiter check, not proof that a shared waiter never blocked.

[INFERENCE] Mutant (e) is equivalent for the tested stable-PATH, same-inode cooperating appenders: the original fd retains the exclusive lock across the probe and append even though the append obtains a fresh file description. Its survival is not classified as a coverage defect.

## Mutation and restoration evidence

Each original copy began at **H**. Exact patch artifacts are `MutC1Gate/mutant-{a,b,c,d,e,f}.patch`. Mutant hashes:

| Mutant | Mutated gate SHA-256 | Restored SHA-256 |
|---|---|---|
| a | `f17c77bb7783f2cb0a5844e57169cf57f412200bffe34a8c67cca1f5588303c0` | H |
| b | `409bf38f11103196491316f7b9859409d734d2081d1ab59c7a3a86776bbf8582` | H |
| c | `2ca13c48873ba1bd3f0f359fce97cf34328ee4785456dcc384c1ea3a6cc18a3b` | H |
| d | `a86cb5198da449419f94b6eb52ad7e2393483c162bd3229a9f109b85511059cf` | H |
| e | `eb3038655142dee81da2ae89e83aa0291c4ed78d474ed88ef321e768ddaa3235` | H |
| f | `3746d9e0baa7a8a1d4fdcc7f5587c640d9c6806ecc1a971af6efe5185998c016` | H |

[`MutC1Gate/restoration.json`](MutC1Gate/restoration.json) additionally records direct byte equality to the saved pristine bytes for all six copies, each `true`. Every detector run's before/after gate hash matched, and each restored copy passed both detectors after restoration.

Cleanup: `timeout 15 pgrep -af '/fast/scratch/hyaku/chousa-r32/w2/MutC1Gate/(a|b|c|d|e|f|pristine|tmp)(/|$)'` exited **1**, with no output (no matching probe processes). Removed only the three leftover selftest fixture paths inside the private `tmp`; a directory read then returned empty. `timeout 15 /usr/bin/du -sh` over only my scratch/artifact directories exited 0 and reported 2.3 MiB/432 KiB before the final small metadata additions. Before this report, the largest artifact was `results.json`, 46,195 bytes; all artifacts are below 1 MiB. No network access, installs, git/jj writes, integration, or repairs.

Limits: one fixed seed per mutant; this probes detector sensitivity, not an exhaustive concurrency proof or the full two-fresh-seed P1 admission condition. No below-target run occurred on landed bytes in this seat. This seat did not run C2, adjudicate other receipts, or examine path replacement/non-cooperating writers. Stop after the assigned six mutation probes.
