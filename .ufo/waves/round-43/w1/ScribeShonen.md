# ScribeShonen — round 43, wave 1 (scribe)

Seat: chousa round-43 leaf L2, item ScribeShonen. Assigned attack: read `SHONEN.md` if it exists, list the four promotion boxes, and say this round can only mark them `[~]` because no non-author verifier has signed.

Pins: dispatcher measured commit `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`. Observed `git rev-parse HEAD` equals that commit. `SHONEN.md` last commit is `d8c8cff3923f10481ac9ced66d0af7c41d38130c` (ancestor of HEAD; subject `round-25: land verify-metadata gate omitted from integration checkpoint; canonical SHONEN form`, date `2026-10-21T04:35:31-03:00`). Working tree for `SHONEN.md` matches HEAD (`git diff --quiet -- SHONEN.md` exit 0). File bytes 868, sha256 `6cebe10f9b2a855447c3cc4e06a8e846c09912285e0c89b79e02854a290e2e71`. Mark counts in the file bytes: `[~]`=4, `[x]`=0, `[ ]`=0.

Method: read-only against the lane tree. No network, no fetch, no production edit, no git index or jj operation, no sibling or fleet write, no tool install. This seat did not run the round-43 counters. The only file written is this report.

## Axes walked

1. Operability — the four boxes are a checklist with marks, not a command this seat executed.
2. Calibration — do not upgrade a lane assertion, a pointer that exists, a prior heading check, or this lane seat into a non-author signature.
3. Depth — quote the boxes and the round-43 pending sentence, and separate "heading present with `[~]`" from a signature that would allow `[x]`.

## Behavior

Read `SHONEN.md` (12 lines, file exists). Counted marks. Confirmed HEAD, cleanliness, last commit, and the absence of `corpus/lessons/round-43-verifier-spotcheck.md`. Checked that the paths cited under the four boxes exist as files or a directory. Did not run those paths. Did not edit `SHONEN.md`. Did not mark any box `[x]`.

## Gates

| Gate | This seat | Result |
|---|---|---|
| `SHONEN.md` exists and lists four boxes | read | observed, four boxes, all `[~]` |
| This round may mark a box `[x]` | lesson pending sentence + missing round-43 verifier file + this seat is a lane seat | no — only `[~]` |
| C1 `c1-count.py` prints `C1=PASS` exit 0 | not run | unobserved; not execution evidence |
| C2 `c2-count.py` prints `SPLIT_AGREES=15/15` exit 0, and `--flip S086` exits 1 | not run | unobserved; not execution evidence |
| C3 `c3-count.py` prints `C3=PASS` exit 0 | not run | unobserved; not execution evidence |

Author text in `corpus/lessons/round-43.md`, `SCORECARD.md` (Round 43 verdict), and `LOG.md` (Round 43) states C1/C2/C3 results. Those sentences are not this seat's runs. An unrun check has not passed here.

## Four boxes

`SHONEN.md` exists. Header: "Promotion to shokunin requires all of:". The four boxes, quoted from the file, are all `[~]`:

1. `[~]` SKILL.md contains real decision tables, error patterns, checklists, cited sources
   `` `SKILL.md` Gates table; `corpus/knowledge/metadata-screen-r25.md` (lane assertion; no non-author verifier) ``
2. `[~]` At least one end-to-end domain task executed and logged in LOG.md
   `` `LOG.md` Round 9 archive verification; `corpus/fixtures/archives-r9/`; r25 explicit-root hold battery (lane assertion) ``
3. `[~]` Instructions executable by an agent without oral context
   `` `bash tools/research-gate.sh --selftest`; `corpus/evidence/round25-measure-after.log`, `round25-meta-differential.log` (lane assertion) ``
4. `[~]` No cross-domain bleed (PROVINCE.md still accurate)
   `` `PROVINCE.md`; `corpus/knowledge/metadata-screen-r25.md` Limits; `.ufo/waves/round-25/build/ConnectorMetaSiblings.md` (lane assertion) ``

