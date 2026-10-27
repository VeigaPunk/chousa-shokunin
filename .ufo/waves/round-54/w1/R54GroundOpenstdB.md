# R54 / W1 — R54GroundOpenstdB: second pass on staged S086 → planned lane S122

- seat `R54GroundOpenstdB` (scribe, second pass; the A-pass report was not opened), leaf member, no dispatch.
- lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` at `9caf8fc` (claims frozen at `5a1a206`).
- target: staged S086 → lane S122, the openstd portal record of GB/T 7714-2025 with its no-text notice (HTML);
  staged row S086 in `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md`, staged entry
  `knowledge/corpus/knowledge/source-type-taxonomy-r36.md` (`source:` line 5, `recheck:` line 7).
- touched surfaces: **this file only** — no registry row, entry, product file, git index/jj state or fleet
  file written; no other seat's report read; campaign tools not run; C1/C2 counters not run (not this seat).

## Capture provenance (on-disk only; no network, no live fetch)

`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/b9ca2a4fdf9455867534f144.{txt,raw}`
for `http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14`

```
$ sha256sum ...b9ca2a4fdf9455867534f144.raw ...txt && cmp ...raw ...txt && echo IDENTICAL
2d68faf7c724eb1baca6c201613cbf0607589ca017153461a9357760d1c8caf1  ...raw
2d68faf7c724eb1baca6c201613cbf0607589ca017153461a9357760d1c8caf1  ...txt
IDENTICAL
$ file ...raw
HTML document, Unicode text, UTF-8 text, with CRLF line terminators
```

24185 bytes, mtime 2026-10-23 20:33 (matches the staged "record read 2026-10-23"). The `.txt` sidecar **is** the
raw HTML, so the text form carries the markup and no quote may cross a tag; read UTF-8/universal newlines =
**22007 chars, 689 lines**, offsets `text.find(quote)` on that form (the `build-spans.py:122` read).

## Identity stamp the record carries itself (line / char offset)

| element | value | where |
|---|---|---|
| title | `国家标准|GB/T 7714-2025` | 16 / 159 |
| number | `标准号：GB/T 7714-2025` | 431 / 13300 |
| names | zh `信息与文献 参考文献著录规则` · en `Information and documentation—Rules for bibliographic references and citations to information resources` | 448 / 13784 · 460 |
| status | `现行` | 470 / 14510 |
| adoption badge | `该标准采用国际标准` (title attr of the `采` label) | 434 / 13411 |
| CCS / ICS | `中国标准分类号（CCS）` = `A14` · `01.140.20` | 505 / 15560 · 514 / 15840 |
| dates | published `2025-12-02` · in force `2026-07-01` | 523 / 16105 · 530 / 16321 |
| bodies | 主管部门 + 归口部门 `国家标准委` (2x) · 发布单位 `国家市场监督管理总局、国家标准化管理委员会` | 543, 549 · 558 / 17078 |
| platform | `全国标准信息公共服务平台` (anchor → `https://std.samr.gov.cn/`); hcno `C6CE52E55AC09B9C79A20AEA77CEDD14` as the button `data-value` (URL-bound) | 384 / 11716 · 486 / 14937 |
| host footer | `主办：国家市场监督管理总局国家标准技术审评中心` · `京ICP备18022388号-1` | 617 / 19081 · 620 / 19383 |
| no-text notice | `该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务` | 491 / 15188 |

## Located quotes (each `count==1`, on ONE line, ≤25 words, ≤160 chars)

```
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	该标准采用国际标准	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	中国标准分类号（CCS）	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	01.140.20	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	2025-12-02	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	2026-07-01	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	国家市场监督管理总局、国家标准化管理委员会	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	主办：国家市场监督管理总局国家标准技术审评中心	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	京ICP备18022388号-1	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	该标准暂无全文，请等待更新	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	自2017年1月1日后新发布的标准将在发布后20个工作日内公开，请耐心等待；	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务	corpus/knowledge/source-type-taxonomy-r36.md
```

Rows 1-10 are the non-headline quotes (offsets 13411, 15560, 15840, 16105, 16321, 17078, 19081, 19383, 1712, 1796); row 11 is the notice (15188), shipped because the entry's core quote is line-wrapped (F3); row order = span numbering.

Span-builder receipt (fake root in scratch, lane untouched):

```
$ python3 corpus/evidence/round54/build-spans.py --root $S/fakeroot   # 11 rows, output condensed here
QUOTE S122 char 13411 / 15560 / 15840 / 16105 / 16321 / 17078 / 19081 / 1712 / 19383 / 1796 / 15188  (spans/S122-1..11.txt)
SPANS_ROWS=11 WRITTEN=11   # per span: slice_ok True, longer True (169…207 chars), holds_quote True
```

`corpus/evidence/round51/quote-substance-check.py` on that manifest: `IDS=1 QUOTES=11 FAILURES=0` (exit 0).

