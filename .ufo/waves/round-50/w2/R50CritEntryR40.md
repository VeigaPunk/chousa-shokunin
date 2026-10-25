# R50CritEntryR40 — claim-by-claim attack on `corpus/knowledge/cnki-citation-check-r40.md`

target: `corpus/knowledge/cnki-citation-check-r40.md`, blob `e691b179…`, 30 lines, landed 74794db (5 Observation / 5 Inference / 5 Unknown bullets)
capture: `e3ca8f4fdd15420b80096a75.txt` — sha256 `2197abe2…`, 83,384 bytes, 38,174 chars UTF-8, 1,944 LF, 0 CR, 57 form feeds; `.raw` and `.pdf` are the same bytes, 4,482,989, sha256 `d36191c7…`. Cache key recomputed: `printf '%s' '<source URL>' | sha256sum` → `e3ca8f4fdd15420b80096a75…` — provenance holds.

## 1. Located quotes — every one re-found, one is not a quote

`t=open(capture,encoding='utf-8').read(); t.find(q)` over every backticked span, then repeat-`find` for uniqueness:

- All 14 spans the bullets locate resolve to the claimed offset with count 1: `48, 30745, 30778, 30800, 30844, 30878, 30935, 31063, 31079, 31101, 31137, 31169, 31206, 31233`. `第一类是“没找到”` is unique at 30947 (no offset claimed). No quote exceeds 25 words / 160 chars.
- **Defect (locator).** `知网学位论文学术不端行为检测系统` occurs **57×** in the capture (first at 0) — it is the running page header, not a located quote, so the `(char 48)` in line 14 cannot locate it; char 48 locates only `更新时间：2020 年 7 月`. Smallest fix: keep the title as a name (unbackticked or marked "page header, 57×"), or quote `使用手册` (23) + `（管理员）` (33).
- **Defect (header vs body).** Line 3 lists 7 offsets (`48, 30745, 30800, 31063, 31101, 31137, 31233`, copied from SOURCES.md:115) while the body cites 14; `30778, 30844, 30878, 30935, 31079, 31169, 31206` are body-only. A reader following the header cannot find six body quotes. Fix: list all 14, or append "and the further spans named in the bullets".

## 2. Claim-by-claim

