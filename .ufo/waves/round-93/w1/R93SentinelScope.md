# R93SentinelScope — round-93 perimeter and harm review of the committed surface

Seat: `R93SentinelScope` (sentinel; leaf, no dispatch). Round 93, lane `chousa`, L1 `ChousaR93`.
Attacked tree: carrier **C2 `754b62fb6adc60e44e12375af5461a0ebe302994`** (freeze **F2 `b7241252c2358613d3b22b7d0454d98c56dab373`** + six committed control receipts),
cloned at `/fast/scratch/hyaku/chousa-r93/R93SentinelScope/repo`. Base: `206226dc9d9baef620e7d3d30bdac5f9194a459f`.

Every check below was **run** by this seat. Commands, observed lines and exit codes are in the six receipts
copied next to this report in this folder:

| receipt | covers |
|---|---|
| `R93SentinelScope-a-scope.txt` | (1) changed-path scope |
| `R93SentinelScope-b-credential-shape.txt` | (3) credential/secret shape, host paths, host-safety keywords, network surface |
| `R93SentinelScope-c-harm.txt` | (2) `research-gate.sh --selftest`, `gate-records.py verify` |
| `R93SentinelScope-d-confinement.txt` | (4) verify/emit confinement, `/tmp`, write targets |
| `R93SentinelScope-e-c1-battery.txt` | C1 forgeries battery at C2 on both host pythons |
| `R93SentinelScope-f-claim-observations.txt` | the four claim-bearing tool invocations at C2 (byte context for the harm findings) |

Scratch (`/fast/scratch/hyaku/chousa-r93/R93SentinelScope/`) was deleted after the runs; no tool was installed
(this seat needed none), so the operator tooling directive has no entry.

---

## 1. Scope — every changed path is inside the lane's write scope

`git diff --name-status 206226dc..754b62fb` → **17 paths, all additions, rc 0** (receipt `-a-scope.txt`):

```
.ufo/waves/round-93/claims.json
.ufo/waves/round-93/claims.md
corpus/evidence/round93/control-driver-r93.py
corpus/evidence/round93/controls/expected.tsv
corpus/evidence/round93/controls/receipts/c1-gate-r89.txt
corpus/evidence/round93/controls/receipts/c1-harm-setup.txt
corpus/evidence/round93/controls/receipts/c1-harm.txt
corpus/evidence/round93/controls/receipts/c1-mutants-r89.txt
corpus/evidence/round93/controls/receipts/c2-prior-controls.txt
corpus/evidence/round93/controls/receipts/c2-prior-landing.txt
corpus/evidence/round93/controls/selftest-r93.txt
corpus/evidence/round93/curation-controls-r93.py
corpus/evidence/round93/curation-r93.py
corpus/evidence/round93/forgeries-r93.py
corpus/evidence/round93/instrument-pins.txt
corpus/evidence/round93/skill-tally-r93-controls.py
corpus/evidence/round93/skill-tally-r93.py
```

All 17 are files of the lane repository `chousa-shokunin` (its own `.git`; the fleet root gitignores
`*-shokunin/`, so the lane is not a subdirectory of the fleet repo). Path-by-path classification:

- **15 files** under `corpus/evidence/round93/` — the round's own evidence directory. In scope.
- **2 files** `.ufo/waves/round-93/claims.md` and `claims.json` — the wave folder inside the lane repo; the
  frozen predicate set the assignment itself names as the round's claim document. In scope (this seat's own
  report path, `.ufo/waves/round-93/w1/R93SentinelScope.md`, is the same folder family and is deliberately
  **not** pinned — see §4 finding F-4).

Flagged surfaces, each verified **unchanged** by `git diff <base>..<C2> -- <path>` (all 0 paths, receipt `-a-scope.txt`):

