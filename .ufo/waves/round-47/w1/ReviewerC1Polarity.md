# ReviewerC1Polarity — round 47 wave 1

Item: code-review the polarity probe (`phrase_polarity`, `polarity_flips`, `count_keys`,
`figure_flip`, call sites in `main`) of `tools/inference-ground.py` against docstring
rule 5 (lines 26-35) and the R47-C1 rule sentence `corpus/evidence/round47/claims.md:33-41`;
run the six fixtures; report every code/sentence mismatch; no edits.
Reviewed: lane HEAD `a15610a` (landing), tool sha256
`8899e7868ffb66fd0d58162342a20a2ab6f3a0e1aee7d0d5b36aa1b7fd7a0a40`; working tree clean for
`tools/` and the fixture dir. LSP: not used (no `lsp` device available on this seat; text read
of a single 460-line file). No installs. No fetch. Scratch `/tmp/chousa-r47-ReviewerC1Polarity/` deleted.

Verdict (recommendation): the frozen predicate holds (`C1=PASS`), and the checklist items mostly
match the sentence. Three figure-path defects let a junk flip pass where the sentence
demands a refusal (M1, M2, M3). Two code-only tie-break rules are absent from the sentence
(M4 first carrying span, M5 mixed keys). Lows L1-L5 are narrowings or widenings the sentence does not state.

## Runs (verbatim, trimmed)
`python3 tools/inference-ground.py --entry $F/<n>.md --spans $F/spans.tsv --counts $F/counts.json --root $F`
(F=`corpus/fixtures/inference-ground-r47`):
```
positive-affirmed.md        GROUND: PASS exit=0
positive-figure-negated.md  GROUND: PASS exit=0
positive-negation-kept.md   GROUND: PASS exit=0
junk-flip-asserted.md  FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / revised'  exit=1
junk-flip-denied.md    FINDING INF_POLARITY_FLIP bullet=1 token='the release ships a frozen pool / frozen' exit=1
junk-flip-figure.md    FINDING INF_POLARITY_FLIP bullet=1 token='7,572 / counts key answers_named_source' exit=1
```
(each also printed `GROUND entry=<n> section=1 bullets=1 tokens=1 grounded=1`)
`python3 corpus/evidence/round47/c1-count.py` →
`TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS` exit 0.

Scratch probes (`probe.py`/`probe2.py`, importing the tool and running its CLI on
one-bullet entries with their own spans.tsv/counts.json). Each line below is verbatim tool
output, labelled with the probe name.

## Checklist (code line → sentence)
| item | code | matches sentence? |
|---|---|---|
| P1 window 3 before / 2 after | `:295` `uw[j-3:j]`, `uw[j+1:j+3]` | yes. W2 `rarely not traced` (neg 3rd after) → FLIP; W3 `never appear` (2nd after) → PASS |
| P2 window 3 before | `:295`,`:298` | yes. W4 `never is the pool frozen` → flags `pool` only |
| span negator window 3 before | `:269` `words(s[:idx])[-3:]` | yes. W6 neg 4 back → not negated; W7 neg 3 back → negated |
| figure window 4 after | `:342` `words(...)[:4]` | yes (positive-figure-negated has `no` as exactly word 4) |
| five-letter stem | `:242-243` `w[:5]` | yes; P2 also stem-matches (L2) |
| STOP words | `:225-230`, used `:247`,`:293` | not in the sentence (L4) |
| `unquoted()` drops S-ids | `:250-251` via `ID_RE` `:58` | yes (`x S901 s901 S90 y` → `x   s901 S90 y`) |
| `unquoted()` drops all quoted phrases | `:250-251` | **no** (L3) |
| first carrying span decides | `:261-271` | code says so (`:255`); sentence does not (M4) |
| curly n't | `:231` WORDS_RE has `\u2019`; `:239` | yes. A1 `isn’t frozen` → FLIP. U+02BC `isnʼt` → PASS (L5) |
| span-grounded figure skips P3 | `:415` grounds first, then `:420` `if not ok`; `:416` excludes numerals from P1/P2 | yes, consistent with "grounded by a counts key". F6 → PASS |
| mixed-polarity keys decide nothing | `:334-336` | code only, not in sentence or rule 5 (M5) |

## Findings by severity

### Medium — junk the sentence refuses passes
- **M1 duplicate figure: only the first occurrence is checked.** `figure_flip` `:339`
  `text.find(tok)` always returns the first position. When a figure appears twice, both
  tokens are checked at that first position. F4 bullet `7,572 answers name a source, and 7,572 answers name no source (S902)`
  under key `answers_named_source` → `exit=0 GROUND: PASS`. The sentence says "a figure …
  must not be [followed by a negator]", which applies to every occurrence.
- **M2 figure located by substring, not at a digit boundary.** `:339` uses `find`; `numeral_in`
  `:130-133` already enforces digit boundaries for grounding, but `figure_flip` does not
  reuse it. F5 bullet `1582 rows carry a key, and 582 answers name no source` with counts
  `{"answers_named":582,"rows_keyed":1582}` finds `582` inside `1582`, reads the window
  `rows carry a key` → `exit=0 GROUND: PASS`. The same bug can falsely flag a correct bullet.
