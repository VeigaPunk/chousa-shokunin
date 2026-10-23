# ExecD6Snapshot — D6 repair: commit snapshot-control code + audit zero-socket assertion

Routed defect D6 (`corpus/lessons/round-29-verifier-spotcheck.md:160-161`): the round-29
snapshot control's code and data stayed in scratch. Repaired by committing the code beside a
full manifest of the scratch data.

## 1. What was copied

Byte-exact copies from `/fast/scratch/hyaku/chousa-r29/w2/CriticClaimDesign/` into
`.ufo/waves/round-30/build/ExecD6Snapshot/`, verified by `sha256sum` + `cmp` (exit 0 for each
pair, `ALL_BYTE_EXACT` printed):

| File | sha256 | Stated value (CriticClaimDesign.md:93-96) | Match |
|---|---|---|---|
| `offline_snapshot_control.py` | `8ec6ac7b6697901954b29110d7f42c43a66d40d1ada7cef861dbd9e57e0ea2cd` | `8ec6ac7b...ea2cd` | yes |
| `network_guard.py` | `10e93e64d45271d4a2d8a911a4a9a9a4a72084decb96032e50b6d4cf6b2b4f73` | `10e93e64...b4f73` | yes |
| `prepare_snapshots.py` | `7ffaf5b0cf39ca38c11fd84d1e25628ded4a26522af2ca47bb364cd1d3cb180a` | (no stated value) | computed |
| `snapshot-provenance.json` | `8e66d9dec272812ae2555afe28695e7766f8c94ead6467e046cb76d99fefed59` | (no stated value) | computed |

The assignment named `offline_snapshot_control.py` and `prepare_snapshots.py` as the two `.py`
files; both are committed. I additionally committed `network_guard.py` (stated-hash, 498 bytes)
and `snapshot-provenance.json` (2 547 bytes) because they are the measurement instrument and
origin record for the very assertion D6 asks to make auditable; leaving them in scratch would
have kept the audit partial. `audit_receipts.py` (the receipt-audit tool for section (b), not
the snapshot control) is covered by hash and path in `manifest.json` only.

## 2. manifest.json

`.ufo/waves/round-30/build/ExecD6Snapshot/manifest.json` lists all 6 files of the scratch dir
with `scratch_path`, `size_bytes`, `sha256`, `mtime_utc` (all mtimes 2026-10-23T01:51:56Z–
01:52:54Z), a `copied_to_ExecD6Snapshot` flag, and the field
`snapshots_json_holds_third_party_page_text: true`. `snapshots.json` (569 691 bytes, sha256
`b22b0f3482ff4f2eb0c13ac47279592413948169ed3c7d3bfc2a95ccb01dc3ab`, matching the stated value)
is a URL-keyed dict of 8 normalized page texts from Poynter, hapgood.us, cochrane.org,
jsonlines.org, w3.org and docs.python.org; per contract it is **not** copied into the lane.

## 3. Audit: how "zero socket events" was measured

Instrument: `network_guard.py` (hash `10e93e64...b4f73`, now committed here). It installs a
`sys.addaudithook` callback that appends every `socket.*` audit event to a counter and raises
`RuntimeError`, then runs the candidate in-process via `runpy.run_path(..., '__main__')` and in
a `finally` block prints `CANDIDATE_SOCKET_EVENTS=<n>` to stderr. Because the candidate runs in
the same process, the guard sees every socket audit event it emits; the counter's own page
fetches run in the counter's separate process and are out of the guard's scope (the receipt
records 16 counter page-fetch slots per run — a network fetch by the counter, not the
candidate).

Recorded evidence (all committed round-29 bytes, no re-run needed):

- `.ufo/waves/round-29/falsify/CriticClaimDesign/offline-snapshot-run{1,2}.json`: the frozen
  counter's own receipts; `cmd` names both scratch scripts, `stderr_tail` is
  `"CANDIDATE_SOCKET_EVENTS=0\n"`, `match` 130/130, seeds
  18048917927880715405 / 6764259072167322905.
- `offline-snapshot-run{1,2}-command.json`: exact argv (`timeout 180s python3
  corpus/evidence/round29/c1-count.py --receipt ... -- python3 .../network_guard.py
  .../offline_snapshot_control.py`), counter exit 0, whole-command wall 4.485 s / 4.502 s.
- `snapshot-provenance-summary.json`: `candidate_socket_events_observed_each_run: [0, 0]`.

## 4. Verdict: can a reader re-check it from committed bytes?

**Recorded outcome — yes.** The receipts, exact command and guard source hash are all
committed; a reader can confirm what was measured and the printed `CANDIDATE_SOCKET_EVENTS=0`
without trusting scratch.

**Re-execution — partially.** The candidate source, guard source and preparation script are now
committed here, and `prepare_snapshots.py` still works today only because the wave-1 cache
(`/fast/scratch/hyaku/chousa-r29/w1/CriticRuntimeVariants/cache/`) still exists on disk
[INFERENCE: scratch is not durable]. A full re-run needs `snapshots.json`, which is
deliberately uncommitted third-party page text; a re-checker must regenerate it with
`prepare_snapshots.py` and confirm sha256 `b22b0f34...c3ab` before running the guard-wrapped
candidate under `c1-count.py`. The measurement chain is therefore fully *auditable* from
committed bytes but not fully *re-executable* from committed bytes alone — a residual scratch
dependency remains on the wave-1 cache.

No network was fetched and nothing was re-run; all work was file copies, hashing and reading
of committed bytes.

## Files changed

- `.ufo/waves/round-30/build/ExecD6Snapshot/offline_snapshot_control.py` (new, byte-exact)
- `.ufo/waves/round-30/build/ExecD6Snapshot/prepare_snapshots.py` (new, byte-exact)
- `.ufo/waves/round-30/build/ExecD6Snapshot/network_guard.py` (new, byte-exact)
- `.ufo/waves/round-30/build/ExecD6Snapshot/snapshot-provenance.json` (new, byte-exact)
- `.ufo/waves/round-30/build/ExecD6Snapshot/manifest.json` (new)
- `.ufo/waves/round-30/build/ExecD6Snapshot.md` (this report)

## Limits

- `audit_receipts.py` is hash-and-path recorded in `manifest.json`, not copied (section-(b)
  audit tooling, outside the snapshot-control measurement chain).
- `snapshots.json` content verified as page text only by sampling its values; the full text was
  not reproduced here (contract forbids copying it into the lane).
- Zero fetches performed; `snapshots.json` staleness vs. current pages is unmeasured.

Tools: none installed or updated.
