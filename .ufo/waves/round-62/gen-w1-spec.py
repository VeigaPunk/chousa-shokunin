#!/usr/bin/env python3
"""Generate .ufo/waves/round-62/w1-spec.json (chousa round 62, one v2 wave of 64 seats)."""
import json
import hashlib
import pathlib
import sys
from collections import Counter

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
W = f"{LANE}/.ufo/waves/round-62/w1"
EV = f"{LANE}/corpus/evidence/round62"
CTL = f"{EV}/controls"
CL = f"{EV}/claims.md"
BASE = "8607de84723d5ff9bbcbe71eedebd6a0d30bfd87"
FREEZE = sys.argv[1] if len(sys.argv) > 1 else "<FREEZE>"
DIGEST = hashlib.sha256(pathlib.Path(CL).read_bytes()).hexdigest()
DIRECTIVE = pathlib.Path("/home/vgpnk/.agents/skills/godspeed/directive.md").read_text().rstrip("\n")
SC = "/fast/scratch/hyaku/chousa-r62"

CONTEXT = f"""/skill:godspeed
Round 62 chousa, wave w1 (one v2 wave). Lane root {LANE}; every path you read or write is absolute under it. Frozen claims: {CL} (sha256 {DIGEST}), committed at lane revision {FREEZE} (base {BASE}). Read the claims file first: two claims, C1 operability (a counter that tells a hardened span builder from a forger: counter {EV}/c1v2-count.py, battery {EV}/c1v2-battery.py) and C2 coverage, sourced (entry on openat2 kernel path resolution: counter {EV}/c2v2-count.py, probe candidate {CTL}/candidate-openat2-probe.py), with controls in {CTL}/. The frozen predicates, counters, battery, kill rules and controls are not yours to change: never edit anything under {EV}/, {LANE}/tools/, {LANE}/corpus/ or {LANE}/SKILL.md; the L1 integrates. Your only writes: your report at {W}/<your-name>.md and, when your item says so, candidate files under your own directory {W}/<your-name>/. Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>. No external live fetch or network use (fetch-scope L0 8d77e6c1 is open); no fleet, sibling-lane or shokuknow writes; no git, jj or index mutation anywhere (read-only git is fine, always `git -C {LANE} ...`). Fixture repos, if you need one: D=$(mktemp -d --tmpdir={SC}/<your-name>) && git -C "$D" init -q, and every later git call names -C "$D". Scratch exactly {SC}/<your-name>/ (create with mkdir -p; counters take it via --work and TMPDIR={SC}/<your-name>); delete it before you yield (trap rm -rf in shell, finally in Python); /tmp only for files under 50 MB and never as cited evidence. Use `python3 -B` for any script you run from the lane. Tooling authorization (operator, 2026-10-19): you and every seat may install or upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md (official channels, update-safety gate; record tool/version/channel/reason). pacman guard: all pacman transactions are paused host-wide (no pacman, no -Sy/-Syu/-U/-R, no partial upgrades); install via uv tool, npx or an official binary in ~/.local/bin, or report the need. Honesty: report only what you ran; an unrun check has not passed; cite commands with their output; mark inference as INFERENCE. Keep the report under 150 lines: findings first, evidence pointers (command and observed output), end with the one-line verdict your item names. L1 holds the planner seat and integration ownership; you are a leaf — no seat spawning, except that an executor may spawn one read-only labrat for one falsifiable probe. Seats never message agent://all."""

ITEMS = []


def add(name, role, body, verdict):
    prompt = "/skill:godspeed\n" + DIRECTIVE + "\n\n" + f"Item {name} ({role}). " + body + f" Final line of your report: `VERDICT: {verdict}`."
    ITEMS.append({"name": name, "role": role, "prompt": prompt})


C1 = f"C1V2_SEED=<N> python3 -B {EV}/c1v2-count.py --builder <builder> --work {SC}/<your-name>/w"
BAT = f"python3 -B {EV}/c1v2-battery.py --counter <counter> --work {SC}/<your-name>/b"
R61 = f"{LANE}/corpus/evidence/round61"
LANDED = f"{LANE}/tools/build-spans.py"
BASEB = f"{CTL}/base-build-spans.py"

# ---- attack: new forgers against the v2 counter (named-limit classes first) -----------------------------------
add("CritC1Ns", "critic",
    f"Attack R62-C1 by sandbox detection. Write in your scratch a forger (landing builder {LANDED} when its test fires, the unhardened base {BASEB} otherwise, wrapped as in {EV}/c1v2-battery.py TEMPLATE) whose test detects the PID namespace: `NSpid` in /proc/self/status with two or more ids, `os.getpid() == 1`, `/proc/1/cmdline`, the mount namespace id. Run `{BAT}` with `--only` for your forger and `{C1}` on it at three seeds. Report whether v2 accepts it (the claims name this as an open limit) and what the smallest counter change would be that stops it without making the sandbox itself the signal (e.g. run the builder as pid>1 under a shim init, nest namespaces, randomise pids). Do not edit the counter.",
    "NS_FORGER_ACCEPTED=<yes|no> best=<k>/20")
add("CritC1Content", "critic",
    f"Attack R62-C1 by content detection: a forger that recognises the counter's fixtures by what is in them (the `S###` id shape with ids 100-899, the quote vocabulary `chain`/`anchor`/Chinese tokens, quote length, `capture-text.py` beside the builder, capture file names that are 24 hex digits, the `corpus/knowledge/x.md` entry cell, span context 80). Build three such forgers in scratch from the TEMPLATE in {EV}/c1v2-battery.py, run `{C1}` on each at three seeds, report LEGS and which sniff worked. Say which could be defeated by the counter (more varied vocabulary, real-looking entries) and which are indistinguishable from real data (then it is a named limit).",
    "CONTENT_FORGE_BEST=<k>/20 defeatable=<n>")
