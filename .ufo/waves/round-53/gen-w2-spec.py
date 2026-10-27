#!/usr/bin/env python3
"""Generate the round-53 wave-2 (falsify) spec. Writes w2-spec.json beside itself."""
import json
import pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
Q = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache"
P = "/home/vgpnk/Projects/shokuknow/merge/chousa"
EV = f"{L}/corpus/evidence/round53"
SCR = "/fast/scratch/hyaku/chousa-r53"
FREEZE = "a6ff732c70011f11c9beb681d832cedc6e75f566"
CAND = "32aab5edd70e43145cae72ec872278f3bc6efba7"
BASE = "5b550133d79bc09c82d8965cce2e48c2598b8c3e"
TIP = "f4343163b70ce20e6b6d4f52b39935156e8afb26"
E_STR = "corpus/knowledge/search-tracking-record-r40.md"
E_WIA = "corpus/knowledge/western-instrument-alignment-r50.md"
E_QCG = "corpus/knowledge/quality-control-guideline-issued-text-r48.md"
DOCS = {
    "S117": ("0ae65ac01b93119d3c2f3fed", "JMLA PRISMA 2020/PRISMA-S common-questions commentary (PDF; .txt = pdftotext -layout, two-column)", E_STR),
    "S118": ("16fe8487aa97b98576a0dbac", "the issued 药品临床综合评价质量控制指南（2024 年版 试行） (PDF)", f"{E_WIA} and {E_QCG}"),
    "S119": ("cfa080b4046592eb9490a82c", "the society's posting of the release notice (HTML .txt)", E_QCG),
    "S120": ("c9d1e74c3ac8d9eb332c9770", "Cochrane Handbook chapter 4 (HTML .txt)", E_WIA),
}

CONTEXT = f"""# Goal
chousa lane (deep-research method), round 53, wave 2 (FALSIFY). Wave 1 built and the L1 integrated at lane tip {TIP}. Two claims are FROZEN at {FREEZE} in {EV}/claims.md (read it and {EV}/claims-erratum.md E1–E6 first); never propose changing a predicate, target, counter or control. C1 (operability): adopter v4 `{L}/tools/assimilate-rows.py` (candidate {CAND}, unchanged since) — `twin` label, `HELD=`/`TWIN=` counts, recheck pre-pass, registry-first refusal also without --entry; frozen counter `python3 {EV}/c1-count.py` (target LEGS=8/8 on three unseeded runs and --seed 7) and the post-freeze `python3 {EV}/c1-supplement.py` (not the claim's rule). C2 (depth, sourced): three lane entries {E_STR}, {E_WIA}, {E_QCG} on four bound Registry rows S117–S120 of {L}/corpus/SOURCES.md (S118 is cited by two entries; staged S190, the NMPA 2019 notice print, is refused as a document — `refused-doc` line in {L}/corpus/lessons/round-53.md); 63 located quotes in {EV}/quotes.tsv → spans.tsv; frozen counter `python3 {EV}/c2-count.py` (now prints C2=PASS). Also landed: the CJK polarity window in {L}/tools/inference-ground.py with fixtures {L}/corpus/fixtures/inference-ground-cjk/ and `{EV}/cjk-polarity-check.py`; `{EV}/pointer-anchor-check.py` with anchored `correction:` lines at the end of {L}/SCORECARD.md; `{EV}/pdf-crosscheck.py`; `{EV}/weakness-streak.py` + recurring.tsv; QUALITY 91–96 at the end of {L}/corpus/QUALITY.md; SKILL.md Gates rows `assimilate-rows (v4, round 53)`, `chousa round-53 counters and checks`, `chousa round-53 post-freeze checks`; README section `Round53 coverage and frontier`. Your job: ATTACK one named item and report what survives. Every item names what it attacks.

# Boundaries (binding)
Lane repo: {L}. Your ONLY write is your own report file: every `Report:` trailer path is relative to {L} — write it at {L}/<that path>. Never write a production file, another seat's report, the git index, jj state, the fleet repo /home/vgpnk/Projects/shokunin (read only), any sibling lane, or /home/vgpnk/Projects/shokuknow (read-only; never run its campaign tools renumber-staged.py, merge-plan.py, quote-lint.py, absent-defect-register.py). Never run git commit/add/stash/checkout/reset/push or any mutating jj command anywhere except inside your own fixture repo. Scratch ONLY under {SCR}/<YourSeatName>/ (mkdir -p; export TMPDIR there; never /tmp; never a relative redirect such as `> out.txt` — every output path absolute under your scratch) and remove it before you finish (trap 'rm -rf -- "$S"' EXIT); copy any receipt you cite into your report first. Any git fixture repo: D=$(mktemp -d -p {SCR}/<YourSeatName>) && git -C "$D" init -q, every later git call names -C "$D", verify `git -C "$D" rev-parse --show-toplevel` equals $D before any commit. To test a changed lane copy, use `git -C {L} archive {TIP} | tar -x -C <scratch dir>` and run with --root / --tool there. No network and no live fetch (L0 `8d77e6c1` open): every source is an on-disk capture under {Q} (key = first 24 hex of sha256 of the URL). Code or text a seat drafts goes INSIDE its report (fenced blocks labelled with the intended lane path). Never message the orchestrator or other lanes' seats.

# Evidence
Ground every statement in a command you ran or a file:line/char offset you opened; paste commands with observed output. A check you did not run has not passed. ≤120 lines (≤220 when the item asks for a script or a draft). End with a one-line VERDICT naming what you attacked and whether it survived.

# Tooling
Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard: ALL pacman transactions are PAUSED host-wide (never -S/-Sy/-Syu/-U/-R, no downgrade, no service restart); use uv tool / npx / an official binary in ~/.local/bin instead (pypdf: `uv run --quiet --with pypdf python …`). Routing is host-owned; never pass a model."""

