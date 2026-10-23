/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
C1 arm S12 — `json_unescape` under `LC_ALL=C` (repair R4).
# Run
1. Read `json_unescape` in the landed gate (line numbers) and state how it decodes UTF-8 now.
2. Build a minimal JSONL record whose claim text carries `\u00e9`; run the mode that decodes claims
   (find it in usage) under `LC_ALL=C` on the landed gate and on the base control gate.
3. Show the landed output containing the decoded character (`é`) and the base output's failure text.
   Verify with `LC_ALL=C printf` that the byte sequence is the expected two-byte UTF-8.
# Acceptance
Two runs + the decoded-byte proof. State which locale variables you set and whether unsetting them
changes the result (one extra run).

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch except your single labrat.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ExecLocaleDecode.md
