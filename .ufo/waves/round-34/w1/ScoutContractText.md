# ScoutContractText — span-length wording that a C1 landing would stale

Read-only census, 2026-10-23. Question: every lane text that states or implies the span-length behaviour of `verify-claims` / `tok_span_at` / `tok_span_all` and would need a wording change if spans of 32768..65536 bytes become verifiable. No gate run, no counter run, no edits outside this file.

Searches (tool `grep`, lane tree, then narrowed off `.ufo/`): `argv limit`, `32 KiB or more`, `cannot be located`, `very long lines`, `per-character cost`, `Argument list too long`, `MAX_ARG_STRLEN`, `tok_span_at`. Opened the hits below. Fleet `AXES.md` (`/home/vgpnk/Projects/shokunin/AXES.md`) has none of those span-length phrases; it is not a lane file.

## Update these (living sentences that become false)

1. `corpus/knowledge/claim-record-fields-r33.md:79-80` (opened 2026-10-23). One sentence, the Limits bullet:
   > spans of 32 KiB or more cannot be located at all (`tok_span_at` argv limit, base too).
   The preceding clause on the same lines ("`json_unescape` still walks read field values byte by byte") is the reader-cost limit, not the matcher. A C1 landing falsifies only the "cannot be located" clause. Leave the byte-walk clause unless that walk is also removed.

2. `corpus/lessons/round-33.md:68-69` (opened 2026-10-23):
   > Spans of 32 KiB or more cannot be located (`tok_span_at` argv limit; base too, ProbeLongLines33 F1).
   Same assertion, lesson copy. The rest of that bullet (raw control bytes, nested member grammar, escaped keys) is not span length.

3. `SCORECARD.md:1902-1906` (opened 2026-10-23). Heading `## Planned — round 34 (not started)` then:
   > spans of 32 KiB or more (`tok_span_at` argv limit)
   This is the only SCORECARD hit for that phrase (the r20 rows at `:1041-1049` record the grep-PCRE rewrite as a past 8 MiB stall fix; they stay historical). A landing replaces "not started" the way prior planned sections were replaced; the argv-limit candidate stops being an open plan.

## Cited by the frozen claim, but not the argv miss

4. `corpus/README.md:996`, inside the Round 33 paragraph under `## Round32 frontier disposition` (the file's `## Frontier` is at `:348` and does not mention span length). Opened 2026-10-23:
   > and the per-character cost of the bash reader on very long lines.
   That names reader cost, the same split as the knowledge note's byte-walk clause. It does not say a long span fails to match. `corpus/evidence/round34/claims.md:27-29` points at this phrase as the frontier carrier, but closing C1 does not make `:996` false. Do not delete it on a matcher-only landing. `LOG.md:1262-1263` ("quadratic cost on long members (64 KiB unread member") is the same cost repair, already recorded as done, and is not a span-matcher ceiling.

## State the failure; do not amend (frozen design v1)

Kill rule in `claims.md:61-63`: counter, TOTAL and P1 are never amended after a candidate is scored. These describe the base defect as the claim's before-state. They stay true as history if the landing matches them.

5. `corpus/evidence/round34/claims.md:21-24` (opened 2026-10-23):
   > A span of 32768 bytes or more makes that string longer than the kernel's single-argument limit
   Also `:27-29` (the README/SCORECARD pointers above), `:35-43` (the contract those lengths must then meet), `:85` ("Spans above 65536 bytes" stay not claimed — that sentence must survive a 32768..65536 fix).

6. `corpus/evidence/round34/c1-count.py:11-14` (opened 2026-10-23):
   > a span of 32768 bytes or more fails with "Argument list too long"
   Line 2 is the goal ("verifies spans of 32 KiB and more"), not a ceiling.

## Mechanism comment — stale only if the `\xHH` argv pattern goes away

7. `tools/research-gate.sh:1561-1562`, inside `tok_span_at` (`:1553-1579`). Opened 2026-10-23:
   > Hex escapes keep the PCRE pattern byte-exact and literal.
   `tok_span_all` (`:1582-1607`) has no length sentence; it builds the same `regex+="\\x$hex"` and the same `grep -a -z -b -o -P -- "$regex"` (`:1593`, `:1605`). The header and `usage()` never say that pattern can exceed one argv string. If the landed matcher still builds one `\xHH` pattern, this comment stays. If it stops (the frozen note at `claims.md:92-94` says a long literal PCRE is not a fix either), `:1561-1562` needs a rewrite. No other comment in `research-gate.sh` states an argv ceiling (the only other "long lines" hit is `:2910`, a CR-strip note in the metadata reader, not `tok_span_*`).

## Checked; no span-length ceiling, so no corrective edit

These say the boundary rule with no length exception. They already match the post-fix contract (verbatim, token-bounded). They do not say long spans fail.

- Gate header `tools/research-gate.sh:46-94` (claims mode) and `:269-287` (token boundaries). `:72-74` and `usage` `:391-392` are the 8 MiB **source-file** cap (`SOURCE_READ_MAX_BYTES`), not a span cap. A 64 KiB span sits under that cap.
- `usage()` `:362-377` and `:399-403`: "Spans must appear verbatim in sources at token boundaries" (`:376-377`); multi-line outer-edge rule at `:403`. No length.
- `SKILL.md:78` registry row for `research-gate verify-claims`: exits, selftest case list, boundary. No length. `SKILL.md:130-136`: "matches each `span` as a byte-exact occurrence". No length. (`:83` is the metadata-row range named by repair E3; it is not span-length text.)
- `corpus/knowledge/claim-verification-r2.md:84-87`: a CLEAN run means the span's literal bytes occur. No length.
- `corpus/knowledge/line-binding-r31.md:9` and Limits `:42`: line binding, not span length. `:42` does not name a size.
- `corpus/knowledge/anchor-boundaries-r4.md:122-136`: residual limits are token-aligned shortening and non-ASCII edges, not argv.
- `corpus/knowledge/reader-allocation-r26.md:21`: "long lines" as a metadata-reader test shape, not `tok_span_at`.
- `corpus/fixtures/claims-r2.README.md:108` and `:110`: "long span" means a long archive sentence, not 32 KiB.
- `LOG.md:745-760`: historical record that r20 switched `tok_span_at` to `\xNN` plus `grep -P`. True of that revision; not a living "cannot locate" claim.
- `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/lessons/round-33-verifier-spotcheck.md`, `PROVINCE.md`, lane `README.md`: no `argv limit` / `32 KiB or more` / `cannot be located` hit.
- `.ufo/` wave reports name `tok_span_at` from past rounds. They are historical receipts, not living contract text, and were not treated as update targets.

## Verdict

Three living sentences become false if 32768..65536 spans verify: `claim-record-fields-r33.md:79-80`, `lessons/round-33.md:68-69`, `SCORECARD.md:1905-1906` (with the `:1902` "not started" heading). `corpus/README.md:996` is the long-line **cost** item the frozen claim cites; it is not the argv miss and should stay unless the byte-walk is removed too. Frozen `claims.md` and `c1-count.py` document the base failure and must not be amended. Gate header, `usage()`, and the SKILL registry row do not state a span-length ceiling.

Confidence: high on the three living hits and the negatives (those files were opened or the phrase search returned no hit). Unresolved: whether a landing also drops the `json_unescape` byte-walk (that decides `:996` and the first clause of `:79`). Not run: no candidate gate, so this is a wording census, not a measurement that long spans already verify.
