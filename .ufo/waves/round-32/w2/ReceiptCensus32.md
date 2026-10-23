# ReceiptCensus32 — round 32 attempt 2

**Axes:** operability (C1), coverage (C2). **Scope:** committed round-32 JSON through `5d8a170795dcf48c3746a4f03dee9cfe32812834`.

**Scoped verdict: BROKEN — fixable C1 control-provenance defect. All three requested numerical/chronological census checks HOLD.** No below-target candidate receipt or non-oracle v2 target hit was found. This is a critic finding, not admission or canonical judgment.

## What was attacked and what held

1. **Candidate saturation:** all four receipts binding gate `10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098` use the frozen v2 counters; C1 is 24/24 twice, C2 132/132 twice, all `predicate_holds=true`. Zero below-target committed receipts.
2. **Chronology:** every candidate receipt's recorded UTC is strictly later than all three specified control/design commits, using their **committer** timestamps. The latest cutoff is `a065845a` at 07:20:56Z; the earliest candidate UTC is 07:21:14Z, **18 seconds later**. All four candidate receipt files first enter Git in `5d8a1707`; the controls are ancestors, not later commits. `merge-base --is-ancestor` returned 0 for each consecutive pair below.
3. **Non-oracle controls:** under the exact canonical v2 hashes, C1 has 61 non-oracle receipts across 25 gate hashes, maximum **12/24**; C2 has 104 across 39 gate hashes, maximum **126/132**. No control reaches its v2 target. These counts classify by **gate hash**, never by filename alone; the mislabeled L1 copies described below remain in the BASE bucket.

Evidence for these computations: [census-checks.json](ReceiptCensus32/census-checks.json), [complete receipt ledger](ReceiptCensus32/receipt-census.jsonl), [full counter × gate table with source paths](ReceiptCensus32/counter-gate-groups.tsv), and the exact executed argv/exit-code log [commands.json](ReceiptCensus32/commands.json).

### Candidate receipts

All paths below are relative to `.ufo/waves/round-32/`.

| Receipt (under `measure/`) | Counter | Seed | Recorded UTC | Count | Predicate |
|---|---|---:|---|---|---|
| `after-c1-s32001.json` | `e6bf9531` | 32001 | 2026-10-23T07:21:31Z | 24/24 | true |
| `after-c1-s32002.json` | `e6bf9531` | 32002 | 2026-10-23T07:23:15Z | 24/24 | true |
| `after-c2-s32011.json` | `8ec1a1ed` | 32011 | 2026-10-23T07:21:14Z | 132/132 | true |
| `after-c2-s32012.json` | `8ec1a1ed` | 32012 | 2026-10-23T07:21:22Z | 132/132 | true |

### Commit ordering

| Commit | Committer date, UTC | Parent |
|---|---|---|
| `3d586d3a` | 2026-10-23T06:59:48Z | `4111607c` |
| `f43dd5a3` | 2026-10-23T07:13:17Z | `3d586d3a` |
| `a065845a` | 2026-10-23T07:20:56Z | `f43dd5a3` |
| `0f96bc1c` | 2026-10-23T07:21:04Z | `a065845a` |
| `5d8a1707` | 2026-10-23T07:25:26Z | `0f96bc1c` |

### V2 category census

| Counter | Gate category | Receipts | Gate hashes | Matched range | Target hits |
|---|---|---:|---:|---|---:|
| C1 v2 | candidate | 2 | 1 | 24–24 | 2 |
| C1 v2 | oracle | 10 | 5 | 24–24 | 10 |
| C1 v2 | non-oracle control | 61 | 25 | 0–12 | 0 |
| C2 v2 | candidate | 2 | 1 | 132–132 | 2 |
| C2 v2 | oracle | 2 | 1 | 132–132 | 2 |
| C2 v2 | non-oracle control | 104 | 39 | 0–126 | 0 |

Oracle classification is evidenced by `corpus/evidence/round32/claims.md:156-182`, `w1/OracleC1B/v2-rescore.md:16-23`, and `w1/MutC1CounterB/v2-rescore.md:13-29`. The C2 oracle's full identity is also recorded in `w1/OracleC2B.md:15-20`. The committed L1 oracle copies hash to `719d0b92…` (C1) and `1e3d02fe…` (C2); these hashes were independently computed from Git blob bytes. These are feasibility oracles, not non-oracle controls.

## Reproduced counterexample: nominal L1 controls are actually BASE

