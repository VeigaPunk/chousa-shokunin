# RevGatesRows — round-46 wave-2 (falsify): the five new `## Gates` rows

Seat `L1Chousa46.RevGatesRows` (reviewer, leaf). Item: structural conformance of the five
round-46 Gates rows with the table header (8 cells, 9 separators, one line) and the frozen row
rule; verify pinned `sha256` prefixes; report stale digests. Object:
`d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a`. The lane moved during the seat (`d09fc8e` →
`3807537` → `e50b388`, HEAD at exit). All byte claims use `git show <commit>:path`; landing-byte
runs use `git archive d09fc8e | tar -x` in `/tmp/chousa-r46w2-RevGatesRows/` (removed). No
network, no installs, pacman untouched; nothing in the lane written but this file.

Header = line 77: `| name | kind | entry | verdict map | self-test | pinned values | write scope
| owner |` → 9 pipes, 8 cells; delimiter row = line 78 only. Frozen row rule
(`corpus/evidence/round46/c2-count.py:17-19,96`): inside `## Gates` (to the next `## `),
fence-aware, `line.startswith("|") and bare.count("|") >= 8 and "exit" in bare`.
## Per-row structural result (d09fc8e; same structure at e50b388)
Separators = unescaped `|`; `\|` inside a code span is GFM-legal and does not split a cell.

| line | char off | row | cells | sep | raw pipes | 1 line | `exit` | in table? |
|---|---|---|---|---|---|---|---|---|
| 113 | 41991 | `round24–27 counting instruments` (r46 registration) | 8 | 9 | 15 | yes | yes | **NO** (F1) |
| 114 | 43752 | `round33–34 census instruments` (r46 registration) | 8 | 9 | 9 | yes | yes | **NO** (F1) |
| 115 | 45014 | `qr-harness` (r30; r46 registration) | 8 | 9 | 9 | yes | yes | **NO** (F1) |
| 116 | 45902 | `inference-ground` (r46) | 8 | 9 | 9 | yes | yes | **NO** (F1) |
| 117 | 47020 | `chousa round-46 counters` | 8 | 9 | 9 | yes | yes | **NO** (F1) |

