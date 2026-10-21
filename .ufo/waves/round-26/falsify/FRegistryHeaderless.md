# FRegistryHeaderless — C3 "registry without valid named table header exits 2"

Seat `ChousaR26R.FRegistryHeaderless`, round 26 attempt 1, author-lane advice only (no outside judge).

**Verdict: FALSIFIED.** On the immutable target, a registry with no valid
`id`/`status`/`used-by` header line can still exit 0. This happens when a full
header-named line was seen earlier and ended by a non-pipe line, such as a blank
line, prose, or a fence marker. The same root cause also produces column misbinding
in both directions: real defects get hidden (a false negative) and clean rows get
flagged (a false positive). On the real `SOURCES.md`, one prose column mention
plus a blank line turns a clean r24+ run (exit 0) into 11
`META_SOURCE_NOT_MINED` false positives (exit 1). The oracle stays clean on that
input.

## Target identity

- Revision `0e9784bd52eca456b24d0bc40921480a47f91a2b`, from `corpus/evidence/round26-measured-revision.json`. Claim base is `ba3333254dd337658a4f25e7a9471f9cf4e4567e`. The lane `HEAD` observed at start was also `0e9784bd…`.
- Sandbox: `git archive 0e9784bd… | tar -x -C /tmp/chousa-r26-falsify-FRegistryHeaderless/tree`.
- `sha256(tree/tools/research-gate.sh)` = `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`. This equals the manifest input hash.
- Oracle: `tree/corpus/evidence/round26-registry-oracle.py`, manifest hash `6b2d135c…`.
- Toolchain: GNU bash 5.3.20, Python 3.14.8. Nothing was installed or updated.
- Scripts are sandbox-only. `run.sh` sha256 is `93b4c69ad15238f7e2726aa92e5a6ad1b27befb34e5eec449560c42dc43a7037`. `stale.sh` sha256 is `9dd01f9c5393d35a03fb1a44abeac83d0a51175b67ca52a7cf0afb8e6cdc20d5`.

## Commands and exits

- `bash /tmp/chousa-r26-falsify-FRegistryHeaderless/run.sh` exited 0. This is the 35-fixture matrix plus refusal and flag-combination controls; run time was 1.5 s.
- `bash /tmp/chousa-r26-falsify-FRegistryHeaderless/stale.sh` exited 0. This covers the stale-index fixtures and the real-`SOURCES.md` shape.

Each gate call was:

```
env -u CHOUSA_RECORD -u CHOUSA_CLAIMS CHOUSA_STRICT=0 CHOUSA_ROOT=$W \
  bash tree/tools/research-gate.sh verify-metadata $W/corpus/knowledge/e.md --root $W --registry <fixture>
```

Each oracle call was `python3 round26-registry-oracle.py <same args>`. The entry
`e.md` is `source: S001` / `verified-at: 2026-10-20 checked` / `recheck: 90d`.

No selftest, build, lint, formatter, 8 MiB probe, or source fetch was run.

## Primary finding R26-FRH-1: stale header columns let a headerless table through (exit 0, should be 2)

Root cause, by code reading of `tools/research-gate.sh` at the target:

- `metadata_registry_load` lines 2412–2415: a non-pipe line sets `header_candidate=0; continue` but does not reset `id_col`/`status_col`/`usedby_col`.
- The only reset paths are line 2454 (a candidate followed by a non-separator pipe line) and line 2466 (a partial header line).
- On the next pipe line, every `if ((x_col < 0))` guard fails, so the stale indices survive. The "all three ≥ 0" test at line 2463 then marks that line as a header candidate whatever its cells say.
- Any following delimiter row sets `header_found=1`, and data rows are read with the stale indices.
- This contradicts the claim text ("columns are located by header name"; "a registry with no table whose header has `id`, `status`, `used-by` columns exits 2").

In the fixtures below, `HDR` is `| id | status | used-by |`, `SEP` is `|---|---|---|`, and `ROW` is `| S001 | mined | corpus/knowledge/e.md |`.

