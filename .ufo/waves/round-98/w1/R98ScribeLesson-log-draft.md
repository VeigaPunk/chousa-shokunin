# R98ScribeLesson — draft LOG.md entry, round 98 (scribe; L1 `ChousaR98` owns LOG.md, not edited here)

## Round 98 — 2026-11-09

Lane `chousa`, round 98 (attempt 1, L1 `ChousaR98`). Base `98b8177c`; freeze F `aac82684` (committed author date
`23:42:55 -03:00`, committer `00:02:37 -03:00`; the tree attacked is F). Claims `.ufo/waves/round-98/claims.md` /
`claims.json`: C1 operability (`tools/search-rerun.py --selftest`: guard canary `g00`, cases `r17`-`r34`, scored by
`corpus/evidence/round98/selftest-controls-r98.py` against the 37 mutants of `R97MutantsC1`) and C2 depth
(`corpus/knowledge/press-2015-statement-questions-r98.md` on S231, the statement's abstract through Europe PMC's
index record). Approval table `corpus/evidence/round98/egress-approval.md`. Plan `plans/round-98.md` (pre-freeze fix
P0: a new case's text contained a scored mutant's site, `g06-refusal-detail SETUP applies 3 times`, fixed by binding
`code = exc.code` first).

- Scribe re-run at F (`R98ScribeLesson`, scratch clone, not the lane): the frozen battery printed
  `POSITIVE=1/1 KILL_REQUIRED=35/35 DO_NOTHING_REFUSED=1/1 PRIOR_R97_KILLED=34/34 R96_MUTANTS_KILLED=23/23
  EQUIVALENT_SURVIVED=3/3 ORACLES_REJECTED=5/5 NO_WRITE=1/1 REGRESSION_R95=2/2 EXTERNAL_R97_KILLED=35/37
  BASE_KILLED=12/37 CASES=67`, `SELFTEST_CONTROLS_R98=PASS`, exit 0, in 688 s
  (`.ufo/waves/round-98/w1/R98ScribeLesson-battery-F.txt:146-147`). The g01-g05 guard mutants die by
  `failed=g00-guard-canary` (`:2-6`). The battery file's sha256 equals the one in `before/c1-base.txt`.
- Mistake mined: one (`corpus/lessons/round-98.md`, `## Mistakes`): a guard instrumented only on its raise path;
  the verdict path (count, summary, exit) was observed by nothing in round 97. Fixed by `g00` and the battery's
  g01-g05 requirement; residual: `selftest()`'s own exit path (`tools/search-rerun.py:723`) is not observed. Probe
  `.ufo/waves/round-98/w1/R98ScribeLesson-exit-probe.txt` (one failing case: F returns 1, the mutant returns 0).
- Correction candidate (approval table, `corpus/evidence/round98/egress-approval.md` first paragraph): "It was
  written before any round-98 GET" is not true of its final bytes. The S229-S231 rows say they were added after
  the CADTH GET and the NCBI GETs; the file mtime is `23:48:34` local, after GETs S228-S230 (`23:47:35`, `23:48:10`).
  Open for the L1; no edit by the scribe.
- Correction candidate (challenge pages): the approval table and the S230 row say a challenge page is "never a
  capture", yet the S229 and S230 bytes sit under `corpus/captures/`. Open for the L1.
- Gate: S228 (403), S229 (203 cookie challenge), S230 (200 reCAPTCHA) rejected; S231 admitted, tier A for the
  abstract scope, quote 16 words, capture `corpus/captures/4ec85a1e83553aa272caeb69.txt`, sha256 `4111c45a…`.
  Scribe hashes: `.ufo/waves/round-98/w1/R98ScribeLesson-gate-hashes.txt`.
- C2 gates (`gate-records.py`, `research-gate.sh`, `search-rerun.py verify`, `entry-controls-r98.py`): not run by
  this scribe; the L1 and the verifier own them.
- Routed, not in this round: D1 (`S224` names two documents in `refetch.tsv`) stays carried; a self-test exit-path
  mutant (above) is a round-99 candidate.
