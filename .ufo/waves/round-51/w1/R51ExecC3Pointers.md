# R51ExecC3Pointers — C3 repair map: the five dangling pointers, each to an on-disk target

Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`. The counter was only ever run read-only from the lane with `--root` on a `/dev/shm` scratch tree; no production file, git index or jj state written. No tool install. Scratch `/dev/shm/chousa-r51-R51ExecC3Pointers/` deleted before yield.

## 1. Before-state (matches `claims-erratum.md` E1: 8 → 5)

```
$ python3 corpus/evidence/round51/c3-count.py; echo "EXIT=$?"
CAP_ROWS=36 (base 36)
POINTERS=74 (base 74)
RESOLVED_BY_CORRECTION=0
DANGLING SCORECARD.md:1843 measure/final/
DANGLING SCORECARD.md:2073 measure-l1/c1-s36361.json
DANGLING SCORECARD.md:2074 measure-l1/c2-s36371.json
DANGLING SCORECARD.md:2616 c1-supplement.py
DANGLING SHONEN.md:10 round25-meta-differential.log
DANGLING=5
C3=FAIL
EXIT=1
```

## 2. What each row meant (row text read at the printed line)

`for n in 1843 2073 2074 2616; do sed -n "${n}p" SCORECARD.md; done` → rows 1843 (`serialized manifest appends`), 2073 (`engine-swap canary`), 2074 (`per-record argv attribution`), 2616 (`adopter self-test`); `sed -n '10p' SHONEN.md` → the `research-gate.sh --selftest` evidence line. Every pointer is a bare basename or a bare wave-relative dir; the row's prose gives the round (1843/2073/2074 name their round in the heading above the table, 2616 in `## Capabilities (round-50 addition)`).

## 3. Candidate per pointer — all five exist; none is a never-committed name

