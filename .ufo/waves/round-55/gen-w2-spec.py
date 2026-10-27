#!/usr/bin/env python3
"""Generate the round-55 wave-2 (falsify) spec. Writes w2-spec.json beside itself. TIP = lane master now."""
import hashlib
import json
import pathlib
import subprocess
from collections import Counter

L = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
Q = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache"
P = "/home/vgpnk/Projects/shokuknow/merge/chousa"
K = f"{P}/knowledge/corpus/knowledge"
EV = f"{L}/corpus/evidence/round55"
W1 = f"{L}/.ufo/waves/round-55/w1"
W54 = f"{L}/.ufo/waves/round-54/w2"
SCR = "/fast/scratch/hyaku/chousa-r55"
FREEZE = "1fc5d92b5a7866ec16f1cac2de749fccfa6b49cb"
CAND = "6ca924995d48facbf704d2aa22ddaec236059039"
BASE = "dba605deb5cd5ed4874e0e3c39ba24737409cd80"
TIP = subprocess.run(["git", "-C", L, "rev-parse", "master"], capture_output=True, text=True, check=True).stdout.strip()
REG = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md"
ENT = f"{L}/corpus/knowledge/grey-literature-and-chinese-search-record-r40.md"
R36 = f"{L}/corpus/knowledge/source-type-taxonomy-r36.md"
LES = f"{L}/corpus/lessons/round-55.md"
QUAL = f"{L}/corpus/QUALITY.md"
GCP = "http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc"
CNPHARM = "http://m.cnpharm.com/201906/18/c280684.html"
NMPA_EN = "https://english.nmpa.gov.cn/2019-07/18/c_388252.htm"


def key(u):
    return hashlib.sha256(u.encode()).hexdigest()[:24]


GCP_FORM = f"`python3 {L}/tools/capture-text.py {Q}/{key(GCP)}.raw` (the defined OLE text form; never the `.txt` sidecar)"

CONTEXT = f"""# Goal
chousa lane (deep-research method), round 55, wave 2 (FALSIFY). Wave 1 built and the L1 integrated at lane tip {TIP} (`git -C {L} log --oneline {BASE}..{TIP}`). Three claims are FROZEN at {FREEZE} in {EV}/claims.md (read it first); never propose changing a predicate, target, counter or control — findings against them are reported, not patched. C1 (operability, capability acquisition): `tools/build-spans.py` (candidate {CAND}) builds span manifests through each capture's DEFINED text form (OLE/zip `.raw` via `tools/capture-text.py`, else `.txt`; no UTF-16LE fallback); counter `python3 {EV}/c1-count.py`, after-receipt {EV}/c1-measure-after.txt (LEGS=4/4 ×4). C2 (depth, sourced): the NMPA grey-literature search-record field by document — entry {ENT}, rows S124 (gcpunion `.doc` copy of the guideline, {GCP}), S125 (中国食品药品网 report, {CNPHARM}), S126 (NMPA English notice, {NMPA_EN}) in {L}/corpus/SOURCES.md, quotes {EV}/quotes.tsv → spans {EV}/spans.tsv, lesson {LES} (`## Gate`, quarantine verdict for register S125 round6 — the register's id, not the lane's S125); counter `python3 {EV}/c2-count.py`. C3 (calibration): eleven anchored errata E01–E11 in {L}/SCORECARD.md `## Round 55 statement errata`, with in-target corrections ({R36} `#### Corrections (round 55)`, {QUAL} criterion 101, the lesson's `## Corrections`); counter `python3 {EV}/c3-count.py`. Also landed: QUALITY 102–105, {EV}/wave-settled-check.py, {EV}/considerthese-ledger-check.py, {EV}/pdf-crosscheck.py (each with a `.txt` receipt), SKILL.md registry rows for `build-spans` and the round-55 counters, a corpus/README.md Round55 section. Wave-1 seat reports are in {W1}/ (read the ones your item names). The round-54 W2 reports are in {W54}/. Attack: every item names what it attacks; report survives / falsified with evidence. The planner seat is held by the L1.

# Boundaries (binding)
Lane repo: {L}. Your ONLY write is your own report file: every `Report:` trailer path is relative to {L} — write it at {L}/<that path>. Never write a production file, another seat's report, the git index, jj state, the fleet repo /home/vgpnk/Projects/shokunin (read only), any sibling lane, or /home/vgpnk/Projects/shokuknow (read-only; never run its campaign tools renumber-staged.py, merge-plan.py, quote-lint.py, absent-defect-register.py). Never run git commit/add/stash/checkout/reset/push or any mutating jj command anywhere except inside your own fixture repo. Your cwd starts at the fleet root: cd to your scratch first. Scratch ONLY under {SCR}/<YourSeatName>/ (create with mkdir -p; export TMPDIR there and PYTHONDONTWRITEBYTECODE=1; never /tmp, never /dev/shm for anything over 50 MB; never a relative redirect — every output path absolute under your scratch) and remove it before you finish (trap 'rm -rf -- "$S"' EXIT); copy any receipt you cite into your report first. Every counter run passes `--work <empty dir under your scratch>` where it accepts one. Any LibreOffice run uses a private profile under your scratch and must leave no `soffice.bin` behind. Any git fixture repo: D=$(mktemp -d -p {SCR}/<YourSeatName>) && git -C "$D" init -q, every later git call names -C "$D", verify `git -C "$D" rev-parse --show-toplevel` equals $D before any commit. To test a modified copy of a lane file, copy the lane (`git -C {L} archive {TIP} | tar -x -C $S/lane`) and edit the copy — never the lane. No network and no live source fetch (L0 `8d77e6c1` is open): every source is an on-disk capture under {Q} (key = first 24 hex of sha256 of the URL). No writes to any PATH directory (~/.local/bin included). Never message the orchestrator or other lanes' seats.

# Evidence
Ground every statement in a command you ran or a file:line/char offset you opened; paste commands with observed output. A check you did not run has not passed. ≤120 lines. End with a one-line VERDICT naming what you attacked and whether it survived.

# Tooling
Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard: ALL pacman transactions are PAUSED host-wide (never -S/-Sy/-Syu/-U/-R, no downgrade, no service restart); use uv tool / npx / an official binary in ~/.local/bin instead (e.g. `uv run --with pypdf python …` in your scratch). Routing is host-owned; never pass a model."""

