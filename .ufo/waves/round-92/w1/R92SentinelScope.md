# R92SentinelScope — scope & safety review of round 92's instruments and dispatch text

Seat: `R92SentinelScope` (sentinel, scope/safety lane) · Wave: round 92 / w1
Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`
Scratch: `/fast/scratch/hyaku/chousa-r92/R92SentinelScope` (deleted before yield)
Receipts: `.ufo/waves/round-92/w1/receipts/R92SentinelScope/` (21 files, all cited below)

Attacked tree: carrier **C5** `16ccf7693c61b8ffe392fc757352304f239bfcad` (clone at
`$S/repo`, `git -C $S/repo rev-parse HEAD` = `16ccf769…`, toplevel asserted = `$S/repo`).
Freeze **F5** `42e0337822a508208800f98faa3a63c6af9f8c27`.

**No tool was installed or upgraded this round** — every check used preinstalled
`git`, `python3` (`python3 -B`), `sha256sum`, `grep`, `cmp`, `man`. Nothing in
`/home/vgpnk/.omp/agent/RULES.md`'s channel order was needed; no `pacman`, `uv`, `npx`,
`cargo` or `npm` transaction was performed, so the host-wide pacman pause was not
touched. Network: none (the only re-open was item **S070**, the local installed
`sha256sum(1)` page, read from disk with `man -P cat 1 sha256sum` — see §7).

---

## Verdict summary

| # | Severity | Scope | Finding |
|---|----------|-------|---------|
| F1 | **HIGH** | C1 / C2 dispatch text | Two frozen counting commands name files that do not exist at C5 → `python3: can't open file … No such file or directory`, exit 2 |
| F2 | **MEDIUM** | C1 dispatch text | `emit` without `--receipts` does **not** exit 2 and **does** write into the tree's receipts dir — rule 8 of the frozen claim is not implemented |
| F3 | **MEDIUM** | C1 dispatch text | `PIN_DUPLICATE` exits **1**, not the frozen "exit 2"; message goes to **stderr**, not stdout |
| F4 | **MEDIUM** | C1 dispatch text | `verify` with `--root` ≠ the driver tree reads/scores files **outside `--root`** (path escape via `rel_for`) |
| F5 | **MEDIUM** | C1 dispatch text | On-disk tampering of a **pinned** instrument (`curation-r92.py`) is not detected: `PINNED_FILES=7` of 16 pins are byte-checked |
| F6 | **LOW** | C2 dispatch text | C2 controls summary line prints `PRIOR_REGRESSION=4/4`, not the frozen `PRIOR_REGRESSION=7/7` |
| F7 | **LOW** | C1 expected.tsv | The `c1-harm` row hard-codes `HOME=/home/vgpnk`, defeating the driver's scrubbed-env leg |
| F8 | **LOW** | C3 tree | Byte-identical alias instruments `tally-r92.py` / `tally-controls-r92.py` are pinned-but-unreferenced dead weight |
| F9 | **INFO** | plan / claims | The plan's `narrowing` pointer target `.ufo/waves/round-92/claim-falsification.tsv` does not exist |
| F10 | **INFO** | C3 claims | `controls/receipts/c{1,2,3}-before.txt` cited by the plan/claims are absent at C5 |

Everything else in the assignment's checklist **held**: no network calls, no host
mutations, no secret shapes, no writes under `controls/receipts/` from `verify`,
`--work` is the only write root, and F5→C5 changed exactly the six receipts.

---

## F1 — HIGH — two frozen counting commands name non-existent files

The frozen predicate set names two instruments that do not exist at C5.

**F1a — C1 forgery battery.** `corpus/evidence/round92/claims.md:16` and
`.ufo/waves/round-92/claims.json:32` both name `corpus/evidence/round92/control-forgeries-r92.py`.
No such file exists at C5. The file that exists is `corpus/evidence/round92/forgeries-r92.py`
(plus byte-identical aliases `tally-r92.py`, `tally-controls-r92.py`).

Command, verbatim from the claim, run at C5:

```
$ cd $S/repo && python3 -B corpus/evidence/round92/control-forgeries-r92.py --work $S/r2
python3: can't open file '/fast/scratch/hyaku/chousa-r92/R92SentinelScope/repo/corpus/evidence/round92/control-forgeries-r92.py': [Errno 2] No such file or directory
EXIT=2
```
Receipt: `receipts/R92SentinelScope/r2-forgery-claim-path.txt`.

The **substance** of the claim is satisfiable at the real path — `forgeries-r92.py`
prints exactly the claimed `FORGERY_REFUSED=3/3 POSITIVE=pass` (exit 0), receipt
`r3-forgery-real-path.txt`:

