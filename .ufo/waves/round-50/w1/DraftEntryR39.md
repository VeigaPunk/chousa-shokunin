# DraftEntryR39 — lane draft of `corpus/knowledge/istic-citation-verification-r39.md` (ISTIC 引证检索 page, lane id S104)

Seat DraftEntryR39, round 50 wave 1. My only write is this report; the draft below is text for the L1 to land.

## What I did
- Re-grounded the staged entry by document to capture `001287c436f0e6b1d166ae8d.*` (key = `sha256("https://chaxin.las.ac.cn/service/citation-search")[:24]`, re-derived). Text form: the `.txt` read as UTF-8, 2288 chars, `sha256 67f6f2df8ce9…`; each of the eleven quotes occurs there exactly once, so the UTF-16LE `.raw` form (352066 bytes, `sha256 203b1690…`) was never used.
- The entry contains `S104` and no other `S###` token; other entries are named by path (`cnki-citation-check-r40.md`, `citation-matching-semantics-r41.md`, `citation-count-semantics-r37.md`). The staged row id is dropped.
- Staged Unknown "CNKI's own 引文核对 feature remains unopened" replaced by a pointer to `corpus/knowledge/cnki-citation-check-r40.md`; "two Chinese authorities … property of Chinese citation practice" narrowed to what two documents state; the staged "same rule" reading reduced to a co-author boundary both state. I opened `citation-count-semantics-r37.md` and quote nothing from it: a quote must sit in an S104 span to pass `inference-ground`, and an S100 citation would be an unbound id under C2.
- Gates run against a scratch mirror (`/dev/shm/chousa-r50-DraftEntryR39/lane`), no production write.

## Gates and sweeps (observed output)
```
build-spans.py --root …/lane          -> eleven `QUOTE S104 char N` lines; SPANS_ROWS=11 WRITTEN=11
build-spans.py --root …/lane --check  -> SPANS_ROWS=11 STALE=0                      rc=0
inference-ground.py --entry … --spans …/spans.tsv --counts /dev/null --registry …/SOURCES.md --root …/lane
  GROUND entry=corpus/knowledge/istic-citation-verification-r39.md section=1 bullets=4 tokens=5 grounded=5
  GROUND: PASS                                                                      rc=0
quote-substance-check.py …/spans.tsv  -> IDS=1 QUOTES=11 FAILURES=0                 rc=0
grep -cE 'CNKI|知网' <cap>            -> 0
grep -cE '版本|快照|snapshot|更新时间|数据日期' <cap> -> 0
grep -c '核对' / '匹配' / '查重' / '逐条' / '全文|原文' <cap> -> 0 / 0 / 0 / 0 / 0   (grep -c exits 1 on zero)
grep -c '复核' <cap>                  -> 1
grep -c chaxin corpus/SOURCES.md      -> 0        (no existing row carries this URL)
git grep -l -e '引文核对' -e '引证检索' 3c51da77 -- corpus/knowledge -> no output, rc=1 (NEW_GROUND leg satisfiable)
grep -oE '^\| S[0-9]{3}' corpus/SOURCES.md | sort -u | tail -3 -> S101 S102 S103 (registry max; S104 is next)
```

## Machine lines — the eleven `quotes.tsv` rows (lane id in column 2)
```
QUOTE	S104	https://chaxin.las.ac.cn/service/citation-search	论文收录引用检索（简称引证检索）指通过检索SCI、SSCI、EI、ESI、CSCD等国内外评价类数据库，查询个人、团队等的代表性论著收录和引用情况，为职称评定、项目申报、人才评价等需求提供客观、准确的第三方检索报告。	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S104	https://chaxin.las.ac.cn/service/citation-search	03 完成并审核 报告 06 出具正式报 告并存档	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S104	https://chaxin.las.ac.cn/service/citation-search	证明费 300 元/份。提供 1 份证明，需要多份证明，增加 1 份 50 元	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S104	https://chaxin.las.ac.cn/service/citation-search	按合作者排除自引标准统计他引次数， 1 元/篇次	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S104	https://chaxin.las.ac.cn/service/citation-search	1.委托5篇以内收录检索，检索费300元。	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S104	https://chaxin.las.ac.cn/service/citation-search	对于在2年内提供检索要求相同的用户进行多次委托时，用户在提供上次检索结果同时，本次检索可免去相同数据的费用	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S104	https://chaxin.las.ac.cn/service/citation-search	将一周之内的网络检索结果打印后到我中心进行复核，复核收费为：收录5元/篇，引用按提供论文数每篇20元	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S104	https://chaxin.las.ac.cn/service/citation-search	出具1个检索报告即填写1项委托；需要多个检索报告，需逐个填写委托单	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S104	https://chaxin.las.ac.cn/service/citation-search	所有文章必须包括全部作者（全拼）、标题、期刊、年、卷、页码、DOI等完整信息	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S104	https://chaxin.las.ac.cn/service/citation-search	委托论文在10篇以内可在5个工作日完成报告（不含邮寄时间），超过10篇双方协商完成时间	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S104	https://chaxin.las.ac.cn/service/citation-search	检索报告默认提供打印盖章文件1份，且仅打印报告正文，不含附件	corpus/knowledge/istic-citation-verification-r39.md
```

