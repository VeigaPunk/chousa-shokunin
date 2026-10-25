# R51GroundJaohfaB — independent second pass, staged S110 (JAOHFA reporting form)

Seat R51GroundJaohfaB (scribe; leaf, no dispatch). Document: staged S110, planned lane id S108,
`https://jaohfa.com/pdf/systematic_review.pdf`. I did not open `R51GroundJaohfaA.md` or any other seat's
report, ran no counter, fetched nothing, and wrote nothing outside this file.

## Capture and text form

```
$ ls -l .qcache/62be15a474e866e4bef6c9d5.*
-rw-r--r-- 1 vgpnk vgpnk 291615 Oct 23 20:38 62be15a474e866e4bef6c9d5.pdf
-rw-r--r-- 1 vgpnk vgpnk 291615 Oct 23 20:38 62be15a474e866e4bef6c9d5.raw
-rw-r--r-- 1 vgpnk vgpnk  61188 Oct 23 20:38 62be15a474e866e4bef6c9d5.txt
$ file 62be15a474e866e4bef6c9d5.raw 62be15a474e866e4bef6c9d5.txt
62be15a474e866e4bef6c9d5.raw: PDF document, version 1.6 (zip deflate encoded)
62be15a474e866e4bef6c9d5.txt: Unicode text, UTF-8 text
$ pdftotext -layout 62be15a474e866e4bef6c9d5.raw repro.txt && sha256sum repro.txt 62be15a474e866e4bef6c9d5.txt
960da5cf632dbd278ea941c54d83e3ed8f13657bcb4bcbbfc8d63c9d834acf4a  repro.txt
960da5cf632dbd278ea941c54d83e3ed8f13657bcb4bcbbfc8d63c9d834acf4a  62be15a474e866e4bef6c9d5.txt
LAYOUT_IDENTICAL
```

Text form used for every quote and count: **the `.txt` read as UTF-8** — 61188 bytes, 39676 chars,
sha256 `960da5cf…d834acf4a`; byte-exact `pdftotext -layout` output of the `.raw` (poppler), so nothing
was lost relative to that extractor. Offsets are Python `str` indices (`text.find`), i.e. characters.

## Identity stamp (document's own)

- Title, unique only with its section suffix, char **809**, 66 chars / 6 words:
  `機能性表示食品制度の届出資料におけるPRISMA 2020声明 システマティックレビュー記載の留意点(別紙様式 (V) -4 本文)`.
  Bare title 3× (809, 28799, 36392); page-7 section title `(V) -5以降` once at 36448.
- Edition line `2026年6月5日 第２版` — **3×** (142, 28270, 35901); author line
  `作成：一般社団法人 健康食品産業協議会` **3×** (298, 28394, 36016); `協力：` 3× (460, 28514, 36127)
  with exactly three bodies: 公益財団法人 日本健康・栄養食品協会 (463), 特定非営利活動法人 日本抗加齢協会
  (628), 公益社団法人 日本通信販売協会 (792). None is unique, so none can serve as a located quote.
- Host: `jaohfa` **0×**, `https` 0×, `www.` 0× — the host exists only in the URL.
- `pdfinfo`: `Title: systematic_review.pdf`, `CreationDate: Mon Jun 1 22:15:17 2026 -03`,
  `ModDate: Wed Jun 3 02:19:08 2026 -03`, `Pages: 9`. Edition date is two days after the last
  modification; no revision history (`改訂` 0×, `初版` 0×, `第1版` 0×, `令和` 0×).

## Located quotes — 8 unique, byte-exact, ≤25 whitespace words and ≤160 chars

char/len/ws-words: #1 4045/22/1, #2 4124/30/1, #3 4211/39/1, #4 4409/37/3, #5 5720/41/1,
#6 36834/39/1, #7 15059/27/1, #8 36747/28/5. Each checked `t.count(q)==1` and `t[i:i+len(q)]==q`.
#1–#3 are item 6's 留意点 cell (p.1); #4 item 7's; #5 item 8's; #6–#8 the (V)-5以降 section row 2.
None is the title, the edition line or the author line.

```
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	検索したデータベース等の情報を全て記載する。	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	それぞれのデータベース毎に最後に検索した日の日付を記載する。	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	ハンドサーチの有無を記載する。ハンドサーチを実施した場合はその方法を記載する。	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	検索者は、原則、#8に記載する。ただし＃7にも記載してあったとしても差し支えない。	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	検索ワードや検索式は実際に使用した、もしくはそれと同等の詳細なものであること。	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	ハンドサーチを実施している場合は、その結果を記載する。	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S110	https://jaohfa.com/pdf/systematic_review.pdf	別紙様式 (V) -4 (#7) に合わせた記載とする。	corpus/knowledge/japanese-search-record-r38.md
```

## Negative sweeps — exact counts in the `.txt`

