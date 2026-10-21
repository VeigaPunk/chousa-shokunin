# ScoutSourceCensus — round27 initial SOURCES census

Seat: ChousaR27.ScoutSourceCensus (leaf, static read-only). Base observed:
64eec5d41c7cf7f17f5ce1e968e28b3769952596 (lane master). No edits, no lane Git/jj
writes, no gate/selftest/regression execution, no network, no host/live probes.

## Assigned item

Open `corpus/SOURCES.md`, derive the initial row/tier/status counts **using the
gate's own parser text**, and report the exact opened-source quote.

## Opened source and exact quote

Opened: `corpus/SOURCES.md` (regular file, single link, 26,793 bytes, no NUL,
final byte 0x0a). Registry header at lines 9–10; rows S001–S039 at lines 11–49;
line 50 is empty.

Exact quote (21 words), `corpus/SOURCES.md:4-5`:

> a row here is a claim that its author opened the source and judged its tier for the stated scope only.

## Parser text used (derivation authority)

`metadata_registry_load()` — `tools/research-gate.sh:2361-2470`; refusal/probe
path 2366–2405 (denylist, fd re-check, single link, `SOURCE_READ_MAX_BYTES`,
NUL/read status; limit is 8 MiB at `tools/research-gate.sh:271`).

Rules that decide which lines are rows (line-anchored):

1. A line with fewer than two `|` characters is skipped; once a header is found
   it **breaks the scan** (`2413: ((header_found)) && break`). Census therefore
   covers only the first contiguous pipe table.
2. Outer pipes are stripped, cells are split (`2422`) and trimmed; a row is
   accepted only after a header line containing cells exactly `id`, `status`,
   `used-by` (`2464`) is followed by an all-`^:?-{3,}:?$` separator (`2444`).
3. Accepted row ids must match `^S[0-9]{3,}$` (`2433`) and the **first**
   occurrence wins (`-z ${META_REGISTRY_STATUS[$row_id]+x}`); later duplicates
   are ignored. Status and used-by are stored raw (no vocabulary validation).
4. `2469` is fatal when no table header is found. No such condition applies here.

Applied to `corpus/SOURCES.md`, the header is line 9, the separator line 10 is
all `---` cells, and 39 contiguous rows (lines 11–49) are consumed before the
blank line 50 breaks the scan.

## Initial census (under those parser rules)

| count | value |
|---|---|
| rows | 39 (S001–S039, 39 distinct ids, 0 duplicates) |
| tier A | 33 |
| tier B | 1 (S018) |
| tier C | 5 (S014, S015, S016, S025, S027) |
| status mined | 16 |
| status queued | 19 |
| status rejected | 4 |

Cross-tab (tier/status): A/mined 16, A/queued 17, B/queued 1, C/queued 1,
C/rejected 4. Sums reconcile: 16+17+1+1+4 = 39.

Link consistency (calibration, not an admission): all 16 `mined` rows name a
concrete `used-by` entry path; 23 rows carry `—` (19 queued + 4 rejected);
16+23 = 39. Every row parses to 11 cells uniformly (no `\|` escapes anywhere in
the file; cells=13 only counts FS artifacts of `awk -F'|'` on the outer pipes).

## Census-stability notes for C3 (observation only, no fix here)

- The `2413` break means a non-table line inside or after the table truncates
  parsing silently; this census is exact only because the table is contiguous.
- `2444` requires the separator cells to match as a whole; a header followed by
  any other line resets `header_candidate` and the header columns are re-derived
  (`2453-2464`), so a fresh named header after a break is what FRegistryHeaderless
  must restore without changing these counts.
- Duplicate/overlapping id behavior is first-occurrence (`2433-2441`); FRegistryIdBoundary
  work must keep consumed-text scanning from turning one literal id into two
  occurrences without altering row identity counts.

## Final-census rule (not performed in this seat)

This is the **initial** census. After the new own-work S-row append, re-derive
with the identical rules: expected final = 40 rows, tier A 34, status mined 17,
used-by concrete 17, `—` 23 — provided the appended row is tier A/mined with a
real entry path and the table stays contiguous; any other row shape changes the
expected deltas accordingly. Do not hand-count; reuse this rule.

## Unrun checks / unknowns

- Not run (per lane bounds): `bash tools/research-gate.sh --selftest`,
  `python3 corpus/evidence/round27-regressions.py`, any gate invocation with
  `--registry corpus/SOURCES.md`, date/registry differentials. The parser above
  was read statically; its runtime acceptance of this file is not claimed.
- Unknown: whether any consumer currently passes this file as `--registry` in a
  test; no such call was executed or traced in this seat.
- No tools installed or updated; no pacman/uv/npm action taken.
