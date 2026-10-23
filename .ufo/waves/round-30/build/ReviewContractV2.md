# ReviewContractV2: tool contract v2 against HTML 5.2 "in head" and sentinel T1/T4

Seat: ReviewContractV2 (reviewer, leaf). Judged on coverage and operability. Scope: findings only on
`corpus/evidence/round30/claims.md` "Tool contract v2" (lines 189-211). I read the frozen claims
file, `.ufo/waves/round-29/falsify/SentinelTool.md` (T1, T4), `c1-count.py`, `c2-count.py`,
`qr_harness.py`, `tools/quote-reopen.py` and the CPython 3.14.8 stdlib. I edited no lane production
file, counter, harness or claims file, and ran no git or jj write command. I installed and updated
nothing.

Spec page opened (access date 2026-10-23):
`https://www.w3.org/TR/2017/REC-html52-20171214/syntax.html`. It answered HTTP 200 with no redirect,
4415303 bytes, sha256 `1db65aefdde4f6a728aefde0069110eac400814be988ad4259a38800fb25e141`, and its page
heading is "HTML 5.2 W3C Recommendation, 14 December 2017". Sections used: 8.2.5.4.4 "in head"
(`#the-in-head-insertion-mode`), 8.2.5.4.5, 8.2.5.4.6 and 8.1.2.4 "Optional tags". The text extract is in
`.ufo/waves/round-30/build/ReviewContractV2/sections.txt`. Why I used this URL instead of the named one
is in finding 13.

## Findings, by severity

### High

**1. The TLS half of item 3 is exercised by neither counter, yet every registry row uses it.**
Item 3 (claims.md:205-209) requires that "the host name is still used for the `Host` header and for TLS
(SNI and certificate check)" while the connection goes to a pinned address. Every URL that either
counter generates is `http://`: `c1-count.py:242,254` and `c2-count.py:152,159`. The harness server is
plain TCP only (`qr_harness.py:133-152,265`). Meanwhile all 40 `S…` rows in `corpus/SOURCES.md` carry
an `https://` URL, and none is http-only (measured with `grep -c`).

So a candidate can pin the address in a way that breaks HTTPS and still print 27/27 and 106/106. Two
ways it could do so [INFERENCE]: pass the IP to `HTTPSConnection`, so the certificate is checked
against the IP, or disable `check_hostname`. This is not listed under "Not claimed" (claims.md:213-222).

- Smallest repair: add "TLS with a pinned address" to Not claimed.
- First falsifier for the falsify wave: a loopback TLS server with a throwaway CA that asserts the SNI
  value and the certificate name.

### Medium

**2. The time spent resolving names is not bounded, and the counter cannot observe it.**
Item 2 (claims.md:201-204) lists "every redirect hop, header read, body read and the one retry". It
does not name resolution or TCP connect. The harness `fake_gai` answers instantly from the map
(`qr_harness.py:60-87`), so no item in the counter measures resolver latency. CPython's
`socket.getaddrinfo(host, port, family=0, type=0, proto=0, flags=0)` takes no timeout
(`/usr/lib/python3.14/socket.py:972`).

I measured this in a private network and mount namespace (`unshare -rmn`) with a silent DNS sink on
127.0.0.1:53 and a bind-mounted `hosts: files dns`, so no packet could leave the box.

| resolver options | command | result |
|---|---|---|
| default (`nameserver 127.0.0.1`) | `getaddrinfo` under `setdefaulttimeout(0.5)` | `wall=10.01s result=gaierror -3 dns_packets=4` |
| default | round-29 `fetch_page` with `DEADLINE=1.0` | `wall=10.01s detail='host does not resolve'` |
| `timeout:2 attempts:1` | both of the above | `wall=2.00s` each |

The commands were `timeout 120 unshare -rmn sh -c '… python3 probe_dns_time.py'`, exit 0 both times.
The script is `ReviewContractV2/probe_dns_time.py`.

- The round-29 tool charges resolution to the deadline clock (`tools/quote-reopen.py:331` starts the
  clock; the lookup at 270 precedes the check at 271-273), but it cannot interrupt the lookup.
- Smallest repair: say whether resolution counts toward `DEADLINE`. If it does not, list resolver
  latency under Not claimed. Meeting "bounds the whole fetch" for resolution needs the lookup to run
  under its own budget, for example a worker thread joined with the remaining time [INFERENCE].

