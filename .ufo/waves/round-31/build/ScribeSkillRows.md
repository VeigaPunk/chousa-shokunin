# ScribeSkillRows report

- **Behavior/verdict:** Drafted append-only SKILL.md additions for C1 line binding and C2 exact-byte revision binding; no product file was changed.
- **Artifacts:** `.ufo/waves/round-31/build/ScribeSkillRows/drafts.md` contains exact rows and insertion points for the Decision table, Error patterns, Checklist, and `research-gate verify-claims` Gates note.
- **Evidence/provenance:** Read `corpus/evidence/round31/claims.md` lines 22–32 and 73–81, plus `SKILL.md` lines 13–25, 39–50, 64–78. Draft semantics follow that frozen contract and current table/item structure.
- **Gate note:** Includes `CLAIM_LINE_MISMATCH` → `observed=mislocated`, `CLAIM_SOURCE_REVISION_MISMATCH` → `observed=stale`, and malformed fields → `CLAIM_RECORD_INVALID`, `observed=invalid`. `PASS (N cases)` remains an L1 placeholder.
- **Actions/outcomes:** `timeout 10s mkdir -p .ufo/waves/round-31/build/ScribeSkillRows` completed with no output; the shell tool exposed no exit-code field. Draft and report writes succeeded.
- **Gates/limits:** No counter, gate, self-test, or other verification was run; no external source was opened and no tool was installed. The C1/C2 counter predicates and expanded self-test result remain unverified here.