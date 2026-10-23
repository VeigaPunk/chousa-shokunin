# C1 partial-lock controls — frozen design v2 re-score

Axes: operability and detector coverage. Read `corpus/evidence/round32/claims.md:119-189` and the frozen `c1-count-v2.py` contract. **All four controls MISSES: 0/24 on both fresh seeds each.** The v1 probe-only survivor no longer meets the v2 target of 24/24. No candidate or oracle was scored by this seat.

## Frozen inputs and layout

The current counter and `git show 3d586d3a:corpus/evidence/round32/c1-count-v2.py` both hashed to:

`e6bf95313ad603ff75e03bb64fbe5a2689a9dfe9bc4c0715a21012383508d891`

Rebuilt the exact four previously tested mutant byte strings from pristine BASE, using the original minimal edits (preserved in the sibling `*.patch` files). Each mutant hash below differs from BASE:

`0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`

Scratch gates were placed at `/fast/scratch/hyaku/chousa-r32/w1/CtlC1PartialLockB/v2/<control>/tools/research-gate.sh`. C1_TMP, C2_TMP and TMPDIR were all `/fast/scratch/hyaku/chousa-r32/w1/CtlC1PartialLockB/v2/tmp`, outside every gate's lane root. Every scored mutant receipt confirms its rebuilt hash.

## Scores

All receipts/logs below are in `.ufo/waves/round-32/w1/CtlC1PartialLockB/v2/`. Each seed has a receipt named `mutated-<control>-s<seed>.json` and a matching `.txt` containing its actual command, exit and stdout/stderr.

| Control | Mutated gate SHA-256 | Fresh seeds | APPEND_SERIALIZED | Verdict |
|---|---|---|---|---|
| `a-append-only` — probe before EX; append under EX | `4a39b99728ec559f9d3d0c4140be410dec457f69c65a5a7184bbbcc144cae1ca` | 32472011, 32472012 | 0/24, 0/24 | MISSES |
| `b-probe-only` — EX around probe, unlock before append | `034f786be1570136b27d72ec630e24be1c6a673ce53434d476af94f4bb5f0340` | 32472021, 32472022 | 0/24, 0/24 | MISSES |
| `c-cached-probe` — cache before verification; later EX uses stale delimiter | `59ea2a22bc7293715b15eae245046bab71ad541b641fedad4e62169181f9949c` | 32472031, 32472032 | 0/24, 0/24 | MISSES |
| `d-shared-lock` — SH around probe and append | `76c4c073bb5990a220e9adf69acc674b907ecc1579d27588954d6652b40c0b78` | 32472041, 32472042 | 0/24, 0/24 | MISSES |

Every mutant run exited **1**, printed `F_unterminated 0/12`, `L_empty 0/4`, `L_terminated 0/4`, `L_unterminated 0/4`, and emitted a complete v2 receipt. `v2/runs-and-trials.txt` retains all actual command/output records plus every per-trial receipt field. Counter bytes were never edited. The frozen 300,000 µs write delay/startup self-check is recorded in the receipts; the pre-registered v2 change is described at `claims.md:145-154`.

Commands ran from `/home/vgpnk/Projects/shokunin/chousa-shokunin`, bounded by `timeout 840s prlimit --nproc=8192 --as=4294967296`, with the environment paths above, invoking the committed `python3 corpus/evidence/round32/c1-count-v2.py --gate <isolated-gate> --seed <seed> --receipt <receipt>`. At most two counters ran concurrently, awaited in the foreground; exact expanded commands are in each `.txt`.

## Pristine/restored evidence and limits

Pristine BASE scored **0/24** on fresh seeds 32472001 and 32472002, exit 1 (`v2/pristine-pristine-s32472001.json`, `...32472002.json`). After the eight mutant runs, restored all four gate paths to exact pristine bytes; four bounded `cmp` calls exited 0 and explicit `sha256sum` returned BASE's hash for every path (`v2/restoration.txt`). Ran the same v2 detector on each restored path with seed 32472001: **0/24**, exit 1 each (`v2/restored-<control>-s32472001.json`). Thus **no killed-mutant attribution is claimed: pristine is red, so strict mutation attribution is INCONCLUSIVE**. The requested control verdicts above are measured MISSES.

A final bounded process sweep found no matching scratch gate/counter/strace process (`v2/process-completion.txt`, pgrep exit 1, no output). Existing strace was version 7.2; nothing was installed. Initial disk check showed 231G available. An initial wildcard hash listing printed all four expected mutant hashes but exited 1 on a nonexistent `tmp/tools` path; this tool behavior was reported, and completed receipts independently confirm every scored mutant hash. No scored counter invocation failed its harness.

No network, candidate scoring, counter edits, production edits, Git/jj writes, subagent dispatch or background jobs. The original v1 report was not rewritten. All scratch gates are restored; retained v2 receipts/logs and this supplement remain only under this seat's artifact directory. The full per-trial appendix is 41,966 bytes; every retained artifact is below 1 MiB.
