/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
The pin/drift contract: `grep_pin_init`, the echo, `--pin`, `--drift`, `gate_drift_line_id`.
# Review
1. Read the code paths; state where the echo is written (fd), whether it can reach a receipt, stdout
   consumed by a caller, or a JSON field.
2. Check the `--pin` capture environment scrub (R1): enumerate every variable that changes the echo or
   drift output and confirm each is scrubbed; name any variable not scrubbed.
3. Check the two selftest cases 260/261 actually exercise the scrub and the token; quote the lines.
# Acceptance
Table of variables → scrubbed? → evidence line. Verdict: contract sound or the exact hole with a
reproducing command.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/RevPinContract.md
