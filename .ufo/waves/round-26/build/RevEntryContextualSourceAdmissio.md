# Freshness re-verification — contextual-source-admission-r24

- Scope: assigned entry only. Private clone base observed: `f361d12e44687841e30ec35710ddb366c6f795e0` (`/tmp/chousa-r26-RevEntryContextualSourceAdmissio`). No production files changed.
- The entry's `recheck:` at `corpus/knowledge/contextual-source-admission-r24.md:4` is a schedule, not a shell command: S004 `on-release`; S002/S003 `365d`. QUALITY 6 permits a cadence optionally followed by a command (`corpus/QUALITY.md:17-23`). No per-entry command was present; ran the base gate's metadata recheck:
  - cwd `/tmp/chousa-r26-RevEntryContextualSourceAdmissio`
  - `bash tools/research-gate.sh verify-metadata corpus/knowledge/contextual-source-admission-r24.md --root /home/vgpnk/Projects/shokunin`
  - exit `0`; output: `META entry=contextual-source-admission-r24.md source=present verified_at=dated recheck=scheduled verdict=clean`; `METADATA_COMPLETE=1/1`; `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)`.

## Reopened source anchors (accessed 2026-10-21)

- S002, https://ifcncodeofprinciples.poynter.org/the-commitments — Principle #2, “Criteria: To be compliant on sources,” bullets 2–3. The excerpts cited at entry lines 23–27 remain verbatim; e.g. “The applicant uses the best available primary, not secondary, sources of evidence wherever suitable primary sources are available.” The row is mined, tier A for what the Code requires on source transparency, and used-by names this entry (`corpus/SOURCES.md:12`).
- S003, https://hapgood.us/2019/06/19/sift-the-four-moves/ — “Investigate the source” paragraph 2 and “Find better coverage” paragraph 1. Both excerpts at entry lines 33–36 remain verbatim; e.g. “knowing the expertise and agenda of the source is crucial to your interpretation of what they say.” The row is mined, tier A for Caulfield’s own statement of SIFT, and used-by names this entry (`corpus/SOURCES.md:13`).
- S004, https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-24 — §24.2.1.3 and Key Points bullet 5. Both excerpts at entry lines 28–32 remain verbatim; e.g. “place an emphasis on specific features of study design (e.g. which parts of the study were prospectively designed) rather than ‘labels’ for study designs”. The live page still cites Handbook v6.5 (2024), chapter last updated October 2019; the cited release/anchor matches the entry’s on-release note. The row is mined, tier A for Cochrane’s own NRSI appraisal guidance, and used-by names this entry (`corpus/SOURCES.md:14`).

## Claim audit

- Entry lines 8–19 and 40–60 cite the above sources. Their quoted content supports only the stated source-specific propositions; the broader per-claim checklist is not represented as a rule those sources state: entry lines 69–73 explicitly label its generalization and admission row as analogy/lane construction. This matches the scoped-tier requirement (QUALITY 7, `corpus/QUALITY.md:24-27`; tier A is scoped by `CORPUS.md:93-100`).
- The internal ladder citations resolve: `SKILL.md:18` states the ordering; `SKILL.md:25-33` explicitly calls it the lane’s construction. Entry lines 51–60 and 79–83 characterize it consistently.
- Entry lines 64–75 separates observation, inference, and unknown, and does not claim that source availability/topicality alone establishes truth. No QUALITY 2/7/8 defect found (`corpus/QUALITY.md:3-5,24-32`). Its cited rows are mined and correctly backlink this path (`corpus/SOURCES.md:12-14`).

## Findings, residual risk, verification gaps

- Findings: none; no stale quoted anchor or false attribution observed.
- Residual risk: the sources have domain-limited scope; transfer to general research method remains an explicitly labeled lane inference, not external authority.
- Verification gap: the base `verify-metadata` command validates header presence/scheduling only; it does not fetch cited pages. Page freshness and quote matching above were checked by reopening each URL, not established by that gate output. No installs.

VERDICT: re-verifies — all cited anchors remain present verbatim and the entry’s scoped claims match their rows/anchors as of 2026-10-21.