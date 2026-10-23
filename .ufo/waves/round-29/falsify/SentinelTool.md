# SentinelTool — security review of the landed `tools/quote-reopen.py` against T1–T7

Seat: SentinelTool (sentinel, leaf, no subagents). Lane: `chousa-shokunin`.
Tool reviewed: `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quote-reopen.py`,
sha256 `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea`, landed at
`30c9d24` (`git log --oneline -1 -- tools/quote-reopen.py`), clean in
`git status --porcelain tools/quote-reopen.py`.
Source of the threats: `.ufo/waves/round-29/build/SentinelFetchBounds.md` (T1–T7).
Judged on: operability. I did **not** edit the tool, the frozen claim, the counter or
the fixture; I ran no `git`/`jj` write command; I wrote nothing outside my seat
directory and `/fast/scratch/hyaku/chousa-r29/w2/SentinelTool/`.

## Verdict summary

| # | Threat | Closer in the landed code | Verdict | Severity of what remains |
|---|---|---|---|---|
| T1 | registry URL or redirect reaching loopback / private / link-local / cloud metadata | `_check_url` 163-184, `_check_address` 186-205 (`is_global` at 204), called **per hop** at 269-270 | **OPEN (partial)** — static targets blocked, **DNS rebinding bypasses it** | medium: needs a hostile DNS answer for a registry or redirect host |
| T2 | `file:` / `ftp:` / `data:` via redirect | scheme check 167-168 applied to every hop (269); extractor `URL_RE` 67 matches `https?://` only | **CLOSED** | — |
| T3 | gzip/deflate bomb against the 8 MiB cap | wire cap 251-254; incremental inflate with `max_length` 221-225 | **CLOSED** | — |
| T4 | slowloris body against the 30 s deadline | deadline 331, per-iteration timeout 237-245 | **OPEN** — the deadline bounds the gap *between* reads, not a single `read()` | medium: a drip server holds the tool for minutes-to-hours |
| T5 | oversized response headers aborting the run | `fetch_page` catch set 339-341 includes `HTTPException` and `InvalidURL` | **CLOSED** | — |
| T6 | credentials in a URL | userinfo refused 169-170; details are fixed strings, never URLs or exception text (340) | **CLOSED** | — |
| T7 | page bytes written to disk or echoed | all writes go to stdout/stderr (412-415); `strace` shows no write-mode open | **CLOSED** | — |

**Overall:** five of seven threats are fully closed by the landed code, and the
closures are real, not incidental. Two are only partly closed: **T1** because the
address check and the connection resolve the name independently (a classic
check-then-connect TOCTOU), and **T4** because the 30 s deadline is checked
between chunk reads while one `read()` may block arbitrarily long. Both need a
hostile server, so neither touches the eight fixture sources and neither changes
the 130/130 predicate. Both are closable inside the frozen contract without
changing any verdict.

## How I tested — and why not on `127.0.0.1` for the fetch path

T1's own closure makes an all-loopback harness impossible for anything that must
actually fetch: `_check_address` (186-205) refuses a resolved peer that is not
`is_global`, and it runs on the **initial** URL too (269-270), not only on
redirects. Measured, with a live listener on `127.0.0.1`:

```
== T1-a registry URL is loopback   exit=1
   QUOTE_REOPEN  i1  UNREACHABLE  host resolves to a non-global address
   loopback listener accepted=0 requests=[]
```

So a temporary registry naming a `127.0.0.1` server is refused **before any
socket is opened** — the loopback listener logged zero accepted connections.
Testing therefore splits into two halves:

1. **Refusal half, on literal loopback** (the cases above): the tool must refuse
   and must not connect. Zero accepted connections is the assertion.
2. **Fetch half, on this host's own globally-scoped IPv6 address**
   `2804:14d:5c56:36ef:fe9d:5ff:fe5e:5dbe`, which is `is_global=True` but routed
   locally (`ip -6 route get` → `local … dev lo table local`). A server bound
   there passes T1's check and traffic never leaves the machine. Everything that
   needs a successful fetch (T2 redirects, T3 bombs, T4 drip, T5 headers, T6
   userinfo, T7 writes, the T1 rebinding case) runs there.
