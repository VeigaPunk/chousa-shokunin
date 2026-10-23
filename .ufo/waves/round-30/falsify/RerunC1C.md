VERDICT: holds — C1 counter printed QUOTE_REOPEN_HEADLESS_MATCH=106/106 with exit 0 on 3 of 3 runs, each with a fresh seed, on the landed tool.

## Hashes (verified before scoring)

`sha256sum` run from the lane root at tip `a9d3a05a8fd812a60323b08381019152069581fd` (`git rev-parse HEAD`):

| file | SHA-256 | frozen value |
|---|---|---|
| corpus/evidence/round30/c1-count.py | 5b312d84365924779ba8e6fe447cad3467f59c11848083d0967528c7a5e9d6e6 | match |
| corpus/evidence/round30/c2-count.py | 0a59e3736fed8ef4cf7b00a75955eccfd0336c8a0ca84bee23402408b727f88f | match |
| corpus/evidence/round30/qr_harness.py | e2be0dd16da5b2bf03430772831763e56c6ff6dd6a44063bb05c909b284f50d4 | match |
| tools/quote-reopen.py | 47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201 | match |

## Runs

Command (from the lane root, `ulimit -v 4000000`):
`timeout 300 python3 corpus/evidence/round30/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-30/falsify/RerunC1C/run<i>.json`

| run | printed line | exit | seed | tool_sha256 | predicate_holds | wall_s |
|---|---|---|---|---|---|---|
| 1 | QUOTE_REOPEN_HEADLESS_MATCH=106/106 | 0 | 6480751607110391343 | 47a657e7…1201 | true | 0.047 |
| 2 | QUOTE_REOPEN_HEADLESS_MATCH=106/106 | 0 | 2558078681949341811 | 47a657e7…1201 | true | 0.049 |
| 3 | QUOTE_REOPEN_HEADLESS_MATCH=106/106 | 0 | 1394360516317001804 | 47a657e7…1201 | true | 0.051 |

Every receipt also records `counter_sha256` 5b312d84…9d6e6, `harness_sha256` e2be0dd1…50d4,
`n`=`t`=`frozen_total`=106, `tool_killed` false, `tool_rc` 1 and `net_connect_events` 21.
The 3 seeds are different. Receipts: `RerunC1C/run{1,2,3}.json` (SHA-256 12cfcf9d…2320,
39bec4ac…4b98, ff61eb21…75ac) and their stdout in `RerunC1C/run{1,2,3}.out`.

## Failed measurement (not scored)

My first set of 3 runs also used `ulimit -u 2000`. That limit counts every process this
user has on the host, so `H.Server()` hit `RuntimeError: can't start new thread`
(`qr_harness.py:154`) before scoring any item. The cause was my cap, not the tool or the
counter, and no receipt was written. I re-ran without that cap, keeping only the memory cap.
The logs are at `/fast/scratch/hyaku/chousa-r30/w2/RerunC1C/run{1,2,3}-ulimit-u2000.out`.

## Residual risk

- [INFERENCE] `net_connect_events` 21 counts the harness's loopback connects. The counter
  fetches nothing from the network, so this run says nothing about reaching the real network.
- This seat only measured C1. C2, the mutants and the sources are outside its scope.

No tools were installed or updated.
