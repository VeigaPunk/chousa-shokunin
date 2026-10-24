#!/usr/bin/env python3
"""Generate the round-37 wave-1 spec (v1 policy, band 32-64)."""
import json, os, sys

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
GOD = open(os.path.expanduser("~/.agents/skills/godspeed/directive.md"), encoding="utf-8").read().rstrip("\n")
GATE = LANE + "/tools/research-gate.sh"
BASE = LANE + "/.ufo/waves/round-37/controls/base-gate-r37.sh"
C1 = LANE + "/corpus/evidence/round37/c1-count.py"
C2 = LANE + "/corpus/evidence/round37/c2-count.py"
CLAIMS = LANE + "/corpus/evidence/round37/claims.md"
OUT = LANE + "/.ufo/waves/round-37/w1"

CONTEXT = f"""# Goal
chousa lane (deep-research method), round 37, wave 1 of a v1 two-wave shape — build, re-derive and
first-falsify the round's two frozen claims. Lane repo {LANE} (jj-colocated; the branch tip was
b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65 at dispatch; read it with `git -C {LANE} rev-parse master`,
never `@{{u}}`). Fleet root /home/vgpnk/Projects/shokunin is READ-ONLY for every seat.

# The two claims (frozen: {CLAIMS})
C1 (operability): a claim's `sha256` revision pin is hashed through one pinned absolute `sha256sum`
and never through the caller's PATH (`sha256sum`/`cut`). Predicate
`python3 {C1} --gate {GATE} --seed N --receipt F` prints `CLAIM_PIN_PROVENANCE_MATCH=7/7`.
Base gate {BASE} (sha256 a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8) scores 2/7.
C2 (freshness): a `--pin` baseline is independent of the caller's `BASH_ENV`. Predicate
`python3 {C2} --gate {GATE} --seed N --receipt F` prints `PIN_CAPTURE_ENV_MATCH=7/7`; base scores 3/7.
Committed construction receipts: {LANE}/corpus/evidence/round37/receipts/.
Gate selftest on the dispatched bytes: `PASS (267 cases, 0 skipped)`.

# Seat rules (bind every seat)
- You are a LEAF: no spawns, no background jobs, no `task` calls, no swarm of your own.
- Never write outside your own report file under {OUT}/ and temp dirs you create under /tmp.
  Never mutate the lane repo, its jj state or its git index, the fleet repo, or a sibling lane.
  Never run `git add/commit/push/stash/checkout/switch/reset/pull` or any mutating `jj` command.
  Read-only git is fine (`log`, `show`, `diff`, `rev-parse`, `status`).
- Run counters with `C1_TMP`/`C2_TMP` pointing at a temp dir that EXISTS (mkdtemp runs inside it).
  Use fresh seeds (>= 37101 for wave work) and name your seed in your report.
- Evidence is a re-executed command plus its output; a naked assertion is not evidence.
- Tooling authorization (operator 2026-10-19): you may install or upgrade tools that help the task —
  read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate, record
  tool/version/channel/reason in your report). pacman guard (orchestrator ruling 2026-10-20): ALL
  pacman transactions are PAUSED host-wide; install via `uv tool`/`npx`/an official binary into
  ~/.local/bin, or file an L0 question. Never `-Sy`, `-Syu`, `-U`, `-R`, downgrade or restart a
  host service; if the pause lifts, dry-run `pacman -Sp --print-format '%n %v' <pkgs>` first and
  proceed only when no listed package is already installed.
- Every `Report:` trailer path this renderer gives you is relative to {LANE} — write it at
  {LANE}/<that path>, i.e. under {OUT}/.
- Agent ids and peer notes: never `agent://all`.

# Report shape (Markdown, <=120 lines)
`# <YourSeatName>` / `## Verdict` (one line) / `## Evidence` (commands + observed output, absolute
paths, seeds) / `## Findings` (numbered, each with the pointer that grounds it) / `## Limits`.
"""

