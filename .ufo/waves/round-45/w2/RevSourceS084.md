# RevSourceS084 — attack on row S084 (AVeriTeC train.json) at 5e8c7ad2f7b8254d83358820286e3d12ca4672d1

Seat: `L1Chousa45.RevSourceS084` (reviewer, leaf). Item: recount every figure in row S084's anchor and teaches cells from the on-disk capture with own code (no import of `c3-count.py`), confirm the capture sha256. No fetch, no lane writes, no subagents.

## Method

- Tree measured: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 5e8c7ad2f7b8254d83358820286e3d12ca4672d1 | tar -x -C /tmp/chousa-r45-RevSourceS084/tree` — row read from `corpus/SOURCES.md:94` (S084), entry read from `corpus/knowledge/evidence-snapshot-coverage-r40.md`.
- Capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/974299ae4b5f3bdb808b36a9.txt` (read-only). Recount scripts written from scratch (`/tmp/chousa-r45-RevSourceS084/recount.py`, `recount3.py`, `final.py`, `loc.py`); json parsed, counts computed independently.
- Verified recomputation of the frozen 7 counts also matches (`c3-count.py` rederive semantics reproduced independently): records 3068, evidence_with_field 6511, nonempty 6510, empty 1, claims_with_field 2531, nonempty 1145, empty 1386.

## Capture identity

`sha256sum` (my own, verbatim): `ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c`, 10,184,813 bytes — matches the row's recorded sha256 and `counts.json`. **HOLDS.**

## Verdict per figure (own code)

| Figure in row S084 | Claimed | My independent count | Verdict |
|---|---|---|---|
| records | 3,068 | 3068 (len of top-level JSON list) | HOLDS |
| answers naming a real source (source_url non-empty, not `Metadata`) | 7,572 | 7572 | HOLDS |
| of those, carry a web.archive.org link | 5,959 | 5959 (URL-host classification) / 5960 (raw substring) | HOLDS-narrowed (see below) |
| real-source answers with no `cached_source_url` key | 1,491 | 1491 | HOLDS |
| claim fields filled | 1,145 of 2,531 | 1145 non-empty of 2531 records carrying `cached_original_claim_url` | HOLDS |

### The one edge: 5,959 vs 5,960

Exactly one answer's `cached_source_url` contains the substring `web.archive.org` but is not a web.archive.org URL — a malformed doubled value: `https://web.archive.ohttps://web.archive.org/web/20210729025817/https://www.investopedia.com/articles/markets/120315/if-...` (record index 2923, question 0, answer 0; claim "Musician Prince invested in Nike in 1971."; its `source_url` is the same malformed string).

- Raw substring test `"web.archive.org" in cached_source_url` over the 7,572 real-source answers → **5,960**.
- URL-parsed hostname test (`urllib.parse.urlparse(...).hostname == "web.archive.org"`) → **5,959**.

The committed 5,959 is reproducible only with the well-formedness exclusion. The SOURCES.md row itself does not state the exclusion; the adopted entry does ("… and a tail of live or malformed addresses", `evidence-snapshot-coverage-r40.md` line 13). The difference is 1/7,572 ≈ 0.013%; the 78.7% figure checks out (5959/7572). Finding: definitional precision gap, not a fabricated count. If "carry a web.archive.org link" is read literally as substring occurrence, the row undercounts by one.

## Supporting cross-checks (same code, all match the entry)

- Partition of all 6,510 non-empty `cached_source_url` values: webarchive 5959, `Metadata` placeholder 429, archive.ph 41, perma.cc 27, archive.vn 6, other/live/malformed 48 → sum 6510. Matches `evidence-snapshot-coverage-r40.md` lines 13-15.
- 8 webarchive values wrap an archive.is/archive.md address (entry line 14; `counts.json` `web_archive_wrapping_archive_is_or_md: 8`).
- 1,968 answers lack the key; 386 unanswerable; 1,582 name a source_url (1,491 real + 91 `Metadata`); 520 `Metadata`-source answers, 429 with non-empty cached. All consistent.

## Resolvable pointers

- Row: `corpus/SOURCES.md:94` (S084) at 5e8c7ad2f7b8254d83358820286e3d12ca4672d1.
- Entry: `corpus/knowledge/evidence-snapshot-coverage-r40.md:3,10-21`.
- Capture: `.qcache/974299ae4b5f3bdb808b36a9.txt`, sha256 `ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c` (my recomputation).
- Malformed archive value: record index 2923 (0-based), question 0, answer 0.
- Off-by-one definition edge: 5,959 holds only under URL-host classification; raw-substring count is 5,960.

## Residual risk / gaps

- No external fetch performed (L0 `8d77e6c1` open); all reads from the on-disk capture.
- The 5,959 figure's exact predicate is not pinned in SOURCES.md; verdict rests on the entry's documented "malformed addresses" exclusion.
