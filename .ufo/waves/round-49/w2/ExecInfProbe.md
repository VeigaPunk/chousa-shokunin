# ExecInfProbe — round 49 w2 report

Seat: ExecInfProbe (executor, leaf). Item attacked: the INFERENCE_GROUNDED leg on the two adopted entries
— `corpus/knowledge/aggregator-vs-source-r36.md` (E1) and `corpus/knowledge/citation-count-semantics-r37.md`
(E2) under `tools/inference-ground.py` with `corpus/evidence/round49/spans.tsv`. No predicate, target or
counter proposed for change.

Code pinned: `git -C <lane> rev-parse master` → `87e9335…`; `sha256sum tools/inference-ground.py` →
`fa2b4eb5fc29b4dd30f468d9409790ba55fa4b012851e5c9f3efce0074658b6e`, identical to
`git show 4ce61fc…:tools/inference-ground.py | sha256sum` (`git diff --stat 4ce61fc… -- tools/inference-ground.py`
printed nothing), so every probe ran the code measure-after.txt measured.

## Baseline (unmutated entries — the frozen predicate)

```
$ python3 tools/inference-ground.py --entry corpus/knowledge/aggregator-vs-source-r36.md --spans corpus/evidence/round49/spans.tsv --counts /dev/null --registry corpus/SOURCES.md --root .
GROUND entry=corpus/knowledge/aggregator-vs-source-r36.md section=1 bullets=4 tokens=4 grounded=4
GROUND: PASS
exit=0
$ python3 tools/inference-ground.py --entry corpus/knowledge/citation-count-semantics-r37.md --spans … (same flags)
GROUND entry=corpus/knowledge/citation-count-semantics-r37.md section=1 bullets=4 tokens=4 grounded=4
GROUND: PASS
exit=0
```

`bullets=4 tokens=4` is the whole result: **each bullet clears the gate on exactly one token** (inventory
below). The frozen predicate (claims.md:66 "both entries exit 0 under `tools/inference-ground.py`") is true.

## One-edit mutants (`/dev/shm/chousa-r49-ExecInfProbe/`, `diff` = 1 line each; originals `cmp`-identical)

Run shape for every mutant (`$D` scratch, `$L` lane):
`python3 $L/tools/inference-ground.py --entry $D/<mutant> --spans $L/corpus/evidence/round49/spans.tsv --counts /dev/null --registry $L/corpus/SOURCES.md --root $L`

| # | one edit (in `#### Inference`) | observed | verdict |
|---|---|---|---|
| E1-M1 | B4 `names investigating` → `names not investigating` (Latin stem) | `INF_POLARITY_FLIP bullet=4 token='…investing attention in the site at hand / investigating'` FAIL exit=1 | refused |
| E1-M2 | B1 quote `実際の論文` → `実際の論分` (one char) | `INF_TOKEN_NOT_IN_SPAN bullet=1 token='CiNii Researchの「参考文献」は、実際の論分の…'` FAIL | refused |
| E1-M3 | B1 `: S096 says` → `: says` (drop the only S-id) | `INF_UNCITED bullet=1` + `INF_TOKEN_NOT_IN_SPAN bullet=1` FAIL | refused |
| E1-M4 | B4 Latin quote → CJK-only `実際の論文の参考文献と必ずしも一致していません` | `tokens=3` `INF_UNGROUNDED bullet=4` FAIL | refused, bluntly (§1) |
| E1-M5 | B2 add unquoted `(959 records)` (absent from spans) | `INF_TOKEN_NOT_IN_SPAN bullet=2 token='959'` FAIL | refused |
| E1-M6 | B4 add unquoted `271 sources` (271 **is** in span S099-2) | `tokens=5 grounded=5` **PASS** exit=0 | passes |
| E1-M7 | B2 `and S096's count` → `and its count` (drop 1 of 2 cited ids) | `bullets=4 tokens=4 grounded=4` **PASS** exit=0 | passes |
| E1-M8 | B4 add quote `Students practiced the heuristic`, present only in S099-1's **context window** | `tokens=5 grounded=5` **PASS** | passes (rule-consistent) |
| E2-M7 | B1 CJK quote `任一合作者` → `任一合作老` (one char) | `tokens=4 grounded=4` **PASS** exit=0 | passes |
| E2-M8 | B1 Latin quote → CJK-only quote | `tokens=3` `INF_UNGROUNDED bullet=1` FAIL | refused, bluntly |
| E2-M9 | B2 `S100 says` → `S100 does not say` before a CJK quote | `tokens=4 grounded=4` **PASS** exit=0 | passes |
| E2-M10 | B1 `while CiNii says` → `while not CiNii says` (Latin stem) | `INF_POLARITY_FLIP bullet=1 token='CiNii … / cinii'` FAIL | refused |

5 of 12 one-edit mutants pass. Three of those (E2-M7, E2-M9, E1-M7) contradict what the leg reads as
certifying; two (E1-M6, E1-M8) are consistent with the frozen rule's wording and are limits, not defects.

## 1 — CJK-only quotes are not tokens, and their polarity is unreachable (QUALITY 66 named limit)

