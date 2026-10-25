# LabC1FalsePos — round 47 wave 1, labrat probe of the C1 polarity probe

## Item
Hypothesis: "the polarity probe refuses fewer than 1 in 5 correctly-reasoned bullets that
discuss a negated span phrase". 10 short fixture entries in the shape of
`corpus/fixtures/inference-ground-r47/positive-negation-kept.md`, each with one `#### Inference`
bullet that quotes a NEGATED phrase of `spans/S901-1.txt` or `spans/S902-1.txt` and reasons
correctly about it; run the landed tool on each against the r47 fixture spans and counts.

## Verdict
**Hypothesis FALSIFIED. Refused 9/10 (90%); bound was < 2/10.** Every refusal is
`INF_POLARITY_FLIP`, and every one comes from rule 5 P1: the bullet reuses a scope-word stem
(`revis`, `recor`, `archi`) in its own unquoted words, and no literal negator sits in the
window of 3 words before or 2 words after. The tool does what the frozen predicate says
(claims.md:35-36), so this is a **calibration tradeoff of the frozen predicate**, not a code
defect. Natural academic English expresses absence with words the tool does not count as
negators (`lacks`, `absent`, `untraceable`, `unverifiable`, `unsuitable`). It also puts the
negator outside the window (`cannot … when the archive is checked`), or restates the negated
noun affirmatively as the subject of an absence claim (`revisions are untraceable`).

## Environment
- Lane HEAD `a15610a59aaeaf43b79ccc650acee4bd4da00341` (the C1 landing); `tools/inference-ground.py`
  is unmodified in the working tree; sha256 `8899e7868ffb66fd0d58162342a20a2ab6f3a0e1aee7d0d5b36aa1b7fd7a0a40`.
- Spans: S901 = `the release ships a frozen pool of pages; no revision is recorded per sentence`;
  S902 = `the archived copy is dated at build time; a placeholder value is not an archive link`.
- Negated phrases probed (the in-phrase negator puts each in P1 scope, tool lines 254-272):
  `no revision is recorded` (scope stems `revis`, `recor`) and `not an archive link`
  (scope stems `archi`, `link`).
- No installs. No network. Scratch `/tmp/chousa-r47-LabC1FalsePos/` was deleted at the end.

## Baseline (the landed fixtures, same flags)
`python3 tools/inference-ground.py --entry corpus/fixtures/inference-ground-r47/<f> --spans …/spans.tsv --counts …/counts.json`
```
junk-flip-asserted.md   FINDING INF_POLARITY_FLIP token='no revision is recorded / revised'  exit=1
junk-flip-denied.md     FINDING INF_POLARITY_FLIP token='the release ships a frozen pool / frozen' exit=1
junk-flip-figure.md     FINDING INF_POLARITY_FLIP token='7,572 / counts key answers_named_source' exit=1
positive-affirmed.md    GROUND: PASS exit=0
positive-figure-negated.md GROUND: PASS exit=0
positive-negation-kept.md  GROUND: PASS exit=0
```
(The first loop omitted `--entry` and every run exited 2 with a usage error; the loop was rerun with `--entry`.)

## Probe runs
Command per probe (run from the lane root):
`python3 tools/inference-ground.py --entry /tmp/chousa-r47-LabC1FalsePos/pNN.md --spans corpus/fixtures/inference-ground-r47/spans.tsv --counts corpus/fixtures/inference-ground-r47/counts.json`

Each run printed `GROUND … bullets=1 tokens=1 grounded=1`, so every quote grounded.

