# HeldOut07 — held-out generalization attack on C1 (blind → tool)

Attacked: `tools/quote-reopen.py verify` on 3 located quotes never in the fixture —
h19 (S020), h20 (S021), h21 (S022) from
`.ufo/waves/round-29/build/ScoutGateQuotes/held-out.tsv`.

## Verdict: HOLDS (3/3 agree), with two findings, neither a tool defect

### STEP 1 — blind verdicts (my own bounded GET + contract replica, recorded before STEP 2)

Fetched each registry URL with `curl -L` (GET only, UA `chousa-quote-reopen
blind-check`), saved to `/fast/scratch/hyaku/chousa-r29/w2/HeldOut07/`, and applied
the frozen contract's HTML→text + NFKC + boundary rules via a scratch script
(`contract_text.py`, reimplementation, not the tool):

| item | source | status/ct/size I observed | blind verdict | basis |
|---|---|---|---|---|
| h19 | S020 w3.org PROV-O | 200 `text/html`, 464 179 B | VERBATIM | normalized page contains quote verbatim: "…usable. The properties prov:generatedAtTime and prov:invalidatedAtTime can be used to bound the starting and ending moments of an Entity's existence. The Activities…" |
| h20 | S021 pubmed 17638714 | **203** `text/html`, 5 590 B | ABSENT | body is a cookie/JS challenge ("Cookies must be enabled…challengeId"); quote text not present |
| h21 | S022 pubmed 28912002 | **203** `text/html`, 5 590 B | ABSENT | same challenge page |

Key blind detail: PubMed answers 203 + `text/html`, i.e. 2xx and an allowed content
type, so under the contract this parses to a text that lacks the quote → **ABSENT,
not UNREACHABLE**. The held-out TSV already tagged both rows
`[direct-get-challenge]`; the wave-1 scout knew they block plain GETs.

### STEP 2 — tool run

`items.tsv` written to `.ufo/waves/round-29/falsify/HeldOut07/items.tsv` (header
`id<TAB>source_id<TAB>quote`). Command from lane root:

```
timeout 300 python3 tools/quote-reopen.py verify --items .ufo/waves/round-29/falsify/HeldOut07/items.tsv
```

Output, exit 1:

```
QUOTE_REOPEN	h19	VERBATIM	matched in normalized page text
QUOTE_REOPEN	h20	ABSENT	no match in normalized page text
QUOTE_REOPEN	h21	ABSENT	no match in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=1 absent=2 too_long=0 no_source=0 unreachable=0
```

### Agreement: 3/3 AGREE — no DISAGREE items

### Finding F1 (freshness, minor): h20 is inexact as cited by the lane

The lane's quote is `A signal occurred within 2 years…` (capital A). The abstract
text (NCBI E-utilities rendering of the same record) reads "…However, a signal
occurred within 2 years for 23% of reviews and within 1 year for 15%. In 7%…" —
lowercase 'a' mid-sentence. Boundary check on the real text: the capital-A variant
does **not** match (case-sensitive contract); the lowercase variant does. So even
if PubMed served the real page, the lane's quote is ABSENT. It works as a
quotation in `lessons/round-25.md` because the lane promoted it to sentence-initial
capital — a normal quoting convention, but invisible to this contract. This is an
inexact-citation finding on the lane, not a tool defect, and it means h20 is
doubly ABSENT (challenge page + case).

### Finding F2 (contract limit, not a defect): 203 challenge pages read as ABSENT

PubMed's anti-bot response is 2xx with an allowed content type, so the contract
classifies these as ABSENT rather than UNREACHABLE. Semantically "the quote is not
in the served text" is literally true, but the verdict loses reachability
information — an operator reading ABSENT would conclude the source doesn't contain
the quote, when in fact the tool was refused. The frozen contract permits only
these five verdicts; a 203-body-detection rule is out of scope. h21's quote is
present verbatim in the real abstract (it is the LSR definition clause,
lower-cased mid-sentence as cited), so on a reachable fetch the tool would
correctly say VERBATIM.

## Operability assessment

The tool generalized to unseen registry rows without error: correct verdict on a
200 page (h19, including the typographic-apostrophe path the page uses for
"Entity's"), correct contract verdicts on challenge pages (h20, h21), exit code 1
as specified when any item is non-VERBATIM, one line per item in input order plus
the summary line, all within the 30 s/network bounds. No crash, no format
deviation, no hallucinated VERBATIM.

## Limits

- I did not run the frozen counter `c1-count.py` (not my assignment); this attacks
  the tool surface only.
- My blind check used a scratch contract reimplementation; agreement on all 3
  items means the tool and an independent reading converge.
- The `read` tool's fetch shortcuts (W3C API, NCBI E-utilities) bypass the
  challenge and confirmed both quotes exist verbatim-ish in the real content —
  supporting F1/F2 — but are not what the contract fetches.
- No installs or updates were needed; no files in the lane were mutated outside
  my report dir and `items.tsv` inside it.

Report: .ufo/waves/round-29/falsify/HeldOut07.md
