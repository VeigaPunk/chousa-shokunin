# Evidence index findings: rounds 21–23

Observed: `corpus/evidence/README.md:580` places the r12–r23 receipt rows under `## Round-8 gate-baseline receipts`; the table starts at line 624. Of its 43 r12–r23 rows (`README.md:629–671`), the 12 target rows are r21 at 660–663, r22 at 664–667, and r23 at 668–671. Drafts below preserve those row texts verbatim.

`ls -1 corpus/evidence/` showed all 12 target files; `sha256sum` returned these prefixes (first 12 hex digits):

| README line | Filename | SHA-256 prefix |
|---:|---|---|
| 660 | `ptr-r21-20261019T184000Z-selftest.log` | `1b26eccd98bb` |
| 661 | `ptr-r21-20261019T184000Z-demo.log` | `d01576d3587b` |
| 662 | `ptr-r21-20261019T184000Z-battery.log` | `3bb217c1f9f4` |
| 663 | `ptr-r21-20261019T184000Z-drift.log` | `d489fb31f5eb` |
| 664 | `deny-r22-20261019T190000Z-selftest.log` | `64f351dfe3c1` |
| 665 | `deny-r22-20261019T190000Z-demo.log` | `9d63885cd4d0` |
| 666 | `deny-r22-20261019T190000Z-battery.log` | `3bb217c1f9f4` |
| 667 | `deny-r22-20261019T190000Z-drift.log` | `d489fb31f5eb` |
| 668 | `fanchor-r23-20261019T192000Z-selftest.log` | `dc9aaa6c2962` |
| 669 | `fanchor-r23-20261019T192000Z-demo.log` | `2bb3db8a9d7b` |
| 670 | `fanchor-r23-20261019T192000Z-battery.log` | `3bb217c1f9f4` |
| 671 | `fanchor-r23-20261019T192000Z-drift.log` | `d489fb31f5eb` |

Unindexed files: comparing the evidence directory's `*.log` names with README backtick-indexed names returned `scope-r12-20261019T115519Z-battery.log` (receipt; SHA-256 `27a97fd158b6…`, no README row) and `round25-measure-before.log` (pre-registration before-output, not a stamped round receipt; `round25-claims.md` names it). Round 16 is outside the requested set; no r16 row occurs in the r12–r23 table and no r16 receipt filename appeared in the directory inventory.

## Round-21 pointer-boundary receipts — stamp 20261019T184000Z

SCORECARD.md lines 1086–1099 report gate SHA `49b36759…` before → `bfc291ef…` after and selftest `PASS (128 cases, 0 skipped)` (cases 1–124 unchanged). Rows copied verbatim from `corpus/evidence/README.md:660–663`:
| `ptr-r21-20261019T184000Z-selftest.log` | r21: `PASS (128 cases, 0 skipped)`; cases 1–124 `cmp` byte-identical vs `verify-r20-…-selftest.log` |
| `ptr-r21-20261019T184000Z-demo.log` | before/after pair: pre-round gate (`b057245`) passes CLEAN on a traversal pointer; landed gate refuses `POINTER_UNRESOLVED` warn |
| `ptr-r21-20261019T184000Z-battery.log` | masked battery (banner/ts) vs the pre-round gate: A/B/C-r9, claims-r2, chain-r3, sweeps-r5, integrity-r7, full-r6 — ALL IDENTICAL |
| `ptr-r21-20261019T184000Z-drift.log` | `--drift` vs the r12 baseline → `GATE_DRIFT: none`, exit 0 (no re-pin needed) |

## Round-22 denylist-path-start-bypass receipts — stamp 20261019T190000Z

SCORECARD.md lines 1142–1156 report gate SHA `bfc291ef…` before → `dfb798b4…` after and selftest `PASS (132 cases, 0 skipped)` (cases 1–128 unchanged). Rows copied verbatim from `corpus/evidence/README.md:664–667`:
| `deny-r22-20261019T190000Z-selftest.log` | r22: `PASS (132 cases, 0 skipped)`; cases 1–128 `cmp` byte-identical vs `ptr-r21-…-selftest.log` |
| `deny-r22-20261019T190000Z-demo.log` | before/after pair: pre-round gate (`10083e1`) passes CLEAN on `.config/agent-token.txt` (no `./` prefix); landed gate refuses `CLAIM_SOURCE_SESSION` crit |
| `deny-r22-20261019T190000Z-battery.log` | masked battery (banner/ts) vs the pre-round gate: A/B/C-r9, claims-r2, chain-r3, sweeps-r5, integrity-r7, full-r6 — ALL IDENTICAL |
| `deny-r22-20261019T190000Z-drift.log` | `--drift` vs the r12 baseline → `GATE_DRIFT: none`, exit 0 (no re-pin needed) |

## Round-23 fenced-heading-anchor-false-positive receipts — stamp 20261019T192000Z

SCORECARD.md lines 1196–1205 report gate SHA `dfb798b4…` before → `b5d0f93d…` after and selftest `PASS (133 cases, 0 skipped)` (cases 1–128 unchanged). Rows copied verbatim from `corpus/evidence/README.md:668–671`:
| `fanchor-r23-20261019T192000Z-selftest.log` | r23: `PASS (133 cases, 0 skipped)`; cases 1–128 `cmp` byte-identical vs `deny-r22-…-selftest.log` |
| `fanchor-r23-20261019T192000Z-demo.log` | before/after pair: pre-round gate (`fb70ddb`) verifies a fenced heading as a real anchor; landed gate refuses `CHAIN_ANCHOR_NOT_FOUND` warn |
| `fanchor-r23-20261019T192000Z-battery.log` | masked battery (banner/ts) vs the pre-round gate: A/B/C-r9, claims-r2, chain-r3, sweeps-r5, integrity-r7, full-r6 — ALL IDENTICAL |
| `fanchor-r23-20261019T192000Z-drift.log` | `--drift` vs the r12 baseline → `GATE_DRIFT: none`, exit 0 (no re-pin needed) |

VERDICT: All twelve r21–r23 receipt rows map to present files with recorded SHA-256 prefixes; the three drafted sections carry their respective gate transitions and selftest counts. The r12 battery receipt is unindexed; round 16 is out of scope and has no observed receipt row/file.
Installs: none.