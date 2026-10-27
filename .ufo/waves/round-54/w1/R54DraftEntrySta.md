# R54DraftEntrySta — r36 entry draft (GB/T 7714-2025: SAMR record + openstd notice)

Lane: chousa-shokunin. Scope: draft ONE entry, `corpus/knowledge/source-type-taxonomy-r36.md`, from the
staged package file `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/source-type-taxonomy-r36.md`.
Frozen C2 predicate, counters, registry and lesson untouched; no production file, index, jj/git state or
sibling lane written. No network, no live fetch (L0 `8d77e6c1` open): every source is the on-disk `.qcache`
capture named in the seed. Planner seat held by the L1; no subagent dispatched.

## What the draft does

- Cites the two documents as planned lane ids: `S121` = the SAMR record
  (`https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F`, text form
  `.qcache/adf6ba934e813b2c326fa150.txt`, 3,591 chars) and `S122` = the openstd full-text page
  (`http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14`, text form
  `.qcache/b9ca2a4fdf9455867534f144.txt`, 22,007 chars). Provenance trio (source lines, `verified-at:
  2026-10-26`, `recheck: 180d` + command), `ground:`, `adopted:`, then Observation / Inference / Unknown.
- Holds the C2 NEW_GROUND term `ISO 690:2021` inside a located quote: `本标准非等效采用ISO国际标准：ISO 690:2021。`
  at char 1797 of the record's text form (count 1, one line). No `S###` token survives except `S121`/`S122`
  on the two `source:` lines (verified by regex over the draft: `IDS ['S121', 'S122']`).
- Narrowed from the staged text, with the reason in `#### Unknown`: the staged headline "publishes its text
  as unreadable" is dropped (the page's sentence is about the portal's own system — `本系统` — and names
  copyright); the staged enumeration of document types is dropped with the type table it came from (the
  bracketed codes occur 0 times in both text forms); the staged claim that the lane held no Chinese row is
  dropped as stale; the staged tier inference is restated as the lane's inference, each bullet carrying an
  S-id and a verbatim phrase.
- Adds what the two prior entries do not hold. `citation-version-binding-r36.md` names GB/T 7714-2025 only
  in its `#### Unknown` as a staged row it did not adopt; this entry supplies the record itself (number,
  both dates, replacement block, technical committee, adoption basis) and records that the entry's
  180-day flip is met line by line, not as one contiguous span. `citation-count-semantics-r37.md` reaches
  ISO 690 and GB/T 7714 only through a university-hosted data specification's format clauses; this entry
  reaches the authority instead, and adds the authority's own statement that it serves no text reading.

## Gates run (observed output)

