VERDICT: pass — S053 quote is verbatim (22 words) at the socket.create_connection section; landed tool verify returns VERBATIM, exit 0.

## (1) Source row S053 vs page
- Row (SOURCES.md:63): kind docs, tier A, anchor "section socket.create_connection, Python 3.15.1 documentation"; scope "documented create_connection behavior for a host name; not a guarantee of DNS pinning or per-hop validation"; teaches "create_connection resolves a host name itself and tries each address, so an earlier address check does not pin the later connection".
- Page opened once: `timeout 90 curl -sS -o .../socket.html -w 'HTTP=%{http_code} BYTES=%{size_download}' https://docs.python.org/3/library/socket.html` → HTTP=200 BYTES=309740; file SHA-256 54e4bac8…3e2203. Anchor `id="socket.create_connection"` present (grep match, offset 110506).
- Quote verbatim: extracted the `<dt>…<dd>` block after the anchor, stripped tags, collapsed whitespace. The page text contains exactly: "it will try to resolve it for both AF_INET and AF_INET6, and then try to connect to all possible addresses in turn until a connection succeeds." Gate quote = first 22 words (`len(q.split())==22` ≤ 25), contiguous and character-identical.
- Cells vs page: scope positive part states exactly the documented behavior (non-numeric hostname resolved for both AF_INET and AF_INET6, all addresses tried in turn); the negative clause matches the page's silence on pinning/per-hop. teaches first clause is page text; the "earlier address check does not pin" clause is the direct consequence of in-function resolution [INFERENCE], no extra claims. Tier A docs consistent with sibling docs rows (S052/S054–S056).

## (2) Landed tool run
- Tool hash `sha256sum tools/quote-reopen.py` → 47a657e7…222a1201 (matches frozen claim); tip a9d3a05a…69581fd; tool last commit 49b2aa30…c21405d (unchanged).
- Item TSV written to .ufo/waves/round-30/falsify/AttackRowS053/items.tsv: header `id\tsource_id\tquote`, one row `t1\tS053\t<quote>`. `cat -A` confirms single tabs, no stray chars.
- Run from lane root: `timeout 120 python3 tools/quote-reopen.py verify --items .ufo/waves/round-30/falsify/AttackRowS053/items.tsv` →
  `QUOTE_REOPEN t1 VERBATIM matched in normalized page text`
  `QUOTE_REOPEN_SUMMARY verbatim=1 absent=0 too_long=0 no_source=0 unreachable=0`
  EXIT=0. MAX_WORDS=25 (quote 22 words, so not TOO_LONG).
- No non-VERBATIM finding; no tool installs made (curl/python3 pre-existing).
