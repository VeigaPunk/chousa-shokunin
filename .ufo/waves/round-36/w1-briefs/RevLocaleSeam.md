/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
The locale fix (repair R4) and every other locale-sensitive operation in /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh.
# Review
1. Read `json_unescape` and its `LC_ALL=C` scope; confirm the scope covers the decode and not the
   caller's variables.
2. Sweep the gate for other locale-sensitive constructs: `sort`, `tr`, `cut`, `printf` of non-ASCII,
   `[[:alpha:]]`/bracket classes, `grep` without `LC_ALL=C`, `--` handling of UTF-8 in spans.
3. For each hit name the line, whether a C-locale environment changes its answer, and whether a test
   covers it.
# Acceptance
Findings table (line · construct · locale exposure · covered?) + a verdict: seam closed for decode,
with the remaining exposures named (or a sweep command showing none).

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/RevLocaleSeam.md
