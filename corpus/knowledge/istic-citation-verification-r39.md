# What a Chinese Academy of Sciences citation-verification service compares, and what its own page states about self-citation

source: S104 — https://chaxin.las.ac.cn/service/citation-search — the 服务介绍 paragraph (char 194), the 委托流程 step list (char 380), the 收费标准 table (char 422, char 464, char 498, char 511, char 524, char 549) and 收费说明 items (char 662, char 684, char 697, char 735, char 788, char 849), the 用户须知 items (char 1380, char 1419, char 1784) — capture `.txt` read as UTF-8, page captured 2026-10-23
verified-at: 2026-10-25 — the seventeen quotes below re-located in the on-disk capture at the stated offsets by `python3 corpus/evidence/round50/build-spans.py` (no fetch: L0 `8d77e6c1` open)
recheck: 90d — re-open https://chaxin.las.ac.cn/service/citation-search and confirm the 其他 row still reads 按合作者排除自引标准统计他引次数， 1 元/篇次 and the 收费标准 table is unchanged; the on-disk half is `cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round50/build-spans.py --check`, which must print `STALE=0` (its `SPANS_ROWS` is the whole round-50 manifest, 67 rows at landing); this round re-located the 其他 row in the 2026-10-23 capture at char 549
ground: the round-50 theme "what a Chinese citation-checking feature compares, and which of CNKI's manuals document it" — this entry is the 中国科学院文献情报中心 引证检索 page's seat in that theme (the lane filename says istic, inherited from the staged entry: the capture names 中国科学院文献情报中心 three times and ISTIC and 中国科学技术信息研究所 not at all), beside `corpus/knowledge/cnki-citation-check-r40.md` and `corpus/knowledge/citation-matching-semantics-r41.md`; the CNKI self-citation rule it is compared with is described at `corpus/knowledge/citation-count-semantics-r37.md`. One document is cited here, so the other entries are named by path, never by row id; every claim is scoped to this centre's service as its own page states it
adopted: round 50 from the campaign package `merge/chousa/` (staged `corpus/knowledge/istic-citation-verification-r39.md`), re-bound by document to the 中国科学院文献情报中心 引证检索 page; the staged row id is dropped and the document carries the lane's own row for this URL

#### Observation

- **The service, in its own page's words.** The page defines
  论文收录引用检索（简称引证检索）指通过检索SCI、SSCI、EI、ESI、CSCD等国内外评价类数据库，查询个人、团队等的代表性论著收录和引用情况，为职称评定、项目申报、人才评价等需求提供客观、准确的第三方检索报告。
  (char 194): five named evaluation indexes, a person's or team's
  representative works, and their 收录 and 引用, delivered as a third-party
  report (`S104`).
- **What the client must supply, per article.** 所有文章必须包括全部作者（全拼）、标题、期刊、年、卷、页码、DOI等完整信息
  (char 1380) — author (full pinyin), title, journal, year, volume, pages and DOI; an SCI or EI
  accession number is recommended but not required: 如有SCI或EI收录号，也建议提供 (char 1419) (`S104`).
- **The workflow draws two actor rows, and the last step is the client's.** The 委托流程 block puts the client's steps
  above a divider (01 提交委托, 04 确认报告内容, 05 缴费并填写开票信息, 07 获取报告、下载发票) and the retrieval officer's below it (02 确认需求并受理委托,
  03 完成并审核报告, 06 出具正式报告并存档); the text form holds the officer's two steps as 03 完成并审核 报告 06 出具正式报 告并存档
  (char 380, a contiguous slice with the capture's own spacing; the row assignment is read from the page's vector layout, not from the text)
  (`S104`).
- **The default deliverable is a printed, stamped body.** 检索报告默认提供打印盖章文件1份，且仅打印报告正文，不含附件
  (char 1784), stated under 用户须知, not as a workflow step (`S104`).
- **The fee table names a self-citation standard, and the retrieval is priced by item.** The certificate is priced
  证明费 300 元/份。提供 1 份证明，需要多份证明，增加 1 份 50 元 (char 422); the retrieval lines are 数据库检索费 10 元起 (char 464),
  收录篇数 5 元/篇 (char 498), 引用篇次 5 元/次 (char 511) and 期刊影响因子及分区 5 元/指标 (char 524); and the 其他 row prices the non-self count as
  按合作者排除自引标准统计他引次数， 1 元/篇次 (char 549) (`S104`).
- **Concessions are listed under 收费说明, and the second group is for 中国科学院 users.** Item 1 is 1.委托5篇以内收录检索，检索费300元。 (char 662);
  item 2 is headed 2.针对中国科学院用户： (char 684) and lists a citation price, （1）引用检索费：3元/次（1-200次），2元/次（200次以上） (char 697), a repeat-commission concession,
  对于在2年内提供检索要求相同的用户进行多次委托时，用户在提供上次检索结果同时，本次检索可免去相同数据的费用 (char 735) with the retained fees
  ，但要收取本次检索的开库费、复核费和证明费 (char 788), and a 复核 route,
  将一周之内的网络检索结果打印后到我中心进行复核，复核收费为：收录5元/篇，引用按提供论文数每篇20元 (char 849), in which a 科学院合法用户 searches SCI, EI or ISTP on the centre's or institute's network and brings a week-old printout (`S104`).

#### Inference

