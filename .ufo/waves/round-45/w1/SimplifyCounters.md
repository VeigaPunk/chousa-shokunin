# SimplifyCounters — round 45 w1 report (leaf seat, report-only)

Assignment: read `corpus/evidence/round45/c1-count.py`, `c2-count.py`,
`c3-count.py` and `claims.md`; report dead code, redundancy, and logic that
could drift from the frozen predicate sentences; propose deletions only where
frozen semantics stay byte-identical in output. Also judge
`.ufo/waves/round-45/assimilation/map-staged.py`'s `cited_by` column.

## Verdict
- No deletion candidate in any of the three counters meets the byte-identical
  bar: no dead code, no redundant branch, no unreachable path whose removal
  leaves the frozen outputs unchanged. All imports, helpers, and branches are
  live under the frozen cases.
- Three drift risks found (C1 ×1, C2 ×2): each is a *check-tightening* that
  preserves today's outputs byte-for-byte; none is a deletion.
- `map-staged.py`'s `cited_by` column is misleading — confirmed empirically
  (one false citation on the committed tree; 18/55 entries carry prose-only
  S-ids the column would credit as citations). One-line fix given, with an
  id-space-collision caveat that the one-liner alone cannot cure.

## Commands run (verbatim, trimmed)
1. `python3 .ufo/waves/round-45/assimilation/map-staged.py` (from lane root),
   filtered to rows S084/S132/S139/S140:
   ```
   staged	url	key	capture_chars	quarantine_reg_id	r42_verdict	cited_by
   S084	https://www.rfc-editor.org/rfc/rfc7089.txt	d0c4a09a9de32cb91d5e3797	107130			chain-resolution-r3-amendment-2026-10-23.md
   S132	https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/data/train.json	974299ae4b5f3bdb808b36a9	10184813			evidence-snapshot-coverage-r40.md
   S139	https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/README.md	ce16d57277fedfd4f0e7750e	4771			evidence-archive-field-policy-r41.md
   S140	https://arxiv.org/html/2305.13117v3	412b146a2720ce6557268d05	144049			evidence-archive-field-policy-r41.md
   ```
2. Python scan over `merge/chousa/knowledge/corpus/knowledge/*.md`:
   source: ids vs whole-body ids. Result: 18/55 entries have prose-only ids
   (present in body, absent from their `source:` lines), e.g.:
   - `chain-resolution-r3-amendment-2026-10-23.md`: source [S105-S108],
     prose-only [S073, S078, S084]
   - `chinese-search-log-r37.md`: source [S102-S104], prose-only
     [S071, S072, S079, S101]
   - `aggregator-vs-source-r36.md`: source [S087-S089, S091, S092],
     prose-only [S003]
   - `evidence-pool-versioning-r39-amendment-2026-10-23.md`: prose-only
     [S071, S082, S095]
3. Read: three counters (full), `claims.md`, lane `corpus/SOURCES.md`
   Registry (S001-S081; no S082-S084 yet), `SKILL.md` `## Gates` section
   (rows 77-99, 21 rows), `SOURCES.append.md` rows S082-S19x.

## C1 (c1-count.py) — claims.md R45-C1
Predicate text in docstring == claims.md §C1 verbatim. Cases (a)-(e) map
1:1 to the frozen sentence; exit-code contract (0/1/2) matches the kill rule;
stub on PATH, `--timeout` passed/omitted, `timeout_s=` start-line check all
match (e) and (d).

Drift risk (low, tightening keeps outputs identical):
- Case (b): `"n_spawned=2" in end_line(rec)` / `"n_reaped=2" in end_line(rec)`
  are plain substrings, while case (a) uses word-boundary
  `\bn_spawned=0\b`. (b) would falsely accept `n_spawned=20`/`n_reaped=20`.
  Tighten (b) to the same word-boundary form (`re.search(r"\bn_spawned=2\b", …)`
  etc.). Current launcher output unaffected.
- `STUB`'s trailing `exit 9` is unreachable under the only two modes the
  harness uses (ok/hang); it is a defensive fallback, not dead weight — not a
  deletion candidate under the byte-identical rule.
- No dead imports/helpers; `end_line`/`start_has`/`dispatch`/`run` all live.

