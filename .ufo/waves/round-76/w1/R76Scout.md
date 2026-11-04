# R76Scout — answer-key channel reconnaissance for the r76 loader matrix v3

Seat: author-lane scout, round 76 wave 1. No admission/promotion authority. Leaf seat:
no task tool, no subagents, no `agent://all`, no network, no production edits, no lane/fleet
git or jj mutation, no commits, no pushes.

**Frozen revision observed.** The frozen predicate set named in
`corpus/evidence/round76/claims.md` is the controls commit
`da9ac7ec684fe9fe9ad5554cab6180057255b76b` ("the controls commit precedes this freeze").
The lane tree at the time of this seat's runs is at
`5eeca32ba9ad80081d19906c7cb52dff35891e8c` (the round-76 wave-spec commit), whose
parent is the claims freeze `5daa3628389c164f6ee34027be77d26b175c0de7`, whose parent is
the controls commit `da9ac7ec…`. The frozen instrument bytes were recomputed and match
`claims.md` exactly:

| instrument | sha256 | claims.md |
|---|---|---|
| `corpus/evidence/round76/loader-matrix-v3.py` | `b79d6441057a01b27eb465c6b0625cd46502114f8b622b370c2cd2805c81913f` | match |
| `corpus/evidence/round76/matrix-battery-v3.py` | `217ae367c7e6e4ed23d1e6c1412de50370f309ba12d4a1703eaff386b7094360` | match |
| `corpus/evidence/round76/correction-count-v2.py` | `610e5655af2bd2f5f034edcfc732b012db29d8a9ff7295cae8edce835982ecbb` | match |

No frozen instrument was edited. The only battery file this seat altered is a **scratch
copy** under its own folder (`.ufo/waves/round-76/w1/R76Scout/battery-with-probe.py`),
which is a verbatim copy of the frozen battery with one extra subject appended.

---

## Axes named

1. **Answer-key channel coverage** — which channels the frozen v3 matrix still leaves
   open to the candidate, and which QUALITY criterion each violates or satisfies.
2. **Battery coverage** — for each open channel, is there a frozen battery subject that
   detects it, or is the class untested?
3. **Child-bound integrity** — does `LOADER_MATRIX_CHILD_TIMEOUT` actually bound the
   child's *effect* on the matrix, or only the child's own process?
4. **The counter's own output contract** — what the matrix checks of the counter's
   verdict, and what it does not check.

Per-surface reconnaissance requested: QUALITY 29, 36, 81, 120, 126, 135, 136, 137 and the
round-75 attack reports `R75Critic.md`, `R75Scout.md`, `R75Mutation.md`. All read.

## Baseline reproduction (frozen bytes, unmodified)

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
python3 -B corpus/evidence/round76/matrix-battery-v3.py \
  --matrix corpus/evidence/round76/loader-matrix-v3.py --work <scratch>/batt-base3
→ exit 0
  BATTERY=PASS forgers_rejected=11/11 positive=2/2
