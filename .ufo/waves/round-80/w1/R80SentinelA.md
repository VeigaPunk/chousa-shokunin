# R80SentinelA — audit report (round 80, chousa)

Seat `R80SentinelA`, leaf sentinel. Read-only on everything outside
`.ufo/waves/round-80/w1/R80SentinelA/`; scratch `/fast/scratch/hyaku/chousa-r80/R80SentinelA/`
(created, used for two reproductions, removed before yield); no subagents, no network, no git/jj
mutation, no tool installed (none needed).

Base revision `b7803829922770b890e9f4efdd30d12c3695439a`; **measured at
`44d09edfc20dba26ee8d58a93d365989916a2692`** (HEAD moved from `0d253c95…` at 00:00:43 during the
audit, when the integration commit landed the re-run controls and S199–S202). Every scan was re-run
at `44d09edf`; worktree clean on every path scanned (`git status --porcelain` → empty, exit 0).

Full audit with every command and its output:
`.ufo/waves/round-80/w1/R80SentinelA/audit.md` (sha256
`b29aee02482db68252292e7df7f2ef2ac75a6290ddf34016ab324ff58d6f1900`, 316 lines) plus ten receipts in
`.ufo/waves/round-80/w1/R80SentinelA/receipts/` (each named and hashed inside `audit.md`).

## Assignments and verdicts

1. **Leak / scope scan** (`01-leak-scan.txt`) — **CLEAN.** No `/tmp` or `/var/tmp` path, no network
   call (the single `socket` hit is `census-start.txt:2`, a SOURCES duplicate-URL warning containing
   `socket.html`), no `git commit`/`git push`/`jj`, no credential-shaped string, no sibling-lane or
   fleet-repo write target. Every write in the instruments is under the caller's `--work`
   (`matrix-battery-v7.py:299-302`, `:588`, `:604`; `oracle-check.py:48`; `gate-grounding-check.py`
   has no write call; `forgers/a10-payload-decode.py` has no write, no `open`, no `subprocess`).
2. **Revision binding of control receipts** (`02-rev-binding.txt`) — **FINDING.** 7 receipts exist at
   `44d09edf`; **5** carry a 40-hex `LANE_REV=` line, **2 do not and carry no 40-hex token at all**:
   `corpus/evidence/round80/controls/oracle-structure-v6-accepted.txt` and
   `corpus/evidence/round80/controls/oracle-before-r80.txt`. `REV=worktree` occurs **0** times in the
   whole evidence directory. `oracle-structure-v6-accepted.txt` is the receipt `claims.md:29-31` cites
   as C1's do-nothing control, so the round's own before-control for its lowest axis is one of the two
   unbound files. This is round-79 routed defect 6 recurring in the round that was to adopt it.
3. **Declared sha256 vs committed bytes** (`03-sha256.txt`) — **CLEAN.** 4/4 instruments match
   `claims.md:13-16` exactly at both the worktree and `git show HEAD:` bytes
   (`35351b23…914d`, `580233ad…0289`, `d9e42621…c553`, `3cb234be…9f64`), and the two predecessor pins
   reproduce too (`bb91406e…61e1d` for `round79/matrix-battery-v6.py`, `b79d6441…913f` for
   `round76/loader-matrix-v3.py`).
4. **Declared instrument limits of `matrix-battery-v7.py`** (`04-v7-limits.txt`) — **CLEAN** on all
   three questions: no absolute path literal (`grep` exits 1 for both patterns), no
   `mkdtemp`/`tempfile`/`TMPDIR` use at all (`--work` is `required=True`, validated, and every emitted
   copy is `work / token_hex(8)`), and every ground-truth input (`POSITIVES`, `FORGERS`, `ORACLES`,
   `WITNESS`) is `LANE / …`; only `--matrix` is caller-supplied. Three notes recorded: `_lane_rev()`
   names `git rev-parse master`, not the bytes measured (F5); the full environment and the lane root
   are exported to untrusted subjects (F4); `_rename` does not rename `ast.Attribute.attr` (F2).