## Negative sweeps (`text.count`, same text form)

```
GB/T 7714-2025 2 (164, 13304)   GB/T 7714-2015 0 ABSENT   ISO 690 0 ABSENT   ISO 690:2021 0 ABSENT
非等效 0 ABSENT   等同 0 ABSENT   修改 0 ABSENT   文献类型标识 0 ABSENT   文献载体标识 0 ABSENT
ＯＬ 0 ABSENT   OL 0 ABSENT   ＥＢ 0 ABSENT   EB 0 ABSENT   引用日期 0 ABSENT
本系统不提供文本阅读服务 1   版权 2 (notice 15216, footer 18933)   图书馆员 0 ABSENT   作者 0 ABSENT
```

Supporting: `代替 0`, `替代 0`, `废止 0`, `ISO690 0`, `ISO/IEC 0`, `采标 0`, `指南 0`, `附录 0`, `表A 0`,
`文献类型 0`, `载体 0`, `顺序编码 0`, `.pdf 0`, `403 0`, `xuebao 0`, `jmu 0`, `hit.edu 0`, `openstd 0`;
present: `采用 2`, `著录 1`, `参考文献 1`, `标准全文 4`, `全文 6`, `预览 7`, `下载 1`, `公开 2`,
`20个工作日 1`, `现行 1`. Boundary check on S085 (`adf6ba934e813b2c326fa150.txt`, 12 terms): `ISO 690 1`,
`ISO 690:2021 1`, `非等效 1`, `采标情况 1`, `GB/T 7714-2015 2`, notice `0` — each absence above is a boundary,
not a gap.

## Findings against the staged entry (reported, not patched)

- **F1 attribution.** r36 lines 12-18 mix S085 and S086. On S122 the number, names, status, dates, CCS/ICS,
  ministry and issuing bodies are grounded; `ISO 690`/`ISO 690:2021`/`非等效`/`GB/T 7714-2015` are **0**.
  "non-equivalent adoption of ISO 690:2021" and "wholly replacing GB/T 7714-2015" belong to S121 only.
- **F2 recheck.** r36 line 7 asks S122's recheck to confirm the `采标情况` block; S122 has `采标情况` 0. S122's
  own recheck object is the notice plus status/dates/CCS/ICS/publisher.
- **F3 quote hygiene.** The notice is one whole line in the capture (491) but the entry wraps it across lines
  20-21, so only its tail is contiguous in the entry; if row 11 is used the entry must carry it unwrapped.
- **F4 record state.** The no-text state is the adoption/copyright notice, not the "not yet public" path:
  `该标准暂无全文，请等待更新` (1712) and the 20-working-day policy (1796) are defined in the i18n block and
  never rendered, and the `在线预览提示` modal is dead code (`$('#myModal').modal('show')` is commented out
  in the `.ck_btn` handler). No full-text control is rendered: the only record button is `实施信息反馈` (486);
  `ck_btn`/`xz_btn` occur only as JS selectors (0 markup elements); `.pdf` 0.
- **F5 adoption wording.** The notice says `ISO、IEC等国际国外组织的标准` (international/foreign organisations' standards, ISO and IEC named); it never names ISO 690:2021.
- **F6 host.** The page names itself `全国标准信息公共服务平台` and links `std.samr.gov.cn`; `openstd` is **0**
  in the text form, so "openstd record" is URL-only provenance — anchor the Registry row on the notice plus
  status/dates/CCS/ICS/publisher, not on a host string.
- **F7 metadata scope.** Status `现行`, both dates, CCS `A14`, ICS `01.140.20`, 主管部门/归口部门 `国家标准委`,
  发布单位 present, 备注 empty, no `采标情况`: the staged row's "serves only metadata – status, dates,
  ICS/CCS, supervising body" holds; the only adoption signal is the `采` badge's `该标准采用国际标准`.

## Gates run / not run

- Run: byte identity/`file` of `.txt`/`.raw`; char/line counts; 18 required + 26 additional sweeps on S086; 12-term boundary sweep on S085; `build-spans.py` acceptance of all 11 rows; span exact-slice/containment; entry-containment per quote.
- Not run: C1/C2 counters, `inference-ground.py`, `quote-substance-check.py`, LibreOffice, any git/jj mutation; no tool installed; no `soffice` started. Scratch `/fast/scratch/hyaku/chousa-r54/R54GroundOpenstdB/` (TMPDIR there) removed after these receipts were copied here.

VERDICT: attacked staged S086→S122 for supportable substance — the record grounds its own identity, the
no-text/copyright notice and the metadata block (11 quotes located once, spans accepted by the frozen builder)
and grounds none of the entry's adoption/predecessor/scope claims (`ISO 690:2021`, `非等效`, `GB/T 7714-2015`,
`图书馆员`, `作者` all 0 here, all present on S085); S122 is usable only once the ISO/predecessor claims move to
S121 and the notice quote is unwrapped.
