# ScribeD8 — scoped findings (2026-10-23)
- **Behavior / axes:** Drafted three dated, append-only D8 corrections; no coverage or operability score is claimed.
- **Evidence:** ReviewContractV2 finding 13 and recorded redirect commands support the finding-13 pointer (`round-30-verifier-spotcheck.md:58-60`; `.ufo/waves/round-30/build/ReviewContractV2.md:185-195,237-243`).
- **Evidence:** `differential-receipt.json` records `landed-heldout`, exit 1, 33/33; its network record and `ReviewCorrections.md:25` show 32 allowed GETs, 2 refused, and statuses 27×200, 2×203, 2×301, 1×403 (`round-30-verifier-spotcheck.md:197-198`).
- **Evidence:** D4's abstract came via NCBI E-utilities; the review reports no retained bytes/hash and its registered PubMed GET receipt records HTTP 203, cookie gate, zero quote matches (`ScribeD4H20.md:3`; `ReviewCorrections.md:26`; `receipt-pubmed-17638714.json`).
- **Touched surfaces:** Only drafts/report artifacts. Draft insertion points: `corpus/lessons/round-30.md` after line 67; `SCORECARD.md` after line 1654; `corpus/lessons/round-25.md` after line 269. No production file edited.
- **Fleet-only items:** Carry `7908ce2a` vs `bf657822`, omitted `dad857af`, and `03:52Z` vs commit `03:50:30Z` into the round-31 report; no lane edit (`round-30-verifier-spotcheck.md:194-196`).
- **Gates / limits:** No counters, tests, or network access performed; no tools installed. `timeout 10s mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-31/build/ScribeD8` returned no output; the tool did not surface an exit code. No git/jj writes.
- **Artifacts:** `.ufo/waves/round-31/build/ScribeD8/drafts.md`; `.ufo/waves/round-31/build/ScribeD8.md`.