This round can only mark them `[~]`, because no non-author verifier has signed. This seat is a lane-dispatched seat. `corpus/lessons/round-43.md` says seats this lane dispatches are still the lane. A lane seat cannot sign the boxes, and this report is not a signature.

Precision, not a retune of the marks: only box 1's evidence line contains the words "no non-author verifier". Boxes 2–4 say "(lane assertion)" only. All four checkbox marks are `[~]`.

## Findings

- F1. The checklist is already `[~]` on all four boxes at the measured commit. Round 43 did not change `SHONEN.md` (last touch `d8c8cff`, round 25; diff against HEAD empty).
- F2. No round-43 non-author spot-check file is in the lane. `corpus/lessons/round-43-verifier-spotcheck.md` is missing. Lesson, verbatim:

```
### Non-author spot-check

Pending. Seats this lane dispatches are still the lane.
```

  (`corpus/lessons/round-43.md` lines 58–60.)
- F3. `SCORECARD.md` Round 43 learning line, verbatim: "Learning trends, lane view: expansion improved (one opened row, one lesson, one new operation); quality improved (counters against do-nothing controls; QUALITY 61); discernment unchanged until a non-author spot-check." That sentence does not sign the four boxes.
- F4. Cited paths exist (file or directory). Existence is not a pass and not a signature. This seat did not run `bash tools/research-gate.sh --selftest` and did not re-read the cited logs.

| cited path | observed kind |
|---|---|
| `SKILL.md` | file |
| `corpus/knowledge/metadata-screen-r25.md` | file |
| `LOG.md` | file |
| `corpus/fixtures/archives-r9` | dir |
| `tools/research-gate.sh` | file |
| `corpus/evidence/round25-measure-after.log` | file |
| `corpus/evidence/round25-meta-differential.log` | file |
| `PROVINCE.md` | file |
| `.ufo/waves/round-25/build/ConnectorMetaSiblings.md` | file |

- F5. Prior non-author files confirm `[~]` and do not promote the boxes. They are not a round-43 signature. Verbatim:
  - `corpus/lessons/round-42-verifier-spotcheck.md:14`: `` `SHONEN` heading present at report line 154 with four `[~]` lines, one per box — PASS. ``
  - `corpus/lessons/round-41-verifier-spotcheck.md:81`: "D4 (note for operator): SHONEN boxes are all `[~]` lane-asserted with resolvable pointers; they are checkable by a non-author (gate selftest, LOG entries, PROVINCE) — promotion is operator-owned and not exercised here."
  - `corpus/lessons/round-40-verifier-spotcheck.md:69-71`: "## SHONEN promotion note" / "All four boxes are checkable by a non-author (each `[~]` line carries resolvable pointers; box 3 cites runnable artifacts). Promotion is operator-owned; flagging for the operator only."
  - `corpus/lessons/round-28-verifier-spotcheck.md:137-139`: "SHONEN: the four boxes are all `[~]`, and their pointers are lane assertions. None can be checked fully by a non-author from this round's bytes. No `[x]` was written. Promotion is operator-owned."

  Round 42's non-author pass improved that round's admit/reject discernment. It did not write `[x]` on these four boxes. Round 43's own spot-check is still the pending sentence in F2.

## Conflicts for the L1

None observed that falsify "this round can only mark them `[~]`".

Not a conflict, recorded so it is not smoothed: a non-author has, in earlier rounds, checked that a fleet report's SHONEN heading had four `[~]` lines (F5). That is a heading-presence check, not a signature of the promotion boxes, and it is not a round-43 file. If "signed" were read as "any non-author has ever written the word SHONEN," F5 would be the opposing lines. This seat does not adopt that reading. The boxes in `SHONEN.md` remain `[~]`.

## Touched surfaces

