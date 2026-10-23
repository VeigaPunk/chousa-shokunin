# ScoutSourcesCensus — corpus/SOURCES.md census

Axes: operability (frozen validate runs, exit and every warning captured) and calibration (independent status and tier counts agree with census mode; the recheck-before-date list is the literal recheck column).

No installs. Read-only on production files. Access date 2026-10-23. UTC date from `date -u +%F`: 2026-10-23.

## Inputs

- Fleet `scripts/sources-census.sh`: sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`
- `chousa-shokunin/corpus/SOURCES.md`: sha256 `3281259a49ffd2dd3e95b1924d494db4229fb499d90991ff7aaea10ea08c18ab`

`wc -l corpus/SOURCES.md`: 247. Registry header `corpus/SOURCES.md:9-10`. Data rows `corpus/SOURCES.md:11-76` (S001-S066). `## Paths` at `corpus/SOURCES.md:78`.

## Validate

Command: `timeout 60 /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`

Exit 0. Stderr empty, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Stdout sha256 `eb4dde9b2cde81e8432e70d5b673f4fb3cb3bbac681e0382c4dfe25a1e49d98d`. Three lines, two warnings:

```
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

No E-codes. Receipts under `.ufo/waves/round-35/w2/ScoutSourcesCensus/` (`validate.stdout`, `validate.stderr`, `validate.exit`) and the same bytes at `/tmp/hyaku/chousa-r35/w2/ScoutSourcesCensus/`.

W04 pairs (fragment stripped, `scripts/sources-census.sh:600-604`):

- `corpus/SOURCES.md:60` S050 and `:61` S051 share `https://www.w3.org/TR/2017/REC-html52-20171214/syntax.html`.
- `corpus/SOURCES.md:62` S052 and `:63` S053 share `https://docs.python.org/3/library/socket.html`.

Search log already names this W04 (`corpus/SOURCES.md:131`). W-codes do not change status (`scripts/sources-census.sh:16-18`, `:32-33`). Exit 0 matches that.

## Counts

Registry-section pipe rows only. One gawk `-F'|'` command for status, one for tier.

Status: rows 66; mined 43; queued 19; rejected 4.

Tier: rows 66; A 60; B 1; C 5.

Cross-check (not the counting commands): `sources-census.sh census --root /home/vgpnk/Projects/shokunin chousa` exit 0 with the same six figures; fleet invalid tiers and statuses 0; fleet missing 0.

Non-A rows in `corpus/SOURCES.md`:

- :28 S018 tier B queued
- :24 S014 tier C rejected
- :25 S015 tier C rejected
- :26 S016 tier C rejected
- :35 S025 tier C rejected
- :37 S027 tier C queued

Rejected set is S014, S015, S016, S025.

## Recheck before 2026-10-23

Same registry parse. A row counts only when column 11 (`recheck`, `scripts/sources-census.sh:628`) matches `YYYY-MM-DD` and is strictly before `2026-10-23`.

Result: iso_dates 0; before_2026-10-23 0. No row has a recheck date.

Histogram of all 66 recheck cells: `365d` 30, `on-release` 29, `180d` 3, `90d` 4.

Separate check: `sources-census.sh overdue --today 2026-10-23 --root /home/vgpnk/Projects/shokunin chousa` exit 0, 0 overdue lines, 66 cadence lines. Stdout sha256 `eb3c38555a0e4223d769f533f9859caccb089e1db22454187cc607fc0692e88d` (3536 bytes). `Nd` and symbolic values are cadence, not stored dates (`scripts/sources-census.sh:34-37`, `:675-685`).

## Verdict

Validate exit 0. Warnings are only the two W04 lines. Status mined/queued/rejected = 43/19/4. Tier A/B/C = 60/1/5. No registry row has a recheck date before 2026-10-23.

## Limits

Counts follow the census section rule (0-3 leading spaces, Registry only). Cadence strings were not treated as calendar dates. No URL was re-fetched. C1 and C2 were not scored.
