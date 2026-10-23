# ProbeDupVariants33 — duplicate forms beyond the C1 counter (round 33, WAVE 2)

Item: probe duplicates on the landed gate beyond what `c1-count-v2.py` generates — three or more
occurrences, a duplicated `marker`, an `id` duplicated with differing values, non-string duplicates
(`"line":5,"line":"3"`), two different keys each duplicated, duplicates in `marker_default` rows,
and duplicated unread keys (`"claim"` twice — must stay valid). Check `observed` and the
`CLAIM_RECORD_INVALID` finding text. Do not edit lane files.

## 0. Identity, and a lane that moved during the wave

- Base gate: `git -C <lane> show 2b9cc73aed30c2e2c95699db6617d9531ef49fb2:tools/research-gate.sh`
  → sha256 `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` (scratch copy
  `base-gate.sh`).
- **Landed gate pinned as assigned**: `git -C <lane> show 0fb300b5c27900ab8bb3abeb5f54776d71e04beb:
  tools/research-gate.sh` → sha256 `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e`
  (7742 lines; scratch copy `landed-gate-94a7be5a.sh`). Every result below is from this copy.
- Feasibility oracle: `.ufo/waves/round-33/controls/L1-design/oracle-gate.sh` (read-only, used as a
  third reader; it is not a candidate).
- **Drift observed mid-wave**: at 06:11 the lane tip was `4c076a0` and `tools/research-gate.sh` was
  dirty; its sha256 was `b808e9b5…e55e4`, then `154f7d3d…b4ec` seconds later, with a new
  `JSON_DUPDIFF` table ("r33 post-falsify: three or more repeats, ReviewKnowledge33"). At report
  time the tip is `0cad05e` ("post-falsify repairs (uncounted fail-closed clauses)") and the gate is
  `165acd5f…a3563`. My first probe pass (06:07–06:10) therefore straddled two file versions; I
  discarded it and re-ran everything against the pinned 94a7be5a copy. Snapshot differentials
  against `154f7d3d` and `165acd5f` are reported separately (§5) and are not evidence about 94a7be5a.

## 1. Counter runs (kill rule)

Both runs are on the landed gate 94a7be5a, both carry `--receipt`, both have stdout redirected to a
file. Fresh seeds, outside 3301–3373.

```
C1_TMP=<scratch>/tmp TMPDIR=<scratch>/tmp \
python3 corpus/evidence/round33/c1-count-v2.py --seed 4401 \
  --receipt .ufo/waves/round-33/w2/ProbeDupVariants33/c1-landed-s4401.json > …/c1-landed-s4401.out
→ TOPLEVEL_FIELD_MATCH=156/156, exit 0, all 15 classes full (D1_duplicate_top_level 24/24)
  receipt: counter_sha256=cb354dd1…e6a514 gate_sha256=94a7be5a…8506e matched=156 total=156 predicate_holds=true
same command, --seed 4402 → TOPLEVEL_FIELD_MATCH=156/156, exit 0, predicate_holds=true
```

No other counter run was made. I deliberately did not run it against the dirty working-tree gate: the
file changed between two consecutive reads, so a run there is not reproducible.

## 2. Method

Fixture root `<scratch>/root/src/a.txt` (3 lines; span `beta gamma` on line 2; sha256
`b373ef7a6591de3d1aa38a73ac3ab45d72d1e0fc951ed4fe4c376999d6d9cfb4`). Each probe is one claims file
holding the verbatim line under test, run through three readers:

```
bash <gate> verify-claims probes/<p>.jsonl --root <root>       # base, landed, oracle
```

Drivers `drive.py` (39 probes) and `drive2.py` (12 probes); inputs and per-gate raw stdout in
`probes/`, `probes2/`; tables `summary-pinned.txt`, `summary2-pinned.txt`. Plain control
(`p00_plain`) is identical on all three readers (`observed=supported`).

## 3. Assigned forms on the landed gate 94a7be5a

