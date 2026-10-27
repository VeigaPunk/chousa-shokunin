# R54DraftRows — Registry rows for GB/T 7714-2025 (S121, S122, S123)

seat R54DraftRows (scribe, leaf; no subagent dispatch) · lane chousa-shokunin · round 54 wave 1 · 2026-10-26
Write surface: this report only. No product file, registry row, entry, lesson, span manifest, git index or jj state was touched. No tool installed (python3 stdlib only); no `soffice` run; no network.

## 1. Behaviour

Drafted the three new Registry rows from the staged rows S085, S086, S093 (read whole at
`/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` lines 10, 11, 18), shaped on the lane's own
S117-S120 (`corpus/SOURCES.md:127-130`) and CORPUS.md "SOURCES.md": 11 cells, kind `docs`, tiers A/A/B,
status `mined`, opened 2026-10-26, `recheck` reduced to the bare `180d` cadence, `used-by` exactly the one
citing entry per row. Also drafted the S101 `used-by` cell change (§5), whose trigger is now met: the r37
entry seat confirmed by IRC that its entry cites S101. The S101 `anchor` cell belongs to R54DraftS101Reanchor
and is untouched here.

## 2. Grounding receipts (all run this round from the read-only capture cache)

Cache key = sha256(URL)[:24]. Files: `adf6ba934e813b2c326fa150.txt` (SAMR record, 6626 bytes),
`b9ca2a4fdf9455867534f144.txt` (openstd notice, 24185 bytes), `0f33243fd7ac2fe88b85c1ba.txt` (JMU PDF text, 190614 bytes).
Quotes verified in the counters' own form — `Path.read_text(encoding="utf-8", errors="replace")`, which is what
`build-spans.py:122` and `c2-count.py:127` use, i.e. CRLF folded to LF, so offsets are normalized-form offsets
(the raw bytes decode longer: SAMR 4468 chars, openstd 22695):

```
S121 adf6ba934e813b2c326fa150.txt chars=3591 sha256=4e46154f4a841d17
  count=1 char=1029 len=15 words=3 oneline=True    发布 于 2025-12-02
  count=1 char=1048 len=15 words=3 oneline=True    实施 于 2026-07-01
  count=1 char=1797 len=29 words=2 oneline=True    本标准非等效采用ISO国际标准：ISO 690:2021。
S122 b9ca2a4fdf9455867534f144.txt chars=22007 sha256=2d68faf7c724eb1b
  count=1 char=15188 len=47 words=1 oneline=True   该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务
  count=1 char=16105 len=10 words=1 oneline=True   2025-12-02
  count=1 char=16321 len=10 words=1 oneline=True   2026-07-01
S123 0f33243fd7ac2fe88b85c1ba.txt chars=83061 sha256=13a34aa9bb107eef
  count=1 char=5576  len=19 words=1 oneline=True   本文件适用于作者和编制者著录参考文献。
  count=1 char=5602  len=33 words=1 oneline=True   本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。
  count=1 char=11542 len=42 words=1 oneline=True   文献类型标识、文献载体标识应按照附录Ａ著录。电子资源既应著录文献类型标识，也应著录文
```

Anchor self-check (every `char N` in an anchor cell must be a quote offset of that id): S121 [1029, 1048, 1797]
all true; S122 [15188, 16105, 16321] all true; S123 [5576, 5602, 11542] all true. The two entry seats confirmed
by IRC that their entries carry exactly these strings (EntrySta also carries S121 `char 477 推荐性` and others;
EntryStb confirmed 11542 = 42 chars, no leading spaces, after I flagged the 11539/45-char variant).

Census (frozen awks from CORPUS.md) on the real `corpus/SOURCES.md` with the three rows inserted after line 130:
rows 123, malformed 0, tier A=104 B=14 C=5, status mined=99 queued=19 rejected=5, duplicate ids none, enum
violations none, and the only `used-by` paths not on disk are the three entries this wave is drafting.

## 3. corpus/SOURCES.md — rows to append after S120

