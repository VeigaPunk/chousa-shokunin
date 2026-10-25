# R45 W2 — independent counts and span-builder falsification

## Item
`corpus/evidence/round45/counts.json` extra and frozen count keys, plus reproducibility of `build-spans.py`'s outputs at lane commit `5e8c7ad2f7b8254d83358820286e3d12ca4672d1`.

## Method and decisive output
Extracted that commit with `git archive` to `/tmp/chousa-r45-ExecExtraCounts/tree`; read the train.json capture at `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/974299ae4b5f3bdb808b36a9.txt`. Wrote and ran an independent Python recount (no import of `build-spans.py`); it enumerated answer/claim fields directly from JSON and compared every key in both maps against committed `counts.json`.

Verbatim decisive recount output:
```
capture_bytes computed: 10184813 | committed: 10184813
capture_sha256 computed: ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c
capture_sha256 committed: ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c
sha256 match: True
counts.records = 3068 [OK] committed=3068
counts.evidence_with_field = 6511 [OK] committed=6511
counts.evidence_nonempty = 6510 [OK] committed=6510
counts.evidence_empty = 1 [OK] committed=1
counts.claims_with_field = 2531 [OK] committed=2531
counts.claims_nonempty = 1145 [OK] committed=1145
counts.claims_empty = 1386 [OK] committed=1386
extra_not_frozen.answers = 8479 [OK] committed=8479
extra_not_frozen.answers_without_key = 1968 [OK] committed=1968
extra_not_frozen.answers_without_key_unanswerable = 386 [OK] committed=386
extra_not_frozen.answers_with_source_url = 8092 [OK] committed=8092
extra_not_frozen.sourced_answers_without_key = 1582 [OK] committed=1582
extra_not_frozen.real_source_answers = 7572 [OK] committed=7572
extra_not_frozen.real_source_answers_without_key = 1491 [OK] committed=1491
extra_not_frozen.real_source_answers_web_archive = 5959 [OK] committed=5959
extra_not_frozen.filled_web_archive = 5959 [OK] committed=5959
extra_not_frozen.filled_not_web_archive = 551 [OK] committed=551
extra_not_frozen.filled_metadata_placeholder = 429 [OK] committed=429
extra_not_frozen.web_archive_wrapping_archive_is_or_md = 8 [OK] committed=8
ALL MATCH
```

Then ran `python3 /tmp/chousa-r45-ExecExtraCounts/tree/corpus/evidence/round45/build-spans.py /tmp/chousa-r45-ExecExtraCounts/buildrun` with an empty `corpus/evidence/round45/` in the scratch root. Exact output:
```
spans 4 counts {'records': 3068, 'evidence_with_field': 6511, 'evidence_nonempty': 6510, 'evidence_empty': 1, 'claims_with_field': 2531, 'claims_nonempty': 1145, 'claims_empty': 1386}
exit=0
```
Compared `counts.json`, `spans.tsv`, and `spans/` to the committed archive tree using `diff -u`/`diff -ru`:
```
counts_diff_exit=0
tsv_diff_exit=0
spans_dir_diff_exit=0
```
SHA256 pairs (committed then rebuilt; each pair identical):
```
counts.json  ded8747ef8e7b23c5246e0d3613a539c6506a691799635aa7429313405d9665c
spans.tsv    fbb6862c6ca4a0477a31eeb6421f244829fe593fc37f65e220a69d47d9f380ac
S082-1.txt   0ff6a4ef44c066e9f1d9820da2e8f56bbdd02af0f236e286d919dc00170af3a2
S082-2.txt   ec4156d84760c004a737058775511fbdf9bdd0e027353de0127043d01c7ca796
S083-1.txt   69d724c425ec49ecb0ea67b79593ecf0031c63ac8b0cf9b92c77c281b883395e
S083-2.txt   831d88ef7b9052552b5171bf9f1e8970d9bae38be3c5a9fb3d343bd648d8182c
```
Scratch was removed (`scratch removed`). No tool installs.

## Verdict
**holds** — the independent recount agrees on every `counts` and `extra_not_frozen` key and capture identity; rebuilding all four spans, manifest, and counts from the specified cache reproduces the committed files byte-for-byte. No defect observed in this assigned item.

## Pointers
- `corpus/evidence/round45/counts.json`: counts lines 7–15; extra lines 16–29.
- `corpus/evidence/round45/build-spans.py`: capture/quote construction lines 33–55; count derivation lines 57–93.
- Capture SHA256: `ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c`.
- Committed `counts.json` SHA256: `ded8747ef8e7b23c5246e0d3613a539c6506a691799635aa7429313405d9665c`.
- Committed `spans.tsv` SHA256: `fbb6862c6ca4a0477a31eeb6421f244829fe593fc37f65e220a69d47d9f380ac`.
