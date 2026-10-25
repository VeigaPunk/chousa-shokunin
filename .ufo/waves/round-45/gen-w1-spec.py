#!/usr/bin/env python3
"""gen-w1-spec.py — build the round-45 chousa wave-1 spec (v1 band 32-64).

Wave 1 = build + first falsifiers. Seats are read-only toward production
files: each writes only its own report; the L1 integrates. Absolute paths
only; the `reportDir` stays lane-relative.
"""
import json
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
OUT = pathlib.Path(LANE) / ".ufo/waves/round-45/w1-spec.json"
EV = f"{LANE}/corpus/evidence/round45"
PKG = "/home/vgpnk/Projects/shokuknow/merge/chousa"
QC = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache"
README_C = f"{QC}/ce16d57277fedfd4f0e7750e.txt"
PAPER_C = f"{QC}/412b146a2720ce6557268d05.txt"
TRAIN_C = f"{QC}/974299ae4b5f3bdb808b36a9.txt"

DIRECTIVE = """You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

CONTEXT = f"""# Goal
chousa lane (deep-research method: question framing, source hierarchy, citation chaining, claim-vs-source verification), round 45, wave 1 (build + first falsifiers). Three claims are FROZEN in {EV}/claims.md at lane commit d82cec904bf0fb8736886b9f17be913c7807427a — read it first; never propose changing a predicate, a counter or a target.
- C1 operability: tools/parent-lifetime.sh gets an exit contract (exit 3 on zero tasks or any seat timeout; required --timeout recorded as timeout_s= in the start line). Counter {EV}/c1-count.py (stub `kimi` on PATH). Control: the round-44 tool scores CASES_MATCH=1/5.
- C2 calibration: every committed gate entry point (files directly under tools/, and corpus/evidence/round*/c<N>-count*.py, verify-receipts.py, errata-count.py) must be named by repo-relative path inside a Gates row of {LANE}/SKILL.md (the `## Gates` section; a row starts with `|`, has >=8 `|`, contains `exit`). Counter {EV}/c2-count.py --list. Before: 29 unregistered at the freeze tree.
- C3 depth (assimilation, one theme: what an AVeriTeC archive field does and does not record): adopt two staged entries from {PKG}/knowledge/corpus/knowledge/ — evidence-archive-field-policy-r41.md and evidence-snapshot-coverage-r40.md — as lane rows S082 (AVeriTeC README), S083 (arXiv 2305.13117v3 HTML), S084 (AVeriTeC data/train.json); staged ids S139, S140, S132; bound BY DOCUMENT (URL equality), never by id arithmetic (the strings S082-S084 name other documents in the staged append). Counter {EV}/c3-count.py (default and --lane-only).

