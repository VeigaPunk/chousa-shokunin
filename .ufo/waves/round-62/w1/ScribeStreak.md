# ScribeStreak — round 62, wave w1 (scribe, leaf)

Item: draft the frozen-counter weakness table by round (49–61), extended with round 62's battery and its red-before. Deliverable: `.ufo/waves/round-62/w1/ScribeStreak/streak.md` (29 rows). Read-only elsewhere; no lane, fleet or git writes; no network; no installs (no tools needed beyond `read`, `grep`, `sed`, `python3 -B`).

## Findings

1. **The weakness is the frozen counter, and it recurs by class, not by round.** Replay or forgery of a frozen C1/C3 counter appears in rounds 49–54 and 57 (R49-2, R50-1, R51-1, R52-1, R53-3, R54-1, R57-1). Rounds 55–56 carry it into successors; rounds 58–59 carry a verdict-path defect (R58-1, R59-1); round 60 is a do-nothing defect (R60-1); round 61 is detection-forgeability (R61-2). Non-counter process defects are excluded.
2. **Of 29 rows, 11 landed a fix with a red-before receipt, 7 are partial, 10 have no fix, 1 is pending** (R62-2). Landed rows are successors or new checks; the lessons state that no frozen predicate was edited after data, and I did not run `git diff` to confirm it (closure check). Landed: R51-1, R51-2, R53-4, R55-1, R56-1, R60-1, R61-2, R61-3, R61-4, R61-5, R62-1. Partial: R49-1, R50-1, R52-1, R53-3, R54-1, R55-2, R61-1.
3. **Round 62 closes the round-61 class for the v2 counter, with a measured red.** The battery on the round-61 counter prints `FORGERS_REJECTED=0/12 BATTERY=FAIL`, exit 1 (`corpus/evidence/round62/controls/c1v2-before.txt`). I re-ran the battery on `c1v2-count.py` (sha256 prefix `b7016fba91b03460`): `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=PASS`, exit 0. The v2 counter on `tools/build-spans.py`: `LEGS=20/20 C1V2=PASS`, exit 0 (one random seed). The battery's forgers are authored by the same lane (named overfit risk), so this closes the class only for the twelve listed forgers.
4. **Today's re-runs confirm three frozen-counter weaknesses still open.** The round-53 counter passes `forge-c1.py` at `LEGS=8/8 C1=PASS` (seed 7). The round-53 counter passes `--per-leg 0` at `LEGS=8/8 C1=PASS` with zero `case` lines. The round-50 forge keeps `PERTURB_PASS=6/6`.
5. **Two counters are not re-measurable here.** The round-50 counter's `R49_REGRESSION` leg and the round-52 counter's `REAL` leg fail on inputs the host no longer has (the deleted campaign cache; INFERENCE, the R49 reason was not printed). So their current verdicts (`LEGS=4/5`, `LEGS=8/9`) are environment-bound, not refutations; the forge-shape still passes 8 of 9 legs on the round-52 counter.
6. **One row is UNOPENED.** R59-1 cites `corpus/lessons/round-59.md:27` for a forged builder that injects `=PASS` into stderr. `grep -n -i inject .ufo/waves/round-59/w1/R59Executor09.md` prints nothing; the seat file contains only the needle analysis (`ref_pass` true in 0 combinations, lines 69–89). The claim rests on the lesson alone.
7. **Calibration defects in the source lessons (the rows keep the source figure; the discrepancy is recorded).** Round-51 lesson Mistakes 8 says "supplement 1/6 and 3/6"; `corpus/evidence/round51/controls/c1-supplement-controls.txt` prints `SUPPLEMENT_LEGS=1/10` and `3/10`. Round-53 lesson says `forge-c1.py` is 189 lines; `wc -l` gives 187. Round-61 lesson says 8–12/20 for the amended counter; `ExecForgeSeqRed.md` shows 8–11/20 at the four seeds it lists.
8. **C2 is not landed at the lane HEAD.** `corpus/knowledge/openat2-resolve-r62.md` and `corpus/evidence/round62/openat2-probe.py` do not exist at `d173d14`; the candidate probe is at `controls/candidate-openat2-probe.py`. The red-before (`c2v2-before.txt`, `C2=FAIL`, exit 1) and the v2 echo control (`c2v2-controls.txt:15`, `echo-claim … ECHO=0/1`) are opened.

## Evidence (commands and observed output)

