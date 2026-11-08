# R87ExecForge — C1 forgery attack on the 203 classes (K2)

Seat: `R87ExecForge`, lane `chousa`, round 87, wave w1. Kill rule under test: **K2** —
"any in-class forged record is accepted, or is refused with a code outside its frozen expected set —
the two 203 classes (`D1-203-admit`, `D2-203-reject`) expect `REFETCH`". All work on committed
bytes only, no network. Tree: `git archive e6e920a4e6988287c31e89b3e920a118b569ae52` extracted to
`/fast/scratch/hyaku/chousa-r87/R87ExecForge` (removed after receipts were copied).
Subject tool: that tree's `tools/gate-records.py`; battery: its `corpus/evidence/round87/gate-records-r87.py`.

Baseline re-measured (receipt `battery-run.txt`):

```
python3 -B $S/corpus/evidence/round87/gate-records-r87.py --root $S --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --work $S/w-baseline
TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15
GATE_RECORDS_R87=PASS  (exit 0)
```

Command form for every forgery below (exact):

```sh
python3 -B $S/tools/gate-records.py verify --root $S --repo /home/vgpnk/Projects/shokunin/chousa-shokunin <file>
```

The D1/D2 records were **built by the battery's own builders** (`build_d1_203_admits` /
`build_d2_203_rejects`, receipt `built-records.txt`), never re-typed. Committed 203 rows
(`corpus/evidence/round57/refetch.tsv`): exactly 3 — S021 `2026-11-08T02:15:39Z` and S032
`2026-11-08T02:15:50Z` on `https://pubmed.ncbi.nlm.nih.gov/17638714/` (key `58725f5e…`), S022
`2026-11-08T02:16:21Z` on `https://pubmed.ncbi.nlm.nih.gov/28912002/` (key `ff9013bd…`); all
`curl_rc=0 http=203`, both captures hash to `7070b59c…` (the short "Cookies must be enabled"
page). Receipts: `.ufo/waves/round-87/w1/R87ExecForge-receipts/` — `forge-run.txt` (116 record
files, verdict line + exit each), `built-records.txt`, `battery-run.txt`, and the 116 record
files under `records/`.

## (a) The two 203 classes

Built records (verbatim):

```
D1-S021 GATE-RECORD S021 url=https://pubmed.ncbi.nlm.nih.gov/17638714/ fetched=2026-11-08T02:15:39Z tier=A decision=admit capture=corpus/captures/58725f5e0ac436166546a5ec.txt capture_sha256=7070b59c3434b677 words=10 quote="Enable cookies for pubmed.ncbi.nlm.nih.gov and reload this page to continue."
D2-S021 GATE-RECORD S021 url=https://pubmed.ncbi.nlm.nih.gov/17638714/ fetched=2026-11-08T02:15:39Z tier=A decision=reject capture=none curl_rc=0 http=203 words=0 quote=none
```

- D1 on all 3 rows: `…:1 S021 FAIL REFETCH`, exit 1 (same S032, S022). Expected `REFETCH`. **Match.**
- D2 on all 3 rows: `…:1 S021 FAIL REFETCH`, exit 1 (same S032, S022). Expected `REFETCH`. **Match.**
- **D1 quote = one long line of the 203 capture** (`F1a-longline.md`): quote is the whole capture
  normalized to one line (18 words, verbatim present, `words=18`): `FAIL REFETCH`, exit 1 —
  refused with exactly `REFETCH` (the quote grounds fine; only the 203 row fails it). **Match.**
  The 26-word variant (`F1a-26words.md`) adds `QUOTE_ABSENT,QUOTE_LEN` alongside `REFETCH` —
  refused, and `REFETCH` is in the set, so the battery's membership test counts it (same shape as
  R86ExecForge F2). Not a K2 breach: the expected code is present, merely not the only code.
- **D2 reject with `http=200`, `curl_rc` non-zero** (22/28/1/7, `F1b-rc{22,28,1,7}-http200.md`):
  `FAIL REFETCH`, exit 1, all four. `curl_rc=0 http=200` likewise. **Match** (no committed row
  matches the stated fetched/rc/http, and the 2xx-success rule agrees).
