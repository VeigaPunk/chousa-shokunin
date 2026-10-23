# ProbeTypes33 — top-level value types on the landed gate (round 33, wave 2)

**Item.** Probe top-level value types in `verify-claims`: non-string top-level
`id`/`source`/`span`/`expect`/`marker` (number, `true`, `null`, array, object), empty strings, a
top-level `line`/`sha256` that is a container, JSON numbers with exponent/negative/fraction as
unknown members, and `true`/`false`/`null` as unknown members. Compare landed vs base vs the
python feasibility oracle; any record whose landed verdict differs from the contract
(`corpus/evidence/round33/claims.md`, design v2 governs) is a finding.

**Pins (verified by sha256, all runs on explicit copies).**

| role | bytes | sha256 |
|---|---|---|
| landed | `gate-94a7be5a.sh` = `git show 0fb300b:tools/research-gate.sh` | `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e` |
| base | `base-gate.sh` = `git show 2b9cc73a:tools/research-gate.sh` | `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` |
| oracle | `.ufo/waves/round-33/controls/L1-design/oracle-gate.sh` | `930a20755418eed3277a893c5b8a96bffd93f2ea90a79fd79bc122426e5677a9` |

Lane reads only via `git show`/`cp`; no lane writes. Fixture root
`/fast/scratch/hyaku/chousa-r33/w2/ProbeTypes33/fx/`: `src/a.txt` =
`alpha one\nbravo TARGET_SPAN M charlie\ndelta four\n`, 70 one-line claim records
(`claims.jsonl`, sha256 `3f0c3fd5…f89361`), plus single-line fixtures `f1a`–`f1d` and four
`marker_default` files (`md-a`–`md-d`, the last with source `src/c.txt`). Every record was run through each gate with
`bash <gate> verify-claims <file> --root <fx>`; per-record output in `outs/`, verdict matrix in
`matrix.tsv` (sha256 `7d6070e4…4bab`).

## Counter runs (kill rule)

Every run carried `--receipt` and redirected stdout to a file.

| receipt | gate argument | `gate_sha256` in receipt | seed | label | holds |
|---|---|---|---|---|---|
| `c1-landed-s4201.json` | `tools/research-gate.sh` (lane path) | `94a7be5a…` | 4201 | `TOPLEVEL_FIELD_MATCH=156/156` | true |
| `c1-gate94a7be5a-s4203.json` | explicit `gate-94a7be5a.sh` copy | `94a7be5a…` | 4203 | `TOPLEVEL_FIELD_MATCH=156/156` | true |
| `c1-landed-s4202.json` | `tools/research-gate.sh` (lane path) | **`45d76b4f…`** | 4202 | `TOPLEVEL_FIELD_MATCH=156/156` | true |

Command: `C1_TMP=<scratch>/tmp timeout 900 prlimit --nproc=2000 --as=4000000000 python3
corpus/evidence/round33/c1-count-v2.py --gate <gate> --seed <N> --receipt <dir>/<name>.json >
<dir>/<name>.out 2>&1` (rc=0 each; `counter_sha256` = `cb354dd1…a514` each). The third run is
reported because it happened: the lane **working-tree** gate changed under me between runs (see
Risks), so that receipt records `45d76b4f…`, not the landed `94a7be5a…`. It printed 156/156
anyway; it is not evidence about the landed revision.

## Result — 60 contract-decided type records, landed conforms on 60/60

`matrix.tsv` classifies each of the 70 records; 60 are decided by contract items 1–4, 10 are
invalid-JSON lines the contract explicitly does not claim. Landed (`94a7be5a`) equals the
contract expectation on **all 60 decided records**. Landed equals the oracle on **66/70**; the
four exceptions (rows 32, 33, 35, 37) are invalid JSON (finding F1). Landed differs from base on
17 rows, and every one is an item-1/2 fix or a fail-closed improvement:

- **Non-string read fields → invalid, as at base.** `id` = number/`true`/`null`/array/object
  (rows 01–05), `source` = number/array (06–07), `span` = `null`/object (08–09), `expect` =
  `true`/array (10–11): `observed=invalid`, `expected=-` where the value is unreadable; base
  identical.
- **Empty strings → invalid, as at base.** `id`/`source`/`span`/`expect` empty (12–15), `line`
  `""` (16), `sha256` `""` (17): invalid. `marker ""` is absent (18, supported) — base identical.
- **Top-level `line`/`sha256` containers and scalars → invalid, as at base.** `line` `{}`/`[]`/
  `2`/`true`/`null` (19–23), `sha256` `{}`/`[]`/`123`/`true` (24–27): invalid, base identical.
  These are the r31/32 "present non-string is malformed, never absent" rule, unchanged.
