# R54ScoutCoverage — coverage-map ground check (round 54 wave 1)

Seat: scout (read-only). Lane tip read: `9caf8fc`; base `c49ffc6c`. Captures: `.qcache` = `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`; key = sha256(URL)[:24] (recomputed here: SAMR `adf6ba934e813b2c326fa150`, openstd `b9ca2a4fdf9455867534f144`, JMU `0f33243fd7ac2fe88b85c1ba`, HIT `6dc68fd6b32ce9c8dfcebce8`). Tooling: none installed. Scratch removed (`pgrep -u $USER -f UserInstallation=file://<scratch>` -> 0; no LibreOffice run).

## 1. Base sweep (command, rc, output)
```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -l -e 'ISO 690:2021' -e 文献载体标识 c49ffc6ce1c3de87c1dfa96856239ed7274bf07b -- corpus/knowledge
(no output)   rc=1
$ git ls-tree -r --name-only c49ffc6c… corpus/knowledge | grep -c taxonomy   ->  0
```
Neither taxonomy entry exists at base; neither term is held. Both terms are CJK/ASCII as typed; the JMU capture holds the carrier term as `文献载体标识` (ordinary CJK; digits/Latin there are full-width), so the sweep term matches the capture.

## 2. Coverage map: where the lane stands (base c49ffc6c) and what each document touches
The coverage map is `corpus/README.md`: a table (`:5-:87`, then rows appended at `:1049-:1081`) and per-round sections `## Round51/52/53 coverage and frontier` (`:1085`, `:1113`, `:1140`) each with `### Frontier` (Advanced / Left open). There is NO row or frontier line about the citation-standard theme itself; the nearest rows are:

| Held row | Path:line | What it holds of this theme |
|---|---|---|
| `knowledge/citation-count-semantics-r37.md` (S101 HIT spec) | README:1072; entry `:24-31` (文献标志码; `文献类型及载体类型标志` `:27`; 14.1 recommends `GB/T 7714` 顺序编码制/作者-出版年制 `:28`; 14.4 `参照ISO 690及ISO 690-2` `:30`; table `参照ISO 690` `:31`), `:69`, `:84-86` | GB/T 7714 and ISO 690 only as UNVERSIONED names inside a pre-2025 data specification; its Unknown `:79-80` "whether the specification copy (S101) is the version in force" |
| `knowledge/citation-version-binding-r36.md` | README:1061; entry `:21`; `lessons/round-44.md:108-111` | staged S082 (the SAMR record) REFUSED with flip: "a text capture of that record contains the issued and effective dates as a contiguous span" |
| `lessons/round-47.md:243-250` | | S101's `.txt` sidecar has zero hits for 文献标志码 (confirmed: sidecar is mojibake, 128,416 chars, 0 hits for 文献标志码/GB/T 7714/ISO 690) |
| `corpus/SOURCES.md:111` S101 | status `mined`, opened 2026-10-25, used-by = `corpus/knowledge/citation-count-semantics-r37.md` only | the held row that must gain the r37 entry if cited |
| `corpus/evidence/round43/absent-split.tsv:2` | `S082 not-carried` (campaign id) | the round-43 verdict behind the refusal |

Sweep for anything else: `git grep -n -e 引用日期 -e 访问日期 -e 著录规则 -e 载体 -e 参考文献著录 c49ffc6c -- corpus/knowledge` -> one hit only (`citation-count-semantics-r37.md:27`, `载体`). `git grep -e std.samr.gov.cn -e openstd.samr -e xuebaobangong` at base -> no hit in `corpus/` (only `jc.hit.edu.cn` rows). No Registry row carries the SAMR, openstd or JMU URL.

## 3. Per-document verdict (opened from capture bytes this round)
Offsets are python `text.find(quote)` on the `.txt` sidecar as UTF-8; each quote is on ONE line and occurs exactly once (count checked).

### A. SAMR record (planned lane S121) — NEW GROUND, advances a refused flip
Capture `.txt` 6,626 B (HTML text form, one fact per line; 996 lines).
| Fact | Quote (offset) | Status vs lane |
|---|---|---|
| status 现行, published, in force | `发布 于 2025-12-02` (1029); `实施 于 2026-07-01` (1048) — txt lines 268, 270 | new (lane holds no edition) |
| replaces 2015 | `（全部代替）` (1162, line 307) after `GB/T 7714-2015` (301); `全部代替标准` (1415) | new |
| non-equivalent adoption | `本标准非等效采用ISO国际标准：ISO 690:2021。` (1797, line 468, 2 words/29 chars); `采标中文名称:信息与文献 参考文献和信息资源引用指南。` (1829, line 470) | NEW: `ISO 690:2021` held nowhere; only SAMR carries it (JMU: 0 hits, see C) |
| identity | title lines 145-147; 标准号 `GB/T 7714-2025` line 367; CCS A14 line 408; ICS 01.140.20 line 415; 国家标准委 line 452; plan 20240256-T-469 line 396 | new |
Finding (flip): the dates are NOT one contiguous line here — `发布 于 2025-12-02 \n\n 实施 于 2026-07-01` crosses two line breaks (1029..1063). The round-44 flip text ("contiguous span") is met only as a multi-line span; a one-line located quote cannot hold both. The JMU cover line does hold both on one line (C). Two single-date quotes are the SAMR route. `现行` occurs 2x and `GB/T 7714-2015` 2x: not usable as quotes.

