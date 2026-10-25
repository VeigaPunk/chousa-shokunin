# W2ConnOverlap

## Matching paths

none

Exact string `Memento-Datetime` under `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge`: no path.

## Axes

operability, calibration, depth. This seat only searches. It does not admit a note, edit `SOURCES.md`, or score C3.

## Evidence

Assigned search, quoted (ripgrep 15.2.0 (rev e89fff89ac)):

```
rg -n -F --hidden --no-ignore --stats 'Memento-Datetime' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge
```

```
0 matches
0 matched lines
0 files contained matches
56 files searched
0 bytes printed
429866 bytes searched
0.000109 seconds spent searching
0.001662 seconds total
hidden_exit:1
```

`find … -type f | wc -l` on that directory printed `56`. The same token without `--hidden` searched 55 files, also exit 1, 429866 bytes. The 56th file is `corpus/knowledge/.gitkeep`, `wc -c` = `0`. An empty file cannot hold the token. `--no-ignore` did not uncover a gitignored hit.

Case and punctuation, same root, all exit 1, no lines:

- `rg -n -F -i --no-ignore 'Memento-Datetime'`
- `rg -n -F -i --no-ignore 'Memento'`
- `rg -n -F --no-ignore 'Datetime'`
- `rg -n --no-ignore -e 'Memento.Datetime' -e 'Memento–Datetime' -e 'Memento—Datetime'`

One false friend, not a match. Case-insensitive `datetime` (not the assigned token) hits only:

```
corpus/knowledge/recheck-due-r26.md:1: … S038 — https://docs.python.org/3/library/datetime.html, Python3.15.0 date.toordinal …
```

That is Python calendar-day arithmetic. It does not contain `Memento` or `Memento-Datetime`.

Named C3 entry is absent. Not a counter run:

```
ls -la /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/citation-version-binding-r36.md
ls: cannot access '…/citation-version-binding-r36.md': No such file or directory
ls_exit:2
```

`corpus/evidence/round44/c3-count.py` defaults `ENTRY` to that path (`c3-count.py:24`) and tests `source: S079 —`, absence of `source: S081 —`, the row URL, and the quote `constitutes a promise that the resource state` (`c3-count.py:29-31,56-63`). It does not search for `Memento-Datetime`. This seat did not run `c3-count.py`. Entry absence is not reported here as `C3=FAIL`.

Outside the assigned root, so not a knowledge path: the RFC capture named in `claims.md:99-101` contains the token. `rg -c -F` on `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt` printed `51`, exit 0. One line: `2.1.1.  Accept-Datetime and Memento-Datetime` (file line 359). `corpus/SOURCES.md` has neither `Memento-Datetime` nor `7089` (`rg -n -F`, both exit 1). Wave-1 `ConnQuoteOverlap.md` is not on disk.

## Findings

1. No knowledge overlap on the header name. Fifty-six files, including the empty `.gitkeep`, and no case or dash variant. Admitting `citation-version-binding-r36.md` would be a new file, not an edit of a note that already says `Memento-Datetime`.

2. Homonym, do not absorb — `revision-binding-r31.md`. It pins a claim-record `"sha256"` to source-file bytes (`revision-binding-r31.md:9-11`). That is a content digest, not an HTTP `Memento-Datetime`.

3. Homonym, do not absorb — `line-binding-r31.md`. It binds a span to a line or range via RFC 5147 (`line-binding-r31.md:3,9`). A line number is not a version datetime.

4. Homonym, do not absorb — `citation-chain-fidelity-r24.md`. `resolved` is locator existence, not version identity (`citation-chain-fidelity-r24.md:9`). Hop fidelity does not own the Memento header.

5. False friend, do not absorb — `recheck-due-r26.md:1`. `datetime.html` is S038's calendar arithmetic. Folding it into a Memento hit would make the overlap scan mean two mechanisms.

6. Token present, different surface. The capture has 51 occurrences; knowledge and `SOURCES.md` have zero. A later entry can satisfy C3 without ever writing `Memento-Datetime`, because the counter does not require that string. Writing the string into some other knowledge file would not by itself pass C3. This negative is an overlap result, not a depth score.

Proposed move (calibration up, operability unharmed; frontier text only, do not edit frozen `claims.md` or knowledge): state two non-claims. (a) No current knowledge path is a prior holder of `Memento-Datetime`; do not retitle `revision-binding-r31.md`, `line-binding-r31.md`, or `recheck-due-r26.md` to cover it. (b) Do not treat this grep's exit 1 as `C3=PASS` or `C3=FAIL`.

## Limits

Search root was `corpus/knowledge` only. Sibling `PROVINCE.md` files are W2ConnSibling's seat. This seat did not fetch, did not run `c3-count.py`, and did not open every capture line beyond the count and one quoted heading. The 51 capture hits show the token exists off-root; they do not show that a knowledge note should quote all 51. Risk if ignored: a parent treats `datetime.html` or revision-binding as already owning the header, or treats "none" as a C3 measurement.
