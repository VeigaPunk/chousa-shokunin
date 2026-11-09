# LOG.md entry draft — chousa-shokunin, round 100

Append after the round-99 block in `LOG.md`. Existing style: a `## Round NN — YYYY-MM-DD` heading, then
bullet paragraphs (`-` leading) for motivating evidence, amendments, routed items, census and mistakes.

---

## Round 100 — 2026-11-09

Lane `chousa`, round 100 (attempt 1, L1 `ChousaR100`). Base `929c784c`; P `96835234`; R `6f837487` (pre-freeze
controls); F `6d4e8487` (claims + plan), recorded in `plans/round-100.md` `## Freeze` by carrier `7d2d3abe`; F2
(A1-A4, B1-B5) wave-forced re-freeze, no predicate, counter code, kill rule or target changed. Two claims:
C1 operability (the gate's rev-form CHALLENGE by capture identity) and C2 freshness (the round-99 entry's
`recheck: on-release` fired and was answered by a new entry sourced on the 2025 update). Approval table for the
round's GETs `corpus/evidence/round100/egress-approval.md`, written before the first GET.

- Motivating evidence C1: round 99 keyed the rev-form CHALLENGE guard to a path's *spelling*
  (`CAP_RE.fullmatch(kv["path"])`) while `git cat-file` resolves `./corpus/captures/<key>.txt`, `<key>.raw` and a
  byte copy at another path to the same challenge blob; the round-99 tool printed `OK` on each
  (`.ufo/waves/round-99/w1/R99SentinelC1.md` F-1). After: `tools/gate-records.py` resolves `rev:path` to an object
  id and judges the blob when that id is a `corpus/captures/` entry of the record's rev; battery
  `NEG=7/7 MARK=11/11 BOUND=3/3 NORM=2/2 POS=4/4 REV=11/11 REVPOS=3/3 PROD=6/6 HARM_SAME=27/27
  BASE_REV_ADMITTED=8/11 ORACLES_REJECTED=12/12`, `CHALLENGE_CONTROLS_R100=PASS`; base tool `REV=3/11 PROD=4/6`,
  FAIL exit 1 (`corpus/evidence/round100/before/c1-base.txt`, `before/c1-candidate.txt`).
- Motivating evidence C2: round 99's entry carried `recheck: on-release`; the authors' 2025 update (Baethge &
  Jergas, Res Integr Peer Rev 2025, pmid 40696441) was opened this round through its Europe PMC core record
  (S238, tier B). After: `corpus/knowledge/quotation-error-update-r100.md` (16 located quotes, 8 decision rows) and a
  `## Update` section on `corpus/knowledge/quotation-error-rates-r99.md`; `records=17 ok=17 fail=0`,
  `ENTRY_CONTROLS_R100=PASS` (`corpus/evidence/round100/before/c2-candidate.txt`).
- Gate: three rows added — S237 (Europe PMC full text PMC4627914, rejected, http 500 ×3), S238 (Europe PMC core
  record of PMID 40696441, tier B, mined), S239 (Europe PMC full text PMC12285159, rejected, http 500 ×3); S236
  `used-by` extended in place to the new entry. No web search this round: every URL was named by committed round-99
  artifacts. Census exit 0 before (`corpus/evidence/round100/census-start.txt`); one new W04 (S237/S235 same URL across
  scopes, both rejected) after — **the after-census receipt is not yet committed and must land with this round.**
- Corrections at F2 (claims.md `## Amendments`): A1 "that rev's tree" (a HEAD-tree stand-in prints the frozen PASS
  line; `R100CriticClaims` F-1, `R100ExecC1Repro` finding 1, `R100MutantsC1` survivor `n-cache-repoonly`); A2 the
  `.raw` sibling rule (`R100ConnectorSiblings` F1); A3 the battery's PASS is weaker than the frozen predicate line
  (`R100MutantsC1` b1, b4-b7, b9); A4 the "not judged" quadrant, no narrowing (`R100CriticClaims` F-2); B1 row 2's
  trend verdict moved to the Lane cell and row 4's "were not" restored to the warrant's "were not statistically
  significantly associated" (`R100ReviewerC2`); B2 the GET count ("both/two" → three, from `refetch.tsv`);
  B3 U9/U11 are located after the tool's normalization (the record prints U+2009 thin spaces; `R100ExecC2Repro` F-1);
  B4 "fired and was answered" is not what FRESH checks (`R100ConnectorSiblings` F2, `R100CriticClaims` F-6). All C2
  tallies unchanged at F2.
- New in round 100 (this seat's findings, receipts in `.ufo/waves/round-100/w1/R100ScribeLesson-*.txt`):
  S237 — a row the round opened — carries **no** `GATE-RECORD` line anywhere in the frozen tree, while S238 has 14
  and S239 has 1; QUALITY 173 (`corpus/QUALITY.md:1110`) asks for a record per opened row, the round-99 `url/unreach`
  form fits S237 exactly (it verifies `OK`), and every C2 counter reads only the entry file, so no counter noticed
  (`R100ScribeLesson-receipt-record-coverage.txt`, exit 1). The registry's own anchor cells carried shell-clock
  times rather than the fetch log's (`corpus/evidence/round100/after-f2/anchor-times.txt`).
- Routed to round 101: a two-commit fixture with cross-rev legs and a two-rev single-file record, so the "that rev's
  tree" clause is enforced by a leg rather than by seat probes only (A1, named limit (f)); a counter that walks the
  rows added since the base and counts their `GATE-RECORD` lines, so an opened row without a record fails instead of
  passing unnoticed; a `## Update` section that carries one checkable warrant numeral, so "fired" is not a presence
  check (B4); the fleet tier question for index-record abstracts (tameshi A vs chousa B) stays open.
- Census: start exit 0, end exit 0 (one new W04, S237/S235 same URL across scopes). QUALITY 231 added (a guard on a
  cited file is keyed to what the resolver returns, not to how the path is spelled); README and lesson updated; mistakes
  mined: 5 (`corpus/lessons/round-100.md`).
