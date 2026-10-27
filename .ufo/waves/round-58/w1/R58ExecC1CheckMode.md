# R58ExecC1CheckMode — `--check` audit of `tools/build-spans.py`

Seat R58ExecC1CheckMode (leaf, operability). Lane `chousa-shokunin`. Freeze `9e73a031ab1ac3bac343de008850d7d87f9e5634`, claim base `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`. Brief: audit `tools/build-spans.py --check` with a scratch manifest — are symlinked `spans.tsv`/span files or orphan spans followed — and propose a check-mode guard consistent with frozen C1. No live fetch; no lane file written except this report. Scratch `/fast/scratch/hyaku/chousa-r58/R58ExecC1CheckMode/` (removed before yielding). In outputs `S=` = that scratch dir, `L=` = lane root. Read: `claims.md` (C1 clause whole; line 19 raw), `c1-count.py` (406 lines whole), `c2-count.py`, `tools/build-spans.py` (217 lines whole).

## 0. The builder's current bytes

```
$ cd L && sha256sum tools/build-spans.py corpus/evidence/round58/controls/build-spans-r55.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  corpus/evidence/round58/controls/build-spans-r55.py
$ git diff --stat 9e73a031ab1ac3bac343de008850d7d87f9e5634 HEAD -- corpus/evidence/round58/claims.md \
    corpus/evidence/round58/c1-count.py corpus/evidence/round58/c2-count.py corpus/evidence/round58/c2/quotes.tsv tools/build-spans.py
(empty = unchanged)
```

The lane builder is **still byte-identical to the pinned round-55 "before" builder** — C1 hardening is not applied. Re-verified at the current tip (the lane advanced to `5da0a63` under other seats while I worked); the diff is empty, so every measurement still describes the frozen surface.

## 1. The frozen C1 counter never exercises `--check`

```
$ grep -n -- "--check" corpus/evidence/round58/c1-count.py   -> NONE
$ grep -n -- "--check" corpus/evidence/round55/c1-count.py   -> NONE
```

`run_builder()` (c1-count.py:118-127) invokes the builder **without** `--check`; every C1 leg is a **build-mode** leg, so `check()` (build-spans.py:189-215) is reached by **no** frozen leg. `--check` is nevertheless a live operator surface: `corpus/knowledge/grey-literature-and-chinese-search-record-r40.md:6` and `corpus/knowledge/grey-literature-field-china-r42.md:8` instruct the reader to run it, and the lane's round-46/47 verifier spot-checks record `build-spans.py --check` → `SPANS_ROWS=n STALE=0` as a gate. So it is inside C1's "operability" wording but **outside what the frozen predicate can measure**.

## 2. Measured `--check` behaviour on the frozen builder

Scratch copy `S/build-spans-base.py` (sha256 `1ed2650a…`, byte-for-byte from the lane); commands run with cwd inside scratch and `TMPDIR` set to it. One fixture per row; `rc` is the child's exit code.

| fixture | base `--check` | meaning | |---|---|---| | clean tree | rc=0 `SPANS_ROWS=1 STALE=0` | baseline | | `out/spans.tsv` → outside regular file (identical bytes) | rc=0 `SPANS_ROWS=1 STALE=0` | **followed** | | `out/spans/S501-1.txt` → outside identical file | rc=0 `SPANS_ROWS=1 STALE=0` | **followed** | | orphan `out/spans/S777-1.txt` | rc=1 `SPANS_FILE_ORPHAN spans/S777-1.txt` | reported, file preserved | | `out/spans` → outside dir | rc=1 `SPANS_HEADER_STALE`, `SPANS_ROW_STALE` | **followed** | | `out/spans.tsv` is a FIFO | rc=1 `SPANS_HEADER_STALE` | not hung (`is_file()` False) | | `out/spans/S501-1.txt` is a FIFO | rc=1 `SPANS_FILE_STALE` | not hung | | `out/spans.tsv` → `/dev/zero` | rc=1 `SPANS_HEADER_STALE` | not hung | | orphans `notes.txt`, `S777-1.txt`, `S888-1.txt.bak` | only `S777-1.txt` reported | orphan rule is `SPAN_RE`-scoped | | `--out` itself a symlink to a real dir | rc=0 `SPANS_ROWS=1 STALE=0` | **followed** | | orphan `S777-1.txt` is itself a symlink | rc=1 `SPANS_FILE_ORPHAN` | reported; link untouched | | **every** artifact an external symlink, zero real files in `out/` | rc=0 `SPANS_ROWS=1 STALE=0` | **sharpest case** |

