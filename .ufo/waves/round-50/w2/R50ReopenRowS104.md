# R50ReopenRowS104 — re-open Registry row S104

Attacked: row S104 in `corpus/SOURCES.md` (line 114) against its capture
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/001287c436f0e6b1d166ae8d.txt`
(5599 bytes, 2288 chars UTF-8; `sha256(txt)=67f6f2df…a1db` = spans.tsv manifest hash;
`sha256("https://chaxin.las.ac.cn/service/citation-search")[:24]=001287c436f0e6b1d166ae8d` = stated key)
and the frozen SOURCES contract v1 in `/home/vgpnk/Projects/shokunin/CORPUS.md`.

## 1. Shape — 11 cells, enums, opened/recheck
`awk -F'|' 'NR==114'` → NF=13 (11 cells), no `|` inside cells. Cells:
`S104 | <title> — 中国科学院文献情报中心 科技查新检索服务平台 — <URL> | docs | A | <scope> | <anchor> | <teaches> | mined | 2026-10-25 | 90d | corpus/knowledge/istic-citation-verification-r39.md`.
`docs` ∈ enum; tier `A` valid because kind is not `community`; `mined` ∈ enum;
`opened` 2026-10-25 = the day the row's author opened the on-disk capture (lesson line 8: every
re-open "accessed 2026-10-25"; stat: `.txt` mtime 2026-10-23 20:39 — the "captured 2026-10-23"
anchor claim is the capture date, not the open date; consistent). `recheck 90d` ∈ allowed cadence.
`source` is title — canonical URL: `docs` row needs a URL; URL form fine, no credentials.

## 2. Anchor — section names + date + every char N a located quote
Section names all occur in the capture: `服务介绍`×1, `委托流程`×1, `收费标准`×3, `用户须知`×1
(`grep`/`str.count` run on the .txt). Capture date stated (2026-10-23). All six cited offsets verified
by `text[off:off+60]` on the UTF-8 decode:
- char 194 → `论文收录引用检索（简称引证检索）指通过检索SCI、SSCI、EI、ESI、CSCD等国内外评价类数据库…` (quotes.tsv row 2 start)
- char 380 → `03 完成并审核 报告 06 出具正式报 告并存档` (quotes.tsv row 7)
- char 549 → `按合作者排除自引标准统计他引次数， 1 元/篇次。` (rows 9–10)
- char 735 → `对于在2年内提供检索要求相同的用户…免去相同数据的费用` (row 13)
- char 849 → `将一周之内的网络检索结果打印后到我中心进行复核，复核收费为：收录5元/篇，引用按提供论文数每篇20元` (rows 14–15)
- char 1380 → `所有文章必须包括全部作者（全拼）、标题、期刊、年、卷、页码、DOI等完整信息` (row 17)
Each ≤25 whitespace words, ≤160 chars, located once at the stated offset — all are quote starts in
`corpus/evidence/round50/quotes.tsv` S104 lines. Anchor contract satisfied.

## 3. `used-by` and `status` — exactly the citing entries
`grep -rn 'S104' corpus/knowledge/` → only `istic-citation-verification-r39.md` (`source: S104`, line 3,
plus 14 `(`S104`)` body citations); the file exists → `mined` correct, `used-by` exact.
Other `S104` tokens in `corpus/lessons/round-43-verifier-spotcheck.md:60`, `round-48.md:52,67`,
`round-49-verifier-spotcheck.md:41` refer to *other* row ids (a quarantined staged row and a scratch
renumber target), not this row — correctly absent from `used-by`. `round-50.md` names S104 only as the
new row id it records (rule-1 Gate record), not a `source:` citation — S095's precedent of listing a
lesson is not triggered.

## 4. `scope`/`teaches` against the capture
- "five indexes it queries": SCI/SSCI/EI/ESI/CSCD named at char 194 (`等国内外评价类数据库` — "five" is
  the scope's own enumeration; the page says 等, so exactly-five is the page's list, arguably floor).
- "bibliography each article must carry": char 1380 quote verified.
- "fee table that names a co-author self-citation standard": char 549 verified (标准 named, procedure not stated).
- "the archived report": `出具正式报 告并存档` char 380; `存档` occurs once, `归档`×0 — claim is "archived", held.
- "reuse and 复核 concessions … for 中国科学院 users": both under `2.针对中国科学院用户：` (char 684) — scoped correctly.
- `teaches`: single benefit sentence; its negative claim ("publishes no index snapshot or version") verified by
  sweep — `t.count()` for 版本/更新/修订/快照/snapshot/version/截至/数据更新 all 0; `re.findall` date pattern → `[]`.
- Attribution fixed, not repeated: capture contains `中国科学院`×5, `中国科学技术信息研究所`×0, `ISTIC`×0;
  row source names 中国科学院文献情报中心 correctly despite the entry filename's `istic` misnomer
  (lesson row 47 acknowledges this; the filename is staged-package lineage, outside this row's contract).

## 5. Tier challenge — A vs B
S105/S106 are B explicitly because "the content is the vendor's, the carrier a university file host"
(lesson line 132) — i.e. the *copy* is non-canonical. S104's host `chaxin.las.ac.cn` is the operator's own
platform (footer: `单 位：中国科学院文献情报中心`, `docref@mail.las.ac.cn`, `京公网安备 11010802021795号`),
so the carrier is first-party. Scope is minimal — "as the page itself states them" — making the page primary
for its own self-description (analogous to a maintainer statement). A reviewer arguing B would have to claim
a marketing page overstates its own service; the scope forecloses that by claiming only what the page states.
A is sound and consistent with the sibling rows' B rationale.

## 6. Cross-check vs `corpus/evidence/round50/spans.tsv` (peer flag R50ReopenRowS105 — resolved)
A peer flagged spans.tsv `offset` values as uniformly −80 vs capture quote offsets. Verified on S104:
all 18 S104 rows recorded = actual quote offset − 80 (e.g. recorded 114 → actual 194; 1704 → 1784),
and `spans/S104-1.txt == capture[114:114+len(span)]` byte-equal with the quote at position 80 inside.
This is `build-spans.py` by design: docstring lines 16–18 — `offset` is the *span* start (quote plus
80 chars context each side, `CONTEXT = 80`), and the located `char N` = `offset` + quote position
within the span (line 25). S106 shows the same −80 (83→3, 22511→22431, 22549→22469); S105's head row
(recorded 0, actual 48) is `max(0, off−80)` clamping. No defect in spans.tsv; the column name `offset`
is the only nit — ambiguous enough to mislead a reviewer (recorded here, not in-scope to change).

## 7. Residual observations (not defects)
- `opened` semantics: page itself was fetched 2026-10-23; author opened the capture 2026-10-25. Contract's
  "date the row's author opened the source" supports the latter; same convention as S105/S106.
- `kind docs` is the least-wrong enum for a service page (not `community`); no better fit exists.

No tools installed; no lane files mutated; scratch (`/dev/shm/s104row.txt`) removed.

VERDICT: attacked row S104 (shape, anchor offsets, used-by/status, scope/teaches grounding, attribution, tier A vs B) — survived; row sound, no change needed.
