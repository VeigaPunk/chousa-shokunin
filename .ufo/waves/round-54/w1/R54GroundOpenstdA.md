# R54GroundOpenstdA — grounding pass A: staged S086 → lane S122 (openstd record, GB/T 7714-2025)

Leaf seat, no dispatch. Scratch `/fast/scratch/hyaku/chousa-r54/R54GroundOpenstdA` (TMPDIR there), removed at exit; no soffice, no git/jj call anywhere, no write outside this report. Everything below was re-read from capture bytes this round; the campaign's quotes and dates were used for nothing.

## Inputs (digests recomputed, not copied)

```
sha256 2d68faf7c724eb1baca6c201613cbf0607589ca017153461a9357760d1c8caf1  24185 B  .qcache/b9ca2a4fdf9455867534f144.txt
sha256 2d68faf7c724eb1baca6c201613cbf0607589ca017153461a9357760d1c8caf1  24185 B  .qcache/b9ca2a4fdf9455867534f144.raw
.txt: 22007 chars / 689 lines, U+FFFD 0   (the sidecar IS the byte-identical raw: sha256 of URL
http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14, first 24 hex
= b9ca2a4fdf9455867534f144, recomputed with hashlib.sha256(url.encode()).hexdigest()[:24])
```
Entry `merge/chousa/knowledge/corpus/knowledge/source-type-taxonomy-r36.md`; staged row `SOURCES.append.md:11` (`S086`, `mined`, `2026-10-23`, `used-by` = `corpus/knowledge/source-type-taxonomy-r36.md`). Capture mtime `Oct 23 20:33`, consistent with the entry's "record read 2026-10-23".

## Page title and the identity the record shows (offsets = `text.find` on the whole `.txt`)

| element | printed | offset | line | n |
|---|---|---|---|---|
| `<title>` | `国家标准\|GB/T 7714-2025` | 159 | 16 | 1 |
| 标准号 | `标准号：GB/T 7714-2025` | 13300 | 431 | 1 |
| adoption badge (only one on the page) | `<span … title="该标准采用国际标准">采</span>` | 13411 | 434 | 1 |
| 中文标准名称 | `信息与文献 参考文献著录规则` | 13784 | 448 | 1 |
| 英文标准名称 | `Information and documentation—Rules for bibliographic references and citations to information resources` | 14089 | 460 | 1 |
| 标准状态 | `现行` (label `标准状态：` @14278) | 14510 | 470 | 1 |
| CCS | `中国标准分类号（CCS）` / `A14` | 15560 / 15657 | 505 / 508 | 1 / 1 |
| ICS | `国际标准分类号（ICS）` / `01.140.20` | 15743 / 15840 | 511 / 514 | 1 / 1 |
| 发布日期 | `发布日期` @16016 / `2025-12-02` | 16105 | 520 / 523 | 1 / 1 |
| 实施日期 | `实施日期` @16219 / `2026-07-01` | 16321 | 527 / 530 | 1 / 1 |
| 主管部门 / 归口部门 | `国家标准委` / `国家标准委` | 16638 / 16740 | 543 / 549 | **2** / **2** |
| 发布单位 | `发布单位` @16988 / `国家市场监督管理总局、国家标准化管理委员会` | 17078 | 555 / 558 | 1 / 1 |
| 备注 | label @17267, value empty | — | 564-568 | 1 |

`GB/T 7714-2025` alone occurs **twice** (@164 in `<title>`, @13315 in 标准号) → no unique bare-number quote; `国家标准委` occurs **twice** → the supervising-body sentence has **no unique quote** (the SAMR seat reached the same duplicate-string conclusion independently, `R54GroundSamrA.md`).

## The no-text-reading notice, and its stated reason

