# ScoutSourcesFrontier32 — frontier recon

Axes: operability (census actually runs and its exit is recorded) and coverage (every registry row classified; every still-open Frontier item cited). Read-only. No installs. No counter runs. As-of date 2026-10-23.

## Validate

Command: `timeout 120 /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`

Exit: 0. Stdout (saved at `.ufo/waves/round-32/w1/ScoutSourcesFrontier32/validate.out`):

```
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

W04 does not fail the lane (`scripts/sources-census.sh:33`). Exit 0 means no E01–E12, so no row has a status outside `queued|mined|rejected` (`scripts/sources-census.sh:4`, `:658`).

## Rows due on or before 2026-10-23, or status candidate/unopened

**None. 0 of 59 registry rows.**

Method: split the `## Registry` table (`corpus/SOURCES.md:9-69`, 11 cells each, ids S001–S059). Status counts: mined 36, queued 19, rejected 4. Recheck cells: `on-release` 24, `365d` 28, `90d` 4, `180d` 3. Zero ISO dates. Zero `candidate`. Zero `unopened`. Full classification: `.ufo/waves/round-32/w1/ScoutSourcesFrontier32/registry-recheck.tsv` (`matches_filter` all false).

Due date used the census rule, not the cell text: `NNd` is due at `opened + N days`; `on-release` is not a date (`scripts/sources-census.sh:34-37`, `:675-685`). Independent calendar check, as-of 2026-10-23: earliest due is S006, S007, and S015, opened 2026-10-19, `90d`, due **2027-01-17** (86 days out). Next is S027, due 2027-01-19. No due date is on or before 2026-10-23.

Same census, overdue mode: `timeout 60 /home/vgpnk/Projects/shokunin/scripts/sources-census.sh overdue --root /home/vgpnk/Projects/shokunin --today 2026-10-23 chousa` exited 0 with 59 `cadence` lines and no `overdue` line (`.ufo/waves/round-32/w1/ScoutSourcesFrontier32/overdue.out`). Exit 0 is the script's "no overdue findings" code (`scripts/sources-census.sh:16`). `NNd` rows are printed as `cadence` even when not yet due (`:676-677`); an overdue row would be a second line.

`## Leads (unopened)` (`corpus/SOURCES.md:203-216`) is not a status cell. Six leads, none a registry row: TREC RAG site, AVeriTeC (`https://arxiv.org/html/2410.23850v1`), Check Please, DRBench, OCEBM background, Garner 2016 (HTTP 403 on 2026-10-21). Queued is not `candidate`: the 19 queued rows (S008–S012, S017–S024, S026–S028, S030–S032) stay outside this filter. S008–S012, S017, and S018 are still the rows `corpus/README.md:848-849` said were waiting to be mined.

No round-32 search-log entry and no S060. Last opening is Round 31, S057–S059, opened 2026-10-23 (`corpus/SOURCES.md:67-69`, `:92-101`).

## Frontier items still open

`## Frontier` starts at `corpus/README.md:346` and the file ends at `:968`. There is no Round 32 paragraph. Later sentences close two earlier "open" edges: pages that omit `</head>` are held ground (`:944-945`, limited by the D1 correction at `:956`), and verify-claims `"line"` / `"sha256"` binding is held ground (`:960-964`). What the latest text still calls open:

Round 31 remainder (`corpus/README.md:965-968`): line binding for a record's `## Claims` table pointers (`path:N`) in `verify` mode; chain hops; uniqueness; whether the named line is the right one for the claim's meaning; a claim with no pin is not revision-checked. Quote re-open items from rounds 29 and 30, and the L0 fetch-scope question, stay carried.

Those carried quote re-open items (`:948-952`, with C2 fetch bounds put back by `:956`): fetch bounds not held (`QUOTE_REOPEN_FETCH_BOUND_MATCH` 26/27 on 3 of 44 fresh-seed runs); pages without a `<head>` start tag; 2xx challenge pages; PDF sources; prefix and suffix disambiguation; resolver time inside the deadline; IPv6. Round 26–28 path-denylist debts carried unchanged (`:940`, `:952`).

Round 26 list kept in force (`:875`, `:891`, `:907`): concurrent JSON appenders; filesystem races; parent-root legacy rechecks; receipt gaps. The same paragraph's "pairing a span's occurrence with a named pointer line" is the table-pointer remainder at `:965`, not a second item. Receipt identity, the non-author admit/reject spot-check, and frozen-replay conformance are still named at `:831-833`. Semantic and external-source verification are out of scope by design there, not a closeable item.

Round 3 exemption gap is still the unread class this round's C2 names (`corpus/README.md:360`: "exemption is record-declared and unverifiable"; `corpus/evidence/round32/claims.md:53-56`). It is not in the round 31 "still open" sentence; C2 is the claim that would move it.

## Which open item a row opened this round could advance

**Concurrent appenders to one manifest** (`corpus/README.md:847` and `:875`).

That is the item frozen C1 is aimed at (`corpus/evidence/round32/claims.md:14-21`: the last-byte probe and the append are unlocked, so two writers can each insert a newline). No registry row teaches the lock. S001 and S013 teach the delimiter only (`corpus/SOURCES.md:11`, `:23`). A row opened this round, scoped to exclusive `flock(2)` across that probe and append, is what would ground that item. The recheck queue cannot supply it: 0 rows are due, candidate, or unopened, and none of the six leads is a lock source.

It would not be a new URL row for C2. C2 moves the round-3 exemption sentence by reading local exempt hops, and it adds no network read (`corpus/evidence/round32/claims.md:69`). Rounds 29–31 already worked `verify-claims` and `tools/quote-reopen.py`; this round's claims do not touch either (`claims.md:10-11`), so opening another quote-reopen or line-meaning source would not advance this round's frontier. Fetching an unregistered `flock(2)` page is blocked while the L0 fetch-scope question stays open (`corpus/README.md:967-968`; registered hosts are the URLs already in `corpus/SOURCES.md`).

## Limits

Did not open network URLs. Did not run `c1-count.py` or `c2-count.py`. Did not re-read SCORECARD to see whether any Frontier sentence older than round 26 was closed outside `corpus/README.md`. `on-release` (24 rows) is an event cadence, not a date, and was not treated as due. No lane production file was edited.
