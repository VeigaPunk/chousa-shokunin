# MutCounterC1v2 — counter-of-counter probe

**Axes:** operability; coverage of probe-only locking defects and silently failed delay injection.

**Scoped verdict: HOLDS for the original C1 v2 detector protections exercised here.** Removing the write delay and explicitly bypassing its guard falsely accepts the actual probe-only control, 24/24 instead of pristine/restored 0/24. The original self-check rejects an inert strace shim with exit 2; deleting the check under that same shim falsely accepts the control, 24/24. A 1 ms delay with the check bypassed scores 22/24: weaker discrimination, but **not** a surviving gate control on this run. No candidate gate or C2 counter was run; this is not a round-admission judgment.

**Separate finding: BROKEN supplied control provenance.** The named `controls/L1-design-v2/c1-probeonly-control-gate.sh` is byte-identical to the base gate, not the actual probe-only control. Testing that file alone cannot demonstrate the requested probe-only-lock result.

## Inputs, confinement and detector

Paths below are relative to the lane unless absolute. Artifacts named without a directory are under `.ufo/waves/round-32/w2/MutCounterC1v2/` (A). Scratch root S is `/fast/scratch/hyaku/chousa-r32/w2/MutCounterC1v2`.

- Read the frozen Design v2 at `corpus/evidence/round32/claims.md:119-189`, especially the 300 ms delay and fail-closed check at lines 145-148. Contract: lines 23-28. Counter behavior: `c1-count-v2.py:85-105,312-319,334-373`.
- Counter source SHA-256: `e6bf95313ad603ff75e03bb64fbe5a2689a9dfe9bc4c0715a21012383508d891`. Every trial is the existing fixed 24-trial detector; fixture generation, writer counts, deadlines and manifest checks are unchanged.
- Supplied gate SHA-256: `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258` (the registered base digest). Its append at `controls/L1-design-v2/c1-probeonly-control-gate.sh:3192-3202` has no flock. The old `controls/L1-design-v2/c1-probeonly-s3201.json:6-7` also records that base digest despite the probe-only name. The old receipt is context only, not a run of this seat.
- To finish the reachable experiment without silently substituting the supplied gate, retained it unchanged at `S/as-supplied/tools/research-gate.sh` and separately reconstructed the intended control at `S/probe-only/tools/research-gate.sh` from the opened `w1/CtlC1PartialLockB/b-probe-only.patch:7-24`. Reconstructed SHA-256 exactly matches the old actual control: `034f786be1570136b27d72ec630e24be1c6a673ce53434d476af94f4bb5f0340`. Its exclusive probe lock is explicitly unlocked before the write. Evidence copies: `as-supplied-gate.sh`, `reconstructed-probe-only-gate.sh`, `original-probe-only.patch`.
- All experiments used own scratch copies; C1_TMP, C2_TMP and TMPDIR pointed at `S/tmp`, outside both scratch lane roots. No lane production files, Git index, jj state, sibling files, network or other runtime were written/invoked.
- Initial `timeout 30s df -h /fast` exited 0: 220G available. Existing dependencies: strace 7.2, Python 3.14.8, `/usr/bin/prlimit`. **No installs.**

The same bounded invocation was used throughout (complete actual argv, exit, stdout, stderr and hashes are in every `<run>.run.json`, collected in `all-runs.json`):

```sh
timeout --kill-after=10s 720s prlimit --nproc=8000 --fsize=1048576 env C1_TMP="$S/tmp" C2_TMP="$S/tmp" TMPDIR="$S/tmp" PYTHONDONTWRITEBYTECODE=1 python3 "$COUNTER" --gate "$GATE" --seed 32482001 --receipt "$A/$RUN.json"
```

Shim runs additionally prepend `S/shim` to PATH. The executable shim discards only the counter's known strace arguments and `exec`s the traced command, without tracing/injecting; exact bytes: `inert-strace-shim.sh`. At most two foreground counters ran concurrently, managed and joined within each call; no background jobs. All receipt/run wrappers identify these as controls or mutants, never candidates.

## Mutations and hashes

Pristine and all restored counter copies have the source digest above. Exact mutation snapshots and their `.patch` files are retained in A.

| Copy | Smallest behavior change | Mutant SHA-256 |
|---|---|---|
| `remove-delay.py` | Remove only the injection `-e` option from `traced()`; keep self-check | `be94a67cd48ced1706df8f09547769df667d1e797aabd531d1de2a27765c3869` |
| `one-ms.py` | Change only `DELAY_US = 300000` to `1000`; keep 0.25 s self-check | `8aa8ef2571b13729ac93639a307bd2230a9e0ccbb3334e73c8d4a8d1592ae117` |
| `drop-selfcheck.py` | Replace startup check/abort block with `delay_took = None`; keep 300 ms injection | `c8b65fb705a62a26033e0fa5d1b1ef9020d6cb46da667c4c0df3bcdce5239aca` |
| `remove-delay-bypass.py` | No injection plus the explicit check bypass, to permit full scoring | `5a86f172747433d1ff5acab9a15373ff57d0024d27043cfad57d869d20f1805a` |
| `one-ms-bypass.py` | 1 ms injection plus the explicit check bypass, to permit full scoring | `e7079b360f515efb409989cd0d9ca21eddfeb347d7ba1d3aaea16c011b6e8598` |

The last two are deliberately **compound weakened controls**, not claims that a one-line delay change alone bypasses the original self-check. Without that second change both abort correctly.

## Every run and actual output

All run names below end in `-s32482001`; each has `<name>.run.json` containing the actual command/output. A numeric score means stdout `APPEND_SERIALIZED=N/24`; numeric receipts additionally exist as `<name>.json`. `guard` means stderr `c1-count: strace delay self-check failed (took T)` with no numeric receipt. Each full run contains all 24 original trials. There were **23 invocations: 16 full receipts and 7 harness rejections**; no omitted/retried counter run.

