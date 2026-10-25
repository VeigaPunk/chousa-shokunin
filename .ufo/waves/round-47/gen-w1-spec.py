#!/usr/bin/env python3
"""gen-w1-spec.py — build the round-47 chousa wave-1 spec (v1 band 32-64).

Wave 1 = build + first falsifiers. Seats are read-only toward production
files: each writes only its own report; the L1 integrates. Absolute paths
only; the `reportDir` stays lane-relative.
"""
import hashlib
import json
import pathlib

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
OUT = pathlib.Path(LANE) / ".ufo/waves/round-47/w1-spec.json"
EV = f"{LANE}/corpus/evidence/round47"
FIX = f"{LANE}/corpus/fixtures/inference-ground-r47"
PKG = "/home/vgpnk/Projects/shokuknow/merge/chousa"
STAGED = f"{PKG}/knowledge/corpus/knowledge"
QC = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache"
REG = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md"
URLS = {
    "S085": "https://fever.ai/dataset/fever.html",
    "S090": "https://aclanthology.org/2026.findings-acl.19.pdf",
    "S091": "https://ojs.aaai.org/index.php/AAAI/article/download/29825/31432",
    "S092": "https://arxiv.org/html/1803.05355",
    "S093": "https://arxiv.org/html/2012.00614v2",
    "S094": "https://aclanthology.org/2025.coling-main.108.pdf",
}
C = {k: f"{QC}/{hashlib.sha256(u.encode()).hexdigest()[:24]}.txt" for k, u in URLS.items()}
BASE = "corpus/knowledge/claim-support-test-r37.md"
AMEND = "corpus/knowledge/claim-support-test-r37-amendment-2026-10-23.md"

