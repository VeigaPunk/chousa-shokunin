# Draft01 — local pathlib source opening

Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Documentation-only, advisory; no production integration or claim closure.

## Behavior and findings

Opened installed Python **3.14.8**, source `/usr/lib/python3.14/pathlib/__init__.py`, and rendered both docstrings locally with pydoc. No web fetch.

- `PurePath.parents`, line 393: “A sequence of this path's logical parents.” — 7 words.
- `Path.resolve`, lines 934–935: “Make the path absolute, resolving all symlinks on the way and also normalizing it.” — 14 words.
- Line 932 defaults `strict=False`; line 938 delegates to `os.path.realpath(self, strict=strict)`; lines 63–72 implement positional ancestor selection.

**Draft inference:** resolving a path and selecting an ancestor do not establish intended lane identity. An explicit required-file check is separate and still cannot distinguish two populated roots. Existing S150 and the lane-root entry already carry this material; reuse the row. Sources opened are installed code/docstrings, not a fetched or located HTML manual.

## Gates and limits

Admit the narrowly quoted descriptions and observed implementation. Reject repository-detection or strict-default-existence interpretations. The existing knowledge entry has no literal `## Gate` section; this seat does not declare the frozen Gate criterion satisfied. S151/S152 and claim counters were not independently checked.

Frozen context retained verbatim: “Frozen C1 has E12/E13 fixture mismatch; inherited repair is c1-battery-supplement.py, a distinct post-freeze supplement. Report frozen failure honestly.” No C1 run or PASS asserted here; candidate ref-preflight-v3.py is not established production. Assigned freeze hash was not independently commit-blob checked.

## Commands, surfaces, and artifacts

Python version/location command printed `rc_version=0`, `rc_probe=0`. Successful pydoc command: `python3 -m pydoc pathlib.Path.resolve && python3 -m pydoc pathlib.Path.parents`; successful tool output, no explicit numeric exit printed. Three initial requests failed cwd validation before launch; exact commands and outputs are retained in evidence.

Empty scratch `/fast/scratch/hyaku/chousa-r64/Draft01/` removed with `rmdir` (successful tool result, no output). No clone, installs, package transaction, network, service restart, production edit, git/jj mutation, or tests/counter execution.

Touched only named seat report/evidence paths. L1 owns production integration; GNU realpath admission, fixture repair, counters, and canonical judgment remain outside this seat.

Full draft, gates, limits, and self-evaluation: `.ufo/waves/round-64/w1/Draft01/report.md`.
Exact commands, outputs, source excerpts and provenance: `.ufo/waves/round-64/w1/Draft01/evidence.md`.

Report: .ufo/waves/round-64/w1/Draft01.md
