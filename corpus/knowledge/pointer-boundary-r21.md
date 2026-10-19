# Pointer boundary (round 21)

source: tools/research-gate.sh (ptr_resolves_meta :591-615; check_pointer :611-642; verify_record :760+; verify_chain structural :947-983); receipts: corpus/evidence/ptr-r21-20261019T184000Z-{demo,selftest,battery,drift}.log; round-20 named debt closed
verified-at: 2026-10-19 (round 21, landed; selftest PASS (128 cases, 0 skipped); gate sha bfc291ef…)
recheck: `bash tools/research-gate.sh --selftest` (cases 125–128 pin the escape class); the demo record in `evidence/ptr-r21-…-demo.log`

## The defect

`ptr_resolves_meta` checks whether a record's pointer resolves to a readable
local file. For relative paths it used raw `-f "$ROOT/$f"` or `-f
"$LANE_ROOT/$f"` — no canonicalization. A `lib/../../etc/passwd` or a
symlink to outside passed if the file existed under the raw path. For
absolute paths it checked `in_root` against `root_r` only — an absolute
pointer under `LANE_ROOT` was refused incorrectly.

## The fix

The candidate is canonicalized with `readlink -f` (resolving `..` and
symlinks), then checked with `in_root` against BOTH roots. The denylist
is applied to the canonical target too — a benign symlink to
`.config/passwd` is refused even when the citation itself was clean.

## Named limits

- The `.config` path-start bypass (`is_denylist_path` uses `*/.config/*`,
  missing `.config/foo`) is closed by the canonical check — the canonical
  path contains the resolved `.config` component which the pattern catches.
  A direct `.config/foo` citation (not through a symlink) still bypasses
  the path-start form — a separate named debt.
- The chain `heading` anchor false-positive (headings inside fences match)
  is a different function (`chain_anchor_heading`, not `load_sections`) —
  named debt for a future round.
