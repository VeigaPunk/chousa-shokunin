# CritForgeC2 — attack on the C2 counter (round 49, wave 1)

Seat: CritForgeC2 (godspeed). Target: `corpus/evidence/round49/c2-count.py` (frozen).
I built scratch lane roots under `/tmp/chousa-r49-CritForgeC2/` and ran `c2-count.py --root <scratch>`
against them (counter reads lane git only for BASE_REV SOURCES; register/cache are absolute read-only).
No lane file was written; the lane's git status before/after is unchanged except siblings' own untracked files.
No tool installs (RULES.md read; nothing needed). Scratch will be deleted after this report.

## 1. Cheapest byte set that prints C2=PASS (observed)

Base root: 7 bound rows S096–S102 (documents 1–7), 2 refused docs (toho, umac).
Entries contain only `source:` lines plus one `#### Inference` bullet per entry; spans are the entire
capture `.txt` file (offset 0, digest = sha256 of that file); every span quote is a single space ` `;
each registry `anchor` cell holds one `char N` where N = position of the first space in the capture;
lesson carries two `refused-doc` lines and five self-declared `register S0xx verdict: present` lines.

```
$ python3 corpus/evidence/round49/c2-count.py --root /tmp/chousa-r49-CritForgeC2/base
ENTRIES=2/2 | BOUND=7/9 (min 7) REFUSED=2 | BOUND_IDS=S096,...,S102 | REF_ID_UNBOUND=0
| QUOTE_ROWS=14 ON_BOUND=14/14 | SPAN_IDS=7/7 | QUOTES_IN_SPAN=14/14 | QUOTES_IN_ENTRY=14/14
| QUOTES_IN_LESSON=14/14 | QUOTE_SHORT=14/14 | SPAN_CONTEXT=14/14 | CAPTURE_BOUND=14/14
| ANCHOR_BOUND=7/7 | INFERENCE_GROUNDED=2/2 | QUARANTINE_VERDICTS=5/5 (S082,S084,S086,S095,S096)
| QUARANTINE_BLOCKED_ADOPTED=0 | C2=PASS  (exit 0)
```

What this means (all 18 legs passed):

- **Quotes**: a single space is a valid quote (substring of span/entry/lesson; 0 words ≤ 25; 1 char ≤ 160).
  Nothing requires a quote to be a word, let alone evidence. The counter's `QUOTES_IN_*` legs are pure
  substring checks.
- **Spans**: the whole capture text form as one span passes `CAPTURE_BOUND` (slice equality at offset 0,
  file digest matches). The intended ±80-char context is not enforced; no semantic bound exists.
- **Anchors**: one `char N` computed from the same scan always passes (`ANCHOR_BOUND`). It is a
  self-consistent pointer to wherever the (empty) quote sits — boilerplate, footer, nav all fine.
- **Inference** (`tools/inference-ground.py`, run by the counter): a bullet that **asserts nothing** —
  `- 2026 (S096, S097, S098, S099, S100).` — passes: one grounding token (numeral ≥ 3 digits) present in
  any cited span. Numerals bypass the polarity machinery entirely. `INF_SECTION_ABSENT` / `INF_UNCITED` /
  `INF_UNGROUNDED` / `INF_TOKEN_NOT_IN_SPAN` each refuse the corresponding hollow bullet (variants below),
  but an assertion-free numeral bullet is accepted.
- **Refusal**: two docs refused with zero work: no row, no `source:` line, two lesson lines. `BOUND+REFUSED=9`
  holds with 7/7 bound.
- **Verdicts**: five lines `register S0xx verdict: present` (S082,S084,S086,S095,S096 — exactly the register
  ids on theme URLs). The counter only checks presence of a line per register id and that a bound doc's verdict
  is not `fabricated`/`unverifiable`; it never re-checks the register's payload claim.

## 2. Which leg refuses which shortcut (observed; one mutation at a time on the passing base)

