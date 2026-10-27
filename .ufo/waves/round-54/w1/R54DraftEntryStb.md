# R54DraftEntryStb — r37 entry draft (GB/T 7714-2025: the journal-office PDF, and the HIT data specification beside it)

Lane: chousa-shokunin. Scope: draft ONE entry, `corpus/knowledge/source-type-taxonomy-r37.md`, from the staged
`/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/source-type-taxonomy-r37.md`. The frozen
C2 predicate, its counter, the registry rows and the lesson are untouched; no production file, git/jj state or
sibling lane was written; no network and no live fetch (L0 `8d77e6c1` open) — every source is an on-disk
`.qcache` capture. No subagent dispatched (leaf seat). No tool installed or upgraded this round. Entry not
landed (the lane entry file is the L1's write, not mine); the counter was not run (see `## Not run`).

## What the draft does

- **Two documents, two planned lane ids, one provenance trio.** `S123` = the JMU PDF
  (`https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf`, text form = the
  capture sidecar `.qcache/0f33243fd7ac2fe88b85c1ba.txt`, 83,061 characters). `S101` = the HIT `.doc`
  (`https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc`,
  text form = the raw UTF-16LE decode of `.qcache/6dc68fd6b32ce9c8dfcebce8.raw`, the form the lane's S101 span
  rows slice; `tools/capture-text.py` prints the same text as 47,356 bytes / 27,012 characters, at different
  offsets). Then `verified-at: 2026-10-26`, a `recheck:` with a runnable command, `ground:`, `adopted:`, and
  Observation (7 bullets) / Inference (9) / Unknown (6).
- **Holds the C2 NEW_GROUND term in a located quote.** `文献载体标识` sits inside the 7.3 sentence at char
  11542 (42 characters, one line, count 1) — the same string the row seat anchors as `char 11542`. Correction
  sent to the row seat: my first note said the bare term occurs 23 times; the measured count is 32
  (`[32, 0, 0]` sweep below). The conclusion is unchanged — a bare term is not a locator, the sentence is.
- **Decides S101 in favour of citing it, narrowly.** The staged entry used the HIT specification for its nine
  reference elements and its 参照GB/T 7714/ISO 690 clauses; `corpus/knowledge/citation-count-semantics-r37.md`
  already holds both, so re-citing them would duplicate that holding. What this entry cites S101 for is the one
  thing that entry does not hold: the specification's own carrier alphabet (14.3.4 four two-letter codes,
  15.5 a one-letter GB 3469 code `P`/`M`) beside the 2025 standard's five-row table, including the collision
  where `M` is 普通图书 in both type tables and 缩微制品 in the older carrier code. Consequence for the L1:
  **row S101's `used-by` must gain `corpus/knowledge/source-type-taxonomy-r37.md`.** The source line is byte-exact
  `source: S101 — <its url> — …`; the row seat `R54DraftRows` has this in writing from me. If the L1 prefers no
  held-document citation, dropping the four S101 quotes and Inference bullets 1–4 leaves a coherent single-document
  entry — but the carrier-alphabet collision, which is the entry's sharpest finding, goes with them.
- **Narrows from the staged text, with the reason in `#### Unknown`.** (1) The staged 7.3 quote crossed a line
  break (`…也应著录文` / `献载体标识。`); the entry quotes the sentence up to the break. (2) The staged entry said
  the change list replaced 图书 where the copy reads 普通图书. (3) It cited S101 for "sections 11 and 14"; the
  carrier rules read here are 14.3.1, 14.3.4 and 15.5. (4) It read 附录Ａ's codes without recording that 附录Ａ is
  规范性 and 附录Ｂ 资料性 — the entry adds that the code alphabet is normative and the formats illustrative.
- **Adds what the two prior entries do not hold** (stated on the `ground:` line). `citation-count-semantics-r37.md`
  names GB/T 7714 only as the format a university-hosted data specification defers to (its 14.1/14.4, beside ISO
  690); `citation-version-binding-r36.md` binds a citation to a prior state with no PRC standard at all. Neither
  holds the standard's scope clause, its code appendices and their normative/informative status, its change list,
  its issue and effective dates, or the second carrier alphabet this entry sets beside it. This entry also refuses
  the staged document's own framing: the PDF is a journal office's reproduction of the print (tier B), and the
  entry says so in its source line, its first Observation bullet, its `ground:` line and its `#### Unknown`.

## Gates run (observed output, scratch root)