add("CritC1Timing", "critic",
    f"Attack R62-C1 with a builder that cooperates with the counter's own timing and ordering: counts its invocations in the environment it can reach (PID counter in the namespace, /proc/uptime, the fixture mtimes, file-system state it creates outside the fixture such as under /dev/shm or the parent of its cwd), sleeps past the 60 s timeout on suspicion, or behaves differently on the first call per profile. The counter shuffles legs and runs profiles in random order from an environment seed. Build two builders, run `{C1}` at five seeds, report the best LEGS and whether any leg verdict flips between runs of the same seed.",
    "TIMING_FORGE_BEST=<k>/20 over 5 seeds")
add("CritC1Shm", "critic",
    f"Attack the memory legs H14 and H15 under the v2 counter (RLIMIT_AS 200 MiB, namespace, ru_maxrss of the waited tree). Try: a detached helper reading the 192 MiB capture (the namespace reaps it; AS limit bounds it), a memfd/shm staging copy under the AS limit, mmap with MADV_DONTNEED, streaming in chunks and refusing at the end, a helper that never exits within the 60 s timeout. For each: counter H14/H15 verdict, the independent peak (VmHWM, /proc/meminfo Shmem), and whether it is a legitimate streaming reader or an escape. The claims name shared-memory retention and detached readers as limits; measure how far each reaches. Use {R61}/c1-count.py's legs as reference; do not edit the counter.",
    "RSS_ESCAPES_UNDER_V2=<k> legitimate_streaming=<yes|no>")
add("CritC1Detached", "critic",
    f"Attack the v2 sandbox against escape: a builder that tries to leave or survive the PID namespace (setsid, double fork, PR_SET_PDEATHSIG races, prctl subreaper, unshare nested namespaces, writing to /proc/sys, kill -9 of pid -1, opening the counter's work directory by walking .. from its cwd, reading other fixtures' names), and builders that mutate the fixture tree after exit via a helper born before exit. Replicate round 61's CritC1Detached routes ({LANE}/.ufo/waves/round-61/w1/CritC1Detached.md: pyc cleaner, symlink-victim restore, daemon poller) against v2 and report which still flip a leg. F12 of {EV}/c1v2-battery.py is the cleaner.",
    "V2_ESCAPE_FLIPS=<k> legs=<list>")
add("CritC1Sandbox", "critic",
    f"Attack the claim that `unshare -Ufp --kill-child --mount-proc` is safe and portable as the counter's sandbox. Check: files the builder can reach outside the fixture (host / is still mounted: can it read the lane, other fixtures, /home?), whether it can write outside, uid mapping effects on the mode-000 leg H17 and the FIFO leg, kernel.unprivileged_userns_clone / max_user_namespaces / apparmor restrictions (the counter fails closed with exit 2: show it, e.g. by a PATH without unshare or `unshare` replaced by a script that exits 1), behaviour as root, inside a container, and when /proc is mounted nosuid. Report which environments make the counter exit 2 vs give a wrong verdict. Do not edit the counter.",
    "SANDBOX_WRONG_VERDICTS=<k> fail_closed=<yes|no>")

# ---- reviewers: legs under both profiles ---------------------------------------------------------------------------
LEG_GROUPS = [("RevC1V2LegsP1", "P01 TXT, P02 DOCX, P03 NOPYC"), ("RevC1V2LegsP2", "P04 CHECK, P05 REFUSEROW, P06 REBUILD"),
              ("RevC1V2LegsH1", "H07 FOREIGN, H08 REPLACE, H09 ORPHAN"), ("RevC1V2LegsH2", "H10 SPANSLINK, H11 FILELINK, H12 TSVLINK"),
              ("RevC1V2LegsH3", "H13 OUTSIDE, H14 BIGTXT, H15 BIGRAW"), ("RevC1V2LegsH4", "H16 OUTFILE, H17 UNREADABLE, H18 FIFO, H19 ENTRYDOT, H20 BIGFORM")]
for n, legs in LEG_GROUPS:
    add(n, "reviewer",
        f"Review the legs {legs} of {EV}/c1v2-count.py (docstring first) in BOTH profiles. (a) False negatives: write three different CORRECT builders for these legs (policies the docstring allows: refuse vs replace a link, exit codes within the stated sets, different guard order; start from {CTL}/pos-indep1.py, pos-indep2.py, pos-indep3.py and edit in scratch) and run `{C1}`; any correct builder that fails a leg in either profile is a false positive of the counter. (b) Tautologies: can a leg pass with the builder doing nothing? Can the neutral profile mask a real hazard (e.g. a name that makes the hazard fixture ineffective)? (c) Leg verdicts that depend on the profile (names, env, pipes vs files, address-space limit): list them. Report defects with a minimal reproduction.",
        f"LEG_DEFECTS=<k> false_positive=<n> tautology=<m> legs={legs}")

# ---- mutation ---------------------------------------------------------------------------------------------------------
MUT = [("MutC1V2Profile", "the neutral profile code: `Fx.__init__`, `_env_and_limits`, `new_url`, the pipe/closed-stdin branch of `run`, the cwd handling"),
       ("MutC1V2Run", "`run()` and the sandbox: SANDBOX flags, RLIMIT_AS/FSIZE, timeout and killpg, the stderr cap, wait4/ru_maxrss, `clean_out`, `tools_unchanged`"),
       ("MutC1V2Legs", "the leg bodies (`leg_p01`..`leg_h20`) and `snap`/`tree_of`/golden-tree code (drop an equality, weaken a comparison, skip the mtime check, accept any exit code)"),
       ("MutC1V2Main", "`main()`: profile pairing (`all(oks)`), the seeded shuffles, the fail-closed preflight, exit codes, work-dir cleanup, the verdict line")]