```
15188  L491  该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务
```
- The stated reason is **版权保护** (`由于涉及版权保护问题` @15212, n=1); the trigger it states is that the standard *has adopted ISO, IEC and other international and foreign organisations' standards* (`采用了ISO、IEC等国际国外组织的标准`), not "ISO/IEC standards" — the page's `国际国外组织` (international **and foreign**) is dropped by the entry's rendering.
- The tail clause `本系统不提供文本阅读服务` @15223, n=1 — this is the only capture in the theme carrying it (the SAMR sidecar has 0; cross-check `R54GroundSamrA.md`).

## Preview / download controls: none present

| sweep | command | result |
|---|---|---|
| elements carrying class `ck_btn` (preview) | `re.findall(r'class="[^"]*ck_btn', t)` | **0** |
| elements carrying class `xz_btn` (download) | `re.findall(r'class="[^"]*xz_btn', t)` | **0** |
| server-rendered preview links | `re.findall(r'href="[^"]*showGb', t)` | **0** |
| `showGb(` call sites | `re.findall(r'showGb\(', t)` | 4 — all inside the page's own `<script>` (L112/117/124 calls, L143 definition) |
| `<iframe|embed|object` | regex | **0** |
| `<button` | grep | 4 — navbar toggle (L376), `fk_btn` 实施信息反馈 with `app-hide` (L486), modal close (L587), modal 知道了 (L594) |
| `ck_btn` / `xz_btn` / `下载标准` occurrences | `t.count` | 2 / 2 / 1 — i18n dictionary (L61-62) and jQuery handlers (L106-121) only |

So: the page ships the *machinery* for an online preview and a download (i18n `preview`/`download`, `showGb(...type=online)` and `...type=download`), plus the "browser unsupported" modal `#myModal` (L583-598) and the unused key `'noFullText': '该标准暂无全文，请等待更新'` (L64, 2 definitions, 0 uses) — but **this record emits no preview or download control at all** and instead prints the red notice. That is exactly what the entry's "Only metadata is served" rests on; it is sound, and it is an absence, not a quote.

## Quote machine lines (staged id = planned lane id **S122**)

```
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	国家标准|GB/T 7714-2025	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	标准号：GB/T 7714-2025	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	该标准采用国际标准	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	信息与文献 参考文献著录规则	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	Information and documentation—Rules for bibliographic references and citations to information resources	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	中国标准分类号（CCS）	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	A14	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	国际标准分类号（ICS）	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	01.140.20	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	2025-12-02	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	2026-07-01	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	发布单位	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	国家市场监督管理总局、国家标准化管理委员会	corpus/knowledge/source-type-taxonomy-r36.md
```

All 14 rows verified by one python pass: `count==1`, wholly inside the `.txt` line named above, `len<=160`, whitespace words `<=25`, copied byte-exact (full-width `：（）` and the em dash preserved). Offsets in row order: 159, 13300, 13411, 13784, 14089, 15560, 15657, 15743, 15840, 15188, 16105, 16321, 16988, 17078. `build-spans.py` will take the `.txt` form for every one of them (each occurs there exactly once) and its own `key(url)` derivation on this URL is `b9ca2a4fdf9455867534f144`, so the URL must be pasted byte-exact.

## Integration traps for the L1 (measured, not guessed)

