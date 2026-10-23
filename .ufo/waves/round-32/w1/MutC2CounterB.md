# MutC2CounterB — C2 counter-of-counter

Axes: **operability** (reproducible, bounded detector and exact restoration) and **coverage** (matching guards and hidden truth). This is a CONTROL/mutation investigation, not a candidate implementation or a C2 admission judgment.

## Most important result: frozen-counter survivors

On **both seeds 320260230271 and 320260230283**, these deliberately wrong output controls printed `EXEMPT_AUDIT_MATCH=120/120` under the **unchanged frozen counter**, counter exit 0:

| Control | Actual wrong behavior | Gate exit | Verdict |
|---|---|---:|---|
| `duplicate-finding` | 72 CHAIN_EXEMPT_RESOLVABLE findings: two for each of 36 resolvable hops | 1 | **MEETS-TARGET; SURVIVED** |
| `no-verdict` | No RESEARCH_GATE verdict and no RESOLVED_HOPS summary | 1 | **MEETS-TARGET; SURVIVED** |
| `clean-exit` | Reports CLEAN and exits 0 despite 36 mismatch/resolvable hops and warn findings | 0 | **MEETS-TARGET; SURVIVED** |
| `stray-unknown` | Adds one FINDING naming a nonexistent hop, alongside the 36 expected findings | 1 | **MEETS-TARGET; SURVIVED** |

Why they pass, in `corpus/evidence/round32/c2-count.py`:
- **Multiplicity:** line 273 stores finding ids in a set; lines 284–286 compare sets. Two identical findings collapse to one. This directly misses the exactly-one finding requirement in `claims.md:63-65`.
- **Verdict/exit coherence:** line 269 accepts either exit 0 or 1. Lines 270–294 never examine the verdict/summary lines, so absent verdicts and CLEAN/exit-0 contradictions are invisible. A verdict-line guard does not exist to delete.
- **Unknown-hop stray finding:** line 273 records it, but lines 282–286 inspect only truth-map hop ids. There is no global stray-finding check. This is an output-hygiene coverage finding; the frozen per-hop predicate does not explicitly forbid findings about unknown ids.

Evidence: `MutC2CounterB/frozen-<control>-s<seed>.json`, matching `.output.json` files, `raw-observations.json`, and `raw-<control>-s<seed>.output.json`. The raw observations show respectively 72, 36, 36 and 37 finding lines, with 120 CHAIN lines in every case. All 14 classes match fully on each surviving trial: `class-matrix.tsv:14-21`.

**Limit:** these are intentionally white-box parser-isolation controls. They receive the frozen generator's truth through a scratch sidecar and do not read cited source files. Their scores demonstrate missing output checks, not a seed-independent implementation or a real candidate's behavior. No counter repair or contract change was made.

## Six one-point scratch-counter mutations

Following the L1 clarification, only isolated scratch **copies** were mutated; the committed counter was never edited. Each control is a copy of the BASE gate with a three-line interception after its shebang, delegating `verify-chain` to the fake-output emitter. No C2 reader implementation was built or scored here.

Detector assertion: **the deliberately wrong gate must be rejected** (`matched < 120`, counter exit 1, no timeout). The same counter invocation and rejection assertion were applied to pristine, one-guard-mutated, and exactly restored bytes. Thus a baseline counter exit 1 is the expected rejection, not a failed baseline. `summarize-evidence.py` applies the assertion to the preserved behavioral receipts; its executed output reports pristine PASS → mutant FAIL → restored PASS for all twelve seed/probe pairs.

Counts below are identical on both control seeds; every denominator is 120:

| Probe / wrong gate | Single counter change, original line | Pristine / frozen | Mutant-counter | Restored | Counter-mutant verdict |
|---|---|---:|---:|---:|---|
| `unique`: duplicate every CHAIN line | 277: replace `dup.add(m.group(1))` with `pass` | 0, MISSES | 120, MEETS-TARGET | 0, MISSES | KILLED |
| `observed`: wrong observed value on every hop, otherwise expected findings | 286: `ok = got == want` | 0, MISSES | 120, MEETS-TARGET | 0, MISSES | KILLED |
| `findings`: correct observations, omit all findings | 286: `ok = obs == t` | 84, MISSES | 120, MEETS-TARGET | 84, MISSES | KILLED |
| `stray-known`: add unexpected findings to every non-resolvable truth hop | 286: `ok = obs == t and (t != "resolvable" or got == want)` | 36, MISSES | 120, MEETS-TARGET | 36, MISSES | KILLED |
| `exit`: otherwise matching output, exit 2 | 269: `if not timed_out:` | 0, MISSES | 120, MEETS-TARGET | 0, MISSES | KILLED |
| `scrub`: matching output only when CHOUSA_MUTCOUNTER_ALLOW survives | 262: `env = os.environ.copy()` | 0, MISSES | 120, MEETS-TARGET | 0, MISSES | KILLED |

