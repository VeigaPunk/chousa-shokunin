# Crossref Crossmark source check

- **Opened:** https://www.crossref.org/services/crossmark/ (final URL; canonical URL agrees), 2026-10-21.
- **HTTP:** `curl --location --silent --show-error --output /dev/null --write-out 'http_code=%{http_code}\neffective_url=%{url_effective}\nredirects=%{num_redirects}\n' https://www.crossref.org/services/crossmark/` → `http_code=200`, `effective_url=https://www.crossref.org/services/crossmark/`, `redirects=0`. The page opened; not blocked or paywalled.
- **Verbatim quote (9 words):** “Crossmark makes this information more visible to readers.” **Location:** introductory text, in the paragraph after “It’s important to know if the content being cited has been updated, corrected, or retracted,” immediately before “Benefits of Crossmark”.
- **Source freshness observation:** page footer says “Last updated: 2020-April-08”; served-page metadata reports `meta-gitlastmod: 2026-10-06`.

## Proposed registry row

Next unused ID is **S019** (existing IDs S001–S018 are listed at `corpus/SOURCES.md:9-28`). Proposed fields: **source** Crossmark — Crossref — https://www.crossref.org/services/crossmark/; **kind** `docs`; **tier** `A`, scoped only to Crossref's own Crossmark service behavior; **scope** Crossref's stated reader-facing access to an item's reported status and member-registered updates, corrections, retractions, and related metadata; **anchor** introductory text; “Benefits of Crossmark”; “How Crossmark works”; “Obligations for Crossmark”; page as served 2026-10-21 (footer date 2020-04-08); **teaches** Crossmark can expose a work's reported current status and changes, but its presence is not a guarantee; **status** `queued`; **opened** `2026-10-21`; **recheck** `365d`; **used-by** `—` until a knowledge entry cites it. Column and status definitions: `CORPUS.md:86-108`.

## Claim assessment and recommendation

**Claim support: partial.** The page says Crossmark exposes reported current status and makes updates/corrections/retractions more visible, including changes readers may learn about long after download. It does not say a scheduled date or cadence makes staleness computable, nor that `source:` and `verified-at:` are prerequisites for re-verification. The page also cautions that Crossmark's presence is not a guarantee. Do not use it alone to substantiate the full claim. The claim's metadata requirements are consistent with the lane's separate criterion 6 (`corpus/QUALITY.md:17-27`), not established by this source.

**Recommend admit as `queued`**, narrowly scoped as above: an opened official source worth mining for a knowledge entry on Crossmark's coverage and limits in checking cited works for updates. Do not mark `mined` until a knowledge entry cites this row, as required by `CORPUS.md:103-108`. This is not a claim that the source establishes a recheck cadence or provenance precondition.

VERDICT: Admit S019 as queued, tier A only for Crossref's own Crossmark behavior; partial support for the stated metadata claim. No tools installed or updated.