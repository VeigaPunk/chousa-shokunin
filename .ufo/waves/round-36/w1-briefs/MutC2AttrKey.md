/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
Prove the per-record attribution key is load-bearing in /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py.
# Mutate
In scratch (never edit the lane): patch a COPY of argv-witness.py twice —
 (a) collapse per-record attribution to a global count (any matcher argv counts for every record);
 (b) require only a prefix of the span (first 64 bytes) in the argv.
Score each mutant with /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py (seed 36341/36351) and record the label + which variants it now admits.
A mutant that still scores 5/5 means the counter does not measure per-record attribution.
# Acceptance
Two mutants: patch diff, receipt, label, variant table. Verdict per mutant: load-bearing or not.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/MutC2AttrKey.md
