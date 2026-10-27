# R59Executor11 — frozen round-58 C1 counter: positive-verdict path is dead

Seat: R59Executor11 (leaf executor, axes: operability). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Task: inspect and run the exact round-58 frozen counter/controls for the positive-verdict-path defect, isolated scratch only, no lane edits.

Status: **complete, two defects isolated and calibrated with positive + negative controls.** No lane file written, no tooling installed, scratch removed.

Frozen inputs are read-only here. `corpus/evidence/round59/claims.md` does **not exist** (at 15:14 and still at 15:26 the directory held only `census-start.txt`, `controls/c1-before.txt`, and — written by another seat at 15:26 — `s101-open.txt`); the round-58 frozen predicate/counter named below is what the task names, and round-58 `claims.md` was read instead. That missing file is recorded as a risk, not worked around.

The round-59 before-receipt `corpus/evidence/round59/controls/c1-before.txt` (958 B) is the **same** frozen counter run without `--controls`: its 16 lines match E1 below minus the two `CONTROL_*` lines, ending `SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0` / `C1=FAIL`. Round 59 is therefore carrying the same frozen bytes, so F1 blocks round-59's positive-path calibration directly, not only round-58's.

## 0. Artifacts and environment (sha256 observed this wave)

| artifact | sha256 |
|---|---|
| `corpus/evidence/round58/c1-count.py` (frozen C1 counter) | `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f` |
| `corpus/evidence/round58/c2-count.py` (contrast) | `dbb859612f9d018296b217baec76a5c6cb744609b7c95372dabae4d6691c8503` |
| `corpus/evidence/round58/controls/build-spans-r55.py` (base pin) | `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` |
| `tools/build-spans.py` (lane base, same bytes as r55 pin) | `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` |
| positive control built in scratch | `c4032f32a0ab55b150b8f8a2d5584e9eaa1b76b5bbf6a5d520ca78ba90e7c647` (7516 B) |

Environment: `Python 3.14.8 (main, Oct 2 2026) [GCC 16.2.1 20260810]`. Every run used `PYTHONDONTWRITEBYTECODE=1` and `python3 -B`; the lane `corpus/evidence/round58/__pycache__` mtimes (14:12–14:27) predate this seat (first command 15:14), and all lane artifact mtimes/hashes are unchanged after the wave.

## 1. Findings

### F1 (decisive, unconditional) — `ref_pass` compares lowercase leg text against an uppercase token, so `C1=PASS` is unreachable

Frozen source, `corpus/evidence/round58/c1-count.py`:

```
51: PASS = "pass"
52: FAIL = "fail"
```

`expect_refuse()` (lines 146–159) returns `f"{name}={PASS}(refused)"`, i.e. `FOREIGN=pass(refused)`. But the aggregation at line 391 asks for the uppercase literal, and the summary at line 399 repeats it:

```
391:    ref_pass = all(("=PASS" in l) for l in ref_legs)
...
399:          f"REFUSE={sum('=PASS' in l for l in ref_legs)}/{len(ref_legs)} "
```

Enumerating every `legs.append` producer (lines 198, 204, 207, 218, 220, 223, 232, 234/236, 250, 263, 265, 278, 280, 295, 306, 315, 317, 323, 333, 345, 360, 378, 381, 382) shows every refusal/safe leg string is built from the lowercase constants or hardcoded lowercase `pass(refused)`. The string `"=PASS"` therefore occurs in **no** leg line; only the final `C1=PASS|FAIL` verdict line uses uppercase. Hence:

```
ref_pass = False  for every possible input
verdict  = "PASS" if (ok_pass and ref_pass and integrity and denied_pass) else "FAIL"
         = "FAIL" always
```

Consequences: (a) no candidate builder, compliant or not, can ever produce the claimed `C1=PASS`/exit 0; (b) the `REFUSE` counters in every receipt read `0/7` by construction, so the observable `SUMMARY ... REFUSE=0/7` never carried the information the receipts implied; (c) the do-nothing-control check is vacuous, because it tests for a target that cannot be emitted (F3).

### F2 (conditional) — expected-span arithmetic uses the span start instead of the quote offset

Frozen source, lines 133 and 138:

```
133:        start = max(0, form.find(quote) - CONTEXT)
138:        span = form[offset:offset + len(quote) + min(CONTEXT, offset) + CONTEXT]
```

