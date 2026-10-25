# RevRowLauncher — wave 2 falsify report: SKILL.md Gates row `parent-lifetime` (r44; exit contract r45)

Target: Gates row at SKILL.md:110 of commit `5e8c7ad2f7b8254d83358820286e3d12ca4672d1` (archive tree `/tmp/chousa-r45-RevRowLauncher/tree`). Row has exactly **8 cells** (awk `FS='|'` → 10 fields = leading/trailing empties + 8 data cells; header line 77 declares exactly the 8 columns name|kind|entry|verdict map|self-test|pinned values|write scope|owner).

## Cell-by-cell verdict

### 1. name — HOLDS
Row text: `` `parent-lifetime` (r44; exit contract r45) ``. Observed verbatim at line 110.

### 2. kind — HOLDS
Row text: `tool`. Observed.

### 3. entry — HOLDS
Row text: `` `bash tools/parent-lifetime.sh --dispatch JSON --receipt PATH --agent FILE --timeout SECS` · `bash tools/parent-lifetime.sh --selftest --receipt PATH` ``. Both commands run from the archive tree and perform as documented (see 4, 5).
- `tools/parent-lifetime.sh` exists at the commit (4057 B, executable), and `grep -n 'parent-lifetime'` shows exactly the one row.

### 4. verdict map — HOLDS (all four exit codes observed or traced)
Row text: `exit 0 end line written, n_spawned>0, every child reaped, no seat exited 124/137 · exit 3 end line written but zero tasks spawned or a seat timed out (receipt complete, wave not) · exit 1 a child pid not captured or the parent pid changed · exit 2 usage, including a dispatch run without --timeout; the start line carries timeout_s=`

Observations (cwd = archive tree; stub `kimi` on PATH; receipts in scratch):
- **exit 0**: selftest → `rc=0`; receipt has `start parent_pid=2711842 epoch=1792921772 timeout_s=0`, two spawn lines, two reap lines `exit_code=0`, `end parent_pid=2711842 … n_spawned=2 n_reaped=2`. Two-seat dispatch with stub exiting 0 → `rc=0`, `end … n_spawned=2 n_reaped=2`.
- **exit 3**: empty dispatch (`--timeout 5`) → `rc=3`, stderr `parent-lifetime: incomplete wave n_spawned=0 n_timeout=0`; receipt end line `n_spawned=0 n_reaped=0` (complete receipt). Two-seat hang (`--timeout 1`) → `rc=3`, both reap lines `exit_code=124`, end line written `n_spawned=2 n_reaped=2`.
- **exit 1**: code path exists — child-pid-null check at `tools/parent-lifetime.sh:86-89` (`[[ -z "$child" || "$child" -le 0 ]]` → `exit 1`) and parent-pid-change check at `:113-116` (`$$ != parent_pid` → `exit 1`). Both branches unreachable in normal runs (bash always sets `$!`; `$$` cannot change mid-process) but implement the stated contract.
- **exit 2**: dispatch without `--timeout` → `rc=2` (usage on stderr); also unknown flag, missing `--receipt`, nonexistent `--dispatch` file → all `rc=2`.
- **start line carries timeout_s=**: present in every receipt — selftest `timeout_s=0`, case A/B `timeout_s=5`, case C `timeout_s=1` (line 47: `printf 'start parent_pid=%s epoch=%s timeout_s=%s\n'`).

### 5. self-test — HOLDS
Row text: `` `python3 corpus/evidence/round45/c1-count.py` → `CASES_MATCH=5/5` (stub `kimi` on PATH); the round-44 tool scores `CASES_MATCH=1/5`, exit 1 (`corpus/evidence/round45/controls/c1-control-r44-tool.txt`) ``.

Observations:
- `python3 corpus/evidence/round45/c1-count.py` in archive tree → verbatim output: `CASE a_empty_exits_3=ok` … `CASE e_start_timeout_s=ok`, `CASES_MATCH=5/5`, `C1=PASS`, `rc=0`. It creates its own stub `kimi` in a temp `bin` prepended to PATH (script lines 34-40, 88-91).
- Control file `corpus/evidence/round45/controls/c1-control-r44-tool.txt` exists (165 B) and its content matches the claim exactly: `CASE a_empty_exits_3=FAIL`, `CASE b_ok_exits_0=ok`, `CASE c_timeout_exits_3=FAIL`, `CASE d_no_timeout_exits_2=FAIL`, `CASE e_start_timeout_s=FAIL`, `CASES_MATCH=1/5`, `C1=FAIL`, `exit=1`. (The round-44 launcher blob itself is not committed; the control file is the frozen record of its score.)

### 6. pinned values — HOLDS
Row text: `contract corpus/evidence/round45/claims.md R45-C1; round-44 receipts corpus/evidence/round44/parent-lifetime.receipt still verify under corpus/evidence/round44/c1-count.py`

Observations:
- `corpus/evidence/round45/claims.md` exists (6258 B) and contains predicate R45-C1 verbatim (lines 23-29), counting command, target `CASES_MATCH=5/5`, `C1=PASS`, exit 0, and the do-nothing control note.
- `corpus/evidence/round44/parent-lifetime.receipt` exists (8637 B, 64 seats, start line has no `timeout_s=`).
- `python3 corpus/evidence/round44/c1-count.py` in archive tree → `N_SPAWNED=64/64`, `N_REAPED=64/64`, `PARENT_PID_MATCH=1/1`, `ZERO_PIDS=0`, `NAMES_MATCH=64/64`, `C1=PASS`, `rc=0`. Verifies under the pinned counter.

### 7. write scope — HOLDS
Row text: `writes the receipt and seat-logs/ beside it; spawns kimi per task; no network of its own`. Observed: receipt written at `--receipt` path, `seat-logs/` created beside it (line 71: `logdir=$(dirname -- "$RECEIPT")/seat-logs`), one `kimi` background child per task (lines 82-84), no network calls in the script (no curl/wget; only `date`, `mkdir`, `timeout`, `kimi`, `python3` local JSON parsing).

### 8. owner — HOLDS
Row text: `chousa`. Observed.

## Verdict: ROW HOLDS in all 8 cells; no defect found.

## Residual risk / gaps
- Exit-1 branches (child-pid null, parent-pid change) verified by code reading only — not triggerable in practice; they match the stated contract.
- Round-44 tool self-test score (1/5) verified via the committed control file, not by re-running the r44 launcher blob (not committed; blob `79ee8f29…` unavailable in the freeze tree).
- No tool installs were needed (no tooling changes recorded). Scratch `/tmp/chousa-r45-RevRowLauncher/` was used and will be removed.

Measurement note: all counters and commands were run inside the extracted archive tree (git archive of `5e8c7ad2f7b8254d83358820286e3d12ca4672d1`), never in the live repo.
