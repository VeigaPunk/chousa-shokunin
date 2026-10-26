# R51W2ConnCrossEntry — cross-entry / cross-registry consistency audit (round 51 w2)

Seat: R51W2ConnCrossEntry (leaf member; no subagents). Files read from the lane repo
`chousa-shokunin` at tip `4436e279…` (captures under the read-only `.qcache`). All
commands below ran and their output is reproduced.

## Attack surface
Three entries: `corpus/knowledge/japanese-search-record-r38.md` (JA), `chinese-search-record-r39.md` (ZH),
`japanese-search-record-r38-amendment-2026-10-23.md` (AMEND). Six registry rows S107–S112
(`corpus/SOURCES.md:117-122`), lesson `corpus/lessons/round-51.md`, README coverage/frontier,
claims + errata, staged package `merge/chousa/` (read-only; no campaign tools run).

## Method
1. Parse quotes/offsets from: (a) SOURCES.md anchor cells, (b) each entry's header `source:` line,
   (c) lesson "All located quotes" table, (d) `spans.tsv`, (e) captures (bytes re-checked with
   `text.find`; `.txt` form read as UTF-8). 2. Re-resolve every `.md` cross-reference inside the
   three entries. 3. Compare the repeated facts (offsets, counts, titles, volumes, six-docs count,
   staged-id map, refused doc) across places.

## Result: fact · place · value table

### A. S108 located-quote offset lists disagree (3 different lists)
| fact | place | value |
|---|---|---|
| S108 quote offsets | SOURCES.md:118 (anchor cell) | 3966, 4192, 4124, 4211, 4409, 36834 (6) |
| | JA entry :4 (`source: S108` line) | 3966, 4192, 4124, 4211, **4311**, 4409, 36834 (7) |
| | lesson All-located-quotes table / `spans.tsv` | 809, 1498, 3966, 4124, 4192, 4211, 4409, 36834, 36844, 36859 (10; offsets from `spans.tsv` rows S108-1..10 + `find` check, 0 mismatches) |

`4311` is a real, unique offset: capture `62be15a474e866e4bef6c9d5.txt` has `検索戦略` exactly once
(`t.count('検索戦略')` → 1; `t[4311:4311+5]` → `検索戦略`). So the JA header's list is longer than the
Registry anchor, and the quote manifest omits 4311 entirely (it is not in `spans.tsv` nor in the
lesson table). The JA header's own `located quotes` count (7) disagrees with the manifest count (10)
and with the anchor cell (6). Registry/manifest are mutually consistent; the header is the odd one.
Not caught by c2 because `ANCHOR_BOUND` verifies only anchor-cell offsets against `spans.tsv`.

### B. S107 pagination: registry cell vs source
| fact | place | value |
|---|---|---|
| S107 pages | SOURCES.md:117 | 32(2):**120-121** (2024) |
| | capture `7194acc65a18f6555e4b8893.txt` header | `日健教誌，2024; 32(2): 118–124` (three-field sentence on the page whose footer reads 122; lesson re-opened row S107 and correction line) |

Disagreement: the register states the article spans 120–121, the article itself spans 118–124.
The lesson corrects the *staged p.121 →* footer 122 but does not amend the register cell; the two
facts (pages of the article; page of the sentence) are now stated inconsistently across the same
round's files.

### C. Searcher-field naming: README contradicts the JA entry
| fact | place | value |
|---|---|---|
| Japanese academic sources name searcher? | AMEND :6 (`ground:` question); AMEND :20 (S112 only) | “searcher is not a field in this article” |
| | README.md:1105 | “the Japanese functional-foods form files 検索者 on a separate attachment **while the Japanese academic sources do not**” |
| | JA :12 (S107) | article specifies recording `誰が検索を行ったの` (char 13721) together with date/time and expression |

Contradiction: S107 is an academic source (日本健康教育学会誌, 特別報告) and explicitly names the
searcher as something to record (`誰が検索を行ったの`, char 13721); README:1105 asserts the Japanese
academic sources do not name the searcher. AMEND:20 is scoped to S112 only and does not contradict
S107; the README generalization does. (The phrase “as a field” does not rescue it: the README says
“do not [name]”, while S107 names the searcher explicitly.)

### D. S111 title orthography (minor)
| place | title |
|---|---|
| capture `42bac8830527d6f1bb125c49.txt` | `系统评价/Meta分析中文献检索报告清单(PRISMA-S)解读` (half-width parens) |
| SOURCES.md:121; lesson:51 | `系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读` (full-width parens) |

Same document, differing parenthesis width. Cosmetic; noted as the one title-form disagreement.
(`系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读` → `find` 0 in capture; half-width form → 1.)

### E. Holds (no disagreement found)
- Char counts: 21216 / 39676 / 52208 / 50952 / 1675 / 25811 identical in SOURCES.md anchor cells,
  entry headers, lesson re-opened table, and computed `len(open(key+'.txt').read())`.
- Six-documents count and staged map: lesson Gate (staged S109→S107, S110→S108, S116→S109,
  S117→S110, S119→S111, S126→S112; S125 refused) == `c2-count.py` `DOCS` == claims C2 == README.
  `env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c2-count.py` → `BOUND=6/7 REFUSED=1
  BOUND_IDS=S107..S112 ANCHOR_BOUND=6/6 C2=PASS`.
- Refused doc identity: lesson (“国立保健医療科学院 費用対効果評価 分析結果の記載様式と手引 [第2.0版] 2024年4月”),
  unzipped `word/document.xml` plain text (“医薬品及び医療機器の費用対効果評価に係る分析結果の記載様式と手引[第2.0版]国立保健医療科学院2024年4月”),
  staged S125 row (“提出様式（日本語）Reporting_Format_Jap_202404”) — same document, consistent paraphrase; no conflict.
- Journals/volumes: S109/S110 “实验动物与比较医学 2025;45(4):496-507 / 45(1):101-111”; S112
  “日本保健医療行動科学会雑誌 38(1):60-69 (2023)”; S111 “中国循证医学杂志 卷：26 期：4” — agree in
  registry, entries, lesson.
- Cross-references resolve: AMEND → `japanese-search-record-r38.md` (exists); JA → `chain-resolution-r3.md`
  (exists), `SKILL.md`, `corpus/README.md`; ZH → `PROVINCE.md`, `corpus/lessons/round-51.md`.
  Unresolved mentions (`chinese-search-log-r37-amendment-2026-10-23.md` in ZH:9; the staged path in
  AMEND:7) are documented drop-notes (the lane does not hold them), not live links.

## Verdict-relevant commands
```
python3 corpus/evidence/round51/c2-count.py   # (env -u ASSIMILATE_CITES) → C2=PASS, anchors 6/6
python3 corpus/evidence/round51/build-spans.py --check  # STALE=0 (run by peer; this seat: spans.tsv vs lesson 0 mismatches)
python3 - <<'PY'
# offset lists: SOURCES anchor vs JA header vs lesson table vs spans.tsv — see table A/B
PY
```

## VERDICT
Attacked cross-entry/cross-registry consistency of the three entries, six registry rows, lesson and
READMEME: found 3 substantive disagreements (S108 located-quote list differs between entry header /
Registry anchor / quote manifest incl. offset 4311; S107 pages “120-121” in SOURCES.md vs source's
118–124; README:1105 “Japanese academic sources do not” name searcher vs S107’s 誰が検索を行ったの),
1 cosmetic (S111 paren-width), and all other repeated facts, the staged-id map, the six-docs count,
refused-doc identity and live cross-references hold.
