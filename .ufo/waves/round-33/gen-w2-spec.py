#!/usr/bin/env python3
"""chousa round 33 wave 2 = falsify. Usage: gen-w2-spec.py > w2-spec.json"""
import json
import pathlib
import sys
from collections import Counter

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
WD = f"{LANE}/.ufo/waves/round-33/w2"
W1 = f"{LANE}/.ufo/waves/round-33/w1"
SCR = "/fast/scratch/hyaku/chousa-r33/w2"
TIP = "0fb300b5c27900ab8bb3abeb5f54776d71e04beb"
BASE = "2b9cc73aed30c2e2c95699db6617d9531ef49fb2"
GATE = f"{LANE}/tools/research-gate.sh"
GSHA = "94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e"
BSHA = "f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0"
C1 = f"{LANE}/corpus/evidence/round33/c1-count-v2.py"
C2V3 = f"{LANE}/corpus/evidence/round32/c2-count-v3.py"
CLAIMS = f"{LANE}/corpus/evidence/round33/claims.md"
KNOW = f"{LANE}/corpus/knowledge/claim-record-fields-r33.md"
SPOT = f"{LANE}/corpus/lessons/round-32-verifier-spotcheck.md"
ORACLE = f"{LANE}/.ufo/waves/round-33/controls/L1-design/oracle-gate.sh"
PROMPT = "/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-33.md"
GOD = pathlib.Path.home().joinpath(".agents/skills/godspeed/directive.md").read_text()
LEAD = "/skill:godspeed\n" + GOD + "\n"

CONTEXT = f"""# Goal
chousa lane (deep-research method: question framing, source hierarchy, citation chaining, claim-vs-source verification), round 33, WAVE 2 = FALSIFY. Lane repo {LANE} (jj-colocated, branch master, tip {TIP}). Round base {BASE} (gate SHA-256 {BSHA}). Landed gate tools/research-gate.sh SHA-256 {GSHA}. Read {CLAIMS} first (design v1 then the appended "Design v2" section, which governs).
One claim: C1 operability — verify-claims reads id/source/span/expect/marker/line/sha256 from the record's TOP-LEVEL JSON object only (claim_scan in the gate); a nested member of the same name changes nothing; a repeated top-level read field makes the record invalid; string content is never structure; a line that is not one well-formed object is invalid. Counter v2 `python3 corpus/evidence/round33/c1-count-v2.py` prints TOPLEVEL_FIELD_MATCH=k/156; P1 v2 needs 156/156 on two fresh seeds and no lower run on the landed revision. L1 measured base 60/156, landed 156/156 on seeds 3351/3352 (gate 52f07c74) and 3371/3372 (gate {GSHA[:8]}). Pre-data controls: best non-oracle 142/156 ({LANE}/.ufo/waves/round-33/controls/L1-v2-rescore/summary.txt). Repairs (not claims): D1 exempt-hop counter v3 {C2V3} (decoupled metadata); D2 census corpus/evidence/round33/d2-census.py; D3 battery header ({W1}/ExecNoHarmBase33/battery.sh); D5 check corpus/evidence/round33/no-name-signals.sh; QUALITY 36-39; sources S062 (RFC 8259) and S063 (Python json docs); knowledge {KNOW}.
Your item attacks one thing. A finding that the landed gate breaks the C1 contract (claims.md) on inputs the counter does not generate is the most valuable output: give the minimal input line, base vs landed output, and what the contract says. Never edit lane files; the L1 integrates.

# Contract
- Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. Write your report once. Extra artifacts (receipts, inputs, outputs, mutant gates) go ONLY inside your own directory {WD}/<YourName>/ (create it); each artifact under 1 MiB (large logs stay in scratch; cite path and sha256).
- KILL RULE BINDING: every run of c1-count-v2.py on the landed gate ({GSHA}) MUST pass `--receipt {WD}/<YourName>/<name>.json` (fresh seeds, never 3301-3373) and redirect stdout to a file (never pipe it into head/tail: the counter prints before it writes the receipt). Report every such run, whatever it prints.
- Seats never mutate the fleet repo (/home/vgpnk/Projects/shokunin), sibling lanes, lane production files (tools/, corpus/, SCORECARD.md, LOG.md, SKILL.md, README.md, PROVINCE.md …), lane jj state or the lane Git index. No git or jj write commands in the lane or fleet repo; read-only git (log/show/diff/status) is fine. Code experiments only in your scratch dir {SCR}/<YourName>/ (copy the gate there, or `git clone -q {LANE} <dir>` then `git -C <dir> checkout -q {TIP}`; unset GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE first). Set C1_TMP / C2_TMP / TMPDIR to your scratch dir; for c2-count-v3.py put any gate copy at <dir>/tools/research-gate.sh with C2_TMP outside <dir> (layout guard).
- Processes (QUALITY 39): never signal a process by name or pattern (no pkill, killall, `kill $(pgrep …)`); kill only PIDs/process groups you recorded, before you return.
- Disk: bound every fixture or log write; never point a MARKER, log or redirect at a file Python imports (sitecustomize.py, *.pth, usercustomize.py); check `df -h /fast` before anything large. Never run `du`/`find` over /fast/scratch except as /usr/bin/du on your own dir.
- Network: none, except an item that names a URL to open: GET only, that URL's host only, no redirect to another host, no credentials, no posting.
- Bound every command with `timeout` (<=1800 s for the gate selftest, <=900 s otherwise); cap memory/processes for anything heavy (`prlimit --nproc=2000 --as=4000000000`), no unbounded recursive test runs. Leaf seat: no subagents and no background jobs (an executor may spawn at most one read-only labrat probe).
- Honesty: report only what you ran or opened; quote command lines, exit codes and key output. Mark inference [INFERENCE]. A located quote is copied from the page you opened, <=25 words, with URL and access date 2026-10-23.
- Time box: return within 30 minutes of your start; a partial report with what you verified beats none.
# Tooling directive — operator, 2026-10-19 (always on, every agent)
You and every seat may install or update tools that help the task without asking; read /home/vgpnk/.omp/agent/RULES.md first and record each install (tool, version, channel, reason). All pacman transactions are PAUSED host-wide: never pacman -S/-Sy/-Syu/-U/-R, downgrade, or restart a host service; use uv tool / npx / an official binary in ~/.local/bin, or report the need. Prefer no installs.
# Output
Report at the trailer path: what you attacked, evidence (paths, commands, exit codes, inputs, outputs, receipt paths), verdict (HOLDS / BROKEN / INCONCLUSIVE) with reasons, limits. Return <=8 lines summarizing it.
"""

