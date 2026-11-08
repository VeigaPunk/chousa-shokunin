# Round 89 — settlement draft (scribe `R89ScribeLesson`)

Drafted by the scribe seat from the committed receipts only; the L1 (`ChousaR89`) integrates. Base `f8fa55ec`, claim
freeze `ac0a0892`. Every command below was run by this seat; the receipt paths are under
`.ufo/waves/round-89/w1/R89ScribeLesson/receipts/`.

## Gate

No fetch this round; no registry row opened, re-anchored or re-opened. The two rows this round's claims cite were
**re-opened from committed bytes** — S216's capture (`corpus/captures/b1b13a12aee75c6ecc20fb91.txt`) and S218's repo
files — and their `used-by` cells were extended old→new with `corpus/evidence/round89/claims.md`:

| row | old `used-by` | new `used-by` |
|---|---|---|
| S216 | `corpus/evidence/round86/claims.md, corpus/evidence/round87/claims.md` | `corpus/evidence/round86/claims.md, corpus/evidence/round87/claims.md, corpus/evidence/round89/claims.md` |
| S218 | `corpus/evidence/round87/claims.md` | `corpus/evidence/round87/claims.md, corpus/evidence/round89/claims.md` |

No other cell moved: `git diff f8fa55ec ac0a0892 -- corpus/SOURCES.md` is exactly two `-|`/`+|` pairs, both in the
last cell (`receipts/r8-registry-diff.txt`). Registry 218 rows at both revisions
(`git show <rev>:corpus/SOURCES.md | grep -cE '^\| S[0-9]+'` → 218 / 218, `receipts/r8-registry-diff.txt`).

GATE-RECORD S216 url=https://www.rfc-editor.org/rfc/rfc9110.html fetched=2026-11-08T06:50:40Z tier=A decision=admit capture=corpus/captures/b1b13a12aee75c6ecc20fb91.txt capture_sha256=ec14fa3499c2dfbcf3f08f5e50cb623fa268bd1066d34e5ea710c23f0a46794e words=22 quote="indicates that the request was successful but the enclosed content has been modified from that of the origin server's 200 (OK) response"

GATE-RECORD S218 rev=ac0a0892c15de11fb28d3208f2b287687c00477e path=corpus/QUALITY.md line=1120 words=11 quote=A frozen `teaches` cell is not evidence; the superseding row's is.

