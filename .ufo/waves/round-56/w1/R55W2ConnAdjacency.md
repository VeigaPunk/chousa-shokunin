# R55W2ConnAdjacency — C2 adjacency, cross-lane ownership, and 灰色文献 entry coherence

seat R55W2ConnAdjacency · chousa round 56 W1 · 2026-10-27 · connector / falsify item.
Audited round-55 C2 (`grey-literature-and-chinese-search-record-r40.md:33`) province claim, scanned sibling
ownership across 20 sibling lanes, and evaluated the lane's 灰色文献 cluster for contradictions and pointers.

## 1. Sibling PROVINCE.md and corpus scan (Evidence)
- Target: 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/` (excluding `chousa-shokunin`).
- Terms: `pharmacovigilance`, `ADR`, `药品不良反应`, `上市许可持有人`, `NMPA`, `systematic review reporting`, `PRISMA`.
- Sweep A (all 20 sibling PROVINCE.md files):
  - Command: `grep -iE "pharmacovigilance|药品不良反应|上市许可持有人|NMPA|systematic review reporting" *-shokunin/PROVINCE.md` -> 0 matches.
  - Command: `grep -w "ADR" *-shokunin/PROVINCE.md` -> 0 matches (substring hits only: kaidoku:151, mori:407 inside "headroom").
  - Command: `grep -i "PRISMA" *-shokunin/PROVINCE.md` -> 0 matches.
- Sweep B (all sibling corpora text files):
  - `pharmacovigilance`, `药品不良反应`, `上市许可持有人`, `NMPA`, `systematic review reporting`: 0 matches fleet-wide.
  - `ADR`: 0 matches in medical/pharmacovigilance sense. Only ARM64 instruction displacement hits in kaidoku (`round-32/sources/pe-format.md:580`, `round-33/sources/pe-format.md:584`) and raw audio bytes in audio-shokunin.
  - `PRISMA`: 0 matches for systematic review reporting standards. Matches in kaidoku (`usr/share/nvim/runtime/ftplugin/prisma.vim:689` Prisma ORM), kasegi (`corpus/source-snapshots/round-24/S011.txt:594` Prisma ORM), kengaku (`corpus/evidence/round26-sources/gate.md:23` analogizing paper screening to PRISMA count), and mori (`corpus/evidence/sources-r36/S205.src:126` "PRISMA-inspired, not PRISMA-compliant" search log).
- Ownership analysis: Substantive clinical drug-safety evaluation, ADR, 药品不良反应, 上市许可持有人, and NMPA regulatory practice are **unowned across the entire fleet** (orphan domain). Sibling lanes explicitly route general search and source-hierarchy method to chousa (11 sibling declarations, e.g. kengaku PROVINCE.md:137, souji:82, kake:36, kasegi:47, kagi:67).
- Verdict on r40.md:33: The entry's assertion that drug-safety evaluation practice is adjacent ground that chousa reports and does not hold is **fully verified and survives**. Per `chousa PROVINCE.md:17` ("Out of province -> report, never absorb"), reporting regulatory requirements as document evidence without absorbing substantive doctrine is the exact required posture.

## 2. Cross-entry coherence across the lane's 灰色文献 cluster
Audited `chinese-search-record-r39.md`, `quality-control-guideline-issued-text-r48.md`, and `western-instrument-alignment-r50.md` against round-55 C2 (`r40.md`) and round-56 C2 (`grey-literature-field-china-r42.md`):
- `chinese-search-record-r39.md` (animal-experiment SR reporting recommendation, S109):
  - Contradiction: None. r39 carefully bounded itself to animal-experiment reporting (`尚无专门针对动物实验 SR 的报告规范`, S109:char 15310).
  - Pointers: r39's `#### Unknown` asked whether any Chinese body issued a national standard for search reporting (:34) and whether other Chinese journals/forms require grey literature (:35). r40 (NMPA regulatory guideline requiring `是否检索灰色文献`) and r42 (T/CLPA workflow standard in 中国药房 grading grey literature Ⅰ级/A) directly answer these unknowns.
- `quality-control-guideline-issued-text-r48.md` (NHC development center 2024 QC guideline, S118):
  - Contradiction: None. S118 factually has 0 occurrences of `灰色文献` (r48:16), requiring published peer-reviewed literature.
  - Resolves r42's Unknown: Staged r42:48 had an open Unknown ("Whether the 2024 试行 质量控制指南... lists 灰色文献 the same way"). r48 holds S118 and proves `灰色文献` count is 0.
  - Institutional divergence: A mutual pointer is needed to highlight the divergence within Chinese drug clinical comprehensive evaluation: the working group/association workflow standard (S127 in r42) mandates grey literature at Ⅰ级/A, whereas the NHC development center's QC guideline (S118 in r48) omits it entirely.
- `western-instrument-alignment-r50.md` (Cochrane Handbook Ch 4 vs S118):
  - Contradiction: None. r50 bounded itself to S120 and S118, refusing to generalize to a whole tradition (:27).
  - Pointers: r50 contrasted Cochrane's bias rationale for unpublished literature against S118's omission. But r40 proved that NMPA's 2019 guideline explicitly adopted Cochrane's bias rationale (`灰色文献中可能包含阴性研究结果` / `会引入发表偏倚`, S124:char 1046, 1082) into Chinese regulatory reporting. A pointer from r50 to r40 prevents readers from concluding that Chinese drug literature evaluation ignores Cochrane's bias rationale.

## 3. Connector Proposal: Institutional-lineage cross-pointer topology
- **Affected axes:** Depth (C2), Calibration (C3/lane coherence), Operability (C1 decoupling).
- **Proposed move:**
  1. *Resolve r42's Unknown using r48:* Formally cite held S118 in r42, closing staged r42:48 by documenting the institutional divergence (working group T/CLPA standard: Ⅰ级/A vs NHC center S118: 0 grey literature).
  2. *Close r39's search-standard Unknown via r40 and r42:* Add cross-references from r39's open questions to r40 and r42.
  3. *Contextualize r50 via r40:* Link r40 in r50 to document that Cochrane's publication bias doctrine was incorporated into NMPA regulatory reporting, contrasting S118's omission.
  4. *Enforce adjacency boundaries:* Keep all cross-references strictly confined to source metadata, document provenance, and byte-exact counts, leaving substantive medical/regulatory doctrine unabsorbed.
- **Second-order effects:**
  - *Runtime*: Zero overhead; purely documentation and knowledge-graph linking; no subprocess or audit-hook triggers.
  - *Contract*: Strict compliance with `PROVINCE.md:17` ("report, never absorb").
  - *Substrate*: Leverages held on-disk capture S118 without duplicate source fetches.
  - *Verification*: `python3 corpus/evidence/round56/c2-count.py` passes cleanly without interference.
- **Risks & mitigation:** Risk of introducing ungrounded generalities is mitigated by restricting cross-pointers to verified file paths and byte-exact occurrence counts.
- **Verification:** Verified S118 grey literature count (`0`), S124 bias quotes (char 1046, 1082), and 20-sibling sweeps.

VERDICT: attacked r40 C2 adjacency and cross-entry coherence — r40 adjacent-ground claim survived (pharmacovigilance/drug-safety is unowned across fleet); 0 contradictions across 灰色文献 cluster; cross-pointer topology proposed.
