# Draft source row

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0NN | Python ipaddress documentation — https://docs.python.org/3/library/ipaddress.html | docs | A | Python `ipaddress.is_global` classification of global reachability; not DNS resolution or connection pinning | `IPv4Address.is_global` section; Python 3.15.1 documentation served 2026-10-23 | Treat `is_global` as an IANA special-registry global-reachability predicate, accounting for the documented IPv4-mapped IPv6 and shared-address-space exceptions | mined | 2026-10-23 | on-release | corpus/knowledge/quote-reopen-r30.md |

Located quote (21 words): “`True` if the address is defined as globally reachable by [iana-ipv4-special-registry] (for IPv4) or [iana-ipv6-special-registry] (for IPv6) with the following exception:” — `IPv4Address.is_global`, https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Address.is_global (opened 2026-10-23).

Limits in the opened section: IPv4-mapped IPv6 uses the underlying IPv4 `is_global` semantics; `is_global` is opposite `is_private` except that `100.64.0.0/10` is neither; the page notes false-positive and false-negative fixes in Python 3.13. The page defines the address predicate, not DNS lookup count or connection pinning. Supports claim C2, tool contract v2 item 3 only.
