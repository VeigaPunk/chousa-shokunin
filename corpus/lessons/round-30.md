# Round 30 — quote re-open: the head boundary and the fetch bounds

Dates are UTC (the host clock reads UTC-3). Base
`a3a3710e3d0adf2f95882292f17b5093e3baf97c`. This round works only the routed
list of the round-29 outside spot-check (D1 to D7). Two claims, both on
`tools/quote-reopen.py`: C1 coverage (pages that omit `</head>`, routed D7 and
D3) and C2 operability (the stated fetch bounds under slow senders and DNS
rebinding, sentinel findings T4 and T1, routed D7). Frozen design:
`corpus/evidence/round30/claims.md` (design v4 at `abfdf932`, wording at
`60d51f79`). Landed tool: `49b2aa3006d3c44a29b171ab30df09776c21405d`.

## Spot-check intake

| Previous outside finding | Disposition in round 30 |
|---|---|
| D1, "live" wording rests on evidence outside the counter (`round-29-verifier-spotcheck.md:143-147`) | dated correction under the round-29 capabilities table in `SCORECARD.md` cites the DiffToolB network receipt (8 GETs, 8 responses 200, one run); new prose avoids the word; QUALITY 26 with a check shown able to fail |
| D2, 6 re-runs reported, 5 committed (`:148-150`) | dated corrections in `SCORECARD.md` and `LOG.md`; checker `corpus/evidence/round30/rerun-check.py` prints `RERUN_RECEIPTS=5/6`, exit 1, against the stated 6; QUALITY 27 |
| D3, three surviving mutants (`:151-153`) | the C1 counter carries script windows, case flips and verdict-order items; the round-29 mutants score 76, 66 and 72 on it against the round-29 tool's 78 (`.ufo/waves/round-30/build/CriticD3Classes.md`); the falsify wave re-applies them to the landed tool; QUALITY 28 |
| D4, the round-25 Gate quote at `lessons/round-25.md:70` (`:154-155`) | dated correction appended to `lessons/round-25.md` with the verbatim quote ("However, a signal occurred …"); meaning and admission unchanged |
| D5, chronology wording (`:156-159`) | dated correction appended to `lessons/round-29.md`: "before either primary executor scored its candidate", with the v1 reference baseline (82/82) and the MutateCounter replays disclosed. This round's control wave forbade full-contract baselines in its context |
| D6, snapshot-control code in scratch (`:160-161`) | `offline_snapshot_control.py`, `prepare_snapshots.py`, `network_guard.py` and a manifest of all six scratch files (size, SHA-256, mtime) committed under `.ufo/waves/round-30/build/ExecD6Snapshot/`; hashes match the round-29 report; the page-text file `snapshots.json` stays out of the lane (third-party text) and is listed by hash |
| D7, carried items (`:162-163`) | missing `</head>` is C1; T1 and T4 are C2; 2xx challenge pages and the L0 fetch-scope question (fleet `8d77e6c1`, unanswered, `ScoutOperatorLessons.md`) stay carried |
| operator `*.md` teachings | none exist in the lane (`.ufo/waves/round-30/build/ScoutOperatorLessons.md`) |

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| A counter's item URLs showed the item's class | design v1 at `f42906d7`: C2 paths `/drip-head/`, `/stall/`, `/slow-ok/`; C1 host names carried the document index (`claims.md`, "Design v2 note") | the L1's own read before any seat; QUALITY 24 | opaque per-run URLs and host names, shuffled plan and registry rows, run map hidden from the candidate (v2). QUALITY 29 |
| A label that is constant per class, and a response shape per class, let a control meet the counter without the work | C2 v2: `dns_header_keyed.py` met 20/20 (`.ufo/waves/round-30/controls/CtlShapeKeyed/receipt-dns-header-c2-run1.json`) | the pre-data control wave (QUALITY 24) | v3: fair-coin labels on fetchable items, one response head shape for every item, a drip-steady class, a per-item DEADLINE. Shown able to fail: the same control scores 13/27, 16/27 (v3) and 16/27 (v4) (`controls/L1Rescore/`). QUALITY 29 |
| Item shape carried the label | C1 v2: a no-reader control reached 104/106 from quote length, shared words and case patterns (`controls/CtlNoReader/receipt-relational-c1-h3.json`) | the control wave | v4: one length range, disjoint spans, inner capitals in ordinary words, case swaps both ways; the strengthened no-reader control fell to 79/106 and 84/106 (`controls/CtlNoReader.md`) |
| A counter that would reject a correct tool | C2 v3 harness sent a seventh paced piece for chunked slow-ok, so a page labelled VERBATIM finished after its DEADLINE when DEADLINE > 5.6 s (`controls/CtlTrivialC2.md`, `controls/CriticClaimDesign30.md`) | the control wave | v4 sends the chunk terminator with the sixth piece and ends the body at DEADLINE - 1.0 s |
| Two passing runs of a randomized counter were read as coverage | the C2 executor's candidate scored 27/27 twice in its seat; the L1's first run on the landed revision `33dd643f` scored 24/27: an end of stream caused by the deadline timer was read as a complete page (`.ufo/waves/round-30/measure/revA-c2-run1.json`) | the counter itself, on the next fresh seed | the tool reads an end of stream at the deadline, or before a declared length, as `UNREACHABLE` (`bd43bd53`); the falsify wave re-runs the counter on many seeds |
| The L1 truncated two lesson files while appending a correction (`open(path, "w")` evaluated before the read) | `git diff --numstat` showed `corpus/lessons/round-25.md` 3+/259- and `round-29.md` 2+/119- before any commit | the L1's diff check before commit; none in a rule | restored from the branch with `git show master:<path>`, appended again; a deletion count in `git diff --numstat` stops a commit |
| A rejected edit followed by a commit in the same batch | `claims.md` landed at `bf657822` without the v3 header because the edit had been refused; corrected at `7908ce2a` | the L1's read of the file head | never batch an edit and its commit; commit only after the edit reports success |

