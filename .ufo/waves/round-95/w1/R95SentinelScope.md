# R95SentinelScope — containment & side-effect review of C1 at carrier C

**Seat:** R95SentinelScope (sentinel) · **Lane:** chousa round 95, L1 · **Scope:** `tools/search-rerun.py` and
`corpus/evidence/round95/rerun-controls-r95.py` at C `d27e9891ba6d2bae8b1f6060f7c01bf13a1a6ea1`.
**Target claim:** `claims.md` C1 kill rule **K3** — *"the tool writes a file, opens a socket, or reads a path
outside `--root` (symlinks included)"* — plus the containment wording of the tool's own docstring and of the C1
sentence.

**Method.** `git clone -q --shared` of the lane into scratch, `checkout d27e9891`; every fixture repo created with
`git init -q` and asserted `rev-parse --show-toplevel` == fixture dir before any mutating git call. All work under
`/fast/scratch/hyaku/chousa-r95/R95SentinelScope/`. `strace` (GNU, `/usr/bin/strace`) used for the syscall-level
claims. Receipts: `.ufo/waves/round-95/w1/R95SentinelScope-c*.txt`.

**Baseline holds.** The committed predicate is reproduced at C: the positive verify exits 0 with
`SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8` and `SEARCH_RERUN: CLEAN` (receipt c1), and the battery prints
`POSITIVE=1/1 STRICT_TREE=1/1 FORGERY_REFUSED=8/8 PRIOR_ACCEPTED=8/8 SETUP_REFUSED=12/12 CLONE_TREE=2/2
DO_NOTHING_REFUSED=1/1 ORACLES_REJECTED=3/3` / `RERUN_CONTROLS=PASS`, exit 0 (receipt c3). Under a plain
environment the tool writes nothing (every `write(2)` in the positive strace is to fd 1; none to fd 3+), opens no
socket (`connect()` count 0), and opens no lane-external data path (receipt c2). The battery writes only under
`--work` — every absolute `O_WRONLY|O_CREAT` open in the battery strace lands under
`<work>/rerun-controls-r95/...`, none under the lane (receipt c12) — and it removes `--work` on exit, including on
setup failure.

---

## FINDING 1 — HIGH — `GIT_DIR` in the caller's environment redirects the rev-side re-run to a foreign object
## database, and a forged record is then accepted as `CLEAN` (exit 0)

**K3 fired.** The tool reads paths outside `--root` (the foreign ODB), and the forgery it is built to refuse is
accepted.

**Exploit path.**

