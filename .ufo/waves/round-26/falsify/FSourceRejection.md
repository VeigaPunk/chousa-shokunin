# FSourceRejection — reopen S025 (RFC 9111 §4.2), round26 attempt1

Seat `ChousaR26R.FSourceRejection`, scout, author-lane advice only (not an outside judge, not admission).
Judged on: freshness. The C1/C2/C3 verdicts are out of scope. This seat checks only whether the sourced rejection holds and how it relates to C2.

## Revisions and inputs observed

- Target: `0e9784bd52eca456b24d0bc40921480a47f91a2b`, from `corpus/evidence/round26-measured-revision.json`. `git cat-file -t` returned `commit`. Extracted with `git archive $REV | tar -x -C /tmp/chousa-r26-falsify-FSourceRejection` (exit 0). The moving working tree was not graded.
- Archived digests match the measured-revision JSON:
  - `tools/research-gate.sh`: `c2c813f1…abc6`
  - `corpus/SOURCES.md`: `8308e629…a9`
  - `corpus/QUALITY.md`: `2428baaf…7e0`
  - `corpus/evidence/round26-claims.md`: `dcbe2b5f…1c`
- Claim base `ba3333254dd337658a4f25e7a9471f9cf4e4567e` is noted from the claims file. It was not separately extracted, because S025 is not touched by any round26 claim.
- Fleet root (moving tree, read-only): `HEAD bf495b6b4e12ab2f35464ecfe2d8589bb1e4fdae`. The `CORPUS.md` sha256 is `88556402…50b8`, and lines 85–115 hold the SOURCE contract v1.
- Source copies (static public documentation only) are in `/tmp/chousa-r26-falsify-FSourceRejection-src/`. The status and errata pages were fetched with `curl -sSL`, which followed the redirects (the first no-follow tries returned 301 and 302).

| Fetch | HTTP | Bytes | sha256 |
|---|---|---|---|
| `https://www.rfc-editor.org/rfc/rfc9111.txt` | 200 | 84,477 | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` |
| `https://www.rfc-editor.org/rfc/rfc9111.html` | 200 | 232,630 | `ce91ee9848d2b9ac46386b0f0cbd4bfd9c0cd1948ebc363834cadc7e0997f3d7` |
| `https://www.rfc-editor.org/rfc/rfc9111.json` | 200 | — | status metadata |
| `https://www.rfc-editor.org/info/rfc9111` → `/info/rfc9111/` | 200 | — | info page |
| `https://www.rfc-editor.org/errata/rfc9111` → `errata.rfc-editor.org/search/?rfc_number=9111&presentation=records` | 200 | — | errata records |

No gate, selftest, measure probe, build, lint, or fixture was run. Everything about the gate below comes from reading the archived source.

## Where S025 appears at the target

Searched with `grep -rn "S025\|9111\|response_is_fresh\|freshness_lifetime"` over `corpus SKILL.md LOG.md SCORECARD.md AXES.md` (exit 0). It appears only in:

- `corpus/SOURCES.md:35`: the row.
- `corpus/SOURCES.md:70`: the "Keeping records current" path says "S025 is a rejected HTTP analogy, not authority for research-record validity".
- `corpus/lessons/round-25.md:74`: the Gate quote.
- `corpus/lessons/round-25.md:80-82`: the rejection rationale and flip.
- `corpus/lessons/round-25.md:87`: curation note.
- `corpus/lessons/round-26.md:15`: intake.

No `corpus/knowledge/*.md` entry cites S025. In particular, the C2 entry `knowledge/recheck-due-r26.md` cites S035, S037, S038, and S029, not S025.

## Observed facts

1. **The Gate quote is exact and correctly located.** `response_is_fresh = (freshness_lifetime > current_age)` is 5 whitespace tokens. It appears byte-for-byte in `rfc9111.txt:621`, inside `4.2.  Freshness` (heading at txt:581, next heading `4.2.1` at txt:652). It is also present in the tag-stripped HTML. The location claim "§4.2 Freshness" at `round-25.md:74` is correct.
2. **The row's anchor is accurate.** The RFC header says `Category: Standards Track` and `STD: 98`, dated June 2022. The JSON metadata gives `status: INTERNET STANDARD`, `obsoletes: [RFC7234]`, `obsoleted_by: []`, `updated_by: []`. "Standards Track, June 2022" is correct, though less precise than "Internet Standard, STD 98".
3. **The source itself limits its scope (strongest grounding, at txt:647-649, end of §4.2).** This 25-word quote is the first sentence of that paragraph, checked by a whitespace token count:
   > "Note that freshness applies only to cache operation; it cannot be used to force a user agent to refresh its display or reload a resource."

   Supporting text: the Abstract says "This document defines HTTP caches…". §1 (txt:140-175) frames freshness as cache reuse without validation. §4.2 bases freshness on an origin-assigned expiration time (Expires or max-age).
