# Attack18 — C3 startup/depth review

Full report: [Attack18/report.md](Attack18/report.md). Command/output/exit evidence: [Attack18/probe-receipt.json](Attack18/probe-receipt.json).

- **High — frozen C3 claim/instrument failure:** `corpus/evidence/round64/c3-count.py:91` expects `mirror.parent/corpus/SOURCES.md`, whereas each unchanged instrument correctly reports `mirror.parents[2]/corpus/SOURCES.md`. Exact frozen-fixture probes: all three exit 2, correct named missing paths, all three frozen match predicates false. Therefore the required `RELOCATION_MATCH=3/3` is unreachable with those bytes. Full counter output was not run or claimed.
- **Medium — wrong advertised relocation shape:** counter line 86 substitutes round65 for round64 at the same depth, rather than adding a directory. Actual extra-directory controls correctly exit 2 for all three guards.
- **Supported named limit, not a bypass:** complete frozen committed-tree export relocated under a deeper renamed lane imports all three instruments successfully (exit 0). Removing SOURCES triggers exact-path exit 2 for all three; removing lane-preflight triggers exact-path exit 2 for both guards that assert it.

Frozen/working bytes matched for all three instruments. C1's known frozen E12/E13 mismatch remains a failure; its distinct post-freeze supplement does not repair that verdict. No production/rule edits or installs; LSP device unavailable. Fourteen bounded probes recorded. Scratch export removed, zero live clones. Findings are advisory, not admission or round closure.
