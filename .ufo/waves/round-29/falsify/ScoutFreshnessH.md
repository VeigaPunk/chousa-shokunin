# Wave-2 FALSIFY — C1 operability (ScoutFreshnessH)

Scope: re-derive the frozen C1 predicate, attack the landed verifier with mutants and
guard probes, and (read-only by-product) run the tool over the 33 held-out lesson quotes.
Lane root for every command: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
No production file was edited; my only writes are inside
`.ufo/waves/round-29/falsify/ScoutFreshnessH/` and scratch
`/fast/scratch/hyaku/chousa-r29/w2/ScoutFreshnessH/`.

## Verdict: C1 HOLDS

Frozen predicate, verbatim:
`python3 corpus/evidence/round29/c1-count.py -- python3 tools/quote-reopen.py verify`

| run | seed | QUOTE_REOPEN_MATCH | counter exit | tool wall |
|---|---|---|---|---|
| 1 (`--receipt rederive-receipt.json`) | 13173258806708832500 | 130/130 | 0 | 2.29 s |
| 2 (frozen form, no receipt) | 12970099299958901445 | 130/130 | 0 (final unpiped run `rederive3.out`) | 2.25 s |
| 3 (frozen form, no receipt) | 3497534629407128034 | 130/130 | 0 | 2.27 s |

Every run drew a fresh 64-bit seed, so the three scores are independent and no
wave-1 receipt could be replayed into them.

Identity of what was scored: `sha256(tools/quote-reopen.py)` =
`72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea`, byte-identical to
`git show 30c9d24da1815e01e161ed2f52d5f951005cc2b8:tools/quote-reopen.py` (same sha256);
lane HEAD `b18b3ec`; `git status --porcelain tools/quote-reopen.py corpus/evidence/round29/`
is clean except untracked `__pycache__/`.
`sha256(corpus/evidence/round29/c1-count.py)` = `cd50965032278c35...` and both wave-1
receipts (`after-run1.json`, `after-run2.json`) carry `counter_sha256` starting
`cd50965032278c35`, `predicate_holds: true`, `cmd: ["python3","tools/quote-reopen.py","verify"]`.
The counter reads `cells[2]` of each registry row through `registry_url`, i.e. exactly the
`source` column the claim names; `corpus/SOURCES.md` has 49 row ids and no duplicate id,
so `rows.setdefault` cannot silently pick a stale row.

## Mutants (counter discriminating power)

Stubs in scratch, run through the frozen counter from the lane root:

| mutant | behaviour | score |
|---|---|---|
| `stub_all_verbatim.py` | prints VERBATIM for every item, exit 0 | 52/130 |
| `stub_fixture_oracle.py` | reads the committed 40 fixture items + labels, answers by content, guesses VERBATIM for anything unseen, no network | 78/130 |

The label arithmetic closes against those numbers: fixture classes give 14 VERBATIM and
20 ABSENT plus 3 TOO_LONG and 3 NO_SOURCE (40 items); the run-time variants add 14
subspan VERBATIM, 14 transpose ABSENT, 14 crossattr ABSENT; the page samples add 24
window VERBATIM and 24 page-transpose ABSENT. Total VERBATIM = 14 + 14 + 24 = 52 (the
always-VERBATIM ceiling), and 40 + 14 + 24 = 78 for the oracle that only knows committed
bytes (the no-fetch ceiling). A candidate that cannot reach the live pages is capped at
78/130, so the page-sampled half of the counter is genuinely fetch-gated.

## Guard probes (`_check_url` + `_check_address`, called directly)

REFUSED: `file://`, `ftp://`, userinfo URL, `127.0.0.1`, `[::1]`, `localhost`,
port 99999, and the cloud-metadata address `169.254.169.254`. One oddity: `https://host:0/`
is ALLOWED by the port check (port 0 connects nowhere, so it degrades to UNREACHABLE, not
an SSRF path). Registry URLs carry no userinfo, no port, and no non-global host, so the
guards never fire on the real corpus.

## Held-out freshness by-product (33 quotes, 32 source ids, 31 distinct URLs)

