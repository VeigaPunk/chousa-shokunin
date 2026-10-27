# R56GroundNote — S128 《药品临床综合评价工作流程指南》编制说明, grounded

seat: R56GroundNote (chousa round 56, leaf, no dispatch) · base `e5a3795191601797613eb986b36fa0b1a73fe6a1` · lane HEAD when read `99eff0e`
target: lane S128 — https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf
read-only: no fetch (L0 `8d77e6c1` open); lane touched only by this report. scratch `/fast/scratch/hyaku/chousa-r56/R56GroundNote` (removed)
## 1. Provenance — the defined text form is complete

```
KEY = sha256(url)[:24] = de9f5afc3809acbf61f4d5bb ; .pdf 321559  .raw 321559  .txt 17547 ; raw head 255044462d312e37 -> PDF
sha256 .pdf f3181ed0af4178ce04fdca5e0570def229fb96d50fc92cd288fdbd1c6c3e50f3   .txt 7e3e3cf426a787a62b50fdae064e54ab28865a1ef5114cd0bf5687a87d2bd9d2 (capture_sha256 in spans.tsv)
pdfinfo: Pages 8, CreationDate Mon Apr 7 05:02:38 2025 -03, Producer Word 2021
pdftotext -> squeezed equal? True ; form 6296 non-ws chars ; pdftotext 6296 ; xpages 8
```

`.raw` is a PDF, so the DEFINED form is the `.txt` read UTF-8 / universal newlines: **7,031 chars, 220 lines, no CR**,
form-feeds at 953/1866/2847/3619/4460/5392/6334/7030 (8 pages). The capture is a complete, whitespace-only-different rendering
of the PDF, so every absence count below stands for the whole document, not for a truncated extraction.
## 2. Identity

