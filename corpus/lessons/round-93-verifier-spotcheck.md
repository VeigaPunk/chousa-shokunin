author: hyaku closure (non-author integrator, @m_zfl)

# Round 93 verifier spot-check — chousa (non-author, hyaku closure)

Date 2026-11-08. Judge: hyaku closure (non-author integrator), lane `chousa`. Base
`206226dc9d9baef620e7d3d30bdac5f9194a459f`; lane HEAD after the round
`af917ae6342df4b9fd3d7a5816b13e9599d45e7f`; freeze F6 `3789608dc8c0eded67f1e5d3840caf0a27522a88`;
carrier C7 `9d03318527f8fe734e67d24f64ac5dce192d43fc`. Report `.ufo/reports/round-93/chousa.md`.

## Conformance (step 1)

- Report identity: `git log --format='%an %H' -- .ufo/reports/round-93/chousa.md` → `chousa-shokunin
  676fc690881dae8f25bd93f1dc45bd53268e6875` (first filing `chousa-shokunin 123bd0e8…`, superseded by the
  filed amendment). Lane identity OK.
- SHONEN: `grep -c '^## SHONEN'` → 1; four `[~]` lines, one per `SHONEN.md` box; the lane wrote no `[x]`.
- Cited lane commits: `84998563`, `b7241252`, `754b62fb`, `d740760e`, `d5c19c54`, `94fbf892`, `596eabc9`,
  `881a541f`, `1362f4b2`, `c1ebb1d9`, `3789608d`, `9d033185`, `9fa45759`, `d4f97cf7`, `af917ae6` — every
  one `git merge-base --is-ancestor <hash> master` exit 0; base `206226dc` is an ancestor of `af917ae6`.
- Clean/pushed: `jj-lane.sh state chousa-shokunin` → `branch=master local=af917ae6 remote=af917ae6 ahead=0
  behind=0 head=detached tracked=0 untracked=0`; `git -C chousa-shokunin status --porcelain` empty;
  `git ls-remote origin refs/heads/master` → `af917ae6…`.
- Report lands last: final report commit `676fc690` (`%ct` 1794149126) > lane HEAD `af917ae6`
  (1794149120). The first filing `123bd0e8` (1794149091) predated the wave-results commit and was
  superseded by the amendment recorded in report §Wave settlement; the filed bytes land after the lane's
  last commit.
- Prompt fidelity: `.ufo/prompts/chousa-round-93.md` equals `templates/round-prompt.md` rendered; a
  difflib over the 140-line template prefix has one difference only — the working-dir line resolves
  `<chousa-repo>` → `chousa-shokunin`. The five child-lane items are present (report path, report-lands-last,
  `## SHONEN` grep, landed-hash citation rule, write scope), the §8 ledger mandate is present, and the L2
  floor (≥8, one batched call; band 8–16) matches MISSION §L2.
- Marker check: real commits, evidence pointers, LOG tie → status **ok**, not a marker.
- Watchdog digest (copied): `2026-11-08T10:48:46-03:00 launch chousa round=93 pgid=1637074
  driver=hyaku-inline attempt=1`; `2026-11-08T11:45:53-03:00 complete chousa round=93; hyaku-inline
  attempt=1`; no dead/wave-error line for round 93.
- Wave: `w1-dispatch.json` counts spawn 12 / resume 0; policy band 8–16, ceiling 256; `w1-results.json`
  12 results, 0 errors; 12 seat reports each carry a `VERDICT:` trailer; attack seats = 3 reviewers + critic +
  mutation-tester + sentinel + revenger + connector = 8/12 (≥25%), one connector.

Status-neutral defects found here: D1 ledger absent (step 2b), D2 stale 22/22 in `SCORECARD.md:4163`, D3
"eleven amendments" vs 12, D4 landing/wave-results hashes not cited in Landed changes, D5 C2/C3 receipts lack
a measured-revision line, D6 the r82 clip residual is not carried. All are routed below.

## Step 2b — pre-file falsification ledger

`python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane chousa --round 93` →
`FINDING ledger-missing /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-93/claim-falsification.tsv`;
`PREFILE-FALSIFICATION: SETUP findings=1`; exit 2. The report omits the required pasted line. **Defect D1**,
a conformance defect, not automatic rejection.