items = []


def add(name, role, text):
    items.append({"name": name, "role": role, "item": text})


# ---------------- C1
add("R55W2ExecC1Rerun", "executor",
    f"Attack C1's after-state at {TIP}: sha256 {L}/tools/build-spans.py (must equal the {CAND} blob) and tools/capture-text.py (must be 2c0140bc…); run `python3 {EV}/c1-count.py --seed 7 --work <empty>` and three unseeded runs (fresh --work each); paste every line and compare with {EV}/c1-measure-after.txt. Then `--per-leg 6 --seed 555`. Any FAIL: reproduce and name the leg, quote and line.")
add("R55W2CritForgeNonReader", "critic",
    f"W1 `R55CritForgeEcho` ({W1}/R55CritForgeEcho.md) admits its surrogate forge was misconfigured. Build a real non-reading forge for {EV}/c1-count.py: a builder that never imports, copies or reimplements `tools/capture-text.py` (no CFB/FIB/Clx parsing) yet tries to produce exact slices of the defined form — e.g. search the quote in the raw's UTF-16LE decode and in the `.txt` sidecar and emit a slice of that; strip control chars to approximate the form; exploit that a window's 80-char context may be taken from either side. Score with `--seed 7` and two unseeded runs; per leg, the first divergence from the defined form. VERDICT: best LEGS a non-reading forge reaches.")
add("R55W2CritHookEscape", "critic",
    f"W1 `R55CritForgeHook` ({W1}/R55CritForgeHook.md) found the hook in {EV}/c1-count.py does not resolve `dir_fd`/relative opens after `os.chdir` and does not list `os.symlink`/`os.kill`. Turn that into an exploit or rule it out: from inside the builder, can you reach anything that reveals an expected offset or the seed (the counter's process memory `/proc/<ppid>/mem` or `/proc/<ppid>/environ`, its argv, a file the counter writes)? Can you read the campaign cache or the lane corpus via `os.open(name, dir_fd=…)`? Paste probes (a scratch builder run under the counter) and the counter output. VERDICT: hole exploitable for a leg pass or only a boundary defect.")
