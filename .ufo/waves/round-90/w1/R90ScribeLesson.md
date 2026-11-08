# R90ScribeLesson — round-90 lesson settlement draft

Seat: scribe. Lane `chousa`, round 90. **Draft only — the L1 integrates.**
Draft: `.ufo/waves/round-90/w1/R90ScribeLesson/lesson-settlement-draft.md`.
Receipts cited: `.ufo/waves/round-90/w1/R90ScribeLesson/receipts/` (28 files).

Scope: read `corpus/evidence/round90/claims.md`, `plans/round-90.md`, the receipts under `corpus/evidence/round90/controls/`,
`corpus/lessons/round-89.md` (shape) and `corpus/lessons/round-89-verifier-spotcheck.md` (routed defects 1–7); then
re-measured all three claims from committed bytes and drafted the lesson.

## Behaviour

Three claims re-measured from committed bytes; every number in the draft was produced by a command this seat ran, and every
receipt the draft cites is copied into the wave output folder.

**C1 — `C1-DRIVER-R90` (operability): verified on the wording narrowed by Amendments 2, 3, 4, 7 and 9.**
`python3 -B corpus/evidence/round90/control-driver-r90.py verify --root . --repo . --rev 8d9893b42eb22690ea5f920ab87fd7e1810b847a --receipts-rev 9bad12011187d114ba2c4588c5df08a21ab28145`
→ seven `OK`/`SELF_PIN OK` lines and `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS`,
exit 0 (`receipts/c1-verify-lane-root.txt`; reproduced in a clean `git clone --shared` at the carrier,
`receipts/c1-verify-clone-root-and-repo.txt`).
`control-forgeries-r90.py` → `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`, exit 0 (`receipts/c1-forgeries.txt`).
The nine receipts' sha256 digests are identical before and after the run (`receipts/receipts-sha-before.txt` /
`receipts-sha-after.txt`).

**C2 — `C2-CURATION-R90` (calibration): honest stop — the frozen kill rule K2 fires.**
`curation-r90.py --root .` → `LEGS_MEASURED=10/10 VERDICT fields_hold=1`, `VERDICT fields_hold=1 legs_ok=10/10
DETECTOR_WITNESS=8/8`, `CURATION_R90=PASS`, exit 0, `grep -c 'VERDICT fields_hold=1'` → 2 (`receipts/c2-counter.txt`);
the r89 counter on the same tree prints 0 of the token (`receipts/c2-r89-prior.txt`).
`curation-r90-mutants.py` → `MUTANTS_KILLED=10/10 COUNTER_DETECTED=9 BATTERY_DETECTED=1 PRIOR_R89_SURVIVORS=2/2`, exit 0
(`receipts/c2-mutants.txt`). `curation-r90-controls.py` → `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7`, exit 0
(`receipts/c2-controls.txt`).
But the three commands are not the claim. I re-derived the two tree forgeries independently on scratch copies of the
carrier tree: a fabricated quote row whose first cell is not a `Q\d+` id, and a cited source's registry `status` flipped
`mined` → `rejected`. Both leave the whole kit green at exit 0 (`receipts/c2-forge-f1.txt`, `c2-forge-f2.txt`,
`c2-f1-mutants.txt`, `c2-f1-controls.txt`, `c2-f2-mutants.txt`, `c2-f2-controls.txt`). K2 says "a tree forgery is
accepted" kills the claim; a kill rule is not a wording clause. This matches the L1's Amendment 8 and the L1's in-progress
lesson, and the draft reports C2 as an honest stop, not a pass.