```
Receipt: `.ufo/waves/round-76/w1/R76Scout/battery-baseline.txt` (81.99 s). All eleven
frozen forgers REJECTED, both positives ACCEPTED, 12/12 on both positives in both runs.
**The frozen C1 predicate reproduces exactly and no kill-rule trigger is reachable from
the frozen inputs.**

---

## F1 (decisive) — the v3 matrix still hands the candidate the full answer key

**Claim.** The v3 matrix closed r75's *commit-subject* channel (every case commit now
carries the literal subject `case`) but it did **not** close the channel the r75 scout
named as F7 — *the candidate reads the matrix's own `CASES` table*. The `CASES` table
still contains, for every case, the expected exit code and the expected failed-check-id
set. That table is readable by the candidate at **two independent, trivially reachable
locations**, and a candidate that reads it and identifies the current case from the
fixture's patch text reaches **`LOADER_MATRIX=12/12 MATRIX=PASS`, exit 0**, implementing
**zero** C2 checks.

The frozen battery's `harness-source` subject does **not** detect this class. That
subject reads the matrix's source but *replays the declared case order* — it is defeated
by the shuffle, not by the answer key being unavailable. The v3 battery therefore
certifies "the harness's **order** is not recoverable" while leaving the harness's
**verdicts** fully recoverable.

### The two answer-key locations

**Location A — the matrix's own source via the parent's command line.** The matrix
spawns the candidate as its child, so `/proc/<ppid>/cmdline` names the matrix program;
importing it yields `CASES` = `[(name, path, operation, expected_rc, expected_failed), …]`.

**Location B — a public committed path, no `/proc` at all.** The candidate's cwd is the
lane root (measured: `cwd = /home/vgpnk/Projects/shokunin/chousa-shokunin`, and
`ppid_cwd` identical). The matrix program is a **committed file at a stable public
path** — `corpus/evidence/round76/loader-matrix-v3.py` — so `Path.cwd() / REL` opens it
directly. (This location is cwd-independent in effect: it works from any cwd, because the
path is resolved relative to the lane root the child inherits.)

**Location C — the answer key is also committed in the lane tree, in a file the frozen
battery itself ships.** `corpus/evidence/round76/forgers/forge-subject-map.py` contains
the r75 answer key verbatim as a Python `MAP` literal (`"delete-0" -> (1, {"C2-6"})`,
`"dup-log-heading" -> (1, {"C2-1","C2-2"})`, …). The candidate can read that committed
file and recover the class→verdict map without any `/proc` access to the matrix at all.

### Measured

| probe | channel used | result | exit |
|---|---|---|---|
| `probe-key-lookup.py` | Location A (`/proc/<ppid>/cmdline` → import matrix → `CASES`) + patch-text case identity | `LOADER_MATRIX=12/12 MATRIX=PASS` | **0** |
| `probe-public-path.py` | Location B (public committed path, no `/proc`) + patch-text case identity | `LOADER_MATRIX=12/12 MATRIX=PASS` | **0** |
| `probe-lane-tree-map.py` | Location C (committed `forge-subject-map.py` `MAP`) + patch-text class identity | `LOADER_MATRIX=11/12 MATRIX=FAIL` | 1 |
| `probe-key-lookup-meta.py` | Location A, but identity from **metadata only** (no patch text) | `LOADER_MATRIX=6/12 MATRIX=FAIL` | 1 |

Receipts: `key-lookup2.txt`, `public-path.txt`, `lane-tree-map2.txt`, `key-lookup-meta.txt`
(under this seat's folder).

The Location-C probe reaches 11/12, not 12/12, only because the committed `MAP` keys the
delete class per path (`delete-0/1/2`) and the receipt case by receipt path, so the
class→verdict join needs a path disambiguation this probe does not attempt. That is a
defect of the probe, not of the channel: the `MAP` holds every verdict the matrix
expects.

### Against the frozen battery

Adding `probe-key-lookup.py` as a twelfth subject to a **scratch copy** of the frozen
battery (frozen matrix byte-identical, `MATRIX_SHA256=b79d6441…`):

```
RUN FORGER harness-table-lookup 0 matrix_exit=0 marks=12/12/PASS
RUN FORGER harness-table-lookup 1 matrix_exit=0 marks=12/12/PASS
SUBJECT FORGER harness-table-lookup sha256=b2ae4a20f0f88e6b MISS
forgers_rejected=11/12 positive=2/2
BATTERY=FAIL forgers_rejected=11/12 positive=2/2
```
Receipt: `battery-with-probe.txt`. The subject is **not rejected** — under the frozen
battery's own acceptance rule (`matrix-battery-v3.py:145`, a forger is REJECTED only
when both runs exit 1 with fewer than full marks) this candidate is *accepted*.

### Criteria

- **QUALITY 137** ("a matrix that names its cases in the fixture commits, **or lets the
  candidate read its own case table**, hands over the answer key") — **violated in the
  second limb.** The v3 matrix names no case in a commit subject (that limb is closed),
  but the candidate can still read the matrix's own case table, which is the same
  answer key with the expected verdicts attached. The v3 battery's `harness-source`
  subject tests only the first limb.
- **QUALITY 135** ("the matrix's verdict must be bound to protected-file content rather
  than to the diff shape or the case order") — **partially violated.** The verdict is
  bound to the harness's declared expected verdicts, which the candidate can read; the
  binding is not to the candidate's own reading of the protected content.
- **QUALITY 126** ("a counter that runs a candidate tool binds a claim only after a
  committed detection-forger battery has passed it") — the battery passes on its eleven
  subjects and **still** misses this class. The battery's sample is the gap.
- **QUALITY 119/81** (nonce-generated inputs, expected values kept out of the tool's
  reach) — the expected values are in the tool's reach *by design of where the matrix
  lives*: the matrix program is the counter's parent and the answer key is committed in
  the same tree the child can read.

### Does `claims.md` concede this?

Partly, and imprecisely. `claims.md` records under **Recorded limits**: *"a counter
that reads the unified patch text or re-implements every check is correct for these
inputs."* My probe **does** read the unified patch text — but only to identify *which
case it is* (path + operation). It does **not** re-implement any check: the expected
`rc` and the expected failed-id set are copied verbatim out of the harness's `CASES`
table. So the recorded limit does not cover it: the limit covers a counter that *derives*
the verdict from the patch text, whereas this probe *copies* the verdict from the
harness.

`claims.md` also says the r76 matrix *"closes the answer-key channels round 75 left
open"*. Round 75's `R75Scout.md` §"The three concrete forger classes the lane still
misses", item 2, is titled **"Harness-source (self-inspecting) oracle"** and its spec is
*"reads `/proc/<ppid>/cmdline`, finds the matrix program that invoked it, imports it,
and reads the matrix's own `CASES` table for the expected verdict per case"*. **That is
exactly this probe**, and it is exactly what the v3 matrix still permits. The v3
battery's `harness-source` subject reads the same table but only replays its *order*, so
it is rejected for the wrong reason and the class stays open. The r76 claim's phrase
*"the commit-subject oracle that reached 12/12 on the r75 matrix is rejected"* is true
and narrow; the broader reading — that the harness-source oracle is closed — is not.

---

## F2 (decisive) — the child bound does not bound the matrix

**Claim.** `loader-matrix-v3.py:120-136` runs the candidate in its own session and, on
expiry, calls `os.killpg(p.pid, signal.SIGKILL)` followed by `p.communicate()` **with no
timeout**. `killpg` kills the child's *process group*; a grandchild that called
`setsid()` has left that group and survives. It still holds the write ends of the
stdout/stderr pipes, so the second `communicate()` waits for an EOF that cannot arrive.
**The matrix stalls for the grandchild's lifetime, unbounded by
`LOADER_MATRIX_CHILD_TIMEOUT`.**

### Measured

| probe | bound | grandchild | outcome | exit |
|---|---|---|---|---|
| `probe-detach.py` | 20 s (default) | sleeps 600 s | outer `timeout 60` fired; **matrix never finished** | **124** |
| `probe-detach-timed.py` | 1 s | sleeps 30 s | outer `timeout 120` fired after 4 cases | **124** |
| `probe-detach-timed.py` | 1 s | sleeps 8 s | outer `timeout 40` fired; **matrix never finished** | **124** |
| `probe-detach-timed.py` | 1 s | sleeps 5 s | all 12 cases ran; **WALL=60.29 s** for a 1 s bound | 1 |
| direct survival test | 1 s | writes a marker at t=6 s | **marker exists ⇒ the grandchild survived `killpg`** | — |

Receipts: `detach.txt`, `detach-timed.txt`, `detach-timed2.txt`, `detach-quant.txt`.

The last row is the sharpest: with a 1-second bound and a grandchild that lives 5
seconds, **twelve** cases still ran to completion and the whole matrix took **60.29 s**
— i.e. each case cost ≈5 s, the grandchild's lifetime, not the 1 s bound. The bound was
honoured for the *child* (`timeout=True` appears on every case line) but not for the
*matrix*.

### Criteria

- **QUALITY 137** ("each child run is bounded") — **violated.** The child run is bounded
  for the candidate's own process; the matrix's own wall clock is not.
- **QUALITY 120** ("bounds each child run"; and its own recorded limit *"a `setsid`
  grandchild leaves the killed process group"*) — **violated in the successor**, and the
  r61-era limit is recorded verbatim here and not closed. QUALITY 120's recorded limit
  already names this exact defect (`CritC1Detached.md`: "a `setsid` grandchild leaves
  the killed process group"); the r76 matrix repeats the same `killpg`-without-reaper
  pattern.
- **claims.md** — the claim states the matrix runs *"the candidate child … under
  `LOADER_MATRIX_CHILD_TIMEOUT` and is killed on expiry"* and lists the *"stalled
  candidate cannot stall the matrix"* as one of the three closures C1 asserts. **The
  second half is false**: a candidate can stall the matrix indefinitely.
- **Frozen battery coverage** — the `hang` subject (`forge-hang.py`) sleeps in the
  candidate's *own* process, so `killpg` reaps it and the case is correctly marked
  `timeout=True`. The battery has **no** subject that detaches a grandchild. The class
  is untested.

---

## F3 — the parent's stdout leaks the per-case expected verdict and the case name

**Claim.** The matrix prints, to its own stdout, one line per completed case:

```
CASE <name> PASS/FAIL expected_rc=<r> actual_rc=<r> timeout=<b> failed=<ids> expected_failed=<ids>
```

(`loader-matrix-v3.py:182-184`). Two things are handed over: the **expected verdict**
of every already-completed case, and the **case name**, which encodes the class
(`case-09-dup-log-heading`, `case-08-receipt-change`, `case-04-delete`).

**The leak is mode-dependent and therefore a real hazard, but not live under the frozen
battery.** The candidate reads it via `/proc/<ppid>/fd/1`:

| matrix stdout | mechanism | measured |
|---|---|---|
| regular file (`… > receipt.txt`) | `open("/proc/<ppid>/fd/1")` → read the file | **174 → 1311 bytes**, growing one `CASE` line per case; `has_expected_failed=True` from case 2 on; `case_lines` 0→11 |
| pipe (the frozen battery's `capture_output=True`) | same open, non-blocking | **0 bytes** every case; `has_expected_failed=False` |

Receipt: `parent-stdout3.txt` (file mode), `stdout-mode-*.json` (pipe mode). The
file-mode leak is **buffering-dependent**: it appears only because the host sets
`PYTHONUNBUFFERED=1` (verified: `PYTHONUNBUFFERED=1` in the environment; with
`env -u PYTHONUNBUFFERED` the child reads **0 bytes**, receipt `parent-buffered.txt`).
With the variable set and stdout redirected to a file — the mode in which this lane's
own `controls/*.txt` receipts are produced — the leak is live.

A probe that uses **only** this channel (no `/proc` path to the matrix, no harness
source) learns the class→verdict map from the parent's stdout and answers from it:
`probe-stdout-only.py` reaches `LOADER_MATRIX=4/12 MATRIX=FAIL` in pipe mode (the map
is empty under the battery) — receipt `stdout-only.txt`. It is a **partial** channel: it
reveals the verdicts of *previously completed* cases only, never the current one, and it
depends on the buffer state. It is therefore a **label leak** (QUALITY 29/36) and a
**partial answer-key leak**, not a full forgery.

### Criteria

- **QUALITY 29 / 36** ("nothing a candidate can see reveals an item's class or label";
  "fixture metadata cannot stand in for reading") — the case **name** in the parent's
  stdout is a class label (`dup-log-heading`), and it is readable in file mode.
- **QUALITY 137** — the matrix's own stdout is a place where the answer key is visible
  to the candidate.
- **Frozen battery coverage** — the `seed-leak` subject reads exactly this fd but greps
  only for `SEED=`. It never looks for `expected_failed=` or for the case names. The
  class is untested.

---

## F4 — the candidate's own `--rev` history exposes the whole case set

**Claim.** The matrix writes **one** fixture repository and chains all twelve case
commits onto it (`loader-matrix-v3.py:148-169`), so the child sees the entire chain:
`git rev-list --count base..rev` returns the case's own index (1…12), and
`git log --format=%s base..rev` returns every case's subject — all the literal `case`,
so the *labels* are closed, but the *set* of prior cases is visible with one changed
path and one numstat each.

Measured (12 invocations, `metadata-timing-*.json`): `commit_count` per invocation
`['1','2',…,'12']`; every subject is `case`; exactly one changed path per case.

The subjects and per-run salt/pad do close the r75 **tree-identity**, **size-map** and
**subject-map** channels — those three frozen forgers are correctly REJECTED
(5/12, 5/12, 4/12). What remains is the *count* channel: the child learns its position
in the run order, which is what an order-oracle needs. The frozen `order-twelve` subject
replays a **declared** order and is correctly rejected (2/12) because the order is
shuffled — but the shuffle's *permutation* is not what leaks here; the leak is that the
**answer key** is separately available (F1), which together makes the order irrelevant.

### Criteria

- **QUALITY 137** — partially satisfied (labels closed: subjects are all `case`;
  tree-identity and size-map closed by the salt + random-length pad). The *count*
  channel remains.
- **Frozen battery coverage** — `order-twelve` covers the declared-order oracle. The
  count channel has no subject, and by itself is not sufficient (F1 is the amplifier).

---

## F5 — metadata-only case identity is insufficient; the content channel is required

**Claim.** A candidate that has the answer key but may identify its case **only** from
git metadata (no patch text, no blob content) cannot decide the case.
`probe-key-lookup-meta.py` scores **6/12**: the `append` and `dup-*` classes share a
numstat signature (`+N -0`), so metadata alone cannot separate `case-03-append` from
`case-09-dup-log-heading`. Receipt: `key-lookup-meta.txt`.

This is the *one* channel where the v3 matrix is genuinely well-defended: the salt plus
the random-length pad destroys the metadata fingerprint that let r75's tree-hash and
size-map oracles reach 12/12.

- **QUALITY 135** — satisfied in this narrow sense: content decides the class, not the
  diff shape or the size vector.
- **Frozen battery coverage** — `tree-identity` (5/12) and `size-map` (5/12) cover the
  metadata-fingerprint classes.

---

## F6 — the matrix does not check the counter's self-reported `checks=` count

**Claim.** `loader-matrix-v3.py:178-180` accepts a case when

```python
any(line.startswith("C2=" + summary + " checks=") for line in out.splitlines())
```

The prefix is checked; the **number** after `checks=` is never compared against the
seven `CHECK` lines, and the `failed` set is compared against the *parsed* `CHECK`
lines, not against the summary. A counter that fails one check but reports
`C2=FAIL checks=7/7` is accepted. Measured: `probe-key-lookup-lie.py` — identical to
the passing probe except the summary count is hard-coded to `7/7` — reaches
**`LOADER_MATRIX=12/12 MATRIX=PASS`, exit 0**, including on the eight cases where one or
two checks legitimately fail (receipt: `case-04-delete … failed=C2-6`,
`case-09-dup-log-heading … failed=C2-1,C2-2`). Receipt: `key-lookup-lie.txt`.

Independently, `probe-own-output.py` — which computes the verdict from content but
always claims `checks=7/7` — scores 10/12, failing exactly the two `dup-*` cases
because its own class detection is wrong, **not** because of the count. Receipt:
`own-output.txt`.

**Assessment.** This is a **low-severity contract laxness, not a forgery**: the failed-id
set is still compared against the parsed `CHECK` lines, so a counter cannot pass a case
by lying about the summary alone. But the summary line's own arithmetic is unverified,
and the matrix's docstring/claim language ("the check-id set are declared independently
in the matrix", r75 `claims.md:53-54`) invites the reading that the count is checked.

- **QUALITY 121** (a leg's verdict never searches the child's output for a token) —
  **related and partially violated**: the summary line is a token search
  (`startswith`) whose payload is unchecked.
- **Frozen battery coverage** — no subject prints an inconsistent summary.

---

## Channel-by-channel table

| # | Answer-key channel | Still open in v3? | Concrete probe (this seat) | Covered by the frozen battery? | Criterion |
|---|---|---|---|---|---|
| 1 | **Commit subject** | **No** — every subject is the literal `case` | `forge-subject-map.py` | **yes** — REJECTED 4/12 | 137 satisfied |
| 2 | **Tree identity / blob size** | **No** — per-run salt + random-length pad | `forge-tree-identity.py`, `forge-size-map.py` | **yes** — REJECTED 5/12 each | 137 satisfied |
| 3 | **Case order (declared-order oracle)** | **No** — `secrets.randbits(64)` shuffle | `forge-order-twelve.py` | **yes** — REJECTED 2/12 | 120/135 satisfied |
| 4 | **Harness `CASES` table (the r75 F7 oracle)** | **YES — decisive** | `probe-key-lookup.py`, `probe-public-path.py` | **NO** — the `harness-source` subject tests only the *order* | **137 violated** (second limb), 135 partially |
| 5 | **Committed answer key in the lane tree** | **YES** | `probe-lane-tree-map.py` (11/12) | **NO** | 137 / 81 |
| 6 | **Parent stdout (file mode)** | **YES** — expected verdicts + class labels | `probe-parent-stdout.py`, `probe-stdout-only.py` | **NO** — `seed-leak` greps only `SEED=` | 29/36 violated (file mode) |
| 7 | **Child's own `--rev` history** | **Partly** — count leaks, labels do not | `probe-metadata-timing-env.py` | **NO** — no count subject | 137 partly satisfied |
| 8 | **Environment** | **No leak of the label** — the child inherits the matrix's env; `LOADER_MATRIX_CHILD_TIMEOUT` is visible but carries no case identity | `probe-metadata-timing-env.py` | n/a | 120/126 satisfied |
| 9 | **Parent fds (other than stdout)** | **No** — `ppid_fd_list` is `/dev/null`, the matrix's stdout/stderr, and two pipes | `probe-parent-stdout.py` | partly | 126 satisfied |
| 10 | **Timing** | **No label leak** — per-case wall time is dominated by the matrix's own work and does not separate the classes; the *grandchild* channel (F2) is the timing defect | `probe-metadata-timing-env.py` | partly (the `hang` subject) | 120 violated via F2 |
| 11 | **The counter's own output contract** | **Partly** — the summary `checks=` count is unverified (F6) | `probe-key-lookup-lie.py`, `probe-own-output.py` | **NO** | 121 partly violated |
| 12 | **Child-bound integrity** | **NO** — a detached grandchild stalls the matrix (F2) | `probe-detach.py`, `probe-detach-timed.py` | **NO** — `forge-hang.py` sleeps in-process | **120/137 violated** |
| 13 | **Metadata-only case identity** | **Closed** — numstat cannot separate `append` from `dup-*` | `probe-key-lookup-meta.py` (6/12) | yes (`diff-only` 9/12, `tree-identity`, `size-map`) | 135 satisfied |

---

## What the frozen predicate does and does not establish

- **Reproduced exactly.** `BATTERY=PASS forgers_rejected=11/11 positive=2/2`, exit 0
  (`battery-baseline.txt`). C1's kill rule is not triggered by the frozen inputs.
- **What it establishes.** The v3 matrix defeats the r75 answer-key classes the battery
  samples: commit subject, tree identity, byte size, declared order, diff shape, naive
  presence-grep, in-process hang, and the `SEED=` seed leak.
- **What it does not establish.** The battery's eleven subjects leave four open classes
  unmeasured, and each has a measured probe above: the **harness answer-key table**
  (F1 — reaches 12/12 under the frozen battery's own rules), the **detached-grandchild
  stall** (F2 — the matrix never finishes), the **parent-stdout label/verdict leak**
  (F3 — file mode), and the **unchecked summary count** (F6). `claims.md`'s phrase
  *"a counter that reads the unified patch text … is correct for these inputs"* does not
  cover F1, because the F1 probe reads the patch text only to identify the case and
  copies the verdict from the harness's table.

## Scope and limits of this seat's reconnaissance

- All probes ran against the **frozen** `loader-matrix-v3.py` (sha256 verified before
  and after). The one battery variant used is a scratch copy with one extra subject; the
  frozen battery file was never edited.
- Probes are **read-only against the lane tree**. The matrix creates its own disposable
  fixture repositories under `--work`, inside this seat's scratch; the seat created no
  fixture repository of its own and performed no git mutation anywhere.
- **F1 is measured, not argued**: `probe-key-lookup.py` and `probe-public-path.py` each
  print `LOADER_MATRIX=12/12 MATRIX=PASS` and exit 0 against the frozen matrix, and the
  scratch battery copy scores the subject `MISS` (not rejected) and prints
  `BATTERY=FAIL forgers_rejected=11/12 positive=2/2`.
- **F2 is measured, not argued**: the grandchild-survival marker was written at t=6 s
  after a `killpg` at t=1 s, and the matrix stalled past a 30 s outer timeout.
- The F1 probe identifies the case from the patch text. Whether the lane considers
  patch-text reading a legitimate content channel (as `claims.md`'s recorded limit
  suggests) is a **routing decision for L1 and the reviewer, not a fact this seat
  settles**; what is settled is that the *verdict* is copied from the harness rather
  than derived, and that the frozen battery does not detect it.
- The F3 leak is **mode- and environment-dependent** (`PYTHONUNBUFFERED=1` + regular-file
  stdout). Under the frozen battery's own pipe mode it reads 0 bytes. It is reported as
  a live hazard for receipt production, not as a battery-breaking forgery.
- No claim is made about arbitrary-forgery freedom, about the C2 axis
  (`correction-count-v2.py` / `c2-battery.py` were not measured by this seat), or about
  any instrument outside `corpus/evidence/round76/`.

## Artifacts

Under `.ufo/waves/round-76/w1/R76Scout/`:

- probes: `probe-key-lookup.py`, `probe-public-path.py`, `probe-lane-tree-map.py`,
  `probe-key-lookup-meta.py`, `probe-key-lookup-lie.py`, `probe-import-harness.py`,
  `probe-parent-stdout.py`, `probe-stdout-only.py`, `probe-stdout-mode.py`,
  `probe-metadata-timing-env.py`, `probe-channels.py`, `probe-own-output.py`,
  `probe-detach.py`, `probe-detach-timed.py`, `battery-with-probe.py`
- receipts: `battery-baseline.txt`, `battery-with-probe.txt`, `key-lookup*.txt`,
  `public-path.txt`, `lane-tree-map*.txt`, `parent-stdout3.txt`, `parent-buffered.txt`,
  `stdout-only.txt`, `metadata-timing.txt`, `own-output.txt`, `detach*.txt`,
  `import-harness*.txt`, plus 12 `metadata-timing-<pid>.json` and 12
  `parent-stdout-<pid>.json` per-case channel reports.

## Boundaries observed

- Read-only against the lane's frozen artifacts and the frozen instruments; the only
  files this seat wrote are its own report, its own wave folder, and its scratch tree.
- All scratch work lived under `/fast/scratch/hyaku/chousa-r76/R76Scout/` and was
  deleted before this report was filed.
- No network, no package install, no tool installed or upgraded this round (the host's
  `python3 3.14.8` and `git 2.56.0` sufficed). Per `/home/vgpnk/.omp/agent/RULES.md`, no
  pacman transaction was attempted; the host-wide pacman guard was not approached.
- No task tool, no subagent dispatch, no `agent://all`, no lane/fleet git or jj
  mutation, no commit, no push. Sibling seats' outputs were read only.

…

Report: `.ufo/waves/round-76/w1/R76Scout.md`
