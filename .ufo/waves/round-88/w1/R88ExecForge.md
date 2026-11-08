# R88ExecForge — C1 forgery battery (round 88, w1)

Seat: `R88ExecForge` — forge in-class records against the frozen C1 predicate.
Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Base/freeze `4ea9d008abfd2e09cb51649a42678a78f52ac530`.
Tree built by `git archive 4ea9d008… | tar -x` into `/fast/scratch/hyaku/chousa-r88/R88ExecForge`.
Frozen predicate: `corpus/evidence/round88/claims.md` (C1: K1–K4). Subject tool `tools/gate-records.py` unchanged.

**Tooling note:** no tool installs were needed. `python3 -B`, `git archive`, `tar` only. No network used.

## Axes
1. 203-binding correctness (D1/D2 classes exact-203).
2. Forged-record acceptance (K2 — any accept = finding).
3. Width-derivation robustness (ROWS_203 = 3 pin).
4. Escape-hatch coverage / grammar exactness (PARSE vs REFETCH code).

## Baseline (receipt `receipts/battery-r88.txt`)
Ran `python3 -B corpus/evidence/round88/gate-records-r88.py --root <tree> --repo <lane> --work <tree>`:
`TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15`, `LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15`, `GATE_RECORDS_R88=PASS`, exit 0. Predicate held at landing.

## Committed 203 estate (ground for all forgeries below)
`corpus/evidence/round57/refetch.tsv` `curl_rc=0 http=203` rows (3):
- `S021 https://pubmed.ncbi.nlm.nih.gov/17638714/ key=58725f5e0ac436166546a5ec fetched=2026-11-08T02:15:39Z txt=7070b59c…`
- `S032 https://pubmed.ncbi.nlm.nih.gov/17638714/ key=58725f5e0ac436166546a5ec fetched=2026-11-08T02:15:50Z txt=7070b59c…` (same URL/capture as S021, later attempt)
- `S022 https://pubmed.ncbi.nlm.nih.gov/28912002/ key=ff9013bd7d9387e45cd6e000 fetched=2026-11-08T02:16:21Z txt=7070b59c…`
Both captures are 190 bytes; the only quotable line (8–25 words) is ` Enable cookies for pubmed.ncbi.nlm.nih.gov and reload this page to continue.` (L13, 10 words). Registry tier for S021/S022/S032 is `A`.

## (a) The two 203 classes

