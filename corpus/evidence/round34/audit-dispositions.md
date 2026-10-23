# Round 34 attempt 2 — audit dispositions
# format: <check id> | <disposition>
audit-tool-digest | superseded by audit-tool-digest-v3 (tool gained receipt_gate_file, SET_SHA256 and HEAD-byte reads; value pinned in the set)
audit-tool-digest-v2 | superseded by audit-tool-digest-v3 (never counted against a landed revision; dropped from the set before the final counted run)
skill-tally-256 | fixed at integration (SKILL.md rows 77-84 and :92 cite the gate exact banner form PASS (256 cases, 0 skipped); found by wave seat ScoutSkillTally)
skill-tally-253-stale | fixed at integration (same edit; the stale-form pattern now pins the absence of non-exact banner forms)
audit-tool-digest-v3 | pins this integration commit tool bytes; passes at the post-integration counted run (receipt measure-a2/audit-v3-final.txt); the only prelim undispositioned line
scorecard-count-assert | fixed at integration: the C3 verdict cell now carries the pinned first-run literal SELF_AUDIT_MISMATCHES=0 (the post-reshape count string moved to an explicit pointer)
claims-a2-digest | re-pinned: the post-data erratum (before ceiling 21/37, RevC2Receipts/ExecC2Rerun) changed the doc digest; the set pins the erratum-carrying bytes; the old pin aaeb375e is superseded