```
OK dup-pin-path: r92 rc=1 (PIN_DUPLICATE), r91 mechanism proven=True
OK second-script-unpinned: r92 rc=1 (INSTRUMENT_UNPINNED:elsewhere.sh), r91 mechanism proven=True
OK pins-rewrite: r92 rc=1 (INSTRUMENT_PIN_MISMATCH:pins.txt), r91 mechanism proven=True
OK positive: r92 rc=0 (r91 verify is not run: …)
FORGERY_REFUSED=3/3 POSITIVE=pass
EXIT=0
```

**F1b — C2 controls battery.** `corpus/evidence/round92/claims.md:66` and
`.ufo/waves/round-92/claims.json:86` name `corpus/evidence/round92/curation-r92-controls.py`.
The file that exists is `corpus/evidence/round92/curation-controls-r92.py`.

```
$ cd $S/repo && python3 -B corpus/evidence/round92/curation-r92-controls.py --root . --work $S/r5
python3: can't open file '…/corpus/evidence/round92/curation-r92-controls.py': [Errno 2] No such file or directory
EXIT=2
```
Receipt: `r6-c2-controls-claim-path.txt`. The real path works and prints the
claimed fields (exit 0) — receipt `r5-c2-controls-real-path.txt`.

**Exploit path / impact.** A wave seat that copies the claim's `counting_command`
verbatim — the natural thing to do, since the claim is the frozen contract — gets
`No such file or directory` and exit 2 on **correct bytes**, and will plausibly
report "the instrument is missing" or, worse, silently substitute a differently-named
file and attribute its output to the claim. The predicate *is* met at the real paths,
so this is a **dispatch-text defect, not a claim falsification**: the round report
must state the correct filenames (`forgeries-r92.py`, `curation-controls-r92.py`) and
the claim/claims.json prose needs a corrective amendment.

Note the naming drift is asymmetric across the three claims: C3's names
(`skill-tally-r92.py`, `skill-tally-r92-controls.py`) are correct; C1 and C2's are not.
Round-91's equivalent files were `control-forgeries-r91.py` and `curation-r91-controls.py`,
so the r92 filenames appear to have been shortened/reordered relative to their r91
predecessors without the claim text being updated.

**Smallest remediation.** Amend `corpus/evidence/round92/claims.md:16,66` and
`.ufo/waves/round-92/claims.json:32,86` to the real filenames
(`forgeries-r92.py`, `curation-controls-r92.py`) — or, cheaper and safer for the
frozen pins table, add `control-forgeries-r92.py` and `curation-r92-controls.py` as
copies of the real files and pin them (the pins table already pins
`forgeries-r92.py` and `curation-controls-r92.py`, so the copies must be added to
`instrument-pins.txt` and the pins file's minus-self digest regenerated).

---

## F2 — MEDIUM — `emit` without `--receipts` does not exit 2 and writes into the tree

`corpus/evidence/round92/claims.md:32` (rule 8) freezes:
> "`emit` without an explicit `--receipts` exits 2 (`emit requires an explicit --receipts`)"

Neither half is implemented at C5.

- The string `emit requires an explicit --receipts` appears **only** in
  `claims.md:32` and in `claims.json`; `git grep -n "emit requires an explicit" 16ccf769…`
  returns exactly one hit — the claim text itself. The driver
  (`corpus/evidence/round92/control-driver-r92.py:370`) has
  `ap.add_argument("--receipts", default=DEFAULT_RECEIPTS)`, i.e. a **silent default**,
  and `main()` at line 391 does `os.makedirs(a.receipts, exist_ok=True)` with no
  check that `--receipts` was passed explicitly.
- Observed: `emit` without `--receipts` runs all six legs and **overwrites the six
  committed receipts in the tree**:

```
$ python3 -B $D/corpus/evidence/round92/control-driver-r92.py emit --root $D --rev 42e0337… --work $S/r15
EMIT c1-gate-r89 exit=1 want=0 MISMATCH
EMIT c1-mutants-r89 exit=0 want=0 OK
EMIT c1-harm exit=128 want=0 MISMATCH
EMIT c1-harm-setup exit=2 want=2 OK
EMIT c2-prior-landing exit=0 want=0 OK
EMIT c2-prior-controls exit=0 want=0 OK
EMITTED=6 MISMATCH=2
EXIT=1
--- did it write under controls/receipts/ ? ---
-rw-r--r--  13145  c1-gate-r89.txt      (was 513 bytes at C5)
-rw-r--r--    213  c1-harm-setup.txt   (was 199)
-rw-r--r--    243  c1-harm.txt         (was 163)
-rw-r--r--   5866  c1-mutants-r89.txt   (was 2565)
-rw-r--r--   1767  c2-prior-controls.txt
-rw-r--r--    530  c2-prior-landing.txt
```
Receipts: `r15-emit-without-receipts.txt`, `r16-emit-clobbers-tree-receipts.txt`.

**Impact.** The claim's own rule 1 (`verify` writes nothing under
`controls/receipts/`) is satisfied by `verify` — I confirmed the receipts directory
is byte-identical before and after a `verify` run (sha256 of all six files matches;
receipt `r11-receipts-write-scope.txt`), and a whole-tree hash before/after `verify`
is `TREE_IDENTICAL`. But the *`emit`* path has no such guard: running `emit` in a
checkout silently rewrites the committed receipts, destroying the committed evidence
that `verify` then scores. Two `EMIT … MISMATCH` lines above also show `emit` produces
non-matching bodies when the tree is not a git checkout (`git show` fails, exit 128) —
so the overwrite is not merely idempotent, it is destructive.

