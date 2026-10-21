# Round 26 — C3 registry walk

Base observed: `ba3333254dd337658a4f25e7a9471f9cf4e4567e` (`git rev-parse --verify <base>^{commit}`). POP24 is the five files at `corpus/evidence/round26-measure.sh:28-29`; registry rows below are from `git show <base>:corpus/SOURCES.md`. C3 criteria/predictions: `corpus/evidence/round26-claims.md:84-114`; exact-path correction: `:134-139`.

Observed: each POP24 `source:` value is a single line (no continuation lines); IDs below include all S### tokens in it. All registry statuses are `mined`, and each used-by cell contains the exact repo-relative path of the citing entry.

- `corpus/knowledge/citation-chain-fidelity-r24.md:3`: S005, S003. S005 row `corpus/SOURCES.md:15`: mined; used-by `corpus/knowledge/citation-chain-fidelity-r24.md` (names this entry: yes). S003 row `:13`: mined; used-by `corpus/knowledge/contextual-source-admission-r24.md, corpus/knowledge/citation-chain-fidelity-r24.md` (yes). `verified-at` at entry `:4` names opened source anchors, quote rereads and local-boundary reread: says what was checked (yes).
- `corpus/knowledge/claim-support-states-r24.md:3`: S006, S007. Rows `corpus/SOURCES.md:16-17`: both mined; each used-by cell is `corpus/knowledge/claim-support-states-r24.md` (names this entry: yes). Entry `:4` says both arXiv pages/quoted anchors and the README known-gaps bullet were reread: yes.
- `corpus/knowledge/contextual-source-admission-r24.md:2`: S002, S004, S003. S002 row `corpus/SOURCES.md:12` and S004 row `:14`: mined; each used-by cell is `corpus/knowledge/contextual-source-admission-r24.md` (yes). S003 row `:13` has the two-path cell quoted above (yes). Entry `:3` says all three pages were opened and S004's subsection number read from the live page: yes.
- `corpus/knowledge/json-delimiter-r24.md:3`: S001, S013. Rows `corpus/SOURCES.md:11,23`: both mined; each used-by cell is `corpus/knowledge/json-delimiter-r24.md` (yes). Entry `:4` describes before/after gate runs and three single-edit mutants failing their pinning case: yes.
- `corpus/knowledge/metadata-screen-r25.md:3`: S029, S033. Rows `corpus/SOURCES.md:39,43`: both mined; each used-by cell is `corpus/knowledge/metadata-screen-r25.md` (yes). Entry `:4` describes frozen-population/fixture runs, differential agreement, and source-opening/quote evidence: yes.

Reverse direction: all mined rows at this base are S001-S007, S013, S029, S033 (`corpus/SOURCES.md:11-17,23,39,43`). Every nonempty used-by path on those rows cites its row ID back in its source field; no mined used-by→entry mismatch found. Thus all five POP24 entries are clean on the requested registry-link and descriptive verified-at checks (5/5), not merely unknown because the base gate lacked `--registry`.

Judgment boundary: the `verified-at` “yes” findings mean the field text states concrete checks; this walk does not independently authenticate that the historical checks occurred. No tools installed.

VERDICT: No scoped C3 data defect or reverse-link curation defect found at the registered base.