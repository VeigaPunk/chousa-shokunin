ATTACKS: C1 lexical negator lists (IMPLICIT_NEG, UN_NEG_RE) and the is_neg-driven polarity logic
VERDICT: defect — C1==operability holds exactly (C1=PASS on pinned fixtures), but the negator list/regex over-tag, so the probe can ACCEPT a real flip (negator-count masking) and REFUSE a correct bullet. Claim language "no rule widened toward acceptance of a flip" is therefore stronger than the implementation.

Method: I inspected tools/inference-ground.py (#9812) rules 2-6 and lines 232-338 (NEG_WORDS, IMPLICIT_NEG, UN_NEG_RE, is_neg, occurrence_polarity, phrase_polarity, polarity_flips) and ran three probes under /tmp/chousa-r47w2-L1Chousa47.RevC1Regex/ plus the frozen counter. No tools installed (no installs needed). No rate fetches.

1. UN_NEG_RE sweep over every distinct lowercase word of corpus/knowledge/*.md (63 files):
   `python3 - <<'EOF'` with the file's regex: 60 distinct matches, all LEXICALLY genuine un-negations (unaffected, unanchored, unanswerable, unasserted, unavailable, unbalanced, uncapped, unchanged(79), unchecked, unclaimed, unclosed, uncommitted, uncomputable, uncovered, undated, undecidable, undeclared, unexercised, unexpected, unfenced, unfilled, unfixable, unfixed, unlabeled, unlocked, unmapped, unmarked, unmasked, unmeasurable, unmeasured, unmoved, unmutated, unnamed, unobservable, unobserved, unopenable, unopened, unparseable, unparsed, unpredictable, unprivileged, unquoted, unreachable, unreadable, unreconciled, unresolvable, unresolved(84), unscanned, unscheduled, unscored, unsourced, unsupported(30), unterminated, untouched, untrusted, unvalidated, unverifiable, unverified, unwalkable).
   - LATENT regex false positives (positive-valence words that MATCH UN_NEG_RE, absent from knowledge corpus today): `unified`, `unpacked`, `unveiled`, `unfolded`, `unwrapped` (verified by direct match: `unified True, unpacked True, unveiled True, unfolded True, unwrapped True`; `united False` via the `it` lookahead). These would fire as negators if they appear in any production span/bullet.
   - The defect is not the list membership but the USE: most matches are attributive adjectives (`unverified claim`, `unsupported value`, `unchecked flag`, `unterminated string`, `unchanged data`). occurrence_polarity (line 283-287) treats a negator INSIDE the phrase token or among the 3 preceding span words as negating the entity phrase's existence, so a phrase like `unverified records` always reads as NEGATED even when the span asserts the records exist.

2. IMPLICIT_NEG words used non-negatively in corpus:
   - `free` (9 uses): "gate-free python" (compound affix), "S078 is the next free lane id" / "S079 is the next free lane id" / "next free ids" (search-log-method-r39.md:27, citation-version-binding-r36.md:28, citation-version-binding-r37.md:30) — "free" = "available", not a negation.
   - `fail`/`fails`/`failed` (81/31/15): mostly verbal technical "fails closed" (negation-compatible), but nominal/adjectival non-clause uses exist: "first long record only | fail | **fail**" (per-record-argv-attribution-r36.md:49, status label), "claims-fail-stray-marker" / "chain-fail-external" / "integrity-fail-dangling-source" (identifier components), "FAIL (2/136)" / "observed=unsupported" result labels, "an always-fail witness" (attributive).
   - `missing`/`absent` (108/147): frequent as count/label tokens ("anchor-missing=0", "absent=0", "baseline missing/unreadable/malformed") describing record states, not clause negations; "missing X" / "absent X" preceding a noun phrase attaches privatively to the noun (the entity still exists).
   - `nothing` is listed in BOTH NEG_WORDS and IMPLICIT_NEG (harmless redundancy).

3. Mechanistic demos (all run at tip 1fc5ed193; verbatim decisive output):
   A. ACCEPT-mask (real flip accepted). Span file: `S078 is the next free lane id`; bullet: `- `lane id` is not assignable to S078 (S999)`.
      Output: `GROUND entry=accept.md section=1 bullets=1 tokens=1 grounded=1` / `GROUND: PASS` / `exit=0`.
      The bullet denies an entity the span affirms; the false negator `free` in the 3 span words before `lane id` makes the phrase read as NEGATED, so P2 never fires.
   B. Control (same bullet, clean span `S078 is the next lane id`): output `FINDING INF_POLARITY_FLIP bullet=1 token='lane id / lane'` / `GROUND: FAIL` / `exit=1`. Proves `free` is the causal mask.
   C. REFUSE (correct bullet refused). Span file: `S999: archives keep unverified records`; bullet: `- archives keep `unverified records`; each record is filed anyway (S999)`.
      Output: `FINDING INF_POLARITY_FLIP bullet=1 token='unverified records / record'` / `GROUND: FAIL` / `exit=1`.
      The bullet truthfully affirms the span (records are kept, unverified); the in-token attributive `unverified` negates the phrase, so the bullet's bare `record` is flagged as a P1 flip.
   D. Frozen counter (read-only run): `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS` / `exit=0`.

Residual risk: the demos are minimal 1-bullet manifests under /tmp (not lane fixtures) — they exercise the exact code paths (grounding_tokens → span_texts → phrase_polarity → polarity_flips). The same mechanism applies to `lacks`/`absent`/`missing` and any UN_NEG_RE attributive. No claim wording change proposed; this is a calibration/name-limit finding, not a fixture change.

Verification gaps: none for the mechanism; the sweep counts were computed with the tool's exact regex/list (copied verbatim from source lines 251-259).
