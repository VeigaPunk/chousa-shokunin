# W2ScoutRfc

Axes: operability, calibration, depth.

Verdict: the RFC 7089 capture is not a Client Challenge page.

## Request for Comments line

File: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt`

Newline-delimited line 8, the only line containing `Request for Comments`. Sixteen spaces sit between `7089` and `Los Alamos`. No leading space. Trailing newline, no carriage return.

```
Request for Comments: 7089                Los Alamos National Laboratory
```

Python `repr` of that line, including the newline:

```
'Request for Comments: 7089                Los Alamos National Laboratory\n'
```

The first six lines are empty. The first non-empty line is line 7, `Independent Submission                                  H. Van de Sompel`, not `Client Challenge`.

## Identity

This is the capture named by `corpus/evidence/round44/claims.md` (sha256 of the URL, first 24 hex digits). Checked locally. No fetch.

```
d0c4a09a9de32cb91d5e37971b546f2c380d0a60581c6bb80fb9ef72d97743d0
d0c4a09a9de32cb91d5e3797
filename_match True
```

URL hashed: `https://www.rfc-editor.org/rfc/rfc7089.txt`. `tools/quarantine-check.py` `cache_key` returns the same 24 digits. That identifies the cache key. It does not prove these bytes still match a live fetch.

```
ASCII text
  2803 107130 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt
-rw-r--r-- 1 vgpnk vgpnk 107130 Oct 23 20:33 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt
```

Decoded UTF-8 length is also 107130. The file is ASCII, ends with a newline, and contains no NUL and no CR. `wc -l` is 2803. Python `splitlines()` is 2853 because the body has 50 form feeds (`0x0c`), which `splitlines` treats as breaks and `wc -l` does not. Those form feeds are not in the header, so line 8 is the Request for Comments line under both counts.

The sibling `d0c4a09a9de32cb91d5e3797.raw` is byte-identical (`cmp` exit 0). Same sha256: `c3c7b7f2c495dce0fad758dac34dcc1eef3623d13c9ef346e19b30dbbbe801dc`. The raw head is the same RFC header, not an HTTP status line and not HTML.

## Not a Client Challenge page

A Client Challenge capture in this cache is a short HTML interstitial whose first non-empty line is `Client Challenge` (see `.ufo/waves/round-43/w1/CritBotWall.md` on `01f657b3d0ab045c494b3f92.txt`). This file is not that form.

`tools/quarantine-check.py` `capture_kind` reads the first 4000 characters for `INTERSTITIAL_MARKERS`, including `client challenge`. On this text it returns `page`, which in that function means "no interstitial marker in the head," not "this is an HTML page."

```
capture_kind page
cache_key d0c4a09a9de32cb91d5e3797
marker_count 19
```

The same markers were also scanned over the whole file, not only the 4000-character window. Every one was absent in both ranges, including `client challenge`, `just a moment`, `cf-browser-verification`, `attention required`, `captcha`, `verify you are human`, and `enable javascript and cookies to continue`. `<!doctype html>` and `<title>client challenge</title>` are absent from the head. The raw sibling has the same absences.

So: not a Client Challenge page, not an HTML bot wall, and not classified as an interstitial. It is the ASCII text of RFC 7089, header included.

No lane production file was modified. No network.

Report: .ufo/waves/round-44/w2/W2ScoutRfc.md
