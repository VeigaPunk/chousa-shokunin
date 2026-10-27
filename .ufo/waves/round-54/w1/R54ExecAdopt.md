# R54ExecAdopt — lane adopter run (round 54, wave 1)

Seat R54ExecAdopt (leaf; no dispatch, no counter/production write). Scratch `/fast/scratch/hyaku/chousa-r54/R54ExecAdopt`
(removed at exit; `pgrep -u $USER -f "UserInstallation=file://$S"` prints nothing — no `soffice` was run). Lane HEAD
`9caf8fc`, freeze `5a1a206`, `BASE_REV` `c49ffc6`. No fetch. **No tool installed or upgraded** (`pdftotext` already at
`/usr/bin/pdftotext`).
## 1. Adopter run — exit, stdout, stderr
```
TMPDIR=$PWD python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/assimilate-rows.py \
  --staged /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md \
  --knowledge /home/vgpnk/Projects/shokuknow/merge/chousa/knowledge \
  --registry /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md \
  --opened 2026-10-26 --out $PWD/out \
  --entry corpus/knowledge/source-type-taxonomy-r36.md --entry corpus/knowledge/source-type-taxonomy-r37.md
```
`EXIT=0`; **stderr empty**; stdout verbatim `COLLISIONS=39` / `CITED=4 APPEND=3 HELD=1 TWIN=0` / `BODYONLY=0`.
`COLLISIONS=39` = lane ids S082..S120 reused by the staged file for *other* documents (staged S085/S086/S093 are
the GB/T theme; lane S085/S086/S093 are FEVER, FEVER, climate-fever). The tool maps by document URL, not by id, and
minted S121..S123 — correct.
## 2. Map — CONFIRMED (`renumber.tsv`, header + 4 rows)
```
staged_id	lane_id	action	url
S085	S121	append	std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F
S086	S122	append	openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14
S093	S123	append	xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf
S101	S101	held	jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc
```
Expected `S085->S121 S086->S122 S093->S123 S101 held` — exactly as predicted. `S101` maps to itself because lane
S101 already carries that `.doc` URL, so the staged row appends nothing.
## 3. `bodyonly.tsv` / `stripped.tsv`
`bodyonly.tsv` = header only (`entry<TAB>staged_id`); no *staged* id is left body-only. §7.1 shows the guard cannot
see the token that matters.
```
lane_id	column	stripped
S121	recheck	180d — re-open the SAMR detail record and confirm 发布日期 2025-12-02 and 实施日期 2026-07-01 are unchanged (ran 2026-10-23)
S121	opened	2026-10-23
S121	used-by	corpus/knowledge/citation-version-binding-r36.md, corpus/knowledge/source-type-taxonomy-r36.md
S122	recheck	180d — re-open the openstd record and confirm the notice still reads "本系统不提供文本阅读服务" (ran 2026-10-23)
S122	opened	2026-10-23
S123	recheck	180d — re-download the PDF and confirm section 7.3 still reads "电子资源既应著录文献类型标识，也应著录文献载体标识" (ran 2026-10-23)
S123	opened	2026-10-23
```
The S121 `used-by` strip is not a loss: the staged package wanted `citation-version-binding-r36.md` as a citer, but
the lane's copy of that entry carries only `source: S079` (its `ground:` line says "Staged S082 (the GB/T record) is
not cited"), so the adopter's narrowing to the one real citer is what the counter needs.
## 4. `append.md` — 3 rows, 11 cells each (measured `ncells 11`)
```
| S121 | GB/T 7714-2025 信息与文献 参考文献著录规则 — 全国标准信息公共服务平台 (国家市场监督管理总局 / 国家标准化管理委员会) — https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F | docs | A | the identity, status and adoption basis of the current PRC national standard for bibliographic references and citations | 基础信息 table and 采标情况 block on the standard's detail record; record read 2026-10-23 | GB/T 7714-2025 was issued 2025-12-02 and took effect 2026-07-01, wholly replacing GB/T 7714-2015; it is a non-equivalent adoption of ISO 690:2021, Chinese title 信息与文献 参考文献和信息资源引用指南; ICS 01.140.20, CCS A14, supervised by the national standardisation administration | mined | 2026-10-26 | 180d | corpus/knowledge/source-type-taxonomy-r36.md |
| S122 | 国家标准 GB/T 7714-2025 在线预览 — 全国标准信息公共服务平台 (openstd) — http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14 | docs | A | whether the operative text of the current Chinese citation standard is publicly readable at the official full-text portal | the full-text notice on the standard's openstd record; record read 2026-10-23 | because the standard adopts ISO/IEC international standards, the official portal refuses text reading for copyright reasons and serves only metadata - status, dates, ICS/CCS, supervising body; the Chinese rules themselves are therefore not publicly verifiable from the authority | mined | 2026-10-26 | 180d | corpus/knowledge/source-type-taxonomy-r36.md |
| S123 | GB/T 7714—2025《信息与文献 参考文献著录规则》full text, copy hosted by the 集美大学学报 editorial office — https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf | docs | B | the operative text of the current PRC citation standard as reproduced by a university journal editorial office's copy; the authority serves no text (see S075), so this row is scoped to the reproduction and not to the standard | sections 1 范围, 5.2, 7.3, 7.6, 7.9, 8.15 and 附录A 表A.1 / 表A.2; PDF text extracted with pdftotext, read 2026-10-23 | the standard's own scope clause limits it to the author side: 本文件适用于作者和编制者著录参考文献; and expressly excludes 图书馆员、文献目录编制者以及索引编制者; the type rule is 电子资源既应著录文献类型标识，也应著录文献载体标识; 附录A lists 17 document types with codes (图书 M, 期刊 J, 报纸 N, 会议录 C, 学位论文 D, 报告 R, 标准 S, 专利 P, 网站、网页 EB, 档案 A, 地图 CM, 数据集 DS, 预印本 PP, 汇编 G, 计算机程序 CP, 数据库 DB, 其他 Z) and 5 carrier codes (MT, DK, CD, OL, MM); §7.6 requires creation/publication/modification date and 引用日期 in YYYY-MM-DD | mined | 2026-10-26 | 180d | corpus/knowledge/source-type-taxonomy-r37.md |
```
## 5. Rewritten entries — `source:` lines
```
r36: source: S121 — https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F — 基础信息 and 采标情况 — record read 2026-10-23
r36: source: S122 — http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14 — the full-text notice on the standard's openstd record — record read 2026-10-23
r37: source: S123 — https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf — sections 1, 7.3, 7.6 和 附录A 表A.1/表A.2 — PDF text extracted 2026-10-23
r37: source: S101 — https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc — sections 11 and 14 — document text extracted 2026-10-23
```
## 6. S101 (held) `used-by` cell — exact old → new
The adopter never touches a held row, and r37's own `source: S101 — <that .doc url>` line makes the held citation
real; `c2-count.py:186-196` then requires `e in used` for that citing entry. So (`corpus/SOURCES.md:111`, cell 12):
- **old** (verbatim): `corpus/knowledge/citation-count-semantics-r37.md`
- **new**: `corpus/knowledge/citation-count-semantics-r37.md, corpus/knowledge/source-type-taxonomy-r37.md`
`citation-count-semantics-r37.md` must stay — it carries `source: S101 — https://jc.hit.edu.cn/...` today. Measured:
cell as-is → `HELD_CITED=- HELD_BAD=1 REF_ID_UNBOUND=3`; cell patched → `HELD_CITED=S101 HELD_BAD=0`, leaving only
`REF_ID_UNBOUND=1` (§7.1). **Moot under the state now landed** — the lane's r37 dropped the HIT half outright ("not
carried this round"), so no entry cites S101 and the held leg passes vacuously (`HELD_CITED=- HELD_BAD=0`). Use the
draft only if the HIT half is restored.
## 7. Falsifiers on the adopter-only path (scratch lane from `git show 9caf8fc:corpus/SOURCES.md`)
Adopter rows + adopter-rewritten entries, `--lane-only`: `BOUND=3/3 BOUND_IDS=S121,S122,S123 NEW_GROUND=2/2
QUARANTINE_VERDICTS=3/3` but `HELD_BAD=1 REF_ID_UNBOUND=3 SPAN_IDS=0/3 ANCHOR_BOUND=0/3 SUBSTANCE=FAIL
INFERENCE_GROUNDED=0/2 C2=FAIL`. The mechanical output binds ids but cannot pass C2 alone.
**7.1 A stale body token the adopter cannot see.** r37's Unknown prints "…serves no text for 采标 standards (wave 1's
`S075`)…". S075 is neither a staged id (staged ids start S082) nor a minted id, so `bodyonly.tsv` and `bodyclash.tsv`
are both blind to it — yet in the lane **S075 is the GNU coreutils `mktemp(1)` manual** (`corpus/SOURCES.md:85`).
Measured with the S101 cell patched: `REF_ID_UNBOUND=1`, context `"…serves no text for 采标 standards (wave 1's
`S075`), and the copy…"`. Hand-fix: drop the token, or re-point it to S122 (the openstd row it means).
**7.2 No anchor offsets.** All three `cell6` anchors are prose with no `char N` → `ANCHOR_BOUND=0/3`; the counter
demands ≥1 per bound row, each equal to a quote offset in `spans.tsv`.
**7.3** `SPAN_IDS/SUBSTANCE/INFERENCE_GROUNDED` are the quotes/spans/lesson legs — out of the adopter's reach.
## 8. Re-grounded against capture bytes (offsets in the counter's own form: `.txt` via
`read_text(utf-8, errors="replace")`, i.e. universal newlines — SAMR 3591, OPENSTD 22007, JMU 83061 chars)
- **S121 `teaches` is supported**: `本标准非等效采用ISO国际标准：ISO 690:2021。` (1 @1797), 采标中文名称
  `信息与文献 参考文献和信息资源引用指南`, `（全部代替）` (1 @1162), 2025-12-02 / 2026-07-01, `中国标准分类号 A14`,
  `01.140.20`. Caveat: `GB/T 7714-2015` occurs **2×** and the replacement is a 3-line block, so it is a block read,
  not one quotable string.