1. `tools/search-rerun.py` runs every git call as `subprocess.run(["git", "-C", root, *args])` with **no `env=`
   argument**, so the child inherits the caller's environment verbatim. `git -C <root>` changes the *working
   directory* but does **not** override `GIT_DIR`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES` or
   `GIT_COMMON_DIR` — those still select the object database `ls-tree`/`cat-file` read.
2. The tool's only root check is `git(root, "rev-parse", "--show-toplevel")` compared against
   `os.path.realpath(root)`. With `GIT_DIR` set, `rev-parse --show-toplevel` still reports the **cwd** (the lane),
   so the check passes — the check validates the work tree, never the object database.
3. `files_at_rev()` therefore lists the foreign repository's tree for the recorded `rev`, and `blob()` reads that
   repository's blobs.
4. A `refs/replace/<recorded-rev>` in the foreign repo makes `git ls-tree`/`cat-file` serve a *different* tree for
   the recorded revision. The tool has no `--no-replace-objects` and no `GIT_NO_REPLACE_OBJECTS`, so the substitution
   is invisible to it.
5. A record forged to match the substituted tree is reported `rev_match=8/8 … SEARCH_RERUN: CLEAN`, **exit 0**,
   while the same record on the unmodified lane is correctly refused with `COUNT_DRIFT,SET_DRIFT`, exit 1.

**Evidence (exact commands, receipt, observed line, exit code).**

Setup (self-contained foreign repo, own objects, no alternates back to the lane):
```
S=/fast/scratch/hyaku/chousa-r95/R95SentinelScope
git clone -q --no-checkout "$S/repo" "$S/foreign"
git -C "$S/foreign" fetch -q --no-tags origin 7b2373586fb70f0ead6446c671fcc8b546d3e687
git -C "$S/foreign" checkout -q --detach FETCH_HEAD
printf 'retrieval 检索\n' > "$S/foreign/corpus/captures/zz-extra.txt"
git -C "$S/foreign" add -A
git -C "$S/foreign" -c user.name=fixture -c user.email=fixture@invalid commit -q -m repl
git -C "$S/foreign" replace 7b2373586fb70f0ead6446c671fcc8b546d3e687 "$(git -C "$S/foreign" rev-parse HEAD)"
```
Forged record: Q5 `hits` 14 → 15 with the matching `sha256:` digest of the 15-path set.

Control (no injection), from the lane root:
```
python3 -B tools/search-rerun.py verify "$S/forged-q5-15.md" --root .
```
→ exit 1, `SEARCH_RERUN Q5 rev=DRIFT … recorded=15 at_rev=14 at_tree=14 COUNT_DRIFT,SET_DRIFT`,
`SEARCH_RERUN: DRIFT`. (receipt c5, section E2)

Attack:
```
env GIT_DIR="$S/foreign/.git" python3 -B tools/search-rerun.py verify "$S/forged-q5-15.md" --root .
```
→ **exit 0**, `SEARCH_RERUN Q5 rev=MATCH tree=CHANGED recorded=15 at_rev=15 at_tree=14 TREE_CHANGED`,
`SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8 tree_same=2/8 findings=0`, `SEARCH_RERUN: CLEAN`.
(receipt c5, section E3)

Containment proof — the rev data came from outside `--root`. `strace -f -e trace=openat` of the same run:
**1364** opens under `<scratch>/foreign/.git/...` (the foreign ODB), **0** opens under
`<scratch>/repo/.git/objects/...` (the lane's ODB). Sample:
```
openat(AT_FDCWD, "/…/R95SentinelScope/foreign/.git/objects/02/142ecdf99fa556b7268479d1cb704d774dd091", O_RDONLY|O_CLOEXEC)
```
(receipt c4). The same read-through occurs with `GIT_ALTERNATE_OBJECT_DIRECTORIES` pointing outside `--root`
(630 opens under the foreign ODB; receipt c11).

**A second, environment-free variant of the same root cause exists.** A `refs/replace/<rev>` planted in the
**lane repository itself** (no env var at all) produces the identical false `CLEAN`:
```
git -C "$S/repo" replace 7b2373586fb70f0ead6446c671fcc8b546d3e687 <repl-commit>
python3 -B tools/search-rerun.py verify "$S/forged-q5-15.md" --root .
```
→ exit 0, `SEARCH_RERUN Q5 rev=MATCH … at_rev=15`, `rev_match=8/8 … SEARCH_RERUN: CLEAN`. The replace ref must
live in `.git/refs/replace/`, which is not committed, so it is not reachable through the lane's history — but it is
reachable through any clone, any `git fetch`, or any `GIT_DIR` pointing at a repo that has it. `GIT_NO_REPLACE_OBJECTS=1`
in the child environment restores the correct refusal (verified: `rev=DRIFT … COUNT_DRIFT,SET_DRIFT`, exit 1).

**Why this falsifies the claim.** The C1 sentence promises the tool *"re-runs a recorded local search expression at
the revision the record names"* and *"refuses a record whose filed count or hit set differs from what the expression
finds there"*. Under either vector it re-ran at a **different** revision than the one named (the replace-ref
substitute) and **accepted** the forged record — precisely the "COUNT_DRIFT/SET_DRIFT, exit 1" behaviour the claim
states. The docstring's promise *"Reads only ROOT's files and its git objects"* is false in the same run: the rev
data came from `<scratch>/foreign/.git/objects/…`, outside `--root`.

Note the lane's own nearest prior instrument already treats this class as a defect: `tools/research-gate.sh` pins
`grep` by absolute path and verifies its provenance (round-35 C1, `research-gate.sh:415-470`), explicitly because
*"the gate's behaviour is a function of the caller's environment"*. `search-rerun.py` resolves `git` through `PATH`
and inherits the git environment with no equivalent pin. This is a live asymmetry with the lane's established
convention, not a new standard.

**Smallest remediation.** In `git()` (`tools/search-rerun.py:66-68`), pass an explicit scrubbed `env` to
`subprocess.run` — drop `GIT_DIR`, `GIT_WORK_TREE`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`,
`GIT_COMMON_DIR`, `GIT_INDEX_FILE`, `GIT_CEILING_DIRECTORIES`, `GIT_NAMESPACE`; set `GIT_NO_REPLACE_OBJECTS=1`,
`GIT_NO_LAZY_FETCH=1`, `GIT_TERMINAL_PROMPT=0`, `GIT_ASKPASS=`/`SSH_ASKPASS=`; and resolve `git` to an absolute path
(e.g. `/usr/bin/git`) after a `--version` provenance check, mirroring `research-gate.sh`'s grep pin. Verified: with
that scrub the same forged record is refused (`rev=DRIFT … COUNT_DRIFT,SET_DRIFT`, exit 1) **with** `GIT_DIR` still
set in the parent environment.

