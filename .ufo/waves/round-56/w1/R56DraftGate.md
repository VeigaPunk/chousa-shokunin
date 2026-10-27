# R56DraftGate — the round-56 lesson `## Gate` block (draft)

seat: scribe (leaf, no dispatch) · reads: lane work tree at `99eff0e` (C2 integration) on base `e5a37951`, freeze `41c58925`
scope: the C2 half of the lesson's `## Gate` — collision/renumber, the four new rows plus the held S118, the assimilation set, quarantine, the sweep, the quote table and the census. C1 material and the 36 `R55W2*` items are not mine and are not touched. This report is my only write.

## What I ran and saw

- `python3 corpus/evidence/round56/c2-count.py` (TMPDIR in scratch, `PYTHONDONTWRITEBYTECODE=1`) → exit 0:
  `ENTRIES=1/1 REFUSED_ENTRIES=0 · HELD_CITED=S118 HELD_BAD=0 · BOUND=4/4 (min 3) REFUSED=0 · BOUND_IDS=S127,S128,S129,S130 GUIDELINE_BOUND=yes · REF_ID_UNBOUND=0 · NEW_GROUND=1/1 · QUOTE_ROWS=23 ON_BOUND=23/23 · SPAN_IDS=4/4 · QUOTES_IN_SPAN=23/23 · QUOTES_IN_ENTRY=23/23 · QUOTES_IN_LESSON=23/23 · QUOTE_SHORT=23/23 · SPAN_CONTEXT=23/23 · CAPTURE_BOUND=23/23 · SUBSTANCE=PASS · ANCHOR_BOUND=4/4 · INFERENCE_GROUNDED=1/1 · QUARANTINE_VERDICTS=0/0 () · QUARANTINE_BLOCKED_ADOPTED=0 · C2=PASS`
- `python3 tools/build-spans.py --quotes corpus/evidence/round56/quotes.tsv --out corpus/evidence/round56 --check` → `SPANS_ROWS=23 STALE=0` (exit 0); same with `quotes-held.tsv --out …/held` → `SPANS_ROWS=1 STALE=0`.
- my own quote audit (script, not the counter): 23/23 rows occur exactly once, lie on one line, are ≤25 whitespace words and ≤160 characters, the span file is the exact slice, and `offset + span.find(quote)` equals the lesson table's `char N` for every row (23826, 24624, 24791, 24849, 166, 360, 425, 8242, 8285 / 4, 77, 3064, 3105, 4792 / 10, 3590, 22539, 22564, 8950, 748 / 11, 103, 129).
- `ls -l --time-style=+%F` on the five `.txt`: **2026-10-24** each (b27… 120,386 B, de9f… 17,547 B, 5233… 118,594 B, a42… 19,242 B, 16fe… 61,909 B).
- collision re-derivation: `reg-ids` 126 (S001–S126) ∩ `staged-ids` 114 = 45 S-ids, equal to `collisions` (S082–S126); `quarantine-slice` 24 data rows. Guard re-derived on a scratch fixture: `  | S155 | staged row |` matches `^ {0,3}\|[ \t]*(S\d{3,})` and not `^\|[ \t]*(S\d{3,})` — the two-space row is invisible to a column-zero reader.
- `git grep -l '中国循证医学中心' e5a37951 -- corpus/knowledge` → no match (exit 1); at `HEAD` → 6 occurrences in the entry. Register rows S127–S130: 11 cells, `mined`, `2026-10-27`, `180d`, `used-by` = the entry; S118's `used-by` at base = two entries, now three.
- `grep -cE 'ttbz\.org\.cn|china-pharmacy\.com|nhc\.gov\.cn/yaozs|bjhea\.org\.cn' …/absent-defect-register.md` → `0`.
- pdfplumber geometry of the S129 page 5: `表7 药品临床综合评价的信息来源情况` at x=73,top=355; its header `信息来源@45 信息内容@144 证据等级@236 推荐强度@260`; the row `灰色文献@45,top=576 / 未公开发表的研究信息…@76 / Ⅰ@241 级@246 A@268`; `表10` header at x=321,top=567 — a different column block.

## Draft: `## Gate`

### Collision check (section 10, 0–3-space pattern, scratch)

