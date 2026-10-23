# Reopen S062 — RFC 8259 vs SOURCES.md and claim-record-fields-r33.md

Attacked: whether S062’s pin and every RFC quote or paraphrase in `corpus/knowledge/claim-record-fields-r33.md` match the page, and whether that note over-reads the RFC. No gate run. No lane production edit.

## Fetch

- Command: `curl -sS -D …/rfc8259.headers -o …/rfc8259.txt --max-redirs 0 --proto '=https' --fail 'https://www.rfc-editor.org/rfc/rfc8259.txt'` (exit 0).
- Response: `HTTP/2 200`, `date: Fri, 23 Oct 2026 09:00:13 GMT`, `content-type: text/plain;charset=utf-8`. Header copy: `.ufo/waves/round-33/w2/ReopenS062/rfc8259.headers`.
- Body: `/fast/scratch/hyaku/chousa-r33/w2/ReopenS062/rfc8259.txt`. `sha256sum` = `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`. `wc -c` = 28360. Newlines = 899 (`LF` 899, `CR` 0). Form feeds = 16 (one per page line: 59, 115, 171, 227, 283, 339, 395, 451, 507, 563, 619, 675, 731, 787, 843, 899). Line 339 is a single `\x0c`.
- Line numbers below are newline numbers (`grep -n`, `split('\n')`). Python `splitlines()` is wrong here: it also splits on `\f` and yields 915 lines.

S062’s pin matches this GET: HTTP 200, 28,360 bytes, SHA-256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`, opened 2026-10-23, December 2017 (page banner line 284). `grep -cF` transcript: `.ufo/waves/round-33/w2/ReopenS062/grep-cf.txt` (sha256 `58ec87297e7c35359117753f155fb40b562bd89aa7d5aab676fa328ff7629122`).

## S062 row (`corpus/SOURCES.md:72`)

Scope and teaches are paraphrases, not over-reads. Anchor line range drops one body line.

| Claim | Verdict | Evidence |
| --- | --- | --- |
| §3 permits object and array values; anchor lines 296–308 | HOLDS | Line 296 is `3.  Values`. Lines 298–299: `A JSON value MUST be an object, array, number, or string, or one of` / `the following three literal names:`. Line 308: `value = false / null / true / object / array / number / string`. `grep -cF` = 1 for both the MUST sentence and the `value =` rule. |
| Members are string-name/value pairs | HOLDS | Lines 318–320: `An object structure is represented as a pair of curly brackets` / `surrounding zero or more name/value pairs (or members).  A name is a` / `string.` Line 327: `member = string name-separator value` (`grep -cF` = 1). “A name is a string.” is wrapped, so it is not one `grep -F` line. |
| §4 recommends unique names | HOLDS | Line 322: `name.  The names within an object SHOULD be unique.` `grep -cF` of `The names within an object SHOULD be unique.` = 1. |
| Duplicate-name receiver behavior is unpredictable | HOLDS | Lines 331–333 join to: `When the names within an object are not unique, the behavior of software that receives such an object is unpredictable.` The full sentence is wrapped, so `grep -cF` of the one-line string is 0; `grep -cF` of `the behavior of software that receives such an object is` = 1 (line 332) and of `unpredictable` = 2. The other hit is line 525 (§8.2, unpaired surrogates), not this claim. |
| Teaches: unique names are recommended *because* that behavior is unpredictable | HOLDS as paraphrase | The RFC states the SHOULD (line 322), then the interoperability paragraph (lines 329–333). It does not use “because”. The causal link is the note’s, and it does not add a requirement. |
| Scope disclaimer: standards semantics, not the lane’s `verify-claims` contract | HOLDS | Row text only. The RFC does not mention this gate. |
| Anchor `§4 “Objects” lines 316–333, 343–344` | BROKEN locator | 316 is `4.  Objects`. 322, 327, 331–333, 343–344 are the right newline numbers. Line 334 is body text and is not in the range. The range therefore ends mid-sentence at `pair` (333) and resumes at `object, and some implementations…` (343). Page furniture is 335–342 plus the form feed on 339, not 334. |

## Knowledge note (`corpus/knowledge/claim-record-fields-r33.md`)

Joined §4 paragraph (lines 329–334 + 343–344), whitespace normalized:

> An object whose names are all unique is interoperable in the sense that all software implementations receiving that object will agree on the name-value mappings. When the names within an object are not unique, the behavior of software that receives such an object is unpredictable. Many implementations report the last name/value pair only. Other implementations report an error or fail to parse the object, and some implementations report all of the name/value pairs, including duplicates.

| Quote or paraphrase in the note | Verdict |
| --- | --- |
| L38 `"The names within an object SHOULD be unique."` (line 322) | HOLDS. Exact. `grep -cF` = 1, `grep -nF` line 322. |
| L39–40 `"Many implementations report the last name/value pair"` (line 333; sentence ends `"only."` on line 334) | HOLDS. Exact fragment is wholly on line 333 (`grep -cF` = 1). Line 334 begins `only.`. |
| L41 next sentence says other implementations `"report an error or fail to parse"` | HOLDS as a fragment, not the whole sentence. `Other implementations report an error or fail to parse` is on the page: line 334, `grep -cF` = 1, followed by ` the`. The sentence continues on lines 343–344: `object, and some implementations report all of the name/value pairs,` / `including duplicates.` (`grep -cF` = 1 each). The note does not claim the sentence ends at “parse”. |
| L39 “when they are not, receiver behaviour is unpredictable” | HOLDS paraphrase. Matches lines 331–333. “behaviour” is the note’s spelling; the RFC has “behavior”. Not a quotation. The line 525 “unpredictable” is a different section and is not what this sentence cites. |
| L43–45 refusing the record “as the RFC's error-reporting implementations do”, and “neither source says a verifier must” | HOLDS. Not an over-read. The RFC describes three observed behaviors (last pair only; report an error or fail to parse; report all pairs). It does not say a receiver MUST reject duplicates. The note labels refusal as the lane’s design choice. “error-reporting” compresses “report an error or fail to parse”; the same sentence’s third behavior (lines 343–344) is omitted. That is under-inclusion, not a stronger claim than the RFC. |

## Does the entry over-read the RFC?

No. It does not turn SHOULD-unique or “unpredictable” into a requirement that a verifier reject duplicates. The fail-closed rule is stated as this lane’s choice. The phrase `Other implementations report an error or fail to parse` is on the page (line 334). S062’s anchor is the defect: that line is outside `316–333, 343–344`, so the anchor alone does not show the phrase the knowledge note quotes.

## Limits

- One GET, no redirect, 2026-10-23. Did not re-fetch S063. Did not run `c1-count-v2.py`.
- `grep -cF` counts matching lines. Wrapped sentences were checked by joining newline-numbered lines, not by a single fixed string.
