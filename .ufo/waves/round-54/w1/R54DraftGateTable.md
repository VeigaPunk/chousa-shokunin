# R54 W1 — Gate decisions table, theme C (GB/T 7714-2025)

seat R54DraftGateTable (scribe, leaf) · lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` · head `9caf8fc6e9113c8135f930503102eef0dd909e2e`
BASE_REV `c49ffc6ce1c3de87c1dfa96856239ed7274bf07b` · C1 candidate `8a7d0f137a352000d78704ba5695ded8857104fe` (`tools/capture-text.py`)
frozen claims read first (`corpus/evidence/round54/claims.md`); counters read, never edited; no production file written.
scratch `/fast/scratch/hyaku/chousa-r54/R54DraftGateTable` (TMPDIR there; `uv run --with pypdf` used, nothing installed to a PATH dir).
Text forms: `.txt` sidecar read `open(p, encoding="utf-8")` — universal newlines, the read `build-spans.py:122` and `c2-count.py:127` perform.
**The S085 sidecar is CRLF on disk** (6,626 B → 5,749 B after newline translation, 3,591 chars): an offset taken on the raw bytes differs from the
offset `spans.tsv` needs. Every `char N` below is the universal-newline offset.

## Gate — documents

| staged → lane | document | capture on disk (key, size) | decision | reason |
|---|---|---|---|---|
| S085 → **S121** | 全国标准信息公共服务平台 detail record for GB/T 7714-2025 (std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE1…) | `adf6ba934e813b2c326fa150` `.raw` 76,252 B; `.txt` 6,626 B / 3,591 ch; `.txt` sha256 `4e46154f4a841d17…` | **bound** (tier A) | identity, status, adoption basis only: `发布 于 2025-12-02` (1029), `实施 于 2026-07-01` (1048), `本标准非等效采用ISO国际标准：ISO 690:2021。` (1797), `信息与文献 参考文献和信息资源引用指南` (1836), `A14` (1517); carries the 采标情况 block and no text |
| S086 → **S122** | openstd full-text record for the same standard (openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E5…) | `b9ca2a4fdf9455867534f144` `.raw` = `.txt`, 24,185 B / 22,007 ch, 0 U+FFFD | **bound** (tier A, notice only) | not a twin of S121: `采标情况` 0 ×, `非等效采用` 0 ×, `全部代替` 0 × in its form, while S121 has `不提供文本阅读` 0 ×; it is the sole carrier of `该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务` (15,188, unique, one line) |
| S093 → **S123** | 集美大学学报 editorial office's copy of the standard's text (xuebaobangong.jmu.edu.cn/…/64b9ba1b-….pdf) | `0f33243fd7ac2fe88b85c1ba` `.pdf`/`.raw` 6,209,520 B; `.txt` 190,614 B / 83,061 ch (pdftotext, 45 pages, 0 U+FFFD) | **bound** (tier B, scope = "as this reproduction renders it") | operative text only this copy serves: scope clause (5576/5602), 附录A scope sentence (57,785), foreword item o) (4736), 7.6 (14,096); the authority serves none (S122) |
| S101 (lane id held) | 中国学术期刊（光盘版）检索与评价数据规范（修订本）, 哈尔滨工业大学 copy | `6dc68fd6b32ce9c8dfcebce8` `.raw` 129,024 B; old `.txt` 128,416 ch **14,486 U+FFFD**; `capture-text` form 27,012 ch, 0 U+FFFD | **held** | already a lane row at BASE_REV (`SOURCES.md:111`, `used-by` = `citation-count-semantics-r37.md`); the r37 entry's S101 leg is cut (below), so the cell is unchanged |

## Gate — decisions (theme C)

| staged entry | documents (S-ids) | capture on disk (key, size) | province fit | decision | reason | flip |
|---|---|---|---|---|---|---|
| `source-type-taxonomy-r36.md` — "The Chinese citation standard names a source's type, and publishes its text as unreadable" | S085→**S121**, S086→**S122** | as above | **in**: source hierarchy — a record authoritative about its own identity/status while refusing its operative text; claim-vs-source verification for the refusal (QUALITY 87) | **admit, narrowed** | four cuts: (a) the headline's first clause has no document here — S121 carries no type list, the 17 types are S123's, so the title states identity/status/adoption + the no-text notice only; (b) `excludes librarians, bibliophiles and indexers` is S123's clause (`本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。`, 5602) mis-copied into a two-document entry — cut (it also has no `source:` line); (c) the notice never says "ISO/IEC international standards" — it says `ISO、IEC等国际国外组织的标准`, so the *reason* is the portal's own sentence; (d) the staged Unknown "Appendix A was **not** read … see `CANNOT-ANSWER.md`" is false this round — restate as "not read at the authority; read only in the JMU copy (S123)". `ISO 690:2021` must stay in the text (C2 `TERMS`) and is at BASE_REV 0 files (`git grep … c49ffc6 -- corpus/knowledge` → rc 1) | refuse if `发布 于 2025-12-02` or `实施 于 2026-07-01` stops being unique in the S121 `.txt`, or the S122 notice line leaves the page |
| `source-type-taxonomy-r37.md` — "What the Chinese citation standard prescribes, and whom it does not govern" | S093→**S123**; S101 **held** (leg cut) | as above | **in**: the same, plus the standard's own scope limit (who it does not govern) | **admit, narrowed** | five cuts: (a) drop the `source: S101 — …` line and every S101 token — the nine 14.2 elements and the 文献标志码 A–E are already carried by `citation-count-semantics-r37.md` (`source: S101` at `:5`), so the leg is a duplicate of an existing entry and earns no document credit (per-document credit; S101 held); (b) the staged 7.3 quote is a two-line join — re-cut to the one-line `文献类型标识、文献载体标识应按照附录Ａ著录。` (11,542); (c) the "change list" sentence mis-transcribes the foreword: item o) reads `将文献类型“普通图书”“舆图”分别更改为“图书”“地图”` (4736) — the old names are 普通图书 and 舆图, not 图书 and 舆图; (d) "17 document types with **single-letter** codes" contradicts the entry's own list (11 single + 6 two-letter: EB CM DS PP CP DB) — state the counts that hold; (e) drop the token `S075` from the Unknown (not bound this round) — after the cut, S123 is the entry's only `S###` token. Quotes must be **CJK-only** (see QUALITY 96 finding) | refuse if `本文件适用于作者和编制者著录参考文献。` (5576) or `本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。` (5602) stops being unique, or the S123 digest changes |

