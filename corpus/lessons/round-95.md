# Round 95 — a recorded search becomes re-runnable, and PRISMA-S is held in its own words (2026-11-08)

Base `7b2373586fb70f0ead6446c671fcc8b546d3e687` (round-94 landing + its non-author spot-check). Freeze F
`d6429e02bb4807bdb4cc26cd35f62f3c5c5dc7d2`, carrier C `d27e9891ba6d2bae8b1f6060f7c01bf13a1a6ea1`. Frozen claims:
`.ufo/waves/round-95/claims.md` / `claims.json`; plan and amendments: `plans/round-95.md`. Two claims (C1
operability capability, C2 depth), both sourced on S222. Attempt 2 of the round (`ChousaR95a2`); attempt 1's
untracked leftovers were discarded unverified (`.ufo/waves/round-95/inherited-attempt1.txt`).

## Gate

Registry: one row added, `S222` (PRISMA-S, JMLA 109(2):174-200, 2021, publisher PDF, tier A), status `mined`,
`used-by: corpus/knowledge/search-rerun-record-r95.md`. No existing row's `status`, `recheck` or `used-by` cell
changed. Census exit 0 before (`corpus/evidence/round95/census-start.txt`, 220 rows) and after
(`corpus/evidence/round95/census-end.txt`), the same five pre-existing `W04` duplicate-url warnings.
Approval table for the round's two GETs: `corpus/evidence/round95/egress-approval.md`.

- **S222 admitted.** URL `https://jmla.pitt.edu/ojs/jmla/article/download/962/1274`, accessed 2026-11-08
  (fetched `2026-11-08T22:51:39Z`, http 200, refetch.tsv row, raw sha256 `07036f03…`, txt sha256 `86f1aacd…`).
  Located quote (Table 1, item 8, 16 words): "Include the search strategies for each database and information
  source, copied and pasted exactly as run." Tier A for the scope in the row: the standard's own checklist and item
  explanations, by its authors, in the journal that published it. It grounds both claims: C1's record files the
  expression as run and the count per source (items 8 and 15) and the tool separates the two causes ITEM 15 names
  for a different re-run count; C2's entry holds nine located quotes from this capture.

GATE-RECORD S222 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-08T22:51:39Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=16 quote="Include the search strategies for each database and information source, copied and pasted exactly as run."

- **Route rejected (unreachable, not a source rejection).** The first route to the same document, Europe PMC REST
  full-text XML for PMC7839230, answered http 500 (curl rc 22) at `2026-11-08T22:51:19Z`; no bytes were stored.
  Reason: no capture; flip: a 200 on a later attempt (≤3 per URL under the approval table) would make it a second
  carrier of the same text, worth holding only if the PDF's two-column text form blocks a needed quote.

GATE-RECORD S222 url=https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7839230/fullTextXML fetched=2026-11-08T22:51:19Z tier=A decision=reject capture=none curl_rc=22 http=500 words=0 quote=none

- **Read, not registered.** S117 (PRISMA 2020 and PRISMA-S common questions, JMLA 2022) and S120 (Cochrane
  Handbook ch.4) were not re-opened; they are only the registered sources that name PRISMA-S and so put it in
  scope under the approval table. Cells unchanged.
- **Correction to the S222 row (`R95ScoutSources` F3), recorded here; the row's cells stay as committed (CORPUS
  rule 2 changes only status/recheck/used-by in place).** The row's source cell says "(co-published in Systematic
  Reviews 10:39)". The captured PDF supports the co-publication with the DOI `10.1186/s13643-020-01542-z`; the
  volume/article locator `10:39` came from the round's web-search summary, not from the capture. Read the cell as
  "co-published in Systematic Reviews (doi 10.1186/s13643-020-01542-z)".
- **Re-open by a non-author seat.** `R95ScoutSources` re-fetched the URL into its own scratch: raw sha256
  `07036f03…` and `pdftotext -layout` sha256 `86f1aacd…` both equal the refetch.tsv row; no erratum or newer
  PRISMA-S version was found (five web searches, `.ufo/waves/round-95/w1/R95ScoutSources-E-erratum.txt`).

