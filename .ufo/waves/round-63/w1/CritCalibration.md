# CritCalibration — round 63 wave w1 (critic)

Scope: calibration of `corpus/evidence/round63/claims.md` (sha256 prefix `6c46b2cc193e1a44`, freeze commit `62876ef`, base `a847a37`).
Method: every statement that counts, names a file, a command or an output line, checked by command against the lane tree,
git history and the receipts under `corpus/evidence/round63/controls/`. I did not re-run the battery, the counters or the probe;
receipts were compared, not regenerated. No writes outside this report, the erratum and my scratch (deleted). No installs.

## Findings (mismatches)

1. **"Controls (all committed before the freeze)"** (claims.md line 81) is false as written.
   - `git -C <lane> log --oneline --diff-filter=A --format='%h %s' -- corpus/evidence/round63/controls corpus/evidence/round63/claims.md corpus/evidence/round63/c1-battery.py corpus/evidence/round63/c2-count.py` → `62876ef round-63: freeze claims, battery, counter, controls and receipts` (one commit).
   - `git show --stat 62876ef` lists all 21 files, including `claims.md`, `c1-battery.py`, `c2-count.py` and every control. The controls are in the freeze commit, not before it.
   - Erratum E1.
2. **"wrong header file"** (line 144, C2 variant list) mislabels `s143-wrong-file`.
   - `run-c2-controls.py` line 113 replaces the S143 row path `/usr/share/man/man7/gitrevisions.7.gz` with `/usr/share/man/man1/git-log.1.gz`: a wrong man page, not a header. Count (19 variants) is correct. Erratum E2.
3. **Quoted SCORECARD heading** (line 14) does not occur verbatim.
   - `grep -cF 'Planned — round 63 (amended before the freeze)' SCORECARD.md` → `0`.
   - Actual heading, `SCORECARD.md` line 2991: `## Planned — round 63 (amended before the freeze, 2026-10-28)`. Erratum E3.
4. **"the lane holds nothing on what a git revision name ... names"** (line 115) is overbroad.
   - Scoped claim holds: `git -C <lane> grep -c rev-parse a847a37cc263c80417ee1cdf650de33e2f91a839 -- corpus/knowledge` → no output, exit 1 (worktree `grep -rl rev-parse corpus/knowledge` also exit 1).
   - Lane-wide, `git grep -c rev-parse a847a37… -- corpus tools` lists 12 files with nonzero counts, e.g. `corpus/lessons/round-31-verifier-spotcheck.md` (`git rev-parse --verify <h>^{commit}`), `corpus/evidence/round57/sidecar-audits.md` (`git rev-parse master:corpus/evidence/round45/spans.tsv`), `corpus/evidence/round51/receipt-check.py` (`<rev>:<path>` blob resolution), `tools/capture-fetch.py`. These are uses, not explanations, but the sentence is universal over the lane. Erratum E4 narrows it to `corpus/knowledge/`.

Count of mismatched statements: **k = 4** (items 1–4; item 4 is a judgment on an overbroad universal, strictly false-as-written count = 3 without it).

## Verified true (command → observed)