## Registry row to append after S103 (11 cells; every `char N` is a quote offset above)
```
| S104 | 科技查新检索服务平台 — 引证检索 (Chinese Academy of Sciences Documentation and Information Center) — https://chaxin.las.ac.cn/service/citation-search | docs | A | what this institute's 引证检索 service states about its own retrieval — the five indexes it queries, the bibliography fields a client must supply, the fee table carrying the co-author non-self-count standard, the workflow, the archive and the reuse provision — as its own page states it; not CNKI's feature, not the matching algorithm, not an index snapshot | 服务介绍 (char 194), 委托流程 (char 380), 收费标准 (char 422, char 549, char 662, char 735, char 849), 用户须知 (char 1236, char 1380, char 1469, char 1784) (capture .txt) | The 引证检索 service retrieves representative works' 收录 and 引用 from SCI, SSCI, EI, ESI and CSCD for a client-supplied bibliography and issues an archived, stamped third-party report; the fee table prices a non-self count 按合作者排除自引标准统计他引次数，1 元/篇次 and the certificate at 300 元/份; a repeat commission within two years waives the same data's fee when the earlier result is supplied, and a 复核 route re-checks a client's printed search output; no index snapshot is published | mined | 2026-10-25 | 90d | corpus/knowledge/istic-citation-verification-r39.md |
```

## The draft