**Smallest remediation.** In `main()`, in the `emit` branch, reject when
`"--receipts" not in sys.argv` (or when `a.receipts == DEFAULT_RECEIPTS`) with
`print("emit requires an explicit --receipts"); return 2`, and amend `claims.md:32`
only if the amended behaviour is stated differently.

---

## F3 — MEDIUM — `PIN_DUPLICATE` exits 1, not 2, and prints to stderr

`corpus/evidence/round92/claims.md:29` (rule 6) freezes:
> "a repeated pin path is `SETUP PIN_DUPLICATE` exit 2 before any receipt is scored"

The refusal itself works and is correctly ordered (no receipt is scored — confirmed:
stdout contains no `RECEIPT …` line). But the exit code and stream differ:

```
EXITCODE= 1
STDOUT= 'BASES root=… repo=…\n'
STDERR= 'SETUP PIN_DUPLICATE path=corpus/evidence/round92/control-driver-r92.py\n'
```
Receipt: `r13-pin-duplicate-exit.txt`.

The driver reaches this via `raise SystemExit(f"SETUP PIN_DUPLICATE path={path}")`
at `control-driver-r92.py:115` (inside `read_pins`). `SystemExit` with a **string**
message prints it to stderr and exits **1**. Contrast the driver's *other* setup
errors, which print to stdout and exit 2:

```
$ … --pins /nonexistent/pins.txt …
CONTROL_DRIVER_R92=SETUP missing /nonexistent/pins.txt
EXITCODE= 2   (STDOUT, stderr empty)
```

**Impact.** A wave seat or gate that scrapes stdout for `SETUP PIN_DUPLICATE` (the
claim names it as a *code*) sees nothing on stdout, and a seat that asserts exit 2
sees exit 1. Both are false negatives against the frozen text. The forgery battery
already asserts `rc=1` for this class (`forgeries-r92.py`, receipt `r3`), so the
battery and the claim disagree with each other.

**Smallest remediation.** Change line 115 to `print(f"SETUP PIN_DUPLICATE path={path}"); raise SystemExit(2)`,
and reconcile `claims.md:29` with the battery's `rc=1` expectation — or fix the
battery to expect 2. One of the two must move; the frozen text currently matches neither.

---

## F4 — MEDIUM — `verify` reads and scores files outside `--root`

