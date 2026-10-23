# SimplifierTool — YAGNI review of `tools/quote-reopen.py` (440 lines)

Seat: SimplifierTool (leaf, no subagents). Judged on: operability.
Target: the landed `tools/quote-reopen.py` at lane commit `30c9d24d`
(SHA-256 `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea`),
reviewed against the frozen contract (`corpus/evidence/round29/claims.md`) and
the sentinel hardening (`.ufo/waves/round-29/build/SentinelFetchBounds.md`,
findings T1–T7). Lane files were not edited; the lane tool SHA above was
re-measured after all work and is unchanged. A proposed diff is at
`.ufo/waves/round-29/falsify/SimplifierTool/quote-reopen-cuts.patch`, produced
against a scratch copy at `/fast/scratch/hyaku/chousa-r29/w2/SimplifierTool/lane`.

## Verdict: HOLDS (within this scope)

Nothing cut or flagged affects the 130/130 measurement: every deletion is dead
code, a redundant exception name, a duplicated probe, or a verbatim-equivalent
rewrite, and the shortcut scan found no fixture/label/receipt/counter reads.
The claim's tool is a real implementation of the frozen contract, not weight
carrying hidden authority — but it carries about 13 lines of dead or
duplicated weight and one latent cache-key defect.

## Shortcut scan (negative — clean)

- `grep -nE 'fixture|labels|c1-count|c1_count|receipt|\.ufo|seed|random|QUOTE_REOPEN_MATCH' tools/quote-reopen.py` → **no matches**.
- Only two `open()` calls: the registry (`registry_rows`, line 131) and the
  items file (`load_items`, line 353). No read of `labels.tsv`, no receipt
  files, no counter import, no embedded URLs or ids.
- The url cache (line 397) is keyed by the registry URL, not by item id or
  item order; verdicts come from `found(text, quote)` over fetched text.

## Deletions in the proposed diff (440 → 427 lines, 30/30 selftest OK)

Patch tested in scratch: `python3 -m py_compile` clean and the wave-1
ExecTool `selftest.py` (30 cases incl. the live S044 fetch) → `OK` before
**and** after the patch.

| lines | what | why unneeded |
|---|---|---|
| 294 | `resp.read(0)` before redirect `continue` | reads zero bytes; dead no-op (−1) |
| 332, 334 | `detail = ""`, `retryable = False` | both rebound on every path before any use (−2) |
| 339–340 | `http.client.InvalidURL`, `ssl.SSLError` in the fetch except-tuple | `InvalidURL` ⊂ `HTTPException`, `SSLError` ⊂ `OSError`; same catch set (−0) |
| 348 | `return None, None, None, detail or "fetch failed"` | unreachable: the loop body's last `if` returns whenever the loop can fall through (−1) |
| 373–375 | `resolve_registry` probe of `LANE/arg` and `LANE/corpus/arg` | contract: `--registry` names the file; the probe silently substitutes a different file than the one passed (−3) |
| 385, 410–411 | `out` list + second print loop | item lines are order-independent of fetch order; print in the same loop (−2 net) |
| 402 | `detail = detail or "unreachable"` | dead fallback: `fetch_page` always returns a non-empty detail when `text` is None (−1) |
| 412 | `detail.replace("\t", " ")` | every detail is a tool-built literal; none can contain a tab (−0) |
| 429–431 | `if args.command != "verify"` usage block | `add_subparsers(required=True)` gives identical exit-2 semantics (−3 net with the +1 at 421) |
| 434 | `UnicodeDecodeError` in the I/O except-tuple | ⊂ `ValueError`; same catch set (−0) |
| 397–399 +402 | cache keyed by unstripped `url` + dead fallback | replaced by `key = url.split("#", 1)[0]` (see defect below) (+1 line for the key; −3 net here incl. fallback) |

Sum: 440 → 427 lines, −13 net. No constant, table (`SKIP`, `BLOCK`, `QMAP`),
or hardening function is touched: `_check_url`, `_check_address`,
`_read_response`, `_inflate_stream`, the redirect hop checks and the deadline
plumbing all implement contract clauses or T1–T7 and stay.

## Latent defect found while cutting (1)

**Fetch-once bound vs fragment cache key (contract fetch bounds).** The
contract removes the fragment before fetching; `fetch_page` strips it at line
330, but `verify` caches by the *unstripped* `url` (line 397). Two registry
URLs differing only in fragment would each be fetched — more than once per run
for the same fetched target. Latent today: exactly one registry URL carries a
fragment (S046, `#text-quote-selector`); measured 130/130 unaffected. The
patch keys the cache by the stripped URL (−0 net, correctness repair).

## Flagged but NOT in the diff (candidates / tradeoffs)

- **`norm(quote)` computed twice per item in `verify`** (lines 393, 395) plus
  once inside `found` (line 114): harmless duplicate work; hoisting adds a
  name for ~0 line gain. Skipped.
- **Tool-side `_Text`/`norm`/`found`/`QMAP`/`BLOCK`/`SKIP` duplicate the
  counter's reference functions** (tool 58–125 vs counter 63–112). This is
  deliberate contract parity — the labels are defined by those functions — so
  it is a second authority by design, kept.
- **`_inflate_stream`'s raw-deflate retry and `"zlib"` encoding arm**
  (lines 213–229): the contract and counter (`zlib.decompress` only) need just
  the zlib wrapper for `deflate`; the raw-1951 retry and `zlib` token cover
  servers that mislabel. ~10 optional lines; kept because removing them only
  narrows tolerance, gains nothing measurable.
- **Unsupported `Content-Encoding` is reported as "body over 8 MiB"**
  (lines 213–214 → 305–306): verdict (UNREACHABLE) is right, the detail string
  is wrong. Cosmetic.
- **`load_items` tolerates CRLF** (lines 355, 359) and `rows.setdefault`
  keeps the first row on a duplicate id (line 141): tiny tolerances the
  contract does not demand; harmless, kept.
- The `for _ in range(MAX_REDIRECTS + 1)` hop cap, `handle_startendtag`,
  `Accept-Encoding: gzip`, and the socket re-arm in `_read_response` all have
  sentinel or counter-parity justification; not weight.

## Evidence and limits

- Ran: `timeout 300 python3 selftest.py` from the scratch lane → `Ran 30
  tests ... OK` on the pristine copy and on the 427-line cut copy.
- `sha256sum tools/quote-reopen.py` after all work →
  `72a3ad47...54fea`, identical to the landed hash; `git status --porcelain
  tools/` empty. No git/jj write command run; nothing outside my falsify dir
  and my scratch dir was written.
- Limits: the cut copy was validated by the 30-case contract selftest only —
  I did **not** re-run the frozen 130/130 counter on it (that is a
  re-measurement for whoever applies the diff). The `resp.read(0)` and tail-
  return dead-code proofs are by control-flow reading plus the selftest, not
  by a coverage tool.

## Installs

None. Only the Python 3.14.8 standard library already on the host was used.

Report: .ufo/waves/round-29/falsify/SimplifierTool.md
