# Round 25 — ScribeQualityCriteria (draft criteria 13–14)

Seat: ChousaR25Recovery.ScribeQualityCriteria-3 (writer). Base `b820e4e40ce52deedf53b191140cd7b08ddda929`.
Clone: `/tmp/chousa-r25-ScribeQualityCriteria`, branch `r25-ScribeQualityCriteria`, commit `861f7ba`
(uncommitted in live lane; no git/jj mutation there). Installs: none.

## Behavior
Appended `## Round-25 additions` to `corpus/QUALITY.md` after criterion 12: criterion 13 (runnable
`recheck:`, binds `knowledge/`) and criterion 14 (`## Spot-check intake`, binds `lessons/`). Each cites
its motivating debt and carries a one-line check. Criteria 1–12 untouched: `git diff --numstat b820e4e HEAD`
→ `33 0 corpus/QUALITY.md` (33 insertions, 0 deletions). File now 88 lines.

## Checks run (read-only; exit 0 = criterion holds)
Criterion 13 check, base file (live lane, identical in clone):
```
$ ! grep -nE '^recheck:.*--root +"?[^/$"]' corpus/knowledge/citation-chain-fidelity-r24.md
5:recheck: 90d (`bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..` confirms ...
CHECK13 live rc=1
```
Criterion 14 check, base file (live lane and clone):
```
$ grep -qx '## Spot-check intake' corpus/lessons/round-24.md; echo rc=$?
CHECK14 live rc=1
```
Discrimination controls (scratch `/tmp/r25-fx-*.md`): `--root "$SHOKUNIN_ROOT"` → rc 0 (pass);
`--root ..` → rc 1 (fail); `--root //` inside backticks → rc 0 (pass, absolute).

## Findings (path:line or command+output)
1. Debt "citation-chain recheck needs the fleet root as --root" is confirmed live at
   `corpus/knowledge/citation-chain-fidelity-r24.md:5`. The same defect is wider than the debt names:
   `corpus/knowledge/archived-export-intake.md:4` and `:19` both carry `--root ..`
   (`grep -rnE '^recheck:.*--root +"?[^/$"]' corpus/knowledge/` → 3 hits). Criterion 13 names them as
   debt queued to round 25; this draft does not edit them (criterion 4: errata append-only).
2. Debt "the lesson template should carry a spot-check slot" is confirmed: `corpus/lessons/round-24.md`
   has `## ` headings Mistakes / Unlearned before this round / Gate / What the round learned — no intake
   section. Criterion 14 disposes the three r24 debts in `lessons/round-25.md` (not yet written by this seat).
3. Debt 1 of `corpus/lessons/round-24-verifier-spotcheck.md:17` ("concurrent-append blank-line residual")
   has no criterion in 13–14. It stays unbound; a later round must name it or refuse it.
4. Gate root default is `CHOUSA_ROOT`, not `SHOKUNIN_ROOT`: `tools/research-gate.sh:278`
   `ROOT=${CHOUSA_ROOT:-$PWD}`. Criterion 13 therefore names `--root "$SHOKUNIN_ROOT"` explicitly; the
   gate does not read `SHOKUNIN_ROOT` itself (observation, not run).
5. Open gap: the r24 recheck's record path `corpus/fixtures/chain-r3.md` is cwd-relative. The one-line check
   covers only the `--root` argument; criterion 13 says so and leaves path-prefixing to a reviewer.
6. Legacy form not matched by the check: `corpus/knowledge/audit-r11.md:22` (`recheck (from the lane cwd ...`,
   no colon; M-13). Named here, not bound.
7. Criterion 14's check tests presence only. Per-debt coverage is a reviewer read; the criterion says so.

## Touched surfaces
- Clone only: `corpus/QUALITY.md` (appended; commit `861f7ba`).
- Live lane: this report only, `.ufo/waves/round-25/build/ScribeQualityCriteria.md`.
- Scratch: `/tmp/r25-fx-ok.md`, `/tmp/r25-fx-bad.md`, `/tmp/r25-fx-abs.md`.

## Files written, sha256
- `/tmp/chousa-r25-ScribeQualityCriteria/corpus/QUALITY.md`
  `0967438a26e20e9f849110946b6ed49cf205a712f550d1b9b0ab70c45a4b09e5`

## Out of scope / not done
- `corpus/lessons/round-25.md` (intake disposition of the three r24 debts) — Frontier step, not this item.
- Repair of `archived-export-intake.md:4,19` and `citation-chain-fidelity-r24.md:5` — queued r25 (erratum route).
- Gate not re-run; the selftest was not run (no gate code touched).

VERDICT: criteria 13–14 drafted and appended (clone commit `861f7ba`, +33/−0); both checks exit 1 on their named base files, live and in clone; criterion 13 leaves the `--root` regex as its only automated test and debt 1 of the r24 spot-check unbound.
