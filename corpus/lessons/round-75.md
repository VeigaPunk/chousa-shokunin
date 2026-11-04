# Round 75 — QUALITY 126 battery before the freeze; the source-blind order oracle dies

Base: `8022f72c889c904b5657d52c7f29e1643392a216`; freeze A: `43a7a0db52c8aabdf32735f58e09610e05200e79`;
landing: `L1` (content) / `L2` (final tip, receipts). Two claims in `corpus/evidence/round75/claims.md`: C1 operability (lowest
scored non-retired axis, 3/10) and C2 calibration. The historical 3/10 numeric observable is
deliberately not moved.

## Gate

- Admit S184, own-work B, scoped to the two defects routed by the r74 non-author verifier:
  `corpus/lessons/round-74-verifier-spotcheck.md` at `43a7a0db52c8aabdf32735f58e09610e05200e79`, lines 73–74.
  Opened 2026-11-04. Located quotes: line 73 "before any future successor binds a candidate-running counter, meet existing QUALITY 126 with committed prefreeze detection-forger controls and record limits" (20 words); line 74 "append a correction to the lesson's quoted-word counts (16/11 whitespace tokens, not 18/13)" (13 words). Grounds both claims; it is the r74 closure record, not independent truth of any counter.
- Reject S185, own-work C, scoped to `corpus/QUALITY.md` criterion 126 as a source row: same revision, line 1002. Opened 2026-11-04. Located anchor: criterion 126's text. REJECTED because `corpus/SOURCES.md`'s own header separates admission criteria from sources and no fleet lane registers a `corpus/QUALITY.md` row; flip: admit scoped to the criterion's text if an admitted entry ever cites `corpus/QUALITY.md` as the origin of its content rather than as the bar that content must meet. The criterion still binds C1 through the battery, not through a registry row.
- Admit S186, own-work B, scoped to the r74 matrix's discrimination failure:
  `.ufo/waves/round-74/w1/R74Critic/forge-order-oracle.py` line 3 and `forge-order-oracle.log` line 11, byte-identical to the r75 frozen copy (sha256 `180d1a3d…`). Opened 2026-11-04. Located quotes: "Never reads --lane bytes nor any repository content. Scores 9/9 on the frozen" (13 words); `LOADER_MATRIX=9/9 C1=PASS` (2 words). Grounds the C1 target only; not a general forge-freedom claim.
- New registry rows S184 mined, used-by this lesson; S185 rejected, used-by `—`; S186 mined, used-by this lesson. Existing status/recheck/used-by cells unchanged. No URL fetched: all three are committed repo paths.
- Non-author spot-check requested: two admits and one reject above. Dispatched wave seats are author-lane evidence, not independent admission or promotion reviewers.
- Assimilation: none — no package bytes adopted, so no id-collision check is run. `considerthese/2026-10-26.md` was opened; no proposal was adopted this round (claim cap), recorded rather than implemented.

## Corrections to the frozen claims text (append-only; predicates and kill rules unchanged)

- **Fixture topology.** `claims.md` C1 says the successor matrix "writes twelve disposable fixture repositories, one real commit per case". It writes ONE repository per matrix run and twelve case commits inside it (a thirteenth for the base), restoring the fixture bytes before each case; the battery therefore creates fourteen repositories over its two runs, not twenty-four. Found by `R75Review` F3 from the shared `base=` and twelve distinct `rev=` values; the per-case diff is still exactly the single mutation, so the measurement is unaffected.
- **"prints exactly" (C2).** The counter appends `rev=… base=…` to the verdict line, so the claim's `C2=PASS checks=4/4` is a prefix match, not a full-line equality (`R75Review` F10). The C1 `BATTERY=` line is a full-line match.
- **S184 at the freeze.** `claims.md` says C2 is "sourced on S184, opened this round"; S184 is not in the registry at A because the row lands with this lesson (E11 requires the `used-by` path to exist). `R75Review` F6; the row is opened here.
- **"Decidable only from protected-file content" is false (`R75Critic` §2–§3).** The matrix's case
  identity leaks through three stable metadata channels — the commit subject is literally the case
  name, the fixture trees are byte-identical across runs and orders, and the byte sizes differ per
  case — so four content-blind, metadata-reading counters (commit subject, tree-hash memo, `ls-tree -l`
  sizes, plain `Path.stat().st_size`) reach 12/12 exit 0 without opening a blob or implementing any
  check. The claim's sentence and the matrix's own header should be read as "not decidable from
  numstat alone". Source-blind (argv-only) forgers remain capped at 4/12, so C1's predicate survives;
  the memorisation class is cheaper than re-implementation and the frozen battery has no
  metadata-reading subject.
