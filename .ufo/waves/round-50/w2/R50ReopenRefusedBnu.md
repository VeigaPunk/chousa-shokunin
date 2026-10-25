# R50ReopenRefusedBnu — re-open the refused CNKI 教师 manual (wave 2, falsify)

Seat: `R50ReopenRefusedBnu` (godspeed). Lane: chousa, round 50, wave 2. Bounds respected: only write is this report; nothing else touched, no git, no fleet/campaign tools run; scratch `/dev/shm/chousa-r50-R50ReopenRefusedBnu/` (used, deleted before close). No tool installed (tooling directive: none needed; no pacman transaction attempted).

Target: the refused CNKI 大学生论文管理系统使用手册（教师）, capture `…/.qcache/275c79d45b1e9b0fd32cef93.txt` (key = sha256(url)[:24]). Gate claims in `corpus/lessons/round-50.md:51` and refused-doc line `:53`; staged row S145 in `merge/chousa/SOURCES.append.md:70`; r41 entry `corpus/knowledge/citation-matching-semantics-r41.md`; r40 entry `corpus/knowledge/cnki-citation-check-r40.md`.

## 1. Reproduce every gate number

Command (python3, capture read UTF-8), abbreviated output:

```
len(t)=9914; t.count('引文核对')=0; t.count('核对')=0; t.count('匹配')=0;
t.count('引文')=9; t.count('标明引文')=9
引文 offsets [1260,6733,8055,8842,8863,8890,9063,9155,9415]
标明引文 offsets [1258,6731,8053,8840,8861,8888,9061,9153,9413]
all_引文_inside_标明引文=True      # every 引文 starts at 标明引文+2
t.find('教师可查看的报告单包括简洁报告单、全文（标明引文）报告单、去除本人')=8033
```

Cross-check: `wc -m` (default locale) → `9914`; `LC_ALL=C.UTF-8 wc -m` → `9914`; `sha256sum` → `8d201ed15c15709dd413d1468e45352011f03c1618c668068977bff5a9703031`. All five numbers of the Gate (9914, 0/0/0, 9-all-inside, char 8033) reproduce exactly.

No in-text version or host, command `[t.count(w) for w in ('更新时间','版本','V 5','2014','2016','http','www','.cn','.edu','bnu','sxu','seu','北京师范大学','山西大学','东南大学')]` → all 0. Domain-like regex matches are only section-number fragments (e.g. `.1` from `2.1`); version/date regex empty. Publisher credit line 8 `CNKI 科研诚信管理系统研究中心` is not a host (same attribution as S106's row).

## 2. Does the refusal reason hold?

Refused-doc reason (`lessons/round-50.md:53`): staged tier C, negative-scope only — adds only that 标明引文 is a report-sheet name, carries no in-text version or host.

(a) **Negative-scope only — holds.** The only 引文-related token is 标明引文 (9×, all inside, offsets above; §2.3.2 全文（标明引文）报告单 at 8840/8861, table-form listing at 8053, sibling mentions 9061/9153/9413). The checking feature 引文核对, 核对, 匹配, 辅助, 查重 all 0. Staged row S145's teaches column ("引文核对 and 匹配 occur zero times … what it calls 引文 is a thesis's citations, listed on a report sheet") matches the capture.

(b) **A date? No.** S105 has in-text `更新时间：2020 年 7 月` (char 48); S106 has `2014-03-10  V 5.0` in its title block (chars ~60-90) plus 日期 6×; the 教师 capture has none (all date/version tokens 0). Nothing to locate.

(c) **A role statement? Only login-flow UI framing, no knowledge content.** Unique-to-teacher tokens vs S106: `选择身份` 1 (login step `选择身份（教师）`, char ~1340) and `学校` 6 (school-picker login). S106 already carries role words (教师 69, 管理员 8, 子账号 71), and the teacher sentence at 8033 (`教师可查看的报告单包括…五种不同的形式`) restates a list S106 already documents in identical terms at chars 19279 (`其中报告单提供了简洁报告单、全文（标明引文）报告单、去除本人文献报告单、全文对照报告单及跨语言报告单五种不同的形式。`) and 20213 (`报告单分为简洁报告单、全文（标明引文）报告单、去除本人文献报告单、全文对照报告单和跨语言报告单五种不同的形式`). Every 引文-adjacent feature word in the teacher manual is also in S106: 两两比对 1/1, 去除引用文献复制比 3/3, 文献溯源 1/5, 逐一对比 1/1, 剽窃观点 2/4; conversely S106 has 相似度 1 and 文本复制检测报告单 1 that teacher lacks. The teacher manual is a content-subset of S106 modulo role framing.

(d) Flip condition not met: no lane claim requires 管理员+子账号 manuals to be supplemented by the 教师 manual, and the flip's "date and host located" cannot be fulfilled (there is no in-text date or host to locate).

## 3. Does r41 lose a supportable claim by not citing it?

- Every r41 Observation/Inference is quoted from S105/S106; none needs the 教师 manual. Inference 4 is deliberately product-level: "only the 学位论文检测系统's 管理员 copy documents it" — adding a second 大学生论文管理系统 copy without 引文核对 leaves it true.
- r41's Unknown bullet already discloses the omission: "the 教师 manual (refused this round) was not used" (`citation-matching-semantics-r41.md:29`).
- r40 already mines the only usable fact from the refused capture in its Unknown bullet 3 (`cnki-citation-check-r40.md:28`): the sweep over all four captures prints `e3ca8f4fdd15420b80096a75 4 / 28750bcdf5d36cd90a7709fb 0 / 275c79d45b1e9b0fd32cef93 0 / 001287c436f0e6b1d166ae8d 0` — i.e. the refused manual's absence of 引文核对 is already used, unbound, as negative evidence. That is exactly the "negative-scope only" use.
- The staged S145 teaches column's role-fact ("documented on the administrative side") was dropped in the admission narrowing (decision table, `lessons/round-50.md:124`), and r41's narrowed product-fact formulation needs no teacher manual. No supportable claim is lost.

## 4. Verdict

Refusal stands. All five gate numbers reproduce byte-for-byte (9914 chars; 引文核对/核对/匹配 0; 引文 9 all inside 标明引文; sentence at char 8033); the manual carries no in-text date, version or host, no 引文-related feature beyond the 标明引文 report-sheet name, and only role-framing login text that S106's identical five-report-form documentation already supersedes; r41 loses no supportable claim (its Unknown discloses the omission, r40 already uses the capture negatively).

VERDICT: attacked the refused CNKI 教师 manual gate and the r41 non-citation — refusal survived (all numbers reproduce; negative-scope-only holds; no date/host/feature lost; r41 loses no supportable claim).
