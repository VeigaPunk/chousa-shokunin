# R58ExecC1Atomicity — C1 build-spans: partial-write / write-ordering probe

Seat: R58ExecC1Atomicity (executor, operability). Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Baseline read: lane commit `9e73a031ab1ac3bac343de008850d7d87f9e5634`; claim base `b13ca7b5…`.
`tools/build-spans.py` sha256 `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` = the pinned
round-55 builder (the lane tool IS the pre-hardening baseline). Lane files READ ONLY; my only write is this
report. Scratch `/fast/scratch/hyaku/chousa-r58/R58ExecC1Atomicity/` (removed before yield).
**Method (no system-wide disk pressure):** scratch copy of `tools/build-spans.py` driven **in-process** with
`pathlib.Path.write_bytes` / `os.replace` monkeypatched to raise `OSError(28)` at a chosen call — no disk
filling, no quota, no privileged setup. Fixture: one synthetic `.txt` capture + a deterministic 3-row quotes
table. Driver `probe.py` (scratch).

## 1. Finding A — the base builder is not atomic

Base `main()` order (lines 200-210): orphan `unlink()` → write `spans.tsv` → write each span file. The manifest
is published **before** its payload; each span file is a separate truncating `write_bytes`.

```
$ python3 probe.py base-fresh-partial tools/build-spans.py work
rc=-1 exc=OSError: [Errno 28] No space left on device
state:
  spans/S601-1.txt size=168 sha=20a7ce6eb1a9
  spans.tsv size=561 sha=97fe1121b021
check rc=1 SPANS_FILE_STALE spans/S602-1.txt | SPANS_FILE_STALE spans/S603-1.txt | SPANS_ROWS=3 STALE=2
```

`spans.tsv` is complete (3 rows) while 2 of 3 span files are missing — a manifest pointing at absent evidence
(`--check` reports `STALE=2`: detectable, not prevented). Torn-write variant (fails *after* truncating the
target): `spans/S602-1.txt size=87 sha=283e741e6b42`, content
`'page.\nline 001 carries the token ALPHA001 across the page.\nline 002 carries the token A'` — truncated, yet
still matching `S\d{3}-\d+\.txt`. Rebuild over an existing state: the orphan is deleted **first**, then the write
fails — prior evidence is destroyed by a FAILED run and `--check` then reports the new state as clean:

```
$ python3 probe.py base-rebuild-partial tools/build-spans.py work
failing rebuild rc=-1 exc=OSError: [Errno 28] No space left on device
state after failure:
  spans/S601-1.txt size=168 sha=20a7ce6eb1a9
  spans/S602-1.txt size=174 sha=9ad1f69a40a2
  spans.tsv size=390 sha=4e39f466a51b
before-state files still present:
  spans/S603-1.txt present=False      <-- prior evidence destroyed by a FAILED run
check rc=0 SPANS_ROWS=2 STALE=0        <-- --check reports the NEW state as clean
```

## 2. Finding B — the base builder deletes foreign evidence

The base unlinks any `spans/S###-N.txt` not in the new file set, so a file it never produced is destroyed:

```
== base  rc 0   foreign still present: False   spans.tsv written: True
== prop  rc 1   foreign still present: True    spans.tsv written: False
  build-spans: refused FOREIGN span file(s) in .../spans: S777-1.txt (not produced by this build,
  not in the previous manifest; refusing to delete foreign evidence)
```

## 3. Proposed smallest transactional write ordering

Three rules: (1) **decide before you mutate** — scan `spans/` for files this build will not produce before any
`mkdir`/`unlink`/write, and refuse (exit 1) on an unattributable file, so a refusal leaves the dir identical;
(2) **stage, then commit** — write each span file to `spans/.tmp.<name>.part` and the manifest to
`.spans.tsv.tmp`, then `os.replace()` the span files, then `os.replace()` the manifest **last** (the manifest is
the commit point); (3) **delete only after commit** — orphan removal happens after the manifest lands, and a
`finally` removes temporaries (and any `spans/` dir this run created but did not commit).

