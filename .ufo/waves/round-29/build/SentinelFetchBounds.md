# SentinelFetchBounds — security review of the frozen C1 fetch bounds

Seat: SentinelFetchBounds (sentinel, leaf, no subagents). Lane:
`chousa-shokunin`. Lane HEAD at review time: `66bf1b9300733b24e76efe393646b3037402080e`
(`git rev-parse HEAD`). Frozen design reviewed: round-29 C1 **v3**
(`corpus/evidence/round29/claims.md`, section *Tool contract (frozen)*).
Counter SHA-256 at review time:
`cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d`
(`sha256sum corpus/evidence/round29/c1-count.py`).

Judged on: operability. Scope: the fetch bounds only — command construction,
address and scheme resolution, untrusted records, secrets, permissions and
process cleanup. I did **not** edit the frozen claim, counter or fixture, did
not write to the lane's production files, and ran no `git`/`jj` write command.

---

## 1. What I did

1. Read the frozen contract (`claims.md`, *Tool contract (frozen)*), the frozen
   counter's reference functions (`corpus/evidence/round29/c1-count.py`), the
   lane registry (`corpus/SOURCES.md`), `PROVINCE.md`, `/home/vgpnk/Projects/shokunin/CORPUS.md`,
   the lane `SKILL.md` boundary clause and the round-29 prompt addendum.
2. Re-ran the registry census and re-derived the registry facts the fetch
   bounds depend on (row count, URL presence, schemes, userinfo, hosts,
   redirect outcomes) with re-run commands.
3. Wrote one self-contained stdlib probe
   (`.ufo/waves/round-29/build/SentinelFetchBounds/probe_fetch_bounds.py`) that
   starts a loopback HTTP server and measures how `urllib.request` actually
   behaves for each threat: redirect scheme and host, gzip inflation, socket
   timeout semantics, oversized headers, userinfo, ambient proxy, direct
   `file:`/`data:` handling. All traffic is to `127.0.0.1`; no external host
   was contacted by this seat.
4. Ran it and kept the output verbatim next to the script
   (`.ufo/waves/round-29/build/SentinelFetchBounds/probe_output.txt`).

Probe command and result:

```
timeout 180 python3 probe_fetch_bounds.py > probe_output.txt 2>&1 ; echo EXIT=$?
EXIT=0
```

Wall time of that command: 24.89 s (measured by the tool, printed as the last
line of the run log in `probe_output.txt`).

---

## 2. Verdict summary

Severity is stated for the **landed tool** `tools/quote-reopen.py` as the
frozen contract describes it, against the registry the lane actually holds
today.

| # | Threat | Frozen contract covers it? | Severity | Smallest safe implementation note | L0 question needed? |
|---|---|---|---|---|---|
| T1 | Registry URL or redirect reaching loopback, link-local, private ranges or cloud metadata | **Partial** — scheme only; redirect host and resolved address unbounded | medium | Confine redirects to the registry host set; refuse any resolved peer address that is not global | no |
| T2 | `file:`, `ftp:`, `data:` schemes via redirect | **Partial** — `file:`/`data:` blocked by stdlib luck; **`ftp:` is followed** | low | Custom redirect handler: allow only `http`/`https`, refuse userinfo | no |
| T3 | gzip/deflate decompression bomb against the 8 MiB cap | **Partial** — "the body" is ambiguous between wire and inflated bytes | medium | Cap wire bytes *and* inflated bytes at 8 MiB + 1, inflate incrementally | no |
| T4 | Slowloris body against the 30 s timeout | **Partial** — stdlib timeout is per-operation, not a wall-clock deadline | medium | Enforce a total per-URL deadline; share it with the single retry | no |
| T5 | Huge response headers | **No** — but stdlib refuses them, with an exception class that escapes the usual `except` set | medium | Catch `http.client.HTTPException` / `InvalidURL`; map every fetch exception to `UNREACHABLE` | no |
| T6 | Credentials in a URL | **Partial** — "no cookies or credentials" covers the request, not the registry cell | medium | Refuse userinfo before the request; never echo a URL or exception text into stdout/stderr | no |
| T7 | Logging page bytes to disk | **No** clause, and the receipt captures stderr verbatim | medium | Memory only, no cache file; stdout carries only the contract lines; stderr carries byte counts and digests only | no |

