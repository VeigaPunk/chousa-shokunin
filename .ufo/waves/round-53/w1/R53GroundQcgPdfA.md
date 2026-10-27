# R53 ground — S185/S195 → planned lane S118: the issued quality-control guideline PDF

seat: `R53GroundQcgPdfA` (chousa, round 53 wave 1, leaf — no subagent dispatch).
scope: re-ground the two staged entries that rest on the issued 《药品临床综合评价质量控制指南（2024 年版 试行）》
against its on-disk capture; planned lane id **S118**; findings only — no predicate, target, counter or control touched.
writes: this report file only (all other reads read-only; scratch `$S=/fast/scratch/hyaku/chousa-r53/R53GroundQcgPdfA`, removed at exit).

## 1. Capture, hashes, and whether the `.txt` is a faithful text form

```
$ ls -l .qcache/16fe8487aa97b98576a0dbac.*
-rw-r--r-- 415245 16fe8487aa97b98576a0dbac.pdf / .raw ; -rw-r--r-- 61909 16fe8487aa97b98576a0dbac.txt
$ sha256sum *.pdf *.raw *.txt
7b600fe3ee9bda2bd59f437a689451486f746af0c1daf2774aab2aec56b67e26  16fe8487aa97b98576a0dbac.pdf
7b600fe3ee9bda2bd59f437a689451486f746af0c1daf2774aab2aec56b67e26  16fe8487aa97b98576a0dbac.raw   # pdf == raw
927ff71c6d499477c9cc7a3acf9ed7e335cd63b802850e5f39f5aa86a398d3a4  16fe8487aa97b98576a0dbac.txt
$ file 16fe8487aa97b98576a0dbac.pdf  -> PDF document, version 1.7, 42 page(s)
$ pdfinfo ...raw | egrep 'Creator|CreationDate|Pages'
Creator: WPS 文字 ; CreationDate: Tue Dec 31 06:01:53 2024 -03 ; Pages: 42
$ python3 -c 'len(t)' -> 27609 chars ; t.count(chr(0xFFFD)) -> 0 ; grep -c \x0c -> 42
$ pdftotext -layout -enc UTF-8 16fe8487aa97b98576a0dbac.raw $S/pt.txt   # pdftotext 26.08.0
$ sha256sum $S/pt.txt -> 927ff71c...a4 ; wc -c -> 61909 ; difflib sidecar vs pt.txt: diff ops 0, equal True
```

The `.txt` sidecar is **byte-identical** to `pdftotext -layout -enc UTF-8` of the raw (not merely a sample): 61,909 bytes,
27,609 characters, **U+FFFD count 0**, 42 form-feed page breaks = 42 PDF pages. All offsets below are `str.find` on that `.txt`.

## 2. S185 — `corpus/knowledge/quality-control-guideline-issued-text-r48.md` claim by claim

