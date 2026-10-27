# R57W1CritLessonFlags — attack on the R57-C2 FRESHNESS-FLAG leg

Seat: R57W1CritLessonFlags (critic, leaf). Scope: the FLAG leg of the frozen C2 predicate
(`corpus/evidence/round57/c2-count.py`, R57-C2 frozen at lane commit c2f914c5). No lane files
were edited; all mutations were inside a scratch fixture clone, deleted before yield.

## What the leg requires (frozen, read at c2-count.py)

- `:62` `FLAG_RE = ^- FRESHNESS-FLAG (S\d{3}) ([0-9a-f]{24}) absent=(\d+)/(\d+)$` — line grammar.
- `:194` parsed lines stored as `flags[(id, key)] = (a, m)` — keyed by (id, key) pair.
- `:226-228` for each DRIFTED triple only: `need_flag += 1` when some pinned quote is absent
  from the defined form; `flagged += 1` iff `flags.get((sid, k)) == (absent, m)` — exact tuple.
- `:238` `ok_all` requires `flagged == need_flag`.

## Fixture construction (scratch clone of the lane, `--shared`)

S113 triple: url `https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3`,
key `453d492becd9a2f4632cb8dd`, pin `ad6b09f0…571cdc52`; 6 pinned quotes from
`corpus/evidence/round52/spans.tsv` at SET_REV (all six rows, `git show 6656f077:…`).

Occurrence probe on the committed fresh capture (all my own checks):

```
Q1..Q6 in lane .txt form: True True True True True True     (absent=0/6 — matches dispatch note)
Q1..Q6 verbatim in .raw : False False False True True True  (Q1-Q3 are tag-joined by html_to_text)
```

Baseline counter run on the untouched scratch clone (tip f9736a3 worktree):

```
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS
```

(The 4 pending retries have since landed: 41 REPRODUCED / 1 UNREACHABLE.)

Absence crafted via the FORM path per assignment: in the scratch clone only, replaced the two
verbatim-occuring quotes Q5 (`NameList=[AttachmentFileName…])`) and Q6 (`梅斯医学是面向医生的综合互联网平台`)
in `453d492becd9a2f4632cb8dd.raw` with equal-length `X` runs, regenerated `.txt` with the
counter's own `recipe_txt`/`html_to_text` (imported from the scratch copy of the frozen
counter), and updated the S113 attempt-2 row of scratch `refetch.tsv` (raw_sha256 →
`5e8fe074…`, txt_sha256 → `b2fc718f…`). Observed: pin still differs from both shas (stays
DRIFTED), and the counter's own per-quote recount gives **absent=2/6** — Q5, Q6 absent, Q1-Q4
present. CONSISTENT stayed 46/46 in every scenario run below, so the FLAG leg was the only
varying axis.

## Scenarios (each counter summary line pasted verbatim; verbose S113 line identical in all runs)

S0, no lesson line (fixture sanity — need_flag must fire):
```
CAPTURE S113 453d492becd9a2f4632cb8dd pin=ad6b09f0599c DRIFTED absent=2/6
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/1 C2=FAIL
```

(1) lesson line a off by one, `- FRESHNESS-FLAG S113 453d492becd9a2f4632cb8dd absent=3/6`:
```
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/1 C2=FAIL   (counter exit=1)
```
m off by one (`absent=2/5`) — same FAIL, `FLAGGED=0/1`. Exact tuple equality; no tolerance. ✔ must FAIL, does.

(2) exact line, `absent=2/6`:
```
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=1/1 C2=PASS   (counter exit=0)
```
✔ leg passes.

(3) exact S113 line plus a bogus flag for a REPRODUCED triple,
`- FRESHNESS-FLAG S118 16fe8487aa97b98576a0dbac absent=9/9`:
```
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=1/1 C2=PASS
```
✔ the REPRODUCED-triple line is parsed but never consulted — counts unchanged.

(4) right id, wrong key, `- FRESHNESS-FLAG S113 000000000000000000000000 absent=2/6` (a/m exact):
```
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/1 C2=FAIL
```
✔ key mismatch → ignored; the triple goes unflagged.

Bonus probe, two lines same (id,key): `absent=2/6` then `absent=4/6`:
```
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/1 C2=FAIL
```
`:194` dict last-wins — a stale/wrong later line overrides a correct earlier one, failing closed.

## Findings (impacted axes)

1. **Freshness FLAG leg: SURVIVES.** Off-by-one in a or m fails (`FLAGGED<need_flag`); exact a/m
   passes; flag lines for REPRODUCED triples and wrong-key lines are ignored. The leg cannot be
   satisfied by a hand-rolled guess — the reporter must quote the counter's own a/m.
2. The leg is currently **vacuous at the real lane tip** (all 5 DRIFTED triples have absent=0,
   `FLAGGED=0/0`); this fixture is the first exercise of the nonzero path I am aware of this wave.
3. Calibration note for the L1/lesson seat: the flag line must be the counter's *final* numbers —
   any later correction line overrides it (last-wins), and a wrong line cannot be rescued by an
   earlier right one. Write one line, write it last, copy a/m from `c2-count.py --verbose`.
4. No defect found that the canonical Rust judge must reject; all behaviors match the frozen
   predicate text. Findings reported, not patched — no counter/lesson changes proposed.

Hygiene: no tools installed; no network use; scratch dir
`/fast/scratch/hyaku/chousa-r57/R57W1CritLessonFlags` deleted (`rm -rf`) before this report;
only write outside scratch is this file.

VERDICT: attacked the R57-C2 FRESHNESS-FLAG leg with a scratch DRIFTED S113 fixture (absent=2/6) — off-by-one fails closed, exact a/m passes, REPRODUCED-triple and wrong-key flag lines are ignored; leg SURVIVES, no judge-blocking defect.
