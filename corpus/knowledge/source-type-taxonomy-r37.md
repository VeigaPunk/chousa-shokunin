# A carrier code is prescribed by a normative table: the Chinese bibliographic standard's 文献载体标识, its scope clause and its change list, read from a journal office's reproduction

source: S123 — https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf — ＧＢ／Ｔ ７７１４—２０２５ 信息与文献 参考文献著录规则, a journal office's reproduction of the printed edition (tier B, not the authority's own text): 第１章 范围 (char 5576, char 5602), 第６章 著录用符号 (char 8881), ７．３ (char 11542), ７．６ (char 14096), 前 言 change list item ｏ） (char 4736, char 4812, char 4852), ８．３．２ (char 21382), 附录Ａ (char 2512, char 57965, char 58840, char 59201), 附录Ｂ (char 2655), and the colophon (char 82465, char 82834); text form = the capture's `.txt` sidecar `0f33243fd7ac2fe88b85c1ba.txt`, 83,061 characters
verified-at: 2026-10-26
recheck: 180d — from the lane root, `python3 -c "t=open('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0f33243fd7ac2fe88b85c1ba.txt',encoding='utf-8').read(); print(t.find('文献类型标识、文献载体标识应按照附录Ａ著录。'), t.count('文献载体标识'))"` prints `11542 32`; re-download the document and confirm 表Ａ．２ still carries five carrier codes and 第１章 still disclaims the librarian, the catalogue compiler and the indexer
ground: what a carrier designation in a Chinese reference string is a designation *of*, and whose work the standard governs, read from the standard's own clauses. The lane's `corpus/knowledge/citation-count-semantics-r37.md` names GB/T 7714 only as the format another instrument defers to (its 14.1 and 14.4, beside ISO 690), and `corpus/knowledge/citation-version-binding-r36.md` binds a citation to a prior state without any PRC standard; neither holds the standard's scope clause, its code appendices and their normative/informative status, its change list or its date rule. The copy read here is a journal office's reproduction of the print (tier B); it is not the issued text and nothing below is quoted as the authority's own typography
adopted: round 54 from the campaign package merge/chousa/ (staged knowledge/corpus/knowledge/source-type-taxonomy-r37.md; its GB/T half re-bound by document to the new lane row S123; its data-specification half — the HIT data specification the lane already registers (its `corpus/SOURCES.md` row for the jc.hit.edu.cn `.doc`) — is not carried this round — see `#### Unknown`)

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

#### Inference

- **The type letters are renamed between editions, so a code read from an older Chinese reference is resolved through the edition it was written under.** The change list records `将文献类型“普通图书”“舆图”分别更改为“图书”“地图”` and `将“ＥＢ”代表的文献类型更改为“网站、网页”` (S123): the same letter can stand for a differently named type in the replaced and the current table, so a lane row quotes the table and its edition, not the letter alone.
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
- **The standard names its own normative references.** It lists `ＧＢ／Ｔ ４８９４ 信息与文献 基础和术语` among them, and the older Chinese code standard's number occurs 0 times in its text form (S123; the count is in `#### Unknown`): a reference written to 表Ａ．２ rests on that table.

#### Unknown

- **Negative sweeps, with counts.** `python3 -c "t=open('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0f33243fd7ac2fe88b85c1ba.txt',encoding='utf-8').read(); print([t.count(w) for w in ('文献载体标识','3469','ＩＳＯ ６９０','690')])"` prints `[32, 0, 0, 0]`: the reproduction names neither the older code standard nor ISO 690 (the adoption relation to ISO 690:2021 is the authority record's field, `corpus/knowledge/source-type-taxonomy-r36.md`, not this copy's).
- **Whether the reproduction's operative clauses match the issued text.** No entitled copy, authority portal or bookshop text was opened this round and no fetch was made; the reproduction carries the publisher's colophon, but a colophon is not a collation with the issued pages, and OCR can lose or alter a glyph. Two extractors also disagree on width: `pdftotext` renders `附录Ａ` and `ＹＹＹＹ－ＭＭ－ＤＤ` where an independent pypdf extraction renders half-width letters (round-54 W1 `R54DraftGateTable`), so the quotes are checked against the independent extraction under NFKC folding (`corpus/evidence/round54/pdf-crosscheck.py`).
- **Whether the standard's issue and effective dates are what the authority records.** A record page is the other entry's document (`corpus/knowledge/source-type-taxonomy-r36.md`); this entry does not treat a record page as proof of the text, and a record's dates are the record's fields.
- **Whether any publisher, journal or index applies 表Ａ．２'s codes.** No publisher page or index guide was read; the standard prescribes, and whether a given reference list obeys was not established.
- **The older data specification beside it (the lane's held HIT row) is not carried this round.** The staged entry also read the HIT data specification's carrier and type letters (its 14.3.1, 14.3.4 and 15.5), and W1 `R54DraftEntryStb` found a sharp contrast there (one medium, two codes; the letter M a type code in both instruments and a carrier code in one). Its only span form is a raw UTF-16LE decode of the `.doc`, the form round 54 found undefined (`corpus/lessons/round-54.md` `## Mistakes` row 2); the round-54 span builder has no OLE text form, so no new anchor on that row is written. Flip: a span builder that reads an OLE `.doc` through `tools/capture-text.py`, and the four data-specification quotes re-located in that form.
- **Staged material corrected on adoption.** The staged entry quoted ７．３ across a line break (`…也应著录文` / `献载体标识。`), named the replaced type as 图书 where the copy reads `将文献类型“普通图书”“舆图”分别更改为“图书”“地图”`, and read 附录Ａ's type codes without recording that the appendix is normative and 附录Ｂ informative. Those three are corrected here; its data-specification half is set aside (above).

#### Corrections (round 55)

Appended after round-54 wave 2 re-read the copy (`.ufo/waves/round-54/w2/R54W2CritEntailStb.md`); the bullets above stay as filed.

- **The scope inference's clause on matching is withdrawn.** The scope sentence itself ends `以及参考文献标引体系编制法。` (`S123`, char 5555), and the copy's chapter 9 sets out how citations in the text are tied to list entries (顺序编码制, 著者－出版年制), so the standard does govern how a reference list is matched to the text. What the scope clause excludes is the librarian, catalogue-compiler and indexer as users; the separation from counting stands, the matching clause does not.
- **The carrier inference's headline is too narrow.** The definition the bullet quotes covers storage media, but 表Ａ．２ also lists 联机网络（ｏｎｌｉｎｅ） with ＯＬ (char 59161), a network carrier; the bullet's body already concedes one networked entry. Read the headline as: a carrier code names the resource's medium, not the reader's access.
- **"Occasional" is one instance.** 贵 occurs three times in the copy's text form (chars 10679, 21386, 78811); only the one at 21386 is the wrong glyph, the others being a place name and a surname. A single confusable substitution fits a print typo as well as OCR, so the OCR attribution stays a possibility, as the Unknown section says.
