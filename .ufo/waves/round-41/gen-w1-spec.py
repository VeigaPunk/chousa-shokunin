#!/usr/bin/env python3
import json

L = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
items = [
    # --- executors: re-run the frozen counters and no-harm battery
    ("ExecC1BaseReceipt", "executor", f"Run `python3 corpus/evidence/round41/c1-count.py --gate .ufo/waves/round-41/controls/base-gate-r41.sh` in {L} (detached copy allowed); record CAPTURE_PIN_MATCH and confirm it differs from the committed controls/control-before.txt."),
    ("ExecC1LandedReceipt", "executor", f"Run `python3 corpus/evidence/round41/c1-count.py --gate tools/research-gate.sh` in {L}; record CAPTURE_PIN_MATCH and each cell verdict; confirm receipts/cells/cells.json matches."),
    ("ExecC2Count", "executor", f"Run `python3 corpus/evidence/round41/c2-count.py` in {L}; record W04_DISPOSITIONED and exit code; confirm 4/4 joins against the live census."),
    ("ExecC2Before", "executor", f"In a copy of {L} with corpus/evidence/round41/w04-dispositions.tsv removed, re-run c2-count.py; confirm W04_DISPOSITIONED=0/4 and exit 1 — the committed controls/c2-control-before.txt must match."),
    ("ExecNoHarm", "executor", f"Run in {L}: `bash tools/research-gate.sh --selftest` (record PASS/case count); then the pinned no-harm battery from corpus/evidence/round39/claims.md: verify-all claims 17/17, verify-chain, broken control drift, and the three archive exports on ../research/deep-research-2026-09-28/. Report every observable verbatim."),
    ("ExecPinDrift", "executor", f"Run `bash tools/research-gate.sh --pin /tmp/r41-pin-check.txt` and `--drift /tmp/r41-pin-check.txt` in {L} under a clean env; confirm GATE_PIN ok and GATE_DRIFT none, exit codes 0."),
    # --- reviewers: audit the change and the counters
    ("ReviewPinTable", "reviewer", f"Read tools/research-gate.sh captool_pin_init in {L}; verify every name in CAPTOOL_NAMES gets a GNU-version probe, absolute-path override check, and <NAME>_PROVENANCE refusal before records are read. Name any name that escapes the table."),
    ("ReviewChildPath", "reviewer", f"Read gate_canonical_capture in {L}/tools/research-gate.sh; verify the child env unsets LD_PRELOAD and LD_LIBRARY_PATH and sets PATH=$CAP_CHILD_PATH; check the override RESEARCH_GATE_CAPTURE_PATH is the only escape and that verify_all's own section children stay pinned."),
    ("ReviewC1Counter", "reviewer", f"Audit corpus/evidence/round41/c1-count.py in {L}: does each of the 12 cells assert the mechanism its name claims (QUALITY criterion 52)? Name any cell whose assertion is a weaker proxy or cannot fire on the base gate."),
    ("ReviewC2Counter", "reviewer", f"Audit corpus/evidence/round41/c2-count.py + w04-dispositions.tsv in {L}: can a TSV row pass with empty or unresolvable evidence? Does the join cover exactly the census's W04 ids? Verify the before/after receipt pair."),
    ("ReviewFreeze", "reviewer", f"Diff corpus/evidence/round41/claims.md against the landed tools/research-gate.sh and counters in {L}: is the frozen predicate the same sentence the counters implement (kumitate r42 rule)? Flag any post-data claim-text change or any landed behavior the freeze does not name."),
    ("ReviewSourcesRows", "reviewer", f"Verify S075 and S076 rows in {L}/corpus/SOURCES.md: 11 columns, tier/kind/status enums valid, anchor locates a ≤25-word quote in the named installed file (zcat + line numbers), sha256 cells match `sha256sum` of the files. Read the installed copies only — no network."),
    # --- critics: falsify the claims
    ("CriticC1Kill", "critic", f"Falsify C1 in {L}: find a PATH-resolved or function-delivered external invocation reachable by the canonical capture that the pin table + fixed child PATH do not cover (BASH_FUNC_*, command -v, eval'd names, aliases). Demonstrate on the landed gate or name it a covered named limit."),
    ("CriticC1Scope", "critic", f"Attack C1's scope in {L}: does the claim's 'measured surface' wording let an unmeasured tool slip in? Check the gate for external calls NOT in the r41 instrumentation trap set (cp/mv/ln/stat/find/xargs/jq/perl/awk). Each finding names call site and reachability from --pin/--drift."),
    ("CriticC2Kill", "critic", f"Falsify C2 in {L}: does w04-dispositions.tsv disposition anything real, or does it only narrate? Try: rename a disposition id, empty an evidence cell, add a TSV row for a non-warned id — does c2-count.py catch each? Report which mutations pass the counter (counter-blind cells)."),
    ("CriticSeparability", "critic", f"Verify causal separability in {L}: revert tools/research-gate.sh alone (use controls/base-gate-r41.sh) and confirm c2 still scores 4/4; keep gate and remove w04-dispositions.tsv and confirm c1 still scores 12/12. Any cross-dependency falsifies the claim pair."),
    ("CriticSourcedClaim", "critic", f"Attack the sourced-claim binding in {L}: does corpus/knowledge/capture-path-pin-r41.md actually need S075/S076, or is it grounded only in lane-own measurement? Check each S### citation resolves to a row opened this round and teaches what the note claims."),
    ("CriticMistakeRows", "critic", f"Attack corpus/lessons/round-41.md ## Mistakes in {L}: is each fix shown able to fail (CORPUS rule)? Is the W04/measurement-target entry a real mistake with evidence and captured-by, or padding?"),
    # --- scouts: reconnaissance per surface (loopback only — no fetches)
    ("ScoutTrapInventory", "scout", f"Re-run the r41 instrumentation sweep in {L} with a WIDER trap set than the committed list (add cp, mv, ln, install, awk, perl, file, join, fmt, pr, xargs, sed2, xxd): log every PATH-resolved call of one --pin and one --drift on the LANDED gate. Confirm zero marks or name new unmeasured surfaces. Local only."),
    ("ScoutFrontierOverlap", "scout", f"Scan sibling lane reports/SCORECARDs under /home/vgpnk/Projects/shokunin (read-only) for overlapping pin/PATH-independence work (mori pin/drift lineage, tsukuroi loader-env). Report overlaps chousa must attribute vs absorb. Local only."),
    ("ScoutProvinceBoundary", "scout", f"Check {L}/PROVINCE.md + SKILL.md against the r41 change: does capture-invocation pinning stay inside 'claim-vs-source verification'/'this lane's own gates'? Flag any bleed into kumitate orchestration or tsukuroi loader territory."),
    # --- scribes: draft-quality review of corpus artifacts (advisory)
    ("ScribeKnowledgeCheck", "scribe", f"Review corpus/knowledge/capture-path-pin-r41.md in {L}: provenance trio first, falsifiable limits, S075/S076/S067 citations correct, counts carry commands. List every claim in the note that lacks a resolvable pointer."),
    ("ScribeLessonGate", "scribe", f"Review corpus/lessons/round-41.md in {L}: ## Gate records every new S-row with URL/path, access date, ≤25-word located quote; Mistakes rows have class/evidence/captured-by/fix; census before→after pasted with exit codes."),
    ("ScribeSearchLog", "scribe", f"Check the round-41 Search log entry in {L}/corpus/SOURCES.md against CORPUS.md rule 5: question/query, where searched, date, identified/screened/included/excluded counts, exclusion reasons, stop rationale — and the 'registered hosts / open L0 fetch-scope' clause restored."),
    # --- mutation-testers
    ("MutatePinTable", "mutation-tester", f"Mutation-test the pin in {L}: on a sandbox copy, delete one CAPTOOL_NAMES entry and re-run c1-count.py — the corresponding cell must FAIL. Do the same by neutering one wrapper's absolute path (point at /bin/false). Report which mutations the counter misses."),
    ("MutateChildEnv", "mutation-tester", f"Mutation-test the child env in {L}: remove `-u LD_PRELOAD` or revert PATH to the caller's in a sandbox copy of the gate; c1 S11/S12 must fail. If they still pass, the cells are vacuous."),
    ("MutateC2Join", "mutation-tester", f"Mutation-test c2-count.py in {L}: feed a census stub emitting a W04 for S999 not in the TSV; the counter must print W04_DISPOSITIONED<4 and exit 1. Feed a TSV whose evidence names a missing path; it must also fail."),
    # --- sentinels
    ("SentinelWriteScope", "sentinel", f"Audit the r41 diff in {L}: confirm only tools/research-gate.sh, corpus/**, .ufo/waves/round-41/** changed; no fleet paths, no sibling paths, no .ufo/state or watchdog; no aggregator-owned files committed."),
    ("SentinelFetchScope", "sentinel", f"Audit r41 for external egress in {L}: grep the round's wave spec, counters, lesson, SOURCES rows for https?:// references and verify every source open used installed files only; flag any item whose semantics require network (the r40 ScoutHashSource class)."),
    ("SentinelCounterPin", "sentinel", f"Audit commit-pinning of r41 evidence in {L}: do c1-count.py/c2-count.py and the receipts name the gate path + revision they measured? Flag any receipt that can silently re-measure a different tree than the cited commit (the r40 ReviewActivePopulation class)."),
    # --- revengers
    ("RevengerPinHistory", "revenger", f"Reverse-engineer the r35-r40 pin lineage in {L} (grep→env→bash→sha256 pins + lessons): does the r41 table miss a previously-named sibling bare name or duplicate a mechanism the earlier pins already cover? Cite the r37/r38/r39 named-limit lists."),
    ("RevengerW04History", "revenger", f"Trace the W04 warnings S051/S053/S073/S074 to their origin rounds in {L} corpus/lessons and search log: is each disposition in w04-dispositions.tsv faithful to the recorded origin, or does any row rewrite history?"),
    # --- connector + simplifier
    ("ConnectorSiblingScan", "connector", f"Connector scan in /home/vgpnk/Projects/shokunin (read-only): which sibling lanes pin tool invocations or run capture/drift gates (mori census lineage)? Where could chousa's CAPTOOL table be reused, and does any sibling artifact contradict the r41 mechanism? Report cross-lane evidence only."),
    ("SimplifierAudit", "simplifier", f"Simplification audit of the r41 diff in {L}: is the 14-name pin table minimal — any pinned name never invoked by the measured surface (pure padding)? Is the per-name override boilerplate reducible without losing a check? Report only; no edits."),
    ("CriticDoNothing", "critic", f"Attack the do-nothing control in {L}: controls/base-gate-r41.sh must be byte-identical to the pre-round gate (diff against git show). Confirm control-before.txt was produced by that control and not by an intermediate edit; any substitution falsifies the before measurement."),
]

