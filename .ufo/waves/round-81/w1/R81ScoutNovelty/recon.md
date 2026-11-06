# Round 81 — R81ScoutNovelty — per-surface reconnaissance for C1's novelty and placement

Seat: `R81ScoutNovelty`. Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Base revision: `378fda82dc2cbcc555a0565052cc408121813cef`. Candidate landing: `7e2da96a0541946e796384d42fea18e09ede9e9f`.
Read-only seat. No production file, registry, counter, claim or receipt was edited. No network was used.
Every command below was run from the fleet root or from the seat scratch (now deleted); receipts are copied into
`.ufo/waves/round-81/w1/R81ScoutNovelty/receipts/`.

Scratch used during the seat: `/fast/scratch/hyaku/chousa-r81/R81ScoutNovelty/` (base tree and landing tree extracted
with `git -C <lane> archive <rev> | tar -x -C <scratch>`), deleted before yield.

---

## 0. Summary of findings

| # | Question | Answer |
|---|---|---|
| F1 | Does a base `corpus/knowledge/*.md` already govern citation *searching* as a retrieval method? | **No** — but see F3: the base **capture** `c9d1e74c3ac8d9eb332c9770.txt` (S120) already names the TARCiS statement and already carries a mandatory retraction/errata-check section (MECIR Box 4.4.e, C48). The ground was in the lane's bytes; it was not held as a knowledge entry. |
| F2 | Does a base `corpus/knowledge/*.md` already govern erratum/retraction status of a cited work before reuse? | **No** — same caveat as F3. |
| F3 | Adjacent/same-ground base material | `search-tracking-record-r40.md` (S117) and `chinese-search-record-r39.md` (S109) touch "citation searching" only as a **reporting slot / form field** — adjacent, not same ground. `western-instrument-alignment-r50.md` (S120) holds the *source* of both new topics in its capture but teaches neither — the strongest partial weakening of C1's "ground the lane does not hold". |
| F4 | Which coverage row(s) do the two new entries belong under, and proposed appended row text | The README's per-round section pattern → a new `## Round81 coverage and frontier (2026-11-06)` section with a two-row table (text in §2). **The landing revision has no README row at all**, so the lane's own `G02 knowledge-index` preflight gate **FAILS** at the landing revision (F5). |
| F5 | Placement defect at the landing revision | `tools/lane-preflight.py --root <landing tree> --only G02` → `FAIL 2 not named in corpus/README.md: citation-searching-tarcis-r81.md,correction-retraction-status-r81.md`. Base passes (`PASS 91 entries indexed`). |
| F6 | Registry duplicate URL for S203–S207? | **No.** Six pre-existing duplicate-URL groups in the registry; none involves S203–S208. Census `validate` at the landing registry emits the same five pre-existing `W04` rows as the committed `census-start.txt` — **no new W04**. |
| F7 | Is S028 (Crossmark) a source the E2 entry should also have cited? | **Yes on the same ground — and it is a lane row the round left dangling.** S028 is `queued` since 2026-10-21, `used-by —`, **no capture bytes** (key `dedff231d5c3d3cdb0b4f8e3` absent from `corpus/captures/` at base *and* at landing) and no `refetch.tsv` row, so it cannot be cited as a located quote — but round 25 already recorded it as "A cited work's update, correction or retraction status is published metadata a reader can check, a recheck trigger". The E2 entry neither cites nor dispositions it. |

---

## 1. Base-tree novelty reconnaissance (base `378fda82`)

### 1.1 The prescribed grep

```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -n -i -E 'tarcis|citation search|forward citation|backward citation|co-cit|retract|erratum|errata|expression of concern|crossmark|retraction watch' 378fda82dc2cbcc555a0565052cc408121813cef -- corpus/knowledge corpus/README.md SKILL.md
```

Receipt: `receipts/r01-base-novelty-grep.txt` (exit code 0). The hits it returns are:

