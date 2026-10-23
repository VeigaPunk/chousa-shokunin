/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
Attack C2's stated limit and the renamed control.
# Attack
1. Build the call-for-show engine: query the recorder with the record's span, discard the answer, then
   answer by exact search. Score it with /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py (seed 36331). State whether it is separated (expected,
   per claims.md's limit) and what that means for P2's reading.
2. Try to make a LEGITIMATE refactor fail: rename the matcher functions AND move the argv construction
   into a helper; check `RENAMED=pass` still holds. A false kill is a C2 defect.
3. Try to forge an argv log line from inside the gate (the stated anti-instrumentation limit) and state
   whether P2 still passes — if yes, that is a MEETS.
# Acceptance
Three scored attempts with commands and labels; a verdict line per attempt.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/CritC2CallForShow.md
