# R50CritTheme — C2's axis and expansion credit

Attacks one thing: whether adopting `cnki-citation-check-r40.md`, `citation-matching-semantics-r41.md`,
`istic-citation-verification-r39.md` is *depth*, and whether any of their ground was already held at
`3c51da7`. I changed no lane file; the only write is this report. Proposal and round-cache text changed
no contract, axis or route.

## Commands run (lane root)

1. `git grep -n -e 引文核对 -e 引证检索 -e chaxin -e CNKI 3c51da7 -- corpus` → RC=0, 24 hits: **0** for 引文核对,
   引证检索, chaxin; every CNKI/知网 hit is `citation-count-semantics-r37.md` (10, 16, 32, 40–41, 49, 62, 72, 77,
   81–83), `aggregator-vs-source-r36.md:85-86`, `lessons/round-49.md`, `SOURCES.md:110-113`, `evidence/round49/*`.
2. Base term census over `corpus/knowledge`, `git grep -l` per term: `自引 他引 引文数据库 引用量 被引` →
   `citation-count-semantics-r37.md` (+`被引` in `r36.md`); `引文核对 引证检索 核对 去除本人 复制比 学术不端` → **no file**.
3. `python3 corpus/evidence/round50/c2-count.py` → `ENTRIES=3/3 BOUND=3/4 REFUSED=1 BOUND_IDS=S104,S105,S106
   REF_ID_UNBOUND=0 NEW_GROUND=3/3 QUOTE_ROWS=55 ON_BOUND=55/55 CAPTURE_BOUND=55/55 SUBSTANCE=PASS ANCHOR_BOUND=3/3
   INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=0/0 ( ) C2=PASS`, RC=0.
4. `spans.tsv` cross-entry compare (`csv.DictReader`, tab): 55 rows; r40 21, r41 16; **8 byte-identical
   `(id, quote)` pairs sit under both entries** — `以“中国知网”的文献资源为核对源内容`, `以核对引文内容的正确性`,
   `但是引文中有某一部分的信息与源内容不同`, `各项内容都相同`, `更新时间：2020 年 7 月`, `状态、篇名、作者和文献来源`,
   `第 6 章 辅助功能`, `第一类是“没找到”`. All S105; r41 rows not in r40: 8.
5. S104 capture `001287c436f0e6b1d166ae8d.txt`: `2288 5 0 0 0 6` for len/中国科学院/中国科学技术信息研究所/ISTIC/istic/引证检索.
6. `case "$u" in *istic*)` on `https://chaxin.las.ac.cn/service/citation-search` → `URL_CONTAINS_istic=no`;
   `grep -n ISTIC istic-citation-verification-r39.md` → lines 6, 7 only.

## Held ground at BASE_REV

`citation-count-semantics-r37.md` already holds: 他引频次 queried through 中国引文数据库 (S100); the co-author
self-citation rule — a reference naming any collaborator of a co-authored work counts as self-citation (`:49`);
zero-count rows not displayed; the KNS columns 篇名/作者/刊名/发表时间/被引/下载 with their glosses (S102); the AI
panel's 来源数据库/引用量 (S103); "a number an index displays is not the paper's own number"; "a traced source and
a counter are separate evidence objects" (`:45-72`).

## Claim by claim: duplicate (no credit) vs new

| entry | claim | class |
|---|---|---|
| r40 O1–O2 | 引文核对 defined, 中国知网's own literature as checking source, paste-then-搜索; four columns 状态/篇名/作者/文献来源, 篇名 links out | **new** (adjacent to r37's KNS columns; different list, new column) |
| r40 O3–O4 | three states 没找到 / 橙色 (names the differing part) / 绿色; which copy this is (管理员, 2020-07) | **new** |
| r41 O1–O2 | definition, paste step, four columns, three states | **DUPLICATE of r40 O1–O3** (same document, same §6.1) |
| r41 O3 | §6.1 slice (535 chars) has no ranking/weight/similarity/algorithm word; 匹配 0 in 38,174 | **strengthens r40's Unknown**, which ran the same four-word sweep (`[0,0,0,0]`); the §6.2 两两比对 contrast (char 31273) is **new** |
| r41 O4–O6 | 仅去除第一作者本人文献 a folder property (S106 §2.6, S105 §3.7); the 子账号 copy has no 引文核对/辅助; the two feature texts do not meet | **new** (`去除本人`, `复制比` absent at base) |
| r39 O1–O4, O6–O9 | 引证检索 definition and five indexes; per-article bibliography; one report per commission; archived stamped report; ≤5-work price; reuse waiver under 中国科学院 heading; 复核 route; 5-working-day turnaround | **new** (term absent at base; new vendor document) |
| r39 O5 | 收费标准 其他 row prices 他引次数 按合作者排除自引标准 | **CONVERGENCE with held ground** — r37's S100 rule; the entry says so, Gate row 125 says "a second institutional authority" |

Net: r40 one new feature; r39 one new document and eight new propositions **plus one already held**; r41 four residues **and a restatement of r40's two core observations**.

## Is one document counted twice for expansion?

**Binding: no.** `by_doc` groups the four staged URLs; the SXU PDF is one document, counted once in `BOUND=3/4`, `used-by` naming both citing entries as the predicate requires.