items = []


def add(name, role, text):
    items.append({"name": name, "role": role, "item": text})


# ---- executors (re-run every counter and check; runnable attacks)
add("R53W2ExecC1Target", "executor",
    f"Attack the C1 after-state: with TMPDIR={SCR}/R53W2ExecC1Target run `python3 {EV}/c1-count.py` three times unseeded, once `--seed 7`, once `--per-leg 10`, and once `--tool <BASE tool from git -C {L} show {BASE}:tools/assimilate-rows.py>`; paste the leg lines. Confirm the tool at the tip equals the candidate (`git -C {L} diff {CAND} {TIP} -- tools/assimilate-rows.py` empty; sha256). Does any run miss 8/8? Is the base still 1/8?")
add("R53W2ExecSupplement", "executor",
    f"Attack the post-freeze C1 supplement as evidence: run `python3 {EV}/c1-supplement.py` five times unseeded and with --seed 1..5 on the landed tool, and on `{EV}/controls/forge-c1.py` and the BASE tool (git show {BASE}:tools/assimilate-rows.py). Tabulate SUPPLEMENT_LEGS per run. Any flake? Does CALENDAR ever draw a date the tool's `valid_date` considers valid (print each drawn date and `datetime.date.fromisoformat` result)? Does REAL_PERTURBED depend on the campaign package bytes (what if SOURCES.append.md were edited — it is read-only, so reason from code)?")
for sid, (key, what, ent) in DOCS.items():
    add(f"R53W2ExecQuotes{sid}", "executor",
        f"Re-open {sid} ({what}), capture {Q}/{key}.txt (raw {key}.raw), cited by {ent}. For EVERY row of {EV}/quotes.tsv with id {sid}: count it in the .txt (must be 1), confirm it lies on one line, ≤25 words, ≤160 chars, that its offset equals the `char N` the entry/row/lesson state for it (grep the entry's source line and the S-row anchor cell in {L}/corpus/SOURCES.md and the lesson table in {L}/corpus/lessons/round-53.md), and that the span file under {EV}/spans/ is the exact slice of the .txt at the manifest offset. For PDFs also check each quote (whitespace removed) occurs in an independent pypdf extraction. Then read each sentence of the entry that cites {sid} and mark: supported / narrower-than-text / overstated / unsupported, quoting the capture. Table + defects.")
