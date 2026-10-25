# Draft: citation-count-semantics-r37.md

## Entry draft

```markdown
# What a Chinese citation count actually counts

source: S101 — https://www.zcmu.edu.cn/__local/2/33/FC/FFA702D0F9381C8224BD74CB435_0E777725_C3A00.doc?e=.doc — 关于自引的说明 and the 他引频次 query section — document read 2026-10-23
source: S102 — https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc — sections 11 and 14 — document read 2026-10-23
source: S103 — https://www.toho-shoten.co.jp/export/sites/default/cnki/help/cnki-kns80.pdf — sections 5.4, 5.6.1 and 6.4 — PDF read 2026-10-23
source: S104 — https://library.um.edu.mo/upload/databases/c1b0fa89e2809581b12c79b9c60ea1af.pdf — section 2.1 and the result-field list — PDF read 2026-10-23
verified-at: 2026-10-23
recheck: 180d — re-download all four and confirm the self-citation rule, the 被引字段 and the 溯源 field list are unchanged (ran 2026-10-23)
ground: wave-1 queue Q2 — CNKI's reference-list and cited-by semantics; the lane held no Chinese row against which its own tier rule could be checked, and wave 1 had established that a citation index's list is a derived artefact (S096)

#### Observation

- **CNKI's self-citation rule is co-authorship-based.** The CNKI document hosted by a university says a citation is classed as self-citation if any co-author appears in it: "任一合作者" (S101). Its query instructions also say that works with zero 被引 frequency are not displayed: "被引频次为0的文献将不会显示" (S101). These describe the document's stated rule and query display, not the correctness or completeness of an individual count.
- **A database specification describes record fields and selection codes, not an observed count's provenance.** The specification lists a reference type/carrier field, "文献类型及载体类型标志" (S102), and prescribes a 文献标志码 for articles or materials according to content: "每一篇文章或资料应根据其内容性质标识一个文献标志码" (S102). It says the code is for statistics, journal evaluation and setting retrieval scope: "为便于文献的统计和期刊评价" (S102). These are specification statements; they do not establish that a particular CNKI count applies those codes.
- **The publisher guide labels distinct CNKI result fields and a graph view.** It says 被引 frequency is one of "被引频次 20 項目" searchable fields (S103), translates the result-list value 被引 as "被引用回数" (S103), and describes the graph as showing "年毎の参考、被引用の関係" (S103). This is a third-party usage guide, not CNKI's own definition of the counter's database-wide scope.
- **The library guide describes a traceable-source interface, not validation of AI answers.** In the trace mode it says CNKI AI generates an enhanced answer based on related literature: "根据相关文献，生成可信增强回答" (S104). Its source display lists "文献来源、来源数据库" (S104) and the source-result ordering includes "相关度、发表时间、被引次数和下载量" (S104). This establishes that those fields and ordering are described in the guide; it does not establish that a cited source supports an answer or that the counter is accurate.

#### Inference

- **A citation number must be scoped to the index's documented matching and counting rules, not treated as a paper's printed bibliography count.** The lane's CiNii admission is specific: its note says "同定・統合された参考文献だけが表示されます" (S096) and that it counts "同定・統合された分をカウントしています" (S096). CNKI's sources here do not establish the same derived-list rule for CNKI. The defensible cross-document inference is methodological: name the index and its documented count definition for each number; do not transfer CiNii's mechanism to CNKI.
- **A source trace and a counter are separate evidence objects.** S104 names both "来源数据库" and a counter field, "引用量" (S104), while S103 separately describes 被引 and 下载 values. A displayed source/counter association is useful to inspect, but by itself does not establish that the cited document entails a generated statement or that citation and download counters measure the same event.
- **A zero displayed in a query is a display-conditioned result, not evidence that no citing work exists.** S101 says "被引频次为0的文献将不会显示" (S101). Therefore a reader cannot infer absence of citations from a result set that omits zero-frequency records; this is a limitation of interpreting that query, not a claim about the database's actual underlying records.
- **The specification's classification scheme makes selection a separate question from matching.** S102 states the code's purpose includes "为便于文献的统计和期刊评价" (S102), while its reference rules name "文献类型及载体类型标志" (S102). A count interpretation should ask separately what records are eligible and how a reference is matched; these excerpts do not show CNKI's operational implementation of either choice.

#### Unknown

- The CNKI-hosted university copy (S101) gives a self-citation rule and query procedure, but the captures do not establish whether the stated rule is current or how 他引频次 is computed across all products. It says the query uses 中国引文数据库; the actual result-generation internals were not documented in the read passage.
- S102 is a hosted copy of a revised data specification. The excerpt does not establish whether this version is currently in force or whether its fields and codes are used by the counted records described in S101 or S103.
- S103 is a third-party guide and S104 a library guide. Neither establishes CNKI's authoritative definition of the scope, matching, update cadence, or completeness of 被引/引用量. S104 describes a product interface, not an evaluation of answer quality.
- The reference-list derivation admission is grounded in the CiNii manual (S096), not a Chinese CNKI source. CNKI's equivalent reference-list/cited-by behavior remains unknown in these captures.

---
```

