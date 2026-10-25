# W2ReviewWarp — round 44, wave 2

Seat: confirm `National institution websites are archived once per month` is contiguous in qcache file `5f54e82c87a76eefdc9a0d35.txt`, and report the offset. No fetch. Recommendation only; no production file was edited.

Axes: operability (the named file opens and the span is a unique exact run), calibration (file-byte index versus a decoded code-point index, versus the `.raw` body, versus the line start), depth (URL binding, extractor versus text node, and what this offset does not score).

## Answer

**Contiguous: yes. Byte offset: 6525** (0-based index into the `.txt` bytes; one hit; 57 bytes; exclusive end 6582).

The span is ASCII. Its own byte length equals its code-point length. The start index does not. A decoded `str.find` returns **6425**. That is not a seek offset into this file. `dd skip=6425` lands in an earlier sentence. `dd skip=6525 count=57` returns the phrase.

Do not substitute **20462**. That is the same phrase in the sibling `.raw` (55,951 bytes), a different object.

## Evidence

Local only. No curl, wget, or fetch. Capture path:

`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/5f54e82c87a76eefdc9a0d35.txt`

```
=== stat txt ===
size=28659 mtime=2026-10-23 20:36:10.486713407 -0300
=== sha256 txt ===
a7e46e274b0784f81426bdc602785b03db1fa87f8f34916097d42ff36cac8dc8  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/5f54e82c87a76eefdc9a0d35.txt
=== grep -abo ===
6525:National institution websites are archived once per month
=== dd skip 6525 count 57 ===
National institution websites are archived once per month
=== dd skip 6425 count 40 ===
 events, online periodicals, and similar
=== dd skip 6524 count 12 ===
 National in
```

Python on the same bytes: `txt_offset 6525`, `end_excl 6582`, `count 1`, `prev_byte 0x20`, `next_byte 0x2c`, `span_ascii True`, `internal_newline False`, `internal_tab False`, `double_space False`. A 40-byte-gap pattern over the eight words also hit once, at 6525, with gap 0. `once per month` occurs once. The same line later has `archived once per year` (byte 6711); that is not a second copy of this phrase.

Line: 418 (1-based; 417 LF bytes before the hit). Line byte start is 6524. The line begins with one space, so the phrase is column 1 of that line, not column 0. A 1-based byte index would be 6526 and is also the wrong seek.

## Calibration

The 100-byte gap (6525 − 6425) is 50 non-ASCII code points before the hit, each UTF-8 length 3, so 100 extra bytes:

- U+3000 ideographic space ×48
- U+FF08 fullwidth `（` ×1
- U+FF09 fullwidth `）` ×1

`wc` agrees the file is not byte-equal to its decoded length: `1123 28542 28659` (lines, characters, bytes). `file` reports UTF-8. CR count 0, NUL count 0, so the offset is not a CRLF artifact.

Filename binding, local `sha256` of the URL string, first 24 hex digits, the same rule as `quote-lint.py` `cache_path` and `c3-count.py`:

```
MATCH 5f54e82c87a76eefdc9a0d35 https://warp.ndl.go.jp/en/info/qanda
miss  48dd800300156abe7f43f70d https://warp.ndl.go.jp/en/info/qanda/
miss  002505023b68a00b1a30b382 http://warp.ndl.go.jp/en/info/qanda
```

The unsuffixed HTTPS URL matches. A trailing slash does not. This seat did not re-fetch that URL.

`.txt` is not the HTTP body. `quote-lint.py` `html_to_text` strips tags and collapses spaces, so a `.txt`-only hit can be manufactured. That did not happen here. The sibling `.raw` (size 55951, sha256 `7c9dc42995fa46b1470cdf19ee6c3711c1d3f879630c27a080fb51c3c0019aec`, same mtime second) contains the phrase once at byte **20462**, immediately after `\n        <p>`, followed by `, and th`. No `<` occurs between that start and `</p>` at raw byte 20874. The 57 bytes are one HTML text node, not a join across tags.

The longer proposed cadence sentence (209 bytes, through `once per year.`) is also one contiguous run, starting at the same offsets: txt 6525, raw 20462, count 1 in each file. This seat's assigned phrase is the first 57 bytes of that run.

No published numeric locator for this phrase was found to refute. The assimilation draft at `.ufo/waves/round-44/assimilation/draft/citation-version-binding-r37.md` pins this `.txt` digest (`a7e46e27…c8dc8`) and says "byte offset of the committed capture" without a number. The number for that digest is 6525, not 20462 and not 6425. This seat did not fill that draft.

## What this does not establish

- Frozen R44-C3 does not read this file or this quote. C3's quote is `constitutes a promise that the resource state` in the RFC 7089 capture. This confirm is not a C3 score.
- The offset is not a freshness check. The file mtime is 2026-10-23 20:36:10 -0300, before this round's 2026-10-24 seats. Opening it does not show the live page still says this.
- It is not a Client Challenge page. The `.txt` begins with `NDL Web Archiving Project (WARP)`. That identifies the extraction; it does not re-prove the origin.
- Eight words, under a 25-word cap, is a count only. Contiguity does not make the FAQ a Memento header or a version-binding protocol.

## Residual

The qcache directory is outside this lane repo. If `5f54e82c87a76eefdc9a0d35.txt` is absent, offset 6525 is not reproducible from the lane tree. The digest above is the pin. No shokuknow file, lane production file, git index, or jj state was modified.

Report: .ufo/waves/round-44/w2/W2ReviewWarp.md
