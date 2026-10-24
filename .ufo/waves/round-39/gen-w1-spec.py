#!/usr/bin/env python3
"""Generate the round-39 wave-1 spec (v1, 32 seats, policy band 32-64)."""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
FLEET = "/home/vgpnk/Projects/shokunin"

GODSPEED_DIRECTIVE = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.
"""

CONTEXT = """# Goal
chousa lane (deep-research method), round 39, wave 1 of a v1 two-wave shape — re-derive and
first-falsify the round's two frozen claims, probe the discrimination controls, and draft the
frontier material. Lane repo /home/vgpnk/Projects/shokunin/chousa-shokunin (jj-colocated; read
the tip with `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master`, never
`@{u}`). Fleet root /home/vgpnk/Projects/shokunin is READ-ONLY for every seat.

# The two claims (frozen: /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/claims.md;
expectations frozen: /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/expectations.jsonl)
C1 (operability, lowest axis 3/10): the canonical pin capture's grandchild and the verify-all
section children run through ONE pinned absolute `bash` (RESEARCH_GATE_BASH override, BASH_PROVENANCE
refusal exit 2 before any mode runs); predicate `ENV_PIN_CAPTURE_MATCH=8/8`.
C2 (calibration): round-39 receipts bind verifier_sha256 + subject_counter_sha256, re-derived by
corpus/evidence/round39/verify-receipts.py with named refusals; predicate `RECEIPT_BINDING_MATCH=8/8`.
Controls: pre-round gate .ufo/waves/round-39/controls/base-gate-r39.sh (0447ad14…, C1 scores 7/8 on it);
PATH-env mutant .ufo/waves/round-39/controls/mut-gate-path-env.sh (e1251030…, scores 4/8);
r38 receipts refuse under the r39 verifier. Routed repairs D1-D6 from the round-38 closure are
in scope to re-check.

# Contract for every seat
- Work ONLY inside /home/vgpnk/Projects/shokunin/chousa-shokunin (read-only elsewhere; NEVER
  mutate lane jj state or the lane git index, never write under .ufo/state, never touch the
  fleet repo or sibling lanes).
- Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/chousa-shokunin —
  write it at /home/vgpnk/Projects/shokunin/chousa-shokunin/<that path>. Absolute paths for
  every other read/write.
- Counters need C1_TMP / C2_TMP (or --tmp) to EXIST (mkdtemp inside). No network anywhere:
  all sources open from installed man pages/info files.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help
  the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety
  gate, record tool/version/channel/reason in your report). Pacman guard (orchestrator ruling
  2026-10-20): ALL pacman transactions are PAUSED host-wide — install via `uv tool`/`npx`/an
  official binary in ~/.local/bin, or file an L0 question; never run pacman -S/-Sy/-Syu/-U/-R.
- Measurement environment: committed runs are made under a clean caller environment; the
  counters scrub BASH_FUNC_*/CHOUSA_*/RESEARCH_GATE_*/PYTHON*, BASH_ENV/ENV/SHELLOPTS/BASHOPTS/
  POSIXLY_CORRECT. An ambient hostile channel that moves a verdict is a finding about the
  measurement environment, named per QUALITY 53, never silently scored.
- Do not rerun git/jj validation commands for their own sake; tool results are evidence.
- Report: one markdown file per seat at the Report path your item names, carrying the command,
  its actual output, and the verdict. Claims you assert without a resolvable pointer do not count.
