# FuzzDiff33 — differential fuzz of `verify-claims`' top-level field reader

**Verdict: HOLDS.** On the assigned landed gate (`tools/research-gate.sh` SHA-256
`94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e`, commit `0fb300b`/`4c076a0`,
claims.md design v2) **750/750** generated records match an independent contract reference, and
**650/650** on a second fixture from a pre-extension generator. On the successor that landed at
06:12 mid-wave (`165acd5f…`, commit `0cad05e`) the identical 750-record fixture is also **750/750**.
No disagreement with C1 was found; there is therefore no minimal counterexample line against the
landed gate to report. My instrument is validated on the do-nothing gate (`f4731885…`), where the
same fixture (byte-identical, SHA-256 `91eaf163…`) yields **437/750** disagreements, six of which I
delta-minimized to one-line counterexamples.

Artifacts: `.ufo/waves/round-33/w2/FuzzDiff33/` (all < 1 MiB; scratch under
`/fast/scratch/hyaku/chousa-r33/w2/FuzzDiff33/`). No installs, no network, no lane file edited.

## What I attacked

C1 as v2 defines it: the seven read fields (`id/source/span/expect/marker/line/sha256`) are read
from the record's **top-level** JSON object only; a same-named member of a nested object/array
changes nothing; a repeated top-level read field makes the record `invalid`; characters inside JSON
strings are never structure. The counter (`c1-count-v2.py`) emits its records through
`json.dumps`, so it produces **no whitespace at all** beyond one space after `,`/`:`, no tabs, no
leading/trailing space, no CRLF, no empty member names, no near-miss key spellings, no `line`
ranges, no read key whose top-level value is a container, no duplicate whose second value is a
container, and at most three container levels. I generated exactly those shapes.

## Method (independent reference, no gate code reused)

`fuzz_c1.py` (artifact, SHA-256 `a0a9cd7f…`) builds, per seed, a small source corpus (6 files,
12–20 lines, unique standalone span words at known lines) and one claims JSONL. Each record:
random member order; random whitespace (`""`, `" "`, `"  "`, `"\t"`) around `{ } [ ] : ,`; 0–3
unknown-key decoy members whose nested object/array values hold random subsets of the seven read
keys (object, array, two-level and deeper wrappings, empty `{}`/`[]`); string confusers (`}`, `[`,
escaped quotes, trailing `\\`, literal `\u007b` text, `\n` escapes); occasional top-level
duplicates (identical, differing, nested-container, or non-string second value, including `id` and
`marker`); near-miss key spellings (`line `, ` line`, `LINE`, `Line`, `linex`, `sha256 `); empty
member names; a read key whose top-level value is an object/array holding the same key; `line`
ranges (`L-L`, `L-L+1`, inverted); leading/trailing spaces, tabs and CRLF; 10 % of records with
malformed `line`/`sha256` values. Every line is a valid JSON object (`json.loads` asserted at
generation; failures abort the run).

The contract verdict is computed by my own reference: `json.loads(..., object_pairs_hook=Pairs)`,
count top-level names, **any repeat among the eight read names (seven + `marker_default`) →
`invalid`**, first occurrence wins for reads, string-typed reads, sha-pin compare against the
file's real digest, span occurrence with token boundaries, `line` binding. The gate is run once per
fixture (`verify-claims <claims> --root <tmp>`, `CHOUSA_*` removed); comparison is per id (or
`lineN` when the id is unreadable), and also requires **exactly one** `CLAIM` line for that id. A
mismatch would be delta-minimized (drop top-level members, collapse nested containers, strip
whitespace), re-observed on the gate on a one-record file, and a reduction is accepted only while
the disagreement survives; the minimizer never fired on a landed gate.

## Evidence

| run | records | gate | result |
|---|---|---|---|
| `landed-90214d` seed 90214 | 750 (full feature set) | `94a7be5a…` (copy extracted with `git show 4c076a0:tools/research-gate.sh`) | `CALIBRATION_FLAT=60/60`, `DIFF_CLAIMS=750/750`, `MISMATCHES=0` |
| `full-90212` seed 90212 | 650 (pre-extension generator) | `94a7be5a…` (lane path) | `CALIBRATION_FLAT=60/60`, `DIFF_CLAIMS=650/650`, `MISMATCHES=0` |
| `smoke3` seed 90213 | 100 (full feature set) | `94a7be5a…` | `DIFF_CLAIMS=100/100`, `MISMATCHES=0` |
| `full-90214b` seed 90214 | 750 (same bytes as `landed-90214d`) | `165acd5f…` | `DIFF_CLAIMS=750/750`, `MISMATCHES=0` |
| `full-90214` seed 90214 | 750 | `45d76b4f…` — **working-tree state, not in any commit** (`git show <rev>:tools/research-gate.sh` gives `52f07c74…`, `94a7be5a…`, `94a7be5a…`, `165acd5f…` for the four most recent commits — never `45d76b4f`) | `DIFF_CLAIMS=750/750`, `MISMATCHES=0` (reported, not attributed) |
| `base-90214c` seed 90214 | 750 (identical fixture) | `f4731885…` = base `2b9cc73:tools/research-gate.sh` (verified) | `DIFF_CLAIMS=313/750`, **437 mismatches** |

