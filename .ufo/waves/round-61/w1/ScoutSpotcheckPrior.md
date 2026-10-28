# ScoutSpotcheckPrior — round-61 status of round-60 routed defects

Four items in `corpus/lessons/round-60-verifier-spotcheck.md` lines 44–47. The freeze closes the pre-dispatch digest and control defect. The Gate, the sourced-row grounding, and the round-61 report headings stay open. The committed round-60 report already has the contract headings the spot-check called missing.

## 1. Freeze digest and discriminating controls — addressed

The freeze binds the wave digest to the final claims bytes and includes no-op, forge, and positive controls. It does not record an operability or depth move.

Pointer: `corpus/evidence/round61/claims.md` lines 5–16 (digest from final bytes, QUALITY 116; controls a–f) and sections C1, C2, Amendment A1. Commit `2b0e17b2a3b20a5f350e4dc4ddd5900c4d1f952c`, parent `1661b85bfa84d3dc75712d64f79034265b8831d3`, 2026-10-28 18:52:24 -0300, subject `round-61: amend freeze A1 (counter order/process-group/limits) before dispatch`. First freeze `1661b85b` subject `round-61: freeze claims, counters and controls before dispatch`. Base `9eef15e7c0e0ae0055228e7066dc1eec676a91d2` is an ancestor.

`sha256sum` of the worktree file and of `git show 2b0e17b2:corpus/evidence/round61/claims.md` are both `9afec8d493f0ba511a256f38cd5098ff508f9ed311c6c49ff5383add9ce0acec`. Worktree `git hash-object` and the commit blob are both `5cbaa992f42031713726f680d8d05b7033a45598`. That digest is the claims line in `.ufo/waves/round-61/w1-digests.txt` and in the `w1-dispatch.json` context. It is absent from `claims.md` itself and from `.ufo/prompts/chousa-round-61.md`.

Receipts read, counters not re-run. `controls/c1-before.txt`: `LEGS=7/20 C1=FAIL` exit 1 at seeds 61001 and 61002. `controls/c1-controls.txt`: base 7/20, `noop0` 1/20, `always2` 14/20, `forge-token` 7/20, `naive-guard` 10/20, `reference` 20/20, M01–M14 each fail the named legs, `CONTROLS_UNEXPECTED=0` exit 0. `controls/c2-before.txt`: `ENTRY=0/1 … ROWS=0/3 … C2=FAIL` exit 1, S134–S136 absent. `controls/c2-controls.txt`: absent and forged cases `C2=FAIL`, positive `C2=PASS`, `echo-claims` also `C2=PASS` (claims.md lines 87–89 name that structural limit), `C2_CONTROLS_UNEXPECTED=0`.

`git diff --stat 1661b85b 2b0e17b2 -- corpus/evidence/round61` is five files: `c1-count.py`, `claims.md`, `c1-before.txt`, `c1-reference.txt`, `sniff-sweep.txt` (54 insertions, 22 deletions). `c1-controls.txt` blob `ee12adc97c612d5d5789b8a617a2255cc1d3d342` and `c2-controls.txt` blob `5c5210fc42b96de5a3e930e0613118a68a36e43d` are identical at both commits. Identical bytes leave open whether those two receipts were regenerated.

Report constraint that the freeze already obeys: do not score operability or depth moved. C1’s kill rule is `LEGS=20/20` at three fresh seeds and `REAL_REBUILD=3/3`. C2’s kill rule is `C2=PASS` on the landed commit. Neither landing is in the tree.

## 2. Round-local Gate (admit, reject, non-author review) — open

The freeze names the pair and assigns quote judgment to closure. It does not record the Gate.

Pointer: `claims.md` section C2, lines 69–95. S134–S136 are “each opened in this round (2026-10-28)”. Lines 92–95: S137 is a rejected own-work row and “gives the round’s Gate its reject”; non-author reviewers and the closure re-read the claims. Row text: `controls/c2-positive-rows.txt` (S134–S136 `mined`, `opened` 2026-10-28, used-by `corpus/knowledge/derived-output-safety-r61.md`; S137 `rejected`, used-by `—`). Commit `2b0e17b2`.

