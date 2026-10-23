# Runtime variant falsification

**Hypothesis verdict: HOLDS for the opened page snapshots and requested seed ranges.** No mislabeled variant or extractor disagreement was found. This is not a verdict on claim C1 or a proof about future page contents.

## Axes and method

Primary axis: **operability**. Reviewed dimensions: expected-label correctness, independent contract extraction, and bounded source access. Calibration is protected by reporting the sampling limits below.

Read `corpus/evidence/round29/claims.md` first, then the frozen counter, both fixture tables, registry rows and the repair lesson. Wrote an independent stdlib extractor in `/fast/scratch/hyaku/chousa-r29/w1/CriticRuntimeVariants/reference.py`; it independently implements dropped HTML content, the exact block list, Unicode normalization, case-sensitive matching and alphanumeric boundaries.

Fetched registry sources S002, S003, S008, S013, S019, S020, S038 and S044 concurrently, exactly once each: **8 GETs, all HTTP 200**. Imported a byte-identical scratch copy of `c1-count.py`, pointed its fixture and registry variables at the originals, and replaced `fetch_text` with a memoized wrapper whose original parser reads only the cached response bytes. No further network access occurred. For the 500 fixture-only builds, suppressed only page-case generation; restored it for the 50 complete builds. Expected labels and committed files were unchanged.

## Executed command and results

```sh
timeout 180s prlimit --as=1073741824 --nproc=4096 -- python3 -B /fast/scratch/hyaku/chousa-r29/w1/CriticRuntimeVariants/audit.py
```

Exit **0**; command wall time **6.27 s**; Python **3.14.8**. Memory bounded to 1 GiB and process count to 4096. No background jobs or child processes were launched.

| Generated class | Seeds | Items checked | Mislabeled |
|---|---|---:|---:|
| Fixture subspan | 2901–3400, inclusive | 7000 | 0 |
| Fixture adjacent-token transposition | 2901–3400, inclusive | 7000 | 0 |
| Fixture rotation cross-attribution | 2901–3400, inclusive | 7000 | 0 |
| Page window | 2901–2950, inclusive | 1200 | 0 |
| Page adjacent-token transposition | 2901–2950, inclusive | 1200 | 0 |
| **Total** | **500 fixture seeds; 50 page seeds** | **23400** | **0** |

Counter and independent normalized page text were character-for-character equal on **8/8 pages**. Supplementary enumeration of the entire fixture generator domain checked **748 subspans, 170 transpositions and 14 rotation cross-attributions**: **0/932 mislabeled**. This covers fixture possibilities the seed sample did not reach.

**Every counterexample (seed, quote): none.** No impacted-axis regression was demonstrated. **Smallest safe correction: none indicated; leave the frozen design unchanged.**

## Evidence

All paths below are relative to `.ufo/waves/round-29/build/CriticRuntimeVariants/`:

- `result.json`: observed counts, seed bounds, elapsed time and cache-read counts.
- `mislabeled-variants.json`: empty sampled and exhaustive counterexample arrays.
- `checked-variants.jsonl`: every sampled seed, source, quote, expected label and independent verdict.
- `extractor-diffs.json`: all 8 text comparisons; empty differences array.
- `fetch-manifest.json`: exact registry URLs, status, content type, charset and byte counts.
- `reference.py`, `audit.py`: retained experiment source. Cached response bytes, decoded pages and both extracted texts remain under `/fast/scratch/hyaku/chousa-r29/w1/CriticRuntimeVariants/cache/`.

Located source example, copied from opened page text: “JSON Lines is a convenient format for storing structured data that may be processed” — https://jsonlines.org/, access date **2026-10-23**; cached `S013.document`, line 36. This is a 15-word source quotation, not a generated negative example.

## Limits

Both counter fetch slots deliberately use the same cached response, as assigned; temporal drift between live fetches was not tested. Page sampling covers 50 seeds on these 8 snapshots, not every possible seed or future page revision. Exact extractor agreement is observed on these pages, not asserted for every possible HTML document. The candidate verifier and the C1 scoring command were not run. No tools were installed or updated, and no production, frozen, Git-index or revision-state files were changed.