`.ufo/waves/round-56/assimilation/` (L1 commands, committed at the freeze `41c58925`; the two id sets, the collision set, the slice row count and the guard behaviour re-derived here): `reg-ids` 126 (S001–S126), `staged-ids` 114, `collisions` 45 (S082–S126, re-derived as the exact intersection), `quarantine-slice` 24 rows (none on a theme URL). Guard proved in `guard-proof.txt`: a two-space-indented `  | S155 |` fixture row collides under the 0–3-space pattern and not under the column-zero one. Renumber by document (the URL is the evidence, the id follows it; staged ids read from `merge/chousa/SOURCES.append.md` cells 1): staged S168 → S127 (https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf), staged S156 = S169 (one URL, two staged rows) → S128 (https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf), staged S155 → S129 (https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/…pdf), staged S157 → S130 (https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf).

### New rows (opened 2026-10-27 from the read-only campaign cache; captures dated 2026-10-24; no fetch)

| lane id | document | URL | text form (UTF-8 `.txt`, universal newlines) | headline quote (char) |
|---|---|---|---|---|
| S127 | 药品临床综合评价工作流程指南（2025 版）（征求意见稿）, T/CLPA XXXX—2025, 中国药师协会, served by the 全国团体标准信息平台 | https://www.ttbz.org.cn/upload/file/20250407/6387963976070960491020144.pdf | 70,038 chars, 0 U+FFFD | `（9）灰色文献：未公开发表研究信息，可能包含了最新的研究成果和观点，能够研究` (char 24624, 1 word) |
| S128 | 《药品临床综合评价工作流程指南》编制说明, the draft's explanatory note, same platform | https://www.ttbz.org.cn/upload/file/20250407/6387963977456239722441041.pdf | 7,031 chars, 0 U+FFFD | `（2）2024 年 6 月-8 月，工作组采用中国循证医学中心中国循证医学中心的` (char 3064, 5 words) |
| S129 | 药品临床综合评价工作流程指南, 中国药房 2025;36(19):2353-2365, doi 10.6039/j.issn.1001-0408.2025.19.01, journal-hosted PDF | https://journal.china-pharmacy.com/rc-pub/front/front-article/download/129333664/lowqualitypdf/%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E7%BB%BC%E5%90%88%E8%AF%84%E4%BB%B7%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B%E6%8C%87%E5%8D%97.pdf | 80,732 chars, 0 U+FFFD | `灰色文献 未公开发表的研究信息，可能包含了最新的研究成果和观点           Ⅰ级    A` (char 22564, 4 words) |
| S130 | 药品临床综合评价管理指南（试行）, 国家药物和卫生技术综合评估中心（国家卫生健康委卫生发展研究中心）and 国家卫生健康委药具管理中心, 二〇二〇年十一月, nhc.gov.cn | https://www.nhc.gov.cn/yaozs/c100098/202011/6fe336283f69438e9b46f090bc2ec6d1/files/1732786237821_21413.pdf | 6,930 chars, 0 U+FFFD | `二〇二〇年十一月` (char 129, 1 word) |
| S118 (held, opened 2026-10-26) | 药品临床综合评价质量控制指南（2024 年版 试行）, 国家药物和卫生技术综合评估中心, 二〇二四年十二月 | https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf | 27,609 chars, 0 U+FFFD | `指标 2：纳入的学术研究类证据来源是否为在同行评议期刊已发表` (char 17840, 2 words) |

Recorded form digests (`capture_sha256`, file digest of the `.txt`): S127 `23306b9f84c95b06008ab5e4a5deaeb9b0e937041f5239ec57792710480f1d5d` · S128 `7e3e3cf426a787a62b50fdae064e54ab28865a1ef5114cd0bf5687a87d2bd9d2` · S129 `beac2b7feb425a8885927850ea79ed5e916339c6f5cd4b45c3abbf1753f49b05` · S130 `71fed1a3bc95a7e1377ef86e364f0aa183f0885175c8f0dce459b818a861688f` · S118 `927ff71c6d499477c9cc7a3acf9ed7e335cd63b802850e5f39f5aa86a398d3a4`.

Row touched: S118 `used-by` `…quality-control-guideline-issued-text-r48.md, …western-instrument-alignment-r50.md` → `…, corpus/knowledge/grey-literature-field-china-r42.md`; status (`mined`), `opened` and recheck unchanged. Held manifest `corpus/evidence/round56/held/spans.tsv` (1 row, `--check` → `STALE=0`).

