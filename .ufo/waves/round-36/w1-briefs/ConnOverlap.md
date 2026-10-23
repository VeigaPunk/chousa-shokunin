/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
Sibling-overlap scan: is per-record argv attribution or the engine-swap canary already held elsewhere in
the fleet?
# Scan
Grep sibling lane repos under /home/vgpnk/Projects/shokunin/*-shokunin for: `argv-witness`,
`ENGINE_SWAP_CANARY`, `WITNESS_PER_RECORD`, `RESEARCH_GATE_GREP`, `mechanism-witness`, `PS4` witness
channels, `canary`. Also search `.ufo/reports/` for the same tokens.
# Acceptance
Table: token · repo · path:line · verdict (fleet-unique / reused pattern / contested scope). State
which lane would own it if contested (PROVINCE.md basis) and whether this round duplicates work.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ConnOverlap.md