- **D2 reject on a 203 row whose `fetched` is a different attempt of the same row**: S021 citing
  S032's `2026-11-08T02:15:50Z`, and S022 citing its other row's `2026-11-08T02:16:17Z` (rc22 404
  row): both `FAIL REFETCH`, exit 1. The `fetched` match is per-(sid,url,fetched,rc,http), so a
  cross-attempt `fetched` has no row. **Match.**

## (b) Tier / tier-flip / capture_sha prefix / rev & path forms on the 203 rows

- Tier B (and C) on D1 and D2 (`B-tierB/C.md`, `B-d2-tierB.md`): `FAIL REFETCH,TIER`, exit 1.
  `REFETCH` present. **Match** (all three 203 sids are registry tier A, so any other tier flips).
- `capture_sha256` on D1: full 64, 16, 17, 32, and 16+`…`/16+`...` prefixes all give exactly
  `FAIL REFETCH` (sha correct; 203 row only). The 7-char prefix and the flipped first hex digit
  add `CAPTURE_SHA` (7 < 16-char minimum; flipped ≠ capture prefix). Raw-sha (`f8860990…`, the
  row's `raw_sha256` instead of `txt_sha256`) gives `FAIL CAPTURE_SHA,REFETCH`. **Match** throughout.
- `rev`/`path` forms on the 203 sids (`B-rev-S021/S032/S022.md`): a genuine committed `rev` record
  (S199, `rev=b7803829…`, `path=corpus/lessons/round-79-verifier-spotcheck.md:222`) re-labelled
  S021/S032/S022 → **`…:1 S021 OK`, exit 0** — accepted. This is **not a K2 forgery**: the `rev`
  form never consults `refetch.tsv`/the 203 row at all; it checks only that the sid exists in the
  registry and the quote is verbatim on the cited rev/path/line. Any registry sid can carry such a
  record. In-class for the *admit* class only if "citing a 203-sid" counted as citing the 203
  *fetch* — the rev form cites no fetch, so it is outside both 203 classes (same as round 86: a
  rev record is not an admit over the 203 row). Reported as a scope note, not fired. The
  capture-as-rev-path variant: `FAIL LINE,REV`, exit 1 (the capture is not a rev blob).

## (c) Escape hatches

- BOM / ZWSP / ZWNJ / NBSP prefix (`C-prefix-*.md`), on D1 and on D2: each `FAIL REFETCH`, exit 1.
  `lead_strip` drops leading whitespace and Cf characters for both detection (`REC_RE`) and parsing
  (`parse`), so the record is seen and judged like the un-prefixed one — it cannot hide. **Match.**
- Indented (1/2/3 spaces) and tab-prefixed: same `FAIL REFETCH`. **Match.**
- Inside a fenced code block (`C-fenced.md`): judged at its own line, `FAIL REFETCH`. **Match.**
- Duplicate `GATE-RECORD` lines for one S-id (`C-dup2.md` two identical D1; `C-dup.md` a `PARSE`
  line + D1): both files `FAIL` with per-record verdicts, exit 1; no deduplication bypass — every
  `^GATE-RECORD` line is judged. **Match.**
- Mid-line (`x GATE-RECORD …`, `note: GATE-RECORD …`, lowercase `gate-record`, fullwidth Ｇ):
  `records=0`, exit 1 (never seen — invisible, hence never accepted-as-record; the file-level
  `records==0` still fails the tool). Reported for completeness: such text is skipped, not accepted.

## (d) The `url/unreach` grammar

On the S021 D2 base and on the genuine S208 row (`curl_rc=22 http=403`, verified `OK` as control):

| case | S021-base verdict | S208-base verdict |
|---|---|---|
| `curl_rc=0 http=203` (the D2 itself) | `FAIL REFETCH` | `FAIL REFETCH` |
| `curl_rc=0 http=299` / `204` | `FAIL REFETCH` | `FAIL REFETCH` |
| `curl_rc=0 http=300` / `301` / `199` / `200` | `FAIL REFETCH` | `FAIL REFETCH` |
| `curl_rc=1 http=203` / `299` / `200` | `FAIL REFETCH` | `FAIL REFETCH` |
| `curl_rc=22 http=200` | `FAIL REFETCH` | `FAIL REFETCH` |
| `curl_rc=007 http=203` | `FAIL PARSE` | — |
| `http=20A` / `4040` / `20`, `curl_rc=A`, empty `curl_rc` | `FAIL PARSE` | — |

All exit 1. Expected for D2-class shapes is `REFETCH`; every syntactically valid 2xx/3xx/4xx
claim here is refused `REFETCH` (no committed row matches), and malformed numbers are `PARSE`.
**Match** on all 20 probed combinations. Cross-URL: D2-S021 with S022's cochrane URL → `FAIL
REFETCH`; D1-S022 with the cochrane URL → `FAIL CAPTURE_KEY,REFETCH` (key follows the URL).
Also probed, all refused as expected: double-space/tab separators, dup key, `words=00`,
`capture=NONE`, unfenced trailing junk, `+00:00` fetched, `S21` (PARSE), `S0021`/`S999`
(`REGISTRY,REFETCH`), `./`/`//`/trailing-slash capture paths, uppercase sha, padded quote,
quote with embedded newline. The genuine S216 lesson record verifies `OK` (exit 0) as control.

## The one acceptance found — below the frozen K2 text, against the claim's premise

**13 committed rows have `curl_rc=28 http=200`** (S103, S105 ×3 attempts, S106, S134 ×2, S135 ×3,
S136 ×3) with `txt_sha256="-"`. A `url/unreach` record citing any of them verbatim is
**ACCEPTED** (`…:1 S103 OK`, exit 0 — all 13 rows; receipts `f4/E-nonzero200-*.md`):

```
GATE-RECORD S103 url=https://library.um.edu.mo/upload/databases/c1b0fa89e2809581b12c79b9c60ea1af.pdf fetched=2026-10-27T08:05:52Z tier=B decision=reject capture=none curl_rc=28 http=200 words=0 quote=none
```

Why I do **not** fire K2 on this. (1) K2's frozen expected set covers exactly "the two 203
classes"; these rows are HTTP 200, not 203, and the records are the honest transcription of a
committed failed fetch (curl timeout 28 — the transfer did fail even though 200 headers arrived),
so they are the *genuine* `url/unreach` shape, not a forged one; the battery itself builds a fresh
unreach positive with the same semantics (S100 `curl_rc=28 http=000`). (2) It is **not a repair
regression**: the pre-round-87 tool accepts the same 13 records identically (`success = rc=="0"
and http=="200"` was already false for `rc=28`, and the row matches) — verified by running
`git show c033577b^:tools/gate-records.py`. (3) The landed code's own comment and the plan's
repair note define the rule as "`curl_rc==0` **and** 2xx" is success, i.e. a non-zero curl exit
denotes failure regardless of status; the only claim wording that would fire is the seat brief's
parenthetical shorthand "any 2xx is a successful response, never a failed transfer", which is
stronger than both the frozen claim and the coded rule. Records: `f4/E-nonzero200-*.md`, both-tool
runs in the same directory's run output. **L1 adjudication item, not a held/fired verdict on its own.**

What the battery executed myself vs. left to checkers: everything above is measured, not inferred.

## Verdict on the forgeries attempted

116 record files; every one refused with the expected membership (`REFETCH` present for all
203-class shapes; `PARSE`/`TIER`/`CAPTURE_SHA`/`CAPTURE_KEY`/`WORDS`/`REGISTRY` where the shape is
malformed) except the two scope items: (i) the 13 `curl_rc=28 http=200` honest unreach records,
accepted by pre- and post-repair tools alike, outside the frozen D1/D2 class text; (ii) the
`rev`-form records re-labelled to 203 sids, accepted, but citing no fetch at all. Neither is an
in-class forged record accepted under the frozen wording.

Tooling: no installs; `python3` (stdlib only), `git`, `sha256sum` were used. No network access.

Report: .ufo/waves/round-87/w1/R87ExecForge.md
VERDICT: R87ExecForge C1 held — all 203-class forgeries refused with REFETCH (or PARSE for malformed forms); the only acceptances (rc=28/http=200 honest unreach rows, rev-form on 203 sids) are outside the frozen D1/D2 class text and pre-date the repair.
