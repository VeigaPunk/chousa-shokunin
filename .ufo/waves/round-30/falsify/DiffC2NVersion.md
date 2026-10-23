VERDICT: pass — landed tool and ExecC2FetchB build both score C2 27/27 in 3/3 runs (exit 0, margin to bound), and the two fetch layers differ in 7 behaviors the counter cannot see.

## Measurement
All commands from the lane root. Counters/harness SHA-256 match frozen values (c2-count.py 0a59e373…f88f, qr_harness.py e2be0dd1…50d4). Tool SHA-256: landed 47a657e72f38… (matches frozen); build a3027c480e34… (distinct revision).

```
for i in 1 2 3; do python3 corpus/evidence/round30/c2-count.py --tool tools/quote-reopen.py --receipt .ufo/waves/round-30/falsify/DiffC2NVersion/receipt-landed-run$i.json; echo rc=$?; done
QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27  rc=0 (x3)
for i in 1 2 3; do python3 corpus/evidence/round30/c2-count.py --tool .ufo/waves/round-30/build/ExecC2FetchB/quote-reopen.py --receipt .ufo/waves/round-30/falsify/DiffC2NVersion/receipt-build-run$i.json; echo rc=$?; done
QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27  rc=0 (x3)
```

## Per-kind results (81/81 items each; no miss, no unvalidated dest on any item)
Landed and build both: drip-head 6/6, drip-body 9/9, drip-steady 6/6, stall-body 3/3, mixed-address 3/3, no-resolve 3/3, redirect-loop 3/3, rebind-loop 12/12, rebind-private 6/6, rebind-redirect 6/6, stable 12/12, slow-ok 6/6, multi-address 6/6. Each run uses a fresh `urandom` seed (recorded in receipts).

Wall margins `wall − DEADLINE` (bound check is `deadline + 1.5`):
- Landed: drip/stall/steady land within +0.06…+0.33 s of the deadline; slow-ok −0.70…−0.94; fast items −1.96…−5.92. No margin > 1.5.
- Build: drip/stall/steady +0.06…+0.10; slow-ok −0.91…−0.94; fast items −1.96…−5.92. No margin > 1.5.
Both tools stop at the deadline with ~0.1 s mechanical delay, far inside the 1.5 s slack; neither overruns.

## Fetch layers read
- Landed: `tools/quote-reopen.py` lines 204–464 (`_check_address`, `_dial`, `_kill`, `_read_response`, `_request_once`, `fetch_page`); http.client-based with a `threading.Timer` watchdog that `shutdown(SHUT_RDWR)`+closes the captured socket at the deadline.
- Build: `.ufo/waves/round-30/build/ExecC2FetchB/quote-reopen.py` lines 160–550; raw-socket reader (select-based `_park`, `_fill`, `_send_all`, `_read_head`, `_read_exact`, `_read_line`, `_read_body`, `_connect`, `_wrap_tls`, `_request_once`, `fetch_page`); every wait is bounded by the absolute monotonic deadline.

Common contract surface (both): resolve once per hop, refuse any non-global address, connect to a validated address, Host header/SNI/cert check use the host name, one retry shared with the deadline, 8 MiB wire and inflated caps, GET only, http(s) only, fragment stripped, no userinfo/cookies/credentials, no disk writes, module-level `DEADLINE` and `main(argv)`.

## Behavioral differences the C2 counter cannot see (harness fake gai is instant and routes/refuses instantly)
1. **Resolver hang (deadline not applied).** Landed `_check_address` calls `socket.getaddrinfo` synchronously with no timeout — a stuck resolver extends the fetch past `DEADLINE` (and past CAP at the harness). Build `_resolve` runs the lookup on a daemon thread joined with `max(0, deadline − now)` and raises `_Refuse("deadline exceeded during name resolution")`. Counter-invisible: fake gai never blocks.
2. **Multi-address connect fallback can overrun the deadline.** Landed `_dial` captures a single `connect_timeout = min(remaining, 5.0)` and applies it to each address attempt in turn; with N black-holed validated addresses the connect phase can take N×5 s > deadline (the retry loop then exits at the deadline, but wall time can exceed `deadline + 1.5`). Build `_connect` parks each attempt on the absolute deadline via `_park`, so the chain cannot overrun.
3. **Malformed framing/truncation outcome class differs.** Landed: truncated Content-Length body → `_Refuse` (UNREACHABLE, no retry); malformed chunked framing → `http.client.HTTPException` → `_Refuse`, no retry. Build: truncation → `EOFError`/`ConnectionError` (retryable), malformed chunk size/content-length → `ConnectionError` → retried once. On a real flaky server the two tools can produce different verdicts (retry vs immediate UNREACHABLE).
4. **Response head size cap.** Build caps the head at 256 KiB (`_Refuse`); landed has no explicit head-size cap (http.client's per-line/header limits only) — a slow header flood is bounded only by the deadline/watchdog.
5. **Deadline mechanism granularity.** Landed uses a Timer-based socket shutdown (thread wake latency, ~ms; observed margins up to +0.33 s); build uses select with absolute deadline in every path (margins ≤ +0.10 s). Both are well inside slack, but the landed margin is 3× larger on drip items.
6. **Interim 1xx responses.** Landed relies on http.client's internal 100-Continue skip; build skips 100–199 explicitly in the raw head loop. Equivalent behavior, different implementation.
7. **TLS handshake pacing.** Landed: blocking `wrap_socket` with the per-op socket timeout, watchdog covers it. Build: `do_handshake_on_connect=False` + explicit park loop, also deadline-bounded. Both enforce; only the mechanism differs.

No claim regression found: both tools satisfy the frozen C2 predicate on the frozen counter (3 runs each), and the build is not a re-scaled or keyed shortcut (it implements contract items 2 and 3; verdicts come from real fetches, per the receipts' item rows).
