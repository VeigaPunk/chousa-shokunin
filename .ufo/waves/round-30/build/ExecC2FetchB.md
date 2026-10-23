# ExecC2FetchB — independent second implementation of contract v2 items 2-4

## What I did

Copied `tools/quote-reopen.py` to `.ufo/waves/round-30/build/ExecC2FetchB/quote-reopen.py`
and rewrote only the fetch layer, without reading any sibling build directory. The parser
(`_Text`, `html_to_text`), `found`, registry handling, verdict order, `main(argv)` and the
module-level `DEADLINE` are untouched.

New fetch layer (replaces `_check_address`, `_read_response`, `_request_once`; `http.client`
import dropped):

- `_resolve(host, port, deadline)` — one `getaddrinfo` per hop, run on a daemon thread
  joined for the remaining budget, so the lookup itself cannot outlive the deadline. Every
  returned address must parse and be `is_global`, else `_Refuse`. Returns
  `(family, sockaddr)` pairs; the name is never resolved a second time for that hop.
- `_connect(addrs, deadline)` — non-blocking `socket.socket.connect_ex` to a validated
  sockaddr (so the logged destination is always a validated address), completed via
  `select` + `SO_ERROR`. Tries the validated addresses in order.
- `_wrap_tls(sock, host, deadline)` — `ssl.create_default_context().wrap_socket(
  server_hostname=host, do_handshake_on_connect=False)` with a `SSLWantRead/Write`
  select loop: SNI and certificate check keep the host name even though the TCP peer is
  a validated literal address (contract item 3, TLS half).
- `_park(sock, deadline, write)` — the single wait primitive: `select` with timeout =
  `deadline - time.monotonic()`; an empty result or a non-positive remainder raises
  `_Refuse("deadline exceeded")`. `_fill` also re-checks the remainder before every
  `recv`, so a sender that keeps the socket readable cannot extend the fetch.
- Buffered readers `_read_head` / `_read_exact` / `_read_line` / `_read_body` parse the
  status line, headers, `Content-Length`, chunked framing (extensions and trailers) and
  close-delimited bodies, all under the wire cap and the same absolute deadline.
- `_request_once` keeps the base semantics (redirects to 10 hops, `GET` only, same
  headers, same status/ctype/inflate/charset handling, same return tuple). `fetch_page`
  keeps the shared deadline across the one retry.

## Measured scores (loopback harness, no network)

```
timeout 600 python3 corpus/evidence/round30/c2-count.py \
  --tool .ufo/waves/round-30/build/ExecC2FetchB/quote-reopen.py \
  --receipt .ufo/waves/round-30/build/ExecC2FetchB/receipt-c2-run1.json
QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27   exit 0   (re-run after a review fix; identical)
QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27   exit 0   run 2
timeout 600 python3 corpus/evidence/round30/c1-count.py --tool ... (same flags)
QUOTE_REOPEN_HEADLESS_MATCH=78/106     exit 1   (unchanged, as expected)
```

Receipts (same directory): `receipt-c2-run1.json`, `receipt-c2-run2.json`,
`receipt-c1-run1.json`. Both C2 runs: `predicate_holds=true`, all 27 items
`verdict_ok && bound_ok && validated_only`; walls 0.056-5.949 s vs per-item bounds
deadline+1.5 s; `unvalidated_dests` empty everywhere — all 8 rebind-class items
(rebind-loop x4, rebind-private x2, rebind-redirect x2) refused the second answer.
`by_kind` full marks in all 12 classes in both runs. C1 misses are exactly the 28
headless body windows (fetch layer untouched by C1).

SHA-256 of my candidate: `a3027c480e340bd656ad090a1c7584896f3a418acc0bfb0593d76a9aac73923f`
(recorded as `tool_sha256` in all 3 receipts). Counter/harness SHA-256 in receipts match
claims.md v4 (`c1` `5b312d84…`, `c2` `0a59e373…`, `qr_harness` `e2be0dd1…`).

## Design difference vs a watchdog-timer approach

A watchdog (timer thread + blocking socket that gets force-closed, or a signal alarm)
bounds *when* the fetch is interrupted, not *what* it waits on; it races the blocking
call, can fire late under load, and a second `getaddrinfo` hidden inside
`http.client.HTTPConnection(host).connect()` is invisible to it — that second lookup is
exactly the T1 rebind hole. This design instead makes the deadline the only clock: every
blocking point is a `select` whose timeout is recomputed as `deadline - now`, and the
only resolution is the single validated `getaddrinfo` whose sockaddr is passed to
`connect_ex` directly. Failure shape also differs: deadline expiry is `_Refuse` →
immediate `UNREACHABLE` with no retry, while transport errors stay retryable inside the
same budget.

## Limits

- HTTPS is code-path only: the harness serves plain HTTP, so `_wrap_tls` is exercised
  syntactically, not against a TLS peer [INFERENCE: correct by construction —
  `server_hostname=host` preserved, handshake bounded by `_park`].
- DNS threading is only a bounding device for a hanging resolver; the harness resolver
  returns instantly.
- No network was contacted; all evidence is the loopback counters. No tools installed.
