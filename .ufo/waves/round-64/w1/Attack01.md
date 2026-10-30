# Attack01 — C1 frozen fixture review

Scoped findings and reproducible bounded probe: [Attack01/report.md](Attack01/report.md), [Attack01/probe.py](Attack01/probe.py).

Frozen E12/E13 create one random-tagged filename and index a separately drawn tag. Both concrete frozen fixtures fail candidate G02 correctly (exit 1); inherited supplement reuses each tag and both repaired fixtures pass (exit 0). Frozen claims and instrument match freeze commit bytes. Supplement success is not frozen-C1 success; report the instrument failure honestly. Partial battery exit 0 is not a PASS verdict. No universal impossibility claim: random-tag collisions remain possible.

Impacted axes: operability and calibration/provenance. Smallest safe correction: preserve frozen claim/instrument, keep supplement separately named, clarify supplement's inconsistent copied identity/count documentation. Canonical judgment remains with L1.

Probe outer exit 0; scratch removed; no installs, network calls, clones, git mutations, or production edits.

Report: .ufo/waves/round-64/w1/Attack01.md
