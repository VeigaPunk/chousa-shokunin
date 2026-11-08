# R94SentinelScope — scope and safety review of the round-94 instruments

Seat: `R94SentinelScope` (sentinel, leaf). Attacked tree: carrier `C = 352924bbea624caf3771ef291be98fd4ec679dda`,
clone `git clone --shared … <S>/repo && git checkout C`, `<S> = /fast/scratch/hyaku/chousa-r94/R94SentinelScope`.
Freeze `F = 41038ed7c40cffc4cf86d649a6ba433c4b9eec1a`. No lane edit, no network, no sudo, no
production mutation. Receipts for every claim below are in `.ufo/waves/round-94/w1/R94SentinelScope/`.

**SCOPE_FINDINGS=10**

Rubric: severity is the effect on the round's evidence, not on a hostile third party. The
instruments are operator-invoked harness code, so an unvalidated operator argument is a defect only
when it destroys data, escapes the tree, or makes a claimed predicate unfalsifiable.

---

## F1 — C1 predicate not met at the carrier: the forgeries battery exits 1 (`FORGERIES=FAIL`)

Severity: **high** (K1 class; the claim's own machine predicate carries `"exit": 0`).

```
$ python3 -B corpus/evidence/round94/forgeries-r94.py --root . --repo . \
    --rev 41038ed7c40cffc4cf86d649a6ba433c4b9eec1a \
    --receipts-rev 352924bbea624caf3771ef291be98fd4ec679dda --work <S>/r02-forg
FAIL s1-schema-two-column: r93 rc=0 r94 rc=0 needles=SETUP PIN_SCHEMA
FORGERIES=FAIL FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 SCHEMA_REFUSED=1/1 SCHEMA_PRIOR_ACCEPTED=1/1 CARRIED_REFUSED=2/2 POSITIVE=pass
# exit=1
```
Receipt: `R94SentinelScope/r02-c1-forgeries-at-C.txt` (observed independently twice; the second run,
`<S>/du-f`, reproduced `FORGERY=FAIL` and `FORG_RC=1`).

Cause, by construction: `corpus/evidence/round94/forgeries-r94.py:168`
```python
    case("s1-schema-two-column", None, 2, ["SETUP PIN_SCHEMA"])
```
`case()` with `rows_mutator=None` calls `write_r94(tpins, rows, PINS_REL)` — a **three-column**
table — then demands `rc_new == 2` and `SETUP PIN_SCHEMA`. A three-column table is exactly what the
driver accepts, so `rc_new == 0` and the case can never pass. `ok = all(results.values())`, so the
whole battery reports FAIL. Every other case prints `OK` (d1…d4, s0-schema-prior, c1/c2 carried,
positive) in the same run, and `FORGERRY_REFUSED…POSITIVE=pass` are all full — the failure is solely
this dead fixture.

Frozen predicate it violates: `claims.md` C1 — "The battery prints `FORGERIES=PASS
FORGERY_REFUSED=4/4 … POSITIVE=pass` (exit 0)"; `claims.json` C1 `predicate.exit = 0`.

Smallest remediation (verified): delete that one line.
```
$ python3 - <<'PY'   # in the clone only, then restored with git checkout
p="corpus/evidence/round94/forgeries-r94.py"; s=open(p).read()
open(p,"w").write(s.replace('    case("s1-schema-two-column", None, 2, ["SETUP PIN_SCHEMA"])\n',"",1))
PY
$ python3 -B corpus/evidence/round94/forgeries-r94.py … --work <S>/fix-forg
FORGERIES=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 SCHEMA_REFUSED=1/1 SCHEMA_PRIOR_ACCEPTED=1/1 CARRIED_REFUSED=2/2 POSITIVE=pass
# exit=0
```
Receipt: `R94SentinelScope/r19-remediation.txt` (captured from job `bg_25224`, command as shown).

State of the lane, for the L1: while this seat ran, the lane moved past the assigned carrier —
`4cbaed6c freeze F2 (… dead code removed, s1 dropped …)`, `ebbcbe39 freeze F3 (reviewer/critic/sentinel
findings applied …)`, then carriers `C2 f276d7fb` and `C3 d13c2ff2`. At lane `HEAD d13c2ff2` the case is
gone (`grep -c s1-schema-two-column …` → `0`), so F1 is closed on the later revision. What failed is the
**committed carrier `C = 352924bb`** that this seat was assigned and that its pin table binds; the
per-finding status at `HEAD` is tabulated at the end of this report.

Note the C1 *verify* half of the predicate **is** met at `C` (see the positive confirmations), so the
failure is localised to the forgeries battery.

---

## F2 — all three batteries `rmtree` the caller's `--work` with no containment guard

Severity: **medium** (silent recursive deletion of an arbitrary operator-supplied path).

```python
forgeries-r94.py:108            shutil.rmtree(work, ignore_errors=True)
curation-controls-r94.py:97     shutil.rmtree(work, ignore_errors=True)
skill-tally-r94-controls.py:111 shutil.rmtree(work, ignore_errors=True)
```
No `realpath`/`commonpath`/`is_relative_to` check against `--root`, the tree, or `$HOME` anywhere in
the three files (`grep -nE 'work (==|in|startswith)|is_relative_to|commonpath|realpath.*work'` → no hit).

Measured, on scratch fixtures:
```
$ mkdir -p <S>/victim/precious && echo important > <S>/victim/precious/data.txt
$ python3 -B corpus/evidence/round94/curation-controls-r94.py --root . --work <S>/victim
OK positive: …   (runs; # exit=1 later)
$ ls <S>/victim        # → c1-nonq-row positive pristine ws-space ws-tab
$ test -f <S>/victim/precious/data.txt → DELETED_BY_BATTERY
```
and the same with `skill-tally-r94-controls.py --root . --work <S>/hz/mytree` →
`USER_DATA_DELETED` (1 file before, 9 after, the original gone).
Receipts: `r11-work-rmtree.txt`.

Related, same class: `control-driver-r94.py:459` defaults `--work` to
`os.environ.get("TMPDIR") or "/fast/scratch/hyaku"` and writes `fresh-<case>.out` **directly** into
that path (line 547), i.e. into a shared scratch root when `--work` is omitted. Code-derived (not
executed against the shared root, by seat rule).

Smallest remediation: refuse unless `work` is absent, empty, or a path this run created
(`mkdtemp(dir=…)`); at minimum reject `work` resolving to `root`, an ancestor of `root`, or `$HOME`.

---

## F3 — a pinned expectation hardcodes an absolute host `HOME`, defeating the driver's own scrub

Severity: **medium-low** (non-reproducible host path in a pinned artefact; reads `$HOME` outside the tree).

`corpus/evidence/round94/controls/expected.tsv:4` (role `expectation`, pinned at `C`):
```
c1-harm	mkdir -p @WORK@/harm && HOME=/home/vgpnk git -C @ROOT@ show 265b8633…:tools/gate-records.py > … && python3 -B …/harm-recheck-r90.py …
```
`control-driver-r94.py:211-213` deliberately sets `HOME` to the tree root for every fresh leg
("no rc/profile reads"); the `c1-harm` row overrides it back to the operator's real home. Measured:
```
$ strace -f -qq -e trace=openat -o strace-c1.txt python3 -B …/control-driver-r94.py verify …
$ grep -o 'openat(AT_FDCWD, "/home/vgpnk[^"]*"' strace-c1.txt | sort | uniq -c
    129 openat(AT_FDCWD, "/home/vgpnk/.config/git/config"
```
`/home/vgpnk/.config/git/config` exists and contains
`credential.https://github.com.helper=!/home/vgpnk/.local/bin/gh auth git-credential` — a credential
helper is loaded by the harness's own git call. No credential is emitted (`git show` on a local rev
never authenticates, no network), so this is a read/config-leak exposure, not a live token leak.

The override is **not necessary** — measured both ways:
```
$ HOME="$PWD" bash -c "… git show 265b…:tools/gate-records.py > … && python3 -B …/harm-recheck-r90.py …"
HARM_RECHECK files=22 records=36 moved=0 base_rc=1 head_rc=1     # exit 0
$ HOME=/home/vgpnk bash -c "… (identical command) …"
HARM_RECHECK files=22 records=36 moved=0 base_rc=1 head_rc=1     # exit 0
```
Receipts: `r10-home-read.txt`.

Smallest remediation: drop `HOME=/home/vgpnk` from the row (let `scrub_env` apply) and re-emit the
`c1-harm` receipt; the fixture pins the changed expectation row in the same commit.

---

## F4 — a pinned receipt embeds the emitter's absolute scratch path

Severity: **low** (non-reproducible body; the FRESH comparison tolerates it).

`corpus/evidence/round94/controls/receipts/c1-harm-setup.txt:5` (role `receipt`, pinned at `C`):
```
HARM_RECHECK_ERROR base-tool missing: /fast/scratch/hyaku/chousa-r94/l1/emit/absent-tool.py
```
`/fast/scratch/hyaku/chousa-r94/l1/emit/` is the L1's scratch path at emit time. It cannot be
reproduced from any other `--work`: the `c1-harm-setup` row's required token is only
`HARM_RECHECK_ERROR`, so `check_body` accepts any `--work` path in the fresh body and the committed
bytes are never compared to a fresh body.
Smallest remediation: strip/normalise the work path in the emitted body, or make the required value a
token with no path (e.g. `base-tool missing`).

---

## F5 — a pins row naming an in-tree symlink reads bytes outside the tree

Severity: **low** (latent: no symlink row exists at `C`; reachable by any tree whose pins table names a symlink).

`pin_report` rejects a row only lexically (`os.path.isabs(rel) or ".." in parts` → `PIN_ROW_OUTSIDE`),
then `sha256_file(os.path.join(abspath(root), rel))` follows symlinks. Measured on a fixture tree with
`corpus/evidence/round94/link.txt -> <outside>/secret.txt`:
```
# hash == the OUTSIDE file's hash:
PINNED_FILES=34/35   (the symlink row counted as verified; only the self-row mismatch)
# hash != the outside file's hash:
RECEIPT PINS FINDING … PIN_DISK_MISMATCH path=corpus/evidence/round94/link.txt
```
The second line proves the outside bytes were read and hashed. Receipts: `r12-symlink-pin-escape.txt`.
Smallest remediation: after building `disk`, require
`os.path.realpath(disk).startswith(os.path.realpath(root) + os.sep)`.

---

## F6 — `--pins` outside the tree is read (and its content echoed) before containment is checked; exit is 1, not 2

Severity: **low**.

```
$ … control-driver-r94.py verify --root . --repo . --rev F --receipts-rev C --work <S>/t1 --pins /etc/hostname
BASES root=… repo=…
SETUP PIN_SCHEMA row is not `<sha256>  <role>  <path>`: 'plazir27'      # ← /etc/hostname's first line, echoed
# exit=2
$ … verify … --pins <S>/outside/pins.txt      # a valid 3-column table outside the tree
RECEIPT c1-gate-r89 OK …  (all six fresh legs run first)
SETUP path escapes base: <S>/outside/pins.txt vs <S>/repo
# exit=1        ← setup-class refusal, finding-class exit
```
Receipts: `r09-traversal.txt`. `rel_for(root, pins_path)` is only reached inside `pin_report`, i.e.
after `read_pins()` and after every fresh leg. Smallest remediation: `rel_for(root, a.pins)` in
`main()` before `read_pins`, and exit 2.

---

## F7 — `--receipts-rev` is not validated the way `--rev` is

Severity: **low** (`--rev` is gated; its sibling is not).

`REV_RE` guards only `a.rev` (`control-driver-r94.py:476`); `a.receipts_rev` flows unvalidated into
`git show f"{rv}:{rel}"`. Measured:
```
$ … verify … --receipts-rev '41038ed7c40cffc4cf86d649a6ba433c4b9eec1a:/etc' --work <S>/t6
RECEIPT SELF_PIN FINDING SELF_DRIFT corpus/evidence/round94/controls/receipts/c1-gate-r89.txt@41038ed7…:/etc,…
# exit=1
```
No escape occurred (git itself refuses paths outside the repository —
`fatal: '../../../../etc/hostname' is outside repository` and
`fatal: path '/etc/hostname' exists on disk, but not in '41038ed7…'`), but a setup-class input
reaches `git show` unchecked. Receipts: `r09-traversal.txt`. Smallest remediation: assert
`REV_RE.fullmatch(a.receipts_rev or a.rev)` next to the `--rev` guard.

---

## F8 — `bash` clones with `--shared` (correct) but leaves the clone behind on every exit path

Severity: **low-medium** (disk only; all inside `--work`, so contained by the seat's scratch rule).

`forgeries-r94.py:112` `git clone --shared --quiet a.repo tree`; the clone's own object store is
`4.0K`, `objects/info/alternates` points at `<repo>/./.git/objects` — i.e. genuinely shared and must
never be repacked (S221). There is no `finally`; the only `rmtree` is at start-up.
Measured:
```
normal exit  : <work> = 399M, <work>/tree = 398M, plus 16 per-case dirs (w-*/o-*)
failing exit : --receipts-rev 0000…0 → "SETUP git checkout 0000… failed: fatal: unable to read tree" exit 2,
               <work> = 398M, <work>/tree left behind
```
`curation-controls-r94.py` / `skill-tally-r94-controls.py` leave 2.3M / 2.7M of mirrored trees.
Receipts: `r02-c1-forgeries-at-C.txt` (normal-exit du) and `r13-leftovers-failing-exit.txt`.
Smallest remediation: `tempfile.mkdtemp(dir=work)` for the clone and `shutil.rmtree` in `finally`.

---

## F9 — files the executed instruments read are pinned nowhere; a byte drift there is invisible

Severity: **low** (partly disclosed by C1 named limit 3; the round brief asserts something stronger).

`make-pins-r94.py` is **self-consistent** — it opens exactly the files it pins (expected.tsv →
`expectation`, the receipts dir → `receipt`, the two claims → `claims`, its `DRIVERS` tuple →
`driver`, and each expected-row instrument token → `instrument`), and it opens no file it does not
pin. Regeneration reproduces the table up to the self-row path (`--out` outside the tree makes the
self row `../regen-pins.txt`, which the driver then rejects as `PIN_SELF_ROW_ABSENT`/`PIN_ROW_OUTSIDE`
— note `make-pins` has **no** containment check on `--out`). Receipts: `r17-pins-regen-symmetry.txt`.

The gap is one level out: the *executed* set reads bytes pinned nowhere —
`tools/gate-records.py`, `tools/research-gate.sh`,
`corpus/evidence/round90/curation-r90-controls.py` (executed as `REG` by
`curation-controls-r94.py:187`), `corpus/SOURCES.md`, `corpus/captures/*`,
`corpus/evidence/round57/refetch.tsv`, `corpus/lessons/*`, `SKILL.md`. Measured:
```
$ printf '\n# noop-drift-probe\n' >> tools/gate-records.py
$ … control-driver-r94.py verify --root . --repo . --rev F --receipts-rev C --work <S>/drift1
RECEIPT PINS OK 34/34 pinned files byte-identical RECEIPT_PINS_OK=6/6
CONTROL_DRIVER_R94=PASS
# exit=0                     ← a byte change to the tool the round scores, invisible to the pin walk
```
Receipts: `r15-unpinned-tool-drift.txt`. The FRESH legs catch *behavioural* drift only when the
output tokens change. The round brief's sentence "`tools/research-gate.sh` and `tools/gate-records.py`
are UNCHANGED this round" is therefore asserted, not bound (git confirms `tools/` is byte-identical
`F..C` and `base..C`, so the assertion is currently true — it is just unenforced). Smallest
remediation: add both tools as `driver` rows, or restate the sentence as unpinned.

---

## F10 — a setup-class failure surfaces as a raw traceback and exit 1

Severity: **low**.

```
$ python3 -B corpus/evidence/round94/curation-controls-r94.py --root <S>/fail-tree --work <S>/fail-c
    with open(src, 'rb') as fsrc:
FileNotFoundError: [Errno 2] No such file or directory: '<S>/fail-tree/corpus/evidence/round93/controls/legs.txt'
# exit=1
```
No `SETUP …` line and not exit 2, unlike the counters' convention. Receipts: `r16-setup-traceback.txt`.
Smallest remediation: catch the copy and emit `SETUP missing <path>` / exit 2.

---

# Positive confirmations (the six assigned questions where the answer is "no defect")

## Q1 — does any r94 instrument write outside `--work`?  **No.**

Three independent measurements.
1. `strace -f -e trace=openat,creat,mkdir,mkdirat,unlink,rename` over the whole C1 predicate:
   write-mode opens under the repo tree **0**, under `/home/vgpnk` or `/etc` **0**; all writes are
   `<work>/**` plus `/dev/null`. Receipts: `r07-writes-scope-strace.txt`.
2. All three predicates re-run against a **read-only** bind mount
   (`bwrap --ro-bind / / --ro-bind <S>/repo <S>/ro --bind <S>/ro-work <S>/ro-work`):
   C1 `CONTROL_DRIVER_R94=PASS` exit 0. Receipts: `r08-readonly-tree.txt`.
3. `git status --porcelain` in the clone is empty after every battery run.

The read-only mount and the strace agree: `verify` writes only `fresh-<case>.out` (and the legs the
r89/r90 instruments write under `@WORK@`).

## Q2 — can `--root`/`--rev`/`--pins` make it read or write outside the tree?  **Partly** — see F5–F7.

`--rev` is 40-hex-gated; `--root /etc` → `SETUP missing /etc/corpus/evidence/round94/controls/expected.tsv` exit 2;
`--pins /etc/hostname` → refused (F6); a valid pins table outside the tree → `SETUP path escapes base`
(F6, exit-code defect only); a symlink row escapes the read (F5); `--receipts-rev` unvalidated (F7).
No instrument was made to **write** outside the tree by any argument.

## Q3 — `--shared` and leftovers.  **Yes `--shared`; a tree is left behind (F8).**
Own objects 4.0K, alternates → source repo; normal exit leaves 399M under `--work`; failing exit
leaves the 398M partial clone. Nothing is left outside `--work`.

## Q4 — network or `$HOME`?  **No network; `$HOME` is read (F3).**
No `curl`/`wget`/`urllib`/`socket`/`http` in any r94 instrument. All three predicates PASS inside
`unshare -rn` with only `lo` present (`1: lo: <LOOPBACK> … state DOWN`):
`CONTROL_DRIVER_R94=PASS`/`CURATION_R94=PASS`/`SKILL_TALLY_R94=PASS`, all exit 0.
Receipts: `r14-network-off.txt`.
`$HOME` **is** read, only through F3's forced `HOME=/home/vgpnk` (129 opens of
`/home/vgpnk/.config/git/config` in the driver's own trace, which carries a credential helper line).

## Q5 — `make-pins-r94.py` read/pin symmetry.  **Symmetric** (see F9 for the table-level gap).
It pins exactly the files it opens; a file it does not open is not pinned; the regenerated table
matches the committed one modulo the self-row path.

## Q6 — credential shapes or non-reproducible absolute paths.  **No credentials; two host paths.**
`grep -ciE '(password|passwd|secret|api[_-]?key|authorization:|bearer |BEGIN … PRIVATE KEY|ssh-(rsa|ed25519)|AKIA…|ghp_…|github_pat_|\.local/bin/gh)'`
over the pins table, `expected.tsv`, `legs.txt`, `selftest-r94.txt`, `evidence-before/*` and every
receipt returns one hit — `ok-case  16 fail-secret-shaped  exit=1`, the tool's own case *name*, a
false positive. No key material anywhere. Two absolute host paths are committed and pinned:
`expected.tsv:4` `/home/vgpnk` (F3) and `receipts/c1-harm-setup.txt:5`
`/fast/scratch/hyaku/chousa-r94/l1/emit/absent-tool.py` (F4). Receipts: `r18-credential-hostpath-sweep.txt`.

Also observed while sweeping: `corpus/evidence/round94/after/` is an **empty** directory at `C`
(`git ls-tree -r C -- corpus/evidence/round94/after/ | wc -l` = 0) although the plan calls it the home
of the scored receipts; the scored receipts used by the driver live under `controls/receipts/`
instead. Not a claim deviation (the claim's counting commands name `controls/receipts/`), recorded for
the L1 so the plan's "the scored receipts under `corpus/evidence/round94/after/`" is not read as a
missing artefact.

# Claim predicates as measured at `C`

| claim | command | observed | exit |
|---|---|---|---|
| C1 verify | `control-driver-r94.py verify --root . --repo . --rev F --receipts-rev C --work <S>/rc1` | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=34/34 RECEIPT_PINS=6/6 PIN_ROLES_OK=14/14 CONTROL_DRIVER_R94=PASS` | 0 |
| C1 forgeries | `forgeries-r94.py --root . --repo . --rev F --receipts-rev C --work <S>/r02-forg` | `FORGERIES=FAIL … POSITIVE=pass` (**F1**) | 1 |
| C2 counter | `curation-r94.py --root .` | `LEGS_MEASURED=16/16 Q_SHAPE_FAIL=0 Q_WSQUOT=0 Q_PUNCTQUOT=0 Q_ROWS=20 WARRANT_OK=17/17 TFREQ_OK=17/17 DUP_QIDS=0` + `CURATION_R94=PASS` | 0 |
| C2 controls | `curation-controls-r94.py --root . --work <S>/rc2` | `CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 PUNCT_NAMED=2/2 PUNCT_SHAPE_GREEN_R93=1/1 PRIOR_REGRESSION=7/7` (+`DUPCOUNT_1=1/1`) | 0 |
| C3 counter | `skill-tally-r94.py --root . --selftest …/selftest-r94.txt` | `LEGS=4/4 TAIL_OK=1 TAIL_OWNED_OK=2/2 HIST_DERIVED=2/2 HIST_PRESENT=2/2 STALE_TALLIES=0/8 CASE_RANGE_OK=2/2 MISLABELED=0` + `SKILL_TALLY_R94=PASS` | 0 |
| C3 controls | `skill-tally-r94-controls.py --root . --work <S>/rc3` | `CONTROLS=PASS CARRIED_REFUSED=6/6 MOVED_REFUSED=2/2 MOVED_PRIOR_ACCEPTED=2/2 DOUBLE_REFUSED=1/1 HEADING_ALIAS_ACCEPTED=1/1` | 0 |

Receipts: `r01-c1-verify.txt`, `r02-c1-forgeries-at-C.txt`, `r03-c2-counter.txt`,
`r04-c2-controls.txt`, `r05-c3-counter.txt`, `r06-c3-controls.txt`.

# Status of each finding at lane `HEAD d13c2ff2` (measured live, after the L1's F2/F3 amendments)

The lane consumed this seat's report while it ran and folded several findings into `ebbcbe39` (whose
message names "containment guards, receipts-rev validation, reproducible receipts"). Measured live
against the lane's own scripts, read-only, writes confined to `<S>`:

| finding | at `C` (assigned) | at `HEAD d13c2ff2` | evidence |
|---|---|---|---|
| F1 s1 dead case | FAIL, exit 1 | **closed** — `grep -c s1-schema-two-column` → `0` | `r20-residual-at-lane-head.txt` |
| F2 `--work` deleted | user data deleted | **residual** — `refuse_work_root()` is a 6-entry denylist (`/`, `/home`, `/tmp`, `/var/tmp`, `~`, `~/`); any other pre-existing dir is still wiped: `--work <S>/v2` → `USER_DATA_DELETED` | `r20-…` |
| F3 `HOME=/home/vgpnk` | present | **closed** — no `/home/vgpnk` in `expected.tsv` or the receipts | `r20-…` |
| F4 scratch path in receipt | present | **closed** — no `/fast/scratch` in any pinned receipt | `r20-…` |
| F5 symlink pin escape | reads outside tree | **closed** — `os.path.realpath(disk)` containment, commented `R94SentinelScope F5` | `r20-…` |
| F6 `--pins` read+echo | content echoed, exit 1 | **closed** — `CONTROL_DRIVER_R94=SETUP --pins outside --root: /etc/hostname`, exit 2, no content | `r20-…` |
| F7 `--receipts-rev` unvalidated | accepted revspec | **closed** — `SETUP --receipts-rev is not a 40-hex revision`, exit 2 | `r20-…` |
| F8 leftover clone | 398M left, no `finally` | **residual** — still `NO_FINALLY` | `r20-…` |
| F9 tools unpinned | drift invisible | **residual** — `grep -cE 'tools/(gate-records\|research-gate)' instrument-pins.txt` → `0` | `r20-…` |
| F10 setup traceback | `FileNotFoundError`, exit 1 | **residual** — unchanged | `r20-…` |

Residual set at `HEAD`: **F2 (denylist, not containment), F8, F9, F10**. The F2 residual is the one I
would not leave: a denylist cannot cover "an operator passed the wrong directory", which is the actual
failure mode (the list omits the tree root, any ancestor of it, and every ordinary working directory).

Also noted at `HEAD`: `curation-controls-r94.py` now prints an extra `CJK_SILENT=1/1` token alongside
the predicate the claim names — additive, the claimed tokens are unchanged.

# Receipt index (`.ufo/waves/round-94/w1/R94SentinelScope/`)

`r01-c1-verify.txt` · `r02-c1-forgeries-at-C.txt` · `r03-c2-counter.txt` · `r04-c2-controls.txt` ·
`r05-c3-counter.txt` · `r06-c3-controls.txt` · `r07-writes-scope-strace.txt` · `r08-readonly-tree.txt` ·
`r09-traversal.txt` · `r10-home-read.txt` · `r11-work-rmtree.txt` · `r12-symlink-pin-escape.txt` ·
`r13-leftovers-failing-exit.txt` · `r14-network-off.txt` · `r15-unpinned-tool-drift.txt` ·
`r16-setup-traceback.txt` · `r17-pins-regen-symmetry.txt` · `r18-credential-hostpath-sweep.txt` ·
`r19-remediation.txt` · `r20-residual-at-lane-head.txt`

# Tooling

Nothing installed or upgraded. Used only the installed `strace`, `bwrap`, `unshare`, `git 2.56.0`,
`python3 3.14.8` (all pre-existing; `pacman` untouched per the host-wide pause).

VERDICT: R94SentinelScope C1 fired — the committed forgeries battery exits 1 with `FORGERIES=FAIL` because the `s1-schema-two-column` fixture is unwinnable by construction (it writes a valid three-column table and demands `PIN_SCHEMA`), so the frozen `exit 0` / `FORGERIES=PASS` predicate is not met at carrier `C` (F1); the verify half passes.
VERDICT: R94SentinelScope C2 held — counter and controls reproduce exactly (`CURATION_R94=PASS`, `LEGS_MEASURED=16/16`, `PUNCT_NAMED=2/2`, `PUNCT_SHAPE_GREEN_R93=1/1`, `PRIOR_REGRESSION=7/7`), including with the network namespace empty.
VERDICT: R94SentinelScope C3 held — counter and controls reproduce exactly (`SKILL_TALLY_R94=PASS`, `TAIL_OWNED_OK=2/2`, `MOVED_REFUSED=2/2`, `MOVED_PRIOR_ACCEPTED=2/2`, `HEADING_ALIAS_ACCEPTED=1/1`), including with the network namespace empty.
