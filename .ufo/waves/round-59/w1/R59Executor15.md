# R59Executor15 — positive-verdict-path calibration against the round-58 frozen C1 counter

- Seat: R59Executor15 (leaf executor, operability axis). No spawns, no lane edits, no git/jj/index writes.
- Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin` (all lane bytes read-only).
- Scratch: `/fast/scratch/hyaku/chousa-r59/R59Executor15/x15` (removed at yield; every work root below is under it).
- Subject bytes: `corpus/evidence/round58/c1-count.py`, sha256 `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f` (unchanged since the round-58 freeze); pinned r55 builder `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`; `tools/capture-text.py` `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`.

## 0. Handoff state read before work

- **Round-59 frozen claims do not exist.** `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round59/claims.md` → `ENOENT` (read attempted first, per the wave item). `corpus/evidence/round59/` holds only `census-start.txt` and `controls/c1-before.txt`; `predata/` is absent.
- `corpus/evidence/round59/controls/c1-before.txt` sha256 `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe` is **byte-identical** to `corpus/evidence/round58/controls/c1-before.txt`. Round-59's "before" receipt is round-58's, unchanged.
- No round-59 counter/tool exists, so the only frozen predicate available is round-58's C1 counter. All runs below use its exact bytes (a namespaced byte-copy), plus one clearly-labelled scratch token-fix copy for calibration only.
- `tools/build-spans.py` sha256 `1ed2650a…c80bf6` is **byte-identical to the pinned r55 "BEFORE" control** `corpus/evidence/round58/controls/build-spans-r55.py`. The lane surface still holds the unhardened builder; round-58's C1 target never landed (`c1-measure-after.txt` absent from `corpus/evidence/round58/`, which contains only `census-start.txt`, `census-end.txt`, `s101-open.txt`; `c2-measure-after.txt` also absent).

## 1. Defect confirmed: `C1=PASS` is dead code for every builder

Token sites in the frozen counter:

| line | bytes | effect |
|---|---|---|
| `:51` | `PASS = "pass"` | lowercase credit token |
| `:160` | `return f"{name}={PASS}(refused)"` | refusal legs emit `=pass(refused)` |
| `:223` | `legs.append(f"FOREIGN={PASS}(refused)" …)` | lowercase |
| `:234` | `legs[-1] = f"SYMLINK_OUT={PASS}(refused)"` | lowercase |
| `:391` | `ref_pass = all(("=PASS" in l) for l in ref_legs)` | matches **uppercase** |
| `:399` | `REFUSE={sum('=PASS' in l for l in ref_legs)}` | matches **uppercase** |
| `:394`, `:402` | `verdict = "PASS" if (ok_pass and ref_pass …)` / `return 0 if verdict == "PASS" else 1` | verdict and exit are gated on `ref_pass` |

`ref_pass` is therefore a constant `False`; the verdict is a constant `FAIL` and the exit a constant `1`, whatever the builder does. `:389` is also a dead assignment immediately overwritten by `:390`.

### Command A — frozen counter, fully conforming pass-side control (see §2)

```
cd /fast/scratch/hyaku/chousa-r59/R59Executor15/x15
python3 -B ev/round58/c1-count.py --builder lane/tools/refbuilder.py \
        --work /fast/scratch/hyaku/chousa-r59/R59Executor15/x15/runs/A-frozen-ref
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

Eleven legs print the credit token, integrity holds, controls are vacuous here (`DENIED=0/0`), and the verdict is still `FAIL`. This is the round-58 `C1=PASS` unreachability reproduced on the exact frozen bytes in isolated scratch, independent of builder quality. It agrees with the round-58 reports already on the lane: `.ufo/waves/round-58/w1/R58SentinelCounterScope.md` (F1, critical/blocking) and `.ufo/waves/round-58/w1/R58ExecC1PathContainment.md` (HIGH item 1). No novelty is claimed for the token diagnosis; the contribution here is the **pass-side calibration** and the falsifiers in §2–§5.

## 2. Pass-side control used for calibration (scratch only, not a lane artifact)

