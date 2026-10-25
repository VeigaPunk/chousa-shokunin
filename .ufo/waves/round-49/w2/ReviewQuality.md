# ReviewQuality — r49 W2 — QUALITY 69 (round-49 note), 71, 72 + a05 intake corrections

Scope: is each criterion's check command real, is it shown able to fail exactly as stated (each such
command run), does the text overclaim; and do `corpus/lessons/round-49.md:28` (intake row 1) and the
P2/pointer rows match `corpus/lessons/round-48-verifier-spotcheck.md` ruling (a). No frozen predicate,
target or counter touched. All runs from the lane checkout, `TMPDIR=/dev/shm/chousa-r49-ReviewQuality`
(deleted after this write); only write: this file. LSP unavailable for this prose/evidence audit — all
evidence is executed commands and file:line reads (grep used as literal fallback; no server offered).

## Commands real — all six scripts tracked at lane tip 87e9335

`git ls-files --error-unmatch` OK for round48/{c1-count,mutation-check,precision-count}.py and
round49/{a05-check,capture-age-check,quote-substance-check}.py. Criterion 71's mined source is real:
`considerthese/2026-10-25.md:55-56` proposes exactly the capture-age line.

## 69 — pass legs replayed

- `python3 corpus/evidence/round48/c1-count.py` → `CORRECT_BULLETS_PASS=12/12 … C1=PASS`, rc=0.
- `python3 corpus/evidence/round48/mutation-check.py` → `MUTANTS_KILLED=5/5`, rc=0.
- `python3 corpus/evidence/round48/precision-count.py` → `CORRECT_BULLETS_PASS=12/12`, rc=0 (note (a) exact).

## 69 — shown-able-to-fail legs run

- R47-tool control (`git show d4e6ef09…:tools/inference-ground.py` to scratch; `c1-count.py --tool …`) →
  `p03=REFUSED rc=1 p04=REFUSED rc=1 a05=REFUSED rc=1 CORRECT_BULLETS_PASS=9/12 PRECISION_GATE=FAIL
  C1=FAIL`, rc=1 — same labels as `corpus/evidence/round48/controls/before.txt`. Note a05 IS refused
  here (3-before window fires) and per ruling (a) that refusal is correct, so false refusals = p03,p04.
- Accept-all component: `precision-count.py --tool <exit-0 stub>` → `CORRECT_BULLETS_PASS=12/12
  PRECISION_GATE=PASS`, rc=0 — component alone accepts it, exactly as the criterion states.
- Name-key control: `python3 corpus/evidence/round48/controls/name-key-control.py` →
  `NAME_KEYED_C1_COMPONENT=PASS … C1=PASS … NAME_KEYED_MUTATION_CHECK=REJECTED
  implicit-neg=MUTATION_NOT_APPLIED COMPOSITE_CONTROL=REJECTED`, rc=0 — composite rejects, as stated.
- Round-49 note (a), fixtures rebuilt per W1 `DraftP2Limit.md:13-24`: a05 entry (`that date is not the
  copy's build date`, S902 fixture span) under `python3 tools/inference-ground.py --entry … --spans
  corpus/fixtures/inference-ground-r47/spans.tsv --counts …/counts.json --registry corpus/SOURCES.md
  --root . --quiet` → rc=0; independent three-before denial (`the archive stores each ballot` /
  `the stored figure is not the recorded ballot`) → rc=0; two-before control (`…not the ballot`) →
  `FINDING INF_POLARITY_FLIP`, rc=1. Matches `DraftP2Limit.md:20,22,24` and QUALITY 69 note exactly.
- Note (b): "2/12 (p03, p04)" is ruling (a)'s own figure and matches the refusal set above. ✓
- Note (c): `round-48.md:11` `## Mistakes` has exactly two unnumbered rows; `:18` `## Spot-check intake`
  has rows 1–3; no "Mistake 4" anywhere in that file. Pointer correction accurate. ✓

## 71 — fail leg exact, pass leg real

- `python3 corpus/evidence/round49/capture-age-check.py /home/vgpnk/Projects/shokunin/.ufo/reports/round-48/chousa.md`
  → `FRESHNESS_CAPTURE_AGE=FAIL`, rc=1 — exactly as stated.
