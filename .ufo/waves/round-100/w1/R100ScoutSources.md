# R100ScoutSources — source re-open and frontier scout (round 100)

**Seat:** `R100ScoutSources` · **date:** 2026-11-09 · **attacked tree:** F = `6d4e8487ee6a16823c24a8e085c6559b92b9fec8`
**Base:** `929c784c63a1fd17961d21742101b2b109b7b8ff` · **Pre-freeze build P:** `9683523467a1be9a9c46972f9b92bed26f44750d`

**Method.** Read the frozen `claims.md` first (both claims, all kill rules, all named limits), then
(a) re-opened the four URLs named in my seat item with the lane's own recipe, read-only, into seat scratch;
(b) read the resulting 2025 and 2015 article bodies; (c) re-ran every counting command of both claims against
the frozen tree; (d) probed the C1 tool with my own git fixtures; (e) one web search for a non-medical
quotation-accuracy study (leads only, nothing fetched). No lane file was modified; no corpus/captures or
refetch.tsv write; no git mutation of the lane; the live tree was read only.

**Quoting convention.** Every source fragment quoted in this report and in the receipts is a verbatim run of
the fetched article text (tags stripped, whitespace collapsed); the article's reference markers carry spaces
("[ 2 , 8 ]") and are elided between fragments. Each fragment was re-verified by exact substring match
after whitespace collapse against the fetched body.

**Receipts** (all under `.ufo/waves/round-100/w1/`, seat-name prefixed):
`R100ScoutSources-reopen-status.txt` · `-fulltext-content.txt` · `-source-vs-rows.txt` · `-flip-conditions.txt` ·
`-c1-battery.txt` · `-c1-named-limits.txt` · `-c1-battery-gap.txt` · `-c2-counters.txt` · `-quote-location.txt` ·
`-frontier-leads.txt` · `-fetch-status.txt`

---

## Summary

| Claim | Instrument | Wording | Verdict |
|---|---|---|---|
| **C1** `C1-GATE-REVCAP-R100` | green (predicate line reproduced exactly, exit 0) | **says more than its battery enforces** | **fired** (instrument gap; the tool itself is right) |
| **C2** `C2-ENTRY-UPDATE-R100` | green (all six counting commands match, exit 0) | **a decision row and the r99 `## Update` say more than the source supports** | **fired** |

Both claims' counters are green. Both claims still fire, for different reasons: C1's counting command cannot
see the one thing its sentence is about, and C2's entry carries sentences the *reachable* article body
contradicts.

---

## F-1 (C2, decisive) — the "unreachable" full text answers 200 with the lane's own recipe

`tools/capture-fetch.py` rejected S237 and S239 as unreachable on three GETs each, all `curl rc 22 / HTTP 500`.
`corpus/SOURCES.md` gives each row a flip condition, verbatim at F:

> **S239** — "REJECTED (unreachable, not fabrication): the service answered a server error to every lane GET;
> the abstract was read through S238; **flip: a 200 carrying the article XML**"

**I met that flip condition.** Same recipe as `capture-fetch.py` (`curl -fsSL --compressed --max-time 15 -A <UA>`),
same UA string (verified byte-identical by Python string compare), read-only into seat scratch:

| URL | attempt | http | bytes | body |
|---|---|---|---|---|
| `…/PMC12285159/fullTextXML` (2025) | 1 | **200** | 95 755 | **the article** (JATS XML; 0 challenge markers) |
| `…/PMC4627914/fullTextXML` (2015) | 1 | **200** | 126 445 | **the article** (PeerJ JATS XML; 0 challenge markers) |
| `…/PMC4627914/fullTextXML` (2015) | 2 | **200** | 126 445 | same sha256 |
| `…/PMC12285159/fullTextXML` (2025) | 2, 3 | 500 | 0 | — |
| `…/search?query=EXT_ID:40696441…` | 1, 2 | 200 | 5 166 | the core record; sha256 `175f805d…` = the committed S238 capture |
| `…/fulltextRepo?pprId=PMC12285159…` (PDF) | 1, 2 | 403 | 0 | status only; body not parsed |

**Answer to the seat question — is the 500 recipe-specific? No.** The identical recipe that produced the lane's
three 500s produced a 200 carrying the article on my first attempt for both routes. The 500 is transient
server-side flakiness on that Europe PMC full-text route, not a property of the URL, the UA, or `--compressed`.

Two corroborations already committed at F:

