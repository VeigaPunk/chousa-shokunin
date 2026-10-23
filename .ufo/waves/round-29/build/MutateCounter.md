# Counter mutation probe — historical design v2

**Axes:** operability, counter sensitivity, repeatability, isolation, wall time.

**Result:** 7 killed, 0 surviving, 0 inconclusive under the local detectors below. All 7 pristine detectors and all 7 restored detectors passed. These are historical scratch experiments, **not live C1 measurements and not evidence for the replacement design**. The stop order arrived after the probes finished; no counter or fixture execution followed it.

## Method and limits

Cloned the lane into `/fast/scratch/hyaku/chousa-r29/w1/MutateCounter/` with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 90s git clone --no-hardlinks -- /home/vgpnk/Projects/shokunin/chousa-shokunin /fast/scratch/hyaku/chousa-r29/w1/MutateCounter` (exit 0). Only the scratch counter was mutated, one change at a time, then restored before the next probe. The production counter, frozen fixture and claim were not edited.

The scratch harness `.mutation-probes/probe.py` executes the counter's actual `main()` and its real candidate subprocess. It replaces `page_cases` with the 48 recorded page cases from `.ufo/waves/round-29/controls/before-do-nothing-v2.json`, copied to `MutateCounter/page-replay.json`, and supplies deterministic entropy from `random.Random(2901001)`. The variant seed is 2901. The fixture-derived variants, serialization, output parsing, scoring, receipts and frozen total guard otherwise execute normally. No network requests were made. This does not test live fetching, page sampling or entropy quality.

Replay input SHA-256: `0567c0c9e7e66124bcfdaac309797a40a60ab563e1840a1640c889243a22d9de`; replay artifact SHA-256: `9ee43d420ac7427a8449b94bdb8ad1490fadc3384c7a34d90894ccffae674aff`.

## Actual outputs and expected detectors

Scores below are the actual `QUOTE_REOPEN_MATCH=` suffixes, in **pristine → mutated → restored** order. Counter exit codes use the same order. Each detector requires the pristine control behavior, so its exit codes were **0 → 1 → 0** for every row; the middle 1 is the killed mutant, not a baseline failure. Every candidate subprocess exited 0.

| Mutant, original line | Cheap control / expected detector | Actual score sequence | Counter exits | Verdict |
|---|---|---|---|---|
| 1: omit subspan append, 213–214 | Always `ABSENT`; require 130 cases, 14 subspans and 72 matches | 72/130 → 72/116 → 72/130 | 1 → 1 → 1 | killed |
| 2: omit fixture-transposition append, 218–219 | Always `ABSENT`; require 130 cases, 14 fixture transpositions and 72 matches | 72/130 → 58/116 → 72/130 | 1 → 1 → 1 | killed |
| 3: reuse original ids for the 40 frozen items, 226; variants retain fresh ids | Fixture-id label lookup, `ABSENT` fallback; require no exposed fixture ids and 72 matches | 72/130 → 92/130 → 72/130 | 1 → 1 → 1 | killed |
| 4: omit shuffle, 231 | Position-keyed label sequence for this fixed replay; require fewer than 130 matches | 57/130 → 130/130 → 57/130 | 1 → 0 → 1 | killed |
| 5: count `<missing>` as matching, 280 | Print nothing; require 0 matches | 0/130 → 130/130 → 0/130 | 1 → 0 → 1 | killed |
| 6: case-fold verdict and label, 280 | Always lowercase `absent`; require 0 matches | 0/130 → 72/130 → 0/130 | 1 → 1 → 1 | killed |
| 7: last duplicated verdict wins, 274 | Print each id twice: `ABSENT`, then `VERBATIM`; require first-result semantics and 72 matches | 72/130 → 52/130 → 72/130 | 1 → 1 → 1 | killed |

For mutants 1 and 2, the changed denominator distinguishes the outcomes even though neither counter exit becomes successful; the 130-item guard remains intact. Mutant 3 exposes exactly 40 fixture ids. Only mutants 4 and 5 produce a local false pass. The position control uses the recorded page-label order and is not evidence of a shortcut against live sampling. No conclusion about the new design follows from these experiments.

## Commands, times and artifacts

All probes ran synchronously from the scratch root. Actual command forms were:

```text
timeout 60s prlimit --as=536870912 --nproc=4096 --cpu=40 -- python3 .mutation-probes/probe.py --mutant all --phase pristine
timeout 60s prlimit --as=536870912 --nproc=4096 --cpu=40 -- python3 .mutation-probes/probe.py --mutant 1 --phase mutated
timeout 60s prlimit --as=536870912 --nproc=4096 --cpu=40 -- python3 .mutation-probes/probe.py --mutant 1 --phase restored
```

The first command exited 0. The latter two commands were each run separately for every number from 1 through 7, with exits 1 and 0 respectively. The candidate timeout was 5 seconds. Do not rerun these while the stop order is active. Per-run rendered arguments are in the result files; their `counter_command` field describes arguments supplied to the imported `main()`, not a separately executed live CLI measurement.

All receipt timestamps are on 2026-10-23 UTC. All pristine receipts: `01:25:59Z`. Mutated receipts, in numeric order: `01:26:09Z`, `01:26:24Z`, `01:26:42Z`, `01:26:54Z`, `01:27:12Z`, `01:27:23Z`, `01:27:35Z`. Restored receipts: `01:26:17Z`, `01:26:31Z`, `01:26:48Z`, `01:26:59Z`, `01:27:18Z`, `01:27:29Z`, `01:27:45Z`. Harness-measured duration per probe: 0.0273–0.0503 seconds; first-to-last receipt interval: 106 seconds.

Evidence is under `.ufo/waves/round-29/build/MutateCounter/`: for each number and phase (`pristine`, `mutated`, `restored`), `<number>-<phase>.stdout.txt`, `.stderr.txt`, `.receipt.json` and `.result.json` contain actual output, labels, verdicts, exits, arguments and hashes. `mutations.json` records exact independent edits and their hashes. Scratch controls: `.mutation-probes/control.py`.

## Byte restoration

Pristine and every restored counter SHA-256: `574ffcad7a78d2fdf04b895445c1aac72537cc548b944cae62012baf4ba4e2dd`. Read-only `git show 12244431d636bfa615d7e8d3a0a48b85b3cba06f:corpus/evidence/round29/c1-count.py | sha256sum`, bounded by 15-second timeouts, produced that same digest (exit 0). A final bounded `sha256sum` of the production and restored scratch counters also produced that digest for both (exit 0, before the stop order). Every restored detector recorded it independently.

| Mutant | Mutated counter SHA-256 |
|---|---|
| 1 | `7629efe3022ae394828b5fa3224b3eead8355e3ea5f8cdec4ae80328224ec628` |
| 2 | `43601267f87754416afb1cdda40d14dd2b68352aaf4970bb15a086bb5281db43` |
| 3 | `d6e6a3106a8ce70ad85cf56bc7270695e1f40cecd8d55db836fe114ab6754260` |
| 4 | `cfb3d92a5382ed95e3a88aa5be9927a0f77ddd09e790b0899dfb65be0318d8cc` |
| 5 | `b2e0e2cae69e91c3bc0db62bca44a434868d11ce22105f77d79f4738820cc028` |
| 6 | `1babf4f8e001b64d87251ba97951c51df304a69aaf93803de6d0d876b50474a4` |
| 7 | `4ee1635666a6ad69ec50193c3952065936dd990d98345bac0c376f6aaf5de3a4` |

Harness SHA-256: `6707199ada6fecbc26a8fb396da5ab7321cad7a986eff7c3e8c06d4996c8a68f`; control SHA-256: `786297dd19d8fc77133c226a593f2f8bef7e5ae967713a2efa98c4f9c96bed0a`. No tools were installed or updated. No background jobs were started; all subprocesses exited. No source page was opened and no new located quote is asserted.