**Entry credit: yes, once.** Two of the three entries take their core claim from the same 535-character §6.1 slice
of that one document, and 8 of r41's 16 manifest rows are byte-identical `(id, quote)` pairs r40 already carries.
r41's `anchor` offsets (30738, 30778, 30793, 30880, 30947, 31101, 31218) and r40's (30745, 30778, 30800, 30844,
30878, 30935, 31063, 31101, 31137, 31169, 31206) all land in that slice.

**Counter credit: also yes.** `TERMS = {E_R40: "引文核对", E_R41: "引文核对", E_R39: "引证检索"}`
(`c2-count.py:72`); `new_ground += g.returncode == 1 and term in texts…` (`:175-179`) gives r41 the same credit
as r40 for the same term from the same section. `NEW_GROUND=3/3` reports **three**; distinct new terms are
**two**. "Each entry holds its own term" is satisfied mechanically by a shared term — it never tests that a
term is entry-specific. The counter is frozen; this is a limit to record, because a reader takes 3/3 as three
new grounds.

## Gate consistency (strongest counterexample)

The Gate refused `citation-check-status-vocabulary-r48.md` for "repeats r40's three states on the same PDF"
(Decisions row). r41 repeats exactly that in O1–O2 and was admitted. Admitting r41 is defensible on its residue, but
the same class was a refusal ground for one staged entry and is unnamed for the other: r41's Decisions row states its
narrowing and never says which bullets are r40's, so the Gate cannot tell a reader which half earns credit.

## False provenance

`istic-citation-verification-r39.md:6` calls it "the ISTIC document's seat"; `:7` says "re-bound by document to the
ISTIC 引证检索 page". The capture names 中国科学院 5 × and 中国科学技术信息研究所 0 ×; `SOURCES.md` S104 names
"中国科学院文献情报中心 科技查新检索服务平台". The row is right, the **entry's own provenance lines** carry the
wrong institute, so the durable surface contradicts its row. Gate row 47 discloses the mismatch but attributes it to
"the path" — the URL contains no `istic`; only the staged filename does. r40 corrected its staged "amber" and 诚信档案
attribution on adoption; r39 corrected its body and not this.

## Axis verdicts

- **Depth: improved.** Three documents re-opened and bound; r40's feature definition and three-state output, r41's
  no-method negative plus §6.2 contrast, r39's service shape are propositions the lane did not hold. Nothing in the
  parts I re-opened contradicts its capture: S105 offsets 48/30661/30745/30880/31101/31218/30947 recomputed with `text.find`.
- **Expansion: improved, overstated.** Distinct new ground = 2 term-units + 1 convergence, credited 3/3;
  README:1077 also credits r41 with r40's "comparison source and verdict granularity". One document's one section
  is counted twice at entry level — a credit-accounting defect, not a claim defect: C2's frozen predicate is met,
  so the claim is not falsified, the credit is.

## Drafts (intended lane paths; not applied)

`corpus/knowledge/istic-citation-verification-r39.md:6-7` — replace both ISTIC namings (no quote, id or
counter constant moves):

```
ground: … this entry is the 中国科学院文献情报中心 引证检索 page's seat in that theme (the staged package's filename said "istic"; the capture names 中国科学院 5 × and 中国科学技术信息研究所 0 ×, so the institute label here is the page's own), beside `cnki-citation-check-r40.md` and `citation-matching-semantics-r41.md`; …
adopted: round 50 from the campaign package `merge/chousa/` (staged `istic-citation-verification-r39.md`), re-bound by document to the 中国科学院文献情报中心 引证检索 page; …
```

`corpus/lessons/round-50.md` Gate row 47 — "the path says istic" → "the staged filename says istic (the URL
carries no such label)". Decisions row `citation-matching-semantics-r41.md` — append `; expansion residue =
slice-scoped no-method sweep, §6.2 两两比对, S106 §2.6/§3.7, the product fact; its definition, paste step, four
columns and three states are r40's and earn no expansion credit (8 of 16 manifest rows byte-identical to r40's)`.

`corpus/README.md:1077` — replace "the 管理员 manual publishes a comparison source and a verdict granularity but
no matching method" with "the 管理员 manual's §6.1 slice (535 characters) publishes no matching method (匹配 0 in
38,174 characters, 算法/相似度 0) and §6.2's 两两比对 is a document-to-document comparison; the comparison source
and the three states are r40's, not re-credited here". `:1078` — append to "a fee table naming a co-author
self-citation standard": ` (a second authority for the boundary already held at citation-count-semantics-r37.md)`.

`corpus/lessons/round-50.md` named limits — add `C2's NEW_GROUND leg credits every entry carrying its assigned
term; r40 and r41 share 引文核对, so 3/3 credits two distinct terms three times. It measures term novelty, not
proposition novelty.`

VERDICT: attacked C2's depth/expansion credit — **survived on depth** (three documents, new propositions, no
contradiction in what I re-opened), **defect found on expansion credit**: one document's §6.1 credited to two entries
(8/16 of r41's manifest rows identical to r40's, `NEW_GROUND=3/3` over two distinct terms, README:1077
double-crediting), the same class the Gate used to refuse `citation-check-status-vocabulary-r48.md`, plus a false
institute label at `istic-citation-verification-r39.md:6-7`; smallest safe correction is the text edits above, none
touching a predicate, target, counter or control.
