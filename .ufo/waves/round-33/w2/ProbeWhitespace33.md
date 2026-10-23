# ProbeWhitespace33 — JSON whitespace and line endings on flat claim records (r33 w2 FALSIFY)

Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`, landed tip `0fb300b5c27900ab8bb3abeb5f54776d71e04beb`.
Gates under test: landed `tools/research-gate.sh` SHA-256 `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e`;
base `2b9cc73aed30c2e2c95699db6617d9531ef49fb2:tools/research-gate.sh` (`git show`, read-only) SHA-256
`f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0`; L1 feasibility oracle
`.ufo/waves/round-33/controls/L1-design/oracle-gate.sh` SHA-256 `930a20755418eed3277a893c5b8a96bffd93f2ea90a79fd79bc122426e5677a9`.
Lane files changed: **none**. All work in `/fast/scratch/hyaku/chousa-r33/w2/ProbeWhitespace33/` (gate copies, 300 KB each,
not copied) and my artifact dir `.ufo/waves/round-33/w2/ProbeWhitespace33/` (472 KB total; largest file 4 KB).

## What I attacked

Contract item 4 (`corpus/evidence/round33/claims.md`, "Everything else is the landed round-31/32
`verify-claims` behaviour … Records without nesting or duplicates verify exactly as at base") on flat,
non-duplicated **valid** JSON records, across: no spaces; spaces/tabs around `:` and `,`; leading/trailing
whitespace; CRLF; CR between members; plus the non-JSON whitespace characters form feed (0x0C) and vertical
tab (0x0B) between members; NBSP; CR-only separators; a trailing comma; a BOM; raw control characters
inside string values. 35 byte-exact inputs (`cases/`), each run on the landed and base gate against the same
fixture root (`root/SRC.md`, SHA-256 `abec6741a6b02969a6d80720290140c110a96cbbfd07481091d9cdb10069d127`).

Commands (full log `commands.txt`; per-case outputs `out/<case>.{landed,base,oracle}.txt`):

```
timeout 120 bash landed-gate.sh verify-claims cases/<case>.jsonl --root "$PWD/root" > out/<case>.landed.txt 2>&1
timeout 120 bash base-gate.sh   verify-claims cases/<case>.jsonl --root "$PWD/root" > out/<case>.base.txt   2>&1
timeout 120 bash <oracle-gate.sh> verify-claims cases/<case>.jsonl --root "$PWD/root" > out/<case>.oracle.txt 2>&1
```

Differential table (all 35 rows) is `summary.txt`; outputs compared after masking only `ts=`.

## Result 1 — item 4 on valid flat records: HOLDS

Every valid-JSON case is **byte-identical** between landed and base after `ts=` masking, with the same
`CLAIM id=… observed=supported … verdict=match` and the same `RESEARCH_GATE: CLEAN` summary:

- no spaces (`01`), spaces around `:`/`,` (`02`), tabs (`03`), mixed (`04`), leading/trailing space+tab (`05`);
- CRLF (`06`), CR between members (`07`), CRLF with a blank CRLF line (`30`), CRLF + `line`/`sha256` pins (`16`);
- full whitespace spread with both pins (`15`), `line="2"` pin + sha256 (`32`);
- space inside a string value (`19`), escaped `{[,:}]`/`\"` in strings (`26`), string ending in an escaped
  backslash (`27`), `\t` escape in `id` (`28`), number/exponent/negative/bool/null members (`25`),
  `[]`/`{}` values (`29`), four records in one file with mixed styles and no final LF (`20`);
- `{}` and `{  }` (`22`, `23`) are valid JSON but not records — both gates mark them `invalid` identically
  (`missing id`), so even that edge is byte-equal.

No finding on the assigned axis: whitespace and line endings on valid flat records preserve base behaviour.

## Result 2 — FINDING (fail-open): FF and VT are accepted as JSON whitespace by the landed gate

Minimal input line (`cases/08-ff-between.jsonl`, exact bytes, `od -c`: `"W08" \f , \f "source"` …):

```
{"id":"W08"<FF>,<FF>"source":"SRC.md"<FF>,<FF>"span":"alpha"<FF>,<FF>"expect":"supported"}
```

`\v` (0x0B) variant `cases/09-vt-between.jsonl` behaves identically; `cases/10-ff-colon`,
`cases/11-vt-colon`, `cases/31-ff-space-mix`, `cases/17-pinned-ff` (with `line`+`sha256` pins) too.

| gate | exit | CLAIM / verdict |
|---|---|---|
| landed `94a7be5a` | 0 | `CLAIM id=W08 expected=supported observed=supported source=SRC.md at=line:1 verdict=match` / `RESEARCH_GATE: CLEAN (claims=1 … invalid=0 findings=0 drift=0)` |
| base `f4731885` | 0 | identical (`out/08-ff-between.base.txt`) |
| L1 oracle `930a2075` (python `json.loads` reader) | 1 | `CLAIM id=line1 expected=- observed=invalid … verdict=invalid`, `FINDING CLAIM_RECORD_INVALID … obs=line=1 missing id`, `RESEARCH_GATE: DRIFT` (`out/08-ff-between.oracle.txt`) |
| `python3 json.loads` on the same bytes | — | `JSONDecodeError: Expecting ',' delimiter: line 1 column 12 (char 11)` |

JSON's grammar admits only space, tab, LF and CR as insignificant whitespace (RFC 8259 §2; not re-opened
here — the measured corroboration is `python3 json.loads` and the L1 oracle rejecting the same bytes), so
this line is **not** "one well-formed JSON object". The landed gate nevertheless treats it as a well-formed
record and verifies the claim.

Why this is a contract break, not just base parity:

- `claims.md` design v2, "Not claimed": *"lines that are not exactly one valid JSON object (the candidate is
  asked to fail closed on them; no fixture class counts it)"* — the landed candidate does not fail closed here.
- The landed gate's own help text (`tools/research-gate.sh:365-367`) states: *"a line that is not one
  well-formed JSON object, makes the record invalid (observed=invalid)"*. On FF/VT lines that promise is false.
- The design's own feasibility oracle rejects exactly these bytes, so the landed reader is weaker than the
  instrument the design was accepted on.
- The counter (`c1-count-v2.py`) never generates these bytes, so P1 is unaffected — this is a defect on
  inputs the counter does not generate.

Root cause (landed): `claim_scan` skips POSIX `[[:space:]]` (C locale, set by `local LC_ALL=C` at
`tools/research-gate.sh:1136`), and POSIX space includes 0x0B and 0x0C. Occurrences:
`tools/research-gate.sh:1144, 1149, 1155, 1173, 1176, 1244, 1249`. The scan doc comment
(`:1117-1134`) says "bracket depth over `{}` and `[]` outside strings" but never narrows whitespace to the
JSON set. [INFERENCE] the minimal fix is to compare against the four RFC whitespace characters
(space, tab, CR, LF) at those seven sites.

Sharpening evidence that this is a whitespace-set bug, not a deliberate leniency: the landed gate **does**
fail closed on other non-JSON forms that the base gate accepts —
NBSP between members (`14`: landed invalid/DRIFT exit 1, base verified/CLEAN exit 0),
CR-only record separators (`21`: invalid vs verified), trailing comma (`24`: invalid vs verified), and a
form feed *in place of a comma* (`35`: landed invalid, base verified). So structure checking works; only the
whitespace character class is too wide (NBSP is outside it and is rejected; FF/VT are inside it and are not).

## Result 3 — shared/inherited fail-opens (not item-4 regressions)

- Leading/trailing FF/VT (`12`, `13`) are stripped before validation by the prestrip loops
  `tools/research-gate.sh:1591-1592`, which are byte-identical to base `:1440-1441` (`[[:space:]]` again).
  Base behaviour, so not an item-4 break, but the same fail-closed promise is unmet for `{"…"}\f`.
- Raw FF and raw TAB inside a string value (`33`, `34`) are accepted by both gates (`observed=supported`,
  CLEAN), while `python3 json.loads` rejects them (`Invalid control character at: line 1 column 11`) and the
  oracle marks them invalid. `claim_scan`'s string loop accepts any byte except `"` and `\`. Adjacent
  control-character class; also outside the counted fixture.

## Counter re-runs (kill rule honoured)

Every run on the landed gate used `--receipt` in my dir and stdout redirected to a file (no pipe), fresh
seeds 3411/3412 (never 3301-3373), `C1_TMP=TMPDIR=<scratch>/tmp`, `timeout 900`:

```
python3 corpus/evidence/round33/c1-count-v2.py --gate tools/research-gate.sh --seed 3411 \
  --receipt .ufo/waves/round-33/w2/ProbeWhitespace33/c1v2-seed3411.json > <scratch>/out/c1v2-seed3411.stdout.txt 2>&1
```

- seed 3411: rc=0, `TOPLEVEL_FIELD_MATCH=156/156`; receipt `c1v2-seed3411.json` (sha256
  `d452a1295408db49db1feda8c0b76ccea1d490246601d792afb5fd05b1ba04a6`): `gate_sha256=94a7be5a…`,
  `counter_sha256=cb354dd1…`, `gate_rc=1`, `matched=156`, `predicate_holds=true`.
- seed 3412: rc=0, `TOPLEVEL_FIELD_MATCH=156/156`; receipt `c1v2-seed3412.json` (sha256
  `f5d504836b01f06cfa6efbe85eef5630e0296c018bc911f257d61655eb16cb05`): same fields; `elapsed_s=3.771`.
- Per-class tallies were full on both (`D1_duplicate_top_level 24/24`, `F1_flat_plain 12/12`,
  `N1..N11` and `S1/S2` all complete), via `out/c1v2-seed3411.stdout.txt`, `…3412.stdout.txt`.

No lower run of the counter on the landed gate occurred in this probe; the frozen P1 v2 predicate is **not**
falsified by counting.

## Verdict

- **P1 v2 (counted): HOLDS** — 156/156 on fresh seeds 3411 and 3412, receipts above.
- **Contract item 4, assigned axis (valid flat JSON, whitespace/line endings): HOLDS** — zero differential
  across the 20 valid-JSON cases; FF/VT rows are not valid JSON and are not item-4 material.
- **Contract item 1 / fail-closed clause: BROKEN, narrowly** — the landed gate reports `RESEARCH_GATE: CLEAN`
  with `observed=supported` for a line containing raw form feed or vertical tab between members. The L1
  oracle and `python3 json.loads` reject the same bytes, and the landed help text (`:365-367`) and the v2
  contract both promise `invalid`. Inputs are ones the counter never generates, so this is a claim-surface
  defect, not a P1 miss.

## Limits

- 35 hand-built inputs, one source fixture, one host (bash 5.x, LANG=en_US.UTF-8; the interior finding is
  locale-independent because `claim_scan` sets `LC_ALL=C`).
- Only `verify-claims` was exercised; no selftest/build/lint per wave rule; no other mode's JSON reading.
- The oracle is an L1 control instrument, cited as corroboration, not as the contract.
- The FF/VT lines are invalid JSON; the contract itself says no fixture class counts them, so whether the
  L1 treats this as a break or a documented limitation is an integration judgement — the measured behaviour
  and the contradicting promise lines are what I can assert.