```md corpus/knowledge/istic-citation-verification-r39.md
# What a Chinese citation-verification service compares, and what its own page states about self-citation

source: S104 — https://chaxin.las.ac.cn/service/citation-search — the 服务介绍 paragraph (char 194), the 委托流程 step list (char 380), the 收费标准 rows (char 422, char 549, char 662, char 735, char 849), the 用户须知 items (char 1236, char 1380, char 1469, char 1784) — capture `.txt` read as UTF-8, page captured 2026-10-23
verified-at: 2026-10-25 — the eleven quotes below re-located in the on-disk capture at the stated offsets by `python3 corpus/evidence/round50/build-spans.py` (no fetch: L0 `8d77e6c1` open)
recheck: 90d — re-open https://chaxin.las.ac.cn/service/citation-search and confirm the 其他 row still reads 按合作者排除自引标准统计他引次数， 1 元/篇次 and the 收费标准 rows are unchanged; the on-disk half is `cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round50/build-spans.py --check`, which must print `SPANS_ROWS=11 STALE=0`; this round re-located that row in the 2026-10-23 capture at char 549
ground: the round-50 theme "what a Chinese citation-checking feature compares, and which of CNKI's manuals document it" — this entry is the ISTIC document's seat in that theme, beside `corpus/knowledge/cnki-citation-check-r40.md` and `corpus/knowledge/citation-matching-semantics-r41.md`; the CNKI self-citation rule it is compared with is described at `corpus/knowledge/citation-count-semantics-r37.md`. One document is cited here, so the other entries are named by path, never by row id; every claim is scoped to this institute's service as its own page states it
adopted: round 50 from the campaign package `merge/chousa/` (staged `corpus/knowledge/istic-citation-verification-r39.md`), re-bound by document to the ISTIC 引证检索 page; the staged row id is dropped and the document carries the lane's own row for this URL

#### Observation

- **The service, in its own page's words.** The page defines
  论文收录引用检索（简称引证检索）指通过检索SCI、SSCI、EI、ESI、CSCD等国内外评价类数据库，查询个人、团队等的代表性论著收录和引用情况，为职称评定、项目申报、人才评价等需求提供客观、准确的第三方检索报告。
  (char 194): five named evaluation indexes, a person's or team's
  representative works, and their 收录 and 引用, delivered as a third-party
  report (`S104`).
- **What the client must supply, per article.** 所有文章必须包括全部作者（全拼）、标题、期刊、年、卷、页码、DOI等完整信息
  (char 1380) — the commission is a bibliography whose entries carry author
  (full pinyin), title, journal, year, volume, pages and DOI; an SCI or EI
  accession number is optional (`S104`).
- **One commission, one report.** 出具1个检索报告即填写1项委托；需要多个检索报告，需逐个填写委托单
  (char 1236): the unit of work is the single report, and several reports
  need several forms (`S104`).
- **The workflow ends in an archived, stamped report.** The step list reads
  03 完成并审核 报告 06 出具正式报 告并存档 (char 380), and the default
  deliverable is 检索报告默认提供打印盖章文件1份，且仅打印报告正文，不含附件
  (char 1784) (`S104`).
- **The fee table names a self-citation standard, and it is this institute's own price list.** The certificate is priced
  证明费 300 元/份。提供 1 份证明，需要多份证明，增加 1 份 50 元 (char 422),
  and the 其他 row prices the non-self count as
  按合作者排除自引标准统计他引次数， 1 元/篇次 (char 549) (`S104`).
- **A commission of five works or fewer has its own price.** 1.委托5篇以内收录检索，检索费300元。
  (char 662) (`S104`).
- **Reuse is a supplied-result provision.** 对于在2年内提供检索要求相同的用户进行多次委托时，用户在提供上次检索结果同时，本次检索可免去相同数据的费用
  (char 735) — the same data's fee is waived, but the 收费说明 keeps the
  开库费、复核费和证明费 (`S104`).
- **The page describes a 复核 route over the client's own retrieval.** 将一周之内的网络检索结果打印后到我中心进行复核，复核收费为：收录5元/篇，引用按提供论文数每篇20元
  (char 849): a lawful academy user may search SCI, EI or ISTP from the
  institute's network, print a week's results, and bring them in for 复核
  (`S104`).
- **Turnaround is stated in working days.** 委托论文在10篇以内可在5个工作日完成报告（不含邮寄时间），超过10篇双方协商完成时间
  (char 1469) (`S104`).

#### Inference

- **The comparison this page describes runs between a client's bibliography and index records, at the level of a whole article list.** The priced unit is the commission — `1.委托5篇以内收录检索，检索费300元。` (`char 662`), one report per form (`出具1个检索报告即填写1项委托；需要多个检索报告，需逐个填写委托单`, `char 1236`) — and each article must arrive with `所有文章必须包括全部作者（全拼）、标题、期刊、年、卷、页码、DOI等完整信息` (`char 1380`), so 300 元 buys the matching of a bibliography against what SCI, SSCI, EI, ESI and CSCD record for it. The page states no comparison of a claim with the source it cites: 核对, 匹配 and 查重 occur 0 times in the capture (grep -c 核对 prints 0, grep -c 匹配 prints 0, grep -c 查重 prints 0), and 全文 and 原文 occur 0 times too (grep -cE '全文|原文' prints 0), so a claim-versus-source check is not what this document describes (`S104`).
- **The self-citation standard is invoked to price a count, and is not defined on this page.** Under 其他 the table reads `按合作者排除自引标准统计他引次数， 1 元/篇次` (`char 549`), beside a 证明费 of 300 元/份 (`char 422`): the standard is named, the matching procedure is not, and the page never says how a reference is resolved to the work it cites. What the lane can say about convergence is bounded by documents: this page states a co-author exclusion standard, and the CNKI copy described at `corpus/knowledge/citation-count-semantics-r37.md` states that a reference naming any one collaborator of a co-authored work counts as a self-citation (described there by path, not quoted here, because this entry cites one document). Two documents stating a co-author boundary is all that is established; neither says the two rules are the same rule, and neither makes it a property of Chinese citation practice (`S104`).
- **The durable object is the reviewed, archived and stamped report.** The workflow's closing steps are `03 完成并审核 报告 06 出具正式报 告并存档` (`char 380`) and the default deliverable is `检索报告默认提供打印盖章文件1份，且仅打印报告正文，不含附件` (`char 1784`); what the client pays 300 元/份 for is that certificate, not a query session. A verdict-shaped artefact outliving the session is the shape the lane's support side wants; what this page does not attach to it is the state of the indexes it was taken from (`S104`).
- **Reuse is a supplied-result waiver, not a versioned index state, and the 复核 route is the same shape.** The fee for the same data is waived when the client supplies the earlier result within two years (`对于在2年内提供检索要求相同的用户进行多次委托时，用户在提供上次检索结果同时，本次检索可免去相同数据的费用`, `char 735`), and the 复核 route takes the client's own printed search output and re-checks it in the institute's databases (`将一周之内的网络检索结果打印后到我中心进行复核，复核收费为：收录5元/篇，引用按提供论文数每篇20元`, `char 849`); both rest on an artefact the client brings, while the neighbouring 收费说明 still charges the 开库费、复核费和证明费 and prices a 引用检索 at 3 元/次 for 1-200 次 and 2 元/次 above 200 次. Neither route is a state the institute can re-enter: the page publishes no snapshot, and grep -cE '版本|快照|snapshot|更新时间|数据日期' over the capture prints 0 (`S104`).

#### Unknown

- **Which state of the indexes a report is taken against is not published.** The reuse provision implies results can differ between commissions, but the page carries no date, version or run identifier — `grep -cE '版本|快照|snapshot|更新时间|数据日期'` over the capture prints 0 — so an archived report cannot be bound to a state of SCI, SSCI, EI, ESI or CSCD by anything this page states.
- **How a reference is resolved to the work it cites is not stated here.** The exclusion standard appears only in a price line; `grep -c 核对` prints 0, `grep -c 匹配` prints 0, `grep -c 查重` prints 0 and `grep -cE '全文|原文'` prints 0 over the capture, so neither the comparison rule nor a duplicate check nor a full-text comparison is described. Whether 按合作者 means any co-author, or the commissioning author only, the page does not say.
- **What the 复核 route compares is not stated.** 复核 appears on one line of the capture (`grep -c 复核` prints 1, three occurrences on it), and `grep -c 逐条` prints 0, so the page does not say whether the printed output is checked record by record, by count, or against the report's own totals.
- **CNKI's own citation-checking feature is not described on this page; the lane holds it elsewhere.** This page never names the vendor: `grep -cE 'CNKI|知网'` over the capture prints 0. The 引文核对 feature is adopted this round at `corpus/knowledge/cnki-citation-check-r40.md`, and the CNKI self-citation rule this entry compares against is described at `corpus/knowledge/citation-count-semantics-r37.md`; whether CNKI applies the same co-author boundary internally is stated by neither document.
- **Whether the paid, commissioned shape bounds what can be re-checked.** The service is fee-charging and commission-only, so a lane cannot re-run it at will; nothing opened here states a free or self-service route to the same retrieval, and whether other 查新 platforms share this price list or this exclusion standard is not stated by this page.
- **Staged material corrected on adoption.** The staged entry's Unknown that CNKI's own 引文核对 feature "remains unopened" is false in this lane this round — the feature's entry is adopted at the path named above — and the staged sentence is replaced by that pointer. The staged Inference's "two Chinese authorities ... a property of Chinese citation practice" is narrowed to what two documents state, and its "same rule" reading is reduced to a co-author boundary that both state. The staged recheck claims to have re-opened the page; no fetch is permitted this round (L0 `8d77e6c1` open), so the note was re-located in the 2026-10-23 capture at char 549 instead, and the 90d cadence carries the re-open forward.
```

