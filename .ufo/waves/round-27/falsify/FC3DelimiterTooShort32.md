# FC3DelimiterTooShort32 — falsify C3 control `delimiter-too-short`

Lane: chousa-shokunin · round 27 attempt1 · landed revision `dd72641e574679c4f7882dd43de072b4c8892d6f` · gate `tools/research-gate.sh` sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (matches the assignment).
Comparison: base `64eec5d` gate sha256 `c2c813f1b425bc4e…` (extracted with `git show`).
Sandbox: `/tmp/chousa-r27-falsify-FC3DelimiterTooShort32` (`git archive dd72641e | tar -x`). No lane production, git, index, fleet, or sibling file was touched. Nothing was committed.

## Verdict

**FALSIFIED — the C3 delimiter-width control family is vacuous against a same-class mutant. The control itself is correctly derived and discriminates width equality. No counterexample to the landed gate was found on the width class.**

- Q1, expectation derived from the contract: **HOLDS**.
- Q2, reverting the targeted fix makes the control fail for the intended reason: **HOLDS** (m1–m4).
- Q3, nearby input where the landed gate is wrong or the control is vacuous: **FALSIFIED for the control suite** (CE-1, CE-2). The landed gate is correct on every width-class neighbor probed. Its only deltas from base are contract-undefined escape and BOM cases (CE-3 to CE-5), reported as residual risk.

Axes: calibration is the primary axis and is under-calibrated (three same-class mutants escape the delimiter controls, one escapes all 10 table controls). Operability is sound: each run is deterministic and about 18 ms. One caveat: the reason substring copies gate text (CE-0). Freshness is not affected.

## 0. Control under attack

`corpus/evidence/round27-regressions.py:138`
`('delimiter-too-short', '| id | status | used-by |\n|---|---|\n' + row, 2, None)`
`:139` is `delimiter-too-long` (4-cell delimiter). The row is `| S001 | mined | corpus/knowledge/entry.md |`.
Expectation: exit 2, no `RESEARCH_GATE:` verdict line, and the substring `metadata registry has no table`.

## 1. Q1 — is the expectation contract-derived and independent of gate code?

Yes. Every value is a literal in the script:
- C3 (`corpus/evidence/round27-claims.md:15`) requires "matching header/delimiter widths". A 2-cell delimiter under a 3-cell header therefore does not establish a header, so no table exists.
- The gate's declared exit contract (`tools/research-gate.sh:386`, `Exit: 0 CLEAN | 1 DRIFT | 2 setup/usage`) and `die_usage` (`:390`) make rc 2 the only outcome a no-table registry can produce.
- Lesson R27-M4 (`corpus/lessons/round-27.md:38`) states the contract as "fresh columns after breaks and matching delimiter width", with S042 at `:59`.

Caveat (CE-0, operability): the reason substring is a copy of the gate's message at `tools/research-gate.sh:2496`. A wording change would fail the control with no semantic change. The control also pairs with `valid-table`, which differs only in the delimiter row, so it isolates width.

## 2. Q2 — mutation: does the control fail for the intended reason?

Mutants were built in the sandbox from landed with `diff`-verified single-line changes:
- m1: line 2466 `(( ${#cells[@]} == header_width )) || is_separator=0` → `true` (width check removed)
- m2: `==` → `<=`; m3: `==` → `>=`; m4: → `header_width=${#cells[@]}` (width taken from the delimiter)
- m5: → `(( ${#cells[@]} == 3 ))` (hardcoded width); m7: → `(( ${#cells[@]} == usedby_col + 1 ))`
- m6: lines 2477–2479 (`header_candidate=0; id_col=-1…; header_width=0`) → `continue` (a rejected delimiter leaves the header armed)

m1 on `delimiter-too-short`: `exit 0 != 2`, `missing 'metadata registry has no table'`, `count RESEARCH_GATE: 1 != 0`. The gate accepts the mismatched table and emits a clean verdict. This is the intended failure, not a parse or setup error: `bash -n` exits 0 for every mutant, and `valid-table`, `valid-aligned`, `valid-crlf`, and `valid-no-outer-pipes` still pass under m1.

Outcome matrix over the 10 registry-table tuples the script declares (lines 137–142 family), driver `probe/c3_delim_probe.py`:

