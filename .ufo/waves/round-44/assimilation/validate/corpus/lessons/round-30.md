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

### 2026-10-23 correction — ReviewContractV2 pointer (routed D8)

`corpus/lessons/round-30-verifier-spotcheck.md:58-60` identifies the line-57 pointer as wrong: the redirect-follow disclosure is `build/ReviewContractV2.md` finding 13, not finding 7. Finding 7 concerns item 2's wording (`.ufo/waves/round-30/build/ReviewContractV2.md:111-115`); finding 13 records the 301 → 307 → 200 chain and final WHATWG host (`.ufo/waves/round-30/build/ReviewContractV2.md:185-195`), followed by the off-registry GET/HEAD disclosure and deleted bytes (`.ufo/waves/round-30/build/ReviewContractV2.md:237-243`). The report records `curl -sS -L https://www.w3.org/TR/html52/syntax.html` and `curl -I -L https://www.w3.org/TR/html52/syntax.html` for the redirect chain. This is a pointer correction only; the earlier text remains unchanged.

## Census

Start (base `a3a3710e`): `scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin chousa` → `chousa ok`, exit 0; manual census 49
rows, 0 malformed, tier A 43 B 1 C 5, status mined 26 queued 19 rejected 4
(`.ufo/waves/round-30/build/ScoutCensus.md`). The end census is in SCORECARD.md
Round 30 and the round report.

### 2026-10-23 corrections to the Gate above (falsify wave)

- S052: the quote is not verbatim. The page reads "In timeout mode, operations
  fail if they cannot be completed within the timeout specified for the socket
  (they raise a timeout exception) or if the system returns an error." The
  located quote is "In timeout mode, operations fail if they cannot be completed
  within the timeout specified for the socket" (18 words); the landed tool read
  the Gate version as `ABSENT` (`.ufo/waves/round-30/falsify/AttackRowS052.md`).
  The row's teaching is unchanged.
- S055: the teaches cell said "when the socket is connected to a validated
  address", which the page does not say; corrected in `SOURCES.md`
  (`falsify/AttackRowS055.md`). S050: its scope said "superseded", which the
  page does not say; corrected (`falsify/AttackRowS050.md`).
- The other five Gate quotes were re-opened and the landed tool read each as
  `VERBATIM` (`falsify/AttackRowS05{0,1,3,4,6}.md`).

## Falsify wave findings (37 seats, `.ufo/waves/round-30/falsify/`)

- C1 holds: 106/106 in every re-run (RerunC1A, B, C: 9 runs; SeparabilityRevs;
  CriticClaimsAfter 14 runs). The N-version differential agrees on 200 of 200
  counter documents; 29 disagreements on hand-made shapes the counter does not
  generate (`DiffC1NVersion.md`). On the real S047 page the round-29 tool reads
  3 quotes `ABSENT` and the landed tool `VERBATIM` (`LiveS047After.md`).
- C2 is a miss: 26/27 on 3 of 44 fresh-seed runs of the landed tool
  (`RerunC2B.md`, `CriticClaimsAfter.md`). Each miss is a slow-ok item refused
  about 0.07 s after its DEADLINE. RerunC2B's diagnosis: the frozen harness
  server's listen queue (backlog 5) overflowed on loaded runs, delaying the
  connection; a scratch copy with backlog 128 scored 27/27 in 18 of 18 runs. The
  frozen counter is not changed and the claim is not re-scaled.
- Mutants: killed 9 of 10. Round-29 MutOrder 104, MutSkipScript 66, MutCasefold
  86 (routed D3 closed on the landed tool); MutHeadBodyOnly 88, MutTitleKept 86;
  MutNoWatchdog 25/27, MutReResolve 19/27, MutTruncAsFull 25-26/27,
  MutIgnoreDeadlineConst 19/27. Survivor: MutHeadNoText (text in head does not
  end it) scores 106/106, because in every headless-text document the inline
  markup or the next block start tag also ends the head. A coverage gap for a
  later counter.
- Separability holds: C2-only revision 78/106 and 27/27; C1-only build 106/106
  and 12-14/27 (`SeparabilityRevs.md`).
- No harm: the round-29 counter scored `QUOTE_REOPEN_MATCH=130/130` on the
  landed tool; `research-gate.sh` unchanged; round-1 command
  `VERDICT_BEARING_EXPORTS=3/3` (`NoHarmR29Counter.md`). TLS certificate and host
  name checks still refuse a self-signed or wrong-name certificate
  (`TlsCertCheck.md`).
- Security (`SentinelFetchLayer.md`): one validated resolution and TLS identity
  hold; the total deadline does not cover name resolution or dialing (medium);
  hop timers are not cancelled (low). Not claimed by C2's counter; carried.
