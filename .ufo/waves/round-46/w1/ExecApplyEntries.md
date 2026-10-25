# ExecApplyEntries — inference-grounding rule on the four admitted entries (measurement, not a gate)

Item: run `python3 tools/inference-ground.py --entry <entry> --spans
corpus/evidence/round46/spans.tsv --counts /dev/null` on the lane's four admitted entries; paste every
finding; then say per entry which bullets fail only because (a) no backticked/quoted token exists,
(b) no numeral is grounded, (c) the manifest has no span for the cited id. Entries not edited.

Provenance (sha256 at run time = post-run state; nothing was edited):
tools/inference-ground.py `81e163b3a637c393b690d109cf79d1d6132245f724d90b1fcb890949936da14c` ·
round46/spans.tsv `224f706214e6037c88340c26de4878c080933d75a0f320fce4ff345556edd51a` (11 rows,
ids **S085–S089 only**; file appeared mid-run, `ExecSpanBuilder` owns it, no S079–S084 row) ·
r41 `c8c7b065c142317595cfdd30de0610705841b58e6433e6f19998fdd9ce920565` ·
r40 `4312d14c259f613d101e788714fc85f1afedb0698483474739819503c770f8df` ·
r36 `8a879d0ad24e51a7f2671ace2228d2ae9eedc4496a97677d622f390da6033f46` ·
r37 `af8d980675b55fa6e4eb55bdc74e452d5e7ecc4f378952be31656893d84b0b89`.

## 1. The commanded run (verbatim)

```
$ cd chousa-shokunin && for e in evidence-archive-field-policy-r41 evidence-snapshot-coverage-r40 \
    citation-version-binding-r36 citation-version-binding-r37; do python3 tools/inference-ground.py \
    --entry corpus/knowledge/$e.md --spans corpus/evidence/round46/spans.tsv --counts /dev/null; echo EXIT=$?; done
```
```
########## evidence-archive-field-policy-r41 ##########
GROUND entry=corpus/knowledge/evidence-archive-field-policy-r41.md section=1 bullets=4 tokens=1 grounded=0
FINDING INF_UNCITED bullet=1 token=''
FINDING INF_UNGROUNDED bullet=1 token=''
FINDING INF_UNCITED bullet=2 token=''
FINDING INF_UNGROUNDED bullet=2 token=''
FINDING INF_UNCITED bullet=3 token=''
FINDING INF_UNGROUNDED bullet=3 token=''
FINDING INF_UNCITED bullet=4 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=4 token='404'
GROUND: FAIL
EXIT=1
########## evidence-snapshot-coverage-r40 ##########
GROUND entry=corpus/knowledge/evidence-snapshot-coverage-r40.md section=1 bullets=4 tokens=11 grounded=0
FINDING INF_UNCITED bullet=1 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='6,510'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='6,511'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='99.98%'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='1,145'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='2,531'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='45.2%'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='1,386'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=2 token='7,572'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=2 token='5,959'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=2 token='78.7%'
FINDING INF_UNCITED bullet=3 token=''
FINDING INF_UNGROUNDED bullet=3 token=''
FINDING INF_UNCITED bullet=4 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=4 token='404'
GROUND: FAIL
EXIT=1
########## citation-version-binding-r36 ##########
GROUND entry=corpus/knowledge/citation-version-binding-r36.md section=1 bullets=2 tokens=0 grounded=0
FINDING INF_UNCITED bullet=1 token=''
FINDING INF_UNGROUNDED bullet=1 token=''
FINDING INF_UNCITED bullet=2 token=''
FINDING INF_UNGROUNDED bullet=2 token=''
GROUND: FAIL
EXIT=1
########## citation-version-binding-r37 ##########
GROUND entry=corpus/knowledge/citation-version-binding-r37.md section=1 bullets=2 tokens=0 grounded=0
FINDING INF_UNCITED bullet=1 token=''
FINDING INF_UNGROUNDED bullet=1 token=''
FINDING INF_UNGROUNDED bullet=2 token=''
GROUND: FAIL
EXIT=1
```
**12 bullets, 12 tokens, 0 grounded, 12/12 bullets fail; 30 findings = 10 INF_UNCITED + 8
INF_UNGROUNDED + 12 INF_TOKEN_NOT_IN_SPAN** (counted: `grep -c` over the run).

## 2. Sensitivity control — manifest+counts that do cover their ids

`--spans corpus/evidence/round45/spans.tsv --counts corpus/evidence/round45/counts.json` (S082/S083
spans, S084-derived integers). r41, r36, r37 reproduce §1 byte-identically (grounded=0), so their
failures do not depend on manifest coverage. r40 changes to `tokens=11 grounded=7`; residual findings:
`INF_TOKEN_NOT_IN_SPAN bullet=1 token='99.98%'`, `bullet=1 token='45.2%'`,
`bullet=2 token='78.7%'`, `bullet=4 token='404'`, plus the INF_UNCITED/INF_UNGROUNDED of bullets 1,3,4.

## 3. Counterfactual — add only the missing citation (scratch copies, entries untouched)

