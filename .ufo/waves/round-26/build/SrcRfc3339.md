# RFC 3339 source finding — C2

## Observed
- Requested-URL check: `curl -sS -o /dev/null -w 'HTTP %{http_code} | redirect=%{redirect_url}\n' 'https://www.rfc-editor.org/rfc/rfc3339'` → `HTTP 301 | redirect=https://www.rfc-editor.org/info/rfc3339/`.
- Following the requested URL: `curl -sS -L --max-time 60 -o /tmp/rfc3339.txt -w 'HTTP %{http_code} | final=%{url_effective} | bytes=%{size_download}\n' 'https://www.rfc-editor.org/rfc/rfc3339'` → `HTTP 200 | final=https://www.rfc-editor.org/info/rfc3339/ | bytes=234768` (HTML landing page).
- Opened the full official RFC text at `https://www.rfc-editor.org/rfc/rfc3339.txt`: `curl -sS --max-time 60 -o /tmp/rfc3339.txt -w 'HTTP %{http_code} | final=%{url_effective} | bytes=%{size_download} | type=%{content_type}\n' 'https://www.rfc-editor.org/rfc/rfc3339.txt'` → `HTTP 200 | final=https://www.rfc-editor.org/rfc/rfc3339.txt | bytes=35064 | type=text/plain;charset=utf-8`.
- RFC 3339 §5.6 gives `date-fullyear = 4DIGIT`, `date-month = 2DIGIT ; 01-12`, and `full-date = date-fullyear "-" date-month "-" date-mday` (retrieved text lines 399–423). §5.7 states month/year-dependent `date-mday` maxima and lists February as 28 days in a normal year and 29 in a leap year (lines 455–478).
- Located quote, RFC 3339 §5.7, “The grammar element date-mday represents the day number within the current month. The maximum value varies based on the month and year as follows:” (24 words; retrieved text lines 457–459).
- `corpus/SOURCES.md` currently ends at S033; search for `3339|rfc-editor|ISO 8601` found no RFC 3339 row (the rfc-editor match shown was S025, RFC 9111). Proposed next id: S034.
- C2’s frozen spec requires calendar-valid `verified-at`, recheck dates, and `--as-of` values, and uses proleptic-Gregorian date addition (`corpus/evidence/round26-claims.md:59–73`). QUALITY 7–8 require scope-matched tiering and distinguish source availability/topic from claim support/truth (`corpus/QUALITY.md:24–32`).

## Proposed SOURCES.md row (contract v1 column order; not written)
| S034 | RFC 3339, Date and Time on the Internet: Timestamps — https://www.rfc-editor.org/rfc/rfc3339 | spec | A | RFC 3339 full-date syntax and day-of-month limits by month and year, including leap-year February; not metadata-field or freshness policy | sections 5.6 (Internet Date/Time Format) and 5.7 (Restrictions), RFC 3339 Standards Track, July 2002 | A full-date uses four-digit year-month-day, and valid day-of-month limits depend on month and year | queued | 2026-10-21 | on-release | — |

## Scope limits / epistemic boundary
- The RFC supports the syntax and calendar day bounds of its own Internet date/time profile. It does not define chousa’s `verified-at`/`recheck` fields, the `--as-of` option, due-date arithmetic, freshness labels, or whether a cited source was actually checked. Applying its date rules to those lane fields is a scope-specific implementation choice, not a claim the RFC itself makes.
- Under QUALITY 7, the proposed tier A is only for that narrow format/calendar scope; any broader policy claim is inference and must be labelled. Under QUALITY 8, opening this source or finding it on-topic does not establish that any specific metadata value is correct or that the underlying claim is true.

## Inference and unresolved
- Inference: RFC 3339 is a primary specification source for validating the profile’s `YYYY-MM-DD` date shape and month/year day limits, but it is not authority for the lane’s freshness semantics.
- Unresolved here: whether the gate implementation and C2 tests correctly realize the frozen spec; this source-opening assignment did not inspect or run them.

VERDICT: Official RFC text opened (HTTP 200); no duplicate RFC 3339 registry row observed; proposed S034 is queued and narrowly scoped.
Installs: none.
