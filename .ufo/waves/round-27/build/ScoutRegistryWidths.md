# ScoutRegistryWidths — C3 header/separator width derivation (round 27 attempt 1)

Seat `ChousaR27.ScoutRegistryWidths` (scout, leaf). Read-only static analysis; no gate,
selftest, regression script, oracle or differential was executed, and nothing was installed.
Axes: **calibration** primary, **operability** secondary (the exit-2 no-table contract);
freshness unaffected. All fixtures below are synthetic strings for a temporary directory; none
were run. `[OBS]` = read from source/receipt, `[DERIVED]` = traced statically, `[INFERENCE]` =
conclusion resting on the derivation.

## Identity and scope

- Lane base `64eec5d41c7cf7f17f5ce1e968e28b3769952596`. Parser cited from
  `.ufo/waves/round-27/baseline-research-gate.sh`, sha256
  `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`
  (`baseline-identity.json:baseline_gate_sha256`).
- The lane working tree has an uncommitted C1 hunk in `tools/research-gate.sh` (`diff` hunks at
  6007, 6021, 6235); the registry function region 2361–2507 is byte-identical to the baseline
  file. Line numbers below are baseline numbering.
- Oracle `corpus/evidence/round26-registry-oracle.py` sha256 `6b2d135c…b40f1d78`; persisted r27
  controls `corpus/evidence/round27-regressions.py` sha256 `3198bf21…158aa751`.
- Assignment: derive header/separator width validation, including extra and missing outer pipes,
  for `metadata_registry_load`. Token identity and the filesystem-path denylist are other seats.

## What the base parser already does `[OBS]`

1. **Cell splitting is already GFM-shaped.** After trailing-whitespace trim, it removes **at most
   one** leading `|` and one trailing `|` (`:2417-2421`), then splits on `|` and preserves empty
   fields via the `__chousa_registry_end__` sentinel (`:2422-2423`), then trims each cell
   (`:2424-2429`). A doubled edge pipe therefore yields one empty edge cell; a missing edge pipe
   changes no cell count.
2. The line guard requires two `|` characters (`:2412`). Any line of three or more cells has at
   least two pipes, so this guard can never exclude a header or delimiter of a qualifying
   three-name table. It is not part of the width rule.
3. Header recognition records only first-occurrence column indices for the exact trimmed cells
   `id`, `status`, `used-by` (`:2456-2461`) and sets `header_candidate=1` (`:2463-2464`). It
   records **no width**.
4. Delimiter recognition tests only the per-cell grammar `^:?-{3,}:?$` (`:2443-2451`); there is no
   cell-count comparison.
5. Reset sites are inconsistent: the non-pipe branch clears only `header_candidate` (`:2412-2415`);
   the failed-delimiter path clears the three indices (`:2453-2454`); the failed-header path
   clears them (`:2465-2466`). This is the r26 stale-state defect.

Authority for the rule: “a delimiter row with a cell count different from the header is not a
table” (`.ufo/waves/round-26/falsify/FRegistryHeaderless.md:89`, 15 words), and the round-27
requirement “matching header/delimiter widths” (`corpus/evidence/round27-claims.md:15`). The
gate's single-outer-pipe stripping is the split that r26 already judged GFM-correct on
`FRegistryHeaderless.md:92-93` (G10/G11); the oracle's `strip("|")` is the deviation.

## Derived width rule

**W0 — width definition.** `width(line)` = number of fields after removing at most one leading
and one trailing `|`, splitting on `|`, and retaining empty fields. It is **not** the pipe count
and **not** the result of stripping all outer pipes.

**W1 — capture.** When the name scan makes a line a candidate header, record
`header_width=${#cells[@]}` in the same branch. A qualifying header necessarily has width ≥ 3, so
the `:2412` guard cannot have excluded it.

**W2 — match.** A candidate is completed by the next line iff (a) `${#cells[@]} == header_width`
and (b) every cell matches `^:?-{3,}:?$`. The dash grammar is unchanged.

**W3 — state tuple.** `header_candidate`, `id_col`, `status_col`, `usedby_col`, `header_width`
are one tuple: assigned together, cleared together. Clear all five on the non-pipe branch
(`:2414`), on a failed delimiter (`:2454`) and on a failed header scan (`:2466`). On acceptance,
clear only `header_candidate` and `header_width`; the three indices must survive to read body
rows. Width is never inherited across a break or across a second header. Keep the existing
fall-through that re-examines a failed-delimiter line as a possible header.

