# FxQualityCriteria — QUALITY 13/14 review

Axes: calibration (criterion claim vs evidence) and operability (whether the prescribed recheck works).

## Findings

None actionable. The additions are grounded in the cited defects and do not conflict with QUALITY 1–12: QUALITY 4 preserves the old header by append-only erratum, while QUALITY 13 applies to new recheck commands; QUALITY 14 applies prospectively to new lessons. Neither criterion claims that grep alone proves command execution or row completeness.

## Evidence

- Checkpoint clone base observed: `d730ae4c33989ad9c8535764d4cae77b4db869f6`; corrected full checkpoint observed: `e93ac711f885a10d44fdd80a1734997419595b5a`.
- At the base, the named negated grep in QUALITY.md:64–65 printed `citation-chain-fidelity-r24.md:5` and exited 1; `verify-chain ... --root ..` returned `RESOLVED_HOPS=0/22`, DRIFT, exit 1. The named `grep -qx '## Spot-check intake' corpus/lessons/round-24.md` exited 1.
- At e93, that grep remains exit 1 because the original line 5 is intentionally preserved. The appended erratum at `corpus/knowledge/citation-chain-fidelity-r24.md:89–97` explicitly says it supersedes the old command and gives the lane cwd plus `$SHOKUNIN_ROOT`. Running the old `--root ..` command in the private clone still produced 0/22, DRIFT, exit 1; running the erratum command with `SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin` produced `RESOLVED_HOPS=17/22`, CLEAN, exit 0. This independently exercises the command; the grep is only the syntax screen QUALITY.md:67 says it is.
- At e93, the named heading check remains absent from the unchanged r24 lesson (exit 1) and is present in `corpus/lessons/round-25.md` (exit 0). QUALITY.md:75 explicitly leaves the per-debt row check to a reviewer. The r24 outside check lists three debts at `corpus/lessons/round-24-verifier-spotcheck.md:17`; round-25 intake has corresponding rows at `corpus/lessons/round-25.md:20–22` (concurrent append, root placement, lesson slot), each with a disposition/pointer. R25-M2/M3 at lines 38–39 point to those corrections.

## Residual risk and verification gaps

- QUALITY 13's named grep continues to fail on the corrected artifact because the superseded historical `recheck:` line is retained. It is not an affirmative post-fix test; the criterion's “new” scope, append-only correction, explicit limitation, and separately executed clone check make this non-actionable. Future reviewers must not treat that grep as proof that the superseding command is runnable.
- QUALITY 14's heading grep proves only heading presence, not row-per-debt coverage; the criterion explicitly requires reviewer comparison, which was performed against the three debts in the cited r24 outside check.
- LSP device unavailable (`read xd://lsp` returned “No such tool”); no semantic LSP checks were possible. No full gate selftest/suite was run; not assigned. No installs.

VERDICT: No actionable defect in QUALITY 13 or 14; both are calibrated when their stated manual checks are honored.
