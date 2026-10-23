/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
C2 counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py against the landed gate and witness.
# Run
```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && C2_TMP=/tmp/hyaku/chousa-r36/w1/ExecC2FreshA timeout 1800 python3 corpus/evidence/round36/c2-count.py \
  --gate tools/research-gate.sh --witness tools/argv-witness.py --seed 36301 \
  --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2FreshA/c2-after-s36301.json
```
Record stdout/stderr/exit/elapsed and the receipt's fields: matched, output_equiv, landed_attrib,
renamed, witness_sha256, gate_sha256, predicate_holds. Confirm both tool hashes against the commit.
# Acceptance
Command/exit/label/receipt sha + the per-variant table (V1-V6: witness result, output match/total).

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch except your single labrat.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ExecC2FreshA.md
