# R57W1ReviewC2Same — same-sentence audit of R57-C2 (predicate vs docstring vs enforcing code)

Seat: R57W1ReviewC2Same (leaf, no subagents). Scope: the three texts of R57-C2 only; nothing mutated in the lane;
frozen counter and peers read-only. Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ReviewC2Same/` used for fixture
clones of the counter and was deleted before yield (`ls` confirms gone). No network use; no installs (python3/git/
pdftotext 26.08.0/sha256sum already present; pacman untouched).

Inputs: `corpus/evidence/round57/claims.md` (C2 section, frozen at `c2f914c5`), `corpus/evidence/round57/c2-count.py`.
Freeze integrity: `git log --oneline -- c2-count.py` shows only `c2f914c`; `git diff c2f914c..HEAD -- c2-count.py | wc -l` → `0`.
Predicate equality: extracted claims.md predicate paragraph vs docstring lines 4–26, whitespace/backtick-normalized →
`claims.md predicate == c2-count.py docstring: True` (mechanical diff, no output). So the audit is docstring↔code.

## Clause ↔ code map (claims.md wording → c2-count.py)

1. "47 distinct (id,url,capture_sha256) triples … every `corpus/evidence/**/spans.tsv` with a `capture_sha256` column"
   → `pinned_set()` L85–106 (`ls-tree` at SET_REV L87, `endswith("spans.tsv")` L90, header check L96, columns L98,
   one entry per triple L103, `SET_N` env-guard L104–105). Confirmed against live repo: counter prints `SET=47`.
2. "exactly one verdict recomputed from committed bytes" → single `verdict` per triple through branches L204–233,
   counted once L234; `VERDICTS = SET_N - MISSING` L237.
3. REPRODUCED ("capture … whose sha256 equals the raw_sha256 of the triple's last successful attempt … has the
   pinned digest itself or a `<key>.txt` beside it that has it") → L205–218: capture present L205, last-success-bytes
   equality L207 (else note+MISSING L208), `pin in (sha(raw), sha(txt)…)` L217.
4. DRIFTED ("such a capture exists and neither digest equals the pin") → L219–220; quote-absence `absent=a/m` over
   the triple's pinned quotes L221–224 (`defined_form` L135–144).
5. UNREACHABLE ("no capture, and at least two failed attempts (curl_rc != 0, or http_code outside 200-299, or an
   empty body) recorded at least 600 seconds apart") → L229–233 with `failed()` L154–159 and `when()` L147–151.
6. CONSISTENT (recipe sentence) → `recipe_txt` L120–132 (PDF+pdftotext-26.08.0-nonblank L121–128, else UTF-8/replace
   L129, html_to_text when starts-like-HTML L130–131), per-capture check L211–216, `consistent == backed` in `ok_all` L238.
7. FLAG ("`- FRESHNESS-FLAG <id> <key> absent=<a>/<m>` in corpus/lessons/round-57.md with the counter's own a and m")
   → `FLAG_RE` L62, lesson scan L188–194, match on `(absent, m)` L227, `flagged == need_flag` L238.
8. "counted `SET=47 VERDICTS=47/47 CONSISTENT=b/b FLAGGED=g/g` with REPRODUCED >= 5 and BYTE_BACKED (REPRODUCED +
   DRIFTED) >= 32, printed `C2=PASS`" → print L240–242; `MIN_REPRODUCED = 5` L60, `MIN_BYTE_BACKED = 32` L61,
   enforced L238–239; BYTE_BACKED is structurally REPRODUCED+DRIFTED (both verdicts assigned only inside the
   `backed` branch L210/218/220).

## Findings (drift named, reported, not patched — claim is frozen)

- **D1 (code stricter than predicate, minor).** The CONSISTENT check adds a ledger binding absent from the predicate
  sentence: L213 requires `ok[-1]["txt_sha256"] == sha(txt)` in addition to "its `.txt` equals the frozen campaign
  recipe applied to its `.raw`". A capture whose `.txt` is exactly `recipe_txt(raw)` but whose refetch row records a
  different txt_sha256 is predicate-CONSISTENT but code-inconsistent. Fixture evidence (47-triple scratch repo, T4):
  `SET=47 … CONSISTENT=43/44 … C2=FAIL` where only the ledger txt_sha256 differed.
- **D2 (code laxer than predicate, minor, cosmetic).** `FLAG_RE` L62 ends in `\s*$`, so lines with trailing whitespace
  — outside the exact format `- FRESHNESS-FLAG S### <24hex> absent=a/m` — are accepted. Fixture T2: flag line with a
  trailing space still yields `FLAGGED=1/1`. Unit checks: exact format matches; `S02`/`S0022`/uppercase key/23-hex
  key/`absent=1 /2`/double space all correctly rejected. Related: duplicate flag lines for one (id,key) are
  last-wins (dict overwrite L189–194), so a lesson carrying a wrong flag line above the correct one passes (T3:
  `FLAGGED=1/1`); the predicate says "the line" (singular).
- **D3 (both texts silent, fails safe).** States the predicate never names get verdict `MISSING` (L195, L204–208,
  L229–233 else-branch): a store capture matching no ledger success digest (or none exists), or <2 failures, or
  failures <600s apart. "The lane holds exactly one verdict" is then operationalized as "not MISSING"; `VERDICTS<47`
  still forces `C2=FAIL`, so the claim fails safe, but the sentence itself covers only 3 of the 4 emitted verdicts.
  Fixture T1 evidence: `VERDICTS=45/47 REPRODUCED=43 DRIFTED=1 UNREACHABLE=1 … C2=FAIL` with the two induced MISSING.