```
$ python3 tools/capture-text.py .../.qcache/6dc68fd6b32ce9c8dfcebce8.raw > $S/hit.txt ; echo exit=$?
exit=0                      # 47356 bytes, 27012 characters
$ python3 tools/capture-text.py .../.qcache/0f33243fd7ac2fe88b85c1ba.raw ; echo exit=$?
REFUSED neither a zip package nor an OLE compound file (a Word capture is one of them)
exit=2                      # so the PDF's text form is its .txt sidecar (build-spans `form_texts` reads .txt first)
$ python3 corpus/evidence/round54/build-spans.py --root $S/fakeroot --cache .../.qcache
QUOTE S123 char 5576 spans/S123-1.txt      … (25 rows, offsets as the entry states)
SPANS_ROWS=25 WRITTEN=25
$ … build-spans.py --root $S/fakeroot --cache .../.qcache --check
SPANS_ROWS=25 STALE=0
$ python3 corpus/evidence/round51/quote-substance-check.py $S/fakeroot/corpus/evidence/round54/spans.tsv
IDS=2 QUOTES=25 FAILURES=0
$ python3 tools/inference-ground.py --entry $S/entry_wrapped.md --spans $S/fakeroot/corpus/evidence/round54/spans.tsv --counts /dev/null --registry corpus/SOURCES.md
GROUND entry=entry_wrapped.md section=1 bullets=9 tokens=16 grounded=16
GROUND: PASS
$ python3 -c "import re;e=open('$S/entry_wrapped.md',encoding='utf-8').read();print(sorted(set(re.findall(r'S[0-9]{3,}',e))),e.count('文献载体标识'))"
['S101', 'S123'] 11          # 11 = 9 in the body + 2 inside the `recheck:` command, which names the term
```

- Every quote was extracted by offset from its form, not retyped (`build.py` asserts `count==1` and no CR/LF
  inside the slice for all 25, then `build-spans.py` accepted all 25 at the offsets the entry states).
- `inference-ground` bit twice before it passed, and the fixes are in the draft: a too-short backtick pair
  (`Ｍ`) swallowed the next backticked quote as `as well (`, a bullet quoted S101 without citing it, and the
  OCR bullet ended `char 21382` (a bare figure with no counts key). Fixed: fullwidth letters unbackticked, the
  bullet now cites `(S101, S123)`, the offset moved to Observation. First run: `GROUND: FAIL`, exit 1; final:
  `GROUND: PASS`, exit 0.
- Negative sweeps, run verbatim from the entry's `#### Unknown` (`[32, 0, 0]` on S123's form, `[0, 1, 4, 3]` on
  S101's) and reproduced in this report's gate block. The `文献载体标识` = 0 leg is what makes the two instruments
  distinct vocabularies for one axis; the `3469` = 0 leg is what makes the "does not inherit the older code
  standard" claim checkable. The entry's third claim there — that the older copy has no carrier *table* — is
  backed by reading every line of its form that says 载体: `grep -n 载体 $S/hit.txt` → 14 lines, all prose
  (7, 70, 71, 78, 125, 131, 245, 260, 261, 268, 303, 309, 398, 404), none a table.

## Not run, and out of scope

- **`corpus/evidence/round54/c2-count.py` was not run.** It reads the lane tree at `corpus/knowledge/…`, where
  this entry does not exist (my only write is this report). The L1 lands the entry, then runs the counter.
- **The lesson half of the C2 substance leg is not mine**: "each quote … inside the round-54 lesson" and the
  three absent-defect-register verdicts (`S080`, `S088`, `S096`) belong to the lesson seats. I verified the
  span-side, entry-side and quote-side legs with lane tools in scratch; the lesson leg is unverified here.
- **`--counts /dev/null`**: my Inference carries no figure needing a counts key, so the real round-54 counts
  manifest cannot change this entry's grounding. The `21382` figure lives in Observation, where the tool does
  not read.
- **Fidelity of the reproduction to the issued text is untested** and is recorded as Unknown in the entry: no
  entitled copy, authority portal or bookshop text was opened, and no fetch was made.

## Entry — `corpus/knowledge/source-type-taxonomy-r37.md`