## Quote TSV

Every phrase below is used in an inference bullet. Each source phrase was checked against the corresponding capture text; counts are exact occurrence counts in that text form.

```tsv
id	url	quote	entry
S096	https://support.nii.ac.jp/ja/cir/manual_articles_detail	同定・統合された参考文献だけが表示されます	corpus/knowledge/citation-count-semantics-r37.md
S096	https://support.nii.ac.jp/ja/cir/manual_articles_detail	同定・統合された分をカウントしています	corpus/knowledge/citation-count-semantics-r37.md
S104	https://library.um.edu.mo/upload/databases/c1b0fa89e2809581b12c79b9c60ea1af.pdf	来源数据库	corpus/knowledge/citation-count-semantics-r37.md
S104	https://library.um.edu.mo/upload/databases/c1b0fa89e2809581b12c79b9c60ea1af.pdf	引用量	corpus/knowledge/citation-count-semantics-r37.md
S101	https://www.zcmu.edu.cn/__local/2/33/FC/FFA702D0F9381C8224BD74CB435_0E777725_C3A00.doc?e=.doc	被引频次为0的文献将不会显示	corpus/knowledge/citation-count-semantics-r37.md
S102	https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc	为便于文献的统计和期刊评价	corpus/knowledge/citation-count-semantics-r37.md
S102	https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc	文献类型及载体类型标志	corpus/knowledge/citation-count-semantics-r37.md
```

## Work/evidence record

- Scope: drafted only; no product code, lane entry, frozen claim, counter, or other seat report was edited. This report is the sole written artifact for this seat. No subagents, background jobs, network access, or live fetches were used.
- Read the staged entry and sibling entry, lane `corpus/QUALITY.md`, `tools/inference-ground.py`, the staged `append.md` and `renumber.tsv`, the S101/S102 `.doc` captures, S103/S104 text captures, S096 text capture, and absent-defect-register rows. All captures were read from disk. `corpus/QUALITY.md` criteria 3–8 require separation of observation/inference/unknown, source support, scoped tier and precise support states; `inference-ground.py` requires every inference bullet to cite an ID and carry a verbatim quote / numeral grounding token, with lexical polarity checks.
- Conversion command (only scratch output): `soffice --headless -env:UserInstallation=file:///tmp/chousa-r49-DraftEntryCCS/lo-profile --convert-to 'txt:Text (encoded):UTF8' --outdir /tmp/chousa-r49-DraftEntryCCS/ /tmp/chousa-r49-DraftEntryCCS/S101.doc /tmp/chousa-r49-DraftEntryCCS/S102.doc` → both OLE2 `.doc` inputs converted to `.txt`; the earlier `iconv -f UTF-16LE -t UTF-8 ...S101.raw` failed `illegal input sequence at position 3708` because those captures are OLE2, not raw UTF-16LE text.
- Capture-name check command: a Python `hashlib.sha256(url.encode()).hexdigest()[:24]` loop returned S101 `b539a80218080da56a75b624`, S102 `6dc68fd6b32ce9c8dfcebce8`, S103 `7809d5114330a60527436b07`, S104 `02aefcf570a7108e699d0990`, matching the four opened capture basenames. S096 URL was likewise mapped to `09fc63de41f293d43d631c46` and its opened capture contains both quoted caveat phrases.
- Quote check command in the eval kernel: `files[id].count(phrase)` for each TSV phrase returned exactly `1` (S096 phrases each 1; S104 `来源数据库` and `引用量` each 1; S101 zero-display phrase 1; S102 classification-purpose and field phrases each 1). Phrase `文献出处或电子文献的可获得地址` was deliberately not used because it occurs twice in S102. The S104 phrase `来源数据库、引用量以及下载量` was rejected because it is not contiguous in capture text. The report uses S096, never S076: renumber.tsv and sibling entry identify S096 as the CiNii row; S076's GNU sed manual is not used.
- Province check: **No inference bullet is a model/evaluation claim (kengaku);** each is about how to scope, interpret, and inspect citation evidence / research records. The S104 observation explicitly limits itself to guide-described interface behavior and disclaims answer validation.
- No lane gate, inference-ground invocation, or C2 counter was run; this is a draft/report task, not an admission or counter pass. No tools were installed.
- Scratch cleanup is required by the assignment and was completed with `rm -rf /tmp/chousa-r49-DraftEntryCCS`.

VERDICT: Drafted and quote-checked the lane citation-count entry, corrected S076 to S096, and narrowed unsupported CNKI / AI-answer claims; no gate or counter was executed.
