# R55W2CritTrends — attack on round-55 trend verdicts

Axes: **operability**, **depth**, **calibration**. Scope is the round-55 planned trend language at `29cfb12abd70f688b48c0d17f31e636f2d81104a`; this is not a re-judgment of round 56's frozen C1/C2 predicates.

## Counterexample and evidence

- **Expansion — survives, narrowly.** The closure's test is new ground, not volume: `git grep -c 是否检索灰色文献 dba605deb5cd5ed4874e0e3c39ba24737409cd80 -- corpus/knowledge` is absent at base (closure §2 reports exit 1), while the landed r40 entry contains it. Closure §2 records three new, document-bound S124–S126 rows and 19 checked spans (§4). This supports expansion on **coverage**; it does not by itself show breadth or adjudicate all 36 falsify items. The capability-row addition is not a separate new source/document and must not inflate expansion credit.

- **Quality — survives as narrow, not comprehensive.** Closure §2 reports all additions in the base→TIP whole-round diff with zero deleted lines; the supplied base→29cfb12 numstat likewise has no negative/deletion counts (all listed files add lines). Thus no evidence of a removed existing row, entry, or criterion in this interval. The closure independently checked 19/19 spans and 33/33 regression spans byte-identical (§2), and 8/11 C3 observations; the other three were receipt-backed, not re-run. The same closure explicitly records that the round-55 C1 counter's 9/9 mutants survived and its audit hook missed cwd/dir_fd-relative access (§2, §6). Therefore quality improved for the located-span/append-only correction work, but this must not be read as a robust gate/counter or complete verification claim. Later round-56 C1 work is not evidence that repairs this round-55 limitation.

- **Discernment — overclaimed as “improved”; safest verdict is “unprovable-but-better” (or unchanged under a binary evidence standard).** Closure §4 is a real external re-open: agreement on one admit, two rejects, and one quarantine verdict, with reasons and captures. But the closure also says the 36-item W2 falsify wave was never dispatched and W1 was unsettled at filing (§1 D1; §6), while the trend claim says those are conformance debt, not disagreement (§5). Absence of falsification is not positive validation of the untested decision set. The later-committed `w1-results.json` records results for 48 W1 seats (JSON lines 1–5); it does not retroactively make the report's earlier W2 non-dispatch or filing-time W1 settlement true. Evidence supports a limited spot-check, not a general discernment improvement.

## Smallest safe correction

Retain expansion and quality only with their measured scopes; change the trend's discernment label from **improved** to **unprovable-but-better** and state the one-admit/two-reject/one-quarantine scope plus the omitted W2 limitation. Do not alter round-55 predicates, targets, counters, controls, or frozen claims. No demonstrated axis harm: the observed diff is additions-only; no existing row/entry/criterion loss is evidenced.

## Commands / observed evidence

```text
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --numstat dba605deb5cd5ed4874e0e3c39ba24737409cd80 29cfb12abd70f688b48c0d17f31e636f2d81104a
```
Observed: every numstat row has additions and `0` deletions; `corpus/knowledge/grey-literature-and-chinese-search-record-r40.md` is `33 0`; `SCORECARD.md` is `18 0`; r36 and r37 entries are `9 0` and `8 0`. Closure source: `corpus/lessons/round-55-verifier-spotcheck.md` §§1, 2, 4–6 (especially lines 29–32, 43–48, 52–60, 63–81, 83–85, 110–122). Late results: `.ufo/waves/round-55/w1-results.json` lines 1–5.

VERDICT: Round-55 expansion survives narrowly; quality survives narrowly with major C1-counter caveat; discernment “improved” is not earned beyond the limited spot-check and should be “unprovable-but-better.”
