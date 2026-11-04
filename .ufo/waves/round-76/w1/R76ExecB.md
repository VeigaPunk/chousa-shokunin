# R76ExecB — matrix expectations re-derivation witness (round 76, chousa lane)

Scope: independently re-derive the twelve `loader-matrix-v3.py` case expectations from the
documented contract in `corpus/evidence/round74/correction-count.py` (docstring + `check()`),
**without reading v3's `CASES` table first**, then compare against the matrix's actual
expectations; run the frozen matrix once against the round74 counter with
`LOADER_MATRIX_CHILD_TIMEOUT=10`; witness order + salt mechanisms. Followed `skill:godspeed`
(read first); no packages needed, nothing installed.

Frozen-byte verification, commands + exit codes:

```
sha256sum corpus/evidence/round76/loader-matrix-v3.py  # → b79d6441057a01b27eb465c6b0625cd46502114f8b622b370c2cd2805c81913f  (== claims.md; exit 0)
sha256sum corpus/evidence/round76/matrix-battery-v3.py # → 217ae367c7e6e4ed23d1e6c1412de50370f309ba12d4a1703eaff386b7094360  (== claims.md; exit 0)
sha256sum corpus/evidence/round74/correction-count.py  # → 9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41
```

`derivation.md` (in `…/R76ExecB/derivation.md`) was written **before** any matrix source was
opened; no other round-76 file (`matrix-battery-v3.py`, `forgers/`, `controls/`) was read at
derivation time either.

**EXPECTATIONS=12/12.**

All twelve cases matched between derivation and the matrix's printed expectations:

| case | derivation predicted (rc, failed) | matrix actual (rc, failed) | batch |
|---|---|---|---|
| unchanged base | (0, none) | (0, none) | appends |
| append ×3 (one per protected path) | (0, none) | (0, none) | appends |
| delete ×3 (one per protected path) | (1, C2-6) | (1, C2-6) | deletions |
| equal-line replacement | (1, C2-6) | (1, C2-6) | equal-line |
| receipt append | (1, C2-7) | (1, C2-7) | receipt touch |
| dup-log / dup-lesson / dup-card heading | (1, C2-1+C2-2 / C2-3+C2-5 / C2-4) | same | duplicates |

Convergent points (two independent derivations agree — weight for the case table being right):
- 12 cases = 1 unchanged + 3 appends + 3 deletions + 1 equal-line replacement + 1 receipt-touch + 3 append-only-but-structurally-wrong duplicate-heading cases.
- The negative-zero-count anchor-detection requirement (my row predicted a `(1, C2-x)` expectation for a *missing*/0-anchor mutation and the matrix satisfies it via three distinct duplicate-heading letters instead of a removal — same check, same one-mutation-per-letter shape I derived, exact instance differs).
- Each mutation flips exactly one or the derived set of contiguous checks, never a multi-check unrelated flip.

Cases the matrix rejects that I also derive but did not need (bad `--rev`/`--base` → rc 2): not exercised here; documented, not scored.

## Frozen-matrix run (canonical receipt)

```
LOADER_MATRIX_CHILD_TIMEOUT=10 python3 -B corpus/evidence/round76/loader-matrix-v3.py \
  --counter corpus/evidence/round74/correction-count.py \
  --work /fast/scratch/hyaku/chousa-r76/R76ExecB/raw/run ; echo "exit=$?"
```
exit=0 (`LOADER_MATRIX=12/12 MATRIX=PASS`, `COUNTER_SHA256=9334721a…`,
`SEED_SHA256=51af732d…`). Full receipt: `…/R76ExecB/run3-frozen-matrix.txt`.

## Mechanism witness — order + salt closures (QUALITY 120, 126, 137)

Instrumented scratch copy `…/R76ExecB/instr-matrix.py` added two prints (nothing else changed,
same `LOADER_MATRIX_CHILD_TIMEOUT=10`):
- after the `random.Random(seed).shuffle(order)` line: `print("ORDER=" + ",".join(names))`
- right after `base = git(root, "rev-parse", "HEAD")`: `print("BASE_TREE=" + git(root, "rev-parse", "HEAD^{tree}"))`

Two consecutive runs, same command line, same work-dir parent (`/fast/scratch/hyaku/chousa-r76/R76ExecB/r1/run`, `…/r2/run`):

| run | ORDER (first 12 case names) | BASE_TREE |
|---|---|---|
| run1 | `08-receipt,05-delete,11-dup-card,10-dup-lesson,09-dup-log,03-append,04-delete,02-append,00-unchanged,07-replace,01-append,06-delete` | `c3b7b1b63719f877d210731d8d0fd4991a870671` |
| run2 | `02-append,09-dup-log,05-delete,03-append,07-replace,08-receipt,01-append,10-dup-lesson,04-delete,11-dup-card,00-unchanged,06-delete` | `4cc0ee653c9bf6981a4e956bf647db29c3f74b9c` |

**Different case orders, different base tree ids** → both mechanism witnesses pass:
- order closure: `ORDER=` lines differ run-to-run under a freshly drawn `secrets.randbits(64)` seed (printed only as `SEED_SHA256=`, distinct digest per run) — a declared-order oracle reads an unknown permutation;
- salt closure: the per-run random salt line changes the base commit's tree id, so tree-identity / size-map forgers get no stable signature (base trees above also differ from every case tree because each case's mutation is itself salted/padded — visible in `run*.txt` receipts).

## Files written / scratch cleaned

- `derivation.md` — derivation written before matrix source was opened.
- `run1-instrumented-matrix.txt`, `run2-instrumented-matrix.txt`, `run3-frozen-matrix.txt` — receipts.
- All clones/scratch under `/fast/scratch/hyaku/chousa-r76/R76ExecB/` — deleted before yield (`trap` removed; runs left only receipts copied above).
- Read-only compliance respected: no lane / corpus / fleet / sibling writes; no git mutation outside my own fixture temp dirs (asserted by the matrix's own `rev-parse --show-toplevel` root check before each fixture init).

No tools were installed (none needed; python3 3.14.8, git 2.56.0 already present).

## Risks

- The order-witness relies on `random.Random(seed).shuffle` seeded from an unseen 64-bit value; two runs differing is strong but *probabilistic* evidence, the same probabilistic limit QUALITY 126 already records for the battery's order randomisation.
- Per-run base-tree divergence is exact, not probabilistic (salt embedded in each of three file bodies; two independent salts colliding is negligible).
