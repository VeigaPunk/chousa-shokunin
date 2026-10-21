# SrcPythonDatetime — Python datetime.date calendar (round 26, C2 oracle)

Axis: freshness (C2 due-date arithmetic). Seat: ChousaR26.SrcPythonDatetime-3, 2026-10-21.
Opened sources: 1. Installs: none. No clone/patches written (read-only seat + this report).

## Opening
- `curl -sS -o /tmp/py-dt.html -w "..." "https://docs.python.org/3/library/datetime.html"`
  → `HTTP=200 URL=https://docs.python.org/3/library/datetime.html BYTES=430438 TYPE=text/html` (2026-10-21).
- Not blocked; no mirror needed. Saved page: /tmp/py-dt.html (verbatim quotes below at its line numbers).

## (1) Verbatim located quote (23 words ≤25)
- Quote: "A date object represents a date (year, month and day) in an idealized
  calendar, the current Gregorian calendar indefinitely extended in both directions."
- Location: section "date objects", anchor `id="datetime.date"`; served HTML lines
  715-716 of /tmp/py-dt.html. Footnote [2] (lines 3484-3487): "This matches the
  definition of the "proleptic Gregorian" calendar in Dershowitz and Reingold's
  book Calendrical Calculations". Supporting anchors on same page:
  `datetime.date.toordinal` / `datetime.date.fromordinal` (lines 986 / 764,
  round-trip `date.fromordinal(d.toordinal()) == d`); `datetime.MINYEAR` /
  `datetime.MAXYEAR` (lines 304 / 311: MINYEAR is 1, MAXYEAR is 9999).

## (2) Proposed registry row — contract v1 column order, next id S034
No duplicate exists: grep `python|datetime|proleptic|gregorian` over corpus/SOURCES.md
matches no existing row (nearest: S025 RFC 9111 HTTP caching, S033 PROV-O — both unrelated).

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S034 | Python documentation, datetime — date objects — https://docs.python.org/3/library/datetime.html | docs | A | which calendar Python date arithmetic uses for C2 due-date day addition (due=V+N) and its ordinal round-trip; not the bash side, not date parsing, not recheck policy | section "date objects" (anchor datetime.date), "idealized calendar, the current Gregorian calendar indefinitely extended in both directions"; footnote [2] names Dershowitz and Reingold, Calendrical Calculations; page as served 2026-10-21, HTTP 200 | Python date arithmetic is proleptic Gregorian over years 1-9999 with fromordinal(toordinal(d))==d, so the C2 Python oracle's due=V+N days is defined in one stated calendar | queued | 2026-10-21 | 365d | — |

## (3) What this source does NOT support (QUALITY 7/8 scope limits)
- Not which calendar the gate's Bash day-add uses: C2 requires oracle and gate to
  share a calendar, but GNU date's rules are a different source (not opened). Their
  agreement is a measured observation (C2_ORACLE_AGREE), never supported by this row.
- Not ISO parsing/validation of `--as-of` or recheck tokens: format rules live in
  the strftime/strptime and fromisoformat sections, outside the quoted anchor.
- Not recheck-cadence or overdue/current semantics: freshness thresholds are the
  lane's pre-registered spec (corpus/evidence/round26-claims.md, Claim 2), not
  Python authority.
- Not historical-calendar claims: "indefinitely extended" abstracts away the
  Julian/Gregorian reform; cannot support statements about dates under historical
  calendars.
- Not arithmetic outside years 1-9999 (MINYEAR/MAXYEAR bounds): overflow there is
  out of scope; C2 inputs are bounded lane dates.
- QUALITY 8: the row states what Python's calendar is (source-states-claim); it is
  not evidence that any oracle output is true of an entry.

VERDICT: Page opened HTTP 200 2026-10-21; proleptic-Gregorian quote located at anchor datetime.date; S034 queued tier-A row proposed, no duplicate; bash-side calendar source remains unopened.
