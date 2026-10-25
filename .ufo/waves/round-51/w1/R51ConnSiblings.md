# R51 Sibling-Overlap Scan (Japanese & Chinese Search-Record Theme)

Seat: R51ConnSiblings (leaf connector) · Date: 2026-10-25 · Lane: chousa-shokunin@cfe6c9f (claims frozen @d603f6f)
Tooling: no installs (RULES.md read, pacman paused); scratch `/dev/shm/chousa-r51-R51ConnSiblings/` unused/clean.

## 1. Evidence: Sibling-Overlap Scan Across 20 Sibling Lanes
Term set: `検索式`, `検索期間`, `检索策略`, `检索记录`, `search record`, `search log`, `PRISMA-S`, `searcher`, `灰色文献`, `grey literature`, `systematic review`.
Target paths: 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/` (`corpus/` and `SKILL.md`; chousa excluded).

### A. Zero-Hit Terms (0 hits across all 20 sibling corpora and SKILL.md)
Scan command: python regex over UTF-8 text files (<2MB) across all 20 sibling `corpus/` directories and `SKILL.md`.
Observed hits:
- `検索式`: 0 hits
- `検索期間`: 0 hits
- `检索策略`: 0 hits
- `检索记录`: 0 hits
- `PRISMA-S`: 0 hits
- `灰色文献`: 0 hits
- `grey literature`: 0 hits
Zero sibling lane mentions Japanese or Chinese search syntax/record terms, PRISMA-S reporting standards, or grey literature.

### B. `search record` (3 hits across 3 lanes)
1. **kagi**: `corpus/README.md:83` — `| Source registry | corpus/SOURCES.md | contract-v1 registry, study paths, bounded search record, and unopened leads |` (fleet SOURCES contract v1 table description).
2. **kotoba**: `corpus/lessons/round-66-verifier-spotcheck.md:62` — `| Round-66 reject candidate | none produced | ... §Gate + corpus/SOURCES.md search log | n/a — noted | the bounded search records 1 identified / 1 screened ...` (verb usage).
3. **kotodama**: `corpus/SOURCES.md:360` — `| S331 | National Diet Library, NDL Search record 畫圖百鬼夜行 3巻...` (NDL bibliographic catalog entry for a 1776 picture book).

### C. `searcher` (3 standalone hits; 182 substring hits inside "researcher")
- Standalone hits:
  1. **kake**: `corpus/knowledge/canonical-selection.md:48` — `and notes that the choice can follow the searcher rather than the declaration [S262]` (web search user in Google search documentation).
  2. **kotodama**: `corpus/knowledge/culture-material/sumptuary-law-rank-display.md:32` — `| England | churchwardens, "searchers," aulnagers (cloth measurers) |` (historical English cloth inspectors under 1363 Statute of Apparel).
  3. **kotodama**: `corpus/knowledge/culture-material/sumptuary-law-rank-display.md:66` — same historical apparel inspector context.
- 182 substring hits: security researchers (`kasegi`, `kake`), benchmark/ML researchers (`kengaku`), linguistic/historical researchers (`kotodama`, `tabi`).

### D. `systematic review` (13 hits across 2 lanes)
1. **kengaku**: `corpus/SOURCES.md:23` (S001 paper on LLM benchmark contamination), `corpus/SOURCES.md:30` (S008 paper on construct validity); `corpus/evidence/round11-fleet/r11-prior-art-prereg.md:121`; `corpus/evidence/round12-fleet/r12-prior-art-transport.md:136`; `corpus/knowledge/benchmark-saturation-and-lifecycle.md:34,58`; `corpus/knowledge/contamination-detection-and-transparency.md:20,54` (all citing academic literature reviews on benchmark validity).
2. **kotodama**: `corpus/SOURCES.md:676` (S721 turn-taking meta-analysis), `corpus/SOURCES.md:680` (S725 recast intervention meta-analysis); `corpus/knowledge/culture-material/music-instrument-lexicon.md:4,106` (singing-bowl sound healing review); `corpus/lessons/round-2-triage/C11.md:13` (same).

### E. `search log` (108 hits across all 20 sibling lanes)
- All 20 sibling lanes contain `## Search log` headings in `corpus/SOURCES.md`: audio:35, game-dev-2d:46, game-dev-3d:54, kagi:76, kaidoku:140, kake:183, kama:224, kasegi:62, kengaku:131, kotoba:177, kotodama:871, kumitate:187, lore:52, mado:279, mori:275, revenger:76, souji:170, tabi:133, tameshi:143, tsukuroi:225.
- References also appear in 6 `SKILL.md` files (kotoba:494, kotodama:600, mado:20, mori:229, tabi:1602, tsukuroi:1661) and lesson spotchecks.
- Semantic sense: 100% of hits denote repository maintenance under fleet kaika SOURCES contract v1 (logging internal source intake queries and inclusion/exclusion decisions), NOT literature search methodology, database query syntax, or PRISMA-S reporting standards.

