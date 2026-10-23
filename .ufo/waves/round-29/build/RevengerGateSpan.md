# RevengerGateSpan — gate span semantics vs frozen quote-reopen contract (round 29, wave 1)

Seat: ChousaR29.RevengerGateSpan, revenger, read-only. Date of work: 2026-10-22/23 session.
Scope: reverse-engineer `tools/research-gate.sh` span-matching semantics and compare point by
point with the frozen C1 contract in `corpus/evidence/round29/claims.md`. No frozen file was
edited; the gate selftest was NOT run (per assignment); no network was used (zero GETs); no
tool installs were made (nothing to record under the 2026-10-19 tooling directive).

Frozen artifacts read (all paths relative to the lane root):

- `tools/research-gate.sh` sha256 `ac1315ddaa12e79b68069d1a9866b9b1b55e3a43efef3ba0cb5ca5e665835765` (current working tree; lane HEAD `8026fe6`).
- `corpus/evidence/round29/claims.md` (design v2, frozen contract), `corpus/evidence/round29/c1-count.py` sha256 `574ffcad7a78d2fdf04b895445c1aac72537cc548b944cae62012baf4ba4e2dd`.
- `corpus/fixtures/quote-reopen-r29/items.tsv` sha256 `e6305beba9563fe4d37430019831610ddf7a5adf1e35de60869e3b764f939bcc` (read to confirm truncated-token cut positions).
- `corpus/knowledge/claim-verification-r2.md`, `corpus/knowledge/anchor-boundaries-r4.md`.

## Gate semantics (reconstructed, with line numbers)

The gate matches raw file bytes with no normalization:

- Rule statement: header `tools/research-gate.sh:232-252` — byte-exact, case-sensitive; an
  occurrence counts only when both outer edges sit at a token boundary; only the outer edges
  are checked (a multi-line span may cut mid-token inside).
- Boundary classes: `TOK_WS` = space, tab, LF, CR, VT, FF (`:1255`); `TOK_PUNCT` =
  `` !"#$%&()*+,./:;<=>?@[\]^_`{|}~ `` (`:1256`); plus file edge and line edge (`:1269`, `:1283`).
- Word character: ASCII letter, ASCII digit, or any non-ASCII character (`tok_word_char`,
  `:1258-1265`); `_` is punctuation (a boundary), `-` and `'` are excluded from `TOK_PUNCT`.
- Conditional joiners: `-`/`'` are boundaries only when they do not join two word characters
  (`tok_left_ok :1267-1279`, `tok_right_ok :1281-1293`) — `cross-check` and `workers'` are
  single tokens, so a span cut at a hyphen/apostrophe edge inside a compound misses.
- Scanner: `tok_span_at :1295-1322` — `LC_ALL=C` (`:1298`), empty span refuses (`:1302`),
  `grep -a -z -b -o -P` with hex-escaped literal bytes (`:1320`), first boundary-delimited
  occurrence wins; glued occurrences are skipped, not reported. Call sites: claims spans
  `:1403-1405`, chain quote anchors `:1573-1575`. One matcher, both modes.
- Adjacent bounds that are not span semantics: local sources over 8 MiB refused unread
  (`SOURCE_READ_MAX_BYTES :270-271`); URL sources refused unfetched (`:1150-1151`,
  `CLAIM_SOURCE_EXTERNAL`).

## New-command semantics (frozen contract)

`claims.md` "Tool contract (frozen)" + the counter's reference functions
(`c1-count.py:60-108`, which exist to make that contract executable for page-sampled labels):

- Input: live HTML (or plain text) fetched from the registry URL, decoded per Python
  `html.parser` with `convert_charrefs=True` (`:71`), `script`/`style`/`noscript`/`template`/`head`
  dropped (`SKIP :60`), exactly the listed block elements emitting one space at start and end
  (`BLOCK :61-63`), comments dropped.
- Normalization on page text and quote alike (`norm :95-96`): NFKC; U+2018/U+2019/U+201A/U+201B
  → `'` and U+201C/U+201D/U+201E/U+201F → `"` (`QMAP :64-66`); U+00AD, U+200B, U+200C, U+200D,
  U+FEFF deleted; every whitespace run to one space; ends stripped.
