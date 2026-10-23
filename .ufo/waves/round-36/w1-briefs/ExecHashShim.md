/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
C1 arm S11 — manifest hash identity under a hostile `sha256sum` (repair R3).
# Run
1. In scratch build a PATH dir whose `sha256sum` prints a fixed fake digest for every argument and
   exits 0; put it FIRST on PATH.
2. Run `verify-all --json` (find the exact mode name in the gate's usage) against a small fixture with
   the hostile PATH, on the landed gate and on the base control gate. Record exit, stdout tail, and
   whether recorded `record_sha256`/`gate_sha256` fields are poisoned.
3. Confirm the landed gate's refusal is named (which marker/exit code?) and that it refuses BEFORE
   appending a manifest line (show the manifest is unchanged).
# Acceptance
Two runs (landed, base) with command/exit/output lines; the arm's pass condition and whether it holds.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch except your single labrat.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ExecHashShim.md
