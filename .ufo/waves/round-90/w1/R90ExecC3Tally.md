# R90ExecC3Tally — frozen C3 (`C3-TALLY-R90`) before-state + discrimination

Seat `R90ExecC3Tally` (executor leaf). Lane `chousa`, round 90. Tree attacked:
`9bad12011187d114ba2c4588c5df08a21ab28145` (the freeze commit plus the committed control receipts; this was the
lane HEAD while the seat ran). Tree built with
`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 9bad12011187d114ba2c4588c5df08a21ab28145 | tar -x -C $S/tree`.
Scratch `S=/fast/scratch/hyaku/chousa-r90/R90ExecC3Tally`; all temp work under `$S/tmp/*` via `TMPDIR=`, removed
before yield. No writes under `/tmp`, no production edits, no git/jj mutation in the lane or a fixture, no network
call (the selftest is local), no sudo, no pacman transaction, no tool install/upgrade.

Instrument bytes at this revision (sha256, from the extracted tree):

- `corpus/evidence/round90/skill-tally-r90.py` = `c8018d1b34ba61601868eaaa0679d0df1e6e5d0cfc4646f0c745610aa7ebb950`
- `tools/research-gate.sh` = `b23301b6dc141968edc33e838733df9cc3b3ecc2ab815e6d0acffd7efb546065`
- `tools/gate-records.py` = `905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60`
- `SKILL.md` = `f1faa3dde3ea8f87894bc307c663922fcdae4674ae73bcef6f7674c78b918cf9`

Round premise check (not a C3 pass condition):
`git -C <lane> diff --stat f54a45ed197dd475af50d82e43a22df3d2e99782 9bad12011187d114ba2c4588c5df08a21ab28145 -- tools/research-gate.sh tools/gate-records.py SKILL.md`
prints an empty diff (rc 0): both gate tools are unchanged this round and `SKILL.md` is byte-identical to the base,
so the 275 tallies are inherited, not introduced by the freeze.

## Axes

- **A1 before-state fidelity** — reproduce the frozen `Before` exactly.
- **A2 discrimination** — the only change needed to flip the check is the nine current cells.
- **A3 sweep completeness** — enumerate every `PASS (<n> cases` occurrence and classify current vs historical.

## (a) Before-state — reproduced

Command (cwd = `$S/tree`):

```sh
TMPDIR=$S/tmp/a python3 -B corpus/evidence/round90/skill-tally-r90.py --root .
```

Receipt `c3-a-tally.txt` (exit in `c3-a-tally.exit`), full body — nine identical stale lines then the summary:

```
STALE_TALLY PASS (275 cases, 0 skipped) != tool 283/0
STALE_TALLY PASS (275 cases, 0 skipped) != tool 283/0
STALE_TALLY PASS (275 cases, 0 skipped) != tool 283/0
STALE_TALLY PASS (275 cases, 0 skipped) != tool 283/0
STALE_TALLY PASS (275 cases, 0 skipped) != tool 283/0
STALE_TALLY PASS (275 cases, 0 skipped) != tool 283/0
STALE_TALLY PASS (275 cases, 0 skipped) != tool 283/0
STALE_TALLY PASS (275 cases, 0 skipped) != tool 283/0
STALE_TALLY PASS (275 cases, 0 skipped) != tool 283/0
TALLY_ROWS=9 STALE_TALLIES=9/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=FAIL
```

Observed line: `TALLY_ROWS=9 STALE_TALLIES=9/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=FAIL`
Exit: **1**. This matches the frozen `Before` (`STALE_TALLIES=9/9` with `EXPECTED_CASES=283`).

The reproduced body is byte-identical to the committed before-receipt
`corpus/evidence/round90/controls/receipts/c3-before.txt` (`diff` empty; both sha256
`4ea066814ec3a268502e362f4a20e9d5e75c3fc3198bacb421054d1ecd25a6d3`).

Selftest capture (the transcript used by the discrimination leg, same tree) —

```sh
TMPDIR=$S/tmp/b bash tools/research-gate.sh --selftest
```

Receipt `c3-a-selftest.txt` (exit in `c3-a-selftest.exit`): 285 lines, 283 `ok-case` lines, 0 `FAIL-case` lines,
verdict at line 285: `RESEARCH_GATE_SELFTEST: PASS (283 cases, 0 skipped)`, exit **0**. This is the tool's own
verdict the counter re-derives against; the check never reads a literal from the file.

## (b) Discrimination — nine current cells only

`$S/after` is a `cp -a` of `$S/tree`; the only changed file is `SKILL.md`. The edit replaced the exact string
`PASS (275 cases, 0 skipped)` with `PASS (283 cases, 0 skipped)`, asserting 9 occurrences before writing; after the
write the file holds 9 `PASS (283 cases, 0 skipped)` and 0 `PASS (275 cases, 0 skipped)`.

`diff -u` receipt `c3-b-skill-diff.txt`: 9 `-` lines and 9 `+` lines in two hunks —
`@@ -83,14 +83,14 @@` (Gates-table rows L86–L93) and `@@ -778,7 +778,7 @@` (Selftest host note L781). Historical lines
186, 188 and 640 are not in the diff.

Command (cwd = `$S/after`), transcript = the (a) selftest receipt:

```sh
TMPDIR=$S/tmp/c python3 -B corpus/evidence/round90/skill-tally-r90.py --root . --selftest $S/receipts/c3-a-selftest.txt
```

Observed line (receipt `c3-b-tally-after.txt`, exit in `c3-b-tally-after.exit`):

```
TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 SKILL_TALLY_R90=PASS
```

Exit: **0**. This is the frozen C3 predicate field-for-field.

