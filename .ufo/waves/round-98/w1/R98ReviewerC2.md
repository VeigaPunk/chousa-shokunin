# R98ReviewerC2 — fidelity review of `corpus/knowledge/press-2015-statement-questions-r98.md` at F (`aac8268`)

Method: shared clone at F; every quote checked against capture bytes; gates/controls re-run.
No tool installs (nothing installed; RULES.md read — pacman paused per orchestrator ruling; none needed).

Receipts in `.ufo/waves/round-98/w1/R98ReviewerC2-*`. Every finding names the exact command, receipt path, observed line, exit code.

## Findings (severity order)

### F1 — K2 FIRE. M1 is not inside the record's `abstractText`.

- Command: `python3 -B` JSON/normalization probe over `corpus/captures/4ec85a1e83553aa272caeb69.txt` (sha256 `4111c45a…0429` verified), testing the 15 M quotes against `resultList.result[0].abstractText` plain and with `gate-records.py` normalization.
- Receipt: `.ufo/waves/round-98/w1/R98ReviewerC2-M1-abstract.txt`
- Observed: M2–M15 all `True` (exact, inside `abstractText`); M1 `False` both ways (`M1 in abstractText exact: False`, `norm in abstractText: False`, `norm in full capture: True`). Record `title` is `'… Guideline\xa0Statement.'` (NBSP) — M1 is not byte-equal to the title either.
- Why it kills: claims.md C2 K2 — "an S231 quote is not inside the record's `abstractText`." The controls (`check_quotes` in `entry-controls-r98.py`) and `tools/gate-records.py` both test the whole capture, so both pass M1 (`GATE_RECORDS files=1 records=38 ok=38 fail=0`, rc 0; `ENTRY_CONTROLS_R98=PASS`, rc 0) — the abstract-containment clause is reviewer-only. Nothing else catches it.
- False sentences: entry line 30 "Every S231 quote below is a substring of that string [the `abstractText` string]" — false for M1. C2 claim sentence "holds the … abstract … in 15 located quotes" — 14 abstract quotes + 1 title quote presented as 15.
- Impact: bibliographic fact true (title is the statement's title); row-1 warrant use sound. Firing is on framing/counting ("15 abstract quotes"), not substance.

### F2 — K3 FIRE (strict). Row 2 Never is not its Do's negation.

- Text (entry lines 102–103): Do: "say that the statement's systematic review found no new search elements to add and no evidence refuting any of the existing elements, and that its results suggested structured PRESS could identify…" (M3–M6). Never: "say that the abstract reports evidence for each question; it speaks of elements."
- Negation of Do = "do not say X / do not say Y". Never prohibits an unmade third claim (question-level evidence). Per K3 ("must be the negation of its own Do clause or `(none stated by the sources)`"), it fires on a strict reading.
- Sub-note (not a fire): Do drops M4's scope ("for addition to the existing (2008-2010) Checklist") and needs the Results' "Systematic review:" prefix (not in M3–M6) for its attribution. Minor overreach.
- Related note, not scored: Row 1 Never negates one conjunct of a two-conjunct Do (cite-statement half; silent on name-the-document half) — defensible partial negation.

### F3 — Line-number fidelity defects (wording says more than it counts).

- Command: `sed -n Np` / `grep -n` / Python `splitlines()` probes over `corpus/captures/347c55ba9be9d63afe17986e.txt` (sha `abd08a93…9c8`; 2 form feeds, 0 CR, 83 LF).
- Receipt: `.ufo/waves/round-98/w1/R98ReviewerC2-linenums.txt`
- Observed: entry's "K17-K18 = line 66, K19 = line 67, K21-K22 = line 78" is exactly right under `sed`/`grep` (66 = "Have the appropriate fields…", 67 = "or excluded…", 78 = "Are any potentially helpful limits…") but off-by-one under Python `splitlines()` (67/68/79) — the same ambiguity r97 documented (`press-checklist-questions-r97.md:27-29`) and r98 never resolves.
- Claims (c) / entry "lines 64, 65, 78 carry several; 66-67 one": under sed, multi-`?` lines are **53 (2), 64 (3), 65 (3), 78 (3)** — line 53 (K9, two questions one quote) omitted by both. "66-67 one" is true as a `?`-count (1 per line), false as a question-count (two questions: one whole in 66 + one split across 66–67 = K17–K19). The 36/36 line count itself re-verified (`QUESTION_LINES_HELD=36/36 BASE_HELD=16/36`).

### F4 — Note; K5 HOLDS. Page elision "40-6" vs "40-46".

- S225 lines 82–83: `2016 Jul;75:40-6` (elided). S231 `pageInfo: 40-46`. Entry Named limits parents `(J Clin Epidemiol 2016;75:40-46, …)` as "agree[ing]" with S225 — strictly the entry expands S225's elided form. K5 (title/authors/DOI/PMID vs Derived-from) all match (authors identical; title modulo NBSP; DOI `10.1016/j.jclinepi.2016.01.021`; PMID 27005575). No fire; bibliographic identity unaffected.

### F5 — Reservation (no fire). Tier A "for the abstract scope" from an index record.

- Europe PMC record is `SRC:MED`, single result (`hitCount: 1`), `inEPMC: N`, `hasPDF: N` — an NLM index record, not the publisher's page (entry discloses this, lines 141–142). Tier A for the MEDLINE-supplied abstract text is defensible given the tight scope (abstract only; body/checklist/E&E excluded), but a carrier-based reading by the lane's S123/S124 logic (third-party copies = tier B) would make it B. The gates cannot test this; it is the judgement the next round should reconfirm before ever citing S231 for statement-body claims.

## Held (verified, not fires)

- **Quotes.** M2–M15, K1–K22 exact substrings of captures; ≤25 words each (max K17 = 22). Gate re-runs at F, all rc 0: `python3 -B tools/gate-records.py verify --root . corpus/knowledge/press-2015-statement-questions-r98.md` → `GATE_RECORDS files=1 records=38 ok=38 fail=0`; `bash tools/research-gate.sh verify-metadata … --root .` → `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`; `python3 -B tools/search-rerun.py verify …` → `rev_match=5/5`, `SEARCH_RERUN: CLEAN`; `python3 -B corpus/evidence/round98/entry-controls-r98.py --root .` → `ENTRY_CONTROLS_R98=PASS`. Receipts: `R98ReviewerC2-entry-controls.txt` etc.
- **Decision rows 3–10 — faithful.** Row 3: Do = M7+M8 verbatim + "survey of experts" from M3; Never = true negation (survey-feeling vs SR-finding). Row 4: Do verbatim M9/M10, Never negation via M11. Row 5: Do M11/M12 (forum attribution structural, warranted); Never `(none stated)` defensible. Rows 6–10: Do paraphrases faithful (dropped sub-questions are narrowings, e.g. K15 "capture irrelevant material", K16 "too many/too few"); all Nevers correctly `(none stated by the sources)`.
- **Elements table (K4).** All S231 cells in normalized `abstractText`; all S225 cells whole capture lines; order agreement + each form difference (numbering; parens on 2/3/4; "searching" vs "search"; serial comma on 5) re-derived; S223 pointers (L20–L23, L26–L27) verified against `search-peer-review-dedup-r96.md`.
- **Lane cells.** Checked against tree at F: r97 = reprint questions only; r96 holds timing; `tools/search-rerun.py:26-29` documents fixed/`regex` (grep -F / Python re modelled on grep -P) so "GNU grep expressions over its own capture store" is fair for the recorded searches ("no second database" true); `where`-glob limit and subject-heading non-applicability match r97 rows; SKILL.md carries question framing. Marginal: row 5's "GNU grep expressions" elides Python-`re` regex — noted only.
- **SOURCES.md S228–S231.** S231 row (tier/scope/anchor/teaches/`mined`/2026-11-09/`on-release`/used-by) matches refetch row `S231 … 2026-11-09T02:48:35Z 0 200 4111c45a…` and capture sha. S228: `rejected`, anchor "none located … curl rc 22 HTTP 403", matches refetch (403, `-`, `-`); no capture file exists (verified absent). S229/S230 rejections match stored challenge bytes ("Cookies must be enabled", key `09541495…`; "Checking your browser … reCAPTCHA", key `b5b8d05…`). Snippet-sourced identities honestly parenthesized; no fabricated quote.
- **As-run.** Q1–Q5 re-run with `/usr/bin/grep -F` on the base-revision capture store archive: 0/0/0/1/2 as recorded (S231 capture absent at base — verified). At F: Q1–Q4 each also find S231's capture (entry says "Q1-Q3 now find", true and incomplete re Q4 — not false). Both capture shas match the entry's GATE-RECORD fields.

## Residual risk / verification gaps

- No live re-fetch of S231 (leaf bounds; no network): the record as captured is byte-verified, the live record was not re-opened.
- Tier-A-for-index (F5) is untestable by gates; flagged as judgement.
- C1 not re-scored under this fidelity mandate.

VERDICT: R98ReviewerC2 C1 n/a — not in this seat's fidelity scope.
VERDICT: R98ReviewerC2 C2 fired — M1 is record title, not `abstractText` (K2: "15 abstract quotes" overstates), row-2 Never is not its Do's negation (K3 strict); 36/36 lines, elements, K5 identity and SOURCES otherwise hold.

Report: .ufo/waves/round-98/w1/R98ReviewerC2.md