`python3 -B tools/gate-records.py verify --root . corpus/lessons/round-95.md` → landing receipt
`corpus/evidence/round95/after-f2/lesson-gate.txt`.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| a report sentence states a tally from memory instead of from the instrument | round-94 report `.ufo/reports/round-94/chousa.md:188` and `:224` say "9 `falsifies-wording`, 1 `falsifies-number`, 9 `neutral`"; `awk -F'\t' '{c[$3]++} END{for(k in c) print k, c[k]}' .ufo/waves/round-94/claim-falsification.tsv` prints `falsifies-wording 8`, `falsifies-number 1`, `neutral 10` (no header row) — round-94 spot-check D1 | none (the prefile gate reads the ledger, not the report's prose about it) | the round-95 report pastes the `awk` command and its output for its own ledger instead of a recalled count; shown able to fail: the same command over the round-94 ledger disagrees with the round-94 sentence (8 ≠ 9, 10 ≠ 9) |
| a forgery case that can fail for two reasons cannot attribute the refusal | first pre-freeze run of `entry-controls-r95.py`: `CASE g7-long rc=1 expect=1 fail=['QUOTE_ABSENT'] want=QUOTE_LEN FAIL` — the 25-word stand-in was both absent from the capture and not over the limit | the battery's own one-code rule (`len(fails) == 1` and the wanted code present) | `g7-long` now uses a 32-word span that is contiguous in the text form (Table 1 items 8–9), so only `QUOTE_LEN` can refuse it; shown able to fail: the first run printed `FAIL` for that case and `ENTRY_CONTROLS=FAIL` (plan, pre-freeze fix 1) |
| an absence sentence wider than the search that supports it | the entry's first draft said the lane "never captured" PRISMA-S's full text; `/usr/bin/grep -l -i -F 'extension to the PRISMA statement for reporting literature searches' corpus/captures/*.txt` at base lists 2 captures (S120 Cochrane ch.4, S204 Campbell guide), which cite the title | none (no instrument reads an entry's prose absence claims) | the sentence now names the measured absence and its command (the item-15 sentence occurs in no base capture, `grep -l -F` exit 1); shown able to fail: the title search above returns 2 files, so the wide sentence is false on base bytes (plan, pre-freeze fix 3) |
| two located column-line fragments read as one sentence because they were adjacent in the layout text | the F entry and C2's named limit (a) said Q7–Q9 "form one sentence"; `pdftotext` without `-layout` (`.ufo/waves/round-95/w1/R95ExecC2Repro-regen-nolayout.txt`) shows Q7 ending ITEM 15's first explanation sentence and Q8/Q9 in the second (`R95ExecC2Repro` F1, `R95ScoutSources` F1); row 5's Do ("nearly the same … timeframe") rested on an unlocated line between the fragments (`R95ReviewerC2` F1) | none (gate-records locates each fragment alone; nothing reads reading order) | before joining fragments, read the reading-order text form; every load-bearing word of a Do is in a located quote (Q10/Q11 added) and `WARRANT_TERMS` requires a shared content word; shown able to fail: `entry-controls-r95.py` case `b1-nonsense-do` drops `WARRANT_TERMS` to 6/7 |
| a forgery that changes two properties at once cannot tell which check refused it | first F2-candidate `f10-dup-path` duplicated one path and dropped another, so a set-equality comparator also refused it; `mutants-r95.py` printed `MUTANT m16-set-dedup SURVIVED` and `MUTANTS_KILLED=9/10` | `corpus/evidence/round95/mutants-r95.py` (the survivor rebuild) | `f10` now lists both real paths plus a duplicate (same set, wrong list); shown able to fail: the 9/10 run above, then `MUTANTS_KILLED=10/10` |
| a novelty word ("the nearest prior instrument") stated without a fleet scan | the F sentence of C1; `R95ConnectorSiblings` P1 names tameshi `tools/count-recheck.py` (r70) and kagi `corpus/recheck-replay.py` (r56), which re-run one pinned command and compare a count | the wave's connector item | the sentence says "the lane's nearest prior instrument" and the tool docstring names both sibling mechanisms (routed, not absorbed); shown able to fail: the connector's `grep -rlE` over sibling lanes returns those two files |