def item(name, role, text):
    return {"name": name, "role": role, "prompt": "/skill:godspeed\n" + GOD + "\n\n" + text.strip() + "\n"}

I = []
A = I.append

A(item("ExecC1BaseRederive", "executor", f"""
# Target
{C1} against {BASE}.
# Do
Run it twice on two fresh seeds (37101, 37123) with `--tmp` a temp dir you create and `--receipt`
under {OUT}/ExecC1BaseRederive/. Report the exact `CLAIM_PIN_PROVENANCE_MATCH=` line, exit codes, and
which scenarios fail with which observed tuples. State whether the receipt `gate_sha256` equals the
base gate's sha256 you re-derive yourself with `sha256sum`.
# Acceptance
Two receipts committed under your report dir, both 2/7, with the five failing cell names."""))

A(item("ExecC1LandedRederive", "executor", f"""
# Target
{C1} against {GATE}.
# Do
Run it on fresh seeds 37111 and 37133, receipts under {OUT}/ExecC1LandedRederive/. Report the
`CLAIM_PIN_PROVENANCE_MATCH=` lines, exit codes, and re-derive `sha256sum {GATE}` to compare with the
receipt `gate_sha256`.
# Acceptance
Two receipts, both 7/7 exit 0, gate sha256 named and matching."""))

A(item("ExecC2BaseRederive", "executor", f"""
# Target
{C2} against {BASE}.
# Do
Run it on fresh seeds 37201 and 37223, receipts under {OUT}/ExecC2BaseRederive/. Report the
`PIN_CAPTURE_ENV_MATCH=` lines, exit codes, and for each failing scenario the expected-vs-observed
tuple (pin_rc, pin_file, baseline_echo_lines, drift_rc, drift_line).
# Acceptance
Two receipts, both 3/7, the four separation cells named with their observed drift lines."""))

A(item("ExecC2LandedRederive", "executor", f"""
# Target
{C2} against {GATE}.
# Do
Run it on fresh seeds 37211 and 37311, receipts under {OUT}/ExecC2LandedRederive/. Report the
`PIN_CAPTURE_ENV_MATCH=` lines and exit codes, and re-derive the gate sha256 from the receipts.
# Acceptance
Two receipts, both 7/7 exit 0."""))

A(item("ExecSelftestRederive", "executor", f"""
# Target
`bash {GATE} --selftest`.
# Do
Run it once from {LANE}; save the whole log under {OUT}/ExecSelftestRederive/selftest.log. Report the
last line verbatim, the exit code, the `skip-case` lines, and the case numbers/names of
`r2-hash-fault-pinned`, `claims-sha-path-shim`, `claims-sha-cut-shim`, `claims-sha-stdin-hold`,
`pin-bashenv-echo`, `drift-bashenv-echo`, `pin-bashenv-root`.
# Acceptance
`RESEARCH_GATE_SELFTEST: PASS (267 cases, 0 skipped)` with the seven case lines quoted from the log."""))

A(item("ExecNoHarmPin", "executor", f"""
# Target
The gate's pinned observables on the dispatched bytes: claims fixture, chain fixture, broken chain
control, and the three archived inputs.
# Do
From {LANE} run: `bash {GATE} verify-claims corpus/fixtures/claims-r2.jsonl --root .`; `bash {GATE}
verify-chain corpus/fixtures/chain-r3.md --root .`; `bash {GATE} verify-chain
corpus/fixtures/chain-r3-broken.md --root .`; and `bash {GATE} verify
../research/deep-research-2026-09-28/<A|B|C>-*.md --root ..` for the three archives. Report each
tally line (`VERDICT_BEARING_CLAIMS=`, `RESOLVED_HOPS=`, `RESEARCH_GATE: `) and exit code, and
compare against the round-36 pins stated in {LANE}/SCORECARD.md (claims 17/17, chain 17/22, broken
1/2, archives 3/3).
# Acceptance
A table of six runs with observed tallies; any deviation from the round-36 pins is called out as harm."""))

