# ScribeRenumber — round 43

Seat: ScribeRenumber (leaf scribe). No subagent. No install. No network. No fetch.
Measured commit named by the dispatcher: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
Worktree `git rev-parse HEAD` printed that same hash. This seat did not judge, commit, push, or edit production files.

## Axes

- operability: quote the assigned map from the file that was read, with the command that hashed it.
- calibration: do not treat the map's staged ids as execution evidence when the staged append disagrees.
- depth: name the document each id actually carries, and leave the disagreement for the L1.

## One sentence

Lane S078 is not staged S078 because the lane row is the Europe PMC full-text document and the staged append has no S078 row at all: the Cochrane chapter-4 URL the map labels "staged S078" is append row S080, and that URL was not copied onto lane S078.

## Renumber map (quoted)

Path: `.ufo/waves/round-43/assimilation/renumber-map.txt`
Tracked at HEAD (`git ls-files --error-unmatch` printed the path and exited 0). `git status --short` on that path printed no lines.
`sha256sum` / `wc`:

```
7e08e3eb5cc6e1caa161d2f24dacae72ace97409ff5125626e23a9a588d024ef  .ufo/waves/round-43/assimilation/renumber-map.txt
  4 593 .ufo/waves/round-43/assimilation/renumber-map.txt
```

Full file, four lines, no added wording:

```
lane S077 | Poppler pdftotext(1) manual | stays S077 | not a staged document
staged S077 | https://doi.org/10.1186/s13643-020-01542-z | collides with lane S077 | NOT adopted (bot-wall capture) | if later adopted, next free id then, by this URL, never by overwriting lane S077
staged S118 | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML | adopted as lane S078 | URL is the evidence; S078 is the next free lane id, not S118 and not staged S078
staged S078 | Cochrane chapter 4 URL | NOT adopted | must not be copied onto lane S078; lane S078 is the Europe PMC document
```

What the map itself says, not upgraded to a staged-row fact: lane S078 is the Europe PMC document, taken as the next free lane id; staged S078 is the Cochrane chapter-4 URL, not adopted, and must not be copied onto lane S078.

## Behavior

Read-only except this report. Commands that were run, and their outcomes:

1. `sha256sum .ufo/waves/round-43/assimilation/renumber-map.txt && wc -l -c .ufo/waves/round-43/assimilation/renumber-map.txt && git rev-parse HEAD && git status --short -- .ufo/waves/round-43/assimilation/renumber-map.txt corpus/SOURCES.md corpus/knowledge/search-log-method-r39.md && git log -1 --format='%H %s' -- corpus/SOURCES.md`

```
7e08e3eb5cc6e1caa161d2f24dacae72ace97409ff5125626e23a9a588d024ef  .ufo/waves/round-43/assimilation/renumber-map.txt
  4 593 .ufo/waves/round-43/assimilation/renumber-map.txt
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
737f40b6aa8f37ffe2269db370fd6d65a720d9a8 round-43: split the absent class and adopt one locally re-opened search-log entry
```

`git status --short` printed no lines. The second hash line is `git log -1` for `corpus/SOURCES.md`, same commit.

2. `git check-ignore -v .ufo/waves/round-43/assimilation/renumber-map.txt; echo "check-ignore-exit:$?"`

```
check-ignore-exit:1
```

Not ignored. No ignore-rule line was printed.

3. `git ls-files --error-unmatch .ufo/waves/round-43/assimilation/renumber-map.txt; echo "ls-files-exit:$?"`

```
.ufo/waves/round-43/assimilation/renumber-map.txt
ls-files-exit:0
```

4. Python read of `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` (read-only; shokuknow tools not run). Source cells below were truncated at 220 characters by that script. Untruncated lines are quoted in the conflict section from the file read, not from this truncated print.