`corpus/evidence/round32/claims.md:156-159` attributes the L1 v2 receipts to probe-only, append-only, cached-probe and shared-lock controls. The cited evidence does not have those identities:

| Nominal control | Receipt | Recorded gate SHA-256 | Committed purported control copy SHA-256 |
|---|---|---|---|
| probe-only | `controls/L1-design-v2/c1-probeonly-s3201.json` | `0bc318b3…1258` | `c1-probeonly-control-gate.sh`: `0bc318b3…1258` |
| append-only | `controls/L1-design-v2/c1-appendonly-s3201.json` | `0bc318b3…1258` | `a-append-only.sh`: `0bc318b3…1258` |
| cached-probe | `controls/L1-design-v2/c1-cached-s3201.json` | `0bc318b3…1258` | `c-cached-probe.sh`: `0bc318b3…1258` |
| shared-lock | `controls/L1-design-v2/c1-shared-s3201.json` | `0bc318b3…1258` | `d-shared-lock.sh`: `0bc318b3…1258` |

All four purported control copies are byte-identical BASE (`306617` bytes, full hash `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`). Reproduction: for each of the four paths, `timeout 30s git -C <lane> show 5d8a1707:<path>` exited **0**; Python `hashlib.sha256` over each returned blob produced the hash above. Exact paths and results are in `census-checks.json` → `l1_control_identities`, with executed argv in `commands.json`. The probe receipt independently shows BASE at line 7 and 0/24 at lines 12–15; its gate filename at line 6 cannot override that hash.

This is a **false control attribution**, not a counter lie: the receipts honestly record BASE and 0/24. It affects the **operability evidence/provenance** for C1; this census found no corresponding C2 coverage defect or candidate score failure. It is fixable without an axis tradeoff, predicate change, or re-scaling.

**Smallest safe correction:** keep the raw receipts unchanged, label these four entries as BASE reruns, and replace the nominal-control citations with the already committed genuine v2 receipts in `w1/CtlC1PartialLockB/v2/`:

| Genuine control | Gate SHA prefix | Receipt seeds | Recorded results |
|---|---|---|---|
| `mutated-a-append-only` | `4a39b997` | 32472011, 32472012 | 0/24, 0/24 |
| `mutated-b-probe-only` | `034f786b` | 32472021, 32472022 | 0/24, 0/24 |
| `mutated-c-cached-probe` | `59ea2a22` | 32472031, 32472032 | 0/24, 0/24 |
| `mutated-d-shared-lock` | `76c4c073` | 32472041, 32472042 | 0/24, 0/24 |

For example, `w1/CtlC1PartialLockB/v2/mutated-b-probe-only-s32472021.json:5-15` binds canonical counter `e6bf9531…`, genuine gate `034f786b…`, and 0/24. All eight witness rows, full hashes and paths are in the saved ledger. No new counter run is needed to correct the citation identity.

## Exhaustive census method and totals

Read frozen Design v2 (`claims.md:119-189`) first. Commands were bounded and read-only:

- `timeout 30s git -C <lane> ls-tree -rlz 5d8a170795dcf48c3746a4f03dee9cfe32812834 -- .ufo/waves/round-32/` → **780** `.json` blobs, **4,833,698** bytes total, maximum **368,182** bytes; exit **0**.
- `timeout 30s git -C <lane> cat-file --batch` received those blob IDs, preserving committed bytes independently of live wave-2 filesystem writes; exit **0**.
- Each blob was wrapped as `{path,blob,data:<original JSON>}`; `timeout 60s jq -c 'select(.data|type=="object") | select(.data|has("counter_sha256")) | ...'` selected **627** top-level hash-bearing objects; exit **0**. The complete projection is recorded in `commands.json`.
- `timeout 30s jq -s 'group_by([.counter_sha256,.gate_sha256]) | ...'` produced **176** groups across **24** counter hashes; exit **0**. **508** objects are schema-bearing receipts with numeric `matched`/`total`; **119** are metadata/command records and are not treated as failed runs.
- `timeout 30s git -C <lane> log --reverse '--format=COMMIT %H' --name-status 7a7259f0ad41a68068131bfa422a829db9fd1b55..5d8a170795dcf48c3746a4f03dee9cfe32812834 -- .ufo/waves/round-32/` showed **780 JSON additions, zero modifications/deletions**; exit **0**. Thus no earlier committed JSON version in that interval was dropped from this census.
- Git-show blob hashing independently matched the candidate and all four supplied canonical counter identities. Census used subprocess **jq 1.8.2**. One intermediate winner-query program had a missing parenthesis and exited **3**; the corrected query exited **0**. Both invocations are retained in `commands.json`; this was not a counter run or finding.

