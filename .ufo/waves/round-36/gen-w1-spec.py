#!/usr/bin/env python3
"""chousa round 36 (attempt 2), wave 1 = build + independent re-derivation (36 seats, v1 band).
Usage: python3 gen-w1-spec.py > w1-spec.json"""
import json
import pathlib
import sys

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
WD = f"{LANE}/.ufo/waves/round-36/w1"
SCR = "/tmp/hyaku/chousa-r36/w1"
BASE = "700bd5fcbf9abc118a6a0f078d51a2e7460c2878"
GATE = f"{LANE}/tools/research-gate.sh"
GSHA = "a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8"
BASE_GATE = f"{LANE}/.ufo/waves/round-36/controls/base-gate-r36.sh"
BASE_SHA = "a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad"
CLAIMS = f"{LANE}/corpus/evidence/round36/claims.md"
C1C = f"{LANE}/corpus/evidence/round36/c1-count.py"
C2C = f"{LANE}/corpus/evidence/round36/c2-count.py"
WIT = f"{LANE}/tools/argv-witness.py"
R35WIT = f"{LANE}/tools/mechanism-witness.py"
MEAS = f"{LANE}/.ufo/waves/round-36/measure"
GOD = pathlib.Path.home().joinpath(".agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + GOD + "\n"

CONTEXT = f"""# Goal
chousa lane (deep-research method), round 36, attempt 2, wave 1 of a v1 two-wave shape — build and
independently re-derive the round's two frozen claims. Lane repo {LANE} (jj-colocated, branch master,
HEAD detached; read the tip with `git rev-parse master`). Wave base revision {BASE}; the landed gate
{GATE} has sha256 {GSHA} (verify: sha256sum {GATE}); the pre-round control gate {BASE_GATE} is the
round-35 blob {BASE_SHA}.
Read FIRST, in this order: the frozen claim design {CLAIMS} (two claims, P1/P2, kill rules, stated
limits, repairs R1-R6), then the C1 counter {C1C}, the C2 counter {C2C}, the per-record witness {WIT},
and the round-35 witness {R35WIT} it replaces. Committed receipts: {MEAS}/.
The round's two claims, landed by the L1's construction runs on seeds 36001/36011 (NOT the wave's):
- C1 operability (lowest scored axis, operability 3/10): the gate and its counter separate an
  output-equivalent engine swap in fourteen independent scenarios (PATH shim, BASH_ENV function,
  PATH-less host, relative/missing/non-GNU overrides, distinct-path override honoured and observed,
  default pin with a LIVE --version, override beating an imported shim, per-record argv attribution,
  manifest hash identity under a hostile sha256sum, C-locale decode, and the two pin echo/drift cells).
  P1 = `ENGINE_SWAP_CANARY=14/14` + `predicate_holds=true` on each of two fresh seeds. Before (base
  gate): 10/14 (S11-S14 fail). The cheapest do-nothing control is the base gate itself.
- C2 calibration: `tools/argv-witness.py` scores the matcher PER RECORD through the pinned engine's
  out-of-band argv channel (a distinct-path GNU-reporting recorder as `RESEARCH_GATE_GREP` logs one
  NUL-delimited argv per invocation; each record's own span must appear in a `-a -z -b -o -P` argv),
  separating the five output-equivalent survivors the round-35 witness admitted (python-exact,
  environment-keyed, witness-forge, one-call-for-show, body-replaced) while a renamed matcher passes.
  P2 = `WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass` on two fresh seeds.
  Before (base tree + r35 witness): 2/5, landed attribution absent, renamed fail.
Your job: independently re-derive both claims on FRESH seeds (36301, 36311, 36321, 36331, 36341 — do not
reuse 36001/36011/36021), attack each claim's fixture, and draft the frontier artifacts. A MEETS
finding — an output-equivalent engine that still scores 14/14 or attributes every record, a witness
bypass that passes P2, a scenario that passes without the gate behaving — is the most valuable result;
say exactly why, with the command and the receipt.

# Contract
- Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Write your report once.
  Extra artifacts (receipts, patched gates, logs, drafts) go ONLY inside your own directory
  {WD}/<YourName>/ (create it); keep each artifact under 1 MiB (large logs stay in {SCR}; cite path+sha256).
- Read-only on ALL lane production files (tools/, corpus/, SCORECARD.md, LOG.md, SKILL.md, README.md,
  PROVINCE.md, SHONEN.md, .ufo/waves/round-36/{{controls,measure}}/ …) and on the fleet repo, sibling
  lanes, lane jj state and the lane Git index. No git/jj write commands anywhere; read-only git
  (log/show/diff/status/rev-parse/cat-file) is fine. Experiments only in {SCR}/<YourName>/: copy files,
  or `git clone -q {LANE} <dir> && git -C <dir> checkout -q {BASE}` (unset GIT_DIR/GIT_WORK_TREE/
  GIT_INDEX_FILE first). Counters: set C1_TMP / C2_TMP / WITNESS_TMP / TMPDIR to your scratch dir.
- Pin every gate you score: sha256 it. A receipt whose gate sha256 is neither {GSHA} nor the base
  control {BASE_SHA} nor a control you built and named is not evidence. Never edit the committed
  counters, the witness, the claims file or the gate — a bug is a finding.
- Processes: never signal by name/pattern (no pkill/killall/ps|grep kill loops); keep the PIDs you start
  and kill only those. Disk: {SCR} is on /tmp; do not write to /fast. Network: NONE. Bound every command
  with `timeout` (<=1800 s for selftest/counters, <=900 s otherwise). Leaf seat: no subagents (an
  executor may spawn at most one read-only labrat probe). Do not run `pacman` anything.
- Honesty: report only what you ran or opened; quote commands, exit codes, key output. Mark inference
  [INFERENCE]. Located quotes <=25 words with path + access date 2026-10-23.
- Time box: return within 35 minutes of your start; a partial report with what you verified beats none.
# Tooling directive — operator, 2026-10-19 (always on, every agent)
You may install or update tools that help the task without asking; read /home/vgpnk/.omp/agent/RULES.md
first and record each install (tool, version, channel, reason). All pacman transactions are PAUSED
host-wide: install via `uv tool`/`npx`/an official binary in ~/.local/bin, or file an L0 question; never
`pacman -S/-Sy/-Syu/-U/-R` and never restart a host service."""

TAIL = """
# Acceptance
Your report names: every command you ran (verbatim), its exit code and the line that decides the
answer; every file you opened with the access date; every artifact path + sha256 under
{wd}/<YourName>/; and an explicit verdict line. Read-only on lane production files; your receipts
may be written under {wd}/<YourName>/ only. Do not commit. Time box 35 minutes."""

ITEMS = [
    ("ScoutGateDiff", "scout", f"""# Target
Base control gate {BASE_GATE} ({BASE_SHA}) versus the landed gate {GATE} ({GSHA}).
# Check
1. `diff -u` the two files; enumerate EVERY hunk with landed line numbers and a one-line classification
   (functional / selftest case / comment / whitespace).
2. For each functional hunk, name which claims.md item it serves (C1 arm S1-S14, C2, repair R1-R6) or
   state "not tied to a declared item".
3. Flag any edit that changes behaviour on a gate mode claims.md does not name, and any hunk that
   touches a matcher call site without going through the pin wrapper.
# Acceptance
Table: hunk · line range · class · tied item · risk. End with the count of functional hunks and of
untied hunks."""),
    ("ScoutC1Counter", "scout", f"""# Target
{C1C}.
# Check
Read it whole. For each of the 14 scenarios report: scenario id/name, the fixture it builds, the
assertion it makes, the pass condition, and the line numbers. Then name, with reasons, any scenario
that could pass without the gate behaving correctly (vacuous pass), and any scenario whose fixture
weakens the claim (e.g. compares only an echo string).
# Acceptance
14-row table + a "vacuity candidates" section naming at most 3 with line cites. State the counter's
own reference/sanity guards and whether they can be satisfied trivially."""),
    ("ScoutC2Counter", "scout", f"""# Target
{C2C} and {WIT}.
# Check
Read both. Report: (a) the witness channel (who writes the log, where its name and marker come from,
what the gate can and cannot read); (b) how per-record attribution is keyed; (c) each of the five
variants V1-V5 and the renamed control V6 — the exact patch applied and why it is output-equivalent;
(d) every place the counter passes/fails; (e) the docstring's numeric claims, line by line.
# Acceptance
Sectioned report with line cites. End with the list of docstring numeric claims that the committed
receipts ({MEAS}/c2-before-legacy-s36001.json, c2-after-s*.json) do not support."""),
    ("ScoutReceipts", "scout", f"""# Target
{MEAS}/ (11 committed receipts).
# Check
For every receipt print: file, seed, gate_sha256, label, total/matched, predicate_holds. State the
lowest count per counter against the landed gate ({GSHA}) and any receipt measured against other
bytes (name the file it belongs to). Cross-check the two `before` receipts against {BASE_SHA}.
# Acceptance
One table + a kill-rule reading: "no committed run against the landed gate is lower than <x>".
Name any receipt whose gate_sha256 matches none of the two known gates."""),
    ("ScoutInherited", "scout", f"""# Target
Inherited attempt-1 state in the lane: `corpus/evidence/round36/` and `git -C {LANE} status --porcelain`.
# Check
1. Show the untracked path(s), list the files, and `file` each: are they bytecode only? Any source,
   receipt or artifact inside?
2. Compare the tracked contents of `corpus/evidence/round36/` against the freeze commit {BASE}
   (`git -C {LANE} ls-tree -r --name-only {BASE} -- corpus/evidence/round36`), byte-compare with
   `git show` where a diff is possible.
3. Say per item: reuse (re-verified this round) or discard, and why. Do NOT delete anything.
# Acceptance
Item table: path · tracked? · content class · reuse/discard + reason. State explicitly whether the
untracked debris contains any authored work."""),
    ("ExecC1FreshA", "executor", f"""# Target
C1 counter {C1C} against the landed gate {GATE}.
# Run
```
cd {LANE} && C1_TMP={SCR}/ExecC1FreshA timeout 1800 python3 corpus/evidence/round36/c1-count.py \\
  --gate tools/research-gate.sh --seed 36301 --receipt {WD}/ExecC1FreshA/c1-after-s36301.json
```
Record stdout, stderr, exit code, elapsed and the receipt's gate_sha256/label/total/predicate_holds.
Then `sha256sum tools/research-gate.sh` and confirm it equals {GSHA}. Re-run once (same seed) only if
the first run errors; a different count on a re-run is itself a finding.
# Acceptance
Report: command, exit, the deciding label line, receipt path+sha256, gate sha. Verdict: P1 arm
measured or not."""),
    ("ExecC1FreshB", "executor", f"""# Target
C1 counter {C1C}, second fresh seed.
# Run
```
cd {LANE} && C1_TMP={SCR}/ExecC1FreshB timeout 1800 python3 corpus/evidence/round36/c1-count.py \\
  --gate tools/research-gate.sh --seed 36311 --receipt {WD}/ExecC1FreshB/c1-after-s36311.json
```
Same recording duty as ExecC1FreshA. Additionally diff the per-scenario pass map of your receipt
against {MEAS}/c1-after-s36001.json and name every scenario whose verdict differs.
# Acceptance
Command/exit/label/receipt sha + the scenario-diff list (or "identical pass map")."""),
    ("ExecC1BaseCtl", "executor", f"""# Target
The before-state: base control gate {BASE_GATE}.
# Run
1. `sha256sum {BASE_GATE}` must equal {BASE_SHA}; if not, stop and report that mismatch.
2. ```
cd {LANE} && C1_TMP={SCR}/ExecC1BaseCtl timeout 1800 python3 corpus/evidence/round36/c1-count.py \\
  --gate .ufo/waves/round-36/controls/base-gate-r36.sh --seed 36321 \\
  --receipt {WD}/ExecC1BaseCtl/c1-before-s36321.json
```
3. Name which scenarios fail and check each against claims.md's S11-S14 description.
# Acceptance
Receipt sha + label (expected `ENGINE_SWAP_CANARY=10/14`) + failing scenario ids + whether the four
failures match S11, S12, S13, S14 one-for-one."""),
    ("ExecC1ScenarioMap", "executor", f"""# Target
Per-scenario evidence for the four fixed arms.
# Run
Using seed 36331 against the landed gate, produce a receipt and then, for S11 (manifest hash shim),
S12 (C-locale decode), S13 (pin echo isolation) and S14 (drift token), extract from the receipt the
scenario's own observed detail (whatever the counter records: expected/actual, exit, stderr excerpt).
Then reproduce S11 and S12 BY HAND in your scratch dir: hostile `sha256sum` on PATH for S11; a
`\\u00e9` fixture under `LC_ALL=C` for S12. Show the landed gate's named refusal/decoded output and the
base control's failure on the same fixture.
# Acceptance
Four sub-sections, each with the counter's detail + your hand reproduction (command, exit, line).
Mark anything you could not reproduce MEETS-ADJACENT and say why."""),
    ("ExecC2FreshA", "executor", f"""# Target
C2 counter {C2C} against the landed gate and witness.
# Run
```
cd {LANE} && C2_TMP={SCR}/ExecC2FreshA timeout 1800 python3 corpus/evidence/round36/c2-count.py \\
  --gate tools/research-gate.sh --witness tools/argv-witness.py --seed 36301 \\
  --receipt {WD}/ExecC2FreshA/c2-after-s36301.json
```
Record stdout/stderr/exit/elapsed and the receipt's fields: matched, output_equiv, landed_attrib,
renamed, witness_sha256, gate_sha256, predicate_holds. Confirm both tool hashes against the commit.
# Acceptance
Command/exit/label/receipt sha + the per-variant table (V1-V6: witness result, output match/total)."""),
    ("ExecC2FreshB", "executor", f"""# Target
C2 counter {C2C}, second fresh seed (36311) — same recording duty as ExecC2FreshA, and compare the
per-variant table against {MEAS}/c2-after-s36001.json naming any verdict that differs.
# Acceptance
Command/exit/label/receipt sha + per-variant table + verdict-diff line."""),
    ("ExecC2LegacyCtl", "executor", f"""# Target
The before-state for C2: the round-35 witness {R35WIT} scored by the round-36 counter on the base gate.
# Run
```
cd {LANE} && C2_TMP={SCR}/ExecC2LegacyCtl timeout 1800 python3 corpus/evidence/round36/c2-count.py \\
  --gate .ufo/waves/round-36/controls/base-gate-r36.sh --witness tools/mechanism-witness.py \\
  --seed 36321 --receipt {WD}/ExecC2LegacyCtl/c2-before-legacy-s36321.json
```
1. Record label, matched, output_equiv, landed_attrib, renamed, and per-variant witness/output.
2. State EXACTLY which variants the legacy witness separated and which passed it.
3. Compare those facts to the counter's docstring sentence about the legacy battery AND to
   claims.md's "Before" paragraph; report every numeric or attribution mismatch with line cites.
# Acceptance
Command/exit/label/receipt sha + "separated: <list>; passed: <list>" + a mismatch table."""),
    ("ExecWitnessDirect", "executor", f"""# Target
The witness tool {WIT} run directly, plus its own log format.
# Run
```
cd {LANE} && WITNESS_TMP={SCR}/ExecWitnessDirect timeout 1800 python3 tools/argv-witness.py \\
  --gate tools/research-gate.sh --seed 36341 --json {WD}/ExecWitnessDirect/witness-s36341.json
```
1. Record exit, the summary line (records attributed / total / output match).
2. Find the recorder log in your scratch tree; show its structure (`tr '\\0' '\\n'`), and quote one
   representative matcher argv in full for one record, confirming it carries `-a -z -b -o -P` and the
   record's span (or its first 4096 bytes).
3. Confirm the log name/marker are drawn outside the gate's environment (show the code path).
# Acceptance
Report: exit, attributed/total, the quoted argv (abbreviate the span with its length + sha256), and
the code cites for channel independence."""),
    ("ExecSelftest", "executor", f"""# Target
`{GATE}` selftest, normal and C locale.
# Run
1. `timeout 1800 bash tools/research-gate.sh --selftest` → expect `PASS (261 cases, 0 skipped)`.
2. `LC_ALL=C timeout 1800 bash tools/research-gate.sh --selftest` → expect the same PASS (repair R4).
3. Run `--selftest` once more with `TMPDIR` pointed inside your scratch dir and report the case count.
Capture the last 8 lines of each run and the exit code. A non-PASS line is a no-harm finding.
# Acceptance
Three runs: command, exit, tail, case count. Verdict: no-harm holds or is harmed (name the case)."""),
    ("ExecNewCases", "executor", f"""# Target
The five new selftest cases 257-261 (repair R5), and their red-before state.
# Run
1. From the base control gate {BASE_GATE}, list its selftest case names/labels (`grep -n` the case
   table or run `--selftest` and capture labels 250-261 if present). State whether 257-261 exist there.
2. Show, for each of the five, the landed case body (line numbers) and what it asserts (one line each):
   258 claims-locale-boundary, 259 all-manifest-hash-shim, 260 pin-echo-isolation, 261
   pin-drift-grep-token, 257 (name it).
3. Copy the landed case bodies into a scratch copy of the BASE gate one at a time (or the minimum
   harness needed) and record whether each case FAILS on the base behaviour. If a case cannot run
   against the base gate, state exactly what is missing instead of guessing.
# Acceptance
Table: case · landed assert · exists on base? · fails on base? (observed command/exit or "not
runnable: reason"). This is the red-before evidence; do not claim a failure you did not observe."""),
    ("ExecHashShim", "executor", f"""# Target
C1 arm S11 — manifest hash identity under a hostile `sha256sum` (repair R3).
# Run
1. In scratch build a PATH dir whose `sha256sum` prints a fixed fake digest for every argument and
   exits 0; put it FIRST on PATH.
2. Run `verify-all --json` (find the exact mode name in the gate's usage) against a small fixture with
   the hostile PATH, on the landed gate and on the base control gate. Record exit, stdout tail, and
   whether recorded `record_sha256`/`gate_sha256` fields are poisoned.
3. Confirm the landed gate's refusal is named (which marker/exit code?) and that it refuses BEFORE
   appending a manifest line (show the manifest is unchanged).
# Acceptance
Two runs (landed, base) with command/exit/output lines; the arm's pass condition and whether it holds."""),
    ("ExecLocaleDecode", "executor", f"""# Target
C1 arm S12 — `json_unescape` under `LC_ALL=C` (repair R4).
# Run
1. Read `json_unescape` in the landed gate (line numbers) and state how it decodes UTF-8 now.
2. Build a minimal JSONL record whose claim text carries `\\u00e9`; run the mode that decodes claims
   (find it in usage) under `LC_ALL=C` on the landed gate and on the base control gate.
3. Show the landed output containing the decoded character (`é`) and the base output's failure text.
   Verify with `LC_ALL=C printf` that the byte sequence is the expected two-byte UTF-8.
# Acceptance
Two runs + the decoded-byte proof. State which locale variables you set and whether unsetting them
changes the result (one extra run)."""),
    ("ExecPinEchoDrift", "executor", f"""# Target
C1 arms S13/S14 — pin echo isolation and the drift token; plus repair R1's `--pin` env scrub.
# Run
1. Baseline with `CHOUSA_GREP_PIN_ECHO=1` then `--drift` WITHOUT the variable: confirm the baseline
   receipt does not contain `GATE_GREP:` (R1) and drift prints `GATE_DRIFT: -LINE` or clean.
2. Set the echo variable in the environment of the `--pin` call itself; confirm the captured baseline
   still has no echo line (the scrub).
3. Inject a `GATE_GREP:` line into a copy of the baseline and run `--drift`: confirm the diagnostic
   names the token (`gate_drift_line_id` / repair R2) rather than `-LINE`.
Record each command, exit, and the exact output line. Use the gate's own usage output to find the
--pin/--drift syntax; never guess a mode.
# Acceptance
Three numbered runs with the deciding lines; state whether S13/S14 hold on the landed gate."""),
    ("ExecModeCoverage", "executor", f"""# Target
Repair R6 — the pin-coverage ledger: `verify-integrity` and `verify-sweeps` run no matcher grep.
# Run
1. Find the ledger row(s) that state this (SKILL.md and/or gate comments) with line cites.
2. Prove it for the LANded gate: run `verify-integrity` and `verify-sweeps` on a small fixture with
   `RESEARCH_GATE_GREP` pointing at a recorder script that logs each call; count calls. If the
   recorder route is unavailable for a mode, use `CHOUSA_GREP_PIN_ECHO=1` and state what it does and
   does not prove.
3. State whether the claim ("run no matcher grep") is true, false, or not measurable, with the count.
# Acceptance
Per mode: command, exit, observed recorder call count, line cites for the ledger claim, verdict."""),
    ("RevLocaleSeam", "reviewer", f"""# Target
The locale fix (repair R4) and every other locale-sensitive operation in {GATE}.
# Review
1. Read `json_unescape` and its `LC_ALL=C` scope; confirm the scope covers the decode and not the
   caller's variables.
2. Sweep the gate for other locale-sensitive constructs: `sort`, `tr`, `cut`, `printf` of non-ASCII,
   `[[:alpha:]]`/bracket classes, `grep` without `LC_ALL=C`, `--` handling of UTF-8 in spans.
3. For each hit name the line, whether a C-locale environment changes its answer, and whether a test
   covers it.
# Acceptance
Findings table (line · construct · locale exposure · covered?) + a verdict: seam closed for decode,
with the remaining exposures named (or a sweep command showing none)."""),
    ("RevPinContract", "reviewer", f"""# Target
The pin/drift contract: `grep_pin_init`, the echo, `--pin`, `--drift`, `gate_drift_line_id`.
# Review
1. Read the code paths; state where the echo is written (fd), whether it can reach a receipt, stdout
   consumed by a caller, or a JSON field.
2. Check the `--pin` capture environment scrub (R1): enumerate every variable that changes the echo or
   drift output and confirm each is scrubbed; name any variable not scrubbed.
3. Check the two selftest cases 260/261 actually exercise the scrub and the token; quote the lines.
# Acceptance
Table of variables → scrubbed? → evidence line. Verdict: contract sound or the exact hole with a
reproducing command."""),
    ("RevCounterHonesty", "reviewer", f"""# Target
{C1C}: fraud/vacuity audit of its own guards.
# Review
1. Enumerate every guard (reference sanity, output equality, gate hash, fixture integrity) with lines.
2. For each guard, describe one way a broken fixture could still satisfy it; where you find a real
   hole, prove it in scratch (a stub engine that scores higher than it should).
3. Check the kill-rule sentence in claims.md against the counter's actual exit/label condition.
# Acceptance
Guard table + (if any) a MEETS-style proof with command/exit/label. If no hole, say so and name the
strongest guard and why it holds."""),
    ("RevClaimPredicate", "reviewer", f"""# Target
{CLAIMS} P1/P2 versus the two counters' code.
# Review
1. Extract P1's sentence, label string, threshold and exit condition; compare to c1-count.py's LABEL,
   the pass computation and `predicate_holds`.
2. Same for P2 (four fields: WITNESS_PER_RECORD, OUTPUT_EQUIV, LANDED_ATTRIB, RENAMED).
3. Report any divergence of wording, threshold, or field name — a claim whose prose and code disagree
   is a calibration defect.
# Acceptance
Two-column comparison table (claim prose vs code line) + a "same sentence?" verdict per claim."""),
    ("CritC1Swap", "critic", f"""# Target
Attack C1's separation: can an engine score 14/14 while skipping the claimed work?
# Attack
In scratch, build a gate whose dead-zone matcher is replaced by an exact search AND which fakes
whatever the counter's scenarios read (echo line, recorder argv, manifest hash) — i.e. the strongest
output-equivalent engine you can write inside the time box. Score it with {C1C} (seed 36331+).
Also try the reverse: a CORRECT gate that the counter kills (false negative).
# Acceptance
Two scored attempts with commands, receipts and labels. MEETS (score >=14 with the work skipped), or
the wall that stopped you named precisely (which scenario, which assertion, why it cannot be faked)."""),
    ("CritC2CallForShow", "critic", f"""# Target
Attack C2's stated limit and the renamed control.
# Attack
1. Build the call-for-show engine: query the recorder with the record's span, discard the answer, then
   answer by exact search. Score it with {C2C} (seed 36331). State whether it is separated (expected,
   per claims.md's limit) and what that means for P2's reading.
2. Try to make a LEGITIMATE refactor fail: rename the matcher functions AND move the argv construction
   into a helper; check `RENAMED=pass` still holds. A false kill is a C2 defect.
3. Try to forge an argv log line from inside the gate (the stated anti-instrumentation limit) and state
   whether P2 still passes — if yes, that is a MEETS.
# Acceptance
Three scored attempts with commands and labels; a verdict line per attempt."""),
    ("MutC2AttrKey", "mutation-tester", f"""# Target
Prove the per-record attribution key is load-bearing in {WIT}.
# Mutate
In scratch (never edit the lane): patch a COPY of argv-witness.py twice —
 (a) collapse per-record attribution to a global count (any matcher argv counts for every record);
 (b) require only a prefix of the span (first 64 bytes) in the argv.
Score each mutant with {C2C} (seed 36341/36351) and record the label + which variants it now admits.
A mutant that still scores 5/5 means the counter does not measure per-record attribution.
# Acceptance
Two mutants: patch diff, receipt, label, variant table. Verdict per mutant: load-bearing or not."""),
    ("MutC1Arm", "mutation-tester", f"""# Target
Prove one C1 arm is load-bearing.
# Mutate
In scratch, patch a COPY of {C1C} to disable exactly one arm — (a) the manifest hash-pin validation, or
(b) the locale arm — and run it against the landed gate (seed 36341+) and against the base gate.
The mutant must be a counter change, not a gate change; state clearly that the score is then not
evidence for the claim.
# Acceptance
Patch diff + two scored runs + a reading: which arm the count actually rides on, and whether the
committed counter's 14/14 can be explained by fewer than 14 independent behaviours."""),
    ("SentNoHarm", "sentinel", f"""# Target
No-harm on the previously pinned observables after the round-36 gate edits.
# Run
From {LANE}/SKILL.md find the pinned observable commands (claims VERDICT_BEARING_CLAIMS 17/17, chain
RESOLVED_HOPS 17/22, broken control 1/2, r1 archives VERDICT_BEARING_EXPORTS 3/3). Re-run each on the
landed gate against the same fixtures the runbook names; a fixture lives under
`../research/deep-research-2026-09-28/` or the lane's own test data — use the runbook's exact paths.
# Acceptance
One table: observable · expected (r35 recorded value) · observed · pass/harm. Any drift is a no-harm
finding (name the exact value and command). Include the commands verbatim."""),
    ("SimpDiff", "simplifier", f"""# Target
YAGNI pass over the landed round-36 gate diff (base control → landed gate) and the new tool {WIT}.
# Review
1. List anything in the diff that no claim arm or repair needs: duplicated helper, dead branch,
   defensive check that cannot fire, comment that overstates.
2. Same for argv-witness.py: functions/fields/CLI options never exercised by the counter or a useful
   direct run (show the usage counts you measured).
3. For each, state the smallest deletion that preserves verified behaviour — propose only, do not edit.
# Acceptance
Deletion candidates table (path:line · why unused · verification that still holds). If none, say so
and show the sweep you ran."""),
    ("ConnOverlap", "connector", f"""# Target
Sibling-overlap scan: is per-record argv attribution or the engine-swap canary already held elsewhere in
the fleet?
# Scan
Grep sibling lane repos under /home/vgpnk/Projects/shokunin/*-shokunin for: `argv-witness`,
`ENGINE_SWAP_CANARY`, `WITNESS_PER_RECORD`, `RESEARCH_GATE_GREP`, `mechanism-witness`, `PS4` witness
channels, `canary`. Also search `.ufo/reports/` for the same tokens.
# Acceptance
Table: token · repo · path:line · verdict (fleet-unique / reused pattern / contested scope). State
which lane would own it if contested (PROVINCE.md basis) and whether this round duplicates work."""),
    ("LabScenarioIsolation", "executor", f"""# Target
One falsifiable hypothesis about {C1C}: the fourteen scenarios do NOT leak state into each other.
# Probe
1. Read how each scenario builds its fixture (TMP dir, manifest path, PATH, env). Name every resource
   a scenario could share with the next (manifest file, temp dir, exported variables).
2. Hypothesis: "every scenario is hermetic — its verdict is unchanged when run in a different order or
   alone". Test it by running the counter on the landed gate with seed 36351 and comparing per-scenario
   verdicts to a single-scenario run if the counter can select one; if it cannot, prove hermeticity by
   inspection plus one experiment: poison a parallel process's environment variable the counter reads
   and show it does not move any verdict.
3. State the hypothesis, the observation, and whether it was falsified. A falsified hypothesis is a
   real finding about the counter, not a failure.
# Acceptance
Hypothesis line, experiment command(s), observed per-scenario verdicts, falsified yes/no with reason."""),
    ("ScribeSrcGrep", "scribe", f"""# Target
New SOURCES row S069 — GNU grep(1) manual, `-b`/`-o`/`-a` semantics (the witness's argv/offset channel).
# Open
Read `/usr/share/man/man1/grep.1.gz` locally (this is the same installed page as S066, a DIFFERENT
scope: byte-offset and only-matching output semantics, not pattern-file/-F/-P/-z). Record: package
version (`pacman -Q grep` is read-only and allowed), file sha256, and the exact section names.
# Draft
Write `{WD}/ScribeSrcGrep/row-draft.md` with: the 11-cell row (id S069, source title + `— /usr/share/man/man1/grep.1.gz`,
kind docs, tier A, scope, anchor with decompressed line numbers, teaches, status mined, opened 2026-10-23,
recheck on-release, used-by corpus/knowledge/per-record-argv-attribution-r36.md) and a `## Gate` entry
carrying the URL-or-path, access date 2026-10-23, and ONE located quote of <=25 words with its line
numbers grounding `teaches` (the sentence about `-b` with `-o` printing the offset of the matching
part). Also state what the page does NOT say (e.g. nothing about per-record attribution as a method).
# Acceptance
Row draft + Gate entry + file sha256 + quote with line numbers; no edits outside your wave dir."""),
    ("ScribeSrcSha", "scribe", f"""# Target
New SOURCES row S070 — coreutils `sha256sum(1)`, digest shape and `--check` (repair R3's pin).
# Open
Read `/usr/share/man/man1/sha256sum.1.gz` locally. Record package version (`pacman -Q coreutils`,
read-only), file sha256, section names, and the exact sentence stating the 256-bit / 64-hex output
shape and what `--check` reads.
# Draft
Write `{WD}/ScribeSrcSha/row-draft.md`: the 11-cell row (S070, source `GNU coreutils sha256sum(1) —
/usr/share/man/man1/sha256sum.1.gz`, kind docs, tier A, scope = the digest text format and --check
input, anchor with decompressed lines, teaches one grounded sentence, status mined, opened 2026-10-23,
recheck on-release, used-by corpus/knowledge/engine-swap-canary-r36.md) + `## Gate` entry with access
date and ONE located quote <=25 words with line numbers. State what the page does NOT say (it does not
define a validation policy, so the gate's 64-lowercase-hex rule is the lane's choice [INFERENCE]).
# Acceptance
Row draft + Gate entry + sha256 + located quote with lines."""),
    ("ScribeKnowC1", "scribe", f"""# Target
Draft `corpus/knowledge/engine-swap-canary-r36.md` (C1's knowledge entry).
# Draft
Provenance trio first: `source:` (cites S070 plus the committed receipts
`.ufo/waves/round-36/measure/c1-*.json` and the frozen claims path), `verified-at: 2026-10-23`,
`recheck: on-release`. Then: (1) the mechanism — the gate and counter separate an output-equivalent
engine swap in fourteen named scenarios; a table of the 14 with one line each (scenario · what it
proves · receipt field); (2) the before state (base gate 10/14, S11-S14) and the do-nothing control
reading; (3) the stated limits verbatim from claims.md (semantic canary proves the query, not the use;
call-for-show survives; a gate that reads the recorder can forge); (4) the reading rule: the counter
proves what its scenarios assert, one at a time, never "the engine is genuine".
Cite only committed bytes; no unverified number. Every count gets its counting command.
# Acceptance
Entry draft in your wave dir with the provenance trio, the 14-row table, the before-state, the limits,
and a closing "what this entry does not claim" line."""),
    ("ScribeKnowC2", "scribe", f"""# Target
Draft `corpus/knowledge/per-record-argv-attribution-r36.md` (C2's knowledge entry).
# Draft
Provenance trio: `source:` cites S069 + the receipts `.ufo/waves/round-36/measure/c2-*.json` + the
witness path; `verified-at: 2026-10-23`; `recheck: on-release`. Then: (1) the channel (distinct-path
GNU-reporting recorder as `RESEARCH_GATE_GREP`, NUL-delimited argv log, name+marker outside the gate's
environment); (2) the attribution rule (each record's span, or its first 4096 bytes for a dead-zone
span, must appear in a `-a -z -b -o -P` argv) and why the offset semantics come from the grep manual
(row S069); (3) the survivor table V1-V5 with the legacy witness's before-scores; (4) the renamed
control and why a false kill matters; (5) limits (query not use; active anti-instrumentation out of
scope; the counting command). Cite only committed bytes.
# Acceptance
Entry draft with provenance trio, channel, attribution rule, survivor table, renamed control, limits,
counting command."""),
    ("ScribeLesson", "scribe", f"""# Target
Draft `.ufo/waves/round-36/w1/ScribeLesson/lesson-draft.md`: the round-36 lesson skeleton.
# Draft
1. `## Mistakes` — a table (class · evidence pointer · captured-by · fix) with at least these two
   candidates, each re-verified by you against the files (do not take them on trust):
   (a) number-drift/attribution in `corpus/evidence/round36/c2-count.py`'s docstring: it states the
       round-35 witness "separates only 3/5 (V3 and V5 pass it)" while the committed legacy receipt
       ({MEAS}/c2-before-legacy-s36001.json) reports matched=2/5 with V2 and V3 passing — quote the
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
skeleton naming rows, rejects and the spot-check pointer."""),
]


def main():
    items = []
    for name, role, body in ITEMS:
        prompt = LEAD + body.strip() + "\n" + TAIL.format(wd=WD)
        items.append({"name": name, "role": role, "prompt": prompt})
    spec = {
        "wave": "chousa-r36-w1",
        "milestone": "round-36 attempt 2 wave 1: build + independent re-derivation of C1 (14-scenario engine-swap canary) and C2 (per-record argv attribution), frontier drafts",
        "reportDir": ".ufo/waves/round-36/w1",
        "axes": ["operability", "calibration"],
        "context": CONTEXT,
        "items": items,
    }
    json.dump(spec, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
