#!/usr/bin/env python3
"""Generate .ufo/waves/round-61/w1-spec.json (chousa round 61, one v2 wave)."""
import json, pathlib, hashlib

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
W = f"{LANE}/.ufo/waves/round-61/w1"
CL = f"{LANE}/corpus/evidence/round61/claims.md"
EV = f"{LANE}/corpus/evidence/round61"
CTL = f"{EV}/controls"
FREEZE = "2b0e17b2a3b20a5f350e4dc4ddd5900c4d1f952c"
FIRST = "1661b85bfa84d3dc75712d64f79034265b8831d3"
BASE = "9eef15e7c0e0ae0055228e7066dc1eec676a91d2"
DIGEST = hashlib.sha256(pathlib.Path(CL).read_bytes()).hexdigest()
DIRECTIVE = pathlib.Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text().rstrip("\n")
SC = "/fast/scratch/hyaku/chousa-r61"

CONTEXT = f"""/skill:godspeed
Round 61 chousa, wave w1 (one v2 wave). Lane root {LANE}; every path you read or write is absolute under it. Frozen claims: {CL} (sha256 {DIGEST}), committed at lane revision {FREEZE} (amended once, before any seat existed, from first freeze {FIRST}; base {BASE}). Read the claims file first: two claims, C1 operability (span builder output safety, counter {EV}/c1-count.py) and C2 depth (sourced entry on derived-output safety, counter {EV}/c2-count.py), with controls in {CTL}/. The frozen predicates, counters, kill rules and controls are not yours to change: never edit anything under {EV}/, {LANE}/tools/, {LANE}/corpus/ or {LANE}/SKILL.md; the L1 integrates. Your only writes: your report at {W}/<your-name>.md and, when your item says so, candidate files under your own directory {W}/<your-name>/. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. No external live fetch or network use (fetch-scope L0 8d77e6c1 is open); no fleet, sibling-lane or shokuknow writes; no git, jj or index mutation anywhere (read-only git is fine, always `git -C {LANE} ...`). Fixture repos, if you need one: D=$(mktemp -d --tmpdir={SC}/<your-name>) && git -C "$D" init -q, and every later git call names -C "$D". Scratch exactly {SC}/<your-name>/ (create with mkdir -p; counters take it via --work and TMPDIR={SC}/<your-name>); delete it before you yield (trap rm -rf in shell, finally in Python); /tmp only for files under 50 MB and never as cited evidence. Use `python3 -B` for any script you run from the lane. Tooling: read /home/vgpnk/.omp/agent/RULES.md before installing anything; pacman is paused host-wide (no pacman, no partial upgrades); record any install (tool, version, channel, reason). Honesty: report only what you ran; an unrun check has not passed; cite commands with their output; mark inference as INFERENCE. Keep the report under 150 lines: findings first, evidence pointers (command and observed output), end with the one-line verdict your item names. L1 holds the planner seat and integration ownership; you are a leaf — no seat spawning, except that an executor may spawn one read-only labrat for one falsifiable probe. Seats never message agent://all."""

ITEMS = []


def add(name, role, body, verdict):
    prompt = "/skill:godspeed\n" + DIRECTIVE + "\n\n" + f"Item {name} ({role}). " + body + f" Final line of your report: `VERDICT: {verdict}`."
    ITEMS.append({"name": name, "role": role, "prompt": prompt})


COUNTER = f"python3 -B {EV}/c1-count.py --builder <builder> --work {SC}/<your-name>/w --seed <N>"

# ---- attack: C1 counter forgeries -------------------------------------------------------------
add("CritC1Sniff", "critic",
    f"Attack R61-C1 by test detection. Build, in your scratch, a copy of the BASE builder ({LANE}/tools/build-spans.py) that stays unhardened but tries to score 20/20 by detecting the counter: /proc/<ppid>/cmdline, the cwd name pattern, HOME, LANG, the directory layout (tools/ beside cache/, q.tsv), file names, the order of earlier runs. Run `{COUNTER}` at three seeds. Report LEGS reached, which sniff worked on which legs, and whether the frozen sweep `grep -nE 'getppid|/proc/|c1-count|round61|leg-|argv\\[0\\]' <builder>` would catch each sniff (claims.md A1). Do not edit the counter.",
    "FORGE_BEST=<k>/20 sniff_caught_by_sweep=<yes|no|partly>")
add("CritC1Seq", "critic",
    f"Attack R61-C1 by call-sequence inference under the amended shuffled order. Build a builder (copy of the base builder plus your forge) that records its invocations in shared state it can reach from a child process (/dev/shm, /tmp, the parent directory of its cwd, environment of the parent via /proc, file timestamps) and tries to infer which leg it is in. Measure the best score over 5 seeds; also test whether the two-name leg groups (P02/P03, H07/H08) or the repeated runs inside P04/P06 leave a fingerprint. Report the best LEGS and the exact information channel used.",
    "SEQ_FORGE_BEST=<k>/20 over 5 seeds")