**C3 — `C3-TALLY-R90` (freshness): verified on the wording narrowed by Amendments 1 and 10 (the before+landing pair).**
At `9bad1201`: `STALE_TALLIES=9/9 EXPECTED_CASES=283 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=FAIL`, exit 1
(`receipts/c3-at-carrier.txt`). With the nine current cells at 283 (the working tree's `SKILL.md` edit — `git diff
--numstat SKILL.md` → `9  9`, every changed line a `PASS (<n> cases, <m> skipped)` cell, zero other lines):
`TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=PASS`, exit 0
(`receipts/c3-worktree.txt`). Discrimination re-measured three ways (`receipts/c3-discrimination.txt`,
`c3-mutant-widened-rule.txt`, `c3-historical-lookscurrent.txt`).

**Gate.** The `S220` Gate record in `url/admit` form, with the refetch row's values, plus the `S219` reservation note and
its measurement (`receipts/s219-id-collision.txt`), are in the draft's `## Gate`.

## Gates run by this seat (all green unless stated)

| gate | command | result |
|---|---|---|
| Gate record (S220) | `python3 -B tools/gate-records.py verify --root . --repo . <record>` | `S220 OK`, `GATE_RECORDS files=1 records=1 ok=1 fail=0`, exit 0 (`receipts/gate-records-words10.txt`) |
| Gate record, `words=11` | same, on the record with `words=11` | `S220 FAIL WORDS`, exit 1 (`receipts/gate-records-words11.txt`) — **finding** |
| Gate record, tier / sha / fetched deviations | same, one field changed at a time | `FAIL TIER`, `FAIL CAPTURE_SHA`, `FAIL REFETCH`, exit 1 each (`receipts/gate-records-tierB.txt`, `-badsha.txt`, `-wrong-fetched.txt`) |
| Gate record for S219 | same, on an `url/unreach` S219 record | `S219 FAIL REGISTRY`, exit 1 (`receipts/gate-records-s219-unreach.txt`) — S219 has no registry row |
| Source census | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` | exit 0, `chousa ok …/corpus/SOURCES.md`, same five pre-existing `W04` |
| Lane preflight | `python3 -B tools/lane-preflight.py` | `PREFLIGHT=8/8 FAILED=none ENV=none SKIPPED=none`, exit 0 |
| Instrument pins | sha256 of each `instrument-pins.txt` path at both `8d9893b4` and `9bad1201` | 11/11 OK at both revisions |
| Scope | `git diff --name-only f54a45ed 9bad1201` | 26 paths, all under `corpus/evidence/round90/`, `corpus/SOURCES.md`, `corpus/evidence/round57/refetch.tsv`, `plans/round-90.md`, `.ufo/waves/round-90/`; `corpus/knowledge/` and `tools/` empty |

## Touched surfaces

Written (only these):
- `.ufo/waves/round-90/w1/R90ScribeLesson/lesson-settlement-draft.md` — the draft lesson.
- `.ufo/waves/round-90/w1/R90ScribeLesson/receipts/` — 28 cited transcripts and probe records.
- `.ufo/waves/round-90/w1/R90ScribeLesson.md` — this report.

Not written: any lane source, instrument, receipt, plan, registry row, `LOG.md`, `SCORECARD.md`, `SHONEN.md`,
`QUALITY.md`, `MANIFEST.json`, `.ufo/state`, `scripts/`, `considerthese/`, any sibling repo. No git/jj mutation, no commit,
no push. No network fetch (C3's own selftest is local; the S220 capture was already committed by the L1 in `aa7d4223`).
No `sudo`, no sysctl, no service restart. Scratch `/fast/scratch/hyaku/chousa-r90/R90ScribeLesson/` deleted on yield.

## Findings

1. **The wave's seat text specifies `words=11` for the `S220` Gate quote; the correct value is `10`.**
   The quote `Select only those matches that exactly match the whole line.` is ten whitespace-separated tokens, and
   `tools/gate-records.py` computes `n = len(quote.split())` and refuses any other count (`WORDS`).
   Command: `python3 -B tools/gate-records.py verify --root . --repo . <record>` → `S220 FAIL WORDS`, exit 1
   (`receipts/gate-records-words11.txt`); with `words=10` → `S220 OK`, exit 0 (`receipts/gate-records-words10.txt`).
   The `11` is round 89's `S218` count (`corpus/lessons/round-89.md:19`) copied across. **The L1 must land `words=10`** or
   the lesson's `## Gate` fails the lane's own gate.
2. **The frozen C3 prose names the wrong historical rounds.** `claims.md` says "round-25/32/34/37 quotes"; the three the
   binding rule sees are `SKILL.md:186` (256 — a round-34 quotation inside the round-25 historical paragraph), `:188`
   (161 — round-25 final) and `:640` (215 — round-27). No round-37 two-number quote exists at the carrier. Already
   narrowed by the plan's Amendment 1; the draft's `## Mistakes` row 2 carries the measured lines.
3. **The wave context's C1 command form does not pass.** `verify --root <lane> --repo <clone at 9bad1201>` →
   `RECEIPT SELF_PIN FINDING SELF_DRIFT` (every scoring file) and `CONTROL_DRIVER_R90=FAIL`, exit 1
   (`receipts/c1-verify-lane-root-vs-clone-repo.txt`): `self_pin` resolves the scoring files' paths relative to `--repo`,
   so a driver outside `--repo` puts every scoring file outside the pinned tree. The frozen claim's own form is
   `--root . --repo .` (`claims.md`, `claims.json`), which passes (exit 0). **Use the frozen form.**
4. **The `S220` capture bytes are not in the freeze.** `git ls-tree 8d9893b4 corpus/captures/` lists no
   `e6ec761219e8044b0e9e067a`; the capture lands in `aa7d42237364509d6647d10c93ee421d4626a3ca`, after the carrier. A Gate
   record verified against a carrier tree fails `CAPTURE_PATH,CAPTURE_SHA,QUOTE_ABSENT,REFETCH`. The lesson's `## Gate`
   must be verified against a tree containing `aa7d4223` or later — the lesson lands after that commit.
5. **The `S219` reservation re-derived.** A real `S219` registry row appended to a copy of `corpus/SOURCES.md` makes the
   round-89 control battery print `CASE_DEVIATION SUP-clause-mirror` and `FORGERY_REFUSED=7/7
   PRIOR_ACCEPTED_FORGERY=6/7 / CONTROLS=FAIL`, exit 1 (`receipts/s219-id-collision.txt`); unmodified, the same command
   prints `PRIOR_ACCEPTED_FORGERY=7/7 / CONTROLS=PASS`, exit 0.
6. **The ledger keeps two `S219` rows, one of them a success.** `corpus/evidence/round57/refetch.tsv:186` is the failed
   gnu.org attempt (curl rc=28, http 000, no bytes); `:187` is a *successful* man7.org fetch under `S219` at `09:44:57Z`
   with the same capture key and the same `raw_sha256`/`txt_sha256` as the `S220` row at `:188`. The `S219` success is the
   id-rename residue of one transfer; it is not a registry row and is not citable, and a Gate record citing it fails
   `REFETCH` (`receipts/gate-records-wrong-fetched.txt`).
7. **C3's recogniser is shallower than its binding rule.** The check decides "current cell" by the phrase
   `Selftest `PASS (` and binds by the numeric pattern. A historical line rewritten to carry that phrase becomes a bound
   row and is refused: `TALLY_ROWS=10 STALE_TALLIES=1/10 … FAIL`, exit 1
   (`receipts/c3-historical-lookscurrent.txt`). Widening the rule to every occurrence binds the three historical rows and
   refuses the tree: `TALLY_ROWS=12 STALE_TALLIES=3/12 … FAIL`, exit 1 (`receipts/c3-mutant-widened-rule.txt`). This is
   the frozen named limit 2, observed rather than assumed.
8. **The falsification ledger does not exist yet.** `.ufo/waves/round-90/claim-falsification.tsv` is absent at the carrier
   and in the working tree; the wave spec has 13 seats. The attack share is the ledger's to state at filing — round 89's
   routed defect 2 was exactly this arithmetic, so the lesson quotes the ledger rather than a hand count.
9. **C2 does not verify as frozen, and this seat re-derived the two forgeries independently.** A fabricated quote row
   whose first cell is not a `Q\d+` id is dropped by the width/qid filter before counting, so it appears in no capture yet
   `QUOTES_LOCATED=20/20`; a cited source's registry `status` flipped `mined` → `rejected` moves no field and no leg.
   Both leave the counter, the mutants battery and the controls battery all green at exit 0
   (`receipts/c2-forge-f1.txt` — `CURATION_R90=PASS`, exit 0; `receipts/c2-forge-f2.txt` — same; the four battery
   receipts in the same folder). The frozen kill rule K2 fires, so C2 is an honest stop (the L1's Amendment 8 and the
   L1's in-progress lesson say the same; this seat did not take that from the wave's report).
10. **The draft was reconciled against the L1's ten amendments.** The draft's C1/C2/C3 verdicts were written against the
   frozen text and then changed to the amendments' rulings (C2: verified → honest stop; C1 and C3: verified → verified on
   the narrowed wording). The reconciliation note at the top of the draft names the three changes so the L1 can check
   them against its own rulings.

## Out of scope

- No new lesson text beyond the draft; the L1 owns the lesson file, `LOG.md`, `SCORECARD.md`, `SHONEN.md` and any
  `QUALITY` criterion mined from the draft's five mistake rows.
- Round-89's routed defects 6(a)–6(c) (round-74 order oracle, QUALITY 173, r80 Gate-id backlog) are carried, untouched —
  no instrument in this round reaches them.
- The `after/` receipts and `controls/selftest-r90.txt` are untracked in the lane working tree at the time of writing;
  the L1's landing must commit them if they are to be citable.
- No `git`/`jj` mutation of the lane or fleet repo, no commit, no push, no sibling-repo read beyond `git ls-files`/`grep`
  of the lane.

## Artifacts

- Draft: `.ufo/waves/round-90/w1/R90ScribeLesson/lesson-settlement-draft.md`
- Receipts: `.ufo/waves/round-90/w1/R90ScribeLesson/receipts/` (34 files) — `c1-verify-lane-root.txt`,
  `c1-verify-clone-root-and-repo.txt`, `c1-verify-lane-root-vs-clone-repo.txt`, `c1-forgeries.txt`,
  `receipts-sha-before.txt`, `receipts-sha-after.txt`, `c2-counter.txt`, `c2-mutants.txt`, `c2-controls.txt`,
  `c2-r89-prior.txt`, `c2-forge-f1.txt`, `c2-forge-f2.txt`, `c2-f1-mutants.txt`, `c2-f1-controls.txt`,
  `c2-f2-mutants.txt`, `c2-f2-controls.txt`, `c3-at-carrier.txt`, `c3-worktree.txt`, `c3-discrimination.txt`,
  `c3-mutant-widened-rule.txt`, `c3-historical-lookscurrent.txt`, `s219-id-collision.txt`,
  `gate-record-s220-words10.md`, `gate-record-s220-words11.md`, `gate-record-s220-tierB.md`,
  `gate-record-s220-badsha.md`, `gate-record-s220-wrong-fetched.md`, `gate-record-s219-unreach.md`,
  `gate-records-words10.txt`, `gate-records-words11.txt`, `gate-records-tierB.txt`, `gate-records-badsha.txt`,
  `gate-records-wrong-fetched.txt`, `gate-records-s219-unreach.txt`.

VERDICT: R90ScribeLesson C1 held — the r90 driver verifies the six committed receipts at the carrier
(`COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS`, exit 0) and refuses all six forgery
classes, so C1's predicate is met on the wording narrowed by Amendments 2, 3, 4, 7 and 9.
VERDICT: R90ScribeLesson C2 fired — the frozen kill rule K2 fires: a fabricated quote row outside the parser's shape
and a cited source's `status` flip are both accepted by the counter, the mutants battery and the controls battery at exit
0, so the claim does not verify as frozen (the L1's Amendment 8 rules this an honest stop).
VERDICT: R90ScribeLesson C3 held — the tally check re-derives all nine current cells to the tool's live verdict
(`STALE_TALLIES=0/9 … SKILL_TALLY_R90=PASS`, exit 0) at the landing state and refuses the carrier's nine stale cells
(`STALE_TALLIES=9/9`, exit 1), with the discrimination legs reproduced; the predicate is met on the wording narrowed by
Amendments 1 and 10, once the L1 commits the `SKILL.md` 275→283 repair (staged in the working tree, not yet committed).
