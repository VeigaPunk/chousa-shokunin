#!/usr/bin/env python3
"""gen-w1-spec.py — build the round-46 chousa wave-1 spec (v1 band 32-64).

Wave 1 = build + first falsifiers. Seats are read-only toward production
files: each writes only its own report; the L1 integrates. Absolute paths
only; the `reportDir` stays lane-relative.
"""
import json
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
OUT = pathlib.Path(LANE) / ".ufo/waves/round-46/w1-spec.json"
EV = f"{LANE}/corpus/evidence/round46"
FIX = f"{LANE}/corpus/fixtures/inference-ground-r46"
PKG = "/home/vgpnk/Projects/shokuknow/merge/chousa"
QC = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache"
C = {
    "S085": f"{QC}/5a631adb18988a1a2421ce75.txt",
    "S086": f"{QC}/1c15b611118dee97e4105fcf.txt",
    "S087": f"{QC}/7800e2e1e2df3bc124b6b83e.txt",
    "S088": f"{QC}/b73f7e8dd5b0ace740e48046.txt",
    "S089": f"{QC}/78761b633aee2289e5874ce9.txt",
}
BASE = "corpus/knowledge/evidence-pool-versioning-r39.md"
AMEND = "corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md"

DIRECTIVE = """You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

CONTEXT = f"""# Goal
chousa lane (deep-research method: question framing, source hierarchy, citation chaining, claim-vs-source verification), round 46, wave 1 (build + first falsifiers). Three claims are FROZEN in {EV}/claims.md at lane commit `c2f0e9d100c0d46633a6277b2fd51d2ac99678eb` — read it first; never propose changing a predicate, a counter, a fixture set or a target.
- C1 operability (lowest scored axis, 3/10): `tools/inference-ground.py` makes inference grounding executable. It must exit 0 on every `positive-*.md` fixture and 1 on every `junk-*.md` fixture of {FIX}/. Counter `{EV}/c1-count.py`. Before: `TOOL=absent POSITIVE_PASS=0/3 JUNK_KILLED=0/3` exit 1. Controls: an always-exit-0 tool scores JUNK_KILLED=0/3; a citation-presence-only tool scores 1/3.
- C2 calibration: every committed gate entry point — (A) each file directly under tools/, (B) the round-45 pattern (corpus/evidence/round*/{{c<N>-count*,verify-receipts,errata-count}}.py), (C) every EXISTING *.py/*.sh path that SCORECARD.md or a corpus/evidence/round*/claims*.md names — must be named by repo-relative path inside a `## Gates` row of {LANE}/SKILL.md. Counter `{EV}/c2-count.py --list`. Before (base tree): `ENTRY_POINTS=71 (tools=7 counters=50 named=66) GATES_ROWS=30 REGISTERED=55/71 UNREGISTERED=16` exit 1.
- C3 depth (assimilation §10, one theme: what makes a support verdict durable, and how a later corpus binds each citation to an archived state): adopt TWO staged entries as lane entries {BASE} (rows S085 FEVER dataset page, S086 FEVER ACL paper, S087 FEVER Zenodo record) and {AMEND} (rows S088 AVeriTeC dataset page, S089 AVerImaTeC arXiv HTML). Eleven located quotes must sit in {EV}/spans.tsv, each span file an exact slice of its capture at the recorded offset. Counter `{EV}/c3-count.py` (default and --lane-only). Before: `ENTRIES=0/2` exit 1. Lane ids follow S084; the staged ids (S120–S122, S127, S128, and prose ids such as S071/S082/S095) must be re-bound BY DOCUMENT and never by id arithmetic.

