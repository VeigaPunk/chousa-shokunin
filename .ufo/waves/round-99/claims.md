# chousa round 99 — frozen claims (L1 `ChousaR99`)

Base `47ed34fa785288837f84cde9db15c41300854a78` (round-98 landing plus its non-author spot-check). Freeze F = the lane
commit that first carries this file; its hash is recorded in `plans/round-99.md` `## Freeze` by the next commit (a
commit cannot name its own hash — round-98 spot-check routed defect 1). Fresh-start rule: not bound (r91-r98
admitted, MANIFEST closures). Two claims, two axes, no exploratory claim. Machine form: `claims.json`.

Causal separability: C1 changes `tools/gate-records.py` only; C2 adds one knowledge entry, its registry rows and
captures. C2's gate records verify OK under the base tool and under the C1 tool alike (none of its captures is a
challenge page). ~~C1's battery reads S234's capture (C2's round, but a rejected row no entry cites) and no C2
file.~~ **A3 (F2):** C1's battery reads S234's capture (a rejected row no entry cites) and also two C2 files: POS
p1/p2 quote C2's S233 and S236 captures, and HARM reads C2's entry (`R99CriticClaims`). C1 does not depend on them:
with C2's entry and both captures deleted and p1/p2 pointed at BASE captures S225 and S231, the same battery prints
`NEG_REFUSED=7/7 POS_ADMITTED=4/4 PROD_REFUSED=4/4 HARM_SAME=24/24 … CHALLENGE_CONTROLS_R99=PASS`, exit 0
(`corpus/evidence/round99/after-f2/c1-separability.txt`).

## C1 `C1-GATE-CHALLENGE-R99` — operability (lowest axis, historical 3/10)

**Sentence.** `tools/gate-records.py verify` gains a CHALLENGE check: a url/admit record, or a rev record whose path
is `corpus/captures/<24 hex>.txt`, fails with code CHALLENGE (exit 1) when its capture's normalized, lower-cased text
has at most 200 words and contains one of the 11 frozen `CHALLENGE_MARKERS`. Through the public CLI it refuses seven
challenge-page records in a scratch lane (three committed captures — S230 reCAPTCHA, S229 cookie wall, S234 "Client
Challenge" — and four written by the battery), admits four non-challenge records (two committed captures, a
300-plus-word article that names "reCAPTCHA" and "Just a moment", a ~~30-word~~ 28-word (A1) page with no marker), refuses four records
on the production path (`--root` the lane: url/admit on S230 and S234, rev on S230 and S229 at BASE), prints output
byte-identical to the base tool on every committed knowledge/lesson file carrying GATE-RECORD lines, and five
stand-in tools (short-only, marker-only, known-bytes, scratch-only, lane-only) each fail the battery. The base tool
admits all seven challenge records.

**Counting command.**

    python3 -B corpus/evidence/round99/challenge-controls-r99.py --root . --work <scratch>

**Predicate (frozen).** stdout carries
`NEG_REFUSED=7/7 POS_ADMITTED=4/4 PROD_REFUSED=4/4 HARM_SAME=n/n BASE_NEG_ADMITTED=7/7 ORACLES_REJECTED=5/5` with
n ≥ 25 (n counts the files at the measured revision; 25 at F) and `CHALLENGE_CONTROLS_R99=PASS`; exit 0.

**Before (do-nothing control).** The base tool through the same battery (`--tool <base tool> --no-oracles`; the
oracles are patches of the candidate, so they have no base form): `NEG_REFUSED=0/7 … PROD_REFUSED=0/4 …
CHALLENGE_CONTROLS_R99=FAIL`, exit 1 (`corpus/evidence/round99/before/c1-base.txt`).

**Kill rules.** K1 any NEG or PROD record admitted, or failing with a code other than CHALLENGE alone. K2 any POS
record refused. K3 any HARM file whose stdout or exit code differs from the base tool's. K4 any oracle passing the
battery. K5 the battery passing with `--tool` = the base tool.

**Named limits.** (a) Lexical: a challenge page in other words than the 11 markers, or longer than 200 words, passes.
(b) A real document of at most 200 words that contains a marker phrase is refused (false refusal). (c) Markers are
matched after the tool's normalization only (curly quotes, whitespace, lower case): no NFKC, so full-width letters or
a zero-width character inside a marker pass. (d) The url/unreach form has no capture and is not checked; a rev
record whose path is not ~~under `corpus/captures/`~~ spelled exactly `corpus/captures/<24 lower-case hex>.txt` is not
checked — **A4 (F2):** so `./corpus/captures/<key>.txt` and `corpus/captures/<key>.raw` naming a challenge blob are
admitted (`R99ConnectorSiblings`, `R99ReviewerC1` F4). (e) The battery's oracle set is five patches; it
does not show that every wrong tool fails it. (f) QUALITY 126 detection forgers: o4/o5 detect the scratch lane by the
absence/presence of `.git`; a forger that detects the battery any other way (process tree, `S9xx` fixture ids, the
`fixture.invalid` host) is not scored. **A5 (F2) (g):** the battery does not show that each marker, the bound or the
rev-path guard is live: one-site mutants dropping any of 8 of the 11 markers, moving the bound to 199 or 201 or `<`,
dropping `norm` inside `is_challenge`, or replacing the rev branch's `CAP_RE` guard with `True` all pass it
(`R99MutantsC1`, 13/28 survive); the 11 markers and the 200-word bound are verified by reading the code
(`R99ReviewerC1` §1) and by the seats' direct probes (200 words refused, 201 admitted), not by the battery. Six of
eight one-site loosenings of the battery itself still pass the F tool and fail the base tool (`R99MutantsC1` b1-b8).
**A7 (F2):** the PROD rev legs quote the capture's first line, which is the marker line in every committed challenge
capture, so a tool that judges only the quoted line instead of the whole blob passes the battery
(`R99SentinelC1` F-4); the tool judges the whole blob (code read).
**A6 (F2) (h):** in the lane's committed store, a 12-word Chinese verification page (`712ec7bb981a9669a6921db7`)
carries no marker and is admitted (an instance of (a); `R99RevenPrior`). **A2 (F2):** the battery's docstring said
o3-o5 act "only" under their gate; they patch the url/admit call only and the rev branch stays unconditional
(`R99ReviewerC1` F2) — docstring corrected at F2, code bytes unchanged (`after-f2/c1-all.txt` header).

## C2 `C2-ENTRY-R99` — coverage (new province ground: measured quotation-error rates)

**Sentence.** New entry `corpus/knowledge/quotation-error-rates-r99.md`, sourced on S236 (Europe PMC's core record of
Jergas & Baethge 2015, the authors' own abstract, tier B) and S233 (Mogull 2017, publisher full text, tier A), both
opened this round, holds (B2: new to this lane's corpus; tameshi holds a Europe PMC record of the same abstract as its S327) 23 located quotes (J0-J8, G0-G13) and an 8-row decision table on how often a cited source
fails the citing sentence, how a mismatch is classed (major/minor, source error) and how the rate is counted. Every
~~number~~ numeral (B6: digits, as `NUM` reads them) a Do cell states is printed in one of that row's own warrant quotes. At BASE no knowledge entry contains the
phrase "quotation error" and the entry is absent.

**Counting commands.**

    python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-rates-r99.md
    bash tools/research-gate.sh verify-metadata corpus/knowledge/quotation-error-rates-r99.md --root .
    python3 -B tools/search-rerun.py verify corpus/knowledge/quotation-error-rates-r99.md --root .
    python3 -B corpus/evidence/round99/entry-controls-r99.py --root .

**Predicate (frozen).** `GATE_RECORDS files=1 records=25 ok=25 fail=0` exit 0; `METADATA_COMPLETE=1/1` and
`RESEARCH_GATE: CLEAN` exit 0; `rev_match=4/4` and `SEARCH_RERUN: CLEAN` exit 0; controls tally
`QUOTES=23/23 FIELD=9/9 IDENTITY=2/2 WARRANTS=8/8 NUMBERS=6/6 TOPIC=1/1 NUMBERS_SOURCED=6/6 BASE_TOPIC_HITS=0
BASE_ENTRY=absent FORGERY_REFUSED=10/10 ACCEPTED=2/2` and `ENTRY_CONTROLS_R99=PASS`, exit 0.

**Before.** Entry absent at BASE: `gate-records.py verify` exit 2 (`GATE_RECORDS_ERROR missing`), controls exit 2;
`BASE_TOPIC_HITS=0` (`corpus/evidence/round99/before/c2-base.txt`).

**Kill rules.** K1 a quote not in its source's capture, or a J quote outside its JSON field. K2 a Do-cell number not
printed in that row's warrant quotes. K3 the S236 record is not Jergas & Baethge 2015 (pmid, doi, year, journal,
volume) or S233's capture lacks its doi/title. K4 a forgery accepted or a no-claim edit refused. K5 a decision row's
Do cell states what its warrant quotes do not say (a paraphrase that widens or reverses a quote) — judged by a
reviewer, not by the controls.

**Named limits.** (a) S236 is an abstract, read through an index record (tier B). (b) Both sources are about medical
journal articles; nothing here measures the lane's own citation-failure rate. (c) The controls check numbers and
quote presence, not that a paraphrase is faithful beyond its numbers (K5 is reviewer-judged). **B1 (F2):** in
particular the controls read neither the Never cells nor a number's sense: a Do cell that reuses a warrant's number
for another quantity (G9's "15" articles as "15 studies", a CI bound as a rate) or a Never cell that states a
prohibition no quote states passes them (`R99MutantsC2` F-B2, F-D, F-F); NUMBERS matches by substring, so "11"
counts as printed inside "11,9%". Ten of sixteen one-site mutants of the controls survive (`R99MutantsC2`). (d) The two rates
(25.4% pooled over 28 studies, 14.5% re-counted over 15) count different things; the entry does not reconcile them.

## Amendments

F2 = the lane commit that first carries this section (its hash is written into `plans/round-99.md` `## Freeze` by the
commit after it). Every amendment narrows a sentence to what its instrument enforces, citing the seat artifact; no
predicate, counter code, kill rule or target changed (the C1 battery's docstring changed, its code did not).

- A1 (C1): "30-word page" → "28-word page" (`R99ReviewerC1` F1, `R99CriticClaims`).
- A2 (C1): battery docstring, o3-o5 descriptions (`R99ReviewerC1` F2).
- A3 (separability): C1's battery reads two C2 captures and C2's entry; separability probe receipt
  (`R99CriticClaims`; `after-f2/c1-separability.txt`).
- A4 (C1 limit (d)): the rev guard is keyed to the exact path spelling (`R99ConnectorSiblings`, `R99ReviewerC1` F4).
- A5 (C1 limit (g)): markers, bound and rev guard not shown live by the battery; battery loosenings
  (`R99MutantsC1`); `R99SentinelC1` F-3 (marker spellings the normalization does not undo) is limit (c).
- A6 (C1 limit (h)): a committed marker-less challenge page is admitted (`R99RevenPrior`).
- A7 (C1 limit (g)): the rev legs cannot tell a whole-blob check from a quoted-line check (`R99SentinelC1` F-4);
  `R99SentinelC1` F-1 (rev path spelling) is A4.
- B1 (C2 limit (c)): Never cells and number sense unchecked (`R99MutantsC2`).
- B2 (C2 sentence): the coverage is new to this lane's corpus, not to the fleet: tameshi holds Europe PMC records of
  both papers (its S327, Jergas & Baethge by DOI query, tier A, `mined`; its S328, Mogull's record, tier A,
  `rejected` for its own question), opened 2026-11-08 (`R99ConnectorSiblings` F4; L1 re-read of tameshi
  `corpus/SOURCES.md` rows S327-S328). The grading difference (A there, B here for an index-record abstract) is
  recorded in the lesson and routed, not absorbed.

F3 = the lane commit that first carries B3-B6 (its hash is written into `plans/round-99.md` `## Freeze` by the commit
after it). B3-B5 change the entry's prose (two sentences, one Do cell, two named-limit bullets); no quote, warrant
list, number token, counter, predicate or kill rule changed, and every C2 tally is identical at F3
(`corpus/evidence/round99/after-f3/c2-all.txt`).

- B3 (C2 entry scope): "the two quantitative syntheses of that literature that this host could read" was false — the
  2025 update's Europe PMC record answers http 200 (`R99ScoutSources` F-2); now "the two whose text this round's GETs
  returned", and the entry names the record as not held.
- B4 (C2 entry row 1, K5): "a meta-analysis of 28 studies put … major ones at 11,9%" and "a re-count per quotation"
  said more than the row's warrants (`R99ScoutSources` F-3): now "a meta-analysis that included 28 studies in its main
  analysis" (J1's words) and "a re-count put 14.5% of cited assertions in original research articles in medical
  journals inaccurate" (G10's words).
- B5 (C2 named limit): the abstract ties all rates to 28 studies; the body (not held) pools major/minor over 27
  (`R99ScoutSources` F-3).
- B6 (C2 sentence and limit (c)): NUMBERS reads numerals only; a spelled-out quantity ("one sixth" → "one third")
  passes the controls (`R99ScoutSources` F-4).
- Not an amendment (recorded): S235's flip condition ("a 200 carrying the article XML") was met by a seat's read-only
  re-open (`R99ScoutSources` F-1: attempt-2-equivalent GET, http 200, 126,445 bytes); the registry row records the
  lane's own attempt 1 (http 500) truthfully; a lane GET of that route is routed to round 100.
