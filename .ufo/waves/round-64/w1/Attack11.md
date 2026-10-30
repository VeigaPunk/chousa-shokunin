# Attack11 — scoped C2 findings

Detailed report and evidence: [Attack11/report.md](Attack11/report.md), [probe output](Attack11/probe-output.txt), [probe driver](Attack11/probe.py).

- A07: the claimed later-modification defect is not implemented: newest-first `git log` plus `c[-1]` still selects the add commit under `--diff-filter=AM`. Synthetic exact-R7 log-shape probe returns the same firing verdict for BASE and A07; real R2–R4 hold. Full-matrix survival is inferred, not reported as measured.
- A08: removing the unreadable guard still fires on the absent nonempty needle; frozen C6 kills loss of the `unreadable` diagnostic, not an actual fail-open verdict.
- A09: genuine kill confirmed by real R2/R3 summary mismatches and a one-row minimal counterexample.

Measured generator, runner, v1 and v2 bytes equal freeze bf40d99bda9eefdad3ed6276da077cfb24ba82f1. Probe command exits 0; individual receipt commands/exits/output are preserved. No git mutations or full git-writing matrix run. Frozen C1 E12/E13 failure remains unrepaired and distinct from its supplement. No production edits, tool installs, network, or service changes. Scratch removed.

Advisory only: preserve frozen rules; canonical L1 must handle closure and any separately named future correction.