A(item("ExecMutGateC1", "executor", f"""
# Target
A gate mutant that removes ONLY C1's fix, in a scratch copy.
# Do
Copy {GATE} to /tmp and replace the pinned claim-pin hash line
(`sha_actual=$( {{ sha256_hex_stream < "$path"; }} 2>/dev/null ) || sha_actual=unreadable`) with the
old `sha_actual=$(sha256sum < "$path" 2>/dev/null | cut -d' ' -f1 || true)`. Run BOTH counters against
the mutant on fresh seeds. Report both counts and exit codes.
# Acceptance
C1 below 7/7 (expected 2/7) while C2 stays 7/7 — the separability evidence. If either differs from
that expectation, report the exact observed counts and say the claims are not separable as stated."""))

A(item("ExecMutGateC2", "executor", f"""
# Target
A gate mutant that removes ONLY C2's fix, in a scratch copy.
# Do
Copy {GATE} to /tmp and delete `-u BASH_ENV` from the `gate_canonical_capture` child `env` line. Run
BOTH counters against the mutant on fresh seeds. Report both counts and exit codes.
# Acceptance
C2 below 7/7 (expected 3/7) while C1 stays 7/7 — the separability evidence. If either differs, report
the exact observed counts."""))

A(item("ExecMutC1Counter", "executor", f"""
# Target
The C1 counter's own expectation table.
# Do
Copy {C1} to /tmp, restore the inherited (wrong) expectation for `sha-shim-other`
(`(1, "DRIFT", "stale", True)`) and run it against {GATE} on a fresh seed. Then write a second mutant
that flips `hold-match` to expect DRIFT. Report both counts.
# Acceptance
The first mutant scores 6/7 (not 7/7) and the second fails the hold — evidence that the counter can
fail and that the corrected expectation is load-bearing."""))

A(item("ExecMutC2Counter", "executor", f"""
# Target
The C2 counter's assertions.
# Do
Copy {C2} to /tmp and weaken `baseline_echo_lines`/`drift_line` checks for `env-echo-pin` (accept any
drift line). Run it against {BASE} on a fresh seed. Report the count.
# Acceptance
A count above the base's 3/7 (state the exact number) — proof that the assertion, not the fixture, is
what separates."""))

A(item("ScoutC1Counter", "scout", f"""
# Target
{C1} (read it whole).
# Do
For each of the seven scenarios report: id, the fixture it builds, the assertion it makes, its pass
condition, and line numbers. Then name every vacuity candidate: a scenario that could pass without
the fix being present, or whose assertion is weaker than its name.
# Acceptance
A per-scenario table plus a numbered vacuity list, each entry naming the line range it attacks."""))

A(item("ScoutC2Counter", "scout", f"""
# Target
{C2} (read it whole).
# Do
Same analysis as for a counter review: per-scenario fixture/assertion/pass-condition/line numbers,
then vacuity candidates (e.g. a scenario that passes on the base gate, a hold that asserts nothing
the base lacks, a shim the counter never observes).
# Acceptance
A per-scenario table plus a numbered vacuity list with line ranges."""))

A(item("ScoutPinHelpers", "scout", f"""
# Target
The `sha256_pin_bin`, `sha256_hex_stream` and `sha256_hex_file` helpers and the `verify_claims`
revision-pin block in {GATE}.
# Do
Read the code and report: every call site of each helper, what each does on a missing/unexecutable
binary, what happens to a sha256sum that prints extra whitespace or a leading backslash, and whether
the `verify-all --json` manifest path and the claim pin now share one resolution. Name any remaining
`PATH` lookup on a hashing tool in the gate (`grep -n 'sha256sum\\|shasum\\|md5sum' {GATE}`).
# Acceptance
A call-site table and a numbered list of residual PATH lookups with line numbers (or the sweep that
found none)."""))

