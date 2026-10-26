#!/usr/bin/env python3
"""Generate the round-52 wave-2 (falsify) spec. Writes w2-spec.json beside itself."""
import hashlib
import json
import pathlib
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
Q = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache"
P = "/home/vgpnk/Projects/shokuknow/merge/chousa"
EV = f"{L}/corpus/evidence/round52"
SCR = "/fast/scratch/hyaku/chousa-r52"
FREEZE = "37468eadd8d098e80289b2f31a22de3872d4a1f6"
CAND = "804a45370dc992bfe714817281535055c2f9b032"
TIP = "e769c03738d08c36109556ebf301a1db0dcf143d"
BASE = "00f8c7f5272a1d98b6d34913985fa4537e00aaf9"
URL = {
    "S113": "https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3",
    "S114": "https://www.chinagp.net/CN/column/item185.shtml",
    "S115": "https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx",
    "S116": "https://web.archive.org/web/2024/https://www.lifescience.co.jp/yk/jpt_online/prisma/list_1.pdf",
}
ENT = {
    "Niph": "corpus/knowledge/japanese-search-record-niph-form-r52.md",
    "Jpw": "corpus/knowledge/japanese-prisma-item-wording-r40.md",
    "Zhr": "corpus/knowledge/chinese-prisma-s-reception-r52.md",
}


def key(u):
    return hashlib.sha256(u.encode()).hexdigest()[:24]


def cap(sid):
    form = f"python3 {L}/tools/capture-text.py {Q}/{key(URL[sid])}.raw" if sid == "S115" else f"{Q}/{key(URL[sid])}.txt read as UTF-8"
    return f"{form} (key {key(URL[sid])}), URL {URL[sid]}"


CONTEXT = f"""# Goal
chousa lane (deep-research method), round 52, wave 2 (falsify). Wave 1 built; the L1 integrated and landed lane commit {TIP} (base {BASE}, freeze {FREEZE}, C1 candidate {CAND}). Every item below ATTACKS one thing wave 1 produced or the L1 landed; name what you attacked and the result. Claims are FROZEN in {EV}/claims.md (never propose changing a predicate, counter, control or target); post-freeze changes are disclosed in {EV}/claims-erratum.md E1-E4. C1 (operability, capability): `python3 {L}/tools/capture-text.py RAW [--locate QUOTE]` — the OOXML .docx text form; frozen counter `python3 {EV}/c1-count.py` (9 legs), post-freeze supplement `python3 {EV}/c1-supplement.py` (4 legs: re-spelled XML + pinned NIPH text digest). C2 (depth, sourced): three lane entries {L}/{ENT['Niph']}, {L}/{ENT['Jpw']}, {L}/{ENT['Zhr']} on four new Registry rows S113 (梅斯医学 portal record), S114 (中国全科医学 checklist page), S115 (NIPH .docx, read through capture-text), S116 (archived Japanese PRISMA 2020 table) in {L}/corpus/SOURCES.md; counter `python3 {EV}/c2-count.py`; manifest {EV}/spans.tsv built by {EV}/build-spans.py from {EV}/quotes.tsv. Lesson {L}/corpus/lessons/round-52.md (Mistakes, Spot-check intake, Gate, quarantine verdict, considerthese, located quotes, census); QUALITY.md criteria 87-90; README block `## Round52 coverage and frontier`; SKILL.md Gates rows `capture-text` and `chousa round-52 counters and checks`; considerthese pick {EV}/verdict-gap.py. Wave-1 reports: {L}/.ufo/waves/round-52/w1/<Name>.md. Captures are read-only under {Q}/ (key = sha256(url)[:24]); the staged package is read-only at {P}.

# Boundaries (binding)
Lane repo: {L}. Your ONLY write is your own report file: every `Report:` trailer path is relative to {L} — write it at {L}/<that path> (an absolute path). FIRST run `mkdir -p {SCR}/<YourSeatName> && cd {SCR}/<YourSeatName>` and stay there: never redirect or write to a relative path from any other directory (a wave-1 seat left `p.out`/`p.err` at the fleet root). Never write a production file, another seat's report, the git index, jj state, the fleet repo /home/vgpnk/Projects/shokunin (read only), any sibling lane, or /home/vgpnk/Projects/shokuknow (read-only; never run its campaign tools renumber-staged.py, merge-plan.py, quote-lint.py, absent-defect-register.py). Never run git commit/add/stash/checkout/reset/push or any mutating jj command except inside your own fixture repo. Scratch ONLY under {SCR}/<YourSeatName>/ (export TMPDIR there; never /tmp) and remove it before you finish (trap 'rm -rf -- "$S"' EXIT); copy any receipt you cite into your report first. Any git fixture or clone: create it under your scratch (`git clone -q --shared {L} $S/clone`), every later git call names -C on it. Never run `build-spans.py` without `--check` against the lane root (it writes spans); in a scratch copy pass `--root`. No network and no live source fetch (L0 `8d77e6c1` is open). Code or text you draft goes INSIDE your report (fenced blocks, labelled with the intended lane path); the L1 integrates. Never message the orchestrator or other lanes' seats.

# Evidence
Ground every statement in a command you ran or a file:line/char offset you opened; paste commands with observed output. A check you did not run has not passed. ≤120 lines (≤200 for a draft). A located quote is ≤25 whitespace words, occurs exactly once in its stated text form, with its character offset. End with a one-line VERDICT naming what you attacked and the result.

# Tooling
Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard: ALL pacman transactions are PAUSED host-wide (never -S/-Sy/-Syu/-U/-R); use uv tool / npx / an official binary in ~/.local/bin instead. No install is expected. Routing is host-owned; never pass a model."""

