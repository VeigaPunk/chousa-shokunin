# Scout report — by-document binding recheck at 5e8c7ad (round 45 w2)

Scout: `L1Chousa45.ScoutRenumberMap` (leaf; no dispatch, no fetch, no lane writes).
Item: for every line of `renumber-map.tsv`, confirm staged-row URL = map URL = lane-row URL;
re-run the 0-3-space id-collision extraction on the tip registry vs the staged append;
confirm the committed pre-append `collisions` file is empty.

## Method / sources
- Lane tree measured over committed bytes: `git archive 5e8c7ad2f7b8254d83358820286e3d12ca4672d1` → `/tmp/chousa-r45-ScoutRenumberMap/tree` (read-only; deleted after).
- Staged append (read-only): `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md`.
- Map: `.ufo/waves/round-45/assimilation/renumber-map.tsv` (3 rows, all `bound_by=url-equality`).
- Extraction pattern (same as wave 1 / census parser): `^ {0,3}\|\s*S[0-9]{3,}` (row start, 0-3 spaces, `|`, optional space, `S`+3 digits).

## 1. By-document binding (3/3 hold)
Verbatim decisive output (Python eval, fresh read of both files):

```
S139->S082: lane line 92 == https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/README.md | staged line 64 == https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/README.md | all three equal: True
S140->S083: lane line 93 == https://arxiv.org/html/2305.13117v3 | staged line 65 == https://arxiv.org/html/2305.13117v3 | all three equal: True
S132->S084: lane line 94 == https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/data/train.json | staged line 57 == https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/data/train.json | all three equal: True
ALL MAP ROWS HOLD: True
```

Each URL occurs exactly once in the lane registry (S082/S083/S084) and exactly once in the staged append (S139/S140/S132) — binding is unambiguous, no duplicate-URL ambiguity.

## 2. Id-collision extraction at tip (0-3-space pattern)

```
reg count 84 unique 84 first/last S001 S084
stag count 114 unique 114 first/last S082 S195
intersection (reg ∩ staged): ['S082', 'S083', 'S084']
```

- Tip registry `corpus/SOURCES.md`: 84 unique row-start ids, S001–S084.
- Staged append: 114 unique row-start ids, S082–S195.
- Collision set = **exactly {S082, S083, S084}** — the adopted lane ids. This is **expected and NOT a defect**: the lane rows bind by URL/name equality with AVeriTeC documents (S082 README, S083 arXiv 2305.13117v3, S084 train.json), while the staged append's S082/S083/S084 strings name different documents (PRISMA-S, Cochrane Handbook ch.4, RFC 7089 — confirmed in wave-1 report `w1/ScoutCollisionRecheck.md`). The id strings collide; the documents do not. No arithmetic renumbering was applied; re-pointing is by document only.

## 3. Committed pre-append `collisions` file
`git show 5e8c7ad2f7b8254d83358820286e3d12ca4672d1:.ufo/waves/round-45/assimilation/collisions` → **0 bytes (empty)**, consistent with the pre-adoption registry (S001–S081) vs staged (S082–S195) intersecting on nothing. The non-empty `guard/collisions` (S084) is the indented-fixture guard, unrelated to the real check.

## Verdict
- By-document map: **holds** (3/3 rows; staged URL = map URL = lane URL).
- Collision extraction at tip: set is exactly S082–S084, as expected; not a defect (URL-bound).
- Committed `collisions`: empty, as claimed.

## Commands run
1. `git archive` → scratch tree; `git show` of committed `collisions` (0 bytes).
2. Python eval: 0-3-space row-start id extraction on both files, intersection, per-row URL triple equality, URL uniqueness.
No tool installs/updates. Scratch `/tmp/chousa-r45-ScoutRenumberMap/` deleted. No network egress.
