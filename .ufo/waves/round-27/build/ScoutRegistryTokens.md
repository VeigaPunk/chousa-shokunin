# ScoutRegistryTokens — C3 S-id token derivation and expected occurrence counts

Seat `ChousaR27.ScoutRegistryTokens`, round 27 attempt 1. Author-lane advice;
not an outside judge. **Static, read-only: no gate/selftest/regression execution,
no runtime probe, no fixture created, no production edit.** Observed facts come
from reading `tools/research-gate.sh` at lane HEAD `64eec5d4…` (base master);
ground truth for r26 failures is the committed
`.ufo/waves/round-26/falsify/FRegistryIdBoundary.md`, not a rerun.

Note: the lane working tree is being edited concurrently — C1 usage controls
landed at `tools/research-gate.sh` ~6007–6110 (+26 lines) while I read. The C3
scanner lines cited below are unchanged; symbol names are authoritative.

## 1. What is being derived

The only S-id consumer for this contract is
`metadata_registry_check_source` (`tools/research-gate.sh:2472–2507`), called
once from `verify_metadata:2695`. Its input is the `source:` value assembled by
continuation (`$rest` then `$'\n'`-joined non-blank lines until blank line,
`## `, or EOF; `verify_metadata:2640–2688`). Its current scan is:

- `source_id_re='(^|[^[:alnum:]_])(S[0-9]{3,})([^[:alnum:]_]|$)'` — line 2474;
- `while [[ $source_scan =~ $source_id_re ]]` — line 2477;
- `source_scan=${source_scan#*"$source_match"}` — line 2503 (the defect);
- `META_SOURCE_NO_ROW_ID` emitted once iff no match — lines 2505–2506.

`verify_metadata` declares `local LC_ALL=C` at line 2539, so
`[[:alnum:]]` == `[A-Za-z0-9]` and `${#var}` counts bytes at the call site.
`metadata_registry_check_source` itself declares no locale; if it is refactored
or its body moved, the pin must move with it.

## 2. Derived token model (the contract the repair must implement)

Let `A = [A-Za-z0-9_]` (C locale). For the value `v`:

1. Split `v` into maximal runs over `A`. Every other byte — space, tab,
   newline, ASCII punctuation, control bytes, and every byte >= 0x80 — is a
   separator and is not part of any token.
2. A run is an **S-id** iff it matches `^S[0-9]{3,}$` in full. `S` is
   uppercase; digits are ASCII `0-9` only; at least three.
3. Each S-id run yields **exactly one** evaluation (one finding line when it
   emits), in left-to-right run order. No run is evaluated twice.
4. Zero S-id runs yields one `META_SOURCE_NO_ROW_ID` info line.

This is byte-for-byte the rule in the frozen independent oracle:
`(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])`,
`corpus/evidence/round26-registry-oracle.py:12`. It is also what the live r27
control already expects (`corpus/evidence/round27-regressions.py:149–150`
expects `S002,S002` -> 2 findings and `S001,S002` -> 1), so the per-occurrence
reading is settled: multiplicity = number of standalone run occurrences.
"No invented or duplicate occurrences" excludes (a) ids manufactured from a
non-standalone run and (b) the same run evaluated more than once, not two
distinct standalone runs of the same id.

**Equivalence claim.** For every value with no end-of-value trigger (section 4),
model T above produces the same ordered id list as the current regex loop; the
two differ only in the defect class. Ground-truth cross-check: the r26 table's
agreeing rows a1–a8, b7–b10 and the b3/b11/b12 duplicate rows are all explained
exactly by T (report §Fixtures), including the newline cases b5/b8, which show
that a newline is a separator and that the trailing `$` match is end-of-string.

## 3. Boundary classes and expected occurrence counts

`E` = expected finding lines for the value, with registry rows
`S001 mined`, `S0001 mined`, `S1234 mined` (each used-by correctly naming the
entry) and `S002 queued`; every other id has no row. Entry template:

```
source: <VALUE, or key + continuation lines>
verified-at: 2026-01-02 checked synthetic fixture
recheck: 90d

## Claim
synthetic
```

`F` = `findings=` in the anchored verdict; `D` = `drift=`; `rc` = exit.
The fixture suite must be generated into a fresh temporary directory; none of
these values exists in the repo.

