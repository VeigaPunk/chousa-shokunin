## Decision table addition

| Intent | Correct surface | Never | Expected output |
|---|---|---|---|
| Re-open a quote on a page whose HTML omits `</head>` | Run `python3 tools/quote-reopen.py verify --items <tsv>` and extract body text using the permitted HTML head boundary | Treating the missing end tag as end-of-document; reading `VERBATIM` as support or truth | One verdict per quote; record and hand-check each non-`VERBATIM` result |

## Error-pattern additions

| Observation | Reading |
|---|---|
| body quote `ABSENT` on a headless page | The parser may have treated all following content as head; apply the HTML head boundary and inspect the extracted body text before recording a source finding |
| fetch exceeds its stated deadline under a slow sender | A per-operation timeout is not a total-fetch deadline; bound redirects, headers, body reads and retry together, and stop as `UNREACHABLE` when the total deadline expires |
| address check passes, connection goes elsewhere (second DNS lookup) | Validation and connection used different resolutions; resolve once per hop and connect only to a validated address, retaining the hostname for `Host` and TLS |

## Gates addition

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| `quote-reopen` frozen coverage and fetch-bound counters | gate | `python3 corpus/evidence/round30/c1-count.py` · `python3 corpus/evidence/round30/c2-count.py` | `QUOTE_REOPEN_HEADLESS_MATCH=106/106` · `QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27`; any other count is a miss | Run both entry commands; each must print its stated target | Frozen predicates in `corpus/evidence/round30/claims.md` | Loopback harness only; no network; optional receipt output only when requested | chousa |
