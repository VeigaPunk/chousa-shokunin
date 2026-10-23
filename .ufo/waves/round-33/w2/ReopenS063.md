# Reopen S063 — Python json docs (2026-10-23)

Attacked: S063 in `corpus/SOURCES.md:73` (body SHA-256, footer clock, section, the repeated-name quote once in tag-stripped text) and the Python sentence in `corpus/knowledge/claim-record-fields-r33.md:41-42`. GET only, host `docs.python.org`, no redirect followed. No install. No `c1-count` run (this item does not score the gate).

Verdict: **HOLDS**. No footer-clock variance.

## Fetch

Both GETs (scratch `/fast/scratch/hyaku/chousa-r33/w2/ReopenS063/`):

```sh
timeout 75 curl --proto '=https' --max-redirs 0 --max-time 60 --max-filesize 2097152 -sS \
  -D json-N.headers -o json-N.html \
  -w 'HTTP_STATUS=%{http_code}\nURL_EFFECTIVE=%{url_effective}\nSIZE_DOWNLOAD=%{size_download}\nREDIRECT_URL=%{redirect_url}\n' \
  https://docs.python.org/3/library/json.html
```

| GET | curl exit | HTTP | effective URL | bytes | redirect |
|---|---|---|---|---|---|
| 1 | 0 | 200 | `https://docs.python.org/3/library/json.html` | 115104 | empty |
| 2 | 0 | 200 | same | 115104 | empty |

```sh
sha256sum json-1.html json-2.html
# 5ceeeaf6b0c866bd413ac0a9316f92cd46e03984cfec87cf7ac051ca6235608b  both
cmp -s json-1.html json-2.html; echo CMP12=$?          # 0
cmp -s json-1.html .ufo/waves/round-33/w1/ScribeSourcePyJson/json-1.html; echo CMP_SCRIBE=$?  # 0
```

Recorded pin in `corpus/SOURCES.md:73` is `5ceeeaf6b0c866bd413ac0a9316f92cd46e03984cfec87cf7ac051ca6235608b`. Match.

Headers (copies in this directory: `json-1.headers`, `json-2.headers`): both `HTTP/2 200`, `last-modified: Fri, 23 Oct 2026 07:36:14 GMT`, `etag: "6adb0e6e-1c1a0"`, `content-length: 115104`, `date: Fri, 23 Oct 2026 09:00:37 GMT`, `age: 1978`. The scribe capture (`.ufo/waves/round-33/w1/ScribeSourcePyJson/json-1.headers:4-5,10-11`) had the same Last-Modified and ETag, `date: Fri, 23 Oct 2026 08:28:16 GMT`, `age: 37`. Cache age moved; the body did not.

## Footer clock

```sh
grep -oE 'Last updated[^<]+' json-1.html json-2.html
# both: Last updated on Oct 23, 2026 (07:34 UTC).
grep -cF 'Last updated on Oct 23, 2026 (07:34 UTC).' json-1.html   # 1, exit 0
grep -cF 'Last updated on Oct 23, 2026 (07:34 UTC).' json-2.html   # 1, exit 0
```

Same string the row records (`corpus/SOURCES.md:73`: `` footer `Last updated on Oct 23, 2026 (07:34 UTC)` (same timestamp and body in both GETs) ``). Variance this run: none. Variance against the row and against the L1 reopen (`.ufo/waves/round-33/measure/reopen-L1.txt:8`): none. Unlike S060, a later GET did not move the footer clock.

Page version: `<title>… Python 3.15.1 documentation</title>` (`json-1.html:20`) and `title="Search within Python 3.15.1 documentation"` (`json-1.html:34`). Matches the row's "Python 3.15.1".

## Quotes

Tag-strip: `html.parser.HTMLParser(convert_charrefs=True)`, `script`/`style`/`noscript` dropped, then whitespace runs squeezed to one space (`json-tag-stripped.txt`, sha256 `fbaea04d26c783bf321515101c82d5b4689a5b8b0f04c295793926adea0c08d5`). Newline-preserving strip: `json-tag-stripped-raw.txt`, sha256 `252fa660a4e8c3389fe1674fb75ce822d6ba823665f3d62c375560c8602555fa`. Both under the scratch dir.

| quote | squeezed `grep -cF` | raw strip `grep -cF` |
|---|---|---|
| `it ignores all but the last name-value pair for a given name` | 1 (exit 0) | 0 (exit 1) |
| `By default, this module does not raise an exception; instead, it ignores all but the last name-value pair for a given name:` | 1 (exit 0) | 0 (exit 1) |
| `The object_pairs_hook parameter can be used to alter this behavior.` | 1 (exit 0) | 1 (exit 0) |

The behavioral sentence is wrapped in the HTML (`json-1.html:900-902`): "it ignores all but" ends line 901 and "the last name-value pair…" starts line 902. A fixed-string search of the raw body or a newline-preserving strip does not see it. After the squeeze the row's method uses, it occurs once.

Section at that match: `h3:Repeated Names Within an Object` (`json-1.html:897-908`, `id="repeated-names-within-an-object"`). The heading text itself occurs 4 times (TOC, heading, and nav), not once. The sentence does not.

Located text, copied from that section (access 2026-10-23, https://docs.python.org/3/library/json.html#repeated-names-within-an-object):

> By default, this module does not raise an exception; instead, it ignores all but the last name-value pair for a given name:

Example on the next lines (`json-1.html:903-905`): `json.loads('{"x": 1, "x": 2, "x": 3}')` → `{'x': 3}`. Next paragraph (`json-1.html:908`):

> The object_pairs_hook parameter can be used to alter this behavior.

The preceding sentence says the RFC "does not mandate how repeated names in JSON objects should be handled" (`json-1.html:899-900`). A different section (`json-1.html:893-895`, Infinite and NaN) uses "alter this behavior" for `allow_nan` and `parse_constant`; that is not the `object_pairs_hook` sentence, which stays at count 1.

`object_pairs_hook` is a parameter of `json.load` (`json-1.html:459,478-483`) and of `json.loads` (`json-1.html:544`; the text says "Identical to load()"). The anchor in `corpus/SOURCES.md:73` matches.

### Per quote

1. Knowledge, `corpus/knowledge/claim-record-fields-r33.md:41-42`: "Python's decoder keeps the last: \"it ignores all but the last name-value pair for a given name\" (S063)." **HOLDS.** The quoted 12 words are the page's words, once, in that h3. "keeps the last" is not the page's verb; the page says "ignores all but the last", and the example retains `3`, the last value. [INFERENCE] that is the same claim, not an over-read. The page does not say a verifier must refuse duplicates; the entry's next sentence (`:43-45`) already says the fail-closed choice is the lane's, not the source's.
2. S063 teaches, `corpus/SOURCES.md:73`: "Python's default decoder ignores all but the last repeated object name-value pair; `object_pairs_hook` can alter that behavior." **HOLDS** as paraphrase. "this module" / `json.loads` default, object names, last pair kept; the hook sentence is verbatim in the same section. Scope ("not JSON's normative requirements") matches "does not mandate".
3. Section label "Repeated Names Within an Object" and the hash/footer/HTTP-200/3.15.1 anchor. **HOLDS**, with the heading-count and wrap limits above.

## Limits

- Contiguous-quote search without whitespace squeeze returns 0. That does not falsify the quote; it is how the paragraph is wrapped.
- Bodies stayed in scratch (115104 bytes each). This directory holds the two header files and this report.
- Not checked: whether a future docs rebuild moves the footer the way S060's did. This pair of GETs, and the comparison to the scribe body, did not.
