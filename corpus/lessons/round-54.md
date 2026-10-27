# Round 54 lesson

author: chousa L1 (hyaku run 9, `ChousaR54`)  
date: 2026-10-26  
base: `c49ffc6ce1c3de87c1dfa96856239ed7274bf07b`  
freeze: `5a1a20630d8176a816a60bb43b0d0e7ee2db19a0`; C1 candidate `8a7d0f137a352000d78704ba5695ded8857104fe`

No external fetch or network egress: L0 `8d77e6c1` remains open. Every source re-opened below is an on-disk capture under the read-only campaign cache `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` (key = first 24 hex of sha256 of the URL), accessed 2026-10-26; the campaign's own quotes and dates were not reused.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| 1. wave handoff reported as dispatched and merely late: the round-53 report says "W2: 43 seats dispatched" and that its results "had not arrived", while the wave has no dispatched marker, no results file, no seat report and 43 of 43 registry members carry `agentId: null` | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-53/chousa.md:14`; at `d21eb285` `.ufo/waves/round-53/w2.ready` exists and `w2.ready.dispatched` / `w2-results.json` do not (`git cat-file -e` → `fatal`); `python3 corpus/evidence/round50/wave-complete-check.py .ufo/waves/round-53/w2-spec.json .ufo/waves/round-53/w2 --rev d21eb285 --lane .` → `OK 0/43`, exit 1 (W1 `R54DraftMistakes` R1) | none — QUALITY 75's check existed and was not run before filing | QUALITY 99: a wave is reported dispatched only with the dispatcher's `.ready.dispatched` marker or results file. Shown able to fail: the same check prints `OK 0/43` exit 1 for round-53 W2 and `OK 49/49` for round-53 W1. This round's report cites `w1.ready.dispatched` and the results file for each wave it calls dispatched |
| 2. anchor in an undefined text form: nine Registry offsets (S100 ×3, S101 ×6, round 49) index a whole-file UTF-16LE decode of the `.doc` that no lane command prints — 263 U+FFFD, 243 `0x0B`, a binary preamble — so every offset lands elsewhere in the defined form (S101 `11170→11972` … `34374→25123`; S100 `1296→16`, `1431→151`, `2843→492`) | `corpus/SOURCES.md:110-111` anchor cells "(UTF-16LE text of the raw .doc capture)"; `corpus/lessons/round-49.md:92-100`; W1 `R54DraftMistakes` R2, `R54DraftS101Reanchor` | none — QUALITY 76's `decode-form-check.py` passes the row because it only requires the form to be named (`DECODE_FORM=PASS`) | the OLE text form (C1) plus nine anchored `correction:` lines into tool dumps (`SCORECARD.md` "Round 54 pointer corrections"; `corpus/evidence/round54/S100-text-form.txt`, `S101-text-form.txt`) and QUALITY 97. Shown able to fail: on a mirror without the two dumps `pointer-anchor-check.py` prints `BAD=6` exit 1 (W1 `R54DraftS101Reanchor`); with them `ANCHORED=16/16` exit 0. Caught again in round: W1 `R54DraftEntryStb` anchored four new S101 quotes "in the raw UTF-16LE text form"; the L1 cut that leg rather than write new anchors in that form (`## Gate`) |
| 3. runtime artifact left uncommitted at the round tip: round-53 W2's swarm registry existed only on disk | `corpus/lessons/round-53-verifier-spotcheck.md:13,78`; `git cat-file -e d21eb285:.ufo/waves/round-53/w2/swarm-registry.json` → exit 128 | the closure (non-author) | committed in the round-54 freeze `5a1a2063` (`git cat-file -e 5a1a2063:…` → exit 0); this round commits each wave's registry with its integration commit |
| 4. forgeable frozen capability counter, sixth round running (RW-1): the round-54 C1 counter left each generated document's HTML source beside it and pinned REAL by digest, so a tool that reads the sibling HTML and returns canned LibreOffice exports passed 6/6 on four runs | W1 `R54CritForgeC1` (four runs `LEGS=6/6`); rebuilt as `corpus/evidence/round54/controls/build-c1-forge.py`, receipt `controls/c1-forge.txt` | QUALITY 85 (work dirs carry random names) — it did not cover a generator's input files left in the work tree | post-freeze supplement `corpus/evidence/round54/c1-supplement.py` (ISOLATED, RESAVE, HELDOUT): candidate 3/3, rebuilt forge 0/3 (`controls/c1-forge.txt`); QUALITY 98's named limit. Not the frozen rule (claims-erratum E1) |