```corpus/SOURCES.md
| S121 | GB/T 7714-2025 信息与文献 参考文献著录规则 — 全国标准信息公共服务平台 (国家市场监督管理总局 / 国家标准化管理委员会) — https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F | docs | A | for what the record itself states about this standard — number and title, kind and status, issue and effective dates, the standard it wholly replaces, and its adoption basis — the standards administration's own record page, so tier A for that scope only | the 标准状态 block (发布 于 2025-12-02, 实施 于 2026-07-01), the 采标情况 block (本标准非等效采用ISO国际标准：ISO 690:2021。 and its 采标中文名称), the 基础信息 rows 标准号 / 标准状态 / 全部代替标准 / 中国标准分类号 / 国际标准分类号, and the 归口单位 and 主管部门 rows; capture .txt adf6ba934e813b2c326fa150.txt read as UTF-8 with newline normalisation, 3591 characters, sha256 prefix 4e46154f4a841d17; char 1029, char 1048, char 1797 | GB/T 7714-2025 is a 推荐性 现行 national standard for bibliographic references, published 2025-12-02 and effective 2026-07-01, wholly replacing GB/T 7714-2015; it is a non-equivalent adoption (非等效采用) of ISO 690:2021, whose Chinese title the record gives as 信息与文献 参考文献和信息资源引用指南; CCS A14, ICS 01.140.20, 归口单位 全国信息与文献标准化技术委员会, 主管部门 国家标准委 | mined | 2026-10-26 | 180d | corpus/knowledge/source-type-taxonomy-r36.md |
| S122 | 国家标准 GB/T 7714-2025 在线预览 — 全国标准信息公共服务平台 (openstd) — http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14 | docs | A | for what the full-text portal itself serves for this standard and why it serves no text — the same authority's portal notice about its own service, so tier A for that scope only | the 标准号 heading, the 中文标准名称 and 英文标准名称 rows, 标准状态, the 中国标准分类号（CCS） and 国际标准分类号（ICS） rows, the 发布日期 and 实施日期 rows, and the notice paragraph standing where a text would be; capture .txt b9ca2a4fdf9455867534f144.txt read as UTF-8 with newline normalisation, 22007 characters, sha256 prefix 2d68faf7c724eb1b (the sidecar is the served HTML itself: that digest is also the .raw's); char 15188, char 16105, char 16321 | the portal shows this standard as 现行, with 中文标准名称 信息与文献 参考文献著录规则, an English title, CCS A14 and ICS 01.140.20, published 2025-12-02 and effective 2026-07-01; in place of any full text it states that because the standard adopts ISO and IEC standards the system, for copyright reasons, serves no text-reading service — so the authority offers metadata for this standard and no readable text | mined | 2026-10-26 | 180d | corpus/knowledge/source-type-taxonomy-r36.md |
| S123 | GB/T 7714—2025《信息与文献 参考文献著录规则》full text, a PDF copy on the 集美大学学报 journal office's file host — https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf | docs | B | for what this reproduced copy carries of the standard's own clauses — scope, type and carrier identifiers, date rules — a university journal office's upload rather than the issuing authority, so tier B, scoped to the reproduction and never to the issued standard | the title page (ＧＢ／Ｔ ７７１４—２０２５, 代替ＧＢ／Ｔ ７７１４—２０１５), clause １ 范围, clause ７．３ 文献类型标识、文献载体标识, clause ７．６ 创建／发布或修改日期、引用日期, and the 附录Ａ 表A.1 rows marked 电子资源必备; capture .txt 0f33243fd7ac2fe88b85c1ba.txt (the PDF text form; full-width digits throughout) read as UTF-8 with newline normalisation, 83061 characters, sha256 prefix 13a34aa9bb107eef; char 5576, char 5602, char 11542 | the copy's scope clause limits the standard to 作者和编制者 and excludes 图书馆员、文献目录编制者以及索引编制者; 7.3 requires a type identifier and a carrier identifier, the carrier one 必备 for electronic resources; 7.6 fixes 创建／发布或修改日期 and 引用日期 in ＹＹＹＹ－ＭＭ－ＤＤ form | mined | 2026-10-26 | 180d | corpus/knowledge/source-type-taxonomy-r37.md |
```

Tier, one line each: S121 an authority's own record page for the standard (authoritative for the record's
fields, nothing about the standard's text); S122 the same authority's full-text portal notice about its own
service (authoritative for what the portal serves, nothing about the rules); S123 a journal editorial office's
upload of the text (tier B: proves what that reproduction carries, not that it is the issued text).

## 4. Row S101 — `used-by` old -> new (single-cell change; no other cell moves)

```corpus/SOURCES.md (row S101, 11th cell only)
old: corpus/knowledge/citation-count-semantics-r37.md
new: corpus/knowledge/citation-count-semantics-r37.md, corpus/knowledge/source-type-taxonomy-r37.md
```

