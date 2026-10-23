VERDICT: pass — S056 quote verbatim at the named section and the landed tool verifies it VERBATIM.

(1) Quote check.
- URL opened once (GET): https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Address.is_global
- Command: `timeout 60 curl -sS -X GET --max-time 50 -o ipaddress.html -w 'HTTP=%{http_code} SIZE=%{size_download}\n' '<url>'` → `HTTP=200 SIZE=146106`, exit 0.
- Located under `id="ipaddress.IPv4Address.is_global"` in the served page; the definition sentence reads verbatim: "True if the address is defined as globally reachable by iana-ipv4-special-registry (for IPv4) or iana-ipv6-special-registry (for IPv6)". 17 words (≤ 25). No page-change drift.
- Row cells vs page: tier `docs` = Python documentation page; scope (is_global classification of global reachability, not DNS resolution or connection pinning) = page states only the property and its exceptions (IPv4-mapped IPv6, 100.64.0.0/10), nothing about DNS or pinning; teaches cell = page text confirms IANA special-purpose registry basis and the two documented exceptions. Cells say no more than the page.

(2) Tool check.
- Tool SHA-256 `47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201` matches the frozen landed revision 49b2aa3; lane tip a9d3a05a8fd812a60323b08381019152069581fd (read-only git log).
- One-item TSV at .ufo/waves/round-30/falsify/AttackRowS056/items.tsv (header `id<TAB>source_id<TAB>quote`, item S056/S056/quote). First run without the header exited 2 (`quote-reopen: ValueError`); the tool requires the documented header — corrected, never a tool defect.
- `timeout 120 python3 tools/quote-reopen.py verify --items .ufo/waves/round-30/falsify/AttackRowS056/items.tsv` from the lane root → `QUOTE_REOPEN	S056	VERBATIM	matched in normalized page text`, `QUOTE_REOPEN_SUMMARY verbatim=1 absent=0 too_long=0 no_source=0 unreachable=0`, exit 0.
- No finding: verdict is VERBATIM.

Frozen counter SHAs verified: c1-count.py 5b312d84…d6e6, c2-count.py 0a59e373…f88f, qr_harness.py e2be0dd1…50d4, all matching claims.md.