`lane/tools/refbuilder.py` (sha256 `8297447e2923d0f0359e6cc919e0553a650460d63535cd743c471f12f8982121`, source in Appendix A) implements exactly the behaviours the counter checks, using the span slicing documented by `tools/build-spans.py` (`form[max(0, off-80) : off+len(quote)+80]`): symlink/FIFO/device capture refusal, 64 MiB raw cap, 100 000-row cap, `..` entry refusal, foreign-span refusal before orphan deletion, symlink `--out` refusal, digest/offset/span exactness, byte-identical rebuild. Environment variable `X15_GUARDS` selects guards so each guard can be dropped as a mutant without editing the file.

### Command C — single-token-fixed counter (`:391` and `:399` `"=PASS"` → `"=pass"`, nothing else changed; scratch copy sha256 `21dae5d327157654ca679eb848b4c7d172643e2cf77e0e6180e454fa24e7eeba`), conforming control, with the declared do-nothing controls

```
python3 -B ev/round58/c1-count-tokenfix.py --builder lane/tools/refbuilder.py \
        --work /fast/scratch/hyaku/chousa-r59/R59Executor15/x15/runs/C-tokenfix-ref \
        --controls ev/round58/controls
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

Seed robustness of that positive verdict (`--seed` sweep, same builder, `runs/S-seed`):

```
TOKENFIX+refbuilder seeds1-30: PASS=30 FAIL=0
seed 1007 (the seed the counter's own nested controls use): C1=PASS, REFUSE=7/7, exit 0
```

So the positive branch is reachable and total for the default fixture family **once the single token at `:391`/`:399` is normalised**; no other counter change was needed.

## 3. Falsifiers — the fixed positive verdict is not vacuous

Each row drops exactly one behaviour from the conforming control (or swaps the subject builder); all runs use the token-fixed counter.

| # | subject | command discriminator | observed |
|---|---|---|---|
| D | lane `tools/build-spans.py` (sha `1ed2650a…`, unhardened) | `--builder lane/tools/build-spans.py` | `SUMMARY OK=4/4 REFUSE=0/7 … C1=FAIL`, EXIT=1 |
| E | control with foreign guard removed | `X15_GUARDS=symlink_out,capture_type,size,rows,escape` | `FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)`, `REFUSE=6/7`, `C1=FAIL`, EXIT=1 |
| H | control with 64 MiB raw cap removed | `X15_GUARDS=foreign,symlink_out,capture_type,rows,escape` | `FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused capture-text refused f96cbd6d82dbae8a8e2c6223.raw: ole-malformed: sector shift 0, mini shift 0')`, `REFUSE=6/7`, `C1=FAIL`, EXIT=1 |
| G | declared do-nothing control `REFUSEALL.py` | `--builder ev/round58/controls/REFUSEALL.py` | no leg summary and no `C1=` line at all — see §5 |

Exact commands for D/E/H (work roots under `runs/`): the C command above with the `--builder`/`X15_GUARDS` substitutions shown. The seven refusal legs therefore still require distinct observed behaviours; the token fix alone cannot manufacture a pass.

## 4. Second positive-path defect: the span-end formula is not the builder's span-end formula

- Counter (`:139`): `span = form[offset:offset + len(quote) + min(CONTEXT, offset) + CONTEXT]`, where `offset = max(0, form.find(quote) - 80)`.
- Builder (`tools/build-spans.py` docstring line 16 and `:142-143`): `form[max(0, off-80) : off+len(quote)+80]`.

For `off ≥ 80` the two agree. For `0 < off < 80`, `offset = 0`, so the counter expects `form[0:len(quote)+80]` while a conforming builder writes `form[0:off+len(quote)+80]` — the counter's expectation is short by exactly `off` bytes. The `min(CONTEXT, offset)` term is the slip: `offset` is already clamped to 0, so it contributes nothing; the builder uses `off`.

Evidence (both the frozen and the token-fixed counter, conforming control, `--seed 35`):

```
EMPTY_OK=fail(spans/S502-1.txt span bytes)
REBUILD_OK=pass
HELDOUT_OK=pass
SUMMARY OK=3/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
```

