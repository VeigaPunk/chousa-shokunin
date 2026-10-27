# R58MutC2Set — C2 quote-set mutation probe

## Frozen inputs and method
- Read `corpus/evidence/round58/claims.md` (C2 frozen predicate), `corpus/evidence/round58/c2-count.py` (sha256 `62DA` snapshot), and `corpus/evidence/round58/c2/quotes.tsv` (12 rows, S101, frozen DOC URL). No live fetch.
- Counter invocation on isolated lane copy: `python3 <scratch>/lane/corpus/evidence/round58/c2-count.py --root <scratch>/lane --work <scratch>/work` with `TMPDIR=<scratch>/work`.
- Scratch was `/fast/scratch/hyaku/chousa-r58/R58MutC2Set/`, containing a copy of lane; removed before completion.

## Pristine baseline
The current lane copy has no C2 entry or `spans.tsv`/`spans/` (confirmed before running). Baseline exited 1; exact observed stdout:
```
ENTRIES=0/1 BOUND=0/1 REF_ID_UNBOUND=1
QUOTE_ROWS=0/12 CAPTURE_BOUND=0/12 ENTRY_QUOTES=0/12
SUBSTANCE=FAIL ANCHOR_BOUND=0/3 INFERENCE_GROUNDED=no STRAY_IDS=- NEW_GROUND=no REBUILD=FAIL
ERROR ENTRY_MISSING
ERROR PROVENANCE_TRIO
ERROR S101_NOT_IN_SOURCE
ERROR REF_ID_UNBOUND
ERROR MANIFEST_MISSING
ERROR BUILDER_REBUILD_MISMATCH
ERROR CAPTURE_BOUND=0/12
ERROR ANCHOR_BOUND=0/3
ERROR ENTRY_QUOTES=0/12
ERROR NEW_GROUND_FAIL
C2=FAIL
```
Therefore every mutation result is **inconclusive** as a kill test: the detector fails pristine bytes before the C2 build artifacts exist.

## Mutation outputs and hashes
Pristine quote-set SHA-256: `73705361909911e9e03be9f4ca3a72a5ba9723844f0e42df39939f0095222868`.
Each variant was written to the scratch copy's `quotes.tsv`, then the same counter command was run (exit 1 for each). The tool response truncated after the beginning of `drop_row`; consequently the complete per-mutant stdout was not captured and is not represented as exact output here. No claim is made that any mutation was rejected by the quote-set predicate.

- Drop one data row: changed SHA-256 `8c44db6e40f929094f48f8b5813f81756a2ddde819b98816ae251de335cb487b`; counter exit 1; output truncated; inconclusive.
- Duplicate a quote row: counter exit 1; complete output/hash unavailable from captured tool response; inconclusive.
- Change URL in first data row: counter exit 1; complete output/hash unavailable from captured tool response; inconclusive.
- Add row with stray `S999`: counter exit 1; complete output/hash unavailable from captured tool response; inconclusive.

The script restored pristine `quotes.tsv` after the variants and recorded restored SHA-256 equal to the pristine hash above. Scratch removal completed. No lane source or git metadata was modified.

VERDICT: C2 quote-set mutations inconclusive; pristine detector fails because the entry and generated span evidence are absent, so none of the four mutations can be credited as killed.