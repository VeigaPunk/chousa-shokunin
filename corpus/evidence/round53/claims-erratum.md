# Round 53 — claims erratum (post-freeze disclosures)

The frozen claims (`claims.md`, freeze `a6ff732c70011f11c9beb681d832cedc6e75f566`)
and both counters are unchanged. Every item below is outside the frozen rules
and is reported beside them; none changes a predicate, target, kill rule or
control.

- **E1 — C1 supplement (post-freeze, not the claim's rule).** W1
  `R53CritForgeC1` passed the frozen C1 counter `LEGS=8/8` with a 189-line
  forge (`controls/forge-c1.py`) that implements the held/twin/append map but
  cans REAL on the pinned package digest, rejects only the generator's four
  invalid-date shapes and prints the round-50 self-test strings without running
  it. `c1-supplement.py` adds CALENDAR (calendar-only invalid dates with a
  leap-day control), REAL_PERTURBED (the real package with fresh staged ids,
  entry names and registry maximum) and SELFTEST_RAN (one expected finding
  dropped must fail). The landed adopter scores `SUPPLEMENT_LEGS=3/3`, the forge
  `1/3`. The supplement is itself forgeable by a tool that reimplements the
  adopter; it only removes the three cheap shortcuts.
- **E2 — `--per-leg 0` is vacuous (named, not changed).** W1 `R53SentCounters`
  H1: the frozen counter accepts `--per-leg 0` or a negative value and prints
  `LEGS=8/8` with no generated package. The target runs use the default (3) and
  `--per-leg 10`; the after-receipt keeps the per-package lines so the case count
  is visible. QUALITY 96 binds the next counter.
- **E3 — the frozen sentence is narrower than the tool on a bare cadence.** The
  R53-C1 sentence says a recheck with "no leading calendar-valid date or `NNd`"
  is refused; the adopter also accepts a symbolic cadence (`quarterly`), as the
  CORPUS.md recheck column allows (W1 `R53SentCounters` H2). The counter never
  generates a cadence, so no leg measures the gap. The tool keeps the census
  rule.
- **E4 — `tools/inference-ground.py` gained a CJK polarity window after the
  freeze.** The C2 counter runs the lane's `tools/inference-ground.py`. Round 53
  lands the closure-routed CJK negator window (W1 `R53ExecCjkPolarity`;
  `cjk-polarity-check.py`: base 2/6, landed 6/6). C2 was measured with both
  tools: the round-52 tool (`git show 5b550133:tools/inference-ground.py` in a
  scratch root) and the landed one each give `INFERENCE_GROUNDED=3/3 C2=PASS`.
  The change only adds findings, so it cannot make a failing entry pass.
- **E5 — the `ENTRIES` minimum of two is not exercised and is partly
  unreachable (named, not changed).** W1 `R53ReviewC2Counter` F1: a refused entry
  whose exclusive document keeps a lane row leaves that document neither BOUND
  nor REFUSED, so `BOUND+REFUSED=5` fails. This round admits all three entries
  (`ENTRIES=3/3`), so the path is not used; the relaxation from round 52's 3/3
  bought nothing and is not a weakening that the measured result relies on.
  F2 (the registry splitter drops a row with an escaped `\|`) and F3 (a loose
  `refused-entry` matcher) are named limits; no lane row carries `\|` (census
  NF check) and no entry is refused.
- **E6 — in-round narrowing (outside the frozen counters).** The three entries
  were drafted by W1 seats and narrowed against W1 critics before landing (the
  Wia title to the two documents; the QCG draft-versus-issued comparison
  dropped; the staged JMLA and Cochrane sentences re-cut at line breaks); S190
  (the 2019 NMPA notice print) was refused as a document after the QCG entry
  stopped resting on it, so the adopter's map is S117–S120 rather than the
  planned S117–S121 in the wave context.