add("CritC1Heuristic", "critic",
    f"List output-safety hazards the 20 legs do not cover and measure the reference builder ({CTL}/ref-build-spans.py, the landing candidate) against them. Build at least 8 fixtures yourself: the parent of --out itself a symlink; --out under a symlinked directory; a hardlinked span file to a victim; a cache directory whose name is a string prefix of a sibling (cache vs cache-evil) holding a symlinked capture; a leftover .tmp file from a crashed run in spans/; a spans.tsv with CRLF; read-only --out; ENOSPC (tmpfs of 1 MiB under {SC}/<your-name> if you can mount none, say so). For each: exit code, files touched outside the intended set, damage yes or no.",
    "UNCOVERED_HAZARDS_THAT_DAMAGE=<k> of <n>")
add("CritC1Detached", "critic",
    f"Attack the counter's process handling (claims.md A1). A builder grandchild can call os.setsid() and leave the process group the counter kills when the run ends; a builder can also fork a helper that survives its exit. Construct such builders in your scratch and determine whether any leg's verdict can be flipped from fail to pass by a post-exit mutation of the fixture before the counter's snapshot, or by the helper surviving into later legs. If no flip is possible, say so plainly: A1(2) is then hardening, not a demonstrated forge. Propose the smallest counter change; do not apply it.",
    "DETACHED_FLIP_POSSIBLE=<yes|no> legs=<list>")
add("CritC1Rss", "critic",
    f"Attack the memory leg of R61-C1 (H14 BIGTXT, H15 BIGRAW: peak RSS under 96 MiB measured by wait4 ru_maxrss of the child). Try to make a builder that really reads the 192 MiB capture yet reports a low ru_maxrss: reading in a waited helper process, mmap with MADV_DONTNEED, streaming in chunks and refusing at the end, reading from a detached helper. Decide which of these are legitimate (the capture is never held whole) and which are a measurement escape. Report the escapes with the exact peak RSS the counter saw.",
    "RSS_ESCAPES=<k> legitimate_streaming=<yes|no>")

# ---- attack: legs, group by group ------------------------------------------------------------------
LEG_GROUPS = [("RevC1LegsP1", "P01 TXT, P02 DOCX, P03 NOPYC"), ("RevC1LegsP2", "P04 CHECK, P05 REFUSEROW, P06 REBUILD"),
              ("RevC1LegsH1", "H07 FOREIGN, H08 REPLACE, H09 ORPHAN"), ("RevC1LegsH2", "H10 SPANSLINK, H11 FILELINK, H12 TSVLINK"),
              ("RevC1LegsH3", "H13 OUTSIDE, H14 BIGTXT, H15 BIGRAW"), ("RevC1LegsH4", "H16 OUTFILE, H17 UNREADABLE, H18 FIFO, H19 ENTRYDOT, H20 BIGFORM")]
for n, legs in LEG_GROUPS:
    add(n, "reviewer",
        f"Review the legs {legs} of {EV}/c1-count.py against the predicate in {CL}. (a) False negatives: write three different CORRECT builders (policies the counter docstring allows: refuse vs replace a link, different exit codes within the stated sets, different guard order) as copies of the reference {CTL}/ref-build-spans.py edited in your scratch, and run `{COUNTER}`; any correct builder that fails one of your legs is a counter defect. (b) False positives: write three INCORRECT builders that violate the leg's hazard but might pass; any that pass are a counter defect. Cite the counter line numbers. Do not edit the counter or the reference.",
        f"LEG_DEFECTS=<k> false_negative=<n> false_positive=<m> legs={legs}")

# ---- attack: mutation ------------------------------------------------------------------------------
MUT = [("MutC1ExtraProbe", "the `Forms._probe`, `Forms.get`, `Forms._read` and `_capture_text` code (commonpath vs startswith, `> MAX_CAPTURE` vs `>=`, the S_ISREG test, the head read, the dont_write_bytecode restore)"),
       ("MutC1ExtraWrite", "`guard_out`, `_atomic_write`, `write_out` (O_NOFOLLOW removal, O_EXCL removal, the order orphans are unlinked, the tmp file left behind on failure, mode 0o644, the `.tmp` name, writing the manifest before the span files)"),
       ("MutC1ExtraMain", "`read_quotes`, `build`, `check`, `main` (exit codes 1 vs 2, `--check` read errors, partial writes after a refusal, the `span == quote` refusal, memo reuse)"),
       ("MutC1ExtraDoc", "each behaviour sentence of the reference docstring (cap sizes, `.txt` newline handling, `--replace` semantics, exit-code list): mutate the code so the sentence becomes false and see whether the counter notices")]