Non-standalone (A) — `F=1 D=0 rc=0`, one `NO_ROW_ID` info each:

| value | runs | ids |
|---|---|---|
| `xS001` (letter left) | `xS001` | — |
| `S001x` (letter right) | `S001x` | — |
| `_S001` / `S001_` | one run | — |
| `9S001` (digit left) | `9S001` | — |
| `S001S002`, `S001_S002`, `S1234S0003`, `S001S` | one run | — |
| `S12`, `S1`, `S`, `s001` | one run | — |
| `S٠٠١` (Arabic-Indic digits) | `S` + separable bytes | — |
| `S００１` (fullwidth digits) | `S` + separable bytes | — |

Punctuation boundaries (B) — one id each, all yield
`NOT_MINED S002` x1, `F=1 D=1 rc=1`:

`(S002)` `[S002]` `,S002,` `;S002;` `S002:` `S002.` `"S002"` `-S002-`
`/S002/` `S002'` `a<TAB>S002` and `S002—note` (em dash: its UTF-8 bytes are
separators). The em-dash and any non-ASCII separator are inherited
byte-boundary semantics and the oracle agrees; they also pin C locale.

Newline boundaries (C; continuation lines are part of the value):

| # | value (lines) | ids in order | E | F/D/rc |
|---|---|---|---|---|
| C1 | `S001` + `  S002` | S001, S002 | NOT_MINED S002 x1 | 1/1/1 |
| C2 | `open S002` + `S003` (no indent) | S002, S003 | NOT_MINED S002 + ROW_MISSING S003 | 2/2/1 |
| C3 | `S001` + `S0001` | S001, S0001 | none | 0/0/0 |
| C4 | `S002` + blank + `S003` | S002 only (blank ends key) | NOT_MINED S002 x1 | 1/1/1 |
| C5 | `S001S003` + `  S001` | S001 | none | 0/0/0 |
| C6 | `x` + `S001S003` + `S001` | S001 | none | 0/0/0 |
| C7 | CRLF-written `S002` alone | S002 | NOT_MINED S002 x1 | 1/1/1 |
| C8 | `S002` + `  more` | S002 | NOT_MINED S002 x1 | 1/1/1 |
| C9 | `source:` + `S002` | S002 | NOT_MINED S002 x1 | 1/1/1 |

Trigger class (D) — glued-before-terminal; this is the r26 FRegistryIdBoundary
defect. Ground-truth base behaviour is quoted from the r26 report only for D1,
D2, D5, C5, D7, D8, D9; D10–D13 and C6 are **derived** from the same root cause
by source reading, not executed.

| # | value | expected ids | E | base (ground truth / derived) |
|---|---|---|---|---|
| D1 | `see S001S002 and S001` | S001 | none, rc0 | NOT_MINED S002 (r26 b1) |
| D2 | `see S001S003 and S001` | S001 | none, rc0 | ROW_MISSING S003 (b2) |
| D3 | `ref S002_ and S002` | S002 | NOT_MINED x1 | x2 (b11) |
| D4 | `ref S002S002 and S002` | S002 | NOT_MINED x1 | x3 (b12) |
| D5 | `x S1234S0003 y S1234` | S1234 | none, rc0 | ROW_MISSING S0003 (b6) |
| D6 | `see S001S003 and S001 ` (trailing space) | S001 | none | none (b7, non-regression) |
| D7 | `see S001S003 and S001` + `  more` | S001 | none | none (b8) |
| D8 | `(S001S003) S001` | S001 | none | none (b9) |
| D9 | `see S001_S003 and S001` | S001 | none | none (b10) |
| D10 | `recall S0001S0003 and S0001` | S0001 | none, rc0 | ROW_MISSING S0003 [INFERENCE] |
| D11 | `x S002_003 S002` | S002 | NOT_MINED x1 | x2 [INFERENCE] |
| D12 | `see S002S003 and S002` | S002 | NOT_MINED x1, no row-missing | NOT_MINED x2 + ROW_MISSING S003 x1 [INFERENCE] |
| D13 | `recall S0012S003 and S0012` | S0012 | ROW_MISSING S0012 x1, no S003 | ROW_MISSING S0012 x2 + ROW_MISSING S003 x1 [INFERENCE] |

