# ReviewKnowledge — admission review of `corpus/knowledge/quote-reopen-r29.md` (round 29, wave 2)

Seat: ChousaR29.ReviewKnowledge, reviewer, read-only on the lane. Date: 2026-10-22/23.
Object: working-tree `corpus/knowledge/quote-reopen-r29.md` (uncommitted `M` on top of
`b18b3ec`; reviewed at snapshot `#9EC5`, which already carries a sibling's UTC/S047
amendment to `verified-at` — the amendment landed mid-review and was re-verified).

**Verdict: FIX-NEEDED** — two real defects (one overclaim clause, one imprecise
anchor title) and one conditional dangling pointer; every other factual statement
checked held against the landed code, the live sources and the committed receipts.

## Commands run (all bounded, all exited)

- `timeout 590 python3 corpus/evidence/round29/c1-count.py -- python3 tools/quote-reopen.py verify`
  from the lane root → `QUOTE_REOPEN_MATCH=130/130`, `REcheck_EXIT=0`, wall 6.72 s
  (seed 15240140703577499734). The assigned 900 s wrapper was lowered to 590 s to
  respect the lane's ≤600 s command bound. `PYTHONDONTWRITEBYTECODE=1` was set so the
  run writes nothing into the lane.
- `timeout 60 python3 corpus/evidence/round29/prose-check.py corpus/knowledge/quote-reopen-r29.md`
  → `TOTAL hits=0`, `PROSE_EXIT=0` (run again on the amended file: same result).
- `curl -m 30 https://wicg.github.io/scroll-to-text-fragment/` → 368,361 B;
  `grep -c '</head>'` = **0**, `<head` = 1, `<body` = 1 (S047 Limit confirmed).
- Counter reference extractor on that live WICG body (scratch
  `/fast/scratch/hyaku/chousa-r29/w2/ReviewKnowledge/`):
  `m._Text` + `norm` → `extracted_len=0`, `found(...)=False` — the S047 quote
  *cannot* have been re-located with the reference extractor.
- `curl https://www.w3.org/TR/annotation-model/` → §4.2.4 heading "Text Quote
  Selector" and the doc's quoted sentence verbatim ("...some of the text
  immediately before (a prefix) and after (a suffix) it to distinguish between
  multiple copies of the same sequence of characters.").
- WICG page: "Context terms are used to disambiguate the target text fragment."
  verbatim; "case-insensitive search also ignoring accents, umlauts" verbatim;
  §3.6.2 "Word Boundaries" present.
- UAX #15 page: §1.2 contains "Normalization Forms KC and KD must not be blindly
  applied to arbitrary text." verbatim; circled-digit→digit example present in
  §1.1 Figure 2.
- Python docs page: the S049 `convert_charrefs` sentence verbatim, including
  "(except the ones in elements like `script` and `style`)".
- Receipts (python json): `CtlRawGrep/receipt-v2.json` match=100, `receipt-v2-seed2.json`
  =99, `receipt-v3.json` =98, `receipt-v3-run2.json` =93 → "93 to 100 of 130" ✓.
  `CtlCasefoldNoBoundary/receipt-v3{,-run2}.json` =126/130 both, only
  `absent-truncated-token` 0/4 → "lost exactly the 4 truncated-token items" ✓.
- Fixture: `labels.tsv` VERBATIM classes = 9 inline-markup + 3 plain + 2
  typographic = 14 → "9 of 14 true quotes cross inline markup" ✓.
- `git status`: doc is `M`; `SCORECARD.md` contains no "Round 29" heading or
  mention (tail = round-28 errata).
- Mutant claims: `MutOrder.md`, `MutSkipScript.md`, `MutCasefold.md` all report
  mutant `130/130` survivors with the exact code paths the doc names; `items.tsv`
  contains no case-only edit, no hidden-text-only item and no over-long item on an
  unreachable source → the new Limits bullet is accurate.
- S021/S022 = the two `pubmed.ncbi.nlm.nih.gov` rows; 203 challenge recorded in
  `ScoutRegistryFetch/registry-fetch.tsv` and `ScoutFreshnessH.md`. S014 = 403 in
  `registry-fetch.tsv`. S011/S037 are PDF rows → UNREACHABLE claims all confirmed.
- Gate comparison: `RevengerGateSpan.md` documents the conditional `-`/`'` joiner
  rule (`tok_left_ok`/`tok_right_ok`) and the measured `hyphen-cut-before` probe;
  the doc's `cross-` example is correct under the reading "a quote beginning right
  after `cross-`" (gate left-edge joiner fails → ABSENT; tool `-` is a boundary →
  VERBATIM), matching the probe's `apos-cut-head` direction.
- Tool code cross-check (`tools/quote-reopen.py`): verdict order :386-408,
  TOO_LONG before fetch :393-398, first-URL `URL_RE.search` + `rstrip(".,;)")`
  :145-152, never fetches item-supplied URLs :387-388, `SKIP`/`BLOCK` sets
  :57-62,:83-101, `norm` NFKC+QMAP :64-72, `isalnum` boundary :123,
  exit codes :416,:428-436, fetch bounds GET/http(s)/30 s/8 MiB :48-54,:163-205,
  :259-325. Every doc statement about the tool is true of the landed code.