* The 2015 body I fetched has sha256 `c033b0493a09832723507c96fb0e2a13b4d2f3a168e9fe1e5d2147c4c543b0ab` — byte-identical
  to the http 200 body the **round-99** seat recorded in `.ufo/waves/round-99/w1/R99ScoutSources-s235-reopen.txt`.
  So S237's flip condition was already met at F by a lane-committed wave receipt, and the lane still re-ran it
  three times and kept it rejected.
* The 2025 core-record body I fetched has sha256 `175f805d…` — byte-identical to the committed capture
  `corpus/captures/b5eec205612ee5f138cf065d.txt`. The S238 capture is the served body, unaltered.

**Why this fires C2.** C2's named limit (a) — "S238 is the abstract only; the full text (S239, PMC12285159)
answered http 500" — and the entry's own scope sentence ("nothing here rests on the article body: not the list
of 46 studies, not how 'major' is defined there, not the heterogeneity statistic") both rest on the
full text being unreachable. It is reachable, and every one of those three exclusions is now answerable.

*(Deviation disclosed: u1 received a **third** attempt, beyond my seat item's "at most 2 attempts each". It
returned 500 and changed nothing; the two decisive 200s are attempts 1 of each route.)*

---

## F-2 (C2, decisive) — the article contradicts three decision rows and the r99 `## Update`

With the 2025 body in hand, the entry's claims about study sets and about `major` are contradicted by its own source.

### F-2a — the 46-study set **contains** the 28-study 2015 set; they are not "different study sets"

> **Entry, row 2 Do cell (F):** "keep each rate with its own study set: the earlier review included 28 studies in
> the main analysis (total 25.4%, major 11,9% as printed); **the update identified 46 studies** (total 16.9%,
> major 8.0%)…"
> **Entry, Named Limits (F):** "The 2015 and 2025 pooled rates come from **different study sets** (28 and 46
> studies); the abstracts do not say how many studies they share."
> **r99 `## Update` (F):** "the two rates come from **different study sets** (28 and 46 studies)"

> **Source (2025 Results), verbatim fragments** (reference markers elided):
> "we included 18 reports on 18 new studies" · "for a total of 46 studies – together with 28 studies" ·
> "from our systematic review published in 2015" · "that form the basis of this meta-analysis"

46 = **18 new** studies + the **28 carried over from 2015**. The 2015 set is a subset of the 2025 set, not a
different one. The entry's "the update identified 46 studies" reads as 46 fresh studies.

**How many of the 46 overlap the 2015 set? All 28 of them** — the 2015 main analysis is carried forward
whole; 18 are new. The 2025 review is an *update* of the 2015 one ("We updated our meta-analysis from 2015 [8]
that included studies published until December 26, 2014", searching 2014-01-01 to 2023-10-01).

### F-2b — the authors DID make the same-study-set comparison the entry says is absent

> **Entry, row 2 Do cell (F):** "the gap between them is not a measured trend" (warrants J1, J2, U4, U7 — the
> 2015 and 2025 **abstracts**; the Lane cell at F2 now says the abstracts state no comparison)
> **r99 `## Update` (F):** "the abstracts state no comparison between them"

> **Source (2025 Results), verbatim:** "When we re-calculated the meta-analysis from 2015 with imputed data, we
> arrived at a figure very similar to our current overall result (total quotation error rate of 17.0% [12.9–22.0],
> n = 28)"

That is the like-for-like comparison on the **shared 28 studies**: 17.0% (2015's studies, 2025's method) against
16.9% (all 46). The entry's framing — two rates from separate study sets, no comparison between them — is not
what the source says. The entry's own Warrant set (the abstracts) cannot settle this; the article body can, and
it does.

### F-2c — the update **does** define major and minor; the entry and the r99 `## Update` say it does not

> **r99 `## Update` (F):** "the 2025 abstract does not define major and minor, so the rows that use them still
> stand on S233 (G4, G5, G11)"
> **Entry, Named Limits (F):** "not how \"major\" is defined there" (i.e. unavailable)

> **Source (2025 Methods), verbatim fragments:**
> "major errors usually mean that a quotation seriously misrepresents the source; it is not at all" ·
> "accordance with the authors’ claim" · "Minor errors are usually defined as inconsistencies and factual errors not
> severe enough to contradict" · "the claim by the authors"

The 2015 paper (also 200) defines them too: "a major quotation error is not at all in accordance with the claim
of the authors". The r99 sentence is true of the *abstract* and false of the two papers. It is also the sentence
that carries the entry's remaining `major`/`minor` rows (S233's G4/G5/G11), so the deferral matters.

### F-2d — two numbers whose study base the entry gets wrong (the full text sharpens both)

