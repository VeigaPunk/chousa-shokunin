# ReviewC2Rerun

Seat: leaf reviewer. No subagent. No production edit. No network. No tool install.
Axes: operability (counter runs on the canonical interpreter and path), calibration (frozen 15/15 and the S086 flip kill), depth (the counter recomputes R43-SPLIT rather than printing a constant).
Milestone: Round 43 absent-class split. Measured commit `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
Recommendation only. Not an admission.

## Identity

`git rev-parse HEAD` printed `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
`git log -1 --oneline 737f40b6aa8f37ffe2269db370fd6d65a720d9a8` printed `737f40b round-43: split the absent class and adopt one locally re-opened search-log entry`.
`git merge-base --is-ancestor 737f40b6aa8f37ffe2269db370fd6d65a720d9a8 HEAD` exited 0.
`git rev-parse HEAD:corpus/evidence/round43/c2-count.py` and the same path at `737f40b6aa8f37ffe2269db370fd6d65a720d9a8` both printed `77fd3a2e25de4d1eb5cd8b510fccdfbed932278d`.
Runtime: `Python 3.14.8` at `/usr/bin/python3`. The frozen command was that interpreter on the committed script. No `--table`, `--register`, or `--cache` override. `LANE` is `Path(__file__).resolve().parents[3]`, so the script's own tree is the lane; it was not pointed at the assimilation copy.

After both runs, `git status --porcelain -- corpus/evidence/round43/c2-count.py corpus/evidence/round43/absent-split.tsv corpus/evidence/round43/claims.md` printed no lines. The flip path in `corpus/evidence/round43/c2-count.py` (lines 115–119) rebuilds the in-memory row list. The file has no write of the table, register, or cache. There is no resume path and no continuity preflight in this counter, so the flip is the only continuity-like control; it caused zero mutation of those three paths.

## Unflipped command

Command: `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c2-count.py`

Stdout, verbatim:

```
SPLIT_AGREES=15/15
VOCAB_OK=15/15
MISMATCHES=0
C2=PASS
```

Exit code: 0.

## Flipped command

Command: `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c2-count.py --flip S086`

Stdout, verbatim:

```
SPLIT_AGREES=14/15
VOCAB_OK=15/15
MISMATCHES=1
MISMATCH S086 table=misquote independent=not-carried
C2=FAIL
```

Exit code: 1.

## Frozen predicate

`corpus/evidence/round43/claims.md` lines 60–62 require `C2=PASS`, `SPLIT_AGREES=15/15`, `VOCAB_OK=15/15`, exit 0, and `--flip S086` must print `SPLIT_AGREES=14/15` and exit 1. Both runs match. The bound in the counter is `BOUND = 1 / 2` (`c2-count.py` line 39). It was not retuned.

On-disk row used by the flip, `corpus/evidence/round43/absent-split.tsv` line 4: `S086	not-carried	4	46	0.086957	2`. The mismatch line `table=misquote` is the in-memory swap of that `not-carried` label, not a write. `independent=not-carried` is the counter's recompute, so the kill is a real disagreement, not a counter that still prints 15/15.

`sha256sum corpus/evidence/round43/absent-split.tsv` printed `bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58`. The file has 15 data rows and no header. The printed denominators were 15 both times, so saturation is the whole table, not a subset.

## Findings

No actionable defect in this seat's scope.

Checked, and not a miss of the frozen command:

- Operability: the canonical script ran to completion on `/usr/bin/python3` at the measured commit. Exit 0 unflipped, exit 1 on the named flip.
- Calibration: agreement is computed in the loop at `c2-count.py` lines 121–136 (`agreed` increments only when `label in vocab and expected.get(rid) == label`; pass requires `n == 15 and agreed == 15 and vocab_ok == 15`). The flip output is inconsistent with a constant `15/15` printer.
- Depth: `independent_labels` (`c2-count.py` lines 80–97) recomputes NFKC, whitespace collapse (`nfkc_ws`, lines 42–43), longest contiguous common run (`longest_run`, lines 46–59), and row-max ratio `>= 1/2`. It does not import `tools/absent-split.py`. Grep of `c2-count.py` for `urllib`, `requests`, `curl`, `wget`, `socket`, and `open(` found no matches.
- Same-identity: one chousa register row for S086 (`absent-defect-register.md` line 41). The `game-dev-2d` `S086` row (line 292) is a different lane and is excluded by `quarantine-check.py` `parse_register` (`LANE = "chousa"`, line 42; lane filter at line 179). No same-id overwrite on the graded row.
- Zero mutation: see Identity. No resume preflight exists to fail.

## Residual risk

- This seat did not recompute the 15 ratios with a second implementation. `SPLIT_AGREES=15/15` is the counter's recompute against the table. The ratio column on the S086 line was read, not re-derived here.
- Quote text and capture bytes come from `tools/quarantine-check.py` `parse_register` and `cache_doc`, the same loader `tools/absent-split.py` uses. The ratio functions are duplicated, not shared, so a loader bug would not be split by C2. `cache_doc` reads with `errors="replace"` (`quarantine-check.py` line 252).
- `--flip` of an id that is not in the table is a no-op (`c2-count.py` lines 115–119) and would still exit 0 if the other rows agree. The frozen control is S086, which is present. That hole was not executed.
- C2 does not require the 15 ids to be the round-42 absent set. `claims.md` lines 72–73 assign that enumeration to C1. This report does not certify the id set.
- Each command was run once. C2 does not claim byte-identical reruns. A second run was not performed.

## Verification gaps

- Capture bytes for the 15 URLs were not hashed here.
- Round-42 `quarantine-verdicts.tsv` was not diffed against the split-table ids here.
- No alternate longest-run implementation was executed.
- `git status` was limited to the three paths named above. Source review found no other write, but the rest of the worktree was not status-checked by this seat.

## Recommendation

Accept the frozen C2 observable on `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`: unflipped `SPLIT_AGREES=15/15`, `VOCAB_OK=15/15`, `C2=PASS`, exit 0; `--flip S086` prints `SPLIT_AGREES=14/15` and exits 1, with zero mutation of the split table. Do not retune the 1/2 bound from this seat.