- Match (`found :99-108`): case-sensitive substring over normalized text; VERBATIM iff the
  character before and after the occurrence (when present) are not `str.isalnum`. No joiner
  clause; every non-alphanumeric character is a boundary. Too-long gate at 25 words precedes
  the fetch; body over 8 MiB is `UNREACHABLE`.

## Point-by-point table

| # | Rule | Gate (`research-gate.sh`) | New command (`claims.md` + `c1-count.py`) | Same? | Justified by live HTML vs local Markdown? |
|---|------|---------------------------|-------------------------------------------|-------|-------------------------------------------|
| 1 | Input medium | local file bytes, read whole (`:1403`) | fetched page rendered to text (`:69-93`) | different | Yes — the entire C1 surface (gate refuses URLs, `:1150-1151`) |
| 2 | Normalization | none; byte-exact (`:245`, `:1298`) | NFKC + quote mapping + zero-width deletion (`:95-96`, `:64-66`) | different | Yes — HTML carries entities, typographic quotes, soft hyphens; lane Markdown is authored to match |
| 3 | Case | case-sensitive (`:245`) | case-sensitive (`claims.md` Match; `:99-108`) | same | — (v2 control `casefold, no token boundary` confirms casefold must stay out) |
| 4 | Boundary class | `TOK_WS` ∪ `TOK_PUNCT` ∪ file/line edge (`:1255-1256`, `:1269`, `:1283`) | any non-`str.isalnum` character (`claims.md` Match; `:102-107`) | different in set, see 5-6 | Partly — see rows 5 and 6 |
| 5 | Non-ASCII punctuation neighbor (`—`, `“`, `。`) | word character → fails closed, span misses (`:1258-1265`) | boundary (`—`.isalnum() is false) → span hits | different | Yes — r4 named this exact false-negative class (10 of its 15 failing probes); live pages abut typographic punctuation without spaces |
| 6 | Word-internal `-`/`'` joiner | conditional boundary; a cut at a hyphen/apostrophe edge inside a compound misses (`:1267-1293`) | no joiner clause; `-`/`'` are always boundaries | different | No — design choice, not medium-forced; see Divergence A |
| 7 | Whitespace runs and line breaks | must match bytes; multi-line span needs the LF byte inside it (`:244-245`, `:1316`) | every whitespace run collapses to one space, so wrapping and indentation never block a match (`:95-96`) | different | Yes — HTML text extraction inserts block spaces and folds wrapping |
| 8 | Markup inside span | Markdown markup bytes must occur verbatim (a span crossing `*` or a hard wrap misses) | tags dropped; block elements emit one space (`:60-63`, `:69-93`) | different | Yes — tags are not reader-visible text |
| 9 | Edges checked | outer edges only (`:1314`; header `:243-245`) | outer edges only (`:104-106`) | same | — |
| 10 | No-character edge | boundary (`:1269`, `:1283`) | boundary (`i == 0` / `j == len(text)`, `:105-106`) | same | — |
| 11 | Empty span | refuses (`:1302`) | never matches (`while q:` skips, `:100-101`) | same outcome | — |
| 12 | First-delimited-occurrence scan | yes, reports `line:N` / `lines:N-M` (`:1295-1322`) | yes, verdict-only, no location (`:99-108`) | same acceptance; reporting differs | Yes — output contract is a verdict, not an anchor |
| 13 | Underscore neighbor | boundary (in `TOK_PUNCT`, `:1256`) | boundary (not alnum) | same outcome, different reason | — |
| 14 | CJK / non-ASCII letters abutting | word char → miss | alnum → miss | same | — |
| 15 | Digit-glued token (`route66 map`) | left edge mid-token → miss | alnum neighbor → ABSENT | same | — (matches repair-first D1: both rules reject digit-glued spans) |
| 16 | Oversized input | local source over 8 MiB refused unread (`:270-271`) | body over 8 MiB → `UNREACHABLE` | same cap, different disposition | Yes — refuse-vs-fail maps to local-vs-fetched failure modes |
| 17 | Contradiction marker co-occurrence | `contradicted` arm only (`:796-815` region) | no analogue (verbatim location only) | not applicable | Yes — outside C1's predicate by design (`claims.md` "Not claimed") |

## Measured differential (14-probe battery)