- **S122 `teaches` first half is verbatim**: `该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供
  文本阅读服务` (1 @15188); ICS/CCS/主管部门/发布日期/实施日期 each once (13300/14082/16105/16321/17078). **Overreach:**
  "the Chinese rules themselves are therefore not publicly verifiable from the authority" — the capture is the
  portal's statement about its own service, and the S121 record still prints `查看文本` (1 @3453), never opened.
- **S123 `teaches` outruns the capture in three ways**: 17 type rows and 5 carrier rows do verify in 表Ａ．１/表Ａ．２,
  but the workbook renders them **fullwidth** (`Ｍ Ｊ Ｎ Ｃ Ｄ Ｒ Ｓ Ｐ ＥＢ Ａ ＣＭ ＤＳ ＰＰ Ｇ ＣＰ ＤＢ Ｚ`; `ＭＴ ＤＫ ＣＤ
  ＯＬ ＭＭ`) while the cell writes halfwidth `M/J/EB/PP/MT…`; the date form is `ＹＹＹＹ－ＭＭ－ＤＤ` (count 2) and
  halfwidth `YYYY-MM-DD` is **count 0**; and `电子资源既应著录文献类型标识，也应著录文献载体标识` is **count 0** in the
  `.txt` — it breaks as `…也应著录文\n献载体标识。`, so it cannot be a one-line located quote (the on-line cut is
  `文献类型标识、文献载体标识应按照附录Ａ著录。` 1 @11542).
