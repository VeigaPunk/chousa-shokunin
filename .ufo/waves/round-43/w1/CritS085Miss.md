# CritS085Miss — 参照日 is absent from the named article-page capture

Seat: leaf critic. Axes: operability, calibration, depth.
Measured commit: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
Attacked approach: the round-43 rejection sentence that the Japanese capture does not contain 参照日 (`corpus/lessons/round-43.md`, `corpus/SOURCES.md` line 250). Bound not retuned. No fetch. No production edit. No tool installed.

Assigned probe, answered first: in the committed capture of `https://www.jstage.jst.go.jp/article/jjsme/105/2/105_17/_article/-char/ja`, 参照日 is **absent**. Capture size of the text object the cache reader uses: **6333 bytes**.

## Axes

- operability: C1 enumerates the 15 round-42 `absent` ids. This URL is not one of them. A miss here must not be laundered into `ABSENT_ENUMERATED`.
- calibration: an unqualified "the Japanese capture" names one file. Two local captures of this article disagree (0 vs 4). The 1/2 bound is not involved.
- depth: the search-log stop rationale treats the Japanese sentence as ungroundable without a fetch. That saturates early if a committed text rendering already contains the quoted line. C3's admitted quote is a different capture and is not this probe.

## Assigned observation

Cache key is `sha256(url)[:24]`, the convention in `tools/quarantine-check.py` `cache_key` (line 142-143). `cache_doc` reads the `.txt`, not the `.raw`.

```text
URL https://www.jstage.jst.go.jp/article/jjsme/105/2/105_17/_article/-char/ja
KEY 02b3b0e812df68ca305c7bc3
TXT_PATH /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/02b3b0e812df68ca305c7bc3.txt
TXT_BYTES 6333
RAW_BYTES 67014
TXT_UTF8_SCALARS 4076
TXT_CRLF 534
NEEDLE 参照日
TXT_COUNT 0
RAW_COUNT 0
TXT_SHO 0
NFKC_COUNT 0
SHA256_TXT 5b04117c382313a08514cdf224efe3e1531eb09783814b8ebde0e3e519fbd046
SHA256_RAW a02ffd5ee8cd70ac01bde27556b2bfefe464721ee4a7af1315be6758f3db09fe
```

`wc -c` of those two files, verbatim:

```text
 6333 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/02b3b0e812df68ca305c7bc3.txt
67014 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/02b3b0e812df68ca305c7bc3.raw
73347 total
```

Size to score: **6333 bytes** (the `.txt`). The `.raw` is 67014 bytes of the same HTML (`<!DOCTYPE html`, `meta charset="utf-8"`), not a second article. 4076 is the UTF-8 scalar count with CRLF preserved; 534 CRLF pairs are why a universal-newline `len` prints 3542. Do not treat 3542 or 67014 as the text-capture size. The round-42 S077 erratum already separates bytes from Unicode scalars; this file is 6333 bytes and 4076 scalars.

Absence is not a fold miss. U+7167 照 occurs 0 times in both the `.txt` and the `.raw`. NFKC does not create it. No numeric-entity form of 参, 照, or 日 was present. The page is a bibliographic shell: title, ISSN 2434-8619, `書誌`, `p. 17-19`, `PDFをダウンロード (507K)`, `記事の1ページ目`. It is not p.19 of the article.

`git -C /home/vgpnk/Projects/shokuknow ls-files` on the `.txt` printed no path. "Committed capture" here means the campaign `.qcache` object the lane tools read, the same sense as the Europe PMC capture named in the round-43 lesson. This seat did not fetch.

## Counterexample

The strongest local counterexample is not a live page. It is the other cache object the same HTML already links.

