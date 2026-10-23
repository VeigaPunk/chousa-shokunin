# ExecCounterC1Timing — round-35 w2: C1 counter cost (operability axis)

Seat: leaf executor, lane chousa, round 35 v2 wave. Read-only on all lane
production files; no edits outside this directory. No installs were needed
(nothing installed).

## 1. What I ran

Gate under test (receipt-pinned, verified before and after):

```
sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617
```

This equals the round-35 lane-declared landed-gate sha256, so every score below
is a measurement of the landed gate.

Counter (committed, unmodified):

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
export C1_TMP=/tmp/hyaku/chousa-r35/w2/ExecCounterC1Timing
timeout 1800 python3 corpus/evidence/round35/c1-count.py --seed 3571 --receipt .ufo/waves/round-35/w2/ExecCounterC1Timing/run1.json   # exit 0
timeout 1800 python3 corpus/evidence/round35/c1-count.py --seed 3571 --receipt .ufo/waves/round-35/w2/ExecCounterC1Timing/run2.json   # exit 0
```

Both runs printed `GREP_PIN_MATCH=9/9` (all nine scenarios PASS) and exited 0.

## 2. Total wall time (the asked number)

External wall clock (`bash` `time`, TIMEFORMAT `%R`), seed 3571:

| run | external wall | counter-internal `elapsed_s` | `matched` | `predicate_holds` | `gate_sha256` | `len(receipt["runs"])` |
|-----|---------------|------------------------------|-----------|-------------------|----------------|----------------------|
| run1 | **0.812 s** | 0.77 s | 9/9 | true | `1f2fb4f5…` | 10 |
| run2 | **0.703 s** | 0.66 s | 9/9 | true | `1f2fb4f5…` | 10 |

**Total for the two required runs: 1.515 s (≈0.75 s per run).**
The expectation in my brief ("the fixture is 3 short claims, so it should be
seconds") is *not* met as stated — the whole counter is **sub-second**, not
seconds. That is strictly better for the operability axis; the C1 counter is
cheap enough to run on every mutation.

Stability (5 further repetitions of the identical command, runs 3–7, exit 0
each, `GREP_PIN_MATCH=9/9` each): external walls 0.772 / 0.754 / 0.715 / 0.750
/ 0.683 s (mean 0.741 s, min 0.683, max 0.812). Counter-internal `elapsed_s`:
0.72 / 0.71 / 0.67 / 0.71 / 0.64.

Caveat on load: the host was heavily loaded by the parallel fleet during part
of the session (`/proc/loadavg` ≈ 35.85 on 32 CPUs at 16:59). Under that load
the same command measured 1.51–1.78 s internally. The 0.7–0.8 s figures above
were taken in the quieter windows; the honest range is **0.64–1.78 s**, still
seconds-scale, never minutes.

## 3. Gate invocations per run, and the reference

**Gate invocations per counter run = 10** (one reference + nine scenarios),
counted from the receipt's `runs` array, which has exactly 10 entries in every
one of the 7 receipts I produced:

```
runs[0] scenario=reference  rc=1
runs[1] scenario=S1 rc=1   runs[2] scenario=S2 rc=1   runs[3] scenario=S3 rc=1
runs[4] scenario=S4 rc=2   runs[5] scenario=S5 rc=2   runs[6] scenario=S6 rc=2
runs[7] scenario=S7 rc=1   runs[8] scenario=S8 rc=1   runs[9] scenario=S9 rc=1
```

Reference entry (identical in run1 and run2):

```json
{"drift": true, "obs": {"K1": ["supported", "match"], "K2": ["unsupported", "mismatch"],
 "K3": ["unsupported", "mismatch"]}, "rc": 1, "scenario": "reference", "stderr_tail": ""}
```

`reference_sane` = true in all 7 receipts.

**The reference is re-derived per counter run — yes.** It is executed afresh
inside `main()` on every invocation, never cached across runs:

- `corpus/evidence/round35/c1-count.py:188-189`
  `# reference: real PATH, no shims, no overrides`
  `rc0, out0, err0 = run_gate(gate, claims, root, path_override=clean_path)`
- captured at `c1-count.py:193` (`ref = {"rc": rc0, …}`) and appended to the
  receipt at `c1-count.py:194-195`.

