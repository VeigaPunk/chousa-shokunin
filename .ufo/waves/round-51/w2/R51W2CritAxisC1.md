# R51W2CritAxisC1 — is C1 an axis move, and are C1/C2/C3 separable?

Seat R51W2CritAxisC1, round 51 wave 2 (falsify). Only write: this file. No install.
Tip check: the assignment names tip `4436e279`; live HEAD is `72566c84` and
`git merge-base --is-ancestor 4436e279 HEAD` → YES, `git diff --stat 4436e279 HEAD` → 4 files, all
`.ufo/waves/round-51/{gen-w2-spec.py,w2-dispatch.json,w2-run.err,w2-spec.json}`. All runs below use a
clone pinned at the stated tip (`git clone --no-hardlinks` → `S/lane`, `git rev-parse HEAD` = `4436e279…`,
`rev-parse --show-toplevel` = `$S/lane`), scratch `/dev/shm/chousa-r51-R51W2CritAxisC1/` (removed at end).

## 1. C1 is plumbing; it moves the operability observable by 0 (holds, with one disclosure owed)

The frozen observable is not the adopter. `SCORECARD.md:7`:
`| operability | 3 | Gate commit 31b46832…: A/B/C each exit 1 with exactly one full DRIFT summary; .ufo/evidence/round-1/acceptance.json; baseline 34774a1… was 0/3 | 1 |`.
That line is byte-identical at tip — `git diff 9ec1751 4436e27 -- SCORECARD.md` prints one hunk only,
`@@ -2618,3 +2618,12 @@` (the four append-only `correction:` lines); nothing near :7. The adopter cannot even
enter the observable: `grep -c RESEARCH_GATE tools/assimilate-rows.py` → `0`. And the observable still
measures what it measured: replaying the acceptance rows at tip (read-only; `git status --porcelain` shows
no new write) prints, for each of A/B/C:
`A-shokunin-tradition.md rc=1 DRIFT=1 · B-multiagent-knowledge.md rc=1 DRIFT=1 · C-rank-taxonomy.md rc=1 DRIFT=1`
→ 3/3, unchanged since round 1. So C1's move on this axis is 0 measured, 0 harmed; `SCORECARD.md:2618`
("The numeric operability scale stays 3/10") is not contradicted by anything that landed.

The tag is right by the lane's own rule: `corpus/QUALITY.md:64` — plumbing is a claim that "changes a
gate, counter, receipt pipeline or registry mechanism"; the adopter is a registry mechanism, and rounds
49/50 already tag it so (`SCORECARD.md:2586`, `:2616`). `grep -n "Round 51 verdict…" SCORECARD.md` → no
match: no round-51 verdict table has landed, so the only text calling C1 "operability … capability
extension" is the claims heading. Verdict on the framing: C1 is plumbing for the lane's own assimilation,
not an operability move; a draft verdict row must not say the 3/10 moved.

## 2. Strongest counterexample: on the real package the artifact needed a human refusal edit

The counter generates its own packages; the package the round actually assimilated is
`/home/vgpnk/Projects/shokuknow/merge/chousa`. Copied to scratch (`cp -a`, package untouched) and run at
the state the round integrated against (`git show 9ec1751:corpus/SOURCES.md`):

