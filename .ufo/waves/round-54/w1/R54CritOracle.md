# R54CritOracle — C1 REAL falsifiers

Evidence: frozen claim at `corpus/evidence/round54/claims.md` (opened); `c1-count.py` lines 244–276 define `leg_real`: per-line presence (after optional leading-label removal), 0.90–1.10 whitespace-free length, pinned quote locate; no sequence/order comparison and no upper-bound/equality test for text. Candidate extracted from commit `8a7d0f137a352000d78704ba5695ded8857104fe`, SHA-256 `fd0ed3f58565b781ab8eedaad5d229976e150bdd8e391a2b0cacd0a0825fcd89`.

## Attack scoring
Ran each command with `TMPDIR=/fast/scratch/hyaku/chousa-r54/R54CritOracle`, `--seed 54`, distinct scratch `--work` directory; each used frozen `c1-count.py` and emitted all six leg results. Relevant observed output:

| variant | GEN | REAL | all legs | result |
|---|---|---|---|---|
| drop every 10th output paragraph | FAIL (item count 0) | FAIL: oracle line missing `5.2.9　数据转换问题\t4` | 4/6 | REAL catches omission |
| duplicate whole output | FAIL (item count 2) | FAIL: ratio 1.944 | 4/6 | ratio catches duplication |
| append table-stream strings, capped at 5% of output's non-whitespace length | PASS | PASS 5 captures | 6/6 | **wrong output accepted** |
| retain field-code text | FAIL (item count 0) | FAIL: oracle line missing `2　规范性引用文件\t1` | 4/6 | field interpretation altered; this variant fails, not a counterexample |
| append footnote/header/textbox CP stories | PASS | PASS 5 captures | 6/6 | **wrong output accepted** |
| reverse piece-table pieces | PASS | FAIL: oracle line missing `5.2　代码问题\t2` | 5/6 | piece boundaries split lines; REAL catches this case |
| reverse paragraph output order | FAIL (item out of order) | FAIL: oracle line missing table header | 4/6 | this implementation also reverses table-cell/newline structure; not a clean order-only probe |

Receipts were generated at `score_{drop10,dup,tblstrings,fieldcodes,foothead,reorderpieces,reorderparas}.txt` under scratch; exact reported REAL/GEN/LEGS lines are transcribed above. The `tblstrings` variant appends printable table-stream strings, truncated to 5% of its output length; the uncapped extraction was also smoke-tested and grew the 54fe twin output from 33,239 to 135,697 bytes (well beyond the ratio allowance). The capped variant is the useful falsifier: it adds arbitrary non-story text yet passes every frozen leg. Foothead variant extends CP extraction through non-main stories and likewise passes all legs. These are counterexamples to REAL's exclusion/precision guarantee, not proposals to alter the frozen predicate.

## Label-drop-only oracle lines
I built the oracle with the same `soffice --headless --convert-to 'txt:Text (encoded):UTF8'` filter and compared candidate output using the counter's `ws0` and label regex. Every following line is an oracle line whose full whitespace-free form was absent but whose post-label remainder was present. Format: `capture: label => exact oracle line` (twin capture has identical findings; shown once per distinct document). This is all observed lines, including the repeated twin result represented by its twin key.

