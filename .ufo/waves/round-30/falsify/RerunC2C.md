VERDICT: holds — C2 counter printed QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27, exit 0, in 5 of 5 fresh-seed runs on the landed tool

## Target
C2 measurement (operability) on lane tip `a9d3a05a8fd812a60323b08381019152069581fd`, tool `tools/quote-reopen.py`.

## Frozen hashes (verified before scoring)
`sha256sum corpus/evidence/round30/{c1-count.py,c2-count.py,qr_harness.py} tools/quote-reopen.py`, exit 0:
- c1-count.py `5b312d84365924779ba8e6fe447cad3467f59c11848083d0967528c7a5e9d6e6` (matches)
- c2-count.py `0a59e3736fed8ef4cf7b00a75955eccfd0336c8a0ca84bee23402408b727f88f` (matches)
- qr_harness.py `e2be0dd16da5b2bf03430772831763e56c6ff6dd6a44063bb05c909b284f50d4` (matches)
- tools/quote-reopen.py `47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201` (matches the landed tool)
Every receipt also records these counter, harness and tool hashes, and they match.

## Runs
Command, from the lane root, run 5 times one after another (N=1..5), bounded with `prlimit --as=4000000000 --nproc=4000`:
`timeout 300 python3 corpus/evidence/round30/c2-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-30/falsify/RerunC2C/run{N}.json`

| run | line | exit | seed | utc | tightest item (kind, label, got, wall_s, bound_s) |
|---|---|---|---|---|---|
| 1 | QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27 | 0 | 14661333144224252009 | 03:34:46Z | drip-body, UNREACHABLE, UNREACHABLE, 2.533, 3.96 |
| 2 | QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27 | 0 | 14527059432671780261 | 03:34:52Z | drip-head, UNREACHABLE, UNREACHABLE, 3.845, 5.26 |
| 3 | QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27 | 0 | 12338532452282397991 | 03:34:58Z | drip-body, UNREACHABLE, UNREACHABLE, 3.01, 4.44 |
| 4 | QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27 | 0 | 8221803114137297199 | 03:35:09Z | drip-head, UNREACHABLE, UNREACHABLE, 3.818, 5.24 |
| 5 | QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27 | 0 | 11280913907122518467 | 03:35:14Z | drip-body, UNREACHABLE, UNREACHABLE, 2.144, 3.57 |

Non-matching items: none in any run, so there is no kind, label, got, wall_s or bound_s to report for a miss.
The table shows the item closest to its bound in each run. The smallest margin over all 135 items is 1.415 s (run 2). Each tightest item finished about 0.07-0.09 s after its own DEADLINE, inside the 1.5 s slack.

Per receipt (all 5 runs): `predicate_holds: true`, `design: "v3"`, `n = t = frozen_total = 27`, 27 of 27 `match`, 0 `killed`, 0 `unvalidated_dests`, and `validated_only` true for every item.
Each run drew the full item mix: drip-body 3, drip-head 2, drip-steady 2, stall-body 1, mixed-address 1, no-resolve 1, redirect-loop 1, rebind-loop 4, rebind-private 2, rebind-redirect 2, stable 4, slow-ok 2, multi-address 2.
stderr was empty (0 bytes) in all 5 runs. Each run took about 5-6 s of wall time.

## Artifacts
`.ufo/waves/round-30/falsify/RerunC2C/run{1..5}.json` (receipts), `run{1..5}.stdout`, `run{1..5}.stderr`.

## Residual risk and verification gaps
- Load: at start, `uptime` showed a load average of 7.76 on 32 cores. Sibling seats (`RerunC2B`, `MutNoWatchdog`) were running the same counter at the same time, so these 5 passes held under moderate contention, not on an idle host. [INFERENCE] Heavier contention could reduce the 1.4 s margin. Under v4, timing is the only axis these runs exercise that load can move.
- Five draws sample the per-item DEADLINE in [2.0, 6.0] s and the coin labels. They do not exhaust them. The earlier 24/27 on revision 33dd643f, where end of stream at the deadline was read as a full page, did not recur in 135 item draws.
- The run only scores against the counter, within its stated "Not claimed" limits: no per-hop address check and no real-network liveness.
- Clean-up: every process this seat started exited, and `pgrep` showed only other seats' processes. No installs or updates were made.
