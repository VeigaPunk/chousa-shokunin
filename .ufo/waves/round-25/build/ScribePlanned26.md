# ScribePlanned26 — round-26 SCORECARD candidates (draft)

Scope: read-only drafting. Sources: `SCORECARD.md:1300-1303` (round-20 debt list), `corpus/evidence/round25-claims.md`, `corpus/evidence/round25-measure-before.log`, `corpus/lessons/round-24-verifier-spotcheck.md:17-18`, `corpus/knowledge/json-delimiter-r24.md:69-71`, `corpus/README.md:502-504`, `corpus/QUALITY.md:17-23`, `corpus/SOURCES.md` rows S001-S018. No gate or selftest run. Only grep/read and one bash awk over `SOURCES.md`.

## Findings

1. **Calibration miss in round-25 pre-registration (judged axis).** Criterion 6 binds `knowledge/` entries "admitted from round 24 on" (`corpus/QUALITY.md:17`). The three legacy entries named in claim 1 (`archives-verified-r9.md`, `audit-r11.md`, `gate-baseline-r8.md`) are pre-r24, so their missing `recheck:` is outside the bar. The 25/28 prediction and its `META_RECHECK_ABSENT` drifts would count out-of-scope entries as drift. Inference: the in-scope population is 4 (`citation-chain-fidelity-r24`, `claim-support-states-r24`, `contextual-source-admission-r24`, `json-delimiter-r24`); all 4 carry `source:`/`verified-at:`/`recheck:` (observed by grep of the header lines).
2. **S### row check is absent (round-25 debt), but the current data passes.** Counting the 9 cited (entry, S-id) pairs in the four r24 `source:` lines: each row's status (field 9) is `mined` and its `used-by` cell (field 12) contains the entry basename: 9/9 (observation, awk over `corpus/SOURCES.md`). The check that would catch a regression does not exist; spec v1 tests presence only (`round25-claims.md:36-37`).
3. **Concurrency residual is open.** `json-delimiter-r24.md:70-71`: the gate assumes one writer; `flock` is the candidate. Receipt `corpus/evidence/json-r24-20261019T213117Z-demo.log` §concurrency: run=3 `blank_lines=1` of 3 runs at 16 writers. `/usr/bin/flock` is present (util-linux 2.42.4, observed); no install performed.
4. **Trend furthest behind: freshness.** Across the SCORECARD round tables, freshness verdicts are 18 `unchanged`, 3 `improved narrowly`, 1 `improved` (23 rows; grep `| freshness |`). Calibration: 7 `unchanged`, 10 `improved narrowly`, 4 `improved`, 1 `improved (claim 3)`.
5. **Lowest measured axis: operability = 3/10** (`SCORECARD.md:7`, narrow archive observable only).
6. **Recheck computability.** `QUALITY.md:22-23`: a command-only `recheck:` leaves "overdue" uncomputable. The four r24 entries have dated/cadence values (`90d`, `365d`, `on-release`) yet no mode computes due dates. Next due for `90d` from `verified-at: 2026-10-19`: 2027-01-17 (inference: arithmetic only).

## Draft — `## Planned — round 26` (not pre-registered; for the round-25 landing)

Claims, 3, distinct axes, each with a before→after counting idea. Priority by judged axis, then lowest/furthest-behind.

1. **calibration (judged) — the metadata screen tests the bar, not presence.** Scope `verify-metadata` to criterion 6 (`knowledge/` admitted r24+) and add an S### row check (id exists, status `mined`, `used-by` names the entry). Before: spec v1 passes 3/3 planted controls (unknown `S999`; row `queued`; `used-by` omits the entry) as CLEAN; in-scope population flagged 28 instead of 4. After: controls 3/3 DRIFT; real pairs 9/9 clean; legacy entries reported `out-of-scope`, not drift. Append an erratum to round-25 (criterion 4), since its prediction counted out-of-scope entries.
2. **freshness (trend furthest behind: 18/23 `unchanged`) — first computed recheck due date.** `verify-metadata --as-of DATE` computes `verified-at` + cadence and prints `RECHECK_OVERDUE=N`; `on-release` counts `unscheduled`, not overdue. Before: 0/1 planted past-due control caught (no computation). After: 1/1 caught; real in-scope overdue at 2026-10-21 = 0 (next due 2027-01-17).
3. **operability (lowest scored, 3/10) — serialize concurrent appenders.** `flock` around probe+append in the `verify-all --json` path. Before: 1 blank line in 1 of 3 runs at 16 writers (`json-r24-…-demo.log` §concurrency). After: 10 runs × 16 writers, `blank_lines=0 glued_lines=0`, objects=16 per run. Named caveat: bash-3 / non-Linux portability stays debt.

## Installs and tools

None. `flock` observed present; no pacman, uv, npm, or binary installs.

## Not verified

No gate, selftest, or `round25-measure.sh` run (not assigned). Before-values above are observations of grep/awk output; "after" values are predictions, not measurements.

## Files written

- `.ufo/waves/round-25/build/ScribePlanned26.md` (this file, only write). Message sent: `ChousaR25Recovery.CriticClaim1-3` (finding 1 flag).

VERDICT: Round-26 draft = 3 claims (calibration-judged scope fix + S### row check; freshness computed recheck due; operability flock); finding 1 flags round-25 claim 1's 28-entry population as wider than criterion 6's r24+ bar.