items = []


def add(name, role, text):
    items.append({"name": "R52W2" + name, "role": role, "item": text})


# ---- the four new registry rows
for sid in URL:
    ent = {"S113": "Zhr", "S114": "Zhr", "S115": "Niph", "S116": "Jpw"}[sid]
    add(f"ReopenRow{sid}", "reviewer",
        f"ATTACKS the Registry row `{sid}` (`grep -n '^| {sid} ' {L}/corpus/SOURCES.md`). Re-open its capture yourself ({cap(sid)}) and check every cell: source title/URL (the FIRST URL is the document), kind, tier (argued by scope: A only where the page is primary for what the row scopes), scope, anchor (each `char N` must be the offset of a located quote of this id: `awk -F'\\t' '$1==\"{sid}\"' {EV}/spans.tsv` gives span start + span.find(quote)), teaches (every clause carried by the capture? quote it or call it a defect), status, opened, recheck, used-by (exactly the entries whose `source:` line cites {sid}: `grep -ln '^source: {sid} ' {L}/corpus/knowledge/*.md`). Report holds/defect per cell with the located text, and whether the row survives a non-author re-open. Citing entry: {L}/{ENT[ent]}.")

# ---- entries: entailment critic + negatives/sweeps executor each
for e, path in ENT.items():
    add(f"CritEntry{e}", "critic",
        f"ATTACKS the entailment of {L}/{path}: for EVERY bullet under `#### Observation` and `#### Inference`, open the quoted spans in their capture text form (the `source:` lines name the ids; captures: {', '.join(cap(s) for s in URL)}) and judge whether the sentence as worded is carried by what the capture says — supports / weaker than the sentence / unsupported / contradicted. Look hardest at characterisations (\"requires\", \"asks\", \"names no\", \"only\", \"hosted copy\", \"not an attributed translation\", \"record, not the article\", \"bounded by procedure\"), at numbers (counts, offsets, character totals) and at any comparison with another lane file (open it). List each defect with the exact narrowed wording you would land.")
    add(f"ExecSweeps{e}", "executor",
        f"RE-RUNS every command and negative claim in {L}/{path}: the `recheck:` command, every sweep in `#### Unknown`, every 'occurs 0 times'/'names no'/'not in the capture' statement, and every `char N` (re-locate each quoted phrase with python `text.find` / `count` in the stated form; for S115 use `python3 {L}/tools/capture-text.py <raw> --locate '<q>'`). Paste each command and output and mark reproduces / differs (both numbers) / not runnable as written. Then widen two negatives by five synonyms each in the capture's language and say whether the narrowed wording still holds. Run `python3 {L}/tools/inference-ground.py --entry {L}/{path} --spans {EV}/spans.tsv --counts /dev/null --registry {L}/corpus/SOURCES.md --root {L} ` (read its docstring) and, in a scratch COPY of the entry, negate one Inference bullet's claim: does the tool catch it?")

