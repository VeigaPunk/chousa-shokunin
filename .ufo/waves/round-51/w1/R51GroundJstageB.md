# R51GroundJstageB — independent second pass on staged S109 (日本健康教育学会誌 32(2), 2024)

seat: R51GroundJstageB (scribe, leaf) · date: 2026-10-25 · lane: /home/vgpnk/Projects/shokunin/chousa-shokunin
capture (read-only): /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/7194acc65a18f6555e4b8893.{txt,raw}
**form used:** the `.txt` read as UTF-8 (21,216 chars); every offset below is `text.find(quote)` on that exact string. The `.raw` is the PDF and was read only with `pdfinfo`/`pdftotext`. No network, no install (poppler already present).

## Provenance

```
$ python3 -c "import hashlib;print(hashlib.sha256(b'https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja').hexdigest()[:24])"
7194acc65a18f6555e4b8893
$ sha256sum 7194acc65a18f6555e4b8893.raw 7194acc65a18f6555e4b8893.txt
9315274a275172fe1cadacb8871264647211e50c07431e7fb127502554918d69  ...raw
05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f  ...txt
$ head -c 8 ...raw | xxd   -> 00000000: 2550 4446 2d31 2e36   (%PDF-1.6)
$ cmp ...raw ...pdf && echo RAW_EQ_PDF   -> RAW_EQ_PDF
$ pdfinfo ...raw | head -8
Title:  Japanese Journal of Health Education and Promotion 32(2): 118-124 (2024)
CreationDate: Wed Jun 5 04:12:54 2024 -03 · Pages: 7 · PDF version: 1.6 · Encrypted: yes (RC4; print/copy yes)
```

## Document identity stamp (the document's own statement of itself)

| element | value | offset in .txt |
|---|---|---|
| title | `システマティックレビューの基礎` | 76 (running head 3109 / 9368 / 13907) |
| author | `喜屋武       享 *1,*2` (琉球大学医学部保健学科 / 京都大学大学院医学研究科) | 132 |
| citation | `〔日健教誌，2024; 32(2): 118–124〕` | 747 |
| publisher line | `Copyright © Japanese Society of Health Education and Promotion` | 2968 |
| PDF metadata title | `Japanese Journal of Health Education and Promotion 32(2): 118-124 (2024)` | `.raw` (pdfinfo) |
| edition | 2024, 32(2), 7 pages, pp.118–124, created 2024-06-05 | `.raw` + 747 |
| host | `www.jstage.jst.go.jp` — from the URL and the cache key; the capture names J-STAGE only as a database in 表1 (6061), never as its own host | URL |

## Page attribution — the section is on p.122, not p.121

7 formfeeds split the .txt into the PDF's 7 pages: boundaries 3031(119) 5705(120) 9322(121) 10182(122) 13817(123) 19132(124). Per-page check on the `.raw`:

```
$ pdftotext -f 4 -l 4 -enc UTF-8 ...raw - | grep -n -e 'グレー論文' -e '^121$'
33:白書などの “グレー論文” を含めることが一般的である．
59:121
$ pdftotext -f 5 -l 5 -enc UTF-8 ...raw - | grep -n -e 'その日時' -e '1 次情報のまとめ' -e '^122$'
5:か，その日時，使用した検索式を同時に記録しておくこ
179:1 次情報のまとめ
201:122
```

- **p.121** (PDF page 4) = section 2 (検索式と検索するデータベース) + the `グレー論文` sentence + section 3 heading.
- **p.122** (PDF page 5) = heading `7.    1 次情報のまとめ` (13418) and the recording instruction (13710 + 10234).

⇒ staged row S109 `日本健康教育学会誌 32(2):120-121` and `the section on 1次情報のまとめ, p.121`, and entry line 4 `the section on 1次情報の「収集」, p.121`, drift twice: **page** (122, not 121) and **range** (118–124, not 120–121); and the heading is まとめ, not 収集 — `1次情報の収集` occurs 0×, `1次情報の「収集」` 0×, `1 次情報を収集する` 1× (13560, body).

## The staged "who conducted the search" claim IS carried — by a phrase no sweep term catches

The instruction spans a column break on p.122 (left column ends, right column begins):