add("R53W2ExecC2Rerun", "executor",
    f"Attack the C2 after-state: with TMPDIR={SCR}/R53W2ExecC2Rerun run at the tip `python3 {EV}/c2-count.py`, `--lane-only`, `python3 {EV}/build-spans.py --check`, `python3 {L}/corpus/evidence/round51/quote-substance-check.py {EV}/spans.tsv`, and `python3 {EV}/controls/build-c2-controls.py` (both controls must still FAIL). Then export the tip to scratch and run c2-count with --root on it after replacing tools/inference-ground.py by the base version (`git -C {L} show {BASE}:tools/inference-ground.py`) — erratum E4 says 3/3 either way. Paste every line.")
add("R53W2ExecPdfGlue", "executor",
    f"Attack the claim that no PDF quote is a two-column glue: run `uv run --quiet --with pypdf python {EV}/pdf-crosscheck.py` from {L}. Then build the strongest counter-test: for S117 ({Q}/0ae65ac01b93119d3c2f3fed.txt) list every quote of {EV}/quotes.tsv whose line in the .txt also carries a second column block (split at ≥5 spaces) and check whether the quote crosses blocks; also check reading order — a quote can be in pypdf text yet be two half-sentences from different columns that happen to be adjacent in pypdf too (compare with `pdftotext` without -layout, `/usr/bin/pdftotext -raw`). Report any quote whose meaning depends on an interleave.")
add("R53W2ExecQualityChecks", "executor",
    f"Attack QUALITY 91–96 at the end of {L}/corpus/QUALITY.md: for each criterion run its stated check command and its stated 'shown able to fail' command exactly as written (TMPDIR={SCR}/R53W2ExecQualityChecks; use an exported tip copy for any mutation). Table: criterion · check output · red-before output · matches the criterion's text? Flag any claim in a criterion that you could not reproduce, any check that cannot fail, and any pointer that does not resolve.")
add("R53W2ExecCensusMisroot", "executor",
    f"Round-end conformance probes: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` (exit, every line); the CORPUS.md awk NF check on S117–S120 (`awk -F'|' '/^\\| S11[7-9] |^\\| S120 /{{print NF}}' {L}/corpus/SOURCES.md`); `git -C /home/vgpnk/Projects/shokunin status --porcelain` and `git -C {L} status --porcelain` — list every untracked file and say which (if any) a round-53 seat wrote (grep its content for 'R53' / 'round 53'); never move or delete anything. Also: any file under {SCR}/ older than 45 minutes left by a W1 seat (`find {SCR} -maxdepth 1 -mmin +45`)?")
add("R53W2ExecCjkSweep", "executor",
    f"False-refusal sweep of the landed CJK polarity window: for EVERY corpus/knowledge entry in {L} that has a round spans manifest (`grep -l` the entry path in {L}/corpus/evidence/round*/spans.tsv), run the tip `tools/inference-ground.py --entry <e> --spans <that manifest> --counts /dev/null --registry {L}/corpus/SOURCES.md --root {L} --quiet` and the base tool (git show {BASE}:tools/inference-ground.py) the same way; tabulate exit codes and findings; any entry the tip flags that the base passed is a regression — print the finding and judge it (true reversal or false refusal). Also run `python3 {EV}/cjk-polarity-check.py` and the round-46/47/48 inference-ground counters (`python3 {L}/corpus/evidence/round46/c1-count.py`, round47/c1-count.py, round48/precision-count.py).")
add("R53W2ExecAnchorForge", "executor",
    f"Attack `{EV}/pointer-anchor-check.py` (round-52 closure routed 4): on an exported tip copy, write correction lines that PASS it while pointing at the wrong place (an anchor that occurs exactly once in the target but belongs to unrelated content; an anchor in a directory pool; a later line superseding a good one with a bad one) and lines that should pass but FAIL (an anchor containing `\"`; Unicode dashes). Report each with output, and whether the seven anchored lines at the end of {L}/SCORECARD.md are content-true (open each target at the anchor and say whether it shows what the corrected pointer meant).")
