# Round 90 — the receipt driver's whole-token rule and a `SKILL.md` tally that re-derives to the tool's own verdict verify; the curation counter prints its verdict but honest-stops on its frozen kill rule (2026-11-08)

Base `f54a45ed197dd475af50d82e43a22df3d2e99782` (round-89 landing + its non-author spot-check). Frozen claims in
`corpus/evidence/round90/claims.md` and `.ufo/waves/round-90/claims.json`; plan and amendments in
`plans/round-90.md`. Round 89's non-author check routed seven defects; this round closes 1–7. One v1 wave, 13 seats.

Every number below was re-measured by this seat from committed bytes at the carrier `9bad12011187d114ba2c4588c5df08a21ab28145`
and the freeze `8d9893b42eb22690ea5f920ab87fd7e1810b847a`. Transcripts: `.ufo/waves/round-90/w1/R90ScribeLesson/receipts/`.

**Reconciliation note for the L1.** This draft was written against the frozen claims and then reconciled against the
plan's Amendments 1–10 (working-tree `plans/round-90.md`) and the L1's in-progress `corpus/lessons/round-90.md`. Three
outcomes changed as a result, and the L1's rulings govern: **C2 is an honest stop, not a pass** (Amendment 8 — the
frozen kill rule K2 fires; this seat re-derived both forgeries independently, below); **C1 verifies only on the wording
narrowed by Amendments 2, 3, 4, 7 and 9**; **C3 verifies only on the wording narrowed by Amendments 1 and 10**. Where
the wave's artifacts contradict the frozen text, the amendment wins and the narrowed property is what this draft
reports.

## Gate

One row was opened this round and one row was mined. The fetch was a single `GET` to the man7.org GNU grep(1) page;
the failed gnu.org attempt that preceded it is a ledger row, not a registry row.

GATE-RECORD S220 url=https://man7.org/linux/man-pages/man1/grep.1.html fetched=2026-11-08T09:52:31Z tier=A decision=admit capture=corpus/captures/e6ec761219e8044b0e9e067a.txt capture_sha256=5a5e69c56413ba682b1609cba2baacafb393ff6821d5b752938efc390fd12823 words=10 quote="Select only those matches that exactly match the whole line."

Verified with the lane's own gate tool, unmodified this round (`git diff f54a45ed 9bad1201 -- tools/gate-records.py`
→ empty):

```
python3 -B tools/gate-records.py verify --root . --repo . .ufo/waves/round-90/w1/R90ScribeLesson/receipts/gate-record-s220-words10.md
GATE_RECORD …:5 S220 OK
GATE_RECORDS files=1 records=1 ok=1 fail=0                      # exit 0
```
(`receipts/gate-records-words10.txt`)

The `words=` value is **10**, not the 11 the wave's own seat text carries. The quote is
`Select only those matches that exactly match the whole line.` — ten whitespace-separated tokens — and
`tools/gate-records.py` computes `n = len(quote.split())` and refuses any other number (`WORDS`). A record written with
`words=11` fails: `receipts/gate-records-words11.txt` → `S220 FAIL WORDS`, exit 1. The `11` is round 89's S218 word count
(`corpus/lessons/round-89.md:19`), carried over by copy. **The L1 must land `words=10`.**

