# chousa round 83 — lesson

Base `a46534a51756f7e7d9bb55dd9a275156d908d84c`; egress table `8fff80ee43fbb99fb391c0f4751dbfd47c722744` (before any
fetch); prefreeze instruments `1b9b2ff8955190a3e5cd42800009d13d6b8e4e04`; freeze `3fbf8d1227a8aa317a036604edad93d7b20a149f`
(`corpus/evidence/round83/claims.md`, controls 8/8 as expected); scored landing
`81b81173f19d175e2b2a6b409b2a496d09d0b258`; after receipts `dd373b0c2e63f5503b1644af5e6660862a3faaca`.

## Gate

One record per registry row touched this round. `fetched` is the `refetch.tsv` time (UTC); `tier` is the registry
tier; each quote is located in the committed capture text of the row after whitespace collapse, at 1–25 words. All three
fetches answered HTTP 200 with `curl_rc=0` (`corpus/evidence/round57/refetch.tsv`, the three rows dated
2026-11-06T20:53Z), and every URL appears in `corpus/evidence/round83/egress-approval.md`'s intended-target table,
committed at 20:53:00Z, before the first fetch (20:53:06Z). Search query that located the two Handbook chapters:
"Cochrane Handbook chapter 7 considering bias and conflicts of interest among included studies two review authors
independently" (S009's URL was already in the registry since round 1).

```
GATE-RECORD S009 url=https://www.cochrane.org/authors/handbooks-and-manuals/mecir-manual/standards-conduct-new-cochrane-intervention-reviews-c1-c75/performing-review-c24-c75/assessing-risk-bias-included-studies-c52-c60 fetched=2026-11-06T20:53:06Z tier=A decision=admit capture=corpus/captures/ea16817cb78993196ea1a095.txt capture_sha256=3dfd10e567809633… words=24 quote="Collect the source of information for each risk of bias judgement (e.g. quotation, summary of information from a trial report, correspondence with investigator etc.)."
GATE-RECORD S212 url=https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-07 fetched=2026-11-06T20:53:07Z tier=A decision=admit capture=corpus/captures/708022d401fd771fc59bd1d9.txt capture_sha256=3b57cb03552f141d… words=14 quote="Risk-of-bias assessments in Cochrane reviews should be performed independently by at least two people"
GATE-RECORD S213 url=https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-08 fetched=2026-11-06T20:53:08Z tier=A decision=admit capture=corpus/captures/963807d173af711593fd1c45.txt capture_sha256=f5dae335fb45d593… words=16 quote="Answers to signalling questions and judgements about risk of bias should be supported by written justifications."
```

**Check command** (replaces the hand "Location command" of rounds 81–82):
`python3 tools/gate-records.py verify --root . corpus/lessons/round-83.md` → three `OK` lines, exit 0.

Registry changes (old → new):

- S009: status `queued` → `mined`; anchor "standards C53, C54, C55 table rows; page as served 2026-10-19" → "standards
  C52-C59 table rows (C53 duplicate, C54 support for judgement, C55 sources of information), as served 2026-11-06
  (capture key ea16817cb78993196ea1a095)"; teaches cell extended with "and the source of the information behind it";
  recheck `365d` → `on-release`; used-by `—` → `corpus/knowledge/appraisal-judgment-records-r83.md`. `opened` keeps its
  first date 2026-10-19.
- S212, S213: new rows, `mined`, opened 2026-11-06, recheck `on-release`, used-by the new entry.

Rejected this round (kept as a decision, no registry row): the Millard et al. finding quoted inside S212 (one reviewer
for about one-third of articles with a machine-learning tool) — reject as support for any row: it is a study result
reported by a secondary chapter, not the conduct standard; flip condition: the primary study opened and its design read.
