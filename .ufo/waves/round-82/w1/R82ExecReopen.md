# R82ExecReopen — C2 kill rule K2: fire or hold

Seat: `R82ExecReopen` (round-82 wave 1, lane `chousa-shokunin`).
Bytes under attack: `b4a41d251b488f06b4a6ab01a11bc12ce72edd20` (candidate landing).
Frozen claims: `corpus/evidence/round82/claims.md` (read first, with its kill rules).
Scope: C2 kill rule K2 only — "a counted quote is absent from its committed capture text, or the capture's
sha256 differs from its refetch row (re-derived by a seat)". K1/K3/K4 and all of C1 are other seats' work and
are **not** scored here.

## Result

**K2 does not fire. All 13 quotes re-derived from committed bytes; all 11 counted quotes plus both S028
addendum quotes are verbatim in their committed captures AND still verbatim on the live page.**

The counted set is unambiguous. The entry's `## Located quotes` table holds 11 rows: Q1–Q5 on S008, Q6–Q9 on
S210, Q10 on S211, Q11 on S209. No other sourced quotation exists anywhere in the entry (a scan for
double-quoted spans returns only those 11 rows plus two prose mentions of the internal SKILL.md section name
"Question framing", which cite nothing external). The frozen counter agrees independently: `quotes=11/11`.

The S028 pair is the round-82 addendum of `corpus/knowledge/correction-retraction-status-r81.md`
(lines 66 and 68; the addendum heading opens at line 61). The r81 file carries 8 blockquotes in total; the
other six (S205 ×2, S206 ×3, S207 ×1) belong to the r81 body and were checked as a supplement only.

## Evidence, by check

### 1. Capture hashes equal their refetch rows (`k2-local-check.txt`, exit 0)

`refetch-rows-five.txt` shows exactly **one** row per id for S008/S209/S210/S211/S028 — attempt 1,
`curl_rc=0`, `http_code=200`, `fetched_utc` 2026-11-06T19:42:03Z…19:42:10Z. There is no failed later attempt
to step back past, so "the LAST successful row" is that single row.

| source | key (sha256(URL)[:24]) | `.raw` vs `raw_sha256` | `.txt` vs `txt_sha256` |
|---|---|---|---|
| S008 | `fd7eed5e0e6c64e22bc1470c` | OK | OK |
| S209 | `213237301753814b95b24684` | OK | OK |
| S210 | `bcb4a695b2aa019305121cff` | OK | OK |
| S211 | `97223722748a928c3c6912b5` | OK | OK |
| S028 | `dedff231d5c3d3cdb0b4f8e3` | OK | OK |

Every key recomputed from the landing-revision registry URL equals both the refetch `key` column and the
capture filename stem — the registry URL at landing is the URL that was fetched.

`K2_LOCAL quotes=13 pass=13 fail=0`.

### 2. Strict verbatim, no normalization ( `k2-strict-wc.txt`, exit 0)

Run with **no** whitespace collapse and **no** curly-quote folding — a raw substring test against the
committed `.txt`. All 11 pass `exact_substring_in_txt=True`. The normalization the kill rule permits was
therefore not load-bearing anywhere.

`wc -w` per counted quote, in table order:

| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 | Q11 |
|---|---|---|---|---|---|---|---|---|---|---|
| 18 | 21 | 20 | 15 | 23 | 17 | 23 | 21 | 11 | 21 | 20 |

All within the required 8–25. `STRICT wc_fail_or_absent=0 []`. S028 addendum quotes: 15 and 19 words, also
in range.

### 3. The `.txt` is derived from the `.raw`, not assembled by hand (`k2-live-check.txt`, exit 0)

Re-ran `tools/capture-fetch.py`'s own `html_to_text` + `recipe_txt` recipe over each committed `.raw` and
hashed the result: `txt_reproduced_from_raw=True` for all five sources. The committed text is a deterministic
function of the committed bytes.

### 4. Nothing was rewritten between prefreeze and landing (`commands.txt` §6)

- `git diff --stat 38f5af82… b4a41d25… -- corpus/captures/` → **empty**. No capture byte changed after the
  prefreeze commit.
- `git diff 38f5af82… b4a41d25… -- corpus/evidence/round57/refetch.tsv` → **empty**. The five rows were
  appended at 38f5af82 and never edited.
- `git diff 5d792e1e… b4a41d25… -- corpus/evidence/round57/refetch.tsv` → only the five-row **append**; no
  pre-existing row touched.
- Egress-table commit `5d792e1e…` is `2026-11-06T16:41:56-03:00` = 19:41:56Z, 7 s **before** the first
  round-82 refetch row (19:42:03Z). The table therefore preceded the fetches it authorises.

All five URLs in the landing registry match the intended targets in `egress-approval.md` (S008 Cochrane
chapter-02; S209 355862667/10.2.2; S210 355862687; S211 355862707; S028 crossref/services/crossmark). No
off-table URL was fetched.

### 5. Live re-open — one GET per URL (`live/fetch-log.tsv`)

`curl -fsSL --compressed --max-time 30 -A 'Mozilla/5.0 (X11; Linux x86_64)'`, one GET each:

