# R52GroundArchiveB — second grounding pass: the Japanese PRISMA 2020 checklist (staged S129 → lane S116)

seat: R52GroundArchiveB · round 52, wave 1 · date 2026-10-26 · base `00f8c7f5` · lane `chousa-shokunin`
axis: depth (sourced), with the capture-form operability of this document
scope: the archived Japanese PRISMA 2020 checklist only — identity stamp, located quotes, negative sweeps,
an entry draft for `corpus/knowledge/japanese-prisma-item-wording-r40.md`, and the facts its lane Registry
row needs. Read: the two captures under `.qcache`, the staged package `merge/chousa/`, and lane files
(`QUALITY.md`, `PROVINCE.md`, `SOURCES.md`, `claims.md`, `c2-count.py`, `build-spans.py`,
`inference-ground.py`, `quote-substance-check.py`). NOT read: `R52GroundArchiveA`'s report (independent
pass by instruction). No frozen counter run (`c1-count.py`, `c2-count.py` belong to other seats); I mirrored
individual C2 legs read-only. No product file, no index, no jj/git state touched.

## 1. Capture and its text form (measured, not assumed)

```
$ file .qcache/e84bfe97808591d23fe3266f.raw   -> PDF document, version 1.6, 1 page(s)
$ sha256sum .txt .raw  -> 93558b6d…0ab155 (10106 B) / ba9bc9c1…399732 (343301 B)
$ pdftotext -layout c.pdf out_layout.txt && cmp out_layout.txt .qcache/…f.txt  -> IDENTICAL (no output)
```
- Cache key is derived, not guessed: `sha256("https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf")[:24]` = `e84bfe97808591d23fe3266f`. The original URL hashes to `f3dbe2fe59a684b1b94cfadc`, whose only cache file is a 6-byte `.fail` reading `rc=28`.
- Text form used everywhere below: the `.txt` read as UTF-8 = **5,328 characters / 10,106 bytes**, byte-identical to `pdftotext -layout` of the `.raw`. Span digest `93558b6d4b0e7a6b76d37954f7cfced59847c2f34454dc887677b560730ab155`.
- Limit: this capture's *raw* form is the builder's fallback decode (UTF-16LE over PDF bytes) — 171,617 chars of garbage, and none of my quotes occur in it (0 each). So every span for this document must bind to the `.txt` form and its digest, which is what `build-spans.py`'s documented form order picks.

## 2. The document's own identity stamp — title, edition, host, author

