# R99CriticClaims — adversarial review of claims.md (both claims) at F

Seat `R99CriticClaims`, lane chousa round 99, L1 `ChousaR99` holds the canonical planner seat. F = `d41f4cd8b857c6de683e7be5c5e8125b32763a8e`, base `47ed34fa785288837f84cde9db15c41300854a78`. Tree: shared clone checked out at F under `/fast/scratch/hyaku/chousa-r99/R99CriticClaims/repo` (batteries run against the clone, never the live lane). No network use; no production edits; scratch removed on exit. Tooling: no installs (operator tooling directive read; pacman paused per 2026-10-20 ruling; task uses only python3/git/GNU grep 3.12).

Method: every clause of each claim sentence was mapped to the instrument leg enforcing it, or shown unenforced. Two cheap stand-ins per claim were built and run through the frozen counters. Citations below name the exact command, the receipt in this directory, the observed line, and the exit code. Receipts live in `.ufo/waves/round-99/w1/` and correspond to `Report:` paths as instructed.

## Summary

- C1 sentence: **substantively true** (the frozen tool does implement the stated rule, verified by direct code read of `tools/gate-records.py:104-128,280,307` and by the battery). Two wording/evidence defects stand: the "30-word page" clause is false (28 words), and the causal-separability sentence ("no C2 file") is false (POS legs read C2's S233/S236 captures; HARM leg reads the C2 entry). The battery's oracle defense is string-identity fragile, but this is exactly the disclosed named limit (f).
- C2 sentence: **true as stated** (23 quotes, 8 rows, every number sourced — all verified). Two assessment problems: K5 Do-fidelity is unenforced by the counting commands (a reversed-Do forgery passes all legs) — this is honestly named as "reviewer, not the controls", limit (c) — and the axis label "coverage" is defensible but depth-shaped; it credits a decision table that AXES.md's depth row describes verbatim, so an axis double-count risk exists. Neither falsifies a number.
- No kill-rule violation was found in the frozen counters themselves (C1 battery PASS 7/7, 4/4, 4/4, 25/25, 7/7, 5/5; C2 counters PASS 25/25, CLEAN, 4/4, controls PASS).

## Axes

1. coverage (AXES.md: fraction of the domain's real surfaces governed; a new measured surface counts).
2. depth (verifiable detail — decision tables with real thresholds, named error signatures, cited sources).
3. operability (runnable artifacts; a checklist item runs and produces the stated outcome).
4. calibration (self-assessment honesty; overreach caught).
5. freshness (drift detection).
6. adjacency (cross-domain awareness, not absorbed).

## C1 `C1-GATE-CHALLENGE-R99` — clause-by-clause audit

### Instrument map (each clause → enforcing leg)

| Claim clause | Instrument leg | Result |
|---|---|---|
| "`verify` gains a CHALLENGE check" | `tools/gate-records.py` `is_challenge` (`norm().lower()`, `≤200` words, any of 11 `CHALLENGE_MARKERS`), called from `check()` admit branch (line 280) and rev-capture branch (line 307) | True (code read) |
| "a url/admit record, or a rev record whose path is `corpus/captures/<24 hex>.txt`, fails with code CHALLENGE (exit 1)" | `check()` appends `CHALLENGE`; `main` exits 1 on any failure. `CAP_RE` exactly `corpus/captures/([0-9a-f]{24})\.txt` | True; `verdict()` regex enforces CHALLENGE alone (a `FAIL CHALLENGE,REFETCH` verdict ≠ `CHALLENGE`) |
| "has at most 200 words and contains one of the 11 frozen `CHALLENGE_MARKERS`" | `len(t.split()) <= CHALLENGE_MAX_WORDS` (200) and `any(m in t)` over the 11-tuple (lines 110-122) | True (counted 11; 200 exact) |
| "refuses seven challenge-page records in a scratch lane (three committed captures — S230 reCAPTCHA, S229 cookie wall, S234 "Client Challenge" — and four written by the battery)" | NEG legs n1-n7: n1 S230 (23 words, markers `checking your browser`, `recaptcha`), n2 S229 (18 words, `cookies must be enabled`), n3 S234 (37 words, `client challenge`, `couldn't load`), n4 CF, n5 Turnstile, n6 Attn, n7 S230 upper+double-spaced | True; receipts confirm |
| "admits four non-challenge records (two committed captures, a 300-plus-word article that names "reCAPTCHA" and "Just a moment", a 30-word page with no marker)" | POS p1 S233 (8,455 words), p2 S236 (307 words JSON), p3 ARTICLE (381 words, both markers inside long prose), p4 SHORT | **"30-word" FALSE — SHORT is 28 words** (see F1). Remainder true |
| "refuses four records on the production path (`--root` the lane: url/admit on S230 and S234, rev on S230 and S229 at BASE)" | PROD legs: 2 url/admit records + 2 rev records (`corr` via `git show BASE:path`; `run()` verifies with `--root lane`) | True |
| "prints output byte-identical to the base tool on every committed knowledge/lesson file carrying GATE-RECORD lines" | HARM leg compares `(returncode, stdout)` per file (lines 188-193); 25 files at F, 25/25 same | True in substance; the battery compares stdout+rc only, not stderr. The tool emits no stderr on these files in practice, so "byte-identical output" is accurate, though the battery does not capture stderr. Not falsified |
| "five stand-in tools (short-only, marker-only, known-bytes, scratch-only, lane-only) each fail the battery" | ORACLES o1-o5 patched from the candidate; `ORACLES_REJECTED=5/5` | True — but each oracle is a string-patch of the candidate (sites must match exactly once). Any non-identical reimplementation fails `SITE-MISSING`, which is a degenerate fail, not a principled rejection. Named limit (f) discloses the undetected detection surfaces |
| "The base tool admits all seven challenge records" | `BASE_NEG_ADMITTED=7/7`; receipt `before/c1-base.txt` | True (also re-verified at F against the clone) |

### Stand-in attacks (run through the frozen battery)

Both forgeries avoid the claimed general property entirely. Neither counts words nor matches markers. Both exploit exactly the named-limit-(f) surface: fixture shape, not content.

**Forge A** (`R99CriticClaims-forgerA-tool.txt`, battery output `R99CriticClaims-forgerA.txt`): refuses `CHALLENGE` when the URL host contains `fixture.invalid` with suffix `/n*` (scratch NEG), and when the capture/rev path is one of the three PROD captures' committed paths. Command: `python3 -B corpus/evidence/round99/challenge-controls-r99.py --root . --work <scratch> --tool <forgeA> --no-oracles` → `NEG_REFUSED=7/7 POS_ADMITTED=4/4 PROD_REFUSED=4/4 HARM_SAME=25/25 BASE_NEG_ADMITTED=7/7 ORACLES_REJECTED=0/0`, `CHALLENGE_CONTROLS_R99=PASS`, exit 0. With the oracle leg enabled it fails only because the oracle string-patches don't match its source (`SITE-MISSING`), `ORACLES_REJECTED=0/5`, exit 1 — a fail for scaffolding reasons, not for catching a forgery. A new challenge page on any other host would be admitted by forge A.

**Forge B** (`R99CriticClaims-forgerB-tool.txt`, output `R99CriticClaims-forgerB.txt`): refuses `CHALLENGE` when the source id number is ≥900 with `/n*` URL suffix (the Lab numbers fixtures `S901`+), plus the same three PROD paths. Same tallies, same `PASS` under `--no-oracles`. Two independent forgeries pass the scoring legs without implementing the rule. The claim sentence is therefore not entailed by the battery legs alone; the sentence remains true of the frozen tool by direct inspection, and limit (f) names this class verbatim ("a forger that detects the battery any other way (process tree, `S9xx` fixture ids, the `fixture.invalid` host) is not scored"). The battery's full-predicate PASS for the frozen tool is genuine (receipt `R99CriticClaims-c1-battery.txt`: all 5 oracles principlly rejected, `CHALLENGE_CONTROLS_R99=PASS`, exit 0, deterministic across two runs — identical sha256 `bb0cb776…` both runs, receipt `R99CriticClaims-determinism.txt`).

Named limits (a)-(e) each verified against the instrument: (a) >200-word or synonym challenge pages pass (ARTICUTE leg p3 proves the >200 side; synonyms not in the 11 markers pass by construction); (b) false refusal of a short marker-bearing real document is admitted — the POS set contains no such control; (c) no NFKC — verified (`norm()` only folds curly quotes + whitespace); (d) `unreach` form and non-capture `rev` paths unchecked — verified in `check()`; (e) five oracles cannot show every wrong tool fails — exactly what forges A/B demonstrate.

### Do-nothing control: is the base tool the cheapest skip?

Yes. The cheapest tool that skips the CHALLENGE work is the base tool (admits everything). It is also the strongest possible "skip" that still parses: an empty stub would error, not admit, and fail K2/K3 differently. `BASE_NEG_ADMITTED=7/7` with `NEG_REFUSED=0/7 PROD_REFUSED=0/4 CHALLENGE_CONTROLS_R99=FAIL` — re-verified at F (receipt in analysis log). PASS with `--tool` = base is impossible (K5 holds). The control is minimal and honest.

## C2 `C2-ENTRY-R99` — clause-by-clause audit

### Instrument map

| Claim clause | Instrument leg | Result |
|---|---|---|
| "New entry `corpus/knowledge/quotation-error-rates-r99.md`, sourced on S236 (Europe PMC's core record of Jergas & Baethge 2015, the authors' own abstract, tier B)" | S236 capture parsed as JSON: `hitCount` 1, `pmid` `26528420`, `doi` `10.7717/peerj.1364`, `pubYear` `2015`, journal PeerJ, volume `3`; `abstractText` head matches. Registry row tier B, carrier rule | True (IDENTITY 2/2, verified manually) |
| "S233 (Mogull 2017, publisher full text, tier A)" | Capture carries doi `10.1371/journal.pone.0184727` and G0 title (8,455 words) | True |
| "both opened this round" | Refetch rows S233/S236 dated 2026-11-09, http 200; rejects S232 (403), S235 (500) | True |
| "holds 23 located quotes (J0-J8, G0-G13)" | QUOTES 23/23 (9 J + 14 G), FIELD 9/9 (J0 = title field, J1-J8 ⊆ `abstractText`) | True |
| "an 8-row decision table on how often a cited source fails the citing sentence, how a mismatch is classed (major/minor, source error) and how the rate is counted" | WARRANTS 8/8; rows cover rate (row 1), major/minor (row 2), source/content (row 3), denominator (row 4), ascertainment differences (row 5), sampling (row 6), split (row 7), prevention (row 8) | True |
| "Every number a Do cell states is printed in one of that row's own warrant quotes" | NUMBERS/NUMBERS_SOURCED 6/6: 28, 25.4%, 11,9%, 14.5%, 6.7%, 64.8%, each `in` its row's warrant text as written (substring match, exact token) | True (substring-weak, but all six genuinely appear; e.g. `28` from J1 "included 28 in the main analysis") |
| "At BASE no knowledge entry contains the phrase "quotation error" and the entry is absent" | TOPIC/BASE legs over `git ls-tree BASE corpus/knowledge/`: `BASE_TOPIC_HITS=0`, `BASE_ENTRY=absent` | True; capture side covered by Q1 search (0 hits — entry `## Searches`), which the sentence does not bind to the controls — correctly so |
| "S232, S234, S235 rejected" | S232/S235 have `decision=reject` GATE-RECORDs matching refetch 403/500; S234 appears once in prose ("rejected for route and nothing here rests on it", no GATE-RECORD) | True in substance; S234's rejection is prose, not a gate record. The gate counts it only as absence of support, which holds |

### Stand-in attacks

**C2 forgery (Do-reversal)** (`R99CriticClaims-forgerC2.txt`): reversed the Do cells — "unreliable" → "reliable", major/minor swapped, denominator/numerator swapped — while keeping every number and every warrant. Run via entry-controls `score()` (in-memory copy of the entry): `QUOTES=23/23 FIELD=9/9 IDENTITY=2/2 WARRANTS=8/8 NUMBERS=6/6 TOPIC=1/1` → passes=True. The counting commands therefore cannot enforce K5. This is exactly what the claim and limit (c) concede: "K5 is reviewer-judged", "the controls check numbers and quote presence, not that a paraphrase is faithful beyond its numbers".

Auditor's K5 review of the landed entry itself (all 8 rows against their warrants): rows 2, 4, 5, 6, 7, 8 paraphrase tightly. Two soft widenings (not reversals):
- Row 1 Do: "treat an unchecked citation as **unreliable**" — warrants say errors are "common" and give rates; no warrant prescribes the treatment. The normative force is the lane's addition (partly laundered into the Never column honesty, `(none stated by the sources)`).
- Row 3 Do: "(the cited source was not read)" — G6 defines source errors as "secondary (or indirect) citations"; the parenthetical gloss goes beyond the quote.
Neither reverses a quote. Both are the class limit (c) names ("a paraphrase can still narrow or widen a quote's meaning"). No K5 kill fires on the landed text, but K5 has no instrument — it is a human attestation, and the strongest available counterexample (reversal) passes the counters.

**Second stand-in (number-dropping Do cells)**: replacing 25.4%/11,9%/14.5% with prose changes QUOTES (21/23 — the edits broke quote rows because the numbers sit inside G-quotes, not Do cells) and NUMBERS (4/6), so it is refused — but that refusal rides on quote-table edits, not on Do-cell numbers. Do-cell numbers are checked only for presence in warrants; a Do cell with no numbers (e.g., "report the rate without its denominator") would pass NUMBERS vacuously for that row. Not exploited here because WARRANTS 8/8 still binds the row to real quotes, but the instrument does not force Do cells to state numbers.

### Is "coverage" the right axis?

By AXES.md, defensibly yes — and the alternative (depth) double-counts. The base had zero knowledge content on quotation-error rates (`BASE_TOPIC_HITS=0`); the entry opens a new measured surface inside PROVINCE's owned method (claim-vs-source verification), exactly the coverage signal ("PROVINCE lists every surface; none unexplored without reason"). SCORECARD's per-axis convention supports this: past rounds credit coverage when a new method becomes verdict-bearing and depth when an entry documents an existing surface's semantics. This entry is depth-shaped in form (decision table with thresholds and citations, AXES depth row verbatim) but coverage in substance (first entry on the topic). A round may credit one axis per claim (two claims on one axis count as one); claiming both coverage and depth for this single entry would double-count. The claim's parenthetical "new province ground: measured quotation-error rates" is the honest part and matches the evidence. One provenance nit: SCORECARD `## Planned — round 99` item 3 promised depth (the press-guideline question wording); the plan substituted C2's coverage entry for that depth item. The plan (L1's seat) is the frozen contract, and the substitution is disclosed in `plans/round-99.md`, but the round as landed does not close the planned depth debt — a Hagber streit, not a false number; worth a carried-debt line in the lesson.

## Causal separability

- **C2 gate under the BASE tool**: verified. `python3 -B <base tool> verify --root . corpus/knowledge/quotation-error-rates-r99.md` → `records=25 ok=25 fail=0`, exit 0. Both tools admit C2's records (no capture is a challenge page). This half of the separability sentence holds.
- **C1 battery without C2's files**: does **not** hold as written. The battery's POS legs read S233's and S236's captures (POS p1/p2 are the C2 sources' captures), and the HARM leg enumerates every `corpus/knowledge/*.md` carrying GATE-RECORD lines — the C2 entry among them — comparing candidate vs base stdout on it (25/25 same, because both tools admit C2's records). The battery crashes at BASE regardless (missing C2 captures: `FileNotFoundError … b90988847e704a08aabc8321.txt`). The dependency is **benign** (HARM compares the two tools, neither of which starves on C2's records), so the claims are separable in substance — but the printed sentence "the battery reads S234's capture … and no C2 file" is literally false. The correct sentence: the battery reads C2's captures (as POS material) and C2's entry (as HARM material), and both still pass because neither gate-starves on them.

## Findings, with counters

Active lines are quoted from receipts already verified. Severity = what breaks if the finding is taken as-is.

- **F1 (C1, wording FALSE, minor):** "a … 30-word page with no marker" — the SHORT fixture is 28 words by both raw and normalized count (battery constant `SHORT`, 28 tokens). Counter: the battery counts no word length on POS legs; POS passes regardless. Observable fix: change "30-word" to "28-word". Receipt: `R99CriticClaims-c1-battery.txt` (POS p4 PASS) plus a word-count command in the audit log (28 words, exit 0).
- **F2 (separability sentence FALSE, moderate):** "C1's battery reads S234's capture … and no C2 file" — battery code (`CAP` includes `S233`/`S236`; `harm_files()` sweeps `corpus/knowledge/*.md` GATE-RECORD files, including the C2 entry) reads C2 files; it errors at BASE where C2 captures don't yet exist. AXES requires claims causally separable ("each verifiable without the others having landed"); here the battery has a hard setup dependency on C2's round — not on the C2 claim's truth, but on its bytes being present. Observable fix: restate the sentence and name the shared dependencies (S233/S236 captures, C2 entry in HARM) plus why they don't confound (both tools admit them). Counter: `FileNotFoundError` when the same battery runs with `--root` at BASE (S234 capture missing), exit 0 (script's own tail) — receipt in audit log; HARM_SAME=25/25 includes the C2 entry.
- **F3 (C1, evidence gap, disclosed — no action, do not re-claim):** the battery legs (`--no-oracles`) PASS for two forgeries (A, B) that implement no general rule; the full battery rejects them only via `SITE-MISSING` string-matching, not by catching forgery. Named limit (f) already covers this class. Counter: forgerA `NEG_REFUSED=7/7 POS_ADMITTED=4/4 PROD_REFUSED=4/4 HARM_SAME=25/25` `CHALLENGE_CONTROLS_R99=PASS` exit 0 (`R99CriticClaims-forgerA.txt`); forgerB identical (`R99CriticClaims-forgerB.txt`). With oracles on, both print `ORACLES_REJECTED=0/5 … FAIL`, exit 1, solely via the exact-string requirement. Judgement: operability credit should be weighed against the disclosed forger class, per QUALITY 126 — the rule itself is genuinely implemented (code read), so this is a battery-hardening note for round 100, not a falsification of the frozen sentence (beyond F1).
- **F4 (C2, K5 unenforced — disclosed, moderate):** reversed-Do entry passes `score()` fully. Counter: `passes=True, QUOTES…NUMBERS=6/6` (`R99CriticClaims-forgerC2.txt`). Limit (c) concedes this. Judgement: the "coverage" credit for C2 rests on a reviewer attestation the machine counters cannot produce; the round's verification story for the decision table is half mechanical, half human — and the human half is not yet on record from a non-author reviewer (who "attested K5 clean" for the 8 rows? No reviewer pointer appears in the frozen materials — unlike the exploratory-claim rule, K5 has no named-reviewer requirement, but credit should not pretend otherwise).
- **F5 (C2, K5 soft widenings — minor, non-killing):** Row-1 "unreliable" prescription and Row-3 "(the cited source was not read)" gloss exceed their warrants. Neither reverses a quote; both sit inside admitted limit (c). Recommended: either soften to quote-faithful wording ("treat as *common enough to re-open*") or name the inference in the Lane column (as the entry already does for its own readings generally). Counter: full decision-table read in the audit log (lands after the F2 section) — every row quoted.
- **F6 (C2/S234, form mismatch — minor):** "S232, S234, S235 rejected" is instrument-true for S232/S235 (gate-record `reject` rows, http 403/500 matching refetch) but prose-only for S234 (one sentence, no GATE-RECORD). A reader auditing "rejections" via gate records alone would find only two. Observable fix: one line in `## Gate records` for S234 as `decision=reject` (http 200, `words=0` in the unreach form) or drop S234 from the "rejected" clause. No counter needed — `grep -c S234` = 1, zero GATE-RECORD S234 lines.

## Axes: impacts

- **operability (C1)**: improved and runnable (`CHALLENGE` refuses the defect class end-to-end, deterministically — identical sha256 across runs), but the battery evidence is forger-fragile (F3). Lowest axis correctly chosen (3/10 per SCORECARD); credit warranted with the forger class priced in.
- **coverage (C2)**: improved (new measured surface, `BASE_TOPIC_HITS=0` → 23 quotes + 8 rows). Depth-shaped form risks an implicit depth credit; claim only coverage. K5 soft widenings (F5) do not fail the coverage move.
- **calibration**: improved — nearly every limit the auditor needed is already named ((a)-(f), (c), S234 prose rejection). The claim's own English, however, overstates in two places (F1 "30-word", F2 "no C2 file"), and the round planned-depth substitution leaves a carried debt (the press-guideline item) that `plans/round-99.md` should carry forward explicitly.
- **depth/freshness/adjacency**: no axis moved by either claim; none harmed.

## Smallest safe corrections

1. F1: "30-word" → "28-word" in `claims.md`/`plans/round-99.md` (one word each).
2. F2: rewrite the causal-separability sentence: battery reads C2's captures (POS) and C2's entry (HARM) and needs them present; claims separable in outcome because both tools admit C2's records.
3. F4: attach a named non-author reviewer attestation for K5 (8 rows) or downgrade the decision-table credit to "numerically sourced; paraphrase reviewer-attested as of …".
4. F3: round 100: add a forger that detects via process tree / argv / cwd (QUALITY 126 class) and a POS control for a short marker-bearing real document (limit (b) currently unproven by any leg).
5. F6: add the S234 reject GATE-RECORD or narrow the "rejected" clause to S232/S235.
6. Carry the planned-depth item (press-guideline question wording) into round 100's planned section — it was displaced, not closed.

## Verdicts

VERDICT: R99CriticClaims C1 fired — "30-word page" is 28 words and "no C2 file" is false (POS reads C2's captures, HARM reads C2's entry), though the tool implements the rule and all tallies pass.
VERDICT: R99CriticClaims C2 held — 23 quotes, 8 rows, all numbers sourced, identities exact, rejects as stated; K5 is reviewer-only (disclosed) and the coverage axis is defensible.

## Receipts

| Receipt | Command (in clone at F) | Observed |
|---|---|---|
| `R99CriticClaims-c1-battery.txt` | `python3 -B corpus/evidence/round99/challenge-controls-r99.py --root . --work <scratch>` | `NEG_REFUSED=7/7 POS_ADMITTED=4/4 PROD_REFUSED=4/4 HARM_SAME=25/25 BASE_NEG_ADMITTED=7/7 ORACLES_REJECTED=5/5`, `CHALLENGE_CONTROLS_R99=PASS`, exit 0 |
| `R99CriticClaims-c2-controls.txt` | `python3 -B corpus/evidence/round99/entry-controls-r99.py --root .` | `QUOTES=23/23 FIELD=9/9 IDENTITY=2/2 WARRANTS=8/8 NUMBERS=6/6 TOPIC=1/1 NUMBERS_SOURCED=6/6 BASE_TOPIC_HITS=0 BASE_ENTRY=absent FORGERY_REFUSED=10/10 ACCEPTED=2/2`, `ENTRY_CONTROLS_R99=PASS`, exit 0; gate 25/25, metadata CLEAN, rerun 4/4 (verified by hand at F) |
| `R99CriticClaims-forgerA-tool.txt`, `R99CriticClaims-forgerA.txt` | battery `--tool <forgeA> --no-oracles` | `7/7, 4/4, 4/4, 25/25, 7/7, 0/0`, `PASS`, exit 0 (no general rule) |
| `R99CriticClaims-forgerB-tool.txt`, `R99CriticClaims-forgerB.txt` | battery `--tool <forgeB> --no-oracles` | same PASS with independent S9xx-based fingerprint |
| `R99CriticClaims-forgerC2.txt` | entry-controls `score()` on reversed-Do in-memory entry | `passes=True` (QUOTES 23/23 … NUMBERS 6/6) — K5 unenforced by counters |
| `R99CriticClaims-determinism.txt` | two battery runs | identical sha256 `bb0cb776…` — deterministic |