## 2. Sibling PROVINCE.md Authority Analysis
10 sibling lanes explicitly recognize chousa's exclusive domain over research method and source hierarchy:
- **kumitate** `PROVINCE.md:28`: "Research method → chousa."
- **kengaku** `PROVINCE.md:137`: "| **chousa** | research method — `corpus/QUALITY.md` and the SOURCES contract both state the question → source-hierarchy → citation-chain → claim-vs-source method stays chousa's (`chousa-shokunin/SKILL.md`); this lane holds neither method nor duplicates it |"
- **kotoba** `PROVINCE.md:51`: "| chousa | adjacent ... deep-research method; kotoba cites it, never re-derives it (`corpus/QUALITY.md`: claim admission stays here, the research method stays chousa's) |"
- **kasegi** `PROVINCE.md:47`: "- chousa — research method and source hierarchy"
- **kake** `PROVINCE.md:36`: "`chousa` owns research method and source hierarchy"
- **kagi** `PROVINCE.md:67`: "chousa owns the research method (`SOURCES.md` restates neither method nor admission bar)"
- **souji** `PROVINCE.md:82`: "chousa-shokunin owns the research method and source hierarchy; souji's `corpus/SOURCES.md` applies it and does not restate it."
- **lore** `PROVINCE.md:27`: "- chousa — research method, not lore canon: `chousa-shokunin/SKILL.md`"
- **audio** `PROVINCE.md:53`: "research method (chousa)"
- **kotodama** `PROVINCE.md:19`: "general source-research method (chousa)"

Remaining 10 sibling lanes (`kama` serving, `kaidoku` binary RE, `mori` observability, `tameshi` verification fixtures, `revenger` decompilation, `tsukuroi` host OS, `game-dev-2d/3d` games, `mado` desktop UI, `tabi` browser automation) claim disjoint technical domains and hold zero research-method ground.

## 3. Connector Synthesis & Proposed Move
- **Affected axes**: `depth` (primary improvement: clear articulation of literature search reporting), `calibration` (secondary improvement: zero false cross-lane claims or conflation between repo search logs and systematic-review search records), `operability` (unharmed).
- **Proposed move**: Codify in chousa's knowledge entries and quality criteria (`QUALITY.md` / `japanese-search-record-r38.md`, `chinese-search-record-r39.md`, `japanese-search-record-r38-amendment-2026-10-23.md`) the strict taxonomy separating:
  1. *Repo source intake logs* (`## Search log` in `SOURCES.md` across all 20 lanes to record source ingestion under SOURCES contract v1); and
  2. *Systematic review search records / search documentation* (PRISMA-S reporting, 検索式 / 检索策略 syntax, limits / 検索期間, grey literature / 灰色文献, database interfaces in J-STAGE, SinoMed, JAOHFA, NIPH, JAHBS).
- **Closest sibling file**: `kotodama-shokunin/corpus/SOURCES.md` (specifically line 360, citing a National Diet Library catalog record: `NDL Search record 畫圖百鬼夜行 3巻`, and lines 676/680 citing systematic review papers; followed by `kagi-shokunin/corpus/README.md:83` mentioning "bounded search record").
- **Risks**: None; purely delineates semantic boundaries without mutating frozen predicates, counters, or tool interfaces.
- **Verification**: Re-run automated search terms; observe zero collisions and 100% province deferrals.

VERDICT: Attacked sibling overlap of Japanese/Chinese search-record theme across 20 sibling corpora and SKILL.md — no overlap (closest sibling file: kotodama-shokunin/corpus/SOURCES.md:360 [NDL Search record]); 10 sibling provinces explicitly defer research method to chousa.