* **Row 1.** Entry: "major errors 8.0% [95% CI: 6.4%-10.0%], **over 46 studies** analyzing 32,000
  quotations/references". Source Table 1: "Total errors (46) 16.9 … **Major errors (36) 8.0** … **Minor errors (36)
  7.8** … **Secondary errors (18) 5.3**". The 8.0% major rate is over **36** studies; only the 16.9% total is
  over 46. The entry attaches one base to two rates. (Its warrant U4 — the abstract's "identified 46 studies
  analyzing 32,000 quotations/references" — does not distinguish them either, so this is a paraphrase the full
  text sharpens rather than a misquotation.)
* **Row 4.** Entry: "journal impact factor was associated with total error rate (Spearman's ρ = -0.253, p = 0.043,
  binomial test, **N = 25**)". Source: "negatively correlated with journal impact factor: Spearman's ρ = –0.253
  (**based on 23 studies reporting correlation coefficients**)". ρ rests on 23 studies; N = 25 is the binomial
  test's base. The entry's "N = 25" reads as the correlation's base.
* **Row 6.** The source adds a trim-and-fill sensitivity the entry cannot show: "higher error rates were added to
  the funnel plots of total errors (4 potential studies for a summary estimate of 18.7% [15.7–22.0])" — the pooled
  total moves to 18.7%.
