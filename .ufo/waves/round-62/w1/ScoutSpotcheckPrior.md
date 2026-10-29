# Round 62 w1 — ScoutSpotcheckPrior — routed defects status + round-61 report conformance

Scope: (a) per routed defect of `corpus/lessons/round-61-verifier-spotcheck.md` §"Routed to the lane's
next round": what the round-62 freeze did (pointer), what stays open, what the round-62 report must say;
(b) round-61 report `.ufo/reports/round-61/chousa.md` vs contract §4 (`.ufo/prompts/chousa-round-62.md`),
section headings and SHONEN lines. Freeze = commit `388d1535` (claims, counters, battery, controls);
wave = `d173d144` (w1 spec/dispatch/ready, freeze-check-live). All commands below were run by me from the
lane root; outputs quoted verbatim. Read-only git only; nothing under the frozen paths edited.

## (a) The four routed defects

### 1. C1 counter surface (argv `--seed`, `Traceback` token tests H16/H17, detached/setsid, RSS) — ADDRESSED by the freeze

- Pointer: `claims.md` §C1, paragraph "What the v2 counter changes against v1 (instrument, frozen)":
  seed from env `C1V2_SEED` never argv; H16/H17 `Traceback`-token tests gone (exit code and tree only);
  every run inside `unshare -Ufp --kill-child --mount-proc` (no helper outlives the builder, builder cannot
  see the counter); `plain`+`neutral` profiles (random dir/builder/quotes/cache/out names, host shape, env,
  LANG, PATH order, RLIMIT_FSIZE, empty cwd, closed stdin, piped stdout/stderr); refusal snapshots compare
  mtimes. Files: `corpus/evidence/round62/c1v2-count.py` (sha256 prefix `b7016fba91b03460`, matches claims),
  `c1v2-battery.py` (F01–F12 forgers, F12 = bytecode + `setsid` helper deleting `__pycache__`).
- Observed mechanics: `grep -c Traceback c1v2-count.py` → `0`; line 15 "from the environment (`C1V2_SEED`),
  never from its argv"; line 141 `SANDBOX = ["unshare", "-Ufp", "--kill-child", "--mount-proc"]`; lines
  139–158 profile/name randomization; line 310 `RLIMIT_AS`.
- Observed discrimination receipts (committed at `388d1535`): `controls/c1v2-before.txt` — round-61 counter
  `FORGERS_REJECTED=0/12 … BATTERY=FAIL exit=1` (all twelve forgers read 20/20 PASS); `controls/c1v2-controls.txt`
  — X00 intact `FORGERS_REJECTED=12/12 BATTERY=PASS`, ten mutants each killed by exactly the forgers their
  removed feature stops, `CONTROLS_UNEXPECTED=0`, X10 (no address-space limit) SURVIVES as the named gap;
  `controls/null-counters.txt` — null-pass `0/12`+`0/4`, null-fail and null-hashlist reject the salted landing
  builder `LANDED=0/3`, all `BATTERY=FAIL`.
- Still open (claims.md "Named limits", disclosed before data): a builder that detects the sandbox itself
  (`NSpid` in `/proc/self/status`, `getpid() == 1`); features neither profile varies (`capture-text.py` file
  name, `S###` id shape, quote vocabulary); a builder that waits out the counter; a detached helper reading a
  192 MiB capture is bounded, not measured; a shared-memory read below the limit is not measured; forgers
  authored by the counter's own lane (overfit); battery builders all Python; X10 has no forger.
- Report must say: kill rule run as frozen — battery on the unmodified `c1v2-count.py` prints
  `FORGERS_REJECTED=12/12 … BATTERY=PASS` exit 0 at the landing commit and at closure, and
  `LEGS=20/20 C1V2=PASS` at three fresh seeds (`C1V2_SEED` unset); any forger found beyond the twelve is
  routed as a counter limit for the next battery, never a refutation.