Seed 35's fixture has quote offsets `[5405, 26, 4077]`; the `off=26` quote yields counter-span 96 bytes vs builder-span 122 bytes. Frequency over the generator: **9 of 500 seeds** (1–500) place a quote at `0 < off < 80` (first: 35, 104, 138, 140, 308, 313, 344, 353). The frozen predicate's default seed 7 is unaffected (`[3734, 1415, 4074]`), as are seeds 1–30 and 1007, so the defect is **latent** under the frozen invocation but material for any pass-side control that varies the seed — including round-59 calibration batteries that re-run the target at other seeds.

## 5. Third defect: the declared do-nothing control aborts the counter instead of being denied

### Command I — frozen counter, `REFUSEALL.py`

```
python3 -B ev/round58/c1-count.py --builder ev/round58/controls/REFUSEALL.py \
        --work /fast/scratch/hyaku/chousa-r59/R59Executor15/x15/runs/I-frozen-refuseall
```

```
Traceback (most recent call last):
  File ".../ev/round58/c1-count.py", line 406, in <module>
    sys.exit(main())
  File ".../ev/round58/c1-count.py", line 212, in main
    foreign.write_bytes(b"foreign evidence bytes\n")
FileNotFoundError: [Errno 2] No such file or directory:
  '.../runs/I-frozen-refuseall/out-empty/spans/S777-1.txt'
EXIT=1
```

A builder that exits non-zero during `EMPTY_OK` never creates `out/spans`, and `:212` writes the foreign fixture unguarded. The claim clause "Do-nothing controls must not reach `C1=PASS`" is satisfied only because the counter produces **no verdict line at all**; the `--controls` deny tally (`:377`, `:382`) classifies a missing `C1=` line as `denied`, so a crash is scored as a denial. The token-fixed counter crashes identically (run G), i.e. the fix at `:391`/`:399` does not touch this path.

## 6. Round-58 negative receipt reproduced exactly

### Command B — frozen counter, lane builder, declared controls

```
python3 -B ev/round58/c1-count.py --builder lane/tools/build-spans.py \
        --work /fast/scratch/hyaku/chousa-r59/R59Executor15/x15/runs/B-frozen-lane \
        --controls ev/round58/controls
```

All 15 verdict-relevant lines are identical to `corpus/evidence/round58/controls/c1-controls.txt`; the only `diff` hunk is a trailing `\n` inside the `FAT_RAW` reason repr that the receipt trimmed:

```
EMPTY_OK=pass / REBUILD_OK=pass / FOREIGN=fail(rc=0, orphans deleted: foreign gone=True) /
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!) / SYMLINK_CACHE=fail(rc=0, expected refusal) /
FIFO_TXT=fail(...) / DEVZERO_TXT=fail(...) / FAT_RAW=fail(rc=1, reason ['SIZE'] absent in '… ole-malformed …') /
MANY_QUOTES=fail(rc=0, expected refusal) / ESCAPE_ENTRY=pass(refused) / HELDOUT_OK=pass /
BEFORE_FOREIGN=deleted / CONTROL_REFUSEALL=denied / CONTROL_build-spans-r55=denied / DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL   EXIT=1
```

