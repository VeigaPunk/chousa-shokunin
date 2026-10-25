# W2ConnSibling

## Matching paths

none

Assigned query: `Memento` or `RFC 7089` (also `RFC7089`) in files named `PROVINCE.md` under `/home/vgpnk/Projects/shokunin`. No path matched. No sibling file was edited.

## Axes

operability, calibration, depth. This seat only searches. It does not admit a province note, edit a sibling, or score C3.

## Evidence

Ripgrep 15.2.0 (rev e89fff89ac). A no-match `rg` exits 1. `xargs` turns that into 123 when every invocation exits 1–125. Confirmed on the chousa file alone: `single_rg_exit:1`.

Lane roots. Twenty-one `*/PROVINCE.md` files, 249771 bytes, including chousa. `wc -c` total line is `249771 total`.

```
rg -n --stats -e 'Memento' -e 'RFC 7089' -e 'RFC7089' <21 lane-root PROVINCE.md paths>
```

```
0 matches
0 matched lines
0 files contained matches
21 files searched
0 bytes printed
249771 bytes searched
lane_root_rg_exit:1
```

The 21 paths are the lane roots of audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi. No fleet-root `PROVINCE.md`. No `PROVINCE.md` in `research/`, `scripts/`, `templates/`, `write/`, or `tameshi-shokukin/`.

Wider census, not only lane roots. `find` pruned directories named `.git`, `worktrees`, `clone`, and `node_modules`, then printed paths. `census_find_exit:0`. `wc -l` printed `1565`. That set includes the 21 roots, two `.tower/jj-probe/*/PROVINCE.md` copies, three `kotodama-shokunin/.scratch/*/PROVINCE.md` files, and 1486 `kagi-shokunin/.ufo/.../PROVINCE.md` sandbox copies. `xargs -d '\n' rg --stats` split into two invocations (859 + 706 = 1565):

```
0 matches
0 matched lines
0 files contained matches
859 files searched
0 bytes printed
11758461 bytes searched

0 matches
0 matched lines
0 files contained matches
706 files searched
0 bytes printed
9692881 bytes searched
xargs_rg_cs_exit:123
```

Same 1565, case-insensitive `memento` / `rfc 7089` / `rfc7089`: also 0 matches, 859 + 706 files, same byte counts, `xargs_rg_ci_exit:123`.

Near-miss on those 1565, not the assigned query: `7089`, `TimeGate`, `timegate`, `memento`. 0 matches, same two batches, `near_exit:123`. A hit on `RFC-7089` or `Memento-Datetime` would have matched `7089` or `Memento`. Neither form appeared.

Nine files the name-prune skipped, then searched separately. All 0 matches, 176521 bytes, `extra_rg_exit:123`. Case-insensitive `memento` / `rfc 7089` / `7089` / `TimeGate` on the same nine: 0 matches, `extra_near_exit:123`.

```
/home/vgpnk/Projects/shokunin/kagi-shokunin/.ufo/waves/round-28/sandboxes/RevScorecardShape-7/clone/PROVINCE.md
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/runtime/KaidokuR23.RunBefore/clone/PROVINCE.md
/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/worktrees/AppImageLibraries/PROVINCE.md
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/DispatchLedger/PROVINCE.md
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/FreezeOrder/PROVINCE.md
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutDispatchLedger/PROVINCE.md
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutFreezeOrder/PROVINCE.md
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/MutRetentionGate/PROVINCE.md
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/RetentionGate/PROVINCE.md
```

Chousa's own province was read in full (17 lines, `wc -c` = 880). It does not contain `Memento` or `7089`. Closing line: `**Out of province → report, never absorb.**`

Related tokens on the 21 roots only, not counted as the assigned query: `TimeGate`, `Accept-Datetime`, `Memento-Datetime`, `7089`, `web archive`, `version-anchor`, `version anchor`. 0 matches, 21 files, 249771 bytes, `related_exit:1`.

## Findings

1. No sibling province holds the assigned tokens. The operational set is the 21 lane roots. The wider 1565 plus the nine worktree/clone files also have none. There is no path to paste and no sibling sentence to absorb.

2. Chousa does not already hold the note either. A Memento version-anchor sentence is not in `chousa-shokunin/PROVINCE.md`. That is a read of this file, not a score of the scout seat.

3. Do not treat exit 1 as `C3=PASS` or `C3=FAIL`. C3 is the knowledge entry, the row URL, and the frozen quote. This grep does not read that entry.

4. Do not edit siblings to "add the overlap." None of them name the protocol. The chousa refuse line already says report, never absorb. Writing `Memento` or `RFC 7089` into kagi, mori, kaidoku, or any other lane province would create the overlap this search did not find.

Proposed move (frontier text only; do not edit frozen `claims.md`, any `PROVINCE.md`, or a sibling repo): (a) matching paths stay none — no sibling province is a prior holder of `Memento` or `RFC 7089`. (b) do not retitle a sibling scope sentence to cover the version anchor. (c) do not treat this grep as a C3 measurement.

## Limits

An unbounded `find` of every `PROVINCE.md` under `/home/vgpnk/Projects/shokunin` was killed at 60s. A second count restricted to `*/.ufo/*/.ufo/*` was killed at 90s. Cause: `mori-shokunin/.ufo/worktrees/round-19/ContentGate/` is a real directory chain, not a symlink, repeating `.ufo/worktrees/round-19/ContentGate` at least eight levels. `ContentGate/PROVINCE.md` itself is missing at depth 1 and depth 2. One nested copy that does exist is byte-identical to a file already in the nine:

```
73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130
  mori-shokunin/.ufo/worktrees/round-18/RetentionGate/PROVINCE.md
  mori-shokunin/.ufo/worktrees/round-19/ContentGate/.ufo/worktrees/round-18/RetentionGate/PROVINCE.md
cmp: identical
```

That shows the chain repeats an already-negative file at the first extra level. It does not prove every deeper copy is identical. Those deeper copies were not listed. `find` with `-maxdepth 8` under `*/.ufo/worktrees/*` printed 6 `PROVINCE.md` paths, all in the nine already searched. Round-19 `ContentGate`, `ContentGateActual`, and `ContentGateSparse` have no top-level `PROVINCE.md` (`find -maxdepth 2` printed nothing).

A separate list under three known nest roots, pruning a third `.ufo`, had 1573 paths. `rg` on that list: 0 matches, 843 + 730 files, `one_extra_exit:123`. Eighty-three of those paths were not in the 1565 or the nine; they are clone-of-sandbox copies (`kagi` round-28 `clone/.ufo/waves/...`, `kaidoku` round-23 `clone/.ufo/waves/...`). The superset search covers them. It does not cover the ContentGate chain past the identical copy above.

Risk if ignored: a parent walks the ContentGate chain, treats a repeated `RetentionGate/PROVINCE.md` as a new sibling claim, or edits a sibling province because this report said none.
