# ScribeStreak — round 61, wave w1 (scribe)

Item: draft the lesson text for considerthese 2026-10-26 proposal 2, "Track recurring weaknesses as streaks". Deliverable: `.ufo/waves/round-61/w1/ScribeStreak/streak.md` (lesson draft: a 13-row table, rounds 49-61, with class, evidence pointer and red-before status, plus streak notes and lane notes). Read-only otherwise. Frozen round-61 files were not touched.

## Findings

1. **The proposal is already implemented, and the implementation fails on the current tree.** Round 53 landed `corpus/evidence/round53/weakness-streak.py` with `recurring.tsv` (`corpus/lessons/round-53.md:78`; `LOG.md:1850`; registered at `SKILL.md:138`). Running it read-only now reports two red rows (output in E1). The registered gate therefore exits 1 on this tree.
2. **The tool's counts are wrong in both directions.** Its regex `forg(e|ed|able|ery)` matches mentions. Round 49's hit is the seat name `CritForgeC1` (`corpus/lessons/round-49-verifier-spotcheck.md:45`). Its claimed streak `5` is a value typed at round 53. `LOG.md:1871` records streak 7 at round 55. Nothing recomputes it.
3. **Classed streak (from the table, not the regex).** Class F (a forge or replay passes the frozen counter) runs 49-55 consecutively, 7 rounds. Round 56 has an unmeasured F attempt (the capture cache was deleted; `corpus/lessons/round-56-verifier-spotcheck.md:36`). F recurs at round 57. Rounds 58-60 are not F. The F run ending at round 60 is 0.
4. **Red-before fixes landed only in narrow places.** Landed with a red state: the round-55 counter mutants, killed in round 56 (`KILLED=1/9` → `9/9`; E4). The freeze-before-dispatch rule (QUALITY 116, round 59; round 61 followed it). Supplements in rounds 50-54 carry red controls, but the frozen counters did not change. Not landed for the frozen counters in rounds 49, 52-54, 57, 58 and 60. Round 61 has red-before controls at freeze (E5); the landed builder is absent (`tools/build-spans.py` unchanged since base).
5. **Round 58's C1 unreachability is code-read, not run.** Refusal legs print through the lowercase `PASS = "pass"` (`corpus/evidence/round58/c1-count.py:51`, legs at `:147`, `:223`, `:234`, `:315`), while the verdict tests `"=PASS"` (`:391`). I did not run the counter. The C2 offset half of the round-58 row is lesson-only; I did not re-derive it.

## Evidence (commands and observed output)

E1. `TMPDIR=<scratch> python3 -B corpus/evidence/round53/weakness-streak.py --root <lane> --table corpus/evidence/round53/recurring.tsv; echo exit=$?`
   → `FAIL RW-1 streak=12 claimed=5 first_in_run=49 routed=corpus/evidence/round53/c1-supplement.py frozen counter forgeable` / `FAIL RW-3 streak=0 claimed=2 first_in_run=- routed=- stray write outside scratch` / `WEAKNESS_ROWS=2 FAILING=2` / `exit=1`. The script only reads; no file was written.

E2. Per-round regex hits (`grep -ciE 'forg(e|ed|able|ery)'` over `corpus/lessons/round-N*.md`): every round 49-60 has at least one hit in one of its two lesson files, including rounds 58 and 59 (1 hit each in `round-58.md` and `round-59.md`), which the tool counts. I did not classify each hit.