for n, target in MUT:
    add(n, "mutation-tester",
        f"Mutation-test the v2 counter {EV}/c1v2-count.py, aimed at {target}. Work on a copy in your scratch laid out as {CTL}/run-c1v2-controls.py lays out its mutants (the counter at <dir>/corpus/evidence/round62/c1v2-count.py and the lane's tools/capture-text.py at <dir>/tools/). Apply at least 10 NEW mutants beyond X01-X12 of that runner. For each, run `{BAT} --counter <mutant>` (about 50 s; you may use --only subsets for speed) and report: mutant, edit, battery verdict, forgers newly accepted, KILLED or SURVIVED. For each survivor say whether it is equivalent or a real control gap and name the forger or builder that would kill it.",
        "KILLED=<k>/<n> survivors_that_are_gaps=<g>")
add("MutC1Battery", "mutation-tester",
    f"Mutation-test the BATTERY {EV}/c1v2-battery.py itself: in a scratch copy apply at least 10 mutants (drop the salt, accept exit 2 as reject, expect exit 0 for a forger, remove a forger sniff so it always fires or never fires, drop the stub group, change a denominator, make LANDED count 2 of 3, let `--only` pass the verdict) and run each against the v2 counter, the round-61 counter, and the three null counters in {CTL}. Report which mutants flip a BATTERY verdict wrongly and which the controls in {CTL} would not notice.",
    "BATTERY_MUTANTS_KILLED=<k>/<n> control_gaps=<g>")
add("MutC2V2Counter", "mutation-tester",
    f"Mutation-test {EV}/c2v2-count.py: in a scratch copy apply at least 12 mutants (drop the anchor check, the opened-date bound, the used-by check, the quote word cap, COVERAGE minimums, the ECHO ratio, the PROBE live run, the probe-lines comparison, the MAP check, the [INFERENCE] requirement, resolve S139 to any file, accept an entry with fewer than 5 claims, ...). Run each against the control matrix of {CTL}/run-c2v2-controls.py (a scratch copy pointing at your mutant) and report which mutants none of the 20 controls kills.",
    "C2_MUTANTS_KILLED=<k>/<n> control_gaps=<g>")

# ---- attack: C2 --------------------------------------------------------------------------------------------------------
add("CritC2V2Forge", "critic",
    f"Attack R62-C2 ({EV}/c2v2-count.py): produce entries that reach C2=PASS in a scratch mirror prepared as {CTL}/run-c2v2-controls.py does, while being wrong or empty: claims that add filler words around a quote (ECHO passes on any three fresh words), a probe whose expected values are rewritten to match a wrong observation, a probe script that prints the committed lines without touching the kernel, a source cell naming the entry itself, a README line that names the path inside a comment, a fake `man`/`col` on PATH. Report each forge with the exact counter line and the smallest counter change that would stop it.",
    "C2_FORGES_REACHING_PASS=<k> named_in_claims=<n>")
add("CritC2Probe", "critic",
    f"Attack the probe {CTL}/candidate-openat2-probe.py (and its output candidate-openat2-probe.txt): every `expected` value was chosen by the author. For each of P01-P14 find the sentence of /usr/share/man/man2/openat2.2.gz (render `MANWIDTH=1000 man -l FILE | col -bx`) or /usr/include/linux/openat2.h that predicts it, or say the expectation is the author's inference. Look for probes that cannot fail (P01), that depend on the filesystem, on uid, on symlink target resolution, or on being run as the owner; look for missing cases (RESOLVE_NO_XDEV, RESOLVE_NO_MAGICLINKS on /proc/self/fd, O_CREAT, EAGAIN). Run the probe from a different cwd, with a different umask and as `nice -n 19`; report instability.",
    "PROBES_WITHOUT_SOURCE_SENTENCE=<k>/14 cannot_fail=<n>")
add("CritC2Quotes", "critic",
    f"Attack the quotes of {CTL}/c2v2-positive-entry.md (Q1-Q9): for each find a reading under which the quote, in its page context, does NOT support what the row's `teaches` cell and the entry's claims say (hedges, kernel-version qualifiers such as `since Linux x.y`, the `OPENAT2_REGULAR (since Linux 7.2)` line, the FreeBSD/chroot remarks, `Currently ... may change in the future`). Check that Q3's `only in the final component` belongs to the RESOLVE_NO_SYMLINKS paragraph and says what claim 1 says, and that Q5's `glibc provides no wrapper` is scoped to the page's version (man-pages 6.19 and the host's glibc: `pacman -Q glibc`).",
    "QUOTES_WITH_UNSTATED_LIMIT=<k> of 9")
for i in range(1, 6):
    add(f"RevC2V2Claim{i}", "reviewer",
        f"Entailment review of Claim {i} of the candidate entry {CTL}/c2v2-positive-entry.md (also the landing candidate). Re-open the quotes it cites yourself: render `MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx`; read /usr/include/linux/openat2.h; read {CTL}/candidate-openat2-probe.txt and run {CTL}/candidate-openat2-probe.py --work {SC}/<your-name>/p. Decide whether the claim follows from exactly those quotes, whether it overreaches (scope, `all`/`any` words, `always`, host-specific facts stated as general), and whether a hedge from the page is lost. Rewrite the claim if needed, with its quote set, and run `python3 -B {EV}/c2v2-count.py` on a mirror prepared as {CTL}/run-c2v2-controls.py does to confirm your rewrite still passes.",
        f"CLAIM{i}=<supported|overreach|misread> rewrite_needed=<yes|no>")