**W4 — one split rule.** Header, delimiter and body rows must use the same W0 split. Do not
"repair" rows by trimming empty edge cells; that would reintroduce the oracle's doubled-pipe
laxity and make row positions differ from the declared columns.

**W5 — monotonicity.** The test is conjunctive with the existing dash check, so it can only
reject pairs the base accepts; it cannot make any currently rejected pair a table.

Why cell count and not pipe count: a header `id | | status | used-by` has 3 pipes and 4 cells,
while the matching delimiter `|---|---|---|---|` has 5 pipes and 4 cells. A pipe-count rule would
reject this GFM-valid four-column table; W0 accepts it (control K below).

## Truth table (fixture labels expanded in the next block)

`now` is the base outcome traced from `:2412-2467`; `after` is the outcome under W0–W5.
Exit 0 means one CLEAN verdict unless noted.

| ID | header / delimiter / body | width | now | after | note |
|---|---|---|---|---|---|
| A | H3s / S3c / R3c | 3/3 | 0 | 0 | canonical positive control |
| B | H3s / S2c / R3c | 3/2 | 0 clean | **2** | persisted `delimiter-too-short` (`round27-regressions.py:132`) |
| C | H3s / S4c / R3c | 3/4 | 0 clean | **2** | persisted `delimiter-too-long` (`:133`) |
| D | H3s / S4t / R3c | 3/4 | 2 | 2 | doubled trailing delimiter pipe; gate stays right (oracle says 0) |
| E | H4l / S4c / R4l | 4/4 | 0 | 0 | G11: extra leading pipe is an empty column, not decoration |
| F | H4l / S3c / R4l | 4/3 | 0 clean | **2** | new rejection: empty leading column not declared by delimiter |
| G | H4t / S4c / R3c | 4/4 | 0 | 0 | extra trailing pipe = empty last column; id/status/used-by stay at 0/1/2 |
| H | H4t / S3c / R3c | 4/3 | 0 clean | **2** | new rejection |
| I | H3s / S3n / R3c | 3/3 | 0 | 0 | outer pipes optional on the delimiter alone |
| J | H3n / S3c / R3n | 3/3 | 0 | 0 | P02 class: outer pipes optional everywhere |
| K | H4e / S4c / R4e | 4/4 | 0 | 0 | pipe-count trap: 3 pipes vs 5 pipes, equal cells |
| L | H3s, prose, H4r / S3c / R3c | 4/3 | 0 clean | **2** | width binds to the immediately preceding candidate; today stale indices accept it |
| M | H4l / S4c / R3c | 4/4 | 1 ROW_MISSING | 1 | positional body read; empty id cell fails closed |
| N | H3s / S4i / R3c | 3/4 | 2 | 2 | inner empty delimiter cell |
| O | H4x / S4c / R4x | 4/4 | 0 | 0 | extra named column preserved |
| P | H3s / `\|:---\|:---:\|---:\|` / R3c | 3/3 | 0 | 0 | alignment colons (P04) |
| Q | H3s / S3c / R3c, all CRLF | 3/3 | 0 | 0 | CR stripped at `:2411` (P03) |

Fixture legend (one line each; `\n` is a literal newline):

```
H3s  = | id | status | used-by |
H3n  = id | status | used-by
H4l  = || id | status | used-by |          # 4 cells: "", id, status, used-by
H4t  = | id | status | used-by ||          # 4 cells: id, status, used-by, ""
H4e  = id | | status | used-by             # 4 cells: id, "", status, used-by
H4r  = | id | note | status | used-by |    # 4 cells, reordered
H4x  = | id | status | used-by | x |      # 4 cells, extra named column
S3c  = |---|---|---|        S3n = ---|---|---
S2c  = |---|---           S4c = |---|---|---|---|
S4t  = |---|---|---||     S4i = |---|---||---|
R3c  = | S001 | mined | corpus/knowledge/entry.md |
R3n  = S001 | mined | corpus/knowledge/entry.md
R4l  = || S001 | mined | corpus/knowledge/entry.md |
R4e  = | S001 | x | mined | corpus/knowledge/entry.md |
R4x  = | S001 | mined | corpus/knowledge/entry.md | note |
```

