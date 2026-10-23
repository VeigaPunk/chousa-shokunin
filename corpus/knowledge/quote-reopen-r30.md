# `quote-reopen.py` — HTML head boundary and bounded fetch (round 30)

source: S050 https://www.w3.org/TR/2017/REC-html52-20171214/syntax.html#optional-tags §8.1.2.4 "Optional tags"; S051 https://www.w3.org/TR/2017/REC-html52-20171214/syntax.html#the-in-head-insertion-mode §8.2.5.4.4 "The in head insertion mode"; S052 https://docs.python.org/3/library/socket.html#socket-timeouts "Notes on socket timeouts"; S053 https://docs.python.org/3/library/socket.html#socket.create_connection; S054 https://docs.python.org/3/library/http.client.html#http.client.HTTPConnection; S055 https://docs.python.org/3/library/ssl.html#ssl.SSLContext.wrap_socket; S056 https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Address.is_global; frozen contract `corpus/evidence/round30/claims.md` (design v4, tool contract v2)
verified-at: 2026-10-23 UTC (round 30; each source passage was opened once on 2026-10-23 and its located quote is in `corpus/lessons/round-30.md` `## Gate`; S050 and S051 are the dated W3C HTML 5.2 Recommendation, because the undated `/TR/html52/` URL now redirects off www.w3.org. The counters' measured results are in SCORECARD.md, section "Round 30")
recheck: 180d (from the lane root: `python3 corpus/evidence/round30/c1-count.py` and `python3 corpus/evidence/round30/c2-count.py`; re-open S050 to S056 on a new release)

## What changed

Round 30 changes the contract of `tools/quote-reopen.py verify` (contract v2 in
`corpus/evidence/round30/claims.md`) on two separate surfaces: the HTML-to-text
step (C1) and the fetch layer (C2). Everything else in the round-29 contract
(`corpus/knowledge/quote-reopen-r29.md`) stands.

### C1 — the head boundary

HTML lets a page omit the `head` end tag (S050), and the HTML 5.2 parser ends
the head at the first token its "in head" rules do not handle: the "anything
else" branch pops the head element and reprocesses the token (S051). Python's
`html.parser` does not build that tree, so a tool that drops content from
`<head>` to `</head>` drops the whole page when `</head>` is missing. That was
the round-29 limit on S047.

Contract v2: content inside `head` is dropped. The head ends at `</head>`, at a
`<body>` start tag, at any start tag other than `base basefont bgsound link meta
noframes noscript script style template title`, or at character data outside
those elements that is not only whitespace (that data is page text). The
content of `title`, `script`, `style`, `noscript` and `template` is dropped
wherever it appears.

### C2 — one total deadline and one resolution per hop

A socket timeout bounds each blocking operation, not a whole transfer (S052,
S054). A sender that delivers one byte just inside the timeout keeps every read
alive, so the round-29 tool had no bound on a drip (sentinel finding T4).
Contract v2: the module constant `DEADLINE` (seconds, default 30) bounds the
whole fetch of one registry URL, across redirects, header and body reads and the
single retry. When it passes, the item is `UNREACHABLE`. The landed tool arms a
timer that shuts the socket down at the deadline, and it treats an end of stream
that arrives at the deadline, or before a declared `Content-Length` is
complete, as `UNREACHABLE`, not as a complete page.

`socket.create_connection` resolves a host name itself and tries each address
(S053), so a tool that checks the addresses and then connects by name resolves
twice, and the second answer can differ (sentinel finding T1, DNS rebinding).
Contract v2: each hop's host is resolved once; if any address is not global by
`ipaddress.is_global` (S056) the hop is refused; otherwise the tool connects to
a validated address. The host name stays in the `Host` header and is passed as
`server_hostname` so TLS keeps SNI and the certificate host check (S055).

## Counters and limits

Both counters run the candidate in a loopback harness
(`corpus/evidence/round30/qr_harness.py`) that answers DNS from a per-run map
and routes every connection to a local server. Every run draws a fresh seed.

| counter | what one item checks | before (round-29 tool) | after (landed) |
|---|---|---|---|
| `c1-count.py` → `QUOTE_REOPEN_HEADLESS_MATCH` | verdict equals its construction label on 100 generated document items (5 kinds of head shape) plus 6 verdict-order items | 78/106 | 106/106 twice |
| `c2-count.py` → `QUOTE_REOPEN_FETCH_BOUND_MATCH` | verdict equals label, wall time within that item's DEADLINE + 1.5 s, every connection to a routed global address | 12/27 | 27/27 on 41 of 44 fresh-seed runs; 26/27 on 3 (a slow-ok item refused about 0.07 s after its DEADLINE), so the C2 predicate is not met |

The after values were measured on lane revision `49b2aa3006d3c44a29b171ab30df09776c21405d`
(receipts `.ufo/waves/round-30/measure/after-c{1,2}-run{1,2}.json`).

What the counters do not show:

- Liveness. Neither counter reaches a real network.
- TLS. Every harness URL is `http://`; the TLS path is checked only by a
  separate real-page run.
- Per-hop address provenance. C2 checks that each connection goes to a global
  address of the item's own name map, not that each hop uses its own lookup.
- Name resolution and dialing. The harness answers lookups at once and every
  routed address connects. In the landed tool the lookup is a blocking
  `getaddrinfo` before the deadline check, each address reuses one connect
  timeout, and the timer starts only after dialing, so a slow resolver or a
  silent first address overruns `DEADLINE` (`.ufo/waves/round-30/falsify/SentinelFetchLayer.md`;
  a probe measured 6.0 s at DEADLINE 3, `falsify/ReviewKnowledge30.md`).
- IPv6, pages without a `<head>` start tag, 2xx challenge pages (S021, S022 on
  PubMed), PDFs and pages rendered by JavaScript.
- Support or truth. A `VERBATIM` verdict locates a quote; it does not show that
  the quote supports a claim or that the source is true.
