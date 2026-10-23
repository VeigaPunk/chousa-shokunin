# CtlC1AllFalseB — design-v2 re-score

Axes: **operability**, and **coverage** of the four assigned C1 negative controls. Read `corpus/evidence/round32/claims.md:119-189` and the v2 counter before re-scoring. Target remains `APPEND_SERIALIZED=24/24` (`claims.md:150-154`). **All four controls MISSES on both fresh seeds; no control meets target.**

## Provenance and isolation

Frozen counter: `corpus/evidence/round32/c1-count-v2.py`, SHA-256 `e6bf95313ad603ff75e03bb64fbe5a2689a9dfe9bc4c0715a21012383508d891`. Both `timeout 30 sha256sum <counter>` and `timeout 30 git show 3d586d3a:corpus/evidence/round32/c1-count-v2.py | timeout 30 sha256sum` returned this hash, exit 0; all eight receipts record it.

Scratch prefix `S=/fast/scratch/hyaku/chousa-r32/w1/CtlC1AllFalseB`. Each retained v1 mutant was still mutated, then copied unchanged to `$S/<control>/tools/research-gate.sh` using bounded `mkdir`/`cp` commands (exit 0). `timeout 30 sha256sum` on all four relocated gates (exit 0) returned the hashes below; none equals BASE `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`. Set `C1_TMP=C2_TMP=TMPDIR=$S/v2-tmp`, a sibling outside every control's lane root. No counter or production file was edited, and no candidate was scored.

## Scores

Each seed has its own receipt at `v2/<control>-s<seed>.json`. Every run exited **1**, had solo `ref_rc=0`, and recorded `predicate_holds=false`.

| Control | Gate SHA-256 | Fresh seeds (in count order) | APPEND_SERIALIZED | Verdict |
|---|---|---|---|---|
| no-append | `7e98299ae624a258fd370fc94f5115c60224c7a533d8b195ceee88a4a43e8e2a` | 1571745372, 3031817921 | 0/24, 0/24 | MISSES |
| junk-line | `6c2053e16366bff23289de4c221f6661eee21034092648a661f16175474aa4bd` | 2660296547, 3208011672 | 0/24, 0/24 | MISSES |
| always-newline | `61e2e1122c0dbfa2caf1d01bec3ce7c6dd110da14853cf7cce6b3759e87692d6` | 4091295572, 668434059 | 0/24, 0/24 | MISSES |
| rewrite-rename, exclusive flock retained through rename | `1623967376676c6c490acc170d08d0094da1c8aeec931030b92d2a96e3f689c0` | 2712189448, 3169471396 | 0/24, 0/24 | MISSES |

Every completed stdout reported:

```text
APPEND_SERIALIZED=0/24
  F_unterminated 0/12
  L_empty 0/4
  L_terminated 0/4
  L_unterminated 0/4
```

Exact expanded commands, environment, exits and stdout/stderr: [v2/run-log.json](v2/run-log.json). Full per-trial failure lines derived from the eight receipts: [v2/trial-lines.txt](v2/trial-lines.txt). Receipt links: [no-append 1571745372](v2/no-append-s1571745372.json), [3031817921](v2/no-append-s3031817921.json); [junk-line 2660296547](v2/junk-line-s2660296547.json), [3208011672](v2/junk-line-s3208011672.json); [always-newline 4091295572](v2/always-newline-s4091295572.json), [668434059](v2/always-newline-s668434059.json); [rewrite-rename 2712189448](v2/rewrite-rename-s2712189448.json), [3169471396](v2/rewrite-rename-s3169471396.json).

Execution shape, cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`, with the temp environment above and `PYTHONDONTWRITEBYTECODE=1`:

```sh
timeout --signal=INT --kill-after=15 400 prlimit --nproc=8192 --as=4294967296 \
  python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count-v2.py \
  --gate "$S/<control>/tools/research-gate.sh" --seed <seed> \
  --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC1AllFalseB/v2/<control>-s<seed>.json
```

Four controls ran concurrently, two seeds per control. Existing `strace --version` reported 7.2; no install was needed. All receipt delay self-checks passed (0.303-0.309 s; `delay_us=300000`). No writer-rc, writer-deadline or lock-deadline failures appear in the eight receipt arrays.

## Counterexamples and limits

No-append fails all trials for absent gate lines and absent final newline. Junk and blind-newline controls fail all L trials for writing under the cooperating lock; their F trials have blank/invalid JSON lines. Rename remains the strongest identity counterexample: all L trials fail `inode-changed`, while all F trials lose receipt lines (9-15 of 16). Holding the original inode's flock does not preserve the manifest pathname's inode. Smallest safe behavior correction remains append-only writing on the locked manifest descriptor, with delimiter probe and append both inside the lock; no counter correction is suggested by these four re-scores.

`timeout 30 df -h /fast` returned 231G available before the copies. Final bounded `pgrep -af` for the four relocated gate paths exited 1 with no output: no matching control processes remained. Scoped receipts and logs are below 1 MiB each. No C2 runs, candidates, network, installs, production edits, counter edits, git/jj writes, or canonical admission/judgment. These negative controls do not prove complete C1 coverage.
