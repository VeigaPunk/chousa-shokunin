VERDICT: fail — C2 printed 27/27 on 3 of 5 runs; runs 2 and 4 printed 26/27, each a slow-ok item answered UNREACHABLE about 0.07 s past its DEADLINE (a 1 s connect stall; the cause points to the harness listen backlog of 5, not the tool's bounds)

## Frozen inputs (verified before scoring)

`sha256sum` from the lane root, tip `a9d3a05a8fd812a60323b08381019152069581fd` (`git rev-parse HEAD`), exit 0:

| file | SHA-256 | match |
|---|---|---|
| `corpus/evidence/round30/c1-count.py` | `5b312d84365924779ba8e6fe447cad3467f59c11848083d0967528c7a5e9d6e6` | yes |
| `corpus/evidence/round30/c2-count.py` | `0a59e3736fed8ef4cf7b00a75955eccfd0336c8a0ca84bee23402408b727f88f` | yes |
| `corpus/evidence/round30/qr_harness.py` | `e2be0dd16da5b2bf03430772831763e56c6ff6dd6a44063bb05c909b284f50d4` | yes |
| `tools/quote-reopen.py` | `47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201` | yes |

Every receipt below also records these counter, harness and tool hashes. Python 3.14.8.

## The five scored runs

Command, run one after another from the lane root (memory cap `ulimit -v 8000000`, process cap `ulimit -u 6000`):
`timeout 300 python3 corpus/evidence/round30/c2-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-30/falsify/RerunC2B/run{N}.json`

| run | printed line | exit | seed | wall |
|---|---|---|---|---|
| 1 | `QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27` | 0 | 7055672528826366775 | 6 s |
| 2 | `QUOTE_REOPEN_FETCH_BOUND_MATCH=26/27` | 1 | 821943121835704974 | 6 s |
| 3 | `QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27` | 0 | 508262958971894567 | 6 s |
| 4 | `QUOTE_REOPEN_FETCH_BOUND_MATCH=26/27` | 1 | 909001692554153263 | 6 s |
| 5 | `QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27` | 0 | 1654084451538910082 | 6 s |

Items that did not match (from `run2.json` and `run4.json`):

| run | kind | label | got | wall_s | bound_s | deadline_s | bound_ok | validated_only |
|---|---|---|---|---|---|---|---|---|
| 2 | slow-ok | VERBATIM | UNREACHABLE | 3.828 | 5.26 | 3.76 | true | true |
| 4 | slow-ok | VERBATIM | UNREACHABLE | 2.126 | 3.56 | 2.06 | true | true |

Both misses are verdict misses only: the wall time is inside the bound and every connection went to a routed address.

An earlier attempt at runs 1 and 2 crashed before scoring (`RuntimeError: can't start new thread` in `qr_harness.py:154`, exit 1, no receipt written). My own cap `ulimit -u 2000` caused it: `ulimit -u` counts every thread the user owns, and the user already had 2713. Those attempts are not scored; the table above is the rerun with the cap raised to 6000.

## Why the slow-ok items miss

1. On every passing slow-ok item the tool finished 0.93-0.94 s before DEADLINE (10 items across the five runs). The harness sends the last body piece DEADLINE - 1.0 s after the head (`qr_harness.py:252-264`). Both misses ended 0.066-0.068 s after DEADLINE, so each run lost about 1.0 s before the body began.
2. The label and framing do not cause it. I replayed `build()` from each recorded seed with a stub server (scratch, read-only use of the frozen counter). The two misses were Content-Length framed and labelled VERBATIM, but a scratch driver using the frozen harness unmodified (`/fast/scratch/hyaku/chousa-r30/w2/RerunC2B/slowok_matrix.py`) scored 32 of 32 slow-ok items across Content-Length or chunked × VERBATIM or ABSENT (8 each). Extra run 16 below also missed on an ABSENT item.
3. The tool reacts correctly: `fetch_page` starts the deadline before dialing (`tools/quote-reopen.py:447`), and `_read_response` refuses at the deadline (`:342-344`, `:359-360`). If the body completes later than DEADLINE, any tool that honors DEADLINE must answer UNREACHABLE.
4. [INFERENCE] The 1.0 s matches the Linux initial SYN retransmission timeout after a dropped SYN. The harness server is a `socketserver.ThreadingTCPServer` with the default `request_queue_size = 5` (`python3 -c "import socketserver;print(socketserver.TCPServer.request_queue_size)"` printed `5`; `qr_harness.py:146-151` does not change it). `c2-count.py:197` starts all 27 children at once (`max_workers=len(specs)`). The slow-ok class is the only class whose margin (1.0 s) does not absorb a 1 s connect stall. Every other class either has its label fixed to UNREACHABLE or finishes far inside DEADLINE + 1.5 s.

## Diagnostic runs (not scored; same frozen counter and tool)

- `extra{1..18}.json`: 17 of 18 printed 27/27. Extra run 16 (seed 3816068956073394450) printed 26/27: slow-ok, label ABSENT, got UNREACHABLE, wall_s 2.662, deadline_s 2.6, bound_s 4.1. The host-wide `nstat` TcpExtListenOverflows + TcpExtListenDrops delta was nonzero on runs 10-14 and 16 (8-30) and zero on the rest. The counter is host-wide, so this is consistent with the stall but does not prove it.
- Backlog control, scratch only: copies of `c2-count.py` and `qr_harness.py` in `/fast/scratch/hyaku/chousa-r30/w2/RerunC2B/bl/`. The only edit adds `request_queue_size = 128` to the harness server class. I ran it 18 times with `--tool /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quote-reopen.py` (receipts `bl/bl{1..18}.json`, harness SHA-256 `91475cbe…`, tool `47a657e7…`). All 18 printed 27/27, exit 0. The `nstat` TcpExtListenOverflows delta was 0 on all 18 control runs. On the frozen harness it was nonzero on 6 of the 18 extra runs. Extra runs 1-6 logged TcpExtListenOverflows alone; runs 7-18 logged it summed with TcpExtListenDrops. The frozen harness missed on 3 of 23 runs and the backlog-128 copy on 0 of 18. If the frozen rate were the true rate, 18 clean runs would happen about 8 percent of the time ((20/23)^18 ≈ 0.08). The direction is consistent with the backlog cause but not conclusive.

Across all 23 frozen-counter runs (5 scored, 18 extra), 3 printed 26/27, each with one slow-ok miss of this shape. That is 3 of 46 slow-ok items. No other kind ever missed.

## Residual risk and gaps

- Under the frozen kill rule ("any other value ... is a miss"; "a miss is reported, never re-scaled"), C2 is not met on this sample: 3 of 5 scored runs print 27/27.
- Root cause [INFERENCE]: the harness listen backlog. It is not shown per connection, because the counter keeps no connect timestamps and deletes its work directory. A fix would raise the server backlog, or leave slow-ok more than 1 s of margin before DEADLINE. Either change is a re-design, so it belongs to the L1 under claims.md rules. I changed nothing in the lane.
- No network fetch was made; no tools were installed or updated.