**The concrete work/attack (last row).** A tree whose `spans.tsv` and `spans/` are symlinks into an external directory holds **no real file at all** under `--out`, yet `--check` prints `STALE=0` and exits 0: the operator conclusion ("this manifest is current") comes entirely from bytes outside the directory being certified — and `--check` is what the knowledge entries cite as the recheck procedure.

**Orphan spans are followed, not merely reported.** `sorted(sd.iterdir())` walks the *target* of a symlinked `spans/`, so an orphan `S###-N.txt` living outside `--out` is reported as `SPANS_FILE_ORPHAN` as if it were the lane's own. The positive side holds: a genuine in-tree orphan is reported and **preserved** (`foreign file still exists: True | tree unchanged: True`) — `--check` never unlinks.

**Unbounded read.** `check()` reads the manifest with `m.read_text()` and each span with `p.read_bytes()`, neither size-bounded. Child peak RSS via `getrusage(RUSAGE_CHILDREN).ru_maxrss` (`rss.py` wrapper; `/usr/bin/time -v` is not installed here):

```
### MANIFEST_1GIB  (out/spans.tsv -> 1 GiB sparse file)      CHILD_MAXRSS_KIB=2116924  (≈2.06 GiB)  rc=1
### SPANFILE_1GIB  (out/spans/S501-1.txt -> 1 GiB sparse)    CHILD_MAXRSS_KIB=1067168  (≈1.02 GiB)  rc=1
```

C1 bounds *raw capture* reads at 64 MiB; the manifest/span read path in `--check` is unbounded and reachable by a symlink alone. Largest committed artifacts are tiny (`spans.tsv` ≤ 18155 B; span ≤ 740 B) — a hazard-surface finding, not a live-cost one.

## 3. Adjacent finding (build mode, same tool) — destructive escape through symlinks

Outside this seat's `--check` brief but the same class; the L1 will be asked. **Build** writes and deletes through symlinks with no containment (scratch fixtures `S/probe2`, `S/probe5`):

```
A  build, out/spans -> outside dir
     rc=0 | outside| S501-1.txt len=139 head=b'Sentence 000 carries alpha bravo charlie delta e'  <-- wrote OUTSIDE --out
B  build, out/spans.tsv -> outside victim
     rc=0 | victim now: b'id\turl\tcapture_sha256\toffset\tspan_file\tquote\tent'                <-- overwrote outside file
C  build, out/spans/S501-1.txt -> outside victim
     rc=0 | victim now: b'Sentence 000 carries alpha bravo charlie delta e'                     <-- overwrote outside file
del_through_symlink (build, out/spans -> outside dir, foreign S777-1.txt outside): outside victim exists before: True / after: False  <-- DELETED outside --out
```

The last is the destructive counterpart of C1's FOREIGN leg: the base deletes a foreign `S###-N.txt` — the FOREIGN leg's own target class — and the deletion escapes `--out` when `out/spans` is a symlink. The frozen SYMLINK_OUT leg symlinks `--out` itself, so it does not cover a link *inside* `--out`.

## 4. Two frozen-counter defects (findings; no frozen file edited)

**4a. `c1-count.py` can never print `C1=PASS`.** `PASS = "pass"` (line 51) but the refusal aggregate is `ref_pass = all(("=PASS" in l) for l in ref_legs)` (line 391) and `SUMMARY` counts `"=PASS"` too (line 399). Every refusal leg is *emitted* lowercase (`expect_refuse`, line 160 → `f"{name}={PASS}(refused)"`), so `"=PASS"` never matches a passing refusal leg; the safe-leg aggregate uses lowercase `"=pass"` (line 390) and does work — hence `OK=4/4` below. Reproduced with a scratch stub satisfying every leg predicate (`S/stub/ALLPASS.py`, importing the lane builder read-only for the safe-leg bytes):

```
$ python3 corpus/evidence/round58/c1-count.py --builder S/stub/ALLPASS.py --work S/c1-stub2
EMPTY_OK=pass / REBUILD_OK=pass / FOREIGN=pass(refused) / SYMLINK_OUT=pass(refused) / SYMLINK_CACHE=pass(refused) / FIFO_TXT=pass(refused) / DEVZERO_TXT=pass(refused) / FAT_RAW=pass(refused) / MANY_QUOTES=pass(refused) / ESCAPE_ENTRY=pass(refused) / HELDOUT_OK=pass / BEFORE_FOREIGN=deleted / DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
```

**All eleven legs pass and the verdict is still `C1=FAIL`** (`REFUSE=0/7` — the tally uses `"=PASS"` too). Under the counter as frozen, **no builder patch can make `C1=PASS` print**: the frozen predicate ("must print `C1=PASS` and exit 0") is unreachable and `C1=PASS` is a falsified outcome condition, not a pass signal. The legs *do* discriminate behaviour — the frozen builder against the same counter:

