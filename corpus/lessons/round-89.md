# Round 89 — per-format leg reconciliation and a field-derived curation verdict; the round-88 wave's four survivor shapes close (2026-11-08)

Base `f8fa55ec` (round-88 landing + its non-author spot-check). Frozen claims in `corpus/evidence/round89/claims.md`
and `.ufo/waves/round-89/claims.json`; plan and pre-freeze repairs in `plans/round-89.md`. Round 88's non-author check
routed eight defects; this round closes 1–7 (8 is operator-owned and carried). One v1 wave, 12 seats, 0 dead.

## Gate

No fetch this round; no registry row opened, re-anchored or re-opened. The two rows this round's claims cite were
**re-opened from committed bytes** (S216's capture, S218's repo files), and their `used-by` cells were extended
old→new with `corpus/evidence/round89/claims.md` (S216: `corpus/evidence/round86/claims.md,
corpus/evidence/round87/claims.md` → the same plus round 89; S218: `corpus/evidence/round87/claims.md` → the same plus
round 89). No other cell moved: `git diff <base> <freeze> -- corpus/SOURCES.md` is exactly two lines, both in the last
cell. Registry 218 rows at both revisions; census exit 0 at start and end with the same five pre-existing `W04`
warnings (`corpus/evidence/round89/census-start.txt`, `.ufo/waves/round-89/census-end.txt`).

GATE-RECORD S216 url=https://www.rfc-editor.org/rfc/rfc9110.html fetched=2026-11-08T06:50:40Z tier=A decision=admit capture=corpus/captures/b1b13a12aee75c6ecc20fb91.txt capture_sha256=ec14fa3499c2dfbcf3f08f5e50cb623fa268bd1066d34e5ea710c23f0a46794e words=22 quote="indicates that the request was successful but the enclosed content has been modified from that of the origin server's 200 (OK) response"

GATE-RECORD S218 rev=ac0a0892c15de11fb28d3208f2b287687c00477e path=corpus/QUALITY.md line=1120 words=11 quote=A frozen `teaches` cell is not evidence; the superseding row's is.

- **S216** (RFC 9110 §15.3.4, section "203 Non-Authoritative Information"): the located sentence is the ground for
  binding the two 203 classes to `203` rather than to `2xx` or to `200` — a 203 is a *successful* response whose body
  is not the origin's, so an admit record claiming OK content and a reject record claiming a failed transfer are both
  refusals. Re-opened at the committed capture, not fetched: the refetch row is round 87's
  (`corpus/evidence/round57/refetch.tsv:185`, `http_code=200`).
- **S218** (own-work: `corpus/QUALITY.md` criterion 178 + `CORPUS.md` rule 2): the rule the `TEACHES` and
  superseder-own-read legs enforce — a superseded row's frozen `teaches` is not evidence, and only `status`,
  `recheck` and `used-by` may change in place. Re-opened at the freeze revision so the line number cannot move under
  the integration commit.

Verified: `python3 -B tools/gate-records.py verify --root . --repo . corpus/lessons/round-89.md` →
`GATE_RECORDS files=1 records=2 ok=2 fail=0`, exit 0 (`corpus/evidence/round89/controls/receipts/gate-records-round89.txt`).

Registry changes, old→new (CORPUS rule 2): the two `used-by` cells above; no status, recheck, anchor or teaches cell
changed. One entry cell was **not** edited this round (round 88's disclosed `Q1, Q3 (S215)` → `Q1 (S215)` repair
stands; `git diff <base> <freeze> -- corpus/knowledge/` is empty).

No egress table was required: `SKILL.md` `## Boundaries` says "A window without an approval table is loopback-only",
and this window was loopback-only (the sentinel's item (a) receipt: zero refetch rows newer than the freeze, zero
captures newer than the freeze commit).

## Claim outcomes

Both claims are scored on the freeze bytes and then attacked by the round's wave. At the freeze `ac0a0892`:

