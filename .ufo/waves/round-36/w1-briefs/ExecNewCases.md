/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
The five new selftest cases 257-261 (repair R5), and their red-before state.
# Run
1. From the base control gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh, list its selftest case names/labels (`grep -n` the case
   table or run `--selftest` and capture labels 250-261 if present). State whether 257-261 exist there.
2. Show, for each of the five, the landed case body (line numbers) and what it asserts (one line each):
   258 claims-locale-boundary, 259 all-manifest-hash-shim, 260 pin-echo-isolation, 261
   pin-drift-grep-token, 257 (name it).
3. Copy the landed case bodies into a scratch copy of the BASE gate one at a time (or the minimum
   harness needed) and record whether each case FAILS on the base behaviour. If a case cannot run
   against the base gate, state exactly what is missing instead of guessing.
# Acceptance
Table: case · landed assert · exists on base? · fails on base? (observed command/exit or "not
runnable: reason"). This is the red-before evidence; do not claim a failure you did not observe.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch except your single labrat.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ExecNewCases.md