| gate variant | control FAILs (of 10) | notes |
|---|---|---|
| landed `dd72641e` | none (10/10 PASS) | |
| base `64eec5d` | header-break-blank, header-break-prose, reorder-clean, reorder-queued, delimiter-too-short, delimiter-too-long | base accepts a 2-cell delimiter, a mismatched 4/3 pair, and a bad-then-good delimiter pair |
| m1 check removed | delimiter-too-short, delimiter-too-long | intended reason (CE-0 detail above) |
| m2 `<=` | delimiter-too-short | too-long still rejected (4 > 3) |
| m3 `>=` | delimiter-too-long | too-short still rejected (2 < 3) |
| m4 width from delimiter | delimiter-too-short, delimiter-too-long | |
| m5 `== 3` | reorder-clean, reorder-queued; **both delimiter controls PASS** | vacuous |
| m7 `== usedby_col+1` | reorder-queued; **both delimiter controls PASS** | vacuous; used-by-last shapes pass |
| m6 failed delimiter keeps header armed | **none; all 10 PASS, both delimiter controls included** | vacuous; caught only by neighbors (CE-1) |

Mutation evidence: reverting the width check fails the control for the intended reason (m1–m4). The reset of the header after a failed delimiter (m6) is not pinned by any control.

## 3. Q3 — counterexamples (exact bytes)

All runs use the script's `run()` semantics: `LC_ALL=C`, `CHOUSA_*` removed, `verify-metadata <entry> --root <root> --registry <registry>`, one fresh synthetic root per case, and the entry `source: S001 / verified-at: 2026-01-02 … / recheck: 90d`.

**CE-1 (decisive; control vacuity, m6).** Minimal registry:
```
| id | status | used-by |
|---|---|
|---|---|---|
| S001 | mined | corpus/knowledge/entry.md |
```
Landed: exit 2, `metadata registry has no table…`. Correct, since the 2-cell delimiter removes the header. m6: exit 0 with a clean verdict, so a stale header is accepted. No control contains a delimiter followed by another delimiter, so none catches this. The 4/3/4 variant (`| id | status | used-by | x |` / `|---|---|---|` / `|---|---|---|---|` / row) also gives landed exit 2 and m6 exit 0. This is the same stale-state class as r26 FRegistryHeaderless (lesson S042: "a non-pipe line sets header_candidate=0; continue but does not reset id_col/status_col/usedby_col"), but triggered by a table-shaped break.

**CE-2 (width-generality vacuity).** Both delimiter controls use header width 3 only. m5 is caught only by `reorder-clean`/`reorder-queued`, and m7 only by `reorder-queued`, whose intent is reordering and the queued finding, not width. Neighbor the landed gate accepts (rc 0, clean verdict), with m5 and m7 both rejecting (rc 2):
```
| id | status | used-by | note |
|---|---|---|---|
| S001 | mined | corpus/knowledge/entry.md | x |
```
Also accepted by landed and rejected by m5 and m7: the 5-column middle used-by shape `| x | id | status | used-by | y |` / `|---|---|---|---|---|` / `| a | S001 | mined | corpus/knowledge/entry.md | b |`.

**CE-3 (contract-undefined; base→landed change, escaped pipe in a header cell).**
```
| id | status | note\|x | used-by |
|---|---|---|---|
| S001 | mined | a\|b | corpus/knowledge/entry.md |
```
Landed: exit 2, no table. Base: exit 0, clean. Under GFM this is a valid 4-cell table where `\|` is content [INFERENCE: GFM from memory; no network to fetch the spec]. The gate has no escape grammar. Its docs define none, and `corpus/SOURCES.md` contains zero `\|`. Under the gate's naive pipe-splitting, the 5-vs-4 width mismatch is a legitimate rejection, so this is not counted as a C3 violation. It is reported as a residual contract question.

**CE-4 (pre-existing; base = landed; escaped pipe in a data row).**
```
| id | status | note | used-by |
|---|---|---|---|
| S001 | mined | a\|corpus/knowledge/entry.md |
```
Landed and base both exit 0, clean. Under GFM the row has 3 cells, so used-by is empty and the gate should report `META_SOURCE_USEDBY_MISSING`. The naive split matches the path into the used-by slot instead. This is a false clean, pre-existing, not introduced by C3, and contract-undefined.

**CE-5 (pre-existing; BOM before the first header).** Landed: exit 2, no table. Base: exit 1 with a false `META_SOURCE_ROW_MISSING`, since the BOM occupies cell 0 and shifts the bindings. A case-insensitive search of the landed gate for `feff|BOM|byte.order` found no matches, so the registry reader has no BOM handling. Neither revision is correct here, and this is not a width defect.

**CE-6 (pre-existing).** `| id | status | used-by |` / `|--|--|--|` plus the row: exit 2 in both base and landed. The `^:?-{3,}:?$` rule rejects one- and two-hyphen cells. GFM accepts one or more hyphens [INFERENCE]. Not a C3 wording violation.

