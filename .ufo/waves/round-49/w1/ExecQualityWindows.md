# ExecQualityWindows — round 49 w1 report

Seat: ExecQualityWindows (executor, leaf). Assignment: verify QUALITY.md criterion 69's second sentence (the "R48 Named limit" window sentence) against `tools/inference-ground.py` by reading `occurrence_polarity()`/`polarity_flips()` and running window probes; check the `round-48.md Mistake 4` citation.

## Tool identity
- Lane HEAD: `6594092 round-49: C1 candidate tools/assimilate-rows.py ...`; `tools/inference-ground.py` is clean in the working tree (`git status --porcelain tools/inference-ground.py` → empty), last touched by round-48 repair commit `671b096`.
- `sha256sum tools/inference-ground.py` → `fa2b4eb5fc29b4dd30f468d9409790ba55fa4b012851e5c9f3efce0074658b6e`.
- No tool installation was needed or performed (in-repo python3 3.14.8 + stdlib; `~/.omp/agent/RULES.md` read; pacman untouched).

## Code reading (working tree)
- `occurrence_polarity()` (lines 283–296): span-side negation = explicit negator in `words(before)[-3:]` of the clause segment `re.split(r"[\n.;:()]", s[:idx])[-1]` → span-side window is **3 words before**, same clause.
- `polarity_flips()` (lines 317–349): P1 (span negates) refuses a same-stem bullet word when no negator in `uw[max(0, j-7):j] + after` where `after = uw[j+1:j+4]` → **7 before / 3 after**. P2 (span affirms) flips when `is_neg` sits in `before[-2:]` where `before = uw[max(0, j-3):j]` → **2 before**.
- Note: the quoted token's own words are stripped by `BACKTICK_RE` in `unquoted()` (line 280), so probe distances were placed on prose words outside the backtick phrase.

## Probes (scratch /tmp/chousa-r49-ExecQualityWindows/probes/<p>/; entry.md = `#### Inference` + one bullet citing S123; spans.tsv = 7-col manifest; --counts /dev/null)
Command per probe: `python3 tools/inference-ground.py --entry <p>/entry.md --spans <p>/spans.tsv --counts /dev/null; echo rc=$?` (run from lane root).

| probe | setup | observed output | rc |
|---|---|---|---|
| p1-7before | span "the report does not include feature alpha"; bullet "- `feature alpha` not one two three four five six features (S123)" ('not' at 7 before 'features') | `GROUND: PASS` | 0 |
| p1-8before | same span; bullet "- `feature alpha` not a one two three four five six features (S123)" ('not' at 8 before) | `FINDING INF_POLARITY_FLIP bullet=1 token='feature alpha / features'` → `GROUND: FAIL` | 1 |
| p1-3after | same span; bullet "- `feature alpha` features one two not (S123)" ('not' at 3 after) | `GROUND: PASS` | 0 |
| p1-4after | same span; bullet "- `feature alpha` features one two three not (S123)" ('not' at 4 after) | `FINDING INF_POLARITY_FLIP bullet=1 token='feature alpha / features'` → `GROUND: FAIL` | 1 |
| p2-2before | span "the report includes feature alpha here"; bullet "- `feature alpha` is not real feature (S123)" ('not' at 2 before) | `FINDING INF_POLARITY_FLIP bullet=1 token='feature alpha / feature'` → `GROUND: FAIL` | 1 |
| p2-3before | same span; bullet "- `feature alpha` is not quite real feature (S123)" ('not' at 3 before) | `GROUND: PASS` | 0 |
| span-3before | span "the report does not dim green feature alpha here" ('not' at 3 before phrase); bullet "- `feature alpha` is a real feature (S123)" | `FINDING INF_POLARITY_FLIP bullet=1 token='feature alpha / feature'` → `GROUND: FAIL` | 1 |
| span-4before | span "the report does not dim green brown feature alpha here" ('not' at 4 before phrase); same bullet | `GROUND: PASS` | 0 |

All probes printed `section=1 bullets=1 tokens=1 grounded=1` (grounding clean; no confound from other findings).

## Verdict on the sentence
The line "The R48 Named limit records the current bullet-side windows (P1: 7-before/3-after; P2: 2-before); the span-side window remains 3-before" is **true as written** against the working-tree tool:
- P1: negator at exactly 7 before is still inside the window (rc 0); at 8 it fires a flip (rc 1). At exactly 3 after inside (rc 0); at 4 it fires (rc 1).
- P2: negator at exactly 2 before fires the flip (rc 1); at 3 it is outside (rc 0).
- Span-side: negator at exactly 3 words before the phrase negates it (rc 1 via P1 flip); at 4 it does not (rc 0).
All windows are inclusive at the stated boundary distances. The sentence's contrast with "Criterion 67's 3/2 values describe the R47 behavior" is consistent with criterion 67's text (QUALITY.md lines 653–658: "three words before, two after; four after a figure") and with the R48 code above.

## `round-48.md Mistake 4` citation check
- `corpus/lessons/round-48.md` (77 lines) `## Mistakes` (line 11) is a **2-row, unnumbered table** (lines 15–16: "Forward `used-by` pointer"; "Control-output transcription"). There is no Mistake 4 and no Mistake 5.
- History: `git log --oneline --follow -- corpus/lessons/round-48.md` → single commit `73ea811` (round-48 land); `git show 73ea811:corpus/lessons/round-48.md | grep -cE 'Mistake|M-[0-9]'` → 1 (the `## Mistakes` heading). No revision ever contained a numbered mistake.
- Whole-lane grep `Mistake\s+[0-9]` (case-insensitive) matches only QUALITY.md lines 703 and 714 (criterion 69's and criterion 70's citations) and lowercase "mistake N" phrasings inside round-45/46/47 lessons — none in round-48.
- So the citation `corpus/lessons/round-48.md` Mistake 4 **does not resolve**; the lesson has no Mistake 4 (criterion 70's "Mistake 5" citation is equally absent). The window sentence itself is unaffected and stands on the code/probes above.

VERDICT: Attacked the QUALITY 69 R48 Named-limit sentence — all eight window probes pass at the stated inclusive boundaries (P1 7-before/3-after, P2 2-before, span-side 3-before), so the line is true as written; the `round-48.md Mistake 4` citation does not exist in that lesson (2-row unnumbered Mistakes table at all revisions).