### 2. Commit the `research-gate.sh --selftest` tally whenever SKILL.md cites it — OPEN, freeze did nothing

- Pointer: neither `388d1535` nor `d173d144` adds a selftest receipt; `git log -1 -- SKILL.md` → `2a5029e`
  (round-61; untouched in round 62), and SKILL.md lines 81–88 still cite
  `bash tools/research-gate.sh --selftest` → `PASS (275 cases, 0 skipped)`. `claims.md` does not mention it.
- Mitigation already in place: the SKILL.md rows carry the exact reproducible command inline (the defect's
  "or a cited reproducible command" half), so the tally is checkable — but no committed output exists.
- Report must say: either paste a fresh selftest run (command + output + exit code) as evidence, or re-cite
  the SKILL.md command instead of a scratch observation; never cite an uncommitted figure.

### 3. Missing `w1/ScoutC2Package.md` + erratum "8 located quotes"→10 — HALF-ADDRESSED

- Record half, addressed at wave level: `d173d144`'s `w1-spec.json` ScoutC2Package item ends "Write your
  findings in …/.ufo/waves/round-62/w1/ScoutC2Package.md (round 61 lost this record: the seat settled with
  JSON and no file)" — the omission is noted in the wave spec/dispatch and the record is re-dispatched.
  Open until that seat settles: the round-62 file was not yet present when I listed `w1/`; the report must
  confirm it landed (and `corpus/lessons/round-62.md` should still record the round-61 omission class).
- Erratum half, OPEN: `corpus/evidence/round61/claims-erratum.md` history is only `2a5029e` and its text
  corrects two digests + M08 + the H16/H17 token note; it does not mention the quote count. The wrong figure
  stands at `corpus/evidence/round61/claims.md:81` ("8 located quotes" vs the counter's `QUOTES=10/10`).
- Report must say: the record re-dispatched and landed (or say it did not); the 8→10 correction landed in an
  erratum/lesson row, or route it again explicitly.

### 4. SHONEN `[~]` → `[x]` promotion is the operator's — OPEN (correctly untouched by the freeze)

- Pointer: lane `SHONEN.md` lines 5/7/9/11 — four boxes, all `- [~]`; nothing in `388d1535`/`d173d144`
  touches SHONEN or names non-author verifiers. claims.md correctly does not promote.
- Report must say: one line per box, `[~]` with resolvable pointer, `[x]` only where a named non-author
  verifier is on record (the round-62 closure spot-check may serve once it exists); state plainly that
  promotion remains pending with the operator.

## (b) Round-61 report vs contract §4 — headings and SHONEN

Conformant (observed): required sections present in contract order — `## Work performed`, `## Landed
changes`, `## Before → after measurements`, `## Sources & frontier`, `## Trend verdicts`, `## SHONEN`;
report opens by naming both claims and axes; Trend verdicts use the enum with evidence; Sources & frontier
carries rows before→after with the counting command, tiers, touched rows, frontier advanced, census
start/end pasted with exit codes; SHONEN = exactly four lines matching the four SHONEN.md boxes, all `[~]`
with pointers, honest "no non-author verifier named", no `[x]`.

Conformance gaps the round-62 report must NOT repeat:

1. Scratch-only evidence for a cited figure: round-61 cited the 275-case selftest as "(observed at round
   start …; not committed — scratch output)". Every figure the report cites must be committed or carry its
   exact reproducible command in the report itself (see defect 2).
2. A dangling pointer to a seat report never written: round-61's wave narrative treated ScoutC2Package as
   settled while its claimed `w1/ScoutC2Package.md` never existed (only the results.json JSON). Before
   filing, resolve every named pointer to an existing file.
3. A frozen numeric target disagreeing with the landed artifact: round-61's frozen "8 located quotes"
   (`round61/claims.md:81`) vs the counter's `QUOTES=10/10`, plus the two abbreviated digests the erratum
   names. Round-62: quote the exact printed count lines from the frozen counters (e.g. `FORGERS_REJECTED=12/12`,
   `PROBE_FACTS=14/14`, the actual `QUOTES=k/k`) and check digests with `sha256sum FILE | cut -c1-16`
   (claims.md itself mandates the prefix form), never retype a digest.
