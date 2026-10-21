# ExecC2DateDiff — round 26 attempt 1

Axes: freshness correctness, falsifiability, and runtime cost.

## Scoped artifact

- Private clone created at `/tmp/chousa-r26-ExecC2DateDiff`; observed base from `git rev-parse HEAD`: `f361d12e44687841e30ec35710ddb366c6f795e0`.
- Added `/tmp/chousa-r26-ExecC2DateDiff/corpus/evidence/round26-date-differential.sh` (207 lines; source lines 1–207). It generates fixtures across 1900–2100, crosses the requested 14 day intervals, tests pre/equal/post due boundaries, explicit ISO dates, and invalid calendar dates against a Python `datetime` oracle. It prints `DATE_DIFF_AGREE=k/n` and exits 1 on mismatch.
- Retained script SHA-256: `bb8f7f44871b1ac52d3da1f85d6d314aee77490315b566b382788d94ada1f5e7` (`sha256sum` output).
- Patch: `/tmp/chousa-r26-ExecC2DateDiff/r26-ExecC2DateDiff.patch`; SHA-256 `e297e9f83118f68b8cf243fd7cbe544936e82ab086d73b349323864a796774ba` (`sha256sum` output). Patch was generated against the observed base revision.

## Execution and limits

- Neither the intended differential run against `/tmp/chousa-r26-ExecC2Due-3/tools/research-gate.sh` nor the deliberately broken-copy run was executed. No `DATE_DIFF_AGREE` result or gate pass/failure is claimed. The replacement L1 instruction said not to run tests/builds/formatters now; I stopped at the existing artifacts and report.
- Consequently the requested positive result and demonstrated exit-1 falsifier remain unobserved for integration. Script behavior against the C2 implementation is not yet verified.
- Latest sibling handoff reports candidate gate `/tmp/chousa-r26-ExecC2Due-3/tools/research-gate.sh` SHA-256 `e5e5506edee6cfb23d6b8ada6a8cc9fb30a8b6f355e50ce2acaec23dbe3606af` and confirms it did not run the differential; this is handoff identity, not execution evidence.
- No installs or updates. No source-code, live-lane, sibling-clone, or external-state changes were made by this seat.

VERDICT: Differential script and patch are retained in the private clone; required runtime evidence is outstanding per the L1 stop instruction.