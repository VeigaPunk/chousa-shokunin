# R53DraftEntryWia — draft of `corpus/knowledge/western-instrument-alignment-r50.md` (round 53, wave 1)

seat `R53DraftEntryWia` (scribe, leaf) · lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` · lane HEAD `6365f15`, C1/C2 base `5b550133`
writes: this report only. No production file, no git/jj state, no fleet-repo write, no shokuknow write, no campaign tool run, no counter run against the lane.
tooling: nothing installed or upgraded (no pacman/uv/npm/cargo transaction). scratch `/fast/scratch/hyaku/chousa-r53/R53DraftEntryWia/`, `TMPDIR` exported there, removed at the end.

## 1. Frozen-claim position

I build the C2 document side for `E_WIA` only: Cochrane chapter 4 → planned lane id `S121`; the issued QC guideline PDF → planned lane id `S118` (the same PDF the QCG entry cites as staged S185: one lane row, twin staged ids). Nothing here proposes changing a predicate, target, counter, control or the DOCS table; the counter's rules I read read-only and wrote the draft to satisfy are `c2-count.py` (DOCS/TERMS `information specialist`, the `source:` regex on bound id + URL, S-token rule, ≥3 quote rows per bound id, anchor-`char`-is-a-quote-offset leg), `tools/inference-ground.py` (bullets, ≥2-word quotes, polarity) and `corpus/evidence/round51/quote-substance-check.py`.

## 2. Commands run and what they printed

```text
$ wc -c /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/c9d1e74c3ac8d9eb332c9770.txt /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/16fe8487aa97b98576a0dbac.txt
211326 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/c9d1e74c3ac8d9eb332c9770.txt
 61909 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/16fe8487aa97b98576a0dbac.txt
$ python3 - <<'PY'   # len(t), lines, sha256 of the file bytes
c9d1e74c3ac8d9eb332c9770 210708 722d3ce9b16486e8f7246670c37511b959abe427dc31304234e3ab12e665d97c
16fe8487aa97b98576a0dbac 27609 927ff71c6d499477c9cc7a3acf9ed7e335cd63b802850e5f39f5aa86a398d3a4
$ python3 - <<'PY'   # counters out of the .txt text forms
chars 210708 lines 1465
chars 27609 lines 1524
$ cd .qcache && for t in PRISMA prisma 灰色文献 未发表 内部资料 期刊评审 质量控制指南 指标 Cochrane; do c=$(grep -o -F "$t" 16fe8487aa97b98576a0dbac.txt | wc -l); echo "$t=$c"; done
PRISMA=0
prisma=0
灰色文献=0
未发表=0
内部资料=0
期刊评审=0
质量控制指南=2
指标=107
Cochrane=11
$ cd .qcache && python3 - <<'PY'   # handbook string counts
t=open('c9d1e74c3ac8d9eb332c9770.txt',encoding='utf-8').read()
for p in ['PRISMA-S','PRISMA 2020','PRISMA','MECIR','bias','unpublished','ongoing studies','information specialist']:
    print(repr(p), t.count(p))
