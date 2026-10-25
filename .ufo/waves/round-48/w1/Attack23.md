# Attack23 — register hand-check, chousa S080 (round 48 wave 1)

Seat: L1Chousa48.Attack23 (leaf scout). Round 48 wave 1. No fetch, no nested
dispatch, no installs (none needed; `RULES.md` read before any would-be tool
work — no tool change happened).

## Item
Hand-check one distinct lane-row from the chousa slice of `absent-defect-register.md`,
row ordinal 2 when sorted by lane source rows. Read only local campaign captures and
lane repo; classify present/absent/unverifiable with exact evidence and anchor.
No live fetch, no adoption edits.

## Row selection (ordinal 2)
"Sorted by lane source rows" is applied as: the chousa slice, sorted by its source-id
(`S###`) within the lane — the same order the lane's own quarantine slice enumerates
(`.ufo/waves/round-48/assimilation/quarantine-slice` lines 1–20: S077, S080, …).
Ordinal 1 = S077, so ordinal 2 = **S080**. (Under an alternate reading — sort by the
cited-source URL string — ordinal 2 would be S110, which already has a round-47 verdict
`QuarReg110.md`; the fresh-row reading is used and is the one consistent with the
quarantine-slice enumeration.)

Selected row: `absent-defect-register.md` line 38:
```
| `chousa` | round1 | S080 | `payload-absent` | https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F | `标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01` | cited source, companion URLs and local artifacts were all checked; the quote is in none of them |
```
The row's quote cell carries one backticked quote (120 chars, ends at sentence end).

## Inputs (read-only)
- Register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (line 38).
- Census: `quote-lint-full-v5.json` findings [83] (chousa S080, verdict `ABSENT`, fold null) and [84] (same row, second quote `GB/T 7714-2015 （全部代替）`, verdict `folded`/whitespace).
- Capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/adf6ba934e813b2c326fa150.txt` (6626 bytes, 3591 chars, sha256 `4e46154f4a841d17d858eafb5c0099257030f301daadcaa30c37f2e668fb7138`) and `.raw` (70132 chars, sha256 `a7b868be292a4c00a6cc1f56b1bd238549a468da4b03a9935b158523654f1409`). Filename = `sha256(URL)[:24]` of the row's cited URL; mtime 2026-10-23T20:33 (pre-round-48, no live fetch). Offsets below are 0-based Python str (code-point) offsets into `.txt` unless stated.

## Commands and decisive output
1. `printf '%s' URL | sha256sum | cut -c1-24` → `adf6ba934e813b2c326fa150`; capture exists as `.txt`/`.raw`.
2. Exact substring search of the register quote in `.txt` and `.raw`: `-1` both. Whitespace-collapsed search (collapse all `\s+`): `-1` both. So the mechanical "absent" is reproducible even after whitespace-only normalisation.
3. Fragment scans (`.txt`): `标准号` @1327; `GB/T 7714-2025` @1239 and @1333; `发布日期` @1354; `2025-12-02` @1034 and @1361; `实施日期` @1382; `2026-07-01` @1053 and @1391. No `标准号：`/`发布日期：`/`实施日期：` (or ASCII `:`) anywhere adjacent to any label (full-source find `-1` on both captures).
4. Second census quote (not shown in the register's quote cell): `GB/T 7714-2015 （全部代替）` whitespace-fold present at collapsed index 504, raw `.txt` chars 1136–1172 (`GB/T 7714-2015` @1136, `（全部代替）` @1162).

## Capture structure (why the fold fails)
The page is the national-standard record for GB/T 7714-2025 ("信息与文献 参考文献著录规则").
The quoted triple is the `基础信息` field block, which the text layer renders as separate
label/value tokens, not as colon-joined text:
```
基础信息 @1309
标准号 @1327  →  GB/T 7714-2025 @1333
发布日期 @1354  →  2025-12-02 @1361
实施日期 @1382  →  2026-07-01 @1391
```
Raw HTML confirms: `<dl class="basicInfo-block …"><dt …>标准号</dt><dd …>GB/T 7714-2025</dd>` then the same for 发布日期/实施日期 (raw chars 39799–40120); no `：`/`:` occurs in the block. The same dates also appear in the status timeline as `发布 于 2025-12-02` @1029 and `实施 于 2026-07-01` @1048 (no colons there either).

## Verdict
- quarantine: register `S080` (https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F) verdict: `absent` — the quoted line `标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01` exists nowhere in the capture (exact and whitespace-fold searches both `-1`); every element exists only as separate label→value cells in the `基础信息` block (`标准号`@1327→`GB/T 7714-2025`@1333, `发布日期`@1354→`2025-12-02`@1361, `实施日期`@1382→`2026-07-01`@1391), so the quote is a re-rendered concatenation that inserts `：` characters absent from the source — a quote-hygiene/structure artifact, not invented data (all three facts are genuinely on the page).

## Anchor (contiguous, present)
- `GB/T 7714-2025` @1239 (inside "当前标准" panel) and @1333 (`基础信息` value); count 2, not unique.
- `2025-12-02` @1361 and `2026-07-01` @1391 (field values), also `发布 于 2025-12-02` @1029 / `实施 于 2026-07-01` @1048 (timeline).
- Second census quote `GB/T 7714-2015 （全部代替）` present on whitespace fold (chars 1136–1172) — it is the row's other quote and is NOT absent.

## Findings by severity
1. (medium, register) `absent-defect-register.md:38` marks S080 `payload-absent`; the mechanical verdict stands for the quoted span as written, but the row is a *restyled metadata line*, not a fabricated fact: all three data points (standard number, publish date 2025-12-02, implement date 2026-07-01) are present as field pairs in the capture. A lane entry citing this record should quote one of the anchors above (e.g. `GB/T 7714-2025` or `发布 于 2025-12-02`), not the colon-joined line.
2. (low, register completeness) The register's quote cell shows only the first of the row's two census quotes; the second (`GB/T 7714-2015 （全部代替）`) is whitespace-fold present and was already marked `folded` in `quote-lint-full-v5.json` [84]. The single-quote display hides a mixed (absent + present) row.

## Residual risk and verification gaps
- Hand-check covers only the on-disk captures (`.txt`, `.raw`); live page not fetched (L0 `8d77e6c1` open). Capture fidelity to the live page is assumed from the Oct-23 fetch.
- Offsets are code-point indices into the UTF-8 `.txt`; the page's JS-rendered mobile view could render the field block colon-joined, but no such rendering is captured locally.
- No tools installed. No scratch dir used. No lane/production files touched; register read-only.
