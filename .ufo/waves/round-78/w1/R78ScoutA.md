# R78ScoutA — reconnaissance over the lane's self-descriptions (round 78, wave 1)

Seat: scout, leaf, read-only. Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`
at `HEAD = 01b444b7f8d90785515e77c7ba9db5d63361329b` (freeze commit), frozen predicate set
`corpus/evidence/round78/claims.md` (base `53dbd512`, controls `93e0432e`).

**The lane worktree moved under this seat.** `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`,
`corpus/SOURCES.md` are modified and `corpus/lessons/round-78.md` is new — sibling seats
(`R78ReviewB`, `R78L1`) are landing round-78 surfaces while this reconnaissance ran. Every
finding below is pinned to a digest; the two snapshots are:

| snapshot | `corpus/QUALITY.md` sha256 | lines | criteria |
|---|---|---|---|
| HEAD `01b444b7` (frozen) | `f09b37a46ac371bed712f85ab66ac4a84590f07e4e25b44e5d717c81213de449` | 1052 | 1–145 |
| worktree, mid-wave | `a6769c43c2583c0b6a5ede1823fcc826ffe46e236b7868d69d2d12e087aeeca9` | 1056 | 1–147 |

Axes: **A1** does any *live* surface still present `matrix-battery-v4.py` as the current outer
battery; **A2** what the three `CHECK` lines say and whether they are stable; **A3** how far the
"backticked token resolves as a committed-path suffix" rule actually reaches across all criteria.

---

## (a) Every committed artifact mentioning `matrix-battery-v4.py`, classified

Universe: `git grep -l matrix-battery-v4 HEAD` (raw list in `R78ScoutA/v4-reference-census.txt`,
classification in `R78ScoutA/a-v4-classification.txt`). 19 committed non-`.ufo` files, 15 files
under `.ufo/waves/round-77/`, 1 under `.ufo/waves/round-76/`.

| artifact (HEAD) | what it says | class |
|---|---|---|
| `SKILL.md:168` | gate-registry row `round77 order-and-content battery`, command `matrix-battery-v4.py` | **historical** — append-only registry row, dated by its own label, malformed (7 cells / 8) and corrected by `SKILL.md:171`; successor row `SKILL.md:169` registers `round78 order-and-content battery v5` **and** `forge-battery.py` |
| `SCORECARD.md:3449` | round-77 C1 plan, v4 command | **historical** — inside `## Planned — round 77` (line 3442) |
| `SCORECARD.md:3475` | v4 digest `155fafb1…f106a3d` | **historical** — inside `## Round 77 verdict` (line 3471) |
| `SCORECARD.md:3480` | round-77 C1 verdict row, v4 command | **historical** — same section |
| `LOG.md:2199` | v4 permutation behaviour | **historical** — inside `## Round 77 — …` (line 2186), append-only log |
| `corpus/QUALITY.md:1042` (**criterion 141**) | *"Check: `python3 -B corpus/evidence/round77/matrix-battery-v4.py --matrix corpus/evidence/round76/loader-matrix-v3.py --work DIR` prints exactly `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`"* | **STALE PRESENT-TENSE CLAIM** — live criterion with no superseder, naming the superseded instrument as the current check and never pointing at v5 |
| `corpus/QUALITY.md:1044` (**142**) | v4's work-directory defect narrative | **historical** — explicitly superseded (`supersedes: 142` in criterion 144, line 1050) |
| `corpus/QUALITY.md:1050` (**144**) | v4 as the *before* state (`WORK_CONTRACT=FAIL …`) | **historical by design** — before-state of a successor criterion |
| `corpus/QUALITY.md:1052` (**145**) | `R77CriticA/…` receipts as "shown able to fail" | **historical evidence inside a live criterion** — its own check command is v5 |
| `corpus/evidence/round77/*` (10 files) | round-77 instruments, receipts, controls | **historical** |
| `corpus/evidence/round78/{claims.md,controls/forge-battery-before-v4.txt,controls/work-contract-before-v4.txt,forge-battery.py}` | v4 as the named *before* subject of C1 | **historical/before-state (correct)** |
| `corpus/lessons/round-77.md`, `corpus/lessons/round-77-verifier-spotcheck.md` | round-77 lessons | **historical** |
| `.ufo/waves/round-77/` (15 files) | dispatch, spec, seat reports, receipts | **historical** |
| `.ufo/waves/round-76/w1/R76Connect.md` | round-76 wave artifact | **historical** |
| `corpus/README.md` | — | no hit; the README names no outer battery at all |

