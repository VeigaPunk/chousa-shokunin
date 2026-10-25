# ReviewerC2Set — round 47 w1: independent re-derivation of the R47-C2 entry-point set

Item: re-derive C2's set with my own script (legs A–C per the round-46 docstring, D dependence closed,
E check-named), compare set-for-set with `c2-count.py --list` and the ENTRY_POINTS line, and check the
docstring against the code (`./` handling, binary reads, comments counted as dependence).
Lane tip `a15610a59aaeaf43b79ccc650acee4bd4da00341`. Pinned digests: round46/c2-count.py `f93cb107…046f`
(matches R46_SHA), round47/c2-count.py `36b3934e…36d1`, SKILL.md `0fcdc442…d2d1`, QUALITY.md `8c989355…35e2`.
Instrument: `/tmp/chousa-r47-ReviewerC2Set/derive.py` (sha256 `6bea8c8a…cfe3`, deleted after the run). It imports
neither counter and uses its own path regex with `./` normalisation, its own leg walks, three D variants (all
text / string literals plus docstrings / string literals only) and two cell splitters (naive and GFM, where `\|` stays inside the cell).
Set comparison: a /tmp copy of the round-47 counter, changed only to dump `eps`, run with `--root` against the lane.
Probes ran on an rsync copy of the lane in /tmp. No lane file was written apart from this report, and nothing was fetched or installed.

## Verdict
SET AGREES: my set and the counter's are identical, 92 = 92 with no difference in either direction, and the A–C subset is 84 = 84.
The ENTRY_POINTS line reproduces. **The UNREGISTERED count does not hold as a measurement of the predicate.** About 10 of the 25
mismatches come from a parser defect (F1), and the "exit code in verdict map" test accepts and rejects the wrong cells (F2).
Treat MISMATCHES=25 as an upper bound. On today's tree the GFM-correct count is 15.

## Commands and decisive output
`python3 corpus/evidence/round47/c2-count.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --list` (exit 1):
```
UNREGISTERED_PATH .ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh   … (25 lines; full list = MINE below)
ENTRY_POINTS=92 (abc=84 dependence=+1 check_named=+7)
FLOOR=92  GATES_ROWS=36  REGISTERED=67/92  UNREGISTERED=25  DANGLING=0  MISMATCHES=25  C2=FAIL
```
`python3 derive.py <lane>`:
```
A=8 B=53 C=82 C_raw=82 C_cmd=61 E=27 E_fenceaware=27   ABC=84 E_new=7 seed=91
EP[all]=92 D_new=1 ['corpus/evidence/round25-meta-oracle.py']   (EP[str+doc]=92, EP[str]=92, same member)
D_edges_all [('corpus/evidence/round25-meta-differential.sh', 'corpus/evidence/round25-meta-oracle.py')]
binary_read None
E_only: mask-gate.sh, receipt-binding.py, slen-probe.sh, round29/prose-check.py, round30/rerun-check.py,
        round32/q33-check.py, round45/tag-count.py           (= counter chk, 7/7)
GATES_ROWS=36 entry_rows_naive=29 entry_rows_gfm=30
UNREG_naive=25 UNREG_gfm=15 DANGLING=0
naive_minus_gfm: round24-measure.sh round25-ledger-recount.py round25-measure.sh round25-meta-differential.sh
  round26-date-differential.sh round26-measure.sh round26-registry-differential.sh round27-falsify-controls.py
  round27-mechanisms.py round27-regressions.py
```
Set diff: `eps 92 92 counter-mine [] mine-counter []`, `abc 84 84 counter-mine [] mine-counter []`. Counter
`dep=['corpus/evidence/round25-meta-oracle.py']`, and its `chk` equals my E_only. My 25 naive-split UNREGISTERED paths match the
counter's 25 line for line. The dependence edge is real code: `round25-meta-differential.sh:40`
`run(["python3", "corpus/evidence/round25-meta-oracle.py", p], strict)`, with a mention in the comment at `:6` as well.
On today's tree, comments and docstrings add nothing to D: all three variants give 92.

