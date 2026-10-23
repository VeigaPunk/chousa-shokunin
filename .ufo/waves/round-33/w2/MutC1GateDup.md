# Round 33 / wave 2 — MutC1GateDup

## Scope and verdict

**Axis: operability. Scoped verdict: HOLDS; all four assigned mutants KILLED by both c1-count-v2 and the full selftest.** No surviving mutant and no production C1 counterexample was found in this assigned probe. This is not a judgment of the entire round or of untested inputs.

The governing duplicate contract is `corpus/evidence/round33/claims.md:93-129`, especially :111-114: repeated top-level read fields are invalid even when values agree; an identical duplicated id must remain the CLAIM identity. Detector identity, isolation and exact restoration were non-regression constraints, not additional scored axes.

All paths below are lane-relative unless absolute. Artifact prefix **A** = `.ufo/waves/round-33/w2/MutC1GateDup/`; scratch prefix **S** = `/fast/scratch/hyaku/chousa-r33/w2/MutC1GateDup/`.

## Frozen inputs and smallest mutations

Read-only inspection executed (exit 0):

```sh
timeout 30s git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff 2b9cc73aed30c2e2c95699db6617d9531ef49fb2 0fb300b5c27900ab8bb3abeb5f54776d71e04beb -- tools/research-gate.sh
```

- Frozen gate: **A**`landed.pristine.sh`, SHA-256 `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e`.
- Counter: `corpus/evidence/round33/c1-count-v2.py`, SHA-256 `cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514`; duplicate generation :243-267, identity/finding-aware scoring :369-394.
- Selftest layout prerequisite copied, not invented: **A**`fixture-PROVINCE.md`, SHA-256 `cf7826a43aaab7c00708ab54bb46577217e7a67ab44a43a33e17ee2a58c1bbec`. The selftest deliberately reads this lane-root file (**A**`landed.pristine.sh:5704-5738`).

Each mutation occupied its own scratch `<seat>/tools/research-gate.sh`. Preserved mutant gates are evidence only; no lane production source was edited.

| Mutant / seat | Smallest behavior change; preserved bytes | Mutant SHA-256 |
|---|---|---|
| (a) `no-duplicates` | `json_dup`'s final table predicate becomes `return 1`; **A**`a-no-duplicates.mutant.sh:1275-1278` | `422f319b10e80881c042f5d45c2350ce9d9d3c29743dddfdd0a8f45056aeefce` |
| (b) `line-sha-only` | One guard rejects duplicate queries for every key except line/sha256; **A**`b-line-sha-only.mutant.sh:1275-1279` | `ede3b014b7a5d5c65fbd6f567ced809d5a0b6c4b75bb6bb0d2403ba92649c64d` |
| (c) `id-line-fallback` | Delete the four-line agreeing-id recovery block; duplicated ids always retain `show_id=line$lineno`; **A**`c-id-line-fallback.mutant.sh:1631-1636` | `431beb229dfdd30a8ea37c4a5edbb4b2eadfd2ed4ed23dfb56b05e20c09de9e8` |
| (d) `agreeing-accepted` | One guard makes `json_dup` return false when first/second string values agree; **A**`d-agreeing-accepted.mutant.sh:1275-1279` | `021ca989226b505a7ceca8527d226516874843c7eab20bc284b148e9e3deb922` |

## Commands and bounds

The runner is preserved as **A**`probe.py`. Actual process argv, cwd, recorded PID/process group, exit status, timing, before/after gate hashes, output hashes and receipt path are in every `<stem>.run.json`. Phase manifests: **A**`pristine.runs.json`, `pristine-bounded.runs.json`, `pristine-complete.runs.json`, `mutated.runs.json`, `restored.runs.json`.

Equivalent invocation forms, expanded for every row below:

```sh
C1_TMP="$S/tmp/$seat" C2_TMP="$S/tmp/$seat" TMPDIR="$S/tmp/$seat" \
  timeout --signal=TERM --kill-after=5s 600s \
  prlimit --nproc=2000 --as=4000000000 --core=0 --fsize=900000 -- \
  python3 "$LANE/corpus/evidence/round33/c1-count-v2.py" \
  --gate "$S/$seat/tools/research-gate.sh" --seed "$seed" \
  --receipt "$A/$stem.receipt.json" >"$A/$stem.stdout" 2>"$A/$stem.stderr"

C1_TMP="$S/tmp/$seat" C2_TMP="$S/tmp/$seat" TMPDIR="$S/tmp/$seat" \
  timeout --signal=TERM --kill-after=5s 600s \
  prlimit --nproc=2000 --as=4000000000 --core=0 --fsize=16777216 -- \
  bash "$S/$seat/tools/research-gate.sh" --selftest \
  >"$S/$stem.stdout" 2>"$S/$stem.stderr"
```

`LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin`; S/A in these command forms are absolute prefixes without trailing slash. The runner launched argv directly, stripped inherited CHOUSA_* and Git override variables, and waited for all children; at most three detector processes ran concurrently. Each seat had its own TMPDIR to isolate the selftest's fixed-name sibling fixtures. Selftest logs were copied byte-for-byte from scratch to A after exit. Consequently a selftest `.run.json`'s rendered `command` uses published log paths, whereas its `argv` is the actual launched argv. Counter stdout was redirected directly to A, never piped. The 16 MiB selftest file cap accommodates its bounded 8 MiB source fixtures (:5559-5561 of the pristine gate); preserved gate artifacts are 349,885–350,219 bytes (`timeout 15s wc -c ...`, exit 0).

## Outputs and which detector kills each mutant

A healthy pristine baseline first established `TOPLEVEL_FIELD_MATCH=156/156` on seeds 93330111/93330112 (counter exit 0) and `RESEARCH_GATE_SELFTEST: PASS (248 cases, 0 skipped)` (exit 0). Evidence: **A**`pristine-complete-pristine-counter-93330111.stdout:1`, `pristine-complete-pristine-counter-93330112.stdout:1`, `pristine-complete-pristine-selftest.stdout:250` and their run records/receipts.

| Mutant | Counter on both fresh seeds | Duplicate class on both | Full selftest (exit 1) | Detector verdict |
|---|---|---|---|---|
| (a) no duplicate detection | `132/156`; 93330201, 93330202; counter exit 1 | `0/24` | `FAIL (2/248 cases)`; `r33-top-dup-line` and `r33-top-dup-id` | KILLED by both |
| (b) only line/sha256 | `140/156`; 93330301, 93330302; counter exit 1 | `8/24` | `FAIL (1/248 cases)`; `r33-top-dup-id` | KILLED by both |
| (c) duplicate id always line number | `152/156`; 93330401, 93330402; counter exit 1 | `20/24` | `FAIL (1/248 cases)`; `r33-top-dup-id` | KILLED by both |
| (d) agreeing duplicates accepted | `142/156`; 93330501, 93330502; counter exit 1 | `10/24` | `FAIL (1/248 cases)`; `r33-top-dup-id` | KILLED by both |

Every mutant counter stdout has total at :1 and duplicate-class result at :13; all other classes remained fully matched. Selftest diagnostics: **A**`mutated-no-duplicates-selftest.stdout:246-259`, `mutated-line-sha-only-selftest.stdout:249-255`, `mutated-id-line-fallback-selftest.stdout:249-257`, `mutated-agreeing-accepted-selftest.stdout:249-256`.

Actual selftest input lines, against fixture `lib/span.md` containing the quoted span at line 1 (**A**`landed.pristine.sh:7591-7599,7620-7630`):

```jsonl
{"id":"DP1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported","line":"1","line":"9"}
{"id":"DI1","id":"DI1","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported"}
```

- Pristine/restored: DP1 and DI1 both print `observed=invalid`, retaining their ids.
- (a): DP1 instead prints `observed=supported ... verdict=match` and CLEAN; DI1 also becomes supported.
- (b): DI1 becomes supported; the whole duplicate-id fixture incorrectly exits 0/CLEAN.
- (c): DI1 is still invalid but prints `CLAIM id=line1 ... observed=invalid`; counter misses are identity losses (`observed=none`), not exit-code differences. See **A**`mutated-id-line-fallback-counter-93330401.receipt.json:32-56`.
- (d): DI1 becomes supported while the differing-id row remains invalid; selftest catches the changed claim/tally even though that fixture still exits 1/DRIFT.

## Complete counter run ledger — including every landed-hash run

For **every** stem in this table, all four files exist under A: `<stem>.stdout`, `<stem>.stderr`, `<stem>.run.json`, `<stem>.receipt.json`. Thus this table specifies every receipt path explicitly by suffix. Gate subprocess exit was 1 and no gate timeout occurred in these receipts; `rc` below is the counter exit. The two initial count runs are retained, not discarded because a separate selftest setup attempt failed.

