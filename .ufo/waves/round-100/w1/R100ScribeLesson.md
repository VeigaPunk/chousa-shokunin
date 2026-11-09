# R100ScribeLesson — round-100 lesson scribe: falsification findings

Seat: `R100ScribeLesson` (scribe). Lane `chousa`, round 100, wave 1. Tree attacked: shared clone
`/fast/scratch/hyaku/chousa-r100/R100ScribeLesson/repo` at `6d4e8487ee6a16823c24a8e085c6559b92b9fec8` (freeze F),
base `929c784c63a1fd17961d21742101b2b109b7b8ff`. Clone made with
`git clone -q --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo && git -C $S/repo checkout -q 6d4e8487…`.
No production file was written; the only writes are under
`.ufo/waves/round-100/w1/` (this report and the seat-prefixed drafts/receipts) and my scratch.

Deliverables (seat spec):
- `.ufo/waves/round-100/w1/R100ScribeLesson-lesson-draft.md` — the round-100 lesson's `## Gate` and `## Mistakes`.
- `.ufo/waves/round-100/w1/R100ScribeLesson-log-draft.md` — the `LOG.md` entry draft.

---

## Findings

### F-1 (mine, novel) — S237, a row the round opened, has no `GATE-RECORD` line at the freeze; every C2 counter is blind to it

QUALITY 173 (`corpus/QUALITY.md:1110`) requires: *"every registry row the round opened, re-anchored or re-opened is
recorded in a `GATE-RECORD` line at this round's `fetched` time, or the lesson names the schema gap that prevents one."*

At F the round added three registry rows (S237, S238, S239). S238 carries 14 `GATE-RECORD` lines and S239 carries 1.
**S237 carries 0 — there is no `GATE-RECORD S237` line anywhere in the frozen tree**, and no round-100 lesson existed at
F to carry one.

Command and observed line (receipt `R100ScribeLesson-receipt-S237-no-record.txt`):

```
$ git grep -n "GATE-RECORD S237" 6d4e8487 -- .
exit=1 (1 = no match)
  S237 : 0 line(s)
  S238 : 14 line(s)
  S239 : 1 line(s)
```

Round 99 met the same clause for its two rejected rows: S232 and S235 each have a `url/unreach` line in the r99 entry
*and* the r99 lesson (`corpus/knowledge/quotation-error-rates-r99.md:152-153`,
`corpus/lessons/round-99.md:75-76`). The form fits S237 exactly — I wrote the missing line and it verifies `OK`
against the frozen tool (same receipt, `exit=0`), so **there is no schema gap to name**; the omission was silent.

Why no counter caught it: the frozen C2 counting command 1 is
`python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-update-r100.md`, which reads **one
file** and counts the records that are present (`records=17 ok=17 fail=0`). It never asks about S237.
`corpus/evidence/round100/entry-controls-r100.py` never reads `corpus/SOURCES.md` at all (no reference to the registry
anywhere in the file), so it cannot ask either. The C2 predicate line therefore certifies a file whose record count
(17) is one short of the three rows the round opened.

I wrote a coverage check that walks the rows **added** since the base and counts their records
(`R100ScribeLesson-record-coverage.py`, receipt `R100ScribeLesson-receipt-record-coverage.txt`):

```
$ python3 R100ScribeLesson-record-coverage.py 6d4e8487… <repo>
ROW S237 gate_records=0   <-- NO GATE-RECORD anywhere in the frozen tree
ROW S238 gate_records=14
ROW S239 gate_records=1
RECORD_COVERAGE rev=6d4e8487 rows_added=3 rows_without_record=1
exit=1
```

and over the working tree, which carries the S237 line in the (untracked) round-100 lesson:
`RECORD_COVERAGE rev=WORKTREE rows_added=3 rows_without_record=0`, exit 0. The check is therefore **able to fail** —
it reports exit 1 at F and exit 0 once the record exists.

Note the corrected walk is the meaningful one: the untracked `corpus/lessons/round-100.md` holds the S237 line, so a
tracked-files-only walk reports `rows_without_record=1` against the working tree too. My receipt shows both walks.

**Severity:** this is a documentation/provenance gap, not a false statement in a claim. The C2 claim sentence says the
entry "holds … 14 located quotes (U0-U13) plus J1/J2 from S236" — that is true of the entry. The gap is that the
round's *third* opened row is unrecorded, and the counters the claim is measured by cannot see it. I did not find any
wave artifact asserting a record for S237, so the claim's kill rule ("any wave artifact shows …") is not tripped by my
own artifact; the lesson must carry the record, and a coverage check should be routed.

