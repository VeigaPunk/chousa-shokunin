/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
Draft `.ufo/waves/round-36/w1/ScribeLesson/lesson-draft.md`: the round-36 lesson skeleton.
# Draft
1. `## Mistakes` — a table (class · evidence pointer · captured-by · fix) with at least these two
   candidates, each re-verified by you against the files (do not take them on trust):
   (a) number-drift/attribution in `corpus/evidence/round36/c2-count.py`'s docstring: it states the
       round-35 witness "separates only 3/5 (V3 and V5 pass it)" while the committed legacy receipt
       (/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/measure/c2-before-legacy-s36001.json) reports matched=2/5 with V2 and V3 passing — quote the
       docstring lines and the receipt fields;
   (b) attempt-1 landing debris: an untracked `corpus/evidence/round36/__pycache__` in the lane at wave
       start (show `git status` output you ran), i.e. a crash left untracked build residue.
   Add any third you can verify from the wave's own evidence, else say you found none.
2. `## Gate` skeleton — rows to be added (S069, S070 with their one-line teaches), the rejects to be
   recorded (at least the two that were considered and refused, e.g. reading only the local copy
   without recording file sha; or a network grep/POSIX page not opened), and a spot-check placeholder
   line naming this wave's cross-check seats.
Keep every claim falsifiable and cite paths/lines.
# Acceptance
Lesson draft with a filled `## Mistakes` table (2-3 rows, each with quoted evidence) and a `## Gate`
skeleton naming rows, rejects and the spot-check pointer.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ScribeLesson.md