For `stray-known`, only the empty-finding-set requirement on non-resolvable hops is removed; the resolvable-hop finding requirement remains. Unknown-hop strays and verdict lines were tested separately above because their proposed guards are already absent.

Frozen, pristine and restored failing counter runs exit **1**; all mutant-counter runs exit **0**. Gate exit is 1 except the `exit` control, which exits 2. All recorded gate timeouts are false.

Per-trial, per-class output is preserved without narrowing: `MutC2CounterB/class-matrix.tsv` has all 14 class columns for every frozen/pristine/mutant/restored seed/control pair. Each corresponding `.output.json` contains the actual printed class lines and exact counter command; each receipt contains its misses. `mutation-verdicts.json` records the rejection assertion and KILLED verdict per seed. Receipts named `mutant-*` are **mutant-counter evidence, never frozen/design-v1 receipts**; see `receipt-classification.json`.

### Gate SHA-256 values

Full hashes are also in `hashes-mutated.json` and `hashes-restored.json`:

```text
unique             6596225e40c308b89d9058fd420b7bb0661f152d08f357491344fc15a5db8def
observed           1521524ace0ab017579715f4f21a430977b80e6d72c129bb2b5047cbd020f4a7
findings           7dee91472997d2c439d5f520fc481591301fc3a7f94f64fb6fd0ec121b4b6820
stray-known        9a4f6461b12ee4adb4d2b943061b276e91bdb65e8d7057eb620b7c3dc7b58751
exit               3e6c2a5a52c66f4e20cf81922542e4498a8c670adeba620ac7992a0e27df92f0
scrub              2303d3a7931ae6fa5a598b138863db79611949737f3b6b3d8f7d6d34c150ec75
stray-unknown      5b503e64c0afacf4b888fdd210eda1bb173fe04769ab4b49cd1a734c10991084
no-verdict         447f38015ca98796ec96ecaf95ec5daf82d8740f9ba13447773aff1b13d1ae7c
clean-exit         cf0bc25d17307973df1ddcb282281a8c42a7158ed2f5dd9c55e2f290ea0557d4
duplicate-finding  bc0381068b708a04dab0534215ee326746ad402add08977d9de4e06fa71412ed
```

Scratch controls: `/fast/scratch/hyaku/chousa-r32/w1/MutC2CounterB/control-<name>.sh`. Their shared emitter is `emit-control.py`, SHA-256 `c1cf944700fc7d17163224ea875fae86d68a32f9d7226848a792d83e3770b2a7`.

## Hidden-truth audit on two additional fresh seeds

**320260230317 and 320260230331** were not used in the guard probes. The frozen counter ran with `--keep` and the actual lane BASE gate on each: **84/120**, counter exit 1, R1–R3 0/36 and every other class full. Receipts: `keep-fresh-base-s<seed>.json` and `.output.json`.

For each kept fixture I preserved the original record and created `root/all-resolved.md`, rewriting all **120** hop statuses to `resolved`. I then ran the **actual BASE gate path**, not the relocated copy:

```text
bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify-chain /fast/scratch/hyaku/chousa-r32/w1/MutC2CounterB/kept-s<seed>/root/all-resolved.md --root /fast/scratch/hyaku/chousa-r32/w1/MutC2CounterB/kept-s<seed>/root
```

Both actual runs exited **1** and printed:

```text
RESOLVED_HOPS=60/120
RESEARCH_GATE: DRIFT (hops=120 verified=60 exempt=0 anchor-missing=30 refused=24 invalid=6 findings=60 drift=60)
```