## Spot-check intake

`corpus/lessons/round-53-verifier-spotcheck.md` section 6, item by item: (1) the uncommitted W2 registry — committed at the freeze, Mistakes row 3; (2) round-53 W2 never ran — recorded as not dispatched (Mistakes row 1, QUALITY 99); (3) receipt discipline — this round's before, control, forge, supplement and after receipts are standalone files under `corpus/evidence/round54/` (`controls/c1-before.txt`, `controls/c1-controls.txt`, `controls/c1-forge.txt`, `controls/c2-before.txt`, `controls/c2-controls.txt`, `c1-after-candidate.txt`, `measure-after.txt`); (4) report label — the report names the tool-file sha256 for C1; (5) the five W04 duplicate-url warnings — still present, carried (not this round's surface); (6) the forgeable counter streak — Mistakes row 4: the frozen counter carries a sample-size guard and a counting-time oracle, and is still forgeable; the supplement closes the three shortcuts found. The closure's discernment table agreed with every round-53 decision, so no criterion changes for disagreement.

## Gate

### Collision check (section 10, 0–3-space pattern, scratch)

`.ufo/waves/round-54/assimilation/` (L1 commands; W1 `R54ExecCollision` re-derived all four files byte-identical): `reg-ids` 120 (S001–S120), `staged-ids` 114, `collisions` 39 (first S082, last S120), `quarantine-slice` 24. Guard proved in `guard-proof.txt`: a two-space-indented `  | S002 |` row collides under the 0–3-space pattern and not under the column-zero one. Renumber by document (adopter `--entry` for the two admitted entries): S085→S121, S086→S122, S093→S123; staged S101 is the lane's S101 by URL (`held`), not cited this round.

### Re-opened sources (access 2026-10-26; no fetch)

| lane id | document | URL | text form | headline quote (location) |
|---|---|---|---|---|
| S121 | GB/T 7714-2025 record, 全国标准信息公共服务平台 | https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F | `.txt` UTF-8 (universal newlines), 3,591 characters | 本标准非等效采用ISO国际标准：ISO 690:2021。 (char 1797) |
| S122 | GB/T 7714-2025 on the openstd full-text portal | http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14 | `.txt` = the served HTML, 22,007 characters | 该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务 (char 15188) |
| S123 | GB/T 7714—2025 text, the 集美大学学报 journal office's PDF reproduction | https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf | `.txt` (pdftotext) 83,061 characters; quotes cross-checked against pypdf under NFKC (`pdf-crosscheck.py`: `PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14`, the 14 width-only) | 文献类型标识、文献载体标识应按照附录Ａ著录。电子资源既应著录文献类型标识，也应著录文 (char 11542) |