for n, target in MUT:
    add(n, "mutation-tester",
        f"Mutation-test the reference builder {CTL}/ref-build-spans.py with at least 10 NEW mutants beyond the 14 frozen ones in {CTL}/run-c1-controls.py, aimed at {target}. Work on copies in your scratch; run `{COUNTER}` at seed 61001 for each (reference alone scores 20/20). Report a table: mutant, edit, legs failed, KILLED or SURVIVED. For each survivor say whether it is an equivalent mutant (behaviour unchanged) or a coverage gap in the counter, with the smallest fixture that would kill it.",
        "KILLED=<k>/<n> survivors_that_are_gaps=<g>")
add("MutC1Counter", "mutation-tester",
    f"Mutation-test the COUNTER {EV}/c1-count.py itself: in your scratch copy, apply at least 12 mutants (drop the RSS bound, drop the victim mtime comparison, drop the leaked-marker scan, accept any non-zero exit where exit 2 is required, skip the shuffle, skip a golden-tree equality, drop the NOPYC listing check, ...). Run each mutated counter against the base builder, the reference builder and the stub/mutant controls from {CTL}/run-c1-controls.py (point it at your copy through the script's COUNTER constant in a scratch copy). A mutated counter that still returns the original verdicts on every control is a gap in the control set. Report the table.",
    "COUNTER_MUTANTS_KILLED=<k>/<n> control_gaps=<g>")
add("MutC2Counter", "mutation-tester",
    f"Mutation-test {EV}/c2-count.py: in a scratch copy apply at least 10 mutants (drop the anchor check, drop the opened-date bound, drop the used-by check, drop the quote word cap, drop COVERAGE, drop the claim/quote overlap, drop the census call, resolve S136 to any file, ...). Run each against the control matrix of {CTL}/run-c2-controls.py (scratch copy pointing at your mutant) and report which mutants no control kills — each survivor is a missing control to name.",
    "COUNTER_MUTANTS_KILLED=<k>/<n> control_gaps=<g>")

# ---- attack: sentinel hazards beyond the legs ------------------------------------------------------
add("SentC1Race", "sentinel",
    f"TOCTOU review of the reference builder {CTL}/ref-build-spans.py: the guards test, then write. In a scratch copy, widen the window deterministically (a sleep or a hook between guard_out and the writes) and show what a second process that swaps `out/spans` for a symlink, or plants a symlinked span file, achieves. Report which writes escape, whether O_NOFOLLOW|O_EXCL on the temp file stops them, and what is the minimal further change (dir_fd/openat, or writing under a private temp dir and renaming) with its cost. The claims file already names this as limit (i); measure it, do not argue it.",
    "TOCTOU_ESCAPES=<k> fix=<one phrase>")
add("SentC1Fs", "sentinel",
    f"Filesystem-edge review of the reference builder {CTL}/ref-build-spans.py: --out on a read-only directory, a directory without search permission, a full filesystem (ENOSPC; use a small tmpfs only if you can create one without sudo-risk, otherwise RLIMIT_FSIZE), umask 077, an existing .tmp file with the same name pattern, an interrupted run (SIGKILL mid-write: what is left behind, can the next run recover), and spans/ holding thousands of files. Report exit code, leftovers and recoverability for each.",
    "FS_DEFECTS=<k> leftovers_unrecoverable=<n>")
add("SentC1Input", "sentinel",
    f"Input-edge review of the reference builder {CTL}/ref-build-spans.py: quotes with U+2028/U+0085/NUL, CRLF in the quotes file, BOM, duplicate rows, ids at the S### boundary (S000, S999, S1000), an entry cell with a Windows path or a dot-dot after normalisation, 100000 rows (the R55W2SentBuilder §5 cost), a cache directory with spaces or newlines in its path, a url with unicode. Report which inputs crash with a traceback, which hang, and which write something unexpected.",
    "INPUT_DEFECTS=<k> tracebacks=<n> hangs=<m>")

# ---- review: the reference diff ---------------------------------------------------------------------
DIFFS = [("RevRefDiffGuards", "`guard_out`, `_atomic_write`, `write_out` and the exit codes they return"),
         ("RevRefDiffForms", "`Forms._probe`, `Forms.get`, `Forms._read`, `_capture_text` and the caps"),
         ("RevRefDiffDoc", "the docstring: take every behaviour sentence and find the code line and the counter leg that makes it true, or say it has none")]
for n, what in DIFFS:
    add(n, "reviewer",
        f"Line-by-line review of the diff between the base builder {LANE}/tools/build-spans.py and the landing candidate {CTL}/ref-build-spans.py (`diff -u` them), scoped to {what}. Check correctness, error paths, Python 3.14 semantics (os.replace on a symlink, commonpath on realpaths, pathlib is_symlink on dangling links), behaviour changes the old callers could observe (round 45-57 per-round builders are separate files; `corpus/evidence/round61/regress.py` runs the three real sets). Report defects with line numbers and a reproduction each.",
        "REF_DEFECTS=<k> blocking=<n>")

