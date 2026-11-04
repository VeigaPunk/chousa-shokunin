# R76Review — independent frozen remeasurement

## Scope and axes
Predicate reproduction; revision/digest binding; answer-key isolation; receipt reproducibility. Reviewer recommendation only, not admission. No frozen instrument or production file changed. No packages installed. No network, dispatch, or other runtime used.

## Findings, ordered by severity

### Medium: fixed-order batteries admit repository-content-blind leg oracles
`corpus/evidence/round76/c2-battery.py:159-175` invokes the same counter at a stable path in a fixed order: good block, six bogus fixtures, real lane. `run_counter` at lines 106-113 returns only the process exit status. A counter accepting invocations **1 and 8**, rejecting the other six, obtains the exact passing C2 predicate without reading any repository data or running git. Retained executable: `R76Review/forge-leg-order.py`; exact command/cwd/exit: `R76Review/probe-commands.json`; complete printed lines: `R76Review/c2-order-probe.out`. Result: `C2_BATTERY=PASS bogus_rejected=6/6 positive=1/1 lane=PASS`, exit 0. Its comments mistakenly say seven total/seventh; the executed final expression correctly uses `(1, 8)`. Its private state file is the only data it reads.

The analogous outer battery weakness also exists in `matrix-battery-v3.py:123-143`: subjects are always two positives followed by eleven forgers, two invocations each. A matrix accepting its first four invocations and rejecting all others produces `BATTERY=PASS forgers_rejected=11/11 positive=2/2`, exit 0, without invoking any counter or reading a repository. Retained executable: `R76Review/forge-matrix-leg-order.py`; raw result: `R76Review/c1-order-probe.out`; command/exit in the same JSON receipt.

These probes concern the batteries' inference strength, not a demonstrated wrong outcome from either frozen production instrument. They do not independently trigger the frozen kill rules. C1 records finite-subject/non-arbitrary-forgery limits; C2 records text-shape/semantic limits but does not name this predictable-invocation channel. QUALITY 120/126 and the assignment's prohibition on case-order answer keys make this an actionable limitation to record; do not amend frozen bytes under this claim.

### Low: C2's lane leg follows a moving ref, not the checkout
`c2-battery.py:138,173` defaults to `--lane-rev master`. Although the clone checkout is the controls freeze, its `master` resolves to `5eeca32ba9ad80081d19906c7cb52dff35891e8c`. Thus a clean checkout alone does not pin that leg. Direct counter runs at both the claims' base `1af39fed6058ad46fc075b72fddaae838f43273e` and that master printed identical derived/count checks and exited 0:

```text
DERIVED=S182:16 S183:11 RECORDED=S182:18 S183:13
C2V=PASS checks=9/9 rev=1af39fed6058 base=8022f72c889c
C2V=PASS checks=9/9 rev=5eeca32ba9ad base=8022f72c889c
```
No observed lane-leg divergence, but retain the resolved ref when interpreting replication.

## Frozen revision and digests
A clean `git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/chousa-shokunin clone` was made in `/fast/scratch/hyaku/chousa-r76/R76Review`. After confirming `git rev-parse --show-toplevel` named that clone, detached checkout selected the controls revision. `git rev-parse HEAD` printed:

```text
da9ac7ec684fe9fe9ad5554cab6180057255b76b
```

Each digest below was measured with `git show da9ac7ec684fe9fe9ad5554cab6180057255b76b:<path> | sha256sum` (exact pipelines and outputs retained in `R76Review/revision-and-digests.txt`):

| Path | SHA-256 |
|---|---|
| corpus/evidence/round76/loader-matrix-v3.py | b79d6441057a01b27eb465c6b0625cd46502114f8b622b370c2cd2805c81913f |
| corpus/evidence/round76/matrix-battery-v3.py | 217ae367c7e6e4ed23d1e6c1412de50370f309ba12d4a1703eaff386b7094360 |
| corpus/evidence/round76/correction-count-v2.py | 610e5655af2bd2f5f034edcfc732b012db29d8a9ff7295cae8edce835982ecbb |
| corpus/evidence/round76/c2-battery.py | 7e0d6832b705a81d48a1143d0b039dbaeec0665dc01fc8cbd977f97edc0d8619 |
| corpus/evidence/round75/loader-matrix-v2.py | 95bdd49363e475316c5f5a9e200f039fcc1611f6fbd52848af8e078be0268ee7 |
| corpus/evidence/round75/c2-count.py | bf0250e7e1c3f3ebf80626d68f743b2b8ac1f3640e5a15a4d4d4048a186e48b8 |

All digest values named by the claims match. Comparing controls..initial master showed only claims.md added under round76, no instrument modifications.

## Exact predicate commands and results
All below ran from `/fast/scratch/hyaku/chousa-r76/R76Review/clone`. Full output lines are retained in the adjacent receipt folder; the final lines and exit codes are reproduced below. No reduced `--runs` or `--matrix-timeout` options used.