# ---- C1 tool, supplement, frozen counter
add("ReviewToolFinal", "reviewer",
    f"ATTACKS the landed tool: `git -C {L} diff {CAND} {TIP} -- tools/capture-text.py` (the post-candidate changes: non-`w:document` root refusal, MAX_PART size bound via ZipInfo.file_size, root-escaping target refusal, MemoryError mapping, el.clear()). Check each against its docstring and erratum E2: can a crafted zip lie about file_size (a local header vs central directory mismatch; a stored entry larger than declared — does zipfile enforce it?), does the root check fire before any text is emitted for a part whose root is w:document in another namespace (Strict OOXML `http://purl.oclc.org/ooxml/wordprocessingml/main`: refused — is that stated?), does el.clear() break nested w:p inside a text box (compare output with and without it on {Q}/{key(URL['S115'])}.raw and on a nested-box fixture), is `..`-prefix check fooled by `a/../../x`? Reproduce each defect in {SCR}/R52W2ReviewToolFinal/.")
add("MutToolFinal", "mutation-tester",
    f"MUTATION-TESTS the landed tool against BOTH detectors (`python3 {EV}/c1-count.py --tool <m>` and `python3 {EV}/c1-supplement.py --tool <m>`, TMPDIR=your scratch): copy {L}/tools/capture-text.py and make one mutant per class: (1) root check removed; (2) size bound removed; (3) MAX_PART set to 1 KiB; (4) `..` check removed; (5) MemoryError mapping removed; (6) el.clear() moved to start events; (7) RUN_BREAKS parent check uses any ancestor w:r; (8) Fallback depth never decremented; (9) External rels not skipped; (10) refusal printed to stdout; (11) --locate counts overlapping occurrences; (12) text joined with no final newline. Kill matrix; every SURVIVOR of both detectors named with the generated case that would kill it (the post-candidate refusals are expected survivors of the frozen counter — say whether the supplement or any lane check sees them).")
add("SentToolFinal", "sentinel",
    f"RE-RUNS the wave-1 hazard set of {L}/.ufo/waves/round-52/w1/R52SentCapture.md (H1 zip bomb, H2 entity expansion and external entities, H3 traversal, H5 counter SIGTERM/--work) against the LANDED tool and counters at {TIP}: which hazards are closed, which remain (H4 build-spans default root, build-c2-controls without dir=, c1-count SIGTERM leak), with the reproducing command and output for each. Add one new attempt each: a zip whose central directory declares a small file_size for a large member; a deflate stream ending early (truncated zip); a 50,000-deep nested element (`RecursionError` in build-spans' recursive docx_text walk vs the tool's iterparse — run both). Severity and smallest fix per item.")
add("MutSupplement", "mutation-tester",
    f"MUTATION-TESTS the post-freeze supplement {EV}/c1-supplement.py (copy it with c1-count.py into a scratch dir — it imports c1-count.py from its own directory): one mutant per leg — PREFIX renames nothing; RELS_FORM keeps attribute order; SYNTAX inserts no comment/CDATA; REAL_TEXT checks only the character count; the default-namespace branch never taken; `respell_package` skips the decoy part. Run each mutant against the real tool (must still pass, else the mutant broke the generator) and against {EV}/controls/forge-shape.py and {EV}/controls/naive-tool.py (must fail). Report which legs are load-bearing (the forge passes when the leg is neutered) and which are decorative.")
add("CritForgeSupplement", "critic",
    f"ATTACKS the supplement {EV}/c1-supplement.py: write (in {SCR}/R52W2CritForgeSupplement/) the cheapest tool that passes BOTH `python3 {EV}/c1-count.py --tool <yours>` and `python3 {EV}/c1-supplement.py --tool <yours>` WITHOUT a real XML parser — prefix-agnostic regexes (`<[^:>]*:t>`), namespace-ignoring, attribute-order-ignoring, CDATA handling, a memoised NIPH text (the REAL_TEXT digest can be met by embedding the 19682-character text). If you pass both, paste the tool and output: say whether what you wrote IS an implementation of the written rule (a different parser) or a forge (keyed to the generators). Name the cheapest surviving cheat and the leg that would refuse it.")
add("ExecSeedSupplement", "executor",
    f"FLAKE and independence of the supplement and the frozen counter at {TIP}: in a shared clone (`git clone -q --shared {L} $S/clone && git -C $S/clone checkout -q {TIP}`) run `python3 corpus/evidence/round52/c1-supplement.py` 20 times unseeded and with `--seed 1..20`, and `python3 corpus/evidence/round52/c1-count.py` 10 times; tabulate legs and verdicts (≤60-line script in the report); print the first non-PASS in full and reproduce it by seed. Time one run of each; confirm zero leftover scratch dirs after each (count entries in TMPDIR) and none under /tmp.")