add("R53W2ExecStreak", "executor",
    f"Attack `{EV}/weakness-streak.py` and `{EV}/recurring.tsv` (considerthese 2026-10-26 proposal 2): run it; then mutants on an exported tip copy — claimed 5→4, routed path removed, a round-54 lesson stub naming nothing, a lesson that mentions 'forge' only in praise. Does the tool fail when it should and pass when it should? Is RW-1's regex too loose (count matches per round in {L}/corpus/lessons/round-4[5-9]*.md and round-5*.md)? Report the matrix and one concrete improvement.")
add("R53W2ExecHistCounters", "executor",
    f"Regression sweep at the tip {TIP}: with TMPDIR={SCR}/R53W2ExecHistCounters run `python3 {L}/corpus/evidence/round47/c2-count.py --list` (SKILL registry), `python3 {L}/corpus/evidence/round51/c3-count.py`, `python3 {L}/corpus/evidence/round52/verdict-gap.py --from 40 --to 52`, `python3 {L}/corpus/evidence/round52/c2-count.py`, `python3 {L}/corpus/evidence/round51/c2-count.py`, `python3 {L}/corpus/evidence/round51/c1-count.py`, `python3 {L}/tools/assimilate-rows.py --selftest`, and `bash {L}/tools/research-gate.sh selftest` if it has one (read its usage). Compare with the base {BASE} (export it). Any count that changed: intended (new rows/tool) or regression?")

# ---- scribes
add("R53W2DraftScorecard", "scribe",
    f"Draft the append-only SCORECARD.md section `## Round 53 verdict — 2026-10-26 (adopter v4; search-record instruments by document)` in the exact shape of the `## Round 52 verdict` section of {L}/SCORECARD.md (read it: intro paragraph, claim table with before→after/command/verdict/tag, axis table, capabilities table, `## Planned — round 54 (not started)`). Use only measured values from {EV}/controls/c1-before.txt, c2-before.txt, c2-controls.txt, the counters run by you at the tip (TMPDIR={SCR}/R53W2DraftScorecard), and claims-erratum E1–E6. State honestly that the frozen C1 counter is forgeable (W1 R53CritForgeC1, supplement 3/3 vs forge 1/3). Planned round 54: theme C (GB/T 7714 source-type, W1 R53ScoutNextThemes) or B; the counter refusing per-leg<1; OLE .doc text form. Output one fenced block labelled SCORECARD.md.")
add("R53W2DraftLog", "scribe",
    f"Draft the append-only LOG.md entry `## Round 53 — …` in the shape of the Round 52 entry at the end of {L}/LOG.md (read it): evidence that motivated the round (round-52 closure routed items, SCORECARD planned row), C1, C2, frontier step (rows 116→120, census, mistakes, considerthese pick weakness-streak), routed fixes landed (CJK polarity, anchored corrections, erratum ranges), not landed/named, waves (W1 49 seats; W2 count from the spec). Use lane commit hashes from `git -C {L} log --oneline {BASE}..{TIP}`. Output one fenced block labelled LOG.md.")
add("R53W2DraftReportSections", "scribe",
    f"Draft the fleet report sections `## Sources & frontier` and `## Trend verdicts` for round 53 in the shape of /home/vgpnk/Projects/shokunin/.ufo/reports/round-52/chousa.md (read it). Sources: census start {EV}/census-start.txt and end (run it), rows before→after with the grep count command at base and tip (`git -C {L} show {BASE}:corpus/SOURCES.md | grep -cE …`), added by tier, rows touched old→new (none expected — verify with `git -C {L} diff {BASE} {TIP} -- corpus/SOURCES.md | grep '^-|'`), assimilation line (theme, collision count, renumber map, admits/refuses, quarantine), considerthese line, open L0. Trend verdicts expansion/quality/discernment with evidence; discernment stays 'unchanged pending closure'. Output fenced blocks.")
