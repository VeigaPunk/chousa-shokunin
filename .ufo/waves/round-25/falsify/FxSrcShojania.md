# FxSrcShojania — source review

Axes: freshness (re-open and scope fit); calibration (wording, inference, decision).

## Findings

- **LOW — S021 teach wording is slightly stronger than its measured endpoint.** The fresh PubMed read of https://pubmed.ncbi.nlm.nih.gov/17638714/ returned the abstract; its `RESULTS` text contains the Gate quote exactly: “A signal occurred within 2 years for 23% of reviews and within 1 year for 15%.” (16 whitespace-delimited words; lesson `round-25.md:70`). It is a verbatim substring at the stated location and under 25 words. The source reports update *signals* and its limitation says judgments about need for updating lacked content experts (PubMed Abstract, `LIMITATION`). Row S021's kind `paper`, tier A for its own measured result, bounded sample scope, and citation/abstract-results anchor are defensible (`corpus/SOURCES.md:31`; scout evidence `.ufo/waves/round-25/build/SrcShojania2007.md:4-18`). `teaches` says “Findings that need updating” rather than the source's more precise “signals for updating”; recommend retaining “signals that may warrant updating” so it does not convert the study's operational signal into expert-confirmed need. This is a wording calibration only: the row scope explicitly limits the result to the study's sample and disclaims a rule for all records.

## Decisions

- **Agree:** S021 remains `queued` with `used-by=—` (`corpus/SOURCES.md:31`). Its round-25 Gate quote documents source opening; no knowledge entry uses it as an admitted premise. The cite/opening record alone should not turn every newly logged candidate into `mined`.
- **Agree:** S019/S020 are `mined` and list `corpus/knowledge/metadata-screen-r25.md` as `used-by` (`corpus/SOURCES.md:29-30`). That entry explicitly labels the mapping as an “inference,” separates the Cochrane periodic-assessment point (S019) from PROV-O derivation/entity-time terms (S020), and says neither source prescribes the header (`metadata-screen-r25.md:20-27`). This is not a claim that either source endorses all three fields; their scopes and source roles remain bounded.
- **Agree:** S025 is rejected as a general research-record staleness authority (`corpus/SOURCES.md:35`). The opened RFC is an HTTP-caching standard; §4.2 Freshness gives `response_is_fresh = (freshness_lifetime > current_age)` (RFC reader artifact `artifact://32633:643-647`). Its scoped rejection is grounded, and the flip—use only as a labelled analogy paired with a directly relevant method source—is concrete and meaningful (`round-25.md:74,79-82`; `.ufo/waves/round-25/build/SrcRfc9111.md:7-20`).

## Residual risk and verification gaps

The PubMed reader supplied the primary paper's abstract, sufficient for this abstract-level quote; full-text access was not established (`SrcShojania2007.md:5-7`). S019/S020's reuse is an explicitly labelled lane inference, not source-backed proof of the header design. These are advisory lane judgments, not outside closure. No tools installed or updated.

VERDICT: Agree with S019/S020 mined, S021 queued, and S025 rejected; only low-severity S021 wording calibration remains. Installs: none.