* `corpus/knowledge/search-tracking-record-r40.md:14` and `:22` — `` `citation searching, and other methods should be reported` (char 6355) `in Column 2` `` and `` `S117` puts `citation searching, and other methods should be reported` in one column ``.
* `corpus/knowledge/chinese-search-record-r39.md:15` — `` asks whether `参考文献追溯`, citation searching or `手工查阅期刊` were used ``.
* `corpus/knowledge/western-instrument-alignment-r50.md:3` — the `source:` line of S120 (Cochrane Handbook ch. 4), whose **capture** contains the TARCiS mention and the retraction section (F3 below).
* Every other hit in the receipt is the word *errata/erratum* used in the lane's **own append-only errata** sense (`## Errata`, `claims-erratum`, `Errata 5/8/10`, `4 errata append-only`), plus `citation-chain-fidelity-r24.md` (a chain-*fidelity* entry, not a citation-searching one). None is about a cited work's retraction status.

### 1.2 Per-family counts inside `corpus/knowledge/*.md` at base

```
cd <scratch>/base && for p in retract 'Retraction Watch' TARCiS 'expression of concern' 'citation searching' 'backward citation' 'forward citation' 'co-cit'; do printf '%-24s ' "$p"; grep -ril -- "$p" corpus/knowledge/*.md | wc -l; done
```

Receipt: `receipts/r03-base-knowledge-retract-count.txt` (exit code 0). Observed: `retract` → 0 files;
`Retraction Watch` → 0; `TARCiS` → 0; `expression of concern` → 0; `backward citation` → 0; `forward citation` → 0;
`co-cit` → 0. `citation searching` → 2 files (`search-tracking-record-r40.md`, `chinese-search-record-r39.md`).

**Verdict on (1) of the seat item:** the frozen claim's literal wording — *"No base entry names TARCiS; no base entry is
about erratum/retraction linking"* — **holds**. Zero base knowledge entries mention TARCiS, retraction, retraction
notice, expression of concern, Crossmark or Retraction Watch, and zero teach backward/forward/co-citation retrieval.

### 1.3 Judgement for every hit (same ground / adjacent / unrelated)

