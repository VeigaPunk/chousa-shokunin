# Attack07 — C1 false-refusal precision, held-out Inference bullets (precision class #7)

- Seat: Attack07 (round-48 wave 1). Read-only probe; no fixture/claim frozen; no network.
- Tool: `tools/inference-ground.py` at lane HEAD `900c72ec…` (sha256
  `9d789b34562cc0ce35be7e4d7ea67a9fa57eabf8794bbf096c8a8d190925149b`), run from lane root.
- Fixture sources: committed `corpus/fixtures/inference-ground-r47/` spans/counts only; scratch
  copy under `/tmp/chousa-r48-Attack07/igr47/` (spans/S901-1.txt, S902-1.txt, counts.json,
  spans.tsv byte-identical to committed; span_file cells kept relative). Tool runs use that
  scratch manifest; entries are fresh scratch files, not committed fixtures.
- Interpretation note: the round-48 w1-spec numbers twelve precision-class slots (Attack01–12)
  with no committed taxonomy enumerating them; I read slot #7 as probing the round-47 measured
  false-refusal families over a negated span phrase (LabC1FalsePos 9/10; HeldOutA p03/p04),
  with the four named axes — varied scope, negator distance, unlisted absence words,
  neighbouring-word binding.

## Probe bullets (each fresh one-bullet `#### Inference` entry; no round-47 held-out sentence reused)

| probe | bullet (citation `(`S901`)` omitted) | exit | findings |
|---|---|---|---|
| A | The log records `no revision is recorded` per sentence, so any revision that a later edit would leave is missing | 1 | `no revision is recorded / records`; `… / revision` |
| B | Because `no revision is recorded` per sentence, the release's revisions stay absent from the pool, so a reader cannot see later revisions in it | 0 | — (PASS) |
| C | Since `no revision is recorded` per sentence, revision history is nonexistent in this pool | 1 | `no revision is recorded / revision` |

Every run printed `GROUND … bullets=1 tokens=1 grounded=1` — the quote grounds in the S901 span.

## Verdict per bullet

- **A — REFUSED (2 × `INF_POLARITY_FLIP`).** Correct: the log records per-sentence that
  revision is not recorded, so any revision a later edit would leave is missing. P1 fires on
  both restated scope stems (`records`, `revision`) because the only absence word, `missing`
  (listed in `IMPLICIT_NEG`), sits ~9 words from `revision` and ~5 from `records` — outside
  the 3-before/2-after window, so the tool reads the stems as an affirmed re-assertion.
  A one-token recasting of the quoted phrase (`records` for `is recorded`) counts as a second
  flipped scope word.
- **B — ACCEPTED.** Same correct relation, but the absence word `absent` (listed) sits
  immediately after the `revision` stem, inside the 2-after window, so P1's negation
  requirement is met; the later `cannot` is 8+ words from any scope stem and never enters a
  window. Confirms the refusal in A is a window/lexicon artifact of distance, not the
  reasoning.
- **C — REFUSED (`INF_POLARITY_FLIP`).** The unlisted absence word `nonexistent` (`non-`,
  matched by neither `IMPLICIT_NEG` nor `UN_NEG_RE`) sits 2 words before `revision` — inside
  the 3-before window positionally, but invisible to `is_neg`, so no negator registers and
  P1 fires on `revision`. (Same mechanism class as HeldOutA p03, fresh wording.)

## Measured calibration takeaway (no change proposed)

- On this held-out sample over a NEGATED span phrase, correct reasoning is refused whenever
  the absence word is unlisted (`nonexistent`) or farther than 2 words past / 3 before the
  reused stem (`missing`, distance), and accepted when a listed absence word is adjacent
  (`absent`). The frozen C1 positive fixtures all use the adjacent-listed form
  (`positive-negation-kept.md`: `cannot` 2 words after `revision`), so
  `POSITIVE_PASS=3/3` measures one narrow phrasing, not the class — the measured false-refusal
  trade (wave-1 9/10, wave-2 2/12) reproduces on fresh text.
- The three probes exercise all four named axes: varied scope (verb-role recast vs
  attributive/possessive noun recast), negator distance (in-window adjacent vs far),
  unlisted absence words (`missing` listed-but-far, `nonexistent` unlisted-adjacent),
  neighbouring-word binding (absence word vs stem gap vs adjacency).

## Integrity

- Scratch removed before finish per lane rules; no installs (no tooling change needed);
  no network; no production files touched; only this report written to the lane.
