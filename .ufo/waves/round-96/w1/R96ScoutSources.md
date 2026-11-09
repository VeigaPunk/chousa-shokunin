# R96ScoutSources — source re-open and frontier scout (round 96)

Seat: `R96ScoutSources`. Tree attacked: freeze **F** `2db151c5ea0883de0b9dc8d95c6fac1755e1056a`
(clone of the lane at F, plus the lane's later F2 re-freeze `e91f82fe`, which I also read).
Scratch (now deleted): `/fast/scratch/hyaku/chousa-r96/R96ScoutSources`.
Receipts in this directory, all prefixed `R96ScoutSources-`.

## Verdict summary

| claim | verdict | one line |
|---|---|---|
| C1 `C1-SELFTEST-R96` | **held** | the amended F2 sentence is true as written; every predicate and every instrument reproduces |
| C2 `C2-ENTRY-R96` | **fired** | the F2 sentence's "read as one sentence from the reading-order text form" is false for the group the entry itself defines, and the wave's own cited receipt says so |

## 1. Re-open of S223 and S224 (the seat's named item)

Both URLs were re-opened read-only into seat scratch with one `curl -sSL` GET each, exactly as the
round's egress table allows a wave seat to do.

| source | URL | http | raw sha256 | `pdftotext -layout` sha256 |
|---|---|---|---|---|
| S223 | `…/jchla/index.php/jchla/article/download/28195/20695/73210` | 200 | `0bcdbf0e…a83606` | `ce72c920…f02243` |
| S224 | `https://jmla.pitt.edu/ojs/jmla/article/download/962/1274` | 200 | `07036f03…d9ec2` | `86f1aacd…3871` |

All four digests equal the `refetch.tsv` round-96 rows (S223 row 194, S224 row 196) **and** the committed
`corpus/captures/*.raw` and `*.txt` bytes. The re-opened bytes are byte-identical to what the lane holds:
nothing drifted. (`R96ScoutSources-reopen-hashes.txt`, `R96ScoutSources-refetch-compare.txt`)

## 2. S223's bibliographic cells, verified from the bytes

All confirmed from the re-opened PDF, not from the registry row (`R96ScoutSources-s223-bibliographic.txt`):
authors **Sampson, McGowan, Salzwedel, Cogo, Lefebvre** (byline, p.98); title **"PRESS: Peer Review of
Electronic Search Strategies 2015 Updated Guideline Statement"**; **JCHLA / JABSC vol. 37 (2016), pages 96–100**
(5 PDF pages; running head `JCHLA / JABSC Vol. 37, 2016`; `pdfinfo` title `JCHLA_A_201619_O 96..100`);
**doi 10.5596/c16-019** (page footer); and the **PRESS abstract occupies printed pages 98–99** — byline and the
Results paragraph start on 98, the MEDLINE/translation sentences and the Discussion paragraph on 99.

## 3. C2 — the finding that fires

**The F2 sentence and the entry both say the located-quote fragment groups "are read as one sentence from the
reading-order text form" (`pdftotext` without `-layout`). That is false for one group — and the wave's own
cited receipt already records it.**

Measured by joining each group and testing contiguity in the reading-order text (`R96ScoutSources-fragment-order.txt`):

```
L19-L23          contiguous_in_reading_order   TRUE
L31+L24-L25      contiguous_in_reading_order   FALSE   gaps=[0, 5]
                                                            intervening: 'LIGHTNING TALKS / PRÉSENTATIONS ÉCLAIR'
L26-L29          contiguous_in_reading_order   TRUE
L32+L30          contiguous_in_reading_order   TRUE
```

`L31 with L24-L25` is the entry's **own** group for the timing sentence (`"Survey respondents and forum
participants recommended that peer review should occur after the MEDLINE search"` + `"…after the MEDLINE search"`
+ `"has been developed but before other database searches are"`). In the reading-order form the running header
`LIGHTNING TALKS / PRÉSENTATIONS ÉCLAIR` (5 words) sits between L24 and L25 there too, so the reading-order form
does not yield one sentence either — the header must be dropped.

