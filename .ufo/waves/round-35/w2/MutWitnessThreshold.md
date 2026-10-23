# Round 35 w2 — threshold attack on the C2 mechanism witness

Seat: MutWitnessThreshold. Task: build an engine that calls
`tok_span_offsets_chunk` exactly once per gate run (first long record) and
answers the rest by exact search; then one that calls it once per long record
and discards the result; show stamp counts and whether the frozen threshold
(`chunk >= long_records`) separates them from the landed gate.

Access date for every citation: 2026-10-23. Gate scored everywhere:
`tools/research-gate.sh` sha256
`1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`
(re-checked before and after; `pristine-gate.sh` is a byte copy with the same
hash). Witness tool unmodified, sha256
`9f537bfde0dd53f2240af149e1b7a03fd0a0f372ee1fa1a32e94044115a252b3`.

## Verdict in one line

The threshold **kills** the once-per-run engine (chunk=1 < 8) and **passes**
both the discard-per-record engine (chunk=9, identical to landed) and an
8-calls-on-one-record engine (chunk=8, exactly at threshold). Those two passes
are the **disclosed limit**, not a P2 failure; but the 8-on-one-record result
shows the implemented predicate is a total call count with no per-record
attribution, stronger than the tool's own docstring.

## Engines built (only the gate was patched; witness used as shipped)

`patch-engines.py` inserts one branch after `local hay=$1 span=$2` in
`tok_span_offsets` (gate:1667) and one `_WONCE_FILE` assignment after
`TOK_DIRECT_SPAN_MAX=` (gate:1650); exact search is a python `bytes.find`
non-overlapping left-to-right scan (`span_search.py`), i.e. K1's contract.

| engine | behaviour | gate sha256 |
|---|---|---|
| pristine | landed, unmodified | `1f2fb4f5…ef617` |
| A `engine-A.sh` | chunk called exactly once per run, on the first long record; its output used; all other long spans exact-search | `6542ca7d87ecc40758f324edd418c280b329ae69d419567e4675c6faa273d3a1` |
| B `engine-B.sh` | chunk called once per long record, result `>/dev/null`; every long span answered by exact search | `dad7fa03d1e8e7a39bf95833c68351ede9adacee821832a1f4b14f3a5acbb63b` |
| C `engine-C.sh` | chunk called 8× on the **first** long record only, all discarded; 7 other long records never enter the matcher | `8b1553d4f06ec8db03e5676bef802fba3c136930b2e2cb2a1f4ea05b5ffe50e1` |
| D `engine-D.sh` | as C with 7 calls (< long_records): boundary control | `3cbbc695f9a430755c9879c2c3df541b58f2b8a9c66483cadf068d4508cbf775` |

Sentinel for "first record only" is a per-process file
`${TMPDIR:-/tmp}/.mw-once-$$-$RANDOM`, because each `tok_span_offsets` call
runs in its own process-substitution subshell (gate:1736) and a shell variable
would not survive; `$$` is stable across those subshells. All four engines pass
`bash -n`.

## Measured detector output

Detector: `python3 tools/mechanism-witness.py --gate G --seed S --json R --tmp D`
(the frozen battery, `WITNESS_TMP`-style dir under
`/tmp/hyaku/chousa-r35/w2/MutWitnessThreshold/`). `long_records=8` in every run
(fixture is 9 records: 8 long, 1 short).

| candidate | seed 3501 stamps chunk/direct | witness | output | rc | seed 7717 stamps | witness | output | rc |
|---|---|---|---|---|---|---|---|---|
| pristine landed | **9**/1 | pass | 9/9 | 0 | **9**/1 | pass | 9/9 | 0 |
| A once-per-run | **1**/1 | **fail** | 9/9 | 1 | **1**/1 | **fail** | 9/9 | 1 |
| B discard-per-record | **9**/1 | **pass** | 9/9 | 0 | **9**/1 | **pass** | 9/9 | 0 |
| C 8 calls, one record | **8**/1 | **pass** | 9/9 | 0 | **8**/1 | **pass** | 9/9 | 0 |
| D 7 calls, one record | **7**/1 | **fail** | 9/9 | 1 | **7**/1 | **fail** | 9/9 | 1 |

Receipts (sha256 in §Artifacts): `witness-{landed,A,B,C,D}-s{3501,7717}.json`.
Every receipt's `gate_sha256` equals the table hash above; `output_full=true`,
`output_match=9`, `output_total=9` in all ten runs.

- **A is killed as intended.** One call, result used for that record (output
  still 9/9, so the call was real), 1 stamp < 8 → `WITNESS=fail`, rc=1.
- **B survives with the landed gate's exact stamp signature** (9/1 at both
  seeds). The extra call is invisible to the threshold because the threshold
  only counts.
