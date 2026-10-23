# Round-34 check of routed round-33 repairs E1–E5

Reviewer: R34ReviewRepairs (UFO-FSD, read-only on lane; runs in /fast/scratch/hyaku/chousa-r34/w2/R34ReviewRepairs). No installs. Commands quoted; outputs observed.

## E1 (fuzz binding) — DONE

- Committed blob: `git -C … show b8053900:tools/research-gate.sh | sha256sum` → `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`.
- Receipts `.ufo/waves/round-34/w1/ExecE1Fuzz/fz-9021{2,3,4}-landed-43a1af35.json` all carry exactly that `gate_sha256`; each `n=650 matched=650 flat=60 calibration_flat_ok=60`. All four E1 files are committed (`git ls-files`).
- Correction appended at `corpus/knowledge/claim-record-fields-r33.md:84-99`, committed at master (git diff b8053900..HEAD shows it; file clean in working tree). Its statements match the artifacts: old receipts `measure/final/fz-9021{2,3,4}.json` bind `b2c07eda…9b4b` and appear verbatim as UNBOUND in `.ufo/waves/round-34/w1/ExecE4Census/census-round33.txt`; new seeds 90212/90213/90214 = 650/650 + calibration 60/60; mask receipt `fz-90215-maskgate.json` = 640/650, binding `ae7d4bfc…` = sha256 of `w2/L1ShortcutMask/mask-gate.sh` (committed).
- Verdict: E1 done; correction accurate.

## E2 (C1 counter v3) — DONE as routed, but the asserted "mask misses" property is NOT robust (finding)

- Seat receipts committed in `.ufo/waves/round-34/w1/ExecE2Counter/`: mask-s9401/9402 155/156 (S2_nested_confusers 5/6), r32-s9403 60/156 on round-32 base f4731885, r33-s9404/9405 156/156 on 43a1af35. Corpus counter sha256 bd81aeea… == seat copy; receipts record the same counter sha.
- My re-runs (LC_ALL=C, C1_TMP/TMPDIR=scratch, same gate copies, fresh seeds):
  - mask seed 9401: 155/156, rc=1 (reproduces seat; miss c6a5a9c1500 S2_nested_confusers truth=supported observed=invalid).
  - mask seed 61111: 156/156, rc=0 — reproduced twice. The L1 shortcut mask PASSES the v3 counter on this fresh seed: `TOPLEVEL_FIELD_MATCH=156/156`.
  - base-b8053900 gate seed 61112: 156/156 rc=0 (holds); seed 61113 default locale: 156/156.
- Verdict: landed round-33 gate holds on fresh seeds. But "mask gate misses by one record per seed" (claim-record-fields-r33.md:97-99) is seed-dependent: seed 61111 gives 156/156, so on that seed the counter cannot distinguish the shortcut mask from the correct gate. Residual risk: the counter does not guarantee per-seed discrimination against this oracle-shortcut; a per-seed pass is not evidence the mask is defeated. Flag for the lane.

## E3 (calibration, SKILL.md metadata range) — DONE

- `SKILL.md:83` now reads "metadata cases 137–208 and 210–215 (209 is a claims-surface control; corrected round 34, E3)".
- Actual `--selftest` case names (base gate 43a1af35, 251 cases; and current lane gate, 253 cases): cases 137–208 and 210–215 are all `metadata-*` (78 total); case 209 = `claims-registry-colon-deny`. Exact match.
- Adjacent observation: the lane gate at HEAD selftests PASS (253 cases) — adds `claims-longspan`/`claims-longspan-line` at 252–253 — while SKILL.md self-test rows still say `PASS (251 cases)`; that column will be stale once the candidate lands (not part of E3's metadata range).

## E4 (measurement binding census) — DONE

- Ran `w1/ExecE4Census/receipt-binding.py` (sha256 230441acc…, matches the hash cited in non-revision-receipts.md) over `.ufo/waves/round-34/`: TOTAL_RECEIPTS 286, WITH_GATE_HASH 230, BOUND 230, UNBOUND 0, UNBOUND_LANDED_FINAL 0, exit 0.
- `.ufo/waves/round-34/controls/` falls inside the walk (walk_receipts has no exclusion); its 137 receipts carrying a gate_sha256 (30 distinct hashes) are all in the bound set. Manifests under controls (e.g. CtlC1AcceptLong/controls.json) reference 30 gate hashes; all 30 are committed-blob hashes (recomputed set of 277: 34 gate blobs + 243 wave shells).
- The 56 no-hash JSONs are harness/spec/manifest artifacts (w1-dispatch/spec/swarm-registry, *.wrapper/*.process/*.run, controls.json manifests, census-round33.json, residual-call.json), not single-gate receipts.

## E5 (misroot proof) — not routed to this checkpoint

The Task's enumerated checks cover E1–E4 only. Round-34 evidence for E5 is limited to draft lesson text (`w1/ScribeLesson/mistakes.md`, `quality.md`); no executed repair/committed `cmp`/sha256 record was present to verify. Skipped per item scope.

## Residual risk / verification gaps

- E2: per-seed falsification of the L1ShortcutMask not guaranteed (seed 61111 → 156/156). Suggest recording a discriminator property (e.g. run the mask on N fresh seeds) or strengthening confuser generation.
- E3: SKILL.md `PASS (251 cases)` self-test cells stale for the 253-case candidate tip.
- E1/E4 are fully verified; no unbound round-34 receipts.