`offset` here is the manifest **span start** (`cells[3]`), not the quote offset. With `start = max(0, off-80)` the intended length is `min(80, off) + len(quote) + 80`; the counter computes `min(80, start) + len(quote) + 80`, which drops the leading `off` characters whenever `off < 80`. Any quote located in the first 80 characters of a fixture text makes `EMPTY_OK`/`HELDOUT_OK` fail with `span bytes` even for a correct builder.

The frozen fixture generator can produce exactly that: computing the counter's own `synth_text`/`synth_quotes` for several seeds,

```
seed 7: quote offsets [(1, 3734), (2, 1415), (3, 4074)]  any<80=False
seed 35: quote offsets [(1, 5405), (2, 26), (3, 4077)]  any<80=True
   S502 off=26 start=0 builder_len=122 counter_len=96 MISMATCH
seed 1007: quote offsets [(1, 5595), (2, 844), (3, 9716)]  any<80=False
seed 1:  ... any<80=False
seed 2:  ... any<80=False
seed 3:  ... any<80=False
```

`c2-count.py` does the same computation correctly (`start=max(0,off-80); end=off+len(quote)+80`, line 104–106), which is why C2 does not share this defect; its verdict is also consistently uppercase (`verdict='PASS' if not errors ...`, line 156).

### F3 (secondary, observed) — denial check is vacuous under F1, live only after F1 is fixed

The control loop (line 377) accepts a control only if the nested run prints the literal `C1=PASS`. Under F1 that never happens, so *any* builder passed as a control is reported `denied`, including a fully compliant one (evidence E7). This makes round-58's "controls must not reach C1=PASS" receipts non-discriminating: they would read the same for a perfect builder and for `REFUSEALL`.

Two further dead/weak spots in the frozen counter (no verdict effect observed):
- line 389 assigns `ok_pass` with a convoluted expression that line 390 immediately overwrites (dead code);
- line 122 `want = {"spans.tsv": None, **expected}` is never used (line 128 only interpolates the *word* "want"), so extra `spans/*.txt` files are never compared in safe legs.

## 2. Evidence — exact commands and observed output

All commands run from the lane root; `S=/fast/scratch/hyaku/chousa-r59/R59Executor11/rerun-1540`.

### E1 — replay of the round-58 receipt (frozen counter + lane base builder + lane controls)

```
PYTHONDONTWRITEBYTECODE=1 python3 -B corpus/evidence/round58/c1-count.py \
  --builder tools/build-spans.py \
  --work $S/rep-base --controls corpus/evidence/round58/controls
```

```
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

This is byte-for-byte the round-58 `controls/c1-controls.txt` verdict shape; the base is still destructive (`BEFORE_FOREIGN=deleted`, `SYMLINK_OUT ... target-dir-written!`), so the battery's negative asymmetry is real.

### E2 — frozen counter against a fully compliant builder (seed 7)

```
PYTHONDONTWRITEBYTECODE=1 python3 -B corpus/evidence/round58/c1-count.py \
  --builder $S/build-spans.py --work $S/r-frozen
```

```
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
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

Every named leg passes and `BEFORE_FOREIGN=deleted` holds, yet the verdict is FAIL and the summary still reports `REFUSE=0/7`. This is F1 observed end-to-end.

### E3 — mechanism proof, using the frozen module's own `expect_refuse()` with all seven refusal legs perfect

```python
import importlib.util, types
P = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py"
spec = importlib.util.spec_from_file_location("frozen_c1", P)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
cases = [("FOREIGN", ["FOREIGN", "777"], "REFUSED FOREIGN S777-1.txt"),
         ("SYMLINK_OUT", ["SYMLINK"], "REFUSED SYMLINK out"),
         ("SYMLINK_CACHE", ["SYMLINK"], "REFUSED SYMLINK cache"),
         ("FIFO_TXT", ["NOT_REGULAR", "FIFO"], "REFUSED NOT_REGULAR FIFO"),
         ("DEVZERO_TXT", ["NOT_REGULAR", "SIZE"], "REFUSED NOT_REGULAR SIZE"),
         ("FAT_RAW", ["SIZE"], "REFUSED SIZE 83886080>67108864"),
         ("MANY_QUOTES", ["SIZE", "ROWS", "CAP"], "REFUSED QUOTES_ROWS_CAP")]
legs = [m.expect_refuse(n, types.SimpleNamespace(returncode=1, stderr=msg+"\n", stdout=""), cls, [])
        for n, cls, msg in cases]
for l in legs: print("leg:", l)
print("all seven legs pass? ", all("=pass" in l for l in legs))
print("frozen ref_pass        =", all(("=PASS" in l) for l in legs))       # line 391 verbatim
print("frozen summary REFUSE  =", sum('=PASS' in l for l in legs), "/", len(legs))  # line 399 verbatim
print("frozen verdict         =", "PASS" if (all("=pass" in l for l in legs) and all(("=PASS" in l) for l in legs)) else "FAIL")
```

