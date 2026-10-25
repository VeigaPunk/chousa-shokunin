# CritC1Admission — C1 admission attack (round 45, wave 2)

Seat: L1Chousa45.CritC1Admission (critic, leaf). Axes: operability, calibration, depth.
Item: judge the landed `tools/parent-lifetime.sh` + `corpus/evidence/round45/parent-lifetime.diff`
at `5e8c7ad2f7b8254d83358820286e3d12ca4672d1` for C1 admission (improved with no harm).
Measured over committed bytes: `git archive 5e8c7ad2… | tar -x -C /tmp/chousa-r45-CritC1Admission/tree`.
No tools installed; no fetch; no lane writes except this report.

## (1) Selftest mode records timeout_s=0 — honest or misleading?

Recorded (committed `tools/parent-lifetime.sh:37-41`):
```
if [[ "$SELFTEST" -eq 1 ]]; then
  TIMEOUT=${TIMEOUT:-0}
else
  [[ "$TIMEOUT" =~ ^[1-9][0-9]*$ ]] || usage
fi
```
Verbatim run:
```
$ bash tools/parent-lifetime.sh --selftest --receipt /tmp/chousa-r45-CritC1Admission/selftest.receipt; echo "selftest_exit=$?"
selftest_exit=0
$ head -1 /tmp/chousa-r45-CritC1Admission/selftest.receipt
start parent_pid=2808863 epoch=1792921788 timeout_s=0
```
Assessment: `0` is not expressible in dispatch mode (regex rejects it), so it is a
fabricated sentinel outside the field's own domain. The selftest branch spawns
`sleep 0.2 &` with **no** timeout wrapper (`tools/parent-lifetime.sh:52-59`), so
`timeout_s=0` describes no enforced timeout. Nothing consumes selftest receipts: the
round-45 counter checks `timeout_s` only on cases (a)-(c) (`c1-count.py:93-111`), and
the header claims only that dispatch mode records the per-wave timeout. **Verdict:
holds-narrowed** — a calibration wrinkle (undocumented sentinel, domain-inconsistent),
not a predicate failure; honest only if read as "no timeout", which no committed doc states.

## (2) Removing `set +e`/`set -e` toggles around `wait`

Old tool (round-44 blob via `git show d82cec9:tools/parent-lifetime.sh`) had:
```
set +e
wait "$child"
ec=$?
set -e
```
and `set -u` only at top (no script-level `set -e`). Landed tool runs the same loop
with no toggles (`tools/parent-lifetime.sh:99-110`); the script now never enables
errexit anywhere.

Two distinct behavior deltas:

(a) Internal: in the old script `set -e` was re-enabled after each wait, so post-loop
commands ran under errexit; a later failure would have aborted before `exit 0`/`exit 3`.
The new script has no errexit at all, so later commands cannot be killed. This is a
behavior difference only if a post-wait command fails; it is, if anything, more robust.

(b) Errexit-inheritance: with `SHELLOPTS` containing `errexit` in the environment, a
child bash starts with errexit enabled; the bare `wait "$child"` then aborts the script
on the first 124/137 reap. Verbatim repro (stub `kimi` with `STUB_MODE=hang`, two
seats, `--timeout 1`):
```
=== control (normal env) ===
parent-lifetime: incomplete wave n_spawned=2 n_timeout=2
control_exit=3
$ cat ctl2.receipt
start parent_pid=2856395 epoch=1792921798 timeout_s=1
spawn name=SeatA child_pid=2856560 epoch=1792921798
spawn name=SeatB child_pid=2856570 epoch=1792921798
reap name=SeatA child_pid=2856560 exit_code=124 epoch=1792921799
reap name=SeatB child_pid=2856570 exit_code=124 epoch=1792921799
end parent_pid=2856395 epoch=1792921799 n_spawned=2 n_reaped=2
=== errexit-inherited (SHELLOPTS=braceexpand:hashall:errexit) ===
errxit_exit=124
$ cat errxit2.receipt
start parent_pid=2862902 epoch=1792921799 timeout_s=1
spawn name=SeatA child_pid=2862993 epoch=1792921799
spawn name=SeatB child_pid=2863000 epoch=1792921799
```
Under errexit the receipt is truncated (no reap lines, no `end` line) and the launcher
exits 124 instead of 3 — the exit contract silently breaks. The old toggles protected
exactly this case. In this environment `env | grep SHELLOPTS` is empty even from a
`set -e` parent, so ordinary callers (including `c1-count.py`'s `subprocess.run`, which
passes `os.environ` unchanged) never hit it; no committed caller invokes dispatch mode
at all (wave-1 `CritC1Harm` verified: only selftest prompts). **Verdict: holds-narrowed**
— a real robustness regression against errexit-env callers, outside the committed lane
contract; the counter still passes 5/5 (verified below). Smallest safe correction:
capture `wait` status in a conditional (`if wait "$child"; then ec=0; else ec=$?; fi`),
or restore the `set +e`/`set -e` toggles verbatim.

