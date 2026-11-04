# R76Sentinel — bounded metadata secrecy review

PROBE=FAIL — one stable blob-size tuple identifies `case-00-unchanged` in all three runs; opaque subjects and fresh tree hashes do not make every metadata channel unstable.

## Contract and axes

Frozen controls revision: `da9ac7ec684fe9fe9ad5554cab6180057255b76b`, as named in `corpus/evidence/round76/claims.md` (read first). Axes: subject opacity; order unpredictability; tree-key instability; size-key instability; candidate-visible class secrecy. This is a scoped diagnostic, not a C1 integration judgment or a claim that a forger reaches 12/12.

Source SHA256 matched the frozen claim: `b79d6441057a01b27eb465c6b0625cd46502114f8b622b370c2cd2805c81913f`. Counter SHA256: `9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41`. No frozen instrument was edited.

## Exact commands and exits

Working directory for all fixture commands: `/fast/scratch/hyaku/chousa-r76/R76Sentinel`. The instrumented copy is retained beside this report under `R76Sentinel/probe-matrix.py`; it adds metadata reads/prints and does not change case construction or scoring. Its diagnostic case labels must never be used as candidate input.

For each `r` in `1 2 3`, ran:
```sh
python3 -B probe-matrix.py --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round74/correction-count.py --work w$r > run$r.txt 2>&1
```
Each invocation exited **0**, each with `LOADER_MATRIX=12/12 MATRIX=PASS`. The three receipts are:
- `.ufo/waves/round-76/w1/R76Sentinel/run1.txt`
- `.ufo/waves/round-76/w1/R76Sentinel/run2.txt`
- `.ufo/waves/round-76/w1/R76Sentinel/run3.txt`

Fail-closed receipt check:
```sh
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-76/w1/R76Sentinel/summarize.py
```
Exit **1**, `PROBE=FAIL`; missing, incomplete or malformed receipts instead exit 2. Output: `R76Sentinel/probe-result.txt`.

## Numbers

- Distinct subjects: **1** (`case`) across **36** observations.
- Distinct case orders: **3/3**. Orders below use case numeric prefixes only.
- Distinct tree ids: **36/36**; every case has **3/3** different trees.
- Distinct blob-size tuples: **32/36**; unchanged has **1/3**, replace-equal **2/3**, all other cases **3/3**.
- Distinct path sets: **1**, identical five paths in all 36 observations.
- Full `(subject,tree,sizes,paths)` tuples: **36/36** distinct. This does NOT establish that each component channel is safe.

Run 1 order: `00 10 05 04 08 06 02 09 11 03 07 01`.
Run 2 order: `03 05 06 04 10 09 11 08 07 01 00 02`.
Run 3 order: `02 05 09 08 01 03 04 06 10 11 07 00`.

Size tuple order: `LOG.md, SCORECARD.md, after-r72-corrections.txt, battery-past-locale-dies-pinzone-r72.txt, corpus/lessons/round-72.md` (exact receipt paths are in the raw runs).

| Case | Run 1 sizes | Run 2 sizes | Run 3 sizes | Distinct |
|---|---|---|---|---|
| case-00-unchanged | (107,101,43,44,202) | (107,101,43,44,202) | (107,101,43,44,202) | 1/3 |
| case-01-append | (140,101,43,44,202) | (142,101,43,44,202) | (164,101,43,44,202) | 3/3 |
| case-02-append | (107,101,43,44,247) | (107,101,43,44,263) | (107,101,43,44,251) | 3/3 |
| case-03-append | (107,150,43,44,202) | (107,138,43,44,202) | (107,136,43,44,202) | 3/3 |
| case-04-delete | (128,101,43,44,202) | (106,101,43,44,202) | (112,101,43,44,202) | 3/3 |
| case-05-delete | (107,101,43,44,207) | (107,101,43,44,229) | (107,101,43,44,211) | 3/3 |
| case-06-delete | (107,110,43,44,202) | (107,112,43,44,202) | (107,108,43,44,202) | 3/3 |
| case-07-replace-equal | (143,101,43,44,202) | (129,101,43,44,202) | (143,101,43,44,202) | 2/3 |
| case-08-receipt-change | (107,101,43,101,202) | (107,101,43,93,202) | (107,101,43,77,202) | 3/3 |
| case-09-dup-log-heading | (161,101,43,44,202) | (159,101,43,44,202) | (171,101,43,44,202) | 3/3 |
| case-10-dup-lesson-heading | (107,101,43,44,257) | (107,101,43,44,277) | (107,101,43,44,251) | 3/3 |
| case-11-dup-card-heading | (107,176,43,44,202) | (107,160,43,44,202) | (107,140,43,44,202) | 3/3 |