# ---- review: C2 claims -------------------------------------------------------------------------------
CLAIMS_TXT = f"{CTL}/c2-positive-entry.md"
for i in range(1, 6):
    add(f"RevC2Claim{i}", "reviewer",
        f"Entailment review of Claim {i} of the candidate entry {CLAIMS_TXT} (the entry the counter's positive control uses; it is also the landing candidate). Re-open the quotes it cites yourself: render `MANWIDTH=1000 man -l /usr/share/man/man2/open.2.gz | col -bx` (rename.2.gz for S135; the S136 file is {LANE}/.ufo/waves/round-56/w1/R55W2SentBuilder.md) and locate each quote in full context, reading the surrounding paragraph. Decide: does the claim follow from the quote and its context (supported), go beyond it (overreach), or misread it? Propose a rewrite for anything not supported. A quote that is present but taken out of its context is a finding.",
        f"CLAIM{i}=<supported|overreach|misread> rewrite_needed=<yes|no>")
add("CritC2Forge", "critic",
    f"Attack R61-C2 ({EV}/c2-count.py): produce entries that reach C2=PASS in a scratch mirror of the lane (see {CTL}/run-c2-controls.py for how a mirror is prepared; copy `corpus/` once) while being wrong or empty: claims that echo quotes (the counter admits this), a source cell for S136 naming the entry itself or the claims file so the entry quotes itself, a PATH shim that supplies a fake `man` or `col`, MANWIDTH/LC variants, quotes that match only because of whitespace normalisation across a section boundary. Report each forge with its output and the smallest counter or freeze addition that would catch it.",
    "C2_FORGES_REACHING_PASS=<k> named_in_claims=<n>")
add("CritC2Quotes", "critic",
    f"Attack the quotes of {CLAIMS_TXT}: for each of Q1-Q8 find a reading under which the quote, in its page context, does NOT support what the row's `teaches` cell and the entry's claims say (hedges, scope limits, kernel-version qualifiers, `until Linux x.y` clauses, the FreeBSD/POSIX remarks). Check also that Q3's `symbolic links are not followed` belongs to the O_CREAT|O_EXCL paragraph and not to O_PATH or another flag. Report per quote: scope sentence that limits it, or none.",
    "QUOTES_WITH_UNSTATED_LIMIT=<k> of 8")

# ---- review: province, streak, quality ------------------------------------------------------------
add("RevProvince", "reviewer",
    f"Province review (PROVINCE.md at {LANE}/PROVINCE.md and SKILL.md Boundaries): is hardening a span builder's output directory and an entry on symlink/rename semantics inside chousa's province (the lane's own corpus and gates), or does it belong to a sibling (kumitate: orchestration tooling; tsukuroi: host hardening; mori/souji)? Read the sibling PROVINCE.md files at /home/vgpnk/Projects/shokunin/<lane>-shokunin/PROVINCE.md read-only. Report any overlap with the evidence, and what adjacency line the report must carry.",
    "PROVINCE=<in|contested|out> contested_with=<lane or none>")
add("RevStreak", "reviewer",
    f"Verify a recurring-weakness table. Claim to check: a frozen counter was reachable, forgeable or unreachable in rounds 49, 50, 51, 52 (C1 supplement), 56, 57 (C3 provenance forge), 58, 59 (token injection), 60 and was pre-freeze controlled in round 61. For each round open the lane lesson and spot-check/report evidence ({LANE}/corpus/lessons/round-N.md, round-N-verifier-spotcheck.md, .ufo/reports via /home/vgpnk/Projects/shokunin/.ufo/reports/round-N/chousa.md) and mark the class (reachable by do-nothing / forgeable / unreachable / none) with a pointer. Source of the proposal: {LANE}/considerthese/2026-10-26.md ('Track recurring weaknesses as streaks').",
    "STREAK_ROWS_CONFIRMED=<k>/10 corrected=<c>")
for n, what in [("RevQualityA", "a criterion requiring a pre-freeze control matrix (base, do-nothing stubs, token forger, naive guard, positive control reaching the target, frozen mutants) before a counter binds data; its shown-able-to-fail check is the round-58/60 counters"),
                ("RevQualityB", "a criterion requiring seeded shuffled leg order and process-group-bounded child runs in any counter that runs a candidate tool; its red-before is a call-counting forge scoring 20/20 on the first-freeze counter ({FIRST}) and lower on the amended one")]:
    add(n, "reviewer",
        f"Draft and then attack one new QUALITY.md criterion for {LANE}/corpus/QUALITY.md (criteria 1-118 exist; read the Round-56..59 additions for format: numbered, rationale with lesson evidence, a Check line, a Shown-able-to-fail line): {what.replace('{FIRST}', FIRST)}. Write the draft text in your report, run its Check command on the real evidence and on a red-before state, and report whether the check can fail for the named reason. Do not edit QUALITY.md.",
        "CRITERION_CHECK_CAN_FAIL=<yes|no> text_ready=<yes|no>")

