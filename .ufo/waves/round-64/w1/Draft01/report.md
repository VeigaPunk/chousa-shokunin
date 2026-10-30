# Draft01 — pathlib source-grounded lane-root draft

## Behavior and axes

Axes: quotation fidelity, exact local provenance, bounded scope, and reproducible handoff. Documentation-only work for `/home/vgpnk/Projects/shokunin/chousa-shokunin`; L1 alone integrates production. Source opening completed; no claim execution or closure asserted.

## Findings and integration-ready draft

Installed interpreter: `/usr/bin/python3`, Python **3.14.8**. Installed source: `/usr/lib/python3.14/pathlib/__init__.py`. Accessed 2026-10-30. This is implementation source with locally rendered pydoc, not an opened HTML reference manual. Existing registry row **S150** already names this source; reuse it rather than inventing another row.

Suggested lane-root entry wording:

> S150 documents `PurePath.parents` as “A sequence of this path's logical parents.” (line 393; 7 words). `Path.resolve` says “Make the path absolute, resolving all symlinks on the way and also normalizing it.” (lines 934–935; 14 words). Its signature defaults `strict=False` (line 932), and its implementation delegates to `os.path.realpath(self, strict=strict)` (line 938). The parent sequence removes components positionally via `_tail[:-idx - 1]` (lines 63–72). **Inference:** normalizing a path and selecting a positional ancestor do not establish the intended lane's identity. An explicit check of the exact required lane file is a separate application condition, not a guarantee supplied by either quotation. Even an existence check cannot distinguish two populated roots.

The quotations total 21 whitespace-delimited words and each is independently below the requested 25-word ceiling. The resolve quote joins one source line break with a space, as pydoc renders it.

## Gates and known limits

- **Admit, scoped:** S150 supports the stated logical-parent description, resolve docstring, default argument, and implementation delegation. Exact local locators were opened and pydoc reproduced both docstrings.
- **Reject:** any stronger reading that `parents[n]` detects a repository, or that default `resolve()` guarantees intended-root identity or strict existence. Those claims are unsupported by these quotes. This is rejection of an inference, not another source-row opening.
- The existing lane-root entry already contains these quotes and positional-arithmetic observations. No production change is needed merely to duplicate this draft.
- The opened entry has no literal `## Gate` section. Its `## Rejection and limits` rejects S153, but this seat does not promote that prose into satisfaction of the frozen requirement for Gate rows with per-row access dates and located quotes. L1 owns integration and any closure determination. S151/S152 were not independently source-reopened by this seat.
- Frozen C1 context, verbatim from assignment: “Frozen C1 has E12/E13 fixture mismatch; inherited repair is c1-battery-supplement.py, a distinct post-freeze supplement. Report frozen failure honestly.” This seat did not run C1; it makes no PASS claim. `ref-preflight-v3.py` remains a candidate, not established production.
- The assigned freeze hash was not independently checked against a commit blob. Working-tree frozen-claims text was read first before investigation. Plain findings are advisory, not outside non-author closure.

## Commands and outcomes

Full commands, outputs, source excerpts, and failed-launch records: `evidence.md` beside this report.

- Python version/source-location command printed `rc_version=0`, `rc_probe=0`; version 3.14.8 and exact installed path matched the claimed Python version.
- `python3 -m pydoc pathlib.Path.resolve && python3 -m pydoc pathlib.Path.parents` returned successful documentation output. No explicit numeric exit was printed by this command.
- Three earlier shell requests were rejected before launch because the requested scratch cwd did not yet exist; they produced no exit codes or evidence. The later successful pydoc call was not a rerun of an executed check.
- No tests, counters, fixture drivers, or production verification were run. No tool installs/updates; existing Python was used through the system installation for the explicitly requested local documentation opening.

## Touched surfaces and exclusions

Writes only: this report, `evidence.md`, and the explicitly requested sibling trailer report `.ufo/waves/round-64/w1/Draft01.md`. Scratch `/fast/scratch/hyaku/chousa-r64/Draft01/` was created empty for documentation commands and removed before handoff. No clone was created. No production, operator input, frozen claim/counter, sibling output, PATH directory, or fleet tracked file was modified. No network fetch, package transaction, service restart, git/jj mutation, commit, push, judge, publication, or deployment.

Out of scope: GNU realpath source admission, C1 fixture repair, counter execution, source-registry/knowledge-entry integration, and canonical Rust judgment.

## Self-evaluation

Accuracy 4/5: source quotes located directly, but no commit-blob binding. Completeness 4/5: requested Python evidence complete; full reference-manual installation not established and not claimed. Clarity 4/5: source facts and inference separated; report retains required failure receipts. Actionability 4/5: draft and locators ready for L1; closure remains external. Conciseness 4/5: detailed command history isolated in evidence. Mean 4.0/5. Improvement priority: L1 should preserve the installed-source/docstring qualification and explicit Gate distinction when integrating; do not invent a manual source or PASS receipt. User-agreement self-check: assessment is limited to this seat's evidence, not C3 acceptance.

## Artifact paths

- `.ufo/waves/round-64/w1/Draft01/report.md`
- `.ufo/waves/round-64/w1/Draft01/evidence.md`
- `.ufo/waves/round-64/w1/Draft01.md`