The other fields are the refetch row's, taken verbatim from `corpus/evidence/round57/refetch.tsv:188`
(`S220  https://man7.org/linux/man-pages/man1/grep.1.html  e6ec761219e8044b0e9e067a  1  2026-11-08T09:52:31Z  0  200
d6f07a7f…  5a5e69c5…`): `fetched=2026-11-08T09:52:31Z`, `capture_sha256=5a5e69c5…` (= the row's `txt_sha256` and
`sha256(corpus/captures/e6ec761219e8044b0e9e067a.txt)`), `tier=A` (= the registry row's tier cell). Each departure is
refused by the same tool: `tier=B` → `FAIL TIER` (`receipts/gate-records-tierB.txt`); a wrong `capture_sha256` →
`FAIL CAPTURE_SHA` (`receipts/gate-records-badsha.txt`); the S219 row's timestamp `09:44:57Z` instead of the S220 row's
`09:52:31Z` → `FAIL REFETCH` (`receipts/gate-records-wrong-fetched.txt`). The capture key is `sha256(url)[:24]`, which
equals the capture file's stem `e6ec761219e8044b0e9e067a` — the row's own anchor cell names that key.

**Landing order for the Gate section.** The capture bytes are not in the freeze: `git ls-tree 8d9893b4 corpus/captures/`
lists no `e6ec761219e8044b0e9e067a` file; the capture lands in `aa7d42237364509d6647d10c93ee421d4626a3ca`
("round-90: S220 source capture"), after the carrier. A Gate record verified against a tree at the carrier fails
`CAPTURE_PATH,CAPTURE_SHA,QUOTE_ABSENT,REFETCH` (re-measured in a clean clone at `9bad1201`). The lesson's `## Gate`
must therefore be verified against a tree that contains `aa7d4223` (or later) — the lesson file itself lands after that.

**S219 is reserved, and the reservation is measured.** `S219` is the round-89 control fixture's mirror-row id
(`corpus/evidence/round89/curation-r89-controls.py:41`, `corpus/evidence/round89/curation-r89-mutants.py:36`). A real
`S219` registry row renames the fixture's row inside the parsed registry, and the r89 control battery's superseder case
stops being accepted by the prior counter. Re-derived by this seat on a scratch copy of the tree at the carrier, with one
real `S219` row appended to `corpus/SOURCES.md`:

```
python3 -B corpus/evidence/round89/curation-r89-controls.py --root <scratch copy> --work <scratch>
CASE_DEVIATION SUP-clause-mirror: NOT refused by r89 or NOT accepted by the prior counter
FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=6/7
CONTROLS=FAIL                                                # exit 1
```
(`receipts/s219-id-collision.txt`; on the unmodified tree the same command prints `FORGERY_REFUSED=7/7
PRIOR_ACCEPTED_FORGERY=7/7 / CONTROLS=PASS`, exit 0.)

So the failed gnu.org attempt stays a ledger row with no registry row — `corpus/evidence/round57/refetch.tsv:186`:
`S219  https://www.gnu.org/software/grep/manual/html_node/Matching-Control.html  d00017f70dae196331f06e4c  1
2026-11-08T09:44:25Z  28  000  -  -` (curl rc=28 timeout, http 000, no bytes) — and the mined row is `S220`. The ledger
also keeps a successful man7.org row under `S219` at `09:44:57Z` (`refetch.tsv:187`, same capture key and the same
`raw_sha256`/`txt_sha256` as the `S220` row): that row is the id-rename residue of the same transfer, and it is not a
registry row and not citable. `tools/gate-records.py` refuses an `S219` Gate record outright (`REGISTRY` — there is no
S219 row): `receipts/gate-records-s219-unreach.txt` → `S219 FAIL REGISTRY`, exit 1.

Registry, base → carrier: **218 → 219 rows**, the one added row being `S220` (tier A, `mined`, `2026-11-08`, `180d`,
`used-by = corpus/evidence/round90/claims.md`). `git diff f54a45ed 9bad1201 -- corpus/SOURCES.md` is exactly one added
line. Knowledge entries 97 → 97. The census exits 0 at start and end with the same five pre-existing `W04` warnings
(`corpus/evidence/round90/census-start.txt`, `corpus/evidence/round90/census-end.txt`).

## Claim outcomes

All three claims are scored on committed bytes and re-measured by this seat. The counting commands are the frozen ones.

### C1 — `C1-DRIVER-R90` (operability) — **verified on the wording narrowed by Amendments 2, 3, 4, 7 and 9**

Frozen command, run from the lane root at the landing bytes (the receipts are unchanged from the carrier):

```
python3 -B corpus/evidence/round90/control-driver-r90.py verify --root . --repo . \
  --rev 8d9893b42eb22690ea5f920ab87fd7e1810b847a \
  --receipts-rev 9bad12011187d114ba2c4588c5df08a21ab28145
RECEIPT c1-gate-r89 OK committed+exact+pin+fresh
RECEIPT c1-mutants-r89 OK committed+exact+pin+fresh
RECEIPT c1-harm OK committed+exact+pin+fresh
RECEIPT c1-harm-setup OK committed+exact+pin+fresh
RECEIPT c2-prior-landing OK committed+exact+pin+fresh
RECEIPT c2-prior-controls OK committed+exact+pin+fresh
RECEIPT SELF_PIN OK all scoring bytes equal their blobs at --rev
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS   # exit 0
```
(`receipts/c1-verify-lane-root.txt`, run from the lane working tree with `--root . --repo .`; the same command in a
clean `git clone --shared` checked out at the carrier gives the same seven lines and the same counts, exit 0 —
`receipts/c1-verify-clone-root-and-repo.txt`. The receipts' bytes are identical in both trees.)

The forged-receipt battery:

```
python3 -B corpus/evidence/round90/control-forgeries-r90.py --root . --work <scratch> --rev 8d9893b4…
OK B2-substring: r90 refused (TOKEN_DETACHED:LEG_REREAD=16/160,FRESH_TOKEN_DETACHED:LEG_REREAD=16/160), r89 accepted
OK B1-committed: r90 refused (TOKEN_DETACHED:LEG_REREAD=0/16), r89 accepted
OK B3-no-pin: r90 refused (PIN_MISSING), r89 accepted
OK B3b-stale-pin: r90 refused (PIN_MISMATCH:0000000000000000000000000000000000000000), r89 accepted
OK B4-harm-vacuity: r90 refused (PREDICATE_SHORT:records=0<1,FRESH_PREDICATE_SHORT:records=0<1), r89 accepted
OK C-duplicate-key: r90 refused (DUPLICATE_KEY:records,FRESH_DUPLICATE_KEY:records), r89 accepted
OK POSITIVE: accepted by both drivers
FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass
CONTROL_FORGERIES_R90=PASS                                                   # exit 0
```
(`receipts/c1-forgeries.txt`)

The receipt is read before any fresh run and the verification path writes nothing under the receipts directory: the nine
files' sha256 digests are identical before and after the verify run (`receipts/receipts-sha-before.txt` vs
`receipts/receipts-sha-after.txt`, `diff` → identical), and `git status --porcelain` in the clone is empty afterwards.

Before: the round-89 driver prints `CONTROL_RECEIPTS=PASS` over its own eight rows
(`corpus/evidence/round90/controls/receipts/c1-prior-driver.txt`) and accepts all six forgery classes (`prior rc=0` on
every line of the battery above) — the r90 driver's six refusal codes are the spot-check's B1–B4 plus the duplicate-key
class, each newly named.

Named limits 1–3 stand as frozen: a joint edit of instrument + receipt + expectation row survives (that edit is the
harness); whole-token matching binds one field per token, not its semantic role (only the C2 verdict phrase uses the
`line:` whole-line form); the self-pin compares bytes at named revisions and cannot detect a rewritten history.
Amendment 4 adds three more, measured by the wave and re-derivable from the driver source: **(4)** header keys are
last-wins, so a receipt carrying two `# exit=` or two `# computed_against=` lines is read by its last value and the
duplicate is not refused; **(5)** the instrument files a row executes are **not** pinned, so a substituted instrument that
prints the required tokens passes the fresh leg (`instrument-pins.txt` is not read by the driver); **(6)** the claim's
detector is the frozen fixture set (six committed rows, six forgery classes, the positive), not a mutant battery, so a
driver edit that makes the fresh comparison vacuous is invisible to it.

### C2 — `C2-CURATION-R90` (calibration) — **honest stop: the frozen kill rule K2 fires**

```
python3 -B corpus/evidence/round90/curation-r90.py --root .
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20
Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7
WARRANT_OK=17/17 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0
SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=10/10 VERDICT fields_hold=1
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
VERDICT fields_hold=1 legs_ok=10/10 DETECTOR_WITNESS=8/8
CURATION_R90=PASS                                                              # exit 0
```
(`receipts/c2-counter.txt`; `grep -c 'VERDICT fields_hold=1'` over the transcript → **2**, so the token round 89's
Amendment 8 said was unprinted is printed on the passing path.)

Before: the round-89 counter on the same tree prints `CURATION_R89=PASS` with `LEGS_MEASURED=8/8` and **no** `VERDICT`
token (`receipts/c2-r89-prior.txt`; `grep -c` → 0; the committed before-receipt `controls/receipts/c2-prior-landing.txt`
also has 0).

```
python3 -B corpus/evidence/round90/curation-r90-mutants.py --root . --work <scratch>
KILLED M1-dead-teaches … KILLED M2-detached-leg … KILLED M3-verdict-legs … KILLED M4a-dup-leg-forced …
KILLED M4b-dup-field-dropped … KILLED M5-lowercase-clause (detector=battery) … KILLED M6-locate-true …
KILLED M7-unentailed-empty … KILLED M8-teaches-never-fires … KILLED M9-dup-dead …
SURVIVOR_PRIOR r89-subst-0 rc=0
SURVIVOR_PRIOR r89-subst-1 rc=0
MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2   # exit 0
```
(`receipts/c2-mutants.txt`; the two constant-substituted detectors die on `LEG_FAIL WITNESS 7/8 bad=1` — `M6` forces
`locates` true, `M7` forces `unentailed_row` false — while the same two substitutions applied to the round-89 counter
stay alive, which is what `SURVIVOR_PRIOR` records.)

```
python3 -B corpus/evidence/round90/curation-r90-controls.py --root . --work <scratch>
OK POSITIVE: positive accepted by both
OK A1c-junk-substitute / A1d-truncate / caseG-relabel / F2-rejected-superseder / B1b-padding-qid /
   D1-duplicate-qid / SUP-clause-mirror: refused by r90 …, refused by the prior counter (regression held)
FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7
CONTROLS=PASS                                                                  # exit 0
```
(`receipts/c2-controls.txt`)

Harm: no curated entry's verdict moved — `git diff f54a45ed 9bad1201 -- corpus/knowledge/` is empty and the registry
diff is the one `S220` row with its `used-by` cell.

**The frozen kill rule K2 fires — the honest stop (Amendment 8).** The three commands above reproduce the frozen lines
on the clean tree, but two *tree forgeries* leave the whole kit green. This seat re-derived both independently on
scratch copies of the carrier tree:

- **F1 — a quote row outside the parser's shape is invisible.** One row appended to `## Located quotes` in
  `corpus/knowledge/provenance-recording-r85.md`, with the first cell `X9` instead of a `Q\d+` id:
  `python3 -B corpus/evidence/round90/curation-r90.py --root <forged copy>` → `QUOTES_LOCATED=20/20 …
  LEGS_MEASURED=10/10 VERDICT fields_hold=1`, `CURATION_R90=PASS`, exit 0 (`receipts/c2-forge-f1.txt`); the mutants
  battery still prints `MUTANTS_KILLED=10/10 … PRIOR_R89_SURVIVORS=2/2`, exit 0 (`receipts/c2-f1-mutants.txt`); the
  controls still print `FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 / CONTROLS=PASS`, exit 0
  (`receipts/c2-f1-controls.txt`). A fabricated quote that appears in no capture is neither counted nor refused.
- **F2 — a cited source's status is read by no leg.** The `status` cell of the cited row `S215` flipped `mined` →
  `rejected` in `corpus/SOURCES.md` (`receipts/c2-forge-f2.txt`, one cell changed): the counter prints the identical
  summary and `CURATION_R90=PASS`, exit 0; mutants `MUTANTS_KILLED=10/10 …`, exit 0 (`receipts/c2-f2-mutants.txt`);
  controls `FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 / CONTROLS=PASS`, exit 0 (`receipts/c2-f2-controls.txt`).

K2 says "a tree forgery is accepted" kills the claim. Both forgeries are tree forgeries in the claim's subject, and the
full three-command kit accepts them. A kill rule is not a wording clause and cannot be rewritten after a seat has
scored (§9), so **C2 does not verify as frozen** — an honest stop, not a narrowed pass. The enforceable property of the
round-90 counter is its printed fields plus the seven listed tree-forgery classes; it does **not** refuse a quote row
outside the parser's shape, nor a status flip on a cited source. Round 91 owns the repairs (Amendment 8).

Named limits stand as frozen: `MIN_TOKENS=7` is a measured floor, not a content check; the qid-set pin guards label
identity, not quote content; the witness exercises each detector function on synthetic strings, so a substitution in a
*caller* that bypasses the function is not witnessed; the superseder-own-read clause is vacuous on the real registry
(`SUP_CLAUSE_CHECKED=0`) and its non-vacuity is the battery's mirror case. Amendment 5 narrows "die on `LEG_FAIL
WITNESS`" to the observed death line in the committed battery's run (a counter edit that forces the WITNESS leg ok, or a
crashing counter, still scores 10/10 — `R90ReviewerC2` F1/F2); Amendment 6 records that the before-receipt
`c2-subst-before.txt` is a derived survival marker (`SURVIVOR_PRIOR … rc=0`), not a raw verdict line.

### C3 — `C3-TALLY-R90` (freshness) — **verified on the wording narrowed by Amendments 1 and 10**

At the carrier `9bad1201` the check prints, exit 1:

```
python3 -B corpus/evidence/round90/skill-tally-r90.py --root .
STALE_TALLY PASS (275 cases, 0 skipped) != tool 283/0      (×9)
TALLY_ROWS=9 STALE_TALLIES=9/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=FAIL
```
(`receipts/c3-at-carrier.txt`; identical to the committed before-receipt `controls/receipts/c3-before.txt`.) The nine
current cells still read `PASS (275 cases, 0 skipped)` at the carrier — `git show 9bad1201:SKILL.md | grep -c "PASS (275
cases, 0 skipped)"` → 9, and `grep -c "PASS (283 cases, 0 skipped)"` → 0. The repair lands after the wave.

