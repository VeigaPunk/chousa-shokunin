# ExecC2Fetch — C2 build seat report (round 30, wave 1)

Scope: tool contract v2 items 2-4 (fetch layer) in a copy of the round-29
`tools/quote-reopen.py` at `.ufo/waves/round-30/build/ExecC2Fetch/quote-reopen.py`.
HTML-to-text step untouched (the diff contains no `html_to_text`, `_Text`, `SKIP` or
`BLOCK` lines).

## What changed

- `_check_address(host, port)` now returns the validated address strings after
  refusing any non-global result (contract item 3): one `getaddrinfo` per hop.
- New `_dial(addrs, port, connect_timeout, timeout, context, server_hostname)`:
  connects a fresh `socket.socket` to a numeric validated address (falling through
  the list), sets the socket timeout to the time remaining, and for https wraps it
  with `context.wrap_socket(sock, server_hostname=host)` on an
  `ssl.create_default_context()`, so SNI, certificate and hostname checks stay on.
  The returned `HTTP(S)Connection` keeps the host name, so the `Host` header is
  still the name. The peer address is never checked after connecting.
- Total deadline (contract item 2): `fetch_page` computes
  `deadline = monotonic() + float(DEADLINE)` (call-time read of the module
  constant, which the harness overwrites per item). A daemon
  `threading.Timer(remaining, _kill(holder))` watchdog shuts the socket down at
  the deadline; `holder[0]` captures the socket object at dial time because
  `http.client.getresponse()` calls `conn.close()` (nulling `conn.sock`) when the
  response is connection-close, while the fd stays alive via the response file
  object and `shutdown(2)` still trips a blocked `recv` — verified directly.
- `_read_response` reads with `resp.read1(CHUNK)` instead of `resp.read(CHUNK)`:
  `read` loops inside `fp.read` until the buffer fills, which a byte-per-0.2 s
  drip exploits without ever returning control; `read1` returns after one
  underlying read, so the deadline check between iterations bounds every drip.
- `main(argv)` and module-level `DEADLINE = 30.0` unchanged; docstring fetch-bounds
  paragraph updated only where the bounds changed.

## Evidence (all commands run from the lane root unless noted)

- `timeout 300 python3 corpus/evidence/round30/c2-count.py --tool
  .ufo/waves/round-30/build/ExecC2Fetch/quote-reopen.py --receipt
  .ufo/waves/round-30/build/ExecC2Fetch/c2-run1.json` →
  `QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27`, exit 0, max item wall 5.94 s
  (bound = per-item DEADLINE + 1.5 s). Run 2 (receipt `c2-run2.json`): 27/27,
  exit 0, max wall 6.125 s. All 13 kinds 100% both runs; every connect destination
  in each item's routed set (`validated_only: true` on all 27 items).
- `timeout 300 python3 corpus/evidence/round30/c1-count.py --tool ... --receipt
  .ufo/waves/round-30/build/ExecC2Fetch/c1-cross.json` →
  `QUOTE_REOPEN_HEADLESS_MATCH=78/106`, exit 1 — unchanged from the round-29 tool,
  as expected (C1 is a separate build).
- Receipt `counter_sha256` `0a59e373…` and `harness_sha256` `e2be0dd1…` match the
  frozen design v4 hashes in `corpus/evidence/round30/claims.md`.
- HTTPS verification check (one real GET to the allowed host docs.python.org, run
  in `/fast/scratch/hyaku/chousa-r30/w1/ExecC2Fetch`): `fetch_page(
  "https://docs.python.org/3/")` returned `status: 200 ctype: text/html
  text_len: 3195 detail: ` — the `server_hostname=host` wrap keeps certificate and
  hostname checks on, exit 0.
- `sha256sum` of the candidate tool:
  `0150361a32712a6a229d7ec09f93284492c90818113fa3dc49bb06a27aeff68b`.
- `diff -u tools/quote-reopen.py .ufo/waves/round-30/build/ExecC2Fetch/quote-reopen.py
  > .ufo/waves/round-30/build/ExecC2Fetch/c2.patch` — patch is 6188 bytes, 90
  `+`/`-` lines.
- Debugging done in scratch only (`/fast/scratch/hyaku/chousa-r30/w1/ExecC2Fetch/`):
  an instrumented copy with `faulthandler` showed the pre-fix hang at
  `socket.py:729 readinto` inside `resp.read`, and a trip log showed the first
  watchdog found `conn.sock=None` (the `will_close` hand-off above). The shipped
  copy carries no instrumentation.

## Verdict

C2 items 2-4 implemented: `QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27` on both runs,
exit 0. C1 unchanged at 78/106. HTTPS path still validates TLS.

## Limits / risks

- `read1` returns after one underlying read; on a drip this iterates once per
  byte — cheap in-process iteration, bounded by the deadline check.
- The watchdog is a daemon `threading.Timer`; a child stuck in pure C with the GIL
  held could delay it, but every blocking call here is socket I/O, which releases
  the GIL. The per-iteration `settimeout(remaining)` is the second bound.
- `_dial` caps the TCP connect per address at `min(remaining, 5.0)` s; with
  several unroutable addresses this stays inside the deadline because each attempt
  is separately capped and the inter-hop check refuses once `remaining <= 0`.
- Per the contract's Not-claimed section, per-hop address provenance is not
  asserted; connections go to addresses from the one lookup of that hop's host.
- Tooling directive: no packages installed; Python 3.14.8 stdlib only.
