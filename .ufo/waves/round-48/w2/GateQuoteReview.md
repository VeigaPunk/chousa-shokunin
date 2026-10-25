# GateQuoteReview — R48 W2: review of the false-refusal docstring change

seat: `L1Chousa48.GateQuoteReview` (leaf) · 2026-10-25 · HEAD `4bbd2348578bb6288c0700dabf37cea04225bfb6`
scope: review the false-refusal docstring change proposed from R48 W1 reports; extract a mechanism/output/path/documentation evidence table. Read-only; no production edits; scratch `/tmp/chousa-r48-GateQuoteReview` created and removed.

## 1. The proposed change (what is actually being reviewed)

Add a false-refusal (cost) sentence to the **Named limit** of `tools/inference-ground.py:59-62`, which today names only false *negatives* ("a wrong inference through a synonym, an antonym of a different stem, or scope beyond the word windows still passes") and never names a refused *correct* bullet.

- Proposed at `.ufo/waves/round-48/w1/Attack27.md:17` (canonical wording: restated stem refused when no recognized negator sits in the P1 window; `nonexistent`-type unlisted absence forms and out-of-window negators as exemplars; a nearby `not` can trigger P2 over a neighbouring occurrence — "lexical-window strictness, not polarity resolution").
- Endorsed independently by `.ufo/waves/round-48/w1/Attack06.md:75`, `Attack12.md:61` (both: docstring Named limit + round-47 lesson).
- **Already routed by R47**: `corpus/lessons/round-47-verifier-spotcheck.md:62` routed defect 1 names this exact repair (docstring Named limit: "`nonexistent`-type unlisted absence words, negator beyond 3/2 windows, `non-` vs `un-`"); `.ufo/waves/round-47/w2/HeldOutA.md:45-46` proposed the same "smallest safe correction" — still unapplied at R48 tip.
- Tool verified unchanged: `sha256 tools/inference-ground.py` = `9d789b34562cc0ce35be7e4d7ea67a9fa57eabf8794bbf096c8a8d190925149b` (matches every W1 probe except Attack05, which logged `0e5a92b9` — misrecorded hash, does not affect its conclusions); last touched by `02d95d32` (R47 wave-2 fixes).

## 2. Evidence table — false-refusal mechanisms observed by W1

| # | mechanism (lexical rule violated by a CORRECT bullet) | exact output (verbatim, observed) | report path | documented by R47 QUALITY? |
|---|---|---|---|---|
| M1 | P1 phrase leg: bullet restates a negated phrase's stem; absence expressed by an **unlisted absence word** (`nonexistent`, `empty`, `undocumented`, `nil`, `non-`/`un…`-unmatched forms), so no recognized negator sits in the 3-before/2-after window (`inference-ground.py:236-268,343-345`) | `FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / revision'` → `GROUND: FAIL`, exit 1 (also `…/ recorded`, `…/ records`) | `w1/Attack01.md:11`; `w1/Attack02.md:21`; `w1/Attack05.md:28-29`; `w1/Attack06.md:28`; `w1/Attack07.md:40-43`; `w1/Attack09.md:29`; `w1/Attack10.md:32`; `w1/Attack11.md:48`; `w1/Attack12.md:25` | **Not in #67's limit text** — rate (2/12) is in `QUALITY.md:656-658` and mechanism class is in `HeldOutA.md:30` + spotcheck route; the "no recognized negator" (unlisted-absence) exemplar is absent from #67's two named refusal cases. R47-documented class, **not R47-QUALITY-worded** |
| M2 | P1 distance: bullet reuses the stem, a **listed** negator (`cannot`, `nothing`, `missing`, `devoid`, `without`) sits beyond the 3-before/2-after window | same `INF_POLARITY_FLIP` line + `GROUND: FAIL` exit 1 (Attack07-A: `missing` ~9/5 words out; Attack09-1: `devoid` 6+; Attack06-1: `nothing` at word 11+) | `w1/Attack07.md:28-32`; `w1/Attack09.md:32`; `w1/Attack03.md:16-19`; `w1/Attack06.md:33` | **Yes** — `QUALITY.md:657` "a correct bullet whose only negator sits outside the window … is refused"; R47 HeldOutA p04 (`cannot` 5 words out) |
| M3 | P2 neighbouring binding: affirmed phrase; bullet's own negator lands in the 3-before window of a content stem but semantically scopes a different noun/subject (`not the build event`, `not the archive's build clock`, `not necessarily frozen forever`, `not the copy`) | `FINDING INF_POLARITY_FLIP bullet=1 token='the archived copy is dated at build / build'` → `GROUND: FAIL`, exit 1 (variants: `…/ archive'`, `…/ dated'`, `…/ copy'`, `'the release ships a frozen pool / frozen'`) | `w1/Attack01.md:13`; `w1/Attack02.md:23`; `w1/Attack06.md:51`; `w1/Attack10.md:50-51`; `w1/Attack11.md:91`; `w1/Attack12.md:47` | **Yes** — `QUALITY.md:657-658` "whose negator binds a neighbouring word, is refused"; R47 HeldOutA a05 (`is not the copy's build date`) |
| M4 | **Figure leg**: figure grounded by a negated counts key (`figures/answers_without_archive_key`, 1,582); the next-4-words window contains only unlisted absence forms (`keyless`, `unbound`), no listed negator (`figure_flip` `:400-415`) | `FINDING INF_POLARITY_FLIP bullet=1 token='1,582 / counts key figures/answers_without_archive_key'` → `GROUND: FAIL`, exit 1 | `w1/Attack09.md:43-46` (only probe of this leg) | **New finding** — no R47 held-out refusal hit the figure leg; #67 names only the two phrase-leg cases; the docstring rule (`:33-35`) describes the requirement but the Named limit names no figure-leg false positive |
| M5 | (counter-coverage, NOT a docstring item) mut-f mutant misreads ancestor-carried key negation as affirmative → refuses a correct bullet that pristine passes | mutant: `FINDING INF_POLARITY_FLIP bullet=1 token='1,582 / counts key without_archive/count'` exit 1 vs pristine `GROUND: PASS` exit 0; frozen counter prints identical `C1=PASS` for both | `w1/Attack17.md:43-49`; corroborated `w1/Attack16.md:5,13` | Out of docstring scope — routed R47 defect 2 (counter fixture coverage: nested counts keys), `spotcheck.md:63` |

