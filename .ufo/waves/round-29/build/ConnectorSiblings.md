# Round 29 wave 1 — sibling-overlap scan (seat ConnectorSiblings)

Scope: read-only scan of the sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/`
(all lanes except chousa) and of `/home/vgpnk/Projects/shokunin/scripts/` for any existing tool
or knowledge entry that re-opens `corpus/SOURCES.md` quotes against live sources, checks located
quotes, or normalizes HTML text for quote matching. Adjacency rule applied: **report, never
absorb**; every hit below names its call (duplicates / complements / conflicts) and the
contested scope.

No network GET was issued by this seat. Every quote below is copied from a repository file at a
pinned commit, not from a page. No tool was installed or updated. Nothing was written outside
this report and my own directory `.ufo/waves/round-29/build/ConnectorSiblings/`.

## Commands run (with observed results)

| # | Command (cwd `/home/vgpnk/Projects/shokunin` unless noted) | Result |
|---|---|---|
| 1 | `for r in */; do git -C "$r" rev-parse HEAD; done` | 22 lane heads; every `path@commit` below was pinned this way |
| 2 | `grep -rlIE 'urlopen\|urllib\.request\|requests\.get\|HTMLParser\|html\.parser\|BeautifulSoup\|NFKC\|html\.unescape' --include='*.py' --include='*.mjs' --include='*.js' --include='*.sh' .` (excluding `site-packages`, `node_modules`, venvs, `arc3-loop1`, kaidoku `round-23/runtime`) | 40 paths, exit 0; after discarding unrelated model probes (kengaku, lore, research) the live-HTML readers are the 6 files in the table |
| 3 | `grep -rnIE '(quote\|text)[^=]*\bin\b *(page\|text\|body\|html)'` (same excludes) | the only quote-in-text tests are `kaidoku quote-fidelity.py:256` and the kotoba counters (via `norm(...) in page`) |
| 4 | `grep -rlI 'chousa'` over sibling code (excluding `.ufo/waves`) | 1 hit: `kotoba-shokunin/verifiers/check_sibling_census.py` (it names lanes in prose; it reads no chousa registry) |
| 5 | `grep -rnIE 'urlopen\|curl \|SOURCES\.md\|verbatim\|located quote' scripts/` | fleet `scripts/` holds `sources-census.sh` only; it parses `SOURCES.md` textually, no fetch |
| 6 | `python3 -c "import urllib.request,inspect; print(inspect.getsource(urllib.request.HTTPRedirectHandler.redirect_request))"` | Python 3.14.8 on this host: the stock handler checks method and status only, **no scheme check on the redirect target** |

## Hits

| path@commit | what it does | call | contested scope |
|---|---|---|---|
| `kotoba-shokunin/verifiers/check_explicit_invocation.py@b0b7140b5a7cf8a50f13989ee6285fc8ee245c41` (blob `9000d1af`) | reads `corpus/SOURCES.md`, takes the **first** http(s) URL out of a row's `source` cell (`URL_RE` line 156, `um.group(0)` line 414), fetches it with `urllib` (line 357), reduces the page with `norm_page` (line 329: regex tag strip, `script`/`style`/comments dropped, `html.unescape`, `'` and `"` folded, lowercased, whitespace collapsed), then `r["found"] = norm(r["quote"]) in page` (line 613). Quote comes from the lesson `## Gate` section. `--fetch` only | **complement, and the nearest partial duplicate**: same capability class (registry URL to live page to quote-in-page), weaker rule (case-folded, no token boundary, no NFKC, no word cap, no per-item verdict line), claim-local inputs (5 fixed client rows), and a fetch failure is folded into `found=False` (lines 609-614) — the frozen contract instead requires `UNREACHABLE` and calls it a mismatch | "who owns live registry-quote re-opening"; its counters fetch for their own claim only |
| `kotoba-shokunin/verifiers/check_description_thresholds.py@b0b7140b` (blob `977ea768`) | identical fetch/match shape: `norm` line 235 (tag strip, `html.unescape`, lowercase), `fetch` line 243, `norm(quote) in page` line 455 | complement / partial duplicate | as above |
| `kotoba-shokunin/verifiers/check_mcp_instructions.py@b0b7140b` (blob `2901d7b5`) | identical shape: `norm` line 211, `fetch` line 219, match line 376 | complement / partial duplicate | as above |
| `kotoba-shokunin/verifiers/check_overlap_levers.py@b0b7140b` (blob `81170cac`) | `--fetch` live probe: `first_https_url` line 485 (first https URL in the cell, trailing punctuation trimmed, `.rstrip(".,;:)!?")` line 490 — the same rule the frozen contract states for the chousa tool), `fetch_text` line 493 (20 s timeout, plain User-Agent line 119), `quote_on_page` line 500, `fetch_probe` line 504 (also tries `url + ".md"`). `normalize` line 480 strips tags, emphasis and whitespace runs only | **complement, and the closest prior art for two frozen bullets** (first-URL extraction with trailing-punctuation trim; bounded live fetch of a registry URL) | URL-extraction and fetch-bounds conventions |
| `kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py@d210fb8fa62d2af04d009cfa0c65a4e8137dc742` (blob `c00c2e64`) | quote-location fidelity gate over a manifest of `{id, source, section, quote}`: `MAX_WORDS = 25` (line 73), `CLEAN, FAILED, CNE = 0, 1, 2` (line 72), `grade_quote` (line 250) emits `quote_too_long`, `quote_not_contiguous` ("no contiguous occurrence in source"), `quote_location_mismatch`; sources are **sha256-pinned local files**, `source_tampered` on mismatch; per-item verdict lines plus a summary; self-test fixtures | **complement** (offline, pinned, section-scoped) with **vocabulary overlap** | the 25-word cap; the "quote verdict per item + summary + exit 0/1/2" line shape; offline-pinned versus live-registry source kinds |
| `kaidoku-shokunin/.ufo/gates/citation-drift/citation-drift-probe.py@d210fb8f` (blob `3b6085ce`) | resolves citations against Git objects at a named revision or against committed snapshots, with a sha256-pinned pointer table; never opens a network connection; `snapshot_tampered`/`pointer_table_tampered` are could-not-evaluate, exit 2 | complement | citation location against a pinned revision; the `CNE = 2` convention |
| `kaidoku-shokunin/tools/round-25/a2/resolve-selectors.py@d210fb8f` (blob `23880aa5`) | `fetch` subcommand queries third-party endpoints with `urllib`, stores each raw response plus UTC time and sha256 in a manifest, and `analyze` replays offline over the stored bytes | complement | "record the bytes and replay offline" pattern |
| `kake-shokunin/scripts/live_snapshot.py@3555f63fbf58f19445823eb88bc3161b7b1faad4` (blob `33050857`; lane HEAD moved to `9d81c75c` during this scan) | GET-only owned-page snapshotter: `safe_url` requires scheme in `{http, https}`, a hostname and **no userinfo** (lines 37-40); `Redirects.redirect_request` refuses any redirect target that fails `safe_url` and any non-GET redirect method (lines 55-64), with the comment "urllib otherwise reports an unfetched file:/userinfo destination as geturl()"; 20 s timeout, at most 5 redirects, 2 MiB cap, no cookies or credentials, per-surface `fetch.json` + `audit.json` + `page.html` + `manifest.json`, and `--reaudit` replays stored bytes with metadata, length and digest checks | **complement, and the prior art for the contract's "http and https only (redirects too)" bullet** | live-fetch bounds, redirect policy and User-Agent conventions |
| `kotodama-shokunin/tools/check-gate-quotes.py@25919ac42e7cf260644ac5a1d44d8cdabb9db46a` (blob `eb86f00c`) | `MAX_WORDS = 25` (line 97) cap over quoted runs in a lesson `## Gate` section, plus `ellipsis-joined`, `doubled-locator` and `truncated-grounds` (compares Grounds against the registry `teaches` cell). No network | complement | the 25-word cap and Gate-quote vocabulary |
| `kumitate-shokunin/scripts/sources-check.mjs@292d92668ff80973547a8b10d12ffb5a48f2d7d8` (blob `6b57424f`) | registry-shape checker for its own lane's `corpus/SOURCES.md` (row/heading normalization, id and URL uniqueness, tier/kind/status enums); no network | complement | registry validation |
| `kumitate-shokunin/scripts/cite-check.mjs@292d9266` (blob `78ff7390`) | resolves citations to local paths and Git content; no network | complement | local citation resolution |
| `kama-shokunin/tools/sources-append-only.py@1560e4d83f42b04f40336357de6f9637eafa0f4b` (blob `804bdf7e`), `kotoba-shokunin/verifiers/check_sources_append_only.py@b0b7140b` | enforce SOURCES-CONTRACT-v1 rule 2 (append-only) between two revisions of `corpus/SOURCES.md`; both take `--repo` / `--path` and guard **their own** lane | complement, and a **gap**: neither covers the chousa registry, and chousa has no `verifiers/` directory | who guards the chousa registry's append-only rule when rows S046-S049 land |
| `kotoba-shokunin/verifiers/check_sibling_census.py@b0b7140b` | re-opens a located quote at its pinned commit ("the quote occurs verbatim -- after collapsing whitespace runs on both sides -- on the cited line or within +/-2 lines of it", header lines 46-49), live on every run; also rejects an empty quote cell as FALSE CONTENT | **complement**: this is the fleet's other quote-reopen shape — quote against a **git revision**, where the chousa command re-opens against a **live registry URL** | quote-reopen ownership is now split by source kind: pinned revision versus live page |
| `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh@fleet HEAD` | fleet-wide `SOURCES.md` census/validate/overdue/shared over all child lanes; parses text, writes stdout or `--out` only, no fetch | complement | registry census and validation stay fleet-owned |