Exactly R1, R2, R3, F1 and E5 verified, **12 each**. E1/E8/E9/E10 were anchor-missing (**30**); E2/E3/E6/E7 refused (**24**); E4 invalid (**6**). There were no duplicate CHAIN ids or per-hop truth mismatches on either seed. Evidence, including original/resolved record hashes and per-class observations: `hidden-truth-base-s320260230317.json`, `hidden-truth-base-s320260230331.json`, their `.output.json` files, and `hidden-truth-audit-fresh-summary.json`.

### Preserved inconclusive attempts and environmental limits

- An initial audit used a byte-identical but flat scratch gate copy and obtained **66 verified / 18 refused**, with precisely E7's six hops differing on each initial control seed. That is **INCONCLUSIVE for the intended boundary**, not a killed mutant or a hidden-truth failure. `LANE_ROOT` is the gate directory's parent (`tools/research-gate.sh:290-291`), and either LANE_ROOT or --root is allowed (`:1213-1222`); the relocated gate admitted the scratch outside directory. Original evidence remains in `hidden-truth-summary.json` and `hidden-truth-s<seed>.output.json`. The subsequent actual-lane-path audits on the initial two seeds also yielded the expected 60/30/24/6; their evidence remains in `hidden-truth-base-summary.json`.
- The first additional-fresh-seed audit failed before launching its first gate: `BlockingIOError: [Errno 11] Resource temporarily unavailable`, outer exit **1**, under `--nproc=2000`. Recorded in `audit-fresh-attempt1-error.json`; no gate score was inferred. Retrying only that failed audit stage with a still-bounded `--nproc=8192` completed both fresh audits. An earlier actual-base run on seed 320260230283 emitted two `fork: retry` warnings but still produced all 120 correct classifications; its stderr is preserved. No warning was suppressed or turned into a passing score.

## Commands and restoration

All commands ran from `/home/vgpnk/Projects/shokunin/chousa-shokunin`. The executed driver stages `prepare`, `frozen`, `pristine`, `keep`, `mutant`, `audit-base`, `restored`, `raw`, and `keep-fresh` completed with outer exit **0**. Representative exact command:

```text
timeout 120s prlimit --as=1073741824 --nproc=2000 python3 /fast/scratch/hyaku/chousa-r32/w1/MutC2CounterB/run-probe.py frozen
```

The frozen stage invokes the committed counter, with explicit `--gate`, `--seed`, and `--receipt` for each control. For example:

```text
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count.py --gate /fast/scratch/hyaku/chousa-r32/w1/MutC2CounterB/control-duplicate-finding.sh --seed 320260230271 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/MutC2CounterB/frozen-duplicate-finding-s320260230271.json
```

Successful additional audit command, outer exit **0**:

```text
timeout 330s prlimit --as=1073741824 --nproc=8192 python3 /fast/scratch/hyaku/chousa-r32/w1/MutC2CounterB/run-probe.py audit-fresh
```

The receipt-rejection detector was executed as `timeout 20s python3 /fast/scratch/hyaku/chousa-r32/w1/MutC2CounterB/summarize-evidence.py`, exit **0**, printing twelve `mutant-verdict=KILLED` lines and `EXACT_RESTORATION=true`. Counter subprocesses were bounded at 30 seconds; base-counter/audit subprocesses at 150 seconds. C1_TMP, C2_TMP and TMPDIR all pointed into this seat's scratch directory. CHOUSA_MUTCOUNTER_ALLOW was an environment string, never a marker/import file. Fixtures, loops and artifact writes were finite; artifacts were capped below 1 MiB.

Before and after, the committed counter and every restored scratch counter have SHA-256:

```text
b6626b2cb81b2aeaf66a8ff11a06c030612bf4e264dc128f290021c4aa71f54c
```

Each of the six different intermediate mutant hashes is recorded in `hashes-mutated.json`; `before.json`, `hashes-restored.json` and restored receipts establish exact byte restoration, not merely equivalent behavior. The lane gate and pristine scratch gate retained BASE SHA-256:

```text
0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258
```

No candidate implementation, production source, lane index/jj state or sibling source was changed. No installs, network requests, other AI runtime, subagents, selftest/build/lint runs, or persistent services were used. One tool call was automatically backgrounded on an incoming message; its completion was delivered before further dependent work, and no process remains intentionally running. The controls and scripts remain as scoped evidence; all six counter copies are restored.
