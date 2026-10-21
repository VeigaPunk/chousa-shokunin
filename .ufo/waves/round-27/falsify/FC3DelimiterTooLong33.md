# FC3DelimiterTooLong33 — falsify C3 control `delimiter-too-long` @ dd72641e

Author-lane advice, not outside admission.

- Sandbox: `/tmp/chousa-r27-falsify-FC3DelimiterTooLong33`, made with `git archive dd72641e574679c4f7882dd43de072b4c8892d6f | tar -x`.
- Gate sha256: `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84`. This matches the assignment.
- Target: `corpus/evidence/round27-regressions.py:139`, which feeds header `| id | status | used-by |` with delimiter `|---|---|---|---|` and expects exit 2, `metadata registry has no table`, and 0 `^RESEARCH_GATE: ` records.
- Production fix under test is the width check `tools/research-gate.sh:2466`, `(( ${#cells[@]} == header_width )) || is_separator=0`, plus the `header_width` bookkeeping at `:2435/2479/2490/2493`. The base 64eec5d had no width check.
- Tools installed: none.

## Verdict

**HOLDS** for the control itself: it is non-vacuous and kills the targeted revert. It also has two limits:

- **Control-class gap.** A plausible width mutant passes every persisted C3 table control but rejects valid tables.
- **Inherited grammar divergence.** Under a GFM cell grammar the landed gate accepts a too-long delimiter, giving CLEAN instead of exit 2. The claim names no cell grammar, so I classify this as an inherited parser limitation the claim says to report. It is not a falsification of the repair.

## (1) Is the expectation independent of the gate code?

Partly.

- **Exit 2 with no verdict.** This follows from the C3 text ("Require … matching header/delimiter widths"): the pair is not a header, so there is no table. That the no-table outcome is a usage error (exit 2) is an existing gate convention (`die_usage`). The contract does not state it.
- **Required substring.** `'metadata registry has no table'` is copied from the gate's `die_usage` string at `:2496`. It is not derived from the contract.
- **Overlap with the selftest.** The fixture has the same shape and the same diagnostic as the gate's own selftest case `metadata-registry-width-long` (`tools/research-gate.sh:6425-6432`). It duplicates the author's selftest rather than adding independent coverage.

## (2) Mutation evidence

Harness: `probe.py` in the sandbox. It copies the control's fixture, environment, invocation and oracle verbatim, and adds nearby inputs. Each run took about 0.4 s, exit 0. I did not run the full suite or the selftest.

| gate | sha256[:12] | control `delimiter-too-long` | `delimiter-too-short` |
|---|---|---|---|
| landed | ca39d14db907 | OK, rc 2 | OK, rc 2 |
| m0: delete `:2466` (base-equivalent) | 5f8d29a03dd0 | **FAIL**, rc 0 `RESEARCH_GATE: CLEAN` | FAIL, rc 0 |
| m1: `==` changed to `>=` | 1060e1b8a87e | **FAIL**, rc 0 CLEAN | OK, rc 2 |
| m2: `==` changed to `<=` | 76f99e220707 | OK, rc 2 | FAIL, rc 0 |
| m3: drop `header_width=0` on non-table line | b6213a5531f9 | OK | OK (equivalent mutant: the value is re-set before use) |

Under m0 and m1 the control fails for the intended reason. The header and delimiter are accepted as a table, row S001 counts as mined, and the run ends clean with exit 0. It is not a parse or setup error. The control also kills m1, which `delimiter-too-short` does not, so it is a necessary member of the pair.

Non-vacuity: `reorder-clean` (a 4-column header with a 4-column delimiter, exit 0) guards against "reject any delimiter longer than 3 cells". My probe case "valid 4-col header 4-col delim" also passes on the landed gate.

## (3) Nearby counterexamples

### A. Control-class gap (calibration, operability)

Mutant m4 (`m4-rawpipes.sh`, ae45b2b37b04) compares raw `|` counts on the header and delimiter lines instead of cell counts after stripping the outer pipes. It passes all 10 persisted C3 table controls (valid, header-break-blank, header-break-prose, reorder-clean, reorder shapes, too-short, too-long, no-outer-pipes, crlf, aligned).

It wrongly refuses with exit 2 on these valid tables, all of which the landed gate accepts with rc 0:

```
id | status | used-by
|---|---|---|
| S001 | mined | corpus/knowledge/entry.md |
```

The same happens with a piped header over a bare delimiter (`| id | status | used-by |` / `---|---|---`) and with a lead-pipe-only header (`| id | status | used-by` / `|---|---|---|`).

Neither the suite nor the gate selftest has a table whose header and delimiter differ in outer pipes. There are zero selftest fixture lines without an outer pipe. The build scout ScoutRegistryWidths was explicitly scoped to "extra/missing outer pipes", yet no persisted control pins it.

**Smallest safe correction:** add one control, `valid-mixed-outer-pipes` (`'id | status | used-by\n|---|---|---|\n' + row`, rc 0). Optionally also add a mixed-pipe too-long control (`'id | status | used-by\n|---|---|---|---|\n' + row`, rc 2).

### B. Escaped-pipe width: false accept and false refusal (calibration; inherited grammar)

The gate splits on every `|` (`:2443`) and ignores the GFM `\|` escape.

**False accept** (a too-long delimiter under GFM gives CLEAN):

```
| id | status | x \| used-by |
|---|---|---|---|
| S001 | mined | x | corpus/knowledge/entry.md |
```

- GFM header has 3 cells (`id`, `status`, `x | used-by`), so a 4-cell delimiter means no table; the expected result is exit 2.
- The landed gate sees 4 cells including `used-by`, accepts the table, and returns rc 0 `RESEARCH_GATE: CLEAN`.

**False refusal:** header `| id | status | used-by | a \| b |` over `|---|---|---|---|`. GFM gives 4 = 4, a valid table. The landed gate counts 5 ≠ 4 and returns rc 2 "no table".

Both are [INFERENCE] against the GFM spec. No GFM oracle is installed locally and network use is forbidden, so this was not checked against a GFM implementation. The behaviour is inherited from base cell splitting, which neither m0 nor the claims change.

**Correction if the contract means GFM:** split on unescaped `|` only, and add these two fixtures. Otherwise, state the "`|` always separates" grammar in the C3 limitations.

### C. Delimiter-cell grammar (inherited, outside the width claim)

`|-|-|-|` is a valid GFM delimiter of width 3. The gate's `^:?-{3,}:?$` (`:2469`, the same as base) refuses it with rc 2. Report it as an inherited grammar limit.

## Further holds on the landed gate (all OK, rc as expected)

These too-long variants all return rc 2:
- aligned `:---:` (+1 cell)
- +5 cells
- no outer pipes
- bare header with piped delimiter
- trailing empty delimiter cell
- CRLF

A too-long pair followed by a fresh valid table goes to the fresh table: rc 1 when the row is `queued`, rc 0 when `mined`. A header with a trailing empty cell over a 4-cell delimiter returns rc 0.

## Limits

- Only the `verify-metadata --registry` path was exercised, and only with synthetic temporary fixtures.
- No full selftest or regression run.
- GFM claims are spec-based [INFERENCE] and were not run against a GFM parser.
- Mutants exist only in the sandbox; no lane files were edited.

Commands: `python3 probe.py <gate>` for each of `tools/research-gate.sh`, `m0-revert.sh`, `m1-ge.sh`, `m2-le.sh`, `m3-noreset.sh` and `m4-rawpipes.sh`. Each ran with `timeout 120` and exited 0, and the probe prints per-case OK or MISS.
