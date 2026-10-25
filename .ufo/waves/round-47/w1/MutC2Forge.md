# MutC2Forge — round 47 w1 — forges against `corpus/evidence/round47/c2-count.py`

Seat: L1Chousa47.MutC2Forge (mutation-tester, leaf). No fetch, no installs, no lane writes except this file.

## Item
Run forges (a)–(g) against the R47-C2 counter on /tmp copies via `--root`. Paste each output and exit code. Name every
forge that scores `C2=PASS` and say whether the claim's named limit covers it (`claims.md:97-98`: "row truth … stays a
reader's check; an entry cell can still name a script that is not a gate").

## Instrument and bytes
- Counter, run from the lane in place: `corpus/evidence/round47/c2-count.py` sha256 `36b3934eda5b8ccd569bf577db51f1ac5286463ba8104ec43d777b72658336d1`
- Pinned r46 module: `corpus/evidence/round46/c2-count.py` sha256 `f93cb10795ef7402848ea355680a6b0bd25ad68c8913c24944ef92029c81046f` (matches `R46_SHA`, c2-count.py:51)
- Lane HEAD `a15610a`. SKILL.md `0fcdc442…d2d1`, QUALITY.md `8c989355…35e2`. The lane and scratch hashes were identical before and after.
- Scratch: `tar --exclude=./.git` copy of the lane into `/tmp/chousa-r47-MutC2Forge/lane`. The driver is `drive.py`. It applies a
  forge, runs `python3 <lane counter> --root <scratch>`, restores the touched files (SKILL.md, QUALITY.md, the r46
  counter, tools/research-gate.sh, tools/noop.py) and compares their sha256 to the pristine values. All 18 forges
  printed `restored=ok`. The scratch was deleted afterwards.
- The junk rows carry the 25 paths from `--list` on pristine scratch. These are the same 25 as the lane baseline
  (`ENTRY_POINTS=92 … UNREGISTERED=25 DANGLING=0 MISMATCHES=25 C2=FAIL`, exit 1).

## Outputs
Each run printed every counter line except FLOOR, GATES_ROWS and REGISTERED, which the table leaves out. FLOOR was 92
on every run. Where `UNREGISTERED=0`, REGISTERED was n/n.

| forge | ENTRY_POINTS (abc/dep/chk) | UNREG | DANGLING | MISM | verdict | exit |
|---|---|---|---|---|---|---|
| P pristine scratch | 92 (84/+1/+7) | 25 | 0 | 25 | C2=FAIL | 1 |
| **a** one 8-cell row, 25 paths in entry cell, verdict `exit 0` | 92 (84/+1/+7) | 0 | 0 | 0 | **C2=PASS** | 0 |
| b same row, paths in 5th cell only | 92 | 25 | 0 | 25 | C2=FAIL | 1 |
| **b2** `\|`-escaped shift: `\| junk \| gate \\\| PATHS \\\| exit 0 \| none \| none \|…` | 92 | 0 | 0 | 0 | **C2=PASS** | 0 |
| c row (a) inside a ```` ``` ```` fence | 92 | 25 | 0 | 25 | C2=FAIL | 1 |
| **c2** row (a) inside a `~~~` fence | 92 | 0 | 0 | 0 | **C2=PASS** | 0 |
| **c3** row (a) inside a `<div hidden>`…`</div>` HTML block (no blank lines) | 92 | 0 | 0 | 0 | **C2=PASS** | 0 |
| d `<!-- ROW_A -->` on one line | 92 | 25 | 0 | 25 | C2=FAIL | 1 |
| d2 `<!--` / ROW_A / `-->` | 92 | 25 | 0 | 25 | C2=FAIL | 1 |
| **d3** `\| junk \| gate <!-- a --> \| <!-- PATHS --> \| <!-- exit 0 --> \| x…` | 92 | 0 | 0 | 0 | **C2=PASS** | 0 |
| e1 delete `tools/research-gate.sh` (its Gates row stays) | 91 (83/+1/+7) | 25 | **1** | 26 | C2=FAIL | 1 |
| e2 (a) + exit row naming `tools/ghost-gate.py` | 92 | 0 | **1** | 1 | C2=FAIL | 1 |
| **e3** (a) + row naming `tools/ghost-gate.py`, verdict `` `0` clean · `1` failed `` (no word `exit`) | 92 | 0 | 0 | 0 | **C2=PASS** | 0 |
| **e4** (a) + exit row naming root-level `ghost-gate.py` | 92 | 0 | 0 | 0 | **C2=PASS** | 0 |
| f1 delete `corpus/evidence/round46/c2-count.py` | — | — | — | — | `R46_INSTRUMENT=absent` C2=FAIL | 2 |
| f2 one byte of the same file (`frozen`→`Frozen`) | — | — | — | — | `R46_INSTRUMENT=changed 39b5902320ff` C2=FAIL | 2 |
| g1 (a) + QUALITY mention of `corpus/evidence/round30/rerun-check.py` replaced (1 mention) | **91** (84/+1/+6) | 0 | 0 | 0 | C2=FAIL (floor) | 1 |
| **g2** g1 + empty `tools/noop.py`, listed in the junk row | 92 (85/+1/+6) | 0 | 0 | 0 | **C2=PASS** | 0 |

## Verdicts on the asked probes
- (a) **survives** with `C2=PASS`, exit 0. **Covered by the named limit.** The row names real entry points in its entry
  cell, and its `exit 0` verdict map is false for most of them. That is exactly the "row truth stays a reader's check"
  limit. It is still the cheapest full-marks gate: one row registers all 25 paths, and no per-script verdict is
  needed. The docstring's QUALITY 60 paragraph (c2-count.py:34-39) names "a Gates row whose verdict map is wrong" but
  not one row registering many paths at once.
- (b) **killed**: the cell roles hold, so the defect-4 repair works for the plain case.
- (c) **killed** for backtick fences.
- (d) **killed** for single-line and multi-line comments.
- (e) **DANGLING fires** for an exit-bearing row that names a missing slash path: e1 and e2 both give `DANGLING=1`.
- (f) **refused** in both cases: exit 2 with `R46_INSTRUMENT=absent` or `changed`.
- (g) **killed by the floor** for a pure deletion: ENTRY_POINTS=91 < 92 gives C2=FAIL with MISMATCHES=0.

## Extra forges that score C2=PASS (none is covered by the named limit)
1. **b2, escaped pipes.** c2-count.py:133 splits the row on every `|`, including GFM-escaped `\|`. GFM renders the
   b2 row with the paths and `exit 0` inside the 2nd (`kind`) cell, and its entry and verdict cells read `none`.
   The counter still reads cells[2]/[3] as entry/verdict. Routed defect 4 (cell roles) is only half-closed. This is
   not row truth: the path is not in the rendered `entry` cell at all.
2. **c2, `~~~` fence.** The fence test in r46 `gates_rows` (round46/c2-count.py:87) only knows ```` ``` ````. A tilde
   fence is literal source too. The r46 docstring (`:77-80`) says a fenced line "never registers a path".
