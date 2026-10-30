# Attack08 — C1 suffix exactness

Full scoped report: `.ufo/waves/round-64/w1/Attack08/report.md`.
Evidence and reproducible bounded driver: `.ufo/waves/round-64/w1/Attack08/evidence.json`, `.ufo/waves/round-64/w1/Attack08/probe.py`.

High: inherited candidate matches `p.stem`, incorrectly accepting README `probe`, `knowledge/probe.txt`, and `knowledge/probe.mdx` for the sole entry `probe.md` (all G02 PASS, exit 0). Exact `.md` and sentence-final-dot controls also pass correctly. Candidate is not production.

High: unchanged frozen E12/E13 independently draw mismatched filenames/references; both isolated frozen fixtures correctly yield G02 FAIL, exit 1 despite battery expectation 0. Supplemental repaired fixtures yield PASS, exit 0 but cannot satisfy frozen C1's immutable kill rule. No full-battery result is asserted.

Nine bounded candidate CLI probes; driver exit 0; complete outputs in evidence.json. Frozen battery hash matches freeze commit. Scratch removed; no clone, production/frozen edits, git/jj mutations, network access, installs or pacman transaction. LSP device unavailable; source fallback and CLI evidence used. Findings advisory only.
