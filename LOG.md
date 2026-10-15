# chousa-shokunin — Iteration Log

- 2026-10-14 — round 0: minted as shonen (sibling mint; rationale in MINT.md).

## 2026-10-15 — boundary parity fix (round 1 integration prep)

`ScopeBoundary` found a contradiction in the mint artifacts: `MINT.md` and the
roster scan (`mint-roster-scan.json`) explicitly rejected **kumitate** as a
complementary province, but the `PROVINCE.md` and `SKILL.md` refusal clauses this
lane wrote omitted it. Closed here — both files now name orchestration,
multi-agent dispatch and agent lifecycle as refused (→ kumitate). Recorded rather
than silently patched, because the omission had already propagated into peer
proposals (`QualityBar` Q-BOUND, `ApprovalTable`), and the proposed gate vocabulary
classified `SCOPE_ORCHESTRATION_ABSORBED` as `info` where the other two absorbed-
scope ids are `warn` — a severity asymmetry that would let an absorbed orchestration
record pass as CLEAN. **Landing requirement:** that id must be elevated to `warn`
so all three refused provinces have identical gate teeth, with one symmetric
selftest fixture per province asserting exit 1.
