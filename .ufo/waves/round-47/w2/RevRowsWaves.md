ATTACKS: Round-47 registered Gates-row entry/verdict-map cells for mask-gate, receipt-binding, slen-probe, and mechanism-witness; ran entries against an archive of lane tip `1fc5ed193ad48a482402c862f4e4cc47e46d5b2d`.
VERDICT: holds

## Results

No false verdict-map or self-test cells found in the four assigned rows. Their entry scripts' failure/success exit behavior and the specified control/self-test outcomes reproduced. The row measurements are historical measurements at `a15610a…`; they should not be read as counts over current tip's expanded tree.

## Commands and decisive output

Commands below ran in `/tmp/chousa-r47w2-RevRowsWaves/tree`, extracted using `git archive 1fc5ed193ad48a482402c862f4e4cc47e46d5b2d`; `LC_ALL=C` for counter runs. No network or installation.

- `sha256sum .ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh corpus/evidence/round33/c1-count-v2.py .ufo/waves/round-34/w1/ExecE2Counter/c1-count-v3.py .ufo/waves/round-34/w1/ExecE4Census/receipt-binding.py .ufo/waves/round-35/repairs/slen-probe.sh tools/mechanism-witness.py tools/research-gate.sh`
  - `ae7d4bfc7ac1d262590dd5014e8abdbbea102266551891b4910666116440e0cd` mask-gate (row's `ae7d4bfc…40e0cd`)
  - `cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514` v2 counter (`cb354dd1…`)
  - `bd81aeea199c460be3afbec0f15116b5ddfe8330b45f35b37568d1665e43d9cc` v3 counter (`bd81aeea…`)
  - `230441acc1103d350780507c36993d87d550ea4b6602a373ad081dcf744c5943` receipt-binding (`230441ac…5943`)
  - `0938c4c21e9b4e311a6786204f954a6a7351e861c3597db665db0ce47988ce60` slen-probe (`0938c4c2…ce60`)
  - `9f537bfde0dd53f2240af149e1b7a03fd0a0f372ee1fa1a32e94044115a252b3` mechanism-witness (`9f537bfd…52b3`)
  - `2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34` landed research-gate (`2cb04bdd…fc34`)
- `bash .ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh` → `research-gate: record path required ...`; usage header; `rc=2` (the row's bare-invocation behavior).
- `python3 .ufo/waves/round-34/w1/ExecE4Census/receipt-binding.py` → argparse required `repo, receipts`; `rc=2`.
- `bash .ufo/waves/round-35/repairs/slen-probe.sh` → `line 16: $1: unbound variable`; `rc=1`.
- `bash .ufo/waves/round-35/repairs/slen-probe.sh /nonexistent-gate.sh` → `slen-probe: gate not found: /nonexistent-gate.sh`; `rc=2`.
- `bash .ufo/waves/round-35/repairs/slen-probe.sh tools/research-gate.sh` → `SLEN_PROBE offsets=1 first=5`; `rc=0`.
- `bash .ufo/waves/round-35/repairs/slen-probe.sh .ufo/waves/round-35/repairs/base-gate.sh` → `SLEN_PROBE offsets=0 first=`; `rc=1`.
- `python3 tools/mechanism-witness.py --gate /nonexistent-gate.sh` → `mechanism-witness: gate not found: /nonexistent-gate.sh`; `rc=2`.
- `timeout 60 python3 tools/mechanism-witness.py --gate tools/research-gate.sh --seed 4741` → `WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1 (long records=8)`; `rc=0`.
- `python3 corpus/evidence/round35/c2-count.py --gate tools/research-gate.sh --battery tools/mechanism-witness.py --seed 4741` → `WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass`; K1 and K2 each `output=9/9 witness=fail stamps={'chunk': 0, 'direct': 1}`; `counter_rc=0`.
- `python3 corpus/evidence/round33/c1-count-v2.py --gate .ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh --seed 4733 --receipt /tmp/chousa-r47w2-RevRowsWaves/maskv2-4733.json` → `TOPLEVEL_FIELD_MATCH=156/156`; `rc=0`.
- `python3 .ufo/waves/round-34/w1/ExecE2Counter/c1-count-v3.py --gate .ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh --seed 4733` → `TOPLEVEL_FIELD_MATCH=154/156`, `S2_nested_confusers 4/6`; `rc=1`.
- Same v3 counter with `--seed 9401` → `TOPLEVEL_FIELD_MATCH=155/156`, `S2_nested_confusers 5/6`; `rc=1`.
- Receipt census was run after initializing/committing the archive copy as a temporary local checkout (the script requires a git checkout): `python3 .ufo/waves/round-34/w1/ExecE4Census/receipt-binding.py "$PWD" "$PWD/.ufo/waves/round-33"` → `TOTAL_RECEIPTS 1060`, `TOTAL_UNBOUND 24`, `TOTAL_UNBOUND_LANDED_FINAL 19`; `rc=1`. For round-34: same command with receipts dir `.ufo/waves/round-34` → `TOTAL_RECEIPTS 478`, `TOTAL_UNBOUND 10`, `TOTAL_UNBOUND_LANDED_FINAL 0`; `rc=0`. Current-tip round-33 totals differ from row's pinned historical `a15610a…` measurement because the archive tree includes later additions; the decisive failure/pass verdicts agree. Synthetic checkout's blob totals are not comparable to the historical clone's blob totals.

## Pointers

- `SKILL.md:100` mechanism-witness; `SKILL.md:124` mask control; `SKILL.md:125` receipt-binding; `SKILL.md:126` slen-probe.
- Entry hashes above identify the exact archived files. No actionable defect in the assigned row cells.