Staged search log row 11 opened `https://www.jstage.jst.go.jp/article/jjsme/105/2/105_17/_pdf/-char/ja` with `pdftotext -layout` and called that **S087**. The article-page URL (this seat's assignment) is search-log row 20, the same staged id, marked identity only. Round-1 `S085` was remapped to staged `S087` (`lanes/chousa/ID-REMAP.md`). Current staged `S085` is a different URL (`ForPublishers/TAB2`); its capture `167e9db7dde3c998838e3469.txt` is 15656 bytes and also has 参照日 count 0. That zero is the wrong document. Do not attach this seat's file to current S085.

PDF text capture, same cache, not fetched this seat:

```text
PDF_URL https://www.jstage.jst.go.jp/article/jjsme/105/2/105_17/_pdf/-char/ja
PDF_KEY 58b1b5641ed80c3554e73727
PDF_TXT_BYTES 11682
PDF_RAW_BYTES 506589
PDF_RAW_MAGIC b'%PDF-1.6'
PDF_COUNT 4
PDF_HAS_TITLE True
PDF_QUOTE True
PDF_MUST True
```

Title shared with the article page: `論文執筆における引用の仕方，図表の転載，及び引用・参考文献の記載形式`.

Quoted spans in `58b1b5641ed80c3554e73727.txt` (UTF-8 offsets):

- offset 3802: `著者名（出版年）．文献名．URL（参照日） ※参照日の記載は必須とする．`
- offset 5888: `著者名（出版年）．文献名．URLと参照日 ※APAスタイルと異なり参照日の記載は必須とする．`

Those are the sentences `search-log-fields-r36.md` attributes to S087, and they are substrings of the PDF text capture. They are not substrings of `02b3b0e812df68ca305c7bc3.txt`.

So the lesson sentence is true only of the bibliographic shell and false of the capture that holds the article text. `corpus/lessons/round-43.md` and `corpus/SOURCES.md` say, without a filename: "the Japanese capture does not contain 参照日." That noun phrase is false provenance. The flip that a later fetch must supply "a capture of each cited source" is premature saturation: the Japanese sentence is already in the cache.

## What this does not falsify

The three-literatures entry still cites staged S077 / the PRISMA-S DOI, whose capture is the bot wall. This seat did not reopen that file. Rejecting the entry as written can survive on that ground alone. Frozen claims.md "Not claimed" states the bot wall and does not state the Japanese absence. C1 does not list this id. C2's 15/15 and the `--flip S086` kill do not read this cache object. C3's located quote is the Europe PMC sentence in `2cef078d8f9f87802e19e770.txt`, not 参照日.

Admitting the entry while it still cites the HTML URL would repeat the defect: the quote would not be a substring of the cited URL's capture. That is the C3 kill shape, applied to a different row. Do not "fix" it by pointing the HTML URL at the PDF bytes.

## Impacted axes

- operability: no miss. Assigned capture is readable, keyed, and reproducible. Not a C1 fail. Not an empty class. Not an id added or dropped from the 15.
- calibration: fixable defect in the rejection prose, not in `absent-split.tsv`. Two captures, one unqualified sentence. L1 per-axis verdicts must not fail C2, and must not retune 1/2, on this probe.
- depth: fixable defect in the stop rationale. The Japanese sentence is locally re-groundable from the PDF text capture. The three-source entry is not, because of the bot wall. L1 must not fail C3. L1 must not treat "Japanese capture lacks 参照日" as a measured fact about the article text.

Tradeoff the scored verdicts must not reject: keeping `search-log-fields-r36.md` out because one of its three cited sources is a bot wall. That is a scope choice the bot-wall evidence supports. The false clause is the extra conjunct.

## Smallest safe correction

Append an erratum. Do not rewrite frozen predicates. Do not fetch. Do not retune the bound. Do not edit the split table. Do not admit the three-source entry. Do not cite the article-page URL as the carrier of 参照日.

Replacement clause: the cited article-page capture `02b3b0e812df68ca305c7bc3.txt` is 6333 bytes and does not contain 参照日 (照 count 0). The committed pdftotext capture `58b1b5641ed80c3554e73727.txt` is 11682 bytes and contains it 4 times, including `著者名（出版年）．文献名．URL（参照日）` and `参照日の記載は必須とする`. A later citation of that sentence must name the PDF URL, not the article-page URL, and not current S085.

## Verdict

Assigned search: **absent**. Capture size: **6333 bytes** (text), raw response 67014 bytes. The lesson's unqualified Japanese-absence sentence does not survive the PDF text capture already in the same cache.

Report: .ufo/waves/round-43/w1/CritS085Miss.md