| form | minimal input (members in order) | landed 94a7be5a | base f4731885 |
|---|---|---|---|
| 3× `line`, identical | `"line":"2","line":"2","line":"2"` | rc1, `CLAIM id=c1 … observed=invalid`; `obs=line=1 duplicate top-level key line` | rc0, `observed=supported` |
| 3× `line`, 2,2,3 | `"line":"2","line":"2","line":"3"` | same as above (invalid) | rc0 supported |
| 3× `line`, 2,3,2 | `"line":"2","line":"3","line":"2"` | invalid, reason `line` | rc0 supported |
| 3× `span`, s,s,t | `"span":"beta gamma","span":"beta gamma","span":"beta"` | invalid, reason `span` | rc0 supported |
| 3× `id`, c1,c1,c2 | `"id":"c1","id":"c1","id":"c2"` | invalid, reason `id`, **`CLAIM id=c1`** (F2) | rc0 supported id=c1 |
| 3× `id`, c1,c2,c1 | `"id":"c1","id":"c2","id":"c1"` | invalid, reason `id`, `CLAIM id=line1` | rc0 supported |
| 3× `id`, c1,c2,c2 | `"id":"c1","id":"c2","id":"c2"` | invalid, reason `id`, `CLAIM id=line1` | rc0 supported |
| duplicated `marker`, same/diff, expect=supported | `…,"expect":"supported","line":"2","marker":"M","marker":"M"` (and `"M","N"`) | invalid, reason `marker` | invalid, but text `marker present but expect=supported (fixture violation)` |
| duplicated `marker`, expect=contradicted | `"expect":"contradicted",…,"marker":"M","marker":"M"` | invalid, reason `marker`, `expected=contradicted` | rc1 `observed=unproven` + `CONTRADICTION_MARKER_ABSENT … declared marker not found within span lines` |
| `id` duplicated, differing | `"id":"c1","id":"c2"` | invalid, `CLAIM id=line1` | rc0 supported id=c1 |
| `id` duplicated, identical (counted control) | `"id":"c1","id":"c1"` | invalid, **`CLAIM id=c1`** | rc0 supported |
| `id` second value non-string | `"id":"c1","id":5` | invalid, `CLAIM id=line1` | rc0 supported |
| non-string `line`, 5 then "2" | `"line":5,"line":"2"` | invalid, reason `line` | rc0 supported (reads `"2"`) |
| non-string `line`, "2" then 5 | `"line":"2","line":5` | invalid, reason `line` | rc0 supported |
| non-string `line`, 5 then 5 | `"line":5,"line":5` | invalid, reason `line` | rc1 `line not a JSON string` |
| non-string `sha256` | `"sha256":123,"sha256":"b373…"` | invalid, reason `sha256` | rc0 supported |
| non-string `expect` | `"expect":5,"expect":"supported"` | invalid, reason `expect`; CLAIM shows `expected=-` | rc0 supported |
| two keys duplicated | `source`×2 + `span`×2 | invalid, reason `source`; CLAIM `source=-` | rc0 supported |
| two keys duplicated | `line`×2 + `sha256`×2 | invalid, reason `line` | rc0 supported |
| two keys duplicated | `marker`×2 + `line`×2 | invalid, reason `marker` (loop order at :1622 puts the uncounted key before `line`) | rc1 marker fixture text |
| duplicated unread keys | `"claim"`×2 same / diff; `"note"`×3; `"claim"`×2 + `"meta"`×2 (nested) | **valid**, `observed=supported`, rc0 | valid except `meta` case (base reads nested `"line":"9"` → `observed=mislocated`) |
| nested duplicates only | `"a":{"line":"9"},"b":{"line":"8"}` + one top-level `line:"2"` | valid, supported | valid, supported |
| same duplicated line twice in one file | (scan-cache probe) | both records invalid, ids `line1`, `line2` | both supported |

Contract check (`corpus/evidence/round33/claims.md`, Design v2, "Contract item 2 (v2, counted)"):
"A duplicated top-level `line`, `sha256`, `source`, `span`, `expect` (identical or differing
values) or `id` (identical values) makes the record `invalid`, and its CLAIM line carries the
record's id. A duplicated `marker`, and an `id` duplicated with differing values, are invalid by the
implementation but not counted." Every row above agrees with that sentence on 94a7be5a: counted
duplicates invalid with the id preserved; `marker` duplicates invalid; `id` with differing values
invalid and unreadable (`line1`); unread-key duplicates stay valid.

