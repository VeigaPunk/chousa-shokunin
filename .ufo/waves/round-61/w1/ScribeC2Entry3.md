# ScribeC2Entry3 — round 61 w1 — C2 independent entry draft (scribe)

Scope: draft `corpus/knowledge/derived-output-safety-r61.md` as a candidate in the shape `c2-count.py` reads, from S134/S135 (rendered man pages) and S136 (`.ufo/waves/round-56/w1/R55W2SentBuilder.md`). No lane file under `corpus/`, `tools/`, `SKILL.md` or `corpus/evidence/round61/` was written. Draft: `.ufo/waves/round-61/w1/ScribeC2Entry3/entry.md`.

## Findings

1. **Counter passes on the scratch mirror** (not on the lane; the lane has no entry and the kill rule applies to the landed commit only):
   `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=7/7 COVERAGE=1/1 CLAIMS=1/1 LIMITS=1/1 CENSUS=1/1 C2=PASS` (rc 0, no detail lines).
2. **Shape:** 7 located quotes (S134 ×3, S135 ×2, S136 ×2), 4 claims: Claims 1–3 are the three principles (O_NOFOLLOW guards only the trailing component; O_CREAT|O_EXCL refuses any symbolic link at the name; rename overwrites a link at newpath and replaces the final name atomically), Claim 4 is the sourced observation from S136 (h2, h3). Limits: 5 bullets.
3. **Quote selection converges with the positive control.** I located the sentences myself in the rendered text; they are verbatim the same sentences the positive control uses for Q1–Q5 and its S136 Q7–Q8 (my Q6–Q7). The only positive-control quote I did not use is the rename(2) window sentence (`However, there will probably be a window...`). Claim wording differs. Low independence of selection is expected: these are the single sentences each source uses for the behaviour. L1 should weigh the merge on claim wording and limits, not on quote choice.
4. **Calibration.** Claim 1's consequence (a writer must check the output directory itself) is tagged `[INFERENCE]` in the claim text, since the page states the trailing-component rule only. The non-atomicity of check-then-write is in Limits, tagged `[INFERENCE]`, as no quote states it. Claim 2 is limited to a link present before the create; a post-create swap is not claimed. Claim 4 is limited to one seat's fixture runs at revision 29cfb12 (tier B, not re-run).
5. **Counter limit, observed:** the `CLAIMS` check only requires ≥2 shared ≥5-letter words with the cited quotes. My claims were written to meet that and to follow from the quotes; the PASS on claims is structural, which the counter docstring and the frozen controls already record (`echo-claims` PASSES). Reviewers must judge whether each claim follows.
6. **Quotes located (exact line in my renders / file):**
   - Q1 S134: `open2.txt:147` "If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP." (20 words)
   - Q2 S134: `open2.txt:147` "Symbolic links in earlier components of the pathname will still be followed." (12)
   - Q3 S134: `open2.txt:123` "symbolic links are not followed: if path is a symbolic link, then open() fails regardless of where the symbolic link points." (21; the sentence starts "When these two flags are specified," at the same line, which I cut to stay ≤25 words)
   - Q4 S135: `rename2.txt:46` "If oldpath refers to a symbolic link, the link is renamed; if newpath refers to a symbolic link, the link will be overwritten." (23)
   - Q5 S135: `rename2.txt:38` "it will be atomically replaced, so that there is no point at which another process attempting to access newpath will find it missing." (23; the sentence starts "If newpath already exists," — cut to stay ≤25)
   - Q6 S136: `R55W2SentBuilder.md:33` "victim/S404-9.txt(28) before → absent after; victim/S001-1.txt(457) created; exit 0, stderr empty" (11)
   - Q7 S136: `R55W2SentBuilder.md:34` "victim/IMPORTANT.txt 10→457 B, victim/LEDGER.tsv 74→243 B (both targets truncated); exit 0" (11)

## Evidence pointers (commands and observed output)

- Render (same environment as the counter's `render_man`):
  `env MANWIDTH=1000 LC_ALL=C.UTF-8 man -l /usr/share/man/man2/open.2.gz | col -bx > …/open2.txt` → rc 0, 516 lines; `…/rename.2.gz` → rc 0, 210 lines. (`MANWIDTH=1000 man -l FILE | col -bx` as the row specifies, plus `LC_ALL=C.UTF-8` to match the counter.) Quotes were read by range from these files; the `grep` tool returned `Path not found` for the `/fast/scratch` path, so I used `read` ranges instead.
- Provenance of S136: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --quiet 9eef15e -- .ufo/waves/round-56/w1/R55W2SentBuilder.md` → rc 0; `git … status --short -- <same path>` → empty. The file read is byte-identical to lane commit 9eef15e.
- Mirror and run: scratch builder `…/ScribeC2Entry3/mirror.py` copies `corpus/` (70 MB) and `R55W2SentBuilder.md` into `…/work/mirror`, inserts `controls/c2-positive-rows.txt` before `## Paths` in the mirror's `SOURCES.md` (same logic as `run-c2-controls.py` `rows_into`), writes my draft to `corpus/knowledge/derived-output-safety-r61.md`, then runs `python3 -B <lane>/corpus/evidence/round61/c2-count.py --root <mirror>` → the output line above, rc 0. The counter file was not edited.
- Lane registry: `grep -c "| S13[4-7] |" corpus/SOURCES.md` → 0 (no S134–S137 rows in the lane before the L1 appends them), so the mirror rows are the only rows the counter read.

## Not done / out of scope

- The entry is not landed; no commit, no SOURCES.md append (L1 only), no `corpus/knowledge/` write in the lane.
- No controls re-run (`run-c2-controls.py` not executed; the mirror logic is copied, not the control variants).
- No external fetch; no man7.org HTML opened (as the claims file's access disclosure says).

## Tooling

No installs. No PATH changes. Scratch `/fast/scratch/hyaku/chousa-r61/ScribeC2Entry3/` removed before yield.

VERDICT: ENTRY3_C2=PASS quotes=7 claims=4
