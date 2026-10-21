# Round-13 Gate hash reconstruction

**Answer:** `${GSHA}` is `6b17e50c` (the first eight hex characters of the round-13 `tools/research-gate.sh` SHA-256). Confidence: high.

## Evidence chain

- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin log --oneline --all -- tools/research-gate.sh` identifies `5691bf5` as round 12, `5993dc4` as round 13 (hardlink-alias refusal), and `e17742f` as round 14 (cross-device refusal).
- Hash command: `for c in 5691bf5 5993dc4 e17742f; do git ... rev-parse "$c"; git ... show "$c:tools/research-gate.sh" | sha256sum; done` (repo path as above). Observed mapping:
  - r12 `5691bf531086dd435006cd9d6157df00933973a3` → `91a01695f64e9fd78907008e131e3a3d929ff0d62ab5a762f31fc6c199a0d538`.
  - r13 `5993dc407cb05f16eefe06aa54e94f9a3df82887` → `6b17e50cc9b61dda5e6d753b1f345c8a015e5331965038c6a9b4751a8374d735`.
  - r14 `e17742fa56cb587ecc335e41005507d09d0da787` → `d8bbd0bf6890d3c4bfb8ce1555e6a4b43779bdc892f52e2cf889ede2df2d12f7`.
- `corpus/knowledge/hardlink-alias-r13.md:4` independently records the r13 gate SHA prefix `6b17e50c`; lines 14–16 describe the before/after bypass result. The paired receipts corroborate the behavior: `corpus/evidence/alias-r13-20261019T123621Z-bypass-before.log:2-5` reads the aliased source as supported/CLEAN; `...bypass-after.log:3-7` refuses it with `CLAIM_SOURCE_MULTILINKED`, `nlink=2`, and DRIFT.
- `corpus/knowledge/hardening-r10.md:488-490` leaves `Gate 91a01695… → ${GSHA}…`; the hashes above establish the arrow as r12 → r13, so fill `${GSHA}` with `6b17e50c`.
- Cross-check: `corpus/knowledge/hardening-r10.md:513-515` gives the r13→r14 trail and `Gate 6b17e50c… → d8bbd0bf…`, matching the independently hashed r13/r14 snapshots.

## Divergence

`91a01695` is not a conflicting r13 hash: it is exactly r12's gate hash. Thus the r13 addendum's leading value is correct as the before-side of the transition, and only its after-side slot is unfilled. Treating `91a01695` as the r13 landing hash would be the inconsistency; commit-content hashes and the r14 addendum disprove that reading.

VERDICT: `${GSHA}` = `6b17e50c`; the r12 → r13 → r14 gate-hash chain is internally consistent. Installs/updates: none.