add("R53W2DraftWaveLimits", "scribe",
    f"Draft the round-53 lesson section `## Wave-2 limits recorded (not fixed this round)` in the shape of the same section in {L}/corpus/lessons/round-52.md. Read every finished wave-1 report in {L}/.ufo/waves/round-53/w1/ for findings the L1 did NOT fix (named limits: adopter symlink write escape and --out==--knowledge input loss from R53SentCounters; c2-count F2/F3 from R53ReviewC2Counter; quarantine verdict contradictions S104/S114/S077 from R53ExecQuarantine; CJK window limits; the forge's surviving routes) and list each with pointer and flip. Verify each pointer exists (grep). Output one fenced block labelled corpus/lessons/round-53.md.")

# ---- sentinel / simplifier
add("R53W2SentNewScripts", "sentinel",
    f"Hazard review of the round's NEW post-freeze scripts and the patched tool: {EV}/c1-supplement.py, pdf-crosscheck.py, cjk-polarity-check.py, pointer-anchor-check.py, weakness-streak.py, and the CJK window in {L}/tools/inference-ground.py (`git -C {L} diff {BASE} {TIP} -- tools/inference-ground.py`). Every write path (hardcoded /tmp? lane writes? rmtree scope), TMPDIR honoured, cleanup on SIGINT, regex catastrophic backtracking on a 1 MB entry line for the CJK window (time it), path traversal in pointer-anchor-check targets (`correction: x:1 p -> ../../etc/passwd anchor: …` — does it read outside the lane?). Severity and fix per hazard.")
add("R53W2SimplifyRound", "simplifier",
    f"YAGNI review of what round 53 landed after the freeze: {EV}/c1-supplement.py (three legs), {EV}/cjk-polarity-check.py, {EV}/weakness-streak.py, the CJK diff in tools/inference-ground.py. Name any branch, flag or leg no fixture or receipt exercises and that could be deleted without changing any printed result — prove by deleting in a scratch copy and re-running. Do not edit the lane.")

# ---- critics
add("R53W2CritForgeSupplement", "critic",
    f"Attack the post-freeze C1 supplement {EV}/c1-supplement.py: write the cheapest tool (in {SCR}/R53W2CritForgeSupplement) that passes BOTH `c1-count.py` 8/8 and `c1-supplement.py` 3/3 without implementing the adopter's full contract (e.g. extend {EV}/controls/forge-c1.py with a real calendar check and a real self-test runner, or key on the supplement's `example.org`/`example.net`/`example.com` hosts or its `n<hex>.md` names). Paste the forge and outputs, or list each shortcut and the leg that refused it.")
add("R53W2CritC1Verdict", "critic",
    f"Attack the C1 verdict the lane will claim ('improved narrowly', operability, capability extension): is v4 a behaviour change any lane workflow uses (does the round's own C2 adoption depend on the twin label — read the lesson Gate's collision paragraph), or a relabel? Is the frozen predicate met on the landed tool for inputs the counter never generates (cadence rechecks, erratum E3; a staged row cited by an entry that is refused)? Would a do-nothing control meet the target (controls in {EV}/controls/c1-before.txt)? Verdict with evidence: improved / improved narrowly / unchanged / harmed.")
add("R53W2CritForgeC2", "critic",
    f"Attack C2 at the tip: on an exported tip copy, find the cheapest lane edits that keep `c2-count.py --root <copy>` at C2=PASS while making an entry false (swap two quotes' bullets; negate an English bullet that quotes a phrase; replace a CJK bullet's claim while keeping its quote; drop an entry's Unknown sweep). Which edits pass? This measures what C2 does NOT certify; list what the closure must read by hand.")
add("R53W2CritEntailStr", "critic",
    f"Entailment attack on {L}/{E_STR} against S117 ({Q}/0ae65ac01b93119d3c2f3fed.txt; read the surrounding paragraphs, not just the quotes; the .txt is two-column, so read the PDF text via `uv run --quiet --with pypdf python` if the order is unclear). For every Observation and Inference sentence: supported / narrower / overstated / unsupported, with the capture text that decides it. Especially: 'a tracking record is routed', 'makes a sweep re-runnable', 'per-source rows are the record', and the Column 2 / Column 1 allocation. Give the narrowed sentence for each defect.")
