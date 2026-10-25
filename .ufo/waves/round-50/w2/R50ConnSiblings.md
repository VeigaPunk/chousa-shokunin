# R50 Sibling-Overlap Scan (Chinese Citation-Checking Theme)

Seat: R50ConnSiblings (leaf connector) · Date: 2026-10-25 · Lane: chousa-shokunin@6a068f2 (frozen claims), L1 landed @74794db0.
Tooling: no installs (RULES.md read, pacman paused); scratch `/dev/shm/chousa-r50-R50ConnSiblings/` removed.

## 1. Evidence: Sibling-Overlap Scan Across 20 Sibling Lanes

Term set: `CNKI`, `引文核对`, `引证检索`, `chaxin`, `他引`, `自引`, `citation check`, `self-citation`, `查新`.
Target paths: 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/` (`corpus/`, `SKILL.md`, `PROVINCE.md`; chousa excluded).

### A. Chinese and Pinyin Terms (`CNKI`, `引文核对`, `引证检索`, `chaxin`, `他引`, `自引`, `查新`)
- `grep -rn -iE 'CNKI|引文核对|引证检索|chaxin|他引|自引|查新' *-shokunin/{corpus,SKILL.md,PROVINCE.md}`:
  Observed: **0 hits** across all 20 sibling corpora, 18 sibling `SKILL.md`, and 20 sibling `PROVINCE.md`.
  Zero sibling lane holds or mentions any Chinese citation index, novelty search, or CJK bibliometric terminology.

### B. Fleet-Wide `SKILL.md` and `PROVINCE.md`
- `grep -rn -iE 'citation check|self-citation' *-shokunin/{SKILL.md,PROVINCE.md}`:
  Observed: **0 hits** across all 18 sibling `SKILL.md` files and all 20 sibling `PROVINCE.md` files.

### C. Corpus Hits for English Terms (`citation check`, `self-citation`)
`grep -rn -iE 'citation check|self-citation' *-shokunin/corpus/` matched in 12 sibling lanes (0 in 8: mori, tameshi, revenger, tsukuroi, game-dev-2d, game-dev-3d; audio live test copies only; kaidoku/tabi test labels):
1. **kumitate**: `corpus/knowledge/round-close-gate.md:89,298` — "the two citation checks it does run (`COMMIT_CITED_UNRESOLVED`, `COMMIT_CITED_NOT_ANCESTOR`)"; git commit hash citation pre-checks.
2. **mado**: `corpus/lessons/round-30-verifier-spotcheck.md:129` (own-work S185→C3 self-citation attack); `round-35.md:205`, `round-36.md:106` (markdown anchor `#mistakes` check).
3. **kengaku**: `corpus/evidence/round11-fleet/r11-connector.md:23` (auditing kumitate's report-integrity `cite-check.mjs`); `corpus/lessons/round-9-aggregator-corpus-verdict.md:18` (location-qualified quote check).
4. **kaidoku**: `corpus/lessons/round-15.md:156,163` — strict citation check catching scorecard/SHONEN phrase rewording (`citation_dead@sc-arc3r2-cites-shonen`).
5. **souji**: `corpus/lessons/round-25.md:76` — cross-table citation checker (`q57=PASS`) for slice mapping.
6. **kasegi**: `corpus/lessons/round-8-aggregator-box3-coldrun.md:76` — lesson self-citation scan in SKILL.md.
7. **tabi**: `corpus/evidence/round-18/harm-at-measured.json:517`, `routed/adjacency-selftest.json:8,22` — `tabi-ref-self-citation` test fixture case label; `corpus/knowledge/state-changing-matrix-r9.md:339` (commit hash pin check).
8. **kama**: `corpus/lessons/round-1-citations.md:20` (artifact path existence check); `round-20.md:39` (git revision resolution check).
9. **kotodama**: `corpus/lessons/round-17.md:164` — internal generation graph self-reference.
10. **kake**: `corpus/lessons/round-53.md:49` — checking that cited sources are registered in `SOURCES.md`.
11. **kotoba**: `corpus/knowledge/claim-census-round12.md:161` — prompt craft citation checklist.
12. **lore**: `corpus/knowledge/2026-10-12-lore-decision-table.md:34` — relation endpoint citation check.
13. **kagi**: `corpus/README.md:43`, `lessons/round-22.md:25` — `scope-gate.sh` fail-closed registry/path citation check.
14. **audio**: `corpus/fixtures/measure_audio.py:11665` (and live test copies) — module refcount prefix check.

Semantic sense: 100% of corpus hits represent repository-internal artifact checks (git commit hashes, markdown anchors, staged registry IDs, test fixture labels). None represents bibliographic citation indexing, citation verification, or Chinese citation databases.

## 2. Sibling PROVINCE.md Authority Analysis

`grep -rn 'chousa' *-shokunin/PROVINCE.md` confirms 10 sibling lanes explicitly recognize chousa's exclusive domain:
- **kumitate** `PROVINCE.md:28`: "Research method → chousa."
- **kengaku** `PROVINCE.md:137`: "| **chousa** | research method — `corpus/QUALITY.md` and the SOURCES contract both state the question → source-hierarchy → citation-chain → claim-vs-source method stays chousa's (`chousa-shokunin/SKILL.md`); this lane holds neither method nor duplicates it |"
- **kasegi** `PROVINCE.md:47`: "- chousa — research method and source hierarchy"
- **kotoba** `PROVINCE.md:27,51`: "chousa owns claim-vs-source research method... deep-research method; kotoba cites it, never re-derives it"
- **kake** `PROVINCE.md:36`: "`chousa` owns research method and source hierarchy"
- **kagi** `PROVINCE.md:67`: "- Adjacent — report, don't absorb: chousa owns the research method (`SOURCES.md` restates neither method nor admission bar)"
- **souji** `PROVINCE.md:82`: "chousa-shokunin owns the research method and source hierarchy; souji's `corpus/SOURCES.md` applies it and does not restate it."
- **audio** `PROVINCE.md:53`: "research method (chousa)"
- **lore** `PROVINCE.md:27`: "- chousa — research method, not lore canon: `chousa-shokunin/SKILL.md`"
- **kotodama** `PROVINCE.md:19`: "general source-research method (chousa)"

Remaining sibling provinces (`kama` serving, `kaidoku` binary RE, `mori` AST, `tameshi` mutation, `revenger` decompilation, `tsukuroi` OS packaging, `game-dev-2d/3d` games, `mado` UI/dashboards, `tabi` routing) claim disjoint technical domains and hold no research-method ground.

## 3. Connector Synthesis & Proposed Move

- **Affected axes**: `depth` (primary improvement), `calibration` (secondary improvement), `operability` (unharmed).
- **Proposed move**: Codify in chousa's quality criteria (`QUALITY.md` / lesson taxonomy) an explicit distinction between:
  1. *Repository-internal citation integrity* (git commits, anchor IDs, registered source tokens — verified by lane tools like `assimilate-rows.py`, `cited-id-check.py`); and
  2. *Bibliographic citation verification* (matching citation strings against index databases like CNKI / CAS / ISTIC, evaluating 他引 vs 自引, and conducting 科技查新 novelty search — added in C2 knowledge entries `cnki-citation-check-r40.md`, `citation-matching-semantics-r41.md`, `istic-citation-verification-r39.md`).
- **Second-order effects**:
  - *Runtime*: Zero tool changes or build overhead.
  - *Contract*: Prevents future false boundary disputes when fleet gates or sibling audit tools (e.g. kumitate `cite-check.mjs`, kagi `scope-gate.sh`) search for "citation check" across the fleet.
  - *Substrate & Verification*: Protects C2's pure-Chinese grounding check (`cjk-ground-check.py`) and token rules from being inappropriately generalized to non-bibliographic internal gates.
- **Risks**: None; purely delineates semantic boundaries without mutating frozen predicates, counters, or tool interfaces.
- **Verification**: Re-run scan commands; observe zero collisions and exact conformance with sibling province deferrals.

VERDICT: Attacked sibling overlap of Chinese citation-checking theme across 20 sibling corpora, 18 SKILL.md, and 20 PROVINCE.md — survived (no overlap found; 0 domain conflicts, 10 sibling provinces explicitly defer research method to chousa).
