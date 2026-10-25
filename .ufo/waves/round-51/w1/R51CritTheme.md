# R51CritTheme — C2's axis and expansion credit

Read-only critique of the three staged C2 entries. No counter run; no tool installed; no scratch.
## 1. What the lane actually holds at base `9ec1751a`

```
$ git grep -n -e 検索 -e 检索 -e PRISMA-S 9ec1751a -- corpus
  corpus/SOURCES.md:110-114 (S100-S104, CNKI/ISTIC rows); round49/50 evidence tsv+spans only
$ for t in 検索者 参照日 灰色文献 ハンドサーチ 別紙様式 检索策略 万方 SinoMed 中国生物医学文献数据库 主题词 学科分类号; do
    git grep -n -- "$t" 9ec1751a -- corpus/knowledge; done            → 0 hits, every term
$ grep -n "s13643-020-01542-z" corpus/SOURCES.md; grep -n "PRISMA-S" corpus/SOURCES.md   → 0 hits
$ grep -n -i prisma 9ec1751a -- corpus/knowledge → only search-log-method-r39.md:27 and
  citation-version-binding-r36.md:28 (id-provenance notes)
$ grep -n -E "^\| S077 " corpus/SOURCES.md → pdftotext manual;  S079 → RFC 7089
```

Held search/record ground is `search-log-method-r39.md:10-16` (a log *document*, updated in
place, recall-checked — S078 Europe PMC/JMLA), the currency position (`recheck-due-r26.md:9-16`,
`metadata-screen-r25.md:21-22`), the claim-vs-check separation (`claim-support-states-r24.md:8-16`)
and the sweep re-run gap (`sweeps-rejections-r5`). **No PRISMA-S ground is held**: the only
PRISMA-S artifact is a twice-refused staged entry whose capture is a 267-byte challenge page
(`lessons/round-47.md:252`; `01f657b3d0ab045c494b3f92.txt`).

## 2. The assigned question

"A Japanese search record carries the searcher, the date and the expression" is
**new relative to held ground** — no held entry names any of the three fields, and
`search-log-method-r39.md` is the log-as-document half, not PRISMA-S. But the premise
"PRISMA-S ground the lane holds" is false: no PRISMA-S item text is held or obtainable on
disk (`PRISMA-S` in 8 captures, none holds an item list; `01542-z` only inside the JMLA
commentary `0ae65ac01b93119d3c2f3fed.txt`), so the comparative claims are unsourced.

## 3. Duplicates (no credit) vs new ground

| staged claim | held ground | class |
|---|---|---|
| `japanese-search-record-r38.md:44-47` "would let a sweep be re-run rather than re-guessed" | `search-log-method-r39.md:10-16`; `sweeps-rejections-r5` | **dup** (only the field set is new) |
| `r38:37` "PRISMA-S and Cochrane both ask for these" | nothing held; Cochrane ch.4 on disk `c9d1e74c…:114456` | unsourced |
| `r38:52-56` "the lane's own `S105` already separates…" | `claim-support-states-r24.md:8-16` | **dup + misbound id** |
| `chinese-search-record-r39.md:58-65` "a search record a reader can re-run … verify-sweeps cannot check" | `search-log-method-r39.md:6,16` | **dup** |
| `r39:43-50` "not a copy of PRISMA-S's sixteen items … no counterpart in PRISMA-S's checklist" | nothing held; `42bac883…:924` gives only "包含16个条目" | unverifiable |
| `r39:51-55` "Grey literature is the Chinese requirement the lane's Western anchors do not carry" | **falsified**: `c9d1e74c3ac8d9eb332c9770.txt` char 53386 `C28 : Searching for grey literature ( Highly desirable )` (staged S083, `SOURCES.append.md:8`) | false as stated |
| `amendment:41-44` "the rationale is the lane's own rationale" | `recheck-due-r26.md:9-16`; `metadata-screen-r25.md:21-22` | **dup**, self-declared confirmation |
| `amendment:45-53` Q12 "searcher … appears in … round 3's `S097`" | `62be15a4…:4409` — the r38 entry's own source `S110` | **double count + misbound id** |

New ground (credit), all on disk and absent from the lane registry (0 hits for the seven host
fragments): `S109:10234` searcher/date/expression as one record with a reproduction rationale;
`S110:4409` per-database last-search date, hand-search declaration, (V)-5 attachment; `S125` docx
`word/document.xml` (tags stripped) 9729 search window with a fixed end point; `S126:11294`
database + **provider** + window with a currency rationale; `S116:15307` module 3 (databases,
time range with terms and their logic, grey literature); `S117:11428` a published record.

## 4. Strongest counterexamples

1. **Q12 credits one document twice.** `amendment:48-50` places the searcher's identity in
   "the functional-foods notification form (round 3's `S097`)", while `r38:25-28` records the
   same field from `S110`. Staged `S097` is **FEVER** (`claim-support-test-r37.md:4`,
   `SOURCES.append.md:22`); staged `S105`/`S106` are lane own-work rows (`SOURCES.append.md:30-31`).
   By document, the amendment adds zero documents for its Q12 answer.
2. **"Series" is one group.** `r39:28` "The reception is a series, not a single paper" rests
   on `S119`, whose own row declares it "**the same item**" as `S141` (`SOURCES.append.md:44`
   vs `:66`); the `S119` capture's author list (郑卿勇; 周泳佳; 田晨; 许建国; 李腾飞 …) is the
   author set of `S116` and `S117` — three outputs, one group, one journal, not a reception series.