## Adjacency verdict

1. **No sibling command duplicates the new command.** No lane has a registry-driven, items-file
   driven re-opener that emits one verdict per item with the frozen taxonomy. The capability is
   split across three weaker shapes: kotoba's four round counters (live fetch, case-folded
   substring, claim-local inputs), kaidoku's `quote-fidelity.py` (pinned local bytes, section
   scoped), and kotoba's `check_sibling_census.py` (pinned commit, +/-2-line window). The chousa
   command is the general, live-registry member of that family; its rule (NFKC, exact case,
   token boundary, 25-word cap, `UNREACHABLE` as its own verdict) is strictly stricter than the
   live-fetch members.
2. **Contested scope, named.** "Live registry-quote re-opening" is contested with kotoba's
   counters, not with the fleet scripts. Any future consolidation belongs to the L1, not to this
   seat. The 25-word cap is shared with kaidoku and kotodama; registry validation stays with the
   fleet census and kumitate's `sources-check.mjs`, so the new command should not grow registry
   validation beyond the frozen `NO_SOURCE` rule.
3. **A verified fleet convention the contract already matches.** The `exit 2` role in the frozen
   contract (usage or I/O error, "a failed measurement; it is re-run") is the same role as
   kaidoku's `CNE = 2` and kotoba's `could-not-evaluate` exit 2. The contract is aligned; nothing
   to change.
