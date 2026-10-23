/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
`/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` selftest, normal and C locale.
# Run
1. `timeout 1800 bash tools/research-gate.sh --selftest` → expect `PASS (261 cases, 0 skipped)`.
2. `LC_ALL=C timeout 1800 bash tools/research-gate.sh --selftest` → expect the same PASS (repair R4).
3. Run `--selftest` once more with `TMPDIR` pointed inside your scratch dir and report the case count.
Capture the last 8 lines of each run and the exit code. A non-PASS line is a no-harm finding.
# Acceptance
Three runs: command, exit, tail, case count. Verdict: no-harm holds or is harmed (name the case).

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch except your single labrat.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ExecSelftest.md