4. **The `on-release` recheck is still satisfied as of 2026-10-21.** Nothing obsoletes or updates the RFC. Errata: two records, both `Reported` and `Technical`:
   - 9004, Section 3.5, reported 2026-06-11
   - 9185, Section 4.3.4, reported 2026-09-24

   Neither touches §4.2.
5. **C2's boundary direction, from the gate source.** `tools/research-gate.sh:2756` reads `if ((asof_days > due_days)); then freshness=overdue; fi`. Selftest expectation `research-gate.sh:6081` is `boundary.md due=2026-10-21 freshness=current`. So when due equals as-of, the entry is **current**. This matches the C2 spec (`round26-claims.md:71-72,79`) and the entry's decision table ("equality is current").

## Inference

- **[INFERENCE] The boundary is inverted.** Map the RFC onto the lane: `current_age` is as-of minus verified-at, and `freshness_lifetime` is N days. Then the RFC's strict `freshness_lifetime > current_age` means fresh iff as-of < due. At as-of = due the RFC model is **stale**, but the lane reports **current**. The analogy also breaks on other points:
  - The RFC uses an expiration assigned by the origin server; the lane uses a schedule the author declares.
  - Its age resets on successful revalidation with the origin.
  - It is defined only for cache reuse (fact 3).
- **Consequence: refusing S025 as generic research-validity authority stays justified, and is load-bearing.** If S025 had been admitted as authority, it would contradict the lane's registered C2 boundary control (due==as-of → current). C2 avoids that by not citing it.

## Findings

1. **HOLDS — the rejection is justified (high confidence).** Tier C for the row's out-of-domain scope and the `rejected` status are both grounded. Fact 3 is a direct source statement, not just a title or topic mismatch. No round26 artifact relies on S025.
2. **LOW — the Gate quote shows the source is on topic but does not ground the rejection reason.** CORPUS rule 1 (`CORPUS.md`, "Rules" 1) asks for a ≤25-word quote "with its location grounding `teaches`". For a rejected row, `teaches` is the rejection reason (HTTP-cache scope only). The recorded quote, the §4.2 formula, only shows the RFC defines a freshness computation. That is the "source is on topic" state of QUALITY criterion 8, not the scope limit. The txt:647 sentence in fact 3 grounds the rejection directly, also within §4.2. This affects the grounding text only, not the verdict. A fix would be an append-only Gate note; this seat made no production edit.
3. **LOW, advisory — the flip hides the boundary hazard.** `SOURCES.md:35` and `round-25.md:81` allow "an explicitly labelled analogy … paired with a directly relevant method source". Taken at face value, that analogy imports the opposite equality rule from C2's registered control. Any future analogy use should state that RFC equality is stale while lane equality is current, and that RFC freshness is origin-assigned, not author-declared. There is also a vocabulary overlap: the lane's `freshness=current/overdue` sits beside RFC "fresh/stale" with no disclaimer in `recheck-due-r26.md`. That is harmless today because the entry never cites the RFC.
4. **CARRIED, unchanged — `used-by` is `—` even though lessons cite the row.** CORPUS v1 defines `used-by` as the "knowledge entries or lessons citing the row". `round-25.md:74,80` and `round-26.md:15` cite S025, yet the cell at `SOURCES.md:35` is still `—` at `0e9784bd`. Round25 `FxSrcRFC.md` already raised this (MEDIUM there). It is unresolved, and it is ambiguous whether a lesson citing a rejection counts. It does not affect C3, which only checks `used-by` for `mined` rows.

## Freshness-axis result

The S025 row is fresh at the as-of date 2026-10-21: it was opened 2026-10-21, its `on-release` trigger has not fired (no obsoleting or updating RFC), and no erratum touches §4.2. This is a metadata and status observation. It is not citation support, truth, or field readiness.

## Remaining unknowns

- I did not check whether the IETF httpbis working group has an active RFC 9111 revision draft. Only the RFC Editor status metadata was consulted.
- The boundary inversion is an analytic mapping, not an executed fixture. No CLI run was authorized for this item.

## Commands and exits

- `git cat-file -t 0e9784bd…`: printed `commit`.
- `git archive … | tar -x`: exit 0.
- `sha256sum` of the four inputs: matched the JSON.
- `grep -rn S025…`: exit 0.
- `curl` fetches: rc 0; HTTP codes as listed in the fetch table.
- `python3` quote, word-count, and errata extraction: exit 0. Results: quote present in txt and HTML; the formula has 5 tokens; the scope sentence has 25 tokens; errata are 9004 (§3.5) and 9185 (§4.3.4).
- `sed -n` reads of `SOURCES.md`, the lessons, the gate (lines 2730-2762), and `CORPUS.md` (lines 85-115): exit 0.

Tools installed or updated: none. Production edits: none, apart from this report.
