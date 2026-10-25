# ScribeGateR40 — round-40 Gates row draft

## Assignment
Draft one `SKILL.md` Gates table row for round 40's c1/c2 counter entry points, using their docstrings/behavior, frozen claims, scorecard verdict, log, lesson, and existing row convention. Run each counter once from the lane root, without write options. Do not edit `SKILL.md` or product/evidence files.

## Commands and observed outputs
Commands ran from `/home/vgpnk/Projects/shokunin/chousa-shokunin`:

`python3 corpus/evidence/round40/c1-count.py; echo "EXIT=$?"`

```text
corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json: ok VERIFY: ok receipt=c1-base-s39001-regenerated.json gate=base-gate-r39.sh counter=c1-count.py
corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json: ok VERIFY: ok receipt=c1-mutenv-s39013-regenerated.json gate=mut-gate-path-env.sh counter=c1-count.py
corpus/evidence/round39/receipts/c1-after-s39111.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c2-after-s39101.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c2-after-s39121.json: fail VERIFY-FAIL: gate-sha256-mismatch
R39_ACTIVE_RECEIPTS=2/6
EXIT=1
```

`python3 corpus/evidence/round40/c2-count.py; echo "EXIT=$?"`

```text
R2_DISPOSITION=ok
R3_DISPOSITION=ok
R4_DISPOSITION=ok
R5_DISPOSITION=ok
R39_CALIBRATION_DISPOSITIONS=4/4
EXIT=0
```

No options were passed. These were read-only invocations. C1's observed result differs from the committed round-40 expected measurement; this is a worktree-vs-commit measurement-target mismatch, explicitly surfaced by the round-40 routed finding and not a falsification of the frozen C1 claim.

## Evidence and verdict
- `corpus/evidence/round40/c1-count.py:1-13,28-40`: docstring and fixed active receipt manifest; no argparse or options; prints per-receipt status and `R39_ACTIVE_RECEIPTS=...`; exits 0 iff 6/6, else 1, malformed/unexpected manifest exits 2.
- `corpus/evidence/round40/c2-count.py:1-23,48-94`: docstring and fixed evidence inputs; no argparse or options; prints R2-R5 dispositions and `R39_CALIBRATION_DISPOSITIONS=...`; exits 0 iff 4/4, else 1, evaluation errors exit 2.
- `corpus/evidence/round40/claims.md:11-15,25-31`: frozen PASS values are `R39_ACTIVE_RECEIPTS=6/6` and `R39_CALIBRATION_DISPOSITIONS=4/4`; controls are 3/6 and 0/4, each exit 1.
- `SCORECARD.md:2262-2273`: both predicates measured at commit `d164f88eb71a6c48a66ae1e7abfcb5fef82219d9`, with improved verdicts; C1 3/6→6/6, C2 0/4→4/4.
- `LOG.md:1475-1478` records the same committed measurements and notes R40-W2: current HEAD gives 6/6 but a worktree with r41 in-flight edits gives 2/6, a measurement-target defect, not r40 falsification.
- `corpus/lessons/round-40.md:9-10` records controls, commit, and expected PASS results; its later sections describe the staged round 40 knowledge/gate work.
- Existing `SKILL.md` Gates header is at lines 75-78; `research-gate round-37 counters` row at line 95 establishes counter row conventions. No superseding round-40 `-v2`/`-v3` counter is identified in the cited round evidence; these are the listed entry points.

## Draft row (verbatim)
```text
| research-gate round-40 counters | gate | `python3 corpus/evidence/round40/c1-count.py` · `python3 corpus/evidence/round40/c2-count.py` (lane root) | C1 `R39_ACTIVE_RECEIPTS=6/6` · C2 `R39_CALIBRATION_DISPOSITIONS=4/4` exit `0`; any other count exit `1`; malformed manifest / evaluation error exit `2` | do-nothing controls: C1 `R39_ACTIVE_RECEIPTS=3/6`, exit 1; C2 `R39_CALIBRATION_DISPOSITIONS=0/4`, exit 1 | frozen `corpus/evidence/round40/claims.md`; measured commit `d164f88eb71a6c48a66ae1e7abfcb5fef82219d9`; C1 current worktree run here: `2/6`, exit 1 (gate SHA mismatches; see R40-W2) | read-only | chousa |
```

## Provenance and limits
- Lane HEAD observed: `d82cec904bf0fb8736886b9f17be913c7807427a` (`git rev-parse HEAD`). Existing unrelated/in-flight working-tree changes were observed and left untouched: round-40 and round-41 swarm registries modified, round-41 cells receipt deleted, and round-45 wave files untracked.
- The row is a draft only; no lane production file was changed. Report file is the sole write.
- No installs or updates.
- The C1 recorded measurement is specifically of this checkout's current state; the committed measurement cited by SCORECARD/LOG and lesson is `6/6`, exit 0. This report does not claim to have reproduced that committed-tree result. C2 current invocation did reproduce `4/4`, exit 0.