Row 113's 6 extra raw pipes are escaped: 4 in the entry code span
(`round26-measure.sh TREE [c1\|c2\|c3\|holds\|all]`, offsets 354/358/362/369) and 2 in the
verdict cell (`round-26 c1\|c2\|c3`, offsets 942/946); lines 77–117 hold no other `\|`.
All five sit inside `## Gates` (75…507) for the counter's scanner; kind and owner cells present.
Pinned digests (17, `git show d09fc8e:<path> | sha256sum`): 113 10/10 match; 114 3/3; 115 1/1;
116 1/1 at landing but stale at HEAD (F3); 117 2 pins, **both stale** (F2).
## Findings
### F1 — HIGH — the five rows are not inside the Gates table
Line 112 is empty. At base `6e2630a` the last row was line 111 (`tag-count`), 112 the blank
closing the table, 113 the `**Historical — Round-25 …**` paragraph. `d09fc8e` inserted rows
113–117 into that gap; the only header/delimiter pair (77/78) is 35 lines above. GFM ends a
table body at the first empty line, and `|…|` lines without header+delimiter are a paragraph —
all five rows render as text, and line 118 abuts row 117 with no blank. The counter cannot see
it: `GATES_ROWS=35` at both commits, since `gates_rows()` only counts `|`/`exit` lines between
headings. Verification gap: no GFM renderer on the host (`markdown_it`/`markdown`/`mistune`
absent; `/usr/bin/cmark` 0.31.2 is CommonMark and rendered even the headed block as `<p>`, as
did `md2html` 0.6.0) — the render outcome is the GFM rule; the byte structure is observed.
### F2 — HIGH — the counters row's two pinned digests are stale
Row 117 pinned cell, verbatim: ``sha256 c1 `96833e22b0eb…`, build-spans `d41b1e5a090d…` ``.
Actual at landing: `c1-count.py` = `819287e2075c3f5b57c4ceb26fb6b3d7594af48e03ad7cfcd61690727c9e0a65`;
`build-spans.py` = `b5c4d83bc9a326395434e582e140b0afb5f3aa4f70a880838582bca708a0edc0`. The lane's
landing record agrees: `measure-after.txt:3` (at d09fc8e) reads `c1 819287e2075c3f5b …
build-spans b5c4d83bc9a32639`. Both pins are pre-final revisions: `w1/ExecCounterRun.md:76`
dates `96833e22b0eb3617` to 07:27:37 (superseded 07:31:17 by `819287e2`);
`w1/ReviewerC3Spans.md:10` dates `d41b1e5a` to the quote-only span builder, superseded by
`b5c4d83b` (`CONTEXT = 80`). At HEAD `e50b388` the cell is unchanged while the files are
`8473abf6c4437bed…` and `b5c4d83bc9a32639…`: two correction commits later the row still names
bytes that were never the tree's.
### F3 — HIGH at HEAD — the tool pin no longer names the file under test
Row 116: ``sha256 `819f83ebdc6c…` at the round-46 landing`` — exact for `d09fc8e`
(`819f83ebdc6c6b47d83216f5403824c152ba1f12f09c88b16e2e1184275326bc`). At HEAD `e50b388` the
tool is `7736688bdefe9df0…` (via `3018b1d2…` at `3807537`), while `e50b388:measure-after.txt:3`
still records `tool 3018b1d25d762054`. The pin chain 819f83eb → 3018b1d2 → 7736688b breaks at
the first correction; neither correction re-pinned the row.
### F4 — MEDIUM — at HEAD the tool's entry cell over-states `--registry`
`git diff d09fc8e HEAD -- SKILL.md` is exactly that one line: `[--registry corpus/SOURCES.md]`
→ `--registry corpus/SOURCES.md`. The tool declares `ap.add_argument("--registry", default=None)`
(d09fc8e:217) and passes without it: `python3 tools/inference-ground.py --entry
corpus/fixtures/inference-ground-r46/positive-a.md --spans <fixture>/spans.tsv --counts
<fixture>/counts.json --root <fixture>` → `GROUND entry=positive-a.md section=1 bullets=1
tokens=1 grounded=1` / `GROUND: PASS`, rc=0. The landing brackets were correct; these bytes are not.
### F5 — MEDIUM — row 113's verdict-map cell is false for 7 of its 10 commands
Cell: "counts, never verdicts: each prints its own tallies and exits 0 on a readable tree,
exit 1 on a harness failure and exit 2 on usage, as each script's own header states".
`round27-regressions.py:5` — "Exit0 means every declared expectation matched; exit1 mismatch;
exit2 setup."; tail `raise SystemExit(int(summary['mismatches'] != 0))` → 0/1 only, and 1 is a
mismatch **verdict**, not a harness failure; `round27-falsify-controls.py:5` identical. Both
contradict "counts, never verdicts" and the exit-2 clause. No exit-2 path: `grep -c "exit 2"` =
0 in `round24-measure.sh` (header states no exit codes), `round25-ledger-recount.py` (`:30
sys.exit("expected 71 ledger rows, parsed %d")` → 1), `round25-meta-differential.sh` (`:46
sys.exit(0 if total > 0 and agree == total else 1)`), `round27-mechanisms.py` (`:5 "This probe
exits0 on successful counting"`). `round25-measure.sh:9` states only "Exit 0 means the
measurements completed, not claim admission". The uniform 0/1/2 convention is unimplemented for
7 of 10 and 2 of 10 are gates. This row's 10 pinned digests are nevertheless all correct.
### F6 — LOW — the frozen row rule cannot see cell count
`c2-count.py:96` tests `bare.count("|") >= 8`, counting escaped pipes and never counting cells.
Landing archive: row 117 + `| extra` (10 raw pipes, 9 cells) → `GATES_ROWS=35
REGISTERED=72/72 UNREGISTERED=0 C2=PASS` rc 0; a 3-cell row carrying the four round-46 paths
padded with `\|` to 8 raw pipes → `REGISTERED=72/72 C2=PASS` rc 0. A row that renders with 3 or
9 cells satisfies C2's "named in a `## Gates` row". Narrower than the frozen limit "Row truth
is not measured": cell count is not measured either, in both directions.
### F7 — LOW — `d2-census` needs a git worktree; row 114 does not say so
In an extracted archive: `python3 corpus/evidence/round33/d2-census.py` →
`subprocess.CalledProcessError: Command '['git', '-C', '.', 'ls-files', '-z',
'.ufo/waves/round-32']' returned non-zero exit status 128` (uncaught, rc 1, not a usage exit);
`--lane <dir>` behaves the same on a non-repo dir. The row advertises `[--lane DIR]` with no
such precondition. In-lane behaviour not re-run by this seat.
## Runs (landing archive unless noted; decisive lines verbatim)
```
$ python3 corpus/evidence/round46/c1-count.py          TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS  rc=0
$ python3 corpus/evidence/round46/c2-count.py --list   ENTRY_POINTS=72 (tools=8 counters=50 named=70)
                                                       GATES_ROWS=35 REGISTERED=72/72 UNREGISTERED=0 C2=PASS rc=0
$ sed -i '113,117d' SKILL.md && c2-count.py --list     GATES_ROWS=30 REGISTERED=55/72 UNREGISTERED=17 C2=FAIL rc=1
$ python3 corpus/evidence/round46/c3-count.py          ENTRIES=2/2 … CAPTURE_BOUND=11/11 REF_BOUND=2/2 C3=PASS rc=0
$ …/c3-count.py --lane-only                            … CAPTURE_BOUND=skipped C3=PASS                     rc=0
$ python3 corpus/evidence/round46/build-spans.py --check  SPANS_ROWS=11 STALE=0                           rc=0
$ c1-count.py --root /tmp/empty                        C1=FAIL no-fixtures                              rc=2
$ c2-count.py --root /tmp/empty                        C2=FAIL no-entry-points                          rc=2
tool over corpus/fixtures/inference-ground-r46/ (+ its own spans.tsv/counts.json, --root <fixture>):
  positive-a/b/c rc=0 GROUND: PASS · junk-uncited/junk-ungrounded/junk-borrowed rc=1 GROUND: FAIL
tool --entry /tmp/nope.md → inference-ground: no entry /tmp/nope.md rc=2 · missing --spans/--counts → rc=1
qr_harness.py bare → rc=2 (colophon first line) · missing map → rc=1 FileNotFoundError
HEAD e50b388: c1 C1=PASS (adds CANARY=pass); c2 GATES_ROWS=35 REGISTERED=73/73 C2=PASS; c3 C3=PASS
```
Rows 114/115 self-test cells otherwise not re-derived (no-name-signals, d2-census `21`,
self-audit live-tree `1`): wave-1 measurements, out of this seat's scope.
## Verdict
On the literal checklist all five **pass** (8 cells, 9 unescaped separators, one line, `exit`
present, inside `## Gates` for the frozen rule). Table membership: all five **fail** (F1).
Pinned digests: 15/17 correct at landing; row 117 stale (F2), row 116 stale at HEAD (F3).
Row content: row 113's verdict map false for 7/10 (F5); row 116's entry cell wrong at HEAD (F4).
C2's registry leg passes in every case, including F6's two forged rows — none of these defects
moves its output.
## Residual risk / gaps
- F1 is spec-derived (no GFM renderer present); the missing header/delimiter after empty line
  112 and the row bytes are observed.
- Lane mutated during the seat (`e50b388` landed after my first read; worktree `c1-count.py`
  changed under the seat). Every digest and run above is commit-pinned; no worktree-only
  measurement is asserted as landing truth.
- Not measured: any downstream consumer assuming the rows are in the table; the only reader
  found is `c2-count.py`.