E1. Pointer opens (read or grep, output truncated to the matched line): `corpus/lessons/round-61.md:33-75`, `round-50-verifier-spotcheck.md:36-38`, `round-51.md:15,18,22`, `round-52.md:16,25,138`, `round-53.md:17-19,27,29`, `round-54.md:17`, `round-55.md:16,34`, `round-56.md:9`, `round-57.md:88-105`, `round-58.md:24-26`, `round-59.md:27`, `round-60.md:21-23`. All opened except the R59-1 injection line (finding 6).

E2. `python3 -B corpus/evidence/round62/c1v2-battery.py --counter corpus/evidence/round62/c1v2-count.py --work <absent dir>` → `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=PASS`, exit 0; wall time 180 s.

E3. `python3 -B corpus/evidence/round62/c1v2-count.py --builder tools/build-spans.py --work <absent dir>` → `LEGS=20/20 C1V2=PASS`, exit 0; wall 7.75 s.

E4. `python3 -B corpus/evidence/round53/c1-count.py --tool corpus/evidence/round53/controls/forge-c1.py --seed 7 --work <dir>` → `LEGS=8/8`, `C1=PASS`, exit 0.

E5. `python3 -B corpus/evidence/round53/c1-count.py --per-leg 0 --seed 5 --work <dir>` → `LEGS=8/8`, `C1=PASS`, exit 0; `grep -c '^case' <output>` → 0.

E6. `python3 -B corpus/evidence/round50/c1-count.py --tool corpus/evidence/round50/controls/forge-tool.py` → `BASELINE=PASS rc=0 findings=26`, `PERTURB_PASS=6/6`, `R49_REGRESSION=FAIL rc=1`, `LEGS=4/5`, `C1=FAIL`, exit 1.

E7. `python3 -B corpus/evidence/round52/c1-count.py --tool corpus/evidence/round52/controls/forge-shape.py --work <dir>` → `PARAS` … `REFUSE` PASS; `REAL=FAIL pinned capture missing or digest differs`; `LEGS=8/9 C1=FAIL`, exit 1. Same counter on `corpus/evidence/round51/controls/forge-dirname.py` → `LEGS=0/9 C1=FAIL` (all nine legs fail).

E8. `python3 -B corpus/evidence/round61/digest-ellipsis-check.py corpus/evidence/round61/claims.md` → `MISMATCH bcca093e…b5624`, `MISMATCH f1d8b6fd…cfff9ef`, `DIGEST_ELLIPSIS tokens=8 matched=6 mismatched=2`, rc 1.

E9. `grep -n Traceback corpus/evidence/round62/c1v2-count.py` → no output; `grep -n 'C1V2_SEED\|argv' …` → seed read from `os.environ.get("C1V2_SEED")` at line 687.

E10. `grep -n -i inject .ufo/waves/round-59/w1/R59Executor09.md` → no output (R59-1 UNOPENED).

E11. `sha256sum corpus/evidence/round62/c1v2-count.py corpus/evidence/round62/c2v2-count.py | cut -c1-16` → `b7016fba91b03460`, `817d5fc0b94e9fc8` (the claims' prefixes).

E12. `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain` run after my counter and battery runs: only the pre-existing untracked `.ufo/waves/round-62/w1*` entries (other seats' files); no lane file written by me. Lane HEAD `d173d14`.

## Row status

- 29 rows (IDs R49-1 … R62-2). Opened: 28. Unopened: 1 (R59-1). Re-run by me: R50-1, R51-1, R52-1, R53-1, R53-3, R62-1 (battery and v2 count), plus the round-53 and round-51 counters above.
- Rows R55-3 and R57-1 cite lessons plus wave-report text; the seat reports themselves were checked by grep only.
- Round 49–54 counters that need the deleted campaign cache (R50, R52) are not re-measured beyond E6–E7.

## Limits

- The table is counter-level by design. Process defects (report filed before settlement, reused seat names, dispatch digest, missing seat report) are excluded and sit in the lessons.
- I did not run the frozen round-49, 54, 55, 56, 57, 58, 60 or 61 counters on their own candidates; their rows rest on the lessons plus the opened seat or receipt files. R58-1 is code-read only.
- The round-61 draft `.ufo/waves/round-61/w1/ScribeStreak.md` (13 rows) and `RevStreak.md` are prior work; this table extends them to round 62. Its row 58 says "unreachable" and its row 56 "none at freeze"; both are consistent with the rows here.
- Not checked: `corpus/evidence/round53/weakness-streak.py` (round-61 draft says it exits 1; not re-run).

## Hygiene

- Installs: none.
- Scratch: `/fast/scratch/hyaku/chousa-r62/ScribeStreak` (created, used for the runs above, removed before this report).
- Writes: `.ufo/waves/round-62/w1/ScribeStreak/streak.md` and this report only.

VERDICT: STREAK_ROWS=29 unopened=1