add("ExecRealDocxFinal", "executor",
    f"RE-RUNS real-data breadth with the LANDED tool: every `.raw` under {Q}/ starting with `PK\\x03\\x04` (8 expected) and every other `.raw` (2,588 expected), `python3 {L}/tools/capture-text.py <raw>`: rc, characters, REFUSED reason histogram. Compare with wave 1's table ({L}/.ufo/waves/round-52/w1/R52ExecRealDocx.md section 2): which rows changed (the two .xlsx and the OLE .doc should now be REFUSED exit 2; the two .docx unchanged at 19682 and 18841 characters — confirm sha256 of the NIPH output equals the supplement's TEXT_SHA `754aae42…`). Any non-zip that is not refused, or any docx whose output changed, is a defect.")

# ---- frozen counters on real bytes
add("ExecReplayAll", "executor",
    f"REPLAYS every counter from committed bytes: `git clone -q --shared {L} $S/clone && git -C $S/clone checkout -q {TIP}`, then from the clone root run `python3 corpus/evidence/round52/c1-count.py`, `c1-count.py --seed 7`, `c1-supplement.py`, `c2-count.py`, `c2-count.py --lane-only`, `build-spans.py --check`, `python3 corpus/evidence/round51/quote-substance-check.py corpus/evidence/round52/spans.tsv`, `python3 corpus/evidence/round47/c2-count.py` (gate registry: expect MISMATCHES=0), `python3 corpus/evidence/round52/verdict-gap.py --from 46 --to 51`, `controls/build-c2-controls.py`, and the census `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md`. Table every verdict line and exit code; say which differ from the lane working tree's runs and why.")
add("MutC2Counter", "mutation-tester",
    f"MUTATION-TESTS the frozen C2 counter on real bytes in a scratch COPY of the lane tree (`git clone -q --shared {L} $S/clone`, checkout {TIP}; pass `--root $S/clone`; c2-count reads BASE from the lane's git, which the clone has): (1) shift one `char N` in an anchor cell by 1; (2) change one quoted character in an entry; (3) swap S113 and S114 in a `source:` line; (4) add a path to a used-by cell; (5) delete the S120 verdict line from the lesson; (6) put the dead original URL first in S116's source cell; (7) rename an entry; (8) drop one spans.tsv row; (9) edit a span file by one byte; (10) add `S111` (an unbound lane id) to an entry body. Run `python3 corpus/evidence/round52/c2-count.py --root $S/clone` per mutation; report which leg turns FAIL and every SURVIVOR.")

# ---- lesson, criteria, gates, readme
add("ReviewLesson", "critic",
    f"ATTACKS {L}/corpus/lessons/round-52.md section by section: `## Mistakes` (every evidence pointer resolves and says what the row claims; every 'shown able to fail' command — run it and paste the red output), `## Spot-check intake` (each disposition true? run what it cites), `## Gate` (collision counts: re-run the section-10 grep/comm into your scratch; renumber map vs the Registry rows; the normalisation paragraph; the decisions table — re-open FOUR decisions' captures), the quarantine block (re-locate the three S120 quotes and the claim that round 51's `char 39411` is an offset of nothing: unzip -p the .raw word/document.xml and find the sentence), `## considerthese` (run verdict-gap), `## Census`, and whether anything changed after the freeze is missing from {EV}/claims-erratum.md (`git -C {L} diff {FREEZE} {TIP} --stat`). Each defect with its line and the observed value.")
add("ReviewQuality8790", "reviewer",
    f"ATTACKS QUALITY.md criteria 87-90 (`grep -n '^8[7-9]\\. \\|^90\\. ' {L}/corpus/QUALITY.md`): for each run its check command from the lane root and confirm the pass output; reproduce its 'shown able to fail' red state exactly (the candidate tool is `git -C {L} show {CAND}:tools/capture-text.py`); confirm every cited file, count and offset; check each cites its Mistakes row in the lesson and that row exists and says the same. A criterion whose red state you cannot reproduce, or whose named limit is wrong, is a defect. Say which of the four would not catch a regression of its own class.")