| line | claim | rests on | as worded? | defect → narrowed wording |
|---|---|---|---|---|
| 11 | "the operator pastes the to-be-checked document's reference list … and clicks 搜索" | 30745, 30778, 30800 | partly | The copy is an imperative with no actor, and the quote starts at `参考文献复制到` so `待检测文献` (the to-be-checked document) is outside it. Use the manifest's own S105-7 span `把待检测文献的参考文献复制到“引文核对”文本框` (30713) and write "the copy instructs the user to paste…". |
| 12 | "The result list has four columns" | 30844, 30878 | **no** | Unquoted derived number: the copy says `展示内容有…` (the displayed content *includes*), not that the list has exactly four columns. → "The list displays four items — `状态、篇名、作者和文献来源` — with 状态 in the first column." |
| 13 | "The first column reports whether the cited work was found and whether the citation content is correct" | quoted fragment 30935 | partly | The quoted `态共分为三种类型：` supports only the three-state half; the first-column claim rests on the unquoted sentence at **30901** (`该列表的第一列显示的是是否查找到该引用文献`). Add char 30901. |
| 13 | "the second is orange, not amber" | 31063 | yes | `橙色` 1× at 31067, `琥珀` 0× — the staged correction is right. |
| 13 | states 1–3 glosses | 30947, 31063, 31079, 31101, 31137, 31169, 31206 | yes | `一一对应` 1× at 30976; hover/red sentence verbatim. Note the third-state quote begins mid-sentence (`相同，`), dropping `判定` (31194) — the word that makes it a verdict; see line 18. |
| 14 | "title block … 更新时间：2020 年 7 月 (char 48)" | 48 | yes | Edition line correct; title not located (see §1). |
| 14 | "beside 两两比对 and 问题库"; "documents 管理员中心 子账号管理 and 校内互检" | none quoted | yes, unquoted | Supporting sentence `辅助模块主要提供了引文核\n对、两两比对和问题库功能` sits at **30696** and contains a newline, so it is unquotable under the manifest's no-newline rule. Cite char 30696 rather than leaving it bare. `管理员中心` 6×, `子账号管理` 7×, `校内互检` 14× — counts support the bullet. |
| 18 | **"The second state is a diff, not a verdict."** | 31101, 31137 | **no** | Strongest counterexample: the copy frames the column as `引文内容的正确性` (30901) and the green state as `判定该条引文与源内容相同` (31194) — the column is a correctness verdict, and the orange row is marked red. "Not a verdict" asserts a neutrality the copy does not state. → "**The orange state reports a located mismatch, not a bare incorrect flag.** … it says *which* part differs, not merely that the citation is wrong." |
| 18 | "a finer output than one correct-or-incorrect flag" | 31063–31137 | yes | Defensible from three states, but the comparison target is a hypothetical the copy never names; attribute it to the lane ("in the lane's terms, finer than…"). |
| 19 | "three states keep a coverage outcome apart from a support outcome" | 30947, 31169 | yes | Frame is the lane's, not the copy's; the second sentence already scopes to "the 2020 copy", so acceptable. |
| 20 | "result row carries the matched work" | 31233, 30878 | yes | `标识符` 0 in capture — the "no other handle" hedge holds. |
| 21 | **"closed-corpus check rather than a check against the open web"** | 30745 + sweeps | **no** | The sweep's word set does not test pools (absence of `匹配` says nothing about pools); `closed-corpus` is the lane's label and the open-web contrast is not drawn by the copy. I widened the probe: `互联网` 0, `网络` 0, `万方` 0, `维普` 0, `数据库` 0 — consistent with "no second pool", but word absence is not a statement. → "**The check names one pool, as this copy states it.** … 'closed-corpus' is the lane's label for a single named pool; the copy does not itself say the pool is closed or contrast it with the open web." |
| 22 | cross-ref to `claim-support-states-r24.md` | that file | **no** | See §4. |
| 27 | **"The matching method is not described."** | sweep `[0,0,0,0]` | **no** | The copy *does* describe matching at field granularity: record must be `一一对应` (30976) and the comparison is over `引文中有某一部分的信息` (31101). Only the mechanism is missing. → "**The match mechanism is not stated** — the copy says the record corresponds one-to-one and the comparison is part-wise, but not whether correspondence is decided by identifier, metadata or text." |
| 28 | "the 学位论文 system's own 子账号 manual is not among the captures" | none | yes | Tested against all captures, see §5. Scope is ambiguous ("the captures" = the four, or the 2,549?); say "among the 2,549 captures in `.qcache`". |
| 28 | siblings are "a different product" | titles | mostly | The copies state different product names; lineage is not stated. → "a different *named* product". |
| 29 | **"Whether every pasted reference must come back as a row is not stated"** | sweep `[0,0,0]` | **conflicts with line 13** | Line 13 says the first column reports found/not-found per citation — which presumes a row per entered citation — while line 29 says row emission is unstated. The copy's own tension is sharper: the list is `搜索到的` (30848) yet `没找到` is a state of that list and its text names `这条引文` (30972, singular). → "The copy describes the list as the found references yet makes 没找到 a state of that list for `这条引文`; the two sentences pull opposite ways, so whether an unmatched entry is listed is unresolved by the copy." |
| 30 | staged corrections (amber→橙色; 诚信档案 dropped; HTTP 000 dropped; body ids dropped) | 31063, sweep 5 | yes | All three drop-reasons verified: `橙色` 1×, `琥珀` 0×; `[0,0,0]` for `诚信档案/科研/人事`; the hntky HTTP-000 bullet is a live-fetch observation and unfetchable this round (L0 `8d77e6c1`). |
| 5 | "re-run the four sweeps in `#### Unknown`" | — | **no** | Unknown holds **five** commands (lines 26, 27, 28, 29, 30). A rechecker following this line skips one. → "the five sweeps". |
| 3 | "manual page 37 of the copy" | TOC | imprecise | TOC (`6.1 引文核对…… 37`) and footer `37` (≈31000) are right for the *start*; §6.1 runs onto printed page 38 (footer `38` ≈31542, form feed at 31012). Exactly half the located quotes are on p.38: `31063, 31079, 31101, 31137, 31169, 31206, 31233` — i.e. the second and third states. → "6.1 引文核对 (printed pages 37–38; the three-state text on p.38)". |

## 3. Unknown sweeps replayed — all five outputs match as stated

| line | command (as pasted in the entry) | stated | observed |
|---|---|---|---|
| 26 | `python3 -c "…print(t.count('未收录'), t.count('匹配'))"` | `0 0` | `0 0` |
| 27 | `print([t.count(w) for w in ['匹配','算法','字段','标识符']])` | `[0, 0, 0, 0]` | `[0, 0, 0, 0]` |
| 28 | `for f in e3ca… 2875… 275c… 0012…; do printf '%s ' "$f"; grep -c '引文核对' "$f.txt"; done` | `4`, `0`, `0`, `0` | `e3ca… 4`, `2875… 0`, `275c… 0`, `0012… 0` (loop exits 1 because `grep -c` returns 1 on zero — harmless, but a `set -e` replay would abort) |
| 29 | `print([t.count(w) for w in ['未找到','无结果','无匹配']])` | `[0, 0, 0]` | `[0, 0, 0]` |
| 30 | `print([t.count(w) for w in ['诚信档案','科研','人事']])` | `[0, 0, 0]` | `[0, 0, 0]` |

