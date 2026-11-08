# R94ExecC1Repro — round-94 C1 (operability) reproduced from a clean carrier tree

Seat `R94ExecC1Repro` (leaf), lane `chousa`, round 94, 2026-11-08. Root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Revisions: base `0f3f84dab3a094ec0a2fe8ae9ae59d3326e1a9b6`; freeze F `41038ed7c40cffc4cf86d649a6ba433c4b9eec1a`;
carrier C `352924bbea624caf3771ef291be98fd4ec679dda` (F plus the six control receipts and the 34-row pins
table). `git merge-base --is-ancestor F C` = 0 (F is an ancestor of C).

Clean tree: `S=/fast/scratch/hyaku/chousa-r94/R94ExecC1Repro`;
`git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo` then
`git -C $S/repo checkout 352924bbea624caf3771ef291be98fd4ec679dda`; `git -C $S/repo rev-parse HEAD` =
`352924bbea624caf3771ef291be98fd4ec679dda`, worktree clean (`git status --porcelain` empty). All runs were
made from `$S/repo` with `--root . --repo .`; every fixture elsewhere is a `--shared` clone under `$S`
(S221: `git -C $S/forge/tree count-objects -v` → `count: 0`, `in-pack: 0`, `packs: 0`). No network; every
check read committed bytes. Scratch removed at the end of the seat; nothing written under `/tmp`.

## (a) `control-driver-r94.py verify` — PASS, exit 0

```bash
cd $S/repo && python3 -B corpus/evidence/round94/control-driver-r94.py verify --root . --repo . \
  --rev 41038ed7c40cffc4cf86d649a6ba433c4b9eec1a \
  --receipts-rev 352924bbea624caf3771ef291be98fd4ec679dda --work "$S/verify"
```

Full stdout (`R94ExecC1Repro-verify.stdout.txt`, 10 lines):

```
BASES root=/fast/scratch/hyaku/chousa-r94/R94ExecC1Repro/repo repo=/fast/scratch/hyaku/chousa-r94/R94ExecC1Repro/repo
RECEIPT c1-gate-r89 OK committed+exact+pin+fresh
RECEIPT c1-mutants-r89 OK committed+exact+pin+fresh
RECEIPT c1-harm OK committed+exact+pin+fresh
RECEIPT c1-harm-setup OK committed+exact+pin+fresh
RECEIPT c2-prior-landing OK committed+exact+pin+fresh
RECEIPT c2-prior-controls OK committed+exact+pin+fresh
RECEIPT PINS OK 34/34 pinned files byte-identical RECEIPT_PINS_OK=6/6
RECEIPT SELF_PIN OK rev=41038ed7c40cffc4cf86d649a6ba433c4b9eec1a receipts_rev=352924bbea624caf3771ef291be98fd4ec679dda
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=34/34 RECEIPT_PINS=6/6 PIN_ROLES_OK=14/14 CONTROL_DRIVER_R94=PASS
```

Exit code 0 (`R94ExecC1Repro-verify.rc`). Every expected token is present verbatim, including the self-pin
line naming F and C. `PINNED_FILES=34/34` is the row count of the committed table (independently counted
34 in `R94ExecC1Repro-pins-census.txt`); `PIN_ROLES_OK=14/14` is its non-`driver` row count (5 instrument +
1 expectation + 6 receipt + 2 claims = 14; 20 rows are `driver`).

## (b) `forgeries-r94.py` — all six counters match, but the battery exits 1 (`FORGERIES=FAIL`)

```bash
cd $S/repo && python3 -B corpus/evidence/round94/forgeries-r94.py --root . --repo . \
  --rev 41038ed7c40cffc4cf86d649a6ba433c4b9eec1a \
  --receipts-rev 352924bbea624caf3771ef291be98fd4ec679dda --work "$S/forge"
```

Full stdout (`R94ExecC1Repro-forge.stdout.txt`), exit 1 (`R94ExecC1Repro-forge.rc`):

```
OK d1-dangling-instrument: r93 rc=0 r94 rc=1 needles=PIN_ROLE_DANGLING role=instrument
OK d2-missing-claims: r93 rc=0 r94 rc=1 needles=PIN_ROLE_MISSING role=claims
OK d3-mis-role-expectation: r93 rc=0 r94 rc=1 needles=PIN_ROLE_MISMATCH role=expectation
OK d4-unknown-role: r93 rc=0 r94 rc=2 needles=SETUP PIN_ROLE_UNKNOWN
FAIL s1-schema-two-column: r93 rc=0 r94 rc=0 needles=SETUP PIN_SCHEMA
  r94: RECEIPT PINS OK 34/34 pinned files byte-identical RECEIPT_PINS_OK=6/6
OK s0-schema-prior: r93 rc=0 (two-column table scores) r94 rc=2 (PIN_SCHEMA)
OK c1-carried-instrument: r94 rc=1 (PIN_DISK_MISMATCH)
OK c2-carried-receipt: r94 rc=1 (RECEIPT_MISMATCH)
OK positive: r94 rc=0
FORGERIES=FAIL FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 SCHEMA_REFUSED=1/1 SCHEMA_PRIOR_ACCEPTED=1/1 CARRIED_REFUSED=2/2 POSITIVE=pass
```

