# ProbeEscapes33 — escapes inside read-field VALUES on flat claim records

Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`, revision tip `0fb300b5c27900ab8bb3abeb5f54776d71e04beb`.
Landed gate `tools/research-gate.sh` SHA-256 `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e`.
Base gate (`git -C <lane> show 2b9cc73aed30c2e2c95699db6617d9531ef49fb2:tools/research-gate.sh`) SHA-256
`f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0`.

**Verdict: C1 HOLDS on the assigned surface.** Across **229 well-formed flat claim records**
(29 hand-built escape cases + 200 randomized escape spellings) the landed gate's output is
**byte-identical to the base gate's** except the `ts=` header line. No input was found on which the
landed top-level reader changes a flat record's verdict, finding set or exit code. The four
divergences from a spec JSON reader that do exist (surrogate pairs, lone surrogate, `\u0000`, keys
spelled with an escape) are **inherited from base** and, for the decoding ones, **mandated by
contract item 4** (`claims.md:39-42`: "Everything else is the landed round-31/32 behaviour … records
without nesting or duplicates verify exactly as at base"). They are not refutations of C1; they are
limits to hand onward.

Files changed in the lane: **none**. Artifacts only under
`.ufo/waves/round-33/w2/ProbeEscapes33/` (all < 1 MiB), scratch under
`/fast/scratch/hyaku/chousa-r33/w2/ProbeEscapes33/` (1.8 MB, removed temp dirs, no processes left).

## What was attacked

The landed reader: `claim_scan` (`tools/research-gate.sh:1135`), `json_str` (`:1259`),
`json_has_key` (`:1267`), `json_dup` (`:1275`), `json_unescape` (`:1280`), called from
`verify_claims`. The escaping surface the counter never generates:

| escape family | record | landed observation | base observation |
|---|---|---|---|
| `\u00e9` BMP non-ASCII in span | E01 | supported, `at=line:2` | identical |
| `\u0041` BMP ASCII in span | E02 | supported | identical |
| `\uD83D\uDE00` surrogate pair, source holds real 😀 | E03 | **unsupported** | identical |
| surrogate pair, source holds look-alike `??` | E03b | **supported (false match)** | identical |
| lone surrogate `\uD800` | E04 | unsupported | identical |
| `\/` in span | E05 | supported | identical |
| `\\` in span (`C:\dir\file`) | E06 | supported | identical |
| `\"` inside span | E07 | supported | identical |
| `\"` inside id | E08 | supported, id printed as `E08_quote_id"q` | identical |
| `\/` inside source path | E09 | supported | identical |
| raw non-ASCII UTF-8 span | E10 | supported | identical |
| key spelled `"l\u0069ne"` (decodes to `line`) | E11 | ignored, supported | identical |
| `\t` in span | E12 | supported | identical |
| string value `{"line": "9"}` (escaped quotes) | E13 | supported, no line read | identical |
| `\u0000` in span | E14 | supported (`ab`, NUL dropped) | identical |
| span ends with `\` (`"trail\\"`) | E15 | supported | identical |
| `\u007b`/`\u007d` braces | E16 | supported | identical |
| sha256 pin spelled `"\u0033…"` | E17 | supported (pin decodes to the real hash) | identical |
| `\"` inside source path (`src/qu"ote.txt`) | E18 | supported | identical |
| mixed `\"` `\/` `\\` | E19 | supported | identical |
| value `a\", b {c}` before the read keys | E20 | supported | identical |
| empty member name `""` | E21 | ignored, supported | identical |
| `"line":2` (number, not string) | E22 | invalid (`line not a JSON string`) | identical |
| `\u0022` quotes in span | E23 | supported | identical |
| line value `"\u0032"` | E24 | supported, `at=line:2` | identical |
| unread value ending `\\`, read keys after | E25 | supported | identical |
| `\u005c` backslash in span | E26 | supported | identical |
| value containing `\u0022line\u0022: 9` | E27 | string content, supported | identical |
| raw astral UTF-8 😀 in span | E28 | supported | identical |

Fixture: `.ufo/waves/round-33/w2/ProbeEscapes33/fix/claims.jsonl`
(SHA-256 `d4e1c201f20a46598221d5c4700cd97fee3e0e4582f798da7682761e9ac4f5b7`), regenerable with
`gen_cases.py` (same dir) into a root that also holds `src/*`; per-record truth view in
`fix/cases.json`.

