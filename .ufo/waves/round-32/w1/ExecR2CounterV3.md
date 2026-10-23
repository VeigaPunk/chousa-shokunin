# ExecR2CounterV3 — round-32 W1, routed defect R2 (counter half)

Verdict: **done**. Two new counter files (v3) were written beside the frozen v2 counters, which
stay byte-identical. v3 scores the landed gate at its total (132/132, twice per counter) and
scores each round-31 non-string mutant below its total (120/132, only the new class misses).
No lane production file, fleet file, jj state or git index was touched; no installs, no network.

## Files (new, in this dir)

| File | SHA-256 | Bytes |
|---|---|---|
| `.ufo/waves/round-32/w1/ExecR2CounterV3/r31-c1-count-v3.py` | `0efbd172bbd89bd44c2cca0ececf933b662f556fc71ad3983a69f3529b36efb6` | 16270 |
| `.ufo/waves/round-32/w1/ExecR2CounterV3/r31-c2-count-v3.py` | `654183e17adc22162d54025a34f4ec2aa9099f2d1118ee07f5b2a9358ea736a8` | ~14 KB |

Both are copies of the frozen v2 files plus only the v3 edits; `r31-c1-v3.diff` and
`r31-c2-v3.diff` are the full `diff -u` against the frozen files (hunk headers: C1 `:3,28,37,46,54,74,83,94,103`; C2
`:3,12,38,47,55,69,78,98`), no unrelated hunk. Frozen v2 files untouched:

```
c3aca35da30ee47edc3402daa559f43320e44a82d3a0143b5ea283ec8c49b427  corpus/evidence/round31/c1-count.py
1064fdb356e25440c64bb4d4d5363acb9c1bbc32c687c8ea50096d74c849d500  corpus/evidence/round31/c2-count.py
```
(the c2 hash is the `frozen_counter_sha256` recorded in
`.ufo/waves/round-31/falsify/MutC2Parse/kill-matrix.json`).

## v3 design (v2 + one fixed non-string class per counter)

- C1 v3: `TOTAL = 132` (`r31-c1-count-v3.py:67`), new class `I2_nonstring_line_value`, 12 claims,
  `invalid` (`:80`), sub-variants `number/null/true/false/array/object` two each (`:137`), builder
  at `:224` (span present; value `5`, `null`, `true`, `false`, `["5"]`, `{"n":5}`). Truth follows
  round-31 `corpus/evidence/round31/claims.md` C1 contract 1: "any other value of a present
  `line`" is invalid (a present non-string is present).
- C2 v3: `TOTAL = 132` (`r31-c2-count-v3.py:62`), new class `I2_nonstring_sha_value`, 12 claims,
  `invalid` (`:72`), same six kinds two each (`:84`), builder at `:204` (`17`, `null`, `true`,
  `false`, `["0"*64]`, `{"n":17}`); every fixture has its span present, so a gate that treats a
  non-string pin as absent reports `supported` and misses.
- `ABSENT = object()` sentinel in both (C1 `:144`, C2 `:90`) so a present JSON `null` is included
  in the record instead of being confused with an omitted key.
- Receipt schemas bumped to `chousa-r31-c1-receipt/v3` (`:333`) and `chousa-r31-c2-receipt/v3`
  (`:293`); `TOTAL` is stated in both docstrings (`:9-22` C1, `:29-40` C2) and in the exit sentence.
- Value kinds were chosen to carry no inner `"sha256": "..."`/`"line": "..."` string, so a value's
  type, never an embedded pin, decides the case (comment at C2 `:205-206`).

## Nested-key class: omitted, with measurement

The round-31 contract's only nested-relevant sentence is "Unknown JSON keys are ignored, as at
base" (`claims.md:150-151`; gate-side reader is a flat raw-line regex, `tools/research-gate.sh:1094-1101`).
Measured on the landed gate `0bc318b3` (`nested-probe.log`, fixture `nested-probe.claims.jsonl`,
gate exit 1):

