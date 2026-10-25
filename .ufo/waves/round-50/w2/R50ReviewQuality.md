# R50ReviewQuality — QUALITY criteria 73-79 vs the shape of 70-72 and vs reality

Attacked: every pasted output, exit code, receipt path and the `correction:` line
in `corpus/QUALITY.md:751-843` at HEAD `c5b8dca` (landed package is `74794db`;
HEAD adds only `.ufo/waves/round-50/w2*` files — `git diff 74794db HEAD --stat`
shows no corpus/tool change).

## Shape and numbering — survives
Criteria 73-79 keep the 70-72 shape (bold rule, check command, `Shown able to
fail`, `Named limit(s)`, lesson pointer). `grep -nE '^[0-9]+\.'` → 79 items,
contiguous; `## Round-50 additions (appended 2026-10-25; criteria 1–72 unchanged)`.
`git diff 3c51da77… 74794db… -- corpus/QUALITY.md` = `96 insertions(+)` only;
criteria 1-72 byte-unchanged verified.

## Criterion 73 (selftest scored on perturbed copies) — survives
`python3 corpus/evidence/round50/c1-count.py` → `LEGS=5/5 C1=PASS` exit 0,
byte-identical to `measure-after-1.txt`. `python3 tools/assimilate-rows.py
--selftest` → `SELFTEST=PASS findings=26 expected=26` and
`FIXTURES_SHA256=c5c56480e9f6…` (= counter PIN `c5c56480e9f6a08d…`). P1-P6 named
`DIFF` lines are asserted in `c1-count.py:107-112`. `EXPECTED_BAD=PASS rc=2`
(S0=ERROR leg). Controls replay byte-identical to `controls/c1-before.txt`:
tool-before → `BASELINE=FAIL rc=2 … LEGS=2/5 C1=FAIL`; echo → `BASELINE=PASS
PERTURB_PASS=0/6 LEGS=4/5 C1=FAIL`; const → `PERTURB_PASS=0/6 LEGS=2/5 C1=FAIL`.
`selftest-duplicates-after.txt` exists and matches the named limit.

## Criterion 74 (stale counts) — DEFECT FOUND (three parts)
Check run now:
```
$ python3 corpus/evidence/round50/stale-count-check.py
RESOLVED corpus/QUALITY.md:746 says 28, receipt 31
RESOLVED corpus/QUALITY.md:786 says 28, receipt 31
RESOLVED corpus/README.md:1074 says 28, receipt 31
STALE corpus/README.md:1080 says 55, receipt 31
RESOLVED corpus/README.md:1083 says 28, receipt 31
STALE LOG.md:1803 says 28, receipt 31
RESOLVED corpus/lessons/round-49.md:20 says 28, receipt 31
RESOLVED corpus/lessons/round-49.md:220 says 28, receipt 31
STALE_HITS=8 UNRESOLVED=2 RECEIPT_ROWS=31
STALE_COUNT=FAIL
exit=1
```
- F74a — claimed output does not reproduce: text says "after them
  `STALE_COUNT=PASS`, exit 0 (`stale-count-after.txt`)". Observed FAIL exit 1.
- F74b — cited receipt missing: `ls corpus/evidence/round50/stale-count-after.txt`
  → No such file (dir listing shows only `stale-count-before.txt`).
- F74c — the check is unpassable on the landed corpus: `README.md:1080` prints
  `55` (the round-50 manifest size, correct prose) but the scan's single receipt
  is 31 (`evidence/round49/spans.tsv` data rows); and `LOG.md:1803` (28 located
  quotes) has no `correction:` line naming it — `grep -n correction LOG.md`
  hits 1663/1777/1791, none naming 1803; LOG.md is append-only. Both hits
  already exist at `74794db` (`git show 74794db:corpus/README.md` line 1080
  = "55-row manifest"; no LOG correction in that tree). The disclosed
  "one receipt per scan" named limit is exactly what bites: the very row added
  to README describing this round's own 55-row manifest trips the check.
Sub-claim verified in the other direction: the four pre-correction STALE lines
(QUALITY.md:746, README.md:1074, LOG.md:1803, round-49.md:20) are still
present verbatim, so `stale-count-before.txt`'s "four STALE says 28" is
consistent. `correction:` line — `QUALITY.md:786` names `corpus/QUALITY.md:746`
with "superseded by"; checker output prints `RESOLVED corpus/QUALITY.md:746`
→ the correction mechanism does resolve 746 specifically. Receipt 31 is real:
`corpus/evidence/round49/measure-after.txt:78` = `IDS=8 QUOTES=31 FAILURES=0`;
`awk 'NR>1' corpus/evidence/round49/spans.tsv | wc -l` = 31 (56-line
round-50 spans.tsv/quotes.tsv are a different receipt the check cannot see).

