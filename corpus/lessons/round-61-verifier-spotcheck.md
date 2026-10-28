# Round 61 verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Dispatch digest (`.ufo/watchdog.log`, mutable): `2026-10-28T18:36:04-03:00 launch chousa round=61 pgid=2214392 driver=hyaku-inline attempt=1`; `2026-10-28T20:09:01-03:00 complete chousa round=61; hyaku-inline attempt=1`. Lane HEAD before `9eef15e7c0e0ae0055228e7066dc1eec676a91d2`, after `b6c1d0e5eb3276bd56dfe7c2ba94ffd9363d777d`. All measurements below ran from a scratch copy outside the lane (`git archive 9eef15e7 | tar -x -C <scratch>/base` for the base; `--work` dirs under `/fast/scratch/closure61.*`); the lane tree was only read (`git status --porcelain` empty before and after).

## Conformance (step 1)

- Report `.ufo/reports/round-61/chousa.md` committed by the lane identity: `git log --format='%an %H' -- .ufo/reports/round-61/chousa.md` → `chousa-shokunin 68cb98a068640febb244fc2f3dfa61e5cbeaa714`.
- `## SHONEN` heading count 1, four `[~]` lines matching the four boxes of `SHONEN.md` (no `[x]`).
- Cited lane commits `9eef15e7`, `1661b85b`, `2b0e17b2`, `9f32ac05`, `2edacafa`, `11fa23e4`, `2a5029e6`, `b6c1d0e5`: each `git -C chousa-shokunin merge-base --is-ancestor <hash> master` → exit 0.
- `scripts/hyaku/jj-lane.sh state chousa-shokunin` → `local=b6c1d0e5… remote=b6c1d0e5… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty; `git ls-remote origin refs/heads/master` → `b6c1d0e5…`.
- Dispatched prompt `.ufo/prompts/chousa-round-61.md` exists (689 lines); the report names it and the template/hyaku-addendum rendering. Real report with checkable work and commits, not a marker → status `ok`.
- Defects (status-neutral): (a) `claims.md` is frozen with a target "8 located quotes" and abbreviated digests that do not match their files (the lane's own `claims-erratum.md` names the digests and M08; the 8-vs-10 quote count is not in the erratum — the counter's predicate is `QUOTES=k/k`, landed 10/10); (b) `ScoutC2Package` settled with no `w1/ScoutC2Package.md` (lane lesson Mistakes row 7); (c) the start-of-round `research-gate.sh --selftest` 275-case figure is scratch output, not committed (no round-61 claim rests on it); (d) S137's `teaches` cell lists "caps" that sit in a different docstring paragraph (lane-recorded, append-only).

## Claim re-checks (step 2)

### C1 — operability, span builder output safety (re-measured by me, frozen predicate R61-C1)

- Builder bytes: `sha256sum tools/build-spans.py` → `c366492005ce304a0396401c4eea9d41b8cd2d384f82174b79277678f5474eac` (equals the report's; unchanged `2edacafa`→`b6c1d0e5`).
- After: `python3 corpus/evidence/round61/c1-count.py --builder tools/build-spans.py --work <absent dir>` → `SEED=1574145114`, all 20 legs `pass`, `LEGS=20/20 C1=PASS`, exit 0 (fresh random seed, not the lane's).
- Before: same counter on the base tree's `tools/build-spans.py` (git blob `072415ad36d9167f4ebe8117765b7053fb261069` confirmed with `git hash-object`, file sha256 `1ed2650a…`) → `SEED=4092970990`, failing P03, H07–H17, H20; passing P01, P02, P04, P05, P06, H18, H19; `LEGS=7/20 C1=FAIL`, exit 1. Reported 7/20 reproduced (same failing set as the claim).
- No-harm: `python3 corpus/evidence/round61/regress.py --work <dir>` → rounds 55, 56, 57/c3 each `check_rc=0 build_rc=0 identical=True pass`, `REAL_REBUILD=3/3`, exit 0.
- Frozen admission add-on: `grep -nE 'getppid|/proc/|c1-count|round61|leg-|argv\[0\]' tools/build-spans.py` → exit 1 (no match); `python3 corpus/evidence/round61/sniff-sweep.py tools/build-spans.py` → `SNIFF_SWEEP findings=0`, exit 0. I also read the builder head and grepped for `getppid|environ|sys.argv|inspect|ctypes|subprocess|gc.`: only `TOOLS = …__file__…` appears; nothing keyed to the counter.
- Post-wave supplement (not the frozen counter): `python3 corpus/evidence/round61/extras.py --builder tools/build-spans.py --work <dir>` → `EXTRAS=16/16` (incl. X14–X16 swap-in-the-window cases).
- Caveat I weigh, disclosed by the lane (Mistakes 1–3, `CritC1Sniff`, `CritC1Seq`, `CritC1Detached`): the frozen counter is forgeable by a builder that detects it. The landed builder does not (sweep exit 1/0, my skim, source review seats). The counter's verdict therefore measures the landed bytes honestly on every observable I could check; it is a counter limit routed to the next round, not a refutation.
- Verified by re-measurement (not evidence-only): LEGS before/after, regress, extras, sweeps. Gate-standard evidence only: `tools/freeze-check.py` selftest `34/34` and live runs (`freeze-check-selftest.txt`: `VERDICT: FREEZE_CHECK=34/34 red_before_exit=1`; `freeze-check-live.txt`: round-61 triple `FREEZE_CHECK=PASS` exit 0, round-60 pair `FAIL` exit 1 as the red-before) — verified as committed evidence, not executed.
- **Grade: operability `improved`.**

### C2 — depth (sourced), `derived-output-safety-r61.md` (re-measured by me)

- `sha256sum corpus/knowledge/derived-output-safety-r61.md` → `7137cacad9ac66a93bc0fb8f8b9050aeff8f999025065dfdaa088e6bc5da0716` (equals the report's).
- After: `python3 corpus/evidence/round61/c2-count.py` → `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=10/10 COVERAGE=1/1 CLAIMS=1/1 LIMITS=1/1 CENSUS=1/1 C2=PASS`, exit 0.
- Before: same counter with `--root <base-tree>` → `ENTRY=0/1 TRIO=0/1 ROWS=0/3 QUOTES=0/0 COVERAGE=0/1 CLAIMS=0/1 LIMITS=0/1 CENSUS=1/1 C2=FAIL`, rows S134–S136 absent; the entry file is absent at `9eef15e7` (`git archive` listing count 0).
- Entailment (the frozen claim leaves it to the closure): I rendered both pages myself (`MANWIDTH=1000 man -l /usr/share/man/man2/{open,rename}.2.gz | col -bx`; sha256 of the `.gz` files equal the lane's `a525cf9f…` and `4b6d62db…`; `pacman -Q man-pages` → `6.19-1`) and grepped Q1–Q8 with `grep -n -F`: all found (open: lines 147 ×Q1/Q2, 123 Q3, 473 Q7/Q8; rename: 46 Q4, 38 Q5/Q6). Q9/Q10 found verbatim at lines 33–34 of `R55W2SentBuilder.md`. Quote word counts ≤25 (Q4 21 words). Claims 1–6 follow from their quotes with the scopes the Limits section states (Q3 holds only when O_CREAT and O_EXCL are both given — Claim 2 says so; Claim 6's "overwrote" is the correct word for sizes that grew, against the seat's "truncated"). Claim 3's "rather than writing through it" and the cleanup rule are marked `[INFERENCE]` or sit under `## Application (not sourced)`.
- The counter is structural (an echoing claim passes; recorded by the lane); this check is the entailment read.
- **Grade: depth `improved`.**