---

## FINDING 2 — HIGH — a partial (promisor) clone makes the tool open a network socket and let git **write into
## `--root`'s object store**

**K3 fired, twice:** the tool opens a socket, and it causes a write.

**Exploit path.** `blob()` runs `git -C root cat-file blob <obj>`. In a partial clone (`--filter=blob:none`) with a
promisor remote, a missing blob is fetched lazily: git spawns `git fetch origin --filter=blob:none` and
`git-upload-pack`, opening a socket to the remote and **writing the fetched objects into the root repository's
`.git/objects/`**. `search-rerun.py` sets no `GIT_NO_LAZY_FETCH` and passes no `--no-lazy-fetch`, and it has no
promisor/`extensions.partialClone` check.

**Evidence.** A `git://` promisor clone served over loopback (`git daemon --base-path=… --port=9419 --listen=127.0.0.1`):

`strace -f -e trace=openat,connect` of
`python3 -B tools/search-rerun.py verify <record> --root <partial-clone>`:
**87** `connect()` calls, every one to the remote:
```
connect(3, {sa_family=AF_INET, sin_port=htons(9419), sin_addr=inet_addr("127.0.0.1")}, 16) = 0
```
(receipt c6; tool output in receipt c7).

`strace -f -e trace=openat,connect,write,execve` of the same run against a `file://` promisor clone shows the tool
spawning the fetch:
```
execve("/usr/lib/git-core/git", ["git","-c","fetch.negotiationAlgorithm=noop","fetch","origin","--no-tags",
       "--no-write-fetch-head","--recurse-submodules=no","--filter=blob:none","--stdin"], …) = 0
execve("/usr/lib/git-core/git-upload-pack", ["git-upload-pack","/…/R95SentinelScope/repo"], …) = 0
```
(receipt c8). The write is observable in the filesystem: the root clone's object count went **4 → 354** files across
the run, and the three probe blobs flipped `MISSING-before → PRESENT-after`. The tool's own docstring says
*"No network, no writes"* — both false in this configuration.

**Why this falsifies the claim.** K3 says the tool *"writes a file, opens a socket, or reads a path outside
`--root`"*. Here it does the first two. The docstring's *"Reads only ROOT's files and its git objects (read-only
`git ls-tree`/`git cat-file`). No network, no writes"* is false. The lane's own repo is not a promisor today
(`git config --get remote.origin.promisor` is empty at C), so the shipped predicate does not exercise this — but
the tool's stated containment property is what C1 asserts, and it does not hold for a valid `--root` that happens to
be a partial clone. `GIT_NO_LAZY_FETCH=1` is the mitigation (verified: with it, the same run produces **0**
`connect()` calls and **0** `upload-pack` execs).

---

## FINDING 3 — MEDIUM — the record path is resolved against the **process CWD**, not `--root`, and a record that is
## itself a symlink is read with no refusal

**Exploit path.** `main()` calls `verify(a.record, os.path.abspath(a.root), a.strict)`; `parse_record()` opens
`path` verbatim (`tools/search-rerun.py:124-128`). The record path is therefore interpreted relative to the
caller's current working directory, never relative to `--root`. Two consequences:

**(a) The record is read from outside `--root`.** A record supplied as a symlink is opened through it with no
refusal, and the tool reads the target:
```
ln -sf /etc/hostname "$S/rec-etc.md"
python3 -B tools/search-rerun.py verify "$S/rec-etc.md" --root .
```
→ exit 2, `SEARCH_RERUN_ERROR SECTION expected exactly one '## Searches' heading, found 0` — i.e. the tool read
`/etc/hostname` (`plazir27`) through the symlink. The strace shows the open of the symlink path itself
(`openat(AT_FDCWD, "…/rec-etc.md", O_RDONLY|O_CLOEXEC)`), which the kernel resolves to the out-of-root target. The
tree-side code refuses symlinks by design (`WHERE_TYPE`); the record side does not.