### F-2 (mine, novel) — the round-100 approval table's "every URL below was named by a committed round-99 artifact" is false for two of the three URLs, and the lesson inherits it

`corpus/evidence/round100/egress-approval.md` states: *"No web search runs this round: every URL below was named by a
committed round-99 artifact (SCORECARD.md `## Planned — round 100` item 2; `.ufo/waves/round-99/w1/R99ScoutSources.md`)."*

Checked against the base tree (receipt `R100ScribeLesson-receipt-search-sweep.txt` and the greps below):

| row | URL | in the base tree? |
|---|---|---|
| S237 | `…/rest/PMC4627914/fullTextXML` | **yes**, verbatim (`.ufo/waves/round-99/build_spec.py:164` and 12 more files) |
| S239 | `…/rest/PMC12285159/fullTextXML` | **no** — only the fragment `PMC12285159/fullTextXML` (`R99ScoutSources.md:140`, `R99ScoutSources-ripr2025-core-record.txt:29`) |
| S238 | `…/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json` | **no** — the string `EXT_ID:40696441` appears nowhere; round 99 named the DOI form of the same endpoint (`.ufo/waves/round-99/build_spec.py:166`) and the pmid as prose (`SCORECARD.md:4428`, `corpus/README.md:1490`) |

The substantive point holds and I confirmed it: no web search was needed, because the identifiers were named. The
*sentence* says more than the evidence supports — "every URL below was named" — when what was named was the route and
the identifier, and the lane composed the exact query strings. Round 99's own approval table is the precedent for the
weaker wording: it authorized `https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML` **with the PMCID
the publisher page or the search names** — a template plus an identifier, not a URL. The lesson I drafted therefore
says the route and document were named and records that the exact S238 query string is the lane's own composition.

### F-3 (corroborates peers, adds the decisive leg) — the frozen battery cannot see a HEAD-tree capture set, and the two tools give *different* verdicts

Peers `R100ExecC1Repro` (finding 1), `R100CriticClaims` (F-1) and `R100MutantsC1` (survivor `n-cache-repoonly`) already
found that a stand-in building the capture set at `HEAD` prints the frozen PASS line; amendment A1 narrows the sentence
and named limit (f) routes the fix to round 101. I reproduce it and add the leg the wave lacked: the mutant and the
frozen tool **disagree on a case**, not merely on a tally.

Receipt `R100ScribeLesson-receipt-M1-head-tree.txt`. Mutant: one line in `capture_oids` changed from
`ls-tree -z rev -- corpus/captures/` to `ls-tree -z HEAD -- corpus/captures/`.

(a) The frozen battery passes the mutant unchanged:
```
$ python3 -B corpus/evidence/round100/challenge-controls-r100.py --root . --work <scratch> --tool M1.py --no-oracles
NEG=7/7 MARK=11/11 BOUND=3/3 NORM=2/2 POS=4/4 REV=11/11 REVPOS=3/3 PROD=6/6 HARM_SAME=27/27 BASE_REV_ADMITTED=8/11 ORACLES_REJECTED=0/0
CHALLENGE_CONTROLS_R100=PASS
exit=0
```