```
PATH=/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md
BYTES=144266
ROW_COUNT=111
FIRST_ID=S079
LAST_ID=S189
---WANT---
L7	S079	PRISMA-S: an extension to the PRISMA Statement for Reporting Literature Searches in Systematic Reviews (Rethlefsen, Kirks, Ayala, Moher, Page, Koffel; PRISMA-S Group, Systematic Reviews 10:39) — https://doi.org/10.1186/s
L8	S080	Cochrane Handbook for Systematic Reviews of Interventions, Chapter 4: Searching for and selecting studies (Lefebvre, Glanville, Briscoe, Featherstone, Littlewood, Metzendorf, Noel-Storr, Paynter, Rader, Thomas, Wieland; 
L46	S118	FEVER: a Large-scale Dataset for Fact Extraction and VERification (Thorne, Vlachos, Christodoulopoulos, Mittal) — NAACL-HLT 2018, doi 10.18653/v1/N18-1074 — https://aclanthology.org/N18-1074.pdf
L48	S120	A systematic approach to searching: an efficient and complete method to develop literature searches (Bramer, de Jonge, Rethlefsen, Mast, Kleijnen) — J Med Libr Assoc 2018;106(4):531-539, doi 10.5195/jmla.2018.283 — https
---URLS---
10.1186/s13643-020-01542-z	[(7, 'S079')]
chapter-04	[(8, 'S080')]
PMC6148622/fullTextXML	[(48, 'S120')]
N18-1074.pdf	[(46, 'S118')]
S078_SUBSTRING False
S077_ROW False
S078_ROW False
```

5. Python read of the lane registry and the two knowledge-entry source lines:

```
LANE_ROWS_S077=1
SOURCE_CELL_S077=Poppler `pdftotext(1)` manual — `/usr/share/man/man1/pdftotext.1.gz` (canonical project URL `http://poppler.freedesktop.org/` printed by the installed `pdftotext -v`; not fetched)
LANE_ROWS_S078=1
SOURCE_CELL_S078=Bramer, de Jonge, Rethlefsen, Mast, Kleijnen, A systematic approach to searching — Europe PMC full-text XML https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML (capture sha256 833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d; not fetched this round)
LANE_ENTRY_L3=source: S078 — https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML — section 6, byte offset 17383 of the committed capture — J Med Libr Assoc 2018;106(4):531-539, doi 10.5195/jmla.2018.283
STAGED_ENTRY_L6=source: S120 — https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML — section "6. Document the search process in a text document" and section "15. Test and reiterate" — J Med Libr Assoc 2018;106(4):531-539, doi 10.5195/jmla.2018.283
```

Lane S077's source cell matches map line 1 (pdftotext manual, not a staged document). Lane S078's source cell is the Europe PMC URL, not a Cochrane URL.

## Gates

This seat did not run C1, C2, or C3. An unrun check has not passed.

- C1 `python3 corpus/evidence/round43/c1-count.py`: not run. Not passed by this seat.
- C2 `python3 corpus/evidence/round43/c2-count.py` and `--flip S086`: not run. Not passed by this seat.
- C3 `python3 corpus/evidence/round43/c3-count.py`: not run. Not passed by this seat.
- R43-SPLIT bound: not retuned. Not recomputed.

## Touched surfaces

Wrote only `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScribeRenumber.md`.
Did not modify lane production files, the git index, jj state, the fleet repo, a sibling repo, or `/home/vgpnk/Projects/shokuknow`.

## Out of scope

- Running or editing `tools/absent-split.py` or the round-43 counters.
- Adopting, rejecting, or renumbering any registry row.
- Re-running the indented collision guard.
- Fetching any URL. Opening a capture. Hashing the Europe PMC capture.
- Sibling PROVINCE files, SHONEN boxes, QUALITY 61, the round-42 erratum.
- Installing a tool. Pacman was not invoked.

## Findings

Map line 1 agrees with the lane registry: S077 stays the pdftotext manual.

The map's staged ids do not agree with the staged append. Conflict, quoted for the L1, not resolved here.

Map line 2 says staged S077 is `https://doi.org/10.1186/s13643-020-01542-z`. The append's first row id is S079, and that DOI is on that row. The append has no row id S077 (`S077_ROW False`). Append line 7, source cell as read:

```
| S079 | PRISMA-S: an extension to the PRISMA Statement for Reporting Literature Searches in Systematic Reviews (Rethlefsen, Kirks, Ayala, Moher, Page, Koffel; PRISMA-S Group, Systematic Reviews 10:39) — https://doi.org/10.1186/s13643-020-01542-z | paper | A | ...
```

Map line 4 says staged S078 is the Cochrane chapter-4 URL and must not be copied onto lane S078. The append contains no substring `S078` (`S078_SUBSTRING False`, `S078_ROW False`). The chapter-04 URL is append row S080. Append line 8, source cell as read:

```
| S080 | Cochrane Handbook for Systematic Reviews of Interventions, Chapter 4: Searching for and selecting studies (Lefebvre, Glanville, Briscoe, Featherstone, Littlewood, Metzendorf, Noel-Storr, Paynter, Rader, Thomas, Wieland; Cochrane Information Retrieval Methods Group) — https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04 | docs | A | ...
```

Map line 3 says staged S118 is `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML`, adopted as lane S078. The append puts that URL on S120, and puts S118 on a different document. Append lines 46 and 48, source cells as read:

```
| S118 | FEVER: a Large-scale Dataset for Fact Extraction and VERification (Thorne, Vlachos, Christodoulopoulos, Mittal) — NAACL-HLT 2018, doi 10.18653/v1/N18-1074 — https://aclanthology.org/N18-1074.pdf | paper | A | ...
| S120 | A systematic approach to searching: an efficient and complete method to develop literature searches (Bramer, de Jonge, Rethlefsen, Mast, Kleijnen) — J Med Libr Assoc 2018;106(4):531-539, doi 10.5195/jmla.2018.283 — https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML | paper | A | ...
```

Same URL, different staged id, in the package's own files:

- Staged amendment `search-log-method-r39.md` line 6: `source: S120 — https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML — section "6. Document the search process in a text document" and section "15. Test and reiterate" — J Med Libr Assoc 2018;106(4):531-539, doi 10.5195/jmla.2018.283`
- Lane entry line 3: `source: S078 — https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML — section 6, byte offset 17383 of the committed capture — J Med Libr Assoc 2018;106(4):531-539, doi 10.5195/jmla.2018.283`
- `/home/vgpnk/Projects/shokuknow/merge/chousa/MERGE-REPORT.md` line 91: ``| `S120` | S078 | the complete search strategies should be designed and created in a log document rather than directly in the database, to register the steps taken and make searches accountable and reproducible, with the developed strategies copied and pasted into each database from that document; any change to the strategy should be made in the log so the log always holds the most recent version; and for systematic-review strategies the search's recall should be checked, which can be done after the review's included references have been determined |``

The lane lesson and the frozen claims repeat the map's staged id, not the append's:

- `corpus/lessons/round-43.md` line 56: `Lane ids and staged ids collide on S077 only (`assimilation/collisions`). The indented-fixture guard (`  | S118 |`) produces a nonempty collision; a column-zero-only pattern misses that indented row (`assimilation/guard/`). Lane S077 stays the pdftotext manual. Staged S077 is not adopted. The adopted document (Europe PMC URL, staged id S118) is lane S078, the next free lane id. Staged S078 is the Cochrane chapter and is not this row; it must not be copied onto lane S078.`
- `corpus/evidence/round43/claims.md` line 95: `The source opened this round is S078 (renumbered by document from staged S118; the URL is the evidence, the id follows the lane registry, never arithmetic).`

Observed arithmetic, not a cause: for these three URLs the map's staged id is the append row id minus 2 (DOI S079 called S077, Cochrane S080 called S078, Europe PMC S120 called S118). Append row S118 is the FEVER PDF, so the map's label "staged S118" names a different document than the append row with that id.

The indented guard file is not that document. As read, `.ufo/waves/round-43/assimilation/guard/indented-registry.md` is:

```
  | S118 | indented staged collision
| S077 | column-zero
    | S119 | four-space-must-miss
```

`assimilation/staged-ids` as read is 109 lines beginning `S077` and ending `S185`. That is not the append row-id set (111 rows, `S079` through `S189`). This seat did not recompute an id intersection and did not re-run the guard.

URL agreement that was observed, separate from the id disagreement: lane S078's URL equals append S120's Europe PMC URL, and it does not equal the Cochrane chapter-04 URL. The staged entry cites S120; the lane entry cites S078. Whether that re-point is the adoption the claim describes is the L1's verdict. This seat does not score it.

## Known limits

- C1, C2, and C3 were not executed here.
- The 220-character truncation is in the Python print only. The conflict quotes are from the file reads named above.
- No capture byte was opened. No digest of the Europe PMC capture was recomputed.
- `assimilation/collisions` as read is the single line `S077`. That file was not regenerated.

## Artifact paths

- Report: `.ufo/waves/round-43/w1/ScribeRenumber.md`
- Map quoted: `.ufo/waves/round-43/assimilation/renumber-map.txt` (sha256 `7e08e3eb5cc6e1caa161d2f24dacae72ace97409ff5125626e23a9a588d024ef`)

Report: .ufo/waves/round-43/w1/ScribeRenumber.md
