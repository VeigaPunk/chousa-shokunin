# Round 25 source review: Schema.org `lastReviewed`

Axes: coverage; freshness.

## Opened source and evidence

- Opened: [Schema.org Property: `lastReviewed`](https://schema.org/lastReviewed).
- Access date: 2026-10-21. Final URL actually opened: `https://schema.org/lastReviewed`; HTTP 200, zero redirects (`curl -L`; effective URL unchanged). Not blocked or paywalled.
- The page identifies `lastReviewed` as a Schema.org property, says its expected value type is `Date`, and says it is used on `WebPage`. The page displayed the development-version notice and footer `Schema.org • V30.1 | 2026-09-16`.
- Verbatim quote (16 words), location: page heading **lastReviewed**, definition paragraph immediately below it: “Date on which the content on this web page was last reviewed for accuracy and/or completeness.”
- The opened page documents `lastReviewed`; it does not provide a `reviewedBy` definition or reviewer-identity evidence. No second source was opened.

## Proposed `SOURCES.md` fields

Per contract v1 (`CORPUS.md:86-108`), propose:

| Field | Proposal |
|---|---|
| source | Schema.org Property: `lastReviewed` — https://schema.org/lastReviewed |
| kind | `spec` |
| tier | `A`, scoped only to Schema.org's own definition and declared use of this property |
| scope | Schema.org's declared meaning, value type, and use of `WebPage.lastReviewed`; not a general re-verification protocol |
| anchor | `lastReviewed` heading/definition; “Values expected to be one of these types” (`Date`); “Used on these types” (`WebPage`); Schema.org V30.1, 2026-09-16 (development version notice shown on access) |
| teaches | Schema.org defines `lastReviewed` as the date web-page content was last reviewed for accuracy/completeness, with `Date` as its expected value and `WebPage` as its declared use. |
| status / opened / recheck / used-by | `queued` / `2026-10-21` / `on-release` / `—` initially |

## Claim assessment and recommendation

**Partial support.** A recorded last-review date can contribute to calculating elapsed time when compared with a chosen reference date, but the property page defines only the past review date. It neither specifies a scheduled future recheck (date or cadence), defines a staleness threshold, nor establishes `source` and `verified-at` as prerequisites to re-verification. The round-25 `verify-metadata` specification separately requires those three metadata keys (`corpus/evidence/round25-claims.md:20-39`); this source does not justify that whole contract.

**Recommend admit as `queued`**, narrowly scoped as above: the official vocabulary page is authoritative for its own property, and its date semantics are relevant to freshness metadata. Keep it queued until a knowledge entry cites it; only then promote to `mined` under contract v1 (`CORPUS.md:103-115`). Do not use it as evidence for `reviewedBy`, a recheck schedule, or provenance preconditions. No reject/flip condition is needed for this admission recommendation.

Remaining unknown: what `reviewedBy` means in Schema.org, because that property was not established by the one opened URL and the one-source limit was maintained.

Installs/updates: none.