Required condition, now met: the r37 entry carries `source: S101 — https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc — <anchor>`.
If the L1 lands r37 without that line, this cell must stay as it is (c2's held check requires `used` to contain
each citing entry, `c2-count.py:190-195`).

## 5. Stripped prose (row keeps `180d`; the prose below is for the lesson Gate, not the cell)

| staged row | cadence kept | recheck prose stripped from the cell | note for the Gate |
|---|---|---|---|
| S085 | `180d` | re-open the SAMR detail record and confirm 发布日期 2025-12-02 and 实施日期 2026-07-01 are unchanged | both values re-read this round at char 1029 and char 1048; the `(ran 2026-10-23)` marker is a campaign marker and was not this round's check |
| S086 | `180d` | re-open the openstd record and confirm the notice still reads "本系统不提供文本阅读服务" | the notice is one line at char 15188 and the string occurs once; this round read the capture, not a live fetch |
| S093 | `180d` | re-download the PDF and confirm section 7.3 still reads "电子资源既应著录文献类型标识，也应著录文献载体标识" | that sentence occurs 0 times as one string in the text form: it is split after `…也应著录文` (char 11542) with `献载体标识。` on the next line; it occurs once in the whitespace-free form, so the prose must be reworded or the check done on that form |

## 6. Findings (reported, not patched)

1. Staged S085's `used-by` names `corpus/knowledge/citation-version-binding-r36.md`, but that lane entry says at
   line 21: "Staged S082, the SAMR record for GB/T 7714-2025, is not adopted." Its stated flip is "a text capture
   of that record contains the issued and effective dates as a contiguous span" — in this capture the dates are
   separated by ` 实施 于 ` / `实施日期` (verified: gap `' \n\n 实施 于 '`), and `2025-12-022026-07-01` is absent
   from both the raw and the whitespace-free form, so the flip is not met by these bytes. The new rows therefore
   name only the r36 entry the citing side owns; naming the refusing entry would also break `used == citing`.
2. The openstd `.txt` sidecar is byte-identical to its `.raw` (sha256 2d68faf7c724eb1b, 24185 bytes): its "text
   form" is the served HTML, so its quotes are HTML-line fragments. The notice quote is a bare text node on one
   line, so it survives, but a reader expecting rendered text will not find one.
3. The JMU PDF text form carries full-width digits (`２０２５－１２－０２`), so any ASCII-date quote against it fails;
   the row's dates come from S121/S122, not from S123.
4. `文献载体标识` alone is not a usable anchor: 32 occurrences (`文献类型标识` 35). The 7.3 sentence must be cut at
   its line break (char 11542, 42 chars) — flagged to EntryStb and now agreed.
5. Anchor offsets are normalized-form offsets. On this capture set the SAMR/ openstd `.txt` files carry CRLF, so a
   raw-byte offset is 877 / 688 characters larger. Both round-54 counters read with newline translation, so the
   row's numbers are consistent with them, but they cannot be compared with the raw file's byte offsets.
6. The three rows must land with their entries, not before: until `source-type-taxonomy-r36/r37.md` exist, the
   lane's own census prints those three paths as missing (reproduced, and expected pre-landing).
7. S101 stays HELD; per R54DraftS101Reanchor a bound S101 would fail ANCHOR_BOUND because the span builder resolves
   an OLE `.doc`'s `char N` in the UTF-16LE raw form while the round-54 corrections are defined-form. My cell change
   does not depend on that, but the L1 must not treat S101 as bound.

## 7. Not done here (out of scope)

No entry, lesson, `quotes.tsv`/`spans.tsv`, quarantine verdict, C1/C2 counter run, README or Gate edit; no staged
file in `/home/vgpnk/Projects/shokuknow` was run or written; no commit/add/stash/jj. Not independently verified:
that the drafted entries really contain the six quotes — only the two entry seats' IRC word, and the census takes
the registry cells only.

Artifact: this file. Scratch `/fast/scratch/hyaku/chousa-r54/R54DraftRows` (quote receipts, candidate tables) was
created under TMPDIR and removed on exit.

VERDICT: attacked the registry side of the GB/T 7714-2025 theme — three rows drafted with 9 located quotes (each count 1, one line, offset re-checked in the counters' normalized form), S101's used-by change drafted against a confirmed citing entry, and staged S085's used-by shown to name an entry that refuses the record — census clean (123 rows, 0 malformed, no dup ids, no enum violations), rows are ready to land with their entries.