Tree ids by case (runs 1 / 2 / 3):

- `case-00-unchanged`: `71197e6ebbccf5361ea2ecd9e3554dabc60f697a` / `c812fab244ca538a3d736dc131963a4f7452baf6` / `9df442540c74b4570942921fa866565ac4560dc9`
- `case-01-append`: `19f814c094e1c60574d2887336102fa7b7df62bb` / `af6434993414e411dce5c67aa00eed5ca0d50e81` / `82601229bce912f3feff597bb05e5e352287e544`
- `case-02-append`: `a652f07234a7fde0112f85e94c50df4521bb4608` / `169fff3bfc1f31bad3fd8b849ce66ce300daf394` / `1e883ecf9f2477f23c972b9ad0b1e097246b677e`
- `case-03-append`: `20cd314a6e21ed51e9858ae9be4cbce96439865e` / `b26650296c43ebb53ba9e8743bcf0cfd8e328285` / `0d75b2139a2bb6f51c29351b9ca262bcd8b2961a`
- `case-04-delete`: `bde04dc402f94fa84a5ab7ea1a9e8e070ca0382a` / `393262c934cbd4e4fcb212f5f2b399c370bf54b2` / `3561b8e66d6d5433876ede4f181d3f7b85bd639c`
- `case-05-delete`: `2eb2e59b451d5b3f5d74ba87982947cbc4c1ecbb` / `44a9181445c9db3a1b9caee63069258de27898c9` / `8c954ddf2e1e5ea05f538e18c83cfcb3db747e1f`
- `case-06-delete`: `622bbdc9b14062463921a023c28c84d48883c89b` / `df47fd603155bcee96cbbd8f00b77e0aa96efc1e` / `b068056499300189f9fb1b1768e62e803975f943`
- `case-07-replace-equal`: `5b71151909ebb76a31a4eb4b4d6e92549be5d7d3` / `506712fd944b7cad29dd3d8b6e233095553cc9e1` / `f8d3af504de73025c7802351d9de1ac1840d3a08`
- `case-08-receipt-change`: `05be8107e02969598f7f26bc64ab119a4d04950c` / `61c1cf27ed0ff82cbb9323fb4e379f83584887c0` / `27606af85767860d98ab780b99884fc766492a21`
- `case-09-dup-log-heading`: `21b3569b5bba95118a0e57df5bd93707a5429cf8` / `bf3b1f15d7ccebbb5acbee804a36faa3e09c9b65` / `f926274623bee08187079db0f907246f4cf0f637`
- `case-10-dup-lesson-heading`: `c84ca3b96a5c60099f9e50ef32b0a473e2df7d2a` / `4bb8b77ea010fd1977f648a73eddb90d84f721d6` / `27b8a376b3c49ed3bdc470cfdae946360d8bfaba`
- `case-11-dup-card-heading`: `8f5657f15dcd14e6e6480d2d2262ef757d1fd618` / `d54e5016e7bfa368f567f043d1ae7a3a06efc50a` / `ce64121f4ac14b2652154b4d233c5df502dd1c3a`

## Finding — medium: stable size oracle for one class