| flagged path | changed at base..C2 | changed at base..lane-HEAD (context) |
|---|---|---|
| `tools/` (incl. `research-gate.sh`, `gate-records.py`) | **0** (diff empty, rc 0) | **0** |
| `corpus/SOURCES.md` | **0** | **0** |
| `corpus/knowledge/` | **0** | **0** |
| `SKILL.md` | **0** | **0** |
| `MANIFEST.json` | **0** (tracked by the fleet repo; `git diff -- MANIFEST.json` empty) | **0** |
| `considerthese/` | **0** | **0** |
| `.scratch/` | **0** | **0** |
| `.ufo/state/` | **0** (the lane has no `.ufo/state/`; the fleet root's is untouched) | **0** |
| sibling repos / fleet-root `scripts/` | **0** (`git -C /home/vgpnk/Projects/shokunin diff -- scripts/ .ufo/state/ MANIFEST.json` empty) | **0** |

The lane's working tree at inspection time also showed uncommitted `LOG.md`/`SCORECARD.md` edits and untracked
`corpus/evidence/round93/after/`, `.../census-{start,end}.txt`, `.../evidence-before/`, `corpus/lessons/round-93.md`
— **none of these are inside the base..C2 diff**; they are the L1's later integration working set (lane HEAD had
already advanced to `c1ebb1d9` "carrier C6" by the end of this seat's run). Not attributable to the attacked pair.

**Item 1 verdict: FIRES — scope is clean.** No changed path touches `tools/`, `corpus/SOURCES.md`,
`corpus/knowledge/`, `SKILL.md`, `MANIFEST.json`, a sibling repo, the fleet root, `.scratch/` or `.ufo/state/`.

---

## 2. Harm — the subject tools, unchanged

**`tools/research-gate.sh --selftest`** (host `python3` 3.14.8; run in the clone at C2 with `TMPDIR` pointed at
this seat's scratch; receipt `-c-harm.txt`):

```
ok-case  283 bash-pin-override-fake       exit=2
RESEARCH_GATE_SELFTEST: PASS (283 cases, 0 skipped)
EXITCODE=0
```

Expected `PASS (283 cases, 0 skipped)` — **observed exactly**, exit 0. Wall time 806 s; the tool's own r71 note
records that case 258 is unbounded on a contended host, so the long run is expected, not a stall. The same
verdict line is what the committed `corpus/evidence/round93/controls/selftest-r93.txt:285` carries.

**`tools/gate-records.py verify`** — the tool has a single read-only mode (`verify --root ROOT [--repo REPO]
files…`; it opens files read-only and prints `GATE_RECORD <file>:<line> <sid> OK|FAIL`; there is no write path
in `tools/gate-records.py` — `grep` for `open(...,'w')` finds none).

- against the lane worktree's uncommitted round-93 lesson: `GATE_RECORD corpus/lessons/round-93.md:20 S001 OK` /
  `GATE_RECORDS files=1 records=1 ok=1 fail=0` / **EXITCODE=0**;
- against the **committed** C2 clone, where `corpus/lessons/round-93.md` does not exist:
  `GATE_RECORDS_ERROR missing corpus/lessons/round-93.md` / **EXITCODE=2**.

That exit 2 is the tool's correct setup error, not a defect: the round's lesson file is a later L1 artifact and
is not in the C2 tree (it is untracked in the worktree). `git diff base..HEAD -- corpus/lessons/` shows 0 changed
paths at every revision inspected, so `corpus/lessons/round-93.md` is still uncommitted at lane HEAD — noted as
§6 finding F-5.

**`git diff 206226dc..754b62fb -- tools/`** → empty output, rc 0. `tools/research-gate.sh` and
`tools/gate-records.py` are byte-identical at base, C2 and lane HEAD.

**Item 2 verdict: HOLDS.** Both subject tools run unchanged with the expected output and exit 0; `tools/` is
untouched at every revision checked.

---

## 3. Credential / secret shape

Scan over all 17 changed paths (receipt `-b-credential-shape.txt`):

- **No secret-shaped material.** Zero matches for `BEGIN … PRIVATE KEY`, `AKIA[0-9A-Z]{16}`, `ghp_…`,
  `sk-…`, `xox[baprs]-…`, `bearer <token>`, `api_key =`, `secret =`, `password =`. The only hits for the words
  *token*/*secret* are the word "tokens" in prose and the two selftest case names
  `fail-secret-shaped` (`controls/selftest-r93.txt:16`) and `metadata-registry-no-token-id` (:192) — labels, not
  values.
- **No network surface** in the six new `.py` files: zero matches for `curl`, `wget`, `urllib`, `requests.`,
  `urlopen`, `socket.`. The round is network-free by construction.
- **Host paths outside the lane — two, both benign, both named here with file:line:**
  - `corpus/evidence/round93/controls/expected.tsv:4` — the `c1-harm` instrument row embeds
    `HOME=/home/vgpnk` for its `git show` call. This is an absolute path outside the lane in a committed file.
    It does **not** leak a credential: the row reads a local blob (`git show <rev>:tools/gate-records.py`) and
    never contacts a remote. Measured: with `HOME=/home/vgpnk`, with `HOME` unset, and with the driver's own
    scrubbed `HOME=<tree>` the blob is **byte-identical** (`sha256 905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60` in
    all three cases), so the override is a portability wart, not a dependency. Smallest remediation if the L1
    wants it: `git -c safe.directory='*' -C @ROOT@ show …` (measured rc 0, same blob) or drop the `HOME=`
    prefix entirely.
  - `corpus/evidence/round93/controls/receipts/c1-harm-setup.txt:5` — the committed receipt body quotes the
    emitter's scratch path (`HARM_RECHECK_ERROR base-tool missing: /fast/scratch/hyaku/chousa-r93/c1/emit2/absent-tool.py`).
    A scratch path of the L1's own run, not a secret and not a home path. It is the only committed receipt of
    the six that embeds a host path.
- `.ufo/waves/round-93/claims.md:4-5` cites the fleet-root census command by absolute path
  (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`) — documentation prose in the claim document, not
  executed code.

**Item 3 verdict: FIRES (minor, informational) — no live credential, private key, token or secret is present in
the committed surface; two host paths are named above (an absolute `HOME=` inside a committed instrument row and
a scratch path inside one committed receipt), neither of which carries or transports a secret.**

---

## 4. Confinement

**(a) Does the driver's `verify` path write outside `--work`?** **No.** Static: in verify mode the only writes
are `control-driver-r93.py:418` `os.makedirs(work)` and `:476` `open(os.path.join(work, "fresh-<case>.out"), "w")`;
the receipt-directory writes (`:424`, `:431`) are inside the `if a.mode == "emit"` branch. Empirical: a
whole-tree `sha256`/mtime snapshot of the clone before and after the scored verify run diffs **empty**, and
`git status --porcelain` in the clone is empty afterwards (receipt `-d-confinement.txt`). The C2/C3 control
batteries were checked the same way: `curation-controls-r93.py --root .` and `skill-tally-r93-controls.py
--root .` leave the `--root` tree byte-identical (before/after `sha256` diff empty). The `verify` path never
writes under the receipts directory.

**(b) Does `emit` refuse without `--receipts`?** **Yes.** `control-driver-r93.py:421-423`:

```
$ python3 -B corpus/evidence/round93/control-driver-r93.py emit --root . --work $S/w/emit1 --rev 754b62fb…
CONTROL_DRIVER_R93=SETUP emit requires an explicit --receipts
EXITCODE=2
```

Note the guard is `"--receipts" not in sys.argv` (a literal argv test), so the `--receipts=PATH` spelling is
**also** refused (measured: same SETUP line, exit 2). That is fail-closed, not a hole — but it means the
documented `--receipts D` form is the only one that works. Worth one word to the L1, no security impact.

**(c) Does any new tool write under `/tmp` regardless of `TMPDIR`/`--work`?** **No.** The only `TMPDIR`
reference in the six new `.py` files is `control-driver-r93.py:388`, the `--work` **default**
(`$TMPDIR` else `/fast/scratch/hyaku` — never `/tmp`). The three control batteries take `--work` as a required
argument and write only under it (`forgeries-r93.py:78-79`, `curation-controls-r93.py:90-91`,
`skill-tally-r93-controls.py:70-71`). `curation-r93.py` and `skill-tally-r93.py` write nothing at all (every
`open()` in them is a read).
One indirect path, named for completeness and **not** on any scored path:
`skill-tally-r93.py:58` runs `bash tools/research-gate.sh --selftest` when `--selftest` is omitted, and that
(unchanged) gate tool mktemps under `${TMPDIR:-/tmp}` (`tools/research-gate.sh:4259,4498,4501`). It honours
`TMPDIR`; the scored C3 command always passes `--selftest corpus/evidence/round93/controls/selftest-r93.txt`,
so the gate's temp path is not taken. (I confirmed my own first, TMPDIR-less selftest attempt did leave a
`/tmp/chousa-gate-pin.eyhdIl` behind; I removed it, and no `/tmp/chousa-*` newer than my start remains.)

**(d) Write-through into the live lane from the control batteries — measured, none.** The C2 controls
`mirror()` symlinks the *live* `corpus/captures` and `corpus/evidence/round57` into each scratch tree, but it
copies `corpus/SOURCES.md` and the two knowledge entries as real copies and the counters only read. Measured on
the **live lane root**: `sha256` of `corpus/SOURCES.md` and the two routed entries before and after a full
`curation-controls-r93.py --root .` run — **identical**. (The `instrument-pins.txt`/receipt bytes that moved
during that window were the L1's own concurrent F5/C6 re-cut, not the battery's writing; a second
`before/after` pair six seconds apart with no tool running was **stable**, and `git status` showed those files
matching HEAD.)

**Item 4 verdict: FIRES (minor) — the verify path is confined to `--work`, `emit` refuses without an explicit
`--receipts`, and no new tool writes under `/tmp`; two nits are named above (the `--receipts=PATH` spelling is
refused by the argv-literal guard; `skill-tally-r93.py`'s no-`--selftest` branch reaches the unchanged gate's
`${TMPDIR:-/tmp}` fallback).**

---

## 5. Host safety

`grep -n -E 'sysctl|sudo |systemctl|/etc/init|launchctl|service [A-Za-z]+ (start|restart|stop)'` over all 17
changed paths → **zero matches** (receipt `-b-credential-shape.txt`). No new file mutates a sysctl, runs `sudo`,
or restarts a service. The only `sudo`/`sysctl` strings anywhere near this round are the prose in the wave
dispatch (`build_spec.py:61-62,230`) restating the prohibition — not code.

The only host-state surface the round's tools touch is **git**: the new tools shell out to `git show`,
`git clone --shared`, `git archive`. Every such call is a **local** object read; no remote, no push, no fetch.

**Item 5 verdict: HOLDS.**

---

## 6. Findings on the attacked surface (beyond the five checklist items)

**F-1 (HIGH, C1 predicate not met at the attacked carrier — corroborates `R93ExecC1Repro` / `R93ReviewerC1`).**
The C1 forgeries battery at C2 does not run on this host. Receipt `-e-c1-battery.txt`.

- Host `python3` is **3.14.8**; `corpus/evidence/round93/forgeries-r93.py:51` calls `tf.extractall(dest)` with
  **no `filter=` argument**. Python 3.14 defaults to the `data` filter, which refuses the **committed** absolute
  symlink `.ufo/waves/round-35/w2/MutGrepShimPath/shims/b/grep -> /bin/false`:
  `tarfile.AbsoluteLinkError: '.ufo/waves/round-35/w2/MutGrepShimPath/shims/b/grep' is a link to an absolute path`,
  **EXITCODE=1**, and no `FORGERY_REFUSED` line is printed at all.
- Under `python3.13.16` the extraction succeeds but the extracted `git archive` tree has **no `.git`**, so the
  fresh legs that need a git dir fail (`c1-gate-r89` via `gate-records-r89 --repo @ROOT@`; `c1-harm` via
  `git -C @ROOT@ show`): `FRESH_OK=4/6`, and the battery prints
  `FORGERY_REFUSED=0/2 PRIOR_ACCEPTED=0/2 DERIVE_OK=0/1 POSITIVE=fail`, **EXITCODE=1**.
- The predicate the frozen claim demands is `FORGERY_REFUSED=2/2 PRIOR_ACCEPTED=2/2 DERIVE_OK=1/1 POSITIVE=pass`.
  At C2 it is unreachable on this host in either interpreter.
- Smallest remediation: `tf.extractall(dest, filter="tar")` (measured: extracts cleanly, preserves the three
  symlinks) **and** build the fixture as a shared clone (`git clone --shared` + `checkout`), not a
  `git archive` tree — a clone carries the `.git` the fresh legs need. Both are what the lane has already done
  downstream: lane HEAD's `forgeries-r93.py` uses `clone()` and the battery at HEAD prints
  `FORGERY_REFUSED=2/2 PRIOR_ACCEPTED=2/2 DERIVE_OK=1/1 REGRESSION_REFUSED=2/2 POSITIVE=pass`, **EXITCODE=0**.
  So the defect is real at the attacked pair and already repaired downstream — the finding matters because C2
  is the pair this wave scored.

**F-2 (MEDIUM — the pin walk is coupled to a mutable wave artifact).** `corpus/evidence/round93/instrument-pins.txt`
pins `.ufo/waves/round-93/claims.md` (row 9) and `.ufo/waves/round-93/claims.json` (row 10) — the frozen claim
document **and its machine form**. The L1 amends that file after the freeze (F4 did: `596eabc9` "wave findings
applied … claims narrowed"), and the C2 pins table still carries the C2 blob's digest. Measured on a copy of the
C2 clone: appending one line to `.ufo/waves/round-93/claims.md` makes the scored verify print
`RECEIPT PINS FINDING PIN_DISK_MISMATCH path=.ufo/waves/round-93/claims.md` and
`PINNED_FILES=21/22 … CONTROL_DRIVER_R93=FAIL`, **EXITCODE=1** — a genuine-row-moved failure caused by an
edits to the claim text, not to any instrument. The lane mitigates this by re-cutting the pins table at each
carrier (HEAD's row 9 digest `a09f70db…` matches HEAD's `claims.md`), so it is a coupling to record, not a
live break. It is the same class as the pre-round self-pin defect named in the assignment (the `84998563` pair
"self_pin took the pin dict for the pins path").

**F-3 (MEDIUM — the minus-self digest is not enforced at C2).** `control-driver-r93.py:290-294` treats the pins
file's own row as a *minus-self* digest (`pins_file_sha_minus_self`), and `self_pin` at `:368` re-derives it
from the carrier blob. But the **self row is not required**: measured on a copy of the C2 clone, deleting the
`corpus/evidence/round93/instrument-pins.txt` row from the table entirely still yields
`RECEIPT PINS OK 21/21 pinned files byte-identical RECEIPT_PINS_OK=6/6` and
`PINNED_FILES=21/21 … CONTROL_DRIVER_R93=PASS`, **EXITCODE=0** — a PASS with the table's own coherence anchor
removed. (Deleting a *receipt* row is correctly caught: `RECEIPT_UNPINNED:c1-harm` → `PINNED_FILES=20/21 …
CONTROL_DRIVER_R93=FAIL`, EXITCODE=1.) The lane has since closed this: HEAD's driver carries
`PIN_SELF_ROW_ABSENT path=<pins>` (`control-driver-r93.py:304-307`) and the HEAD battery scores
`OK self-row-deleted: r93 rc=1 (PIN_SELF_ROW_ABSENT)`. At the attacked pair C2 the K4-style vacuity is live.

**F-4 (LOW — the pins table deliberately excludes the wave output folder, so seat reports cannot move the score).**
`instrument-pins.txt` at C2 pins 22 rows: 15 instrument/expectation/claim rows, 6 receipt rows and the self row.
No row names `.ufo/waves/round-93/w1/**`, so the thirteen seat reports landing in this folder — including this
one — cannot perturb the C1 pin walk. **HOLDS**, and worth stating as a positive.

**F-5 (LOW — the round's own artifacts are uncommitted).** `corpus/lessons/round-93.md` (the file the frozen
claims say the mistake is mined into), `corpus/evidence/round93/after/`, `.../census-{start,end}.txt` and
`.../evidence-before/` are **untracked in the lane worktree** at every revision I inspected (lane HEAD included):
`git ls-tree -r --name-only HEAD corpus/evidence/round93/` lists only the 15 committed files, and
`git status --porcelain` shows `?? corpus/lessons/round-93.md`, `?? corpus/evidence/round93/after/`,
`?? corpus/evidence/round93/census-{start,end}.txt`, `?? corpus/evidence/round93/evidence-before/`. The
frozen claim text points at `corpus/evidence/round93/census-start.txt` and
`corpus/evidence/round93/evidence-before/c1-prior-accepts.txt` as committed evidence; at the attacked pair
**neither path exists in the tree**, and `evidence-before/` holds only `c2-prior-accepts.txt` and
`c3-prior-accepts.txt` (no `c1-prior-accepts.txt` anywhere on the lane). That is why `gate-records.py verify`
exits 2 on the committed tree (§2). Not a scope breach — the L1 owns the integration — but the C1 "Before"
measurement the claim cites has no committed artifact at C2.

**F-6 (LOW — the machine form `claims.json` and the prose `claims.md` disagree on C2's control tokens).**
`claims.json` (C2, pinned row 10) requires C2 controls `['CONTROLS=PASS','FORGERY_REFUSED=4/4',
'PRIOR_ACCEPTED=4/4','FORGERY_REFUSED=7/7']` and C3 controls `['CONTROLS=PASS','TAIL_REFUSED=1/1',
'TAIL_PRIOR_ACCEPTED=1/1']`. The instruments print `CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 WS_SHAPE_GREEN_R92=1/1
DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7` (C2) and `TAIL_REFUSED=2/2` (C3) — the `FORGERY_REFUSED=4/4` /
`PRIOR_ACCEPTED=4/4` / `TAIL_REFUSED=1/1` strings are **never printed** by any of the three tools
(`grep` over the full C2 controls output: only `FORGERY_REFUSED=7/7` appears, inside the r90 regression line).
The prose `claims.md` matches the instruments. The machine form is the unsatisfiable one.

**F-7 (LOW — one committed receipt body is not path-stable).** `controls/receipts/c1-harm-setup.txt:5` embeds the
emitter's scratch path; re-emitting that case under a different `--work` yields a different body
(`…/R93SentinelScope/w/emit3work/absent-tool.py`). The driver's `check_body` compares required **tokens**, so the
row still scores (`HARM_RECHECK_ERROR`); only the byte-level body differs. Consequence for a re-cut: the receipt
digest changes with the scratch path, so the pins table must be re-cut after any re-emit from a new path.

**F-8 (INFORMATIONAL — `resume_continuity_v1` does not exist in this lane).** The role's continuity clause
requires verifying that every `resume_continuity_v1` rejection causes zero mutation. `grep -rn
resume_continuity_v1 tools/ corpus/` in the lane returns **no matches**; the only occurrences anywhere are
historical wave reports (rounds 25/37/38/60 and other lanes' `.ufo/waves/` prose), which themselves record that
no such runtime exists in chousa. There is therefore no canonical run logic and no rejection path in the
attacked surface to exercise: **n/a, not passed**. The nearest analogous refusal in this round is the driver's
own `SETUP path escapes base` guard (`control-driver-r93.py:120-127`), and *that* refusal is zero-mutation:
measured on the C2 clone, `verify --root <non-repo tree>` exits with the SETUP line and leaves the tree
byte-identical.

**Context (not a finding against C2):** the lane advanced past the attacked pair during this seat's run —
HEAD moved `881a541f` (F4/C5) → `c1ebb1d9` (F5/C6) — and the C1 battery at HEAD now prints
`FORGERY_REFUSED=2/2 PRIOR_ACCEPTED=2/2 DERIVE_OK=1/1 REGRESSION_REFUSED=2/2 POSITIVE=pass` (EXITCODE=0), i.e.
F-1 is repaired downstream. The C1 `verify` half at HEAD/F5-C6, however, prints
`PIN_OK=0/6 … RECEIPT SELF_PIN FINDING SELF_DRIFT … CONTROL_DRIVER_R93=FAIL` (EXITCODE=1) because the six
committed receipts carry `computed_against=3789608d…` while HEAD's pins/self-pin are cut at F5/C6 — the L1 is
mid-re-cut. Out of this seat's attacked pair; recorded because it was observed.

---

## 7. What I did **not** verify

- I did not adjudicate any claim's kill rules — the C1/C2/C3 predicates are the executors' and reviewers'
  surfaces. I ran the four claim-bearing commands only to fix the byte context in which my harm findings sit
  (receipt `-f-claim-observations.txt`); each result there is labelled as context, not as a claim verdict.
- I did not run the r92 comparison legs except where the C1 battery's own output forced them
  (`PRIOR_ACCEPTED` lines are the battery's, not mine).
- I did not exercise the `emit` path against a live receipts directory in the lane (it would have written
  committed receipts); the guard was tested with `--receipts` pointed at scratch.
- No tool was installed or upgraded, so the operator tooling directive records nothing.

---

VERDICT: R93SentinelScope C1 fired — the C2 forgeries battery cannot run on this host (3.14.8 `tarfile.AbsoluteLinkError` at `forgeries-r93.py:51`, exit 1; under 3.13 `FORGERY_REFUSED=0/2 … POSITIVE=fail`, exit 1), the C2 pins table does not require its own self row (`PINNED_FILES=21/21 … PASS`, exit 0), and the pin walk is coupled to the mutable `.ufo/waves/round-93/claims.md` (one appended line → `PIN_DISK_MISMATCH`, exit 1); the verify half itself holds exactly at C2 (`CONTROL_DRIVER_R93=PASS`, 22/22, exit 0).
VERDICT: R93SentinelScope C2 held — no scope, harm, credential or confinement defect on C2's own surface: the changed paths are lane-only, `tools/` is byte-identical, the counter and controls print their frozen fields at exit 0, the C2 controls write nothing into the live lane, and the only defects found are the machine-form token drift in `claims.json` and the uncommitted `evidence-before/c1-prior-accepts.txt` the claim cites.
VERDICT: R93SentinelScope C3 held — the tally counter and its controls print their frozen fields at exit 0, the counter writes nothing, `skill-tally-r93.py`'s only host-state reach is the unchanged gate's `${TMPDIR:-/tmp}` fallback on a branch the scored command never takes, and the C3 machine form's `TAIL_REFUSED=1/1` is likewise never printed (prose form is the satisfiable one).
