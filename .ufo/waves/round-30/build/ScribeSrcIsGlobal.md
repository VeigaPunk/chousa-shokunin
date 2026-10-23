# Scoped findings
- Opened https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Address.is_global once via `read`; page returned Python 3.15.1 docs, accessed 2026-10-23.
- Located quote (21 words), `IPv4Address.is_global`: “`True` if the address is defined as globally reachable by [iana-ipv4-special-registry] (for IPv4) or [iana-ipv6-special-registry] (for IPv6) with the following exception:”
- Draft 11-cell row and quote: `.ufo/waves/round-30/build/ScribeSrcIsGlobal/row.md`; `corpus/SOURCES.md` was not edited.
- Verdict: scoped support for C2, tool contract v2 item 3 (global-address predicate), not proof of DNS-once/connect-pinning behavior or the full C2 predicate.
- Limits: the docs preserve IPv4-mapped IPv6 semantics, note the `100.64.0.0/10` exception, and record false-positive/negative fixes in Python 3.13; knowledge entry `corpus/knowledge/quote-reopen-r30.md` was not found, so `mined`/`used-by` remain draft pending its citation.
- Gates and scope: no counters, harness, candidate tool, or network behavior tested; no install. No C1 or contract items 2/4 finding.
- Touches: `row.md` and this report only. `timeout 10s mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-30/build/ScribeSrcIsGlobal` returned no output; exit code was not exposed. No other shell command ran.
