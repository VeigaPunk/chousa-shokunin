# MutC1Probe — mutation probe of rule 5 (`INF_POLARITY_FLIP`) against the frozen C1 counter

Seat: mutation-tester, round 47 wave 1. Item: one /tmp mutant each of
`tools/inference-ground.py` — (a) P1 off, (b) P2 off, (c) P3 off, (d) stem 5→3,
(e) P1 after-window 2→0, (f) `is_neg` ignores `n't`, (g) STOP emptied, (h) polarity
from the LAST carrying span. Each one is scored by the frozen counter. For every survivor:
the fixture that kills it, and whether it is a counter gap or a harmless equivalence.
Lane head `a15610a59aaeaf43b79ccc650acee4bd4da00341`. No fetch, no lane writes besides this file, no installs.

## Pristine bytes and mutant sites
- `tools/inference-ground.py` sha256 `8899e786…7a0a40` (copied to /tmp as `pristine.py`, same hash);
  `corpus/evidence/round47/c1-count.py` sha256 `6d39dce5…bc023d0cc7`.
- Mutants were built by one exact-once string replace each (an assert checks the count is 1):
| id | site (pristine path:line) | change | mutant sha256[:16] |
|---|---|---|---|
| a | inference-ground.py:296 | `if negated and …` → `if False and negated and …` | 53e16161909007f0 |
| b | :298 | `elif not negated and …` → `elif False and …` | df7d43fefe37d4ea |
| c | :343 | `return key_neg != any(…)` → `return False` | 700ae04a564c7b14 |
| d | :243 | `w[:5]` → `w[:3]` | 5ad1ffe957cf0c81 |
| e | :295 | `uw[j + 1:j + 3]` → `uw[j + 1:j + 1]` | 8cedee93991f2ffe |
| f | :239 | `return w in NEG_WORDS` (drops both `n't` tests) | a203e9f08cb059ba |
| g | :225–230 | `STOP = set()` | dd2e61ad92896dda |
| h | :261 (inside `phrase_polarity`) | `for s in spans:` → `for s in reversed(spans):` | ddfaa3665d04c76c |

## Frozen-counter scores (verbatim)
Command for each: `python3 …/corpus/evidence/round47/c1-count.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --tool /tmp/chousa-r47-MutC1Probe/<m>.py`
```
pristine     TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS exit=0
a-P1-off     TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=2/3 CANARY=fail R46_COUNTER=pass R46_ENTRIES=2/2 C1=FAIL exit=1
b-P2-off     TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=2/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=FAIL exit=1
c-P3-off     TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=2/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=FAIL exit=1
d-stem3      TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS exit=0
e-after0     TOOL=present POSITIVE_PASS=2/3 JUNK_KILLED=3/3 CANARY=fail R46_COUNTER=pass R46_ENTRIES=2/2 C1=FAIL exit=1
f-no-nt      TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS exit=0
g-STOP-empty TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS exit=0
h-last-span  TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS exit=0
```
Baseline is green, so every verdict below is conclusive. **Killed 4/8 (a, b, c, e). Survived 4/8 (d, f, g, h).**

Which fixture killed each one (direct tool runs on the 6 lane fixtures, findings verbatim):
- a: `junk-flip-asserted` rc=0 (pristine rc=1 `'no revision is recorded / revised'`). It also fails CANARY, because canary-b is a copy of this fixture.
- b: `junk-flip-denied` rc=0 (pristine rc=1 `'the release ships a frozen pool / frozen'`).
- c: `junk-flip-figure` rc=0 (pristine rc=1 `'7,572 / counts key answers_named_source'`).
- e: `positive-negation-kept` rc=1 `'no revision is recorded / revision'`. Its negator `cannot` sits only in the after-window. Also CANARY-a.
Each of P1, P2, P3 and the after-window has exactly one fixture keeping it alive.

