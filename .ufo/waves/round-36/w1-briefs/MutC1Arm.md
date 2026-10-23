/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
Prove one C1 arm is load-bearing.
# Mutate
In scratch, patch a COPY of /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py to disable exactly one arm — (a) the manifest hash-pin validation, or
(b) the locale arm — and run it against the landed gate (seed 36341+) and against the base gate.
The mutant must be a counter change, not a gate change; state clearly that the score is then not
evidence for the claim.
# Acceptance
Patch diff + two scored runs + a reading: which arm the count actually rides on, and whether the
committed counter's 14/14 can be explained by fewer than 14 independent behaviours.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/MutC1Arm.md
