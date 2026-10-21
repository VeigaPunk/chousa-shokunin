# Round 12–15 evidence-index findings
Observed: `corpus/evidence/README.md:580` labels the block `Round-8 gate-baseline receipts`; target rows 629–643 remain beneath it.
Heading moves follow knowledge-note titles at `corpus/knowledge/{scope-refusal-r12,hardlink-alias-r13,mount-alias-r14,root-slash-boundary-r15}.md:1`; gate/selftest prefixes follow `SCORECARD.md:520-752` and note metadata.
`ls -l` confirmed the 15 indexed files below exist; `sha256sum` was run on each absolute `corpus/evidence/` path (prefixes shown).
| Round | README line, filename (SHA-256 prefix) |
|---|---|
| 12 | 629 `scope-r12-20261019T115519Z-selftest.log` (d2911cb9); 630 `scope-r12-20261019T115519Z-A-fix.log` (3738ab6a); 631 `scope-r12-20261019T115519Z-drift-r8.log` (bcdfe5cc) |
| 13 | 632 `alias-r13-20261019T123621Z-selftest.log` (8480ae90); 633 `alias-r13-20261019T123621Z-bypass-before.log` (0468f501); 634 `alias-r13-20261019T123621Z-bypass-after.log` (1b0b33bb); 639 `alias-r13-20261019T123621Z-battery.log` (830d7c2d) |
| 14 | 635 `mount-r14-20261019T132025Z-selftest.log` (78659577); 636 `mount-r14-20261019T132025Z-bypass-before.log` (1014f240); 637 `mount-r14-20261019T132025Z-bypass-after.log` (928733b6); 638 `mount-r14-20261019T132025Z-battery.log` (f34b459b) |
| 15 | 640 `root-r15-20261019T152000Z-selftest.log` (6f32b940); 641 `root-r15-20261019T152000Z-demo.log` (513995e7); 642 `root-r15-20261019T152000Z-battery.log` (3bb217c1); 643 `root-r15-20261019T152000Z-drift.log` (d489fb31) |

## Round-12 scope-refusal screening receipts — stamp 20261019T115519Z
Gate sha256 prefixes `46f5ddb3… → 91a01695…`; selftest `PASS (98 cases)` (85→98; `SCORECARD.md:520-528`).

| Receipt (sha256) | Shows | Key result |
|---|---|---|
| `scope-r12-20261019T115519Z-selftest.log` | r12 acceptance: `PASS (98 cases)`; cases 1–85 `cmp` byte-identical vs `pin-r8-…-selftest.log` |
| `scope-r12-20261019T115519Z-A-fix.log` | A-r9 post-fix `verify-all` CLEAN at `dfd2ae1a…` (run without `--json`; manifest untouched) |
| `scope-r12-20261019T115519Z-drift-r8.log` | `--drift` vs the r8 baseline → `GATE_DRIFT: GATE record_sha256`, exit 1 (recorded reason) |

## Round-13 hardlink-alias boundary receipts — stamp 20261019T123621Z
Gate sha256 prefixes `91a01695… → 6b17e50cc9b61dda…`; selftest `PASS (102 cases)` (98→102; `SCORECARD.md:629-637`).

| Receipt (sha256) | Shows | Key result |
|---|---|---|
| `alias-r13-20261019T123621Z-selftest.log` | r13: `PASS (102 cases)`; cases 1–98 `cmp` byte-identical vs `scope-r12-…-selftest.log` |
| `alias-r13-20261019T123621Z-bypass-before.log` | the r2 residual reproduced live: a claim through an in-root hardlink alias of an out-of-root file reads `observed=supported` CLEAN at the pre-round gate (rc=0) |
| `alias-r13-20261019T123621Z-bypass-after.log` | same fixture at the landed gate: `CLAIM_SOURCE_MULTILINKED` crit, `observed=refused` (rc=1) |
| `alias-r13-20261019T123621Z-battery.log` | masked battery (banner/ts) vs the pre-round gate, run with LANE_ROOT intact (temp copy inside `tools/`): A/B/C-r9, r6, r7, claims-r2, chain-r3, sweeps-r5, six controls — ALL IDENTICAL; records the /tmp-copy LANE_ROOT artifact |

## Round-14 mount-alias (cross-device) boundary receipts — stamp 20261019T132025Z
Gate sha256 prefixes `6b17e50c… → d8bbd0bf…`; selftest `PASS (106 cases, 0 skipped)` (102→106; `SCORECARD.md:690-697`).

| Receipt (sha256) | Shows | Key result |
|---|---|---|
| `mount-r14-20261019T132025Z-selftest.log` | r14: `PASS (106 cases, 0 skipped)`; cases 1–102 `cmp` byte-identical |
| `mount-r14-20261019T132025Z-bypass-before.log` | a tmpfs mounted over an in-root dir (unprivileged userns): the claim reads `observed=supported` CLEAN at the pre-round gate (rc=0) |
| `mount-r14-20261019T132025Z-bypass-after.log` | same fixture at the landed gate: `CLAIM_SOURCE_CROSS_DEVICE` crit, `observed=refused` (rc=1) |
| `mount-r14-20261019T132025Z-battery.log` | masked battery vs the pre-round gate, LANE_ROOT intact: ALL IDENTICAL; records the ns-fixture recipe |

## Round-15 root-slash boundary dead-arm receipts — stamp 20261019T152000Z
Gate sha256 prefixes `d8bbd0bf… → dd0951d7…`; selftest `PASS (110 cases, 0 skipped)` (106→110; `SCORECARD.md:743-752`).

| Receipt (sha256) | Shows | Key result |
|---|---|---|
| `root-r15-20261019T152000Z-selftest.log` | r15: `PASS (110 cases, 0 skipped)`; cases 1–106 `cmp` byte-identical vs `mount-r14-…-selftest.log` |
| `root-r15-20261019T152000Z-demo.log` | before/after pair: pre-round gate (`aabf7f4`) refuses `/etc/hostname` `OUT_OF_CORPUS` crit at `CHOUSA_ROOT=/`; landed gate reads it `CLEAN` `1/1` |
| `root-r15-20261019T152000Z-battery.log` | masked battery (banner/ts) vs the pre-round gate: A/B/C-r9, claims-r2, chain-r3, sweeps-r5, integrity-r7, full-r6 — ALL IDENTICAL |
| `root-r15-20261019T152000Z-drift.log` | `--drift` vs the r12 baseline → `GATE_DRIFT: none`, exit 0 (no re-pin needed — no banner/VERSION/canonical-surface change) |

Unindexed scoped receipt: `scope-r12-20261019T115519Z-battery.log` exists (284 B; SHA-256 prefix `27a97fd1`), but exact-name search in `corpus/evidence/README.md` returns no match. Round 16 is outside this [12–15] slice; README has no `r16-` receipt row and `corpus/evidence/*r16*` yielded no files.
VERDICT: Four sections drafted with the indexed rows verbatim; all 15 referenced files exist and hash as listed. Installs: none.