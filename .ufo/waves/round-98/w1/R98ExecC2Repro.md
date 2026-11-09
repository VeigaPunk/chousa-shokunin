# R98ExecC2Repro — C2 reproduction from F (aac826848dda5029ba459568b29d9a92176dc2b6)

Seat assignment (falsify, not adjudicate this fuel: C2 here is the reusable
knowledge-lane loop of the noisy book — see the executable component-1 lesson
R98ExecC2 from the round-95 loop; the frozen claim under test is C2-ENTRY-R98
only, C1 not touched). Method: shared clone at F, `--work` scratch under
`/fast/scratch/hyaku/chousa-r98/R98ExecC2Repro`, live lane never run against.

## 1. The four counting commands — reproduce exactly

All exit 0; receipts in w1/R98ExecC2Repro-a…d (plus tallies in f/g):

- `python3 -B tools/gate-records.py verify --root . corpus/knowledge/press-2015-statement-questions-r98.md`
  → last line `GATE_RECORDS files=1 records=38 ok=38 fail=0`, rc=0
  (38 GATE_RECORD lines: 15 S231 + 22 S225 + 1 S228 reject; entry's `## Gate
  records` carries the same 38).
- `bash tools/research-gate.sh verify-metadata ...` → `METADATA_COMPLETE=1/1`,
  `RESEARCH_GATE: CLEAN`, rc=0.
- `python3 -B tools/search-rerun.py verify ...` → `SEARCH_RERUN_SUMMARY
  searches=5 rev_match=5/5 tree_same=1/5 findings=0`, `SEARCH_RERUN: CLEAN`,
  rc=0 (tree_same=1/5 is expected: Q1–Q3 find S231's capture on the current
  tree but not at base; not a finding without --strict).
- `python3 -B corpus/evidence/round98/entry-controls-r98.py --root .`
  → `POSITIVE=1/1 DO_NOTHING_REFUSED=1/1 NEW_ONLY=1/1 FORGERY_REFUSED=7/7
  QUESTION_LINES_HELD=36/36 BASE_HELD=16/36 ELEMENTS=7+6/7+6 WARRANTS_OK=10/10
  LANE_FILLED=10/10` + `ENTRY_CONTROLS_R98=PASS`, rc=0.

## 2. Independent re-derivation of `## Searches` (Q1–Q5)

`git archive 98b8177c… corpus/captures | tar -x -C $S/base`, then
`/usr/bin/grep -l -F` per row, `LC_ALL=C sort`. Receipt:
w1/R98ExecC2Repro-g-searches.txt.

| row | recorded hits | my hits | match |
|---|---|---|---|
| Q1 `Guideline Assessment Form` | 0 | 0 | yes |
| Q2 `Recommendations for Librarian Practice` | 0 | 0 | yes |
| Q3 `skilled translation` | 0 | 0 | yes |
| Q4 `consensus development forum` | 1 (e94691f5…) | 1 (same file) | yes |
| Q5 `Are the search concepts clear` | 2 (347c55ba…, 80a844fe…) | 2 (same files) | yes |

`rev_match=5/5` reproduced independently; note S231's capture correctly
absent at base (git-archive tree has no 4ec85a1e…).

## 3. Independent held-count re-derivation (no lane script)

≤30-line checker stdlib only (reproduced at
w1/R98ExecC2Repro-e-check_c2.py / -e-check.txt). S225 capture lines strictly
between `PRESS 2015 Guideline Evidence-Based Checklist` (capture line 32) and
`Derived from:` (line 82) containing `?`: 36 lines (1-based capture lines
34–80 as listed in receipt). A line is held iff its whitespace-collapsed
text equals one S225 quote or consecutive S225 quotes of one entry joined
by one space.

- held-by-both (R97 at F + R98): **36/36** (lines [34…80] all held).
- held-at-BASE (R97 at 98b8177c only): **16/36** (lines
  [34,36,38,39,42,44,50,58,61,63,69,72,73,74,77,80]).
- held-after: 36/36 (same as held-by-both).

Both differ from claimed 36/36 and 16/36 by 0 — **no K1 finding**.

## 4. M1–M15 substring check vs `abstractText` — FINDING (K2)

`json.loads(capture 4ec85a1e…).resultList.result[0].abstractText`
(1 835 chars), whitespace-collapsed both sides, gate-norm variant identical
for M1. Receipt: w1/R98ExecC2Repro-f-mcheck.txt (rerun in §5).

- **M1 (`PRESS Peer Review … Guideline Statement.`) is NOT a substring of
  `abstractText`.** It is the record's `title` field (with a NBSP between
  "Guideline" and "Statement."; gate-norm collapses it), present in S225's
  "Derived from" citation, and present in the whole-capture normalized text
  — which is why `gate-records.py` QUOTE_ABSENT and the entry controls'
  `check_quotes` (whole-capture `norm(caps[src])`) pass it.
