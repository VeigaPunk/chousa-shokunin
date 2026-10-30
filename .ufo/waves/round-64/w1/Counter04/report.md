# Counter04 — round 64 attempt 2

- Scope: `tools/claims-audit-v2.py` selftest and fault arm, using the frozen C2 selftest expectations in `corpus/evidence/round64/claims.md`.
- `python3 tools/claims-audit-v2.py --selftest`: observed all ten `CASE … ok` lines and `AUDIT_SELFTEST=PASS (10 cases)`; exit 0.
- `python3 tools/claims-audit-v2.py --selftest --selftest-fault 1`: observed `AUDIT_SELFTEST: FAULT case 1 forced` on stderr, no stdout; exit 1.
- Complete captured stdout/stderr and exits: `evidence.txt` alongside this report.
- Frozen-claims context: claims.md defines these expected outcomes; this bounded probe does not measure the full C2 mutation battery or its closure kill rule.
- Files changed: only this seat's `report.md` and `evidence.txt`. No tools installed/updated; no production edits.
- Risks/blockers: none for the requested selftest probe. The full mutation-battery verdict remains unmeasured by this seat.
