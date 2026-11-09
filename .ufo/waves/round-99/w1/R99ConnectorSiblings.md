# R99ConnectorSiblings — cross-lane pattern scan (route, do not absorb)

Seat: connector (leaf). Round 99, lane `chousa`. Attacked tree: shared clone of F
`d41f4cd8b857c6de683e7be5c5e8125b32763a8e` at `/fast/scratch/hyaku/chousa-r99/R99ConnectorSiblings/repo`
(`git -C $S/repo rev-parse --show-toplevel` → the scratch dir, asserted in every receipt).
Read-only over the sibling lanes (`git -C <lane> show/grep HEAD`); no lane or fleet mutation, no commits,
no network. Installed nothing.

Tool bytes are identical at F and at the lane HEAD `f8f480ffd738cda9b427e0fe8fa8e79c78fb409d`:
`tools/gate-records.py` sha256 `e92c4526…`, `tools/quarantine-check.py` sha256 `8e74549d…`,
`corpus/evidence/round99/challenge-controls-r99.py` sha256 `6f354228…` (both `git show` sides).

Receipts written (all under this directory):

- `R99ConnectorSiblings-c1-path-bypass.txt`
- `R99ConnectorSiblings-c1-battery-at-F.txt`
- `R99ConnectorSiblings-classifier-divergence.txt`
- `R99ConnectorSiblings-crosslane.txt`
- `R99ConnectorSiblings-c2-k5-candidate.txt`

Axes named up front: **operability** (C1's gate), **coverage** (C2's entry), and the **verification surface**
(the instruments and their cross-lane duplications), which is where four of the six findings land.

---

## F1 — C1 rev leg: the CHALLENGE guard is keyed to a path *spelling*, not to the capture

**Contradiction stated plainly.** The frozen sentence restricts the rev leg to "a rev record whose path is
`corpus/captures/<24 hex>.txt`", and named limit (d) presents "a rev record whose path is not under
`corpus/captures/`" as the unchecked class. But the REV leg resolves the blob with `git cat-file` on the record's
literal path, and git accepts spellings that `CAP_RE.fullmatch` rejects. Two are admitted **OK, exit 0** at F:

| record | verdict |
|---|---|
| `path=corpus/captures/b90988847e704a08aabc8321.txt` (guarded) | `FAIL CHALLENGE`, exit 1 |
| `path=./corpus/captures/b90988847e704a08aabc8321.txt` | **`OK`**, exit 0 |
| `path=corpus/captures/b90988847e704a08aabc8321.raw` | **`OK`**, exit 0 |

All three name the same S234 "Client Challenge" blob; the record bodies are identical except the path token
(`R99ConnectorSiblings-c1-path-bypass.txt`, "record bodies"). Note the `.raw` twin is the lane's own served-bytes
store (`tools/capture-fetch.py:11`), 3038 B of HTML against the 267 B text extract — the more natural thing to cite
in a rev record, and the one no battery leg produces.

This is the round-98 defect one layer down: P0 extended the check from url/admit to rev at all, precisely because
"a rev record citing S230's blob passed". The extension is still spelling-scoped.

**Second-order effect (why a naive fix will not close it).** `is_challenge` on the `.raw` HTML returns **False**
because the HTML is 230 whitespace tokens (over the 200-word cap); the `.txt` twin is 37 tokens and returns True.
So adding `(txt|raw)` to the regex still admits the `.raw` record. A repair must resolve the *key* to its `.txt`
capture form (or strip tags) before applying the predicate.

**Affected axis.** operability (C1). No coverage or calibration effect.

**Proposed move (part of the one bounded move below).** Normalise the record path with `os.path.normpath`, match
`corpus/captures/<24 hex>.(txt|raw)`, and — for `.raw` — run `is_challenge` on the sibling `<key>.txt` bytes at the
same rev. Assert the blob's `sha256` against the capture key's refetch `txt_sha256` (already in
`corpus/evidence/round57/refetch.tsv`) so an arbitrary blob cannot be smuggled through the key form.

