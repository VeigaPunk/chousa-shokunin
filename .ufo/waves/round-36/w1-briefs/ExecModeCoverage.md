/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
Repair R6 — the pin-coverage ledger: `verify-integrity` and `verify-sweeps` run no matcher grep.
# Run
1. Find the ledger row(s) that state this (SKILL.md and/or gate comments) with line cites.
2. Prove it for the LANded gate: run `verify-integrity` and `verify-sweeps` on a small fixture with
   `RESEARCH_GATE_GREP` pointing at a recorder script that logs each call; count calls. If the
   recorder route is unavailable for a mode, use `CHOUSA_GREP_PIN_ECHO=1` and state what it does and
   does not prove.
3. State whether the claim ("run no matcher grep") is true, false, or not measurable, with the count.
# Acceptance
Per mode: command, exit, observed recorder call count, line cites for the ledger claim, verdict.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch except your single labrat.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ExecModeCoverage.md