## Findings and limits
- **The frozen tool's phrase leg is inert on this capture, measured.** Running the tool's own unmodified functions on the four Inference bullets prints `1 tokens= ['300']`, `2 tokens= ['300']`, `3 tokens= ['300']`, `4 tokens= ['200', '200']`: every grounding token is a restated fee figure, because `has_two_words()` counts only ASCII-letter words and `has_two_words("按合作者排除自引标准统计他引次数， 1 元/篇次")` is `False`. So `GROUND: PASS` certifies five numerals inside located spans, not entailment; the Gate reader must judge the eleven quotes.
- **Style consequence of the same rule.** A backticked command with two ASCII words is itself a grounding token, so sweep commands are unbackticked in `#### Inference` (the tool never reads `#### Unknown`). My first draft failed `FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='grep -c 核对'` and `token='662'` for a bare `char 662`; backticking `char N` and unbackticking commands gave `GROUND: PASS`.
- **L1 hand-off:** all eleven quotes must also appear in `corpus/lessons/round-50.md` (C2 leg `QUOTES_IN_LESSON=n/n`), and the S104 row's `used-by` must be exactly `corpus/knowledge/istic-citation-verification-r39.md`.
- **Not attempted, out of scope:** `c2-count.py` end to end (needs the other two entries and the lesson), any C1 leg, any production file. No tool installed. Scratch is deleted after this report.

VERDICT: built and gate-checked the lane version of the ISTIC entry — eleven located quotes, one bound id, `GROUND: PASS`, `SUBSTANCE` 0 failures, `SPANS_ROWS=11 STALE=0` — and found the frozen inference check sees only restated figures on Chinese-only text, so its pass is a numeral check, not entailment.