PY
'PRISMA-S' 11
'PRISMA 2020' 10
'PRISMA' 31
'MECIR' 46
'bias' 43
'unpublished' 43
'ongoing studies' 10
'information specialist' 23
$ grep -rln 'Cochrane Handbook' corpus/knowledge
corpus/knowledge/contextual-source-admission-r24.md
corpus/knowledge/metadata-screen-r25.md
$ git grep -l -e 'information specialist' 5b550133 -- corpus/knowledge
(no output, exit 1)
$ git -C … rev-parse --short HEAD ; git -C … log --oneline -1
6365f15
6365f15 round-53: wave-1 spec and dispatch (49 seats)
```

Sweeps behind every negative claim in the entry:

```text
$ python3 -c "import re,pathlib;t=pathlib.Path('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/16fe8487aa97b98576a0dbac.txt').read_text(encoding='utf-8');print(len(t),len(re.findall('(?i)prisma',t)),len(re.findall('(?i)prisma-s',t)),[t.count(w) for w in ('对齐','接轨','灰色文献','未发表','内部资料','期刊评审','CHEERS','报告规范')])"
27609 0 0 [0, 0, 0, 0, 0, 0, 3, 6]
$ python3 -c "import re,pathlib;t=pathlib.Path('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/16fe8487aa97b98576a0dbac.txt').read_text(encoding='utf-8');a,b=t.find('1.文献研究的质量控制'),t.find('2.模型研究的质量控制');s=t[a:b];print(len(s),s.count('Cochrane'),len(re.findall('(?i)prisma',s)),len(s[s.find('（1）文献获取'):s.find('（2）数据提取')]),t.count('参照'),t.count('参照 Cochrane'))"
2168 3 0 412 5 2
$ python3 - <<'PY'   # （1）文献获取 subsection alone
t=open('16fe8487aa97b98576a0dbac.txt',encoding='utf-8').read()
a,b=t.find('（1）文献获取'),t.find('（2）数据提取'); sec=t[a:b]
print('获取 subsection',a,b,'chars',len(sec),'Cochrane',sec.count('Cochrane'),'prisma',len(re.findall('(?i)prisma',sec)))
PY
获取 subsection 10098 10510 chars 412 Cochrane 0 prisma 0
```

## 3. The staged headline and the PRISMA claim — verified, then narrowed

- "PRISMA counts 0 in the guideline": holds. 0 case-insensitively over the 27,609-character text form (also 0 for `prisma`, `Prisma`, `PRISMA-S`), 0 in the 2,168-char literature-research section, 0 in the 412-char （1）文献获取 subsection. Limit: text form only; no OCR or page-image pass.
- "the alignment exists only in the western handbook's own voice": holds only about alignment language and PRISMA names — 对齐 0, 接轨 0, and the asking verb 参照 occurs 5 times, twice as 参照 Cochrane (指标 4 and 指标 5, i.e. checklist questions put to the evaluator). It does NOT hold about reporting vocabulary: the guideline names CHEERS as 卫生经济学评价报告标准共识 (3 occurrences) and Cochrane RoB as an appraisal tool (附件三 table char 24614; also （4）证据质量评价 char 11148). The draft therefore claims the narrow version: the chapter asserts its own alignment; the guideline asks for compliance and names no search-reporting standard.
- Non-vacuity check: the same sweep finds CHEERS 3 and 报告规范 6 in the same file, so the zeros are not a dead matcher.

## 4. What this entry adds beyond the lane's two Handbook citations

`contextual-source-admission-r24.md` cites chapter 24 §24.2.1.3 (source admission); `metadata-screen-r25.md` cites chapter IV §IV.1 (currency assessment) and quotes "All Cochrane reviews should be assessed periodically…". Neither cites chapter 4, neither holds the §4.2.1 alignment bullet, the §4.3.2 unpublished-data statements or the term `information specialist` (0 files at base). This entry adds those, plus the paired issued Chinese guideline's search section, which no lane entry holds.

## 5. Entry (complete text; intended lane path `corpus/knowledge/western-instrument-alignment-r50.md`)

```markdown
# The alignment is asserted in one voice: the handbook's search chapter states that its reporting aligns with PRISMA and PRISMA-S, while the issued quality-control guideline's Cochrane references are a checklist question and an appraisal-tool list

source: S121 — https://training.cochrane.org/handbook/current/chapter-04 — Cochrane Handbook, Chapter 4 "Searching for and selecting studies" [last updated March 2025], version 6.5.1: §4.1, §4.2.1 Role of the information specialist/librarian (its services list, the MECIR/PRISMA bullet, the role sentence) and §4.3.2 Ongoing studies and unpublished data sources; text form `.qcache/c9d1e74c3ac8d9eb332c9770.txt`, 210,708 characters — char 7432, char 7735, char 9949, char 13480, char 35599, char 36552
source: S118 — https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf — 药品临床综合评价质量控制指南（2024 年版 试行）, 国家药物和卫生技术综合评估中心 (国家卫生健康委卫生发展研究中心), 二〇二四年十二月: 1.文献研究的质量控制, its （1）文献获取 and （4）证据质量评价 subsections, 指标 2 and 指标 4 of 3.项目实施, and 附件三; text form `.qcache/16fe8487aa97b98576a0dbac.txt`, 27,609 characters — char 78, char 9938, char 10119, char 10360, char 10394, char 10459, char 11148, char 17860, char 18046, char 18091, char 24614, char 25343
verified-at: 2026-10-26 — both captures re-opened from the read-only qcache; every quoted phrase re-located in its `.txt` text form at the stated offset (`count` 1, on one line); no fetch made (L0 `8d77e6c1` open)
recheck: 180d — `python3 -c "import pathlib;t=pathlib.Path('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/c9d1e74c3ac8d9eb332c9770.txt').read_text(encoding='utf-8');print(t.count('the reporting aligns with the current reporting guidance for PRISMA'),t.find('the reporting aligns with the current reporting guidance for PRISMA'))"` prints `1 13480`, and the same one-liner over the guideline's `.txt` with the 指标-4 line prints `1 18046`; then re-open the chapter URL and the PDF URL and confirm both read as printed, the `[last updated March 2025]` line is unchanged, and PRISMA still counts 0 in the guideline
ground: the campaign's cross-tradition lead — what the western chapter on search conduct says that the Chinese quality-control guideline does not, and what the guideline says that the chapter does not. The lane's two existing citations of the Handbook (its chapter on source admission, `corpus/knowledge/contextual-source-admission-r24.md`, §24.2.1.3, and its chapter on currency assessment, `corpus/knowledge/metadata-screen-r25.md`, §IV.1) hold neither of these sections and do not hold the term `information specialist`, which occurs 0 times in `corpus/knowledge` at the round-52 base (`git grep -l -e 'information specialist' 5b550133 -- corpus/knowledge` prints nothing, exit 1)
adopted: round 53 from the campaign package merge/chousa/ (staged `corpus/knowledge/western-instrument-alignment-r50.md`)

