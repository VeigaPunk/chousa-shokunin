/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
Attack C1's separation: can an engine score 14/14 while skipping the claimed work?
# Attack
In scratch, build a gate whose dead-zone matcher is replaced by an exact search AND which fakes
whatever the counter's scenarios read (echo line, recorder argv, manifest hash) — i.e. the strongest
output-equivalent engine you can write inside the time box. Score it with /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py (seed 36331+).
Also try the reverse: a CORRECT gate that the counter kills (false negative).
# Acceptance
Two scored attempts with commands, receipts and labels. MEETS (score >=14 with the work skipped), or
the wall that stopped you named precisely (which scenario, which assertion, why it cannot be faked).

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/CritC1Swap.md
