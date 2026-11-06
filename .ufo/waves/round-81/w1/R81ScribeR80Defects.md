# R81ScribeR80Defects — report

Seat: `R81ScribeR80Defects` (leaf scribe, round 81 wave 1). Deliverable: draft (not landed) append-only
closure text for the six routed defects in `corpus/lessons/round-80-verifier-spotcheck.md` §6, plus one
QUALITY criterion draft. Draft file: `.ufo/waves/round-81/w1/R81ScribeR80Defects/drafts.md`.

## Behavior

Read the frozen predicate set first (`corpus/evidence/round81/claims.md`), then the spot-check §6, then
re-measured every defect against **committed candidate bytes** `7e2da96a0541946e796384d42fea18e09ede9e9f`
(`git show <rev>:<path> | grep -nF`), never against the working tree alone. Wrote two append-ready
correction blocks (one for `SCORECARD.md`, one for `corpus/lessons/round-80.md`) that quote the current
text with `grep -n`, name the frozen authority and the corrected value, and rewrite no filed byte; a
one-paragraph dead-evidence disposition for the stray wave-2 directory; and QUALITY criterion 161 with a
Check line and a shown-able-to-fail pointer. No file outside the seat's wave output folder and scratch
was written. No network, no fetch, no subagent dispatch, no git/jj mutation, no commit.

## Gates run (exact command → receipt → observed line, exit code)

All commands run from `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Receipts under
`.ufo/waves/round-81/w1/R81ScribeR80Defects/receipts/`.

| # | command | receipt | observed line / rc |
|---|---|---|---|
| 1 | `bash tools/research-gate.sh verify-sweeps corpus/evidence/round81/negA-probe.md --root .` | `01-negA-verify-sweeps-alone.txt` | `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1`; `RESEARCH_GATE: CLEAN …`; `RC=0` |
| 2 | `bash tools/research-gate.sh verify corpus/evidence/round81/negA-probe.md --root .` | `02-negA-structure.txt` | `FINDING NEGATIVE_WITHOUT_SWEEP severity=warn surface=negatives obs=claim=N1 negative without sweep`; `RESEARCH_GATE: DRIFT …`; `RC=1` |
| 3 | `f=corpus/evidence/round81/negA-probe.md; ! bash tools/research-gate.sh verify "$f" --root . \| grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP' && bash tools/research-gate.sh verify-sweeps "$f" --root .` (the landed item-2 Run line verbatim) | `03-item2-runline-negA.txt` | no stdout; `RC=1` |
| 4 | same Run line, `f=…/checklist-fixtures/item2-pass.md` | `04-item2-runline-pass-fixture.txt` | `VERIFIED_SWEEPS=1/1`; `RESEARCH_GATE: CLEAN`; `RC=0` |
| 5 | same Run line, `f=…/checklist-fixtures/item2-fail.md` | `05-item2-runline-fail-fixture.txt` | `FINDING SWEEP_LOCATION_ABSENT severity=warn surface=sweeps obs=id=W1 no location named`; `RC=1` |
| 6 | `git show 7e2da96a…:<file> \| grep -nF …` for every quoted defect line; `wc -w` of the S200 quote | `06-quoted-defects-at-candidate.txt` | SCORECARD `3655:`; lesson `73:`; claims `59:`/`90:`; LOG `2335:`; `GATE-RECORD S200 … words=20` at lesson `20:`; `wc -w` = `20` |
| 7 | `git show 7e2da96a…:.ufo/waves/round-80/w1/R80ExecA/{r80a-after-v7-run1,r80d-v7-run2,r80d-v7-run3-fresh3}.txt` | `07-draw-label-vs-receipt.txt` | `r80a…run1.txt:216` = `BATTERY=FAIL … fresh_positive=1/2 fresh_forgers=1/2`; `r80d…run2.txt:216` = `BATTERY=PASS … 2/2+2/2`; `r80d…run3-fresh3.txt:240` = `BATTERY=FAIL … 0/3+0/3` |
| 8 | `git ls-tree -r --name-only 7e2da96a… -- '.ufo/waves/round-80/w2'`; same for `w2-dispatch.json`/`w2.ready`; `git log --all --diff-filter=A` over both | `08-w2-stray-provenance.txt` | six files; `NONE` for dispatch/ready; `git log --diff-filter=A` empty |
| 9 | `git -C /home/vgpnk/Projects/shokunin status --porcelain -- .ufo/reports/round-80/chousa.md`; `git log -1 --format=%H -- …`; `grep -nF -e run1 -e run2 …` | `09-report-prose-and-provenance.txt` | clean; `023ae03e47e3b815acd2733fdffc51ce8e318740`; `117:`/`118:` = `run1 PASS 2/2+2/2, run2 FAIL 1/2+1/2` |
| 10 | `python3 -B corpus/evidence/round81/checklist-run.py --root .` | `10-checklist-run-context.txt` | `CHECKLIST_RUN=6/6 DISCRIMINATE=3/3`; `CHECKLIST=PASS`; `RC=0` |
| 11 | item-2 Run line on two defect-form variants in scratch (capitalised `Negative` kind; `sweep` column dropped) | `11-item2-defect-form-variants.txt` | both `RC=1` |
| 12 | `verify` and `verify-sweeps` separately on both variants | `12-variant-underlying-modes.txt` | both: structure `NEGATIVE_WITHOUT_SWEEP` `RC=1`; sweeps `VERIFIED_SWEEPS=0/0` `CLEAN` `RC=0` |
| 13 | `git diff --stat 0f59b985… 0d253c95… -- corpus/evidence/round80/claims.md`; `sha256sum` of both blobs | `13-claims-freeze-bytes.txt` | empty diff, `RC=0`; both blobs `06086ba2a62375c917b903db84c14d6f48422011f54079bbae8bf553da3ea29a` |

