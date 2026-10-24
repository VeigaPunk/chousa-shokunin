#!/usr/bin/env python3
"""Generate the round-38 wave-1 spec (v1 policy, band 32-64; 32 seats)."""
import json, os

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
GOD = open(os.path.expanduser("~/.agents/skills/godspeed/directive.md"), encoding="utf-8").read().rstrip("\n")
GATE = LANE + "/tools/research-gate.sh"
BASE = LANE + "/.ufo/waves/round-37/controls/base-gate-r37.sh"
C1 = LANE + "/corpus/evidence/round38/c1-count.py"
C2 = LANE + "/corpus/evidence/round38/c2-count.py"
VRFY = LANE + "/corpus/evidence/round38/verify-receipts.py"
CLAIMS = LANE + "/corpus/evidence/round38/claims.md"
EXPECT = LANE + "/corpus/evidence/round38/expectations.jsonl"
R37C1 = LANE + "/corpus/evidence/round37/c1-count.py"
FREEZE = "504c1d2a1257a9ac6e5d752dcaf3f0bb0a35d05f"
OUT = LANE + "/.ufo/waves/round-38/w1"

CONTEXT = f"""# Goal
chousa lane (deep-research method), round 38, wave 1 of a v1 two-wave shape — re-derive and
first-falsify the round's two frozen claims, build the attack fixtures, and draft the frontier
material. Lane repo {LANE} (jj-colocated; the branch tip was {FREEZE} at dispatch; read it with
`git -C {LANE} rev-parse master`, never `@{{u}}`). Fleet root /home/vgpnk/Projects/shokunin is
READ-ONLY for every seat.

# The two claims (frozen: {CLAIMS}; expectations frozen: {EXPECT})
C1 (operability, lowest axis 3/10): the canonical pin capture's child runs through ONE pinned
absolute `env` (RESEARCH_GATE_ENV override, GNU-reporting, refused exit 2 ENV_PROVENANCE), so a
caller-exported function `env` (BASH_FUNC_env%%) cannot interpose on the capture. Predicate
`python3 {C1} --gate {GATE} --seed N --receipt F` prints `ENV_PIN_CAPTURE_MATCH=7/7`.
Base gate {BASE} (sha256 a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8)
scores 2/7.
C2 (calibration): every round-38 counter receipt binds gate_sha256_pre==gate_sha256_post (measured
by the counter; a changed gate refuses exit 2, NO receipt), counter_sha256, expect_sha256 and
receipt_sha256; `{VRFY}` re-derives all bindings and fails closed. Predicate
`python3 {C2} --gate {GATE} --seed N --receipt F` prints `RECEIPT_BINDING_MATCH=7/7`; the same
counter against the r37 counter ({R37C1}) scores 0/7.
Committed construction receipts: {LANE}/corpus/evidence/round38/receipts/.
Gate selftest on the dispatched bytes: `PASS (272 cases, 0 skipped)`.

# Seat rules (bind every seat)
- You are a LEAF: no spawns, no background jobs, no `task` calls, no swarm of your own.
- Never write outside your own report file under {OUT}/ and temp dirs you create under /tmp.
  Never mutate the lane repo, its jj state or its git index, the fleet repo, or a sibling lane.
  Never run `git add/commit/push/stash/checkout/switch/reset/pull` or any mutating `jj` command.
  Read-only git is fine (`log`, `show`, `diff`, `rev-parse`, `status`).
- Run counters with `C1_TMP`/`C2_TMP` pointing at a temp dir that EXISTS (mkdtemp runs inside it).
  Use fresh seeds (>= 38201 for wave-1 work) and name your seed in your report.
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

RULES = """Time-box: return within 15 minutes with your best findings+evidence; partial results are acceptable.
You are an independent leaf: never block on or wait for another seat; if a needed artifact is absent, record the dependency as a finding and return."""

def item(name, role, text):
    return {"name": name, "role": role,
            "prompt": "/skill:godspeed\n" + GOD + "\n\n" + text.strip() + "\n\n" + RULES + "\n"}

I = []
A = I.append

# ---- executors (6) ----
A(item("ExecC1Rederive", "executor", f"""
Re-derive C1's before and after on fresh seeds. Commands (from {LANE}):
`mkdir -p /tmp/your-tmp && C1_TMP=/tmp/your-tmp python3 {C1} --gate {BASE} --seed 38211 --receipt /tmp/c1-base-38211.json` (expect ENV_PIN_CAPTURE_MATCH=2/7)
and the same with --gate {GATE} on seeds 38211 and 38231 (expect 7/7, predicate_holds=true).
For each run report the full per-scenario PASS/FAIL lines and the receipt's gate_sha256 /
counter_sha256 / expect_sha256 / receipt_sha256 values (jq or python). Confirm both after-receipts
verify: `python3 {VRFY} --receipt /tmp/c1-... --gate {GATE} --counter {C1}`.
"""))
A(item("ExecC2Rederive", "executor", f"""
Re-derive C2's before and after on fresh seeds (note: the c2 counter runs the c1 counter inside,
each full run takes ~1-2 min). From {LANE}:
`mkdir -p /tmp/your-tmp && C2_TMP=/tmp/your-tmp python3 {C2} --counter {R37C1} --gate {GATE} --seed 38221 --receipt /tmp/c2-base-38221.json` (expect RECEIPT_BINDING_MATCH=0/7)
`C2_TMP=/tmp/your-tmp python3 {C2} --gate {GATE} --seed 38221 --receipt /tmp/c2-after-38221.json` and a second seed 38241 (expect 7/7).
Verify both after-receipts with {VRFY} (counter {C2}). Report per-scenario lines and all receipt bindings.
"""))
A(item("ExecF1Replay", "executor", f"""
Independently rebuild the round-37 residual F1 attack from {LANE}/.ufo/waves/round-37/residual/RevC1FreshSeed.md
lines 31-60: a gate shim that answers its first invocation from its own bytes and then restores the
target gate over itself, so post-run bytes equal the target. Run the r38 c1 counter ({C1}) against
your shim with the target {GATE}: expect exit 2, NO receipt, stderr naming the changed gate.
Then run the r37 c1 counter ({R37C1}) against the same shim: expect a 7/7 receipt whose
gate_sha256 equals the target's (the vulnerability the fix closes). Report both verbatim.
"""))
A(item("ExecEnvFnHarness", "executor", f"""
Build a SECOND delivery mechanism for the C1 attack and confirm the fix covers both. The counter
delivers the function through a raw BASH_FUNC_env%% env var; your harness instead runs a real
child bash that defines and exports the function (`bash -c 'env() {{ ...; }}; export -f env; exec
bash "$1" --pin "$2"' _ {GATE} BASELINE`), then pins under (a) the echo re-add, (b) the CHOUSA_ROOT
re-add, (c) the suppress function. Run each against the BASE gate {BASE} (expect the captures
moved/failed: echo line embedded, foreign-root drift, or capture failure) and against the LANDED
gate {GATE} (expect every pin rc=0, zero GATE_GREP lines, drift `GATE_DRIFT: none`). Show both.
"""))
A(item("ExecNoHarm", "executor", f"""
Run the pinned no-harm battery on the landed gate from {LANE} and report verbatim outputs:
`bash {GATE} --selftest | tail -3` (expect PASS, 272 cases);
`bash {GATE} verify-claims {LANE}/corpus/fixtures/claims-r2.jsonl --root ..` (expect VERDICT_BEARING_CLAIMS=17/17 CLEAN);
`bash {GATE} verify-chain {LANE}/corpus/fixtures/chain-r3.md --root ..` (expect RESOLVED_HOPS=17/22 CLEAN);
`bash {GATE} verify-all {LANE}/corpus/fixtures/full-r6-broken.md --claims {LANE}/corpus/fixtures/full-r6-broken.claims.jsonl --root ..` (expect DRIFT, drift-sections=2);
the archives one-liner from SCORECARD.md (expect VERDICT_BEARING_EXPORTS=3/3).
"""))
A(item("ExecDoNothingCtl", "executor", f"""
Prove the do-nothing controls cannot reach the frozen targets. From {LANE}:
(1) r38 c1 counter against the BASE gate on a fresh seed — confirm 2/7 (the binding fields alone
must not lift the score);
(2) r38 c2 counter against the base gate {BASE} with the DEFAULT r38 c1 counter — confirm 7/7
(binding is gate-agnostic; the base receipt for C2 used the landed gate, show the gate choice does
not matter);
(3) r37 c1 counter ({R37C1}) against the LANDED gate on a fresh seed — confirm it can still score
its own 7/7 (its predicate is about sha shims, which the landed gate still passes: c1's counter is
C2's control, not C1's). Report each verbatim.
"""))

# ---- scouts (3) ----
A(item("ScoutGatePins", "scout", f"""
Per-surface reconnaissance of {GATE}: enumerate every remaining BARE external-tool invocation
(env, bash, mktemp, sort, sed, grep outside the pinned wrapper, timeout, cat, rm...) with
line numbers, classify each as capture-channel (inside gate_canonical_capture and its callees),
pin-machinery, selftest-only, or record-verification, and say which class each remaining bare call
is a witness surface for (the C1 named-limits audit). Also report whether the r38 env pin has any
other call site besides the capture. No edits anywhere.
"""))
A(item("ScoutCounters", "scout", f"""
Reconnaissance of {C1}, {C2}, {VRFY} and {EXPECT}: trace every code path that could bypass the
frozen expectations (is the expectations file the only source of expectations? any hardcoded
fallback?), every sha computation (which file, when read), the receipt_digest canonicalization
(is it stable under json round-trip? does verify recompute identically?), and any parse looseness
in the drift-line / refusal observations (last-match vs first-match, substring vs anchored). No
edits anywhere.
"""))
A(item("ScoutFrontier", "scout", f"""
Reconnaissance of the frontier surfaces: {LANE}/corpus/SOURCES.md (current row count and tier/status
histograms via the census commands in /home/vgpnk/Projects/shokunin/CORPUS.md; the standing W04
warnings and which rows they name; the exact current S068/S070/S071 rows), corpus/README.md's
frontier paragraph, and the local source files /usr/share/info/bash.info.gz (file sha256, the
'Shell Functions' node, decompressed lines 1455-1470) and /usr/share/man/man1/sha256sum.1.gz
(decompressed lines 1-25, where the `-c, --check` entry sits relative to .SH DESCRIPTION). Report
what a new S072/S073 row must contain to conform to contract v1. No edits anywhere.
"""))

# ---- scribes (3) ----
A(item("ScribeKnowledgeC1", "scribe", f"""
Draft the knowledge entry `corpus/knowledge/env-pin-capture-r38.md` INSIDE your report (the L1
integrates; you cannot write the lane). Ground it only in: {CLAIMS} (C1 body + limits),
{C1}, and the committed receipts {LANE}/corpus/evidence/round38/receipts/. The entry must open
with the provenance trio (source: citing the bash.info row S072 by path + the claims.md evidence;
verified-at: 2026-10-24; recheck: on-release), then the mechanism (BASH_FUNC_env%% delivery, the
three attacks, the pinned-absolute-env fix), the frozen observable (2/7 -> 7/7 across seeds
38001/38011 + wave seeds), and the named limits verbatim from claims.md. Follow the shape of
{LANE}/corpus/knowledge/pin-capture-env-r37.md.
"""))
A(item("ScribeKnowledgeC2", "scribe", f"""
Draft the knowledge entry `corpus/knowledge/receipt-binding-r38.md` INSIDE your report. Ground it
only in {CLAIMS} (C2 body + limits), {C2}, {VRFY}, and the committed receipts. Provenance trio
first (source: the round-37 residual RevC1FreshSeed.md findings F1/F4 as the motivating evidence
plus this round's receipts; verified-at: 2026-10-24; recheck: on-release), then the binding model
(pre==post refusal, counter/expect/receipt digests, verify-receipts re-derivation, legacy
fail-closed), the frozen observable (0/7 -> 7/7), and the named limits. Follow the shape of
{LANE}/corpus/knowledge/claim-pin-provenance-r37.md.
"""))
A(item("ScribeSources", "scribe", f"""
Open the two local sources and draft the two new SOURCES.md rows INSIDE your report (the L1
integrates). (1) /usr/share/info/bash.info.gz: file sha256, Node 'Shell Functions' (3.3), the
exported-functions sentence at decompressed lines 1460-1463 — quote it verbatim (<=25 words, count
them) and give the exact line range you verified. (2) /usr/share/man/man1/sha256sum.1.gz: confirm
the S070 anchor defect (decompressed lines 19-20, the `-c, --check` entry, sit under .SH
DESCRIPTION at line 8, not under .SH SYNOPSIS at line 5) and draft the correction row whose
teaches opens `supersedes S070 —`. Draft both rows as full contract-v1 table rows (11 columns,
no `|` inside cells) with id S072 and S073, tier/scope/kind/status/opened/recheck/used-by filled.
Also draft the round-38 lesson `## Gate` entries for both rows (URL/path, access date, quote).
"""))

# ---- reviewers (6) ----
A(item("RevClaimsC1", "reviewer", f"""
Review the frozen C1 claim in {CLAIMS} against its counter {C1} and expectations {EXPECT}:
does the code condition (`matched == 7`) implement exactly the frozen P1 sentence? Is the kill
rule falsifiable (name the concrete run that would kill C1)? Does the claim text contain any
universal clause or overreach beyond what the seven cells measure (QUALITY 52/54 class)? Are the
named limits honest and complete given the seat-visible attack surface (bash-function witness,
noexec, loader env, version self-report)? Report defects by severity; do not edit anything.
"""))
A(item("RevClaimsC2", "reviewer", f"""
Review the frozen C2 claim in {CLAIMS} against {C2} and {VRFY}: same questions as RevClaimsC1
for P2 — code condition vs frozen sentence, kill-rule feasibility, overreach, limit honesty
(legacy receipts, F2 residual, seed namespacing). Specifically check: can RECEIPT_BINDING_MATCH=7/7
be reached by a do-nothing tree? (The claims.md names the r37-counter control at 0/7 — re-derive
it on one fresh seed and confirm.) Report defects by severity; no edits.
"""))
A(item("RevCounterC1", "reviewer", f"""
Line-level review of {C1}: harness fidelity — does the raw BASH_FUNC_env%% delivery match what a
real `export -f env` produces (compare against `bash -c 'env() {{ :; }}; export -f env; printenv |
grep BASH_FUNC')`)? Is the per-scenario environment otherwise clean (base_env scrubbing: which
families, could the caller's own env leak an expectation-moving variable)? Is the drift run's env
the right control? Is echo_lines anchored (^GATE_GREP: ) and drift_line the LAST GATE_DRIFT line?
List every fidelity defect found, with line numbers; no edits.
"""))
A(item("RevCounterC2", "reviewer", f"""
Line-level review of {C2} and {VRFY}: the self-rewrite shim (does it faithfully replay F1? does
the mv race anything?), the doctor mutants (do they preserve JSON parseability; does verify catch
each on the right binding?), the foreign-gate fixture (byte difference, permissions), the
legacy-receipt cell (does it prove BOTH refusal and positive verification?), and verify-receipts'
check ordering (could an early cheap check mask a later real one?). List defects with line
numbers; no edits.
"""))
A(item("RevSeparability", "reviewer", f"""
Verify the two claims are causally separable as frozen in {CLAIMS} §Separability, by measurement
not assertion: (1) run the c1 counter against a COPY of the landed gate with ONLY the capture
line reverted to bare `env` (single hunk) — expect c1 to drop below 7 while its receipt binding
still works; (2) run the c2 counter against the BASE gate with the default r38 c1 counter —
expect 7/7 (c2 is gate-agnostic); (3) identify the minimal counter-side hunk that would break c2
while leaving c1's scenarios untouched. Report the observed numbers; no edits.
"""))
A(item("RevErrataCtx", "reviewer", f"""
Review the round-37 Errata 5/6 handling in this round: read {LANE}/corpus/evidence/round37/claims.md
§Errata 5-6 and {CLAIMS}: confirm C1 builds on the BASH_FUNC export channel WITHOUT re-litigating
the frozen narrowings (its seven cells are the capture's env invocation, not the grep pin's
sha256sum child or the BASH_ENV scrub), and that claims.md names what r38 still owes on those
channels (loader-env scrub, bash-function witness). Flag any sentence in the r38 claims that
re-opens a frozen erratum or claims its ground; no edits.
"""))

# ---- critics (5) ----
A(item("CritC1Kill", "critic", f"""
Try to falsify C1 beyond its seven cells, on the LANDED gate {GATE}. Avenues worth pressing (find
your own too): an exported `bash` function shadowing the capture's bare `bash` call (is the limit
honestly named? does the moved capture actually happen?); LD_PRELOAD interposing on /usr/bin/env
(does it strip the -u flags? is the claims.md loader-env limit now honest?); a function exported
through BASH_ENV instead of the environment; RESEARCH_GATE_ENV pointing at a real GNU env that is
a wrapper (version self-report limit); hostile TMPDIR. Any kill MUST be reported with the exact
command and output; a kill that the claims.md limits already name is a limit-confirmation, not a
kill — say which.
"""))
A(item("CritC2Kill", "critic", f"""
Try to falsify C2 beyond its seven cells. Avenues: a receipt with EXTRA unknown fields (does
receipt_digest canonicalization cover them?); a receipt whose gate_sha256_pre differs from _post
but the change happened between scenarios (should already refuse — verify); a counter that writes
the receipt and then edits its own file (is the counter_sha256 still truthful? is that in scope?);
symlink the receipt path between write and verify; a legacy receipt doctored to ADD the binding
fields with garbage (does verify fail closed?); feeding verify a c1 receipt where it expects a c2
one (--counter mismatch). Report exact commands/outputs; classify each as kill, named limit, or
out-of-scope with the reason; no edits.
"""))
A(item("CritDoNothing", "critic", f"""
Attack the counting commands as predicates. For each claim: name the cheapest tree that skips the
claimed work and could still print 7/7. Try concretely, from {LANE}: (C1) a counter flag or env
that skips scenarios? (there is none — verify by reading {C1}); a gate that special-cases the
counter's exact drift comparisons? (would that pass the suppress cell too?); (C2) a verify that
accepts missing fields? (feed it a legacy receipt — expect exit 1). Confirm the committed
before-receipts (c1-base 2/7, c2-base 0/7) re-derive from the freeze commit {FREEZE} bytes.
Report each attempt's exact result; no edits.
"""))
A(item("CritNoexec", "critic", f"""
Press the named noexec limit. On the LANDED gate: `SHELLOPTS=noexec bash {GATE} --pin /tmp/ne.txt`
(exit code? baseline file? stdout/stderr?) — confirm the claims.md limit sentence matches
observed bytes exactly. Then attempt ANY conceivable in-body mitigation (early SHELLOPTS check?
BASH_ENV preflight? a `bash -c` re-exec guard?) and demonstrate why each fails under `-n` (the
body does not execute). Conclude whether the claim's carried-debt wording is the honest maximum,
or name a real fix. Report verbatim; no edits.
"""))
A(item("CritTextOverreach", "critic", f"""
Adversarial reading of {CLAIMS} line by line, both claims: mark every sentence as MEASURED
(a counter cell or committed receipt covers it), LIMIT (named), INFERENCE (believed but
unmeasured), or OVERREACH (asserts more than the cells show). Pay special attention to: 'cannot
interpose', 'never by the gate under test', 'fails closed', 'a do-nothing lane commit cannot
reach 7/7', and every 'carried debt' sentence. Cross-check each MEASURED mark against the actual
scenario expectations in {EXPECT}. Report the full marking; no edits.
"""))

# ---- mutation-testers (3) ----
A(item("MutGateC1", "mutation-tester", f"""
Mutation-test the gate's C1 hunks (copy {GATE} to /tmp, mutate the copy, run the c1 counter
against it, fresh seeds): M1 revert the capture line to bare `env`; M2 remove the GNU-coreutils
case from env_pin_verify (accept any --version); M3 remove the override absolute-path refusal;
M4 point the capture at a hardcoded /usr/bin/env while keeping the rest (does the counter
notice? should it?). For each mutant report c1's score AND c2's score against it (run the c2
counter with the default r38 c1 counter against the mutant gate): the separability expectation is
c1 moves, c2 holds. Exact commands and outputs; no lane edits.
"""))
A(item("MutCounterC2", "mutation-tester", f"""
Mutation-test the counter-side C2 bindings (copy {C1} to /tmp, mutate, point {C2} at the mutant
via --counter): M1 hash the gate only AFTER the run (the F1 hole, restored); M2 drop the
pre!=post refusal; M3 drop counter_sha256 from the receipt; M4 drop receipt_sha256. For each:
the c2 counter must score below 7 (name which scenario catches it) while the c1 counter's OWN
scenarios still pass 7/7 against the landed gate (its predicate is C1, not C2). Exact outputs;
no lane edits.
"""))
A(item("MutVerify", "mutation-tester", f"""
Mutation-test {VRFY} (copy to /tmp, mutate, invoke directly): M1 accept a receipt missing
gate_sha256_pre; M2 skip the receipt_sha256 self-digest check; M3 compare gate_sha256_pre only
(ignore _post); M4 compare hashes case-insensitively. For each mutant, feed it (a) the honest
c1-after receipt, (b) the corresponding doctored receipt from the c2 counter's tamper scenario
(you can rebuild the doctoring by editing a copy of {LANE}/corpus/evidence/round38/receipts/c1-after-s38001.json),
and confirm the mutant accepts what the landed verifier refuses. Exact outputs; no lane edits.
"""))

# ---- sentinels (2) ----
A(item("SentScope", "sentinel", f"""
Scope watch. First, read-only: `git -C {LANE} status --porcelain` before any other seat could
finish (record it). Your own write surface is ONLY {OUT}/SentScope.md — everything else in the
lane repo, its .git and jj state, the fleet repo, and sibling lanes must be byte-identical when
you finish: re-run `git -C {LANE} status --porcelain` at the end and diff the two states (every
wave report landing under {OUT}/ is EXPECTED; anything else is a violation — name it). Also list
every file currently under {OUT}/ and flag any seat report written outside it.
"""))
A(item("SentNoNet", "sentinel", f"""
Network watch. Confirm the round-38 counters never touch the network: with strace (install via
uv/npx if absent — record tool/version/channel) or an equivalent tracer, run one full c1 counter
pass against the landed gate and one verify-receipts invocation; report every socket/connect
line (expect none) and the exact trace command. Without a tracer, sample `ss -tnp` during the
runs. Also confirm the counters' writes stay inside their temp dir and the receipt path
(strace -f -e trace=openat,connect). Exact evidence; no edits anywhere.
"""))

# ---- revengers (2) ----
A(item("RevF1Disposition", "revenger", f"""
Reverse-engineer the round-37 residual findings and disposition each against the landed r38
bytes. Read {LANE}/.ufo/waves/round-37/residual/RevC1FreshSeed.md (F1, F2, F4, F5), CritC1Kill.md,
CritC2Kill.md, RevReceiptAudit.md and RevSeparability.md. For EACH finding: CLOSED (demonstrate
the exact r38 behavior that closes it, with a command), NAMED-LIMIT (the claims.md/QUALITY row
that bounds it — quote it), or OPEN (still reachable on the landed bytes — demonstrate). F1 gets
a live replay (your own shim), not a prose claim. Exact evidence for every disposition; no edits.
"""))
A(item("RevRoutedQueue", "revenger", f"""
Reverse-engineer the round-37 closure's routed-defects list
({LANE}/corpus/lessons/round-37-verifier-spotcheck.md, section 'Routed defects / notes for the
operator and round 38', 6 items) and the SCORECARD planned-38 candidate list: for every item,
state r38's disposition (landed by C1/C2/frontier this round with evidence pointer, explicitly
deferred with the reason, or not addressed), and flag any item whose disposition the round report
will overstate. Also check the carried C1 debt (spans >= 32768) is untouched and still named.
No edits.
"""))

# ---- connector (1) ----
A(item("ConnOverlap", "connector", f"""
Sibling-overlap scan: read the other lanes' round-37/round-38 reports and SCORECARD planned
sections under /home/vgpnk/Projects/shokunin/*-shokunin/ and /home/vgpnk/Projects/shokunin/.ufo/reports/
(kake, kumitate, kaidoku, kotodama, mori, tsukuroi at minimum) for claims overlapping chousa's
r38 surfaces (pin/provenance machinery, receipt binding, BASH_FUNC/env-hermetic captures,
counter-strength). For each overlap: name the lane, the round, the contested scope, and whether
chousa's claims text absorbs another lane's ground (adjacency violation) or stays in-province.
Fleet repos are read-only for you; no edits anywhere.
"""))

# ---- simplifier (1) ----
A(item("SimpCounters", "simplifier", f"""
YAGNI review of the four new artifacts ({C1}, {C2}, {VRFY}, {EXPECT}) against the lane's planned-list
dead-fields class (round-36's argv-witness D1-D3 pattern): flag every field/option/code path that
no scenario, receipt, or verify check consumes (candidates to check: c2's subject_counter receipt
field — does anything read it? the --tmp option plumbing, the receipt 'gate' path vs gate_sha,
unused imports). For each flag: name it, show it is dead by grep/execution, and say whether
deleting it shrinks the claim surface (do NOT edit the lane — the L1 decides). No edits anywhere.
"""))

SPEC = {
    "wave": "chousa-r38-w1",
    "milestone": "round-38 wave 1 (v1 build+falsify): re-derive and attack the two frozen claims, build attack fixtures, draft frontier material",
    "reportDir": ".ufo/waves/round-38/w1",
    "axes": ["operability", "calibration"],
    "context": CONTEXT,
    "items": I,
}

out = os.path.join(LANE, ".ufo/waves/round-38/w1-spec.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(SPEC, fh, indent=1)
print("wrote %s with %d items" % (out, len(I)))