**Answer to (a): exactly one committed artifact presents v4 as the lane's current outer battery —
`corpus/QUALITY.md` criterion 141.** Everything else is dated historical evidence.

Two supporting facts about 141's staleness: v4 stays committed and its own committed receipt records
`BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` and `# exit: 0`
(`corpus/evidence/round77/controls/after-battery-v4.txt`), so the sentence is still *true*; it is
stale because it names the superseded instrument. v5 keeps the same surface (`--no-permute`,
`--no-content`, `--print-order`, the same `BATTERY=` line) and adds a `RECEIPT_LINES` trailer before
it (`corpus/evidence/round78/matrix-battery-v5.py:264-271,328-330`), so v5 still emits 141's line —
but 141's "prints exactly" phrasing would need re-reading against v5's extra trailer. [INFERENCE:
read from source, not measured by this seat.]

**Secondary (calibration, adjacent to (a)):** criterion 143 has **no superseder** — 145 restates the
answer-key requirement against v5 but carries no `supersedes: 143`
(`R78ScoutA/probe-143-supersession.txt`, `grep` exit 1). The lane therefore carries two live
criteria for the same requirement, one of which cites only round-77 receipts.

---

## (b) `selfcheck.py` — the three `CHECK` lines, verbatim

### Run 1 — start of this seat, on the frozen bytes

Command: `python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round78/selfcheck.py --lane /home/vgpnk/Projects/shokunin/chousa-shokunin --verbose`

```
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin REV=worktree
CHECK S1-skill-registry ok rows_malformed=[168] corrected=[132, 168] unresolved=[]
CHECK S2-quality-pointers ok criteria=[144, 145] missing=[] superseders={142: [144]} unresolved=[]
CHECK S3-lesson-mistakes ok mistakes_width=4 stranded=[73] errata=[73] unresolved=[]
SELFCHECK=PASS unresolved=0/3
# exit: 0
```

Run 1's tree is not digest-pinned (it predates the digest capture); its output is byte-identical to
the run against the committed HEAD bytes (`f09b37a4…`, 1052 lines), so the frozen state is the
reference. The same three lines are reproduced deterministically from committed bytes at the controls
commit and at HEAD (`--rev 93e0432e…` and `--rev 01b444b7…`, both exit 0 —
`R78ScoutA/selfcheck-at-controls-93e0432e.txt`, `R78ScoutA/selfcheck-at-rev-HEAD-01b444b7.txt`).

### Run 2 — mid-wave, same command, worktree has moved

`R78ScoutA/selfcheck-worktree-midwave.txt` (QUALITY sha `a6769c43…`, 1056 lines):

```
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin REV=worktree
CHECK S1-skill-registry ok rows_malformed=[168] corrected=[132, 168] unresolved=[]
CHECK S2-quality-pointers FAIL criteria=[144, 145, 146, 147] missing=[146, 147] superseders={142: [144, 146]} unresolved=['146:R78ReviewB/ALL-three-hollow.txt,R78ReviewB/atkB2-new-block-window.txt,R78ReviewB/ctrlA-defect-no-correction.txt', '147:R78L1/a8-normalizer-v5.txt,R78L1/a8-normalizer-v4.txt']
CHECK S3-lesson-mistakes ok mistakes_width=4 stranded=[73] errata=[73] unresolved=[]
SELFCHECK=FAIL unresolved=1/3
# exit: 1
```

Cause, established read-only: sibling seats appended criteria **146** (line 1054) and **147**
(line 1056) *inside the newest* `## Round-78 addition` block (line 1048), and both cite receipts
that exist on disk but are **not committed** —
`.ufo/waves/round-78/w1/R78ReviewB/{ALL-three-hollow,atkB2-new-block-window,ctrlA-defect-no-correction}.txt`
and `.ufo/waves/round-78/w1/R78L1/a8-normalizer-v{4,5}.txt` (directory listing verified). The
counter's resolution universe is `git ls-files`, so uncommitted receipts cannot resolve.