## Gate

Sources opened between 03:15 and 03:25 UTC on 2026-10-23. Each quote is at
most 25 words, copied from the opened page. The falsify wave re-opens each
one, with the landed tool as well as by hand.

| Row | URL | Located quote | Verdict |
|---|---|---|---|
| S050 | https://www.w3.org/TR/2017/REC-html52-20171214/syntax.html#optional-tags, §8.1.2.4 | "A head element’s end tag may be omitted if the head element is not immediately followed by a space character or a comment." | admit, tier A spec (dated W3C snapshot, superseded), mined; opened by the L1 (HTTP 200, 4415303 bytes, SHA-256 `1db65aef…e141`) |
| S051 | same page, §8.2.5.4.4 "in head" insertion mode, branch "Anything else" | "Pop the current node (which will be the head element) off the stack of open elements." | admit, tier A spec, mined (`build/ScribeSrcInHead.md`) |
| S052 | https://docs.python.org/3/library/socket.html#socket-timeouts | "In timeout mode, operations fail if they cannot be completed within the timeout specified for the socket." | admit, tier A docs, mined (`build/ScribeSrcSocketTimeout.md`) |
| S053 | https://docs.python.org/3/library/socket.html#socket.create_connection | "it will try to resolve it for both AF_INET and AF_INET6, and then try to connect to all possible addresses in turn" | admit, tier A docs, mined (`build/ScribeSrcCreateConnection.md`) |
| S054 | https://docs.python.org/3/library/http.client.html#http.client.HTTPConnection | "blocking operations (like connection attempts) will timeout after that many seconds" | admit, tier A docs, mined (`build/ScribeSrcHttpClient.md`) |
| S055 | https://docs.python.org/3/library/ssl.html#ssl.SSLContext.wrap_socket | "pass server_hostname to wrap_socket() in order to match the hostname." | admit, tier A docs, mined (`build/ScribeSrcSslSni.md`) |
| S056 | https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Address.is_global | "True if the address is defined as globally reachable by iana-ipv4-special-registry (for IPv4) or iana-ipv6-special-registry (for IPv6)" | admit, tier A docs, mined (`build/ScribeSrcIsGlobal.md`) |

Rejected source: `https://www.w3.org/TR/html52/syntax.html#optional-tags`, the
undated W3C URL. It answers 301, then 307, to html.spec.whatwg.org, a host the
lane has not registered, while the fetch-scope L0 question is open. Two seats
stopped at the redirect (`build/ScribeSrcOptionalTags.md`); one followed it once
and disclosed it (`build/ReviewContractV2.md` finding 7). Flip: the operator
registers the WHATWG HTML Standard host, or answers the L0 question.

Rejected inference: "C2 at 27/27 shows the tool is safe against DNS rebinding
and slow senders on the real network." The counter is loopback only and plain
HTTP; it does not test TLS, IPv6, resolver time or per-hop provenance
(`claims.md` "Not claimed"). Flip: none from this counter; it needs its own
predicate.

Status changes: none to existing rows. New rows S050 to S056 enter as `mined`,
used by `corpus/knowledge/quote-reopen-r30.md`.

## Census

Start (base `a3a3710e`): `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin chousa` → `chousa ok`, exit 0; manual census 49
rows, 0 malformed, tier A 43 B 1 C 5, status mined 26 queued 19 rejected 4
(`.ufo/waves/round-30/build/ScoutCensus.md`). The end census is in SCORECARD.md
Round 30 and the round report.
