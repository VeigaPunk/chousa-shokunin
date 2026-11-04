# R74ExecA — frozen loader-matrix comparison

Author-lane evidence only; no admission or promotion ruling.

## Scope and result

Axes: nine-case public-CLI loader correctness; preservation of frozen artifacts and host isolation.

Observed lane HEAD: `1eaa30ad248bbd3bd7469b2c17295fcda5fc02bb`.
Executed the unmodified round-74 loader matrix exactly twice, sequentially, with `--work /fast/scratch/hyaku/chousa-r74/R74ExecA`:

| Counter | Exit | Exact summary |
|---|---:|---|
| round73/c2-count.py | 1 | `LOADER_MATRIX=3/9 C1=FAIL` |
| round74/correction-count.py | 0 | `LOADER_MATRIX=9/9 C1=PASS` |

For the original, all three appends incorrectly exit 1 with only C2-6 failing; all three pure deletions incorrectly exit 0 with no failed checks. Unchanged, equal-line replacement, and receipt change match expectations.
For the successor, all appends exit 0 without failed checks; all deletions exit 1 with exactly C2-6 failing. Equal-line replacement still fails only C2-6; receipt change still fails only C2-7; unchanged passes. Thus deletion cases **pass the matrix by correctly failing the counter**.

## Mechanism

Direct source inspection of each counter's `load()` shows the original stores numstat column 0 (additions) as deleted lines, using 0 for nonnumeric cells. The successor stores column 1 (deletions), using 1 for nonnumeric cells. The unchanged C2-6 check rejects any nonzero protected-path deletion count.

The matrix appends two lines, producing additions/deletions 2/0; the original misreports two removals while the successor sees zero. Removing the sentinel produces 0/1; the original sees zero while the successor sees one. Equal-line replacement has 1/1, so both reject it. The nonnumeric fallback change is source-observed only: this matrix does not exercise it. No broader binary/encoding guarantee follows.

## Retained evidence (absolute paths)

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74ExecA/original-r73.stdout.txt` — complete original matrix stdout, including failed-case counter output, digest, fixture base/revisions, and summary.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74ExecA/original-r73.stderr.txt` — complete stderr (empty).
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74ExecA/original-r73.exit.txt` — exit 1.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74ExecA/successor-r74.stdout.txt` — complete successor matrix stdout, digest, fixture base/revisions, and summary.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74ExecA/successor-r74.stderr.txt` — complete stderr (empty).
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74ExecA/successor-r74.exit.txt` — exit 0.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74ExecA/execution.json` — exact commands, cwd, exits, SHA-256 digests, fixture-root guard, cleanup result, and axes.

Original counter SHA-256: `e6e22b1ec8d270171cf015d44cac3d544a61bd23a3fa67d14c91fa26585dc320`.
Successor counter SHA-256: `9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41`.

## Bounds, risks, and cleanup

No tools or production files edited; no installs, network, delegation, full battery, preflight, unrelated tests, or lane mutations. Only this report and the seven receipt files were created. The frozen matrix explicitly uses git -C and verifies its temporary fixture top-level after initialization, before add/commit. Runs were sequential, keeping one fixture live at most. Scratch was removed in finally after receipts were copied; execution.json records `scratch_removed: true`.

The matrix prints nested counter stdout only for mismatches; retained files contain its complete output, not suppressed passing-case nested output. The historical-landing conjunct was outside this seat's assigned two runs and was not exercised. No independent C1 admission is asserted. LSP tools are not available in this seat; analysis used direct source inspection, without symbol edits or refactors. No blockers.

## Self-evaluation

Accuracy 4/5: exact outputs/exits retained; successful nested stdout is intentionally omitted by the frozen matrix. Completeness 5/5: both assigned runs and append/deletion explanation delivered. Clarity 5/5: distinguishes matrix success from expected counter rejection. Actionability 5/5: exact commands, hashes and absolute receipts supplied. Conciseness 4/5: absolute-path inventory adds repetition required for handoff. Overall 4.6/5. Improvement: consult separate seats' historical-landing evidence before integration; do not broaden this seat's measured claim. Would the user agree? Expected, because the report separates observed outcomes from untested scope.
