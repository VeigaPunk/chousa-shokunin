
# What a Chinese citation count actually counts

source: S100 — https://www.zcmu.edu.cn/__local/2/33/FC/FFA702D0F9381C8224BD74CB435_0E777725_C3A00.doc?e=.doc — the 他引频次 query note and 关于自引的说明 (OLE .doc; read as the UTF-16LE text of the raw capture) — capture 2026-10-23, re-opened 2026-10-25
source: S101 — https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc — sections 11 and 14 (OLE .doc; UTF-16LE text of the raw capture) — capture 2026-10-23, re-opened 2026-10-25
source: S102 — https://www.toho-shoten.co.jp/export/sites/default/cnki/help/cnki-kns80.pdf — sections 5.6.1 and 6.4 — capture 2026-10-23, re-opened 2026-10-25
source: S103 — https://library.um.edu.mo/upload/databases/c1b0fa89e2809581b12c79b9c60ea1af.pdf — section 2.1 and the result-ordering note — capture 2026-10-23, re-opened 2026-10-25
verified-at: 2026-10-25
recheck: 180d
ground: source hierarchy — what an index's counter is a count of; every source here is a copy or a third-party guide (no CNKI first-party page was opened), so the rows are scoped to "as these copies state"
adopted: round 49 from the campaign package `merge/chousa/`, re-bound by document to S100–S103; the staged ground line pointed at a campaign-era id that names the lane's GNU sed manual row, and is re-pointed by document to the CiNii row S096 of `corpus/knowledge/aggregator-vs-source-r36.md` (map in `corpus/lessons/round-49.md` `## Gate`)

#### Observation

- **A self-citation rule based on co-authorship (Chinese, copy hosted by a
  university).** The CNKI note says "中国知网他引频次的查询需要使用《中国引文数据库》。"
  and, under its self-citation heading,
  "关于自引的说明：对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被认定为自引。"
  — a citation in which any co-author appears is counted as a self-citation.
  Its query steps add "被引频次为0的文献将不会显示": records cited zero times are
  not listed (S100).
- **The data specification under the counts (Chinese, copy hosted by a
  university).** It assigns each article a 文献标志码 —
  "每一篇文章或资料应根据其内容性质标识一个文献标志码" — whose stated purpose
  begins "为便于文献的统计和期刊评价"; its reference elements include
  "文献类型及载体类型标志"; and for reference format it says
  "本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。"
  (it recommends, rather than defers to, the GB/T 7714 formats; a later
  parameter table reads "参考文献格式，参照ISO 690") (S101).
- **A third-party guide to the CNKI interface (Japanese).** The KNS8.0 guide
  glosses the result-list columns "「发表时间」「被引」「下载」" as
  "「下载」はそれぞれ文献の公開時期、被引用回数、ダウンロード回数を示します。", and
  describes the citation-network view as
  "当該文献を中心に年毎の参考、被引用の関係をビジュアルに提示" (S102).
- **A library guide to CNKI's AI answer mode (Chinese).** In trace mode
  "CNKI AI 根据相关文献，生成可信增强回答。"; the traced-source panel shows
  fields including "来源数据库" and "引用量", and results can be ordered by
  "相关度、发表时间、被引次数和下载量" (S103).

#### Inference

- A citation number must be scoped to the index that produced it and that
  index's stated counting rule. The CNKI copy counts as self-citation any
  reference sharing a co-author (`关于自引的说明：对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被认定为自引。`,
  S100), while CiNii says its list is matched items only (S096:
  `CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずしも一致していません`).
  Two indexes give two different reasons why an inbound number is not the
  paper's own number; a lane record names the index and its rule beside each
  count.
- A displayed zero, or a missing row, in an index query is a display-conditioned
  result: S100 says `被引频次为0的文献将不会显示`. Like CiNii's matched-item list
  (S096: `CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずしも一致していません`),
  an index's empty result is evidence about the index, and a search of the
  sources themselves is needed before a claim that nothing cites a work.
- A traced source and a counter are separate evidence objects. S103's trace
  mode says `CNKI AI 根据相关文献，生成可信增强回答。` and shows `来源数据库`
  beside `引用量`; S102 glosses citation and download counts as separate columns.
  A shown source is a lead to open, and a download count carries no claim of
  dependence: neither replaces reading the cited document.
- Selection is a separate question from matching. S101 sets a per-article code
  for statistics and evaluation (`为便于文献的统计和期刊评价`) and recommends a
  reference format (`本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。`);
  which records are eligible to be counted and how a reference string is
  matched are two decisions a count inherits, and these copies show neither
  decision as CNKI implements it.

#### Unknown

- Whether the copy's self-citation rule is current, and whether 被引 counts
  records in 中国引文数据库 or across CNKI as a whole: S100 is a university-hosted
  copy and states only that the query uses that database.
- Whether the specification copy (S101) is the version in force, and whether
  the counted records in S100 or S102 apply its codes.
- CNKI's own first-party statement of how its reference lists and cited-by
  lists are derived: no CNKI page was opened, so the CiNii admission (S096)
  is not transferred to CNKI.
- The staged entry's ISO-versus-GB/T reading: the register quote that put
  "GB/T 7714" into the parameter-table sentence is absent as written; the
  capture says ISO 690 there and GB/T 7714 in section 14.