Row contract for the integrator: each new row `mined`, `opened 2026-10-26`, first source-cell URL = the document's URL, `used-by` = exactly the
entry citing it (one path each) — `c2-count.py:176` compares `used == citing` with `citing` drawn only from the two new entries. Source lines say
`re-opened 2026-10-26` (staged `record read 2026-10-23` is the campaign's date); staged ids S085/S086/S093 must not survive as tokens — they name
other lane rows.

## Gate — neighbours

| staged entry / lane object | decision | reason | flip |
|---|---|---|---|
| staged **S082** SAMR record (round 43/44 numbering) = this package's **S085**; lane entry `corpus/knowledge/citation-version-binding-r36.md:21` carries the refusal | **admit** (= S121, above) — the r43/44 refusal is lifted | the flip **fires**: the record's capture holds both dates in one contiguous span, `s85[1029:1063]` = `发布 于 2025-12-02 \n\n 实施 于 2026-07-01` (34 chars, whitespace only between them), and the round-43/44 ground ("the row was not fetched this round and the flip … was not met", `round-44-verifier-spotcheck.md:141`) is cleared by an on-disk 76,252-B capture. Also a numbering trap for review: today's lane **S082 is the AVeriTeC README** (`SOURCES.md`, round 45 renumber), so `grep S082 corpus/lessons` returns that row, not this record | — |
| `grey-literature-and-chinese-search-record-r40.md` (staged S130, S131, S133) | **refuse** (adoption waits for its own round) | its round-53 flip asked for *a defined OLE `.doc` text form*: that conjunct **now fires** — `python3 tools/capture-text.py .qcache/bdff491a75c6abeda1d9c01d.raw` → rc 0, 13,718 ch, 0 U+FFFD, `是否检索灰色文献` once at **4678** on one line (the old `.txt` sidecar is 241,510 ch with 40,252 U+FFFD). Adoption still waits because (i) its document set is outside this round's frozen by-document set (C2 counts S085/S086/S093 only), (ii) S133 duplicates the lane's S111 URL and so can never be a document of its own, (iii) it has no quote set or spans this round, and (iv) its own recheck string `五个方面` occurs **0** times in both forms — the recheck is itself unverified | round 55: bind S130 under the `capture-text` form with ≥3 located quotes, cut S133 to a `refused-doc` line |
| `amendments/corpus/knowledge/citation-version-binding-r36.md` (package) | **do not land this round** | it cites the theme's own S085 URL (`source: S085 — https://std.samr.gov.cn/…`) as an append to an existing lane entry; landing it makes the real citing set two entries, and `used-by` must then name both, which `c2-count.py:176` (`used == citing`, `citing` ⊆ the two new entries) fails by construction — a post-freeze predicate change, not an option | re-point to S121 and land only where the used-by contract is re-frozen with it |
| `amendments/corpus/knowledge/search-log-method-r39.md` (package) | **do not land this round** | its first source line carries the token **`S123`** for the Europe PMC PRISMA-S article — the id this round plans for the JMU copy; landing it verbatim makes S123 two documents | renumber at adoption; no theme-C content |

Amendment list (the package's only `amendments/` entries): `citation-version-binding-r36.md`, `citation-version-binding-r37.md`,
`search-log-method-r39.md` — **no theme-C amendment exists**; `grep -l "7714\|文献载体\|source-type"` matches only the first (its S085 leg above).
`knowledge/corpus/knowledge/` holds exactly the two staged theme entries, no third theme file.

## Quarantine slice (three register rows on theme URLs; hand-checked, verdict lines for the lesson)

- register `S080` (SAMR record, `https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE1…`) — verdict: absent-as-written. Form: S121 `.txt` (universal-newline UTF-8); the register's `标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01` occurs 0 ×, and `标准号：` 0 × — it splices three table cells and adds colons the form lacks; the substance is on the page as separate rows (`标准号 \n GB/T 7714-2025` char 1327, `发布日期 \n 2025-12-02` char 1354, `实施日期 \n \n 2026-07-01` char 1382; each 1 ×).
- register `S088` (JMU copy, `https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-….pdf`) — verdict: absent-as-written. Form: S123 `.txt`; the slash-joined carrier list with fullwidth Latin occurs 0 ×; the five rows are separate lines, each 1 × (`磁带（ｍａｇｎｅｔｉｃ ｔａｐｅ）` 59025, `缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）` 59201).
- register `S096` (HIT specification, `https://jc.hit.edu.cn/…/1f6f2731-….doc`) — verdict: absent-as-written. Form: this round's `capture-text` form of the `.raw` (27,012 ch, 0 U+FFFD; the old `.txt` form has 14,486 U+FFFD); the `…`-elided splice occurs 0 × in both forms, and its third `<br>` piece `参考文献格式，参照 GB/T 7714，采用` is a paraphrase (0 ×); the nine 14.2 items are separate lines (`c. 文献类型及载体类型标志；` char 12960, `文献标准编号(ISBN，ISSN，……)` 1 ×).

None is `fabricated` or `unverifiable`, so no bound document is blocked (`c2-count.py:269`).

## Findings that change the draft, not the predicate

1. **QUALITY 96 binds the S123 quote set: fullwidth Latin cannot be quoted.** `pdftotext` renders `附录Ａ` / `ＹＹＹＹ－ＭＭ－ＤＤ`, an independent
   pypdf extraction renders `附录A` / `YYYY-MM-DD` (same passage): `文献类型标识、文献载体标识应按照附录Ａ著录。` and the 7.6 sentence are
   **NOT_IN** the independent extraction (0 ×) while four CJK-only candidates are `IN … 1 ×` each. So: quote CJK-only spans; state the 17 types
   and 5 carriers as observation of 表A.1/表A.2 without quoting a row that crosses a Latin code (a `预印本 … ＰＰ` quote fails the check by one code point).
2. **QUALITY 89 / form pinning.** The S101 row's stored `char` cells (11170 … 34374) are offsets of the old raw UTF-16LE decode (128,416 ch,
   14,486 U+FFFD); `capture-text` is now the defined form (27,012 ch) and 34,374 exceeds it. The row is append-only as filed, but no new S101
   quote may be located in the old form — which is a second, independent reason the r37 S101 leg is cut rather than re-quoted.
3. **`citation-count-semantics-r37.md:5` declares S101's form as "UTF-16LE text of the raw capture"** — a form `capture-text` no longer
   produces, so that entry's S101 quotes cannot be re-located with the lane's tool. Route with (2); the row and the entry stay as filed.
4. The r36 entry's staged title also mislabels the source: `publishes its text as unreadable` is about the **portal**, not the standard — keep it
   attached to S122 in the body, or the title states something no document says.

## Commands run (observed output, abridged)

```
$ python3 -c 'key=sha256(url)[:24] …'  → S085 adf6ba93… .raw 76252 / .txt 6626 | S086 b9ca2a4f… 24185/24185 | S093 0f33243f… 6209520 / .txt 190614 | S101 6dc68fd6… 129024
$ python3 tools/capture-text.py .qcache/6dc68fd6b32ce9c8dfcebce8.raw   → rc 0, 27012 chars, FFFD 0
$ python3 tools/capture-text.py .qcache/bdff491a75c6abeda1d9c01d.raw   → rc 0, 13718 chars, FFFD 0, 是否检索灰色文献 @4678
$ uv run --quiet --with pypdf python pdfx.py   → pages 45 chars 58009 wsfree 53799; IN 4 / NOT_IN 2 (附录Ａ, ＹＹＹＹ－ＭＭ－ＤＤ)
$ s85[1029:1063] = '发布 于 2025-12-02 \n\n 实施 于 2026-07-01'   (34 chars, contiguous, whitespace only)
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md → 120 ; tail ids S116…S120 ; S121–S123 free
$ grep -n "S082" corpus/SOURCES.md | cut -c1-100 → 92:| S082 | AVeriTeC dataset README … (the round-45 lane row, not the SAMR record)
$ git grep -l -e "ISO 690:2021" -e "文献载体标识" c49ffc6 -- corpus/knowledge ; rc=1
$ grep -n "^source:" …/grey-literature-and-chinese-search-record-r40.md | cut -c1-60 → 4:S130, 5:S131, 6:S133
```

Tooling: `uv run --with pypdf` (scratch-only, ephemeral; pypdf resolved by uv, no PATH write). No pacman transaction, no network, no fetch.
No `soffice` started by this seat: `pgrep -u $USER -f "UserInstallation=file:///fast/scratch/hyaku/chousa-r54/R54DraftGateTable"` → rc 1, no match.

VERDICT: drafted the round-54 Gate for theme C — bound S121/S122/S123, held S101, admitted both entries narrowed (11 concrete cuts), lifted the
round-43/44 SAMR refusal on a firing flip, kept the grey-literature entry refused with its text-form flip now met, refused to land two package
amendments that collide with `used-by`/`S123`, and handed three `absent-as-written` quarantine verdicts — plus one binding constraint found by
running pypdf against `pdftotext`: fullwidth Latin quotes on S123 fail QUALITY 96 and must not be drafted into the entry.