spec = {
    "wave": "chousa-r41-w1",
    "milestone": "Round 41: independently audit the frozen capture-invocation-pin claim (C1) and W04-disposition claim (C2); no production edits, no external fetches",
    "reportDir": ".ufo/waves/round-41/w1",
    "axes": ["operability", "calibration", "depth"],
    "context": "\n".join([
        "# Goal",
        f"chousa lane (deep-research method), round 41, one v1 build-and-first-falsify wave. Frozen claims: {L}/corpus/evidence/round41/claims.md. Lane repo: {L}. Fleet repo /home/vgpnk/Projects/shokunin is read-only; sibling lanes and domain source trees are read-only.",
        "",
        "# Claim bindings",
        "C1 operability (lowest scored axis, 3/10): `python3 corpus/evidence/round41/c1-count.py --gate tools/research-gate.sh` must print `CAPTURE_PIN_MATCH=12/12`; control `.ufo/waves/round-41/controls/base-gate-r41.sh` must score `1/12`. C2 calibration: `python3 corpus/evidence/round41/c2-count.py` must print `W04_DISPOSITIONED=4/4`; the TSV is corpus/evidence/round41/w04-dispositions.tsv.",
        "",
        "# Seat contract",
        "- Every seat is a leaf; do not spawn, dispatch, or create background work.",
        f"- Work read-only against committed lane artifacts; write only your own uniquely named report under {L}/.ufo/waves/round-41/w1/. Never modify lane production files, the lane git index or jj state, /home/vgpnk/Projects/shokunin/.ufo/state, the fleet repo, or sibling repos.",
        f"- Every `Report:` trailer path is relative to {L} — write it at {L}/<that path>. Use absolute paths for every other read/write.",
        "- Use the route assigned by the host role table at /home/vgpnk/.omp/agent/config.yml; never pass or hardcode a model.",
        "- NO external live-target fetches or network egress of any kind. Source re-opens read INSTALLED/committed copies only (man pages under /usr/share/man, /usr/share/info, committed capture bodies under .ufo/waves/round-31/). A seat that judges a live read necessary reports it as a finding, never performs it (round-40 ScoutHashSource lesson: a dispatch item is not an operator approval).",
        "- Tooling authorization: any agent may install or update a tool that helps this task or is a strict upgrade; read /home/vgpnk/.omp/agent/RULES.md first, use official sources only, and record tool/version/channel/reason in the report. Pacman transactions are PAUSED host-wide: do not run pacman -S, -Sy, -Syu, -U, or -R; use an approved non-pacman channel or file an L0 question.",
        "- The planner seat is the L1; the validator rejects `planner` as a swarm role. The bounded planning data-walk rides the scout and connector items.",
        "- Each report records the assigned attack, exact command and output, verdict, and a resolvable artifact pointer.",
        "- Measure against the pinned committed tree, not a mutable worktree (round-40 lesson: reviewers observed worktree-only mismatches when a sibling round's in-flight edits changed tools/research-gate.sh). Where a counter takes --gate, pass the committed path.",
    ]),
    "items": [{"name": n, "role": r, "item": t} for n, r, t in items],
}
import os
out = os.path.join(os.path.dirname(__file__), "w1-spec.json")
with open(out, "w") as f:
    json.dump(spec, f, indent=1)
print(f"wrote {out}: {len(items)} items")
