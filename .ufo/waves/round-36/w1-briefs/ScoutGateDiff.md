/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
Base control gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh (a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad) versus the landed gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh (a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8).
# Check
1. `diff -u` the two files; enumerate EVERY hunk with landed line numbers and a one-line classification
   (functional / selftest case / comment / whitespace).
2. For each functional hunk, name which claims.md item it serves (C1 arm S1-S14, C2, repair R1-R6) or
   state "not tied to a declared item".
3. Flag any edit that changes behaviour on a gate mode claims.md does not name, and any hunk that
   touches a matcher call site without going through the pin wrapper.
# Acceptance
Table: hunk · line range · class · tied item · risk. End with the count of functional hunks and of
untied hunks.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ScoutGateDiff.md
