VERDICT: holds — C2 counter printed QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27, exit 0, in 5 of 5 fresh-seed runs on the landed tool

## Hash check (before scoring)
`sha256sum` from the lane root at `git rev-parse HEAD` = a9d3a05a8fd812a60323b08381019152069581fd:
- c2-count.py 0a59e3736fed8ef4cf7b00a75955eccfd0336c8a0ca84bee23402408b727f88f (frozen, match)
- c1-count.py 5b312d84365924779ba8e6fe447cad3467f59c11848083d0967528c7a5e9d6e6 (frozen, match)
- qr_harness.py e2be0dd16da5b2bf03430772831763e56c6ff6dd6a44063bb05c909b284f50d4 (frozen, match)
- tools/quote-reopen.py 47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201 (landed, match)
Every receipt repeats the same counter, harness and tool SHA-256.

## Runs
Command: `timeout 300 python3 corpus/evidence/round30/c2-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-30/falsify/RerunC2A/run{N}.json`, run one after another, about 6-7 s each.

| N | line | exit | seed | killed | unvalidated dests | tightest item (kind, wall_s / bound_s) |
|---|---|---|---|---|---|---|
| 1 | QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27 | 0 | 10663666237924183162 | 0 | 0 | drip-steady 2.327 / 3.76 |
| 2 | QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27 | 0 | 1259139663601668267 | 0 | 0 | drip-body 4.843 / 6.27 |
| 3 | QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27 | 0 | 13113785594144604319 | 0 | 0 | drip-steady 5.021 / 6.45 |
| 4 | QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27 | 0 | 3940947623884200138 | 0 | 0 | drip-steady 4.731 / 6.16 |
| 5 | QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27 | 0 | 8341740830682759523 | 0 | 0 | drip-steady 2.433 / 3.85 |

No item failed to match, so there is no miss to report by kind, label, got, wall_s or bound_s. `predicate_holds` is true in all 5 receipts. The largest overshoot of any item past its own DEADLINE was 0.067-0.083 s per run, well inside SLACK 1.5 s. The tightest margin to the bound was 1.417 s.

## Notes
- Receipts carry `design: "v3"` although claims.md describes design v4. That matches claims.md line 163, which fixes the receipt field as `design: "v3"`. The counter hash is the frozen v4 hash.
- Sibling seats were running C2 counters and mutants on the same host at the same time (RerunC2B, MutTruncAsFull, seen with `pgrep`), so these 5 runs were under shared CPU load and still held. [INFERENCE] The margin under load suggests the pass does not depend on an idle host.
- Raw outputs: `.ufo/waves/round-30/falsify/RerunC2A/run{1..5}.{json,out}`. No network fetch, no tool installs, no files changed outside the seat directory and this report. None of my processes were left running.