D13 note: the maximal run is `S0012`, so the expected line names `S0012`; a
repair that kept a 3-digit prefix rule would emit `source_id=S001` (mined,
clean) and hide the reference. Assert `source_id=S0012` present and
`source_id=S003` absent.

Multiplicity (E) — pins step 3 of the model:

| # | value | E | F/D/rc |
|---|---|---|---|
| E1 | `S002 S002` | NOT_MINED S002 x2 | 2/2/1 |
| E2 | `S002, S002; S002` | NOT_MINED S002 x3 | 3/3/1 |
| E3 | `S001 S001` | none (both clean) | 0/0/0 |

E3 is deliberately a limit control: duplicate evaluation of a *clean* id is
invisible in `FINDING` lines, so it proves nothing about de-duplication.
Cardinality must be asserted on ids that emit (E1/E2) and on the verdict's
`findings=`/`drift=`.

Digit-run identity (F): `S0001` and `S1234` clean (0/0/0); `S0010`, `S0012`,
`S00100`, `S000`, `S0000` each produce exactly one
`ROW_MISSING <that id> x1` with `F=1 D=1 rc=1`; `S000` and `S0000` are
different ids (no normalization). Locale boundary (G): `éS002` yields
`NOT_MINED S002 x1` only under the C-locale byte rule (pin it); `S٤٥٦` yields
`NO_ROW_ID`.

## 4. Exact defect characterisation (why only this class moves)

The strip on line 2503 removes the shortest prefix ending in the first
*literal* occurrence of `$source_match`, not the prefix ending at the match
position. Two consequences, both observed in the r26 report:

- **Invention.** When the last match ends at end-of-string, `source_match` is
  `<sep>S<id>` with no trailing byte. An earlier run `<sep>S<id><suffix>`
  (`suffix` in `[A-Za-z0-9_]`) is not itself a match but is the first literal
  occurrence; the strip lands inside it and the remainder begins with the
  suffix, which `^` then treats as a boundary. The invented id is `S`+digits
  from the suffix (D1/D2/D5/D10/D12/D13, C5/C6).
- **Duplicate.** Same mechanism when the suffix is not `S`+3 digits: the
  remainder still ends with the real token, which is matched and emitted again
  (D3/D4/D11; r26 b3/b11/b12).

Trigger precondition: the value's final token is a standalone id and the same
`sep+id` literal occurs earlier inside a longer run. All other shapes —
trailing space (D6), continuation text (D7), different preceding char (D8/D9),
punctuation-separated ids, line-internal ids — agree today and must not change.

## 5. Validation of the live r27 control and the coverage gaps

`corpus/evidence/round27-regressions.py:142–157` (untracked, present in the
lane at read time) already encodes seven S-id cases. Against model T all seven
expectations are **correct**: `glued-before-terminal` 0, `glued-missing-
before-terminal` 0, `underscore-glued` 0, `nonstandalone-duplicate` 1,
`glued-repeat-duplicate` 1, `two-real-occurrences` 2, `adjacent-real-ids` 1;
the `ROW_MISSING` count of 0 is right for all seven. `two-real-occurrences`
confirms per-occurrence semantics.

Gaps worth adding (synthetic, same harness):

1. Punctuation boundaries B (currently only comma is covered).
2. Newline boundaries C1–C9, especially the newline-left-boundary trigger C6
   and the continuation forms C3/C4.
3. Digit-run identity F (`S0012`, `S00100`) — proves no 3-digit prefix
   truncation and no invented shorter id.
4. D10–D13 (long glue, `_digits` suffix, invented queued-prefix case,
   4-digit maximal run).
5. E1/E2 space/semicolon multiplicity, plus `findings=`/`drift=` exact counts
   in every case. The current cases assert only per-type line counts; a mis-
   paired used-by line would still exit 1 with both counted types at 0. Assert
   the verdict `findings=N drift=N` (e.g. `findings=0 drift=0`) to bind totals.

The selftest helper only checks substring presence
(`tools/research-gate.sh:6172–6173`), so the 187-case run cannot see duplicate
emission; the count control must stay in the independent script. The frozen
oracle collapses ids to a set (`round26-registry-oracle.py:122–123`) and the
differential compares sets (`round26-registry-differential.sh:215,245–247`),
so neither can detect cardinality — do not rely on them for this axis.