| id | fixture (`\n`-joined) | gate rc / findings | oracle rc / findings | contract |
|---|---|---|---|---|
| C01 (control) | `\| a \| b \| c \|`, SEP, ROW | 2 / no-table | 2 | 2 ✓ |
| S01 | HDR, *blank*, `\| a \| b \| c \|`, SEP, ROW | **0** / none, 1 verdict line | 2 | 2 ✗ |
| S02 | HDR, *blank*, SEP, SEP, ROW | **0** / none | 2 | 2 ✗ |
| S03 | fence, HDR, fence, *blank*, `\| a \| b \| c \|`, SEP, ROW | **0** / none | 2 | 2 ✗ |
| S04 | HDR, `prose`, `\| id \| note \| used-by \| status \|`, 4-cell SEP, `\| S001 \| mined \| corpus/knowledge/e.md \| queued \|` | **0** / none (**false negative**: the real status is `queued`) | 0 / `META_SOURCE_NOT_MINED` | 1 + NOT_MINED ✗ |
| S05 | HDR, `prose`, `\| id \| note \| status \| used-by \|`, 4-cell SEP, `\| S001 \| - \| mined \| corpus/knowledge/e.md \|` | **1** / `META_SOURCE_NOT_MINED` (**false positive**) | 0 / clean | 0 ✗ |
| P05 | HDR, `prose`, blank, the same 4-column table as S05 | **1** / `META_SOURCE_NOT_MINED` | 0 / clean | 0 ✗ |

C01 and S01 differ only by the leading HDR line and a blank line, which isolates
the trigger. In S01, S02 and S03, the table that was accepted has no
`id`/`status`/`used-by` header at all. In S03, the stale candidate is a header
line inside a fenced code block.

**R26-FRH-1b, realistic shape (calibration harm on the population).** The input
is the target-tree `corpus/SOURCES.md` with `Registry columns used by the gate:`,
a blank line, HDR and another blank line prepended. It is graded over the five
frozen r24+ entries, copied into a fresh root:

- With the unmodified `SOURCES.md`, the gate exits 0 with `META_RECHECK_ROOT_PARENT=1` only. The oracle exits 0 with all five entries clean.
- With the prepended mention, the gate exits **1** with `META_RECHECK_ROOT_PARENT=1 META_SOURCE_NOT_MINED=11`. The oracle exits 0 with all five clean.

In that case the stale indices 0/1/2 read `status` from the real `source` column
and `used-by` from `kind`.

The independent oracle catches S01–S05, so the differential design can detect
this class. However, `round26-registry-differential.sh` adversarial fixtures and
the 8 `metadata_registry_case` selftest calls contain no headerless or
no-named-table case. A grep for `no table with id` in the gate finds only the
`die_usage` line. The exit-2 branch therefore has no failing control (QUALITY 17).

## Secondary findings: grammar of a "valid table header" (gate and oracle disagree)

| id | fixture | gate | oracle | note |
|---|---|---|---|---|
| R26-FRH-2 (G01) | HDR + `\|---\|---\|` (2-cell delimiter row) + ROW | **0** | 2 | The gate never compares cell counts. In GFM, a delimiter row with a cell count different from the header is not a table, so the oracle is right. |
| R26-FRH-2 (G02) | HDR + 4-cell delimiter row + ROW | **0** | 2 | Same cause. |
| R26-FRH-2 (G09) | `\| x \\| id \| status \| used-by \|` + 3-cell delimiter row | **0** | 2 | Same cause. The contract forbids `\|` in cells, so the input is contract-invalid, but the gate still accepts it as a named header. |
| R26-FRH-3 (G10) | HDR + `\|---\|---\|---\|\|` | 2 | **0** | The oracle's `strip("\|")` collapses doubled outer pipes. The gate sees an empty 4th delimiter cell, which is invalid. Here the oracle is the lax side. |
| R26-FRH-3 (G11) | `\|\| id \| status \| used-by \|` + 4-cell delimiter row + `\|\| S001 …` | 0 | **2** | The same oracle `strip("\|")` produces 3 header cells against 4 delimiter cells. The gate's 4-cell reading matches GFM. Oracle defect. |
| R26-FRH-3 (H12) | `\| id<NBSP>\| status \| used-by \|` | 2 | **0** | Python `str.strip()` trims U+00A0, while the gate trims ASCII whitespace under `LC_ALL=C`. The gate matches the GFM rule of trimming spaces only. Oracle laxity. |