Exact patch (applies to `tools/build-spans.py` @ `1ed2650a`; `diff -U0`, 54 lines):

```diff
@@ -36,0 +37 @@
+import os
@@ -201,0 +203,17 @@
+    # FOREIGN scan BEFORE any write, mkdir or deletion
+    mpath = out / "spans.tsv"
+    attributable = {pathlib.PurePosixPath(c.split("\t")[4]).name
+                    for c in mpath.read_text(encoding="utf-8", errors="replace").splitlines()[1:]
+                    if c.count("\t") >= 4} if mpath.is_file() else set()
+    existing = sorted(q.name for q in sd.iterdir() if q.is_file() and SPAN_RE.match(q.name)) \
+        if sd.is_dir() else []
+    want = {n.split("/", 1)[1] for n in files}
+    foreign = [n for n in existing if n not in want and n not in attributable]
+    if foreign:
+        print(f"build-spans: refused FOREIGN span file(s) in {sd}: {', '.join(foreign)} "
+              f"(not produced by this build, not in the previous manifest; refusing to delete foreign evidence)",
+              file=sys.stderr)
+        return 1
+    orphans = [n for n in existing if n not in want]
+    # transactional write: stage -> replace span files -> replace manifest LAST
+    made_spans = not sd.exists()
@@ -203,6 +221,27 @@
-    for p in sd.iterdir():
-        if SPAN_RE.match(p.name) and f"spans/{p.name}" not in files:
-            p.unlink()
-    (out / "spans.tsv").write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
-    for name, body in files.items():
-        (out / name).write_bytes(body.encode("utf-8"))
+    for stale_tmp in sd.glob(".tmp.*"):
+        stale_tmp.unlink(missing_ok=True)   # leftovers of an earlier interrupted run
+    staged: list[tuple[pathlib.Path, pathlib.Path]] = []
+    committed = False
+    try:
+        for name, body in files.items():
+            leaf = name.split("/", 1)[1]
+            tmp = sd / (".tmp." + leaf + ".part")
+            staged.append((tmp, sd / leaf))
+            tmp.write_bytes(body.encode("utf-8"))
+        mtmp = out / ".spans.tsv.tmp"
+        mtmp.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
+        for tmp, dest in staged:
+            os.replace(tmp, dest)
+        os.replace(mtmp, out / "spans.tsv")
+        committed = True
+    finally:
+        for tmp, _ in staged:
+            tmp.unlink(missing_ok=True)
+        (out / ".spans.tsv.tmp").unlink(missing_ok=True)
+        if not committed and made_spans:
+            try:
+                sd.rmdir()          # leave the output dir byte-identical to before
+            except OSError:
+                pass
+    for n in orphans:
+        (sd / n).unlink(missing_ok=True)
```

`--check` is untouched: the patch sits entirely after the `if a.check: return check(...)` early return, so
`check()` and its `SPANS_ROWS=n STALE=k` output are byte-identical to the base. Measured effect, same fixtures
and injection points: fresh build failing at span 2 → base leaves a complete manifest with 2 of 3 span files
missing, patched leaves the output dir empty; torn write → base leaves `S602-1.txt` truncated to 87 B under a
valid span name, patched leaves no span file and cleans temporaries; rebuild over existing state → base deletes
`S603-1.txt`, replaces the manifest and reports `--check` `STALE=0`, patched keeps all 4 pre-failure files
byte-identical (`--check` on the OLD quotes: `SPANS_ROWS=3 STALE=0`); foreign `S777-1.txt` → base deletes it with
`rc 0`, patched preserves it with `rc 1` and writes nothing.

