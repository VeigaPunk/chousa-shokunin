# LOG.md entry draft (seat R97ScribeLesson) — for the canonical planner to append to LOG.md; not written to the tracked file

## Round 97 — self-test grip measured against external mutants, and the PRESS checklist entry (2026-11-08, draft)

Lane `chousa`, round 97 (attempt 1, L1 `ChousaR97`). Base `c8087ac5` (round-96 landing); freeze F `9a0ce201`. Frozen
claims: `.ufo/waves/round-97/claims.md` / `claims.json`. Two claims: C1 operability (`tools/search-rerun.py --selftest`
at 47 cases, guarded per case, scored by `corpus/evidence/round97/selftest-controls-r97.py` against 30 external
mutants), C2 depth (`corpus/knowledge/press-checklist-questions-r97.md`, sourced on S225 and S226, S227 rejected on
route). Plan and pre-freeze fixes P0-P2: `plans/round-97.md`.

- Pre-freeze (P0-P2, `plans/round-97.md`): the battery reader accepts `str + str` only; the C2 forged-line-join control
  joins capture lines 36 and 38 (`QUOTE_ABSENT`); a `ONE_LINE` binding was added because `gate-records.py` matches the
  whitespace-collapsed whole text; the SKILL.md checklist item was dropped to keep the Gates row at line 180.
- Before (`corpus/evidence/round97/before/`): the base self-test passes 32/32; scored by the battery it kills 10 of the
  30 external mutants (`BASE_KILLED=10/30`, `c1-base.txt:68`); n11, n12, n13 and n26 exit 1 with a traceback and count as
  survivors (`c1-base.txt:47-49`, `:62`); the battery prints `SELFTEST_CONTROLS_R97=FAIL` (`:94`).
- After at F (`corpus/evidence/round97/after/`): `SEARCH_RERUN_SELFTEST: PASS cases=47/47` (`c1-all.txt:50`); the same
  four crash mutants are `KILLED` with failing case ids (`:63-65`, `:78`); three stand-ins fail the battery
  (`:138-140`). The receipt `c1-all.txt` ends at line 142 before the battery's tally and before the
  `regression-mutants-r95` leg: `SELFTEST_CONTROLS_R97=PASS` is not in any committed receipt (the seat's tail check,
  `.ufo/waves/round-97/w1/R97ScribeLesson-r97-c1-all-tail-check.txt`). Open until the complete tally is committed.
- C2 receipts at F: `corpus/evidence/round97/after/c2-all.txt` (`GATE_RECORDS files=1 records=30 ok=30 fail=0`,
  `METADATA_COMPLETE=1/1`, `SEARCH_RERUN_SUMMARY searches=7 rev_match=7/7`, `ENTRY_CONTROLS=PASS`). The entry's second
  reprint (S226) is corroboration, not a row's sole support. Verdicts: [pending the canonical planner's integration].
- Routed, not absorbed: the `refetch.tsv` id collision (`S224` names two documents; D1); the four gate-kind tools without
  `--selftest` (D3); the self-test's setup outside the per-case guard (`tools/search-rerun.py:450-474` and `:512`; a crash
  there survives the battery's rule, `R97ScribeLesson-unguarded-residue.txt`); the self-test's unexercised inputs beyond
  the 47 cases (`R96MutantsC1` class C, now covered only for the named inputs).
- Correction for the round-96 record (append-only, to be placed by the planner): `.ufo/waves/round-96/w1/R96MutantsC1.md:247`
  says "15 of them also pass the round-95 CLI battery". The body gives 3 of the 19 failing it (`:62`, `:64`, `:70`), 12
  passing it (the Class C section, `:103-153`), and 4 crashes not run. The probe's tally line `KILLED 10/30`
  (`R96MutantsC1-mutprobe-out.txt:60`) counts the skipped n08 in its denominator; the seat's own figure is `10/29`.
  Receipts: `.ufo/waves/round-97/w1/R97ScribeLesson-R96MutantsC1-md-class-grep.txt`, `R97ScribeLesson-r96-probe-tally.txt`.
- Mistakes mined: 1 (`corpus/lessons/round-97.md` `## Mistakes`, draft `.ufo/waves/round-97/w1/R97ScribeLesson-mistakes-draft.md`).
