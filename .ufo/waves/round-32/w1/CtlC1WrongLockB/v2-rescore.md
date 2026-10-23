# C1 wrong-lock controls — design v2 re-score

**Axes:** operability; counter coverage of wrong lock object/family/protocol. **Result: all four controls MISSES on two completed fresh-seed runs each; no MEETS-TARGET escape.** Target is 24/24 (`corpus/evidence/round32/claims.md:143-154`). No candidate was scored and no counter was edited.

## Frozen counter and isolated layout

Read Design v2 (`claims.md:119-189`) and `c1-count-v2.py:1-175`. From lane cwd, this read-only provenance command exited 0:

```text
timeout 20 git show 3d586d3a:corpus/evidence/round32/c1-count-v2.py | timeout 20 sha256sum
e6bf95313ad603ff75e03bb64fbe5a2689a9dfe9bc4c0715a21012383508d891  -
```

The working counter and all eight completed receipts have that same hash. Existing `strace --version` reports 7.2; no installation/update occurred. Each completed receipt records `delay_us=300000`, successful delay self-check 0.302–0.311 seconds, and solo reference exit 0 (`receipt.json:2-11`).

Let **S** = `/fast/scratch/hyaku/chousa-r32/w1/CtlC1WrongLockB/` and **A** = `.ufo/waves/round-32/w1/CtlC1WrongLockB/v2/` relative to the lane. Each gate is now **S**`<control>/tools/research-gate.sh`; `C1_TMP`, `C2_TMP`, and `TMPDIR` are all **S**`v2-tmp`. Thus no gate's lane root contains the fixture temp parent.

The original four mutated gates were preserved, not restored. They were copied unchanged into these isolated paths. `timeout 20 sha256sum` over all four isolated copies exited 0 and produced the hashes below; every hash differs from base `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`. Each receipt independently records its gate hash at line 7.

## Completed scores

| Control / gate subdirectory | Gate SHA-256 | Fresh seeds → APPEND_SERIALIZED | Verdict |
|---|---|---|---|
| `sibling-flock` — flock on PATH.lock | `cddd8cae755620da69c9f61ddc5bd6931de15becd4b2252093266cb1ef7e06c7` | `1164394067745934815` → 12/24; `6942719030958574319` → 12/24 | MISSES |
| `per-process-flock` — flock on PATH.lock.$$ | `f02db76766f29106e967155ee19addec5272cca3c00f0634b98d43c0845db249` | `8813274439468374557` → 0/24; `4497807281718331427` → 0/24 | MISSES |
| `posix-lockf` — Python POSIX lockf on PATH | `bf1b9c06f050d84dc5b2443cc10235ea52ab0accce634f94486c15ac067f2863` | `3931168057388379246` → 12/24; `1611102174911494980` → 12/24 | MISSES |
| `mkdir-spin` — bounded mkdir/rmdir lock | `13f387cf3095804242eb1d869b9dd0b2ddb672472f01f4ed0a201dddf6cba3f7` | `2446386726986300289` → 12/24; `6013957116027521829` → 12/24 | MISSES |

For each table pair, evidence stem is **A**`<control>-s<seed>`:

- `.json:2-21`: frozen receipt, delay check, counter/gate hashes, seed, total, count, predicate and per-class scores.
- `.command.json:4-8`: lane cwd, exact executed command, counter exit code **1**, hashes.
- `.stdout.txt:1-5`: raw count and every per-class output line.
- `.trials.txt:1-24`: every per-trial pass/failure line rendered from the receipt.

All completed runs have `L_empty=0/4`, `L_terminated=0/4`, and `L_unterminated=0/4`. The three common-protocol controls have `F_unterminated=12/12`; per-process flock has `F_unterminated=0/12`. The two per-process receipts' complete failure-name sets contain only `appended-under-cooperating-lock`, `prefix-rewritten`, `blank-line`, and `invalid-json-line`—not writer exit/deadline failures.

## Commands, resource errors, limits

`S/score-control-v2.py` draws fresh `secrets.randbits(63)` seeds and runs the unmodified counter. Four scorer processes were initially executed concurrently and synchronously awaited; each was bounded by `timeout --kill-after=10s 850s`. Inner counter commands, preserved verbatim in each `.command.json:5`, use `timeout --kill-after=10s 400s`, `prlimit --as=2147483648 --fsize=983040`, the required scratch temp variables, the exact v2 counter path, isolated gate path, explicit seed, and receipt under **A**. Initial `--nproc` was 2000.

Three attempts exited **2**, with no receipt or count; they are retained, not treated as predicate misses:

| Evidence stem under A | Raw `.stdout.txt:1` |
|---|---|
| `sibling-flock-s3654444391053792470` | `c1-count: trial 8 harness error: BlockingIOError(11, 'Resource temporarily unavailable')` |
| `posix-lockf-s115068134866061245` | `c1-count: trial 4 harness error: BlockingIOError(11, 'Resource temporarily unavailable')` |
| `posix-lockf-s2301002376000482972` | `c1-count: strace delay self-check failed (took BlockingIOError(11, 'Resource temporarily unavailable'))` |

Only the missing receipt work was repeated, with fresh seeds: one sibling run and two lockf runs. Fanout was reduced to two scorers and the finite process ceiling raised to `--nproc=4096`; all three then completed with exit 1 and the scores above. Neither gate nor counter bytes changed for these retries. Exact failed and completed command lines and exits remain in their `.command.json` files.

The scorer used subreaper cleanup after each attempt; `cleanup_killed` records PIDs sent SIGKILL, without distinguishing live processes from zombies, and cleanup requires no remaining children before return. No background jobs remain. `timeout 20 wc -c` on **A**`*.json` and **A**`*.txt` exited 0: total 63,143 bytes; largest artifact 4,609 bytes. No production files, prior report, Git/jj state, or sibling artifacts were changed. No C2, selftest, candidate, network or canonical judgment was run.

## Counterexample and smallest safe correction

The strongest wrong-lock alternatives still pass every free-writer trial while failing every held-manifest-lock trial; free-writer serialization is not evidence of the required cooperation. V2 additionally drives per-process locking to 0/24 on both completed seeds. These controls do not expose a v2 escape. The safe implementation correction remains exclusive flock on the opened manifest append descriptor, held from before the last-byte probe through append; no counter correction is indicated by these controls.
