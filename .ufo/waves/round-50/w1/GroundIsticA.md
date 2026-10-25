# GroundIsticA — round 50 w1: ISTIC 引证检索 page re-grounded (staged S118 → lane S104)

Scope: re-ground the 引证检索 service page on disk and locate quotes for the 服务介绍 paragraph and the
委托流程 steps (incl. the 存档 step). Read-only on every repo; no network, no fetch, no production file.

## 1. Capture identity and which form carries the page text

| form | bytes | chars | sha256 |
|---|---|---|---|
| `001287c436f0e6b1d166ae8d.txt` | 5,599 | 2,288 (112 lines) | `67f6f2df8ce96d01673d8f2f740e663f55ed8324bbf804834562bf746740a1db` |
| `001287c436f0e6b1d166ae8d.raw` | 352,066 | 346,919 (UTF-8, `<meta charset="utf-8">`) | `203b16907c2c953e49bb71310df2a5fd761d3f1798115ceb2ad6881cd01c17c5` |

```
$ wc -c .../001287c436f0e6b1d166ae8d.txt .../001287c436f0e6b1d166ae8d.raw
   5599 .../001287c436f0e6b1d166ae8d.txt
 352066 .../001287c436f0e6b1d166ae8d.raw
$ python3  # sha256(url)[:24]; txt.count('<'); txt lines; raw head
key=001287c436f0e6b1d166ae8d  txt '<' count 0  txt lines 112
raw head: <!DOCTYPE html><html  data-capo=""><head><meta charset="utf-8"> … <title>科技查新检索服务平台</title>
```
The `.txt` is the page text: 2,288 chars, 112 lines, **zero** `<` — the extraction, no markup; and the cache key
`sha256(url)[:24]` for `https://chaxin.las.ac.cn/service/citation-search` is the key named above. The `.raw` is
the HTML (346,919 chars): its 委托流程 is an inline `<svg id="flow1">` whose step labels are split across
`<tspan>` nodes, e.g. `<tspan x="20" y="115">完成并审核</tspan><tspan x="20" y="155">报告</tspan>`, so **no**
flow-step string is contiguous there. **Decision: every quote below is located in the `.txt` read as UTF-8**,
each occurring exactly once (`txt=1`); the flow-step quotes are `raw=0` precisely because the raw splits them.

## 2. Located quotes (offsets are `text.find(quote)` in the `.txt` form)

| # | quote (byte-exact) | .txt off | line | chars | ws-words | txt | raw |
|---|---|---|---|---|---|---|---|
| Q1 | 论文收录引用检索（简称引证检索）指通过检索SCI、SSCI、EI、ESI、CSCD等国内外评价类数据库 | 194 | 56 | 51 | 1 | 1 | 1 |
| Q2 | 查询个人、团队等的代表性论著收录和引用情况 | 246 | 56 | 21 | 1 | 1 | 1 |
| Q3 | 为职称评定、项目申报、人才评价等需求提供客观、准确的第三方检索报告 | 268 | 56 | 33 | 1 | 1 | 1 |
| Q4 | 01 提交委托 | 319 | 59 | 7 | 2 | 1 | 0 |
| Q5 | 02 确认需求并 受理委托 | 366 | 59 | 13 | 3 | 1 | 0 |
| Q6 | 03 完成并审核 报告 06 出具正式报 告并存档 | 380 | 59 | 25 | 6 | 1 | 0 |
| Q7 | 按合作者排除自引标准统计他引次数 | 549 | 67 | 16 | 1 | 1 | 1 |

```
$ python3  # per quote: len, whitespace words, .txt count, .txt offset, .raw count
len= 51 words= 1 txt=1 off= 194 raw=1
len= 21 words= 1 txt=1 off= 246 raw=1
len= 33 words= 1 txt=1 off= 268 raw=1
len=  7 words= 2 txt=1 off= 319 raw=0
len= 13 words= 3 txt=1 off= 366 raw=0
len= 25 words= 6 txt=1 off= 380 raw=0
len= 16 words= 1 txt=1 off= 549 raw=1
```
What these locate, in the page's own words: 194–300 is one sentence — the service is 论文收录引用检索 (引证检索),
it queries SCI/SSCI/EI/ESI/CSCD **等** "and other domestic and foreign evaluation databases" (`等` makes the list
non-exhaustive), it queries a person's or team's representative works' **inclusion and citation** situation, and
it issues an **objective, accurate third-party retrieval report** for 职称评定 (title), 项目申报 (project
application) and 人才评价 (talent evaluation). 319–403 is the 委托流程 block: 01 提交委托, 02 确认需求并受理委托,
03 完成并审核报告, 04 确认报告内容, 05 缴费并填写开票信息, 06 出具正式报告并存档, 07 获取报告、下载发票.
Also located, no row emitted (each `txt=1`): `04 确认报告内 容` 327 · `05 缴费并填写 开票信息` 338 · `07 获取报告、 下载发票` 352 · `收录篇数 5 元/篇` 498 · `引用篇次 5 元/次` 511.

## 3. Machine lines

```
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	论文收录引用检索（简称引证检索）指通过检索SCI、SSCI、EI、ESI、CSCD等国内外评价类数据库	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	查询个人、团队等的代表性论著收录和引用情况	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	为职称评定、项目申报、人才评价等需求提供客观、准确的第三方检索报告	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	01 提交委托	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	02 确认需求并 受理委托	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	03 完成并审核 报告 06 出具正式报 告并存档	corpus/knowledge/istic-citation-verification-r39.md
QUOTE	S118	https://chaxin.las.ac.cn/service/citation-search	按合作者排除自引标准统计他引次数	corpus/knowledge/istic-citation-verification-r39.md
```
Checked against the assembler's own rules (`assemble-quotes.py`: 5 tab fields, `txt.count==1`, ≤25 ws-words,
≤160 chars, URL → lane id): all 7 rows are `fields=5 sid=S118 lane=S104 count=1` and inside the limits.

