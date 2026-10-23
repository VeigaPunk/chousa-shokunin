/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
New SOURCES row S070 — coreutils `sha256sum(1)`, digest shape and `--check` (repair R3's pin).
# Open
Read `/usr/share/man/man1/sha256sum.1.gz` locally. Record package version (`pacman -Q coreutils`,
read-only), file sha256, section names, and the exact sentence stating the 256-bit / 64-hex output
shape and what `--check` reads.
# Draft
Write `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeSrcSha/row-draft.md`: the 11-cell row (S070, source `GNU coreutils sha256sum(1) —
/usr/share/man/man1/sha256sum.1.gz`, kind docs, tier A, scope = the digest text format and --check
input, anchor with decompressed lines, teaches one grounded sentence, status mined, opened 2026-10-23,
recheck on-release, used-by corpus/knowledge/engine-swap-canary-r36.md) + `## Gate` entry with access
date and ONE located quote <=25 words with line numbers. State what the page does NOT say (it does not
define a validation policy, so the gate's 64-lowercase-hex rule is the lane's choice [INFERENCE]).
# Acceptance
Row draft + Gate entry + sha256 + located quote with lines.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ScribeSrcSha.md