# ---- executors -----------------------------------------------------------------------------------------
for i, pol in [(1, "refuse every link and any differing existing output (strict)"), (2, "replace a link at a span or manifest path with a regular file instead of refusing, refuse only a symlinked spans directory and a differing manifest"), (3, "the smallest diff from the base builder that makes the counter pass")]:
    add(f"ExecIndepBuilder{i}", "executor",
        f"Reachability by an independent implementer. WITHOUT reading {CTL}/ref-build-spans.py (do not open it), read only the docstring of {EV}/c1-count.py and the base builder {LANE}/tools/build-spans.py, and write a hardened builder at {W}/ExecIndepBuilder{i}/build-spans.py following this policy: {pol}. Run `{COUNTER}` at three seeds and `python3 -B {EV}/regress.py --builder <yours> --work {SC}/<your-name>/rg`. Report LEGS at each seed, REAL_REBUILD, the legs you first failed and why, and every place the counter docstring was ambiguous.",
        f"INDEP{i}_LEGS=<k>/20 REAL_REBUILD=<j>/3 ambiguities=<n>")
add("ExecForgeSeqRed", "executor",
    f"Red-before for amendment A1 (a fix counts only once shown able to fail). Extract the FIRST-freeze counter: `git -C {LANE} show {FIRST}:corpus/evidence/round61/c1-count.py > {SC}/<your-name>/c1-first.py` (its HERE/LANE paths resolve from its own location, so copy it to {SC}/<your-name>/tree/corpus/evidence/round61/c1-first.py and symlink or copy {LANE}/tools/capture-text.py to {SC}/<your-name>/tree/tools/). Write a call-counting forge builder that scores 20/20 on that first-freeze counter without implementing the guards (the leg order was fixed: P01, P02, P04, P05, P06, H07, ...), then run the SAME forge on the amended counter {EV}/c1-count.py at five seeds. Report both scores; the red-before is met when the first-freeze counter is forged to 20/20 and the amended one is not.",
    "FIRST_FREEZE_FORGED=<k>/20 AMENDED=<min>-<max>/20 over 5 seeds")
add("ExecForgeProcgroup", "executor",
    f"Probe for amendment A1 part (2) and (3): against the FIRST-freeze counter (`git -C {LANE} show {FIRST}:corpus/evidence/round61/c1-count.py`, run from a scratch tree as in ExecForgeSeqRed's recipe) build (a) a builder whose child daemonises and keeps writing after the builder exits, (b) a builder that floods stderr with 2 GiB and stdout likewise. Report whether the first-freeze counter's verdicts can be flipped or the host harmed (watch disk and memory; stop at 1 GiB written under {SC}/<your-name>), and what the amended counter does with the same builders.",
    "FIRST_FREEZE_FLIPPED=<yes|no> flood_harm=<none|...> amended_ok=<yes|no>")
add("ExecRegressSets", "executor",
    f"Real-data no-harm run. `python3 -B {EV}/regress.py --builder {CTL}/ref-build-spans.py --work {SC}/<your-name>/a` and the same for the base builder; then extend by hand to every committed span set under {LANE}/corpus/evidence/round4x..round57 whose quotes.tsv and captures resolve in the lane-owned store {LANE}/corpus/captures (find them with find; skip the ones needing the deleted campaign cache and list the skip reasons): `--check` and a fresh build into scratch, byte-compare with the committed spans. Report counts per set.",
    "REGRESS_SETS_CHECKED=<n> identical=<k> skipped=<s>")
add("ExecRegressRows", "executor",
    f"Differential run: choose 40 random (id, url, quote) rows from the committed quotes.tsv files of rounds 55-57 whose captures are in {LANE}/corpus/captures, write them as quotes tables of 5-10 rows, and build each with the base builder and with the reference ({CTL}/ref-build-spans.py) into separate empty scratch outputs; the two output trees must be byte-identical (spans.tsv, spans/*, stdout). Include rows on `.raw` zip/OLE captures and `.txt` captures. Report the number of tables built and any difference.",
    "TABLES=<n> DIFFERENT=<k>")
