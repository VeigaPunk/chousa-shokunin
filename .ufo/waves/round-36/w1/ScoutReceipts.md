# ScoutReceipts — committed measure catalog

Access date: 2026-10-23. Lane tip `git rev-parse master` = `git rev-parse HEAD` = `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`. Worktree blobs of the eight receipts equal those `master` blobs (`git hash-object` = `git rev-parse master:<path>`). `git status --porcelain` on `measure/`, `tools/research-gate.sh`, and `controls/` printed nothing.

The brief says 11 committed receipts. The tree has **8**. No ninth path exists under `.ufo/waves/round-36/measure/` (directory listing and `git ls-tree -r --name-only master`).

Pins checked with `sha256sum` (both match the brief):

| role | path | sha256 |
|---|---|---|
| landed gate | `tools/research-gate.sh` | `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` |
| base control | `.ufo/waves/round-36/controls/base-gate-r36.sh` | `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` |
| claim witness | `tools/argv-witness.py` | `e6832e0b9cbbdfae9da823528cc0a6218a6af7d8ed7e5864378713df2e19107e` |
| r35 witness | `tools/mechanism-witness.py` | `9f537bfde0dd53f2240af149e1b7a03fd0a0f372ee1fa1a32e94044115a252b3` |
| stub-pass | `.ufo/waves/round-36/controls/ctl-c2-stub-pass.py` | `ee0e0cc7d38a191443e948daeed3bfe3b9bc8b474d61114dcaeeeb75ca86fbb7` |
| stub-fail | `.ufo/waves/round-36/controls/ctl-c2-stub-fail.py` | `c8dab587d553b477560457e6d45d2cf2569310e0d66e389646c2c5788d871dfb` |

Each receipt's `witness_sha256` equals the `sha256sum` of the file named in its `witness` field.

## Table

Top-level fields only. `gate_sha256` below is the receipt's scored gate, not variant-engine hashes nested under `variants.*.gate_sha256`.

| file | seed | gate_sha256 | label | total/matched | predicate_holds | scored against |
|---|---:|---|---|---|---|---|
| `c1-after-s36001.json` | 36001 | `a7d3922c…1f54e8` | `ENGINE_SWAP_CANARY=14/14` | 14/14 | true | landed `research-gate.sh` |
| `c1-after-s36011.json` | 36011 | `a7d3922c…1f54e8` | `ENGINE_SWAP_CANARY=14/14` | 14/14 | true | landed `research-gate.sh` |
| `c1-before-s36001.json` | 36001 | `a4768851…0c38ad` | `ENGINE_SWAP_CANARY=10/14` | 14/10 | false | **base** `base-gate-r36.sh` |
| `c2-after-s36001.json` | 36001 | `a7d3922c…1f54e8` | `WITNESS_PER_RECORD=5/5` | 5/5 | true | landed gate + `argv-witness.py` |
| `c2-after-s36011.json` | 36011 | `a7d3922c…1f54e8` | `WITNESS_PER_RECORD=5/5` | 5/5 | true | landed gate + `argv-witness.py` |
| `c2-before-legacy-s36001.json` | 36001 | `a4768851…0c38ad` | `WITNESS_PER_RECORD=2/5` | 5/2 | false | **base** `base-gate-r36.sh` + `mechanism-witness.py` |
| `c2-stubfail-s36001.json` | 36001 | `a7d3922c…1f54e8` | `WITNESS_PER_RECORD=5/5` | 5/5 | false | landed gate + **stub** `ctl-c2-stub-fail.py` (`landed_attrib=fail`, `renamed=fail`) |
| `c2-stubpass-s36001.json` | 36001 | `a7d3922c…1f54e8` | `WITNESS_PER_RECORD=0/5` | 5/0 | false | landed gate + **stub** `ctl-c2-stub-pass.py` |

Full hashes and git blobs: `.ufo/waves/round-36/w1/ScoutReceipts/receipt-table.json`.

## Before cross-check

Both `before` receipts store `gate_sha256` `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` and `gate` `…/controls/base-gate-r36.sh`. That string equals `sha256sum` of the control file on this tip. Neither before receipt is pinned to the landed gate.

`c1-before-s36001.json` pass map: S1–S10 true, S11–S14 false (`S11-manifest-hash-shim`, `S12-locale-c`, `S13-pin-echo-isolation`, `S14-pin-drift-token`). Both `c1-after` receipts pass all fourteen, and their pass maps are identical. That matches `corpus/evidence/round36/claims.md` lines 52–58 (accessed 2026-10-23).

`c2-before-legacy-s36001.json`: `matched=2`, `output_equiv=5`, `landed_attrib=absent`, `renamed=fail`. Variant witness results: V1 fail, V2 pass, V3 pass, V4 fail, V5 pass, V6 `unparseable`. Witness bytes are `mechanism-witness.py` (`9f537bfd…`), not `argv-witness.py`.

## Other bytes

Receipts whose **gate** sha is not the landed gate (both are the base control, not an unknown file):

- `c1-before-s36001.json` → `base-gate-r36.sh`
- `c2-before-legacy-s36001.json` → `base-gate-r36.sh` (witness is the other file: `tools/mechanism-witness.py`)

Receipts on the landed gate whose **witness** is not `argv-witness.py`:

