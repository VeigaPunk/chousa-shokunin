# R51W2ReopenRowS107 — Re-open and cell-by-cell audit of Registry row `S107`

Seat: `R51W2ReopenRowS107` (round 51, wave 2 — falsify) · Tip: `4436e279b91d8d68fd439c9095695035fbeeab74` · Base: `9ec1751a24231e899ceea4688e21c8edf6046d35` · Freeze: `d603f6f00f78d64f123d3aed2dd9f8701547a4ba`.
Capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/7194acc65a18f6555e4b8893.txt` (read-only).
**Form used throughout:** the `.txt` read as UTF-8 (`len(text) = 21216`, `36968` bytes, sha256 `05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f`); every offset below is `text.find(quote)` in that UTF-8 string, where `text.count(quote) == 1`, `len(quote.split()) <= 25`, and `len(quote) <= 160`. No tool installed; no network; no scratch directory created.

## 1. Commands and observed output

```text
$ grep -n '^| S107 ' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
117:| S107 | システマティックレビューの基礎（喜屋武 享）— 日本健康教育学会誌 32(2):120-121 (2024) — https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja | paper | A | what this Japanese health-education society article recommends a review's search record carry, and why, as this copy states it | section 7 (1 次情報のまとめ) on the page whose footer reads 122 of 日健教誌 第 32 巻 第 2 号 (2024); capture .txt read as UTF-8, 21216 characters; char 13721, char 10234, char 10314, char 10370, char 12666, char 12732, char 12807, char 17398 | the article recommends (望ましい) recording together who conducted the search, the date and the search expression used, so that others can reproduce the search; it notes PRISMA is translated into Japanese with a checklist appended and names no search-reporting extension | mined | 2026-10-25 | 365d | corpus/knowledge/japanese-search-record-r38.md |

$ awk -F'\t' '$1=="S107"' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round51/spans.tsv
S107	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f	10152	spans/S107-1.txt	か，その日時，使用した検索式を同時に記録しておく	corpus/knowledge/japanese-search-record-r38.md
S107	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f	10154	spans/S107-2.txt	その日時，使用した検索式を同時に記録しておく	corpus/knowledge/japanese-search-record-r38.md
S107	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f	10159	spans/S107-3.txt	使用した検索式	corpus/knowledge/japanese-search-record-r38.md
S107	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f	10221	spans/S107-4.txt	とが望ましい．	corpus/knowledge/japanese-search-record-r38.md
S107	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f	10234	spans/S107-5.txt	研究の透明性を保ち，他者	corpus/knowledge/japanese-search-record-r38.md
S107	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f	10290	spans/S107-6.txt	が同様の検索を再現できるようになる	corpus/knowledge/japanese-search-record-r38.md
S107	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f	12586	spans/S107-7.txt	PRISMA は，日本語を含め	corpus/knowledge/japanese-search-record-r38.md
S107	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f	12652	spans/S107-8.txt	言語に翻訳されている	corpus/knowledge/japanese-search-record-r38.md
S107	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f	12727	spans/S107-9.txt	報告すべき内容のチェックリストも付録されてい	corpus/knowledge/japanese-search-record-r38.md
S107	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f	12735	spans/S107-10.txt	チェックリストも付録されてい	corpus/knowledge/japanese-search-record-r38.md
S107	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f	12793	spans/S107-11.txt	るため，使いやすさという点でも考慮されている．	corpus/knowledge/japanese-search-record-r38.md
S107	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f	13630	spans/S107-12.txt	このプロセスに際して，誰が検索を行ったの	corpus/knowledge/japanese-search-record-r38.md
S107	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f	13641	spans/S107-13.txt	誰が検索を行った	corpus/knowledge/japanese-search-record-r38.md
S107	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f	13641	spans/S107-14.txt	誰が検索を行ったの	corpus/knowledge/japanese-search-record-r38.md
S107	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f	17318	spans/S107-15.txt	本健康教育学会誌にもシステマティックレビューの投	corpus/knowledge/japanese-search-record-r38.md
S107	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f	18361	spans/S107-16.txt	PRISMA-ScR	corpus/knowledge/japanese-search-record-r38.md

