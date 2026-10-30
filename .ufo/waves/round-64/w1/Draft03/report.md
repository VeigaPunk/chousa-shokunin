# Draft03 — reject intended-root proof from existence assertions

## Behavior and finding

**REJECT** the stronger statement: “The existence assertions prove that the derived root is the correct intended lane root.”

**ADMIT, narrowly:** the source implements an early regular-file check at the computed paths and a missing-file diagnostic/exit branch. This is source evidence of the branch, not execution evidence that any counter passed.

Axes: evidential accuracy, source traceability, scope containment. No axis score or production-readiness verdict is claimed.

## Located local source

Primary local source opened directly, without a network fetch: `/usr/lib/python3.14/pathlib/__init__.py`.

- Lines 63–72: `_PathParents.__getitem__` constructs a parent by slicing `self._tail[:-idx - 1]`. Lines 392–396 describe parents as “A sequence of this path's logical parents.” These operations select components; they do not compare repository identity or operator intent.
- Lines 932–938: `resolve(self, strict=False)` documents making the path absolute, resolving symlinks and normalizing it, then delegates to `os.path.realpath(self, strict=strict)`. Neither the shown implementation nor its docstring promises intended-lane selection.
- Lines 685–695: `is_file` documents “Whether this path is a regular file (also True for symlinks pointing to regular files).” With its default `follow_symlinks=True`, it delegates to `os.path.isfile(self)`. That property does not authenticate file content, repository provenance, or the intended root.

Lane source opened directly:

- `corpus/evidence/round64/c3-count.py:34–39`: `HERE = pathlib.Path(__file__).resolve().parent`, `LANE = HERE.parents[2]`, then `is_file()` on `corpus/SOURCES.md`; the false branch prints `MISSING_LANE_FILE:` and raises `SystemExit(2)`.
- `corpus/evidence/round64/c1-battery-v3.py:119–124` and `corpus/evidence/round64/run-receipts-v3.py:25–30`: the same arithmetic, checking `corpus/SOURCES.md` and `tools/lane-preflight.py`.
- `corpus/knowledge/lane-root-derivation-r64.md:20–23` already limits the claim: parent selection has no intended-root binding, and a check does not catch a wrong but populated root. Its lines 29–31 explicitly disclaim provenance/content proof and disambiguation of populated trees.
- `corpus/SOURCES.md:160–162` scopes S150 to installed pathlib implementation, S151 to existing-components semantics, and S152 to counter source rather than a passing relocation verdict. This report directly reopened S150; it did not reopen the S151 man page.

**[INFERENCE] Non-entailment:** an unintended tree containing regular files at all checked relative paths satisfies those checks just as the intended tree does. The predicates shown have no input representing the intended repository identity. Thus check success cannot logically distinguish those cases. This is a source-based countermodel, not an executed fixture.

Suggested rejection text for L1: “Rejected as proof of intended root: positional parent selection, path resolution, and regular-file assertions establish a derived location and the presence/type of selected entries, not that the location is the operator-intended lane. Admit only the missing-derived-file fail-fast behavior, subject to separate execution receipts.”

This does not reject frozen C3 merely for lacking the stronger property: `claims.md:235–239` already excludes a relocated complete tree from the probe's scope. No new closure rule is introduced.

## Gates, provenance, and execution evidence

- Read `/home/vgpnk/.omp/agent/RULES.md` first, then the frozen claims and `skill://godspeed`; read `skill://agent-self-evaluation` before delivery.
- All inspected lane paths were under `/home/vgpnk/Projects/shokunin/chousa-shokunin`; installed-library source was read-only.
- Read operations: `claims.md` (complete tool response); knowledge entry `:1–150`; counter `:1–130`; installed pathlib `:40–75,385–400,925–945` and `:649–702`; battery `:45–85`. Glob located the knowledge entry; grep located S150/S151/S152 and startup assertion lines. Outcomes: successful tool responses containing the quoted source. File-read/search tools do not report process exits; exit status **not applicable**, not assumed zero.
- Shell commands, fixture probes, counters, build/tests, another runtime, git/jj commands, and network fetches: **none executed**. No execution receipt or success verdict is fabricated. This seat's item required a source-grounded rejection, not a runnable probe.
- No tools installed or updated; no version command run. Python 3.14.8 and coreutils 9.12 are source-row declarations, not versions measured by this seat.
- Scratch `/fast/scratch/hyaku/chousa-r64/Draft03/` was never created or used; no clone or scratch tree was created and none requires removal by this seat.

## Frozen failure and boundaries

The assignment states: “Frozen C1 has E12/E13 fixture mismatch; inherited repair is c1-battery-supplement.py, a distinct post-freeze supplement.” This is inherited failure information, not independently executed here. It must not be upgraded to frozen C1 PASS by a supplement result. Candidate `ref-preflight-v3.py` is not production. This report claims neither C1 nor C2 nor C3 execution success and makes no outside non-author closure judgment.

Frozen claims were read from the requested local path; this seat did not independently verify the supplied freeze commit `bf40d99bda9eefdad3ed6276da077cfb24ba82f1` or its file hashes. The source reads establish observed local text, not commit-byte identity.

## Output-path conflict (verbatim)

- “Write only your own report and evidence beneath /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Draft03/ (report.md); no production edits.”
- “Report: write your scoped findings to .ufo/waves/round-64/w1/Draft03.md”

These name different destinations. This seat honors the explicit only-own-folder write boundary and writes this report inside `Draft03/`; the sibling-level `Draft03.md` is intentionally not written. Canonical routing/judgment remains with L1 and the canonical Rust judge.

## Touched surfaces and artifact

Only created artifact: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Draft03/report.md`.

No product, frozen claim/counter, operator input, judge, sibling, fleet-root tracked file, PATH directory, or service was modified. No commits, pushes, publishes, deployments, or production integration performed.

## Self-evaluation

Accuracy 4/5: source quotations are directly observed; commit-byte identity is deliberately unverified. Completeness 4/5: rejection and local authority are supplied; contradictory trailer destination is left unwritten to preserve the stricter write boundary. Clarity 4/5: admission/rejection and inference are separated; detailed provenance adds length. Actionability 4/5: ready-to-use rejection text is supplied; routing requires canonical adjudication. Conciseness 4/5: audit requirements add evidence and conflict sections. Overall 4.0/5. Highest-impact improvements belong to L1: resolve output routing and bind any admitted execution claim to its actual frozen-byte receipt. These are limits, not new seat tasks. Self-check: the report distinguishes every observed source fact from inference and inherited status.