**Risks.** (i) `normpath` also unifies `corpus/captures/../captures/<key>.txt`, which git *rejects* today — accepting
more spellings in the guard is harmless only if REV still refuses them, so test both directions. (ii) A rev record
may legitimately cite a `.raw` for a *non*-challenge capture; the `.txt` twin check must not require the `.raw`
bytes to equal the `.txt` bytes (they do not). (iii) If `<key>.txt` is missing in the record's rev, the check must
fail closed with a named code, not silently pass.

**Verification.** Re-run the battery; add three NEG legs (dot-slash `.txt`, `.raw`, and a 254-word "Error 1020"
wall) plus one POS leg (a `.raw` of a non-challenge capture); a red tool that matches the literal path only must
fail the extended battery. Expect `NEG_REFUSED=10/10` and unchanged `HARM_SAME=25/25`.

---

## F2 — two interstitial classifiers in one lane, with divergent vocabularies and verdicts

`tools/gate-records.py` (C1) and `tools/quarantine-check.py` (round 42, still imported by
`tools/absent-split.py:46,73`) both decide "is this capture a wall", and disagree:

- marker sets: 11 vs 19; `only-gate-records` = {`a required part of this site couldn't load`, `are you a robot`,
  `cookies must be enabled`, `ddos protection`, `recaptcha`}; `only-quarantine` = 12 entries including
  `error 1020`, `access denied`, `unusual traffic`, `request blocked`, `请开启javascript`, `验证码`.
- semantics: gate-records caps at 200 words; quarantine-check scans `text[:4000].lower()` with **no** cap.
- fixture verdicts (`R99ConnectorSiblings-classifier-divergence.txt`): a 254-word Cloudflare "Error 1020 / Access
  denied" wall is **page** to gate-records and **interstitial** to quarantine-check; the class the C1 docstring
  explicitly *admits* ("a document of more than 200 words that mentions a marker (an article about CAPTCHAs)") is
  **interstitial** to quarantine-check (410 and 704-word fixtures).
- on the 100 committed `corpus/captures/*.txt` at F the two agree that nothing is quarantine-only, and gate-records
  catches **3** short walls that quarantine-check misses (`0954149536…`, `58725f5e…`, `ff9013bd…`, 18 words each).
  So neither list is a superset; the union is the safe floor and the 200-word cap is the only guard against the
  false refusals the older list already commits.

This is a duplicate instrument, not a contradiction in C1's counts: QUALITY 229 (at F, `corpus/QUALITY.md:1432-1439`)
was the routed prior rule and its four-pattern grep is subsumed by the 11 markers.

**Affected axis.** operability + verification surface (two gates can return opposite verdicts on one capture).

**Should adopt.** One shared predicate module (markers + normalisation + cap as parameters) imported by both tools;
`quarantine-check` keeps its no-cap call, `gate-records` keeps ≤200. Record in the entry/lesson which wall families
each caller covers, so "the lane refuses walls" has one answer.

---

## F3 — an http-200 wall rejection has no GATE-RECORD form at F

C1 makes a wall capture a *refusal*. The only other form, `url/unreach`, requires a failed transfer:

```
GATE-RECORD S234 url=https://…/10.1186/s41073-025-00173-z fetched=2026-11-09T04:00:33Z tier=A \
  decision=reject capture=none curl_rc=0 http=200 words=0 quote=none
  → GATE_RECORD … FAIL REFETCH   (exit 1)
```

(`R99ConnectorSiblings-c1-path-bypass.txt` §4; the `not success` conjunct at `tools/gate-records.py:284-290`, a
round-87 rule, refuses a 2xx.) So S234 — the round's own live instance, "route, not fabrication" — is expressible
in `corpus/SOURCES.md` but **not** as a GATE-RECORD: admit fails CHALLENGE, unreach fails REFETCH, and the only
passing spelling is the F1 bypass. Neither the claim nor named limits (a)-(f) mention this hole.