### B. openstd notice (planned lane S122) — NEW GROUND, narrow; second carrier of S121's facts
Capture: `.txt` is byte-identical to `.raw` (`cmp` -> same): it is raw HTML (22,007 chars), not a text form; the notice is one HTML line.
- `该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务` (offset 15188; count 1; 47 chars, 1 whitespace word). Context: status `现行` (14510), CCS A14, ICS 01.140.20, `发布日期` 2025-12-02 (16105), `实施日期` 2026-07-01 (16321) in separate table cells.
- It names ISO/IEC generically, NOT `ISO 690` (0 hits) and NOT the replaced edition (`7714-2015`, `代替` 0 hits). The link "no text because the standard adopts ISO 690:2021" is an inference joining S121 line 468 with this sentence; the capture does not say it.
- Credit per README practice: the notice is the one fact absent from every other lane document (`git grep -c 本系统不提供文本阅读服务 c49ffc6c -- corpus` rc=1, no output; no row carries the URL); status/dates/CCS/ICS duplicate S121. Per `README:1124` (梅斯医学 earned nothing as a second carrier) and `README:1149` (S119 credited because it alone carries the issuance facts), credit S122 only for the notice sentence; an entry resting on S122 for more earns nothing more.

### C. JMU copy (planned lane S123) — NEW GROUND (scope, codes, dates); NOT a source for ISO 690:2021
Capture `.pdf`=`.raw`; `.txt` 190,614 B / 83,061 chars / 1,834 lines, text layer rendered FULL-WIDTH (`ＧＢ／Ｔ ７７１４—２０２５`, digits `２０２５`, Latin `Ａ`, `ＹＹＹＹ－ＭＭ－ＤＤ`). Any quote must keep full-width (the staged entry's ASCII `GB/T 7714-2025`, `YYYY-MM-DD`, `7.3` forms are absent in the capture).
| Fact | Quote (offset; txt line) | Status |
|---|---|---|
| issue/effective dates on one line | `２０２５－１２－０２发布                                                      ２０２６－０７－０１实施` (424; line 22; 2 words/78 chars; 56 spaces between) | new; meets the r44 flip as one line |
| replaces 2015 | `本文件代替ＧＢ／Ｔ ７７１４—２０１５《信息与文献 参考文献著录规则》，与ＧＢ／Ｔ ７７１４—２０１５ 相比，除` (3602; line 105); `——本次为第三次修订。` (5375; line 149) | duplicates S121 (same fact, second carrier) |
| scope clause (applies) | `本文件适用于作者和编制者著录参考文献。` (5576; line 165) | NEW |
| scope clause (excludes) | `本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。` (5602; line 166, 33 chars) | NEW |
| type + carrier rule | heading `７．３ 文献类型标识、文献载体标识` occurs 2x (TOC + body): NOT usable; body `文献类型标识、文献载体标识应按照附录Ａ著录。电子资源既应著录文献类型标识，也应著录文` (11542; line 361); the sentence ends on line 362 (`献载体标识。`) so it cannot be quoted whole | NEW (`文献载体标识` held nowhere at base) |
| 17 types | Table A.1 lines 1345-1361: M J N C D R S P EB A CM DS PP G CP DB Z = 17 (11 one-letter, 6 two-letter); one-row quote `期刊                          Ｊ` (58013; line 1346) | NEW |
| 5 carriers | Table A.2 lines 1376-1380: MT DK CD OL MM; `联机网络（ｏｎｌｉｎｅ）                         ＯＬ` (59161; line 1379) | NEW |
| date rule | `电子资源的创建日期、发布日期、修改日期、引用日期应按照“ＹＹＹＹ－ＭＭ－ＤＤ”格式，用阿拉伯数字` (14096; line 450); example `示例：（２０１２－０５－０３）［２０１３－１１－１２］` (14151; line 452) | NEW (`引用日期` held nowhere at base) |
| change list | `ｏ）将文献类型“普通图书”“舆图”分别更改为“图书”“地图”，增加了文献类型“预印本”及其标识` (4734; line 132); `代码“ＰＰ”（见附录Ａ，２０１５年版的附录Ｂ），增加了电子资源载体“缩微资料”及其标识代码` (4788; line 133); `“ＭＭ”（见附录 Ａ），将“ＥＢ”代表的文献类型更改为“网站、网页”（见附录Ａ，２０１５ 年版` (4840; line 134) | NEW |
`ISO 690`, `ＩＳＯ ６９０`, `６９０`, `非等效`: 0 hits in JMU; its 10 `采用` hits are all drafting rules (e.g. 引文采用序号标注, 出版年应采用公元纪年), none an adoption statement; its only ＩＳＯ hits are ISO 4, ISO 21378, ISO/IEC 80079 and the ISO home page. So the non-equivalence claim rests on S121 alone.

## 4. Held vs advanced vs new (what the entries may claim as coverage)
- HELD already (no credit): the unversioned pairing "GB/T 7714 recommended, ISO 690 for layout" and the element name `文献类型及载体类型标志` — `citation-count-semantics-r37.md:27-31` (S101); HIT's `.txt` sidecar unusable (`round-47.md:247`), held quotes live at UTF-16LE raw offsets (`lessons/round-49.md:95-100`).
- FRONTIER ADVANCED: (i) the round-44 refused flip (`citation-version-binding-r36.md:21`, `round-44.md:108-111`): met by S121 as two single-date quotes and by S123 line 22 as one line; (ii) the S101 Unknown (`citation-count-semantics-r37.md:79-80`, "version in force"): S121+S123 show the 2025 edition replaced 2015 and moved to a numbered type/carrier table; they do NOT say what S101's older type list was (HIT text not re-read by the entries); (iii) `README:1156` carrier discipline — here the carrier split recurs: S121 carries identity/dates/replacement/ISO basis, S122 only the no-text notice, S123 the wording.
- NEW GROUND: ISO 690:2021 non-equivalent adoption; edition/dates/replacement; the openstd no-text notice; scope clause; the 17-type/5-carrier tables; the 7.3 and 7.6 rules; the 2015->2025 change list.
- NOT advanced / do not claim: `README:1107`-style "national standard for search reporting" (GB/T 7714 is a citation-description standard, not a search-reporting one; `chinese-search-record-r39.md:34` stays open); no PRC body's tier-A anchor for the lane's tier rule.
- Ground-line defect: both staged entries' `ground:` cite "frontier item 3 — source-tier adjudication" / "wave-1 queue Q1". `git grep -n -i -e 'frontier item' -e 'source-tier adjudication' c49ffc6c -- corpus` finds no lane referent. The lane's `## Frontier` has no numbered item 3; cite the real ones above (README:1156; `citation-version-binding-r36.md:21`; `citation-count-semantics-r37.md:79-80`).

## 5. Staged-text defects seen against the captures (for the entry reviewers; entries are not mine)
1. r37 staged: "17 document types with single-letter codes" — false: 6 of 17 are two-letter (EB CM DS PP CP DB; JMU lines 1353-1359).
2. r37 staged change list "图书 and 舆图 were replaced by 图书 and 地图" — capture (line 132): 普通图书 -> 图书 and 舆图 -> 地图.
3. r36 staged Inference attributes the scope clause (`excludes librarians…`) to the standard while its two sources are S085/S086 (SAMR, openstd), which do not hold it (0 hits for 图书馆员 in both captures, `grep -c`). The clause lives only in S123; the entry must cite S123 or drop it.
4. r36 staged Unknown cites a reseller "HTTP 403" and a reseller table of contents: no capture of it in `.qcache`; uncheckable, keep as Unknown only.
5. r37 staged says S101 data spec "defers to GB/T 7714": S101 recommends it (14.1) while its own layout rule (14.4) and parameter table say ISO 690 (`citation-count-semantics-r37.md:84-86`); do not write "defers".

## 6. C1 side-observation (candidate tool on S101; informational, not a score)
`python3 tools/capture-text.py <HIT .raw>` -> rc 0, 27,012 chars, no U+FFFD; all five held S101 quotes occur exactly once in it (文献标志码 at 12007, `文献类型及载体类型标志` 12963, 14.1 sentence 12795, `参考文献格式，参照ISO 690` 25123, 14.4 sentence 14049); `--locate` printed `LOCATED count=1 offset=12007`. Offsets differ from round-49's UTF-16LE char offsets (11205 etc.), so an r37 entry citing S101 with the tool's text form must record the new offsets; no new span is needed only if round-49's are kept.

## 7. Draft README rows for the L1 (intended path `corpus/README.md`, new `## Round54 coverage and frontier`)
Credit is per document: three bound documents at most (S121 SAMR record, S122 openstd notice — notice sentence only, S123 JMU copy); S101 (held) earns none. Base sweep as given in section 1 (`rc=1`, no output).

VERDICT: coverage-mapped all three documents against base c49ffc6c — S121 and S123 new ground, S122 new for its one notice sentence only; the round-44 SAMR flip is met only as two single-date quotes (SAMR) or one line (JMU cover); ISO 690:2021 is carried by S121 alone; base sweep rc=1 empty; five staged-text defects found.
