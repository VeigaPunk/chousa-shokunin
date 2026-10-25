# Review of QUALITY 65 (round 45, wave 2) — RevQuality65

Item: QUALITY 65 in `corpus/QUALITY.md` at 5e8c7ad2f7b8254d83358820286e3d12ca4672d1 — "A corpus's archive coverage is counted by value, not by field." Attack targets: the three figures in its "Shown able to fail" sentence (5,959 of 6,510; 429 `Metadata`; 1,582 sourced answers without a key), the verbatim staged sentence it quotes, and whether 65 is checkable.

## Method
- Extracted committed tree: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 5e8c7ad… | tar -x -C /tmp/chousa-r45-RevQuality65/tree`; ran everything inside that tree.
- Independent recount (fresh script, same definitions as `corpus/evidence/round45/build-spans.py` lines 59–89) over the qcache capture `974299ae4b5f3bdb808b36a9.txt`; no lane file modified.

## Verdict: HOLDS-NARROWED
All three figures are exactly reproduced; the criterion is checkable; the quoted staged sentence is semantically exact but **not byte-verbatim** (hard line break + markdown bold delimiters inside the quoted span), so the "exists verbatim" claim is imprecise. The demonstration itself (staged sentence fails the value-count) holds.

## Evidence

### 1. Capture identity (counts.json vs on-disk capture)
```
CAPTURE_SHA256 ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c
COMMITTED_CAPTURE_SHA256 ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c
CAPTURE_BYTES 10184813 COMMITTED_BYTES 10184813
```
Matches counts.json `capture_sha256` / `capture_bytes`. (Capture path: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/974299ae4b5f3bdb808b36a9.txt` — outside the lane repo.)

### 2. Independent recount vs committed counts.json
`counts equal: True`; `extra equal: True` — every key reproduced:
```
OK evidence_nonempty      recomputed=6510 committed=6510
OK evidence_with_field    recomputed=6511 committed=6511
OK evidence_empty         recomputed=1   committed=1
OK filled_web_archive     recomputed=5959 committed=5959
OK filled_not_web_archive recomputed=551  committed=551
OK filled_metadata_placeholder recomputed=429 committed=429
OK sourced_answers_without_key recomputed=1582 committed=1582
OK real_source_answers_web_archive recomputed=5959 committed=5959
OK answers_without_key     recomputed=1968 committed=1968
(also records 3068, claims_with_field 2531, claims_nonempty 1145, claims_empty 1386,
 answers 8479, answers_with_source_url 8092, real_source_answers 7572,
 real_source_answers_without_key 1491, web_archive_wrapping_archive_is_or_md 8, all OK)
```
Defined as in build-spans.py: `filled` = non-empty `cached_source_url` values (6,510); `wb` = `^https?://web\.archive\.org/`; `src` = answers with truthy `source_url`; `real` = `src` minus literal `"Metadata"` source.

### 3. The three figures in QUALITY 65's "Shown able to fail"
- "5,959 of the 6,510 filled values are web.archive.org links" → `filled_web_archive` 5,959 / `evidence_nonempty` 6,510 ✓
- "429 are the literal `Metadata`" → `filled_metadata_placeholder` 429 ✓ (429 of the 551 non-WB values)
- "1,582 sourced answers that carry no archive key" → `sourced_answers_without_key` 1,582 ✓ (answers with `source_url` but no `cached_source_url` key; invisible to the field count `evidence_with_field` 6,511) ✓
- Staged sentence's "6,510 hold a non-empty archive.org URL" is refuted by the recount: only 5,959 hold web.archive.org URLs; 551 others are not web.archive.org links (429 literal `Metadata`; 122 other values incl. perma.cc, archive.ph/is/vn/md, domain-less strings, malformed URLs such as `web.archihttps://africacheck.org/…`, `Vhttps://…`, `web.archive.ohttps://web.archive.org/…`, `file:///…`, and a computation `38287801729.78*4.7`). So the value-count ≠ field-count, exactly as 65 claims.

### 4. "Staged sentence exists verbatim" check
Quoted phrase in QUALITY 65: `"6,510 hold a non-empty archive.org URL"` (line 607–608). In staged `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/evidence-snapshot-coverage-r40.md`:
```
 11:- **The per-citation binding is effectively universal.** Of the 6,511 evidence
 12:  entries in the file that carry `cached_source_url`, **6,510 hold a non-empty
 13:  archive.org URL and 1 is empty** (`S132`).
```
- `"6,510 hold a non-empty archive.org URL"` as contiguous bytes: **found at offset -1 (absent)**; `"6,510 hold a non-empty"` at offset 859; `"non-empty archive.org URL"` absent — the phrase is split by a hard line break between "non-empty" and "archive.org URL" (plus markdown `**` wrappers). Semantically unique and exact (one occurrence); byte-verbatim it is not. The committed lane copy `corpus/knowledge/evidence-snapshot-coverage-r40.md` also contains "6,510".

### 5. Checkability of criterion 65
- The Check names a committed recount over the capture: `build-spans.py` (committed at 5e8c7ad, lines 70–93) computes `counts` + `extra_not_frozen`; I reproduced all values with an independent implementation. Executable.
- Capture is referenced by sha256 pin in counts.json and is byte-identical on disk; deterministic recount. Executable given the host-mounted qcache path (the harness's established layout). Residual dependence: the capture itself is not in the lane tree; without the mounted `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/` file the check cannot run from the lane alone (but it is hash-pinned, so drift would be detectable).
- "Shown able to fail" is demonstrable and demonstrated: recount proves the staged sentence overstates the web.archive.org-link count (5,959 < 6,510). Verdict: 65 is a **checkable criterion** (not a slogan), with the one verbatim-quote nit above. No counter or predicate changes proposed (frozen claims respected).

## Tooling
No tools installed (used system python3 and bash read-only). No fetch, no lane writes.

## Pointers
- `corpus/QUALITY.md:600-611` (65 entry); quoted phrase at 607–608.
- `corpus/evidence/round45/counts.json` lines 7–15 (counts), 20–28 (`extra_not_frozen`).
- `corpus/evidence/round45/build-spans.py:59-93` (committed recount logic).
- Staged file `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/evidence-snapshot-coverage-r40.md` lines 11–13 (sentence at char offsets 859–1013; phrase split at ~914).
- Capture sha256: `ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c`.
