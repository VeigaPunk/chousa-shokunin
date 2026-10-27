# R59Executor13 — round-58 C1 counter, positive-verdict path (isolated reproduction)

Role: leaf executor, axis **operability**. Assignment: *in isolated scratch only, inspect and run the exact round58 frozen counter/tool or controls relevant to the positive-verdict-path defect; report exact command/output; never edit lane files.*

Result: reproduced the defect end to end and calibrated it. The frozen `corpus/evidence/round58/c1-count.py` **cannot print `C1=PASS` for any builder**, while a one-token copy can; with that copy, the same battery still rejects the base builder and still kills a positive control. All runs are scratch-only; the lane was read, never written.

## 0. Inputs (byte pins, copied read-only into scratch)

```
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  bin/build-spans-base.py   (= lane tools/build-spans.py, round-55 pin)
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  bin/controls/build-spans-r55.py
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  bin/capture-text.py
65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f  bin/c1-count.py            (frozen round-58 counter, unmodified)
6b6000ed83f25e9c8ddbe757624da9a3f085834a5d9b7609d14f4013c95d3a46  bin/c1-count-fixed.py      (scratch copy, 1 line changed — §4)
e7721cefe050ee435d3bab811ed65933d26a865ca30340feaab3f9388c3572fb  bin/controls/REFUSEALL.py
```
Scratch root: `/fast/scratch/hyaku/chousa-r59/R59Executor13` (Python 3.14.8, freezer `/fast`).
Installs/updates: none. No pacman, no git/jj write, no fetch.

## 1. Scratch portability fact (affects the measurement)

`tools/build-spans.py` imports its decoder from **its own directory** (`TOOLS = Path(__file__).resolve().parent`, `build-spans.py:41,56-59`). A scratch copy of the builder without a sibling `capture-text.py` makes two legs fail for the wrong reason. Observed on the first base run:

```
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'Traceback (most recent call last):\n  File ".../bin/build-spans-base.py", line 217, in <module>\n    sys.exit(main())\n   ')
HELDOUT_OK=fail(rc=1 )
SUMMARY OK=3/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
```
with the captured cause `FileNotFoundError: [Errno 2] No such file or directory: '.../bin/capture-text.py'`.
With `capture-text.py` copied beside the builder, both legs behave as the round-58 receipt (`FAT_RAW` reaches capture-text and is refused as `ole-malformed`; `HELDOUT_OK=pass`). Any off-lane replay of this battery must copy the decoder too, else the battery mis-attributes two legs.

## 2. Baseline: frozen counter vs the base builder (reproduces the frozen before-receipt)

```
$ cd /fast/scratch/hyaku/chousa-r59/R59Executor13/work
$ python3 /fast/scratch/hyaku/chousa-r59/R59Executor13/bin/c1-count.py \
    --builder /fast/scratch/hyaku/chousa-r59/R59Executor13/bin/build-spans-base.py \
    --work /fast/scratch/hyaku/chousa-r59/R59Executor13/work/base2 \
    --controls /fast/scratch/hyaku/chousa-r59/R59Executor13/bin/controls
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: no defined text form for f4088c6d6da1f4763182a51d (raw neither OLE nor zip, no .txt)\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused S581: no defined text form for a172f04219497476db868414 (raw neither OLE nor zip, no .txt)\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused S551: capture-text refused f96cbd6d82dbae8a8e2c6223.raw: ole-malformed: sector shift 0, mini shift 0\n')
MANY_QUOTES=fail(rc=0, expected refusal)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
EXIT=1
```
Line-for-line identical to `corpus/evidence/round58/controls/c1-controls.txt` (70.6 s). So the frozen before-state is reproducible and the base builder is genuinely unhardened.

## 3. Positive path: every leg passes, verdict is still FAIL

A scratch candidate `build-spans-hardened.py` guards the frozen hazard classes (lstat kind/size before read, `--out` symlink, unexpected file in `out/spans/` before orphan deletion, quote-row cap, `..` entry) and then `execv`s the byte-identical base builder to produce spans, so the safe legs are satisfied by the real span logic, not faked:

```
$ python3 /fast/scratch/hyaku/chousa-r59/R59Executor13/bin/c1-count.py \
    --builder /fast/scratch/hyaku/chousa-r59/R59Executor13/bin/build-spans-hardened.py \
    --work /fast/scratch/hyaku/chousa-r59/R59Executor13/work/hardened \
    --controls /fast/scratch/hyaku/chousa-r59/R59Executor13/bin/controls
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=pass(refused)
SYMLINK_OUT=pass(refused)
SYMLINK_CACHE=pass(refused)
FIFO_TXT=pass(refused)
DEVZERO_TXT=pass(refused)
FAT_RAW=pass(refused)
MANY_QUOTES=pass(refused)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
EXIT=1
```
11/11 legs satisfied, integrity leg satisfied, both controls denied — and the aggregate still reports `REFUSE=0/7` and `C1=FAIL`. This is the defect: the frozen predicate's positive branch is **unreachable**, not merely unmet.

## 4. Localization (frozen bytes, `65da18bb…`)