add("R55W2MutC1BuilderKill", "mutation-tester",
    f"Mutation kill table for the C1 candidate (independent of W1 `R55MutC1Builder`): in a scratch lane copy at {TIP}, mutate `tools/build-spans.py` one at a time — use the `.txt` sidecar first for OLE, fall back to UTF-16LE for unknown raws, CONTEXT 79/81, accept 2 occurrences, write before refusing, drop universal-newline normalisation, offset=char, skip the zip branch, refuse zip raws — and run the copy's `corpus/evidence/round55/c1-count.py --seed 7 --work <empty>`. Table mutant → LEGS → killing leg; list survivors and say what input would catch each.")
add("R55W2ReviewC1Claims", "reviewer",
    f"Review every landed C1 claim against evidence: the SKILL.md `build-spans` row (registered as `probe`: is that the honest kind under PROTOCOL §Gate standard?), the corpus/README.md Round55 `../tools/build-spans.py` row (\"re-derives rounds 47 and 50–54's committed manifests byte for byte and the nine round-49 OLE rows\" — re-run it: `git -C {L} show {BASE}:corpus/evidence/round5N/quotes.tsv` → `python3 {L}/tools/build-spans.py --quotes … --out $S/oN --cache {Q}` then diff against committed spans), and {EV}/c1-seed-sweep-L1.txt. Report each claim survives / overstated with your output.")
add("R55W2SentBuilder", "sentinel",
    f"Hazard review of {L}/tools/build-spans.py at {TIP}: `--out` pointing at an existing directory with unrelated `S###-N.txt` files (it deletes orphans — demonstrate in scratch), a symlinked `spans/` dir, a cache `.raw` that is a zip bomb or a huge OLE file (memory/time through capture-text), a `.txt` that is a FIFO or /dev/zero symlink, quotes.tsv with 100k rows, an entry path with `..`. Run each in scratch; report exit code, wall time, peak RSS, and any write outside --out. Propose the smallest guard per hazard (do not edit).")
add("R55W2CritC1Verdict", "critic",
    f"Attack the planned C1 verdict 'improved (capability acquisition)': does the counter measure that the builder reads OLE through the defined form, or only that its output equals capture-text's (would a builder that shells to capture-text pass? — note the hook), and is a wrapper around an existing tool a capability worth a SCORECARD row (AXES.md Capabilities)? Is RW-1 (the forgeable-counter streak, {L}/corpus/evidence/round53/recurring.tsv) broken this round, still running, or unknowable from W1+W2 evidence? Read {W1}/R55CritForge*.md, R55MutC1*.md, R55ReviewC1*.md. VERDICT with the honest wording.")
add("R55W2ExecBuilderDiff", "executor",
    f"Diff the candidate against the round-54 builder: `diff {L}/corpus/evidence/round54/build-spans.py {L}/tools/build-spans.py`; for each behavioural difference construct a scratch capture and quote that shows it (OLE raw + garbage `.txt` sidecar; zip raw + `.txt`; HTML raw + `.txt` with the quote twice; unknown raw, no `.txt`); run both builders (round-54 one via a scratch lane copy with its own quotes path) and tabulate outputs/exit codes. Confirm no behavioural change for `.txt`-only captures.")

# ---------------- C2
add("R55W2ExecC2Rerun", "executor",
    f"Attack C2's after-state at {TIP}: run `python3 {EV}/c2-count.py` and `--lane-only` (paste all lines and exits), `python3 {L}/tools/build-spans.py --quotes {EV}/quotes.tsv --out {EV} --check` from a scratch COPY of the lane (the --check writes nothing, but run it on the copy anyway), `python3 {L}/corpus/evidence/round51/quote-substance-check.py {EV}/spans.tsv`, `python3 {L}/tools/inference-ground.py --entry {ENT} --spans {EV}/spans.tsv --counts /dev/null --registry {L}/corpus/SOURCES.md --root {L}`. Then rebuild the controls (`python3 {EV}/controls/build-c2-controls.py $S/c2c`) and score them; compare with {EV}/controls/c2-controls.txt.")
add("R55W2ReopenS124", "scout",
    f"Re-open lane S124 ({GCP}; form {GCP_FORM}) and verify, quote by quote, every S124 offset the lane states: the entry's `source:` line chars (761, 994, 4625, 4652), every `char N` in its Observation bullets, the S124 Registry row's anchor cell, the lesson's quote table, and the entry's Unknown sweep command (run it from {L}; does it print what the entry says?). Report each mismatch with the true value.")
