# CritC1Axis — C1 as an axis move (round 49 w1)

Seat: CritC1Axis (UFO-FSD critic, leaf). Attack target: the frozen R49-C1 adopter
claim — is it an operability move or plumbing? Are C1/C2 causally separable?
Run: 2026-10-25, lane repo /home/vgpnk/Projects/shokunin/chousa-shokunin.
Tooling: no install performed (none needed); operator RULES.md read; pacman untouched.

## 1. Measured state (commands run, outputs verbatim)

`python3 corpus/evidence/round49/c1-count.py` (read-only; exit 0):
```
BASE_REV=414a2ec6cde05a921dbdd9e02e7ae56b0db647ef
TOOL=present sha256=3b8a6e7daa45dca66c1d2f84cbb7903d999091a75a4b92ac2cda2c71997b06a6
BASE_CENSUS=ok
SET_A TOOL_EXIT=0 CITED=9 APPEND=9/9 HELD=0/0 BY_DOC=9/9 EXTRA=0 REWRITE=2/2 SHAPE=9/9 CONTIGUOUS=yes URL=9/9 USED_BY=9/9 NORMALIZED=9/9 COLLISIONS=match CENSUS=ok -> PASS
SET_B TOOL_EXIT=0 CITED=3 APPEND=3/3 HELD=0/0 BY_DOC=3/3 EXTRA=0 REWRITE=1/1 SHAPE=3/3 CONTIGUOUS=yes URL=3/3 USED_BY=3/3 NORMALIZED=3/3 COLLISIONS=match CENSUS=ok -> PASS
SET_C TOOL_EXIT=0 CITED=5 APPEND=3/3 HELD=2/2 BY_DOC=5/5 EXTRA=0 REWRITE=1/1 SHAPE=3/3 CONTIGUOUS=yes URL=3/3 USED_BY=3/3 NORMALIZED=3/3 COLLISIONS=match CENSUS=ok -> PASS
GUARD TOOL_EXIT=0 COLLISIONS=['S002'] -> PASS
PIPE TOOL_EXIT=0 ROWS=1 CELLS=11 RECHECK=90d STRIPPED_LOGGED=yes CENSUS=ok -> PASS
SETS_PASS=3/3
C1=PASS
```

`python3 corpus/evidence/round49/c2-count.py` (read-only; exit 1):
```
ENTRIES=0/2
BOUND=0/9 (min 7) REFUSED=0
BOUND_IDS=
REF_ID_UNBOUND=0
QUOTE_ROWS=0 ON_BOUND=0/0
SPAN_IDS=0/0 (min 2 each)
QUOTES_IN_SPAN=0/0
QUOTES_IN_ENTRY=0/0
QUOTES_IN_LESSON=0/0
QUOTE_SHORT=0/0
SPAN_CONTEXT=0/0
CAPTURE_BOUND=0/0
ANCHOR_BOUND=0/0
INFERENCE_GROUNDED=0/2
QUARANTINE_VERDICTS=0/5 (S082,S084,S086,S095,S096)
QUARANTINE_BLOCKED_ADOPTED=0
C2=FAIL
```

Git facts (`git -C <lane> …`):
- `HEAD=65940928cc9332b386bcbca92571451cc4374cbe` — log: `6594092 round-49: C1 candidate tools/assimilate-rows.py …`; parent `fe740e7 round-49: freeze claims C1 …`.
- `git ls-tree HEAD -- tools/assimilate-rows.py` → blob `8597d3d8…1789f`; `sha256sum tools/assimilate-rows.py` = `3b8a6e7…` = sha of the blob at commit 6594092 (`git show 6594092:tools/assimilate-rows.py`). The measured tool is the committed candidate.
- `git diff --stat 414a2ec..HEAD` → 11 files, +2475: tool, both counters, claims.md, controls, build-spans.py (no scorecard, no registry rows).
- BASE_REV and working-tree registry both end at S095 (`git show 414a2ec:corpus/SOURCES.md` and `corpus/SOURCES.md` id sets identical: S001..S095). Scratch adoption outputs match the counter: `.ufo/waves/round-49/assimilation/adopt/renumber.tsv` maps staged S087,S088,S089,S091,S092,S100,S101,S102,S103 → lane S096..S104, all `append`; `append.md` = 9 eleven-cell rows; rewritten entries 90/88 lines.
- `git status --porcelain` shows ` M corpus/QUALITY.md` only among tracked; SCORECARD.md unmodified; `?? corpus/lessons/round-49.md` (untracked) exists but carries no register verdict lines (C2 prints 0/5).