## Survivors — kill fixtures (built under /tmp, run pristine vs mutant, verbatim)
Each kill fixture is a dir with `spans.tsv` (7 cols), `spans/`, empty `counts.json` and one entry with one Inference bullet.
```
kd-pos-near-stem [positive] pristine: rc=0
kd-pos-near-stem [positive] d-stem3: rc=1 FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / recent'
kf-junk-isnt [junk] pristine: rc=1 FINDING INF_POLARITY_FLIP bullet=1 token='the release ships a frozen pool / frozen'
kf-junk-isnt [junk] f-no-nt: rc=0
kf-pos-isnt [positive] pristine: rc=0
kf-pos-isnt [positive] f-no-nt: rc=1 FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / revision'
kg-pos-stopword [positive] pristine: rc=0
kg-pos-stopword [positive] g-STOP-empty: rc=1 FINDING INF_POLARITY_FLIP bullet=1 token='release ships with a frozen pool / with'
kh-junk-order-ab [junk] pristine: rc=1 FINDING INF_POLARITY_FLIP bullet=1 token='revision is recorded / revision'
kh-junk-order-ab [junk] h-last-span: rc=0
kh-junk-order-ba [junk] pristine: rc=0
kh-junk-order-ba [junk] h-last-span: rc=1 FINDING INF_POLARITY_FLIP bullet=1 token='revision is recorded / revision'
```
- **d (stem 3) — counter gap.** Kill: a positive whose bullet has an unnegated word that shares
  3 letters but not 5 with a negated scope word. Span `no revision is recorded` (S901); bullet "Because
  `no revision is recorded` per sentence, a revision cannot be traced, so recent edits stay
  unattributed". `recent`→`rec` = `recorded`→`rec`. A shorter stem only adds matches, so the mutant
  can never miss a junk the pristine kills. Only a positive can kill it, and none of the 3 positives has a
  near-stem neighbour. The mutant is not equivalent: it is a real precision loss against the frozen "same
  five-letter stem" rule (claims.md:35).
- **f (no `n't`) — counter gap, and it hurts both ways.** Kill as junk: "the pool isn't frozen" after
  `the release ships a frozen pool`. P2 goes blind, a missed flip in the D7 class. Kill as positive: "a
  revision isn't traceable" after `no revision is recorded`. The P1 after-window loses its negator, a
  false refusal. None of the six fixtures or the canary contains a contraction. Every negator they use
  is a NEG_WORDS member (`no`, `not`, `cannot`).
- **g (STOP emptied) — counter gap, low severity.** Kill: a positive whose quoted phrase contains a STOP
  word, with that word negated in the bullet's own text. Span `every release ships with a frozen pool of pages`;
  bullet "Since `release ships with a frozen pool`, the pool is frozen at release, not with later
  edits". P2 fires on `with`. An empty STOP only enlarges the scope and the bullet-word sets, so the mutant
  is a strict superset of the pristine's refusals. Only a positive can kill it. No fixture phrase holds a STOP word: the
  phrases are `no revision is recorded`, `the release ships a frozen pool` and
  `the archived copy is dated at build`, and their ≥4-letter words are all non-STOP.
- **h (last span) — equivalent on the frozen set; it exposes order dependence in the pristine probe.**
  `span_texts` (inference-ground.py:167–190) appends one text per manifest row. The fixture's only
  multi-row source, S901, has both rows on `spans/S901-1.txt`, so the first and last texts are identical
  and the mutant is equivalent there. Kill: two S904 rows on different files that carry one phrase with opposite
  polarity (`no revision is recorded per sentence` vs `a revision is recorded per page`), plus a bullet
  asserting `revision` with no negator. With rows in order a→b, the pristine kills it and h passes it.
  With rows b→a, the verdicts swap. **Finding:** the pristine verdict on the same junk entry depends on
  the spans.tsv row order. "First carrying span" (inference-ground.py:255 docstring) is a tie-break, not
  a polarity rule, and claims.md:32–41 never states it. So h differs from the pristine only up to a
  permutation of manifest rows. As a counter gap it matters only for conflicting-polarity spans, which
  the counter has no fixture for. Whether a conflicting-polarity phrase should be refused outright is a
  design question for the owner, not for this seat.

## What would close the gaps (coverage findings; the frozen C1 set is not proposed for change)
A later round's counter could add a near-stem positive (d), an `isn't`/`doesn't` junk and positive pair (f),
a STOP-word-in-phrase positive (g), and a two-span conflicting-polarity fixture whose expected verdict
does not depend on row order (h). The four bullets above are ready to use as drafts.

## Restoration evidence
- Lane bytes were never edited. Only /tmp copies were mutated. After all runs:
  `sha256sum -c lane-before.sha` → `…/tools/inference-ground.py: OK`; c1-count.py still `6d39dce5…`;
  `git status --porcelain tools corpus/fixtures corpus/evidence/round47` printed nothing → `CLEAN`.
- Scratch /tmp/chousa-r47-MutC1Probe/ (pristine.py, the 8 mutants, gen.py, kill.py, kill/) was deleted at the end of the seat.
- Environment: Python 3.14.8. Installs: none.