- **M3 string-valued counts escape P3.** `count_values` `:367-368` grounds digit strings, but
  `count_keys` `:320-324` indexes only int/float values. For a string value, `keys` is empty,
  so `:335` returns False. F1 counts `{"answers_named_source":"7572"}` with bullet
  `7,572 answers name no source` → `exit=0 GROUND: PASS`. The sentence covers any figure "grounded by a counts key".
- **M4 manifest row order decides polarity.** `phrase_polarity` `:261-271` returns at the
  first span in `spans.tsv` row order that contains the phrase, and within that span at the
  first `find` hit. The sentence (`claims.md:33-34`, "if the span NEGATES it") and rule 5
  (`:27-28` "a phrase its span NEGATES") never say "first". The two probes use the same
  bullet (`Because \`revision is recorded\`, every sentence is revised`) and the same two
  spans: S901 `a revision is recorded per page` and S903 `no revision is recorded here`.
  P5b (S901 row first) → `exit=0 GROUND: PASS`. P5c (rows swapped) →
  `FINDING INF_POLARITY_FLIP … 'revision is recorded / revised'` exit=1. P5d (a single span,
  affirmed occurrence first, then the negated one) → `exit=0 GROUND: PASS`. The verdict
  therefore depends on manifest ordering, which is not a property of the bullet.
- **M5 mixed-polarity keys: the sentence does not say "decide nothing".** `:334-336` returns
  False when the figure's keys disagree. That rule appears only in the `figure_flip`
  docstring `:333`, not in rule 5 or `claims.md:38-41`. Read literally, the sentence imposes
  both requirements, which together refuse the bullet. F2 counts `{answers_named_source:7572, answers_without_key:7572}`
  with bullet `7,572 answers name no source` → `exit=0 GROUND: PASS`. One added counts key
  turns P3 off for that value.

### Low
- **L1 key-name parsing is narrower than "name carries".** `:334` splits only on `_` and
  checks only the leaf key (`count_keys` `:315-316` passes `str(k)` for the leaf). F3
  `answers-without-archive`, F3b `answersWithoutArchive`, and F7 nested
  `{"without_archive":{"count":1582}}` are each read as affirmative. A correct bullet
  `1,582 answers carry no archive key` is then refused, e.g.
  `FINDING INF_POLARITY_FLIP … '1,582 / counts key count'`.
- **L2 P2 matches by stem; the sentence says "content words".** `:293` applies `stem(w) not in stems`
  to both P1 and P2. The sentence names the five-letter stem only for P1 (`claims.md:35`),
  while P2 says "one of the phrase's content words" (`:38`). W1 `there is no frozenness`
  → FLIP `/ frozenness`. This widens P2 beyond the sentence.
- **L3 `unquoted()` does not remove all quoted text.** It removes only straight-double and
  backtick runs of 4 or more characters (`QUOTE_RE`/`BACKTICK_RE` `:59-60`).
  - Curly quotes `“…”` and single quotes `'…'` stay in the bullet's own words. B2
    `the pool is “not” frozen` → FLIP: the curly-quoted negator counts as the bullet's own.
  - A backtick run shorter than 4 characters makes `BACKTICK_RE` pair its closing backtick
    with the next opening one, removing the bullet's own words in between.
    `a \`no\` b c \`S901\`` → `'a \`no  \`'`, and `b c` becomes a grounding token. B1
    `the \`v2\` pool is not frozen (\`S901\`)` → `FINDING INF_TOKEN_NOT_IN_SPAN … 'pool is not frozen ('`.
    It still exits 1, but under the wrong code: the flip is never seen by P2.
  - The pairing regex predates round 47, but rule 5 now relies on it.
- **L4 the STOP list and 4-letter floor are not in the sentence.**
  - `content` `:247` and `:293` drop words under 4 letters and the 56 STOP words. When a
    phrase's scope becomes empty, `:288` returns no finding.
  - K1 span `copy is not the same` with bullet `the copy is the same` → PASS (`same` is a STOP word).
  - K2 `key is not set` with bullet `the key is set` → PASS (`set` has 3 letters).
  - K3b: a 4-letter word stems to itself, so `copy` never matches `copies` (`copie`). `no copy exists` with
    `many copies are kept` → PASS.
  - The sentence's "scope words" and "content words" are defined only in the docstrings at `:256-259`.
- **L5 only two apostrophe forms are recognized.** `:239` handles `'` and U+2019. U+02BC is not a
  negator: A2 `isnʼt frozen` → PASS. `NEG_WORDS` `:222-223` is a code-only list; the sentence
  says "negator" without enumerating it (`NEG_KEY_PARTS` `:224` does match `claims.md:39`).

## Residual risk / gaps
- The frozen fixtures exercise none of M1-M5 or L1-L5, so `C1=PASS` does not cover them.
  The sentence and claim are frozen; routing is the L1's call.
- No LSP semantic check was run: single file, no `lsp` device on this seat.
- I did not re-run the round-46 counter separately; its result comes via `R46_COUNTER=pass`.
- All probe evidence is synthetic one-bullet entries. No lane entry was found to trigger M1-M5.
