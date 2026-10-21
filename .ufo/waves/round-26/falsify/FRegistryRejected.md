# FRegistryRejected — C3 relation/grammar: rejected row ⇒ META_SOURCE_NOT_MINED

Seat `ChousaR26R.FRegistryRejected` (scout, author-lane advice only; no outside
judge). Judged on: calibration.

## Revisions and inputs observed

- Target: `0e9784bd52eca456b24d0bc40921480a47f91a2b` (from
  `corpus/evidence/round26-measured-revision.json`), extracted with
  `git archive 0e9784bd… | tar -x -C /tmp/chousa-r26-falsify-FRegistryRejected/tree` (exit 0).
- Claim base: `ba3333254dd337658a4f25e7a9471f9cf4e4567e`, extracted the same way to
  `/tmp/chousa-r26-falsify-FRegistryRejected/base` (exit 0).
- `sha256sum` in the extracted target: `tools/research-gate.sh`
  `c2c813f1…abc6`, `corpus/SOURCES.md` `8308e629…a5aa9`,
  `corpus/evidence/round26-registry-oracle.py` `6b2d135c…1d78`. All three match
  the measured-revision file. `git show 0e9784bd…:tools/research-gate.sh | sha256sum`
  gives the same gate hash `c2c813f1…abc6` (QUALITY 15).
- Code under test: `metadata_registry_load` (`tools/research-gate.sh:2361-2470`),
  `metadata_registry_check_source` (`:2472-2507`), and the header key loop (`:2627-2682`).
  The contract is `round26-claims.md:90-107,133-141` and `../CORPUS.md:86-108`
  (`No | inside any cell`; status ∈ `queued` · `mined` · `rejected`).
- Tools installed or updated: none.

## Method

- Harness: `/tmp/chousa-r26-falsify-FRegistryRejected/run.sh`, log `run.log`
  (harness exit 0, wall time 1.03 s). It contains 25 isolated fixtures, R01–R25, under
  `/tmp/chousa-r26-falsify-FRegistryRejected/w`.
- Each fixture runs two commands:
  - Gate: `env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0
    CHOUSA_ROOT=$W bash tree/tools/research-gate.sh verify-metadata <entry> --root $W
    --registry <reg>`. This is the same environment as the selftest's `metadata_registry_case`.
  - Oracle: `python3 tree/corpus/evidence/round26-registry-oracle.py <entry> --root $W
    --registry <reg>`.
- Not run: the full selftest, build, lint, `round26-measure.sh`,
  `round26-registry-differential.sh`, and the 8 MiB probe. No production file was
  edited, and no mutation of the gate was made.
- Expectations come from the C3 spec, the `CORPUS.md` contract and CommonMark/GFM
  table grammar. They are not taken from either implementation.

## Results (gate exit / gate findings / oracle)