Recheck cells: the staged rows' prose rechecks (`180d — re-download …`, staged cells 9) are normalised to `180d`; the conditions live in the entry's `recheck:` line. Both staged conditions that the form cannot satisfy are dropped: staged S169's `中国循证医学中心的证据分级体系` occurs 0× in the note's form (the note prints `中国循证医学中心中国循证医学中心的` once, char 3087); the entry's replacement `2024 年 6 月-8 月` occurs once (char 3067). Staged S168's "the group's own published copy" is dropped — the capture is the 征求意见稿.

### Decisions (theme: the grey-literature source row of 药品临床综合评价工作流程指南)

| staged entry | documents | capture on disk | decision | reason | flip |
|---|---|---|---|---|---|
| `grey-literature-field-china-r42.md` | S168→S127, S156=S169→S128, S155→S129, S157→S130; S118 held | `b27ffd2f…`, `de9f5afc…`, `5233bf47…`, `a42feaea…`, `16fe8487…` | **admit, narrowed** | six narrowings: (1) the platform text is a 征求意见稿 with placeholder number and dates (`（征求意见稿）` char 360, `T/CLPA XXXX—2025` char 166, `2025 - XX - XX 发布` char 425), not an issued standard; (2) the grade does not single grey literature out — the journal's **表7 信息来源情况** prints Ⅰ级/A for every source row (nine rows; geometry: 灰色文献@45/top=576 with Ⅰ@241 级@246 A@268 under the 表7 header 证据等级@236/推荐强度@260), and the draft prints one grade line for the whole 7.2.3.3 list (offset 24815, after `（10）搜索引擎…` at 24791), so "the highest grade in its table" is not carried; (3) the Ⅰ级/A grades the recommendation to use the source, not unpublished studies as evidence (`A 推荐，证据极有效（证据等级为Ⅰ级）`, char 8950); (4) the centre's name is printed twice — `中国循证医学中心的证据分级体系` occurs 0× in S127 and S128, 1× in S129 (char 761) — so that phrase is bound to S129 and the other two forms are quoted as printed; (5) S130 is the two centres' 2020 text (`附件` cover, 药政司 commission), not "the national commission's own", and its silence is scoped to the 2020 capture, not to the 2021 管理指南 the note names (char 1672); (6) the "three channels" inference is not carried | an issued (not 征求意见稿) T/CLPA text, or one more capture of the 2021 管理指南 |
| `grey-literature-national-route-r44.md` | S168 (= S127), S169 (= S128) — a subset of the admitted entry's documents | not opened separately this round | **refuse** | same theme on an overlapping document set, merged by document into the r42 entry: its two documents are this round's S127 and S128, and its distinctive claims do not survive — "as normative references" misdescribes the note, whose list is headed `参考文献：` (char 5595; `规范性引用文件` 0×), and its `#### Unknown` premise ("the national centre's quality-control guideline … cannot be cited") is stale, since the lane holds a complete 42-page capture of that guideline (S118, 27,609 chars) | a round that binds the centre's own technical-guideline documents (the note's `参考文献` entries [3]–[6]) and shows them in an issued text's 规范性引用文件 clause — then it is an amendment to the r42 entry, not a new entry |

Refused documents: **none**. All four new documents are BOUND (`BOUND=4/4`, `REFUSED=0`; the counter's `nbound + refused == len(by_doc)` holds as 4 + 0 = 4), so the refusal leg is empty by construction and no `refused-doc` line is written. The refusal above is an entry refusal (recorded by the entry's `adopted:` line and the `sources-census`), not a document refusal.

### Quarantine

Register rows on theme URLs: 0 (`grep` of `…/absent-defect-register.md` for ttbz / china-pharmacy / nhc.gov.cn/yaozs / bjhea → 0; counter `QUARANTINE_VERDICTS=0/0`). The 24-row slice (`.ufo/waves/round-56/assimilation/quarantine-slice`) names none of them, so no verdict line is due and no bound document is `fabricated` or `unverifiable`.

### Sweep (counts in the defined text forms: 灰色, 未公开发表, 中国循证医学中心)

S127 [1, 1, 1] · S128 [0, 0, 2] · S129 [1, 1, 2] · S130 [0, 0, 0] · S118 [0, 0, 0] (re-counted here over all five forms; the 2020 guideline's form also holds 检索 0× and 文献 1×, and its 16 pages end at 第四章's closing sentence, so its absence claim is over a complete form).

