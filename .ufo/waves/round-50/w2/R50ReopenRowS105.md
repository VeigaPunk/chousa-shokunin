# R50ReopenRowS105 — re-open Registry row S105

Attacks: row `S105` in `corpus/SOURCES.md:115` against capture `…/.qcache/e3ca8f4fdd15420b80096a75.txt` (83,384 B; sha256 `2197abe27dad4a681b33bee7a6a93a46681968bc8ee88cc0c674eaccdd84f71e` — matches spans.tsv's recorded digest) and the SOURCES.md contract v1 (CORPUS.md §SOURCES.md, lines 86–147). No scratch created; nothing to clean.

## 1. Cell count, kind, status, recheck

Python parse: 13 pipe fields → 11 cells; `awk` NF==13 pattern consistent with the contract's lint (`NF!=13 {n++}`). Cell values: id `S105`, kind `docs` (valid enum), tier `B`, status `mined` (valid enum), opened `2026-10-25`, recheck `180d` (valid cadence). No `|` inside cells — the row is 1,020 chars on one line.

## 2. Anchor — section name, revision/date, every `char N` re-located

Anchor cell: `第6章 辅助功能, 6.1 引文核对 of the text capture (… pdftotext -layout of the 57-page PDF, captured 2026-10-23; update stamp 2020年7月); located quotes char 48, char 30745, char 30800, char 31063, char 31101, char 31137, char 31233`.

- Section name: capture has `第 6 章 辅助功能` at char 30661 and `6.1 引文核对` at char 30727 (heading; the `6.1` at 6868 is a TOC line, `… 37`). Row's `第6章` drops the capture's space — cosmetic only.
- Revision + date: `更新时间：2020 年 7 月` at char 48 (the edition line); file mtime `Oct 23 20:40` matches "captured 2026-10-23"; `t.count('\x0c')` → `57` confirms the 57-page claim (one formfeed per page, `pdftotext -layout` form).
- Every `char N` re-located by me, read as UTF-8, each quote occurring exactly once (`t.count(q)` → 1):
  - 48 → `更新时间：2020 年 7 月`
  - 30745 → `以“中国知网”的文献资源为核对源内容，将输入的引文内\n容进行比对…`
  - 30800 → `参考文献复制到“引文核对”文本框，点击“搜索”按钮，…`
  - 31063 → `第二类是橙色的标识（    ），表示系统经过核对已经找到了该条引文记录，`
  - 31101 → `但是引文中有某一部分的信息与源内容不同，将鼠标放到该标识上，…`
  - 31137 → `提示具体哪部分不同，列表中对应的内容也会红色提示。`
  - 31233 → `列表中的“篇名”可以点击，链接到该引用文献的详细信息。`
- The lesson's own manifest (round-50.md lines 77–113) uses these same offsets (27587, 30661, 30738, 30745, 30778, 30793, 30880, 30947, 31101, 31218, 31273 — all re-verified by me, all exact and once-only). **Side-check, resolved:** `evidence/round50/spans.tsv` records the same quotes at uniformly lower offsets (−80 tail, −48 head); that is by design, not drift — `build-spans.py` docstring lines 17–18/25 and `CONTEXT = 80` (line 44), `start = max(0, off - CONTEXT)` (line 119) make `offset` the **span's start**, with the Registry `anchor` `char N` being `offset + the quote's position in its span`. Verified myself: for S105-1/2/8/34, `capture[off:off+len(span)] == span_file` exactly, quote at span-index 80 (48 for the clamped head row). Registry `anchor char N` semantics = quote position; the row is the correct set.

## 3. scope — every clause grounded

`what CNKI's 引文核对 feature compares against and the three states it reports, as the 2020-07 administrator manual of the 学位论文学术不端行为检测系统 states them; content is the vendor's, the carrier a university file host, hence B`

- Document identity: char 0 `知网学位论文学术不端行为检测系统\n 使用手册\n （管理员）`; edition char 48 `更新时间：2020 年 7 月` → the 2020-07 administrator manual, as stated.
- "Compares against": char 30745 `以“中国知网”的文献资源为核对源内容` — CNKI's literature resources, exactly as scoped.
- "Three states": `态共分为三种类型：` char 30935; 没找到 30947; 橙色 31063; 绿色 31169. Exactly three.
- Vendor content / university carrier: the manual brands 中国知网 throughout (title block, page headers); the URL host `gs.sxu.edu.cn` is 山西大学 (a third-party file host, not cnki.net). Clause accurate.

## 4. teaches — one grounded benefit

- Definition 30738 (`引文核对是指，以“中国知网”…`), input step 30793, columns 30880 (`容有状态、篇名、作者和文献来源。`), states 30947/31063/31169, middle names the differing part 31101+31137. All re-located, all once-only.
- Absence claim verified: §6.1 body slice `t.find('6.1 引文核对',30000)=30727` … `6.2 两两比对=31262` (535 chars) counts: 匹配 0, 算法 0, 相似/相似度 0, 权重 0, 排序 0, 字段 0, 比例 0, 复制比 0, 阈值 0, 方法 0, 机制 0, 去除本人 0. Whole-capture sweeps: 匹配 0, 算法 0, 查重 0 (cross-checks r41's recheck line `38174 0 4 5 0`). The slice contains definition + input + list + states + title-link and nothing else — "publishes no matching method" holds as stated (the section's verb is 比对, which teaches does not deny).

## 5. Tier challenge (would a reviewer give a different tier?)

- Case for A: scope is document-scoped ("as the … manual states them"), and official docs are A per contract; staged S135 gave this document A ("vendor's own manual is the…") for scope "CNKI's own 引文核对 matching behaviour". Under that reading the captured copy is the primary statement.
- Case for B (what the gate chose, lesson line 132): scope phrases the referent as "what **CNKI's 引文核对 feature** compares against" — a claim about the vendor's product — while the copy is hosted on a university file host with no vendor chain of custody; fidelity of the 57-page copy to a canonical CNKI edition cannot be verified without a fetch (L0 `8d77e6c1` open). The staged rows themselves contested it (S124 B vs S135 A vs S180/S187 B for the same URL). B = "strong secondary with reproducible detail" is the honest tier under unverifiable provenance; S106 (sibling vendor manual, third-party mirror) is consistently B too.
- A reviewer could defend A, but B is not a mis-tier: it is the conservative, defensible choice and the row's scope cell discloses the reasoning ("content is the vendor's, the carrier a university file host, hence B"). No change required.

## 6. used-by / status

`grep -rln 'S105' corpus/knowledge/` → exactly `citation-matching-semantics-r41.md` and `cnki-citation-check-r40.md`; both carry `source: S105` header lines (r40:3, r41:3). used-by lists exactly those two paths, both exist → `mined` valid. Convention check: round-49 rows S096–S103 also list only the citing knowledge entries (round-49 lesson names them but is not in used-by); lessons-in-used-by exists (S040–S045, S077) but is not required — the contract says paths "of the knowledge entries or lessons citing the row" and round-50.md documents the row rather than citing it. Exactness holds.

## VERDICT

Attacked: S105 row (11 cells, anchor offsets, scope/teaches claims, tier challenge, used-by exactness) against its .txt capture and CORPUS.md contract v1 — **row survived**; every anchor `char N` re-located exactly once, scope and teaches fully grounded, tier B defensible under challenged A reading, used-by exact. No change to the row. (Side-note, not a defect: `spans.tsv`'s `offset` column is the span-block start — `start = max(0, off − 80)`, `build-spans.py:44,119` — its uniform −80/−48 vs quote positions is by design. The bare header `offset` is mildly ambiguous against the entries' `char N` quote positions, but it is frozen wave-1 evidence bytes and both counters consume it positionally (`c2-count.py:190`, `inference-ground.py:193` — verified myself), so it stays a naming note only; the semantics are already documented in the builder's docstring lines 17–18/25.)