- Reviews: corrections D1, D2, D4, D5 hold with low findings
  (`ReviewCorrections.md`: the D1 block understates a second DiffToolB network
  run; the D4 quote came through NCBI E-utilities, PubMed itself answers 203);
  QUALITY 26 to 29 pass their cited checks, with two defects in the evidence
  tools (`ReviewQuality30.md`); knowledge-entry defects fixed above
  (`ReviewKnowledge30.md`).

### 2026-10-23 correction (round 31, D2)

The statement above that the frozen harness's listen queue overflowed reports a cause as fact. The backlog explanation is **[INFERENCE]**, not established: `RerunC2B.md:45` labels the diagnosis `[INFERENCE]`, and `:57` says no per-connection record shows a dropped or delayed SYN. The 18/18 backlog-128 control is consistent with, but does not prove, that explanation (`.ufo/waves/round-30/falsify/RerunC2B.md:49-50`). Round-31 copies: `.ufo/waves/round-31/build/ExecD2Backlog/bl/`. The scored C2 misses remain misses under the frozen kill rule; this correction changes neither the result nor the frozen v4 bytes. Any future C2 counter version that sets `request_queue_size` must be declared before data as a new version; never edit the frozen v4 bytes. This append-only correction answers D2 in `corpus/lessons/round-30-verifier-spotcheck.md:169-174`.

### 2026-10-23 correction — routed D4

The C1 re-derivation above is corrected: 32 of 35 distinct committed after-receipts carrying landed tool SHA `47a657e7…` and frozen C1 counter SHA `5b312d84…` scored 106/106. The other three (`falsify/ConnectorKagiPin/c1-run2.json`, `falsify/MutR29Order/baseline.json`, and `falsify/MutR29SkipScript/baseline.json`) scored 0/106 under resource caps and are inconclusive. The stated 14/14 for `CriticClaimsAfter` is the combined count of 3 `CriticClaimsAfter` C1 receipts, 9 `RerunC1A/B/C` receipts, and 2 measurement receipts—not an additional 14 runs. `SeparabilityRevs` contributes 2 distinct receipts. This repairs the count routed by `corpus/lessons/round-30-verifier-spotcheck.md:178-181` without rewriting the earlier finding.

Evidence: `.ufo/waves/round-31/build/ExecD4Rerun/enum-output.txt:1-57` and `.ufo/waves/round-31/build/ExecD4Rerun.md:11-18,22-46` (recorded command exit 0).

### 2026-10-23 correction — routed D4 (`.ufo/waves/round-30/falsify/CriticClaimsAfter.md:31`)

The RerunC2B portion of the 03:43:52Z snapshot above is corrected: it was 20/23 at 27/27, not 17/20. The committed RerunC2B set has 23 distinct receipts: 20 printed 27/27 and 3 printed 26/27. With RerunC2A 5, RerunC2C 5, `measure/after-c2` 2, and this report's 9 C2 runs, the snapshot total remains 41/44. This corrects the defect routed by `corpus/lessons/round-30-verifier-spotcheck.md:178-181`.

Evidence: `.ufo/waves/round-31/build/ExecD4Rerun/enum-output.txt:167-192` and `.ufo/waves/round-30/falsify/RerunC2B.md:21-27,49-52`. The receipt-enumerator command and recorded exit code 0 are at `.ufo/waves/round-31/build/ExecD4Rerun.md:11-18`.

## Learning

Author view, for the outside check to rule on: expansion improved (C1 moves the
missing-`</head>` page class into held ground, with S050 to S056); quality
unchanged by count, with D1 to D6 repaired and one Gate quote (S052) caught by
the round's own re-open; discernment improved in process (four pre-data design
changes, each forced by a control) but C2 shows that a counter with a tight
timing slack can fail a candidate under host load.

### 2026-10-23 correction (D3)

The count in the paragraph above was wrong: the record shows three distinct control findings and two control-forced redesign versions, not four control-forced redesigns. CtlShapeKeyed's C2-v2 shortcut reached 20/20 and forced C2 v3; CtlNoReader's no-reader C1 control reached 104/106; and CtlTrivialC2 together with CriticClaimDesign30 identified the C2 slow-ok chunk-terminator timing defect. The latter two findings led to the C1 and C2 changes in v4, respectively. The earlier v2 redesign came from the L1's own read of exposed URL/host/order features before any control or data seat, not from a control. This is a count/attribution correction; the wording change altered no counter or harness bytes.

Evidence: routed D3, `corpus/lessons/round-30-verifier-spotcheck.md:175-177`; v2/v3/v4 history and L1-read account, `corpus/evidence/round30/claims.md:3-22,32-69`; C2-v2 20/20, `.ufo/waves/round-30/controls/CtlShapeKeyed/receipt-dns-header-c2-run1.json:336-343`; C1 104/106 with zero connections, `.ufo/waves/round-30/controls/CtlNoReader/receipt-relational-c1-h3.json:112-120`; slow-ok mismatch, `.ufo/waves/round-30/controls/CtlTrivialC2/receipt-do-nothing-c2-run1-v3.json:390-404`; timing finding, `.ufo/waves/round-30/controls/CtlTrivialC2.md:15` and `.ufo/waves/round-30/controls/CriticClaimDesign30.md:41`.

