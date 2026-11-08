# chousa round 85 — lesson

Base `43c3f7284eee4889cdcc6ac1626573f6579cd533`; prefreeze controls and the egress table
`corpus/evidence/round85/egress-approval.md` committed at the freeze
`5d0b94139ae8baf60d6f630715bc495f0a93b448`; claims freeze amendment `02df67db4f9ad39f8ebc73984ce50ea1fbea315f`
(alignment to the measured ground: S215/S026/S024, not S023 re-quote).

## Gate

One record per registry row opened or re-anchored this round. `fetched` is the `refetch.tsv` time (UTC); `tier` is the
registry tier; each quote is located in the committed capture text of the row after whitespace collapse, at 1–25 words.

```
GATE-RECORD S215 url=https://www.w3.org/TR/prov-o/ fetched=2026-11-08T03:55:52Z tier=A decision=admit capture=corpus/captures/6e48bcc4a04d13b7b3ebb68e.txt capture_sha256=8c9aeabb466fb6d1… words=12 quote="Provenance chains comprising only Entities can be formed using the prov:wasDerivedFrom property."
GATE-RECORD S026 url=https://www.gofair.foundation/r1-2 fetched=2026-11-08T04:14:51Z tier=A decision=admit capture=corpus/captures/67983a3dbbd1d690aa648744.txt capture_sha256=27ee75739788bd9a… words=20 quote="Detailed provenance includes facets such as how the resource was generated, why it was generated, by whom, under what conditions"
GATE-RECORD S024 url=https://schema.org/lastReviewed fetched=2026-11-08T04:16:13Z tier=A decision=admit capture=corpus/captures/11d6cc56bb24adfc61eea2b4.txt capture_sha256=97fe1a6adbd2ded4… words=16 quote="Date on which the content on this web page was last reviewed for accuracy and/or completeness."
```

**Check command**: `python3 tools/gate-records.py verify --root . corpus/lessons/round-85.md` → three `OK` lines, exit 0.

Search queries that located the two newly opened sources: "GO FAIR R1.2 provenance metadata" (S026 row was queued
since round 21 with its URL; the page was opened this round) and "schema.org lastReviewed property" (S024, same).
S215 is the W3C's alternate PROV-O URL; the canonical `REC-prov-o-20130430` URL answered HTTP 403 on three attempts in
round 84 and again this round (rows in `refetch.tsv`, `curl_rc=22`), so the alternate URL carries the row.

Registry changes (old → new):

- S215: new row, `mined`, opened 2026-11-08, recheck `365d`, used-by `corpus/knowledge/provenance-recording-r85.md`.
- S026: status `queued` → `mined`; anchor gains the capture key `67983a3dbbd1d690aa648744`; `teaches` rewritten to
  the located quote's facets; opened date 2026-10-21 kept (first open), used-by `—` → the new entry.
- S024: status `queued` → `mined`; anchor gains the capture key `11d6cc56bb24adfc61eea2b4`; opened date 2026-10-21
  kept; used-by `—` → the new entry.
- S023: `used-by` unchanged (the round-84 entry keeps it). A re-open row (attempt 2, HTTP 200, 2026-11-08T03:54:40Z)
  exists in `refetch.tsv`; the round-84 `modified` Definition repair stands in that entry, and the new entry does not
  re-quote it (novelty, E4).
- S020: unchanged (`queued`). Its canonical URL was retried three times (403) — the alternate-URL row S215 carries
  the material instead; S020 is left for the operator's call on whether to mark it superseded by S215.

Rejected this round (kept as a decision, no registry row): none new — every candidate URL opened answered 200 and
carried a locatable quote.

## Claim outcomes

| claim | predicate at the landing revision | kill rules | verdict |
|---|---|---|---|
| C1 operability (`tools/gate-records.py` round-85 repair) | `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=354/354 EXPECTED_CODE=354/354 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1`, `GATE_RECORDS_R85=PASS` rc 0 | K1 met; K2–K4 decided by the wave | **verified** (measured at the landing revision) |
| C2 depth (`provenance-recording-r85.md`) | `DEPTH_R85 entries=1 ok_entries=1 rows=6 located_quotes=7 fresh_sources=3`, `DEPTH_R85=PASS` rc 0 | K1 met; K2–K4 decided by the wave | **verified** (counter) |

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `vacuous` — the prefreeze C2 fixed the *instrument* (S023) before the ground was measured: the depth counter's E6 requires three fresh source ids and E7 excludes ground a base entry already cites, so an entry citing S023 as its second source could never pass — the frozen predicate (`fresh_sources=2`) was unreachable by construction and only the first scoring showed it | `corpus/evidence/round85/claims.md` C2 as frozen at `5d0b9413` (`source:` S020/S023; predicate `fresh_sources=2`); scoring receipt `corpus/evidence/round85/controls/receipts/c2-d0-donothing.txt` and the E6/E7 lines of the first candidate run | none before this round — QUALITY 169 (new) | measure each `source:` id against the counter's own FRESH/E6/E7 rules before freezing (dry-run the counter on a stub entry); the round-85 fix is the C2 amendment at `02df67db` re-pointed to S215/S026/S024, and the counter's PASS on the real entry is the demonstration. Shown able to fail: the pre-amendment candidate at `5d0b9413` prints `ok=no fails=E6,E7`; the amended entry prints `ok=yes fails=-` |
| `number-drift` — the same prefreeze also predicted a 9-quote, 7-row entry while the counter's E4 novelty rule rejects every quote the round-84 entry already carries, so only 7 quotes / 6 rows were reachable | first candidate run `quotes=4/9`, `rows=7`; `corpus/knowledge/search-transparency-reporting-r84.md` Q9/Q10 | QUALITY 169 | same fix: the counter's four rules (FRESH, E6 coverage, E7 ground, E4 novelty) are read as a set before the entry is written |

## considerthese

Read `considerthese/2026-11-07.md` and `2026-11-06.md` (never edited). The newest still-unimplemented proposal is
"One open Gate-record S-id per daily review" (noted in round 83, implemented in rounds 83–84 by
`tools/gate-records.py verify` on each lesson). This round keeps that practice: the three records above are checked
by the same command, and the tool's round-85 repair is itself what the spot-check routed.

## Assimilation

none — no `merge/chousa/` theme adopted this round; the package's id drift is still unresolved in scratch and the
round's claim cap is spent on the two repairs.

## Routed to round 86

1. `tools/gate-records.py` still has no `--selftest`; the r85 counter is a separate file. A selftest inside the tool
   would let a future round prove the tool's own contract without the counter.
2. S020's canonical URL is dead for this lane (six 403 rows); decide whether S215 supersedes it (a registry append,
   not an edit) or whether the row stays queued.
3. The mutation-tester's survivor list, if any, is a round-86 fixture class (QUALITY 170 candidate).