Commands, verbatim shape (all bounded by `timeout`, `prlimit --nproc=2000 --as=4000000000`,
`C1_TMP`/`TMPDIR` in scratch). The fuzz harness prints its verdict lines and exits 0 iff
`matched == n`; the observed output lines are what the table quotes (the fuzz runs were tailed, so
only the counter runs below have an observed process exit code):

```
python3 fuzz_c1.py --gate <gate> --root <scratch tmp> --seed 90214 --n 750 --flat 60 --out <json>
python3 probe_spot.py <root> <gate>
python3 probe_marker_default.py <root> <gate>
```

Fixture identity: `sha256(tmp/.../claims.jsonl) = 91eaf1634facb6c7e04707df36035c2ba5a1aba0be200d86394c7a4a4a88d796`
for the 750-record fixture — identical in the `94a7be5a`, `165acd5f` and base-control roots, so the
four gate results are the same bytes.

Inspected reports (hashes in the artefact directory): `landed-90214d.json` `6b2a9e2e…`,
`full-90212.json` `5d6ecffe…`, `full-90214b.json` `b2dbbb5d…`, `full-90214.json` `553e90e9…`,
`base-90214c.json` `faf7fe3a…`. Each report records the gate SHA-256 its run actually hashed, so
the mid-wave changes are visible per run.

### Counting commands (kill-rule receipts)

Every `c1-count-v2.py` run passed `--receipt` into my directory and its stdout was redirected to a
file (never piped; the counter prints before it writes the receipt).

| seed | gate | stdout | receipt | result |
|---|---|---|---|---|
| 8101 | `94a7be5a…` | `c1-v2-seed8101.stdout` (`1eeb8be8…`) | `c1-v2-seed8101.json` (`3d8580c1…`) | `TOPLEVEL_FIELD_MATCH=156/156`, `predicate_holds=true`, `gate_rc=1` |
| 8102 | `94a7be5a…` | `c1-v2-seed8102.stdout` (identical bytes) | `c1-v2-seed8102.json` (`0f491c63…`) | `156/156`, `predicate_holds=true`, `gate_rc=1` |
| 8103 | `165acd5f…` | `c1-v2-seed8103-tip.stdout` (identical bytes) | `c1-v2-seed8103-tip.json` (`ae2bc9ea…`) | `156/156`, `predicate_holds=true`, `gate_rc=1` |

All three receipts carry `counter_sha256=cb354dd1…a514`, the frozen v2 counter.

### Hand-written minimal cases (`spot-94a7be5a.out`, `10/10`)

`S1` nested `{"line":"9"}` before a correct top-level `"line":"2"` → `observed=supported`
(nested decoy ignored). `S2` nested `"line":"2"` with top-level `"line":"4"` → `mislocated`.
`S3` duplicated top-level `span` → `CLAIM id=s3 … observed=invalid` +
`FINDING … duplicate top-level key span`. `S4` top-level `"line": {"line":"2"}` → `invalid`
(`line not a JSON string`) — the reader does not descend. `S5` depth-4 nesting holding all seven
read keys → `supported`. `S6` string value with fake members before a wrong top-level line →
`mislocated`. `S7` duplicated `id` identical → `CLAIM id=s7 … invalid`. `S8` duplicated `id`
differing → `CLAIM id=line8 … invalid`. `S9` `id` as a number → `invalid`. `S10` duplicated
`expect` → `invalid`.

### Same-reader side probe, `marker_default` (not the counted surface): `PROBE_OK=4/4`

Top-level default used and nested decoy ignored; top-level default absent but nested present →
`unproven` (never adopted); a duplicated `marker_default` row and a nested-only `marker_default`
row are both refused as default rows (the following contradicted claim stays `unproven`).

## Instrument validation: the same fixture breaks the do-nothing gate