4. **One concrete defect class for the fetch bounds.** Python 3.14.8's stock
   `HTTPRedirectHandler.redirect_request` checks only status and method; it performs no scheme
   check on the redirect target (command 6 above, read from the interpreter on this host).
   `kake-shokunin/scripts/live_snapshot.py@3555f63f` already implements the guard the contract
   needs, with a comment naming the `file:`/userinfo hole. That the chousa tool can be walked to
   a non-http(s) target through a redirect is **[INFERENCE]** — I did not run an exploit, and the
   network policy of this seat forbids a local test server.
5. **Candidate adjacency citations** for the L1 to judge (the fleet goal allows a dispatch note to
   name up to 3 sibling entries as `path@hash`; rows S046-S049 are already spoken for by the four
   source seats, so these are extra): `kotoba-shokunin/verifiers/check_overlap_levers.py@b0b7140b`
   for first-URL extraction with the trailing-punctuation trim,
   `kake-shokunin/scripts/live_snapshot.py@3555f63f` for redirect and fetch bounds, and
   `kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py@d210fb8f` for the per-item
   verdict plus summary shape and the 25-word cap.

## Contradiction found while scanning (stated, not smoothed)

The frozen text at `corpus/evidence/round29/claims.md:150-151` reads: "Any control that reaches
`130/130` voids v2 too: C1 would then be declared exploratory, never re-scaled." A control in the
lane's own pre-data control directory meets that condition on the two seeds the control wave
recorded, and only on them.

Evidence, all read-only:

- `.ufo/waves/round-29/controls/CtlLabelKeyed/control-v2.py` (the warmed label-keyed cheat) builds
  its answer key from the committed fixture labels **and** from
  `receipt-v2.json` and `receipt-v2-seed2.json` in its own directory — `remember(case["source_id"],
  case["quote"], case["label"])` over those receipts' `cases` — and fetches nothing.
- `receipt-v2-warmed.json` (seed 2901) and `receipt-v2-warmed-seed2.json` (seed 2902) both record
  `"match": 130, "total": 130, "predicate_holds": true` with counter sha256
  `574ffcad7a78d2fdf04b895445c1aac72537cc548b944cae62012baf4ba4e2dd`.
- `receipt-v2-warmed-freshseed-L1.json` (seed 2848469338, an unrecorded seed) records
  `"match": 106, "total": 130, "predicate_holds": false` for the same control code.
