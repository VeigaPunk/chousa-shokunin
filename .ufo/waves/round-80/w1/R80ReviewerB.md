# R80ReviewerB report — Attack frozen claim C2 (calibration)

Round 80 `chousa`, frozen predicate set `corpus/evidence/round80/claims.md` (commit `0d253c95`).
The attacked instrument was the committed counter
`corpus/evidence/round80/gate-grounding-check.py`.

## Instrument bytes I cited (sha256 measured, not asserted)

| instrument | sha256 |
|---|---|
| `corpus/evidence/round80/gate-grounding-check.py` | `d9e426216665a098cd90adf8fbf5e5dd62e02dc7b5b707c322b404b3eb55c553` (matches claims.md and the freeze commit) |
| `corpus/evidence/round80/claims.md` (worktree, uncommitted) | `06086ba2a62375c917b903db84c14d6f48422011f54079bbae8bf553da3ea29a` — the freeze commit `0d253c95` carries a different (unknown) version; the `0f59b985`-committed version is byte-what-claims-cite |

Not attacked / NOT a committed instrument: a `selfcheck5.py` was seen referenced in the round-79
spot-check only as a planning artifact and never landed as a round-80 committed counter; I only
found and attacked the byte-verified `gate-grounding-check.py`.

## Scratch

Every run executed in a mirror:
`/fast/scratch/hyaku/chousa-r80/R80ReviewerB/mirror` (a `git clone --shared` of
`/home/vgpnk/Projects/shokunin/chousa-shokunin`, remote detached, no push, no lane worktree or
`/tmp` writes). Scratch deleted after the last run.

Tool installs: none (no packages installed; used only bash, git, and the preinstalled python3).

## Baselines re-run before any forgery

Fresh re-run of the committed `grounding-before` and the (committed round-80) after counter:

- `00-before-base.txt` (rev `b7803829`): `GATE_GROUNDING=FAIL unresolved=3 superseded_resolved=0
  audited=S196,S197,S198` **exit=1** (byte habits match the committed control, despite D2
  revision binding).
- `01-after-landing.txt` (rev `44d09edf`): `GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3
  audited=S199,S200,S201,S202` **exit=0**.

No change to the instrument was made anywhere; the counter's sha256 was verified per run
(header of each receipt).

## Finding 1 — C2 as-frozen does not verify (three independent ALL-PASS holes)

The frozen kill rule says the claim fails if any audited tip or superseded row resolves while a
rule R1-R4 "fails" in spirit (quote does not support `teaches`, words off, quote comes from a
wrong line). All three defects below produce the **same PASS line**:

```
GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3 audited=...
```

Note: the predicate freezes exact counts `superseded_resolved=3 audited=S199,S200,S201,S202`
over the *landing* fixture; my holes use the same fixture plus only *added* rows (or slight
mutations), so the predicate tolerates them but the same PASS is printed with new ids appended
in `audited=`.

### 1a. R3 is a substring test on a line, never a "teaches"-binding test — off-forge PASS
`20-f1a-off-by-line-quote-real.txt` (mirror head `6c3c9ee3`, exit=1 audit shows
`ROW S144 record=ok ... verdict=OK`): record for `S144` names a real 24-word fragment of the
registry's `| S140 |` row line 150 (`path=corpus/SOURCES.md line=150`) — the fragment exists
byte-for-byte at that line, but it is a fragment of a **different row's** cell and does not
state anything S144 owns. The counter happily prints `verdict=OK`. Scored against the frozen
defense's "counter prints verdict=OK ⟹ quote is on-line at-named line": TRUE, but the frozen
policy only covers "quote is present at the line", which (as the round-79 S198 case showed) is
not the guarantee the row's `teaches` needs.

`20d-f1a-full-battery-plus-forged.txt` (mirror head `da9483d6`, **exit=0**, full PASS on
`audited=S199,S200,S201,S202,S204`): fixture with the real landing records and the S204
(cross-row) record added on top. The landing predicate line itself (with added S204 id in the
audited= cell) is unchanged: the same PASS line prints with a forger admitted.