- **C1 operability** — `GATE_RECORDS_R89=PASS`, exit 0:
  `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362 EMPTY_REFUSED=1/1
  RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 DIV3=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3
  MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS_MEASURED=15/15`
  / `LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16`; mutants `MUTANTS_KILLED=11/11
  TOOL_MUTANTS_CAUGHT=2/2 TOTAL=13/13`; harm `HARM_RECHECK files=… records=… moved=0`
  (`corpus/evidence/round89/controls/receipts/c1-landing.txt`, `c1-mutants.txt`, `c1-harm.txt`). Before: the round-88
  battery on the same tree prints `GATE_RECORDS_R88=PASS` with no `CROSSCHECK` field and accepts all four survivor
  shapes (`c1-prior-instrument.txt`; non-vacuity is the mutant battery).
- **C2 calibration** — `CURATION_R89=PASS`, exit 0: `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1
  QUOTES_LOCATED=20/20 Q_FLOORS=… WARRANT_OK=17/17 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1
  TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=8/9` / `CURATION_R89=PASS`; controls
  `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7`; mutants `MUTANTS_KILLED=6/6 COUNTER_DETECTED=5
  BATTERY_DETECTED=1` (`c2-landing.txt`, `c2-controls.txt`, `c2-mutants.txt`). Before: the round-88 counter on the same
  tree prints `CURATION_R88=PASS` with no `DUPQID` leg, no field-derived verdict and a dead superseder clause
  (`c2-prior-instrument.txt`).

## What the instruments measure, and what they do not

C1's `rederive()` reads four grammars and the summary cross-check closes the leg-vs-field gap in both directions;
`DIV3` is printed so the third width derivation is checkable from the summary rather than only from the leg's own
string. Named limits, unfixed at the measured width: a **joint** rewrite of the leg writer, the receipts and the
reconciliation survives (that edit is the counter); `TOOL`'s witness is the filesystem, not a number; and a leg
computed from a wrong constant and printed honestly passes — the reconciliation certifies agreement, not the truth of
the expression that produced both sides.

C2's verdict now follows from the printed tallies, so a dead detector and a detached leg both fail; the `DUPQID` leg
rejects a qid cited twice on one warrant cell; and the superseder-own-read clause matches the raw cell, with the
battery's `SUP-clause-mirror` as its non-vacuity witness because **no real superseding row names a date term**
(`SUP_CLAUSE_CHECKED=0`). Named limits: `MIN_TOKENS = 7` is a measured floor, not a content check; the qid-set pin
guards label identity, so swapping two pinned rows' quote texts still passes; row reorder passes (benign).

## Mistakes

1. **Class: a mutant that breaks a measurement without detaching the leg that hides it proves nothing.** The first
   `E7c`/`E7b` I wrote replaced only the leg's `ok` with `True` on a *healthy* tree, so the detail still re-derived
   `True` and both mutants SURVIVED — a healthy-tree constant is the round-88 `A3` shape, not a detachment.
   **Evidence pointer:** the first `mutate-r89.py` run, `SURVIVOR E7c-width-detached`, `SURVIVOR
   E7b-mutant-detached`, `SURVIVOR E7d-width-detail-forged` (three of eleven). **Captured-by:** none — QUALITY 185
   ("a verdict is accounted, not conjoined") covered leg accounting but not mutant *construction*.
   **Fix:** a mutant carries a list of edits — a broken measurement **plus** the detachment — and the fixed battery
   prints `UNRECONCILED D1_WIDTH detail=3/3/1 pin3 receipt_ok=True rederived=False` for `E7c` and
   `UNRECONCILED MUT_ADMIT detail=derived=0 killed=0` for `E7b`; shown able to fail by re-applying the single-point
   form, which is still a survivor.
