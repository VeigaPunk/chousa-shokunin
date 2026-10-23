# ExecC1HeadB — independent second implementation of contract v2 item 1 (head boundary)

## What I did

Copied `tools/quote-reopen.py` to `.ufo/waves/round-30/build/ExecC1HeadB/quote-reopen.py`
and rewrote only the HTML-to-text step as an independent implementation (no other seat's
files under `build/` were opened). The round-29 `_Text` class was an
`html.parser.HTMLParser` with a flat skip counter. My version is a small insertion-mode
machine over a hand-written tag scanner (`class _Reader`):

- Three modes — `before-head`, `in-head`, `after-head`. The head opens only at a `<head>`
  start tag. In `in-head`, `</head>`, `<body>`, `</body>`, `</html>`, `</br>`, any start
  tag outside `HEAD_CONTENT` (the contract's list of 11 names), or non-whitespace
  character data moves to `after-head`; that data is emitted as page text. Whitespace-only
  data in `before-head`/`in-head` is dropped. Any token that cannot be head content in
  `before-head` implies an empty head (`<html>` alone leaves the mode unchanged).
- `title`, `script`, `style` are raw-text: the scanner jumps to their case-insensitive
  end tag wherever they appear (`_swallow`, regex `_RAW_END`). `noscript`, `template` are
  dropped by a balanced-element stack (`self.dropping`), so nested templates work.
- The scanner handles comments, declarations, processing instructions and bogus
  comments, quoted/unquoted attribute values (`>` inside quotes does not close a tag),
  `</>` and `</x` malformations, and literal `<` in data. `html.unescape` replaces
  `convert_charrefs`; `norm`, `found`, `BLOCK` and the whole fetch layer are untouched.
- Deliberate spec-faithful divergences from the round-29 parser (fine for an N-version
  diff): `/>` on a non-void element is ignored (`<title/>x` reads `x` as title raw text),
  and `<noframes>` content is emitted (contract lists `noframes` as head content but not
  as a dropped element).

## Scores (frozen counter, run from lane root)

    timeout 400 python3 corpus/evidence/round30/c1-count.py \
      --tool .ufo/waves/round-30/build/ExecC1HeadB/quote-reopen.py \
      --receipt .ufo/waves/round-30/build/ExecC1HeadB/receipt-c1-run1.json
    -> QUOTE_REOPEN_HEADLESS_MATCH=106/106   exit 0
    run 2 (same command, receipt-c1-run2.json)
    -> QUOTE_REOPEN_HEADLESS_MATCH=106/106   exit 0

Receipt fields (both runs): `predicate_holds: true`, `tool_rc: 1` (ABSENT items present,
expected), `tool_killed: false`, `misses_first40: []`, `counter_sha256` `5b312d84…`
and `harness_sha256` `e2be0dd1…` match the frozen v4 hashes in claims.md.

## difftext.py

`.ufo/waves/round-30/build/ExecC1HeadB/difftext.py FILE.html` loads the sibling
`quote-reopen.py` via `importlib` and prints `norm(html_to_text(doc))` — one logical
line for the wave-2 diff against the landed tool. Smoke test on a headless doc prints
`first & second words third fourth` (head, style, script dropped; entities decoded);
usage exit is 2.

## sha256

    7f6d234fabe528650cefefb5818aaa526b39da0a263bc13e8bc500c0b270775c  quote-reopen.py
    bbfd3ae764832e82ba23119c9b4ba0de0ba2a9f22b0329449f703a07e4bd1864  difftext.py

Files in this seat's dir: `quote-reopen.py`, `difftext.py`, `receipt-c1-run1.json`,
`receipt-c1-run2.json`. Scratch copies of test docs live under
`/fast/scratch/hyaku/chousa-r30/w1/ExecC1HeadB/`.

## Limits / risks

- `tool_rc: 1` in the receipts is the tool's own verdict exit (not all VERBATIM), not a
  failure; the counter scores per-item verdicts, all 106 matched.
- `LANE`/`DEFAULT_REGISTRY` in my copy resolves under `build/`; harmless because the
  harness always passes `--registry` (qr_harness.py `run_tool` builds `--registry` into
  the argv). No network was touched; counters run on loopback.
- Known divergences vs the base tool (for the wave-2 diff, none reachable from the C1
  corpus): `/>`-flag handling on non-void elements, `noframes`/`basefont`/`bgsound`
  content emitted, tag names limited to ASCII letters.
- No installs or updates were needed; `python3` stdlib only.
