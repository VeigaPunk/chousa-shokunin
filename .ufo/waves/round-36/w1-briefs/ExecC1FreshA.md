/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
C1 counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py against the landed gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh.
# Run
```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && C1_TMP=/tmp/hyaku/chousa-r36/w1/ExecC1FreshA timeout 1800 python3 corpus/evidence/round36/c1-count.py \
  --gate tools/research-gate.sh --seed 36301 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC1FreshA/c1-after-s36301.json
```
Record stdout, stderr, exit code, elapsed and the receipt's gate_sha256/label/total/predicate_holds.
Then `sha256sum tools/research-gate.sh` and confirm it equals a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8. Re-run once (same seed) only if
the first run errors; a different count on a re-run is itself a finding.
# Acceptance
Report: command, exit, the deciding label line, receipt path+sha256, gate sha. Verdict: P1 arm
measured or not.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch except your single labrat.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ExecC1FreshA.md