| Base hit | Quote | Judgement |
|---|---|---|
| `corpus/knowledge/search-tracking-record-r40.md:14` | `` Records identified from websites, organizations, `citation searching, and other methods should be reported` (char 6355) `in Column 2.` `` | **Adjacent.** The phrase is a *PRISMA-S flow-diagram column label* — where a count is printed, not how to search. It carries no backward/forward/co-citation taxonomy, no "when to run it", no TARCiS terminology, and no guidance on supplement-vs-stand-alone. The entry's own inference (`:22`) is a reporting split, not a retrieval method. |
| `corpus/knowledge/search-tracking-record-r40.md:15` | `` `Citation indexes are indeed databases and can be included` (char 13633) in Column 1 `` | **Adjacent.** A counting/placement rule about citation indexes. The new E1 entry's rec-6 rule (combine two indexes for coverage) is a *retrieval-coverage* rule; it is not in this base entry. |
| `corpus/knowledge/chinese-search-record-r39.md:15` | `` asks whether `参考文献追溯`, citation searching or `手工查阅期刊` were used `` | **Adjacent.** A *reporting-form field* of a Chinese animal-experiment reporting copy. It asks whether the method was used; it teaches nothing about how to run it. |
| `corpus/knowledge/citation-chain-fidelity-r24.md` (title and §Erratum) | "a resolved hop proves a locator exists, not that the relay is faithful" | **Unrelated** to citation searching as a retrieval method (it is about verifying one hop's fidelity) — but it *is* the correct neighbour the new E1 entry already names in its `## Relation to existing lane knowledge` (`citation-searching-tarcis-r81.md:65`). |
| `corpus/knowledge/citation-version-binding-r36.md` / `-r37.md`, `citation-count-semantics-r37.md`, `cnki-citation-check-r40.md`, `istic-citation-verification-r39.md`, `search-log-method-r39.md` | — | **Unrelated** (or adjacent in the weak sense of "citation" in the bibliographic-verification sense). None mentions retraction/erratum status. |
| All `## Errata` / `claims-erratum` / `Errata N` hits | — | **Unrelated** — the lane's own append-only correction apparatus, a different sense of "errata" from a published work's correction notice. |

### 1.4 F3 — the partial weakening: the ground was already in the lane's *bytes*

```
grep -n -i -E 'the TARCiS statement|4\.4\.6 Identifying|MECIR Box 4\.4\.e|C48 : Examining errata|expressions of concern associated' <scratch>/base/corpus/captures/c9d1e74c3ac8d9eb332c9770.txt
```

Receipt: `receipts/r02-base-capture-S120-ground.txt` (exit code 0). This capture is S120 (Cochrane Handbook ch. 4,
`https://training.cochrane.org/handbook/current/chapter-04`, key `c9d1e74c3ac8d9eb332c9770`), status `mined`,
opened 2026-10-26, `used-by corpus/knowledge/western-instrument-alignment-r50.md`. Observed in the **base** capture:

* capture line 918: ` Documenting the searching of sources other than databases, including the search terms used, is also required if searches are to be reproducible ( Atkinson et al 2015 , Chow 2015 , Witkowski and Aldhouse 2015 , Booth et al 2020b , Hirt et al 2024a ). Guidance on terminology, application, and reporting of citation searching has recently been published (the TARCiS statement) ( Hirt et al 2024a ).`
* capture line 740: ` 4.4.6 Identifying fraudulent studies, other retracted publications, errata and comments`
* capture line 742: `... publications for some studies may have been found to contain errors or to be fraudulent or may, for other reasons, have been corrected, retracted or had expressions of concern associated with them since publication. Review authors should examine any relevant retraction notices and errata for information ( MECIR Box 4.4.e )...`
* capture line 747: ` MECIR Box 4.4.e Relevant expectations for conduct of intervention reviews` / ` C48 : Examining errata ( Mandatory ) ` / ` Examine any relevant retraction statements and errata for information.`
* capture line 743: ` Errata are published to correct unintended errors ... Retractions are defined by the Committee on Publication Ethics (COPE) Council's retraction guidelines ...`

and the base capture's own reference list (lines 1003–1279) carries the COPE retraction-guidelines URL, the retraction-search
literature, and line 1121 the TARCiS statement itself.

**What this does and does not do.** It does **not** falsify the frozen claim: no base *entry* names TARCiS and no base
entry teaches retraction-status checking. `western-instrument-alignment-r50.md` cites S120 only for §4.1, §4.2.1 and
§4.3.2 and quotes none of §4.4.6, MECIR C48 or the TARCiS mention — verified:

```
grep -n -i -E '4\.4\.6|MECIR Box 4\.4|C48|seriously considered|TARCiS|Hirt|retract|errata' corpus/knowledge/western-instrument-alignment-r50.md
```

→ one hit only, line 14, the MECIR *search expectations* bullet of §4.2.1; no §4.4.6, no C48, no TARCiS (exit code 0).

But it **does** weaken the novelty *rationale* the claim rests on, and the reviewer should weigh it: the lane already held,
committed and mined, a single document that (i) names the TARCiS statement as the guidance on citation-searching
terminology/application/reporting, and (ii) prescribes, as a **Mandatory** MECIR expectation, examining retraction
notices and errata. An entry on both topics could have been built from S120 alone, with **zero** new fetches. The round
instead opened six new URLs (S203–S208) to reach a TARCiS manuscript that S120 already cites, a Cochrane §4.4.6 the lane
already held, and three publisher pages. Whether the C1 surface (a *sourced* depth claim) is weakened is the reviewer's
call, but the reconnaissance finding stands: the ground was in the corpus at base, just not in an entry.

This is **not** a K3 firing. K3 requires a counted entry to assert, in a decision-table row, something its *cited located
quote* contradicts; S120 is not a quoted source of either new entry, and no located quote of S203–S207 contradicts
either entry.

### 1.5 Adjacent-decision-table observations (for the reviewer; not K3)

Recorded because they are cheap and concrete; neither is a K3 firing (no cited located quote contradicts them).

1. `citation-searching-tarcis-r81.md:33` — decision row: *"The review team judges its topic difficult to search for
   with database queries | **run** backward **and** forward citation searching as a supplement to the database search
   | … | S203 recommendation 2"*, while the located quote at `:43` reads *"backward and forward citation searching
   **should be seriously considered** as supplementary search techniques."* The source modality ("should be seriously
   considered") is rendered as an unconditional "run". The capture (line 289) confirms rec 2's wording is "should be
   seriously considered".
2. `citation-searching-tarcis-r81.md:39` — decision row asserts "(rec 5 was corrected)" as a fact about a document the
   lane could not read; the warrant cell reads "S208 (rejected, unreachable) — lane inference". The claim rests on a
   *search-result snippet*, which the entry discloses only in the `## Version caveat` section (`:56–61`), not in the
   decision row itself. S208 has no located quote, so K3 does not reach it.
3. `citation-searching-tarcis-r81.md:53` — the located quote for recommendation 10 is only the fragment
   *"the directionality of searching (backward, forward, co-cited, co-citing),"*, yet the decision row at `:38` asks for
   "seeds, directionality, dates, iterations and indexes/tools". The capture (lines 463–480) does list all of those
   items under recommendation 10, so the row is supported by the capture; only the quoted fragment is narrower.

---

## 2. `corpus/README.md` coverage map — placement of the two new entries

### 2.1 How the coverage map is organised at base

`corpus/README.md` (1365 lines at base) has one top-level `## Coverage map` table (`:3`–`:95`, header
`| Note | Holds | Sources |`, 68 body rows counted by `awk 'NR>=5 && NR<=78 && /^\| \`/' corpus/README.md | wc -l` →
receipt `r04-base-capture-count-and-index.txt`, exit code 0), and then per-round sections
`## Round51 coverage and frontier (2026-11-…)` … `## Round62 coverage and frontier (2026-10-28)`, followed by
prose-style round sections `## Round64 root-derivation detail` … `## Round74 correction-counter loader`.

The **Round51–Round62 sections are the established home for a round's new knowledge entries**: each is a
`| Note | Holds | Sources |` table whose first column is the `knowledge/….md` path (e.g. `## Round51 coverage and
frontier (2026-10-25)` rows `knowledge/japanese-search-record-r38.md`, `knowledge/chinese-search-record-r39.md`,
`knowledge/japanese-search-record-r38-amendment-2026-10-23.md`; `## Round52 …` rows
`knowledge/japanese-search-record-niph-form-r52.md`, `knowledge/japanese-prisma-item-wording-r40.md`,
`knowledge/chinese-prisma-s-reception-r52.md`). **Round 81's two entries therefore belong under a new
`## Round81 coverage and frontier (2026-11-06)` section**, in the same three-column shape, placed after the
`## Round74 correction-counter loader` section at the end of the file. (The alternative — appending to the top
`## Coverage map` table — would also satisfy the gate, but it breaks the per-round credit convention that rounds
51–62 established and that rounds 64–74 continued.)

### 2.2 Placement defect at the landing revision (F5)

The landing commit changed `corpus/SOURCES.md`, `corpus/knowledge/*` and `SKILL.md` — **`corpus/README.md` was not
touched**:

```
git -C <lane> diff --stat 378fda82dc2cbcc555a0565052cc408121813cef 7e2da96a0541946e796384d42fea18e09ede9e9f -- corpus/README.md
```
→ empty output (exit code 0).

Consequence, measured on the extracted landing tree:

```
cd <scratch>/landing && python3 -B <lane>/tools/lane-preflight.py --root . --only G02
```

Receipt: `receipts/r09-preflight-G02-landing.txt`, **exit code 1**, observed line:

```
GATE G02 knowledge-index FAIL 2 not named in corpus/README.md: citation-searching-tarcis-r81.md,correction-retraction-status-r81.md
```

The same gate on the base tree (receipt `r10-preflight-G02-base.txt`, exit code 0) reads
`GATE G02 knowledge-index PASS 91 entries indexed`. So the candidate landing **fails a lane-owned gate that the base
passes**, for exactly the two new files. This is a placement finding, not a claim-counter finding: the C1 counter
(`depth-r81.py`) does not read `corpus/README.md`, so `DEPTH_R81=PASS` is unaffected — the failure is in the lane's own
knowledge-index preflight.

### 2.3 Proposed appended row text (no edit made)

New section to append at the end of `corpus/README.md`:

```markdown
## Round81 coverage and frontier (2026-11-06)

| Note | Holds | Sources |
|---|---|---|
| `knowledge/citation-searching-tarcis-r81.md` | What the TARCiS statement says about citation searching as a retrieval method: direct (backward and forward) versus indirect (co-citing and co-cited) searching; when it is a supplement and never a stand-alone route for a completeness-of-recall search; two citation indexes for coverage; deduplication before screening; iteration with the newly found records as seeds; what a reporting paragraph must state (seed references, directionality, dates, iterations, indexes and tools); and the version caveat that the read text is the accepted manuscript, not the version of record, and that its 2024 erratum was unreachable | S203 (Hirt et al., BMJ 2024;385:e078384, accepted manuscript, capture `f2489455cc311a4de981e926`), S204 (Campbell Systematic Reviews 2024, PMC11386270, capture `c52a1f15884a78028febcf43`), S208 rejected (HTTP 403, flip recorded); counter `corpus/evidence/round81/depth-r81.py` (`DEPTH_R81 entries=2 fresh_rows=5 located_quotes=14`, `DEPTH_R81=PASS`, exit 0) |
| `knowledge/correction-retraction-status-r81.md` | Where the correction, retraction and version status of a cited work is published and what each signal does and does not establish: PubMed links an erratum notice to the corrected article's citation and assigns Publication Type Retracted Publication to a retracted article; ICMJE asks journals to archive prior versions and to mark earlier electronic versions as superseded; the Crossref-distributed Retraction Watch data are updated every working day but carry expressions of concern and corrections less comprehensively than retractions, so a no-hit is weaker for those; and the lane's own status-check rule marked as inference, not as a source statement | S205 (NLM, capture `371c55117727d526805f030d`), S206 (ICMJE, capture `f221c90f69188f775e32cd34`), S207 (Crossref Retraction Watch, capture `43a45b49723f7677d6446c92`); counter as above |
```

Two further rows are legitimate but optional: one for `corpus/evidence/round81/` (the frozen claims, counters, fixtures
and controls, in the shape used by `evidence/round49/`, `evidence/round50/`, `evidence/round52/` rows of the top table),
and one for the two entries' shared S028 gap if the closure wants it recorded. Both are left out of the proposal above
because the seat item asked for one row per new entry.

### 2.4 Secondary README observation (pre-existing, not caused by the landing)

The README's count paragraph (`:76`–`:93`) is stale at base and stays stale: it reads
"Round-25 correction (appended 2026-10-21; supersedes the round-24 count as current at this landing): 43 entries — 29
knowledge notes and 14 lessons". The actual counts are **91** `knowledge/*.md` at base (`ls corpus/knowledge/*.md | wc -l`,
receipt `r04`, exit code 0) and **93** at the landing. Note also that `git ls-tree … corpus/knowledge/` gives **92**
entries at base because it counts `.gitkeep` — the frozen claim's "92 files at base" is the tree-entry count, whereas the
knowledge-note count at base is 91. Pre-existing; G02 does not check the count paragraph.