- **S123 `scope` carries `(see S075)`** — same wrong document as §7.1, inside a registry cell (the counter scans
  entries, not rows, so it costs nothing there, but it is a false pointer in the lane namespace). Its `anchor`
  also lists sections `5.2, 7.9, 8.15` the entry never cites, and writes `附录A 表A.1` halfwidth where the capture
  prints `附录Ａ 表Ａ．１`.
## 9. Cross-claim fact for the L1 (C1 ⇄ C2)
The held HIT `.doc` **is** one of C1's five pinned REAL captures: `.qcache/6dc68fd6b32ce9c8dfcebce8.raw`, sha256
`6063a3aff7a4081e93a6…`, matching `c1-count.py` `REAL["6dc68fd6b32ce9c8dfcebce8"]`. `tools/capture-text.py` reads it to
**27,012 chars, 0 U+FFFD**, and C1's pinned quote `本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中
规定的作者-出版年制。` sits at **12795** in that form vs **11993** in the whole-file UTF-16LE decode. That corroborates
`corpus/lessons/round-54.md` `## Mistakes` row 2 (nine S100/S101 anchors index an undefined form; offsets land
elsewhere in the defined one) — and the frozen C2 predicate needs no new span on S101, so this is a routing note,
not a C2 defect.
## VERDICT
Built and ran the lane adopter on the frozen staged package (exit 0, stderr empty, `CITED=4 APPEND=3 HELD=1 TWIN=0`,
map `S085→S121 / S086→S122 / S093→S123 / S101 held` confirmed), then attacked its output against the frozen
`c2-count.py`: it binds 3/3 but fails on three hand-normalisations it cannot make — an invisible stale `S075` body
token that reads as the GNU `mktemp` row (`REF_ID_UNBOUND=1`, measured), anchor cells with no `char N`
(`ANCHOR_BOUND=0/3`, measured), and the held S101 `used-by` cell needing
`corpus/knowledge/source-type-taxonomy-r37.md` whenever r37 cites it (`HELD_BAD=1`→`0`, measured) — and re-grounded
every append-row scope/teaches claim to capture bytes, finding three cells that outrun them (S122's "not publicly
verifiable from the authority", S123's halfwidth code and date forms against a fullwidth source, and the un-quotable
7.3 sentence that crosses a line break).
