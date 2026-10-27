# R58ScoutS101Freshness — S101 opening freshness

## Finding

**A fresh local opening from committed bytes is honest; a fresh external acquisition is not.** On 2026-10-27 I opened the lane-committed S101 capture with the pinned local `tools/capture-text.py`; no live fetch was made for this inspection. This verifies the bytes and located text in the frozen C2 sense. It does not establish that the document is currently served at the URL, that it is newly acquired in round 58, or that the content is true/current.

## Source and prior metadata

- `corpus/SOURCES.md:111`, S101: `中国学术期刊（光盘版）检索与评价数据规范（修订本）`, copy hosted by 哈尔滨工业大学; kind `docs`, tier B. URL: `https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc`.
- SOURCES anchor: section 11 (文献标志码), sections 14.1 and 14.4 (参考文献), and section 15.7 parameter table; row describes a UTF-16LE text of raw `.doc` capture. Existing row metadata: status `mined`, opened `2026-10-25`, recheck `180d`, used by `corpus/knowledge/citation-count-semantics-r37.md`. Thus this is **not** S101's first-ever opening/admission.
- Round-58 frozen `claims.md` lines 15–19 and `c2/quotes.tsv` specify S101 and the same URL. Frozen claim says opened from committed lane capture this round, no external fetch, and scopes the claim to located text, not standards validity or semantic truth.
- `corpus/evidence/round58/s101-open.txt` records a 2026-10-27 local opening, explicitly “from lane-owned committed capture (no live fetch),” and the defined-form command and quote locations. It is a later opening record, not evidence that the raw bytes were newly fetched by this round.

## Byte and text checks

Commands run from lane root (all reads; no network):

```text
sha256sum corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3  corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
sha256sum tools/capture-text.py
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  tools/capture-text.py
TMPDIR=/fast/scratch/hyaku/chousa-r58/R58ScoutS101Freshness python3 tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw > /fast/scratch/hyaku/chousa-r58/R58ScoutS101Freshness/s101.txt
wc -c -m /fast/scratch/hyaku/chousa-r58/R58ScoutS101Freshness/s101.txt
27012 47356 /fast/scratch/hyaku/chousa-r58/R58ScoutS101Freshness/s101.txt
```

The defined form has 27,012 characters, matching `s101-open.txt`. I checked all 12 frozen quote strings at the recorded offsets against this output: every string occurs exactly once at its stated offset (`315, 330, 590, 683, 734, 781, 797, 838, 965, 993, 1460, 11723`). This establishes text presence and offset binding, not entailment or truth.

Important sidecar distinction: committed `corpus/captures/6dc68fd6b32ce9c8dfcebce8.txt` hashes to `d4e7e5adc9f723d61852a6dffd559062ba3db5603c43ec158d96d6d4e564e112`, while the defined-form stdout above is 47,356 bytes and the raw-derived capture-text command is what C2 pins and runs. The `.txt` sidecar begins with replacement-character representations of binary OLE bytes; do not use it as the quote-text source. The refetch receipt separately records that sidecar digest.

## Acquisition history and limits

`corpus/evidence/round57/refetch.tsv:19` records S101, attempt 1, fetched `2026-10-27T08:05:26Z`, HTTP 200, raw SHA256 matching the frozen pin, and the sidecar SHA above. Line 66 records attempt 2 at `2026-10-27T08:29:36Z` with the same raw and sidecar digests. `git show --stat f9736a3` shows the raw and `.txt` first added in that round-57 re-fetch commit; `git log --follow` shows no earlier committed raw capture. Therefore the raw bytes were externally fetched during round 57, not newly fetched during this local round-58 opening. A matching digest across those receipt attempts only establishes recorded byte identity; it does not prove current remote availability or source authenticity.

No live URL request is authorized here; round-57 egress-scope L0 remains open. I did not fetch, amend claims/counters/quotes, or make any source-repository changes. Scratch was removed.

## Evidence classes

- **Observed:** S101 URL/anchor and prior `opened: 2026-10-25` in SOURCES; 2026-10-27 round-57 fetch receipt; committed raw SHA matches claims; pinned tool hash matches; defined text output and all 12 offsets reproduce.
- **Inference:** “fresh opening this round” is accurate only as a dated local re-opening/rechecking of lane-owned committed bytes. It must not be read as a new web access, first-ever opening, or freshness of the hosted document.
- **Unknown:** Present-day URL response, whether the hosted file changed since round-57 fetch, and the factual/standards correctness of the document's statements.

VERDICT: S101 fresh-local-opening claim survives with the explicit committed-bytes/no-fetch qualification; any implication of a fresh round-58 external acquisition is falsified by the round-57 fetch record.