The driver resolves `--expected`, `--receipts` and `--pins` against `HERE`
(the driver's own directory, lines 70–73) but then relativises them against
`--root` via `rel_for(root, path)` (line 149). When the driver lives outside
`--root`, that relativisation yields a `..`-prefixed path, and the subsequent
`os.path.join(os.path.abspath(root), rel)` **resolves outside `--root`**.

Demonstrated (receipt `r14-path-escape-rel_for.txt`):

```
root= /home/vgpnk/Projects/shokunin/chousa-shokunin
expected= /fast/scratch/…/repo/corpus/evidence/round92/controls/expected.tsv
rel_for(root,expected)= ../../../../../fast/scratch/…/repo/corpus/evidence/round92/controls/expected.tsv
rel escapes root: True
disk resolved= /fast/scratch/…/repo/corpus/evidence/round92/controls/expected.tsv
outside root: True      file exists: True
```

End-to-end, running the C5 driver **from the clone** while pointing `--root` at the
lane repo produces `CONTROL_DRIVER_R92=FAIL` with `INSTRUMENT_UNPINNED` and
`SELF_DRIFT` naming paths like
`../../../../../fast/scratch/hyaku/chousa-r92/R92SentinelScope/repo/corpus/evidence/round92/controls/expected.tsv`
(receipt `r9-verify-root-lane-repo-clone-driver.txt`, exit 1). The same invocation
with the driver taken from the tree *it names as root* passes (exit 0) — so the
failure is a base-mismatch artefact, not a defect in the bytes.

**Exploit path.** `rel_for` is the trust boundary between "the base a file was read
from" and "the base the path is resolved against". Because `rel_for` has no
containment check, a caller who supplies `--root A` while the driver's defaults
resolve under `B` makes the driver read `B`'s expectations/pins/receipts, then
`git show` them from `A`'s repo, then score the result as if it were `A`'s. A
concretely reachable case: `verify --root <checkout> --repo <other-checkout>` — the
"external root" form the dispatch text asks about — is *not* the failure here
(that form passes, exit 0, receipt `r1`/`r11` and my lane-repo run), but the
path-escape is one argument swap away and the driver has no guard.

**Impact.** Contained in the current wave (both bases point at the same bytes), but
the driver will happily score bytes from outside the tree it was told to verify, and
the resulting `PASS` would carry the wrong provenance.

**Smallest remediation.** In `rel_for`, reject any result that starts with `..`
(or, better, derive `expected`/`receipts`/`pins` from `--root` rather than `HERE`):
make the defaults `os.path.join(root, "corpus/evidence/round92/…")` and keep `HERE`
only for `__file__`.

---

## F5 — MEDIUM — pinned instruments are not byte-checked on disk (7 of 16)

`instrument-pins.txt` carries **16** pin rows. The on-disk byte-identity leg
(`pin_report`, `control-driver-r92.py:288–289`) builds its `wanted` set from the
scripts named by the *expected rows* plus the expectations and pins files — only
**7** paths. The other **9** pinned rows are never compared byte-for-byte against
the file on disk; they are only compared *as blobs at `--rev`* by the `SELF_PIN`
leg (`pin_at_rev`, line 314), which reads the commit, not the working tree.

Enumerated (receipt `r20-pin-coverage.txt`):

```
pins rows total = 16
on-disk byte-checked set (pin_report wanted) = 7
   CHECKED  corpus/evidence/round89/curation-r89-controls.py
   CHECKED  corpus/evidence/round89/curation-r89.py
   CHECKED  corpus/evidence/round89/gate-records-r89.py
   CHECKED  corpus/evidence/round89/mutate-r89.py
   CHECKED  corpus/evidence/round90/harm-recheck-r90.py
   CHECKED  corpus/evidence/round92/controls/expected.tsv
   CHECKED  corpus/evidence/round92/instrument-pins.txt
PINNED but NEVER on-disk byte-checked:
   UNCHECKED .ufo/waves/round-92/claims.json
   UNCHECKED corpus/evidence/round92/claims.md
   UNCHECKED corpus/evidence/round92/control-driver-r92.py
   UNCHECKED corpus/evidence/round92/controls/selftest-r92.txt
   UNCHECKED corpus/evidence/round92/curation-controls-r92.py
   UNCHECKED corpus/evidence/round92/curation-r92.py
   UNCHECKED corpus/evidence/round92/forgeries-r92.py
   UNCHECKED corpus/evidence/round92/skill-tally-r92-controls.py
   UNCHECKED corpus/evidence/round92/skill-tally-r92.py
```

**Exploit path / impact.** Tampering the on-disk copy of a pinned instrument is
accepted. I appended one comment line to `corpus/evidence/round92/curation-r92.py`
in a fresh clone and re-ran `verify`:

```
on-disk sha256 of tampered file:
22d7b095f9db5b48be044328a1aa8e1ae56fb31a2e3085aeb0a76105432efa42  …/corpus/evidence/round92/curation-r92.py
pin row:
81310bba8c8878e3cbb9026cd5a87f42fe0e79beb51ab8160c5adfc1ff644166  corpus/evidence/round92/curation-r92.py
--- verify ---
RECEIPT PINS OK 7/16 pinned files byte-identical
RECEIPT SELF_PIN OK rev=42e0337… receipts_rev=16ccf769…
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=7 CONTROL_DRIVER_R92=PASS
R12_EXIT=0
```
Receipt: `r12-ondisk-tamper-curation-r92.txt`. The tampered file's digest
(`22d7b095…`) differs from its pin (`81310bba…`) and `verify` still says `PASS`.

This matters because `curation-r92.py` and `skill-tally-r92.py` are the C2/C3
**counter instruments** — the bytes whose output the other two claims score. An
on-disk edit to the C2 counter is invisible to the C1 driver. The frozen claim's
rule 5 says "**EVERY** file a row's command names as its script (not just the
first) … its on-disk sha256 equals the pin", which the 7-path set satisfies
narrowly; but the pins table plainly *intends* 16 byte-bound files, and the
driver's own `SELF_PIN` leg covers `__file__` — so the driver's behaviour and the
pins table disagree about what "pinned" means.