**(b) The documented invocation is CWD-dependent.** The C1 predicate in `claims.md` is
`python3 -B tools/search-rerun.py verify corpus/fixtures/search-rerun-r95.md --root .`. That works only because
CWD == `--root`. Run from anywhere else, the same command reads a *different* file (or none):
```
cd "$S" && python3 -B repo/tools/search-rerun.py verify corpus/fixtures/search-rerun-r95.md --root "$S/repo"
```
→ exit 2, `SEARCH_RERUN_ERROR RECORD_UNREADABLE corpus/fixtures/search-rerun-r95.md: [Errno 2] No such file or
directory`. The `--root` argument is advertised as scoping the run, but the record is not scoped by it.

**Why this falsifies the claim.** K3 names "reads a path outside `--root` (symlinks included)". The record is a
path the tool reads; a symlinked record is followed out of root without the `WHERE_TYPE` refusal the corpus side
applies. Severity is MEDIUM rather than HIGH because the record path is an explicit CLI argument the caller
chooses — but the tool's own docstring says *"Reads only ROOT's files and its git objects"*, which does not hold, and
the C1 sentence's "the revision the record names" is ambiguous when the record itself may be somewhere else.

**Smallest remediation.** Resolve the record against `--root` when it is relative
(`os.path.join(root, record)` if not `os.path.isabs(record)`), and refuse a record that is not a regular file
inside `--root` (`os.path.islink` → a new `RECORD_TYPE` setup code, exit 2), matching the tree-side discipline.

---

## FINDING 4 — LOW — the record's `rev` is accepted from a foreign object database, so the documented setup error
## ("a rev that is not a commit of ROOT's repository") is not enforced

`files_at_rev()` validates the revision with `git -C root cat-file -e <rev>^{commit}` — again subject to the
caller's `GIT_DIR` (Finding 1). With `GIT_DIR` pointed at a foreign repository, a revision that is **not** a commit
of the lane was accepted and evaluated rather than refused:
```
git -C "$S/foreign" -c user.name=fixture -c user.email=fixture@invalid commit -q --allow-empty -m "foreign-only"
sed "s/7b237358…/$FONLY/" corpus/fixtures/search-rerun-r95.md > "$S/rec-foreign-rev.md"
env GIT_DIR="$S/foreign/.git" python3 -B tools/search-rerun.py verify "$S/rec-foreign-rev.md" --root .
```
→ exit 1 (drift on the counts), **not** exit 2 `SEARCH_RERUN_ERROR REV … is not a commit of ROOT's repository`.
Uninjected, the same revision is refused correctly (`SEARCH_RERUN_ERROR REV 7e8dd45… is not a commit in
…/fixrev`, exit 2 — receipt c9/c10). This is the same root cause as Finding 1 and is fixed by the same scrub; it is
listed separately because the docstring enumerates this refusal as a guarantee and it does not hold.

---

## What holds (negative results worth recording)

All of these were attacked and are correctly refused or correctly bounded. Receipt c9, c10.

