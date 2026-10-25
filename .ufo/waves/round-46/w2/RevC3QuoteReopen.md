# RevC3QuoteReopen — round 46 / wave 2

seat: reviewer (leaf, no dispatch). item: run the lane's quote-reopen tool over the eleven round-46
quotes as an independent second check. **Not run as a binary**: `tools/quote-reopen.py` has no
offline path and this round forbids egress (L0 `8d77e6c1` open). Instead: the tool's code read line
by line, the eleven items assembled in `/tmp`, and a local byte-compare of each quote against its
capture at the recorded offset, evaluated with the tool's *own* `norm`/`html_to_text`/`found`
functions imported from the frozen file (import opens no socket). Base
`d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a`; `git show --name-only d09fc8e7` lists only
`tools/inference-ground.py` under `tools/`, so the verdict rules are the round-29 contract, not
something this round edited. Scratch `/tmp/chousa-r46w2-RevC3QuoteReopen/` removed.

## 1. What the tool would do

`verify()` (`tools/quote-reopen.py:487-532`) per item: look `source_id` up in `corpus/SOURCES.md`
(`registry_rows`/`registry_url`); `NO_SOURCE` if absent; `TOO_LONG` if `norm(quote)` exceeds 25
words (`MAX_WORDS`, `:60`); else one cached `fetch_page(url)` per distinct URL (`:514`).
`fetch_page` (`:444`) calls `_request_once`, whose first steps are `_check_url` (`:217`: http/https
only — no `file://`, no local-source flag) and `_check_address` (`:242`, `:249`: the resolver;
non-global addresses refused). A body is gated on `ctype not in ALLOWED_TYPES` (`:415`) with
`ALLOWED_TYPES = {"text/html", "application/xhtml+xml", "text/plain"}` (`:60`); otherwise text is
`norm(html_to_text(doc))` for HTML, `norm(doc)` for text/plain, and `found()` (`:170`: NFKC, curly
quotes folded, whitespace collapsed, non-alphanumeric boundary) decides `VERBATIM`/`ABSENT`. Exit 0
only if every item is `VERBATIM` (`:532`).

## 2. Why it cannot be used offline — deterministic

No local-document branch exists: `_check_url` admits only http/https (`:217`), `_check_address` is
the only address supplier and needs the resolver, `_dial` opens real sockets, and the `cache`
(`:499`) is an in-process dict keyed by URL, not a disk cache. Every item reaches `fetch_page`,
which returns `None` on any `_Refuse`/transport failure, so `verify` prints `UNREACHABLE` (`:517`).
Expected output under the L0 freeze:

```
QUOTE_REOPEN	<id>	UNREACHABLE	host does not resolve
... (x11)
QUOTE_REOPEN_SUMMARY verbatim=0 absent=0 too_long=0 no_source=0 unreachable=11
```

exit `1` — a **false negative**: the exit code would assert "not re-opened" when only the resolver
failed. No wave-2 seat may read that `1` as evidence.

## 3. Local substitute — per-quote verdict

Item file built to the tool's `ITEM_HEADER` (3 tab-separated columns), ids `S085-1`…`S089-2`,
`source_id` = registry id; the tool's `load_items` accepted all 11 and `registry_url` resolved each
to the same string as `spans.tsv` (five-way equality verified). Offsets are **characters** in
`read_text(encoding="utf-8", errors="replace")`, the quantity `c3-count.py:127` slices; all five
capture digests recomputed and equal to the manifest's `capture_sha256`.

| id | src | slice | context | span | entry | words | `found` |
|----|-----|-------|---------|------|-------|-------|---------|
| S085-1 | S085 | exact | 80+23+80 | yes | yes | 5 | true |
| S085-2 | S085 | exact | 80+46+80 | yes | yes | 6 | true |
| S086-1 | S086 | exact | 80+44+80 | yes | yes | 7 | true |
| S086-2 | S086 | exact | 80+16+80 | yes | yes | 3 | true |
| S086-3 | S086 | exact | 80+19+80 | yes | yes | 4 | true |
| S087-1 | S087 | exact | 80+38+80 | yes | yes | 2 | true |
| S087-2 | S087 | exact | 80+23+80 | yes | yes | 2 | true |
| S088-1 | S088 | exact | 80+38+80 | yes | yes | 7 | true |
| S088-2 | S088 | exact | 80+55+80 | yes | yes | 10 | true |
| S089-1 | S089 | exact | 80+42+80 | yes | yes | 4 | true |
| S089-2 | S089 | exact | 80+33+80 | yes | yes | 5 | true |

Every quote is unique in its capture (`ct.count(quote) == 1`, 11/11), so the recorded offset is not
one of several candidates. Verdict: **11/11 local VERBATIM-equivalent**, re-derived twice (current
tree and a `--root` copy of the frozen tree). Counters re-run, verbatim: `c3-count.py` →
`ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11
CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=PASS` exit 0, and `--lane-only` the same with
`CAPTURE_BOUND=skipped`, exit 0; `c1-count.py` → `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3
C1=PASS` exit 0; `c2-count.py --list` → `ENTRY_POINTS=73 (tools=8 counters=50 named=71)
GATES_ROWS=35 REGISTERED=73/73 UNREGISTERED=0 C2=PASS` exit 0.

