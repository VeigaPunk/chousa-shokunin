# R89ScribeLesson — round-89 settlement draft (scribe seat)

Lane `chousa`, round 89. Base `f8fa55ec`, claim freeze `ac0a0892c15de11fb28d3208f2b287687c00477e`. L1 `ChousaR89`
holds the canonical planner seat, the freeze and the integration; this seat drafts the lesson, the L1 integrates.

**Artifacts written (both under my seat folder, nothing else touched):**

- `.ufo/waves/round-89/w1/R89ScribeLesson/lesson-settlement-draft.md` — the settlement draft with the five required
  sections (`## Gate`, `## Claim outcomes`, `## Mistakes`, `## Spot-check intake`, `## Trends`) plus a
  `## Findings on the L1's own draft` section for the integrator.
- `.ufo/waves/round-89/w1/R89ScribeLesson/receipts/` — 22 receipt files, every one cited in the draft.

No production file was edited, no git/jj mutation was made in the lane or the fleet, no commit or push, no fetch.

## What I ran (every command, its receipt, the observed line, the exit code)

All trees were built at the freeze revision in my scratch (`/fast/scratch/hyaku/chousa-r89/R89ScribeLesson/`), which
was deleted before this report was written.

| # | command | receipt | observed | exit |
|---|---|---|---|---|
| 1 | `python3 -B corpus/evidence/round89/gate-records-r89.py --root <clone> --repo <clone> --work <scratch>` | `receipts/r1-c1-landing.txt` | `LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16` / `GATE_RECORDS_R89=PASS` | 0 |
| 2 | `python3 -B corpus/evidence/round89/mutate-r89.py --root <clone> --repo <clone> --work <scratch>` | `receipts/r2-c1-mutants.txt` | `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2 EQUIVALENT_ON_TREE=0/0 TOTAL=13/13` | 0 |
| 3 | `python3 -B corpus/evidence/round89/harm-recheck.py --root <clone> --repo <clone> --base-tool <scratch>/base-tool.py` | `receipts/r3-c1-harm.txt` | `HARM_RECHECK files=13 records=29 moved=0 base_rc=0 r88_rc=0` | 0 |
| 4 | `python3 -B corpus/evidence/round89/curation-r89.py --root <clone>` | `receipts/r4-c2-landing.txt` | `WARRANT_OK=17/17 DUP_QIDS=0 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=8/8` / `CURATION_R89=PASS` | 0 |
| 5 | `python3 -B corpus/evidence/round89/curation-r89-controls.py --root <clone> --work <scratch>` | `receipts/r5-c2-controls.txt` | `FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7` / `CONTROLS=PASS` | 0 |
| 6 | `python3 -B corpus/evidence/round89/curation-r89-mutants.py --root <clone> --work <scratch>` | `receipts/r6-c2-mutants.txt` | `MUTANTS_KILLED=6/6 COUNTER_DETECTED=5 BATTERY_DETECTED=1` | 0 |
| 7 | `bash corpus/evidence/round89/controls/run-controls.sh <clone> <scratch>` | `receipts/r7-run-controls.txt` | `RECEIPT_OK` × 8 / `CONTROL_RECEIPTS=PASS` | 0 |
| 8 | `python3 -B tools/gate-records.py verify --root <lane> --repo <lane> <my draft>` | `receipts/r10-gate-verify.txt` | `GATE_RECORD …:22 S216 OK` / `…:24 S218 OK` / `files=1 records=2 ok=2 fail=0` | 0 |
| 9 | `bash tools/research-gate.sh --selftest` | `receipts/r13-gate-selftest.txt` | `RESEARCH_GATE_SELFTEST: PASS (283 cases, 0 skipped)` | 0 |
| 10 | `sha256sum -c` over `corpus/evidence/round89/instrument-pins.txt` | `receipts/r15-instrument-pins.txt` | `OK` × 10 (nine round-89 files + the unchanged `tools/gate-records.py`) | 0 |
| 11 | `python3 scripts/hyaku/prefile-falsification.py --lane chousa --round 89` | `receipts/r12-prefile-check.txt` | `FINDING wave-missing …/w1-results.json` / `PREFILE-FALSIFICATION: SETUP findings=1` | 2 |