### 1b. Huge line 222 admits irrelevant 12-word slices
`21c-f6b-12word-slice.txt` (mirror head `24d6750c`, exit=1 audit shows
`ROW S199 record=ok … words=12 verdict=OK`): the S199 record is rewritten to name a 12-word
slice of the *same* 103-word `round-79-verifier-spotcheck.md` line 222 that has nothing to do
with S199's `teaches`, at words=12. The counter prints `verdict=OK` (byte-verified real quote,
byte-verified correct line, byte-verified correct word count — and no `teaches` binding).
`21-f1b-huge-line-irrelevant-slice.txt` earlier variant is the same hole on the first slice.

### 1c. Grounding can be faked from pure boilerplate
`22b-f1c-final-boilerplate-pass.txt` (mirror head `c91cd550`, **exit=0**, full PASS on
`audited=S199,S200,S201,S202`): the S199 record is replaced with a record naming the first
25 words of `round-79-verifier-spotcheck.md` line 29 (the run-of-the-mill table-prose honoring
the spot-check's own rules — `| report authored by the lane identity | git -C <fleet> log …`),
at words=25, still at rev `b7803829` and the named line. Counter prints the FULL landing
predicate — the same PASS line. So: a `words=25` boilerplate quote, real bytes, real line, real
count, zero teaching content — the exact "words matches quote but the quote is 25 words of
boilerplate" forgery class spec'd by the seat — PASSES fully.

(First attempt `23-f1c-boilerplate-as-S200-tip.txt` failed because a *second* GATE-RECORD S200
record in the same lesson override-forged the first one — see Finding 5. The single-record
version `24-f1c-fixed-single-record.txt` proved the same principle at row level.)

## Finding 2 — Supersession arithmetic: any re-filing counts as a resolution

The counter's parent map is computed by matching the `supersedes S###` prefix in the teaches
cell. The `superseded_resolved` count is incremented when `tip`'s record passes. Nothing checks
that the superseded record's defect (e.g. "quote words stated 25 but measured 27") was actually
changed by the tip's record — only that a *tip* has a valid record.

`30-s203-label-only-supersede.txt` (mirror head `7c397d68`, exit=0 PASS): the S203 fixture
re-points the SAME 20-word quote/line the parent S196 already carried and tells the audit
nothing new; `superseded_resolved=3` is unchanged: S196 resolves by S203 as if it were a
correction. **`superseded_resolved` counts a re-filing, not a repair.**

`30b-f2-chain-s196-s200-s203.txt` (mirror head `ba3d2a49`, exit=0,
`superseded_resolved=4`): a signed chain S196 → S200 → S203 where the byte content at every
hop is the same QUALITY 147 line and only the label changes. Counter resolves BOTH S196 (by
S200) and S200 (by S203) — one falsified sentence counts twice.

`30c-f2c-chain-tail-only.txt` (mirror head `a7c441d6`, exit=1 but the *record* is only
accepted at the tip S203): when the chain's own record is only on the S203 tip, rows S196,
S197, S198 are `record=none → UNRESOLVED` — the counter looks only at the tail record and
nothing prevents a *later* tip's record from becoming the entire audit (a re-filing can be
scored as a resolution). `30d-f2d-chain-decided-tail-record.txt` (mirror head `9a0dbeac`,
`SUPERSEDED S196 by S200 record=none UNRESOLVED` + `SUPERSEDED S200 by S203 record=ok
RESOLVED`): the chain can be scored as "resolved" purely by where the record lives.

`32-f2b-label-only-direct-resolve.txt` (mirror head `7c6a51e2`, exit=1,
`SUPERSEDED S196 by S203 record=ok verdict=RESOLVED` inside an otherwise-FAIL output): the
label-only re-point is accepted as a direct resolution of the parent's defect.

## Finding 3 — `decided` window silently drops decided-but-recordless tips

