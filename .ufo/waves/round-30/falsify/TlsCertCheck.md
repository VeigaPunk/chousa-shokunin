VERDICT: holds — C2's direct dial keeps TLS verification on: a self-signed or wrong-name cert gives no page text, and a real GET of S052 returns 200 with text

Seat: ChousaR30.TlsCertCheck (wave 2 falsify). Target: C2 must not have broken TLS certificate or hostname checks (the counters only exercise http).
Tool: `tools/quote-reopen.py` at lane tip a9d3a05a, SHA-256 47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201 (each receipt recomputes this and records it). Python 3.14.8, OpenSSL 3.6.5.
Probe: `.ufo/waves/round-30/falsify/TlsCertCheck/tlscheck.py` (SHA-256 dfec89b8…7f9ce7; scratch copy at /fast/scratch/hyaku/chousa-r30/w2/TlsCertCheck/). The probe loads the tool with importlib and calls `fetch_page(url)`. In local mode the only patch is `_check_address` replaced by a function that returns `['127.0.0.1']`; `DEADLINE` is set to 10. The server is a `ThreadingHTTPServer` on 127.0.0.1, wrapped with `ssl.PROTOCOL_TLS_SERVER`. The certs came from `openssl req -x509 -newkey rsa:2048 -nodes -subj /CN=localhost -addext subjectAltName=DNS:localhost,IP:127.0.0.1`, plus a second cert for `other.example`.

## Results (all four commands exited 0 under `timeout 60`)

| case | command (cwd scratch) | status | detail | text | server GETs |
|---|---|---|---|---|---|
| A: untrusted self-signed (the target) | `python3 tlscheck.py local cert.pem key.pem localhost` | None | `fetch failed: SSLCertVerificationError` | None | 0 |
| B: control, same cert trusted via `SSL_CERT_FILE=cert.pem` | same, with that environment variable | 200 | "" | `tls probe body sentinel words` (29 chars) | 1 |
| C: trusted cert for `other.example`, URL host `localhost` | `SSL_CERT_FILE=cert2.pem python3 tlscheck.py local cert2.pem key2.pem localhost` | None | `fetch failed: SSLCertVerificationError` | None | 0 |
| D: real GET of S052 (no patch) | `python3 tlscheck.py real "https://docs.python.org/3/library/socket.html#socket-timeouts"` | 200 | "" | 78397 chars, contains "Notes on socket timeouts", text SHA-256 bc1e8286…cbe5 | n/a |

Receipts: `.ufo/waves/round-30/falsify/TlsCertCheck/receipt-local-selfsigned.json`, `receipt-local-trusted-control.json`, `receipt-local-hostname-mismatch.json`, `receipt-real-s052.json`. Case D is a network fetch made at 2026-10-23T03:35:15Z (wall 0.162 s) to the registered S052 host only. The URL fragment was removed before the request.

- Case A matches the expected result: the certificate error gives no page text and the server never sees an HTTP request. Case B shows the server and the patched path both work, so the failure in A comes from the certificate check alone. Case C shows the hostname check is still on: `_dial` passes `server_hostname=host` to `ssl.create_default_context().wrap_socket` (tool lines 260-279, 390-392), even though the TCP connect goes to the numeric address.
- Case D: the fetch path, unpatched, reaches the real network over verified TLS (system trust store, with `SSL_CERT_FILE` and `SSL_CERT_DIR` unset) and returns page text.

## Low-severity observation (not a C2 defect)

- A certificate failure is retried once. `check_address_calls` lists 2 entries in cases A and C. `fetch_page` (tool lines 455-459) catches `ssl.SSLError`, which includes `SSLCertVerificationError`, and marks it `retryable = True`. The docstring of `_request_once` says retries are for "a transport-level failure" only. A certificate error will fail the same way again, so the second handshake does no useful work. It stays inside the shared deadline and returns no text, so contract item 3 and the C2 predicate are unaffected. [INFERENCE] The cost is 1 extra resolution and handshake for each failing https URL.

## Gaps

- Not tested: an expired cert, a cert signed by an untrusted intermediate, or TLS through an IPv6 address. The C1 and C2 counters were not run by this seat; other seats score them.
- No tools were installed or updated. All processes finished in the foreground; `pgrep -af tlscheck` found nothing left running.
