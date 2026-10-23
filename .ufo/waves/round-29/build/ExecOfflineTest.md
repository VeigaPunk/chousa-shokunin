# ExecOfflineTest — quote-reopen offline conformance test (round 29, W1)

**Deliverable:** `.ufo/waves/round-29/build/ExecOfflineTest/quote-reopen-offline-test.py` (569 lines, stdlib only, SHA-256 `e09aebdb370d955a8cae81c7534e1cb7f8f136fd015debf95cabe2ff5dd989c6`).

A loopback-only conformance harness for the frozen "Tool contract (frozen)" in
`corpus/evidence/round29/claims.md`. It starts a private `http.server` on
127.0.0.1 (random port), serves 26 synthetic pages, writes a temp registry
(`SOURCES.md` rows pointing at loopback URLs) plus an `items.tsv` (45 items),
runs `CMD verify --items X --registry Y`, and scores the output. It never reads
the frozen fixture and never runs `c1-count.py` (L1 stop-order honored: zero
counter executions, zero seeds).

## Usage

```
python3 .ufo/waves/round-29/build/ExecOfflineTest/quote-reopen-offline-test.py \
  [--lane-root DIR] [--work-dir DIR] [--quiet] -- CMD...
```

The harness appends `verify` when CMD does not already end with it, then always
appends `--items <items.tsv> --registry <SOURCES.md>`. `--lane-root` defaults to
the nearest ancestor containing `corpus/SOURCES.md` (the lane), which is the
candidate's cwd. Temp files go to a `quote-reopen-offline-*` dir inside
`build/ExecOfflineTest/` (inside the lane, inside my own seat dir), removed in
`finally`; `--work-dir` overrides. Prints `OFFLINE_TEST_PASS=<n>/<t>`; exit 0
iff all checks pass. Loopback only: every URL is 127.0.0.1.

## Coverage (45 items + 20 structural checks = 65 checks)

All derived from claims.md "Tool contract (frozen)":

- **Entity decode (i01/i02):** `&amp;` / `&#8217;` / `&nbsp;` decode on the page
  side; a quote containing literal `&amp;` is ABSENT (quote text is not entity
  decoded — the frozen normalization list is closed).
- **Quote spanning `<em>`/`<a>`** (i03/i04); **newline inside a paragraph**
  (i05).
- **script/style/head not matchable** (i06–i08, head drops its title),
  **noscript/template** (i38/i39), **HTML comment** (i09).
- **Invisible chars deleted** (i10 SHY, i11 ZWSP, i12 ZWSP inside the quote,
  i40 ZWNJ, i41 ZWJ, i42 BOM).
- **Curly-to-straight quotes both ways** (i13 straight quote vs curly page,
  i14 pair, i43 all 8 curly chars, i44 curly in quote vs straight page).
- **NFKC** (i15 U+FB01 `ﬁ` → `fi`).
- **Boundary rule** (i16 start, i17 end VERBATIM; i18 mid-token prefix,
  i19 mid-token suffix ABSENT).
- **Case sensitivity** (i20 ABSENT).
- **Verdict order:** i21 26 words + refused URL → TOO_LONG; i22 25 words +
  refused URL → UNREACHABLE (25 is not >25); i24 unregistered id + 26 words →
  NO_SOURCE (NO_SOURCE precedes TOO_LONG).
- **NO_SOURCE:** i23 unregistered id S999, i25 URL-less row S916.
- **UNREACHABLE:** i26 404, i27 application/pdf, i28 302→gopher:// (non-http
  scheme), i29 9 MiB body (>8 MiB), i22 connection refused.
- **URL extraction:** i32 first-of-two URLs wins + `/second` never fetched;
  i33 trailing `.` stripped; i45 trailing `)` stripped; i37 `#sec` fragment
  removed + a server-side check that no `#` reaches the wire.
- **Fetch once per run:** /shared (2 items), /entities (3), /invisible (6) each
  fetched exactly once; plus a ≤2-hits-per-URL bound tolerating the contract's
  one-retry allowance on failures.
- **Fetch discipline:** GET only, UA contains `chousa-quote-reopen`, no
  Cookie/Authorization, no request outside the registry URL set.
- **Output shape:** one line per item in input order, 4 tab-separated fields,
  `QUOTE_REOPEN_SUMMARY` counts + key order; exit 1 on mixed run / 0 on
  all-VERBATIM / 2 on a missing items file.
- **Default registry:** a fake lane (`fakelane/tools/` + `fakelane/corpus/
  SOURCES.md`) runs the tool without `--registry`, exercising the "lane root =
  parent of tools/" rule — the path the frozen counter itself relies on (it
  passes only `--items`).

**Not covered (declared):** the 30 s timeout (the hit bound tolerates one
retry); `application/xhtml+xml`, gzip/deflate, non-UTF-8 charsets, malformed
items rows — uniform or low-risk paths.

## Validation (evidence)

Command shape:
`python3 .ufo/waves/round-29/build/ExecOfflineTest/quote-reopen-offline-test.py -- python3 <cand>.py`

All four candidates live in `candidates/` inside the seat dir; full logs are
`ref_run.txt` and `wrong_*_run.txt` next to the harness:

| candidate | OFFLINE_TEST_PASS | exit |
|---|---|---|
| `candidates/ref_quote_reopen.py` (contract-following reference) | **65/65** | 0 |
| `candidates/wrong_always_absent.py` (always ABSENT) | 21/65 | 1 |
| `candidates/wrong_rawgrep.py` (raw-HTML substring match) | 35/65 | 1 |
| `candidates/wrong_casefold.py` (case-fold, no boundary) | 45/65 | 1 |

Failure shapes are sensible: rawgrep fails markup/script/comment/absent cases;
casefold fails boundary and case checks; always-absent fails every VERBATIM
expectation plus fetch discipline (zero requests recorded). The negative
control proves the harness can fail — always-ABSENT scores 21/65, not 65/65.

## Limits / notes

- Never run against the real tool — none landed yet (`tools/` still holds only
  `research-gate.sh`). The harness is validated only against my scratch
  reference implementation plus three wrong variants.
- "Fetch once per run" is asserted as exactly 1 on successful URLs and ≤2 per
  URL overall (the contract's one-retry allowance applies to failures).
- The default-registry phase only runs when CMD names a readable `.py` file;
  otherwise it prints SKIP (not counted in the total). It copies the script
  into the fake lane, so a tool that relies on sibling files under `tools/`
  may behave differently there — a caveat for imported dependencies.
- A stricter "no fetch before the TOO_LONG verdict" check was intentionally
  not asserted; the contract orders the verdict, not the fetch schedule.
- Note for peers: file changed after an earlier SHA-256 pin
  (`5f963489…5f7f`); current pin is `e09aebdb…989c6` above.

## Tooling

No installs or updates made (stdlib only; Python 3.14.8 present).
