# ScoutSentinelT1T4 — does the C2 counter cover every attack shape SentinelTool measured?

Seat: ScoutSentinelT1T4 (scout, leaf, no subagents). Lane: `chousa-shokunin`. Read-only.
Question: map the round-29 sentinel findings T1 (DNS rebinding) and T4 (slow-drip) in
`.ufo/waves/round-29/falsify/SentinelTool.md` onto the item kinds of the frozen C2 counter
`corpus/evidence/round30/c2-count.py` (design v3, `PLAN` at lines 73-80, `build` at 110-161,
`score` at 164-175) and its harness `qr_harness.py` (bootstrap 39-128, server 133-265).
Report whether every described attack shape has a counter item, and name shapes that do not.

## Short answer

**Yes for the two findings C2 claims**: every attack shape inside T1's rebinding core and
T4's drip core has at least one item kind, and the label/side conditions match. **No for the
edges around them**: T1's IPv6 rebinding answer (`::1`), rebind to link-local/metadata
(`169.254.169.254`), NAT64/multicast residuals, and T4's never-answers baseline have no
items; and several contract-adjacent shapes (TLS handshake, drip on a redirect hop,
retry-shared deadline, per-hop provenance, connect-phase stalls, IPv6 routing) are outside
the counter's item space. Each gap is cited below with whether it matters for the claim.

## T1 — the shapes the sentinel described, mapped

SentinelTool T1 (`SentinelTool.md:113-191`): the check resolves the name once at
`_check_address` (line 188 of the tool) and the connect resolves it a second time inside
`http.client` (tool lines 276-280); sentinel lines 115-121 describe the classic
check-then-connect TOCTOU. Measured shapes and their counter items:

| sentinel shape (line cites) | counter item | match? |
|---|---|---|
| First DNS answer global, second `127.0.0.1` — `REBIND-SUCCEEDED` (SentinelTool.md:122-137) | `rebind-loop` 4 items: `resolve = {host: [[g1], ["127.0.0.1"]]}` (c2-count.py:135-136, docstring line 39) | yes |
| Second DNS answer private instead of loopback (implicit in T1's "private" class; SentinelTool.md:17, 108-110) | `rebind-private` 2 items: `[[g1], ["10.x.y.z"]]` (c2-count.py:137-139, docstring line 40) | yes |
| SSRF chain: stable registry host 302s to a rebinding host, loopback GET, `SSRF-CHAIN-SUCCEEDED` (SentinelTool.md:139-154) | `rebind-redirect` 2 items: `host` stable `[g1]`; `host2` `[[g2], ["127.0.0.1"]]` (c2-count.py:147-155, docstring line 41) | yes |
| Redirect to a non-global answer on hop 2 (SentinelTool.md:101-105 lists static cases; the rebinding variant is 139-154) | `redirect-loop` 1 item: `host2` resolves only `["127.0.0.1"]` (c2-count.py:156-157), label UNREACHABLE | yes |
| One lookup returning a global *and* a non-global address in the same answer (SentinelTool.md:76-79 requires **every** returned address `is_global`) | `mixed-address` 1 item: `[[g1, "127.0.0.1"]]` in one answer (c2-count.py:143-144), label UNREACHABLE | yes |
| Multi-global answer, tool may pick either (SentinelTool.md:164-171 shows cross-global redirects work) | `multi-address` 2 items: `[[g1, g2]]`, `routed = [g1, g2]` (c2-count.py:140-142) | yes |
| Silent DNS / NXDOMAIN (SentinelTool.md:59-63 namespace cases; T5 malformed host `host does not resolve` at line 329) | `no-resolve` 1 item: `resolve = {}` (c2-count.py:145-146), label UNREACHABLE | yes |

Why a buggy check-then-connect tool is caught, mechanically: the child's `fake_gai` returns
the *k*-th entry of the host's sequence (qr_harness.py:75-78), so the second resolve lands on
`127.0.0.1` or `10.x`; `fake_connect` logs `{"ev":"connect","dest":…}` before routing
(qr_harness.py:89-98) and `score` fails the item on any `dest` outside `spec["routed"]`
(c2-count.py:166-170). `rebind-*` labels are a fair-coin VERBATIM/ABSENT (c2-count.py:121-126),
so a correct tool that resolves once must actually fetch and judge the page — it cannot pass
by refusing.

### T1 shapes with NO counter item

1. **Second answer `::1` or other non-global IPv6.** The sentinel measured the second AAAA
   answer as `::1` alongside `127.0.0.1` (SentinelTool.md:131-133) and lists v6 metadata
   `fd00:ec2::254` refused at line 100. Counter answers are IPv4-only: `global_addrs` draws
   IPv4 (qr_harness.py:270-277), rebind targets are `127.0.0.1`/`10.x` (c2-count.py:135-139),
   and `fake_connect` refuses any `AF_INET6` dial outright (qr_harness.py:104-105). A tool
   whose fix pinned only the IPv4 path would not be distinguished. Severity: low — the
   contract's "one validated DNS resolution" fix pins whatever `getaddrinfo` returned, which
   is version-agnostic [INFERENCE].
2. **Rebind to link-local / metadata (`169.254.169.254`) or private ranges other than
   10.x (`172.16/12`, `192.168/16`, `fd00::/7`).** Sentinel tables at SentinelTool.md:91-103
   name them; `rebind-private` exercises only `10.x` (c2-count.py:137-139). Same fix class;
   low severity [INFERENCE].
3. **NAT64-wrapped metadata and multicast residuals.** SentinelTool.md:173-179:
   `64:ff9b::169.254.169.254` and `224.0.0.1` report `is_global=True` and are attempted.
   No counter item can express them: the name map cannot mint such addresses as "routed",
   and any connection to them is refused by `target` (qr_harness.py:96-98). These stay open
   residuals of the `is_global` predicate itself, outside C2's contract items 2-4.
4. **Per-hop provenance.** Sentinel's host-set observation (SentinelTool.md:163-171) aside,
   the counter checks the item's routed *set*, not which hop produced which address —
   `claims.md` lists this under "Not claimed" (claims.md:215-217). By design, but worth
   repeating: a wrong-hop connection to the item's own other global address passes.
5. **Unrouted-global connect.** `target` refuses any dest not in `routed` and not loopback
   (qr_harness.py:96-98), so an item could mark a connect to a foreign-but-global address;
   no spec creates one (`routed` covers every global address the map can return for that
   item's hosts). Only reachable via a name the map does not know — which `fake_gai` refuses
   first (qr_harness.py:72-74), so no counter item could trigger it.
6. **TLS layer.** T1's `HTTPSConnection` path (SentinelTool.md:117-118) is untested: every
   item URL is `http://` (c2-count.py:152, 159). Contract v2 item 3 requires the hostname be
   used "for TLS (SNI and certificate check)" (claims.md:207-209) — the counter cannot see
   SNI, certificate verification, or a **slow TLS handshake**, the missing drip shape the
   task names. A tool that skipped certificate verification would score 27/27 [INFERENCE].

## T4 — the shapes the sentinel described, mapped

SentinelTool T4 (`SentinelTool.md:243-302`): `resp.read(CHUNK)` at tool line 247 waits for
all 65536 bytes; the socket timeout is per-recv; the deadline is checked only between reads
(lines 256-264). Measured shapes and their items:

| sentinel shape (line cites) | counter item | match? |
|---|---|---|
| Body drip, 1 byte per interval, read() blocks past deadline (SentinelTool.md:270-272) | `drip-body` 3 items: head + 200 bytes at once, then 1 byte per 0.2 s (c2-count.py docstring line 32; qr_harness.py:234-240) | yes |
| Headers dribbled line-by-line, 50.6 s (SentinelTool.md:273); remediation line 300-301 says wrap `getresponse()` in the same budget | `drip-head` 2 items: the whole head 1 byte per 0.2 s (docstring line 31; qr_harness.py:231-232) | yes |
| Multi-hour steady drip, extrapolated days (SentinelTool.md:278-281) | `drip-steady` 2 items: ~3 MB at 4096 B per 0.25 s ≈ 190 s (docstring line 33; qr_harness.py:242-251), label UNREACHABLE — defeats a minimum-rate shortcut (claims.md:44-45) | yes |
| Slow-but-legit sender must finish within DEADLINE (smallest-remediation spirit, SentinelTool.md:295-302) | `slow-ok` 2 items: 6 pieces spread over DEADLINE − 1.0 s, label VERBATIM/ABSENT (docstring line 43; qr_harness.py:252-264; c2-count.py:131-132) — a blunt fixed cutoff or an `UNREACHABLE`-on-slow rule fails these | yes |
| Overall wall bound, kill at cap (SentinelTool.md:290-293) | every item: `bound = DEADLINE + 1.5`, kill at `CAP = 20` (c2-count.py:67-69, 160, 169) | yes |

### T4 shapes with NO counter item

1. **Stall body (send head then silence).** Present — `stall-body` 1 item — but note its
   discriminating power is weak: the sentinel measured the *base* tool already bounding the
   silent case at 30.1 s via the per-recv socket timeout (SentinelTool.md:274-276). It
   guards against a fix that drops socket timeouts entirely; it cannot distinguish
   read()-vs-read1(). By design (regression net).
2. **Server never answers at all** (SentinelTool.md:274). No item: `stall` sends head + 200
   bytes first (qr_harness.py:236-238). A "connect then nothing" shape is untested, though
   it is the one case the base tool already bounds, so its absence costs little.
3. **Drip during a redirect hop** — the missing shape the task names. `rebind-redirect` and
   `redirect-loop` serve `b"moved"` instantly and `host2`'s page is always fast
   (c2-count.py:150-152 has no `behavior=`). Consequence: contract item 2 says DEADLINE
   bounds "every redirect hop … and the one retry" (claims.md:202-204), yet a tool that
   applies DEADLINE **per hop** (fresh budget each hop) instead of **per URL** passes all 27
   items — a slow second hop would expose it and none exists. Same for the **shared retry
   budget**: no item ever causes a retry, so a retry that restarts the clock is invisible.
   Severity: medium — this is a contract-semantics hole a compliant-to-the-letter-but-not-
   the-spirit implementation could pass through [INFERENCE].
4. **Slow connect / slow TCP open.** `fake_connect` completes instantly or refuses
   (qr_harness.py:100-106); no item measures a DEADLINE that must cover connection setup.
   Small; the harness could not delay connects without new machinery.
5. **IPv6 data path.** As under T1: `fake_connect` refuses `AF_INET6` (qr_harness.py:104-105).
   A drip or stall over IPv6 is not expressible; the sentinel itself tested drip only over
   v4/v6-literal loopback (SentinelTool.md:53-58).

## Cross-cutting observations for the build seats

- **Rebind items also pin the *order* of the fix.** `fake_gai` counts calls per host
  (qr_harness.py:75-77); a tool that resolves twice gets the second (hostile) answer, while a
  tool that resolves once and pins/connects to that answer always sees `g1`/`g2`. The counter
  does not assert the *number* of resolves — a tool that resolves 3 times but pins the first
  answer would also pass [INFERENCE] — but contract item 3 only requires "resolved once …
  never resolves the name again for that hop" (claims.md:205-209), and the observable proxy
  is exactly what `score` checks (connect dests ⊆ routed set).
- **`rebind-redirect` demands cross-host redirect following.** A fix that over-corrects to
  the sentinel's optional "confine redirects to the registry host set" (SentinelTool.md:165-171)
  would refuse hop 2 and answer UNREACHABLE against a VERBATIM/ABSENT label. Build seats: pin
  the validated address per hop, keep cross-global-host redirects allowed.
- **Head shape is uniform** (c2-count.py docstring lines 18-21): no header-signature leaks —
  verdict cannot be keyed from headers alone (the v2 CtlShapeKeyed leak, claims.md:32-40).
- **DEADLINE is written into the module constant per item** (qr_harness.py:123-124;
  c2-count.py:119), uniform in [2.0, 6.0] s. A hard-coded 30 s or tiny cutoff fails
  `slow-ok` and bound checks respectively (claims.md:45-47).

## Limits

- I read the frozen counter, harness, sentinel report and claims only; I ran no counter
  (read-only seat) and edited nothing. Counter/harness line numbers are from current lane
  files at `abfdf932…` design-v4 freeze; claims.md lines cited from the same file.
- "Would pass/fail" statements about hypothetical fixes are [INFERENCE] from the score
  function, not measured runs.
- Gaps 3, 4, 6 under T1 and 3 under T4 are the substantive ones to weigh; the rest are
  either harness-inexpressible or already-bounded-at-base.

## Verdict

Every attack shape the sentinel *measured as exploitable* in T1 and T4 has a counter item
(rebind → loopback/private/redirect, mixed-answer, NXDOMAIN, head/body/steady drip, stall,
slow-ok). Missing shapes, in descending weight: per-URL-vs-per-hop deadline and shared-retry
budget (no drip-on-redirect item), TLS including slow handshake and SNI/cert checking
(counter is http-only), IPv6 answers and destinations (harness refuses AF_INET6), rebind
targets beyond `127.0.0.1`/`10.x`, never-answers and connect-phase stalls, and the
`is_global` residuals (NAT64, multicast) which no item design could close.

Report: .ufo/waves/round-30/build/ScoutSentinelT1T4.md