```
$ pdfinfo c.pdf
Title: 表1 · Creator: Adobe Illustrator 24.3 (Macintosh) · Producer: Adobe PDF library 15.00
Pages: 1 · Page size: 595.275 x 841.89 pts (A4) · Tagged: no · Custom Metadata: no
CreationDate/ModDate: 2023-09-19 14:06 +09:00 (XMP: xmp:CreateDate 2023-09-19T14:06+09:00)
$ byte sweep: /Author 0, dc:creator 0, pdf:Keywords 0   (XMP dc:title = 表1)
```
- **Title (printed):** `PRISMA 2020 チェックリスト` at char 0; `PRISMA 2020` twice (char 0; char 200 inside item 2's `PRISMA 2020 抄録チェックリスト`).
- **Edition:** `PRISMA 2020`, 42 numbered rows — 1-9, 10a/10b, 11-12, 13a-13f, 14-15, 16a/16b, 17-19, 20a-20d, 21, 22, 23a-23d, 24a-24c, 25-26, 27 (a `^`-anchored scan finds 41; item 27's number sits after its wrapped label).
- **Date:** none printed. The only date artefact is the PDF's own 2023-09-19 14:06 +09:00 creation stamp, which dates the file, not a publication.
- **Host:** `lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf`; the staged row's attribution (JPT ONLINE, ライフサイエンス株式会社) is the host's — the text form counts `ライフサイエンス` 0 and `JPT` 0.
- **Author/translator:** none, anywhere. Sweep: `翻訳` 0, `監訳` 0, `訳` 0, `日本語版` 0; PDF `/Author` absent, `dc:creator` absent. `表1` is the Illustrator artboard name and must not be read as the document's title.

## 3. Negative sweeps — exact counts in the stated form

Form: the `.txt` read as UTF-8 (5,328 characters), the same form the spans use.
```
$ python3 -c "t=open('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/e84bfe97808591d23fe3266f.txt',encoding='utf-8').read();print(len(t),{x:t.count(x) for x in ('検索者','検索担当','检索者','检索人员','検索日','検索期間','文献検索期間','检索日期','检索时间','検索式','検索戦略','检索策略','检索式','灰色文献','グレーリテラチャー','PRISMA-S','レビューア','レビュー担当者','日付','助言','司書','相談')})"
5328 {'検索者': 0, '検索担当': 0, '检索者': 0, '检索人员': 0, '検索日': 0, '検索期間': 0, '文献検索期間': 0, '检索日期': 0, '检索时间': 0, '検索式': 0, '検索戦略': 2, '检索策略': 0, '检索式': 0, '灰色文献': 0, 'グレーリテラチャー': 0, 'PRISMA-S': 0, 'レビューア': 2, 'レビュー担当者': 1, '日付': 1, '助言': 1, '司書': 0, '相談': 0}
```
**Absent (0):** 検索者, 検索担当, 検索日, 検索期間, 文献検索期間, 検索式, 灰色文献, グレーリテラチャー, PRISMA-S, 司書, 相談, and all six simplified-Chinese terms (检索者, 检索人员, 检索日期, 检索时间, 检索策略, 检索式) — the capture holds no simplified Chinese. **Present (positive controls):** 検索戦略 2 (item 7's label char 619; inside `完全な検索戦略` char 766), レビューア 2 (chars 824, 1838), レビュー担当者 1 (char 1004), 日付 1 (char 609), 助言 1 (char 523). Also 0: 翻訳, 監訳, 訳, 日本語版, ライフサイエンス, JPT, http, .pdf, 2023. 1 each: `PRISMA 2020 チェックリスト` (char 0), `PRISMA 2020 抄録チェックリスト` (char 200), `表 2` (char 225).
So the negative claim the entry carries is: **no searcher term, no search-date or search-period field name, no search-expression term, no grey-literature term and no PRISMA-S mention** — each with the count above, in this form.

## 4. QUOTE machine lines (staged id S129, entry = lane r40 entry)

```
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	および統合のために研究がどのようにグループ化されたかを記載する。	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	それぞれの情報源が最後に調べられた日付を記載する。	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	試験登録，Web サイトの完全な検索戦略を記載する。	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	各記録と取得した各報告をスクリーニングしたレビューアの数，独立して作業したかどうか，	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	各報告からデータを収集したレビュー担当者の数，独立して作業したかどうか，	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	および使用したソフトウェアパッケージを記載する。	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	検索で特定した記録数からレビューで採用した研究数まで	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	試験登録名と登録番号を含むレビューの登録情報を提供する，	corpus/knowledge/japanese-prisma-item-wording-r40.md
QUOTE	S129	https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf	次のうちどれが公開されており，どこにあるかを報告する。	corpus/knowledge/japanese-prisma-item-wording-r40.md

```

Each quote is byte-exact, occurs exactly once in the stated form, is ≤25 whitespace words and ≤160 characters (longest: 42 characters, 1 whitespace word — Japanese carries no spaces).
Seven of the nine are items other than the theme's headline sentences: item 5 (char 419), item 8 (803), item 9 (991), item 13d (2647), item 16a (3111), item 24a (4675) and item 27 (5157). The only two theme sentences included are item 6's date sentence (592) and item 7's strategy sentence (753), because they are load-bearing for the entry; the title line, item 6's first sentence and the two item labels are deliberately not machine lines.

## 5. Draft entry — intended lane path `corpus/knowledge/japanese-prisma-item-wording-r40.md`

Amends the staged entry; keeps its path and its amendment relation to round 5's r38 amendment. L1 integrates. Only `S116` appears in it (no staged id, no other id).

```
# PRISMA 2020's Japanese checklist asks for the sources, their dates and the strategy, and counts people only at screening, data collection and bias assessment — the search itself has no person field

source: S116 — https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf — 「PRISMA 2020 チェックリスト」 (JPT ONLINE, ライフサイエンス株式会社), one A4 page, items 1-27 with 10a/10b, 13a-13f, 16a/16b, 20a-20d, 23a-23d and 24a-24c, 42 numbered rows; the publisher's original at https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf serves nothing from this cache (its only capture is a 6-byte `.fail` reading `rc=28`); capture `.qcache/e84bfe97808591d23fe3266f.txt` read as UTF-8, 5,328 characters (10,106 bytes), sha256 `93558b6d…0ab155`, byte-identical to `pdftotext -layout` of the `.raw` (sha256 `ba9bc9c1…399732`)
verified-at: 2026-10-26 — the capture re-opened from the read-only qcache and every quoted phrase re-located at its stated offset with `text.find`; the `.txt` proved to be `pdftotext -layout` output byte for byte (`cmp` prints nothing); no fetch made (L0 `8d77e6c1` open)
recheck: 180d — from the lane root, `python3 corpus/evidence/round52/build-spans.py --check` prints `SPANS_ROWS=n STALE=0` for this entry's rows, then re-fetch the archive route and confirm item 7 still reads `試験登録，Web サイトの完全な検索戦略を記載する。` (char 753) and item 6 still reads `それぞれの情報源が最後に調べられた日付を記載する。` (char 592)
ground: round 52's first grounding pass on the search-record theme — what PRISMA 2020's own Japanese translation asks a review to record about a search, and whether it names the person who ran it; **this entry amends round 5's `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`, which it adds to and does not replace**
adopted: round 52 from the campaign package `merge/chousa/`, staged `knowledge/corpus/knowledge/japanese-prisma-item-wording-r40.md`, re-bound by document to this lane's S116; the staged Registry row is re-pointed so the archive route is its source cell's first URL (the staged cell led with the dead original, which no capture backs) and the staged body's unchecked host result is replaced by the `.fail` capture reading `rc=28`

#### Observation

- **Identity stamp: the page prints a title and an edition, and no date, translator or publisher.** Line 1 is `PRISMA 2020 チェックリスト` (char 0); `PRISMA 2020` occurs twice, the second time at char 200 inside item 2's `PRISMA 2020 抄録チェックリスト`. The text form holds no `翻訳`, no `監訳`, no `訳`, no `日本語版`, no `ライフサイエンス`, no `JPT` and no `http` (each 0 in the sweep below), so the translator, the publisher credit and any publication date are supplied by the host path and the staged row, not by the document.
- **The only date the file carries is its own creation timestamp, and it has no author.** `pdfinfo` on the `.raw` prints `Pages: 1`, `Page size: 595.275 x 841.89 pts (A4)`, `Tagged: no`, `Creator: Adobe Illustrator 24.3 (Macintosh)`, `Producer: Adobe PDF library 15.00`, `Title: 表1`, and a creation/modification stamp that the XMP states as `2023-09-19T14:06+09:00`; the trailer holds no `/Author` key (`grep -c` over the bytes: `/Author` 0, `dc:creator` 0, `pdf:Keywords` 0) and the XMP's `dc:title` is `表1`, the artboard's name, not the checklist's title.
- **Item 6 asks for the sources, an advice clause, and a date per source.** `すべてのデータベース，研究登録，Web サイト，組織，文献リスト，研究を特定するために調べたり，助言を求めた情報源を記載する。` (char 475) and then `それぞれの情報源が最後に調べられた日付を記載する。` (char 592). The date is asked per source and as the date that source was last examined; the sentence names no field for a search's start, end or duration.
- **Item 7 asks for the complete strategy, with the filters and limits named first.** The item reads `用いたフィルターや制限も含め，` (char 641) and closes `試験登録，Web サイトの完全な検索戦略を記載する。` (char 753). `検索戦略` occurs twice in the whole capture: as the item's own label (char 619) and inside this sentence, where `完全な検索戦略` starts at char 766 (the `検索戦略` within it at char 769).
- **People are counted at three later stages, and never for the search.** Item 8 asks `各記録と取得した各報告をスクリーニングしたレビューアの数，独立して作業したかどうか，` (char 803); item 9 asks `各報告からデータを収集したレビュー担当者の数，独立して作業したかどうか，` (char 991); item 11 asks `使用したツールの詳細，各研究を評価したレビューアの数，` (char 1819). The vocabulary for a person is therefore present and item-specific — `レビューア` twice (chars 824, 1838) and `レビュー担当者` once (char 1004) — and no item applies it to whoever ran the search.
- **The search appears on the output side, as a count of records.** Item 16a reads `検索で特定した記録数からレビューで採用した研究数まで` (char 3111) and asks for the process and its results from there; what the checklist asks about a search is what it produced and how it was specified, not who performed it.
- **Registration, synthesis software and shared materials are all named fields.** Item 24a asks `試験登録名と登録番号を含むレビューの登録情報を提供する，` (char 4675); item 13d asks for the model, the heterogeneity assessment and `および使用したソフトウェアパッケージを記載する。` (char 2647); item 27 asks `次のうちどれが公開されており，どこにあるかを報告する。` (char 5157) and enumerates the data collection form, extracted data, analysis data and analysis code, closing with `レビューで使用したその他の資料` — a catch-all, with the strategy itself not enumerated.
- **Item 5 fixes how studies are grouped for synthesis.** `および統合のために研究がどのようにグループ化されたかを記載する。` (char 419) — the grouping is a stated method item, separate from the search.
- **The negative sweeps, with their exact counts.** Form: the `.txt` read as UTF-8 (5,328 characters), the same form the spans use. Command: `python3 -c "t=open('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/e84bfe97808591d23fe3266f.txt',encoding='utf-8').read();print(len(t),{x:t.count(x) for x in ('検索者','検索担当','检索者','检索人员','検索日','検索期間','文献検索期間','检索日期','检索时间','検索式','検索戦略','检索策略','检索式','灰色文献','グレーリテラチャー','PRISMA-S','レビューア','レビュー担当者','日付','助言','司書','相談')})"` prints `5328 {'検索者': 0, '検索担当': 0, '检索者': 0, '检索人员': 0, '検索日': 0, '検索期間': 0, '文献検索期間': 0, '检索日期': 0, '检索时间': 0, '検索式': 0, '検索戦略': 2, '检索策略': 0, '检索式': 0, '灰色文献': 0, 'グレーリテラチャー': 0, 'PRISMA-S': 0, 'レビューア': 2, 'レビュー担当者': 1, '日付': 1, '助言': 1, '司書': 0, '相談': 0}` (keys as run, in the order given). Absent: `検索者`, `検索担当`, `検索日`, `検索期間`, `文献検索期間`, `検索式`, `灰色文献`, `グレーリテラチャー`, `PRISMA-S`, `司書`, `相談`, and all six simplified-Chinese terms (`检索者`, `检索人员`, `检索日期`, `检索时间`, `检索策略`, `检索式`) — the capture holds no simplified Chinese at all. Present as positive controls: `検索戦略` 2, `レビューア` 2, `レビュー担当者` 1, `日付` 1, `助言` 1.

#### Inference

- **The absence of a searcher field is item-specific, not a blanket absence of people.** `スクリーニングしたレビューアの数` (`S116`) and `データを収集したレビュー担当者の数` (`S116`) show the translation counting the people at screening and at data collection, while `検索者` and `検索担当` are 0 in the same capture form; the checklist counts a person wherever it asks for one, and it does not ask at the search.
- **The search's date is requested as a state of each source, not as a log entry.** `それぞれの情報源が最後に調べられた日付を記載する` (`S116`) asks for the last date each source was examined; `検索日` and `検索期間` are 0, so the lane may say the translation asks for a per-source date and may not say it asks for a search date or a search period.
- **The strategy is asked in full, with its filters and limits, and nothing more about the searcher.** `完全な検索戦略を記載する` (`S116`) is the whole of item 7's demand, prefaced by the filters and limits clause; a complete strategy can be reported without naming who wrote or ran it, which is what this item asks for.
- **What the checklist calls a search record ends at its output.** `検索で特定した記録数からレビューで採用した研究数まで` (`S116`) is where the search re-enters the checklist, on item 16a's reporting side; the search's own section is items 6 and 7 only.
- **Sharing is asked for data and code, and only by catch-all for anything else.** `次のうちどれが公開されており，どこにあるかを報告する` (`S116`) enumerates forms, extracted data, analysis data and analysis code; the strategy is not in the enumeration, so the lane cannot claim this checklist requires the strategy to be published as a shared artefact.
- **Registration and software are separate named fields, so the checklist's silence about a searcher is a choice, not a formatting limit.** `試験登録名と登録番号を含むレビューの登録情報を提供する` (`S116`) and `および使用したソフトウェアパッケージを記載する` (`S116`) are items that name their artefact exactly; the search items name data sources and a strategy, and name no person.
- **Grouping is a stated method item, which keeps the search items narrow.** `および統合のために研究がどのようにグループ化されたかを記載する` (`S116`) sits in item 5, before the search items; the checklist separates how studies were grouped from how they were found.
- **The advice clause is part of what item 6 asks to record, and an earlier summary dropped it.** `助言を求めた情報` (`S116`) is inside item 6's sentence beside the databases, registries, websites, organisations and reference lists; a summary that lists only the sources loses the clause under which a review records whom it asked.

#### Unknown

- **Who translated the checklist, and when, is not on the document.** The sweep counts `翻訳` 0, `監訳` 0, `訳` 0, `日本語版` 0, `ライフサイエンス` 0, `JPT` 0; the only date-bearing artefact is the PDF's own `2023-09-19T14:06+09:00` creation stamp, which dates the file, not the translation's publication. The staged row's attribution to JPT ONLINE and ライフサイエンス株式会社 is the host's, and this entry repeats it as the host's.
- **The archived copy is the newest archive state, and no further revision is observable.** The capture at the archive route is byte-identical to the 2026-04-18 memento on disk (`sha256 ba9bc9c1…399732` for both `.raw` files, 343,301 bytes; `93558b6d…0ab155` for both `.txt` files); the archive's own timemap names two mementos (`20250218234744`, `20260418151432`) and its CDX index gives both the same `digest 77FLJAP2BJCPHEZR6LAWRPWKM2BUBH4J`, with record lengths 296,572 and 300,917. That bounds what can be said: no revision is visible at the archive between those two states, and a revision made only on the dead host would not appear here.
- **The publisher's original is not reproducible from this cache.** Its capture is a 6-byte `.fail` reading `rc=28` — a curl timeout, not a recorded status — so nothing in this entry rests on a live check of the original, and the earlier entry's "HTTP 000 with zero bytes on three consecutive rounds" is replaced by the capture that exists.
- **Whether PRISMA 2020's English original words items 6 and 7 differently was not checked here.** This entry is about the Japanese checklist's own wording; the English text is a separate document and no capture of it was opened this round.
- **The count of items was read from the page, not from a published item list.** The text form holds items 1-27 with the sub-item letters above; no second rendering of the checklist was opened to cross-check the sub-item set.

```

## 6. What the lane Registry row `S116` must carry (derived from `c2-count.py`, not guessed)

- `mined`, `opened 2026-10-26`, `used-by` naming exactly the citing entry (`corpus/knowledge/japanese-prisma-item-wording-r40.md`) — the counter compares that cell and each entry's `source:` line.
- **Its source cell must have the ARCHIVE URL first.** `url_of()` reads only the first URL of a cell and normalises scheme away; the counter compares it with `url_of(DOCS[1].url)` = the archive route. Measured with the counter's own function:
  ```
  staged cell first URL -> www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf
  archive-first cell    -> web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf
  DOCS url_of(m.ARCHIVE)-> web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf
  ```
  The staged S129 cell (`merge/chousa/SOURCES.append.md:54`) leads with `**original withdrawn**: https://www.lifescience.co.jp/…`, so copying that cell shape yields `hits=[]` and this document stays `REF_ID_UNBOUND`. The dead original belongs later in the cell (or in the entry body, as the draft does), not first.
- **`anchor` needs at least one `char N` and every one of them must be a located offset.** The staged anchor cell (line 54) carries none. Verified offsets for this document: `char 419`, `char 592`, `char 753`, `char 803`, `char 991`, `char 2647`, `char 3111`, `char 4675`, `char 5157`.
- Span rows (9, all `S116`, all this entry) — the exact shape `build-spans.py` writes, digest `93558b6d…0ab155`, offsets 339/512/673/723/911/2567/3031/4595/5077 for span files `spans/S116-1.txt` … `spans/S116-9.txt`, each span 184-202 chars (longer than its quote).

## 6a. Conflict observed at integration time — the lane entry exists and is not my draft

`corpus/knowledge/japanese-prisma-item-wording-r40.md` was already adopted in the lane while this pass ran
(`ls -la` → 8,298 bytes, mtime 2026-10-26 20:11; 28 lines, 7,238 characters). I did not write it and did not
edit it; I read it once to check for conflict. Measured:
- It carries `source: S116 — <archive URL>`, `完全な検索戦略` 6×, and anchors at chars 0, 225, 453, 475, 508, 555,
  592, 619, 641, 694, 753, 766, 815, 996 (`char 13710` in its Unknown is an offset in *another* entry's
  capture, not in this 5,328-character form).
- **None of my nine quote strings occurs in it** (each count 0). Its item-8/9 phrases are sub-phrases of my
  quotes (`スクリーニングしたレビューアの数` char 815 sits inside my char-803 sentence; `データを収集したレビュー担当者の数`
  char 996 inside my char-991 sentence).
- **The two independent passes agree where they overlap**: chars 475 (item 6 body), 592 (the date sentence),
  641 (filters and limits), 753 (the strategy sentence) and 766 (`完全な検索戦略`) are located by both, from
  separate reads of the same `.txt`.
- Delta this pass adds: items 5, 13d, 16a, 24a and 27 as located quotes; the PDF-metadata identity stamp
  (no `/Author`, `dc:title 表1`, 42 numbered rows); the six-term identity sweep; and the measurement that
  closes the adopted entry's Unknown #1 — the archive route's bytes equal the 2026-04-18 memento's bytes, and
  the archive's own timemap and CDX index show exactly two mementos with one content digest.
- **Integration consequence (for the L1, not acted on here):** the C2 `in_entry` leg requires every
  `spans.tsv` quote to appear verbatim in the citing entry. If my nine rows join the manifest, those nine
  strings must be added to the entry, or the manifest must keep only the adopted entry's quotes. The two sets
  cannot coexist as they stand.

## 7. Gates I ran on the draft (all read-only; probe tree removed afterwards, paths as run)

```
$ python3 tools/inference-ground.py --entry /fast/scratch/hyaku/chousa-r52/R52GroundArchiveB/probe/corpus/knowledge/japanese-prisma-item-wording-r40.md \
    --spans /fast/scratch/hyaku/chousa-r52/R52GroundArchiveB/probe/corpus/evidence/round52/spans.tsv --counts /dev/null --registry corpus/SOURCES.md --root /fast/scratch/hyaku/chousa-r52/R52GroundArchiveB/probe
GROUND entry=corpus/knowledge/japanese-prisma-item-wording-r40.md section=1 bullets=8 tokens=10 grounded=10
GROUND: PASS                                                            (rc=0; first run: 3 INF_TOKEN_NOT_IN_SPAN on bare numerals 5,328 / 2020 / 2020, fixed by rewording)
$ python3 corpus/evidence/round51/quote-substance-check.py /fast/scratch/hyaku/chousa-r52/R52GroundArchiveB/probe/corpus/evidence/round52/spans.tsv
IDS=1 QUOTES=9 FAILURES=0                                               (rc=0)
$ python3 corpus/evidence/round52/build-spans.py --root /fast/scratch/hyaku/chousa-r52/R52GroundArchiveB/probe --cache …/.qcache --check
SPANS_ROWS=9 STALE=0                                                    (rc=0)
```
C2 legs mirrored for this document (importing the counter's own `url_of`, `key`, `form_text`, `_builder`): `in_span 9, in_entry 9, short 9, ctx 9, cap 9`, `OFFSETS [419, 592, 753, 803, 991, 2647, 3111, 4675, 5157]`, source-line regex `True`, `完全な検索戦略` 4×, foreign S-tokens `[]`.
New-ground legs, read-only: `git cat-file -e BASE:corpus/knowledge/japanese-prisma-item-wording-r40.md` → `ABSENT`; `git grep -l 完全な検索戦略 BASE -- corpus/knowledge` → no output (rc 1); Registry table row ids end at `S112` (`grep -nE "^\| S[0-9]{3} \|" corpus/SOURCES.md | tail` → `S109, S110, S111, S112`; the `S125/S126/S132/S139/S140` hits in that file are prose mentions, not rows), so `S116` is free and above the maximum.

## 8. Findings (each measured; these are the pass's falsifiers)

1. **The staged row's cell order breaks this document's binding.** `url_of` sees only the first URL; the staged cell leads with the dead original (see §6). Fix: archive URL first in the lane row. Measured with the counter's function, not read from prose.
2. **The staged `S138` anchor's "10,106 characters" is a byte count.** The form is 5,328 characters / 10,106 bytes. Any row copying that figure overstates the text by 1.9×, and the round-51 lane entry for the JAHBS article already states 5,328 characters for the same capture.
3. **The staged r40 body's "HTTP 000 with zero bytes on three consecutive rounds" is unbacked by the cache.** The original's only capture is 6 bytes reading `rc=28` — a curl timeout, which records no status and no body. The draft replaces it.
4. **The staged r40 Unknown ("whether the archived capture is the current revision … not established") is now answerable, and bounded.** The archive-route `.raw` is byte-identical to the 2026-04-18 memento on disk (`ba9bc9c1…399732`, 343,301 B each; `.txt` `93558b6d…0ab155` each); the timemap names exactly two mementos (`20250218234744`, `20260418151432`) and the CDX index gives both `digest 77FLJAP2BJCPHEZR6LAWRPWKM2BUBH4J` with record lengths 296,572 / 300,917 (WARC record sizes, not file sizes — the lengths differ while the digest agrees). So: no revision is visible at the archive between the two states; a host-only revision would not appear.
5. **The staged anchor cell cannot bind: it carries no `char N`.** The nine offsets in §6 supply them.
6. **The negative claim gets sharper, not just located.** The staged entry says the term 検索者 is absent (true: 0) but stops there; items 8, 9 and 11 of the same page ask for `レビューアの数` / `レビュー担当者の数`, and item 16a asks for the records the search identified. The checklist does count people and does count search output — the absence is specific to the search's operator, which is a claim about item structure rather than about a missing word.
7. **The date field is a state of each source, not a log field.** `それぞれの情報源が最後に調べられた日付を記載する。` (char 592) is the whole date requirement; `検索日`/`検索期間`/`文献検索期間` are 0. This sits beside the NIPH form's 文献検索期間 on the C2 theme as a contrast, not a coincidence of vocabulary.
8. **The page's identity is thinner than the staged row implies.** No printed date, translator or publisher (`翻訳`/`監訳`/`訳`/`日本語版`/`ライフサイエンス`/`JPT` all 0), no PDF author (`/Author` 0, `dc:creator` 0), and `dc:title` is the Illustrator artboard name `表1`. The entry attributes translator/host to the host, not to the document.
9. **Capture-form limit for this document: the `.txt` is the only usable form.** The raw form of a PDF `.raw` is the builder's UTF-16LE fallback (171,617 chars of garbage; my quotes occur 0 times in it), so a span here must bind to the `.txt` and its digest. This is the PDF analogue of the round-51 `.docx` capture-form defect, and it does not affect the manifest because `build-spans.py` picks the `.txt` first.

## 9. Out of scope / not done

- The A-pass report, the other three C2 documents, `tools/capture-text.py` and the C1 legs (other seats), the frozen counters themselves (not run), the lesson file `corpus/lessons/round-52.md`, the Gate/criteria text, and any lane write other than this report.
- No fetch: L0 `8d77e6c1` open; every source above is an on-disk capture, including the timemap and CDX captures (keys `9c28bfe4…` and `32401404…`).
- Not established here: the translation's translator and publication date; PRISMA 2020's English wording of items 6 and 7 (no capture opened); whether the dead host ever revised the file.

## 10. Tooling and hygiene

No install, no upgrade, no PATH change (nothing was needed; `pdfinfo`/`pdftotext`/`python3` were already present). Scratch `/fast/scratch/hyaku/chousa-r52/R52GroundArchiveB/` held the probe tree (`/fast/scratch/hyaku/chousa-r52/R52GroundArchiveB/probe/corpus/knowledge/…` + `/fast/scratch/hyaku/chousa-r52/R52GroundArchiveB/probe/corpus/evidence/round52/{quotes.tsv,spans.tsv,spans/}`) and the copies of `build-spans.py` / `inference-ground.py`; removed after assembly. Every receipt cited above is in this file. Product writes: none. Report path: `.ufo/waves/round-52/w1/R52GroundArchiveB.md`.

VERDICT: attacked the staged S129 entry and the C2 binding facts for the Japanese PRISMA 2020 checklist — 9 located quotes (all four-plus non-headline), 16 term sweeps with exact counts in the `.txt` form, an identity stamp with no author and no printed date, a full draft entry passing `inference-ground` (8/8 bullets, 10/10 tokens), `quote-substance-check` (9 quotes, 0 failures) and `build-spans --check` (9 rows, 0 stale); falsified the staged cell order (unbindable), the "10,106 characters" figure (bytes), the "HTTP 000" host claim (`rc=28`) and the "not established" currency unknown (byte-identical 2026 memento); recorded that the lane entry adopted at 20:11 carries none of these nine quote strings, so the manifest and the entry must be reconciled before C2's `in_entry` leg can pass.
