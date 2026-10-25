# ScribeSearchLog — round 43, wave 1

Seat: chousa round-43 leaf scribe. Assigned work: quote the Round 43 search-log bullet in `corpus/SOURCES.md` and count included and excluded. No other seat's files were written.

Pins: measured commit `737f40b6aa8f37ffe2269db370fd6d65a720d9a8` (this seat's `git rev-parse HEAD` printed that hash; `git merge-base --is-ancestor` of that hash against HEAD exited 0). Subject file `corpus/SOURCES.md` working-tree blob `3c7811d07cd1b033b9a9a7e37b9a446f121abc94` equals `HEAD:corpus/SOURCES.md`. sha256 `1d4c5004beb48a4e3ba67715cd342d406f159f238de91407fe412a9d09209a7c`. `git status --porcelain` on `corpus/SOURCES.md`, `corpus/lessons/round-43.md`, and `corpus/knowledge/search-log-method-r39.md` printed no lines (`porcelain_done=0`).

Method: read-only. No fetch, no network, no production edit, no index or jj operation, no tool install. The only file written is this report.

## Axes

1. Operability — the Round 43 search-log bullet is one locatable committed line, quoted as printed.
2. Calibration — included and excluded are counted from that line's stated figures and from the names it enumerates; 1+2 is checked against identified/screened.
3. Depth — provenance is the blob, not a paraphrase; unrun C1/C2/C3 are not upgraded to execution evidence; adjacent lesson text is quoted, not folded into the bullet's denominator.

## Behavior

Extracted the single line in `corpus/SOURCES.md` that starts `- Round 43 `. Counted stated `included` / `excluded` integers, token occurrences, and backtick-named `Rejected` filenames on that line only. Cross-checked the lesson Gate's admitted and rejected bullets, and whether the three named knowledge paths exist in the lane. Did not re-run `c1-count.py`, `c2-count.py`, or `c3-count.py`.

## Quote

`corpus/SOURCES.md` line 250, the only Round 43 search-log bullet (`ROUND43_BULLET_COUNT=1`). One physical line, 1045 Unicode characters, 1053 UTF-8 bytes (the extra bytes are `—` and `参照日`). Quoted exactly as `print` emitted it:

```
- Round 43 (2026-10-24): question — what must a search log record, and which of those requirements can be re-opened from committed captures without a fetch? Where: the campaign's committed capture cache only; no URL was fetched (L0 `8d77e6c1` still open). Identified 3 candidate entries on the search-log theme, screened 3, included 1 (S078, Europe PMC full-text XML of Bramer et al. 2018, staged id S118 re-pointed by document), excluded 2. Rejected `search-log-fields-r36.md`: staged S077's capture is a 267-byte Client Challenge, and the Japanese capture does not contain 参照日. Flip: the fetch-scope ruling is answered and a capture of the cited article contains the quoted checklist items. Rejected `search-tracking-record-r40.md`: the column-allocation sentence is not a contiguous span in the pdftotext capture. Flip: a rendering where "should be reported in Column 2" is contiguous. Stop rationale: one opened capture contains the three located sentences; the other two entries cannot be re-grounded without a fetch or a cleaner rendering.
```

## Count

From that line only:

| Class | Count | What the line names |
|---|---|---|
| included | 1 | S078, Europe PMC full-text XML of Bramer et al. 2018, staged id S118 re-pointed by document |
| excluded | 2 | `search-log-fields-r36.md`; `search-tracking-record-r40.md` |
| identified | 3 | "3 candidate entries on the search-log theme" |
| screened | 3 | same denominator as identified |

Arithmetic on the stated integers: 1 + 2 = 3, and 3 = identified = screened. Token `included` occurs once. Token `excluded` occurs once. `Rejected ` occurs twice. `NAMED_REJECTED_COUNT=2`. The included parenthetical names one id (S078), not a knowledge filename.

The bullet does not name `search-log-method-r39.md`. That filename is the lesson's admitted entry and the S078 `used-by` cell (`corpus/SOURCES.md` line 88), not a second include.

## Gates

This seat's checks, observed:

- One Round 43 bullet, line 250, blob matches HEAD. Hold.
- Stated included = 1, stated excluded = 2, and the named dispositions are 1 and 2. Hold.
- 1 + 2 = 3 = identified = screened. Hold.

Not run by this seat, so not passed here:

- `python3 corpus/evidence/round43/c1-count.py` — unrun. Peer item `ReviewC1Rerun`.
- `python3 corpus/evidence/round43/c2-count.py` and `--flip S086` — unrun. Peer item `ReviewC2Rerun`.
- `python3 corpus/evidence/round43/c3-count.py` — unrun. Peer item `ReviewC3Rerun`.

The frozen claims file and `corpus/lessons/round-43.md` state those counters passed. That is a contract and a lesson sentence, not this seat's execution evidence.

## Touched surfaces

- Written: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScribeSearchLog.md` (this file).
- Read: `corpus/SOURCES.md`, `corpus/lessons/round-43.md`, `corpus/evidence/round43/claims.md`, and (read-only, outside the lane) `/home/vgpnk/Projects/shokuknow/merge/chousa/MERGE-REPORT.md`.
- Not written: lane production files, git index, jj state, fleet repo, sibling repos, `/home/vgpnk/Projects/shokuknow`, `LOG.md`.
- Tools installed: none. No pacman. No network.

## Out of scope

- Re-running C1, C2, or C3, or `tools/absent-split.py`.
- Retuning the 1/2 bound, or scoring R43-SPLIT.
- Admitting or rejecting knowledge files. The two excluded filenames are absent from the lane tree; that absence corroborates non-adoption, it is not the definition of the search-log count.
- The lesson's third Gate reject, "The rest of the package", is outside this bullet's denominator of 3. It is quoted below so the L1 can verdict the boundary. It was not added to excluded.
- Chinese-search-log rows in the campaign merge report (`chinese-search-log-r37.md` and its amendment). The bullet does not name them. They were not counted as part of the 3.

## Findings

### F1 — included 1, excluded 2

The bullet's own integers and its own names agree. Included is the one parenthetical (S078). Excluded is the two `Rejected` filenames. Stop rationale in the same line says "the other two entries", which matches excluded 2 and does not name a third screened entry.

### F2 — lesson Gate lists one extra reject that this bullet does not count

`corpus/lessons/round-43.md` admitted search-log line count observed by the second Python was 1:

```
`corpus/knowledge/search-log-method-r39.md`, citing S078. The filename is the package's label. The source is the Europe PMC full-text XML of Bramer et al. 2018, opened from the committed capture, not fetched.
```

Rejected bullets under `### Rejected` observed as 3. The first two are the bullet's excluded pair. The third is not one of the 3 screened entries:

```
- `search-log-fields-r36.md` (the three-literatures candidate). Reason: staged S077's local capture is a 267-byte / 265-character Client Challenge, not the PRISMA-S article, and the Japanese capture does not contain 参照日. A row that cites an unreopened source is not admitted. Flip: the fetch-scope ruling is answered and a capture of each cited source contains the quoted sentences.
- `search-tracking-record-r40.md`. Reason: "should be reported in Column 2" is not a contiguous span in the committed pdftotext capture, so the column claim cannot be re-grounded. Two other sentences in that capture are contiguous; they are not enough to admit the column claim. Flip: a rendering in which that sentence is contiguous.
- The rest of the package. Reason: one theme, and only the rows an admitted entry cites are appended. Flip: a later round re-grounds another theme from local captures, or the fetch ruling opens the rest.
```

No numeric disagreement inside the search-log bullet. The lesson's third reject is a different set. This seat does not fold it into excluded.

Adjacent precision, not a count defect: the bullet says "267-byte Client Challenge"; the lesson says "267-byte / 265-character". The bullet does not deny the character count.

### F3 — lane files match the disposition, and are not the count

Observed:

- `corpus/knowledge/search-log-method-r39.md` exists (the included row's used-by, not a name inside the bullet).
- `corpus/knowledge/search-log-fields-r36.md` does not exist.
- `corpus/knowledge/search-tracking-record-r40.md` does not exist.

File absence is corroboration only. The count is the bullet's.

## Conflicts

None inside the bullet: stated included 1, stated excluded 2, named rejected 2, identified 3, screened 3, and 1+2=3.

Recorded for the L1, not resolved by this seat: the lesson Gate's rejected section has 3 bullets, while the search-log bullet's excluded figure is 2. Verbatim texts are F2. If the L1 treats "The rest of the package" as a fourth screened search-log candidate, the bullet does not; it says identified 3 and names two excludes plus one include.

## Commands and observed output

1. Bullet extract, HEAD pin, and token count. Working directory `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

```
git rev-parse HEAD && git status --porcelain -- corpus/SOURCES.md corpus/lessons/round-43.md corpus/knowledge/search-log-method-r39.md && git log -1 --format='%H%n%s' -- corpus/SOURCES.md && git merge-base --is-ancestor 737f40b6aa8f37ffe2269db370fd6d65a720d9a8 HEAD; echo "ancestor_exit=$?" && git rev-parse 737f40b6aa8f37ffe2269db370fd6d65a720d9a8 && python3 - << 'PY'
... extract lines starting "- Round 43 ", print the line, count included/excluded tokens and Rejected filenames ...
PY
```

Stdout, verbatim:

```
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
round-43: split the absent class and adopt one locally re-opened search-log entry
ancestor_exit=0
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
ROUND43_BULLET_COUNT=1
FILE_LINES=277
FILE_BYTES=64314
LINE=250
LINE_CHARS=1045
LINE_BYTES=1053
---BULLET-BEGIN---
- Round 43 (2026-10-24): question — what must a search log record, and which of those requirements can be re-opened from committed captures without a fetch? Where: the campaign's committed capture cache only; no URL was fetched (L0 `8d77e6c1` still open). Identified 3 candidate entries on the search-log theme, screened 3, included 1 (S078, Europe PMC full-text XML of Bramer et al. 2018, staged id S118 re-pointed by document), excluded 2. Rejected `search-log-fields-r36.md`: staged S077's capture is a 267-byte Client Challenge, and the Japanese capture does not contain 参照日. Flip: the fetch-scope ruling is answered and a capture of the cited article contains the quoted checklist items. Rejected `search-tracking-record-r40.md`: the column-allocation sentence is not a contiguous span in the pdftotext capture. Flip: a rendering where "should be reported in Column 2" is contiguous. Stop rationale: one opened capture contains the three located sentences; the other two entries cannot be re-grounded without a fetch or a cleaner rendering.
---BULLET-END---
STATED_IDENTIFIED=3
STATED_SCREENED=3
STATED_INCLUDED=1
STATED_EXCLUDED=2
TOKEN_included=1
TOKEN_excluded=1
TOKEN_Rejected=2
NAMED_REJECTED_COUNT=2
NAMED_REJECTED=search-log-fields-r36.md
NAMED_REJECTED=search-tracking-record-r40.md
INCLUDED_PAREN=['S078, Europe PMC full-text XML of Bramer et al. 2018, staged id S118 re-pointed by document']
```

`git status --porcelain` for those three paths produced no lines between the two identical hashes. Exit of that combined command was 0.

2. Lane existence and lesson Gate bullets. A `printf '---lesson rejects---\n'` in the same shell failed (`printf: --: invalid option`) because the format began with `-`. The shell had no `set -e`, so the following Python still ran. That usage error is this seat's probe, not a lane result. Lesson numbers below are from that Python's stdout, not from the failed printf.

```
LANE_EXISTS corpus/knowledge/search-log-method-r39.md True
LANE_EXISTS corpus/knowledge/search-log-fields-r36.md False
LANE_EXISTS corpus/knowledge/search-tracking-record-r40.md False
MERGE_SEARCHLOG_ROWS=7
MERGE_ROW=| `corpus/knowledge/search-log-fields-r36.md` | new-file | round1 | What a search log must record, in three literatures | new file |
MERGE_ROW=| `corpus/knowledge/chinese-search-log-r37.md` | new-file | round2 | What a Chinese-language search record must carry | new file |
MERGE_ROW=| `corpus/knowledge/chinese-search-log-r37-amendment-2026-10-23.md` | new-file | round3 | The Chinese answer is a reception, not a standard | new file |
MERGE_ROW=| `corpus/knowledge/search-log-method-r39.md` | amendment | round4 | The search log as a working document, not a field list | **target already exists in the lane — append, do not replace** |
MERGE_ROW=| `corpus/knowledge/search-tracking-record-r40.md` | new-file | round6 | What PRISMA-S puts in a tracking record, and in which column | new file |
MERGE_ROW=| `S099` | corpus/knowledge/citation-count-semantics-r37.md | corpus/knowledge/citation-count-semantics-r37.md, corpus/knowledge/chinese-search-log-r37.md |
MERGE_ROW=| `S100` | corpus/knowledge/citation-count-semantics-r37.md | corpus/knowledge/citation-count-semantics-r37.md, corpus/knowledge/chinese-search-log-r37.md |
/bin/bash: line 22: printf: --: invalid option
printf: usage: printf [-v var] format [arguments]
LESSON_ADMITTED_SEARCHLOG_LINES=1
ADMITTED=`corpus/knowledge/search-log-method-r39.md`, citing S078. The filename is the package's label. The source is the Europe PMC full-text XML of Bramer et al. 2018, opened from the committed capture, not fetched.
LESSON_REJECTED_BULLETS=3
REJECTED=- `search-log-fields-r36.md` (the three-literatures candidate). Reason: staged S077's local capture is a 267-byte / 265-character Client Challenge, not the PRISMA-S article, and the Japanese capture does not contain 参照日. A row that cites an unreopened source is not admitted. Flip: the fetch-scope ruling is answered and a capture of each cited source contains the quoted sentences.
REJECTED=- `search-tracking-record-r40.md`. Reason: "should be reported in Column 2" is not a contiguous span in the committed pdftotext capture, so the column claim cannot be re-grounded. Two other sentences in that capture are contiguous; they are not enough to admit the column claim. Flip: a rendering in which that sentence is contiguous.
REJECTED=- The rest of the package. Reason: one theme, and only the rows an admitted entry cites are appended. Flip: a later round re-grounds another theme from local captures, or the fetch ruling opens the rest.
```

`MERGE_SEARCHLOG_ROWS=7` is a substring hit on "search-log" in the campaign merge report, not the bullet's identified-3. Five of those rows are knowledge-path rows; two are S099/S100 used-by cells. Not used as the count.

3. Blob identity.

```
sha256sum corpus/SOURCES.md corpus/lessons/round-43.md && git hash-object corpus/SOURCES.md && git rev-parse HEAD:corpus/SOURCES.md && git status --porcelain -- corpus/SOURCES.md corpus/lessons/round-43.md corpus/knowledge/search-log-method-r39.md; echo "porcelain_done=$?"
```

```
1d4c5004beb48a4e3ba67715cd342d406f159f238de91407fe412a9d09209a7c  corpus/SOURCES.md
ff8f54498ef7e8849a47e06cea1907a86b4720017fa3d1f87922a72a95f53adf  corpus/lessons/round-43.md
3c7811d07cd1b033b9a9a7e37b9a446f121abc94
3c7811d07cd1b033b9a9a7e37b9a446f121abc94
porcelain_done=0
```

## Known limits

- The count is a parse of the committed bullet plus a name enumeration on that line. This seat did not re-open captures or re-derive why those three entries were the identified set.
- C1, C2, and C3 were not executed here.
- The campaign merge report was read to see which filenames exist upstream. It is not the lane search log. Its seven substring hits are not included or excluded.
- No live URL was opened. The bullet's "no URL was fetched" sentence was not independently re-proved beyond the absence of a fetch in this seat.

## Artifact paths

- Bullet: `corpus/SOURCES.md` line 250, blob `3c7811d07cd1b033b9a9a7e37b9a446f121abc94`, sha256 `1d4c5004beb48a4e3ba67715cd342d406f159f238de91407fe412a9d09209a7c`, commit `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
- Adjacent lesson: `corpus/lessons/round-43.md`, sha256 `ff8f54498ef7e8849a47e06cea1907a86b4720017fa3d1f87922a72a95f53adf`.
- This report: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScribeSearchLog.md`.

Report: .ufo/waves/round-43/w1/ScribeSearchLog.md
