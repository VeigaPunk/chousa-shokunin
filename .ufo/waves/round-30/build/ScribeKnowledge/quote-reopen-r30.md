# `quote-reopen.py` — HTML head boundary and bounded fetch (round 30)

source: S0NN (W3C optional tags); S0NN (W3C in-head insertion mode); S0NN (Python socket timeouts); S0NN (`socket.create_connection`); S0NN (`http.client`); S0NN (`ssl.wrap_socket` `server_hostname`); S0NN (`ipaddress.is_global`); frozen contract `corpus/evidence/round30/claims.md` (design v4, tool contract v2)
verified-at: 2026-10-23 UTC (drafted from the frozen local contract; source pages were not opened for this draft)
recheck: 180d (open the assigned S0NN sources and rerun `python3 corpus/evidence/round30/c1-count.py` and `python3 corpus/evidence/round30/c2-count.py` against the release)

## What changed

Round 30 updates the contract for `tools/quote-reopen.py verify`, which reopens registered source URLs to check whether a quote is located on a page. The changes address two distinct surfaces: HTML text extraction (C1) and fetching (C2).

### C1 — HTML head boundary

The old rule dropped content from `<head>` through an explicit `</head>`. HTML permits the `head` end tag to be omitted, and Python's parser does not infer that end tag; on such a document the old rule could therefore discard the later page text too. Contract v2 starts head suppression only at a `<head>` start tag and ends it at the first `</head>`, `<body>` start tag, start tag outside `base basefont bgsound link meta noframes noscript script style template title`, or non-whitespace character data outside those elements. Content of `title`, `script`, `style`, `noscript` and `template` remains dropped wherever it appears. The W3C optional-tags and in-head insertion-mode sources explain the HTML boundary represented by this rule.

### C2 — total fetch deadline and one DNS resolution per hop

A socket timeout bounds an individual blocking operation, not the entire fetch: a sender that keeps delivering bytes can keep successive reads active. Contract v2 makes `DEADLINE` bound the whole registry-URL fetch, including redirects, header and body reads, and the single retry; expiry stops the fetch and yields `UNREACHABLE`, so a steady drip cannot extend the total. The Python socket-timeout and `http.client` sources document the operation-level behavior the total bound must not be confused with.

The old connection path resolved the hostname again at connect, leaving the address check and destination vulnerable to DNS rebinding. Contract v2 resolves each hop's host once. If any returned address is non-global, the hop is refused; otherwise the connection uses one of those validated addresses, without a second lookup during connect. The hostname remains in the HTTP `Host` header and is used for TLS SNI and certificate verification. The `socket.create_connection`, `ssl.wrap_socket` `server_hostname`, and `ipaddress.is_global` source placeholders cover these interfaces and the address check.

## Counter evidence and limits

Run from the lane root:

```sh
python3 corpus/evidence/round30/c1-count.py
python3 corpus/evidence/round30/c2-count.py
```

C1 compares candidate verdicts with construction labels for generated head-boundary and regression cases. Its result belongs here as `QUOTE_REOPEN_HEADLESS_MATCH=<measured>`. C2 compares verdicts, elapsed time against each item's deadline-plus-slack, and connection destinations against the harness's routed global-address set. Its result belongs here as `QUOTE_REOPEN_FETCH_BOUND_MATCH=<measured>`. The L1 fills both placeholders from receipts; this draft contains no measured result.

Both counters execute the candidate in a loopback harness and make no network fetch. They do not establish liveness or show that real external pages are reached. C1 does not cover pages without a `<head>` start tag. A 2xx challenge page can pass the reachability check and produce `ABSENT` for its challenge content, indistinguishable there from a genuine missing quote. PDFs are out of scope. C2's destination predicate does not prove per-hop address provenance: it checks that connections use an address in the harness's routed set for that item. Neither counter establishes that a quote supports a claim or that its source is true.
