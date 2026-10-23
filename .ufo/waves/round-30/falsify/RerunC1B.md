VERDICT: holds — C1 counter printed QUOTE_REOPEN_HEADLESS_MATCH=106/106, exit 0, in 3 of 3 scored runs on the landed tool

Lane tip `a9d3a05a8fd812a60323b08381019152069581fd` (`git rev-parse HEAD`, read-only).

## Hashes (`sha256sum`, exit 0) — all equal the frozen values
- `corpus/evidence/round30/c1-count.py` 5b312d84365924779ba8e6fe447cad3467f59c11848083d0967528c7a5e9d6e6
- `corpus/evidence/round30/c2-count.py` 0a59e3736fed8ef4cf7b00a75955eccfd0336c8a0ca84bee23402408b727f88f
- `corpus/evidence/round30/qr_harness.py` e2be0dd16da5b2bf03430772831763e56c6ff6dd6a44063bb05c909b284f50d4
- `tools/quote-reopen.py` 47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201

## Runs
Command, from the lane root:
`bash -c "ulimit -v 16000000; ulimit -u 60000; timeout 300 python3 corpus/evidence/round30/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-30/falsify/RerunC1B/run$i.json"`

| run | stdout | exit | seed | tool_sha256 | utc |
|---|---|---|---|---|---|
| 1 | QUOTE_REOPEN_HEADLESS_MATCH=106/106 | 0 | 12387048102743538144 | 47a657e7…1201 | 2026-10-23T03:35:01Z |
| 2 | QUOTE_REOPEN_HEADLESS_MATCH=106/106 | 0 | 15530321693159665075 | 47a657e7…1201 | 2026-10-23T03:35:02Z |
| 3 | QUOTE_REOPEN_HEADLESS_MATCH=106/106 | 0 | 463077083262045314 | 47a657e7…1201 | 2026-10-23T03:35:02Z |

In every receipt: `predicate_holds: true`, `n = t = frozen_total = 106`, `misses_first40: []`,
every `by_class` entry full (for example headless-text/body-window 8/8, headless-body/body-window
10/10, headless-nobody/body-window 10/10), `tool_killed: false`, `counter_sha256` and
`harness_sha256` equal the frozen values, stderr empty. The 3 seeds differ from each other.
`tool_rc: 1` in all 3 is the candidate's own exit code; the counter scores verdicts, not that code.

## Aborted attempts (not scored, kept)
My first 3 attempts ran under `ulimit -v 4000000; ulimit -u 2000`. Each died in
`qr_harness.py:154` `Server().__init__` with `RuntimeError: can't start new thread` before
any item was scored, and wrote no receipt. The traceback is in `RerunC1B/aborted-capped-run{1,2,3}.stderr`.
The cause was my own caps: `-u` counts every process the user runs on this host.
[INFERENCE] These are harness failures under the claim's kill rule, not misses. The 3 scored
runs above replace them.

## Residual risk
Each run takes about 0.05 s of tool wall time (`wall_s` 0.048 to 0.051), and every page is
served from loopback. The counter makes no network claim. No counter processes were left over
(`pgrep -af 'python3 corpus/evidence/round30/c1-count'` found none). No tools installed or updated.

Artifacts: `.ufo/waves/round-30/falsify/RerunC1B/run{1,2,3}.json`, `run{1,2,3}.stdout`,
`run{1,2,3}.stderr` (empty), `aborted-capped-run{1,2,3}.stderr`.
