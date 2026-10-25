# Review: README quote "Where possible, an archive.org link to the original claim url"

## Item
Reviewer seat L1Chousa45.ReviewQuoteReadmeClaim (round 45, wave 1): locate the quote in the README capture and report sha256, char offset, occurrence count, 200 chars verbatim, field-level confirmation, and all other archive.org-mentioning fields.

## Commands run (verbatim decisive output)

### 1. sha256sum + wc (bash)
```
$ sha256sum /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/ce16d57277fedfd4f0e7750e.txt && wc -c -l <same>
8e1f5bff76c14672de04987fcaa6a0fcecfbb493f4c2b6c8f1c3443d91989fe5  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/ce16d57277fedfd4f0e7750e.txt
  99 4771 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/ce16d57277fedfd4f0e7750e.txt
```

### 2. Python str.find / occurrence count / 200-char slice (eval)
```
TOTAL len: 4771
occurrences: 1
offsets: [1027]
find offset: 1027
occurrences of 'archive.org' in whole file: 2
occurrences of 'archive.org' case-insensitive: 2
preceding key check: o the original location",
    "cached_original_claim_url":
```

### 3. Grep `archive\.org` (matches starred)
```
 18:    "cached_original_claim_url": "Where possible, an archive.org link to the original claim url",
 36:                    "cached_source_url": "An archive.org link for the source url"
```

## Findings

### Quote located — VERDICT: LOCATED
- File: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/ce16d57277fedfd4f0e7750e.txt`
- sha256 (file): `8e1f5bff76c14672de04987fcaa6a0fcecfbb493f4c2b6c8f1c3443d91989fe5` (4771 bytes, 99 lines)
- Exact quote: `Where possible, an archive.org link to the original claim url`
- Occurrence count: **1** (unique in file)
- Char offset (Python `str.find` on full file text): **1027**
- 200 chars around it, verbatim (offset 927–1127; the quote occupies 1027–1077):
```
 first appeared on the internet, a url to the original location",
    "cached_original_claim_url": "Where possible, an archive.org link to the original claim url",
    "fact_checking_article": "The fa
```

### Field-level confirmation
The quote is the JSON-string value of **`cached_original_claim_url`** (README line 18, file offset ~1027). It is a **claim-level** field: it sits at the top level of the claim object in the README's Format block, a sibling of `claim`, `label`, `original_claim_url`, `fact_checking_article`, etc. It carries the description "Where possible, an archive.org link to the original claim url" — i.e., a cached archive.org mirror of the claim's original URL.

### Every other field whose description mentions archive.org
- **`cached_source_url`** (README line 36): description "An archive.org link for the source url". **Answer-level** field, nested under `questions[].answers[]` — not claim-level.
- Total literal `archive.org` occurrences in file: 2 (exactly these two field descriptions; no other field description or body text mentions archive.org).

## Resolvable pointers
- quote: `.../.qcache/ce16d57277fedfd4f0e7750e.txt:18` (offset 1027; sha256 of file above)
- claim-level field: line 18 (`cached_original_claim_url`); answer-level field: line 36 (`cached_source_url`)

## Residual risk / verification gaps
- The capture is a single 4771-byte text; quote counted case-sensitively and case-insensitively (both 2 for `archive.org`). No other spelling variants (e.g., "web.archive.org", "archive dot org") present — checked via grep `archive\.org` and Python `.count`.
- Verification was read-only against on-disk capture; no network egress performed.

## Report
- Location: (this file) `.ufo/waves/round-45/w1/ReviewQuoteReadmeClaim.md` under lane root.