add("ReviewGatesRows", "reviewer",
    f"ATTACKS the SKILL.md `## Gates` rows `capture-text` and `chousa round-52 counters and checks` (`grep -n 'capture-text\\|round-52 counters' {L}/SKILL.md`): run every command the rows print, from the lane root (TMPDIR=scratch), and check every stated value (exit codes per verdict, LEGS=9/9, SUPPLEMENT_LEGS=4/4, control scores 4/9 0/9 0/9, the NIPH digest and 19682, the freeze and BASE_REV hashes, the refusal list against the tool's actual REFUSED reasons). Run `python3 {L}/corpus/evidence/round47/c2-count.py` (MISMATCHES must be 0). Every value that does not reproduce is a defect with the observed value.")
add("ReviewReadme", "critic",
    f"ATTACKS the appended README block `## Round52 coverage and frontier` in {L}/corpus/README.md (from that heading to EOF): every count and command (run them; the base sweep `git -C {L} grep -l -e 文献検索期間 -e 完全な検索戦略 -e 检索报告清单 {BASE} -- corpus/knowledge` must exit 1), every claim of what the lane 'held' before (git grep at {BASE}), the per-document credit of three with S113 as a second carrier (is the SinoMed record really the same article? compare {Q}/42bac8830527d6f1bb125c49.txt with S113's capture), and every 'Left open' item against the entries. Defects with lines and observed values.")
add("ReviewVerdictGap", "reviewer",
    f"ATTACKS the considerthese pick {EV}/verdict-gap.py: run `python3 {EV}/verdict-gap.py --from 40 --to 51` and `--from 46 --to 51`; for each printed gap and each UNPARSED round, open the SCORECARD `## Round N verdict` axis table and the round's verifier spot-check axis table and confirm the parse by hand; find rounds where the parser reads the wrong table (a claims table before the axis table, a `| depth | **improved** |` row inside prose) or misses a verifier form (round 48 bullets); does `dirn` misread 'improved narrowly, disputed as a trade' or 'not harmed'? Report every misparse with the line, and say whether the script's two gaps are real.")
add("CritGateDecisions", "critic",
    f"ATTACKS the lesson's Gate decisions table ({L}/corpus/lessons/round-52.md `### Decisions`): re-open the capture behind EVERY refuse/admit-later row (search-log-fields-r36, search-tracking-record-r40, chinese-search-log-r37, grey-literature-and-chinese-search-record-r40 and -r41; keys in the table) and check the stated reason and flip: does the cited string occur as stated (count, offset)? Is any flip condition already met (so the refusal is stale)? Is any refusal really a province call that the table dresses as a capture call? Also attack the three admits' 'admit' cells for the repair each names. Agree/disagree per row with evidence.")
add("ReviewQuarantine", "reviewer",
    f"ATTACKS the quarantine claims: (1) re-derive the lane's register slice from /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md with the section-10 awk (count the data rows: the lesson says 24) and list which rows name any of the four round-52 URLs in any spelling (http/https, trailing slash, the lifescience original vs the archive); (2) re-locate the S120 verdict's three quotes with `python3 {L}/tools/capture-text.py {Q}/{key(URL['S115'])}.raw --locate '<q>'` (lesson says 8996, 9020, 9428); (3) re-check the lesson's claim that the round-51 line's `char 39411` in the XML form is the offset of nothing (`unzip -p` the .raw word/document.xml, python find of the sentence, and of its first 10 characters). Verdict per item.")

# ---- admission and axes
add("CritAdmission", "critic",
    f"ATTACKS the round's admission case as the operator's closure would: for C1 (operability) and C2 (depth) write the strongest argument for REJECTION or a trade — C1: the frozen counter is forgeable (forge-shape passes 9/9), the supplement is post-freeze, the tool changed after the candidate in ways the frozen predicate does not list (erratum E2), and it is one file type; C2: entailment uncounted, one of four documents earns no expansion credit, BOUND 4/4 includes a second carrier, the counter accepts sidecar spans (E4). Then rebut each from committed bytes with commands. Verdict per claim (improved / improved narrowly / unprovable / harmed) and whether any owned axis is harmed (operability, depth, coverage, freshness, calibration, adjacency); name what you could not decide.")
add("CritAxisC1", "critic",
    f"ATTACKS C1 as an axis move: is tools/capture-text.py an operability move (a runnable artefact producing its stated outcome on the lane's real inputs) or plumbing? Which lane workflow calls it now (SKILL.md, the entries' recheck lines, the lesson's S120 verdict, the span builder — grep)? Does it move the round-1 operability observable ({L}/SCORECARD.md:7, 3/10)? Are C1 and C2 causally separable as {EV}/claims.md says: in a scratch clone at {TIP} delete tools/capture-text.py and run c2-count.py (must still PASS); delete the three entries and run c1-count.py (must still PASS). Verdict with commands.")