| # | Forgery | Expected | Observed (tool) | Verdict |
|---|---|---|---|---|
| a1 D1 admit, quote = first quotable line of the 203 capture, `capture_sha256=7070b59c3434b677` (real 16-hex prefix), correct url/key/fetched/tier | `REFETCH` | `S021 FAIL REFETCH`, exit 1 (`receipts/a1-d1-admit-first-line.txt`) | refused, exact code |
| a2 D2 reject `http=200 curl_rc=28` on committed `S103 …/c1b0…af.pdf fetched=2026-10-27T08:05:52Z tier=B` (real committed refetch row rc=28 http=200, txt `-`) | grammar: `curl_rc=28≠0` ⇒ not success ⇒ refetch row exists ⇒ **OK** (correct acceptance, not a forgery of the failure-grammar: exit was genuinely non-zero) | `S103 OK`, exit 0 (`receipts/a2-d2-reject-200-rc28.txt`) | accepted **and correct** — grammar permits non-zero rc with any status; not a K2 finding (the row really exists; the tool's own doc: "Only a non-2xx status or a non-zero curl exit denotes a failure") |
| a2b contrast: `http=200 curl_rc=0` S103 (no such refetch row) | `REFETCH` | `FAIL REFETCH`, exit 1 | refused, exact code |
| a3 D2 reject 203, `fetched`=S032's attempt (02:15:50), sid S021 | `REFETCH` (no S021 row at that fetched) | `FAIL REFETCH`, exit 1 | refused, exact code |
| a3b D1 admit 203, fetched=S032's attempt on S021 | `REFETCH` | `FAIL REFETCH`, exit 1 | refused, exact code |

No K2 acceptance in class (a). The one acceptance (a2) is a genuine committed row and conforms to the stated grammar — flagging it as a bearing issue would be wrong: it is the grammar working as documented.

## (b) Width pin

Built `atkA/refetch-b1.tsv` (S008 row appended: `rc=0 http=203 txt=real sha256`, quotable capture) and `refetch-b2.tsv` (same but `txt=000…0`).
Direct derivation evaluation:
- clean: `q=3 c=3 d3=3`
- b1: `q=4 c=4 d3=4 d1=4 d2=4` — **all three move together**; battery `D1_WIDTH` requires `len(d1)==d1_expected==div3==ROWS_203(3)` ⇒ 4≠3 ⇒ width legs fail. A *real* new committed row moves the third derivation with the other two and the freeze pin catches it (predicate is frozen at 3).
- b2: `q=3 c=3 d3=4` — the hash-junk row moves only the third derivation; `D1_WIDTH` = `3/3/4` fails. Split is caught in both directions.

No width forgery survives. The pin assumes the committed bytes are the estate (a forged refetch row *is* a new estate member, and `ROWS_203` is a frozen measured count — arguably a new claim, exactly as claims.md says).

## (c) Escape hatches

On the D1 S021 forge (refuse target):

| Forgery | Observed | Verdict |
|---|---|---|
| `BOM` prefix | `FAIL REFETCH` exit 1 (`receipts/c1-bom-admit.txt`) | detected, exact code |
| zero-width-space (U+200B) prefix | `FAIL REFETCH` exit 1 (`receipts/c2-zwsp-admit.txt`) | detected, exact code |
| 3-space indent | `FAIL REFETCH` exit 1 (`receipts/c3-indented-admit.txt`) | detected, exact code |
| record inside a ```` ``` ```` fence (line 2) | `FAIL REFETCH` exit 1 (`receipts/c4-fenced-admit.txt`) | detected, exact code |
| duplicate `GATE-RECORD GATE-RECORD S021` | `FAIL PARSE` exit 1 (`receipts/c5-dup-gate-record.txt`) | refused; code is `PARSE` not `REFETCH` — expected `PARSE` (line doesn't match `^GATE-RECORD (S…)` with single space) |

Genuine positive (S203, round-81) with hatches — harm probes, all OK (no K3 harm from hatch-tolerance):
`c6-bom` OK, `c7-zwsp+bom` OK, `c8-indented` OK, `c9-fenced` OK (`:2`), `c10` same record twice on two lines: both OK (`records=2 ok=2`, exit 0).
Hatch-tolerance is bidirectional by design (`lead_strip` strips whitespace + Cf): a record cannot hide by formatting, and the tool is honest about duplicates. No K2 acceptance, no K3 harm.

## (d) url/unreach grammar

| # | Record | Observed | Verdict |
|---|---|---|---|
| d1 `curl_rc=0 http=299` | `FAIL REFETCH` exit 1 (`receipts/d1-rc0-http299.txt`) | success-2xx ⇒ refused with expected `REFETCH` |
| d2 `curl_rc=0 http=300` | `FAIL REFETCH` exit 1 (`receipts/d2-rc0-http300.txt`) | non-success but no committed row ⇒ refused `REFETCH` (doc-correct: 300 is not success; failure is decided by committed-row existence) |
| d3 `curl_rc=1 http=203` S021/S032 203 row rewritten | `FAIL REFETCH` exit 1 | no committed row with `curl_rc=1 http=203` ⇒ refused `REFETCH` |
| d4 `curl_rc=0 http=200` S022 (fabricated row) | `FAIL REFETCH` exit 1 | refused |
| d5 `curl_rc=0 http=199` | `FAIL REFETCH` exit 1 | refused |
| d6 `curl_rc=0 http=204` | `FAIL REFETCH` exit 1 | refused |
| e1 `http=000 rc=0` | `FAIL REFETCH` | refused |
| e2 `http=999 rc=0` | `FAIL REFETCH` | refused |
| e3 `http=299 rc=5` | `FAIL REFETCH` | refused (no such committed row) |
| e4 `http=200 rc=1` | `FAIL REFETCH` | refused |
| e5 `http=100 rc=0` | `FAIL REFETCH` | refused |
| e6 double-space separator | `FAIL PARSE` | exact code (tokens split on single space → empty token) |
| e7 tab separator | `FAIL PARSE` | exact code |

**Note on (d2):** `curl_rc=0 http=300` is *not* refused for being a "successful" status — 300 is outside 200–299, so `success=False`; it's refused because no refetch row matches `rc=0 http=300` for S022. The grammar is `success ⇒ REFETCH; else row must exist`. This matches the tool doc verbatim and is the conservative direction (refuse on committedness, not on status table).

## Summary
- 28 forgeries/probes run. **Zero accepted forgeries.** Every forged record refused with exactly its expected code (`REFETCH`, or `PARSE` for the two malformed lines where `PARSE` is the frozen expectation).
- The single acceptance (a2, `curl_rc=28 http=200` S103) is a correct acceptance of a genuine committed row under the documented failure grammar.
- Width: both a fully-real and a hash-junk new 203 row fail `D1_WIDTH` (pin moves against them or the third derivation splits).
- Harm: frozen positives byte-identical OK (`files=5 records=18 ok=18` combined receipt run), hatch-formatted genuine records OK.

Receipts in `receipts/` (one `.txt` per probe + `battery-r88.txt` + `atkA.tar.gz` with the width trees). Scratch removed after copy.