Consequences, stated without repairing anything:
- C2's frozen predicate is still satisfied **at its frozen revision** (controls `93e0432e`, HEAD).
- The lane's **worktree** C2 is red right now (`SELFCHECK=FAIL unresolved=1/3`, exit 1) and stays red
  until those two criteria's receipts are committed. A seat that scores C2 on the worktree today
  scores a red counter.
- The failure is the mechanism criterion 146 itself names: the audited window is "the newest block",
  so any append to that block changes the predicate's outcome. This is a post-freeze observation,
  reported as a limit — the instrument is not edited.

---

## (c) Wider pointer sweep of `corpus/QUALITY.md` (all criteria, not just the newest block)

Probe: `R78ScoutA/sweep_final.py` (copy of the script, run with `python3 -B`; exit 0 both runs).
It re-uses the frozen instrument's token filter (`^(\d{3})` widened to `^(\d{1,3})\.\s`, same
`NOT_A_PATH` prefixes, same "no space / must contain `/`" rule) and its suffix match, then sweeps
**every** criterion.

| snapshot | criteria | Rule A = instrument-exact (`token.lstrip("./")`) | Rule B = only a literal `./` stripped | content-level after classification |
|---|---|---|---|---|
| HEAD `01b444b7` | 145 | **83 criteria** with a non-resolving token | 71 | **1** |
| worktree `a6769c43` | 147 | 85 | 73 | 3 |

Receipts: `R78ScoutA/quality-sweep-at-HEAD.txt`, `R78ScoutA/quality-sweep-worktree.txt`.

### The list, with criterion ids

