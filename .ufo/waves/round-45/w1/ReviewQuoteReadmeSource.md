# ReviewQuoteReadmeSource

Item given: Locate `An archive.org link for the source url` in the README capture; report file sha256, byte/char length, Python `str.find` offset, occurrence count, 200 surrounding characters verbatim; confirm `cached_source_url` is inside each answer's evidence object, not claim-level. Verdict: located / absent.

## Findings

- Verdict: **located** (one occurrence).
- Capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/ce16d57277fedfd4f0e7750e.txt`
- SHA-256: `8e1f5bff76c14672de04987fcaa6a0fcecfbb493f4c2b6c8f1c3443d91989fe5`
- Length: 4771 bytes; 4771 characters (UTF-8 decoded).
- `str.find` offset: 1969; occurrence count: 1.
- The quote describes `cached_source_url` in the per-answer object: the README example nests `questions` → `answers` → an object containing `answer`, `answer_type`, `source_url`, and `cached_source_url` (capture lines 28–39). It is not the claim-level field. Claim-level `cached_original_claim_url` is separately shown at line 18.
- 200 characters around the quote, verbatim (100 before + quote + 100 after):

```text
           "source_url": "The source url for the answer",
                    "cached_source_url": "An archive.org link for the source url"
                    "source_medium": "The medium the answer appeared in, e.g. web text, a pdf, or 
```

## Commands and verbatim outputs

1. `sha256sum /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/ce16d57277fedfd4f0e7750e.txt && wc -c /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/ce16d57277fedfd4f0e7750e.txt && wc -m /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/ce16d57277fedfd4f0e7750e.txt`

```text
8e1f5bff76c14672de04987fcaa6a0fcecfbb493f4c2b6c8f1c3443d91989fe5  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/ce16d57277fedfd4f0e7750e.txt
4771 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/ce16d57277fedfd4f0e7750e.txt
4771 /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/ce16d57277fedfd4f0e7750e.txt
```

2. Python evaluation read the UTF-8 file, counted successive `.find` results, and printed the 100 chars before/after the quote. Verbatim decisive output:

```text
occurrences: 1
first offset: 1969
---100 BEFORE---
'           "source_url": "The source url for the answer",\n                    "cached_source_url": "'
---QUOTE---
'An archive.org link for the source url'
---100 AFTER---
'"\n                    "source_medium": "The medium the answer appeared in, e.g. web text, a pdf, or '
---VERBATIM 200 AROUND---
           "source_url": "The source url for the answer",
                    "cached_source_url": "An archive.org link for the source url"
                    "source_medium": "The medium the answer appeared in, e.g. web text, a pdf, or 
```

3. Read-only capture inspection: `read` of the absolute capture path, lines 1–100. Relevant output: lines 28–39 show the `questions` array with `answers` array and the per-answer object; line 36 has `"cached_source_url": "An archive.org link for the source url"`. Line 18 separately identifies the claim-level `cached_original_claim_url`.

No tools installed or updated. No source/network fetch performed. No scratch files created.
