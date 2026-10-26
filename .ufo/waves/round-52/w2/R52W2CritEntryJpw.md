# R52W2CritEntryJpw — entailment attack on `corpus/knowledge/japanese-prisma-item-wording-r40.md` (S116)

Attacked: the entailment of every bullet under `#### Observation` and `#### Inference`
of `japanese-prisma-item-wording-r40.md` against its capture text form
`.qcache/e84bfe97808591d23fe3266f.txt` (key `e84bfe97808591d23fe3266f`, archive URL
`https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf`),
plus the entry's two cross-lane-file comparisons. No fetch; L0 `8d77e6c1` open.
No install needed (pdfinfo/pdftotext already at `/usr/bin/`).

## Evidence (commands run)

`python3 verify_s116.py` (scratch) printed:
- `len(chars) = 5328`, `len(bytes) = 10106`, sha256 `93558b6d4b0e7a6b76d37954f7cfced59847c2f34454dc887677b560730ab155` (all match entry line 3).
- Every located quote occurs exactly once at its stated offset: `すべてのデータベース，研究登録，Web サイト，組織，文献リスト` find=475; `研究を特定するために調べたり，助言を求めた情報` find=508; `源を記載する。` find=555; `それぞれの情報源が最後に調べられた日付を記載する` find=592; `用いたフィルターや制限も含め，` find=641; `試験登録，Web サイトの完全な検索戦略を記載する` find=753; `完全な検索戦略` find=766; `スクリーニングしたレビューアの数` find=815; `データを収集したレビュー担当者の数` find=996. All count=1.
- `表 2` find=225, count=1; `PRISMA 2020 チェックリスト` find=0; header `大項目`/`番号`/`チェックリスト項目` at 20/37/71; item numbers 1…27 all present (27 at 5151; tail is item 27 + `\n\x0c`).
- Zero counts: `出版 0`, `年 0`, `版 0`, `http 0`, `検索者 0`, `検索担当者 0`, `司書 0`, `誰が 0`; `独立して作業したかどうか 3`; `情報源 2`; `研究登録 1`; `試験登録 3`; `組織 1` (find 499), `文献リスト 1` (find 502) — both only inside item 6.
- URL keys: archive URL → `e84bfe97808591d23fe3266f`, original URL → `f3dbe2fe59a684b1b94cfadc`.

`pdfinfo .qcache/e84bfe97808591d23fe3266f.raw` → `Title: 表1`, `CreationDate: Tue Sep 19 02:06:00 2023 -03`, `Pages: 1`, `Page size: 595.275 x 841.89 pts (A4)`.

`pdftotext -layout <raw> pdftotext_out.txt && cmp pdftotext_out.txt <txt>` → `CMP_IDENTICAL` (10,106 bytes both; reproduces entry line 4).

Replicated the entry's recheck command verbatim → `5328 [0, 0, 0, 0] [475, 508, 592, 641, 753, 766, 815, 996]` (matches line 5).

`ls` of the cache: `f3dbe2fe59a684b1b94cfadc.fail` = 6 bytes, content `rc=28`; `c280fdf897ab0d488017b63a.raw` sha256 = `ba9bc9c1…9732` and `.txt` = `93558b6d…ab155` (same as e84bfe97); memento URL `https://web.archive.org/web/20260418151432/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf` hashes to `c280fdf897ab0d488017b63a`.

S116 registry row (SOURCES.md line 126, raw): anchor cell = `char 475, char 592, char 641, char 753` (all quote offsets); `used-by` = `corpus/knowledge/japanese-prisma-item-wording-r40.md`; opened `2026-10-26`, recheck 180d, tier B.

Cross-lane comparisons opened:
- `japanese-search-record-r38-amendment-2026-10-23.md` (ground note): records S112 fields `検索した文献データベース名` (char 11229), provider `Ovid などのプロバ` (11243) and `検索の開始日と終了日を記載することで` (11294) — database, provider, window ✓.
- `japanese-search-record-r38.md` Unknown bullet (my entry's Unknown 3): re-opened S107 capture `7194acc65a18f6555e4b8893.txt` (len 21216) → `このプロセスに際して，誰が検索を行ったの` count=1 find=13710 ✓ ("who conducted the search").
- `chinese-search-record-r39.md` (my entry's Unknown 4): holds SinoMed record (S111) and Chinese animal-experiment reporting copies (S109, S110), not this checklist's items ✓.

## Verdict per bullet

All four Observation bullets and all three Inference bullets: **supports** — every quote, offset, count, hash, page size and zero-sweep I re-ran agrees with the sentence as worded. Three wording-level defects found (none contradicts; all are "weaker/scope" issues):

**D1 (source line, locator literals).** `項目6 情報源 (char 453) and 項目7 検索戦略 (char 619)` — the literals `項目6`/`項目7` occur 0 times (項目 appears only in 大項目/チェックリスト項目/データ項目); at char 453 begins the row label `情報源` and the digit 6 sits at char 469; at char 619 begins `検索戦略` and the digit 7 at char 631 (`t[469]='6'`, `t[619:638]='検索戦略            7  '`). The labels are recoverable but the sentence is not literally entailed. Narrowed source-line wording: `the 情報源 row numbered 6 (label at char 453, number at char 469) and the 検索戦略 row numbered 7 (label at char 619, number at char 631) of the checklist table`.

**D2 (Inference 2, vocabulary split).** `so a record keyed to item 7 alone omits two source classes` presumes item 6's `研究登録` and item 7's `試験登録` are one class: literally item 7's list (databases, 試験登録, websites) is not a subset of item 6's five (databases, 研究登録, websites, organisations, reference lists) — 研究登録 is also absent from item 7 as worded. The two named absent classes (organisations, reference lists) are correct and verbatim. Narrowed wording: append to that sentence `(item 7 names 試験登録 where item 6 says 研究登録)` or replace `omits two source classes` with `omits organisations and reference lists`.

**D3 (Observation 4, "only").** `The archive copy is the only readable capture` is ambiguous: a second readable capture of the same PDF exists (2026-04-18 memento `c280fdf897ab0d488017b63a`, in the cache; same raw sha256), disclosed later in Unknown bullet 1. "Only" holds within the {archive URL, original URL} pair. Narrowed wording: `The archived copy is the only readable capture of the original URL: the archive URL maps to e84bfe97 (a .txt and a .raw), while the original URL maps to f3dbe2fe.fail only (rc=28, 6 bytes); the 2026 memento (c280fdf…) is also readable but is not a lane row.`

Everything else checked passes exactly: Obs 1 (pdfinfo page/title/creation date; zero 出版/年/版/http; items 1–27; 表 2 at 225), Obs 2 (five classes; 組織 at 499, 文献リスト at 502; advice clause; date sentence), Obs 3 (three classes; second database mention at 694; 組織/文献リスト absent from item 7), Obs 4 (reviewer counts at 815/996; both carry 独立して作業したかどうか), Inf 1 (four-term sweep 0; no searcher slot), Inf 3 (counts vs searcher terms), and the two cross-file comparisons.

VERDICT: Attacked the entailment of japanese-prisma-item-wording-r40.md's Observation/Inference bullets against the S116 capture and its two lane-file comparisons — all bullets support; landed three wording-level corrections D1–D3 (locator literals, 研究登録/試験登録 split, "only readable capture" scope); no contradiction found.