Me, re-run vs committed fixtures (observed now): M1 `…/revision'` FAIL exit 1; M3 `…/build'` FAIL exit 1; M4 `…/figures/answers_without_archive_key'` FAIL exit 1 — all `grounded=1`, all `INF_POLARITY_FLIP`. Verbatim repro of the W1 outputs above.

## 3. Review verdict on the proposal

- **Accurate mechanism attribution.** The three mechanisms the Attack27 wording names map 1:1 to observed W1 outputs: unlisted absence (M1), out-of-window listed negator (M2), neighbouring-word `not` (M3). The reports agree the refusals are lexical-window strictness — correct framing, not a polarity claim.
- **Gap vs W1 evidence: M4 is not covered by the proposed sentence.** The wording exemplars are all phrase-leg; the figure leg's "must be followed by a *listed* negator" refusal (Attack09-2 `keyless`/`unbound`) would remain unnamed. If the change lands, add a figure-leg clause or a phrase such as "the same strictness applies after a negated-key figure".
- **Calibration caveat the docstring must not imply otherwise on:** `precision-count.py` is one-sided — Attack28 (`w1/Attack28.md:5`: do-nothing candidate passes, no flip/control leg) and Attack31 (`:26`: accept-all scores 12/12) measured this; the docstring sentence should describe refusal cost only, not claim the precision gate bounds it.
- **Operability of the change itself:** docstring-only; the frozen R48-C1 counters run tool *behavior* on fixtures (`c1-count.py`, `mutation-check.py`, `precision-count.py`), so this change neither helps nor harms any C1 leg. It discharges routed defect 1 (spotcheck §6.1) only partially unless M4 is included.
- QUALITY.md needs no parallel edit for correctness — #67:656-658 already documents the class and the 2/12 measurement — but if the docstring names `nonexistent`/figure-leg cases, that detail exceeds #67's limit text; harmless divergence, or mirror it there too.

## 4. Commands run (all from lane root)

```
sha256sum tools/inference-ground.py            # 9d789b34… (matches W1 reports)
git rev-parse HEAD                             # 4bbd2348…
git status --porcelain -- tools/inference-ground.py corpus/QUALITY.md corpus/lessons/   # empty (clean)
python3 tools/inference-ground.py --entry /tmp/chousa-r48-GateQuoteReview/{m1,m3,m4}.md \
  --spans …/spans.tsv --counts …/counts.json --root /tmp/chousa-r48-GateQuoteReview      # outputs in §2
```

Reads: `corpus/evidence/round48/claims.md` (frozen C1), `tools/inference-ground.py:20-70,230-273,299-353`, `corpus/QUALITY.md:641-659`, `corpus/lessons/round-47-verifier-spotcheck.md:54-66`, `corpus/lessons/round-47.md:145-156`, `.ufo/waves/round-47/w2/HeldOutA.md:12-46`, and W1 reports Attack01–03,05–12,17,27,28,31,32 plus grep-sweeps of 13–16,18–26,29,30. No installs; no network; no production files changed; scratch verified absent (`ls` → No such file or directory).