#### Observation

- **The handbook names itself, its edition and its scope.** Its citation line reads "Chapter 4: Searching for and selecting studies [last updated March 2025]" (`S121`, char 7432), inside "version 6.5.1 Cochrane, 2025" (char 7647), and §4.1 opens on "Cochrane reviews take a systematic and comprehensive approach" (char 7735), which fixes the frame of every later sentence in the chapter.
- **The role is a person's, not a field's.** §4.2.1 opens "Medical/healthcare librarians and information specialists have an integral role in the production of Cochrane reviews." (`S121`, char 9949); the section then lists the services a Cochrane Group may provide authors, from advising on databases and designing strategies to running the searches and drafting the methods section.
- **The alignment is stated as one item of that list, and what it aligns is reporting.** That item requires the review's conduct to meet the MECIR search expectations and "the reporting aligns with the current reporting guidance for PRISMA" (`S121`, char 13480), citing the two PRISMA 2020 papers and, in the same item, PRISMA-S (Rethlefsen et al 2021); the string PRISMA occurs 31 times in the text form and PRISMA-S 11 of them.
- **Unpublished studies are a bias question there.** In §4.3.2 "Initiatives to provide access to ongoing studies and unpublished data constitute a fast-moving field" (`S121`, char 35599); the next paragraph puts "Finding out about unpublished studies, and including their results in a systematic review when eligible and appropriate" (char 36552) as a step that "is important for minimizing bias" (char 36693).
- **The guideline's literature-research section fixes the acquisition procedure.** Under "1.文献研究的质量控制" (`S118`, char 9938) its （1）文献获取 subsection requires guideline evidence that is "应获取最新的、权威的且已公开发表" (char 10119), fixes "数据库应包括多个中、英文专业数据库。" (char 10360), the screeners "如遇分歧，则由第三方协助判断。" (char 10394) and the chart "根据文献筛选流程制定流程图，注明每环节" (char 10459); 指标 2 elsewhere requires academic evidence from "在同行评议期刊已发表" (char 17860) full texts or government reports.
- **Its Cochrane references are a compliance question and an appraisal-tool list.** 指标 4, in the 文献研究 row of 3.项目实施, reads "指标 4：在文献检索和筛选阶段，是否参照 Cochrane 等组织制定的" (char 18046) and continues "相应规范或指南开展文献检索，提供系统检索策略和文献筛选流程" (char 18091); the same section's （4）证据质量评价 (char 11148) names appraisal tools, and 附件三's table gives "Cochrane RoB 等" (char 24614) for randomized trials.
- **The guideline does name one reporting standard, for economic evaluation.** Its （4）subtask names CHEERS for health-economic evaluation (3 occurrences; 附件三's note gives the Chinese name "卫生经济学评价报告标准共识", char 25343), so the document is not without reporting vocabulary.
- **It dates itself and names its issuer.** Its title page carries "二〇二四年十二月" (`S118`, char 78); 国家药物和卫生技术综合评估中心 occurs 5 times, so the issuer is not quoted.

#### Inference

- **Of these two documents, only the handbook asserts an alignment; the guideline asks the evaluator to comply.** `S121` states "the reporting aligns with the current reporting guidance for PRISMA"; `S118` asks whether the search stage did "是否参照 Cochrane 等组织制定的" methods and requires "提供系统检索策略和文献筛选流程". A reader can take the chapter's sentence as the document's own claim and the checklist item as a question put to the evaluator; nothing in the guideline asserts an alignment of its own.
- **A record under the guideline carries procedure fields at each step.** `S118` fixes the databases ("数据库应包括多个中、英文专业数据库。"), the screeners ("如遇分歧，则由第三方协助判断。") and the chart that states counts and reasons per step ("根据文献筛选流程制定流程图，注明每环节"), so a search record built for this checklist can be checked step by step without a reporting standard.
- **The publication-status vocabulary runs one way in each document.** `S118` requires evidence that is "应获取最新的、权威的且已公开发表" and, at 指标 2, "在同行评议期刊已发表", and the text form holds 0 occurrences of 灰色文献, 未发表, 内部资料 and 期刊评审 (sweep in `#### Unknown`); `S121` makes the unpublished side a bias question — "Finding out about unpublished studies, and including their results in a systematic review when eligible and appropriate", "is important for minimizing bias".
- **The guideline names appraisal instruments and a reporting standard, and still no search-reporting standard.** `S118` lists "Cochrane RoB 等" as the tool for randomized trials and names a "卫生经济学评价报告标准共识" for economic evaluation, while PRISMA and PRISMA-S count 0 across its text form (sweep in `#### Unknown`); the absence is specific to the search-reporting layer, not to the document's instrument vocabulary.
- **Two documents, two jurisdictions of wording.** `S121` writes for "Cochrane reviews take a systematic and comprehensive approach", and `S118` is one national centre's guideline for 药品临床综合评价; the finding is about these two texts, and neither sentence can be carried to a tradition or a country.

#### Unknown

- **Sweep: PRISMA, alignment words and the unpublished-material terms in the guideline.** `python3 -c "import re,pathlib;t=pathlib.Path('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/16fe8487aa97b98576a0dbac.txt').read_text(encoding='utf-8');print(len(t),len(re.findall('(?i)prisma',t)),len(re.findall('(?i)prisma-s',t)),[t.count(w) for w in ('对齐','接轨','灰色文献','未发表','内部资料','期刊评审','CHEERS','报告规范')])"` prints `27609 0 0 [0, 0, 0, 0, 0, 0, 3, 6]`. PRISMA is absent in every case, as are the four unpublished-material terms and the two alignment words; the six 报告规范 occurrences are 指标 19–21 and the report template's 所选评价方法的报告规范, about reporting the evaluation results.
- **Sweep: Cochrane inside the guideline's literature-research section.** `python3 -c "import re,pathlib;t=pathlib.Path('/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/16fe8487aa97b98576a0dbac.txt').read_text(encoding='utf-8');a,b=t.find('1.文献研究的质量控制'),t.find('2.模型研究的质量控制');s=t[a:b];print(len(s),s.count('Cochrane'),len(re.findall('(?i)prisma',s)),len(s[s.find('（1）文献获取'):s.find('（2）数据提取')]),t.count('参照'),t.count('参照 Cochrane'))"` prints `2168 3 0 412 5 2`: the section holds Cochrane 3 times and PRISMA 0, the （1）文献获取 subsection alone (412 characters) holds it 0 times, and the asking verb 参照 occurs 5 times in the text form, twice as 参照 Cochrane.
- **What the extraction omits.** The claim that PRISMA counts 0 is a claim about the 27,609-character text form; a page rendered as an image would not appear in it, and no OCR or page-image pass was made.
- **Whether the checklist is met in practice.** 指标 4 asks a yes/no question of the evaluator; no evaluation report or audit under this guideline was opened this round, so compliance is unmeasured.
- **Whether other Chinese instruments name PRISMA-S.** Two documents were opened; the lane's other Chinese rows were not re-opened, and this entry says nothing about them.
- **Staged material narrowed on adoption.** The staged headline ("the alignment exists only in the western handbook's own voice") survives as a statement about alignment words and PRISMA names, but not as one about reporting vocabulary: the guideline names CHEERS as a reporting-standards consensus (3 occurrences) and names Cochrane RoB as an appraisal tool. The staged §4.3.2 quotation was normalized (it removed the parenthetical citation and two commas); this entry quotes the text as printed at char 36552. The staged inference that "naming an instrument in a references list is a different act" is dropped: 附件三's table is an instrument table, not a references list, and 指标 4 is a question, not a citation.
```

## 6. QUOTE machine lines (staged-id = planned lane id)

```text
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	Chapter 4: Searching for and selecting studies [last updated March 2025]	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	version 6.5.1 Cochrane, 2025	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	Cochrane reviews take a systematic and comprehensive approach	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	Medical/healthcare librarians and information specialists have an integral role in the production of Cochrane reviews.	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	the reporting aligns with the current reporting guidance for PRISMA	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	Initiatives to provide access to ongoing studies and unpublished data constitute a fast-moving field	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	Finding out about unpublished studies, and including their results in a systematic review when eligible and appropriate	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S121	https://training.cochrane.org/handbook/current/chapter-04	is important for minimizing bias	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	二〇二四年十二月	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	1.文献研究的质量控制	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	应获取最新的、权威的且已公开发表	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	数据库应包括多个中、英文专业数据库。	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	如遇分歧，则由第三方协助判断。	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	根据文献筛选流程制定流程图，注明每环节	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	（4）证据质量评价	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	在同行评议期刊已发表	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	指标 4：在文献检索和筛选阶段，是否参照 Cochrane 等组织制定的	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	相应规范或指南开展文献检索，提供系统检索策略和文献筛选流程	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	Cochrane RoB 等	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	卫生经济学评价报告标准共识	corpus/knowledge/western-instrument-alignment-r50.md
```

Offsets for the Registry anchor cells (each a `text.find` on the `.txt` text form; every quote occurs exactly once, on one line): S121 → 7432, 7647, 7735, 9949, 13480, 35599, 36552, 36693; S118 → 78, 9938, 10119, 10360, 10394, 10459, 11148, 17860, 18046, 18091, 24614, 25343. Capture digests for `spans.tsv`: S121 `722d3ce9b16486e8f7246670c37511b959abe427dc31304234e3ab12e665d97c`, S118 `927ff71c6d499477c9cc7a3acf9ed7e335cd63b802850e5f39f5aa86a398d3a4`.

## 7. Preflight of my own draft (scratch manifest, real tools, lane untouched)

```text
$ export TMPDIR=/fast/scratch/hyaku/chousa-r53/R53DraftEntryWia
$ python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/inference-ground.py --entry "$TMPDIR/entry.md" --spans "$TMPDIR/spans.tsv" --counts /dev/null --registry /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md --root "$TMPDIR"
GROUND entry=entry.md section=1 bullets=5 tokens=13 grounded=13
GROUND: PASS
$ python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round51/quote-substance-check.py "$TMPDIR/spans.tsv"
IDS=2 QUOTES=20 FAILURES=0
$ python3 - <<'PY'   # structural checks over the same two files
rows 20 missing_in_entry []
long []
ids_in_entry ['S118', 'S121']
lines 36
PY
```

This is a preflight of the tool legs only. `c2-count.py` was not run: it cannot pass until the L1 lands the entry, the Registry row, `quotes.tsv`, `spans.tsv` + span files and the round-53 lesson lines. Named limits: text forms only (no OCR); the twin-id relation (staged S185/S195 on one lane row) is asserted from the campaign package, not re-derived here.

## 8. Findings against the staged text (reported, not patched into the claim)

- Headline overreach: the staged inference "naming an instrument in a references list is a different act" does not fit — 附件三 is an instrument table, not a references list — and the guideline does name a reporting standard (CHEERS, 3×). Dropped.
- The staged §4.3.2 quotation was normalized (two commas and the "( Cook et al 1993 )" parenthetical removed); my quote is the printed stretch at char 36552, cut at a comma boundary on one line.
- Staged "It could not have held the alignment, because the Chinese document … never names PRISMA-S at all": the name absence is true (0), but the stronger evidence is 对齐/接轨 = 0 — no alignment language at all.
- §4.2.1 attribution is right; but the alignment sentence is one of twelve service items, not a section-level statement — corrected in wording.
- The staged body carried no other body ids; staged S193/S195 are replaced by the planned lane ids on the two `source:` lines and no staged id remains.

## 9. Out of scope / left to the L1

- Registry rows for S118 and S121 (`mined`, opened `2026-10-26`, anchor cells from the offsets above): S121's row is `used-by` this entry only; S118's row is the shared PDF row, so its `used-by` must name this entry **and** `corpus/knowledge/quality-control-guideline-issued-text-r48.md` (the counter compares that cell against exactly the existing entries carrying the `source:` line for that URL). Then `corpus/evidence/round53/quotes.tsv`, the `build-spans.py` run, the `c2-count.py` run, the round-53 lesson (`## Gate`, `refused-doc`/`refused-entry` lines), and the two sister entries.
- I ran no counter, edited no lane file, created no git fixture, fetched nothing, and used no shokuknow campaign tool. Scratch was created under `/fast/scratch/hyaku/chousa-r53/R53DraftEntryWia/` and removed.

VERDICT: Built and preflighted the draft entry for `corpus/knowledge/western-instrument-alignment-r50.md` — 20 single-line, exactly-once, offset-located quotes over the two captures (with `information specialist` inside one), inference-ground PASS 5/5 bullets / 13 tokens, quote-substance 0 failures — and attacked the staged headline: PRISMA/S counts of 0 and zero alignment words are confirmed, while the "no reporting vocabulary" reading is falsified (CHEERS 3, Cochrane RoB named), so the claim is narrowed to the search-reporting layer.
