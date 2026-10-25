# R50CritAxisC1 — C1 attacked as an axis move: plumbing, separable, and it passed a broken adopter

Seat: critic, wave 2 (falsify). Target: frozen R50-C1 (`corpus/evidence/round50/claims.md:20-47`) and
`corpus/evidence/round50/c1-count.py`; neither edited, no lane file written but this report. Scratch
`/dev/shm/chousa-r50-R50CritAxisC1/`, deleted at end. No install, no network, no fetch. My mutants are real-code
edits of the landed `tools/assimilate-rows.py` (m1 `:82` GREP_RE, m2 `:85` ESC_SPLIT, m3 `:96` fragment strip,
m4 `:99` host case); the fake-tool forge attack belongs to `w2/R50CritForgeC1.md` and is not repeated.
## 1. Operability-shaped artifact, not an axis move
`/home/vgpnk/Projects/shokunin/AXES.md:13` defines operability as "Runnable artifacts: checklists that are
executable, commands that exist, scripts that run", observable "A checklist item can be run and produces the
stated outcome". C1's artifact fits: `--selftest` runs and states an outcome. But the lane's score is not that
definition, it is one observable — `SCORECARD.md:7` scores 3, last-change round 1, over the three archived A/B/C
inputs. Re-running its counting command at the tip:
```
$ python3 -c '... tools/research-gate.sh verify ../research/deep-research-2026-09-28/<A|B|C> ...'
VERDICT_BEARING_EXPORTS=3/3
```
C1 moves no point of it, and its own tag says so (`claims.md:47`, `Tag: plumbing (QUALITY 64)`). Verdict:
plumbing with no lane-facing score effect — correct as tagged, wrong if a closure sentence credits C1 to
operability. Calibration note: the observable is capped at 3/10 and has not been re-derived since round 1, so
the round's one genuinely runnable new command cannot be recorded on the axis it belongs to; the round-50 row
must read `operability 3, unchanged, VERDICT_BEARING_EXPORTS=3/3`.
## 2. C1 and C2 are causally separable — observed in both directions
```
$ # root = tools/assimilate-rows.py + corpus/fixtures/assimilate-selftest only (no corpus/knowledge, no SOURCES.md)
$ python3 corpus/evidence/round50/c1-count.py --root …/noadopt        ->  LEGS=5/5  C1=PASS  exit=0
$ # root = corpus/{SOURCES.md,knowledge,lessons/round-50.md,evidence/round50} + tools/inference-ground.py; no adopter
$ python3 corpus/evidence/round50/c2-count.py --root …/noselftest    ->  CAPTURE_BOUND=55/55 … C2=PASS  exit=0
```
C2 passes with `tools/assimilate-rows.py` absent; C1 passes with the whole adoption absent: neither counter can
be satisfied by the other's work. Asymmetry worth stating: C2's *controls* (`controls/build-c2-controls.py`)
drive the adopter to build their before states; only the counter is independent. At the tip: `c1-count.py` →
`LEGS=5/5 C1=PASS` (2.9 s), `c2-count.py` → `BOUND=3/4 REFUSED=1 … C2=PASS`.
## 3. The two named mutants: caught, but by BASELINE, not by the perturbation legs
```
$ c1-count.py --tool m1-colzero.py   # collision grep at column 0 only
BASELINE=FAIL rc=1  PERTURB_PASS=6/6  R49_REGRESSION=FAIL rc=1  LEGS=3/5  C1=FAIL
$ round49/c1-count.py --tool m1-colzero.py  ->  SET_A/B/C PASS  GUARD COLLISIONS=[] -> FAIL  C1=FAIL
$ c1-count.py --tool m2-nopipe.py    # escaped-pipe handling removed
BASELINE=FAIL rc=1  PERTURB P5 … -> FAIL  PERTURB_PASS=5/6  R49_REGRESSION=FAIL  LEGS=2/5  C1=FAIL
$ round49/c1-count.py --tool m2-nopipe.py   ->  SET_C FAIL  PIPE ROWS=0 -> FAIL  GUARD PASS
```
Both are caught twice (round-50 `BASELINE`; round-49 `GUARD`/`SET_C`/`PIPE`). The legs meant to localise them
are vacuous — m1's unperturbed run already prints exactly P1's expected line, m2's already prints 27 `DIFF`
lines including P3's:
```
$ m1-colzero.py --selftest --fixtures …/c1-fixtures --expected …/expected.json | grep ^DIFF
DIFF missing COLLISIONS S011,S012
$ m2-nopipe.py --selftest … | grep -c '^DIFF' ; … | grep 'STRIPPED S015'
27
DIFF missing STRIPPED S015 cell6-pipe
```
So `PERTURB P1 -> PASS` and `PERTURB P3 -> PASS` mean "the line is missing", already true before the
perturbation: the counter never checks a `DIFF` is absent at baseline. Six perturbations prove less than six —
not admit-blocking, but `QUALITY 73` must not be read as "six independent perturbations".
## 4. Yes — C1 passes with the adopter broken on a real package. Observed, not hypothetical