**Overall:** the frozen contract's *intent* covers every threat, but four of
the seven (T1, T3, T4, T5) are not enforced by the stdlib behaviour the
contract's own wording leads an implementer to use. All seven are closable
inside the frozen contract — none of them changes a verdict for the eight
fixture sources, so none of them threatens the 130/130 target. **No L0 question
is required.** The one genuinely open item is a province-fit judgment, which
the lane can settle itself (§5).

---

## 3. Findings in detail

### T1 — Redirect or registry URL reaching loopback, link-local, private ranges or cloud metadata

**Exploit path.** The contract says "the tool fetches only registry URLs, with
GET only … http and https only (redirects too)". That constrains the *scheme*
of the request and of redirects; it names no bound on the redirect *host* or on
the resolved peer address. An implementer who reaches for
`urllib.request.urlopen` inherits `HTTPRedirectHandler`, which follows a
`Location:` to any host. Two routes reach a private address:

* a registry row naming a private address directly — reachable through the
  `--registry` option, which accepts any registry file, not only the lane's
  own; and
* a public registry host answering `302 Location: http://169.254.169.254/…`.

**Evidence (measured, `probe_output.txt` section 1/2).** Against a loopback
server that answered `302 Location: <target>`, the default opener attempted
every private target:

```
file:///etc/hostname                    urllib.error.HTTPError | OSError=True :: HTTP Error 302: Found - Redirection to url 'file:///etc/hostname' is n
ftp://127.0.0.1:1/secret                urllib.error.URLError | OSError=True :: <urlopen error ftp error: [Errno 111] Connection refused>
http://127.0.0.1:1/x                    urllib.error.URLError | OSError=True :: <urlopen error [Errno 111] Connection refused>
http://[::1]:1/x                        urllib.error.URLError | OSError=True :: <urlopen error [Errno 111] Connection refused>
http://169.254.169.254/latest/meta-data/ urllib.error.URLError | OSError=True :: <urlopen error timed out>
http://169.254.169.254/latest/meta-data/iam/security-credentials/ urllib.error.URLError | OSError=True :: <urlopen error timed out>
http://10.0.0.1/y                       urllib.error.URLError | OSError=True :: <urlopen error timed out>
```

"Connection refused" is the outcome of a connection attempt that was made and
reached the host stack: the loopback target and the `ftp://` target were
dialled. "timed out" on `169.254.169.254` and `10.0.0.1` means the request
was routed to those addresses and no answer came within the probe's 4 s
timeout — this host has no route to them, but the request was still issued
toward the link-local metadata address rather than refused by the client. The
metadata service on `169.254.169.254` returns instance credentials on a
reachable host; a tool that read that body would hold a credential in memory
and could echo it into its output.