## 2. Is C1 an operability move? No — it is capability/plumbing.

Scorecard (SCORECARD.md:5-13, 26-30) defines operability as one narrow count: the
three named archives each `exit 1` with exactly one `RESEARCH_GATE: DRIFT` summary via
`tools/research-gate.sh verify`. Nothing in C1 touches that: the tool is not called by
research-gate.sh, the three archived inputs are untouched, and the scorecard is not
modified. The 3/10 score cannot move because of C1. The claim itself is honest about
this — `Tag: plumbing (QUALITY 64)`, capability row only if after-measurement passes
(claims.md:45-46) — but the claim title's "operability (lowest scored axis, 3/10)"
overstates the axis link. C1 measures the tool's transformation (renumber by document,
contiguous append from base max, one simultaneous substitution, 11-cell parse, 0-3-space
collision report, census-valid mirrors) on scratch mirrors built solely from
`git archive BASE_REV corpus` (c1-count.py:364-386). It is an enablement artifact, a
precondition; the lane-facing effect begins only when the adoption executes and lands
registry rows + entries — which is C2's territory (currently unlanded: ENTRIES=0/2,
BOUND=0/9). A wave stopping at C1=PASS yields zero measurable lane change (scorecard
3/10, no entries, no rows).

## 3. Separability claim verified — both directions.

- C1 never reads lane-adopted bytes: the mirror is the BASE_REV archive; its knowledge
  dir is symlinked from that archive tree (c1-count.py:148-166, 364-386), not from the
  current lane. Observed: C1=PASS while the lane has ENTRIES=0/2 — C1 passes with zero
  adoption. So C1 is satisfiable with no lane change beyond the committed tool.
- C2 never runs the tool: c2-count.py references no assimilate-rows path; its only
  subprocesses are `git show BASE_REV:corpus/SOURCES.md` and `tools/inference-ground.py`
  (c2-count.py:128, 195). C2 measures lane bytes + qcache captures + register; any
  compliant writer of those bytes satisfies it even if the tool never ran. The claims.md
  separation sentence (claims.md:13-16) is therefore accurate.
- Consequence: the two counters cannot gate each other. C1=PASS implies nothing about C2
  (C2 is FAIL now), and a future C2=PASS would not prove the tool ran. Admission must keep
  them independent; do not report C1 as progress on the adoption.

## 4. Calibration notes (non-blocking).

- Counter and tool share verbatim copies of `url_of`/`ROW_RE`/`GREP_RE` (tool-candidate.py:52-69 vs c1-count.py:67-89); a normalization bug shared by both would be invisible to the counter, but the mirror census E-checks (CENSUS=ok on every set + guard + pipe) independently validate the appended rows, and the 0-3-space/escaped-pipe legs exercise the messy cases. No defect found.
- `held` dedup by normalized URL means two staged rows for one URL collapse to one lane id and used-by is not widened — a documented limit (tool docstring lines 41-42), not a regression here (this package has none).
- Kill rule is meaningful: a do-nothing control would fail SETS_PASS=0/3 plus GUARD/PIPE (controls/c1-before.txt, controls/copy-tool.py exist at the commit); a pass is non-trivial, not a vacuous self-check.

## 5. Verdict

C1 is a passing, well-falsifiable capability/plumbing test, not an operability move: it
cannot change the 3/10 score, changes nothing in the lane today, and must be recorded as
a tool acquisition; C1/C2 separability (C1 passes with no adoption; C2 needs only lane
bytes, never the tool) is confirmed by code and live runs, so neither claim may be read
as the other's evidence, and the round-49 adoption itself is not yet admitted (C2 FAIL).

VERDICT: attacked frozen C1 as an axis move — confirmed it is plumbing/capability (no
scorecard-observable effect, zero lane-facing change), verified C1/C2 causal separability
by code inspection and live counter runs (C1=PASS with an unadopted lane, C2=FAIL with no
tool dependency), and found no fixable defect in the counter, tool, or claim wording.