- **Order-randomisation limit is conservative.** The frozen r74 oracle cannot reach 12/12 on the twelve-case matrix under any permutation (max 9/12 over 200 000 permutations, `R75Review` F9); the "lucky permutation is not excluded" sentence overstates the risk for that oracle, not for a hypothetical twelve-entry script.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| a control silently re-created the defect it was meant to isolate | the diff-only and naive-grep forgers were first written with `deleted[path] = int(parts[0])` — the r73 additions-as-deletions bug — so on the r74 matrix they exited 1 for the wrong reason instead of reaching 9/9; the superseded first receipt was overwritten before commit and is not in the tree, so the class is carried by the corrected receipt `corpus/evidence/round75/controls/before-battery-r74-matrix.txt` (diff-only exit 1) against its prediction (exit 0) | the battery prints `matrix_exit=` beside every verdict, and the receipt was read against the pre-registered prediction | forgers read numstat column 1 (deletions); the battery requires `marks` for every verdict, so a subject with no parsed summary line is never scored in the matrix's favour |
| a parser narrower than the union of its inputs turns a pass into "no marks" | the first `MATRIX_LINE` accepted only `MATRIX=`, while the r74 matrix prints `C1=PASS`; every r74 run parsed as `marks=none`, so the battery reported `positive=0/2` while both positives printed 9/9 exit 0, and the SUBJECT labels inverted. Guard shown able to fail: `corpus/evidence/round75/controls/mutation-battery-parser-slip.txt` | the first receipt's `forgers_rejected=0/5 positive=0/2` contradicted the two 9/9 exit-0 runs printed above it | the frozen regex accepts both anchored labels and every verdict requires non-null marks (`corpus/evidence/round75/matrix-battery.py:61`) |
| a claim described its evidence topology from memory rather than from the code | `claims.md` C1's "twelve disposable fixture repositories, one real commit per case" versus one repository per run with twelve case commits (`R75Review` F3, `13-claim-facts.txt`) | the non-author-role reviewer read the matrix's `git init` and the shared `base=`; the L1's own claims file was not re-read against the code before freeze | re-read the instrument before describing it in a frozen claim; the correction is append-only above, and the predicate is unaffected |

## Instrument limits (seat-discovered, recorded not fixed; frozen bytes are not amended after scoring)

- **C1 battery does not test the shuffle (`R75Mutation` M2, surviving mutant).** Removing the
  `random.Random(seed).shuffle(order)` line leaves the battery at `PASS 5/5 2/2` while a twelve-entry
  invocation oracle that reads no repository bytes reaches 12/12. Independently confirmed by the L1:
  `corpus/evidence/round75/controls/shuffle-necessity-r75.txt` (4/12 against the frozen matrix,
  12/12 against a fixed-order scratch copy). The shuffle is load-bearing; the frozen battery does not
  observe it. Next-round item: add the twelve-entry oracle to the battery's subject set.
- **A patch-text-only counter reaches 12/12 (`R75Review` F4).** Reading only the unified `git diff`
  patch (three lines of context) reconstructs every fixture pre-image, so the matrix does not bind a
  candidate to opening a file. The "diff-only" forger is the narrower numstat/name-only shape (9/12).
  The claim sentence "decidable only from protected-file content" survives literally (patch context is
  protected-file content), but the "source-blind vs content" framing is broader than the battery.
- **Both positives are lane-authored in the same commit (`R75Review` F7).** `ref-counter.py` is
  plumbing-independent but not author-independent; agreement proves contract consistency between two
  implementations, not independence. QUALITY 126's r62 precedent records the analogous limit.
- **`SEED=` is informational, not replayable (`R75Review` F8):** the matrix accepts no `--seed`.
- **C2 is a presence test, not a correction test (`R75Review2` F1/F2/F3, `R75Review` F1/F5).**
  `derive()` takes the first `Located quote:` match anywhere, so an insertion above the authored
  bullets rebinds `RECORDED` and a block can pass without correcting 18/13; Q2/Q3 test substring
  presence, so a negation, a wrong magnitude ("161"/"117") or an HTML comment passes 4/4; Q4 is an
  endpoint diff over a caller-supplied base with no ancestry check; Q1 does not enforce "appended at
  the end". At this landing the block is read by eye and states the correction explicitly, and the
  derived 16/11 are correct; the instrument's limits are recorded here. Next-round item: bind the
  derivation to the authored bullet, test polarity/magnitude, require the block to be the last
  section, and check base ancestry.
- **Chronology.** Controls were executed 16:02–16:05 and committed in the same freeze commit as the
  claims (16:06) — which binds no data and precedes the wave dispatch (16:07:40), but is not strictly
  preceding per the sibling precedent `souji` QUALITY Q120. Recorded; next round splits the controls
  commit from the claims commit.

## Boundaries

