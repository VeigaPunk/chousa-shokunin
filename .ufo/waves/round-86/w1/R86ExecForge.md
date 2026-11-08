# R86ExecForge — C1 `D1`/203 coverage attack (K2)

Seat: `R86ExecForge`, lane `chousa`, round 86, wave w1. Attack surface: the round-86 C1 successor battery's forged-estate
coverage on committed bytes only — **no network**. All tool invocations read the tree extracted from landing revision
`667a5d091dc46168ed95eda0ae7f19a9bcf139a2`; the tool is that tree's own `tools/gate-records.py`.

## Revisions, bytes and the exact command forms

| object | revision / sha256 |
|---|---|
| landing tree attacked | `667a5d091dc46168ed95eda0ae7f19a9bcf139a2` (`git archive` → `/fast/scratch/hyaku/chousa-r86/R86ExecForge/tree`) |
| subject tool `tools/gate-records.py` | `fe204539b9b549ef1c6092a3963d73c7772946b027ab07da19c89961817aa287` = pin |
| frozen counter `corpus/evidence/round86/gate-records-r86.py` | `20bc1a733bd6c79f428a16c564cdc49555d8f02c389307eb2c6a28ceeb106d66` = pin |
| `corpus/evidence/round86/c2-positives.tsv` | `8c089828981bb0c8b5a0ab253bb4ec5f1537825cb84cea8964497310bb01f3c6` = pin |
| D1 record exactly as the counter builds it | sha256 `264389ac9588bef02d2cc198c334b3e7ff374e8ac037eb5c02db5e47b9b0d03f` (record built by calling the frozen counter's own `build_d1_203_admit()` — not re-typed) |
| S021 203 capture `corpus/captures/58725f5e0ac436166546a5ec.txt` | `7070b59c3434b67711f6a6ad723834ee1fce7a82230ac6970c1b12844c042a00` |

Every candidate was run as (exact form):

```sh
python3 -B <tree>/tools/gate-records.py verify \
  --root /fast/scratch/hyaku/chousa-r86/R86ExecForge/tree \
  --repo /home/vgpnk/Projects/shokunin/chousa-shokunin <record file>
```

Records and their hashes: `.ufo/waves/round-86/w1/R86ExecForge/records/` (`SHA256SUMS` in that dir).
Raw run receipts: `forge-run.txt` (candidates 1–5 + h01), `extra-run.txt` (c06/c07), `sweep-run.txt` (all committed
203 rows), `battery-run.txt` (the frozen predicate at landing), `forge-report.json` (machine copy of the candidate run).

## Candidate results (the required five, plus three boundary probes)

`expected` is the seat assignment's stated expectation; `match` compares the **observed code set** against it.

| # | candidate (record file) | observed verdict line | exit | codes | expected | match |
|---|---|---|---|---|---|---|
| 1 | `c01-d1-exact.md` — D1 exactly as the counter builds it | `…c01-d1-exact.md:1 S021 FAIL REFETCH` | 1 | `REFETCH` | `REFETCH` | **yes** |
| 2 | `c02-d1-quote-absent.md` — same record, quote absent (`words` kept consistent: 12) | `…c02-d1-quote-absent.md:1 S021 FAIL QUOTE_ABSENT,REFETCH` | 1 | `QUOTE_ABSENT,REFETCH` | `QUOTE_ABSENT`, *not* `REFETCH` | **partial**: `QUOTE_ABSENT` present; `REFETCH` also present (see F2) |
| 3 | `c03-reject-success-203.md` — `decision=reject capture=none curl_rc=0 http=203` | `…c03-reject-success-203.md:1 S021 OK` | **0** | — | `REFETCH` | **no — ACCEPTED** (F1) |
| 4a | `c04a-admit-curlrc-nonzero.md` — 203 admit shape + `curl_rc=7` | `…c04a-admit-curlrc-nonzero.md:1 S021 FAIL PARSE` | 1 | `PARSE` | `REFETCH` or `PARSE` | **yes** (refused as `PARSE`: the admit form admits no `curl_rc` key, `tools/gate-records.py:128-133`) |
| 4b | `c04b-reject-curlrc-nonzero.md` — reject/none, `curl_rc=7 http=203` | `…c04b-reject-curlrc-nonzero.md:1 S021 FAIL REFETCH` | 1 | `REFETCH` | `REFETCH` or `PARSE` | **yes** (refused as `REFETCH`: no row `S021/…/2026-11-08T02:15:39Z/7/203` exists in `corpus/evidence/round57/refetch.tsv`) |
| 5 | `c05-d1-words-plus-one.md` — D1 exact, `words=11` | `…c05-d1-words-plus-one.md:1 S021 FAIL REFETCH,WORDS` | 1 | `REFETCH,WORDS` | `WORDS` | **yes** (`WORDS` present) |
| 6 | `c06-reject-203-S022.md` — reject/none, `curl_rc=0 http=203`, S022 row | `…c06-reject-203-S022.md:1 S022 OK` | **0** | — | not in the seat's five; in-class check | **ACCEPTED** (F1, class breadth: it is every 203 row, not only S021) |
| 7 | `c07-admit-S032-cross-fetched.md` — S032 admit citing S021's `fetched` | `…c07-admit-S032-cross-fetched.md:1 S032 FAIL REFETCH` | 1 | `REFETCH` | `REFETCH` | **yes** (the refetch match is per-`sid`, `tools/gate-records.py:238`) |

Record bodies (verbatim, one line each):

```
c01 GATE-RECORD S021 url=https://pubmed.ncbi.nlm.nih.gov/17638714/ fetched=2026-11-08T02:15:39Z tier=A decision=admit capture=corpus/captures/58725f5e0ac436166546a5ec.txt capture_sha256=7070b59c3434b677 words=10 quote="Enable cookies for pubmed.ncbi.nlm.nih.gov and reload this page to continue."
c03 GATE-RECORD S021 url=https://pubmed.ncbi.nlm.nih.gov/17638714/ fetched=2026-11-08T02:15:39Z tier=A decision=reject capture=none curl_rc=0 http=203 words=0 quote=none
c06 GATE-RECORD S022 url=https://pubmed.ncbi.nlm.nih.gov/28912002/ fetched=2026-11-08T02:16:21Z tier=A decision=reject capture=none curl_rc=0 http=203 words=0 quote=none
c08 GATE-RECORD S032 url=https://pubmed.ncbi.nlm.nih.gov/17638714/ fetched=2026-11-08T02:15:50Z tier=A decision=reject capture=none curl_rc=0 http=203 words=0 quote=none
```

## Findings

### F1 `NOT_REFUSED` — a 203 record is accepted in the `decision=reject capture=none` form (candidates 3 and 6)

The tool accepts (`EXIT=0`, verdict `OK`) a record that cites exactly the committed 203 refetch row:
`curl_rc=0 http=203 decision=reject capture=none`. This is a **deviation from the seat assignment's stated expectation
`REFETCH`** — recorded as a `NOT_REFUSED` finding per the assignment's rule ("any candidate the tool accepts is a
`NOT_REFUSED` finding with its bytes").

Mechanism (`tools/gate-records.py:249`): `success = kv["curl_rc"] == "0" and kv["http"] == "200"`. A 203 is therefore
classified as a *non-success*, and the unreach leg (`tools/gate-records.py:249-252`) only requires `not success` plus a
matching committed row — which the S021/S022 203 rows are. Measured on all three committed 203 rows (three records, two
distinct URLs; `records/c08-reject-203-S032.md` → `S032 OK`, `EXIT=0`, receipt `extra-run.txt`): **3/3 accepted**. The accepted record is the honest record of the attempt: the
transport succeeded (`curl_rc=0`) and the decision was to reject the 203 body without capturing it.

Scope of the break: **not** the frozen D1 class. `claims.md` defines the class as "an **admit** record whose stored body
arrived under HTTP 203"; these records are `capture=none`, admit no body, and are not generated by the battery (the
battery's only unreach positive is S100 `curl_rc=28 http=000`, and it is a *positive*, expected `OK`). So K2's first
clause ("any in-class forged record is accepted") is not fired by F1 as the class is frozen; if the L1 reads "203-class"
as "any record citing a 203 row", F1 is an acceptance finding and K2 fires. That adjudication is the L1's; the bytes are
above.

### F2 `QUOTE_ABSENT,REFETCH` — `REFETCH` is unavoidable for any admit over the 203 row, so the seat's "not REFETCH" is unsatisfiable

Candidate 2 is refused with **both** codes. Candidate 1 (identical except the quote is grounded) shows `REFETCH` alone,
i.e. the 203 row alone raises `REFETCH` (`tools/gate-records.py:238`: the match requires `r[6] == "200"`). No record
citing the S021 203 row can be refused with `QUOTE_ABSENT` only.

The battery's expected-code test is a **subset (membership) test**, not equality — frozen counter line 411
`if code in v[1]:` (and line 414 sets `d1_refused = 1` on that membership). Consequence, stated as a coverage note, not
a breach: if the D1 leg were ever built with an ungrounded quote, it would be refused `QUOTE_ABSENT,REFETCH` and the
battery would still print `D1_REFUSED=1/1` (K2's letter "refused with a code outside its frozen expected set" is only
partially enforced by the instrument). On the **committed landing bytes this does not fire**: the D1 record the counter
builds has its quote located in the capture and is refused with exactly `{REFETCH}` (candidate 1, receipt `forge-run.txt`).

### F3 `REFETCH,WORDS` — word-count drift is not isolated (candidate 5)

`WORDS` is present as expected, alongside the unconditional `REFETCH`. Same subset-test note as F2.

### F4 no accepted admit over a 203 body — sweep of every committed 203 candidate

All refetch rows with `curl_rc=0`, `http!=200`, `txt_sha != "-"` were rebuilt as D1-style admits (registry tier, row
key/fetched/`txt_sha256`, the stored capture and a located quote) and run: 3 records, 0 accepted, 0 skipped.

```
sweep-run.txt:
S021 http=203 rc=1 FAIL REFETCH
S032 http=203 rc=1 FAIL REFETCH
S022 http=203 rc=1 FAIL REFETCH
TOTAL 3 ACCEPTED 0
```

So no in-class (`admit`/stored-203-body) forgery is accepted from committed bytes.

### F5 the battery's 203 estate is exactly one record; the second 203 rung contributes zero

`battery-run.txt` at landing:

```
TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=355/355 EXPECTED_CODE=355/355 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_FORGES=1 D1_REFUSED=1/1 MUT17_KILLED=1/1
GATE_RECORDS_R86=PASS
EXIT=0
```

`355 = 354 (round-85 estate, `controls/receipts/c1-k0b-frozen-instrument.txt` line 4) + 1 (the D1-203-admit)`: the
"D1-stale-refetch-txt-sha-drift" rung emitted **0** records, measured independently — the failed-attempt URL set
(`curl_rc=0`, `http!=200`, `txt_sha!="-"`: 2 distinct URLs, the pubmed/17638714 and pubmed/28912002 rows) has an empty
intersection with the 10 admit-positive URLs (`forge-report.json`, `both_status_groups: []`), so no admit exists whose
URL can be re-sha'd to a 203 body. The only 203-class forged record the predicate can generate is `D1-203-admit`
(`D1_FORGES=1`), confirmed by the landed run.

### F6 latent sha-shadow surface is empty in the committed refetch table

No `(sid, url)` group in `corpus/evidence/round57/refetch.tsv` has both a `curl_rc=0 http=200` attempt and a stored
non-200 attempt (`both_status_groups: []` in `forge-report.json`). An admit citing a 200 attempt while quoting the 203
body (the only shape that could be accepted with a 203-sourced quote) is therefore unreachable from committed bytes this
round. S021 and S032 share the same URL and capture key `58725f5e0ac436166546a5ec`, but both of their rows are 203, and
the per-`sid` refetch match rejects the cross-`sid` citation (candidate 7).

## Verdict on the seat assignment

- In-class (`admit`, stored 203 body) forgery accepted: **none** (F4) — K2 as frozen is **not** fired.
- Out-of-class 203 record accepted (`decision=reject capture=none curl_rc=0 http=203`): **yes**, on every 203 row
  (F1) — contradicts the assignment's stated `REFETCH` expectation; `NOT_REFUSED`, bytes above, L1 adjudication needed
  on whether that form is inside the class.
- Instrument weakness (not a live breach): D1's expected-code check is membership-only (F2/F3).

Risks: the D1 leg is a single generated record whose refusal is entailed by `http != 200`; the battery does not test
that a 203 admit is refused *for that reason alone*, and it does not generate any reject/none record over a 203 row.
No blockers; no network used; scratch `/fast/scratch/hyaku/chousa-r86/R86ExecForge` removed before yield.

VERDICT: R86ExecForge C1 held — no admit over a committed 203 body is accepted and the built D1 record is refused with exactly REFETCH, though a rejection-form 203 record (`capture=none`, `curl_rc=0`) is accepted on every 203 row, against the seat's stated expectation, and the D1 expected-code check is membership-only.
