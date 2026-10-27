# R54GroundSamrB — staged S085 → planned lane S121 (GB/T 7714-2025 SAMR record), independent second pass

seat R54GroundSamrB · chousa round 54 wave 1 · 2026-10-26 · no network · no other seat's report read (R54GroundSamrA not opened) · only write is this file

## Capture under test

- URL: `https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F`
- Key check (`python3`): `sha256(url)[:24]` = `adf6ba934e813b2c326fa150` → **True** against the file name; the cache key is the URL's, so the capture is bound to this record.
- `.txt` text form: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/adf6ba934e813b2c326fa150.txt`, 6626 bytes, sha256 `4e46154f4a841d17d858eafb5c0099257030f301daadcaa30c37f2e668fb7138`, mtime 2026-10-23 20:33:09 -0300.
- `.raw`: 76252 bytes; `<title>国家标准 - 全国标准信息公共服务平台</title>`; the URL's id `4507EFE13D37CB6AE06397BE0A0A601F` occurs once; `std.samr.gov.cn` 73×.
- **Offset convention:** all offsets below are on `pathlib.read_text(encoding="utf-8")`, the read `build-spans.py:122` uses. The file holds 877 CRLF pairs, so a raw-byte decode yields 4468 chars where the normalized form has 3591, and offsets shift (发布… is 1029 normalized, 1257 raw). Any byte-mode reader that produces spans will mis-anchor.
- Lane HEAD at run `9caf8fc6` (not BASE_REV `c49ffc6c`); `corpus/knowledge/source-type-taxonomy-r36.md` and `-r37.md` do not exist; `grep -c std.samr.gov.cn corpus/SOURCES.md` = **0**.

## Identity stamp — what the record itself asserts (count @ normalized offset)

| field | record's own value |
|---|---|
| Chinese title | 信息与文献 参考文献著录规则 — 4× @344 |
| English title | Information and documentation—Rules for bibliographic references and citations to information resources — 1× @361 |
| kind / status | 国家标准 · 推荐性 1× @477 · 现行 2× @489 |
| number | GB/T 7714-2025 — 2× @1239 |
| dates | 发布 于 2025-12-02 (status block @1029) and 发布日期 @1354 + 2025-12-02 (table); 实施 于 2026-07-01 @1048 and 实施日期 @1382 + 2026-07-01 — each date stated twice |
| predecessor | GB/T 7714-2015 @1136 · 全部代替 2× @1163 · 全部代替标准 @1415 |
| plan | 标准计划 @1452 → 20240256-T-469 @1463 |
| classification | 中国标准分类号 @1507 → A14 @1517; 国际标准分类号 @1527 → 01.140.20 @1572 (3×) |
| committee / supervisor | 归口单位 @1692 = 执行单位 @1723 = 全国信息与文献标准化技术委员会; 主管部门 @569 → 国家标准委 @575 |
| adoption | 采标情况 @1787; 非等效 @1795; ISO 690:2021; 采标中文名称 @1829 = 信息与文献 参考文献和信息资源引用指南 |
| host / publisher | 主管：@3203 · 主办：@3230 · 技术支持：@3256 · 支持电话：@3276 · 备案号 @3296 · 版权所有 侵权必究 @3190; served by 全国标准信息公共服务平台 on std.samr.gov.cn |

Reading: this is a metadata record of a **recommended (GB/T), current** national standard, issued 2025-12-02, effective 2026-07-01, wholly replacing GB/T 7714-2015, non-equivalently adopting ISO 690:2021. Today 2026-10-26 is past the effective date, consistent with 现行.

## Located quotes — 8, all non-headline, each `count == 1`

```
QUOTE	S121	https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F	发布 于 2025-12-02	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S121	https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F	实施 于 2026-07-01	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S121	https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F	20240256-T-469	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S121	https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F	由 TC4 （全国信息与文献标准化技术委员会）归口	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S121	https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F	本标准非等效采用ISO国际标准：ISO 690:2021。	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S121	https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F	采标中文名称:信息与文献 参考文献和信息资源引用指南	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S121	https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F	主管：国家市场监督管理总局 国家标准化管理委员会	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S121	https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F	备案号： 京ICP备18022388号-1	corpus/knowledge/source-type-taxonomy-r36.md
```

Offsets in the same order: 1029, 1048, 1463, 537, 1797, 1829, 3203, 3296. Longest 29 chars / 3 whitespace words; every quote lies inside one line (`text.rfind("\n",0,o) <= o` and `o+len(q) <= text.find("\n",o)` passed for all 8); no TAB, no newline inside any quote (asserted). The headline forms were deliberately excluded because they are not unique: Chinese title 4×, `GB/T 7714-2025` 2×.

## Negative sweeps — `text.count`, exact, on the .txt form

```
GB/T 7714-2025	2
GB/T 7714-2015	2
ISO 690	1
ISO 690:2021	1
非等效	1
等同	0
修改	0
文献类型标识	0
文献载体标识	0
ＯＬ	0
OL	0
ＥＢ	0
EB	0
引用日期	0
本系统不提供文本阅读服务	0
版权	1
图书馆员	0
作者	0
```

**Absent (0) — 12 of 18:** 等同, 修改, 文献类型标识, 文献载体标识, ＯＬ, OL, ＥＢ, EB, 引用日期, 本系统不提供文本阅读服务, 图书馆员, 作者. Every negative an entry makes about this record must cite this sweep: the record states no equivalent/modified adoption, no type or carrier identifier, no access-date rule, no text-reading refusal, no librarian scope, no author. The one 版权 hit is the site footer 版权所有 侵权必究 @3190, not a rights statement about the standard.

## Findings

**F1 — the refusal notice is not on this record; it is on S086.** `本系统不提供文本阅读服务` = 0 and 版权 = 1 (footer) here. The sentence lives in the openstd capture `b9ca2a4fdf9455867534f144.txt` (count 1, offset 15223), one HTML line `该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务`. This record instead exposes `查看文本` @3453 — a text *entry point*, not a refusal. The staged r36 entry's "the official portal refuses … for copyright reasons" must be attributed to S086/S122; on S085 it is unsupported. (Also observed, for the S122 owner: that sidecar is `cmp`-identical to its `.raw`, so S086's "text form" is raw HTML — spans there will contain markup.)

**F2 — the type/carrier taxonomy and the librarian exclusion are S093's, not S085's.** This record: 文献类型标识 0, 文献载体标识 0, ＯＬ 0, ＥＢ 0, 引用日期 0, 图书馆员 0. JMU copy of the standard's text (key `0f33243fd7ac2fe88b85c1ba`, 83061 chars): 文献类型标识 35, 文献载体标识 32, ＯＬ 124, ＥＢ 22, 引用日期 15, 图书馆员 1 @5609 on one line `本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。` The staged entry's inference that the scope "explicitly excludes librarians" therefore cannot rest on S085+S086: it belongs to S123 (r37), or S121 drops it. S121's province stops at identity, status and adoption basis.

**F3 — adoption is stated once and only as 非等效.** 等同 0, 修改 0, 非等效 1; the single sentence is the quote at @1797. No entry may call this an identical or modified adoption.

**F4 — empty cells are not assertions.** 上次复审 @1067 and 废止 @1075 are table labels whose value cells are empty in the text form. The record states no review date and no withdrawal; it does not state that no review occurred or that the standard is never withdrawn. Do not convert an empty cell into a fact.

**F5 — the round-43 flip is unmet in the form the lane wrote it.** `corpus/knowledge/citation-version-binding-r36.md:21` says the SAMR row is "not adopted … Round 43 classed that row not-carried" and gives the flip: "a text capture of that record contains the issued and effective dates as a contiguous span." Measured: `2025-12-02 2026-07-01` count **0**; between the two date lines the bytes are `' \n\n '` (1029+15 … 1048). The flip is satisfied only as two separately located quotes, not as a contiguous span. S121 must either restate that condition (per-date located spans) or the lane keeps two contradictory statements about one document. Each date does appear twice, so the facts themselves are solid.

**F6 — quarantine row S080 (register `chousa | round1 | S080 | payload-absent`) hand-check.** Its row id does not resolve to this URL in the lane: `corpus/SOURCES.md:90` S080 is the NDL WARP FAQ (`warp.ndl.go.jp`). Checked by URL+quote instead: the whole quoted string `标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01` = 0; each fragment with a full-width colon = 0 (`标准号：GB/T 7714-2025`, `发布日期：2025-12-02`, `实施日期：2026-07-01`); the record's own forms are `标准号 ` @1327, `GB/T 7714-2025` @1239, `发布日期 ` @1354, `实施日期 ` @1382 with the dates on their own lines. **Verdict: payload-absent STANDS — the quote is not byte-exact (it concatenates three separate lines and invents `：` after two labels). The document is neither fabricated nor unverifiable**: identity is fully present and locatable, and the machine block above supplies the correct forms. Because `grep -c std.samr.gov.cn corpus/SOURCES.md` = 0, no lane row exists for the URL, so C2's "exactly one new row" is still satisfiable.

**F7 — C2's negative premise holds at BASE_REV (premise check, not my axis).** `git grep -F` over `corpus/knowledge` at `c49ffc6c`: `ISO 690:2021` → 0 files, `文献载体标识` → 0 files, `文献类型标识` → 0 files; bare `ISO 690` → 1 file (`citation-count-semantics-r37.md:86`), a different string from the counter's token.

## Gates

- Writes: this report only. Scratch `/fast/scratch/hyaku/chousa-r54/R54GroundSamrB` held two throwaway `python3` scripts and `machine.tsv`, removed on exit; no fixture repo, no git/jj mutation anywhere.
- Network: none; every byte read from the on-disk `.qcache`. No tool installed or upgraded (python3 stdlib only), so no channel/version entry.
- LibreOffice: never invoked; `pgrep -u $USER -f "UserInstallation=file:///fast/scratch/hyaku/chousa-r54"` → empty.
- Counters `c1-count.py` / `c2-count.py`: not run (outside this slice); no frozen predicate, target, counter or control was touched.

## Out of scope (reported, not patched)

- S086 / S093 / S096 hand-check verdicts belong to other wave-1 seats; only the cross-document attribution facts above (counts, offsets, S086 text form = HTML) are offered as inputs.
- Entry drafting, registry row creation, `spans.tsv` derivation, the round-54 lesson and the Gate verdict are the L1's.

## Artifacts

- This report: `.ufo/waves/round-54/w1/R54GroundSamrB.md` (lane-relative).
- Capture: `.qcache/adf6ba934e813b2c326fa150.{txt,raw}` (sha256 as above); cross-checks on `.qcache/b9ca2a4fdf9455867534f144.txt` (S086) and `.qcache/0f33243fd7ac2fe88b85c1ba.txt` (S093).
- Read-only lane inputs: `corpus/SOURCES.md:90`, `corpus/knowledge/citation-version-binding-r36.md:21`, `corpus/evidence/round54/{claims.md,build-spans.py:122,c2-count.py}`.

VERDICT — attacked staged S085 as S121: identity stamp confirmed from bytes (8 unique located quotes, longest 29 chars, offsets 537-3296), 18-term sweep with 12 absent terms; found the copyright-refusal notice and the librarian scope attributed to the wrong document, the round-43 contiguous-date flip unmet as written, and the S080 quarantine quote non-byte-exact — the entry's identity/status/adoption core stands, its scope must stop there.
