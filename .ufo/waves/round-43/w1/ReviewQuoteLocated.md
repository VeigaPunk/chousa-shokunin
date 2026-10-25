# ReviewQuoteLocated — round 43, wave 1

Seat: locate `to register the steps taken and to make searches accountable and reproducible` in the committed capture `2cef078d8f9f87802e19e770.txt` and report the byte offset. No fetch. Recommendation only; no production file was edited.

Axes: operability (the named capture opens and the span is unique), calibration (file-byte index versus a decoded code-point index), depth (identity of that capture, section enclosure, and whether the frozen C3 predicate even checks the offset).

## Answer

**Byte offset: 17410** (0-based index into the file bytes; one hit; 77 bytes; ASCII, so the span's own byte length equals its code-point length).

The published locator **17383 is not the byte offset**. It is the 0-based Unicode code-point index of the same start after UTF-8 decode. The gap is 27 bytes, from 14 non-ASCII code points earlier in the file. A seek to byte 17383 lands inside `ly in the database itself, `, 27 bytes before the sentence.

## Findings by severity

### Medium — published "byte offset 17383" is a code-point index

Measured commit `737f40b6aa8f37ffe2269db370fd6d65a720d9a8` (lane HEAD; those three files have no working-tree diff) states byte offset 17383 in four places:

- `corpus/knowledge/search-log-method-r39.md:3`
- `corpus/knowledge/search-log-method-r39.md:10`
- `corpus/lessons/round-43.md:37`
- `corpus/SOURCES.md:88` (anchor cell)

Evidence, commands run against the on-disk capture, output verbatim:

```
=== sha256sum ===
833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/2cef078d8f9f87802e19e770.txt
=== wc -c ===
80107 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/2cef078d8f9f87802e19e770.txt
=== grep -abo ===
17410:to register the steps taken and to make searches accountable and reproducible
=== dd skip 17410 count 77 ===
to register the steps taken and to make searches accountable and reproducible
=== dd skip 17383 count 40 ===
ly in the database itself, to register t
=== python ===
2cef078d8f9f87802e19e770
```

`grep -abo` and `dd skip=17410 count=77` agree. `dd skip=17383` does not start at the sentence. A 1-based reading does not rescue 17383 either: 1-based byte would be 17411; 1-based code point would be 17384.

Mechanism: the file is UTF-8 (declared `encoding="UTF-8"`; 80107 bytes, 79840 code points). Before the match there are 14 non-ASCII code points (en dashes U+2013, copyright U+00A9, curly quotes U+201C/U+201D, apostrophe U+2019). They add 27 bytes. `str.find` on the decoded text returns 17383; `bytes.find` / `grep -b` return 17410. That is the same char/byte split the round-42 erratum already recorded for S077 (265 Unicode characters, 267 bytes, `corpus/lessons/round-42.md:151-153`). This locator repeats the class and then calls the character index a byte offset.

The sentence is unique in this file. It is followed immediately by `.` at byte 17487. The 12-word span the lesson quotes starts at 17410 either with or without that period. It sits inside the article's section 6: title `<title>6. Document the search process in a text document</title>` at byte 17216, enclosing `</sec>` at byte 17800. XML id is `sec10`; the article's own heading number is 6. "Section 6" is a fair description of the heading, not a claim that the XML id is `sec6`.

Recommendation: do not treat this as a failed frozen C3 (see below). Do not rewrite the four sentences in place. An append-only erratum, on the round-42 pattern, should cite both numbers: file byte 17410, decoded code-point index 17383. This seat did not apply that edit.

### Low — bibliographic tail "531-539" is not in the cited capture

Same source line (`search-log-method-r39.md:3`) ends `J Med Libr Assoc 2018;106(4):531-539`. In the capture front matter (`</front>` at byte 6393):

- `<volume>106</volume><issue>4</issue><fpage>531</fpage><page-range>531–541</page-range>` is present (en dash, U+2013).
- `10.5195/jmla.2018.283` is present (byte 760).
- The token `539` does not occur in the front matter. `531-539` and `531–539` do not occur in the file.

This is outside the frozen C3 predicate and outside a live journal-page check (fetch forbidden). Relative to the capture the row cites, the page end 539 is unsupported; the capture's own page-range is 531–541. Not adjudicated against any other rendering.

## What holds

- Canonical capture for the Europe PMC URL. `sha256(url)[:24]` is `2cef078d8f9f87802e19e770`, matching the filename. File sha256 matches the digest named in the entry, the lesson, and the S078 row: `833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d`. `.txt` and `.raw` are byte-identical (same size, same digest). No second rendering, no reroute.
- Frozen C3 does not read the offset. `corpus/evidence/round43/c3-count.py` sets `located` by substring membership (`QUOTE in capture.read_text(...)`). Live rerun:

```
ENTRY_CITES=1/1
QUOTE_LOCATED=1/1
URL_MATCH=1/1
C3=PASS
EXIT:0
```

A counter that only asks "is the quote a substring" cannot see this defect. C3=PASS is not evidence that byte 17383 is the start of the sentence.

## Residual risk and verification gaps

- The qcache path is gitignored in shokuknow (`.gitignore:5` ignores `.ufo/waves/corpus-expansion-1/.qcache/`). "Committed capture" here means the campaign file on disk that `c3-count.py` opens, not a git blob. No git object id was available to pin. No fetch was used to replace it. If that file is absent, the offset is not reproducible from the lane repo alone.
- No network, no curl, no wget, no shokuknow tool. Live-web identity of the article was not checked. Claims already exclude live-web truth.
- C1 and C2 were not rerun on this seat. R43-SPLIT was not retuned.
- `.txt` equals `.raw`, so this pair has no alternate offset. A different extraction (tags stripped, NFKC) was not what the published number matches; the published number matches decoded `str.find` on the whole file, not a stripped text.
- This seat wrote only this report. The capture and the lane tree were not mutated.

Report: .ufo/waves/round-43/w1/ReviewQuoteLocated.md
