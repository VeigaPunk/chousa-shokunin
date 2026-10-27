# R57W2ReviewC3After — final re-derivation of R57-C3 at HEAD

Scope: lane HEAD `3010e7537d163d9a76264a166d491214ecdaf45e` (spec tip `1c9626e`; the landed
W2-dispatch commit adds no corpus bytes). Nothing attacked outside R57-C3. All runs had
`TMPDIR`/`PYTHONDONTWRITEBYTECODE=1` set under `/fast/scratch/hyaku/chousa-r57/R57W2ReviewC3After`.

## 1. build-spans --check (manifest regeneration)

```
$ python3 tools/build-spans.py --check --quotes corpus/evidence/round57/c3/quotes.tsv \
    --out corpus/evidence/round57/c3 --cache corpus/captures
SPANS_ROWS=10 STALE=0          (rc=0)
```
`git status --porcelain -- corpus/evidence/round57/c3 corpus/captures` → 0 lines: builder rewrote nothing,
manifest and captures are the committed bytes.

## 2. Counter + substance check at HEAD

```
$ python3 corpus/evidence/round51/quote-substance-check.py corpus/evidence/round57/c3/spans.tsv
IDS=5 QUOTES=10 FAILURES=0      (rc=0)
$ python3 corpus/evidence/round57/c3-count.py
ENTRY=yes S127_CITED=yes NEW_GROUND=yes CLAUSE=yes
BOUND=4/7 (min 4) R1:S131 R2:S132 R3:S133 R7:S118
SWEPT=3/3 R4 R5 R6
QUOTE_ROWS=10 IN_SPAN=10 IN_ENTRY=10 IN_LESSON=10 SHORT=10 CONTEXT=10 CAPTURE_BOUND=10
SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=yes STRAY_IDS=-
C3=PASS                        (rc=0)
```

## 3. Frozen inputs

The spec's C3 freeze SHA `fd95724d56a33a150cd2638fadd2ce1f3425e6c` is a **bad revision** — a
transcription error (`…a33a150c…` vs real `…a33ad150c…`; the landed lesson addendum already logs this
as `R57W2SentFinal.md` F1, "wrong id appears in no committed claims/counter/controls"). Against the
real freeze commit `fd95724d56a33ad150cd263f8add2ce1f3425e6c`:

```
$ git diff fd95724d56a33ad150cd263f8add2ce1f3425e6c HEAD -- corpus/evidence/round57/c3-count.py
(empty, rc=0)
$ git diff fd95724d56a33ad150cd263f8add2ce1f3425e6c HEAD -- corpus/evidence/round57/claims.md
(empty, rc=0)
```
`git log` confirms `fd95724` is the last commit touching `claims.md` — the frozen C3 section is
unamended. BASE `6656f07` registry contains S130 but no S131–S133 (newness precondition real).

## 4. Independent per-bound-row re-derivation (own code, not the counter)

Scratch `verify.py` re-implemented: key = sha256(url)[:24]; defined form = `.txt` (none of the five
raws is OLE/PK — `6f545e…` starts `%PDF-1.7`, the HTML raws `<!DOCTYPE html>`); heading rule verbatim
from the freeze; last-successful-refetch per (id,url) with later rows overwriting.

**A. capture bytes == last successful refetch** (all True, attempt/utc shown):

| id | key | raw==last-good | txt==last-good |
|----|-----|----------------|----------------|
| S131 | 788d2e2f0191d7326b6ca03b | T (att 1, 09:04:41Z) | T |
| S132 | a476f4128186c7976671ab54 | T (att 1, 08:43:48Z) | T |
| S133 | 6f545e6c16b6b568ea3f591b | T (att 2, 08:35:01Z; att 1 rc=28/000 precedes, no later success) | T |
| S118 | 16fe8487aa97b98576a0dbac | T (att 2, 08:31:19Z) | T |
| S127 | b27ffd2f0161104c6a28c9f5 | T (att 2, 08:31:42Z) | T |

No (id, bound-url) pair has a later successful attempt: `grep` of `refetch.tsv` shows S133's only
success at 08:35:01Z, S132 at 08:43:48Z, S131 at 09:04:41Z.

**B. recipe honesty (a leg C3 does *not* check — I added it):** `recipe_txt(.raw)` (the frozen
campaign recipe: `pdftotext -layout` for `%PDF-`, else `html_to_text`) byte-equals the committed
`.txt` for all five captures — derived sha equals the refetch `txt_sha256` (`650f1cdc…`,
`8976b167…`, `ceef80d9…`, `927ff71c…`, `23306b9f…`). So the defined forms are honestly derived, not
just digest-witnessed. S132's token `〔2021〕16号` is span-split in raw HTML
(`国卫办药政发〔<span>2021</span>〕<span>16</span>号`, raw:257) but contiguous in the derived `.txt`
line 316 `国卫办药政发〔 2021 〕 16 号` — the binding is real.

**C. heading + edition token (whitespace-removed, committed `.txt`):**

```
R1 S131: heading line 106 '国家卫生健康委关于开展药品使用监测和临床综合评价工作的通知' (prefix '') ; '〔2019〕80号' present
R2 S132: heading line 301 '国家卫生健康委办公厅关于规范开展药品临床综合评价工作的通知' (prefix '') ; '〔2021〕16号' present
R3 S133: heading line 2 '药品临床综合评价管理指南' (cover, after trailing （…） drop)          ; '2021年版' present
R7 S118: heading line 0 '药品临床综合评价质量控制指南'                                          ; '2024年版' present
```

**D. all 10 manifest rows:** quote ∈ span, span == `form[offset:offset+len(span)]` exactly,
manifest digest == committed `.txt` sha256, span > quote, ≤25 words / ≤160 chars — 10/10.

**E. anchors:** registry col-6 `char N` cells of the new rows are quote offsets recomputed as
`offset + span.find(quote)`: S131 {271,352}, S132 {68,1036}, S133 {19,54} — all match
(`ANCHOR_BOUND=3/3` independently confirmed). `how=mined`, `opened=2026-10-27`, `used-by` names the
entry; exactly one row per id; cites `source: <id> — <first-url>` present.

**F. entry/lesson:** `- UNBOUND R4/R5/R6 sweep:` lines present; all 10 quotes occur in the
**committed** `HEAD:corpus/lessons/round-57.md` (the worktree's ` M` lesson is an additive
integration block — C3 legs unaffected); uppercase S### in entry = {S118,S127,S131,S132,S133} only,
no lowercase `s###` or fullwidth ids (w1 `R57W1CritC3Stray` case-(3) hole not exercised here).

## Findings

- **F1 (documentation, already landed):** the spec/SCORECARD C3 freeze SHA was a 40-hex string that
  names no commit; the true freeze `fd95724d56a33ad150cd263f8add2ce1f3425e6c` is byte-identical at
  HEAD for both `c3-count.py` and `claims.md`. Recorded, not a predicate defect.
- Residual (w1-carried, per freeze rule): lowercase `s###` ids evade STRAY_IDS; unexercised by this
  entry. Predicate does not require `.txt==recipe(.raw)` for new captures — closed empirically above.

## Hygiene

No installs, no network, no lane writes other than this file; scratch held only `verify.py` +
`lesson_head.txt`, removed before yield.

VERDICT: attacked R57-C3's landed state — builder freshness, all five bound-row byte/digest/recipe
provenance, heading+token rules, span slices, anchors, UNBOUND/stray legs, frozen-input integrity —
at HEAD `3010e75` every leg re-derives independently and the counter prints `C3=PASS`: SURVIVES.