5. **Wave scope** (`05-wave-scope.txt`) — **CLEAN.** The five committed files under
   `.ufo/waves/round-80/` name fleet or sibling paths only as a prohibition (`build_spec.py:14`) or a
   read-only search instruction (`build_spec.py:196`, and the connector seat's prompt). `reportDir` is
   `.ufo/waves/round-80/w1` and all 12 seats route into `{LANE}/.ufo/waves/round-80/w1/<seat>/`. Note:
   `w1-validate.err` is 0 bytes, so the validator's own result is not retained.

## Findings beyond the checklist (each with command, receipt, observed line)

- **F1 HIGH — the fresh leg's ground truth is the subject under test.** `matrix-battery-v7.py:125`
  sets `WITNESS = LANE/corpus/evidence/round76/loader-matrix-v3.py`; the frozen counting command passes
  that same path as `--matrix`, and `controls/v7-legit-matrix-r80.txt:3-4` prints it with
  `MATRIX_SHA256=b79d6441…913f`, equal to `sha256sum corpus/evidence/round76/loader-matrix-v3.py`.
  `draw_fresh` (`:457`) takes no matrix argument and labels the copy at `:486` from the witness's own
  rc/marks/cells, after which `score` (`:498`) requires the *same file* to accept POSITIVE and reject
  FORGER. So `fresh_positive=2/2 fresh_forgers=2/2` are self-consistency assertions for the frozen
  subject (a wrong-but-self-consistent matrix satisfies them); a constant verdict is still caught
  (cannot draw a FORGER → exit 2), so the leg tests reactivity, not correctness. `claims.md:53-55`
  records the witness's fallibility, not its identity with the subject. Receipt
  `06-fresh-leg-ground-truth.txt`. Remediation: refuse/annotate `--matrix == WITNESS` (one guard at
  `:611`) plus a second-independent witness, or one clause in the next claims file; append-only.
- **F2 HIGH — one of the five counted oracle rejections never produced a verdict.** In
  `controls/v7-legit-matrix-r80.txt`, **17 of 17** `ORACLE:structure-identity RUN` lines read
  `matrix_exit=1 marks=none content=bad` (lines 146-162) and line 180 counts it `REJECTED`; `v7:636`
  (`oracle_ok += not full`) cannot tell "missed" from "never ran". Reproduced in
  `09-rename-defect-repro.txt`: the oracle alone prints `LOADER_MATRIX=12/12 MATRIX=PASS`, `# exit=0`;
  the same oracle re-emitted exactly as `v7:632` does exits **1** with **0 stdout lines** and
  `AttributeError: '_7ff523aa' object has no attribute 'canon'`. Cause: `_rename` (`:231-282`) renames
  class-body `Name` stores but never `ast.Attribute.attr`, so `canon = …` becomes `_xxxx` while
  `self.canon` keeps `canon`. The matrix under test survives the same treatment (12/12 PASS, exit 0),
  so the failure is specific to the oracle's attribute pattern. Impact: `oracles_rejected=5/5` counts
  a packaging crash as an anchor rejection, and the round-79 structure-identity matrix — the strongest
  known adversary, `BATTERY=PASS` on v5 and v6 — is destroyed before it can be measured. Remediation:
  exclude every identifier seen as an `ast.Attribute.attr` from the rename map (one comprehension in
  `_rename`), and count a no-marks run as `oracle_error`, never `oracle_ok`.
- **F3 MEDIUM — the C1 after receipt binds neither its command nor its exit.** `07-receipt-provenance.txt`:
  `diff <(tail -n +3 controls/v7-legit-matrix-prefreeze.txt) controls/v7-legit-matrix-after.txt` →
  `IDENTICAL_BODY`, exit 0; the after file is 216 lines with 0 `# command:` and 0 `# exit:` trailers,
  and neither v7 receipt carries the sha of the battery that produced it (`grep` for
  `BATTERY_SHA256|INSTRUMENT_SHA|SELF_SHA` matches only the two v6 receipts, which name the battery
  *under test*). Partly repaired at `44d09edf` by `v7-legit-matrix-r80.txt` (command + `LANE_REV` +
  `# exit: 0`), which still omits the instrument's own sha. Remediation: emit
  `BATTERY_SELF_SHA256` beside `MATRIX_SHA256`, and always land the exit trailer.
- **F4 LOW/MEDIUM — full environment and lane root handed to untrusted subjects.** `v7:194-195` and
  `:439-440` build `dict(os.environ, LOADER_MATRIX_CHILD_TIMEOUT=…, LOADER_MATRIX_LANE=str(LANE))` and
  pass it to every subject (`:200`) and to the witness (`:444`); `forgers/a10-payload-decode.py:34-35`
  consumes `LOADER_MATRIX_LANE`. A subject can read the battery, the claims and the expected predicate
  at scoring time, and inherits every secret in the seat environment. Not `/tmp` and not network, but
  a leak the "the subject sees only its own bytes" argument does not cover. Remediation: minimal env
  plus a scratch root instead of the lane.
- **F5 LOW — `LANE_REV` names `master`, and the instrument is absent at that revision.**
  `git cat-file -e b7803829:corpus/evidence/round80/matrix-battery-v7.py` →
  `fatal: path … exists on disk, but not in 'b7803829…'`, `# exit=128`; the file was first added in
  `0f59b985`. So all three v7 receipts print a revision at which the instrument they measured does not
  exist, and `_lane_rev()` (`:657`) would print the same token from a dirty worktree. Remediation: also
  emit `WORKTREE_REV` (`git rev-parse HEAD`) and `WORKTREE_DIRTY` (`git status --porcelain`).

## Scope statement

Wrote only `.ufo/waves/round-80/w1/R80SentinelA/` (this report, `audit.md`, `receipts/`) and the
scratch directory, which was deleted before yield. Nothing under `corpus/evidence/round79/` or
`corpus/evidence/round80/` was created, modified or deleted; every git invocation was
`rev-parse`/`show`/`ls-tree`/`cat-file`/`log`/`status`; no fleet or sibling repo was touched.