Recheck prose stripped from the staged rows (W1 `R54DraftRows`; the rows keep `180d`): S085 "re-open the SAMR detail record and confirm 发布日期 2025-12-02 and 实施日期 2026-07-01 are unchanged"; S086 "re-open the openstd record and confirm the notice still reads 本系统不提供文本阅读服务"; S093 "re-download the PDF and confirm section 7.3 still reads …" (its quoted sentence crosses a line break in the text form; the entry's `recheck:` uses the one-line cut). Each entry's `recheck:` line carries a runnable command.

### Decisions (theme C, the PRC citation standard GB/T 7714-2025; W1 `R54DraftGateTable`, re-decided by the L1 where the entry drafts narrowed)

| staged entry | documents | capture on disk | province fit | decision | reason | flip |
|---|---|---|---|---|---|---|
| `source-type-taxonomy-r36.md` | S085→S121, S086→S122 | `adf6ba934e813b2c326fa150` (.raw 76,252 B, .txt 6,626 B); `b9ca2a4fdf9455867534f144` (24,185 B) | in: source hierarchy — what an authority's record proves about a standard and where it stops | **admit, narrowed** | the staged headline ("publishes its text as unreadable") is about the portal's own service, so it is narrowed to the notice; the type enumeration is cut (neither page carries it, sweep in the entry); the librarian clause belongs to S123 and is cut here | — |
| `source-type-taxonomy-r37.md` | S093→S123; staged S101 (= lane S101, held) | `0f33243fd7ac2fe88b85c1ba` (.raw/.pdf 6,209,520 B, .txt 190,614 B) | in: source hierarchy and citation chaining — the standard's own scope clause and its normative code tables | **admit, narrowed** (S123 only) | the 7.3 quote is re-cut at its line break; the change-list wording is corrected (普通图书, not 图书); the normative/informative appendix status is added | — |
| the S101 leg of the r37 draft | lane S101 (HIT data specification `.doc`) | `6dc68fd6b32ce9c8dfcebce8.raw` 129,024 B | in | **refuse (this round)** | the W1 draft anchored four new S101 quotes in the raw UTF-16LE decode — the form Mistakes row 2 finds undefined — and the frozen span builder has no OLE text form; S101's `used-by` is therefore unchanged | a span builder that reads an OLE `.doc` through `tools/capture-text.py`, and the four quotes re-located in that form |
| `grey-literature-and-chinese-search-record-r40.md` | S130, S131, S133 | `bdff491a75c6abeda1d9c01d.raw` 243,929 B | in for the record field | **refuse (still)** | the text-form half of its round-53 flip now fires (`是否检索灰色文献` once at 4678 in the defined form, 0 U+FFFD), but the entry is outside this round's frozen document set, S133 duplicates the lane's S111 URL, and no quote set exists | its own round, with quotes located in the defined form |
| package amendment `citation-version-binding-r36.md` | the theme's S085 URL | — | in | **not landed** | landing it makes the S121 citing set two entries; the frozen `used-by == citing` rule is counted over the two new entries | re-point to S121 in a round whose counter covers it |

refused-entry: none.

### Quarantine slice (hand-checked this round)

The lane's register slice has 24 data rows (`quarantine-slice`); three name a theme URL. Verdicts (W1 `R54DraftGateTable`, `R54GroundSamrA/B`, `R54GroundJmuA/B`, `R54DraftReadme`; text forms as above):

- register `S080` (round1) — https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F — verdict: absent-as-written — the joined `标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01` occurs 0 times and `标准号：` 0 times in the S121 form; the three values sit as separate cells, each once (`发布 于 2025-12-02` char 1029, `实施 于 2026-07-01` char 1048).
- register `S088` (round2) — https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf — verdict: absent-as-written — the slash-joined carrier list occurs 0 times; its five rows are separate lines of 表Ａ．２, each once (`磁带（ｍａｇｎｅｔｉｃ ｔａｐｅ）` 59025 … `缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）` 59201).
- register `S096` (round2) — https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc — verdict: absent-as-written — read in the defined OLE form (27,012 characters, 0 U+FFFD): the `…`-elided splice occurs 0 times; its third piece `参考文献格式，参照 GB/T 7714，采用` is not in the capture, whose parameter table reads `参考文献格式，参照ISO 690` (char 25123). This supersedes round 42's `unverifiable` for this row, which rested on the capture being binary.

None is `fabricated` or `unverifiable`; no bound document is blocked.

### Admit and reject for the non-author spot-check

Admit `source-type-taxonomy-r36.md` (S121): re-open the `.txt` and check `本标准非等效采用ISO国际标准：ISO 690:2021。` once at char 1797, and that the S122 notice is about `本系统` (the portal), not the document. Admit `source-type-taxonomy-r37.md` (S123): check `本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。` once at char 5602. Reject the S101 leg: check that S101's `used-by` is unchanged and that no `source: S101` line is in either entry. Reject S130: check that the defined form holds `是否检索灰色文献` once and that no entry cites it.

## considerthese

`considerthese/2026-10-26.md` proposal 1 (stable proposal ids; W1 `R54ScoutConsiderthese` found it implemented nowhere) implemented as `corpus/evidence/round54/considerthese-ledger.tsv` with `corpus/evidence/round54/considerthese-ledger-check.py`: ids `CT-YYYYMMDD-n` assigned lane-side (considerthese/ untouched); `python3 corpus/evidence/round54/considerthese-ledger-check.py --root .` → `PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0`, exit 0; a dropped row, a dead pointer, a stale regex or a new unledgered bullet each exit 1 (seat receipts). Proposal 4 (an independent CJK spot-check) needs a reader the lane does not dispatch: ledger `FMT`.

## All located quotes

Every quote below is ≤25 whitespace words and ≤160 characters, on one line of its `.txt` form, occurring there exactly once at the stated offset (`python3 corpus/evidence/round54/build-spans.py --check` → `STALE=0`).

| id | char | quote | entry |
|---|---:|---|---|
| S121 | 477 | 推荐性 | `corpus/knowledge/source-type-taxonomy-r36.md` |
| S121 | 537 | 由 TC4 （全国信息与文献标准化技术委员会）归口 | `corpus/knowledge/source-type-taxonomy-r36.md` |
| S121 | 1029 | 发布 于 2025-12-02 | `corpus/knowledge/source-type-taxonomy-r36.md` |
| S121 | 1048 | 实施 于 2026-07-01 | `corpus/knowledge/source-type-taxonomy-r36.md` |
| S121 | 1162 | （全部代替） | `corpus/knowledge/source-type-taxonomy-r36.md` |
| S121 | 1797 | 本标准非等效采用ISO国际标准：ISO 690:2021。 | `corpus/knowledge/source-type-taxonomy-r36.md` |
| S122 | 13300 | 标准号：GB/T 7714-2025 | `corpus/knowledge/source-type-taxonomy-r36.md` |
| S122 | 14082 | 英文标准名称：Information and documentation—Rules for bibliographic references and citations to information resources | `corpus/knowledge/source-type-taxonomy-r36.md` |
| S122 | 15188 | 该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务 | `corpus/knowledge/source-type-taxonomy-r36.md` |
| S122 | 16105 | 2025-12-02 | `corpus/knowledge/source-type-taxonomy-r36.md` |
| S122 | 16321 | 2026-07-01 | `corpus/knowledge/source-type-taxonomy-r36.md` |
| S122 | 17078 | 国家市场监督管理总局、国家标准化管理委员会 | `corpus/knowledge/source-type-taxonomy-r36.md` |
| S123 | 5576 | 本文件适用于作者和编制者著录参考文献。 | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 5602 | 本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。 | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 11542 | 文献类型标识、文献载体标识应按照附录Ａ著录。电子资源既应著录文献类型标识，也应著录文 | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 14096 | 电子资源的创建日期、发布日期、修改日期、引用日期应按照“ＹＹＹＹ－ＭＭ－ＤＤ”格式，用阿拉伯数字 | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 4812 | 增加了电子资源载体“缩微资料”及其标识代码 | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 4736 | 将文献类型“普通图书”“舆图”分别更改为“图书”“地图” | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 4852 | 将“ＥＢ”代表的文献类型更改为“网站、网页” | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 21382 | 图书主要贵任者 | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 82465 | 中国标准出版社出版发行 | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 82834 | ２０２５年１２月第１版 ２０２５年１２月第１次印刷 | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 3602 | 本文件代替ＧＢ／Ｔ ７７１４—２０１５《信息与文献 参考文献著录规则》 | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 424 | ２０２５－１２－０２发布 | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 490 | ２０２６－０７－０１实施 | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 5751 | ＧＢ／Ｔ ４８９４ 信息与文献 基础和术语 | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 2512 | 附录Ａ（规范性） 文献类型和文献载体标识代码 | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 2655 | 附录Ｂ（资料性） | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 58840 | 电子资源载体和标识代码应按照表Ａ．２著录。 | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 59201 | 缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ） | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 57965 | 图书                          Ｍ | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 8881 | “／”用于合期的期号或合卷的卷号间（见８．５．１．２）、文献载体标识前。 | `corpus/knowledge/source-type-taxonomy-r37.md` |
| S123 | 5982 | 以数字方式将图、文、声、像等信息存储在磁、光、电介质上 | `corpus/knowledge/source-type-taxonomy-r37.md` |

## Census

Round start (`corpus/evidence/round54/census-start.txt`): exit 0, `ok`, five pre-existing W04 (S051 S053 S073 S074 S075). Round end: `corpus/evidence/round54/census-end.txt`. Rows 120 → 123 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`); added S121 (A), S122 (A), S123 (B); no existing row touched (S101 `used-by` unchanged).

## Disclosed post-freeze changes

`corpus/evidence/round54/claims-erratum.md`.