**Registry facts, re-run** (`python3` over `corpus/SOURCES.md`, plus
`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 49):

```
rows=49 with_http_url=40 without_url=9 distinct_hosts=22 rows_with_multiple_urls=0 non_http_scheme_urls=0 urls_with_userinfo=0
```

DNS resolution of the eight fixture hosts returned only global addresses
(`162.159.140.98`, `172.66.0.96`, `192.0.78.24`, `99.83.231.148`,
`104.21.44.235`, `104.18.22.19`, `151.101.0.223`, `2606:4700:7::60` — all
`is_global=True`). No registry row is plain `http`. The sibling fetch census
(`.ufo/waves/round-29/build/ScoutRegistryFetch/registry-fetch.tsv`) shows the
final host equals the registry host for every one of the 40 fetched rows, so
confinement changes no label today.

**Impact.** A hostile or simply careless registry file (reachable through
`--registry`) turns a verification tool into a request launcher aimed at
loopback services and cloud metadata, with the response body treated as page
text and eligible to appear in the tool's output.

**Smallest safe implementation note.** Two checks, both cheap:

1. Refuse a URL whose `urlsplit(...).username` or `.password` is set (T6).
2. Resolve each hop and refuse any peer address that is not global —
   `ipaddress.ip_address(a).is_global` — which excludes loopback
   (`127.0.0.0/8`, `::1`), link-local (`169.254.0.0/16`, `fe80::/10`),
   private (`10/8`, `172.16/12`, `192.168/16`, `fc00::/7`) and the metadata
   addresses (`169.254.169.254`, `100.100.100.200`, `fd00:ec2::254`).
   Measured classification in `probe_output.txt`: every one of those addresses
   reports `is_global=False`; `8.8.8.8` reports `is_global=True`.

If a host allowlist is preferred over an address check, make it **host-level,
not exact-URL**: `S025` redirects `https://www.rfc-editor.org/rfc/rfc9111` to
`https://www.rfc-editor.org/info/rfc9111/` (different path, same host), so an
exact-URL allowlist would refuse a legitimate redirect. The lane already has
the redirect-guard shape in
`.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/control.py` (a
`RegistryRedirect(HTTPRedirectHandler)` subclass refusing a scheme outside
`{http, https}` and refusing credentials); reuse that shape.

**L0:** no. The frozen wording "the tool fetches only registry URLs" plus
"http and https only (redirects too)" already supports confinement, and
confinement changes no verdict for the eight fixture sources.

### T2 — `file:`, `ftp:`, `data:` schemes through a redirect

**Exploit path.** Same redirect surface as T1, different payload.

**Evidence (measured).** `file:` and `data:` redirects are refused by the
stdlib handler ("Redirection to url 'file:///etc/hostname' is not allowed") —
but that is stdlib behaviour, not the contract, and it is not symmetric:
**`ftp://` redirects are followed.** The probe shows
`ftp://127.0.0.1:1/secret` producing `<urlopen error ftp error: [Errno 111]
Connection refused>` — an FTP connection was attempted, which the contract's
"http and https only (redirects too)" forbids. Separately, the *default*
opener includes `FileHandler` and `DataHandler`, so a direct
`urlopen("file:///etc/hostname")` read a local file and
`urlopen("data:text/plain,hello")` returned inline data (probe section 8) —
reachable only if a non-http(s) URL is ever handed to the opener.

**Impact.** A `ftp:` hop leaves the http/https envelope the contract draws.
The `file:`/`data:` direct path is closed by the contract's own `NO_SOURCE`
rule (a cell with no `http://`/`https://` URL is `NO_SOURCE`, never fetched),
but only if the URL extractor matches `https?://` specifically. The frozen
counter does: `re.search(r"https?://\S+", ln.split("|")[2])`
(`c1-count.py`, `registry_url`). A generic `\S+://\S+` extractor would pick up
`file:` and `data:` URLs and break that rule.

**Smallest safe implementation note.** One redirect handler that raises unless
`parts.scheme in {"http", "https"}` and `not (parts.username or
parts.password)`, and one URL extractor that matches `https?://\S+` only.
Both shapes already exist in the lane (control cited under T1).

**L0:** no.

### T3 — Decompression bomb against the 8 MiB cap

**Exploit path.** The contract makes "the body is over 8 MiB" an `UNREACHABLE`
trigger but does not say whether "the body" is the wire bytes or the inflated
bytes. The counter's reference function
(`c1-count.py`, `fetch_text`) reads `r.read(8 * 1024 * 1024 + 1)` of **wire**
bytes and then calls `gzip.decompress(body)` on the whole thing with no size
limit. An implementer who mirrors the reference inherits an unbounded inflate.

**Evidence (measured, probe section 3).** A 200 MiB body of repeated `A`
compressed to 203861 bytes was served with `Content-Encoding: gzip`:

```
wire bytes read under the 8 MiB+1 read cap: 203861
gzip.decompress of that prefix expands to: 209715200 bytes (200.0 MiB)
counter reference inflate ratio: 1029x
bounded incremental inflate with max_length=8 MiB+1 stops at: 8388609 bytes
```

**Impact.** One registry host can force a multi-hundred-megabyte allocation
per fetch, with the retry doubling it. The same host would also inflate
inside the frozen counter, so this is a measurement-availability risk as well
as a tool risk.

**Smallest safe implementation note.** Apply the cap twice: read at most
`8 * 1024 * 1024 + 1` wire bytes, and inflate through
`zlib.decompressobj(...).decompress(data, 8 * 1024 * 1024 + 1)` so the
inflated stream is bounded as well; anything over either cap is
`UNREACHABLE`. This changes no label for the eight fixture sources: the
largest inflated fixture page is `S003` at 1,171,446 bytes
(`.ufo/waves/round-29/build/ScoutRegistryFetch/registry-fetch.tsv`,
`inflated_bytes` column), far below the cap.

**L0:** no.

### T4 — Slowloris body against the 30 s timeout

**Exploit path.** "a 30 s timeout" reads as a wall-clock bound on a fetch.
`urllib.request.urlopen(timeout=…)` sets a *per-socket-operation* timeout, so
a server that dribbles one byte per interval keeps the read alive far past
the nominal timeout.

**Evidence (measured, probe section 4).** A server that sent 20 bytes at
0.6 s intervals, against a socket timeout of 2 s:

```
read 20 bytes in 11.4 s wall with socket timeout=2 s
```

Wall time was 5.7 times the stated timeout, and the read had not ended. With
eight registry hosts and one retry each, the total run is unbounded relative to
the contract's stated bound. The counter passes `--timeout 900` to the
candidate process, so an over-long run is killed and scored as a miss rather
than a hang.

**Smallest safe implementation note.** Treat 30 s as a **total per-URL
deadline**: track `time.monotonic()` across the whole fetch, pass the
remaining budget as the socket timeout, and check it between reads; let the
single retry share the same total budget rather than restarting it. This
strengthens the stated bound without changing any verdict on the eight
fixture sources, all of which answered in under two seconds
(`registry-fetch.tsv`, `note` column).

**L0:** no.

### T5 — Huge response headers

**Exploit path.** The contract has no clause about response headers. The
stdlib refuses them, but with an exception class that a typical fetch wrapper
does not catch.

**Evidence (measured, probe section 5).** `http.client` rejects a header line
over 65536 bytes and more than 100 headers:

```
/big-header    http.client.LineTooLong | OSError=False :: got more than 65536 bytes when reading header line
/many-headers  http.client.HTTPException | OSError=False :: got more than 100 headers
caught by (OSError, URLError, ValueError, LookupError)? HTTPException                False
caught by (OSError, URLError, ValueError, LookupError)? InvalidURL                   False
```

`LineTooLong` and `TooManyHeaders` derive from `http.client.HTTPException`,
which is **not** an `OSError` subclass. The catch set used by the lane's own
control (`except (OSError, URLError, ValueError, LookupError)`,
`.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/control.py`) therefore
lets them escape. The same is true of `http.client.InvalidURL`, which is what
a URL carrying a bad port or userinfo raises.

**Impact.** One malformed header line from one host aborts the whole run with
an unhandled traceback and a nonzero exit, instead of producing one
`UNREACHABLE` line and continuing. Against the counter that is a failed
measurement, not a partial pass: the candidate's stdout is truncated, so the
remaining items score `<missing>`.

**Smallest safe implementation note.** Catch `http.client.HTTPException` and
`http.client.InvalidURL` in addition to the `OSError` family, and map **every**
fetch-time exception to `UNREACHABLE` for that item so the run continues. The
contract's verdict order then holds, since `UNREACHABLE` is listed for "the
fetch failed".

**L0:** no.

### T6 — Credentials in a URL

**Exploit path.** "no cookies or credentials" is a promise about the request
the tool makes. It says nothing about a registry *cell* that carries a URL
with userinfo, and it says nothing about what the tool prints when the fetch
fails.

**Evidence (measured, probe section 6).** `urllib` keeps the credential inside
the host field:

```
Request.host for http://alice:s3cr3t@example.invalid/x          -> 'alice:s3cr3t@example.invalid'
http://alice:s3cr3t@example.invalid/x -> http.client.InvalidURL | OSError=False :: nonnumeric port: 's3cr3t@example.invalid'
a naive stderr log line would print the secret:
  FETCH http://alice:s3cr3t@example.invalid/x failed nonnumeric port: 's3cr3t@example.invalid'
```

The exception text carries the secret. The counter persists the candidate's
stderr verbatim into its receipt (`c1-count.py`: `"stderr_tail": err[-2000:]`),
so a stderr line of the shape shown above writes a credential into a committed
record — which the corpus contract forbids outright ("No credential material,
ever", `/home/vgpnk/Projects/shokunin/CORPUS.md`).

**Registry facts, re-run:** `urls_with_userinfo=0` and `non_http_scheme_urls=0`
across all 49 rows. The hazard is latent: it needs a future registry row, or
a redirect whose `Location` carries userinfo.

**Smallest safe implementation note.** Refuse a URL with `parts.username` or
`parts.password` before the request, and never print the URL or the raw
exception text into stdout or stderr — print the source id and a fixed reason
string. Where a fetch is logged at all, log the source id, the status, the
byte count and a digest of the body, never the URL and never the exception
message. This is a narrowing inside the contract's "no cookies or credentials",
not a change of it.

**L0:** no.

### T7 — Logging page bytes to disk

**Exploit path.** The contract has no clause about persistence, and the
counter copies the candidate's stderr into a committed receipt. Two failure
modes: a page cache written into the repository tree, and page text echoed into
stderr and thence into the receipt.

**Evidence.** The frozen counter's reference function keeps the body in memory
and writes nothing (`c1-count.py`, `fetch_text`); the receipt captures
`stderr_tail` up to 2000 characters. The lane's control logs the right
shape — `FETCH {url} ok bytes={len(body)} sha256={…}` — which is counts and a
digest, not content. Note that the URL in that line is still a leak vector
under T6.

**Impact.** Third-party page content written into the lane tree or into a
committed receipt, plus a per-run cache would blur the "each URL at most once
per run" bound the contract states.

**Smallest safe implementation note.** Memory only: no cache file, no
temporary directory, nothing written outside the process. stdout carries
exactly the contract's lines (`QUOTE_REOPEN<TAB>…` per item in input order,
then `QUOTE_REOPEN_SUMMARY …`). stderr, if used at all, carries the source id,
status, byte count and body digest only.

**L0:** no.

---

## 4. Two contract-fidelity notes for the executor

* **"one retry" against "each URL at most once per run".** The only reading
  that satisfies both is: at most one *successful* fetch per URL per run, with
  at most one retry of a *failed* attempt, and the fetched text cached and
  reused for every item sharing that source id. The eight fixture sources are
  shared across all 130 items, so the cache is what keeps the run at eight
  fetches instead of 130. An unconditional retry would double the server hits
  and contradict the wave-2 offline expectation of one hit per URL.
* **Trailing-character strip.** The contract's "strips trailing `.,;)`
  characters" applied with `rstrip` also removes a legitimate `)` from a URL
  such as a Wikipedia path ending in a parenthesis. No registry row is
  affected today; implement as the contract states and treat it as a named
  fidelity limit rather than a security issue.

---

## 5. Province fit: is re-opening the lane's own registered sources a live-target fetch?

**Judgment: no, and no L0 question is needed.** Grounds, cited:

1. `PROVINCE.md` refuses "external live-target research without operator
   approval (loopback-only otherwise)" and owns "the external-target approval
   table for a research window; this lane's own corpus and gates". The refused
   activity is *research against an external live target*. The C1 tool has no
   target to choose: its subject is the lane's own `corpus/SOURCES.md`, and it
   re-opens pages the lane already opened once and registered — every row
   carries a tier, an anchor, an opened date and a located quote. It discovers
   no new external surface and probes nothing.
2. `CORPUS.md`'s SOURCES contract v1 makes opening the source a precondition
   of the corpus method, rule 1: "A row is a claim. Write it only after
   opening the source in the round that writes the row … Non-author
   verification re-opens a sample." Re-opening registered documentation
   pages *is* the corpus's own method, and the round-28 spot-check did
   exactly that (re-opened `https://docs.python.org/3/library/os.path.html`,
   opened 2026-10-22). A tool that performs the corpus's own re-verification
   step is not an out-of-province act.
3. The gate's executable refusal points the same way.
   `tools/research-gate.sh:670-671` refuses a *record pointer* to an external
   URL without an approved window (`EXTERNAL_WITHOUT_APPROVAL`), and
   `tools/research-gate.sh:1151` refuses a URL *source* ("url source refused
   (no external fetch)"). Both are checks on what a corpus record may cite,
   not on whether the lane may read a source it has already registered.
4. The operator's own instruction for this wave already grants exactly these
   fetches: the round-29 dispatch context permits "GET only, and only to
   (a) the http(s) URLs in the `source` column of …/corpus/SOURCES.md, or
   (b) the specific public documentation URL your task names". That is the
   approval the province demands, for this round and for the tool's own run.

**Residual, and where the L1 should put it.** The tool is a *standing*
capability: in later rounds it will fetch whatever URL a later registry row
names, and follow whatever redirect that row's host serves. The lane's
approval-table deliverable exists for exactly this purpose ("the
external-target approval table for a research window"), and its rows are all
`pending`. The lane owns that table, so the honest move is a lane-side
curation action, not an operator escalation: add one row naming "re-open
registered documentation sources", with the scope limit the contract already
states (GET only, registry rows only, no credentials, redirects confined to
the registry host set, one fetch per URL per run) and an approval state the
operator sets. If the L1 wants operator sign-off before a durable
network-capable command ships, that is a reasonable thing to ask — but it is
a lane-deliverable question, and it does not block the tool's landing.

---

## 6. Observations about the frozen counter (report only — the counter is frozen)

These are outside my remediation scope because the counter is frozen and must
not be edited. They are recorded because they interact with the tool's
verdicts.

* The reference `fetch_text` uses the default opener, so it follows redirects
  to any host, permits `ftp:` redirects, honours an ambient `http_proxy`, and
  inflates gzip without a bound (T1, T2, T3). It fetches only the eight
  registered fixture hosts, all of which are public and stay on-host, so the
  exposure is bounded today.
* The reference `fetch_text` never compares the read length with the 8 MiB
  cap, while the tool must. If a fixture page ever grows past 8 MiB, the
  counter would label from a truncated body while the tool reports
  `UNREACHABLE` — and the kill rule counts `UNREACHABLE` as a mismatch. No
  fixture page is near the cap today (largest inflated: 1,171,446 bytes), so
  this is a named future risk, not a present defect.
* The reference `fetch_text` reads only `8 * 1024 * 1024 + 1` wire bytes and
  then inflates that prefix, so a body larger than the cap raises
  `EOFError` inside the counter rather than returning a page — a counter-side
  fetch failure (exit 2, re-run, never scored as a pass), per the kill rule.

---

## 7. Limits of this review

* I did not fetch any external host. Every HTTP request in my probe went to a
  `127.0.0.1` server started by the probe script; the external facts I rely
  on (registry rows, redirect outcomes, content types, inflated sizes) come
  from re-run local commands over committed bytes and from the sibling seat's
  own fetch census at
  `.ufo/waves/round-29/build/ScoutRegistryFetch/registry-fetch.tsv`.
* I did not exercise the real `tools/quote-reopen.py`; it has not landed
  (`tools/` holds only `research-gate.sh`). The findings are about the frozen
  contract and the stdlib behaviour an implementer would inherit, not about
  landed code.
* Whether a specific future registry row is hostile is unobservable from
  here; my address and scheme checks are stated as the minimum, not as a
  proof that no registry row can be hostile.
* I did not install or update any tool. The probe uses only the Python 3
  standard library: `python3 -VV` → `Python 3.14.8 (main, Oct 2 2026, 10:23:31)
  [GCC 16.2.1 20260810]`.
* No process started by this seat remains running; the probe server is shut
  down inside `main()` before exit, and the probe exited 0.

**Files written by this seat** (both inside the seat's own directory, plus
this report):
`.ufo/waves/round-29/build/SentinelFetchBounds.md`,
`.ufo/waves/round-29/build/SentinelFetchBounds/probe_fetch_bounds.py`,
`.ufo/waves/round-29/build/SentinelFetchBounds/probe_output.txt`.

Report: .ufo/waves/round-29/build/SentinelFetchBounds.md