`41-f3-window-old-lesson-s206.txt` (mirror head `e662ad16`): a tip (S206) that carries a
GATE-RECORD in the round-80 lesson is audited (tested by the same fixture with the record in
round-80; PASS). A tip whose *only* `- Admit S206` bullet sits in a committed lesson **older
than `--since-round`** (round-78 in the fixture,
`41-f3b-old-lesson-admit-silent.txt`, mirror head `00e9181f`) is never audited and prints no
row at all: the counter's default run above shows `TIPS=193 AUDITED=4
[S199,S200,S201,S202]` with NO mention of S207, printing `PASS`, while the same tip is
`ROW S207 record=none UNRESOLVED` as soon as `--since-round` is lowered to 78
(`41b-f3b-since-78-s207-surfaces.txt`, mirror 41b grep: `ROW S207 ... UNRESOLVED`, and top
line `SINCE_ROUND=78 … AUDITED=8`). Therefore a default-run PASS hides a decided tip's
missing GATE-RECORD whenever the deciding lesson predates `--since-round` (default 79).

## Finding 4 — R4 is enforced at exactly >25, not at >=25; count-mismatch is line-bound

- `53-f4-26-at-bound.txt` (mirror `f9eaf5f0`, exit=1,
  `R4 quote is 26 words (contract bound is 25)`): bound fires only above 25 (26 fails);
  a 25-word quote at `words=25` still PASSES anywhere (see 1c).
- `52-f4-count-mismatch.txt` and `54-f4c-s196-defect-class.txt`: quote=25 words with
  `words=24` (the round-79 S196 defect class) — caught and printed as `R4 quote is 25 words,
  record says 24`. So a 25-word quote declared as 25 (and a 27-word quote measured as 27)
  both pass through the R4 grammar; only the *declared* count matters.
- The 25/26 boundary in the record row is correct; the 24-vs-25 defect type Feeding
  `superseded_resolved` is down to Finding 2's arithmetic — consequences

## Finding 5 — the audit's last-record-wins dict lets one record hide another

`records_at` walks lessons in `git ls-tree` order and overwrites `out[id]` per id, so the
LAST GATE-RECORD line for an id wins.

- `60-f5-last-wins-hides-defect.txt` (mirror `03928d63`, exit=0): a fixture with a *defective*
  S200 record (quote absent from `corpus/QUALITY.md:1058`) committed in
  `corpus/lessons/round-79.md` (earlier in the tree) alongside the GOOD S200 record in
  `round-80.md`: the audit prints `ROW S200 record=ok qc=20 … verdict=OK` and the
  defective record is invisible (the defective one is shadowed).
- `60b-f5b-sort-order-escape.txt` (mirror `c5d0527d`, exit=1): when the defective record is
  moved into a lesson sorting after `round-80.md` the same defect surfaces. So the SAME
  bytes audit to different verdicts depending only on which lesson's tree path sorts last.

## Residual risks (not falsified, recorded as limits)

- `corpus/evidence/round80/claims.md` in the freeze commit `0d253c95` itself was described by
  `corpus/lessons/round-80.md` as "the 20-word quote", while the round-79 lesson quoted the
  same criterion as a "25-word"/27-word quote (the worktree `claims.md` I read says
  "corrected 15-word located quote": the number churned between the freezing and the
  landing — no single frozen source of that word count). Not falsified by seed counts
  because the instrument committed at the freeze digest matches the landing digest I re-ran;
  only the prose numbers drift.
- `superseded_resolved=3` frozen predicate makes one re-looked-up `SUPERSEDED … by S203
  resolution possible on any single re-filed row; the end-state PASS prints can't tell
  re-filing from repairing (Finding 2).

## Deviations I hid none of; all 40+ receipts are preserved

Every receipt in `.ufo/waves/round-80/w1/R80ReviewerB/` is the printed stdout+exit of the
byte-verified counter run described in the header line; receipt paths are cited with their
runs above. No receipts were mutated after the run; `41b`, `53-`, `54-`, `60b-`, `70-`, `82b-`
survive as the falsifying PASS/FAIL pairs.

## Bottom line

Claim C2's frozen predicate — the exact PASS line
`GATE_GROUNDING=PASS unresolved=0 superseded_resolved=3 [audited=…]` — is reachable with
boilerplate/orphan-line/off-row quotes, label-only re-filings, old-round-decided hidden tips
and shadow-defective records. The counter's R1-R4 are sound as *byte* checks but do not
measure what the round-80 lesson and QUALITY 152-154 claim they measure (a "located quote
that supports the row's teaches"). Calibration did not close.