# ---- scouts ------------------------------------------------------------------------------------------------------------
add("ScoutC2ManPages", "scout",
    f"Re-open the sources of S138 and S139 (rows are in {CTL}/c2v2-positive-rows.txt): render `MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx`, read the unrendered roff (`zcat`), and read /usr/include/linux/openat2.h. For each of Q1-Q6 of {CTL}/c2v2-positive-entry.md report line numbers in rendered and raw forms, whether `col -bx` or whitespace normalisation changed the text, and the section heading it sits under. Add up to four further quotes of at most 25 words that would strengthen the entry (e.g. the EAGAIN-on-race text, RESOLVE_IN_ROOT, RESOLVE_NO_XDEV), with locations.",
    "Q1_Q6_LOCATED=<k>/6 extra_quotes=<n>")
add("ScoutC2Package", "scout",
    f"Provenance of the installed sources: `pacman -Qi man-pages linux-api-headers`, `pacman -Qo /usr/share/man/man2/openat2.2.gz /usr/include/linux/openat2.h`, `man -w 2 openat2`, any earlier MANPATH entry that could shadow the page, the `.TH` line, install dates, `pacman -Q glibc`. Report whether the rendered text of the cited paragraphs and the header lines are the packages' text, and write the one-line access disclosure the registry rows and the lesson Gate should carry. Write your findings in {W}/ScoutC2Package.md (round 61 lost this record: the seat settled with JSON and no file).",
    "SOURCES_ARE_PACKAGE_COPIES=<yes|no> man_pages=<x> headers=<y>")
add("ScoutC2Python", "scout",
    f"Open what the host's Python and libc say about openat2, read-only: `python3 -c 'import os; print(hasattr(os, \"openat2\"))'`, the installed CPython `os` documentation text if present (`python3 -m pydoc os.open`, /usr/lib/python3*/ and any docs package), `grep -rn openat2 /usr/lib/python3*/ 2>/dev/null | head`, glibc headers (/usr/include/bits, /usr/include/fcntl.h), `ldd --version`, and whether `strace`/`systemd`/`coreutils` binaries on the host reference the syscall (`strings` on a small binary is fine). Report what is sourced locally for the claim 'Python 3.14.8 has no openat2 function', and a second Python version if one is installed.",
    "PYTHON_OPENAT2=<absent|present> sources=<k>")
add("ScoutC2RowsCensus", "scout",
    f"Validate the three candidate rows {CTL}/c2v2-positive-rows.txt against the contract in /home/vgpnk/Projects/shokunin/CORPUS.md (section SOURCES.md): column count, id uniqueness (collision against the current registry, ids S138-S140 free?), enums, ISO dates, recheck cadences, used-by paths, the 0-3 leading-space parser note. Build a scratch registry copy with the rows inserted and run `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <copy>` from a copy of the lane (cwd = lane copy) and the manual census awk lines. Report the expected before/after census: rows 137 -> 140, tier A 108 -> 110, B 23 -> 24, status mined 112 -> 115, W-codes.",
    "CENSUS_EXIT=<0|n> rows=<before>-><after> findings=<none|list>")
add("ScoutC2RowsScope", "scout",
    f"Registry-fit review of the three candidate rows: do their `scope` cells claim more than the source supports (tier A is per scope; is a kernel header tier A for the numeric values and B for the semantics)? Is the own-work probe row honestly tier B? Is any row a near-duplicate of an existing row (`grep -n 'open(2)\\|rename(2)\\|openat' {LANE}/corpus/SOURCES.md`; the Leads line for openat2 in `## Leads`)? Report edits you would make to each row cell as replacement text, and whether the Leads bullet must be removed or annotated when the lead becomes a row (append-only rule 2).",
    "ROWS_NEEDING_EDIT=<k>/3")
add("ScoutMistakesPrior", "scout",
    f"Mine mistakes from rounds 59-61 for the round-62 lesson's `## Mistakes` (format in {LANE}/corpus/lessons/round-61.md: class, evidence pointer, captured-by, fix, shown-able-to-fail). Read the lessons and verifier spot-checks of rounds 59, 60, 61, QUALITY.md 115-123, and round 61's routed defects. List every distinct mistake with the QUALITY criterion that should have caught it or `none`, and which have a real fix landed (with a command that fails on the pre-fix state) and which only have a sentence. Rank by recurrence.",
    "MISTAKES=<n> uncaught=<k> fixed_with_red_before=<j>")
add("ScoutMistakesThisRound", "scout",
    f"Mine this round's own pre-freeze mistakes: read {CL}, the instruments in {EV} and {CTL}, and the git log since {BASE} (`git -C {LANE} log --stat {BASE}..HEAD`); find defects the freeze left or fixed on the way (e.g. the X04 control mutant that broke stdin handling and reported an unexpected result until its pattern was rewritten, the first positive C2 control that failed on census E11 because the mirror lacked knowledge files, a claim sharing no words with its quote). Count claims-file statements that do not match the files (counts of controls, digests as 16-hex prefixes: `sha256sum FILE | cut -c1-16`). Run `git -C /home/vgpnk/Projects/shokunin status --porcelain` and report any file a seat or the L1 wrote at the fleet root.",
    "THIS_ROUND_MISTAKES=<n> stale_claim_statements=<k> misroot_files=<m>")