A(item("ScoutCaptureEnv", "scout", f"""
# Target
`gate_canonical_capture` and every other place {GATE} builds a child environment.
# Do
List every `env -u ...` invocation and every `bash "$SELF"` child, with line numbers, and for each
name which variables are scrubbed and which startup hooks (`BASH_ENV`, `ENV`, `SHELLOPTS`,
`BASHOPTS`, `TMPDIR`, `PATH`) remain inherited. Read the GNU Bash manual section on startup files if
you need the semantics (cite the URL you opened).
# Acceptance
A site table (line, child, scrubbed set, inherited hooks) and a ranked residual list."""))

A(item("ScoutSelftestNames", "scout", f"""
# Target
Selftest cases 240 and 262-267 in {GATE} (grep the case labels).
# Do
For each case report the name, the mechanism it injects, the assertions it makes, and whether the
assertions would fail if the named mechanism were absent (QUALITY 52). Pay attention to
`r2-hash-fault-pinned` (userns bind) and to whether its skip path can silently pass.
# Acceptance
A per-case table with a PASS/weak verdict per case and the line numbers."""))

A(item("ScoutR2FaultCase", "scout", f"""
# Target
The re-based `r2-hash-fault-pinned` case and the namespace harness it reuses (`ns_probe`, and the r14
cases 103-106).
# Do
Establish, by reading and by one re-execution you design (`unshare --user --map-root-user --mount`,
bind a failing stub over /usr/bin/sha256sum, run `verify-claims` on a correct pin), whether the case
really fails closed to `actual=unreadable`. Report the commands and output.
# Acceptance
A re-executed demonstration plus a judgement on whether the skip path (no userns) is honest."""))

A(item("ScoutPathLookups", "scout", f"""
# Target
Unaided `PATH` lookups in the gate's receipt/identity paths.
# Do
Sweep {GATE} for commands invoked by bare name in hashing, pinning, drift, manifest and claims code
paths (`grep -nE '(^|[^/[:alnum:]_])(sha256sum|cut|grep|sed|awk|tr|head|tail|mktemp|readlink|stat) '`),
and for each hit say whether a caller-controlled PATH can change an observable verdict or receipt.
# Acceptance
A hit table with a verdict per hit and the line numbers of any real exposure."""))

A(item("RevC1Claim", "reviewer", f"""
# Target
C1's section of {CLAIMS} against {C1}.
# Do
Check that the frozen predicate sentence equals the counter's code condition, that the kill rule can
actually fire, that the "cheapest control" claim is true (the base gate is the control), and that the
named limits cover what the scenarios do not test. Report contradictions with line pointers.
# Acceptance
A PASS/FAIL per checked item with file:line citations; FAIL entries name the exact mismatch."""))

A(item("RevC2Claim", "reviewer", f"""
# Target
C2's section of {CLAIMS} against {C2}.
# Do
Same checks as RevC1Claim for C2: predicate == code condition, kill rule firable, control true,
limits honest (BASH_ENV-only scope; the gate process already sourced the file), separability
paragraph verifiable.
# Acceptance
A PASS/FAIL per checked item with file:line citations."""))

A(item("RevGateC1Code", "reviewer", f"""
# Target
The C1 hunk in {GATE}: `sha256_pin_bin`, `sha256_hex_stream`, `sha256_hex_file`, and the `verify_claims`
revision-pin replacement.
# Do
Review for correctness: rc propagation, the `out=` suffix-strip against a backslash-prefixed name,
`2>/dev/null` swallowing a real error, the `|| sha_actual=unreadable` ordering, and whether the
`[[ $sha_actual =~ ^[0-9a-f]{64}$ ]]` guard is still reachable. Name any input that makes the new code
worse than the old.
# Acceptance
A numbered finding list with severity and line numbers; "no findings" needs the sweep you ran."""))

A(item("RevGateC2Code", "reviewer", f"""
# Target
The C2 hunk in {GATE}: the `-u BASH_ENV` addition and selftest cases 265-267.
# Do
Review for correctness and scope: is `BASH_ENV` the only hook the child bash reads, does the scrub
cover both `--pin` and `--drift`, could the change hide a real environment difference (e.g. a caller
whose BASH_ENV is required for the gate to run), and do cases 265-267 assert the mechanism or a proxy.
# Acceptance
A numbered finding list with severity and line numbers."""))