- **Unknown numeric/literal members → ignored.** `1e5`, `-1.5`, `0.5`, `-0.0`, `1E5`, `1e+3`,
  `0` (28–31, 61–64) and `true`/`false`/`null` (31): supported, base identical. A duplicated
  *unknown* key (`"x":1,"x":2`, row 48) is supported — not a read field.
- **Item 1 with a non-string top-level field beats a nested decoy.** `"line":{"line":"2"}` →
  invalid (41); `"sha256":{"sha256":"<correct pin>"}` → invalid (42); `"marker":{"marker":"M"}`
  with `expect=supported` → supported (43) and with `expect=contradicted` → unproven (44).
  Base read the nested member in all four (supported / supported / invalid / contradicted), so
  landed == oracle here.
- **Item 2 duplicates.** `line` duplicated string-then-number (45), identical twice (57),
  differing (68), number-then-string (69); `id` identical twice (46, 67); `source`
  string-then-array (47): all invalid, CLAIM line carries the top-level id where the contract
  says so (`id=p46`, `id=p67`). Duplicated `marker` (70) invalid — implementation, not counted
  (`claims.md:113-114`).
- **Item 3 string content / valid nesting.** `note:"{\"line\": \"9\"}"` (50), a trailing escaped
  backslash (51), valid nested object/array (39, 40): supported. Base mislocated row 40 (it read
  the nested `"line":"9"` inside the array); landed == oracle.

## F1 — the fail-closed ask is only partly met (boundary; not counted; base identical)

Minimal one-line inputs, each alone in its file, on landed `94a7be5a`:

```
{"id":"f1a","source":"src/a.txt","span":"TARGET_SPAN","expect":"supported","x":tru}
{"id":"f1b","source":"src/a.txt","span":"TARGET_SPAN","expect":"supported","x":01}
{"id":"f1d","source":"src/a.txt","span":"TARGET_SPAN","expect":"supported","x":"a<TAB>b"}
```

