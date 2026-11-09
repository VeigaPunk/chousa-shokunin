# R99ScoutSources — source re-open and frontier scout (round 99, wave 1)

Seat: `R99ScoutSources`. Attacked tree: `/home/vgpnk/Projects/shokunin/chousa-shokunin` @ `d41f4cd8b857c6de683e7be5c5e8125b32763a8e` (clone `--shared` under
`/fast/scratch/hyaku/chousa-r99/R99ScoutSources/repo`). No production edit, no lane git/jj mutation, no subagents.

Network was used only for the four URLs this seat was given, read-only, into the seat scratch. Nothing was written to
`corpus/captures/`, `corpus/evidence/round57/refetch.tsv`, or any lane file. All scratch was deleted before this yield.

Receipts (all under `.ufo/waves/round-99/w1/`):

| file | what it shows |
|---|---|
| `R99ScoutSources-reopen-urls.txt` | http status / bytes / markers for the four named URLs |
| `R99ScoutSources-c1-battery.txt` | C1 battery at F and with the BASE tool |
| `R99ScoutSources-c2-counting.txt` | the four C2 counting commands at F |
| `R99ScoutSources-s235-reopen.txt` | S235's route answers **200** on a second attempt |
| `R99ScoutSources-ripr2025-core-record.txt` | the 2025 synthesis' Europe PMC core record answers **200** |
| `R99ScoutSources-c1-instrument-gaps.txt` | the C1 battery does not pin `CHALLENGE_MAX_WORDS=200` nor the 11 markers |
| `R99ScoutSources-c2-numbers-gap.txt` | the C2 NUMBERS leg accepts a changed number in a Do cell |
| `R99ScoutSources-c2-wording.txt` | the entry's Do cells say more than their warrants print |
| `R99ScoutSources-post-F-lesson.txt` | read at yield time after F: the round-99 lesson and the sibling lane's DOI query |

No tool was installed or upgraded (nothing was needed; `curl`, `/usr/bin/grep` 3.12-modified, `git` 2.56.0 and Python 3.14
were already present — see `R99ScoutSources-reopen-urls.txt` and the battery receipts for the versions in use).

---

## 1. The four named URLs, re-opened

`curl -sS -L --max-time 45 -A 'Mozilla/5.0 (X11; Linux x86_64) … Chrome/124 Safari/537.36' <url>` into `$S/web`, then classified with
`tools/gate-records.py`'s own `is_challenge()` and `CHALLENGE_MARKERS`.

| # | URL | http | bytes | body | markers carried |
|---|---|---|---|---|---|
| A | `https://peerj.com/articles/1364/` | **403** | 5 644 | Cloudflare interstitial, **not** the document | `just a moment`, `enable javascript and cookies to continue` |
| B | `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4627914/fullTextXML` | **500** (1st attempt) → **200** (2nd attempt) | 150 → **126 445** | 1st: JSON server error; 2nd: the **full JATS article** | none (both attempts) |
| C | `https://researchintegrityjournal.biomedcentral.com/articles/10.1186/s41073-025-00173-z` | **200** | 3 038 | "Client Challenge" interstitial, **not** the document | `client challenge`, `a required part of this site couldn't load` |
| D | `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1186/s41073-025-00173-z&resultType=core&format=json` | **200** | 5 123 | the **document** (Europe PMC core record) | none |