- Digests, `sha256sum FILE | cut -c1-16`: header `6c46b2cc193e1a44` ✓; c1-battery `0073fba73c89aaf8` ✓; c2-count `606207e224c0b7cf` ✓; pos-ref-preflight `07683086fd6c6b41` ✓; run-c1-controls `8e9bd4c3e304b5f0` ✓; run-c2-controls `8b2b371340b01b58` ✓; candidate probe `ccd702f4e9a2f7c4` ✓; c2-positive-entry `93ad2c681783b6ce` ✓; candidate-git-rows `cfdf7b117c26a07f` ✓. 9/9.
- `git rev-parse 62876ef^` → `a847a37cc263…` ✓ (base). `62876ef` is the freeze commit; `c8bfcc6` (HEAD/master now) is later.
- `git diff --stat 62876ef HEAD -- corpus tools corpus/evidence/round63 SKILL.md` → empty; `git status --short` on round63, SCORECARD, tools → empty. No frozen file changed after the freeze. `claims.md` at `62876ef` has sha prefix `6c46b2cc193e1a44`, same as the working tree.
- Before lines: `grep -Fx 'CLEAN=0/1 DEFECTS=0/15 BENIGN=0/6 BATTERY=FAIL' controls/c1-before.txt` ✓, exit line `exit=1` ✓. `grep -Fx 'ENTRY=0/1 TRIO=0/1 ROWS=0/3 QUOTES=0/0 COVERAGE=0/1 CLAIMS=0/1 ECHO=0/1 LIMITS=0/1 PROBE=0/1 MAP=0/1 CENSUS=1/1 C2=FAIL' controls/c2-before.txt` ✓, exit=1 ✓.
- After-line receipts: `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS` in `c1-reference-runs.txt` (3 blocks, `grep -c BATTERY=` → 3) and in `c1-controls.txt` (`positive-ref`, rc=0) ✓. C2 `positive` rc=0 `C2=PASS` ✓.
- Leg count: `c1-battery.py` defines CLEAN + D01–D15 + B01–B06 = 22 (lines 239–262) ✓. Battery prints `CLEAN=… DEFECTS=…/15 BENIGN=…/6 BATTERY=…` (lines 392–397) ✓. Battery args `--tool --work --fleet --jobs --only` present; `--work` must be absent/empty (line 362) ✓. D13 exit 2 ✓ (`c1-reference-runs.txt`: `D13 defect ok rc=2 (want 2, no PREFLIGHT line)`).
- Controls: `c1-controls.txt` has 22 named rows (`grep -c 'rc='` → 22): positive-ref, absent-tool, null-pass, null-fail, null-diff-oracle, null-selfreport, M01–M16. All null/absent rows read `BATTERY=FAIL` ✓. Mutants: 15 `rc=1 … BATTERY=FAIL` + M11 `rc=0 … BATTERY=PASS SURVIVED-expected` = 16 ✓. `C1_CONTROLS_UNEXPECTED=0` ✓.
  - Mutant descriptions vs `run-c1-controls.py` lines 32–48: M01 first-fail-only, M02 G03 always pass, M03 ENV as pass, M04 skip silent, M05 summary counts skip, M06 exit always 0, M07 no `:N` strip, M08 G02 index check `miss = []` (checks nothing), M09 census exit ignored, M10 selftest (G06) exit ignored, M11 G07 token dropped, M12 all SCORECARD tables, M13 `--only` ignored, M14 unknown id accepted, M15 exact heading, M16 first path word. All match the claims list ✓.
  - Best do-nothing and forger statements: `null-pass` CLEAN 1/1, DEFECTS 0/15, BENIGN 6/6 ✓; `null-diff-oracle` CLEAN 1/1, DEFECTS 15/15, BENIGN 0/6 ✓.
  - `null-pass.py`/`null-fail.py`/`null-selfreport.py` contents match descriptions (selfreport: 8 PASS lines, `PREFLIGHT=8/8`) ✓.