# Sources (read-only, no fetch)
On-disk campaign capture cache (file = sha256(url)[:24].txt): S085 {C['S085']}; S086 {C['S086']}; S087 {C['S087']}; S088 {C['S088']}; S089 {C['S089']}. Staged package {PKG} (MERGE-REPORT.md, SOURCES.append.md, knowledge/corpus/knowledge/evidence-pool-versioning-r39*.md). Lane registry {LANE}/corpus/SOURCES.md (rows S079 = RFC 7089, S080 = WARP FAQ, S081 = NDL E2867, S082–S084 = AVeriTeC README / paper / train.json); lane schema and rules /home/vgpnk/Projects/shokunin/CORPUS.md; lane bar {LANE}/corpus/QUALITY.md (criteria 64–65 are this lane's newest); province {LANE}/PROVINCE.md; previous round {LANE}/corpus/lessons/round-45.md and its non-author spot-check {LANE}/corpus/lessons/round-45-verifier-spotcheck.md (routed defects D7, D8); frozen round-45 claims {LANE}/corpus/evidence/round45/claims.md.

# Seat contract
- Every seat is a leaf: do not spawn, dispatch or create background work. The only exception: an executor may spawn one read-only `labrat` probe for one falsifiable hypothesis.
- Write ONLY your own report file. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Never write anywhere else in the lane, never modify lane production files, the lane git index or jj state (no git add/commit/stash/checkout/reset, no mutating jj), the fleet repo /home/vgpnk/Projects/shokunin (including its .ufo/state and .scratch), any sibling lane, or anything under /home/vgpnk/Projects/shokuknow (read-only; never run its tools renumber-staged.py, merge-plan.py, quote-lint.py, absent-defect-register.py).
- Scratch work goes under /tmp/chousa-r46-<YourName>/ and you delete it before you finish.
- Use absolute paths for every read and write; your tools start at the fleet root, so a relative path lands in the wrong repo.
- NO external live-target fetches and no network egress of any kind (fetch-scope L0 8d77e6c1 is open). Read on-disk captures and committed files only. A dispatch item is NOT an operator approval; if you judge a live read necessary, report it as a finding and do not perform it.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md before installing, official channels only, record tool/version/channel/reason in your report. Reading RULES.md is a precondition for an INSTALL only, not for writing your report. pacman guard: all pacman transactions are PAUSED host-wide — never run pacman -S, -Sy, -Syu, -U or -R; use uv tool / npx / an official binary in ~/.local/bin, or report the need.
- Routing is the host role table (~/.omp/agent/config.yml task.agentModelOverrides; operator-owned, read-only). Never pass or hardcode a model.
- The planner seat is the L1 (the validator rejects `planner` as a swarm role); bounded planning data-walks ride scout and connector items.
- Never message agent://all. Your report records: the item you were given, every command you ran with its verbatim output (trim long output, keep the decisive lines), your verdict, and resolvable pointers (path:line, char offset, sha256). Never assert a result you did not run. Keep the report under 150 lines."""

GATE_HINT = (
    "The Gates table columns are: name | kind | entry | verdict map | self-test | pinned values | write scope | owner "
    "(read the rows between `## Gates` and the next `## ` heading in " + LANE + "/SKILL.md, e.g. `research-gate round-45 counters`, "
    "and copy their conventions). Draft rows ONLY for the paths named in your item, one row per instrument family, each a single line "
    "starting with `| ` and ending with ` |`, exactly 8 cells, naming every listed file by its full repo-relative path in the entry cell, "
    "a verdict map stating each exit code (`exit 0` / `exit 1` / `exit 2`) and the exact PASS print values, the control that fails it in the "
    "self-test cell, the measured lane commit or receipt in pinned values, `read-only` or the receipt path it writes in write scope, and "
    "`chousa` as owner. If a script was superseded, say so with the successor path. Run each listed script read-only once (never pass an option "
    "that writes a receipt into the lane; if the script writes without an option, snapshot and restore its bytes and say so) and paste output and "
    "exit code, so the row states observed values. Put the rows verbatim in a fenced block in your report. Never invent a command you did not run."
)


def opener(name, sid, extra):
    return (name, "reviewer",
            f"Open lane source {sid} this round and locate the quotes that will ground its Registry row. Capture: {C[sid]}. "
            f"Report: sha256 of the capture and its byte/char length; for EACH listed quote, its char offset (Python str.find), occurrence count, "
            f"the 120 chars either side verbatim, and a verbatim slice of at most 25 words that can serve as the row's anchor. "
            f"{extra} Also state which sentences of the staged entry ({PKG}/knowledge/corpus/knowledge/evidence-pool-versioning-r39.md and its "
            f"-amendment-2026-10-23.md) this source actually supports, and any staged sentence it CONTRADICTS (quote both sides). "
            f"Verdict per quote: located / absent. No fetch.")


ITEMS = [
    # --- C3 source opening (5 reviewers, one per row)
    opener("ReviewOpenS085", "S085",
           "Quotes: `A list of evidence sets`; `Pre-processed Wikipedia Pages (June 2017 dump)`; the sentence that names the FEVER evidence tuple fields."),
    opener("ReviewOpenS086", "S086",
           "Quotes: `used the June 2017 Wikipedia dump, processed`; `recall of 72.36%`; `We found that 91.2%`; and the passage that states 31.75/16.82/12.15 percent of claims needing multi-sentence or multi-page evidence. NOTE the capture is PDF text with column interleaving: report exactly what is contiguous."),
    opener("ReviewOpenS087", "S087",
           "Quotes: `conceptdoi` and the two DOI values beside it; `wiki-pages.zip`; the publication date field. State what the API record documents and does not (e.g. whether it versions the Wikipedia pages inside the deposit)."),
    opener("ReviewOpenS088", "S088",
           "Quotes: `An archive.org link for the source url`; `Our best estimate for the date the claim first appeared`; the four-label sentence containing `Conflicting Evidence`. Report which field each belongs to (evidence answer vs claim) and whether the claim-level archive description carries a qualifier."),
    opener("ReviewOpenS089", "S089",
           "Quotes: `temporally constrained evidence annotation`; the sentence about evidence `published before the claim’s date` (note the curly apostrophe — report the exact bytes); and the reported kappa / QA-pair consistency figures. State which section each sits in."),

    # --- C3 entry drafting (3 scribes)
    ("ScribeEntryBase", "scribe",
     f"Draft the lane's re-grounded version of {PKG}/knowledge/corpus/knowledge/evidence-pool-versioning-r39.md for {LANE}/{BASE}. "
     f"Header lines exactly: `source: S085 — https://fever.ai/dataset/fever.html — <your located anchor>`, `source: S086 — https://aclanthology.org/N18-1074.pdf — <anchor>`, `source: S087 — https://zenodo.org/api/records/4925954 — <anchor>`, `verified-at: 2026-10-25`, `recheck: 365d`, then a `ground:` line in the lane's own words with NO campaign queue ids. "
     f"Read {LANE}/corpus/knowledge/evidence-archive-field-policy-r41.md and citation-version-binding-r36.md for the lane's entry style. Body: `#### Observation` / `#### Inference` / `#### Unknown`. "
     f"RULE (frozen C1): every Inference bullet must cite at least one of S085/S086/S087 and must carry at least one grounding token — a backticked or double-quoted phrase of two or more words, or a numeral of three or more digits or a percentage — and EVERY such token must appear verbatim in the capture ({C['S085']} / {C['S086']} / {C['S087']}). Test your draft with `python3 {LANE}/tools/inference-ground.py --entry <your draft in /tmp> --spans /dev/null --counts /dev/null` is NOT enough: instead check each token by hand with grep and paste the offsets. "
     f"Correct the staged text where the captures disagree with it (the staged 'We used the June 2017 Wikipedia dump' and '91.2 % of the examples' are not contiguous in the PDF capture — say what is). Remove every campaign cross-reference and every S-id outside S079–S089. Cite RFC 7089 as lane S079 and the timestamped WARP URL as lane S081, each in a sentence that names the document. Put the full draft in a fenced block."),
    ("ScribeEntryAmend", "scribe",
     f"Draft the lane's re-grounded version of {PKG}/knowledge/corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md for {LANE}/{AMEND}. "
     f"Header: `source: S088 — https://fever.ai/dataset/averitec.html — <located anchor>`, `source: S089 — https://arxiv.org/html/2505.17978v2 — <anchor>`, `verified-at: 2026-10-25`, `recheck: 365d`, a `ground:` line in lane words with no campaign queue id (no 'Q14', no wave-4). Body: Observation / Inference / Unknown, and it must state that it CONTINUES the base entry by path (the lane now holds both). "
     f"Same frozen C1 rule: every Inference bullet cites S088 or S089 and every grounding token appears verbatim in {C['S088']} / {C['S089']}. The staged amendment's 'before the claim's date' uses an ASCII apostrophe and is ABSENT from the capture, which has a curly one — report both and use the capture's bytes. The staged references to 'round 1's S071' and 'round 2's S082' must be re-bound by document (lane S079 = RFC 7089; lane S081 = the NDL E2867 WARP timestamp-in-URL note) and 'the lane's S095 amendment' replaced by the lane path that actually holds the claim. Put the full draft in a fenced block."),
    ("ScribeRows", "scribe",
     f"Draft the five lane Registry rows (S085–S089) in CORPUS.md / census schema — 11 cells each: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by — for {C['S085']} (FEVER dataset page), {C['S086']} (FEVER ACL paper N18-1074), {C['S087']} (FEVER Zenodo record 4925954), {C['S088']} (AVeriTeC dataset page), {C['S089']} (AVerImaTeC arXiv 2505.17978v2). "
     f"Read the staged rows S120–S122 and S127–S128 in {PKG}/SOURCES.append.md for provenance, and copy the shape of lane rows S079–S084 from {LANE}/corpus/SOURCES.md. Rules: status `mined`; opened `2026-10-25`; recheck a valid ISO date or `NNd` (no prose — list the stripped prose separately); NO literal or escaped `|` in any cell; anchor = your own located quote of at most 25 words (locate it yourself with Python in the capture and paste the char offset); teaches = one grounded learner benefit; used-by exactly `{BASE}` for S085–S087 and `{AMEND}` for S088–S089. Check EACH drafted line has exactly 12 `|` and `awk -F'|' 'NF!=13'` reports nothing. Put the rows verbatim in a fenced block plus the stripped-prose list."),
    ("ScribeGateBlock", "scribe",
     f"Draft the `## Gate` section for {LANE}/corpus/lessons/round-46.md: the one theme, the two admitted entries (with the per-entry province and bar check), the ADMIT entries, the REJECT decision, and for every new row the URL, access date `2026-10-25` and a <=25-word located quote. "
     f"Read {LANE}/corpus/lessons/round-45.md `## Gate` for the shape. The reject to record: the staged amendment was refused in round 45 (base entry not held, prose ids wrong) and this round adopts it ONLY because the flip condition is met — say exactly which parts of the flip are met and paste the evidence pointers (the base entry path, the re-bound ids, the located quotes). Add a second rejection candidate to judge: `{PKG}/knowledge/corpus/knowledge/claim-support-test-r37-amendment-2026-10-23.md` as an adoption candidate for a LATER round, with a one-sentence reason and flip condition (check whether the lane holds its base entry and whether its rows are in the staged append). Record the id-collision result and the pre-append census exit as placeholders the L1 fills from {EV}/. Put the block in a fenced block."),

    # --- C2: Gates rows for the unregistered verifiers (3 scribes)
    ("ScribeGatesR24to27", "scribe",
     f"Draft SKILL.md Gates rows covering these unregistered instruments, in families: {LANE}/corpus/evidence/round24-measure.sh, round25-measure.sh, round25-ledger-recount.py, round25-meta-differential.sh, round26-measure.sh, round26-date-differential.sh, round26-registry-differential.sh, round27-mechanisms.py, round27-regressions.py, round27-falsify-controls.py (all under {LANE}/corpus/evidence/). "
     f"Read each script's header/argparse to state its real entry, exit contract and write scope; read {LANE}/SCORECARD.md and LOG.md for the round cells that name it. " + GATE_HINT),
    ("ScribeGatesR33R34", "scribe",
     f"Draft SKILL.md Gates rows covering {LANE}/corpus/evidence/round33/d2-census.py, round33/no-name-signals.sh, round34/self-audit.py, and round30/qr_harness.py (qris named only incidentally today — decide and state whether it deserves a row or a superseded note). "
     f"Round-45 closure D8 named round34/self-audit.py as the counterexample; read {LANE}/corpus/lessons/round-33.md, round-34.md and SCORECARD.md for what each instrument measured. " + GATE_HINT),
    ("ScribeGatesR46", "scribe",
     f"Draft SKILL.md Gates rows for round 46: (a) `tools/inference-ground.py` — entry `python3 tools/inference-ground.py --entry PATH --spans TSV --counts JSON [--root DIR] [--json OUT] [--quiet]`, exit 0 no findings / 1 findings / 2 usage; self-test `python3 corpus/evidence/round46/c1-count.py`; (b) this round's three counters {LANE}/corpus/evidence/round46/c1-count.py, c2-count.py, c3-count.py with the frozen targets from {EV}/claims.md. Read {EV}/claims.md, the three docstrings, the counter sources and the committed controls in {EV}/controls/. Run each once read-only and paste output and exit code (before landing they are expected to FAIL — state that the row gives the frozen targets and quote the control files for the self-test cell). " + GATE_HINT),

    # --- C1/C3 build executors
    ("ExecSpanBuilder", "executor",
     f"Write, in /tmp/chousa-r46-ExecSpanBuilder/, a builder script `build-spans.py` that produces {EV}/spans.tsv and {EV}/spans/*.txt for ELEVEN located quotes: S085 `A list of evidence sets`, S085 `Pre-processed Wikipedia Pages (June 2017 dump)`, S086 `used the June 2017 Wikipedia dump, processed`, S086 `recall of 72.36%`, S086 `We found that 91.2%`, S087 `10.5281/zenodo.4925953`, S087 `wiki-pages.zip`, S088 `An archive.org link for the source url`, S088 `Our best estimate for the date the claim first appeared`, S089 `temporally constrained evidence annotation`, S089 `published before the claim’s date`. "
     f"Contract: capture file = sha256(url)[:24].txt under {QC}; each span file content is the EXACT slice capture[o:o+len(quote)+1] (the quote plus its following newline, so the counter's slice equality holds); the manifest row is 7 tab columns (id url capture_sha256 offset span_file quote entry) with offset = the char offset of the quote and capture_sha256 = sha256 of the capture file; entry = `{BASE}` for S085–S087 and `{AMEND}` for S088–S089. "
     f"Write to a /tmp tree first, run `python3 {LANE}/corpus/evidence/round46/c3-count.py --root <tree>` if the entries exist there (else state which legs fail only for missing entries), and paste: the builder source, each quote's offset, each span's byte length, and a re-derivation that capture[o:o+len]==span for all eleven. Do NOT write into the lane."),
    ("ExecApplyEntries", "executor",
     f"Apply the new inference-grounding rule to the lane's four admitted entries as a measurement (not a gate): run `python3 {LANE}/tools/inference-ground.py --entry <entry> --spans {EV}/spans.tsv --counts /dev/null` for each of {LANE}/corpus/knowledge/evidence-archive-field-policy-r41.md, evidence-snapshot-coverage-r40.md, citation-version-binding-r36.md, citation-version-binding-r37.md. Paste every finding. Then say, per entry, which bullets fail only because (a) no backticked/quoted token exists, (b) no numeral is grounded, (c) the span manifest has no span for the cited id. This measures the D7 gap on the lane's existing corpus; do not edit the entries."),
    ("ExecRegistryMirror", "executor",
     f"Build the pre-append mirror the assimilation contract requires, in /tmp/chousa-r46-ExecRegistryMirror/: copy {LANE}/corpus/ (including SOURCES.md), {LANE}/tools/ and the two drafted entries (take them from the wave reports of ScribeEntryBase/ScribeEntryAmend if present; else use stand-ins and say so), append the five S085–S089 rows into the mirror's `## Registry`, and run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md`. Paste the full output and exit code. If it reports E03/E04 name the colliding ids; if it reports E11 'missing used-by', check whether the mirror carries tools/quarantine-check.py (round-45 mistake 3) and fix the mirror, not the lane. Also run the live census `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` and paste exit code."),
    ("ExecCounterRun", "executor",
     f"Run the three frozen counters against the CURRENT lane tree (working tree, which already carries tools/inference-ground.py but not the entries) and against a `git archive` of the freeze commit `c2f0e9d100c0d46633a6277b2fd51d2ac99678eb` extracted to /tmp: paste `python3 {EV}/c1-count.py --root X`, `--c2-count.py --root X --list`, `--c3-count.py --root X` outputs and exit codes for both trees. Then run `bash {LANE}/tools/research-gate.sh --selftest 2>&1 | tail -2` and `bash {LANE}/tools/parent-lifetime.sh --selftest --receipt /tmp/chousa-r46-ExecCounterRun/st.receipt; echo $?` as regression evidence that nothing this round touched those instruments."),

    # --- falsifiers of the frozen claims
    ("ReviewerC1Tool", "reviewer",
     f"Code-review {LANE}/tools/inference-ground.py against the frozen R46-C1 sentence in {EV}/claims.md. Check: does `inference_bullets` end the section exactly at the next heading of level <= 4 and treat fenced headings as literal? Do grounding-token extraction and the numeral variants match the sentence? Can a bullet with an S-id inside code/backticks pass the citation leg? Is the counts leg case-safe? Does `--root` mis-report entry paths? Run it on all six fixtures and paste. Report mismatches with line numbers; do not edit."),
    ("ReviewerC2Set", "reviewer",
     f"Independently re-derive C2's entry-point set: enumerate (A) files under {LANE}/tools/, (B) the round-45 pattern under corpus/evidence/round*/, (C) every existing *.py/*.sh path named in {LANE}/SCORECARD.md or corpus/evidence/round*/claims*.md — with YOUR OWN script, not by importing c2-count.py. Compare set-for-set with `python3 {EV}/c2-count.py --root {LANE} --list` (paste both, state the differences). Then judge: which of the 66 named paths are not gates at all (harnesses, oracles, one-off measurement scripts) and would a Gates row for them mislead? Name up to five and say what the counter should not have included (do not change the counter)."),
    ("ReviewGatesSection", "reviewer",
     f"Read the `## Gates` section of {LANE}/SKILL.md and report: the exact column header, how many rows the frozen C2 rule counts (run `python3 {EV}/c2-count.py --root {LANE} --list | tail -3` and paste), every line starting with `|` inside the section that the rule does NOT count (fewer than 8 separators or no `exit`), and whether any `### ` subsection sits inside the section before the next `## ` heading. State the exact insertion point (line number and neighbouring row names) where this round's new rows must go, and whether a row naming a path inside a fenced code block would be counted (test it on a /tmp copy)."),
    ("ReviewerC3Spans", "reviewer",
     f"Review the span plan for C3. For each of the eleven planned quotes (list in {EV}/claims.md C3), locate it yourself in its capture, report char offset and occurrence count, and say whether it is contiguous in the capture (the PDF and HTML captures have line breaks and interleaving). Flag any planned quote that is NOT contiguous or occurs more than once and give a replacement slice of at most 25 words that IS contiguous and unique. Also check the two cross-reference bindings: does {LANE}/corpus/knowledge/citation-version-binding-r36.md hold RFC 7089's Memento-Datetime claim, and does citation-version-binding-r37.md hold the WARP timestamp-in-URL claim — so that the amendment can cite S079/S081 by document?"),
    ("CritC1Attack", "critic",
     f"Attack C1's fixture set as an oracle. Read {EV}/claims.md C1 and {FIX}/. Ask: do the three junk fixtures cover the D7 class fairly, or are they strawmen (the junk-uncited fixture also fails the grounding leg, so a citation-only tool still kills it)? Write a FOURTH junk mutant in /tmp that reuses correct spans and figures and asserts something wrong while every emergent token is grounded (e.g. correct quote, wrong quantifier: 'every' where the span says 'some'), run the tool, and report: killed or survives. Then state the narrowest sentence that describes what the tool now enforces, and what it still cannot."),
    ("CritC2Framing", "critic",
     f"Attack C2's framing as calibration. Is 'a path named in SCORECARD.md or a claims file' the right surface for a gate registry, or does it register instruments that are evidence, not gates? Which executable verifiers remain OUTSIDE the frozen set even after the extension (grep the lane for *.py/*.sh under corpus/evidence/, scripts/, .ufo/waves/ that no SCORECARD row names but that a round's receipt depends on)? Give the strongest objection, the residual list with paths, and a one-sentence judgement: does the extension make the registry agree with the tree (claim verified) or merely with the prose?"),
    ("CritC3Inference", "critic",
     f"Attack the two drafted entries (read the reports of ScribeEntryBase and ScribeEntryAmend; if absent, attack the staged originals in {PKG}/knowledge/corpus/knowledge/). For each Inference bullet: does it state more than its cited capture supports? Specifically test (1) 'the durability comes from freezing the pool, not from stamping the citations' against {C['S085']} and {C['S087']} (does the FEVER page or the Zenodo record say anything about revisions?); (2) the amendment's claim that AVeriTeC answers Q14 — does {C['S088']} say the archive link is per citation and best-effort, and does {C['S089']} say the constraint is operational? (3) any figure in either entry that you cannot find verbatim in a capture. Verdict per bullet: holds / holds narrowed (give the narrowed sentence) / fails."),
    ("MutC1Junk", "mutation-tester",
     f"Mutation-test the new gate: build SIX mutants of {FIX}/positive-a.md in /tmp/chousa-r46-MutC1Junk/ — (1) drop the citation, (2) change one word inside a backticked phrase, (3) replace a grounded numeral with 4,137, (4) move the grounding token into the Observation section only, (5) add a fenced heading `#### Inference` inside the section (fence-shadow), (6) replace `#### Inference` with `## Inference`. Run {LANE}/tools/inference-ground.py on each and paste exit codes and findings; report any mutant the tool accepts. Then run {EV}/c1-count.py with your mutants as the fixture set (use --root on a copied tree) and say whether the counter's declared 3/3+3/3 would catch them."),
    ("MutC2Forge", "mutation-tester",
     f"Attack {EV}/c2-count.py with five forges on /tmp copies (use --root/--skill): (a) a row naming the paths with a WRONG verdict map and a dead command; (b) a row with 8 separators inside a fenced code block in the Gates section; (c) the same paths in an HTML comment inside Gates; (d) a row placed inside a `### ` subsection of Gates (the frozen rule runs to the next `## `); (e) a path named only as a prefix of another path (e.g. `corpus/evidence/round34/self-audit.py` present while the entry point is `.../self-audit.pyc`). Report REGISTERED/UNREGISTERED for each and whether the counter matches its frozen rule (b, c, d are the interesting ones)."),

    # --- scouts / connector / sentinel
    ("ScoutProvinceFit", "scout",
     f"Province check for the two entries to adopt: read {LANE}/PROVINCE.md and the staged entries in {PKG}/knowledge/corpus/knowledge/ (evidence-pool-versioning-r39.md and its -amendment-2026-10-23.md). chousa owns claim-vs-source verification, source hierarchy, citation chaining; it refuses model-quality/evaluation claims (kengaku) and orchestration (kumitate). Judge each entry sentence-group: in province or out? Quote the deciding sentences. Name every sentence that must be cut on adoption, and whether the entry's 'the authors measured the labels themselves' paragraph crosses into model evaluation."),
    ("ScoutCoverageGround", "scout",
     f"Coverage check: read {LANE}/corpus/README.md (coverage map and `## Frontier`). Grep {LANE}/corpus/knowledge/ for FEVER, AVeriTeC, zenodo, archive, cached, Memento, durable, verdict. Report what version-binding/archive ground the lane already holds (file:line) and whether 'what makes a support verdict durable inside a verification corpus, and how a successor corpus binds each citation to an archived state' is ground the coverage map does NOT hold. Draft the two coverage-map rows in the map's exact shape (quote an existing row)."),
    ("ScoutQuarantineOverlap", "scout",
     f"Quarantine check for the five URLs to adopt: run `python3 {LANE}/tools/quarantine-check.py slice` and the operator awk recipe over /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md, then grep the whole register for 'fever.ai', 'aclanthology', 'zenodo', '2505.17978', '2305.13117', 'AVeriTeC', 'AVeriMaTeC'. Report every hit with line number and lane. Verdict: is any adopted row quarantined (yes/no) and is the 24-row slice still 24 rows today (paste the count)?"),
    ("ScoutCollisionRecheck", "scout",
     f"Re-run the id-collision check independently for this round's append: extract `^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}` ids from {LANE}/corpus/SOURCES.md and from {PKG}/SOURCES.append.md, intersect, and report the intersection size and members. Confirm the lane's highest id is S084 so the next five are S085–S089, and check that no staged row URL equals an existing lane row URL (the census E04 class) for the five adopted documents. Then verify the by-document mapping for the amendment's prose ids: which document does staged S071 name, which lane id holds RFC 7089, which lane id holds the NDL E2867 note?"),
    ("ScoutInheritedTree", "scout",
     f"Report `git -C {LANE} status --porcelain`, `git -C {LANE} diff --stat`, and the lane tip via `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state {LANE}`. Confirm the three modified paths are the previously left-named ones and name any untracked path this round's seats created in the lane. Check /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md for an operator answer to (a) 8d77e6c1 fetch scope, (b) the round-43 inherited-tree question, (c) the round-44 round-shape question; quote the lines or state 'no answer'."),
    ("ConnectSiblings", "connector",
     f"Sibling-overlap scan: grep every sibling lane corpus under /home/vgpnk/Projects/shokunin/*-shokunin/corpus/ (exclude chousa) for FEVER, AVeriTeC, zenodo, 'archive.org', Memento, 'cached_source_url', 'evidence pool'. Report each hit with lane and path:line and judge whether adopting this theme absorbs a sibling's held ground. Also run `git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec) and attribute every untracked file whose content names chousa or round-46 (misroot sweep; the fleet root copy is the one to report, never delete)."),
    ("SentScopeAudit", "sentinel",
     f"Audit the round's new code for scope and egress: read {LANE}/tools/inference-ground.py, {EV}/c1-count.py, c2-count.py, c3-count.py. Grep for urllib, requests, socket, http.client, curl, wget, os.system, subprocess and any write path. Report each hit and whether it can egress or write outside its declared scope (c1: temp-free, subprocess only to the tool; c2: read-only; c3: read-only + cache reads; tool: read-only). Also verify no new file this round writes into /home/vgpnk/Projects/shokuknow or the fleet repo, and that the fixture spans.tsv's bogus digest cannot be mistaken for a real capture digest (state what a reader would have to check)."),
]


def main():
    items = [{"name": n, "role": r, "item": DIRECTIVE + "\n\n" + t} for n, r, t in ITEMS]
    spec = {
        "wave": "chousa-r46-w1",
        "milestone": "Round 46 wave 1 (build + first falsifiers): open five sources, draft two entries and their rows, build the span manifest, register the unregistered verifiers, falsify the three counters; no fetch, no seat writes to production files",
        "reportDir": ".ufo/waves/round-46/w1",
        "axes": ["operability", "calibration", "depth"],
        "context": CONTEXT,
        "items": items,
    }
    OUT.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    roles = {}
    for i in items:
        roles[i["role"]] = roles.get(i["role"], 0) + 1
    print("wrote", OUT, len(items), "items", roles)


if __name__ == "__main__":
    main()
