# W2 ReviewControlReceipts33 — control re-score receipt audit (round 33, FALSIFY)

Date 2026-10-23. Seat: ChousaR33.ReviewControlReceipts33 (leaf reviewer; no subagents, no background jobs, no installs).

## Attacked

The pre-data control re-score `.ufo/waves/round-33/controls/L1-v2-rescore/` (68 receipts + summary.txt + rescore.sh) and the seats' own v1 receipts under `.ufo/waves/round-33/w1/CtlC1*/`. Questions: (1) is any rescore receipt scored on a gate restored to base under a control name (the round-32 mistake); (2) does every receipt's `gate_sha256` equal the sha256 of the gate file it names; (3) is every receipt on counter v2 `cb354dd1…`; (4) does summary.txt match the receipts; (5) do the seats' v1 receipts name mutated gate hashes.

## Method

Script `audit.py` (copy in `.ufo/waves/round-33/w2/ReviewControlReceipts33/audit.py`, detail log `audit-detail.txt`) computed, per receipt: counter hash, gate file existence + fresh sha256, base-hash-vs-control-name, total/label/predicate arithmetic, seed, gate_rc, `.out` first line, and summary.txt bijection + rc consistency. Chain check joined each rescore gate hash to the same-named control's v1 mutated-phase receipt hash. Two independent reproduction runs of the counter (below). Referenced hashes recomputed: landed gate `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e`, `c1-count-v2.py` `cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514`, `c1-count.py` `ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229` — all equal the design values in `corpus/evidence/round33/claims.md`.

## Results

**Primary check — no round-32 mistake.** All 68 rescore receipts name a lane gate under `.ufo/waves/round-33/w1/CtlC1*/` and `gate_sha256 == sha256(file)` for 68/68 (zero mismatches). Exactly three controls carry the base hash `f4731885…`, all base-by-design: `CtlC1DoNothing/research-gate-do-nothing`, `CtlC1BraceDepth/pristine-gate`, `CtlC1NoFinding/base-pristine`. No mutated-named control scores on base bytes. Seeds are 3341/3342 only (fresh; never 3301–3373).

**Counter hash.** `counter_sha256 == cb354dd1…` in 68/68 receipts. `total=156` and `label == TOPLEVEL_FIELD_MATCH=matched/total` in 68/68; `predicate_holds=true` exactly on the two feasibility-oracle controls × 2 seeds (`CtlC1DupPolicy/strict-oracle`, `CtlC1NoFinding/oracle-pristine`, 156/156, counter rc=0); every non-oracle receipt rc=1. `gate_rc=1` on 66/68 (exception below, documented).

**summary.txt ↔ receipts.** 68 rows ↔ 68 receipts, bijective; every row's label equals its receipt label and its `.out` first line; rc=0 iff matched=156, else 1, in all 68. Best non-oracle row: `CtlC1DupPolicy c-differ-only 142/156` — max over all non-oracle rows, matching the claimed 142/156.

**v1 receipts name mutated hashes.** Every mutated-phase v1 receipt in `w1/CtlC1*/` carries a non-base `gate_sha256` (e.g. `w1/CtlC1StripNested/control-a-93331001.json` → `d673f65c8337…`). Chain v1-mutated → lane gate file → v2 rescore hash is identical for all 28 mutated controls (script output "CHAIN-OK" 28/28; e.g. `CtlC1RejectNested/c-truncate-nested` `f2ac600bce55`, `CtlC1NoReader/control-c` `c0f935cdd97f`). The `*-restored-*` and `*-pristine-*` v1 receipts that carry the base hash are deliberate lifecycle restore-checks, honestly named and documented (`CtlC1BraceDepth.md:35`, `CtlC1LastWins.md:154-156`, `CtlC1AllJunk.md:117-118`); their scratch gate paths now hold base bytes because the seats restored them by design — the archived mutant bytes live in the lane w1 gate files, which is what the rescore scored.

**Reproduction (KILL-RULE compliant: `--receipt` in my dir, stdout redirected to file, fresh seeds 3451/3452, C1_TMP/C2_TMP/TMPDIR in my scratch).**
- `timeout 900 python3 corpus/evidence/round33/c1-count-v2.py --gate .ufo/waves/round-33/w1/CtlC1DupPolicy/c-differ-only.sh --seed 3451 --receipt .ufo/waves/round-33/w2/ReviewControlReceipts33/repro-c-differ-only-s3451.json > …/repro-c-differ-only-s3451.out 2>&1` → exit 1, `TOPLEVEL_FIELD_MATCH=142/156` (summary row: 142/156; receipt gate_sha256 `a22183229567…` = lane file).
- Same on `CtlC1BraceDepth/pristine-gate.sh`, seed 3452 → exit 1, `TOPLEVEL_FIELD_MATCH=60/156` (summary row: 60/156; base hash).

## Findings by severity

- **HIGH/CRIT: none.** The control re-score is internally consistent and not affected by the round-32 restored-to-base mistake.
- **INFO-1:** `CtlC1AllJunk--all-supported-s334{1,2}.json` have `gate_rc=0`, so the counter scores all records none → 0/156. Documented by the seat (`CtlC1AllJunk.md:44` "all-supported, whose gate itself exited 0") and consistent with the counter's fail-closed rule (`c1-count-v2.py` docstring). Not a defect.
- **INFO-2:** `CtlC1DupPolicy/strict-oracle` and `CtlC1NoFinding/oracle-pristine` share identical gate bytes `930a20755418…`. Both are feasibility oracles (never candidates), and the shared hash is documented (`CtlC1DupPolicy.md:91-93`). Not a defect.

## Verdict

**HOLDS.** All 68 v2 rescore receipts: correct counter hash, gate hash == named file, base hash only on the three base-by-design controls, summary.txt/`.out`/receipts agree, oracle-only 156/156, best non-oracle 142/156 reproduced independently on a fresh seed. v1 receipts all name genuine mutated gate hashes with an unbroken hash chain into the v2 re-score.

## Limits and residual risk

- Reproduction covered 2 of 34 control gates (the max non-oracle and a base control); the other 32 rows are verified only by receipt↔file-hash↔summary consistency, not re-execution.
- The v1→v2 chain proves byte identity of gate files, not that each seat's v1 mutated hash was the bytes actually executed at v1 time; that rests on the seats' own run logs (spot-checked in `CtlC1BraceDepth/*.run.json` with before/after hashes; not exhaustively re-derived).
- `per_class` distributions inside receipts were checked for label arithmetic only, not recomputed from raw gate output (except via the two reproduction runs' totals).

Artifacts (all in `.ufo/waves/round-33/w2/ReviewControlReceipts33/`, each < 1 MiB): `audit.py`, `audit-detail.txt`, `repro-c-differ-only-s3451.{json,out}`, `repro-pristine-gate-s3452.{json,out}`. No lane files edited; no git/jj writes; no processes signalled (none started beyond the two awaited counter runs); no network.
