# ProbeFlatBehaviour33 — flat-record contract item 4, differential base vs landed

Lane: chousa-shokunin, round 33, wave 2. Item: contract item 4 (round-31/32 behaviour on flat
records) on the landed gate. Method: same claims fixtures through the base gate
(`2b9cc73a…` / `f4731885…`) and the landed gate (`0fb300b5…` / `94a7be5a…`), diff every line.
No lane file was edited; no installs; no background jobs.

## Setup (scratch, read-only lane)

```
git clone -q <lane> /fast/scratch/hyaku/chousa-r33/w2/ProbeFlatBehaviour33/{landed,base}
git -C landed checkout -q 0fb300b5c27900ab8bb3abeb5f54776d71e04beb
git -C base   checkout -q 2b9cc73aed30c2e2c95699db6617d9531ef49fb2
sha256sum landed/tools/research-gate.sh base/tools/research-gate.sh
→ 94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e  landed
→ f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0  base
```

Source corpus (artifacts `.../fixtures/`): `source.txt` = 5 lines (`alpha bravo charlie` at
lines 1 and 5, `delta echo foxtrot` line 2, `golf hotel india` line 3, `juliet kilo lima
NEGATIVE` line 4); `source2.txt`; `source3.txt` = `AA/BB/AA/BB` for later-occurrence binding.
Every gate call is `timeout 300 <gate> verify-claims <fixture> --root <scratch>/corpus`;
stdout+stderr captured per gate under `.../outputs/`.

The claims-mode code diff base→landed (`.../outputs/claims-region.diff`) adds exactly three
things and changes nothing else in the region: `claim_scan` (landed `:1135-1290`), a
`json_dup` guard on the marker-default row (`:1608-1612`), and the duplicate-read-field block
(`:1614-1644`). So every output difference below is attributable to those.

## Counted claim re-run (kill rule honoured)

`c1-count-v2.py` sha256 `cb354dd1…a514`, lane gate sha256 `94a7be5a…506e`, fresh seeds, stdout
redirected to files, `--receipt` in this directory:

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
C1_TMP=<scratch>/tmp TMPDIR=$C1_TMP python3 corpus/evidence/round33/c1-count-v2.py \
  --gate "$PWD/tools/research-gate.sh" --seed 6181 \
  --receipt .ufo/waves/round-33/w2/ProbeFlatBehaviour33/counter-6181.json > .../counter-6181.out
→ TOPLEVEL_FIELD_MATCH=156/156, rc=0   (receipt predicate_holds=true, gate_rc=1, all 15 classes full)
seed 6182 identical (counter-6182.json / .out).
```

No lower run exists. This confirms L1's 52f07c74 and 94a7be5a measurements; P1 is not falsified.

## Flat differential — results

Fixtures: `fixtures/claims-main.jsonl` (72 records), `claims-later.jsonl` (7), `claims-dup.jsonl`
(14), `claims-edge.jsonl` (19), `claims-x.jsonl` (6), `claims-badjson.jsonl` (17),
`malformed-scalar.jsonl` (1). Outputs in `outputs/`.

**Equal base vs landed (zero bytes of difference, timestamps masked):** line+sha256 together
(correct/correct, wrong pin, correct pin+wrong line, correct pin + line naming another
occurrence, uppercase/short/numeric/null pins, pin whitespace, sha-before-line precedence),
line ranges (`N`, `N-M`, M<=N, leading zero, spaces, en dash, non-string line: number/null/
true/float/array), multi-line spans with and without `line`, later-occurrence binding (first vs
second occurrence, `at=line:5`/`lines:3-4` for bound, `first_delimited_occurrence` for
mislocated), `expect=contradicted` with top-level `marker`, `marker_default` rows (normal,
empty-changing, non-string), `expect=unsupported` (span absent and span present + finding),
missing/empty fields, duplicate **unread** keys, empty-key repeats, nested-only duplicates, and
all refused sources (absolute `/etc/hostname`, `../outside.txt`, `https://…`, `file:///…`,
`session:…` → same finding class/severity/obs). `claims-later.jsonl`: 7/7 identical.
`claims-x.jsonl`: 6/6 identical (`outputs/x-*.txt`).

**Valid-JSON differential fuzz:** 240 generated records (random read-field combos, 26 with
nested containers holding read-key decoys, string confusers including `} ] { , "`, trailing
escaped backslash): 26/26 differences occur only on records that carry nested extras; 0
differences among the 214 records without nested containers. Every difference is base reading a
nested `line`/`sha256`/`source`/`id`/`span`/`marker` decoy that landed correctly ignores
(`outputs/fuzz-*.txt`, generator `/fast/scratch/.../fuzz.py`).

**Every difference, base → landed (all intended by C1 except the last group):**

