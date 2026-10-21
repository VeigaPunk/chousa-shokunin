# FSourcePython — falsify S038 (Python datetime docs), round 26 attempt 1

Seat `ChousaR26R.FSourcePython`, 2026-10-21. Axis: freshness (C2 sourced claim).
Author-lane advice only; not an outside judge.

VERDICT: **S038 not falsified.** The Gate quote is verbatim at the stated
anchor, at most 25 words, and served by the cited version. The Gregorian
calendar, the day-addition rule and the year bounds are all stated by the
source. The transfer to Bash is labelled a lane design choice and inference.
Two minor residuals follow (version identity and unpinned URL); neither
changes what C2 says.

## Revisions and inputs

- Target: `0e9784bd52eca456b24d0bc40921480a47f91a2b` (from
  `corpus/evidence/round26-measured-revision.json`); `git cat-file -t` → `commit`, rc0.
  Claim base `ba3333254dd337658a4f25e7a9471f9cf4e4567e`.
- Sandbox: `git archive 0e9784bd… | tar -x -C /tmp/chousa-r26-falsify-FSourcePython/tree`, rc0.
  The lane `HEAD` observed when I took the archive was also `0e9784bd…`.
- Archive digests match the measured-revision JSON:
  `tools/research-gate.sh` c2c813f1…abc6, `corpus/SOURCES.md` 8308e629…aaa9,
  `corpus/knowledge/recheck-due-r26.md` a0995b78…7d5e,
  `corpus/evidence/round26-claims.md` dcbe2b5f…7f1c.
- Records attacked at that revision:
  - `corpus/SOURCES.md:48` (S038 row);
  - `corpus/lessons/round-26.md:44` (Gate row);
  - `corpus/knowledge/recheck-due-r26.md:1,15-19`;
  - `corpus/README.md:63,867-868`;
  - `corpus/evidence/round26-date-differential.sh`;
  - `tools/research-gate.sh:2295-2359`.

## Reopening (static public documentation only)

| command | result |
|---|---|
| `curl -sS -L -D headers.txt https://docs.python.org/3/library/datetime.html` | rc0. HTTP 200, 430438 bytes (the same byte count the build seat `SrcPythonDatetime` recorded). sha256 `4857975a…6c39`. `<title>` "… Python 3.15.0 documentation". "Last updated on Oct 21, 2026 (07:27 UTC)". Last-modified Wed, 21 Oct 2026 07:29:32 GMT, which is before the target commit time of 12:48 UTC. |
| `curl … https://docs.python.org/3.15/library/datetime.html` | HTTP 200. Byte-identical to `/3/` (`cmp` rc0, same sha256). |
| `curl … raw.githubusercontent.com/python/cpython/v3.15.0/Doc/library/datetime.rst` | HTTP 200. Tag source contains `toordinal` at rst:761, "indefinitely extended" at :502, `MINYEAR` is 1 at :84, `MAXYEAR` is 9999 at :90, and note (1) with the OverflowError bound. |
| python.org release API | Python 3.15.0 final released 2026-10-09T13:54:59Z, so "Python3.15.0 documentation served 2026-10-21" is consistent. |
| `curl … https://docs.python.org/3.14/library/datetime.html` | HTTP 200, "Python 3.14.8 documentation". Used for the version check below. |

## Checks

1. **Gate quote, exact text and location — PASS.**
   - The quote is "Return the proleptic Gregorian ordinal of the date, where
     January 1 of year 1 has ordinal 1." It is 17 words.
   - It appears verbatim in `<dd>` under `id="datetime.date.toordinal"` (served
     HTML lines 986–988). The Gate gives the location as `date.toordinal`,
     Python 3.15.0 docs, which is correct.
   - The same sentence also appears in `date.fromordinal` with a different
     lead verb. Only the `toordinal` form matches the Gate.
2. **Gregorian calendar and day addition, as taught by the row — PASS.**
   - The `date objects` section says "an idealized calendar, the current
     Gregorian calendar indefinitely extended in both directions". Footnote [2]
     names this the "proleptic Gregorian" calendar.
   - The operations table says "date2 will be timedelta.days days after
     date1. (1)". Note (1) is the first note.