1. BASE-REV novelty of the terms (the counter's NEW_GROUND leg), from the lane root:
   `git grep -l -e 'ISO 690:2021' -e '文献载体标识' c49ffc6ce1c3de87c1dfa96856239ed7274bf07b -- corpus/knowledge`
   prints nothing, `RC=1`; `git grep -c -e 'GB/T 7714-2025' <same rev> -- corpus/knowledge` prints one row
   (`citation-version-binding-r36.md:1`) and no other.
2. Span build over MY quotes only, into MY scratch root (never the lane's `corpus/evidence/round54/`):
   `python3 corpus/evidence/round54/build-spans.py --root /fast/scratch/hyaku/chousa-r54/R54DraftEntrySta/root`
   printed `QUOTE S121 char 477|537|1029|1048|1162|1797`, `QUOTE S122 char 13300|14082|15188|16105|16321|17078`,
   `SPANS_ROWS=12 WRITTEN=12` — every quote occurs exactly once in its `.txt` form, on one line, span longer
   than quote, and the offsets match the anchors the registry-row seat (`R54DraftRows`) is writing.
3. Lane bar tool: `python3 tools/inference-ground.py --entry <draft> --spans <my spans.tsv> --counts /dev/null
   --registry corpus/SOURCES.md --root <scratch root>` prints
   `GROUND entry=corpus/knowledge/source-type-taxonomy-r36.md section=1 bullets=5 tokens=6 grounded=6` and
   `GROUND: PASS`. Two earlier runs found five distinct defects, all fixed: bullets 3 and 4 cited no S-id,
   and the bare numerals `16105`, `16321`, `3453` sat outside backticks (the tool reads them as figures).
4. `python3 corpus/evidence/round51/quote-substance-check.py <my spans.tsv>` prints `IDS=2 QUOTES=12 FAILURES=0`
   (exit 0).
5. Invariant pass over the draft: 12 quote rows, `MISSING_IN_ENTRY []`, `MAXWORDS 11 MAXCHARS 110`,
   `IDS ['S121','S122']`, `ENTRY_LINES 36`, sections `Observation / Inference / Unknown`; both
   `^source: S121 — <url>` and `^source: S122 — <url>` match the counter's regex.

Not run, by boundary: the frozen counter itself (`c2-count.py`) — the entry is a draft in scratch, so the
lane still reads `ENTRIES=0/2`; the L1 runs it after integration.

## Entry text — `corpus/knowledge/source-type-taxonomy-r36.md`

```markdown
# The PRC citation standard's number, its two dates and an ISO 690:2021 adoption basis sit on the authority's record page, and the authority's own full-text page states that it serves no text reading

source: S121 — https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F — 全国标准信息公共服务平台 record of GB/T 7714-2025: the byline sentence, the 标准状态 block, the 代替 block, the 基础信息 fields and the 采标情况 block; text form `.qcache/adf6ba934e813b2c326fa150.txt` read as UTF-8, 3,591 characters — char 537, char 1029, char 1048, char 1162, char 1797
source: S122 — http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14 — 国家标准全文公开系统 page for the same standard: the 标准号 line, the 英文标准名称 line, the copyright notice under the record table, and 发布单位; text form `.qcache/b9ca2a4fdf9455867534f144.txt` read as UTF-8, 22,007 characters — char 13300, char 14082, char 15188, char 17078
verified-at: 2026-10-26 — both captures re-opened read-only from the campaign cache and every quoted phrase re-located in its text form with `text.find` (count 1 each, on one line); no fetch made (L0 `8d77e6c1` open)
recheck: 180d — `python3 -c "import pathlib;c=pathlib.Path('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache');a=(c/'adf6ba934e813b2c326fa150.txt').read_text(encoding='utf-8');b=(c/'b9ca2a4fdf9455867534f144.txt').read_text(encoding='utf-8');print(a.count('本标准非等效采用ISO国际标准：ISO 690:2021。'),a.find('本标准非等效采用ISO国际标准：ISO 690:2021。'),b.count('由于涉及版权保护问题，本系统不提供文本阅读服务'),b.find('由于涉及版权保护问题，本系统不提供文本阅读服务'))"` prints `1 1797 1 15212`; then re-open both pages and confirm the 采标情况 block still prints the ISO designation and the portal still prints the copyright notice
ground: source hierarchy — what a standards authority's own record proves about a standard, and where that proof stops. The lane's two prior entries name this standard and hold neither document: `citation-version-binding-r36.md` names GB/T 7714-2025 only in its `#### Unknown`, as a staged row it did not adopt, and `citation-count-semantics-r37.md` reaches ISO 690 and GB/T 7714 only through a university-hosted data specification's format clauses (its 14.1, 14.4 and parameter-table lines). At this round's base the term `ISO 690:2021` occurs in no `corpus/knowledge` file (`git grep -l -e 'ISO 690:2021' -e '文献载体标识' c49ffc6ce1c3de87c1dfa96856239ed7274bf07b -- corpus/knowledge` prints nothing, exit 1), and the designator GB/T 7714-2025 in exactly one, that Unknown line (`git grep -c -e 'GB/T 7714-2025'` at the same revision prints `1` for that file and no other). This entry adds the authority's own record rather than a copy's: the number, the two dates, the replacement relation, the technical committee and the ISO adoption basis.
adopted: round 54 from the campaign package merge/chousa/ (staged `knowledge/corpus/knowledge/source-type-taxonomy-r36.md`), re-bound by document to this lane's S121 and S122; the staged headline and the staged tier judgement are narrowed, and the staged statement that the lane held no Chinese row is dropped (see `#### Unknown`)

#### Observation

- **The record fixes the number, the status and the two dates.** The 标准号 field prints GB/T 7714-2025 (the designator occurs twice in the text form, chars 1239 and 1333), the 标准状态 block prints `发布 于 2025-12-02` (`S121`, char 1029) and `实施 于 2026-07-01` (char 1048), and 现行 occurs twice (chars 489 and 1261) with 推荐性 once (char 477): the record presents a recommended national standard in force.
- **The replacement of the 2015 edition is a block, not a sentence.** Its 代替 block prints the designator GB/T 7714-2015 and, several lines below in the same block, `（全部代替）` (`S121`, char 1162); the 2015 designator occurs twice in the text form (chars 1136 and 1426) and the words 全部代替 twice (chars 1163 and 1415), so neither the designator nor the qualifier can be quoted whole as a unique string, and the relation is read from the block rather than from one sentence.
- **The adoption basis is a labelled field.** 采标情况 (char 1787) prints `本标准非等效采用ISO国际标准：ISO 690:2021。` (`S121`, char 1797), and the next non-blank line gives the ISO document's Chinese title, 采标中文名称:信息与文献 参考文献和信息资源引用指南。 (char 1829). `ISO 690` occurs once in this text form and `690` once.
- **The committee and the supervising department are separate fields.** The byline sentence reads `由 TC4 （全国信息与文献标准化技术委员会）归口` (`S121`, char 537) and continues that 主管部门为 国家标准委 (char 575); in 基础信息 the 归口单位 and 执行单位 both print 全国信息与文献标准化技术委员会 and 主管部门 prints 国家标准委 (char 1759).
- **The full-text portal serves the record fields and states that it serves no text reading.** Its notice reads `该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务` (`S122`, char 15188): the portal's own system offers no text-reading service for a standard that adopts ISO/IEC documents, for copyright protection. The same page prints `标准号：GB/T 7714-2025` (char 13300) and `英文标准名称：Information and documentation—Rules for bibliographic references and citations to information resources` (char 14082), gives 发布日期 and 实施日期 as label/value pairs on separate lines (values at chars 16105 and 16321, the record's two dates), and prints the 发布单位 `国家市场监督管理总局、国家标准化管理委员会` (char 17078).
- **The two authority pages do not print the same 归口 body.** The record's 归口单位 is 全国信息与文献标准化技术委员会 (`S121`, `由 TC4 （全国信息与文献标准化技术委员会）归口`); the portal's 归口部门 label (char 16726) is followed on its value line by 国家标准委 (char 16815), the value its 主管部门 field also carries (char 16638). 国家标准委 occurs twice in the portal's text form, so that value is not quotable there.
- **Neither text form carries a clause or a type code of the standard.** In both forms 附录, 文献类型, 文献类型标识, 载体标识, [M], [J] and EB/OL each occur 0 times (sweep in `#### Unknown`); 著录 occurs 5 times in the record and once on the portal, and four of the record's five are inside the title 信息与文献 参考文献著录规则, the fifth inside a related standard's title in the 相近标准 list (标准文献题录著录规则, char 2993).

#### Inference

- **A record page proves the record's fields; it does not carry the standard's clauses.** `S121` prints the adoption basis (`本标准非等效采用ISO国际标准：ISO 690:2021。`) and `S122` the number (`标准号：GB/T 7714-2025`), while neither text form holds 附录, 文献类型 or a bracketed document-type code (0 occurrences in both, sweep in `#### Unknown`). A row scoped to the identity, status and adoption basis of this standard is grounded on these two pages; a row scoped to the type table the standard is said to prescribe has no readable authority source in this lane's captures, and no lane row should quote such a table from memory or from a vendor mirror.
- **The dates and the replacement relation are the record's own reported state, and the dates repeat on a second authority page.** `S121` prints `（全部代替）` between the two editions' designators and gives both dates; `S122` prints the same two dates under 发布日期 and 实施日期 at `char 16105` and `char 16321`. The pair agrees on the dates and only one of the two carries the replacement block, so a reader who wants the edition relation must read the record and a reader who wants the portal's fields must read the portal.
- **The notice is the portal's statement about its own service, not a property of the document.** Its subject is the system and its stated reason is copyright (`S122`: `该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务`); nothing in the sentence says the document's text is unreadable, and the record page still offers a 查看文本 control (`S121`, `char 3453`) whose target this round did not open. What these pages support is that the authority serves the record and, for this standard, no reading service; the stronger claim that the text is unavailable belongs to no line here.
- **A field is read on the page that prints it.** The record's 归口单位 prints 全国信息与文献标准化技术委员会 (`S121`: `由 TC4 （全国信息与文献标准化技术委员会）归口`) while the portal's 归口部门 label prints 国家标准委 (`S122`, the 归口部门 and 主管部门 value lines); the two pages fill fields of similar name with different bodies, so carrying either value into the other page's field would misstate the record, and this entry quotes each field only where it is printed.
- **The tier judgement the two records support is the lane's, and it is about scope.** At the authority the identity is answerable field by field (`S121`: `本标准非等效采用ISO国际标准：ISO 690:2021。`) and the issuer is printed there too (`S122`: `国家市场监督管理总局、国家标准化管理委员会` as 发布单位), so a row scoped to the identity, status and adoption basis of this standard can rest on these pages; a row scoped to the document-type taxonomy the standard prescribes cannot, because the taxonomy is not in either capture. Type and tier are different axes: naming what kind of thing a citation points to is a fact about form, never evidence of authority for a claim.

#### Unknown

- **Sweep: clause and type-table vocabulary in both text forms.** `python3 -c "import pathlib;c=pathlib.Path('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache');a=(c/'adf6ba934e813b2c326fa150.txt').read_text(encoding='utf-8');b=(c/'b9ca2a4fdf9455867534f144.txt').read_text(encoding='utf-8');w=('附录','文献类型','文献类型标识','载体标识','[M]','[J]','EB/OL','ISO 690','ISO','采标','非等效','代替','GB/T 7714-2015','GB/T 7714-2025','著录','2025-12-02','2026-07-01','查看文本','现行');print(len(a),len(b));print([a.count(x) for x in w]);print([b.count(x) for x in w])"` prints `3591 22007`, `[0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 3, 2, 2, 5, 2, 2, 1, 2]` and `[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 1, 1, 0, 1]`.
- **What the sweep counts.** They are counts over the 3,591-character record form and the 22,007-character portal form (the portal's form is its page HTML read as text). A page rendered as an image, an attached PDF or a click-through viewer would not appear in either form; no OCR, no preview modal and no 查看文本 target was opened this round, so the count of 0 for the type-table tokens is a statement about these two captures.
- **The standard's operative text and its type table were not read.** 附录, 文献类型 and the bracketed codes occur 0 times in both forms, and the portal's own notice says why it serves no reading service; the table attributed to the 2025 edition by the campaign package has no readable authority source in this lane's captures this round.
- **Staged material narrowed on adoption.** The staged headline said the standard publishes its text as unreadable; the page's sentence is about the portal's system and names copyright, so that headline is dropped and only the notice is carried. The staged tier inference is kept as the lane's inference with its quotes; the staged statement that the lane held no Chinese row against which to check its tier rule is dropped as stale, and the staged enumeration of document types is dropped with the type table it came from.
- **The flip in `citation-version-binding-r36.md` is met line by line, not as one span.** That entry's `#### Unknown` asks for the issued and effective dates as a contiguous span; this capture prints them in one 标准状态 block as two adjacent lines (chars 1029 and 1048), so the record now grounds the dates and no single contiguous string holds both.
- **Whether the standard is applied anywhere.** The record prints 现行 and an 实施日期 of 2026-07-01; whether any publisher, index or journal applies this edition, and which document-type identifiers they use, was not checked.
- **What the adoption relation means for the text.** 非等效采用 names an adoption relation between the documents; which clauses differ from ISO 690:2021 cannot be read from either page, and this entry cites no copy of the standard's text, since a third-party copy would prove what that copy carries and not what the authority issued.
```

## QUOTE machine lines (5 columns; staged-id column = planned LANE id)

```
QUOTE	S121	https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F	推荐性	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S121	https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F	由 TC4 （全国信息与文献标准化技术委员会）归口	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S121	https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F	发布 于 2025-12-02	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S121	https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F	实施 于 2026-07-01	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S121	https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F	（全部代替）	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S121	https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F	本标准非等效采用ISO国际标准：ISO 690:2021。	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	标准号：GB/T 7714-2025	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	英文标准名称：Information and documentation—Rules for bibliographic references and citations to information resources	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	2025-12-02	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	2026-07-01	corpus/knowledge/source-type-taxonomy-r36.md
QUOTE	S122	http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14	国家市场监督管理总局、国家标准化管理委员会	corpus/knowledge/source-type-taxonomy-r36.md
```

## Span rows and located offsets (from the build above)

```
S121	char 477	推荐性
S121	char 537	由 TC4 （全国信息与文献标准化技术委员会）归口
S121	char 1029	发布 于 2025-12-02
S121	char 1048	实施 于 2026-07-01
S121	char 1162	（全部代替）
S121	char 1797	本标准非等效采用ISO国际标准：ISO 690:2021。
S122	char 13300	标准号：GB/T 7714-2025
S122	char 14082	英文标准名称：Information and documentation—Rul
S122	char 15188	该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提
S122	char 16105	2025-12-02
S122	char 16321	2026-07-01
S122	char 17078	国家市场监督管理总局、国家标准化管理委员会
```

Capture digests (`.txt` sidecars, as recorded in the manifest):
`adf6ba934e813b2c326fa150.txt` = `4e46154f4a841d17d858eafb5c0099257030f301daadcaa30c37f2e668fb7138`;
`b9ca2a4fdf9455867534f144.txt` = `2d68faf7c724eb1baca6c201613cbf0607589ca017153461a9357760d1c8caf1`.

## Touched surfaces

- Written: this report, and (inside it) the entry text above. Nothing else in the lane.
- Scratch, removed before finish: `/fast/scratch/hyaku/chousa-r54/R54DraftEntrySta/` (draft entry,
  `quotes.tsv`, derived `spans.tsv` + `spans/`, `TMPDIR`). No LibreOffice run this seat, so no profile and
  no `soffice.bin`.
- Read only: the two `.qcache` sidecars, `claims.md`, `c2-count.py`, `build-spans.py`,
  `inference-ground.py`, `quote-substance-check.py`, the staged r36 file, `citation-version-binding-r36.md`,
  `citation-count-semantics-r37.md`, `corpus/SOURCES.md` (for the tool's registry titles only).

## Out of scope (left to other seats)

- `corpus/evidence/round54/quotes.tsv` / `spans.tsv` integration, `corpus/SOURCES.md` rows and `anchor`
  cells (agreed with `R54DraftRows`: S121 anchors 477, 1029, 1048, 1797; S122 anchors 15188, 16105, 16321;
  my four extra rows — S121 537, 1162; S122 13300, 14082, 17078 — are unanchored but needed as grounding
  tokens), the round-54 lesson and its re-check verdict lines, the r37 entry, and the counter run.
- The lesson MUST carry all 12 quotes byte-exact (`QUOTES_IN_LESSON=12/12`), or C2 fails on my rows.
- S101's `used-by` update belongs to the r37 entry; this entry does not cite the HIT specification.

## Findings

1. **The two authority pages disagree on the 归口 body.** The record's 归口单位 is
   全国信息与文献标准化技术委员会 (`由 TC4 （全国信息与文献标准化技术委员会）归口`, char 537); the portal's
   归口部门 label (char 16726) is followed by 国家标准委 (char 16815), the same value its 主管部门 field
   carries (char 16638). Neither page can be quoted for the other's field. Recorded as an Observation and
   the Inference "a field is read on the page that prints it".
2. **The notice is a service statement, not a legibility claim.** `本系统不提供文本阅读服务` names the
   portal's system and copyright; the record page still offers a 查看文本 control (char 3453, unopened).
   The staged headline is thereby narrowed rather than carried.
3. **The type table is absent from both text forms**: 附录, 文献类型, 文献类型标识, 载体标识, `[M]`, `[J]`,
   `EB/OL` = 0 occurrences each in both sidecars. The sweep command and its printed output are in the
   entry's `#### Unknown`, so the negative claim travels with its count.
4. **`citation-version-binding-r36.md`'s flip is only partly met**: it asks for "the issued and effective
   dates as a contiguous span"; the capture prints them as two adjacent lines (chars 1029, 1048). Stated in
   the entry rather than claimed as a clean flip.
5. **Two quotes cannot be used as unique strings** and are not quoted: `GB/T 7714-2015` (count 2 in the
   record), `GB/T 7714-2025` (count 2 in each form), 国家标准委 (count 2 in the portal). The entry quotes
   `（全部代替）` instead and states the counts.
6. **Known limit of the draft**: the five Inference bullets are lexical-checked, not entailment-checked; the
   tier statement ("type and tier are different axes") is the lane's inference and is labelled as such,
   with its quotes, not as a page's claim.

VERDICT: built the r36 entry draft (S121 SAMR record + S122 openstd notice, `ISO 690:2021` grounded at char 1797, 12 unique located quotes, 5 cited Inference bullets) and attacked it with the lane bar — `inference-ground` PASS 6/6, `quote-substance-check` 0 failures, build-spans 12/12 — while narrowing the staged headline, type enumeration and stale tier remark; entry not landed, counter not run.
