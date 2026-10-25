# Review: lane row S082 (AVeriTeC README) — Round 45 wave 2 (falsify)

Item attacked: row S082 in `corpus/SOURCES.md` at 5e8c7ad2f7b8254d83358820286e3d12ca4672d1.

Method: measured over committed bytes — `git archive` of 5e8c7ad2f7b8254d83358820286e3d12ca4672d1 extracted to /tmp/chousa-r45-RevSourceS082/tree; counters run inside that tree. Capture read from on-disk cache `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/ce16d57277fedfd4f0e7750e.txt` (4771 bytes).

## Cell checks (11 cells, header columns: id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by)

| # | cell | verdict | evidence |
|---|---|---|---|
| 1 | id `S082` | holds | well-formed, unique |
| 2 | source: AVeriTeC README + raw.githubusercontent URL | holds | capture file content is the AVeriTeC README (title `# Averitec`, JSON field dictionary); sha256 of capture = 8e1f5bff76c14672de04987fcaa6a0fcecfbb493f4c2b6c8f1c3443d91989fe5 = capture_sha256 in spans.tsv |
| 3 | kind `dataset` | holds | README of a dataset repo documenting the dataset JSON format |
| 4 | tier `A` | holds | consistent with sibling S083/S084; tier policy not falsifiable here |
| 5 | scope: what archive fields are documented to hold, claim-level and evidence-level | holds | capture line 18 `cached_original_claim_url` and line 36 `cached_source_url` are exactly the two documented archive fields |
| 6 | anchor: JSON field dictionary, quote at capture char 1027, on-disk capture, no fetch, span committed | holds | `str.find` of `Where possible, an archive.org link to the original claim url` = char offset **1027** (exact); quote word count = **10** <= 25; capture is on disk (sha matched); spans committed and verbatim (below); no-fetch claim consistent with L0 `8d77e6c1` open and cache-only method |
| 7 | teaches: claim-level best-effort, evidence-level unconditional, empty claim archive records only no link stored, not why | holds (no overclaim) | line 18 `"Where possible, an archive.org link to the original claim url"` = best-effort; line 36 `"An archive.org link for the source url"` = no qualifier; full capture contains exactly two `archive` mentions (chars 1046, 1972), neither states a cause for a missing/empty field, so "records only that no link is stored, not why" is faithful and explicitly asserts no cause ("not why") — does NOT claim more than the README says |
| 8 | status `mined` | holds | source is a committed on-disk capture |
| 9 | opened `2026-10-25` | holds | matches round 45 date in SOURCES.md changelog |
| 10 | recheck `365d` | holds | matches knowledge file `recheck: 365d` |
| 11 | used-by `corpus/knowledge/evidence-archive-field-policy-r41.md` | holds | file exists in tree; references S082 at capture chars 1027 and 1969 with consistent wording; inference already narrowed post-critic (`narrowed after the round-45 critic CritFieldPolicyInference`) |

## Table integrity

- Header has 11 columns; S082 row splits into 13 `|`-delimited parts = 11 interior cells + edge pipes; no escaped pipe (`\|`) and no literal `|` inside any cell. Row renders as a valid 11-column row.
- `grep -n '\|' row082.txt` → no matches.
- Counter `corpus/evidence/round45/c3-count.py` from the tree: `ENTRIES=2/2`, `CITES_BOUND=3/3`, `QUOTES_IN_SPAN=4/4`, `QUOTES_IN_ENTRY=4/4`, `COUNTS_IN_ENTRY=7/7`, `CAPTURE_BOUND=4/4`, `COUNTS_REDERIVED=7/7`, `C3=PASS`; `--lane-only` also PASS (CAPTURE_BOUND/COUNTS_REDERIVED skipped by design). S082's spans register.

## Span fidelity

- `spans/S082-1.txt` and `spans/S082-2.txt` exist; both are verbatim substrings of the capture (`span in capture? True` for both); their start offsets in the capture are 1809 and 867, matching the `offset` column of `spans.tsv`. Quote literals are inside their span fragments (counter QUOTES_IN_SPAN=4/4).
- Char citations in the row and knowledge file are exact: `Where possible...` literal starts at 1027; `An archive.org link for the source url` literal starts at 1969.

## Verdict

All 11 cells hold. The anchor quote is located exactly at capture char 1027 (10 words <= 25). The teaches cell is supported by the capture verbatim and claims nothing beyond it: it cites the two documented field descriptions and draws only the negative conclusion (no documented cause for an empty claim archive), which the full-text scan confirms — no overclaim, no invented cause.

## Residual risk / verification gaps

- "No fetch" cannot be independently proven from committed bytes; only consistency with the open L0 fetch-scope and the cache-only method is observable. No live fetch performed (per seat contract).
- Span fragments begin mid-line (cosmetic; they are contiguous JSON-dictionary blocks, faithful to the capture).
- Tier/status conventions are lane policy, not falsifiable from source text.

Scratch removed before finish.