**3. "Global" is undefined in item 3; under Python's `is_global`, some non-public addresses pass.**
Item 3 says "If any returned address is not global" (claims.md:205-206). I measured these values on
Python 3.14.8:

- `is_global` is True for:
  - `64:ff9b::7f00:1` (NAT64 wrapping 127.0.0.1) and `64:ff9b::a9fe:a9fe` (wrapping 169.254.169.254)
  - `fec0::1` (deprecated site-local)
  - `ff02::1`, `ff0e::1` and `224.0.0.1` (multicast)
  - `192.88.99.1`
- `is_global` is False for `::ffff:127.0.0.1`, `2002:7f00:1::1`, `fe80::1` and `100.64.0.1`.

SentinelTool.md:173-179 already named NAT64 and multicast. Contract v2 neither defines "global" nor lists
this residue. On a NAT64 network, the `64:ff9b::` form reaches the metadata address [INFERENCE: no
NAT64 route here to test].

**4. IPv6 is entirely outside the C2 harness.**
`global_addrs` generates IPv4 only (`qr_harness.py:270-277`). No name map in `c2-count.py:133-157`
holds an AAAA-style answer. Any AF_INET6 connect is refused (`qr_harness.py:104-105`). So for AAAA
answers, the following parts of item 3 are untested: which address family to pick, scope ids,
IPv4-mapped addresses, and falling back from IPv6 to IPv4. A tool that resolves AF_INET only would pass.

### Low

**5. Item 3 does not say how a connect failure moves between validated addresses.**
"the connection goes to one of those validated addresses" (claims.md:207) leaves open:

- whether a connect failure may try the next validated address;
- whether that fallback shares `DEADLINE`.

`socket.create_connection` sets the full `timeout` on each address in turn (`socket.py:850-858`), so
setting the timeout once costs up to the number of addresses times `timeout`. The harness refuses
unrouted destinations at once (`qr_harness.py:96-98`) and never black-holes one, so the counter cannot
see connect time. Multi-address items route both addresses (`c2-count.py:140-142`).

**6. TLS handshake time is not listed in item 2, though this runtime bounds it when the timeout is set.**
I tested on loopback against a server that drips a 16 KiB TLS record after a 5-byte record header. The
runtime was CPython 3.14.8 with OpenSSL 3.6.5.

- With a socket timeout of 2.0 s and a 0.05 s drip, the handshake ended with `TimeoutError@2.01s`.
- With a timeout of 1.0 s and a 0.2 s drip, it ended at 1.00 s.
- A control `makefile("rb").read(16384)` under the same 0.2 s drip was still running at the 6.00 s
  cap. This is the T4 shape.

So the handshake stays inside `DEADLINE` if and only if the socket timeout is at most the remaining time
before `wrap_socket`. The contract leaves this implicit, and the counter has no TLS (finding 1). Scripts:
`ReviewContractV2/probe_tls_drip.py`, plus the inline control run, exit 0.

**7. Item 2's wording "stops" has no tolerance, but the predicate grants one.**
Item 2 says "When it passes, the fetch stops" (claims.md:203). The predicate allows
`DEADLINE + SLACK`, with `SLACK = 1.5` (`c2-count.py:68,160`; claims.md:148-153). A tool that stops at
`DEADLINE` + 1.4 s meets C2 while breaking a literal reading of item 2. Smallest repair: say "within
1.5 s of `DEADLINE`", or state that the slack is the measurement tolerance.

**8. Redirect host-set confinement was rejected implicitly.**
SentinelTool.md:163-171 suggested confining redirects to the registry host set. The rebind-redirect
items need a cross-host redirect to be followed (`c2-count.py:147-155`, with a fair-coin VERBATIM or
ABSENT label). So that hardening would score a miss. This is a design decision that is not written in
the contract.

### Item 1 (C1 head boundary) against HTML 5.2

**9. Item 1 matches the spec on every shape the counter generates.**
I imported the frozen `c1-count.py` `build()` read-only (with `PYTHONDONTWRITEBYTECODE=1`) for seeds 1
to 10, giving 200 documents. I compared a literal implementation of item 1 on `html.parser` with
Chromium 154.0.8037.97 `DOMParser`, run headless inside `unshare -rn` with no network.