Round-59 `controls/c1-before.txt` (same sha as round-58's) is therefore still the operative "before", and `BEFORE_FOREIGN=deleted` still holds on the pinned r55 builder — the destructive leg discriminates.

## 7. Reading of the operability surface (measurement, not a score claim)

- Positive path: **structurally unreachable at the frozen bytes** (`:391` token); reachable and total on a conforming builder only after that single normalisation, with 7/7 refusal legs and 2/2 denied controls.
- Negative path: reproducible, but the declared do-nothing control is denied by *crash*, not by verdict (§5).
- Fixture path: the counter's own span expectation diverges from the builder's documented slicing for `0 < off < 80` (§4), so a green run is seed-conditional at ≈1.8 % of seeds.
- Substrate path: no hardened candidate exists on the lane (`tools/build-spans.py` == pinned r55 BEFORE), and neither round-58 after-receipt (`c1-measure-after.txt`, `c2-measure-after.txt`) exists. `c2-count.py` (sha `dbb859612f9d018296b217baec76a5c6cb744609b7c95372dabae4d6691c8503`) uses one `PASS` token consistently at `:156/:160/:163`; the C1 token split is not present there.

## 8. Evidence retained, scratch removed

- Run outputs and work roots (all read-only lane inputs; work roots removed with scratch): `runs/{A-frozen-ref,B-frozen-lane,C-tokenfix-ref,D-tokenfix-lane,E-nofor,F-seed35,G-refuseall,H-nosize,I-frozen-refuseall,J-frozen-seed35,K-seed1007,S-seed}`.
- Copies verified by sha before use: counter `65da18bb…`, `capture-text` `2c0140bc…`, r55 control `1ed2650a…`, `REFUSEALL` `e7721cef…`.
- No installs or updates were performed; no package manager was invoked (pacman paused). No lane file, frozen claim, counter or census was written or modified; the only lane write is this report.

## Appendix A — pass-side control source (scratch-only, sha256 `8297447e2923d0f0359e6cc919e0553a650460d63535cd743c471f12f8982121`, deleted with scratch)

```python
#!/usr/bin/env python3
"""Scratch pass-side control for the frozen R58 C1 counter (positive verdict path).

NOT a lane artifact, NOT a candidate builder for the lane. It implements only what
corpus/evidence/round58/c1-count.py checks, using the span slicing documented by
tools/build-spans.py (docstring line 16): form[max(0, off-80) : off+len(quote)+80].
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import pathlib
import re
import stat
import sys

TOOLS = pathlib.Path(__file__).resolve().parent
CONTEXT = 80
SIZE_CAP = 64 * 1024 * 1024
QUOTES_CAP = 100_000
IN_HEADER = ["id", "url", "quote", "entry"]
OUT_HEADER = "id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry"
ID_RE = re.compile(r"^S\d{3}$")
SPAN_RE = re.compile(r"^S\d{3}-\d+\.txt$")
OLE = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
ZIP = b"PK\x03\x04"

CT: list = []
import os

GUARDS = set(filter(None, os.environ.get(
    "X15_GUARDS", "foreign,symlink_out,capture_type,size,rows,escape").split(",")))


def die(msg: str) -> None:
    print(f"build-spans: refused {msg}", file=sys.stderr)
    raise SystemExit(1)


def key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def check_regular(path: pathlib.Path) -> int:
    if "capture_type" not in GUARDS:
        return path.lstat().st_size
    st = path.lstat()
    if stat.S_ISLNK(st.st_mode):
        die(f"symlink capture {path.name}")
    if not stat.S_ISREG(st.st_mode):
        kind = "FIFO" if stat.S_ISFIFO(st.st_mode) else "not_regular"
        die(f"{kind} capture {path.name} (not regular)")
    if "size" in GUARDS and st.st_size > SIZE_CAP:
        die(f"size {st.st_size} exceeds cap {SIZE_CAP} for {path.name}")
    return st.st_size


def capture_text_mod():
    spec = importlib.util.spec_from_file_location("capture_text", TOOLS / "capture-text.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def form_for(cache: pathlib.Path, url: str):
    raw, txt = cache / f"{key(url)}.raw", cache / f"{key(url)}.txt"
    for p in (raw, txt):
        if p.exists() or p.is_symlink():
            check_regular(p)
    if raw.exists():
        with raw.open("rb") as f:
            head = f.read(8)
        if head[:8] != OLE and head[:4] != ZIP:
            die(f"no defined text form for {key(url)}")
        if not CT:
            CT.append(capture_text_mod())
        b = raw.read_bytes()
        try:
            return CT[0].text_form(str(raw)), hashlib.sha256(b).hexdigest()
        except Exception as e:
            die(f"capture-text refused {raw.name}: {str(e)[:120]}")
    if txt.exists():
        b = txt.read_bytes()
        return (b.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n"),
                hashlib.sha256(b).hexdigest())
    die(f"no defined text form for {key(url)}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quotes", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cache", required=True)
    a = ap.parse_args()
    qp, out, cache = pathlib.Path(a.quotes), pathlib.Path(a.out), pathlib.Path(a.cache)

    if out.is_symlink() and "symlink_out" in GUARDS:
        die(f"symlink output {out}")
    if not qp.is_file():
        die(f"no input {qp}")
    lines_in = qp.read_text(encoding="utf-8").splitlines()
    if not lines_in or lines_in[0].split("\t") != IN_HEADER:
        die(f"{qp} header must be {' '.join(IN_HEADER)}")
    if "rows" in GUARDS and len(lines_in) - 1 > QUOTES_CAP:
        die(f"rows {len(lines_in) - 1} exceeds cap {QUOTES_CAP}")

    rows = []
    for ln, line in enumerate(lines_in[1:], start=2):
        cells = line.split("\t")
        if len(cells) != 4:
            die(f"{qp}:{ln} expected 4 columns")
        sid, url, quote, entry = cells
        if not ID_RE.match(sid):
            die(f"{qp}:{ln} bad id {sid!r}")
        if "escape" in GUARDS and ".." in entry:
            die(f"{qp}:{ln} entry escapes: {entry!r}")
        rows.append((sid, url, quote, entry))

    planned: dict[str, str] = {}
    out_rows = [OUT_HEADER]
    seen: dict[str, int] = {}
    for sid, url, quote, entry in rows:
        form, digest = form_for(cache, url)
        n = form.count(quote)
        if n != 1:
            die(f"{sid}: quote occurs {n}x")
        off = form.find(quote)
        seen[sid] = seen.get(sid, 0) + 1
        name = f"spans/{sid}-{seen[sid]}.txt"
        start = max(0, off - CONTEXT)
        span = form[start:off + len(quote) + CONTEXT]
        if span == quote:
            die(f"{sid}: no context around quote")
        planned[name] = span
        out_rows.append("\t".join([sid, url, digest, str(start), name, quote, entry]))

    sd = out / "spans"
    if sd.is_dir() and "foreign" in GUARDS:
        foreign = [p.name for p in sorted(sd.iterdir())
                   if SPAN_RE.match(p.name) and f"spans/{p.name}" not in planned]
        if foreign:
            die(f"foreign spans file spans/{foreign[0]} (kept, refusing before orphan deletion)")

    sd.mkdir(parents=True, exist_ok=True)
    for p in list(sd.iterdir()):
        if SPAN_RE.match(p.name) and f"spans/{p.name}" not in planned:
            p.unlink()
    (out / "spans.tsv").write_bytes(("\n".join(out_rows) + "\n").encode("utf-8"))
    for name, body in planned.items():
        (out / name).write_bytes(body.encode("utf-8"))
    for line in out_rows[1:]:
        cells = line.split("\t")
        print(f"QUOTE {cells[0]} char {cells[3]} {cells[4]}")
    print(f"SPANS_ROWS={len(planned)} WRITTEN={len(planned)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## Appendix B — risks and blockers

- **Blocker (handoff):** round-59 frozen claims absent at the path the wave item names; the wave is executing against round-58 bytes. Any round-59 verdict must say which round's predicate it measured.
- **Risk:** `C1=PASS` is unobtainable from the frozen round-58 counter for any builder; a round-59 positive measurement cannot be produced without normalising `:391`/`:399` (measured: that one change flips the conforming control to `PASS`, exit 0).
- **Risk:** the `0 < off < 80` span expectation (§4, 9/500 seeds) makes any positive measurement seed-conditional; a pass-side battery that varies `--seed` will report false failures for a conforming builder.
- **Risk:** the declared do-nothing control aborts the counter (§5); a deny tally that counts a missing `C1=` line as denial cannot distinguish refusal from crash.

Trailer (relative to lane root):
`report=.ufo/waves/round-59/w1/R59Executor15.md  lane_writes=[report]  scratch=/fast/scratch/hyaku/chousa-r59/R59Executor15 (removed)  installs=none`

## Appendix C — additive measurements from the second instance of this seat id

A second process assigned the same seat (`R59Executor15`) ran concurrently under `/fast/scratch/hyaku/chousa-r59/R59Executor15/{frozen,fixed,w-*}/` and wrote a report to this same path; the sections above are that instance's. Its artifacts were removed; its measurements and the ones below agree on defect A (`C1=PASS` unreachable, two-literal repair flips a conforming builder to `PASS`, exit 0) and on the negative receipt. The findings below are not covered above. All were measured with the exact frozen counter `65da18bb…` and a namespaced copy plus the one-token case fix; a scratch probe builder (`guarded.py`, sha256 `015406be9d381fb5285df39ee6a8e4568a81d2718b9603b26da1b6ed47406dc0`) satisfied every leg predicate by refusing the named reason before delegating to the lane builder for safe legs.

**C1. `SYMLINK_OUT` accepts a write outside `--out` while printing its own annotation (accepted hazard).** `expect_refuse`'s `forbidden_touch` means "must still exist" (`c1-count.py:157-159`) — correct for `FOREIGN` (preserve), inverted for this creation hazard — and the post-check re-labels without demoting (`:234-236` appends to a string that already contains `=pass`). Stub that refuses `SYMLINK` *after* writing `spans.tsv` into the symlink target, on the case-repaired counter:

```
SYMLINK_OUT=pass(refused)(target-dir-written!)
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0
$ ls -l <work>/realdir/        -> -rw-r--r-- ... spans.tsv     # outside --out
$ cat <work>/realdir/spans.tsv -> partial
```

Claim clause (6) ("generated writes are contained under `--out`") is therefore unenforced on the positive path even after the case repair; the annotation is operator-visible text, not a falsifier.

**C2. Six of seven refusal legs assert nothing about partial writes.** Only `SYMLINK_OUT` receives a non-empty `forbidden_touch` (and it is inverted, above); `SYMLINK_CACHE`, `FIFO_TXT`, `DEVZERO_TXT`, `FAT_RAW`, `MANY_QUOTES` are called with `[]` (`:239/:256/:271/:284/:305`). Stub that writes `out-5/spans.tsv` and then refuses the 80 MiB raw input by `SIZE`:

```
FAT_RAW=pass(refused)
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0
$ ls -l <work>/out-5/  -> -rw-r--r-- ... spans.tsv          # left in a refused run's --out
```

The claim clause "refuses … **without partial writes**" (r58 `claims.md:7`) is measured by no leg except the preserve-`FOREIGN` one — reachable as `PASS` once the aggregate is repaired.

**C3. The positive path is `HERE`-relative and fails on a conforming builder without the adjacent control tree.** `BEFORE_BUILDER = HERE / "controls" / "build-spans-r55.py"` (`:26`); a conforming stub run against a copy lacking `controls/` prints `BEFORE_FOREIGN=absent`, `OK=4/4 REFUSE=7/7`, `C1=FAIL`, exit 1. The published command line only works from the exact lane layout.

**C4. Two-direction calibration of the repaired aggregate.** On the case-repaired copy: conforming stub → `OK=4/4 REFUSE=7/7 DENIED=2/2 C1=PASS` exit 0 (nested `--controls` path: `CONTROL_REFUSEALL=denied`, `CONTROL_build-spans-r55=denied`); same stub with the `FOREIGN` guard removed → `FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)`, `REFUSE=6/7`, `C1=FAIL` exit 1; lane builder → `OK=4/4 REFUSE=0/7 C1=FAIL` exit 1. Individual legs discriminate; the accepted hazards in C1/C2 are what the positive verdict misses.

**C5. The `REFUSEALL` control aborts the counter directly as well as being denied when nested** (`fixed/c1-count.py:212` `foreign.write_bytes` into a builder-created `out-empty/spans/`): `FileNotFoundError … out-empty/spans/S777-1.txt`, no `C1=` line, exit 1 — same conclusion as §5 above, reproduced independently on the case-repaired copy.

Trailer (relative to lane root):
`report=.ufo/waves/round-59/w1/R59Executor15.md  lane_writes=[report]  scratch=/fast/scratch/hyaku/chousa-r59/R59Executor15 (own artifacts removed; concurrent instance's x15/ left intact)  installs=none`
