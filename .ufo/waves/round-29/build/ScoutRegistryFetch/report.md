# ScoutRegistryFetch — registry freshness reconnaissance (round 29, wave 1)

Scope: one bounded GET for every row of `corpus/SOURCES.md` whose `source` cell
holds an http(s) URL, and a judgement of what the frozen C1 contract
(`corpus/evidence/round29/claims.md`, tool contract verdict 3) would call
reachable. This is reconnaissance for C1's 130/130 target; it measures nothing
about C1 and it edits nothing.

## Method — what I ran

1. Row and URL extraction mirrors the counter's own parser, `c1-count.py`
   `registry_url` (lines 112–118): lines starting `| S`, split on `|`, field 2,
   first `https?://\S+`, trailing `.,;)` stripped.
2. Fetch mirrors the counter's `fetch_text` (lines 121–139): `urllib.request`,
   User-Agent containing `chousa-quote-reopen`, `Accept-Encoding: gzip`, 30 s
   timeout, redirects followed (urllib default), fragment removed
   (`url.split("#")[0]`), `read(8 MiB + 1)`, gzip/deflate inflate, then
   `html.parser` text extraction with the counter's `SKIP`/`BLOCK` sets.
3. One GET per unique URL. First pass: 36 registry rows over 31 URLs, in 5
   duplicate pairs (S029=S019, S030=S022, S031=S024, S032=S021, S033=S020);
   duplicate rows inherit the single fetch record and are marked `dup-of-*`,
   they were not fetched again.
4. Additive pass after the registry grew during the run: the 4 rows that had
   landed (S046–S049) were fetched once each, no recorded URL was re-fetched,
   and every previously recorded row's URL was re-checked against the new
   registry revision (`drift=0`).
5. Fidelity of my copies against the counter's reference functions was checked
   behaviorally, not by eye: `SKIP` equal, `BLOCK` equal (31 elements), `QMAP`
   equal, `norm` equal on NFKC/typographic/whitespace samples, HTML extraction
   equal on a mixed-markup sample.

Commands and observed results:

```
mkdir -p /fast/scratch/hyaku/chousa-r29/w1/ScoutRegistryFetch \
         <lane>/.ufo/waves/round-29/build/ScoutRegistryFetch
ls -la <lane>/tools/ && python3 -VV && curl --version | head -2
  -> tools/ holds only research-gate.sh; Python 3.14.8; curl 8.23.0
cd /fast/scratch/hyaku/chousa-r29/w1/ScoutRegistryFetch
timeout 590 python3 registry_fetch.py <tsv>      -> EXIT=0, "rows=45 unique_urls=31",
                                                    shell wall 18.56 s
timeout 200 python3 registry_fetch_more.py <tsv> -> EXIT=0, "new_rows=4 drift=0"
env | grep -i -E 'proxy|no_proxy'   -> no match, rc 1 (no proxy in the environment)
date -u +'UTC now: %Y-%m-%dT%H:%M:%SZ' -> UTC now: 2026-10-23T01:26:00Z
```

Inputs at read time, hashed:

| artifact | sha256 |
|---|---|
| `corpus/SOURCES.md`, first read (45 rows) | `8bc103823c3a08114e3f787dca96384a6f739931ae3de8c5bdbc64b7225c64b4` |
| `corpus/SOURCES.md`, second read (49 rows) | `d8aa0454b50bbe229f255885c970660540f8ecf5bac633ec136165b3425819be` |
| `registry_fetch.py` | `283623765576c13ae5b18f25af272695c90b2b73c363ac97beb727f2dc9ab472` |
| `registry_fetch_more.py` | `08fab0372e60d79bcdb7047b3c5fb0e3aceb9b388c0dfc7ece2b7520d48d8417` |
| `registry-fetch.tsv` (final) | `ba73e4ce502a3c26a432453e6d21cf3cccedd7aae4f69ff2fa3a5ba2d4a539b1` |

## Observed — 35 GETs, access date 2026-10-23 (UTC)

- Registry rows: 49, of which 40 hold a URL (the 9 without a URL are S001,
  S034, S035, S036, S040, S041, S042, S043, S045). The registry grew from 45 to
  49 rows between my two reads; S046–S049 are the rows that appeared.
- 35 unique URLs, 35 GETs, one redirect (S025
  `https://www.rfc-editor.org/rfc/rfc9111` →
  `https://www.rfc-editor.org/info/rfc9111/`, same host, final 200 `text/html`).
- Final statuses: 32 × `200`, 2 × `203`, 1 × `403`.
- Content types: 33 × `text/html`, 2 × `application/pdf`.
- No body over 8 MiB; largest 3,652,650 B (S011).

Full table: `registry-fetch.tsv` beside this file. Rows the frozen contract
would mark `UNREACHABLE`:

| id | status | content type | bytes | gate that fires |
|---|---:|---|---:|---|
| S011 | 200 | `application/pdf` | 3,652,650 | content type not in text/html, application/xhtml+xml, text/plain |
| S037 | 200 | `application/pdf` | 1,457,761 | content type, same rule |
| S014 | 403 | `text/html` | 919 | final status is not 2xx |

These are named limits, not failures: the claim's own "Not claimed" section
excludes PDF sources, and S014 is a rejected row. No row is over the 8 MiB body
bound.

Reachable by the contract's letter, degraded in substance (silent risk):