Precision worth stating, because "re-derived" can be read two ways:
it is re-derived **once per counter process/run** (line 189), and *that single
in-process reference* is then the comparison basis for all nine scenarios via
`same_as_ref` (`c1-count.py:207-209`, which compares against `ref["rc"]`,
`ref["drift"]`, `ref["obs"]`). The reference is **not** re-run per scenario —
so of the 10 gate invocations, 1 is the reference and 9 are the scenarios. The
reference is a fresh subprocess each time (10 distinct `bash <gate>` execs per
run), so a stateful or cached gate cannot borrow the reference's result.

## 4. Per-scenario timing pattern

Per-invocation wall time was measured with a read-only instrument that imports
the committed counter as a module and wraps its `run_gate()`; the repo file was
not edited. Instrument: `.ufo/waves/round-35/w2/ExecCounterC1Timing/timing-probe.py`
(sha256 `028022f2f3c8c4bc626cdec5cdd7ef8223f06eb3fd20705045f97e515f5e741f`),
5 repetitions, all exit 0, all `GREP_PIN_MATCH=9/9`.

| scenario | min s | median s | max s | pattern |
|----------|-------|----------|-------|---------|
| reference | 0.103 | 0.220 | 0.232 | full match path |
| S1 shim-first PATH | 0.114 | 0.224 | 0.296 | full match path |
| S2 BASH_ENV fn shim | 0.100 | 0.228 | 0.265 | full match path |
| S3 grep absent from PATH | 0.098 | 0.194 | 0.227 | full match path |
| S4 override relative | 0.014 | 0.030 | 0.035 | **refusal — early exit** |
| S5 override missing | 0.016 | 0.023 | 0.041 | **refusal — early exit** |
| S6 override non-GNU | 0.016 | 0.025 | 0.044 | **refusal — early exit** |
| S7 override real + echo | 0.095 | 0.180 | 0.257 | full match path |
| S8 default + echo | 0.111 | 0.168 | 0.224 | full match path |
| S9 override beats shim | 0.110 | 0.188 | 0.220 | full match path |

Sum of the 10 gate invocations: min 0.788 s, median 1.505 s, max 1.781 s
(median inflated by the load window, see §2).

The pattern is two clean clusters, and it is exactly what the landed gate's
design predicts:
* **seven "does the matcher run" scenarios** (reference, S1, S2, S3, S7, S8, S9)
  each cost ~0.10–0.30 s — the gate reads the fixture, resolves and verifies
  the grep pin, and runs the matcher on three short claims;
* **three "refusal" scenarios** (S4, S5, S6) each cost ~0.014–0.044 s — roughly
  **4–8× cheaper** — because the gate refuses at startup with
  `research-gate: GREP_PROVENANCE refused: …` and exit 2 *before* any record is
  read. Observed refusals (verbatim from the receipts):
  - S4: `override is not an absolute path (candidate=bin/grep)`
  - S5: `override is not a regular file (candidate=…/_shim/absent-grep)`
  - S6: `override does not report GNU grep: <no version> (candidate=…/_shim/stub-grep)`

  S6's `stub_calls` = 1: the non-GNU stub was exec'd exactly once (the
  provenance `--version` probe) and never used for a match.

Cost shape conclusion for the operability axis: **the C1 counter's cost is
dominated by per-scenario gate startup, not by fixture size.** Seven scenarios
do a full verification pass over a 3-claim fixture and still finish in ~0.1 s
each. There is no cost cliff for a mutant suite.

## 5. Calibration observation (new; not a kill)

**The C1 counter's `--seed` is decorative: two "fresh seeds" are two runs of a
bit-identical fixture.** Measured, not inferred:

- `make_fixture(root)` (`c1-count.py:71`) takes no seed and writes fixed
  content; `c1-count.py:187` calls it as `claims = make_fixture(root)`.
- `seed` is consumed in exactly three places: the default generator
  (`c1-count.py:157`), the temp-dir **name prefix** (`c1-count.py:164`,
  `root = tempfile.mkdtemp(prefix="w35c1-%08x-" % (seed & 0xFFFFFFFF), dir=base)`),
  and the receipt field (`c1-count.py:281`).
- Direct measurement: I called the counter's own `make_fixture()` for seeds
  3501, 3517 and 3571 into separate roots; the produced `claims.jsonl` is
  **byte-identical**, sha256
  `8ca39794fc82cbb6fcb40e6942cafc91405776188fa03e51dc9981580c200b7e`, 405 bytes,
  for all three seeds (`ALL_IDENTICAL=True`). Content is the fixed 3-claim set
  K1 supported / K2 mutated / K3 left-glued.