| id | HTTP | curl rc | bytes | live sha256 | vs committed `.raw` |
|---|---|---|---|---|---|
| S008 | 200 | 0 | 150395 | `132c9f6f28bd1d5a…` | **IDENTICAL** |
| S209 | 200 | 0 | 1225386 | `aea56d51994e1c11…` | differs (dynamic) |
| S210 | 200 | 0 | 1221952 | `b9b40e62e75926f3…` | differs (dynamic) |
| S211 | 200 | 0 | 1270295 | `92366900050c84b7…` | differs (dynamic) |
| S028 | 200 | 0 | 38924 | `b459fa33346b334c…` | **IDENTICAL** |

S008 and S028 come back **byte-for-byte** as captured ~40 minutes earlier — independent confirmation that
those two captures are the genuine served documents. The three Atlassian pages differ byte-wise (per-request
tokens/session material in a 1.2 MB SPA payload); per the frozen kill rule this is **recorded as drift, not
fired**. On all five, **every quote still resolves live**:

`in_committed_capture=True in_live=True` for Q1–Q11, S028-q1, S028-q2 — `K2_LIVE fails=0`.

### 6. Independent verifier (`quote-reopen-verify.txt`, exit 0)

`python3 -B tools/quote-reopen.py verify --items quote-reopen-items.tsv` over the 13 quotes re-derived from the
committed blobs:

```
QUOTE_REOPEN  Q1 … Q11, S028-q1, S028-q2   → VERBATIM  matched in normalized page text   (13 lines)
QUOTE_REOPEN_SUMMARY verbatim=13 absent=0 too_long=0 no_source=0 unreachable=0
```

The lane's own tool — a separate implementation with its own extraction and its own fetch path — reaches the
same verdict on every item. rc 0.

### 7. Attribution is clean (`k2-cross-capture.txt`, exit 0)

Each of the 11 quotes is present in **its own** capture and in **none** of the other four. No quote is
attributed to the wrong page, and no JBI page's text has leaked into another's capture.
`MISATTRIBUTION absent_from_own_capture=0 []`.

### 8. Cross-check against the frozen counter (`depth-r82-at-landing.txt`, exit 0)

Running the frozen counting command on an `git archive` of the landing revision:

```
ENTRY question-framing-frames-r82.md ok=yes rows=9 quotes=11/11 fails=-
DEPTH_R82 entries=1 ok_entries=1 rows=9 located_quotes=11 fresh_sources=4
DEPTH_R82=PASS
```

The counter's own E3 test — every declared quote 8..25 words and LOCATED in the normalized text of its
`corpus/captures/<key>.txt`, over a FRESH source whose `txt_sha256` equals the file's hash — passes 11/11 with
4 fresh sources. This is not a substitute for the derivation above; it is a second, independent route to the
same conclusion.

## Residuals (recorded, not fired)

1. **Q1–Q3 are not literal substrings of the `.raw`.** In the Cochrane HTML the sentences are interrupted by
   inline `<strong>` markup (`The <strong>review PICO</strong> (planned at the protocol stage) is the PICO on
   which eligibility of studies is based…`). They are verbatim in the extracted `.txt`, which is what the kill
   rule names ("its committed capture text"). Observed on `in_raw=False` for Q1–Q3 only; not a defect.
2. **Three captures are not byte-reproducible live.** S209/S210/S211 are Atlas SPA pages; their wire bytes
   carry per-request material. Their **quotes** are stable live. Recorded as drift per the frozen rule.
3. **The refetch rows were written by the L1 itself.** There is no independent fetch witness in-repo for the
   `raw_sha256` columns. The live re-open is the only independent check available, and it confirms S008 and
   S028 byte-identically and confirms all 13 quotes on all five pages. This is a structural limitation of the
   lane's capture model, not a defect of this entry.
4. **K3 was not scored by this seat.** Whether each Do/Never follows from its warranting quote read in context
   is the non-author reviewer's check under the frozen rules. This seat tested presence and provenance only.
5. `c2-b1-salad-boundary` (declared in `claims.md`) means grounding and form can pass while a row still fails
   to follow from its quote. K2 passing says nothing about that boundary; it is declared, so it is not a
   finding.

## Tooling

No installs, no upgrades. `curl`, `git`, `python3` (stdlib only) were sufficient. No pacman or service
transaction was attempted. Nothing was written outside
`.ufo/waves/round-82/w1/R82ExecReopen/` and the scratch dir
`/fast/scratch/hyaku/chousa-r82/R82ExecReopen/` (removed at exit).

## Receipts (all in this folder)

`commands.txt` · `k2-local-check.txt` · `k2-live-check.txt` · `k2-strict-wc.txt` · `k2-cross-capture.txt` ·
`k2-r81-all-blockquotes.txt` · `quote-reopen-verify.txt` · `quote-reopen-items.tsv` · `refetch-rows-five.txt` ·
`depth-r82-at-landing.txt` · `live/fetch-log.tsv` · `k2_local_check.py` · `k2_live_check.py`

VERDICT: R82ExecReopen C1 n/a — seat did not touch the operability predicate.
VERDICT: R82ExecReopen C2 held — K2 not fired: 13/13 quotes verbatim in committed captures matching their refetch rows, 11/11 counted quotes strictly verbatim and 8-25 words, all 13 resolving on live re-open; three Atlas captures differ byte-wise live as expected for dynamic pages.