| claim (first ≤80 chars) | verdict | located quote (offset) |
|---|---|---|
| the national centre (国家药物和卫生技术综合评估中心, also 国家卫生健康委卫生发展研究中心) issued the guideline | located — cover title block, lines at 0/15/36/53/78 | `（国家卫生健康委卫生发展研究中心）` 53; `二〇二四年十二月` 78 |
| …on 2024-12-31 and released it on 2025-01-03, with a notice that reads 现予以发布 | absent in this text / partly corroborated — `2024-12-31` 0, `12月31日` 0, `2025` 0, `现予以发布` 0; PDF CreationDate is Tue Dec 31 06:01:53 2024; date+notice belong to S186 | title block only: `二〇二四年十二月` 78 |
| names the issuing body as 国家卫生健康委卫生发展研究中心 | located | `（国家卫生健康委卫生发展研究中心）` 53 |
| Both the notice and the issued text are open access, on a professional society's own file host | absent from the document — `北京市卫生经济学会` 0, `卫生经济学会` 0, `北京市` 0; the carrier is only in the URL host (bjhea.org.cn) and the staged row | — (host from URL, not text) |
| The issued text's title block reads 药品临床综合评价质量控制指南 /（2024 年版 试行）/ 国家药物和卫生技术综合评估中心 /（国家卫生健康委卫生发展研究中心）/ 二〇二四年十二月 | located exactly, as five cover lines (0/15/36/53/78) | `   （2024 年版 试行）` 15 (three leading spaces make it unique; the bare string occurs twice) |
| Its §1 文献研究的质量控制 divides the evidence into 循证指南 and 学术研究 | located-narrower — heading is `1.文献研究的质量控制`; taxonomy sentence splits at a line break (lines 675/677) | `1.文献研究的质量控制` 9938 |
| sets the inclusion and exclusion criteria 由评价主题确定 and 可基于 PICOS 原则 | contradicted as quoted — the text reads 根据评价主题确定; `由评价主题确定` 0 occurrences; `可基于` 10187, `PICOS` 10191 | `根据评价主题确定纳入与排除标准` 10171 |
| requires 所检索的数据库应包括**多个**中、英文专业数据库 | located — sentence split at 10359 (`所检索的` ends line 698) | `数据库应包括多个中、英文专业数据库。` 10360 |
| two researchers to screen independently with a third arbitrating | located — `由两名研究人员独立筛` / `选文献，如遇分歧，则由第三方协助判断。` split at the break | `由第三方协助判断` 10400 |
| and a flow chart recording the counts and reasons at each step | located | `根据文献筛选流程制定流程图，注明每环节` 10459; `纳入与排除文献的数量及理由，以保证纳入文献的可靠性。` 10480 |
| Over the whole extraction — 27,609 characters — 灰色文献 0, 灰色 0, 未发表 0, 内部资料 0, 期刊评审 0; 文献检索 3, 系统评价 7, 数据库 3, PICOS 1 | located exactly — len 27609; measured 0/0/0/0/0 and 3/7/3/1 | counts re-run on the `.txt` (§1 command block) |
| The corpus already held a row for this guideline, quoting the draft for comment | out of this document — the lane row is S176 (a 征求意见稿 file); this PDF names its own predecessor 《…（2024 年版 讨论 稿）》 across a line break; `征求意见` 0 here | `稿）》` 3367 (preceded by `讨论` at 3222+146) |
| the draft's 纳入标准应基于 PICOS 原则 becomes 可根据评价主题确定纳入与排除标准，可基于 PICOS 原则 | contradicted — `可根据评价主题确定` 0; issued text keeps 应: 应根据评价主题确定纳入与排除标准，可基于“PICOS”原则进行 | `根据评价主题确定纳入与排除标准` 10171 + `可基于` 10187 |
| the draft's 所检索的数据库应包括中、英文专业数据库 becomes …应包括**多个**… | located for the issued side (the 中、英文专业数据库 fragment is split from 数据库 by the break) | `数据库应包括多个中、英文专业数据库。` 10360 |
| The grey-literature count is 0 in both | 0 in this text; the draft capture (S176) was not re-opened by this seat | `灰色` 0; `灰色文献` 0 |
| Inference: the issued guideline carries no grey-literature field | located — 灰色文献/灰色/未发表/内部资料/期刊评审 all 0 over 27,609 chars | counts §1 |
| Inference: 应 becomes 可, and 一个数据库 becomes 多个数据库 | contradicted for 应→可 (应 is retained on the criteria; 可 attaches to the PICOS basis); located for 多个 | `根据评价主题确定纳入与排除标准` 10171 |
| Unknown: the issued text's 附件四 is titled 药品临床综合评价报告模板 | located — 附件四：药品临床综合评价报告模板 (TOC and body) | `附件四：药品临床综合评价报告模板` 2274 |

## 3. S195 — `corpus/knowledge/western-instrument-alignment-r50.md` claim by claim