```text
54fe0734c01f699e735b4b0a (identical for 74ced3e9311594a8cc3f1f42):
—— => —— 原标准GB/T 33561—2017和GB/T 30279—2013中的范围对应本标准的范围，内容进行合并修改。
—— => —— 原标准GB/T 33561—2017和GB/T 30279—2013中的规范性引用文件对应本标准的规范性引用文件，引用文件内容有所补充。
—— => —— 原标准GB/T 33561—2017和GB/T 30279—2013中的术语和定义对应本标准的术语和定义，内容进行合并修改。
—— => —— 删除了原标准GB/T 33561—2017中的缩略语。
—— => —— 原标准GB/T 33561—2017中的“按成因分类”对应本标准的“网络安全漏洞分类”，将原标准采用的线性分类框架调整为树形
—— => —— 删除原标准GB/T 33561—2017中的“按空间分类”。
—— => —— 删除原标准GB/T 33561—2017中的“按时间分类”。
—— => —— 原标准GB/T 30279—2013的“等级划分要素”对应本标准的“网络安全漏洞评级指标”，丰富了漏洞分级指标。
—— => —— 原标准GB/T 30279—2013的“等级划分”对应本标准的“网络安全漏洞分级方法”，将原标准中的分级方法修订为技术分级和综合分级。
图1 => 图1　 网络安全漏洞分类导图
5.2.3.1 => 5.2.3.1　 概述
5.2.3.2 => 5.2.3.2　 缓冲区错误
5.2.3.3 => 5.2.3.3　 注入
5.2.3.3.1 => 5.2.3.3.1　 概述
5.2.3.3.2 => 5.2.3.3.2　 格式化字符串错误
5.2.3.3.3 => 5.2.3.3.3　 跨站脚本
5.2.3.3.4 => 5.2.3.3.4　 命令注入
b) => b) 操作系统命令注入
5.2.3.3.5 => 5.2.3.3.5　 代码注入
5.2.3.3.6 => 5.2.3.3.6　 SQL注入
5.2.3.4 => 5.2.3.4　 路径遍历
5.2.3.5 => 5.2.3.5　 后置链接
5.2.3.6 => 5.2.3.6　 跨站请求伪造
5.2.8.1 => 5.2.8.1　 信任管理问题
5.2.8.2 => 5.2.8.2　 权限许可和访问控制问题
5.4.2.1 => 5.4.2.1　 概述
5.4.2.2 => 5.4.2.2　 日志信息泄露
5.4.2.3 => 5.4.2.3　 调试信息泄露
5.4.2.4 => 5.4.2.4　 侧信道信息泄露
6.2.1.1 => 6.2.1.1　 访问路径
表1 => 表1　 访问路径赋值说明表
6.2.1.2 => 6.2.1.2　 触发要求
表2 => 表2　 触发要求赋值说明表
6.2.1.3 => 6.2.1.3　 权限需求
表3 => 表3　 权限需求赋值说明表
6.2.1.4 => 6.2.1.4　 交互条件
表4 => 表4　 交互条件赋值说明表
表5 => 表5　 保密性影响赋值说明表
表6 => 表6　 完整性影响赋值说明表
表7 => 表7　 可用性影响赋值说明表
6.2.3.1 => 6.2.3.1　 被利用成本
表8 => 表8　 被利用成本赋值说明表
6.2.3.2 => 6.2.3.2　 修复难度
表9 => 表9　 修复难度赋值说明表
6.2.3.3 => 6.2.3.3　 影响范围
表10 => 表10　 影响范围赋值说明表
图2 => 图2　 漏洞分级流程图
6.3.2.1 => 6.3.2.1　 被利用性评级
6.3.2.2 => 6.3.2.2　 影响程度评级
6.3.2.3 => 6.3.2.3　 环境因素评级
1 => 1　网络　低　无　不需要　9
2 => 2　网络　低　低　不需要　8
4 => 4　邻接　低　无　不需要
5 => 5　本地　低　无　不需要
6 => 6　网络　高　无　不需要
7 => 7　网络　低　低　需要　7
8 => 8　邻接　低　低　不需要
9 => 9　网络　低　高　不需要
10 => 10　邻接　低　无　需要　6
11 => 11　本地　低　无　需要
12 => 12　本地　低　低　不需要
13 => 13　网络　高　低　不需要　5
14 => 14　网络　高　无　需要
15 => 15　邻接　高　无　不需要
16 => 16　邻接　低　低　需要
17 => 17　邻接　高　无　需要　4
18 => 18　邻接　高　低　不需要
19 => 19　本地　高　无　不需要
20 => 20　本地　低　低　需要
21 => 21　网络　高　低　需要
22 => 22　本地　高　低　不需要　3
23 => 23　网络　高　高　不需要
24 => 24　网络　低　高　需要
25 => 25　邻接　低　高　需要
26 => 26　邻接　低　高　不需要
27 => 27　本地　低　高　不需要　2
28 => 28　本地　高　无　需要
29 => 29　物理　低　无　不需要
30 => 30　网络　高　高　需要
31 => 31　邻接　高　高　不需要
32 => 32　邻接　高　低　需要
33 => 33　本地　低　高　需要
34 => 34　物理　低　无　需要
35 => 35　物理　低　低　不需要
36 => 36　本地　高　高　不需要
37 => 37　本地　高　低　需要　1
38 => 38　邻接　高　高　需要
39 => 39　物理　高　无　不需要
40 => 40　物理　低　高　不需要
41 => 41　物理　低　低　需要
42 => 42　物理　高　低　不需要
43 => 43　本地　高　高　需要
44 => 44　物理　高　无　需要
45 => 45　物理　高　高　需要
46 => 46　物理　高　高　不需要
47 => 47　物理　高　低　需要
48 => 48　物理　低　高　需要
10 => 10　1-4　8　中危
11 => 11　1-5　7　中危
12 => 12　1-7　6　中危
13 => 13　1-7　5　中危
14 => 14　2-8　4　中危
15 => 15　3-8　3　中危
16 => 16　3-9　2　中危
19 => 19　1-2　3　低危
20 => 20　1-2　2　低危
21 => 21　1-8　1　低危
1 => 1　超危　7-9　超危
2 => 2　超危　4-6　高危
3 => 3　超危　1-3　中危
4 => 4　高危　8-9　超危
6 => 6　高危　5-6　中危
7 => 7　高危　1-4　低危
10 => 10　中危　6-7　中危
11 => 11　中危　1-5　低危
13 => 13　低危　7-8　中危
14 => 14　低危　1-6　低危
[1] => [1] Common Vulnerability Scoring System v3.1: Specification Document
[2] => [2] Common Weakness Enumeration List Version 3.1

b539a80218080da56a75b624:
5. => 5. 检索机构的论文

bdff491a75c6abeda1d9c01d:
• => • Cochrane数据库：http：//www.cochranelibrary.com/，http：//www.cochranelibrary.com/about/central
• => • Pubmed数据库：https：//www.ncbi.nlm.nih.gov/pmc/
• => • Embase数据库：https：//www.elsevier.com/solutions/ embase-biomedical-research
• => • SinoMed数据库（含CBM数据库）：http：//www.sinomed. ac.cn/
• => • CNKI全文数据库：http：//www.cnki.net/
• => • 维普全文数据库：http：//lib.cqvip.com/
• => • 万方全文数据库：http：//new.wanfangdata.com.cn/index.html
• => • 临床试验数据库：如中国临床试验注册中心（http：//www.chictr.org/cn/），美国临床试验注册平台（https：//clinicaltrials.gov/）等。
• => • WHO 国际临床试验注册平台（ICTRP）：http：//www.who. int/ictrp/en/
• => • WHO 基本药物目录（EML）：http：//www.who. int/medicines/publications/essentialmedicines/en/
• => • 国家食品药品监督管理局：http：//www. nmpa.gov.cn/
• => • 国家药品不良反应监测中心：http：//www.cdr-adr.org.cn/
• => • 美国食品药品监督管理局：https：//www.fda.gov/default .htm
• => • 欧洲药品局：http：//www.ema.europa.eu/ema/
```

