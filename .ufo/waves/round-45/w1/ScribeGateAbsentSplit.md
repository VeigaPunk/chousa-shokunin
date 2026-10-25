# ScribeGateAbsentSplit — round 43 Gates row

## Assignment and verdict

Drafted one proposed Gates row for the round-43 `tools/absent-split.py` gate. It is **not inserted** into `SKILL.md`: this seat may write only this report. Axes: operability (C1), calibration (C2), depth (C3). The round-43 targets are supported by one observed default tool run and fresh read-only runs of all three round-43 counters. No files other than this report were written by this seat.

Proposed row (verbatim):

```text
| `absent-split` (round 43) | tool | `python3 tools/absent-split.py` · `python3 corpus/evidence/round43/c1-count.py` · `python3 corpus/evidence/round43/c2-count.py` · `python3 corpus/evidence/round43/c3-count.py` | tool exit `0` with both classes nonempty and all absent rows classified; `1` missing row/empty class/uncomputable ratio; `2` usage/env. C1 exit `0`: `ABSENT_ENUMERATED=15/15 CLASSED=15/15 BOTH_NONEMPTY=1/1 REPRODUCIBLE=1/1 MUTANT_DETECTED=1/1 C1=PASS`; exit `1` any count miss; `2` usage/env. C2 exit `0`: `SPLIT_AGREES=15/15 VOCAB_OK=15/15 C2=PASS`; exit `1` miss; `2` usage/env. C3 exit `0`: `ENTRY_CITES=1/1 QUOTE_LOCATED=1/1 URL_MATCH=1/1 C3=PASS`; exit `1` miss; `2` usage/env | flipped-row C2 control `--flip S086` → `SPLIT_AGREES=14/15`, exit 1; C1 missing-tool control and C3 missing-entry control also exit 1 (`corpus/evidence/round43/controls/c1-control-before.txt`, `c3-control-before.txt`) | measured lane HEAD `d82cec904bf0fb8736886b9f17be913c7807427a`; claims frozen base `15f9f3fbd3c17b2155f718c67cbef0624034cf6d` | read-only | chousa |
```

## Provenance and observations

- Lane HEAD command: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD` → `d82cec904bf0fb8736886b9f17be913c7807427a`.
- Tool source read: `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/absent-split.py:1-145`. It documents default invocation `python3 tools/absent-split.py`, TSV output, no network/write behavior, and exit 0/1/2 meanings; argparse defaults are table, register, and cache constants. Its exact observed exit and output:

```text
S080\tnot-carried\t19\t50\t0.380000\t1
S082\tnot-carried\t18\t43\t0.418605\t1
S084\tmisquote\t48\t90\t0.533333\t2
S086\tnot-carried\t4\t46\t0.086957\t2
S088\tnot-carried\t26\t94\t0.276596\t1
S093\tmisquote\t79\t120\t0.658333\t1
S094\tmisquote\t63\t86\t0.732558\t3
S104\tnot-carried\t25\t88\t0.284091\t1
S105\tmisquote\t17\t24\t0.708333\t3
S108\tmisquote\t69\t108\t0.638889\t1
S110\tmisquote\t72\t119\t0.605042\t3
S111\tmisquote\t10\t19\t0.526316\t1
S112\tmisquote\t40\t71\t0.563380\t3
S114\tnot-carried\t7\t32\t0.218750\t2
S116\tmisquote\t34\t36\t0.944444\t3
EXIT_CODE=0
```

  The literal command was run from lane root: `python3 tools/absent-split.py; rc=$?; printf 'EXIT_CODE=%s\\n' "$rc"; exit 0`. The `EXIT_CODE` line reports the tool's saved status; the shell wrapper exits 0 to preserve output.
- Claims read: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/claims.md:28-96`. It freezes C1/C2/C3 targets; C2 flipped-row control is S086. No round-43 `SCORECARD.md` was found by the scoped evidence glob; therefore the verdict map uses frozen claims, not an unobserved scorecard.
- Lessons read: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-43.md:7-18,29-49`. It records the target values and control facts.
- Gates conventions read: `/home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md:75-99`, including the header, 8-column row format, and `research-gate round-37 counters` conventions. Existing entries demonstrate gate counter exit mappings.
- Counter sources read: `corpus/evidence/round43/c1-count.py:1-103`, `c2-count.py:1-141`, `c3-count.py:1-72`. Each docstring documents exit 0/1/2. No round-43 counter supersession was found in the table excerpt; listed counters are the round's C1/C2/C3.

Each counter was run exactly once from `/home/vgpnk/Projects/shokunin/chousa-shokunin` without receipt-writing options:

```text
$ python3 corpus/evidence/round43/c1-count.py
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED PASS 15/15
CLASSED PASS 15/15
BOTH_NONEMPTY PASS misquote=9 not-carried=6
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=14 expected=15
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=PASS
EXIT_CODE=0

$ python3 corpus/evidence/round43/c2-count.py
SPLIT_AGREES=15/15
VOCAB_OK=15/15
MISMATCHES=0
C2=PASS
EXIT_CODE=0

$ python3 corpus/evidence/round43/c3-count.py
ENTRY_CITES=1/1
QUOTE_LOCATED=1/1
URL_MATCH=1/1
C3=PASS
EXIT_CODE=0
```

The command wrapper for each saves the counter's exit status before printing `EXIT_CODE`, then exits 0 itself; the reported status is the saved counter status.

## Gates and scope

- C1 control receipt read at `corpus/evidence/round43/controls/c1-control-before.txt`: `TABLE_ABSENT PASS 15/15`, `TOOL_PRESENT FAIL missing /tmp/no-such-absent-split.py`, `C1=FAIL` (counter implementation returns 1 for missing tool). C3 control at `controls/c3-control-before.txt`: all three counts 0/1 and `C3=FAIL entry-missing` (counter returns 1). C2 control at `controls/c2-control-before.txt`: `SPLIT_AGREES=14/15`, `VOCAB_OK=15/15`, `MISMATCHES=1`, S086 mismatch, `C2=FAIL`; claims specify it exits 1.
- The proposed row is eight cells and uses only repo-relative entry paths. The entry points are exactly the tool and three round-43 counters. `read-only` is supported by absent-split's documented contract; counters were run without write-receipt options.
- No live target was fetched, no tool installed, no production file/index/jj state modified. The default command and counters were invoked read-only. The report is the sole write.

## Commands / file-surface summary

Reads: skill instructions; `SKILL.md` Gates section; absent-split source; round-43 lesson, claims, three counter sources, three control files; three round-43 receipt files; round-45 claims (context); `quarantine-check.py` write-pattern search; evidence globs for round-43 files and `SCORECARD.md`; git HEAD/log metadata. Executions: the default absent-split invocation once; each of c1/c2/c3 once. No install or network command.
