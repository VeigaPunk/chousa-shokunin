# R55GroundGcpA — S130 → lane S124 grounding

## Scope and provenance

Grounding pass for staged S130, the NMPA guideline copy hosted at `http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc`, against the staged entry `corpus/knowledge/grey-literature-and-chinese-search-record-r40.md` (staged package path: `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/grey-literature-and-chinese-search-record-r40.md`). Lane id under the frozen claims is S124. No source fetch or network access was used. The capture was read from `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d9c01d.raw`.

Defined-form command and observed result:

```sh
cd /fast/scratch/hyaku/chousa-r55/R55GroundGcpA && export TMPDIR=$PWD PYTHONDONTWRITEBYTECODE=1 && python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d.raw > $PWD/form.txt 2> $PWD/form.err; echo "exit=$?"; wc -l -c $PWD/form.txt
```

```text
exit=0
  865 34234 /fast/scratch/hyaku/chousa-r55/R55GroundGcpA/form.txt
```

Capture digest command/result:

```sh
sha256sum /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d9c01d.raw
ac0fad62ed9a11fa3bd135e78427329be30899df90946de7ac45e153974e6c44  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d9c01d.raw
```

The sidecar is not a usable form: UTF-8-with-replacement read of `bdff491a75c6abeda1d9c01d.txt` produced counts `是否检索灰色文献=0`, `灰色文献=0`, `检索策略=0`, `会议论文=0`. A UTF-16LE decode of the raw does contain the phrases, but its offsets are not offsets in the defined form (e.g. first quote below: defined-form offset 4623; UTF-16LE-decode offset 57442). The defined form is the `capture-text.py` stdout above, not either alternate decoding.

## Located quotes

Offsets are Python `form.find(quote)` character offsets in the complete defined form. The following exact quotes each occur once (`form.count(quote)=1`), and are each on one form line: Q1/Q2 line 53; Q3 line 15; Q4/Q5/Q6 line 16. All are under 160 characters and below 25 whitespace-separated words.

```text
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	2.文献检索策略：检索途径、检索数据库、检索时限及检索式。	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	应当说明是否有检索限制（如语言限制）、是否手工检索、是否检索灰色文献等关键问题。	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	检索策略包括检索的数据库、检索范围（如主题等）、检索词、检索式（即检索词组合方式）和时间范围等	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	查找时应当注意收集未公开发表的文献，即“灰色文献”，如会议论文、未发表的学位论文、产业报告、咨询报告等。	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	灰色文献中可能包含阴性研究结果，这些结果在通常情况下公开发表的机会较小，若文献评价中只纳入已公开发表的文献会引入发表偏倚。	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
QUOTE	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	数据资料包括常用数据库、专业数据库、政府网站、会议摘要、学术论文集以及其他未公开发表的文献等	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
```

Observed `(count, offset, form-line)` for these six, in order: `(1,4623,53)`, `(1,4652,53)`, `(1,761,15)`, `(1,994,16)`, `(1,1046,16)`, `(1,871,16)`. The first five directly ground the five requested S130 topics; Q6 additionally grounds the guideline's broader data-source statement.

## Sentence-level comparison and narrower wording

- Observation, first bullet, report-field sentence: reproduced by Q1 and Q2. The text explicitly lists `检索途径、检索数据库、检索时限及检索式` and says the report should state limits (including language limits), hand searching, and whether grey literature was searched.
- Observation, first bullet, protocol sentence: reproduced by Q3. Narrow wording: the protocol's search scope is `检索范围（如主题等）` (“search scope, e.g. topic”), not an unqualified specification of every possible scope dimension.
- Observation, first bullet, unpublished-material/publication-bias sentence: reproduced by Q4 and Q5. For the collection verb, the narrow translation is “reviewers should pay attention to collecting” (`应当注意收集`); the guideline says grey literature may contain negative results, which are less likely to be published, and evaluating only published literature introduces publication bias.
- Inference, first bullet (“required item of the report” and stated publication-bias reason): supported by Q2 and Q5. The report-writing section uses `应当说明`; avoid strengthening this to an unquoted `必须`.
- Inference, second bullet, the NMPA clause about hand searching and grey literature: supported by Q2. The adjacent comparative claims about Japanese practice, PRISMA-S, and its translation are not established by S130 and must remain grounded in their cited documents.
- Staged `recheck:` clause's `是否检索灰色文献等关键问题` is present once, at offset 4678. Its separate `五个方面` wording is absent from the defined form: `form.count('五个方面') = 0`; attribute that point to S131 (the Chinese Food and Drug News report), not S130. `paymentAmount=10` likewise is not an S130 claim.
- The staged unknown stating that the .doc could not be reread by literal grep is a method caveat, not a document proposition; narrow it to: “the source is an OLE container; the quoted text was read from the defined `capture-text.py` form, not the UTF-8-decoded `.txt` sidecar.”
- Locator precision: the report-field quote is under `三、报告撰写规范` → `(二)方法` → `2.文献检索策略`; including `(二)方法` makes the locator complete.
- Staged source-id defect: the staged entry cites the MedSci item as S133. Lane registry `corpus/SOURCES.md` has that item as S113 (round 52, row at line 123); the lane entry must cite `source: S113 — https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3`, never staged id S133. The S124/S125/S126 target entry and `spans.tsv` were absent from the lane tree when checked; this is grounding evidence only, not a C2 counter run.

## Evidence limits / gates

The staged SOURCES.append.md row S130 (line 55) describes the same guideline sections and decoded local `.doc` capture. This pass establishes the requested source text and its offsets; it did not run `c2-count.py`, `quote-substance-check.py`, `inference-ground.py`, any builder, or any C1/C3 gate, and makes no pass claim for those gates. No tool was installed. Scratch was confined to `/fast/scratch/hyaku/chousa-r55/R55GroundGcpA` and removed before finishing. Only this seat report is written.

VERDICT: Grounded the S130 → S124 NMPA search-record claims with six unique defined-form quotes; flagged S133→S113, the unsupported-by-S130 `五个方面` phrase, and wording/locator qualifications; no C2 gate was run.