---

## 3. Registry `corpus/SOURCES.md` — duplicates and S028

### 3.1 Are S203–S207's URLs registered under another id?

A scan of the landing registry (208 parseable 11-cell rows) for repeated first-URL:

Receipt: `receipts/r07-dup-url-scan.txt` (exit code 0). Observed: `parseable rows: 208`, `duplicate-URL groups: 6`, and the
six groups are all pre-existing:

```
DUP https://docs.python.org/3/library/hashlib.html                        [('S059','mined','2026-10-23'), ('S074','rejected','2026-10-24')]
DUP https://pubmed.ncbi.nlm.nih.gov/17638714/                             [('S021','queued','2026-10-21'), ('S032','queued','2026-10-21')]
DUP https://pubmed.ncbi.nlm.nih.gov/28912002/                             [('S022','queued','2026-10-21'), ('S030','queued','2026-10-21')]
DUP https://schema.org/lastReviewed                                        [('S024','queued','2026-10-21'), ('S031','queued','2026-10-21')]
DUP https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv  [('S019','queued','2026-10-21'), ('S029','mined','2026-10-21')]
DUP https://www.w3.org/TR/2013/REC-prov-o-20130430/                       [('S020','queued','2026-10-21'), ('S033','mined','2026-10-21')]
```

**No S203–S208 URL appears in any group.** Each of S203–S207 is registered exactly once, under its own id.

