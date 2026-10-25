# Attack08 — round 48 wave 1: held-out Inference bullet probes for the C1 precision class (false-refusal)

- seat: L1Chousa48.Attack08 (reviewer) · date: 2026-10-25 · probe, not a frozen fixture or claim
- item: construct 2 distinct correctly-reasoned held-out Inference bullet examples for the precision class (varied scope, negator distance, unlisted absence words, neighbouring-word binding); run current `tools/inference-ground.py` on scratch copies; state refusal status and why; no round-47 held-out text reuse; no network.

## Method

- Committed local fixtures only (copied verbatim to scratch `/tmp/chousa-r48-Attack08/`):
  - `corpus/fixtures/inference-ground-r47/spans.tsv` (rows S901×2, S902), `spans/S901-1.txt`, `spans/S902-1.txt`, `counts.json`.
  - Span text used: S901-1.txt = `the release ships a frozen pool of pages; no revision is recorded per sentence`.
- Tool: current lane `tools/inference-ground.py`, sha256 `9d789b34562cc0ce35be7e4d7ea67a9fa57eabf8794bbf096c8a8d190925149b` (working tree; `corpus/evidence/round47/c1-count.py` at tip still prints `C1=PASS`, exit 0 — tool healthy).
- Command per bullet: `python3 tools/inference-ground.py --entry $S/<e>.md --spans $S/spans.tsv --counts $S/counts.json --root $S`.
- Entries shaped like the committed r47 fixture `positive-negation-kept.md`: one `#### Inference` bullet quoting `` `no revision is recorded` `` (verbatim in S901).

## Bullet 1 — REFUSED (`FINDING INF_POLARITY_FLIP` 'no revision is recorded / recorded')

- Text: *"The release's recorded history is nil, consistent with `no revision is recorded` (S901)."*
- Correctness: "no revision is recorded" entails the release's recorded history is empty/nil — the bullet asserts absence, matching the span's polarity. No flip.
- Measured output (exit 1):
  ```
  GROUND entry=e1.md section=1 bullets=1 tokens=1 grounded=1
  FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / recorded'
  GROUND: FAIL
  ```
- Why refused: P1 on a negated span. The phrase carries an internal explicit negator `no` (lines 291–296) → negated=True, scope=`[revision, recorded]`, stems `{revis, recor}`. The bullet reuses scope word `recorded` (stem `recor`); measured window before=`[the, release's]`, after=`[history, is]` holds no negator (lines 341–348). Absence is conveyed by `nil`, which is unlisted: not in `NEG_WORDS` (236–237), not in `IMPLICIT_NEG` (255–257), and `UN_NEG_RE` (258–259) does not match it (not an `un-` form). Unlisted-absence-word mechanism (routed defect 1 class: `nonexistent`-type).

## Bullet 2 — REFUSED (`FINDING INF_POLARITY_FLIP` 'no revision is recorded / revision')

- Text: *"The pool cannot assert that any revision was committed, per `no revision is recorded` (S901)."*
- Correctness: if no revision is recorded, the pool cannot assert that any revision was committed — the negation is preserved (modally weakened). `cannot` binds the neighbouring verb `assert` (the modality), not the noun `revision`; the sentence stays correct.
- Measured output (exit 1):
  ```
  GROUND entry=e2.md section=1 bullets=1 tokens=1 grounded=1
  FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / revision'
  GROUND: FAIL
  ```
- Why refused: P1 on the same negated span. Bullet word `revision` (stem `revis`) reused; measured window before=`[assert, that, any]`, after=`[was, committed]` holds no negator. The listed negator `cannot` (`NEG_WORDS`) sits 4 words before `revision` — outside the 3-before/2-after window (line 343). Negator-distance mechanism; the neighbouring-word binding (cannot→assert) is why the bullet is correct.

## Dimension coverage (the four named axes)

- varied scope: B1 restates absence over `recorded history` (`recor` stem) vs the span's `revision`; B2 restates over `any revision was committed` (`revis` stem) vs the span's `revision is recorded`. Both correct restatements across predicate shapes trigger the stem scan.
- negator distance: B2 — a listed negator (`cannot`) beyond the 3-before window ⇒ refusal despite correctness.
- unlisted absence words: B1 — `nil` (same class as `nonexistent`) unrecognized ⇒ no negator found ⇒ refusal.
- neighbouring-word binding: B2 — `cannot` binds `assert`, not `revision`; the lexical window misattributes it.

## Reuse check

- Round-47 held-out text is not reused: B1/B2 sentences do not appear in round-47 w1/w2 reports (checked by grep; HeldOutA p03 `…revision history is nonexistent` and p04 `cannot show that any sentence has been revised` are distinct sentences). The underlying committed span phrase `` `no revision is recorded` `` is necessarily reused (only committed spans exist), but every bullet sentence is new.

## Status

- Both probes are correctly-reasoned and both are refused by the current tool → measured false-refusal rate on this 2-bullet probe: **2/2**. This reproduces the round-47 HeldOutA refusal class (p03 unlisted `nonexistent`; p04 distance) on fresh wording against the current tool.
- Probe only: no fixture, claim, counter, or frozen predicate touched; no network; no tool installs; scratch `/tmp/chousa-r48-Attack08` removed on completion.

## Residual risk / gaps

- Two bullets, one negated phrase, one span set — the rate is a probe, not a population estimate.
- Only the P1 (negated-span) side is probed; the P2 affirmed-span and figure-keys sides of the precision class are left to other seats.
- The check is lexical: correct bullets that avoid scope stems entirely pass, so the refusal class is real but narrow (docstring Named-limit material).