```
leg: FOREIGN=pass(refused)
leg: SYMLINK_OUT=pass(refused)
leg: SYMLINK_CACHE=pass(refused)
leg: FIFO_TXT=pass(refused)
leg: DEVZERO_TXT=pass(refused)
leg: FAT_RAW=pass(refused)
leg: MANY_QUOTES=pass(refused)
all seven legs pass?  True
frozen ref_pass        = False
frozen summary REFUSE  = 0 / 7
frozen verdict         = FAIL
```

### E4 — F1 fixed (two tokens) and nothing else: compliant builder now certifies

Scratch copy of the frozen counter, sha256 `21dae5d327157654ca679eb848b4c7d172643e2cf77e0e6180e454fa24e7eeba` (exactly `"=PASS"` → `"=pass"` at lines 391 and 399), with genuine controls:

```
PYTHONDONTWRITEBYTECODE=1 python3 -B $S/calib3/c1-count.py \
  --builder $S/build-spans.py --work $S/calib3/run-genuine --controls $S/calib3/controls
```

```
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
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=PASS
EXIT=0
```

The same two-token fix does **not** loosen the base: fixed counter + `tools/build-spans.py` → `SUMMARY OK=4/4 REFUSE=0/7`, `C1=FAIL`, exit 1.

### E5 — F2 isolated: F1-fixed counter, compliant builder, seed 35

```
PYTHONDONTWRITEBYTECODE=1 python3 -B $S/calib3/c1-count.py \
  --builder $S/build-spans.py --work $S/calib3/run-s35 --seed 35
```

```
EMPTY_OK=fail(spans/S502-1.txt span bytes)
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
DENIED=0/0
SUMMARY OK=3/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

`S502` sits at char offset 26 in the seed-35 fixture; the manifest offset is `0`, so line 138 computes a 96-char expectation against the builder's 122-char span (E9 table).

### E6 — F1+F2 fixed: positive path is live and seed-robust

Scratch copy sha256 `a3aa542b06098193a1e28844967249d2f7919f4c957bd8d3929e9d0695743414` (E4's two tokens plus line 138 → `span = form[offset:form.find(quote) + len(quote) + CONTEXT]`), compliant builder:

- seed 35 → `SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0`, `C1=PASS`, `EXIT=0`
- seed 7 → `SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0`, `C1=PASS`, `EXIT=0`
- seed 2 → `SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0`, `C1=PASS`, `EXIT=0`
- the same fixed counter with `tools/build-spans.py` still yields `SUMMARY OK=4/4 REFUSE=0/7`, `C1=FAIL`, `EXIT=1`

### E7 — denial check is vacuous under F1 (compliant builder passed *as* a control)

```
PYTHONDONTWRITEBYTECODE=1 python3 -B corpus/evidence/round58/c1-count.py \
  --builder $S/build-spans.py --work $S/rep-vac --controls $S/controls-vacuous
# controls-vacuous/REFUSEALL.py = lane REFUSEALL.py
# controls-vacuous/build-spans-r55.py = the compliant control builder (sha c4032f32…)
```

```
BEFORE_FOREIGN=deleted
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
EXIT=1
```

### E8 — after F1+F2 are fixed, the same control is correctly detected

```
PYTHONDONTWRITEBYTECODE=1 python3 -B $S/calib3/c1-count.py \
  --builder $S/build-spans.py --work $S/calib3/run-misuse --controls $S/controls-vacuous