## 4. Findings

### F1 — Medium — calibration: half these quotes cannot be re-opened by the registered tool even with network

The captures have `.raw` sidecars: `file -b` says `PDF document, version 1.5` for
`1c15b611118dee97e4105fcf.raw` (S086, magic `%PDF-1.5`) and `JSON text data` for
`7800e2e1e2df3bc124b6b83e.raw` (S087). `ALLOWED_TYPES` (`:60`) holds neither, so:

- **S086 ×3** — `application/pdf` ⇒ `UNREACHABLE` at `:415`; and had the server announced
  `text/plain`, the tool would decode PDF bytes as text and `found()` returns **false** for all
  three (measured with the imported `found`), because the text sits in compressed streams. S086 can
  **never** be `VERBATIM` through this tool, on any header.
- **S087 ×2** — bytes are a JSON API body: `application/json` ⇒ `UNREACHABLE`; only a `text/plain`
  label yields `VERBATIM` (`found` true on the decoded JSON). The capture records bytes, not
  headers, so the header value is `[INFERENCE]`; the bytes are not.

Measured on the raw bytes through the tool's own pipeline: S085, S088, S089 (HTML) → true 6/6;
S086 → false 3/3; S087 as text → true 2/2. Net: **6/11 reachable-and-`VERBATIM`, 3/11 impossible,
2/11 header-dependent.** `SKILL.md:71` requires every cited web quote to be re-opened with this tool
*and every non-`VERBATIM` verdict recorded*; no `VERBATIM`/`UNREACHABLE` verdict appears anywhere in
`corpus/evidence/round46/`, `corpus/lessons/round-46.md` or `.ufo/waves/round-46/w1/` (grep; only
`ScribeGatesR33R34.md` discusses the r30 harness). The round substitutes a capture-slice check — a
**sounder instrument for the PDF** — but records it nowhere as a tool limit, so C3's "re-opened this
round from the on-disk captures" reads as if the registered instrument had run. Fix: one C3 limit
line naming the three-type gate, the capture method as the substitute, and S086 as the case where
the substitute is strictly stronger. C3's substance is unharmed; this is calibration honesty.

### F2 — Medium — calibration: C3's coverage is a count, not a cover

`c3-count.py:148/153` require `len(rows) == N_QUOTES`; `CITES_BOUND` (`:142`) checks the five
`source:` lines only. Nothing ties a bound source to a span row. Mutation on a copy of the frozen
tree (`git archive d09fc8e7 | tar -x`, then rewrite `spans.tsv`): drop both S089 rows, duplicate the
S085-1 row twice → still 11 rows → every line identical (`… QUOTE_ROWS=11/11 … CAPTURE_BOUND=11/11
C3=PASS`), exit 0. A manifest that never re-opens one of the five bound sources therefore passes
every leg. The live tree is complete (S085×2, S086×3, S087×2, S088×2, S089×2), so this is not a
live false pass; it is a prospective hole, and the claim's "each cited source is re-opened this
round" is enforced only by a human reading it. Not mine to re-scale — recorded per the seat
contract. Next-round tightening: require ≥1 row per bound source, or freeze the (source, quote) set
instead of its cardinality.

### F3 — Low — two sources of truth for "which document"

`c3-count.py` keys the capture by the `url` column of `spans.tsv`; `quote-reopen.py` resolves the
URL from the `SOURCES.md` cell of `source_id`. All five agree today (string equality, S085–S089),
so nothing is wrong; but a registry URL edited after the freeze would silently point the tool at a
different page while the counter keeps the old pin, and both could look consistent.

### Verified positives (could have failed; did not)

- The registry's own `char N` anchors are **exact** — no counter checks them: 2349 (S085); 6737,
  6784, 20847 (S086); 171 (S087); 3909, 2891, 2904 (S088); 7084 (S089). Each slice equals the
  quoted text at that character, including the post-fix S088 pair (2891 = `claim_date :`, 2904 =
  the quote), so `corpus/lessons/round-46.md` item 7's fix verifies against the bytes. S087's
  `1,713,485,474` sits at 4962, 33 chars past the row's `(char 4929)`, but 4929 is the
  `"key": "wiki-pages.zip"` quote start and the size is inside that same 183-char span — not wrong.
- Span lengths 176–215 against quotes of 16–55: context is exactly 80/80 on all eleven, so the
  `entailed-leg` lesson (item 11) is genuinely closed.
- All eleven quotes ≤10 words, so `TOO_LONG` cannot mask an `ABSENT`; capture digests all equal.

## Residual risk / verification gaps

- No page fetched and the binary never run (instruction + L0 `8d77e6c1`): drift between capture and
  now is unmeasured, so the pipeline result is a verdict **modulo drift**, not a live `VERBATIM`.
- Captures hold bytes, not headers, so the S086 `UNREACHABLE`-vs-`ABSENT` split and the S087
  `VERBATIM`-vs-`UNREACHABLE` split cannot be pinned offline; S086 is non-`VERBATIM` either way.
- Row truth (does each span carry the entry's inference) is C3's named limit and other seats'; I
  judged quote location, uniqueness, and what the counter enforces only. C1/C2 were re-run for tree
  state, not judged beyond their exit codes.