```markdown
# A carrier code belongs to the instrument that issued it: the Chinese bibliographic standard's 文献载体标识 table, and the older data specification's carrier alphabet beside it

source: S101 — https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc — 中国学术期刊（光盘版）检索与评价数据规范（修订本）: sections 14.3.1 (文献类型标志), 14.3.4 (电子文献的载体类型及其标志) and 15.5 (文献载体代码) — char 12392, char 12682 and char 34265, in the raw UTF-16LE text form of the capture `.qcache/6dc68fd6b32ce9c8dfcebce8.raw` (the form this lane's S101 span rows slice)
source: S123 — https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf — ＧＢ／Ｔ ７７１４—２０２５ 信息与文献 参考文献著录规则, a journal office's reproduction of the printed edition (tier B, not the authority's own text): 第１章 范围 (char 5576, char 5602), 第６章 著录用符号 (char 8881), ７．３ (char 11542), ７．６ (char 14096), 前 言 change list item ｏ） (char 4736, char 4812, char 4852), ８．３．２ (char 21382), 附录Ａ (char 2512, char 57965, char 58840, char 59201), 附录Ｂ (char 2655), and the colophon (char 82465, char 82834); text form = the capture's `.txt` sidecar `0f33243fd7ac2fe88b85c1ba.txt`, 83,061 characters
verified-at: 2026-10-26
recheck: 180d — from the lane root, `python3 -c "t=open('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0f33243fd7ac2fe88b85c1ba.txt',encoding='utf-8').read(); print(t.find('文献类型标识、文献载体标识应按照附录Ａ著录。'), t.count('文献载体标识'))"` prints `11542 32`; then `python3 -c "b=open('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/6dc68fd6b32ce9c8dfcebce8.raw','rb').read().decode('utf-16-le','replace'); print(b.find('15.5文献载体代码'))"` prints `34265`; re-download both documents and confirm 表Ａ．２ still carries five carrier codes and 15.5 still defers its one-letter codes to GB 3469
ground: what a carrier designation in a Chinese reference string is a designation *of*, read from the two instruments' own tables. The lane's `corpus/knowledge/citation-count-semantics-r37.md` names GB/T 7714 only as the format another instrument defers to (its 14.1 and 14.4, beside ISO 690), and `corpus/knowledge/citation-version-binding-r36.md` binds a citation to a prior state without any PRC standard; neither holds the standard's scope clause, its code appendices, its change list, its issue and effective dates, or the second carrier alphabet this entry sets beside it. The copy read here is a journal office's reproduction of the print (tier B); it is not the issued text and nothing below is quoted as the authority's own typography
adopted: round 54 from the campaign package merge/chousa/ (staged knowledge/corpus/knowledge/source-type-taxonomy-r37.md; its GB/T half re-bound by document to the new lane row S123, its data-specification half to the lane row S101, and the staged body reused only where the text form supports it)

#### Observation

- **What the reproduction is, on its own face.** The title page carries the standard's number and title,
  `２０２５－１２－０２发布` beside `２０２６－０７－０１实施`, and the preface sentence `本文件代替ＧＢ／Ｔ ７７１４—２０１５《信息与文献 参考文献著录规则》`; the
  closing pages carry the publisher's colophon `中国标准出版社出版发行` and `２０２５年１２月第１版 ２０２５年１２月第１次印刷`. The file is
  therefore a journal office's reproduction of the printed edition, and it is an OCR of it: the 8.3.2 template
  reads `图书主要贵任者` (贵 for 责) at char 21382, while 主要责任者 occurs 31 times in the same text form (S123).
- **Scope.** 第１章 states the standard's own applicability and then its limit: `本文件适用于作者和编制者著录参考文献。` —
  followed by `本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。`. The standard governs the author and the compiler of a
  reference list, and disclaims the librarian, the catalogue compiler and the indexer (S123).
- **The carrier designation is normative text, placed after a slash.** ７．３ reads
  `文献类型标识、文献载体标识应按照附录Ａ著录。电子资源既应著录文献类型标识，也应著录文` (the sentence continues 献载体标识。 on the following line of the
  text form), 第６章 puts the carrier after the slash: `“／”用于合期的期号或合卷的卷号间（见８．５．１．２）、文献载体标识前。`, and the code
  appendix is marked normative while the worked examples are not — `附录Ａ（规范性） 文献类型和文献载体标识代码` against `附录Ｂ（资料性）`
  (S123).
- **The carrier table has five rows and the microform row is new.** Ａ．２ says `电子资源载体和标识代码应按照表Ａ．２著录。` and its
  rows are 磁带 MT, 磁盘 DK, 光盘 CD, 联机网络 OL and `缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）` MM; the preface's change list records
  that last one as an addition (`增加了电子资源载体“缩微资料”及其标识代码`), and the type table beside it gives 图书 the code in
  the row `图书                          Ｍ` (S123).
- **The date rule.** ７．６ reads `电子资源的创建日期、发布日期、修改日期、引用日期应按照“ＹＹＹＹ－ＭＭ－ＤＤ”格式，用阿拉伯数字` (S123).
- **The older specification's own alphabet.** Its 14.3.4 lists four carrier codes in pair notation —
  `磁带(magnetic tape)——MT，磁盘(disk)——DK，光盘(CD-ROM)——CD，联机网络(online)——OL` — and its 14.3.1 assigns document-type
  letters `文献类型标志 M C N J D R S P G K`; separately 15.5 fixes a one-letter carrier code:
  `15.5文献载体代码，根据GB 3469规定，采用1位字母：P——印刷本，M——缩微制品`. That copy uses neither the term 文献载体标识 nor a table like
  表Ａ．２: the term occurs 0 times in it, 文献载体代码 once and 载体类型标志 4 times (S101).

#### Inference

- **The two instruments give one medium two codes.** The standard's change list records the microform
  carrier as a new **code** (`增加了电子资源载体“缩微资料”及其标识代码`, S123), while the older specification fixes the same
  medium under a one-letter code (`15.5文献载体代码，根据GB 3469规定，采用1位字母：P——印刷本，M——缩微制品`, S101). A row that copies a
  carrier code without its instrument and its table can hold ＭＭ and Ｍ for one medium, and neither row would
  look wrong.
- **The letter M is a type code in both instruments and a carrier code in one.** The older specification's
  type row assigns `文献类型标志 M C N J D R S P G K` to its document types, M for 普通图书, and its carrier rule then
  gives M to 缩微制品; the standard's type table gives 图书 the code Ｍ as well (`图书                          Ｍ`) in
  the same slot (S101, S123). An unqualified M names an axis only when the reader knows which table is in
  force, so a lane row quotes the table, not the letter.
- **The shared carrier letters are continuity of code, not of instrument.** The older specification's list
  `磁带(magnetic tape)——MT，磁盘(disk)——DK，光盘(CD-ROM)——CD，联机网络(online)——OL` (S101) and the standard's five-row
  table carry the same four letters, so a carrier code read from an older Chinese reference still resolves in
  the current table — while the type letters beside them do not, because the standard renames and repurposes
  types: `将文献类型“普通图书”“舆图”分别更改为“图书”“地图”` and `将“ＥＢ”代表的文献类型更改为“网站、网页”` (S123).
- **The standard defines its codes itself and does not inherit the older code standard.** The older
  specification opens its type rule with `14.3.1根据 GB 3469规定，以单字母方式标识以下各种参考文献类型` (S101); the standard's
  normative references are two documents, among them `ＧＢ／Ｔ ４８９４ 信息与文献 基础和术语` (S123), and the older code
  standard's number occurs 0 times in the standard's text form (sweep in `#### Unknown`). A reference written
  to 表Ａ．２ rests on that table, not on the earlier instrument's deferral.
