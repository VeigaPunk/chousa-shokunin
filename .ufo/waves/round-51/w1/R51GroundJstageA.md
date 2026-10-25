# R51GroundJstageA — re-ground staged S109 (日健教誌 32(2) 2024, primary-information collection)

Staged entry: `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/japanese-search-record-r38.md` (75 lines, read-only). Lane target path: `corpus/knowledge/japanese-search-record-r38.md`.
Capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/7194acc65a18f6555e4b8893.txt` (+ `.raw`, + `.pdf`). URL `https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja`.
**Form used throughout: the `.txt` read as UTF-8 (no BOM), 21216 characters** (`len(open(p, encoding='utf-8').read())`).

## 1. Capture identity (observed)
```
$ python3 -c "hashlib.sha256(b'https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja').hexdigest()[:24]"
7194acc65a18f6555e4b8893            # == cache filename stem
$ .raw 713922 bytes, starts b'%PDF-1.6\r%\xe2\xe3\xcf\xd3\r\n122 ' ; sha256 9315274a…918d69
$ .pdf 713922 bytes (same object as .raw)
$ .txt 36968 bytes, sha256 05c7ee9fe9e554614f9331c0edb8c482b8d4e04aab7dcc5fd1d8e0fc52c6171f, 21216 chars
$ pdfinfo .raw → Pages: 7, Title: "Japanese Journal of Health Education and Promotion 32(2): 118-124 (2024)"
```
The `.txt` is a two-column extraction interleaving left/right fragments per line, so the §7 sentence is split across two
non-adjacent offsets (13710 then 10232) — one sentence, not two.

## 2. Page and article identity — staged `p.121` is NOT carried; the section is on p.122
`re.finditer('\x0c', t)` → form feeds at 3031, 5705, 9322, 10182, 13817, 19132, 21215; each block's tail carries its marker:
```
0 0–3031      copyright line                                    118 (span from citation at 747)
1 3031–5705   `119` at 5595                                     119
2 5705–9322   `120       日健教誌          第 32 巻   第2 号   2024 年`  120
3 9322–10182  `121` at 10178                                    121
4 10182–13817 `122    日健教誌   第 32 巻   第2 号   2024 年` at 13780  122  ← §7
5 13817–19132 `123` at 19004                                    123
6 19132–21215 `124      日健教誌 …` at 21177                     124
```
`7.    1 次情報のまとめ` (13418) and both halves of the record sentence (13710, 10232) fall in **block 4 = p.122**.
Independent check on the original bytes (`pdftotext -layout -f 4` / `-f 5` on `.raw`): PDF page 4 ends with the printed `121`
and breaks mid-sentence in §4 (`…アウトカム指標お`); PDF page 5 opens `喜屋武` + `よび結果データを…`, ends with
`122    日健教誌   第 32 巻   第2 号   2024 年`, and contains §7, the sentence and the PRISMA note. So the staged `p.121` on
the `source:` line (staged char 168) is a one-page drift; the dispatch brief repeats it.
The heading is also mislabelled: `1 次情報の「収集」` occurs **twice** — 297 (abstract) and 1528 (intro), both p.118 — never as a
heading. The section carrying the recommendation is `1 次情報のまとめ` (13418, p.122); its first body sentence does say
`1 次情報を収集する` (13560), so "section on primary-information collection" describes the content, not the heading, and p.122.

## 3. Located quotes (each exactly once in the form stated; offsets from `t.find`)
- **159** `本稿は，これからシステマティックレビューを実施してみたいという初学者がその基礎を一通り理解で` — supports: an
  introductory methods course for beginners (title block `特別報告` 0, `特集：…方法論講座` 23) = the staged "tutorial". Does
  **not** support "peer-reviewed" or any standard status.
- **747** `〔日健教誌，2024; 32(2): 118–124〕` — supports article identity: journal, year, volume(issue), page span 118–124.
  Does **not** locate a section: the span cannot place §7 on 121 or 122.
- **13418** `7.    1 次情報のまとめ` — supports the actual heading (p.122). Does **not** support the staged `1次情報の「収集」`;
  that phrase is the abstract's four-step list (297).
- **13710** `このプロセスに際して，誰が検索を行ったの` — supports *who conducted the search* as the first element, inside §7's
  collection step (p.122). Does **not** support a named individual, a format, or the term `検索者` (`t.count('検索者') == 0`).
- **10232** `か，その日時，使用した検索式を同時に記録しておくこ` — supports the *date* (`その日時`) and *expression*
  (`使用した検索式`) recorded *together* with the searcher; it contains the staged `recheck:` run
  `その日時，使用した検索式を同時に記録しておく` (10234, once). Does **not** support "as actually run/what was typed"
  (`入力` = 0), per-database dates, or an attachment form.
- **10301** `とが望ましい．これにより，研究の透明性を保ち，他者` — supports the **advisory** modality (the only `望ましい`
  in the `.txt`, count 1 at 10303) and the transparency purpose. Does **not** support "must/required": `必要がある` at 9956
  attaches to inclusion/exclusion criteria, at 13610 to qualitative review; neither to this record. Transparency is `研究の`.
- **10370** `が同様の検索を再現できるようになる．` — supports the stated reason: **others can reproduce the same search**
  (`再現` count 1). Does **not** support that reproduction was tested, or that the same results are guaranteed.
- **12666** `PRISMA は，日本語を含め 9），複数の` — supports PRISMA translated, Japanese included, into multiple languages.
  Does **not** support a count ("several other languages": text says `複数の言語`, no number, footnotes 9) 10)), and it is in
  §8 結果の報告・論文執筆 (p.122), not the search-record section.
- **12815** `チェックリストも付録されてい` — supports a checklist appended (`付録` count 1). Does **not** support that the
  checklist is in *this* article's appendix; `付録` refers to PRISMA's supplement.
- **13780** `122    日健教誌   第 32 巻   第2 号   2024 年` — supports: the block holding §7 closes with running head **122**.
  Does **not** by itself place the heading; the block table in §2 does.

### Machine lines
```
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	本稿は，これからシステマティックレビューを実施してみたいという初学者がその基礎を一通り理解で	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	〔日健教誌，2024; 32(2): 118–124〕	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	7.    1 次情報のまとめ	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	このプロセスに際して，誰が検索を行ったの	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	か，その日時，使用した検索式を同時に記録しておくこ	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	とが望ましい．これにより，研究の透明性を保ち，他者	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	が同様の検索を再現できるようになる．	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	PRISMA は，日本語を含め 9），複数の	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	チェックリストも付録されてい	corpus/knowledge/japanese-search-record-r38.md
QUOTE	S109	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja	122    日健教誌   第 32 巻   第2 号   2024 年	corpus/knowledge/japanese-search-record-r38.md
```

## 4. Staged claims about S109 that the capture does NOT carry
1. **`p.121`** (source line, staged char 168) — the section and the sentence are on **p.122** (§2); the `121` block
   (9322–10182) ends mid-sentence in §4 and carries no part of §7.
2. **`the section on 1次情報の「収集」`** — no such heading; it is `7.    1 次情報のまとめ` (13418). The quoted phrase occurs
   only in the abstract (297) and intro (1528), both p.118.
3. **`The three are stated as one record, not three`** — capture says `同時に記録しておく` (record at the same time; `同時に`
   count 1 at 10247). "One record"/a single field is not stated; "together" is.
4. **`translated into Japanese and several other languages`** — text says `複数の言語`, no count; "several" adds a number.
5. **`the review's transparency`** — text says `研究の透明性` (the research's), 研究の透明性 count 1.
6. **`the date`** — text says `その日時` (date *and time*); 日時 count 1 at 10236.
7. **Inference `the attachment must hold what was typed, not a reconstruction` / "as actually run"** — not in this document:
   `使用した検索式` is all it says, `入力` = 0. The typed/attachment force is S110's (V)-5 form, absent from this capture.
