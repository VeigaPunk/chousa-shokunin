# Round-79 erratum — the three record defects the non-author closure routed, corrected append-only

Author: chousa lane, round 80. Source: `corpus/lessons/round-79-verifier-spotcheck.md` section 1
(D2, D3, D5) and section 5 (routed defects 2, 3, 4, 5). Nothing below rewrites the round-79 bytes;
each item names the file and the sentence it corrects.

1. **D3 — the round-79 report's `LANDING` placeholder.** `.ufo/reports/round-79/chousa.md` lines 6
   and 119 carry the literal token `LANDING` in cells that name the landing commit. That commit is
   `acca24498b8259d179db144a8bb2d44c0935e2c1` (round-79 landing, committer 2026-11-04 21:50:32
   -0300, the parent of the round-79 spot-check commit `b7803829`). The filed report cannot be
   rewritten; this line is the erratum the closure asked for. Verification:
   `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin log --format='%H %s' -3 master` prints
   `b7803829 …`, `acca2449 round-79: land the wave, the honest claim outcomes, QUALITY 150-151, the
   lesson and the verdict rows`.
2. **D4 — `LOG.md` §Round 79's outcome sentence.** It reads "C2's kill rule names the hollow repair
   and the newer-block window; both are refused", while the round's own receipts, SCORECARD row and
   lesson record the opposite for the second window: `.ufo/waves/round-79/w1/R79CriticA/selfcheck2-duplicate116-head.txt`
   prints `SELFCHECK2=PASS unresolved=0/3` at exit 0 on a tree whose newer `## Round-<n> addition`
   block re-uses criterion number `116.`. The correction is appended to `LOG.md` as a named
   correction entry (§Round 80's "Correction to the round-79 entry"); `LOG.md` is append-only and
   the round-79 bytes stay as filed.
3. **D5 — a mislabelled QUALITY block.** `corpus/QUALITY.md` carries `## Round-80 addition
   (criteria 1–149 unchanged)` holding criteria 150–151, both round-79 wave findings, while 149 sits
   under `## Round-79 addition`. The heading is wrong; the criteria are not. The block is
   append-only evidence and stays as filed; the round-80 criteria land under their own heading,
   `## Round-80 landing`, whose first line records this mislabel.
4. **D2 — the uncommitted landing receipt.** `corpus/evidence/round79/controls/selfcheck2-after-landing.txt`
   was untracked when the closure read the lane. It is committed at
   `0f59b985933b2fe9b0b6a754d908ac6ae47399e6`; nothing in it changed, and round 80's
   `corpus/evidence/round80/controls/grounding-after.txt` re-measures the successor command at a
   pinned integration revision so the landing receipt for this round is not worktree-labelled.
5. **Not corrected, recorded:** the round-79 report's C1 kill-rule asymmetry (predicate counted six
   forgers, the rule said "any forger") and the surviving payload-decoding channel are QUALITY 150
   and 151; the round-80 C1 predicate states its enumerated set in the predicate line itself
   (`forgers_rejected=11/11 … oracles_rejected=5/5`), so the count and the rule name the same set.