```
51:PASS = "pass"
52:FAIL = "fail"
160:    return f"{name}={PASS}(refused)"                       # every refusal leg emits lowercase "=pass"
384-388: ok_legs / ref_legs selected by exact leg names, split on "="
389: ok_pass = all(l.endswith("(pass)") or ... "=pass" in l for l in ok_legs)   # dead: overwritten by 390
390: ok_pass = all(("=pass" in l) for l in ok_legs)
391: ref_pass = all(("=PASS" in l) for l in ref_legs)          # uppercase token: never matches
394: verdict = "PASS" if (ok_pass and ref_pass and integrity and denied_pass) else "FAIL"
399: REFUSE={sum('=PASS' in l for l in ref_legs)}/{len(ref_legs)}   # same uppercase token in the SUMMARY
```
Emitter probe (imports the frozen module, calls its own `expect_refuse` on a proc that refuses):

```
PASS constant      = 'pass'
FAIL constant      = 'fail'
expect_refuse leg  = 'SYMLINK_OUT=pass(refused)'
ref_pass token hit = False | lowercase token hit = True
```
`ref_legs` is never empty on this path (all seven legs are appended unconditionally), so `ref_pass` is `False` on every run: `C1=PASS` and exit 0 are dead code for all builders. A second, non-fatal form of the same token bug makes the SUMMARY print `REFUSE=0/7` even when seven refusals were measured (§5).

## 5. Falsification controls (one token; no other change)