## Findings

1. **Defect 1 confirmed (C2 sourcing label).** At the candidate, `SCORECARD.md:3655` opens
   `| C2 calibration (sourced on S199) |`, `corpus/lessons/round-80.md:73` opens the same, and
   `LOG.md:2335` reads `- C2 calibration (sourced on S199): …`. Frozen authority
   `corpus/evidence/round80/claims.md:59` reads `## C2 — calibration (sourced on S200)` and `:88–90`
   reads `C2's landing cites **S200**` (`C1's evidence cites **S199**`). Corrected value: **S200**.
   Receipt `06`. Draft: block A + block B item 1.
2. **Defect 2 confirmed (lesson outcome cell).** `corpus/lessons/round-80.md:73` verdict cell reads
   `**improved**, with three instrument limits recorded (below)`, while the same file's
   `## Kill-rule outcomes` states "**C2 as written does not verify**" and `SCORECARD.md:3655` reads
   `**falsified by its own kill rule — honest stop**`. Corrected value: honest stop. Receipt `06`.
   Draft: block B item 2.
3. **Defect 3 confirmed (frozen "15-word").** `corpus/evidence/round80/claims.md:90` says `the
   corrected 15-word located quote that supersedes S196`; the landed record is
   `GATE-RECORD S200 … words=20` (`corpus/lessons/round-80.md:20`), `wc -w` of the quote = `20`, and
   `R80CriticA/receipts/c2-after-repro.txt:6` prints `quote_words=20`. Corrected value: **20**; the
   frozen file is not amended. Receipt `06`. Draft: block B item 3.