### Other axes

- `git diff 9eef15e7 b6c1d0e5 -- SCORECARD.md`: pure append (26 lines: Round 61 verdict table + Planned round 62); no existing score, capability row or verdict changed; operability numeric 3/10 explicitly not moved.
- Diffstat outside evidence/waves: LOG, SCORECARD, SKILL (+5, no deletions), QUALITY, README, SOURCES (+6 rows), entry, lesson, `build-spans.py`, `freeze-check.py`; `PROVINCE.md` untouched; `corpus/captures` untouched.
- coverage `improved` (narrowly): first entry on OS link semantics under the lane's evidence writers; `corpus/README.md` lines 7–8 and `## Round61 coverage and frontier` at 1267. freshness `unchanged` (no fetch, captures untouched). calibration `improved` (narrowly): QUALITY 119–123 each cite a lesson row with red-before; `claims-erratum.md`. adjacency `unchanged` (`PROVINCE.md` untouched; souji overlap named as contested, not absorbed).

## Discernment spot-check (step 3)

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0; five `W04` duplicate-url warnings (S051, S053, S073, S074, S075), `chousa ok …/corpus/SOURCES.md`; identical to the lane's start/end census.

| item | decision | re-opened source | agree? | reason |
|---|---|---|---|---|
| S136 | admit (B, own-work) | `.ufo/waves/round-56/w1/R55W2SentBuilder.md` lines 11–12, 33–34; `git show 9eef15e:… \| cmp` identical | agree | h2/h3 quotes are verbatim; the file is a seat's fixture run, correctly tier B and 180d recheck, correctly not tier A; the entry uses "overwrote" where the seat's "truncated" contradicts its own byte counts (10→457, 74→243) |
| S137 | reject (C) | `tools/build-spans.py` line 37; `git show 9eef15e:tools/build-spans.py \| grep -c 'Output safety'` → 0 | agree | docstring is intent, not evidence; paragraph absent at base, present at `2edacafa`; flip condition (c1-count/extras exiting 0) stated and met, row stays rejected |
| S134 (extra) | admit (A) | `/usr/share/man/man2/open.2.gz` rendered, sha256 match | agree | Q1–Q3, Q7, Q8 located; the O_EXCL quote needs the preceding "both flags" scope, which Claim 2/Limits carry |
| S135 (extra) | admit (A) | `/usr/share/man/man2/rename.2.gz` rendered, sha256 match | agree | Q4–Q6 located at lines 46 and 38; Claim 4's "probably a window" hedge preserved |
| new SOURCES rows S134–S137 (quote check) | rows added | `grep -nE '^\| S13[4-7] ' corpus/SOURCES.md`; man renders above | agree | S134/S135 carry located quote ranges and an access disclosure (no URL, installed pages — honest, man7.org not opened); the ≤25-word quotes in the entry and lesson Gate are verbatim; census exit 0 |