## Seats and holds

Control wave 8 seats (ordinary task call: 4 critic, 4 mutation-tester), build
wave 32 (validated v1), falsify wave 37 (validated v1): 77 seats. Dead seats:
CriticHarnessIntegrity (critic) refused with `code=cyber_policy`; CtlShapeKeyed
(critic) refused on its v3 follow-up ("triggered restrictions on violative
cyber content"), after its v2 result; CriticS047Live (critic) died on a provider
quota error (HTTP 429, "Individual quota reached"). Each is a hold, not retried;
the L1 re-scored CtlShapeKeyed's two committed controls itself
(`controls/L1Rescore/`). ScribeSrcOptionalTags declined a second GET outside its
assignment; the L1 opened S050 itself. ReviewContractV2 followed one redirect to
html.spec.whatwg.org (an unregistered host) and disclosed it.

### 2026-10-23 correction to the dead-seat record (routed defect D6)

The preceding “Each is a hold, not retried” statement is not accurate for `CriticS047Live`: after its provider-quota HTTP 429 (“Individual quota reached”), the S047 real-page task was re-issued in the falsify wave as `LiveS047After` under the same `critic` role. Record this as a retry; this correction does not rewrite the earlier account. Evidence: `corpus/lessons/round-30-verifier-spotcheck.md:65-69`; `.ufo/waves/round-30/build-spec.json:147-150` and `falsify-spec.json:122-125`; `.ufo/waves/round-30/build-dispatch.json:323-332` and `falsify-dispatch.json:268-277`; `.ufo/waves/round-30/falsify/LiveS047After.md:4-10`.

### 2026-10-23 correction to the criterion-29 control evidence (routed defect D6; `.ufo/waves/round-30/falsify/ReviewQuality30.md:44`)

`CriticHarnessIntegrity` refused with `code=cyber_policy`; `.ufo/waves/round-30/controls/CriticHarnessIntegrity/leak-map.py` and `metadata-audit.py` are unreviewed output of that refused seat, not reviewed control evidence. Do not rely on the preceding characterization of `leak-map.py` as a keyed control or on the inference that these files may cover item-order or registry-id shortcuts; their coverage remains unverified. The earlier text is retained unchanged. Evidence: `corpus/lessons/round-30.md:167-172` (Seats and holds, as landed in round 31); `timeout 30s git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show --stat abfdf932` and `timeout 30s git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show --format= --name-only abfdf932` (both list the two scripts); the name-only output contains no seat report, and a current-path check found `.ufo/waves/round-30/build/CriticHarnessIntegrity.md` and `.ufo/waves/round-30/build/CriticHarnessIntegrity/` absent.

## Census (end)

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
→ `chousa ok`, exit 0, with two W04 warnings (S051 and S050 share a page URL;
S053 and S052 share a page URL). Rows 49 → 56; tier A 43 → 50; status mined
26 → 33, queued 19, rejected 4.

### Misroot (2026-10-23)

Seat ConnectorKagiPin wrote its report at the fleet root
(`/home/vgpnk/Projects/shokunin/.ufo/waves/round-30/falsify/ConnectorKagiPin.md`) instead of the
lane. The L1 copied it byte-exact to `.ufo/waves/round-30/falsify/ConnectorKagiPin.md` (`cmp`
exit 0) and deleted the fleet copy. Captured-by: the misroot sweep; fix: the wave context
already names absolute paths, so the seat's relative write is the cause.

### 2026-10-23 correction to the v4 C1 control result (routed defect D5)

The 79/106 and 84/106 figures above are the strengthened no-reader control's two C1 scores, not the maximum across all v4 C1 controls. The committed all-control tally lists 61 receipts carrying the v4 counter hashes: the overall maximum is 86/106 in `.ufo/waves/round-30/controls/CtlParseShortcuts/receipt-skip-nothing-v4.json` (`n=86`, `t=106`, `predicate_holds=false`, `tool_rc=1`), while the best no-reader result is 84/106 in `.ufo/waves/round-30/controls/CtlNoReader/receipt-relational-v4-c1-v4-run2.json` (`n=84`, `net_connect_events=0`, `predicate_holds=false`). Evidence: `.ufo/waves/round-31/build/ExecD5Controls/tally_v4_receipts.out:1-4,64-77`; routed by `corpus/lessons/round-30-verifier-spotcheck.md:182-183`. This clarification adds the all-control comparison without changing the earlier lesson row.