(b) On a two-commit fixture (capture present at the record's rev, deleted at `HEAD`), the two tools disagree:
```
--- FROZEN tool (capture set at the record's rev) ---
GATE_RECORD …/probe3.md:1 S900 FAIL CHALLENGE,REGISTRY,WORDS
--- M1 mutant (capture set at HEAD) ---
GATE_RECORD …/probe3.md:1 S900 FAIL REGISTRY,WORDS
```
The frozen tool refuses the record with CHALLENGE; the mutant does not judge it at all. The battery's single-commit
fixture cannot separate the two implementations, so the predicate line cannot certify the "of that rev's tree" clause —
which is exactly why A1 narrowed the sentence rather than the tool.

Also confirmed the tool's own resolver is consistent across 27 path spellings, so the identity rule is not itself
split-brained (receipt `R100ScribeLesson-receipt-resolver-agreement.txt`): `git rev-parse --verify --quiet rev:path`
and `git cat-file -t rev:path` agree on **0 divergences** across 27 spellings — including `./corpus//captures/…`,
`./corpus/./captures/…`, `./notes/../corpus/captures/…`, `corpus//captures/…` (both fail), `….TXT` (both fail) and
`.raw` (both resolve to the raw blob). The battery's spelling set is representative.

### F-4 (corroborates `R100ReviewerC2` B2, independently verified) — the frozen entry's GET count is false against the lane's own fetch log

At F, `corpus/knowledge/quotation-error-update-r100.md:20` says the full-text route *"answered http 500 to **both** of
this round's GETs"* and `:89` says *"this round's **two** GETs"*. `corpus/evidence/round57/refetch.tsv` holds **three**
S239 attempts (05:12:32Z, 05:18:35Z, 05:28:39Z) and three S237 attempts (05:12:31Z, 05:18:33Z, 05:28:38Z) — I
counted them from the ledger (receipt `R100ScribeLesson-receipt-getcount.txt`). The lane's own `SOURCES.md` rows say
"attempts 1-3". So the entry says two where the instrument records three, and the round-100 `SOURCES.md` search-log
line ("seven GETs") agrees with the ledger (3+1+3=7). `R100ReviewerC2` found the same defect (amendment B2, fixed in the
working tree); my contribution is the independent ledger count and the same class in the registry's own anchor cells,
which the L1 already caught in `corpus/evidence/round100/after-f2/anchor-times.txt` (`ANCHOR_TIMES rev=96835234
logged=2/6`, exit 1 at P → `logged=6/6`, exit 0 after) — the anchor cells had cited the shell's clock, not the fetch
log, the same way the entry had miscounted.

### F-5 (corroborates `R100ExecC2Repro` B3) — two of the entry's quotes are not literal substrings of the capture

Independently confirmed (receipt `R100ScribeLesson-receipt-thinspace.txt`): of U1-U13, **U9 and U11 are not literal
substrings** of S238's `abstractText` as served — the record prints U+2009 THIN SPACE where the entry prints U+0020
(`p\u2009=\u20090.85`, `ρ\u2009=\u2009-0.253`; 8 U+2009 in the field). They are located only after
`tools/gate-records.py`'s normalization (Python's `str.split()` treats U+2009 as whitespace). The entry at F says
"U1-U13 **are substrings** of its `abstractText` field" — false for U9 and U11 as written; amendment B3 narrows it and
the working tree now discloses the thin space.

I also verified the 16 quote locations and the numeral warrants independently of the lane's controls
(receipt `R100ScribeLesson-receipt-thinspace.txt` and the numbers check): all 16 locate (U0 = `title`, U1-U13 and
J1/J2 in `abstractText`, all ≤25 words), and every Do/Never numeral in the 8 decision rows is a token of that row's own
warrants (24/24, computed with the same regex the controls use) — the C2 controls' tally is honest about what it
measures.

### F-6 (mine, novel) — the round-100 lesson that the lane is assembling cites a census receipt that does not exist

The lane's in-flight `corpus/lessons/round-100.md` (untracked) says at line 18: *"Census exit 0 before
(`corpus/evidence/round100/census-start.txt`) and after (`corpus/evidence/round100/census-end.txt`)"*.
**`corpus/evidence/round100/census-end.txt` does not exist** — not at F, not in the working tree. Round 99 shipped both
(`corpus/evidence/round99/census-start.txt` and `census-end.txt`).

I reproduced the after-census myself over the freeze tree (receipt `R100ScribeLesson-receipt-census-freeze.txt`):
`bash scripts/sources-census.sh validate --root <fleet2> --today 2026-11-09 <fleet2>/chousa-shokunin` → exit 0, with
the six pre-existing W04s, the pre-existing W01, and **one new warning** `W04 S237 duplicate url
www.ebi.ac.uk/europepmc/webservices/rest/PMC4627914/fullTextXML across scopes` (S235 is round 99's attempt on the same
route; both rows rejected) — matching what the lesson says the census shows, so the content is right and only the
receipt is missing. My lesson draft names the receipt as still-to-land rather than citing an absent file.

### F-7 (mine, novel, minor) — the round-100 entry's `## Searches` sweep cannot fail: all three expressions are absent from the base capture store by construction

The new entry's `## Searches` lists Q1 `quotation inaccuracy`, Q2 `32,000 quotations`, Q3 `40696441` with hits 0 at
rev `929c784c`. I materialised the base capture store with
`git archive 929c784c… corpus/captures | tar -x -C <scratch>` and searched it (receipt
`R100ScribeLesson-receipt-search-sweep.txt`): all three give **0 capture files** — expected, since all three strings come
from the document being admitted. The lane's *topic* phrase for this ground does hit the base store: `quotation error`
→ 2 capture files (`405a0054e1f6dbd1854a3618.txt`, `4b70901ad80c513f0c2f750c.txt` — the S236 and S233 captures the
round-99 entry already mined). So the three searches attest only "the corpus did not already contain *these exact
strings*", which is a near-tautology, not a coverage sweep. Not a false statement — the sweep's numbers are honest — but
a reader could take three zero-hit searches as evidence the topic was uncovered, which it was not. Worth a line in the
lesson's limits; not claim-firing.

