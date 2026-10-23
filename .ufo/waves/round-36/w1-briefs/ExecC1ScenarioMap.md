/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
Per-scenario evidence for the four fixed arms.
# Run
Using seed 36331 against the landed gate, produce a receipt and then, for S11 (manifest hash shim),
S12 (C-locale decode), S13 (pin echo isolation) and S14 (drift token), extract from the receipt the
scenario's own observed detail (whatever the counter records: expected/actual, exit, stderr excerpt).
Then reproduce S11 and S12 BY HAND in your scratch dir: hostile `sha256sum` on PATH for S11; a
`\u00e9` fixture under `LC_ALL=C` for S12. Show the landed gate's named refusal/decoded output and the
base control's failure on the same fixture.
# Acceptance
Four sub-sections, each with the counter's detail + your hand reproduction (command, exit, line).
Mark anything you could not reproduce MEETS-ADJACENT and say why.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch except your single labrat.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ExecC1ScenarioMap.md
