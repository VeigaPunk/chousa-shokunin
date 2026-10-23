VERDICT: holds — all 4 files at a9d3a05a show insertions only against a3a3710e, and every checked claim in the D1, D2, D4 and D5 blocks matches its cited file; 3 low findings, 1 nit and 1 note, none changes a count, a score or an admission.

Seat ChousaR30.ReviewCorrections, round 30 wave 2. Read only; no counter, harness or lane production file was run or edited. Tools: git, python3 stdlib, curl, all already installed (nothing installed or updated).

## Append-only check

- `git diff a3a3710e a9d3a05a8fd812a60323b08381019152069581fd --stat -- SCORECARD.md LOG.md corpus/lessons/round-25.md corpus/lessons/round-29.md` exit 0: `4 files changed, 40 insertions(+)`. For each file, `git diff … | grep -E '^-[^-]' | wc -l` gives 0 removed lines.
- Where each block sits: SCORECARD hunk `@@ -1639,6 +1639,32 @@`, which is directly above `## Planned — round 30`. LOG `@@ -1199,3 +1199,7 @@`, round-25 `@@ -261,3 +261,9 @@` and round-29 `@@ -120,3 +120,7 @@` are all at the end of the file.
- The working copy and the tip agree for all 4 files (sha256 of the working file equals sha256 of `git show a9d3a05a:<file>`).

## Claims checked: all match

- **D2 seeds** (SCORECARD and LOG): RerunCounterA `receipt.json` has seed 16442982337510174646. RerunCounterB `receipt-1.json` has 5392061795029416258 and `receipt-2.json` has 1932010155184684229. ScoutFreshnessH `rederive-receipt.json` and `rederive.out:17` have 13173258806708832500. `rederive3.out:17` has 3497534629407128034. Each records 130/130 with counter `cd509650…`, and every file is committed at the tip (`git cat-file -e`).
- **D2 origin text**: the base SCORECARD Round 29 row reads "130/130 in 6 further runs (RerunCounterA, RerunCounterB x2, ScoutFreshnessH x3)", and base `LOG.md:1190` reads "6 more wave-2 runs".
- **D2 run 2**: `ScoutFreshnessH.md:18` gives the run 2 seed 12970099299958901445 and cites `rederive3.out`. `git grep 12970099299958901445 a9d3a05a` finds that seed only in markdown and spec files (ScoutFreshnessH.md, round-30 build reports and specs, LOG, SCORECARD, the spot-check). There is no receipt or `.out` for it, so a count of 5 for the named seats is right.
- **D1** (`DiffToolB/landed-fixture.network.json`): 8 events, each `kind=request, method=GET, allowed=true`, and 8 responses with `status=200`. The `landed-fixture` entry in `differential-receipt.json` has the quoted command and cwd byte for byte, `exit_code` 1, `expected_count` 40, `observed_count` 40, and `QUOTE_REOPEN_SUMMARY verbatim=14 absent=20 too_long=3 no_source=3 unreachable=0`. Top-level `production_bytes_unchanged: true`.
- **D1 other citations**: the cache-only verifier receipts `CriticClaimDesign/offline-snapshot-run{1,2}.json` record 130/130 and are committed. `corpus/QUALITY.md:181` is criterion 26. `ScribeD1Liveness/drafts.md:19` is section B ("Case-insensitive `live` grep inventory"). `round-29-verifier-spotcheck.md:143-147` is D1 and `:148-150` is D2.
- **D4**: base `corpus/lessons/round-25.md:70`, under `## Gate — sources opened this round` (line 59), reads "A signal occurred within 2 years for 23% of reviews and within 1 year for 15%." That fits "casing error, omits However," and `ScoutFreshnessH.md:89` (h20, ABSENT). At the tip, `SOURCES.md:31` is S021 with status queued, and `:42` is S032 ("supersedes S021", status queued).
- **D5**: `corpus/evidence/round29/claims.md:13` holds the quoted phrase. In `CtlCasefoldNoBoundary/report.md`, lines 123-145 run from the "Pristine detector output" heading to the closing fence and include `QUOTE_REOPEN_MATCH=82/82`. The adjacent `receipt.json` is 78/82 on the v1 counter `fc219ef8…`, seed 2901, and is the mutant result (report line 25).
- **D5 times**: the `at` fields of the MutateCounter receipts run from `2026-10-23T01:25:59Z` to `01:27:45Z`, matching `MutateCounter.md:43`. The v3 freeze `aa5e1a31` was committed at `2026-10-22T22:28:23-03:00`, which is 01:28:23 UTC. `CriticClaimDesign.md:13-28` holds the timeline table and the qualification.

## Findings

1. **Low, D2 scope (LOG wording).** LOG says "Committed evidence supports 5 further runs at 130/130" with no scope. Committed wave-2 evidence also holds 12 more 130/130 receipts of `python3 tools/quote-reopen.py verify` on counter `cd509650…`: the baseline and pristine receipts of MutInlineBlock, MutOrder, MutCasefold, MutQuoteMap, MutSkipScript and MutBoundary (for example `MutOrder/receipt-pristine.json`, seed 13704728832739408635, at 01:51:12Z). The count of 5 is right only for the 4 seats the round-29 row names. Since it is an undercount, no score changes; the fix would be to say "of the named re-run seats".
2. **Low, D1 "that one DiffToolB run only".** `DiffToolB/landed-heldout.network.json` records a second network-recorded run of the landed tool. It has 32 allowed GETs and 2 refused ones, and its responses are 27 with status 200, 2 with 203, 2 with 301 and 1 with 403 (33 items, `differential-receipt.json` run 2). The SCORECARD block and the drafts inventory leave this run out. That understates the evidence; it does not overstate it.
3. **Low, D4 provenance.** The corrected verbatim text comes from a reader shortcut through NCBI E-utilities (`ScribeD4H20.md:3`). `git grep -i eutils a9d3a05a -- corpus/SOURCES.md` finds 0 rows, so that host is not registered, and no response bytes or hash were kept. My GET to the registered URL returned HTTP 203 with the cookie gate (body sha256 `0265ca42…3ff9c`, 0 matches for the quote; receipt `.ufo/waves/round-30/falsify/ReviewCorrections/receipt-pubmed-17638714.json`). So the corrected text is not confirmed by a fetch of a registered URL. HeldOut07 (`HeldOut07.md:50`, also through E-utilities) and `ScoutFreshnessH.md:89` give the same wording [INFERENCE: the text is likely right, but it has no receipt].
4. **Nit, D1 prose.** In SCORECARD, the `[INFERENCE]` tag is attached to a directive ("Keep the row's counter result distinct …"), not to an inference.
5. **Note, not a defect.** The D1 block does not name the frozen `corpus/evidence/round29/claims.md:41-42` ("live"). The inventory it cites covers that line (`drafts.md` section B, line 21: opened, frozen, unchanged).

## Gaps

- I did not re-run any counter. The D2 and D5 checks rest on committed receipts and git metadata only.
- I made 1 network request, a GET to a registered URL: `https://pubmed.ncbi.nlm.nih.gov/17638714/`, with exit 0 and HTTP 203, and no redirects followed.
- The only processes I started were short foreground commands, and none is still running.