- Output: `{"generated_docs": 200, "head_equal": 200, "seeds": [1, …, 10], "text_equal": 200}`.
- Command: `timeout 300 python3 probe_item1.py`, exit 0. Output file:
  `ReviewContractV2/probe_item1.out`.
- Text agreed on all 200 documents, and so did the list of head elements.

The 11 names in item 1 (claims.md:193-194) are exactly the spec's in-head start-tag rows. The spec
quotes: 'A start tag whose tag name is one of: "base", "basefont", "bgsound", "link"', followed by the
rows for "meta", "title", "noscript", "noframes", "style", "script" and "template" (8.2.5.4.4).

No listed head-content element is wrong.

**10. Item 1 diverges from the spec in cases the counter never generates; all of them leave the extracted text unchanged.**

- (a) Spec: 'A start tag whose tag name is "html"' / 'Process the token using the rules for the "in
  body" insertion mode.' The `<head>` start tag row ends in "Parse error." Neither ends the head, but
  item 1's "any start tag other than …" does. Probe `html-starttag-in-head`: item 1 head `[]`,
  Chromium head `['title']`, text equal.
- (b) Spec: 'An end tag whose tag name is one of: "body", "html", "br"' / 'Act as described in the
  "anything else" entry below.' These end tags close the head; item 1 names only `</head>`. Probes
  `br-endtag-in-head` and `body-endtag-in-head`: head and text equal.
- (c) Spec whitespace is the ASCII set: 'A character token that is one of U+0009 CHARACTER TABULATION,
  U+000A LINE FEED (LF), U+000C FORM FEED (FF), U+000D CARRIAGE RETURN (CR), or U+0020 SPACE'. Item 1
  says only "not only whitespace", and Python's `str.strip()` also strips VT and NBSP. Probes
  `nbsp-then-p` and `vt-then-text`: text equal after `norm()`.

Why the text is unaffected: under item 1, any non-whitespace character data ends the head. A late end
can therefore hide text only inside a listed element whose content is not in the drop list, which
leaves only `noframes` (finding 12). An early end only moves whitespace. The counter generates none of
these tokens (`c1-count.py:146-180`), and item 1 itself says the boundary cannot be observed on these
documents (claims.md:196-200). The skip-nothing control agrees: it scored 86/106 by missing every title
window (`controls/CtlParseShortcuts.md:8,65`).

**11. Item 1 assumes scripting is enabled, but never says so.**
Spec: 'A start tag whose tag name is "noscript", if the scripting flag is enabled' means raw text. With
the flag disabled, noscript content that is not head content ends the head. Two parsers gave different
results:

- `DOMParser` (scripting disabled), probes `noscript-p-in-head` and `noscript-text-in-head`: Chromium
  put "Ns text" and "Plain ns" into the body, while item 1 drops them.
- Chromium iframe `srcdoc` (scripting enabled; `ReviewContractV2/ns.out`): head `['noscript','title']`
  and `['noscript']`, body text "Body two" and "Body fourteen", equal to item 1.

The round-29 parser uses the stdlib default `scripting=False` (`tools/quote-reopen.py:79`;
`/usr/lib/python3.14/html/parser.py:137-149`), so tags inside noscript are tokenized. A literal "any
start tag" scan would then end the head at a `<p>` inside `<noscript>`. That does not change the text,
because noscript content is dropped. Smallest repair: one clause, "parsed as with scripting enabled".