add("ExecPerf", "executor",
    f"Performance no-harm: time and peak-RSS (use /usr/bin/time -v or resource.wait4) the base builder and the reference ({CTL}/ref-build-spans.py) on the three real sets (round 55, 56, 57/c3: quotes.tsv with --cache {LANE}/corpus/captures) and on a synthetic 5000-row table over one 1 MiB capture; five runs each, median. Report the ratio ref/base for wall time and RSS; flag any ratio above 1.25.",
    "WALL_RATIO=<x> RSS_RATIO=<y>")
for tag, seeds in [("A", "7101 7102 7103"), ("B", "7104 7105 7106"), ("C", "7107 7108 7109 7110")]:
    add(f"ExecReproC1{tag}", "executor",
        f"Independent measurement of C1. Run `{COUNTER}` for the base builder {LANE}/tools/build-spans.py and for the reference {CTL}/ref-build-spans.py at seeds {seeds} (fresh --work each). While your runs go, load the host with a parallel `python3 -c` busy loop on two cores for one of the seeds to see whether any leg (RSS, timeouts) is load-sensitive. Report per seed LEGS and failing legs for both builders, and any leg whose verdict changed between runs of the same seed.",
        "BASE=<min>-<max>/20 REF=<min>-<max>/20 flaky_legs=<list or none>")
add("ExecReproC2", "executor",
    f"Independent measurement of C2. Prepare a scratch mirror as {CTL}/run-c2-controls.py does (copy `corpus/` once; insert {CTL}/c2-positive-rows.txt into the registry; put {CTL}/c2-positive-entry.md at corpus/knowledge/derived-output-safety-r61.md; copy the S136 file) and run `python3 -B {EV}/c2-count.py --root <mirror>`. Repeat under MANWIDTH=80 and MANWIDTH=1000 in the caller environment, LANG=C and LANG=C.UTF-8, and with `man` resolved from a different PATH order; report whether the verdict ever changes. Run {CTL}/run-c2-controls.py once and report its summary line.",
    "C2_VERDICT_STABLE=<yes|no> controls_unexpected=<k>")
add("ExecFreezeCheck", "executor",
    f"Build the check that would have caught round 60's frozen-digest mismatch and round 59's spec rewrite (lessons {LANE}/corpus/lessons/round-59.md and round-60.md Mistakes; QUALITY 116 and 118). Write {W}/ExecFreezeCheck/freeze-check.py: `freeze-check.py --claims <file> --dispatch <w1-dispatch.json> --spec <w1-spec.json> --ready <w1.ready>` exits 0 only when the claims file is nonempty, its sha256 appears in the dispatch taskCall.context, no other 64-hex digest-looking token in any item prompt differs from it, every dispatch task body equals the corresponding spec item body after the validator's rendering rules you infer from a real pair (round 59: {LANE}/.ufo/waves/round-59/w1-spec.json and w1-dispatch.json; round 60 likewise), and the ready JSON names an existing dispatch file with a matching lane/round/wave. Include `--selftest` with red-before fixtures built from the real round-60 pair (claim digest 65721569... versus prompt 09d8053f...) that exit 1 for the named reason, and a green fixture that exits 0. Write no files outside your directories; never /tmp for evidence.",
    "FREEZE_CHECK=<selftest k/n pass> red_before_exit=<code>")

# ---- scouts ------------------------------------------------------------------------------------------------
add("ScoutC2ManPages", "scout",
    f"Re-open the sources of S134/S135 (rows are in {CTL}/c2-positive-rows.txt): render `MANWIDTH=1000 man -l /usr/share/man/man2/open.2.gz | col -bx` and rename.2.gz, read the unrendered roff (`zcat`) too, and for each of Q1-Q6 of {CTL}/c2-positive-entry.md report line numbers in both forms, whether `col -bx` or whitespace normalisation changed the text (hyphenation, bold overstrike, list indentation), and the section heading the quote sits under. Add up to four further quotes of at most 25 words that would strengthen the entry, with their locations.",
    "Q1_Q6_LOCATED=<k>/6 extra_quotes=<n>")
add("ScoutC2Package", "scout",
    f"Provenance of the installed pages: `pacman -Qi man-pages`, `pacman -Ql man-pages | grep -E 'man2/(open|rename)\\.2'`, `pacman -Qo /usr/share/man/man2/open.2.gz`, `man -w 2 open`, `man --path`, any earlier MANPATH entry that could shadow the page (/usr/local/share/man, ~/.local/share/man), the `.TH` line of both pages, and the package install date. Report whether the rendered text of the cited paragraphs is the package's text or a shadow, and write the one-line access disclosure the registry rows and the lesson Gate should carry.",
    "PAGES_ARE_PACKAGE_COPIES=<yes|no> version=<x>")
