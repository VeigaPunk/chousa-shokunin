# Attack11 — round 48 wave 1: held-out precision probe, class #11 (C1 false-refusal)

seat: L1Chousa48.Attack11 (reviewer, leaf) · 2026-10-25 · item: construct 2 distinct
correctly-reasoned held-out Inference bullet examples for the precision class (varied
scope, negator distance, unlisted absence words, neighbouring-word binding); use only
committed local fixture spans/counts; run the current `tools/inference-ground.py` on
scratch copies; state whether each correct bullet is refused and why. Round-47 held-out
bodies not reused.

## 0. Tool and fixture grounding

```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD
``` (lane HEAD read at run time; tool `tools/inference-ground.py` unmodified, run from
lane root)

Spans/counts: committed `corpus/fixtures/inference-ground-r47/` only —
`spans.tsv` (S901, S902), `spans/S901-1.txt`, `spans/S902-1.txt`,
`counts.json`. No network. No installs. Scratch `/tmp/chousa-r48-Attack11/` deleted at
close.

## 1. Probe A — negated phrase, unlisted absence word, distance

Entry (scratch `probe-a.md`, shaped like `positive-negation-kept.md`):

```
# Probe A — negated span phrase, correct reasoning via unlisted absence word (held-out)

source: S901 — https://example.invalid/fixture-a — a fixture span, not a real source

#### Observation

- The span records no per-sentence revision (`S901`).

#### Inference

- Because `no revision is recorded` per sentence, any revision timeline a reader tries to build is nil (`S901`).
```

Run:

```
$ python3 tools/inference-ground.py --entry /tmp/chousa-r48-Attack11/probe-a.md \
    --spans corpus/fixtures/inference-ground-r47/spans.tsv \
    --counts corpus/fixtures/inference-ground-r47/counts.json \
    --root /tmp/chousa-r48-Attack11
GROUND entry=probe-a.md section=1 bullets=1 tokens=1 grounded=1
FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / revision'
GROUND: FAIL
exit=1
```

**Refused — yes.** Token grounded (grounded=1); the refusal is `INF_POLARITY_FLIP`.

Why: the quote `no revision is recorded` carries an in-phrase negator (`no`), so
rule 5 P1 treats the span as negating it, scope stems `revis`/`recor`
(`occurrence_polarity` → `content(inner[1:])`). The bullet's unquoted words restate
`revision` (stem `revis`) with no negator in the 3-before/2-after window: before =
[`sentence`, `any`], after = [`timeline`, `a`]. The absence word `nil` is unlisted —
not in `NEG_WORDS`, not in `IMPLICIT_NEG`, and no match for `UN_NEG_RE` (starts with
`ni`, not `un`; `non-` forms are likewise unmatched) — and it sits six words past the
stem, beyond both windows. The bullet is correct (no per-sentence revision ⇒ any
revision timeline is empty), but the lexical probe cannot see the negation.

## 2. Probe B — affirmed phrase, neighbouring-word binding, in-window negator

Entry (scratch `probe-b.md`):

```
# Probe B — affirmed span phrase, correct hedged reasoning with neighbouring negator (held-out)

source: S901 — https://example.invalid/fixture-a — a fixture span, not a real source

#### Observation

- The span says the pool ships frozen (`S901`).

#### Inference

- Although `the release ships a frozen pool`, the pool is not necessarily frozen forever (`S901`).
```

Run:

```
$ python3 tools/inference-ground.py --entry /tmp/chousa-r48-Attack11/probe-b.md \
    --spans corpus/fixtures/inference-ground-r47/spans.tsv \
    --counts corpus/fixtures/inference-ground-r47/counts.json \
    --root /tmp/chousa-r48-Attack11
GROUND entry=probe-b.md section=1 bullets=1 tokens=1 grounded=1
FINDING INF_POLARITY_FLIP bullet=1 token='the release ships a frozen pool / frozen'
GROUND: FAIL
exit=1
```

**Refused — yes.** Token grounded; refusal is `INF_POLARITY_FLIP`.

Why: `the release ships a frozen pool` is affirmed in the span (no negator inside or in
the three preceding span words), scope stems `relea`/`ship`/`froz`/`pool`. The bullet's
own word `not` sits two words before `frozen` (before = [`is`, `not`, `necessarily`]),
so P2 flags `frozen` — even though the negator binds to `forever` (a scalar hedge:
shipping frozen does not entail frozen forever), not to frozenness. Correct reasoning,
lexical refusal.

## 3. Result and calibration read

- **2/2 correct bullets refused** on this sample, both `INF_POLARITY_FLIP`; neither was
  confused with ungrounded/uncited (tokens=1 grounded=1 on both).
- The two refusals are the two documented false-refusal mechanisms (round-47 routed
  defect 1; `HeldOutA` p03/p04): unlisted absence word plus distance (A), and an
  in-window bullet negator whose real scope is a neighbouring constituent (B).
- Dimension coverage: **varied scope** — A restates the negated noun `revision`; B's
  affirmed-phrase `pool` (subject) passes while `frozen` (complement) is flagged.
  **Negator distance** — A: no listed negator in window (absence only via `nil`, 6+
  words out); B: negator in window (2 before) → triggers. **Unlisted absence words** —
  `nil` (A). **Neighbouring-word binding** — B: `not` binds to `forever`, not to
  `frozen`; A: before/after windows of `revision` are negator-free. (Round-47 list
  `IMPLICIT_NEG` includes `lacks`/`absent`/`missing`/`devoid`/`un-…` forms;
  `nil`, `nonexistent`, `zero`, `gone`, `free of` are outside it.)
- Distinctness: neither bullet appears in round-47 held-out sets (`LabC1FalsePos`
  p01–p10, `HeldOutA` p01–p06/a01–a06, `HeldOutB` hb01–hb12); probes are correct
  (the hb bodies are flips by construction) and use new wording (`revision timeline …
  is nil`; `not necessarily frozen forever`).
- No tool/counter/fixture/predicate change made or proposed; this is a probe only.

## 4. Commands run

Two `python3 tools/inference-ground.py` invocations above (verbatim decisive output);
`git rev-parse HEAD` noted; scratch `/tmp/chousa-r48-Attack11/` removed after this
report was written.