add("R53W2CritEntailWia", "critic",
    f"Entailment attack on {L}/{E_WIA} against S120 ({Q}/c9d1e74c3ac8d9eb332c9770.txt) and S118 ({Q}/16fe8487aa97b98576a0dbac.txt). For every sentence: supported / narrower / overstated / unsupported. Especially: is 'the reporting aligns with … PRISMA' one item of a list of librarian services (read §4.2.1's list) — does the entry say whose obligation it is? Is 指标 4 at char 18046 in the 文献研究 indicator row (check the table structure around it; the guideline has several 指标 4)? 'nothing in the guideline asserts an alignment of its own' — sweep. Give narrowed sentences.")
add("R53W2CritEntailQcg", "critic",
    f"Entailment attack on {L}/{E_QCG} against S118 ({Q}/16fe8487aa97b98576a0dbac.txt) and S119 ({Q}/cfa080b4046592eb9490a82c.txt and its .raw HTML). For every sentence: supported / narrower / overstated / unsupported. Especially: 'posted day and signed day differ and the page does not reconcile them'; 'the text cannot date itself'; 'the two carriers spell the title differently'; 'the instrument … lists the strategy as a required annex'; '检索日期 0 times'. Give narrowed sentences.")
add("R53W2CritRefuseS190", "critic",
    f"Attack the refusal of staged S190 (the pharmwyp print of the 2019 NMPA notice, {Q}/0435b64f65c3ea7ddc6bb92e.txt) in {L}/corpus/lessons/round-53.md (Gate decisions and the refused-doc line). W1 `R53ReviewProvince` said register it tier C; W1 `R53CritNegatives` found it names PRISMA (char ~7797) which contradicts the staged Wia title. Is the refusal the decisive reason (QUALITY 93)? Does the admitted Wia entry now say anything the NMPA print contradicts? Was a document refused to make C2 easier (it does not need S190: BOUND 4/5 ≥3)? Verdict: refusal right / wrong / right-for-wrong-reason.")
add("R53W2CritCredit", "critic",
    f"Attack the expansion credit: the README `Round53 coverage and frontier` section in {L}/corpus/README.md claims four documents of credit (S117–S120). Is S119 (a release-notice posting) a document with its own ground or a carrier stamp of S118? Is S120 (Cochrane ch.4) new when the lane already cites other Cochrane Handbook chapters (`git -C {L} grep -n 'Cochrane Handbook' {BASE} -- corpus/knowledge corpus/SOURCES.md`) and staged S083 is the same chapter at another host? Verdict per document: credit / no credit, with pointers.")
add("R53W2CritMistakes", "critic",
    f"Attack `## Mistakes` in {L}/corpus/lessons/round-53.md (six rows): for each row, is the class right, does the evidence pointer resolve (open it), is 'captured-by' honest, and is the fix shown able to fail by a command you can run (run it)? A fix that cannot fail does not count. Also: is any round-53 mistake missing (e.g. the wave context named planned ids S117–S121 that changed to S117–S120; a seat-drafted README assumed S120=NMPA)?")
add("R53W2CritTrends", "critic",
    f"Attack the round's trend verdicts before they are filed: expansion (four documents, a capability), quality (narrowing on adoption, routed fixes landed), discernment (unchanged pending closure). Read the lesson, README section, SCORECARD tail and the W1 reports of R53CritTheme, R53CritNegatives, R53ReviewProvince. For each trend: the strongest argument it is overstated, and the verdict you would give with evidence.")

# ---- reviewers
add("R53W2ReviewSupplement", "reviewer",
    f"Review {EV}/c1-supplement.py line by line against its docstring and claims-erratum E1: CALENDAR's date draws (are all of them calendar-invalid? any day-32 month a tool might accept by lexical check?), the leap-year control, REAL_PERTURBED's expected map (staged order preserved? twin last?), SELFTEST_RAN's dropped-finding logic when the dropped finding occurs twice. Defects with reproducing commands (scratch {SCR}/R53W2ReviewSupplement).")
