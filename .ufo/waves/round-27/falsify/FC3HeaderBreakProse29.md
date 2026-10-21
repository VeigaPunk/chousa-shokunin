# FC3HeaderBreakProse29: falsification of C3 control `header-break-prose`

Target: dd72641e574679c4f7882dd43de072b4c8892d6f (master lane, read via `git archive` into `/tmp/chousa-r27-falsify-HeaderBreakProse29`).
Gate sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` matches the assignment. `corpus/evidence/round27-regressions.py` is byte-identical to the dd72641e blob (`diff` exit 0; sha256 `5afea786…5df`).
Landed fix under attack: prose-branch reset in `metadata_registry_load`, `tools/research-gate.sh:2432-2435`.
Control under attack: `corpus/evidence/round27-regressions.py:135` (the fixture) and the `tables` loop at `:144-149`.
Contract: `corpus/evidence/round27-claims.md:15`.

## Verdict

- **Control `header-break-prose`: FALSIFIED as a sufficient guard.** It is non-vacuous against the base defect (the stale-column leak) and against a columns-only revert. It is vacuous against a same-class regression in which the header candidate survives the prose line. The control passes that regression for the wrong reason: an intervening table-ish row clears the candidate.
- **Landed production fix (prose-branch reset): HOLDS** on every probe: 8,585 enumerated synthetic fixtures, 13 hand-picked near inputs, and the 10 C3 suite tables. I found no counterexample in the header-break class.
- Axes:
  - *operability*: this class gets exit 2 with no verdict line, as designed.
  - *freshness*: the C3 tables are wall-clock independent. Without `--as-of` the verifier computes no due/freshness (documented at gate usage line 321). Output was identical with `CHOUSA_NOW_EPOCH=2026-03-01` and with the system clock.
  - *calibration*: the control-vacuity finding above, plus inherited first-table-only and first-row-wins semantics (section 4). These are not C3 regressions.

## 1. Is the expectation derived from the contract, independent of gate code?

Yes, with one brittleness caveat.

- The fixture is hand-written: `| id | status | used-by |` / `prose` / `| a | b | c |` / `|---|---|---|` / S001 row. Expected: exit 2, the `metadata registry has no table` diagnostic, and zero `^RESEARCH_GATE: ` lines.
- The rule comes from the contract: "Require fresh named headers after breaks". A non-table line ends the header; the following anonymous table has no fresh header, so no table exists. Exit 2 is the gate's declared setup/usage code, and it matches the base's existing no-table handling.
- I wrote an independent contract oracle (`drv/enum_header_breaks.py`) without reading gate predicates. It reproduces the expectations of the 10 C3 suite tables that map onto its alphabet.
- Caveat: the control binds the gate's diagnostic wording, so a text change fails it without any logic change.

## 2. Revert/mutate the targeted fix: does the control fail for the intended reason?

Sandbox-only mutants of the landed gate, produced by `drv/make_mutants.py`. Each changes one anchor in the prose branch unless noted.

| variant | change | header-break-prose | suite C3 tables (10) | near (13) | enum ≤4 (4680) |
|---|---|---|---|---|---|
| BASE-64eec5d (full base gate) | whole base file | FAIL: exit 0, stale table accepted | 6 FAIL | 2 FAIL | not run |
| M1 | prose branch = base (keeps columns) | FAIL: exit 0 != 2, no diagnostic; stdout `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)` | 4 FAIL (header-break-blank, header-break-prose, reorder-clean, reorder-queued) | — | not run |
| M3 | prose keeps stale columns | FAIL, same signature as M1 | 4 FAIL (same set) | — | not run |
| M2 | prose keeps candidate, resets width | PASS | 0 | 0 | 0 mismatches (equivalent) |
| M4 | prose keeps width, resets candidate | PASS | 0 | 0 | 0 mismatches (equivalent) |
| **M7** | prose keeps candidate and width, resets columns only | **PASS (vacuous)** | **0 FAIL (suite 10/10 pass)** | 4 FAIL | **38 mismatches** |
| M5 | candidate-fail branch keeps columns | not exercised | **0 FAIL (suite 10/10 pass)** | 2 FAIL | **84 mismatches** |
| M6 | else branch keeps columns | not exercised | **0 FAIL (suite 10/10 pass)** | 1 FAIL | not in alphabet |

Notes:
- M1 and M3 fail the control for the intended reason. The stale column indices let the post-break row `| a | b | c |` look like a header, and the delimiter then makes a table. Exit 0 with a CLEAN verdict is the leak itself, not a parse or setup error.
- M2 and M4 are equivalent. Either reset alone suffices: width 0 makes every later separator check fail, and candidate 0 skips the check.
- M7 passes the control because `| a | b | c |` clears the surviving candidate through the candidate-fail branch. The control therefore never tests a delimiter directly after a non-table line.

## 3. Counterexamples

### CE1: control vacuous for the candidate-flag leak (M7). Minimal, same class.

Input, with entry `source: S001`, `verified-at: 2026-01-02`, `recheck: 90d`:
```
| id | status | used-by |
prose
|---|---|---|
| S001 | mined | corpus/knowledge/entry.md |
```
- Expected: exit 2, "no table". Landed gate: exit 2 (correct).
- M7: exit 1, `FINDING META_SOURCE_ROW_MISSING`, `RESEARCH_GATE: DRIFT`. The pre-break header was accepted across the prose line.
- Suite `header-break-prose` (with the `| a | b | c |` row) passes under M7. The blank analogue (`header-break-blank`) also passes under M7.
- Other M7 misses from the near set: whitespace-only break, single-pipe break `|`, and CRLF-blank break. Each is exit 1 where exit 2 is expected.

Proposed additional controls (not applied; the author decides): direct-delimiter variants of prose and blank, with expected exit 2 and the same diagnostic.

### CE2: no control for the candidate-fail path (M5)

- `| id | status | used-by |` / `| S001 | mined | corpus/knowledge/entry.md |` / `|---|---|---|` → landed exit 2; M5 exit 1 (table accepted).
- `| id | status | used-by |` / `note | a | b` / `|---|---|---|` / S001 row → landed exit 2; M5 exit 0 (accepted).
- All 10 suite tables pass under M5.

### CE3: no control for the partial-header else-branch (M6)

- `| id | status | note |` / `| x | used-by | y |` / `|---|---|---|` / S001 row → landed exit 2; M6 exit 1 (accepted with stale positions).
- All 10 suite tables pass under M6.

### Landed gate: no counterexample found in the class

- Exhaustive over alphabet {H, D, D2, R, P, B, X, F}, length ≤4: 4680 fixtures, 0 mismatches against the oracle.
- Exhaustive over alphabet {H, D, P, X, R}, length ≤5: 3905 fixtures, 0 mismatches.
- Near inputs, 13/13 as the contract requires. These include fresh header after prose (exit 0), blank-then-header (exit 0), two-pipe prose before header (exit 0), CRLF/whitespace/single-pipe breaks (exit 2), width mismatch then matching delimiter (exit 2), and partial header with used-by on the next line (exit 2).

## 4. Inherited observations (identical at base; not C3 regressions)

- **I1, first table only.** After the first table, the first non-table line ends parsing, so a later fresh table is never read. `H, D, R(S001 mined), prose, H, D, R(S001 queued)` gives CLEAN exit 0 on the target and on BASE. Whether multi-table registries are intended is not stated by the contract. If they are, this is a calibration hole.
- **I2, duplicate rows first-wins.** `H, D, R(mined), R(queued)` gives CLEAN exit 0 on target and BASE; the reverse order gives DRIFT exit 1.
- **I3, GFM-valid one-dash delimiters refused.** `|-|-|-|` and `|:-|-:|:-:|` give exit 2 "no table" on the target. The regex `^:?-{3,}:?$` is unchanged from base.
- **Freshness, documented opt-in.** Default `verify-metadata` never evaluates recheck overdue. A `verified-at: 2026-01-02` / `recheck: 90d` entry is CLEAN at the current date unless `--as-of` is given (usage line 321).

## 5. Commands and results (all sandbox, synthetic)

- `git archive dd72641e… | tar -x -C …` → exit 0.
- Gate sha256 → matches the assignment. Regressions blob `diff` → exit 0.
- `python3 drv/run_c3_tables.py tools/research-gate.sh --near` → `SUMMARY pass=23 fail=0`.
- Same without `--near` → `pass=10 fail=0`. Mutant suite-only results are in the table above.
- `drv/run_c3_tables.py mut/M1…` with `--show` on `header-break-prose` → exit-0 CLEAN signature quoted above.
- `drv/enum_header_breaks.py tools/research-gate.sh 4` → 4680 total, 0 mismatches (56.5 s).
- `drv/enum_header_breaks.py tools/research-gate.sh 5 H,D,P,X,R` → 3905 total, 0 mismatches (48.2 s).
- Same enumerator on M7 (38), M5 (84), M2 (0), M4 (0), each length ≤4.
- Oracle sanity: agreed on valid-table, header-break-blank/prose, delimiter-too-short, near-prose-then-direct-delim, near-fresh-header-after-prose, near-fresh-header-no-delim, near-blank-then-header, near-two-pipe-prose-then-header, near-width-mismatch-then-matching-delim.
- The driver and enumerator exit 0 regardless of mismatches; read the SUMMARY/ENUM line.

Scope: I did not run `--selftest` or the whole regression script. The driver extracted the `tables` list from the script by AST and ran only those 10 fixtures.

## 6. Limits

- Synthetic fixtures only, in the sandbox. No network, no host files, no live processes.
- The enumeration alphabet lacks 4-column headers, escaped pipes, Unicode, and CR-only files. Whitespace-only, single-pipe, and partial-with-used-by lines are covered by hand-picked near inputs only.
- The oracle follows the gate's declared table grammar: at least two pipes is a table line, a delimiter has at least three dashes, and header names are exact. The contract does not independently fix that grammar.
- The "equivalent" labels for M2 and M4 are backed by exhaustive runs only within the enumerated alphabet.
- I did not evaluate the sibling `header-break-blank` item beyond the shared M7 result.

## 7. Tooling

No installs or updates. Used bash and python3 3.14.8, both already present.

## 8. Author-lane advice (not an outside admission)

1. Add direct-delimiter controls: `header-break-prose-direct` = header, `prose`, `|---|---|---|`, S001 row, expected exit 2. Add a blank analogue. Both fail under M7.
2. Add a `candidate-fail` control: header, `note | a | b`, delimiter, S001 row, expected exit 2 (fails under M5). Add a partial-header control: `| id | status | note |`, `| x | used-by | y |`, delimiter, S001 row, expected exit 2 (fails under M6).
3. Decide and document I1 (later tables) and I2 (duplicate rows). Currently both fail silently toward CLEAN.
4. The prose branch carries two redundant resets (candidate and width). Either is sufficient. Keep one only if you want the code smaller; this is optional.

## Clarifications (appended after writing)

- Section 1: I had read the gate's registry parser before writing the oracle. The oracle's independence is of construction (rules written from the contract and the declared table grammar), not of prior ignorance.
- Verdict, freshness: the two `verify-metadata` runs (`CHOUSA_NOW_EPOCH=2026-03-01` and the system clock) differed only in the `ts=` header field. The META and verdict lines were identical.