- **The comparison this page describes runs between a client's bibliography and index records, at the level of a whole article list, and is priced by item.** Each article must arrive with `所有文章必须包括全部作者（全拼）、标题、期刊、年、卷、页码、DOI等完整信息` (`char 1380`), and the table prices the work line by line: `数据库检索费 10 元起` (`char 464`), `收录篇数 5 元/篇` (`char 498`), `引用篇次 5 元/次` (`char 511`) and `期刊影响因子及分区 5 元/指标` (`char 524`). The two 300 figures are different lines: `1.委托5篇以内收录检索，检索费300元。` (`char 662`) is a flat fee for a 收录 commission of five works or fewer, and `证明费 300 元/份。提供 1 份证明，需要多份证明，增加 1 份 50 元` (`char 422`) prices the certificate, so 300 is not the price of the whole comparison. The page states no comparison of a claim with the source it cites (`S104`).
- **The self-citation standard is invoked to price a count, and is not defined on this page.** Under 其他 the table reads `按合作者排除自引标准统计他引次数， 1 元/篇次` (`char 549`): the standard is named, the matching procedure is not, and the page never says how a reference is resolved to the work it cites. The CNKI copy described at `corpus/knowledge/citation-count-semantics-r37.md` states that a reference naming any one collaborator of a co-authored work counts as a self-citation; this page names a co-author exclusion standard without defining it. One document states a boundary and the other names a standard, and neither says the two are the same rule (`S104`).
- **The report is the officer's record, and its printed form is stated elsewhere.** Review and archive are the retrieval officer's steps, `03 完成并审核 报告 06 出具正式报 告并存档` (`char 380`), and the default deliverable is `检索报告默认提供打印盖章文件1份，且仅打印报告正文，不含附件` (`char 1784`); a third-party report artefact that outlives the session is the shape the lane's support side wants, and what the page does not attach to it is the state of the indexes it was taken from (`S104`).
- **The repeat-commission concession is a supplied-result fee waiver for 中国科学院 users, not a versioned index state, and the 复核 route has the same shape.** It sits under `2.针对中国科学院用户：` (`char 684`); the fee for the same data may be waived (`对于在2年内提供检索要求相同的用户进行多次委托时，用户在提供上次检索结果同时，本次检索可免去相同数据的费用`, `char 735`) while `，但要收取本次检索的开库费、复核费和证明费` (`char 788`) is retained, and the 复核 route takes a client-supplied printout and re-checks it (`将一周之内的网络检索结果打印后到我中心进行复核，复核收费为：收录5元/篇，引用按提供论文数每篇20元`, `char 849`). The page states no free route and its only self-service shape is that route, which belongs to the same user group; the same user group is priced `（1）引用检索费：3元/次（1-200次），2元/次（200次以上）` (`char 697`) against the table's general `引用篇次 5 元/次` (`char 511`) (`S104`).

#### Unknown

- **Which state of the indexes a report is taken against is not published.** The page carries no date, version or run identifier — `grep -cE '版本|快照|snapshot|更新时间|数据日期'` over the capture prints 0 — so an archived report cannot be bound to a state of SCI, SSCI, EI, ESI or CSCD by anything this page states. The retained 复核费 on a repeat is the only hint that a repeat is re-reviewed rather than re-issued unchanged [INFERENCE].
- **How a reference is resolved to the work it cites is not stated here.** The exclusion standard appears only in a price line; `grep -c 核对` prints 0, `grep -c 匹配` prints 0, `grep -c 查重` prints 0 and `grep -cE '全文|原文'` prints 0 over the capture, so neither the comparison rule nor a duplicate check nor a full-text comparison is described. Whether 按合作者 means any co-author, or the commissioning author only, the page does not say.
- **What the 复核 route compares is not stated.** 复核 appears on one line of the capture (`grep -c 复核` prints 1, three occurrences on it), and `grep -c 逐条` prints 0, so the page does not say whether the printed output is checked record by record, by count, or against the report's own totals.
- **CNKI's own citation-checking feature is not described on this page; the lane holds it elsewhere.** This page never names the vendor: `grep -cE 'CNKI|知网'` over the capture prints 0. The 引文核对 feature is adopted this round at `corpus/knowledge/cnki-citation-check-r40.md`, and the CNKI self-citation rule this entry compares against is described at `corpus/knowledge/citation-count-semantics-r37.md`; whether CNKI applies the same co-author boundary internally is stated by neither document.
- **Whether the paid, commissioned shape bounds what can be re-checked.** The service is fee-charging and commission-only, so a lane cannot re-run it at will; whether other 查新 platforms share this price list or this exclusion standard is not stated by this page.
- **Staged material corrected on adoption.** The staged entry's Unknown that CNKI's own 引文核对 feature "remains unopened" is false in this lane this round — the feature's entry is adopted at the path named above — and the staged sentence is replaced by that pointer. The staged Inference's "two Chinese authorities ... a property of Chinese citation practice" is narrowed to what two documents state. The staged recheck claims to have re-opened the page; no fetch is permitted this round (L0 `8d77e6c1` open), so the note was re-located in the 2026-10-23 capture at char 549 instead. The staged "reviewed and archived" report is re-attributed to the retrieval officer's steps, the staged reuse provision is scoped to 中国科学院 users, the 3 元/次 citation price is scoped the same way, and the staged "300 元 buys the matching" is split into the two lines that carry 300.