**12. "HTML allows only text-dropping or empty elements in `head`" (claims.md:197) is not true of `noframes`.**
`noframes` is in item 1's head list but not in its drop list (claims.md:193-195). The spec parses it
in head as raw text ('A start tag whose tag name is one of: "noframes", "style"' / 'Follow the generic
raw text element parsing algorithm.'). Probe `noframes-in-body`: item 1 keeps "Nf body", and so does
the round-29 tool. Whether browsers render it is in the rendering section, which I did not open
[INFERENCE: hidden]. The counter's scoped equivalence still holds because the counter never emits
`noframes`.

**13. The named spec URL no longer serves HTML 5.2; the dated Recommendation URL should be cited instead.**
`curl -I -L https://www.w3.org/TR/html52/syntax.html` showed `HTTP/2 301 location:
https://www.w3.org/TR/html/syntax.html`, then `HTTP/2 307 location:
https://html.spec.whatwg.org/multipage/syntax.html`, then `HTTP/2 200`. That final page is the WHATWG
Living Standard, titled "HTML Standard" and "Last Updated 22 October 2026". It is not HTML 5.2 and it is
not on www.w3.org, although claims.md:128-131 promises a www.w3.org row. A row citing the undated URL
would resolve off-host.

- The dated URL above answers 200 on www.w3.org with no redirect. Cite it in `SOURCES.md`.
- Spec text note: in HTML 5.2, the in-head `head` start-tag row reads only "Parse error.", with no
  "Ignore the token.".

**14. "which HTML allows" (claims.md:97-98) is loose for the counter's own documents.**
The spec says (8.1.2.4): "A head element’s end tag may be omitted if the head element is not
immediately followed by a space character or a comment." Every headless document in the counter puts
`\n` right after the last head element: `c1-count.py:180` joins parts with `"\n"`, and 166 adds another
for headless-text. So all 14 headless documents are non-conforming as authored. The parse is still well
defined (the first in-head row: "Insert the character."), so the text is unchanged. This is wording
only.

### Do items 2 and 3 close T1 and T4 as described?

**15. T1 is closed as described for IPv4 over plain HTTP.**
Item 3 forbids a second lookup and forbids checking "only after connecting" (claims.md:207-209). That
is stronger than the sentinel's smallest remediation, a `getpeername` re-check (SentinelTool.md:181-187),
which would still open a TCP connection to loopback. The counter enforces this:

- The harness logs every connect destination before it routes the connection (`qr_harness.py:89-98`).
- Rule (c) fails any destination outside the routed set (`c2-count.py:166-170`).
- The rebind-loop, rebind-private and rebind-redirect items reproduce the sentinel's `dns_rebind.py`
  and `ssrf_chain.py` (SentinelTool.md:123-148).

The contract does not say whether the single retry may resolve again. Either choice is safe, because a
second harness lookup returns the rebinding answer (`qr_harness.py:75-78`), which is validated and
refused. The parts that stay open are findings 1, 3 and 4.

**16. T4 is closed as described on the plain-HTTP path.**
Item 2 names the header read and the body read, and says "A slow but steady sender cannot extend it"
(claims.md:202-204). That covers all three overruns the sentinel measured: a 1 B/s body that took
40.1 s, a 1 B/2 s body still running at 70 s, and a header dribble that took 50.6 s
(SentinelTool.md:268-273). The counter's drip-head, drip-body, drip-steady and stall-body items
(`c2-count.py:30-35`; `qr_harness.py:231-251`) exercise each shape. The parts that stay open are DNS
time (finding 2), connect time (finding 5) and the TLS handshake (finding 6).

## Residual risk and verification gaps

- I did not run either frozen counter: this was a contract review, and no candidate tool exists yet.
- The Chromium comparison uses the WHATWG-era parser in Chromium 154 as a stand-in for HTML 5.2. For
  the in-head rows quoted above, the two texts agree [INFERENCE: I did not diff them line by line].
- The DNS and TLS timings come from this host only: Python 3.14.8, OpenSSL 3.6.5, glibc resolver in a
  namespace.

Network disclosure:

- My first fetch, `curl -sS -L https://www.w3.org/TR/html52/syntax.html`, followed the redirect chain
  in finding 13. It made one GET to `html.spec.whatwg.org`, and the follow-up `curl -I -L` made one
  HEAD there. That host is outside the allowed set.
- I used that page's bytes (89196 bytes, sha256 `0128a08f…648f`) for no finding, only to show the
  redirect, and deleted them.
- Every other request was the one GET to the dated www.w3.org URL, or loopback or namespace traffic.

Files: this report, plus probes and outputs in `.ufo/waves/round-30/build/ReviewContractV2/`
(`probe_item1.py`, `probe_item1.out`, `ns.out`, `probe_tls_drip.py`, `probe_dns_time.py`, `nsswitch.probe`,
`resolv.probe`, `resolv.default`, `sections.txt`). Scratch copy: `/fast/scratch/hyaku/chousa-r30/w1/ReviewContractV2/`.
No process I started is still running. The remaining Chromium processes belong to the user's desktop
session.

Report: .ufo/waves/round-30/build/ReviewContractV2.md