Base gate `f4731885…`, seed 90214, 750 records: 313 match, **437 disagreements** (by kind:
supported 106/278, mislocated 78/204, stale 64/135, unsupported 38/91, linebad 27/42). Six
delta-minimal counterexamples (`base-minimals.jsonl`, each one line, re-observed on the base gate):

1. `{"zelo":{"yotu":true,"marker":"serigu","nadamogu":"fari"},"span":"hohofa","id":"c2077847d70","expect":"supported","source":"src/0f66fdca1b9283fd.md"}`
   — contract: supported (nested `marker` is not the record's marker); base: `invalid`.
2. `{"fayomo":{"visepeho":"text with \\u007b and \\u005b escapes","momozefa":{"id":"cd4a3fdf11c","marker":"monabi"}},"span":"pelokavi","source":"src/ed51d46ad7e520ed.md","expect":"supported","id":"ca11f2dde24"}`
   — contract: supported; base: `invalid` (nested `marker` read as the record's).
3. `{"span":"dagukagu","source":"src/d1dae25331ac482c.md","id":"c0cbb2ef307","expect":"supported","pegumo":{"expect":"unsupported","marker":"guguyofa","dapevi":"guseseyo","source":"src/727ae625366c55d9.md","napevi":"vigumo"}}`
   — contract: supported; base: `invalid` (nested `marker`/`source`/`expect` read as top-level).
4. `{"gubifabi":["ends with a backslash \\",{"lotutufa":"a quote \" then } more","kapefamo":{"sha256":"634348081e4c2e7150e88b6427e2e889e7018dcb57388fe1569fa53c0a24109f","gupekaze":"trailing \\\\ two backslashes then }","yona":true}}],"expect":"contradicted","id":"c3466cb89e3","span":"yodana","source":"src/bb6573d182d8fa67.md"}`
   — contract: no top-level `sha256`, no marker → `unproven`; base: `stale` from the nested pin.
5. `{"zehovi":{"expect":"unsupported"},"id":"cc3fd7d1604","source":"src/d1dae25331ac482c.md","span":"dagukagu"}`
   — contract: `invalid` (top-level `expect` missing); base: `supported` from the nested `expect`.
6. `{"span":"hobibi","expect":"supported","id":"c252c22be5f","sha256":[{"sha256":"9ec0cc97b64fc382725a9466193abe90c338857e04565cd9c5151c154623ede9"},"pemodalo"],"source":"src/fe51adf1c4250e12.md"}`
   — contract: `invalid` (top-level `sha256` is an array); base: `supported` from the inner pin.

Each minimal line is a disagreement-preserving reduction (the minimizer refuses a reduction that
stops disagreeing); the *original* record's disagreement is given in `base-90214c.json`. On the
landed gates the same classes verify with the contract's verdict (spot cases S1–S6).

## Coverage of the 750-record fixture (seed 90214, `coverage.txt`)

609 records contain a tab; 53 leading whitespace; 38 trailing whitespace/CR; 48 an empty member
name; 71 a near-miss key spelling; 21 a `line` range; 405 have at least one read key inside a
nested container; 149 have a repeated top-level read key; measured maximum container depth 5.
Reference verdicts: supported 194, invalid 246, mislocated 145, stale 95, unsupported 70.
The flat calibration (60 records, no nesting/duplicates, random member order) is 60/60 on every
gate tested including the base — the reference agrees with the undisturbed reader.

## Limits

- My span model (unique standalone words, single-line occurrences) matches the gate for the
  fixtures I generate; multi-occurrence spans, multi-line spans and the full token-boundary edge
  set are base behaviour I model only approximately (and only for the minimized lines' `contradicted`
  path). Those paths are outside C1.
- Not fuzzed: non-ASCII in read values, keys spelled with JSON escapes, malformed JSON lines
  (all explicitly "not claimed"); `marker_default` rows beyond the four probe cases; any other
  mode. `verify-all` manifest parsing is not C1.
- The lane gate changed under me while I ran: `94a7be5a` (assigned) → a working-tree state
  `45d76b4f` that exists in no commit → `165acd5f` (commit `0cad05e`). Each report records the
  SHA-256 its run hashed; the attributable results are the `94a7be5a` and `165acd5f` rows.
- A harness bug I found and fixed mid-run (nested `Pairs` objects re-serialized as pair-arrays in
  the *minimizer* only) corrupted the first base-control minimals; it never ran on a landed gate
  (zero mismatches), and the base control was re-run from scratch with the fix (`base-90214c`).
- D1–D5 repairs, sources, knowledge and QUALITY rows were not this seat's surface; nothing here
  speaks to them. No build/lint/selftest was run (parent owns the post-integration gate).
