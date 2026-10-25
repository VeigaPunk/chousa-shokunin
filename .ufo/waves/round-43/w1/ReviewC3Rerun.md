# ReviewC3Rerun — round 43 / w1 (leaf, no dispatch)

Axes: operability, calibration, depth. This seat is the depth rerun only
(predicate R43-C3). Operability and calibration were not re-scored here.

Assigned check: re-run `corpus/evidence/round43/c3-count.py`, paste stdout and
exit code, and confirm the admitted entry cites S078 and not `source: S118`.

Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. HEAD
`737f40b6aa8f37ffe2269db370fd6d65a720d9a8` equals the measured commit
(`737f40b round-43: split the absent class and adopt one locally re-opened search-log entry`).
`git status --short` on `corpus/knowledge/search-log-method-r39.md`,
`corpus/evidence/round43/c3-count.py`, and `corpus/SOURCES.md` printed nothing.
No production file, git index, or jj state was written. No network. No tool
install. Caller checks are literal text search plus a direct read of the entry
and the counter; this seat has no semantic index, so that search is not
semantic proof.

## Verdict

Recommendation: the C3 rerun holds. The counting command printed `C3=PASS` and
exited 0. The admitted entry's source line cites S078. The string
`source: S118` is absent. No actionable defect in this seat's scope.

## Verification ledger

### 1. Counting command (canonical rerun)

```
$ python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c3-count.py; printf 'EXIT_CODE:%s\n' "$?"
ENTRY_CITES=1/1
QUOTE_LOCATED=1/1
URL_MATCH=1/1
C3=PASS
EXIT_CODE:0
```

An earlier wrapper run printed the same four script lines and exit 0. The
`EXIT_CODE:` line is the wrapper, not the counter.

The counter's citation predicate (read, not edited) is the substring pair
`"source: S078 —" in text and "source: S118 —" not in text`
(`corpus/evidence/round43/c3-count.py`, the `cites` assignment). `ENTRY_CITES=1/1`
is that pair, not a free-text scan for the token S118.

### 2. Independent citation check

The check was:

```
python3 -c '
from pathlib import Path
p = Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/search-log-method-r39.md")
text = p.read_text(encoding="utf-8")
print("HAS_SOURCE_S078", "source: S078 —" in text)
print("HAS_SOURCE_S118_CITE", "source: S118 —" in text)
print("HAS_SOURCE_S118_PREFIX", "source: S118" in text)
for i, line in enumerate(text.splitlines(), 1):
    if "S078" in line or "S118" in line:
        print(f"{i}:{line}")
'
```

Command (read-only), output verbatim:

```
HAS_SOURCE_S078 True
HAS_SOURCE_S118_CITE False
HAS_SOURCE_S118_PREFIX False
3:source: S078 — https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML — section 6, byte offset 17383 of the committed capture — J Med Libr Assoc 2018;106(4):531-539, doi 10.5195/jmla.2018.283
10:- The method says to design the complete search strategies "in a log document, instead of directly in the database itself, to register the steps taken and to make searches accountable and reproducible" (S078, capture byte offset 17383).
11:- It says "Any change to the search strategy should be done in the log document" (S078, the same capture).
12:- It says "checking searches for their recall is advised" (S078, the same capture).
27:The staged citation id was S118. The lane id is S078 because the URL is the evidence and S078 is the next free lane id. Staged S077 stays the PRISMA-S DOI and is not this row. Lane S077 stays the pdftotext manual.
```

A content search for `source: S118` in
`corpus/knowledge/search-log-method-r39.md` returned no matches.

Confirmation: the entry cites S078 (`source: S078 —` on line 3, and parenthetical
S078 on lines 10–12). It does not contain `source: S118`. Line 27 names the
staged id S118 as the id that was not adopted. That sentence is not the citation
form the counter rejects, and it is not `source: S118`.

## Findings

None. No severity-ranked defect. The rerun matches the frozen target
(`C3=PASS`, `ENTRY_CITES=1/1`, exit 0), and the citation confirmation holds on
the measured tree.

## Residual risk

- The counter's negative check is the exact citation form `source: S118 —`, not
  a ban on the token S118. The current entry uses that token only in the
  staged-id disclosure on line 27, which does not fail the frozen predicate.
  A later edit that cited S118 under different punctuation, while keeping
  `source: S078 —`, would still print `ENTRY_CITES=1/1`. That is a width limit
  of the frozen counter, not a miss on this tree. The bound is not retuned here.
- `QUOTE_LOCATED=1/1` and `URL_MATCH=1/1` are the counter's own lines from this
  run. This seat did not byte-search the capture and did not re-derive the
  capture key. Those legs are outside the citation confirmation.

## Verification gaps

- No fetch. The capture was not re-opened by this seat.
- No semantic reference index. Citation presence is literal text in the one
  admitted entry, which is what the counter reads.
- Worktree cleanliness was checked only for the three C3 inputs named above.
  Those three were clean at HEAD `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