Note on B: the body carries 230 normalized words (138 after the lane's own `html_to_text` recipe), i.e. **over the 200-word
cap**, and it carries no marker — so the raw body alone would not trip `is_challenge`. It is the *same* URL that the lane
recorded as an unreachable 500, and it now serves the article. See finding **F-1**.

Note on C: the raw body is 230 normalized words (37 after the lane's `html_to_text` recipe) and it *does* carry two markers.
The committed capture `b90988847e704a08aabc8321.txt` is the recipe form — 37 words, both markers, `is_challenge → True`. So
the lane's committed capture **is** detected. The round's rejection of S234 (a 200 carrying a challenge page) is correct as a
routing decision; what is wrong is that the lane never tried the *other* approved Europe PMC route to the same document
(finding **F-2**).

---

## 2. The 2025 update's Europe PMC record — it answers

Route D returned http 200 with a complete core record:

- `hitCount` 1, **pmid 40696441**, **pmcid PMC12285159**, doi `10.1186/s41073-025-00173-z`
- title **"Systematic review and meta-analysis of quotation inaccuracy in medicine."**
- `authorString` "Baethge C, Jergas H." — *the same two authors as the 2015 review the entry sources*
- `Research integrity and peer review`, vol 10, 2025, article 13; license `cc by`, `inEPMC Y`, `inPMC Y`, `hasPDF Y`

Pooled rates, quoted from the record's own `abstractText` (each ≤ 25 words):

- "identified 46 studies analyzing 32,000 quotations/references"
- "16.9% (95% CI: 14.1%-20.0%) of quotations were incorrect"
- "approximately half classified as major errors (8.0% [95% CI: 6.4%-10.0%])"
- "Heterogeneity was high, and Egger's test for small study effects remained negative throughout"
- "Meta-regression showed no significant improvement in quotation accuracy over recent years"
- "journal impact factor was: Spearman's ρ = -0.253 (p = 0.043, binomial test, N = 25)"
- "Quotation errors remain a problem in the medical literature, with no improvement over time."

**Does it contradict the entry?** No number in the entry is falsified — the two rates it carries (25.4 %, 14.5 %) are quoted
faithfully and each is located in its capture. But the entry's *scope* sentence is falsified (finding **F-2**), and the
entry's decision-table wording is wider than its warrants support (finding **F-3**). Note the denominators: 25.4 % is
**per reference** (Mogull's G2/G3 call it "the more prevalent and weighted metric of quotation errors to the references
selected"); the 2025 figure of 16.9 % is **per quotation**. They are not the same quantity and the entry does not say they are.

---

## 3. Other reachable routes to Jergas & Baethge 2015's full text (web search only — no fetch)

Search only, per the seat item. Lead URLs, in preference order:

1. `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4627914/fullTextXML` — **confirmed reachable, http 200, 126 445 bytes
   of JATS** (receipt 4). This is the lane's own approved route; it needs no new approval.
2. `https://pmc.ncbi.nlm.nih.gov/articles/PMC4627914/` — PMC full text (PMC4627914), the publisher's deposited version.
3. `https://pdfs.semanticscholar.org/0fcb/f86b9ecc0a380cc093c41fd2f742c51b668b.pdf` — open-access PDF mirror (CC BY 4.0).
4. `https://peerj.com/articles/1364/` — publisher page (403 to a plain GET; see URL A).
5. `https://europepmc.org/article/MED/26528420` and `https://europepmc.org/article/PMC/PMC12285159` — Europe PMC article pages.
6. `https://kups.ub.uni-koeln.de/80931/` and `https://kups.ub.uni-koeln.de/80931/1/s41073-025-00173-z.pdf` — the University of
   Cologne's institutional repository (KUPS) holds the **2025** update's PDF; it does **not** appear to hold a separate 2015
   author manuscript for this PeerJ article.
7. `https://cir.nii.ac.jp/crid/1360294647470993536` — CiNii Research record carrying the JATS abstract.
8. `https://ouci.dntb.gov.ua/en/works/73ZEJdQ9/` — OUCI record with the abstract.

No author manuscript of the 2015 article was found in an institutional repository; the published open-access version (PMC /
PeerJ / Semantic Scholar PDF) is the reachable full text, and route 1 above serves it from the lane's own approved host.

---

## 4. Findings

### F-1 — C2: S235's "unreachable" verdict is not reproducible; the route now serves the article

**Where.** `corpus/SOURCES.md:247` (S235 row) reads *"REJECTED (unreachable, not fabrication): the service answered a server
error; flip: a 200 carrying the article XML"*. `corpus/knowledge/quotation-error-rates-r99.md:17` repeats it: *"Europe PMC's
full-text route answered http 500, S235"*.

**Evidence.**
- `corpus/evidence/round57/refetch.tsv` has **exactly one** row for S235 (attempt 1, `curl_rc=22`, `http=500`). The lane's own
  tool docstring (`tools/capture-fetch.py:20-21`) states *"UNREACHABLE attestations (c2-count) need >= 2 failed attempts recorded
  >= 600 s apart"*. One attempt does not meet the lane's own bar for an unreachable attestation.
- Re-open, second attempt, same URL, same UA as `capture-fetch.py`:
  `curl -sS -L --max-time 45 -o body2-fulltext.bin -w '%{http_code}' …` → **http=200, 126 445 bytes**, sha256
  `c033b0493a09832723507c96fb0e2a13b4d2f3a168e9fe1e5d2147c4c543b0ab`, body begins `<!DOCTYPE article … <article
  article-type="research-article">`. Not an error page, not a challenge page.
- The body is the article: it contains `25.4% [19.5, 32.5], n = 28`, `11.9% major quotation errors [8.4, 16.6]`, `6.7%`,
  "one fourth of all references is wrong or problematic", and the same 559-studies/28-studies abstract.

**Command / exit code.** `curl … ; echo $?` → exit 0; http 200. Receipt: `R99ScoutSources-s235-reopen.txt`.

**Why it matters.** The entry's tier-B framing of the 2015 review — "read through its own published abstract in Europe PMC's
index record", and its Named limit (a) *"S236 is an abstract, read through an index record (tier B)"* — rests on a route that
answers. The full text is the authors' own article, so the entry's decision-table wording could have been checked against the
body (and, per F-3, would have failed). This is a **reachability** defect in the round's routing, not a defect in the C2
predicate: every command in C2's counting list still exits 0 at F (receipt 3). The one recorded S235 attempt also sits at odds
with the lane's own >=2-attempt rule.

### F-2 — C2: the entry's scope sentence says the literature is two syntheses; a third is reachable

**Where.** `corpus/knowledge/quotation-error-rates-r99.md:12-13`: *"This entry holds the two quantitative syntheses of that
literature that this host could read"*, and `:22-23`: *"A third route, the authors' 2025 update … answered an http 200 whose body
is a 'Client Challenge' page (S234); it is rejected for route and nothing here rests on it."*

**Evidence.**
- The 2025 synthesis is reachable at route D: http 200, 5 123 bytes, pmid 40696441 / pmcid PMC12285159, full abstract with
  pooled rates (receipt 5). This is the **same route family the lane used for S236 and S231**
  (`…/rest/search?query=EXT_ID:…&resultType=core&format=json`), only the query key differs (`DOI:` vs `EXT_ID:`).
- The round's own approval table already permitted it: `corpus/evidence/round99/egress-approval.md` row *"any of the three
  documents' Europe PMC full-text record, only if its publisher row ends in a non-200 status or a challenge page"* — S234's
  publisher row **did** end in a challenge page, so `…/rest/PMC12285159/fullTextXML` was approved for up to 3 attempts.
  `refetch.tsv` records **1** attempt for S234, and it was to the publisher page.
- The 2025 record also carries `inEPMC Y`, `inPMC Y`, `hasPDF Y`, license `cc by` — i.e. the *full text* is open and in
  Europe PMC, not just the abstract.

**Command / exit code.** `curl -sS -L … -w '%{http_code}' …` → exit 0, http 200. Receipt: `R99ScoutSources-ripr2025-core-record.txt`.

**Why it matters.** "the two … that this host could read" is false as written on the day the round landed: the 2025
synthesis — the *authors' own update* to the 2015 review, pooling **46 studies / 32 000 quotations** and reporting
**16.9 % per quotation with ~half major (8.0 %)** — is readable and was not read. The entry's own Named limit (d) says the two
rates *"count different things; the entry does not reconcile them"*; the 2025 record is precisely a synthesis that reconciles
them on a per-quotation denominator. This is a coverage gap in the round's routing decision, not an arithmetic error in the
entry.

### F-3 — C2: two Do cells say more than their own warrants print (the claim's K5, reviewer-judged)

**Where.** `corpus/knowledge/quotation-error-rates-r99.md:66` (row 1) and `:68` (row 3).

**Evidence.**
- **Row 1** warrants are `J1, J2, J5, G10`. The Do cell says *"a meta-analysis of **28 studies** put total quotation errors at
  25.4 % and **major ones at 11,9 %**"*. J1 prints *"Out of 559 studies screened we included 28 in the main analysis"* — but the
  article body (F-1's re-open) shows the pooling is **not** over 28 studies for the major rate: *"11.9 % major quotation errors
  [8.4, 16.6] … among the **27 studies** included (I²: 95 %)"*, minor *"11.5 % [8.3, 15.7] … (n = 27 studies)"*, and only the
  **total** *"25.4 % [19.5, 32.5], n = 28"*. The Do cell attributes the 28-study denominator to the 11,9 % major rate, which the
  body contradicts. The 2015 abstract (S236) does not disclose this — it says only "28 in the main analysis" — so the error is
  invisible from the tier-B capture the entry actually holds.
- **Row 1** also says *"a **re-count per quotation** put inaccurate cited assertions at 14.5 %"*. Its warrant G10 prints *"I
  estimate that 14.5 % … of cited assertions in original research articles in medical journals are inaccurate."* — G10 states no
  denominator at all. The phrase "per quotation" is G2's (*"the ratio of quotation errors to quotations examined"*), and **G2 is
  row 4's warrant, not row 1's**. A reader checking row 1 against its own warrants finds no per-quotation denominator.

**Command / exit code.** `grep -n '^| Deciding whether' corpus/knowledge/quotation-error-rates-r99.md` → the row;
`sed -n '66p'`; warrant membership tested with `norm(quote) in norm(capture)`. Receipt: `R99ScoutSources-c2-wording.txt`.

**Why it matters.** The C2 claim's own K5 is *"a decision row's Do cell states what its warrant quotes do not say (a paraphrase
that widens or reverses a quote) — judged by a reviewer, not by the controls"*. Both instances are that. The 28-vs-27 one is
factual (the body's Table 2 says 27 for major), and the per-quotation one is an unsourced denominator carried into a row
whose warrants do not contain it. Neither is caught by the frozen controls (F-4).

### F-4 — C2: the frozen NUMBERS leg does not enforce the claim's kill rule K2

**Where.** `corpus/evidence/round99/entry-controls-r99.py:100-104` — `NUM = re.compile(r"[0-9]+(?:[.,][0-9]+)*%?")` and
`nums_ok += n in wtext`.

**Evidence.** In a `--shared` clone of the lane at F with **only** the entry edited (the battery unmodified), the frozen
controls accept a changed number in a Do cell:
- Row 3 Do: *"less than one **sixth** of all quotation problems"* → *"less than one **third** of all quotation problems"* →
  `CASE NUMBERS 6/6 PASS`, `ENTRY_CONTROLS_R99=PASS`, **exit 0**. J4 prints *"less than one sixth of all quotation problems"*;
  "one third" is printed in no warrant of row 3.
- Row 5 Do: *"source errors counted as minor in about **half** the studies"* → *"… about **two thirds** of the studies"* →
  `CASE NUMBERS 6/6 PASS`, `ENTRY_CONTROLS_R99=PASS`, **exit 0**. G7 prints *"approximately half of the studies"*.
- The regex matches digit-forms only, so spelled-out numbers are never collected. And the digit-form test is *substring*, not
  token equality: row 1 Do *"quotation errors at 25.4 %"* → *"at 5.4 %"* is accepted (`"5.4%"` is a substring of `"25.4%"`),
  `NUMBERS 6/6 PASS`, exit 0. (Row 1's *"at 14.5 %"* → *"at 4.5 %"* **is** refused — exit 1 — because `4.5%` is a substring
  of no warrant number; the test is substring, not token.)
- The frozen forgery set never mutates a word-number: `entry-controls-r99.py:162` — `"f10": (text.replace(first_do, first_do +
  " (lowest 6.7%)", 1), caps)`.

**Command / exit code.** `python3 -B corpus/evidence/r99/entry-controls-r99.py --root .` in each edited lane → exit 0 (accepts the
forgery); `ENTRY_CONTROLS_R99=PASS`. Receipt: `R99ScoutSources-c2-numbers-gap.txt`.

**Why it matters.** C2's kill rule K2 is *"a Do-cell number not printed in that row's warrant quotes"*. A spelled-out number
in a Do cell is a number; the instrument never looks at one, so K2 is unenforced for exactly the quantities the entry uses in
prose form ("one sixth", "half"). The controls' own tally `NUMBERS=6/6` therefore certifies less than the claim states.

### F-5 — C1: the battery does not pin `CHALLENGE_MAX_WORDS=200` nor the 11 markers

**Where.** `tools/gate-records.py:110-127` (`CHALLENGE_MAX_WORDS = 200`, `CHALLENGE_MARKERS` = 11 phrases) and
`corpus/evidence/round99/challenge-controls-r99.py`.

**Evidence.**
- **Threshold.** Mutating only the constant and running the frozen battery with `--tool <mutant> --no-oracles`:
  `n=36` → `FAIL`; `n=37` → `PASS`; `n=50` → `PASS`; `n=201` → `PASS`; `n=300` → `PASS`; `n=380` → `PASS`; `n=381` → `FAIL`.
  The battery accepts **any** threshold in **[37, 380]** — 200 is one of 344 values it cannot distinguish.
- **Markers.** Removing one marker at a time: only `'cookies must be enabled'`, `'verify you are human'` and
  `'attention required'` are load-bearing (removing each → `FAIL`). Removing any of the other **eight** — `'checking your
  browser'`, `'recaptcha'`, `'client challenge'`, `"a required part of this site couldn't load"`, `'just a moment'`,
  `'enable javascript and cookies to continue'`, `'ddos protection'`, `'are you a robot'` — leaves the battery **PASSing**.
  Two markers (`'ddos protection'`, `'are you a robot'`) are carried by **no NEG fixture at all**; only 9 of the 11 are
  exercised (n1/n7 → 2, n2 → 1, n3 → 2, n4 → 2, n5 → 1, n6 → 1).
- The other mutants confirm the battery does pin the *shape* (drop the admit-form check → `NEG_REFUSED=0/7` FAIL; drop the
  rev-form check → `PROD_REFUSED=2/4` FAIL; lowercase only → FAIL; marker-free → `POS_ADMITTED=3/4` FAIL).

**Command / exit code.** `python3 -B corpus/evidence/round99/challenge-controls-r99.py --root . --work <dir> --tool <mutant>
--no-oracles` → exit 0 (`PASS`) for every surviving mutant above. Receipt: `R99ScoutSources-c1-instrument-gaps.txt`.

**Why it matters.** The C1 claim freezes two named numbers — `CHALLENGE_MAX_WORDS 200` and `CHALLENGE_MARKERS` **11 phrases** —
and the frozen predicate (`NEG_REFUSED=7/7 … CHALLENGE_CONTROLS_R99=PASS`) certifies neither. The lane's own QUALITY 179
("A published predicate's numeric floor is a conjunct of the instrument, not of the prose") and QUALITY 167 (mutation coverage,
not mutation count) are the applicable rules; by either, a tool with 3 load-bearing markers, or with a 50-word threshold, passes
this battery. Note this is a *strength* finding as well as a gap: the battery does pin the two-branch structure and the
lowercase-normalization behaviour tightly.

### F-6 — C1: the CHALLENGE code is not exclusive; a challenge record can still fail for other reasons

**Where.** `tools/gate-records.py` `check()`, admit branch.

**Evidence.** A `url/admit` record for S234's committed challenge capture, quoting text the capture does **not** contain:
`GATE_RECORD … S234 FAIL CHALLENGE,QUOTE_ABSENT,WORDS` (exit 1). With a wrong tier: `FAIL CHALLENGE,TIER` (exit 1). The
`verdict()` helper in the battery matches `FAIL (\S+)` — the **first** code only — so it reads `CHALLENGE` here, but the record's
failure is not attributable to CHALLENGE alone.

**Command / exit code.** `python3 -B tools/gate-records.py verify --root . <scratch>/A_nonlocated_quote.md` → exit 1, line
`… FAIL CHALLENGE,QUOTE_ABSENT,WORDS`. Receipt: `R99ScoutSources-c1-instrument-gaps.txt` §D.

**Why it matters.** The C1 claim's kill rule K1 is *"any NEG or PROD record admitted, **or failing with a code other than
CHALLENGE alone**"*. The tool cannot produce CHALLENGE alone for a record that also has another defect, so a battery that
asserts `verdict == "CHALLENGE"` (as `challenge-controls-r99.py` does) is not asserting what K1 says. In the shipped battery
this is benign — the fixtures are constructed so the quote is located and the tier is right — but the instrument's notion of
"CHALLENGE alone" is narrower than the kill rule's.

### F-7 — C2 (added after F, read at yield time): another lane's DOI query to Europe PMC was mined, tier A — the round-99 route inventory missed it

**Where.** `corpus/lessons/round-99.md:51` — *"records of both papers on 2026-11-08 — its S327 (Jergas & Baethge, DOI query, tier
**A**, `mined`) and S328 (Mogull, …)"*.

**Evidence.** A sibling lane had already mined a Europe PMC **DOI query** for this same literature, on 2026-11-08 — the day
before round 99 opened it — and graded the result **tier A** and `mined`. The round-99 entry sources the same review through
the equivalent **EXT_ID** query graded **tier B** (S236) and states that only *two* syntheses of the literature were readable
(F-2). So the route was not merely permitted by round 99's own approval table and reachable by me (receipt 5) — it was
**exercised and mined inside the lane** for the same literature, and round 99's route inventory did not use it for the 2025
paper.

**Command / exit code.** `grep -n 'S327' corpus/lessons/round-99.md` → the row; `curl … -w '%{http_code}'` on route D → exit 0,
http 200 (receipt 5).

**Why it matters.** This converts F-2 from "the host could have read a third synthesis" to "the lane had read it, on a route
another seat used, and the round did not". The entry's *"the two quantitative syntheses of that literature that this host could
read"* is therefore falsified from inside the lane's own corpus, not only from a re-open.

### F-8 — C1 (informational, low weight): the round's own round-98 receipt is now stale

`corpus/evidence/round98/gate-records-challenge-200.txt` records the base tool accepting a GATE-RECORD quoting S230's
reCAPTCHA body (`GATE_RECORD … S230 OK`, exit 0). Re-running the F tool over that committed file now prints
`GATE_RECORD … S230 FAIL CHALLENGE` (exit 1). That is the *intended* effect of C1 — but the file is a committed receipt that
now contradicts the tool, and `corpus/QUALITY.md` (unchanged base→F) still asserts at QUALITY 229 that *"tools/gate-records.py
accepts a GATE-RECORD quoting it (`OK`, exit 0, `corpus/evidence/round98/gate-records-challenge-200.txt`)"*. The QUALITY text
now describes a behaviour the tool no longer has.

**Command / exit code.** `python3 -B tools/gate-records.py verify --root . corpus/evidence/round98/gate-records-challenge-200.txt`
→ exit 1, `FAIL CHALLENGE`; with the BASE tool → exit 0, `OK`.

---

## 5. What I verified as **held**

Recorded so the reviewer does not re-derive it. All at F, all commands in receipts 2 and 3.

- **C1 predicate, as printed.** `NEG_REFUSED=7/7 POS_ADMITTED=4/4 PROD_REFUSED=4/4 HARM_SAME=25/25 BASE_NEG_ADMITTED=7/7
  ORACLES_REJECTED=5/5`, `CHALLENGE_CONTROLS_R99=PASS`, **exit 0** — reproduced exactly.
- **C1 before-control.** `--tool <BASE tool> --no-oracles` → `NEG_REFUSED=0/7 … PROD_REFUSED=0/4 … CHALLENGE_CONTROLS_R99=FAIL`,
  **exit 1** — reproduced exactly, and it matches the committed `corpus/evidence/round99/before/c1-base.txt` line for line.
- **C1 `HARM_SAME=25/25`.** The F tool and the base tool produce byte-identical stdout on all 25 committed
  knowledge/lesson files carrying GATE-RECORD lines. I re-ran the F tool over all 25 individually: 24 exit 0, and
  `corpus/lessons/round-96-verifier-spotcheck.md` exits 1 on **both** tools (a pre-existing `FAIL PARSE` at line 61, a prose
  line beginning "GATE-RECORD lines / decisions" — not a C1 regression; the base tool fails it identically).
- **C1's two-branch structure is real.** Mutants that delete the admit-form check (`NEG_REFUSED=0/7` FAIL) or the rev-form
  check (`PROD_REFUSED=2/4` FAIL) are both caught.
- **C2 predicate, as printed.** `GATE_RECORDS files=1 records=25 ok=25 fail=0` (exit 0); `METADATA_COMPLETE=1/1` +
  `RESEARCH_GATE: CLEAN` (exit 0); `rev_match=4/4` + `SEARCH_RERUN: CLEAN` (exit 0); `ENTRY_CONTROLS_R99=PASS` with
  `QUOTES=23/23 FIELD=9/9 IDENTITY=2/2 WARRANTS=8/8 NUMBERS=6/6 TOPIC=1/1 NUMBERS_SOURCED=6/6 BASE_TOPIC_HITS=0
  BASE_ENTRY=absent FORGERY_REFUSED=10/10 ACCEPTED=2/2` (exit 0) — reproduced exactly.
- **C2 quote fidelity, independently.** All 23 quotes (J0-J8, G0-G13) occur in their named capture after the tool's own
  normalization; J0 equals the record's `title` field and J1-J8 all lie inside `abstractText` (the record has exactly one
  result, `hitCount` 1). G4's wording is the capture's own past-tense Table-2 sentence, not the present-tense paraphrase that
  also appears in the capture — the entry quoted the harder one correctly.
- **C2 identity.** S236 is Jergas & Baethge 2015: pmid 26528420, doi `10.7717/peerj.1364`, pubYear 2015, journal `PeerJ`,
  volume 3, `authorString` "Jergas H, Baethge C."; the entry's title uses the record's hyphenated "articles-a" form, which is
  what the record prints (the publisher's own title uses an em dash).
- **C2 base-leg.** `BASE_TOPIC_HITS=0` and the entry absent at `47ed34fa` — I confirmed independently that no blob at BASE under
  `corpus/knowledge/` contains "quotation error", and that none of the three captures the entry depends on
  (`405a0054…`, `4b70901a…`, `b9098884…`) exists at BASE — they were all added this round.
- **S234's committed capture is reproducible.** `b90988847e704a08aabc8321.txt` sha256 `c42ccd00…` equals the `txt_sha256` in
  S234's `refetch.tsv` row, and my live re-open of the publisher URL, run through the lane's own `capture-fetch.py`
  `recipe_txt()`, reproduces that exact sha256 — so the challenge page has not changed since the round captured it, and the
  CHALLENGE check will keep firing on it.
- **QUALITY 229's lexical check still passes at F** (its `grep -lE` over the captures cited by GATE-RECORD lines prints
  nothing) — the C1 change does not disturb it.

## 6. Unresolved / limits of this seat

- I did **not** fetch the PMC HTML page or the Semantic Scholar PDF for the 2015 article: my seat item scoped the fetches to
  the four named URLs and to web-*search* for other routes. The re-open of route B is what establishes the article is
  reachable; the other URLs are search leads only.
- I did not attempt `…/rest/PMC12285159/fullTextXML` for the 2025 paper (the route the approval table permits). My seat item
  named route D for that document, and D already answers; the full-text route is a lead, not a measurement.
- The F-3 28-vs-27 finding rests on the article body as served by route B on this date. The 2015 *abstract* (S236, the capture
  the entry holds) does not disclose the 27/28 split, so the discrepancy is invisible from the entry's own warrant — that is
  the point, but it means the entry cannot be repaired by re-reading S236.
- `corpus/lessons/round-99.md` did not exist at F (the freeze commit `d41f4cd` carries `claims.md`, and the L1 landed the
  lesson after it, while I was working). **Update after F, read at yield time:** the lesson now exists and it *does* name the
  S234 schema gap for QUALITY 173 — `corpus/lessons/round-99.md:36-40`: *"No `GATE-RECORD`: the url/unreach form refuses a 2xx
  status and, from F, the url/admit form refuses the capture (CHALLENGE). The article's identity rests on a search result
  only. Flip: a 200 carrying the article text."* That discharges the QUALITY-173 concern I could not check at F. It does **not**
  discharge F-1 or F-2: the lesson's S235 line (`round-99.md:41-42`) still records *"attempted 2026-11-09T04:00:42Z, curl rc
  22, http 500. Flip: a 200 carrying the article XML"* — one attempt, and the flip condition is now met (receipt 4); and the
  lesson's web-search note (`round-99.md:25-28`) records that the search *"returned … the 2025 update on the Springer/BMC host"*
  and that *"the publisher routes were tried first, Europe PMC's after the PeerJ 403"* — i.e. Europe PMC was tried **for the
  2015 paper** (S236) but **not for the 2025 paper**, whose Europe PMC core record answers 200 (receipt 5). The lesson also
  records a *different* lane's rows S327/S328 (`round-99.md:51`, "Jergas & Baethge, DOI query, tier **A**") — a DOI query to
  Europe PMC for this very literature was mined by another lane, which corroborates route D's reachability from inside the
  lane. My F-2 finding is therefore that the round-99 *route inventory* omitted a route that (i) its own approval table
  permitted and (ii) another lane used.
- I ran every battery against a `--shared` clone of the lane at F, never against the live lane.

---

VERDICT: R99ScoutSources C1 fired — the C1 instrument does not pin the two numbers its own claim freezes (`CHALLENGE_MAX_WORDS 200`, `CHALLENGE_MARKERS` 11 phrases): mutants with thresholds of 37/50/201/300/380 and with 8 of the 11 markers removed still print `CHALLENGE_CONTROLS_R99=PASS`, and the CHALLENGE code is not exclusive, so the battery's `verdict == "CHALLENGE"` is narrower than kill rule K1's "CHALLENGE alone".
VERDICT: R99ScoutSources C2 fired — the entry's scope sentence "the two quantitative syntheses of that literature that this host could read" is false (the 2025 synthesis answers http 200 at Europe PMC with 46 studies and pooled 16.9 %/8.0 %, and a sibling lane had already mined that DOI query at tier A per corpus/lessons/round-99.md:51), S235's "unreachable" verdict does not reproduce (its URL answers http 200 with the full article on a second attempt, against the lane's own >=2-attempt rule), two Do cells say more than their own warrants print (28 studies for the 11,9 % major rate, which the body attributes to 27; "per quotation", which is G2's and not row 1's), and the frozen NUMBERS leg never inspects a spelled-out number, so kill rule K2 is unenforced for exactly the quantities the entry uses in prose form.