3. **Year bounds — PASS.**
   - `datetime.MINYEAR` says "MINYEAR is 1." and `datetime.MAXYEAR` says
     "MAXYEAR is 9999."
   - Note (1) says: "OverflowError is raised if date2.year would be smaller
     than MINYEAR or larger than MAXYEAR."
   - Together these support the row's "within years1–9999". They also support
     the spec correction (`round26-claims.md:143-148`, cutoff
     0001-01-01..9999-12-31 → unknown) as Python's behaviour.
4. **Transfer to Bash is labelled — PASS.**
   - `recheck-due-r26.md:15-19`: "The following is **this lane's policy**,
     not a Cochrane rule [INFERENCE]: … the independent oracle uses those
     semantics. Adopting them for the Bash checker is a lane design choice."
   - `README.md:867-868`: "The generic schedule and registry policy are the
     lane's design, not Cochrane, Python or PROV requirements."
   - The S038 scope says "used by the independent oracle; not a generic
     freshness policy".
   - No record claims that S038 supports the Bash algorithm. The Bash code
     (`metadata_days_from_civil`/`metadata_civil_from_days`, a civil-days
     algorithm) has no opened source. The build seat said so
     (`SrcPythonDatetime.md`: "bash-side calendar source remains unopened").
5. **Do the Bash and Python results agree at the year bounds? — No
   contradiction (bounded fixture).**
   - The shipped differential samples only years 1900–2101, plus selftest
     cases for 2027/2028 and 9999-12-31 overflow. Years 1–1899 and 2102–9999
     were therefore unexercised.
   - I wrote `/tmp/chousa-r26-falsify-FSourcePython/bounds.py`, which runs one
     CLI call with 27 fixtures and `--as-of 5000-06-15`. The cases are:
     - 0001-01-01 plus 0, 58 and 3652058 days, which yields 9999-12-31;
     - 0001-01-01 plus 3652059, 9999999 and 10000000 days;
     - single-day leap and non-leap steps at 0001, 0004, 0100, 0400, 1582,
       1752, 1899, 8000, 9900 and 9999;
     - `00000000001d`;
     - explicit ISO rechecks 0001-01-01, 9999-12-31, 0000-12-31, 1900-02-29
       and 0400-02-29.
   - Command:
     `python3 bounds.py tree/tools/research-gate.sh /tmp/chousa-r26-falsify-FSourcePython`
     → `gate_rc 1` (expected: the overdue rows are drift), stderr empty,
     **`BOUNDS_AGREE=27/27`**, script rc0.
   - Scope: this covers the due-date field only, for the sampled points. It
     is not exhaustive equivalence.

## Residuals (minor, not falsifying)

- **R1 — version identity.**
  - S038 cites the Python 3.15.0 docs and says it is "used by the independent
    oracle". The oracle invokes bare `python3`, which is `/usr/bin/python3`,
    version **3.14.8** (`round26-date-differential.sh:17`,
    `round26-measure.sh:97`).
  - Observed: all six cited or supporting passages (toordinal, MINYEAR,
    MAXYEAR, operations row (1), note (1), "indefinitely extended") are
    present byte-for-byte in both the 3.15.0 and the 3.14.8 docs.
    `MINYEAR`/`MAXYEAR`/`date(1,1,1).toordinal()` on 3.14.8 return 1/9999/1.
  - Consequence: none for C2 today. However, the row's anchor names a
    different interpreter version from the one that ran the oracle.
- **R2 — unpinned URL.**
  - The row's URL `/3/` is a floating alias. It currently matches `/3.15/`
    byte-for-byte, but it will serve 3.16 after the next feature release, and
    the docs build was re-stamped the same morning.
  - The `on-release` recheck fits a floating URL. But the anchor
    "Python3.15.0 … served 2026-10-21" is reproducible only through
    `https://docs.python.org/3.15/library/datetime.html` or the v3.15.0 rST.
- **R3 — quote coverage.**
  - The Gate quote alone supports only the ordinal/proleptic part of the
    row's "teaches" text. The day-addition and year-bound parts rest on
    unquoted anchors (note 1, MINYEAR/MAXYEAR).
  - I verified those anchors verbatim above, so the support state is "source
    states the claim" for all three parts. This is support state only, not
    truth of any entry (QUALITY 8).

## Boundaries

- No production file except this report was written.
- No full selftest, build, lint, formatter or 8 MiB probe was run.
- No live-target probing; I only fetched static public documentation pages,
  the python.org release API and the raw CPython rST.
- Installs/updates: none.
