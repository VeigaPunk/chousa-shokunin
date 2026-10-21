# FRegistryUsedByMissing — C3 attack: mined row with no path ⇒ `META_SOURCE_USEDBY_MISSING`

Seat `ChousaR26R.FRegistryUsedByMissing` (scout, falsify wave, round 26 attempt 1). Author-lane advice only;
not an outside judge or SHONEN claim.

## Verdict

**Not falsified.** Every shape I tried of "a `mined` row whose `used-by` names no path for the entry"
produces exactly one `FINDING META_SOURCE_USEDBY_MISSING severity=warn surface=metadata`, with the
entry verdict `drift` and exit 1 (25 negative fixtures). Six positive controls stay clean with exit 0.
Non-mined and missing rows are routed to their own codes, not to USEDBY. There are five calibration
observations below. None of them breaks the C3 spec as corrected; one is a root-dependence hazard
that conflicts with QUALITY 13.

## Target and sandbox

- Measured revision: `0e9784bd52eca456b24d0bc40921480a47f91a2b`. `git cat-file -t` returns `commit`,
  and the lane `HEAD` was the same revision when I observed it.
- Sandbox: `git archive 0e9784bd… | tar -x -C /tmp/chousa-r26-falsify-FRegistryUsedByMissing/tree`
  (rc=0).
- `sha256sum tree/tools/research-gate.sh` gives `c2c813f1…6abc6`, and
  `tree/corpus/SOURCES.md` gives `8308e629…a5aa9`. Both equal
  `round26-measured-revision.json`.
- Base registry for the population rerun: `git show ba333325…:corpus/SOURCES.md`, sha256
  `bfd47b5d8d34b0bb8ef5bfed4390996edd6bbac5d22086eb1c5042ade9f91532`.
- Runtime: GNU bash 5.3.20. I installed no tools and edited no production files. All fixtures are
  under the sandbox (`fx/`, `fy/`, `fleet/`, `pop/`).
- Command form throughout:
  `bash tree/tools/research-gate.sh verify-metadata ENTRY --root ROOT --registry REG`.
  I did not run selftest, build, lint, or the amplification probe.

## Observed: no-path shapes (all negatives caught)

Registry `fx/SOURCES.md` uses the 11-column SOURCES shape. Each entry is
`source: S### …`, `verified-at: 2026-10-20 checked the anchor quote`, `recheck: 90d`, `## Body`, and
is run with `--root fx`.

| fixture | `used-by` cell of the mined row | rc | finding |
|---|---|---|---|
| e100 | empty | 1 | `META_SOURCE_USEDBY_MISSING` S100 |
| e101 | `—` | 1 | USEDBY_MISSING S101 |
| e102 | cell absent (short row) | 1 | USEDBY_MISSING S102 |
| e103 | `, ,` | 1 | USEDBY_MISSING S103 |
| e104 | `-` | 1 | USEDBY_MISSING S104 |
| e105 | basename only `e105.md` | 1 | USEDBY_MISSING S105 |
| e106 | `corpus/other/e106.md` (same basename, other dir) | 1 | USEDBY_MISSING S106 |
| e107 | `corpus/knowledge/` | 1 | USEDBY_MISSING S107 |
| e108 | `./` | 1 | USEDBY_MISSING S108 |
| e111 | `\|\|` (empty extra cells) | 1 | USEDBY_MISSING S111 |
| e112 | `/corpus/knowledge/e112.md` | 1 | USEDBY_MISSING S112 |
| e113 | tab + spaces only | 1 | USEDBY_MISSING S113 |
| e114 | path + ` (r24)` suffix | 1 | USEDBY_MISSING S114 |
| e115 | backticked path | 1 | USEDBY_MISSING S115 |
| e118 | empty, id `S0118` (4 digits) | 1 | USEDBY_MISSING S0118 |
| emulti | `source: S119 … S100`; S119 names the entry, S100 is empty | 1 | exactly one USEDBY_MISSING, for S100 |
| fy dup | `S200` first row empty, second row names the entry | 1 | USEDBY_MISSING S200 (first row wins, per spec) |
| fy e201 | `*` | 1 | USEDBY_MISSING S201 (no glob approval) |
| fy e204 / e205 | `corpus//knowledge/…`, `corpus/./knowledge/…` | 1 / 1 | USEDBY_MISSING (only leading `./` is normalized, per correction) |
| fy eX10 | `corpus/knowledge/e?10.md` | 1 | USEDBY_MISSING S210 (no glob approval) |
| fy C3 | CRLF registry, empty cell | 1 | USEDBY_MISSING S400 |
| fy C7 | duplicate `used-by` column, first empty, second names entry | 1 | USEDBY_MISSING (first column wins) |
| fy C9 | 3-column table, short row | 1 | USEDBY_MISSING S400 |
| fy C13 | CRLF entry, empty cell | 1 | USEDBY_MISSING S501 |
| fy root=/ | `--root /`, empty cell | 1 | USEDBY_MISSING S300 |

Routing controls (these must not be classified as USEDBY):

- e116 (`queued`, empty cell) gives rc=1 and `META_SOURCE_NOT_MINED` S116.
- e117 (`Mined`, empty cell) gives rc=1 and `META_SOURCE_NOT_MINED` S117. The status match is
  case-exact.

Composition and legacy controls:

