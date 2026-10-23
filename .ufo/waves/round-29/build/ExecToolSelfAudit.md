# ExecToolSelfAudit — reference-function conformance audit (round-29 C1 counter)

Seat: `ExecToolSelfAudit`, wave 1 build, chousa lane round 29.
Target: the six reference functions of `corpus/evidence/round29/c1-count.py`
(`_Text`, `norm`, `found`, `registry_url`, `fetch_text`, `page_cases`), which
label the 48 page-sampled items.
Contract text: `corpus/evidence/round29/claims.md`, section "Tool contract
(frozen)".
Measured counter: SHA-256 `cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d`
at lane commit `66bf1b93` (design v3). I re-derived that the reference-function
block is byte-identical between the v2 freeze `1224443` and the v3 freeze
`aa5e1a3`, so this audit applies to both.

## Verdict

**REFERENCE-DEVIATES** — 6 deviations, listed below. 1 is present in the live
markup (Dev-1, on S003); 5 are latent, with zero occurrences on the eight live
pages on 2026-10-23. **None changes a label on the eight pages as they are
served today**: all eight token streams are identical between the reference and
the contract-literal reading (0 of 8 differ). The deviations are risks, not
observed mislabels.

## What I did

Two independent artefacts, both stdlib only, both in my scratch directory and
copied to `.ufo/waves/round-29/build/ExecToolSelfAudit/`:

- `contract_model.py` — an independent transcription of the contract text into
  executable rules (`CONTRACT_BLOCK`, `CONTRACT_SKIP`, `contract_norm`,
  `ContractText`, `contract_found`, `contract_registry_url`,
  `contract_body_decoding`). Built with `chr()` codenames so no literal
  U+200B can be lost in transit — an earlier literal-character version
  fabricated a false S003 divergence and was discarded.
- `audit_reference.py` — 72 unit checks that import the committed counter
  read-only and compare each reference function against the model on synthetic
  inputs, plus two differential fuzzers.

