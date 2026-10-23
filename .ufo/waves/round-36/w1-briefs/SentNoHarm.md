/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
No-harm on the previously pinned observables after the round-36 gate edits.
# Run
From /home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md find the pinned observable commands (claims VERDICT_BEARING_CLAIMS 17/17, chain
RESOLVED_HOPS 17/22, broken control 1/2, r1 archives VERDICT_BEARING_EXPORTS 3/3). Re-run each on the
landed gate against the same fixtures the runbook names; a fixture lives under
`../research/deep-research-2026-09-28/` or the lane's own test data — use the runbook's exact paths.
# Acceptance
One table: observable · expected (r35 recorded value) · observed · pass/harm. Any drift is a no-harm
finding (name the exact value and command). Include the commands verbatim.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/SentNoHarm.md