**Landed correct (base wrong, confirming the fix):** `header-trailing-empty-mismatch` (`| id | status | used-by | |` over `|---|---|---|`) is accepted by base and rejected by landed. `bad-then-good-delim 3-2-3` and `4-3-4` are accepted by base and rejected by landed. `prose-break-then-valid` is misbound by base (exit 1, false finding) and correct in landed (exit 0).

## 4. Real-data check

`bash tools/research-gate.sh verify-metadata corpus/knowledge/registry-link-r26.md --root . --registry corpus/SOURCES.md` (sandbox copy, landed) → exit 0, `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)`. The production registry's header and delimiter are both 11 cells, `used-by` last, with zero `\|`. Landed width handles it.

## 5. Recommended control additions (author-lane advice; not applied)

These three inputs are the probe fixtures above, run against landed and the mutants. Each expectation follows the script's conventions (`RESEARCH_GATE:` count 0 on rc 2, 1 on rc 0):

```
('delimiter-bad-then-good-delimiter', '| id | status | used-by |\n|---|---|\n|---|---|---|\n' + row, 2, None),
('delimiter-usedby-trailing-column', '| id | status | used-by | note |\n|---|---|---|---|\n| S001 | mined | ' + relative + ' | x |\n', 0, None),
('delimiter-five-columns-usedby-middle', '| x | id | status | used-by | y |\n|---|---|---|---|---|\n| a | S001 | mined | ' + relative + ' | b |\n', 0, None),
```

Observed: the first gives landed rc 2 and m6 rc 0. The second and third give landed rc 0 and m5 and m7 rc 2. Together they cover CE-1 and CE-2. Without them, the C3 delimiter suite cannot detect m6, and it detects m5 and m7 only incidentally.

## 6. Commands and exit codes (sandbox; key output)

| command | exit | key output |
|---|---|---|
| `git -C <lane> archive dd72641e… \| tar -x -C <sandbox>` | 0 | extracted |
| `sha256sum tools/research-gate.sh` | 0 | `ca39d14db907ec3f…` (matches assignment) |
| `bash -n tools/research-gate.sh` | 0 | syntax OK |
| `python3 probe/c3_delim_probe.py` | 0 | 9 gate variants × 26 synthetic fixtures (10 controls + 16 neighbors), ~4.2 s; matrix in `probe/run3.txt` |
| `bash tools/research-gate.sh verify-metadata corpus/knowledge/registry-link-r26.md --root . --registry corpus/SOURCES.md` | 0 | `RESEARCH_GATE: CLEAN` |
| `diff tools/research-gate.sh probe/mutants/m{1,5,6,7}-*.sh` | 1 each | single-hunk changes at 2466 (m1, m5, m7) and 2477–2479 (m6) |
| case-insensitive search for `feff\|BOM\|byte.order` in the landed gate | none | no BOM handling |

Not run: `--selftest` and the full `round27-regressions.py` (L1 owns both). The probe replays only the 10 registry-table tuples, eval'd verbatim from the script's source lines.

## 7. Limits

- Single-line mutants only; the search is not exhaustive. Lines 2469–2470 and 2488–2490 (the `header_width=0` resets) are dead stores, since `header_width` is read only when `header_candidate=1`, and that is only set alongside `header_width`. No control can detect their removal, so that is not a gap.
- GFM statements are `[INFERENCE]`, from memory, with no network in this lane.
- BOM handling for entries was not checked.
- Scope is the registry-table family only. Denylist, S-id, and date items were not probed.
- The verdict is advice to the author lane, not an outside admission.

## Tooling record

No installs or updates. `bash 5.3.20` and `python3 3.14.8` were already present. `RULES.md` was read first; nothing was installed, so there is nothing further to record.

## Erratum (appended; corrects three citations)

- Section 7 cited the `header_width=0` resets at 2469–2470 and 2488–2490. The correct lines are 2435 (non-table reset), 2479 (failed-separator reset), and 2493 (else reset). The arm is `header_candidate=1; header_width=${#cells[@]}` at 2489–2490, and the only read is the width check at 2466. All three resets are dead stores because each runs with `header_candidate=0`.
- Section 2 cited "lines 137–142 family". The ten tuples span lines 133–142 of the `tables` block (valid-table 133 through valid-aligned 142).
- Section 1 verdict said the landed gate's "only deltas from base" are CE-3 to CE-5. That overstates it. Base→landed deltas also include the intended fixes (header-trailing-empty-mismatch, bad-then-good 3-2-3 and 4-3-4, prose-break-then-valid). The only deltas that are not fixes are the contract-undefined escape and BOM cases.
- The S042 quote in CE-1 dropped backticks. The exact text is: a non-pipe line sets `header_candidate=0; continue` but does not reset `id_col`/`status_col`/`usedby_col`.