4. **Defect 4 confirmed (draw labels inverted vs receipt names).** Report prose
   (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-80/chousa.md:117–118`, fleet commit `023ae03e`,
   file clean) says `run1 PASS 2/2+2/2, run2 FAIL 1/2+1/2`; the committed receipts carry the opposite:
   `r80a-after-v7-run1.txt:216` = FAIL 1/2+1/2, `r80d-v7-run2.txt:216` = PASS 2/2+2/2. The
   falsification is unaffected (both draws committed; `--fresh 3` FAIL 0/3+0/3 at `:240`). Receipt `07`.
   Draft: block B item 4.
5. **Defect 5 confirmed (stray wave-2 dir is dead evidence).** Six files under
   `.ufo/waves/round-80/w2/Exec/SubjC2 RECEIPT/`, added in `596c2f2a` (ancestor of the candidate); no
   `w2-dispatch.json` and no `w2.ready` at any revision (`git log --all --diff-filter=A` empty); the
   round's own `w1-results.json` calls them "draft artifacts of conflated scope … superseded by the
   w1/R80ExecC.md report of record"; the report disclosed them at lines 75–78. Receipt `08`. Draft:
   block B item 5 (one-paragraph dead-evidence disposition).
6. **Defect 6 confirmed (Mistakes table formatting).** `corpus/lessons/round-80.md:154` is blank and
   `:155` begins the fifth row without a repeated header, so GFM renders it outside the table.
   Corrected reading: line 155 is the fifth `## Mistakes` row. Receipt `06`. Draft: block B item 6.
7. **Mined mistake measured (basis for QUALITY 161).** On `corpus/evidence/round81/negA-probe.md` — a
   record whose `N1` negative claim row's `sweep` cell is empty — `verify-sweeps` alone prints
   `VERIFIED_SWEEPS=0/0 … RESEARCH_GATE: CLEAN` and **exits 0** (receipt `01`), while the structure
   mode prints `FINDING NEGATIVE_WITHOUT_SWEEP` and exits 1 (receipt `02`). The landed item-2 Run line
   (structure conjunct + sweeps mode) exits 1 on that record (receipt `03`) and 0 on the pass fixture
   (receipt `04`), so **C2's kill rule K2 does not fire on this record** — the conjunct is load-bearing.
   The round-81 control set's item-2 fail leg is a different form (`SWEEP_LOCATION_ABSENT`, receipt
   `05`), which is exactly why criterion 161 requires the control set to carry the item text's own
   defect form. Two shape variants (capitalised kind, dropped `sweep` column) also exit 1 with
   `verify-sweeps` alone at 0 (receipts `11`, `12`); those two fixtures were scratch-only and are
   deleted, so receipts `11`–`12` are their only record — the primary probe `negA-probe.md` is
   committed and reproducible.
8. **Observation, not a routed defect (silent failure path).** The item-2 Run line's defect path
   produces no gate output: receipt `03` contains the echoed command and `RC=1` only, because
   `grep -q` consumes the structure finding and the `!` conjunct short-circuits before the sweeps
   mode runs. An operator sees an exit code with no diagnostic. Measured, not repaired; recorded
   here for the integrator.

## Touched surfaces

- Read (lane): `corpus/evidence/round81/claims.md`, `corpus/lessons/round-80-verifier-spotcheck.md`,
  `corpus/lessons/round-80.md`, `SCORECARD.md`, `LOG.md`, `corpus/QUALITY.md`, `SKILL.md`,
  `corpus/evidence/round80/claims.md`, `corpus/evidence/round80/controls/*`,
  `corpus/evidence/round81/negA-probe.md`, `corpus/evidence/round81/checklist-fixtures/*`,
  `.ufo/waves/round-80/**` (read-only), `tools/research-gate.sh` (grep only, not executed as source).
- Read (fleet): `/home/vgpnk/Projects/shokunin/.ufo/reports/round-80/chousa.md` (read-only, clean).
- Written: `.ufo/waves/round-81/w1/R81ScribeR80Defects/drafts.md`,
  `.ufo/waves/round-81/w1/R81ScribeR80Defects/receipts/01…12`, this report; scratch
  `/fast/scratch/hyaku/chousa-r81/R81ScribeR80Defects/` (two variant fixtures, deleted before yield).
- No production edit, no commit, no push, no `corpus/captures/` or `refetch.tsv` write, no `/tmp` write.

## Out of scope / not done

- No claim adjudication: the frozen counters were not re-run as evidence of C1/C2, except the C2
  counter as context (receipt `10`) and the item-2 Run line as the criterion's probe.
- No network fetch (none needed; all defects are revision-pinned committed bytes).
- No repair of the filed bytes; the drafts are append-only text for the integrator to land.
- No subagent dispatch, no lane/fleet git or jj mutation.

## Artifact paths

- `.ufo/waves/round-81/w1/R81ScribeR80Defects/drafts.md` — the deliverable (blocks A, B, C + integrator notes).
- `.ufo/waves/round-81/w1/R81ScribeR80Defects/receipts/01…13` — every command cited above.
- `.ufo/waves/round-81/w1/R81ScribeR80Defects.md` — this report.

VERDICT: R81ScribeR80Defects C1 n/a — no C1 predicate was executed or adjudicated here; this seat only corrected the round-80 draw-label citation (defect 4) against the committed receipt bytes, leaving the recorded C1 kill-rule firing untouched.
VERDICT: R81ScribeR80Defects C2 n/a — no C2 predicate was adjudicated here; this seat measured that `verify-sweeps` alone exits 0 on `negA-probe.md` while the landed item-2 Run line exits 1 (K2 does not fire on that record) and drafted QUALITY 161 from the measurement.