add("ScoutSpotcheckPrior", "scout",
    f"Status of the round-61 closure's routed defects ({LANE}/corpus/lessons/round-61-verifier-spotcheck.md, section Routed to the lane's next round, four items): for each say what the round-62 freeze did about it with a pointer (claims.md section, file, commit), what remains open, and what the report must say. Also check the round-61 report at /home/vgpnk/Projects/shokunin/.ufo/reports/round-61/chousa.md against the contract in /home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-62.md section 4 (section headings, SHONEN lines) and list conformance gaps the round-62 report must not repeat.",
    "ROUTED_DEFECTS_ADDRESSED=<k>/4 open=<list>")
add("ScoutConsiderthese", "scout",
    f"Mine {LANE}/considerthese/ for ONE still-unimplemented proposal this round could land as a lesson, QUALITY criterion or registry row (contract: section 10 of /home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-62.md; the reflection is a pointer, not evidence — open what it points at). Round 61 mined the distillation half of CT-20261019-4 and left its size-watch half open; check that, scan the other proposals, grep the lane for each candidate (record the command), recommend one with the evidence you opened, and name two you reject with reasons.",
    "RECOMMENDED=<proposal title> implemented_check=<command>")
add("ScoutCensusCounts", "scout",
    f"Pre-compute the census the report must paste. At the current lane revision: run `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` (rows, tiers, statuses by the manual awk lines in /home/vgpnk/Projects/shokunin/CORPUS.md, the W04 list), the counting commands for knowledge entries (`find {LANE}/corpus/knowledge -name '*.md' | wc -l`, entries with `recheck:`), and project the after-values if S138-S140 and one entry are added (rows 137 -> 140; A 108 -> 110, B 23 -> 24; mined +3). Report a table the L1 can compare with the real after-census.",
    "BEFORE_ROWS=<n> PROJECTED_AFTER=<n>")
add("ScoutStreakTable", "scout",
    f"The recurring-weakness tool {LANE}/corpus/evidence/round53/weakness-streak.py with its table recurring.tsv exits 1 on this tree (`python3 -B corpus/evidence/round53/weakness-streak.py --table corpus/evidence/round53/recurring.tsv`: RW-1 streak=13 claimed=5, RW-3 streak=1 claimed=2). Read the tool, the table, round 61's RevStreak report ({LANE}/.ufo/waves/round-61/w1/RevStreak.md) and its corrected table in {LANE}/corpus/lessons/round-61.md. Decide for each row whether the regex measures the weakness it names (open three matching and three non-matching rounds' text), whether the claimed value or the regex is wrong, and propose the minimal re-registration (new table rows, not rewrites) that makes the tool exit 0 for a stated reason. Report the proposed rows verbatim.",
    "STREAK_ROWS_RIGHT=<k>/2 proposed_rows=<n>")

# ---- scribes -----------------------------------------------------------------------------------------------------------
for i, stance in [(1, "a practitioner's checklist: what a tool author does, in order, when opening paths under an untrusted directory"), (2, "a decision table: hazard, what the kernel can enforce with each flag, what Python can reach, which probe line shows it"), (3, "a compact reference: three principles with their quotes, then the limits")]:
    add(f"ScribeC2V2Entry{i}", "scribe",
        f"Draft an independent candidate for the knowledge entry corpus/knowledge/openat2-resolve-r62.md in the shape the counter {EV}/c2v2-count.py reads (read its docstring), as {stance}. Re-open S138 (rendered man page `MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx`), S139 (/usr/include/linux/openat2.h) and the probe output yourself and use quotes you located; keep ids S138, S139, S140; the rows to assume are in {CTL}/c2v2-positive-rows.txt. Prepare a scratch mirror as {CTL}/run-c2v2-controls.py does, put your draft in it and run `python3 -B {EV}/c2v2-count.py --root <mirror>`; deliver your draft at {W}/ScribeC2V2Entry{i}/entry.md and the counter's output line. The L1 will compare the three drafts and the positive control {CTL}/c2v2-positive-entry.md and merge. Keep claims no stronger than the quotes; mark inference [INFERENCE]; every number carries its command.",
        f"ENTRY{i}_C2=<PASS|FAIL> quotes=<k> claims=<n>")
add("ScribeGate", "scribe",
    f"Draft the `## Gate` section of corpus/lessons/round-62.md for the three new registry rows S138-S140 ({CTL}/c2v2-positive-rows.txt): for every row the path, the access date 2026-10-28, a located quote of at most 25 words with its location grounding `teaches`, and the admit decision with reason. Add one REJECTED row candidate of your own if you opened a source that fails the bar (e.g. a blog or a generic man page that restates openat2 without adding anything) — only if you really opened it, no URL fetch (offline). Re-open each source yourself before writing it and give line numbers. End with the spot-check request: name one admit and one reject for a non-author to re-open. Deliver at {W}/ScribeGate/gate.md.",
    "GATE_ROWS_WRITTEN=<k>/3 quotes_reopened=<n>")
add("ScribeStreak", "scribe",
    f"Draft, from the lessons and spot-checks of rounds 49-61 (open every pointer you cite), a compact table of the frozen-counter weakness by round: class, evidence pointer, and whether a fix with a red-before state landed; extend with round 62's battery as the next fix and its red-before ({CTL}/c1v2-before.txt). Deliver at {W}/ScribeStreak/streak.md; the reviewer seats will verify your rows, so mark every row you could not open.",
    "STREAK_ROWS=<n> unopened=<k>")