## Findings

1. **(moderate) `verified-at` still overclaims S047.** The clause "the four
   source passages were opened and the quotes below re-located with the reference
   extractor of `corpus/evidence/round29/c1-count.py`" is false for S047: the
   reference extractor returns zero characters on that page (measured). The same
   sentence's own qualifier ("The S047 quote was located in the body text only")
   concedes a different method, so the header contradicts itself. Fix: "three of
   the four quotes re-located with the reference extractor; the S047 quote
   located in the body text only."
2. **(minor) S047 anchor title.** `source:` cites `§3.6.1 "Find a String in
   Range"`; the live spec titles §3.6.1 "Finding Ranges in a Document" (respec
   `data-level="3.6.1" id="finding-ranges-in-a-document"`). "find a string in
   range" is a defined term *inside* §3.6.1, not its title. Registry row S047
   carries the same loose anchor, so the doc reproduces it; quoting it as a
   section title is imprecise. Fix: `§3.6.1 "Finding Ranges in a Document" (the
   "find a string in range" algorithm)`.
3. **(conditional) Dangling pointer "SCORECARD.md Round 29".** Cited twice
   (`verified-at` line 4, "Measured result" line 117); `SCORECARD.md` ends at
   the round-28 errata with no Round-29 section. `lessons/round-29.md:73` makes
   the same forward reference. Resolves if the Round-29 scorecard section lands
   in the same integration; a dangling cited anchor if this entry lands first.
4. **(nit) `recheck:` note.** "re-open S046 to S049 on a new release" does not
   match the rows' own cadences (S046–S048 `365d`, S049 `on-release`); the `180d`
   field itself is a permitted cadence. Informational only.
5. **(nit) `CtlCasefoldNoBoundary` gloss.** "which drops it" omits that the
   control also casefolds; the observed loss is nonetheless exactly the four
   truncated-token items, so the attribution to the boundary rule is correct.
   The control's name makes the second mutation discoverable — elliptical, not
   false.
6. **(residual, criterion 9 adjacent)** The restated control totals (93–100/130,
   126/130) carry no owning-file+revision or re-derive command. Criterion 9 is
   outside the assigned set and the numbers are owned by `controls/` reports;
   noted, not blocking.

## Criteria sweep (assigned: 6–8, 10, 13, 17–25)

- **6 header trio**: `source:`/`verified-at:`/`recheck:` present; S046–S049 are
  `mined`, tier A, `used-by` names this entry (verified all four cells);
  `verified-at` is ISO date + what was checked (see finding 1); `recheck` is a
  valid cadence plus command. PASS modulo finding 1.
- **7 scoped tier**: every external claim rests on a tier-A row within its
  `scope` cell. PASS.
- **8 support states**: "location only … does not judge whether the quote
  supports a claim or whether the source is true"; `VERBATIM` qualified as
  "equal after these folds". PASS.
- **10 no unfilled template**: `grep -nE '\$\{[A-Z_]+\}|\bTODO\b|\bTBD\b|LANE_HASH'`
  gives 0 hits; `<items.tsv>` is the frozen contract's own usage notation, not an
  unfilled slot. PASS.
- **13 runnable recheck**: states cwd ("from the lane root"), no `--root` to
  misplace; command run once, exit 0, 130/130. PASS.
- **17–22**: independent failing controls exist and precede data (all v2/v3
  control receipts committed, best 126/130 < 130; `before-do-nothing-v3.json`
  0/130). PASS as far as this entry is concerned.
- **23**: `prose-check.py` exit 0 (0 glued tokens, 0 custody hits) on the amended
  file. PASS.
- **24**: controls scored before data; v1 (82/82 label replay) and v2 (130/130
  seed replay) voided honestly in `claims.md`. PASS.
- **25**: this entry is criterion 25's own exemplar; the S047 ABSENT is named as
  a tool limit in Limits, not relabelled. PASS.

## Limits of this review

- The file changed mid-review (uncommitted sibling amendment); findings apply to
  snapshot `#9EC5` (current working tree). A later edit could add or remove
  defects.
- Finding 3 is conditional on the round-29 scorecard landing order.
- `CORPUS.md` is cited bare; it lives at the fleet root
  (`/home/vgpnk/Projects/shokunin/CORPUS.md`, SOURCES rule 1 and the ≤25-word
  quote rule verified there), not in the lane — same convention as `SKILL.md`.
- "Registry URLs only" mirrors the frozen contract; redirect hops are checked
  per-hop (scheme/userinfo/global address) but can leave the registered host —
  contract-faithful, recorded for completeness.
- No tools installed or updated; nothing to record under the tooling directive.
- One scratch artifact only: `/fast/scratch/hyaku/chousa-r29/w2/ReviewKnowledge/wicg.html`.
- Network use: GET only, only to registry-column URLs (wicg.github.io,
  www.w3.org, unicode.org, docs.python.org). No processes left running.

Report: .ufo/waves/round-29/falsify/ReviewKnowledge.md
