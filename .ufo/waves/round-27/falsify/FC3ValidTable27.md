# FC3ValidTable27 — falsify C3 control `valid-table` at dd72641e

- **Item attacked:** `corpus/evidence/round27-regressions.py:133` `('valid-table', header + row, 0, None)`.
- **Target:** `dd72641e574679c4f7882dd43de072b4c8892d6f`; `tools/research-gate.sh` sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (re-measured in sandbox).
- **Sandbox:** `/tmp/chousa-r27-falsify-FC3ValidTable27`, made with `git archive dd72641e | tar -x`. Base gate `64eec5d4:tools/research-gate.sh` (sha256 `c2c813f1…abc6`) was copied there as `base-gate.sh`. No lane files were edited except this report.
- **Verdict: FALSIFIED (partial).** The control itself is sound and green, and it does kill the over-rejection mutant it guards against. But the C3 width-equality fix it is meant to bless regresses on a nearby GFM-valid table that base accepted, and the control family is vacuous against at least one plausible width mutant.

## (1) Is the expectation independent of gate code?

Yes.
- The fixture is hand-written: a 3×3 table with outer pipes and S001 `mined`, with used-by exactly `corpus/knowledge/entry.md`. It expects exit 0 and exactly one `^RESEARCH_GATE: ` record.
- This follows from the claims text (`round27-claims.md:15`: "Existing well-formed registry behavior and exact used-by rules remain") and does not read any gate code sets.
- An independent GFM oracle agrees. `markdown-it-py` 4.2.0 (`MarkdownIt('commonmark').enable('table')`) returns a width-3 table with S001 = (`mined`, `corpus/knowledge/entry.md`).

**Weakness:** the control asserts only the exit code and the verdict count. It does not assert `findings=0` or `^FINDING ` = 0 (`composed-current-registry` does), and it does not prove the parsed row was consulted. Mutant M5 below (`metadata_registry_check_source` returns immediately) still passes it. On its own, it is satisfied by any gate that finds some table and ignores it.

## (2) Mutation evidence

Runner: `c3tables.py` execs only the verbatim regressions-script setup and the `tables` list/loop (lines 1–68 and 130–150). It does not run the whole script. Each command was `timeout 120 python3 c3tables.py <gate>`, and all exited 0.

| gate | valid-table | other table controls |
|---|---|---|
| landed | rc0 ok | 10/10 ok |
| base (full C3 revert) | rc0 ok | 6 MISMATCH: break-blank, break-prose, reorder-clean, reorder-queued, too-short, too-long |
| M1: delete `header_width=${#cells[@]}` (`:2490`) | **rc2 MISMATCH** (`exit 2 != 0; count ^RESEARCH_GATE: 0 != 1`) | 6 positives fail the same way |
| M2: width = count of raw `\|` characters on both lines | rc0 ok | **10/10 ok: survives** |
| M3: delete the width comparison (`:2466`) | rc0 ok | too-short and too-long MISMATCH |
| M5: `return 0` at the top of `metadata_registry_check_source` | rc0 ok | only reorder-queued MISMATCH |
| M7: delete the whole non-table-line reset (`:2433-2435`, including `header_candidate=0`) | rc0 ok | **10/10 ok: survives** |

- **M1:** `valid-table` fails for the intended reason. It goes to exit 2 with "metadata registry has no table…", which is an over-rejection of a valid table, not a parse or setup error.
- **Full revert:** `valid-table` passes, as expected for a positive or no-trade control. The revert is detected by the negative siblings, not by this control.
- **M2:** this mutant is wrong on GFM-valid tables, yet nothing kills it. On the landed gate, all five mixed-outer-pipe shapes below exit 0. Under M2 they all exit 2:
  - `| id | status | used-by |` + `---|---|---`
  - `id | status | used-by` + `|---|---|---|`
  - lead-only pipe on the header
  - lead-only pipe on the delimiter
  - trail-only pipe on the delimiter

  The oracle reports a valid width-3 table for all five. No r27 control and no selftest registry fixture mixes outer-pipe styles; every fixture has outer pipes on both lines, or neither. So M2 probably also survives `--selftest` [INFERENCE: not run, per lane bounds; based on the fixture shapes at `research-gate.sh:6215-6476`].
- **M7:** this mutant survives because the `header-break-blank` fixture puts a non-delimiter pipe row (`| a | b | c |`) after the break, and the candidate branch resets state there anyway. Killing input: `| id | status | used-by |`, then a blank line, then `|---|---|---|`, then `| S001 | mined | corpus/knowledge/entry.md |`. Landed and base both exit 2, which is correct (the oracle finds 0 tables). M7 exits 0 with `RESEARCH_GATE: CLEAN`. Peer `FC3HeaderBreakBlank28-11` was told. That peer independently confirmed the masking with a narrower one-line mutant that skips only the empty-line reset (`[[ -z $line ]] && continue`). Their mutant also survives `header-break-blank` and is killed once the `a/b/c` row is removed. See `FC3HeaderBreakBlank28.md`.

