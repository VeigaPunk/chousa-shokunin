# Round 56 lesson — chousa

author: chousa L1 (hyaku run 9, `ChousaR56`) · date: 2026-10-27 · base `e5a3795191601797613eb986b36fa0b1a73fe6a1` · freeze `41c58925580af6be22049f13cfde234c5475b858`

## Mistakes

(filled after the wave settles; see below)

## Spot-check intake

Round-55 closure (`corpus/lessons/round-55-verifier-spotcheck.md` §6) routed five items; their disposition:

1. Settle round 55's waves — the late `w1-results.json` is committed under round 55 (`e5a37951`); the 36 never-dispatched W2 items ran inside this round's single wave (names `R55W2*`, reports `.ufo/waves/round-56/w1/`), their findings integrated as round-55 corrections below.
2. C1 counter hardening — claim R56-C1 (`corpus/evidence/round56/claims.md`).
3. D3 receipt revisions — appended correction in `corpus/lessons/round-55.md` `## Corrections`; this round's report cites only receipt-header revisions.
4. D4 quarantine offset — appended correction in `corpus/lessons/round-55.md` `## Corrections` (char 1012; 994 is the sentence start).
5. `build-spans` registry class — re-registered as a gate (SKILL.md, appended row) whose gate is `corpus/evidence/round56/c1-gate.py` and whose clause coverage is R56-C1.

## Gate

### Collision check (section 10, 0–3-space pattern, scratch)

`.ufo/waves/round-56/assimilation/` (L1 commands, committed at the freeze): `reg-ids` 126 (S001–S126), `staged-ids` 114, `collisions` 45, `quarantine-slice` 24 rows (none on a theme URL). Guard proved in `guard-proof.txt`: a two-space-indented `  | S155 |` fixture row collides under the 0–3-space pattern and not under the column-zero one. Renumber by document (the URL is the evidence, the id follows it): staged S168 → S127 (https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf), staged S156 = S169 → S128 (https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf), staged S155 → S129 (https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf), staged S157 → S130 (https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf). No theme URL had a lane row before (`grep -cF` each URL in `corpus/SOURCES.md` at the base → 0).

### New rows (opened 2026-10-27 from the read-only campaign cache; campaign capture dates 2026-10-24; no fetch)

- S127 — https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf — accessed 2026-10-27 — `（9）灰色文献：未公开发表研究信息，可能包含了最新的研究成果和观点，能够研究` (char 24624).
- S128 — https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf — accessed 2026-10-27 — `（2）2024 年 6 月-8 月，工作组采用中国循证医学中心中国循证医学中心的` (char 3064).
- S129 — https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf — accessed 2026-10-27 — `灰色文献 未公开发表的研究信息，可能包含了最新的研究成果和观点           Ⅰ级    A` (char 22564).
- S130 — https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf — accessed 2026-10-27 — `二〇二〇年十一月` (char 129).

Row touched: S118 `used-by` old `corpus/knowledge/quality-control-guideline-issued-text-r48.md, corpus/knowledge/western-instrument-alignment-r50.md` → new `…, corpus/knowledge/grey-literature-field-china-r42.md`; its status (`mined`) and recheck unchanged. Held quote (manifest `corpus/evidence/round56/held/spans.tsv`): S118 `指标 2：纳入的学术研究类证据来源是否为在同行评议期刊已发表` (char 17840).

Recheck cells: the staged rows' prose rechecks (`180d — re-download …`) are normalised to `180d`; the stripped conditions are the entry's `recheck:` line.

### Assimilation set (theme: the grey-literature source row of 药品临床综合评价工作流程指南)

- admit, narrowed: staged `grey-literature-field-china-r42.md` → `corpus/knowledge/grey-literature-field-china-r42.md`. Narrowings: the platform text is a 征求意见稿 with placeholder number and dates, not an issued standard; the Ⅰ级/A grades the recommendation to use the source (the draft prints one grade for the whole list; the journal table prints one per row), not grey literature as evidence, and "the highest grade in its table" is not carried; the nhc.gov.cn guideline is the national centres' 2020 text, not "the national commission's own", and its silence is scoped to its captured form and not to the 2021 管理指南; the "three channels" inference is not carried.
- refuse: staged `grey-literature-national-route-r44.md` — reason: the same theme on an overlapping document set (its two documents are S127 and S128 here), and its claim that the national centre's documents are the guideline's "inputs" rests on a reference list this round did not bind; flip: a round that binds the note's reference list by document and an issued T/CLPA text.

### Quarantine

Register rows on theme URLs: 0 (`python3 corpus/evidence/round56/c2-count.py` prints `QUARANTINE_VERDICTS=0/0`; the 24-row slice is in `.ufo/waves/round-56/assimilation/quarantine-slice`, none on these URLs).

### Sweep (counts in the defined text forms: 灰色, 未公开发表, 中国循证医学中心)

S127 [1, 1, 1], S128 [0, 0, 2], S129 [1, 1, 2], S130 [0, 0, 0], S118 [0, 0, 0].

## All located quotes

| id | char | quote |
|---|---|---|
| S127 | 23826 | 药品临床综合评价工作可根据评价维度及评价方法，从多种渠道获得相关信息资料。全 |
| S127 | 24624 | （9）灰色文献：未公开发表研究信息，可能包含了最新的研究成果和观点，能够研究 |
| S127 | 24791 | （10）搜索引擎：公众/媒体关注度等补充数据。 |
| S127 | 24849 | [31,35,79-82] |
| S127 | 166 | T/CLPA XXXX—2025 |
| S127 | 360 | （征求意见稿） |
| S127 | 425 | 2025 - XX - XX 发布 |
| S127 | 8242 | 将百度等公共搜索引擎及 AI 检索工具作为补充检索。本指南为管理型指南，采用中国循证 |
| S127 | 8285 | 医学中心中国循证医学中心的证据质量分级体系，采用牛津大学循证医学中心制定的推荐强 |
| S128 | 4 | 《药品临床综合评价工作流程指南》编制说明 |
| S128 | 77 | 床综合评价中心；天津医科大学总医院提出，由中国药师协会平台立项。 |
| S128 | 3064 | （2）2024 年 6 月-8 月，工作组采用中国循证医学中心中国循证医学中心的 |
| S128 | 3105 | 证据分级体系，采用牛津大学循证医学中心制定的推荐强度分级标准对证据进行 |
| S128 | 4792 | （下简称为“管理指南”）。2022 年，国家药物和卫生技术综合评估中心（“国 |
| S129 | 10 | 药品临床综合评价工作流程指南Δ |
| S129 | 3590 | China Pharmacy 2025 Vol. 36 No. 19   ·2353· |
| S129 | 22539 | 表 10   其他研究的研究类型、研究方法及内容 |
| S129 | 22564 | 灰色文献 未公开发表的研究信息，可能包含了最新的研究成果和观点           Ⅰ级    A |
| S129 | 8950 | A        推荐，证据极有效（证据等级为Ⅰ级） |
| S129 | 748 | 研究方法建立研究证据，采用中国循证医学中心的证据分级体系进行证据分级评价，采用牛津大学循证医学中心制定的推荐强度 |
| S130 | 11 | 药品临床综合评价管理指南 |
| S130 | 103 | 国家卫生健康委药具管理中心 |
| S130 | 129 | 二〇二〇年十一月 |
| S118 | 17840 | 指标 2：纳入的学术研究类证据来源是否为在同行评议期刊已发表 |

## Census

Start: `corpus/evidence/round56/census-start.txt` (exit 0, five pre-existing W04). End: `corpus/evidence/round56/census-end.txt`.
