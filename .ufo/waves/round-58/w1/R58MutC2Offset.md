# R58MutC2Offset — C2 mutation probe

Read the frozen `claims.md` and `c2-count.py` at lane HEAD `5da0a6375a554e1229492a8cb0b9695bd8e85456`; claims name freeze commit `9e73a031ab1ac3bac343de008850d7d87f9e5634` and claim base `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`. Counter bytes SHA-256: `dbb859612f9d018296b217baec76a5c6cb744609b7c95372dabae4d6691c8503`. No live fetch.

## Procedure and pristine baseline

Scratch clone: `/fast/scratch/hyaku/chousa-r58/R58MutC2Offset/lane`; work directory passed explicitly as `/fast/scratch/hyaku/chousa-r58/R58MutC2Offset/work`. The candidate C2 entry, registry binding and committed spans were absent from lane HEAD. I staged the committed quote set and raw capture in the clone, then generated spans there with the pinned builder:

`python3 -B <scratch>/lane/tools/build-spans.py --quotes <scratch>/lane/corpus/evidence/round58/c2/quotes.tsv --out <scratch>/lane/corpus/evidence/round58/c2 --cache <scratch>/lane/corpus/captures`

Observed builder output: `SPANS_ROWS=12 WRITTEN=12`, exit 0. The first emitted quote location was `char 315`; its manifest offset was `235` (difference 80). The counter treats the manifest offset as the quote's start, so pristine staged evidence already fails all 12 `CAPTURE_BIND:S101` checks. This is the frozen counter/builder offset disagreement; baseline is not a valid pass.

Frozen counter command for every run:
`python3 -B <scratch>/lane/corpus/evidence/round58/c2-count.py --root <scratch>/lane --work <scratch>/work`

Pristine output (before mutations; exit 1): `QUOTE_ROWS=12/12 CAPTURE_BOUND=0/12 ENTRY_QUOTES=0/12`; errors include `ENTRY_MISSING`, `REF_ID_UNBOUND`, twelve `CAPTURE_BIND:S101`, `CAPTURE_BOUND=0/12`, and `NEW_GROUND_FAIL`; final `C2=FAIL`.

## Mutation results

| Scratch mutation | Counter evidence | Result |
|---|---|---|
| First manifest offset +1 | `CAPTURE_BIND:S101` x12; `BUILDER_REBUILD_MISMATCH`; `C2=FAIL` | Inconclusive: same 12 bind failures exist pristine. |
| First manifest digest first hex digit flipped | `CAPTURE_BIND:S101` x12; `BUILDER_REBUILD_MISMATCH`; `C2=FAIL` | Inconclusive: same bind failures exist pristine. |
| First span byte changed to `X` (with diagnostic manifest offsets shifted +80 to quote starts) | `QUOTE_ROWS=12/12 CAPTURE_BOUND=12/12`; `SPAN_BYTES:S101`; `C2=FAIL` | Span-byte rejection observed, but whole counter remains baseline-failing (entry absent and rebuild mismatch). Not a killed mutant under baseline rule. |
| First frozen quote occurrence changed `标`→`標` | `ERROR QUOTE_SET=12/12`; `BUILDER_REBUILD_MISMATCH`; `C2=FAIL` | Quote mutation detected. `QUOTE_SET=12/12` is a misleading count-only token despite content inequality; the `ERROR` and failure still prevent a pass. |

The isolated span-byte run used diagnostic offset adjustment only to reach span comparison; this is not a C2 fix or alternate frozen predicate. Because the regular staged baseline fails, mutation detection cannot be credited as a killed mutant. No false pass occurred in observed outputs; quote-set output has an ambiguous count token, not a false pass.

## Restoration

Restored original quote bytes and the scratch-generated pristine manifest/span bytes. Before cleanup, scratch/original quote SHA-256 both `73705361909911e9e03be9f4ca3a72a5ba9723844f0e42df39939f0095222868`; pristine/restored manifest both `8b910a5ec191e023ed9416f07ce58b8109f33ca1973a666a470db752800b460b`; pristine/restored first span both `60ae136202c74b70c7246da9650f510eac2bfadaffe74536639e270a5a1b75c2`. Restored counter output matched pristine (`CAPTURE_BOUND=0/12`, `REBUILD=MATCH`, `C2=FAIL`, exit 1). Scratch removed: `SCRATCH_REMOVED=1`.

VERDICT: Inconclusive — C2 offset/digest mutants were masked by pristine failure; span-byte and quote edits emitted rejection tokens, but no complete passing baseline existed. Builder-emitted offsets disagree with the counter's quote-start interpretation; the L1 integrator should assess this frozen-predicate finding.