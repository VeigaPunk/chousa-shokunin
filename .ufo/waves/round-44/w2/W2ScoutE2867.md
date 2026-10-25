# W2ScoutE2867

Axes: operability, calibration, depth.

Verdict: yes. The title area of qcache file `0034b800811072de3980e85b.txt` is NDL Current Awareness Portal note E2867, 「国立国会図書館インターネット資料収集保存事業（WARP）のウェブサービスリニューアル」. It is not a Client Challenge page. It is not E2868 or E2873. Those ids appear later as sibling links, not as the document title.

No fetch. No production edit. Frozen claims in `corpus/evidence/round44/claims.md` do not mention E2867 (string find returned -1) and are not retuned here. The capture's mtime is 2026-10-23, before this round; that is not a freshness improvement.

## Title area

Assigned file, read locally:

`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0034b800811072de3980e85b.txt`

The extract has no `<title` tag (`find` returned -1). Lines 1–44 are whitespace. The title area is the first non-blank line, line 45, byte offset 81. A first-20-lines read would miss it. The dash is U+2013 EN DASH, not hyphen-minus. The line has one leading space and one trailing space, then LF.

```
 E2867 – 国立国会図書館インターネット資料収集保存事業（WARP）のウェブサービスリニューアル | カレントアウェアネス・ポータル 
```

`repr` of that line:

```
' E2867 – 国立国会図書館インターネット資料収集保存事業（WARP）のウェブサービスリニューアル | カレントアウェアネス・ポータル '
```

`E2867` itself starts at byte 82. After strip, the line starts with `E2867`.

The same heading is repeated in the body without the portal suffix, line 270, byte 1767:

```
 E2867 – 国立国会図書館インターネット資料収集保存事業（WARP）のウェブサービスリニューアル
```

Line 312 is the bare id ` E2867`. Those three lines, plus the breadcrumb range on line 255, are the only `E2867` hits in the `.txt` (lines 45, 255, 270, 312). Lowercase `e2867` occurs 0 times in the `.txt`.

The breadcrumb is a range, not a second article:

```
 ホーム » カレントアウェアネス-E » 2026年　（通号No.516-： E2854-） » No.519 （E2867-E2869） 2026.02.26 
```

Sibling links in the same issue nav, not the title:

```
 E2873 – 第50回ISSNセンター長会議＜報告＞
 E2868 – 意味に基づく多言語学術資源検索手法に関するCOARによる報告書
```

## Why the filename agrees, and what it does not prove

`tools/quarantine-check.py` lines 23–24 state the cache key convention: `sha256(url)[:24] + ".txt"`. Local hash, no fetch:

```
url https://current.ndl.go.jp/e2867
url_sha256 0034b800811072de3980e85b94545859d4d38f9e50ee53f20eda5a66b28be8d5
filename_stem 0034b800811072de3980e85b
stem_is_url_sha256_prefix24 True
```

The stem is not a prefix of the file digest (`d2a58e70eb8a2b4e42836c0b3df5035c67a45bbce71c412cbcd2bfb155d4848f`). That is expected: the key is the URL, not the bytes. Variants with a trailing slash, `http://`, or uppercase `E2867` do not match the stem. The `.txt` does not itself contain the URL string.

Cross-check only, companion `.raw` (344664 bytes), not the assigned quote file. Its `<title>` at offset 2253 is `E2867 &#8211; … | カレントアウェアネス・ポータル`. `html.unescape` of that entity string equals the stripped line 45 (`TITLES_MATCH_AFTER_UNESCAPE True`). Canonical link: `href="https://current.ndl.go.jp/e2867"`. The note headline is `h1.entry-title`, not the earlier site-logo `h1`.

## Not a wall

`Client Challenge` and `Just a moment` are absent (`find` -1). The extract is 13942 bytes and 840 newlines, not a short challenge page. `file` reports one CRLF among LF terminators (`crlf` count 1). The title line is LF, not that CRLF.

## Command output

`ls -la`, `file`, `wc -c -l`:

```
-rw-r--r-- 1 vgpnk vgpnk 13942 Oct 23 20:36 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0034b800811072de3980e85b.txt
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0034b800811072de3980e85b.txt: Unicode text, UTF-8 text, with CRLF, LF line terminators
  840 13942 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0034b800811072de3980e85b.txt
```

Identity probe (`python3`, UTF-8 decode, `hashlib.sha256`, no network), exit 0:

```
path /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0034b800811072de3980e85b.txt
bytes 13942
lf_segments 841
crlf 1
first_nonblank_line 45
line45_repr ' E2867 – 国立国会図書館インターネット資料収集保存事業（WARP）のウェブサービスリニューアル | カレントアウェアネス・ポータル '
line45_startswith_E2867_after_strip True
dash_codepoints ['0x2013']
line45_byte_offset 81
E2867_byte_offset 82
url https://current.ndl.go.jp/e2867
url_sha256 0034b800811072de3980e85b94545859d4d38f9e50ee53f20eda5a66b28be8d5
filename_stem 0034b800811072de3980e85b
stem_is_url_sha256_prefix24 True
file_sha256 d2a58e70eb8a2b4e42836c0b3df5035c67a45bbce71c412cbcd2bfb155d4848f
stem_is_file_sha256_prefix24 False
find 'Client Challenge' -1
find 'Just a moment' -1
find '<title' -1
E2867_line_numbers [45, 255, 270, 312]
e2867_count 0
```

`lf_segments 841` is `split("\n")` on a file that ends in a newline. `wc -l` and the Read tool both count 840 lines. Line 45 is the same under both counts.

Report: .ufo/waves/round-44/w2/W2ScoutE2867.md
