# MutC1CounterB — design v2 re-score

Axes: operability, coverage. Read `corpus/evidence/round32/claims.md:119-189` and the v2 counter docstring. Re-scored **every gate built previously**: ten final wrong controls, both retained initial controls, and the feasibility-only oracle. **26/26 invocations completed with receipts; nothing assigned remains NOT RUN.** No candidate or mutated counter was scored.

The exact committed `3d586d3a` counter was invoked from the lane root:

`corpus/evidence/round32/c1-count-v2.py`, SHA-256 **`e6bf95313ad603ff75e03bb64fbe5a2689a9dfe9bc4c0715a21012383508d891`**.

Read-only `timeout 20s git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 3d586d3a:corpus/evidence/round32/c1-count-v2.py` exited 0; its bytes exactly matched the invoked file. Before/after counter hashes match. No counter was edited. Existing strace version: **7.2**; no installs/updates.

## Results

Counts are `APPEND_SERIALIZED=k/24` in seed order. Every wrong control **MISSES** on both seeds; only the declared feasibility oracle **MEETS-TARGET**. That oracle is not an adversarial control or candidate.

| Gate/control | SHA-256 | Fresh seeds | Counts | Exit codes | Verdict |
|---|---|---|---|---|---|
| hold | `971cdda669e04589ab8c2d40ec43d445f1dc31c1d9454ec6bd95ca17e14ae877` | 322500, 322501 | 12/24, 12/24 | 1, 1 | MISSES |
| waiter | `62d9b76cc5326bd92ad1670f066e73ff1d6319b0e21ef5f89afdf0f76161fead` | 322502, 322503 | 12/24, 12/24 | 1, 1 | MISSES |
| writer-rc | `d2aeebf79ed21a081c94f26d87dcd04e9d911ffb3470ed920d4b66d3f2aaa4ac` | 322504, 322505 | 0/24, 0/24 | 1, 1 | MISSES |
| inode | `5096cf85d9ce5defa887b9612f743e2d99c9a2d48e9b80c542c139a62f00a13c` | 322506, 322507 | 0/24, 0/24 | 1, 1 | MISSES |
| seed-prefix | `1b3cf2838cf08c38c83f225749279bdd784ea436e3768c53b170b12929b8c5df` | 322508, 322509 | 0/24, 0/24 | 1, 1 | MISSES |
| line-count | `daf9cd007034782f52d59fdda2be5747c3ac90f9d2e77a2eb5ca3ad449d775d3` | 322510, 322511 | 0/24, 0/24 | 1, 1 | MISSES |
| blank-line | `016bca0b7fe5ebb8e41d601ce4a607083c642e00eef44c1a905dba52c41022b2` | 322512, 322513 | 0/24, 0/24 | 1, 1 | MISSES |
| json-object | `e712c76c57232889f06d9564e329bdf806de19b2bcb65d31c75ed1ce6658d7b7` | 322514, 322515 | 0/24, 0/24 | 1, 1 | MISSES |
| schema | `719064c352762edd6a1dde1b75d771a14f57b8bd332edee76e853381765209b0` | 322516, 322517 | 0/24, 0/24 | 1, 1 | MISSES |
| final-newline | `cf1f234e2dff7832000d5563a6e0a1c3145597f57eb178b72149bf6faf105644` | 322518, 322519 | 0/24, 0/24 | 1, 1 | MISSES |
| hold-initial | `dfbb56686ce7cd9363487d70c1eb04ad932ed3ff22a305b0941f97c3f71881b0` | 322520, 322521 | 12/24, 12/24 | 1, 1 | MISSES |
| inode-initial | `25114e4695f7b7c64892435f071954f51c187ac17250b4b8a5564c7e7f6797ec` | 322522, 322523 | 0/24, 1/24 | 1, 1 | MISSES |
| oracle, feasibility only | `b00c40d4d6be9dd9296481d5848ba5d4693029d9b9a5cde2cba6bcb600b62597` | 322524, 322525 | 24/24, 24/24 | 0, 0 | MEETS-TARGET |

For hold, waiter, and hold-initial, class counts were F_unterminated 12/12 and every L class 0/4. Other wrong controls had all classes zero except inode-initial seed 322523: F_unterminated 1/12, every L class 0/4. Oracle classes were F_unterminated 12/12 and every L class 4/4. Full per-trial failure lines are retained below.

## Layout, commands, and receipts

`S=/fast/scratch/hyaku/chousa-r32/w1/MutC1CounterB`; `A=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/MutC1CounterB`.

Every control was copied without byte changes to **`$S/v2-<control>/tools/research-gate.sh`**. Its lane root excludes the fixture temp parent `$S/v2-fixtures`. All thirteen copied gate hashes were checked before scoring and differ from BASE `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`; all remained unchanged after scoring.

Actual invocation pattern, cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`:

```sh
C1_TMP="$S/v2-fixtures" C2_TMP="$S/v2-fixtures" TMPDIR="$S/v2-fixtures" \
  PYTHONDONTWRITEBYTECODE=1 timeout --kill-after=5s 900s \
  prlimit --nproc=16384 --as=4294967296 -- \
  python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count-v2.py \
  --gate "$S/v2-<control>/tools/research-gate.sh" --seed <seed> \
  --receipt "$A/v2/<control>-s<seed>.json"
```

At most four finite invocations ran concurrently; all were awaited. Each receipt is **`v2/<control>-s<seed>.json`**, with its exact argv, environment, exit code, stdout, stderr, and elapsed time in **`v2/<control>-s<seed>.run.json`**.

Evidence relative to this supplement:

- `v2/provenance.json`: committed counter comparison, all gate paths/hashes/seeds, and fixture isolation.
- `v2/summary.json`: all 26 counts, class counts, exit codes, verdicts, and receipt paths.
- `v2/trial-lines.txt`: actual class and per-trial lines for every run; **46885 bytes**, SHA-256 **`f56b833208c5fa584ff5bfe97a0d76a1ee2022463c295e44a8d2ffbf6ceec92e`**.
- `v2/after-hashes.json`: unchanged counter and all thirteen unchanged gate hashes.

Before expanding fixtures, `timeout 20s df -h /fast` exited 0 with 231 GiB available. Final `timeout 20s pgrep -af '(^|[[:space:]])(python3|bash|strace|flock)[[:space:]].*/fast/scratch/hyaku/chousa-r32/w1/MutC1CounterB/'` exited **1**, empty output: no matching own probe process remained. No network, candidate, C2 re-score, production change, or additional counter mutation was performed.
