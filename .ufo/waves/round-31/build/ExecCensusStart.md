# ExecCensusStart — frontier-step census at round start (wave 1 build)

Date: 2026-10-23. Lane: chousa-shokunin @ SOURCES.md commit fc97f43b8e4a5cc8797d8c0f7dbf8fd2dfb07872.

## Ran
1. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` (timeout 600) — exit 0; stderr empty. stdout:
   - `chousa\tW04\tS051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes`
   - `chousa\tW04\tS053 duplicate url docs.python.org/3/library/socket.html across scopes`
   - `chousa\tok\t/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md`
2. Same script, `census` mode (timeout 600) — exit 0; stderr empty. stdout (chousa = FLEET, only lane targeted):
   - `rows 56`; `tier.A 50`, `tier.B 1`, `tier.C 5`, `tier.invalid 0`
   - `status.mined 33`, `status.queued 19`, `status.rejected 4`, `status.invalid 0`; `missing 0`
3. Manual census (Python parse of `## Registry`; NF=13 per contract incl. lead/trail empties): rows 56; malformed 0; tier A/B/C = 50/1/5; status mined/queued/rejected = 33/19/4 (other 0); no duplicate ids; ids S001–S056 no gaps; **next free id S057**; recheck column: on-release 23, 365d 26, 90d 4, 180d 3 — no ISO dates, so **0 rows with recheck date ≤ 2026-10-23** (NNd cadences due opened+N d; earliest due 2027-01-16).

## Verdict
Validate clean (exit 0, only the two known W04 cross-scope duplicate-URL warnings, S051/S053, matching the round-30 search-log note). Census and manual counts agree exactly. Frontier step: 56 sources, next id S057; no row currently due for recheck.

## Artifacts (evidence)
- `validate.stdout`, `validate.stderr`, `census.stdout`, `census.stderr` — raw outputs
- `sources-census.sh` — copy of the script used
- `manual-census.txt` — full manual census method + numbers
All under `.ufo/waves/round-31/build/ExecCensusStart/`.

## Limits
- Reflected only the chousa registry (fleet-level `FLEET` rows identical by construction of the single-lane run).
- Recheck due-date interpretation: ISO dates absent; NNd cadences counted by contract (opened + N days); symbolic `on-release` is not a date.
- No tools installed/updated (no tooling change needed); no network used; read-only git (one `git log`).