**Rule A (the lane's own frozen rule applied to the whole file) — 83 ids:**
5, 6, 13, 14, 18, 21, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 46,
48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 63, 64, 65, 66, 67, 68, 69, 71, 73, 74, 80, 81, 82, 83,
85, 86, 87, 88, 89, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 106, 107, 115, 116,
120, 121, 124, 125, 126, 129, 131, 132, 135, 137, 138, 142.

**After removing the instrument's own `lstrip("./")` defect (Rule B) — 71 ids:** the same list minus
28, 40, 41, 49, 50, 52, 53, 54, 55, 57, 63, 138 (12 criteria whose only gap is a hidden `.ufo/…` path).

**After classifying each token (Rule B set) — the only genuinely broken committed-path pointer is
criterion 142, `receipts/02c-work-unwritable.*`** (the routed defect 3 that criterion 144 supersedes).
Token-class census over the Rule B set (the largest class, 62 output snippets, is not a path at all):

| class | tokens | criteria |
|---|---|---|
| output snippet, e.g. `LEGS=5/5`, `TAGGED=k/n` — not a path | 62 | 18, 27, 29, 31, 36, 46, 48, 64, 65, 67, 68, 69, 73, 74, 80, 81, 82, 85, 87, 88, 91, 92, 95, 96, 101, 102, 106, 107, 115, 120, 121, 124, 125, 126, 137 |
| `path:line` / `path:a-b` anchor whose base file **is** committed | 28 | 13, 14, 26, 30, 36, 37, 38, 39, 42, 71, 81, 91, 93, 97, 98, 100, 132, 135 |
| directory token (`dir/`, or a directory path) that exists with committed files | 19 | 5, 6, 21, 24, 29, 31, 32, 36, 39, 42, 51, 66, 67, 73, 94, 102, 103 |
| placeholder / fragment / brace shorthand (`<dir>`, `<lane>`, `<round>`, `…`, `.ufo/...`, `</head>`, `<w:tab/>`, `…{1,2}.json`) | 12 | 14, 25, 34, 35, 36, 42, 83, 86, 88, 94, 99 |
| numeric ratio (`4/8`, `3/10`) — not a path | 6 | 56, 85, 88 |
| intentional negative citation (the criterion quotes an absent path as the defect) | 3 | 116 (`corpus/evidence/round59/claims.md`), 129 (`knowledge/*.md`, `knowledge/*.md;corpus/lessons/*.md`) |
| source-id shorthand `S1549/S1559/S1569` | 1 | 131 |
| archive-internal `word/document.xml` | 1 | 89 |
| runtime work tree `real/*.doc` (counter-created, never committed) | 1 | 98 |
| **GENUINE-UNRESOLVED** | **1** | **142** |

Brace shorthand `…{1,2}.json` (criteria 34, 36, 42) expands to files that **are** committed
(`b-s32471021.json`, `b-s32471022.json`, …) — the literal token cannot resolve, the citations do.

**Hidden-path defect, quantified:** 33 criteria at HEAD carry at least one `.ufo/…` token (41 tokens);
**none** of them can ever resolve because `resolves()` does `token.lstrip("./")`, which turns
`.ufo/...` into `ufo/...`. Proof, importing the frozen instrument's own function
(`R78ScoutA/probe-hidden-path-lstrip.txt`, exit 0):

```
token: .ufo/waves/round-30/build/ExecRerunCount.md
  committed exactly : True
  resolves()        : False
  after lstrip('./'): 'ufo/waves/round-30/build/ExecRerunCount.md'
  literal-'./'-strip: .ufo/waves/round-30/build/ExecRerunCount.md -> True
```

The newest-block restriction hides this today (144/145 cite no `.ufo` path); a widened sweep without
the fix false-fails 12 criteria outright.

### Direct answer to (c)

- Under the lane's frozen rule applied to the whole file: **83 criteria** (list above).
- Of those, **one** is a real broken pointer: **142** (`receipts/02c-work-unwritable.*`), already
  superseded by 144. **None** of criteria 1–143 has an unreachable *content* citation apart from it.
- The other 82 are artifacts of the lexical rule (hidden paths, `:line` anchors, directories, brace
  shorthand) or tokens that are not paths (output snippets, ratios, placeholders, intentional
  negative examples). Widening S2 to the whole file **without** a token classifier would turn a
  green self-assessment red for reasons that are not defects.
- On the moving worktree the content-level set grows to {142, 146, 147}; 146/147 are post-freeze
  additions whose receipts exist but are uncommitted (see (b)).

---

## Instrument defects observed (fail-closed; nothing edited)

1. **`resolves()` destroys hidden paths.** `token.lstrip("./")` strips *all* leading dots and
   slashes, so `.ufo/...` → `ufo/...`. Verified by importing the instrument (`probe-hidden-path-lstrip.txt`).
   Severity today: latent (newest block has no `.ufo` token); severity if widened: 12 false failures.
2. **`SUPERSEDES` matches quoted prose.** Criterion 146 quotes the attack input `supersedes: 142` in
   its body; the counter registers `superseders={142: [144, 146]}` — a *quotation* becomes a
   supersession edge (`R78ScoutA/probe-supersedes-quotation.txt`). The escape hatches are lexical set
   membership with no content check, which is exactly criterion 146's own subject.
3. **The audited window is "the newest `## Round-<n> addition` block"** (last match wins), so an
   append to that block silently removes every earlier criterion from pointer auditing — demonstrated
   live by (b): the same frozen instrument that prints `SELFCHECK=PASS` at HEAD prints
   `SELFCHECK=FAIL` on the worktree once 146 and 147 land in the round-78 block.
4. **The token filter cannot see path shapes**: `:line` anchors, directories, brace shorthand, and it
   *does* see output snippets (`LEGS=5/5`). Any successor criterion that widens the audit window must
   first classify tokens, or it will report 82 false gaps on today's file.

## Unknowns / limits of this seat

- The worktree is moving; both snapshots are digest-pinned and may not match the tree at integration
  time. HEAD (`01b444b7`) is the stable reference.
- `selfcheck --rev` reads Git; a worktree run resolves against `git ls-files` (the index), not HEAD —
  an uncommitted `QUALITY.md` is therefore audited against the committed path universe, which is why
  146/147 fail rather than resolve.
- I did not re-run `matrix-battery-v4.py` or `matrix-battery-v5.py`; v4's PASS is cited from its
  committed round-77 receipt, v5's interface from its source lines.
- `.ufo/waves/round-77/` was read through `git grep` only; no round-77 artifact was opened beyond the
  hits listed, and no sibling report was used as evidence.

## Housekeeping

- Tool installs/upgrades: **none** (no pacman transaction; the host guard's pause was never needed).
- Scratch `/fast/scratch/hyaku/chousa-r78/R78ScoutA/` removed before yield; the probe scripts and
  every receipt were copied into `R78ScoutA/` first.
- Wrote only `.ufo/waves/round-78/w1/R78ScoutA/` and this file. No lane, fleet, git or jj mutation.