"""


def item(name, role, task):
    return {"name": name, "role": role,
            "prompt": GODSPEED_DIRECTIVE + "\n" + task}


ITEMS = [
    item("ExecC1Rederive", "executor",
         "Re-derive C1's before and after on FRESH seeds (not 39001/39011). Commands (cwd "
         + LANE + "):\n"
         "`mkdir -p /tmp/exec-c1 && C1_TMP=/tmp/exec-c1 python3 corpus/evidence/round39/c1-count.py "
         "--gate .ufo/waves/round-39/controls/base-gate-r39.sh --seed <fresh> --receipt /tmp/exec-c1/base-<seed>.json` "
         "(expect 7/8, predicate_holds=false) and the same against tools/research-gate.sh (expect 8/8, "
         "predicate_holds=true). Verify both receipts with corpus/evidence/round39/verify-receipts.py "
         "against their bound gates. Report: .ufo/waves/round-39/w1/ExecC1Rederive.md"),
    item("ExecC2Rederive", "executor",
         "Re-derive C2 on a FRESH seed (not 39101/39121) against tools/research-gate.sh "
         "(cwd " + LANE + "): `mkdir -p /tmp/exec-c2 && C2_TMP=/tmp/exec-c2 python3 "
         "corpus/evidence/round39/c2-count.py --gate tools/research-gate.sh --seed <fresh> "
         "--receipt /tmp/exec-c2/c2-<seed>.json` (expect 8/8). Verify the receipt with "
         "corpus/evidence/round39/verify-receipts.py --counter corpus/evidence/round39/c2-count.py. "
         "Report: .ufo/waves/round-39/w1/ExecC2Rederive.md"),
    item("ExecMutantReprobe", "executor",
         "Re-probe the two discrimination controls on fresh seeds (cwd " + LANE + "): the PATH-env "
         "mutant .ufo/waves/round-39/controls/mut-gate-path-env.sh (expect 4/8: the three r38 "
         "BASH_FUNC_env%% cells plus path_env_shim_echo fail) and the base gate (expect 7/8). "
         "Confirm the mutant differs from the landed gate in exactly the capture env line "
         "(`diff <(sed -n '4067,4072p' mutant) <(sed -n '4067,4072p' tools/research-gate.sh)`). "
         "Report: .ufo/waves/round-39/w1/ExecMutantReprobe.md"),
    item("ExecNoHarm", "executor",
         "Run the no-harm battery on the landed gate (cwd " + LANE + "): `bash tools/research-gate.sh "
         "--selftest` (expect PASS 275 cases 0 skipped); verify-claims corpus/fixtures/claims-r2.jsonl "
         "--root .. (17/17 CLEAN); verify-chain corpus/fixtures/chain-r3.md (17/22 CLEAN) and "
         "chain-r3-broken.md (1/2 DRIFT); the r1 observable "
         "(`python3 -c 'import subprocess; names=(\"A-shokunin-tradition.md\",\"B-multiagent-knowledge.md\",\"C-rank-taxonomy.md\"); "
         "rows=[subprocess.run([\"bash\",\"tools/research-gate.sh\",\"verify\",\"../research/deep-research-2026-09-28/\"+n,\"--root\",\"..\"],capture_output=True,text=True) for n in names]; "
         "print(\"VERDICT_BEARING_EXPORTS=%d/3\" % sum(r.returncode==1 and sum(s.startswith(\"RESEARCH_GATE: DRIFT (\") for s in r.stdout.splitlines())==1 for r in rows))'` → 3/3); "
         "verify-all corpus/fixtures/integrity-r7.md --claims corpus/fixtures/integrity-r7.claims.jsonl --root .. (composed CLEAN). "
         "Report: .ufo/waves/round-39/w1/ExecNoHarm.md"),
    item("ExecDoNothingCtl", "executor",
         "Prove the do-nothing controls cannot reach the predicates (cwd " + LANE + "): (a) verify "
         "the committed r38 receipt corpus/evidence/round38/receipts/c1-after-s38001.json under the "
         "r39 verifier with --counter corpus/evidence/round38/c1-count.py --expectations "
         "corpus/evidence/round38/expectations.jsonl (expect VERIFY-FAIL predicate-mismatch); "
         "(b) run the r39 c1 counter against the base gate and confirm 7/8 with the eighth family "
         "observed values (echo_lines 1 / suppress pin_rc 2 / override pin_rc 0) matching "
         "corpus/evidence/round39/receipts/c1-base-s39001.json; (c) state why a lane commit without "
         "the bash pin cannot print 8/8. Report: .ufo/waves/round-39/w1/ExecDoNothingCtl.md"),
    item("ExecReceiptAudit", "executor",
         "Audit all six committed receipts under corpus/evidence/round39/receipts/: re-derive "
         "gate/counter/expect/verifier/subject bindings with corpus/evidence/round39/verify-receipts.py "
         "(c1 receipts: --counter corpus/evidence/round39/c1-count.py against BOTH tools/research-gate.sh "
         "(expect ok for c1-after-*) and the base/mutant controls (expect ok for their own receipts, "
         "gate-sha256-mismatch for the landed gate); c2 receipts: --counter corpus/evidence/round39/c2-count.py). "
         "Also jq each receipt's predicate_holds/matched against its printed count. "
         "Report: .ufo/waves/round-39/w1/ExecReceiptAudit.md"),
    item("RevClaims", "reviewer",
         "Review corpus/evidence/round39/claims.md against QUALITY 54 (claim text must not outrun "
         "its counter cells): read each claim sentence against the c1/c2 expectation tables and the "
         "landed gate bytes; name any general clause with no counter cell behind it, and any limit "
         "that omits a demonstrated vector class (the r37 residual class). Also check the frozen "
         "P1/P2 predicates match the counters' hard-coded 8/8 checks and the receipt labels. "
         "Report: .ufo/waves/round-39/w1/RevClaims.md"),
    item("RevSeparability", "reviewer",
         "Demonstrate separability in BOTH directions (cwd " + LANE + "): (a) C1-only: the base gate "
         "+ r39 counters must score c1 7/8 while the c2 machinery is inert (run c2 against the base "
         "gate and confirm 8/8 — receipt binding is gate-agnostic per r38 Erratum 4); (b) C2-only: "
         "take the landed counters, point them at the base gate, and confirm the receipts still bind "
         "and verify (bindings do not touch the bash-pin cells). Write the demonstration commands and "
         "outputs. Report: .ufo/waves/round-39/w1/RevSeparability.md"),
    item("RevCounters", "reviewer",
         "Review corpus/evidence/round39/{c1-count.py,c2-count.py} line by line: (a) base_env scrub "
         "completeness — which channels can still reach the gate child or the counter's own children "
         "(name each, classify ambient-vs-scenario, per QUALITY 53/54); (b) the hard-8 checks "
         "(matched==8 and total==8 — can an edited-to-7 table print 8/8?); (c) the pre-run "
         "expectations hash and the changed-gate refusal; (d) the stale-receipt unlink before every "
         "refusal path; (e) the nested-c2 guard (CHOUSA_R39_NESTED) — can it be bypassed to recurse? "
         "Report: .ufo/waves/round-39/w1/RevCounters.md"),
    item("RevGate", "reviewer",
         "Review the landed gate diff (cwd " + LANE + "): `git diff 8c7c867 -- tools/research-gate.sh`. "
         "Check: bash_pin_init mirrors env_pin_init (absolute default probe, GNU-reporting verify, "
         "anchored refusal, readonly guard); the capture grandchild call site; the verify_all_section "
         "call site (is it reached from the canonical capture? from ordinary verify-all?); init "
         "ordering (grep/env/bash pins before any mode); selftest cases 273-275 assert what the "
         "comment claims. Name any drift between the SKILL.md gates-table row and the bytes. "
         "Report: .ufo/waves/round-39/w1/RevGate.md"),
    item("RevRoutedDefects", "reviewer",
         "Re-check the round-38 closure's routed defects D1-D6 against committed bytes (cwd " + LANE + "): "
         "D1/D2 — corpus/evidence/round38/claims.md Errata 14/15 exist, are append-only, and name the "
         "correct hashes (0447ad14… supersession; harness changes); D3 — LOG.md/SCORECARD.md/lessons "
         "counts say 13; D4 — SCORECARD r38 attribution note present; D5 — SKILL.md line 95 row has 9 "
         "pipes ending `| chousa |`; D6 — corpus/lessons/round-38.md correction block carries the URLs "
         "and the rejected-candidate wording fix. Report each as landed or not with evidence. "
         "Report: .ufo/waves/round-39/w1/RevRoutedDefects.md"),
    item("RevReceipts", "reviewer",
         "Independently re-verify the receipt arithmetic (cwd " + LANE + "): for c2-after-s39101.json, "
         "recompute receipt_sha256 over the body (json.dumps indent=2 sort_keys + '\\n'), recompute "
         "each scenario's ok from its expect/observed, recount matched, and confirm predicate_holds "
         "consistency — without executing the counters (pure byte/jq/python work, per PROTOCOL Gate "
         "standard). Then cross-check one fresh c2 seed run's printed lines against its receipt. "
         "Report: .ufo/waves/round-39/w1/RevReceipts.md"),
    item("CritC1Text", "critic",
         "Attack the C1 claim TEXT beyond its counter cells (cwd " + LANE + "): the limits name "
         "mktemp/sed/rm as carried debt — demonstrate ONE of them live (a PATH sed or mktemp shim "
         "reaching the capture path; if none fires, say what blocks it and whether the claim text "
         "already covers it); check the 'verify-all section children' clause is actually pinned "
         "(probe a section-level interposition); check BASH_PROVENANCE fires before ANY mode "
         "(run verify/verify-all/selftest with a relative RESEARCH_GATE_BASH). If a demonstration "
         "contradicts the text, name the erratum class. Report: .ufo/waves/round-39/w1/CritC1Text.md"),
    item("CritC2Text", "critic",
         "Attack the C2 claim TEXT: (a) re-point a c2 receipt at a doctored subject WITH a "
         "re-derived digest + re-seal — the claim says this is 'a new honest receipt, not a forgery'; "
         "demonstrate and judge whether the text's narrowed reading survives; (b) bind a receipt to a "
         "/tmp counter copy (the Erratum-10 'committed-tree membership is the caller's discipline' "
         "clause) — does the claim text still hold?; (c) check the 'r38 receipts refuse' before-claim "
         "against EVERY r38 receipt, not just c1-after-s38001. Report: .ufo/waves/round-39/w1/CritC2Text.md"),
    item("CritKillRule", "critic",
         "Attack the frozen kill rules (cwd " + LANE + "): can any run against the landed gate print "
         "below 8/8 WITHOUT the claimed work being absent (e.g. an environment-conditioned refusal — "
         "QUALITY 53 class; a fixture that weakens itself — the kill rule's own clause)? Run the c1 "
         "counter with an ambient hostile BASH_ENV/POSIXLY_CORRECT and classify any move as "
         "environment vs gate. Check the kill-rule sentence 'a run whose receipt gate_sha256 differs "
         "from the landed gate's is not the claim's measurement' holds for every committed receipt. "
         "Report: .ufo/waves/round-39/w1/CritKillRule.md"),
    item("CritFixtureFires", "critic",
         "Apply QUALITY 56 to every attack fixture in the round (cwd " + LANE + "): the PATH bash "
         "shims (echo/suppress), the PATH env shim, the doctored subject, the weakened verifier — "
         "for each, demonstrate it FIRES on the control bytes (red-before) and is resisted on the "
         "landed bytes (the committed receipts already show the landed side; reproduce the control "
         "side independently). A fixture that cannot fire is a vacuous cell — name it. "
         "Report: .ufo/waves/round-39/w1/CritFixtureFires.md"),
    item("CritCensusGate", "critic",
         "Attack the Sources & frontier records: re-run the census; confirm the S071 used-by change "
         "is the only row touched and the lesson Gate records URL/date/quote per contract v1 rule 1; "
         "re-open env.1.gz and verify the quote, anchor and sha; confirm the rejected-candidate rows "
         "carry reasons + flips. Report: .ufo/waves/round-39/w1/CritCensusGate.md"),
    item("ScoutSurfaces", "scout",
         "Map every bare-name invocation reachable from the canonical pin capture in "
         "tools/research-gate.sh (cwd " + LANE + "): start at gate_canonical_capture and follow into "
         "gate_pin_fixture, gate_drift_normalize, verify_all/verify_all_section and one level into "
         "each mode's helpers. Classify each bare name (mktemp, sed, rm, …) as pinned-by-wrapper, "
         "absolute, or bare-and-reachable; produce the table the claims.md 'Limits' clause must "
         "enumerate. Report: .ufo/waves/round-39/w1/ScoutSurfaces.md"),
    item("ScoutSources", "scout",
         "Re-open every source the round's knowledge entries cite (cwd " + LANE + "): S071 env.1.gz "
         "(quote at line 28, sha 4ae797e6…), S072 bash.info (quote at 1461-1463, sha cde1a336…). "
         "Verify the used-by paths in SOURCES.md exist for both rows. Report: .ufo/waves/round-39/w1/ScoutSources.md"),
    item("ScoutSiblings", "scout",
         "Sibling-overlap scan (read-only): which fleet lanes own material this round touches — "
         "tsukuroi's loader-env channel (the LD_PRELOAD debt), kumitate's dispatch/host mapping, "
         "mori's pin patterns. Read the sibling PROVINCE.md files under /home/vgpnk/Projects/shokunin/*-shokunin/ "
         "and confirm chousa's report routes (never absorbs) the overlap. Report: .ufo/waves/round-39/w1/ScoutSiblings.md"),
    item("ScribeKnowledgeC1", "scribe",
         "Read corpus/knowledge/capture-bash-pin-r39.md against the committed bytes (cwd " + LANE + "): "
         "every measured value (7/8, 8/8, 4/8, 275 cases, sha prefixes) must re-derive from the named "
         "receipts and commands; the S071/S072 citations must match the SOURCES.md rows; the Limits "
         "must match claims.md §Limits. Propose exact corrections for any drift (do not apply them). "
         "Report: .ufo/waves/round-39/w1/ScribeKnowledgeC1.md"),
    item("ScribeKnowledgeC2", "scribe",
         "Read corpus/knowledge/receipt-verifier-subject-r39.md against the committed bytes (cwd "
         + LANE + "): verify the measured values, the named refusal labels (run the two doctor shapes "
         "yourself in /tmp if needed), the sha prefixes, and the construction-note honesty (the "
         "discarded first-run receipt is NOT committed). Propose corrections for drift. "
         "Report: .ufo/waves/round-39/w1/ScribeKnowledgeC2.md"),
    item("ScribeLesson", "scribe",
         "Read corpus/lessons/round-39.md: the four ## Mistakes rows must carry class · evidence · "
         "captured-by · fix with mistake-class vocabulary from the fleet taxonomy; each fix must be "
         "shown able to fail (name the receipt/command that shows it); the ## Gate must satisfy "
         "contract v1 rule 1 for the S071 re-open. Check QUALITY 56 cites this lesson. Propose "
         "corrections for drift. Report: .ufo/waves/round-39/w1/ScribeLesson.md"),
    item("MutBashPin", "mutation-tester",
         "Mutation-test the gate fix (cwd " + LANE + "; copy tools/research-gate.sh to /tmp and mutate "
         "the COPY): M1 restore bare `bash` at the capture grandchild; M2 restore bare `bash` at "
         "verify_all_section; M3 delete the relative-override refusal in bash_pin_init; M4 remove the "
         "readonly guard. Run corpus/evidence/round39/c1-count.py against each mutant (C1_TMP in /tmp) "
         "and record which cells catch which mutant (expect: M1 kills the path-bash cells, M2 kills "
         "suppress, M3/M4 are caught by the override cells/selftest respectively — report what "
         "actually happens). Report: .ufo/waves/round-39/w1/MutBashPin.md"),
    item("MutVerifyBindings", "mutation-tester",
         "Mutation-test the verifier (cwd " + LANE + "; copy corpus/evidence/round39/verify-receipts.py "
         "to /tmp and mutate the COPY): V1 drop the verifier_sha256 check; V2 drop the "
         "subject_counter_sha256 check; V3 case-insensitive hash compare; V4 skip the census. Run "
         "corpus/evidence/round39/c2-count.py... actually run verify-receipts directly against the "
         "committed c2 receipt with each mutant: expect V1/V2 re-adjudicate silently (rc 0 — the "
         "r38 Erratum-11 class the binding exists to catch), V3/V4 refuse by their own arithmetic. "
         "Record which checks the c2 counter's own cells would NOT catch (the named remainder). "
         "Report: .ufo/waves/round-39/w1/MutVerifyBindings.md"),
    item("MutCounters", "mutation-tester",
         "Mutation-test the counters (cwd " + LANE + "; copy corpus/evidence/round39/c1-count.py to "
         "/tmp and mutate the COPY): C1 edit expectations to 7 rows (does the hard-8 check fire?); "
         "C2 weaken one expect value (does the receipt show predicate_holds=false? does the verifier "
         "still ok it — and is that correct?); C3 drop the env scrub of BASH_ENV. Run each against "
         "the landed gate with --tmp /tmp. Record the observable each mutant moves. "
         "Report: .ufo/waves/round-39/w1/MutCounters.md"),
    item("SentScope", "sentinel",
         "Scope sweep: after this wave's seats finish (run this item LAST in your batch — check the "
         "mtime order under .ufo/waves/round-39/w1/), confirm every seat report landed under "
         "/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-39/w1/ and NOWHERE else: "
         "`git -C /home/vgpnk/Projects/shokunin status --porcelain` must show no fleet-root writes by "
         "this wave, and `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain` "
         "must show only the lane-authored round-39 paths (no .ufo/state, no fleet files). "
         "Report: .ufo/waves/round-39/w1/SentScope.md"),
    item("SentEnv", "sentinel",
         "Environment sweep: run corpus/evidence/round39/c1-count.py and c2-count.py once each in a "
         "clean env (cwd " + LANE + ", fresh /tmp dirs) and once with an ambient hostile BASH_ENV "
         "startup file (exporting a benign function + unsetting the scrub). Classify any verdict move "
         "per QUALITY 53 (measurement environment, not gate harm) and confirm the counters' own "
         "base_env scrub keeps committed-run semantics stable. Report: .ufo/waves/round-39/w1/SentEnv.md"),
    item("RevErrataCtx", "revenger",
         "Reverse-engineer the r38 errata repairs (cwd " + LANE + "): for claims.md Errata 14-15, "
         "confirm the landed gate sha 0447ad14… really equals git show 8c7c867:tools/research-gate.sh "
         "| sha256sum, and that the base control at .ufo/waves/round-39/controls/base-gate-r39.sh is "
         "byte-identical to it; confirm Erratum 15's harness claims match the committed counter "
         "bytes (PYTHON*/POSIXLY_CORRECT scrubs, -E children, timeouts). Report any overclaim in the "
         "errata text itself. Report: .ufo/waves/round-39/w1/RevErrataCtx.md"),
    item("RevTextOverreach", "revenger",
         "Hunt overreach in every round-39 prose surface (cwd " + LANE + "): SCORECARD r39 section, "
         "LOG entry, knowledge entries, the report draft if present, and claims.md body — apply "
         "QUALITY 54 literally (each general clause must have a counter cell or a named limit). The "
         "'three pinned call sites' phrase in the knowledge entry vs the actual diff: is the third "
         "site real? (the readonly guard is not a call site — check the wording). "
         "Report: .ufo/waves/round-39/w1/RevTextOverreach.md"),
    item("ConnectorSiblings", "connector",
         "Cross-lane pattern scan (read-only): read the round reports of tsukuroi, kumitate and mori "
         "under /home/vgpnk/Projects/shokunin/.ufo/reports/round-3[5-8]/ for material overlapping "
         "this round (bash/env pinning, receipt/witness binding, loader-env debt, host dispatch "
         "mapping). Produce the sibling-overlap table for the round report: what each sibling owns, "
         "what chousa routes rather than absorbs. Report: .ufo/waves/round-39/w1/ConnectorSiblings.md"),
    item("SimpCounters", "simplifier",
         "YAGNI scan of the round-39 additions (cwd " + LANE + "): read corpus/evidence/round39/"
         "{c1-count.py,c2-count.py,verify-receipts.py} and the gate diff; list dead fields, unused "
         "plumbing, duplicated logic and comment debt that can be deleted WITHOUT changing any "
         "observable (run the counter before/after any proposed deletion in /tmp to prove "
         "byte-identical receipts). If nothing is safely deletable, say so with the sweep evidence. "
         "Report: .ufo/waves/round-39/w1/SimpCounters.md"),
]

spec = {
    "wave": "chousa-r39-w1",
    "milestone": "round-39 wave 1 (v1 build+falsify): re-derive and first-falsify the two frozen "
                 "claims, probe the discrimination controls, re-check routed defects D1-D6, draft "
                 "frontier material",
    "reportDir": ".ufo/waves/round-39/w1",
    "axes": ["operability", "calibration"],
    "context": CONTEXT,
    "items": ITEMS,
}

out = os.path.join(LANE, ".ufo/waves/round-39/w1-spec.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(spec, fh, indent=1)
    fh.write("\n")
print("wrote", out, "items", len(ITEMS))