| case | base | landed |
|---|---|---|
| `d01`–`d08` duplicated top-level read field | supported | `CLAIM_RECORD_INVALID duplicate top-level key <k>`, invalid |
| `q01` duplicated `marker` | unproven | invalid (v2: invalid by implementation, not counted) |
| `q02` `id` duplicated, differing | id=q02 supported | invalid id=line8 (documented) |
| duplicate `marker_default` row (`edge:4`) | default row, marker `AAA` | invalid claim; later findings say "no marker defined" |
| `zzz` marker_default + nested `id` | CLAIM id=zzz invalid | no claim line (default row) |
| `n01`,`e01`,`e02`,`e03`,`e14` nested decoys | reads decoy (mislocated/stale/supported) | top-level-only result |
| `g01` trailing ` x` after the object | supported | `not one well-formed JSON object` invalid |
| `m08` `"junk":}` | supported | invalid |
| `m09` single-quoted object | invalid "missing id" | invalid "not one well-formed JSON object" |
| `m01`–`m07`, `b01`–`b17` invalid JSON values (see below) | supported, CLEAN | supported, CLEAN (unchanged) |

Refused sources and all marker/line/sha semantics on flat records: no difference.

## Contract break found (input the counter never generates)

Landed usage says (`tools/research-gate.sh:366-367`): "a repeated top-level read field, or a line
that is not one well-formed JSON object, makes the record invalid (observed=invalid)". Header
`:53` and the knowledge note `corpus/knowledge/claim-record-fields-r33.md:66` ("malformed lines
(the reader refuses them; no counter class measures it)") say the same.

Measured: the reader fails closed only on **structural** malformations. The scalar-value branch
(`:1218-1226`) accepts any non-empty token, and the nested-value skipper (`:1190-1216`) validates
only bracket balance/string state, never member-name quoting, value grammar or escape set. So
lexically invalid JSON is verified as a well-formed record.

Minimal input (`fixtures/malformed-scalar.jsonl`):

```json
{"id":"BAD1","source":"source.txt","span":"delta echo foxtrot","expect":"supported","junk":xyz}
```

```
landed: rc=0  CLAIM id=BAD1 … observed=supported … verdict=match
              RESEARCH_GATE: CLEAN (claims=1 supported=1 … invalid=0 findings=0 drift=0)
base:   identical (rc=0, same line)          # outputs/bad-{base,landed}.txt
```

Matrix `fixtures/claims-badjson.jsonl` (17 lines, all rejected by CPython `json.loads` except
`NaN`, which Python accepts and RFC 8259 does not): landed accepts all 17 as supported and exits 0
CLEAN (`outputs/claims-badjson-landed.txt`, `VERDICT_BEARING_CLAIMS=17/17`). Accepted forms
include unquoted/garbage scalars (`xyz`, `+1`, `01`, `1.`, `.5`, `1e`, `tru`, `1.2.3`, `-`,
`'single'`), `NaN`, unquoted nested member names (`{"a":oops}`, `{"a" 1}`), bad array syntax
(`[1 2]`, `[1,,2]`), invalid escapes (`"bad\qescape"`) and a raw tab inside a string. Base
behaves identically (it never had the reader); this is a landed-gate contract-vs-behaviour
mismatch, not a regression against base.

Impact: a claims file containing such lines can produce `RESEARCH_GATE: CLEAN`, exit 0, while the
record is not one well-formed JSON object. P1 is unaffected: `claims.md:139-140` explicitly does
not claim such lines ("the candidate is asked to fail closed on them; no fixture class counts
it"); the counter generates only valid JSON.

## Verdict

- **P1 / counted C1: HOLDS** — 156/156 on seeds 6181 and 6182 against `94a7be5a…`, receipts with
  `predicate_holds=true`; flat, line/sha, range, multi-line, later-occurrence, marker,
  `marker_default`, unsupported and refused-source behaviour is byte-identical to base except the
  three intended C1 differences.
- **Fail-closed clause of the stated reader contract: BROKEN** — lines that are not one
  well-formed JSON object are accepted and can close CLEAN, contradicting gate usage `:366-367`,
  header `:53`, and knowledge note `:66`. Minimal line and outputs above. No counter class
  generates it, so it does not falsify 156/156; it falsifies the accompanying "fail closed"
  statement.

## Risks / limits

- Base and landed both accept lexically invalid JSON, so no round-33 candidate-only regression;
  the risk is the lane shipping a reader described as fail-closed that is only structurally so.
- Python `json.loads` was the conforming parser used to classify validity (local, no network);
  the RFC statement is taken from the lane's cited S062, not re-opened here.
- Fixtures are mine (not the counter); nested decoys/duplicates are classified per `claims.md`
  v2, including the uncounted `marker`/`marker_default` duplicate choices.
- Source files are tiny scratch files; cost/TOCTOU/8 MiB paths not exercised. The lane selftest
  was not run (wave rule).
- Artifacts: `.../ProbeFlatBehaviour33/{fixtures,outputs,counter-6181.*,counter-6182.*}`, each
  file < 1 MiB; experiment scratch `/fast/scratch/hyaku/chousa-r33/w2/ProbeFlatBehaviour33/`.
