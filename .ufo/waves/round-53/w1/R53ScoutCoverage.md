# R53ScoutCoverage — coverage-map ground check (round 53 W1)

Scope: read-only. No scratch used, no fixture repo, nothing but this file written. Lane `corpus/README.md` is 1138 lines at the working tree; every held/not-held statement below is checked at BASE `5b550133d79bc09c82d8965cce2e48c2598b8c3e` with `git grep`/`git show`.

## 1. Base sweep (as assigned)

```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -l -e 'tracking record' -e 'information specialist' -e 质量控制指南 5b550133d79bc09c82d8965cce2e48c2598b8c3e -- corpus/knowledge
(no output)   rc=1
```
No lane `corpus/knowledge` file held any of the three terms at base — C2's "BASE_REV sweep" precondition is true. Registry (`corpus/SOURCES.md` at base) has 116 `S###` rows; the last, `S116` (`SOURCES.md:126`), so the package's five new documents land as S117–S121. `git grep -n -i jmla.pitt.edu | bjhea.org.cn | pharmwyp` at base over `corpus` → empty for all three; `training.cochrane.org` appears only inside `corpus/lessons/round-52.md:61` (a lesson-table cell naming a capture key, not a Registry row). No Registry row carries any of the five URLs (held already = none).

## 2. Per document: held / frontier / new ground

Capture keys (sha256(url)[:24], `.qcache`): JMLA `0ae65ac01b93119d3c2f3fed` (.txt 27,737 B); QCG PDF `16fe8487aa97b98576a0dbac` (.txt 61,909 B); notice `cfa080b4046592eb9490a82c` (.txt 2,661 B); NMPA copy `0435b64f65c3ea7ddc6bb92e` (.txt 43,744 B, 21,573 chars); Cochrane ch.4 `c9d1e74c3ac8d9eb332c9770` (.txt 211,326 B). All five on disk.