`t.count(x)` plus a full offset walk (no line anchoring). Searcher: 検索者 **3** [4409, 5720, 36710];
检索者 0; 检索人员 0; 検索担当 0. Grey literature: 灰色文献 0; グレーリテラチャー 0; gray literature 0;
grey literature 0; 灰色 0; グレー 0; gray 0; grey 0. Hand-search: ハンドサーチ **3** [4211, 4226, 15059];
手検索 0; 手工检索 0; hand-search 0; handsearch 0; hand search 0; ﾊﾝﾄﾞｻｰﾁ 0; ハンド・サーチ 0.
Search date: 検索日 0; 検索期間 0; 检索时间 0; 检索日期 0; but 最後に検索した日 **2** [4137, 31451];
日付 5 [4146, 4285, 25168, 31429, 31460]. `期間` 3 hits (16674, 23921, 33145) are all 摂取期間.

**Absent, stated for the sweep:** 检索者, 检索人员, 検索担当, 灰色文献, グレーリテラチャー,
gray literature, grey literature, 手検索, 手工检索, hand-search, 検索日, 検索期間, 检索时间, 检索日期
— all 0. Present: 検索者 3× and ハンドサーチ 3×. So a staged "neither names the searcher" sentence is
**false for S110** (4409, 5720, 36710; (V)-5 row 2 gives the searcher a row at 36710). Grey literature
is genuinely unnamed by every sweep term. A search-date claim must be phrased on
`最後に検索した日の日付` (4124, 31451), not on 検索日/検索期間, which are absent.

## Staged entry checked against the capture

Grounded byte-exact: "date of the last search **for each database**" = #2; "presence or absence of
hand-searching … method if it was" = #3; "searcher, search words, search expression … (V)-5" = #4 plus
the (V)-5 row-2 cell (検索者、36710 / 検索ワード、36795 / 検索式 36840); "words and expression … actually
used, or an equivalent detail" = #6; "edition line … author … three cooperating bodies" = the
作成/協力 lines above. Findings the L1 should carry (no predicate touched):

1. **Searcher locus understated.** Entry puts the searcher on (V)-5; the form says
   `検索者は、原則、#8に記載する` (#5) and (V)-5 row 2 must match (V)-4 #7 (#8). #8 is the primary locus;
   (V)-5 carries the field but points back to #7.
2. **Second hand-search rule missing.** #7 (15059, item 16a 研究の選択) requires the *results* of
   hand-searching to be reported when done; the entry covers only presence and method.
3. **Filters and limits missing.** Item 7's checklist column reads `用いたフィルターや制限も含め、…`
   (`用いたフィルターや制限も含め` unique at 4330; `完全な検` 4403 and `索戦略を記載する` 4481 are the same
   cell split by layout). The record here must carry filters and limits; the entry never says so.
4. **Modality upgrade.** `必須` 0×, `望ましい` 28×, `記載する` 141×; the document titles itself
   記載の留意点 (points to note). "The form **requires**" is the PRISMA checklist column's modality, not
   the association's note; attribute it to the column or soften to "directs".
5. **Title drift in the staged row (round-50 routed defect 4 class).** SOURCES.append.md:35 titles it
   `PRISMA声明チェックリスト(2020年) 別紙様式 (V)-4 および (V)-5（機能性表示食品制度の届出資料）— … 第2版`.
   `PRISMA声明チェックリスト(2020年）` is the *column header* (895, 4598, …, 5×), not the title (809);
   the row writes `第2版` (0× in text) for `第２版` (3×), and `(V)-4`/`(V)-5` (0× each) for
   `(V) -4`/`(V) -5` (5× each, the text-form spacing).
6. **Recheck anchor mislabelled.** `検索者、検索ワード、検索式` occurs exactly once, at 4409, inside item
   7's 留意点 cell. The (V)-5 heading cell is those words wrapped over three lines (36710, 36795, 36840)
   and is never contiguous; the anchor resolves but "(V)-5 heading" names the wrong cell, so a
   re-download check written that way can pass while the heading changes.
7. **"A revision, and says so"** rests only on `第２版`; no 改訂/初版 history exists, so the document
   does not say what the revision changed.

## Lane-side state observed (read-only)

`git log --oneline -3` at the lane tip: `cfe6c9f`, `75a9406`, `2a3389d`; base `9ec1751a…` is an
ancestor. `corpus/SOURCES.md` max row S106; `grep -cE "^\| S(10[7-9]|11[0-3]) "` = 0 (S107–S113 free);
`grep -n jaohfa corpus/SOURCES.md corpus/knowledge/*.md` no match; `ls corpus/knowledge` has no
`*search-record*` file — consistent with the frozen `ENTRIES=0/3` before-line; S110 is unbound at the tip.

## Limits

No network, no live fetch; one extractor only (the PDF is a form, so cell order is layout order, not
reading order); the A-pass report unread; no counter run; no lane edit; S109 and S116–S126 not checked.
Offsets are character indices in the `.txt`, not byte offsets; the `.raw` served only for the extractor
check and `pdfinfo`.

VERDICT: attacked staged S110's identity, quotes and negative sweeps independently — identity stamp found (title 809, edition 3×, author + three cooperating bodies, host only in URL, PDF ModDate 2026-06-03), eight unique located quotes emitted, searcher/grey/hand-search/search-date sweeps counted (検索者 3, ハンドサーチ 3, all Chinese and grey terms 0, 検索日/検索期間 0 but 最後に検索した日 2), and the staged entry is grounded on its four main claims while seven calibration/depth corrections stand (searcher locus #8, hand-search results #16a, filters/limits, modality, title drift, recheck anchor mislabel, revision history).