- **C survives at exactly the threshold** (8/1, `8 >= 8`), although 7 of the 8
  long records never enter the chunk matcher; their answers come from exact
  search, which is precisely K1's output path.
- **D is the boundary control**: 7 calls fail, so the pass/fail line is the
  total count, not any record coverage.

## Why landed is 9, not 8 (threshold slack)

`thresh-probe.py` loads the shipped witness module, generates the seed-3501
fixture, and runs the gate once per claim under the same private PS4, counting
chunk entry-line stamps per record:

```
dz-verbatim-1l 1   dz-mut 1   dz-verbatim-ml 1   dz-glued-left 1
dz-verbatim-ml 1   dz-mut 1   dz-line-bound 2   dz-edge 1
short-verbatim 0 (direct=1)
total chunk stamps=9 long_records=8 entry={'chunk': 1699, 'direct': 1677}
```

Only `dz-line-bound` (span occurs twice in one source, witness build at
mechanism-witness.py:163-170) triggers two calls. So the landed gate already
has one call of slack: a candidate could leave one long record uncovered and
still meet `>= 8` if it over-calls elsewhere — C is that candidate.

## Is a passing discarded-result engine a P2 failure?

**No — it is the disclosed limit, stated twice before data.**

- `corpus/evidence/round35/claims.md:106-109`: "an engine that […] calls the
  chunk matcher once for show and ignores its result […] can still defeat a
  trace witness; the witness rules out fingerprint-and-shortcut engines, not
  active anti-instrumentation" (24 words quoted).
- `tools/mechanism-witness.py:27-28`: "calls the chunk matcher once for show
  and ignores its result) can still defeat a trace witness".

P2's predicate is satisfied independently of these engines: the counter
separates its two committed variants (K1/K2, stamps `chunk=0` vs landed 9)
and the landed gate passes. I re-derived it on two seeds from the repo root:

```
$ python3 corpus/evidence/round35/c2-count.py --seed 3517 --receipt …/c2-s3517-root.json
WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass        rc=0
$ python3 corpus/evidence/round35/c2-count.py --seed 7717 --receipt …/c2-s7717-root.json
WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass        rc=0
  K1-python-exact  output=9/9 witness=fail stamps={'chunk': 0, 'direct': 1}
  K2-root-keyed    output=9/9 witness=fail stamps={'chunk': 0, 'direct': 1}
```

Receipts: `c2-s3517-root.json`, `c2-s7717-root.json`, both with
`gate_sha256=1f2fb4f5…ef617`, `battery_present=true`. 7717 was not an L1 seed.

**Qualification (calibration, not a kill).** C shows the witness is *weaker
than its own description*: mechanism-witness.py:20-21 says a run witnesses the
chunk matcher iff "the trace stamped the chunk matcher's function-entry line at
least once per long-span record (one stamp per call)", but the code at
mechanism-witness.py:295 is
`witness_ok = stamps["chunk"] >= long_records and stamps["chunk"] > 0` — no
record attribution at all. Eight calls on one record plus seven exact-search
records passes. This is still inside the disclosed "call for show and ignore"
limit, so P2 survives; the defect is that the docstring promises a per-record
property the implementation does not check. If a future round wants the stated
property, the stamp loop (mechanism-witness.py:270-282) already knows the line
but not the record: it would need to bracket trace lines at each `CLAIM` emit
and require ≥1 chunk stamp per long `CLAIM`, which would kill C and still pass
B only by the same disclosure.

## Secondary finding: the C2 counter's default battery path is CWD-relative

Invoked by absolute path from a scratch directory (a natural way to write an
out-of-tree receipt), the frozen counter reports the **before-state**:

```
$ cd /tmp/hyaku/chousa-r35/w2/MutWitnessThreshold
$ python3 /…/corpus/evidence/round35/c2-count.py --seed 3517 --receipt …/c2-s3517.json
WITNESS_SEPARATED=0/2 battery=absent                              rc=1
```

The receipt shows why: `battery=/tmp/…/tools/mechanism-witness.py`,
`battery_present=false`. `c2-count.py:133` defaults `--battery` to
`tools/mechanism-witness.py` and `c2-count.py:139` resolves it with
`os.path.abspath` against the CWD, not against the repository. `--gate`
(c2-count.py:132) has the same shape but was overridden here.

Consequences, both calibration/operability:
1. The printed label is byte-identical to the committed before-control
   (`controls/c2-before-s3501.json` → `WITNESS_SEPARATED=0/2 battery=absent`),
   so silence in the label conflates "battery absent from the tree" with
   "battery not found from this directory". Only the receipt's `battery` field
   distinguishes them (`/nonexistent/witness.py` vs the resolved scratch path).
