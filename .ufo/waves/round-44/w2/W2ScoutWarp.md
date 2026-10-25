# W2ScoutWarp

Axes: operability, calibration, depth.

Verdict: the WARP capture is the NDL WARP FAQ, not a bot wall. No fetch.

## One line

From `5f54e82c87a76eefdc9a0d35.txt` line 143, `repr` `' Frequently Asked Questions about WARP\n'`:

```
 Frequently Asked Questions about WARP
```

A challenge page would be a Client Challenge / Just a moment interstitial. This line is the FAQ heading.

## Identity (local hash, not a fetch)

URL named for this capture: `https://warp.ndl.go.jp/en/info/qanda`.

```
 1123 28659 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/5f54e82c87a76eefdc9a0d35.txt
5f54e82c87a76eefdc9a0d358310adf805e10f14f02372c6697749c86b7d7416
5f54e82c87a76eefdc9a0d35
```

```
path /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/5f54e82c87a76eefdc9a0d35.txt
exists True
bytes 28659
sha256_file a7e46e274b0784f81426bdc602785b03db1fa87f8f34916097d42ff36cac8dc8
url https://warp.ndl.go.jp/en/info/qanda
sha256_url_24 5f54e82c87a76eefdc9a0d35
filename_stem 5f54e82c87a76eefdc9a0d35
stem_eq_url_prefix True
```

Filename stem equals `sha256(url.encode()).hexdigest()[:24]`. File digest above is the capture bytes, not the URL digest.

Sibling raw, same stem, same mtime:

```
-rw-r--r-- 1 vgpnk vgpnk 55951 Oct 23 20:36 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/5f54e82c87a76eefdc9a0d35.raw
-rw-r--r-- 1 vgpnk vgpnk 28659 Oct 23 20:36 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/5f54e82c87a76eefdc9a0d35.txt
```

Raw agrees. Title is NDL; h1 is the same FAQ heading the txt line extracts:

```
5f54e82c87a76eefdc9a0d35.raw:5:    <title>NDL Web Archiving Project (WARP)</title>
5f54e82c87a76eefdc9a0d35.raw:128:<h1 class="emb-title warp-h1">Frequently Asked Questions about WARP</h1>
```

First nonempty txt line is the same title, not a wall: `' NDL Web Archiving Project (WARP) '`.

## Not a bot wall

Markers from `tools/quarantine-check.py` `INTERSTITIAL_MARKERS`, counted in the txt (full file):

```
marker_hits_full none
marker_hits_head4000 none
client_challenge_present False
count 'client challenge' 0
count 'just a moment' 0
count 'cf-browser-verification' 0
count 'attention required' 0
count 'enable javascript and cookies to continue' 0
count 'checking your browser before accessing' 0
count 'error 1020' 0
count 'access denied' 0
count 'captcha' 0
count 'verify you are human' 0
count 'robot check' 0
count 'checking your browser' 0
count 'request blocked' 0
count 'unusual traffic' 0
```

The head is a cookie consent block (`' Our use of Cookies on NDL Web Archiving Project (WARP)'`), not a challenge. Consent text is not an interstitial marker. The FAQ heading is inside the first 4000 characters, so a head-only `capture_kind` window sees it and would return `page`. That negative (no marker) is not the identification. The heading is.

FAQ body is also present. `National institution websites are archived once per month` is a contiguous substring at byte offset 6525. That sentence is answer text, not a wall.

## Calibration

- Byte offset of the heading is 1468; character offset is 1464. The +4 is two fullwidth parentheses earlier in the cookie sentence (`U+FF08` and `U+FF09`, 3 bytes each). Do not treat 1464 and 1468 as a mismatch.
- mtime is before this round. Opening the file is not a freshness improvement.

```
2026-10-23 20:36:10.486713407 -0300 28659 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/5f54e82c87a76eefdc9a0d35.txt
```

No network. No production edit. No package install.
