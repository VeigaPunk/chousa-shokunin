# FC3 — `valid-no-outer-pipes` (C3 control) at dd72641

Item attacked: C3 control `valid-no-outer-pipes` in
`corpus/evidence/round27-regressions.py:140`, against lane revision
`dd72641e574679c4f7882dd43de072b4c8892d6f` (branch master), gate
`tools/research-gate.sh` sha256
`ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (equals
`git show dd72641:tools/research-gate.sh`). Sandbox:
`/tmp/chousa-r27-falsify-FC3ValidNoOuterPipes34` (git archive), base comparison
tree at `...-base` (git archive of `64eec5d41c7cf7f17f5ce1e968e28b3769952596`,
gate sha256 `c2c813f1…`). No production file, git/jj state, sibling lane or host
path was touched. No packages installed.

## Verdict

**HOLDS** as an expectation: the fixture is accepted by the landed gate for the
right reason, the expectation is a literal independent of gate code, and the
mutant that requires outer pipes makes it fail with the intended exit-2
diagnostic.

**FALSIFIED as a calibration discriminator:** the control cannot distinguish
cell-count width from raw-pipe-count width, and cannot distinguish
one-pipe-per-side stripping from strip-all-outer-pipes. Those are exactly the
two wrong implementations the r27 build notes assign to it. A gate mutated to
count raw pipes, or to strip every outer pipe, passes this control and all ten
shipped table controls; only two unshipped shapes catch them.

## What the control actually asserts

`round27-regressions.py:140`:

```python
('valid-no-outer-pipes', 'id | status | used-by\n---|---|---\n' + f'S001 | mined | {relative}\n', 0, None)
```

`observe()` (same file, `:34-45`) then requires only: exit `0`, no required or
forbidden substrings, and `len(re.findall(r'^RESEARCH_GATE: ', output, re.MULTILINE)) == 1`.
No C3 expectation is read from the gate; the gate text is read once at module
scope only to extract the two C1 usage helpers (`:76-82`). Code-independence at
runtime: yes.

Exact fixture run (sandbox, `LC_ALL=C`, `CHOUSA_STRICT=0`):

```
research-gate v2 — ts=2026-10-21T15:36:34Z — mode=verify-metadata — path=corpus/knowledge/entry.md — root=/tmp/tmp.PQTiObGelR
META entry=entry.md source=present verified_at=dated recheck=scheduled verdict=clean
METADATA_COMPLETE=1/1
RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)
EXIT=0
```

The same fixture on the **base** gate (`64eec5d`) also exits 0 with CLEAN. So
the control has zero differential power over the r27 repair itself: it is a
preservation/anti-overfit guard, not a detector that the width fix exists.

## (1) Is the expectation derived from the declared contract?

Partly, and the gap should be recorded.

- Declared text: `SKILL.md:482` defines `--registry FILE` as checking IDs
  "against the first table with id/status/used-by columns"; `round27-claims.md:15`
  (C3) additionally requires "matching header/delimiter widths" and
  "Existing well-formed registry behavior and exact used-by rules remain".
  The fixture is exactly such a table, and the base gate already accepted it,
  so the expected `0` is anchored by the preservation clause.
- The optionality of leading/trailing pipes is **not** declared in any lane
  contract document. Outside the r26/r27 wave-analysis notes under
  `.ufo/waves/` (findings, not declarations), the only occurrence of the term
  in the lane is the control's own name (`round27-regressions.py:140`); grep
  for "outer pipe|outer-pipe|leading pipe|trailing pipe" over `SKILL.md`,
  `README.md`, `PROVINCE.md`, `AGENTS.md`, `corpus/*.md` and
  `corpus/knowledge/*.md` returns no policy text. The r26 record is
  explicit that the grammar is undecided: "The claim says 'table' without
  naming a grammar. These rows need a contract decision, either GFM or
  'line-pair scan', before they can be graded"
  (`.ufo/waves/round-26/falsify/FRegistryHeaderless.md:112`), while recording
  P02 "no outer pipes" as an exit-0 positive for both readers at r26
  (`:120`). So the control's expectation rests on the r26 convention plus
  baseline behavior, not on a sentence of the frozen contract.
- Consequence for calibration: the C3 claim adopts GFM-style width equality
  (widths only mean anything under a Markdown table grammar) while the gate
  still keeps non-GFM strictness elsewhere (`--` delimiter cells rejected,
  blockquote table rejected, see below). The suite does not record which
  grammar it grades against.

## (2) Mutation of the targeted fix

Four single-hunk mutants of the sandbox gate copy; the shipped suite was not
executed. Each mutant was exercised with (a) a byte-faithful replica of the ten
shipped table rows plus two extra same-class positives (`width_subset.py`, 12
rows), and (b) a 17-row class probe (`probe.sh`).

| mutant | change | `valid-no-outer-pipes` | shipped 10 table controls | extra mixed-style | extra doubled-trailing delimiter |
|---|---|---|---|---|---|
| M1 `77f4bacd…` | require both outer pipes on every table line | **rc 2 vs 0**, verdict-count 0 vs 1 | 1 mismatch (this control) | mismatch | agree |
| M2 `6d8cda9e…` | width = raw pipe count of the pre-strip line | **agree (rc 0)** | **0 mismatches** | mismatch | agree |
| M3 `f0c831de…` | strip **all** leading/trailing pipes | **agree (rc 0)** | **0 mismatches** | agree | mismatch |
| M4 `91e3a4c6…` | delete the width comparison (revert the fix) | **agree (rc 0)** | 2 mismatches (`delimiter-too-short`, `delimiter-too-long`) | agree | agree |

M1 is the intended-direction mutant, and the failure reason is the intended
one, not a crash or parse error:

```
$ bash probe.sh mut-M1.sh M1        # fixture: id | status | used-by / ---|--- / S001 | mined | corpus/knowledge/entry.md
no-outer-all                       rc=2 | research-gate: metadata registry has no table with id, status, and used-by columns;
outer-all                          rc=0 | RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0);
```

M2's exact wrong refusal on the discriminator shape:

```
$ bash probe.sh mut-M2.sh M2
no-outer-all                       rc=0 | RESEARCH_GATE: CLEAN (...)
hdr-no_delim-yes_row-yes           rc=2 | research-gate: metadata registry has no table with id, status, and used-by columns;
```

M3's exact wrong acceptance:

```
$ bash probe.sh mut-M3.sh M3
no-outer-double-trail-delim        rc=0 | RESEARCH_GATE: CLEAN (...)   # landed gate: rc=2, no table
```

M4 shows the control is not a revert detector at all: deleting the new width
comparison leaves `valid-no-outer-pipes` green; only the two shipped negative
width rows fail. That is normal for a positive control but rules out reading
this control as evidence that the width comparison is present.

Mutant diffs were minimal, e.g. M2:

```
-      (( ${#cells[@]} == header_width )) || is_separator=0
+      pipebuf=${line//[^|]/}; (( ${#pipebuf} == header_width )) || is_separator=0
-      header_width=${#cells[@]}
+      pipebuf=${line//[^|]/}; header_width=${#pipebuf}
```

## (3) Nearby same-class inputs: where the control is vacuous

Mechanism: after the one-pipe-per-side strip, `cell_count == pipe_count + 1`
holds for every line. A width check that compares **pre-strip pipe counts**
therefore agrees with cell-count equality on every table whose header and
delimiter use the **same** outer-pipe style. It diverges only on mixed per-line
styles. Likewise a one-pipe strip and a strip-all implementation diverge only
on doubled outer pipes. The shipped control set has neither shape:

- `delimiter-too-short` (`:138`) and `delimiter-too-long` (`:139`) use fully
  piped headers and delimiters (4 pipes on both sides of the comparison for
  the long row; 4 vs 3 for the short row) — M2 and M3 both agree.
- the only no-outer-pipe row is this control, which is uniformly no-pipe
  (2 pipes on header and delimiter) — M2 agrees.
- no shipped row contains `||` or a mixed-style pair; grep of
  `round27-regressions.py` finds no such fixture. The gate selftest fixtures
  (`tools/research-gate.sh:6215-6434`) are also uniformly piped.

Precise counterexample inputs (both synthetic, both accepted by the landed gate
as shown):

1. mixed style — the raw-pipe-count discriminator; landed gate: rc 0 CLEAN;
   M2: rc 2 "no table" (wrong):

```
id | status | used-by
|---|---|---|
S001 | mined | corpus/knowledge/entry.md
```

2. doubled trailing pipes — the strip-all discriminator; landed gate: rc 2
   "no table" (GFM reading, matching r26 G10/G11 reasoning); M3: rc 0 CLEAN
   (wrong):

```
id | status | used-by
||---|---|---||
S001 | mined | corpus/knowledge/entry.md
```

The build notes themselves predicted both shapes and named the second one as
the detector: `.ufo/waves/round-27/build/ScoutRegistryWidths.md:95-96` (cases I
and J, expected 0), `:205` (`delimiter-doubled-pipe`, expected 2), `:213-214`
("`delimiter-doubled-pipe` is the mutation detector for a 'strip every outer
pipe' implementation: it must stay 2, not become 0"), `:52-53` ("**not** the
pipe count and **not** the result of stripping all outer pipes"). None of
cases I, J or `delimiter-doubled-pipe` is in the shipped suite. Also false as
written is `ScoutMetadataHeader.md:218-221`: "A width check based on raw pipes/
line length fails at least one" of its three recommended positives — those
three are uniformly styled per table, so raw-pipe counting passes all three
(measured: M2 mismatches 1 of 12 only on the mixed extra).

## Landed gate correctness for the class

29 same-class probes against landed and base gates (`probe.sh`, `probe2.sh`):
all-outer, all-no-outer, mixed header/delimiter/row styles, alignment colons,
CRLF, no-space cells, extra column, wide/short rows, header-only, `./` used-by
normalization, negative row variants (`queued`, wrong used-by, header-only),
plus BOM, 2-dash delimiter, 4-space indent, blockquote and second table after
prose. **Every landed result equals the base result**, and the landed output is
the contract-consistent one for the no-outer-pipe family (rc 0), with live
negatives proving the fixture path is exercised: `S001 | queued | …` →
`META_SOURCE_NOT_MINED` rc 1; wrong used-by → `META_SOURCE_USEDBY_MISSING` rc 1;
header-only → `META_SOURCE_ROW_MISSING` rc 1. No landed-gate error was found in
this class; r27 introduced no regression here.

Pre-existing class-adjacent strictness (base == landed, outside C3's promised
scope, recorded only to bound the grammar claim): BOM-prefixed no-outer table
rc 2, `-- | -- | --` delimiter rc 2 (GFM-valid; r26 FRH-4 records the shared
strictness), blockquote table rc 2 (GFM-valid), 4-space-indented table rc 0
(accepted although `../CORPUS.md:152-153` per r26 FRH-4 G05 says indented code
is ignored).

## Limits

- The full `--selftest` and the whole `round27-regressions.py` were not run
  (L1 owns both). The ten shipped table rows were re-executed via a
  byte-faithful replica (`width_subset.py`, sha256 `c5eb5268…`); results are
  stated for that replica, not for the script's own report.
- Mutation effects are measured on the sandbox copies only, with `LC_ALL=C`,
  `CHOUSA_STRICT=0`, temp roots under `/tmp`; no network, no host secret
  paths, no debugger, no `/proc` or live-process inspection by me (the gate
  reads its own `/proc/$$/fd/N` as shipped).
- The GFM statements are quoted from the lane's r26 evidence record, not from
  an external fetch (no network); the frozen claims do not declare a grammar,
  which is itself the point of finding (1).

## Author-lane advice

1. Ship the two discriminator controls the build notes already specify:
   mixed-style positive (`id | status | used-by` + `|---|---|---|` + row,
   expect 0) and `delimiter-doubled-pipe` (`||---|---|---||`, expect 2). Without
   them the C3 table set does not discriminate cell-count width from pipe-count
   width, or one-pipe strip from strip-all.
2. Correct the claim attached to `valid-no-outer-pipes`: it detects
   "outer pipes required", not "width counted by raw pipes" (M2) and not
   "outer pipes stripped repeatedly" (M3).
3. Record the grammar assumption behind "matching header/delimiter widths"
   (r26 left it undecided) or the preservation-only basis for the no-outer-pipe
   positive, so the control's expectation is auditable against text rather
   than convention.