- **D4 (latent order-dependence, inactive under the tool).** "Last successful attempt" is resolved as the last
  successful row in ledger FILE ORDER (`ok[-1]` L203), not by `max(fetched_utc)`. Fixture T5: with S006's rows written
  out of chronological order the code prints `CAPTURE S006 … REPRODUCED` although the chronologically-last success
  has different bytes. Inactive: `tools/capture-fetch.py` L111–115 appends rows in execution order (sequential
  attempts). Related edge: `when()` drops malformed `fetched_utc` from the UNREACHABLE spacing math (L147–151, L230).

## Attacked and survived (checks 2–7 of the item, fixture-verified)

- **(2) FLAG_RE** enforces the exact format on every structural element (T6 table above); only trailing whitespace
  slips (D2).
- **(3) UNREACHABLE rule** — `failed()` is exactly the predicate's three conditions (rc≠0; http outside 200–299 with
  unparseable→0; `raw_sha256 == "-"` ⇔ empty/absent body, since capture-fetch.py L137–143 only records a success with
  non-empty body): all six unit cases pass. Spacing: code tests `(max−min) ≥ 600s` over failed timestamps; this is
  logically equivalent to "∃ two failed attempts ≥600s apart" (the max/min pair is such a pair), so no drift.
  Boundary in T1: exactly 600s → `UNREACHABLE`, 599s → not. Live S105: fails 08:06:12/08:30:12/08:33:48 → pairs
  1440s/1656s/216s, ∃≥600 → both texts agree.
- **(4) REPRODUCED** accepts `pin == sha(raw)` OR `pin == sha(txt)` exactly as worded: T1 triple with txt-only pin
  reproduces; T7 triple with no `.txt` at all and `pin == sha(raw)` reproduces (`REPRODUCED` accepted; it then cannot
  be CONSISTENT, which both texts agree on since no `.txt` can equal the recipe).
- **(5) CONSISTENT** covers every byte-backed capture: `consistent == backed` gates `ok_all` (L238) and the recipe is
  the campaign's verbatim — counter `html_to_text` L111–117 is character-identical to shokuknow
  `.ufo/waves/corpus-expansion-1/quote-lint.py` L515–522, and that file's sha256 is exactly the frozen citation
  `e864a01f…b958`; `capture-fetch.py` `recipe_txt` L78–92 is identical to the counter's. pdftotext preflight pins
  26.08.0 (L56, L168–170; host reports `pdftotext version 26.08.0`). Modulo the extra ledger binding (D1).
- **(6) printed summary** carries every counted element: `SET=47 VERDICTS=47/47 REPRODUCED=… DRIFTED=… UNREACHABLE=…
  BYTE_BACKED=… CONSISTENT=b/b FLAGGED=g/g C2=PASS` (L240–242). DRIFTED/UNREACHABLE fields are a superset of the
  counted sentence but the line format is identical to `controls/c2-before.txt`'s format (field-by-field check), so
  the kill rule's "any other line" is unaffected.
- **(7) thresholds** `MIN_REPRODUCED=5` (L60) and `MIN_BYTE_BACKED=32` (L61) are enforced in `ok_all` (L238–239);
  T1-style fixtures with lowered counts would flip C2 (indirectly evidenced by VERDICTS gating).
- **(1) vice versa** — code elements with no predicate clause: the D1 ledger binding, MISSING/VERDICTS
  operationalization (D3), preflights (`SET_N` guard L104–105, pdftotext L168–170, `REFETCH_HEADER` notice L181–182
  which prints and continues), and the two extra printed counts. All are mechanical/strengthening except D1–D3 above.

## Live-state observation (measurement, not a predicate change)

`python3 corpus/evidence/round57/c2-count.py` at lane tip now prints:
`SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS`
(exit 0) — attempt-2 rows landed for S100/S103/S106 (all REPRODUCED) and S105 failed 3× → UNREACHABLE; the five
DRIFTED carry `absent=0/2,0/2,0/6,0/9,0/6` (S083/S087/S113/S114/S121), so no FRESHNESS-FLAG lines are owed and the
absent `corpus/lessons/round-57.md` is consistent with `FLAGGED=0/0`. C3-originated ledger rows (S131–S135) are
outside the pinned 47 and are ignored by construction (`mine` filter L201).

## Residual risk / verification gaps

- The OLE/zip `defined_form` branch (L137–141 via `tools/capture-text.py`) is untested by live data this round (all
  five DRIFTED are HTML/JSON) and by my stub fixture; quote-absence for a drifted OLE capture rests on
  `capture-text.py` stdout conventions (line-ending normalization in particular).
- D1/D2/D4 are dormant under tool-written ledgers/lessons; they bite only on hand-repaired artifacts.
- I did not re-verify the 47 pin digests against SET_REV manifests independently; `pinned_set`'s `SET_N==47` guard
  and the REPRODUCED digest matches are the binding checks and both ran.

VERDICT: attacked the three-text conformance of R57-C2 (claims.md predicate = docstring = enforcing code); the claim
survives — predicate and docstring are mechanically identical, every clause has enforcing code, checks (2)–(7) hold
under fixture attack — with four named drifts reported not patched: D1 code-stricter CONSISTENT ledger binding
(L213), D2 FLAG_RE trailing-whitespace/duplicate-flag laxity (L62, L189–194), D3 unnamed MISSING verdict states
(L204–208/L229–233), D4 file-order "last successful attempt" (L203, inactive under capture-fetch.py).
