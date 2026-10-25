# W2ExecNumstat

Axes: operability, calibration, depth. No commit. No `jj`. No network.

## Three paths

Predicate R44-C2 names "the three modified paths" (`corpus/evidence/round44/claims.md`). They are the `MODIFIED` tuple in `corpus/evidence/round44/c2-count.py` (lines 59–63), not every dirty path:

- `.ufo/waves/round-40/w1/swarm-registry.json`
- `.ufo/waves/round-41/w1/swarm-registry.json`
- `corpus/evidence/round41/receipts/cells/cells.json`

## Command and output

```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --numstat -- .ufo/waves/round-40/w1/swarm-registry.json .ufo/waves/round-41/w1/swarm-registry.json corpus/evidence/round41/receipts/cells/cells.json
```

```
36	34	.ufo/waves/round-40/w1/swarm-registry.json
427	214	.ufo/waves/round-41/w1/swarm-registry.json
149	36	corpus/evidence/round41/receipts/cells/cells.json
```

Exit code 0 (`echo EXIT:$?` printed `EXIT:0`). Columns are added, deleted, path. Sum of those columns, not a git line: 612 added, 284 deleted.

## What this numstat is

`git diff --numstat` here is working tree versus index. The same three paths with `--cached` printed no lines and exited 0. `git status --short --` on them:

```
 M .ufo/waves/round-40/w1/swarm-registry.json
 M .ufo/waves/round-41/w1/swarm-registry.json
 M corpus/evidence/round41/receipts/cells/cells.json
 M tools/parent-lifetime.sh
```

HEAD is detached at `043f19a1db91288947493d9f879e61e7a9f07241`. Claims base is `e6983f6e242c7b82bd9a9c5ee170257624e8f109` (`git cat-file -t` printed `commit`). `git diff --numstat e6983f6e242c7b82bd9a9c5ee170257624e8f109 HEAD --` the three paths printed no lines (exit 0), so those committed blobs match the claims base. Worktree versus that base printed the same three numstat lines as the command above (exit 0). This does not say the rest of HEAD matches the claims base.

## Not the fourth dirty path

Unfiltered `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --numstat` also printed `3	1	tools/parent-lifetime.sh`. That path is modified and unstaged. It is not in `c2-count.py` `MODIFIED` and is not one of the three.

## Not hunk verification, not C2=PASS

Numstat is line counts. It is not a hunk review. R44-C2 requires each of the three to be `left-named` with a reason containing `not hunk-verified`. `test -f corpus/evidence/round44/disposition.tsv` failed; the check printed `TABLE=absent`. This seat did not run `c2-count.py` and does not claim `C2=PASS`. Nothing was committed.
