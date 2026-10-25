# MutIndentGuard — indented collision guard re-run

Role: mutation tester (leaf, no subagents). Probe date 2026-10-24.
Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. `git rev-parse HEAD` (read-only) printed `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`, the measured commit. No lane production file, git index, jj state, fleet file, sibling, or `/home/vgpnk/Projects/shokuknow` path was written. No network. Scratch only: `/tmp/hyaku/chousa-r43/w1/MutIndentGuard/`.

Axes: **operability** (the guard command re-runs and exits 0), **calibration** (re-run bytes match the committed id lists; S118 is in `fixture-collisions` and not in `column-zero-ids`), **depth** (0–3 ASCII spaces vs column-zero vs the 4-space miss, plus one indent-byte mutant). Not a C1/C2/C3 score. Not a contract change.

## Claimed invariant

Lesson `corpus/lessons/round-43.md` line 56: the indented-fixture guard (`  | S118 |`) produces a nonempty collision; a column-zero-only pattern misses that indented row (`assimilation/guard/`). Census parser (`scripts/sources-census.sh` lines 40–42 and 541, 615–616) accepts `^ {0,3}\|` and ignores 4 or more leading ASCII spaces. The prompt's collision extractor is `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` then `grep -oE 'S[0-9]+'`. Column-zero-only is the same with `^\|`.

Plausible defect challenged: the first leading byte of the indented S118 row is not an ASCII space (tab). If the detector still reported S118 in the collision set, the space-class bound would be unenforced.

## Re-run (pristine guard bytes, not rewritten)

Fixture bytes (`od -An -tx1`), 92 bytes, sha256 `34d228d232d870fa51579ae52da0bab44f721385963daf49bb685b626e464818`:

```
 20 20 7c 20 53 31 31 38 20 7c 20 69 6e 64 65 6e
 74 65 64 20 73 74 61 67 65 64 20 63 6f 6c 6c 69
 73 69 6f 6e 0a 7c 20 53 30 37 37 20 7c 20 63 6f
 6c 75 6d 6e 2d 7a 65 72 6f 0a 20 20 20 20 7c 20
 53 31 31 39 20 7c 20 66 6f 75 72 2d 73 70 61 63
 65 2d 6d 75 73 74 2d 6d 69 73 73 0a
```

`cat -A` of `indented-registry.md`:

```
  | S118 | indented staged collision$
| S077 | column-zero$
    | S119 | four-space-must-miss$
```

Commands (pipefail; each pipeline exit 0). Staged set: `assimilation/staged-ids` sha256 `c22b2b89703afc4eb53243192391ca0e3a40e44532615236d2c349cbe97066a2`.

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' \
  .../assimilation/guard/indented-registry.md | grep -oE 'S[0-9]+' | sort
grep -oE '^\|[[:space:]]*S[0-9]{3,}' \
  .../assimilation/guard/indented-registry.md | grep -oE 'S[0-9]+' | sort
comm -12 <rerun-fixture-ids> .../assimilation/staged-ids
```

Re-run stdout (`cat -A`):

```
fixture-ids:
S077$
S118$
fixture-collisions:
S077$
S118$
column-zero-ids:
S077$
```

`cmp` against the committed guard files: `fixture-ids` exit 0, `fixture-collisions` exit 0, `column-zero-ids` exit 0. `fixture-ids` and `fixture-collisions` share sha256 `a37242a0390d67897bc92c72211b2b510d3335e2c016879289ca113b5b1e6cef` (10 bytes) because both extracted ids are in the staged set. `column-zero-ids` sha256 `5535c528f31a279120cf3948a1c6f74fd8cd091547d8619ccce49b58fd9b03b8` (5 bytes).

Membership from the re-run, not from a prior reading:

- `fixture-collisions` contains S118: YES
- `column-zero-ids` contains S118: NO
- `fixture-ids` contains S119: NO
- `staged-ids` contains S119: YES (4-space row is staged and must miss)

## Pasted files

`assimilation/guard/fixture-collisions` (full file):

```
S077
S118
```

`assimilation/guard/column-zero-ids` (full file):

```
S077
```

Confirmation holds: S118 is in `fixture-collisions` and is not in `column-zero-ids`.

## Mutant, detector, output, verdict

Isolated copy: `/tmp/hyaku/chousa-r43/w1/MutIndentGuard/mut/indented-registry.md`, copied from the guard fixture. Lane bytes were not the mutation target.

- **Mutant:** one byte at offset 0, `0x20` → `0x09` (first of the two leading spaces on the S118 line becomes a tab). Length stayed 92. Mutated sha256 `aedaeadd6782bdc1c72f7e7795f14de3fa4de40344397cb8ab050d2115c15eb0`. `cat -A` first line: `^I | S118 | indented staged collision$`.
- **Expected detector:** the same two greps plus `comm -12` against `staged-ids`. Pass (exit 0) only if `fixture-collisions` contains S118 and `column-zero-ids` does not. Detector script sha256 `906b653167d5dc5545010da90bd3a484c74a4c124966283470a3e662d08062ab` (unchanged across the three runs).

Pristine output (exit 0):

```
fixture-ids:
S077$
S118$
fixture-collisions:
S077$
S118$
column-zero-ids:
S077$
COLLISIONS_CONTAINS_S118=1
COLUMN_ZERO_CONTAINS_S118=0
DETECTOR=PASS
```

Mutated output (exit 1):

```
fixture-ids:
S077$
fixture-collisions:
S077$
column-zero-ids:
S077$
COLLISIONS_CONTAINS_S118=0
COLUMN_ZERO_CONTAINS_S118=0
DETECTOR=FAIL
```

**Verdict: killed.** Baseline was PASS/exit 0, so this is not inconclusive. The kill is the collisions half (`COLLISIONS_CONTAINS_S118` 1→0). Column-zero still does not contain S118; the tab did not become a column-zero hit. A surviving mutant would have been a coverage finding only. This kill is not permission to change the 0–3 ASCII-space contract.

## Restoration evidence

Restored by copying the pristine scratch bytes back over the mutated file.

```
34d228d232d870fa51579ae52da0bab44f721385963daf49bb685b626e464818  pristine/indented-registry.md
34d228d232d870fa51579ae52da0bab44f721385963daf49bb685b626e464818  mut/indented-registry.md
cmp restored exit=0
```

Restored detector: `COLLISIONS_CONTAINS_S118=1`, `COLUMN_ZERO_CONTAINS_S118=0`, `DETECTOR=PASS`, exit 0. Same lists as pristine (`S077`/`S118`, `S077`/`S118`, `S077`).

Lane guard hashes after the probe equal the before hashes:

```
34d228d232d870fa51579ae52da0bab44f721385963daf49bb685b626e464818  assimilation/guard/indented-registry.md
a37242a0390d67897bc92c72211b2b510d3335e2c016879289ca113b5b1e6cef  assimilation/guard/fixture-ids
a37242a0390d67897bc92c72211b2b510d3335e2c016879289ca113b5b1e6cef  assimilation/guard/fixture-collisions
5535c528f31a279120cf3948a1c6f74fd8cd091547d8619ccce49b58fd9b03b8  assimilation/guard/column-zero-ids
```

`cmp` of the lane fixture against the pristine scratch copy: exit 0.