add("CritExpansion", "critic",
    f"ATTACKS C2's coverage and expansion credit as the lane states it (three documents; S113 a second carrier): argue both directions — that S113 should be credited (the abstract's last clause and the record-vs-article observation are new) or refused outright (a second carrier bound as a row is padding), and that S116 or S114 is itself a second carrier of ground the lane held (the lane's round-51 entries quote the JAOHFA form's PRISMA-derived wording `それぞれの情報源が最後に調べられた` — is S116's item-6 date sentence new ground or the same sentence's source?). Use `git -C {L} grep -n` at {BASE} for each claimed-new fact. Verdict per document: credit / no credit, with evidence.")

# ---- cross-cutting
add("ConnCrossEntry", "connector",
    f"CROSS-ENTRY consistency across the three entries, the four rows, the lesson, the README block and the claims erratum: the same fact stated in two places (an offset, a character total, a title, a date, the 'three documents' credit, the S113-S116 map, tier, the S120 offsets) must agree — build a table fact · place · value and mark every disagreement; check the entries do not contradict each other or the round-51 entries they reference (open {L}/corpus/knowledge/japanese-search-record-r38.md, chinese-search-record-r39.md, japanese-search-record-r38-amendment-2026-10-23.md), and that every lane file an entry names exists. Disagreements with file:line pairs.")
add("ConnSiblingsFinal", "connector",
    "FINAL sibling-overlap scan on the LANDED text: read the three new entries and tools/capture-text.py in /home/vgpnk/Projects/shokunin/chousa-shokunin/ and grep the sibling lanes under /home/vgpnk/Projects/shokunin/*-shokunin (corpus/knowledge, tools, SKILL.md, PROVINCE.md; read-only; skip chousa) for each distinctive claim (文献検索期間, 費用対効果評価, 中央社会保険医療協議会, 检索或查询日期, 中国全科医学, 梅斯, PRISMA 2020 チェックリスト, docx, word/document.xml, OOXML). Report any sibling holding the same fact or tool (path:line), any sibling PROVINCE.md claiming health-technology assessment or document-format tooling, and any entry claim that is another lane's domain. Verdict: overlap or not.")
add("ScoutClosureRisks", "scout",
    f"Read {L}/corpus/lessons/round-51-verifier-spotcheck.md and round-50's (the closure's method: what it re-measures, where it disagreed, section 6 routed defects) and predict the five items of THIS round the same closure is most likely to attack or route (file:line, the command it would run), and for each whether the committed bytes at {TIP} withstand it. Ranked table: risk · where · likely command · what the lane holds · gap.")
add("ScoutQuoteSample", "scout",
    f"Independent sample of the 38-row manifest {EV}/spans.tsv: pick 15 rows spread over S113-S116 WITHOUT reading the lesson table, open each capture (S115 via `python3 {L}/tools/capture-text.py <raw>`), confirm the quote occurs once at offset + span.find(quote), then read the entry sentence quoting it and judge: supports / weaker than the sentence / unrelated. Counts and every weaker case with the narrowing.")

# ---- census and inference
add("ExecCensusFinal", "executor",
    f"CENSUS and registry integrity at {TIP}: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` (exit, every W/E line), then the manual census one-liners from /home/vgpnk/Projects/shokunin/CORPUS.md section 'SOURCES.md — where a shokunin learns' from the lane root (rows 116, malformed 0, tiers, statuses, duplicate ids none, enum violations none, used-by paths exist); confirm rows S001-S112 are byte-identical to the base (`git -C {L} diff {BASE} {TIP} -- corpus/SOURCES.md` shows only four added lines). Also run the CORPUS.md 'provenance trio' check on the three entries (source:/verified-at:/recheck: first). Report every difference.")
add("ExecInfRegression", "executor",
    f"INFERENCE-GROUND regression: `python3 {L}/tools/inference-ground.py` is unchanged this round, but earlier counters read it — run `python3 {L}/corpus/evidence/round46/c1-count.py`, round47 and round48 counterparts (`ls {L}/corpus/evidence/round4[678]/*count*.py`; TMPDIR=scratch; paste each last line and exit) and the tool on each new entry with {EV}/spans.tsv (`--json` to your scratch to see per-bullet tokens). Then the CJK polarity probe: in scratch copies, rewrite one Inference bullet per entry to assert the opposite while keeping its quoted CJK phrase (e.g. 'requires' → 'does not require'), and report whether INF_POLARITY_FLIP fires. Name the blind spot.")