add("R55W2ReopenS125", "scout",
    f"Re-open lane S125 ({CNPHARM}; {Q}/{key(CNPHARM)}.txt read UTF-8 with universal newlines) and verify every S125 quote, offset and fact in {ENT}, the S125 Registry row (title cell, scope, anchor chars 242/371/780, teaches: 'issued … by notice on 18 June', five parts, Cochrane) and the lesson. Is '2019-06-18' in the body or only the byline? Is the 'teaches' cell entailed sentence by sentence? Report mismatches.")
add("R55W2ReopenS126", "scout",
    f"Re-open lane S126 ({NMPA_EN}; {Q}/{key(NMPA_EN)}.txt read UTF-8 with universal newlines) and verify every S126 quote and offset (777, 1204, 1324, 2528) and the Registry row's teaches cell (issued June 18 2019; cites Article 4 of the 2018 No. 66 announcement; Cochrane). Is 'tier A for identity and date' defensible (the page is on the regulator's domain, 'Presented by China Daily', 'CCFDIE')? Report mismatches and the honest tier wording.")
add("R55W2CritEntailObs", "critic",
    f"Entailment attack on the LANDED entry {ENT} `#### Observation` (six bullets) against the defined forms (S124 {GCP_FORM}; S125/S126 `.txt`). For each sentence: ENTAILED / OVERSTATED / ABSENT with offsets or sweep counts. Watch: 'lists, under 2' and 'continues on the same line'; 'the four kinds are examples (`等`)'; 'names 国家药品监督管理局 only as the author of an earlier announcement'; '2019 occurs 0 times and 发布 0 times'; 'matching the `.doc`'s five numbered headings'; 'the English page renders it as'.")
add("R55W2CritEntailInf", "critic",
    f"Entailment attack on the LANDED entry {ENT} `#### Inference` and `#### Unknown`: 'makes … a field of the evaluation report, not only a step of the search'; 'the issuer is attested by S125 … and S126 …, not by the `.doc`'; 'the field is about completeness of evidence, not about a source list' and 'the method point this entry adds to the lane's grey-literature-as-source-category entries' (check the lane: `git -C {L} grep -n 灰色文献 -- corpus/knowledge`); 'identity is fixed by two independent issuance records' — are S125 and S126 independent of each other? Each: survives / narrow to <wording> / cut.")
add("R55W2ReviewRows", "reviewer",
    f"Review Registry rows S124–S126 in {L}/corpus/SOURCES.md against /home/vgpnk/Projects/shokunin/CORPUS.md section SOURCES.md (11 cells, enums, no `|` in cells, anchor char N = a located quote's offset in the defined form, `opened` 2026-10-27, `recheck` 180d, used-by), the tier justifications (B third-party copy; B newspaper; A regulator's English site for identity only), and the census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` (paste). Any row whose `teaches` exceeds its source?")
add("R55W2CritQuarantine", "critic",
    f"Attack the lesson's verdict for absent-defect register row S125 (round6; `grep -n 'round6 | S125' {REG}`): {LES} says `absent-as-written` (two of three quoted strings present in the defined form, the third differs only by curly quotes around 灰色文献). Re-derive the three counts in {GCP_FORM}, the `.txt` sidecar and the UTF-16LE decode. Is `absent-as-written` the right class under the lane's classes (round 42–54 lessons: `grep -rn 'absent-as-written' {L}/corpus/lessons | head`), or should it be `present` with a note? Is the 'register's payload-absent is wrong for two quotes' sentence right?")
add("R55W2CritGate", "critic",
    f"Attack the lesson Gate decisions in {LES} `## Gate`: the r40 admit-narrowed reasons; the r43 refusal ({K}/grey-literature-field-boundary-r43.md — read it; is the refusal reason true? is the flip checkable?) and its `refused-doc` line for staged S161; the decision not to cite the held S113 (medsci) — read {W1}/R55GroundMedsci.md if present and the capture {Q}/453d492becd9a2f4632cb8dd.txt; the admit/reject spot-check instructions (run them exactly as written; do they work?).")
