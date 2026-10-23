/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py.
# Check
Read it whole. For each of the 14 scenarios report: scenario id/name, the fixture it builds, the
assertion it makes, the pass condition, and the line numbers. Then name, with reasons, any scenario
that could pass without the gate behaving correctly (vacuous pass), and any scenario whose fixture
weakens the claim (e.g. compares only an echo string).
# Acceptance
14-row table + a "vacuity candidates" section naming at most 3 with line cites. State the counter's
own reference/sanity guards and whether they can be satisfied trivially.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ScoutC1Counter.md