2. The frozen kill rule ("any run of the counter against the landed gate below
   2/2 separation … kills C2") has no CWD qualifier; by its letter, a correct
   lane measured from the wrong directory reads as a kill. The claim's own
   command is repo-root-relative, so the committed P2 measurement is
   unaffected — this is a reproducibility hazard, not a contradiction.

Suggested fix (not applied; lane files read-only): derive the default from
`__file__` (repo root = `c2-count.py` two dirs up from `corpus/evidence/…`),
and print `battery=not-found(path=…)` with rc=2 when the resolved path is
outside the tree.

Minor: `mechanism-witness.py --tmp` requires the base directory to exist; a
missing base gives `rc=2 "temp dir: [Errno 2]…"`. `c2-count` creates it first
(`run_witness`), so the frozen path is unaffected; direct witness calls need
`mkdir -p`.

## Restoration evidence

- Lane gate never modified: `sha256sum tools/research-gate.sh` =
  `1f2fb4f5…ef617` at start and end; scratch `pristine-gate.sh` identical.
- Witness tool never modified: `9f537bfd…52b3` before and after.
- No gate/jj writes. `git status --porcelain -- tools/` shows only
  `?? tools/__pycache__/`, whose `mechanism-witness.cpython-314.pyc` mtime is
  16:46:04, earlier than my first probe (~17:00) and later than the source
  mtime 16:44:45 — pre-existing lane debris, reused (not rewritten) by my
  read-only import.
- All five `/tmp/.mw-once-*` sentinels removed (`ls` → no such file). Scratch
  only under `/tmp/hyaku/chousa-r35/w2/MutWitnessThreshold/`.

## Limits

- One fixture seed per candidate plus a second seed for confirmation; the
  fixture shape (9 records, 8 long) is fixed by `CLASS_COUNTS`, so
  `long_records=8` is not seed-dependent.
- I did not test active anti-instrumentation beyond discarding results (the
  disclosed class) and did not test the committed stub controls (out of scope).
- Engines patch only `tok_span_offsets`; the chunk matcher and the witness
  trace path are the shipped bytes. A gate that also moves the entry line or
  prints decoy `CLAIM` lines is untested.
- No network, no package installs.

## Artifacts

Lane dir `.ufo/waves/round-35/w2/MutWitnessThreshold/` (all sha256):

| file | sha256 |
|---|---|
| `patch-engines.py` | `9e9af4804ef7c98247240cd36604ecac4916519ac0c347aad50f251f576eed0d` |
| `span_search.py` | `ab435490b41cc338ff8c8f02ce327e0fa7a7bef4887367a01c396d8257a439c9` |
| `thresh-probe.py` | `298ca6a2736aabaa0e5e705d9b720097b6c5217151fd627057d479fad89c9e16` |
| `witness-landed-s3501.json` | `281492a744fcb363553e4f75b411c9d88702ebb17cc121f5b37cc25d2a979517` |
| `witness-landed-s7717.json` | `da401b36f224b80082b7e12553a56575991203275e37aa378d0a1c862a060ac4` |
| `witness-A-s3501.json` | `f9f3d3ed472e3ff08b9fbd4d422ffd6ed70b5ea7ebc02c3ca673449e07b4612e` |
| `witness-A-s7717.json` | `dbcab2bfe209008daa1eae3148c5988fd0bc49ec47fc7f09225f0cf624e033d4` |
| `witness-B-s3501.json` | `439e83e2be84d0a511899eafac28479f1796c5d996a81f5a81b2621a7fedb2cc` |
| `witness-B-s7717.json` | `6ad49d3693b05363dc28b07580357f031dea4d2a73619fd9790ae2c20684b027` |
| `witness-C-s3501.json` | `cc38663921dac831fd75102b066193b0593144b231aed27b49785f587193067e` |
| `witness-C-s7717.json` | `a9596e023e5aed4155ed5dfc1bf26bde9d919aefbe8deb9d710f2da56571d621` |
| `witness-D-s3501.json` | `9f142e75fa98102418416264141779022eee2e05707d453b1685e5a0485a748a` |
| `witness-D-s7717.json` | `ee3f9f4459f4ad197275753db81c4efeeb5fa9a3626023793e333455aecaeff6` |
| `c2-s3517-root.json` | `42eebe7ae77192134def9c97a0457f2b68f95d862d14b6a5048bf2c8756858cb` |
| `c2-s7717-root.json` | `9ac068aa962bd8bf470bdd9b938bf038413c8c35d1b7eac66f2ecdb873d8a700` |
| `c2-s3517.json` (wrong-CWD control) | `1d45d6dcd61ffed97af470e5d24c4f380b284062ab9fb9065f3aa4fdb161bd7c` |

Scratch (`/tmp/hyaku/chousa-r35/w2/MutWitnessThreshold/`): `pristine-gate.sh`
`1f2fb4f5…ef617`, `engine-A.sh` `6542ca7d…`, `engine-B.sh` `dad7fa03…`,
`engine-C.sh` `8b1553d4…`, `engine-D.sh` `3cbbc695…`.