$ grep -ln '^source: S107 ' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/*.md
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/japanese-search-record-r38.md

$ env -u ASSIMILATE_CITES python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round51/c2-count.py
ENTRIES=3/3
BOUND=6/7 (min 5) REFUSED=1
BOUND_IDS=S107,S108,S109,S110,S111,S112
...
ANCHOR_BOUND=6/6
...
C2=PASS
```

## 2. Cell-by-cell audit against `7194acc65a18f6555e4b8893.txt` (read as UTF-8)

| # | Cell | Value in `corpus/SOURCES.md:117` | Verdict | Evidence & located quotes (`.txt` UTF-8) |
|---:|---|---|---|---|
| 1 | `id` | `S107` | **HOLDS** | Maps staged `S109` → lane `S107` (first new row after `BASE_REV` max `S106`). |
| 2 | `source` | `システマティックレビューの基礎（喜屋武 享）— 日本健康教育学会誌 32(2):120-121 (2024) — https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja` | **DEFECT** (page range `120-121`) | URL `sha256(url)[:24]` = `7194acc65a18f6555e4b8893` (**holds**). Title + author: `システマティックレビューの基礎\n                                        喜屋武       享 *1,*2` at `char 76` (unique, 4 words, 73 chars; `喜屋武       享 *1,*2` alone at `char 132`) (**holds**). Full journal name across line 281–282: `本健康教育学会誌にもシステマティックレビューの投` at `char 17398` (**holds**). **Defect:** the cell keeps the staged page range `32(2):120-121 (2024)` (from `SOURCES.append.md:34`), whereas the article is a 7-page `特別報告` (`char 0`) spanning **pp. 118–124**: Japanese citation `〔日健教誌，2024; 32(2): 118–124〕` at `char 747` (unique, 3 words, 27 chars), English citation `〔 JJHEP, 2024; 32(2): 118–124〕` at `char 20804` (unique, 5 words, 30 chars), and `120-121` / `120–121` occur `0` times in the capture. Even the anchored §7 passage sits on p. 122 (`122    日健教誌   第 32 巻   第2 号   2024 年` at `char 13780`), outside `120-121`. |
| 3 | `kind` | `paper` | **HOLDS** | Published journal article (`特別報告` at `char 0`; `〔日健教誌，2024; 32(2): 118–124〕` at `char 747`). |
| 4 | `tier` | `A` | **HOLDS** | Argued by `scope`: the row is scoped strictly to what this article itself recommends and states (`as this copy states it`), for which the own-document J-STAGE PDF text is primary (`A`), unlike an index record (`B`). |
| 5 | `scope` | `what this Japanese health-education society article recommends a review's search record carry, and why, as this copy states it` | **HOLDS** | Matches the society publisher (`Copyright © Japanese Society of Health Education and Promotion` at `char 2968`), the journal name (`char 17398`), and the own-copy boundary supporting tier `A`. |
| 6 | `anchor` | `section 7 (1 次情報のまとめ) on the page whose footer reads 122 of 日健教誌 第 32 巻 第 2 号 (2024); capture .txt read as UTF-8, 21216 characters; char 13721, char 10234, char 10314, char 10370, char 12666, char 12732, char 12807, char 17398` | **HOLDS** (with section-label imprecision) | Section heading `7.    1 次情報のまとめ` is at `char 13418` on the page whose footer reads `122    日健教誌   第 32 巻   第2 号   2024 年` at `char 13780` (correcting the staged `p.121` and `1次情報の「収集」`). Capture `.txt` read as UTF-8 is `21216` chars. Every `char N` in `anchor` is the exact `text.find(quote)` (`int(offset) + span.find(quote)`) of a located quote of `S107` in `spans.tsv`: `char 13721` (`誰が検索を行った` in `S107-13.txt` and `誰が検索を行ったの` in `S107-14.txt`, `13641+80`), `char 10234` (`その日時，使用した検索式を同時に記録しておく` in `S107-2.txt`, `10154+80`), `char 10314` (`研究の透明性を保ち，他者` in `S107-5.txt`, `10234+80`), `char 10370` (`が同様の検索を再現できるようになる` in `S107-6.txt`, `10290+80`), `char 12666` (`PRISMA は，日本語を含め` in `S107-7.txt`, `12586+80`), `char 12732` (`言語に翻訳されている` in `S107-8.txt`, `12652+80`), `char 12807` (`報告すべき内容のチェックリストも付録されてい` in `S107-9.txt`, `12727+80`), `char 17398` (`本健康教育学会誌にもシステマティックレビューの投` in `S107-15.txt`, `17318+80`). Minor imprecision: `12666`, `12732`, `12807` sit in `8.         結果の報告・論文執筆` (`char 11762`, also on p. 122) and `17398` in `IV   おわりに` (p. 123), though the cell header names only `section 7 (1 次情報のまとめ)`. |
| 7 | `teaches` | `the article recommends (望ましい) recording together who conducted the search, the date and the search expression used, so that others can reproduce the search; it notes PRISMA is translated into Japanese with a checklist appended and names no search-reporting extension` | **HOLDS** | Every clause is carried by the capture: (1) recommends (`望ましい`): `とが望ましい．` at `char 10301`; (2) recording together who conducted the search, the date and the search expression used: `このプロセスに際して，誰が検索を行ったの` (`char 13710`, containing `誰が検索を行ったの` at `char 13721` at the foot of the left column) continuing at the head of the right column `か，その日時，使用した検索式を同時に記録しておく` (`char 10232`, containing `その日時，使用した検索式を同時に記録しておく` at `char 10234` and `使用した検索式` at `char 10239`); (3) so that others can reproduce the search: `研究の透明性を保ち，他者` (`char 10314`) + `が同様の検索を再現できるようになる` (`char 10370`); (4) PRISMA is translated into Japanese with a checklist appended: `PRISMA は，日本語を含め` (`char 12666`) + `言語に翻訳されている` (`char 12732`) + `報告すべき内容のチェックリストも付録されてい` (`char 12807`) + `るため，使いやすさという点でも考慮されている．` (`char 12873`); (5) names no search-reporting extension: `PRISMA-S` occurs only once in the capture, as a prefix of `PRISMA-ScR` (scoping-review extension, ref. 12) at `char 18441`. |
| 8 | `status` | `mined` | **HOLDS** | Admitted and cited by an active entry in `corpus/knowledge/`. |
| 9 | `opened` | `2026-10-25` | **HOLDS** | Re-opened from the campaign capture cache in round 51 on `2026-10-25`. |
| 10 | `recheck` | `365d` | **HOLDS** | Valid `NNd` cadence matching `japanese-search-record-r38.md:6`. |
| 11 | `used-by` | `corpus/knowledge/japanese-search-record-r38.md` | **HOLDS** | Matches `grep -ln '^source: S107 ' corpus/knowledge/*.md` (`corpus/knowledge/japanese-search-record-r38.md` only). |

## 3. Non-author re-open survivability and repair

- **Automated gates (`c2-count.py`, `sources-census.sh validate`):** **SURVIVES.** `c2-count.py` checks URL matching (`url_of`), `mined`, `2026-10-25`, `used-by`, and that every `char N` in `anchor` is in `spans.tsv`'s offset set for `S107` (`ANCHOR_BOUND=6/6`, `C2=PASS`).
- **Non-author human re-open:** **FAILS on `source` cell bibliographic page range (`32(2):120-121` vs `32(2):118–124`).** While Wave 1 fixed the staged `p.121` anchor error inside the `anchor` cell and the entry, `tools/assimilate-rows.py` copied cell 2 (`source`) from staged `S109` (`32(2):120-121`) without correcting the page span to `118-124` (`〔日健教誌，2024; 32(2): 118–124〕` at `char 747`), leaving `source` self-contradictory against `anchor`'s `page whose footer reads 122`.

```markdown corpus/SOURCES.md
| S107 | システマティックレビューの基礎（喜屋武 享）— 日本健康教育学会誌 32(2):118-124 (2024) — https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja | paper | A | what this Japanese health-education society article recommends a review's search record carry, and why, as this copy states it | section 7 (1 次情報のまとめ) and section 8 on the page whose footer reads 122 of 日健教誌 第 32 巻 第 2 号 (2024); capture .txt read as UTF-8, 21216 characters; char 13721, char 10234, char 10314, char 10370, char 12666, char 12732, char 12807, char 17398 | the article recommends (望ましい) recording together who conducted the search, the date and the search expression used, so that others can reproduce the search; it notes PRISMA is translated into Japanese with a checklist appended and names no search-reporting extension | mined | 2026-10-25 | 365d | corpus/knowledge/japanese-search-record-r38.md |
```

VERDICT: Attacked `corpus/SOURCES.md` row `S107` against `.qcache/7194acc65a18f6555e4b8893.txt` (UTF-8, 21216 chars) — 10 of 11 cells (`id`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `status`, `opened`, `recheck`, `used-by`), all 8 anchor offsets (`13721`, `10234`, `10314`, `10370`, `12666`, `12732`, `12807`, `17398`), and all 16 `spans.tsv` quotes hold, but the `source` cell has a bibliographic defect (`32(2):120-121 (2024)` leftover from staged `S109` instead of `32(2):118-124 (2024)` at `char 747`, contradicting `anchor`'s p. 122).
