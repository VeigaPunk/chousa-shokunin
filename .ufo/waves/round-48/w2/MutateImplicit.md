# MutateImplicit — round-48 wave-2 mutation probe

agent: L1Chousa48.MutateImplicit · role: mutation-tester · date: 2026-10-25
scope: frozen C1 mutation check, cells `implicit-neg` and `un-neg` only.
Lane files unmodified; all mutation work in `/tmp/chousa-r48-MutateImplicit` (deleted after run).
No external fetch. No installs (python3 present; pacman paused per directive — none needed).

## Inputs (sha256, before → after run)

- `tools/inference-ground.py`: `9d789b34562cc0ce35be7e4d7ea67a9fa57eabf8794bbf096c8a8d190925149b` → identical. `git status` shows only pre-existing sibling modifications elsewhere; my lane never touched the file (harness mutates tempfile copies only).
- `corpus/evidence/round48/mutation-check.py`: `aee54b9f199d1d6df81f83e74c3e4ca9249e1fccd6b458d16f929dd1957df2ca`
- `corpus/evidence/round48/c1-count.py`: `b2a69185213674a8f3bea126e820e2a3ea2c2ad02540f9c6a055f5af007f271e`

## Mutation targets (pristine byte offsets in tools/inference-ground.py)

- `implicit-neg`: `IMPLICIT_NEG = {…}` 15-word set literal, bytes [10735, 10930) / lines 255–257 → `IMPLICIT_NEG = set()`. Harness: `re.sub(r'IMPLICIT_NEG = \{[^}]*\}', …, flags=re.S)`.
- `un-neg`: two-line `UN_NEG_RE = re.compile(r"^un(?!der|til|…)" r"[a-z]{3,}(?:able|ible|ed|known|clear|sure)$")`, bytes [10931, 11094) / lines 258–259 → `UN_NEG_RE = re.compile(r"(?!)")` (matches nothing).

## Commands and observed output

1. `python3 corpus/evidence/round48/mutation-check.py` (frozen harness, run in-place):
   `PRISTINE_CASES=PASS`; `implicit-neg=KILLED expected-cell=implicit-neg rc=1`; `un-neg=KILLED expected-cell=un-neg rc=1`; other three mutants also KILLED; `MUTANTS_KILLED=5/5`; rc=0; wall 1.11 s.

2. Independent reconstruction (scratch `/tmp/chousa-r48-MutateImplicit`, line-splice not the harness regex): located `IMPLICIT_NEG = {` line, replaced lines through closing `}` with `IMPLICIT_NEG = set()`; located `UN_NEG_RE = re.compile(`, replaced both continuation lines with `UN_NEG_RE = re.compile(r"(?!)")`. Result compared byte-for-byte against each harness lambda applied to pristine source: **implicit-neg byte-identical=True; un-neg byte-identical=True** (mutant sha256 prefixes `93636f1b7f10776e`, `c11d5e2ff5bd5727`).

3. Detector `python3 corpus/evidence/round48/c1-count.py --root <lane> --tool <scratch>/<f>.py --cases-only`:
   - pristine.py: `implicit-neg=PASS rc=0`, `un-neg=PASS rc=0`, all five PASS → `REFINEMENT_CASES=5/5`, `C1_CASES=PASS`, rc=0.
   - implicit-neg.py: `implicit-neg=FAIL wanted_rc=0 observed_rc=1 FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / revision'`; other 4 cells PASS → `4/5`, `C1_CASES=FAIL`, rc=1. KILLED, surgical (only its cell).
   - un-neg.py: `un-neg=FAIL wanted_rc=0 observed_rc=1 FINDING INF_POLARITY_FLIP … / revision'`; other 4 cells PASS → `4/5`, `C1_CASES=FAIL`, rc=1. KILLED, surgical.

4. Mechanism probe (imports of scratch copies, `is_neg` truth table):
   - pristine: `is_neg(lacks)=True is_neg(untraceable)=True |IMPLICIT_NEG|=15`.
   - implicit-neg mutant: `is_neg(lacks)=False is_neg(untraceable)=True |IMPLICIT_NEG|=0` — orthogonal: kills only the lexical-list leg.
   - un-neg mutant: `is_neg(lacks)=True is_neg(untraceable)=False`, `UN_NEG_RE.pattern='(?!)'` — kills only the un-prefix leg.
   Same FINDING line both ways because both cases share span `no revision is recorded`: with the mutant's negator gone, `untraceable`/`lacks` reads affirmative, so bullet word `revision` (stem in the negated scope) has a live negator in its after-window → `INF_POLARITY_FLIP` vs wanted rc 0. Distinct machinery, same flip symptom — correct calibration: each fixture pins exactly one leg of `is_neg`.

5. Restoration: `cp pristine.py implicit-neg.py un-neg.py` in scratch → all three sha256 `9d789b34…5149b`; re-scored both restored files: `REFINEMENT_CASES=5/5`, `C1_CASES=PASS`. Scratch dir deleted.

## Verdict

Both assigned mutants **KILLED** by their named cells under the frozen counter; pristine passes; transforms byte-identical to the harness's; exact bytes restored and re-passed. No coverage finding; C1 mutation leg upheld on my two cells (the other three mutants also KILLED under the same harness run, consistent with `MUTANTS_KILLED=5/5`).
