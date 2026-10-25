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

## Corrections to this erratum (appended after the wave-2 critique `w2/R50CritErratum.md`; the text above stays as filed)

- Item 3 is not a post-freeze change: `build-spans.py` and `quote-substance-check.py` exist at `6a068f2a` and did not change afterwards (they are the round-49 files with the round number replaced at the freeze).
- Item 2 overstated: under the freeze-time `inference-ground` two of the three entries already exit 0; only the pure-Chinese entry (r41) was blocked (`tokens=0`, `INF_UNGROUNDED`). The repair is fair (a CJK token is now span-checked, floor four characters); an undisclosed consequence is that the polarity rule is structurally unreachable for CJK tokens (`words()` is Latin-only), so a flip inside the same span passes in all three entries (`w2/R50ExecInfLanded.md` §4). Named limit, QUALITY 79.
- Paths added after the freeze that the list above did not name: `corpus/fixtures/assimilate-selftest/` (the default fixture package, C1 leg 1's input; the counter pins only `c1-fixtures/`), the whole C2 candidate (three entries, S104–S106, the quote manifest, the lesson, QUALITY 73–79, the SKILL rows, README rows), the checks and receipts under `corpus/evidence/round50/`, and, after wave 2, `c1-supplement.py`, `controls/forge-tool.py`, `controls/c2-controls-at-landing.txt`, hardened `decode-form-check.py`, `wave-complete-check.py`, `cjk-ground-check.py`.
- Item 5 (new): `controls/build-c2-controls.py` (a frozen control file) was edited after the freeze: it copied the landed manifest into the control root, so its receipt `controls/c2-before.txt` no longer reproduced at the tip (`w2/R50ExecReplay.md` D1). It now ignores the manifest, spans and receipts; `controls/c2-controls-at-landing.txt` records the re-run: STAGED `C2=FAIL` (`REF_ID_UNBOUND=15`), TOOLED `C2=FAIL` with `BOUND=4/4` — once the tool widens `used-by`, the mechanical adoption binds every registry leg and only the quote, span, anchor, lesson and grounding legs separate it from the real work. `c2-before.txt` stays as scored at the freeze.
- The frozen C1 counter is weaker than its claim: W2 `R50CritForgeC1` passes it with a tool that replays the six literal DIFF lines (`controls/forge-tool.py`; `c1-supplement-receipt.txt` last block: `LEGS=5/5 C1=PASS`). The supplementary counter `c1-supplement.py` (nonce perturbation with an exclusive DIFF set, plus four hardening probes) is post-freeze and does not replace the frozen counter; the forge scores 1/5 on it, echo 2/5, constant 0/5, the base tool 1/5, the real tool 5/5. The C1 verdict is stated on both.
