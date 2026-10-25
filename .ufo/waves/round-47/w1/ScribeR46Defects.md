# ScribeR46Defects — disposition of round-46 closure routed defects 1–6 (round 47, wave 1)

item: dispose `corpus/lessons/round-46-verifier-spotcheck.md` §6 defects 1–6; for defect 3 re-run the
`controls/c2-controls.txt` forges against the FINAL round-46 counter on /tmp copies and draft a refreshed
receipt. Seat: scribe (leaf). No lane production write, no git/jj mutation, no fetch, no install.
Lane HEAD `a15610a` (freeze `22a44b8`). All runs `PYTHONDONTWRITEBYTECODE=1` (no `__pycache__` left).

## Verdict
- Defect 3 is **real and now quantified**. The committed receipt is the pre-widening counter's
  output (`f2fcb654…`). The final counter `f93cb10795ef7402848ea355680a6b0bd25ad68c8913c24944ef92029c81046f`
  (= `sha256sum corpus/evidence/round46/c2-count.py`) prints `79 (named=74) 58/79 UNREGISTERED=21` on the same tree.
  Honest count: **ten forges, eight refusals plus two passing blocks** (dotslash, 7pipe). The header's
  "nine refusals and one positive control" is wrong under both counters.
- The forge bytes were never committed (`CritRoundHonesty` #11; `find -name 'SKILL-*'`=0). I rebuilt them from
  their descriptions (`MutC2Forge`, `MutC2More` a2/a3/b3, `CritC2Scope` §1, receipt history `d09fc8e`→`c294484`).
  **Calibration:** my rebuild plus the old counter reproduces all ten stale blocks exactly, `GATES_ROWS` included.
- Under the old receipt's 16-path content, the final counter no longer passes dotslash or 7pipe
  (`74/79 UNREGISTERED=5`). The five `.ufo/waves/round-3{5,6,7,9}/controls/*` paths added by `1e9756f` are missing from that content.
- The round-47 counter closes the 7pipe class (defect 4) and enforces the floor (defect 2) on the same tree.

## Tree and forge recipe
Tree A (`/tmp/c46A` in the receipt) = `git archive 6e2630a6` + `c1/c2/c3-count.py` from `5c6e2ca`, with **no**
round-46 `claims.md`. With `claims.md` added the counter prints `named=77`/`69`, which is the receipt's tree B shape. Base `SKILL.md`
`7b49e2ae…d05433`. Each forge inserts one block after the last Gates table row (line 111). `after` instead
inserts after the next `## ` heading (line 503). Paths = the counter's own `--list` (16 old / 21 final).
Valid row = `| forged | gate | <paths> | \`0\` ok · \`1\` drift (exit 0/1) | none | none | none | nobody |`.
prose = paragraph; 6cell = 7 pipes; noexit = 9 pipes, no `exit`; fenced = in a fence; suffix = `…pyc`/`…shc`;
abut = `<!--x-->` + row; multicomment = `<!--`/row/`-->`; dotslash = `./` paths; 7pipe = paths in the 8th cell.
[INFERENCE] The original 7pipe cell layout is unrecoverable. The round-46 counter ignores cell roles, so any layout gives the same output.

## Commands (verbatim decisive output)
```
$ python3 corpus/evidence/round46/c2-count.py --root $S/V1     # final f93cb107, tree A
ENTRY_POINTS=79 (tools=7 counters=50 named=74) GATES_ROWS=30 REGISTERED=58/79 UNREGISTERED=21 C2=FAIL
$ python3 $S/old/c2-count-f2fcb654.py --root $S/V1             # `git show c294484:…/c2-count.py`, sha f2fcb654fb207898…
ENTRY_POINTS=71 (tools=7 counters=50 named=66) GATES_ROWS=30 REGISTERED=55/71 UNREGISTERED=16 C2=FAIL
== R0 old counter + 16-path forges: prose/6cell/noexit/after/fenced/abut/multicomment GATES_ROWS=30 55/71 exit=1;
   suffix GATES_ROWS=31 55/71 exit=1; dotslash, 7pipe GATES_ROWS=31 REGISTERED=71/71 C2=PASS exit=0  (== committed file)
== R1 final counter + 21-path forges: see refreshed receipt below (8 × exit=1, 2 × exit=0)
== R2 final counter + 16-path forges: 8 refusals unchanged at 58/79; dotslash, 7pipe REGISTERED=74/79 UNREGISTERED=5 exit=1
$ python3 corpus/evidence/round47/c2-count.py --root $S/V47 [--list]   # same tree A, round-47 counter
ENTRY_POINTS=87 (abc=79 dependence=+1 check_named=+7) FLOOR=92 GATES_ROWS=30 REGISTERED=53/87 UNREGISTERED=34 DANGLING=0 MISMATCHES=34 C2=FAIL exit=1
  7pipe (34 paths, 8th cell)  GATES_ROWS=31 REGISTERED=53/87 UNREGISTERED=34 MISMATCHES=34 C2=FAIL exit=1
  entrycell (34, entry cell)  GATES_ROWS=31 REGISTERED=87/87 UNREGISTERED=0 MISMATCHES=0 C2=FAIL exit=1   ← 87 < FLOOR 92
  dotslash (34, `./`)         REGISTERED=87/87 MISMATCHES=0 C2=FAIL exit=1 (floor); suffix 53/87 DANGLING=0 exit=1; multicomment GATES_ROWS=30 exit=1
$ python3 corpus/evidence/round46/c2-count.py --root $S/V1 --skill entrycell  → REGISTERED=79/79 C2=PASS (r46 has no floor leg)
$ python3 corpus/evidence/round47/c2-count.py   # lane working tree
ENTRY_POINTS=92 (abc=84 dependence=+1 check_named=+7) FLOOR=92 GATES_ROWS=36 REGISTERED=67/92 UNREGISTERED=25 DANGLING=0 MISMATCHES=25 C2=FAIL  rc=1
$ git diff --stat 22a44b8 HEAD -- corpus/evidence/round47/ ; git status --porcelain -- corpus/evidence/round47/   → (empty, empty)
```
Hashes: gen.py `177a5d2a…`. 21-path forges: prose `503d31ab`, 6cell `d9f0f56b`, noexit `a8c1d92c`, after `88359810`,
fenced `ab07a585`, suffix `ece6c61b`, abut `5e36aba9`, multicomment `5d3a4924`, dotslash `27bdf21d`, 7pipe `5c280146`.
r47 forges: 7pipe `75ed8b49`, entrycell `6f3c30a0`. r47 `c2-count.py` `36b3934e…` (== freeze), `c3-count.py` `ce93fe29…`.

## Draft — refreshed `corpus/evidence/round46/controls/c2-controls.txt`
```
### R46-C2 controls (final counter f93cb10795ef7402848ea355680a6b0bd25ad68c8913c24944ef92029c81046f —
### ten forges: eight refusals and two passing blocks; regenerated round 47 over the final counter)
### tree /tmp/c46A = git archive 6e2630a6 + corpus/evidence/round46/{c1,c2,c3}-count.py at 5c6e2ca (no claims.md)
### base SKILL.md 7b49e2ae…d05433; one forged block after Gates table line 111 (`after`: after line 503);
### forged paths = the 21 UNREGISTERED_PATH lines of the baseline run below
$ python3 corpus/evidence/round46/c2-count.py --root /tmp/c46A          # baseline, no forge
ENTRY_POINTS=79 (tools=7 counters=50 named=74) GATES_ROWS=30 REGISTERED=58/79 UNREGISTERED=21 C2=FAIL exit=1
$ ... --root /tmp/c46A --skill <SKILL-prose.md>          # paths as prose in ## Gates
ENTRY_POINTS=79 (tools=7 counters=50 named=74) GATES_ROWS=30 REGISTERED=58/79 UNREGISTERED=21 C2=FAIL exit=1
$ ... --skill <SKILL-6cell.md>                           # six-cell row (7 pipes)
ENTRY_POINTS=79 (tools=7 counters=50 named=74) GATES_ROWS=30 REGISTERED=58/79 UNREGISTERED=21 C2=FAIL exit=1
$ ... --skill <SKILL-noexit.md>                          # eight-cell row, no `exit`
ENTRY_POINTS=79 (tools=7 counters=50 named=74) GATES_ROWS=30 REGISTERED=58/79 UNREGISTERED=21 C2=FAIL exit=1
$ ... --skill <SKILL-after.md>                           # valid row after the next `## `
ENTRY_POINTS=79 (tools=7 counters=50 named=74) GATES_ROWS=30 REGISTERED=58/79 UNREGISTERED=21 C2=FAIL exit=1
$ ... --skill <SKILL-fenced.md>                          # valid row inside a fence
ENTRY_POINTS=79 (tools=7 counters=50 named=74) GATES_ROWS=30 REGISTERED=58/79 UNREGISTERED=21 C2=FAIL exit=1
$ ... --skill <SKILL-suffix.md>                          # row names …pyc/…shc
ENTRY_POINTS=79 (tools=7 counters=50 named=74) GATES_ROWS=31 REGISTERED=58/79 UNREGISTERED=21 C2=FAIL exit=1
$ ... --skill <SKILL-abut.md>                            # <!--x--> abutting the row
ENTRY_POINTS=79 (tools=7 counters=50 named=74) GATES_ROWS=30 REGISTERED=58/79 UNREGISTERED=21 C2=FAIL exit=1
$ ... --skill <SKILL-multicomment.md>                    # <!-- / row / -->
ENTRY_POINTS=79 (tools=7 counters=50 named=74) GATES_ROWS=30 REGISTERED=58/79 UNREGISTERED=21 C2=FAIL exit=1
$ ... --skill <SKILL-dotslash.md>   # PASSES: `./`-prefixed repo-relative paths register (predicate-faithful, MutC2More N2)
ENTRY_POINTS=79 (tools=7 counters=50 named=74) GATES_ROWS=31 REGISTERED=79/79 UNREGISTERED=0 C2=PASS exit=0
$ ... --skill <SKILL-7pipe.md>      # PASSES — SURVIVOR: one 8-cell row, every path in a non-entry cell; cell roles unread
ENTRY_POINTS=79 (tools=7 counters=50 named=74) GATES_ROWS=31 REGISTERED=79/79 UNREGISTERED=0 C2=PASS exit=0
### the previous file's numbers (71/55/16, header f2fcb654) were the pre-widening counter at c294484; re-run
### here, that counter reproduces them exactly on this tree. Forge inputs are not committed: commit
### the generator beside this receipt, or state that the forges are reproducible in shape only.
```

## Draft — disposition table
```
| defect | disposition this round | evidence pointer |
|---|---|---|
| 1 freeze sentence/code gap (C2) | closed by freeze practice: R47 froze sentence + code together (docstring "the same sentence as claims.md"), pins the r46 instrument by sha and kills on drift; zero instrument edits since freeze | corpus/evidence/round47/c2-count.py:4,51,97; claims.md:76-85,95-96; `git diff --stat 22a44b8 HEAD -- corpus/evidence/round47/` = empty |
| 2 kill floor not enforced (C2) | addressed by R47-C2: FLOOR=92 in code, PASS needs ENTRY_POINTS ≥ FLOOR; shown able to fail: MISMATCHES=0 at 87 entry points → C2=FAIL exit 1 (r46 counter: C2=PASS on the same forge) | corpus/evidence/round47/c2-count.py:52,159; this report §Commands (entrycell) |
| 3 stale C2 control receipt labels | receipt regenerated on the final counter f93cb107 (79/58/21); header corrected to "ten forges: eight refusals and two passing blocks"; reconstruction calibrated (old counter reproduces the old file exactly) | draft above; corpus/evidence/round46/controls/c2-controls.txt:1,66-80; .ufo/waves/round-47/w1/ScribeR46Defects.md |
| 4 cheap-gate residue (C2) | 8-pipe-anywhere class closed by R47-C2 cell roles (path must sit in the `entry` cell of a row whose `verdict map` names an exit): 7pipe forge → UNREGISTERED=34 exit 1; dotslash kept and named as predicate-faithful normalization; row truth stays a named reader's check | corpus/evidence/round47/c2-count.py:19-24,131-136; claims.md:71-73,97-98 |
| 5 anchor char drift (C3/SOURCES) | addressed by R47-C3 ANCHOR_BOUND leg (every `char N` in the S085, S090–S094 anchor cells must equal a located quote offset); open until the leg passes: SOURCES S085 still "char 2349" vs spans.tsv 2280/1191 | corpus/evidence/round47/c3-count.py:60,161,199; corpus/SOURCES.md:95; corpus/evidence/round46/spans.tsv:2-3; claims.md:124-126 |
| 6 report wording | correct in the round-47 report: "`CritC2Scope`'s report is committed at `5c6e2ca` (round-46 final commit, +81 lines)"; drop "produced no report … recorded dead" | /home/vgpnk/Projects/shokunin/.ufo/reports/round-46/chousa.md:107-109; `git show --stat 5c6e2ca` → .ufo/waves/round-46/w2/CritC2Scope.md +81 |
```

## Findings (for the L1)
1. **F1 (defect 3, record).** Every one of the ten committed blocks shows 71/55/16, the pre-widening counter's output. The file header says "final counter f2fcb654", which is not the final counter. The closure's claim of eight refusals plus two passing blocks is correct.
2. **F2 (defect 3, content).** If only the labels were relabelled to f93cb107, the receipt would be false. With the stale 16-path content, the final counter does not pass dotslash or 7pipe (`UNREGISTERED=5`). The receipt must be regenerated, not relabelled.
3. **F3 (defect 4, residual).** Under the r47 counter the suffix forge is refused only through UNREGISTERED. DANGLING stays 0 because `NAMED`'s `\.py\b` never matches `…pyc`, so a non-existent `.pyc`/`.shc` name is not flagged as dangling. This is a limit, not a false PASS.
4. **F4 (defect 5).** The lane tree is still in its before-state. S085's anchor is `char 2349` (SOURCES.md:95) and the C3 leg is not yet green. The disposition depends on C3 landing.
5. **F5.** The lane-tree run of the r47 C2 counter matches the frozen before-state (`92/25/0/25 C2=FAIL` rc 1). C2 is unaddressed at HEAD.

## Scope / provenance
Touched: this report only. Scratch `/tmp/chousa-r47-ScribeR46Defects/` (trees V1, V2, A, V47, forges f16/f21/f47,
gen.py) is deleted at finish. Read-only: lane files, fleet report. Out of scope: editing c2-controls.txt, lesson, SKILL.md.
No tool installs.