3. **Namespace cases** (DNS rebinding, silent DNS) run under
   `unshare -m -n --map-root-user` with a private `resolve.conf` pointing at a
   53/udp responder I start in the namespace; a bind mount replaces
   `/etc/resolv.conf` inside the namespace only. The host's resolver is untouched.
   The namespace has only loopback, so nothing external is reachable from it.

Python 3.14.8. No tools installed or updated. No external host contacted: the
only non-loopback address used is this machine's own global IPv6, and the
namespace cases have no route off the box.

## T1 — address confinement: **OPEN (partial)**

### What the code does

`_check_url` (163-184) parses each hop and refuses a scheme outside `http`/`https`
(167-168), userinfo (169-170), a missing host (172-173) and a bad port (174-177).
`_check_address` (186-205) resolves with `socket.getaddrinfo(host, port,
type=SOCK_STREAM)`, refuses a resolution failure (190-198) and refuses unless
**every** returned address has `ipaddress.ip_address(...).is_global` (203-205).
`_request_once` calls both **per redirect hop** (269-270) before opening the
connection (276-280). That is the correct shape and it is strictly stronger than
the wave-1 note required.

### Measured — static targets are refused, and nothing is dialled

Every one of these returned `UNREACHABLE  host resolves to a non-global address`,
in `0.0 s`, with the loopback listener accepting **0** connections:

| input | result |
|---|---|
| registry URL `http://127.0.0.1:PORT/ok` | refused, 0 connections |
| registry URL `http://10.0.0.1/x` | refused |
| registry URL `http://169.254.169.254/…` | refused |
| registry URL `http://2130706433/x` (decimal-int 127.0.0.1) | refused |
| registry URL `http://0x7f000001/x` (hex 127.0.0.1) | refused |
| registry URL `http://127.1/x` (short form) | refused |
| registry URL `http://[::ffff:127.0.0.1]/x` (IPv4-mapped) | refused |
| registry URL `http://localhost:PORT/ok`, `localhost.localdomain` | refused |
| registry URL `http://[::ffff:169.254.169.254]/x` | refused |
| registry URL `http://100.100.100.200/x` (Alibaba metadata) | refused |
| registry URL `http://192.0.0.192/x` (Oracle metadata) | refused |
| registry URL `http://[fd00:ec2::254]/x` (AWS v6 metadata) | refused |
| `302 → http://127.0.0.1:PORT/` | not followed, 0 connections |
| `302 → http://10.0.0.1/x` | not followed |
| `302 → http://169.254.169.254/latest/meta-data/` | not followed |
| `302 → //127.0.0.1:PORT/x` (scheme-relative) | not followed, 0 connections |
| `302 → http://localhost:PORT/` | not followed, 0 connections |
| control: `302 →` same global host `/ok` | followed, `VERBATIM` |

`is_global` is the right predicate for the plain cases: `127.0.0.1`, `::1`,
`169.254.169.254`, `10.0.0.1`, `100.100.100.200`, `192.0.0.192`,
`fd00:ec2::254`, `100.64.0.1` all report `is_global=False`; `8.8.8.8`,
`93.184.216.34` report `True`.

### The gap: check-then-connect (DNS rebinding)

`_check_address` resolves the name at 188. The connection then resolves the *same
name again*, independently, inside `http.client.HTTPConnection` at 280 (and
`HTTPSConnection` at 276-278); `socket.create_connection` calls `getaddrinfo` a
second time. There is no `getpeername()` re-check after connect — I grepped the
file and the only socket-object use is `sock.settimeout` at 243. A DNS server
that answers the first query with a global address and the second with `127.0.0.1`
therefore passes the policy check and lands the connection on loopback.

**Measured, twice, in a private netns** (`dns_rebind.py`). Registry row
`http://rebind.test:45799/ok`; the 53/udp responder answers the first A/AAAA round
with `93.184.216.34` / the host's global IPv6 and every later round with
`127.0.0.1` / `::1`:

```
exit=0 elapsed=0.0s
QUOTE_REOPEN  i1  VERBATIM  matched in normalized page text
dns answers (nth-of-type, qtype, addr): [(1,1,'93.184.216.34'), (1,28,'2804:…:5dbe'),
                                         (2,1,'127.0.0.1'), (2,28,'::1')]
loopback http connections accepted: 1 [('127.0.0.1', 51434)]
REBIND-SUCCEEDED
```

Repeated: `REBIND-SUCCEEDED` on both runs, one loopback connection each.

**And the full chain, which needs no hostile registry row** (`ssrf_chain.py`):
the registry URL is an ordinary globally-scoped address, that host answers `302
Location: http://rebind.test:PORT2/ok`, and the rebinding name does the rest.

```
exit=0 elapsed=0.2s
QUOTE_REOPEN  i1  VERBATIM  matched in normalized page text
first-hop connections: 1
LOOPBACK connections accepted: 1 [('127.0.0.1', 40656)]
SSRF-CHAIN-SUCCEEDED
```

The tool followed a redirect off the registry host, then read a page from
`127.0.0.1` and reported `VERBATIM` — a full SSRF into any loopback service, and
in a cloud host into the metadata endpoint, from a registry row whose own URL is
a perfectly ordinary public address.

**Exploit path, plainly.** (1) A registry row, or any redirect served by a
registry host, names a host whose DNS the attacker controls — the lane's redirect
surface is open, see below. (2) That DNS answers `A 93.184.216.34` for the policy
check and `A 127.0.0.1` for the connect. (3) The tool GETs the loopback service,
normalizes its body as page text, and can print it into the counter's stdout — a
`VERBATIM` verdict for a quote that exists only on an internal service.

**Also measured, not a bypass but worth recording:** a redirect to a *different*
global host is followed (`Q6` returned `VERBATIM` for a redirect from one global
address to a second one). The contract says "the tool fetches only registry
URLs", and the wave-1 note suggested confining redirects to the registry host
set. The landed tool confines redirects by **address class**, not by host set, so
"registry URLs only" is true for the first hop only. Given the T1 rebinding vector
above, host-set confinement would shrink the attack surface materially. It
changes no label today: the sibling census shows final host equals registry host
for all 40 fetched rows.

**Residual, classification only:** `64:ff9b::169.254.169.254` (a NAT64
translation prefix wrapping the metadata IPv4) reports `is_global=True` and the
tool attempts it (`UNREACHABLE  fetch failed: TimeoutError` after the full 30 s,
because this host has no NAT64 route). Multicast also passes (`224.0.0.1`,
`ff02::1` are `is_global=True`); `224.0.0.1` produced `fetch failed: OSError`.
Neither is reachable metadata on this host; both are named so a later reader does
not assume `is_global` means "public unicast".