add("ScribeLogDraft", "scribe",
    f"Draft, from the frozen facts only and with the measured AFTER values left as the literal marker <AFTER> for the L1 to fill, the text of: the round-62 LOG.md entry ({LANE}/LOG.md — read its last entry for format), the SCORECARD.md round-62 verdict block (read the round-60/61 blocks; keep the numeric operability 3/10 unchanged and say so), and the corpus/README.md coverage-map row and Frontier paragraph for the new entry (read the Round61 section for the format). Deliver at {W}/ScribeLogDraft/draft.md; write nothing into the lane files.",
    "DRAFT_SECTIONS=<n> after_markers=<k>")
add("ScribeSkillRows", "scribe",
    f"Draft the {LANE}/SKILL.md additions for this round (read the Gates table and decision tables first: grep -n '^## \\|^| ' SKILL.md | head -80): (1) a Gates/decision row for the counter-validity battery (`c1v2-battery.py`: when a counter runs a candidate tool, run the forger battery before the counter binds data), (2) a decision row for opening paths under an untrusted directory (O_NOFOLLOW vs RESOLVE_NO_SYMLINKS vs RESOLVE_BENEATH, with the probe command), (3) one error-pattern row for 'counter accepts a detection forger'. Each row cites its source (path, command). Deliver at {W}/ScribeSkillRows/rows.md with the exact table row text and the line after which each belongs.",
    "ROWS_DRAFTED=<k>/3 cited_sources=<n>")

# ---- quality criteria --------------------------------------------------------------------------------------------------
for n, what in [("RevQualityA", "a criterion requiring any counter that runs a candidate tool to pass a detection-forger battery (a profile differential, a sandbox that removes the counter from the builder's view) before it binds a claim; Shown-able-to-fail: the round-61 counter prints FORGERS_REJECTED=0/12 BATTERY=FAIL on the same battery that the v2 counter passes"),
                ("RevQualityB", "a criterion requiring a sourced knowledge entry that rests on a probe to bind the probe's live output to its committed output in its counter (the PROBE check), and requiring each `expected` value in the probe to cite the sentence that predicts it or be marked as inference; Shown-able-to-fail: the controls probe-output-edited and probe-output-stale of run-c2v2-controls.py"),
                ("RevQualityC", "a criterion on freeze files: digests written inside a frozen claims file are 16-hex prefixes verified by `sha256sum FILE | cut -c1-16`, never abbreviated with an ellipsis, and a claims statement that counts controls (`ten mutants`) is verified by a command; Shown-able-to-fail: round 61's claims.md abbreviations and its `8 located quotes` vs 10 (see round-61-verifier-spotcheck.md defect (a))")]:
    add(n, "reviewer",
        f"Draft and then attack one new QUALITY.md criterion for {LANE}/corpus/QUALITY.md (criteria 1-123 exist; read 115-123 for the format: numbered, rationale with lesson evidence, a Check line, a Shown-able-to-fail line): {what}. Write the draft text in your report, run its Check command on the real evidence and on a red-before state, and report whether the check can fail and whether the criterion duplicates an existing one (grep QUALITY.md; name the number).",
        "CRITERION_CHECK_CAN_FAIL=<yes|no> duplicate_of=<n or none> text_ready=<yes|no>")

# ---- executors ---------------------------------------------------------------------------------------------------------
for tag, seeds in [("A", "8101 8102 8103"), ("B", "8104 8105 8106"), ("C", "8107 8108 8109 8110")]:
    add(f"ExecReproC1V2{tag}", "executor",
        f"Independent measurement of C1 instruments. For the landing builder {LANDED}, the three independent builders {CTL}/pos-indep1.py..pos-indep3.py and the reference {CTL}/pos-ref.py, run `{C1}` with C1V2_SEED set to each of {seeds} (fresh --work each; unset-seed runs too) and report LEGS per run. For one of the seeds load the host with two parallel `python3 -c` busy loops. Report any leg whose verdict changed between runs of the same builder and seed, and the wall time per run.",
        "LANDED=<min>-<max>/20 POSITIVES=<min>-<max>/20 flaky_legs=<list or none>")
add("ExecReproBattery", "executor",
    f"Independent measurement of the battery. Run `{BAT}` with `--counter {EV}/c1v2-count.py` three times and once with `--counter {R61}/c1-count.py`; report the summary line of each and the wall time. Run each of the three null counters in {CTL} (null-pass.py, null-fail.py, null-hashlist.py) through the battery and report the summary lines. Compare with {CTL}/c1v2-before.txt and {CTL}/null-counters.txt (committed receipts).",
    "BATTERY_V2=<PASS|FAIL> x3 V1=<FORGERS_REJECTED k/12> NULLS_FAIL=<k>/3")
add("ExecParallelLoad", "executor",
    f"Concurrency and load robustness of the v2 counter: run eight `{C1}` processes at once on the landing builder {LANDED} with distinct --work dirs under {SC}/<your-name>/, then the battery's LANDED subset (`{BAT} --only LANDED`) twice at once; report LEGS per run, any timeout/ENOSPC/EAGAIN, wall times, peak disk (`du -sh {SC}/<your-name>` mid-run), and whether the address-space limit or the 60 s timeout produced a false FAIL under load. Check `{LANE}/../scripts/hyaku/disk-guard.sh status` first and obey it.",
    "PARALLEL_LEGS_MIN=<k>/20 false_fail=<yes|no> peak_disk=<size>")