| # | bullet (citation `(\`S90x\`)` omitted) | exit | finding(s) |
|---|---|---|---|
| 01 | Because `no revision is recorded` per sentence, revisions are untraceable to the sentence they changed | 1 | `no revision is recorded / revisions` |
| 02 | The record lacks any revision at sentence grain, since the span states `no revision is recorded` | 1 | `… / record`; `… / revision` |
| 03 | Since `no revision is recorded`, the revision history of each sentence is absent from the release | 1 | `… / revision` |
| 04 | With `no revision is recorded` per sentence, a reader cannot date when a sentence was last edited | 0 | — (PASS) |
| 05 | The phrase `no revision is recorded` implies the pool is static: nothing in it is revised after release | 1 | `… / revised` |
| 06 | Because `no revision is recorded`, any claim that a sentence was revised later is unverifiable from this capture | 1 | `… / revised` |
| 07 | Because the placeholder value is `not an archive link`, a citation carrying it lacks a usable archive | 1 | `not an archive link / archive` |
| 08 | A placeholder is `not an archive link`, so a check that counts it as archived overstates coverage | 1 | `not an archive link / archived` |
| 09 | Because a placeholder value is `not an archive link`, it cannot stand in for one when the archive is checked | 1 | `not an archive link / archive` |
| 10 | Under `no revision is recorded`, the pool cannot show which sentence changed, so it is unsuitable for revision-sensitive evaluation | 1 | `no revision is recorded / revision` |

Refusals: **9/10**. Accepted: p04 only. It passes because its unquoted words contain no `revis`/`recor`
stem; it was not judged correct.

Probe sha256 values (files now deleted):
p01 84c7bbab…c02 · p02 2eefbc7e…1d588d9 · p03 2773eb26…e6 · p04 8b279e04…dc · p05 0a78b87f…db ·
p06 2d8775f8…de · p07 d1dfc935…89 · p08 61f093af…11 · p09 417c8c20…52 · p10 b13600d6…b8aa.

## Why each one fails (mechanism, tool lines 275-299)
- Implicit negators are outside `NEG_WORDS` (lines 222-223): `lacks` (p02, p07), `absent` (p03),
  `untraceable` (p01), `unverifiable` (p06), `unsuitable` (p10). The tool reads them as affirmative.
- The window is too short: in p09, `cannot` sits 6 words before `archive`, and the window is 3 before
  and 2 after. In p05, `nothing` sits 4 words before `revised` (`nothing in it is revised`).
- The negated noun becomes a subject or modifier: `revisions are untraceable` (p01), `revision
  history` (p03), `revision-sensitive` (p10), and `counts it as archived` (p08, a counterfactual that
  the bullet itself rejects).

## Counterexample (strongest)
p01 is the assignment's own exemplar wording: "because no revision is recorded, revisions are
untraceable". It is semantically identical to the landed positive `positive-negation-kept.md`
("a revision cannot be traced"). The tool accepts the landed form and refuses the exemplar. The
landed positive passes only because its author placed `cannot` within 2 words after `revision`,
so `POSITIVE_PASS=3/3` measures that one phrasing, not the class.

## Impacted axes
- **Calibration**: the false-refusal rate on correct bullets that discuss a negated phrase is about 90%
  on this sample. The C1 counter's 3 positives do not sample the class (selection bias in the
  fixture set, which is frozen and is not proposed for change here).
- **Operability**: authors must either phrase every absence with a literal `no/not/never/cannot/without`
  within the window, or avoid restating the negated noun. Neither is documented in the tool's
  docstring. Its "Named limit" (lines 44-48) lists only false NEGATIVES (synonym, antonym, scope).
- **Depth (C3 risk)** [INFERENCE]: the C3 leg requires both adopted claim-support-test entries to
  exit 0 under this tool. Any Inference bullet in them that quotes a negated span phrase (FEVER
  "NOT ENOUGH INFO"-style spans) and then uses its stem affirmatively will be refused, which
  pressures drafters to reword correct reasoning to satisfy the lexer.

## Smallest safe correction (no predicate, counter, fixture, floor or target change)
1. Add to the tool docstring's "Named limit" a FALSE-POSITIVE sentence: rule 5 P1 refuses a correct
   bullet that restates a negated phrase's stem without a literal negator in its 3-before/2-after
   window (implicit negators such as `lacks`/`absent`/`un-…` and long-range `cannot` do not count).
2. Have the round-47 lesson record the measured rate (9/10 on this probe set) as a calibration
   tradeoff of the frozen C1 predicate, for the canonical judge to weigh. Whether to widen
   `NEG_WORDS` or the window is a next-round claim with new fixtures. It is not a wave-1 edit.
3. C3 drafters should run the tool on the two adopted entries early and record any P1 refusal
   verbatim rather than silently rewording.

## Cleanup
`rm -rf /tmp/chousa-r47-LabC1FalsePos` was run after writing this report.
