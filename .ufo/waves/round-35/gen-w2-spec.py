#!/usr/bin/env python3
"""chousa round 35, wave 2 = one v2 wave (64 seats, attack + build together).
Usage: gen-w2-spec.py > w2-spec.json"""
import json
import pathlib
import sys
from collections import Counter

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
WD = f"{LANE}/.ufo/waves/round-35/w2"
SCR = "/tmp/hyaku/chousa-r35/w2"
FREEZE = "e87c5d7ea2dbf3730b36a3961de3f06261d015e4"
GATE = f"{LANE}/tools/research-gate.sh"
GSHA = "1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617"
BASE_GATE = f"{LANE}/.ufo/waves/round-35/repairs/base-gate.sh"
BASE_SHA = "a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b"
CLAIMS = f"{LANE}/corpus/evidence/round35/claims.md"
C1C = f"{LANE}/corpus/evidence/round35/c1-count.py"
C2C = f"{LANE}/corpus/evidence/round35/c2-count.py"
WIT = f"{LANE}/tools/mechanism-witness.py"
PROBE = f"{LANE}/.ufo/waves/round-35/repairs/slen-probe.sh"
CTL = f"{LANE}/.ufo/waves/round-35/controls"
MEAS = f"{LANE}/.ufo/waves/round-35/measure"
GOD = pathlib.Path.home().joinpath(".agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + GOD + "\n"

CONTEXT = f"""# Goal
chousa lane (deep-research method), round 35, ONE v2 wave — build and attack together. Lane repo {LANE}
(jj-colocated, branch master). Wave base revision {FREEZE}; the landed gate {GATE} has sha256 prefix
{GSHA} (verify: sha256sum {GATE}) and the pre-round gate {BASE_GATE} is the round-34 blob {BASE_SHA}.
Read FIRST, in this order: the frozen claim design {CLAIMS} (two claims, P1/P2, kill rules, pre-data
controls), the C1 counter {C1C}, the C2 counter {C2C}, the witness tool {WIT}, and the slen probe {PROBE}.
The round's two claims, both already measured by the L1 on seeds 3501/3517:
- C1 operability (lowest scored axis, operability 3/10): research-gate.sh resolves, verifies and pins ONE
  grep binary (absolute; `RESEARCH_GATE_GREP` override must be absolute and must report GNU grep; refusal is
  exit 2 with `research-gate: GREP_PROVENANCE refused: ...`; `CHOUSA_GREP_PIN_ECHO=1` prints
  `GATE_GREP: path=... source=default|override version="..."`). P1 = GREP_PIN_MATCH=9/9 on two fresh seeds.
  Before (base gate): 0/9. Cheapest non-oracle control (hardcoded pin, no provenance/override/echo): 3/9.
- C2 calibration: `tools/mechanism-witness.py` witnesses the dead-zone mechanism out of band (gate under
  `bash -x`, private PS4, matcher-function entry stamps per long-span record) and {C2C} applies it to two
  output-equivalent keyed engines (K1 python-exact for long spans; K2 the same branch gated on ROOT looking
  like a harness temp dir). P2 = WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass. Before: 0/2
  (battery absent). Trivial witness stubs (always-pass, always-fail) both fail P2 (controls committed).
Repairs also landed: R1 the chunk matcher's `slen` now reads its own parameter (dynamic-scope bug; probe
shows base 0 offsets / landed 1); R2 selftest case-range comments corrected to 252-253 and 254-256.
Your job: attack and re-derive. A MEETS finding — an engine that scores 9/9 on C1 or separates nothing on
C2, or a witness bypass that still passes P2 — is the most valuable result of this wave: say exactly why.

# Contract
- Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Write your report once.
  Extra artifacts (patched gates, receipts, logs, patches) go ONLY inside your own directory
  {WD}/<YourName>/ (create it); keep each artifact under 1 MiB (large logs stay in {SCR}; cite path+sha256).
- Read-only on ALL lane production files (tools/, corpus/, SCORECARD.md, LOG.md, SKILL.md, README.md,
  PROVINCE.md, SHONEN.md, .ufo/waves/round-35/{{controls,measure,repairs}}/ …) and on the fleet repo,
  sibling lanes, lane jj state and the lane Git index. No git/jj write commands anywhere; read-only git
  (log/show/diff/status/rev-parse/cat-file) is fine. Experiments only in {SCR}/<YourName>/: copy files, or
  `git clone -q {LANE} <dir> && git -C <dir> checkout -q {FREEZE}` (unset GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE
  first). Counters: set C1_TMP / C2_TMP / WITNESS_TMP / TMPDIR to your scratch dir.
- Pin every gate you score: sha256 it; a receipt whose gate sha256 is neither {GSHA} nor a control you built
  and named is not evidence. Never edit the committed counters or the witness tool — a bug is a finding.
- Processes: never signal by name/pattern (no pkill/killall); keep PIDs you start and kill only those. Disk:
  {SCR} is on /tmp (113 GiB free); /fast is 98% full — do not write there. Network: NONE. Bound every
  command with `timeout` (<=1800 s for selftest/counters, <=900 s otherwise). Leaf seat: no subagents (an
  executor may spawn at most one read-only labrat probe). Do not run `pacman` anything.
- Honesty: report only what you ran or opened; quote commands, exit codes, key output. Mark inference
  [INFERENCE]. Located quotes <=25 words with path + access date 2026-10-23.
- Time box: return within 35 minutes of your start; a partial report with what you verified beats none.
# Tooling directive — operator, 2026-10-19 (always on, every agent)
You may install or update tools that help the task without asking; read /home/vgpnk/.omp/agent/RULES.md
first and record each install (tool, version, channel, reason). All pacman transactions are PAUSED
host-wide: never pacman -S/-Sy/-Syu/-U/-R, downgrade, or restart a host service; use uv tool / npx / an
official binary in ~/.local/bin, or report the need. Prefer no installs.
# Output
Report at the trailer path: what you did, evidence (paths, commands, exit codes, receipts), the verdict your
item asks for, limits. Return <=8 lines summarizing it.
"""


def item(name, role, text):
    return {"name": name, "role": role,
            "prompt": LEAD + "\n# Target\n" + text +
                      "\n# Acceptance\nReport at the trailer path; artifacts only in your own directory; "
                      "every claim backed by a command/output or path:line."}


SITE = ("Enumerate across the WHOLE gate file (grep for `grep`, `command grep`, `egrep`, `fgrep`, `bash -c`, "
        "`sh -c`, `eval`, and command substitutions) every place a grep invocation can run, with `grep -n` line "
        "numbers, the enclosing function/mode, and the shell context (pipeline, process substitution, `$(...)`, "
        "subshell). For each, say whether the `grep()` wrapper pins it and give the command that proves it "
        "(e.g. run that mode under a PATH shim {scr}/<You>/shim/bin/grep that appends to a tripwire and execs "
        "{real}; the tripwire must stay empty). Report any site that bypasses the wrapper as a finding.")


ITEMS = [
    # ---------------- reviewers (10)
    ("RevGrepSites", "reviewer",
     SITE.format(scr=SCR, real="/usr/bin/grep") +
     " Also state, for each bypass you find, whether the pinned binary still runs (wrapper missing but the "
     "absolute default resolves) or whether the shim would win."),
    ("RevGrepModesA", "reviewer",
     f"Pin coverage, part A: run modes `verify` and `verify-claims` on a scratch clone at {FREEZE} under (a) a "
     f"PATH shim named grep first on PATH, (b) a BASH_ENV file defining a logging grep function, (c) "
     f"RESEARCH_GATE_GREP=/usr/bin/grep with a shim on PATH. For each: exit code, whether the tripwire stayed "
     f"empty, and whether the verdict equals the unshimmed run byte for byte. Use the committed fixtures "
     f"(`corpus/fixtures/claims-r2.jsonl`, a record under `corpus/fixtures/`) and record the exact commands."),
    ("RevGrepModesB", "reviewer",
     f"Pin coverage, part B: same three shadow environments as RevGrepModesA for modes `verify-chain`, "
     f"`verify-sweeps` and `verify-integrity` on the committed chain/sweep fixtures (find them under "
     f"corpus/fixtures and the round-1 archives; cite the paths). Report per mode: exit, tripwire, verdict "
     f"identity, and any mode where the pin is not reached."),
    ("RevGrepModesC", "reviewer",
     f"Pin coverage, part C: modes `verify-metadata --registry corpus/SOURCES.md --as-of 2026-10-23`, "
     f"`verify-all --json <scratch>/m.jsonl`, `--pin`, `--drift` and `--selftest` under the same three shadow "
     f"environments. `--selftest` is the important one: it re-invokes the gate as a child, so confirm the pin "
     f"is re-resolved per child (echo the flag and count `GATE_GREP:` lines) and that a refused override exits "
     f"2 before case 1 runs (no `ok-case`/`FAIL-case` output)."),
    ("RevScenarioS1S2", "reviewer",
     f"Audit the C1 counter's S1/S2 assertions (`{C1C}` lines for `S1-shim-first-path`, "
     f"`S2-bash-env-function`): is `tripwire empty` plus `output equals reference` actually sufficient to prove "
     f"the pin, or could a gate pass both while still executing the shim (e.g. shim invoked with no argv, shim "
     f"under a different name, shim inside a subshell whose redirect fails)? Write and run at least one attack "
     f"gate that scores S1/S2 PASS while a shim executes, if one exists; otherwise prove none does."),
    ("RevScenarioS3S4S5", "reviewer",
     f"Audit S3/S4/S5 of `{C1C}`: is the symlink farm (`build_nogrep_path`, NOGREP_TOOLS) complete enough that "
     f"a MISS there is about grep and not a missing tool (name every tool the claims path actually execs, from "
     f"a `bash -x` trace of one run)? Do S4/S5's refusals fire before any record read (trace evidence: the "
     f"first trace line number should precede verify_claims' body)? Would a gate that refuses with exit 2 for "
     f"ANY override (even a valid one) still score S4/S5 and fail elsewhere?"),
    ("RevScenarioS6S7S8S9", "reviewer",
     f"Audit S6/S7/S8/S9 of `{C1C}`: S6's stub prints the uutils version to stderr — confirm the gate refuses "
     f"without ever using it for a match (stub call count and argv), and that a stub printing GNU grep on "
     f"stdout with a wrong exit code behaves as the check intends. For S7/S8/S9 parse the echo line strictly: "
     f"is `path=/usr/bin/grep` substring-matching gameable (e.g. a path containing that text)? Propose the "
     f"tighter assertion and show the current one still discriminates."),
    ("RevWitnessFixture", "reviewer",
     f"Audit the fixture generator in `{WIT}` (`generate`, `build`, `Gen.span`): can any generated span fall "
     f"outside 32765..32767 or be shorter/longer than the class intends (draw 300 spans across 20 seeds and "
     f"report min/max per class)? Are the line-bound records' `line` values correct? Do the randomizations "
     f"really vary prefix/id-width/name-scheme/key order/record order? Is `long_records` the right "
     f"denominator for the stamp threshold, and can a seed produce a fixture where the landed gate stamps "
     f"fewer entries than `long_records` (make such a seed a finding)?"),
    ("RevWitnessCode", "reviewer",
     f"Static review of `{WIT}`: the stamp regex and function-span extraction (what if a function body "
     f"contains a line starting with a bare closing brace at column 0, or `tok_span_offsets` appears inside a comment/string?), "
     f"the trace file's size bound for 9 records with 32 KiB spans (measure it), cleanup on timeout, the JSON "
     f"contract, exit codes, and `--tmp`. Report each defect with a demonstrating input."),
    ("RevSlenSweep", "reviewer",
     f"Dynamic-scope sweep: `local a=$1 b=${{#a}}` expands every right-hand side before assigning any of them, "
     f"so any derived value in the same `local` statement reads the CALLER's dynamic scope. Sweep the WHOLE "
     f"gate for that shape (every `local` line with a derived expansion of a name assigned in the same "
     f"statement: `${{#x}}`, `${{x:...}}`, `${{x%%...}}`, arithmetic on `$x`) and report every instance with "
     f"line:context, whether the caller happens to pass the same value (latent) or differs (live bug), and the "
     f"one-line repair. Do not edit the gate."),
    ("RevCaseRanges", "reviewer",
     f"Case-range audit: run `bash {GATE} --selftest` on a clone at {FREEZE} and map every `ok-case` line to "
     f"its comment block; verify the corrected ranges 252-253 (round-34 C1) and 254-256 (round-34 attempt-2 "
     f"dead zone) and EVERY other `cases N-M` comment in the gate plus the ranges quoted in SKILL.md. Report "
     f"each mismatch as a finding with the correct range (the r34 closure routed exactly this class)."),

    # ---------------- critics (6)
    ("CritGrepProvenance", "critic",
     f"Attack C1's provenance check (`grep_pin_init`/`grep_pin_verify` in {GATE}). Try: a wrapper script that "
     f"prints a GNU line for `--version` and execs a shim for everything else; a symlink to a non-GNU binary; "
     f"an override that is a directory, a FIFO, a 0-byte file, a path with a space and a newline; an override "
     f"whose `--version` exits nonzero or prints nothing; a binary that prints GNU on line 2 only (the check "
     f"reads line 1); TOCTOU between check and use. For each: what the gate does, and whether the claim's "
     f"disclosed limit already covers it. A bypass that changes a verdict is the finding."),
    ("CritGrepClaimScope", "critic",
     f"Attack C1 as a claim (`{CLAIMS}` §C1) against the round prompt's claim-sizing rules: is 'the gate pins "
     f"the binary' a surface move or a restatement? Does the counter have a do-nothing control that could reach "
     f"9/9 (re-run the base receipt `{MEAS}/../controls/c1-base-s3501.json` and the hardcoded control)? Is P1's "
     f"sentence exactly the counter's code condition and receipt label? Does the pin cost measurable time per "
     f"invocation and per selftest (measure base vs landed selftest wall time)? Name what a reader would "
     f"wrongly assume it covers (provenance beyond self-report; `VERIFY_ALL` writes; sha pinning of the "
     f"binary)."),
    ("CritWitnessBlind", "critic",
     f"Blind-spot hunt on `{WIT}`: build engines that (a) call `tok_span_offsets_chunk` once and ignore its "
     f"result; (b) run `set +x` before a keyed branch; (c) `exec 2>`/`BASH_XTRACEFD` inside the gate; (d) "
     f"re-invoke itself with `bash --norc` for the matcher; (e) implement the exact search INSIDE "
     f"`tok_span_offsets_chunk` (witness passes, mechanism replaced — the honest limit); (f) call the chunk "
     f"matcher on a synthetic hay. Score each with `{C2C}` (or the tool directly). Report which defeat the "
     f"witness, which P2 already discloses, and whether any defeat leaves the *landed* gate miscredited (that "
     f"would be fatal to P2)."),
    ("CritC2AxisFit", "critic",
     f"Attack C2 as a claim (`{CLAIMS}` §C2): is 'the lane can separate output-equivalent engines' calibration "
     f"or coverage, and does the report's axis assignment survive that question? Is the metric gameable — can "
     f"a battery that only ever answers 'fail' for non-identical gates pass (the stub-fail control says no: "
     f"prove it), can a gate be separated for the wrong reason (output mismatch)? Is K1/K2 a fair "
     f"representation of the round-34 finding (ctl4/ctl6) or a weaker strawman? Does the claim overreach by "
     f"writing 'kills' when the witness only declines to credit?"),
    ("CritRoundShape", "critic",
     f"Round-shape audit for the report: this is ONE v2 wave of 64 seats under policy v2 "
     f"(scripts/hyaku/ufo-wave-policy-v2.json, band 64-128, maxLanes 256). Verify against the spec/registry the "
     f"counts the report must state: total seats, role mix, attack share (reviewer+critic+mutation-tester >= "
     f"25%), that the validator emitted ONE taskCall (dispatch.calls/one-task-call invariant), that no planner "
     f"seat exists anywhere (the L1 holds the §3 planner seat; the planning data-walk rides scout/connector "
     f"items), and that every item names an absolute lane path. Report any inconsistency and the exact numbers "
     f"the report should carry."),
    ("CritClaimSizing", "critic",
     f"§9 claim-sizing audit of BOTH claims in `{CLAIMS}`: for each, restate the after-state as one concrete "
     f"value re-derivable with one command over committed bytes; check for universal clauses; check the "
     f"before-state receipts exist and are authentic (open `{CTL}/c1-base-s3501.json`, "
     f"`{CTL}/c1-hardcoded-s3501.json`, `{CTL}/c2-before-s3501.json`, `{CTL}/c2-stub-pass-s3501.json and c2-stub-fail-s3501.json`); "
     f"check the claim is causally separable from the other (C1 on a tree without the witness tool still "
     f"9/9? C2 on the base gate still 2/2? demonstrate one direction); flag any sentence that narrows the "
     f"target after landing or leans on an uncommitted artifact."),

    # ---------------- mutation-testers (10)
    ("MutGrepShimPath", "mutation-tester",
     f"PATH-shadow controls for C1: in scratch, build four shims named `grep` placed first on PATH — (a) a "
     f"script that logs and execs /usr/bin/grep; (b) a symlink to /bin/false; (c) a script that prints a "
     f"GNU-looking version for --version and wrong output otherwise; (d) a directory entry named `grep` that is "
     f"not executable plus a real /usr/bin/grep later. Score each with `{C1C} --gate {GATE}` on one fresh seed "
     f"(not 3501/3517) and report which scenarios move. Expected: no scenario fails; a failure is the finding."),
    ("MutGrepShimEnv", "mutation-tester",
     f"Environment-shadow controls for C1: (a) BASH_ENV defining a grep function that logs; (b) an exported "
     f"function via `env 'BASH_FUNC_grep%%=() { ... }'`; (c) an alias in BASH_ENV; (d) `ENV` (sh) plus a `sh` "
     f"invocation from the gate if any. Score with `{C1C}` and report whether exported functions can beat the "
     f"gate's own `grep()` definition (definition order: BASH_ENV is sourced before the script body, so the "
     f"script's definition should win — prove it or refute it with a trace)."),
    ("MutGrepPinEngines", "mutation-tester",
     f"Correct-output non-grep engines vs C1: build three gates whose matcher answers correctly without the "
     f"pinned grep for short spans — (a) bash `case`/glob search on the hay, (b) `awk index()`, (c) `python3` "
     f"bytes.find — each leaving the pin code untouched or removed. Score each with `{C1C}` (fresh seed). The "
     f"counter must not credit a gate that bypasses the pin for the scenarios that test the pin; if one "
     f"reaches 9/9 while never execing the pinned binary, say exactly which scenario is too weak."),
    ("MutCounterC1", "mutation-tester",
     f"Counter-of-counter for C1: in a scratch COPY of `{C1C}` remove one requirement at a time (S1 tripwire, "
     f"S2 tripwire, S3 output identity, S4/S5 marker, S6 marker, S7/S8/S9 echo field checks) and show — with a "
     f"deliberately wrong gate — which removals let that gate reach 9/9 (load-bearing) and which none needs. "
     f"Never edit the committed counter. Report the load-bearing set and any redundant scenario."),
    ("MutWitnessBypass1", "mutation-tester",
     f"Witness bypass family 1: from the landed gate build (a) 'chunk-once' — call `tok_span_offsets_chunk` "
     f"once on the first long span, then answer every long span from a python exact search; (b) 'trace-off' — "
     f"`set +x` immediately before a keyed branch and `set -x` after. Score each with `{WIT}` directly and "
     f"with `{C2C}` (same fresh seed). For (a) state the exact stamp count the witness saw and whether the "
     f"threshold `>= long_records` caught it; for (b) whether bash continues tracing after `set +x`."),
    ("MutWitnessBypass2", "mutation-tester",
     f"Witness bypass family 2: (a) redirect stderr inside the gate (`exec 2>/dev/null` before the branch, "
     f"restoring after) — does the trace still reach the witness's file? (b) put the python exact search "
     f"INSIDE `tok_span_offsets_chunk` (witness passes, mechanism replaced): report it as the disclosed limit "
     f"and say whether P2's text already covers it; (c) call the chunk matcher on a synthetic hay then ignore "
     f"it. Score each with `{WIT}`."),
    ("MutC2KeyedBattery", "mutation-tester",
     f"Extend the keyed-engine battery: build three MORE output-equivalent engines from the landed gate — (a) "
     f"fixed temp-prefix key (`chousa-` anywhere in ROOT), (b) record-shape key (ids/names matching the "
     f"witness's own scheme), (c) id-length-mod-3 verdict pick combined with exact search. Score each with "
     f"`{C2C}`'s witness on a fresh seed using your own driver (do not edit the counter) and report output "
     f"fullness and witness verdict. The finding is any engine that is output-full AND witness-pass."),
    ("MutWitnessThreshold", "mutation-tester",
     f"Threshold attack: build an engine that calls `tok_span_offsets_chunk` exactly ONE time per gate run (on "
     f"the first long record) and answers everything else by exact search, then an engine that calls it once "
     f"per long record but discards the result. Show the witness's stamp counts and whether the frozen "
     f"threshold (`chunk >= long_records`) separates them from the landed gate. If a discarded-result engine "
     f"passes, say whether that is a P2 failure or the disclosed limit."),
    ("MutSlenScope", "mutation-tester",
     f"R1 kill test: create scratch variants of the landed gate's chunk matcher — (a) the pre-fix "
     f"`local hay=$1 span=$2 slen=${{#span}}`; (b) `local slen` + `slen=${{#span}}` (landed); (c) `slen=$2` "
     f"length-of-argument-only. Run `bash {PROBE} <variant>` and report offsets for each: the probe must print "
     f"offsets=0 for (a) and 1 for (b) (it did on {BASE_GATE}/{GATE}); show (c) as an equivalent repair or a "
     f"wrong one. Then run the landed selftest once on (a) to show the public path does not catch it (why the "
     f"defect was latent)."),
    ("MutPinRefusals", "mutation-tester",
     f"Refusal completeness for C1: build six malformed overrides — empty string, `,`, `/`, a directory, a "
     f"FIFO, a 0-byte file — plus `RESEARCH_GATE_GREP` set but empty (`RESEARCH_GATE_GREP=` must be treated as "
     f"UNSET or refused; state which the code does and whether the claim's text is honest about it). Run each "
     f"against `{GATE} verify-claims` and report exit code, stderr, and that no record was read. Any case that "
     f"proceeds (exit 0/1) is a finding."),

    # ---------------- executors (22)
    ("ExecC1Fresh1", "executor",
     f"Re-derive C1: on a scratch clone at {FREEZE} verify `sha256sum tools/research-gate.sh` = {GSHA}, then "
     f"run `C1_TMP=<scratch> python3 {C1C} --gate <clone>/tools/research-gate.sh --seed S --receipt "
     f"{WD}/ExecC1Fresh1/c1-sS.json` for seeds 3529 and 3539. Report counts, per-scenario lines, timings, and "
     f"whether the two committed after-receipts `{MEAS}/c1-after-s3501.json`/`c1-after-s3517.json` carry the "
     f"same counter sha256 and gate sha256."),
    ("ExecC1Control", "executor",
     f"Re-score the pre-data C1 control on two fresh seeds: `{CTL}/ctl-c1-hardcoded-grep.sh` (sha256 it; it is "
     f"the base gate plus a hardcoded `/usr/bin/grep` wrapper) with `{C1C} --gate <control> --seed 3529/3539 "
     f"--receipt {WD}/ExecC1Control/`. Expected 3/9; report which scenarios a hardcoded pin wins and which it "
     f"cannot (refusals, echo naming). A count above 4 is a finding against P1's discrimination."),
    ("ExecC2Fresh1", "executor",
     f"Re-derive C2: clone at {FREEZE}, verify the witness tool sha256 "
     f"`9f537bfde0dd53f2240af149e1b7a03fd0a0f372ee1fa1a32e94044115a252b3` (recompute it), then run "
     f"`C2_TMP=<scratch> python3 {C2C} --seed 3529 --receipt {WD}/ExecC2Fresh1/c2-s3529.json` and the same for "
     f"seed 3539. Report WITNESS_SEPARATED, OUTPUT_EQUIV, LANDED_WITNESS, the per-variant output/stamp lines, "
     f"and total wall time."),
    ("ExecC2Fresh2", "executor",
     f"Second independent C2 re-derivation: seeds 3547 and 3559 with `{C2C}`, receipts under "
     f"{WD}/ExecC2Fresh2/. Then run `{WIT} --gate <clone>/tools/research-gate.sh --seed 3547 --json "
     f"{WD}/ExecC2Fresh2/witness-3547.json` directly and report the raw stamp counts (chunk/direct) versus "
     f"`long_records`."),
    ("ExecNoHarm", "executor",
     f"Full no-harm battery on the landed gate, independently: on a scratch clone at {FREEZE} run (1) "
     f"`bash tools/research-gate.sh --selftest` (expect PASS 256, first 253 case lines identical to base — "
     f"compare against `{BASE_GATE}` in a second clone), (2) claims fixture verify-claims (17/17 CLEAN), (3) "
     f"chain fixture (17/22 CLEAN and the broken fixture 1/2 DRIFT), (4) the round-1 observable 3/3 (the "
     f"SCORECARD counting command), (5) r31 c1/c2 counters, (6) r32 c2 v2 and v3, (7) r33 c1 v2, (8) r34 c2. "
     f"Report one row per check with exit codes; any changed line is a finding."),
    ("ExecSelftestEnv", "executor",
     f"Locale re-measure: `LC_ALL=C bash <clone>/tools/research-gate.sh --selftest` on {FREEZE} and on "
     f"{BASE_GATE}; list the failing case names for both and compare with the round-34 disclosure (base 11 / "
     f"landed 10 under LC_ALL=C). Report whether the grep pin changes the count or the failing set, and "
     f"whether any dead-zone case is locale-dependent."),
    ("ExecSlenProbe", "executor",
     f"R1 probe matrix: run `bash {PROBE} {BASE_GATE}` (expect offsets=0, exit 1) and `bash {PROBE} {GATE}` "
     f"(expect offsets=1 first=5, exit 0). Then extend the probe idea in scratch: call the extracted chunk "
     f"matcher with (a) no visible `span` at all, (b) a visible `span` of 1 byte, (c) a visible `span` of "
     f"30000 bytes, on both gates. Report a table; the base gate should report 0 offsets in all three and the "
     f"landed gate 1."),
    ("ExecPinModeVerify", "executor",
     f"Mode `verify` under the pin: on a clone at {FREEZE}, run `verify` on a committed research record (pick "
     f"one under `corpus/` or the round-1 archives; cite it) with (a) clean PATH, (b) PATH shim + tripwire, (c) "
     f"RESEARCH_GATE_GREP=/usr/bin/grep + shim, (d) CHOUSA_GREP_PIN_ECHO=1. Report exit codes, verdict lines, "
     f"tripwire emptiness, the echo line, and whether (a) and (b) are byte-identical on stdout."),
    ("ExecPinModeClaims", "executor",
     f"Mode `verify-claims` under the pin: same four environments as ExecPinModeVerify on "
     f"`corpus/fixtures/claims-r2.jsonl` (with `--root` set so the fixture resolves). Include one case with "
     f"`RESEARCH_GATE_GREP=bin/grep` (relative) and report the refusal text and exit 2. Then re-run the same "
     f"fixture with the echo flag and diff stdout against the no-flag run (must be identical)."),
    ("ExecPinModeChain", "executor",
     f"Mode `verify-chain` under the pin: four environments on the committed chain fixture (find the "
     f"round-3 chain fixture the selftest and the battery use; cite the path) plus a refused override. Report "
     f"exit codes, `RESOLVED_HOPS=` lines, tripwire, refusal text. Confirm the chain matcher uses the same "
     f"pinned binary (stamp the wrapper: set `RESEARCH_GATE_GREP` to a logging wrapper that execs /usr/bin/grep "
     f"and report the argv it received, including whether `-a -z -b -o -P` appears)."),
    ("ExecPinModeSweeps", "executor",
     f"Mode `verify-sweeps` under the pin: four environments on a committed sweep fixture with `VERIFIED_SWEEPS`"
     f"output; plus a refused override. Report exit, summary line, tripwire, refusal. Any difference between "
     f"the clean and shimmed runs is the finding."),
    ("ExecPinModeIntegrity", "executor",
     f"Mode `verify-integrity` under the pin: four environments on the committed integrity fixture; report "
     f"exit, `INTEGRITY refs=` line, tripwire, refusal. Also check whether this mode calls grep at all (trace "
     f"it) — a mode that never greps should be unaffected by the pin, and the report must say so rather than "
     f"imply coverage."),
    ("ExecPinModeMetadata", "executor",
     f"Mode `verify-metadata --registry {LANE}/corpus/SOURCES.md --as-of 2026-10-23` under the pin: four "
     f"environments; report exit, counts, tripwire, refusal. Note the registry path is the committed SOURCES "
     f"table; do not edit it."),
    ("ExecPinModeAll", "executor",
     f"Mode `verify-all --json <scratch>/m.jsonl` under the pin on a committed record+claims surface: four "
     f"environments; report exit, the `VERIFY_ALL` line, manifest line count, tripwire, refusal. Confirm the "
     f"manifest write path is untouched by the pin (compare the manifest bytes with the clean run, modulo the "
     f"gate sha256/timestamp fields)."),
    ("ExecPinModePinDrift", "executor",
     f"Baseline modes under the pin: `--pin` and `--drift` on a scratch baseline file, each with (a) clean "
     f"env, (b) refused override (relative path) → expect exit 2 and no baseline write/read, (c) refused "
     f"non-GNU override. Report exit codes, files touched, stderr. A baseline written despite a refused pin is "
     f"a finding."),
    ("ExecPinModeSelftest", "executor",
     f"`--selftest` under the pin: (a) `RESEARCH_GATE_GREP=bin/grep bash {GATE} --selftest` must exit 2 with "
     f"the refusal and print NO `ok-case`/`FAIL-case` lines (count them: zero); (b) `CHOUSA_GREP_PIN_ECHO=1` "
     f"with PATH containing a directory full of `GATE_GREP`-like text — count `GATE_GREP:` lines (one per "
     f"child invocation is expected; report the exact number and how it relates to the 256 cases); (c) clean "
     f"run PASS 256."),
    ("ExecPinEchoStability", "executor",
     f"Echo-flag stability: for every mode the gate supports, diff stdout+stderr of a run WITHOUT "
     f"`CHOUSA_GREP_PIN_ECHO` against the same run on {BASE_GATE} (same inputs, same scratch). Report one row "
     f"per mode: byte-identical or the exact diff. This is the no-harm proof for the pin's default path; any "
     f"unexpected stderr line (including a stray `GATE_GREP:` ) is a finding."),
    ("ExecWitnessTiming", "executor",
     f"Witness cost bound: run `{WIT} --gate <clone gate> --seed 3569 --json <scratch>/w.json` and report wall "
     f"time, peak RSS (use `/usr/bin/time -v` if present), and the trace file's size (instrument by running "
     f"`bash -x` yourself with the same PS4 and measuring the stderr file). State whether the tool is safe to "
     f"run in a receipt loop (record the numbers the runbook can cite)."),
    ("ExecCounterC1Timing", "executor",
     f"C1 counter cost: time each scenario by running `{C1C} --seed 3571` twice and report total wall time "
     f"and the per-scenario pattern (the fixture is 3 short claims, so it should be seconds). Also report the "
     f"number of gate invocations per run (count them from the receipt's `runs` array) — 9 scenarios plus a "
     f"reference, and say whether the reference is re-derived per run (it is: quote the code line)."),
    ("ExecPriorCounters", "executor",
     f"Prior-counter no-harm: on a clone at {FREEZE} run the committed counters r31 c1/c2 (v2), r32 c2 (v2 and "
     f"v3), r33 c1 v2, r34 c2, each on ONE fresh seed with `--receipt` under {WD}/ExecPriorCounters/. Report "
     f"the printed labels (expect 120/120, 120/120, 132/132, 132/132, 156/156, 37/37) and any miss by class."),
    ("ExecR34C1V3", "executor",
     f"r34 long-span counter on the landed gate: `LC_ALL=C C1_TMP=<scratch> python3 "
     f"corpus/evidence/round34/c1-count-v3.py --gate <clone>/tools/research-gate.sh --seed 3593 --receipt "
     f"{WD}/ExecR34C1V3/c1v3-s3593.json` (add seed 3607 if time allows). Expect LONGSPAN_MATCH=42/42; report "
     f"counts and timing (the counter is bounded at 1500 s; bound your command at 1700 s)."),
    ("ExecCensus", "executor",
     f"Source registry census: run "
     f"`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa; "
     f"echo exit=$?` and report the exit code and every line. Then count rows (`grep -c '^| S[0-9]' "
     f"corpus/SOURCES.md`), list the last five row ids with their status/tier columns, and report whether any "
     f"row's `used-by` names a round-35 artifact. Do not edit the registry."),

    # ---------------- scouts (8)
    ("ScoutGrepSites", "scout",
     SITE.format(scr=SCR, real="/usr/bin/grep") +
     " Produce the site table only (no verdicts beyond wrapper/bystander), plus the count of sites."),
    ("ScoutDebris", "scout",
     f"r34 evidence reconciliation: on a clone at {FREEZE} count `.ufo/waves/round-34/w2a2/*.md` reports "
     f"(find -maxdepth 1), and verify whether `.ufo/waves/round-34/w2a2/ExecC2Oracle/{{boundary-diff,diff-fuzz,"
     f"pcre-boundary}}.txt` are tracked (`git ls-tree -r <commit> --name-only`) and at which commit. Also run "
     f"`git status --porcelain` on the clone and report any untracked/ignored debris under .ufo/ that a "
     f"round-35 report should name. Do not delete anything."),
    ("ScoutManExecvp", "scout",
     f"Open the installed `execvp(3)` manual page (`/usr/share/man/man3/execvp.3.gz` if present, else find it "
     f"with `man -w execvp`), report its sha256, the decompressed line numbers, and ONE located quote of <=25 "
     f"words that states the PATH search semantics (for the SOURCES row the L1 will curate as S067). Access "
     f"date 2026-10-23. Also report the package that owns the page (`pacman -Qo <path>`; read-only) and "
     f"whether `PATH` lookup order is stated."),
    ("ScoutManBash", "scout",
     f"Open the installed `bash(1)` manual page (`/usr/share/man/man1/bash.1.gz`), report sha256 and one "
     f"located quote <=25 words for each of: `BASH_ENV` (non-interactive startup file) and exported shell "
     f"functions (`export -f`, `BASH_FUNC_name%%`). These are the two shadow channels C1 defends against; the "
     f"L1 will curate them as S068. Include decompressed line numbers and the owning package."),
    ("ScoutManGrep", "scout",
     f"Re-open `grep(1)` (`/usr/share/man/man1/grep.1.gz`) for the three claims the pin relies on: `-z` "
     f"(NUL-delimited), `-P` (PCRE), and `--version` output. Report sha256, decompressed line numbers, and one "
     f"located quote <=25 words each. Note whether the page states anything about which binary is invoked "
     f"(it does not — say so, it is part of the C1 limit)."),
    ("ScoutSourcesCensus", "scout",
     f"Independent census of `corpus/SOURCES.md`: run the frozen census command "
     f"(`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin "
     f"chousa`), report exit and every warning line; count rows by status (mined/queued/rejected) and by tier "
     f"(A/B/C) with one command each; list any row whose `recheck` date is before 2026-10-23."),
    ("ScoutSkillTally", "scout",
     f"SKILL.md tally audit on a clone at {FREEZE}: extract every self-test number/range string in SKILL.md "
     f"(`grep -n 'cases\\|PASS (' SKILL.md`), then re-derive from committed bytes: the selftest banner (run "
     f"it), the case ranges per table row, the two round-34 counter rows, and the round-35 surfaces this wave "
     f"adds (they are NOT in SKILL.md yet — the L1 will add the pin paragraph and the witness tool; list the "
     f"SKILL.md lines that must change, with current text)."),
    ("ScoutFrontier", "scout",
     f"Frontier check: read `corpus/README.md` §Frontier and `corpus/QUALITY.md` (last 10 criteria); list which "
     f"frontier rows the round-35 work advances (grep pin, mechanism witness, keyed-engine class) and which "
     f"stay open, with the exact rows quoted. Also read `corpus/knowledge/` filenames and say whether any "
     f"entry already documents the keyed-engine output-equivalence class (a duplicate entry is a finding)."),

    # ---------------- connectors (2)
    ("ConnectorOverlap", "connector",
     f"Sibling-overlap scan (read-only): read `/home/vgpnk/Projects/shokunin/.ufo/reports/round-34/` (every "
     f"lane report present) and the round-35 reports that exist at the time you run. Build one table: lane | "
     f"surface | overlap with chousa's C1 (pinned-binary provenance) or C2 (mechanism witness / keyed-engine "
     f"equivalence) | import, duplicate or contradict. The session note says tameshi hit the same keyed class; "
     f"confirm or refute from its report bytes. Do not edit anything anywhere."),
    ("ConnectorCorpus", "connector",
     f"Corpus-level overlap: read every file in `{LANE}/corpus/knowledge/` (titles + first 15 lines) and "
     f"`{LANE}/corpus/lessons/` names; report whether a knowledge entry or lesson already states (a) the "
     f"dynamic-scope `local a=$1 b=${{#a}}` hazard, (b) PATH-resolved tool provenance, (c) output-equivalence "
     f"vs mechanism witnesses. If one exists, quote it and say whether the L1's planned entry must supersede "
     f"it rather than duplicate it."),

    # ---------------- scribes (6)
    ("ScribeKnowledgeKeyed", "scribe",
     f"Draft, in your own directory as `knowledge-keyed-engine-r35.md`, the corpus entry for the keyed-engine "
     f"output-equivalence class: (1) the class — an engine that fingerprints a counter's fixture (stable temp "
     f"prefix, record shape, root under /tmp) and answers from a cheaper exact search scores full marks "
     f"without running the mechanism under test; (2) why no output counter can kill it (it implements the "
     f"contract; killing it would be a false negative); (3) the three defenses and their costs — fixture "
     f"unpredictability (removes specific keys, not harness detection), mechanism witness (rules out "
     f"fingerprint-and-shortcut, not anti-instrumentation), and the honest limit; (4) the round-34 evidence "
     f"(`.ufo/waves/round-34/w2a2/MutC2Keyed.md`, ctl4/ctl6 37/37) and the round-35 evidence "
     f"(`{CLAIMS}`, K1/K2, receipts under `{MEAS}`). Cite sources as S0xx only where a SOURCES row exists; "
     f"never invent a row id. The L1 will file it."),
    ("ScribeLessonMistake", "scribe",
     f"Draft the round-35 `## Mistakes` row for `corpus/lessons/round-35.md`: class · evidence pointer · "
     f"captured-by · fix-shown-able-to-fail. The round's mined mistake is the `local a=$1 b=${{#a}}` "
     f"dynamic-scope read that shipped in round 34 and was caught by a non-author spot-check rather than by "
     f"any counter or selftest; the fix is `slen=${{#span}}` and the receipt is the probe "
     f"(`{PROBE}`: base 0 offsets / landed 1). Write it in the lesson file's existing style (read the last "
     f"two lessons), name the criterion that should have caught it (QUALITY row or a new one), and state what "
     f"would catch the next instance (a sweep over `local` lines with derived expansions)."),
    ("ScribeRunbook", "scribe",
     f"Draft, as `skill-runbook-r35.md`, the exact SKILL.md paragraph for the two round-35 surfaces: (a) the "
     f"grep pin — name the binary (`/usr/bin/grep`, GNU grep 3.12-modified on this host), the override "
     f"(`RESEARCH_GATE_GREP`, absolute, GNU only), the refusal marker (`research-gate: GREP_PROVENANCE "
     f"refused:`), the echo flag (`CHOUSA_GREP_PIN_ECHO=1` → `GATE_GREP: path=... source=... version=...`) "
     f"and the re-check command (a one-liner that prints the pin); (b) the witness tool — its command line, "
     f"what `WITNESS=` / `OUTPUT=` / `STAMPS` mean, the threshold, and its disclosed limit. Match SKILL.md's "
     f"existing row style (read it); the L1 applies it."),
    ("ScribeReportFacts", "scribe",
     f"Report-fact preflight (read-only): the L1's report will state — C1 before 0/9, after 9/9 on seeds "
     f"3501/3517, control 3/9; C2 before 0/2 (battery absent), after 2/2 on 3501/3517, stub-pass 0/2, "
     f"stub-fail landed-fail; selftest PASS (256 cases) with case ranges 252-253 / 254-256; slen base 0 / "
     f"landed 1; gate sha 1f2fb4f5; freeze commit 0e167649; landed commit e87c5d7e. Verify each against "
     f"committed bytes and the receipts, and list any number that cannot be re-derived with the stated "
     f"command, with the correct value."),
    ("ScribeScorecardRow", "scribe",
     f"Draft, as `scorecard-rows-r35.md`, the SCORECARD.md rows the L1 must append: the two claim rows "
     f"(axis | before → after | counting command | verdict) in the file's existing table shape, the two "
     f"capabilities rows (pinned-binary resolution + mechanism witness) with the exact evidence pointers, and "
     f"the planned-round-36 candidate list (read the current Planned section). Include the primary-source "
     f"citations only where a committed receipt backs them. Do not write to SCORECARD.md."),
    ("ScribeSourcesRows", "scribe",
     f"Draft, as `sources-rows-r35.md`, two SOURCES.md rows in the registry's exact column shape (read the "
     f"header and the last rows): S067 for execvp(3) (PATH search) and S068 for bash(1) (BASH_ENV + exported "
     f"functions). Use only locations and quotes you can verify yourself this round (open the installed man "
     f"pages, sha256 them, give decompressed line numbers and a <=25-word quote each, access date "
     f"2026-10-23), and fill status/tier/recheck per the contract. Never invent a quote; the L1 re-opens every "
     f"row before filing."),
]

spec = {
    "wave": "chousa-r35-w2",
    "milestone": "round-35 v2 wave: attack and re-derive C1 (grep pin) and C2 (mechanism witness), audit the claim record, the repairs and the round shape",
    "reportDir": ".ufo/waves/round-35/w2",
    "axes": ["operability", "calibration"],
    "context": CONTEXT,
    "items": [item(*t) for t in ITEMS],
}
counts = Counter(i["role"] for i in spec["items"])
attack = sum(1 for i in spec["items"] if i["role"] in ("reviewer", "critic", "mutation-tester"))
print("// seats=%d attack=%d (%.0f%%) mix=%s" % (len(spec["items"]), attack, 100.0 * attack / len(spec["items"]),
                                                    dict(counts)), file=sys.stderr)
assert 64 <= len(spec["items"]) <= 128, len(spec["items"])
assert attack * 4 >= len(spec["items"]), "attack share below 25%"
print(json.dumps(spec, indent=1))