---

## Checks that came out clean (recorded so they are not re-run)

- **C1 frozen predicate, reproduced:** `python3 -B corpus/evidence/round100/challenge-controls-r100.py --root . --work
  <scratch>` at F → `NEG=7/7 MARK=11/11 BOUND=3/3 NORM=2/2 POS=4/4 REV=11/11 REVPOS=3/3 PROD=6/6 HARM_SAME=27/27
  BASE_REV_ADMITTED=8/11 ORACLES_REJECTED=12/12` + `CHALLENGE_CONTROLS_R100=PASS`, exit 0 — character-for-character the
  frozen predicate. Base tool through the same battery: `REV=3/11 PROD=4/6 … FAIL`, exit 1
  (`R100ScribeLesson-receipt-c1-base-repro.txt`).
- **C1's counters are not new:** the tool change is `rev_capture_text` + `capture_oids` (identity by object id) replacing
  the spelling-keyed `CAP_RE.fullmatch(kv["path"])` guard; the round-99 battery still passes against the round-100 tool
  (`CHALLENGE_CONTROLS_R99=PASS`, exit 0) — no round-99 leg regressed.
- **C2 frozen counters, reproduced at F:** `records=17 ok=17 fail=0` exit 0; `METADATA_COMPLETE=1/1` / `RESEARCH_GATE:
  CLEAN` exit 0; `rev_match=3/3` / `SEARCH_RERUN: CLEAN` exit 0; `ENTRY_CONTROLS_R100=PASS` exit 0; harm
  `records=25 ok=25 fail=0` exit 0 and `ENTRY_CONTROLS_R99=PASS` exit 0. All four C2 counting commands and the harm leg
  reproduce exactly as frozen.
- **Decision-row numerals:** independently recomputed 24/24 tokens-in-warrants over the 8 rows; all 16 quotes locate in
  the right capture field; all ≤25 words.
- **Resolver agreement:** 0 divergences over 27 path spellings (F-3).

## Routed (not fixed by me — production files are out of scope for this seat)

1. Add the S237 `url/unreach` `GATE-RECORD` line to the round-100 lesson (my draft carries it) and land
   `corpus/evidence/round100/census-end.txt` — the lesson must not cite an absent receipt.
2. Route a coverage check that walks the rows added since the base and counts their records, so an opened row without a
   record fails instead of passing unnoticed (F-1).
3. Route the two-commit fixture with cross-rev legs and a two-rev single-file record to round 101 (A1, named limit (f)) —
   the semantic leg in F-3 is the shape it must take.
4. Narrow the approval table's "every URL below was named" to what round 99 actually named (route + identifier), and
   note in the lesson that the S238 query string is the lane's composition (F-2).
5. Note in the lesson's limits that the three `## Searches` expressions are absent from the base store by construction
   (F-7).

## Trail

Scratch `/fast/scratch/hyaku/chousa-r100/R100ScribeLesson/` (clone, fixtures `fx2.QA1OSJ` with `git rev-parse
--show-toplevel` asserted equal to the fixture dir before each mutating call, commits with `-c
user.name=fixture -c user.email=fixture@invalid`), removed before yield. Receipts copied into
`.ufo/waves/round-100/w1/` with the `R100ScribeLesson-` prefix: `receipt-record-coverage.txt`,
`receipt-S237-no-record.txt`, `receipt-M1-head-tree.txt`, `receipt-setup-repro.txt`, `receipt-census-freeze.txt`,
`receipt-search-sweep.txt`, `receipt-thinspace.txt`, `receipt-resolver-agreement.txt`, `receipt-getcount.txt`,
plus `record-coverage.py` (the check itself).

VERDICT: R100ScribeLesson C1 n/a — this seat drafts the lesson and the LOG entry; C1's predicate reproduces exactly and the one C1 defect I found (the battery cannot see a HEAD-tree capture set) is already routed as amendment A1, so I render no verdict.
VERDICT: R100ScribeLesson C2 n/a — this seat drafts the lesson and the LOG entry; C2's four counting commands and the harm leg all reproduce exactly, and my findings (the S237 record gap, the census receipt, the GET count) are documentation/provenance gaps I fixed in the draft rather than claim-firing, so I render no verdict.