add("R53W2ReviewRows", "reviewer",
    f"Review Registry rows S117–S120 in {L}/corpus/SOURCES.md against CORPUS.md's SOURCES.md contract (/home/vgpnk/Projects/shokunin/CORPUS.md): 11 cells, kind/tier enums, tier justification (S118/S119 tier B society carriers; S117 tier A publisher PDF; S120 tier A), anchor cells (every `char N` is a quote offset in {EV}/spans.tsv — compute offset+span.find(quote)), teaches cells entailed by the captures, used-by exact, recheck valid. Also the lesson's re-opened-sources table (≤25-word located quote per new row, access date). Defects per cell.")
add("R53W2ReviewCjkPatch", "reviewer",
    f"Review the CJK polarity diff `git -C {L} diff {BASE} {TIP} -- tools/inference-ground.py` line by line: negator lists, the six-character clause-bounded window, interaction with the Latin path, the docstring's named limits, and the fixtures {L}/corpus/fixtures/inference-ground-cjk/ (do the positives really exercise a near-miss; is S901 reused across three fixtures a problem for the spans manifest's entry column?). Defects with reproducing commands; name one false-refusal shape you can build and run it.")
add("R53W2ReviewCorrections", "reviewer",
    f"Review the seven anchored `correction:` lines at the end of {L}/SCORECARD.md and the erratum-range corrections: does each correct what the round-52 closure section 6 item 1 and the round-51 closure item 4 asked ({L}/corpus/lessons/round-52-verifier-spotcheck.md, round-51-verifier-spotcheck.md)? Is SKILL.md:133 really the round-51 erratum range site (open it)? Is any other stale erratum range left in the lane (`grep -rn 'E1–E[0-9]\\|E1-E[0-9]' {L}/SCORECARD.md {L}/SKILL.md {L}/LOG.md {L}/corpus/lessons` and compare with each erratum's real range)? Defects.")
add("R53W2ReviewSkillReadme", "reviewer",
    f"Review the three new SKILL.md Gates rows (grep -n 'round 53\\|round-53' {L}/SKILL.md) and the README section `Round53 coverage and frontier`: every command runs as written from {L} (run each with TMPDIR={SCR}/R53W2ReviewSkillReadme), every pinned value matches the file (REAL_PIN, R50_PIN, FIXTURES_SHA256 9822ad59…), every claim in the README rows matches the entries (open them). Defects with output.")

# ---- mutation testers
add("R53W2MutSupplement", "mutation-tester",
    f"Mutation-test the adopter through {EV}/c1-supplement.py: copy {L}/tools/assimilate-rows.py to {SCR}/R53W2MutSupplement/ and mutate (1) valid_date → lexical regex only; (2) leap-year handling broken (Feb 29 always invalid); (3) selftest prints PASS without comparing; (4) selftest ignores missing findings; (5) twin label on the perturbed package only when ids < 200; (6) registry max read from the first row not the max. Run the supplement (and the frozen counter) per mutant; kill matrix; survivors with the leg that would kill them.")
add("R53W2MutCjkCheck", "mutation-tester",
    f"Mutation-test the CJK window through {EV}/cjk-polarity-check.py: copy {L}/tools/inference-ground.py to scratch {SCR}/R53W2MutCjkCheck and mutate (1) window 6→1; (2) drop 未 from the negators; (3) drop the span-negated direction; (4) ignore clause boundaries; (5) post-negators removed; (6) flip only when the negator is adjacent. Run `python3 {EV}/cjk-polarity-check.py --tool <mutant>` per mutant; kill matrix; survivors with the fixture that would kill them.")
add("R53W2MutPdfCrosscheck", "mutation-tester",
    f"Mutation-test {EV}/pdf-crosscheck.py: on a scratch copy of {EV} (quotes.tsv), plant (1) a quote glued across the two JMLA columns from one .txt line; (2) a quote with one changed character; (3) a quote that exists only in the .txt header/footer; (4) a quote from S118 with a CJK wrap joined. Does the check fail each? It reads quotes.tsv beside itself — run the copy from its own directory. Kill matrix and survivors.")