- `このプロセスに際して，誰が検索を行ったの` — 13710, unique (left column, last line)
- `か，その日時，使用した検索式を同時に記録しておく` — 10234, unique (right column, first line; the `か` at 10232 completes the fragment above)
- `とが望ましい．これにより，研究の透明性を保ち，他者` — 10301, unique
- `が同様の検索を再現できるようになる` — 10370, unique

Reconstructed: このプロセスに際して，**誰が検索を行ったのか**，その日時，使用した検索式を**同時に**記録しておくことが望ましい．これにより，研究の透明性を保ち，他者が同様の検索を再現できるようになる． So the staged claims (a) three fields recorded together and (b) reason = transparency + reproduction **are carried**. The entry's `recheck` run `その日時，使用した検索式を同時に記録しておく` (unique, 10234) omits the searcher clause, so a re-download could drop 誰が検索を行ったのか and the recheck would still pass.

## Negative sweeps — exact counts in the .txt (all 16 specified terms = 0)

```
検索者 0   检索者 0   检索人员 0   検索担当 0
灰色文献 0   グレーリテラチャー 0   gray literature 0
ハンドサーチ 0   手検索 0   手工检索 0
検索日 0   検索期間 0   检索时间 0   检索日期 0
adjacent forms, also 0: 検索実施者 検索担当者 検索者名 サーチャー 担当者 グレー文献 グレイ 灰色
  Grey literature Gray literature ハンド・サーチ 手工搜索 手作業 引用文献検索 参考文献検索
  検索日時 検索年月日 最終検索日 検索した日 参照日 アクセス日 检索年限 检索策略
context (present): 検索 28  検索式 8  データベース 16  レビューワー 2
```

Adjacent forms that defeat a bare "neither names X" reading:
- `誰が検索を行ったの` ×1 (13721) — **searcher named** without 検索者.
- `グレー論文` ×1 (9775, p.121) — **grey literature named** without 灰色文献/グレーリテラチャー/gray literature.
- `日時` ×1 (10234) — **search date/time required** without 検索日/検索期間.
- `レビューワー` ×2 (10332, 11587) — reviewers, a different role from the searcher.

Hand-search is the one sweep that survives a concept check: all hand-search terms 0, and no route is described (`引用文献` 0, `参考文献` 0; `リスト` only inside リストアップ at 7901).

⇒ a staged "neither names the searcher" claim must carry its sweep **and** state that the sweep is lexical only: here 検索者=0 while the searcher is named once (13721); likewise grey literature (9775) and the date (10234). Only hand-search is absent lexically and conceptually in this capture.

## Other staged claims checked

- PRISMA translated into Japanese and several languages, checklist in the appendix — **carried**: `PRISMA は，日本語を含め 9），複数の` (12666) + `言語に翻訳されている 10）` (12732) + `おいて報告すべき内容のチェックリストも付録されてい` (12804), all p.122.
- Exclusion reasons recorded — **carried**: `各行程で最終的な批評の対象から外れた論文は，その` (10858, p.122).
- Two reviewers independent — **carried**: `2 名以上のレビューワーが独立して` (11581, p.122).

## QUOTE machine lines

staged-id column = staged package id **S109** (planned lane id **S107**); entry = lane path.

```
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	〔日健教誌，2024; 32(2): 118–124〕	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	Copyright © Japanese Society of Health Education and Promotion	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	白書などの “グレー論文” を含めることが一般的である	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	その日時，使用した検索式を同時に記録しておく	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	とが望ましい．これにより，研究の透明性を保ち，他者	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	が同様の検索を再現できるようになる	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	各行程で最終的な批評の対象から外れた論文は，その	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	2 名以上のレビューワーが独立して	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	7.    1 次情報のまとめ	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	このプロセスに際して，誰が検索を行ったの	corpus/knowledge/japanese-search-record-r38.md
```

VERDICT: I attacked the staged S109 identity and its searcher claim against the capture — the "who conducted the search" claim holds (13710+10234, p.122) but the staged page/range identity is wrong (p.122, 118–124), all 16 sweep terms are 0 while the searcher, grey literature and date are each present under other lexical forms (13721, 9775, 10234), and hand-search alone is absent both lexically and conceptually.
