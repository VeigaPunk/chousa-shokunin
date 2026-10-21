# ReviewSourceAdmission — round27 attempt1

**Assigned item:** Review proposed own-work source boundaries; regression output is not semantic truth; reject overbroad public-source inference. Static review only; no verification run.

## Finding

- **Low — inexact located quote:** `corpus/lessons/round-27.md:57` attributes `“Verdict: RESEARCH_GATE: CLEAN\u007cDRIFT”` to `.ufo/waves/round-26/falsify/FNoTrade.md:124–128`. The source at line 126 has the literal `CLEAN|DRIFT`; `\u007c` is not that character in this Markdown inline-code quote. Replace it with the literal `|` or quote a shorter exact substring. The report itself confirms the unsatisfiable help-text predicate at lines 124–128.

## Source boundary and acceptance oracle

- S040–S042 (`corpus/SOURCES.md:50–52`) are appropriately scoped as **own-work**: their authority is only what the named local r26 reports say about the reported C1, C2, and C3 diagnoses. Tier A is defensible for that narrow scope, not for general gate correctness, source relevance/truth, or the success of the proposed repairs. The R27 lesson already calls them reported diagnoses (`corpus/lessons/round-27.md:61–69`); retain that qualification and use exact report path/line/quote anchors. `S042`'s quote at lesson line 59 matches `FRegistryHeaderless.md:45`; `S041`'s quote at line 58 matches `FDateHugeCadence.md:42–44`.
- **Do not turn counts into semantics.** C1 acceptance is the independent harness controls plus full selftest PASS with all 187 original case identities and expected exit/diagnostic/no-verdict requirements intact (`corpus/evidence/round27-claims.md:5–7`). C2 acceptance is zero mismatches in the specified synthetic suite and original date differential, preserving ASCII-only dates, long/all-zero cadence, bounds/overflow, strict overdue semantics, and plain mode (`:9–11`). C3 acceptance is zero mismatches in persisted controls while retaining well-formed registry/exact-used-by behavior, fresh named headers and widths, unique standalone ASCII S-id occurrences, and complete-filesystem-path refusal without changing citation-pointer semantics (`:13–15`). A regression count, mechanism-text count, successful status code alone, or source row is not a semantic pass; acceptance must be tied to observed final receipts and limited to those contracts.
- **Public sources stay out of this admission.** The task requires local source opening; do not reuse r26 public-source proposals or rows as fresh validation, and do not imply these repairs admit r26 claims or full criterion-6 semantic verification (`round27-claims.md:19`; r26 withdrawal in `corpus/lessons/round-26.md:190–193`). New own-work rows may support the lesson's account of local reports only. No public source was opened or independently revalidated by this review.

## Residual risk and verification gaps

The source census scout records the initial base census only (`.ufo/waves/round-27/build/ScoutSourceCensus.md:77–90`); this review did not derive a final census or run regressions, selftest, differential scripts, or frozen checks. I make no after-result or pass claim. Broader registry grammar/resource safety and public-source/criterion-6 support remain outside these bounded repairs (`corpus/lessons/round-26.md:181–183,190–193`).
