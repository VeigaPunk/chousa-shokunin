# Attack05 — held-out correct bullet probe, precision class #5 (C1 false-refusal)

seat: L1Chousa48.Attack05 (reviewer, leaf) · 2026-10-25 · item: construct 2 distinct
correctly-reasoned held-out Inference bullet examples for precision class #5 (varied scope,
negator distance, unlisted absence words, neighbouring-word binding) over the r47 fixture
spans; run current `tools/inference-ground.py` on scratch copies; state whether each correct
bullet is refused and why. Probe only — no fixture, counter or claim edit. No network, no
installs. Scratch `/tmp/chousa-r48-Attack05` removed at close.

## 1. Sources (committed only)

- Span files and manifests copied byte-identical from the committed r47 fixtures
  (`git hash-object` matches the index blobs): `spans/S901-1.txt` = `44a7de39…`,
  `spans/S902-1.txt` = `c172c627…`, `counts.json` = `d9e62285…`, `spans.tsv` =
  `07724671…`. S901 = `the release ships a frozen pool of pages; no revision is recorded per
  sentence`; S902 = `the archived copy is dated at build time; a placeholder value is not an
  archive link`. Scratch copies read by the tool from `/tmp/chousa-r48-Attack05/`.
- Tool: `tools/inference-ground.py` (worktree, sha256 `0e5a92b9…` == index blob 100755).

## 2. The two held-out correct bullets and their runs

Command: `python3 tools/inference-ground.py --entry <scratch>/<f> --spans <scratch>/spans.tsv
--counts <scratch>/counts.json`.

| # | bullet (verbatim) | token | result |
|---|---|---|---|
| B1 | Because `no revision is recorded` per sentence, revisions cannot be traced to the sentence they changed (`S901`). | `no revision is recorded` | `GROUND: PASS` exit 0 |
| B2 | A placeholder value is `not an archive link`, so a check that counts it as archived overstates coverage (`S902`). | `not an archive link` | `FINDING INF_POLARITY_FLIP bullet=1 token='not an archive link / archived'` exit 1 |
| B3 | Since the placeholder is `not an archive link`, the citation remains unverifiable whenever the archive is checked (`S902`). | `not an archive link` | `FINDING INF_POLARITY_FLIP bullet=1 token='not an archive link / archive'` exit 1 |

B2 and B3 are the two deliverable bullets (2 distinct refusals). Each is correctly reasoned:
B2 — the span records the citation cell's value is a placeholder, not an archive link, so a
coverage check that counts such a value as archived overstates true coverage; B3 — because the
placeholder is not an archive link, an archive check carried out on the citation can never
verify it.

## 3. Why each is refused (mechanism, tool `polarity_flips` P1, lines 317-348)

Both B2 and B3 reuse a scope-word stem of the quoted negated phrase in their own unquoted
words — `archived`/`archive` share the 5-letter stem `archi` with the content word `archive`
of `not an archive link` — and no negator stands in the 3-before/2-after window of that word
(B2: `counts it as … overstates coverage`; B3: `whenever the … is checked`). The later
negators `overstates`/`unverifiable` are unlisted absence words (not in `NEG_WORDS`,
`IMPLICIT_NEG` or `UN_NEG_RE`), so P1 reads the stem reuse as an affirmed flip. Refusal is
independent of the bullet being correct; B1 passes only because its stem reuse (`revisions`,
scope stem `revis` of `no revision is recorded`) happens to carry `cannot` 4 words earlier —
outside the window — so no P1 match fires. Controls on the same scratch spans confirm the
probe still fires on genuine flips and lets correct positives through: `junk-flip-asserted`
(genuine flip `revised`) exit 1; `positive-figure-negated` and `positive-affirmed` exit 0.

## 4. Findings

- Measured: the current tool refuses 2/2 correctly-reasoned bullets that restate a negated
  span phrase's scope stem via an unlisted absence word (B2 `archived`, B3 `archive`), each
  with finding `INF_POLARITY_FLIP`. Round-47 `LabC1FalsePos`'s measured false-refusal trade
  (9/10) reproduces here on fresh (non-r47) wording; the implicit-negator list
  (`IMPLICIT_NEG`, `UN_NEG_RE`) does not cover this class.
- The refusal is insensitive to negator distance: in B1 the negator `cannot` at distance 4 is
  outside the window and no flip is flagged (it passes); in B2/B3 absence is expressed by the
  unlisted `unverifiable`/`overstates` forms, invisible to the lexer, and the stem reuse is
  flagged. Distance and absence-word coverage jointly decide the verdict, not the inference.
- Scope shape is irrelevant to the verdict: B2 restates via derived adjective + counterfactual
  (`counts it as archived`), B3 via bare noun in a procedural check (`whenever the archive is
  checked`); both are refused identically.

Verdict: C1 false-refusal precision class #5 (unlisted absence words reusing a negated
phrase's stem, at any negator distance) still refuses correct inferences; probe evidence only,
no code/fixture/claim change recommended here.
