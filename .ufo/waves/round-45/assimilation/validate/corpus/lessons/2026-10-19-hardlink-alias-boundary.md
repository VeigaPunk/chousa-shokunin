# Round 13 — hardlink-alias boundary

Round 13, 2026-10-19 (LOG.md round-13 admission). The last r2 carried
residual (ledger row 8) closes.

## What worked

- One chokepoint, one probe: `stat -c '%s %h'` now serves the r12 size cap
  AND the r13 alias check before any read; claims, chain and verify-all's
  declared-claims binding refuse alike.
- Refuse-on-count, not enumeration: the wave's two enumeration designs were
  BLOCKed as unsound (order dependence, nested/bind-mounted roots); the
  count rule is O(1), deterministic, fails closed. Case 101 pins the
  legit-family refusal as intended behavior so the trade is explicit.
- The bypass proof is a live receipt pair (alias-r13-20261019T123621Z-bypass-before.log
  shows `observed=supported` CLEAN on an out-of-root alias at the pre-round
  gate; -after.log shows the crit refusal at the landed gate).

## What the adversaries caught (carried forward, named)

TOCTOU (stat-then-read), same-device bind mounts (nlink=1 — the mount
boundary is stat-invisible), unmeasurable-stat fallback skipping the alias
check, and the /tmp battery artifact: a gate copy outside the lane breaks
LANE_ROOT-relative pointer resolution (sweeps-r5 S4) — battery pre-round
copies must run from inside tools/ (recorded in alias-r13-20261019T123621Z-battery.log).

## Receipts

evidence/alias-r13-20261019T123621Z-{selftest,bypass-before,bypass-after,battery}.log;
gate 6b17e50cc9b61dda…; selftest PASS (102), cases 1-98 byte-identical; drift none vs
the r12 baseline (no re-pin — the canonical invocation is unchanged).