- The counter's seed is random when `--seed` is absent: `c1-count.py:250` reads
  `seed = opts.seed if opts.seed is not None else secrets.randbits(32)`. The frozen predicate
  line (`claims.md:33`) names the counter with no `--seed`, so the predicate's literal form is
  the fresh-seed form.
- Every receipt carries the full `cases` list with `label`, so the labels of any recorded seed
  are committed bytes after the first run on that seed. Command:
  `grep -rhoE '"seed": [0-9]+' .ufo/waves/round-29/controls/ | sort | uniq -c` gave, at the time of
  writing, 24 fields at 2901, 21 at 2902, 1 at 2917, 1 at 2848469338 and 1 at 8324306809653312270 —
  45 of 48 seed fields sit on the two recorded seeds. The counts move while seats run; the copy of
  the command's output I took is in `.ufo/waves/round-29/build/ConnectorSiblings/recorded-seeds.txt`.
- The nearest live-fetch sibling shape (kotoba's counters, hit 1 above) is the same shape as the
  `CtlCasefoldNoBoundary` control, whose v2 receipts record 126/130 on both recorded seeds
  (`receipt-v2.json`, `receipt-v2-seed2.json`); all 4 misses are the 4 frozen
  `absent-truncated-token` items (S008, S013, S020, S044). So the whole margin between that
  shortcut shape and the threshold is the token-boundary rule on truncated tokens.

I do not judge this. Two readings exist and the frozen files may not be edited: (a) a control that
needs the lane's own prior receipts is not "a control" under the frozen sentence, and v2 stands;
(b) the sentence is unconditional and v2 is voided. The measurement discipline below holds under
either reading.

## Proposed move (one, bounded)

**Measure the after value only through the predicate's literal, unseeded counter form, and record
the seed in the receipt; a receipt whose `seed` already appears in any pre-existing lane receipt
must not be offered as the after value.**

- Affected axis: **operability** (the claim's axis) — it makes the after value evidence of the
  capability rather than of same-seed replay. Other axes: no harm. The tool contract, the counter,
  the fixture and the predicate are untouched; the command line is already the predicate's own.
- Cost: zero. The counter already defaults to `secrets.randbits(32)`; the receipt already records
  `seed`. The only new requirement is a check before the after value is written: compare the
  receipt's `seed` against the seeds in `.ufo/waves/round-29/controls/*/receipt*.json`.
- Why it is non-obvious: the seed is recorded *inside* the receipt, so a run can look perfectly
  formed while its labels were already committed by an earlier run on the same seed.

## Risks

- A reader could take this as narrowing the target after data. It does not: no data seat has run
  (`tools/quote-reopen.py` does not exist; `tools/` holds `research-gate.sh` only), the frozen
  predicate line omits `--seed`, and the counter's default is random. Rejecting only *recorded*
  seeds is the smallest possible form.
- If the design owner rules reading (a) above, the discipline is still correct and merely
  redundant; if reading (b), the discipline keeps the after value admissible.
- Rejecting the two recorded seeds must not become a re-scale of the claim: the before value
  (`before-do-nothing-v2.json`, seed 2901, 0/130) stays as recorded history.

## Verification the L1 can run

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
# 1. recorded seeds, and how many of them
grep -rhoE '"seed": [0-9]+' .ufo/waves/round-29/controls/ | sort | uniq -c
# 2. the warmed control's two seeds versus a fresh one
python3 -c "import json;[print(p, json.load(open(p))['seed'], json.load(open(p))['match'], json.load(open(p))['predicate_holds']) for p in ('.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v2-warmed.json','.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v2-warmed-seed2.json','.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v2-warmed-freshseed-L1.json')]"
# 3. the after value, unseeded, receipt recording the fresh seed
python3 corpus/evidence/round29/c1-count.py --receipt /tmp/after.json -- python3 tools/quote-reopen.py verify
python3 -c "import json;print(json.load(open('/tmp/after.json'))['seed'])"
```

## Limits

- Read-only seat: I ran no counter, no control and no tool; `tools/quote-reopen.py` does not exist
  yet, so the duplicate/complement calls above compare the frozen contract against sibling code,
  not the command's bytes.
- No network GET was issued; nothing here is a located page quote, so no URL and access date are
  owed.
- Sibling lanes are live: `kake-shokunin` HEAD moved from `3555f63f` to `9d81c75c` during this
  scan, so the `kake` row is pinned to the commit whose blob I read (`33050857`).
- The grep in command 2 was bounded and its exclusions are stated; I did not walk every sibling
  `.ufo/waves` tree, so a live-fetch quote matcher hidden in an unlisted archive tree is possible.