Landed: `CLAIM id=f1a expected=supported observed=supported … verdict=match` and
`RESEARCH_GATE: CLEAN` rc=0 (`f1-single-line.log`, sha256 `980e2e8f…84f3`; base identical).
Oracle: `CLAIM id=line1 expected=- observed=invalid …` and `RESEARCH_GATE: DRIFT` rc=1. So a line
that is not a JSON object is verified as a supported claim and can close CLEAN. Contract:
`claims.md:30` "A claim record is one JSON object per line", and `claims.md:139-140` "lines that
are not exactly one valid JSON object (the candidate is asked to fail closed on them; no fixture
class counts it)". It is explicitly **not claimed** and base behaves the same (no regression),
but the landed reader's comment (`tools/research-gate.sh:1126-1128` at `94a7be5a`) enumerates only
three fail-closed shapes — unbalanced/mismatched brackets, trailing garbage, a non-string member
name — and a bare token that is not a JSON literal is not among them. `x:NaN` (f1c) is accepted
by landed **and** by the oracle (python's `json` accepts `NaN`), so the oracle cannot adjudicate
NaN/Infinity.

## F2 — a duplicated `marker_default` row becomes an invalid claim (outside counter and battery)

Minimal 2-line input (`md-d.jsonl`, sha256 `7a93e860…aacd`; source `src/c.txt` =
`alpha one\nbravo TARGET_TEXT QQ charlie\ndelta four\n`):

```
{"marker_default":"QQ","marker_default":"ZZ"}
{"id":"q3","source":"src/c.txt","span":"TARGET_TEXT","expect":"contradicted"}
```

The three gates disagree three ways on the same bytes:

- base `f4731885`: `CLAIM id=q3 expected=contradicted observed=contradicted … verdict=match`,
  `RESEARCH_GATE: CLEAN` rc=0, claims=1 (first value `QQ` wins; the span line contains `QQ`).
- landed `94a7be5a`: `CLAIM id=line1 expected=- observed=invalid …`, `FINDING
  CLAIM_RECORD_INVALID … duplicate top-level key marker_default`, then `CLAIM id=q3 …
  observed=unproven …`, `RESEARCH_GATE: DRIFT` rc=1, claims=2.
- oracle: `CLAIM id=q3 … observed=unproven …`, `FINDING CONTRADICTION_MARKER_ABSENT … declared
  marker not found within span lines`, `RESEARCH_GATE: DRIFT` rc=1, claims=1 (python
  `json.loads` keeps the last value `ZZ`).

So base keeps the row a directive with the first value, the oracle keeps it a directive with the
last value, and landed turns it into an invalid claim and drops the directive (base emits no CLAIM
line for such a row; landed does). Contract: v2 item 2 (`claims.md:111-114`) enumerates `line`,
`sha256`, `source`, `span`, `expect`, `id`; `marker_default` is not among them, and v1
`claims.md:80` lists `marker_default` rows under "Not claimed". v1 item 4 (`claims.md:39-41`)
says "Everything else is the landed round-31/32 behaviour"; v2 item 4 (`claims.md:116-118`) scopes
exactness to "as far as the no-harm battery measures" — the battery has **0** `marker_default`
lines (grep of `.ufo/waves/round-33/w1/ExecNoHarmBase33/battery.sh`), and the counter generates no
`marker_default` row at all. Under the governing v2 text this is therefore not a counted break;
under v1's unqualified sentence the row's classification (directive vs invalid claim) is a
deviation. Direction is fail-closed (the ambiguous directive is refused rather than half-applied),
and RFC 8259 §4 leaves the duplicated value itself unpredictable. Correction to my own first
fixture (`md-c`, kept in `outs/`): its span text `TARGET_SPAN` contains the oracle's last-wins
value `N`, so the oracle also printed contradicted there; `md-d` removes that coincidence. A
sibling seat's directory `.ufo/waves/round-33/w2/ProbeMarkerDefault33/` exists on this shape; I
did not read or edit it.

## Post-repair spot-check at tip `165acd5f` (commit `0cad05e`, after my measurements)

The working-tree edits I saw in flight were committed as `0cad05e`; the gate at that tip is
`165acd5f6cebfb1d0a179f75572315ae6458ae330fdfc1f1ac412c36478a3563`. Re-running my fixtures
against an explicit copy of that gate (outputs `outs/tip165acd5f.*.out`):

- rows 32, 33, 34, 35, 37 (bare tokens `tru`, `01`, `NaN`, `+1`, `'a'`) now `observed=invalid` —
  F1's bare-token instances are closed, and the tip is stricter than the python oracle on `NaN`.
- the other 65 records keep their `94a7be5a` verdicts, so all 60 contract-decided records still
  conform at the tip.
- `md-d` is unchanged: the duplicated `marker_default` row is still refused (the commit message
  calls this deliberate — "marker_default rows with a repeated read field refused").
- **`f1d` (a raw TAB inside a string value) is still accepted**: `CLAIM id=f1d expected=supported
  observed=supported … verdict=match`, `RESEARCH_GATE: CLEAN` rc=0. The oracle rejects it
  (`json.loads` refuses an unescaped control character in a string), and the repair's own comment
  lists raw control bytes inside strings as "Not checked (as at base)", so this one fail-closed
  instance is live at the tip.

This is a spot-check, not a gate verdict: I did not run the selftest, the no-harm battery or the
counter on the tip (parent's gate).

## Verdict

**HOLDS** for the counted C1 value-type contract: counter v2 prints `156/156` twice on the landed
gate `94a7be5a` (seeds 4201, 4203), and all 60 contract-decided type records match items 1–4.
No input on this axis breaks the governing v2 contract. The two deviations are (F1) in the
explicitly not-claimed invalid-JSON band, base-identical and permissive, and (F2) outside both
the counter and the no-harm battery — a duplicated `marker_default` row is reclassified as an
invalid claim — fail-closed, with base, oracle and landed disagreeing three ways.

## Risks

1. **The lane working-tree gate was edited live during this run.** Committed gate at `0fb300b`
   and `4c076a0` is `94a7be5a` (`git diff 0fb300b 4c076a0 -- tools/research-gate.sh` empty), but
   while I ran, the working tree changed `94a7be5a` → `45d76b4f` (06:10:31) → `b808e9b5` →
   `220bcf17` (06:11:12), and the edits were then committed as `0cad05e` (gate `165acd5f`). A
   mid-edit snapshot (`gate-tip.sh`, `b808e9b5`) crashed with `line 1658: p46: unbound variable`
   and emitted no CLAIM lines. Any seat measuring "the gate" must pin bytes and record
   `gate_sha256`; my receipts do.
2. The oracle accepts `NaN`/`Infinity` (python `json` default), so it cannot serve as the
   fail-closed authority for those tokens.
3. F2's disposition depends on which item-4 text governs (v1 unqualified vs v2 battery-scoped);
   a duplicated `marker_default` also has no single base-equivalent across readers (base
   first-wins, oracle last-wins, landed refuses), so "keep base behaviour" is not well defined
   for that row.

## Limits

70 hand-built records, not exhaustive. I did not attack D1/D2/D5, sources, knowledge or QUALITY
rows (outside this item), and did not re-run the selftest or the no-harm battery (parent's gate).
No network, no subagents, no background jobs, no git/jj writes, no lane file edits; the only
files I wrote are this report and the artifacts under
`.ufo/waves/round-33/w2/ProbeTypes33/`.