- C10 (`--as-of 2027-06-01` + `--registry`, empty cell): rc=1. The META line keeps
  `due=2027-01-18 freshness=overdue verdict=drift`, and both findings are present:
  `META_SOURCE_USEDBY_MISSING` and `META_RECHECK_OVERDUE`. This matches the composition clarification.
- C11 (directory mode, `a.md` names itself and `b.md` has an empty cell): rc=1. `a.md` is clean,
  `b.md` is drift with USEDBY_MISSING S501, and the totals are `findings=1 drift=1`.
- C12 (the same no-path entry without `--registry`): rc=0 and clean. The legacy path is unaffected.

## Observed: positive controls (all clean, rc=0, findings=0)

- e109 names its exact path.
- e110 has the list `corpus/knowledge/zz.md ,  ././corpus/knowledge/e110.md`.
- `fx/corpus/other/e106.md` is matched by `corpus/other/e106.md`, so same-basename identity is
  path-exact.
- `e 202.md` (internal space) and `e[2]09.md` (glob metacharacters in the filename) both match.
- e206 is clean under three root forms: `--root fy/r/` (trailing slash), `--root` through a symlink
  to the root, and `--root /` with a rooted path in `used-by`.
- C4 (CRLF registry with the correct path) is clean.

Real lane state:

- `verify-metadata tree/corpus/knowledge --root tree --registry tree/corpus/SOURCES.md` gives rc=1,
  `entries=32 complete=29 findings=57 drift=3`, and zero `META_SOURCE_USEDBY_MISSING`. The three
  drift entries are pre-r24 `recheck=absent` cases; the rest of the findings are
  `META_SOURCE_NO_ROW_ID` info.
- `(cd tree && verify-metadata corpus/knowledge/registry-link-r26.md --root . --registry
  corpus/SOURCES.md)` gives rc=0 and is clean.
- Frozen POP24 from the base, run against the base registry: rc=0, all 5 entries clean,
  `findings=1 drift=0`. The one finding is `META_RECHECK_ROOT_PARENT` info on
  `citation-chain-fidelity-r24.md`.
- The target `SOURCES.md` has 39 S rows on contiguous lines 11–49 (16 mined, 19 queued,
  4 rejected). No mined row has a `used-by` without a `corpus/knowledge/` path, so this case has no
  live population instance.

## Calibration observations

All of these are observed except where marked `[INFERENCE]`.

1. **Root dependence (medium; conflicts with QUALITY 13, not with the corrected C3 spec).**
   Identity is the entry path relative to `--root`. If `--root` names the fleet root, which is the
   role QUALITY 13 prescribes for recheck commands, a correctly attributed entry reports drift.
   `verify-metadata fleet/chousa-shokunin/corpus/knowledge/registry-link-r26.md --root fleet
   --registry tree/corpus/SOURCES.md` gives rc=1 with `META_SOURCE_USEDBY_MISSING` for S036 and
   S039, while the same entry with `--root .` from the lane cwd gives rc=0.
   - In my fixture the lane under `fleet/` was a symlink, so `entry_path` came out empty
     (`fdcanon` is outside the `pwd -P` root).
   - `[INFERENCE]` With a real subdirectory, the derived path would be
     `chousa-shokunin/corpus/knowledge/…`, which also fails to match.
   - The r26 entries' rechecks state `cwd=lane root; --root .`, which QUALITY 13 allows because it
     states the layout. A reader who follows the "fleet root by role" rule would still get false
     positives. The fix would be in documentation or the contract, not the matcher.
2. **Entry reached through a symlink (low).** `link207.md` points to `t207.md`, and with
   `used-by: corpus/knowledge/link207.md` the result is rc=1 USEDBY_MISSING S207. Identity is the
   canonical target. This is consistent with the gate's fd-bound reading, but it is not stated in
   the spec.
3. **Comma in a filename cannot be named (low, latent).** `e,203.md` with an exact `used-by` gives
   rc=1 USEDBY_MISSING S203, because the comma split happens before trimming. No real entry has a
   comma.
4. **GFM escaped pipe shifts columns (low, latent; adjacent to this target).** The row
   `| S400 | a \| b | mined | corpus/knowledge/e400.md |` gives rc=1 `META_SOURCE_NOT_MINED` S400
   instead of clean, which is the wrong code because the cells are misaligned. The target
   `SOURCES.md` has 0 `\|`.
5. **A second table is not read (latent).** A no-path mined row in a second table gives
   `META_SOURCE_ROW_MISSING` S400 instead of USEDBY. The spec phrase "a registry with no table…" is
   singular. The live registry is one contiguous table.

The header variants `used by` and `Used-by` exit 2 with "metadata registry has no table with id,
status, and used-by columns". That is the specified refusal.

## Unresolved

- I did not run a QUALITY 17 mutation (disabling the USEDBY arm) from this seat. That belongs to
  `FMutateC3Killed`.
- I did not observe a real-subdirectory fleet-root run; it is marked `[INFERENCE]` in observation 1.
- I did not test duplicate occurrences of the same S-id inside one `source:` value.

## Checks for L1

Run C3 once in the integrated main verification:
`bash corpus/evidence/round26-measure.sh <tree> c3`. Separately, decide whether QUALITY 13's
fleet-root role needs a carve-out for `--registry` runs.