| claim (first ≤80 chars) | verdict | located quote (offset) |
|---|---|---|
| The Chinese one — the national centre's issued 《药品临床综合评价质量控制指南（2024 年版 试行）》 — prescribes… | located, but only as the two cover lines: the single string with 《》 title and 试行 is 0 occurrences (cover splits 药品临床综合评价质量控制指南 / （2024 年版 试行）) | `   （2024 年版 试行）` 15 (bare form also at 3553); `药品临床综合评价质量控制指南` 0 |
| the evidence taxonomy into 循证指南 and 学术研究 | located-narrower (taxonomy sentence crosses the 9980/10010 break, so only the second half is quotable whole) | `证指南和学术研究。循证指南包括临床指南、药品使用规范、专` 9981 |
| inclusion by evaluation theme on PICOS | located | `根据评价主题确定纳入与排除标准` 10171; `可基于` 10187 |
| the search's databases to include 多个中、英文专业数据库 | located | `数据库应包括多个中、英文专业数据库。` 10360 |
| two researchers screening independently with a third arbitrating | located | `由第三方协助判断` 10400 |
| and a flow chart recording counts and reasons at each step | located | `根据文献筛选流程制定流程图，注明每环节` 10459 |
| 指标 4 asks whether the search and screening stage referred to the methods developed by Cochrane… | located-narrower — the 文献研究 row is 指标 4 at 18046, but `指标 4` labels four different rows (16260 主题遴选, 17080 立项启动, 18046 文献研究, 19653 报告), so `指标 4` alone is ambiguous | `指标 4：在文献检索和筛选阶段，是否参照 Cochrane 等组织制定的` 18046 + `确保获取文献的全面性和准确性` 18130 |
| the Cochrane risk-of-bias tool is named as an instrument to use | located — also printed spaced at 11581 and as `Cochrane RoB` in the tool table (24614/25153) | `风险偏倚评估工具` 25144 |
| Over the whole 27,609-character extraction, PRISMA counts 0 | located — also PRISMA-S 0 and MOOSE 0 in this document | `PRISMA` 0; `MOOSE` 0; len 27609 |
| Inference: the corpus's Chinese documents name PRISMA, MOOSE and the Cochrane Handbook | not supported by THIS document for PRISMA/MOOSE (both 0); the handbook IS named in 附件三's tool list, its title split at the break | `《Cochrane 干预措施系统评价手` 24134 |
| Inference: it is a Cochrane-referenced quality-control document | located — Cochrane ×11, incl. 指标 4 and 指标 5 (是否参照 Cochrane 等组织制定的相应规范或指南) | `指标 4：在文献检索和筛选阶段，是否参照 Cochrane 等组织制定的` 18046 |
| Inference: no field for unpublished evidence — 灰色文献, 未发表, 内部资料, 期刊评审 each 0 | located | counts §1 |
| Inference: graded on databases, screening and the flow chart | located-narrower — indicators 4 and 6 (文献研究 stage) and 31 (附件) grade exactly those | `提供系统检索策略和文献筛选流程` 17222 and 18083 (指标 6 / 指标 4); `指标 31：是否提供项目主要的技术附件，如检索策略、检索结果和` 22082 |

## 4. Findings routed to the L1 (no predicate/counter touched)

F1 **`由评价主题确定` is not in the document** (0 occurrences); the text reads `根据评价主题确定` (10171). Any span built from the
   S185 Observation sentence must use 根据, or record the entry's wording as a paraphrase.
F2 **`应 becomes 可` is contradicted by the issued text.** The issued sentence keeps 应 on the criteria and puts 可 on the PICOS
   basis: `应根据评价主题确定纳入与排除标准，可基于“PICOS”` (10167–10197) + `原则进行` (10199) — the sentence crosses the
   10197/10199 break, so it is quotable only as those two fragments. The claimed issued string `可根据评价主题确定`
   is absent. The draft→issued shift that IS visible on the issued side is 可 based on PICOS (an option), not 应→可 on the criteria.