FRH-3 rows show that the oracle is not a byte-exact grammar twin. Its
"agreement" is only evidence on shapes where both readers use the same split
rule.

## Contract gaps where gate and oracle agree (unresolved, not graded as gate defects)

| id | fixture | gate | oracle | note |
|---|---|---|---|---|
| R26-FRH-4 (G03) | the only table is inside a fenced code block | 0 | 0 | Neither reader is fence-aware for the registry, though the oracle *is* fence-aware for entry metadata. |
| R26-FRH-4 (G04) | fenced example table (`S001 queued`) placed before the real table (`S001 mined`) | 1 / `META_SOURCE_NOT_MINED` | 1 / same | First-table-wins lets a documentation example shadow the real registry. Both report a false positive. |
| R26-FRH-4 (G05) | table indented 4 spaces (indented code) | 0 | 0 | `../CORPUS.md:152-153` (a maintained parser note outside frozen v1) says 4 or more spaces is indented code and ignored. |
| R26-FRH-4 (G06) | table inside `<!-- … -->` | 0 | 0 | Contract is silent. |
| R26-FRH-4 (G07) | non-qualifying table `\| a \| b \| c \|` whose body rows are HDR then SEP | 0 | 0 | In GFM these are body rows, so the registry has no named header. Both scan line pairs and fabricate a header from body rows. |
| R26-FRH-4 (G08) | table in a blockquote | 2 | 2 | GFM-valid table, rejected by both. This is over-strict, not unsafe. |

The claim says "table" without naming a grammar. These rows need a contract
decision, either GFM or "line-pair scan", before they can be graded. They are
recorded here as calibration risk only.

## Exit-2 path holds (expected-negative controls, all observed)

- **H01–H18 all exit 2** in both gate and oracle, except H12 (see FRH-3). Every gate run printed 0 `RESEARCH_GATE:` lines and the stderr line `research-gate: metadata registry has no table with id, status, and used-by columns`. The fixtures cover:
  - an empty file and prose only;
  - a header with no delimiter row, and a delimiter row with no header;
  - a missing `used-by` column, the `ID/Status/Used-By` case variant, backticked names and `used_by`;
  - header, blank line, then delimiter row;
  - `--` delimiter cells, which are GFM-valid but rejected by both readers (a strict choice that both share);
  - a single-pipe line, a non-dash delimiter cell, a setext `---`, and a heading-only file;
  - a non-separator line between header and delimiter, an empty delimiter cell, and the three columns split across two tables.
- **Positive controls:** P01 (plain), P02 (no outer pipes), P03 (CRLF) and P04 (alignment colons) all exit 0 with no findings in both readers. G12 (header-only table) exits 1 with `META_SOURCE_ROW_MISSING` in both.
- **Refusals:** a nonexistent path exits 2 with `metadata registry not found`. A directory exits 2 with `metadata registry is not a regular file`. A hardlinked file exits 2 with `metadata registry refused: multilink`.
- **Combinations:** a directory entry path with `--as-of 2026-10-21` and a headerless registry exits 2 with 0 stdout bytes. Repeating `--registry` uses the last value: `H01` then `P01` exits 0, and `P01` then `H01` exits 2. This is not a defect, just undocumented.

## Remaining unknowns

- I did not run a mutation that resets the indices at lines 2412–2415. The causal link rests on code reading plus the minimal-pair fixture C01 versus S01.
- I did not check whether any current production registry contains a stale candidate line. The real `SOURCES.md` grades cleanly (REAL-plain).

Checks for L1:
- Add negative selftest controls S01, S04 and S05 alongside a fix that resets all three column indices on every non-pipe line.
- Add G01 (delimiter cell count must equal header cell count) to both the gate and the differential.
- Decide the registry grammar for FRH-4 before grading those rows.