Consequence: P1's "on each of two fresh seeds" is satisfied *formally* but buys
no additional fixture diversity for C1 — the two seed runs are replications of
one fixed fixture (which is why my 7 runs are so tightly clustered, §2). This
is a **calibration gap, not a kill**: the predicate still holds 9/9 on every
seed I ran, and the discriminating power the counter was designed for (S1–S9)
does not depend on fixture randomization. It does contrast with C2, whose
counter explicitly reasons about per-seed randomization
(`corpus/evidence/round35/c2-count.py:26`: "per-seed randomization of the
fixture does not remove it"). For C1 the honest statement is: *one fixture,
N replications.* If the round wants C1's seed to mean something, the fixture
builder would have to consume the seed (e.g. vary span length / mutation
position / glued side) — currently the seed only renames the temp directory.

## 6. Artefacts (all inside my own directory, all < 1 MiB)

`/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-35/w2/ExecCounterC1Timing/`
(120 KB total)

| file | sha256 |
|------|--------|
| `run1.json` (required run 1 receipt) | `4eb690195b1a6df412d7090c793f805ae0826918d97299e13b7ab0c816c9c68a` |
| `run2.json` (required run 2 receipt) | `47bf10b62d1699d09b95632027d763cf54ca78f47cec103e5a71c18dba0c9e5e` |
| `run3.json`…`run7.json` (5 extra repetitions) | see dir listing |
| `probe1.json`…`probe5.json` (instrumented timing receipts) | see dir listing |
| `timing-probe.py` (read-only instrument, 1439 B) | `028022f2f3c8c4bc626cdec5cdd7ef8223f06eb3fd20705045f97e515f5e741f` |
| `run3.out`…`run7.out` (stdout of the extra repetitions) | — |

Scratch (outside the repo, for logs): `/tmp/hyaku/chousa-r35/w2/ExecCounterC1Timing/`
(the same files plus `fixture-probe.py`; the instrumented runs' stdout). No
counter temp dir leaked under my `C1_TMP` (`ls -d …/w35c1-*` → 0 matches; the
counter removes its root in its `finally`, `c1-count.py:296`).

Observed but **not mine and not touched**: two leftovers `/tmp/w35c1-00000dad-*`
(seed 3501) and `/tmp/w35c1-00000dbd-*` (seed 3517), created 16:49 by another
seat whose runs did not set `C1_TMP`/`TMPDIR`. Flagging only.

## 7. Verdict

- **Operability (my axis): PASS, and better than briefed.** The C1 counter
  costs **0.64–0.81 s per run unloaded (median 0.74 s), total 1.515 s for the
  two required seed-3571 runs**, worst case 1.78 s under fleet load. It is a
  sub-second to ~2 s counter, cheap enough to be run against every mutant.
- **Cost pattern:** 10 gate invocations per run (1 reference + 9 scenarios);
  the reference is re-derived per run at `c1-count.py:188-189` and reused as the
  in-process comparison basis for all nine scenarios (`c1-count.py:207-209`).
  Seven scenarios pay a full verification pass (~0.10–0.30 s each); the three
  refusal scenarios exit at startup in ~0.014–0.044 s (4–8× cheaper).
- **Calibration finding (new):** the C1 fixture is byte-identical across seeds
  (sha256 `8ca39794…`), so C1's "two fresh seeds" are two replications of one
  fixture, not two samples. Reported as a calibration gap, not a kill — P1 held
  9/9 with `predicate_holds=true` on every one of the 7 seed-3571 runs I made,
  all against the landed gate sha256 `1f2fb4f5…`.
- **No MEETS-style finding in my lane**: I did not find a gate that scores 9/9
  without doing the claimed work; I did not build or score any mutant here, so
  I make no claim about the counter's discriminating power (other seats own the
  mutant batteries).

## 8. Limits

- Wall times are from a 32-CPU host shared with a parallel fleet; absolute
  numbers are load-dependent (range 0.64–1.78 s observed). Relative pattern
  (refusal scenarios 4–8× cheaper) is stable across all 5 instrumented runs.
- `--seed 3571` only; the fixture-identity result in §5 was additionally
  checked at seeds 3501 and 3517 through the counter's own `make_fixture()`.
- I did not re-derive the "before" (base-gate) C1 numbers; those belong to the
  committed controls, and my measurement scope was the landed gate's cost.
- Commands run under `/home/vgpnk/Projects/shokunin/chousa-shokunin` (jj-colocated,
  branch master, HEAD `2b2e0171153f63c2fb657ba601d74c7830662c1b`); no git/jj
  write command was issued. Access date for all quoted lines: 2026-10-23.