`observed`/finding text for duplicates is uniform: `CLAIM id=<id> expected=<…> observed=invalid
source=<…> at=- verdict=invalid` plus `FINDING CLAIM_RECORD_INVALID severity=warn surface=claims
obs=line=N duplicate top-level key <K>` (`tools/research-gate.sh` at 0fb300b:1643). Side effects
inside the CLAIM line: a duplicated `expect` prints `expected=-`; a duplicated `source` prints
`source=-` (neither is required or forbidden by the contract).

## 4. Findings

**F1 — the counted duplicate contract holds on every form probed, including 12 forms the counter
never generates** (triples, differing `id`, non-string values, two-key duplicates, mixed-type
duplicates). No counted class can fail through a duplicate form that `c1-count-v2.py` omits.

**F2 — mixed `id` triples print an id that a later occurrence contradicts (uncounted).**
Input `{"id": "c1", "id": "c1", "id": "c2", "source": "src/a.txt", "span": "beta gamma",
"expect": "supported", "line": "2"}` → 94a7be5a prints `CLAIM id=c1 … observed=invalid` and
`obs=line=1 duplicate top-level key id`. The gate's own rule comment says the opposite for differing
values: "a duplicated \"id\" leaves no id to print" (pinned copy :1620) and "differing or
non-string values leave the id unreadable" (:1633); the code compares only the first two values
(:1636), so the third is never examined. Contract item 2's caveat ("an `id` duplicated with
differing values … invalid by the implementation but not counted") is satisfied (the record is
invalid); the printed identity is the hole. A NUL-tailed second value behaves the same way:
`{"id":"c1","id":"c1\u0000"}` prints `id=c1` (bash drops the decoded NUL). Base prints `id=c1 … supported`.
**Repaired post-falsify**: lane snapshot `154f7d3d` and current `165acd5f` print `CLAIM id=line1`
for the same line (JSON_DUPDIFF compares every repeat's raw body).

**F3 — duplicated `marker_default` invalidates records whose seven read fields occur once
(uncounted; three-way divergence; still present at 165acd5f).**
- Row `{"marker_default": "delta", "marker_default": "delta"}` → 94a7be5a rc1, a *CLAIM line*
  `CLAIM id=line1 expected=- observed=invalid source=- at=-` and `obs=line=1 duplicate top-level
  key marker_default`; base rc0 with **no** CLAIM line; oracle rc0 with no CLAIM line.
- Claim `{"id":"c1","source":"src/a.txt","span":"beta gamma","expect":"supported","line":"2",
  "marker_default":"delta","marker_default":"delta"}` → 94a7be5a rc1 `observed=invalid`; base and
  oracle rc0 `observed=supported`. `marker_default` is not one of the seven fields contract item 1
  enumerates, so this invalidation is neither required nor forbidden by item 2.
- Downstream effect (two-line file): duplicated default row + contradicted claim →
  base applies the **first** default (`delta`) → `observed=contradicted` (match); 94a7be5a drops the
  default → `observed=unproven` + `CONTRADICTION_MARKER_ABSENT … no marker defined (per-claim or
  marker_default)`; oracle applies the **last** default (`nope`) → `observed=unproven` +
  `declared marker not found within span lines`. Three readers, three answers on an input the
  counter does not generate; the row is also counted in `claims=` (`N_CLAIMS`) on the landed gate.
  This is a behaviour change outside C1's enumerated surface (v1 contract item 4 "Everything else
  is the landed round-31/32 `verify-claims` behaviour"; v2 marks item 4 out of P1). L1 should decide
  whether the fail-closed extension is wanted; it does not affect any counted class.

**F4 — lines that are not valid JSON are accepted as claims (non-counted contract sentence not
met on 94a7be5a).** Design v2, "Not claimed (correction to v1's list)": "lines that are not exactly
one valid JSON object (the candidate is asked to fail closed on them; no fixture class counts it)."
Two minimal inputs the reader accepts (rc0, `observed=supported`):
- `{"id": "c1", "note": -, "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}`
- `{"id": "c1", "note": tru, "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}`

Cause: the literal branch (:1218) only requires a non-empty token (`[[ -n $val ]] || return 1`).
Base behaves identically (rc0 supported); the oracle rejects both (`FINDING CLAIM_RECORD_INVALID
… obs=line=1 missing id`). Structural malformations are caught (`{"note": 1"id": "c2", …}` → `not
one well-formed JSON object`; `line` 5 then 5 → duplicate reason). The extra CLAIM line is visible
in the summary too: the duplicated default row makes `p26` `claims=2 invalid=1` on 94a7be5a versus
`claims=1 invalid=0` at base. **Repaired post-falsify**: snapshots
`154f7d3d` and `165acd5f` reject both inputs with `obs=line=1 not one well-formed JSON object`.
This is the one place where 94a7be5a misses a sentence of claims.md on inputs the counter does not
generate; the sentence sits in "Not claimed", so P1 is unaffected.

**F5 — explicit non-claims stay non-claims.** A duplicated key spelled with an escape
(`{"id":"c1","\u0069d":"c2",…}`) is not detected by 94a7be5a (rc0, `id=c1`), while the oracle
detects it (rc1, `id=c2`). claims.md excludes "keys spelled with JSON escapes (`"l\u0069ne"`)";
recorded as consistent, not a break. Decoded-identical spellings are handled: `"id":"c1"` +
`"id":"\u00631"` → invalid with `CLAIM id=c1`.

## 5. Snapshot differential (context only, not evidence about 94a7be5a)

Same 51 probes against two working-tree snapshots, labelled by sha:

| snapshot | F2 mixed `id` triple | F4 `tru` / `-` | F3 marker_default duplicates |
|---|---|---|---|
| `154f7d3d82a9…b4ec` | `CLAIM id=line1` (fixed) | rejected, `not one well-formed JSON object` (fixed) | unchanged (invalid, still `expected=-`, `source=-`) |
| `165acd5f6ceb…3563` (current lane, tip 0cad05e) | `CLAIM id=line1` (fixed) | rejected (fixed) | unchanged |

Tables: `summary-wt-154f7d3d.txt`, `summary2-wt-154f7d3d.txt`, `summary-wt2-165acd5f.txt`,
`summary2-wt2-165acd5f.txt`. No counter run was made against these snapshots (moving file).

## Verdict

**HOLDS** — on the landed gate `94a7be5a…` the C1 duplicate contract is met for every assigned
form: counted duplicates (six keys, identical/differing, 3+ occurrences, non-string values, two keys
at once) are `invalid` with the record's id on the CLAIM line and a `duplicate top-level key <K>`
finding; a duplicated `marker` and an `id` duplicated with differing values are invalid; duplicated
unread keys stay valid; nested duplicates only change nothing. No counted class fails on an input the
counter does not generate.
Two non-counted deviations are reported, one open and one already repaired upstream: **F3** (open,
`marker_default` duplicates over-invalidate and change downstream verdicts relative to base and
oracle) and **F2/F4** (present on 94a7be5a, repaired at lane snapshots `154f7d3d`/`165acd5f`).
**F4 is the only claims.md sentence I observed the landed gate miss** — the uncounted "asked to fail
closed" clause for `-`/`tru` literal tokens.

## Limits

- Verdict is about `94a7be5a` only; the lane file changed under me (0fb300b → 4c076a0 → 0cad05e,
  gate dirty during the first pass). Evidence about the lane's current gate is limited to §5.
- Oracle is the L1 feasibility reader, not a candidate; it was used only to label divergences.
- No network, no installs, no lane writes, no git/jj writes. No process signals.
- Not probed: escaped key spellings beyond F5 (explicitly not claimed), surrogate pairs, CRLF
  input, `verify-all` manifest reading, marker semantics beyond duplicated-`marker` invalidity.
- Scratch (gates, drivers, full raw outputs): `/fast/scratch/hyaku/chousa-r33/w2/ProbeDupVariants33/`
  (`landed-gate-94a7be5a.sh` = 94a7be5a…, `base-gate.sh` = f4731885…, `wt2-gate.sh` = 165acd5f…).
  Artifacts copied here: `MANIFEST.txt`, `drive.py`, `drive2.py`, the six summary tables and
  `probes/`, `probes2/`; counter receipts `c1-landed-s4401.json`, `c1-landed-s4402.json` (+ `.out`).