## Result 1 — differential landed vs base (the assignment)

```
$ timeout 300 bash ./landed-gate.sh verify-claims fix/claims.jsonl --root fix > run/landed3.out 2>&1   # rc=1
$ timeout 300 bash ./base-gate.sh   verify-claims fix/claims.jsonl --root fix > run/base3.out   2>&1   # rc=1
$ diff <(tail -n +2 run/base3.out) <(tail -n +2 run/landed3.out) && echo "BASE==LANDED"
BASE==LANDED
```

`run/landed3.out` SHA-256 `5f9bfebee135ba62ddbf578562f62c25da8e1f96cb59b6f690b0126007cf9aa1`,
`run/base3.out` SHA-256 `5c37ea2ae061ef4465acaf460aa6ed356df673337dd406fa4051dbc93f1ea699`.
Both: `VERDICT_BEARING_CLAIMS=26/29`, `research-gate v2 — … findings=3 drift=3`, rc 1.
The only byte that differs between the two files is the `ts=` stamp in line 1.

Second, wider differential — 200 randomized flat records in which the same span text is spelled
with a random mix of raw bytes, `\uXXXX`, `\\`, `\/` and `\"` (raw astral and raw BMP UTF-8 mixed in;
`fuzz_gen.py`, seed 20261023, `fuzz/claims.jsonl` SHA-256
`09076518c860f758f2026ad087da4830249323e98a532b2ae7d3adf6e0eebf06`):

```
$ timeout 300 bash ./landed-gate.sh verify-claims fuzz/claims.jsonl --root fuzz > run/fuzz.landed.out 2>&1  # rc=0
$ timeout 300 bash ./base-gate.sh   verify-claims fuzz/claims.jsonl --root fuzz > run/fuzz.base.out   2>&1  # rc=0
$ diff run/fuzz.base.out run/fuzz.landed.out
1c1
< research-gate v2 — ts=2026-10-23T09:07:19Z — …
> research-gate v2 — ts=2026-10-23T09:07:02Z — …
$ tail -1 run/fuzz.landed.out
RESEARCH_GATE: CLEAN (claims=200 supported=200 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
```

200/200 supported on both gates; identical except the timestamp. A JSON encoder that mishandled
`\\`/`\"`/`\u` inside values, or that let string content act as structure, would have shown up here
as a dropped or extra line; none appeared.

## Result 2 — reference reader (python top-level oracle, feasibility only)

`timeout 600 bash <lane>/.ufo/waves/round-33/controls/L1-design/oracle-gate.sh verify-claims
fix/claims.jsonl --root fix` → rc=1, `run/oracle3.out` SHA-256
`2b2f06a8b13174b69b0e131f4fc132baa8684b6c3d0a81d06abc3c63b00b7d9f`.
Differences from **both** gates (not landed-specific):

1. **Surrogate pair, real astral char in source.** Input line (span field is
   `"smile \ud83d\ude00 here"`):
   `{"id":"E03_surrogate_pair","source":"src/e03.txt","span":"smile \ud83d\ude00 here","expect":"supported","line":"2"}`
   landed/base: `CLAIM id=E03_surrogate_pair expected=supported observed=unsupported source=src/e03.txt at=- verdict=mismatch`;
   oracle: `observed=supported … at=line:2 verdict=match`. Cause: `json_unescape` replaces any
   surrogate half with `?` (`tools/research-gate.sh:1303-1304`), so the span decodes to
   `smile ?? here` and cannot match the real 😀.
2. **Same decode, inverted sign.** With `src/e03b.txt` line 2 holding `omega smile ?? here tau.`,
   landed/base report `observed=supported` (a **false match** on `??`), oracle reports
   `observed=unsupported`. A false positive is the worse direction.
3. **Lone surrogate** (`E04`, span `"x\ud800y"`): landed/base `observed=unsupported`; oracle
   `observed=invalid` (its python re-encoder refuses the lone surrogate, so the field reads empty).
4. **Key spelled with an escape** (`E11`, member `"l\u0069ne":"9"`, span on line 2): landed/base
   `observed=supported` (raw key text `l\u0069ne` ≠ `line`, `claim_scan` keeps raw key spellings);
   oracle `observed=mislocated` with `CLAIM_LINE_MISMATCH line=9-9`.
