# R50MutInferenceCJK — mutation-test of the post-freeze `has_two_words` / `CJK_RE` change

Seat: R50MutInferenceCJK, chousa round 50 wave 2 (falsify). Target: `tools/inference-ground.py`
(lane commit 74794db), the round-50 CJK floor: `has_two_words` falls back to
`len(CJK_RE.findall(s)) >= 4`, `CJK_RE = [\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]`
(tools/inference-ground.py:66, :80). Five mutants, three detectors, three landed entries.
No tooling installed (none needed); pacman untouched. Lane file never modified.

## Setup and restoration evidence

- Scratch `/dev/shm/chousa-r50-R50MutInferenceCJK/` (deleted at end; `rm -rf` verified below).
- `cp tools/inference-ground.py → pristine.py`; both hashed
  `33d4a37f3f7a5ce87862d0a354b3058ed5c579c5491b9e5d3ec6610a8e962b6d` at copy time.
- Mutants (`sha256`): m1 floor `>=1` `24d2ffd3…fdf92`; m2 floor `>=10` `d431b5f9…e53ea`;
  m3 `CJK_RE = [\u4e00-\u9fff]` `96d4ed87…5fdd0`; m4 adds `if words: return False` before the
  CJK branch `8b4249b9…5bc58c`; m5 `WORDS_RE = r"[a-z][a-z'\u2019]*|[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]"`
  (each CJK char a word → polarity windows see CJK) `5de5fd46…7c4ed`.
- Re-hash of lane `tools/inference-ground.py` after all runs: `33d4a37f…e962b6d` — byte-identical, restored/untouched.

## Baselines (pristine) — all green, so mutant runs are conclusive

```
cjk-ground-check --tool pristine.py → CASE A rc=0 PASS; CASE B rc=1 INF_TOKEN_NOT_IN_SPAN PASS;
  CASE C rc=1 INF_UNCITED PASS; CJK_GROUND=PASS ; PRISTINE_CJK_RC=0
precision-count --tool pristine.py → CORRECT_BULLETS_PASS=12/12 ; PRECISION_GATE=PASS ; rc=0
pristine on landed entries →
  cnki-citation-check-r40: section=1 bullets=5 tokens=10 grounded=10 GROUND: PASS rc=0
  citation-matching-semantics-r41: bullets=4 tokens=7 grounded=7 GROUND: PASS rc=0
  istic-citation-verification-r39: bullets=4 tokens=13 grounded=13 GROUND: PASS rc=0
```

## Kill matrix

Command shapes:
`python3 corpus/evidence/round50/cjk-ground-check.py --tool <mutant>` ·
`python3 corpus/evidence/round48/precision-count.py --tool <mutant>` ·
`<mutant> --entry corpus/knowledge/<e>.md --spans corpus/evidence/round50/spans.tsv --counts /dev/null --registry corpus/SOURCES.md --root .` for the three landed entries.

| mutant | cjk-ground-check | precision-count | landed exits (r40/r41/r39) | landed tokens= (r40/r41/r39) |
|---|---|---|---|---|
| m1 floor≥1 | PASS rc0 | 12/12 PASS rc0 | 0 / 0 / 0 (unchanged) | 10 / 7 / 13 (unchanged) |
| m2 floor≥10 | PASS rc0 | 12/12 PASS rc0 | 0 / 0 / 0 (unchanged) | **9 / 5 / 13** |
| m3 CJK_RE=[\u4e00-\u9fff] | PASS rc0 | 12/12 PASS rc0 | 0 / 0 / 0 (unchanged) | 10 / 7 / 13 (unchanged) |
| m4 CJK only when no Latin word | PASS rc0 | 12/12 PASS rc0 | 0 / 0 / 0 (unchanged) | 10 / 7 / **12** |
| m5 words() CJK-aware | PASS rc0 | 12/12 PASS rc0 | 0 / 0 / 0 (unchanged) | 10 / 7 / 13 (unchanged) |

**All five mutants SURVIVED.** No mutant changes an exit on the landed entries — none changes an
exit anywhere in the battery.

## Survivors, with what actually moved (imported each module, diffed `grounding_tokens` per bullet)

- **m2** drops 3 now-too-short CJK tokens, all still-covered bullets:
  `cnki-citation-check-r40.md` bullet2 `` `第一类是"没找到"` `` (7 CJK chars, the m2-killed band 4–9);
  `citation-matching-semantics-r41.md` bullet1 `` `各项内容都相同` `` (7); bullet4 `` `第 6 章 辅助功能` ``
  (6). Each bullet keeps other grounded tokens (10→9, 7→5, grounded=tokens), so rc stays 0.
- **m4** drops `istic-citation-verification-r39.md` bullet1 `` `所有文章必须包括全部作者（全拼）、标题、期刊、年、卷、页码、DOI等完整信息` ``
  (27 CJK + 3 Latin `DOI`; one whitespace word with Latin → `if words: return False`). Bullet
  still exits 0 on remaining tokens (13→12).
- **m1, m3, m5** are behavior-identical on all six runs (token counts unchanged everywhere).
- Kana question: **no lane entry among the three quotes Japanese** (kana regex `[\u3040-\u30ff\uff66-\uff9f\u31f0-\u31ff]`
  → False for all three entries; no matches in `corpus/evidence/round50/` at all). Japanese IS
  quoted elsewhere in the lane, e.g. `corpus/knowledge/aggregator-vs-source-r36.md:17`
  `"CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずしも一致していません"`, so m3's dropped
  ranges are load-bearing lane-wide but invisible to this battery.

## Why nothing kills these (coverage finding, not a contract change)

- `cjk-ground-check.py` cases use quotes of ≥10 CJK chars (case B `该列表显示最终的判定结论并给出评分`,
  17 chars; case A span quote 29), so floors 1/4/10 are indistinguishable to it; all cases are pure
  Chinese, so m3 (kana), m4 (mixed Latin+CJK) and m5 (polarity) see identical inputs.
- `precision-count.py`'s 12 cases are all-Latin; the CJK branch is never taken.
- The landed receipts are exit-only: exit-invariance means the wave-1 C2 gate decisions would not
  flip under any of the five mutants; the finer observable that does move is the `GROUND tokens=`
  count (m2: 9/5/13; m4: 10/7/12). A future check that diffs token counts — not just exits — would
  kill m2 and m4; a kana-bearing or sub-4-char CJK quote fixture would kill m1/m2/m3.

## Cleanup

- `rm -rf /dev/shm/chousa-r50-R50MutInferenceCJK/` run after the re-hash above; scratch gone.
- Writes made: this report only. No production file, sibling report, index, or /tmp touched.

VERDICT: attacked the post-freeze `has_two_words`/`CJK_RE` gate with 5 mutants × 3 detectors × 3 landed entries — all 5 SURVIVED (no exit changes anywhere; only m2/m4 move token counts 10→9, 7→5, 13→12), a detector-coverage finding; the frozen bytes survived.