add("ExecProbeStability", "executor",
    f"Stability of the openat2 probe {CTL}/candidate-openat2-probe.py: run it 10 times (--work fresh each), from three different cwds, under umask 077 and 022, with `nice -n 19`, with TMPDIR set to {SC}/<your-name>, and on a tmpfs path if you can create one without sudo (otherwise /dev/shm); diff each run's PROBE/HEADER lines against {CTL}/candidate-openat2-probe.txt. Also run it as a non-owner path (a world-writable sticky directory) and report any difference. Run `python3 -B {EV}/c2v2-count.py` on a mirror prepared as {CTL}/run-c2v2-controls.py does, 5 times, report the verdict line each.",
    "PROBE_RUNS_IDENTICAL=<k>/10 c2_verdict_stable=<yes|no>")
add("ExecNoSandbox", "executor",
    f"Fail-closed behaviour of the v2 counter when the sandbox is missing: run `{C1}` with PATH lacking `unshare`, with `unshare` replaced by a script on PATH that exits 1, and one that exits 0 without running its argument (a fake sandbox: what verdict does the counter give, and does the preflight `unshare ... true` catch it?). Report exit codes and counter lines. A counter that exits 0/1 on a fake sandbox is a defect: propose the smallest fix (e.g. resolve /usr/bin/unshare absolutely, preflight that runs a probe program and checks its output). Do not edit the counter.",
    "FAKE_SANDBOX_GIVES_VERDICT=<yes|no> fail_closed=<yes|no>")
add("ExecScratchHygiene", "executor",
    f"Scratch and /tmp hygiene (round contract section 7): run `{C1}` and the battery once each with TMPDIR={SC}/<your-name>/t and `strace -f -e trace=openat,mkdir -o {SC}/<your-name>/trace.txt` if strace exists (else `lsof`/inotify-free alternatives: compare `find /tmp /var/tmp /dev/shm -newer <marker> 2>/dev/null` before and after). Report every path created outside --work, any residue after the run (including a leftover process: `pgrep -af 'build-spans|builder.py'`), and whether the counter's work directory is fully removed (including mode-000 and FIFO leftovers). The counters must not hardcode /tmp (`grep -n '/tmp\\|mkdtemp\\|tempfile' {EV}/*.py {CTL}/*.py`).",
    "PATHS_OUTSIDE_WORK=<k> residue=<none|list> hardcoded_tmp=<k>")
add("ExecMeasureAfter", "executor",
    f"Cross-measurement the L1 will compare with its own: run, from the lane root with fresh scratch under {SC}/<your-name>/, (1) `{BAT} --counter {EV}/c1v2-count.py`, (2) `{C1}` on the landing builder at three unset seeds, (3) `python3 -B {EV}/c2v2-count.py` (expect FAIL: the entry is not landed yet; paste the line), (4) `python3 -B {CTL}/run-c2v2-controls.py --work {SC}/<your-name>/c2`, (5) `python3 -B {CTL}/run-c1v2-controls.py --work {SC}/<your-name>/c1 --only X00 X01 X02` and paste each summary line with its exit code. Report any line that differs from the committed receipts in {CTL}/c1v2-controls.txt and {CTL}/c2v2-controls.txt.",
    "MEASURE_AFTER_MATCHES_RECEIPTS=<yes|no> differing=<list>")
add("ExecForgeVariants", "executor",
    f"Red-before for the profile differential: build, from the TEMPLATE in {EV}/c1v2-battery.py, three more sniff-wrapper forgers beyond F01-F12 that use features the v2 neutral profile does vary (HOME value, PATH element order, the number of environment variables, argv[0] path depth, the cwd being under the fixture or not, `sys.flags`) and three that use features it does NOT vary (stdin being closed vs open, the temp dir name `cwd-xxxx` vs `leg-xxxx` prefix hints, the file `capture-text.py` name, the `--replace` flag position). Run each through `{C1}` at three seeds; report which are rejected and which accepted. The accepted ones are candidate limits for the lesson and for next round's battery.",
    "VARIED_REJECTED=<k>/3 NOT_VARIED_ACCEPTED=<j>/3")

# ---- sentinels ----------------------------------------------------------------------------------------------------------
add("SentC1V2Safety", "sentinel",
    f"Safety review of running a hostile builder under the v2 counter: the counter executes the builder under the user's uid with the host filesystem visible. List what a builder could damage or read outside its fixture (the lane tree, ~/.ssh, other scratch dirs; the sandbox changes pid/user/mount-proc namespaces only), what the counter relies on (RLIMIT_FSIZE, AS limit, timeout, killpg), and the cheapest hardening (e.g. `--map-user`, bwrap with read-only binds, a mount namespace with a tmpfs root) that keeps the legs working. Verify with a harmless probe builder that writes a marker file outside the fixture: does it succeed? No real secrets are to be read or written. Report findings with exact commands.",
    "OUTSIDE_WRITES_POSSIBLE=<yes|no> hardening=<one phrase>")
add("SentC2ProbeSafety", "sentinel",
    f"Safety review of {CTL}/candidate-openat2-probe.py: it creates symlinks and files in --work only and calls syscall 437 through ctypes. Check: no path escapes --work, no deletion outside it (shutil.rmtree of a symlink target?), behaviour when --work is a symlink or contains one, when /usr/include is missing, on a non-x86_64 host (exit 2), when the syscall is blocked by seccomp (ENOSYS: what exit?), and that the cleanup runs on exception. Run it with --work on a path whose parent is a symlink to a scratch dir and report. Do not edit the probe.",
    "PROBE_SAFETY_DEFECTS=<k> exit_on_enosys=<code>")
