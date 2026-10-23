# Attack Row S054 — falsify report

VERDICT: pass — S054 row cells match the opened page (quote verbatim, 12 words) and the landed tool verdicts VERBATIM (exit 0).

## (1) Page open + row-cell check

- Opened once (GET only): `timeout 120 curl -sS -o s054.html -w 'HTTP=%{http_code} BYTES=%{size_download} URL=%{url_effective}\n' --max-time 60 'https://docs.python.org/3/library/http.client.html#http.client.HTTPConnection'` → `HTTP=200 BYTES=100605 URL=https://docs.python.org/3/library/http.client.html#http.client.HTTPConnection` (no redirect; stayed on the registered host). Page SHA-256 `8cda0c544c834623f7869647fc49cd9dcbb658987b59364426988b7ca01d9443` (scratch copy `s054.html`).
- Anchor `id="http.client.HTTPConnection"` present. Extracted constructor text (HTML stripped): `class http.client.HTTPConnection(host, port=None, [timeout,] source_address=None, blocksize=8192, max_response_headers=None)` then: "If the optional timeout parameter is given, **blocking operations (like connection attempts) will timeout after that many seconds** (if it is not given, the global default timeout setting is used)."
- Gate quote (round-30.md line 49): `"blocking operations (like connection attempts) will timeout after that many seconds"` — verbatim, 12 words (≤25), at the named section (class http.client.HTTPConnection constructor description). `grep -c 'blocking operations'` on raw HTML = 0 only because the phrase spans `<span>` tags; the text extraction above is the relevant evidence.
- Row S054 cells (SOURCES.md): source URL matches (same host/path/anchor); kind `docs`, tier A, status `mined`, opened 2026-10-23 — consistent with a Python docs page pulled 2026-10-23; scope states "timeout semantics and host-based connection setup; not a total-fetch deadline or DNS-pinning guarantee" — the page says the timeout limits each blocking operation and the target is a host name and port; it does not state a total-fetch deadline or DNS pinning, so the scope is not more than the page says. Anchor matches the constructor description. Teaches "The timeout limits each blocking operation such as a connection attempt, and the connection target is a host name and port" — exactly what the quoted sentences say. No cell exceeds the page.

## (2) Landed tool run

- Tool SHA-256 `47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201` (matches frozen); counters/harness hashes match frozen values (c1 `5b312d84…`, c2 `0a59e373…`, harness `e2be0dd1…`).
- One-item TSV: `id<TAB>source_id<TAB>quote` → `S054-check / S054 / blocking operations (like connection attempts) will timeout after that many seconds`.
- Command: `cd /home/vgpnk/Projects/shokunin/chousa-shokunin && timeout 120 python3 tools/quote-reopen.py verify --items <tsv>`:
  - `QUOTE_REOPEN	S054-check	VERBATIM	matched in normalized page text`
  - `QUOTE_REOPEN_SUMMARY verbatim=1 absent=0 too_long=0 no_source=0 unreachable=0`
  - exit 0. No non-VERBATIM finding. (A first run using lowercase `s054` returned `NO_SOURCE no registry row s054`, exit 1 — a case-sensitive registry key issue in my item file, not a tool defect; with the correct row id S054 the verdict is VERBATIM.)
- Note: the tool fetched the page itself during verify (same URL as above); that is the only network access this seat made, to the registered S054 host.
- Scratch artifacts in `/fast/scratch/hyaku/chousa-r30/w2/AttackRowS054/`: `s054.html`, `items-s054.tsv` (final), server-side no other writes.

## Remaining unknowns

- None blocking the verdict. [INFERENCE] The page our fetch saw (Python 3.15.1 docs) matches the row's anchor cell "Python 3.15.1 documentation"; the row's "on-release" recheck status is a lane metadata convention, not something this seat judges.