E3. Pointer opens (all `path:line` in the table were opened with `read` or `grep -n`). Key lines: `round-50-verifier-spotcheck.md:36,38`; `round-51-verifier-spotcheck.md:38,100`; `.ufo/reports/round-51/chousa.md:13` (fleet repo, the 94-line figure); `round-52-verifier-spotcheck.md:34,94`; `corpus/evidence/round52/measure-after.txt:74` (`SUPPLEMENT_LEGS=0/4`), `:88` (`LEGS=9/9`); `.ufo/waves/round-53/w1/R53CritForgeC1.md:13`; `round-54/controls/c1-forge.txt` (`LEGS=6/6 C1=PASS`); `round-54-verifier-spotcheck.md:44,56,130`; `.ufo/waves/round-55/w1/R55MutC1Counter.md:39-47,86`; `corpus/evidence/round56/controls/c1-before.txt:21` (`KILLED=1/9`), `c1-measure-after.txt:28,57` (`KILLED=9/9`); `round-56-verifier-spotcheck.md:13,36,107`; `.ufo/waves/round-57/w2/R57W2CritC3Forge.md:22,41`; `round-57-verifier-spotcheck.md:62,98`; `corpus/evidence/round57/sidecar-audits.md:59` (`PROVENANCE_CONSISTENT=YES`); `round-58-verifier-spotcheck.md:15,36`; `round-59-verifier-spotcheck.md:8,41`; `LOG.md:1917-1921`; `corpus/QUALITY.md:978` (criterion 116); `round-60-verifier-spotcheck.md:18,44`; `.ufo/waves/round-60/w1/BuildCounter.md:102,176` (do-nothing reaches `C1=PASS`; D2); `.ufo/waves/round-60/c1-before.txt:6` and `c1-after.txt:2` (`C1=FAIL`, exit 1).

E4. `sed`/`grep` on `corpus/evidence/round56/controls/c1-before.txt:21`: `CANDIDATE=2/2 KILLED=1/9 DENIED=0/2`; `corpus/evidence/round56/c1-measure-after.txt:28`: `CANDIDATE=2/2 KILLED=9/9 DENIED=2/2` (two runs, `:57` the same).

E5. Round 61 (read only, no scoring): `corpus/evidence/round61/claims.md` sha256 `9afec8d493f0ba511a256f38cd5098ff508f9ed311c6c49ff5383add9ce0acec` (matches the wave context). `controls/c1-before.txt` → `LEGS=7/20 C1=FAIL` exit 1. `controls/c1-controls.txt`: `base 7/20`, `noop0 1/20`, `always2 14/20`, `forge-token 7/20`, `naive-guard 10/20`, `reference 20/20`, `M01-M14 KILLED`, `CONTROLS_UNEXPECTED=0`. `controls/c2-controls.txt`: `echo-claims rc=0 ... C2=PASS`. `git log --format='%h %s' -- corpus/evidence/round61/claims.md` → `2b0e17b` (amend before dispatch), `1661b85` (freeze); `9f32ac0 2026-10-28 18:56:18 -0300 round-61: wave w1 spec and dispatch`. `git diff --stat 9eef15e7 HEAD -- tools/build-spans.py` → empty.

## Row status

- 13 rows (rounds 49-61). Every cited pointer was opened, except the round-58 C2 half: `c2-count.py` was not re-derived. That row is counted as unopened (`unopened=1`).
- The class column is my judgment, based on the lesson's own wording. The RevStreak seat should check each class against the cited line.
- No row claims a verdict on a counter I ran. The round-58 U row is code-read only, and is labelled so in the draft.

## Limits

- The streak run in E1 uses the lane's own tool and table, unchanged. I did not edit `recurring.tsv` or the tool; the notes in `streak.md` route the fix to the lane.
- I did not run any frozen counter (C1, C2, the round-58-60 counters, or the R61 counter). Round-61 numbers are the frozen controls' own receipts.
- The fleet report `.ufo/reports/round-51/chousa.md` is outside the lane; I read it only as evidence for the 94-line figure.

## Hygiene

- Installs: none. Tools used: `read`, `grep`, `sed`, `git log/diff/cat-file` (read-only), and `python3 -B` on the lane's read-only streak script.
- Writes: `.ufo/waves/round-61/w1/ScribeStreak/streak.md` and this report. No other lane, fleet or shokuknow file was written. No git mutation.
- Scratch: `/fast/scratch/hyaku/chousa-r61/ScribeStreak` was created for the run and removed before this report.

VERDICT: STREAK_ROWS=13 unopened=1