- Written: `.ufo/waves/round-43/w1/ScribeShonen.md` (this file only).
- Read: `SHONEN.md`; `corpus/lessons/round-43.md` (including lines 58–60); `SCORECARD.md` Round 43 verdict line; `LOG.md` lines 500–511 and 865 (historical `[~]` hold, not a round-43 signature); verifier spot-check lines quoted in F5; pointer existence via `os.path`.
- Not modified: `SHONEN.md`, lane production files, git index, jj state, fleet repo, sibling repos, `/home/vgpnk/Projects/shokuknow`.

## Out of scope

- C1, C2, C3 counters and their `--flip` / missing-tool controls (other seats). Not run. Not passed by this seat.
- `bash tools/research-gate.sh --selftest` (box 3's cited command; another seat owns the no-harm gate). Not run.
- Whether the four boxes would pass a non-author check of decision tables, LOG round 9, the r25 battery, or `PROVINCE.md` accuracy. Pointer existence is not that check.
- Fleet report `.ufo/reports/round-43/` if any. Not opened. This seat did not search outside the lane for an external signature.
- Rule R43-SPLIT and the 1/2 bound. Not retuned. Not recomputed.
- Editing `SHONEN.md` to `[x]` or to `[~]`. Forbidden, and would be self-attestation.

## Known limits

- Mark counts are a byte count of the three tokens in `SHONEN.md`, not a parse of nested checklists. The file is 12 lines and the four list marks are the only checklist marks.
- `git status --porcelain -- SHONEN.md corpus/lessons/round-43.md` printed no lines. That is cleanliness of those two paths, not a full-tree status.
- Historical LOG lines ("SHONEN 0/4 hold", "never `[x]`") are round-11/round-25 ledger text. They support the standing rule. They are not a round-43 measurement.

## Exact commands and observed output

1. `git rev-parse HEAD && git status --porcelain -- SHONEN.md corpus/lessons/round-43.md && git log -1 --format='commit %H%nsubject %s%ndate %aI' -- SHONEN.md && git ls-files --error-unmatch SHONEN.md && test ! -e corpus/lessons/round-43-verifier-spotcheck.md && echo 'NO_ROUND43_VERIFIER_SPOTCHECK=1'` plus a Python byte/sha/mark count of `SHONEN.md`. Combined stdout, verbatim:

```
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
commit d8c8cff3923f10481ac9ced66d0af7c41d38130c
subject round-25: land verify-metadata gate omitted from integration checkpoint; canonical SHONEN form
date 2026-10-21T04:35:31-03:00
SHONEN.md
NO_ROUND43_VERIFIER_SPOTCHECK=1
bytes 868
sha256 6cebe10f9b2a855447c3cc4e06a8e846c09912285e0c89b79e02854a290e2e71
marks 4 0 0
```

Porcelain printed nothing between the HEAD hash and the `commit d8c8cff…` line.

2. Pointer kind check, then `git diff --quiet -- SHONEN.md` and `git merge-base --is-ancestor d8c8cff3923f10481ac9ced66d0af7c41d38130c HEAD`. Stdout, verbatim:

```
file	SKILL.md
file	corpus/knowledge/metadata-screen-r25.md
file	LOG.md
dir	corpus/fixtures/archives-r9
file	tools/research-gate.sh
file	corpus/evidence/round25-measure-after.log
file	corpus/evidence/round25-meta-differential.log
file	PROVINCE.md
file	.ufo/waves/round-25/build/ConnectorMetaSiblings.md
missing	corpus/lessons/round-43-verifier-spotcheck.md
SHONEN_DIFF_EXIT=0
SHONEN_COMMIT_ANCESTOR_EXIT=0
```

## Artifact paths

- Checklist read: `SHONEN.md`
- Round-43 pending sentence: `corpus/lessons/round-43.md` lines 58–60
- Report: `.ufo/waves/round-43/w1/ScribeShonen.md`

Report: .ufo/waves/round-43/w1/ScribeShonen.md