A(item("RevSelftestBump", "reviewer", f"""
# Target
The SKILL.md Gates table changes in this round (case count 261 -> 267, the r37 case ranges, the new
`research-gate round-37 counters` row) against the actual selftest output.
# Do
Diff the claim against a real selftest run's case list: do the cited ranges (240, 262-264, 265-267)
match the printed case numbers and names? Is `PASS (267 cases, 0 skipped)` the observed string? Does
the new counters row's before-values match the committed receipts?
# Acceptance
A per-citation PASS/FAIL table; every FAIL cites the observed line."""))

A(item("RevCounterHygiene", "reviewer", f"""
# Target
Both counters ({C1}, {C2}) for harness contract: exit codes 0/1/2, temp-dir requirement, receipt
schema, no network, no writes outside temp + receipt.
# Do
Verify each contract by reading and by one run with a missing gate path, a missing temp dir, and a
read-only receipt path (all under /tmp). Report observed exits and messages.
# Acceptance
A contract table with the observed exit for each misuse case."""))

A(item("CritC1", "critic", f"""
# Target
Falsify C1 on {GATE} without editing the gate.
# Do
Try at least four attacks on the claim "no PATH shim can move a pin verdict": (a) a shim earlier on
PATH for `cut` plus `sha256sum`; (b) a PATH entry containing a directory named `sha256sum`; (c) a
`BASH_ENV` that defines a `sha256sum` function; (d) a caller whose `PATH` is empty. For each, run a
one-claim fixture with a correct pin and a tampered source and report the verdict.
# Acceptance
Observed verdicts per attack; any attack that moves a verdict is a falsification and is reported as
such with the exact command."""))

A(item("CritC2", "critic", f"""
# Target
Falsify C2 on {GATE} through a startup vector other than `BASH_ENV`.
# Do
Test: `SHELLOPTS`/`BASHOPTS` carried in the environment, a `--posix` shebang analogue (run the gate
as `bash --posix`), `TMPDIR` pointing at a directory that does not exist, and `ENV` set for a `sh`
invocation. For each, pin under the hostile environment and drift plain; report `GATE_DRIFT:` lines.
# Acceptance
A table of vectors with observed drift lines; any phantom drift is a falsification of the claim's
scope sentence and must be reported as such."""))

A(item("CritClaimSizing", "critic", f"""
# Target
The claim-sizing rule (round prompt section 9): a target must be one a do-nothing control cannot
reach.
# Do
Construct the cheapest do-nothing control you can imagine for each claim (e.g. a lane commit that
touches neither gate nor counters) and score it with the frozen counters, using the base gate where
the control would leave the code unchanged. Show the counts. Then attack the choice of 7 scenarios:
would fewer scenarios still separate?
# Acceptance
Two control scores with receipts and a paragraph on whether 7/7 is reachable without the work."""))

A(item("CritErrata", "critic", f"""
# Target
The three errata in {CLAIMS} and the counter docstring erratum in {C1}.
# Do
Verify each erratum against the base gate's behaviour: is the inherited expectation really wrong
(run the inherited table on the landed gate and show 6/7)? Is the `r2-hash-fault-shim` case really
impossible under the fix? Is attempt 1's gate edit really the C1 fix (diff the base gate against the
dispatched gate)?
# Acceptance
Per-erratum PASS/FAIL with the command that shows it."""))

A(item("CritSeparability", "critic", f"""
# Target
The separability paragraph in {CLAIMS}.
# Do
Independently of ExecMutGateC1/C2, produce two scratch gate copies: one with only the C1 change
reverted, one with only the C2 change reverted; run both counters against each and report the 2x2
matrix. Also check the weaker claim in that paragraph: C1's counter reads no `GATE_DRIFT` line and
C2's fixtures carry no `sha256` field — verify both by reading the counters.
# Acceptance
The 2x2 matrix (four counts) and a PASS/FAIL on the two reading claims."""))