### Census

Start: `corpus/evidence/round56/census-start.txt` (exit 0, `ok`, five pre-existing W04: S051 S053 S073 S074 S075). Rows 126 → 130. End receipt: not in the tree at this read (see finding F2).

## Draft: `## All located quotes`

Every quote ≤25 whitespace words and ≤160 characters, on one line of its defined text form, occurring there exactly once at the stated offset (`build-spans.py --check` → `SPANS_ROWS=23 STALE=0`; every row also read by an independent audit here):

| id | char | quote |
|---|---:|---|
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

(S118's held quote, `指标 2：纳入的学术研究类证据来源是否为在同行评议期刊已发表`, char 17840, sits in `held/spans.tsv`, not in the 23.)

## Findings (report-only; nothing here is patched)

- **F1 — table misattribution (entry, registry S129, lesson).** The row `灰色文献 … Ⅰ级 A` (char 22564) is a row of **表7 药品临床综合评价的信息来源情况**, not of 表10: pdfplumber puts 表7's header at x=73/top=355 with columns 信息来源@45, 信息内容@144, 证据等级@236, 推荐强度@260, and the row's cells at 灰色文献@45, Ⅰ@241, 级@246, A@268 on top=576; `表10`'s header is at x=321/top=567 in the neighbouring column block. The entry's Observation ("its `表 10 …` (char 22539) carries the row"), the S129 registry cells 4/5/6 and the entry's `recheck:` all say 表 10. The quote at char 22539 is real and unique, but it names the neighbouring table. Fix is a wording change in the entry + S129 cells 4/5/6 + the recheck line; the manifest need not change.
- **F2 — census end receipt absent.** `corpus/evidence/round56/census-end.txt` does not exist (only `census-start.txt`), so the Census paragraph above must not cite it until a seat writes it. `ls` at this read: `no such file`.
- **F3 — no C2 after-measurement receipt.** `corpus/evidence/round56/` holds `c1-measure-after.txt` but no `c2-measure-after.txt`; the `C2=PASS` above is my run at the work tree, not a committed receipt with a revision header.
- **F4 — r44 refusal reason sharpened.** The landed draft said the refusal rests on "a reference list this round did not bind"; the note *is* bound (S128) and its `参考文献：` list (char 5595) does name the centre's instruments ([3]–[6]). The surviving reasons are the subset document set, the false "normative references" wording, and the stale `Unknown` that held S118 answers.
- **F5 — the draft's single grade line is not a quotable string.** `（证据等级：I 级；推荐强度：A）` occurs 31× in S127 (and the `Ⅰ` variant 14×), so it can never be a quote row; the list-closing grade at offset 24815 (between `（10）…` 24791 and `[31,35,79-82]` 24849) is cited by offset only. Note the draft prints ASCII `I 级`, the journal prints `Ⅰ级`.
- **F6 — the "highest grade" phrasing would be empty.** Every one of 表7's source rows prints Ⅰ级/A, so the grade cannot be presented as singling grey literature out; the landed narrowing already drops the superlative and should keep dropping it.
- **F7 — settled items I re-derived and found sound.** Collision counts and the guard; the renumber map by URL; all 23 quote rows (offset/one-line/uniqueness/word and character limits, span slice exactness); the held S118 quote and span (190 chars, slice exact); the sweep counts; `QUARANTINE_VERDICTS=0/0`; the base absence of `中国循证医学中心` in `corpus/knowledge` and its 6 occurrences at `HEAD`; S118's `used-by` extension; `C2=PASS` at the work tree.

## Out of scope

C1 (gate clause coverage, the nine mutants, the two hook probes) and the 36 `R55W2*` round-55 falsify items: not attacked, not run, not verified by this seat. No network source fetch: the only egress was a tool install (`uv run --with pypdf` / `--with pdfplumber`, which pulled pypdfium2 3.6 MiB from PyPI into the uv cache; no PATH directory, no `~/.local/bin` write, no pacman).

VERDICT: drafted and independently re-derived the round-56 lesson `## Gate` (collision/renumber, rows S127–S130 + held S118, admit-narrowed r42 / refuse r44, 23 quotes, sweep, quarantine) — C2's predicate survived my attack (`C2=PASS`, 23/23 on every quote leg), with seven findings, two of which are content defects (F1 表7/表10 attribution, F2 missing census end receipt).
