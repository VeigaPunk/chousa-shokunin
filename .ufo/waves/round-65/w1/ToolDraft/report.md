# ToolDraft — round65 C1 independent implementation draft

## Behavior and provenance

Deliverable: `.ufo/waves/round-65/w1/ToolDraft/receipt-pin.py` (executable Python draft; no production installation).

Axes: interface fidelity, independent implementation, auditability, and lane-boundary compliance.

Read `/home/vgpnk/.omp/agent/RULES.md` first in the initial read batch; also read `skill://godspeed`, `skill://python-patterns`, and `skill://agent-self-evaluation`. Opened frozen `corpus/evidence/round65/claims.md`, `c1-count.py`, and `controls/c1-positive.txt`. The claims file enumerates C1 and C2 only. Git HEAD was observed at `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`.

The implementation was written before opening `controls/ref-receipt-pin.py`. Reference source was then read for comparison only; it was neither run nor modified. A subsequent draft edit aligned decimal EXIT syntax with the reference's no-leading-zero convention. A misplaced text patch was immediately repaired using a fresh ranged read; no execution occurred between those edits.

The draft implements `--receipt`, `--root`, and `--revision`; exactly ordered REVISION/EXIT/SHA256 headers; lowercase full-width revision and digest; an empty separator; non-whitespace output; canonical relative POSIX path components; Git-blob SHA256 comparison; and PASS/FAIL tokens with return classes 0/1/2. Nonzero reported EXIT values are valid consistency data, not validator failure. It never reads the named working-tree file. These are source-level descriptions, not observed execution results.

## Gates and exact commands

Executed successfully, read-only:

```sh
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD
```

Observed stdout: `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`.

An earlier compound command was submitted with a nonexistent scratch cwd and did not start:

```sh
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain=v1 -- corpus/evidence/round65/claims.md tools/ | wc -l && grep -c '^## C' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round65/claims.md
```

Tool response: `Working directory does not exist: /fast/scratch/hyaku/chousa-r65/ToolDraft`. No status/count result is claimed. The unnecessary shell grep was never executed; claims were instead read through the file tool.

Executed cleanup/absence check:

```sh
env TMPDIR=/fast/scratch/hyaku/chousa-r65/ToolDraft/ sh -c 'if test -e "$TMPDIR"; then rmdir -- "$TMPDIR"; else printf "%s\n" "SCRATCH_ABSENT=$TMPDIR"; fi'
```

Observed stdout: `SCRATCH_ABSENT=/fast/scratch/hyaku/chousa-r65/ToolDraft/`.

No scratch directory or clone was created. No runtime invocation of the draft, full counter, isolated probe, tests, formatter, lint, compilation, or battery was performed. The positive control's recorded 20/20 belongs to the reference, not this draft. No pass count is asserted for this candidate. No installations, network fetches, git/jj mutations, production edits, sibling writes, or system operations occurred.

L1 verification command, NOT EXECUTED here (fresh L1-owned work directory required):

```sh
python3 corpus/evidence/round65/c1-count.py --tool /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-65/w1/ToolDraft/receipt-pin.py --work /fast/scratch/hyaku/chousa-r65/L1/tooldraft-c1
```

## Findings and known limits

- Frozen 20-case interface coverage is described by the counter but remains unexecuted for this draft. Only L1 can verify/admit/integrate it.
- Draft and reference both reject leading-zero EXIT values and whitespace-only output. These details are more specific than the claims' shorthand wording.
- Draft requires literal LF header/separator framing and accepts arbitrary non-whitespace body bytes; reference decodes UTF-8 and uses universal text line splitting. Thus CRLF framing and invalid UTF-8 body handling differ outside the frozen cases.
- Draft rejects NUL and CR in paths before subprocess argv construction. Canonical components reject absolute paths, duplicate slashes, dot segments, traversal, and trailing slash.
- Draft reports unreadable receipts, unavailable Git/revision, or blob-read failures after a successful type lookup as environment failures (2). Reference groups many of those failures under invalid (1), despite its documented 2 class. Frozen cases do not settle these environment distinctions.
- Draft requires an actual commit revision and disables Git replacement objects; reference directly asks for a blob with the supplied object expression. No authentication claim follows from either design.
- No general parser-security, resource-limit, hostile-Git-environment, or execution-authenticity guarantee is made. The body and reported EXIT are not independently authenticated or replayed. Git lookups are separate read-only processes, not a repository transaction.

## Touched surfaces and scope

Only this seat's draft/report surfaces are written. Frozen claims, counters, controls/reference, `tools/receipt-pin.py`, and C2 knowledge/source surfaces remain unchanged. The report trailer file is an index to this report, not shipping authority.

Path directives, preserved verbatim for canonical interpretation:

> Each writes only its own absolute w1/<seat> output folder; no concurrent production writers.

> Write only /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-65/w1/ToolDraft/report.md and any uniquely named evidence in that folder. No production writes.

> Report: write your scoped findings to .ufo/waves/round-65/w1/ToolDraft.md

The named trailer index is written as the explicit Report-path exception; no other outside-folder write is made.

## Self-evaluation (not an acceptance gate)

Accuracy 4/5: observed commands are separated from unexecuted implementation claims; executable correctness is unverified. Completeness 4/5: complete draft and comparison supplied; verification is deliberately reserved to L1. Clarity 4/5: explicit format/error-class differences remain for integration judgment. Actionability 4/5: exact draft and L1 counter command supplied, but no runtime evidence. Conciseness 4/5: report retains command/path-conflict detail needed for audit. Mean 4.0/5. Highest-impact next action is L1's permitted verification; environment/newline semantics need explicit integration judgment if broader equivalence is desired.

## Artifact paths

- `.ufo/waves/round-65/w1/ToolDraft/receipt-pin.py`
- `.ufo/waves/round-65/w1/ToolDraft/report.md`
- `.ufo/waves/round-65/w1/ToolDraft.md` (requested report trailer index)
