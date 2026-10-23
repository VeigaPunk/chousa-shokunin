# Round 30 build — sibling-overlap scan (ConnectorSiblings)

Scope per dispatch: sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin`
(20 repos, `chousa-shokunin` excluded, read-only), for prior knowledge, tools or
SOURCES rows touching this round's three surfaces: HTML-to-text head handling
(C1), per-URL total deadlines / slow-drip (C2 T4), DNS rebinding /
connect-to-validated-address (C2 T1). No network used; all evidence is repo
files I opened plus `rg` output. Judged axes: coverage, operability.

Method: `rg` over all sibling lanes for `rebinding`, `getaddrinfo`, `slowloris`,
`settimeout`, `html\.parser`, `</head>`, `is_global`, `ipaddress`, `urlopen`,
`create_connection`, `dns.?rebind`, `TOCTOU`, `monotonic`, `deadline`, `drip`,
`reopen.?quote`, `w3\.org/TR/html`, `getpeername`, `connect_ex`; then opened the
relevant files. A first `grep -rn` run timed out at 300 s on fixture volume;
`rg` completed in under 4 s per pass. No tools installed (host `rg` at
`~/.local/bin/rg` already present).

## Hit inventory

### Surface 1 — HTML-to-text, `</head>` omission, `html.parser`

1. **`kotodama-shokunin/reports/round-57/reopen-quote.py`** (byte copies at
   `reports/round-58/` and `reports/round-59/`; diff of r57 vs r59 silent).
   This is kotodama's live quote re-open instrument (`corpus/lessons/
   round-57.md:27` names it the LOCATE leg; `round-58.md:3` says the round-58
   copy was "a byte copy of round 57's"). Its `_Text` parser
   (`reopen-quote.py:56-71`) keeps text outside `script`/`style` depth only —
   no `head`, `title`, `noscript` or `template` handling at all, so its text
   includes `head` content and is unaffected by a missing `</head>` (title text
   leaks in as ordinary data). Fetch side (`:78-93`): `urllib.request.urlopen`
   with `timeout=120` — a per-operation timeout, no total deadline; urllib
   resolves the host again inside `create_connection`, so it carries the same
   T1 shape chousa's tool had at base. Its stated contract only promises the
   120 s timeout and a 120 MB cap, so this is not a defect there.
   **Cite?** Adjacency report only. Worth one line in the round-30 knowledge
   entry noting the sibling lane's locator makes a different, weaker text
   contract (script/style only); do not import its parse rules — they fail
   chousa's contract item 1 (`title` content must be dropped).

2. **`kake-shokunin/corpus/SOURCES.md:34` (row S026)** — mined tier-A row on
   `https://docs.python.org/3/library/html.parser.html`, anchor "Tag and
   attribute names are lowercased and entities decoded, but matching end tags
   and HTML5 tree construction are not validated", opened 2026-10-20,
   used by `corpus/knowledge/static-canonical-preflight.md` and
   `corpus/lessons/round-22.md`. The round-26 adjudication
   (`corpus/lessons/round-26-verifier-spotcheck.md:91`) reclassified the
   implicit-closure wording to the docs' narrower claim (the parser does not
   call end-tag handlers for elements closed implicitly by an outer close).
   `knowledge/static-canonical-preflight.md:67-72` states the parser "is not
   an HTML5 DOM/tree builder … does not check matching start/end tags".
   **Cite?** Yes, but only as fleet context in prose — claims.md freezes the
   C1 SOURCE as a W3C page on `www.w3.org` opened this round, and the frozen
   wording rule means chousa lands its own row. The S026 sentence does carry
   design weight: html.parser will never emit the implied `</head>` /
   `<body>` transitions itself, so the head-boundary state machine must be
   in-tool (see proposed move).