Scratch copy, exactly one line changed:
```
$ diff -u bin/c1-count.py bin/c1-count-fixed.py
@@ -388,7 +388,7 @@
-    ref_pass = all(("=PASS" in l) for l in ref_legs)
+    ref_pass = all(("=pass" in l) for l in ref_legs)
```
(a) hardened candidate → positive path reachable:
```
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=PASS
EXIT=0
```
(all 11 leg lines as in §3; the SUMMARY's `REFUSE=0/7` is the line-399 artifact and does not enter the verdict.)
(b) base builder → discrimination kept:
```
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
... (all seven refusal legs fail as in §2)
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
EXIT=1
```
(c) control gate. A **positive control** was built by installing the 11/11 candidate as `REFUSEALL.py` (with its base builder + decoder siblings, since the wrapper resolves them relative to itself). Placed in a self-consistent counter directory (`c1-count.py` = fixed bytes, so the recursion's `HERE/"c1-count.py"` child is the same logic):
```
# frozen bytes + positive control
CONTROL_REFUSEALL=denied
DENIED=1/1
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=1/1
C1=FAIL

# one-token copy + positive control
CONTROL_REFUSEALL=PASS(!)
DENIED=0/1
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/1
C1=FAIL
```
Under frozen bytes a builder that satisfies every leg is recorded **`denied`**, i.e. indistinguishable from `REFUSEALL`: the control gate's readout is vacuous in the same way as the verdict. After the token fix the gate is live and correctly refuses (`DENIED=0/1`, `C1=FAIL`).

(d) recursion path sensitivity, observed: the counter re-invokes `HERE/"c1-count.py"` (`c1-count.py:366,372`), not its own path. A renamed copy (`bin/c1-count-fixed.py`) therefore judges control children with the **frozen** logic and reports `CONTROL_REFUSEALL=denied` even when the child passes — the fix only takes effect where the counter occupies its own filename (or the recursion is changed). A lane repair must replace the path, not merely add a copy.

## 6. Adjacent read-only check (not my claim surface)

`python3 corpus/evidence/round58/c2-count.py --root <lane> --work <scratch>/c2-base` → `ENTRIES=0/1 BOUND=0/1 REF_ID_UNBOUND=1 QUOTE_ROWS=0/12 … ERROR S101_NOT_IN_SOURCE … C2=FAIL`, `EXIT=1`, matching `corpus/evidence/round58/controls/c2-before.txt`. The C2 positive path was not probed here; `SCORECARD.md:2916` records a separate `unprovable` (span-start/occurrence-offset contradiction) that this run does not measure.

## 7. Calibration verdict for round 59

- The round-58 C1 target (`C1=PASS` on a hardened builder) is not "unmet by the candidate": it is **unmeasurable as frozen**. Observed the exact failure mode, not just its receipt: 11/11 legs pass and the aggregate still fails.
- The defect is one token on the verdict line (plus the same token on the SUMMARY line, and a dead duplicate `ok_pass` assignment at line 389). A one-token change makes the positive path reachable (`C1=PASS`, exit 0) without weakening discrimination (base still `C1=FAIL`, exit 1).
- Any round-59 positive-verdict calibration must include a **positive control** — a builder that satisfies every leg — and must show the counter either admits it (candidate path) or flags it as `PASS(!)` (control path). The frozen bytes cannot do either: both a passing builder and `REFUSEALL` read `denied`.
- No numeric score claim is made here; `SCORECARD.md:2908,2915` already records round-58 C1 as `unprovable`, and this run supplies the independent positive-side reproduction.

## 8. Risks / limits

- The hardened candidate is a scratch guard-and-delegate wrapper over the byte-identical round-55 builder, not a proposed lane patch, and it is not a hardened `tools/build-spans.py`. It validates the *counter* (does the battery admit a builder that meets its written legs), not the lane tool's security.
- `expect_refuse` scores refusals by a lowercase substring of combined stdout/stderr plus nonzero exit; the battery therefore admits any builder that refuses each hazard with the right word. This readout was not attacked here (forgeability is a separate axis, historically covered by rounds 50-52).
- Safe legs were produced by the real builder, so the positive run is a genuine 11/11; the wrapper's guards are what supply the refusal reasons.
- No lane file, frozen counter, claim, or counter byte was modified; no install.
- Scratch lifecycle: all measurements finished at 15:21–15:22 local; at ~15:23 the whole `/fast/scratch/hyaku/chousa-r59/R59Executor13` tree was removed/churned by another process (dirs `w-controls`, `w-controls-cand` appeared under my path between two listings, then the tree vanished). That was not my cleanup and not my write. Nothing in this report depends on scratch surviving: every command, output line and digest above was transcribed from the completed runs, and §9 reproduces the two non-frozen scratch artifacts from text.

## 9. Reproduction of the non-frozen artifacts

Frozen inputs are lane files (pins in §0). The two scratch-only artifacts are given verbatim so a later round can rebuild them without my scratch.

(a) One-token counter copy:
```
cp corpus/evidence/round58/c1-count.py <work>/c1-count.py
python3 - <<'PY' <work>
import pathlib,sys
p=pathlib.Path(sys.argv[1])/'c1-count.py'; b=p.read_bytes()
old=b'ref_pass = all(("=PASS" in l) for l in ref_legs)'; new=b'ref_pass = all(("=pass" in l) for l in ref_legs)'
assert b.count(old)==1; p.write_bytes(b.replace(old,new))
PY
```
Keep `controls/REFUSEALL.py` and `controls/build-spans-r55.py` beside it (`HERE/controls`), since the counter resolves the pinned round-55 builder there.

(b) Hardened candidate `build-spans-hardened.py`, placed in a directory that also holds byte-identical copies of `tools/build-spans.py` as `build-spans-base.py` and `tools/capture-text.py` (the builder imports its decoder from its own directory):
```
#!/usr/bin/env python3
"""Scratch-only hardened candidate for the round-58 C1 battery: guard the frozen
hazard classes, then delegate to the byte-identical round-55 base builder."""
import hashlib, os, stat, sys
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build-spans-base.py")
SIZE_CAP = 64 * 1024 * 1024
ROWS_CAP = 100_000

def die(msg):
    print("build-spans: refused " + msg, file=sys.stderr); raise SystemExit(1)

def main():
    argv = sys.argv[1:]; opt = {}; i = 0
    while i < len(argv):
        if argv[i] in ("--quotes", "--out", "--cache") and i + 1 < len(argv):
            opt[argv[i]] = argv[i + 1]; i += 2
        else:
            i += 1
    quotes, out, cache = opt.get("--quotes"), opt.get("--out"), opt.get("--cache")
    if not (quotes and out and cache):
        os.execv(sys.executable, [sys.executable, "-B", BASE] + argv)
    rows = []
    with open(quotes, encoding="utf-8") as f:
        f.readline()
        for line in f:
            if line.strip():
                rows.append(line.rstrip("\n").split("\t"))
                if len(rows) > ROWS_CAP:
                    die(f"quotes.tsv rows exceed cap {ROWS_CAP} (ROWS)")
    if os.path.islink(out):
        die("SYMLINK output path " + out)
    per, expected = {}, set()
    for cells in rows:
        if len(cells) < 4: die("malformed quotes row")
        sid = cells[0]; per[sid] = per.get(sid, 0) + 1
        expected.add(f"{sid}-{per[sid]}.txt")
    spans_dir = os.path.join(out, "spans")
    if os.path.isdir(spans_dir) and not os.path.islink(spans_dir):
        for name in os.listdir(spans_dir):
            if name not in expected:
                die(f"FOREIGN file {name} present in spans/ (refusing before orphan deletion)")
    for cells in rows:
        sid, url, entry = cells[0], cells[1], cells[3]
        if ".." in entry: die(f"ESCAPE entry {entry} for {sid}")
        key = hashlib.sha256(url.encode()).hexdigest()[:24]
        for ext in (".raw", ".txt"):
            p = os.path.join(cache, key + ext)
            try: st = os.lstat(p)
            except FileNotFoundError: continue
            if stat.S_ISLNK(st.st_mode): die("SYMLINK cache input " + key + ext)
            if not stat.S_ISREG(st.st_mode): die("NOT_REGULAR cache input " + key + ext)
            if st.st_size > SIZE_CAP:
                die(f"SIZE cap {SIZE_CAP} exceeded by {key}{ext} ({st.st_size} bytes)")
    os.execv(sys.executable, [sys.executable, "-B", BASE] + argv)

if __name__ == "__main__":
    main()
```
For the positive control of §5(c), install this file as `REFUSEALL.py` together with both sibling files in the control directory.

## Report

`.ufo/waves/round-59/w1/R59Executor13.md`