- `c2-controls.txt` has 25 receipt rows (`grep -c 'rc='` → 25): absent, no-entry-rows, positive, 19 variants, non-sequitur (rc=0 PASS), openat2-on-lane (rc=0 PASS), git-on-lane-base (informational FAIL). FAIL-expected = 2 + 19 = 21 ✓. Variant list in claims matches `run-c2-controls.py` lines 95–115 (except item 2 above). `C2_CONTROLS_UNEXPECTED=0` ✓.
- Probe: `candidate-git-revision-probe.txt` has P01–P14 and `PROBE_FACTS=14/14` ✓. `# cite` comments marked INFERENCE: P02, P05, P06, P10, P13 = 5 ✓.
- Rows: `candidate-git-rows.txt` S142 tier A, S143 tier A, S144 tier B, opened 2026-10-28 ✓. Man pages `/usr/share/man/man1/git-rev-parse.1.gz` and `/usr/share/man/man7/gitrevisions.7.gz` exist; `.TH … "2026\-09\-27" "Git 2\&.56\&.0"` ✓; `/var/lib/pacman/local/git-2.56.0-1/desc` → `2.56.0-1` (read-only) ✓; `git --version` → `git version 2.56.0` ✓.
- C2 counter: `c2-count.py` `--config` default `git`, `openat2` control ✓; `--fleet`/`$SHOKUNIN_ROOT`/parent handling ✓; missing census → `return 2` with message naming `--fleet` (lines 184–188) ✓. Docstring counts `ENTRY=1/1 … C2=PASS` ✓.
- Gates: 8 gates G01–G08 (`null-pass.py` names identical) ✓. `tools/freeze-check.py` prints `FREEZE_CHECK=`, reads `.ufo/waves/round-59..61` (dirs present) ✓; `tools/assimilate-rows.py` prints `SELFTEST=PASS|FAIL` (line 372) ✓; `tools/research-gate.sh` prints `RESEARCH_GATE_SELFTEST: PASS` (line 8685) ✓; `tools/lane-preflight.py` absent ✓.
- Round-created files absent at HEAD: `tools/lane-preflight.py`, `corpus/knowledge/git-revision-identity-r63.md`, `corpus/evidence/round63/git-revision-probe.{py,txt}`, `corpus/lessons/round-63.md` ✓.
- Referenced files exist: `corpus/knowledge/revision-binding-r31.md` (sha256 pin text ✓), `corpus/knowledge/openat2-resolve-r62.md`, `corpus/lessons/round-62-verifier-spotcheck.md` (section `## Routed to the lane (next round)`, five numbered items ✓), `corpus/SOURCES.md`, `corpus/README.md`, `SHONEN.md` (no change since freeze ✓), `SKILL.md` line 69–70 (every claim carries a resolvable pointer and revision read ✓), `SCORECARD.md`, `.ufo/waves/round-63/census-start.txt` (7 lines, ends `exit 0` ✓), `scripts/sources-census.sh` at fleet root ✓.
- SCORECARD amendment is in the freeze commit (`SCORECARD.md | 4 +`) ✓; the original round-63 heading is `## Planned — round 63 (not started)` (line 2987) with the candidates the claim lists ✓.
- Seat names in item 3 (`CritCalibration`, `RevC1Contract`, `ExecClaimsStatements`) appear in `w1-spec.json` ✓.
- Wave size: `w1-spec.json` has 69 items (band 64–128 ✓). Attack share is not defined in claims.md; with roles critic 11 + mutation-tester 7 = 18/69 = 26.1 % (INFERENCE: this reading of "attack"; reviewer 18 would give 52 %).
- Operability numeric: SCORECARD lines 2715, 2759, 2808, 2838 state the numeric operability scale is 3/10 and "No other numeric score is invented" ✓ (supports "only numerically scored axis").

## Not checkable now (forward-looking, not counted)

- "the report discloses one slip of the L1's own (a shell python replacement on the new reference tool)": a report commitment; nothing in `.ufo/waves/round-63` names it yet (grep for `python replacement`/`shell python` matched only the generic "python one-liners" rule in `gen-w1-spec.py` and `w1-spec.json`). Checkable only at L1 report time.
- All "After target" lines for the landed `tools/lane-preflight.py` (`PREFLIGHT=8/8`, C2 landed `C2=PASS` on the lane) are targets; the reference receipts above stand in for them, and nothing here was run on a landed tool.
- Item 5 "changes nothing in SHONEN.md": no SHONEN change since the freeze (diff empty) ✓.

## Erratum

Needed: **yes**. Written to `.ufo/waves/round-63/w1/CritCalibration/erratum.md` (E1 timing of controls; E2 `wrong header file` label; E3 quoted SCORECARD heading; E4 overbroad lane-wide sentence). For L1 to file under `corpus/evidence/round63/` as an erratum file; claims.md itself is not edited.

## Limits of this read

- Controls were compared to the frozen receipts, not regenerated; I did not run `c1-battery.py`, `c2-count.py` or the probe.
- Quotes in the probe `# cite` comments and rows were not checked against the man pages (the counter does that; I did not run it).
- E4 is a judgment about the scope of an overbroad universal; the other three are literal mismatches.

## Scratch

`/fast/scratch/hyaku/chousa-r63/CritCalibration/` created empty for this seat and removed before yield.

VERDICT: CLAIM_STATEMENT_MISMATCHES=4 erratum_needed=yes