```
$ python3 corpus/evidence/round58/c1-count.py --builder tools/build-spans.py --work S/c1-base
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True) / SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!) / SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason [...] absent in 'build-spans: refused S571: no defined text form for ...') / DEVZERO_TXT=fail(rc=1, reason [...] absent in 'build-spans: refused S581: no defined text form for ...')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused S551: capture-text refused ...: ole-malformed ...') / MANY_QUOTES=fail(rc=0, expected refusal)
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
```

— the same 7 refusal legs the all-pass stub satisfies — but the aggregate cannot express the passing state. This is an **L1 decision** about how to read the frozen claim; the control (`denied_pass`) logic is unaffected. (First reported by peer `R58ScribeC1PatchNotes`; re-derived from source and reproduced here before accepting it.)

**4b. `c1-count.py` crashes (no `C1=` line) on an early-refusing builder.** Line 212 does `foreign.write_bytes(...)` into `out/spans/`, a directory created by the *builder*:

```
$ python3 corpus/evidence/round58/c1-count.py --builder corpus/evidence/round58/controls/REFUSEALL.py --work S/c1-refuseall
Traceback (most recent call last):
  File ".../c1-count.py", line 212, in main
    foreign.write_bytes(b"foreign evidence bytes\n")
FileNotFoundError: [Errno 2] No such file or directory: 'S/c1-refuseall/out-empty/spans/S777-1.txt'
```

No `C1=` line, exit 1 — the frozen `REFUSEALL` control crashes instead of being scored denied. (In the `--controls` sub-path the counter runs as a subprocess and looks for a `C1=` line, so a crash reads as "not `C1=PASS`" = denied; the crash is only fatal when the counter itself is under test.)

## 5. Cross-claim coupling: C2's `BUILDER_PIN` vs any C1 hardening of that file

`c2-count.py` pins `tools/build-spans.py` to the **round-55** sha256 (`BUILDER_SHA`, line 19; checked line 68) and rebuilds the C2 manifest with that same file (line 122). `claims.md` calls C2 "independent of C1's tool change" — but only while C2's `BUILDER_PIN` holds, and C1's target *is* a change to that file. Measured on a scratch `git archive` copy of the lane (never the lane):

```
--- HARDENED-in-place: rc=1  BUILDER_PIN present: True
      ERROR BUILDER_PIN
--- R55-bytes-restored: rc=1  BUILDER_PIN present: False
```

A hardened `tools/build-spans.py` makes C2 fail `BUILDER_PIN` outright. C1 and C2 cannot both be satisfied by the same bytes at that path unless one moves (e.g. C1 hardens a new file; C2 keeps the pinned round-55 builder for its rebuild). **L1 decision, not an executor fix** — it changes which file each claim is about. The C2 rebuild compares byte-for-byte, so any C1 patch changing a written byte also breaks `BUILDER_REBUILD_MISMATCH`.

## 6. Proposed check-mode guard (patch only — no lane file edited)

Scratch patch `S/build-spans-checkguard-min.py`, a minimal diff against the frozen builder bytes (docstring untouched). Four hunks: (1) `SIZE_CAP = 64 * 1024 * 1024`; (2) `guard_path(p, what, want_dir=False)` — refuses `SYMLINK` for a symlinked path, `NOT_REGULAR` for a non-regular file/non-directory, `SIZE` over `SIZE_CAP`, exiting 1 via `_refuse()`; (3) `guard_output_tree(out)` guarding `--out`, `out/spans.tsv`, `out/spans`, called as the **first** statement of `check()` before the manifest is read; (4) a per-span `guard_path(p, "span file")` and refusal of a symlinked **orphan** span. Reason classes are exactly those the frozen counter names (`SYMLINK`, `NOT_REGULAR`/`FIFO`, `SIZE`), so the guard is consistent with frozen C1 vocabulary. Check mode stays **read-only** — the guard refuses, never unlinks — so the FOREIGN "foreign file preserved" property is untouched.

