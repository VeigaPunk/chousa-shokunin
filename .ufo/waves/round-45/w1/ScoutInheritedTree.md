# ScoutInheritedTree — round 45 wave 1

Item: confirm the three working-tree modified paths are exactly the round-44 disposition's left-named rows; check `.ufo/l0-questions.md` for operator answers to the chousa round-43 inherited-tree question, the chousa round-44 round-shape question, and 8d77e6c1 (fetch scope). Leaf seat: no dispatch, no writes outside this report.

## 1. Commands run (verbatim)

### `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain`
```
 M .ufo/waves/round-40/w1/swarm-registry.json
 M .ufo/waves/round-41/w1/swarm-registry.json
 M corpus/evidence/round41/receipts/cells/cells.json
?? .ufo/waves/round-45/gen-w1-spec.py
?? .ufo/waves/round-45/w1-dispatch.json
?? .ufo/waves/round-45/w1-run.err
?? .ufo/waves/round-45/w1-spec.json
?? .ufo/waves/round-45/w1-task-result.json
?? .ufo/waves/round-45/w1/
```

### `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --stat`
```
 .ufo/waves/round-40/w1/swarm-registry.json        |  70 +--
 .ufo/waves/round-41/w1/swarm-registry.json        | 641 ++++++++++++++--------
 corpus/evidence/round41/receipts/cells/cells.json | 185 +++++--
 3 files changed, 612 insertions(+), 284 deletions(-)
```

### Round-44 disposition left-named rows — `corpus/evidence/round44/disposition.tsv` lines 37–39
```
37:.ufo/waves/round-40/w1/swarm-registry.json	left-named	-	left-named; not hunk-verified; numstat 36 insertions, 34 deletions; committing the diff would be a sweep
38:.ufo/waves/round-41/w1/swarm-registry.json	left-named	-	left-named; not hunk-verified; numstat 427 insertions, 214 deletions; committing the diff would be a sweep
39:corpus/evidence/round41/receipts/cells/cells.json	left-named	-	left-named; not hunk-verified; numstat 149 insertions, 36 deletions; committing the diff would be a sweep
```

### l0-questions.md targeted reads
- `:144:raw`: `chousa | round-43 | Inherited working-tree debt, operator decision: PROVINCE.md's mode bit was restored to 644 (content unchanged). Left untouched, not this round's work: modified `.ufo/waves/round-40/w1/swarm-registry.json`, `.ufo/waves/round-41/w1/swarm-registry.json`, `corpus/evidence/round41/receipts/cells/cells.json`, and the untracked r40/r41 seat reports. Commit them as historical wave evidence, or leave them? Chousa will not sweep them.` — NO answer appended.
- `:148:raw`: `chousa | round-44 | Round shape and seat accounting after a mass seat failure — operator ruling wanted. Round 44 ran three v1 waves, 64 (wave 1) + 32 (wave 2) + 32 (wave 3) = 128 seats ... Two rulings wanted: (a) is a recovery wave after a mass seat failure admissible ... (b) should the launcher timeout be sized per wave and recorded in the receipt ... Chousa does not block on this answer and has landed the round.` — NO answer appended.
- 8d77e6c1 fetch scope: `:136` (round-41) asks "may a wave dispatch item ever constitute egress approval on its own text? ... r41's wave contract now bans egress outright — confirm this is the correct standing interpretation." `:140` (round-42): "Fetch-scope ruling still open (8d77e6c1): round 42 made NO external fetch ..." — NO answer appended anywhere (grep for `8d77e6c1` hits only lines 136 and 140; grep for `L0 ANSWER.*chousa|chousa.*ANSWER|ANSWER.*round-43|ANSWER.*round-44` returns no matches).

## 2. Verdict

1. **Modified paths == disposition left-named rows: CONFIRMED.** The three `M` paths in porcelain exactly equal disposition.tsv lines 37–39 (all three `left-named`). Diff --stat shows exactly those three files (3 files changed, 612 insertions, 284 deletions). No other tracked modifications exist. The disposition's own numstat per file (36/34, 427/214, 149/36) differs from today's cumulative diff --stat (70, 641, 185) because the tree changed since round-44 freeze (rows were not hunk-verified; round-45 work has not touched these files — remaining deltas are cumulative r44→now diffs, not a mismatch of identity).
2. **No operator answer exists** for any of the three questions:
   - chousa round-43 inherited-tree question (line 144): open, no `L0 ANSWER` appended.
   - chousa round-44 round-shape question (line 148): open, no `L0 ANSWER` appended.
   - 8d77e6c1 fetch-scope ruling: explicitly recorded as still open at line 140; no answer anywhere in the file.

## 3. Implications / resolvable pointers

- The three modified files remain the round-44 disposition's left-named debt, untouched by round-45; the untracked r40/r41 seat reports referenced in line 144 are no longer present in porcelain (only round-45 untracked artifacts remain: `.ufo/waves/round-45/{gen-w1-spec.py,w1-dispatch.json,w1-run.err,w1-spec.json,w1-task-result.json,w1/}`).
- Fetch-scope L0 `8d77e6c1` is still open: seat contract's "no network egress" standing interpretation stands (round-42 practice).
- Pointers: disposition.tsv lines 37–39 (`corpus/evidence/round44/disposition.tsv:37-39`); l0-questions.md lines 136, 140, 144, 148 (file `.ufo/l0-questions.md#7DB8`, sha256-pinned read header).
