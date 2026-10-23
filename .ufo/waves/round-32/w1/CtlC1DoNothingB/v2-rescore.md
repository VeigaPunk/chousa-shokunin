# C1 do-nothing control — frozen design v2 rescore

**Axes:** operability (manifest locking/framing); coverage (all 24 C1 trials per seed).

**Control: unmodified base. Verdict: MISSES on both completed runs.** This seat built no other control or oracle and scored no candidate.

- Gate: `/fast/scratch/hyaku/chousa-r32/w1/CtlC1DoNothingB/base-control/tools/research-gate.sh`.
- Gate SHA-256: `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`. Matching the pristine hash is intentional for this do-nothing control; there were no mutated bytes to rebuild.
- Counter: `corpus/evidence/round32/c1-count-v2.py`, SHA-256 `e6bf95313ad603ff75e03bb64fbe5a2689a9dfe9bc4c0715a21012383508d891`. `timeout 25s env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 3d586d3a:corpus/evidence/round32/c1-count-v2.py | timeout 25s sha256sum` matched the live counter hash. No counter edit.
- `C1_TMP=C2_TMP=TMPDIR=/fast/scratch/hyaku/chousa-r32/w1/CtlC1DoNothingB/v2-tmp`, outside the gate's lane root `.../base-control/`.

## Scores

Receipts below are under `.ufo/waves/round-32/w1/CtlC1DoNothingB/v2/`.

| Fresh seed | Count | F_unterminated | L_empty | L_terminated | L_unterminated | Exit | Verdict | Receipt |
|---|---|---|---|---|---|---|---|---|
| 5713427460325524559 | APPEND_SERIALIZED=0/24 | 0/12 | 0/4 | 0/4 | 0/4 | 1 | MISSES | `base-s5713427460325524559.json` |
| 5847843539014860249 | APPEND_SERIALIZED=0/24 | 0/12 | 0/4 | 0/4 | 0/4 | 1 | MISSES | `base-s5847843539014860249.json` |

Both receipts: lines 3-9 record the 300000 µs delay, successful 0.303 s delay self-check, counter/gate hashes and solo reference exit 0; lines 12-21 record the scores and `predicate_holds=false`. Both command stderr streams were empty. Frozen target is 24/24 (`corpus/evidence/round32/claims.md:143-154`).

## Every failing trial, grouped by identical checks

Trial ids are zero-based; these groups enumerate all 24 trials in each receipt. Source: each receipt's `trials` array, lines 22-267.

| Seed | Class | Trial ids | Failed checks (verbatim) |
|---|---|---|---|
| 5713427460325524559 | F_unterminated | 0,2,4,5,7,13,15,16,17,21,22,23 | `blank-line`, `invalid-json-line` |
| 5713427460325524559 | L_unterminated | 1,3,10,11 | `appended-under-cooperating-lock`, `blank-line`, `invalid-json-line` |
| 5713427460325524559 | L_empty | 6,8,14,20 | `appended-under-cooperating-lock`, `prefix-rewritten` |
| 5713427460325524559 | L_terminated | 9,12,18,19 | `appended-under-cooperating-lock`, `prefix-rewritten` |
| 5847843539014860249 | F_unterminated | 0,2,3,11,12,13,15,17,18,21,22,23 | `blank-line`, `invalid-json-line` |
| 5847843539014860249 | L_unterminated | 1,6,7,8 | `appended-under-cooperating-lock`, `blank-line`, `invalid-json-line` |
| 5847843539014860249 | L_empty | 4,10,14,16 | `appended-under-cooperating-lock`, `prefix-rewritten` |
| 5847843539014860249 | L_terminated | 5,9,19,20 | `appended-under-cooperating-lock`, `prefix-rewritten` |

Thus all 24 locked trials failed the hold check, and all 24 free-writer trials failed framing. The diagnostic qualifications in the original report still apply: `prefix-rewritten` is an expected-prefix mismatch, not proof of destructive rewriting; blank-line parsing can itself produce `invalid-json-line`. No glued-line finding is claimed.

## Executed commands and resource exception

Both completed score commands ran concurrently, cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`, with the environment above:

```sh
timeout --signal=TERM --kill-after=10s 850s prlimit --nproc=8000 --as=4294967296 --fsize=1048576 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count-v2.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC1DoNothingB/base-control/tools/research-gate.sh --seed 5713427460325524559 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC1DoNothingB/v2/base-s5713427460325524559.json
timeout --signal=TERM --kill-after=10s 850s prlimit --nproc=8000 --as=4294967296 --fsize=1048576 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count-v2.py --gate /fast/scratch/hyaku/chousa-r32/w1/CtlC1DoNothingB/base-control/tools/research-gate.sh --seed 5847843539014860249 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC1DoNothingB/v2/base-s5847843539014860249.json
```

`v2/commands-rescore.json` preserves exact argv, environment, exit codes and output. Earlier fresh seeds 3259841842352555657 and 9047423445119930674, under `--nproc=2000`, exited **2**, respectively reporting trial 13 and 17 `BlockingIOError(11, 'Resource temporarily unavailable')`; neither produced a receipt or count. They are harness errors, not scored misses (`v2/commands.json`). A host snapshot found 1811 same-UID tasks (`v2/resource-failure.json`); [INFERENCE] the 2000-task limit lacked headroom for the concurrent strace/writer bursts. After that diagnosis, the bounded limit was raised to 8000 and two different fresh seeds were used. Memory, file-size and time caps were unchanged.

`timeout 20s strace --version` reported existing strace 7.2; no install. `timeout 20s df -h /fast` reported 231G available. `v2/bounds.json` records successful bounded `stat` (exit 0), gate 306617 bytes, each receipt 4604 bytes, and no surviving process with this seat's exact `C1_TMP`.

**Review conclusion:** v2 rejects this do-nothing control; no false pass was observed. [INFERENCE] The smallest implementation correction remains exclusive flock on the opened manifest, held across both last-byte probe and append. This rescore supplies no conclusion about other controls, candidate implementations, C2, or no-harm checks.