4. Minor: measured commits stated only in the Before→after section preamble (`2edacafa`, `11fa23e4`)
   instead of inside each claim's bullet; the contract asks each measurement to carry "the commit it was
   measured against" — put the commit hash in every bullet.

## Evidence index (command → observed output)

- `sha256sum corpus/evidence/round62/claims.md` → `a3193ebd328919e2af017011278e423c5940fd9447f0730bd400da9d15c866bc` (equals wave context).
- `git -C <lane> log --format='%H %s' -3` → `d173d144` (wave w1 spec/dispatch, 66 seats) ; `388d1535` (freeze) ; `8607de8` (base).
- `git show --stat 388d1535` → 25 files +3516 −0, all under `corpus/evidence/round62/` + census-start; no SKILL.md, no erratum, no SHONEN, no round-61 paths.
- `sha256sum c1v2-count.py c2v2-count.py tools/build-spans.py` prefixes → `b7016fba91b03460`, `817d5fc0b94e9fc8`, `c366492005ce304a` (all match claims.md).
- `grep -c Traceback c1v2-count.py` → `0` ; `grep -n 'C1V2_SEED|unshare|RLIMIT'` hits at lines 15/51/141/309–310.
- `cat controls/c1v2-before.txt | tail -2` → `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=0/12 STUBS_REJECTED=4/4 BATTERY=FAIL` / `exit=1`.
- `cat controls/c1v2-controls.txt | tail -2` → `CONTROLS_UNEXPECTED=0` / `exit=0`; X00 PASS 12/12; X10 SURVIVES (named gap).
- `cat controls/null-counters.txt` → three do-nothing counters `BATTERY=FAIL` (null-fail/null-hashlist `LANDED=0/3`).
- `cat controls/c2v2-controls.txt | tail -2` → `C2V2_CONTROLS_UNEXPECTED=0`; `echo-claim` FAILs (r61 limit closed); `non-sequitur` PASSes (named open limit).
- `cat controls/candidate-openat2-probe.txt | tail -1` → `PROBE_FACTS=14/14`.
- `cat .ufo/waves/round-62/freeze-check-live.txt | tail -2` → `FAILED_CHECKS=none` / `FREEZE_CHECK=PASS` (8 checks, 66 names).
- `git log --follow --format='%h %s' -- corpus/evidence/round61/claims-erratum.md` → only `2a5029e`; `grep -n 'located quotes' corpus/evidence/round61/claims.md` → `81:…8 located quotes…`.
- `git log -1 --format='%h %s' -- SKILL.md` → `2a5029e …` (Gates rows 81–88 still cite `PASS (275 cases, 0 skipped)`; no receipt committed in r62).
- `grep -n '^- \[' SHONEN.md` → four boxes, lines 5/7/9/11, all `[~]`.
- `grep -n ScoutC2Package .ufo/waves/round-61/w1-results.json` → seat output JSON claims `"report": "…/w1/ScoutC2Package.md"`; `ls .ufo/waves/round-61/w1/ | grep -ci scoutc2package` → `0` (file absent).
- `w1-spec.json` ScoutC2Package task tail → "Write your findings in …/.ufo/waves/round-62/w1/ScoutC2Package.md (round 61 lost this record: the seat settled with JSON and no file)".
- No `corpus/lessons/round-62.md` exists yet (round open). No counters, battery or controls were executed beyond the reads above — the after-state measurement is the closure's to run.

VERDICT: ROUTED_DEFECTS_ADDRESSED=1/4 open=2-no-committed-selftest-receipt,3b-erratum-8to10-quote-count,4-shonen-promotion-operator-pending,(3a-record-pending-ScoutC2Package-w62-settlement)