Nine case lines were printed (four role fixtures, `s1`, `s0`, two carried, the positive); the seven named
case lines of the role/schema/positive battery are `d1`, `d2`, `d3`, `d4`, `s1`, `s0`, `positive`. The six
counter tokens required by the assignment are present exactly as expected. **The aggregate token is not**:
the frozen prose predicate (`claims.md` line 49) requires `FORGERIES=PASS … (exit 0)`; the observed value is
`FORGERIES=FAIL` and the process exit is 1.

### Cause (deterministic; instrument bytes identical at F and C)

`corpus/evidence/round94/forgeries-r94.py` (`sha256 f7dd794e3434bf0aa57b55cc491b60e87b68da0bcea85cacc4392318923a5d81`
at both F and C — so this is a freeze-time defect, not a carrier artifact):

- `case()` (lines 127–134) always calls `write_r94(tpins, rows, PINS_REL)` at line 131, i.e. it writes the
  r94 **three-column** table, and only then runs the r94 driver.
- `s1-schema-two-column` is called with `rows_mutator=None` and `want_r94_rc=2` (line 171). With no mutator
  the table handed to r94 is the valid three-column table, so r94 exits 0 and the `SETUP PIN_SCHEMA` needle
  cannot appear. The two-column shape is only ever presented to r94 by the separate `s0-schema-prior` path
  (lines 174–178, `write_r93` first), which is green: `r93 rc=0 r94 rc=2 (PIN_SCHEMA)`.
- The summary hides the failing case: `SCHEMA_REFUSED=int(schema_ok)` reads `s0`, and
  `FORGERY_REFUSED`/`PRIOR_ACCEPTED` count only `d1–d4`; only `ok = all(results.values())` (line 215)
  includes `s1`, so the counters print 4/4 … 1/1 … 2/2 while `FORGERIES=FAIL` and `return 1` follow.
- Reproduced twice from code path and once by execution: the r94 verify on the same valid table is (a),
  exit 0; `s0` demonstrates the refusal the `s1` case claims to measure. No tree/state dependence.

### Kill-rule substance measured green

- K2: each of the four role fixtures is refused by r94 (`PIN_ROLE_DANGLING role=instrument`,
  `PIN_ROLE_MISSING role=claims`, `PIN_ROLE_MISMATCH role=expectation`, `SETUP PIN_ROLE_UNKNOWN`) and each is
  accepted by the r93 driver on the two-column projection (`r93 rc=0`); the positive is accepted
  (`positive: r94 rc=0`); no r93 refusal happened for a non-role reason.
- K3: no genuine row moved (`PINNED_FILES=34/34`, independent walk 34/34); `verify` wrote nothing (see (d)).
- K4: the role leg reads the table, not a constant — deleting one claims row changes the verdict (see (c));
  `driver` rows are excluded from the covered set (14 of 34) and counted only in the byte walk; an empty
  executed set cannot pass (`role_instr - executed` would name every instrument row).
- K1: fires on the battery leg **as written in the prose** (`FORGERIES=PASS`, exit 0). It does not fire on
  the six machine-form tokens (`claims.json` `C1.predicate.forgeries_stdout`), all of which hold. The
  machine form's single `"exit": 0` is met by the verify leg and not by the battery leg.

## (c) Independent role relation (own script, no driver imports) + claims-row deletion

`$S/rolecheck.py $S/repo` (`R94ExecC1Repro-rolecheck.stdout.txt`, exit 0) parses
`corpus/evidence/round94/instrument-pins.txt` and `corpus/evidence/round94/controls/expected.tsv` directly:

| role | pinned members | counterpart members | equal | counterpart used |
|---|---|---|---|---|
| instrument | 5 | 5 | yes | every in-tree `.py`/`.sh` token of the expected rows' instrument column (`@ROOT@` resolved): `round89/curation-r89.py`, `round89/curation-r89-controls.py`, `round89/gate-records-r89.py`, `round89/mutate-r89.py`, `round90/harm-recheck-r90.py` |
| expectation | 1 | 1 | yes | `corpus/evidence/round94/controls/expected.tsv` |
| receipt | 6 | 6 | yes | the six `*.txt` files in `corpus/evidence/round94/controls/receipts/` |
| claims | 2 | 2 | yes | `.ufo/waves/round-94/claims.json`, `.ufo/waves/round-94/claims.md` |

`ROLE_TOTAL rows=34 non_driver=14 driver=20` → the driver's `PIN_ROLES_OK=14/14` is the measured non-driver
count, not a constant. The four role sets are equal in both directions.

Mutation (`$S/rolectl.py`, exit 0 = probe verdict met): in a second `--shared` clone at C
(`git -C $S/role/tree rev-parse --show-toplevel` asserted equal to that tree), delete the
`claims.md` row (`9d197d72… claims .ufo/waves/round-94/claims.md`) from the pins table (34 → 33 rows) and
re-digest the self row the driver's way (sha256 over the table's remaining lines, newline included) =
`6081920218919090d92fe0b1eadc54428531d8c3414d8169b4dbb493c2df6f50`. Committed driver at C then prints
(`R94ExecC1Repro-rolectl-mutation.stdout.txt`, exit 1):