```
### clean              base (0,'SPANS_ROWS=1 STALE=0','-')  guard (0,'SPANS_ROWS=1 STALE=0','-')
### manifest symlink   base (0,'SPANS_ROWS=1 STALE=0','-')  guard (1,'-','build-spans: refused SYMLINK: manifest .../out/spans.tsv is a symlink to .../e.tsv')
### span symlink       base (0,'SPANS_ROWS=1 STALE=0','-')  guard (1,'-','build-spans: refused SYMLINK: span file .../out/spans/S501-1.txt is a symlink to .../e.txt')
### spans dir symlink  base (0,'SPANS_ROWS=1 STALE=0','-')  guard (1,'-','build-spans: refused SYMLINK: spans dir .../out/spans is a symlink to .../ed')
### FIFO manifest      base (1,'SPANS_HEADER_STALE | SPANS_ROW_STALE ...','-')  guard (1,'-','build-spans: refused NOT_REGULAR: manifest ... is not a regular file')
### FIFO span file     guard (1,'-','build-spans: refused NOT_REGULAR: span file ... is not a regular file')
### /dev/zero manifest guard (1,'-','build-spans: refused SYMLINK: manifest ... is a symlink to /dev/zero')
### orphan thru symlinked spans dir  base (1,'SPANS_FILE_ORPHAN spans/S777-1.txt | SPANS_ROWS=1 STALE=1','-')  guard (1,'-','build-spans: refused SYMLINK: spans dir .../out/spans is a symlink to .../outside_spans')
### orphan foreign     base (1,'SPANS_FILE_ORPHAN spans/S777-1.txt | SPANS_ROWS=1 STALE=1','-')  guard (1,'SPANS_FILE_ORPHAN spans/S777-1.txt | SPANS_ROWS=1 STALE=1','-')  <-- unchanged
### tampered span      base (1,'SPANS_FILE_STALE spans/S501-1.txt | SPANS_ROWS=1 STALE=1','-')  guard (1,'SPANS_FILE_STALE spans/S501-1.txt | SPANS_ROWS=1 STALE=1','-')  <-- unchanged
```

**Non-regression evidence.** Build mode untouched → build outputs byte-identical to the frozen builder on two real lane quote sets (`round55` 20 files, `round56` 24 files): `build bytes identical: True` both. Real lane evidence unchanged: `round51 SPANS_ROWS=70 STALE=0`, `round53 63 STALE=0`, `round55 19 STALE=0`, `round56 23 STALE=0` — identical to the frozen builder on every committed dir tested (r49/50/52/54 also identical, including their pre-existing STALE counts). Stale detection preserved: tampered span → `SPANS_FILE_STALE`, extra manifest row → `SPANS_ROW_EXTRA`, header mismatch → `SPANS_ROW_STALE`, all unchanged under the guard. Frozen counter on the patched builder → `SUMMARY OK=4/4 REFUSE=0/7 ... C1=FAIL`, identical to the frozen builder's own result: the check-mode patch neither helps nor hurts the frozen legs.

**Patch scope limits.** The guard covers `--check` only. It does **not** fix §3's build-mode escapes (write and delete through symlinks inside `--out`), the unbounded cache reads, or the row cap — those are the C1 build-mode battery's subject. The same `guard_path` helper would apply to the build path's `sd.mkdir`/`unlink`/`write_bytes` calls, but that is a larger change and, per §5, moves C2's pin anyway.

## 7. Scope discipline

Lane files read only: `tools/build-spans.py`, `tools/capture-text.py` (copy only), `corpus/evidence/round58/*`, `corpus/knowledge/*.md` (grep), `corpus/evidence/round5*/` (read-only `--check` runs). Lane files written: **none** — the only write is this report. No git/jj mutation, no commit, no push, no network; `git rev-parse --show-toplevel` was asserted to be the lane before the one read-only `git archive` (into scratch). Scratch: one directory, no lane clone/worktree (the `git archive` copy is a plain tree, used read-only as a `--root` for the §5 pin test), removed before yielding. Tooling: no install/update requested or performed; no pacman transaction. Unrun: `--check` with a `--quotes` file that is itself a symlink (not probed; `read_quotes` is shared with build mode, outside this brief); concurrent-writer races (out of scope).

VERDICT: the concrete work/attack is `--check` certifying an output tree whose `spans.tsv`, `spans/` and span files are all symlinks pointing outside `--out` — it prints `SPANS_ROWS=1 STALE=0` and exits 0 on a directory containing no real file, because `check()` reads `m.read_text()`, `p.read_bytes()` and `sorted(sd.iterdir())` with no symlink/type/size guard — the attack **survives** on the frozen builder, and the frozen C1 counter cannot observe it (it never passes `--check`); the proposed minimal check-mode guard **falsifies** it (refuses `SYMLINK` before any read; build bytes and stale detection unchanged), but that fix is **inconclusive** as a C1 *verdict*, because the frozen counter's `C1=PASS` condition is unreachable (line 391 aggregates `"=PASS"` against `PASS="pass"`), so no frozen predicate can certify the fix either way.