Hand adjudication of the same surface: I read all eight attack seats' reports and verdicts (`R93ReviewerC1`,
`R93ReviewerC2`, `R93ReviewerC3`, `R93CriticClaims`, `R93ExecMutations`, `R93SentinelScope`,
`R93ConnectorSiblings`, `R93RevPrior`) plus the discriminating receipts. Every fired item maps to a committed
fix: H1 battery → clone-based battery (`after/c1-forgeries.txt`), H2/M1 → `PIN_SELF_ROW_ABSENT` /
`PIN_ROW_OUTSIDE` (`REGRESSION_REFUSED=2/2`), M2 → committed `evidence-before/` at `9fa45759`, ReviewerC2
E6/leg/control tokens → Amendments 4/6, ReviewerC3 F1–F3 → Amendments 7–9, M7/M8 → pinned `controls/legs.txt`
+ controls binding `Q_WSQUOT`/`LEG_FAIL WSQUOTE` (`after/c2-m7-stub.txt`, `after/c2-controls.txt`), Scout
F1/F2 → Amendments 10/11. The one unreconciled *number* is C1's frozen `PINNED_FILES=22/22`, explicitly
superseded by Amendment 12 (23/23); the frozen Before `7/16` is the r92 16-row table
(`corpus/evidence/round92/instrument-pins.txt` = 16 rows), while the report's `7/22` is the r93 fixture — a
fixture difference, not a falsification. No unreconciled `falsifies-wording` row was found by hand.

## Per-claim re-check (step 2)

Method: plain measurements over committed bytes (sha256/grep/wc/awk/git); lane counters are
**evidence-verified** from their committed receipts plus structural inspection, not executed by closure
(§Gate standard). All three claims were independently re-derived on their populations.

### C1 `C1-DRIVER-R93` — operability

- `wc -l corpus/evidence/round93/instrument-pins.txt` → 23 rows.
- Per-row loop `git show 9d033185:<path> | sha256sum` over the 22 non-self rows → **22/22 match**.
- `head -n -1 instrument-pins.txt | sha256sum` → `8cf52d1d…bcead`, identical to the file's own row → the
  minus-self digest is real ("minus-self" means over the 22 non-self rows).
- `git rev-parse 3789608d:<path>` vs `9d033185:<path>` for every pinned path → only the six
  `controls/receipts/*.txt` differ between F6 and C7; each instrument pinned at F6 equals its C7 byte.
- `wc -l controls/expected.tsv` → 7 lines (header + 6 rows); `ls controls/receipts/*.txt | wc -l` → 6.
- Committed `after/c1-verify.txt` (rc 0): `RECEIPT PINS OK 23/23 pinned files byte-identical
  RECEIPT_PINS_OK=6/6`; `RECEIPT SELF_PIN OK rev=3789608d… receipts_rev=9d033185…`; `COMMITTED_OK=6/6
  EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=23/23 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=PASS`.
- Committed `after/c1-forgeries.txt` (rc 0): `OK unexecuted-instrument: r93 rc=1 (PIN_DISK_MISMATCH
  path=corpus/evidence/round93/curation-controls-r93.py), r92 rc=0 accepted=True`; `OK receipt-body: r93
  rc=1 (RECEIPT_MISMATCH:c2-prior-landing), r92 rc=0 accepted=True`; `OK derive-from-root: r92 rc=1 (escapes
  base), r93 rc=0`; `OK self-row-deleted: r93 rc=1 (PIN_SELF_ROW_ABSENT)`; `OK row-outside-root: r93 rc=1
  (PIN_ROW_OUTSIDE)`; `FORGERY_REFUSED=2/2 PRIOR_ACCEPTED=2/2 DERIVE_OK=1/1 REGRESSION_REFUSED=2/2
  POSITIVE=pass`.
- Code inspection `control-driver-r93.py`: `pin_report` walks `sorted(pins)` (278–327); `passed` requires
  `checked == len(pins)` and `rchecked == rtotal > 0` (538–540); the three input defaults derive from `--root`
  (404–406); `rel_for(repo, __file__)` resolves the driver's own bytes (354–355).
- Before receipt `evidence-before/c1-prior-accepts.txt`: r92 tree-only form `PINNED_FILES=7` of 22 with both
  tampered trees `CONTROL_DRIVER_R92=PASS`, derive form `SETUP path escapes base`; r92's own 16-row table at
  base gives 7/16.