## 6. Suggested repair (advice to ExecRegistry)

Replace the regex/strip loop with anchored token consumption; keep every
finding branch and the used-by loop byte-identical:

```bash
local rest=$1 sid_token found_id=0 used_by matched i
local -a used_by_tokens=()
local LC_ALL=C
while [[ -n $rest ]]; do
  if [[ $rest =~ ^[^[:alnum:]_]+ ]]; then rest=${rest:${#BASH_REMATCH[0]}}; fi
  [[ -n $rest ]] || break
  [[ $rest =~ ^[[:alnum:]_]+ ]] || break
  sid_token=${BASH_REMATCH[0]}
  rest=${rest:${#sid_token}}
  [[ $sid_token =~ ^S[0-9]{3,}$ ]] || continue
  found_id=1
  ... existing ROW_MISSING / NOT_MINED / used-by / USEDBY_MISSING branches,
      s/$source_id/$sid_token/ ...
done
((found_id)) || emit_finding META_SOURCE_NO_ROW_ID info metadata "entry=$entry_base source has no S-id"
```

Requirements: `local LC_ALL=C` inside this function (byte boundaries and
`${rest:offset}` offsets); compute `rest` from `sid_token` **before** the id
test and before the inner loop rebinds `token`; do not reuse `token` for the
outer name. Delete `source_id_re`, `source_match` and line 2503. Expected
outcome: D1/D2/D5/D6/C5/C6/D10 become clean; D3/D4/D11 emit once; B/C1–C4/C7–
C9/E/F/G unchanged; population unchanged (section 7). Do not touch the sweep
classifier `^S[0-9][A-Za-z0-9_-]*$` (`:2148`) — different grammar, different
contract.

## 7. Population calibration (static census, no execution)

Applying model T to every `source:` value under `corpus/knowledge/` (same
continuation rules; my read-only Python census, not the gate):

- 8 entries have a `source:` value; per-entry id lists:
  citation-chain-fidelity-r24 [S005,S003]; claim-support-states-r24
  [S006,S007]; contextual-source-admission-r24 [S002,S004,S003];
  json-delimiter-r24 [S001,S013]; metadata-screen-r25 [S029,S033];
  reader-allocation-r26 [1]; recheck-due-r26 [4]; registry-link-r26 [2].
- Non-standalone runs containing an `S[0-9]{3,}` substring: **0**.
- Values in the end-of-value trigger class: **0**. Duplicate ids within one
  value: **0**.

Therefore the repair changes no finding on any current entry; all r24+ positive
results (`5/5`) and frozen hashes should reproduce without new exemptions.
This is a static census result, not a gate run.

## 8. Inherited limits (report, do not claim away)

- Non-ASCII letters and bytes are separators, so `éS002` counts `S002`
  (byte-boundary rule; matches the oracle). ASCII-only *tokens*, not
  Unicode-aware standalone-ness.
- An S-id inside a URL fragment or path (`.../a#S001`) is a cited id; the
  scanner has no notion of citation vs prose.
- Worst-case cost remains O(bytes x tokens) from per-iteration substring
  copies; the 8 MiB read cap bounds input, not parser work. The repair removes
  rescanning and duplicate emission but makes no linearity or resource-safety
  claim. This is the same class as the accepted FNoTrade/FOverlap debt.
- The scanner sees only the assembled `source:` value; blank lines end the
  value (C4) and `## ` ends parsing. Those are existing contracts, unchanged.
- Registry *row* ids are a separate strict rule: full trimmed cell must match
  `^S[0-9]{3,}$`, first row wins for a duplicate id
  (`tools/research-gate.sh:2432–2438`); no change derived or needed there.

## 9. Checks I did not run

No gate, selftest, regression script, differential, oracle, build, lint,
formatter, or fixture execution; no `bash` of the scanner; no network or
live-target access; nothing installed. All counts above are derived by source
reading plus the committed r26 ground-truth table, with D10–D13/C6 labelled
[INFERENCE]. The executor must confirm them by running the independent control
on the final integrated tree (0 mismatches) and, unchanged, on the isolated
base archive (nonzero, with D1/D2/D3/D4/D5 mismatching exactly as the r26
receipt documents).
