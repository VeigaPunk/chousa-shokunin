#!/usr/bin/env python3
"""Generate the round-38 wave-2 spec (v1 policy, band 32-64; 32 seats)."""
import json, os

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
GOD = open(os.path.expanduser("~/.agents/skills/godspeed/directive.md"), encoding="utf-8").read().rstrip("\n")
GATE = LANE + "/tools/research-gate.sh"
BASE37 = LANE + "/.ufo/waves/round-37/controls/base-gate-r37.sh"
BASE38 = LANE + "/.ufo/waves/round-38/controls/base-gate-r38.sh"
C1 = LANE + "/corpus/evidence/round38/c1-count.py"
C2 = LANE + "/corpus/evidence/round38/c2-count.py"
VRFY = LANE + "/corpus/evidence/round38/verify-receipts.py"
CLAIMS = LANE + "/corpus/evidence/round38/claims.md"
EXPECT = LANE + "/corpus/evidence/round38/expectations.jsonl"
R37C1 = LANE + "/corpus/evidence/round37/c1-count.py"
INTEG = "8e93bc916527b3c21f0f702967fa65c3b4c31699"
OUT = LANE + "/.ufo/waves/round-38/w2"

CONTEXT = f"""# Goal
chousa lane (deep-research method), round 38, wave 2 of a v1 two-wave shape — falsify what wave 1
produced and the L1's wave-1 integration. Lane repo {LANE} (jj-colocated; the branch tip was
{INTEG} at dispatch — the wave-1 integration commit; read it with `git -C {LANE} rev-parse master`,
never `@{{u}}`). Fleet root /home/vgpnk/Projects/shokunin is READ-ONLY for every seat.

# What wave 1 found and the integration changed (all in {CLAIMS} §Errata 1-7; read it first)
The frozen C2 verifier certified self-consistency only (legacy laundering, identity reroute,
doctored observations and vacuous receipts verified `ok`); three c2 cells over-asserted the subject
counter's exit code (C2 was gate-coupled, 4/7 on the base gate); the harness left BASH_ENV live (an
ambient startup file forged refusals / unset functions); the tamper doctors never re-sealed so the
named binding checks were unexercised. The integration (commit {INTEG}) closed these: verify-receipts
now binds the counter family + frozen predicate, requires the exact frozen scenario census with each
row's expect tied to the frozen table, re-derives every ok, and keeps the file bindings + arithmetic;
the counters scrub BASH_ENV/ENV/SHELLOPTS/BASHOPTS, pin /usr/bin/bash, assert the anchored refusal
line, hard-check the frozen 7 total, remove a stale --receipt on refusal, and the counter/expect
doctors re-seal with the exact refusal label as the asserted observable. C1 was NARROWED (Erratum 6):
P1 measures function-export interposition on the capture's env invocation + override shape; the
PATH half, the sibling-name witnesses (a `date` function still embeds GATE_GREP + phantom drift),
and the bash-name vectors (PATH shim / suppressing function) are named, demonstrated limits.
P1: `python3 {C1} --gate {GATE} --seed N --receipt F` -> ENV_PIN_CAPTURE_MATCH=7/7 (base gates
{BASE37} and {BASE38} both 2/7; r37 counter is C2's control, not C1's).
P2: `python3 {C2} --gate {GATE} --seed N --receipt F` -> RECEIPT_BINDING_MATCH=7/7 (r37-counter
control 0/7; the r38 counters on the unfixed gate also 7/7 — separability, not a do-nothing path).
Nine committed receipts: {LANE}/corpus/evidence/round38/receipts/ (all VERIFY: ok under the
strengthened verifier; the two base receipts bind their own control gates and correctly REFUSE the
landed gate). Gate selftest on the final bytes: PASS (272 cases).

# Seat rules (bind every seat)
- You are a LEAF: no spawns, no background jobs, no `task` calls, no swarm of your own.
- Never write outside your own report file under {OUT}/ and temp dirs you create under /tmp.
  Never mutate the lane repo, its jj state or its git index, the fleet repo, or a sibling lane.
  Never run `git add/commit/push/stash/checkout/switch/reset/pull` or any mutating `jj` command.
  Read-only git is fine (`log`, `show`, `diff`, `rev-parse`, `status`).
- Run counters with C1_TMP/C2_TMP pointing at a temp dir that EXISTS. Use fresh seeds (>= 38401 for
  wave-2 work) and name your seed in your report. Receipts you generate go under /tmp; quote the
  fields your findings need — do NOT copy full receipts into reports.
- Evidence is a re-executed command plus its output; a naked assertion is not evidence.
- Tooling authorization (operator 2026-10-19): you may install or upgrade tools that help the task —
  read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate, record
  tool/version/channel/reason in your report). pacman guard (orchestrator ruling 2026-10-20): ALL
  pacman transactions are PAUSED host-wide; install via `uv tool`/`npx`/an official binary into
  ~/.local/bin, or file an L0 question. Never `-Sy`, `-Syu`, `-U`, `-R`, downgrade or restart a
  host service.
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

A(item("W2ExecC1Final", "executor", f"""
Re-derive P1 on the FINAL bytes ({INTEG}) with fresh seeds 38411 and 38431: c1 counter against the
landed gate (expect 7/7, predicate_holds=true) and against BOTH base gates {BASE37} and {BASE38}
(expect 2/7 each). Verify every after-receipt with {VRFY}. Report per-scenario lines for one seed and
the receipt binding values for all.
"""))
A(item("W2ExecC2Final", "executor", f"""
Re-derive P2 on the final bytes with fresh seeds 38421 and 38441: c2 counter against the landed gate
(expect 7/7) and the r37-counter control ({R37C1}, expect 0/7). Verify both after-receipts with
{VRFY}. Also re-run c2 against the BASE gate {BASE37} with the default r38 c1 counter — post-Erratum-4
this must now be 7/7 (separability); report it.
"""))
A(item("W2ExecNoHarmFinal", "executor", f"""
Run the pinned no-harm battery on the final bytes from {LANE} and report verbatim outputs:
`bash {GATE} --selftest | tail -3` (expect PASS 272); verify-claims claims-r2.jsonl --root .. (17/17
CLEAN); verify-chain chain-r3.md --root .. (17/22 CLEAN); verify-all full-r6-broken.md with its
claims (DRIFT, drift-sections=2); the SCORECARD archives one-liner (3/3). Absolute fixture paths under
{LANE}/corpus/fixtures/.
"""))
A(item("W2ExecCtlFinal", "executor", f"""
Controls on final bytes, fresh seeds >= 38451: (1) r37 c1 counter ({R37C1}) against the landed gate —
its own predicate must still score 7/7 (C1's gate fix is C2's control surface, not C1's); (2) r38 c1
against base gate {BASE38} (9fcac047, the true pre-round-38 gate) — 2/7; (3) verify the c1-base2
receipt ({LANE}/corpus/evidence/round38/receipts/c1-base2-s38003.json) against {BASE38} — VERIFY: ok —
and against the landed gate — must REFUSE (gate-sha256-mismatch). Report each verbatim.
"""))

A(item("W2RevErrata", "reviewer", f"""
Adversarial audit of {CLAIMS} §Errata 1-7 against the wave-1 seat reports under
{LANE}/.ufo/waves/round-38/w1/: for EACH erratum, verify (a) every wave-1 finding it claims to close
is actually closed by the described mechanism (re-execute the key check), (b) nothing it claims as
CLOSED is still reachable, (c) every wave-1 finding with severity HIGH or above has an erratum (none
dropped). Report per-erratum verdicts with evidence; no edits.
"""))
A(item("W2RevVerifyFinal", "reviewer", f"""
Line-level review of the strengthened {VRFY} plus new bypass attempts (each must refuse; report the
exact label): duplicate scenario ids; a scenario id as a non-string; receipt expect dict with an
injected `_contains` key vs the frozen table; scenarios as a dict not a list; matched as a string
"7"; a 7-row census with one ok flag flipped AND re-sealed; observed containing extra keys (must
still verify — extra observations are not refusals); a receipt for family c2 fed with
--counter c1-count.py. Also confirm the honest receipts in {LANE}/corpus/evidence/round38/receipts/
still VERIFY: ok. No edits.
"""))
A(item("W2RevC1Final", "reviewer", f"""
Review the strengthened {C1}: the base_env scrub list (BASH_ENV/ENV/SHELLOPTS/BASHOPTS + families) —
sufficient or overbroad (does it break any scenario?); the /usr/bin/bash pinning with fallback; the
anchored refusal line; the stale-receipt unlink; the hard-7 holds check; subprocess timeouts. Try to
construct a scenario env leak that still moves a verdict (e.g. a variable family not scrubbed that
the gate consumes: HOME? TMPDIR? LANG/LC_*?). Report defects with line numbers; no edits.
"""))
A(item("W2RevC2Final", "reviewer", f"""
Review the strengthened {C2}: the re_digest doctors (do counter/expect re-sealed doctors actually
reach their NAMED checks now — run one and quote the label); the verify_fail capture and the
_contains comparison; the stale-receipt unlink; the hard-7 check; base_env/timeout parity with c1.
Report defects with line numbers; no edits.
"""))
A(item("W2RevReceipts", "reviewer", f"""
Byte-level audit of all nine receipts in {LANE}/corpus/evidence/round38/receipts/: every binding
field present and 64-hex; scenario census exactly the frozen ids of its family (per {EXPECT});
matched/total/predicate_holds consistent with the per-row ok values; gate_sha256_pre==post and equal
to the sha256 of the gate each receipt claims (landed for afters, control gates for the two bases —
compute all four gate hashes yourself); receipt_sha256 recomputes under the canonical serialization.
Report any defect per receipt; no edits.
"""))
A(item("W2RevClaimsFinal", "reviewer", f"""
Full read of {CLAIMS} INCLUDING §Errata 1-7 as they now stand: mark every erratum sentence
MEASURED/LIMIT/INFERENCE/OVERREACH with the same rigor as the body (does Erratum 2's "closed" claim
match the strengthened verifier's actual checks? does Erratum 6's narrowing claim exactly the cells?
does any erratum introduce a new universal clause?). Cross-check against {EXPECT} and the nine
receipts. Report the marking; no edits.
"""))
A(item("W2RevSeparabilityFinal", "reviewer", f"""
Re-run the three separability measurements on the final bytes: (1) gate-side single hunk (landed gate
copy, capture line "$ENV_BIN" -> bare env): c1 must drop below 7 (its receipt binding must still
work); (2) counter-side single hunk ({C2} copy, the pre!=post check -> False): c2 must drop to 6/7
while c1 stays 7/7; (3) c2 against base gate {BASE37} with the default r38 c1 counter: 7/7
post-Erratum-4. Report all numbers; no edits.
"""))

A(item("W2CritLaundering", "critic", f"""
Replay ALL of wave-1 CritC2Kill's doctoring fixtures against the strengthened {VRFY} on the final
bytes: legacy-rebound (r37 receipt dressed with public hashes + recomputed digest), identity reroute
(c1 receipt with counter_sha256 = c2's hash + re-seal), doctored observation re-sealed, vacuous
empty receipt (scenarios=[], matched=total=0, holds=true), zero-scenarios with predicate string,
extra unknown field unsealed AND re-sealed, c1-as-c2 unmodified. EVERY one must refuse — report the
exact VERIFY-FAIL label for each (which check caught it). Any acceptance is a kill; no edits.
"""))
A(item("W2CritVacuous", "critic", f"""
Census attacks on the strengthened verifier ({VRFY}): duplicate one frozen id (8 rows, one id twice,
one id missing); reorder rows; permute a receipt expect dict's KEYS (dict equality should hold —
confirm it does, and that changing a VALUE refuses with expect-tie-mismatch); flip one ok flag with
re-seal (ok-rederivation-mismatch expected); drop one observed key in one row; change the receipt's
predicate string to the other family's predicate. Report the exact label per attack; no edits.
"""))
A(item("W2CritEnvFinal", "critic", f"""
Ambient-environment attacks on the strengthened harness, from {LANE}: (1) REVCounterC1's exact
r37-forge (a BASH_ENV prelude that unsets the attack function and forges ENV_PROVENANCE tokens) run
against the r37 GATE with the r38 c1 counter — post-Erratum-5 this must STILL score 2/7 (the startup
channels are scrubbed from the scenario env); (2) the honest attack still registers: BASH_FUNC_env%%
echo re-add against the landed gate must still FAIL its cell (2/7 base shape on the base gates);
(3) a PATH `bash` shim must still move verdicts (named limit — confirm claims.md Erratum 5/6 wording
covers exactly what you observe); (4) SHELLOPTS=noexec still exits 0 with no baseline (named).
Report each verbatim; no edits.
"""))
A(item("W2CritKillC1Final", "critic", f"""
Fresh C1 kill attempts on the landed gate beyond its cells: exported `date`, `grep`, `sha256sum`
shell functions through BASH_FUNC (sibling-name witnesses — Erratum 6 says the channel is open:
demonstrate the moved baseline and judge whether the erratum wording matches reality); LD_PRELOAD
interposing on /usr/bin/env (named limit — confirm it still strips -u flags if you can build the
interposer quickly, or reason from ldd); RESEARCH_GATE_ENV pointing at a logging wrapper around the
real env (honoured — a named limit; confirm the capture uses it and the claims say exactly that).
Classify each: kill / named-limit / out-of-scope with reasons; no edits.
"""))
A(item("W2CritDoNothingFinal", "critic", f"""
Final do-nothing audit on {INTEG} bytes: (1) the r37 pipeline ({R37C1} + r37 verifier semantics)
against the landed gate on a fresh seed — must be 0/7 under c2; (2) both base gates 2/7 under c1;
(3) an expectations table edited to SIX c1 scenarios must not let any counter print a passing
predicate (hard-7 check — test with a /tmp copy of the counter pointed at a /tmp six-row table, or
by reading the code and demonstrating with the smallest run); (4) verify-receipts given a receipt
whose scenarios are the frozen six-plus-one-bogus census (re-sealed) must refuse
scenario-census-mismatch. Report each verbatim; no edits.
"""))
A(item("W2CritTextFinal", "critic", f"""
Final adversarial marking of {CLAIMS} as it now stands (body + Errata 1-7): every sentence
MEASURED/LIMIT/INFERENCE/OVERREACH, with the post-integration bytes. Pay special attention to
Erratum 2's narrowed reading ("integrity and self-consistency, NOT authorship") — is that boundary
itself honest given a fabricator can re-run scenarios and produce an indistinguishable receipt?
Name the residual claim the round can still honestly make. Report the full marking; no edits.
"""))

A(item("W2MutVerifyFinal", "mutation-tester", f"""
Mutation-test the strengthened {VRFY} (copy to /tmp, mutate, feed the strengthened c2's own
fixtures): M1 accept missing gate_sha256_pre; M2 skip self-digest; M3 compare pre only; M4
case-insensitive hashes; M5 skip the census check; M6 skip ok re-derivation. For each: the
strengthened c2 counter (default counter) on a fresh seed must score BELOW 7 — name which scenario
catches it (the tamper cells with RE-SEALED doctors are the catchers now). Also run MutVerify's
original probes (d-field-only without re-digest, d-upper) against each mutant. Exact outputs; no
lane edits.
"""))
A(item("W2MutCounterFinal", "mutation-tester", f"""
Re-run MutCounterC2's four counter mutants against the FINAL {C1} (copy to /tmp, mutate, point the
final {C2} at it): M1 post-run gate hash only; M2 pre!=post refusal dropped; M3 no counter_sha256;
M4 no receipt_sha256. Each must drop c2 below 7 (name the catcher) while c1's own scenarios still
score 7/7 against the landed gate on a fresh seed. Exact outputs; no lane edits.
"""))
A(item("W2MutGateFinal", "mutation-tester", f"""
Re-run MutGateC1's four gate mutants against the final {C1}: M1 bare-env capture (expect c1 < 7);
M2 no GNU-coreutils check (expect < 7); M3 no absolute-path override refusal — wave-1 saw this
survive 7/7: confirm the final cells STILL cannot see it and that Erratum 6 names exactly that;
M4 hardcoded /usr/bin/env capture (same question). For M3/M4 quote the claims.md sentence that
dispositions them. Also record c2's score on each mutant (post-Erratum-4, which cells move?).
Exact outputs; no lane edits.
"""))

A(item("W2ScribeKnowledgeC1", "scribe", f"""
Draft the FINAL `corpus/knowledge/env-pin-capture-r38.md` inside your report, superseding the w1
draft: incorporate BOTH delivery mechanisms (raw BASH_FUNC_env%% and real `export -f`), the
MutGateC1 M3/M4 unmeasured-half result, the sibling-name witnesses (date/grep/sha256sum functions),
the PATH bash shim, the narrowed Erratum-6 reading, and the pre-registered r39 cells. Provenance
trio first (source: S072 bash.info by path + {CLAIMS}; verified-at 2026-10-24; recheck on-release).
House style: mirror {LANE}/corpus/knowledge/pin-capture-env-r37.md. Quote only what you verified in
wave reports; cite the wave reports by path.
"""))
A(item("W2ScribeKnowledgeC2", "scribe", f"""
Draft the FINAL `corpus/knowledge/receipt-binding-r38.md` inside your report, superseding the w1
draft: the binding model as INTEGRATED (census tie + ok re-derivation + predicate/family binding),
the wave-1 kill candidates it closed (legacy laundering, identity reroute, doctored observations,
vacuous receipts — each with its wave report pointer), the NOT-authorship narrowed reading
(F2 residual, verify side), and the carried debts (verifier_sha256 binding, r39). Provenance trio
first. House style: mirror {LANE}/corpus/knowledge/claim-pin-provenance-r37.md.
"""))
A(item("W2ScribeLesson", "scribe", f"""
Draft `corpus/lessons/round-38.md` inside your report: a `## Mistakes` table mining this round's
real mistakes — at minimum: (1) the frozen verifier certified self-consistency, not provenance
(class: vacuous; evidence: w1/CritC2Kill.md findings 1-3; captured-by: none — no QUALITY row
required receipt rows to be tied semantically to the frozen table; fix: the census tie + ok
re-derivation, shown able to fail by the w1 kills); (2) the c2 cells over-asserted the subject's
exit code (class: scope; evidence: w1/ExecDoNothingCtl.md; captured-by: none; fix: Erratum 4);
(3) the harness left BASH_ENV live (class: survivor; evidence: w1/RevCounterC1.md finding 1;
captured-by: none; fix: Erratum 5 scrub). Each row: class · evidence pointer · captured-by · fix.
Then a `## Gate` section with the S072/S073 entries (the w1/ScribeSources.md drafts, corrected per
its own findings) and the receipt/census notes for the round close. Also draft a QUALITY.md addition
(one row) that would have caught mistake (1). House style: mirror {LANE}/corpus/lessons/round-37.md.
"""))

A(item("W2ScoutResidual", "scout", f"""
Enumerate the lane's POST-integration open attack surface for the round report's carried-debt list:
every witness the rounds now name but no cell covers (PATH env shim, PATH bash shim, exported
sibling-name functions, hostile-drift coverage, override-honored positive witness, relative-override
refusal, LD_PRELOAD on env and on sha256sum, SHELLOPTS=noexec, BASH_FUNC of `bash`, verifier_sha256
binding, receipt path symlink identity) — for each: the demonstrated evidence pointer (wave report),
the named-limit sentence in {CLAIMS} that bounds it, and the cheapest r39 cell that would measure it.
No edits anywhere.
"""))
A(item("W2ScoutFrontier", "scout", f"""
Run the sources census ({LANE}: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
--root /home/vgpnk/Projects/shokunin chousa`; exit code + rows + tier/status histograms) and audit
the drafted S072/S073 rows in w1/ScribeSources.md for contract-v1 conformance (11 columns; no `|`
inside cells; ids S072/S073 free in {LANE}/corpus/SOURCES.md; the bash.info anchor — verify the
sentence span yourself with zcat/awk and give the exact lines; the sha256sum label defect). Report
what the L1 must fix before the rows land. No edits anywhere.
"""))

A(item("W2SentScopeFinal", "sentinel", f"""
Scope watch across wave 2: record `git -C {LANE} status --porcelain` now and at the end; diff the
two states (every report under {OUT}/ is EXPECTED; anything else is a violation — name it). List
every file under {OUT}/ at the end and flag reports written outside it. No edits anywhere else.
"""))
A(item("W2SentNetFinal", "sentinel", f"""
Network watch on the final counters: strace (already installed — strace 7.2) one full c1 run, one
full c2 run and one verify-receipts invocation against the landed gate; report every
socket/connect line (expect none) and every openat outside the temp dirs, the lane repo and system
libraries (with C1_TMP/C2_TMP set to existing dirs and TMPDIR pointed inside them). Exact evidence;
no edits anywhere.
"""))

A(item("W2RevRoutedFinal", "revenger", f"""
Final disposition table: the r37 closure's routed-defects list (6 items) and the SCORECARD
planned-38 candidate list, against what ACTUALLY landed at {INTEG} — each item: LANDED (pointer),
LANDED-NARROWED (the erratum), DEFERRED-r39 (the cell), or NOT-ADDRESSED (say why). Include the
RevF1Disposition OPEN item (r37 knowledge docs' "7/7 on every committed receipt" — check whether the
round-38 integration's correction of those two docs resolves it, and re-read both files to confirm
the correction is accurate). No edits.
"""))
A(item("W2SimpFinal", "simplifier", f"""
Dead-fields re-audit of the INTEGRATED artifacts ({C1}, {C2}, {VRFY}, {EXPECT}) on {INTEG} bytes:
did the integration add new dead weight (audit clean_verify_out, subject_counter, the *_contains
annotation keys' handling, the BASH fallback branch, the stale-unlink path)? For each flag: prove
dead by grep/execution, say whether deletion shrinks the claim surface. Deletions remain L1's r39
call — do not edit the lane.
"""))
A(item("W2ConnFinal", "connector", f"""
Sibling-overlap re-scan for the NARROWED claims (post-Erratum): the C1 surface is now the capture's
env invocation function-export interposition; C2 is receipt integrity/self-consistency against
committed bytes. Re-check the lanes from w1/ConnOverlap.md (kumitate, kake, mori, kotodama,
kaidoku, kotoba, tsukuroi) for any NEW overlap introduced by the narrowing (especially tsukuroi's
loader-env channel and kumitate's pin receipts) and confirm chousa still absorbs nothing.
Fleet read-only; no edits anywhere.
"""))
A(item("W2LabBashFn", "scout", f"""
One falsifiable probe, executed: pin down EXACTLY which bash-name vectors reach the capture on the
landed gate — (a) an exported `bash` FUNCTION (BASH_FUNC_bash%%) that logs its argv to a file: does
the capture's grandchild `bash` invocation hit the function or the binary? (b) a PATH `bash` shim
that does the same: which invocations does it see? Report the observed argv sets for both, map them
to the gate line numbers (the capture at ~4003 vs the verify_all_section shell-outs at ~3642), and
state precisely which vector the claims.md Erratum-6 limit sentence describes vs what you observed.
No edits.
"""))
A(item("W2LabEnvScrub", "scout", f"""
One falsifiable probe, executed: repeat RevCounterC1's exact ambient-BASH_ENV forge (its report has
the construction: a startup file that unsets the attack function and prints forged ENV_PROVENANCE
lines) against the STRENGTHENED c1 counter on the r37 GATE ({BASE37}) — pre-Erratum-5 this moved
the r37 gate to 7/7; it must now score 2/7 (BASH_ENV is scrubbed from the scenario env). Then the
control: the same forge via a channel that IS still live (if you find one, demonstrate and name it;
if none, say what you swept). Report both verbatim; no edits.
"""))

SPEC = {
    "wave": "chousa-r38-w2",
    "milestone": "round-38 wave 2 (v1 falsify): attack the strengthened pipeline and the integration on final bytes",
    "reportDir": ".ufo/waves/round-38/w2",
    "axes": ["operability", "calibration"],
    "context": CONTEXT,
    "items": I,
}

out = os.path.join(LANE, ".ufo/waves/round-38/w2-spec.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(SPEC, fh, indent=1)
print("wrote %s with %d items" % (out, len(I)))
