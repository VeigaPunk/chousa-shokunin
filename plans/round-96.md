# Round 96 plan — chousa (L1 `ChousaR96`, attempt 1)

Base `bbf64970b6c73ca64bcc5f6de2f33b0550459813` (round-95 landing `07e0e332` + the round-95 non-author spot-check
and its second-pass section). Round-95 closure: admitted (operability improved, depth improved). The lane is not
under a fresh-start rule this round (r95 admitted); the binding §9 rules still apply: every claim beats a committed
do-nothing control and a forgery battery executed before the freeze, through the public CLI.

## Why these claims

- The SCORECARD `## Planned — round 96` row names (1) operability: run the search-rerun capability on a real
  search the lane itself performs and file the record; (2) depth: PRISMA-S items 14 (peer review) and 16
  (deduplication) are read but not held. The round-95 spot-check routes D1: `search-rerun verify` is registered
  as kind `tool` and has no self-invocation mode.
- C1 (operability, the lowest axis) takes D1: a `--selftest` that scores the same decision code `verify` runs, a
  battery that shows it can fail (mutants) and that a stand-in cannot pass it, and a gate registration.
- C2 (depth) takes planned item 2, and planned item 1 rides inside it: the entry's own gap-establishing searches
  are run with GNU grep at the base revision and filed as a `## Searches` record that `verify` re-runs (the
  first record of real round work rather than a fixture).

## Pre-freeze fixes (before any seat scored)

- **P0** — first draft of the C1 refactor (moving the per-row judgement into `evaluate()`) replaced the line
  `at_rev = run_at_rev(root, r, cache)`, which is the mutation site of the round-95 battery's `rev-blind`
  oracle: `rerun-controls-r95.py` printed `SETUP oracle rev-blind mutation did not apply` and `mutants-r95.py`
  printed `MUTANTS_KILLED=0/10` (every mutant's battery setup-failed). The line was restored verbatim inside
  `verify`'s `at_rev_of` closure; the round-95 instruments are a regression leg of the C1 battery (K5).
- **P0b** — the first self-test run printed `FAIL cases=23/32`: the judgement helper read the codes field at the
  wrong index of the `SEARCH_RERUN` line (6, the `at_tree=` field, not 7). Fixed in the helper; no case changed.
- **P1** — first full battery run: `m16-set-dedup` SURVIVED (j05 listed a duplicate in place of a second real
  path, so a set comparison also refused it) and `m34-absolute-allowed` SURVIVED. j05 now lists both real paths
  plus a duplicate; m34 is an equivalent mutant (an absolute glob's first segment is empty, refused by the
  empty-segment check) and was removed, not counted. (m07 had already been strengthened to `a/b?/c/d.txt` while
  the battery was written, before run 1, so the static-directory `break` mutant m32 has a witness.) Receipt:
  `corpus/evidence/round96/prefreeze/c1-run1-transcript.txt`.
- **P2** — the entry's `## Searches` heading first carried the "As run" prose before its table; `verify` refused
  it (`SEARCH_RERUN_ERROR TABLE`). The prose moved to `## As run`.
- **P3** — S222's scope cell excludes search quality and its anchor names items 8, 9, 12, 13 and 15 only; the
  entry's items 14/16 quotes could not honestly cite it. The same PDF was re-opened under a second, separately
  scoped row `S224` (identical raw and text digests) instead of rewriting S222 (CORPUS rule 2).

## Routed defects from the round-95 spot-check

- D1 → C1 (gate registration + self-test).
- D2 → `LOG.md` correction (r95 lesson "nine located quotes" → 13).
- D3 → `LOG.md` correction (the r94 counters were not re-run in round 95; that sentence had no receipt).
- D4 → the Europe PMC JATS route answered http 500 again this round (attempt 2, `refetch.tsv`); the external
  confirmation of "10:39" recorded by the round-95 closure is cited in the lesson, the row is unchanged.
- D5 → `corpus/README.md` correction line (the claimed numbers live in `after-f2/`).

## Wave

One v1 wave, 12 seats, attack share ≥25 %. L1 holds the canonical planner seat.
