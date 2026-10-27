# R58ConnectorSiblingScope — cross-lane bibliography / citation / identifier scan (round 58, w1)

Seat: R58ConnectorSiblingScope (leaf; adjacency). Lane root: /home/vgpnk/Projects/shokunin/chousa-shokunin. Frozen commit 9e73a031ab1ac3bac343de008850d7d87f9e5634; claim base b13ca7b5c8bbb40d2d29a37fb443c64ca043f791.
Not opened by this seat: claims.md, c1-count.py, c2-count.py, controls, quotes.tsv, the S101 capture. C1/C2 are not judged here. Read-only throughout; no git/jj; no installs (none needed); no live fetch; scratch dir created and removed.

## 1. Scope and terms
Inventory: `glob /home/vgpnk/Projects/shokunin/*/PROVINCE.md` → 21 files: audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi.

Terms searched (case-insensitive unless stated):
- citation/bibliography: `bibliograph`, `citation`, `\bcite`, `reference list`, `ISO 690`, `GB/T`, `7714`, `APA|MLA|IEEE|Chicago|Harvard|Vancouver`, `BibTeX|CSL|Zotero`
- identifiers: `DOI`, `ISBN`, `ISSN`, `PMID`, `arXiv`, `permalink`, `Wayback`, `archive.org`, `SOURCES`, `S\d{3}`, `evidence_id`, `Evidence ID`, `sha256`, `capture`
- Chinese registries: `CNKI|CiNii|J-STAGE|SAMR|openstd`
- source evaluation: `source hierarchy`, `primary/secondary source`, `aggregator`, `unsourced`, `reliab`, `credib`, `grading`, `tier`
Also read: chousa PROVINCE.md (17 lines, full); fleet CORPUS.md:64-148; .ufo/waves/kaika/SOURCES-CONTRACT-v1.md (81 lines); PROTOCOL.md:435; chousa SKILL.md:17-35; chousa corpus/README.md:51-54, 1071-1072, 1169-1173; chousa corpus/QUALITY.md:24-27; chousa corpus/SOURCES.md:11-16, 111.

## 2. Results

### 2.1 Shared fleet SOURCES contract (adjacency; no conflict)
- CORPUS.md:64 `## SOURCES.md — where a shokunin learns` carries "Contract v1 (kaika, 2026-10-19, frozen)". Rule 3 (CORPUS.md:119-122): "the research method stays chousa's (`chousa-shokunin/SKILL.md`: question → source hierarchy → citation chain → claim-vs-source check)".
- Command: `diff <(awk 'NR>=3&&NR<=81' SOURCES-CONTRACT-v1.md) <(awk 'NR>=70&&NR<=148' CORPUS.md)` output:
```
7c7
< ## Shape
---
> ### Shape
41c41
< ## Rules
---
> ### Rules
62c62
< ## Census — run from the lane root (tested 2026-10-19 on a synthetic table)
---
> ### Census — run from the lane root (tested 2026-10-19 on a synthetic table)
```
  Result: 79 lines each; rule text identical; only heading depth differs.
- `sha256sum .ufo/waves/kaika/SOURCES-CONTRACT-v1.md` → `6c674a2281afb75b2de11790ebfe34fdcf7ddde61a6734d2eca302f023966119` (same digest prefix recorded by mado corpus/SOURCES.md:16, row S004).
- 21 lanes carry corpus/SOURCES.md. Row counts (`grep -cE '^\| *S[0-9]{3,} *\|'`): audio 15, chousa 133, game-dev-2d 31, game-dev-3d 36, kagi 51, kaidoku 137, kake 171, kama 256, kasegi 63, kengaku 165, kotodama 808, kotoba 151, kumitate 152, lore 32, mado 314, mori 322, revenger 53, souji 154, tabi 144, tameshi 136, tsukuroi 252.
- Stale pointer (fleet root, reported only): PROTOCOL.md:435 says the contract is authority "until that `CORPUS.md` section lands"; the section has landed at CORPUS.md:64.

### 2.2 Identifier namespace collision (real adjacency defect)
- Contract id rule: `S` + ≥3 digits, "the next unused; never reused" (CORPUS.md:89; SOURCES-CONTRACT-v1.md:22). Scope is per lane; there is no fleet-wide ID registry.
- Command: `grep -n '^| S00[123] |' /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md` (21 files; four via a second query). S001 names 21 different sources, one per lane:
  - chousa corpus/SOURCES.md:11 — "chousa research gate — tools/research-gate.sh" (own-work)
  - audio :9 — ITU-R BS.1770-5; kotoba :14 — Agent Skills — Specification
  - kagi :7 — 1Password "Load secrets into scripts"; kaidoku :7 — REA installed skill v42
  - mori :7 — PSI (kernel docs); souji :24 — git-maintenance(1); tsukuroi :7 — Arch Linux News archive
  - tabi :15 — Chrome remote-debugging switches; tameshi :12 — Stryker mutant states; lore :9 — PROV-O
  - kengaku :23 — LLM contamination systematic review; kotodama :30 — Glottolog 5.3; mado :13 — mado round-10 lesson
  - game-dev-2d :7 — Godot release policy; game-dev-3d :9 — Godot 4.7 release; kake :9 — actions/upload-pages-artifact
  - kama :13 — llama.cpp server README; kasegi :7 — FIRST CVSS v4.0 User Guide; kumitate :14 — oh-my-pi docs/tools/task.md; revenger :15 — host freshness re-probe
