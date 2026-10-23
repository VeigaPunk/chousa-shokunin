# ScribeLesson — round 36, wave 1

## Behavior and findings

Drafted the round-36 lesson skeleton at `.ufo/waves/round-36/w1/ScribeLesson/lesson-draft.md`. It contains a three-row `## Mistakes` table, the current `git status` output, provisional S069/S070 teaches, rejected-source methods, and a spot-check placeholder naming wave cross-check seats.

- **C2 counter-docstring drift — confirmed from committed bytes.** `c2-count.py:36-39` says “separates only 3/5 (V3 and V5 pass it).” The committed legacy receipt reports `matched: 2`, `total: 5`, `predicate_holds: false`, and `landed_attrib: absent` (`.ufo/waves/round-36/measure/c2-before-legacy-s36001.json:16-20`). Its variant entries show V2, V3, and V5 each have `exit: 0` and `witness: pass` (`:37-48`, `:50-61`, `:76-87`). Thus the docstring count and listed pass variants do not match the receipt. No counter was rerun.
- **Attempt-1 `__pycache__` debris — not verified at wave start.** The one status command below was run after wave start and has no entry for `corpus/evidence/round36/__pycache__`; a path glob returned “Path not found.” The two opened wave stderr files are empty, not start snapshots. This cannot establish whether residue existed earlier or whether a crash caused it. The draft preserves the complete status output and does not assert the historical allegation as fact.
- **Attempt label — discrepancy observed, intent unknown.** `claims.md:3` says “Attempt: 1.” while `.ufo/waves/round-36/w1-spec.json:3` says “round-36 attempt 2 wave 1”. The draft recommends making frozen-claim reuse explicit without editing the frozen claims.

## Gates and scope

No C1/C2 counter, gate, selftest, or P1/P2 predicate was executed or scored by this scribe. This is a source/receipt cross-check and lesson draft only; therefore no gate SHA is claimed as a scored measurement. No network, package manager, install, subagent, or git/jj write operation was used. Production files and committed receipts were read-only. The wave-start debris allegation remains unverified; intent behind the attempt-label mismatch is unknown. S069/S070 one-line teaches are explicitly provisional pending their source seats' manual citations.

## Commands and deciding output

Commands executed (verbatim; exit codes observed):

1. `timeout 900s git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --short --untracked-files=all` — exit 0. Deciding observation: the complete output, reproduced in the draft, contains no `corpus/evidence/round36/__pycache__` entry. This is a current snapshot only, not evidence of wave-start state.
2. `timeout 900s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeLesson/lesson-draft.md` — exit 0; output: `67a3820321c626a2142249168f0b533a3071eaaef5da3a05c824bc5e38ef9781  /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeLesson/lesson-draft.md`.

Search/tool operations: searched the lane for `S069|S070`, and searched `w1-spec.json` for the cross-check seat names listed in the draft. A glob of `corpus/evidence/round36/__pycache__` returned `Path not found`. No other shell command was run.

## Files opened or searched (access date: 2026-10-23)

Read:
- `/home/vgpnk/.agents/skills/godspeed/SKILL.md`
- `.ufo/waves/round-36/w1-briefs/ScribeLesson.md`
- `corpus/evidence/round36/claims.md`
- `corpus/evidence/round36/c1-count.py`
- `corpus/evidence/round36/c2-count.py`
- `tools/argv-witness.py`
- `tools/mechanism-witness.py`
- `.ufo/waves/round-36/measure/c2-before-legacy-s36001.json`
- `.ufo/waves/round-36/w1-run.err`
- `.ufo/waves/round-36/w1-plan.err`
- `.ufo/waves/round-36/w1-spec.json` (including a JSON query for seat names)
- `.ufo/waves/round-36/w1-briefs/ScribeSrcGrep.md`
- `.ufo/waves/round-36/w1-briefs/ScribeSrcSha.md`
- The created `w1/ScribeLesson/lesson-draft.md` was read for its cited lines before the path correction.

Search results additionally surfaced these lane files for S069/S070: `.ufo/waves/round-36/gen-w1-spec.py`, `.ufo/waves/round-36/w1-dispatch.json`, `.ufo/waves/round-36/w1-taskcall.json`, `.ufo/waves/round-36/w1-briefs/ScribeKnowC1.md`, `.ufo/waves/round-36/w1-briefs/ScribeKnowC2.md`, `.ufo/waves/round-36/w1-briefs/ScribeLesson.md`, `.ufo/waves/round-36/w1-briefs/ScribeSrcGrep.md`, and `.ufo/waves/round-36/w1-briefs/ScribeSrcSha.md`. Directory enumeration also showed the round-36 evidence directory and wave artifact directory; the absent `__pycache__` target is noted above.

## Touched surfaces and artifact

Created only the requested draft under the scribe artifact directory and this report. No product, judge, claim, counter, witness, receipt, gate, or Git-index files were changed by this scribe. The status output records pre-existing/unattributed `.gitignore` modification and concurrent wave artifacts; they are not claimed as this scribe's work.

- `.ufo/waves/round-36/w1/ScribeLesson/lesson-draft.md` — SHA-256 `67a3820321c626a2142249168f0b533a3071eaaef5da3a05c824bc5e38ef9781`
- `.ufo/waves/round-36/w1/ScribeLesson.md` — this report, written once at the requested path.

**Verdict:** C2 docstring/receipt mismatch confirmed; alleged wave-start `__pycache__` residue not independently verified; attempt-1/attempt-2 metadata mismatch observed with intent unknown. Lesson draft complete. C1/C2 claim predicates remain untested by this scribe.
