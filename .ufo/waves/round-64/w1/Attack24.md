# Attack24

Scoped findings and command/exit evidence: [Attack24/report.md](Attack24/report.md), [Attack24/evidence.json](Attack24/evidence.json), [Attack24/realpath-source.txt](Attack24/realpath-source.txt).

High: frozen C3 relocation oracle expects the wrong missing-file path; all three bounded startup probes exit 2 with the correctly derived path but fail the frozen match. Frozen bytes independently matched bf40d99bda9eefdad3ed6276da077cfb24ba82f1. Source-backed pathlib/realpath statements are supported, but S152 is counter source, not a successful execution; no C3 admission follows. Frozen C1 E12/E13 fixture failure remains acknowledged, not repaired or replaced by supplemental results. Advisory only; no outside non-author closure.

Scratch removed; no installs, production edits, network, or VCS mutations.
