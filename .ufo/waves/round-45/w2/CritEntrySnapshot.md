# CritEntrySnapshot — R45 w2 falsify report

Item: corpus/knowledge/evidence-snapshot-coverage-r40.md at
5e8c7ad2f7b8254d83358820286e3d12ca4672d1, every figure and inference; recount from
qcache 974299ae4b5f3bdb808b36a9.txt on disk.

Method/commands (from frozen tree at /tmp/chousa-r45-CritEntrySnapshot/tree):
- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 5e8c7ad2f7b8254d83358820286e3d12ca4672d1 | tar -x -C /tmp/chousa-r45-CritEntrySnapshot/tree`
- `sha256sum /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/974299ae4b5f3bdb808b36a9.txt` → ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c (matches committed counts.json capture_sha256; 10184813 bytes ✓).
- Own Python recount (shown below) over the capture.

My rules: "evidence answers" = every `questions[].answers[]` element (8479 total; no other answer container exists — verified key distribution: four answer shapes, 6511 carry cached_source_url, 1968 do not). empty = key present and value None or strip()=="". web.archive.org link = value matches anchored `^https?://web\.archive\.org/` (this reproduces the lane's 5959; substring `"web.archive.org" in v` gives 5960). real source = non-empty source_url != "Metadata". unanswerable = answer_type=="Unanswerable".

## Counts — verbatim decisive output (my recount)
- records 3068 ✓; questions 7985; answers 8479 ✓
- evidence_with_field 6511 ✓; nonempty 6510 ✓; empty 1 ✓
- answers_without_key 1968 ✓; unanswerable without key 386 ✓ (all 386 Unanswerable answers lack the key)
- answers_with_source_url 8092 ✓; sourced_answers_without_key 1582 ✓; real_source_answers 7572 ✓; real_source_answers_without_key 1491 ✓
- filled_metadata_placeholder 429 ✓; web_archive_wrapping_archive_is_or_md 8 ✓
- claims_with_field 2531 ✓; claims_nonempty 1145 ✓; claims_empty 1386 ✓ (= 1343 None + 43 "")
- empty evidence answer: record index 1175 (0-based), question idx 4, Boolean, source_url "" ✓
- filled_web_archive: mine 5960, committed 5959; filled_not_web_archive: mine 550, committed 551. Exactly one value diverges: `https://web.archive.ohttps://web.archive.org/web/20210729025817/https://www.investopedia.com/articles/markets/120315/if-you-had-invested-right-after-nikes-ipo.aspg/web/20210613214554/https://www.britannica.com/biography/Prince-singer-and-songwriter` — contains the substring "web.archive.org" (twice) but fails the anchored regex. Under substring semantics it is a web.archive.org address; under the anchored rule it falls into the malformed tail. Commit-side 5959 = anchored count, so the figure is definition-bound, not a counting error.

## Inference test
"missing snapshots sit in answers that lack the field and among filled values that are not archive links": holds-narrowed.
- Field-less: 1968 = 386 unanswerable + 1582 sourced (1491 real + 91 Metadata) ✓ part (a).
- Filled non-archive (anchored): 551 = 429 Metadata placeholder (no page; not a missing snapshot) + 77 other-archiver links (41 archive.ph, 27 perma.cc, 6 archive.vn, 2 archive.is, 1 archive.md) + 45 live/malformed. The doc's breakdown names only archive.ph/perma.cc/archive.vn (74) and omits 3 standalone archive.is/archive.md values; the true missing-snapshot tail is ~45, not the implied ~48, and the 74/77 other-archiver values are archive links, not missing snapshots. So the class "filled values that are not archive links" over-includes: only ~45 of 551 are genuinely missing.
- Note: the 8 double-archived web.archive.org values (archive.is/archive.md inside) are counted as web.archive.org links, consistent with the field-level rule.

## Arithmetic sentences
- "99.98%": 6510/6511 = 0.999846 → 99.98% ✓ holds.
- "45.2%": 1145/2531 = 0.452391 → 45.2% ✓ holds.
- "78.7%": 5959/7572 = 0.786977 → 78.7% ✓ holds (5960/7572 = 0.787110 → also 78.7%, so robust to the boundary case).
- "factor of about 2": filled-rate ratio 99.98/45.2 = 2.212. Actual factor is ~2.21; "about 2" is loose but not false. holds-narrowed (precision: 2.2×, not 2×).
- "more than three orders of magnitude (1,386 against 1)": 1386/1 = 1386 = 10^3.14 > 10^3 ✓ holds.

## Verdicts
- All 16 recountable figures: holds, except filled_web_archive/filled_not_web_archive (5959/551 vs my 5960/550) — holds-narrowed, single malformed double-concatenated value whose classification depends on anchored-vs-substring URL rule; the doc's numbers are internally consistent under the anchored rule and the 78.7% is invariant.
- Inference: holds-narrowed — directionally correct; "filled values that are not archive links" over-includes (429 placeholders are not page citations; 77 are other-archiver links), true missing-snapshot tail ≈ 45, and the archiver breakdown omits 3 standalone archive.is/archive.md values.
- Arithmetic: 99.98% holds; 45.2% holds; 78.7% holds; "factor about 2" holds-narrowed (2.21); ">3 orders of magnitude" holds.

Pointers: counts.json values at corpus/evidence/round45/counts.json:24-28 (5959/551); the divergent value is the only cached_source_url failing `^https?://web\.archive\.org/` while containing "web.archive.org"; r40 doc lines 11-13, 20-22. Independent recompute reproducible via the script body in this seat's session (rules stated above); sha256 of capture ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c.
