# Hardlink-alias boundary (round 13)

source: tools/research-gate.sh (claim_source_path combined probe); lessons/2026-10-19-hardlink-alias-boundary.md; receipts evidence/alias-r13-20261019T123621Z-{bypass-before,bypass-after}.log
verified-at: 2026-10-19 (round 13; selftest cases 99-102; gate sha256 6b17e50cc9b61dda…)
recheck: re-run the bypass pair (evidence/alias-r13-20261019T123621Z-bypass-*.log recipes) and `bash tools/research-gate.sh --selftest` after any gate edit

## The asymmetry

Canonicalization resolves NAMES, not content ownership. A symlink to an
out-of-corpus file resolves through readlink -f to the true path, and the
boundary re-check refuses it. A hardlink is different: every alias IS the
file (same inode, no true path), so an in-root alias of an out-of-corpus
original passes canon, the root-prefix check, and — before round 13 — was
read. Measured live (receipts `alias-r13-20261019T123621Z-bypass-{before,after}.log`):
the same claims file reads `observed=supported` before the fix and refuses
`CLAIM_SOURCE_MULTILINKED severity=crit` after.

## The rule (r13)

At the shared `claim_source_path` chokepoint (claims, chain, verify-all's
declared-claims binding alike), one `stat -c '%s %h'` probe serves both the
r12 size cap and the r13 alias check, before any read:

- `nlink != 1` → refuse unread: `CLAIM_SOURCE_MULTILINKED` /
  `CHAIN_SOURCE_MULTILINKED`, crit (parity with the boundary-violation
  family), per-item `observed=refused`.
- `size > 8 MiB` → refuse unread (r12, unchanged).

## Why refuse-all and not partner enumeration

The wave considered enumerating same-inode partners and refusing only when a
partner escapes the roots; two independent seats BLOCKed it as unsound:
partner enumeration is order-dependent, blind to nested/bind-mounted roots,
and pays a census cost per multi-link source. Refusal on the link COUNT is
O(1), deterministic, and fails closed. The consequence — a legitimate
in-root multi-link family (two aliases of one in-root file) refuses too — is
a named false-positive class (selftest case 101 pins it as intended
behavior); the escape hatch is a future count-scoped refinement, not r13.

## Named limits

- **TOCTOU**: stat-then-read; a partner swap between probe and read is not
  closed (the gate's threat model is the operator's own corpus, not
  adversarial disk mutation — same standing decision as the r12 cap).
- **Bind mounts**: a same-device bind of an out-of-corpus tree presents
  nlink=1 entries; the mount boundary is invisible to stat. The r13 claim
  closes the HARDLINK class only; bind-mount aliases stay open (r14+
  candidate).
- **Unmeasurable stat**: the alias check needs `%h`; when stat fails the
  probe falls back to the r12 cap-only path and the alias check is skipped
  (documented residual).
- **Legit in-root families** refuse (above).
- verify-sweeps is untouched: it globs sweep paths but never reads matched
  content (attested r5; re-verified by seat 30 this wave).
