/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
Inherited attempt-1 state in the lane: `corpus/evidence/round36/` and `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain`.
# Check
1. Show the untracked path(s), list the files, and `file` each: are they bytecode only? Any source,
   receipt or artifact inside?
2. Compare the tracked contents of `corpus/evidence/round36/` against the freeze commit 700bd5fcbf9abc118a6a0f078d51a2e7460c2878
   (`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin ls-tree -r --name-only 700bd5fcbf9abc118a6a0f078d51a2e7460c2878 -- corpus/evidence/round36`), byte-compare with
   `git show` where a diff is possible.
3. Say per item: reuse (re-verified this round) or discard, and why. Do NOT delete anything.
# Acceptance
Item table: path · tracked? · content class · reuse/discard + reason. State explicitly whether the
untracked debris contains any authored work.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ScoutInherited.md