Harness: `/fast/scratch/hyaku/chousa-r29/w1/RevengerGateSpan/probe.py` builds one scratch
Markdown source and one JSONL claims file (each probe `expect=supported`), runs the lane gate
read-only in claims mode against the scratch root, and imports the frozen counter's `norm`/
`found` read-only to compute the new-rule verdict on the same text. Receipts copied to
`.ufo/waves/round-29/build/RevengerGateSpan/` (`probe.py`, `run-log.txt`, `gate-stdout.txt`,
`gate-stderr.txt`, `probe.md`, `probe.jsonl`).

Commands and outcomes (re-run commands, per repair-first):

- `python3 probe.py` → rc 0; gate invocation
  `bash tools/research-gate.sh verify-claims probe.jsonl --root <scratch>` → exit 1,
  `VERDICT_BEARING_CLAIMS=2/14`, `RESEARCH_GATE: DRIFT (claims=14 supported=2 … mismatched=12 …)`
  — exit 1 is the expected DRIFT because the fixture pre-registers every span as supported and
  the gate rejects 12 of 14; it is the measurement, not a gate fault.
- Per-probe: gate `unsupported` + new `VERBATIM` (DIFFER) on: emdash-left-neighbor
  (`alpha—omega`), curly-left-neighbor (`“hello there”`), hyphen-cut-before (`cross` of
  `cross-check`), apos-cut-head (`i-ryu` of `jin'i-ryu`), ws-run-collapse (`gamma   delta` vs
  `gamma delta`), newline-in-gap, nfkc-ligature (`ﬁne` vs `fine`), soft-hyphen-in-word.
- Agreeing rows: underscore-neighbor and punct-both-sides (both hit), midword-cut,
  case-sensitive, cjk-neighbor, digit-glued (both miss).
- The four DIFFER rows emdash / curly / hyphen-cut / apos-cut reproduce, one-for-one, the
  r4 probe classes that note measured as gate failures (`anchor-boundaries-r4.md`), which
  cross-validates the harness. First harness run had two malformed probes (a space sat
  between the dash/apostrophe and the span, so the neighbor was a space); they were fixed to
  true abutments and only the corrected run is recorded.

## Divergences that could grow two silent conventions

- **Divergence A (the one to document): hyphen/apostrophe joiner clause.** The gate treats a
  compound as one token, so a span cut at `cross-` or after `jin'` misses; the frozen
  quote-reopen rule has no joiner clause, so the same cut is VERBATIM. This is not forced by
  the input medium. The frozen fixture does not depend on it: all 4 truncated-token rows cut
  inside alnum runs (items `ad795e73` `…iterable pat`, `98406fc4` `…be incl`, `4798287c`
  `…to ans`, `f98e78ae` start-cut `he OWL…`), so the isalnum rule labels them ABSENT exactly
  as the gate would — the frozen predicate is untouched. But `corpus/knowledge/quote-reopen-r29.md`
  (wave-1 scribes) should name this delta explicitly, or the lane will hold two span
  conventions that disagree on hyphen/apostrophe-edge cuts with no recorded reason.
- **Divergences B-D are medium-forced and justified:** typographic punctuation abutment
  (B — gate's own r4 named-limit, resolved here by isalnum after normalization), whitespace
  collapse (C), NFKC/markup normalization (D). Direction is uniform: measured, and by set
  construction (every gate boundary character is a non-alnum character or an edge, so every
  gate-accepted occurrence on identical normalized text is new-accepted), the new accept set
  contains the gate's — the new rule never rejects a span the gate would accept on the same
  text. No probe class with the reverse direction was found; the set argument above is by
  construction, the 14 probes are the measured confirmation. [INFERENCE for untested inputs]

## Limits

- Read-only seat: no lane file edited, no git/jj writes, gate selftest not run, zero network.
- The 14-probe battery covers the divergence classes named by the r4 note plus the
  normalization classes; it is not exhaustive over Unicode (e.g. full-width forms, combining
  marks were checked by reasoning only — full-width digits are alnum in both rules and NFKC
  folds them to ASCII).
- `claims.md`, `c1-count.py`, and the fixture were treated as frozen throughout; nothing here
  proposes changing them. Verdict-facing summary: 4 root-cause divergence groups (rows 2/5/6/7
  of the table), 3 justified by the medium, 1 (joiner clause) a genuine convention delta to
  record in `quote-reopen-r29.md`.