```
$ python3 probe.py prop-rebuild-partial minimal/build-spans.py work
failing rebuild rc=-1 exc=OSError: [Errno 28] No space left on device
pre-failure files preserved byte-identical:
  spans/S601-1.txt present=True identical=True
  spans/S602-1.txt present=True identical=True
  spans/S603-1.txt present=True identical=True
  spans.tsv present=True identical=True
check rc=1 SPANS_ROW_EXTRA spans/S603-1.txt | SPANS_FILE_ORPHAN spans/S603-1.txt | SPANS_ROWS=2 STALE=2
```

The last line is the correct residual: old manifest and old payload are both intact and mutually consistent; the
mismatch is against the *new* quote table, which was never committed. Real-lane regression (read-only; `--check`
writes nothing), base vs patched on three committed lane spans dirs (`round55`/`round56`/`round57-c3`, rc=0
each): `SPANS_ROWS=19 STALE=0 / 23 STALE=0 / 10 STALE=0` for **both** builders. Byte-identical rebuild of
`round55` into a scratch copy of the lane's own `spans/` + `spans.tsv`:

```
$ python3 -B minimal/build-spans.py --quotes quotes.tsv --out . --cache ../captures2
SPANS_ROWS=19 WRITTEN=19 ; rc=0 ; BYTE_IDENTICAL_R55=yes   (spans.tsv + all 19 span files unchanged)
```

`round57/c3` rebuild likewise `BYTE_IDENTICAL=yes` (10 rows).

**Scope boundary.** The ordering patch alone fixes **only** `FOREIGN` + the atomicity class; the five input-side
legs (symlink/type/size/row caps) are a separate surface — on the ordering-only builder the frozen counter
printed `FOREIGN=pass(refused)` but `SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)`,
`SYMLINK_CACHE=fail(rc=0, expected refusal)`, `FIFO_TXT=fail(rc=1, reason [...] absent in ...)`,
`DEVZERO_TXT=fail(...)`, `FAT_RAW=fail(...)`, `MANY_QUOTES=fail(rc=0, expected refusal)`, `SUMMARY OK=4/4
REFUSE=0/7`. A scratch variant adding the input-side hardening (`proposed/`: `lstat`/`S_ISREG` probe, 64 MiB
cap, `QUOTES_CAP = 100_000`, `--out`/`spans/` symlink refusals) satisfies all eleven leg *semantics*:

```
$ python3 .../c1-count.py --builder proposed/build-spans.py --controls <lane controls dir> --work <fresh>
EMPTY_OK=pass REBUILD_OK=pass FOREIGN=pass(refused) SYMLINK_OUT=pass(refused) SYMLINK_CACHE=pass(refused)
FIFO_TXT=pass(refused) DEVZERO_TXT=pass(refused) FAT_RAW=pass(refused) MANY_QUOTES=pass(refused)
ESCAPE_ENTRY=pass(refused) HELDOUT_OK=pass BEFORE_FOREIGN=deleted
CONTROL_REFUSEALL=denied CONTROL_build-spans-r55=denied DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
```

**The counter still prints `C1=FAIL` and exits 1 although every leg passes** — Finding C.

## 4. Finding C — the frozen counter cannot report `C1=PASS` (counter defect, not a builder defect)

`corpus/evidence/round58/c1-count.py` line 51 sets `PASS = "pass"` (lowercase); every leg is formatted with that
constant (line 223 `f"FOREIGN={PASS}(refused)"`, line 234, and `expect_refuse` at line 150). But the aggregation
at line 391 is `ref_pass = all(("=PASS" in l) for l in ref_legs)` — uppercase — and line 399's `SUMMARY` counts
`sum('=PASS' in l ...)` likewise. A leg that *correctly* refuses is `FOREIGN=pass(refused)`, lowercase, and never
contains `=PASS`. Line 390 aggregates the safe legs with lowercase `("=pass" in l)`; only line 391 disagrees with
its own formatter. Replay of the frozen aggregation over the counter's own printed legs:

```
PASS constant: PASS = "pass"
ok_pass = True  ref_pass = False
SUMMARY OK=4/4 REFUSE=0/7
=> verdict = FAIL
```