**Smallest remediation.** In `pin_report`, add every path in `pins` to `wanted`
(not only the row-named scripts), so all 16 pins are byte-checked on disk; and
report `PINNED_FILES` as the count of pins actually checked (16), not the count of
`wanted` entries (7).

**Scope note for the round report.** `PINNED_FILES=7` must not be reported as
"16 pinned files verified". The printed line is `RECEIPT PINS OK 7/16 pinned files
byte-identical` — the honest reading is 7 on-disk byte-identity checks against a
16-row pins table, with the remaining 9 bound only as commit blobs.

---

## F6 — LOW — C2 controls summary line prints `PRIOR_REGRESSION=4/4`, not `7/7`

`claims.md:67` and `claims.json:80` freeze the controls summary as
`CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R91=1 DUPCOUNT_R92=1 PRIOR_REGRESSION=7/7`.

The actual final summary line (receipt `r5-c2-controls-real-path.txt`) is:

```
CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 CARRIED_F1_F4=refused-by-both DUPCOUNT_R91=1 DUPCOUNT_R92=1 PRIOR_REGRESSION=4/4
```

Two deviations: the summary carries an extra `CARRIED_F1_F4=refused-by-both` token
not in the frozen string, and its final field is `PRIOR_REGRESSION=4/4` where the
claim says `7/7`. The token `PRIOR_REGRESSION=7/7` **does** appear in stdout, but on
an earlier line — `OK regression: FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 rc=1` —
so a whole-stdout token check passes while the *summary* line does not match. The
source is `curation-controls-r92.py:200`, which hard-codes
`PRIOR_REGRESSION={'4/4' if reg_ok else 'FAIL'}`.

**Impact.** A seat that greps whole stdout passes; a seat that compares the summary
line, or reports "the controls print `PRIOR_REGRESSION=7/7`", is wrong. The claim
should say `PRIOR_REGRESSION=4/4` on the summary line and note that `7/7` appears on
the regression leg line — or the instrument should print the 7/7 count on the summary
line and move the 4/4 count elsewhere.

**Note (not a finding).** Round-91's summary line reads
`… DUPCOUNT_R90=2 DUPCOUNT_R91=1 PRIOR_REGRESSION=7/7`; r92 drops `DUPCOUNT_R90` and
repurposes `PRIOR_REGRESSION` for the r91 regression count. The r91→r92 drift is
real, and the frozen text was frozen against the wrong shape.

---

## F7 — LOW — `c1-harm` row overrides the scrubbed environment's HOME

`corpus/evidence/round92/controls/expected.tsv:4` (the `c1-harm` row) reads:

```
mkdir -p @WORK@/harm && HOME=/home/vgpnk git -C @ROOT@ show 265b8633…:tools/gate-records.py > @WORK@/harm/base-tool.py && …
```

The driver's `scrub_env` (line 196) builds `{PATH, HOME}` with `HOME` = the tree
root, deliberately ("no rc/profile reads"). This row re-introduces the operator's
real `HOME=/home/vgpnk` for the `git` call, so the fresh leg reads
`/home/vgpnk/.config/git/config` — which contains, among other settings,
`credential.https://github.com.helper=!/home/vgpnk/.local/bin/gh auth git-credential`
(receipt `r18-home-override-row.txt`). The git invocation here is `git show` on a
local object (no network, no credential use), so nothing is exfiltrated in this
round's flow; the risk is that the pinned row establishes a precedent under which a
`HOME` override could expose host git config to a scored leg.

**Smallest remediation.** Replace `HOME=/home/vgpnk` with nothing (git works with the
scrubbed `HOME`), or with `HOME=@WORK@/home` and `mkdir -p` it first; then re-emit
the six receipts and regenerate the pins table.

---

## F8 — LOW — byte-identical alias instruments, pinned but unreferenced

`corpus/evidence/round92/tally-r92.py` and `tally-controls-r92.py` are byte-identical
copies of `skill-tally-r92.py` and `skill-tally-r92-controls.py`
(`cmp -s` reports identical for both pairs). They were added at the F1 freeze
(`bf12c30e`, the superseded pair) and carried forward to C5 unchanged. They are
referenced by nothing: `git grep` finds no reference to `tally-r92.py` /
`tally-controls-r92.py` in `corpus/`, `plans/`, `tools/`, `SKILL.md` or
`.ufo/waves/round-92/`; `instrument-pins.txt` pins the `skill-tally-*` names only.
`corpus/evidence/round92/after/` exists in the working tree but is empty and
gitignored at C5.