R71/r72/r73/r74 rejection rulings stay unchanged; no historical landing is retroactively admitted.
R73's completed battery/preflight is not re-claimed, and no Windows-host flock/load question is
treated as answered. The battery proves seven salted subjects on this host; a forge that fully
re-implements the checks is a correct counter for these inputs, and the content cases cover three
duplicate-heading mutations only. No semantic-entailment, arbitrary-counter or general-matrix claim.
External fetch approval, SHONEN promotion and non-author entailment review remain operator-owned and
unanswered; this round needs none of them. No cross-domain source absorbed; PROVINCE unchanged.

## Wave integration and verdict

One v1 wave, 10 seats, all settled, no dead seat (`WAVE-DONE` from Main; `.ufo/waves/round-75/w1-results.json`):
3 executor, 1 scout, 1 scribe, 1 connector, 2 reviewer, 1 critic, 1 mutation-tester (4 attack seats, 40%);
L1 held the canonical planner seat; no residual call.

- `R75ExecA` reproduced both directions twice each (before `2/5` exit 1, after `5/5` exit 0).
- `R75ExecB` independently derived all twelve expectations from the frozen contract before running: 12/12
  derivable, none decided by the diff alone; printed expectations matched its derivation.
- `R75ExecC` isolated the mechanisms in scratch: dropping the three content cases costs the diff-only and
  naive-grep forgers (battery `3/5`), while a fixed-order copy keeps `5/5` — the frozen nine-entry oracle is
  also killed by the twelve-case set, so order randomisation was not independently isolated by that seat.
- `R75Scout` produced a twelve-class forger table: five classes covered (F1–F5), seven not — commit-subject
  oracle, harness-source oracle (reads the matrix's own `CASES` through the parent's command line),
  memorised-fixture oracle, seed-leak oracle (reads the matrix's `SEED=` from the parent's stdout when it is
  a regular file), an unbounded/hanging child, a blocking parent-fd read, and no structural sweep. Each
  uncovered probe reached 12/12 or stalled the matrix.
- `R75Scribe` drafted S184–S186 with a scratch census proving no new E/W finding, and caught its own quote
  defect (`detection-forge` vs `detection-forger`) before committing; the rows are adopted as drafted, with
  S186 as the third row and `corpus/QUALITY.md` rejected (S185).
- `R75Connect` found the sibling precedent `souji` QUALITY Q120 (controls must be in a commit strictly
  preceding predicate freeze), `kumitate` r68 (`a fixture path leaks the answer key`), `tabi` Q33 (a
  feasibility sentence is written only after the cheapest forgery is run); the chronology limit above is
  routed from Q120.
- `R75Review` re-measured both predicates from a clean clone: C1 met at A (four independent runs of the
  predicate line, digest match, before-state reproduced); C2 prospective at A (as the claim declares) with
  findings F1–F10 — the fixture-topology error F3, the patch-text counter F4, the lane-authored positive F7,
  the unreplayable seed F8, the conservative order limit F9 and the C2 presence-test F1.
- `R75Review2` attacked C2: the derivation correctly reads the lesson at `--rev` and the derived 16/11 are
  right, but an insertion above the authored bullets rebinds `RECORDED` (F1) and negating, wrong-magnitude
  and comment-only blocks each score 4/4 (F2); Q4 is an endpoint diff with no base ancestry (F3) and Q1
  does not enforce last-section placement (F4/F5).
- `R75Critic` confirmed the predicate reproduces and proved no argv-only forger exceeds 4/12 (the modal-answer
  ceiling), but four content-blind metadata-reading counters reach 12/12 — the fixture commits are named
  after their cases, the trees are byte-stable, and the sizes are stable — so the claim's "decidable only
  from protected-file content" sentence is false and memorising the twelve states is cheaper than
  re-implementing the checks.
- `R75Mutation` mutated the frozen instruments seven ways: four killed (drop content cases, skip fixture
  restore, wrong receipt path, battery acceptance inverted), three survivors (fixed order, exit 2 accepted,
  check ids ignored) — the last two are coverage findings against the matrix's ok-predicate and are recorded
  above as limits, not amended after scoring.

**Verdicts.** C1 **improved on its frozen predicate** (before `BATTERY=FAIL forgers_rejected=2/5
positive=2/2` exit 1 over the do-nothing matrix; after `BATTERY=PASS forgers_rejected=5/5 positive=2/2`
exit 0 over the successor, stable across five runs in total). C2 **improved on its frozen predicate** at
the landing (`C2=PASS checks=4/4`, exit 0; see the after receipt). No axis harmed: `SOURCES.md` is
additions-only, no held cell changed, no sibling repo or fleet path touched. The historical operability
score stays 3/10 and no capability row is pre-claimed. The round's attack seats falsified the *rationale*
sentences, not the predicates; every falsification is recorded above and routed, and the canonical
non-author closure owns admission.