add("R55W2MutC2Landed", "mutation-tester",
    f"Mutation-test {EV}/c2-count.py against the LANDED state: in a scratch lane copy at {TIP}, make one perturbation at a time and run `python3 $S/lane/corpus/evidence/round55/c2-count.py --root $S/lane` — drop one lesson quote row, change an S124 anchor `char 4652`→`4653`, add a `source: S113 — …` line without S113's used-by, change S125 `opened` to 2026-10-26, replace one span file with the slice from the `.doc`'s `.txt` sidecar (and fix its digest column to the sidecar's), add a stray `S130` token to the entry, delete the quarantine verdict line. Table: perturbation → C2 line that fails. Name any perturbation the counter misses.")
add("R55W2ConnAdjacency", "connector",
    f"Adjacency and cross-lane pattern for C2: the entry claims the drug-safety evaluation practice is adjacent ground it reports and does not hold. Scan sibling PROVINCE.md and corpora (/home/vgpnk/Projects/shokunin/*-shokunin/, read-only, skip chousa) for pharmacovigilance, ADR, 药品不良反应, 上市许可持有人, NMPA, systematic review reporting, PRISMA. Who, if anyone, owns it? Also: do the lane's other 灰色文献 entries ({L}/corpus/knowledge/chinese-search-record-r39.md, quality-control-guideline-issued-text-r48.md, western-instrument-alignment-r50.md) now contradict or need a pointer to the new entry? Report.")

# ---------------- C3
add("R55W2ExecC3Rerun", "executor",
    f"Attack C3's after-state at {TIP}: run `python3 {EV}/c3-count.py --work <empty>` (full, with E11; paste every line), then `--skip-slow`; rebuild the controls (`python3 {EV}/controls/build-c3-controls.py $S/c3c`) and score both (`--root $S/c3c/<name>`), compare with {EV}/controls/c3-controls.txt. Then append one extra stray `erratum: E05 …` line with a wrong observation OUTSIDE the errata section of a scratch copy's SCORECARD.md and confirm it is ignored; and one inside the section after the real E05 line (last-wins) and confirm E05 turns WRONG.")
add("R55W2CritErrataReadings", "critic",
    f"Attack the readings paragraph under {L}/SCORECARD.md `## Round 55 statement errata` and the observations: E01 — is `该标准暂无全文，请等待更新` really a latent, undisplayed template string (inspect the context around char 1712 of {Q}/b9ca2a4fdf9455867534f144.txt — a JS i18n map? any condition that would display it?); E03 — does 'prescribes' really overstate given S123 carries the type table; E05 — 'no constant repairs all six, but one repairs five'; E09 — rc=0 and SPAWNED really mean the hook missed a spawn; E11 — is the echo tool's 3/3 a property of the supplement (re-derive in a BASE mirror). Each: reading survives / wrong, with evidence.")
add("R55W2ReviewR36Corr", "reviewer",
    f"Review the `#### Corrections (round 55)` section appended to {R36}: is each bullet true against the captures (S121 {Q}/adf6ba934e813b2c326fa150.txt, S122 {Q}/b9ca2a4fdf9455867534f144.txt, universal newlines), does it point at the right bullet ('third inference bullet', 'fourth observation', 'last inference bullet', 'verified-at line'), does each of the four C3 anchors still occur exactly once in the file (python count), and does `python3 {L}/tools/inference-ground.py --entry {R36} --spans {L}/corpus/evidence/round54/spans.tsv --counts /dev/null --registry {L}/corpus/SOURCES.md --root {L}` still pass?")
add("R55W2ReviewQ101", "reviewer",
    f"Review QUALITY 101 in {QUAL} (round-55 correction of 97/98): every number it states (12795/12963 for which phrase, +802 ×5, −9251, 18,451, 469, rc 0, SHELL 1/6) re-derived by you — `git -C {L} show {BASE}:tools/capture-text.py > $S/ct.py`, the six S101 phrases from the S101 `correction:` lines in {L}/SCORECARD.md 'Round 54 pointer corrections', {Q}/6dc68fd6b32ce9c8dfcebce8.raw. Does 101 itself avoid repeating any C3 anchor? Is its Check runnable as written and its 'Shown able to fail' true ({EV}/controls/c3-controls.txt)?")