## 4. Findings

- **F1 — the staged entry's workflow quote is not byte-exact, in either form.** The staged
  `corpus/knowledge/istic-citation-verification-r39.md` quotes `("03 完成并审核报告 06 出具正式报告并存档")`.
  Measured: that string, `完成并审核报告`, and `出具正式报告并存档` all return **`txt=0 raw=0`**. The capture reads
  `03 完成并审核 报告 06 出具正式报 告并存档`; the space sits exactly where the raw's `<tspan>` breaks, so the
  extractor, not the page, supplies it [INFERENCE — the cause is not stated by either form].
  This is the round-49 stale-quote class on a new document. Q6 is the byte-exact replacement and is one
  contiguous slice covering **both** the review step and the 存档 step.
- **F2 — review and archive are the retrieval officer's steps, and the entry does not say so.** Raw SVG geometry:
  actor labels at `y=56` (委托方) and `y=1018` (检索员); step boxes in two rows, `y=175` and `y=660`. Row `y=175`
  holds `01/04/05/07` (submit, confirm report content, pay, collect) — the client's; row `y=660` holds `02/03/06`
  (accept, complete-and-review, issue-and-archive) — the officer's. So "the report is reviewed and archived" is
  correct but under-specified: the review (03) and the archive (06) are the institute's acts, not the requester's.
- **F3 — the staged row's English gloss drifts from the page.** S118's claim says "for title, **grant** and
  talent evaluation"; the page says 项目申报 (project application). The staged entry says "project applications"
  and is right; the row should follow the entry.
- **F4 — the entry's 服务介绍 quotation is an English translation inside quotation marks**
  (`"a person's or team's representative works and their citation situation"`) — not a capture string in either
  form. C2's `QUOTES_IN_ENTRY` leg requires each emitted quote verbatim in the entry and `QUOTES_IN_LESSON`
  requires it verbatim in `corpus/lessons/round-50.md`; Q1–Q3 must be pasted into both, byte-exact including the
  `（简称引证检索）` parenthetical.
- **F5 — the entry's 2-year reuse observation drops fees that are still charged.** The page reads
  `…本次检索可免去相同数据的费用，但要收取本次检索的开库费、复核费和证明费` (off 798–873; `复核` ×3 at 802/870/873).
  "The same data is then not re-charged" is true but incomplete: 开库费, 复核费 and 证明费 remain payable, and
  复核 is a distinct institute re-check, separate from step 03's 审核.
- **F6 — the entry's "no index snapshot" Unknown is confirmed by scan.** In the `.txt`: `版本`, `快照`, `更新时间`,
  `数据更新`, `更新日期`, `检索日期`, `覆盖`, `年限`, `2024`, `2025`, `2026` — **0 occurrences each**. No index state,
  run id or date is published, so an archived report cannot be bound to a state of SCI/SSCI/EI/ESI/CSCD.
- **F7 — the report artefact is not described in text.** `报告展示：` (off 462) is followed by image slots with no alt text or captions; the only statement of what the report contains is Q1–Q3, so the entry should rest there.
- **F8 — integration hazard in the frozen tooling (reported, not changed).** `build-spans.py:form_texts` and
  `c2-count.py:form_text` both decode a `.raw` capture as **UTF-16LE**; this capture is UTF-8. A span row bound to
  the `.raw` digest would fail `CAPTURE_BOUND`. Not triggered here (the `.txt` is tried first and all seven quotes
  are unique in it), but any page whose text exists only in the raw would trip it. Id mapping is handled:
  `assemble-quotes.py` maps this URL to lane id `S104`.
- **F9 — lane-id headroom confirmed.** `corpus/SOURCES.md` has 103 `| S…` rows, max `S103`, no `S104` row, so the planned `S104` is free and staged `S118` re-keys cleanly.

## 5. Limits

- Only the on-disk capture was read (no fetch; L0 `8d77e6c1` open), so "the page says X" means "the 2026-10-23 capture says X"; whether an archived report matches the 服务介绍 promise is unobservable (the 报告展示 gallery carries no text).
- I did not run `c2-count.py` or `build-spans.py`: `corpus/evidence/round50/spans.tsv`, `quotes.tsv`,
  `corpus/lessons/round-50.md` and the lane entry `corpus/knowledge/istic-citation-verification-r39.md` do not
  exist yet in the lane tree (`ls` → "No such file or directory"), so the counter has nothing to read on the
  ISTIC leg this wave. A state observation, not a verdict on the frozen counter.
- No installs or upgrades; no pacman transaction (host-wide pause respected). Scratch
  `/dev/shm/chousa-r50-GroundIsticA/` deleted; the only write is this report.

VERDICT: attacked the staged S118 re-grounding — the page text is the 5,599-byte `.txt` (2,288 chars, no markup) while the 352,066-byte `.raw` is UTF-8 HTML that splits every 委托流程 label across SVG `<tspan>`s; seven quotes are located exactly once at offsets 194/246/268/319/366/380/549, and the staged entry's `"03 完成并审核报告 06 出具正式报告并存档"` is refuted as byte-exact (`txt=0 raw=0`; capture reads `03 完成并审核 报告 06 出具正式报 告并存档`, Q6), with review and archive shown by SVG geometry to be the 检索员's steps.