## Criterion 75 (wave-complete gate) — survives
Replays byte-identical to `wave-complete-before.txt`:
`.ufo/waves/round-49/w2-spec.json .ufo/waves/round-49/w2 --rev 5275c892…` →
8 MISSING (MutA05, MutSubstance, ReviewQuality, ExecReplayC1, ScribeScorecard,
ScribeTrends, ScribeShonen, ScoutPlanned) `OK 27/35` exit 1; r50 w1 → 13
MISSING `OK 29/42` exit 1. Positive leg (criterion claims exit 0):
round-49 w1 spec+dir → `OK 40/40` exit 0. Unusable spec: `/dev/null` → `ERROR`
stderr, exit 2.

## Criterion 76 (decode form named) — survives
`decode-form-check.py corpus/lessons/round-47.md` → `FORM_MISSING` exit 1;
`round-50.md` → `FORM_NAMED` exit 0. Exactly as printed.

## Criterion 77 (cited ids) — survives (one naming nit)
`staged-ids`/`renumber.tsv` in `.ufo/waves/round-50/assimilation/` hold the
cleaned 5-row table. Reconstructed the as-staged 7-row table (5 committed rows
+ S109->S104, S111->S105 per the receipt) and ran the check on the three staged
entries (`/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/
knowledge/{cnki-citation-check-r40,citation-matching-semantics-r41,
istic-citation-verification-r39}.md`): `BODY_CROSSREF S109->S104`,
`BODY_CROSSREF S111->S105`, `CITED_IDS=FAIL rows=7` exit 1 — receipt verbatim.
5-row table on staged entries → `CITED_IDS=PASS rows=5` exit 0. Nit: the
criterion/receipt phrase "entries with body-only ids removed" describes the
renumber TABLE losing body-only rows (S109/S111 appear only in body prose —
`cnki-citation-check-r40.md:41` `round 4's `S109`–`S111``), not edited entries.
Also `renumber.tsv` maps S145->S107; `grep '^\| S107 '` corpus/SOURCES.md →
no row (S145 adopted entry refused) — consistent, not counted.

## Criterion 78 (unique seat names) — survives
`name-collision-check.py .ufo/waves/round-50/w1-spec.json` → the same 13
`NAME_COLLISION` lines + `NAME_COLLISIONS=13 ITEMS=42`, exit 1 (byte-identical
to `name-collision-before.txt`). `w2-spec.json` → `NAME_COLLISIONS=0 ITEMS=43`
exit 0 — the 13 re-assigned seats carry new names.

## Criterion 79 (CJK grounding gate) — survives
Old tool extracted: `git show 74794db^:tools/inference-ground.py` (diff shows
only the CJK_RE/`has_two_words` change). `cjk-ground-check.py --old <that>` →
`CASE A rc=0`, `OLD_TOOL case A rc=1 INF_UNGROUNDED`, `CASE B rc=1
INF_TOKEN_NOT_IN_SPAN`, `CASE C rc=1 INF_UNCITED`, `CJK_GROUND=PASS` exit 0 —
verbatim. `diff inference-regression-before.txt -after.txt` → only the header
line and the trailing 65-entry note differ; all five counter outputs identical.

## Residual risk / gaps
- `spans.tsv` `offset` column is the span-block start (CONTEXT=80 per
  build-spans docstring), not quote position — peer R50ReopenRowS105's offset
  flag was self-retracted; naming ambiguity only, outside this ticket.
- Criterion 73's `selftest()` "only reads" the expected file asserted via
  docstring (`tools/assimilate-rows.py:44-59`) + observed SELFTEST output;
  I did not line-audit selftest() beyond that.
- No install needed; scratch `/dev/shm/chousa-r50-R50ReviewQuality/` deleted.

VERDICT: QUALITY 73-79 — defect found in criterion 74: `stale-count-check.py`
prints `STALE_COUNT=FAIL` exit 1 on the landed tree (LOG.md:1803 uncorrected;
README.md:1080's correct "55-row manifest" unresolvable under the one-receipt
limit) and the cited receipt `stale-count-after.txt` does not exist; criteria
73, 75, 76, 77, 78, 79 and the correction-of-746 mechanism reproduce exactly.