### Canonical-counter totals

| Counter | SHA-256 prefix | Receipt objects | Metadata objects | Receipt gate hashes | Target hits |
|---|---|---:|---:|---:|---:|
| C1 v1 | `9e787e80` | 97 | 54 | 34 | 15 |
| C1 v2 | `e6bf9531` | 73 | 38 | 31 | 12 |
| C2 v1 | `b6626b2c` | 186 | 4 | 43 | 20 |
| C2 v2 | `8ec1a1ed` | 108 | 3 | 41 | 4 |

The other 20 counter hashes account for **44 receipts and 20 metadata objects** (round-31 regression counters or round-32 counter-mutation evidence), retained below and in the full table; none is silently credited to canonical P1/P2.

### Canonical counter × gate table

Every eight-character prefix below is unique among the corresponding committed counter/gate hashes. Full 64-character hashes, exact observed score values and every source path are in `counter-gate-groups.tsv`. `Matched min–max` is the observed numerator range; denominators are C1 v1/v2 = 24, C2 v1 = 120, C2 v2 = 132. Metadata has no measured numerator.

| Counter | Gate SHA-256 prefix | Receipts | Metadata | Matched min–max | Target hits |
|---|---|---:|---:|---|---:|
| C1 v1 | `016bca0b` | 4 | 4 | 0 | 0 |
| C1 v1 | `034f786b` | 2 | 0 | 24 | 2 |
| C1 v1 | `0bc318b3` | 10 | 0 | 5–10 | 0 |
| C1 v1 | `101afefc` | 2 | 0 | 24 | 2 |
| C1 v1 | `13f387cf` | 2 | 2 | 12 | 0 |
| C1 v1 | `16239673` | 2 | 0 | 0 | 0 |
| C1 v1 | `1b3cf283` | 4 | 4 | 0 | 0 |
| C1 v1 | `25114e46` | 2 | 2 | 1–3 | 0 |
| C1 v1 | `2b1f52fd` | 2 | 0 | 11–12 | 0 |
| C1 v1 | `46a6e487` | 2 | 0 | 1 | 0 |
| C1 v1 | `4a39b997` | 2 | 0 | 1–4 | 0 |
| C1 v1 | `5096cf85` | 4 | 4 | 0 | 0 |
| C1 v1 | `591cc341` | 2 | 0 | 7 | 0 |
| C1 v1 | `59ea2a22` | 2 | 0 | 0 | 0 |
| C1 v1 | `61e2e112` | 2 | 0 | 0 | 0 |
| C1 v1 | `62d9b76c` | 4 | 4 | 12 | 0 |
| C1 v1 | `6c2053e1` | 2 | 0 | 0 | 0 |
| C1 v1 | `719064c3` | 4 | 4 | 0 | 0 |
| C1 v1 | `719d0b92` | 1 | 0 | 24 | 1 |
| C1 v1 | `76c4c073` | 2 | 0 | 7–11 | 0 |
| C1 v1 | `777ac24e` | 4 | 0 | 24 | 4 |
| C1 v1 | `7e98299a` | 2 | 0 | 0 | 0 |
| C1 v1 | `917c9f41` | 2 | 0 | 24 | 2 |
| C1 v1 | `971cdda6` | 4 | 4 | 12 | 0 |
| C1 v1 | `b00c40d4` | 2 | 2 | 24 | 2 |
| C1 v1 | `bf1b9c06` | 2 | 2 | 12 | 0 |
| C1 v1 | `cddd8cae` | 2 | 2 | 12 | 0 |
| C1 v1 | `cf1f234e` | 4 | 4 | 0 | 0 |
| C1 v1 | `d2aeebf7` | 4 | 4 | 0 | 0 |
| C1 v1 | `daf9cd00` | 4 | 4 | 0 | 0 |
| C1 v1 | `dfbb5668` | 2 | 2 | 2–3 | 0 |
| C1 v1 | `dfee8480` | 2 | 0 | 24 | 2 |
| C1 v1 | `e712c76c` | 4 | 4 | 0 | 0 |
| C1 v1 | `f02db767` | 2 | 2 | 5–6 | 0 |
| C1 v2 | `(null)` | 0 | 1 | - | 0 |
| C1 v2 | `016bca0b` | 2 | 2 | 0 | 0 |
| C1 v2 | `034f786b` | 2 | 0 | 0 | 0 |
| C1 v2 | `0bc318b3` | 13 | 0 | 0 | 0 |
| C1 v2 | `10f2fe12` | 2 | 0 | 24 | 2 |
| C1 v2 | `13f387cf` | 2 | 2 | 12 | 0 |
| C1 v2 | `16239673` | 2 | 0 | 0 | 0 |
| C1 v2 | `1b3cf283` | 2 | 2 | 0 | 0 |
| C1 v2 | `25114e46` | 2 | 2 | 0–1 | 0 |
| C1 v2 | `4a39b997` | 2 | 0 | 0 | 0 |
| C1 v2 | `5096cf85` | 2 | 2 | 0 | 0 |
| C1 v2 | `59ea2a22` | 2 | 0 | 0 | 0 |
| C1 v2 | `61e2e112` | 2 | 0 | 0 | 0 |
| C1 v2 | `62d9b76c` | 2 | 2 | 12 | 0 |
| C1 v2 | `6c2053e1` | 2 | 0 | 0 | 0 |
| C1 v2 | `719064c3` | 2 | 2 | 0 | 0 |
| C1 v2 | `719d0b92` | 2 | 0 | 24 | 2 |
| C1 v2 | `76c4c073` | 2 | 0 | 0 | 0 |
| C1 v2 | `777ac24e` | 2 | 0 | 24 | 2 |
| C1 v2 | `7e98299a` | 2 | 0 | 0 | 0 |
| C1 v2 | `917c9f41` | 2 | 0 | 24 | 2 |
| C1 v2 | `971cdda6` | 2 | 2 | 12 | 0 |
| C1 v2 | `b00c40d4` | 2 | 2 | 24 | 2 |
| C1 v2 | `bf1b9c06` | 2 | 4 | 12 | 0 |
| C1 v2 | `cddd8cae` | 2 | 3 | 12 | 0 |
| C1 v2 | `cf1f234e` | 2 | 2 | 0 | 0 |
| C1 v2 | `d2aeebf7` | 2 | 2 | 0 | 0 |
| C1 v2 | `daf9cd00` | 2 | 2 | 0 | 0 |
| C1 v2 | `dfbb5668` | 2 | 2 | 12 | 0 |
| C1 v2 | `dfee8480` | 2 | 0 | 24 | 2 |
| C1 v2 | `e712c76c` | 2 | 2 | 0 | 0 |
| C1 v2 | `f02db767` | 2 | 2 | 0 | 0 |
| C2 v1 | `(null)` | 0 | 4 | - | 0 |
| C2 v1 | `0389f0b3` | 4 | 0 | 60 | 0 |
| C2 v1 | `0bc318b3` | 49 | 0 | 84 | 0 |
| C2 v1 | `0cdc8cb7` | 4 | 0 | 84 | 0 |
| C2 v1 | `0ec9610b` | 2 | 0 | 90 | 0 |
| C2 v1 | `147900f0` | 4 | 0 | 60 | 0 |
| C2 v1 | `1521524a` | 6 | 0 | 0 | 0 |
| C2 v1 | `1e3d02fe` | 2 | 0 | 120 | 2 |
| C2 v1 | `2303d3a7` | 6 | 0 | 0 | 0 |
| C2 v1 | `2c45d74e` | 2 | 0 | 66 | 0 |
| C2 v1 | `2dccb4ac` | 2 | 0 | 96 | 0 |
| C2 v1 | `30225fad` | 4 | 0 | 114–120 | 2 |
| C2 v1 | `308dab50` | 4 | 0 | 78 | 0 |
| C2 v1 | `32e03f4f` | 4 | 0 | 114–120 | 2 |
| C2 v1 | `34de7556` | 2 | 0 | 72 | 0 |
| C2 v1 | `36e2326f` | 2 | 0 | 54 | 0 |
| C2 v1 | `3e5a6eaa` | 4 | 0 | 72 | 0 |
| C2 v1 | `3e6c2a5a` | 6 | 0 | 0 | 0 |
| C2 v1 | `43c0ef88` | 2 | 0 | 60 | 0 |
| C2 v1 | `447f3801` | 2 | 0 | 120 | 2 |
| C2 v1 | `4db1cd8c` | 4 | 0 | 60 | 0 |
| C2 v1 | `5a517c0d` | 2 | 0 | 67–79 | 0 |
| C2 v1 | `5b503e64` | 2 | 0 | 120 | 2 |
| C2 v1 | `6596225e` | 6 | 0 | 0 | 0 |
| C2 v1 | `6793d739` | 2 | 0 | 60 | 0 |
| C2 v1 | `6bed45fb` | 4 | 0 | 102–108 | 0 |
| C2 v1 | `7433cf8e` | 4 | 0 | 104–108 | 0 |
| C2 v1 | `7be8f1d2` | 4 | 0 | 96–102 | 0 |
| C2 v1 | `7dee9147` | 6 | 0 | 84 | 0 |
| C2 v1 | `88852cc8` | 2 | 0 | 108 | 0 |
| C2 v1 | `9a4f6461` | 6 | 0 | 36 | 0 |
| C2 v1 | `a0eab06c` | 4 | 0 | 114–120 | 2 |
| C2 v1 | `a4552ca0` | 4 | 0 | 114 | 0 |
| C2 v1 | `a4a1dcee` | 2 | 0 | 60 | 0 |
| C2 v1 | `a7011a17` | 2 | 0 | 42–54 | 0 |
| C2 v1 | `ac7bedd5` | 1 | 0 | 114 | 0 |
| C2 v1 | `afa7bfde` | 4 | 0 | 60 | 0 |
| C2 v1 | `bae7fd1c` | 2 | 0 | 66 | 0 |
| C2 v1 | `bc038106` | 2 | 0 | 120 | 2 |
| C2 v1 | `c9d2eee9` | 2 | 0 | 120 | 2 |
| C2 v1 | `cf0bc25d` | 2 | 0 | 120 | 2 |
| C2 v1 | `d08f0503` | 2 | 0 | 120 | 2 |
| C2 v1 | `d77e0221` | 4 | 0 | 102–108 | 0 |
| C2 v1 | `f22d0239` | 2 | 0 | 60 | 0 |
| C2 v2 | `(null)` | 0 | 3 | - | 0 |
| C2 v2 | `0389f0b3` | 2 | 0 | 60 | 0 |
| C2 v2 | `097adc9a` | 2 | 0 | 0 | 0 |
| C2 v2 | `0bc318b3` | 26 | 0 | 0 | 0 |
| C2 v2 | `0cdc8cb7` | 2 | 0 | 84 | 0 |
| C2 v2 | `0ec9610b` | 2 | 0 | 102 | 0 |
| C2 v2 | `10f2fe12` | 2 | 0 | 132 | 2 |
| C2 v2 | `147900f0` | 2 | 0 | 60 | 0 |
| C2 v2 | `1e3d02fe` | 2 | 0 | 132 | 2 |
| C2 v2 | `2c45d74e` | 2 | 0 | 66 | 0 |
| C2 v2 | `2dccb4ac` | 2 | 0 | 108 | 0 |
| C2 v2 | `30225fad` | 4 | 0 | 96 | 0 |
| C2 v2 | `308dab50` | 2 | 0 | 78 | 0 |
| C2 v2 | `32e03f4f` | 2 | 0 | 126 | 0 |
| C2 v2 | `346de1ab` | 2 | 0 | 0 | 0 |
| C2 v2 | `34de7556` | 2 | 0 | 83–87 | 0 |
| C2 v2 | `36e2326f` | 2 | 0 | 54 | 0 |
| C2 v2 | `3e5a6eaa` | 2 | 0 | 84 | 0 |
| C2 v2 | `43c0ef88` | 2 | 0 | 60 | 0 |
| C2 v2 | `4db1cd8c` | 2 | 0 | 24 | 0 |
| C2 v2 | `5a517c0d` | 2 | 0 | 85–86 | 0 |
| C2 v2 | `5b77f338` | 2 | 0 | 0 | 0 |
| C2 v2 | `6793d739` | 2 | 0 | 60 | 0 |
| C2 v2 | `6bed45fb` | 2 | 0 | 120 | 0 |
| C2 v2 | `7433cf8e` | 2 | 0 | 120 | 0 |
| C2 v2 | `77033ae5` | 2 | 0 | 0 | 0 |
| C2 v2 | `7be8f1d2` | 2 | 0 | 114 | 0 |
| C2 v2 | `88852cc8` | 2 | 0 | 120 | 0 |
| C2 v2 | `a0eab06c` | 2 | 0 | 126 | 0 |
| C2 v2 | `a3aebd9a` | 2 | 0 | 96 | 0 |
| C2 v2 | `a4552ca0` | 2 | 0 | 126 | 0 |
| C2 v2 | `a4a1dcee` | 2 | 0 | 60 | 0 |
| C2 v2 | `a7011a17` | 2 | 0 | 51–52 | 0 |
| C2 v2 | `afa7bfde` | 2 | 0 | 60 | 0 |
| C2 v2 | `bae7fd1c` | 2 | 0 | 66 | 0 |
| C2 v2 | `c70319a9` | 2 | 0 | 96 | 0 |
| C2 v2 | `cc16c479` | 2 | 0 | 0 | 0 |
| C2 v2 | `d1da62be` | 2 | 0 | 0 | 0 |
| C2 v2 | `d5022219` | 2 | 0 | 36 | 0 |
| C2 v2 | `d77e0221` | 2 | 0 | 120 | 0 |
| C2 v2 | `f22d0239` | 2 | 0 | 60 | 0 |
| C2 v2 | `f8576812` | 2 | 0 | 0 | 0 |