add("R55W2MutC3Errata", "mutation-tester",
    f"Mutation-test the landed errata against {EV}/c3-count.py: in a scratch lane copy at {TIP}, perturb one erratum at a time (one character of an observation; an anchor shortened to drop the key phrase; an anchor that now occurs twice because you paste it into the target's correction section; a target path typo; the section heading renamed) and run `--work <empty> --skip-slow` (E11 separately once). Table perturbation → item status. Also: does any later lane edit this round (r36 Corrections, QUALITY 101–105) risk making an anchor occur twice? (python counts at {TIP}).")
add("R55W2CritC3Honest", "critic",
    f"Is C3 an honest calibration move? Read {EV}/claims.md C3, {L}/SCORECARD.md errata block, {W1}/R55ExecC3Obs*.md (independent observations), {W1}/R55CritC3Calib.md if present. Attack: (a) are all eleven real mismatches between a lane self-statement and repo state (quote each statement at {BASE}); (b) could C3 be satisfied by copying W2 numbers without observing (did W1 seats' independent derivations match the counter? compare their observed strings); (c) does any remaining round-54 W2 falsification of a lane statement lack an erratum (scan {W54}/*.md). VERDICT: honest / inflated / incomplete with item ids.")

# ---------------- frontier, integration, conformance
add("R55W2ReviewQ102to105", "reviewer",
    f"Review QUALITY 102–105 in {QUAL}: re-run each Check exactly as written (102: the DELEGATE control via `python3 {EV}/controls/build-c1-controls.py $S/ctl` then `python3 {EV}/c1-count.py --tool $S/ctl/delegate.py --seed 55 --work <empty>`; 103: `uv run --with pypdf python {EV}/pdf-crosscheck.py` and `python3 {EV}/considerthese-ledger-check.py --root {L}`; 104: `python3 {EV}/wave-settled-check.py --round 54` and `--round 52`; 105: the three builders with an in-lane OUTDIR — check nothing is created). Does each 'Shown able to fail' reproduce? Any criterion that restates a C3 anchor?")
add("R55W2MutLedgerV2", "mutation-tester",
    f"Attack {EV}/considerthese-ledger-check.py (round-55 successor): in scratch fixtures, try a symlink inside the root pointing outside, a pointer `a/../../etc/hostname`, a regex the nested-quantifier heuristic misses but still backtracks (`(a|a)+$`, `(a|aa)*c`, `(.*a){{20}}`), a 1 MiB+1 file, a file that grows between stat and read, a ledger row with 5 columns, a considerthese bullet under a different heading. For each: exit code and wall time; which escape works. Receipts {EV}/considerthese-ledger-check.txt reproduce?")
add("R55W2MutPdfV2", "mutation-tester",
    f"Attack {EV}/pdf-crosscheck.py (round-55 successor; run with `uv run --with pypdf python` from your scratch): fixtures — a duplicated S123 row (22 rows), an S123 row with a whitespace-only quote, a BOM-prefixed header, CRLF line ends, a quote present only after NFKC, a wrong sha256 pin (copy the script and edit the pin in scratch). Exit code per fixture; does the 21-row denominator mean 'exactly the frozen set' or just 'any 21 rows'? Reproduce {EV}/pdf-crosscheck.txt.")
add("R55W2MutWaveSettled", "mutation-tester",
    f"Attack {EV}/wave-settled-check.py: in a scratch git fixture (D=$(mktemp -d -p $S) && git -C \"$D\" init -q) build a lane-shaped and a fleet-shaped repo and test — a results file committed after the report; a results file renamed; an uncommitted results file; a dispatched marker that is uncommitted; an ABANDONED marker whose first line is not the timestamp form; a report added, deleted and re-added (which commit counts?); timezone offsets that differ between repos. Exit code per case; which cases mislead? Reproduce {EV}/wave-settled-check.txt on the real repos.")
add("R55W2CritMistakes", "critic",
    f"Attack {LES} `## Mistakes` (three rows): pointers resolve (open each), `captured-by` honest, each fix shown able to fail with a command you run (row 1: `python3 {EV}/wave-settled-check.py --round 54`; row 2: the E08 observation; row 3: the C1 hook and W1 forge reports). Is row 3 a real mistake of the lane or a restatement of a W2 finding? Is any bigger round-54 mistake missing (read {L}/corpus/lessons/round-54-verifier-spotcheck.md §6 and {W54}/R54W2CritCredit.md, R54W2CritTrends.md)?")