Command, 600 s bound, exit 1 (correct: not all VERBATIM):
`python3 tools/quote-reopen.py verify --items .ufo/waves/round-29/falsify/ScoutFreshnessH/heldout-3col.tsv`
Wall 16.10 s. Summary line: `verbatim=27 absent=3 too_long=0 no_source=0 unreachable=3`.
Input is a 3-column copy of `build/ScoutGateQuotes/held-out.tsv` (`heldout-3col.tsv`);
raw output in `heldout-run1.out`.

By lesson round:

| round | items | VERBATIM | ABSENT | UNREACHABLE |
|---|---|---|---|---|
| round-24 | 17 | 14 | 1 | 2 |
| round-25 | 11 | 9 | 2 | 0 |
| round-26 | 4 | 3 | 0 | 1 |
| round-28 | 1 | 1 | 0 | 0 |
| total | 33 | 27 | 3 | 3 |

By source: 30 of 32 source ids are VERBATIM; S006 appears twice (1 VERBATIM, 1 ABSENT);
S011, S014, S037 are UNREACHABLE; S021, S022 are ABSENT.

Non-VERBATIM items, origin line, and cause:

| id | source | origin | verdict | cause |
|---|---|---|---|---|
| h05 | S006 | `lessons/round-24.md:53` `[summary-not-verbatim]` | ABSENT | not a quotation: the arXiv HTML (39,716 chars, 200) contains the §3.3 headings, and the best contiguous token run is 7 of 19 tokens (`Fact Check validates factual accuracy against source`); the item is a composite summary, correctly absent |
| h10 | S011 | `lessons/round-24.md:58` `[pdf-source]` | UNREACHABLE | registry URL is `trec.nist.gov/.../Overview_rag.pdf`; `application/pdf` is outside `ALLOWED_TYPES`, so the tool refuses by design |
| h13 | S014 | `lessons/round-24.md:61` | UNREACHABLE | direct GET returns HTTP 403; the page is live for a reader client (same sentence appears in the served text), so this is a challenge/UA block at the origin, not page drift |
| h20 | S021 | `lessons/round-25.md:70` `[direct-get-challenge]` | ABSENT | PubMed direct GET returns HTTP 203 with a 129-char `Cookies must be enabled` gate page; additionally the quoted sentence is sentence-cased (`A signal`) while the real abstract reads `However, a signal` — `found()` does not casefold, so lowercasing the quote makes it match and the capital does not |
| h21 | S022 | `lessons/round-25.md:71` `[direct-get-challenge]` | ABSENT | same HTTP 203 cookie gate; against the real abstract text `found()` returns True, so the quote is verbatim and only the gate hides it |
| h29 | S037 | `lessons/round-26.md:43` `[pdf-source]` | UNREACHABLE | Cochrane LSR guidance is a PDF; refused by `ALLOWED_TYPES` |

No item failed for page drift or for a `<head>`-only location. h32 (S029,
`[spans-lines-48-49]`) is VERBATIM, so a lesson quote spanning two source lines still
matches after whitespace collapse.

Stability of the 8 page-sampled fixture sources (`S002 S003 S008 S013 S019 S020 S038
S044`, the VERBATIM fixture ids): 3 direct GETs each, 24 of 24 returned 200 `text/html`
with byte-identical extracted lengths (e.g. S003 152,293; S020 185,679). The flake risk
of the 130/130 predicate from these hosts is low today.

## Limits of this attack

- C1 is fixture-scoped. The freshness run above is data, not part of the predicate, and
  its 6 non-VERBATIM items sit on sources the counter never page-samples.
- A transport gate page that returns 2xx is reported as ABSENT, not UNREACHABLE
  (observed with PubMed's 203). This does not endanger C1 — a gate page on a page-sampled
  source would make the counter's own window extraction fail and exit 2 rather than
  score 130/130 — but it does mean `ABSENT` in a freshness report can mean "page blocked".
- PDF-backed registry rows are structurally unverifiable by this tool.
- `found()` is case-sensitive by design; a lesson quote capitalized at a mid-sentence
  start is a false ABSENT (h20).
- The tool refuses loopback/non-global addresses, so it cannot be exercised against a
  local test server; guard behaviour was probed by calling `_check_url`/`_check_address`
  directly instead.
- Not re-run: HEAD-level mutation of the tool (forbidden — the tool is frozen) and
  redirect-chain behaviour (needs a live redirect to an off-registry host; guards were
  verified statically and by direct call).

Tooling installs: none. No package manager, no network beyond the registry URLs.
