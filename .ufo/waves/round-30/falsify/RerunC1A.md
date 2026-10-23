VERDICT: holds — C1 counter printed QUOTE_REOPEN_HEADLESS_MATCH=106/106, exit 0, in 3 of 3 fresh-seed runs on the landed tool at tip a9d3a05a.

## Frozen hashes (sha256sum, run from lane root, exit 0)

- `corpus/evidence/round30/c1-count.py` 5b312d84365924779ba8e6fe447cad3467f59c11848083d0967528c7a5e9d6e6 (matches)
- `corpus/evidence/round30/c2-count.py` 0a59e3736fed8ef4cf7b00a75955eccfd0336c8a0ca84bee23402408b727f88f (matches)
- `corpus/evidence/round30/qr_harness.py` e2be0dd16da5b2bf03430772831763e56c6ff6dd6a44063bb05c909b284f50d4 (matches)
- `tools/quote-reopen.py` 47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201 (matches the landed value)
- `git rev-parse HEAD` a9d3a05a8fd812a60323b08381019152069581fd

## Runs

Command per run (i = 1, 2, 3, run one after another):
`( ulimit -v 4000000; ulimit -u 20000; timeout 300 python3 corpus/evidence/round30/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-30/falsify/RerunC1A/run$i.json )`

| run | printed line | exit | seed | tool_sha256 | predicate_holds |
|---|---|---|---|---|---|
| 1 | QUOTE_REOPEN_HEADLESS_MATCH=106/106 | 0 | 488789735826612895 | 47a657e7…1201 | true |
| 2 | QUOTE_REOPEN_HEADLESS_MATCH=106/106 | 0 | 6597524862147521180 | 47a657e7…1201 | true |
| 3 | QUOTE_REOPEN_HEADLESS_MATCH=106/106 | 0 | 5553904054915123200 | 47a657e7…1201 | true |

Every receipt has `counter_sha256` and `harness_sha256` equal to the frozen values, `misses_first40: []`, every `by_class` cell full (for example `headless-body/body-window` 10/10, `headless-text/body-window` 8/8), `tool_killed: false`, `wall_s` about 0.05, `net_connect_events: 21` (counted by the harness, which serves only loopback), and `tool_rc: 1`. [INFERENCE] `tool_rc: 1` is the tool's own exit code when some verdicts are not VERBATIM. The 106 items carry ABSENT, TOO_LONG, NO_SOURCE and UNREACHABLE labels, and the counter does not score the code.

## Measurement note

The first attempt used `ulimit -u 2000`. The three runs exited 1 with `RuntimeError: can't start new thread` at `qr_harness.py:154` (`Server()` thread start), before any item was scored. That cap counts every process of this host user, and many other agents were running, so this was my own cap failing, not a tool or counter result. No receipts were written. The rerun with `ulimit -u 20000` is the measurement above.

Receipts: `.ufo/waves/round-30/falsify/RerunC1A/run{1,2,3}.json`. No tools installed or updated. No network used. No process left running (`pgrep -f c1-count.py` found none).