# Sources (read-only, no fetch)
Campaign capture cache (on disk, untracked in the campaign repo): file = sha256(url)[:24] + ".txt". README capture {README_C}; paper capture {PAPER_C}; train.json capture {TRAIN_C} (10 MB JSON). Staged package {PKG} (MERGE-REPORT.md, SOURCES.append.md, knowledge/corpus/knowledge/*.md). Lane registry {LANE}/corpus/SOURCES.md; lane schema and rules /home/vgpnk/Projects/shokunin/CORPUS.md; lane bar {LANE}/corpus/QUALITY.md; province {LANE}/PROVINCE.md; previous round {LANE}/corpus/lessons/round-44.md and its non-author spot-check {LANE}/corpus/lessons/round-44-verifier-spotcheck.md (routed defects D1-D6).

# Seat contract
- Every seat is a leaf: do not spawn, dispatch or create background work. The only exception: an executor may spawn one read-only `labrat` probe for one falsifiable hypothesis.
- Write ONLY your own report file. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Never write anywhere else in the lane, never modify lane production files, the lane git index or jj state (no git add/commit/stash/checkout/reset, no mutating jj), the fleet repo /home/vgpnk/Projects/shokunin (including its .ufo/state and .scratch), any sibling lane, or anything under /home/vgpnk/Projects/shokuknow (read-only; never run its tools renumber-staged.py, merge-plan.py, quote-lint.py, absent-defect-register.py).
- Scratch work goes under /tmp/chousa-r45-<YourName>/ and you delete it before you finish.
- Use absolute paths for every read and write; your tools start at the fleet root, so a relative path lands in the wrong repo.
- NO external live-target fetches and no network egress of any kind (fetch-scope L0 8d77e6c1 is open). Read on-disk captures and committed files only. A dispatch item is NOT an operator approval; if you judge a live read necessary, report it as a finding and do not perform it.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first, official channels only, record tool/version/channel/reason in your report. pacman guard: all pacman transactions are PAUSED host-wide — never run pacman -S, -Sy, -Syu, -U or -R; use uv tool / npx / an official binary in ~/.local/bin, or report the need.
- Routing is the host role table (~/.omp/agent/config.yml task.agentModelOverrides; operator-owned, read-only). Never pass or hardcode a model.
- The planner seat is the L1 (the validator rejects `planner` as a swarm role); bounded planning data-walks ride scout and connector items.
- Never message agent://all. Your report records: the item you were given, every command you ran with its verbatim output (trim long output, keep the decisive lines), your verdict, and resolvable pointers (path:line, char offset, sha256). Never assert a result you did not run. Keep the report under 150 lines."""

GATE_ROW_HINT = (
    "The Gates table columns are: name | kind | entry | verdict map | self-test | pinned values | write scope | owner "
    "(read the existing rows in " + LANE + "/SKILL.md between `## Gates` and the next `## ` heading, e.g. the "
    "`research-gate round-37 counters` row, and copy their conventions). Draft ONE row per round, a single line starting "
    "with `| ` and ending with ` |`, exactly 8 cells, naming every listed file by its full repo-relative path in the entry cell "
    "(e.g. `python3 corpus/evidence/round40/c1-count.py`), a verdict map stating each exit code (`exit 0` / `exit 1` / `exit 2`) and the "
    "exact PASS print values from the counter/claims, the control that fails it in the self-test cell, the measured lane commit or "
    "receipt in pinned values, `read-only` or the receipt path it writes in write scope, and `chousa` as owner. "
    "If a counter was superseded (a later -v2/-v3 replaced it), say so in the verdict map with the successor path. "
    "Read each listed counter's docstring/argparse and the round's claims.md and SCORECARD.md verdict before drafting. "
    "Run each listed counter once (from " + LANE + ", read-only; pass no option that writes a receipt into the lane) and paste its output and exit code, "
    "so the row's verdict map states observed values, not remembered ones. Put the row verbatim in a fenced block in your report."
)


def gate(name, rnd, files, extra=""):
    fl = ", ".join(files)
    return (name, "scribe",
            f"Draft the SKILL.md Gates row for round {rnd}'s gate entry points: {fl}. "
            f"Evidence: {LANE}/corpus/evidence/round{rnd}/claims.md (if present), {LANE}/SCORECARD.md (the round {rnd} verdict section), "
            f"{LANE}/LOG.md and {LANE}/corpus/lessons/round-{rnd}.md. {extra} {GATE_ROW_HINT}")


ITEMS = [
    # --- C2: Gates rows (scribes, one per round)
    gate("ScribeGateR31", 31, ["corpus/evidence/round31/c1-count.py", "corpus/evidence/round31/c1-count-v3.py",
                               "corpus/evidence/round31/c2-count.py", "corpus/evidence/round31/c2-count-v3.py"]),
    gate("ScribeGateR32", 32, ["corpus/evidence/round32/c1-count.py", "corpus/evidence/round32/c2-count.py"],
         "The round's -v2/-v3 counters already have a row (`research-gate round-32 counters`); these are the v1 counters it superseded."),
    gate("ScribeGateR33", 33, ["corpus/evidence/round33/c1-count.py", "corpus/evidence/round33/c1-count-v3.py"],
         "The -v2 counter already has a row (`research-gate round-33 counters`)."),
    gate("ScribeGateR34", 34, ["corpus/evidence/round34/c1-count.py", "corpus/evidence/round34/c1-count-v2.py"],
         "c1-count-v3.py and c2-count.py already have rows."),
    gate("ScribeGateR40", 40, ["corpus/evidence/round40/c1-count.py", "corpus/evidence/round40/c2-count.py"]),
    gate("ScribeGateR41", 41, ["corpus/evidence/round41/c1-count.py", "corpus/evidence/round41/c2-count.py"]),
    gate("ScribeGateR42", 42, ["corpus/evidence/round42/c1-count.py", "corpus/evidence/round42/c2-count.py"]),
    ("ScribeGateQuarantine", "scribe",
     f"Draft the SKILL.md Gates row for the tool `tools/quarantine-check.py` (subcommands slice, examine, verdict, digests; round 42). "
     f"Read {LANE}/tools/quarantine-check.py (docstring, argparse, exit codes) and {LANE}/corpus/lessons/round-42.md. Run `python3 {LANE}/tools/quarantine-check.py slice | wc -l` and "
     f"`python3 {LANE}/tools/quarantine-check.py verdict | cut -f1,2 | sort | uniq -c | head` and paste outputs and exit codes. {GATE_ROW_HINT}"),
    gate("ScribeGateR43", 43, ["corpus/evidence/round43/c1-count.py", "corpus/evidence/round43/c2-count.py",
                               "corpus/evidence/round43/c3-count.py"]),
    ("ScribeGateAbsentSplit", "scribe",
     f"Draft the SKILL.md Gates row for the tool `tools/absent-split.py` (round 43). Read {LANE}/tools/absent-split.py (docstring, argparse, exit codes) and "
     f"{LANE}/corpus/lessons/round-43.md; run it once read-only with its documented default invocation and paste output and exit code. {GATE_ROW_HINT}"),
    gate("ScribeGateR44", 44, ["corpus/evidence/round44/c1-count.py", "corpus/evidence/round44/c2-count.py",
                               "corpus/evidence/round44/c3-count.py", "corpus/evidence/round44/errata-count.py"],
         "Note the round-44 closure's D1: c3-count.py reads an untracked campaign capture path, so the row must say it is not reproducible from the lane tree alone."),
    ("ScribeGateLauncher", "scribe",
     f"Draft the SKILL.md Gates row for `tools/parent-lifetime.sh` AS IT WILL BE after round 45's C1 lands: entry `bash tools/parent-lifetime.sh --dispatch JSON --receipt PATH --agent FILE --timeout SECS` "
     f"and `--selftest --receipt PATH`; exit 0 only when n_spawned>0, n_spawned=n_reaped and no seat exited 124/137; exit 3 when the end line is written but zero tasks were spawned or a seat timed out; exit 1 if a child pid was not captured or the parent pid changed; exit 2 usage (including a dispatch run without --timeout); start line `start parent_pid=… epoch=… timeout_s=…`. "
     f"Self-test: `python3 corpus/evidence/round45/c1-count.py` (CASES_MATCH=5/5) with control corpus/evidence/round45/controls/c1-control-r44-tool.txt (1/5). "
     f"Read {LANE}/tools/parent-lifetime.sh (current, pre-fix) and {EV}/claims.md. {GATE_ROW_HINT}"),
    ("ScribeGateR45", "scribe",
     f"Draft the SKILL.md Gates row for round 45's three counters: corpus/evidence/round45/c1-count.py, corpus/evidence/round45/c2-count.py, corpus/evidence/round45/c3-count.py. "
     f"Read {EV}/claims.md and the three counters' docstrings and the committed controls in {EV}/controls/. Run each counter once read-only and paste output and exit code (before landing they are expected to FAIL; state that the row's verdict map gives the frozen targets, and quote the control files for the self-test cell). {GATE_ROW_HINT}"),

    # --- C3: re-grounding the two entries (reviewers / scouts / executor / critics)
    ("ReviewQuoteReadmeSource", "reviewer",
     f"Locate the quote `An archive.org link for the source url` in the README capture {README_C}. Report: sha256 of the file, its byte and char length, the char offset (Python str.find) and the occurrence count of the quote, and the 200 chars around it verbatim. Confirm the field it describes is `cached_source_url` inside the per-answer evidence object (not the claim level). Verdict: located / absent."),
    ("ReviewQuoteReadmeClaim", "reviewer",
     f"Locate the quote `Where possible, an archive.org link to the original claim url` in the README capture {README_C}. Report sha256, char offset (Python str.find), occurrence count, the 200 chars around it verbatim, and confirm the field is the claim-level `cached_original_claim_url`. Also report every other field in that README whose description mentions archive.org. Verdict: located / absent."),
    ("ReviewQuotePaperCache", "reviewer",
     f"Locate the quote `we cache all pages used as evidence in the internet archive` in the paper capture {PAPER_C} (arXiv 2305.13117v3 HTML rendered to text). Report sha256, char offset (Python str.find), occurrence count and 300 chars of context verbatim; state which section of the paper it sits in (search backward for the nearest heading-like line). Verdict: located / absent."),
    ("ReviewQuotePaper404", "reviewer",
     f"Locate the quote `Archive.org returns a 404 page for these` in the paper capture {PAPER_C}. Report sha256, char offset (Python str.find), occurrence count and 500 chars of context verbatim. Answer precisely: WHAT returns a 404 (which kind of link), WHOSE links these are (fact-checking articles? evidence pages?), and where in the paper it sits (main text or annotation-guideline appendix). This finding is new to the lane; state the strongest reading the text supports and nothing wider."),
    ("ExecRecountTrain", "executor",
     f"Independently recount, with your own code (do not import or copy {EV}/c3-count.py), from the train.json capture {TRAIN_C}: number of records; number of evidence answers (records -> questions -> answers) carrying the key `cached_source_url`, how many are non-empty and how many empty (state your emptiness rule: None, empty string, whitespace); number of records carrying `cached_original_claim_url`, non-empty, empty. Also report the sha256 of the file and whether any answer object lacks the key entirely, and how many records lack the claim key. Paste your script and output."),
    ("ExecEmptyEvidenceRecord", "executor",
     f"In the train.json capture {TRAIN_C}, find the ONE evidence answer whose `cached_source_url` is empty. Report its record index, claim text (first 200 chars), the answer's source_url, answer_type and source_medium, and whether that record's other answers are archived. Then look for any `cached_source_url` value that is NOT an archive.org URL, and any archive.org value that embeds archive.is/archive.md (the paper's double-archived case). Report counts and three examples. Paste your script and output."),
    ("CritFieldPolicyInference", "critic",
     f"Attack the staged entry {PKG}/knowledge/corpus/knowledge/evidence-archive-field-policy-r41.md. Its inference: an empty claim-level `cached_original_claim_url` records that no archive was TAKEN, not that none exists; an empty evidence-level `cached_source_url` would be the anomaly. Using only the README capture {README_C} and the paper capture {PAPER_C}, argue the strongest case that this inference over-reads the documentation (e.g. 'Where possible' can mean the archive attempt failed; README descriptions are not a policy). Also check the entry's claim that 'Where possible' occurs once in the paper and is about extractive answers. Verdict: inference holds / holds narrowed (give the narrowed sentence) / fails."),
    ("CritSnapshotInference", "critic",
     f"Attack the staged entry {PKG}/knowledge/corpus/knowledge/evidence-snapshot-coverage-r40.md. In particular: (1) 'the two differ by two orders of magnitude' — compute the archived shares (6510/6511 vs 1145/2531) and the missing shares (1/6511 vs 1386/2531) and say which ratio, if any, is two orders of magnitude; give the corrected sentence; (2) 'The single empty evidence entry is worth more than the 6,510 that are filled' — is this supported or rhetoric?; (3) the entry says it amends a campaign entry the lane does not hold (evidence-pool-versioning-r39-amendment-2026-10-23.md) and names 'the lane's r31 sha256' and 'location binding gap' — check {LANE}/corpus/knowledge/ for revision-binding-r31.md and any 'location binding' text, and say which cross-references survive adoption. Verdict per point."),
    ("ScoutProvinceFit", "scout",
     f"Province check for the two entries to adopt (read {LANE}/PROVINCE.md and both staged entries). chousa owns claim-vs-source verification and source hierarchy; it refuses model-quality or evaluation claims (-> kengaku) and orchestration. Judge each entry: is it about how a corpus binds a claim/evidence citation to an archived state (in province), or about evaluating a fact-checking model (out)? Quote the sentences that decide it. Also list any sentence in either entry that would have to be cut as out of province."),
    ("ScoutCoverageGround", "scout",
     f"Coverage check: read {LANE}/corpus/README.md (coverage map, `## Frontier`) and grep {LANE}/corpus/knowledge/ for archive, snapshot, Memento, cached, AVeriTeC, FEVER, revision-binding. Report what archive/version-binding ground the lane already holds (file:line) and whether 'what an archive field in a verification corpus records, and how much of a real corpus carries it' is ground the lane did NOT hold. Draft the two coverage-map rows for the adopted entries in the map's exact row shape (quote an existing row to show the shape)."),
    ("ScribeRowsNormalize", "scribe",
     f"Draft the three lane Registry rows in CORPUS.md / census schema (11 cells: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by) from the staged rows S139, S140, S132 in {PKG}/SOURCES.append.md, renumbered BY DOCUMENT to lane S082 (README), S083 (paper), S084 (train.json). Rules: status `mined`; opened `2026-10-25`; recheck a valid ISO date, `NNd` or symbolic cadence — strip any prose and list the stripped prose separately; NO literal or escaped `|` in any cell; anchor rewritten as your own located quote of <=25 words that you located yourself in the capture (README {README_C}, paper {PAPER_C}, train.json {TRAIN_C}); used-by exactly `corpus/knowledge/evidence-archive-field-policy-r41.md` for S082/S083 and `corpus/knowledge/evidence-snapshot-coverage-r40.md` for S084; teaches = a grounded learner benefit, no pipe. Read {LANE}/corpus/SOURCES.md rows S079-S081 and copy their shape. Count the `|` in each drafted line (must be 12). Put the three rows verbatim in a fenced block plus the stripped-prose list."),
    ("ScribeEntryFieldPolicy", "scribe",
     f"Draft the lane's re-grounded version of {PKG}/knowledge/corpus/knowledge/evidence-archive-field-policy-r41.md for {LANE}/corpus/knowledge/evidence-archive-field-policy-r41.md. Header lines exactly: `source: S082 — https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/README.md — <anchor>`, `source: S083 — https://arxiv.org/html/2305.13117v3 — <anchor>`, `verified-at: 2026-10-25`, `recheck: 365d`, then a `ground:` line in the lane's own words (no campaign queue ids like Q17). Read {LANE}/corpus/knowledge/citation-version-binding-r36.md for the lane's entry style. Body: Observation / Inference / Unknown. It MUST contain verbatim these four strings: `An archive.org link for the source url`, `Where possible, an archive.org link to the original claim url`, `we cache all pages used as evidence in the internet archive`, `Archive.org returns a 404 page for these` (locate each yourself in {README_C} / {PAPER_C}). Add the 404 finding as the lane's own addition: a filled archive field is not proof that the archived capture resolves. Remove every campaign cross-reference (round-6 count, Q17) and every S-id other than S082/S083 (and S084 if you reference the counts entry). Put the full draft in a fenced block."),
    ("ScribeEntrySnapshot", "scribe",
     f"Draft the lane's re-grounded version of {PKG}/knowledge/corpus/knowledge/evidence-snapshot-coverage-r40.md for {LANE}/corpus/knowledge/evidence-snapshot-coverage-r40.md. Header: `source: S084 — https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/data/train.json — <anchor naming the two fields and 3,068 records, 10,184,813 bytes>`, `verified-at: 2026-10-25`, `recheck: 365d`, a `ground:` line in the lane's own words. Remove the claim that it amends a campaign entry the lane does not hold and every S-id other than S084 (it may point to corpus/knowledge/evidence-archive-field-policy-r41.md by path). Keep the seven figures exactly as `3,068`, `6,511`, `6,510`, `1` (written as the word-bounded digit), `2,531`, `1,145`, `1,386` — recount them yourself from {TRAIN_C} first and stop if any differs. Fix the 'two orders of magnitude' sentence so it is arithmetically true (compute it). Resolve the entry's Unknown 'whether an empty cached_source_url means no archive exists or none was taken' by pointing to the field-policy entry, narrowly. Put the full draft in a fenced block."),
    ("CritRejectPoolAmendment", "critic",
     f"Judge the same-theme staged entry {PKG}/knowledge/corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md as an adoption candidate THIS round, and argue for refusing it. Check: (1) it amends evidence-pool-versioning-r39.md, which the lane does not hold (ls {LANE}/corpus/knowledge/); (2) its prose ids (S071, S082, S095, S127, S128) — map each by document against {PKG}/SOURCES.append.md and {LANE}/corpus/SOURCES.md and say which point at the wrong document in lane numbering; (3) whether its quotes sit in the captures of https://fever.ai/dataset/averitec.html and https://arxiv.org/html/2505.17978v2 (cache file = sha256(url)[:24].txt under {QC}; compute the names, report presence, sizes, and each quote located/absent with offsets). Give a reject reason and a flip condition, one sentence each."),
    ("ScoutQuarantineOverlap", "scout",
     f"Confirm that none of the three URLs to adopt (README, paper, train.json — see context) is in the lane's quarantine slice: run `python3 {LANE}/tools/quarantine-check.py slice` and the operator recipe `awk -F'|' -v l='chousa' '$2 ~ (\"`\" l \"`\") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {{print $4, $5}}' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`, and grep the whole register for 'AVeriTeC', '2305.13117' and 'MichSchli'. Report every hit with line numbers and its lane, and whether any adopted row is quarantined."),
    ("ScoutCollisionRecheck", "scout",
     f"Re-run the id-collision check independently: extract row ids with the 0-3-space pattern `^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}` from {LANE}/corpus/SOURCES.md and {PKG}/SOURCES.append.md, intersect them, and compare with the committed {LANE}/.ufo/waves/round-45/assimilation/collisions (empty) and reg-ids/staged-ids. Then check the by-document map {LANE}/.ufo/waves/round-45/assimilation/renumber-map.tsv: for each staged id there, confirm the URL in the staged row equals the map URL, and report which documents the strings S082, S083, S084 name in the staged append. Verdict: map holds / breaks (which row)."),

    # --- C1: launcher (executors / reviewer / critic)
    ("ExecLauncherPatch", "executor",
     f"Write, in /tmp/chousa-r45-ExecLauncherPatch/, a patched copy of {LANE}/tools/parent-lifetime.sh that meets predicate R45-C1 in {EV}/claims.md with the smallest diff: required --timeout in dispatch mode (exit 2 without it), `timeout_s=<value>` in the start line (selftest too), exit 3 when the end line is written but n_spawned=0 or any reap exit_code is 124 or 137, otherwise the existing contract. Then run `python3 {EV}/c1-count.py --tool <your copy>` and the selftest `bash <your copy> --selftest --receipt /tmp/chousa-r45-ExecLauncherPatch/st.receipt; echo $?`. Paste the unified diff against the lane tool, both outputs and exit codes. Do NOT write into the lane."),
    ("ExecLauncherEdge", "executor",
     f"Probe edge cases of the round-44 launcher {LANE}/tools/parent-lifetime.sh with a stub `kimi` on PATH (copy the stub idea from {EV}/c1-count.py): a seat killed by SIGKILL after the --kill-after window (exit 137), a stub that exits 1 (seat failure, not timeout), a dispatch file that is not JSON, a dispatch with a task name containing a space. Report for each: the tool's exit code and the receipt lines. Then state which of these the frozen C1 predicate covers and which it does not (do not propose changing the predicate; name the residual as a limit)."),
    ("ReviewC1Counter", "reviewer",
     f"Review {EV}/c1-count.py for correctness against the predicate sentence in {EV}/claims.md: does each case check exactly what the sentence says (exit code, end-line fields, both reap lines exit_code=124, start-line timeout_s value)? Is the stub honest (does `exec sleep 30` under `timeout 1` really produce 124)? Can the counter false-PASS on a tool that ignores --timeout? Run it against the lane tool and paste output. Report any mismatch between sentence and code with line numbers."),
    ("CritC1Harm", "critic",
     f"Attack C1 for harm: making --timeout required and returning exit 3 on a timed-out seat — does any committed lane script, doc or counter call tools/parent-lifetime.sh without --timeout or depend on exit 0 (grep {LANE} for parent-lifetime)? Does round-44's c1-count.py or its committed receipts still verify after the change (they read receipts, not the tool — check)? Is a start line with timeout_s still parsed by {LANE}/corpus/evidence/round44/c1-count.py (run it against corpus/evidence/round44/parent-lifetime.receipt and against a copy with ` timeout_s=5` appended to the start line in /tmp)? Verdict: harm / no harm, with evidence."),

    # --- counters: mutation testing (mutation-testers)
    ("MutC1Mutants", "mutation-tester",
     f"Build four mutant launchers in /tmp/chousa-r45-MutC1Mutants/ from {LANE}/tools/parent-lifetime.sh, each breaking exactly one C1 case: (1) exit 0 on zero tasks, (2) no timeout_s in start line, (3) default timeout instead of required, (4) exit 0 on a timed-out seat. Run `python3 {EV}/c1-count.py --tool <mutant>` for each and paste outputs. Every mutant must score <5/5 and exit 1; report any that survives."),
    ("MutC2Forges", "mutation-tester",
     f"Attack {EV}/c2-count.py with forges on a /tmp copy of the lane (cp -r {LANE}/SKILL.md {LANE}/tools {LANE}/corpus/evidence into /tmp/chousa-r45-MutC2Forges/ keeping relative layout, then use --root): (a) paste an unregistered path into a prose line of the Gates section; (b) a row with 7 `|`; (c) a row with 8 `|` but no `exit`; (d) a valid-looking row placed after the next `## ` heading; (e) a valid row in a `### ` subsection inside Gates (does the counter treat ### as leaving the section? the frozen rule says up to the next `## ` heading). Report UNREGISTERED for each and whether the counter matches the frozen rule. Also add a new file tools/x.sh and confirm it is counted."),
    ("MutC3Mutants", "mutation-tester",
     f"Attack {EV}/c3-count.py on scratch trees under /tmp/chousa-r45-MutC3Mutants/ (use --root; build a minimal passing tree first by writing the two entries, three Registry rows inside a `## Registry` section, spans.tsv (7 tab columns: id url capture_sha256 offset span_file quote entry), span files and counts.json from the REAL captures in {QC}, so the default mode PASSes). Then apply one mutation each: row URL changed; row status `queued`; used-by missing the entry; span offset +1; capture sha256 wrong; one count off by one in the entry; entry cites `source: S139` instead of S082. Each must fail the default mode; report which also fail --lane-only. Paste outputs."),
    ("SentNoEgress", "sentinel",
     f"Prove the round's new code cannot reach the network or write outside its scope: read {EV}/c1-count.py, c2-count.py, c3-count.py and {LANE}/.ufo/waves/round-45/assimilation/map-staged.py; grep for urllib, requests, socket, http.client, curl, wget, subprocess and any write path. Report every hit and whether it can egress or write into the lane/campaign tree. Also check that c1-count.py's temp dirs are removed (TemporaryDirectory) and that PATH injection cannot run a non-stub `kimi`."),

    # --- C2 critic / reviewer
    ("CritC2Framing", "critic",
     f"Attack C2's framing as calibration: is the SKILL.md Gates table the lane's self-assessment? Is the entry-point set (files directly under tools/, and corpus/evidence/round*/c<N>-count*.py, verify-receipts.py, errata-count.py) the right set — list every other executable or counter-like file in {LANE} (e.g. *.py/*.sh under corpus/evidence/, .ufo/waves/, scripts) that a reader would call a gate, with a one-line judgement each. Would registering superseded v1 counters mislead a reader? Verdict and the strongest objection."),
    ("ReviewGatesSection", "reviewer",
     f"Read {LANE}/SKILL.md lines 75-120 (the Gates table) and report: the exact column header, how many rows the frozen C2 rule counts as rows (run `python3 {EV}/c2-count.py --list` and paste), any existing row the rule does NOT count (lines starting `|` with <8 pipes or no `exit`), and whether any `### ` subsection sits inside `## Gates` before the next `## ` heading. Recommend where new rows must be inserted (line number) so they sit inside the section."),

    # --- frontier / lesson / quality / hygiene
    ("ScribeQuality64", "scribe",
     f"Ground the operator proposal 'Tag each round as research ground or plumbing' ({LANE}/considerthese/2026-10-24.md, section 'Self-improvement proposals (not acted on)') through the lane's bar: for rounds 35-44, read each round's claims in {LANE}/SCORECARD.md verdict sections and classify each claim as `ground` (adds research coverage: a new opened source or knowledge entry) or `plumbing` (hardens the lane's own tools/gates), with the evidence line. Give the table, the per-round ratio, and draft QUALITY.md criterion 64 (read {LANE}/corpus/QUALITY.md for the style of 62 and 63) that requires the tag, cites considerthese/2026-10-24.md and its date, and states how the criterion can fail."),
    ("ScribeMistakes", "scribe",
     f"Mine candidate `## Mistakes` rows for {LANE}/corpus/lessons/round-45.md from the round-44 non-author spot-check {LANE}/corpus/lessons/round-44-verifier-spotcheck.md (routed D1-D6) and the round-44 lesson. For each, give: class · evidence pointer (path:line) · captured-by (the criterion or rule that should have caught it, or `none`) · fix · how the fix is shown able to fail. Mark which ones round 45's frozen claims address (C1 = D5, C2 = D2, C3 = D1) and draft the erratum for D4 (verify the E2867 capture mtime with `stat` on {QC}/0034b800811072de3980e85b.txt and the launch line in /home/vgpnk/Projects/shokunin/.ufo/watchdog.log for chousa round=44)."),
    ("ScribeShonen", "scribe",
     f"Read {LANE}/SHONEN.md and draft one line per box for the round-45 report: `[x]` only with a named NON-AUTHOR verifier (this wave's seats are author-lane: none qualifies), `[~]` with a resolvable evidence pointer, `[ ]` if untouched. The round-44 closure said box 3 carries the open D2 Gates-registry gap — C2 targets it. Give each line with its pointer."),
    ("ConnectSiblings", "connector",
     f"Sibling-overlap scan: grep the sibling lane corpora under /home/vgpnk/Projects/shokunin/*-shokunin/corpus/ (exclude chousa) for AVeriTeC, FEVER, archive.org, Memento, cached_source_url, 'evidence archiv'. Report each hit with lane and path:line, and judge whether adopting the two AVeriTeC entries into chousa absorbs a sibling's held ground (adjacency harm) or duplicates it. Read-only; also report `git -C /home/vgpnk/Projects/shokunin status --porcelain | head -20` and attribute any path that names chousa or round-45."),
    ("ConnectRouteTable", "connector",
     f"Read /home/vgpnk/.omp/agent/config.yml (READ ONLY) and report the task.agentModelOverrides entries for scout, reviewer, critic, connector, sentinel, executor, mutation-tester, scribe, simplifier, labrat, plus async.maxJobs, task.maxConcurrency, task.maxRecursionDepth, and the file's sha256. State which alias each role resolves to. Do not change anything."),
    ("SimplifyCounters", "simplifier",
     f"Read {EV}/c1-count.py, c2-count.py and c3-count.py and report dead code, redundancy, and logic that could drift from the frozen predicate sentences in {EV}/claims.md. Propose deletions only where frozen semantics stay byte-identical in output. Report only — do not edit. Also judge {LANE}/.ufo/waves/round-45/assimilation/map-staged.py: its `cited_by` column scans every S-id in an entry body, which mixes campaign prose ids with `source:` ids; say whether that column is misleading and the one-line fix."),
    ("ScoutInheritedTree", "scout",
     f"Report `git -C {LANE} status --porcelain` and `git -C {LANE} diff --stat`, and confirm the three modified paths are exactly the round-44 disposition's left-named rows ({LANE}/corpus/evidence/round44/disposition.tsv). Check /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md for any operator answer to the `chousa | round-43` inherited-tree question or the `chousa | round-44` round-shape question, or to 8d77e6c1 (fetch scope). Report the lines verbatim."),
]


def main():
    items = [{"name": n, "role": r, "item": DIRECTIVE + "\n\n" + t} for n, r, t in ITEMS]
    spec = {
        "wave": "chousa-r45-w1",
        "milestone": "Round 45 wave 1 (build + first falsifiers): draft the missing Gates rows, re-ground two AVeriTeC entries from on-disk captures, probe the launcher exit contract, mutation-test the three frozen counters; no fetch, no production writes by seats",
        "reportDir": ".ufo/waves/round-45/w1",
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