Receipts 1–6 are **byte-identical** to the committed `corpus/evidence/round89/controls/receipts/*.txt` (diffed
line-for-line against `receipts/lane-*.txt`, local copies of the committed files) — the round's own receipts are
reproducible from the freeze bytes.

Four demonstration probes, each re-applying a **pre-fix shape to the landed bytes** to show the fix is able to fail:

| # | pre-fix shape re-applied | receipt | observed |
|---|---|---|---|
| d1 | single-point mutant on a healthy tree (leg's `ok` forced `True`, measurement intact) | `receipts/d1-single-point-mutant-probe.txt` | `LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15` / `GATE_RECORDS_R89=PASS` — **survives**, exit 0, no `UNRECONCILED`/`UNCROSSCHECKED` |
| d2 | mirror fixture id reverted from the unused `S219` to the real registry row `S099` | `receipts/d2-last-wins-probe.txt` | last-wins keeps the ERIC row, the mirror's `supersedes S031` edge vanishes (`[]`), and the battery prints `CASE_DEVIATION SUP-clause-mirror` / `FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=0/7` / `CONTROLS=FAIL`, exit 1 |
| d3 | summary cell's denominator re-pointed at `EXPECTED_LEGS` | `receipts/d3-summary-denominator-probe.txt` | `… LEGS_MEASURED=15/16` beside `GATE_RECORDS_R89=PASS`, exit 0 |
| d4 | `UNCROSSCHECKED` diagnostic looking the leg name up in the summary-field map, with the `E7d` shape | `receipts/d4-nonexistent-key-probe.txt` | `UNCROSSCHECKED D1_WIDTH detail=3/3/3 pin3 summary_fields=-` (placeholder on both legs) |

Two further probes I ran for my own verification of the wave's C1 findings (not part of the four required mistakes):
`receipts/d5-legs-measured-hole.txt` (a one-point forge of the printed cell `LEGS_MEASURED=0/15` still prints
`GATE_RECORDS_R89=PASS`, exit 0 — the reviewer's F1) and `receipts/d6-counting-command-verbatim.txt` (the frozen
three-line counting command run verbatim prints `HARM_RECHECK files=13 records=29 moved=29 base_rc=2`, exit 1 — the
reviewer's F2; the `expected.tsv` recipe produces `moved=0`).

## Gates and behaviour

- **C1 (`C1-BATTERY-R89`) — held on the predicate, but the wave fired C1 on two wording clauses** (`R89ReviewerC1`
  F1 the unbound `LEGS_MEASURED` cell, F2 the counting command that cannot produce `moved=0`; `R89SentinelScope`
  B1 the driver that overwrites each receipt before grepping it). My re-measurement confirms both: d5 and d6 above.
  Neither is a claim-falsification I can adjudicate — they are routed to round 90 by `plans/round-89.md` Amendments 4
  and 5, and the lane published them rather than arguing them away.
- **C2 (`C2-CURATION-R89`) — held on the predicate**; the wave fired C2 on wording (the printed `VERDICT
  fields_hold=1` token does not exist on the passing path; the "nine legs" phrasing against `LEGS_MEASURED=8/8`),
  routed by Amendment 8, plus the mutation battery's two single-expression detector substitutions (Amendment 9).
- **Routed defects 1–7 closed, 8 carried** (operator-owned). Row-by-row dispositions with pointers are in the
  draft's `## Spot-check intake`.
- **Seat discipline:** all eleven wave report files ship at least one `VERDICT:` line, but `R89ReviewerC2.md:75`
  ships `VERDICT: build R89ReviewerC2 C2 fired` — the seat token is `build`, not `R89ReviewerC2`, so a parser keyed
  on the second field reads the seat as `build`. Tally: 11 distinct seat tokens for 12 spec seats (the twelfth is
  this scribe's own report). Receipt `receipts/r11-seat-trailers.txt`.

## Findings on the L1's own draft (for the integrator)

1. **`LEGS_MEASURED=8/9` is a misquote.** `corpus/lessons/round-89.md:57` and `plans/round-89.md:178` (Amendment 8)
   both quote the C2 summary cell as `LEGS_MEASURED=8/9`. The instrument prints `LEGS_MEASURED=8/8`
   (`curation-r89.py:293` builds `sum(ok)/len(legs)` over the eight legs that exist when the cell is built;
   `EXPECTED_LEGS = 9` is the expected total, not the printed denominator). The committed receipt and the sentinel's
   own finding both say `8/8`. Receipt `receipts/r14-draft-misquotes.txt`. This is the round's own criterion 192
   (a summary field that reports a total it does not hold) applied to the lesson that mined it.
2. **"Four criteria mined (QUALITY 190–193)" — six were mined.** `grep -cE '^19[0-9]\. ' corpus/QUALITY.md` → **6**
   (190, 191, 192, 193, 194, 195). The same class as round-88's `## Corrections` 2. Same receipt.
3. **One malformed seat trailer** (above). Same receipt.

## Trends I can support from receipts

- **expansion: unchanged** — 97 knowledge `.md` files at base and at the freeze; registry 218 rows at both; only the
  two `used-by` cells moved (`receipts/r8-registry-diff.txt`).
- **quality: improved** — six routed repairs, each with a failable witness this seat re-measured
  (`receipts/r2`, `r5`, `r6`, `r7`, `r3`); pins and the gate selftest pass (`r15`, `r13`); six criteria mined.
- **discernment: improved** — the wave fired the sentence rather than the predicate on several clauses and each
  firing became a numbered plan amendment (`.ufo/waves/round-89/claim-falsification.tsv`, 23 rows at the time of this seat's run); the round's own
  four pre-freeze errors are mined with each fix shown able to fail (`d1`–`d4`); and my independent re-measurement
  reproduces every committed receipt byte-for-byte.

## Out of scope (not touched, not adjudicated)

- The wave's C1/C2 firings are routed, not adjudicated here: `R89ReviewerC1` F1–F7, `R89ReviewerC2` B1–B5,
  `R89SentinelScope` B1–B5, `R89MutBattery` S1–S7, `R89CriticClaims`' wording narrowing, `R89ScoutRegistry`'s
  114/114 campaign-id collision. The lesson's `## Mistakes` rows 5–7 in the L1's draft (the two wave-captured
  classes) are the L1's rows; my four rows are this round's own pre-freeze errors, as specified.
- No claim text, plan amendment, registry cell or instrument byte was edited by this seat.

## Tooling

No tool was installed or upgraded this round; `python3` (3.14), `git`, `bash`, `sha256sum`, `tar` and the lane's own
`tools/gate-records.py` and `tools/research-gate.sh` were sufficient. The pacman guard (all pacman transactions
paused host-wide, operator ruling 2026-10-20) was not exercised: nothing needed installing.

VERDICT: R89ScribeLesson C1 held — the frozen C1 predicate reproduces byte-for-byte at `ac0a0892` (`GATE_RECORDS_R89=PASS` with `LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16`, `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2`, `moved=0`), while the wave's two C1 wording fires (the unbound `LEGS_MEASURED` cell and the counting command that cannot produce `moved=0`) are confirmed by my own probes and routed to round 90.
VERDICT: R89ScribeLesson C2 held — the frozen C2 predicate reproduces byte-for-byte at `ac0a0892` (`CURATION_R89=PASS` with `DUP_QIDS=0 WARRANT_OK=17/17 QUOTES_LOCATED=20/20 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0`, `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7`, `MUTANTS_KILLED=6/6 COUNTER_DETECTED=5 BATTERY_DETECTED=1`), with the wave's C2 wording fires routed as Amendments 8 and 9.