2. **Class: a mirror fixture id that collides with a real registry row is silently discarded by last-wins.** The
   superseder-clause mirror inserted `| S099 | … | mined | … |` while S099 is a real ERIC row further down
   `corpus/SOURCES.md`, so `parse_registry`'s `reg[cells[0]] = cells` kept the real row and the mirror's disposal edge
   vanished — the battery reported `CASE_DEVIATION … refus` for the wrong reason. **Evidence pointer:** a probe
   printing `S099 in reg: True` with the ERIC title, and the edge list showing no `S219`-shaped edge.
   **Captured-by:** none — the census validates the real registry, never a scratch mirror. **Fix:** the mirror uses
   the next unused id (S219) and the battery's positive case would fail loudly if the edge were missing; shown able
   to fail by reverting the id to S099, which reproduces `CASE_DEVIATION`.
3. **Class: a summary field printed before the leg that completes it exists reports a false denominator.** The first
   run printed `LEGS=15/16` beside `GATE_RECORDS_R89=PASS`, because the `SUMMARY` leg is appended after the summary
   string is built; a reader would see a verdict claiming 16 legs while the summary counts 15. **Evidence pointer:**
   the first landing run's line `… LEGS=15/16`. **Captured-by:** none — the `RECONCILED` total included `SUMMARY`, so
   no leg failed. **Fix:** the summary prints `LEGS_MEASURED=n/n` over the legs that exist when it is built, and the
   verdict line carries `LEGS_APPENDED`; shown able to fail by `E7g-receipt-removed`, which prints
   `LEG_FAIL SUMMARY 14/14` and `UNRECONCILED SUMMARY`.
4. **Class: a diagnostic line that names a key which never exists.** The cross-check's `UNCROSSCHECKED` line printed
   `summary_fields=-` because it looked up the *leg* name (`D1_WIDTH`) in a dictionary keyed by summary fields — a
   diagnostic that reads as "no summary field" on every failure, including the intended ones. **Evidence pointer:**
   `UNCROSSCHECKED D1_WIDTH detail=3/3/3 pin3 summary_fields=-` in the `E7d` receipt. **Captured-by:** none.
   **Fix:** `crosscheck()` returns a note naming the cells it compared
   (`D1_FORGES=3 D1_EXPECTED=3 DIV3=1 pin=3/3`); shown able to fail by the `E7d` receipt, whose note names `DIV3=1`
   against the leg's forged `div3=3`.

5. **Class: a printed summary cell that no leg cross-checks is a false field.** `LEGS_MEASURED` was the only one of
   19 printed cells outside the `crosscheck()` map, so a one-point edit rendering `LEGS_MEASURED=0/15` still printed
   `PASS` while the `SUMMARY` receipt read `15/15`. **Evidence pointer:** `R89ReviewerC1`
   `legs-measured-forge.txt`, `variants/lg-legs-measured-14of15.py`. **Captured-by:** QUALITY 193 (a diagnostic names
   the compared value) covers failure *lines*, not uncompared *fields*; none covered coverage of the printed surface.
   **Fix:** routed to round 90 as a one-line comparison against the `SUMMARY` receipt (plan Amendment 4) — not
   repaired after scoring, because a post-scoring repair does not rescue a claim.
