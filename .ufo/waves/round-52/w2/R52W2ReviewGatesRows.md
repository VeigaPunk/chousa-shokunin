# R52W2 ReviewGatesRows — wave-2 falsify report

Attacked: SKILL.md `## Gates` row `capture-text` (line 134) and row `chousa round-52 counters and checks` (line 135) — every command they print, run from the lane root with `TMPDIR`=scratch, every stated value checked. No defect found; all stated values reproduced.

Scratch: `/fast/scratch/hyaku/chousa-r52/R52W2ReviewGatesRows` (removed at exit). Skills read: `godspeed`. No installs (none needed; pacman guard untouched).

## 1. `capture-text` row — entry commands

Pinned capture `3a8b45977cd111e45e3980a5.raw` (under `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`):

```
$ sha256sum .../3a8b45977cd111e45e3980a5.raw
16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763   # matches row pin
$ python3 tools/capture-text.py <capture> > niph.txt; echo rc=$?   # rc=0
$ python3 -c 't=open("niph.txt",encoding="utf-8").read();print(len(t), t.count("SRにおける文献検索期間について明記する"), t.find("SRにおける文献検索期間について明記する"), t.count("\ufffd"))'
19682 1 8996 0
$ python3 tools/capture-text.py <capture> --locate "SRにおける文献検索期間について明記する"
LOCATED count=1 offset=8996      # rc=0; offset 8996 = code-point index, slice verified
```

19682 characters ✓, quote exactly once ✓, UTF-8 clean ✓.

## 2. Verdict map (exit codes)

| case | observed |
|---|---|
| absent quote `不存在` | `LOCATED count=0 offset=-1` rc=1 |
| quote `の` (occurs 559×) | `LOCATED count=559 offset=18` rc=1 |
| `--locate ""` | usage on stderr, rc=2 |
| no `raw` arg / `--locate` without value | argparse usage, rc=2 |

Refusals (each observed: rc=2, stdout empty, stderr starts `REFUSED`):

```
notzip.txt:  REFUSED not a zip (an OOXML capture is a zip package)
nooffice.zip: REFUSED no officeDocument relationship in _rels/.rels
missingmain.zip: REFUSED officeDocument target 'word/document.xml' is not in the package
badxml.zip:  REFUSED unreadable package: unbound prefix: line 1, column 0
xlsx.zip:    REFUSED main part 'xl/workbook.xml' is not WordprocessingML (root {…spreadsheetml…}workbook)
escape.zip:  REFUSED officeDocument target '../x.xml' leaves the package root
bigrels.zip: REFUSED '_rels/.rels' inflates to 269484032 bytes (limit 268435456)
meth99.zip:  REFUSED unreadable package: That compression method is not supported
encrypted.zip: REFUSED unreadable package: File '_rels/.rels' is encrypted, password required for extraction
```

All seven row-listed causes reproduce; the last two are the disclosed E2(e) additions (erratum), consistent with the row (which lists the seven causes, not the E2 extras).

## 3. `chousa round-52 counters and checks` row

C1 (lane root, `TMPDIR`=scratch):

```
$ python3 corpus/evidence/round52/c1-count.py        # and again with --seed 42
PARAS=PASS ok … REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682
LEGS=9/9   C1=PASS   rc=0
$ python3 corpus/evidence/round52/c1-supplement.py
PREFIX=PASS ok … REAL_TEXT=PASS rc=0 chars=19682
SUPPLEMENT_LEGS=4/4   C1_SUPPLEMENT=PASS   rc=0
```

Controls (c1-count `--tool`, same scores as pinned `controls/c1-before.txt`): `naive-tool.py` LEGS=4/9, `cache-txt-tool.py` 0/9, `const-tool.py` 0/9, all `C1=FAIL` rc=1. Base control replayed (archive of `00f8c7f5…` → `--tool base/tools/capture-text.py`): `tool absent`, LEGS=0/9, `C1=FAIL` rc=1 — matches receipt.

C2:

```
$ python3 corpus/evidence/round52/c2-count.py
ENTRIES=3/3  BOUND=4/4 (min 3) REFUSED=0  BOUND_IDS=S113,S114,S115,S116
REF_ID_UNBOUND=0  NEW_GROUND=3/3  QUOTE_ROWS=38 ON_BOUND=38/38
SPAN_IDS=4/4 (min 3 each)  QUOTES_IN_SPAN/ENTRY/LESSON=38/38
QUOTE_SHORT=38/38  SPAN_CONTEXT=38/38  CAPTURE_BOUND=38/38
SUBSTANCE=PASS  ANCHOR_BOUND=4/4  INFERENCE_GROUNDED=3/3
QUARANTINE_VERDICTS=1/1 (S120)  QUARANTINE_BLOCKED_ADOPTED=0
C2=PASS  rc=0
$ python3 corpus/evidence/round52/c2-count.py --lane-only   # same, CAPTURE_BOUND=skipped, rc=0
$ python3 corpus/evidence/round52/build-spans.py --check --root <lane>   # SPANS_ROWS=38 STALE=0 rc=0
$ python3 corpus/evidence/round52/verdict-gap.py --root <lane> --from 46 --to 51
R46 axes lane=6 verifier=6
R47 operability: lane=improved verifier=harmed        # gap
R48 UNPARSED lane_axes=6 verifier_axes=0             # UNPARSED round
VERDICT_GAPS=2 UNPARSED=1    rc=1
```

`verdict-gap` rc=1 is the row's live verdict (a gap exists); output matches lesson `round-52.md` line 88. Usage verdicts: c1-count/`--nonsense` rc=2, build-spans/`--nonsense` rc=2. C2 rc=2 is the `NO_BASE_OR_REGISTER` branch (source lines 152-156); a `--root` pointing away from the lane does not trigger it (base check is hard-wired to LANE), observed rc=1 — behavior note, not a row value.

## 4. Pinned hashes

```
$ git rev-parse HEAD            # d1d972c…  (wave-2 spec dispatch; its parent e769c03… is the W1 landing named in the assignment)
$ git cat-file -t 37468eadd8d098e80289b2f31a22de3872d4a1f6   # commit (freeze)
$ git cat-file -t 804a45370dc992bfe714817281535055c2f9b032   # commit (C1 candidate)
$ git cat-file -t 00f8c7f5272a1d98b6d34913985fa4537e00aaf9   # commit (BASE_REV; round-51 closure tip per log)
$ git ls-tree 37468ead… -- corpus/evidence/round52/claims.md  # 100644 blob 4288a9b3…
$ git hash-object corpus/evidence/round52/claims.md            # 4288a9b3… == freeze blob (claims unchanged since freeze)
```

Round-52 chain observed: `37468ea → 804a453 → 13bc280 → 01c17ce → e769c03 → d1d972c(HEAD)`. README base sweep (`git grep … 00f8c7f5… -- corpus/knowledge`) prints nothing, rc=1 ✓.

## 5. Round-47 counter (task-mandated)

```
$ python3 corpus/evidence/round47/c2-count.py
MISMATCHES=0 … C2=PASS   rc=0
```

## Findings

No defect: every command the two Gates rows print ran from the lane root with scratch TMPDIR, and every stated value (exit codes per verdict, LEGS=9/9, SUPPLEMENT_LEGS=4/4, control scores base 0/9 · naive 4/9 · cache-txt 0/9 · const 0/9, NIPH sha256 `16fc8c55…09763` and 19682 chars, quote-once at 8996, freeze `37468ead…` and BASE_REV `00f8c7f5…`, refusal reasons) reproduced. Notes, not defects: (a) HEAD is `d1d972c…` (wave-2 dispatch), the assignment's landed commit `e769c03…` being its parent; (b) `verdict-gap` currently exits 1 with `VERDICT_GAPS=2 UNPARSED=1`, which is its correct state (gaps disclosed in the lesson); (c) C2 `--root` does not redirect the base check (rc=2 only via `NO_BASE_OR_REGISTER`). Scratch cleanup: counter temp dirs removed on exit; only my scratch files remain.

VERDICT: attacked SKILL.md Gates rows `capture-text` (134) and `chousa round-52 counters and checks` (135) — every printed command and every stated value reproduced exactly; no defect found.