- **S216** — RFC 9110 §15.3.4, "203 Non-Authoritative Information". URL `https://www.rfc-editor.org/rfc/rfc9110.html`;
  access date **2026-11-08T06:50:40Z** (the committed refetch row, `corpus/evidence/round57/refetch.tsv:185`,
  `http_code=200`, `curl_rc=0`; the row is round 87's — this round did not fetch). The located 22-word quote sits in
  the committed capture at `corpus/captures/b1b13a12aee75c6ecc20fb91.txt`; the capture's sha256 is
  `ec14fa34…`, the capture key is `sha256(url)[:24] = b1b13a12aee75c6ecc20fb91`, and the quote is present verbatim
  (`receipts/r9-s216-quote-probe.txt`). This is the ground for binding the two 203 classes to `203` rather than to
  `2xx` or to `200`: a 203 is a *successful* response whose body is not the origin's, so an admit record claiming OK
  content and a reject record claiming a failed transfer are both refusals.
- **S218** — own-work: `corpus/QUALITY.md` criterion 178 + `CORPUS.md` rule 2. Repo path `corpus/QUALITY.md`,
  line **1120** at revision `ac0a0892c15de11fb28d3208f2b287687c00477e`; access date **2026-11-08** (re-opened from
  committed bytes at the freeze). The 11-word located quote is criterion 178's operative clause. This is the rule the
  `TEACHES` and superseder-own-read legs enforce — a superseded row's frozen `teaches` is not evidence, and only
  `status`, `recheck` and `used-by` may change in place.

Verified with the lane's own tool against this draft:
`python3 -B tools/gate-records.py verify --root /home/vgpnk/Projects/shokunin/chousa-shokunin --repo /home/vgpnk/Projects/shokunin/chousa-shokunin .ufo/waves/round-89/w1/R89ScribeLesson/lesson-settlement-draft.md`
→ `GATE_RECORD …:15 S216 OK` / `GATE_RECORD …:17 S218 OK` / `GATE_RECORDS files=1 records=2 ok=2 fail=0`, exit 0
(`receipts/r10-gate-verify.txt`). The same tool run against the lane's own draft lesson
(`corpus/lessons/round-89.md`) prints the same two `OK` verdicts and exit 0
(`corpus/evidence/round89/controls/receipts/gate-records-round89.txt`; local copy `receipts/lane-gate-records-round89.txt`).

No egress table was required: `SKILL.md` `## Boundaries` says "A window without an approval table is loopback-only",
and this window was loopback-only. Nothing in this seat's work fetched anything; every check above reads committed
bytes.

## Claim outcomes

Both claims are scored on the freeze bytes. Every field below was re-measured by this seat at `ac0a0892` in a clone
of the lane repo (`git clone` of the lane repo, `git checkout ac0a0892`), with the instrument's own `--work` under
this seat's scratch.

- **C1 operability** (`C1-BATTERY-R89`) — **PASS**, exit 0.

  ```
  TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362
  EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 DIV3=3 D1_REFUSED=3/3
  D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1
  MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS_MEASURED=15/15
  LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16
  GATE_RECORDS_R89=PASS
  ```

  Command: `python3 -B corpus/evidence/round89/gate-records-r89.py --root <clone> --repo <clone> --work <scratch>`
  → exit 0 (`receipts/r1-c1-landing.txt`; byte-identical to the committed `corpus/evidence/round89/controls/receipts/c1-landing.txt` (local copy `receipts/lane-c1-landing.txt`)).
  Mutants: `python3 -B corpus/evidence/round89/mutate-r89.py --root <clone> --repo <clone> --work <scratch>` →
  `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2 EQUIVALENT_ON_TREE=0/0 TOTAL=13/13`, exit 0
  (`receipts/r2-c1-mutants.txt`; byte-identical to the committed `corpus/evidence/round89/controls/receipts/c1-mutants.txt` (local copy `receipts/lane-c1-mutants.txt`)). The four
  round-88 survivor shapes die on named lines: `E7c` on `UNRECONCILED D1_WIDTH detail=3/3/1 pin3 receipt_ok=True
  rederived=False`, `E7b` on `UNRECONCILED MUT_ADMIT detail=derived=0 killed=0`, `E7d` on
  `UNCROSSCHECKED D1_WIDTH detail=3/3/3 pin3 D1_FORGES=3 D1_EXPECTED=3 DIV3=1 pin=3/3`, `E7f` on
  `UNCROSSCHECKED D1_WIDTH … D1_EXPECTED=4 DIV3=3 pin=3/3`. Harm:
  `python3 -B corpus/evidence/round89/harm-recheck.py --root <clone> --repo <clone> --base-tool <scratch>/base-tool.py`
  → `HARM_RECHECK files=13 records=29 moved=0 base_rc=0 r88_rc=0`, exit 0 (`receipts/r3-c1-harm.txt`; the base
  tool's sha256 is `905f9da2…`, the unchanged subject blob, `receipts/base-tool.py`).
  **Before:** the round-88 battery on the same tree prints `GATE_RECORDS_R88=PASS` with no `CROSSCHECK` field and no
  `DIV3` (`corpus/evidence/round89/controls/receipts/c1-prior-instrument.txt` (local copy `receipts/lane-c1-prior-instrument.txt`)), so it cannot express the round-89 guard.

- **C2 calibration** (`C2-CURATION-R89`) — **PASS**, exit 0.

  ```
  SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20
  Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7
  WARRANT_OK=17/17 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0
  SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=8/8
  TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
  CURATION_R89=PASS
  ```

  Command: `python3 -B corpus/evidence/round89/curation-r89.py --root <clone>` → exit 0
  (`receipts/r4-c2-landing.txt`; byte-identical to the committed `corpus/evidence/round89/controls/receipts/c2-landing.txt` (local copy `receipts/lane-c2-landing.txt`)). Nine legs:
  `EXPECTED_LEGS = 9` (`curation-r89.py:72`), eight appended before the summary is built and `VERDICT` appended
  after, so the printed summary cell reads `LEGS_MEASURED=8/8` — the count over the legs that exist when the cell is
  built — and the verdict is field-derived (`fields_hold`). Controls:
  `python3 -B corpus/evidence/round89/curation-r89-controls.py --root <clone> --work <scratch>` →
  `FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7` / `CONTROLS=PASS`, exit 0 (`receipts/r5-c2-controls.txt`;
  byte-identical to the committed `corpus/evidence/round89/controls/receipts/c2-controls.txt` (local copy `receipts/lane-c2-controls.txt`)). Mutants:
  `python3 -B corpus/evidence/round89/curation-r89-mutants.py --root <clone> --work <scratch>` →
  `MUTANTS_KILLED=6/6 COUNTER_DETECTED=5 BATTERY_DETECTED=1`, exit 0 (`receipts/r6-c2-mutants.txt`; byte-identical
  to the committed `corpus/evidence/round89/controls/receipts/c2-mutants.txt` (local copy `receipts/lane-c2-mutants.txt`)).
  **Before:** the round-88 counter on the same tree prints `CURATION_R88=PASS` with no `DUPQID` leg, no field-derived
  verdict and a dead superseder clause (`corpus/evidence/round89/controls/receipts/c2-prior-instrument.txt` (local copy `receipts/lane-c2-prior-instrument.txt`)).

- **The control driver** (`controls/run-controls.sh`, the routed-defect-5 repair) re-run in this seat's scratch clone:
  `RECEIPT_OK` × 8, `CONTROL_RECEIPTS=PASS`, exit 0 (`receipts/r7-run-controls.txt`). Each receipt's exit code and
  every `required_fields` token in `controls/expected.tsv` agree.

- **The instrument pins** verify against the freeze tree: `sha256sum -c` over `corpus/evidence/round89/instrument-pins.txt`
  → `OK` for all nine round-89 files and for the unchanged subject tool `tools/gate-records.py` (`905f9da2…`)
  (`receipts/r15-instrument-pins.txt`; local copy `receipts/lane-instrument-pins.txt`). The gate selftest passes:
  `bash tools/research-gate.sh --selftest` → `RESEARCH_GATE_SELFTEST: PASS (283 cases, 0 skipped)`, exit 0
  (`receipts/r13-gate-selftest.txt`).

## Mistakes

Four errors of this round's own, each with the class, the evidence pointer, who captured it, and the fix shown able
to fail. All four were pre-freeze errors in the round's own instruments; the fix's ability to fail is demonstrated
below by re-running the pre-fix shape against the landed bytes, in this seat's scratch.

1. **Class: a single-point mutant on a healthy tree proves nothing — it is a constant, not a detachment.** The first
   `E7c`/`E7b` replaced only a leg's `ok` with `True` on a *healthy* tree, leaving the measurement intact, so the
   detail still re-derived `True` and the mutant survived. Nothing about the round-89 guard was exercised.
   **Evidence pointer:** `plans/round-89.md` §Pre-freeze repairs 4 ("a single-point healthy-tree mutant proves
   nothing (its `A3`/`E4` variant)"); `corpus/QUALITY.md:1199` (criterion 190). **Captured-by:** the round-88 wave's
   reviewer and critic (`R88ReviewerC1`, `R88CriticClaims` — the `A3`/`E4` shape), carried by
   `plans/round-89.md` §Inputs defect 2; QUALITY 185 covered leg accounting but not mutant *construction*.
   **Fix:** a mutant carries a list of edits — a broken measurement **plus** the detachment that hides it.
   **Shown able to fail:** re-applying the single-point form to the landed counter (`receipts/d1-single-point-mutant-probe.txt`)
   prints `LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16` / `GATE_RECORDS_R89=PASS`, exit 0,
   with no `UNRECONCILED`/`UNCROSSCHECKED` line — the mutant survives, so the fix is load-bearing. The landed
   multi-point shape dies: `KILLED E7c-width-detached rc=1` with `UNRECONCILED D1_WIDTH detail=3/3/1 pin3
   receipt_ok=True rederived=False` (`receipts/r2-c1-mutants.txt`).

2. **Class: a mirror fixture id that collides with a real registry row is silently discarded by last-wins.** The
   superseder-clause mirror inserted `| S099 | … | mined | … |`, but S099 is a real ERIC record further down
   `corpus/SOURCES.md` (`corpus/SOURCES.md:109`), so `parse_registry`'s `reg[cells[0]] = cells`
   (`curation-r89.py:87`) kept the *real* row and the mirror's disposal edge vanished — the battery then deviated
   for the wrong reason.
   **Evidence pointer:** `corpus/QUALITY.md:1207` (criterion 191); the landed mirror uses the next unused id,
   `S219_ROW` (`curation-r89-controls.py:41`, `curation-r89-mutants.py:36`), and `S219` is absent from the real
   registry (`grep -c '^| S219 ' corpus/SOURCES.md` → 0, `receipts/d2-last-wins-probe.txt`).
   **Captured-by:** none — the census validates the real registry, never a scratch mirror.
   **Fix:** the mirror uses an id that is unused in the registry, and the battery's positive case fails loudly if
   the edge is missing. **Shown able to fail:** inserting the mirror row under the colliding id `S099` and re-reading
   the registry leaves the ERIC title in place and yields **no** row whose teaches names `supersedes S031` — the
   disposal edge is gone (`receipts/d2-last-wins-probe.txt`); re-running the whole control battery with the id
   reverted to `S099` prints `CASE_DEVIATION SUP-clause-mirror: NOT refused by r89 or NOT accepted by the prior
   counter`, `FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=0/7`, `CONTROLS=FAIL`, exit 1 (same receipt).

3. **Class: a summary field printed before the leg that completes it exists reports a false denominator.** The first
   run printed a summary cell reading `15/16` beside `GATE_RECORDS_R89=PASS`, because the completing `SUMMARY` leg
   is appended after the summary string is built: a reader saw a verdict claiming 16 legs while the summary cell
   counted 15.
   **Evidence pointer:** `corpus/QUALITY.md:1214` (criterion 192); the landed counter builds the summary over
   `len(legs)` at build time (`gate-records-r89.py:602`) and carries the appended total on the verdict line
   (`gate-records-r89.py:735`, `LEGS_APPENDED={len(legs)}`).
   **Captured-by:** none — the `RECONCILED` total included `SUMMARY`, so no leg failed.
   **Fix:** the summary prints the measured count over the legs that exist when it is built, and the verdict line
   carries the appended total; the completing leg is itself receipted, re-read and reconciled.
   **Shown able to fail:** re-pointing the landed summary cell's denominator at `EXPECTED_LEGS` reproduces the
   pre-fix line verbatim — `… DERIVE_NEG=1 LEGS_MEASURED=15/16` beside `LEG_REREAD=16/16 RECONCILED=16/16
   CROSSCHECK=15/15 LEGS_APPENDED=16` / `GATE_RECORDS_R89=PASS`, exit 0 (`receipts/d3-summary-denominator-probe.txt`).
   The landed form prints `LEGS_MEASURED=15/15` with `LEGS_APPENDED=16` on the verdict line, and the completing leg
   is load-bearing: `KILLED E7g-receipt-removed rc=1` with `UNRECONCILED SUMMARY detail=14/14 receipt_ok=False
   rederived=True` and `LEG_FAIL SUMMARY 14/14` (`receipts/r2-c1-mutants.txt`).

4. **Class: a diagnostic line that names a key which never exists.** The cross-check's `UNCROSSCHECKED` line looked
   the *leg* name (`D1_WIDTH`) up in a dictionary keyed by **summary fields**, so every failure — intended or not —
   rendered the missing-key placeholder `summary_fields=-` instead of the values actually compared.
   **Evidence pointer:** `corpus/QUALITY.md:1221` (criterion 193); the landed `crosscheck()` returns a note naming
   the cells it compared (`gate-records-r89.py:665-681`).
   **Captured-by:** none.
   **Fix:** the diagnostic names the compared cells and their values. **Shown able to fail:** re-applying the
   pre-fix diagnostic shape to the landed counter and re-running the `E7d` shape prints
   `UNCROSSCHECKED D1_WIDTH detail=3/3/3 pin3 summary_fields=-` and
   `UNCROSSCHECKED D2_WIDTH detail=3/3/3 pin3 summary_fields=-` — the placeholder on both legs
   (`receipts/d4-nonexistent-key-probe.txt`). The landed diagnostic for the same shape names the cells:
   `UNCROSSCHECKED D1_WIDTH detail=3/3/3 pin3 D1_FORGES=3 D1_EXPECTED=3 DIV3=1 pin=3/3` — `DIV3=1` against the
   leg's forged `div3=3` (`receipts/r2-c1-mutants.txt`).

Seat-trailer discipline: every seat's prompt requires a `VERDICT:` trailer; the scribe tallies a missing trailer as
a seat-discipline finding rather than a hold (round-88 routed defect 7). All eleven wave report files present in
`.ufo/waves/round-89/w1/` ship at least one `VERDICT:` line (`receipts/r11-seat-trailers.txt`).

## Spot-check intake

Round 88's non-author check (`corpus/lessons/round-88-verifier-spotcheck.md`) routed eight defects. Disposition, one
row each. Every disposition below was checked by this seat against committed bytes or a receipt named in the row.

| # | routed item (round-88 spot-check) | disposition | pointer |
|---|---|---|---|
| 1 | prefile ledger layout (`claims.json` absent; the checker reads `.ufo/waves/round-<N>/claims.json`) | **fixed** — `.ufo/waves/round-89/claims.json` is written and committed at the freeze (112 lines, keys `C1`/`C2` with `sentence`/`predicate`/`kill_rules`/`named_limits`); the checker no longer reports `claims-missing` | `.ufo/waves/round-89/claims.json`; `scripts/hyaku/prefile-falsification.py:128,135`; this seat's run reports only `wave-missing …/w1-results.json` (the wave-results file is written at integration) — `receipts/r12-prefile-check.txt` |
| 2 | per-format reconciliation (C1): the `RECONCILED` conjunct searched only `detail=(\d+)/(\d+)` | **fixed** — `rederive()` reads four grammars (`n/m`; `len/d1/div3 pinN` with all four equal and `pin == ROWS_203`; `derived=x killed=y` with both 1; `tool present`), so the two width legs and the two mutant legs no longer detach freely; `E7c`/`E7b` die on `UNRECONCILED` | `corpus/evidence/round89/gate-records-r89.py:637-655`; `receipts/r2-c1-mutants.txt`; `receipts/d1-single-point-mutant-probe.txt` |
| 3 | verdict-vs-field reconciliation (C2): the verdict was `all(ok)`, never reconciled with the printed fields | **fixed** — `fields_hold` is computed from the printed tallies and the `VERDICT` leg refuses a divergence in either direction; `M1` (dead detector), `M2`/`M3` (detached leg / legs-only verdict) and `M4a`/`M4b` all die | `corpus/evidence/round89/curation-r89.py:305-317`; `receipts/r6-c2-mutants.txt` |
| 4 | dead superseder-own-read clause (C2): a case-sensitive pattern matched against a lowercased cell | **fixed** — the raw cell is matched (`re.match(r"supersedes (S\d{3,}) —", cells[6])`), `SUP_CLAUSE_CHECKED` is printed so the vacuity on the real registry is visible (`=0`), and the battery's `SUP-clause-mirror` refuses with `sup_unresolved=1 unresolved=0`; `M5` dies through the battery | `corpus/evidence/round89/curation-r89.py:255`; `receipts/r5-c2-controls.txt`; `receipts/r6-c2-mutants.txt` |
| 5 | control-receipt discipline: a receipt filed under a failing expectation, and a receipt with no expectation row | **fixed** — `controls/run-controls.sh` runs each control and refuses to pass unless the receipt's exit code **and** every `required_fields` token agree with the `expected.tsv` row; all 8 rows agree | `corpus/evidence/round89/controls/expected.tsv` (8 rows), `controls/run-controls.sh:23-33`; this seat's re-run: `RECEIPT_OK` ×8, `CONTROL_RECEIPTS=PASS`, exit 0 — `receipts/r7-run-controls.txt` |
| 6 | duplicate-qid / swapped-quote forgeries (C2) | **partly fixed** — the duplicate cite is closed: `DUPQID` refuses a warrant cell citing `Q1, Q1 (S215)` and `M4a`/`M4b` die on it. The quote-content swap and the ≥7-token verbatim substitution are **named limits** in the claim, not closed: `MIN_TOKENS = 7` is a measured floor, and the qid-set pin guards label identity, not content | `corpus/evidence/round89/claims.md` C2 named limits 1–2; `corpus/evidence/round89/curation-r89.py:281`; `receipts/r5-c2-controls.txt` (`LEG_FAIL DUPQID … warrant=Q1, Q1 (S215)`) |
| 7 | seat discipline: a seat shipped no `VERDICT:` trailer | **carried as a requirement** — every seat's prompt demands the trailer and the scribe tallies a miss as a seat-discipline finding, not a hold. This round: all eleven wave report files ship at least one `VERDICT:` line | wave context; `receipts/r11-seat-trailers.txt` |
| 8 | operator-owned prompt corruption (`.ufo/prompts/chousa-round-88.md:143` cuts mid-word) | **not the lane's** — carried, unchanged; operator-owned | `corpus/lessons/round-88-verifier-spotcheck.md` routed defect 8 |

## Trends

| trend | verdict | evidence |
|---|---|---|
| expansion | unchanged | `git ls-tree -r --name-only <rev> -- corpus/knowledge/ \| grep -c '\.md$'` → **97** at base `f8fa55ec` and **97** at the freeze `ac0a0892` (`receipts/r8-registry-diff.txt`); the registry is **218** rows at both revisions and no row was added, removed or re-anchored (same receipt; `git diff f8fa55ec ac0a0892 -- corpus/SOURCES.md` = two `used-by` cells only). The round's gain is in the instruments; nothing is counted as new ground. |
| quality | improved | six routed repairs across two instruments, each with a failable witness this seat re-measured: the per-format reconciliation kills `E7c`/`E7b` on `UNRECONCILED`, the summary cross-check kills `E7d`/`E7f` on `UNCROSSCHECKED` (`receipts/r2-c1-mutants.txt`); the field-derived verdict kills the dead detector, the detached leg and the legs-only verdict (`receipts/r6-c2-mutants.txt`); the duplicate-qid cite is refused (`receipts/r5-c2-controls.txt`); the superseder clause fires on the battery's mirror with `sup_unresolved=1 unresolved=0` (same receipt); the harm sweep moves no genuine record (`receipts/r3-c1-harm.txt`, `moved=0`); the control driver passes all eight rows (`receipts/r7-run-controls.txt`). Six criteria mined (`corpus/QUALITY.md:1199-1232`, 190–195). |
| discernment | improved | the wave fired the *sentence* rather than the predicate on three wording clauses and the lane published each firing as a numbered plan amendment rather than arguing it away (`.ufo/waves/round-89/claim-falsification.tsv`, 23 rows at the time of this seat's run; `plans/round-89.md` §Amendments 1–9); the round's own four pre-freeze errors are mined as criteria 190–193 with each fix shown able to fail (`receipts/d1`–`d4`); and this seat's independent re-measurement reproduces every committed receipt byte-for-byte (`receipts/r1`–`r6` vs `controls/receipts/`), which is the non-vacuity check the lesson's own claims rest on. |

## Findings on the L1's own draft (for the integrator, not part of the lesson body)

Three discrepancies between the L1's working draft (`corpus/lessons/round-89.md`, uncommitted at the time of this
seat's run) and the committed bytes. None changes a predicate; all three are the class the round mined as criterion
192 — a printed field that reports a total it does not hold.

1. **The draft's C2 outcome quotes `LEGS_MEASURED=8/9`; the instrument prints `LEGS_MEASURED=8/8`.** The draft
   (`corpus/lessons/round-89.md:57`) and `plans/round-89.md:178` (Amendment 8) both carry `LEGS_MEASURED=8/9`. The
   committed receipt `corpus/evidence/round89/controls/receipts/c2-landing.txt` (local copy `receipts/lane-c2-landing.txt`) and this seat's re-run both print `LEGS_MEASURED=8/8` —
   `curation-r89.py:293` builds the cell as `sum(ok)/len(legs)` over the legs that exist at that point (eight), and
   `EXPECTED_LEGS = 9` is the *expected* total, not the printed denominator. The sentinel's finding quoted the same
   `8/8`. The draft's `8/9` is a misreading of the nine-leg total as a printed denominator.
   **Receipt:** `receipts/r14-draft-misquotes.txt`.
2. **The draft's trends row says "Four criteria mined (QUALITY 190–193)"; six were mined (190–195).** `grep -cE
   '^19[0-9]\. ' corpus/QUALITY.md` → **6**, criteria 190, 191, 192, 193, 194, 195. This is the same class as
   round-88's `## Corrections` 2 (a lesson and a SCORECARD sentence that named five mined criteria when eight had
   landed) — a count written before its companion landed, asserted by name.
   **Receipt:** `receipts/r14-draft-misquotes.txt`.
3. **One seat's `VERDICT:` trailer names the wrong seat token.** `R89ReviewerC2.md:75` reads
   `VERDICT: build R89ReviewerC2 C2 fired`; the contract is `VERDICT: <seat> <C1|C2> fired|held|n/a`, so the seat
   token is `build` and the seat id sits in the third field. The other 16 trailer lines across the eleven report
   files are well-formed, and every seat carries at least one. Tally: 11 distinct seat tokens for 12 spec seats
   (`w1-spec.json` items = 12) — the twelfth is this scribe's own report, filed with this draft.
   **Receipt:** `receipts/r11-seat-trailers.txt`.