# ---- drafts for the L1
add("DraftLogEntry", "scribe",
    f"DRAFT the round-52 entry for {L}/LOG.md (append-only; read the Round 51 entry: `grep -n '^## Round 51' {L}/LOG.md`, read to EOF). Evidence only — every sentence cites a path, a commit (freeze {FREEZE}, candidate {CAND}, integration {TIP}), a counter output (run each counter at the lane tip with TMPDIR=scratch and quote its last lines) or a wave-1 seat report. Cover: C1 before → after (`LEGS=0/9` → `9/9`; controls 4/9 0/9 0/9; the shape forge 9/9 and the supplement 0/4 vs 4/4), the post-candidate tool changes (erratum E2), C2 (`C2=FAIL` → `C2=PASS`, BOUND=4/4, three documents credited), the S120 re-location, six mistakes, QUALITY 87-90, verdict-gap. ≤60 lines, plain prose; one fenced block labelled LOG.md.")
add("DraftScorecardVerdict", "scribe",
    f"DRAFT the round-52 block for {L}/SCORECARD.md in the shape of the `## Round 51 verdict` block (`grep -n '^## Round 51 verdict' {L}/SCORECARD.md`, read to EOF): claims table (claim/axis · before → after · counting command · verdict · tag) with HONEST verdicts — C1 'improved narrowly' if the frozen counter is forgeable (forge-shape 9/9) even though the supplement refuses it; C2 'improved' as presence and binding (entailment uncounted, one second carrier) — an axis table (operability, depth, calibration, coverage, freshness, adjacency) with one-line evidence each (run the counters at the tip; quote last lines), a `## Capabilities (round-52 addition)` row for capture-text with a pointer that resolves (`ls`), and `## Planned — round 53 (not started)` (candidates: the adopter twin-id/refusal-order patch from W1 R52ExecAdopterTwin; the anchored-correction check from W1 R52ExecPointerAnchor as a calibration claim; search-tracking-record-r40 with its quote re-cut; the verdict gaps). One fenced block labelled SCORECARD.md.")
add("DraftReportSections", "scribe",
    f"DRAFT the 'Sources & frontier' and 'Trend verdicts' sections of the round-52 fleet report (/home/vgpnk/Projects/shokunin/.ufo/reports/round-52/chousa.md; read /home/vgpnk/Projects/shokunin/.ufo/reports/round-51/chousa.md for the shape). Ground by running in {L}: rows 112 → 116 (`grep -cE '^\\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\\|' corpus/SOURCES.md`), tiers added (A: S114 S115; B: S113 S116), census exit at start ({EV}/census-start.txt) and now, the collision files in {L}/.ufo/waves/round-52/assimilation/, the renumber map, assimilation theme and admits/refusals, considerthese pick (verdict-gap), mined mistakes count, sourced claim, freshness (newest capture date: `ls -l --time-style=long-iso {Q} | sort -k6,7 | tail -2`), the open-items line `Open operator items: 8d77e6c1 since round 42 (10 rounds)` checked with `python3 {L}/corpus/evidence/round51/open-items-age.py <draft> --round 52`. Trend verdicts: expansion, quality, discernment with evidence and caveats. One fenced block.")

spec = {
    "wave": "chousa-r52-w2",
    "milestone": "Round 52 falsify: re-open the four rows, attack the three entries' entailment and sweeps, mutate and forge the landed tool and supplement, replay every counter, attack the lesson, criteria, Gates rows, README and admission case",
    "reportDir": ".ufo/waves/round-52/w2",
    "axes": ["operability", "depth"],
    "context": CONTEXT,
    "items": items,
}
out = pathlib.Path(__file__).with_name("w2-spec.json")
out.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
c = Counter(i["role"] for i in items)
print(len(items), dict(c))
attack = c["reviewer"] + c["critic"] + c["mutation-tester"] + c["sentinel"]
print(f"attack-share={attack/len(items):.2f}")
names = [i["name"] for i in items]
print("NAME_COLLISIONS=%d" % (len(names) - len(set(names))))