## Findings (by severity)
**F1 HIGH (calibration): the cell splitter ignores GFM's `\|` escape, which inflates UNREGISTERED by 10.**
`round47/c2-count.py:133` `cells = r.strip().strip("|").split("|")`. SKILL.md:114 (round-46 registration row)
escapes its argument pipes correctly: `` `round26-measure.sh TREE [c1\|c2\|c3\|holds\|all]` ``. GFM renders
those as literal pipes inside the entry cell. The counter splits on them, so `cells[3]` becomes `c2\` and has no "exit". The whole
row is then dropped and its 10 instruments read as unregistered, even though the real verdict cell ("counts, never verdicts, but the exit codes
are NOT uniform…") contains "exit". Probe P5 rewrote only `\|` to `,` on that row: `UNREGISTERED=15`. My GFM
splitter, which leaves `\|` inside the cell, gives 15 on the unmodified tree. Consequence: reaching `MISMATCHES=0` forces a rewrite of valid Markdown
to suit the parser. Row 100 (`mechanism-witness`) is different: its pipes in `WITNESS=pass|fail|…` are
unescaped, GFM splits them too, so that row really is malformed and `tools/mechanism-witness.py` is correctly
UNREGISTERED. Fix the SKILL.md row there (escape the pipes), not the counter.

**F2 MEDIUM (calibration): the docstring says the verdict map "names an exit code"; the code checks for the substring `exit`.**
`round47/c2-count.py:134` `"exit" in cells[3]`. False rejections: SKILL.md rows 80, 83, 84, 85, 87 (the
research-gate rows) have verdict maps of the form `` `0` clean · `1` failed · `2` could-not-evaluate ``. Those are exit
codes, but without the word the rows are dropped. Today this is masked because another row names `tools/research-gate.sh`. False acceptance:
probe P7 forged a row whose verdict cell is literally `no exit code documented` and whose entry is `python3 tools/mechanism-witness.py`.
The result was `UNREGISTERED=24`, with mechanism-witness registered. That is a cheap gate: one word registers a path.

**F3 MEDIUM (calibration / floor): A–C keep `./`-prefixed paths verbatim, so duplicates pad ENTRY_POINTS.**
The round-46 `NAMED` regex matches `./tools/x.py`, and `entry_points()` (r46:65-68) adds that string unnormalised.
Round 47 strips `./` only in D, E and DANGLING (`existing_named`, r47:72; r47:141), so the union holds both forms.
Probe P1 appended `` `python3 ./tools/research-gate.sh` `` to round47/claims.md:
`ENTRY_POINTS=93 (abc=85 …) UNREGISTERED=26`, plus `UNREGISTERED_PATH ./tools/research-gate.sh`. A Gates row naming
`./tools/research-gate.sh` would register that duplicate. Result: one claims mention plus one row lifts ENTRY_POINTS above FLOOR with no
new gate. There is no live instance today (`C_raw - C = []`). The docstring's "A–C unchanged" is literally true, but the union's
"repo-relative path" identity is not.

**F4 MEDIUM (operability / reproducibility): leg A counts every regular file under `tools/`, including untracked, transient, non-script and binary ones,
and D then reads them as source.**
r46:50 `p.is_file()` has no extension or tracked-file filter, and r47:117-121 reads every entry point with
`errors="replace"`. Observed live: my first `ls tools/` (≈11:44 UTC) listed an untracked `tools/swarm-registry.json`, and one
minute later it was gone (`ls -la --time-style=full-iso tools/` shows 8 scripts plus `__pycache__`; there is no git history for the path).
I could not trace who wrote it. [INFERENCE] A sibling seat probed in place. P2 (`{}` written to that path):
`ENTRY_POINTS=93 UNREGISTERED=26`. P3 (`tools/blob.bin` with NUL bytes embedding `.ufo/waves/round-47/gen-w1-spec.py`):
`ENTRY_POINTS=94 dependence=+2`. The binary is decoded as text, and its embedded path pulls an **untracked** script into the set.
So the docstring's "inside the source of an entry point" does not hold. On today's tree there are no binaries, and every one of the 92
entry points is tracked (`untracked_eps []`). The counter's output still depends on transient working-tree state that it does not report.

**F5 LOW (calibration): dependence counts literals that appear only in comments or docstrings.**
`existing_named(root, src, rx)` runs over the whole file. P4 appended `# historical note: .ufo/waves/round-47/gen-w1-spec.py`
to tools/quote-reopen.py and got `dependence=+2`. The docstring justifies D as "a script a gate reads or runs", and a comment does
neither. My "string literals only" variant gives the same 92 today, so there is no live effect. Comment-only mentions do count toward FLOOR, though.
Should they? Not under the stated rationale. That said, over-inclusion is the safe direction for registry completeness and the unsafe one for the floor.

**F6 LOW: `outside_gates` (r47:79-86) ignores code fences, while the round-46 `gates_rows` honours them.** A fenced line beginning `## `
outside Gates would toggle the section. There is no live effect today (`E_fenceaware=27 = E`).

**F7 LOW: blind spots in DANGLING.** P8: a row entry `tools/mechanism-witness.py.bak` is not reported dangling, because `\.py\b` truncates
it to the existing `tools/mechanism-witness.py`. `names()` correctly refuses to register it. P9: an absolute path
`/abs/tools/gone.py` cannot be seen by the regex, while `chousa-shokunin/tools/gone2.py` is reported (`DANGLING=1`).

**F8 INFO: the leg C docstring is narrower than the code.** r46:12-13 says "names **as a counting command**", but `NAMED` takes every
mention. By my heuristic (backtick spans or line starts with python3, bash or sh), 11 union members exist only by mention: 8 `.ufo/waves/round-3[5-9]|41/controls/*`,
`round30/qr_harness.py`, `round33/no-name-signals.sh`, `round46/build-spans.py`. This was chosen deliberately in round 46
(`CritC2Scope` comment at r46:40-42). It is noted here because the sentence does not match the code; it is not a defect in A–C.

**F9 INFO:** running the counter writes `corpus/evidence/round46/__pycache__/c2-count.cpython-314.pyc` (mtime 08:33 -0300,
seen there). That path is gitignored (`.gitignore:3 corpus/**/__pycache__/`), leg B does not recurse into it, and the tree is unaffected.

## Residual risk and verification gaps
- The FLOOR (92) was measured with the same parser and leg A, so F3 and F4 inflation could hold the floor up artificially. I did not
  check whether the freeze-tree 92 depended on any transient file. It probably did not: my run matches it with only tracked files.
- F1 and F2 interact. The GFM-correct UNREGISTERED is 15, but under a "names an exit code" reading the five research-gate rows would
  also register, which changes nothing today because research-gate.sh is registered elsewhere.
- The C_cmd split in F8 is my heuristic, not a parse of "counting command".
- I did not check whether a row's verdict map is actually correct. As both docstrings say, row truth remains a reader's check.

No tools were installed and nothing was fetched. Scratch `/tmp/chousa-r47-ReviewerC2Set/` (script, counter copy, lane copy) was deleted.
