# R99ReviewerC2 — C2 fidelity review (K5) at F d41f4cd

**Attacked tree:** shared clone at F `d41f4cd8b857c6de683e7be5c5e8125b32763a8e` (scratch `/fast/scratch/hyaku/chousa-r99/R99ReviewerC2/repo`, deleted after run). Scratch SHA: `git rev-parse HEAD` → `d41f4cd8...` (see `R99ReviewerC2-counts.txt`).
**Receipts:** `R99ReviewerC2-counts.txt` (all 4 counting commands reproduced at F — entry-controls PASS, gate_records `records=25 ok=25 fail=0`, metadata CLEAN, search-rerun `rev_match=4/4` CLEAN, exit 0 each); `R99ReviewerC2-fidelity-table.txt` (per-row warrant-vs-Do table); `R99ReviewerC2-registry.txt` (SOURCES/refetch cross-check).

## Verdict summary

No K5 overreach/misattribution fired. Each Do cell is what its warrants say. R1's lane inference ("treat an unchecked citation as unreliable") is the entry's disclosed decision-table convention (Never column "(none stated by the sources)"; Named limit 4 warns Do paraphrases can narrow/widen), not presented as a source quote; the numbers it carries (28/25.4%/11,9%/14.5%) are exactly J1/J2/G10's. The lane sentence in R1 is the Lane column's own reading, explicitly lane-owned per `## What this entry governs` line 25. This is the correct reading of the table's contract. No other row widens.

## Per-row fidelity (all faithful)

| # | Do (short) | Warrant(s) | Judgment |
|---|---|---|---|
| R1 | treat unchecked citation as unreliable; 28 studies, 25.4%, 11,9%, 14.5% | J1 (28 in main analysis), J2 (11,9%/25.4%), J5 (errors common), G10 (14.5%) | **faithful** — the inference is labeled lane decision (Never + Names-limit 4); numbers all sourced per row |
| R2 | major: fail to substantiate / unrelated / contradict; minor: oversimplification / generalization / trivial, keeps meaning | G4, G5 (verbatim) | **faithful** — "keeps the intended meaning" restates G5's "did not change the intended meaning of the original authors"; cut preserves meaning |
| R3 | record as source error apart from content error (cited source not read); indirect < 1/6 | G6 (content vs source = secondary/indirect), J4 (<1/6) | **faithful** — "not read" is an accurate gloss of secondary citation; G6 "distinguished ... from source errors" supports "kept apart" |
| R4 | state denominator per quotation, not per reference | G2, G3, G9 | **faithful** — G2/G3 is one sentence split at "rather than" (capture line 910); "state" is the disclosed decision convention |
| R5 | account for ascertainment differences; criteria differ (~half), heterogeneity substantial, lowest 6.7% | J3 (substantial; 6.7%), J8 (taking account of differences … in error ascertainment), G7 (~half) | **faithful** — J8 is a method phrase, warrants the verbatim Do; numbers sourced |
| R6 | sample quotations not only references; judge each assertion in context against original source | G12 (must evaluate each quotation in context … compare to original source), G13 (biased selection of single quotation per reference) | **faithful** — G13's continuation beyond the cut ("authors selected references … rather than quotations", capture line 1115-1116) supports the Do; the cut doesn't reverse meaning |
| R7 | 64.8% major split | G11 (64.8% major to 35.2% minor) | **faithful** — exact number sourced |
| R8 | spot checks; correct placement; declaration of having checked | J6, J7 (near-verbatim) | **faithful** |

**Cut-check notes:** G1 "Previous reviews estimated that approximately 20 to 25%…" (capture line 910) is Mogull *reporting others* — the entry never uses G1 as a warrant and never attributes the 20–25% to Mogull (G1 appears only in the Located-quotes table as a located, not decision, row). G12's real subject is "A broader issue … is that experts must evaluate…" (line 1117) — the cut drops the framing but keeps the normative claim. G13's real lead is "Another limitation … was that the orginal studies had…" (line 1115) — likewise preserved. G4/G5 (line 1017) are "As summarized in Table 2" definitions — entry's Named limit correctly scopes them to S233 ("S236's abstract uses the same words without defining them").

## Governance / Named limits

- "the two quantitative syntheses of that literature that this host could read": Jergas & Baethge is a systematic review + meta-analysis + meta-regression (title; abstract "Methods. We carried out a systematic review, meta-analysis and meta-regression…"); Mogull calls itself "the first systematic review that distinguishes studies of quotation error by research design" (capture line 1007) — "re-derived/synthesis" is accurate.
- "Before this round no capture and no knowledge entry contained the phrase quotation error": reproduced by Q1–Q4 (`rev_match=4/4`, search-rerun CLEAN) and controls `BASE_TOPIC_HITS=0`.
- Limits: both-sources-medical-only, abstract-not-article (J3 heterogeneity), non-reconciliation of 25.4% vs 14.5% (both count different things — S233 re-counts per quotation), and F5's S233-scope note — all verified against captures; the "counts different things" reconciliation is exactly capture lines 1041–1069 (G2/G3 denominator).

## Tiers

- S233 tier A (publisher full text, PLoS One): capture carries doi/title/`Citation: Mogull SA (2017) … PLoS ONE 12(9): e0184727`, Abstract/Methods/Results/Discussion all present; SOURCES scope/anchor/teaches match bytes (see registry receipt).
- S236 tier B (Europe PMC core index record carrying the authors' published abstract): record is `hitCount 1, pmid 26528420, doi 10.7717/peerj.1364, pubYear 2015, journal PeerJ, volume 3` — identity verified from bytes; scope correctly limits to "the review's own published abstract … not the article body"; the "authors' own published abstract" reading is what Europe PMC's `abstractText` for a `PMC4627914` record is. Title prints `articles-a` (record, J0) vs header `articles—a` — entry is faithful to the record it cites, flagged in receipt, not a discrepancy.
- S232 (PeerJ 403), S234 (http 200 Client Challenge, capture `b90988…` verified present in repo), S235 (Europe PMC fullText 500): rejected rows match `refetch.tsv` (id/url/key/attempt/fetched_utc/curl_rc/http_code/raw+txt sha256) and gate reject records S232/S235 (lines 134–135, `curl_rc=22 403`/`500`).

## Lane cells

- R1 "the lane re-opens every source it cites (CORPUS.md rule 1)": CORPUS.md SOURCES Rule 1 says write a row only after opening the source; non-author re-opens a *sample* — the cell overstates ("every source") by one word. This is a Lane-column reading note (explicitly "this lane's reading; not what the sources say") and does not attribute the overstatement to either source; per K5 (source-quote fidelity) it does not fire. Flagged here as a Lane-cell wording nit only.
- R8 "the hyaku closure's non-author spot-check re-opens a sample of the lane's sources (LEARNING.md)": hyaku closure is documented in `corpus/lessons/round-98-verifier-spotcheck.md` (author: hyaku closure); LEARNING.md §"Discernment is checked from outside" states the same practice (non-author spot-checks a sample). Citation is correct.

## Findings

No C2 overreach/misattribution found. One non-firing nit recorded above (R1 Lane "every source" vs CORPUS.md's "re-opens a sample").

VERDICT: R99ReviewerC2 C2 held — every Do cell says only what its warrants say (numbers sourced 6/6, registry/tiers/anchors match captures).