- **M2–M15 (14 quotes) are all substrings of `abstractText`, none contains
  `<h4>`.** M1 has no markup either.

Entry line 30 states verbatim: "Every S231 quote below is a substring of that
string [the abstractText] with no markup inside it." Claims C2 sentence says
the abstract is held "in 15 located quotes"; kill rule K2 says "an S231
quote is not inside the record's abstractText". M1 triggers K2 under the
claims' own wording. The entry's Section cover line ("Every S231 quote below
is a substring of that string", l.30) and, following it, the claims'
"K2: an S231 quote is not inside the record's abstractText" both fire
strictly at F. The frozen counters do not enforce K2's abstractText scope
(gate-records checks the whole JSON capture; controls check the whole
capture), so PASS coexists with the K2 violation — an instrument gap
worth stating alongside the firing.

Neutral note: M1 as a title-quote is accurate provenance (title field +
S225 Derived-from agree, §6), so the repair is to re-caption M1 as the
title, not to withdraw it.

## 5. Quote provenance notes (K1/K2 support)

- M2 objective, M3 method (SR+survey+forum), M4–M5 systematic-review
  finding (no new elements, no refutation), M6 suggested-use, M7–M8 survey
  timing (MEDLINE → before other databases), M9–M10 six retained (with
  element list), M11–M12 seventh removed (skilled translation, discretion),
  M13–M14 four documents, M15 conclusion — all inside abstractText (§4).
- K1–K22 (22 S225 quotes, R98) plus R97's S225 quotes cover the 36
  question lines whole or as consecutive one-space joins (§3), within the
  25-word cap (longest K17 at 22 words; K18+K19 and K21 splits are capture
  lines 67–68 / 79; entry's allocation paragraph l.31-32 matches:
  K17–K18 = line 67 (30 words), K19 = line 68, K20 = line 78,
  K21–K22 = line 79 — 1-based capture lines; the compressed `sed` window
  in §2 differed by the heading offset, resolved at capture lines).

## 6. K4/K5 checks

- K5 (identity): S231 title/authors/doi/pmid = "PRESS Peer Review of
  Electronic Search Strategies: 2015 Guideline Statement." (NBSP,
  normalized away) / McGowan J, Sampson M, Salzwedel DM, Cogo E, Foerster
  V, Lefebvre C / 10.1016/j.jclinepi.2016.01.021 / 27005575 /
  pageInfo 40-46 vs S225 "Derived from" (McGowan J et al., J Clin
  Epidemiol. 2016 Jul;75:40-6, dx.doi 10.1016/j.jclinepi.2016.01.021).
  Identical identity; page style 40-46 vs 40-6 is abbreviation style, not a
  mismatch. K5 holds.
- K4 (element-names): S231 six in abstract order vs S225 headings 1–6
  (reprint adds parentheticals on 2/3/4, "Text word searching" for "text
  word search", serial comma in 5) — every cell is a substring of its
  capture (controls ELEMENTS 7+6/7+6, my substring re-check of M9/M10 and
  element cells agrees); S223 grouping ("limits and filters, syntax and
  line numbers; and spelling", round-96 L22-L23) correctly reported as
  differing. K4 holds.

## 7. K3 probe (decision rows) — judgement note, not a counted fire

Standing direction ("matters-of-judgement" noted, not counted, mirrors
the frozen named-limit (d) reservation): the "Saying what evidence stands
behind the elements" row's Never cell ("say that the abstract reports
evidence for each question") is a scope-gloss on warrants M3–M6 (which say
nothing about questions), with the Do row speaking only of element-level
review findings. Whether this reads as "the negation of its own Do clause"
(K3-allowed) or as an additional prohibition about per-question evidence
(K3-forbidden) is the reviewer's faithfulness call; I do not count it as a
fire here, and flag only that the frozen counters' WARRANT check (10/10)
verifies qid naming only, not this gloss. The element/timing rows' Never
cells parallel their Do rows and are not flagged.

## 8. Tools

No installs needed (python3, bash, GNU /usr/bin/grep 3.12 already present);
RULES.md read first; pacman guard untouched. Scratch deleted before yield
(per seat spec `trap 'rm -rf …'` equivalent at exit).

VERDICT: R98ExecC2Repro C1 n/a — not assigned; only C2 was reproduced.
VERDICT: R98ExecC2Repro C2 fired — M1 is the title, not a substring of abstractText, so the entry line 30 / claims K2 sentence is false as stated while the frozen counters (whole-capture matching) still pass; all four counting commands, the 5 search rows, and 36/36 vs 16/36 independently reproduce.
