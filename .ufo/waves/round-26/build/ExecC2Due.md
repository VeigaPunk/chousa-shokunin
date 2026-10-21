# ExecC2Due — round 26 Claim 2

Base observed in private clone: `f361d12e44687841e30ec35710ddb366c6f795e0` (`git rev-parse HEAD`).

## Implementation
- Private clone: `/tmp/chousa-r26-ExecC2Due-3`.
- `tools/research-gate.sh:307,317`: documented `verify-metadata --as-of` usage.
- `tools/research-gate.sh:2305-2354`: pure-Bash days-from-civil/civil-from-days arithmetic; decimal cadence strips leading zeroes and bounds before arithmetic, returning unknown for oversized/out-of-range due dates.
- `tools/research-gate.sh:2373-2377,2438-2445,2544-2570`: precomputed as-of day, refused-entry fields, per-entry classification and overdue warning.
- `tools/research-gate.sh:5954-5955,5967-5970`: option parsing, mode restriction, and exact calendar validation via `metadata_iso_date`.
- `tools/research-gate.sh:5759-5914`: appended C2 selftests after legacy case 161: six probe controls; invalid/missing value and wrong-mode usage; leap-day/non-leap-day addition; oversized cadence, year-range overflow, invalid verified date, and refused entry.

## Retained evidence
- Candidate file SHA-256: `e5e5506edee6cfb23d6b8ada6a8cc9fb30a8b6f355e50ce2acaec23dbe3606af` (`/tmp/chousa-r26-ExecC2Due-3/tools/research-gate.sh`).
- Patch: `/tmp/chousa-r26-ExecC2Due-3/r26-ExecC2Due-3.patch`.
- Patch SHA-256: `4bebadfcb5751f08b2466efc938b8de9866b88ca00462829ddc2e3f8b05d6d4a`.
- Candidate `round26-measure.sh <clone> c2` and `holds` were not run: the replacement L1 handoff directed no further builds/tests/formatters and assigned post-integration verification to Main. Accordingly `FRESHNESS_CLASSIFIED`, `C2_ORACLE_AGREE`, `C2_CONTROLS_CAUGHT`, oracle-mismatch lines, and holds results are unobserved; no PASS is claimed.
- No installs.

Risk/blocker: candidate measurement and selftest/drift holds remain for Main's post-integration gate; the requested candidate counts cannot be reported before those runs.

VERDICT: C2 implementation and patch are complete; candidate verification is deferred per L1 handoff.