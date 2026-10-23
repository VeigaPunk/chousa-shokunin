# CtlC1PartialLockB — C1 partial-lock controls

## Scope and result

Axes: **operability** (manifest lock lifetime/exclusivity) and **coverage** (whether the frozen detector rejects partial-lock controls).

**Important finding: control (b), exclusive lock around the probe only, MEETS-TARGET on both fresh seeds: 24/24 and 24/24. It explicitly unlocks before appending and therefore violates C1.** This is a detector coverage finding, not candidate admission or permission to change C1.

Read `corpus/evidence/round32/claims.md` first, then both counter docstrings. Ran only BASE-derived scratch controls, pristine BASE, and restored BASE bytes. No candidate implementation, C2 detector, gate selftest, judge, or other orchestration runtime was run. No counter was edited.

Path abbreviations used below:
- `L` = `/home/vgpnk/Projects/shokunin/chousa-shokunin` (every counter's cwd).
- `S` = `/fast/scratch/hyaku/chousa-r32/w1/CtlC1PartialLockB` (all experimental gate files and counter temporary fixtures).
- `A` = `.ufo/waves/round-32/w1/CtlC1PartialLockB` relative to `L` (all extra retained artifacts).

## Inputs and bounded method

Observed initial `timeout 30s df -h /fast`, exit 0: 236G available. Copied `L/tools/research-gate.sh` into `S/pristine-gate.sh`, then four named copies. The input SHA-256 was the frozen BASE gate hash:

`0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`

Observed `timeout 30s sha256sum tools/research-gate.sh corpus/evidence/round32/c1-count.py corpus/evidence/round32/c2-count.py`, exit 0. C1 counter SHA-256:

`9e787e80b215f6522335c639d5e1b2e60d0a5812b83a9760daf8be9f78415885`

It matched the output of `timeout 30s git show 4111607c857bc29ff31883bc095ae00afb527e50:corpus/evidence/round32/c1-count.py | timeout 30s sha256sum`, exit 0. Every completed receipt carries this counter hash.

Exact counter commands, observed exits, summary output, and **every per-trial result** are retained in `A/runs-and-trials.txt:8-473`. The command shape was:

```text
timeout 840s prlimit --nproc=N --as=4294967296 env C1_TMP=S C2_TMP=S TMPDIR=S python3 L/corpus/evidence/round32/c1-count.py --gate S/CONTROL.sh --seed SEED --receipt L/A/RECEIPT.json
```

The artifact expands every abbreviation and records N separately for every actual invocation. Initial runs used N=2000; later runs used N=4096 and at most two counters concurrently after harness errors. Each counter remained frozen; resource ceilings do not alter its detector.

Expected sensitivity: each of the four controls violates `claims.md:23-28`, so a detector establishing that contract should reject it, rather than reporting the 24/24 target. P1 itself is at `claims.md:36-40`; trial semantics are in `c1-count.py:23-45`.

## Mutants, hashes, scores, classes and trials

Only the manifest append region was changed, except (c)'s necessary early probe in `verify_all` before verification. Minimal diffs are retained in `A/*.patch`. **The scratch gate paths are now restored**, so use these patches and recorded mutated hashes to reconstruct the experiments.

| Control | Mutated file | Mutated SHA-256 |
|---|---|---|
| (a) Probe/decide delimiter before taking EX; lock only append | `a-append-only.sh` | `4a39b99728ec559f9d3d0c4140be410dec457f69c65a5a7184bbbcc144cae1ca` |
| (b) EX around probe; explicit unlock before append | `b-probe-only.sh` | `034f786be1570136b27d72ec630e24be1c6a673ce53434d476af94f4bb5f0340` |
| (c) Cache last byte before verification; take EX later but use stale cached delimiter | `c-cached-probe.sh` | `59ea2a22bc7293715b15eae245046bab71ad541b641fedad4e62169181f9949c` |
| (d) SH, not EX, around probe and append | `d-shared-lock.sh` | `76c4c073bb5990a220e9adf69acc674b907ecc1579d27588954d6652b40c0b78` |

All hashes were observed with `timeout 30s sha256sum S/*.sh`, exit 0, and agree with the completed mutant receipts.

Every score below is the actual `APPEND_SERIALIZED` numerator over 24. Class columns are actual printed matches; their denominators are shown in the headers. All receipts reside in `A/`.

| Control | Seed | Score | F_unterminated /12 | L_empty /4 | L_terminated /4 | L_unterminated /4 | Exit | Receipt | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| a | 32471011 | 1/24 | 1 | 0 | 0 | 0 | 1 | `a-s32471011.json` | MISSES |
| a | 32471012 | 4/24 | 4 | 0 | 0 | 0 | 1 | `a-s32471012.json` | MISSES |
| b | 32471021 | 24/24 | 12 | 4 | 4 | 4 | 0 | `b-s32471021.json` | MEETS-TARGET |
| b | 32471022 | 24/24 | 12 | 4 | 4 | 4 | 0 | `b-s32471022.json` | MEETS-TARGET |
| c | 32471033 | 0/24 | 0 | 0 | 0 | 0 | 1 | `c-s32471033.json` | MISSES |
| c | 32471034 | 0/24 | 0 | 0 | 0 | 0 | 1 | `c-s32471034.json` | MISSES |
| d | 32471043 | 7/24 | 7 | 0 | 0 | 0 | 1 | `d-s32471043.json` | MISSES |
| d | 32471044 | 11/24 | 11 | 0 | 0 | 0 | 1 | `d-s32471044.json` | MISSES |

Per-class and per-trial evidence in `A/runs-and-trials.txt`:
- (a): summaries `48-52`, `83-87`; every trial `53-76`, `88-111`.
- (b): summaries `118-122`, `153-157`; every trial `123-146`, `158-181` (all 48 trials have `pass=true`, `fails=[]`).
- (c): summaries `188-192`, `223-227`; every trial `193-216`, `228-251`.
- (d): summaries `258-262`, `293-297`; every trial `263-286`, `298-321`.

The frozen counter prints summaries, not individual trial lines; the per-trial appendix faithfully renders each receipt's `trials` fields. For example, (a)'s `trial=02` on seed 32471011 is `L_terminated`, `pass=false`, `fails=["invalid-json-line"]` (`runs-and-trials.txt:55`); (c)'s first trial on 32471033 has `fails=["blank-line","invalid-json-line"]` (`:193`); (d)'s trial 1 on 32471043 has the same failures (`:264`). These are observations, not assumed failure modes.

## Why (b) passed despite violating C1

The preserved `A/b-probe-only.patch:9-20` shows opening the manifest for append, taking EX, probing its last byte, **`flock -u "$jfd"`**, then `printf` to that fd. Unlocking is unconditional and precedes delimiter construction and the write. That is directly outside the lock-through-write contract.

The detector checks a different, weaker observable:
1. In L trials, it initially holds EX and accepts writers that are listed as blocked waiters (`c1-count.py:213-223`). This control blocks at its probe lock, so that synchronization does not distinguish it from a correctly scoped lock.
2. It checks unchanged seed bytes, appends the cooperating fragment, then releases its lock (`:224-237`). It does **not** reacquire a cooperating lock in the control's later probe-to-write gap, or inspect whether the append itself is under EX.
3. Subsequent checks inspect exit codes, inode/prefix and final JSONL bytes (`:240-245`, `:157-195`), not lock ownership at append. F trials likewise inspect only their final outcome.

Observed result: both seeds produced correct final bytes and all 24 trial predicates passed. [INFERENCE] The serialized, subprocess-based probes normally leave enough time for the preceding writer's immediate post-unlock shell `printf` to complete before the next writer's probe reads; that explains these successful schedules but is not a claim about every schedule. The exact observable gap is established without that scheduling inference: **no counter check requires lock ownership during this control's append**. The two full receipts are a surviving contract-violating control, not proof of C1.

## Pristine, restored, and mutation-verdict limits

The same frozen bounded detector ran on pristine bytes before mutation, on all four mutant byte strings twice, and on each exact restored gate. Pristine and restored runs used seed 32471001:

| State | APPEND_SERIALIZED | F_unterminated | L_empty / L_terminated / L_unterminated | Exit | Receipt in A |
|---|---:|---:|---|---:|---|
| Pristine BASE | 5/24 | 5/12 | 0/4, 0/4, 0/4 | 1 | `pristine-s32471001.json` |
| Restored a | 5/24 | 5/12 | 0/4, 0/4, 0/4 | 1 | `restored-a-s32471001.json` |
| Restored b | 9/24 | 9/12 | 0/4, 0/4, 0/4 | 1 | `restored-b-s32471001.json` |
| Restored c | 8/24 | 8/12 | 0/4, 0/4, 0/4 | 1 | `restored-c-s32471001.json` |
| Restored d | 8/24 | 8/12 | 0/4, 0/4, 0/4 | 1 | `restored-d-s32471001.json` |

Evidence: `A/runs-and-trials.txt:8-41,323-461`. Random seed fixes fixtures/order, not concurrent process scheduling; these observations do not establish deterministic counts for BASE.

**Strict killed-mutant attribution is INCONCLUSIVE because pristine BASE already fails the detector. No killed-mutant claim is made.** The requested negative-control verdicts remain a/c/d MISSES and b MEETS-TARGET, with b a demonstrated predicate survivor.

Exact-byte restoration was performed with bounded `cp` from `S/pristine-gate.sh`, followed by four `timeout 30s cmp PRISTINE CONTROL` commands, each exit 0/no output, then `timeout 30s sha256sum S/*.sh`, exit 0. All five paths have the exact original hash `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`. `A/byte-restoration.txt` records the before/mutated/restored evidence; all restored receipts independently record that same hash.

## Errors, process completion, and bounds

- Initial four-way batch: c seed 32471031 and d seed 32471041 each exited 2 with `c1-count: trial 1 harness error: BlockingIOError(11, 'Resource temporarily unavailable')`. Neither produced a complete receipt; both are **INCONCLUSIVE**, not scored misses. Exact attempted commands/output are retained in `A/runs-and-trials.txt:463-473` and `A/initial-harness-errors.txt`. Later completed runs used fresh seeds and the still-bounded N=4096 ceiling with only two counters concurrently; no failed receipt was overwritten.
- One setup `cp` invocation was malformed and exited 1; the pristine copy existed, the missing controls were then copied with separate successful bounded commands before editing.
- A requested PTY was unavailable; the pristine command ran successfully without a terminal and exited 1 on its 5/24 score. Reported this tool behavior through `xd://report_issue`; no tool was installed or updated.
- After the failed batch and again after all detector runs, `timeout 30s pgrep -af '^bash /fast/scratch/hyaku/chousa-r32/w1/CtlC1PartialLockB/'` returned exit 1/no output. No matching gate process remained. All counter commands completed in the foreground; no background jobs or subagents were started by this seat.
- No network access, installs, Git/jj writes, production-file writes, or sibling-source edits. Retained patches, receipts and evidence are only in A; this report is at the requested trailer path. Each retained artifact is under 1 MiB (the full run/trial appendix is 34,987 bytes).

This report makes no candidate judgment and does not amend the frozen claim or detector.