| case | input shape | gate exit | gate findings | oracle | assessment |
|---|---|---|---|---|---|
| R01 | SOURCES-shaped `rejected` row, used-by names entry | 1 | NOT_MINED S014 | NOT_MINED | holds |
| R02 | `rejected`, used-by `—` | 1 | NOT_MINED S014 | NOT_MINED | holds |
| R03 | **real base `SOURCES.md`**, S014/S015/S016/S025 via continuation lines | 1 | NOT_MINED ×4 | NOT_MINED | holds |
| R04 | mined clean S001 + rejected S014 | 1 | NOT_MINED S014 only | NOT_MINED | holds |
| R05 | S014 cited twice | 1 | NOT_MINED ×2 (findings=2 drift=2) | set: NOT_MINED | count note (FRR-6) |
| R06 | `Rejected`, `REJECTED`, `` `rejected` ``, empty, `rejected (…)` | 1 | NOT_MINED ×5 | NOT_MINED | holds |
| R07 | status `mined`+U+00A0 | 1 | NOT_MINED | **[] (clean)** | gate/oracle split (FRR-5) |
| R08 | rejected row, id `S014`+U+00A0 | 1 | **ROW_MISSING** | NOT_MINED | gate/oracle split (FRR-5) |
| R09 | rejected row, id `S014`+U+001F | 1 | **ROW_MISSING** | NOT_MINED | gate/oracle split (FRR-5) |
| R10 | rejected row, `\|` in teaches (out of contract) | 1 | **USEDBY_MISSING** (not NOT_MINED) | USEDBY_MISSING | wrong finding id (FRR-2) |
| R11 | `\| id \| used-by \| teaches \| status \|`, GFM status `rejected`, `\|` in teaches | **0 CLEAN** | none | [] | **false clean** (FRR-2) |
| R12 | rejected row after a blank line in the table | 1 | ROW_MISSING | ROW_MISSING | GFM-consistent (table ends) |
| R13 | GFM one-pipe body row `S200 \| queued` before rejected row | 1 | **ROW_MISSING** | NOT_MINED | gate grammar (FRR-4) |
| R14 | delimiter-shaped body row before rejected row | 1 | NOT_MINED | **ROW_MISSING** | oracle grammar (FRR-5) |
| R15 | header 3 cells, delimiter 2 cells (GFM: not a table) | **1** | NOT_MINED | **exit 2** no table | gate accepts non-table (FRR-3) |
| R16 | fenced ```` ``` ```` example table (S014 mined) before real table (S014 rejected) | **0 CLEAN** | none | [] | **false clean** (FRR-1) |
| R17 | 4-space-indented code-block table before real rejected row | **0 CLEAN** | none | [] | **false clean** (FRR-1) |
| R18 | `<!-- … -->` comment table before real rejected row | **0 CLEAN** | none | [] | **false clean** (FRR-1) |
| R19 | `source: S014` then a second `source: S001` | **0 CLEAN** | none | [] | rejected citation dropped (FRR-6) |
| R20 | `s014`, `S`+U+200B+`014` | 0 CLEAN | NO_ROW_ID info | NO_ROW_ID | spec-compliant |
| R21 | duplicate id: rejected first, mined second | 1 | NOT_MINED | NOT_MINED | holds (first wins) |
| R22 | duplicate id: mined first, rejected second | 0 CLEAN | none | [] | spec-compliant (first wins); FRR-6 |
| R23 | CRLF registry, rejected row | 1 | NOT_MINED | NOT_MINED | holds |
| R24 | `https://e.example/S014/x S014-draft` | 1 | NOT_MINED ×2 | NOT_MINED | holds; count note |
| R25 | header `id\|status\|used-by\|status`, first `mined`, second `rejected` | 0 CLEAN | none | [] | spec-compliant (first column); FRR-6 |

Exact finding text from R01: `FINDING META_SOURCE_NOT_MINED severity=warn surface=metadata
obs=entry=r01.md source_id=S014 registry row is not mined` /
`RESEARCH_GATE: DRIFT (entries=1 complete=1 findings=1 drift=1)`.

Expected negative control: the base `ba333325` gate run on R01 exits **2**. It prints
the usage text and no `RESEARCH_GATE` line, which matches the registered "before: flag
absent → exit 2".

Population check at the target, run from the extracted tree:
`verify-metadata corpus/knowledge --root . --registry corpus/SOURCES.md` exits 1 with
`RESEARCH_GATE: DRIFT (entries=32 complete=29 findings=57 drift=3)`. It emits
**0** `META_SOURCE_NOT_MINED` findings. A scan of every pre-heading header line for
S014/S015/S016/S025 found no hits (grep exit 1). So no real entry cites a rejected row,
and this arm has no population exposure at this revision. That is an observation, not
a pass.

Real-registry exposure to the shapes above, checked with grep counts on target
`corpus/SOURCES.md`:

- fences 0
- `<!--` 0
- 4-space-indented pipe lines 0
- `\|` 0
- non-ASCII or control whitespace rows 0
- exactly one `| id |` header, at line 9
- all 39 rows have exactly 11 cells (NF=13)
- status counts: mined 16, queued 19, rejected 4 (S014, S015, S016, S025)

## Findings

**FRR-1 — the gate takes a non-table pseudo-table as the registry, so a rejected row is reported CLEAN (gate grammar; the oracle shares the defect).**

- Cases: R16, R17, R18 exit 0 with `verdict=clean`, although the only real
  (CommonMark/GFM) table marks S014 `rejected`.
- Cause: `metadata_registry_load` has no awareness of fenced code, indented code or
  HTML blocks. It trims leading whitespace (`:2418`) and the first qualifying
  pipe-header + delimiter pair wins (`:2413`, `:2469`).
- The oracle (`registry_rows`, `:28-61`) has the same blindness, so the gate/oracle
  differential **cannot** detect this.
- [INFERENCE] If "table" in the spec (`round26-claims.md:94`) means a Markdown table,
  this falsifies the "rejected row ⇒ NOT_MINED" relation at the grammar boundary.
- No current exposure (0 fences, comments or indented tables in `SOURCES.md`).
  `SOURCES.md` and `CORPUS.md` do illustrate structure in fenced blocks.

**FRR-2 — out-of-contract `|` inside a cell silently shifts columns.**

