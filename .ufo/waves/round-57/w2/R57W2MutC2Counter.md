# R57W2MutC2Counter — mutation probe of the frozen R57-C2 counter at the landed AFTER-state

seat: R57W2MutC2Counter (wave W2 residual falsify, chousa round 57)
target: `corpus/evidence/round57/c2-count.py` (frozen counter; live lane sha256 `d6885bae2e8485e28f7d6e1fa59de7a0b3639ee0a242c71baf4c8ba753cb35f9`)
state attacked: landed PASS state — clone HEAD `3010e7537d163d9a76264a166d491214ecdaf45e` (= named tip `1c9626ef…` plus the W2-dispatch commit; `git diff 1c9626e..HEAD` touches only `.ufo/**`, zero `corpus/`/`tools/` files)

## Fixture (mutants applied to copies inside a `git clone --shared`; pristine file never touched)

```
$ git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/lane
$ cd $S/lane && git rev-parse --show-toplevel
/fast/scratch/hyaku/chousa-r57/R57W2MutC2Counter/lane
$ for m in 1..8: cp corpus/evidence/round57/c2-count.py corpus/evidence/round57/mutM$m.py
```

Mutant copies sit in `corpus/evidence/round57/` so `Path(__file__).parents[2]` still resolves to the clone root and `--root` defaults correctly; `pinned_set` globs `*spans.tsv` at SET_REV so `mutM*.py` files cannot enter the pinned set. env: python 3.14.8, pdftotext 26.08.0 (version gate passes), git 2.56.0, TMPDIR=$S, PYTHONDONTWRITEBYTECODE=1.

## Baseline (pristine copy, detector conclusive)

```
$ python3 corpus/evidence/round57/c2-count.py        # rc=0
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS
$ python3 corpus/evidence/round57/c2-count.py --verbose | grep -vE 'REPRODUCED '
CAPTURE S083 … DRIFTED absent=0/2   CAPTURE S087 … DRIFTED absent=0/2
CAPTURE S105 e3ca8f4f… UNREACHABLE 3 failed attempts   (+S113, S114, S121 DRIFTED absent=0/6,0/9,0/6)
```

Data facts that decide the mutants (`refetch.tsv`, 144 rows): 43 pinned triples have ≥2 successful attempts; exactly 3 (S111, S113, S114) have first-vs-last successful raw_sha256 differing; the only UNREACHABLE (S105) has 3 fails spanning 08:06:12Z→08:33:48Z = 1656 s; need_flag=0 (every DRIFTED capture still contains all pinned quotes, absent=0/m).

## Mutants — one edit each; detector = full counter run on the live clone state

| M | Edit (diff vs pristine) | Summary line | PASS/FAIL | Leg attacked → result |
|---|---|---|---|---|
| M1 | `MIN_REPRODUCED = 5` → `1` (L60) | `SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS` | PASS | floor → survives: REPRODUCED=41 ≫ 5, floor not load-bearing on this data |
| M2 | `if len(fails) >= 2 and (…>=600)` → `if len(fails) >= 2:` (L231) | identical to baseline | PASS | ≥600 s spacing → survives: sole UNREACHABLE S105 spans 1656 s |
| M3 | `ok_all`: drop `flagged == need_flag` (L238) | identical to baseline | PASS | FLAGGED leg → survives: need_flag=0, leg never exercised (equivalent mutant on this data) |
| M4 | consistent condition → `if True:` (L212-213) | identical to baseline | PASS | CONSISTENT → survives: all 46 backed `.txt` genuinely satisfy recipe+txt_sha256 |
| M5 | `ok[-1]` → `ok[0]` (L207 raw_sha256, L213 txt_sha256) | `SET=47 VERDICTS=44/47 REPRODUCED=40 DRIFTED=3 UNREACHABLE=1 BYTE_BACKED=43 CONSISTENT=43/43 FLAGGED=0/0 C2=FAIL` rc=1 | **FAIL** | "capture = last successful attempt's bytes" → **counter-killed**: S111/S113/S114 flip to MISSING (verbose: `capture not the last successful attempt's bytes`) |
| M6 | `if len(out) != SET_N:` → `… and False:` (L104) | identical to baseline | PASS | SET_N==47 enforcement → survives: pinned set is exactly 47, guard never fires |
| M7 | `len(fails) >= 2` → `>= 1` (L231) | identical to baseline | PASS | two-fail floor → survives: no pinned triple has exactly one failed attempt and no capture |
| M8 | consistent condition minus `ok[-1]["txt_sha256"] == sha(txt)` (L212-213) | identical to baseline | PASS | txt_sha256 record match → survives: weaker predicate implied by live data (all recorded txt_sha256 correct) |

M5 verbose (the kill):

```
CAPTURE S111 42bac883… pin=4d3bff5067 MISSING capture not the last successful attempt's bytes
CAPTURE S113 453d492b… pin=ad6b09f059 MISSING capture not the last successful attempt's bytes
CAPTURE S114 cacddf3b… pin=b1c3cd6a5c MISSING capture not the last successful attempt's bytes
```

(refetch.tsv shows these three have two successful attempts with different raw bytes — a first fetch then a re-fetch; the counter's LAST-attempt binding is what ties the stored `.raw` to the newest record.)

## Integrity / restoration

```
$ git -C $S/lane status --porcelain          # only ?? mutM{1..8}.py — zero tracked modifications
$ sha256sum corpus/evidence/round57/c2-count.py
d6885bae2e8485e28f7d6e1fa59de7a0b3639ee0a242c71baf4c8ba753cb35f9   # == live-lane file, == HEAD blob
$ diff <(git show HEAD:corpus/evidence/round57/c2-count.py) corpus/evidence/round57/c2-count.py   # empty → PRISTINE
```

Pristine bytes never mutated (mutants were copies); scratch dir deleted after this report. No lane/fleet file written except this report.

## Verdict table

| mutant | outcome | leg killed / coverage finding |
|---|---|---|
| M1 floor 5→1 | survived | REPRODUCED floor (slack 41 vs 5) |
| M2 drop 600 s spacing | survived | UNREACHABLE spacing (S105 margin 1656 s) |
| M3 drop FLAGGED==need_flag | survived | equivalent on this data (need_flag=0) |
| M4 consistent always | survived | CONSISTENT (all 46 truly consistent) |
| M5 first-not-last attempt | **killed** | last-attempt byte binding (VERDICTS 44/47, exit 1) |
| M6 drop SET_N==47 | survived | cardinality guard (never fires; set is 47) |
| M7 one-fail UNREACHABLE | survived | two-fail floor (no 1-fail captureless triple) |
| M8 drop txt_sha256 in CONSISTENT | survived | record-digest match (implied by data) |

VERDICT: attacked the frozen c2-count.py with 8 single-edit mutants at the landed state — M5 killed the counter (last-attempt binding is load-bearing), M1/M2/M3/M4/M6/M7/M8 survived as coverage findings on legs the live data cannot discriminate; the C2=PASS claim itself is not falsified.