Verdict: **verified**, with the Amendment 12 number correction (the landing population is 23 rows; the frozen
sentence's 22/22 is superseded and named).

### C2 `C2-CURATION-R93` — calibration

- `awk` count of data rows in the two entries' `## Located quotes` → 13 + 7 = **20** = `Q_ROWS=20`; every
  data row is a 3-cell `Qn | S### | quote` row, no whitespace-only quote cell on the clean tree
  (`Q_WSQUOT=0`).
- `wc -l controls/legs.txt` → 15 names = `EXPECTED_LEGS=15`; `witness()` rows counted → 13 =
  `DETECTOR_WITNESS=13/13`.
- Code: `ws_quote_cell` is shared by `q_shape_violation`, the WSQUOTE leg and `witness()`; `LEG_FAIL ARITY
  expected=15 measured=<n>` fires on a leg-count change; `LEG_FAIL LEGSET` on a vocabulary drift.
- Committed `after/c2-counter.txt` (rc 0): `CURATION_R93=PASS`, `LEGS_MEASURED=15/15 Q_SHAPE_FAIL=0
  Q_WSQUOT=0 Q_ROWS=20 WARRANT_OK=17/17 TFREQ_OK=17/17 DUP_QIDS=0`, `VERDICT fields_hold=1 legs_ok=15/15
  DETECTOR_WITNESS=13/13`.
- Committed `after/c2-controls.txt` (rc 0): `CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2
  WS_SHAPE_GREEN_R92=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7`; both whitespace trees give `Q_WSQUOT=1` /
  `LEG_FAIL WSQUOTE` while r92 reports `Q_SHAPE_FAIL=0` on the same bytes.
- `after/c2-m7-stub.txt`: the stubbed population prints neither `Q_WSQUOT=1` nor `LEG_FAIL WSQUOTE`, and the
  controls bind both needles (`WS_NAMED`).
- Before `evidence-before/c2-prior-accepts.txt`: r92 on the whitespace tree `Q_SHAPE_FAIL=0`, refusing only
  at FLOOR/WARRANT/TFREQ (+VERDICT).

Verdict: **verified** (classification claim, as narrowed by Amendment 4).

### C3 `C3-TALLY-R93` — freshness

- `grep -cE 'PASS \([0-9]+ cases' SKILL.md` → 21 occurrences at lines 86–93 (8 inside `## Gates`), 640
  (`215`), 781 (`283`); `awk 'NR>=82 && NR<576'` → 8 in-scope rows ⇒ `TALLY_ROWS=8`; none before `## Gates`
  ⇒ `HEAD_DECLARED={}`; the two tail tallies are exactly the declared `{215:1, 283:1}`.
- Grounding receipts: `grep -n 'PASS (161 cases, 0 skipped)' corpus/evidence/round25-final-measure.log` →
  line 53; `grep -n 'PASS (256 cases, 0 skipped)' corpus/evidence/round34/audit-dispositions.md` → line 5;
  both tallies are present in the Gates scope (SKILL.md 186/188).
- `grep -c '^ok-case ' controls/selftest-r93.txt` → 283; verdict `RESEARCH_GATE_SELFTEST: PASS (283 cases,
  0 skipped)`; cases 273–275 and 282–283 present.
- Committed `after/c3-counter.txt` (rc 0): `SKILL_TALLY_R93=PASS TALLY_ROWS=8 STALE_TALLIES=0/8
  CASE_RANGE_OK=2/2 HIST_DERIVED=2/2 HIST_PRESENT=2/2 TAIL_OK=1 LEGS=4/4`.
- Committed `after/c3-controls.txt` (rc 0): `CONTROLS=PASS … TAIL_REFUSED=2/2 HEAD_REFUSED=1/1
  INTERIOR_REFUSED=1/1 HIST_UNGROUNDED_REFUSED=1/1`; r92 accepts the tail-changed/added, head, interior and
  ungrounded trees (rc 0), r93 refuses each.
- Code: `HIST_SOURCES` grounds 161/256 in their receipts with located quotes; `hist_present` requires the
  tally in scope; `TAIL_DECLARED`/`HEAD_DECLARED` scan both sides; the case-range leg compares index sets
  over every `ok-case` line.

Verdict: **verified**.

### No axis harmed

- `git diff 206226dc af917ae6 --stat -- SCORECARD.md` → only the appended round-93 block + planned r94; no
  prior score edited.
- `git diff --quiet 206226dc af917ae6 -- tools/ SKILL.md PROVINCE.md` → empty; `corpus/SOURCES.md` diff
  empty; `corpus/knowledge/` 97 → 97.
- The only stale number is inside the new round-93 block (D2), not a regression of a prior axis.

## Per-axis verdicts

- operability: **improved** (C1 verified; 23-row pin population byte-derived)
- calibration: **improved** (C2 verified)
- freshness: **improved** (C3 verified)
- depth: **unchanged**
- coverage: **unchanged**
- adjacency: **unchanged**

## Discernment spot-check (step 3)

No new `corpus/SOURCES.md` row was written this round (`git diff 206226dc af917ae6 -- corpus/SOURCES.md`
empty, 219 rows), so the "newly written row" quote check samples the two re-opened rows; the round's gate
decisions include the wave's rejection of three frozen claim sentences, sampled below as reject-class items.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S070 re-open — installed `sha256sum(1)`, row kept `mined` | admit | `/usr/share/man/man1/sha256sum.1.gz`; `sha256sum` → `93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f` (identical to the row); `zcat … | sed -n '11p'` → `Print or check SHA256 (256\-bit) checksums.` | agree | digest identical to the row and the lesson; quote at the stated line 11, 7 words; the literal roff form is what was quoted, so S073's anchor correction is respected. |
| S001 re-open — rev-form `GATE-RECORD` | admit | `tools/research-gate.sh:9010` → `printf 'RESEARCH_GATE_SELFTEST: PASS (%d cases%s)\n' "$cases" "${SKIPPED:+, $SKIPPED skipped}"`; `git diff --quiet 206226dc af917ae6 -- tools/` exit 0 | agree | the line prints the exact verdict regex the tally counter reads; the tool is byte-identical at base/F2/landing, so the record verified at F2 holds at F6/C7. |
| C1 frozen battery sentence (wave rejected it as stated at F2/C2) | reject | `R93ExecC1Repro`/`R93ReviewerC1`/`R93SentinelScope` verdicts + committed `after/c1-forgeries.txt` | agree | the frozen battery could not print its line on the host (3.14 `tarfile.AbsoluteLinkError`; 3.13 archive trees lack `.git`); the landing clone-based battery prints `FORGERY_REFUSED=2/2 … POSITIVE=pass`, so the rejection was correct and the narrowed landing claim holds. |
| C2 named limit (wave falsified it; "FLOOR-only" was false) | reject | `R93ReviewerC2` E6 + committed `after/c2-controls.txt` / `after/c2-m7-stub.txt` | agree | the leg counts pre-resolution (`Q_WSQUOT=1` on an unresolvable-source row) and the controls bind it; Amendment 4 records the correction. |
| C3 scope claim ("tallies before and after are declared"; head was invisible) | reject | `R93ReviewerC3` F2 + committed `after/c3-controls.txt` | agree | `HEAD_DECLARED={}` + `HEAD_REFUSED=1/1` and `INTERIOR_REFUSED=1/1` show the repaired leg refuses trees r92 accepts; Amendment 7/8 records it. |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, `chousa ok`,
five pre-existing `W04` duplicate-url warnings (S051/S053/S073/S074/S075), 219 rows.

## Trend verdicts with evidence

- **expansion: unchanged** — knowledge entries 97 → 97 (`git diff … --stat -- corpus/knowledge/` empty),
  registry 219 → 219, `corpus/SOURCES.md` byte-identical; the round's gain is in the instruments.
- **quality: improved** — three counters re-frozen with red-before witnesses and failable controls (C1:
  7→23 pinned population, 2/2 forgery refusals; C2: 15 legs, `WS_NAMED=2/2`; C3: derived tallies, tail/head/
  interior refusals), all committed and re-derived here; no admitted entry found false or stale.
- **discernment: improved** — the wave fired all three frozen sentences before filing; the lane published 12
  amendments and four re-freezes (`corpus/evidence/round93/amendments.md`), and this outside re-check agrees
  with every C1/C2/C3 narrowing. The process defects D1/D2/D3/D5 are routed, not disagreements left
  unlearned.

## Routed defects for next round

1. **D1** — Pre-file falsification ledger absent (`.ufo/waves/round-93/claim-falsification.tsv`; gate exit 2,
   `PREFILE-FALSIFICATION: SETUP findings=1`) and the report omits the required line. For r94: `--init`, one
   row per claim × each of the 8 attack seats, include the C1 22→23 `falsifies-number` row naming Amendment
   12, iterate to exit 0, paste the line.
2. **D2** — `SCORECARD.md:4163` says "22/22 rows byte-checked" while the landing pin population is 23 (the
   same block's C1 row and Amendment 12 say 23/23). Correct in the r94 block naming the superseded text
   (append-only discipline).
3. **D3** — The report says "eleven amendments" twice; `amendments.md` carries 12 (Amendment 12 is the
   twelfth). Erratum or next-round note naming the superseded text.
4. **D4** — "Landed changes" does not cite the landing commit `9fa45759` or the wave-results commit
   `af917ae6` by hash (it names them as "landing commit" and "this report's lane amendment"). Cite every
   landing commit by hash next round.
5. **D5** — `after/c2-counter.txt`, `after/c2-controls.txt`, `after/c3-counter.txt`, `after/c3-controls.txt`
   carry no `computed_against` revision line (the C1 receipts do). Print the measured revision in every
   scored receipt.
6. **D6** — The round-92 routed freshness residual "r82 clip range unbound" is neither bound nor explicitly
   dropped in the round report, and the r94 planned block omits it (the 215-tail half is closed by C3).
   Re-flag it or withdraw it with a reason.

## Operator notes

All four SHONEN boxes carry resolvable evidence (Gates table, `LOG.md` round-93, selftest receipts,
`PROVINCE.md` untouched); boxes 1/3/4 are non-author-checkable from the repo. Box 2's end-to-end task is the
three-counter re-measurement chain (meta-work), which the operator should weigh as domain work before any
promotion. Promotion and any `[x]` are operator-owned; none was written here. No file outside the lane repo
and the report path was written by this round; the fleet tree's other dirty entries are other lanes'/run
state.
