# R98ScoutSources — source re-open and frontier scout (round 98, C2 falsification)

Attacked tree: `aac826848dda5029ba459568b29d9a92176dc2b6` (clone at `/fast/scratch/hyaku/chousa-r98/R98ScoutSources/repo`, checked out; scratch removed before yield). Base `98b8177c1e8b39cdf1167928e4f5d609f6fa81b6`. No tool installed or upgraded. Network used only for the two named URLs (one GET each, both HTTP 200) and web_search; no URL returned by web_search was fetched.

Receipts are in `.ufo/waves/round-98/w1/`, all prefixed `R98ScoutSources-`.

## 1. Re-open and sha256 against refetch.tsv (held)

- `curl` S231 (1 attempt): rc=0, http=200. `sha256sum S231.json` = `4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429`.
  `corpus/evidence/round57/refetch.tsv` row S231: raw = txt = `4111c45a…0429`. Match. `cmp` of the re-open against `corpus/captures/4ec85a1e83553aa272caeb69.txt`: IDENTICAL, exit 0. The JSON `abstractText` diff was not needed.
- `curl` S225 (1 attempt): rc=0, http=200. `sha256sum S225.pdf` = `56c4cdd605dfa3c19ca9b6d0d7e4b43e4a64ec62c8c2daf7c79b1e63cc0dfcc6`. Refetch row S225: raw = `56c4cdd6…dfcc6`; txt = `abd08a93…c9c8`.
  `pdftotext -layout S225.pdf` (pdftotext 26.10.0, official Arch package, already installed; not changed) is byte-identical to `corpus/captures/347c55ba9be9d63afe17986e.txt`: `cmp` exit 0.
- Receipts: `R98ScoutSources-fetch-sha.txt`, `R98ScoutSources-s225-pdftotext.txt`, `R98ScoutSources-refetch-rows.txt`.

## 2. Quotes located in my own copies (held, with one finding in §4)

- M quotes against `abstractText` (tags stripped): M2–M15 are substrings (14/14). M1 is NOT in `abstractText`; it is in the record's `title` field (`'PRESS Peer Review of Electronic Search Strategies: 2015 Guideline\xa0Statement.'`). Receipt: `R98ScoutSources-quotes.txt`.
- K quotes against my `pdftotext -layout` copy, sed numbering: all 22 located on the lines the entry states (K1 35, K2 37, K3 43, K4 45, K5 46, K6 49, K7 51, K8 52, K9 53, K10 54, K11 55, K12 56, K13 61, K14 63, K15 64, K16 65, K17 and K18 66, K19 67, K20 77, K21 and K22 78). The `?` lines between the heading (line 32) and "Derived from:" (line 81) number 36 (`QUESTION_LINES` in the sed numbering), matching the entry's 36 and the 16 held by round 97. Receipt: `R98ScoutSources-quotes.txt`.
- Numbering caveat (note, not a finding against a claim number): the r98 entry's line numbers are `sed`/`cat -n` numbers. Python `str.splitlines()` splits at form feeds and counts one line higher after the first page break (e.g. sed line 79 = "Are sources cited…", splitlines index 79 = "Are any potentially…"). The r97 entry states the convention; r98 does not restate it.

## 3. S231 record identity (held)

