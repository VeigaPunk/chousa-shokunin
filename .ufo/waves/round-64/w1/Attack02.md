# Attack02

Full report: [Attack02/report.md](Attack02/report.md).
Evidence: [Attack02/probe-output.txt](Attack02/probe-output.txt); reproducer: [Attack02/probe.py](Attack02/probe.py).

Medium: frozen and supplemental C1 ZERO judges accept denominator `999` and contradictory/invalid FAILED/ENV/SKIPPED summary memberships because their ZERO branch returns before component validation. Canonical judge probes exit 0, stderr empty. No full-battery pass claimed.

Frozen E12/E13 independently drawn name mismatch remains an honest C1 claim failure; frozen bytes match bf40d99bda9eefdad3ed6276da077cfb24ba82f1. Supplement fixes only those fixture names, not the judge weakness. No production or frozen edits, installs, network access, clones, or scratch trees.
