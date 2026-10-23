# Round 34 C1 partial-fix controls — bounded partial result

Access date: 2026-10-23. Axes: operability, detector sensitivity, line/boundary fidelity, isolation, reproducibility.

## Result

Three controls completed on both fresh seeds, `6241037426710223` and `6241037426710224`: **a MISSES 28/30; b MISSES 19/30; c MISSES 28/30**. No completed control meets 30/30. Control d was built and launched on both seeds, but neither run completed before the binding 40-minute seat stop: **d INCONCLUSIVE, not a measured MISSES or MEETS-TARGET**. The assignment's two completed scores for d are therefore missing.

The pristine base itself scores 19/30 on both seeds. Under the mutation-tester baseline rule, these are counter rejection results, **not formally killed mutants**: whole-predicate kill attribution is INCONCLUSIVE because the baseline already fails. No passing baseline or restored behavioral score is claimed.

## Inputs, commands and boundaries

Read `corpus/evidence/round34/claims.md` first, then the counter docstring and implementation. Frozen counter SHA-256 remained `5ef347874960b52561a1cfa517f3f3fc0d1763830e3580c44b993f8394c0a565`; base/production gate remained `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`. Initial and final `timeout 20s sha256sum` outputs matched these full values.

Let `S=/fast/scratch/hyaku/chousa-r34/w1/CtlC1PartialFix` and `A=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-34/w1/CtlC1PartialFix`. Every scored command used cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin` and this exact expansion template:

```sh
timeout 1800s bash "$S/run-counter.sh" "$S/<gate>.sh" <seed> "$A/<name>-s<seed>.json"
```

The preserved launcher `A/run-counter.sh` prints its PID, exports `C1_TMP=$S` and `TMPDIR=$S`, then execs:

```sh
prlimit --as=2147483648 --nproc=65536 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round34/c1-count.py --gate "$1" --seed "$2" --receipt "$3"
```

The counter itself gives the gate 1500 seconds (`c1-count.py:73,275-276`). At most four counter runs were live. No counter edits, candidate builds, network, installs, git/jj writes, production edits, or selftests. `timeout 20s df -h /fast` showed 88G available before copies. All artifacts are under A except restored experiment files and counter temp fixtures under S. `wc -c` measured the five archived gates at 356561–357537 bytes each, below 1 MiB.

Initial NPROC=2000 launches failed before a gate could start, exit 1 with `BlockingIOError: [Errno 11] Resource temporarily unavailable`; these produced no receipt and were inconclusive. Two bash-tool submissions hit its shared background-job cap. Commands/errors and recovery are recorded in `A/launch-errors.txt`. The successful runs below used NPROC=65536. Completed subprocess commands, PIDs, return codes and literal stdout are preserved in `A/background-first-results.json`, `A/foreground-first-results.json`, `A/first-binding-results.json`, and `A/remaining-results.json`.

## Mutations and identities

Each started as a separate scratch copy of the exact BASE gate. Only the named matcher/line-binding blocks changed. Literal shell matching uses a quoted span, advances one byte after an occurrence, and retains the existing boundary and newline-count helpers; it never places the span in an external argv.

| Control | Changed behavior; archived evidence | SHA-256 of archived control |
|---|---|---|
| a | Non-argv `tok_span_at` only; `tok_span_all` retains grep argv. `A/a-at-only.sh:1553-1604` | `48ebac6c0d26123391668893fbadd4f1a957a74f6313ea01e29745c38848aa97` |
| b | Non-argv `tok_span_all` only; entry search retains grep argv. `A/b-all-only.sh:1553-1606` | `f9b49f77bd750d395c1b6ca4f56535faeacdb81f8407df12ad02f569f1aef6b8` |
| c | Both matchers replaced; line-binding loop receives only `TOK_L1 TOK_L2` from the first occurrence. `A/c-first-only.sh:1553-1603,1807-1820` | `de7d5e687674d3e4ab5e4e9f4519140d244d9f2034c491e634ce4e99898ef59a` |
| d | Both matchers replaced; line-binding block removed, retaining `bound=1`. `A/d-ignore-line.sh:1553-1603,1802-1808` | `1326e457ff75eb2a9dd48958ccbb6e123d73aa42e0b765836d43b18b41599724` |

`timeout 20s sha256sum "$A/base.sh" "$A/a-at-only.sh" "$A/b-all-only.sh" "$A/c-first-only.sh" "$A/d-ignore-line.sh"` produced the listed identities; every completed receipt records its matching gate hash and the frozen counter hash (`:3-5`). Archived control gates intentionally remain mutated for audit; experiment working copies were restored.

## Actual detector output

Each cell below is the literal per-class count printed on **both** seeds. Completed counter exits were 1, gate exits 1, `gate_timed_out=false`, `predicate_holds=false` (each completed receipt `:8-15`). D has no per-class output and must not be substituted with its predicted count.

| Printed class | Pristine | a | b | c | d |
|---|---:|---:|---:|---:|---|
| LONGSPAN_MATCH | 19/30 | 28/30 | 19/30 | 28/30 | no score |
| long-verbatim-ml | 0/3 | 3/3 | 0/3 | 3/3 | no output |
| long-verbatim-1l | 0/2 | 2/2 | 0/2 | 2/2 | no output |
| long-edge | 0/2 | 2/2 | 0/2 | 2/2 | no output |
| long-mut-head | 2/2 | 2/2 | 2/2 | 2/2 | no output |
| long-mut-tail | 2/2 | 2/2 | 2/2 | 2/2 | no output |
| long-mut-mid | 3/3 | 3/3 | 3/3 | 3/3 | no output |
| long-split | 2/2 | 2/2 | 2/2 | 2/2 | no output |
| long-glued-left | 2/2 | 2/2 | 2/2 | 2/2 | no output |
| long-glued-right | 2/2 | 2/2 | 2/2 | 2/2 | no output |
| long-line-bound | 0/2 | 0/2 | 0/2 | 0/2 | no output |
| long-line-wrong | 0/2 | 2/2 | 0/2 | 2/2 | no output |
| short-verbatim | 3/3 | 3/3 | 3/3 | 3/3 | no output |
| short-mut | 3/3 | 3/3 | 3/3 | 3/3 | no output |

Receipts under A (all opened, both seeds):
- `pristine-s6241037426710223.json`, `pristine-s6241037426710224.json`: 19/30; 928.527 s / 941.644 s.
- `a-at-only-s6241037426710223.json`, `a-at-only-s6241037426710224.json`: 28/30; 753.428 s / 678.103 s.
- `b-all-only-s6241037426710223.json`, `b-all-only-s6241037426710224.json`: 19/30; 1171.021 s / 1154.713 s.
- `c-first-only-s6241037426710223.json`, `c-first-only-s6241037426710224.json`: 28/30; 941.033 s / 887.622 s.

Class evidence is at each receipt `:16-29`; misses and observed dispositions follow at `:31-98` (a/c end at `:45`).

### Which classes catch the controls

- **a:** `long-line-bound` catches both records: truth supported, observed mislocated. `tok_span_all` still hits E2BIG; the receipt stderr records four grep errors. `long-line-wrong` still scores 2/2 despite the broken enumeration because failure to enumerate happens to yield its expected mislocated verdict. Evidence: both a receipts `:11,22-23,31-43` (per-class order differs by seed).
- **b:** `long-verbatim-ml`, `long-verbatim-1l`, `long-edge`, `long-line-bound`, and `long-line-wrong` catch all 11 missed records; observed is unsupported throughout. The unfixed `tok_span_at` prevents the fixed all-occurrence matcher from being used. Evidence: both b receipts `:11,16-98`; base call order `tools/research-gate.sh:1806,1827`.
- **c:** `long-line-bound` catches both records, observed mislocated instead of supported. The second occurrence must be considered. Located quote, accessed 2026-10-23: “two delimited occurrences; \"line\" names the second” (`corpus/evidence/round34/c1-count.py:46`). Wrong-line records still score 2/2; both c receipts `:31-43` identify the misses, with empty stderr `:11`.
- **d:** **[INFERENCE]** `long-line-wrong` should catch its two falsely supported records, predicting 28/30; this was not observed. The expected class truth is specified at `c1-count.py:47,188-199`, while the control bypass is at `A/d-ignore-line.sh:1806-1808`.

## Stop, restoration and limits

The completed counter runs took 678–1171 seconds, rather than the planning context's 3–6 minutes. At `2026-10-23T11:39:55Z`, the binding seat timebox required stopping the remaining probes. Only recorded owned process groups were signalled SIGTERM:

- d seed 223: PGID 3617420, counter PID 3617457; exit -15, stdout only its RUN_PID line.
- d seed 224: PGID 4127398, counter PID 4127405; exit -15, stdout only its RUN_PID line.
- restored seed 223: PGID 1692407, counter PID 1692408; exit -15, stdout only its RUN_PID line.
- restored seed 224: PGID 1825587, counter PID 1825591; exit -15, stdout only its RUN_PID line.

Those four attempts produced no score or receipt. The same frozen behavioral detector was invoked on restored bytes, but its restoration runs are **inconclusive due to external interruption**. `A/process-cleanup.json` records exact groups/signals and `all_started_futures_done=true`; `A/remaining-results.json` preserves their actual commands and output. No counter runs were left active.

All four scratch working gates were restored by bounded `cp -- "$S/base.sh" "$S/<control>.sh"` after their runs stopped. Final bounded SHA-256 output for `S/base.sh`, all four working gates, and lane `tools/research-gate.sh` was identically:

```text
43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346
```

The final counter hash also matched its original frozen hash. Thus exact byte restoration is evidenced, while restoration behavior is not claimed. Remaining missing evidence is solely the completed d and restored behavioral runs; no 30/30 survivor or counter coverage escape was observed in the six completed mutant runs.