A(item("ConnSiblingOverlap", "connector", f"""
# Target
Sibling-overlap scan against the other shokunin lanes.
# Do
Search /home/vgpnk/Projects/shokunin/*-shokunin/{{corpus,SKILL.md,LOG.md}} and the fleet
.ufo/reports/round-36/*.md (read-only) for work on PATH provenance, environment scrubbing, pin/drift
contracts, or shell startup files. Report overlaps (same class, same surface) and whether chousa's
round-37 claims duplicate a sibling's landed work.
# Acceptance
A numbered overlap list with paths and one line each on whether it is a duplicate, a complement, or
out of province."""))

A(item("SentC1", "sentinel", f"""
# Target
Security review of C1's residual surface on {GATE}.
# Do
Enumerate exactly what a caller must control to still move a claim-pin verdict after the fix: the
pinned binary's path, mount privileges, `/bin` aliasing, `LD_PRELOAD`, and any remaining shell
function import. For each, state whether the claimed sentence ("no PATH shim can move a pin verdict")
is violated or merely out of scope, and whether the claims file names it.
# Acceptance
A numbered residual-surface list with a violated/out-of-scope verdict per item and the claims-file
line that covers it (or "uncovered")."""))

A(item("SentC2", "sentinel", f"""
# Target
Security review of C2's residual surface on {GATE}.
# Do
Enumerate what a caller-supplied `BASH_ENV` can still do to the gate process itself after the scrub
(function definitions, `readonly -f grep`, aliases, `set -x` to stderr, `TMPDIR`), and whether any of
it can change a `--pin`/`--drift` verdict. Test the two you judge most likely and report observed
outcomes.
# Acceptance
A numbered list with a tested/untested flag per item and an explicit statement of which limits the
claims file already names."""))

A(item("MutC1CaseVacuity", "mutation-tester", f"""
# Target
Selftest cases 262-264 as a detector.
# Do
In a scratch copy of the gate, mutate the case bodies so they pass without the mechanism (e.g. drop
the `CLAIM_SOURCE_REVISION_MISMATCH` assertion, or accept any exit). Show the mutant still prints
`PASS (267 cases...)`. Then show the C1 counter still catches the *gate* regression (revert the fix
in the same mutant) — i.e. the counter, not the case, is the claim's detector.
# Acceptance
Mutant lines, the selftest line it prints, and the counter count on the same mutant."""))

A(item("MutC2CaseVacuity", "mutation-tester", f"""
# Target
Selftest cases 265-267 as a detector.
# Do
Same exercise for C2: make cases 265-267 pass while the gate keeps its old behaviour (e.g. compare
only exit codes), show the selftest stays PASS, and run the C2 counter against that gate copy to show
it drops below 7/7.
# Acceptance
Mutant lines, selftest line, and counter count."""))

A(item("MutC1CutAbs", "mutation-tester", f"""
# Target
The claim's wording "never through the caller's PATH (`sha256sum` or `cut`)".
# Do
Mutate the gate to use an ABSOLUTE `/usr/bin/cut` after the pinned hash (harmless) and separately to
use `/usr/bin/cut` as the only hasher (broken). Run the C1 counter on each. Report counts.
# Acceptance
Both counts plus a sentence on whether the counter distinguishes "absolute tool, wrong job" from the
claimed regression."""))

A(item("RevC1Intent", "revenger", f"""
# Target
The inherited attempt-1 counter expectation (`sha-shim-other` = DRIFT/stale) and the round-36
SCORECARD `Planned` sentence that named this claim.
# Do
Recover the original intent from the committed history (`git -C {LANE} log -p -- corpus/evidence/round37
` will show nothing if inherited bytes were uncommitted; then read round-36 SCORECARD and
corpus/evidence/round36/claims.md §Erratum) and state whether the corrected expectation is what the
planned claim intended. Say plainly if the intent is unrecoverable.
# Acceptance
An intent reconstruction with pointers, or an explicit "unrecoverable" with the sweep that found no
record."""))