r41 bullet 4 += `(S083)`; r40 bullet 1 += `(S084)`; same manifest+counts as §2:
```
### r41: GROUND entry=r41-cf.md bullets=4 tokens=1 grounded=1  -> bullet 4 passes, `404` grounds
### r40: GROUND entry=r40-cf.md bullets=4 tokens=11 grounded=7 -> 99.98% / 45.2% / 78.7% / 404 remain
```
`404` is verbatim in `corpus/evidence/round45/spans/S083-2.txt` ("Archive.org returns a 404 page for
these"), so r41:4's token failure is a citation artifact, not an ungroundable numeral.

## 4. Per entry, per bullet — which class the bullet fails on

| entry | bullet (:line) | tok | fails on |
|---|---|---|---|
| r41 | 1 (:19) | 0 | **(a)**; also uncited |
| r41 | 2 (:20) | 0 | **(a)** — `cached_original_claim_url` is one whitespace-free word, filtered by `has_two_words`; also uncited |
| r41 | 3 (:21) | 0 | **(a)**; also uncited |
| r41 | 4 (:22) | 1 | **no citation** (reported INF_UNCITED; its `404` is merely unlooked-up, §3). Not (c) — cites no id |
| r40 | 1 (:20) | 7 | **no citation**; integers ground once cited (§3), residual **(b)** = `99.98%`, `45.2%` |
| r40 | 2 (:21) | 3 | **(c)** S084 has no r46 span row, **and (b)**: with counts 7,572/5,959 ground, `78.7%` never does → (c) is real but not sufficient |
| r40 | 3 (:22) | 0 | **(a)**; also uncited |
| r40 | 4 (:23) | 1 | **no citation** (INF_UNCITED; `404` groundable via S083); not (c) |
| r36 | 1 (:16) | 0 | **(a)**; also uncited |
| r36 | 2 (:17) | 0 | **(a)**; also uncited |
| r37 | 1 (:17) | 0 | **(a)**; also uncited |
| r37 | 2 (:18) | 0 | **(a)** alone suffices — cites S079, which also has no span (**c**), but 0 tokens means adding the span still yields INF_UNGROUNDED |

**Answer: no bullet fails *only* because (c).** (c) holds for the only two cited bullets (r40:2 →
S084, r37:2 → S079): in r37:2 it is masked by (a), in r40:2 outlived by (b). The binding constraint
is citation placement — 10 of 12 bullets cite no id, and both numeral failures the tool reports
(`404` twice) disappear when the bullet cites the span containing the numeral.

## 5. Findings

- **F1 — citations live in Observation, not Inference.** 10/12 inference bullets carry no source id;
  they close "Lane inference" / "Lane arithmetic". The D7 gap is stylistic, not span coverage.
- **F2 — the numeral rule conflates a document/status name with a measurement** (`RFC 7089` → `7089`;
  `404 page` → `404`). Such a token grounds only if the cited id's span happens to carry the name, so
  the finding tracks citation luck.
- **F3 — numerals under three digits are never tokens** (`NUM_RE` needs `\d[\d,]{2,}`): `8 stored
  evidence values` (r41:22) and `1,386 against 1` (r40:20) are unchecked claims.
- **F4 — single-word backticks never ground** (`has_two_words`): `cached_original_claim_url`,
  `sha256`, `corpus/knowledge/evidence-snapshot-coverage-r40.md` are filtered; field names and
  cross-reference paths cannot serve as grounding tokens.
- **F5 — derived rates are structurally ungroundable**: `78.7%`, `99.98%`, `45.2%`; `count_values`
  ingests only integers and no span carries a rate. Three findings remain after every citation (§3).
- **F6 — `--counts /dev/null` is inert by construction** (`Path.is_file()` false for a character
  device): the commanded run grounds a numeral only via span text; r40 moves 0→7 grounded on a real
  counts file. Read §1's `grounded=0` as "no span and no counts", not "counts disagree".
- **F7 — round-46 entries fit the rule far better, and both fail on the same artifact.** Same command,
  same `/dev/null`, on the two new entries (other seats' in-flight files, unmodified):
  `evidence-pool-versioning-r39.md` (`a59457ca…f7da3`) → `bullets=4 tokens=7 grounded=6`, finding
  `INF_TOKEN_NOT_IN_SPAN bullet=4 token='7089'`; `…-amendment-2026-10-23.md` (`c44d2735…34a6d`,
  absent when §1 ran, measured at 07:27) → `bullets=4 tokens=5 grounded=4`, finding
  `INF_TOKEN_NOT_IN_SPAN bullet=3 token='7089'`. Both residual findings are F2 on the RFC-7089
  sentence (= row S079, one of the held rows with no round-46 span → (c) also). A C1-style gate applied
  to this round's own corpus would refuse both entries over a document name.

## 6. Verdict

Measured, not gated: **0/12 inference bullets ground** (r41 0/4, r40 0/4, r36 0/2, r37 0/2). Supplying
S079–S084 spans would leave all 12 failing — 8 on (a) alone, 3 more (r41:4, r40:1, r40:4) on missing
citation alone, r40:2 on `78.7%`. Supplying the missing citations instead (§3) clears exactly one
bullet (r41:4) and leaves r40:1 with `99.98%` / `45.2%`: every residual finding is a derived rate.
No entry edited; no production file, lane git index or jj state touched; no fetch; scratch
`/tmp/chousa-r46-ExecApplyEntries/` deleted. Installs: none, so RULES.md was not required.
