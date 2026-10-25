# W2ReviewRfc — round 44, wave 2

Seat: locate the contiguous quote `constitutes a promise that the resource state` in the RFC 7089 capture `d0c4a09a9de32cb91d5e3797.txt` under `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` and report the byte offset. No fetch. Recommendation only; no production file was edited.

Axes: operability (the named capture opens and the span is unique), calibration (0-based file-byte index versus a 1-based index, a decoded code-point index, and a wrapped full sentence), depth (capture identity, section enclosure, and whether frozen C3 even checks the offset).

## Answer

**Byte offset: 14896** (0-based index into the file bytes; one hit; 45 bytes).

The file is ASCII (`file -b` reports `ASCII text`; 0 bytes ≥ 128). The 0-based Unicode code-point index of the same start is also 14896. The gap is 0. This is not the round-43 class, where a published "byte offset" was a code-point index 27 bytes earlier.

A 1-based reading does not move the number onto the quote either. 1-based byte would be 14897, which starts at `onstitutes`. The byte before 14896 is a space.

## Evidence

Commands run against the on-disk capture. No network, no curl, no wget.

```
=== sha256sum txt ===
c3c7b7f2c495dce0fad758dac34dcc1eef3623d13c9ef346e19b30dbbbe801dc  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt
=== sha256sum raw ===
c3c7b7f2c495dce0fad758dac34dcc1eef3623d13c9ef346e19b30dbbbe801dc  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.raw
=== wc -c ===
107130 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt
107130 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.raw
=== cmp txt raw ===
cmp_exit=0
=== stat mtime ===
2026-10-23 20:33:05.526350588 -0300 107130 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt
2026-10-23 20:33:05.524186651 -0300 107130 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.raw
=== file ===
ASCII text
=== url sha256 prefix ===
d0c4a09a9de32cb91d5e37971b546f2c380d0a60581c6bb80fb9ef72d97743d0
d0c4a09a9de32cb91d5e3797
=== grep -abo ===
14896:constitutes a promise that the resource state
grep_exit=0
=== grep -c ===
1
=== dd skip 14896 count 45 ===
constitutes a promise that the resource state
=== dd skip=14895 count=46 ===
 constitutes a promise that the resource state
=== dd skip=14897 count=44 ===
onstitutes a promise that the resource state
=== dd skip=14941 count=12 ===
b'\n   reflecte'
```

Python on the same bytes (the two prints `crlf_file=False` and `nul=False` from this first script are discarded: those literals were over-escaped and do not test CR LF or NUL; the rerun below does):

```
bytes=107130
codepoints=107130
byte_offset=14896
codepoint_index=14896
gap=0
non_ascii_before=0
cr_before=0
lf_before=380
quote_bytes=45
occurrences=1
line_start_byte=14876
line_end_byte=14941
col_in_line=20
LINE=   a given response constitutes a promise that the resource state
wrapped_sentence_contiguous=False
client_challenge=False
rfc_line=True
```

Rerun for the discarded checks, plus newline and form-feed counts before byte 14896:

```
cr_total 0
nul_total 0
high_bytes 0
endswith_nl True
newlines_before 380
formfeeds_before 6
1based_line 381
```

`grep -abo` and `dd skip=14896 count=45` agree. `dd skip=14897` does not start at the quote. Exclusive end is 14941; the next byte is LF, then three spaces and `reflecte` (the wrap of `reflected`).

The span is line 381, 0-based column 20 on that line (three spaces plus `a given response `). Six form-feeds precede it. Each is one ASCII byte, so they do not open a byte/code-point gap, and they are not LF, so they do not change the newline line number.

## Findings by severity

### Low — the frozen quote is one line; the surrounding sentence is not a contiguous substring

The capture wraps the sentence (lines 380–382):

```
   The presence of a "Memento-Datetime" header and associated value for
   a given response constitutes a promise that the resource state
   reflected in the response will no longer change (see Section 4.5.6).
```