## (3) Nearby counterexamples

Probes: `probe.py` (gate) and `oracle.py` (markdown-it). All fixtures are synthetic and live under `/tmp`.

### A. Regression introduced by the width fix: escaped pipe in the header (over-rejection)

```text
| id | status | used-by | a \| b |
|---|---|---|---|
| S001 | mined | corpus/knowledge/entry.md | x |
```

- GFM oracle: one table, header `['id','status','used-by','a | b']`, width 4, S001 `mined`, so CLEAN is expected.
- Base gate: rc 0, `RESEARCH_GATE: CLEAN (… findings=0 drift=0)`.
- Landed gate: **rc 2**, `research-gate: metadata registry has no table with id, status, and used-by columns`, with 0 verdicts.

The cause is that `IFS='|' read -a` splits on `\|`, so the header counts 5 cells against 4 delimiter cells. Base accepted this registry and landed refuses it. That violates "existing well-formed registry behavior … remain", and it is an operability and calibration regression. Today's `corpus/SOURCES.md` contains 0 `\|`, so the live corpus is unaffected.

### B. Same mechanism, opposite direction (over-acceptance)

The same header with a 5-cell delimiter `|---|---|---|---|---|`:
- GFM oracle: **0 tables**, so exit 2 is expected.
- Landed and base: both accept the table and process rows (rc 1 with a queued row; it would be rc 0 with `mined`).

So "matching header/delimiter widths" is measured in `|`-split fields, not cells, whenever `\|` appears.

### C. Inherited divergences, not regressions

Base and landed behave identically on these; they are reported, not counted against r27.

| input | GFM oracle | landed gate |
|---|---|---|
| `\|-\|-\|-\|` and `\|:-\|-:\|:-:\|` delimiters | valid table | rc 2 (regex needs `-{3,}`) |
| row after a pipe-less line inside a table | the line is a table row; S001 found | stops at the line; `META_SOURCE_ROW_MISSING`, rc 1 |
| registry header appearing as a body row of an earlier `a\|b\|c` table | no registry table | rc 0 CLEAN |
| table inside a ```` ``` ```` fence | no table | rc 0 CLEAN |

### D. Landed behavior that is now correct where base was wrong

These are not counterexamples, just behavior changes:
- `| id | status | used-by ||` (4 cells) over a 3-cell delimiter: the oracle finds no table, landed exits 2, base exited 0.
- A UTF-8 BOM before the header: the oracle finds no table, landed exits 2, base exited 1.

## Smallest safe corrections (author-lane advice)

1. **Gate.** Split cells on unescaped `|` only (treat `\|` as cell content) for the width comparison, and preferably for every cell read. Add two controls: the escaped-pipe 4/4 table expecting rc 0, and the 4/5 table expecting rc 2.
2. **Controls.** Add a mixed-outer-pipe positive control (for example, header with outer pipes over `---|---|---`, expecting rc 0) to kill M2. Add the headerless-delimiter-after-blank negative control to kill M7.
3. **`valid-table`.** Also assert `^FINDING ` count 0 (or `findings=0`), and pair it with a `queued` twin expecting `META_SOURCE_NOT_MINED`. That proves the parsed row is consulted, which kills M5 inside the control itself.

## Commands and exit codes

- `git archive dd72641e… | tar -x -C /tmp/chousa-r27-falsify-FC3ValidTable27`: 0. Running `sha256sum tools/research-gate.sh` gave `ca39d14d…2f84`.
- `timeout 120 python3 probe.py tools/research-gate.sh`: 0 (29 cases). The same probe on `base-gate.sh`: 0. `diff base.txt landed.txt`: 1, with three differing cases: escaped-pipe-header, empty-trailing-hdr-vs-3, bom-header.
- `timeout 120 uv run --offline --no-project --with markdown-it-py==4.2.0 python oracle.py`: 0.
- `timeout 120 python3 c3tables.py {landed, base, M1, M2, M3, M5, M7}`: 0 each; results are in the table above.
- `timeout 60 python3 probe.py mut/M2.sh <mixed cases>`: 0. Results: valid-table rc 0; all five mixed shapes rc 2.
- Direct `bash <gate> verify-metadata … --registry hb.md` (headerless delimiter after a blank line): landed rc 2, M7 rc 0, base rc 2.
- Direct `--registry ep4.md` (escaped pipe, 4/4): landed rc 2, base rc 0. `--registry ep5.md` (4/5): landed rc 1, base rc 1, oracle 0 tables.

## Limits and tooling

- Full `--selftest` and the whole regression script were not run (L1 owns those), so the M2 and M7 selftest survival is inferred from fixture shapes only.
- markdown-it-py is a GFM-like oracle, not cmark-gfm. Its `str.strip()` also trims NBSP, so NBSP cases were excluded.
- **Tooling:** nothing installed. markdown-it-py 4.2.0 came from the existing uv cache through an ephemeral offline env: `uv run --offline --with`, channel uv cache, used as an independent GFM oracle. No network, `/proc` inspection, or host-secret access.