Measured with the tool's own functions (imported by path):

```
aggregator-vs-source-r36: bullets=4 tokens=4 backticked>=4ch=6 invisible_cjk=2 backticked<=3ch=0
citation-count-semantics-r37: bullets=4 tokens=4 backticked>=4ch=8 invisible_cjk=4 backticked<=3ch=1
TOTAL: bullets=8 tokens=8 backticked>=4ch=14 invisible_cjk=6 (43%) short_ignored=1
```

`has_two_words()` (tools/inference-ground.py:87-89) needs two whitespace-separated words containing
`[A-Za-z]`; every pure-CJK phrase yields `words()==[]` and is skipped. Unchecked in the Inference sections:
`同定・統合された分をカウントしています` (E1 B1), `4.引用文献の原文情報を書誌情報に解析して検索` (E1 B3),
`关于自引的说明：…认定为自引。` (E2 B1), `被引频次为0的文献将不会显示` (E2 B2), `来源数据库` and
`为便于文献的统计和期刊评价` (E2 B3/B4) — plus `引用量`, 3 chars, below `BACKTICK_RE`'s `{4,}` floor (line 73).
7 of the 15 quoted phrases a reader sees sit outside the gate; the six ≥4-char ones are 43% of the 14
tokenizable candidates.

Polarity is unreachable for the same strings: `polarity_flips()` (line 317) takes its scope stems from
`words(tok)` and returns `[]` when `stems` is empty (lines 331-333):

```
words('关于自引的说明：对于合作发文的参考文献中') = []
phrase_polarity('同定・統合された分をカウントしています', [S096-2]) = (False, [])
polarity_flips('- result: S100 does not say `被引频次为0的文献将不会显示`.', '被引频次为0的文献将不会显示', [S100-3]) = []
```

Consequences, measured on the adopted entries themselves:
- E2-M7: a fabricated CJK quote (one character changed) in E2 B1 passes — B1's single token is the
  Latin-bearing CiNii quote.
- E2-M9: a bullet saying `S100 does not say `被引频次为0的文献将不会显示`` passes — a direct inversion of a cited
  source's statement, invisible to both the token rule and P1/P2.
- E1-M4 / E2-M8 are refused only as `INF_UNGROUNDED`: the CJK substitution removed the bullet's **only**
  token. The refusal is a token-count artefact, not a grounding check; E2-M7 shows that a CJK substitution
  leaving another token standing is not refused at all.

## 2 — id accounting is per bullet, not per claim

`INF_UNCITED` fires only when a bullet cites no id at all (tools/inference-ground.py:479-480). E1 B2 cites
S096 and S097; deleting the S096 reference leaves the bullet citing S097, whose J-STAGE quote is its one
token, so it passes while a claim has lost its source. The counter's `REF_ID_UNBOUND=0` cannot see this:
it checks ids present, not claims covered.

## 3 — grounding surface is the span context window; numerals ground by occurrence

Every span file is a window, not the quote: `span_file == quote cell` for 0/28 rows, `quote in span_file`
for 28/28 (span files 48–290 chars vs quotes 3–130 chars). This is by design — claims.md:65 requires each
span file "longer than its quote" — but a token is then grounded by text the entry never quoted (E1-M8:
`Students practiced the heuristic` from S099-1's leading context, PASS). A numeral is grounded by any
digit-boundary occurrence in a cited span (E1-M6: `271` from S099-2's `(n = 271)` attached to an invented
"271 sources were checked"); W1 `CritForgeC2.md:109` already named the numeral bypass, E1-M5 (`959`) is
the control that refuses.

## Calibration — what holds

- One character changed inside a **Latin-bearing** quote is refused (E1-M2); so is a fabricated 3-digit numeral absent from the cited spans (E1-M5), and `not` inserted before an affirmed Latin stem (E1-M1, E2-M10 — the Latin half is genuinely guarded, even where one quote is reused across two bullets).
- Dropping the only cited id is refused (E1-M3) with the token cascade; the frozen C2 result (`INFERENCE_GROUNDED=2/2`, measure-after.txt) reproduces and is honest at its own wording — it certifies 8 bullets / 8 tokens / 8 grounded: one token per bullet, 57% of the Inference sections' quoted phrases, and no claim-to-source coverage.

## Risks / blockers

- No production file, report, index, jj state or external state written; no install needed; no network.
  Scratch `/dev/shm/chousa-r49-ExecInfProbe/` deleted after the runs.
- Residual risk for the parent: this leg's PASS is not evidence that a bullet's CJK quotations are verbatim
  or that its attributions survive. Closing it needs a token rule that does not require Latin letters and a
  per-claim id check — both outside this seat's write scope.

VERDICT: INFERENCE_GROUNDED leg on the two adopted entries — partly — the frozen predicate reproduces and the Latin-bearing half is guarded (5 mutants refused), but 43% of Inference quotes are CJK-only and invisible to both the token rule and the polarity engine (E2-M7 char change and E2-M9 "does not say" inversion pass), and per-bullet id accounting lets a claim lose its citation (E1-M7 passes).
