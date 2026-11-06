# Round-81 drafts — append-only closures for the six routed defects, plus QUALITY criterion 161

Seat `R81ScribeR80Defects`. Status: **draft, not landed**. Nothing in this file has been written into
`SCORECARD.md`, `corpus/lessons/round-80.md`, `corpus/QUALITY.md` or any other filed artifact.

- Candidate bytes attacked: `7e2da96a0541946e796384d42fea18e09ede9e9f` (all quotes below are `git show` of
  that revision, so line numbers are candidate-revision line numbers).
- Defect source: `corpus/lessons/round-80-verifier-spotcheck.md` §6 (six routed defects).
- Method: committed bytes only (`git show`/`grep -nF`/`ls-tree`/`wc -w`); one gate run per control below.
  Receipts: `.ufo/waves/round-81/w1/R81ScribeR80Defects/receipts/` (listed per item).
- Rule applied throughout: **filed bytes are never rewritten**; each block is appended at the end of its
  file and names the frozen authority plus the corrected value.

---

## A. Append-ready block — `SCORECARD.md`

Append at EOF (candidate file is 3686 lines; it ends with the `### Correction — 2026-11-05` block).
Covers routed defect 1 (SCORECARD's C2 label) and confirms the row's verdict, which is the value
defect 2 restores in the lesson's outcome table.

```markdown
### Correction 2 — 2026-11-06, round-81 closure: routed defects 1 and 2 (append-only; filed bytes unchanged)

The frozen claims file is authoritative for the C2 sourcing label. `corpus/evidence/round80/claims.md`
(frozen at `0d253c95732c0ed19a9fa414e5d17769ddefa48d`; byte-identical to the preserved attempt-1 copy
`0f59b985933b2fe9b0b6a754d908ac6ae47399e6`, `git diff --stat` empty; both blobs
`06086ba2a62375c917b903db84c14d6f48422011f54079bbae8bf553da3ea29a`) reads at line 59
`## C2 — calibration (sourced on S200)` and at lines 88–90 `C2's landing cites **S200**`. The C2 row
above opens `| C2 calibration (sourced on S199) |` (line 3655); the `S199` label is corrected here to
**S200**, and `S199` is C1's evidence row (`claims.md:88`: `C1's evidence cites **S199**`). Both rows
are new this round, so the sourced-claim duty was met either way; the label is what is corrected. The
filed cell text is not rewritten. The same label at `corpus/lessons/round-80.md:73` and `LOG.md:2335`
is superseded by this note and by the round-81 correction block appended to `corpus/lessons/round-80.md`
(defect 1).

The C2 verdict cell in the row above — `**falsified by its own kill rule — honest stop**` — is the
operative value and is confirmed, not corrected: `corpus/lessons/round-80.md` `## Kill-rule outcomes`
states "**C2 as written does not verify**" and cites the committed receipt
`.ufo/waves/round-80/w1/R80CriticA/receipts/c2-unopened-superseded-record.txt`; the outcome table's
`**improved**` cell at `corpus/lessons/round-80.md:73` is corrected to this value by defect 2 of the
round-81 block appended to that file.
```

Quoted current text (receipt `receipts/06-quoted-defects-at-candidate.txt`):

- `git show 7e2da96a…:SCORECARD.md | grep -nF 'C2 calibration (sourced on S199)'` →
  `3655:| C2 calibration (sourced on S199) | …`
- `git show 7e2da96a…:corpus/evidence/round80/claims.md | grep -nF -e 'sourced on S200' -e '15-word'` →
  `59:## C2 — calibration (sourced on S200)` and
  `90:… the corrected 15-word located quote that supersedes S196). Both rows carry a`
- `git show 7e2da96a…:LOG.md | grep -nF 'C2 calibration (sourced on S199)'` →
  `2335:- C2 calibration (sourced on S199): round 79's Gate records were prose nothing re-opened — S196`

---

## B. Append-ready block — `corpus/lessons/round-80.md`

Append at EOF (candidate file is 200 lines; it ends with the `## Kill-rule outcomes` bullets).
Covers routed defects 1, 2, 3, 4, 5 and 6.

```markdown
## Corrections — round 81 (append-only; filed bytes unchanged)

Routed defects 1–6 of `corpus/lessons/round-80-verifier-spotcheck.md` §6 are closed by this block.
No filed byte above is rewritten; each correction names the frozen authority and the corrected value.

1. **C2 sourcing label (defect 1).** The outcome table at line 73 opens
   `| C2 calibration (sourced on S199) |`. Frozen authority: `corpus/evidence/round80/claims.md:59`
   (`## C2 — calibration (sourced on S200)`, frozen at `0d253c95732c0ed19a9fa414e5d17769ddefa48d`)
   and `:88–90` (`C2's landing cites **S200**`). Corrected value: **S200**; `S199` is C1's evidence
   row (`claims.md:88`: `C1's evidence cites **S199**`). The same label at `SCORECARD.md:3655` is
   corrected by the round-81 SCORECARD block, and at `LOG.md:2335` by this note. Both rows are new
   this round, so the sourced-claim duty was met either way.
2. **C2 outcome cell (defect 2).** The same row's verdict cell reads
   `**improved**, with three instrument limits recorded (below)`. Frozen authority: the frozen
   claims.md kill rule's third clause and this lesson's own `## Kill-rule outcomes` ("**C2 as written
   does not verify**", citing
   `.ufo/waves/round-80/w1/R80CriticA/receipts/c2-unopened-superseded-record.txt`), corroborated by
   `SCORECARD.md:3655` (`**falsified by its own kill rule — honest stop**`). Corrected value:
   **falsified by its own kill rule — honest stop**, with the three instrument limits recorded below.
   The cell's bytes stay as filed; the operative value is the honest stop.
3. **Frozen claims.md "15-word" (defect 3).** `corpus/evidence/round80/claims.md:90` reads `the
   corrected 15-word located quote that supersedes S196`. Measured value: **20 words** — this file's
   line 20 carries `GATE-RECORD S200 rev=b7803829922770b890e9f4efdd30d12c3695439a
   path=corpus/QUALITY.md line=1056 words=20 …`; `wc -w` of that record's quote text prints `20`
   (round-81 receipt `receipts/06-quoted-defects-at-candidate.txt`); the counter prints
   `ROW S200 record=ok quote_words=20 location=corpus/QUALITY.md:1056@b78038299227 words=20
   verdict=OK` (`.ufo/waves/round-80/w1/R80CriticA/receipts/c2-after-repro.txt:6`). The frozen file
   is not amended (freeze is freeze); `## Instrument limits` item 5 above already records the class.
   Corrected value: **20**, quoted from `corpus/QUALITY.md:1056@b7803829`.
4. **Draw labels vs receipt names (defect 4).** The round-80 report
   (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-80/chousa.md`, fleet commit
   `023ae03e47e3b815acd2733fdffc51ce8e318740`, lines 117–118) reads `run1 PASS 2/2+2/2, run2 FAIL
   1/2+1/2`. Frozen authority: the committed receipts —
   `.ufo/waves/round-80/w1/R80ExecA/r80a-after-v7-run1.txt:216` =
   `BATTERY=FAIL forgers_rejected=11/11 positive=2/2 fresh_positive=1/2 fresh_forgers=1/2
   oracles_rejected=5/5`, and `.ufo/waves/round-80/w1/R80ExecA/r80d-v7-run2.txt:216` =
   `BATTERY=PASS forgers_rejected=11/11 positive=2/2 fresh_positive=2/2 fresh_forgers=2/2
   oracles_rejected=5/5`. Corrected value: the ordinal labels are inverted relative to the receipt
   names; cite a draw by receipt path, never by ordinal. The falsification is unaffected — both draws
   are committed, and `r80d-v7-run3-fresh3.txt:240` is `BATTERY=FAIL … fresh_positive=0/3
   fresh_forgers=0/3`.
5. **Stray wave-2 directory — dead evidence (defect 5).** `.ufo/waves/round-80/w2/Exec/SubjC2
   RECEIPT/` holds six committed files (`git ls-tree -r` at the round-80 tip and at `7e2da96a`),
   added in `596c2f2a` (an ancestor of the candidate); no `w2-dispatch.json` and no `w2.ready` exists at any revision
   (`git log --all --diff-filter=A` over both paths is empty), so no seat was dispatched, no
   validate ran, and no wave-2 output is counted toward round 80. The round's own
   `w1-results.json` records the directory as "draft artifacts of conflated scope … superseded by
   the w1/R80ExecC.md report of record", and the round-80 report disclosed it at lines 75–78.
   Disposition: the six files are **dead evidence** — retained for provenance only, never cited as a
   round-80 wave-2 result, never counted in any seat tally, and superseded by
   `.ufo/waves/round-80/w1/R80ExecC.md`. A future reader who needs the subject-honest C2 reading or
   the 5-run v7 stability note reads them as an inherited attempt's draft, not as dispatched output.
6. **Mistakes-table formatting (defect 6).** Line 154 is blank and line 155 begins
   `| seven earlier rounds' verdict rows were relabelled in place …` without a repeated header, so in
   GitHub-flavoured Markdown that row renders outside the table. Corrected reading: line 155 is the
   fifth `## Mistakes` row (the relabel mistake already corrected in `SCORECARD.md` §Correction). No
   filed byte is rewritten; any restatement of this row repeats the header line.
```

Quoted current text (receipt `receipts/06-quoted-defects-at-candidate.txt` unless noted):

- `git show 7e2da96a…:corpus/lessons/round-80.md | grep -nF -e 'C2 calibration (sourced on S199)' -e '**improved**, with three instrument limits recorded'` →
  `73:| C2 calibration (sourced on S199) | … | **improved**, with three instrument limits recorded (below) |`
- `git show 7e2da96a…:corpus/lessons/round-80.md | grep -nF 'GATE-RECORD S200'` →
  `20:GATE-RECORD S200 rev=b7803829922770b890e9f4efdd30d12c3695439a path=corpus/QUALITY.md line=1056 words=20 quote=…`
- `git show 7e2da96a…:corpus/lessons/round-80.md | grep 'GATE-RECORD S200' | sed 's/.*quote=//' | wc -w` → `20`
- `git show 7e2da96a…:.ufo/waves/round-80/w1/R80ExecA/r80a-after-v7-run1.txt | sed -n '216p'` →
  `BATTERY=FAIL … fresh_positive=1/2 fresh_forgers=1/2 …` (receipt `receipts/07-draw-label-vs-receipt.txt`)
- `git show 7e2da96a…:.ufo/waves/round-80/w1/R80ExecA/r80d-v7-run2.txt | sed -n '216p'` →
  `BATTERY=PASS … fresh_positive=2/2 fresh_forgers=2/2 …` (same receipt)
- `grep -nF 'run1' …/chousa.md` → `117:- verdict: … run1` / `118:  PASS 2/2+2/2, run2 FAIL 1/2+1/2, …`
  (receipt `receipts/09-report-prose-and-provenance.txt`; the file is clean in the fleet repo,
  `git status --porcelain` empty, last commit `023ae03e`)
- `git ls-tree -r --name-only 7e2da96a… -- '.ufo/waves/round-80/w2'` → six files; dispatch/ready
  probe → `NONE`; `git log --all --diff-filter=A` over `w2-dispatch.json`/`w2.ready` → empty
  (receipt `receipts/08-w2-stray-provenance.txt`)
- `git show 7e2da96a…:corpus/lessons/round-80.md | sed -n '154,156p'` → blank line 154, then
  `| seven earlier rounds' verdict rows were relabelled in place …` at line 155 with no header
  (receipt `receipts/06-quoted-defects-at-candidate.txt`)

---

## C. Append-ready block — `corpus/QUALITY.md` (criterion 161)

Last existing criterion at the candidate is `160.` (`corpus/QUALITY.md:1079`; file is 1079 lines, last
heading `## Round-80 landing …`). Append:

```markdown
## Round-81 addition (criteria 1–160 unchanged)

161. **A checklist Run line's control set includes a record carrying the defect form the item text itself names, and the single-mode command the item supersedes is shown to pass that record.** Round 81's item 2 ("A negative claim carries its search sweep, naming where it looked") shipped a fixture pair whose fail leg is a sweep that names nowhere (`corpus/evidence/round81/checklist-fixtures/item2-fail.md` → `FINDING SWEEP_LOCATION_ABSENT`), while the defect the item text names first — a negative claim with no sweep at all — was carried by no fixture: on `corpus/evidence/round81/negA-probe.md` `bash tools/research-gate.sh verify-sweeps corpus/evidence/round81/negA-probe.md --root .` prints `VERIFIED_SWEEPS=0/0 … RESEARCH_GATE: CLEAN` exit 0 (`.ufo/waves/round-81/w1/R81ScribeR80Defects/receipts/01-negA-verify-sweeps-alone.txt`), and only the structure mode prints `FINDING NEGATIVE_WITHOUT_SWEEP` exit 1 (`receipts/02-negA-structure.txt`), so the item's Run line is the structure conjunct plus the sweeps mode (`receipts/03-item2-runline-negA.txt`, exit 1; pass fixture `receipts/04-item2-runline-pass-fixture.txt`, exit 0). Check: for each Run line, one control record reproduces the item's own defect in the item's own words and the Run command exits non-zero on it while the single-mode command the item supersedes exits 0 on the same bytes, and the pass control exits 0. (Shown able to fail: `receipts/01` CLEAN exit 0 vs `receipts/03` exit 1 on the same record; `python3 -B corpus/evidence/round81/checklist-run.py --root .` prints `CHECKLIST_RUN=6/6 DISCRIMINATE=3/3` exit 0 without covering that form — its item-2 fail leg is `SWEEP_LOCATION_ABSENT`, `receipts/05-item2-runline-fail-fixture.txt`.)
```

Receipts for the criterion's claims:

- `receipts/01-negA-verify-sweeps-alone.txt` — `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1`,
  `RESEARCH_GATE: CLEAN …`, `RC=0` on a record whose `N1` claim row's `sweep` cell is empty.
- `receipts/02-negA-structure.txt` — `FINDING NEGATIVE_WITHOUT_SWEEP severity=warn surface=negatives
  obs=claim=N1 negative without sweep`, `RESEARCH_GATE: DRIFT …`, `RC=1`.
- `receipts/03-item2-runline-negA.txt` — the item-2 Run line verbatim on `negA-probe.md`, `RC=1`.
- `receipts/04-item2-runline-pass-fixture.txt` — same Run line on `item2-pass.md`,
  `VERIFIED_SWEEPS=1/1`, `RESEARCH_GATE: CLEAN`, `RC=0`.
- `receipts/05-item2-runline-fail-fixture.txt` — same Run line on `item2-fail.md`,
  `FINDING SWEEP_LOCATION_ABSENT`, `RC=1` (the neighbouring form, not the item's own).
- `receipts/10-checklist-run-context.txt` — `CHECKLIST_RUN=6/6 DISCRIMINATE=3/3`, `CHECKLIST=PASS`,
  `RC=0` (context only; the counter's control set is the one the criterion tightens).
- `receipts/11-item2-defect-form-variants.txt` and `receipts/12-variant-underlying-modes.txt` —
  robustness of the landed Run line: a capitalised `Negative` kind cell and a claim row with the
  `sweep` column dropped both still exit 1, and in both cases `verify-sweeps` alone still exits 0
  (`VERIFIED_SWEEPS=0/0`, `CLEAN`). These are additional controls, not substitutes for the item's
  own wording.

---

## D. Notes for the integrator

- Both blocks are pure appends; no existing line is edited, moved or deleted. `git diff --numstat`
  after landing should show only insertions on the two files.
- Block A's heading is `### Correction 2` because the file already carries `### Correction — 2026-11-05`;
  if the integrator prefers a different ordinal, only the heading changes.
- Block B's numbering follows the spot-check's defect numbers, so a reader can pair each item with
  `corpus/lessons/round-80-verifier-spotcheck.md` §6 one-to-one.
- Criterion 161's check cites this seat's wave receipts. If the wave output is not committed before
  QUALITY lands, the criterion must cite committed equivalents instead (the round-80 precedent:
  QUALITY 152–160 cite `.ufo/waves/round-80/…` receipts).
- The `## Round-81 addition` heading follows the file's existing convention
  (`## Round-80 landing (criteria 1–151 unchanged; …)`); the parenthetical count is the last
  pre-block criterion number (160).