Two supporting facts, both from the wave's own artifacts:
- `.ufo/waves/round-96/w1/R96ExecWrap-fragment-adjacency.txt` — the receipt the entry cites for this — records
  `concat_in_reading_joined=False` for L24-L25, and carries **no row at all** for the two groups F2 added
  (`L31 with L24-L25`, `L32 with L30`).
- The entry's own "Text forms" paragraph (line 23–24) still says **"30/30 measured by `R96ConnectorSiblings`"**,
  while the F2 entry holds **32** located quotes; `R96ConnectorSiblings-f3-quote-locator.txt` likewise reports
  `quotes=30`. The two added quotes (L31, L32) were never covered by that measurement.

So the F2 C2 named limit (d) — *"fragment groups are read as one sentence from the reading-order text form"* —
states more than the cited instrument supports for one of the ten groups, and the entry's evidence line
under-counts its own table. Repair: state that this group crosses the running header in the reading-order form
too (as it already does for the layout form), and update the `30/30` measurement line to 32/32.

Note this does **not** make the located quotes wrong: each of the 32 quotes remains a substring of one capture
line, and K3 does not fire. Measured independently: 32/32 quotes are single-line substrings of their stated
capture; only L1 occurs on two lines (Table 1 checklist at line 303 and the ITEM 14 explanation at line 849),
which the "one line" property does not deny.

## 4. C2 — everything else holds

- `gate-records.py verify` → `records=33 ok=33 fail=0`, exit 0.
- `research-gate.sh verify-metadata` → `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`, exit 0.
- `search-rerun.py verify` → `rev_match=8/8`, `SEARCH_RERUN: CLEAN`, exit 0.
- `entry-controls-r96.py` → `ENTRY_CONTROLS=PASS`, exit 0, with
  `GATE_RECORDS=33/33 LQ_BOUND=32/32 WARRANTS_OK=8/8 WARRANT_TERMS=8/8 LANE_FILLED=8/8`.
- I recomputed all **8** recorded searches myself at base `bbf64970` with GNU grep 3.12: every count and every
  set reproduces exactly, and Q4's digest matches byte-for-byte
  (`R96ScoutSources-searches-recompute.txt`).
- The Located-quotes table is a true multiset of the 32 quoted records, and every quote's stated source is right:
  I checked each of the 32 against its named capture — 32/32 present in the named capture, 0 present in the other.
- The registry is append-only: `git diff bbf64970..F2 -- corpus/SOURCES.md` removes **no** line; S222's row is
  byte-identical (same md5 of its source/status/opened/recheck/used-by cells).

## 5. C1 — the amended F2 sentence holds, and I checked the part it concedes

- `--selftest` → `SEARCH_RERUN_SELFTEST: PASS cases=32/32`, exit 0.
- The battery → `POSITIVE=1/1 DO_NOTHING_REFUSED=1/1 MUTANTS_KILLED=23/23 ORACLES_REJECTED=3/3 NO_WRITE=1/1
  REGRESSION_R95=2/2 CASES=32`, `SELFTEST_CONTROLS=PASS`, exit 0 (I ran it in full; 574 s).
- The base tool exits 2 on `--selftest` ✓. The 23 mutants all exit 1 ✓ (my own run: 23 KILLED, 0 SURVIVED).
- **The F2 parenthetical is true, and I reproduced it rather than taking it on faith** (`R96ScoutSources-a1-shim-check.txt`):
  I built the exact shim the sentence describes — `verify` keeps `evaluate`'s lines but discards its verdict — and
  (a) the shim **passes** `--selftest` 32/32 (so the self-test does not check that `verify` uses the verdict),
  while (b) the round-95 battery inside the REGRESSION leg **fails** it (`FORGERY_REFUSED=0/10`, `RERUN_CONTROLS=FAIL`,
  exit 1). The sentence says exactly this.
- K4 (F2) scope: by a `sys.addaudithook` over the whole `--selftest` run, there are **zero** file writes, **zero**
  subprocess spawns and **zero** socket events; the only non-stdlib opens are the tool reading itself. The same
  selftest passes with an empty `PATH`, so no `git` is invoked (`R96ScoutSources-k4-audit.txt`).

