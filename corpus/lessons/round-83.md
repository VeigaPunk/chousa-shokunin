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

Gate addendum for the non-author spot-check (drafted by seat `R83ScribeLesson`,
`.ufo/waves/round-83/w1/R83ScribeLesson/lesson-draft.md`, receipts under its `receipts/`):

- **admit S009** — the C55 sentence locates at capture line 494 (24 words); capture sha256 equals the `txt_sha256` of
  its refetch row (curl_rc 0, HTTP 200); registry row mined, tier A, used-by the new entry. Boundary note: the anchor says
  "C52-C59 table rows" while the page also lists `C60 Not applicable`; no row cites C60.
- **reject the Millard et al. result inside S212** — the sentence "about one-third of articles could be assessed by just
  one reviewer" locates at S212 capture line 622 inside a "Novel methods" paragraph reporting a study; the conduct
  standard is line 611. No decision row cites it (`grep -c -i millard` on the entry → 0).

## Claim outcomes

| claim | predicate at `81b81173` | kill rules | verdict |
|---|---|---|---|
| C1 depth (S009, S212, S213) | `DEPTH_R83 entries=1 ok_entries=1 rows=10 located_quotes=16 fresh_sources=3` PASS rc 0 (`corpus/evidence/round83/after/c1-after.txt`) | K1 held (`R83ExecRepro`); K2 held — 16/16 quotes in committed captures and on three HTTP 200 live re-opens byte-identical to the raw captures (`R83ExecReopen`); K3 held — all 10 rows supported, no contradicting sentence in the full paragraphs (`R83ReviewerEntry`, `R83CriticClaims` §2.2); K4 held — no base entry cites S009/S212/S213 or their URLs (`R83CriticClaims` §2.3, `R83ExecRepro`) | **verified** (measured) |
| C2 operability, capability `tools/gate-records.py` | (a) `TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3` PASS rc 0 (`after/c2-after.txt`); (b) round-83 lesson `records=3 ok=3` rc 0 | K1 held; K4 held (`R83ExecHarm`); **K2 fired** — `line=2٢٢` (ASCII 2 + Arabic-Indic digits) prints `OK` because `INT_RE` used Python's Unicode `\d` (`R83ExecForge` Finding 1, `forge/c052-line-arabic-222.md`); **K3 fired** — a genuine rev record whose quote begins with `"` is refused `FAIL PARSE` by an undocumented guard (`R83ExecHarm` 06b, `R83CriticClaims` §1.1) | **falsified by its own kill rules — honest stop** |

## Post-scoring repair (does not rescue C2)

`c7d29e1c6b9c6e11f2ec738a1d913aafb5f012d9`: every digit class in the tool is ASCII `[0-9]`, and the rev-form quote may
begin with `"`. At that revision the frozen counter still prints `GATE_RECORDS_R83=PASS` rc 0
(`corpus/evidence/round83/repair/c2-counter-repaired.txt`), the Arabic-Indic record now prints `FAIL PARSE` and the
leading-quote rev record `OK` (`repair/firing-inputs-repaired.txt`), and rounds 80–83's 18 genuine records stay `OK`.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| a parser's numeric field used Python's Unicode-aware `\d`, so a non-ASCII numeral (`2٢٢`) was read as a valid number while string comparisons elsewhere (`words`) treated the same shape as different — an inconsistent value grammar that let one forgery through and refused one genuine shape | `R83ExecForge.md` Finding 1; `tools/gate-records.py` at `81b81173` (`INT_RE = re.compile(r"0\|[1-9]\d{0,6}")`) | none — the prefreeze battery (198 forgeries) mutated values only within ASCII; the mutation seat's 36 mutants did not include a digit-class mutant | QUALITY 164: numeric fields are matched with `[0-9]` (or `re.ASCII`), and a forgery battery for a parser includes one non-ASCII numeral per numeric field. Shown able to fail: the same input printed `OK` at `81b81173` and prints `FAIL PARSE` at `c7d29e1c` (`repair/firing-inputs-repaired.txt`) |
| a form-distinguishing guard (`quote.startswith('"')` in the rev form) refused a shape the documented form allows (`quote=<text to end of line>`) | `R83ExecHarm/06b-k3-guard-isolation.txt`; `R83CriticClaims/c2-k3-rev-quote-leading-dq.txt` | none — every genuine rev record in the lane happened not to start with `"` (0/92 committed records exercise it, `R83ExecHarm`) | QUALITY 165: forms are told apart by their key sets alone; a guard on value content needs a positive control for the boundary value. Shown able to fail: `rev-quote-leading-dq.md` `FAIL PARSE` at `81b81173`, `OK` at `c7d29e1c` |
| a knowledge count taken with a per-file command counted `corpus/knowledge/.gitkeep` (round-82 report 94 → 95; `.md` count 93 → 94) | `corpus/lessons/round-82-verifier-spotcheck.md:24-25`; recount `R83ScribeLesson/receipts/01-knowledge-recount.txt` | the round-82 non-author closure (conformance defect 1) | count with `git ls-tree -r --name-only <rev> corpus/knowledge \| grep -c '\.md$'`; this round's report uses it (94 → 95 is the `.md` count at `a46534a5` → `81b81173`) |

## considerthese

Read `considerthese/2026-11-06.md` and `2026-11-05.md` (never edited). One still-unimplemented proposal: 2026-11-06
"One open Gate-record S-id per daily review". Not implemented as a daily habit this round; the new tool makes it a
one-command check (`python3 tools/gate-records.py verify --root . <lesson>`), and none of the twelve remainder ids is a
round-83 Gate record (`R83ScribeLesson/receipts/05-considerthese.txt`).

## Assimilation

none — the `merge/chousa` collision file from round 78 still lists 111 collisions against 114 staged ids
(`R83ScribeLesson/receipts/06-collisions.txt`); no package bytes read, no campaign tool run.

## Routed to round 84

1. Counter blind spots: 15/36 mutants of `tools/gate-records.py` survive the frozen battery, nine killable with committed
   lane bytes (`R83MutationTool.md` §4); a whitelist tool that accepts the 15 positive lines byte-for-byte and refuses
   everything else passes the frozen counter (`R83CriticClaims` §1.2) — a successor battery needs fresh positives the
   tool cannot list in advance.
2. Setup vs record failure: a rev record checked with a non-git `--repo` is reported `FAIL LINE,REV` (rc 1) instead of a
   setup error (rc 2) (`R83ConnectorSiblings` R1).
3. "committed lane bytes": the tool reads the worktree under `--root`; on a dirty tree a record can pass against
   uncommitted bytes (`R83SentinelScope` R1) — run it on a `git archive` tree or state the limit.
4. The depth counter passes content-free rows at the exact thresholds (`R83CriticClaims` §2.1, B1 boundary): its PASS is
   structure; content rests on K3.
5. Entry residuals (not K3 rows): the Inference's "non-author closure = second independent judgment" drops the
   independence condition; row 8's Limits could also scope against the S213 two-part "No information" antecedent
   (`R83ReviewerEntry` R-1, R-2).
