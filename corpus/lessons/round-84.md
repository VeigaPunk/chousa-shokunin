# chousa round 84 — lesson

Base `408ae68f9e445fc911f713d5bbb3a64dda1ab9fe` (round-83 tip); egress table `corpus/evidence/round84/egress-approval.md`
(committed before any fetch); freeze `3b616420b2dcc1f8a24a1cb9db4198c7adc8929b` (`corpus/evidence/round84/claims.md`,
counters frozen, controls script frozen); scored landing `e98e2a6be8103466943ea8c6e733d977d3a8a8a8` (controls 9/9,
both counters PASS).

## Gate

One record per registry row touched this round. `fetched` is the `refetch.tsv` time (UTC); `tier` is the registry
tier; each quote is located in the committed capture text of the row after whitespace collapse, at 1–25 words. All
three fetches answered HTTP 200 with `curl_rc=0` (`corpus/evidence/round57/refetch.tsv`, the three rows dated
2026-11-08T02:15–02:21Z), and every URL appears in `corpus/evidence/round84/egress-approval.md`'s intended-target
table, committed before the first fetch. Search query that located the PRISMA checklist PDF: "PRISMA 2020 checklist
pdf prisma-statement.org" (S017's landing page was fetched first and reverted; the checklist page linked to the PDF).

```
GATE-RECORD S214 url=https://www.prisma-statement.org/s/PRISMA_2020_checklist-ab3g.pdf fetched=2026-11-08T02:21:13Z tier=A decision=admit capture=corpus/captures/a640b15abf781e5c583d7088.txt capture_sha256=4cbf8881578dbc7b… words=17 quote="Specify all databases, registers, websites, organisations, reference lists and other sources searched or consulted to identify studies."
GATE-RECORD S018 url=https://aclanthology.org/2026.acl-long.1430/ fetched=2026-11-08T02:15:05Z tier=B decision=admit capture=corpus/captures/248b43277f376e437a356909.txt capture_sha256=0640edfc82212389… words=13 quote="aiming to link model outputs to supporting evidence to ensure traceability and verifiability"
GATE-RECORD S023 url=https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ fetched=2026-11-08T02:16:27Z tier=A decision=admit capture=corpus/captures/f5545a194c06ab421875b047.txt capture_sha256=20dc0c3ab7724e1f… words=10 quote="A related resource from which the described resource is derived."
```

**Check command**: `python3 tools/gate-records.py verify --root . corpus/lessons/round-84.md` → three `OK` lines, exit 0.

Registry changes (old → new):

- S214: new row, `mined`, opened 2026-11-08, recheck `on-release`, used-by `corpus/knowledge/search-transparency-reporting-r84.md`.
- S018: status `queued` → `mined`; anchor extended with capture key `248b43277f376e437a356909`; used-by `—` →
  `corpus/knowledge/search-transparency-reporting-r84.md`. `opened` keeps its first date 2026-10-19.
- S023: status `queued` → `mined`; anchor extended with capture key `f5545a194c06ab421875b047`; used-by `—` →
  `corpus/knowledge/search-transparency-reporting-r84.md`. `opened` keeps its first date 2026-10-21.
- S017: fetched (landing page, checklist page, checklist PDF) but reverted to `queued` — the landing page carries no
  quotable checklist text; the PDF was registered as S214 instead.

Rejected this round (kept as a decision, no registry row): S020 PROV-O (HTTP 403, three attempts), S021/S022/S032
PubMed (HTTP 203 cookie-challenge pages, no content), S022 Cochrane news URL (HTTP 404). Flip condition for S020:
a readable copy of the PROV-O recommendation opened and its `wasDerivedFrom` definition located.

## Claim outcomes

| claim | predicate at `e98e2a6b` | kill rules | verdict |
|---|---|---|---|
| C1 operability (`tools/gate-records.py` successor battery) | `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=288/288 EXPECTED_CODE=288/288 EMPTY_REFUSED=1/1 RC=4/4` PASS rc 0 | K1 held (counter PASS at landing); K2 held (288/288 expected codes, no forgery accepted); K3 held (15+5 positives all OK); K4 held (whitelist stub FAILs on fresh leg) | **verified** (measured) |
| C2 depth (`search-transparency-reporting-r84.md`) | `DEPTH_R84 entries=1 ok_entries=1 rows=11 located_quotes=12 fresh_sources=3` PASS rc 0 | K1 held (counter PASS); K2 pending (wave reviewer re-opens); K3 pending (wave reviewer checks warrants); K4 held (no base entry cites S214/S018/S023) | **verified** (counter); K2/K3 pending wave |

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| a source's landing page was fetched and queued for mining, but the quotable content lived in a linked PDF; the registry row's URL pointed to the landing page, so the depth counter's `fresh()` could not locate quotes in the wrong capture | `corpus/evidence/round84/claims.md` C2 section (S017 reverted); `corpus/SOURCES.md` S214 row | self — the depth counter's E3 fail on first run (`quotes=7/12`) exposed the URL→capture mismatch | register the PDF as its own row (S214) with its own URL; the entry cites the row whose URL resolves to the capture holding the quotes. Shown able to fail: `DEPTH_R84=FAIL` with `E3,E6` before S214 was registered, `PASS` after |
| the `c1-b1-salad-boundary` control's overlay replaced registry rows to point `used-by` at the control entry only, breaking the real entry's `fresh()` check and making the counter FAIL on the real entry | `corpus/evidence/round84/controls/receipts/c1-b1-salad-boundary.txt` (first run: `ok=no` for real entry) | self — controls run at landing rev exposed the overlay conflict | `used-by` accepts a comma-separated list; the overlay now names both the real entry and the control entry. Shown able to fail: `DEPTH_R84=FAIL` before the fix, `PASS` after |
| the `c1-d0-donothing` control ran at the landing rev where the new entry already exists, so it PASSed instead of FAILing | `corpus/evidence/round84/controls/receipts/c1-d0-donothing.txt` (first run: `ok=yes`) | self — control semantics changed when the entry landed | the control now runs at the freeze rev (`BASE_REV=3b616420`) where the counter exists but the entry does not. Shown able to fail: `DEPTH_R84=FAIL` at base, `PASS` at landing |

## considerthese

Read `considerthese/2026-11-07.md` (never edited). The daily reflection covers rounds 81–83; no still-unimplemented
proposal is a round-84 Gate record. The r83 lesson noted "One open Gate-record S-id per daily review" as
implementable via `tools/gate-records.py verify`; this round's lesson uses that command for its three records.

## Assimilation

none — no `merge/chousa/` theme adopted this round.

## Routed to round 85

1. The depth counter's `fresh()` resolves a source's capture by the registry row's first URL. When a source's
   quotable content is in a linked document (PDF, appendix), the row must name that document's URL, not the landing
   page's. Consider a `capture=` override column or a convention for "primary document URL" vs "landing page URL".
2. The `c2-k0-donothing` control now tests the pre-repair tool (`81b81173`), not an absent tool. The counter's
   `TOOL=absent` branch is untested; a future battery could add a stub that removes `tools/gate-records.py` from the
   tree to exercise it.
3. S020 (PROV-O) remains queued after three HTTP 403 attempts; S021/S022/S032 PubMed rows return HTTP 203 cookie
   challenges. A future round could try the W3C's alternate PROV-O URL or PubMed's API endpoint.
