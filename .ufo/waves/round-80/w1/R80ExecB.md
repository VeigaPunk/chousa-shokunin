# R80ExecB — C2 calibration reproduction, both directions (lane chousa, round 80)

Seat: leaf executor. Scope: reproduce frozen claim C2 (calibration) in both directions and
validate the `GATE-RECORD` grammar the L1 intends to land, before it lands. Frozen predicate
set: `corpus/evidence/round80/claims.md` (read first); previous-round non-author closure:
`corpus/lessons/round-79-verifier-spotcheck.md` (read before scoring). Counter sha256 measured
on the committed bytes I ran:
`d9e426216665a098cd90adf8fbf5e5dd62e02dc7b5b707c322b404b3eb55c553` — equals the claims.md
instrument row for `gate-grounding-check.py`.

## Result (one line)

C2 reproduces in both directions with zero deviations from the frozen predicate; all four
candidate quotes occur verbatim at their named rev/path/line with exactly the stated word
counts; the R4 negative control fires and reverts clean. The grammar is fit to land as-is.

## (a) BEFORE — frozen do-nothing control, reproduced

Command (tool run from its committed lane path; LANE resolves to the lane repo):

```
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round80/gate-grounding-check.py --rev b7803829922770b890e9f4efdd30d12c3695439a
```

Observed (receipt `grounding-before-run.txt`, exit **1**):

```
LANE_REV=b7803829922770b890e9f4efdd30d12c3695439a SINCE_ROUND=79 TIPS=191 AUDITED=3
ROW S196 record=none quote_words=- location=- verdict=UNRESOLVED
ROW S197 record=none quote_words=- location=- verdict=UNRESOLVED
ROW S198 record=none quote_words=- location=- verdict=UNRESOLVED
GATE_GROUNDING=FAIL unresolved=3 superseded_resolved=0 audited=S196,S197,S198
```

Matches the frozen predicate (`GATE_GROUNDING=FAIL unresolved=3 superseded_resolved=0
audited=S196,S197,S198`, exit 1, `record=none` on all three rows) and is byte-identical to the
committed control `corpus/evidence/round80/controls/grounding-before.txt`. The three rows are
decided by the `- Admit S196 / - Admit S197 / - Reject S198` bullets in
`corpus/lessons/round-79.md` (round ≥ since-round 79) and carry no `GATE-RECORD` at the base rev.
Note: TIPS=191 of 198 rows — 7 registry rows are already superseded parents at the base rev.

## (b) AFTER — candidate landing built in a scratch mirror

Mirror: `/fast/scratch/hyaku/chousa-r80/R80ExecB/mirror`, a `git clone --shared` of the lane
(shared alternates so revs `b7803829…` and `3eb4a3c…` resolve — a plain `git archive` mirror
would fail R1 for every record). `git rev-parse --show-toplevel` asserted equal to the mirror
before the first commit. Worktree checked out at the base rev `b7803829…`, then:

- `corpus/SOURCES.md`: four candidate rows S199–S202 inserted immediately after the last table
  row (S198, line 210; the file's trailing correction prose stays last). Each row has exactly 13
  cells with `teaches` in cell 7; S200/S201/S202 teach cells open `supersedes S196 —` /
  `supersedes S197 —` / `supersedes S198 —`.
- `corpus/lessons/round-80.md`: four `GATE-RECORD` lines in exactly the grammar the counter
  parses (rev=40-hex, path repo-relative, line, words, quote as one line).
- `corpus/evidence/round80/gate-grounding-check.py`: counter copy committed into the mirror
 (sha256 above, byte-identical), so its `LANE` (`parents[3]` of `__file__`) resolves to the
  mirror and the cited instrument bytes are committed bytes.

Quote verification (receipt `quotes-verified.txt`, re-checked against the mirror's own object
store via `git -C mirror show`): every quote occurs verbatim on the named line, word counts
12 / 20 / 25 / 2 for S199/S200/S201/S202. **No candidate needed correction.** S201's 25 words
sits exactly at the ≤25 contract bound.

Candidate commit: `2916e063638085630c2a232701b802b52fec4f7a`
(identity `R80ExecB scratch mirror <r80execb@scratch.invalid>`; no commit anywhere but the
scratch mirror). Receipt `mirror-git-log.txt`.

## (c) AFTER — counter against the mirror commit

Command: `python3 -B <mirror>/corpus/evidence/round80/gate-grounding-check.py --rev 2916e063638085630c2a232701b802b52fec4f7a`

Observed (receipt `grounding-after-run.txt`, exit **0**), exact final line:

```
GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3 audited=S199,S200,S201,S202
```

with `record=ok` on all four rows (locations `…spotcheck.md:222@b78038299227`,
`QUALITY.md:1056@b78038299227`, `QUALITY.md:1054@b78038299227`,
`atkB2-new-block-window.txt:11@3eb4a3cad8fe`) and `SUPERSEDED S196 by S200 / S197 by S201 /
S198 by S202 … verdict=RESOLVED`. `TIPS=192 AUDITED=4`. Matches the frozen predicate exactly.

## (d) Negative control — one-off `words=` cell

Changed S200's `words=20` → `words=21` (one off the real count), committed
(`41e66e8f53fc9c64aacd1387e677ffa629cb94aa`), re-ran (receipt `grounding-negative-r4.txt`,
exit **1**):

```
ROW S200 record=bad quote_words=21 location=R4 quote is 20 words, record says 21 verdict=UNRESOLVED
...
GATE_GROUNDING=FAIL unresolved=2 superseded_resolved=2 audited=S199,S200,S201,S202
```

R4 fires as designed. Coupling worth knowing at landing: because S196's supersession resolves
only if S200's record passes, the bad tip also un-resolves its parent
(`unresolved=2 superseded_resolved=2`) — a defective superseder can never hide behind its
parent. Reverted with `git reset --hard 2916e06…` (toplevel asserted first); re-run restored
`GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3` exit 0 (receipt
`grounding-after-revert.txt`).

## Findings and observations (status-neutral)

1. **The frozen instruments are absent at the base rev.** `git ls-tree b7803829… --
   corpus/evidence/round80/` is empty (6 entries at `0d253c9…`, the lane HEAD). The claims.md
   wording "committed bytes at the freeze commit" refers to `0d253c9…`, not the C2 base rev.
   Consequence for the mirror build only: `mkdir -p` was needed before copying the tool in.
   The counter's own reads are unaffected — it reads lane bytes at `--rev` via `git show`.
2. **S201 is at the bound.** Its 25-word quote passes (`≤25`), but any landing-time rewording
   that adds a word trips R4's bound check. Count rule is whitespace `split()`: markdown tokens
   like `**both**` count as one word.
3. **Records bind from any lesson, decisions only from `round-<n>.md`.** `records_at` scans all
   `.md` under `corpus/lessons/`, but the DECIDED regex only matches
   `corpus/lessons/round-<digits>.md` (dated lessons like `round-79-verifier-spotcheck.md` add
   neither decisions nor round-gating). A `GATE-RECORD` placed in a dated lesson would bind the
   record while leaving the row outside the audit set unless decided elsewhere. Land records in
   `corpus/lessons/round-80.md`.
4. **Grammar constraints observed:** the quote must stay on one line and must not contain `|`
   (it would break neither the RECORD regex nor the SOURCES cells, but a `|` in the row's teach
   cell would shift the cell parse — candidates avoid both).
5. Lane working tree during my run: HEAD `0d253c9…`, only untracked wave-path entries
   (`.ufo/waves/round-80/w1.ready*`, `w1/`). I wrote only `.ufo/waves/round-80/w1/R80ExecB/`
   and the scratch dir; no tracked lane file, no `/tmp` writes, no lane/fleet git mutation.

## Tooling authorization record

No tools installed or upgraded (nothing needed; the pacman pause was not touched).

## Receipts (all under `.ufo/waves/round-80/w1/R80ExecB/`)

- `grounding-before-run.txt` — BEFORE run, stdout+exit 1
- `quotes-verified.txt` — four quotes vs mirror object store (verbatim + counts)
- `mirror-git-log.txt` — `git log --format='%H %s'` head of the mirror + history count
- `grounding-after-run.txt` — AFTER run, PASS line, exit 0
- `grounding-negative-r4.txt` — R4 negative control, FAIL, exit 1
- `grounding-after-revert.txt` — post-revert PASS re-run, exit 0

## For the main agent's gate

Re-run on the lane after L1 lands the real S199–S202 rows: (1) the (a) command must still print
FAIL at the base rev; (2) at the landing commit, the same counter must print the (c) PASS line
with exit 0; (3) spot-check one `words=` cell against `git show <rev>:<path>` + whitespace
split. Scratch dir `/fast/scratch/hyaku/chousa-r80/R80ExecB` was deleted before yield.