Entry for every case: `source: S001` / `verified-at: 2026-01-02 checked synthetic fixture` /
`recheck: 90d` / `## Claim`; `CHOUSA_STRICT=0`, `LC_ALL=C`, cwd = temp root, registry path
absolute. `[DERIVED]` traces:

- F: header cells `["",id,status,used-by]` bind id=1/status=2/used-by=3; the 3-cell delimiter is
  accepted today, so the 4-cell body parses clean. W2 makes the pair 4≠3 and exits 2.
- H: header binds 0/1/2, body 3 cells parses clean today; W2 makes 4≠3 and exits 2.
- L: today the second header reuses the stale indices (id=0, status=1, used-by=2), so the 3-cell
  delimiter is accepted and `status` is read from the `note`-position cell (`mined`) → false
  CLEAN, exit 0; with the tuple reset alone the second header re-binds, but its 4-cell width then
  meets a 3-cell delimiter, so W2 rejects 4≠3 → exit 2.
- M: under the accepted 4-cell header, id_col=1; the canonical 3-cell row's cell 1 is `mined`, not
  an S-id, so the row is ignored → `META_SOURCE_ROW_MISSING` warn, exit 1. This is the positional
  consequence of an empty edge cell; it does not misbind status. Do not special-case it.

## Minimal patch sketch (advice; executors own the edit)

```bash
# :2364
  local id_col=-1 status_col=-1 usedby_col=-1 header_width=0 is_separator

# :2412-2415 non-table break: clear the whole tuple
    if [[ $line != *'|'*'|'* ]]; then
      ((header_found)) && break
      header_candidate=0
      id_col=-1; status_col=-1; usedby_col=-1; header_width=0
      continue
    fi

# :2443-2455 delimiter: width first, then the unchanged dash grammar
    if ((header_candidate)); then
      is_separator=1
      if (( ${#cells[@]} != header_width )); then is_separator=0; fi
      if ((is_separator)); then
        for cell in "${cells[@]}"; do
          [[ $cell =~ ^:?-{3,}:?$ ]] || { is_separator=0; break; }
        done
      fi
      if ((is_separator)); then
        header_found=1
        header_candidate=0
        header_width=0
        continue
      fi
      header_candidate=0
      id_col=-1; status_col=-1; usedby_col=-1; header_width=0
    fi

# :2463-2467 capture with the candidate
    if ((id_col >= 0 && status_col >= 0 && usedby_col >= 0)); then
      header_candidate=1
      header_width=${#cells[@]}
    else
      id_col=-1; status_col=-1; usedby_col=-1; header_width=0
    fi
```

- The script runs `set -euo pipefail` (`:255`); write the width test as an `if`, not a bare
  `(( … )) && …` statement, so a mismatch cannot abort the gate.
- Do **not** factor this into a helper function defined inside `metadata_registry_load`: bash
  functions are global and would leak after return. Inline the tuple clears (two lines each).
- Keep `((header_found)) && break` at `:2413`. It preserves first-table-wins and the oracle's
  first-qualifying-table behavior; the r27 `reorder-*` controls need only the tuple reset, not a
  post-table rescan.
- This sketch plus the tuple reset fixes all seven existing persisted table controls
  (`round27-regressions.py:127-133`): `valid-table` 0, `header-break-blank`/`header-break-prose` 2,
  `reorder-clean` 0, `reorder-queued` 1 NOT_MINED, `delimiter-too-short` 2, `delimiter-too-long` 2.
  `[DERIVED]`

## Persisted controls to add (synthetic; current script style)

Persist in `corpus/evidence/round27-regressions.py:126-134`, not in the selftest, so the 187-case
census and its expected count stay untouched. Add to the `tables` list (rc 2 entries get the
`metadata registry has no table` requirement automatically at `:138-139`):