`corpus/SOURCES.md` last registry row is S133 at line 143. S134–S137 are absent there. S101 is `opened` 2026-10-25 (line 111). `corpus/lessons/round-61.md` is absent. `tools/build-spans.py` has no `Output safety (round 61)` paragraph, so the rejected source text is not in the tree. `corpus/knowledge/derived-output-safety-r61.md` is absent.

The report must record a round-local Gate with at least one admit and one reject (the freeze’s names are S134–S136 and S137), access date, and a located quote of at most 25 words, plus a named non-author reviewer. W1 seat output is not that review.

## 3. Honest frontier; S101 is not this round’s sourced row — open

Pointer: `claims.md` section C2 lines 69–71 and Access disclosure lines 97–98 (S134 and S135 from installed man pages, no URL; man7.org HTML not opened this round). Commit `2b0e17b2`. `controls/c2-before.txt` shows S134–S136 absent and `C2=FAIL`.

S101 remains the 2026-10-25 row. The sourced claim is not grounded in `corpus/SOURCES.md`. The conformance defect stands until a row opened this round is in the registry and the entry cites it.

The report’s Sources & frontier section must keep S101 off the “opened this round” list. Census file read, not re-run: `.ufo/waves/round-61/census-start.txt` ends `chousa ok` and `exit=0` and prints no row count.

## 4. Exact headings — open for the round-61 report; the round-60 premise is false

Contract: `/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-61.md` section 4, lines 99–119. Required order: Work performed, Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN. Lines 121–125: skipping Sources & frontier or Trend verdicts is a conformance defect, and the other missing sections fail the round.

Committed report `739025700c12357a59fd665f4574c1a6bfb619df` (the commit the spot-check names; that path’s `git log` has this one commit; `status --porcelain` empty) has those six `##` headings in that order, including `## Sources & frontier` at line 26 and `## Trend verdicts` at line 30. The spot-check line 9, that those headings are absent and the content sits under alternative headings, does not match that commit.

The lane freeze does not mention heading text. `claims.md` section Not claimed (lines 115–119) only points unclaimed axes at “the report’s trend verdicts”.

`/home/vgpnk/Projects/shokunin/.ufo/reports/round-61/chousa.md` does not exist. The round-61 report must use the exact headings `## Sources & frontier` and `## Trend verdicts`, in the section 4 order. It should state that the committed round-60 report already has them.

## Evidence

Lane git is `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin`. Report history is read-only `git -C /home/vgpnk/Projects/shokunin`.

- `sha256sum corpus/evidence/round61/claims.md` → `9afec8d493f0ba511a256f38cd5098ff508f9ed311c6c49ff5383add9ce0acec`
- `git show 2b0e17b2a3b20a5f350e4dc4ddd5900c4d1f952c:corpus/evidence/round61/claims.md | sha256sum` → the same digest
- `git rev-parse 2b0e17b2…:corpus/evidence/round61/claims.md` and `git hash-object` of the worktree file → `5cbaa992f42031713726f680d8d05b7033a45598`
- `git log -1` on `2b0e17b2` → parent `1661b85b`, date 2026-10-28 18:52:24 -0300, subject as in section 1
- `git merge-base --is-ancestor 9eef15e7 2b0e17b2` exit 0; `1661b85b` exit 0
- `git diff --stat 1661b85b 2b0e17b2 -- corpus/evidence/round61` → the five files in section 1
- control blobs at both freeze commits: `c1-controls.txt` `ee12adc97c612d5d5789b8a617a2255cc1d3d342`; `c2-controls.txt` `5c5210fc42b96de5a3e930e0613118a68a36e43d`
- `git show 739025700c12357a59fd665f4574c1a6bfb619df:.ufo/reports/round-60/chousa.md | grep -n '^#'` → line 1 title, then `##` at 3, 16, 21, 26, 30, 36
- `git status --porcelain -- .ufo/reports/round-60/chousa.md` → empty
- `ls /home/vgpnk/Projects/shokunin/.ufo/reports/round-61/chousa.md` → no such file

`c1-count.py` and `c2-count.py` were not re-run. No tool install.

VERDICT: ROUTED_DEFECTS_ADDRESSED=1/4 open=gate-admit-reject,sourced-row-grounding,report-headings
