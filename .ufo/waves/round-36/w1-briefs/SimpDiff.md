/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
YAGNI pass over the landed round-36 gate diff (base control → landed gate) and the new tool /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py.
# Review
1. List anything in the diff that no claim arm or repair needs: duplicated helper, dead branch,
   defensive check that cannot fire, comment that overstates.
2. Same for argv-witness.py: functions/fields/CLI options never exercised by the counter or a useful
   direct run (show the usage counts you measured).
3. For each, state the smallest deletion that preserves verified behaviour — propose only, do not edit.
# Acceptance
Deletion candidates table (path:line · why unused · verification that still holds). If none, say so
and show the sweep you ran.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/SimpDiff.md
