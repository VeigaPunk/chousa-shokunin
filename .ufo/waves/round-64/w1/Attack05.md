# Attack05 — C1 symlink recursion

Detailed report and bounded probe: [Attack05/report.md](Attack05/report.md), [Attack05/probe.py](Attack05/probe.py).

Counterexample: indexed `ok.md` plus `loop -> .` or a directory symlink falsely passes the inherited reference candidate (exit 0), contradicting frozen C1's non-file-symlink rejection. Current working-tree tool rejects both (exit 1), preserves regular-file symlinks (exit 0), and rejects dangling links (exit 1). This is evidence for the measured working-tree bytes, not a landing/full-battery certificate.

Frozen E12/E13 independently drawn names remain an honest frozen failure; not rerun, hidden, or repaired. The separate supplement fixes their fixture construction but lacks directory-symlink/cycle coverage. Smallest safe correction is rejecting symlinks in os.walk's directory list without following them; current measured tool already does so. Preserve frozen failure and route fresh coverage to a distinct instrument. Only L1 integrates.

Bounded probe command exited 0; all 15 subprocess commands, outputs, exits, source identities, and correction details are recorded in the detailed report. Scratch removed; no installs, network, clones, or production edits.

Report: .ufo/waves/round-64/w1/Attack05/report.md
