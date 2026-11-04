# R74Review — adversarial source review

Frozen revision: `1eaa30ad248bbd3bd7469b2c17295fcda5fc02bb`. Author-lane recommendation only; no admission or promotion authority.

Axes: loader reachability, deletion orientation, independent case expectations, failure honesty, fixture isolation.

## Findings by severity

**No correctness blocker found for the frozen nine-case predicate and historical-landing conjunct.**

- The successor diff against r73 contains the docstring change, executable-mode change (100755 to 100644), and one functional line at `corpus/evidence/round74/correction-count.py:131`: deletion counts now use numstat column 1, and a nonnumeric deletion cell maps to 1 (reject). Column 0 is additions; column 1 is deletions. Invocation explicitly uses Python, so the mode change does not break the claimed commands. The r73 counter has no diff between parent `8a28732b` and the frozen revision.
- Actual loader exercised: `loader-matrix.py:37-65` initializes a real repository, asserts its toplevel before the first commit, commits each case, then invokes the selected counter's public CLI with fixture `--lane`, `--base`, and `--rev`. The counter's `main():194` calls `load()`, whose lines 126-134 read committed files and real Git diffs. No helper injection on this matrix path.
- Independent expectations: `loader-matrix.py:22-26` fixes unchanged/append as rc 0, delete and equal-line replacement as rc 1 with only C2-6 failing, and receipt change as rc 1 with only C2-7 failing. Lines 66-70 compare exact failed-id sets, seven distinct check records, exit status, and summary verdict. Counter subprocess errors without CHECK output cannot pass as an expected rejection.
- Fixture setup errors raise RuntimeError/OSError and return 2 (`loader-matrix.py:28-31,84-88`). Observed missing-work-directory error returned 2 with MATRIX_SETUP; this is distinct from mismatch exit 1.
- Isolation: every fixture Git invocation uses explicit `git -C`; each case restores all five baseline files before mutation and commit. TemporaryDirectory scopes repository cleanup. Both matrix work directories were empty after execution. Scratch was removed in a finally block after preserving receipts. No production edits, lane Git mutations, installs, commits/pushes in the lane, network, broad battery, or preflight were performed.

## Observed bounded results

| Probe | Exit | Result |
|---|---:|---|
| Matrix against r73 | 1 | LOADER_MATRIX=3/9 C1=FAIL; all three pure appends incorrectly rejected and all three deletions incorrectly accepted |
| Matrix against successor | 0 | LOADER_MATRIX=9/9 C1=PASS; all expected failed-id sets match |
| Successor on pinned r73 landing | 0 | C2=PASS checks=7/7 |
| Frozen r73 on same landing | 1 | C2=FAIL checks=6/7, only C2-6 fails |
| Successor helper selftest | 0 | SELFTEST=PASS mutations=7/7; supplemental, not loader proof |
| Matrix nonexistent work directory | 2 | MATRIX_SETUP diagnostic |
| UTF-8-decodable NUL-containing binary SCORECARD | 1 | Real numstat `-\t-\tSCORECARD.md`; C2-6 fails conservatively (also C2-4 fails because content was replaced) |
| Invalid-UTF-8 binary SCORECARD | 1 | UnicodeDecodeError during git-show decoding; never reports PASS |

Counter SHA256: before `e6e22b1ec8d270171cf015d44cac3d544a61bd23a3fa67d14c91fa26585dc320`; successor `9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41`.

## Residual risks and verification gaps

- **Non-blocking inherited binary diagnostic limitation:** `correction-count.py:119,126` uses text-mode git-show decoding before parsing numstat. Invalid UTF-8 raises UnicodeDecodeError rather than producing structured CHECK/C2 output. It fails closed, not falsely positive; binary end-to-end support is outside the nine-case claim. Do not advertise universal clean binary handling. Evidence: binary-invalid-utf8 receipt.
- The matrix checks exact failed-id sets, not the complete seven-id universe, all verdict tokens, or the numeric summary suffix (`loader-matrix.py:66-70`). This is adequate for the inspected counter's fixed output but not a general adversarial counter-output validator. No claim of broader mutation saturation is supported by these nine cases.
- LSP unavailable: reading `xd://lsp` returned “No such tool”; no semantic references/definition/diagnostics service was available. Caller conclusions are grounded in source inspection and the explicitly authorized CLI probes, not semantic indexing.
- Existing substring semantic weaknesses and broader repository behavior were intentionally not certified. No broad tests/build/lint/preflight were run. The successful successor does not alter or admit historical r73 results.

## Absolute evidence paths

All receipts are under `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74Review/`:

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74Review/before-matrix-R74Review.txt`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74Review/after-matrix-R74Review.txt`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74Review/landing-after-R74Review.txt`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74Review/landing-before-R74Review.txt`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74Review/setup-error-R74Review.txt`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74Review/binary-utf8-R74Review.txt`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74Review/binary-invalid-utf8-R74Review.txt`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74Review/selftest-R74Review.txt`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74Review/probe-metadata.json`

Self-evaluation: accuracy 4 (raw binary receipt lacks explicit exit marker; tool output and metadata retain the observed rc); completeness 4 (no LSP available); clarity 4 (source and runtime evidence separated); actionability 4 (scope boundary and binary limitation explicit); conciseness 4 (absolute paths necessarily repetitive). Average 4.0. Improvements: use one probe driver with integrated exit metadata; require LSP availability for future semantic review. Would the user agree: likely, given reproduced predicates and explicit non-admission boundary.