With the nine current cells at 283 (the working tree's `SKILL.md` edit, which touches **only** those nine cells —
`git diff --numstat SKILL.md` → `9  9`, and every changed line is a `PASS (<n> cases, <m> skipped)` cell, zero other
lines), the check re-derives to the tool's own verdict:

```
python3 -B corpus/evidence/round90/skill-tally-r90.py --root . --selftest corpus/evidence/round90/controls/selftest-r90.txt
TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=PASS  # exit 0
```
(`receipts/c3-worktree.txt`; the same line is committed as `corpus/evidence/round90/after/c3-after-receipt.txt`.)

Discrimination, re-measured by this seat:

- a scratch copy of the carrier tree with the nine current cells rewritten to 283 → `STALE_TALLIES=0/9 … PASS`, exit 0
  (`receipts/c3-discrimination.txt`);
- the same tree with the binding rule widened to every occurrence → `STALE_TALLY PASS (256 cases, 0 skipped) …`,
  `TALLY_ROWS=12 STALE_TALLIES=3/12 … FAIL`, exit 1 (`receipts/c3-mutant-widened-rule.txt`) — the three historical
  occurrences are bound and refused;
- the same tree with the historical line at `SKILL.md:188` rewritten to carry the host note's `Selftest` phrase → the line
  becomes a bound row and is refused: `TALLY_ROWS=10 STALE_TALLIES=1/10 … FAIL`, exit 1
  (`receipts/c3-historical-lookscurrent.txt`) — the shallower recognition of named limit 2, observed.