1. **Do not add `现行` as a span row.** `round51/quote-substance-check.py` floors quotes at `MIN_CHARS = 3` non-whitespace characters; `现行` has 2 and would print `HOLLOW_QUOTE S122`. Its offset (14510) belongs in prose. `A14` sits exactly on the floor (3) and passes.
2. **The English title must be a single line in the entry.** The staged entry breaks it (`Information and` / `documentation—Rules for … information` / `  resources)`) — so the quote above cannot be `in` the entry as staged; join it onto one physical line. The bare title form is the least-friction one (the entry prints it parenthetically, without the page's `英文标准名称：` lead-in).
3. **`信息与文献 参考文献著录规则` is already a substring of the staged entry** (inside `《…》`), so that row needs no entry edit; `标准号：GB/T 7714-2025` and the label rows (`中国标准分类号（CCS）`, `国际标准分类号（ICS）`, `发布单位`) are not in the entry yet and must be pasted in.
4. **Every row must also appear in the round-54 lesson** (`c2-count.py`: quote inside span file, inside citing entry, inside the lesson) — the lesson therefore has to carry the notice verbatim, including `国际国外组织` and `版权保护`.
5. **`该标准采用国际标准` is a `title=` attribute value**, not body text (L434). It is still a byte-exact single-line substring, and it is the only adoption marker on this page.

## Sentence-by-sentence — what the staged entry rests on **this** document for

| staged sentence | verdict |
|---|---|
| `GB/T 7714-2025 《信息与文献 参考文献著录规则》 (English title: …) is a **current** PRC national standard` | **reproduces** (13300, 13784, 14089 for the three strings; `现行` @14510 for "current"; `国家标准` in `<title>` @159 and the 全国标准信息公共服务平台 masthead @L384 for "PRC national standard") |
| `published 2025-12-02, in force 2026-07-01` | **reproduces** exactly (16105, 16321, under labels 发布日期/实施日期 @16016/@16219) |
| `wholly replacing GB/T 7714-2015` | **ABSENT here** — `代替` 0, `替代` 0, `7714-2015` 0, `GB/T 7714-2015` 0, 备注 empty. It reproduces only on the SAMR record (`全部代替标准` @1415 there). Narrower/attributed: "the openstd record states no predecessor; the SAMR record marks 全部代替标准 GB/T 7714-2015 (S085)" |
| `a **non-equivalent** adoption of ISO 690:2021, whose Chinese name is 信息与文献 参考文献和信息资源引用指南` | **ABSENT here** — `非等效` 0, `ISO 690` 0, `ISO 690:2021` 0, `采标情况` 0, `信息与文献 参考文献和信息资源引用指南` 0. This page carries only the `采` badge (`该标准采用国际标准`, 13411) and the notice's `ISO、IEC等国际国外组织`. Narrower for S086: "badged 采 / 该标准采用国际标准, and the notice names ISO, IEC and other international and foreign organisations' standards; the specific ISO 690:2021 non-equivalent adoption is stated on the SAMR record (S085)" |
| `ICS 01.140.20, CCS A14` | **reproduces** and both are unique here (15840, 15657) — unlike the SAMR capture where `01.140.20` occurs 3× |
| `supervised by the national standardisation administration` | **reproduces in substance, not as a quote**: `主管部门` @16549 and `归口部门` @16726 both read `国家标准委` (@16638, @16740) — that string is duplicated, so no unique quote exists; the uniquely quotable authority string is 发布单位's `国家市场监督管理总局、国家标准化管理委员会` (17078). Narrower: "its 主管部门 and 归口部门 are 国家标准委; the 发布单位 is 国家市场监督管理总局、国家标准化管理委员会" |
| `The official full-text portal refuses to serve the document's text … "本系统不提供文本阅读服务" — no text reading is provided, for copyright reasons` | **reproduces** (15188; the reason `由于涉及版权保护问题` 15212). Only fix: keep `国际国外组织` instead of compressing the trigger to "ISO/IEC" |
| `Only metadata is served` | **reproduces as an absence** (§ Preview/download controls: 0 element-level controls, 0 preview links) |
| `Its *identity* is fully verifiable … number, dates, predecessor, adoption basis, classification` | **partly absent here**: number/dates/classification ✓ (13300, 16105, 16321, 15560/15657, 15743/15840); **predecessor** and **adoption basis** ✗ (both only on S085). Honest split: S086 gives number, titles, status, dates, CCS/ICS, departments; S085 adds predecessor and adoption basis |
| H1 `The Chinese citation standard **names a source's type**` and Inference `its scope is the bibliographic items for each document type, and its scope statement explicitly excludes librarians, bibliophiles and indexers compiling references` | **ABSENT here** — `文献类型` 0, `文件类型` 0, `电子资源` 0, `著录项目` 0, `范围` 0, `本标准` 0, `适用于` 0, `图书馆` 0, `索引` 0, `附录` 0. This page holds no scope clause and no type table. The H1's first clause asserts precisely what the entry's own *Unknown* disclaims ("not admitted as evidence here"), and r36 lists **no `source:` line** for the JMU copy that would carry it. Narrower: retitle to the document's own evidence ("…publishes its identity and refuses its text"), and move the scope/type sentence into r37 (S123) with a `source:` line, or drop it |
| `source: S086 — … — the full-text notice on the standard's openstd record` | **under-describes its own use**: the entry takes status, dates, CCS/ICS, titles and departments from this record too. Honest descriptor: "the openstd record — 标准号/中英文名称/标准状态, the 采 badge, CCS/ICS, 发布日期/实施日期, 主管部门/归口部门/发布单位, and the no-text-reading notice" |
| `recheck: 180d — re-open both records and confirm the 采标情况 block and the "本系统不提供文本阅读服务" notice are unchanged` | **mis-scoped**: `采标情况` is **0** on this record (it is S085's field), and the recheck pins only the notice's tail clause, not the reason. Honest: "re-open S085 for the 采标情况 block; re-open S086 for the notice `该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务` and the 标准状态 `现行`" |

Sweeps on this sidecar that came back **0** (each `t.count(...)`): `采标情况`, `非等效`, `ISO 690`, `ISO 690:2021`, `7714-2015`, `代替`, `替代`, `文献载体标识`, `范围`, `本标准`, `适用于`, `图书馆`, `索引`, `文献类型`, `文件类型`, `电子资源`, `著录项目`, `附录`, `征求意见`.

## Quarantine slice — this document has **no** register row

```
$ grep -c "openstd" /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
2                     # both other standards: hcno=458BACCE… (S037), hcno=E107EA4D… (S776)
$ grep -n "7714\|C6CE52E55AC09B9C79A20AEA77CEDD14" absent-defect-register.md
exit=1                # no match
```
So the three verdict lines the lesson must carry are register `S080` (SAMR), `S088` (JMU), `S096` (HIT) and **nothing for the openstd URL** — a fourth verdict line for this document would be invented. `c2-count.py` prints 3 at the freeze, which matches.

Register `S080` is already hand-checked by the sibling seat (`R54GroundSamrA.md`: formatting artifact, not a defect). My independent counts agree and add the openstd half: the register's composite `标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01` occurs **0** times on the SAMR capture *and* **0** times here, while its three values are present on both (here at 13300, 16105, 16321). I did not touch rows `S088`/`S096` (JMU PDF, HIT `.doc` — other seats' documents).

## Gates / touched surfaces

Commands run: `read` on the staged entry, `SOURCES.append.md`, the frozen claims, the round-54 builders/counters (read-only), the sibling report; `python3` count/offset/line/regex sweeps over the two capture files and over `absent-defect-register.md`; `sha256sum`, `wc -c`, `file`, `grep` on the read-only cache. No production file, index, jj state, campaign tool or PATH directory touched; no network; no installs; no LibreOffice; no git/jj command anywhere. Sole write: this report. Scratch removed.

VERDICT: grounded staged S086 → S122 from capture bytes — the record shows `<title>国家标准|GB/T 7714-2025</title>`, 标准号/中英文名称/标准状态 现行/CCS A14/ICS 01.140.20/2025-12-02/2026-07-01/主管部门·归口部门 国家标准委/发布单位, and the notice `该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务`, with **zero** preview or download control (only a hidden 实施信息反馈 button) — 14 unique single-line quotes emitted (offsets 159–17078); found 3 staged statements that do not reproduce on this document (`wholly replacing GB/T 7714-2015`, `non-equivalent adoption of ISO 690:2021`, the scope/type-taxonomy sentence behind the H1) plus 2 mis-scoped record-keeping lines (S086 descriptor, `recheck` naming the absent 采标情况), 2 duplicate strings with no unique quote (`GB/T 7714-2025` ×2, `国家标准委` ×2), no absent-defect-register row for this URL, and the `现行` quote rejected as hollow (2 non-space chars vs `MIN_CHARS=3`).
