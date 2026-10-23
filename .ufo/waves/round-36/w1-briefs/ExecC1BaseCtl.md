/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
The before-state: base control gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh.
# Run
1. `sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh` must equal a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad; if not, stop and report that mismatch.
2. ```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && C1_TMP=/tmp/hyaku/chousa-r36/w1/ExecC1BaseCtl timeout 1800 python3 corpus/evidence/round36/c1-count.py \
  --gate .ufo/waves/round-36/controls/base-gate-r36.sh --seed 36321 \
  --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1BaseCtl/c1-before-s36321.json
```
3. Name which scenarios fail and check each against claims.md's S11-S14 description.
# Acceptance
Receipt sha + label (expected `ENGINE_SWAP_CANARY=10/14`) + failing scenario ids + whether the four
failures match S11, S12, S13, S14 one-for-one.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch except your single labrat.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ExecC1BaseCtl.md