Control: the same transcript against the pristine `$S/tree` (receipt `c3-b-tally-before-selftest.txt`, exit in
`c3-b-tally-before-selftest.exit`) prints the (a) body with `STALE_TALLIES=9/9` and exit 1; its sha256 equals
`c3-a-tally.txt` (`4ea06681…a6d3`), so the sole cause of the flip is the nine cells — the transcript is not doing
the work.

## (c) Sweep of `PASS (<n> cases` — line list

Binding regex (the counter's `TALLY_RE`, requires a skip count): `PASS (\d+) cases, (\d+) skipped`.

| line | tally (cases/skipped) | class | why |
|---|---|---|---|
| 86 | 275 / 0 | current | Gates row, first cell `research-gate` |
| 87 | 275 / 0 | current | Gates row, first cell `research-gate verify-claims` |
| 88 | 275 / 0 | current | Gates row, first cell `research-gate verify-chain` |
| 89 | 275 / 0 | current | Gates row, first cell `research-gate verify-sweeps` |
| 90 | 275 / 0 | current | Gates row, first cell `research-gate verify-integrity` |
| 91 | 275 / 0 | current | Gates row, first cell `research-gate verify-all` |
| 92 | 275 / 0 | current | Gates row, first cell `research-gate verify-metadata` |
| 93 | 275 / 0 | current | Gates row, first cell `research-gate --pin / --drift` |
| 781 | 275 / 0 | current | host note `Selftest \`PASS (275 cases, 0 skipped)\` on this host` |
| 186 | 256 / 0 | historical | inside "Historical — Round-25 final registry correction" (round-34 quote) |
| 188 | 161 / 0 | historical | round-25 final shared selftest |
| 640 | 215 / 0 | historical | round-27 section (`original187`/legacy161 paragraph) |

Counts: **current = 9, historical = 3**, total binding occurrences = 12 (receipt `c3-c-sweep.txt`).

The broader literal `PASS (<n> cases` pattern also matches twelve single-number occurrences that carry no skip count
and are outside the counter's regex: L160 `PASS (3 cases)`, L161 `PASS (10 cases)`, L186 ×3 (`228`, `241`, `251`),
L250 (`30`), L273 (`44`), L309 (`40`), L346 (`54`), L393 (`64`), L437 (`74`), L489 (`85`). They are historical
prose, not current cells, and are not counted by `OTHER_OCCURRENCES` (which counts binding-regex matches only); the
counter cannot parse them by construction.

## Observations (no predicate deviation)

**O1 — round labels in the frozen prose are loose.** `claims.md` / `claims.json` call the three unbound occurrences
"round-25/32/34/37 quotes". The three the counter actually sees are L186 (256, a round-34 quote inside the
round-25 historical paragraph), L188 (161, round-25 final), and L640 (215, round-27). No round-37 two-number quote
exists in `SKILL.md` at this revision. The operative value `OTHER_OCCURRENCES=3` is exactly right; only the round
labels in the prose are loose. This sits inside named limit 2 (historical recognition is shallower than the binding
rule) and moves no predicate; recorded so the landing note does not claim a round-37 binding.

**O2 — the case-range note is unbound.** `SKILL.md` L86 still carries the prose "r39 bash-pin cases 273–275". The
discrimination edit (only the nine cells, per the seat) leaves it unchanged and the check still passes — named
limit 1 says the check does not verify which cases 276–283 are. The landing repair may update that note (C3 K3
permits "the one case-range note"); the counter does not bind it, so either choice keeps (b)'s PASS.

**O3 — the staleness is inherited.** `git diff f54a45ed… 9bad1201… -- SKILL.md` is empty: the 275 tallies predate
the freeze commit; the landing repair is the first `SKILL.md` move after `9bad120`.

## Risks / limits of this evidence

- The landing-revision PASS itself is not observable here (the repair lands after the wave). (b) projects it on a
  scratch copy whose `SKILL.md` differs from the tree only in the nine cells; if the landing also edits the
  case-range note (O2), the two-number cells bind exactly as in (b).
- The check binds two numbers per current cell, not the cell prose or the case-range note (named limit 1). Any cell
  rewritten to a number equal to the tool's live output passes.
- The selftest verdict is a single-tool run; two runs were performed here ((a) self-run, (b) captured transcript)
  and the (a) self-run body is byte-identical to the committed before-receipt, so the expected 283 is stable
  across this host's two observations.

## Receipts (copied into `w1/R90ExecC3Tally/`)

| file | what it records | exit |
|---|---|---|
| `c3-a-tally.txt` / `c3-a-tally.exit` | (a) self-run counter on the tree | 1 |
| `c3-a-selftest.txt` / `c3-a-selftest.exit` | captured `research-gate.sh --selftest` transcript (285 lines, verdict line 285) | 0 |
| `c3-b-tally-after.txt` / `c3-b-tally-after.exit` | (b) counter on the nine-cell copy with `--selftest` | 0 |
| `c3-b-tally-before-selftest.txt` / `c3-b-tally-before-selftest.exit` | control: same transcript on the pristine tree | 1 |
| `c3-b-skill-diff.txt` | `diff -u tree/SKILL.md after/SKILL.md` (9−/9+, two hunks) | — |
| `c3-c-sweep.txt` | (c) broad + binding sweep with line numbers and classes | — |

Commands not run: no C1 or C2 command was executed; no network fetch was made; no tool was installed or upgraded
this seat.

VERDICT: R90ExecC3Tally C3 held — the frozen before-state reproduces byte-identically (STALE_TALLIES=9/9, exit 1) and the nine-cell discrimination copy yields STALE_TALLIES=0/9, SKILL_TALLY_R90=PASS, exit 0, matching the frozen field set; the landing-revision PASS is projected, not observed, because the repair lands after the wave.
