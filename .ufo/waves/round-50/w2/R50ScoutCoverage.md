# R50ScoutCoverage — coverage-map ground check (round-50 wave-2)

Seat: R50ScoutCoverage (UFO-FSD scout, leaf). Lane: `chousa-shokunin`.
Frozen claims at `6a068f2`; wave-1 L1 at `74794db`; HEAD `c5b8dca`; base check
`3c51da77b3696ed884c943548ec4b4006e3ca528`. Scope: `corpus/README.md` coverage
map + `## Frontier` mapping for the C2 theme (CNKI 引文核对 feature: comparison
source, three result states, which manuals document it; the CAS institute's paid
引证检索 service and its co-author self-citation standard; the "no matching
method documented" negative). No scratch was needed; no installs.

## 1. Base grep: does 3c51da7 hold 引文核对/引证检索?

Command (observed output verbatim):

    $ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -n -E '引文核对|引证检索' 3c51da77b3696ed884c943548ec4b4006e3ca528 -- .
    3c51da7:.ufo/waves/round-49/assimilation/adopt-final/corpus/knowledge/citation-count-semantics-r37.md:77:  the 诚信档案系统使用手册 (which contains CNKI's 引文核对 citation-checking
    3c51da7:.ufo/waves/round-49/assimilation/adopt/corpus/knowledge/citation-count-semantics-r37.md:77:  the 诚信档案系统使用手册 (which contains CNKI's 引文核对 citation-checking
    3c51da7:.ufo/waves/round-49/assimilation/refused-know/corpus/knowledge/citation-count-semantics-r37.md:77:  the 诚信档案系统使用手册 (which contains CNKI's 引文核对 citation-checking
    3c51da7:.ufo/waves/round-49/w1/DraftGateRefusal.md:62:| `cnki-matching-modes-r42.md` (S149) | **REJECT for this round** | ... distinct from the 引文核对 auxiliary feature (...)
    3c51da7:corpus/lessons/round-49-verifier-spotcheck.md:80:| `cnki-matching-modes-r42.md` · reject this round | ... the three modes govern the search platform "not the 引文核对 feature"; ...

Exit 0. **All five matches are 引文核对; 引证检索 has zero matches anywhere at base.**
Four of five sit in unadopted wave artifacts (`.ufo/waves/round-49/` staging and
draft-refusal copies), not in adopted corpus surfaces. The single corpus-proper
occurrence is the integrator's spot-check lesson, which *names* the feature only
to reject a distinct entry — not coverage of the theme.

Scoped to the canonical surfaces where such a theme would live:

    $ git grep -n -E '引文核对|引证检索' 3c51da7 -- corpus/knowledge corpus/SOURCES.md   # exit 1, no output
    $ git grep -n -E '引文核对|引证检索' 3c51da7 -- corpus/QUALITY.md                      # exit 1, no output
    $ git grep -n -E '引文核对|引证检索' 3c51da7 -- corpus/lessons                        # exit 0: only :80 above

The base's adopted r49 note itself dropped the phrase the staged copy carried:

    $ git show 3c51da7:corpus/knowledge/citation-count-semantics-r37.md | grep -E '引文核对|引证检索'   # exit 1, no output

Base `SOURCES.md` registry ends at S103 (`git show 3c51da7:corpus/SOURCES.md |
grep '^ *| *S10'` → S100 at :110, S101 :111, S102 :112, S103 :113; no
S104–S106). Base `corpus/README.md` (1075 lines) contains neither term.

## 2. Coverage map: what the theme touches

Held already at base (adjacent rows, same citation/CNKI domain; adjacent holdings):

- `corpus/README.md:1071` — row `knowledge/aggregator-vs-source-r36.md`
  (round-49, adopted by document): derived reference lists — CiNii matched-items
  only (S096), J-STAGE link-creation ladder (S097/S098). Touches the "what the
  check compares against" family (list derivation vs checking source) but holds
  nothing about 引文核对 or 引证检索.
- `corpus/README.md:1072` — row `knowledge/citation-count-semantics-r37.md`
  (round-49): what a CNKI count is a count of; co-author self-citation rule
  (S100), 文献标志码/GB-T-7714 split (S101), citation/download columns (S102),
  AI trace panel (S103). Touches the co-author self-citation *rule* kind (ISTIC's
  fee-table standard is a different service's statement) and the CNKI domain;
  the base spot-check lesson (`corpus/lessons/round-49-verifier-spotcheck.md:80`)
  itself classifies 引文核对 as "another feature from the citation-count theme".
- Base README rows for the round-49 package (`:1071-1075`) exist and are unchanged
  at HEAD (`:1071-1075`).

New ground (the C2 adoption; none of these existed at base):

- `corpus/README.md:1076` — `knowledge/cnki-citation-check-r40.md` (comparison
  source = 中国知网's own literature resources; result-list columns; three states
  没找到/橙色/绿色; matching method unstated).
- `corpus/README.md:1077` — `knowledge/citation-matching-semantics-r41.md`
  (匹配 0 in 38174 characters; 仅去除第一作者本人文献 is a folder option in both
  manuals, not linked to 引文核对; "which manual documents the feature is a
  product fact").
- `corpus/README.md:1078` — `knowledge/istic-citation-verification-r39.md`
  (paid 引证检索: five indexes, bibliography, fee table naming a co-author
  self-citation standard, archived report, reuse concession, no index snapshot).
- `corpus/SOURCES.md:114-116` (HEAD) — new registry rows S104 (引证检索 page),
  S105 (CNKI 管理员 manual PDF, 6.1 引文核对), S106 (CNKI 子账号 manual PDF, no
  引文核对 section — the negative). At base the registry ended at S103
  (`:110-113`).
- `corpus/README.md:1079-1081` — round-50 lesson / evidence / selftest-fixture
  rows (the round's artifacts).

Frontier status: no named frontier item is advanced. The only relevant frontier
language is the standing boundary — `corpus/README.md:834-835` ("Semantic and
external-source verification remain out of scope by design") and the round-27
disposition carry `:907-908` ("source truth ... remain outside these controls").
The theme adds *held source content* (expansion credit within the citation-count
theme), not a gate capability or a frontier move; the open frontier items
(receipt identity, non-author spot-check, frozen-replay conformance, quote-reopen
edges, L0 fetch-scope) are untouched by it.

## 3. Calibration

- The literal base grep is NOT empty (exit 0, five lines, all 引文核对). "Base
  holds no 引文核对/引证检索" holds for the canonical adopted surfaces (knowledge
  notes, SOURCES registry, QUALITY) and for 引证检索 everywhere; the four wave
  artifacts and one spot-check lesson line are the only literal occurrences, and
  the lesson line reinforces the theme's distinctness rather than holding it.
- At HEAD the three adopted notes exist and carry the terms: `cnki-citation-check-r40.md`
  30 lines (引文核对 6), `citation-matching-semantics-r41.md` 31 lines (引文核对 8),
  `istic-citation-verification-r39.md` 57 lines (引文核对 2, 引证检索 2).

VERDICT: attacked the coverage-map ground claim — base 3c51da7 holds no 引文核对/引证检索 in its adopted knowledge/registry/QUALITY surfaces (0 in 引证检索; only 5 literal 引文核对 lines, all unadopted wave artifacts or the r49 spot-check lesson naming the feature as distinct), the theme is new ground fully conveyed by coverage rows README:1076-1078 + registry S104-S106, adjacent to held r49 rows README:1071-1072, and advances no frontier item — survived.