- S003 is likewise four sources: chousa :13 SIFT; kotoba :16 Claude Docs best practices; game-dev-2d :9 TileMap; kotodama :32 PHOIBLE 2.0.
- Cross-lane use in PROVINCE files: S-IDs are cited inside the declaring lane (e.g. kotoba PROVINCE.md:15-17; kama PROVINCE.md:147-148). No PROVINCE line read cites another lane's S-ID by bare number (excerpt-based, not exhaustive).
- Precedent: mori PROVINCE.md:90 compared "the S001–S030 URL set" with sibling registries by exact URL: "found no shared URL, so no source rows are merged here."
- Consequence: a fleet-level citation of a chousa row must carry its lane path (e.g. `chousa-shokunin/corpus/SOURCES.md:NN`). Bare `S101` is lane-local.

### 2.3 Source-evaluation vocabulary (inside chousa; no sibling collision)
- Ladder A (PROVINCE.md:5-6): "source hierarchy (primary / secondary / aggregator / unsourced)". SKILL.md:27-35 says this is "this lane's own construction ... Treat the hierarchy as the lane's working standard".
- Ladder B (contract, CORPUS.md:93-97; SOURCES-CONTRACT-v1.md:26-30): per-scope tiers A/B/C; "`community` is never A"; "no NATO/GRADE labels on rows". chousa QUALITY.md:24-27 (criterion 7) admits claims on tier-A or tier-B rows.
- corpus/README.md:52 keeps the primary > secondary > aggregator ladder "as the default ordering, overridden with a stated reason".
- Gap: in chousa SKILL.md, QUALITY.md and corpus/README.md no sentence maps tier A/B/C onto the four-rung ladder (checked by `grep -i 'tier\|aggregator'` on those three files). Unrun: any other chousa file.
- Siblings: none defines a competing ladder. "Source reliability" appears only in lore PROVINCE.md:19, :23 (CM-d, "in-world source reliability ... no grading"). That is in-world canon, not real-world sources.

### 2.4 Ownership claims: consistent deference to chousa (no competing claim)
- kake PROVINCE.md:42-43 — "`chousa` owns research method and source hierarchy; kake keeps only domain findings and its own corpus/SOURCES.md rows."
- kagi PROVINCE.md:67 — "chousa owns the research method (SOURCES.md restates neither method nor admission bar)".
- kengaku PROVINCE.md:137 (table), :262, :403 — "capture and citation method stay chousa's"; :139 — "SOURCES.md contract-v1 is fleet-frozen".
- kasegi PROVINCE.md:47 — "chousa — research method and source hierarchy".
- kumitate PROVINCE.md:29 — "Research method → chousa."
- kotodama PROVINCE.md:19 — refuses "general source-research method (chousa)".
- souji PROVINCE.md:82-83 — "chousa-shokunin owns the research method and source hierarchy; souji's corpus/SOURCES.md applies it and does not restate it."
- kama PROVINCE.md:168-169 — "The generic pinning method (how to pin any repo tag) is chousa's ground".
- audio PROVINCE.md:53 — "research method (chousa)".
- tameshi PROVINCE.md:38, :42 — own SOURCES registry; frontier admission needs a `mined` row. Uses the contract; claims no method.

### 2.5 Bibliography and citation-style standards: no sibling claim
- Clean pass, case-insensitive, over `/home/vgpnk/Projects/shokunin/*/PROVINCE.md`, pattern `ISO 690|GB/T|7714|CNKI|CiNii|J-STAGE|SAMR|openstd|Zotero|BibTeX|reference list|bibliograph|Chicago|APA|MLA|IEEE|DOI|ISBN|PMID|arXiv|permalink|Wayback|SOURCES-CONTRACT|contract-v1`. Hits are limited to:
  - arXiv as public-literature identifier: kengaku PROVINCE.md:20; kumitate PROVINCE.md:24 ("version-pinned to arXiv 2512.08296 v3").
  - SOURCES.md / contract-v1 mentions only (sections 2.1, 2.4).
- `grep -rlE 'GB/T 7714|ISO 690' /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md` → no output, exit 1.
- Bibliographic standards exist only in chousa's own corpus: corpus/README.md:1071-1072 (CNKI count semantics; GB/T 7714 / ISO 690 split), :1169-1170 (PRC citation standard, ISO 690:2021), corpus/SOURCES.md:111 (S101, tier B, 中国学术期刊（光盘版）检索与评价数据规范 copy). No sibling PROVINCE claims these. This states adjacency only; the C2 claim itself is not evaluated here.
- Chinese-language surfaces in siblings are platform documentation, not bibliography: kotoba PROVINCE.md:31 (TRAE, CodeBuddy, Kimi, Zhipu); kasegi PROVINCE.md:74 (CNVD, 360SRC scope).

