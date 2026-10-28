# ExecRegressSets — round 61 w1 real-data no-harm run

Lane root /home/vgpnk/Projects/shokunin/chousa-shokunin. No lane file edited, no install, no network.
Builders: base `tools/build-spans.py` (git blob 072415ad…, sha256 1ed2650a…c80bf6, tree clean for tools/) and
`corpus/evidence/round61/controls/ref-build-spans.py` (sha256 86d64c31…eccfd). Store: `corpus/captures` (129 files, 59M).

## Findings
1. Frozen `regress.py`, reference builder, scratch a: `REAL_REBUILD=3/3`, exit 0 (rounds 55, 56, 57/c3 each check_rc=0 build_rc=0 identical=True).
2. Same, base builder, scratch b: `REAL_REBUILD=3/3`, exit 0. Matches `controls/regress-base.txt` / `regress-reference.txt`.
3. Hand extension to every committed span set with a quotes table (`find corpus/evidence -name quotes.tsv`, rounds 47–57, plus round56 `quotes-held.tsv`→`held/`):
   11 sets examined; 10 resolve in the lane store; 7 byte-identical (spans.tsv + every span file, no extra file, `--check` rc 0).
   The base and reference builders gave the SAME verdict and the same per-set output on all 11 (the reference does not change any real-data result).
4. The 3 checked-but-not-identical sets are old-form or store drift, not builder harm (the round's own per-round builders agree):

| set | rows | check | fresh build | cause (observed) |
|---|---|---|---|---|
| round47 | 35 | STALE=0 | identical | – |
| round49 | 31 | STALE=9 | rc0, 9 rows differ in `offset` (S100×3, S101×6), span files differ | S100/S101 are OLE `.doc` (`d0cf11e0…`); committed digest = `.raw` digest (46d1866c…, 6063a3af…) so same file, but offset was derived from the superseded UTF-16LE form; the shared builder reads capture-text form (builder docstring, round-54 lesson). `round49/build-spans.py --check` itself: STALE=0 |
| round51 | 70 | STALE=0 | identical | – |
| round52 | 39 | STALE=15 | rc0, 15 rows differ in `capture_sha256` (S113×6, S114×9) | committed digests (ad6b09f0…, b1c3cd6a…) equal neither the `.raw` nor `.txt` sha in the store for those keys (store file differs from the one the set was built on; INFERENCE: re-captured / cache origin). `round52/build-spans.py --check` itself: STALE=15 |
| round53 | 63 | STALE=0 | identical | – |
| round54 | 33 | STALE=6 | rc0, S121×6 differ in `capture_sha256` | committed 4e46154f… equals neither store `.raw` (f3cb44c4…) nor `.txt` (ed4dde2e…). `round54/build-spans.py --check` itself: STALE=6 |
| round55 | 19 | STALE=0 | identical | (in regress.py) |
| round56 | 23 | STALE=0 | identical | (in regress.py) |
| round56/held | 1 | STALE=0 | identical | quotes-held.tsv |
| round57/c3 | 10 | STALE=0 | identical | (in regress.py) |

   Rows that differ in those sets: round49 9 + round52 15 + round54 6 = 30 of 103 rows; the other 73 rows in those sets rebuilt byte-equal.
5. Skipped (not counted as checked):
   - round50 (67 rows): S105 capture `e3ca8f4f…24` (gs.sxu.edu.cn PDF) is in the store as neither `.txt` nor `.raw` — needs the deleted campaign cache. Both builders refuse (`no defined text form`, exit 1); the round's own builder refuses too (`no capture … .txt/.raw`). Measured: 41 of the 67 rows, all id S105, have no capture (every other id resolves).
   - round45, round46: committed `spans.tsv`/`spans/` but no `quotes.tsv` in git (round45/46 dirs list none) — nothing to rebuild from.
   - round48: no directory. round58/c2: `quotes.tsv` only, no spans, out of 4x–57 range. `corpus/fixtures/inference-ground-*`: fixtures, no quotes table.

## Evidence pointers
- Scratch harness (deleted): per set `--check` against the committed dir and a fresh `--out` build in scratch, byte compare of spans.tsv, every span file, listing; run for both builders, identical output.
- `python3 -B regress.py --builder <ref|base> --work …/a|b` printed `REAL_REBUILD=3/3`, exit 0 both.
- `python3 -B corpus/evidence/round{47,49,50,51,52,53,54}/build-spans.py --root . --cache corpus/captures --check` → 47: STALE=0; 49: STALE=0; 50: refused S105; 51: STALE=0; 52: STALE=15; 53: STALE=0; 54: STALE=6.

## Calibration
- Result does not weaken C1's `REAL_REBUILD=3/3` kill rule (rounds 55/56/57c3 pass). The extension shows rounds 49/52/54 sets cannot be re-derived by the shared builder from the current store, with or without the round-61 guards: pre-existing, not caused by the reference.
- Not run: the landed builder (none yet landed); this run covers the base and reference only. Not run on rounds 45/46/50/58.

VERDICT: REGRESS_SETS_CHECKED=10 identical=7 skipped=3