```

```
BEFORE_FOREIGN=deleted
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=PASS(!)
DENIED=1/2
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=1/2
C1=FAIL
EXIT=1
```

Methodological caveat: when the fixes are applied *in memory* (`exec(compile(src…))` with `__file__` = lane path), nested control runs re-execute the frozen file, so they still report `denied`; E8 uses a real patched file copy (`$S/calib3/c1-count.py`).

## 3. Calibration matrix (all observed)

| counter bytes | builder | seed | legs | verdict |
|---|---|---|---|---|
| frozen 65da18… | lane base `tools/build-spans.py` | 7 | 4/4 safe, 0/7 refuse | `C1=FAIL`, exit 1 |
| frozen 65da18… | compliant control c4032f3… | 7 | 4/4 safe, 7/7 refuse (`=pass(refused)`) | `C1=FAIL`, exit 1 |
| frozen 65da18… | compliant control, as control | 7 | − | both controls `denied`, `C1=FAIL` |
| F1-fixed 21dae5… | compliant control | 7 | 4/4, 7/7 | **`C1=PASS`**, exit 0 |
| F1-fixed 21dae5… | compliant control | 35 | 3/4, 7/7 | `C1=FAIL` (F2) |
| F1-fixed 21dae5… | lane base | 7 | 4/4, 0/7 | `C1=FAIL` |
| F1+F2-fixed a3aa54… | compliant control | 7 / 35 / 2 | 4/4, 7/7 | **`C1=PASS`**, exit 0 |
| F1+F2-fixed a3aa54… | lane base | 7 | 4/4, 0/7 | `C1=FAIL` |
| F1+F2-fixed a3aa54… | compliant control, as control | 7 | − | `CONTROL_…=PASS(!)`, `DENIED=1/2`, `C1=FAIL` |

## 4. Operability reading (axis: operability, lowest scored 3/10)

- The round-58 C1 predicate as frozen is **equivalent to a constant FAIL**. It cannot certify the hardening it describes, and the only positive-direction evidence the wave could ever produce is absent by construction. Any round-59 "positive verdict path" claim derived from `c1-count.py` is unsupported until F1 is fixed.
- The negative direction still works and is still discriminating: `BEFORE_FOREIGN=deleted` on the pinned r55/base builder, and the seven base-leg failures, reproduce exactly (E1). Round-58 receipts remain valid *as before-receipts*; they were never valid as target receipts.
- The counter's own summary is the tell: `REFUSE=0/7` next to seven `=pass(refused)` lines (E2). Receipts should never be accepted as positive evidence without `REFUSE=7/7`.
- Seed robustness is part of operability: the frozen fixture can place a quote inside the first 80 characters (seed 35), which F2 turns into a false failure of a correct builder.
- Fix scope, calibrated but **not applied** (lane is read-only for this seat): line 391 and 399 token case; line 138 span end; optionally drop the dead line-389 assignment and use the unused `want` (line 122) or delete it.

## 5. Cross-check that did not reproduce a second defect

`c2-count.py` (depth claim, not my axis) was inspected for the same two patterns: it uses `start=max(0,off-80); end=off+len(quote)+80` (lines 104–106) and a single uppercase `verdict` (line 156), so neither F1 nor F2 applies there. Its current base run is FAIL for the documented reason (no entry), which is consistent with `controls/c2-before-frozen.txt`. I did not re-run C2.

## 6. Risks / anomalies

1. **Scratch namespace is being crossed.** A copied frozen counter inside `/fast/scratch/hyaku/chousa-r59/R59Executor11/patched/` was rewritten between 15:18 and 15:19 with exactly the F1 two-token patch (hash `21dae5d3…`, i.e. my own later calibration bytes), and the entire `R59Executor11/` root was then deleted externally around 15:25. Separately, `R59Executor07-2` reports a C2 poison probe it did not create inside its namespace. Mitigation used here: every decisive run re-created its scratch inputs immediately before use, verified the frozen source hash inside the run, and staged copies under freshly named subdirectories. Lane artifacts were verified untouched after every batch (hashes and mtimes above).
2. **Concurrency.** >20 sibling seats were running the same battery simultaneously (`ps` showed `R59Executor01/04/05/06/07/09/10/13/14`, `R59Scribe17`), so wall times in receipts are unreliable and nested-control timing varies; none of the claims above depend on timing.
3. **Missing frozen claims file.** `corpus/evidence/round59/claims.md` is absent; this report binds to round-58 `claims.md` + the named counter. If round-59 claims land later and differ, the F1/F2 evidence still applies to the frozen artifact at the pinned hash.
4. No installs, no `pacman`, no git/jj/index writes, no lane edits, no live fetches.

## 7. Files changed

- `.ufo/waves/round-59/w1/R59Executor11.md` (this report) — only file written.
- Scratch `/fast/scratch/hyaku/chousa-r59/R59Executor11/` removed before yield.

## Appendix A — positive control source (scratch, sha256 `c4032f32…`; reproduce as `--builder`)

```python
#!/usr/bin/env python3
"""build-spans — POSITIVE CONTROL for round-59 calibration (scratch only)."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import os
import pathlib
import re
import stat
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
CONTEXT = 80
SIZE_CAP = 64 * 1024 * 1024
ROWS_CAP = 100_000
IN_HEADER = ["id", "url", "quote", "entry"]
OUT_HEADER = "id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry"
ID_RE = re.compile(r"^S\d{3}$")
SPAN_RE = re.compile(r"^S\d{3}-\d+\.txt$")
OLE = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
ZIP = b"PK\x03\x04"


def die(code: int, msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(code)


def key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def regular_or_absent(path: pathlib.Path, label: str):
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        return None
    if stat.S_ISLNK(st.st_mode):
        die(3, f"build-spans: REFUSED SYMLINK {label} {path}")
    if not stat.S_ISREG(st.st_mode):
        die(3, f"build-spans: REFUSED NOT_REGULAR {label} {path}")
    if st.st_size > SIZE_CAP:
        die(3, f"build-spans: REFUSED SIZE {label} {path} {st.st_size}>{SIZE_CAP}")
    return st


def _capture_text():
    spec = importlib.util.spec_from_file_location("capture_text", LANE / "tools" / "capture-text.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Forms:
    def __init__(self, cache: pathlib.Path):
        self.cache, self.ct, self.memo = cache, None, {}

    def get(self, url: str):
        if url in self.memo:
            return self.memo[url]
        raw, txt = self.cache / f"{key(url)}.raw", self.cache / f"{key(url)}.txt"
        regular_or_absent(raw, "cache raw")
        regular_or_absent(txt, "cache txt")
        res = (None, "", "")
        head = b""
        if raw.exists():
            with raw.open("rb") as f:
                head = f.read(8)
        if head[:8] == OLE or head[:4] == ZIP:
            if self.ct is None:
                self.ct = _capture_text()
            b = raw.read_bytes()
            try:
                res = (self.ct.text_form(str(raw)), hashlib.sha256(b).hexdigest(), raw.name)
            except Exception as e:
                res = (None, "", f"capture-text refused {raw.name}: {str(e)[:120]}")
        elif txt.exists():
            b = txt.read_bytes()
            res = (b.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n"),
                   hashlib.sha256(b).hexdigest(), txt.name)
        else:
            res = (None, "", f"no defined text form for {key(url)} (raw neither OLE nor zip, no .txt)")
        self.memo[url] = res
        return res


def read_quotes(path: pathlib.Path):
    st = regular_or_absent(path, "quotes")
    if st is None:
        die(2, f"build-spans: no input {path}")
    if st.st_size > SIZE_CAP:
        die(3, f"build-spans: REFUSED SIZE quotes {path} {st.st_size}>{SIZE_CAP}")
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].split("\t") != IN_HEADER:
        die(2, f"build-spans: {path} header must be {' '.join(IN_HEADER)} (tab-separated)")
    data = [line for line in lines[1:] if line.strip()]
    if len(data) > ROWS_CAP:
        die(3, f"build-spans: REFUSED QUOTES_ROWS_CAP {len(data)}>{ROWS_CAP} in {path}")
    rows, bad, url_of = [], [], {}
    for n, line in enumerate(data, start=2):
        cells = line.split("\t")
        if len(cells) != 4 or not all(c.strip() for c in cells):
            bad.append(f"line {n}: need 4 non-empty tab cells, got {len(cells)}")
            continue
        sid, url, quote, entry = (c.strip() for c in cells)
        if not ID_RE.match(sid):
            bad.append(f"line {n}: id {sid!r} is not S###")
        elif url_of.setdefault(sid, url) != url:
            bad.append(f"line {n}: {sid} names {url}, earlier rows name {url_of[sid]}")
        elif entry.startswith("/") or ".." in pathlib.PurePath(entry).parts:
            bad.append(f"line {n}: entry {entry!r} must be lane-relative")
        else:
            rows.append((sid, url, quote, entry))
    if bad:
        for b in bad:
            print(f"build-spans: {path} {b}", file=sys.stderr)
        sys.exit(2)
    return rows


def build(rows, forms: Forms):
    lines, files, chars, refused = [OUT_HEADER], {}, [], []
    seen = {}
    for sid, url, quote, entry in rows:
        text, digest, why = forms.get(url)
        if text is None:
            refused.append(f"{sid}: {why}")
            continue
        n = text.count(quote)
        if n != 1:
            refused.append(f"{sid}: quote occurs {n}x in {why}: {quote[:60]!r}")
            continue
        off = text.find(quote)
        seen[sid] = seen.get(sid, 0) + 1
        name = f"spans/{sid}-{seen[sid]}.txt"
        start = max(0, off - CONTEXT)
        span = text[start:off + len(quote) + CONTEXT]
        if span == quote:
            refused.append(f"{sid}: {why} holds no context around {quote[:60]!r}")
            continue
        files[name] = span
        chars.append(off)
        lines.append("\t".join([sid, url, digest, str(start), name, quote, entry]))
    if refused:
        for r in refused:
            print(f"build-spans: refused {r}", file=sys.stderr)
        sys.exit(1)
    return lines, files, chars


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--quotes", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cache", required=True)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    out, cache = pathlib.Path(a.out), pathlib.Path(a.cache)
    if os.path.islink(out):
        die(3, f"build-spans: REFUSED SYMLINK out {out}")
    if os.path.islink(cache):
        die(3, f"build-spans: REFUSED SYMLINK cache {cache}")
    if not cache.is_dir():
        die(2, f"build-spans: no capture cache {cache}")
    sd = out / "spans"
    if os.path.islink(sd):
        die(3, f"build-spans: REFUSED SYMLINK out {sd}")

    rows = read_quotes(pathlib.Path(a.quotes))
    lines, files, chars = build(rows, Forms(cache))

    orphans = []
    if sd.is_dir():
        for p in sorted(sd.iterdir()):
            if os.path.islink(p):
                die(3, f"build-spans: REFUSED SYMLINK out {p}")
            if SPAN_RE.match(p.name) and f"spans/{p.name}" not in files:
                orphans.append(p.name)
    if orphans:
        die(4, "build-spans: REFUSED FOREIGN span files preserved (no orphan deletion): "
            + ", ".join(orphans))

    sd.mkdir(parents=True, exist_ok=True)
    (out / "spans.tsv").write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    for name, body in files.items():
        (out / name).write_bytes(body.encode("utf-8"))
    for line, c in zip(lines[1:], chars):
        cells = line.split("\t")
        print(f"QUOTE {cells[0]} char {c} {cells[4]}")
    print(f"SPANS_ROWS={len(files)} WRITTEN={len(files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## Appendix B — in-memory variant driver (frozen bytes verified, two/three tokens replaced)

```python
import hashlib, pathlib, sys
P = "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py"
SRC = pathlib.Path(P).read_text(encoding="utf-8")
assert hashlib.sha256(SRC.encode()).hexdigest() == \
    "65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f"
src = SRC
src = src.replace('ref_pass = all(("=PASS" in l) for l in ref_legs)',          # F1
                  'ref_pass = all(("=pass" in l) for l in ref_legs)')
src = src.replace("sum('=PASS' in l for l in ref_legs)",                      # F1
                  "sum('=pass' in l for l in ref_legs)")
src = src.replace("span = form[offset:offset + len(quote) + min(CONTEXT, offset) + CONTEXT]",  # F2
                  "span = form[offset:form.find(quote) + len(quote) + CONTEXT]")
sys.argv = [P, "--builder", BUILDER, "--work", WORK, "--seed", SEED]
try:
    exec(compile(src, P, "exec"), {"__name__": "__main__", "__file__": P})
except SystemExit as e:
    print(f"EXIT={e.code}")
```

Caveat: with `__file__` pinned to the lane path, nested `--controls` runs execute the frozen file; control-liveness results (E8) were produced with a real patched copy (`calib3/c1-count.py`, sha256 `a3aa542b…`).

Report: .ufo/waves/round-59/w1/R59Executor11.md