A(item("RevC2Prior", "revenger", f"""
# Target
Round-36's R1 repair and claims §Erratum 7 (the `--pin` capture environment), as committed in
{LANE}/SKILL.md and {LANE}/corpus/evidence/round36/claims.md.
# Do
Read what R1 claimed to fix and its stated residual (`-u BASH_ENV` at 3921). Show, by reading the
committed round-36 gate bytes (`git -C {LANE} show master:tools/research-gate.sh`) and by one run,
that the residual was real and that round 37 closes exactly it — no more, no less.
# Acceptance
A quotation of R1's own words, the residual line, and a closed/no-more-no-less verdict."""))

A(item("SimpGateHelpers", "simplifier", f"""
# Target
The two new helpers and the `-u BASH_ENV` change in {GATE}.
# Do
Name any dead field, redundant branch or duplicated resolution that can be deleted without changing
observed behaviour ({GATE} --selftest and both counters are the behaviour). For each candidate, state
the deletion, the risk, and the command that would prove behaviour preserved. Do not edit the lane.
# Acceptance
A numbered deletion list with a keep/delete recommendation per item; "nothing" needs the sweep."""))

A(item("ScribeKnowledgeC1", "scribe", f"""
# Target
A draft knowledge entry `corpus/knowledge/claim-pin-provenance-r37.md` (write your draft ONLY at
{OUT}/ScribeKnowledgeC1/entry.md).
# Do
Header keys `source:`, `verified-at: 2026-10-23`, `recheck: on-release`. Body: the rule (a pin is a
claim about bytes; resolve the hasher absolutely, once, and never through `cut`), the mechanism
(`sha256_pin_bin` -> `/usr/bin/sha256sum` then `/bin/sha256sum`; stdin hashing keeps `\\`-prefixed
names safe), the before/after (2/7 -> 7/7 with the counter command), the selftest cases, and the
limits (root/mount namespace control is out of scope). Cite CWE-426 with a <=25-word located quote
you take from https://cwe.mitre.org/data/definitions/426.html (open it yourself; quote the
Description or the "fully-qualified pathnames" mitigation row).
# Acceptance
A ready-to-land draft, every claim with a pointer, the S-id placeholder named as S072."""))

A(item("ScribeKnowledgeC2", "scribe", f"""
# Target
A draft knowledge entry `corpus/knowledge/pin-capture-env-r37.md` (draft at
{OUT}/ScribeKnowledgeC2/entry.md).
# Do
Header keys `source:`, `verified-at: 2026-10-23`, `recheck: on-release`. Body: a pinned baseline is
a claim about the gate, so its capture must not inherit the caller's startup file; GNU Bash reads
`$BASH_ENV` in a non-interactive shell; the scrub list must name that hook, not only the app's own
variables; before/after (3/7 -> 7/7), selftest cases 265-267, and the limits (the gate process
itself already sourced the file; `ENV`/`SHELLOPTS`/`TMPDIR` uncovered). Cite
https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html with a <=25-word quote you
open yourself.
# Acceptance
A ready-to-land draft with pointers, the quote, and the S-id placeholder named as S071."""))

spec = {
    "wave": "chousa-r37-w1",
    "milestone": "round-37 wave 1 (v1 build+falsify): re-derive and attack the two frozen claims, open sources, draft frontier entries",
    "reportDir": ".ufo/waves/round-37/w1",
    "axes": ["operability", "freshness"],
    "context": CONTEXT,
    "items": I,
}
out = sys.argv[1] if len(sys.argv) > 1 else LANE + "/.ufo/waves/round-37/w1-spec.json"
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8") as fh:
    json.dump(spec, fh, indent=1)
    fh.write("\n")
print("items", len(I), "->", out)
