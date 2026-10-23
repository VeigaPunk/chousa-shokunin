/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
One falsifiable hypothesis about /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py: the fourteen scenarios do NOT leak state into each other.
# Probe
1. Read how each scenario builds its fixture (TMP dir, manifest path, PATH, env). Name every resource
   a scenario could share with the next (manifest file, temp dir, exported variables).
2. Hypothesis: "every scenario is hermetic — its verdict is unchanged when run in a different order or
   alone". Test it by running the counter on the landed gate with seed 36351 and comparing per-scenario
   verdicts to a single-scenario run if the counter can select one; if it cannot, prove hermeticity by
   inspection plus one experiment: poison a parallel process's environment variable the counter reads
   and show it does not move any verdict.
3. State the hypothesis, the observation, and whether it was falsified. A falsified hypothesis is a
   real finding about the counter, not a failure.
# Acceptance
Hypothesis line, experiment command(s), observed per-scenario verdicts, falsified yes/no with reason.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch except your single labrat.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/LabScenarioIsolation.md