- **Title on line 1** (char 0; the quoted slice begins char 4): `《药品临床综合评价工作流程指南》编制说明` — the explanatory note *of a draft*, not the standard.
- **Class: 团体标准** (chars 1809, 2300): the three bodies `共同发起制定` (line 56) + `《药品临床综合评价工作流程指南》团体标准` (char 1793); `2023 年 6 月，中国药师协会线上召开团体标准立项评审会` (char 2276).
- **Issuer / 立项 body: 中国药师协会** (7×: 47, 98, 119, 1739, 2007, 2290, 2432): `由中国药师协会平台立项。` (char 77).
- **Proposers = drafters** (the 任务来源 block, chars 41–168): 中国药师协会药品临床评价工作委员会；天津市药品使用监测和临床综合评价中心；天津医科大学总医院 (提出, then repeated as 主要起草单位 at char 112); `标准负责人：李正翔（天津医科大学总医院）` (char 170).
- **No printed issue date.** No cover block, no 发布/二〇二五 line for the note itself (`发布` ×9 = policy documents and the centre's instruments; `二〇二五` 0; `2025 年 4 月` 0). Self-dating only: `于 2025 年` (3301) + `3 月定稿。` (3310) → **定稿 2025 年 3 月**, drafting `历时 18 个月` (2592). PDF CreationDate **2025-04-07** matches the `/20250407/` upload path — metadata, not print.
## 3. The adopted grading systems — exact sentence, months and years

Lines 95–97, chars 3064–3149 (one sentence, hard-wrapped at two points):

```
（2）2024 年 6 月-8 月，工作组采用中国循证医学中心中国循证医学中心的
证据分级体系，采用牛津大学循证医学中心制定的推荐强度分级标准对证据进行
质量评价和分级。
```

- **`2024 年 6 月-8 月`** is the only window attached to the adoption (year 2024, months June–August); it sits between stage (1) `2023 年 7 月-2024 年 6 月` search (char 2921) and stage (3) `2024 年 9 月-12 月` Delphi (char 3150).
- 中国循证医学中心 supplies `证据分级体系`; 牛津大学循证医学中心 supplies `推荐强度分级标准`. **No year is given for either system** — an entry must not attach one, and `牛津标准`/`Oxford standard` does not occur (only `牛津大学循证医学中心制定的推荐强度分级标准`, count 1, char 3114).
- **Source defect, verbatim:** the centre's name is printed twice — `采用中国循证医学中心中国循证医学中心的` (3082–3105). It is in the PDF text layer (pdftotext identical) and the draft S127 repeats it across a wrap (char 8289, the break written `\n`: `采用中国循证\n医学中心中国循证医学中心的证据质量分级体系`), so the defect is in the documents, not the capture. Wording differs: draft `证据质量分级体系`, note `证据分级体系`, journal `证据分级体系` (S129, count 1).
- The clean phrase `中国循证医学中心的证据分级体系` occurs **0 times** in this form (broken by the doubling and a newline); it occurs once in S129's form. An S128 quote must carry the doubling or start at char 3105.
## 4. Reference list — the national centre and its instruments

`参考文献：` at char 5595 (a bibliography; `规范性引用文件` 0×). Seven entries, chars 5602–7031:

| ref | char | issuer as printed | instrument | host |
|---|---|---|---|---|
| [3] | 5919 | 国家药物和卫生技术综合评估中心（国家卫生健康委卫生发展研究中心）、国家卫生健康委药具管理中心 | 药品临床综合评价管理指南(2021 年版 试行) | nhc.gov.cn/cms-search/downFiles/86…pdf |
| [4] | 6123 | 国家药物和卫生技术综合评估中心 （…）、国家心血管病中心、…安贞医院、…药具管理中心 | 心血管病药品临床综合评价技术指南（2022 年版 试行） | cpia.net.cn/uploads/20220630/…pdf |
| [5] | 6361 | 国家药物和卫生技术综合评估中心（…）、国家儿童医学中心、…药具管理中心 | 儿童药品临床综合评价技术指南（2022 年版 试行） | cpia.org.cn/uploads/20220630/…pdf |
| [6] | 6600 | 国家药物和卫生技术综合评估中心（…）、国家癌症中心、…药具管理中心 | 抗肿瘤药品临床综合评价技术指南（2022 年版 试行） | hnysfww.com/data/article/…pdf |
| [7] | 6827 | **国家药物和卫生技术综合评价中心** (no 评估, no parenthetical) | 药品临床综合评价质量控制指南（2024 年版 试行） | nhei.cn/nhei/znfb/**202412**/d33db3fc…shtml |

`国家药物和卫生技术综合评估中心` **5×** (refs [3][4][5][6] + §5 at char 4792); `国家药物和卫生技术综合评价中心` **1×** ([7]);
`国家卫生健康委卫生发展研究中心` **4×** ([3]–[6] only). §5 (4792–5079), whose opening slice is the landed quote at char 4792, names the centre across lines 156–157 and then its instruments:
`家卫生健康委卫生发展研究中心“）发布了《心血管病药品临床综合评价技术指` (char 4831), the three 2022 guides, `并于 2024 年发布`
(char 4944), `《药品临床综合评价质量控制指南（2024 年版 试行）》等文件` (char 4956).

Defects, reported not patched: (1) [7] carries access date `[2023-07-10]` for a **2024** edition whose URL path is `202412` and which §5
dates `并于 2024 年发布`; (2) refs [3]–[7] share one batch stamp `[2023-07-10]` while [1]/[2] carry `[2024-09-22]`; (3) [4]/[6] serve the
centre's instruments from cpia.net.cn and hnysfww.com, not the centre's or commission's domain; (4) [7]'s issuer string differs from
[3]–[6] and the note never says it is the same body.
## 5. 灰色文献 — absent; S128 must not be cited for the row

```
灰色文献 0 · 灰色 0 · 未公开发表 0 · (?i)grey|gray 0
文献 4 -> 文献调研 (2052), 文献数据库 (3025), 文献调研 (3459), 参考文献 (heading 5595, 文献 at 5597)
```

The search step names channels only, without the term or the definition (chars 2921–3061): `从指南数据库、系统评价、` (line 92) `卫生技术评估、卫生经济学评价研究数据库、文献数据库、官方网站及公共搜索` (char 3005) `引擎进行证据全面检索` (char 3041). S128 grounds provenance (who, when, which method stage) and nothing
about grey literature; the staged r42 entry and the landed entry both respect this — no overclaim to report, only the standing rule.
## 6. Landed S128 rows — independently re-verified (5/5); each span = `form[offset:offset+len]`, quote unique, one line, ≤25 words/≤160 chars

```
S128-1 off=0    slice=True find=4   abs=4    line=1   words=1 len=20     S128-4 off=3025 slice=True find=80 abs=3105 line=96  words=1 len=35
S128-2 off=0    slice=True find=77  abs=77   line=5   words=1 len=32     S128-5 off=4712 slice=True find=80 abs=4792 line=156 words=2 len=38
S128-3 off=2984 slice=True find=80  abs=3064 line=95  words=5 len=40     registry anchors 4/77/3064/3105/4792 == computed abs offsets
```
## 7. Ready-to-bind quotes — first five landed, last seven new (absent from spans.tsv, entry and lesson)

```
QUOTE	S128	https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf	《药品临床综合评价工作流程指南》编制说明	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S128	https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf	床综合评价中心；天津医科大学总医院提出，由中国药师协会平台立项。	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S128	https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf	（2）2024 年 6 月-8 月，工作组采用中国循证医学中心中国循证医学中心的	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S128	https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf	证据分级体系，采用牛津大学循证医学中心制定的推荐强度分级标准对证据进行	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S128	https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf	（下简称为“管理指南”）。2022 年，国家药物和卫生技术综合评估中心（“国	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S128	https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf	主要起草单位：中国药师协会药品临床评价工作委员会；天津市药品使用监	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S128	https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf	（1）2023 年 7 月-2024 年 6 月，工作组针对已确定的研究问题，参照 PICO	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S128	https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf	卫生技术评估、卫生经济学评价研究数据库、文献数据库、官方网站及公共搜索	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S128	https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf	初稿，提交全体编写组专家成员征求意见，经过 2 轮专家共识函审，于 2025 年	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S128	https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf	《药品临床综合评价质量控制指南（2024 年版 试行）》等文件，就药品临床综	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S128	https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf	[3] 国家药物和卫生技术综合评估中心（国家卫生健康委卫生发展研究中心）、	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S128	https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf	[7] 国家药物和卫生技术综合评价中心.药品临床综合评价质量控制指南（2024	corpus/knowledge/grey-literature-field-china-r42.md
```

New offsets (span may start there, `find=0`, span longer than quote): 112, 2921, 3005, 3269 (+ `3 月定稿。` at 3310), 4956, 5919,
6827 — each `form.count(quote)==1`, `form.find` = that offset, on lines 6, 91, 93, 101, 160, 198, 217; word/char 1/33, 8/46, 1/35,
5/40, 3/38, 2/37, 2/39.
## 8. Grounding gaps and calibration (reported, not patched)

- The bibliography names the centre five times with five instruments, but **no reference-list slice is quoted by S128** in `spans.tsv`, the entry or the lesson; the entry's only centre-related S128 quote is §5 at char 4792, truncated inside the name (`…综合评估中心（“国`). Rows at 5919 and 6827 close that gap.
- The staged sibling `grey-literature-national-route-r44.md` calls the note's list "normative references"; the heading is `参考文献：` (5595) and `规范性引用文件` is absent — whatever is adopted, that phrase must not travel.
- The staged r44 recheck promises to confirm the note "still records the adoption of 中国循证医学中心的证据分级体系" — that phrase is 0× in this form (§3); a recheck must target `2024 年 6 月-8 月` or the char-3105 continuation.
- 2024-06..08 is the only dated claim about the adoption; §5's `并于 2024 年发布` is the only dated claim about the QC guideline and contradicts ref [7]'s `[2023-07-10]`.

VERDICT: S128 《药品临床综合评价工作流程指南》编制说明 was grounded from its complete 8-page capture — identity (title, 中国药师协会立项,
团体标准, no printed issue date, 定稿 2025-03), the adoption sentence (中国循证医学中心 证据分级体系 + 牛津大学循证医学中心 推荐强度分级标准,
`2024 年 6 月-8 月`), five of seven references naming the national centre and its five instruments, and 灰色文献 0× — SURVIVED as a
provenance/method source, with four internal defects reported verbatim (doubled centre name, [7] 2023 access of a 2024 edition, batch
access stamps, [7] issuer variant) and one landed gap: no reference-list slice quoted.