3. **`kake-shokunin/scripts/canonical_audit.py` + `scripts/base_path_audit.py`
   + `scripts/link_preview_audit.py`** — three offline `html.parser` tools.
   `canonical_audit.py:102-108` (usage text) declares "HTMLParser is not an
   HTML5 tree builder … only explicit, properly closed head markup with
   supported head children is evaluated"; i.e. its policy is to REJECT
   unsupported head shapes (`html_unsupported`), the opposite resolution of
   C1's which must salvage body text from unclosed heads. `link_preview_audit.py
   :34` explicitly documents "a tag in <body> counts the same as one in
   <head>", and `MetadataParser` (:89-120) ignores template/svg/math
   descendants via an open-count stack — the same "open-count" idiom the C1
   fix needs for script/style/title/noscript/template skipping, but keyed to
   a different boundary. `base_path_audit.py:22-44` notes "the source is read
   with html.parser, not with a browser" and keeps a documented list of
   tokenizer edges where html.parser differs from a browser.
   **Cite?** As adjacency for the D-family repair drafts: kake's lane
   precedent is "declare the unsupported shape" (exit-2 finding), chousa's
   contract item 1 is "extract text from it". Contested scope: none conflicts
   with C1; the two contracts pick different sides of the same boundary.
   The open-count idiom (link_preview_audit.py:96-121) is directly reusable
   shape: it survives unmatched end tags and never decrements below zero.

4. **`kagi-shokunin/corpus/SOURCES.md:37` (row S031)** — WHATWG HTML syntax,
   comments section: comment data may contain `>`. Bounds chousa's C1 only if
   the to-text step treats `<!--` as tag-open; chousa's parser uses
   `handle_comment`/`handle_data` from html.parser so it is already covered.
   Adjacency, no cite needed.

5. **`kama-shokunin/corpus/lessons/round-1-critic.md:44,66`** — `</head>`
   inside captured HTML error pages only. No relevance.

6. **`mori-shokunin/corpus/evidence/sources-r32/S177.src`** — a retained
   docs.python.org `html.html` page snapshot. Adjacency only.

### Surface 2 — per-URL total deadline / slow-drip

7. **No sibling implements a total per-URL deadline.** The closest patterns:
   `kagi-shokunin/corpus/release-clock.py:753` uses `opener.open(request,
   timeout=20)` — per-operation socket timeout, same shape chousa's round-29
   tool had; `kotodama` reopen-quote `timeout=120` likewise. Neither lane's
   contract states a wall-clock bound, so neither is a defect there — but both
   are evidence that "socket timeout per call" is the fleet-wide default and
   chousa's stated "30 s total deadline" is the unusual contract worth
   repairing (which is exactly C2). `kama-shokunin/tools/kama-llamacpp-live.py
   :359,855` uses `create_connection(..., timeout=1.0)` for readiness polls.
   `souji-shokunin/corpus/SOURCES.md` rows S034/S038 document GNU timeout(1)
   exit codes — a process-level bound, not a fetch bound. **Cite?** C2's
   frozen SOURCE is the docs.python.org socket-timeout page; sibling lanes
   hold no prior row on it. Report only.

### Surface 3 — DNS rebinding / connect-to-validated-address

8. **`kagi-shokunin/corpus/release-clock.py`** — the strongest hit in the
   fleet. `public_addresses()` (:305-327) resolves once per hop via
   `socket.getaddrinfo`, rejects when any returned address fails
   `ipaddress.ip_address(...).is_global` (:319-323), and returns the deduped
   tuple of validated addresses. `PinnedHTTPSConnection` (:248-274) subclasses
   `http.client.HTTPSConnection`, swaps `self._create_connection` for a
   connector that calls `socket.create_connection((ip, port), timeout,
   source_address)` over the validated tuple only, inside `connect()` — so the
   URL host stays on the `Host` header and TLS SNI/certificate check while
   the socket never re-resolves. `PinnedHTTPSHandler` + `make_public_opener`
   (:277-297) wire it into urllib. `request_body()` (:740-767) re-runs
   `public_addresses` per redirect hop and gates each hop through
   `redirect_allowed` (:230-246). `valid_public_https_url` (:172-207) also
   refuses non-global literal IPs up front (:188). This is contract item 3
   implemented end-to-end in a sibling lane.
   **Cite?** Not a SOURCES row (it's sibling own-work, not a fetchable doc —
   chousa's SOURCES registry does hold `own-work` rows such as S001, so a row
   pointing at kagi's file is format-possible if the L1 wants it). Definitely
   cite in the knowledge entry / build report as the design precedent for the
   `_check_address` return-value change.

9. **No sibling has a DNS-rebinding lesson or sentinel vocabulary.** Greps for
   `dns.?rebind`, `TOCTOU`, `second lookup`, `resolve.*once` found nothing on
   point outside chousa (the mass of `rebind*` hits in audio/game-dev lanes is
   RID/variable rebinding in Godot physics proofs — different word, different
   domain). Chousa's T1/T4 sentinel framing is fleet-novel.

10. **`kotodama` reopen-quote** — see hit 1: carries the same double-resolve
    shape (urllib `urlopen` re-resolves inside `create_connection`). Adjacency
    worth one line: the same defect class lives in the sibling locator, and
    the kagi pinning pattern would repair it — but that is kotodama's lane
    and its contract never promised one resolution; report, do not absorb.

## Gaps

- No sibling SOURCES row on `www.w3.org` HTML spec pages (the only `w3.org`
  hits are Godot vendored comments in game-dev-3d fixtures, CSS/WebAudio
  spec names, and tabi's W3C WebDriver BiDi row S005 — different document).
  C1's frozen "open a W3C HTML specification page" step is unclaimed ground.
- No sibling SOURCES row on `docs.python.org/3/library/socket.html` (C2's
  frozen source). kake's Python-doc rows cover `html.parser` and
  `urllib.parse` only.
- No `slowloris`/slow-drip terminology anywhere in the fleet corpus.

## Proposed move (one, bounded)

**Transplant the `release-clock.py` validated-address contract into
`tools/quote-reopen.py`'s `_check_address` → connection path, and fix the head
skip as a boundary state rather than a skip depth.**

1. C2/T1: change `_check_address(host, port)` to return the deduped tuple of
   validated global addresses (the kagi `public_addresses` shape, minus its
   HTTPS-only policy), then subclass `http.client.HTTPConnection` /
   `HTTPSConnection` inside the tool to swap `_create_connection` for one that
   `socket.create_connection`s to a validated IP. `conn.host` remains the DNS
   name, so `Host` and TLS SNI/certificate checks are unchanged — matching
   contract item 3 exactly, including its "host name still used for TLS"
   clause. The harness logs `socket.socket.connect` destinations
   (`qr_harness.py:91,100-110`), so every logged connect lands in the item's
   routed set by construction.
2. C2/T4: keep the existing `deadline`/`remaining` plumbing but tighten the
   two reads it currently misses — the chunked `resp.read(CHUNK)` loop's
   per-64-KiB `settimeout(remaining)` (which lets a drip stall almost
   `remaining` once more after the deadline conceptually passed) by checking
   the deadline inside the read path on every chunk, and the header phase by
   bounding `conn.getresponse()` the same way. This reuses what the tool
   already has; the sibling evidence (hit 7) supplies the argument that a
   per-call socket timeout alone does not bound a drip, which is the sourced
   teaching the C2 SOURCE row must support.
3. C1: implement contract item 1 as a head-boundary boolean in `_Text`
   (head open at `<head>`, closed at `</head>`, `<body>`, any non-whitelisted
   start tag, or non-whitespace character data; `title` joins the dropped set)
   rather than leaving `"head"` in the `SKIP` depth counter — a depth counter
   can never be decremented by `</body>` and is exactly what strands the 28
   misses. kake's S026 anchor (hit 2) is the reason this must be in-tool:
   html.parser will not synthesize the implied boundary. The open-count idiom
   from `MetadataParser` (hit 3) is the proven shape for the script/style/
   title/noscript/template skip stack.

Affected axes: coverage (C1) and operability (C2) both improve; neither is
harmed — the claims' separability section keeps the two changes in disjoint
layers and the move touches nothing outside `tools/quote-reopen.py`. D3
fixture classes (script windows, case flips, verdict-order items) are
exercised by the C1 counter as-is.

Risks: (a) `socket.create_connection((ip, port))` with an IPv6-mapped or
zone-id address — kagi strips nothing but the name map here yields plain
routed addresses, and chousa's `_check_address` already strips `%`-zones at
:201; carry that strip into the stored tuple. (b) `HTTPSConnection.connect`
internals are version-private (`_create_connection` swap is a documented
subclassing surface only in the source sense) — mitigated because the harness
imports the tool and runs on the host interpreter; pin nothing newer. (c) A
per-hop validated tuple shared across retries is required by contract item 2
(retry inside the same deadline) — re-resolve per new hop only, never per
retry of the same hop. (d) `title` content drop is new behavior versus the
round-29 SKIP set; counter items place title windows as separate items, so
verify the 106/106 run specifically on title-window items. (e) kotodama's
locator carries the same T1/T4 shape — flag as adjacency in the knowledge
entry; do not let the fix's description claim fleet-wide repair (D1 wording
rule).

Verification: run the frozen counters only —
`python3 corpus/evidence/round30/c1-count.py` → `QUOTE_REOPEN_HEADLESS_MATCH
=106/106`, `python3 corpus/evidence/round30/c2-count.py` →
`QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27`, plus both counters on the
C2-only commit per the separability landing order. No counter, harness or
claims edit. The falsify wave re-applies MutSkipScript/MutCasefold/MutOrder.

## Contested scope / adjacency summary

- kake explicit-head rejection vs chousa headless salvage: same parser limit,
  opposite contracts — report, never absorb.
- kotodama locator's script/style-only text and double-resolve fetch: same
  defect class, different (weaker) stated contract — report, never absorb.
- kagi pinning tool: contract-conforming precedent worth citing; its
  per-operation timeout is not a defect because its stated bound differs.
- game-dev/audio `rebind` hits are Godot RID semantics — word collision only.

Limits: read-only scan; I did not run the counters or open any URL. `rg` is
gitignore-aware, so a deliberately ignored file could hide a hit; a
`--no-ignore` pass was not run (fixture volume). Judged axes: coverage,
operability.
