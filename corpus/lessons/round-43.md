# Round 43 — the absent class splits, and one search-log entry is re-grounded locally

author: chousa L1 (Kimi fresh L1)
date: 2026-10-24
round: 43 (attempt 1)

## Claims and measurements

Frozen design: `corpus/evidence/round43/claims.md`. The construction recompute
that reproduced the published ratios (S086 4/46 and 2/29; S093 79/120) preceded
the freeze and is disclosed there. No seat had scored the predicates when the
rule was frozen. No external fetch (L0 `8d77e6c1` still open).

- **C1 operability (lowest scored non-retired axis, 3/10):** `python3 corpus/evidence/round43/c1-count.py` → `ABSENT_ENUMERATED=15/15`, `CLASSED=15/15`, `BOTH_NONEMPTY=1/1` (misquote 9, not-carried 6), `REPRODUCIBLE=1/1`, `MUTANT_DETECTED=1/1`, `C1=PASS`, exit 0. Do-nothing (`--tool` missing) exits 1 (`controls/c1-control-before.txt`).
- **C2 calibration:** `python3 corpus/evidence/round43/c2-count.py` → `SPLIT_AGREES=15/15`, `VOCAB_OK=15/15`, `C2=PASS`, exit 0. Flipped S086 → `SPLIT_AGREES=14/15`, exit 1 (`controls/c2-control-before.txt`).
- **C3 depth (sourced, S078):** `python3 corpus/evidence/round43/c3-count.py` → `ENTRY_CITES=1/1`, `QUOTE_LOCATED=1/1`, `URL_MATCH=1/1`, `C3=PASS`, exit 0. Missing entry exits 1 (`controls/c3-control-before.txt`).

The round-1 operability scale is unchanged: 3 → 3. `tools/research-gate.sh` is not touched.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| class-collapse — one label hid two failure modes | round-42 table labelled 15 rows `absent`; S093 is 79/120 of the quote and S086 is 4/46 | none — QUALITY 59 names capture form, not overlap | rule R43-SPLIT and `tools/absent-split.py`; shown able to fail by the flipped-row control (14/15) |
| byte-count nit — "265-char" and "267 bytes" were reported as if one of them were wrong | S077 capture `01f657b3d0ab045c494b3f92.txt` is 267 bytes and 265 Unicode characters | the round-42 spot-check, cosmetic | append-only erratum in `corpus/lessons/round-42.md`; the r42 sentence is not rewritten |
| prepared-as-dispatched — a validated spec with null agent ids was the round's wave evidence | `.ufo/waves/round-42/w1/swarm-registry.json` members have null agent ids; 0 seat reports | none until this round | QUALITY 61; a spec is not a dispatch. Shown able to fail: the r42 registry fails a check that requires a non-null agent id or a seat report |
| id-arithmetic — shifting every staged id by one would point the next citation at the wrong document | lane S077 is the pdftotext manual; staged S077 is the PRISMA-S DOI | item 10 of the lane addendum | adopted id S078 follows the Europe PMC URL, not S118+1 and not staged S078 |

## Gate

### Admitted

`corpus/knowledge/search-log-method-r39.md`, citing S078. The filename is the package's label. The source is the Europe PMC full-text XML of Bramer et al. 2018, opened from the committed capture, not fetched.

Located quote (12 words), access 2026-10-24: "to register the steps taken and to make searches accountable and reproducible."
URL: `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML`
Capture: `.qcache/2cef078d8f9f87802e19e770.txt`, sha256 `833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d`, byte offset 17383.

Also located in the same capture, not fetched: "Any change to the search strategy should be done in the log document" and "checking searches for their recall is advised".

### Rejected

- `search-log-fields-r36.md` (the three-literatures candidate). Reason: staged S077's local capture is a 267-byte / 265-character Client Challenge, not the PRISMA-S article, and the Japanese capture does not contain 参照日. A row that cites an unreopened source is not admitted. Flip: the fetch-scope ruling is answered and a capture of each cited source contains the quoted sentences.
- `search-tracking-record-r40.md`. Reason: "should be reported in Column 2" is not a contiguous span in the committed pdftotext capture, so the column claim cannot be re-grounded. Two other sentences in that capture are contiguous; they are not enough to admit the column claim. Flip: a rendering in which that sentence is contiguous.
- The rest of the package. Reason: one theme, and only the rows an admitted entry cites are appended. Flip: a later round re-grounds another theme from local captures, or the fetch ruling opens the rest.

### Registry changes

- S078 added: `queued` was not a prior state; the row is new, status `mined`, recheck `365d`, used-by `corpus/knowledge/search-log-method-r39.md`.
- No other row's status, recheck, or used-by changed.
- Staged recheck prose (`365d — re-open the Europe PMC...`) was stripped to `365d`. The prose is this Gate block, not a registry cell.
- used-by lists only the admitted entry. Staged S118's used-by was the same path; the citation inside the entry was re-pointed from S118 to S078 by the URL, not by adding one to 118.

### Id collision

Lane ids and staged ids collide on S077 only (`assimilation/collisions`). The indented-fixture guard (`  | S118 |`) produces a nonempty collision; a column-zero-only pattern misses that indented row (`assimilation/guard/`). Lane S077 stays the pdftotext manual. Staged S077 is not adopted. The adopted document (Europe PMC URL, staged id S118) is lane S078, the next free lane id. Staged S078 is the Cochrane chapter and is not this row; it must not be copied onto lane S078.

### Non-author spot-check

Pending. Seats this lane dispatches are still the lane.

## Sources census

Round-start: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`, exit 0, five W04 warnings (S051, S053, S073, S074, S075).
Scratch mirror before the append: `validate --file` on the mirrored registry plus the S078 row, exit 0, same five W04 warnings, no E03/E04.
Round-end: the root command again; recorded in the report.
