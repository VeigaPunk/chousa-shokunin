# R80SentinelA — scope, leak and provenance audit of round 80's committed artifacts

seat `R80SentinelA` (leaf, no dispatch) · lane `chousa` · round 80
base revision (round-79 lane tip): `b7803829922770b890e9f4efdd30d12c3695439a`
**revision measured: `44d09edfc20dba26ee8d58a93d365989916a2692`** — HEAD moved during the audit
(`0d253c95…` at 00:00:43 → `44d09edf…`, commit *"round-80: register S199-S202 with GATE-RECORD lines,
land the re-run controls"*); every scan below was re-run at `44d09edf` and the worktree is clean on
every path scanned (`git status --porcelain -- corpus/evidence/round80 corpus/evidence/round79/matrix-battery-v6.py
corpus/evidence/round76/loader-matrix-v3.py` → no output, exit 0; receipt `03-sha256.txt`).

Method: read-only. Committed bytes only (`git show <rev>:<path>` or a clean worktree), plus two
scratch reproductions under `/fast/scratch/hyaku/chousa-r80/R80SentinelA/` (deleted before yield).
Nothing outside this folder was written; no lane or fleet git/jj mutation; no network; no tool
installed or upgraded (none was needed — `python3`, `git`, `sha256sum`, `grep` were used as installed).

Receipts (all in `receipts/`, sha256 binds them):

| receipt | sha256 |
|---|---|
| `00-revision.txt` | `9adc29e808069ae2433f09c57b095209f9eb95b6cd5336f17d2fda56c8ad2f9c` |
| `01-leak-scan.txt` | `312e2f5ab3907bda56f5b1431f6904727ffd8114ef4737dcae649f4ae1088962` |
| `02-rev-binding.txt` | `7299d619a5fab02bcf3a541b8cdc5908549c14e82699254a615ada3502c873ae` |
| `03-sha256.txt` | `9b8c2bdaea0987ba2486ca6c23a70de5108d771ab0c9f28e32b7a7d8ef3944ff` |
| `04-v7-limits.txt` | `588563a4c11507164841748c8891598a51531dc080a9fd73e3b0f0f8b8aa624a` |
| `05-wave-scope.txt` | `fada409b7274995cc3ba90b7d2fd477fdf4911ed3622b95e2f0fa804bceefe1f` |
| `06-fresh-leg-ground-truth.txt` | `1b7376a01910a9c2acf4aa8b5b03022d5a17813c0281fe6068d7f3bccaf7bac5` |
| `07-receipt-provenance.txt` | `5d93a541bc286261bdbbd0192ac0f9f11c5398c56dc6b9c82d60fb76bb0aeae4` |
| `08-duplication-and-oracle-crash.txt` | `e900a1369330079382e2c29fec4b853b0c8fbef6e20f18d3cd052823bc38c7d5` |
| `09-rename-defect-repro.txt` | `79e4cb562e2a69f3fc60e5835dce118050a72d790e8e3024498e431f73ad02b8` |

---

## 1. Leak / scope scan of `corpus/evidence/round80/` and `.ufo/waves/round-80/census-start.txt`

receipt `01-leak-scan.txt`, revision `44d09edf`.

| probe | command | observed |
|---|---|---|
| `/tmp`, `/var/tmp` | `grep -rnE "/tmp/\|/var/tmp/" corpus/evidence/round80/ .ufo/waves/round-80/census-start.txt` | `# exit=1` — **no hit** |
| network | `grep -rnE "\b(urllib\|requests\|httpx\|curl\|wget\|socket)\b" …` | one hit, `.ufo/waves/round-80/census-start.txt:2` → `chousa W04 S053 duplicate url docs.python.org/3/library/socket.html across scopes` — a SOURCES duplicate-URL census row that happens to contain `socket.html`; **false positive** — `grep -nE "import (socket\|urllib\|http\|requests)\|urllib\.\|requests\.\|socket\.\|curl \|wget " corpus/evidence/round80/*.py corpus/evidence/round80/forgers/*.py` → `# exit=1`, no import or call |
| repo-mutating `subprocess` | `grep -rnE "git (commit\|push)\|jj (commit\|push\|new\|describe)\|subprocess" …` | no `git commit`, no `git push`, no `jj`. The subprocess calls are: `gate-grounding-check.py:57` `git -C <lane> <rev-parse\|show\|ls-tree\|cat-file>` (read-only); `matrix-battery-v7.py:197,:442` `sys.executable <subject>` (subject execution, by design); `matrix-battery-v7.py:657` `git -C <lane> rev-parse master` (read-only); `oracle-check.py:57` `sys.executable <battery>` |
| credentials | `grep -rnE "BEGIN .*PRIVATE KEY\|ghp_\|sk-[A-Za-z0-9]\|op://\|AKIA[0-9A-Z]{16}\|token[ _-]?literal" …` | `# exit=1` — **no hit** |
| sibling lane / fleet write target | `grep -rnE "Projects/shokunin/(scripts\|\.ufo/state\|MANIFEST)\|tsukuroi-\|kasegi-\|souji-\|kama-\|mado-\|kotoba-\|kumitate-" corpus/evidence/round80/` | `# exit=1` — **no hit** |
| writes | `grep -nE "open\(\|write_text\|mkdir\|rmtree" corpus/evidence/round80/*.py corpus/evidence/round80/forgers/*.py` | every write is under the caller's `--work`: `matrix-battery-v7.py:300` `d.mkdir(parents=True)` where `d = work / token_hex(8)` (`:299`), `:302` `target.write_text(...)`; `rmtree` only on directories it created (`:482,:484,:487,:492,:526,:639,:641`). `gate-grounding-check.py` has no write call; `oracle-check.py` only `work.mkdir` (`:48`); `forgers/a10-payload-decode.py` has no write, no `open`, no `subprocess` |
| scratch references | `grep -rn "/fast/scratch" corpus/evidence/round80/` | three hits, all sanctioned: `controls/oracle-before-r80.txt:2` and `controls/v7-legit-matrix-r80.txt:2` name `/fast/scratch/hyaku/chousa-r80/l1/{oracle,v7}` (inside the round's scratch tree), and `forgers/a10-payload-decode.py:6` mentions the **deleted** round-79 clone `/fast/scratch/hyaku/chousa-r79/R79CriticA/lane` in its provenance docstring only (`:34-35` resolves the table root from `LOADER_MATRIX_LANE` or `parents[4]`, never from that literal) |

**ITEM 1: CLEAN** — no `/tmp` or `/var/tmp` path, no network call, no repo-mutating subprocess, no
credential-shaped string, no sibling/fleet write target, every write target under `--work`.
Two qualifications carried forward, both reported below as appendix findings: the battery exports the
lane root and the full environment into untrusted subject code (F4), and the only `/fast/scratch`
literals are scrubbed-path provenance notes, not live reads.

## 2. Do the control receipts name a revision?

receipt `02-rev-binding.txt`, revision `44d09edf`. There are **7** receipts under
`corpus/evidence/round80/controls/` at this revision (4 were present at `0d253c95`; the integration
commit `44d09edf` added `grounding-before-r80.txt`, `oracle-before-r80.txt`, `v7-legit-matrix-r80.txt`).

| receipt | 40-hex `REV=`/`LANE_REV=` | line | 40-hex tokens | `# command:` | `# exit:` |
|---|---|---|---|---|---|
| `grounding-before.txt` | yes | `:4 LANE_REV=b7803829…` | 1 | 1 | 1 |
| `grounding-before-r80.txt` | yes | `:4 LANE_REV=b7803829…` | 1 | 1 | 1 |
| `oracle-structure-v6-accepted.txt` | **no** | — | **0** | 1 | 1 |
| `oracle-before-r80.txt` | **no** | — | **0** | 1 | 1 |
| `v7-legit-matrix-after.txt` | yes | `:3 LANE_REV=b7803829…` | 1 | **0** | **0** |
| `v7-legit-matrix-prefreeze.txt` | yes | `:5 LANE_REV=b7803829…` | 1 | 1 | **0** |
| `v7-legit-matrix-r80.txt` | yes | `:5 LANE_REV=b7803829…` | 1 | 1 | 1 |

- **5 of 7** carry a 40-hex revision line; **2 do not**, and neither carries any 40-hex token at all:
  `corpus/evidence/round80/controls/oracle-structure-v6-accepted.txt` and
  `corpus/evidence/round80/controls/oracle-before-r80.txt` (grep for `^[A-Z_]*REV=` exits 1 on both).
- `REV=worktree` appears **0** times anywhere under `corpus/evidence/round80/`
  (`grep -c 'REV=worktree'` → 0 on every file), so the round-79 D6 form is gone; the surviving form
  of the defect is the two revision-less oracle receipts.
- `oracle-structure-v6-accepted.txt` is the receipt `claims.md:29-31` cites as C1's **do-nothing
  control**, so the round's own before-control for its lowest axis is the receipt that does not name
  the revision it was measured at. `oracle-before-r80.txt` is the re-run of the same control and has
  the same gap.
- The newly landed `v7-legit-matrix-r80.txt` does carry command + `LANE_REV` + `# exit: 0`; the older
  `v7-legit-matrix-after.txt` carries none of the three (see finding F3).

**ITEM 2: FINDING** — 2 of 7 control receipts (`oracle-structure-v6-accepted.txt`,
`oracle-before-r80.txt`) name no revision; 0 use `REV=worktree`. This is round-79 routed defect 6
("a control receipt names the revision it was measured at") recurring in the receipts of the round
that was meant to adopt it.

## 3. Declared instrument sha256 vs the committed bytes

receipt `03-sha256.txt`. Worktree and `git show HEAD:<path>` agree for all four files, and
`git status --porcelain` over them prints nothing.

| path | `sha256sum` (worktree = `HEAD` bytes) | `claims.md` table | match |
|---|---|---|---|
| `corpus/evidence/round80/matrix-battery-v7.py` | `35351b2328bb6a284da13e61240a6ec598f39a148b8d8948d4e3d60dd78d914d` | `claims.md:13` same | yes |
| `corpus/evidence/round80/oracle-check.py` | `580233adaa1cf23b3a24012d05d7e5a2e313f7f4628d382f245433117c5e0289` | `claims.md:14` same | yes |
| `corpus/evidence/round80/gate-grounding-check.py` | `d9e426216665a098cd90adf8fbf5e5dd62e02dc7b5b707c322b404b3eb55c553` | `claims.md:15` same | yes |
| `corpus/evidence/round80/forgers/a10-payload-decode.py` | `3cb234be36a3d0d5d5523f16e5b7bb6926bbd0be8d0701d6229f0d8690ca9f64` | `claims.md:16` same | yes |

The two pins `claims.md` also declares reproduce on the committed bytes:
`corpus/evidence/round79/matrix-battery-v6.py` → `bb91406e9130d9a1960d99226c69380435fc933385db79e0e6ea6b5542a61e1d`
(`claims.md:17`), `corpus/evidence/round76/loader-matrix-v3.py` →
`b79d6441057a01b27eb465c6b0625cd46502114f8b622b370c2cd2805c81913f` (`claims.md:18`).

**ITEM 3: CLEAN** — 6 of 6 declared digests reproduce byte-exactly; no instrument moved between the
freeze commit and `44d09edf`.

## 4. Declared instrument limits of `matrix-battery-v7.py`

receipt `04-v7-limits.txt`; instrument sha `35351b23…914d`.

| question | command | observed |
|---|---|---|
| hardcoded absolute path? | `grep -nE "\"/[A-Za-z]\|'/[A-Za-z]" matrix-battery-v7.py` and `grep -nE "/home/\|/fast/\|/tmp/" …` | both `# exit=1` — **none**. Paths derive from `HERE = __file__.resolve().parent` (`:100`), `LANE = HERE.parents[2]` (`:101`), `WITNESS = LANE / "corpus/evidence/round76/loader-matrix-v3.py"` (`:125`) |
| `mkdtemp()` ignoring `TMPDIR`/`--work`? | `grep -nE "mkdtemp\|TemporaryDirectory\|tempfile\|TMPDIR" matrix-battery-v7.py` | `# exit=1` — no temporary-directory API at all. `--work` is `required=True` (`:552`) and validated (`work.is_dir()`, else exit 2); every emitted copy is `work / token_hex(8)` (`:299`), every run dir `run.mkdir()` under `--work` (`:588`, `:604`) |
| reads a file outside the lane? | `grep -n "HERE =\|LANE =\|WITNESS ="` + read sites | `POSITIVES`, `FORGERS`, `ORACLES`, `WITNESS` are all `LANE / …` (`:103`, `:106`, `:119`, `:125`; `R76F`/`R79F` at `:105`/`:117`); the only caller-supplied read is `--matrix` (`:551`), which may legitimately point outside the lane |

**ITEM 4: CLEAN** on all three questions asked. Three notes, each evidenced in the same receipt and
carried into the appendix:

- **N4a** `_lane_rev()` (`:657`) runs `git -C <lane> rev-parse master` — it names the *branch tip*,
  not the worktree bytes measured. And `matrix-battery-v7.py` does not exist at the revision the v7
  receipts print: `git cat-file -e b7803829:corpus/evidence/round80/matrix-battery-v7.py` →
  `fatal: path … exists on disk, but not in 'b7803829…'`, `# exit=128`; the file was first added in
  `0f59b985`. So `LANE_REV=b7803829…` in those receipts cannot reproduce the instrument (finding F5).
- **N4b** `run_matrix` builds `env = dict(os.environ, LOADER_MATRIX_CHILD_TIMEOUT=…, LOADER_MATRIX_LANE=str(LANE))`
  (`:194-195`) and passes it to every subject (`:200`); `_witness_out` does the same (`:439-440`).
  The full seat environment and a path to the whole lane are handed to untrusted subject code
  (finding F4).
- **N4c** `_rename` (`:231-282`) renames `ast.Name`, `ast.arg`, def/class names, handlers and
  global/nonlocal names, but never `ast.Attribute.attr`: a class-body attribute bound as a `Name`
  is renamed while `obj.attr` reads keep the old spelling. Reproduced in F2.

## 5. Wave scope: does any committed file under `.ufo/waves/round-80/` name a fleet-repo or sibling-lane path as a write target?

receipt `05-wave-scope.txt`, revision `44d09edf`.

```
$ git ls-tree -r --name-only HEAD -- .ufo/waves/round-80
.ufo/waves/round-80/build_spec.py
.ufo/waves/round-80/census-start.txt
.ufo/waves/round-80/w1-dispatch.json
.ufo/waves/round-80/w1-spec.json
.ufo/waves/round-80/w1-validate.err
```

- `w1-spec.json`: `reportDir` = `.ufo/waves/round-80/w1`; all 12 seats (`R80ExecA/B/C`, `R80ScoutA`,
  `R80ScribeA/B`, `R80ReviewerA/B`, `R80CriticA`, `R80MutationA`, `R80SentinelA`, `R80ConnectorA`)
  route output to `{LANE}/.ufo/waves/round-80/w1/<seat>/`. No seat's output folder is outside the lane.
- `grep -nEi "(write|create|commit|push|land)[^.]{0,60}(fleet|sibling|/home/vgpnk/Projects/shokunin/(scripts|\.ufo/state)|MANIFEST)"`
  over the five committed files returns exactly two sentences, and both are the opposite of a write
  target: `build_spec.py:14` forbids them (*"no edits to /home/vgpnk/Projects/shokunin/scripts,
  /home/vgpnk/Projects/shokunin/.ufo/state, MANIFEST.json or any sibling repo"*) and
  `build_spec.py:181` repeats the ban inside the sentinel brief.
- Every fleet-root path token in `build_spec.py`, `w1-spec.json`, `w1-dispatch.json` is one of: the
  lane root, a lane-relative evidence path, or a **read-only** instruction
  (`build_spec.py:196` *"Search the sibling lane repos under `/home/vgpnk/Projects/shokunin/` …"*,
  repeated in the connector seat's prompt), or the operator tooling line naming
  `/home/vgpnk/.omp/agent/RULES.md`.
- `w1-validate.err` is **0 bytes** — no validator output is retained, so "the spec validated" is
  asserted by the zero-byte file alone (observation, not a scope defect).

**ITEM 5: CLEAN** — no committed wave file names a fleet-repo or sibling-lane path as a write target;
fleet paths appear only as prohibitions and read-only scans, and every seat's output folder is inside
the lane.

---

## Appendix — findings adjacent to the assigned items (evidence-backed, for the critic/reviewer seats)

These attack the two frozen claims rather than the five checklist items; each names the exact
command, the receipt and the observed line.

### F1 — HIGH (C1 support): the fresh leg's ground truth is the same file as the subject under test

`corpus/evidence/round80/matrix-battery-v7.py:125` sets
`WITNESS = LANE / "corpus/evidence/round76/loader-matrix-v3.py"`; the frozen counting command
(`claims.md:37-39`) passes `--matrix corpus/evidence/round76/loader-matrix-v3.py`, and
`controls/v7-legit-matrix-r80.txt:3-4` prints that same path with
`MATRIX_SHA256=b79d6441057a01b27eb465c6b0625cd46502114f8b622b370c2cd2805c81913f` — identical to
`sha256sum corpus/evidence/round76/loader-matrix-v3.py`. `draw_fresh` (`:457`) takes **no matrix
argument**; the label comes from `_witness_out` (`:437-455`), which runs `WITNESS` on the base copy
and the mutated copy and sets `group = "POSITIVE" if (wb[0]==wc[0] and …) else "FORGER"` (`:486`),
after which `score` (`:498`) demands that the *same file* accept the POSITIVE and reject the FORGER.

Exploit path: a matrix that is wrong-but-self-consistent — e.g. one whose verdicts are inverted, or a
static table keyed on a constant the rewrite operators do not touch — is labelled POSITIVE for every
semantics-preserving rewrite and FORGER for every semantics-altering mutation *by its own output*, so
it reaches `fresh_positive=2/2 fresh_forgers=2/2` without any independent ground truth. A totally
constant verdict is still caught (a FORGER cannot be drawn in 40 attempts → exit 2), so the leg is
not empty: it tests "does your verdict react to semantics", not "are your judgements right".

Impact: two of the five fields of the frozen predicate are self-consistency assertions for the frozen
subject. The claim's support therefore rests on the 11 committed forgers, the 2 committed positives
and the 5 oracles — exactly the "independent anchor" `claims.md:54-55` names — and `claims.md:53-55`
records only the witness's fallibility ("a witness wrong about a case makes both legs wrong
together"), not its identity with the subject.

Smallest remediation: one clause in the next claims file — for `--matrix == WITNESS` the fresh leg is
a self-consistency check and its two counts are not evidence — or one guard in the instrument
(`if matrix.resolve() == WITNESS: emit("FRESH_LEG=self-witnessed")` around `:611`) and a second,
independent witness matrix. The frozen files are not amended: an append-only `## Mistakes` row plus a
correction line is the fix.

### F2 — HIGH (C1 anchor): one of the five "rejected oracles" never ran — the battery's own rewrite kills it

In `controls/v7-legit-matrix-r80.txt`: **17 of 17** `ORACLE:structure-identity RUN` lines read
`matrix_exit=1 marks=none content=bad` (lines 146-162; the subject verdicts follow to line 179), and line 180 aggregates
`ORACLE structure-identity REJECTED positive=0/2 forger=0/11 fresh_positive=0/2 fresh_forger=0/2`.
`marks=none` means the oracle printed no `LOADER_MATRIX=` line at all: it exited without a verdict and
`oracle_ok += not full` (`v7:636`) counts that as REJECTED.

Reproduced in `receipts/09-rename-defect-repro.txt` with `--work` under my scratch:

```
$ python3 -B .ufo/waves/round-79/w1/R79ExecC/matrix-structure-identity.py \
    --counter corpus/evidence/round74/correction-count.py --work $S/direct
LOADER_MATRIX=12/12 MATRIX=PASS
# exit=0

$ python3 -B <the same oracle re-emitted by v7.reemit(), as v7:632 does> \
    --counter corpus/evidence/round74/correction-count.py --work $S/ow2
# exit=1
# stdout lines=0
AttributeError: '_7ff523aa' object has no attribute 'canon'
```

The matrix under test survives the identical treatment (`LOADER_MATRIX=12/12 MATRIX=PASS`, `# exit=0`),
so the failure is specific to the oracle's class-body attribute pattern and to `_rename`
(`v7:231-282`): a class-body `canon = …` is an `ast.Name` store and is renamed, while `self.canon` /
`obj.canon` are `ast.Attribute.attr` and are not.

Impact: `oracles_rejected=5/5` counts one rejection produced by the battery packaging its own
adversary into a new source file, not by the drawn subject set defeating its method. The round-79
structure-identity matrix is the strongest known adversary — it reached `BATTERY=PASS` on v5 and v6 —
and under v7 it is destroyed before it can be measured. The frozen kill rule cannot tell "missed" from
"never ran", and the receipt's own `marks=none` is the only tell.

Smallest remediation: in `_rename`, add every identifier that appears as an `ast.Attribute.attr`
anywhere in the tree to `excluded` (one comprehension beside `excluded` at `:239`); and in `main`,
count an oracle with no parseable marks as `oracle_error` and never as `oracle_ok` (`v7:630-636`).

### F3 — MEDIUM (provenance): the C1 "after" receipt is a body-copy with no command and no exit code

`receipts/07-receipt-provenance.txt`:

```
$ diff <(tail -n +3 controls/v7-legit-matrix-prefreeze.txt) controls/v7-legit-matrix-after.txt
IDENTICAL_BODY (exit 0)
```

`v7-legit-matrix-after.txt`: 216 lines, `# command:` count **0**, `# exit:` count **0**,
`RECEIPT_LINES=216` at line 215 (line count consistent). The prefreeze receipt has one command header
and no exit trailer. Neither receipt carries the sha of the battery that produced it
(`grep -nE 'BATTERY_SHA256|INSTRUMENT_SHA|SELF_SHA' controls/*.txt` → only the two *v6* oracle
receipts, and those name the battery **under test**, not the battery that ran). So the C1 after
measurement is not bound to its instrument and not bound to its exit status — the first clause of the
frozen predicate ("The command exits 0") is unrecorded.

Partial repair has already landed at `44d09edf`: `controls/v7-legit-matrix-r80.txt` (219 lines) adds
`# command: … --rev b7803829…`, and `# exit: 0`. It still does not name the battery's own sha.

Smallest remediation: three lines in `matrix-battery-v7.py` — `emit("BATTERY_SELF_SHA256=" + hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())`
beside `MATRIX_SHA256` — and the exit trailer on every receipt.

### F4 — LOW/MEDIUM (leak): the battery hands every subject the lane root and the whole environment

`v7:194-195` / `v7:439-440`: `env = dict(os.environ, LOADER_MATRIX_CHILD_TIMEOUT=…, LOADER_MATRIX_LANE=str(LANE))`,
passed at `:200` / `:444`. `forgers/a10-payload-decode.py:34-35` consumes it:
`LANE = pathlib.Path(os.environ.get("LOADER_MATRIX_LANE") or pathlib.Path(__file__).resolve().parents[4])`.

Impact: each scored subject and each oracle receives a path to the entire lane — the claims file, the
battery's own source, the witness, the expected predicate line — plus every variable in the seat's
environment. A forger can therefore read the expected verdict at scoring time; no receipt records the
channel, and the C1 claim's "the drawn set" argument assumes the subject sees only its own bytes.

Smallest remediation: build a minimal env (`PATH`, `LOADER_MATRIX_CHILD_TIMEOUT`) instead of
`dict(os.environ, …)`, and pass a scratch root (not the lane) to `a10`.

### F5 — LOW (provenance): `LANE_REV` names `master`, and the instrument is absent at that revision

`v7:657` `git -C <LANE> rev-parse master` — the receipt's `LANE_REV` is the branch tip, not the bytes
measured (a dirty worktree prints the same token). Concretely for this round:
`git cat-file -e b7803829:corpus/evidence/round80/matrix-battery-v7.py` →
`fatal: path … exists on disk, but not in 'b7803829…'`, `# exit=128`; `git log --diff-filter=A` places
the file in `0f59b985`. So `LANE_REV=b7803829…` in all three v7 receipts names a revision at which the
instrument does not exist; the v7 receipts are reproducible only via the sha in `claims.md`.

Smallest remediation: emit `WORKTREE_REV=` from `git -C <lane> rev-parse HEAD` and
`WORKTREE_DIRTY=` from `git status --porcelain` beside `LANE_REV`, so a receipt states both the branch
it claims and the bytes it measured.

---

## Summary

| item | verdict |
|---|---|
| 1 leak/scope scan | **CLEAN** (no `/tmp`, no network, no mutating subprocess, no credential, no sibling write target, all writes under `--work`) |
| 2 revision binding | **FINDING** — 5/7 carry a 40-hex revision; `oracle-structure-v6-accepted.txt` and `oracle-before-r80.txt` carry none; `REV=worktree` 0/7 |
| 3 declared sha256 | **CLEAN** — 4/4 instruments and 2/2 predecessor pins reproduce byte-exactly at `44d09edf` |
| 4 instrument limits | **CLEAN** on the three questions; notes N4a/N4b/N4c recorded (F5/F4/F2) |
| 5 wave scope | **CLEAN** — no fleet/sibling write target; fleet paths only as prohibitions and read-only scans |

Appendix severities: F1 HIGH (C1's fresh counts are self-labelled for the frozen subject), F2 HIGH
(one of the five counted oracle rejections is a packaging crash, reproduced), F3 MEDIUM (the C1 after
receipt binds neither its command nor its exit; partly repaired at `44d09edf`), F4 LOW/MEDIUM
(lane root + full environment exported to untrusted subjects), F5 LOW (`LANE_REV` names `master`; the
instrument does not exist at the revision printed).

Scope statement: this seat wrote only `.ufo/waves/round-80/w1/R80SentinelA/` (this file, the seat
report one level up, and `receipts/`); its scratch
`/fast/scratch/hyaku/chousa-r80/R80SentinelA/` was removed before yield; nothing under
`corpus/evidence/round79/` or `corpus/evidence/round80/` was created, modified or deleted (drift
check in receipt `03-sha256.txt`: empty `git status --porcelain`, exit 0); no lane or fleet git/jj
mutation was issued (every git invocation above is `rev-parse`, `show`, `ls-tree`, `cat-file`,
`log` or `status`); no tool was installed or upgraded.