| Run name before seed suffix | Gate | Actual score / guard time | Exit |
|---|---|---:|---:|
| `pristine-as-supplied` | supplied base | 0/24 | 1 |
| `pristine-true-probe` | reconstructed probe-only | 0/24 | 1 |
| `removed-delay-guarded-true-probe` | probe-only | guard 0.004 s | 2 |
| `one-ms-guarded-true-probe` | probe-only | guard 0.006 s | 2 |
| `pristine-shim-true-probe` | probe-only + inert shim | guard 0.004 s | 2 |
| `removed-delay-guarded-as-supplied` | supplied base | guard 0.003 s | 2 |
| `one-ms-guarded-as-supplied` | supplied base | guard 0.004 s | 2 |
| `no-selfcheck-real-true-probe` | probe-only | 0/24 | 1 |
| `no-selfcheck-shim-true-probe` | probe-only + inert shim | 24/24 | 0 |
| `removed-delay-bypass-as-supplied` | supplied base | 12/24 | 1 |
| `removed-delay-bypass-true-probe` | probe-only | 24/24 | 0 |
| `one-ms-bypass-as-supplied` | supplied base | 9/24 | 1 |
| `one-ms-bypass-true-probe` | probe-only | 22/24 | 1 |
| `no-selfcheck-real-as-supplied` | supplied base | 0/24 | 1 |
| `no-selfcheck-shim-as-supplied` | supplied base + inert shim | 8/24 | 1 |
| `restored-removed-delay-true-probe` | probe-only | 0/24 | 1 |
| `restored-one-ms-true-probe` | probe-only | 0/24 | 1 |
| `restored-no-selfcheck-real-true-probe` | probe-only | 0/24 | 1 |
| `restored-no-selfcheck-shim-true-probe` | probe-only + inert shim | guard 0.004 s | 2 |
| `restored-removed-delay-as-supplied` | supplied base | 0/24 | 1 |
| `restored-one-ms-as-supplied` | supplied base | 0/24 | 1 |
| `restored-no-selfcheck-real-as-supplied` | supplied base | 0/24 | 1 |
| `restored-no-selfcheck-shim-as-supplied` | supplied base + inert shim | guard 0.006 s | 2 |

The pristine runs' exit 1 / 0/24 is the **expected successful rejection of a known defective gate**, not a failed baseline. Pristine real-strace checks took 0.304/0.305 s. Exit-2 runs have no trial score and are not passed off as killed gate mutants or numerical zeroes.

## Detector and mutation verdicts

Counter-of-counter expectation: reject the deliberately probe-only gate, or reject the host before trial scoring when injection does not work. Here “KILLED counter mutant” means this comparison exposes false acceptance; “SURVIVED” means that binary false-acceptance detector found none.

- **No-delay + explicit guard bypass: KILLED.** Probe-only gate scores pristine 0/24 → mutant 24/24 → exact-byte-restored 0/24. Thus the bad gate **survives the weakened counter**, not the original one. The one-change no-delay copy is instead caught by the retained self-check (exit 2).
- **1 ms + explicit guard bypass: SURVIVED the binary false-acceptance test.** Probe-only scores 0/24 → 22/24 → 0/24. Its two failing trials still reject the gate; do not claim a 24/24 survivor or that 1 ms is always sufficient/insufficient. The one-change 1 ms copy is caught by the original check (exit 2).
- **Self-check deletion: SURVIVED healthy-host scoring; KILLED under silent injection failure.** With real strace it still rejects the probe-only gate at 0/24. Under the inert shim, pristine exit 2 → mutant 24/24 exit 0 → restored exit 2. This directly demonstrates the check's fail-closed host protection and the false acceptance when removed.
- **Supplied-control provenance: BROKEN.** Its unchanged base bytes never reach 24/24 in these runs, even when delay/check are weakened. The result is not evidence against the load-bearing delay; it is a different control with no probe lock. The independently reconstructed, hash-matched probe-only gate supplies the discriminating experiment. Existing W1 true-control receipts are not invalidated by this finding.

## Restoration, scope and limits

`counter-restoration.json` and `restoration-and-scope.json` record before/mutant/restored hashes and exact-byte comparisons. All four mutable scratch counter copies were restored to `e6bf9531…08d891` before the restored detector runs. After those runs, the reconstructed scratch gate was also restored exactly to its originally copied base bytes; both scratch gates finish at `0bc318b3…11258`. Mutant snapshots in A are intentionally retained evidence, not active scratch subjects.

Source counter and supplied control remain byte-identical to initial bytes. The lane production gate was **observed to change during this concurrent wave**, from `10f2fe12…b4098` at initial fingerprinting to `d13a76e3722647965e039c1ac286a166be75c63c0cd5a0e17ad2eef42013edd7` at final scope recording. This seat made no writes to it; authorship/cause is unobserved. No candidate run is attributed to either digest.

`process-cleanup.json`: unique owned C1_TMP environment sweep found `before=[]`, `remaining=[]`, exit 0; all started detector processes returned. Every artifact write is bounded below 1 MiB; detector subprocesses also used a 1 MiB per-file limit. No tools installed. One tool-output issue (worker-thread print output missing despite saved records) was reported through `xd://report_issue`; all results above come from persisted actual subprocess records.

Limits: one fixed seed, one host; deliberately weakened counters are controls, not changes to the frozen predicate. The 1 ms run remains a rejecting negative control. No claim about C2, candidate production correctness, source-row validity, or round admission follows from this scoped probe.