The nine current rows are `SKILL.md` lines 86–93 (the eight Gates-table rows whose first cell names `research-gate`) and
line 781 (the `Selftest` host note). The three unbound historical occurrences are line 186 (`PASS (256 cases, 0 skipped)`,
a round-34 quotation inside the round-25 historical paragraph), line 188 (`PASS (161 cases, 0 skipped)`, round-25 final)
and line 640 (`PASS (215 cases, 0 skipped)`, round-27) — enumerated independently of the tool's own rule.

Named limits stand as frozen: the check binds the two numbers in each current cell and does not verify that cases
276–283 are the `bash-pin-override-*` cases the note names; historical occurrences are recognised by shallower structure
than the binding rule, so a historical line rewritten to look current would be bound and must then also re-derive (measured
above). Amendment 10 narrows the `EXPECTED_CASES=283` clause to the **pair** of runs: the before-state must print
`STALE_TALLIES=9/9 EXPECTED_CASES=283` (exit 1) *and* the landing run `STALE_TALLIES=0/9` (exit 0), because reading the
expected number out of `SKILL.md` instead of the tool's verdict leaves the landing run's printed line identical
(`R90MutBattery`'s `expected-count-read-from-file` mutant). Both legs are reproduced above.

## Mistakes

Seven errors of this round's own making, each with the pointer, the rule that would have caught it, and a fix shown able to
fail. Rows 1–3 and 5 are the rows the L1 has mined as QUALITY 196–201; rows 4, 6 and 7 are this seat's additions, each
re-measured here.

1. **Class: an id reserved to a fixture is spent on a registry row.** The round's first plan named the new source `S219`
   — the id the round-89 control battery uses for its mirror row — and the collision was discovered before any row was
   written. **Evidence pointer:** `plans/round-90.md` §Pre-freeze repairs item 6; the mirror row at
   `corpus/evidence/round89/curation-r89-controls.py:41`; the ledger residue at
   `corpus/evidence/round57/refetch.tsv:186-188` (the `S219` gnu.org failure, the `S219` man7.org success at `09:44:57Z`,
   the `S220` man7.org success at `09:52:31Z`). **Captured-by:** none — the census validates the real registry, never a
   scratch mirror; round 89's lesson records the same class for `S099` but as a *fixture* id, and nothing checks the
   reverse direction (a real row landing on a fixture id). **Fix:** the row is `S220`, `S219` stays reserved, and the
   failed attempt stays a ledger row with no registry row. Shown able to fail: appending one real `S219` row to a copy of
   `corpus/SOURCES.md` and re-running the round-89 battery prints `CASE_DEVIATION SUP-clause-mirror` and
   `FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=6/7 / CONTROLS=FAIL`, exit 1
   (`receipts/s219-id-collision.txt`).
2. **Class: a freshness rule bound historical quotes as if they were current.** The first `skill-tally-r90.py` receipt read
   `TALLY_ROWS=12 STALE_TALLIES=12/12` — the 256/161/215 historical quotations included. **Evidence pointer:** the
   counter's own before-leg, read line by line; the round's `claims.md` C3 sentence names exactly nine bound rows and three
   unbound ones; the plan's Amendment 1 corrects the labels. **Captured-by:** the claim's own before receipt — the
   twelve-row count was printed by the check itself, so the rule had to be read, not assumed. **Fix:** the rule binds only
   the eight Gates-table `research-gate` rows plus the host-note `Selftest` line; the rest are printed as
   `OTHER_OCCURRENCES=3` and not bound. Shown able to fail: this seat's widened-rule mutant binds all three historical
   occurrences and refuses the tree — `TALLY_ROWS=12 STALE_TALLIES=3/12 … FAIL`, exit 1
   (`receipts/c3-mutant-widened-rule.txt`).
   *This seat's addition to that row: the frozen C3 prose also names the wrong rounds — "round-25/32/34/37 quotes" —
   while the three the binding rule sees are `SKILL.md:186` (256, a round-34 quotation inside the round-25 historical
   paragraph), `:188` (161, round-25 final) and `:640` (215, round-27); no `SKILL.md` line carries a round-37 two-number
   tally. Shown able to fail: re-derive the three occurrences by line and read each line's own text against its round
   label.*
3. **Class: two writers produced one receipt.** The first `c3-before.txt` held two interleaved runs (`TALLY_ROWS=9` and
   `TALLY_ROWS=12`) in one file. **Evidence pointer:** the receipt did not parse as one run — the two summaries are
   interleaved in the same body. **Captured-by:** the receipt itself; nothing else reads it before the driver does.
   **Fix:** the before-state is rerun alone and re-read, and the receipt carries one run. Shown able to fail: a receipt
   with two summaries has no single `TALLY_ROWS` to compare — the check's own before-leg is the only witness.
4. **Class: a binding rule that recognises its records by shallower structure than it binds on.** The tally check decides
   what is a current cell with a phrase test (`"Selftest `PASS (" in line`) and binds with a numeric pattern
   (`PASS \((\d+) cases, (\d+) skipped\)`). The recognition is therefore wider than the binding: any line carrying the
   host note's phrase becomes a bound row. **Evidence pointer:** `corpus/evidence/round90/skill-tally-r90.py`
   (`current()` / `TALLY_RE`); the frozen named limit 2 says as much. **Captured-by:** none — QUALITY 187/193 cover field
   enumeration and diagnostic naming, not a recogniser's specificity. **Fix:** the check binds only the nine current cells
   and prints the rest as `OTHER_OCCURRENCES=3`, and the limit is named rather than papered over. Shown able to fail: the
   widened rule binds the three historical occurrences and refuses the tree (`TALLY_ROWS=12 STALE_TALLIES=3/12 … FAIL`,
   exit 1 — `receipts/c3-mutant-widened-rule.txt`), and rewriting one historical line to carry the host note's phrase
   makes it bound and refused (`TALLY_ROWS=10 STALE_TALLIES=1/10 … FAIL`, exit 1 —
   `receipts/c3-historical-lookscurrent.txt`).
5. **Class: a number carried over from a neighbouring record.** The wave's own seat text for this section specifies
   `words=11` for the `S220` Gate quote; the quote is ten tokens and the lane's gate tool computes the count itself, so
   `words=11` is refused (`WORDS`). The `11` is round 89's `S218` word count. **Evidence pointer:**
   `.ufo/waves/round-90/build_spec.py:243` (`words=11`) against `corpus/lessons/round-89.md:19` (`S218 … words=11`) and
   `tools/gate-records.py` (`n = len(quote.split())`; `WORDS`). **Captured-by:** none — the gate tool refuses the record,
   but nothing refused the *instruction*. **Fix:** the Gate line carries `words=10`, the count of the quote it actually
   prints, and it is verified with the lane's own tool before filing. Shown able to fail: the same line with `words=11`
   prints `S220 FAIL WORDS`, exit 1 (`receipts/gate-records-words11.txt`); with `words=10` it prints `S220 OK`, exit 0
   (`receipts/gate-records-words10.txt`).
6. **Class: a command form that names two different trees.** The wave context states the C1 counting command as
   `verify --root <lane> --repo <clone at 9bad1201>`. The driver's self-pin resolves the scoring files' paths *relative to
   `--repo`*, so a driver that does not live inside `--repo` puts every scoring file outside the pinned tree and the pin
   leg reports all of them drifted. **Evidence pointer:** `control-driver-r90.py` (`self_pin`: `os.path.relpath(__file__,
   repo)`); the frozen claim's own form is `--root . --repo .` (`corpus/evidence/round90/claims.md` C1 sentence; the
   machine form in `.ufo/waves/round-90/claims.json`), which is the form that passes. **Captured-by:** none — QUALITY 189
   covers a missing revision pin, not a pin resolved against the wrong root. **Fix:** use the frozen `--root . --repo .`
   form. Shown able to fail: `--root <lane> --repo <clone>` prints `RECEIPT SELF_PIN FINDING SELF_DRIFT …` (every scoring
   file) and `CONTROL_DRIVER_R90=FAIL`, exit 1 (`receipts/c1-verify-lane-root-vs-clone-repo.txt`), while the same command
   with `--root <clone> --repo <clone>` prints `SELF_PIN OK` and `CONTROL_DRIVER_R90=PASS`, exit 0
   (`receipts/c1-verify-clone-root-and-repo.txt`).
7. **Class: a tree forgery the whole kit accepts is a claim failure, not a wording clause.** The round's C2 counter
   accepts a fabricated quote row outside its parser's shape and a `status` flip on a cited source — every field, every
   leg and every printed count unchanged — and the frozen kill rule K2 says that kills the claim. **Evidence pointer:**
   `receipts/c2-forge-f1.txt` (`QUOTES_LOCATED=20/20 … CURATION_R90=PASS`, exit 0 with an `X9` row appended to
   `## Located quotes`), `receipts/c2-forge-f2.txt` (`S215`'s status cell `mined` → `rejected`, same output, exit 0), and
   the accompanying batteries (`receipts/c2-f1-mutants.txt`, `c2-f1-controls.txt`, `c2-f2-mutants.txt`,
   `c2-f2-controls.txt` — all exit 0, all green). **Captured-by:** none — the round's own control battery covers seven
   *named* forgery classes, and a forgery outside the parser's shape belongs to none of them; the wave's
   `R90ExecC2Forge` found it (`w1/R90ExecC2Forge.md` F1/F2). **Fix:** the honest stop (Amendment 8) — C2's enforceable
   property is published, and round 91 owns the repairs (count every row in `## Located quotes` or refuse a non-`Q` /
   non-3-cell row explicitly; cross-check every citation's `status` and `used-by`). Shown able to fail: the two forgeries
   above are accepted by all three commands, so the claim cannot be re-scored as a pass on the current instrument.

Seat-trailer discipline: every seat's prompt requires a `VERDICT:` trailer; the scribe tallies a missing one as a
seat-discipline finding rather than a hold (round-88 routed defect 7).

## Spot-check intake

Round 89's non-author check routed seven defects (`corpus/lessons/round-89-verifier-spotcheck.md` §Routed defects).
Disposition, one row each:

| routed item | disposition | pointer |
|---|---|---|
| 1. C2's after-line quotes an unprinted token (`VERDICT fields_hold=1`) | **fixed** — the r90 counter computes the verdict leg before the summary and prints the token pair on the passing path; `grep -c` over the transcript → 2, against 0 for the r89 counter on the same tree. (C2 itself honest-stops on K2 — see the C2 block — but the token now exists on the passing path.) | `receipts/c2-counter.txt`, `receipts/c2-r89-prior.txt`; `corpus/evidence/round90/controls/receipts/c2-prior-landing.txt` |
| 2. Attack-share arithmetic (7/12 stated vs 6/12 in the ledger) | **conformance requirement, still open** — the wave spec has 13 seats; `.ufo/waves/round-90/claim-falsification.tsv` did **not** exist at the carrier and is still absent from the working tree, so the share is the ledger's to state at filing and the lesson must quote the ledger, not a hand count. The L1's in-progress lesson states six attack seats of thirteen (46 %); that figure is the ledger's to confirm | `.ufo/waves/round-90/w1-spec.json` (13 items); the ledger file is absent at the carrier and in the working tree; `corpus/lessons/round-90.md` §Spot-check intake |
| 3. Work-performed frontier bullet undercounts its own round | **conformance requirement** — this lesson's own counts (three claim outcomes, seven mistake rows, seven intake rows) must match its tables; the L1 owns the report's frontier bullet | this file; `.ufo/waves/round-90/w1/R90ScribeLesson.md` |
| 4. Amendment 8's finding prints `LEGS_MEASURED=8/9` where the counter prints `8/8` | **fixed by construction** — the r90 summary prints the full leg set, `LEGS_MEASURED=10/10`, and the verdict leg is inside those ten (`VERDICT fields_hold=1 legs_ok=10/10`) | `receipts/c2-counter.txt`; `plans/round-90.md` §Pre-freeze repairs item 2 |
| 5. Registry freshness — `SKILL.md` tallies at 275 vs the tool's 283 | **fixed by C3** — the check re-derives each of the nine current cells from the tool's own selftest verdict; stale at the carrier (`STALE_TALLIES=9/9`, exit 1), passing at the landing state (`STALE_TALLIES=0/9`, exit 0) | `receipts/c3-at-carrier.txt`, `receipts/c3-worktree.txt`, `receipts/c3-discrimination.txt` |
| 6. Carried debt, re-flagged: (a) round-74 source-blind order oracle, (b) QUALITY 173's successful-refused record form, (c) r80 backlog Gate ids | **not touched** — no instrument in this round touches them; re-flagged, unchanged | `plans/round-90.md` §Claim selection ("Rejected as claims") |
| 6(d). Amendment 7's control-driver discipline — overwrite-before-read, substring match, no revision pin, vacuous harm row | **fixed by C1** — the six classes are each refused by name (`TOKEN_DETACHED`, `PIN_MISSING`, `PIN_MISMATCH`, `PREDICATE_SHORT`, `DUPLICATE_KEY`) and each accepted by the unchanged r89 driver; the receipts are read before any fresh run and the digests are unchanged | `receipts/c1-forgeries.txt`, `receipts/c1-verify-lane-root.txt`, `receipts/receipts-sha-before.txt` / `receipts-sha-after.txt` |
| 6(e). Amendment 9's detector-substitution witness for C2 and C1 named limit 3 | **fixed by C2** — `locates` forced true and `unentailed_row` forced false die on `LEG_FAIL WITNESS 7/8 bad=1`; the same two substitutions survive r89 (`SURVIVOR_PRIOR … rc=0`) | `receipts/c2-mutants.txt` |
| 7. Named limits stay named in the frozen claims | **carried** — C1 limits 1–3, C2 limits 1–4 and C3's two named limits are in `claims.md` unchanged, and each is restated above with the measurement that shows it is still open | `corpus/evidence/round90/claims.md`; `receipts/c3-historical-lookscurrent.txt` (C3 limit 2 observed) |

## Trends

| trend | verdict | evidence (verified by this seat) |
|---|---|---|
| expansion | unchanged in depth, +1 mined row | `corpus/knowledge/*.md` 97 → 97 (`git ls-tree -r --name-only` at `f54a45ed` and `9bad1201`); registry 218 → 219 rows, the one added row being `S220` (tier A, `mined`, `used-by = corpus/evidence/round90/claims.md`); `git diff f54a45ed 9bad1201 -- corpus/SOURCES.md` is exactly one added line; `git diff f54a45ed 9bad1201 -- corpus/knowledge/` is empty. The round's gain is in instruments, not in new ground. |
| quality | improved (C1 and C3 verified; C2's instrument gains are reported but not admitted — the claim honest-stopped on K2) | C1 `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS` (exit 0) with `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`; C2's three commands print `CURATION_R90=PASS` with `LEGS_MEASURED=10/10`, `VERDICT fields_hold=1 legs_ok=10/10 DETECTOR_WITNESS=8/8`, `MUTANTS_KILLED=10/10 … PRIOR_R89_SURVIVORS=2/2`, `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7` — and yet the claim does not verify, because two tree forgeries leave the whole kit green (`receipts/c2-forge-f1.txt`, `c2-forge-f2.txt`); C3 `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=PASS` at the landing state against `STALE_TALLIES=9/9` at the carrier. The subject tools are unchanged (`git diff f54a45ed 9bad1201 -- tools/gate-records.py` and `-- tools/research-gate.sh` both empty), so no domain record could move; `tools/lane-preflight.py` → `PREFLIGHT=8/8 FAILED=none` (exit 0); census exit 0 at start and end with the same five `W04`. |
| discernment | improved | The wave fired the *sentence*, not the predicate: the plan carries ten amendments (C3's prose labels; C1's "agrees" narrowed to exit + tokens + predicates; C1's "six committed receipts" narrowed to the six `expected.tsv` rows; C1's header/pin/fresh clauses narrowed with named limits 4–6; C2's "die on `LEG_FAIL WITNESS`" narrowed to the observed death line; C2's before-receipt named a derived marker; C1's counting command given its `--work`; C2 ruled an honest stop; C1's named limits 4–6 recorded; C3's expected-number clause bound over the before+landing pair), each naming the artifact and the narrower property. Seven of this round's own errors are mined above, each with a fix shown able to fail — including two this seat found by running the lane's own gate tool against its own lesson text (`words=11` → `FAIL WORDS`) and by running the frozen command with a mixed `--root`/`--repo` (`SELF_DRIFT`, exit 1). The C3 recogniser's shallowness was observed, not assumed (a historical line rewritten to look current becomes bound and refused), and the two C2 forgeries were re-derived independently rather than taken from the wave's report. |
