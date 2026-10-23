# SimplifierHarness — round 30 WAVE 1: frozen harness/counter residue + loaded-host flakiness

Seat: ChousaR30.SimplifierHarness (leaf, no subagents). Date: 2026-10-23.
Scope: read-only analysis of the 3 frozen files under `corpus/evidence/round30/`; no lane file edited, no tool installed or updated (none needed).

Method and evidence:
- Frozen revisions verified before analysis: `qr_harness.py` `e2be0dd1…50d4`, `c1-count.py` `5b312d84…9d6e6`, `c2-count.py` `0a59e373…f88f` — all 3 match the SHA-256 prefixes recorded at the top of `corpus/evidence/round30/claims.md` (design v4).
- No `lsp` device exists in this session's tool inventory, so per the lane role rule this report uses text grep as the literal fallback; nothing below is presented as semantic-reference proof.
- One observed run per counter, sequentially, against a snapshot of the working-tree tool (byte-identical to the committed round-29 tool: `tools/quote-reopen.py` clean at HEAD `30c9d24`; snapshot SHA-256 `72a3ad47…4fea`), from the lane root:
  - `python3 corpus/evidence/round30/c1-count.py --tool <snapshot> --receipt .ufo/waves/round-30/build/SimplifierHarness/receipt-c1-run1.json` → `QUOTE_REOPEN_HEADLESS_MATCH=78/106`, exit 1, wall 0.045 s, tool_rc 1, not killed.
  - `python3 corpus/evidence/round30/c2-count.py --tool <snapshot> --receipt .ufo/waves/round-30/build/SimplifierHarness/receipt-c2-run1.json` → `QUOTE_REOPEN_FETCH_BOUND_MATCH=13/27`, exit 1.
  - Both reproduce the documented before-state; receipts carry counter/harness/tool SHA-256.
- Warm child-spawn cost probe (5 runs of `python3 -c pass` via subprocess): 0.006-0.007 s each. Host load at run time: 1-min 5.5-7.4, 15-min 31-33.

## A. Deletion candidates (recorded only — files are frozen; nothing deleted)

Classification: "free" = removing the line cannot change any output of either counter; "rng-only" = removal changes which items a run draws but not the distribution or the predicate machinery; "defensive" = dead under the current callers but protective if a caller changes.

