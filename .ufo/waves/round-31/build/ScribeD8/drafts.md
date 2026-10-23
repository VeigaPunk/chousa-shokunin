# D8 append-only correction drafts — 2026-10-23

These blocks are ready to paste. They add dated clarifications only; no existing text is to be rewritten.

## 1. `corpus/lessons/round-30.md`

**Insertion point:** at the end of `## Gate`, after current line 67 and before `## Census` (line 69).

```md
### 2026-10-23 correction — ReviewContractV2 pointer (routed D8)

`corpus/lessons/round-30-verifier-spotcheck.md:58-60` identifies the line-57 pointer as wrong: the redirect-follow disclosure is `build/ReviewContractV2.md` finding 13, not finding 7. Finding 7 concerns item 2's wording (`.ufo/waves/round-30/build/ReviewContractV2.md:111-115`); finding 13 records the 301 → 307 → 200 chain and final WHATWG host (`.ufo/waves/round-30/build/ReviewContractV2.md:185-195`), followed by the off-registry GET/HEAD disclosure and deleted bytes (`.ufo/waves/round-30/build/ReviewContractV2.md:237-243`). The report records `curl -sS -L https://www.w3.org/TR/html52/syntax.html` and `curl -I -L https://www.w3.org/TR/html52/syntax.html` for the redirect chain. This is a pointer correction only; the earlier text remains unchanged.
```

## 2. `SCORECARD.md`

**Insertion point:** after current line 1654, at the end of the D1 correction block, before the Round 29 D2 heading at line 1656.

```md
### 2026-10-23 correction — second DiffToolB network run (routed D8)

The D1 correction above says the network evidence is “that one DiffToolB run only”; this omits a second recorded run of the landed tool. `corpus/lessons/round-30-verifier-spotcheck.md:197-198` routes this finding. The `landed-heldout` record in `.ufo/waves/round-29/falsify/DiffToolB/differential-receipt.json` binds the command below to `.ufo/waves/round-29/falsify/DiffToolB/landed-heldout.network.json`; the receipt records exit 1, 33 expected and 33 observed items, and `QUOTE_REOPEN_SUMMARY verbatim=26 absent=3 too_long=0 no_source=0 unreachable=4`:

```text
timeout --kill-after=5s 590s python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/DiffToolB/guarded-run.py /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/DiffToolB/landed-heldout.network.json tools/quote-reopen.py verify --items .ufo/waves/round-29/falsify/DiffToolB/held-out-3col.tsv --registry corpus/SOURCES.md
```

The bound network record contains 32 allowed GETs and 2 refused GET requests; its responses are 27 HTTP 200, 2 HTTP 203, 2 HTTP 301 and 1 HTTP 403 (`.ufo/waves/round-30/falsify/ReviewCorrections.md:25`). This is a second bounded network observation, not evidence that the counter itself fetches or that every registered URL is reachable. The recorded exit is not characterized as a pass. The earlier text remains intact.
```

## 3. `corpus/lessons/round-25.md`

**Insertion point:** after current line 269, at the end of the existing append-only correction to the round-25 Gate.

```md
### 2026-10-23 correction — provenance of the round-25 quote correction (routed D8)

The quote correction above is not verified by a retained fetch from a registered source. The seat report says the reader returned the PubMed abstract via NCBI E-utilities (`.ufo/waves/round-30/build/ScribeD4H20.md:3`); the routed finding is `corpus/lessons/round-30-verifier-spotcheck.md:199`. The review records `git grep -i eutils a9d3a05a -- corpus/SOURCES.md` as finding zero rows, and states that no response bytes or hash were kept for that E-utilities retrieval (`.ufo/waves/round-30/falsify/ReviewCorrections.md:26`). A separate GET to the registered PubMed URL did not verify the quote: `.ufo/waves/round-30/falsify/ReviewCorrections/receipt-pubmed-17638714.json` records the GET command, exit 0, HTTP 203, a cookie-gate body, zero quote matches and no redirects. The quote therefore remains unconfirmed by retained registered-source bytes; this provenance correction does not change the S021 or S032 admission statuses. The earlier text remains unchanged.
```

## Fleet-report-only note for the round-31 report (no lane edit)

The routed spot-check `corpus/lessons/round-30-verifier-spotcheck.md:194-196` also flags report-only items: the fleet report cites `7908ce2a` where the C2 v3 counter bytes are `bf657822`, omits work item `dad857af`, and gives `03:52Z` although the report commit is `03:50:30Z`. These are outside the lane-owned targets; carry them into the round-31 report rather than editing a lane file.