| DANGLING | Candidate (lane-relative) | Why it is the one (command evidence) | size |
|---|---|---|---|
| `SCORECARD.md:1843 measure/final/` | `.ufo/waves/round-32/measure/final/` | `grep -o "APPEND_SERIALIZED=[0-9/]*" .ufo/waves/round-32/measure/final/*` → `c1-s32101.json`, `c1-s32102.json`, `battery.out` all `APPEND_SERIALIZED=24/24` (row's 24/24); `grep -rl "APPEND_SERIALIZED=24/24" .ufo/waves` lists only round-32 trees; round-33's `measure/final` has 0 such files (`grep -rl APPEND_SERIALIZED .ufo/waves/round-33/measure/final \| wc -l` → `0`); the lane itself spells the full path at `corpus/lessons/round-32-verifier-spotcheck.md:66` and `corpus/QUALITY.md:296` | 12403 B, 9 files |
| `SCORECARD.md:2073 measure-l1/c1-s36361.json` | `.ufo/waves/round-36/measure-l1/c1-s36361.json` | receipt `"label": "ENGINE_SWAP_CANARY=14/14"`, `"matched": 14`, `"predicate_holds": true` (row says 14/14); `find . -name 'c1-s36361*'` → one path; `git log --all --diff-filter=A --name-only -- '*c1-s36361*'` → `7659748 round-36: engine-swap canary 14/14 …` | 7039 B |
| `SCORECARD.md:2074 measure-l1/c2-s36371.json` | `.ufo/waves/round-36/measure-l1/c2-s36371.json` | receipt `"label": "WITNESS_PER_RECORD=5/5"` (row says 5/5); same `find`/`git log` uniqueness; round-36 `w1/RevReportCounts.md:56` cites `measure-l1/c1-s36361.json` (14/14) and `c2-s36371.json` (5/5) — the relative base is `.ufo/waves/round-36/` | 4069 B |
| `SCORECARD.md:2616 c1-supplement.py` | `corpus/evidence/round50/c1-supplement.py` | `find . -name 'c1-supplement*'` → this `.py` + its receipt only; docstring `Usage: python3 corpus/evidence/round50/c1-supplement.py`; `git log --all --diff-filter=A --name-only -- '*c1-supplement*'` → `1d7aba0 round-50: wave-2 … supplementary C1 check …` | 4175 B |
| `SHONEN.md:10 round25-meta-differential.log` | `corpus/evidence/round25-meta-differential.log` | the sibling pointer on the same line already carries the `corpus/evidence/` prefix (`round25-measure-after.log`, 5130 B, resolves); this file's content is the round-25 differential result `AGREE=54/54 (fixtures=27, modes normal+strict)`; added by `0fc037e round-25: metadata screen, index freshness, ledger calibration`; the `.ufo/waves/round-4{3,5}/assimilation/validate/…` copies are assimilation snapshots, not round-25's own | 47 B |

Pointer count on SHONEN line 10 is unchanged by the fix: `before 3 ['tools/research-gate.sh', 'corpus/evidence/round25-measure-after.log', 'round25-meta-differential.log']` / `after 3 [..., 'corpus/evidence/round25-meta-differential.log']` (via the counter's own `pointers()`).

## 4. (a) Append-only lines for SCORECARD.md — exact shape, row line as c3-count prints it

```
correction: SCORECARD.md:1843 measure/final/ -> .ufo/waves/round-32/measure/final/
correction: SCORECARD.md:2073 measure-l1/c1-s36361.json -> .ufo/waves/round-36/measure-l1/c1-s36361.json
correction: SCORECARD.md:2074 measure-l1/c2-s36371.json -> .ufo/waves/round-36/measure-l1/c2-s36371.json
correction: SCORECARD.md:2616 c1-supplement.py -> corpus/evidence/round50/c1-supplement.py
```

Precedent for append-only `correction:` lines in this lane: `corpus/lessons/round-49.md:220`; `grep -n "^correction:" SCORECARD.md` is currently empty, so the four lines are additions and no row line moves.

## 5. (b) SHONEN.md evidence line 10 — replacement (full lane-relative pointer, 3 pointers kept)

```
  `bash tools/research-gate.sh --selftest`; `corpus/evidence/round25-measure-after.log`, `corpus/evidence/round25-meta-differential.log` (lane assertion)
```

## 6. Replay: scratch root, lane tree symlinked, the two files copied, the lines applied

```
$ LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin; S=/dev/shm/chousa-r51-R51ExecC3Pointers/root
$ mkdir -p "$S"; for e in $(ls -A "$LANE"); do case "$e" in SCORECARD.md|SHONEN.md) continue;; esac; ln -s "$LANE/$e" "$S/$e"; done
$ cp "$LANE/SCORECARD.md" "$LANE/SHONEN.md" "$S/"
$ printf '%s\n' 'correction: SCORECARD.md:1843 measure/final/ -> .ufo/waves/round-32/measure/final/' \
    'correction: SCORECARD.md:2073 measure-l1/c1-s36361.json -> .ufo/waves/round-36/measure-l1/c1-s36361.json' \
    'correction: SCORECARD.md:2074 measure-l1/c2-s36371.json -> .ufo/waves/round-36/measure-l1/c2-s36371.json' \
    'correction: SCORECARD.md:2616 c1-supplement.py -> corpus/evidence/round50/c1-supplement.py' >> "$S/SCORECARD.md"
$ python3 - "$S" <<'PY'      # t.count("`round25-meta-differential.log`")==1, replace with the `corpus/evidence/` form
$ sed -n '10p' "$S/SHONEN.md"
  `bash tools/research-gate.sh --selftest`; `corpus/evidence/round25-measure-after.log`, `corpus/evidence/round25-meta-differential.log` (lane assertion)
$ python3 "$LANE/corpus/evidence/round51/c3-count.py" --root "$S"; echo "EXIT=$?"
CAP_ROWS=36 (base 36)
POINTERS=74 (base 74)
RESOLVED_BY_CORRECTION=4
DANGLING=0
C3=PASS
EXIT=0
```

## 7. Falsifiers — the repair is not vacuous (each control breaks one element)

```
$ python3 corpus/evidence/round51/c3-count.py --root <ctrl>   # grep -E '^(RESOLVED_BY_CORRECTION|DANGLING=|C3=)'
root              RESOLVED_BY_CORRECTION=4  DANGLING=0  C3=PASS
ctrl-rownum       RESOLVED_BY_CORRECTION=3  DANGLING SCORECARD.md:1843 measure/final/          DANGLING=1  C3=FAIL   # line 1843 → 1844
ctrl-nofile       RESOLVED_BY_CORRECTION=3  DANGLING SCORECARD.md:1843 measure/final/          DANGLING=1  C3=FAIL   # target → .ufo/waves/round-32/measure/absent/
ctrl-trunc        RESOLVED_BY_CORRECTION=3  DANGLING SCORECARD.md:1843 measure/final/          DANGLING=1  C3=FAIL   # pointer written `measure/final` (no slash)
ctrl-noshonen     RESOLVED_BY_CORRECTION=4  DANGLING SHONEN.md:10 round25-meta-differential.log DANGLING=1  C3=FAIL   # SHONEN left at base
ctrl-empty        RESOLVED_BY_CORRECTION=3  DANGLING SCORECARD.md:2616 c1-supplement.py         DANGLING=1  C3=FAIL   # target a 0-byte zero.json
```

So the counter needs: the exact row line, the exact pointer token, a target that exists, non-empty, and the SHONEN edit as a real path edit — not a blanket pass.

## 8. Named limits I could not close

- The counter tests existence, not truth: a `correction:` line pointing at a non-empty but wrong file would pass. My targets rest on content, not existence — the receipts' own labels (`APPEND_SERIALIZED=24/24`, `ENGINE_SWAP_CANARY=14/14`, `WITNESS_PER_RECORD=5/5`, `AGREE=54/54`) and the round commits that added each file.
- `measure/final/` is a directory pointer; `real()` accepts it via `rglob`, so its nine files (12403 B) are what satisfy the pointer, and a future empty `final/` would flip it back to DANGLING.
- The `correction:` mechanism is a suffix record; the rows themselves still print the bare basename. If the L1 prefers in-row rewrites, the counter would then need no correction lines — but that moves the row text, which this wave's frozen target does not ask for.
- The lane tip still prints `DANGLING=5 C3=FAIL` (re-run read-only after the replay) because no lane file was changed: applying §4a/§4b is the L1's write, and the counter then needs one run.

VERDICT: Attacked the five DANGLING pointers of frozen C3 — each has exactly one committed non-empty target, evidenced by receipt content and add-commits; the four append-only correction lines plus the SHONEN line-10 full path drive a scratch replay to `DANGLING=0 C3=PASS` with `CAP_ROWS=36/36`, `POINTERS=74/74`, and five single-element controls still `C3=FAIL`.