### 2.6 Other identifier schemes (separate namespaces; uniqueness not checked)
- kaidoku: `evidence_id` (`ev_<hex>`) plus subject sha256 — PROVINCE.md:31-35, :60-61.
- revenger: "cites Evidence IDs" — PROVINCE.md:6-7.
- chousa: `S###` rows plus quote-reopen verdict labels (SKILL.md:24).

### 2.7 Quote normalizer: one declaration claimed, no chousa consumer found
- kagi PROVINCE.md:56 — `corpus/rendered-text-v1.py` is "the one quote/page normalizer declaration (digest, locate)". kagi SKILL.md:752 — "the ONE declaration".
- `grep -i 'rendered-text' /home/vgpnk/Projects/shokunin/*-shokunin/SKILL.md /home/vgpnk/Projects/shokunin/*-shokunin/corpus/README.md` → kagi only (kagi SKILL.md:752; kagi corpus/README.md:160-161).
- `grep -rE 'rendered-text|kagi-shokunin' chousa-shokunin/tools chousa-shokunin/corpus/evidence/round53 chousa-shokunin/corpus/evidence/round55` → "No matches found". Chousa's capture/quote tools (quote-reopen.py, capture-text.py, build-spans.py; SKILL.md:24-25; corpus/README.md:1171, :1205) do not reference it in those trees. Unrun: the full chousa tools/ tree and rounds 24-54.

### 2.8 Adjacent lanes with overlapping vocabulary (no tie-break stated)
- tabi PROVINCE.md:9-13 — "dynamic-page evidence patterns (what to capture so a claim about a page is re-verifiable)". Overlaps chousa's capture discipline; no boundary sentence.
- lore PROVINCE.md:7 and audio PROVINCE.md:10-11 — real-world reference works cited with "attribution / rights / training permission kept distinct". Lore names this "the art ledger's discipline" and its rights owner as `art-east-asian-design` (lore PROVINCE.md:9; game-dev-2d PROVINCE.md:10, :32). Lore's own correction (lore PROVINCE.md:33) says that lane is absent from the roster. Verified: `ls -d /home/vgpnk/Projects/shokunin/art-east-asian-design` → "No such file or directory"; `grep -c 'art-east-asian' /home/vgpnk/Projects/shokunin/MANIFEST.json` → `0`. No PROVINCE read defines an "art ledger". Dangling owner; not chousa's ground (chousa PROVINCE.md does not claim attribution or rights).

## 3. Limits and unrun checks
- Not run: any chousa counter (c1-count.py, c2-count.py); no read of claims.md or quotes.tsv; no live fetch.
- Sibling scan covered PROVINCE.md files plus the named chousa and fleet files. Sibling SKILL.md and corpus were searched only for `rendered-text` and the S001/S003 IDs.
- Output truncation: the broad source-vocabulary pass was truncated (512-byte lines, 50 KB cap). The clean standards pass and the S001-S003 pass were not truncated; all 21 registries are accounted for across two queries.
- Tooling: no installs or updates. Scratch dir /fast/scratch/hyaku/chousa-r58/R58ConnectorSiblingScope created and removed before this report.

## 4. Proposed (non-binding; for L1; no lane file edited)
- P1: lane-qualified citation form for chousa rows (e.g. `chousa-shokunin/corpus/SOURCES.md:NN`) to avoid the 21-way S-ID collision. Fleet-level decision, not this seat's.
- P2: state the mapping of tier A/B/C onto primary/secondary/aggregator/unsourced in chousa SKILL.md or QUALITY.md (absent from the three files read).
- P3: fleet root PROTOCOL.md:435 pointer is stale (CORPUS.md:64 has landed). Route to the protocol owner.
- P4: name an owner for the "art ledger" at lore PROVINCE.md:7 / audio PROVINCE.md:10-11, or remove the reference; `art-east-asian-design` does not resolve.

## 5. Verdict
VERDICT: cross-lane overlap attack on chousa's citation, bibliography, identifier and source-evaluation ground — FALSIFIED as an ownership or standard overlap. No sibling PROVINCE.md claims ISO 690, GB/T 7714, CNKI, a citation style, DOI/ISBN practice, or a competing source ladder; nine lanes defer method to chousa. Adjacency defects that survive the attack and are reported, not resolved: bare `S###` IDs collide across 21 lanes (S001 = 21 sources); contract tiers A/B/C are not mapped to chousa's four-rung ladder in SKILL.md, QUALITY.md or README; tabi's "capture" boundary is unstated; the lore/audio "art ledger" owner does not resolve.