| Stem | Output `TOPLEVEL_FIELD_MATCH` | rc |
|---|---|---|
| `pristine-pristine-counter-93330101` | `156/156` | 0 |
| `pristine-pristine-counter-93330102` | `156/156` | 0 |
| `pristine-complete-pristine-counter-93330111` | `156/156` | 0 |
| `pristine-complete-pristine-counter-93330112` | `156/156` | 0 |
| `mutated-no-duplicates-counter-93330201` | `132/156` | 1 |
| `mutated-no-duplicates-counter-93330202` | `132/156` | 1 |
| `mutated-line-sha-only-counter-93330301` | `140/156` | 1 |
| `mutated-line-sha-only-counter-93330302` | `140/156` | 1 |
| `mutated-id-line-fallback-counter-93330401` | `152/156` | 1 |
| `mutated-id-line-fallback-counter-93330402` | `152/156` | 1 |
| `mutated-agreeing-accepted-counter-93330501` | `142/156` | 1 |
| `mutated-agreeing-accepted-counter-93330502` | `142/156` | 1 |
| `restored-no-duplicates-counter-93330211` | `156/156` | 0 |
| `restored-no-duplicates-counter-93330212` | `156/156` | 0 |
| `restored-line-sha-only-counter-93330311` | `156/156` | 0 |
| `restored-line-sha-only-counter-93330312` | `156/156` | 0 |
| `restored-id-line-fallback-counter-93330411` | `156/156` | 0 |
| `restored-id-line-fallback-counter-93330412` | `156/156` | 0 |
| `restored-agreeing-accepted-counter-93330511` | `156/156` | 0 |
| `restored-agreeing-accepted-counter-93330512` | `156/156` | 0 |

All twelve runs on exact landed bytes have receipts and score 156/156; none of this seat's landed-hash runs scored lower. Eight deliberately mutated runs are failures, not failures of the landed bytes.

## Initial inconclusive selftest setup attempts

These were not counted as mutant kills:

1. **A**`pristine-pristine-selftest.run.json`: exit 153 with the initial 900,000-byte file cap. Stderr :1-2 reports the size-cap fixture pipeline receiving `File size limit exceeded`; stdout ends after case 94. Initial wrapper used `--fsize=900000`, no `--core=0`, and common `S/tmp`.
2. **A**`pristine-bounded-pristine-selftest.run.json`: exit 1, `RESEARCH_GATE_SELFTEST: FAIL (1/248 cases)`. The only failure was absent copied lane-root `PROVINCE.md`: **A**`pristine-bounded-pristine-selftest.stdout:106-111,255`. This attempt already used the corrected 16 MiB fixture bound, but still common `S/tmp`.
3. Copied the actual dependency into each scratch root and isolated TMPDIR by seat. The complete pristine baseline above then passed all 248 cases. Mutants and restored copies used that same complete layout, command bounds and full selftest; no test was removed or weakened.

## Exact restoration and limits

Restored all four experimental gate files from the pristine scratch copy using `timeout 15s cp -- S/pristine/tools/research-gate.sh S/<seat>/tools/research-gate.sh` (each exit 0). Ran `timeout 15s cmp -- S/pristine/tools/research-gate.sh S/<seat>/tools/research-gate.sh` for each seat (each exit 0, no output), followed by `timeout 15s sha256sum` over all five scratch gates (exit 0). Every restored file exactly matches the before hash `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e`. Evidence: **A**`restoration.json`, `restored.runs.json`; each restored run record also records that hash both before and after its detector.

All four restored pairs scored 156/156, counter exit 0. All four restored full selftests exited 0 and printed `RESEARCH_GATE_SELFTEST: PASS (248 cases, 0 skipped)` at :250 of **A**`restored-<seat>-selftest.stdout`.

The lane production gate was read-only to this seat. It changed independently during the wave: initial hash `94a7be5a...`, later observed hash `165acd5f6cebfb1d0a179f75572315ae6458ae330fdfc1f1ac412c36478a3563`; no attempt was made to revert that owner change. Measurements here remain pinned to the requested 94a7be5a bytes, not the newer moving worktree. No Git/jj writes, network, installations, subagents or persistent background jobs were used. No baseline-vs-landed custom counterexample, repair D1-D5 audit, source review or global round verdict is claimed: this report closes only the four assigned duplicate-handling mutation probes.