**Exploit path:** a subject reads `git ls-tree -l -r --full-tree REV` using its supplied `--lane` and `--rev`. The tuple **(107,101,43,44,202)** names unchanged in **3/3** runs and appears in **0/33** other case observations. No blob need be opened. Thus the answer to “can any single metadata tuple identify a case class across runs?” is **yes: this size tuple identifies one class**. This is not a demonstrated twelve-class oracle.

**Evidence:** `loader-matrix-v3.py:98-100` adds salt with fixed textual length; `:146` supplies `secrets.token_hex(8)`, always 16 hex characters. The unchanged branch (`:164-165`) never calls `mutate()`, so it receives no random-length padding. The sentence “no case keeps a stable ... blob size” at `:99` is false for unchanged. The three raw runs and table above measure the resulting stable tuple. Tree-equals-base also fires exactly **3/3** unchanged cases and **0/33** others; tree randomization does not hide this relation.

**Impact:** partial answer-key leakage and overstated secrecy provenance, despite all positive runs scoring 12/12. A full tuple containing a fresh hash has no exact cross-run repeats, but projecting onto size retains a replayable key. No arbitrary-forgery conclusion or frozen battery kill-rule outcome is claimed.

**Smallest remediation:** in a successor instrument, randomize baseline padding lengths, including the unchanged fixture, and explicitly test the unchanged size signature. For the current frozen claim, record this limit; do not patch the frozen instrument after scoring. Random-length padding alone is probabilistic and does not promise zero collisions or eliminate tree/base equality.

## Supplementary subject-visibility observation (not the battery geometry)

A read-only observer was also run against the **unmodified** matrix with stdout redirected to a regular receipt file:
```sh
PROBE_OBS="$S/ob$r" python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/loader-matrix-v3.py --counter "$S/observer.py" --work "$S/ow$r" > obs-buf-$r.txt 2>&1
```
Three invocations exited **1**, each `LOADER_MATRIX=4/12 MATRIX=FAIL` because the observer deliberately prints constant PASS rather than implementing a counter. These are visibility diagnostics, not claimed forger victories. A fourth run with `PYTHONUNBUFFERED=1` also exited 1 with 4/12.

Through `/proc/<ppid>/fd/1`, each subject invocation read the regular-file prefix. For all three default-env runs, prior `CASE` line counts by invocation were **0,1,2,3,4,5,6,7,8,9,10,11**. The final child therefore has 11 named completed cases; combined with the public 12-case table, the remaining class is forced. This is a second **partial**, regular-file-output answer-key channel. The battery uses `capture_output=True` (a pipe); that geometry was **not measured by this observer**, so these regular-file observations must not be represented as battery leakage. The existing seed-leak forger is not a proof of absence of all order-prefix strategies.

Artifacts: `observer.py`, `ob1/`, `ob2/`, `ob3/`, `obu/`, `obs-buf-{1,2,3}.txt`, `obs-unbuf-1.txt`. Parent environment tokens containing `case` were empty in the inspected record. Measured host ptrace_scope was 1; no memory/ptrace probing was performed. Smallest output-channel remediation for a successor: withhold named per-case results until all children finish, rather than relying on buffering.

## Scope, cleanup, and tools

No lane/fleet Git mutation, commits, network, package installation, runtime delegation, or production edits. Fixture initialization, add and commits were confined to scratch; the matrix asserts `rev-parse --show-toplevel` matches its fixture before add/commit. Only this seat folder and seat report were written outside scratch. Scratch is deleted after copying receipts and before yielding. No `resume_continuity_v1` surface belongs to this assignment.

Self-check: accuracy 4/5 (three-run sample, not arbitrary-forgery proof); completeness 4/5 (required fields and numbers supplied, supplementary pipe geometry intentionally unclaimed); clarity 4/5 (raw paths retained); actionability 4/5 (smallest successor-only remediation named); conciseness 3/5 (full hash/size table retained for audit).

Report: .ufo/waves/round-76/w1/R76Sentinel.md