add("ScoutC2RowsCensus", "scout",
    f"Validate the four candidate rows {CTL}/c2-positive-rows.txt against the contract in /home/vgpnk/Projects/shokunin/CORPUS.md (section SOURCES.md): column count, id uniqueness, kind/tier/status enums, ISO dates, recheck cadences (`on-release`, `180d`), used-by paths, the rejected-row wording `REJECTED: <reason>; flip: <condition>`. Build a scratch registry copy with the rows inserted and run `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <copy>` from a scratch lane tree (cwd = the lane root copy, as the counter does) and the manual census awk lines from CORPUS.md. Report the expected before/after census: rows, tier histogram, status histogram, W-codes.",
    "CENSUS_EXIT=<0|n> rows=<before>-><after> findings=<none|list>")
add("ScoutC2RowsScope", "scout",
    f"Registry-fit review of the four candidate rows: do their `scope` cells claim more than the source supports (tier A is per scope)? Is S136 (a seat report) honestly tier B and S137 (a docstring) honestly C and rejected? Is any row a near-duplicate of an existing row (`grep -n 'R55W2SentBuilder\\|build-spans' {LANE}/corpus/SOURCES.md`, and own-work rows citing builder or gate output)? Check E04 URL duplication risk (none of the new rows carries a URL). Report edits you would make to each row cell, as replacement text.",
    "ROWS_NEEDING_EDIT=<k>/4")
add("ScoutMistakesPrior", "scout",
    f"Mine mistakes from rounds 58-60 for the round-61 lesson's `## Mistakes` (format in {LANE}/corpus/lessons/round-60.md: class, evidence pointer, captured-by, fix, shown-able-to-fail; classes from /home/vgpnk/Projects/shokunin/CORPUS.md). Read the lessons and verifier spot-checks of rounds 58, 59, 60, QUALITY.md 115-118, and the round-60 routed defects. List every distinct mistake with the QUALITY criterion that should have caught it or `none`, and say which have a real fix landed (with a command that fails on the pre-fix state) and which only have a sentence.",
    "MISTAKES=<n> uncaught=<k> fixed_with_red_before=<j>")
add("ScoutMistakesThisRound", "scout",
    f"Mine this round's own pre-freeze mistakes for the lesson: read {CL} (Amendment A1) and the git history of {EV} (`git -C {LANE} log --stat {BASE}..{FREEZE} -- corpus/evidence/round61`, `git -C {LANE} show {FIRST}:corpus/evidence/round61/c1-count.py`), find every defect of the first-frozen counter and controls that the amendment fixed or left (count the claims-file statements that no longer match the files: digests, leg counts, receipts), and the misroot sweep: `git -C /home/vgpnk/Projects/shokunin status --porcelain` for any file a round-61 seat or the L1 wrote at the fleet root. Report rows in the lesson format.",
    "THIS_ROUND_MISTAKES=<n> stale_claim_statements=<k> misroot_files=<m>")
add("ScoutSpotcheckPrior", "scout",
    f"Status of the round-60 closure's routed defects ({LANE}/corpus/lessons/round-60-verifier-spotcheck.md, section Routed defects): for each of the four items say what the round-61 freeze did about it with a pointer (claims.md section, file, commit), what remains open, and what the report must say (e.g. restoring the exact headings `## Sources & frontier` and `## Trend verdicts`). Also check the round-60 report at /home/vgpnk/Projects/shokunin/.ufo/reports/round-60/chousa.md for its section headings against the contract in /home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-61.md section 4.",
    "ROUTED_DEFECTS_ADDRESSED=<k>/4 open=<list>")
add("ScoutConsiderthese", "scout",
    f"Mine {LANE}/considerthese/ for ONE still-unimplemented proposal this round could land as a lesson, QUALITY criterion or registry row (contract: /home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-61.md section 10; the reflection is a pointer, not evidence — open what it points at). Read the latest file 2026-10-26.md and scan 2026-10-19..25 for proposals; grep the lane for each candidate to see whether it was implemented (`grep -rn` with the sweep command recorded). Recommend one, with the evidence you opened, and name the two you rejected with reasons.",
    "RECOMMENDED=<proposal title> implemented_check=<command>")
add("ScoutCensusCounts", "scout",
    f"Pre-compute the census the report must paste. At lane revision {FREEZE}: run `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` (record rows, tiers, statuses via the manual awk lines in /home/vgpnk/Projects/shokunin/CORPUS.md, W04 list) and the counting commands for knowledge entries (`find {LANE}/corpus/knowledge -name '*.md' | wc -l`, entries with `recheck:`), and project the expected after-values if rows S134-S137 and one entry are added (A 106->108, B 22->23, C 5->6; mined +3, rejected +1). Report a table the L1 can compare with the real after-census.",
    "BEFORE_ROWS=<n> PROJECTED_AFTER=<n>")