3. **`r39:39` "The Chinese literature … says so" about PRISMA-S.** `fd468a36…` holds
   `PRISMA-S` **0** times (`PRISMA` 12, `灰色` 3); its absence sentence is
   `尚无专门针对动物实验 SR 的报告规范` (char 17709) — animal-experiment reporting, not
   PRISMA-S adoption.
4. **`amendment:30-38` "It does [exist]" vs its own Unknown `:68-70`** — an institute's
   template plus a journal article is not a standard, and the entry concedes the form binds one institute.
5. **`S125`'s quote form is unusable as cached.** The `.txt` is the docx ZIP decoded as text
   (168,952 chars; `文献検索期間` 0, `明記する` 0); the quote exists only in the extracted
   `word/document.xml` tags-stripped text (20,592 chars) at 9729.
6. **Anchor drift (round-50 filename-drift class).** `r38:4` anchors "1次情報の「収集」" (the
   step, capture 299) while its own registry row says "1次情報のまとめ" (the section, capture
   13426 as `1 次情報のまとめ`); neither string matches byte-exactly.

Located quotes (byte-exact, unique in the named form):

| quote | capture form | offset | n |
|---|---|---|---|
| `C28 : Searching for grey literature ( Highly desirable )` | `c9d1e74c3ac8d9eb332c9770.txt` as UTF-8 | 53386 | 1 |
| `検索者、検索ワード、検索式` | `62be15a474e866e4bef6c9d5.txt` as UTF-8 | 4409 | 1 |
| `その日時，使用した検索式を同時に記録しておく` | `7194acc65a18f6555e4b8893.txt` as UTF-8 | 10234 | 1 |
| `検索の開始日と終了日を記載することで` | `34fcefc159bf2ebbd1e09540.txt` as UTF-8 | 11294 | 1 |
| `为文献检索报告提供了包含16个条目的专项规范` | `42bac8830527d6f1bb125c49.txt` as UTF-8 | 924 | 1 |
| `（3）灰色文献的检索与记录` | `fd468a36d78ff156b6200946.txt` as UTF-8 | 15307 | 1 |
| `SRにおける文献検索期間について明記する` | `3a8b45977cd111e45e3980a5.raw` → `word/document.xml`, tags stripped, UTF-8 | 9729 | 1 |

## 5. Impacted axes

- **depth**: improved only after narrowing — the six field facts are real and new, but the
  inference layer adds three unsourced comparisons, one falsified contrast, one
  self-contradiction and two misbound ids, so SCORECARD's "independently verified domain
  fact" test is not met by the comparison layer.
- **expansion**: +7 new documents, improved at document level; `S109`/`S125`/`S126`/`S116`/
  `S117` add in-province method ground, `S110` is a functional-foods claims-dossier form
  (admissible by the CNKI-manual precedent, not a research standard), `S119` is staged
  `S141`'s item, `S097`/`S105`/`S106` add nothing.
- **operability/calibration**: untouched; the `S125` form defect and five stale body ids hit
  C2's QUOTE and REF legs, not the counter's target.

## 6. Smallest safe correction
1. Replace the five stale body ids with file-path descriptions, or re-point them to
   `S110`/`S116`/`S117`; never carry `S097`/`S105`/`S106`.
2. Demote every PRISMA-S item claim to Unknown; keep only "16 items" cited to `S119:924`,
   and cite Cochrane ch.4 (staged S083, `c9d1e74c…:53386`, `:114456`) as the comparator.
3. State `S125`'s form as the extracted `word/document.xml` (tags stripped) at 9729.
4. Narrow "series" to "one group's three outputs in one journal" and "a standard exists"
   to what the form and article actually bind.

## 7. Verdict per document

| document set | depth | expansion |
|---|---|---|
| `japanese-search-record-r38.md` (S109, S110) | **improved** — three-field record, per-database date, (V)-5 attachment, all on disk | **improved**, +2 docs; conditional on dropping the `S105` misbinding and the PRISMA-S/Cochrane comparison |
| `chinese-search-record-r39.md` (S116, S117, S119) | **improved** on module 3 and the worked record; **unchanged/negative** on "series" and "no counterpart" | **improved**, +3 docs, but `S119` is staged `S141`'s item |
| `japanese-search-record-r38-amendment-2026-10-23.md` (S125, S126) | **improved** on window and provider; Q12 adds no document and one false id; "standard exists" contradicted internally | **improved**, +2 docs |
| comparators `claim-record-fields-r33`, `evidence-snapshot-coverage-r40` | **zero overlap** with the theme — they cannot be the duplication check; the real comparators are `search-log-method-r39`, `recheck-due-r26`, `metadata-screen-r25`, `claim-support-states-r24` | — |

VERDICT: attacked C2's depth and expansion credit — the six field facts are genuinely new and on disk, but three inference claims are unsourced (PRISMA-S item text is a 267-byte challenge page), one is falsified by the campaign's own Cochrane ch.4 capture, Q12 double-counts `S110` under a stale `S097`, and "series" is one group's three outputs; depth improved per document only after those five narrowings, expansion improved (+7 documents) as documents but not as reception.
