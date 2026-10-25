# Attack29 — Round-47 C2 SCORECARD numerics

## Verdict

**The committed correction is accurate.** At the committed round-47 tip, the named final C2 counter measures `94/94`; the freeze-time counter's committed after-measurement is `93/93`. The purported `92/92` is not a measured after-state: `92` is the frozen floor. No numeric correction remains actionable in `SCORECARD.md:2506` at tip `900c72e` / current observed lane history.

## Evidence and commands

- Read `corpus/evidence/round47/measure-after.txt:16-37`. It records the final counter as `ENTRY_POINTS=94 (abc=85 dependence=+2 check_named=+7)`, `FLOOR=92`, `REGISTERED=94/94`, zero unregistered/dangling/mismatches, `C2=PASS`, exit 0. It separately records the freeze-time counter as `ENTRY_POINTS=93 (abc=85 dependence=+1 check_named=+7)`, `FLOOR=92`, `REGISTERED=93/93`, zero mismatches, `C2=PASS`, exit 0.
- Replayed final measure from committed archive: `git archive 900c72e | tar -x -C /tmp/chousa-r48-attack29/final`, then `python3 corpus/evidence/round47/c2-count.py --list`. Observed `ENTRY_POINTS=94 (abc=85 dependence=+2 check_named=+7)`, `FLOOR=92`, `GATES_ROWS=51`, `REGISTERED=94/94`, `UNREGISTERED=0`, `DANGLING=0`, `MISMATCHES=0`, `C2=PASS` (exit 0). Removed scratch after replay.
- `git ls-tree -r --name-only 900c72e -- corpus/evidence/round47/measure-after.txt` returned the path, confirming the receipt is committed. `git log --follow -- corpus/evidence/round47/measure-after.txt` showed commits `900c72e` and `11ead57`.
- `SCORECARD.md:2506` now names final `94/94` and freeze-counter `93/93`; `corpus/lessons/round-47.md:137-140` records the earlier erroneous `93/93` final slot and `92/92` freeze slot as recordkeeping mistakes corrected in the final commit.

## Interpretation / residual risk

- Slot assignment matters: the frozen counter's output is not the after-state for the command named in the SCORECARD row. `94/94` is the final counter's output; `93/93` is the freeze-time counter's output.
- `FLOOR=92` in `measure-after.txt:18,30` and in the counter source (`corpus/evidence/round47/c2-count.py:26-27,53`) is a threshold, not a registered/entry-point ratio. The frozen predicate requires `ENTRY_POINTS >= FLOOR`; it does not claim `92/92`.
- Historical `92/92` does exist in `.ufo/waves/round-47/w1/SentScopeAudit.md:42-47`, but it is the forged-pyc adversarial payload's attacker-controlled output (`abc=92 dependence=+0 check_named=+0`), not a committed measurement. That report explicitly says attacker code ran under the source pin; its mitigation outputs fail. Thus it cannot support the frozen counter's result.
- The archived measure itself supplies the freeze counter result. This audit replayed the final counter but did not independently execute the historical freeze-counter blob; the committed receipt and round-47 verifier spot-check (`corpus/lessons/round-47-verifier-spotcheck.md:23-27`) independently record that 93/93 result. No remaining scorecard numeric defect found in scope.

## Verification gaps

No build/test run. The only executed measurement was the final C2 counter on a `git archive` of `900c72e`; no live fetch, installs, or writes outside this report.