3. **c3, HTML block.** Under CommonMark/GFM block rules, the row lines inside `<div hidden>` with no blank line are
   HTML-block text, not a table row. Whether GitHub's sanitizer keeps the `hidden` attribute is [INFERENCE], not
   rendered here. Either way the counter registers 25 paths from a non-row.
4. **d3, second inline comment.** r46 `gates_rows` (`:96-102`) strips only the FIRST `<!--…-->` on a line. Comments
   two and three stay in `bare`, so the paths and `exit 0` count while the rendered row shows empty cells.
5. **e3, a row without the word `exit`.** DANGLING only scans `gates_rows`, which requires the word `exit`
   (round46:109; round47:137-138). A registry row with a numeric verdict map names a script the tree lacks and
   scores DANGLING=0. This contradicts the predicate "a Gates row names a `*.py`/`*.sh` path the tree does not hold".
6. **e4, path without a slash.** `NAMED` (round46/c2-count.py:43) needs at least one `/`. A root-level
   `ghost-gate.py` is a repo-relative `*.py` path, but it is invisible to DANGLING.
7. **g2, floor substitution.** FLOOR is only a count (c2-count.py:159). Removing a check-named gate and adding any
   empty file under `tools/` restores 92. The docstring's "deleting a QUALITY `Check:` path … shrinks the set below
   FLOOR and fails" (`:36-37`) holds only for a pure deletion.

## Side finding: a real row is wrongly unregistered
SKILL.md:100 (`mechanism-witness`) has unescaped pipes inside a code span, in `` `WITNESS=pass|fail|unparseable|timeout` ``.
The split gives 11 cells, and cells[3] is `` ` WITNESS=pass`` with no `exit`. So `tools/mechanism-witness.py` is
among the 25 UNREGISTERED even though the row has an entry and an exit-bearing verdict. GFM also splits that cell, so
the rendered row is malformed as well. Escaping those pipes as `\|` alone will not register it, because the counter
ignores escapes (b2).

## Summary
PASS-scoring forges: a, b2, c2, c3, d3, e3, e4, g2. Only (a) is covered by the named limit. The other seven break
something the predicate or docstring promises: cell roles, fence and comment awareness, DANGLING over "a Gates row",
and a floor that is enforced as a count but described as protecting the set. b, c, d, e1/e2, f1/f2 and g1 are
killed. Each surviving mutant is a coverage finding, not a contract change. No tools were installed.