```
$ python3 tools/assimilate-rows.py --staged $S/real/staged.md --knowledge $S/real/knowledge \
    --registry $S/real/registry-base.md --opened 2026-10-25 --out $S/real/out-base \
    --entry corpus/knowledge/japanese-search-record-r38.md \
    --entry corpus/knowledge/chinese-search-record-r39.md \
    --entry corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
RC=0  CITED=7 APPEND=7 HELD=0  BODYONLY=5
S109→S107 S110→S108 S116→S109 S117→S110 S119→S111 S125→S112 S126→S113   (all append)
```
i.e. run as staged it mints **S112 for the `.docx` this round REFUSED** and shifts the jahbs row to S113.
The landed registry has no row before S112's jahbs row (`corpus/SOURCES.md:117-122`; S112 =
`jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf`). Dropping exactly the staged amendment's
`source: S125 — …` line (line 4 of the staged copy) and rerunning reproduces the landed mapping exactly:
`S109→S107 S110→S108 S116→S109 S117→S110 S119→S111 S126→S112`, 6 append rows. So the round's six rows are
the adopter's output *after* one manual line drop — the landed entry says so in prose
(`corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`: "its body-only ids are dropped,
not renumbered"). This is not a predicate violation (R51-C1 does not contain a refusal leg) and not a
reason to change a predicate: it is the reason C1=PASS on synthetic packages is not evidence that the
tool assimilates a package unattended. The C1 row and the LOG must disclose it: *the real package run
appends seven rows including the refused `.docx`; the landed six required dropping that `source:` line,
which shifts every later id by one.*

## 3. Causal separability — matrix (all commands run, all exits captured)

| experiment in `$S/lane` | C1 | C2 | C3 |
|---|---|---|---|
| tip | `LEGS=5/5 C1=PASS` rc=0 (×3 runs) | `C2=PASS` rc=0 (61/61 legs) | `DANGLING=0 C3=PASS` rc=0 (36/74) |
| `tools/assimilate-rows.py` := base (`git show 9ec1751:…`) | `LEGS=0/5 C1=FAIL` rc=1 | `C2=PASS` rc=0, **byte-identical** (`diff -u` empty) | `C3=PASS` rc=0, **byte-identical** |
| `rm tools/assimilate-rows.py` | — | `C2=PASS` rc=0, **byte-identical** | `DANGLING SCORECARD.md:2586/:2616 tools/assimilate-rows.py`, `DANGLING=2 C3=FAIL` rc=1 |
| the three entries deleted | `LEGS=5/5 C1=PASS` rc=0 | `C2=FAIL` rc=1 | `C3=PASS`, **byte-identical** |
| all C2 artifacts deleted (`corpus/knowledge`, `corpus/SOURCES.md`, `lessons/round-51.md`, `spans.tsv`, `quotes.tsv`) | `LEGS=5/5 C1=PASS` rc=0 | — | `DANGLING=29 C3=FAIL` rc=1 |

Readings:
- **C1 ⊥ C2 holds as claimed.** The claims sentence "C1's counter … reads no lane entry or registry row"
  is exactly true: with `corpus/knowledge` and `corpus/SOURCES.md` absent C1 still prints 5/5. It does read
  lane bytes it does not name — the pinned round-50 fixtures (`c1-count.py:26`, `R50_PIN`), whose digest
  change exits 2 — so the sentence is accurate as written and would be false if it said "no lane file".
- **C2 ⊥ C1 holds.** Replacing the tool with the base version (or deleting it) leaves C2 byte-identical:
  `diff -u $S/c2-tip.txt $S/c2-basetool.txt` empty, same for `c2-notool.txt`. C2's only subprocesses are
  git reads, `quote-substance-check.py` and `inference-ground.py` (`c2-count.py:145,182,216,229`).
- **C3 ⊥ C1 content holds; C3 ⊥ C1 existence does not.** `diff -u $S/c3-tip.txt $S/c3-basetool.txt`
  empty, but deleting the tool yields `DANGLING=2` at the two capability rows that point at it. The
  claims wording ("reads … the file tree only") is true; the separability sentence needs the
  qualification, because a C1 file rename is a C3 failure unless a `correction:` line lands. These rows
  predate round 51 (`SCORECARD.md:2586` round 49, `:2616` round 50) — pre-existing coupling, not a
  round-51 regression. Positive controls in the opposite direction all pass: base tool → C1 0/5; entries
  absent → C2 FAIL; tool absent → C3 FAIL, so no counter is blind to its own object.
- Detail, not a defect: `claims.md` quotes before `LEGS=1/5` while base-tool-on-tip-fixtures gives 0/5 —
  the before receipt is the whole lane at `d603f6f` (`controls/c1-lane-before.txt:1` `SELFTEST_DEFAULT=PASS`)
  and the fixtures changed at `cf642c6`; the `SELFTEST_DEFAULT` leg is fixture-coupled, as designed.

## 4. Smallest safe correction (text only; no predicate, target, counter or control touched)

1. In the wave-2 report/LOG, the C1 row: name it plumbing, state the axis score is untouched (3/10),
   cite `SCORECARD.md:7` unchanged plus the A/B/C replay (`rc=1 DRIFT=1` ×3), and add the §2 disclosure
   sentence about the seven-row real run and the manual `S125` drop. Nothing else.
2. In the same text, qualify separability: C3's PASS requires the two adopter-pointer files to exist
   (`SCORECARD.md:2586`, `:2616`); a C1 file move needs a `correction:` line, as round 51 already did for
   four pointers.
3. Out-of-seat observation for the README/coverage seat (not judged here): `corpus/README.md:1100` says
   "no gate, tool or counter changed this round" inside the round-51 coverage block, while
   `git diff --stat d603f6f 4436e27 -- tools corpus/evidence/round51` reports
   `tools/assimilate-rows.py | 160 +++++--` among 79 files. The clause is false as written and denies the
   very landing C1 reports.
4. Integrity note for the L1: the live worktree carries `M .ufo/waves/round-51/w1/R51DraftSkillGates.md`
   (a w1 seat report, assigned read-only evidence); I did not touch it.

## 5. What I ran, and clean-up

Commands above, all from the pinned clone except the read-only A/B/C replay (lane root, no write: only
pre-existing worktree entries appear in `git status`). Outputs kept only long enough to quote; scratch
`/dev/shm/chousa-r51-R51W2CritAxisC1/` deleted (`rm -rf`), no lane file written but this one.

VERDICT: attacked C1 as an axis move and the claimed three-way separability — C1 is plumbing that moves
the 3/10 operability observable by zero (observable re-measured 3/3 at tip; tool emits no DRIFT) and its
real-package run needed a manual refusal edit the counter cannot see; separability holds for C1⊥C2, C2⊥C1
and C3⊥C1-content (byte-identical counters under tool substitution, C1 5/5 with every C2 artifact gone),
but C3 FAILs with 2 dangling rows if the adopter file is deleted, so the claims' separable framing needs
that one qualification and the C1 row needs the real-run disclosure; no predicate, target or control is
implicated.
