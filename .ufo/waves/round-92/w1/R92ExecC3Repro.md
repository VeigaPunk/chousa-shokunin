# R92ExecC3Repro — frozen C3 reproduction (carrier C5)

Seat: R92ExecC3Repro. Tree: clone --shared of /home/vgpnk/Projects/shokunin/chousa-shokunin
at 16ccf7693c61b8ffe392fc757352304f239bfcad (carrier C5), scratch
/fast/scratch/hyaku/chousa-r92/R92ExecC3Repro. No network, no tool installs (RULES.md read;
nothing needed beyond python3/bash/git). No edits outside scratch + this report.

## (a) skill-tally-r92 on carrier tree

Command (cwd $S/repo): `python3 -B corpus/evidence/round92/skill-tally-r92.py --root . --selftest corpus/evidence/round92/controls/selftest-r92.txt`
Receipt: receipts-R92ExecC3Repro/a-skill-tally-carrier.txt (copied from $S/run-a.txt)
Output (exit 0):
```
TALLY_ROWS=8 STALE_TALLIES=0/8 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=2 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 OTHERS_OK=1 LEGS=3/3
SKILL_TALLY_R92=PASS
```
Matches frozen predicate exactly, including CASE_RANGE_BASHENV=273-275 and
CASE_RANGE_BASH_PIN=282-283 (case names derive from the tool's ok-case names, not prose
bounds) and OTHER_OCCURRENCES=2.

## (b) skill-tally-r92-controls on carrier tree

Command (cwd $S/repo): `python3 -B corpus/evidence/round92/skill-tally-r92-controls.py --root . --work $S/ctl`
Receipt: receipts-R92ExecC3Repro/b-controls-carrier.txt (copied from $S/run-b.txt)
Output (exit 0):
```
OK old-prose-carried: r91 SKILL_TALLY_R91=FAIL, r92 SKILL_TALLY_R92=FAIL
OK stale-tally: r91 SKILL_TALLY_R91=FAIL (rc=1), r92 SKILL_TALLY_R92=FAIL (rc=1)
OK deleted-other: r91 SKILL_TALLY_R91=PASS (rc=0), r92 SKILL_TALLY_R92=FAIL (rc=1)
CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1
```
Matches frozen predicate exactly. The deleted-other leg is the C3 discrimination: r91
(document-wide, unpinned) passes, r92 (## Gates-scoped, pinned multiset) fails.

## (c) hand re-derivation of scoped others multiset

`grep -n '^## ' SKILL.md` on the carrier tree: `## Gates` at line 82, next `## ` at
line 576 (`## Round26 metadata options and resource qualification`). Section = lines
82–575 (494 lines). Regex `PASS \((\d+) cases, (\d+) skipped\)` over that section yields:
8× current (283,0) at lines 86–93, plus
two non-current occurrences: line 186 `(256,0)` and line 188 `(161,0)`. Others multiset
{(161,0):1, (256,0):1}, sorted [(161,0),(256,0)], count 2 — exactly the frozen pinned
multiset. Doc-wide grep shows the third historical tally `PASS (215 cases, 0 skipped)` at
line 640 (after `## Round26`), deliberately out of scope — confirming the named limit,
not a silent unbind. `PASS (228/241/251 cases)` strings at line 186 lack `, 0 skipped`
and are not counted as occurrences by the frozen regex.

## (d) counter against the committed tree

Command: `python3 -B corpus/evidence/round92/skill-tally-r92.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --selftest corpus/evidence/round92/controls/selftest-r92.txt` (run from the clone; --root/committed tree)
Receipt: receipts-R92ExecC3Repro/d-skill-tally-committed-tree.txt
Same verdict line: `SKILL_TALLY_R92=PASS` with identical counters, exit 0.
Boundaries on the committed tree confirmed by grep: `## Gates` at line 82, next `## ` at
line 576 — same as carrier.

## Findings

None. All four sub-checks reproduce the frozen C3 predicate on C5 and on the committed
tree. No deviation from an expected value was observed; no unrequested network access;
no files written outside scratch + this wave output folder; scratch removal is done by
the yield-time cleanup `rm -rf -- "$S"` equivalent below.

## Tools

None installed/updated. RULES.md read; pacing guard honored — no pacman, no sudo.

VERDICT: R92ExecC3Repro C3 held — frozen C3 reproduces on carrier C5 and committed tree with exact counters.