```
PIN_ROLE_FINDING PIN_ROLE_MISSING role=claims path=.ufo/waves/round-94/claims.md
RECEIPT PINS FINDING PIN_ROLE_MISSING role=claims path=.ufo/waves/round-94/claims.md
RECEIPT SELF_PIN FINDING SELF_DRIFT corpus/evidence/round94/instrument-pins.txt@352924bbea624caf3771ef291be98fd4ec679dda
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=33/33 RECEIPT_PINS=6/6 PIN_ROLES_OK=12/13 CONTROL_DRIVER_R94=FAIL
MUTANT_EXIT=1
```

The `SELF_DRIFT` line is expected and is not a probe defect: the probe's self row is correct for the mutant
table, while the driver's S5 revival check compares the stored self digest with the carrier blob's minus-self
digest, which still describes the original 34-row table — so the self row is bound to committed bytes, not
to whatever table is passed. The role leg still names the missing claims member (`PIN_ROLES_OK=12/13`,
exit 1).

Extra independent measurement: a byte walk of every row with my own hashing
(`R94ExecC1Repro-pinwalk.stdout.txt`) prints `WALK_PINNED=34/34`.

## (d) `verify` writes nothing

Before/after (a), `sha256sum` over the six committed receipts and `instrument-pins.txt`
(`R94ExecC1Repro-receipts-before.sha.txt` / `-after.sha.txt`): byte-identical, `diff` empty
(`R94ExecC1Repro-writeproof.txt` → `NO_DIFF_RC=0`). Inside the clone, `find . -path ./.git -prune -o
-newer "$S/pre-hashes.txt" -type f -print` returns nothing; `git status --porcelain` is empty; the claims
files and receipts keep their checkout mtimes (12:28). The only files `verify` wrote are its own
`fresh-*.out` and per-leg directories under `--work` (`$S/verify`), which is outside the tree.

## Findings

1. **F1 (C1, prose predicate): `forgeries-r94.py` cannot print `FORGERIES=PASS` at C; it exits 1.**
   The `s1-schema-two-column` case writes the r94 three-column table before asserting the r94 two-column
   refusal (`forgeries-r94.py:131` vs the `want_r94_rc=2` call at line 171), so the case fails on every
   tree whose table r94 accepts — deterministically, from F's own bytes. All six listed counters and the
   seven named case lines other than `s1` are green, and `s0` measures the same refusal correctly. The
   summary counters are disjoint from `s1`'s result (`SCHEMA_REFUSED` reads `s0`), so the aggregate is the
   only token that moves. This is a K1 firing against `claims.md` line 49; the machine-form token list in
   `claims.json` is met. Fix would be to have `s1` write the r93 projection before the r94 run (or to drop
   `s1` as a duplicate of `s0`), in a new freeze commit before C.
2. **F2 (minor, observability): `PRIOR_ACCEPTED` is computed from the same result set as `FORGERY_REFUSED`**
   (`forgeries-r94.py:210–213`: both count the same `d1–d4` entries). Prior acceptance is genuinely measured
   inside each case (`old_ok = rc_old == 0`), so the K2 leg is not vacuous, but the printed pair is one
   measurement printed twice.
3. **Note:** the assignment says "the seven case lines"; the battery prints nine (the seven plus the two
   carried-refusal lines). All nine are recorded above.

## Retained evidence (copied into this folder)

- `R94ExecC1Repro-verify.stdout.txt`, `R94ExecC1Repro-verify.rc` — (a)
- `R94ExecC1Repro-forge.stdout.txt`, `R94ExecC1Repro-forge.rc` — (b)
- `R94ExecC1Repro-rolecheck.stdout.txt`, `R94ExecC1Repro-rolecheck.rc` — (c) role sets
- `R94ExecC1Repro-rolectl-mutation.stdout.txt`, `R94ExecC1Repro-rolectl-mutation.rc` — (c) claims-row deletion
- `R94ExecC1Repro-pinwalk.stdout.txt`, `R94ExecC1Repro-pinwalk.rc` — independent 34/34 byte walk
- `R94ExecC1Repro-receipts-before.sha.txt`, `R94ExecC1Repro-receipts-after.sha.txt`,
  `R94ExecC1Repro-writeproof.txt`, `R94ExecC1Repro-writeproof-find.txt` — (d)
- `R94ExecC1Repro-pins-census.txt` — row/role census, self row, minus-self and whole-file digests
- `R94ExecC1Repro-commands.txt` — exact commands

No tool was installed or upgraded. No production file, lane branch, or sibling repo was touched; the only
writes are this folder and the deleted scratch.

VERDICT: R94ExecC1Repro C1 fired — `verify` exits 0 with the full frozen ratio line and the role relation is independently equal and mutation-refused, but `forgeries-r94.py` exits 1 with `FORGERIES=FAIL` because its own `s1-schema-two-column` case hands r94 the valid three-column table before asserting the two-column refusal, so the prose predicate `FORGERIES=PASS … (exit 0)` is not met at C.