### C1 after
```sh
python3 -B corpus/evidence/round76/matrix-battery-v3.py --matrix corpus/evidence/round76/loader-matrix-v3.py --work /fast/scratch/hyaku/chousa-r76/R76Review/w-c1
```
```text
RUNS=2 CHILD_TIMEOUT=3 MATRIX_TIMEOUT=300
forgers_rejected=11/11 positive=2/2
BATTERY=PASS forgers_rejected=11/11 positive=2/2
EXIT=0
```
Full output: `R76Review/c1-after.out`. Both positives 12/12 twice; all eleven forgers rejected twice. Subject-map 4/12 twice; hang 0/12 twice with matrix exit 1, not battery timeout. Duration 82.265 s. Seed-sensitive marks differ from the committed receipt: order-twelve 1/12 and 3/12 (receipt 4/12 and 2/12); harness-source 2/12 twice (receipt 2/12 and 3/12). No aggregate predicate divergence.

### C2 after and before, explicit requested absolute counter paths
```sh
python3 -B corpus/evidence/round76/c2-battery.py --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/correction-count-v2.py --work /fast/scratch/hyaku/chousa-r76/R76Review/c2-after-absolute
python3 -B corpus/evidence/round76/c2-battery.py --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round75/c2-count.py --work /fast/scratch/hyaku/chousa-r76/R76Review/c2-before-absolute
```
```text
C2_BATTERY=PASS bogus_rejected=6/6 positive=1/1 lane=PASS
EXIT=0
C2_BATTERY=FAIL bogus_rejected=2/6 positive=1/1 lane=PASS
EXIT=1
```
Raw complete lines: `R76Review/c2-after-absolute.out`, `R76Review/c2-before-absolute.out`; exact argv/cwd/exits in `absolute-c2-commands.json`. Before accepts negation, magnitude, comment-only and mid-file; rejects decoy-above and deletion-history. Both directions accept the good fixture and real lane. No divergence from claims. Equivalent runs using the counter paths inside the frozen clone also produced the same summary/exits (`c2-after.out`, `c2-before.out`).

## Additional controls
Parser-pair copies were reconstructed by replacing `MATRIX={verdict}` with `C1={verdict}` or `RESULT={verdict}` in the frozen matrix. Their SHA-256 digests **exactly match** the committed receipt's digests. The C1-label battery printed `BATTERY=PASS forgers_rejected=11/11 positive=2/2`, exit 0; RESULT-label printed `BATTERY=FAIL forgers_rejected=0/11 positive=0/2`, exit 1. Retained copies and commands: `R76Review/v3-c1label.py`, `v3-badlabel.py`, `parser-reconstruction.txt`.

The negative wrong-contract counter is `corpus/evidence/round75/c2-count.py`: running the v3 matrix against it printed `LOADER_MATRIX=0/12 MATRIX=FAIL`, exit 1. An initial attempt guessed nonexistent `round75/correction-count.py` and failed setup (exit 2); this was not treated as a negative-control result. The r74 correction counter is a positive and correctly scored 12/12, exit 0.

## C1 before — full frozen defaults
```sh
python3 -B corpus/evidence/round76/matrix-battery-v3.py --matrix corpus/evidence/round75/loader-matrix-v2.py --work /fast/scratch/hyaku/chousa-r76/R76Review/w-c1b
```
```text
RUNS=2 CHILD_TIMEOUT=3 MATRIX_TIMEOUT=300
RUN FORGER subject-map 0 matrix_exit=0 marks=12/12/PASS
RUN FORGER subject-map 1 matrix_exit=0 marks=12/12/PASS
RUN FORGER hang 0 matrix_exit=timeout marks=none
RUN FORGER hang 1 matrix_exit=timeout marks=none
forgers_rejected=9/11 positive=2/2
BATTERY=FAIL forgers_rejected=9/11 positive=2/2
EXIT=1
```
Full output: `R76Review/c1-before.out`; duration 609.799 s. No shortened run or timeout options were used. All claimed aggregate before/after values reproduce. Seed-dependent before marks differ from the committed receipt: order-twelve 2/12 and 4/12 (receipt 5/12 and 4/12); harness-source 2/12 and 4/12 (receipt 2/12 twice). These do not alter rejection status or the predicate.

Receipts and probe sources were copied to the seat folder before deleting the entire seat scratch root. No scratch fixture or clone remains.

## Residual risk and verification gaps
`xd://lsp` is not mounted (`No such tool`); no semantic references/definition/diagnostics checks were available. Source inspection and executed probes are not presented as LSP proof. No runtime, resume, identity-routing or saturation implementation is changed here, so those general review axes are not applicable. Randomised evidence covers these sampled saltings, not all possible seeds or forgers. Frozen instruments remain untouched.

## Self-evaluation
Accuracy 4/5: raw receipts retained; moving master limits freeze isolation. Completeness 4/5: requested predicates covered; no LSP service available. Clarity 4/5: summaries separated from full logs, but multiple supplemental probes add length. Actionability 4/5: exact commands and preserved probe sources supplied; frozen defects require a new claim rather than in-place fixes. Conciseness 4/5: evidence detail is substantial. Overall 4.0/5. Improvements: pin lane ref in any successor claim, and test content-blind leg oracles in that successor. User agreement expected because no passing predicate is misrepresented as admission.