add("R55W2ReviewGateConformance", "reviewer",
    f"Section-10 conformance of {LES} `## Gate` against the round prompt (/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-55.md §6 item 10): collision lists and counts pasted? renumber map by document? recheck prose stripped and recorded? ≥1 admit and ≥1 reject from the assimilation set? quarantine slice derived and the theme rows hand-checked? `refused-doc` lines? Also the W04 adjudication paragraph: re-read rows S050–S053, S059, S070–S075 in {L}/corpus/SOURCES.md and say whether each pair disposition is right.")
add("R55W2ScoutW2Integration", "scout",
    f"Integration completeness for round-54 W2: read {W1}/R55RegisterW2A.md and R55RegisterW2B.md (the register of every round-54 W2 finding with a proposed disposition) and check what actually landed at {TIP} (`git -C {L} diff {BASE} {TIP} --stat`; grep the lesson, QUALITY 101–105, SCORECARD errata, the r36 entry). List every finding whose disposition did not land, with file:line, and say whether its absence matters for this round's claims or only for the next round.")
add("R55W2CritTrends", "critic",
    f"Attack the round's planned trend verdicts before they are filed: expansion improved (three documents S124–S126 absent at base, one entry; `git -C {L} grep -c 是否检索灰色文献 {BASE} -- corpus/knowledge`), quality improved (C1 defined-form spans; r36/QUALITY corrections; check successors), discernment improved (C3 errata recomputed by a counter; quarantine verdict; Gate refusal r43). For each: is 'improved' earned by evidence at {TIP}, or should it be 'unchanged'/'unprovable-but-better'? Is any axis harmed (compare `git -C {L} diff --numstat {BASE} {TIP}` for removed lines; did any existing row, entry or criterion lose content)?")
add("R55W2ExecCensusMisroot", "executor",
    f"Census and hygiene at {TIP}: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` (paste, exit); row count `grep -cE '^\\|[[:space:]]*S[0-9]{{3,}}[[:space:]]*\\|' {L}/corpus/SOURCES.md` (expect 126); tier/status histograms per CORPUS.md; `git -C /home/vgpnk/Projects/shokunin status --porcelain` — list untracked fleet-root files whose content names chousa round 55 (misroots; do NOT move or delete them, just list path + first line); `git -C {L} status --porcelain` (expect only W1/W2 reports and markers); any `__pycache__` the round's counters left in the lane.")
add("R55W2ReviewEntryShape", "reviewer",
    f"Review {ENT} against the lane's entry bar ({QUAL} criteria for entries; the provenance-trio shape of {L}/corpus/knowledge/source-type-taxonomy-r37.md): title claim vs body, `source:` lines (URL immediately after the em dash; anchors), `verified-at` (its `--check` command — run it on a scratch copy), `recheck:` command (run it), `ground:` (its git grep — run it), `adopted:` line; every S-token bound; negative claims carry sweeps. Report every defect with line number.")
add("R55W2CritS101Next", "critic",
    f"Frontier claim check: corpus/README.md Round55 'Left open' says the four round-54 S101 quotes build 4/4 with the new builder (W1 {W1}/R55ExecS101Leg.md). Re-run it: build those quotes (url https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc) with `python3 {L}/tools/build-spans.py --cache {Q}`; report offsets and refusals; is the README sentence accurate? Also: S100/S101 Registry anchors were re-pointed in round 54 by `correction:` lines — do the builder's offsets agree with those corrections?")

spec = {
    "wave": "chousa-r55-w2",
    "milestone": "Round 55 falsify: re-run every counter and check, re-open S124-S126, attack the entry, errata, corrections, QUALITY 101-105, Gate and the new checks",
    "reportDir": ".ufo/waves/round-55/w2",
    "axes": ["operability", "depth", "calibration"],
    "context": CONTEXT,
    "items": items,
}
out = pathlib.Path(__file__).with_name("w2-spec.json")
out.write_text(json.dumps(spec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
c = Counter(i["role"] for i in items)
print(len(items), dict(c))
attack = c["reviewer"] + c["critic"] + c["mutation-tester"]
print(f"attack-share={attack/len(items):.2f}")
names = [i["name"] for i in items]
print("NAME_COLLISIONS=%d" % (len(names) - len(set(names))))