**Impact.** Dead weight in the evidence tree; two extra pinned-looking files a
reviewer or an automated digest sweep must reason about. Low risk, but it is the
kind of alias that later becomes a second scoring path.

**Smallest remediation.** Delete both aliases at the next freeze (they are not
pinned by name, so removing them does not disturb the pins table's minus-self
digest — but re-verify the pins file afterwards, since `instrument-pins.txt` is
itself a pinned path).

---

## F9 — INFO — the plan's `narrowing` pointer target does not exist

`plans/round-92.md` opens with:
> "A `narrowing` cell in `.ufo/waves/round-92/claim-falsification.tsv` resolves to a section here."

`.ufo/waves/round-92/claim-falsification.tsv` does not exist in the lane working tree
or at C5 (`git ls-tree -r 16ccf769… .ufo/waves/round-92/` lists only `claims.json`).
The plan also states its Amendments section is "(None yet)", so nothing currently
routes there — but the closure step is instructed to read that file, and it will not
be there.

**Smallest remediation.** Either commit the falsification table at the next freeze
or amend the plan's opening sentence to name the file that exists.

---

## F10 — INFO — the cited before-receipts are absent at C5

`plans/round-92.md:35` says "Before receipts land in
`corpus/evidence/round92/controls/receipts/c{1,2,3}-before.txt`"; `claims.md:119`
cites `controls/receipts/c3-before.txt` "emitted by the r92 battery"; and
`claims.json` cites `receipts/c1-before.txt`, `receipts/c2-before.txt`,
`receipts/c3-before.txt` as the before-states. None of the three exists at F5 or at
C5 (`git cat-file -e` on each path → absent); the r92 receipts directory holds only
the six committed control receipts.

**Impact.** The "before" evidence for C1/C2/C3 is asserted by citation but not
present in the tree, so a reader cannot check the before-state without re-deriving it.
Round-91's equivalents (`corpus/evidence/round91/controls/receipts/c{1,2,3}-before.txt`)
do exist, which makes the gap easy to miss.

**Smallest remediation.** Emit and commit the three before-receipts at the next
freeze, or amend the citations to name the round-91 files that do exist.

---

## Checklist results (everything the assignment asked me to run)

### 1. Every command form printed in the wave context, run verbatim on correct bytes

| # | Form | Result | Receipt |
|---|------|--------|---------|
| a | `control-driver-r92.py verify --root . --repo . --rev 42e0337… --receipts-rev 16ccf769… --work <scratch>` | **PASS** exit 0, `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6`, `CONTROL_DRIVER_R92=PASS` | `r1-verify-clone.txt` |
| b | same, `--root /home/.../chousa-shokunin --repo <clone>` (driver taken from the clone) | **FAIL** exit 1 — path-escape artefact of the base mismatch (F4) | `r9-verify-root-lane-repo-clone-driver.txt` |
| b' | same, `--root . --repo <clone>` run from the lane repo itself | **PASS** exit 0 | (same command, exit 0; see F4) |
| c | `control-forgeries-r92.py --work <scratch>` (claim-named) | **exit 2**, file not found (F1a) | `r2-forgery-claim-path.txt` |
| c' | `forgeries-r92.py --work <scratch>` (real path) | `FORGERY_REFUSED=3/3 POSITIVE=pass`, exit 0 | `r3-forgery-real-path.txt` |
| d | `curation-r92.py --root .` | `CURATION_R92=PASS`, exit 0, all ten claimed fields present | `r4-c2-counter.txt` |
| e | `curation-r92-controls.py --root . --work <scratch>` (claim-named) | **exit 2**, file not found (F1b) | `r6-c2-controls-claim-path.txt` |
| e' | `curation-controls-r92.py --root . --work <scratch>` (real path) | `CONTROLS=PASS`, exit 0; summary line deviates (F6) | `r5-c2-controls-real-path.txt` |
| f | `skill-tally-r92.py --root . --selftest corpus/evidence/round92/controls/selftest-r92.txt` | `SKILL_TALLY_R92=PASS`, exit 0, all eleven claimed fields present | `r7-c3-counter.txt` |
| g | `skill-tally-r92-controls.py --root . --work <scratch>` | `CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1`, exit 0 | `r8-c3-controls.txt` |

Every frozen predicate token in `.ufo/waves/round-92/claims.json` is **present** in
the corresponding real-path output: C1 `verify_stdout` + `verify_fields` all present;
C2 `counter_stdout` + `counter_fields` all present; C2 `controls_stdout` all present
(`PRIOR_REGRESSION=7/7` present on the regression leg line — see F6 for the summary-line
deviation); C3 `counter_stdout` + `counter_fields` all present; C3 `controls_stdout`
all present. **No claim predicate is falsified**; the defects are in the frozen
*dispatch text* (F1, F2, F3, F6), in the driver's write/pin scope (F4, F5), and in
housekeeping (F7–F10).