The lane's own census agrees. `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md --today 2026-11-06`
(receipt `r05-census-validate-landing.txt`, exit code 0) emits exactly the five pre-existing W04 rows and nothing else:

```
file	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
file	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

These are the same five rows the round's own committed pre-flight receipt `.ufo/waves/round-81/census-start.txt`
records (identical ids and URLs) — **the round introduced no new W04 and no E-code**. `census` mode (receipt
`r06-census-counts-landing.txt`, exit code 0) reports `rows 208, tier.A 129, tier.B 59, tier.C 20, status.mined 166,
status.queued 19, status.rejected 23, tier.invalid 0, status.invalid 0, missing 0`.

Cross-lane, the fleet `shared` mode shows one of the new URLs also present in a sibling lane:
`www.icmje.org/recommendations/browse/publishing-and-editorial-issues/corrections-and-version-control.html shared kotoba,chousa`
(kotoba registers it as its own **S119**, `mined`, opened 2026-10-23, with a `.ufo/waves/round-63/snapshots/S119.page`
snapshot). That is the fleet's informational `shared` metric, not a within-lane duplicate, and it does not affect
chousa's W04 count.

### 3.2 Should the E2 entry also cite S028 (Crossmark)?

**Yes on the same ground — and S028 is a lane row this round left dangling.**

S028 at base and at landing (`corpus/SOURCES.md:38`):

> `| S028 | Crossref Crossmark — https://www.crossref.org/services/crossmark/ | docs | A | Crossref's own description of the Crossmark update/correction/retraction status service | introductory text before Benefits of Crossmark | A cited work's update, correction or retraction status is published metadata a reader can check, a recheck trigger | queued | 2026-10-21 | 180d | — |`