All five are keyword-absence tests. Two of them (lines 21, 27) carry claims that keyword absence cannot establish — the defects above. The other three are honest negatives.

## 4. The one cross-reference to a lane file

`corpus/knowledge/claim-support-states-r24.md` does "separate access, relevance, support and truth as four failable observations" — the Claim section says exactly that ("each separately checkable and separately failable"). Two faults in the sentence built on it:

1. "**the shape that file's observation 3 needs and does not itself supply**" reads false: the file gives observation 3 a shape — "The gate's span check is observation 3 locally, at byte granularity only: `verify-claims` proves the cited span occurs byte-exact at token boundaries … it does not evaluate entailment" (r24 §"How chousa applies it"). → "— a located-difference report; r24's observation 3 has only a byte-exact span check (SKILL.md:103-115), which locates a span but does not compare it part-wise."
2. "**keeps access and relevance (a record was found and it is the cited work)**" overclaims the copy: the orange state says a part of the citation's information *differs*, so the copy does not establish that the record **is** the cited work; and r24's relevance is "the opened content is on the claim's topic", which §6.1 never speaks to. → "keeps access (a record was found) and reports a located difference; it does not establish identity, and says nothing about a claim's topic, so the mapping stops short of r24's relevance."

## 5. Attacks that found nothing (commands and results)

- Quote offsets/uniqueness: §1 — 14/14 at the claimed offsets, count 1.
- Capture identity: `sha256sum`/`wc -c` on `.txt`, `.raw`, `.pdf` — as stated; URL→key recomputed.
- Sweep replays: §3 — 5/5 identical.
- Staged provenance: `grep -rn '9e5cdd215a414bf6b5694912018de4c8' /home/vgpnk/Projects/shokuknow/merge/chousa` — rows S124, S135, S180, S187 all name this one document, as line 7 states.
- "No 学位论文（子账号） manual among the captures": scan of all 2,549 `.txt` files for files containing both `学位论文` and `子账号` → only `e3ca…` (60/32, the 管理员 manual itself) and `2875…` (2/71, the 大学生论文管理系统（子账号） manual). Claim survives — but a keyword test alone cannot settle it; S106 carries `学位论文` twice, so the claim rests on the title block, which the entry cites.
- `spans.tsv` S105 rows: all 34 rows satisfy `capture[off:off+len(span)] == span_file` and contain the quote; the −80 vs quote-position offset is the designed `CONTEXT = 80` window (`build-spans.py:44,119-120`), not drift. (A sibling seat raised and then retracted this; I re-derived it independently.)
- `第 6 章 辅助功能` (30661, 1×), `6.2 两两比对` follows at 31262 — section placement and chapter membership hold.

## 6. Smallest safe corrections, in order

1. Line 18 headline "a diff, not a verdict" → "reports a located mismatch, not a bare incorrect flag" (the copy frames the column as 正确性 and the green state as 判定).
2. Line 21 "closed-corpus check rather than a check against the open web" → "names one pool; 'closed-corpus' is the lane's label".
3. Line 27 "The matching method is not described" → "The match mechanism is not stated" (one-to-one + part-wise are described).
4. Line 22 "does not itself supply" → "has only a byte-exact span check"; and drop "it is the cited work" from the access/relevance clause.
5. Line 29 → restate as the copy's internal tension (`搜索到的` vs `没找到` for `这条引文`), removing the conflict with line 13.
6. Line 12 "four columns" → "four displayed items, 状态 in the first column".
7. Line 5 "four sweeps" → "five sweeps"; line 3 "page 37" → "pages 37–38 (three-state text on p.38)".
8. Line 3 offset list → all 14; line 14 title → not a located quote.
9. Lines 11/13/14: add char 30713 (fuller paste span), char 30901 (first-column sentence), char 30696 (chapter intro).

Nothing here touches a predicate, target, counter or control; every correction narrows the entry to what `e3ca8f4fdd15420b80096a75.txt` states.

VERDICT — attacked every Observation/Inference/Unknown bullet of `cnki-citation-check-r40.md` against capture `e3ca8f4fdd15420b80096a75.txt` (all 14 offsets, all 5 sweeps, the r24 cross-reference, and the manifest/provenance chain): **defect found** — five overclaims ("diff, not a verdict"; "closed-corpus … rather than the open web"; "matching method is not described"; "does not itself supply"; "it is the cited work") plus a contradiction between lines 13 and 29, an unquoted "four columns", a five-vs-four sweep miscount, a page-37 locator that misses p.38 where half the quotes sit, and a 57×-repeated title presented as a located quote; quotes, capture hashes, sweep outputs and staged row numbers all survive.