## C2 (c2-count.py) — claims.md R45-C2
Enumerated set (tools/* files + `c<N>-count*.py`/`verify-receipts.py`/
`errata-count.py` under corpus/evidence/round*) matches the predicate's set;
Gates-section scope (`## Gates` up to next `## `, `|`-start, ≥8 `|`) matches;
exit contract matches. `--list`/`--root`/`--skill` all live. No dead code.

Drift risks (tightenings; outputs identical on the committed table):
- Row rule `"exit" in line` is a substring test; the predicate says "contains
  the word `exit`". A row containing "exited"/"exiting"/"exitcode" would pass
  the row rule. Current 21 rows only use genuine `exit 0/1/2` — so
  `re.search(r"\bexit\b", line)` hardens byte-identically.
- Registration membership `any(p in r for r in rows)` is substring-based: a
  row naming a longer path that starts with an unregistered path registers the
  shorter one too (e.g. a row naming `tools/foo.sh-old` also registers
  `tools/foo.sh` if both exist). Tighten to cell-level token match
  (`p in r.split("|")` or `\b`-delimited). Current table has no such
  adjacency, so output is identical.

## C3 (c3-count.py) — claims.md R45-C3
Docstring == predicate sentence. `BINDINGS` (FIELD→S082/README, FIELD→S083/
paper, SNAP→S084/train.json) matches "their three `source:` lines";
`row_for` requires 11 cells with URL in cell 1, status `mined` in cell 7,
citing entry in cell 10 (used-by) — matches the Registry-row clause; spans
manifest 7 columns checked for in-span, in-entry, and capture-offset
(`ct[o:o+len(span)] == span`) with recorded sha256 — matches the capture
clauses; `rederive` recomputes all seven counts from the train.json capture and
counts.json must match — matches the counts clause; `--lane-only` prints
`skipped` for the two capture-bound lines and drops them from `ok` — matches
claims.md's mode contract. Counts (3,068 records; 6,511/6,510/1; 2,531/
1,145/1,386) reproduce the construction-check figures. `counts_in`'s negative
lookaround guards (`(?<![\d,])` / `(?![\d,])`) correctly reject partial-number
matches. No dead code; `key()`/`sha()`/`fmt_variants()` all live.

Minor: `url in row[1]` and `quote in span` are substrings; both match the
predicate's wording ("carrying that URL"/"sit in"), so no change proposed.

## map-staged.py judgment
`cited_by` is misleading — it misstates which entries cite a staged row.

How it works: `cites()` runs `re.findall(r"\bS\d{3}\b", …)` over the entire
entry body, so every prose mention of any S-id (wave cross-references,
backtick-quoted ids, "the lane's held `S003`" style asides) is credited as a
citation of the append row with that number. Citations in this corpus are a
specific line form (`source: S### — <URL> — scope`); any other mention is not
a citation.

Empirical proof on the committed tree:
- False positive: map-staged.py lists `chain-resolution-r3-amendment-2026-10-23.md`
  as citing staged S084. But the staged row S084 is RFC 7089 Memento
  (`SOURCES.append.md`), while that entry's only S084 mention is prose:
  "NDL's WARP (wave 2's `S084`)" — a different document, in the lane's
  numbering (lane S080 = WARP FAQ; lane has no S084 row yet). Cited-by names a
  non-citation of the wrong document.
- Scale: 18/55 entries carry prose-only ids (measured). E.g.
  `chinese-search-log-r37.md` would be credited with citing staged S101
  (a real append row) although its actual source ids are S102-S104.
- Second hazard (given in the task context, confirmed): the append's id space
  collides with the lane's planned C3 ids — append S082/S083/S084 are
  PRISMA-S/Cochrane/Memento, while lane C3 will bind S082-S084 to the
  AVeriTeC README/paper/train.json. The join uses ids only, never URLs, so any
  future reference to lane-side S082-S084 (e.g.
  `evidence-pool-versioning-r39-amendment-2026-10-23.md` prose S082) would be
  reported as citing the append's wrong documents. The two AVeriTeC entries
  themselves use S139/S140/S132, which currently join correctly — but if
  assimilation rewrites their source lines to lane S082-S084, this column
  flips them to wrong rows.

One-line fix (restrict the scan to `source:` lines):
```python
for sid in sorted(set(re.findall(r"(?m)^source:\s*(S\d{3})\b", p.read_text(encoding="utf-8")))):
```
(`cites()` in map-staged.py, line 28). Caveat to write into the script's
docstring: id-space collisions (S082-S084) are still unresolvable by id alone;
when the entry's source line carries the URL (it does), the join should verify
URL equality against the row and flag mismatches rather than trust the number.

## Tradeoff
No deletions made (report-only seat); the three tightenings are proposals that
keep every current output byte-identical while closing the drift windows above.
The map-staged fix changes the `cited_by` contents (removes prose-credited
citations) — that is the intended correction, not a behavior regression.

## Pointers
- c1-count.py#CC96: lines 94 (a: word-boundary), 98-99 (b: substring), 103-105
  (c); drift at 98-99.
- c2-count.py#D28F: line 53 (`"exit" in line`), line 71 (`p in r`).
- c3-count.py#72FC: lines 44-47, 107-110, 118-131, 133-146 (all consistent).
- map-staged.py#BB06: line 28 (`cites()` body scan) — the fix site.
- SOURCES.append.md: S082-S084 rows (PRISMA-S/Cochrane/Memento).
- SOURCES.md#F7F6: Registry ends at S081 (lines 88-91) — no lane S082-S084 yet.
- SKILL.md#083F: `## Gates` rows 77-99.
