# ScribeGate — round 61 w1 — Gate draft for S134–S137

Draft delivered at `.ufo/waves/round-61/w1/ScribeGate/gate.md` (the `## Gate` section for `corpus/lessons/round-61.md`;
that lesson file was not written by this seat and does not yet exist at HEAD `9f32ac0`). Access date for all rows 2026-10-28.

## Findings

1. S134 (open(2)) — ADMIT, tier A. Quotes Q1, Q2 (rendered line 147) and Q3 (line 123) located in
   `/usr/share/man/man2/open.2.gz` rendered with `MANWIDTH=1000 man -l | col -bx`. The `teaches` conclusion "a writer must check the
   earlier components itself" is [INFERENCE]: the page states only that earlier components are still followed.
2. S135 (rename(2)) — ADMIT, tier A. Quotes Q4 (line 46), Q5 and Q6 (line 38) in `/usr/share/man/man2/rename.2.gz`. "instead of
   writing through it" is [INFERENCE]; the page does not discuss writing through a link.
3. S136 (R55W2SentBuilder seat report) — ADMIT, tier B. Quotes Q7 (`.ufo/waves/round-56/w1/R55W2SentBuilder.md` line 33, case h2)
   and Q8 (line 34, case h3). The file at `9eef15e` is byte-identical to the worktree copy. Scope: rev 29cfb12, seat fixtures; no re-run here.
4. S137 (builder docstring, "Output safety (round 61)") — REJECT. The paragraph is absent from `tools/build-spans.py` at HEAD `9f32ac0`,
   `2b0e17b` and `9eef15e` (grep count 0 in each). The only copy is the control `controls/ref-build-spans.py:34`.
   Reject reason: a docstring is intent, not evidence. Flip: `c1-count.py` exit 0 with `LEGS=20/20 C1=PASS` on the shipped bytes.
5. Row corrections for the L1 before the rows are written: S137 `teaches` says "caps", but the 64 MiB caps are in a separate
   paragraph of the reference builder (lines 16-19), not in "Output safety (round 61)"; S137 `location` names a file that does not
   yet carry the paragraph.
6. Calibration: every quote the gate uses is the entry's own form (Q3 is the 21-word form, not the 16-word shorter one).
   The counter's `anchor in row location` rule holds for all eight entry quotes (`O_NOFOLLOW`, `O_EXCL`, `DESCRIPTION`, `h2`, `h3`).

## Evidence (commands and observed output)

- Man render, reopened: `MANWIDTH=1000 LC_ALL=C.UTF-8 man -l /usr/share/man/man2/open.2.gz | col -bx` → 516 lines;
  `…rename.2.gz` → 210 lines; footer `Linux man-pages 6.19 … 2026-02-08`.
- `sha256sum /usr/share/man/man2/open.2.gz /usr/share/man/man2/rename.2.gz` →
  `a525cf9f…abb3f5`, `4b6d62db…abb3f5` (full digests in gate.md).
- Quote check script (scratch, `python3 -B`, reads the rendered text, the 9eef15e file and the control):
  ```
  Q1 S134 words=20 found=True rendered man line(s) [147] ok=True
  Q2 S134 words=12 found=True rendered man line(s) [147] ok=True
  Q3 S134 words=16 found=True rendered man line(s) [123] ok=True   (entry form, 21 words: found=True)
  Q4 S135 words=23 found=True rendered man line(s) [46] ok=True
  Q5 S135 words=23 found=True rendered man line(s) [38] ok=True
  Q6 S135 words=19 found=True rendered man line(s) [38] ok=True
  Q7 S136 words=11 found=True R55W2 9eef15e line(s) [33] ok=True
  Q8 S136 words=11 found=True R55W2 9eef15e line(s) [34] ok=True
  G1 S137 words=17 found=True controls/ref-build-spans.py line(s) [34] ok=True
  QUOTES_OK=9/9
  ```
  The 8 entry quotes (`c2-positive-entry.md`, Q1–Q8) were checked in a second run: each `found=True`, words 20/12/21/23/23/19/11/11,
  anchor in the row's location cell `True` for all eight.
- Row cells: `c2-positive-rows.txt` → each of S134–S137 has 11 cells; tiers A, A, B, C; status mined, mined, mined, rejected;
  `opened` 2026-10-28 for all four.
- Shipped builder: `grep -c 'Output safety (round 61)' tools/build-spans.py` → `0`; `git show 9eef15e:tools/build-spans.py | grep -c 'Output safety'` → `0`;
  `git show 2b0e17b:tools/build-spans.py | grep -c 'Output safety'` → `0`.
- Control heading: `grep -n 'Output safety' corpus/evidence/round61/controls/ref-build-spans.py` → `34:Output safety (round 61). …`.
- `git -C <lane> show 9eef15e:.ufo/waves/round-56/w1/R55W2SentBuilder.md | cmp - <worktree copy>` → silent (equal).

## Not done / limits

- Did not run `c2-count.py`: the entry it reads does not exist at HEAD, so it would print `ENTRY=0/1 … C2=FAIL`. That run belongs to the L1 after the entry lands.
- Did not re-run any builder or the seat's S136 fixtures; S136 is cited as the seat's observation, graded B.
- No URL exists for S134/S135 (no network use; man7.org HTML not opened). The rows carry the installed-package path instead.
- Tooling: one read-only query `pacman -Qi man-pages` (output `Version 6.19-1`); no install, update or upgrade. No `~/.local/bin` write.
- Writes: `.ufo/waves/round-61/w1/ScribeGate/gate.md`, this report, and scratch `/fast/scratch/hyaku/chousa-r61/ScribeGate/` (removed before yield). No git mutation; no frozen file touched.

## Spot-check request (non-author)

- Admit: S136 — open `.ufo/waves/round-56/w1/R55W2SentBuilder.md` lines 33–34 at commit `9eef15e` and check Q7 and Q8 verbatim.
- Reject: S137 — `grep -n 'Output safety' tools/build-spans.py` should match nothing; `…controls/ref-build-spans.py` should match line 34 only.

VERDICT: GATE_ROWS_WRITTEN=4/4 quotes_reopened=9