- **The scope clause separates writing a reference from counting citations.** The standard says
  `本文件适用于作者和编制者著录参考文献。` and `本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。` (S123), so a row that cites it as authority
  for what an index counts, or for how a reference list is matched, cites a document that disclaims that work:
  it answers what to write, and says nothing about what a count is a count of.
- **A normative code table and an informative example table are different evidence.** The standard marks
  `附录Ａ（规范性） 文献类型和文献载体标识代码` as its normative appendix and `附录Ｂ（资料性）` as its informative one (S123), so a
  reference string copied from an example shows a form the standard illustrates, while the letters in it are
  prescribed only through the normative table. A lane row that quotes an example as the rule reads the
  appendix's status wrong.
- **A carrier code describes storage, not access.** An electronic resource is defined as
  `以数字方式将图、文、声、像等信息存储在磁、光、电介质上` (S123), and the carrier table runs from tape and disk through optical disc and
  the online network to `缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）`; the list is a storage-medium list with one networked
  entry, so a carrier code alone carries no claim about how a lane read the document it cites.
- **The copy dates itself and binds a predecessor, so a citation needs its year.** The reproduction carries
  `２０２５－１２－０２发布` beside `２０２６－０７－０１实施` and the preface sentence `本文件代替ＧＢ／Ｔ ７７１４—２０１５《信息与文献 参考文献著录规则》` (S123).
  A citation that gives the standard's number without its year cannot be told from one written under the
  replaced edition, and the change list is exactly what that year decides.
- **A reproduced page is evidence of its words, not of the authority's typography.** `图书主要贵任者` stands in the
  standard's own 8.3.2 template (S123), where 责 is meant. This entry quotes words and treats the fullwidth
  Latin and the occasional wrong glyph as the reproduction's: a re-checker must match the letter, and a code
  letter read from a reproduction is weaker evidence than one read from an entitled copy.

#### Unknown