- `CORPUS.md:89` forbids `|` in any cell, but the gate never checks that a row's
  cell count equals the header's. Neither does the oracle, or the `NF==13` audit awk
  (`CORPUS.md:145`), which only skips such rows.
- R11 (header order `id | used-by | teaches | status`, which the spec allows because
  columns are located by name) reads status `mined` from the teaches fragment. The
  row's real status is `rejected`, and the result is CLEAN, exit 0.
- R10 (real column order) reports `META_SOURCE_USEDBY_MISSING` instead of
  `META_SOURCE_NOT_MINED`. That is a wrong finding id for a rejected row.
- The contract violation is not refused, so it does not reach exit 2. No current exposure.

**FRR-3 — the gate accepts a header/delimiter cell-count mismatch as a table.**

- R15: the gate exits 1 with NOT_MINED. The oracle exits 2 ("no table"). Under GFM,
  a header that does not match the delimiter row's cell count is not a table, so the
  spec's "registry with no table … exits 2" (`round26-claims.md:92-93`) is not honoured.
- The gate's `is_separator` check (`:2444-2447`) has no length comparison.
- The rejected row still yields NOT_MINED here (fail-closed), so the harm is to the
  exit-code contract, not to the C3 verdict.
- This is the only finding in this report where gate and oracle disagree on the exit code.

**FRR-4 — a GFM-valid body row with one pipe ends the table early.**

- R13: the gate requires two or more pipes per line (`:2412`). A GFM body row
  `S200 | queued` therefore terminates the table, and the following rejected S014 row
  is reported `META_SOURCE_ROW_MISSING`, not NOT_MINED.
- The oracle reports NOT_MINED. Both are still warn and drift; only the finding identity
  is wrong.
- `CORPUS.md:145` rows all start with `|`, so this is outside current usage.

**FRR-5 — the oracle diverges from the gate (oracle defects, gate fail-closed or CommonMark-consistent).**

- R07, R08, R09: the oracle trims with Python `str.strip()`, which removes Unicode
  whitespace and U+001C–U+001F. The gate trims C-locale `[:space:]` only.
  - R07: the oracle approves `mined`+NBSP as clean, while the gate says NOT_MINED.
  - R08/R09: for a rejected row, the gate says ROW_MISSING and the oracle says NOT_MINED.
- R14: the oracle stops at a delimiter-shaped body row, which GFM treats as an ordinary
  row. The gate continues and says NOT_MINED, which is GFM-correct.
- These fixtures would make `round26-registry-differential.sh` report a disagreement if
  added to it [INFERENCE: the differential script was not run].
- For calibration: the "independent" oracle is more lenient than the gate on R07, which
  is the dangerous direction for an approval oracle.

**FRR-6 — spec-compliant behaviours that affect calibration (no spec violation).**

- Repeated citations of one rejected id emit one finding per occurrence (R05, R24:
  `findings=2 drift=2`), so the drift tally counts citations, not distinct defects.
  The oracle compares sets, so counts are never checked against it (R03: four gate
  findings vs one oracle code).
- A duplicate `source:` key keeps only the last value (R19). An earlier citation of a
  rejected row disappears with no finding and exit 0. This is consistent with the
  oracle and with legacy last-key-wins for `verified-at`/`recheck`.
- First-row-wins (R22) and first-status-column-wins (R25) let a `mined` reading mask
  a later `rejected` row or column. This follows the registered rule. `CORPUS.md:88`
  ("never reused") keeps duplicate ids out of contract.
- The NOT_MINED `obs` text omits the observed status, so `rejected` (a taste refusal)
  and `queued` (pending mining) are indistinguishable in the output.

## Verdict for this target

- **Not falsified on in-contract input.** Every contract-shaped rejected row produces
  exactly `META_SOURCE_NOT_MINED` with exit 1 and a drift verdict. That covers R01–R04,
  R06, R21, R23, R24, and R03 on the real base registry.
- **Falsified at the Markdown grammar boundary**: FRR-1 gives three false CLEAN results,
  and FRR-2 gives one false CLEAN result plus one wrong finding id, both shared by the
  oracle. FRR-3 and FRR-4 are gate grammar deviations that change the exit code or the
  finding identity.
- None of these shapes occur in `SOURCES.md` at `0e9784bd`, so the C3 population
  figures are unaffected.
- Suggested independent controls for L1: R11, R15, R16, R17.
  - Expected gate/spec behaviour: exit 2, or NOT_MINED computed from the real table only.
  - With the shipped gate: CLEAN for R11/R16/R17, and exit 1 instead of 2 for R15.
