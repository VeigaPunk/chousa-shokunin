# Sweep symlink escape (round 19)

source: tools/research-gate.sh (sweep_path_guarded :1779-1812; verify_sweeps match check :1970-1995); receipts: corpus/evidence/symlink-r19-20261019T174500Z-{demo,selftest,battery,drift}.log; round-16 named debt closed
verified-at: 2026-10-19 (round 19, landed; selftest PASS (122 cases, 0 skipped); gate sha 9f163807…)
recheck: `bash tools/research-gate.sh --selftest` (cases 120–122 pin the escape class); the demo record in `evidence/symlink-r19-…-demo.log`

## The escape

`sweep_path_guarded` canonicalizes the glob's literal BASE directory and
checks it against the allowed roots. `verify_sweeps` then expands the glob
and counts each match without canonicalizing it. A wildcard inside an
in-root directory can match a symlink whose target is outside both roots —
the guard sees the in-root base while the glob reaches the outside file.

Two escape shapes:

- **Leaf symlink**: `dir/escape.md` → `/outside/file`; `dir/*.md` matches
  the symlink, `readlink -f` resolves to the outside target.
- **Directory symlink**: `dir/linkdir` → `/outside/dir`; `dir/*/*.md`
  traverses the symlinked dir to outside files.

## The fix

After `sweep_glob_matches` returns, every match is canonicalized
(`readlink -f`) and checked against `in_root` for both `root_r` and
`lane_r`. Any match outside both roots refuses the whole sweep —
`SWEEP_LOCATION_OUT_OF_CORPUS` crit, `observed=refused`, no match paths
reported. Matches that canonicalize inside either root are unaffected.

## Named limits

- The check runs post-expansion: bash already traversed the symlinked
  directory during glob expansion (names only, never content). A "refused
  unopened" contract covers the match list, not the expansion traversal.
- A check-to-use race remains possible if symlinks change between the
  canonicalization and the count — same TOCTOU class as the claims/chain
  probes.
- `--root /` makes the guard vacuous by declaration (the whole filesystem
  is in-corpus) — unchanged from the r15 contract.