Counts from the observed comparison: 54fe and its byte twin each short=177/direct=225/label-only=119/missing=0; 6dc68fd6 short=49/direct=386/label-only=0/missing=0; b539 short=33/direct=13/label-only=1/missing=0; bdff short=157/direct=234/label-only=14/missing=0. Therefore label removal masks omission of visible labels (including heading numbering, table/figure numbers, bullets and row identifiers) on 134 lines per distinct document set; the huge twin is 119 per capture. The rule is firing often and on markers broader than conventional numeric list labels. It is allowed by the frozen predicate; report only, no predicate change proposed.

## Non-main-story oracle check
FIB story counts extracted from the pinned captures using the candidate's CFB/Clx parser and documented rgLw indices: `54fe` and its twin: ccpFtn=0, ccpHdd=164, ccpTxbx=0, ccpHdrTxbx=59; `6dc`: all zero; `b539`: ccpFtn=0, ccpHdd=13, ccpTxbx=66; `bdff`: ccpFtn=0, ccpHdd=152, ccpTxbx=5. Oracle text from the same soffice export contains none of the sampled non-main story windows: headers include PAGE-field instructions and document-number text; b539 textbox sample is `限定是否第一作者…限定文章发表时间…限定期刊级别…`, absent from oracle. No footnote CPs exist in any pinned document. Thus these captures do not show the oracle requiring excluded stories; however the `foothead` mutation proves the oracle's one-way inclusion check and 10% tolerance do not enforce exclusion. Empirical commands: `soffice --version` → LibreOffice 26.8.1.1; `build_oracle.py`, `analyze_lines.py`, `piece_scan.py`, `story_check.py` ran in this seat's scratch. No package/tool installation.

**VERDICT: attacked frozen C1 REAL; REAL accepts capped table-stream junk and non-main-story text (both 6/6), while the label rule rescues 119/119/0/1/14 lines; no pinned oracle evidence that excluded story text is required.**