`qr_harness.py` (346 lines):
1. Line 26 `import random` — free. `random.` appears nowhere in the file (grep, 0 hits).
2. Line 50 `real_gai = socket.getaddrinfo` — free, dead store. `fake_gai` (lines 60-87) never delegates to it and nothing restores it.
3. Line 52 `real_connect_ex = socket.socket.connect_ex` — free, dead store. `fake_connect_ex` (lines 108-113) is implemented via `fake_connect` plus `errno`; `real_connect_ex` is never called.
4. Lines 139 and 186 (`self.hits = []` / `self.hits.append(...)`) — free as a pair: write-only state. No reader exists in any of the 3 files (grep on `\.hits`). Keep only if request logging is wanted; today it is pure overhead in the server hot path.
5. Line 125 `m = None` — free, dead store: `m` is never read after. The secrecy gesture is also incomplete: `resolve`, `routed`, `log_path` stay reachable through the `fake_gai`/`target` closures, so a snooping child could introspect them. No scoring leak — labels never enter the child process (only addresses, port and deadline, all of which the contract gives the tool anyway).
6. Line 44 `sys.argv = [tool_path] + list(argv)` — defensive. Redundant for a contract-conforming candidate (contract v2 item 4 fixes `main(argv)`; the counters' tools parse the argument, not `sys.argv`), so removal is neutral for the measured tool, but it guards a candidate that reads `sys.argv`. Record, do not delete while frozen.
7. Line 197 `_drip(self, s, data, every, limit=40.0)` — `limit` is never overridden at either call site (lines 231, 239); a constant parameter. Free to inline, rng-free.
8. Line 258 `float(param or 1.8)` — the `or 1.8` fallback is unreachable through the frozen counters: `slow-ok` is the only behavior that passes `param`, and c2 always passes `deadline - 1.0` > 0 (c2-count.py line 132); c1 passes `param=None` only with `behavior=None`, which never reaches this branch. Defensive.
9. Line 292 defaults `deadline=None, cap=120.0` — never exercised: c1 passes `deadline=None, cap=180.0` explicitly (c1-count.py line 318), c2 passes `deadline=s["deadline"], cap=CAP` (CAP = 20.0). Documentation-only.

`c1-count.py` (357 lines):
10. Line 45 `import html` — free. `html.` appears nowhere in the file (grep, 0 hits); markup is built with string templates.
11. Lines 175-176 `if not script_in_head and not rest: parts.append(js)` — free, unreachable: `blocks` has 2 or 3 entries (line 151), so `rest = blocks[1:]` (lines 167/170) always holds at least 1 element; the body-script case is already fully handled inside the loop at lines 171-174. The branch contains no rng call, so removal cannot even shift the stream.
12. Line 241 — the doc dict keys `"cls"` and `"first"` are written and never read: only `d["path"]`, `d["body"]`, `d["host"]` are read (lines 310, 315-316), and each item's class travels in the items tuple, not the doc dict. Free to shrink (dead data, no rng shift).
13. Line 226 `sid_pool = rng.sample(range(100, 1000), 40)` — rng-only residue: 23 sids are consumed (20 documents + gone + unregistered + urlless); 17 are drawn and never popped. Deleting the overdraw shifts the rng stream for everything drawn afterwards (same distribution, different run), so it is not a free deletion.

`c2-count.py` (235 lines):
14. Line 121 vs 124 — `present = rng.random() < 0.5` at line 121 is a dead store for the 11 `FIXED_UNREACHABLE` items: line 124 redraws it before any read. rng-only residue (removal shifts later draws for those items; distribution identical).
15. Lines 113 and 118 — `gpool = H.global_addrs(rng, 3 * len(PLAN) + 4)` draws 85 addresses; only `gpool[3*k]` and `gpool[3*k+1]` are ever read, and `g2` only for multi-address (2 items) and rebind-redirect (2 items): 31 of 85 used; `gpool[3*k+2]` is never read for any of the 27 items. rng-only residue.
16. Duplication: `sha256()` is defined identically in c1-count.py (lines 66-71) and c2-count.py (lines 83-88) and is not exported by the harness — a third definition waiting to happen. Frozen-file duplication; record as known residue.

Also observed, not residue: line 127 `sys.stdout.flush()` before `os._exit` (line 128) is load-bearing, not dead — `os._exit` skips atexit/flush.

## B. Flakiness on a loaded host (frozen timing geometry, observed margins)

Constants (c2-count.py lines 67-69, 119, 132; qr_harness.py lines 254-262): per-item `DEADLINE` ~ uniform [2.0, 6.0] s; bound = `DEADLINE + 1.5` (SLACK); child killed at CAP = 20 s; slow-ok spreads its body over `param = DEADLINE - 1.0` s in 6 pieces, chunk terminator riding the sixth piece (the v4 fix, lines 260-262 of the harness).

Slack geometry: for an UNREACHABLE drip/stall item, a compliant tool aborts at about `DEADLINE + ε`, where ε = child startup + connect + verdict print + interpreter exit + parent `communicate` return. Observed on this host: ε = 0.06-0.12 s for fast items (walls in receipt-c2-run1.json), warm spawn 0.006-0.007 s. So roughly 1.4 s of the 1.5 s SLACK is spare scheduler room. A single descheduling event of the child longer than about 1.4 s during its 2-6 s run flips a passing item to a miss (wall > bound). This is the binding constraint; the 15-min load average here was 31-33, so multi-second stalls are realistic.

Observed per-class margins (receipt-c2-run1.json, base tool, one run):
- stall-body: wall 4.81 s vs bound 6.19 s → 1.38 s spare. Tightest observed margin, exactly the geometry above.
- slow-ok: 2.456/4.89 and 4.546/6.94 → 2.39-2.43 s spare. Roomiest dynamic class; both matched.
- fast items (stable, mixed-address, multi-address, no-resolve, rebind-*, redirect-loop): walls 0.06-0.12 s vs bounds 3.58-7.41 s → a stall must exceed roughly 3.4 s to matter; the label logic, not the clock, is what the base tool loses here.
- drip-steady: walls 4.107 and 4.123 s regardless of DEADLINE (2.11, 3.90) — the base tool's 64 KiB read granularity overshoots whenever DEADLINE < about 2.6 s; one missed at DEADLINE 2.11 (bound 3.61). A compliant tool gets the standard 1.4 s room.
- drip-head and drip-body (5 items): base tool never aborts → cap-killed at wall 20.00-20.02 s, rc −9, no verdict. Deterministic misses, not flake.

Amplifiers on a loaded host, in order of concern:
1. Stampede: c2 runs all 27 items at once — `ThreadPoolExecutor(max_workers=len(specs))` (c2-count.py line 197), each thread spawning a Python child; 27 interpreters start within a few tens of ms.
2. Accept backlog: the server is a plain `socketserver.ThreadingTCPServer` with `request_queue_size` unset (grep: 0 hits in qr_harness.py), so the default of 5 applies; 27 near-simultaneous connects can overflow the accept queue and incur about 1 s SYN retransmit delays. [INFERENCE on magnitude — no overflow observed in my run; all fast items connected promptly.]
3. Server-side pacing is `time.sleep`-based (`_drip` line 203, drip-steady line 249, slow-ok line 260): sleep overshoot under load delays slow-ok pieces beyond DEADLINE − 1.0 s and eats the item's 1.0 s + SLACK cushion even for a correct tool; observed server gaps were on time in my run.
4. Request-read timeout: `_handle` sets `s.settimeout(10)` (line 173); a child descheduled more than 10 s mid-request gets an empty connection and a wrong verdict — same stall family as 1.
5. Cap-kill semantics: an item whose child exceeds CAP = 20 s is scored a miss (`b` false in `score()`), not a measurement failure; claims.md's "exit 2 is a failed measurement" rule does not cover cap kills. A heavily loaded host can therefore convert every slow item of an otherwise compliant run into misses in one pass. Observation for the lesson, not a defect to fix under freeze.
6. `verdicts.setdefault` (line 329): first printed verdict per id wins — deterministic, but parsing is order-sensitive if a candidate prints twice.
7. C1 is effectively load-immune: 1 child, all pages fast, observed wall 0.045 s against cap 180 s (about 4000× headroom); `Spans.take` cannot realistically exhaust (at most 36 of 50-60 words of a block are ever marked used, 1000 retries, line 206 raise otherwise → exit 2, honestly a failed measurement).

Nothing in either counter or the harness touches the network; both runs above were loopback measurements (each connect event is logged to the run's `net.jsonl` and routed or refused inside the child), so the D1 wording rule applies: these are not live fetches.

## C. Contract preserved, tradeoffs, limits

- Deletions made: none — all 3 files are frozen; the deliverable is the candidate list above for the lesson's known-residue record. Free deletions: qr_harness lines 26, 50, 52, 125, 139+186, 175-176 (as pair), plus the dead dict keys at c1 line 241. The next deletion past that list starts harming axes: lines 44, 258, 292 are defensive armor, and lines 226, 121, 113 are rng-stream live, so "removal would not change behavior" stops here.
- Shared tree untouched: the only writes are this file and the 2 receipts under `.ufo/waves/round-30/build/SimplifierHarness/`; `git status --porcelain -- tools/quote-reopen.py` was clean, and no lane production file was opened for write.
- Limits: single observed run per counter (n = 1 each); margins are one sample of a random draw — the before receipts under `.ufo/waves/round-30/controls/` hold the repeated-run picture. Backlog-overflow magnitude is inference, flagged above.
