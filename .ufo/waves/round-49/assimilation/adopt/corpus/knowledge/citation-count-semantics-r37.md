
# What a Chinese citation count actually counts

source: S101 — https://www.zcmu.edu.cn/__local/2/33/FC/FFA702D0F9381C8224BD74CB435_0E777725_C3A00.doc?e=.doc — 关于自引的说明 and the 他引频次 query section — document read 2026-10-23
source: S102 — https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc — sections 11 and 14 — document read 2026-10-23
source: S103 — https://www.toho-shoten.co.jp/export/sites/default/cnki/help/cnki-kns80.pdf — sections 5.4, 5.6.1 and 6.4 — PDF read 2026-10-23
source: S104 — https://library.um.edu.mo/upload/databases/c1b0fa89e2809581b12c79b9c60ea1af.pdf — section 2.1 and the result-field list — PDF read 2026-10-23
verified-at: 2026-10-23
recheck: 180d — re-download all four and confirm the self-citation rule, the 被引字段 and the 溯源 field list are unchanged (ran 2026-10-23)
ground: wave-1 queue Q2 — CNKI's reference-list and cited-by semantics; the lane held no Chinese row against which its own tier rule could be checked, and wave 1 had established that a citation index's list is a derived artefact (S076)

#### Observation

- **CNKI states its own self-citation rule, and it is co-authorship-based.**
  The CNKI document titled 中国知网他引频次查询方法说明 says that "中国知网他引
  频次的查询需要使用中国引文数据库", and then, under 关于自引的说明:
  "对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被
  认定为自引." A citation by any co-author of the cited work is a self-citation.
- **The counted quantity is named and is not the raw inbound count.** CNKI's
  own guide describes the result list fields as "「发表时间」「被引」「下载」"
  giving respectively 公開時期, **被引用回数** and ダウンロード回数; 被引频次 is
  one of twenty searchable 专业检索 fields, and the 引文网络 view presents, for
  a given article, its yearly 参考 and 被引用 relations as a graph.
- **The data specification underneath the counts names what is being counted.**
  The Chinese journal data specification gives each reference nine prescribed
  elements including 文献类型及载体类型标志 and 文献出处或电子文献的可获得
  地址, and classifies each article by a 文献标志码 (A–E) whose stated purpose
  is "为便于文献的统计和期刊评价…确定文献的检索范围，提高检索结果的适用性".
  The reference format itself is deferred to GB/T 7714.
- **CNKI AI exposes the counters alongside the traced source.** Its 溯源 mode
  "根据相关文献，生成可信增强回答", and the traced-source panel shows each
  document's 标题, 摘要, 作者, 出版日期, 文献来源, **来源数据库, 引用量** and
  **下载量**; result lists can be ordered by 相关度, 发表时间, 被引次数 and
  下载量.

#### Inference

- **CNKI's boundary is co-authorship, and the lane must not assume it is
  authorship.** The rule as CNKI states it is *any* shared co-author, not
  *the* author. A lane that treats "self-citation" as "same author" would
  miscount against CNKI's own definition, and the same lane's rule applied
  against CiNii or Web of Science would be wrong in a *different* direction.
  This is the same lesson as wave 1's CiNii finding — the count is a property
  of the index's matching rules — but it is now demonstrated on the **other
  side** of the same trade: CNKI's rule is broader than authorship, while
  CiNii's count is a matched-item count rather than the paper's printed count.
  Two indexes, two different reasons why an inbound number is not an inbound
  number.
- **被引 and 下载量 are different quantities and the lane should keep them
  apart.** CNKI's own guide names them as separate result fields with
  separate meanings — citation count and download count — and CNKI AI's
  traced-source panel shows both. A download is an access event with no
  evidentiary content at all; a citation is a claimed dependency. Any lane
  metric that treats engagement and dependency as interchangeable would
  conflate them, and the Chinese interfaces make the conflation easy because
  the two counters sit side by side.
- **The 溯源 mode is the Chinese counterpart of the lane's own
  claim-vs-source move.** CNKI AI answers a question and then shows the
  documents it used, each with 来源数据库 and 引用量 — that is a
  claim-to-source trace with a per-source identifier. It is a product
  feature, not a standard, so it is tier B; but it shows that the Chinese
  literature has the *affordance* the lane is trying to specify, and it
  exposes 引用量 per source, which is the field a lane's chain check would
  want.
- **The specification makes the counting auditable in principle.** Nine
  prescribed reference elements, a document-type code, a carrier code and a
  resolvable address mean a citation record in this system has the parts a
  chain check needs — while the A–E 文献标志码 shows that the *selection* of
  what counts as a citable article is a separate, declared decision made for
  counting and evaluation purposes.

#### Unknown

- **CNKI's own documentation of 引用文献 and 被引量 was not reached.** Every
  source here is a copy or a third-party guide: CNKI's own site returned a
  381-byte shell to an automated fetch in wave 1 and again this round, and
  the 诚信档案系统使用手册 (which contains CNKI's 引文核对 citation-checking
  feature description) timed out and was never opened. The row set is
  therefore tier B throughout and is scoped to "as these copies state".
- Whether CNKI's 被引用回数 counts records in 中国引文数据库 or records across
  CNKI as a whole was **not** established.
- Whether the 文献标志码 scheme currently in force is the one in the copy read
  (the copy predates GB/T 7714-2025) is untested.
- No Chinese equivalent of CiNii Research's "your reference list is a derived
  subset of the paper's own list" admission was found; CNKI's own statement
  on that point is exactly what the blocked fetch would have supplied.

---
