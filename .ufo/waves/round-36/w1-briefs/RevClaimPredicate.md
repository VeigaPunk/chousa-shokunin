/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/claims.md P1/P2 versus the two counters' code.
# Review
1. Extract P1's sentence, label string, threshold and exit condition; compare to c1-count.py's LABEL,
   the pass computation and `predicate_holds`.
2. Same for P2 (four fields: WITNESS_PER_RECORD, OUTPUT_EQUIV, LANDED_ATTRIB, RENAMED).
3. Report any divergence of wording, threshold, or field name — a claim whose prose and code disagree
   is a calibration defect.
# Acceptance
Two-column comparison table (claim prose vs code line) + a "same sentence?" verdict per claim.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/RevClaimPredicate.md
