# Attack13 — C2 kill-semantics review

Full report: [Attack13/report.md](Attack13/report.md)
Evidence: [Attack13/timeout-output.txt](Attack13/timeout-output.txt)
Reproducer: [Attack13/timeout-probe.py](Attack13/timeout-probe.py)

Counterexample observed: the unmodified frozen runner's real subprocess timeout path credits infrastructure timeouts as kills. Injecting only a zero-second timeout budget yields `AUDIT_MUTANTS_KILLED=12/12`, exit 0, for both v1 and v2, without a completed checker verdict. Runner/generator hashes match the freeze. This establishes a frozen harness-error/kill separation defect, not a demonstrated default-budget closure miss. Frozen C1 E12/E13 failure remains unrepaired and separate from its supplement.

Impacted axes: calibration, operability, provenance. Smallest safe correction: preserve the freeze; distinctly name a successor that exits 2 on harness timeout and validates an unmutated baseline before scoring. No production edits, git mutations, installs or clones; own scratch removed.

Report: .ufo/waves/round-64/w1/Attack13.md
