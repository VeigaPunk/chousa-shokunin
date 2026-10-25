ATTACKS: six registry rows S085, S090–S094 in corpus/SOURCES.md vs CORPUS.md SOURCES contract v1 (11 cells, kind, tier, status, opened, recheck, used-by exactness, stray pipes, title/venue/year vs captures, S092-vs-S086 duplicate)
VERDICT: holds — no contract violation found. All six rows pass their 11 cells, enums, tiers, status, dates, cadence, exact used-by, and capture-grounded facts. One observation: S092 co-exists with S086 as a second row for the same paper; the lane's gate documents a distinct content rationale (appendix absent from the S086 capture), so it is a row-coherence note, not a defect.

Commands run (all from /home/vgpnk/Projects/shokunin/chousa-shokunin; captures read-only under /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/):

1. awk -F'|' row-split of S085/S086/S090–S094: NF=13 for every row — 11 cells, no stray `|`. awk enum check: kind=dataset/paper (all valid), tier=A, status=mined for all six; no tier-inflation (kind!=community).
2. Frozen census (CORPUS.md lines 135–147): 94 rows; malformed=0; duplicate ids=none; tier A=88 B=1 C=5; status mined=70 queued=19 rejected=5; mined used-by paths all exist (no "missing:" lines). `scripts/sources-census.sh` is not present in this lane root (only .ufo/waves/round-31/build/ExecCensusStart/sources-census.sh); used the frozen awk census instead.
3. used-by exactness: for each id, grep of corpus/knowledge + corpus/lessons:
   - S085: cited by corpus/knowledge/evidence-pool-versioning-r39.md (line 3) and corpus/knowledge/claim-support-test-r37.md (line 3). Row used-by = exactly those two. ✓
   - S090: cited by claim-support-test-r37.md (line 4) only. Row used-by = that one. ✓
   - S091: cited by claim-support-test-r37.md (line 5) only. Row used-by = that one. ✓
   - S092: cited by claim-support-test-r37-amendment-2026-10-23.md (line 3) only. Row used-by = that one. ✓
   - S093: cited by claim-support-test-r37-amendment-2026-10-23.md (line 4) only. Row used-by = that one. ✓
   - S094: cited by claim-support-test-r37-amendment-2026-10-23.md (line 5) only. Row used-by = that one. ✓
   Both entries exist and cite the ids; no lesson/other entry cites any target id as a source row.
4. Title/venue/year/version facts checked against captures:
   - S085 (capture 5a631adb…): "Pre-processed Wikipedia Pages (June 2017 dump)" at char 1271; footer "Build info: refs/heads/live build 385" and "Last updated: 2026-04-02T10:58:13.945736" — both present in capture (lines 162, 295–296).
   - S091 (capture 3749141b…): running head "The Thirty-Eighth AAAI Conference on Artificial Intelligence (AAAI-24)" (capture line 1) — AAAI-24 correct; title "CFEVER: A Chinese Fact Extraction and VERification Dataset" present.
   - S094 (capture a9cf4170…): "Proceedings of the 31st International Conference on Computational Linguistics, pages 1600–1612, January 19–24, 2025" (capture lines 60–62) — COLING 2025 pages 1600–1612 correct.
   - S090 (capture 4132ec1b…): "Findings of the Association for Computational Linguistics: ACL 2026, pages 400–420, July 2-7, 2026" (capture lines 60–62) — correct.
   - S092 (capture b502d4c6…): "arXiv:1803.05355v3 [cs.CL] 18 Dec 2018" (capture line 202) — v3 date correct.
   - S093 (capture 44be8711…): "arXiv:2012.00614v2 [cs.CL] 02 Jan 2021" (capture line 165) — v2 date correct.
5. Anchor char check: python slice at each row's char offset equals the quoted text exactly for all 16 anchors (S085: 2360, 1271; S090: 1526/1576/1669; S091: 966/1567/10406; S092: 2821/2849/6601; S093: 5157/13373/16287; S094: 19167/20462/20650) — all match=True at the stated offset.
6. Opened/recheck: S085–S094 rows opened 2026-10-25 (round-47 write date; captures on disk since 2026-10-23 per mtimes 20:36–20:39; gate states "opened 2026-10-25 from on-disk captures, no fetch" — round-47.md lines 126, 205–210). Assertcheck 365d each; S088 (180d) confirms 365d is an accepted cadence.
7. S092 vs S086: both rows name Thorne et al. FEVER (same work). Gate rationale (round-47.md "Rows added or changed"): "A separate row from S086 by content: the annotation-guideline appendix (A.6, A.7.3) is absent from the S086 NAACL capture"; scopes differ (S086 = measured evidence-selection reliability from publisher PDF; S092 = whether the support test is a specified procedure + validation figure, from arXiv HTML). CORPUS.md has no rule forbidding a second row for the same work (S029/S030/S031/S032/S033 same-work rows are "supersedes" rows because they re-grounded the same claim; S092 is a different claim/scope), so no violation — but note S092 re-reports two figures already carried by S086 (0.6841 Fleiss; 95.42%/72.36%) via the arXiv render, the only cross-row fact overlap.

Residual risk / verification gaps:
- No network fetch (L0 open, no operator approval): venue/page facts verified only against the on-disk captures, not live pages. Captures are authoritative for this lane (gate bound by document).
- `scripts/sources-census.sh` absent from lane root; census run via frozen awk recipe only. Not a defect of the six rows.

Pointers: corpus/SOURCES.md lines 95 (S085), 100–104 (S090–S094); corpus/lessons/round-47.md lines 126–132, 160–176, 205–210; captures under /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/ (5a631adb…, 4132ec1b…, 3749141b…, b502d4c6…, 44be8711…, a9cf4170…).
