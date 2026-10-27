# R57-W2 · R57W2CritDoNothingRound — whole-round do-nothing control, both claims

seat: `R57W2CritDoNothingRound` · wave 57/2 · lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`
claims attacked: **R57-C2** (`c2-count.py`) and **R57-C3** (`c3-count.py`), both landed/PASS at lane tip
`1c9626e`. Frozen claims `corpus/evidence/round57/claims.md` (C2 freeze `c2f914c`, C3 freeze `fd95724`).

## Fixture (the strongest "did nothing" state available)

A `git clone --shared` of the lane, checked out at the round **base** `6656f0770a1460d6ba73d9d2976f698a35311921`,
plus **only** the 14 wrap-up capture files restored byte-exact from `git show b022b13:corpus/captures/<f>` —
no `refetch.tsv`, no entry, no c3 manifest/span rows, no round-57 lesson, no claims file. The two tip counter
scripts were copied in uncommitted solely as the measurement yardstick (they do not exist at base:
`git cat-file -e 6656f07:corpus/evidence/round57/c2-count.py` → `exists on disk, but not in '6656f07…'`;
same for c3). Purity: `git status --porcelain` shows exactly `?? corpus/captures/` (14 files) and
`?? corpus/evidence/round57/` (the 2 counters).

Scratch: `/fast/scratch/hyaku/chousa-r57/R57W2CritDoNothingRound/` (`TMPDIR`/`PYTHONDONTWRITEBYTECODE=1`
exported for every run; `git rev-parse --show-toplevel` asserted `== …/clone` before each counter run).

## Evidence — fixture is exact

```
$ git -C clone rev-parse HEAD
6656f0770a1460d6ba73d9d2976f698a35311921
$ for f in $(git show --name-only --format= b022b13); do git show "b022b13:$f" > "$f"; done
$ git rev-parse "b022b13:$f"  vs  git hash-object "$f"        # all 14
OK  corpus/captures/02aefcf570a7108e699d0990.raw   … OK ×14 (13 .raw + b539a80218080da56a75b624.txt)
$ find corpus/captures -type f | wc -l
14
$ ls corpus/evidence/round57/
c2-count.py  c3-count.py
absent corpus/evidence/round57/refetch.tsv
absent corpus/knowledge/normative-reference-chain-china-r57.md
absent corpus/evidence/round57/c3/spans.tsv
absent corpus/lessons/round-57.md  ·  absent corpus/evidence/round57/claims.md
```

(pdftotext is `version 26.08.0` on this host — the counter's env check, so `C2=FAIL` below is a verdict
failure, not `ENV_CHANGED`.)

## Run — C2 on the fixture

```
$ git rev-parse --show-toplevel
/fast/scratch/hyaku/chousa-r57/R57W2CritDoNothingRound/clone
$ python3 corpus/evidence/round57/c2-count.py
SET=47 VERDICTS=0/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=0 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL
C2 exit=1
$ python3 corpus/evidence/round57/c2-count.py --verbose | grep -c '^CAPTURE '
47
```

The pinned set is genuinely enumerated (47 `CAPTURE` lines at `SET_REV`), and the 14 committed capture
bytes alone cannot produce even one verdict: every triple is `MISSING` because no `refetch.tsv` attests a
successful attempt (`ok` empty → `not the last successful attempt's bytes` where a `.raw` happens to exist).
`VERDICTS=0/47 < 47`, `C2=FAIL`, exit 1.

## Run — C3 on the fixture

```
$ git rev-parse --show-toplevel
/fast/scratch/hyaku/chousa-r57/R57W2CritDoNothingRound/clone
$ python3 corpus/evidence/round57/c3-count.py
ENTRY=no S127_CITED=no NEW_GROUND=no CLAUSE=no
BOUND=0/7 (min 4) -
SWEPT=0/7 -
QUOTE_ROWS=0 IN_SPAN=0 IN_ENTRY=0 IN_LESSON=0 SHORT=0 CONTEXT=0 CAPTURE_BOUND=0
SUBSTANCE=FAIL ANCHOR_BOUND=0/0 INFERENCE_GROUNDED=no STRAY_IDS=-
C3=FAIL
C3 exit=1
```

`ENTRY=no` with `BOUND=0/7`: the wrap-up bytes contribute nothing toward a bound reference — even held
surfaces can't bind without the entry, manifest rows and successful-attempt records, so the claimed
chaining work is load-bearing, not decoration.

## Assessment

- Neither `C2=PASS` nor `C3=PASS` is reachable from base + pre-existing committed bytes alone; the
  do-nothing bar holds for the whole round, not just claim-by-claim. **SURVIVES this attack.**
- W1 corroboration read: `w1/R57W1ExecDoNothing.md` (C2-side control, variants A/B `VERDICTS=0/47` FAIL on
  the freeze commit — same result at the stricter base here) and `w1/R57W1CritC2Controls.md`.
- Residual note (reported, not patched; claims are frozen): W1 already showed `REPRODUCED>=5` is met by 10
  of these 14 pre-existing wrap-up bytes and that the disclosed forge passes with zero network. That is a
  statement about the forge lane, not the do-nothing lane — the fixture here keeps no `refetch.tsv` at all,
  and the counter still binds. No new defect found; nothing in my runs contradicts the landed PASS state.

## Boundaries honoured

Only this report file written in the lane; all mutation inside the scratch clone; frozen counters copied
(read-only) never edited; no network; scratch `/fast/scratch/hyaku/chousa-r57/R57W2CritDoNothingRound/`
deleted before yield (`rm -rf`, verified). No tool installed or upgraded.

**VERDICT: attacked the whole-round do-nothing control — clone @ base 6656f077 + the 14 b022b13 capture bytes and nothing else runs C2 to VERDICTS=0/47 C2=FAIL (exit 1) and C3 to ENTRY=no BOUND=0/7 C3=FAIL (exit 1): both claims' do-nothing bars SURVIVE, neither PASS is reachable without the claimed work.**