Disagreements: none on decisions. Observations: the S134 row's `teaches` cell (O_PATH/O_NOFOLLOW) is broader than the one rendered quote and relies on Limits; S137's `teaches` mentions caps not in the cited paragraph (lane-recorded).

## Trend verdicts

- **expansion — improved** (narrowly): one admitted entry on ground the coverage map did not hold, citing three rows opened this round; evidence: re-run `c2-count.py` PASS, `corpus/README.md` Round61 section.
- **quality — improved**: base builder 7/20 → landed 20/20 on my own seed plus `REAL_REBUILD=3/3` and `EXTRAS=16/16`; the reference candidate with three blocking defects was not landed; four of five first-draft entry claims were corrected before landing and I found no remaining falsified claim in the entry.
- **discernment — improved**: I agree with all four named decisions and re-derived the S137 flip and the S136 "truncated" vs "grew" correction independently; the lane rejected its own C-tier docstring row, stated the flip, and disclosed its own counter's forgeability instead of claiming a clean 20/20 (report Admission read; lesson Mistakes 1–3). The lane-named admit/reject carry concrete re-openable commands.

## Verdict

Both claims verify on their frozen predicates by my re-measurement; no owned axis is harmed. Status `ok`, admitted `true`, verdict `admitted`. No exploratory claim; no promotion.

## Routed to the lane's next round

1. C1 counter: replace the argv `--seed` / detection-forgeable surface and the `Traceback` token test in H16/H17 (contradicts the predicate's no-token rule; `claims-erratum.md`); add tree checks on the `setsid`/detached classes and an RSS check not hideable by a detached reader.
2. Commit the `research-gate.sh --selftest` output (or a cited reproducible command) whenever SKILL.md's Gates row cites its tally; round 61's 275-case line is scratch-only.
3. Write the missing `w1/ScoutC2Package.md` record or note the omission in the wave digest; correct the frozen "8 located quotes" (actual 10) in the erratum.
4. SHONEN: all four boxes cite non-author-checkable evidence by this closure (SKILL decision tables, end-to-end LOG task with my re-run, executable instructions — the counters ran from the lane root with no oral context, PROVINCE untouched). Boxes remain `[~]`; promotion to `[x]` is the operator's.
