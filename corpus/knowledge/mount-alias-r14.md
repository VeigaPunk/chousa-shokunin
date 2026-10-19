# Mount-alias (cross-device) boundary (round 14)

source: tools/research-gate.sh (claim_source_path device probe); lessons/2026-10-19-hardlink-alias-boundary.md (companion); receipts evidence/mount-r14-20261019T132025Z-{bypass-before,bypass-after}.log
verified-at: 2026-10-19 (round 14; selftest cases 103-106, 0 skipped; gate sha256 d8bbd0bf6890d3c4…)
recheck: the bypass pair recipes (evidence/mount-r14-20261019T132025Z-bypass-*.log) + `bash tools/research-gate.sh --selftest` after any gate edit

## The gap

Rounds 12-13 sealed two alias routes — symlinks (readlink -f resolves the
true path and the boundary re-checks) and hardlinks (the nlink probe) — but
a BIND alias was still readable: it keeps its in-root path (readlink -f
follows symlinks, never mounts) and its nlink (a bind is not a link), so
both earlier probes pass. Measured live (receipts
`mount-r14-20261019T132025Z-bypass-{before,after}.log`): a tmpfs mounted inside an
unprivileged user+mount namespace over an in-root directory reads
`observed=supported` CLEAN at the pre-round gate and refuses
`CLAIM_SOURCE_CROSS_DEVICE severity=crit` at the landed gate.

## The rule (r14)

At the same shared chokepoint, one `stat -c '%s %h %d'` probe now serves
three checks, in order: nlink (r13), size (r12), then device (r14) — a
combined source reports the earliest class. The device check compares the
source's st_dev against the RESOLVING ROOT's device: the root whose prefix
matched canon (longest prefix when both match). A source on a different
superblock than the resolving root is refused unread
(`CLAIM_SOURCE_CROSS_DEVICE` / `CHAIN_SOURCE_CROSS_DEVICE`, crit).

The resolving-root rule is load-bearing: the corpus root and the lane root
can sit on different filesystems (measured on this host: $WORK tmpfs dev 57
vs the repo btrfs dev 30), and a live fixture (sweeps-r5 S4) resolves
lane-side. Comparing everything to CHOUSA_ROOT's device would false-refuse
legitimate lane-root citations — selftest case 106 exists precisely to catch
that naive implementation (and fails loudly if PROVINCE.md's pinned span
moves).

## Named limits (all measured this wave)

- **Same-device binds are stat-invisible**: a bind within one filesystem
  presents identical st_dev and nlink; only /proc/self/mountinfo path-
  walking could see it (r15+ candidate). The r14 class is CROSS-DEVICE
  aliases only — claimed narrowly, on purpose.
- **Overlay roots**: a corpus whose resolving root IS an overlay mount
  breaks the file-vs-root-dir comparison (merged files report the upper
  layer's device, not the root dir's); containers on overlayfs would
  refuse everything. Named limit + false-positive class; a root-fstype
  guard is a candidate, not landed.
- **TOCTOU** (probe-to-read mount swap) — same standing decision as r12/r13.
- **Unmeasurable stat**: the fallback path keeps only the r12 cap semantics;
  alias and device checks need %h/%d and are skipped (documented residual).
  The `wc -c` fallback reads the file to measure it (not to search content);
  "refused unread" holds for the primary stat path only. If all measurement
  fails the source is accepted — a fail-open, not a bypass.
- **Legit cross-device subtrees** inside the corpus root now refuse (the
  case-101-style trade: re-root at that filesystem instead).
- **verify-sweeps' glob surface is unclaimed**: sweeps re-measures named
  paths but never reads content; a mount alias under a swept directory is
  invisible to it (r15+ candidate).
- **Latent, discovered this wave (not r14 scope)**: `--root /` dead-arms
  the boundary case (`"$root_r"/*` becomes `//*`, matching nothing), so
  every source refuses OUT_OF_CORPUS. Fix: `in_root()` helper — closed
  round 15 (`corpus/knowledge/root-slash-boundary-r15.md`).