# ---- connectors / scout
add("R53W2ConnSiblingsFinal", "connector",
    "Final sibling-overlap scan for what round 53 LANDED: grep the sibling lanes under /home/vgpnk/Projects/shokunin/*-shokunin/ (corpus/, tools/, SKILL.md, PROVINCE.md; read-only; skip chousa-shokunin) for tracking record, PRISMA-S, information specialist, 质量控制指南, 药品临床综合评价, bjhea, inference-ground, polarity, CJK negat, pointer anchor, correction:. Verdict: overlap / no overlap for each landed surface, closest sibling file named.")
add("R53W2ConnPattern", "connector",
    f"Cross-claim pattern after integration: the round's C1 (twin label: two staged ids, one document) and C2 (S118 cited by two entries through those twins) meet in one registry row. (1) Does any OTHER lane row carry two staged ids of one document without a twin record (`grep -rn 'twin' {L}/corpus/lessons/round-4*.md {L}/corpus/lessons/round-5*.md`; the round-52 S113/S133 case)? (2) Is the 'forgeable frozen counter' streak (RW-1, 5 rounds) a pattern the lane should answer structurally (e.g. counters that call the tool on held-out real packages) — propose one concrete design with a pointer to where it would live. (3) One recommendation for round 54.")
add("R53W2ScoutFrontier", "scout",
    f"Coverage and frontier check after integration: read {L}/corpus/README.md `## Frontier` items and the new `Round53 coverage and frontier` section; for each 'Advanced' and 'Left open' bullet, say whether the landed entries support it (path:line) and whether the base already held it (`git -C {L} grep -n … {BASE} -- corpus/knowledge`). Also list which frontier items from round 52's README section this round moved or did not move.")

add("R53W2ExecZeroCases", "executor",
    f"Red-team the frozen C1 `--per-leg K` interface in {EV}/c1-count.py (W1 `R53SentCounters` H1): reproduce `--per-leg 0` and `--per-leg -3`, count generated case lines, then probe values `1`, `-1`, `2`, and an invalid non-integer; run with `--seed 53` and TMPDIR={SCR}/R53W2ExecZeroCases. Against the landed tool, tabulate exit, LEGS, case lines, and whether each generated leg actually ran. Read claims.md: does the frozen kill rule explicitly exclude a vacuous sample size? Do not edit the counter.")
add("R53W2ExecAdopterBoundary", "executor",
    f"Reproduce the new C1 named limits from W1 `R53SentCounters` H3–H5 against the landed adopter, without writing to the lane: in scratch {SCR}/R53W2ExecAdopterBoundary create (1) a safe package whose `--out` is the same directory as `--knowledge`, and record whether it destroys the entry; (2) a package whose `--out` contains a symlink named as a valid `--entry` pointing outside the scratch root, and record the target's before/after digest; (3) a cited row with a 200,000-character symbolic recheck and measure time/RSS; (4) a cadence-only `quarterly` recheck. Use `timeout`, `ulimit` if appropriate; never point a fixture at a real file. Table command, rc, writes and consequence against the frozen predicate.")

spec = {
    "wave": "chousa-r53-w2",
    "milestone": "Round 53 falsify: re-run every counter and check, re-open every quote, attack entailment, forge the counters and the supplement, review rows, patches and corrections, and draft the verdict sections",
    "reportDir": ".ufo/waves/round-53/w2",
    "axes": ["operability", "depth"],
    "context": CONTEXT,
    "items": items,
}
out = pathlib.Path(__file__).with_name("w2-spec.json")
out.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
c = Counter(i["role"] for i in items)
print(len(items), dict(c))
flash = c["executor"] + c["scribe"] + c["simplifier"] + c["sentinel"] + c["revenger"]
attack = c["reviewer"] + c["critic"] + c["mutation-tester"] + c["sentinel"]
print(f"flash-share={flash/len(items):.2f} attack-share={attack/len(items):.2f}")
names = [i["name"] for i in items]
print("NAME_COLLISIONS=%d" % (len(names) - len(set(names))))