## 6. Two receipts the wave's artifacts cite but that are not in the tree

`corpus/lessons/round-96.md` cites two receipt paths that do not exist
(`R96ScoutSources-missing-receipts.txt`):

- `corpus/evidence/round96/census-end.txt` — cited for "223 rows"; **MISSING**.
- `corpus/evidence/round96/after-f2/lesson-gate.txt` — cited as the landing receipt of
  `gate-records.py verify … corpus/lessons/round-96.md`; **MISSING**.

Every other round that ships a `census-start.txt` also ships `census-end.txt` (rounds 53–59, 90–95); round 96
ships only the start. **The substance of both claims is true** — I re-ran the census at the F2 tree (exit 0, 223
rows, the one new `W04` is S224's) and `gate-records` on the lesson (`records=3 ok=3 fail=0`, exit 0). What is
missing is the receipt file each cites, so the cited paths do not resolve for a verifier.

## 7. Frontier — open routes and version/erratum status (search only, no GET)

My seat may GET only the two URLs my item names, so everything below is a **lead**, not fetched
(`R96ScoutSources-frontier-leads.txt`):

- The CADTH/CDA-AMC E&E PDF — the *same* URL the lane fetched and got 403 on — is search-indexed and quoted in
  full; a plain GET may succeed where the campaign UA was refused:
  `https://www.cda-amc.ca/sites/default/files/pdf/CP0015_PRESS_Update_Report_2016.pdf`.
- The same E&E is mirrored and search-indexed by CORE: `https://core.ac.uk/download/pdf/82048291.pdf`.
- The guideline statement's publisher open-access page: `https://www.sciencedirect.com/science/article/pii/S0895435616000585`
  (the lane fetched the `jclinepi.com/…/pdf` variant: 403). PubMed PMID 27005575 (abstract; no PMC full text).
- **No** PMC/Europe PMC full-text record exists for the 2016 *J Clin Epidemiol* guideline statement.
- PRISMA-S is in PMC for both co-publications: **PMC7839230** (Syst Rev 10:39) and **PMC8270366** (JMLA
  109(2):174–200). The lane's Europe PMC REST route answered 500 twice, but the r95 closure's third attempt got
  http 200 / 226044 B and read `<volume>10</volume>` + `<elocation-id>39</elocation-id>` — so the route is
  intermittent, not dead, and the D4 locator is externally confirmed.
- **No erratum** for either PRISMA-S co-publication, and **no newer version**: the 2021 16-item extension is
  still current (official checklist PDF still dated "Last updated February 27, 2020"); PRISMA-LSR (2024) and
  PRISMA-COSMIN (2024) are separate extensions, not PRISMA-S revisions. **PRESS has no newer edition** —
  PRESS 2015 (J Clin Epidemiol 2016;75:40–46 + CADTH E&E 2016) remains current; CADTH's PRESS page (updated
  2025-08-08) still points to it. Neither S223's nor S224's row needs a version/erratum cell.

## Tools

No tool was installed or upgraded this run; the host already had `curl`, `pdftotext` (poppler 26.10.0) and GNU
grep 3.12 (used for every grep measurement above, as the seat brief requires). The `sys.addaudithook`
instrument in `R96ScoutSources-k4-audit.txt` is stdlib Python, no install.

## Files written by this seat

Only under `.ufo/waves/round-96/w1/`: `R96ScoutSources.md` (this file) and the receipts
`R96ScoutSources-reopen-hashes.txt`, `R96ScoutSources-refetch-compare.txt`,
`R96ScoutSources-s223-bibliographic.txt`, `R96ScoutSources-searches-recompute.txt`,
`R96ScoutSources-fragment-order.txt`, `R96ScoutSources-k4-audit.txt`,
`R96ScoutSources-a1-shim-check.txt`, `R96ScoutSources-missing-receipts.txt`,
`R96ScoutSources-frontier-leads.txt`. No production file, no lane file and no git object was modified; the
scratch tree was deleted.