DIFF = f"`git -C {LANE} diff {BASE} {TIP} -- tools/research-gate.sh`"
PROBE = (f"Method: build input lines, run `bash {GATE} verify-claims <file> --root <dir>` on the LANDED gate and on the BASE gate "
         f"(`git -C {LANE} show {BASE}:tools/research-gate.sh > <scratch>/base-gate.sh`), and where useful on the python feasibility oracle {ORACLE}. "
         "Save every input and output in your directory.")


def item(name, role, text):
    return {"name": name, "role": role,
            "prompt": LEAD + "\n# Target\n" + text +
            "\n# Acceptance\nReport at the trailer path; artifacts only in your own directory; every claim backed by a command/output or path:line."}


ITEMS = [
    # ---------------- re-run counting commands
    ("RerunC1a", "executor", f"Attacks the C1 measurement: re-run `python3 {C1} --gate {GATE} --seed <n> --receipt …` on three fresh seeds of your choice; report each label and per-class line, gate_sha256 and counter_sha256 from each receipt, and whether P1 v2 holds on each."),
    ("RerunC1b", "executor", f"Attacks the C1 measurement under stress: re-run {C1} on the landed gate (a) with C1_TMP on tmpfs (/dev/shm/<your dir>, removed after), (b) under CPU load (4× `timeout 120 yes >/dev/null` you start and kill by recorded PID), (c) with LANG/LC_ALL set to a UTF-8 locale and to C. Receipt for every run."),
    ("RerunD1v3", "executor", f"Attacks the D1 repair: re-run `python3 {C2V3}` on the landed gate on two fresh seeds and on the exact round-32 metadata control ({LANE}/.ufo/waves/round-32/w2/CriticAxis32/metadata-control.sh, adapt only its counter path to v3) on two fresh seeds; also re-run the v2 counter on the same control to show the defect. Report labels; v3 must give landed 132/132 and the control below 132."),
    ("ReceiptCensus33", "executor", f"Attacks the kill rule: census every committed receipt under {LANE}/.ufo/waves/round-33 and {LANE}/corpus whose label starts TOPLEVEL_FIELD_MATCH (git ls-files + jq/python): group by counter_sha256 (v1 ab6b2ae2…, v2 cb354dd1…) and gate_sha256; list every receipt on a candidate/landed gate (52f07c74…, {GSHA[:8]}…) with its count. Any v2 receipt on those gates below 156 is a P1 miss — report it. Paste the counting command."),
    ("Chronology33", "reviewer", f"Attacks pre-data discipline: from `git -C {LANE} log --format='%H %cI %s' {BASE}..{TIP}` and receipt utc fields, show that design v1 (3b528b9a) and v2 (e3e24ec8) were committed before any candidate receipt, that every control receipt (w1/Ctl*, controls/L1-*) has utc before the first candidate receipt (measure/candidate/c1v2-s3351.json) and was committed in 96be7925 before the candidate commit eb179ec3, and that no counter or claims.md P1 text changed after 96be7925 (`git diff`). Report any violation."),
    ("ReviewControlReceipts33", "reviewer", f"Attacks the control re-score: for each receipt in {LANE}/.ufo/waves/round-33/controls/L1-v2-rescore/*.json, check gate_sha256 equals the sha256 of the control gate file it names under {W1}/<Seat>/<name>.sh (no receipt scored on a gate restored to base under a control name — the round-32 mistake), counter_sha256 = v2 (cb354dd1…), and that summary.txt matches the receipts. Also check each seat's own v1 receipts name mutated gate hashes. Report mismatches."),
    # ---------------- mutation tests of the landed gate
    ("MutC1GateDup", "mutation-tester", f"Mutation-test the duplicate handling in the landed gate's claim_scan / verify_claims ({DIFF}): mutants (a) no duplicate detection; (b) duplicates detected only for line/sha256; (c) dup id always prints id=line<N>; (d) agreeing duplicates accepted. For each: c1-count-v2 on two fresh seeds (receipts) and the selftest; report which detector kills it."),
    ("MutC1GateString", "mutation-tester", f"Mutation-test string handling in claim_scan ({DIFF}): mutants (a) backslash escapes ignored in strings (a backslash-quote ends the string); (b) escapes honoured in values but not in member names; (c) string state ignored inside nested values; (d) key comparison after JSON-unescaping. Counter (receipts) and selftest per mutant; report survivors."),
    ("MutC1GateDepth", "mutation-tester", f"Mutation-test nesting in claim_scan ({DIFF}): mutants (a) arrays not tracked; (b) mismatched-bracket check removed; (c) nested value skipped only one level deep; (d) the cache (JSON_SCAN_LINE) not reset per line (stale tables across records); (e) trailing-garbage check removed. Counter (receipts) and selftest per mutant; report survivors and which survivors violate the contract."),
    ("MutSelftest33", "mutation-tester", f"Attack the new selftest cases 242-248 (r33-top-*): for each, find a mutant of the landed gate it kills that the counter also kills, and list mutants the counter kills but the selftest misses (or vice versa). Use at most 8 mutants; counter receipts for each."),
    # ---------------- contract probes outside the counter
    ("ProbeNestedOnly33", "executor", f"Probe contract item 1 on inputs the counter never builds: required fields supplied ONLY by nesting (id, source, span or expect present only inside a nested object/array), a read member whose value is itself a container holding a same-named member (\"source\":{{\"source\":\"x\"}}), several decoy subtrees, depth 5+ nesting, empty containers. Expected: missing/invalid exactly as if the nested member were absent. {PROBE}"),
    ("ProbeTypes33", "executor", f"Probe top-level value types: non-string top-level id/source/span/expect/marker (number, true, null, array, object), empty strings, a top-level 'line' or 'sha256' that is a container, JSON numbers with exponent/negative/fraction as unknown members, true/false/null as unknown members. Compare landed vs base vs python oracle; any record whose landed verdict differs from the contract (claims.md) is a finding. {PROBE}"),
    ("ProbeWhitespace33", "executor", f"Probe JSON whitespace and line endings on FLAT valid records (contract item 4: flat records verify as at base): no spaces, spaces/tabs around ':' and ',', leading/trailing whitespace, CRLF line endings, a form feed or vertical tab between members (not JSON whitespace — what does each gate do?). Differential landed vs base on the same lines; any difference on valid JSON is a finding. {PROBE}"),
    ("ProbeEscapes33", "executor", f"Probe escapes in read-field VALUES on flat records: \\u escapes (BMP and surrogate pairs), \\/ , \\\\ , escaped quotes inside span/source/id, non-ASCII UTF-8 in spans, a key spelled with an escape (\"l\\u0069ne\"). Differential landed vs base: flat records must verify identically; report every difference. {PROBE}"),
    ("ProbeDupVariants33", "executor", f"Probe duplicates beyond the counter: three or more occurrences, a duplicated marker, an id duplicated with differing values, non-string duplicates (\"line\":5,\"line\":\"3\"), two different keys each duplicated, duplicates in marker_default rows, duplicated unread keys (\"claim\" twice — must stay valid). Check observed and the CLAIM_RECORD_INVALID finding text. {PROBE}"),
    ("ProbeMalformed33", "executor", f"Probe fail-closed parsing: unterminated strings, mismatched or unbalanced brackets inside nested values, bytes after the closing brace, two objects on one line, a bare word value, a trailing comma, an empty member name, a NUL or raw control character inside a string. Expected: CLAIM id=line<N> observed=invalid, never supported. Compare with python json.loads validity on each line. {PROBE}"),
    ("FuzzDiff33", "executor", f"Differential fuzz: generate at least 600 random VALID claim records (python, seeded; random nesting of objects/arrays up to depth 4 holding random subsets of the seven read keys; random member order; random whitespace; occasional top-level duplicates) over small source files, compute the contract verdict with your own python reference (json.loads with object_pairs_hook; duplicates of read keys -> invalid; reuse no gate code), and compare with the landed gate's observed per id. Report every disagreement with its minimal line. Bound runtime to 15 min."),
    ("ProbeLongLines33", "executor", f"Attack operability cost: time `verify-claims` on base vs landed gate for flat records whose span is 0.5, 4, 16 and 64 KiB (one record per file, and a 200-record file of 1 KiB records), C locale and UTF-8; report wall/CPU ratio landed/base and whether any run exceeds 60 s. Bound each run with timeout 300. ({W1}/ExecParserCost33.md measured the standalone walk.)"),
    ("NoHarmCorpus33", "executor", f"No-harm on real inputs: find every claims JSONL file committed in {LANE} (corpus/fixtures, corpus/evidence, .ufo/waves fixtures; `git ls-files '*.jsonl'` and files with one JSON object per line that verify-claims accepts) and run verify-claims on each with base and landed gates (same --root each time); compare stdout+exit. Every difference is listed and classified (expected by C1 contract or not)."),
    ("ProbeFlatBehaviour33", "executor", f"Probe contract item 4 (round-31/32 behaviour on flat records): build flat records with line+sha256 together, line ranges, multi-line spans, later-occurrence binding, expect=contradicted with top-level marker and marker_default rows, expect=unsupported, malformed line values, refused sources (absolute path, ../, URL). Differential base vs landed: report every difference."),
    ("ProbeMarkerDefault33", "executor", f"Probe marker_default rows (not counted): flat marker_default row, marker_default nested in an object, duplicated marker_default, a row with both id and marker_default, marker_default followed by contradicted claims. Base vs landed differential and what the knowledge entry {KNOW} says. {PROBE}"),
    # ---------------- reviews and adversarial reading
    ("ReviewC1Diff", "reviewer", f"Code review of {DIFF}: claim_scan correctness against RFC 8259 grammar for the claim-line subset, the duplicate path in verify_claims (id/expect/source display rules), the cache, locale handling, interaction with json_unescape and scan_secrets, error paths. Findings with severity and path:line; you may run small probes in scratch."),
    ("SentinelC1After", "sentinel", f"Security/robustness review of the landed claim reader on hostile claims files: deep nesting (10k brackets), a 1 MB line, 100k members, NUL bytes, invalid UTF-8, a line of only backslashes, key names with shell/glob metacharacters or `]`/`@`/`$(…)` (bash associative-array subscript hazards in JSON_PRESENT/JSON_STR), names like `__proto__`. Run bounded probes (timeout 120, prlimit) on the landed gate; report crashes, hangs, wrong verdicts, code execution."),
    ("CriticClaim33", "critic", f"Attack the C1 verdict and its §9 shape ({PROMPT} lines 343-365; {CLAIMS} Design v2): is P1 v2 the same sentence/condition/label; is v2 a legitimate pre-data redesign (timing: design v2 commit e3e24ec8 vs any candidate receipt); does any control meet 156; does the axis (operability, lowest scored) fit the surface; any universal clause left; is the claim re-scoring a rule already held? Verdict with reasons. Reasoning only, reading committed files."),
    ("CriticControls33", "critic", f"Attack the pre-data control wave as a whole: given the controls under {W1}/Ctl* and {LANE}/.ufo/waves/round-33/controls/, what cheap implementation that skips real top-level parsing could still reach 156/156 under v2 (e.g. keyed on the counter's fixed formatting `\": \"`/`\", \"`, on container shapes, on the fact that read values are always simple strings)? The label-keyed shortcut seat ended on a safety-filter hold; argue from the counter's code whether such a shortcut exists. Reasoning only."),
    ("ReopenS062", "scout", f"Re-open https://www.rfc-editor.org/rfc/rfc8259.txt (GET; host www.rfc-editor.org): check the S062 row in {LANE}/corpus/SOURCES.md (sha256, line numbers, quotes found with grep -cF) and every RFC quote and paraphrase in {KNOW} (is 'Other implementations report an error or fail to parse' on the page? does the entry over-read the RFC?). Verdict per quote."),
    ("ReopenS063", "scout", f"Re-open https://docs.python.org/3/library/json.html (GET; host docs.python.org): check the S063 row in {LANE}/corpus/SOURCES.md (sha256 and footer clock, the quote found once in tag-stripped text, its section) and the knowledge entry's Python sentence in {KNOW}. Verdict per quote; note any footer-clock variance."),
    ("ReviewKnowledge33", "reviewer", f"Review {KNOW} against the landed gate and evidence: every behavioural sentence (nested ignored, duplicates invalid incl. id display rule, malformed lines invalid, cost numbers, measured counts) — verify each by reading the gate and the cited receipts, or by a small probe. Also check it against {LANE}/corpus/QUALITY.md entry criteria. Findings with path:line."),
    ("ReviewQuality33", "reviewer", f"Run each check named in {LANE}/corpus/QUALITY.md criteria 36-39 exactly as written and confirm it fails on the cited failing evidence and passes on the cited passing evidence; report any check that cannot fail, cannot be run as written, or cites a wrong path/line."),
    ("ReviewD1Repair", "reviewer", f"Review the D1 repair: diff {LANE}/corpus/evidence/round32/c2-count-v2.py vs {C2V3}; confirm only fixture metadata/write order and receipt schema changed (classes, TOTAL, matching rule, label unchanged); audit with --keep on one seed that mtime/inode/name order of source files is independent of class. Report any change to what the counter measures."),
    ("MutD1Counter", "mutation-tester", f"Attack the D1 v3 counter's discrimination: re-score the round-32 C2 control gates that still exist under {LANE}/.ufo/waves/round-32/w1/CtlC2*/ and w2/*C2*/ (status-blind, weak readers, no-reader, noisy) with {C2V3} (two seeds each, gate copies laid out as <dir>/tools/research-gate.sh) and compare with their v2 scores; v3 must not admit any gate v2 rejected. Report a table."),
    ("ReviewRepairsD2D3D5", "reviewer", f"Re-run the repair checks: `python3 {LANE}/corpus/evidence/round33/d2-census.py --lane {LANE}` (expect 21 on 10f2fe12 and 3 on f4731885; verify by an independent jq command), the D3 header check from QUALITY 38 on both batteries, and `bash {LANE}/corpus/evidence/round33/no-name-signals.sh` on {LANE}/.ufo/waves/round-32 (expect exit 1) and on {LANE}/.ufo/waves/round-33/w1 (report hits and whether each is prose quoting the rule or a real signal by name)."),
    ("ScoutDocsAfter33", "scout", f"Read-only: list every text in {LANE} (SKILL.md, corpus/README.md, gate header/usage/comments, knowledge entries, SCORECARD planned items) that states claim-record parsing or the selftest count and say whether it matches the landed gate {GSHA[:8]} (248 selftest cases; top-level rule). Report stale or contradictory sentences with path:line."),
    ("CalibrationSkill33", "reviewer", f"Calibration check (self-description vs repo state): for each SKILL.md registry row touching research-gate (selftest counts, case ranges, counter rows) and SHONEN.md box pointers in {LANE}, run or open what it cites and count mismatches. Report the count, each mismatch with path:line, and the command used."),
]

spec = {
    "wave": "chousa-r33-w2",
    "milestone": "falsify C1 (verify-claims top-level field reader) on the landed gate; re-run counting commands; attack D1-D5 repairs, sources, knowledge and quality rows",
    "reportDir": ".ufo/waves/round-33/w2",
    "axes": ["operability"],
    "context": CONTEXT,
    "items": [item(*i) for i in ITEMS],
}
print(json.dumps(spec, indent=1, ensure_ascii=False))
print(dict(Counter(i[1] for i in ITEMS)), len(ITEMS), file=sys.stderr)