(a) **The round-50 candidate itself.** `ec52e63` is the post-freeze C1 candidate; the erratum's item 1 is its
hardening. The frozen counter passes against it, yet on the real package
(`…/shokuknow/merge/chousa/SOURCES.append.md` + entries `cnki-citation-check-r40.md`,
`citation-matching-semantics-r41.md`, registry at `3c51da7`) it writes the 管理员 manual row with one citing
entry, where the landed tool and the landed row carry both:
```
$ c1-count.py --tool tool-ec52e63.py  ->  BASELINE=PASS findings=26  PERTURB_PASS=6/6  R49_REGRESSION=PASS  LEGS=5/5  C1=PASS
ec52e63  S106 used-by=[ corpus/knowledge/cnki-citation-check-r40.md ]
2573dc1  S106 used-by=[ corpus/knowledge/citation-matching-semantics-r41.md, corpus/knowledge/cnki-citation-check-r40.md ]
SOURCES.md:115 (S105)  used-by=[ corpus/knowledge/citation-matching-semantics-r41.md, corpus/knowledge/cnki-citation-check-r40.md ]
```
Neither leg can see this class: the pinned fixture stages no document twice, and the round-49 `USED_BY`
predicate is per staged id (`users[S124] = {r40}`), so the wrong cell matches. The defect was found by a wave-1
seat running the real adoption, never by C1 — C1's pass is not evidence that the adopter is right on a real
package.

(b) **A mutant that still passes C1 today.** m3, fragment strip removed at `tools/assimilate-rows.py:96`:
```
$ c1-count.py --tool m3-nofrag.py   ->  LEGS=5/5  C1=PASS
# staged row citing https://docs.python.org/3/library/socket.html ; lane row S052 holds …socket.html#socket-timeouts
landed:  S900  S052  held     docs.python.org/3/library/socket.html
m3:      S900  S107  append   docs.python.org/3/library/socket.html
```
A duplicate registry row for a document the lane already holds. The census stops it only when the staged scope
cell equals the held row's: same scope → `E04 … duplicate url … within scope …`
(`scripts/sources-census.sh:645-649`); different scope → only `W04 … duplicate url … across scopes` (`:644`);
both observed on the inserted S107. m4 (host lower-casing dropped, `:99`) also passes `LEGS=5/5`; no real-data
case exists (0 uppercase hosts in `corpus/SOURCES.md`), so m4 stays latent and I claim no breakage for it.

(c) **The lane default leg is replayable.** QUALITY 73 requires an expected file "written from the rule, never
one the tool emits", but `c1-count.py:91-94` only checks the no-flag run prints `SELFTEST=PASS`; the default
package's digest is not pinned. Scratch root whose default `expected.json` I regenerated from the tool's own
`FINDING` lines after deleting the escaped-pipe case from the default `staged.md`:
```
$ <scratch>/tools/assimilate-rows.py --selftest  ->  SELFTEST=PASS findings=25 expected=25
$ c1-count.py --root <scratch>                   ->  LEGS=5/5  C1=PASS
```
The landed bytes are honest today — `corpus/fixtures/assimilate-selftest` and `c1-fixtures` share digest
`c5c56480…` with byte-identical `expected.json` — so this is a hole in the check, not a defect in the state.
## 5. Accounting: a leg that never ran is counted as passed
`c1-count.py:93-94` sets `legs["SELFTEST_DEFAULT"] = True` whenever `--tool` is given, then prints
`SELFTEST_DEFAULT=PASS (skipped: --tool)`. Every receipt measuring a non-lane tool carries one free point: the
base tool's `LEGS=2/5` is 1 real leg, echo's `4/5` is 3, m1's `3/5` is 2. C1 needs 5/5, so the verdict is
unaffected, but a check that did not run is printed as passed.
## Smallest safe correction (no frozen text touched)
1. C1 stands admitted on the landed bytes: `LEGS=5/5`, `C1=PASS` at the tip, both named mutants fail it twice.
   Do not move the operability score; record `3, unchanged` with the 3/3 command.
2. Add to `QUALITY 73`'s named limits the three limits that let C1 pass a broken adopter: C1's only real-package
   leg is the pinned round-49 package (no document staged twice, no fragment URL); the no-flag default leg is
   not digest-pinned and is satisfiable by a tool-emitted expected file; a `--tool` run counts a skipped leg as
   PASS. Plus: C1 passed `ec52e63`, whose used-by on the real round-50 package was wrong — C1 certifies fixture
   and round-49-package conformance, not the adoption.
3. Not this frozen claim: the cheapest added leg is a fixture with one document staged twice and cited by two
   entries, plus a staged URL differing from a held row only by fragment — the two classes C1 is blind to.

VERDICT: attacked C1 as an axis move and as a check — it is plumbing with no score effect and is separable from
C2 both ways, and both named mutants fail it twice, so the claim survives admission; but the check is weaker
than its text: C1 passed `ec52e63`, which was broken on the real round-50 package (used-by), and it still passes
a fragment-normalisation mutant that appends a duplicate row over the lane's real registry — defects in C1's
discriminating power, not in the landed bytes.
