# Round 21 ledger addendum — scoped findings

Read-only reconstruction; no repository source or ledger file was edited. The requested draft is below for the integration owner. The Round-21 record identifies the fix as the round-20-named `ptr_resolves_meta` boundary gap, not a hardening-r10 ledger item (`SCORECARD.md:1078-1084,1092-1099`; `LOG.md:768-780`; `corpus/knowledge/pointer-boundary-r21.md:7-22`).

## Proposed append-only text

### Round-21 addendum (2026-10-19, append-only)

E10 [INFERENCE] — **no §3 ledger row and no round-11 queue item was closed, changed, or added by round 21.** Round 21 canonicalizes the `ptr_resolves_meta` candidate with `readlink -f`, checks `in_root` against both roots, and applies the denylist to the canonical target (`SCORECARD.md:1092-1098`; `corpus/knowledge/pointer-boundary-r21.md:16-22`). This closes the round-20-named metadata-pointer traversal/symlink boundary, not one of the classes in the round-11 ledger queue (`LOG.md:770,778-780`; `hardening-r10.md:320-348`).

The closest textual match is row 56: “`A-r9.md:50` row C3 pointer `A:76` vs span occurrence `A:86`; no mode pairs a row's `path:line` with its span's occurrence line” (`hardening-r10.md:281`). Queue item 1 explicitly asks to fix-or-absorb that record and decide whether the **pointer/span** class merits a gate check (`hardening-r10.md:325-328`); queue item 2 is attribution/pointer-line pairing (`hardening-r10.md:329-331`). Round 21 resolves a filesystem path to a pointer target; it does not pair citation `path:line` with a span occurrence. The other tempting phrase match, row 8, is “in-root hardlinks bypass path canonicalization” (`hardening-r10.md:203`); its hardlink class was already explicitly closed in r13, and r21's metadata-pointer traversal/symlink fix does not alter that disposition (`hardening-r10.md:472-482`). Therefore no ledger disposition or round-11 queue transition is warranted; do not change running totals.

Gate blob SHA-256 before → after: `49b36759bc47ffed8971834515f86921b45725038a3ccf20eb215f0fb64448e9` (`git show edcffba:tools/research-gate.sh | sha256sum`) → `bfc291ef526040607436bd4d505354200e4940b4d1e43213008950608f6274ef` (`git show 8a21559:tools/research-gate.sh | sha256sum`). Read-only history shows `edcffba` as the r20 gate change, `8a21559` as the r21 gate change, then `51bd389` as r21 records (`git log --oneline -- tools/research-gate.sh`; `git log --oneline` around r21). The r21 commits' changed-path lists contain no `corpus/knowledge/hardening-r10.md` (`git diff-tree --no-commit-id --name-only -r 8a21559`; same command for `51bd389`).

Selftest: cases 125–128 are `ptr-traversal` (exit 1), `ptr-symlink` (exit 1), `ptr-lane-abs` (exit 0), and `ptr-deny-symlink` (exit 1); receipt reports `PASS (128 cases, 0 skipped)` (`corpus/evidence/ptr-r21-20261019T184000Z-selftest.log:125-129`). Cases 1–124 were byte-identical to the r20 receipt (`SCORECARD.md:1092-1099`; `LOG.md:780`).

**Confidence:** high on the no-row/no-queue-change conclusion; the apparent overlaps are separate defect classes, and both round-21 records and the round-11 queue are explicit. `E10` is inferred from the existing E2/r13, E3/r14, E4/r15 sequence; intervening round addenda are absent in the current file (`hardening-r10.md:466-600`). No tools installed.

VERDICT: Round 21 changed no hardening-r10 ledger row and no round-11 queue item; use this append-only draft without a count update.