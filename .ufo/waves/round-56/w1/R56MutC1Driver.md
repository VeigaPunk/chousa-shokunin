# R56MutC1Driver — frozen C1 counter mutation probe

## Scope and method
- Attacked only the frozen `corpus/evidence/round56/c1-count.py` from lane archive `46e1758f3d8a5d1bf30200d2ff7d909b0230feed`; no production or frozen claim changes. The frozen predicate is `corpus/evidence/round56/claims.md`, §R56-C1.
- Scratch: `/fast/scratch/hyaku/chousa-r56/R56MutC1Driver-2/`; copied lane driver SHA-256 `5eba634ffb9138a787cc6a62b313daad1e821dd96e3d1c61e31bb048e60b1b75`. Archive gate and builder hashes matched receipts: `e3cb3ec5…` and `1ed2650a…` respectively.
- Built (b) with the specified `round56/controls/build-c1-junk.py $S/junk`; built (c) with `round55/controls/build-c1-controls.py $S/r55ctl`. Target batteries were (a) copied R56 battery, (b) `$S/junk`, (c) `$S/r55ctl`.
- For each mutation: changed only that driver clause in the scratch copy; ran its driver against a/b/c, copied back the pristine driver bytes, then reran a/b/c on restored bytes. Every driver invocation used a fresh empty `--work` directory under scratch; `TMPDIR` and `PYTHONDONTWRITEBYTECODE=1` were set. Target (c) used scratch `HOME` for its delegate/LibreOffice path. No `soffice.bin` remained after runs.

## Baseline blocker (all classifications below are inconclusive)
- Diagnostic command: `python3 $S/work/a-base2/gates/G.py --tool $S/lane/tools/build-spans.py --seed 7 --per-leg 2 --work $S/work/direct-g`.
- Observed output: `tool=.../build-spans.py sha256=1ed2650a… seed=7 per-leg=2`; `ENV_CHANGED pinned capture 54fe0734c01f699e735b4b0a digest`; exit 2.
- The expected read-only source path `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` subsequently returned “Path not found”; `sha256sum .../54fe0734c01f699e735b4b0a.raw` returned “No such file or directory.” Earlier in this run, the four raw files were present and their observed SHA prefixes matched the gate pins (`d341c133e37d65f02f8f`, `6063a3aff7a4081e93a6`, `46d1866ce9afd51682e7`, `ac0fad62ed9a11fa3bd1`). The source became unavailable during the probe; I did not write to `shokuknow`.
- Pristine driver runs also returned `CANDIDATE=0/2` with seed vectors `('ENV', 2)` and `C1=FAIL` (e.g. `out/a-base2.txt`, `out/b-base2.txt`, `out/c-base2.txt`). Per mutation/restoration below, the direct gate’s pin failure yielded `CANDIDATE=0/2 KILLED=0/9 DENIED=0/2`, exit 1. This violates the role’s usable-baseline condition; the driver's printed `SURVIVED`/`NOT_DENIED` strings are raw outputs, not valid mutant verdicts.

## Mutation table
`a/b/c` cells are raw `KILLED/DENIED`; `INC` means the missing pinned capture invalidated the baseline. All corresponding restored-byte runs reproduced the same counts and `C1=FAIL`.

| Mutant | Single driver change | a | b | c | Mutated SHA-256 |
|---|---|---:|---:|---:|---|
| A vector vs marker | `failing_legs` drops marker regex (line 205) | 0/9, 0/2 INC | 0/9, 0/2 INC | 0/9, 0/2 INC | `e401dd79338e59dc4e7a12cef9ed624f83a369bdf361fc9870ffc556625169c4` |
| B one seed | accept nonempty `hs` instead of `len(hs)==len(SEEDS)` (line 255) | 0/9, 0/2 INC | 0/9, 0/2 INC | 0/9, 0/2 INC | `f233ecef41746da5b28b2a3eb663e4a5082aa7c91a8d69a22477d523ba160a0f` |
| C one G + one mutant | `seq=["G", tag]` (line 211) | 0/9, 0/2 INC | 0/9, 0/2 INC | 0/9, 0/2 INC | `f8006be2deec54c4609a0ccafa07440b840a4e7e9f6d0d980989f2679141949b` |
| D fixed order | replace `order_rng.shuffle(seq)` with `pass` (line 212) | 0/9, 0/2 INC | 0/9, 0/2 INC | 0/9, 0/2 INC | `9ed79acd0a56f72559009834164c9a6437a49ea8ded698547541d67366ee552b` |
| E sequential run dirs | use `r{self.n:04d}` instead of random token (line 122) | 0/9, 0/2 INC | 0/9, 0/2 INC | 0/9, 0/2 INC | `69f30c443f639e03a1a05b943d7104974355d11251997421fd6dbf6c539e847a` |
| F drop candidate count | remove `cand == len(SEEDS)` from final `passed` (line 281) | 0/9, 0/2 INC | 0/9, 0/2 INC | 0/9, 0/2 INC | `49119c482da852399d3503c3a9ddca4d35eaa4a5fe28fadcfb454ee2c060f877` |
| G weaken DENIED | accept vector without `AUDIT_FORBIDDEN`/`rc=97` (lines 273–274) | 0/9, 0/2 INC | 0/9, 0/2 INC | 0/9, 0/2 INC | `e72f34adc7c606e9ceeacd2de089a913e3060bd325c07936044f2407b0718487` |
| H drop anchor count | remove `src.count(anchor)==1` guard (lines 108–111) | 0/9, 0/2 INC | 0/9, 0/2 INC | 0/9, 0/2 INC | `463bbe62826613309efe7d4ab946fcab04b92b13cf882aad8131d5aa532c853f` |

Each mutant run's full logs are in scratch `out/M-<letter>-{a,b,c}.txt`; restored logs are `out/M-<letter>-restored-{a,b,c}.txt`. In every final matrix run, `CANDIDATE=0/2`, all nine gate mutants printed `SURVIVED`, both probes printed `NOT_DENIED`, and `C1=FAIL`; run counts were a=38, b=34, c=22. Example: `out/M-A-a.txt` has `CANDIDATE=0/2 ...`, `KILLED=0/9 DENIED=0/2`, `C1=FAIL`; `out/M-A-restored-a.txt` has the same.

## Restoration and calibration
- Pristine before every mutation and restored after every mutation: `5eba634ffb9138a787cc6a62b313daad1e821dd96e3d1c61e31bb048e60b1b75`. Each mutated hash is in the table; each `out/hash-M-<letter>.txt` records mutated SHA then restored SHA, which equals pristine.
- No b/c raw counter gain was observed. Because every final run hit the absent pinned-capture baseline failure, this does **not** establish that any clause is load-bearing or that controls fail to exercise one. All eight tested clauses (A–H) are therefore unexercised/inconclusive in this probe; no clause-coverage conclusion is valid. The specific missing prerequisite is the frozen gate's pinned capture at the read-only `.qcache` path.

VERDICT: C1 frozen-driver clause probe — INCONCLUSIVE (pinned capture unavailable; all eight mutations and a/b/c controls fail the baseline).