| Attack | Result | Receipt |
|---|---|---|
| REV-side symlink as a path component (mode 120000 entry under the glob's static dir, in a fixture repo) | exit 2 `WHERE_TYPE Q1: corpus/captures/evil.txt at 475ea892e985 is mode 120000 (blob)` | c9 `b-revsym` |
| REV-side symlink committed at the named rev, working tree clean | exit 2, same `WHERE_TYPE` code | c9 `b-revsym` |
| Symlinked **directory** on the tree side (glob's static dir is a symlink) | exit 2 `WHERE_TYPE corpus on a glob's path is a symlink` | c9 `b-symdir` |
| `--root` pointing at a subdirectory of the repo | exit 2 `ROOT … is not a git toplevel` | c9 `b-subroot` |
| `rev` given as a branch name (`master`) | exit 2 `REV Q1: rev must be 40 lowercase hex` | c9 `b-branch` |
| `rev` given as `HEAD~1` | exit 2 `REV Q1: rev must be 40 lowercase hex` | c9 `b-head1` |
| `rev` that is not a commit of the root repo (uninjected) | exit 2 `REV … is not a commit in …` | c9 `b-fixrev` |
| `GIT_WORK_TREE` pointed outside `--root` | exit 2 `ROOT … is not a git toplevel` | (in c9 series, `S0`) |
| `GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_0` = `core.fsmonitor` (command exec) | not executed by `ls-tree`/`cat-file`; verdict unchanged | (in run log) |
| `GIT_CONFIG_COUNT` = `core.pager` | no pager spawn | (in run log) |
| `PATH` shim `git` earlier in PATH | the fake git's numbers are used but the shim cannot fabricate a *match* — the run reports DRIFT on 7/8 rows, never a false CLEAN | (in run log) |
| Battery writes | every absolute `O_WRONLY\|O_CREAT` open lands under `<work>/rerun-controls-r95/…`; the count of absolute write-mode opens outside `<work>` and outside `/dev/null` is **0** | c12, c13 §1/§1b |
| Battery cleanup on success and on setup failure | `--work` removed in all three paths (PASS, missing `--tool`, unreadable record); only the empty parent `--work` dir remains | c13 §2/§3/§4 |
| Lane mutation by the battery | `git status --porcelain` on the attacked clone: empty (clean) | c13 §5 |

One nuance on the `PATH`-shim row: a shimmed `git` *is* trusted for the rev-side re-run, and the tool's root check
(`rev-parse --show-toplevel`) is itself answered by the shim. In the measured shim it did not yield a false
`CLEAN`, but the tool's trust boundary for `git` is the caller's `PATH` — which is the same class of defect as
Finding 1 and is addressed by the same absolute-path pin.

---

## Post-remediation verification (observed, not claimed)

A concurrent seat edited `tools/search-rerun.py` in the lane working tree while this seat was reporting; the new
`git_env()` docstring cites *"round 95, R95SentinelScope findings 1, 2, 4"* explicitly. This seat did **not** make
that edit and does not claim it. I re-ran my three exploits against the **remediated** working-tree tool and
recorded the results (receipt c14):

| Exploit | Remediated result |
|---|---|
| `GIT_DIR=<foreign ODB with refs/replace>` + forged record (Q5 hits=15 + matching digest) | `SEARCH_RERUN Q5 rev=DRIFT … COUNT_DRIFT,SET_DRIFT`, `rev_match=7/8`, `SEARCH_RERUN: DRIFT` — **no longer CLEAN** |
| record path is a symlink to `/etc/hostname` | `SEARCH_RERUN_ERROR RECORD_TYPE …: the record must be a regular file, not a symlink`, exit 2 — **now refused** |
| partial clone with a promisor remote | `connect()` count **0**, `git-upload-pack` execs **0** — **no socket, no lazy fetch** |

The remediation is `git_env()`: strip every `GIT_*` variable from the child environment and set
`GIT_NO_REPLACE_OBJECTS=1`, `GIT_NO_LAZY_FETCH=1`, `GIT_TERMINAL_PROMPT=0`, with `env=git_env()` on both git
calls (`tools/search-rerun.py:96-108`, `:261`), plus a `RECORD_TYPE` refusal for a symlinked record.

**Residual gap, stated plainly.** The remediation strips `GIT_*` from the *environment* but the tool still resolves
`git` through the caller's `PATH` and does not verify its provenance. A `PATH` shim named `git` is therefore still
trusted for the rev-side re-run and for the tool's own root check (`rev-parse --show-toplevel`). In my measured
shim it did not produce a false `CLEAN`, but the trust boundary is unchanged, and `research-gate.sh` already
solves the identical problem for `grep` by pinning an absolute path and checking its self-reported version
(`tools/research-gate.sh:415-470`). That gap is a LOW residual, not a refutation of the findings above.

---

## Tooling

No tool was installed or upgraded this seat; `strace` (GNU strace, `/usr/bin/strace`, present on the host) and
`git` 2.x (`/usr/bin/git`) were used as found. `/usr/bin/grep` (GNU grep 3.12) was used wherever grep semantics
mattered, per the host note. No pacman transaction was performed (pacman is paused host-wide by the orchestrator).

## Scope note

Findings 1, 2 and 4 are about `tools/search-rerun.py`; Finding 3 is about the same tool's record handling.
`corpus/evidence/round95/rerun-controls-r95.py` is clean on the assigned surface: it writes only under `--work`,
cleans up on failure, leaves the lane unmodified, and its seven scored groups reproduce at C. I did **not** edit
any production file — remediation is stated, not applied, since this seat's assignment is falsification only.

---

VERDICT: R95SentinelScope C1 fired — the tool inherits the caller's git environment, so `GIT_DIR`/`GIT_OBJECT_DIRECTORY`/`GIT_ALTERNATE_OBJECT_DIRECTORIES` and `refs/replace` make it re-run the rev-side search against a foreign object store outside `--root` and report a forged record `CLEAN` (exit 0) where the same record is correctly refused (exit 1), and a partial clone makes it open a network socket and write fetched objects into `--root`; K3 fires.
