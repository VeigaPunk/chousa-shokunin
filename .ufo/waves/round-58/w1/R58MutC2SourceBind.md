# R58MutC2SourceBind — C2 registry binding probe

## Frozen inputs and setup
- Read frozen `claims.md` and `c2-count.py`; report targets the S101 `status`, `used-by`, and entry `source:` ID checks. No live fetch.
- Scratch clone: lane HEAD `5da0a6375a554e1229492a8cb0b9695bd8e85456`; no lane source edits. Copied counter SHA-256 `dbb859612f9d018296b217baec76a5c6cb744609b7c95372dabae4d6691c8503` (same as frozen source).
- Constructed a scratch-only candidate: generated 12 spans with pinned builder; added an entry containing the frozen quotes and extended S101 used-by to include its path. This fixture is only a detector baseline, not a claim or truth judgment.
- Pins observed: builder `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`; capture-text `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`; raw capture `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`.

## Detector baseline
Command (run on pristine candidate and again after all restores):
```sh
cd /fast/scratch/hyaku/chousa-r58/R58MutC2SourceBind && TMPDIR=/fast/scratch/hyaku/chousa-r58/R58MutC2SourceBind/work python3 -B c2-count.py --root /fast/scratch/hyaku/chousa-r58/R58MutC2SourceBind/lane --work /fast/scratch/hyaku/chousa-r58/R58MutC2SourceBind/work
```
Observed both times: `ENTRIES=1/1 BOUND=1/1 REF_ID_UNBOUND=0`; `QUOTE_ROWS=12/12 CAPTURE_BOUND=0/12 ENTRY_QUOTES=0/12`; `SUBSTANCE=PASS ANCHOR_BOUND=0/3 INFERENCE_GROUNDED=yes STRAY_IDS=- NEW_GROUND=yes REBUILD=MATCH`; `ERROR CAPTURE_BOUND=0/12`; `ERROR ANCHOR_BOUND=0/3`; `ERROR ENTRY_QUOTES=0/12`; `C2=FAIL`; exit 1. Both outputs also contained twelve identical `ERROR CAPTURE_BIND:S101` lines.

Baseline is inconclusive for overall mutation-kill classification. Cause is in the frozen counter/builder interface: first manifest row stores offset `235` (span-context start), while the pinned builder output says `QUOTE S101 char 315 spans/S101-1.txt` (quote start). `c2-count.py` compares quote occurrence `315` directly to manifest offset `235`; all 12 rows fail this comparison. The counter's own rebuild still reports `MATCH`.

## One-at-a-time mutations
Every detector invocation used the command above; each mutation was restored from the saved pristine candidate bytes before the next. `C2=FAIL` and the twelve baseline `CAPTURE_BIND:S101` errors occurred in every run, so outcomes below describe the binding subcheck only, not an overall kill/survival verdict.

| Mutation | Mutated file SHA-256 | Exact observed binding output | Restored SHA-256 |
|---|---|---|---|
| `cells[7] mined` → `queued` | `956ba3c9bc4e9240624c08ef09d0c59f48e50faeec1c3a2c2ff7c1fd600526d8` | `BOUND=0/1 REF_ID_UNBOUND=1`; `ERROR REF_ID_UNBOUND` | `3e99be2cf25a6d2d1b05dfb771b6c3f4fd45e3fffd90cfaa291b2e129c058244` |
| Append contradictory second S101 row (`queued`, no backlink) | `7e10cbde7000567b00b8a616c4e2e1f59a2664655fd84ea9325606f2705374d9` | `BOUND=1/1 REF_ID_UNBOUND=0`; no `ERROR REF_ID_UNBOUND` | `3e99be2cf25a6d2d1b05dfb771b6c3f4fd45e3fffd90cfaa291b2e129c058244` |
| Remove entry path from first S101 used-by cell | `e7a1627c63111b1b827c0f58520d387cc835b31bcce294d2a10a986d56776bfb` | `BOUND=0/1 REF_ID_UNBOUND=1`; `ERROR REF_ID_UNBOUND` | `3e99be2cf25a6d2d1b05dfb771b6c3f4fd45e3fffd90cfaa291b2e129c058244` |
| Replace used-by with `draft corpus/knowledge/carrier-alphabet-china-r58.md extra` | `50e3fae29580d891a1b9a6f1334c39e5c33219ac3e8a376b198f4dc09ef18a13` | `BOUND=1/1 REF_ID_UNBOUND=0`; no `ERROR REF_ID_UNBOUND` | `3e99be2cf25a6d2d1b05dfb771b6c3f4fd45e3fffd90cfaa291b2e129c058244` |
| Entry line `source: S101` → `source: S103` | `07a1ab5d5e039d09a9dd861360099dea39ecb8efbcc2b84e081d076d6e24f61b` | `ERROR S101_NOT_IN_SOURCE`; `ERROR STRAY_IDS=S103` | `77608059cca5e8a6fa3df1bd4ffd6f1e814a7a8b572cf9b9839624ac8ed5217f` |
| Entry line `source: S101` → `source: S101x` | `20cfad7f92ec1fb07e05df68b6372cb9277815706f5d3bd4ec60f7715c7cb293` | `BOUND=1/1 REF_ID_UNBOUND=0`; no `S101_NOT_IN_SOURCE`, no `STRAY_IDS` | `77608059cca5e8a6fa3df1bd4ffd6f1e814a7a8b572cf9b9839624ac8ed5217f` |
 
All mutation runs ended `C2=FAIL`, exit 1. The two `S101x` entry hashes above are the observed mutated and restored entry hashes; restored entry hash is `77608059cca5e8a6fa3df1bd4ffd6f1e814a7a8b572cf9b9839624ac8ed5217f`.


## Findings and restoration
- Binding checks locally reject a non-`mined` first row and a first-row used-by cell without the entry path.
- The registry lookup selects only the first S101 row: a later contradictory row is ignored. The used-by test is substring containment: junk-prefixed/suffixed text containing the path passes that check.
- Entry source validation is substring-only (`'S101' in source line`): `S101x` passes and is not a stray token; replacing it with S103 is rejected by both source check and stray-ID scan.
- Final restored detector output matched the baseline failure. Final SHA-256s: counter `dbb859612f9d018296b217baec76a5c6cb744609b7c95372dabae4d6691c8503`; SOURCES `3e99be2cf25a6d2d1b05dfb771b6c3f4fd45e3fffd90cfaa291b2e129c058244`; entry `77608059cca5e8a6fa3df1bd4ffd6f1e814a7a8b572cf9b9839624ac8ed5217f`; spans manifest `8b910a5ec191e023ed9416f07ce58b8109f33ca1973a666a470db752800b460b`; raw `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`.
- All scratch contents were removed after evidence collection. No other checks or fetches were run.

VERDICT: C2 S101 registry-binding probe INCONCLUSIVE overall because pristine C2 fails on the frozen offset mismatch; local status/backlink guards reject the tested deletions, while duplicate-row, substring-backlink, and `S101x` source-ID mutations pass their respective local checks.
