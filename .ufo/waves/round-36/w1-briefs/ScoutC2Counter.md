/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py and /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py.
# Check
Read both. Report: (a) the witness channel (who writes the log, where its name and marker come from,
what the gate can and cannot read); (b) how per-record attribution is keyed; (c) each of the five
variants V1-V5 and the renamed control V6 — the exact patch applied and why it is output-equivalent;
(d) every place the counter passes/fails; (e) the docstring's numeric claims, line by line.
# Acceptance
Sectioned report with line cites. End with the list of docstring numeric claims that the committed
receipts (/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/measure/c2-before-legacy-s36001.json, c2-after-s*.json) do not support.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ScoutC2Counter.md
