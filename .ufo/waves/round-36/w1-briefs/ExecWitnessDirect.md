/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

# Target
The witness tool /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py run directly, plus its own log format.
# Run
```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && WITNESS_TMP=/tmp/hyaku/chousa-r36/w1/ExecWitnessDirect timeout 1800 python3 tools/argv-witness.py \
  --gate tools/research-gate.sh --seed 36341 --json /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecWitnessDirect/witness-s36341.json
```
1. Record exit, the summary line (records attributed / total / output match).
2. Find the recorder log in your scratch tree; show its structure (`tr '\0' '\n'`), and quote one
   representative matcher argv in full for one record, confirming it carries `-a -z -b -o -P` and the
   record's span (or its first 4096 bytes).
3. Confirm the log name/marker are drawn outside the gate's environment (show the code path).
# Acceptance
Report: exit, attributed/total, the quoted argv (abbreviate the span with its length + sha256), and
the code cites for channel independence.

# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/<YourName>/ only. Do not commit. Time box 35 minutes.

Lane bounds: leaf member — no subagent dispatch except your single labrat.
Judged on: operability, calibration
Milestone: round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts

Report: write your scoped findings to .ufo/waves/round-36/w1/ExecWitnessDirect.md
