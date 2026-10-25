# MutateFigure — repeated-figure mutation probe vs frozen R48 C1 counter

seat: L1Chousa48.MutateFigure · wave: round-48/w2 · date: 2026-10-25 · HEAD `4bbd234`
scope: reconstruct the R47 first-occurrence `figure_flip` mutant in scratch, score the
frozen `corpus/evidence/round48/c1-count.py --cases-only` leg; test whether changing
only the first figure occurrence (not the second) games the counter. No lane edits.

## 1. Subject and mutants (all in /tmp/chousa-r48-MutateFigure/, deleted)

- pristine `tools/inference-ground.py` @HEAD sha256 `9d789b34562cc0ce35be7e4d7ea67a9fa57eabf8794bbf096c8a8d190925149b`
  (`git show HEAD:` identical to disk byte-for-byte).
- Anchor: line 411 `for m in re.finditer(r"(?<![\d,.])" + re.escape(bare) + r"(?![\d,])", text):`
  inside `figure_flip` (`:400-415`): `key_neg != any(is_neg(w) for w in nxt)` ⇒ flip.
- mut-A `[:1]` — the R47 survivor `mut-e` of `.ufo/waves/round-47/w2/MutC1Refined.md:26,56-60`,
  byte-equal to `mutation-check.py:21-23`'s frozen `repeated-figure` transform.
  sha256 `c51c7cd167c71f09116052211980c7859dc836ad4e89bd375a8ac5b2e5376153`.
- mut-B `[1:]` — skips the first occurrence, checks 2nd+. sha256 `9a0b238e6c277938dade9c9c016003f9b8d3b83bd30ff7c2ff1aa0aac946aa28`.
- mut-C — literal "change the first occurrence, keep the second": inserts
  `re.sub(..., "\x00", text, count=1)` before the loop. sha256 `c038bfef9efc585842bba11af2158945f1eed420b44e928be84933bcadeb12b4`.

## 2. Runs (commands + observed output)

`python3 corpus/evidence/round48/c1-count.py --root <lane> --tool <tool> --cases-only`

    pristine  rc=0  implicit-neg=PASS un-neg=PASS un-prefix-flip=PASS repeated-figure=PASS
              nested-count-key=PASS REFINEMENT_CASES=5/5 C1_CASES=PASS
    mut-A     rc=1  repeated-figure=FAIL wanted_rc=1 observed_rc=0 'GROUND: PASS'
              REFINEMENT_CASES=4/5 C1_CASES=FAIL   → KILLED in the named cell ✓
    mut-B     rc=0  all five PASS incl. repeated-figure=PASS 'FINDING INF_POLARITY_FLIP
              bullet=1 token='1,582 / counts key figures/answers_without_archive_key''
              REFINEMENT_CASES=5/5 C1_CASES=PASS   → SURVIVED (cases leg games by skip-first)
    mut-C     rc=0  identical 5/5 PASS → SURVIVED

Frozen probe unmodified: `python3 corpus/evidence/round48/mutation-check.py`
    PRISTINE_CASES=PASS · implicit-neg=KILLED · un-neg=KILLED · un-prefix-flip=KILLED
    · repeated-figure=KILLED · nested-count-key=KILLED · MUTANTS_KILLED=5/5 · rc=0
    → ticket requirement holds: the R47 first-occurrence mutant fails the
      repeated-figure cell exactly, rc=1, named-cell FAIL. Confirmed live.

Full counter (`c1-count.py` no `--cases-only`), to see if any other leg catches B/C:

    pristine: REFINEMENT_CASES=5/5 CORRECT_BULLETS_PASS=9/12 PRECISION_GATE=FAIL
              LEGACY_R47=PASS C1=FAIL (the recorded 9/12 before-state)
    mut-B   : same 9/12, PRECISION_GATE=FAIL, LEGACY_R47=FAIL (JUNK_KILLED=2/3) C1=FAIL
    mut-C   : identical to mut-B
    mut-A   : REFINEMENT_CASES=4/5 LEGACY_R47=PASS C1=FAIL

So mut-B/mut-C are indistinguishable from pristine on the R48 refinement leg AND the
precision leg, but the unchanged R47 counter refuses them.

## 3. Direct defect demos (mirror c1-count.run_case, S902 + same counts/span)

R48 cell shape — `1,582 … no archive key, and 1,582 … are bound` (negated key; occ1 negated, occ2 bare):
    pristine rc=1 FINDING INF_POLARITY_FLIP '1,582 / counts key figures/answers_without_archive_key'
    mut-A rc=0 (misses occ2) · mut-B rc=1 · mut-C rc=1
Reversed shape — `1,582 … are bound, and 1,582 … carry no archive key` (occ1 bare/inconsistent, occ2 consistent):
    pristine rc=1 (same finding) · mut-A rc=1 · mut-B rc=0 (misses occ1) · mut-C rc=0
R47 pinned junk `corpus/fixtures/inference-ground-r47/junk-flip-figure.md`
(`7,572 answers name no source`; key `figures/answers_named_source` affirmative —
 the inconsistent occurrence is the FIRST, the only, occurrence):
    pristine rc=1 FINDING '7,572 / counts key figures/answers_named_source'
    mut-B rc=0 GROUND: PASS ← the surviving legacy leg that catches skip-first

## 4. Verdict

- Required check: PASS — reconstructed R47 mut-e (`[:1]`) fails exactly the
  `repeated-figure` cell (rc=1, `repeated-figure=FAIL`); frozen probe kills 5/5.
- "Changing the first occurrence can't game the counter": **holds at the full
  `c1-count.py` predicate; FAILS at the scoped `--cases-only` refinement leg.**
  The refinement cell is directionally one-sided: it pins only "second occurrence
  unchecked" (negated key + negated first + bare second). A tool that ignores the
  FIRST occurrence (mut-B `[1:]`, or mut-C that edits occurrence 1 in place and
  keeps 2) scores `repeated-figure=PASS` and `REFINEMENT_CASES=5/5` — the cell it
  was built to pin cannot see the complementary defect. The claim survives only
  because the unchanged R47 leg `JUNK_KILLED` carries the other direction
  (junk-flip-figure's inconsistent first/only `7,572`), so full C1 still fails
  mut-B/mut-C. Under `--cases-only` — the exact score `mutation-check.py` uses —
  the skip-first mutant is a SURVIVOR: a residual coverage hole in the frozen
  mutation leg, of the same class MutC1Refined reported for R47.
- No claim edit proposed; a coverage finding is not permission to change the
  contract. A symmetric fixture (consistent second, inconsistent first) would pin
  the missing direction.

## 5. Lane hygiene

`git status --porcelain tools/ corpus/` shows only pre-existing
`corpus/SOURCES.md`, `corpus/evidence/round41/receipts/cells/cells.json` mods
(not mine); `tools/inference-ground.py` sha256 unchanged
(`9d789b34…149b`, == HEAD). Scratch `/tmp/chousa-r48-MutateFigure/` removed.
No installs, no pacman, no network.
