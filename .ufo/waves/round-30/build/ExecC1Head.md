# ExecC1Head — C1 head boundary implementation

Scope: tool contract v2 item 1 only (head boundary) in a copy of the round-29 tool at
`.ufo/waves/round-30/build/ExecC1Head/quote-reopen.py`. Fetch layer untouched.

## What changed

- `SKIP` drops `head` and gains `title` (drop list is now `script style noscript
  template title`; `head` is handled by a flag, not the skip counter, because it ends
  at a boundary rather than only at `</head>`).
- New `HEAD_ELEMENTS` = `base basefont bgsound link meta noframes noscript script
  style template title`.
- `_Text` gains `self.head` (inside an unclosed head) and `self.hdeep` (depth inside
  `<noframes>`, the only head element that can carry data `SKIP` does not already
  drop). The head starts at `<head>` and ends at the first of: `</head>`; a start or
  start-end tag outside `HEAD_ELEMENTS` (this covers `<body>`); or character data
  that is not only whitespace while outside head elements (that data is appended as
  page text). Tags and data inside `SKIP` or `noframes` content inside head do not end
  it. `BLOCK` handling and `html_to_text`/`norm`/`found` are unchanged.
- Module docstring: the "extracts the page text" sentence now states the head
  boundary rule and the dropped-content list. No other docstring edits.
- Everything from `def found` to EOF verified byte-identical:
  `diff <(sed -n '/^def found/,$p' tools/quote-reopen.py) <(sed -n '/^def found/,$p'
  .ufo/.../quote-reopen.py)` → empty, `FETCH-LAYER-IDENTICAL`.

## Measurements (run from lane root)

- `timeout 300 python3 corpus/evidence/round30/c1-count.py --tool
  /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-30/build/ExecC1Head/quote-reopen.py
  --receipt .../ExecC1Head/c1-run1.json` → `QUOTE_REOPEN_HEADLESS_MATCH=106/106`,
  exit 0 (receipt `predicate_holds: true`).
- Same command with `c1-run2.json` → `QUOTE_REOPEN_HEADLESS_MATCH=106/106`, exit 0.
- `timeout 300 python3 corpus/evidence/round30/c2-count.py --tool <same> --receipt
  .../ExecC1Head/c2-cross.json` → `QUOTE_REOPEN_FETCH_BOUND_MATCH=13/27`, exit 1 —
  the expected round-29 fetch profile (before: 12/27, 13/27 across runs). All 14
  misses are fetch-layer classes the C1 change cannot move: drip-body/drip-head
  killed at the 20 s cap (wall 20.0 vs bound 4.3-6.2), one drip-steady bound
  overshoot (4.06 vs 3.83), and rebind items logged `bad_dests` 127.0.0.1 / 10.x
  (the tool resolves again at connect).

## Local sanity (scratch, not the counter)

A small `html_to_text` check in `/fast/scratch/hyaku/chousa-r30/w1/ExecC1Head/` on all
four counter document shapes: body words present, title/script/style words absent;
`<head><title>T1</title>body text` → `body text`; `<head><meta>x` → `x`;
`<head><noframes>NF1</noframes><p>BP1` → `BP1`; body `<title>` dropped → `vis1`.

## Artifacts (all inside `.ufo/waves/round-30/build/ExecC1Head/`)

- `quote-reopen.py` sha256 `69682ce44bb98f020faa2447d2a192b4a6cea9f25c419801544c582661b5e33c`
  (counter receipts record the same `tool_sha256`; round-29 tool sha256 was
  `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea`).
- `c1.patch` — `diff -u` round-29 tool vs candidate, 4247 bytes, sha256
  `d5d7843eb9f8f0bd4035ff416ed66683b1dab9e5b9d242022fe26a018c62a96a`.
- `c1-run1.json`, `c1-run2.json`, `c2-cross.json` receipts.

## Limits / notes

- Only item 1 implemented; items 2-4 (fetch bounds) are another seat's work — the
  C2 cross-check exists to show this change does not regress them.
- `noframes` is in `HEAD_ELEMENTS` per the contract list but not in `SKIP` (the
  drop-wherever list names `title script style noscript template` only); its content
  inside head is contained via `hdeep`, outside head it is treated as ordinary
  markup. No counter document exercises it.
- No tools installed; no network accessed; counters ran in the loopback harness only.