6. **Class: a frozen counting command that cannot produce its own required value.** The C1 command sequence omitted
   the `git show master:tools/gate-records.py > $W/base-tool.py` step, so run verbatim it printed
   `HARM_RECHECK … moved=31 base_rc=2`, exit 1 — `moved=0` was unreachable from the frozen three lines, while the
   `expected.tsv` row did produce it. **Evidence pointer:** `R89ReviewerC1` `harm-counting-command-verbatim.txt`.
   **Captured-by:** QUALITY 188 ("an artefact that claims a machine-checkable closure carries the literal command, and
   the command is run once against the artefact's own data") — the rule existed and was not applied to the frozen
   claim text. **Fix:** plan Amendment 5 carries the corrected literal command; QUALITY 195 lands the requirement that
   the frozen text's command is the one the driver runs.
7. **Class: a universal quantifier over a field set the instrument renames.** "Every round-88 field unchanged" was
   false in the letter (`LEGS` → `LEGS_MEASURED`, `DIV3` added), true only for the enumerated measurement fields.
   **Evidence pointer:** `R89ReviewerC1` `field-diff.txt`. **Captured-by:** QUALITY 187 and the §9 claim-sizing rule
   ("no universal clauses unless the counting command enumerates the full set") — the enumeration was in the
   parentheses and the universal sat beside it. **Fix:** Amendment 5 narrows the sentence to the enumeration.

Seat-trailer discipline: every seat's prompt requires a `VERDICT:` trailer; the scribe tallies a missing one as a
seat-discipline finding rather than a hold (round-88 routed defect 7).

## Spot-check intake

Round 88's non-author check routed eight defects. Disposition, one row each:

| routed item | disposition | pointer |
|---|---|---|
| 1. prefile ledger layout (`claims.json` absent) | **fixed** — `.ufo/waves/round-89/claims.json` is written beside the ledger and the gate is run before filing | `.ufo/waves/round-89/claims.json`; report's `PREFILE-FALSIFICATION:` line |
| 2. per-format reconciliation (C1) | **fixed** — `rederive()` reads four grammars; `E7c`/`E7b` die on `UNRECONCILED` | `corpus/evidence/round89/gate-records-r89.py`; `receipts/c1-mutants.txt` |
| 3. verdict-vs-field reconciliation (C2) | **fixed** — `fields_hold` from the printed tallies plus the `VERDICT` leg; `M1`/`M2`/`M3` die | `curation-r89.py`; `receipts/c2-mutants.txt` |
| 4. dead superseder-own-read clause | **fixed** — raw-cell match, `SUP_CLAUSE_CHECKED` printed, battery `SUP-clause-mirror` refuses with `sup_unresolved=1 unresolved=0`; `M5` dies through the battery | `curation-r89-controls.py`; `receipts/c2-controls.txt` |
| 5. control-receipt discipline | **fixed** — `controls/run-controls.sh` checks each receipt's exit and every `required_fields` token against `expected.tsv`; `CONTROL_RECEIPTS=PASS` | `controls/run-controls.sh`; report's receipt line |
| 6. duplicate-qid / swapped-quote forgeries | **partly fixed** — `DUPQID` closes the duplicate cite (`M4a`/`M4b` die); the quote-content swap and ≥7-token substitution are **named limits** in the claim, not closed | `claims.md` C2 named limits 1–2 |
| 7. seat discipline (`VERDICT:` trailer) | **carried as a requirement** — every prompt demands the trailer; the scribe tallies a miss | wave context; `## Mistakes` trailer paragraph |
| 8. operator-owned prompt corruption | **not the lane's** — carried, unchanged | `.ufo/prompts/chousa-round-89.md` |

## Trends

| trend | verdict | evidence |
|---|---|---|
| expansion | unchanged | `ls corpus/knowledge/*.md \| wc -l` → 97 at base and at the freeze; the registry is 218 rows at both revisions (two `used-by` cells extended, no row added, none re-anchored). The round's gain is in the instruments; nothing is counted as new ground. |
| quality | improved | seven routed repairs across two instruments, each with a failable witness: `E7c`/`E7b` die on `UNRECONCILED`, `E7d`/`E7f` on `UNCROSSCHECKED`, the dead detector and the detached leg fail the curation verdict, the duplicate-qid cite is refused, and the superseder clause fires on the battery's mirror with `sup_unresolved=1 unresolved=0`. Four criteria mined (QUALITY 190–193); gate selftest `PASS (283 cases)`; preflight `8/8`. |
| discernment | improved | the wave fired the *sentence* not the predicate (plan Amendment 1), the lane published two by-construction conjuncts as seams instead of letting them read as live checks (Amendment 2), and it refuted one reviewer finding against committed bytes (Amendment 3, `receipts/registry-cells.txt`). Four of this round's own errors are mined with fixes shown able to fail. |

## Wave settlement

One v1 wave, 12 seats (4 executor, 1 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 scout, 1 connector,
1 scribe), attack share 6/12. Every seat named a receipt and a `VERDICT:` trailer; the per-seat verdicts and the
falsification dispositions are in `.ufo/waves/round-89/claim-falsification.tsv` and `w1-results.json`.