8. **Inference `PRISMA-S and Cochrane both ask for these`** — not carried: the only `PRISMA-S` substring is inside
   `PRISMA-ScR` at 18441 (ref. 12, a scoping-review guideline title); the four `Cochrane` hits are the Cochrane Library
   registry entry (7243, 12898/12916) and the Cochrane handbook reference (14014), none a search-record requirement.
9. **Entry scope (for the judge; C2 frozen, no predicate change proposed)** — this staged entry cites **two** documents (S109,
   S110) while C2 reads "adopted BY DOCUMENT". S109 alone supports only the searcher/date/expression triple plus the
   reproduction reason; databases-per-source, hand-searching and (V)-5 in the entry are S110.

Carried and confirmed verbatim: the triple (who / date / expression), the `同時に` "together" force, the advisory `望ましい`, the reproduction rationale, the PRISMA-translation note, the checklist, the journal/year/volume/issue/page-span identity, the tutorial characterisation, and the `recheck:` run `その日時，使用した検索式を同時に記録しておく` (10234, once).

## 5. Commands run (all read-only; no network; no install; no pacman)
```
$ python3 … sha256(b'<url>').hexdigest()[:24] → 7194acc65a18f6555e4b8893 (== cache stem)
$ python3 … len(open(txt,'utf-8').read()) → 21216 ; first 3 bytes b'\xe7\x89\xb9' (no BOM)
$ python3 … re.finditer('\x0c',t) → [3031,5705,9322,10182,13817,19132,21215]
$ python3 … t.count(q) for all ten quotes → 1 each ; t.find(q) → 159,747,13418,13710,10232,10301,10370,12666,12815,13780
$ python3 … counts: 望ましい 1@10303, 同時に 1@10247, 再現 1@10377, 日時 1@10236, 検索者 0, 入力 0, 付録 1@12823,
            翻訳 1@12735, 1 次情報の「収集」 2@[297,1528], 必要がある 2@[9956,13610], 求められ 2@[7922,10940]
$ pdfinfo .raw → Pages: 7 ; pdftotext -layout -f 4 → footer 121 ; -f 5 → footer "122 …2024 年" + §7 + sentence
$ python3 … each quote tested against p1.txt / p5.txt (pdftotext -layout of PDF pages 1 and 5): all ten found once on the
            page §2 assigns (p1: 747,159 ; p5: the other eight)
```
Scratch `/dev/shm/chousa-r51-R51GroundJstageA/` (p1.txt, p5.txt) deleted after the checks. No file under `chousa-shokunin`,
`shokuknow`, or the fleet repo was modified; the only write is this report. No tool installed (none needed).

VERDICT: attacked the staged S109 claims against the on-disk `.txt` (21216 chars, UTF-8) — the who/date/expression triple, its
`同時に` force, the advisory `望ましい`, the reproduction reason and the PRISMA-translation note all hold verbatim, while the
staged `p.121` is really p.122, the cited section is `1 次情報のまとめ` (not `「収集」`), and "one record", "several other
languages", "as actually run" and the PRISMA-S/Cochrane parentage are staged claims the capture does not carry.
