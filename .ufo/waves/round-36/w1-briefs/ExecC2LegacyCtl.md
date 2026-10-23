/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
The before-state for C2: the round-35 witness /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py scored by the round-36 counter on the base gate.
# Run
```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && C2_TMP=/tmp/hyaku/chousa-r36/w1/ExecC2LegacyCtl timeout 1800 python3 corpus/evidence/round36/c2-count.py \
  --gate .ufo/waves/round-36/controls/base-gate-r36.sh --witness tools/mechanism-witness.py \
  --seed 36321 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2LegacyCtl/c2-before-legacy-s36321.json
```
1. Record label, matched, output_equiv, landed_attrib, renamed, and per-variant witness/output.
2. State EXACTLY which variants the legacy witness separated and which passed it.
3. Compare those facts to the counter's docstring sentence about the legacy battery AND to
   claims.md's "Before" paragraph; report every numeric or attribution mismatch with line cites.
# Acceptance
Command/exit/label/receipt sha + "separated: <list>; passed: <list>" + a mismatch table.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch except your single labrat.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ExecC2LegacyCtl.md
