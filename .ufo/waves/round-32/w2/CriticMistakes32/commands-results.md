# CriticMistakes32 — observed command/output record

All commands below were executed in `/home/vgpnk/Projects/shokunin/chousa-shokunin`; receipt basenames are under `.ufo/waves/round-32/w2/CriticMistakes32/`. These are controls unless the name starts `candidate`. No controls are candidates.

## C2 duplicate-control, v2

```sh
timeout --kill-after=5s 300s prlimit --nproc=8000 --fsize=1048576 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/tmp C2_TMP=/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/tmp TMPDIR=/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/tmp python3 corpus/evidence/round32/c2-count-v2.py --gate /fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/duplicate-only/tools/research-gate.sh --seed 323201 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w2/CriticMistakes32/control-duplicate-c2-v2-s323201.json
```

Exit 1; `EXEMPT_AUDIT_MATCH=96/132`, `RECORD_CHECKS=ok`; R1/R2/R3 each 0/12, all other classes full.

## C2 duplicate-control, v1

```sh
timeout --kill-after=5s 300s prlimit --nproc=8000 --fsize=1048576 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/tmp C2_TMP=/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/tmp TMPDIR=/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/tmp python3 corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/duplicate-only/tools/research-gate.sh --seed 323201 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w2/CriticMistakes32/control-duplicate-c2-v1-s323201.json
```

Exit 0; `EXEMPT_AUDIT_MATCH=120/120`; every class full.

## C2 landed gate, v2 (valid layout)

```sh
timeout --kill-after=5s 300s prlimit --nproc=8000 --fsize=1048576 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/tmp C2_TMP=/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/tmp TMPDIR=/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/tmp python3 corpus/evidence/round32/c2-count-v2.py --gate /fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/lane/tools/research-gate.sh --seed 323202 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w2/CriticMistakes32/candidate-c2-v2-s323202.json
```

Exit 0; `EXEMPT_AUDIT_MATCH=132/132`, `RECORD_CHECKS=ok`; every class full.

## C2 no-verdict control, v1

```sh
timeout --kill-after=5s 300s prlimit --nproc=8000 --fsize=1048576 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/tmp C2_TMP=/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/tmp TMPDIR=/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/tmp python3 corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/no-verdict/tools/research-gate.sh --seed 323204 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w2/CriticMistakes32/control-no-verdict-c2-v1-s323204.json
```

Exit 0; `EXEMPT_AUDIT_MATCH=120/120`; every class full.

## C2 no-verdict control, v2

```sh
timeout --kill-after=5s 300s prlimit --nproc=8000 --fsize=1048576 -- env C1_TMP=/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/tmp C2_TMP=/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/tmp TMPDIR=/fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/tmp python3 corpus/evidence/round32/c2-count-v2.py --gate /fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/no-verdict/tools/research-gate.sh --seed 323204 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w2/CriticMistakes32/control-no-verdict-c2-v2-s323204.json
```

Exit 1; `EXEMPT_AUDIT_MATCH=0/132`, `RECORD_CHECKS=fail:drift-summary-lines=0`. Gate rc remains 1. This wrapper strips only `RESEARCH_GATE:` lines from the landed scratch gate's output; its source is `control-no-verdict-gate.sh` in this directory.

## C1 and layout exact argv logs

Executed `timeout --kill-after=5s 870s python3 /fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/run-checks.py c1` through a foreground Python subprocess, outer exit 0. The driver ran at most two counters concurrently. Each child had `timeout --kill-after=5s 840s prlimit --nproc=8000 --fsize=1048576 --` before the committed counter. Exact child argv, cwd, temp environment, exit and output are in:

- `control-probeonly-c1-v2-s323211.log.json`: exit 1, `APPEND_SERIALIZED=0/24`.
- `candidate-c1-v2-s323212.log.json`: exit 0, `APPEND_SERIALIZED=24/24`.

Executed the same outer command with final argument `c1-v1`, outer exit 0:

- `control-probeonly-c1-v1-s323211.log.json`: exit 1, `APPEND_SERIALIZED=23/24`; F 11/12, L 12/12. This seed did not reproduce the historical 24/24 v1 control result; it is fully disclosed, not a candidate miss.

Executed `timeout --kill-after=5s 320s prlimit --fsize=1048576 -- python3 /fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/run-checks.py layout`, outer exit 0:

- `candidate-c2-v2-layout-refusal-s323203.log.json`: child exit 2, no count and no receipt created, because C2_TMP was deliberately the scratch lane root. The exact error says the fixture lies inside the gate's lane root. This is an intentionally invalid harness-layout check, not a below-target P2 receipt.

## R1 focused check

Executed `timeout 30 python3 /fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/r1-check.py` once from each `before` and `after` scratch directory: exit 1 in both, identical FAIL output. Also executed `timeout --kill-after=5s 40s prlimit --fsize=1048576 -- python3 /fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/run-checks.py r1`, outer exit 0, repeating each run to retain exact argv/output as `r1-before.log.json` and `r1-after.log.json`. Thus four R1 invocations total, all exit 1; these are not C1/C2 counter runs. The script is the logic of `w1/ScribeQualityR1/quality.md:11`, with the imports separated onto lines.

## Identity commands

`timeout 10 sha256sum /fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/probe-only/tools/research-gate.sh` → `034f786be1570136b27d72ec630e24be1c6a673ce53434d476af94f4bb5f0340`, exit 0. Reconstructed solely from the base bytes plus `w1/CtlC1PartialLockB/b-probe-only.patch`; those bytes were then scored as a control.

`timeout 20 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git show 5d8a170795dcf48c3746a4f03dee9cfe32812834:.ufo/waves/round-32/controls/L1-design-v2/c1-probeonly-control-gate.sh | timeout 20 sha256sum` → `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`, exit 0.

`timeout 15 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git show 5d8a170795dcf48c3746a4f03dee9cfe32812834:corpus/lessons/round-31.md | timeout 15 sha256sum` and `timeout 10 sha256sum /fast/scratch/hyaku/chousa-r32/w2/CriticMistakes32/after/corpus/lessons/round-31.md` both → `a437466e7ec2135b9e19ae6b0e60de93d5e53a69f8c06c092a7d0676948628ac`, exit 0 each.

`timeout 20 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git show 4111607c:corpus/QUALITY.md` exited 0 and printed criteria 1–32, including 17, 19, 20, 24. The same revision's file was preserved unmodified as `quality-at-v1.md` via a selected-path `git archive`/`tar -x` into this seat's scratch directory and `cp`.

`timeout 10 pgrep -af '^.*(python3|strace|bash) .*/fast/scratch/hyaku/chousa-r32/w2/[C]riticMistakes32/.*$'` after the final experiment → exit 1, no output. All experiment subprocesses were awaited. No background jobs, installs or network reads.
