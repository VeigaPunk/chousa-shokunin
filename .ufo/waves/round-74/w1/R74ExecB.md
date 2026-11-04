# R74ExecB — committed r73 landing probes

Author-lane evidence only; no independent admission authority.

Axes: CLI outcome fidelity; independent deletion evidence; historical status neutrality.

## Scope and results

Frozen scripts extracted read-only from revision `1eaa30ad248bbd3bd7469b2c17295fcda5fc02bb`; both matched the supplied working-file bytes. Each CLI inspected committed landing `5aec90775fc7cc1fe9ad442e0d5491731323eec1` against base `f748abbb6bf58388e732facd4ecec5612419c457`.

- Successor: exit **0**, `C2=PASS checks=7/7 rev=5aec90775fc7 base=f748abbb6bf5`.
- Original frozen r73 CLI: exit **1**, `C2=FAIL checks=6/7 rev=5aec90775fc7 base=f748abbb6bf5`. Sole failed check: **C2-6**, reporting LOG:11, lesson:6, SCORECARD:21 as removed lines.
- Independent protected-file `git diff --numstat`: exit **0**, additions/deletions `11/0 LOG.md`, `21/0 SCORECARD.md`, `6/0 corpus/lessons/round-72.md`.
- Both CLIs passed C2-7 (historical receipts unchanged). All three processes had empty stderr.

The original loader reads additions (column 0) as deletions; the successor reads deletion column 1. Independent Git evidence shows zero actual deletions, agreeing with the successor and explaining the original C2-6 false rejection.

## Interpretation and limits

The successor historical-landing conjunct is satisfied. This seat did not run the nine-case loader matrix and does not establish the full round74 C1 predicate alone. Historical r73 admission remains rejected: successor certification does not retroactively replace the frozen instrument or admit r73. No broader semantic correctness or general expertise claim is made.

## Exact retained evidence

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74ExecB/successor.txt` — exact invocation, stdout and exit.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74ExecB/original.txt` — exact invocation, stdout and exit.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74ExecB/protected-numstat.txt` — independent Git invocation, stdout and exit.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-74/w1/R74ExecB/probes.json` — complete process records, frozen revision and script SHA-256 hashes.

Successor SHA-256: `9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41`.
Original SHA-256: `e6e22b1ec8d270171cf015d44cac3d544a61bd23a3fa67d14c91fa26585dc320`.

## Boundaries and cleanup

Only this report and the four receipt files were retained. No production edits, Git mutations, clone, network, package installs, build/lint/full-battery runs, or delegation. Scratch `/fast/scratch/hyaku/chousa-r74/R74ExecB/` was explicitly created and removed in `finally` after saving receipts (`SCRATCH_REMOVED=True`). No blockers. Integration owner must combine this evidence with the independently assigned matrix result; this seat makes no promotion decision.

Self-evaluation: accuracy 4/5 (bounded CLI outputs, not broader certification); completeness 5/5 (both CLIs, numstat, exits, pinned bytes, cleanup); clarity 4/5 (full hashes necessarily dense); actionability 5/5 (absolute receipts and precise integration boundary); conciseness 4/5 (provenance repeated for standalone usability). Overall 4.4/5. Improvement: use the JSON receipt for machine aggregation rather than parsing this prose. User-agreement self-check: findings remain explicitly scoped to the assigned probes.