### 2. `verify` never writes under `controls/receipts/`; `--work` is the only write root — **HELD**

- sha256 of all six receipt files **before and after** a `verify` run: identical
  (`sha256sum -c` → 6× `OK`, exit 0). Receipt `r11-receipts-write-scope.txt`.
- Whole-tree hash (24 636 files, `.git` excluded) before vs after `verify`:
  **`TREE_IDENTICAL`** (empty `diff`). Same receipt.
- All writes observed land under `--work`: `fresh-<case>.out` ×6 plus the instruments'
  own scratch (`w4/c1gate/legs/*`, `w4/harm/base-tool.py`, …).
- The C2 counter, the C3 counter and the C3 controls battery each leave the tree
  byte-identical (`C2_COUNTER_TREE_UNCHANGED`, `C3_COUNTER_TREE_UNCHANGED`,
  `C3_CONTROLS_TREE_UNCHANGED`).
- The C2 controls battery symlinks `corpus/captures` and `corpus/evidence/round57`
  into its scratch mirror (`curation-controls-r92.py:60–63`), so I checked for
  write-through into the live tree: sha256 of 308 files under `corpus/knowledge`,
  `corpus/captures`, `corpus/evidence/round57` before vs after the battery →
  **`LIVE_TREE_UNCHANGED_BY_C2_CONTROLS`**, and `git status --porcelain -- corpus/`
  is empty. The symlinks are read-only in this flow.
- **Caveat:** the `emit` mode is *not* covered by this guarantee — see F2, where
  `emit` without `--receipts` overwrites the committed receipts in the tree.

### 3. No path escapes / network calls / host mutations — three hits, all benign or explained

Grep over the three instruments (`control-driver-r92.py`, `curation-r92.py`,
`skill-tally-r92.py`) for `/tmp`, absolute writes, `HOME`, `urllib|socket|http`,
`sysctl|sudo|systemctl` — receipt `r17-grep-path-network-host.txt`:

- `control-driver-r92.py:196` — `env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.path.abspath(root)}`:
  the scrubbed-env construction. `HOME` is the tree root, not the operator's home.
  Benign by design; but see F7 for the row that overrides it.
- `control-driver-r92.py:364` — `--work` default `os.environ.get("TMPDIR") or "/fast/scratch/hyaku"`:
  no `/tmp`, no host path. Benign.
- `control-driver-r92.py:388,391,398,443` — `os.makedirs(work)` / `os.makedirs(a.receipts)` /
  `open(a.receipts/<case>.txt,"w")` / `open(fresh_file,"w")`: the `emit` write path (F2)
  and the `verify` fresh-output write (bounded by `--work`).
- `curation-r92.py:125` — `re.findall(r"https?://[^\s|)>\]]+", cells[1])`: a **regex
  over text already in the corpus**, not a network call. Benign.
- `subprocess` use is confined to `bash -c` (line 201), `git show` (lines 314, 330, 345)
  and `bash tools/research-gate.sh --selftest` (`skill-tally-r92.py:58`).
- **No** `urllib`, `requests`, `socket`, `urlopen`, `sysctl`, `sudo`, `systemctl`,
  `os.system`, `eval`, `exec` in any of the three instruments.
- The path-escape in F4 is *not* visible to this grep because it is constructed at
  runtime by `rel_for` (line 149) — grep for `rel_for`/`os.path.join` is what surfaced it.

### 4. The claim's self-pin reading vs `PINNED_FILES=7` and 16 pins — **must not be overstated**

The printed line is `RECEIPT PINS OK 7/16 pinned files byte-identical` and
`PINNED_FILES=7`. The correct reading: **7** on-disk byte-identity checks are
performed against a **16**-row pins table; the other 9 pinned paths are bound only as
blobs at `--rev` (or, for the driver, via the `SELF_PIN` byte-compare against its own
blob), never against their working-tree bytes. See F5 for the enumeration and the
tamper demonstration. A report that says "16 pinned files verified byte-identical"
would be wrong; a report that says "7 of 16 pins byte-checked on disk; the other 9 are
commit-blob-bound" is right. The claim's rule 5 wording ("EVERY file a row's command
names as its script … its on-disk sha256 equals the pin") is satisfied narrowly by the
7-path set, so this is a scope-of-the-pin finding, not a predicate falsification.

### 5. Credential / secret shapes at the carrier — **none**