**Smallest remediation.** Re-check the *connected* peer after the socket exists:
in `_request_once`, after `conn.getresponse()` (or by calling `conn.connect()`
and then `conn.sock.getpeername()` before `request`) apply the same
`is_global` test to `getpeername()[0]` and `_Refuse("peer address is not global")`
on failure. That closes the TOCTOU for both `http` and `https` because
`getpeername` reports the address actually used. Optionally also pin the vetted
address: pass the resolved-and-vetted address to the connection while keeping the
hostname for the `Host` header and for TLS SNI/verification. Neither touches the
frozen contract (`claims.md`, *Tool contract (frozen)*, "registry URLs only … http
and https only (redirects too)") and neither changes a verdict on the eight
fixture sources, all of which resolve to global addresses.

## T2 — scheme confinement: **CLOSED**

`_check_url` 167-168 refuses any scheme other than `http`/`https`, and it is
applied to every hop (269), so a redirect cannot leave the envelope. The URL
extractor is `URL_RE = re.compile(r"https?://\S+")` (67), i.e. a `file:` or
`data:` cell yields no URL at all and becomes `NO_SOURCE` — the wave-1 finding is
closed at both layers. Measured, on the global-v6 origin:

```
302 → file:///etc/hostname   UNREACHABLE  scheme not http or https   (0 loopback conns)
302 → ftp://127.0.0.1:21/x   UNREACHABLE  scheme not http or https   (0 loopback conns)
302 → data:text/plain,hello  UNREACHABLE  scheme not http or https   (0 loopback conns)
registry cell "file:///etc/hostname" only → NO_SOURCE "registry row S001 has no http(s) URL"
```

The tool uses `http.client` directly (276-280), not `urllib.request.urlopen`, so
none of `FileHandler`, `FTPHandler` or `DataHandler` is ever installed — `file:`
and `data:` are not merely refused by policy, they are unreachable by
construction. That is the right shape.

## T3 — decompression bomb: **CLOSED**

Wire bytes are capped in `_read_response` at 251-254 (`total > MAX_BODY` →
`over`). Inflated bytes are capped in `_inflate_stream` by passing
`max_length = MAX_BODY + 1 - len(out)` to `decompress` (221) and returning
`over=True` as soon as `len(out) > MAX_BODY` (222-223). `fetch_page` maps either
`over` to `UNREACHABLE  body over 8 MiB` (298-301). Measured with the tool as a
child of a measuring wrapper (`mem_probe.py`), peak child RSS from
`getrusage(RUSAGE_CHILDREN).ru_maxrss`:

```
R1 baseline 40-byte page          RSS  22 MB   VERBATIM
R2 gzip    256 MiB inflated (261 kB wire)  RSS 38 MB  UNREACHABLE body over 8 MiB  0.6 s
R3 deflate 256 MiB inflated (261 kB wire)  RSS 38 MB  UNREACHABLE body over 8 MiB  0.5 s
R4 wire    64 MiB (uncompressed)           RSS 30 MB  UNREACHABLE body over 8 MiB  0.1 s
```

A 256 MiB inflate costs 16 MB over baseline, i.e. it stops at the 8 MiB cap and
does not allocate the bomb. Also measured: a 12.5 MiB chunked-transfer body →
`body over 8 MiB`; a 10 MiB body with an honest `Content-Length` → `body over
8 MiB`; the wave-1 gzip-of-gzip shape → `ABSENT` (only one layer honoured, no
bomb); a small legitimate gzip body → `VERBATIM`, so the cap does not break the
normal path.

One rotation bug in my first probe: `slow_body` sent the whole 40-byte body in
the header write and then dripped 40 more bytes, so the tool read a complete body
instantly and answered `ABSENT` in `0.0 s`. I fixed the server (headers first,
`Content-Length: 40`, then one byte per second) and the corrected measurement is
the T4 finding below.

## T4 — slow body against the 30 s deadline: **OPEN**

### What the code does

`fetch_page` sets one wall-clock deadline per URL (331: `deadline =
time.monotonic() + DEADLINE`) and shares it with the single retry (333-347,
`attempt >= RETRIES or (deadline - time.monotonic()) <= 0` at 346). That is the
wave-1 recommendation done right: the retry does not restart the budget.
`_read_response` (232-257) recomputes `remaining = deadline - time.monotonic()`
per iteration, raises `_Refuse("deadline exceeded while reading the body")` when
`remaining <= 0` (237-239), and shrinks the socket timeout to `remaining`
(240-245). `_request_once` checks the deadline per hop (271-274).

### The gap: the check is between reads, not around one read

The block is `chunk = resp.read(CHUNK)` (247) with `CHUNK = 65536` (52).
`HTTPResponse.read(amt)` on a known-length body loops in the buffered reader
until it has `amt` bytes or EOF. The socket timeout set at 243 is a **per-recv**
timeout, so a server that dribbles a byte more often than `remaining` never trips
it, and the single `read()` can block far past the deadline. The deadline is then
observed only after that read returns.

**Measured** (`probe2.py` P1 corrected, `probe4.py` S3, `probe3.py` Q1), with
`Content-Length: 100000` and the tool's own 30 s deadline:

| shape | wall time | result |
|---|---|---|
| one byte per second, `Content-Length: 40` | **40.1 s** | `UNREACHABLE  deadline exceeded while reading the body` |
| one byte per **2 s**, `Content-Length: 100000` | **still running at 70 s**, killed | — |
| one byte per **5 s**, `Content-Length: 100000` | **still running at 60 s**, killed | — |
| headers dribbled one line per 0.5 s | **50.6 s** | `UNREACHABLE  fetch failed: HTTPException` (header count cap) |
| server never answers at all | 30.1 s | `UNREACHABLE  fetch failed: TimeoutError` → correctly bounded |

So the "never answers" case is bounded (the first recv times out at the deadline),
but a **drip** is not: the header phase alone ran 50.6 s, and a body drip was
still alive when I killed it at 70 s. Extrapolating the observed mechanism: with
`CHUNK = 65536` and a 2 s drip, one `read()` needs about 36 hours; with 5 s, about
3.8 days. My controlled replication of the exact loop (`read` vs `read1`, 3 s
deadline, drip server) confirms both the diagnosis and the fix:

```
read : deadline check fired at 10.00s (bounded)   <- after the read returned
read1: deadline check fired at  3.00s (bounded)   <- at the deadline
```

**Impact.** One hostile registry host or redirect target holds a verification run
open for minutes to days. The frozen counter passes its own `--timeout`, so the run
is eventually killed and scored as a miss rather than a hang — but the tool's own
stated bound ("a 30 s total deadline per URL shared with the single retry", module
docstring 22-25) is not what the code delivers for a dripping peer, and against
the counter that is a failed measurement, not a partial pass.

**Smallest remediation.** Use `resp.read1(CHUNK)` at 247 instead of `resp.read`,
or `resp.readinto` with a bounded buffer. `read1` returns whatever is available
after at most one `recv`, so the loop's per-iteration deadline check at 237-239
and the shrunk socket timeout at 243 become effective. Measured above: 3.00 s
against a 3 s deadline where `read` took 10.00 s. A stronger variant also wraps
the header read (`conn.getresponse()` at 283) in the same budget, which the
dribbled-header case shows is currently unbounded too. Neither changes any
verdict on the eight fixture sources (all answered in under two seconds).

## T5 — oversized headers: **CLOSED**

`fetch_page`'s catch set at 339-341 is
`(http.client.HTTPException, http.client.InvalidURL, OSError, ValueError,
UnicodeError, ssl.SSLError, zlib.error)`. `LineTooLong` and `TooManyHeaders`
derive from `HTTPException`, which is *not* an `OSError` — the wave-1 finding's
whole point — and `InvalidURL` is named explicitly. Both are caught and mapped to
`detail = "fetch failed: <ExceptionType>"`, `text = None`, hence `UNREACHABLE` for
that item only. Measured:

```
100 kB header line  → UNREACHABLE  fetch failed: LineTooLong     run continues
150 headers         → UNREACHABLE  fetch failed: HTTPException   run continues
mixed run, 3 items: i1 UNREACHABLE LineTooLong | i2 VERBATIM | i3 UNREACHABLE LineTooLong
                     summary verbatim=1 … unreachable=2, exit=1
```

The third line is the decisive one: one item's oversized header does not abort the
run, does not swallow the other verdicts, and does not change the exit code
contract (`1` because not every item is `VERBATIM`). The detail carries the
exception *type name* only — never the message, which was the wave-1 leak path.

Malformed input is equally safe (each `exit=1`, every item still judged):
`http://[::1/x` → `fetch failed: ValueError`; `http:///path` → `url has no host`;
`http://host:99999/x` and `http://host:abc/x` → `url has an invalid port`;
`http://exa%6dple.invalid/x`, a 300-character label → `host does not resolve`;
a 100000-byte `Content-Length` lie → `body over 8 MiB`; a 20-hop redirect chain
and a self-redirect → `too many redirects` after `MAX_REDIRECTS = 10` (51) with
`MAX_REDIRECTS + 1` iterations (267).

## T6 — credentials in a URL: **CLOSED**

`_check_url` refuses userinfo at 169-170 **before** any request is built, on every
hop (269). Every failure detail is a fixed string: the `_Refuse` reasons
(167-205) and `"fetch failed: %s" % type(e).__name__` (340) carry no URL and no
exception message. Measured with secret `s3cr3tP4ss`:

```
registry https://alice:s3cr3tP4ss@[global]:PORT/ok  → UNREACHABLE  url carries userinfo
302 → http://bob:s3cr3tP4ss@127.0.0.1:9/x           → UNREACHABLE  url carries userinfo
secret present in tool output: False   (both cases)
tool output bytes: b'QUOTE_REOPEN\ti1\tUNREACHABLE\turl carries userinfo\n…'
```

That also closes the specific wave-1 leak: the counter persists `stderr_tail`
verbatim into its receipt (`.ufo/waves/round-29/../c1-count.py`, `err[-2000:]`),
and this tool writes nothing to stderr on the fetch path and never echoes the URL,
so a credential cannot reach a committed record. Complements measured:
`http://alice@example.invalid/ok` → `url carries userinfo`; a fragment
(`…/ok#frag`) is stripped (`fetch_page` 330) and does not affect the verdict.

## T7 — nothing written to disk: **CLOSED**

Under `strace -f -e trace=connect,socket,openat,write` (`strace.out`), the run
opens only its own source, the registry and the items file, all `O_RDONLY`:

```
openat(AT_FDCWD, ".../tools/quote-reopen.py", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, ".../reg.tsv",  O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, ".../items.tsv", O_RDONLY|O_CLOEXEC) = 3
```

No `O_WRONLY`, `O_RDWR` or `O_CREAT` open of any application path; the only
write syscalls are the two to stdout/stderr (412-415). A directory listing before
and after a run showed `new files: []`. Page text stays in memory: `verify`
builds `cache[url] = fetch_page(url)` (389-391) and `out` (383) as in-process
objects. stdout carries only the contract lines (412-415); stderr is silent on
the fetch path.

One thing I probed because it is adjacent: server-controlled bytes do reach
stdout — the `UNREACHABLE` detail for a bad type is `"content type %s" % ctype`
(299). It is `.lower()`ed and tabs are replaced with spaces (412). I tried
three shapes (obs-fold continuation carrying a verdict line, a vertical tab, a
bare CR); none forged a parseable verdict line, because the counter splits on
`\n`, requires `parts[0] == "QUOTE_REOPEN"` and lowercases the ctype. A folded
header does put a raw `\r` inside the detail line (`content type text/html\r`),
so the counter's `splitlines()` sees an extra junk fragment — it is ignored
(`parts[0]` is `" quote_reopen"`). Low severity, reported for completeness, not a
T7 breach.

## Limits of this review

* Every fetch went to a server I started: `127.0.0.1`, this host's own global
  IPv6 (locally routed, `local … dev lo`), or a netns with only loopback. I did
  not open a `SOURCES.md` URL and did not contact any external host.
* The T1 rebinding result depends on a hostile DNS answer, which I simulated with
  a responder I control inside a private namespace. A real deployment's exposure
  depends on the resolver and on whether any registry/redirect host is
  attacker-controlled; the mechanism is measured, the real-world likelihood is
  [INFERENCE].
* The `is_global` predicate is Python's; I measured its classification for the
  metadata addresses I could name, not for every registry in use.
* I did not run the frozen predicate or the counter: my job here is the tool's
  security surface, and the security findings change no verdict on the eight
  fixture sources, so the 130/130 claim is untouched either way.
* The T4 numbers are wall-clock measurements on this host; the pathological bound
  (hours to days) is extrapolated from the measured mechanism and the 65536-byte
  chunk, marked [INFERENCE].
* No process I started remains running (`ps` shows none); the servers are
  in-process threads shut down on exit, and the namespace cases are single
  `unshare` invocations that end with the probe.
* No tool was installed or updated.

**Files written by this seat:** this report and, inside
`.ufo/waves/round-29/falsify/SentinelTool/`, the probe scripts and config:
`harness.py`, `tests.py`, `probe2.py`, `probe3.py`, `probe4.py`, `probe5.py`,
`mem_probe.py`, `inject_probe.py`, `dns_rebind.py`, `ssrf_chain.py`,
`dns_deadline.py`, `out2.txt`, `myresolv.conf`, `myresolv2.conf`. The same
scripts are also under `/fast/scratch/hyaku/chousa-r29/w2/SentinelTool/`.

Report: .ufo/waves/round-29/falsify/SentinelTool.md