add("SentRoundScratch", "sentinel",
    f"Disk and process hygiene audit for this wave itself: read /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status (read-only), `df -h /fast /tmp`, `ls {SC}`; the v2 counter creates sparse 192 MiB files per leg twice (plain and neutral); estimate peak disk and file-handle use of one run and of the 64-seat wave if every seat runs the counter at once, and the failure mode (ENOSPC -> exit?). Recommend a safe parallelism for seats and say whether any seat instruction in this wave's items could exceed it. Write only your report.",
    "PEAK_DISK_PER_RUN=<size> safe_parallel=<n>")

# ---- connectors / province ----------------------------------------------------------------------------------------------
add("ConnSiblingOverlap", "connector",
    f"Sibling-overlap scan: does any sibling lane already hold knowledge on kernel path-resolution flags (openat2, RESOLVE_*, O_NOFOLLOW), process sandboxing with namespaces (unshare, bwrap, pid namespaces) as a test harness, or forger/anti-detection batteries for counters? Search /home/vgpnk/Projects/shokunin/<lane>-shokunin/{{PROVINCE.md,corpus/knowledge,corpus/SOURCES.md,tools}} read-only with recorded grep commands (openat2, unshare, namespace, forger, sandbox, O_NOFOLLOW, RESOLVE_). Report overlaps with paths and whether the new entry/instrument duplicates, contradicts or complements them; round 61 named souji's origin-record entries as contested ground for atomic record writing.",
    "SIBLING_OVERLAPS=<k> contested=<lane or none>")
add("ConnClaimTrace", "connector",
    f"Cross-claim trace: map each failure class named in round 61's lesson Mistakes 1-3 and the closure's routed defect 1 (seed on argv, Traceback token in H16/H17, detached/setsid helper, RSS hidden by a detached reader, hash/mtime-blind snapshots, `.raw`-side hazards) to (a) the instrument change that addresses it in {EV}/c1v2-count.py, (b) the forger or control in {EV}/c1v2-battery.py or {CTL}/run-c1v2-controls.py that would fail without that change, and (c) the named limit that remains. Report a table and every class with no change, no forger or no limit.",
    "CLASSES_FULLY_TRACED=<k>/<n>")
add("RevProvince", "reviewer",
    f"Province review ({LANE}/PROVINCE.md and SKILL.md Boundaries): is a counter-validity battery for the lane's own gates (forgery resistance of a counting command) and a sourced entry on kernel path-resolution semantics inside chousa's province (deep-research method, the lane's own corpus and gates), or does it belong to a sibling (kumitate: orchestration and tooling; tsukuroi: host hardening; kengaku: evaluation claims; mori/souji)? Read the sibling PROVINCE.md files at /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md. If any part is out of province say which and what the report should do (report, never absorb).",
    "PROVINCE=<in|contested|out> contested_with=<lane or none>")
add("CritCalibration", "critic",
    f"Attack the frozen claims file {CL} for calibration: universal clauses without an enumerating command, statements that count things (`twelve forgers`, `ten mutants`, `18 variants`, `14 facts`, `20 controls`) — verify each by command against the files; digest prefixes (`sha256sum FILE | cut -c1-16` vs the prefix written); whether each target is one a do-nothing control cannot reach (re-run {CTL}/null-counters.txt's three null counters if you doubt it); whether the predicate sentence is the same sentence in claims.md, the docstring and the counter (QUALITY 116); whether anything promised for C1/C2 is not yet true. Report every mismatch with the line number and the corrected text. The claims are frozen, so these become an erratum, not an edit.",
    "CLAIM_STATEMENT_MISMATCHES=<k> erratum_needed=<yes|no>")
add("CritC1Overfit", "critic",
    f"Argue that the battery and the v2 counter were designed against each other (the forgers F01-F12 were written by the lane that then wrote the profile differential to reject them) and test how far that matters: for each forger find the single v2 feature that rejects it (the controls in {CTL}/c1v2-controls.txt name them) and then construct two forgers that use a detection feature the v2 counter has no differential for (any of: NSpid, pid 1, sys.stdin.isatty(), file descriptor numbers open at start, the count of threads, `os.sched_getaffinity`, `RLIMIT_NOFILE`, the umask, the process's session id equal to its pid). Run them through `{C1}` at three seeds and report accepted ones; each accepted class is a named limit and next round's battery row.",
    "OVERFIT_ACCEPTED=<k> classes=<list>")
add("RevFreezeCheck", "reviewer",
    f"Run the freeze check on this wave's own files as the orchestrator is about to see them: `python3 -B {LANE}/tools/freeze-check.py --claims {CL} --dispatch {LANE}/.ufo/waves/round-62/w1-dispatch.json --spec {LANE}/.ufo/waves/round-62/w1-spec.json --ready {LANE}/.ufo/waves/round-62/w1.ready` (read-only; the ready file may be taken already) and report every CHECK line. Then read the dispatch context and the claims file for any statement that is false at the time you read it (a seat count, a file that does not exist, a command that errors). Report which seats' items cite files that do not exist.",
    "FREEZE_CHECK=<PASS|FAIL> missing_files_cited=<k>")

# --- assemble -------------------------------------------------------------------------------------------------------------
spec = {"wave": "chousa-r62-w1", "reportDir": ".ufo/waves/round-62/w1", "items": ITEMS, "context": CONTEXT,
        "axes": ["operability", "coverage", "calibration"]}
out = pathlib.Path(LANE) / ".ufo/waves/round-62/w1-spec.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n")
roles = Counter(i["role"] for i in ITEMS)
names = [i["name"] for i in ITEMS]
assert len(set(names)) == len(names), "duplicate names"
print(len(ITEMS), dict(roles), "claims sha256", DIGEST)
