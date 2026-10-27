# R58ScribeGateLesson — round-58 lesson Gate outline (draft, report only)

Seat: scribe (leaf, no dispatch, no fetch). Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`,
claim base `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`, freeze `9e73a031ab1ac3bac343de008850d7d87f9e5634`.
Frozen inputs read first: `corpus/evidence/round58/claims.md`, `c1-count.py`, `c2-count.py`,
`c2/quotes.tsv`, `controls/*.txt`. Nothing frozen was altered; my only write is this report.
Scratch `/fast/scratch/hyaku/chousa-r58/R58ScribeGateLesson/` (removed before yielding).

## 0. Commands run (exact, observed)

```
sha256sum corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw → 6063a3aff7a4…ddf3  (129,024 B)
sha256sum tools/capture-text.py tools/build-spans.py → 2c0140bc…2573 · 1ed2650a…0bf6  (pins match claims)
python3 -B tools/capture-text.py <raw> | sha256sum (twice) → a8e3e7ad…f867 · 27,012 chars both runs
--locate '1．2．1 根据GB3469规定，以单字母方式标识以下各种参考文献类型：' → LOCATED count=1 offset=330
--locate '1．2 参考文献类型及其标识' → offset=315 · --locate '与文献标志码(Document code)' → offset=11723
per-quote sweep of c2/quotes.tsv in that form → ANCHORS 3 ROWS 12 UNIQUE 12
  offsets 315,330,590,683,734,781,797,838,965,993,1460,11723 (line-start: 315,330,993)
git log 6dc68fd6…raw → f9736a3 (round-57 re-fetch pass 1); refetch.tsv:19/:66 = attempts 1-2,
  2026-10-27T08:05:26Z / 08:29:36Z, curl_rc 0, HTTP 200, raw_sha256 6063a3af…ddf3
HEAD_ROWS=133 · BASE_ROWS=133 · git diff --stat b13ca7b5..9e73a031 -- corpus/SOURCES.md corpus/knowledge corpus/captures → empty
git grep b13ca7b5 -- corpus/knowledge: '載体类型标识' rc=1 (U+8F09) · '载体类型标识' rc=1 (U+8F7D) · 'GB3469' rc=1
```

## 1. Draft `## Gate` for `corpus/lessons/round-58.md`

### S101 re-opened from the lane-owned capture (no fetch, 2026-10-27)

S101 — `corpus/SOURCES.md:111`, tier B, status `mined`, `opened` 2026-10-25, recheck 180d. Bytes:
`corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`, 129,024 B, sha256
`6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3` (ran), with record rows
`corpus/evidence/round57/refetch.tsv:19` and `:66` (attempts 1 and 2, 2026-10-27T08:05:26Z /
2026-10-27T08:29:36Z, `curl_rc` 0, HTTP 200, `raw_sha256` = the same digest). No fetch this round:
that record is the lane's own fetch attestation, not an independent one (QUALITY 114). Defined form:
`tools/capture-text.py` sha256 `2c0140bc…2573`, 27,012 characters, form digest `a8e3e7ad…f867`.
**Located quote:** `1．2．1 根据GB3469规定，以单字母方式标识以下各种参考文献类型：` — char 330 of the
defined form, count 1, line-start; heading `1．2 参考文献类型及其标识` — char 315, count 1, line-start.
(`quote-reopen.py` is not used: it fetches, and no fetch is authorized this round.)

| surface | decision | evidence | flip |
|---|---|---|---|
| `corpus/knowledge/carrier-alphabet-china-r58.md` (12-quote S101 entry, C2) | **admit, narrowed**, conditional on `C2=PASS` (`corpus/evidence/round58/c2-measure-after.txt`) | 12/12 quotes unique, 3 line-start (315, 330, 993); entry path identical in all 12 manifest rows | a later edition, or a second document for the same ground |
| a new `SOURCES.md` row | **refuse** | base→freeze diff for `corpus/SOURCES.md` empty; rows 133 → 133 | a document the lane does not hold, opened and recorded |
| register `S096` used as a lane id | **refuse** | register and lane ids are different namespaces; the register row binds to lane S101 by URL | URL-bound citation only |
| old UTF-16LE anchors (11170/11205/11993/12161/13247/34374) as this entry's offsets | **refuse** | that decode is undefined (round-54 lesson Mistakes row 2; QUALITY 97 for the named form, 89 for offset re-location); the row cell stays as filed | a re-anchor that names its form and tool |

Narrowings the Gate must carry (each is a measured property of the capture, not a preference):

- **No letter↔type mapping.** The one document prints two tables: 1.2.1 (chars 330-469) prints 12 type
  cells — including 档案 and 古籍 — and 12 letter cells (tail `… G B O K`), all stacked one per line,
  so any pairing is read from stacking order; 14.3.1 (char 13105) prints 10 types against
  `M C N J D R S P G K` on single lines. No frozen quote carries a cell, so no mapping is admitted.
- **No A–E document-code content.** 11.6 (char 11968) prints the five codes; the frozen set holds only
  the section heading (char 11723). `A——基…` is outside this claim.
- **No single-wording claim.** 1.2.4 prints `标识` and `—`; 14.3.4 (char 13398) repeats the rules with
  `标志` and `——` and adds DB/MT, CP/DK, EB/OL.
- **No present-day edition or validity.** The located text carries no issue date or issuer statement.
- **char 1460 is an element-order tail** (`出版地:出版者,出版年:起止页码(当整体引用时不注).`), admissible
  for the element order only — the `[文献类型标识]` token is before the quote, not inside it.

### used-by change (old → new, in place)

- S101 cell 11, old `corpus/knowledge/citation-count-semantics-r37.md` → new
  `corpus/knowledge/citation-count-semantics-r37.md, corpus/knowledge/carrier-alphabet-china-r58.md`.
- No other cell changes: status `mined`, `opened` 2026-10-25, recheck `180d`, tier B, scope and anchor
  stay byte-identical. `opened` is the first lane opening and is not rewritten by this re-opening;
  the access date belongs on the entry's `verified-at:` line.

### Spot-check obligations (non-author, this round)

1. Re-locate the Gate quote and heading in the defined form and record the tool pin (QUALITY 89):
   `LOCATED count=1 offset=330` / `offset=315`; name the form, not the row's old decode.
2. Run the frozen counter on a lane copy with fresh `--work`: `C2=PASS`, `REF_ID_UNBOUND` absent.
3. Recount all 12 offsets and line-start anchors (list in §0). The anchor floor is met exactly at
   3/3 — there is no margin; any offset shift breaks PASS.
4. used-by and no-new-row: 133 rows at base and tip, `git diff --stat` empty, census unchanged
   (`corpus/evidence/round58/census-start.txt`: five pre-existing W04, `EXIT=0`).
5. Entry trio (`source:`, `verified-at:`, `recheck:`), `source:` line carries the URL plus a section
   1.2 anchor, no stray S-id, `载体类型标识` present in the entry.
6. Entailment read: every Observation line maps to a quote; the two-table divergence, char 1460 and
   char 11723 are called out as above.
7. New-ground is **not** evidenced by the counter's `NEW_GROUND` token (see F1). Re-run the
   simplified query: `git grep -l '载体类型标识' b13ca7b5 -- corpus/knowledge` → rc 1 (ran), plus
   `GB3469` → rc 1 (ran).

### Spot-check intake (proposed rows for r57 §6, QUALITY 14 — L1 decides each)

1. report rewrite → carried as practice (errata append, never rewrite); no rewrite in this lesson.
2. lowest-axis/L0 → worked this round by C1 (operability gate surface); the L0 r57 question stays open.
3. W2 residual seats → carried to the orchestrator; not a Gate surface.
4. forgeable provenance (RW-1) → carried; Gate wording says record-attested, never "verified fetch".
5. stray writer → carried: restore-from-branch, never adopt; no new stray this round.
6. five W04 duplicate URLs → carried, unremediated; census baseline unchanged.

## 2. Findings (reported, not fixed)

- **F1 (calibration, counter).** `c2-count.py:153-154` greps the **traditional** `載体类型标识`
  (U+8F09) at base while the entry must carry simplified `载体类型标识` (U+8F7D). The base query can
  never find the marker, so the leg cannot fail on a base entry that carries it. Today both queries
  return rc 1, so no false PASS is exercised; but the Gate must not cite `NEW_GROUND=yes` as new-ground
  evidence — cite the simplified query instead.
- **F2 (calibration, margin).** Line-start anchors are exactly 3/3 (315, 330, 993). The frozen floor is
  3; a rebuild that shifts any offset drops `ANCHOR_BOUND` under 3.
- **F3 (calibration, document).** The capture states the same rules twice (1.2 and 14.3) with different
  table widths and different terminology, so the entry's ground is one copy, narrowed as above; a
  "the specification's alphabet" claim would be contradicted by the document's own second table.
- **F4 (calibration, registry).** S101's scope cell covers "fields and type identifiers", but its anchor
  cell names sections 11, 14.1, 14.4, 15.7 only. The entry's own `source:` line must carry the section
  1.2 anchor (QUALITY 6). Extending the row's anchor cell would be a second edit beyond the frozen
  used-by-only change: do it and declare it, or refuse it — not silently.
- **F5 (calibration, provenance).** The fetch record is the lane's own tool's (QUALITY 114/RW-1); the
  Gate sentence says "committed lane capture with a record row", not "independently verified".
- **F6 (calibration, quote form).** The Gate quote is 36 characters, unique, line-start — inside the
  ≤25-word/≤160-char Gate shape — but it is a lead-in ending in `：`: it supports "single-letter type
  identifiers per GB3469", not an enumeration or a mapping.

## 3. Not run / limits

- `c2-count.py` was not run by me at any root; the base receipt `controls/c2-before.txt` is cited as
  committed (`C2=FAIL`, `ENTRY_MISSING`, exit 1), not re-measured.
- `c1-count.py` was not run; C1 has no Gate surface (no source opened). Its receipt is
  `controls/c1-before.txt` / `c1-controls.txt` (committed).
- `scripts/sources-census.sh` was not run; `census-start.txt` is cited as committed.
- `quote-reopen.py` was not run (live fetch; not authorized).
- No entry exists yet (`corpus/knowledge/carrier-alphabet-china-r58.md` absent), so the admit row is
  conditional and every obligation above is an instruction, not an observation of the entry.

## 4. Artifact paths

- Report: `.ufo/waves/round-58/w1/R58ScribeGateLesson.md`
- Frozen inputs: `corpus/evidence/round58/{claims.md,c1-count.py,c2-count.py,c2/quotes.tsv,controls/}`
- Capture/record: `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`, `corpus/evidence/round57/refetch.tsv`
- Registry: `corpus/SOURCES.md:111`; rules: `corpus/QUALITY.md` 6, 7, 14, 89, 97, 100, 101, 114

VERDICT: Lesson-Gate-outline draft — survives as narrowed to the 12-quote S101 ground (located at char 330, used-by old→new stated, no new row) and falsified as a "single table / A–E content / NEW_GROUND=yes / independent fetch" reading by F1, F3 and F5; F2 and F4 leave obligations with no margin.