- `c2-stubpass-s36001.json` → `ctl-c2-stub-pass.py` (`ee0e0cc7…`)
- `c2-stubfail-s36001.json` → `ctl-c2-stub-fail.py` (`c8dab587…`)

**No receipt has a top-level `gate_sha256` matching neither known gate.** Nested `variants.*.gate_sha256` values are patched-engine identities inside a scored run; they were not treated as the receipt pin.

## Lowest count against the landed gate

Landed gate = `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`.

- C1 (`matched`): 14 and 14. Lowest **14**.
- C2, claim witness `argv-witness.py` only: 5 and 5. Lowest **5**. Both `predicate_holds=true`, `output_equiv=5`, `landed_attrib=pass`, `renamed=pass`.
- C2, every landed-gate receipt including the two disclosed stubs: 5, 5, 5, and **0**. Lowest **0**, from `c2-stubpass-s36001.json`. `predicate_holds` is false there. `claims.md` lines 114–117 name that control and the 0/5 score. It is not a P2 pass and not a witness bypass: the stub answers pass for V1–V6, so separation is 0 while output stays 5/5.

## Kill-rule reading

Claim instruments (landed gate, and for C2 the claim witness): **no committed run against the landed gate is lower than 14 (C1) or 5 (C2).**

Literal min over every committed receipt whose `gate_sha256` is the landed gate: C1 stays 14; C2 drops to 0 because `c2-stubpass-s36001.json` is committed. The sentence "no committed run against the landed gate is lower than 5" is false if that disclosed stub counts. It does not meet P2 (`predicate_holds=false`). [INFERENCE] The freeze text at `claims.md` lines 96 and 114–117 treats the stub as a control that skips the claimed work, not as a claim measurement. This catalog did not re-run either counter.

Not a MEETS. No committed receipt shows an output-equivalent engine still scoring 14/14, or a witness substitution that prints P2 with `predicate_holds=true`.

## Commands

1. `sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh && echo "---" && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD && echo "--- files ---" && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin ls-tree -r --name-only master -- .ufo/waves/round-36/measure/` — exit 0. Deciding lines: the two gate hashes above, tip `700bd5fcbf9abc118a6a0f078d51a2e7460c2878` twice, eight `measure/` paths.

2. `python3` over the eight JSON files printing top-level `seed`, `gate_sha256`, `label`, `matched`, `total`, `predicate_holds` (and nested witness/variant scalars). Exit 0. Deciding lines: the eight rows in the table.

3. `sha256sum` of `argv-witness.py`, `mechanism-witness.py`, `ctl-c2-stub-pass.py`, `ctl-c2-stub-fail.py`, `research-gate.sh`, `base-gate-r36.sh`; then `git status --porcelain` on those paths, `git log -1 --format='%H %s' -- .ufo/waves/round-36/measure`, `git ls-tree -r master -- .ufo/waves/round-36/measure`, and `wc -l` of the name list. Exit 0. Deciding lines: witness hashes equal receipt `witness_sha256`; porcelain empty; `700bd5fc… round-36 freeze: …`; count `8`.

4. `python3` printing each C1 scenario `pass` flag and each C2 `witness` path plus per-variant `witness`/`output_match`; then `git hash-object .ufo/waves/round-36/measure/*.json` and `git rev-parse master:<each receipt>`. Exit 0. Deciding lines: before fails only indexes 10–13; both after receipts all true; eight hash-object ids equal the eight `master` blob ids.

5. `python3` printing scenario names and the before-vs-after index diff. Exit 0. Deciding line: `before vs after differ at [11, 12, 13, 14]`; `after seeds identical pass map True`.

6. `mkdir -p …/w1/ScoutReceipts` — exit 0. `sha256sum …/w1/ScoutReceipts/receipt-table.json` — exit 0. Deciding line: `226eadc58472b011f08b50c723551586bc29434d273463a58e69bab351675f76`.

## Files opened

2026-10-23: `.ufo/waves/round-36/w1-briefs/ScoutReceipts.md`; `corpus/evidence/round36/claims.md`; all eight `.ufo/waves/round-36/measure/*.json` (parsed in full; headers of `c2-before-legacy-s36001.json`, `c2-stubpass-s36001.json`, `c2-stubfail-s36001.json` also read); `sha256sum` only (contents not read) of `tools/research-gate.sh`, `.ufo/waves/round-36/controls/base-gate-r36.sh`, `tools/argv-witness.py`, `tools/mechanism-witness.py`, `ctl-c2-stub-pass.py`, `ctl-c2-stub-fail.py`. `grep` hit `.ufo/waves/round-36/gen-w1-spec.py` (the "11 committed receipts" string) without a full read.

## Artifacts

| path | sha256 |
|---|---|
| `.ufo/waves/round-36/w1/ScoutReceipts/receipt-table.json` | `226eadc58472b011f08b50c723551586bc29434d273463a58e69bab351675f76` |

No installs. Counters were not re-run.

**Verdict: catalog holds — 8 committed receipts, not 11; no top-level gate_sha256 outside the two known gates; both before receipts match `a4768851…` / `base-gate-r36.sh`; no committed claim-instrument run against the landed gate is lower than 14 (C1) or 5 (C2); the only lower landed-gate count is disclosed stub-pass at 0/5 with `predicate_holds=false`.**
