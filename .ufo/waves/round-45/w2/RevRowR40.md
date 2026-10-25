# RevRowR40 — round-40 Gates row

## Verdict: fails (row not honest about archived-tip observations)

Target: `SKILL.md:104` at `5e8c7ad2f7b8254d83358820286e3d12ca4672d1`.

| Cell | Row text / observed result | Verdict |
|---|---|---|
| name | `research-gate round-40 counters` | holds |
| kind | `gate` | holds |
| entry | `python3 corpus/evidence/round40/c1-count.py` · `python3 corpus/evidence/round40/c2-count.py` (lane root) | holds; both commands executed from the extracted archive root. |
| verdict map | C1 `R39_ACTIVE_RECEIPTS=6/6` · C2 `R39_CALIBRATION_DISPOSITIONS=4/4` exit `0`; other count exit `1`; malformed manifest/evaluation error exit `2` | C1 target behavior is the counter's described pass contract, not reached in this run. C2 did not reach the specified verdict output: it emitted `R39_CORRECTION_COUNTER_ERROR=[Errno 2] No such file or directory: '/tmp/chousa-r45-RevRowR40/.ufo/reports/round-39/chousa.md'`, exit 2. Archive-only execution therefore hits an environment dependency. |
| self-test | `do-nothing controls: C1 ...=3/6, exit 1; C2 ...=0/4, exit 1` | holds as stated historical controls in frozen claims (`corpus/evidence/round40/claims.md:15,29`), but not rerun: the entry cell does not name control commands. |
| pinned values | `frozen corpus/evidence/round40/claims.md; measured commit d164f88eb71a6c48a66ae1e7abfcb5fef82219d9; C1 current worktree run here: 2/6, exit 1 (gate SHA mismatches; see R40-W2)` | partially wrong. Claims file exists in archive. The full measured-commit string is not a path and is not the archived tip. At archive tip C1 printed `R39_ACTIVE_RECEIPTS=2/6`, exit 1, with per-receipt output including `VERIFY-FAIL: gate-sha256-mismatch`, so the C1 observation is correct and consistent with the gate-SHA explanation. The claimed R40-W2 report is not present at that path in the archived tree (the round-40 directory has no `R40-W2.md`); thus that pointer does not resolve. |
| write scope | `read-only` | holds |
| owner | `chousa` | holds |

The row has exactly **8 cells**.

## Verbatim commands and decisive output

```text
mkdir -p /tmp/chousa-r45-RevRowR40/tree && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 5e8c7ad2f7b8254d83358820286e3d12ca4672d1 | tar -x -C /tmp/chousa-r45-RevRowR40/tree
cd /tmp/chousa-r45-RevRowR40/tree && python3 corpus/evidence/round40/c1-count.py; r=$?; printf 'C1_RC=%s\n' "$r"; python3 corpus/evidence/round40/c2-count.py; r=$?; printf 'C2_RC=%s\n' "$r"
```

```text
corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json: ok VERIFY: ok receipt=c1-base-s39001-regenerated.json gate=base-gate-r39.sh counter=c1-count.py
corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json: ok VERIFY: ok receipt=c1-mutenv-s39013-regenerated.json gate=mut-gate-path-env.sh counter=c1-count.py
corpus/evidence/round39/receipts/c1-after-s39111.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c2-after-s39101.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c2-after-s39121.json: fail VERIFY-FAIL: gate-sha256-mismatch
R39_ACTIVE_RECEIPTS=2/6
C1_RC=1
R39_CORRECTION_COUNTER_ERROR=[Errno 2] No such file or directory: '/tmp/chousa-r45-RevRowR40/.ufo/reports/round-39/chousa.md'
C2_RC=2
```

```text
python3 -c 'r=[x for x in open("SKILL.md") if "research-gate round-40 counters" in x][0]; print("CELLS",len(r.rstrip("\n").split("|"))-2); print("ROW",r.rstrip())'
CELLS 8
```

Pinned path checks (exit status then path):

```text
0 corpus/evidence/round40/claims.md
1 d164f88eb71a6c48a66ae1e7abfcb5fef82219d9
0 corpus/evidence/round40/receipts/
0 .ufo/waves/round-40/
```

The row's `R40-W2` filename was directly checked and absent; the committed archive's round-40 report listing contains `w1/` material and controls, not that filename. The counter sources identify the missing C2 input as `FLEET / '.ufo/reports/round-39/chousa.md'` (`corpus/evidence/round40/c2-count.py:9-15`); in this archive-only run that external fleet report was unavailable. No files outside this report were changed; scratch tree removed. No tools installed.