| doc (planned lane id) | held already? | frontier item | verdict |
|---|---|---|---|
| JMLA tracking-record FAQ, per-source record counts (S117) | **No document.** Adjacent: `knowledge/search-log-method-r39.md` holds S078 (Bramer et al., log-as-document); `knowledge/chinese-prisma-s-reception-r52.md` and `japanese-prisma-item-wording-r40.md` hold per-source *date*, not per-source *record count*. History: refused r43 (`corpus/lessons/round-43.md:44`, "should be reported in Column 2" not contiguous); `admit-later` r51 (`round-51.md:66`) and r52 (`round-52.md:62`, "admit in any round whose frozen by-document set names it") | `README.md:1099` (search-record field set) and `:1101` ("Non-Western field rules"; names this entry as refused once) — advances **1099** from field-*who/when* to field-*how many, per source*; does not touch `:1135` (searcher identity) | **new ground** (a previously refused document, flip met by naming it in C2's frozen set) |
| Cochrane Handbook ch.4 §4.2.1, §4.3.2 (S121) | **Chapter not held.** Handbook is held at other chapters only: ch.24 (S004, `SOURCES.md:14`), ch.2 (S008, `:18`), ch.IV (S019 `:29`, S029 `:39`), MECIR (S009), living-review guidance (S037). `information specialist` 0 knowledge files at base. Only touch: `knowledge/contextual-source-admission-r24.md`, `metadata-screen-r25.md` mention "Cochrane Handbook" in passing | `README.md:1107` (national standard for either literature — the western counterpart is the reference for the contrast) and `:1105` (searcher identity: §4.2.1 is the western role statement for the person who runs the search); `:1109` unchanged | **new ground** (new chapter of a held source family, so credit is per document, not per source) |
| National centre's issued 质量控制指南 search clauses (S118, twin S195) | **No.** `临床综合评价`, `质量控制`, `药品临床` 0 hits in `SOURCES.md`/`README.md` at base. The package says "the corpus already held a row for this guideline, quoting the draft" — I found **no** such row in the lane registry or README (see §4) | `README.md:1107` ("whether any Chinese body has issued a national standard… the round did not reach") — an issued **national-centre guideline** that governs search/screening; it neither names PRISMA (capture counts 0) nor `灰色文献` (0). Also `:1135` (no searcher field: unchanged) | **new ground**; advances 1107 for the Chinese side |
| Release notice (S119) | **No.** | `README.md:1107` only as a dated issuance fact (`发布时间：2025年01月03日`, `来源：国家卫生健康委卫生发展研究中心`, notice line text offset 501-522, `现予以发布` at 743, count 1) | **new ground, thin**: an issuance record. Credit is per document under the lane's own r52 rule (`README.md:1124`), but a second carrier of the same instrument adds no field — the lane's own r52 reasoning for S113 (`:1124`, "second carrier… earns no expansion credit") may be applied to it by the critic; I report, not decide |
| 2019 NMPA notice copy, pharmwyp (S120) | **No** (`NMPA`, `药监`, `国家药品监督`, `安全性文献`, `文献评价指导原则` 0 at base). The same regulator instrument was reached only as refused package entry `grey-literature-and-chinese-search-record-r40.md` (S130 = OLE `.doc` copy) — refused as *out of province for its spine* (regulator instrument currency), in province only for the field sentence (`round-51.md:70`, `round-52.md:64`). The pharmwyp URL is a different host/format (PDF, 43,744-B .txt) | `README.md:1101`/`:1107`; the **grey-literature field**: this copy states 收集未公开发表的文献即“灰色文献” (char 3340–3353). This is the first lane document holding a Chinese **mandate** for unpublished/grey sources — the lane's `灰色文献` hits at base are only `chinese-search-record-r39.md`, `japanese-search-record-niph-form-r52.md`, `japanese-search-record-r38-amendment-…md` | **new ground**, with a province hazard: its currency (is the 2019 guidance still in force) is NMPA/legal ground that PROVINCE says to report, never absorb. The entry `quality-control-guideline-issued-text-r48.md` uses it only as a contrast (`2019 guidance mandates 会议论文、未发表的学位论文、…`); keep it to what the capture says |

Expansion count I get: 5 documents, 0 held, so up to 5 by document (S118's twin S195 earns none: same URL, `S195`/`S185` carry the identical URL `https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf`, `SOURCES.append.md:110,120`). Realistically defensible: 3 clean (S117, S121, S118) + S120 (on theme, province-limited) + S119 (thin). C2's frozen floor (≥3 bound) is met even if S119/S120 are refused.

## 3. Frontier items advanced, with path:line

- `corpus/README.md:1099` — search-record field set: adds the *per-source record count* and the flow-diagram routing (database total vs other-methods column) — only once the "Column 2" quotes are re-cut (see §4).
- `corpus/README.md:1107` — national standard for either literature: adds an **issued Chinese national-centre guideline** (S118); the notice (S119) fixes issuance date 2025-01-03/2024-12-31 (`2024年12月31日` at notice char 920); it names no PRISMA (capture 0) and no grey-literature field (0). The statement "whether any Chinese body has issued a national standard for systematic-review reporting" remains **open**: the guideline is a drug-evaluation QC instrument, not a reporting standard — do not claim it closes 1107.
- `corpus/README.md:1105` / `:1135` — searcher identity: Cochrane §4.2.1 is the western role statement (23 hits of `information specialist` in the capture; heading "Role of the information specialist" count 2, first at char 3893); nothing in the Chinese guideline names a searcher. Advances the comparison, does not close the item.
- `corpus/README.md:1108` — imperfect search: not touched (no doc states what a record carries on failure).
- `corpus/README.md:1109`/`:1136` — Chinese PRISMA-S item text: not touched.

## 4. Capture facts that bound what an entry may claim (all commands ran; python `str.count/find` on the `.txt` read as UTF-8)

```
JMLA   'PRISMA-S also recommends reporting the number of records identified from each information source' count 0
JMLA   'number of records identified from each information source'  count 1 offset 1334
JMLA   'should be reported in Column 2'  count 0   (the r43 refusal reason stands: line-wrapped)
JMLA   'also suggests reporting an overall number for records identified'  count 0
COCH   'Role of the information specialist' 2 @3893 | '4.3.2' 3 @4094 | 'Ongoing studies and unpublished data sources' 2 @4100 | 'unpublished' 43 @4120 | 'PRISMA-S' 11 @13592
QCG    '灰色文献' 0 | 'PRISMA' 0 | '文献获取' 1 @10101 | '多个中、英文专业数据库' 1 @10366 | '所检索的数据库应包括' 0 | '质量控制指南' 2 @8 | 'Cochrane' 11 @11581
QCG    '指标 4' count 4 @16260,17080,18046,19653 — only @18046 is the Cochrane clause: '指标 4：在文献检索和筛选阶段，是否参照 Cochrane 等组织制定的' ; @16260 is '评价目标药品是否与当前决策需求相关'
NOTICE '现予以发布' 1 @743 | '2025-01-03' 0 (the notice prints 2025年01月03日 @522 and 2024年12月31日 @920) | '质量控制指南' 5 | '国家卫生健康委卫生发展研究中心' 2 @537
NMPA   '灰色文献' 5 @3340 | '会议论文' 1 @3348 | '未发表' 3 @3353 | '发表偏倚' 3 @17359 ; context lines wrap: '…收集未公开发表的文献，即“灰色文献”，如|会议论文、…灰色文|献中可能…'
```
Defects the entry drafters/scribes will hit (reported, nothing patched):
1. JMLA: both staged "column" quotes and the staged recheck sentence have 0 byte-exact hits; only `number of records identified from each information source` (offset 1334, count 1) is a single-line located quote. Round 51's lesson cites char 1334, round 52's cites 935 — I read 1334 on the current `.txt`; the lesson text `round-52.md:62` "located once at char 935" disagrees with my read (`find` → 1334, `count` → 1). Treat offset by `text.find` at build time, not by lesson text.
2. QCG: `所检索的数据库应包括多个中、英文专业数据库` crosses a PDF line break (0); cut to `数据库应包括多个中、英文专业数据库` (check count) — the in-line piece `多个中、英文专业数据库` is count 1 @10366. `指标 4` is four-fold: the staged anchor "指标 4" must be located at 18046, not the first hit.
3. Notice: staged recheck `still states the 2025-01-03 date` has 0 hits as that string; the capture form is `2025年01月03日`.
4. NMPA copy: the grey-literature definition wraps mid-word (`灰色文|献`); a whole-sentence quote fails; cut at the break.
5. The staged entry `quality-control-guideline-issued-text-r48.md` says "The corpus already held a row for this guideline, quoting the draft for comment" and "the round-13 row should be marked": the lane has no such row (0 hits for `临床综合评价` in `SOURCES.md` and `README.md` at base). That sentence is a package-only claim; if the entry keeps it, the critic should flag it as ungrounded in this lane.

## 5. Also observed (not mine to fix)

`/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round53/__pycache__/{c1,c2}-count.cpython-314.pyc` exist (counters were run by someone; untracked bytecode in the evidence directory).
The package's own S083 (the "second host `c9d1e74c…` = `training.cochrane.org`, same 210,708" cell at `round-52.md:61`) is a *package* id for the Cochrane URL; lane S083 (`SOURCES.md:93`) is an unrelated AVeriTeC paper. Planned lane id S121 for ch.4 is therefore correct, but any text quoting "S083" from the round-52 lesson means the package id.

VERDICT: ground-checked the coverage map for the five round-53 documents at BASE `5b550133` — none is held (base sweep rc=1, no output; no Registry row carries any of the five URLs), three advance README frontier items 1099/1105/1107 (S117, S121, S118), two are thin or province-limited (S119 notice, S120 NMPA copy); five capture-level defects in the staged quotes/rechecks reported for the drafters.