# ---- scribes -------------------------------------------------------------------------------------------------
for i, stance in [(1, "a practitioner's checklist: what a tool author does, in order, when writing derived files into a caller-named directory"), (2, "a decision table: hazard, what Linux does, what the tool must test, which counter leg shows it"), (3, "a compact reference: three principles with their quotes, then the limits")]:
    add(f"ScribeC2Entry{i}", "scribe",
        f"Draft an independent candidate for the knowledge entry corpus/knowledge/derived-output-safety-r61.md in the shape the counter {EV}/c2-count.py reads (read its docstring), as {stance}. Re-open S134/S135 (rendered man pages: `MANWIDTH=1000 man -l FILE | col -bx`) and the S136 file yourself and use quotes you located; keep ids S134, S135, S136; the registry rows to assume are in {CTL}/c2-positive-rows.txt. Prepare a scratch mirror as {CTL}/run-c2-controls.py does, put your draft in it and run `python3 -B {EV}/c2-count.py --root <mirror>`; deliver your draft at {W}/ScribeC2Entry{i}/entry.md and the counter's output line. The L1 will compare the three drafts and the positive control {CTL}/c2-positive-entry.md and merge. Keep claims no stronger than their quotes.",
        f"ENTRY{i}_C2=<PASS|FAIL> quotes=<k> claims=<n>")
add("ScribeGate", "scribe",
    f"Draft the `## Gate` section of corpus/lessons/round-61.md for the four new registry rows S134-S137 ({CTL}/c2-positive-rows.txt): for every row the URL or path, the access date 2026-10-28, a located quote of at most 25 words with its location grounding `teaches`, and the admit or reject decision with reason (S137 is a rejection with a flip condition). Re-open each source yourself before writing it (the man pages by rendering, the lane files by path and line) and give the line numbers. End with the spot-check request: name one admit and one reject for a non-author to re-open. Deliver at {W}/ScribeGate/gate.md.",
    "GATE_ROWS_WRITTEN=<k>/4 quotes_reopened=<n>")
add("ScribeStreak", "scribe",
    f"Draft the lesson text for one considerthese proposal, 'Track recurring weaknesses as streaks' ({LANE}/considerthese/2026-10-26.md): a short table of the frozen-counter weakness by round with the class, an evidence pointer per row and whether a fix with a red-before state landed, from the lessons and spot-checks of rounds 49-61. Open every pointer you cite. Deliver at {W}/ScribeStreak/streak.md; the RevStreak seat will verify your rows, so mark every row you could not open.",
    "STREAK_ROWS=<n> unopened=<k>")
add("ScribeLogDraft", "scribe",
    f"Draft, from the frozen facts only and with the measured AFTER values left as the literal marker <AFTER> for the L1 to fill, the text of: the round-61 LOG.md entry ({LANE}/LOG.md — read its last entry for format), the SCORECARD.md round-61 verdict block (read the round-58/60 blocks; keep the numeric operability 3/10 unchanged and say so), and the corpus/README.md coverage-map row and Frontier paragraph for the new entry (read the Round56/57 sections for the format). Deliver at {W}/ScribeLogDraft/draft.md; write nothing into the lane files.",
    "DRAFT_SECTIONS=<n> after_markers=<k>")

# ---- connectors ------------------------------------------------------------------------------------------------
add("ConnSiblingOverlap", "connector",
    f"Sibling-overlap scan: does any sibling lane already hold knowledge on symlink-safe or atomic file writing, output-directory hardening or manual-page-sourced OS semantics, or own a builder/counter for it? Search /home/vgpnk/Projects/shokunin/<lane>-shokunin/{{PROVINCE.md,corpus/knowledge,corpus/SOURCES.md}} read-only with recorded grep commands (symlink, O_NOFOLLOW, rename(2), atomic, os.replace, TOCTOU). Report the overlaps with paths, and whether the new entry duplicates, contradicts or complements them.",
    "SIBLING_OVERLAPS=<k> contested=<lane or none>")
add("ConnClaimTrace", "connector",
    f"Cross-claim trace: map each hazard of the R55W2SentBuilder transcript ({LANE}/.ufo/waves/round-56/w1/R55W2SentBuilder.md cases h1-h11) to (a) the counter leg that detects it ({EV}/c1-count.py), (b) the reference builder guard that handles it, (c) the entry claim or limit that explains why ({CTL}/c2-positive-entry.md). Report a table and every hazard with no leg, no guard or no explanation.",
    "HAZARDS_FULLY_TRACED=<k>/<n>")

# --- assemble ---------------------------------------------------------------------------------------------------
spec = {"wave": "chousa-r61-w1", "reportDir": ".ufo/waves/round-61/w1", "items": ITEMS, "context": CONTEXT,
        "axes": ["operability", "depth", "calibration"]}
out = pathlib.Path(LANE) / ".ufo/waves/round-61/w1-spec.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
from collections import Counter
print(len(ITEMS), dict(Counter(i["role"] for i in ITEMS)), "claims sha256", DIGEST)