- S021 and S022 (with their duplicate rows S032 and S030): HTTP `203`, which is
  2xx, so the contract calls them reachable — but the body is 2,207/2,206 B and
  yields 17 words of text (5,590 inflated bytes). [INFERENCE] that shape is a bot
  interstitial, not the PubMed abstract. I did not retain the body, so I do not
  quote it; the observation is status, size and word count only. An item citing
  these rows would come back `ABSENT` (a false negative), never `UNREACHABLE`.
  A tool that gates on `status != 200` would wrongly emit `UNREACHABLE` here.
- S047: 200, `text/html`, 68,837 B, **1 word** of extracted text. See the
  mechanism section below; any quote item citing S047 comes back `ABSENT`.
- S017 (197 words), S026 (283 words), S024/S031 (94 words): reachable, thin
  extracted text from large HTML (S026: 173,583 B → 283 words), i.e. pages whose
  prose is not in the served HTML or whose term page is short.
- S046's registry URL carries a fragment (`#text-quote-selector`). The contract
  removes fragments, so the tool reads the whole Recommendation: 200,
  `text/html`, 49,021 B, 17,538 words. A quote taken from the fragment's section
  is searched against the whole page, which is correct under the rule but means
  the fragment does not restrict the search.

## S047 and the extractor's implied-end-tag gap

Observed: `https://wicg.github.io/scroll-to-text-fragment/` returns 200
`text/html`, 68,837 B, and the contract's HTML-to-text rule yields exactly 1
word. The source seat for the same row (`.ufo/waves/round-29/build/ScribeSrcTextFragments.md`
line 4) records a located 13-word quote from §3.6.1 of the rendered page — so the
sentence is there for a reader, and still un-reopenable under the frozen rule.

Mechanism, proven on synthetic input with the counter's own `_Text` (this cell's
scratch, not a claim about S047's bytes): Python `html.parser` applies no implied
end tags, and the contract's extractor counts `SKIP` depth. A document that opens
`<head>` and never writes `</head>` — which browsers close implicitly at `<body>`
— leaves the skip counter at 1 for the rest of the document, so every body text
node is dropped:

```
"<html><head><title>T</title></head><body><p>Real text here</p></body></html>"  -> 3 words
"<html><head><title>T</title><body><p>Real text here</p></body></html>"        -> 0 words
"<head><title>T</title><body><p>Alpha beta gamma</p>"                          -> 0 words
skip counter after feeding "<head><title>T</title><body>"                      -> 1
```

[INFERENCE] S047's 1 word follows from either client-side rendering or an
unclosed skip element; I did not retain the bytes (one GET per URL), so I cannot
separate the two causes. Either way the consequence is the same and is inside the
claim's "Not claimed" boundary (pages rendered by JavaScript; block-spanning
quotes): S047 cannot carry a reopenable quote under this contract.

The 8 page-sampled sources do not show this failure: all yield between 393 and
25,125 words, so none is dropped wholesale.

## Bearing on C1's 130/130 target

- Fixture tally, re-run: 40 items, labels 20 ABSENT / 14 VERBATIM / 3 TOO_LONG /
  3 NO_SOURCE; source ids S008 × 8, S044 × 7, S013 × 7, S019 × 5, S020 × 4,
  S002 × 3, S038 × 2, S001 × 1, S045 × 1, S003 × 1, S999 × 1.
- The 8 VERBATIM source ids are exactly {S002, S003, S008, S013, S019, S020,
  S038, S044} — the same 8 the counter page-samples. All 8 returned `200`
  `text/html` with 393 to 25,125 extracted words (S013 is the thinnest at 393).
- In the counter's `build()`, runtime subspan and transpose items keep the
  VERBATIM item's source id, and runtime cross-attribution uses `rot[sid]`, a
  rotation inside the same 8 ids. So every one of the 130 items resolves to the
  8 reachable rows or to the 3 `NO_SOURCE` rows (S001, S045, S999). Zero items
  need S011, S037 or S014, and the frozen fixture references none of S046–S049.
- Verdict: on 2026-10-23 there is no registry-side reachability blocker for C1.
  That is a feasibility statement about the registry, not a measurement of the
  claim; C1's number comes from the executor's own run.

## Unresolved and limits

1. One GET per URL was my bound, so page stability across the counter's two
   fetches is untested. `page_cases()` raises `ValueError` (counter exit 2) if
   any of the 8 sources cannot yield 3 windows present in both fetches with a
   transposition absent from both. S013's 393 words is the tightest margin,
   though 393 words is ample for 3 windows of 6 to 20 tokens.
2. Bodies were not retained, so this report quotes no page text; every statement
   is structural (status, content type, sizes, word counts). The S047 cause is
   therefore inference, not observation.
3. The registry changed during the run (45 rows → 49 rows). This record covers
   the 49-row revision hashed above; a later row needs its own check, and a later
   revision may move an existing row's URL, which the additive pass re-checks
   (`drift=0` on this revision).
4. Live pages can change after 2026-10-23; the frozen counter re-fetches at run
   time, so a later miss is a live-content finding, not a contradiction of this
   reconnaissance.
5. Fetches were sequential, mirroring the tool, so no concurrency artifact was
   introduced; there is also no second sample of any URL to detect churn.

## Tooling

No installs or updates. `python3` 3.14.8 and `curl` 8.23.0 were already present.
No writes outside this seat's own build directory; the fetch scripts are kept
beside this report for re-running.
