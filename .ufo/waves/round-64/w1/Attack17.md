# Attack17 — C3 relocation arithmetic

Scoped report and bounded probe: [Attack17/report.md](Attack17/report.md), [Attack17/probe.py](Attack17/probe.py).

Frozen `c3-count.py:91` expects `lane-copy/corpus/evidence/corpus/SOURCES.md`, while all three unchanged instruments correctly report `lane-copy/corpus/SOURCES.md`. Six bounded probes returned exit 2 with exact correct diagnostics; all frozen-oracle comparisons were false. Current instrument bytes equal freeze bf40d99bda9eefdad3ed6276da077cfb24ba82f1. The counter's `round65` fixture also preserves depth instead of moving one directory deeper.

Impacted axes: depth, calibration, provenance. This is a frozen-counter defect, not just supplemental weakness. Preserve frozen rules; report its target unmet. A distinctly named supplement must fix both expected-path arithmetic and actual relocation depth. No canonical judgment or integration performed. Known independent C1 E12/E13 failure remains unchanged. Scratch removed; no installs, clones, production edits, or git mutations.