| Variant (shortcut) | Observed counter output (delta) | Refusing leg |
|---|---|---|
| quote changed to `zzz` (absent from lesson/entry) | QUOTES_IN_SPAN=0/14, IN_ENTRY=0/14, IN_LESSON=0/14, ANCHOR_BOUND=0/7 | in_span/in_entry/in_lesson, anchors |
| quote = `the` on all docs (CJK docs lack it) | QUOTES_IN_SPAN=8/14, IN_ENTRY=10/14, IN_LESSON=0/14, ANCHOR_BOUND=4/7 | same three, anchors |
| span digest all-zero (`0`×64) on one row | CAPTURE_BOUND=13/14 | form_text digest match |
| span offset 7 instead of 0 (slice no longer equals file) | CAPTURE_BOUND=13/14 | exact-slice equality |
| anchor `char 999999` on one row | ANCHOR_BOUND=6/7 | char ∈ located quote offsets |
| only one span row for one id | QUOTE_ROWS=13, SPAN_IDS=6/7 | ≥ 2 rows per bound id |
| extra span row for unbound S900 | ON_BOUND=14/15, QUOTES_IN_SPAN=14/15, SPAN_CONTEXT=14/15, CAPTURE_BOUND=14/15 | on_bound==n |
| entry contains stray `S105` | REF_ID_UNBOUND=1 | every S### token in a bound id or S003 |
| opened date 2026-10-24 on one row | BOUND=6/9 (and REF_ID_UNBOUND=2) | row must equal OPENED |
| status `queued` on one row | BOUND=6/9 | row must be `mined` |
| `used-by` cell drops entry name | BOUND=6/9 | used-by must name entry |
| row id `S001` (exists at BASE_REV) | BOUND=6/9 | id must be new since BASE_REV |
| second row with same URL (S097 duplicated) | BOUND=6/9 | exactly one row per URL |
| refused doc gets a `source:` line | REFUSED=1, BOUND+REFUSED=8 | no source line for refused |
| refused doc's lesson `refused-doc` line removed | REFUSED=1 | lesson line must name URL |
| `#### Inference` section removed | INFERENCE_GROUNDED=1/2 | section must exist |
| bullet with no grounding token | INFERENCE_GROUNDED=1/2 | INF_UNGROUNDED |
| bullet citing no S-id | INFERENCE_GROUNDED=1/2 | INF_UNCITED |
| bullet token `777777` not in any cited span | INFERENCE_GROUNDED=1/2 | INF_TOKEN_NOT_IN_SPAN |
| bullet `That is no lateral reading (S100).` (negator 2 words before affirmed phrase word) | INFERENCE_GROUNDED=1/2 | INF_POLARITY_FLIP |
| verdict lines removed | QUARANTINE_VERDICTS=4/5 | verdict per register id |
| verdict `fabricated` on a bound doc (S082→NII) | QUARANTINE_BLOCKED_ADOPTED=1 | no fabricatable/unverifiable on bound |
| extra `register S999 verdict: present` line | still C2=PASS | id must be a register id (ignored otherwise) |
| span file content == quote length (`the`) | SPAN_CONTEXT=12/14, CAPTURE_BOUND=12/14 | span must be longer than quote |
| quote 500 chars / multi-line | QUOTE_ROWS=46, QUOTE_SHORT=12/46 | split/over-length rows fail |

So: the cheap-space/`the`-quote, whole-capture-span, one-scan-anchor, numeral-only inference bullets,
two-doc refusal, and self-declared `present` verdicts ALL pass; every kind of *inconsistency* (wrong digest,
wrong offset, wrong anchor, missing lesson/entry copies, off-bound rows, unbound tokens, registry row
condition failures, hollow/uncited/ungrounded inference bullets, missing or blocking verdicts) is refused.

## 3. What the closure must spot-check by hand

The counter verifies consistency between the lane bytes and the real on-disk captures, not that the lane
bytes mean anything. With the minimal PASS root the closure (and the Gate) must eyeball:

1. **Quotes are substantive**: a space or `the` or nav/footer boilerplate satisfies every quote leg. Only a
   human can tell whether the 2-per-id quotes actually support the theme statements.
2. **Inference bullets assert the claim**: `inference-ground.py` accepts a bullet that is only a numeral plus
   cites; it never checks that a bullet states the theme or says anything at all. Also check that the bullets
   relate to the *bound* rows (the counter only needs a token somewhere in a cited span).
3. **Spans are targeted**: whole-capture spans pass. The 80-char-context intent of `build-spans.py` is not
   enforced by the counter; closure should confirm quotes are inside substantive regions.
4. **Anchors point at real quote positions**: mechanically consistent, but with a space/`the` quote the
   anchor points at noise. Verify `char N` actually sits on the quoted text's start.
5. **Verdict lines are true**: `register S0xx verdict: present` is self-declared; counter re-checks nothing
   against the absent-defect register's payload evidence. Spot-check each of S082/S084/S086/S095/S096.
6. **Refused documents genuinely carried no usable text**: refusal requires no evidence at all; an adopter
   could refuse the two hardest documents to dodge work (here: toho/umac PDFs).
7. **Entry semantics**: nothing checks the entry text is coherent with the theme or its rows; any filler
   body without stray S-ids passes.

## 4. Engineering notes for the closure

- `CAPTURE_BOUND` compares the capture slice against the span file read with Python's universal-newline
  translation. For UTF-16LE `.raw` OLE forms, a span containing CRLF will fail until read back the same way
  (observed: zcmu/hit raw forms mismatch at the first `\r\n`; using the `.txt` sidecar consistently passes).
  If the real `build-spans.py` runs are meant to choose raw forms, `--check`/`c2-count` would flag them
  unless reading/writing newline modes are aligned.
- Numeric grounding tokens bypass the polarity engine entirely; an adopter can ground every bullet with a
  bare year/identifier present in the capture.
- `QUARANTINE_VERDICTS` counts only ids that appear in the register on theme URLs, so verdict lines for
  made-up ids are silently ignored (PASS preserved).

VERDICT: Attacked the frozen C2 counter with the cheapest lane bytes; a scratch root with space-quotes,
whole-capture spans, one-scan anchors, numeral-only inference bullets, two refused docs, and self-declared
verdicts prints C2=PASS (exit 0) with zero real re-grounding, and every leg that refuses a shortcut was
individually demonstrated — the closure must hand-check quote substance, bullet assertions, anchor targets,
and register verdicts.