S231 record (`resultList.result[0]`): title `PRESS Peer Review of Electronic Search Strategies: 2015 Guideline Statement.` (NBSP before "Statement"); `authorString` `McGowan J, Sampson M, Salzwedel DM, Cogo E, Foerster V, Lefebvre C.`; `doi` `10.1016/j.jclinepi.2016.01.021`; `pmid` `27005575`; `journalInfo.journal.title` `Journal of clinical epidemiology`; volume 75; `dateOfPublication` `2016 Jul`; `pageInfo` `40-46`.
S225 "Derived from" (capture line 82–83): `McGowan J, Sampson M, Salzwedel DM, Cogo E, Foerster V, Lefebvre C. PRESS Peer Review of Electronic Search Strategies: 2015 Guideline Statement. J Clin Epidemiol. 2016 Jul;75:40-6. https://dx.doi.org/10.1016/j.jclinepi.2016.01.021`.
Agreement: title (after NBSP normalization), authors (exact), DOI (exact), journal, volume, month, pages (`40-46` vs `40-6`, the reprint's abbreviation). PMID `27005575` does not appear in S225, so the PMID leg of K5 has no reprint comparator; it rests on S231 itself and on a web_search listing that names PMID 27005575 for this title. Identity holds on every comparator the lane holds. Receipt: `R98ScoutSources-quotes.txt` (identity block).

Gate and rerun receipts at the attacked tree (all exit 0): `GATE_RECORDS files=1 records=38 ok=38 fail=0`; `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`; `SEARCH_RERUN_SUMMARY searches=5 rev_match=5/5 tree_same=1/5 findings=0`, `SEARCH_RERUN: CLEAN`; `entry-controls-r98.py --root .` → `QUESTION_LINES_HELD=36/36 BASE_HELD=16/36 ELEMENTS=7+6/7+6 WARRANTS_OK=10/10`, `ENTRY_CONTROLS_R98=PASS`. Receipts: `R98ScoutSources-gate-verify.txt`, `R98ScoutSources-entry-controls.txt`.

## 4. Findings (C2)

### F1 — K2 fires: an S231 quote can come from outside `abstractText`, and the instrument does not check it

- Entry sentence (`corpus/knowledge/press-2015-statement-questions-r98.md`, line 30): "Every S231 quote below is a substring of that string with no markup inside it." M1 is not a substring of `abstractText` (receipt `R98ScoutSources-quotes.txt`: `M1 in_abstractText= False in_title= True`). The sentence is false as written.
- Instrument: `corpus/evidence/round98/entry-controls-r98.py` lines 85–95, `check_quotes`, tests `nq not in norm(caps[src])`, where `caps["S231"]` is the whole JSON capture (`corpus/captures/4ec85a1e83553aa272caeb69.txt`, 7288 bytes), not `abstractText`. The claim's K2 ("not inside the record's abstractText") is therefore not enforced.
- Demonstration (`R98ScoutSources-k2-check-quotes.txt`, exit 0): the committed entry gives `check_quotes bad = []`. A synthetic entry adding two S231 quotes that are not in `abstractText` — `"Journal of clinical epidemiology"` (in `journalInfo`) and `"McGowan J, Sampson M, Salzwedel DM"` (in `authorString`) — also gives `check_quotes bad = []`. The FORGERY battery (f1–f7) does not cover this case.
- Fix options for the lane (not applied by this seat): check M-rows against plain `abstractText`, or add a source label for title-sourced quotes and reword line 30.

### F2 — K3 fires: one Never cell is neither the negation of its Do clause nor "(none stated by the sources)"

- Entry line 103, "Saying what evidence stands behind the elements": Never = "say that the abstract reports evidence for each question; it speaks of elements". Its Do clause says what the systematic review found and what its results suggested; the Never prohibits a per-question-evidence claim that the Do does not mention. Claim sentence (`claims.md`, C2 "Do and Never cells ... every round-98 Never cell is the negation of its Do clause or '(none stated by the sources)'") is false for this row. Receipt: `R98ScoutSources-decision-rows-and-element-paragraph.txt`.
- The other nine Never cells (rows 102, 104, 105 and 106–111 of the decision table): three are negations of their Do clauses (the Citing row "cite the checklist as if it were the whole guideline"; the Timing row "report the timing as a finding of the systematic review"; the element row "treat skilled translation … as a PRESS 2015 element"), and six are "(none stated by the sources)". Row 103 is the only one that fails K3.

### F3 — K4 held, note only: the element paragraph lists differences in form but not all

- Entry lines 91–94 say "they differ in form (…)" and list four kinds (numbering, parenthesis, "Text word searching", serial comma). Capitalisation also differs: S231 "translation", "spelling", "limits" vs S225 "Translation", "Spelling", "Limits" (both verified by substring on the two captures, receipt `R98ScoutSources-decision-rows-and-element-paragraph.txt`). The paragraph misstates nothing, so K4 holds; the list reads as complete and is not.

### F4 — K1, K2 (K-quotes), K5 held

- K1 predicate lines all observed (§3 receipts).
- K2 for K-quotes: all 22 are substrings of their capture lines (§2).
- K5 identity: held on all reprint-checkable fields (§3). PMID not reprint-checkable (single source).

### F5 — named-limit gap: "all answered http 403" covers the URLs tried, not the routes

- Entry lines 15–18: "the statement's full text, the CADTH E&E, its Table 9 and the CADTH report 477 appendices all answered http 403 or a challenge page to this host". Each is true of the one URL tried (refetch rows: S224 jclinepi 403; S223 `CP0015_PRESS_Update_Report_2016.pdf` 403; S227 `Table_9-PRESS.pdf` 403; S228 report 477 appendices 403). Two untried URLs exist (§5, L1 and L9). The entry's named limit (a) does not say the list is per-URL. Wording note, not a counted K-rule.

### F6 — record internal inconsistency (note)

- S231 record: `isOpenAccess: "N"`, `hasPDF: "N"`, `inPMC: "N"`, but `fullTextUrlList` carries `"availability": "Open access", "site": "Unpaywall", "url": "http://www.jclinepi.com/article/S0895435616000585/pdf"`. The entry does not mention this link (L1 below). Receipt: `R98ScoutSources-quotes.txt`.

## 5. Full-text and E&E leads (web_search only; none fetched by this seat)

Full list with the tried/untried status is in `R98ScoutSources-routes.txt`. Untried leads, in priority order:

- L1 `http://www.jclinepi.com/article/S0895435616000585/pdf` — the Unpaywall OA PDF URL inside S231's own record (not in the plan's route table).
- L9 `https://www.cda-amc.ca/sites/default/files/attachments/2021-07/CP0015_PRESS_Update_Report_2016_0.pdf` — CADTH PRESS 2015 Explanation & Elaboration, a different URL from the round-96 S223 URL that returned 403.
- L5 `https://core.ac.uk/download/pdf/82048291.pdf` — CORE aggregate of a repository copy of the statement (repository-class; plan names "institutional repository" but this URL is not in its table).
- L2 `https://www.jclinepi.com/article/S0895-4356(16)00058-5/fulltext`; L3 `https://www.sciencedirect.com/science/article/pii/S0895435616000585`; L4 `https://www.jclinepi.com/article/S0895-4356(16)00058-5/addons` (supplementary materials).
- L6 Sydney eScholarship via library discovery; L7 `https://scholar.archive.org/fatcat/release/bf1fef9f-838c-4f92-b2f6-8aad9203be20`; L8 a Scribd upload (rights and provenance unverified); L10 CDA-AMC companion page; L11 CDA-AMC translations page (Portuguese/Spanish Tables 8–10); L12 `https://colab.ws/articles/10.1016%2Fj.jclinepi.2016.01.021` (index reproduction of the abstract, not a full text).
- PMC: a web_search result reports no PMC author manuscript; no PMC URL was checked.

## 6. Not done

- C1 was not examined by this seat; the `selftest-controls-r98.py` battery was not run.
- No S231/S225 quote was reinterpreted beyond the substring and identity checks above.

VERDICT: R98ScoutSources C1 n/a — not examined by this seat; the battery and the self-test were not run.
VERDICT: R98ScoutSources C2 fired — K2 (M1 is sourced from the record's title, not abstractText, and check_quotes tests the whole capture so a non-abstract S231 quote passes) and K3 (decision row "Saying what evidence stands behind the elements" has a Never cell that is neither a negation of its Do nor "(none stated by the sources)"); K1, K4 and K5 held, with the notes in §4.