DIRECTIVE = """You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

CONTEXT = f"""# Goal
chousa lane (deep-research method: question framing, source hierarchy, citation chaining, claim-vs-source verification), round 47, wave 1 (build + first falsifiers). Three claims are FROZEN in {EV}/claims.md at lane commit `22a44b8b5c923d25123a96a852c11938559bb9b2` — read it first; never propose changing a predicate, a counter, a fixture set, a floor or a target.
- C1 operability (lowest scored axis, 3/10): `{LANE}/tools/inference-ground.py` gains a polarity probe (rule 5 of its docstring, finding `INF_POLARITY_FLIP`), landed at `a15610a59aaeaf43b79ccc650acee4bd4da00341`. Counter `python3 {EV}/c1-count.py` over {FIX}/ (3 positives, 3 junk polarity flips, CANARY, the round-46 counter and the two round-46 entries as no-regression legs). Before `JUNK_KILLED=0/3 C1=FAIL`; at the landing `C1=PASS`. Controls in {EV}/controls/c1-controls.txt.
- C2 calibration: `python3 {EV}/c2-count.py --list` — the round-46 gate-entry set plus a DEPENDENCE leg (paths an entry point's source names, closed) and a CHECK-NAMED leg (paths corpus/QUALITY.md or SKILL.md outside `## Gates` names); a path counts as registered only when a `## Gates` row of {LANE}/SKILL.md names it in its `entry` cell (3rd cell) with an exit code in its `verdict map` cell (4th); DANGLING = a Gates row naming a *.py/*.sh path the tree lacks; FLOOR=92 enforced in code. Before (freeze tree) `ENTRY_POINTS=92 UNREGISTERED=25 DANGLING=0 MISMATCHES=25 C2=FAIL`; target `MISMATCHES=0`.
- C3 depth (assimilation §10, one theme: what a support test is, how it is applied, how reliable it is): adopt the staged `{STAGED}/claim-support-test-r37.md` and `{STAGED}/claim-support-test-r37-amendment-2026-10-23.md` as lane entries `{LANE}/{BASE}` and `{LANE}/{AMEND}`. Ids bind BY DOCUMENT (URL equality), never arithmetic: staged S097 → held lane S085 ({URLS['S085']}), S098 → S090 ({URLS['S090']}), S099 → S091 ({URLS['S091']}), S113 → S092 ({URLS['S092']}), S114 → S093 ({URLS['S093']}), S115 → S094 ({URLS['S094']}). Counter `python3 {EV}/c3-count.py` (and `--lane-only`): ≥12 span rows in {EV}/spans.tsv, ≥2 per id, each span an exact capture slice with context; every `char N` in the anchor cells of S085 and S090–S094 equal to a located quote offset; both entries exit 0 under tools/inference-ground.py; four quarantine verdict lines (register S093, S094, S108, S110) in the round lesson. Before: every leg 0, `C3=FAIL`.

# Sources (read-only, no fetch)
On-disk campaign capture cache (file = sha256(url)[:24].txt): S085 {C['S085']}; S090 {C['S090']}; S091 {C['S091']}; S092 {C['S092']}; S093 {C['S093']}; S094 {C['S094']}. Staged package {PKG} (MERGE-REPORT.md, SOURCES.append.md rows S097–S099 and S113–S115, the two staged entries). Absent-defect register (read-only) {REG}. Lane registry {LANE}/corpus/SOURCES.md (S001–S089; S085 = FEVER dataset page, S086 = FEVER NAACL PDF N18-1074); lane schema and rules /home/vgpnk/Projects/shokunin/CORPUS.md; lane bar {LANE}/corpus/QUALITY.md (criterion 66 is the newest); province {LANE}/PROVINCE.md; previous round {LANE}/corpus/lessons/round-46.md and its non-author closure {LANE}/corpus/lessons/round-46-verifier-spotcheck.md (routed defects 1–6); round-46 wave reports {LANE}/.ufo/waves/round-46/w1/ and w2/ (e.g. CritC1D7.md, RevC2TagCount.md); the lane's held support-state entry {LANE}/corpus/knowledge/claim-support-states-r24.md.

# Seat contract
- Every seat is a leaf: do not spawn, dispatch or create background work. The only exception: an executor may spawn one read-only `labrat` probe for one falsifiable hypothesis.
- Write ONLY your own report file. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Never write anywhere else in the lane, never modify lane production files, the lane git index or jj state (no git add/commit/stash/checkout/reset, no mutating jj), the fleet repo /home/vgpnk/Projects/shokunin (including its .ufo/state and .scratch), any sibling lane, or anything under /home/vgpnk/Projects/shokuknow (read-only; never run its tools renumber-staged.py, merge-plan.py, quote-lint.py, absent-defect-register.py).
- Scratch work goes under /tmp/chousa-r47-<YourName>/ and you delete it before you finish.
- Use absolute paths for every read and write; your tools start at the fleet root, so a relative path lands in the wrong repo.
- NO external live-target fetches and no network egress of any kind (fetch-scope L0 8d77e6c1 is open). Read on-disk captures and committed files only. A dispatch item is NOT an operator approval; if you judge a live read necessary, report it as a finding and do not perform it.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md before installing, official channels only, record tool/version/channel/reason in your report. pacman guard: all pacman transactions are PAUSED host-wide — never run pacman -S, -Sy, -Syu, -U or -R; use uv tool / npx / an official binary in ~/.local/bin, or report the need.
- Routing is the host role table (~/.omp/agent/config.yml task.agentModelOverrides; operator-owned, read-only). Never pass or hardcode a model.
- The planner seat is the L1 (the validator rejects `planner` as a swarm role); bounded planning data-walks ride scout and connector items.
- Never message agent://all. Your report records: the item you were given, every command you ran with its verbatim output (trim long output, keep the decisive lines), your verdict, and resolvable pointers (path:line, char offset, sha256). Never assert a result you did not run. Keep the report under 150 lines."""

GATE_HINT = (
    "The Gates table columns are: name | kind | entry | verdict map | self-test | pinned values | write scope | owner "
    f"(read the rows between `## Gates` and the next `## ` heading in {LANE}/SKILL.md and copy their conventions). "
    "Draft rows ONLY for the paths named in your item, one row per instrument family, each a single line starting with `| ` and ending with ` |`, "
    "exactly 8 cells, naming EVERY listed file by its full repo-relative path INSIDE THE ENTRY CELL (the round-47 counter reads the third cell only), "
    "a verdict-map cell stating each exit code (`exit 0` / `exit 1` / `exit 2`) and the exact PASS print values, the control that fails it in the "
    "self-test cell, the measured lane commit or receipt in pinned values, `read-only` or the receipt path it writes in write scope, and `chousa` as owner. "
    "If a script was superseded or is a probe that does not gate, say so in the verdict map. Run each listed script read-only once on a /tmp copy of the lane "
    "(`git -C " + LANE + " archive master | tar -x -C /tmp/...`; never in the lane) and paste output and exit code, so the row states observed values. "
    f"Then put your rows into a /tmp copy of SKILL.md and run `python3 {EV}/c2-count.py --root <tmp copy> --list` to show your paths leave UNREGISTERED. "
    "Put the rows verbatim in a fenced block in your report. Never invent a command you did not run."
)


def opener(name, sid, quotes, extra=""):
    return (name, "reviewer",
            f"Open lane source {sid} ({URLS[sid]}) this round from its capture {C[sid]} and locate the quotes that will ground its Registry row and the entry. "
            f"Candidate quotes from the staged entry and row: {quotes} "
            f"For EACH candidate: is it CONTIGUOUS and verbatim in the capture (PDF captures interleave two columns, break lines and hyphenate; HTML captures carry math markup such as `κ \\\\kappa`)? "
            f"Report its Python str.find char offset, occurrence count and 100 chars either side verbatim; if not contiguous, give the longest contiguous unique replacement slice of 4–25 words that carries the same fact, with its offset. "
            f"Deliver AT LEAST THREE contiguous unique quotes (each 4–25 words, each containing at least one 2+-word phrase a bullet can backtick) as a TSV block `id<TAB>offset<TAB>quote`, verified by `capture[offset:offset+len(quote)]==quote` in Python (paste the check). "
            f"Also report the capture's sha256 and char length, which staged sentences of {STAGED}/claim-support-test-r37.md and {STAGED}/claim-support-test-r37-amendment-2026-10-23.md this source supports, and any staged sentence it CONTRADICTS or overstates (quote both sides). {extra} No fetch.")


def quarantine(name, rid, sid, extra=""):
    return (name, "reviewer",
            f"Quarantine hand-check (§10) of absent-defect-register row `chousa` register {rid}: read that data row of {REG} (grep `| {rid} |`; the lane cell must be `chousa`), take every backticked quote in its quote cell, and hand-check each in the capture of its URL — lane id {sid}, capture {C[sid]}. "
            f"The register's `payload-absent` is a mechanical verdict; round 43 and round 46 found it false where a PDF interleaves columns or an HTML render inserts markup. For each register quote: normalise only whitespace, line breaks, column interleave, hyphen splits and `κ \\\\kappa`-style markup, and say whether every WORD of the quote occurs in order in the capture (present), some words are missing or changed (absent — fabrication class), or the capture cannot be read (unverifiable). Paste the capture slices that carry each part, with char offsets. "
            f"Then give the row's verdict as one line exactly of the form `- quarantine: register `{rid}` ({URLS[sid]}) verdict: `present|absent|unverifiable` — <one-sentence reason with offsets>`, and a contiguous unique anchor quote (4–25 words) you located, with offset. {extra} No fetch.")


ITEMS = [
    # --- C3 source opening (6 reviewers)
    opener("ReviewOpenS085", "S085",
           "`NOT ENOUGH INFO`; the evidence tuple `[Annotation ID, Evidence ID, null, null]`; the sentence saying SUPPORTS/REFUTES carry the sentence(s) forming the necessary evidence; `A list of evidence sets`.",
           "ALSO: the held S085 Registry row's anchor cell (grep `| S085 |` in " + LANE + "/corpus/SOURCES.md) says `char 2349`; the round-46 span manifest " + LANE + "/corpus/evidence/round46/spans.tsv records quote offsets as span-start + position. State the exact char offsets of `A list of evidence sets` and `Pre-processed Wikipedia Pages (June 2017 dump)` in the capture and draft a corrected anchor cell whose every `char N` is a quote's true offset."),
    opener("ReviewOpenS090", "S090",
           "Definition 1 `A set of sentences S provides supporting evidence for a claim c if, supposing the contents of S were true, it would give you greater reason to believe that c is true, all else equal`; Definition 2 (refuting); `If no sentences in the document provide evidence, do not select any sentences`; the abstract's ~22% / ~30% unsupported figures.",
           "State whether the paper's authors and venue (Findings of ACL 2026) are visible in the capture and whether its inter-annotator agreement is reported (the staged entry says it was not read)."),
    opener("ReviewOpenS091", "S091",
           "`CFEVER comprises 30,012 manually created claims based on content in Chinese Wikipedia`; `labeled as “Supports”, “Refutes”, or “Not Enough Info”`; `annotated with corresponding evidence sentences sourced from single or multiple pages in Chinese Wikipedia`.",
           "The capture is a two-column PDF with an interleaved example box; report which candidate is contiguous. State the venue/year printed in the capture (the staged row says AAAI 2021 — check it; the AAAI article id 29825 suggests a later volume)."),
    opener("ReviewOpenS092", "S092",
           "`If I was given only the selected sentences, do I have stronger reason to believe claim is true (supported) or stronger reason to believe the claim is false (refuted)`; `avoid applying your own world-knowledge`; `by annotators achieving 0.6841 in Fleiss`; the Skip / Not enough information instruction.",
           "This is the arXiv v3 HTML of the FEVER paper; the lane already holds the NAACL PDF as S086 (" + LANE + "/corpus/SOURCES.md). Confirm which of these quotes are ABSENT from the S086 capture " + QC + "/1c15b611118dee97e4105fcf.txt (grep each), i.e. whether a separate row is justified by content, and name the appendix section headings that carry them."),
    opener("ReviewOpenS093", "S093",
           "`1,535 real-world claims`; `7,675 annotated claim-evidence pairs` (or the capture's exact wording); the per-sentence SUPPORTS/REFUTES/NOT_ENOUGH_INFO labels and the claim-level `DISPUTED` label; an appendix D worked example.",
           "State whether the climate-fever per-label agreement figures are in the capture (the staged entry says they were outside the portion opened)."),
    opener("ReviewOpenS094", "S094",
           "`The Cohen’s Kappa (Cohen, 1960) score for interannotator agreement is 0.792`; `we re-assign labels based on the claim-relevant evidence gathered from open websites`; the sentence giving 202 NOT ENOUGH INFO claims relabelled.",
           "The capture is a two-column PDF; the register calls two of these quotes absent. Locate the fragments and the contiguous slices."),
    # --- C3 quarantine hand-checks (4 reviewers)
    quarantine("QuarReg093", "S093", "S090"),
    quarantine("QuarReg094", "S094", "S091"),
    quarantine("QuarReg108", "S108", "S092"),
    quarantine("QuarReg110", "S110", "S094"),
    # --- C3 drafting (scribes)
    ("ScribeEntryBase", "scribe",
     f"Draft the lane entry {LANE}/{BASE} by re-grounding the staged {STAGED}/claim-support-test-r37.md against the captures (open them yourself: S085 {C['S085']}, S090 {C['S090']}, S091 {C['S091']}). "
     f"Follow the shape of the lane's adopted entries {LANE}/corpus/knowledge/evidence-pool-versioning-r39.md (header lines `source: S0NN — <url> — <locator>`, `verified-at: 2026-10-25`, `recheck: 365d`, `ground:`; sections `#### Observation`, `#### Inference`, `#### Unknown`). "
     f"Rules: the three `source:` lines are S085 ({URLS['S085']}), S090 ({URLS['S090']}), S091 ({URLS['S091']}) and NO other S-id except lane ids S079–S094; every backticked phrase in an Inference bullet must be copied VERBATIM from a contiguous slice of a cited capture (the round-47 checker `{LANE}/tools/inference-ground.py` refuses a token not in a cited span and refuses a bullet whose own words flip a quoted phrase's polarity); every Inference bullet cites at least one S-id; figures of 3+ digits must appear in a cited capture. "
     f"Correct the staged text where the captures disagree (venue/year of CFEVER, the ~22%/~30% wording, the declared-null tuple) and drop what no capture carries; note that the lane now holds the FEVER NAACL paper as S086, so the staged 'the FEVER paper was retrievable only as an abstract' is stale. Link the lane's {LANE}/corpus/knowledge/claim-support-states-r24.md by path where it is relevant. Put the whole draft in a fenced block plus a list of every quote you used with its capture char offset (verified with Python str.find)."),
    ("ScribeEntryAmend", "scribe",
     f"Draft the lane entry {LANE}/{AMEND} by re-grounding the staged {STAGED}/claim-support-test-r37-amendment-2026-10-23.md against the captures (S092 {C['S092']}, S093 {C['S093']}, S094 {C['S094']}). Same shape and rules as the adopted {LANE}/corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md: `source:` lines S092 ({URLS['S092']}), S093 ({URLS['S093']}), S094 ({URLS['S094']}) only; no staged id (S113–S115) may remain anywhere in the text; the `ground:` line says it amends the lane's {BASE}. "
     f"Every backticked phrase in an Inference bullet must be VERBATIM from a contiguous slice of a cited capture; figures of 3+ digits must appear in a cited capture (0.6841, 0.792, 1,535, 7,675, 202 — check each and its exact wording); a bullet's own words must not flip the polarity of a phrase it quotes (e.g. quoting a negated phrase and then asserting its stem positively). "
     f"Correct the staged text where the captures disagree (e.g. whether 0.6841 is five-way or three-way Fleiss κ; whether climate-fever's DISPUTED is a claim-level label; what exactly CorFEVER relabelled and from which dataset). Put the whole draft in a fenced block plus a list of every quote used with capture char offset (verified with Python str.find)."),
    ("ScribeRows", "scribe",
     f"Draft the Registry rows for {LANE}/corpus/SOURCES.md: new rows S090–S094 (URLs {URLS['S090']}, {URLS['S091']}, {URLS['S092']}, {URLS['S093']}, {URLS['S094']}) and the UPDATED held row S085 (append `{BASE}` to its used-by, keep `corpus/knowledge/evidence-pool-versioning-r39.md`). "
     f"Schema: 11 columns `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` (read /home/vgpnk/Projects/shokunin/CORPUS.md section on SOURCES.md and the existing rows S085–S089). Start from the staged rows S098, S099, S113, S114, S115 in {PKG}/SOURCES.append.md but normalise: status `mined`, opened `2026-10-25`, recheck a valid `365d`-style cadence (put any stripped prose in a separate list), used-by exactly the citing lane entry ({BASE} for S090/S091; {AMEND} for S092–S094), no literal or escaped `|` in any cell, and the anchor cell naming each quote as `char N: <quote>` where N is the quote's TRUE Python str.find offset in the capture (S090 {C['S090']}, S091 {C['S091']}, S092 {C['S092']}, S093 {C['S093']}, S094 {C['S094']}, S085 {C['S085']}) — the round-47 counter checks every `char N` against the span manifest. "
     f"Check EACH drafted line has exactly 12 `|` (awk -F'|' 'NF!=13' reports nothing). Put the rows verbatim in a fenced block plus the stripped-prose list."),
    ("ScribeGateBlock", "scribe",
     f"Draft the `## Gate` section of {LANE}/corpus/lessons/round-47.md. Read {LANE}/corpus/lessons/round-46.md `## Gate` for the shape. Content: the one theme; the per-entry province and QUALITY bar check for the two admitted entries ({BASE}, {AMEND}); the id map by document (staged S097→S085, S098→S090, S099→S091, S113→S092, S114→S093, S115→S094) with the 8-id collision list from {LANE}/.ufo/waves/round-47/assimilation/collisions; the round-46 flip condition for the amendment and which parts are met. "
     f"REJECT at least one other entry of the assimilation set {STAGED}/ this round with reason + flip condition: judge `citation-count-semantics-r37.md` and `search-log-fields-r36.md` (is it generic? sibling-domain? already held — compare {LANE}/corpus/knowledge/search-log-method-r39.md and the round-43 refusal in {LANE}/corpus/lessons/round-43.md?) and pick the reject(s) with evidence pointers. Leave the per-row URL/access date/≤25-word quote list and the quarantine verdict lines as clearly marked slots (the source-opening seats fill them). Put the draft in a fenced block."),
    # --- C3 tooling
    ("ExecSpanBuilder", "executor",
     f"Write, in /tmp/chousa-r47-ExecSpanBuilder/, `build-spans.py` for round 47 by adapting {LANE}/corpus/evidence/round46/build-spans.py: input a TSV `{EV}/quotes.tsv` with columns `id url quote entry`; output {EV}/spans.tsv (7 tab columns id url capture_sha256 offset span_file quote entry) and {EV}/spans/<id>-<n>.txt, each span = capture[offset:offset+len] with ~80 chars of context either side, offset = span start, capture = sha256(url)[:24].txt under {QC}; refuse a quote that is absent or occurs more than once (exit 1 naming it); `--check` re-derives every row and prints `SPANS_ROWS=n STALE=k`. "
     f"Test it end to end on a /tmp tree with at least two quotes per id that YOU locate in the six captures (S085 {C['S085']}, S090 {C['S090']}, S091 {C['S091']}, S092 {C['S092']}, S093 {C['S093']}, S094 {C['S094']}) and run `python3 {EV}/c3-count.py --root <tmp tree>` to show which legs your spans satisfy (others fail for missing entries/rows). Paste the builder source in full and the test output. Do NOT write into the lane."),
    ("ExecMirrorCensus", "executor",
     f"Prepare the pre-append census mirror procedure: write /tmp/chousa-r47-ExecMirrorCensus/mirror.sh that copies {LANE}/corpus/ to a scratch dir, appends rows given in a file to the mirror's `## Registry` table (directly after the last S-row, no blank line — round-46 RevC3Rows F7), replaces the held S085 row with a given replacement, copies given entries in, and runs `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md`. Test it with five placeholder rows S090–S094 that you write in the 11-column schema (status mined, real URLs from the Context) and show the census exit code and any E03/E04/E11 lines; then test that a row duplicating S085's URL in-scope produces E04 (prove the gate can fail). Paste the script and both outputs."),
    # --- C1 falsifiers
    ("ReviewerC1Polarity", "reviewer",
     f"Code-review the polarity probe in {LANE}/tools/inference-ground.py (functions phrase_polarity, polarity_flips, count_keys, figure_flip and their call sites in main) against rule 5 of its docstring and the R47-C1 rule sentence in {EV}/claims.md. Check, with line numbers: window sizes (3 before / 2 after; 3 before for P2; 4 after for figures); the five-letter stem; STOP words; whether `unquoted()` removes S-ids and all quoted phrases; whether the first carrying span decides polarity when several spans carry the phrase; curly apostrophes in n't; whether a figure grounded by a span (not counts) skips P3; whether keys of mixed polarity decide nothing. Run the tool on all six fixtures of {FIX}/ and paste. Report every mismatch between code and sentence; do not edit."),
    ("CritC1Survivors", "critic",
     f"Build the strongest polarity-flip bodies the landed probe ACCEPTS, in /tmp/chousa-r47-CritC1Survivors/, using {FIX}/spans.tsv, spans/ and counts.json: (1) synonym/antonym flip of a different stem (`no revision is recorded` → 'every sentence is edited'); (2) the flip word 4+ words away from its negator; (3) double negation; (4) a flip in a SECOND bullet that quotes nothing; (5) a figure flip via `without` placed 5+ words after the numeral; (6) the round-46 strongest body `v7-strongest.md` from {LANE}/.ufo/waves/round-46/w2/CritC1D7.md §1 (re-create it; does it now exit 1, and on which code?). Run `python3 {LANE}/tools/inference-ground.py --entry <body> --spans {FIX}/spans.tsv --counts {FIX}/counts.json --root <dir>` on each; paste exits and findings. Then state the narrowest TRUE sentence of what the probe refuses, and whether SCORECARD/SKILL wording must say 'stem-sharing polarity flip', not 'entailment'."),
    ("MutC1Probe", "mutation-tester",
     f"Mutation-test the probe against the frozen counter: on /tmp copies of {LANE}/tools/inference-ground.py make one mutant each — (a) P1 disabled, (b) P2 disabled, (c) P3 disabled, (d) stem length 5→3, (e) P1 after-window 2→0, (f) is_neg ignores n't, (g) STOP emptied, (h) polarity read from the LAST carrying span. Score each with `python3 {EV}/c1-count.py --root {LANE} --tool <mutant>` and paste. A mutant that still prints C1=PASS is a survivor: say which fixture would kill it and whether that is a counter gap or a harmless equivalence."),
    ("ExecC1Regress", "executor",
     f"Regression sweep of the probe over the lane's real corpus: for every file in {LANE}/corpus/knowledge/*.md run BOTH the round-46 tool (`git -C {LANE} show 9a9f94db:tools/inference-ground.py > /tmp/chousa-r47-ExecC1Regress/ig46.py`) and the landed tool with `--spans {LANE}/corpus/evidence/round46/spans.tsv --counts /dev/null --registry {LANE}/corpus/SOURCES.md --root {LANE}`, and again with the round-45 manifests (`{LANE}/corpus/evidence/round45/spans.tsv`, `round45/counts.json`). Tabulate entries whose exit changed and every new INF_POLARITY_FLIP finding; for each, judge from the entry text whether it is a TRUE flip or a false positive (quote the bullet). Also run the round-46 counter `python3 {LANE}/corpus/evidence/round46/c1-count.py` and the round-47 counter, paste both."),
    ("LabC1FalsePos", "critic",
     f"Probe one hypothesis: 'the polarity probe refuses fewer than 1 in 5 correctly-reasoned bullets that discuss a negated span phrase'. In /tmp/chousa-r47-LabC1FalsePos/, write 10 short fixture entries in the shape of {FIX}/positive-negation-kept.md, each with one Inference bullet that QUOTES a phrase from {FIX}/spans/S901-1.txt or S902-1.txt and reasons CORRECTLY about it in natural academic English (vary: 'because no revision is recorded, revisions are untraceable', 'the record lacks any revision', 'revision history is absent', etc.). Run the landed tool on each (`--spans {FIX}/spans.tsv --counts {FIX}/counts.json`). Report the refusal count and each refused bullet with its finding; verdict on the hypothesis."),
    ("ScribeC1Rows", "scribe",
     f"Draft the round-47 text that describes the C1 capability, as fenced blocks: (a) the replacement SKILL.md `## Gates` row for `inference-ground` (read the current row in {LANE}/SKILL.md; add `INF_POLARITY_FLIP` and the missing `INF_NO_BULLETS` to the finding codes — round-46 `CritC1D7` §5; replace the stale sha256 pin with the current blob sha256 of {LANE}/tools/inference-ground.py and the commit `a15610a5`; self-test `python3 corpus/evidence/round47/c1-count.py`), keeping the entry cell's path; (b) a QUALITY.md criterion 67 in the style of criteria 64–66 of {LANE}/corpus/QUALITY.md: an Inference bullet must not assert the opposite polarity of a phrase it quotes; Check line; 'Shown able to fail' naming the three junk fixtures and the round-46 tool's 0/3; the named limit (stem-sharing only); (c) a SCORECARD capabilities row 'polarity probe in the inference check'. Run the tool and counter once to paste observed values."),
    # --- C2 rows and falsifiers
    ("ScribeGatesChecks", "scribe",
     f"Draft SKILL.md Gates rows for the QUALITY-named checks the round-47 counter adds: {LANE}/corpus/evidence/round29/prose-check.py, round30/rerun-check.py, round32/q33-check.py, round25-meta-oracle.py (all under {LANE}/corpus/evidence/). Read the QUALITY.md criterion that names each (grep the path) and each script's header to state the real entry, exit contract and write scope. " + GATE_HINT),
    ("ScribeGatesWaves", "scribe",
     f"Draft SKILL.md Gates rows for wave-control scripts the dependence/check-named legs reach: {LANE}/.ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh, {LANE}/.ufo/waves/round-34/w1/ExecE4Census/receipt-binding.py, {LANE}/.ufo/waves/round-35/repairs/slen-probe.sh, and {LANE}/tools/mechanism-witness.py. Find which file names each (grep the lane) and state whether it gates or is a historical probe. " + GATE_HINT),
    ("ScribeGatesMisplaced", "scribe",
     f"Under the round-47 entry-cell rule, nine paths are named in some Gates row but NOT in its entry cell: .ufo/waves/round-38/controls/base-gate-r38.sh, .ufo/waves/round-39/controls/base-gate-r39.sh, .ufo/waves/round-41/controls/base-gate-r41.sh, corpus/evidence/round26-date-differential.sh, round26-registry-differential.sh, round27-falsify-controls.py, round27-mechanisms.py, round27-regressions.py, round29/c1-count.py; and five more are unregistered: corpus/evidence/round24-measure.sh, round25-ledger-recount.py, round25-measure.sh, round25-meta-differential.sh, round26-measure.sh. Find the existing rows naming them in {LANE}/SKILL.md (quote line numbers) and draft CORRECTED replacement rows that move each path into the entry cell (keep the verdict map truthful; split a row if one entry cell would list unrelated instruments). " + GATE_HINT),
    ("ScribeGatesR47", "scribe",
     f"Draft SKILL.md Gates rows for this round's three counters {EV}/c1-count.py, c2-count.py, c3-count.py with the frozen targets from {EV}/claims.md and the controls in {EV}/controls/ (self-test cell). Run each once read-only and paste output and exit code (C2/C3 are expected to FAIL before landing — the row gives the frozen targets). " + GATE_HINT),
    ("ReviewerC2Set", "reviewer",
     f"Independently re-derive C2's set with YOUR OWN script (do not import either counter): legs A–C as the round-46 docstring of {LANE}/corpus/evidence/round46/c2-count.py defines them, D (every existing repo-relative *.py/*.sh literal inside an entry point's source, closed), E (every existing *.py/*.sh path in corpus/QUALITY.md or in SKILL.md outside `## Gates`). Compare set-for-set with `python3 {EV}/c2-count.py --root {LANE} --list` and the ENTRY_POINTS line; paste both and every difference. Check the docstring sentence against the code (e.g. does `./`-prefix handling match; does the closure read binary files; are paths in comments counted as dependence, and should they be?)."),
    ("MutC2Forge", "mutation-tester",
     f"Attack {EV}/c2-count.py with forges on /tmp copies of the lane (`--root`): (a) one junk 8-cell row whose entry cell lists all 25 unregistered paths and whose verdict cell says `exit 0`; (b) the same row with the paths in the 5th cell only; (c) a row inside a fenced block; (d) an HTML comment; (e) a Gates row naming a deleted path (does DANGLING fire?); (f) deleting corpus/evidence/round46/c2-count.py or changing one byte of it (does R46_INSTRUMENT refuse?); (g) deleting a QUALITY `Check:` path to push ENTRY_POINTS below FLOOR. Paste each output and exit. Name every forge that scores C2=PASS and say whether the claim's named limit covers it."),
    ("CritC2Framing", "critic",
     f"Attack C2 as a CALIBRATION claim: AXES.md (/home/vgpnk/Projects/shokunin/AXES.md) and the round prompt require a calibration claim to count mismatches between the lane's self-assessment and observed repo state. Is UNREGISTERED+DANGLING such a count, or plumbing dressed as calibration? Is the dependence leg real dependence (a path literal in a docstring or comment is not a call)? List executables under {LANE}/corpus/evidence/, {LANE}/tools/, {LANE}/.ufo/waves/ that a Gates row SHOULD carry but even the round-47 set misses (grep for `subprocess`, `bash `, `python3 ` invocations). Recommend the honest SCORECARD wording; do not edit."),
    # --- C3 critics / scouts
    ("CritC3Inference", "critic",
     f"Attack the staged inferences of {STAGED}/claim-support-test-r37.md and its amendment against the captures (S090 {C['S090']}, S092 {C['S092']}, S094 {C['S094']}): (1) 'support is defined as evidential strength, not entailment' — does PEOPLEPROFILES say 'not entailment', or is that the staged author's gloss?; (2) 'roughly a third of real citations do not support the claim' — what are the 22%/30% denominators (lead claims vs body claims vs cited sources)?; (3) 'NOT ENOUGH INFO is a statement about the evidence' — does CorFEVER's 202-claim relabelling show that, or show annotation error?; (4) 0.6841 'five-way' vs three labels. Quote both sides with offsets; give the narrowest true sentence for each."),
    ("ScoutProvinceFit", "scout",
     f"Province check for the two entries: read {LANE}/PROVINCE.md (chousa owns claim-vs-source verification; refuses model-quality or evaluation claims → kengaku). FEVER/CFEVER/climate-fever/CorFEVER are fact-verification DATASETS, often used to evaluate models. Judge each staged sentence-group of both staged entries: in province (the support test as a research-method rule a human or checker applies), or out (benchmark/model evaluation results)? Name sentences to drop. Also grep /home/vgpnk/Projects/shokunin/kengaku-shokunin/corpus/ for FEVER, CFEVER, climate-fever, CorFEVER, PEOPLEPROFILES and report hits."),
    ("ScoutCoverageGround", "scout",
     f"Coverage check: read {LANE}/corpus/README.md (coverage map and `## Frontier`) and {LANE}/corpus/knowledge/claim-support-states-r24.md, claim-verification-r2.md. Grep {LANE}/corpus/knowledge/ for 'support', 'NOT ENOUGH', 'Not Enough Info', 'refute', 'kappa', 'agreement'. Report what support-test ground the lane already holds (file:line) and what the two staged entries add that the map does not hold (expansion credit only on ground not held). Draft the coverage-map row(s) in the README's format."),
    ("ConnectSiblings", "connector",
     f"Sibling-overlap scan: grep every sibling lane corpus under /home/vgpnk/Projects/shokunin/*-shokunin/corpus/ (exclude chousa) for FEVER, CFEVER, climate-fever, CorFEVER, PEOPLEPROFILES, 'Not Enough Info', 'NOT ENOUGH INFO', 'Fleiss', 'Cohen'. Report each hit with lane and path:line and judge whether adopting this theme absorbs a sibling's held ground. Also check, as a bounded planning data-walk for the L1, whether the C1 polarity rule or C2 dependence registry duplicates a mechanism a sibling lane already holds (grep sibling tools/ for 'polarity', 'negat', 'Gates'). Report only; no edits."),
    # --- frontier / inherited / scope
    ("ExecReceiptSpot", "executor",
     f"considerthese proposal (operator-authored, {LANE}/considerthese/2026-10-24.md, 'Spot re-verify one receipt a week'): run the lane's newest receipt verifier read-only over a sample. Find the newest `verify-receipts.py` under {LANE}/corpus/evidence/round*/ (ls -t), read its usage, and run it on a /tmp `git archive master` copy of the lane over every receipt it accepts (or a sample of at least 5 receipts from different rounds). Paste the command, output and exit code, and name any receipt that no longer verifies. Then draft a QUALITY.md criterion 68 (style of criteria 64–66) that makes this a per-round check with a Check line and a 'Shown able to fail' (corrupt one receipt byte in /tmp and show the verifier fails)."),
    ("ScribeR46Defects", "scribe",
     f"Disposition of the round-46 closure's routed defects 1–6 ({LANE}/corpus/lessons/round-46-verifier-spotcheck.md §6). For defect 3 (stale C2 control receipts labelled with the pre-widening counter), re-run the forge scripts/forges described in {LANE}/corpus/evidence/round46/controls/c2-controls.txt against the FINAL round-46 counter on /tmp copies and draft a refreshed receipt text (header digest = sha256 of the committed {LANE}/corpus/evidence/round46/c2-count.py; honest count of refusal vs passing blocks). For each of defects 1–6 draft one table row `defect | disposition this round | evidence pointer` (C2 of round 47 addresses 2 and 4; C3 addresses 5; defect 6 is report wording). Put both in fenced blocks."),
    ("ScoutInheritedTree", "scout",
     f"Report `git -C {LANE} status --porcelain`, `git -C {LANE} diff --stat`, and the lane tip via `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state {LANE}`. Confirm the three modified JSON paths (.ufo/waves/round-40/w1/swarm-registry.json, round-41/w1/swarm-registry.json, corpus/evidence/round41/receipts/cells/cells.json) are the previously left-named ones (grep {LANE}/corpus/lessons/round-46.md and round-44.md) and name any untracked path. Check /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md for an operator answer to 8d77e6c1 and the chousa round-43/44 questions. Report only."),
    ("SentScopeAudit", "sentinel",
     f"Audit the round's new code for scope and egress: {LANE}/tools/inference-ground.py, {EV}/c1-count.py, c2-count.py (note: it imports and EXECUTES corpus/evidence/round46/c2-count.py after a sha256 check — is that safe under --root pointing at an untrusted tree?), c3-count.py (it runs tools/inference-ground.py from --root as a subprocess), and {EV}/controls/*.py. Grep for urllib, requests, socket, http.client, curl, wget, os.system, subprocess and every write path. Report each hit, whether it can egress or write outside its scope, and whether running a counter with --root on an attacker tree executes attacker code (and whether that matters for a closure re-run). Also run `git -C /home/vgpnk/Projects/shokunin status --porcelain` and name any untracked file whose content names chousa round 47 (a misroot)."),
]


def main():
    items = [{"name": n, "role": r, "item": DIRECTIVE + "\n\n" + t} for n, r, t in ITEMS]
    spec = {
        "wave": "chousa-r47-w1",
        "milestone": "Round 47 wave 1 (build + first falsifiers): open six sources, hand-check four quarantine rows, draft two entries, rows and Gate block, build spans, register gates, falsify the polarity probe and dependence registry; no fetch",
        "reportDir": ".ufo/waves/round-47/w1",
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