F3 **Notice facts are not in this document**: 2025-01-03, `现予以发布`, 1,461-char notice — those rest on S186, not S185. The
   S185 Observation sentence fuses the two; the L1 should keep the dates/quotation bound to the notice entry.
F4 **2024-12-31 is not in the text either** (`2024-12-31` 0, `12月31日` 0); the title block says only 二〇二四年十二月 (78). The
   PDF's CreationDate (Tue Dec 31 06:01:53 2024 -03) is a metadata corroboration, not a located quote.
F5 **`北京市卫生经济学会` occurs 0 times** in the document. The carrier attribution is carried only by the URL host and the staged
   row (北京市卫生经济学会 载); no quote can bind it to the text.
F6 **`指标 4` is not a unique designator** — four rows carry it (16260, 17080, 18046, 19653). S195's sentence is correct only with
   the stage named (文献研究 stage, under 2.立项启动 in 附件一).
F7 **Search-record profile of the instrument** (the theme continuation): `检索策略` 5 (数据库检索策略 as a required technical
   attachment at 14500, 系统检索策略 at 17222/18109, 检索策略、检索结果和纳入/排除研究列表 at 22082/27457), `数据库` 3, `检索日期` 0,
   `检索时间` 0, `PRISMA` 0, `PRISMA-S` 0. The guideline requires a search strategy and a screening flow chart but has **no search-date
   field** — a located, quotable asymmetry for C2's instrument theme (this seat's own reading, not a counter result).
F8 The title string `《药品临床综合评价质量控制指南（2024 年版 试行）》` occurs 0 times as one string; the cover splits it over two
   lines and the 前言 cites the 讨论稿. A span quoting it must cover the split or use the two fragments.

## 5. QUOTE machine lines (11; staged-id = planned lane id S118; every quote byte-exact, one line, unique, offsets verified)

```
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	（国家卫生健康委卫生发展研究中心）	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	二〇二四年十二月	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	1.文献研究的质量控制	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	（1）文献获取	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	根据评价主题确定纳入与排除标准	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	数据库应包括多个中、英文专业数据库。	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	根据文献筛选流程制定流程图，注明每环节	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	数据库检索策略	corpus/knowledge/quality-control-guideline-issued-text-r48.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	指标 4：在文献检索和筛选阶段，是否参照 Cochrane 等组织制定的	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	确保获取文献的全面性和准确性	corpus/knowledge/western-instrument-alignment-r50.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	风险偏倚评估工具	corpus/knowledge/western-instrument-alignment-r50.md
```

## 6. Limits / out of scope

- Not opened here: the draft capture S176 (20250102/…pdf), the notice S186, the 2019 NMPA copy S190, Cochrane ch.4 S193 — neighbours' seats.
- No counter run (`c1-count.py`/`c2-count.py` untouched), no lane entry, row, span or lesson written; C2 is not scored by this seat.
- Offsets are `str.find` on the `.txt` text form; the `.raw` is the same bytes as the `.pdf`, so the span file for any row built from
  this seat should be the `.txt` (digest 927ff71c…a4) and cannot be shorter than the quote.
- Tooling: nothing installed or upgraded (pdftotext 26.08.0 and pdfinfo already present).

VERDICT: attacked the issued guideline PDF behind S185/S195 — the capture is faithful (byte-identical to `pdftotext -layout`, 0 U+FFFD),
all quantitative and structural claims (27,609 chars, 0/0/0/0/0 grey terms, 3/7/3/1, title block, §1/（1）, 指标 4, RoB tool, 附件四)
are located, while two wording claims fail as written (`由评价主题确定` absent; `应 becomes 可` contradicted — the issued text retains 应;
2024-12-31/2025-01-03/现予以发布 and the society's name are not in this document), and the instrument has no search-date field.