`constitutes a promise that the resource state` sits entirely on line 381 and is a contiguous 45-byte span. The longer string `a given response constitutes a promise that the resource state reflected` is not a contiguous substring (`wrapped_sentence_contiguous=False`). A later row that pastes the whole sentence, including the words across the wrap, would miss C3's substring check even though this 7-word quote hits. Construction already froze the contiguous span (`corpus/evidence/round44/claims.md` lines 99–101). This seat did not rewrite it.

Word count of the frozen quote is 7, which is at most 25. That count is a side measurement on this seat, not the W2ExecWords result.

### Info — C3 does not check the offset, and the live counter does not currently open the capture

`corpus/evidence/round44/c3-count.py` sets `located` by substring membership (`QUOTE in capture.read_text(...)`) and only after the entry file exists. It never reads a byte offset. Live default run:

```
ENTRY_CITES=0/1
QUOTE_LOCATED=0/1
URL_MATCH=0/1
C3=FAIL entry-missing
c3_exit=1
```

That FAIL is the missing-entry printer (`c3-count.py` returns before the capture read). It is the same shape claims.md names for the do-nothing control. It is not evidence that the quote is absent, and it is not a C3 pass. The entry path does not exist:

```
ls: cannot access '/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/citation-version-binding-r36.md': No such file or directory
```

No `S079` row-start is in `corpus/SOURCES.md` (corpus grep for `S079` hits `claims.md` only). A counter that only asks "is the quote a substring, once an entry exists" cannot see this offset. C3=PASS, when it eventually holds, will not be evidence that byte 14896 is the start.

No published locator in the lane tree names 14896 or a rival number for this quote. There is nothing here to erratum the way round 43 erratumed 17383. If a later scribe writes an anchor, the file-byte number is 14896, not 14897.

## What holds

- The quote occurs once. `grep -c` is 1. `bytes.find` count is 1. The word `promise` occurs three times, at bytes 14910 (inside this span), 58333 (line 1474: `Providing this value includes a promise that the resource has not`), and 71465 (line 1831: `entails a promise that`). Those other two are not the frozen quote.
- Section enclosure: body heading `2.1.1.  Accept-Datetime and Memento-Datetime` at byte 13866 (line 359); next section `2.1.2.  Vary` at byte 16414 (line 419). The quote at 14896 is inside 2.1.1. The sentence's cross-reference to Section 4.5.6 is a real heading at line 1827 (`4.5.6.  Sticky "Memento-Datetime" and "original" Link for Mementos`). That section restates the idea in different words (`entails a promise that the response is archived, frozen in time`). It does not repeat the frozen span.
- Capture identity. `sha256(https://www.rfc-editor.org/rfc/rfc7089.txt)[:24]` is `d0c4a09a9de32cb91d5e3797`, matching the filename. Line 8 is `Request for Comments: 7089`. `Client Challenge` / `Just a moment` are absent. `.txt` and `.raw` are byte-identical (same size, same digest, `cmp` exit 0). No second rendering.
- File digest of both renderings: `c3c7b7f2c495dce0fad758dac34dcc1eef3623d13c9ef346e19b30dbbbe801dc`. Claims.md does not publish this digest; this seat measured it. It is not a C3 input.
- Opening this file is not a freshness improvement. mtime is `2026-10-23 20:33:05 -0300`. Claims.md lines 13–14 already say freshness is not a claim and a pre-round capture open is not a freshness improvement. This seat did not fetch a newer copy.

## Residual risk and verification gaps

- The qcache path is gitignored in shokuknow. `git -C /home/vgpnk/Projects/shokuknow check-ignore -v` printed `.gitignore:5:.ufo/waves/corpus-expansion-1/.qcache/` for this file. "Committed capture" in claims.md means the campaign file `c3-count.py` opens, not a git blob. No git object id pins these bytes. If the file is absent, the offset is not reproducible from the lane repo alone.
- No live-web check. Claims already exclude live-web truth. This seat did not fetch.
- C1 and C2 were not rerun here. The C3 script was run only to show that its current FAIL does not read the offset.
- A first script's `crlf_file` and `nul` prints are not evidence. The rerun is: `cr_total 0`, `nul_total 0`.
- This seat wrote only this report. The capture and the lane tree were not mutated.

Report: .ufo/waves/round-44/w2/W2ReviewRfc.md
