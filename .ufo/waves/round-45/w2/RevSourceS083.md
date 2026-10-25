# S083 review — holds

**Item:** `corpus/SOURCES.md:93` in committed tree `5e8c7ad2f7b8254d83358820286e3d12ca4672d1`; claim: S083 supports that evidence pages are cached, claim URLs are not said to be, and guideline 8 warns of double-archived links that yield archive.org 404s. Verdict: **holds**. No actionable overclaim found in the scoped cell.

## Evidence / commands

1. `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 5e8c7ad2f7b8254d83358820286e3d12ca4672d1 | tar -x -C /tmp/chousa-r45-RevSourceS083/tree` → `EXTRACTED`.
2. `read corpus/SOURCES.md:90-94` in that archive: row S083 is line 93 and has 11 pipe-delimited cells. Anchor cell says: `data collection: "we cache all pages used as evidence in the internet archive" (capture char 14575); on-disk capture, no fetch, span committed`.
3. Python `str.find` on `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/412b146a2720ce6557268d05.txt` for the exact 11-word anchor → `find offset: 14575`; `words in quote: 11`. Context: `To avoid sources disappearing from the web, we cache all pages used as evidence in the internet archive ... https://archive.org .` Capture SHA-256: `a3ff65e0db9cc4f2178932ce53965e4cba60c6aab0ba3b1d4ce40020a8a7cf8f`, matching `spans.tsv` S083 capture digest.
4. `read corpus/evidence/round45/spans.tsv` → S083-1 offset `14415`, S083-2 offset `120724`; quotes are respectively `we cache all pages used as evidence in the internet archive` and `Archive.org returns a 404 page for these`.
5. `grep` on capture for `(?i)guideline 8|double.archiv|404|claim url|claim_?url|original claim` finds the warning at capture lines 3965-3967: fact-checking articles stored on archive.org; double-archived links using archive.org and archive.is; archive.org returns a 404; copy-paste the archive.is part. This substantiates the warning/404 clause. The annotation-guideline context is explicit in that section (the captured text follows the annotation-guideline section); it does not say the evidence-page cache statement applies to claims.
6. `grep` on the capture for `(?i)claim[^\n]{0,100}(archive\.org|archive\.is|internet archive|wayback|cached|cache)|(?:archive\.org|archive\.is|internet archive|wayback|cached|cache)[^\n]{0,100}claim` → `No matches found.` Broader search for archive/cached/Wayback surfaces the evidence-page caching statement and the fact-checking-article warning, but no sentence saying claim URLs ARE archived. Thus the cell's careful “claim URLs are not said to be” is supported as a bounded statement about what this capture says, not an assertion they are never archived.
7. Hashes: SOURCES.md `1b53080660abcc64b79c6421fb3280ef5b7acc2836c3804bb9db1ece1149d384`; S083-1 span `69d724c425ec49ecb0ea67b79593ecf0031c63ac8b0cf9b92c77c281b883395e`; S083-2 span `831d88ef7b9052552b5171bf9f1e8970d9bae38be3c5a9fb3d343bd648d8182c`.

## Residual risk / verification gaps

Capture text has extraction artifacts (including the displayed guideline number/diacritics), and no live target was fetched as required. This review confirms only the committed S083 source-row claim against its supplied capture and spans; it does not establish whether archive links resolve now or whether other entries/counters hold. No tools installed. Scratch extraction is under `/tmp/chousa-r45-RevSourceS083/tree`.
