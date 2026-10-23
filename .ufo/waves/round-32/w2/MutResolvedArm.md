# MutResolvedArm — round 32 attempt 2, wave 2

## Axes and verdict

- **Operability:** resolved-hop behaviour and base/landed corpus parity.
- **Coverage:** sensitivity of `--selftest`, `chain-r3`, and C2 v2/F1 to one resolved-only defect.
- **Verdict: HOLDS within this probe's pinned scope.** No base/landed CHAIN-row change was observed. The single mutant was **KILLED by selftest**, but **SURVIVED chain-r3 and c2-count-v2 (including F1)**. That is a reproducible detector-coverage finding, not an observed landed-code defect or permission to change the contract.

All evidence paths below are relative to this report's directory. `MutResolvedArm/` contains the artifacts. The frozen contract says resolved hops are unchanged (`corpus/evidence/round32/claims.md:60-70`); v2 does not change that contract (`:161-182`).

## One mutation

Target: copied pinned gate at `/fast/scratch/hyaku/chousa-r32/w2/MutResolvedArm/landed/tools/research-gate.sh`, inside `chain_probe`, original line 1850. The mutant accepts any literal substring for **resolved quote** hops before the original token-boundary-aware probe. Other statuses and anchor kinds still use the original reader. Patch: `MutResolvedArm/resolved-quote-substring.patch:1-14`; metadata: `MutResolvedArm/mutation.json`.

```bash
if [[ $st == resolved && $PROBE_KIND == quote && $hay == *"$PROBE_TEXT"* ]]; then
  PROBE=verified PROBE_AT="line:$(line_probe "$hay" "$PROBE_TEXT")"
elif chain_anchor_at "$hay" "$PROBE_KIND" "$PROBE_TEXT"; then
```

Expected detector: `chain-fail-boundary` in selftest. Its three resolved quote negatives are partial/glued words (`tools/research-gate.sh:4543-4560` in the pinned landed gate); the fixture source bytes are at `:3685-3690`. The ordinary chain-r3 fixture has valid resolved anchors and genuinely unavailable exempt anchors (`corpus/fixtures/chain-r3.md:26-47`). F1 generates only valid resolved anchors (`corpus/evidence/round32/c2-count-v2.py:216-223`); the glued negative class uses U statuses (`:242-244`).

## Same bounded detectors: pristine → mutant → exact restoration

All nine detector invocations completed. Exit codes are outer command exits; the C2 counter's internal gate exits 1 as required by its drifting fixture. No baseline failed.

| Detector | Pristine | Mutant | Restored | Mutation verdict |
|---|---|---|---|---|
| `--selftest` | PASS, 241 cases, 0 skipped; exit 0 | FAIL, 1/241; exit 1 | PASS, 241 cases, 0 skipped; exit 0 | **KILLED** |
| `verify-chain chain-r3.md` | 17/22, CLEAN; exit 0 | 17/22, CLEAN; exit 0 | 17/22, CLEAN; exit 0 | **SURVIVED** |
| committed `c2-count-v2.py`, seed 323243 | 132/132; F1 12/12; exit 0 | 132/132; F1 12/12; exit 0 | 132/132; F1 12/12; exit 0 | **SURVIVED** |

Evidence:

- Selftest: `MutResolvedArm/pristine-selftest.out:243`, `mutated-selftest.out:44-50,249`, `restored-selftest.out:243`.
- The mutated selftest actually verifies all three bad quotes and prints `RESOLVED_HOPS=3/3` and CLEAN (`MutResolvedArm/mutated-selftest.out:46-50`). This establishes a behaviour-changing mutant, not a no-op.
- Chain-r3: all three `MutResolvedArm/{pristine,mutated,restored}-chain-r3.out:24-25`. Their 22 CHAIN lines are identical across all phases (`MutResolvedArm/detector-matrix.json`).
- Counter: all three `MutResolvedArm/{pristine,mutated,restored}-c2-count-v2.out:1-6`. Full unmodified-counter receipts are `{pristine,mutated,restored}-c2-control.json`; the mutant receipt is explicitly a control, never candidate data. Its gate hash and 132/132 result are at `MutResolvedArm/mutated-c2-control.json:6-20`. **Every counter run is listed here; none scored below target.**
- Counter SHA-256: `8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a`, matching the committed pinned counter.

### Commands and bounds

`MutResolvedArm/detector-runs.json` records all **47 actual commands**, exit codes, elapsed times, environments, output paths, and output hashes (9 phase detectors + 38 corpus comparisons). Commands were run synchronously to completion; independent detectors/comparisons were concurrent within those bounded calls.

For each phase, the actual command forms were the following, with absolute paths expanded in the command ledger. `G=/fast/scratch/hyaku/chousa-r32/w2/MutResolvedArm/landed/tools/research-gate.sh`, `L=/home/vgpnk/Projects/shokunin/chousa-shokunin`, and `P` is pristine, mutated, or restored:

