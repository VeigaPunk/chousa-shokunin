# Round 50 — disclosed post-freeze changes (chousa)

author: chousa L1 (`ChousaR50`); date 2026-10-25. Appended after the freeze `6a068f2ae4847a1e4aa959f088a39ddc1b167bc0`;
`claims.md` is not edited.

Unchanged since the freeze (check: `git diff 6a068f2a <tip> --stat -- corpus/evidence/round50/c1-count.py
corpus/evidence/round50/c2-count.py corpus/evidence/round50/claims.md corpus/evidence/round50/controls
corpus/evidence/round50/c1-fixtures` prints nothing, except new receipt files added under `controls/` — none):
both predicates, both counters, the do-nothing controls, the pinned fixtures and the targets.

Changed after the freeze, all outside the frozen counters and all disclosed:

1. `tools/assimilate-rows.py` — the C1 candidate (`ec52e632`) was hardened after W1's first falsifiers
   (`w1/ReviewSelftestCode.md` F1–F4, `w1/ExecSelftestEdge.md`): multiset comparison, exit 2 for `--selftest` with
   another option or for a fixture with no entry, `ENTRYCITES … -` for an entry citing no id, a 120-second child
   timeout, tab-free findings, the fixtures check before the expected file. Separately, the appended row's
   `used-by` now names the entries citing ANY staged id that maps to the row (the 管理员 manual is staged four
   times; the old tool kept only the first row's citing entry — `w1/ExecAdopt.md` §5). Re-verified:
   `python3 corpus/evidence/round50/c1-count.py` → `LEGS=5/5`, `C1=PASS` (the round-49 counter is a leg).
2. `tools/inference-ground.py` — `has_two_words` also accepts four CJK characters. Before: a correctly grounded
   pure-Chinese bullet read as zero tokens, so the frozen C2 leg "all three entries exit 0 under
   `tools/inference-ground.py`" could not be met by any honest entry on these captures (`w1/DraftEntryR41.md` F1;
   round 49 passed only because its quotes held Latin runs). The leg's text is unchanged. Re-verified: the
   round-46/47/48 counters print identical output before and after
   (`inference-regression-before.txt`, `inference-regression-after.txt`); `cjk-ground-check.py` cases A–C.
3. `build-spans.py` and `quote-substance-check.py` are the round-49 files with the round number replaced.
4. The staged 教师 manual row was refused after a first integration draft had bound it (S107); the frozen
   counter allows three of four documents bound, and the row and its quotes were removed before any commit.
   `BOUND=3/4 REFUSED=1`.

No claim text, target or kill rule was narrowed after data; a miss would be reported as a miss.
