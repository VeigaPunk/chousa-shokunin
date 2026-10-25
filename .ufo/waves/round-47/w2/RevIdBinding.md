ATTACKS: staged-id→lane-row document binding for S097/S098/S099/S113/S114/S115 (SOURCES.append.md vs lane SOURCES.md S085/S090/S091/S092/S093/S094); staged-id survival in the two round-37 knowledge entries and lane rows; collision-check re-run vs committed assimilation/collisions; sources-census validate on chousa
VERDICT: holds

## 1. URL binding — all six staged ids bind to the lane row by URL equality
Extracted the URL from the source cell of each staged row (SOURCES.append.md) and each lane row (corpus/SOURCES.md), compared exactly:

- S097 → S085: https://fever.ai/dataset/fever.html == https://fever.ai/dataset/fever.html ✓
- S098 → S090: https://aclanthology.org/2026.findings-acl.19.pdf == same ✓
- S099 → S091: https://ojs.aaai.org/index.php/AAAI/article/download/29825/31432 == same ✓
- S113 → S092: https://arxiv.org/html/1803.05355 == same ✓
- S114 → S093: https://arxiv.org/html/2012.00614v2 == same ✓
- S115 → S094: https://aclanthology.org/2025.coling-main.108.pdf == same ✓

Reverse direction confirmed (lane row S085/S090/S091/S092/S093/S094 → staged matches S097/S098/S099/S113/S114/S115 respectively).

[INFERENCE] The URL is the binding key, matching the entries' own statements: claim-support-test-r37.md line 8 "the staged ids bind to the lane's S085, S090 and S091 by document (URL equality)"; amendment line 35 "Its three source ids were re-bound by document to this lane's S092, S093 and S094."

## 2. No staged id survives in the entries or in lane rows
- claim-support-test-r37.md: grep for `S(09[7-9]|1[01][0-5])\b` → no matches. S-ids present: S085, S086, S090, S091, S092 (all lane ids).
- claim-support-test-r37-amendment-2026-10-23.md: no staged-id matches; S-ids present: S092, S093, S094.
- Lane SOURCES.md rows S085–S094: scanned for S097/S098/S099/S113/S114/S115 → NONE.
- The staged ids still exist in assimilation/staged-ids (S097…S115 all present) — they are the append block, which is expected; they survive nowhere in lane documents.

## 3. Collision check — committed file is a faithful round-start snapshot; live state has grown (known, disclosed)
Re-run with the current live registry and staged file (same 0–3-space row pattern as the parser, `^ {0,3}\| (S[0-9]{3}) \|`):
- reg unique 94, staged unique 114, collision set: S082–S094 (13 ids).
- Committed file assimilation/collisions lists S082–S089 (8 ids). sha256 of the reconstruction using the committed reg-ids/staged-ids snapshots: 76b8703b409bd759b5833952352ced29df3d7021a2e668e4ff89d98a0db60dba — matches the committed file exactly (`sha256sum collisions`). The committed file correctly records the round-start intersection of 89 reg ids and 114 staged ids.
- The 13-id live collision set matches the calibration disclosed in w1/ScribeGateBlock.md lines 23 and 48 ("After S090–S094 are appended, staged S090–S094 also name different documents, so 13 ids collide; nothing was appended from the staged block as-is"). Not a defect: the file is a start-of-round artifact.
- guard-proof/collisions contains S097 and guard-proof/SOURCES.md an indented `  | S097 |` fixture row; guard-proof/collisions-col0 empty — the 0–3-space guard catches the indented row that a column-0 extractor misses, consistent with the 0–3-space pattern.

## 4. sources-census validate — exit 0, no E-findings, only pre-existing W04s
Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0. Findings: `chousa ok /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md` plus five W04 duplicate-url warnings (S051, S053, S073, S074, S075). The same five W04s appear unchanged in census-start.txt (run before the append) and census-after-append.txt, so the validate outcome is unchanged by this round's work.

## 5. Adjacent observation (out of assigned scope, noted)
The append block also contains rows duplicating other lane rows by URL: S120→S085 (FEVER dataset page, flagged in the staged row itself as mergeable), S127→S088, S121→S086, S122→S087, S128→S089, S139→S082. The six assigned pairs are the only ones with entries in the two round-37 knowledge files.

No tools installed; no fetch; no lane mutations; scratch not used (read-only checks).