**Affected axis.** operability (record grammar), adjacent to C1.

**Should adopt.** kama's existing class for exactly this state: KQ45 (`kama-shokunin:corpus/QUALITY.md:322`) marks
a row whose source the check cannot reach (itself naming "a bot wall") `unverifiable-by-fetch`, "which is not
drift". A `url/wall` form (or `decision=wall` on unreach) that binds `curl_rc`/`http`/capture-key and carries no
quote would let the lane record S234 mechanically instead of leaving the state to prose.

---

## F4 — C2 covers ground tameshi already holds, with two incompatible source verdicts

tameshi `ab60e13444d83d0af58d5bdf052d8bfde21d277c`:

- `corpus/SOURCES.md:203` S327 = **the same Europe PMC core record** (pmid 26528420, doi 10.7717/peerj.1364,
  abstractText **byte-identical, len 1459** to chousa's S236 capture — verified in
  `R99ConnectorSiblings-crosslane.txt`), graded **tier A**, status `mined`.
- `corpus/SOURCES.md:204` S328 = **the same Mogull PLoS One URL** (`10.1371/journal.pone.0184727`), graded tier A,
  status **`rejected`** with a stated flip: "a lane claim that reports a pointer-error rate across records, where
  the per-pointer vs per-record denominator matters".
- `corpus/knowledge/gate-line-pointer-recheck.md` (§2) uses that abstract as its ground and records the S328 reject.

chousa at F: S236 is **tier B** (`corpus/SOURCES.md:248`) under chousa's own carrier rule (consistent with its
round-98 `press-2015-statement-questions-r98.md`), and S233 is **admitted tier A** (`:245`). Round 99 names
neither tameshi nor S327/S328 (`git grep … ; rc=1`, receipt). So the fleet now holds:

1. **two tier grades for one carrier class** — an Europe PMC REST `resultType=core` abstract — A in tameshi, B in
   chousa (chousa is internally consistent; the outlier is tameshi's A);
2. **two verdicts on one URL** — Mogull admitted (chousa S233, tier A) and rejected (tameshi S328, tier A) on the
   same day-ish (tameshi opened 2026-11-08; chousa 2026-11-09). Chousa's question ("how the rate is counted") is
   not tameshi's ("the lane reports no rate"), and chousa's S233 teaches-cell values the definitions, so the
   disagreement is substantive — but it is unrecorded on either side.

**Affected axis.** coverage (C2) and verification surface (source verdicts are not portable).

**Should adopt.** chousa's S236/S233 rows should cite the cross-lane verdicts (a `supersedes`/`used-by`-style note
naming tameshi S327/S328 and tameshi's flip), and the fleet needs one tier rule for index-record abstracts, or a
recorded ruling that lanes may grade them differently. Do **not** absorb tameshi's S327 into chousa's registry
(the two captures are different bytes with different provenance receipts).

---

## F5 — C2 decision row 3: the Do cell's parenthetical is not in its warrants (K5 candidate, reviewer-judged)

Row 3 (`R99ConnectorSiblings-c2-k5-candidate.txt`): Do = "record it as a source error, kept apart from a content
error **(the cited source was not read)**; indirect references were less than one sixth…", warrants **G6, J4**.
G6 defines source errors as "secondary (or indirect) citations"; J4 gives the one-sixth share. Neither says the
cited source was not read. The capture does contain nearby support — "authors … did not trace the statements
further and analyze for accuracy" and "authors are not reading … prior research" — but that support is a different
paragraph and is not one of the row's warrant quotes, which is precisely K5's test. I do not rule on K5; the row is
flagged with its evidence for `R99ReviewerC2` / `R99CriticClaims`.

Everything else in the table re-derives: 6 numbers in Do cells (28, 25.4%, 11,9%, 14.5%, 6.7%, 64.8%), each printed
in its row's own warrant quote(s); J2's "11,9%" is genuinely what the record serves (verified against
`abstractText`), so the entry's "(as printed)" is honest.

---

## F6 — the machine form does not carry the freeze hash

`claims.md` says "Machine form: `claims.json`", but `claims.json` `freeze.F` is a prose pointer ("recorded in
`plans/round-99.md`"), and the hash lives only in the human plan. Round 98's routed defect 1 was the *placeholder*
in `claims.json`; the r99 fix removes the hash from the machine form rather than recording it there in a later
commit. A tool reading `claims.json` cannot name F. Affected surface: verification (machine-readable claims).
Cheapest repair: the carrier commit after F writes `"F": "d41f4cd8…"` into `claims.json` as it already writes the
plan's `## Freeze`.

---

## Cross-lane match table

### (a) rules/tools that refuse challenge or interstitial pages, and their false-refusal handling

| path | rev | one-line relevance | chousa C1 |
|---|---|---|---|
| `chousa-shokunin:tools/quarantine-check.py:123-139` (`INTERSTITIAL_MARKERS`, `capture_kind`) | `f8f480f` (last changed `e0f4895c`) | 19 markers, first 4000 chars, no word cap; still imported by `tools/absent-split.py` | **duplicates** F2; its false-refusal-prone design is what C1's 200-word cap avoids, and C1 drops 12 of its wall families |
| `chousa-shokunin:corpus/QUALITY.md:1432-1439` (criterion 229) | F | the routed prior rule: 4-pattern grep over `capture=` targets, "a lexical floor", gate rule "routed to round 99" | C1 **implements** it; 229's grep is now the weaker of two lane rules — 229's check should defer to the tool |
| `chousa-shokunin:corpus/QUALITY.md:510-517` (criterion 59) | F | names "an interstitial" as a capture *form* that must be recorded before a class is used | **should adopt** as the prose counterpart: S234's row names the wall form, so the missing GATE-RECORD form (F3) is the machine gap |
| `kotodama-shokunin:corpus/QUALITY.md:37` (criterion 10) + `tools/check-source-access.py` | `5fa04a9` | a row reached past an access control counts unopened; "a challenge met and then routed around by an ordinary copy … is not a bypass"; controls `wayback-after-challenge` (0 findings) and `captcha-in-teaches` (flags) | **should adopt** the ordinary-route language and the red/green pair: chousa C1 has no recorded statement of what a *legitimately routed-around* source looks like, so the false-refusal boundary (limit b) rests only on the word cap |
| `kotodama-shokunin:corpus/QUALITY.md:66-72` (criterion 22) | `5fa04a9` | wall/captcha records bind each UA to the response it got; a bypassed block is VOID whatever the status lines say | **should adopt** for wall records: chousa's refetch row records rc/http/key but no UA, so "http 200 was actually the wall" is not re-derivable from the record |
| `kama-shokunin:corpus/QUALITY.md:322` (KQ45) | `65d0271` | bot-wall row → `unverifiable-by-fetch`, "which is not drift" | **should adopt** as F3's record state |
| `kagi-shokunin` round-55/56 `capture/rejections/*`, `corpus/lessons/round-56.md` M56-1 | `a947a42` | wall bodies kept *outside* the manifest, and a `misplaced-receipt` mistake recorded when an assertion about one URL was receipted on a sibling | **contrast**: chousa keeps the wall inside `corpus/captures/` next to documents, so the namespace is partitioned by a lexical predicate only — the structural reason F1's spellings matter |
| `tabi-shokunin` round-18/50 rejections (`cloudflare "Just a moment"` → read via Wayback/API) | `020ce05` | the fleet's usual pattern: record the wall, read the document by an ordinary route, never quote the wall | **contrast**: C1's refusal is stricter than the fleet's read-through-route practice, which is defensible; but it makes the read-through-route capture the only admissible evidence, so the `.txt` twin matters |

### (b) citation/quotation accuracy, claim-vs-source support, index-record reading

| path | rev | one-line relevance | chousa C2 |
|---|---|---|---|
| `tameshi-shokunin:corpus/SOURCES.md:203-204`, `corpus/knowledge/gate-line-pointer-recheck.md` | `ab60e13` | same Jergas/Baethge abstract (tier A) and same Mogull URL (rejected, flip stated); "a pointer is a separate claim from the quote" | **duplicates** the source, **contradicts** on tier and on the Mogull verdict (F4); its flip condition is what chousa should cite |
| `tabi-shokunin:corpus/knowledge/committed-bytes-verification-round-42.md:40-42`, `environment-injection-measurement-integrity-round-41.md:73-83` | `020ce05` | quotes are "verbatim substrings of a committed staged copy"; a spliced two-fragment quote is an errata with a superseding row (S146→S148) | **should adopt** the byte-exact standard as a lint beside C2's normalisation: `gate-records` normalises curly quotes and whitespace, so a C2 quote that differs from the page's typography still passes — the entry discloses this, but nothing can catch a *reconstructed* quote that only normalisation makes equal |
| `kama-shokunin:corpus/QUALITY.md:322` (KQ45) | `65d0271` | byte-exact quote at the cited anchor; drops/markup-shift = defect; the quoted cell is never edited, only superseded | **should adopt** for C2's decision rows: the table's paraphrase layer (K5, F5) has no anchor cell, so a wrong paraphrase has no superseding row — a `warrant` cell naming qid + capture line would make F5 machine-visible |
| `kotodama-shokunin:corpus/knowledge/civilizations/mesopotamia-sumer-akkad.md:25,189` | `5fa04a9` | a repository record "is metadata/abstract only" and claims are re-checked against a document that cites the same tablets | **duplicates (method)**: the index-record reading with a declared scope limit is exactly C2's S236 tier-B move |
| `revenger-shokunin:corpus/knowledge/round-73-re-resource-atlas.md` (S371/S373/S378 rows) | `654d092` | a per-row "abstract only" disclosure column that bounds what each source may be used for | **should adopt** the column idea: C2's limits are prose; a per-quote "field/scope" column would have made S236's abstract-only scope machine-checkable |

---

## One bounded proposal

**Give the lane one interstitial predicate, keyed by capture key rather than by record spelling.** Concretely:
(a) normalise the rev record path and match `corpus/captures/<24 hex>.(txt|raw)`; (b) for `.raw`, run the predicate
on the sibling `<key>.txt` at the same rev and bind the blob to the refetch `txt_sha256`; (c) move
`CHALLENGE_MARKERS`/`is_challenge` into one module that `tools/quarantine-check.py` imports with its own
(no-cap, first-4000-chars) parameters and its own 19-marker extension, so the union has one owner and one
documented false-refusal boundary.

Axis effect: closes F1 and F2 (operability) with no coverage change; keeps every current verdict on the 100
committed captures and the 25 HARM files (that identity is the acceptance test, not an assumption). It also makes
F3's gap visible rather than papered over by the bypass.

---

## What I did not do

No production edits; no lane/fleet git or jj mutation; no commits; no `task` tool or subagents; no network; no
writes outside this `w1/` directory and `/fast/scratch/hyaku/chousa-r99/R99ConnectorSiblings/` (scratch removed
before yield). The `.raw`/dot-slash records were written only inside the scratch clone, never into a lane.

VERDICT: R99ConnectorSiblings C1 held — the frozen counts reproduce exactly at F (7/7, 4/4, 4/4, 25/25, 5/5; base 0/7, FAIL), but the rev-leg CHALLENGE guard is keyed to the literal path spelling and admits the same S234 blob as `./corpus/captures/<key>.txt` and `corpus/captures/<key>.raw` (OK, exit 0), a reach that named limit (d) presents as "not under corpus/captures".
VERDICT: R99ConnectorSiblings C2 held — every stated count re-derives (base phrase absence 0/0, 23 quotes, 6 sourced numbers), but tameshi already holds the byte-identical abstract as tier A and rejected the identical Mogull URL one day earlier, and chousa's round-99 files name neither.