```
('extra-leading-pipe-matched',     H4l + '\n' + S4c + '\n' + R4l, 0, None),
('extra-leading-pipe-mismatched',  H4l + '\n' + S3c + '\n' + R4l, 2, None),
('extra-trailing-pipe-matched',    H4t + '\n' + S4c + '\n' + R3c, 0, None),
('extra-trailing-pipe-mismatched', H4t + '\n' + S3c + '\n' + R3c, 2, None),
('delimiter-doubled-pipe',         H3s + '\n' + S4t + '\n' + R3c, 2, None),
('outer-pipes-missing-mixed',      H3n + '\n' + S3c + '\n' + R3n, 0, None),
('inner-empty-column-pipe-count',  H4e + '\n' + S4c + '\n' + R4e, 0, None),
('fresh-header-own-width',         H3s + '\nprose\n' + H4r + '\n' + S3c + '\n' + R3c, 2, None),
```

For the rc 0 entries, strengthen with `('verdict=clean', 'findings=0 drift=0')` via a direct
`observe` call if the loop's `required` derivation is not extended; exit 0 alone already rules
out warn-level findings, but not info findings. `delimiter-doubled-pipe` is the mutation detector
for a "strip every outer pipe" implementation: it must stay 2, not become 0.

Optional selftest-shaped cases (only if L1 deliberately changes the case census): two
`metadata_registry_case` calls with H4l/S4c/R4l expecting rc 0 and H4l/S3c/R4l expecting rc 2
plus `metadata registry has no table`.

## Preservation argument (harm none)

`[OBS]` Widths of every existing registry input already match, so W2 rejects none of them:

- real `corpus/SOURCES.md`: header/delimiter 11/11 (`:9-10`); all 166 lines beginning with `|` in
  the file carry exactly 12 pipes → 11 cells under W0 (static awk count, no gate run).
- contract shape `../CORPUS.md:86-87`: 11/11.
- selftest fixtures: 3/3 (`research-gate.sh:6168-6169`), reordered 4/4 (`:6205-6206`), duplicate
  3/3 (`:6222-6223`).
- r26 differential generated registry: 12/12 (`round26-registry-differential.sh:121-128`).
- r26 measure fixture: 11/11 (`round26-measure.sh:183-184`).
- r26 observed positives P01–P04 (`FRegistryHeaderless.md:125`); H01–H18 refusals are unaffected
  because W2 only adds a rejection condition.

No finding code, finding text, severity, exit-1/exit-2 meaning, or used-by rule changes. The only
observable changes are the new exit-2 rejections B, C, F, H, L; D and N stay 2 (width and the dash
grammar agree), E, G, I, J, K, O, P, Q stay 0, and M stays 1.

## Oracle and differential alignment

`[OBS]` The oracle already requires `len(header) == len(separator)` (`round26-registry-oracle.py:37`)
but splits with `text.strip("|").split("|")` (`:26`), collapsing **every** doubled edge pipe.

- After W2, gate and oracle agree on G01/G02/G09 (gate 0 → 2, oracle already 2).
- G10 (`|---|---|---||`) and G11 (`|| id | …`) remain disagreements: the gate is GFM-correct
  (`FRegistryHeaderless.md:92-93`), the oracle is not. Do not derive persisted expectations for
  doubled-edge-pipe shapes from the oracle.
- The frozen r26 differential has no width-mismatch or doubled-edge-pipe fixture, so its agreement
  count cannot change; it cannot grade this repair either.

## Residual limits (report, do not claim fixed)

- Fenced, indented (≥4 spaces), HTML-comment and blockquote tables are still scanned as plain
  lines; first qualifying table wins (revives the fenced-example false positive class,
  `FRegistryHeaderless.md:109-113`).
- Duplicate required column names remain first-column-wins.
- `|` inside a cell (contract-invalid, `../CORPUS.md:89`) still shifts later cells; body-row width
  is not validated (GFM pads short rows and ignores extra cells), so an out-of-contract body row
  can still produce a wrong finding id while failing closed.
- A body row with fewer than two pipes still ends the table (`FRR-4`).
- `--` delimiter cells remain rejected (shared strictness with the oracle).
- The width repair establishes table **shape** identity only; it says nothing about registry
  content, source truth, parser resource bounds, or full criterion-6 verification.

## Unrun checks

No execution was performed, per the assignment. L1 should run once after integration:
`python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh`;
`bash tools/research-gate.sh --selftest`; and the r26 registry differential on an isolated copy.
Every exit code above is a static trace and must be confirmed by that run.

**Touched surface:** this report only.
**Artifact:** `.ufo/waves/round-27/build/ScoutRegistryWidths.md`