Its own *teaches* cell is the E2 entry's thesis, in the lane's own words, sixteen days earlier. Round 25 recorded the
quote at `corpus/lessons/round-25.md:77`:

> `| S028 queued (SrcCrossmark) | https://www.crossref.org/services/crossmark/ | Intro before Benefits of Crossmark: "Crossmark makes this information more visible to readers." |`

Why the E2 entry could not cite it as a located quote (measured, not assumed):

* capture key = sha256("https://www.crossref.org/services/crossmark/")[:24] = `dedff231d5c3d3cdb0b4f8e3`;
  `ls corpus/captures/ | grep dedff231` → **no such file**, at base and at landing (exit code 1 on the grep);
* `grep -n -E 'S028' corpus/evidence/round57/refetch.tsv` → **no row**, so the counter's P2 "fetch record" leg could not
  be satisfied for S028 either;
* `grep -rn 'S028' corpus/knowledge/` → **no hit** (exit code 0, empty) — no base or landing entry cites it.

So S028 is a **same-ground, unopenable-as-quote** lead. Concretely it means:

* The E2 entry's `## How the status is published` section names PubMed publication types and linked notices, the
  journal's version note, and the Retraction Watch data — but not **Crossmark**, which is the publisher-side service
  that publishes exactly "a cited work's update, correction or retraction status". The entry's own inference sentence
  ("The three sources describe where status is published") is true of its three sources, but the *lane* already had a
  fourth, closer source for the same question and this entry neither cites nor dispositions it.
* Leaving S028 `queued` with `used-by —` and no flip condition also leaves the registry's own row un-actioned after a
  round that landed an entry on precisely that ground. The honest dispositions are: (a) open Crossmark in this or a
  later round and cite it, or (b) flip S028 to `rejected` with a reason and a flip condition. Neither happened.