- PASS leg is mechanically real (scratch line naming freshness+capture+2026-10-25 → PASS, rc=0). The
  round-49 chousa report does not exist yet (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-49/`
  holds only kake/kotoba/kotodama/kumitate.md), so on the real report only the FAIL direction is shown.

## 72 — both legs exact

- `python3 corpus/evidence/round49/quote-substance-check.py` (default spans.tsv) →
  `IDS=8 QUOTES=28 FAILURES=0`, rc=0 — exact.
- CritForgeC2 shape (single-space quote, 5000-char span, checker's 7-column manifest) →
  `HOLLOW_QUOTE S900 ' ' / OVERWIDE_SPAN S900 spans/S900-1.txt len=5000 / NO_SUBSTANTIVE_QUOTE S900
  longest=0 / IDS=1 QUOTES=1 FAILURES=3`, rc=1 — all three markers, exactly as stated.

## Findings by severity

MEDIUM-1 — `round-49.md:28` names a round-49 SCORECARD section that does not exist: "the round-49
SCORECARD section states the ruling". SCORECARD.md's last section header is `2539:## Round 48 verdict`;
`grep "Round 49|round-49|round 49" SCORECARD.md` → no hits; file unmodified in the working tree. The
ruling lives today only in the lane lesson + QUALITY 69 note. Same pointer-to-nonexistent-row class the
round itself mined (`round-49.md` Mistakes row 4 / QUALITY 69(c)). The row's other half is true:
`SCORECARD.md:2545` does carry the dispute verbatim ("W2 `AttackPrecision.md` disputes the a05 label …
re-open a05 in closure"). `a05-check.py` scans lessons only, so this pointer is unenforced either way.

MEDIUM-2 — `a05-check.py` cannot enforce one of the intake's own corrections: `round-47-verifier-spotcheck.md:35`
carries "2–3/12" with no "a05" on the line, and the propagation regex (`a05-check.py:25`,
`3/12[^\n]*a05|a05[^\n]*3/12`) cannot match it. Its correction (intake row 1, `:35` clause) is
prose-only; no command fails if that line regresses. Observed: `A05_PROPAGATIONS=2 CORRECTED=2`,
naming only `round-47-verifier-spotcheck.md:29` and `round-48.md:34` (both verified to carry
"exit-level 3/12 incl. a05").

MEDIUM-3 — QUALITY 72 overclaims its floor (each demonstrated, real exit-0 run):
- Boilerplate is "substance": a manifest whose one quote is `Introduction` (12 non-space chars) with a
  nonexistent span file → `IDS=1 QUOTES=1 FAILURES=0`, rc=0. Two gaps in one run: the floor is pure
  non-space counting (a 3-non-space-char quote also passes for any id holding one ≥12 quote,
  `quote-substance-check.py:17,43`), and a missing span file is read as "" for the width leg
  (`:45-47`) — a manifest citing `spans/GONE-1.txt` passes silently.
- The headline's second clause "a capability counter has a perturbed-input leg" has no check command
  and is unmet by this round's own adopted C1 counter (round-49 lesson Mistakes row 3 records the
  replay pass as a named limit, deferred) — the criterion states as a norm what this round's C1 does
  not do; only the span-manifest half is mechanically checkable. The script docstring is honest
  ("a substance FLOOR, not an entailment check"); the criterion headline is the overclaim. Minor:
  "wider than its quote plus context" is `len(quote)+2*80+2` (`:18,46`), constant unstated in QUALITY.

LOW-4 — QUALITY 71 overclaims semantics its command cannot check: the check is one-line token
co-occurrence (`capture-age-check.py:24-26`, case-insensitive "freshness" ∧ "capture" ∧
`\b\d{4}-\d{2}-\d{2}\b`). Demonstrated: the line `freshness capture 2026-99-99` → PASS, rc=0 —
"an ISO date" accepts a non-calendar date; and nothing verifies the date is "the age of the newest
capture the lane may read". The criterion's Check sentence states the mechanics accurately; the
headline sentence claims more than the command enforces.

INFO-5 — the a05 corrections otherwise match ruling (a) faithfully: true figure 2/12 (p03, p04), a05's
refusal correct, append-only correction placed in the lane-owned round-49 lesson (routed defect 1
allows "round-47-verifier-spotcheck.md or the round-49 lesson"); `round-48.md:34` left verbatim per the
closure's own "append-only, per Evidence standard" with the correction named and mechanically covered;
intake row 2 (P2 false-negative class, "No tool change this round") reproduced leg-by-leg above.

## Residual risk / verification gaps

- Round-close artefacts absent at audit time: the round-49 chousa report (71's PASS subject) and the
  round-49 SCORECARD section (MEDIUM-1). Re-check both once they land; if the section is added at
  close, MEDIUM-1 downgrades to a stale committed pointer.
- LOG.md carries an uncommitted +11-line round-49 entry (pending lane work; noted, not attacked).
- 72 audited only against the shapes QUALITY names plus the two gaps above; c2-count's structural legs
  and entry/lesson membership are outside this ticket.
- Scratch `/dev/shm/chousa-r49-ReviewQuality` deleted after this write.

VERDICT: QUALITY 69 (round-49 note) / 71 / 72 and the a05 intake corrections — partly — every check command is real and every stated fail/pass leg reproduces exactly (including the 2/12 (p03, p04) a05 ruling and the P2 denial legs), but 72's floor accepts boilerplate quotes and missing span files and its perturbed-input clause is unchecked and unmet by this round's own C1, 71 accepts non-ISO dates and cannot verify the newest-capture claim, and intake row 1 names a round-49 SCORECARD section that does not exist.