5. `\u0000` (`E14`) agrees between landed and oracle (`supported`): the oracle re-escapes to
   `\u0000`, and `json_unescape`'s bash `printf` drops the NUL in both, so this is a
   bash-representation limit shared by every reader in the harness, not a reader choice.

Items 1–3 are the only *decode* deltas and they are identical at base — item 4 of the contract pins
that behaviour. Item 4 is the exclusion `claims.md:80-81` names explicitly ("keys spelled with JSON
escapes (`"l\u0069ne"`)").

## Result 3 — malformed lines (outside the claim, direction confirmed)

`claims.md:136-140` (design v2) excludes lines that are not exactly one valid JSON object and asks
the candidate to fail closed. Measured, `bad/claims.jsonl`, three lines (trailing comma, trailing
garbage, unbalanced):

```
landed rc=1: CLAIM id=line1..line3 observed=invalid   (line=1 "not one well-formed JSON object")
base   rc=1: CLAIM id=I1_trailing_comma observed=supported at=line:1   (base read the trailing-comma line)
```

`run/bad.landed.out` `f65b11ad…`, `run/bad.base.out` `29a394d7…`. This is the *only* difference class
this probe can produce between the gates, and it is the intended fail-closed direction, not a C1
break: contract item 4 speaks about records "without nesting or duplicates", and v2 explicitly does
not claim non-object lines.

## Result 4 — counting commands (kill rule receipts)

All runs: `C1_TMP`/`TMPDIR` = scratch, stdout redirected to a file, fresh seeds never 3301-3373,
`--receipt` into `.ufo/waves/round-33/w2/ProbeEscapes33/`.

```
$ timeout 300 python3 <lane>/corpus/evidence/round33/c1-count-v2.py --gate <lane>/tools/research-gate.sh \
    --seed 4207 --receipt …/c1-landed-s4207.json > …/c1-landed-s4207.out 2>&1   # rc=0
$ … --seed 4209 --receipt …/c1-landed-s4209.json > …/c1-landed-s4209.out …      # rc=0
$ … --gate <scratch>/base-gate.sh --seed 4208 --receipt …/c1-base-s4208.json …  # rc=1
```

| receipt | seed | gate sha | label | predicate_holds | gate rc | misses |
|---|---|---|---|---|---|---|
| `c1-landed-s4207.json` | 4207 | `94a7be5a…` | `TOPLEVEL_FIELD_MATCH=156/156` | true | 1 | 0 |
| `c1-landed-s4209.json` | 4209 | `94a7be5a…` | `TOPLEVEL_FIELD_MATCH=156/156` | true | 1 | 0 |
| `c1-base-s4208.json` | 4208 | `f4731885…` | `TOPLEVEL_FIELD_MATCH=60/156` | false | 1 | 96 |

Counter SHA-256 recorded in every receipt: `cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514`
(design v2). Per-class: all 15 classes full on both landed seeds (duplicates `24/24`); base shows
`N2 0/12`, `N5 0/12`, `N11 0/6`, `D1 0/24`, `S2 0/6`, `S1 12/12`, `F1 12/12` — the exact flat/nested
split this probe started from. No landed run in round 33 by this seat is below 156.

## Findings to hand to L1 (not refutations of C1)

1. **P1 carries no evidence about value escapes.** `c1-count-v2.py:73-78` builds every string
   through `json.dumps`, which never emits `\uXXXX` or `\/`; CONFUSERS exercise `\"` and `\\` only.
   The 156 records therefore say nothing about escaped values, escaped keys, or surrogate pairs.
   The landed reader's behaviour on that surface is measured here for the first time (Result 1).
2. **Escaped key that decodes to a read field is invisible.** Minimal input:
   `{"id":"D1_plain_then_escaped","source":"src/d1.txt","span":"alpha bravo","expect":"supported","line":"2","l\u0069ne":"9"}`
   landed/base: `CLAIM id=D1_plain_then_escaped … observed=supported` and gate rc **0 (CLEAN)**
   (`run/dupesc.landed.out` `591f0205…`, identical to `run/dupesc.base.out` `ab9e22ba…`);
   oracle: `observed=invalid`, `FINDING CLAIM_RECORD_INVALID … duplicate top-level key`
   (`run/dupesc.oracle.out` `87a381a7…`). Contract item 2 (`claims.md:34-36`) speaks of a field that
   "occurs more than once among the top-level members" without saying whether member names are
   compared raw or decoded; `claims.md:80-81` excludes escaped spellings from the claim. If raw is
   intended, item 2 should say so, because a spec reader (RFC 8259 names are strings, escapes
   decoded) sees a duplicate here.
3. **Non-BMP spans encoded per JSON's surrogate-pair form cannot verify, and their lossy decode can
   manufacture a match** (`E03`, `E03b` above; `json_unescape:1303-1304`). Shared with base, so item
   4 protects it; a session that records a claim about an emoji/astral span will silently read
   `unsupported` (or a `??` match) rather than a decode error. [INFERENCE] RFC 8259 §7 (Strings,
   source row S062 per `claims.md`) is the rule that a surrogate pair denotes one astral character;
   I did not open that row this round, so this is stated from the python `json` behaviour observed
   via the oracle (L1-design `mk-oracle.py`), not quoted.
4. `\u0000` in any read string is dropped (`E14`): span `a\u0000b` matches source `ab`. Same at base
   and in the oracle; a bash limit, not a reader bug.

## Risks / limits

- Fixture A is 29 hand-authored records, one host, one bash (`printf %b` Unicode handling is
  bash-builtin behaviour; a different bash could change `\u` decoding for both gates alike).
- Fixture B only randomizes the *spelling* of spans that must verify; negative escape cases are
  covered only by E03b/E04/E11 (single records).
- Escaped values were not fuzzed for `source`/`id` beyond one record each (E08, E09, E18); the
  decode path is the same `json_unescape` for all seven keys, so a key-specific divergence is
  unlikely but not excluded by count.
- The `--root`-relative resolution and the token-boundary matcher were exercised only through these
  records; span edge cases (punctuation joins) are other seats' items.
- No network used; no URL opened; no installs; no lane/fleet writes; no jj/git writes.

## Artifact index (`.ufo/waves/round-33/w2/ProbeEscapes33/`)

| path | SHA-256 |
|---|---|
| `fix/claims.jsonl` (29 escape records) | `d4e1c201f20a46598221d5c4700cd97fee3e0e4582f798da7682761e9ac4f5b7` |
| `fix/cases.json` (spec truth view) | — |
| `gen_cases.py`, `fuzz_gen.py` | generators (regenerate `fix/`, `fuzz/` + `src/`) |
| `fuzz/claims.jsonl` (200 records, seed 20261023) | `09076518c860f758f2026ad087da4830249323e98a532b2ae7d3adf6e0eebf06` |
| `run/landed3.out` | `5f9bfebee135ba62ddbf578562f62c25da8e1f96cb59b6f690b0126007cf9aa1` |
| `run/base3.out` | `5c37ea2ae061ef4465acaf460aa6ed356df673337dd406fa4051dbc93f1ea699` |
| `run/oracle3.out` | `2b2f06a8b13174b69b0e131f4fc132baa8684b6c3d0a81d06abc3c63b00b7d9f` |
| `run/fuzz.landed.out` | `8b62319f357d963483872e797bac0e3dbb76165bbd2e6b4c2a1593e9541cbcd7` |
| `run/fuzz.base.out` | `7714ee076a2395c8533448cb9a3b531876306b89d533ebc3fc3057dc2273fea3` (differs from landed only in `ts=`) |
| `run/bad.landed.out` | `f65b11ad004196d632689d593d7a90bba361817ee00bf4334f08bb9b04bc0c8a` |
| `run/bad.base.out` | `29a394d7684faa5352e5c5da1657f5de061e5f6b9108e11f4622adb0d8b24921` |
| `run/dupesc.landed.out` | `591f0205274771cace01c200aa6a92d0defe105bad152a0739c982f0341f9a33` |
| `run/dupesc.base.out` | `ab9e22ba2de8133f848ecff745cf77f6da0057887db7e99e3999c4730187ba46` |
| `run/dupesc.oracle.out` | `87a381a74bfe8d75191071daa1c344a3a310a9a457eea27f7ec8726b41be459c` |
| `bad-claims.jsonl`, `dupesc-claims.jsonl` | minimal malformed / escaped-key-duplicate fixtures |
| `c1-landed-s4207.json`, `c1-landed-s4209.json`, `c1-base-s4208.json` | counter receipts |