Note for the reviewer: this is a **scope/placement** finding about the landed entry. It is **not** a C1 predicate
failure — the frozen counter counts `*‑r81.md` entries against fresh rows S203–S207, and the counter passes:

```
cd <scratch>/landing && python3 -B corpus/evidence/round81/depth-r81.py --root .
```

Receipt: `receipts/r08-depth-counter-landing.txt`, exit code 0, observed:

```
ENTRY citation-searching-tarcis-r81.md counted=yes reason=all-pass
ENTRY correction-retraction-status-r81.md counted=yes reason=all-pass
DEPTH_R81 entries=2 fresh_rows=5 located_quotes=14
DEPTH_R81=PASS
```

---

## 4. Fetch records (context for the counter's P2 leg)

```
grep -n -E 'S20[3-8]' <scratch>/landing/corpus/evidence/round57/refetch.tsv
```

Receipt: `receipts/r11-refetch-rows-S203-S208.txt` (exit code 0). Observed six rows dated `2026-11-06T18:44:29Z`–`18:44:31Z`,
five with `curl_rc 0` / `http 200` and one with `curl_rc 22` / `http 403` (S208, the BMJ correction). The five success
rows carry `txt_sha256` equal to the sha256 of the corresponding `corpus/captures/<key>.txt`, which is the property
`depth-r81.py` P2 requires.

---

## 5. What I could not resolve

* Whether the *reviewer* should treat F3 (S120 already held the TARCiS citation and MECIR C48) as a weakening of C1's
  novelty premise, a naming obligation on the new entries, or neither. It is a judgement about claim wording, which is
  frozen and not mine to amend; I report the measurement only.
* Whether S208's recommendation-5 wording is as the search snippet described. The seat item names no re-open and the
  egress approval table authorises a re-open only for a seat whose item names it; no network was used. The correction
  remains unreachable (HTTP 403) at the lane's last attempt.
* Whether the README coverage row should also credit `corpus/evidence/round81/` in the top table (§2.3, optional).

---

## 6. Commands and receipts (index)

| Receipt | Command (abbreviated) | Exit |
|---|---|---|
| `r01-base-novelty-grep.txt` | `git grep -n -i -E 'tarcis|citation search|…' 378fda82 -- corpus/knowledge corpus/README.md SKILL.md` | 0 |
| `r02-base-capture-S120-ground.txt` | `grep -n -i -E 'the TARCiS statement|4\.4\.6 Identifying|MECIR Box 4\.4\.e|C48 : Examining errata|…' <scratch>/base/corpus/captures/c9d1e74c3ac8d9eb332c9770.txt` | 0 |
| `r03-base-knowledge-retract-count.txt` | per-family `grep -ril` counts over `corpus/knowledge/*.md` at base | 0 |
| `r04-base-capture-count-and-index.txt` | `ls corpus/knowledge/*.md \| wc -l`; `git ls-tree … corpus/knowledge/ \| wc -l`; README coverage-row count | 0 |
| `r05-census-validate-landing.txt` | `scripts/sources-census.sh validate --file <lane>/corpus/SOURCES.md --today 2026-11-06` | 0 |
| `r06-census-counts-landing.txt` | `scripts/sources-census.sh census --file <lane>/corpus/SOURCES.md` | 0 |
| `r07-dup-url-scan.txt` | python: parse 11-cell rows, group by first URL, print duplicates and the S203–S208/S028 rows | 0 |
| `r08-depth-counter-landing.txt` | `python3 -B corpus/evidence/round81/depth-r81.py --root .` (landing tree) | 0 |
| `r09-preflight-G02-landing.txt` | `tools/lane-preflight.py --root . --only G02` (landing tree) | **1** |
| `r10-preflight-G02-base.txt` | `tools/lane-preflight.py --root . --only G02` (base tree) | 0 |
| `r11-refetch-rows-S203-S208.txt` | `grep -n -E 'S20[3-8]' corpus/evidence/round57/refetch.tsv` (landing tree) | 0 |

Tools installed or upgraded by this seat: none. No pacman, `uv`, `cargo` or `npm` transaction was run.