```bash
timeout --kill-after=5s 850s prlimit --fsize=16777216 --nproc=8000 -- bash "$G" --selftest
timeout --kill-after=5s 180s prlimit --fsize=16777216 --nproc=8000 -- bash "$G" verify-chain "$L/corpus/fixtures/chain-r3.md" --root /home/vgpnk/Projects/shokunin
timeout --kill-after=5s 720s prlimit --fsize=16777216 --nproc=8000 -- python3 "$L/corpus/evidence/round32/c2-count-v2.py" --gate "$G" --seed 323243 --receipt "$L/.ufo/waves/round-32/w2/MutResolvedArm/$P-c2-control.json"
```

All CHOUSA variables were removed from the launching environment; `TMPDIR` and `C1_TMP` were `/fast/scratch/hyaku/chousa-r32/w2/MutResolvedArm/tmp`, and `C2_TMP` was the sibling `c2-tmp`, outside both scratch lane roots. Each command's direct child was waited, then its process group was sent cleanup SIGKILL if still present. No tool background jobs or subagents were used.

## Base versus landed: every corpus Chain table

Inventory search: tool `grep`, pattern `^## Chain[\t ]*$`, path `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus`, `gitignore=false`; all 19 matching sections contain a hop table, including the prose-prefaced knowledge record (`corpus/knowledge/archived-export-intake.md:55-72`). Inventory: `MutResolvedArm/chain-records.txt`.

Each record was passed to both copied gates with the same root `/home/vgpnk/Projects/shokunin` and the 180-second command form above. Base was `7a7259f0ad41a68068131bfa422a829db9fd1b55`; landed was `5d8a170795dcf48c3746a4f03dee9cfe32812834`. Existing corpus/MINT/SKILL/README inputs were exposed through scratch input symlinks; the selftest-required PROVINCE file was copied. Gate bytes were never taken from the changing working copy.

**Result: 19/19 identical, 117/117 CHAIN lines identical, zero changed records.** `MutResolvedArm/corpus-chain-diff.json:2-10` contains totals; each following entry records the input hash, both exits, both output paths and the empty per-record diff. `MutResolvedArm/base-landed-CHAIN.diff` is empty.

| Record under `corpus/` | CHAIN lines, each gate | Base/landed exits | CHAIN diff |
|---|---:|---|---|
| fixtures/archives-r9/A-r9.md | 7 | 0/0 | none |
| fixtures/archives-r9/B-r9.md | 7 | 0/0 | none |
| fixtures/archives-r9/C-r9.md | 8 | 0/0 | none |
| fixtures/archives-r9/controls/A-r9-anchor-missing.md | 7 | 1/1 | none |
| fixtures/archives-r9/controls/A-r9-span-not-found.md | 7 | 0/0 | none |
| fixtures/archives-r9/controls/B-r9-false-sweep.md | 7 | 0/0 | none |
| fixtures/archives-r9/controls/B-r9-rejection-missing-flip.md | 7 | 0/0 | none |
| fixtures/archives-r9/controls/C-r9-dangling-ref.md | 8 | 0/0 | none |
| fixtures/archives-r9/controls/C-r9-structure-break.md | 8 | 0/0 | none |
| fixtures/chain-r3-broken.md | 2 | 1/1 | none |
| fixtures/chain-r3.md | 22 | 0/0 | none |
| fixtures/full-r6-absent.md | 1 | 0/0 | none |
| fixtures/full-r6-broken.md | 3 | 1/1 | none |
| fixtures/full-r6.md | 3 | 0/0 | none |
| fixtures/integrity-r7-broken.md | 4 | 0/0 | none |
| fixtures/integrity-r7.md | 4 | 0/0 | none |
| fixtures/sweeps-r5-broken.md | 1 | 0/0 | none |
| fixtures/sweeps-r5.md | 3 | 0/0 | none |
| knowledge/archived-export-intake.md | 8 | 1/1 | none |

## Restoration and limits

`MutResolvedArm/restoration.json:2-7` records exact byte equality and the 335,789-byte restored scratch gate:

- Before: `10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098`.
- Mutant: `86b0ad3397d77c3f85b3a4d3c790ee3711168381b98215e3dfdd2cb5bad6e633`.
- Restored: `10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098`.
- Base gate: `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258` (`MutResolvedArm/setup.json`).

One mutation only, as assigned by the mutation-tester role; no separate line-offset or source-pointer mutant, no C1 counter, no network, no installs, and no production/code/index/jj writes by this seat. F1's survival establishes only this resolved false-positive blind spot; it does not negate the exempt-hop metric. Selftest catches this defect, so this probe supplies no landed-code falsification.

**Working-copy scope warning:** a final read of the live lane gate returned SHA-256 `d13a76e3722647965e039c1ac286a166be75c63c0cd5a0e17ad2eef42013edd7`, different from the assigned pinned target. That file was not exercised here. All results above remain explicitly about copied `10f2fe12…` bytes, not that later live file (`MutResolvedArm/scope.json`).