* **Row 3** ("no improvement over recent years"): **no contradiction found.** The source agrees ("error rates
  remained constant since quotation error research began in the 1980s").

Each source sentence above is quoted ≤25 words; the receipts carry the fuller windows.

---

## F-3 (C1) — the frozen battery cannot see the one thing C1's sentence is about

C1's sentence: *"fails a rev-form GATE-RECORD with CHALLENGE when the blob git resolves for `rev:path` has the
object id of a `corpus/captures/<24 hex>.txt` or `.raw` entry **of that rev's tree**"*.

**The C1 battery never exercises that phrase.** One-line mutant of the tool: `capture_oids()` reads the capture
set at `HEAD` instead of the record's `rev`.

```
$ python3 -B corpus/evidence/round100/challenge-controls-r100.py --root . --work $S/w-mut2 --tool $S/mut/gate-head.py
NEG=7/7 MARK=11/11 BOUND=3/3 NORM=2/2 POS=4/4 REV=11/11 REVPOS=3/3 PROD=6/6 HARM_SAME=27/27 BASE_REV_ADMITTED=8/11 ORACLES_REJECTED=12/12
CHALLENGE_CONTROLS_R100=PASS
exit=0
```

The mutant reads the wrong tree and still prints the frozen predicate line, exit 0.

**Why:** `fixture_repo()` (battery lines 169-187) commits **once** ("commit FILES … once"), so inside the
fixture `HEAD` == the record's rev; and the lane's PROD rev legs all read the same lane revision (BASE).

**The tool is right; the battery is blind.** Two-commit fixture, capture at rev A = challenge page, at rev B
(= HEAD) = an ordinary body, record citing rev A:

```
$ python3 -B $S/repo/tools/gate-records.py verify --root $S/repo --repo $D $D/rec.md
GATE_RECORD <rec.md>:1 S900 FAIL CHALLENGE,REGISTRY     <- F tool reads rev A's tree: judged
$ python3 -B $S/mut/gate-head.py verify --root $S/repo --repo $D $D/rec.md
GATE_RECORD <rec.md>:1 S900 FAIL REGISTRY               <- HEAD mutant reads rev B's tree: NOT judged
```

The two tools disagree on exactly the frozen sentence's phrase, and the single-commit fixture hides it. So C1's
sentence says more than its counting command enforces. (The lane's F2 amendment A1 already narrows this phrase
for other seats' reasons; my receipt adds the executable mutant and the two-commit control.)

---

## F-4 (C1) — the tool honours all four named limits (probes, no finding)

I probed each named limit with my own git fixtures. All hold:

* **(b) byte identity** — a one-byte-different copy at another path is **not** judged (`FAIL REGISTRY`, no
  CHALLENGE code).
* **(c) the capture set comes from the rev's tree** — a capture present only in the *working tree* (uncommitted)
  is not consulted (`FAIL REGISTRY`, no CHALLENGE).
* **(d) a `.raw` with no sibling `.txt` at that rev** is judged by its own bytes (`FAIL CHALLENGE`).
* **identity, not path spelling** — a byte-identical copy at `notes/bytecopy.txt` is judged `CHALLENGE`, as is
  the capture path itself and the `.raw`.
* the challenge rule is **unchanged**: `CHALLENGE_MARKERS` identical (11 markers), `CHALLENGE_MAX_WORDS` 200 in
  both, `is_challenge()` code identical.
* `GIT_DIR` in the environment does not redirect the capture set.
* A path spelling git itself cannot resolve (`corpus//captures/x.txt` without a leading `./`) is refused as
  `REV`, correctly not `CHALLENGE`. (The battery's `./corpus//captures/…` spellings *are* normalised by git and
  do resolve.)

The C1 base-tool before-leg reproduces `before/c1-base.txt` exactly (`REV=3/11`, `PROD=4/6`, `FAIL`, exit 1), and
the candidate reproduces the frozen predicate line exactly (`HARM_SAME=27/27` ≥ 26, exit 0).

---

## F-5 (C2) — all six counting commands are green; two of the entry's numbers are located only after normalization

All six C2 counting commands at F, verbatim, all exit 0 and matching the frozen predicate:
`GATE_RECORDS files=1 records=17 ok=17 fail=0` · `RESEARCH_GATE: CLEAN` · `rev_match=3/3` +
`SEARCH_RERUN: CLEAN` · `ENTRY_CONTROLS_R100=PASS` with the exact frozen tally line ·
`GATE_RECORDS files=1 records=25 ok=25 fail=0` (r99 entry, unchanged) · `ENTRY_CONTROLS_R99=PASS`.

Independently re-derived, not just re-run: all 16 quotes are located in their stated field (U0 in S238's `title`,
U1-U13 in S238's `abstractText`, J1/J2 in S236's `abstractText`); all 24 Do/Never numerals are tokens of their
row's own warrant quotes (0 unsourced).

**But "located" is true only after normalization.** **U9** and **U11** are **not byte substrings** of their
field: the capture prints U+2009 THIN SPACE around `=` and before the number (`p = 0.85` with U+2009), and
U11's sentence is followed immediately by `<h4>Conc` in the capture. The entry prints ASCII `p = 0.85`. The gate
tool's `norm` folds them via `" ".join(s.split())` (Python's `str.split()` splits on U+2009), so the gate passes.
The claim's "14 located quotes" is true only in the normalized sense — worth stating, since the entry's own
`## As run` describes the search corpus as byte-materialised. (The lane's F2 amendment B3 already records this;
my receipt gives the exact offsets and codepoints.)

---

## Frontier (leads only, nothing fetched)

One web search, no fetch. Six non-medical leads in `R100ScoutSources-frontier-leads.txt`; the most useful for
the lane's topic is **How do authors perceive the way their work is cited?** (JASIST) — 2 648 authors judging
citations of their own work: a **16.6 %** quotation-error rate with **no significant difference across
disciplines** (`asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.70000`). Also: Cobb et al. on psychology
(9.5 % of 3 347 claims completely mischaracterized), a history-journal study (24.27 %), education research
(15 %), and a cross-field review. **Economics has no field-wide quotation-accuracy measurement** — do not read
the cross-disciplinary 16.6 % as an economics rate.

---

## Not found / limits of this seat

* I did not test C1 against the twelve oracles individually (the battery does); I confirmed the frozen aggregate
  line, the base leg, the four named limits and the rev-tree blind spot.
* My 2015 full text (u2) is the **PeerJ** article as deposited in PMC — the lane's `corpus/captures/…405a0054e…`
  is the *Europe PMC core record* for the same paper, so the two agree on every number I compared (28 studies,
  11,9 %, 11.5 %, 25.4 %).
* The 2025 full text's own reference list shows "28 studies [2, 3, 5, 6, 16, 17, 17, 39–45, 45–60]"; the duplicated
  17 and 45 are in the article's own citation-to-reference expansion, not mine.
* I did not attempt the publisher's own page for the 2025 article (round 99 recorded it serving a "Client
  Challenge" interstitial), and I did not fetch the PDF route beyond recording its 403.
* The live lane tree has moved on since F (it carries F2 amendments and an `after-f2/` directory); I judged
  against F, as instructed, and read the live tree only to check whether a finding was already recorded.

---

VERDICT: R100ScoutSources C1 fired — the frozen predicate line reproduces exactly, but a one-line mutant that reads the capture set at HEAD instead of the record's rev still prints it, so the battery cannot enforce the sentence's "of that rev's tree" (the F tool itself is correct on that point).
VERDICT: R100ScoutSources C2 fired — all six counting commands are green, but the full text is reachable at http 200 with the lane's own recipe (meeting SOURCES.md's own "flip: a 200 carrying the article XML"), and it contradicts three decision rows: the 46-study set contains the 28-study 2015 set rather than being a different one, the update does define major and minor, and the authors do state the same-study-set comparison the entry says is absent.