```
git grep -nE 'sk-|ghp_|AKIA|BEGIN [A-Z ]*PRIVATE KEY' 16ccf769… -- . | wc -l   → 2594
strict shape (word-anchored, real key lengths)                                 → 0
```
Receipt `r19-credential-shapes.txt`. The 2 594 loose hits are all substring false
positives in ordinary prose/paths — e.g. `mask-confuser-probe.txt`, `task-result.json`,
`arena-task-spec-audit.md` — and two binary corpus captures under `corpus/captures/`.
No `sk-…`/`ghp_…`/`AKIA…`/`BEGIN … PRIVATE KEY`/`xox…`/`AIza…`/`sk-ant…` shape occurs.
`git grep -c` for the strict pattern returns **0** files.

### 6. Nothing changed between F5 and C5 except the six receipts — **HELD**

```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --name-only \
      42e0337822a508208800f98faa3a63c6af9f8c27 16ccf7693c61b8ffe392fc757352304f239bfcad
corpus/evidence/round92/controls/receipts/c1-gate-r89.txt
corpus/evidence/round92/controls/receipts/c1-harm-setup.txt
corpus/evidence/round92/controls/receipts/c1-harm.txt
corpus/evidence/round92/controls/receipts/c1-mutants-r89.txt
corpus/evidence/round92/controls/receipts/c2-prior-controls.txt
corpus/evidence/round92/controls/receipts/c2-prior-landing.txt
EXIT=0
```
Receipt `r10-diff-f5-c5.txt`. Exactly six paths, all under
`corpus/evidence/round92/controls/receipts/`, all `computed_against=42e0337…` at C5
(they read `computed_against=007d7ea7…` at F5 — the receipts were re-emitted against
the F5 freeze, exactly as the plan's repair history describes). `SKILL.md` is unchanged
F5→C5 and base→F5; `tools/` is unchanged base→C5 (`git diff --name-only … -- tools/`
is empty), consistent with the dispatch statement that `tools/research-gate.sh` and
`tools/gate-records.py` did not change this round.

### 7. S070 re-opened (local, no network)

`man -P cat 1 sha256sum` → `SHA256SUM(1)  User Commands  SHA256SUM(1)` / "NAME
sha256sum - compute and check SHA256 message digest" / "DESCRIPTION Print or check
SHA256 (256-bit) checksums.  Legacy interface to the cksum(1) utility." The frozen
quote "Print or check SHA256 (256-bit) checksums." is present verbatim in the
installed page. This grounds rule 5's digest check and the S5 minus-self digest,
which the driver implements at `control-driver-r92.py:197–204`
(`pins_file_sha_minus_self`) and `:340–352`. No fetch was performed; `egress.tsv`
at C5 records "none — no fetch this round", which matches what I observed.

---

## Scope and safety of what I did

- **Read-only against production.** I wrote only under
  `.ufo/waves/round-92/w1/` (this report and `receipts/R92SentinelScope/`) and under
  my scratch dir. The lane repo's `git status --porcelain -- corpus/` is empty; no
  tracked file was modified. All tamper experiments were performed on **copies**
  (`git archive … | tar -x -C $D`) or on a **separate clone** (`$S/fx-clone`), never
  on the lane checkout.
- **Fixture git hygiene.** The one fixture I created as a repo (`$S/fx-clone`) was
  created with `git clone --shared`, and I asserted
  `test "$(git -C "$T" rev-parse --show-toplevel)" = "$T"` before the mutating
  `checkout`/`append`.
- **No `sudo`, no sysctl, no service restart, no host mutation, no network.**
- **Scratch removed.** `/fast/scratch/hyaku/chousa-r92/R92SentinelScope` was deleted
  before this report was finalised; every receipt cited above is copied into
  `.ufo/waves/round-92/w1/receipts/R92SentinelScope/`.

---

VERDICT: R92SentinelScope C1 fired — the claim's own counting commands name two files that do not exist at C5 (`control-forgeries-r92.py`, `curation-r92-controls.py`), and its frozen rules 6 and 8 (`PIN_DUPLICATE` exit 2, `emit` requires an explicit `--receipts`) are not implemented, though the verify predicate itself passes.
VERDICT: R92SentinelScope C2 fired — the claim's controls counting command names a non-existent file and its frozen summary line prints `PRIOR_REGRESSION=4/4` with an extra `CARRIED_F1_F4` token, though the counter and controls predicates are met at the real paths.
VERDICT: R92SentinelScope C3 held — both C3 counting commands run verbatim on correct bytes and every frozen predicate token is present, with no path, network, host-mutation or secret exposure found in the C3 instruments.
