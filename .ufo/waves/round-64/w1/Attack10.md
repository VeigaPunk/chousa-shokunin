# Attack10 — C2 A04/A05/A06

Full scoped report: [Attack10/report.md](Attack10/report.md).
Raw command/output/exit evidence: [Attack10/evidence.json](Attack10/evidence.json).
Reproduction driver: [Attack10/probe.py](Attack10/probe.py).

No actionable C2 defect found in A04–A06. Independently demonstrated all three mutant errors on both frozen checker versions through minimal fixtures; 48 bounded probes completed, driver exit 0. All five scoped inputs exactly matched freeze bf40d99bda9eefdad3ed6276da077cfb24ba82f1. A04 is directly killed by observed frozen R2/R3 legs; A05/A06 reproduce distinctions enforced by v2 C5/C9, whose full selftest was not executed because it writes git fixtures. This is not a full 12/12 closure reproduction or claim admission.

Known frozen C1 E12/E13 failure remains a failure; the distinct post-freeze supplement cannot repair its frozen predicate. LSP device unavailable. No production/frozen/sibling edits, network, installs, clones, git/jj mutations, or service changes. Scratch removed.
