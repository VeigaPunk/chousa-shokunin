# ScoutRegistryHeadless — C1 real-world reach of missing `</head>`

Round 30, wave 1 (build). Question: how far does the claim C1 edge class —
HTML documents that open `<head>` and never close it — reach across the
registry. One real GET per registered URL; no page bodies saved.

## What was done

- Read `corpus/evidence/round30/claims.md` (frozen, v4) and
  `corpus/SOURCES.md`. The registry table carries 40 `source`-column URLs
  on rows S002–S049; ten rows cite no URL (own-work rows). After fragment
  removal (S046's `#text-quote-selector`) the set dedups to 35 unique URLs;
  five URLs each back two rows (S019/S029, S020/S033, S021/S032,
  S022/S030, S024/S031). URLs in the unregistered `## Leads` section were
  not fetched.
- Wrote `.ufo/waves/round-30/build/ScoutRegistryHeadless/probe.py`
  (stdlib only: urllib + html.parser). One GET per unique URL, 30 s
  timeout, `User-Agent: chousa-shokunin-round30-registry-survey/1.0
  (chousa lane; quote-reopen C1 recon)`, six bounded workers, body read
  capped at 8 MiB and never persisted.
- `HeadProbe` records `<head>` start tag, `</head>` end tag, `<body>`
  start tag, and — only when `</head>` is absent — the first start tag
  after the last head-content element per contract v2 item 1
  (`base basefont bgsound link meta noframes noscript script style
  template title`; `#text` for non-whitespace character data, `EOF` if
  the document ends inside head). Raw-text (`script/style/title`) and
  `template/noscript/noframes` subtrees are skipped so their inner markup
  is not counted as the boundary.
- Verified the detector on 11 synthetic shapes before fetching (all
  passed): closed normal, headless→div, headless→body, headless→text,
  headless→EOF, headless with `<template>`/`<noscript>` subtrees, markup
  inside `<title>`, no-head, no-tags, uppercase.

## Evidence

- Command: `timeout 500 python3 probe.py pages.tsv` in the scratch dir,
  exit 0, wall time 4.12 s. Output:
  `unique-urls=35 rows=40 html-missing-head-end=1 ids=S047`.
- TSV: `.ufo/waves/round-30/build/ScoutRegistryHeadless/pages.tsv`
  (36 lines = header + 35 URL rows; sha256
  `1465870a1bb052757a1e7e868b1bb73ca5549260baba8ee80703ef24d63aacb9`).
- All 35 GETs returned a response; none timed out or raised.

## Findings

- HTML pages lacking `</head>`: **1 of 33** HTML responses —
  **S047** `https://wicg.github.io/scroll-to-text-fragment/` (200,
  text/html): `<head>` yes, `</head>` no, `<body>` yes, first tag after
  the last head-content element = `body`. Same row and count as round 29
  (S047, 1 of 32). Of the 35 unique URLs fetched, 1 lacks `</head>`;
  2 URLs are `application/pdf` (S011, S037) where the columns do not
  apply.
- The S047 boundary form is the counter's head-and-body class: a `<body>`
  start tag ends the unclosed head, so contract item 1 recovers exactly
  the body text the round-29 tool dropped.
- Other observed surface (not C1-relevant, recorded for the L1):
  - S024/S031 `https://schema.org/lastReviewed` — 200 text/html but no
    `<head>` or `<body>` tag detected anywhere in the served body
    [INFERENCE: JS-rendered shell or bot-shaped minimal page].
  - S021/S032 and S022/S030 (pubmed.ncbi.nlm.nih.gov) — HTTP 203
    text/html, all tags present.
  - S014 (cebm.ox.ac.uk) — 403 text/html error page, all tags present.
  - S025 (rfc-editor.org) — followed one redirect to
    `https://www.rfc-editor.org/info/rfc9111/` inside the single GET.

## Limits

- One GET each, no retries: transient states and any body not saved are
  uninspected (notably the schema.org anomaly).
- Tag facts come from `html.parser`, a lenient parser, matching the
  tool's own parsing family; a stricter tokenizer could differ on
  pathological markup.
- Counts are over unique fragment-stripped URLs, not registry rows; the
  two-row URL pairs appear once.
- Tooling: no installs needed — Python 3.14.8 stdlib sufficed.
