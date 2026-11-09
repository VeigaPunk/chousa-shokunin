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

## Amendments after the freeze (wave-forced; every one cites the seat artifact that forces it)

The claims are judged at F2 on the amended sentences and predicates below; the F text in
`.ufo/waves/round-96/claims.md` stays as the F record.

- **A1 (C1, `R96CriticClaims` §Aa).** "scored by the same `evaluate` function `verify` runs" is not enforced by
  `--selftest`: a shim whose `verify` discards `evaluate`'s verdict still prints `PASS cases=32/32` and passes every
  non-regression leg; only the REGRESSION leg (`rerun-controls-r95.py`, `FORGERY_REFUSED=0/10`) catches it. Narrowed:
  the judgement cases *call* `evaluate`, the function `verify` also calls (read at source lines, not checked by the
  self-test); a `verify` that stops using its verdict is caught by the battery's REGRESSION leg, not by
  `--selftest`.
- **A2 (C1, `R96CriticClaims` §Ab).** A source-blind self-test that text-matches the 23 mutated sites scores
  `MUTANTS_KILLED=23/23` and is blind to a novel defect the real self-test catches (`p03-header`). Narrowed: the
  mutant leg shows the self-test fails at the 23 named sites, not that it detects defects elsewhere.
- **A3 (C1, `R96CriticClaims` §Ac).** Predicate 3's grep counts the row, not its kind cell. Narrowed: the kind
  cell reading `gate` is checked by reading (`R96ExecC1Repro`, `R96ConnectorSiblings` F1), not by the grep.
- **A4 (C1, `R96CriticClaims` §Ad).** K4 ("writes a file, runs git or opens a socket") is wider than NO_WRITE,
  which sees only an empty cwd/HOME and `git status --porcelain`. Narrowed: K4 is judged on NO_WRITE's scope; the
  syscall-level observation is a seat measurement (`R96ExecC1Repro`, `R96SentinelC1`), not a battery leg.
- **A5 (tool docstring, `R96CriticClaims` §H1).** "14 parse cases (13 setup refusals and the `\|` alternation)"
  overcounts: 12 refusals, 1 positive parse, 1 alternation. Docstring corrected; no case changed.
- **B1 (C2 row 3, `R96ReviewerC2` row 3, `R96ExecWrap` F3).** The Do cell said "under PRESS 2015" for a sentence
  the abstract attributes to "Survey respondents and forum participants recommended". Row rewritten with that
  agent; quote `L31` added. The Never's "review each database's translation by default" (not warranted by the
  row's quotes) dropped.
- **B2 (C2 row 5, `R96ReviewerC2` row 5, `R96CriticClaims` §Ee).** The Never ("claim a reviewed strategy is complete
  or has high recall") does not follow from L3, and the Lane's "several studies" is not in L30. Never now says the
  sources state none; the guard moves to the Lane column, and `L32` ("Results: Several studies showed") is added.
- **B3 (C2 row 1, `R96ConnectorSiblings` F5).** The Lane said a chousa record names the reviewer; the 8-column
  `## Searches` schema has no such field. Rewritten: the reviewer is named in `## As run` prose, and this entry's
  own searches were not peer reviewed.
- **B4 (C2 text forms, `R96ExecWrap` F2/F4, `R96ConnectorSiblings` F3, `R96CriticClaims` §Ec).** "Consecutive
  fragments … read from the text form's line order" was false for L24-L25 (page break, running header, column
  switch) and L17-L18 (one skipped line). Groups are now described from the reading-order text form, with the two
  layout exceptions named; the claim's named limit (d) narrows the same way. Each quote stays a substring of one
  capture line (30/30 measured by `R96ConnectorSiblings`; K3 does not fire).
- **B5 (C2 named limit, `R96ExecWrap` F2).** The Q6 miss is a page break with a running header, not a wrap
  between two column lines; the entry's note is corrected.
- **B6 (C2 sentence, `R96CriticClaims` §Db, §Ed, §Dd).** "warranted" narrows to "cite located quotes and share a
  content word with them (a lexical floor; the faithfulness of each row is the reviewer item, repaired at B1-B3)";
  "equals the quoted records one-to-one" narrows to "as a multiset of quote strings (the source column is not
  compared)"; S224 is a re-scoping of the S222 bytes, S223 the only new bytes.
- **Counts.** After B1-B2 the entry holds 32 located quotes and 33 GATE-RECORD lines; `entry-controls-r96.py`
  `N_RECORDS` 31 → 33 (the constant only; no leg changed).

### Amendments recorded after F2 (wording only; no tool, battery or entry byte changed — judged on the F2 instruments)

- **A6 (C1, `R96SentinelC1` F2).** The NO_WRITE leg cannot see a lane write: its `before` snapshot is taken after
  the POSITIVE leg has already run the self-test in the lane (a selftest that writes `tools/lane-side-effect.txt`
  scores `NO_WRITE=1/1`), and `git status --porcelain` prints paths, not bytes (a selftest that appends to an
  already-modified tracked file also scores 1/1). It does refuse a write into the empty cwd (`W1` → `NO_WRITE=0/1`).
  Narrowed: NO_WRITE shows the self-test writes nothing into an empty cwd/HOME; that the shipped self-test writes
  nothing into the lane, runs no git and opens no socket is a seat observation (`strace`, `R96SentinelC1`,
  `R96ExecC1Repro`), not a battery result. K4 (A4) narrows the same way.
- **A7 (C1, `R96SentinelC1` F1, F7).** The matching case `m08-env-scrub` asserts the `GIT_DIR` scrub and the
  lazy-fetch guard only; dropping `GIT_NO_REPLACE_OBJECTS` (a false CLEAN under a repo-local replace ref) or
  narrowing the scrub to `GIT_DIR` alone passes the self-test and both batteries. Narrowed: "caller `GIT_*` scrub"
  reads "the `GIT_DIR` scrub and the lazy-fetch guard"; the replace-ref and full-scrub guards are routed to round 97.
- **A8 (battery docstring, `R96SentinelC1` F4, F6).** `selftest-controls-r96.py` says "Read-only on the lane" and
  "removed at exit": `git status` refreshes the lane's `.git/index` stat cache (no content change), and a SIGKILL or
  SIGTERM mid-run leaves 48 files under `--work`. Recorded as corrections in `LOG.md`; the battery bytes stay as
  frozen.
- **B7 (C2 entry text, `R96ScoutSources` §3) — forces re-freeze F3 (entry text only).** The F2 entry said every
  fragment group reads as one sentence in the reading-order form; for `L31 with L24-L25` the running header stands
  between L24 and L25 there too, and the "30/30 measured" line under-counted the 32 quotes. The paragraph now names
  the exception and cites `R96ScoutSources`' 32/32 measurement. C2 named limit (d) narrows the same way. No row,
  quote or Gate record changed; the C2 receipts are re-run at F3. (The two missing receipts the seat names —
  `census-end.txt` and `after-f2/lesson-gate.txt` — are landing receipts, written with the landing commit.)