```
CLAIM id=n1_nested_line expected=supported observed=mislocated ... at=line:2
CLAIM id=n2_nested_sha expected=supported observed=stale ...
FINDING CLAIM_LINE_MISMATCH ... obs=id=n1_nested_line line=9-9
FINDING CLAIM_SOURCE_REVISION_MISMATCH ... obs=id=n2_nested_sha pin=000000000000
```

A nested `"line"`/`"sha256"` is read as the record's own. Round-31 critics call this a contract
violation (`.ufo/waves/round-31/falsify/CriticEdgeC2.md:84-90`, "a nested `sha256` is read as the
record's own pin"; `.ufo/waves/round-31/falsify/ReviewIntegrationDiff31.md:3`), and it is carried
to round 32 as a survivor class (`corpus/lessons/round-31.md:97-99`). Including it in v3 with the
contract truth would make the **landed gate itself** miss the total, which the assignment forbids;
so v3 omits it and this probe stands as evidence of a landed gate defect, not a counter gap.

## Mutant gates

| Gate | SHA-256 | Provenance |
|---|---|---|
| MutC1Grammar nonstring-absent | `85d85a7bae9e0fbd0f91d5c4c0e5ab845cb2cdeedeaca8cc4090eb4050673890` | committed copy, `.ufo/waves/round-31/falsify/MutC1Grammar/nonstring-absent.mutant.sh` (hash verified) |
| MutC2Parse m1-nonstring-absent | `f9da8257da57606cf52a48901aff42497ff34df74590a9141a8f2074b8ac0807` | **rebuilt**: pristine round-31 gate `c23d7537…` from `/fast/scratch/hyaku/chousa-r31/w2/MutC2Parse/repo/tools/research-gate.sh`, one documented edit at line 1444 (`kill-matrix.json` M1 `edit`): `json_has_key "$line" sha256` → `json_str "$line" sha256 >/dev/null 2>&1`; resulting hash equals `f9da8257…` exactly. Diff: `m1-mutation.diff` (one hunk, one line). |

Rebuilt gate kept at `<scratch>/gates/m1/tools/research-gate.sh` so the gate's `LANE_ROOT`
(`dirname(gate)/..`) never contains the fixture dirs; `C1_TMP`/`C2_TMP`/`TMPDIR` were
`/fast/scratch/.../ExecR2CounterV3/tmp` for every run (peer `ChousaR32A2.CtlC2WeakReaderB`'s
layout hazard). Scratch root: `/fast/scratch/hyaku/chousa-r32/w1/ExecR2CounterV3`.

## Results (all receipts in this dir; every receipt binds the final counter SHA)

| Run | Gate | Seed | Label | Exit | Receipt |
|---|---|---|---|---|---|
| C1 v3 landed | `0bc318b3` | 5010428042290874802 | `LINE_BINDING_MATCH=132/132` | 0 | `landed.c1.5010428042290874802.json` |
| C1 v3 landed | `0bc318b3` | 5194322385725341644 | `LINE_BINDING_MATCH=132/132` | 0 | `landed.c1.5194322385725341644.json` |
| C2 v3 landed | `0bc318b3` | 5010428042290874802 | `REVISION_BINDING_MATCH=132/132` | 0 | `landed.c2.5010428042290874802.json` |
| C2 v3 landed | `0bc318b3` | 5194322385725341644 | `REVISION_BINDING_MATCH=132/132` | 0 | `landed.c2.5194322385725341644.json` |
| C1 v3 MutC1Grammar | `85d85a7b` | 5010428042290874802 | `LINE_BINDING_MATCH=120/132` | 1 | `mutC1Grammar.c1.json` |
| C1 v3 MutC1Grammar | `85d85a7b` | 5194322385725341644 | `LINE_BINDING_MATCH=120/132` | 1 | `mutC1Grammar.c1.s2.json` |
| C2 v3 MutC2Parse m1 | `f9da8257` | 5010428042290874802 | `REVISION_BINDING_MATCH=120/132` | 1 | `mutC2Parse.c2.json` |
| C2 v3 MutC2Parse m1 | `f9da8257` | 5194322385725341644 | `REVISION_BINDING_MATCH=120/132` | 1 | `mutC2Parse.c2.s2.json` |
| C1 v3 MutC2Parse (cross) | `f9da8257` | 5010428042290874802 | `LINE_BINDING_MATCH=132/132` | 0 | `mutC2Parse.c1.json` |
| C2 v3 MutC1Grammar (cross) | `85d85a7b` | 5010428042290874802 | `REVISION_BINDING_MATCH=132/132` | 0 | `mutC1Grammar.c2.json` |

Receipt detail: every mutant miss is exactly the new class and nothing else —
`per_class {"I2_nonstring_line_value": "0/12"}` with all 12 misses
`{"class":"I2_nonstring_line_value","truth":"invalid","observed":"supported"}` on `85d85a7b`, and
`{"I2_nonstring_sha_value": "0/12"}` with the same shape on `f9da8257`. Cross runs are clean, so
the mutations are separable from the other counter. `gate_rc` is 1 in the landed receipts by
design: the fixture necessarily contains mislocated/stale claims, and the counter accepts gate rc
0 or 1 (v2 rule, unchanged).

v2 on the same gates was a survivor (committed receipts, not rerun):
`falsify/MutC1Grammar/nonstring-absent.mutated.c1-1.json` = `LINE_BINDING_MATCH=120/120`,
`predicate_holds=true`, gate `85d85a7b`; `falsify/MutC2Parse/m1-nonstring-absent.seed1.receipt.json`
= `REVISION_BINDING_MATCH=120/120`, `predicate_holds=true`, gate `f9da8257`. The v3 delta is
therefore exactly the 12 new claims each.

Fixture spot-check (`--keep`, kept under scratch `keep-c1`, `keep-c2`; 6 of 12 shapes shown):
`"line": null`, `"line": 5`, `"line": ["5"]`, `"line": false`, `"line": true`; `"sha256": {"n": 17}`,
`"sha256": ["0"*64]`, `"sha256": true`, `"sha256": false`, `"sha256": 17`.

## Exact commands (representative; every run used the same prefix)

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
    C1_TMP=<scratch>/tmp C2_TMP=<scratch>/tmp TMPDIR=<scratch>/tmp \
    timeout --signal=TERM --kill-after=5s 900 \
    python3 .ufo/waves/round-32/w1/ExecR2CounterV3/r31-c1-count-v3.py \
      --gate tools/research-gate.sh --seed 5010428042290874802 \
      --receipt .ufo/waves/round-32/w1/ExecR2CounterV3/landed.c1.5010428042290874802.json
```
Mutant runs replace `--gate` with
`/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-31/falsify/MutC1Grammar/nonstring-absent.mutant.sh`
or `<scratch>/gates/m1/tools/research-gate.sh`. Mutation rebuild check:
`diff -u <pristine c23d7537 copy> <scratch>/gates/m1/tools/research-gate.sh` = the single hunk in
`m1-mutation.diff`; `sha256sum` = `f9da8257…`.
Binding check (last step): all 10 receipts' `counter_sha256` equal the final file hashes
(`binding mismatches: []`).

## Limits / risks

- TOTAL is 132, not the frozen predicate numeral 120. The frozen P1/P2 sentences in `claims.md`
  and in the v2 docstrings are historical and were left verbatim; v3 labels itself `n/132` and
  states this in its docstring. A round-32 predicate that adopts v3 must restate the numeral.
- Mutant gates are built on the round-31 gate `c23d7537`/`ee1024fd`, not on the landed `0bc318b3`,
  so a mutant score isolates the mutated dimension rather than scoring a round-32 candidate. Both
  cross runs are 132/132, which is the check that the non-mutated dimension still passes.
- Nested-key and duplicate-key classes, and the counter never reading `at=` (carried defects), are
  outside R2's stated counter scope; nested is separately measured above and shown to be a landed
  gate defect.
- No selftest was run (editing wave; parent owns the gate). R2's second bullet (selftest cases for
  non-string `sha256`, end-line-only binding, per-claim span-before-stale, trim pin, fail-open
  hash-read fault injection) is not in this seat's assignment and is not claimed.
- Installations: none. Network: none. Scratch use: `/fast` had 234 G free before the runs; this
  dir is 148 K and no file exceeds 1 MiB.