Supporting probes: `check_contract_lists.py` (extracts the block and skip lists
out of `claims.md` and diffs them against the counter's sets), and
`probe_live_pages.py` / `probe_materiality.py` /
`probe_structure_hazards.py` / `probe_registry_ambiguity.py` / `probe_details.py`
(one GET per registry `source` URL, read-only).

I never ran the counter: no `build()`, no `main()`, no fixture item, no seed, no
receipt, no subprocess. The counter was imported for its pure functions only.
Per the L1 stop-order of 2026-10-22 I did not invoke it as a program.

## Evidence

```
$ python3 check_contract_lists.py
contract block list (from claims.md): p div li ul ol table tr td th h1 h2 h3 h4 h5 h6
  br section article header footer nav pre blockquote dt dd dl figure figcaption hr main aside
count: 31
contract skip list (from claims.md): script style noscript template head
count: 5
counter BLOCK: article aside blockquote br dd div dl dt figcaption figure footer h1 h2 h3
  h4 h5 h6 header hr li main nav ol p pre section table td th tr ul 31
counter SKIP : head noscript script style template 5
VERDICT: SETS-CONFORM
exit=0

$ python3 audit_reference.py
Ran 72 tests in 0.083s
OK
exit=0

$ python3 audit_reference.py -v | grep fuzz
  fuzz divergence classes: {'same': 1403, 'D1 space-leak': 76, 'UNEXPLAINED': 21}
  # all 21 UNEXPLAINED are D2/D3 shapes: a separate classification run gave
  # D1-only 76, D2-or-D3 21, fourth-class 0

$ python3 probe_materiality.py
  S002: raw_same=True  raw_len_delta=0 token_streams_same=True tokens=1654/1654
  S003: raw_same=False raw_len_delta=2 token_streams_same=True tokens=25125/25125
  S008: raw_same=True  raw_len_delta=0 token_streams_same=True tokens=9529/9529
  S013: raw_same=True  raw_len_delta=0 token_streams_same=True tokens=393/393
  S019: raw_same=True  raw_len_delta=0 token_streams_same=True tokens=5955/5955
  S020: raw_same=True  raw_len_delta=0 token_streams_same=True tokens=21646/21646
  S038: raw_same=True  raw_len_delta=0 token_streams_same=True tokens=13898/13898
  S044: raw_same=True  raw_len_delta=0 token_streams_same=True tokens=3315/3315
  pages whose token streams differ: 0 of 8

  norm() idempotence: non-idempotent samples: 0 of 20000
  counter norm vs contract norm on the live corpus: 0 of 8 differ
```

## What conforms (checked, not assumed)

| Contract clause | Result | Evidence |
|---|---|---|
| block list "exactly these" | conforms, 31 of 31, no extra, no duplicate | `check_contract_lists.py`, `TestFrozenSets` |
| skip list `script style noscript template head` | conforms, 5 of 5 | same |
| comments dropped | conforms | `test_comment_dropped` |
| character references decoded | conforms, `&amp; &#39; &#x2019;` | `test_charrefs_decoded` |
| NFKC before the quote map | conforms | `test_nfkc_applied`, `test_nfkc_before_quote_map_matches_contract` |
| quote map U+2018-201B to `'`, U+201C-201F to `"` | conforms, all 8 | `test_quote_map_*` |
| deletions U+00AD U+200B U+200C U+200D U+FEFF | conforms, all 5 | `test_deletions` |
| whitespace collapse + ends stripped | conforms | `test_whitespace_run_collapse_and_strip` |
| boundary rule at both ends, `str.isalnum` | conforms | `test_left/right_boundary_*`, `test_boundary_at_text_edges` |
| case sensitivity | conforms | `test_case_sensitivity` |
| gzip and zlib-wrapped deflate decoded | conforms | `test_gzip_body_decoded`, `test_zlib_deflate_body_decoded` |
| `text/plain` path is not HTML-parsed | conforms | `test_text_plain_path_is_not_html_parsed` |
| URL fragment stripped before fetch | conforms, `https://example.org/p#sec` to `https://example.org/p` | `test_fragment_is_stripped` |
| registry: first URL in cell, trailing `.,;)` stripped | conforms on all 49 rows and all 8 fixture rows | `TestRealRegistry`, `test_first_url_in_cell_*` |
| 30 s timeout, UA contains `chousa-quote-reopen`, GET | conforms | `test_timeout_is_thirty_seconds`, `test_user_agent_*` |
| `found` normalizes the quote before matching | conforms, and `norm` is idempotent (0/20000) | `test_quote_is_normalized_before_matching` |
| `page_cases` fetches each URL twice, 3 windows, transpose absent from both | conforms | `test_two_fetches_per_url`, `test_transpose_is_absent_from_both_fetches` |

Randomized agreement: `norm` 5000 samples, `found` 5000 samples, zero
disagreements with the contract model.

## Deviations

### Dev-1 (live, latent label risk) — a block element inside a dropped region still emits its space

The counter's `_Text.handle_starttag` / `handle_endtag` append the block
element's space without checking `self.skip`. The contract says the content of
`script`/`style`/`noscript`/`template`/`head` "is dropped", so a dropped region
should contribute nothing.

```
        doc = "foo<noscript><p>x</p></noscript>bar"
counter   _Text -> 'foo  bar'   norm -> 'foo bar'
contract        -> 'foobar'     norm -> 'foobar'      # token streams differ
```

Live: present on **S003** `https://hapgood.us/2019/06/19/sift-the-four-moves/`
(2 `<p>` inside `<noscript>`), raw length delta +2. The leaked spaces sit
inside an existing whitespace run on that page, so after the contract's
whitespace collapse the token streams are identical (25125 tokens both) and no
label changes. A page where the leak lands between two non-space characters
would split a token and could flip a page-window label. Live effect today:
none measured.

### Dev-2 (latent, content-leaking) — one shared depth counter instead of a stack

`_Text` keeps a single integer `skip` for all five drop elements and decrements
it on the end tag of any of them. An end tag for a different drop element ends
the wrong region, so its interior text leaks into the page text. Of the 97
fuzz divergences (1500 documents), the 21 that are not pure space leaks are
this shape or Dev-3.

```
        doc = "<noscript>a</script>SECRET</noscript>"
counter   -> 'SECRET'   contract -> ''
        doc = "<template>x</script>SECRET</template>"
counter   -> 'SECRET'   contract -> ''
```

Live: 0 crossed or unmatched drop end tags on all eight pages
(`probe_structure_hazards.py`), so not triggered today. This class leaks real
words, not whitespace.

### Dev-3 (latent, content-leaking) — a self-closing drop element opens no region

`handle_startendtag` handles only block tags; it never enters a dropped region.
The contract says the content of `script` is dropped, and `<script/>` is not
self-closing in HTML — in Python `html.parser` it routes to
`handle_startendtag`, so the following markup is not dropped.

```
        doc = "<script/>LEAK</script>"
counter   -> 'LEAK'   contract -> ''
```

Live: 0 self-closing `<script/>`/`<template/>`/`<style/>`/`<noscript/>`/`<head/>`
on all eight pages. Not triggered today.

### Dev-4 (latent) — the reference does not enforce the contract's UNREACHABLE rules

`fetch_text` extracts text from any content type and silently truncates at
8 MiB + 1 byte, while the contract's verdict 3 makes a non-allowlisted content
type, a non-2xx final status and a body over 8 MiB `UNREACHABLE`.

```
        Content-Type: application/pdf   contract UNREACHABLE, reference extracts '<p>payload</p>'
        body 8 MiB + 64 bytes           contract UNREACHABLE, reference returns 8388606 chars
        status 302 without Location     contract UNREACHABLE, reference extracts the body
```

Live: all eight pages are `text/html`, status 200, well under 8 MiB (largest
decompressed body 1 171 528 bytes at S003), so not triggered. Relevance: the
48 page-sampled labels are derived through `fetch_text`, so a page that drifts
to a PDF or across the 8 MiB line would make the tool's contract-correct
`UNREACHABLE` disagree with a `VERBATIM`/`ABSENT` label.

### Dev-5 (latent) — redirects are not restricted to http and https

The contract's fetch bounds say "http and https only (redirects too)". The
reference adds no scheme filter; it relies on urllib, whose
`HTTPRedirectHandler` accepts a redirect whose scheme is in
`('http', 'https', 'ftp', '')`. Verified by reading
`inspect.getsource(urllib.request.HTTPRedirectHandler)`.

### Dev-6 (latent robustness) — raw DEFLATE raises instead of decoding

```
        Content-Encoding: deflate, RFC 1951 body (no zlib header)
counter   zlib.decompress(body) -> zlib.error: incorrect header check
```

A legal `Content-Encoding: deflate` body aborts the whole counter run rather
than yielding a label. The contract text is silent on compression, so this is
a robustness gap rather than a contract violation; recorded because the counter
sends `Accept-Encoding: gzip` and a server that answers raw deflate would break
the measurement.

### Notes that are not deviations

- **The `page_cases` alpha filter is stricter than `claims.md`.** The counter
  additionally skips a candidate window unless at least four of its tokens
  contain a letter (`sum(any(ch.isalpha() ...)) < 4`). `claims.md` says only
  "3 token windows of 6 to 20 tokens". This cannot mislabel: it only narrows
  which windows are sampled, and every sampled window is still checked with
  `found()` against both fetches. Its only effect is that a page of pure
  numerals or punctuation could fail to yield three windows and raise
  `ValueError` (counter exit 2, a failed measurement, never scored as a pass).
- **A self-closing block tag emits one space, not two.** `<br/>` gives one space
  via `handle_startendtag`; a strict "one space at start and end" reading gives
  two. The contract's whitespace collapse makes both `"a b"`, so this is
  immaterial (`test_self_closing_block_tag_space_count_is_immaterial_after_norm`).
- **`registry_url` reads `ln.split("|")[2]`.** That is the source cell only
  while the earlier cells hold no pipe. Verified: 0 of the 49 registry rows and
  0 of the 8 fixture rows have a pipe in the source cell, and each of the eight
  ids matches exactly one line, so the positional index agrees with the
  contract's "the row's `source` cell" everywhere it is exercised. This is a
  latent hazard, not an observed deviation.
- **An unclosed `<head>` drops the whole document** in both readings (the
  region never closes), so it is not a divergence. All eight pages close
  `<head>`.

## Risks

1. **Dev-2 and Dev-3 are content leaks, not whitespace leaks.** They leak whole
   words into the counter's page text. They are not triggered by the eight
   pages today, but the pages are live and can change between the counter's
   run and the tool's run. If S003 grows a stray drop end tag, a page window
   could be sampled from text the tool cannot see.
2. **The counter fetches the page and the tool fetches it independently.**
   `page_cases` labels a window `VERBATIM` when it is present in both of the
   counter's two fetches; the tool then fetches the same URL a third time. Any
   drift between those fetches is a mismatch the design accepts. This is
   inherent to the frozen design, not a reference-function deviation.
3. **Dev-4 means the reference's reachability decision can disagree with the
   tool's.** Today all eight pages are `text/html` 200 under 8 MiB.

## Limits

- I audited the six reference functions only. I did not audit the fixture, the
  counter's scoring loop, the receipt writer or `FROZEN_TOTAL`.
- The eight live pages were fetched once each on 2026-10-23 and cached under
  `_cache/`. Their content is a sample, not a guarantee for the data run.
- The `found` and `norm` fuzzers draw from a fixed alphabet with a fixed seed
  (20261023); they are evidence of agreement on that sample, not a proof.
- I did not run the counter, so I have no `QUOTE_REOPEN_MATCH` line of my own.
  Whether the counter's labels match a given tool is out of scope for this
  audit.
- My first oracle build lost the literal U+200B and reported a false S003
  divergence. That is corrected; the numbers above are from the corrected
  build, which rebuilds every special character with `chr()`.
- No tool was installed or updated.

## Reproduce

```
cd .ufo/waves/round-29/build/ExecToolSelfAudit
python3 check_contract_lists.py      # block/skip lists from claims.md vs counter: SETS-CONFORM
python3 audit_reference.py           # 72 unit checks: OK
python3 probe_materiality.py         # live token-stream equality: 0 of 8 differ
python3 probe_structure_hazards.py   # Dev-1/2/3 presence on the eight pages
```

Every script sets `sys.dont_write_bytecode = True`, so importing the committed
counter leaves no `__pycache__` in the lane tree.