- **Negative sweeps, with counts.** `文献载体标识` occurs 32 times in S123's text form and **0** times in S101's: `python3 -c "t=open('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0f33243fd7ac2fe88b85c1ba.txt',encoding='utf-8').read(); print([t.count(w) for w in ('文献载体标识','3469','ＩＳＯ ６９０')])"` prints `[32, 0, 0]`, and `python3 -c "b=open('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/6dc68fd6b32ce9c8dfcebce8.raw','rb').read().decode('utf-16-le','replace'); print([b.count(w) for w in ('文献载体标识','文献载体代码','载体类型标志','3469')])"` prints `[0, 1, 4, 3]`. So the older copy has the axis under other names, and the standard never names the older code standard or ISO 690: its one abbreviation rule names ISO 4 for Western serial titles, and 参考文献 example [2] cites ISO 4:1997.
- **Whether the reproduction's operative clauses match the issued text.** No entitled copy, authority portal or bookshop text was opened this round and no fetch was made; the reproduction carries the publisher's colophon, but a colophon is not a collision with the issued pages, and OCR can lose or alter a glyph.
- **Whether the standard's issue and effective dates are what the authority records.** A record page is the other entry's document (`corpus/knowledge/source-type-taxonomy-r36.md`); this entry does not treat a record page as proof of the text, and a record's dates are the record's fields.
- **Whether any publisher, journal or index applies 表Ａ．２'s codes.** No publisher page or index guide was read; the standard prescribes, and whether a given reference list obeys was not established.
- **Which edition of the older code standard S101 means.** Its 15.5 names that standard without a year, and S101's own text does not date it, so the one-letter carrier code it fixes is unpinned to an edition.
- **Staged material corrected on adoption.** The staged entry quoted ７．３ across a line break (`…也应著录文` / `献载体标识。`), named the replaced type as 图书 where the copy reads `将文献类型“普通图书”“舆图”分别更改为“图书”“地图”`, cited the data specification for "sections 11 and 14" where the carrier rules read here are 14.3.1, 14.3.4 and 15.5, and read 附录Ａ's type codes without recording that the appendix is normative and 附录Ｂ informative. Those four are corrected or dropped here.
```

## QUOTE machine lines (one per line; staged-id = the planned lane id)

```
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	本文件适用于作者和编制者著录参考文献。	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	文献类型标识、文献载体标识应按照附录Ａ著录。电子资源既应著录文献类型标识，也应著录文	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	电子资源的创建日期、发布日期、修改日期、引用日期应按照“ＹＹＹＹ－ＭＭ－ＤＤ”格式，用阿拉伯数字	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	增加了电子资源载体“缩微资料”及其标识代码	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	将文献类型“普通图书”“舆图”分别更改为“图书”“地图”	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	将“ＥＢ”代表的文献类型更改为“网站、网页”	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	图书主要贵任者	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	中国标准出版社出版发行	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	２０２５年１２月第１版 ２０２５年１２月第１次印刷	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	本文件代替ＧＢ／Ｔ ７７１４—２０１５《信息与文献 参考文献著录规则》	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	２０２５－１２－０２发布	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	２０２６－０７－０１实施	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	ＧＢ／Ｔ ４８９４ 信息与文献 基础和术语	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	附录Ａ（规范性） 文献类型和文献载体标识代码	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	附录Ｂ（资料性）	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	电子资源载体和标识代码应按照表Ａ．２著录。	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	图书                          Ｍ	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	“／”用于合期的期号或合卷的卷号间（见８．５．１．２）、文献载体标识前。	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S123	https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf	以数字方式将图、文、声、像等信息存储在磁、光、电介质上	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S101	https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc	14.3.1根据 GB 3469规定，以单字母方式标识以下各种参考文献类型	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S101	https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc	文献类型标志 M C N J D R S P G K	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S101	https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc	磁带(magnetic tape)——MT，磁盘(disk)——DK，光盘(CD-ROM)——CD，联机网络(online)——OL	corpus/knowledge/source-type-taxonomy-r37.md
QUOTE	S101	https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc	15.5文献载体代码，根据GB 3469规定，采用1位字母：P——印刷本，M——缩微制品	corpus/knowledge/source-type-taxonomy-r37.md
```

VERDICT: built the r37 entry draft — the JMU journal-office PDF as S123 with 21 located quotes and the HIT data specification as S101 with 4, `文献载体标识` grounded at char 11542, 9 Inference bullets each citing an S-id and a verbatim phrase — and attacked it with the lane bar: `build-spans` 25/25 at the stated offsets (`--check` STALE=0), `quote-substance-check` 0 failures, `inference-ground` GROUND PASS 16/16, S-tokens `['S101','S123']` only; entry not landed and the counter not run, with S101's `used-by` flagged for the L1.
