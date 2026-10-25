# W2ExecShonen — round 44 wave 2

Seat: executor leaf. Task: paste the four checkbox lines of `SHONEN.md` and confirm none is `[x]`. Axes: operability, calibration, depth.

Method: read-only. No network, no fetch, no production edit, no git index or jj write, no commit. This seat did not run the cited selftest, counters, or promotion checks. The only file written is this report.

## Axes

1. Operability — extract the checkbox lines with a command and quote the output. An unrun check has not passed.
2. Calibration — `[~]` is not `[x]`. Pointer existence is not a pass. A prior spot-check of a report heading is not a mark on this file.
3. Depth — separate the four checkbox lines from the four indented evidence lines, and count marks in the file bytes.

## Four checkbox lines

Source: `/home/vgpnk/Projects/shokunin/chousa-shokunin/SHONEN.md`. These are the only lines that start with `- [`. Quoted exactly:

```
- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
- [~] At least one end-to-end domain task executed and logged in LOG.md
- [~] Instructions executable by an agent without oral context
- [~] No cross-domain bleed (PROVINCE.md still accurate)
```

None is `[x]`. All four marks are `[~]`. There is no `[ ]`.

## Command output

```
path=/home/vgpnk/Projects/shokunin/chousa-shokunin/SHONEN.md
bytes=868 lines=12 sha256=6cebe10f9b2a855447c3cc4e06a8e846c09912285e0c89b79e02854a290e2e71
checkbox_count=4
L5	- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
L7	- [~] At least one end-to-end domain task executed and logged in LOG.md
L9	- [~] Instructions executable by an agent without oral context
L11	- [~] No cross-domain bleed (PROVINCE.md still accurate)
marks x=0 tilde=4 empty=0 other=0
none_is_x=yes
043f19a1db91288947493d9f879e61e7a9f07241
d8c8cff3923f10481ac9ced66d0af7c41d38130c 2026-10-21 04:56:16 -0300 round-25: land verify-metadata gate omitted from integration checkpoint; canonical SHONEN form
diff_exit=0
```

Second scan, same file bytes:

```
count '[x]'=0
count '[X]'=0
count '[ ]'=0
count '[~]'=4
count '[x ]'=0
count '[ x]'=0
L5 mark_bytes=b'[~]' line=- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
L7 mark_bytes=b'[~]' line=- [~] At least one end-to-end domain task executed and logged in LOG.md
L9 mark_bytes=b'[~]' line=- [~] Instructions executable by an agent without oral context
L11 mark_bytes=b'[~]' line=- [~] No cross-domain bleed (PROVINCE.md still accurate)
```

Git pins on the same file (quoted; empty porcelain means no output before the exit echo):

```
porcelain_exit=0
diff_HEAD_index_or_work_exit=0
SHONEN.md
ancestor_exit=0
043f19a1db91
```

`git status --porcelain -- SHONEN.md` printed nothing. `git diff --exit-code -- SHONEN.md` printed nothing and exited 0. `git ls-files -- SHONEN.md` printed `SHONEN.md`. `git merge-base --is-ancestor d8c8cff3923f10481ac9ced66d0af7c41d38130c HEAD` exited 0. Working tree matches the index for this path. Last commit that touched it is still the round-25 canonical form. This seat did not change the file.

## Not checkbox lines

The file has 12 lines. The other eight are the title, the blank lines, the requirement sentence, and four indented evidence lines. Those evidence lines are not boxes and were not counted as checkboxes:

```
L6	  `SKILL.md` Gates table; `corpus/knowledge/metadata-screen-r25.md` (lane assertion; no non-author verifier)
L8	  `LOG.md` Round 9 archive verification; `corpus/fixtures/archives-r9/`; r25 explicit-root hold battery (lane assertion)
L10	  `bash tools/research-gate.sh --selftest`; `corpus/evidence/round25-measure-after.log`, `round25-meta-differential.log` (lane assertion)
L12	  `PROVINCE.md`; `corpus/knowledge/metadata-screen-r25.md` Limits; `.ufo/waves/round-25/build/ConnectorMetaSiblings.md` (lane assertion)
```

Only the first evidence line contains the words `no non-author verifier`. Lines 8, 10, and 12 say `(lane assertion)` only. That wording difference does not change the marks. All four marks are `[~]`.

## What this confirmation is not

- Not a promotion. Header sentence, quoted: `Promotion to shokunin requires all of:`. None of the four required boxes is `[x]`, so the file does not record promotion.
- Not a pass of the cited checks. This seat did not run `bash tools/research-gate.sh --selftest` and did not re-read the cited logs.
- Pointer kinds, classified only, not executed:

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
existence_is_not_a_pass=1
selftest_not_run=1
```

- Not a retune of frozen claims. `corpus/evidence/round44/claims.md` has no `SHONEN` token. C1, C2, and C3 there were not re-scored here.
- Not a non-author signature. This seat is a lane-dispatched leaf. `corpus/lessons/round-43-verifier-spotcheck.md:18` says the round-43 fleet report heading had four `[~]` lines and that promotion was not exercised. That sentence checks a report heading. It does not write `[x]` into `SHONEN.md`. The file sha256 above matches the bytes already recorded for this path in `.ufo/waves/round-43/w1/ScribeShonen.md`.

## Finding

Confirmed. The four checkbox lines are the block above. None is `[x]`. Count in file bytes: `[~]`=4, `[x]`=0, `[ ]`=0.
