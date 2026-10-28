# ScribeC2Entry1 — round 61 w1 — C2 candidate entry (scribe)

## Findings

1. **Draft delivered:** `.ufo/waves/round-61/w1/ScribeC2Entry1/entry.md` — 53 lines, 987 words. Shape follows the
   counter docstring: source/verified-at/recheck trio in the first 3 lines; a 6-step ordered checklist; `## Located
   quotes` with 11 quotes (S134 ×3, S135 ×3, S136 ×5); `## Claims` with 6 claims; `## Limits` with 4 bullets.
2. **Counter, on a scratch mirror of the lane (final draft):** `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=11/11 COVERAGE=1/1 CLAIMS=1/1 LIMITS=1/1 CENSUS=1/1 C2=PASS`, rc 0.
   Mirror = lane `corpus/` copy + the S136 file at its lane path + `controls/c2-positive-rows.txt` inserted above
   `## Paths` in the mirror's `SOURCES.md` (same procedure as `run-c2-controls.py`). The lane's own `SOURCES.md`
   was not edited and has no S134–S137 rows (`grep -c -E '^\| S13[4-7] '` → `0`).
3. **Quotes located by me, not copied from the control:**
   - S134 (`open.2`): lines 120–123 (O_EXCL, "symbolic links are not followed…") and 147 (O_NOFOLLOW, "trailing component…", "earlier components…") of `MANWIDTH=1000 LC_ALL=C.UTF-8 man -l /usr/share/man/man2/open.2.gz | col -bx`.
   - S135 (`rename.2`): lines 38 ("it will be atomically replaced…", "window in which both oldpath and newpath refer…") and 46 ("If oldpath refers to a symbolic link…") of the rendered page.
   - S136 (`R55W2SentBuilder.md`): line 11 and 12 (summary table, h2 and h3 rows), line 27 ("Nothing inspects what was already there."), lines 33–34 (h2 and h3 transcript lines).
   - Eight of the eleven quotes are the same strings as the positive control's Q1–Q8. Q9–Q11 (S136 table rows and line 27) are mine.
4. **Calibration:** every claim is tied to quotes that say it; checklist steps that go beyond the quotes are tagged `[INFERENCE]` (per-component `lstat` as a design choice, removing the temp name on the error path, writing the index last, a fixture-based tree check, and the check-then-write gap listed in Limits). I removed a "must cover every component" clause from Claim 1 during drafting so the claim states only what Q1 and Q2 say.
5. **Claim 5 is the weakest link, disclosed:** it uses Q9 and Q10, which are rows of the summary table at the top of S136 (lines 11–12), not "transcript lines … in section 1" as the S136 registry anchor reads. The counter accepts them because the S136 anchor check is substring-only (`h2`, `h3` occur in the anchor cell). The claim's content (symlink at the spans directory; symlinked span file and `spans.tsv`) is supported by those table rows only; the transcript lines Q7/Q8 support removal, creation and truncation. A reviewer should decide whether the registry anchor should say "summary table and transcript lines".
6. **Counter limit, as recorded:** the counter is structural and does not judge that claims follow from quotes. I did not run the controls (`run-c2-controls.py`) against my draft; that is the L1's merge check, not a claim of mine.

## Evidence

- `python3 -B .../c2-count.py --root <mirror>` (final draft) → `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=11/11 COVERAGE=1/1 CLAIMS=1/1 LIMITS=1/1 CENSUS=1/1 C2=PASS`, exit 0. Earlier run on the pre-tightening draft: same line, exit 0. Driver `prep-run.py` lived in scratch and is deleted.
- `man -l` renders (run for quote location): open.2 lines 120–123, 146–147 printed; rename.2 lines 38, 46 printed (default locale for these two greps; the counter's own render uses `LC_ALL=C.UTF-8`, and its quote check passed).
- S136 source identity: `git -C <lane> show 9eef15e:.ufo/waves/round-56/w1/R55W2SentBuilder.md | cmp - <working copy>` → no output, `SAME_AS_9eef15e`.
- S136 lines read: `sed`-equivalent range read, lines 1–43 (table lines 11–12, section 1 lines 24–40).
- Man-page package: `/var/lib/pacman/local/man-pages-6.19-1/desc` → `%VERSION%` `6.19-1` (file read only; pacman not run).
- Lane state (observation only): `git -C <lane> rev-parse --short HEAD` → `9f32ac0`; `cat-file -t 2b0e17b` → `commit`; `merge-base --is-ancestor 2b0e17b HEAD` → ancestor. The lane has moved past the freeze commit named in the claims; nothing here depends on the difference.
- Corpus size seen when copying the mirror: `du -sh corpus` → `70M` (in scratch only).
- Scratch `/fast/scratch/hyaku/chousa-r61/ScribeC2Entry1/` removed (`ls` → no such file).

## Installs

None. No tool was installed or updated.

## Out of scope

No fleet, sibling-lane or shokuknow write; no git/jj mutation; no network; no change under `corpus/evidence/round61/`, `tools/`, `corpus/`, or `SKILL.md`; no subagent dispatch.

VERDICT: ENTRY1_C2=PASS quotes=11 claims=6
