/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
C1 arms S13/S14 — pin echo isolation and the drift token; plus repair R1's `--pin` env scrub.
# Run
1. Baseline with `CHOUSA_GREP_PIN_ECHO=1` then `--drift` WITHOUT the variable: confirm the baseline
   receipt does not contain `GATE_GREP:` (R1) and drift prints `GATE_DRIFT: -LINE` or clean.
2. Set the echo variable in the environment of the `--pin` call itself; confirm the captured baseline
   still has no echo line (the scrub).
3. Inject a `GATE_GREP:` line into a copy of the baseline and run `--drift`: confirm the diagnostic
   names the token (`gate_drift_line_id` / repair R2) rather than `-LINE`.
Record each command, exit, and the exact output line. Use the gate's own usage output to find the
--pin/--drift syntax; never guess a mode.
# Acceptance
Three numbered runs with the deciding lines; state whether S13/S14 hold on the landed gate.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch except your single labrat.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ExecPinEchoDrift.md