## (3) Stale committed docs ("Exit 0 when the end line is written" / default 420)

Grepped the tip for the phrase and for `420`/`TIMEOUT=420`/`timeout_s`/`--timeout`
across `SKILL.md`, `corpus/QUALITY.md`, `corpus/lessons/`, `corpus/knowledge/`,
`corpus/README.md`, `README.md`. No current guidance doc retains the old contract:
- `SKILL.md:110` Gates row states the new exit contract (0/3/1/2) and required
  `--timeout SECS` in dispatch mode; selftest row is `--selftest --receipt PATH` only.
- `corpus/QUALITY.md:613-616` (round-45 note on criterion 63): the exit-3 + required
  `--timeout` change is recorded, and "Criterion 63's demonstration is the round-44
  tool's behaviour and stays as history."
- `corpus/lessons/round-44.md:58-68` quotes the old header only as a past-tense
  mistake narrative ("Not fixed in this round: the frozen C1 predicate…").
- Remaining `420` hits in committed docs are unrelated (`.ufo/waves` logs; a
  `considerthese` note about SKILL.md being "~420 lines").
`corpus/evidence/round45/parent-lifetime.diff` contains the old wording only on removed
lines (its documented purpose). **Verdict: holds.**

## (4) Round-44 receipts still verify

Run inside the archive tree (round-44 counter; then round-45 counter):
```
$ python3 corpus/evidence/round44/c1-count.py; echo "r44_exit=$?"
N_SPAWNED=64/64
N_REAPED=64/64
PARENT_PID_MATCH=1/1
ZERO_PIDS=0
NAMES_MATCH=64/64
C1=PASS
r44_exit=0
$ python3 corpus/evidence/round45/c1-count.py; echo "r45_exit=$?"
CASE a_empty_exits_3=ok
CASE b_ok_exits_0=ok
CASE c_timeout_exits_3=ok
CASE d_no_timeout_exits_2=ok
CASE e_start_timeout_s=ok
CASES_MATCH=5/5
C1=PASS
r45_exit=0
```
**Verdict: holds.** The round-44 counter reads the receipt file only, not the tool
(`c1-count.py:22-24`), so the tool change cannot affect it; reconstructed `timeout_s`
extension is inert to its whitespace tokenizer.

## Verdict

C1 admission: **holds** (improved with no harm to any committed contract). Four attack
points: (1) selftest `timeout_s=0` — minor wrinkle, no predicate impact; (2) toggle
removal — internal behavior unchanged/robust, but errexit-inherited callers now get a
truncated receipt and exit 124 instead of 3 (fixable, outside committed lane use);
(3) no stale committed docs — the round-45 update fixed wave-1's stale-doc finding;
(4) round-44 receipts still verify. No predicate, counter, or target change proposed.

Commands run (verbatim decisive output above): archive extraction; selftest run + `head -1`;
`git show d82cec9:tools/parent-lifetime.sh`; errexit repro (control vs `SHELLOPTS=…errexit`);
targeted greps; both counters in the archive tree. Scratch `/tmp/chousa-r45-CritC1Admission/`
deleted. Nothing installed.