### Other counter × gate groups (retained, not canonical P1/P2)

| Counter prefix | Gate prefix | Receipts | Metadata | Matched min–max | Schema(s) |
|---|---|---:|---:|---|---|
| `0cc2c78b` | `d2aeebf7` | 2 | 2 | 24 | r32-c1/v1 |
| `0efbd172` | `0bc318b3` | 2 | 0 | 132 | r31-c1/v3 |
| `0efbd172` | `85d85a7b` | 2 | 0 | 120 | r31-c1/v3 |
| `0efbd172` | `f9da8257` | 1 | 0 | 132 | r31-c1/v3 |
| `1064fdb3` | `0bc318b3` | 2 | 0 | 120 | r31-c2/v2 |
| `1c96fd1e` | `1521524a` | 2 | 0 | 120 | r32-c2/v1 |
| `2e097962` | `5096cf85` | 2 | 2 | 24 | r32-c1/v1 |
| `4bde7951` | `e712c76c` | 0 | 2 | - | metadata only |
| `585486de` | `7dee9147` | 2 | 0 | 120 | r32-c2/v1 |
| `654183e1` | `0bc318b3` | 2 | 0 | 132 | r31-c2/v3 |
| `654183e1` | `85d85a7b` | 1 | 0 | 132 | r31-c2/v3 |
| `654183e1` | `f9da8257` | 2 | 0 | 120 | r31-c2/v3 |
| `9a61b157` | `cf1f234e` | 2 | 2 | 24 | r32-c1/v1 |
| `a6e6d7af` | `971cdda6` | 2 | 2 | 24 | r32-c1/v1 |
| `a7b65311` | `9a4f6461` | 2 | 0 | 120 | r32-c2/v1 |
| `a84b173a` | `daf9cd00` | 2 | 2 | 24 | r32-c1/v1 |
| `c3aca35d` | `0bc318b3` | 2 | 0 | 120 | r31-c1/v2 |
| `c5c6ce4a` | `3e6c2a5a` | 2 | 0 | 120 | r32-c2/v1 |
| `c7f1b5e2` | `1b3cf283` | 2 | 2 | 24 | r32-c1/v1 |
| `cbf6189e` | `62d9b76c` | 2 | 2 | 24 | r32-c1/v1 |
| `d20c24b1` | `016bca0b` | 2 | 2 | 0 | r32-c1/v1 |
| `d213368f` | `2303d3a7` | 2 | 0 | 120 | r32-c2/v1 |
| `de621c34` | `6596225e` | 2 | 0 | 120 | r32-c2/v1 |
| `e6f825d7` | `719064c3` | 2 | 2 | 24 | r32-c1/v1 |

## Limits and side effects

This is a census of **committed** evidence at the pinned revision, not uncommitted wave-2 receipts or unrecorded executions. Recorded UTC and SHA fields establish the requested recorded ordering/attribution, not independent wall-clock authentication. The broader claim that no future round-32 run can miss is not established by a finite census. No new gate/counter executions, tests, builds, network requests, installs, runtime judgments, lane production edits, Git/JJ writes, or background processes were performed. Only the requested report and bounded artifacts in this seat's own directory were written; all started subprocesses returned.