So **no builder that refuses correctly can ever make the frozen counter print `C1=PASS`**. Worse, the same
substring test makes it satisfiable by a *wrong* builder: a FAIL line embeds the builder's stderr, so a builder
printing the literal `=PASS` in its refusal text (naming no reason class) turns `ref_pass` true. Demonstrated
with a scratch diagnostic builder (`work/gamer3/`, never in the lane) that also writes into the symlink target:

```
FOREIGN=fail(reason-unnamed:'build-spans: refused span dir .../spans (=PASS)\n')
SYMLINK_OUT=fail(rc=1, reason ['SYMLINK'] absent in '... (=PASS)\n')(target-dir-written!)
SYMLINK_CACHE=fail(rc=1, reason [...] absent in '... (=PASS)\n')
   (all seven refusal legs print "fail" yet contain "=PASS")
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0
```

The frozen predicate is therefore simultaneously **unsatisfiable by a correct builder and satisfiable by an
incorrect one**; its verdict is decoupled from its own printed leg results. The printed leg lines are the truth;
the `C1=` line and exit code are not. I did **not** modify the counter, `claims.md`, `c1-count.py` or any lane
file — this is a finding for the L1. (The same defect was independently reported by peer `R58ScribeC1PatchNotes`;
I re-derived it from source rather than relying on the report.) A one-character-class fix at line 391
(`"=PASS"` → `"=pass"`) would restore the intended discrimination — `C1=PASS` for the scratch `proposed/` builder
and `C1=FAIL` for the gaming builder — but that edit is the L1's to make; the counter is frozen for this wave.

## 5. Unrun / out of scope

- Not run: `c2-count.py` (C2 is another seat's surface); any live fetch (none authorized, none done).
- Not run: the counter against `proposed/` **after** a hypothetical line-391 fix — the fix is the L1's to make and
  the counter is frozen; the equivalent discrimination is established by the replay above.
- Not run: concurrency (two builders on one `--out`); the claim explicitly does not cover broader races.
- Not run: a real >64 MiB capture (the lane's largest capture is 7.8 MB); the cap is exercised by the counter's
  80 MiB sparse `FAT_RAW` fixture, which the scratch `proposed/` builder refuses with the `SIZE` reason.
- `tools/build-spans.py` was NOT modified (sha256 still `1ed2650a…`); `git diff 9e73a03..HEAD` over `tools/`,
  `claims.md` and `c1-count.py` is empty.

## 6. Verdict

VERDICT: The C1 write-ordering hazard is CONFIRMED in the pinned baseline `tools/build-spans.py` (`1ed2650a…`): a
mid-build write failure publishes a complete `spans.tsv` before its span files, can leave a truncated file under
a valid `S###-N.txt` name, and — because orphan deletion runs first — destroys prior evidence and then reports a
`--check`-clean state for a build that never completed; the base also deletes an unattributable `S777-1.txt`
outright. The smallest transactional ordering (decide-then-mutate; stage, replace span files, replace the
manifest LAST; delete orphans only after commit) is given as exact patch text in §3 and is measured to leave the
output directory byte-identical at every failure point while keeping `--check` byte-identical and real-lane
rebuilds byte-identical (`round55` 19 rows, `round57/c3` 10 rows). The ordering patch alone does not close the
five input-side legs (symlink/type/size/row caps) — a separate surface, and the scratch variant adding them
passes all eleven leg semantics. The frozen C1 **predicate** is **falsified as a gate**: `c1-count.py` line 391
aggregates the refusal legs with uppercase `=PASS` against a lowercase `PASS = "pass"` formatter, so no
correctly-refusing builder can print `C1=PASS`, while a builder that merely prints `=PASS` in its stderr and
names no reason class does print `C1=PASS` and exit 0 — both reproduced. The C1 *hazard* findings survive; the
frozen *counter* cannot currently certify them.
