ATTACKS: QUALITY 67 — Check line run on the three junk + three positive r47 fixtures and on both round-47 knowledge entries (`--spans corpus/evidence/round47/spans.tsv --counts /dev/null`), 'Shown able to fail' against controls/c1-controls.txt, every sentence vs observed behaviour.

VERDICT: holds (with one wording mismatch in the Named-limit sentence — see finding)

## Runs (cwd = /home/vgpnk/Projects/shokunin/chousa-shokunin)

1. Check line on all six fixtures (`tools/inference-ground.py --entry <f> --spans corpus/fixtures/inference-ground-r47/spans.tsv --counts corpus/fixtures/inference-ground-r47/counts.json --root .`):
```
junk-flip-asserted.md  FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / revised'  exit=1
junk-flip-denied.md    FINDING INF_POLARITY_FLIP bullet=1 token='the release ships a frozen pool / frozen' exit=1
junk-flip-figure.md    FINDING INF_POLARITY_FLIP bullet=1 token='7,572 / counts key figures/answers_named_source' exit=1
positive-affirmed.md        GROUND: PASS exit=0
positive-figure-negated.md  GROUND: PASS exit=0
positive-negation-kept.md   GROUND: PASS exit=0
```
Criterion 67 lines 650-652 ("the three `junk-flip-*.md` fixtures … each exit 1 on that code") match verbatim.

2. Frozen counter (`corpus/evidence/round47/c1-count.py`):
```
TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS exit=0
```
Matches measure-after.txt:5-13 and the claimed after-state.

3. 'Shown able to fail' controls re-run (`c1-count.py --tool corpus/evidence/round47/controls/<x>.py`):
- base-tool-r46.py: `POSITIVE_PASS=3/3 JUNK_KILLED=0/3 CANARY=fail R46_COUNTER=pass R46_ENTRIES=2/2 C1=FAIL` exit=1 — matches c1-controls.txt:3-11; the `JUNK_KILLED=0/3` quoted in criterion 67 line 652 holds.
- always-exit-1.py: `POSITIVE_PASS=0/3 JUNK_KILLED=3/3 CANARY=fail R46_COUNTER=fail R46_ENTRIES=0/2 C1=FAIL` exit=1 — matches c1-controls.txt:13-21.
- neg-word-refuser.py: `POSITIVE_PASS=1/3 JUNK_KILLED=3/3 CANARY=fail R46_COUNTER=fail R46_ENTRIES=0/2 C1=FAIL` exit=1 — matches c1-controls.txt:23-31.

4. Check line on the two round-47 entries (as specified, `--counts /dev/null`):
```
claim-support-test-r37.md: section=1 bullets=7 tokens=16 grounded=16 GROUND: PASS exit=0
claim-support-test-r37-amendment-2026-10-23.md: section=1 bullets=6 tokens=21 grounded=21 GROUND: PASS exit=0
```

5. Named-limit sentences (lines 653-657) vs observed behaviour. Tool internals verified at tip 1fc5ed193… (sha256 244a1897…, `git status --porcelain` clean): `occurrence_polarity`/`polarity_flips` (:274-338) — P1 window 3-before/2-after, P2 3-before, figure window next 4; `stem = w[:5]` (:262-263); `NEG_WORDS`/`IMPLICIT_NEG`/`UN_NEG_RE` (:232-259). Empirically (all on /tmp copies of the r47 fixture spans/counts):
- different-stem flip passes: bullet "Because `no revision is recorded`, every sentence is edited after publication" → exit=0 (matches "a flip through a different stem … still passes").
- distant negator passes: "The record shows no trace of `no revision is recorded` ever reaching back to its origin" (negator "no" 4+ words from the scope word) → exit=0; "Although `the release ships a frozen pool`, the pool is not, by any reading of it, frozen" → exit=0 (matches lesson `CritC1Survivors` b2-far).
- double negation passes: "Because `no revision is recorded`, there is no sentence that is not revised after publication" → exit=0.
- second-bullet flip passes: bullet 2 "every sentence is revised after publication" quoting `the archived copy is dated at build` (S902) → exit=0 (survivor b4b).
- **Mismatch**: line 656 "a correct bullet whose negator sits outside the window is refused". Observed: the correct bullet is NOT refused — it passes (exit 0). Re-ran the wave-1 lab p01-p10 bodies verbatim (LabC1FalsePos.md:49-60) against the tip tool: p01 (revisions are untraceable), p02 (lacks), p07 (lacks), p10 (unsuitable) now `exit=0`; only p03/p05/p06/p08/p09 `exit=1`. The lab's 9/10 refusal count was measured at commit a15610a5, before the refinements commit 980fe43 (implicit negators, clause-bounded look-back) that landed before criterion 67 was written; the lesson's own Named-limit note (round-47.md:110-113) records the same finding in the correct direction: "a negator four or more words away … still passes". Line 656's "refused" is inverted: the tool accepts (does not refuse) a correct bullet whose negator sits outside the window. The rest of lines 653-656 (fixed windows: three before/two after/four after a figure; five-letter stem; different stem, distant negator, double negation, second bullet still pass) match observed behaviour.

6. Residual risk / gaps: the window escapes above were probed on sanitised /tmp fixture copies, not on the production tree (seat contract). The figure leg is fixture-only in lane practice (`--counts /dev/null` everywhere); criterion 67's Check line with `--counts /dev/null` (as run in item 4) exercises only the P1/P2 phrase legs. No fetch, no installs, no lane production file touched; scratch `/tmp/qual67` deleted.
