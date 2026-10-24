# RevC2FreshSeed — residual falsify seat: C2 / P2 on a fresh seed

Seat: `chousa-r37.RevC2FreshSeed`. Lane: chousa. Round 37, residual falsify call.
Lane repo: `/home/vgpnk/Projects/shokunin/chousa-shokunin`, tip
`b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65` (verified below).
Landed gate `tools/research-gate.sh` sha256:
`9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39`.
Base control gate `.ufo/waves/round-37/controls/base-gate-r37.sh` sha256:
`a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`.
Frozen design read: `corpus/evidence/round37/claims.md` (C2 + P2 + kill rule + Limits).
No fleet file was modified. The only file written is this report; all experiments are
under `/tmp`. No installs or upgrades were made (nothing was needed).

## Verdict

**P2, as frozen, HOLDS on fresh seed 38101: `PIN_CAPTURE_ENV_MATCH=7/7`,
`predicate_holds=true`, exit 0, receipt bound to the landed gate sha256. A second fresh
seed (38203) produced a byte-identical scenario array. The base control reproduces the
frozen 3/7 on the same fresh seed.**

**C2's claim text, however, is FALSIFIED on the landed gate.** A `BASH_ENV` startup file
that *exports a shell function* (`export -f date`) survives the capture's
`env -u … -u BASH_ENV` scrub, because bash delivers exported functions through
`BASH_FUNC_date%%` environment entries that `env -u` does not remove. The capture child
runs the function, writes a `GATE_GREP: …` line into `capture.txt`, the pinned baseline
embeds it, and a later **plain clean `--drift` on the unchanged gate reports exactly
`GATE_DRIFT: -GATE_GREP`, exit 1** — the same phantom-drift signature C2 says cannot
happen (and the base gate's failing `env-echo-pin` cell). A second variant
(`export -f date` emitting `POISON_R37`) yields `GATE_DRIFT: -LINE`, exit 1. The gate
file is unchanged (baseline header still binds `gate_sha256=9fcac047…`).

**The counter cannot detect either failure.** Its only pass/fail inputs are the pin exit
code, baseline existence, a count of baseline lines beginning `GATE_GREP: `, the drift
exit code, and the gate's own `GATE_DRIFT:` string. It never re-hashes or re-diffs the
baseline against an independent capture. Demonstrated: a fabricated gate with *no pin
capture and no drift comparison* (constant baseline containing a poison line, unconditional
`GATE_DRIFT: none`) scores **7/7**; a copy of the landed gate with the single comparison
`if [[ $body == "$GATE_CAP" ]]` replaced by `if true` scores **7/7** and calls a
hand-poisoned baseline `GATE_DRIFT: none` where the real gate reports `-LINE` (exit 1).
Also demonstrated: with an exported `date` function present in the *harness* environment,
the counter prints **7/7** while every pinned baseline embeds `POISON_R37…` (drift `none`
because both sides of the comparison are poisoned).

**Recommendation (not an admission):** do not close C2 as stated. Either (a) harden the
capture to a clean environment (strip inherited `BASH_FUNC_*` / use `env -i` with an
explicit allowlist), add an exported-function scenario to the counter, and correct the
`env-fn-echo-pin` fixture; or (b) freeze an erratum that narrows the claim to the two
re-export/`CHOUSA_ROOT` mechanisms and **names exported-function inheritance through
`BASH_FUNC_*` as residual debt**. P2 as frozen is insensitive to this class and should not
be cited as evidence that the claim's universal sentence holds.

## 1. P2 fresh-seed run (seed 38101, not in {37021, 37211, 37311, 37721, 37941, 37961})

Command (verbatim, appendix C3):

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && C2_TMP=$(mktemp -d) python3 corpus/evidence/round37/c2-count.py --gate tools/research-gate.sh --seed 38101 --receipt /tmp/revc2-c2-s38101.json; echo "EXIT=$?"
```

Result: all seven scenarios PASS; `PIN_CAPTURE_ENV_MATCH=7/7`; `EXIT=0`.

```
PASS hold-plain       env=none           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS hold-benign      env=benign         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-pin     env=echo           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-drift   env=echo-on-drift  expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-fn-echo-pin  env=fn             expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-root-pin     env=root           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-strict-pin   env=strict         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PIN_CAPTURE_ENV_MATCH=7/7
EXIT=0
```

## 2. Receipt audit (`/tmp/revc2-c2-s38101.json`, sha256 `3f08e1bb…d5819d`)

- `seed=38101`, `gate=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`,
  `gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39`
  (equals the landed gate hash printed at the top of this report).
- `matched=7`, `total=7`, `predicate_holds=true`, `predicate="PIN_CAPTURE_ENV_MATCH=7/7"`.
- Per-scenario observations: `pin_rc=0`, `pin_file=true`, `baseline_echo_lines=0`,
  `drift_rc=0`, `drift_line="GATE_DRIFT: none"` for all seven. `pin_out_tail` for
  `env-echo-pin` and `env-fn-echo-pin` is the *gate process's own* stderr echo
  (`GATE_GREP: path=/usr/bin/grep …`), not a baseline line (named limit: the gate process
  has already sourced `BASH_ENV` before its body runs); the baseline still has 0 such lines.
- `gate_sha256` is computed **after** all scenarios have run (`c2-count.py:172-174`), i.e.
  it binds the file as it stands at receipt-write time, not a per-invocation snapshot. No
  run mutates the gate, so this run is sound, but the binding is post-hoc (finding L3).
- Existing committed/untracked receipts (appendix C8): four `c2-after-*` runs
  (s37021, s37721, s37941, s37961) all `matched=7`, `gate_sha256=9fcac047…`; one
  `c2-base-s37021` at 3/7 bound to `a7d3922c…`. No committed run against the landed gate
  prints a lower count. Note `c2-after-s37021.json` reuses the construction seed 37021; it
  is not a fresh-seed run.

## 3. Trust analysis from the counter's code

The counter does **not** independently verify the pinned file's content. Its complete
pass/fail surface (`c2-count.py:122-130`) is:

```
122     echo_lines = -1
123     if os.path.isfile(bp):
124         with open(bp, "r", encoding="utf-8", errors="replace") as fh:
125             echo_lines = sum(1 for line in fh if line.startswith("GATE_GREP: "))
126
127     observed = dict(pin_rc=pin_rc, pin_file=os.path.isfile(bp),
128                     baseline_echo_lines=echo_lines, drift_rc=drift_rc,
129                     drift_line=drift_line(drift_out))
130     ok = all(observed[k] == expected[k] for k in expected)
```

and `drift_line` (`c2-count.py:87-90`) is:

```
87 def drift_line(out):
88     for line in out.splitlines():
89         if line.startswith("GATE_DRIFT:"):
90             return line.strip()
91     return "none"
```

Consequences, each demonstrated in §4:

1. **Drift is trusted, not re-derived.** The counter never computes a diff, never
   re-hashes the baseline, never compares the baseline to a fresh independent capture.
   If the gate prints `GATE_DRIFT: none` and exits 0, the counter believes it. A gate with
   a broken/absent comparator passes (mutants A and B: 7/7).
2. **Content is checked only by one prefix count.** `baseline_echo_lines` counts lines
   beginning exactly `GATE_GREP: `; any other injected line (e.g. `POISON_R37: …`) is
   invisible. A baseline containing arbitrary poisoned content with zero
   `GATE_GREP: `-prefixed lines passes (mutant A; harness-export run).
3. **First `GATE_DRIFT:` line wins.** A gate that prints `GATE_DRIFT: none` before/after
   a genuine drift line is scored on the first match.
4. **`pin_out` is recorded but not scored.** `pin_out_tail` never enters `observed`; a gate
   exiting 0 while printing a failure/short capture line passes if it writes any baseline
   without `GATE_GREP: ` lines.
5. **The fixture named "exported shell function" is not exported.** `FN_ENV`
   (`c2-count.py:41`) is `export CHOUSA_GREP_PIN_ECHO=1\ngrep() { command grep "$@"; }\n` —
   no `export -f`. `grep -n "export -f" c2-count.py` returns nothing (appendix C24). On the
   base gate, `env-fn-echo-pin` and `env-echo-pin` produce identical observations
   (`echo=1`, `GATE_DRIFT: -GATE_GREP`, exit 1), so the cell is a duplicate of
   `env-echo-pin`, not a function-inheritance test. claims.md's phrase "repeats the pin case
   through an exported shell function" is inaccurate.
6. **`--seed` is decorative.** It is stored in the receipt (`c2-count.py:173`) and nowhere
   else; no fixture, order, or PRNG is derived from it (grep for seed/random/shuffle finds
   only the argparse and receipt lines; appendix C9 shows the two fresh seeds produce a
   byte-identical `scenarios` array). The "two fresh seeds" clause adds no coverage; the
   only per-run variation is the temp path (and the `foreign-root` path inside the root
   fixture).

The gate-side behavior the counter is trusting: `gate_canonical_capture`
(`research-gate.sh:3922-3950`) runs the child as
`env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_STRICT -u CHOUSA_ROOT
-u CHOUSA_AGGREGATOR_ERE -u CHOUSA_GREP_PIN_ECHO -u BASH_ENV bash "$SELF" verify-all …`
(lines 3934-3938), and `run_drift` prints `GATE_DRIFT: none`/exit 0 when the normalized
body equals the fresh capture (lines 4145-4152). `env -u` removes named variables only; it
does not remove `BASH_FUNC_*` exported functions, so an exported function defined by
`BASH_ENV` reaches the child (demonstrated in §4.4-4.5).

## 4. Scratch experiments (all under /tmp; lane and fleet untouched)

### 4.1 Mutant A — fabricated gate, no capture, no comparison → 7/7

`/tmp/revc2-mutant-a.sh` (`--pin` writes a constant baseline that includes the line
`POISON_R37: baseline content chosen by the gate, not by any environment`, then prints
`GATE_PIN: ok … gate_sha256=deadbeef`; `--drift` prints `GATE_DRIFT: none`, exit 0).

Counter result: **`PIN_CAPTURE_ENV_MATCH=7/7`, exit 0** (appendix C12), receipt
`gate_sha256=8b85ec9e…` ≠ landed. The counter cannot distinguish the landed gate's real
canonical capture from a fabricated constant file, because it checks only existence and
the `GATE_GREP: ` prefix count.

### 4.2 Mutant B — landed gate with the drift comparison deleted → 7/7

Copy of the landed gate; the single line `if [[ $body == "$GATE_CAP" ]]; then`
(line 4146) replaced by `if true; then  # RevC2 mutation: comparison removed; always
reports none`. Everything else (pin capture, scrub, header, normalization) is unchanged.

- Counter result: **`PIN_CAPTURE_ENV_MATCH=7/7`, exit 0** (C13), receipt
  `gate_sha256=24e5fdcc…`.
- Blindness demo (C14): pin a baseline with the mutant, append
  `POISON_R37: appended after a clean pin` inside the canonical block, then:
  - mutant `--drift`: rc 0, `GATE_DRIFT: none`;
  - landed gate `--drift` on the same file: **rc 1, `GATE_DRIFT: -LINE`**.
  The counter would score the mutant's answer as a pass.

### 4.3 Exported function in the harness environment → 7/7 with poisoned baselines

Run the counter from a bash that defines and exports `date`
(`date() { /usr/bin/date "$@"; builtin printf "POISON_R37: harness-inherited exported
function\n" >&2; }; export -f date`). The counter's `SCRUB` tuple does not include
`BASH_FUNC_*`, so every gate invocation (pin and drift) inherits the function.

- Counter: **7/7, COUNTER_EXIT=0** (C25).
- Manual reproduction (C26): `--pin` rc 0, baseline has **1 `POISON_R37` line**,
  0 `GATE_GREP:` lines, 3037 bytes; `--drift` rc 0 with `GATE_DRIFT: none` — because both
  the pinned and the fresh capture are poisoned identically, the gate's honest comparison
  sees no difference. The counter's only content check (GATE_GREP prefix count) returns 0.
  This is exactly the assignment's hypothetical: *"a gate that prints 'GATE_DRIFT: none'
  while the baseline is poisoned would pass"* — here the gate is the landed, honest gate;
  the poison arrives through inherited exported functions.

### 4.4 Claim-level counterexample: `BASH_ENV`-delivered exported function on the landed gate

Env file `/tmp/revc2-grepinject.*/inject.env`:

```
date() { /usr/bin/date "$@"; builtin printf "GATE_GREP: path=/tmp/evil source=override version=\"forged\"\n" >&2; }
export -f date
```

Run `BASH_ENV=inject.env bash tools/research-gate.sh --pin …` against the **landed gate**
(baseline header line 3 binds `gate_sha256=9fcac047…`):

- pin rc 0; baseline `GATE_GREP:` line count = **1**, at baseline line 9 inside the
  canonical block (`# --- canonical output follows ---` is line 8); bytes 3048 (C22, C27).
- plain clean `--drift` (`env -u BASH_ENV -u CHOUSA_GREP_PIN_ECHO -u CHOUSA_RECORD
  -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE`) on the unchanged gate:
  **rc 1, `GATE_DRIFT: -GATE_GREP`** — byte-for-byte the phantom-drift verdict the base
  gate's `env-echo-pin` cell produces.

Variant with `POISON_R37: exported date shadow`: pin rc 0; baseline POISON lines = 1,
bytes 3022 vs clean 2989 (+33 bytes = the injected line); clean drift **rc 1,
`GATE_DRIFT: -LINE`** (C21).

Mechanism: `BASH_ENV` is sourced by the gate process; `export -f date` marks the function
exported, so bash places `BASH_FUNC_date%%` in the environment. The capture child is started
with `env -u … -u BASH_ENV bash …`; GNU env removes only the named variables, so the child
imports `BASH_FUNC_date%%`, calls the shadowed `date`, and the injected line lands in
`capture.txt`. Direct inheritance check (C20): the child of
`env -u BASH_ENV bash -c 'declare -F date; date …'` prints `FUNCTION_PRESENT` and the
injected line. This is not the claims' named limit ("a startup file can still define
functions **in the gate process**"); the function acts **inside the capture child**, the
exact surface `env -u BASH_ENV` was added to isolate. Independent corroboration exists in a
peer artifact (CritC2Kill reports an `export -f env` variant); this report's verdict rests
on the commands above, not on that artifact.

### 4.5 Ground truth: the landed scrub does work for the *named* vectors

Hostile env `/tmp/revc2-hostile.env` (writes `POISON_R37: injected by BASH_ENV` to stderr;
exports `CHOUSA_GREP_PIN_ECHO=1`, `CHOUSA_STRICT=1`, and a foreign `CHOUSA_ROOT`).
Against the landed gate (C15): pin rc 0; the gate process prints the POISON and
`GATE_GREP:` lines to its own stderr, but the **baseline has 0 GATE_GREP lines and 0 POISON
lines, 2989 bytes** — byte-identical canonical body to a clean pin (headers differ only in
`# pinned_ts` by one second). Clean drift of both baselines: rc 0, `GATE_DRIFT: none`.
So the four frozen separation cells are honestly satisfied for their named mechanisms; the
counter's 7/7 is not merely a self-report artifact *for those inputs*. The falsification is
the exported-function mechanism the fixtures omit.

### 4.6 Seed inertness

Seeds 38101 and 38203: `scenarios` arrays byte-identical (`scenarios identical: True`),
`matched` identical, `gate_sha256` identical (C9). `--seed` only labels the receipt.

### 4.7 Base control and a doc/behavior mismatch

- Base gate at seed 38101: **3/7**, exit 1 (C5), matching the frozen `before` matrix
  cell-for-cell: `env-echo-pin` echo=1/`-GATE_GREP`; `env-echo-drift` `+GATE_GREP`;
  `env-fn-echo-pin` identical to `env-echo-pin`; `env-root-pin` drift token list
  (`-FINDING:CHAIN_SOURCE_MISSING …`); three holds pass.
- Base `env-root-pin` manual reproduction (C23): pin rc 0, baseline written (3547 bytes),
  clean drift rc 1 with the token list. `c2-count.py`'s docstring says a foreign
  `CHOUSA_ROOT` "made the capture fail, so `--pin` exited 2 and wrote no baseline at all";
  measured base behavior is a successful pin of a different capture. claims.md's wording
  ("pins a different capture and the drift reports a token list") matches the measurement;
  the counter docstring is stale.

## 5. Findings by severity

**HIGH-1 — C2 claim text is false on the landed gate (exported-function inheritance).**
`BASH_ENV` + `export -f date` (or `export -f env`, per the independent peer artifact)
survives `env -u … -u BASH_ENV`, poisons the pinned baseline, and makes a plain clean
`--drift` report `-GATE_GREP` / `-LINE` (rc 1) on an unchanged gate. Evidence: §4.4
(commands C20, C21, C22, C27). This is the exact failure class C2 claims impossible, and it
is not the named "functions in the gate process" limit because the function executes in the
capture child. C2's P2 predicate does not model it.

**HIGH-2 — P2's pass/fail is gate self-report; the counter does not verify baseline
content.** `c2-count.py:122-130` takes the gate's `GATE_DRIFT:` string and one
`GATE_GREP: ` prefix count as the whole content check. A fabricated gate with no capture
and no comparison scores 7/7 (§4.1); the landed gate with its comparison removed scores 7/7
and misses a poisoned baseline the real gate flags (§4.2); with an exported `date` in the
harness env the counter scores 7/7 while every baseline embeds `POISON_R37` (§4.3). The
predicate is therefore *not* evidence that the baseline is clean; it is evidence that the
gate says it is clean under seven fixed inputs. (This is a measurement-validity defect, not
a scoring defect: the run does print 7/7.)

**MEDIUM-1 — `env-fn-echo-pin` does not test an exported function.** `FN_ENV` has no
`export -f` (`c2-count.py:41`; C24); on base it duplicates `env-echo-pin`'s observations
(C5), and claims.md describes it as "through an exported shell function". One of seven cells
is mislabeled/redundant, and the genuine exported-function vector is untested.

**MEDIUM-2 — `--seed` is inert.** It is only written to the receipt; no fixture derives
from it (C9). The two-fresh-seed clause provides no independent coverage, so "re-derived on
fresh seeds" is nominally true but statistically empty. (The run is deterministic, which is
good for reproducibility; the claim's independence language should not lean on seeds.)

**MEDIUM-3 — `gate_sha256` binding is post-hoc.** `sha256_file(gate)` runs after all 14
gate invocations (`c2-count.py:172-174`). A gate changed mid-run would be bound at its
final bytes, and pin/drift need not have run the same bytes. No per-invocation identity
check exists; the 7/7 receipt also does not record the lane revision or the counter's own
hash. The kill rule's "receipt `gate_sha256` differs" screen is necessary but only sound if
the gate file is stable during the run.

**LOW-1 — scoring ignores `pin_out`.** `pin_out_tail` is recorded but not compared
(`c2-count.py:131-134`); a gate that exits 0 while printing a failed/short pin message
passes if it writes a `GATE_GREP:`-free file.

**LOW-2 — first-line drift parsing.** `drift_line` returns the first `GATE_DRIFT:` line
(`c2-count.py:87-90`); a gate that emits a `none` line before a real drift is scored on the
first.

**LOW-3 — `matched == total`, not `matched == 7`.** `c2-count.py:171`; the printed predicate
uses `total` too (line 170). Today `total=7`, so the frozen string is produced; adding a
scenario later would silently change the predicate surface while still printing 7/7-shaped
text (e.g. 8/8).

**LOW-4 — stale counter docstring.** The base `env-root-pin` mechanism described as pin
rc 2 / no baseline is measured as pin rc 0 / baseline written / drift token list (C23).

**LOW-5 — harness error handling.** Exit 2 is reserved for missing gate/temp
(`c2-count.py:146-152`); a missing `bash` on PATH or a subprocess timeout raises instead of
returning 2. Also, the counter invokes `bash` through PATH (`subprocess.run(["bash", gate]…)`,
lines 82-83), so the counter's own harness is PATH-sensitive even though C2's claim is not
about PATH (C1's surface).

## 6. Residual risk

- The exported-function class is broad: any command the capture child executes can be
  shadowed by an exported function (`date`, `env`, `sed`, `head`, …). `date` and `env`
  variants are demonstrated; `printf` demonstrably reaches the child too but breaks the
  manifest validation (pin rc 2, no baseline), so it is a denial rather than a phantom
  drift. A clean-environment capture (`env -i` plus an explicit allowlist) is the only
  structural fix; adding more `-u` names cannot enumerate `BASH_FUNC_*`.
- The named debt in claims.md (POSIX `ENV`, `SHELLOPTS`/`BASHOPTS`, hostile `TMPDIR`) is
  untouched by this seat; the peer CritC2Kill artifact reports concrete SHELLOPTS/TMPDIR
  vectors, but that is their evidence, not mine.
- The counter's fixture set is fixed and deterministic; it can certify only those seven
  inputs. Any claim sentence broader than the fixtures ("cannot change the pinned capture")
  is unmeasured by P2.
- The gate's own process still sources `BASH_ENV` (named limit); the demonstrated
  `-GATE_GREP` injection into the baseline comes from the capture child, not the gate
  process's echo.

## 7. Verification gaps

- I did not run the gate's selftest (`RESEARCH_GATE_SELFTEST`); I read the three r37 cases
  (`research-gate.sh:8247-8297`) and note they exercise `BASH_ENV` re-export echo, drift-side
  echo, and `CHOUSA_ROOT` only — no `export -f`. Execution of the selftest is wave-1's
  coverage, not this seat's.
- No network was used; no fetch or install occurred.
- The `bash` used by the counter is PATH-resolved (LOW-5); I did not shim it, and the runs
  above used the host's bash.
- I did not test `BASH_ENV` as `ENV` under `--posix`, `SHELLOPTS`, or `TMPDIR`; those are
  named debt and outside this seat's P2 target.
- Scratch dirs remain under `/tmp` (`revc2-*`) for the session; receipts are
  `/tmp/revc2-c2-s38101.json`, `/tmp/revc2-c2-s38203.json`, `/tmp/revc2-base-s38101.json`,
  `/tmp/revc2-mutant-a.json`, `/tmp/revc2-mutant-b.json`,
  `/tmp/revc2-c2-poisoned-harness.json`.

## 8. Command appendix (verbatim commands, observed output, exit code)

### C1 — lane revision and worktree state

```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master; git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain | head -20; git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD
b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65
 M LOG.md
 M SCORECARD.md
 M corpus/QUALITY.md
 M corpus/README.md
 M corpus/SOURCES.md
?? .ufo/waves/round-37/gen-w1-spec.py
?? .ufo/waves/round-37/w1-dispatch.json
?? .ufo/waves/round-37/w1-run.err
?? .ufo/waves/round-37/w1-spec.json
?? .ufo/waves/round-37/w1/
?? corpus/evidence/round37/receipts/c1-after-s37701.json
?? corpus/evidence/round37/receipts/c1-after-s37901.json
?? corpus/evidence/round37/receipts/c1-after-s37921.json
?? corpus/evidence/round37/receipts/c2-after-s37721.json
?? corpus/evidence/round37/receipts/c2-after-s37941.json
?? corpus/evidence/round37/receipts/c2-after-s37961.json
?? corpus/knowledge/claim-pin-provenance-r37.md
?? corpus/knowledge/pin-capture-env-r37.md
?? corpus/lessons/round-37.md
b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65
```

Exit: not separately echoed in this multi-statement call; re-checked in C28
(`GIT_EXIT=0`). Output shows the expected tip and only pre-existing wave/seat artifacts.

### C2 — gate and counter identity

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && sha256sum tools/research-gate.sh && wc -l tools/research-gate.sh corpus/evidence/round37/c2-count.py
9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  tools/research-gate.sh
  8418 tools/research-gate.sh
   185 corpus/evidence/round37/c2-count.py
  8603 total
```

Exit: not separately echoed; both chained commands produced output (`&&` completed);
re-checked in C28 (`GATE_EXIT=0`).

### C3 — P2 fresh-seed run 38101

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && C2_TMP=$(mktemp -d) python3 corpus/evidence/round37/c2-count.py --gate tools/research-gate.sh --seed 38101 --receipt /tmp/revc2-c2-s38101.json; echo "EXIT=$?"
PASS hold-plain       env=none           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS hold-benign      env=benign         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-pin     env=echo           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-drift   env=echo-on-drift  expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-fn-echo-pin  env=fn             expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-root-pin     env=root           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-strict-pin   env=strict         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PIN_CAPTURE_ENV_MATCH=7/7
EXIT=0
```

### C4 — receipt audit

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 - <<'PY'
import json
r=json.load(open('/tmp/revc2-c2-s38101.json'))
print("seed",r["seed"],"gate",r["gate"],"gate_sha256",r["gate_sha256"])
print("matched",r["matched"],"total",r["total"],"predicate_holds",r["predicate_holds"],"predicate",r["predicate"])
for s in r["scenarios"]:
    o=s["observed"]
    print(s["id"], "ok=",s["ok"], "pin_rc=",o["pin_rc"], "file=",o["pin_file"], "echo=",o["baseline_echo_lines"], "drift_rc=",o["drift_rc"], "drift=",repr(o["drift_line"]), "pin_tail=",s["pin_out_tail"])
PY
echo "EXIT=$?"; sha256sum /tmp/revc2-c2-s38101.json
seed 38101 gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh gate_sha256 9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
matched 7 total 7 predicate_holds True predicate PIN_CAPTURE_ENV_MATCH=7/7
hold-plain ok= True pin_rc= 0 file= True echo= 0 drift_rc= 0 drift= 'GATE_DRIFT: none' pin_tail= ['GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39']
hold-benign ok= True pin_rc= 0 file= True echo= 0 drift_rc= 0 drift= 'GATE_DRIFT: none' pin_tail= ['GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39']
env-echo-pin ok= True pin_rc= 0 file= True echo= 0 drift_rc= 0 drift= 'GATE_DRIFT: none' pin_tail= ['GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"']
env-echo-drift ok= True pin_rc= 0 file= True echo= 0 drift_rc= 0 drift= 'GATE_DRIFT: none' pin_tail= ['GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39']
env-fn-echo-pin ok= True pin_rc= 0 file= True echo= 0 drift_rc= 0 drift= 'GATE_DRIFT: none' pin_tail= ['GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"']
env-root-pin ok= True pin_rc= 0 file= True echo= 0 drift_rc= 0 drift= 'GATE_DRIFT: none' pin_tail= ['GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39']
env-strict-pin ok= True pin_rc= 0 file= True echo= 0 drift_rc= 0 drift= 'GATE_DRIFT: none' pin_tail= ['GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39']
EXIT=0
3f08e1bbc8575a457247db267ceca7b5f17cdc89d4a9afb356c491dc05d5819d  /tmp/revc2-c2-s38101.json
```

### C5 — base control, same fresh seed

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && C2_TMP=$(mktemp -d) python3 corpus/evidence/round37/c2-count.py --gate .ufo/waves/round-37/controls/base-gate-r37.sh --seed 38101 --receipt /tmp/revc2-base-s38101.json; echo "EXIT=$?"
PASS hold-plain       env=none           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS hold-benign      env=benign         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
FAIL env-echo-pin     env=echo           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=1 drift_rc=1 'GATE_DRIFT: -GATE_GREP'
FAIL env-echo-drift   env=echo-on-drift  expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=1 'GATE_DRIFT: +GATE_GREP'
FAIL env-fn-echo-pin  env=fn             expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=1 drift_rc=1 'GATE_DRIFT: -GATE_GREP'
FAIL env-root-pin     env=root           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=1 'GATE_DRIFT: -FINDING:CHAIN_SOURCE_MISSING -FINDING:CLAIM_SOURCE_MISSING -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused root supported tallies tally verdict verified'
PASS env-strict-pin   env=strict         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PIN_CAPTURE_ENV_MATCH=3/7
EXIT=1
```

### C6 — base gate hash and receipt inventory

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && sha256sum .ufo/waves/round-37/controls/base-gate-r37.sh; ls corpus/evidence/round37/receipts/ | sort
a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8  .ufo/waves/round-37/controls/base-gate-r37.sh
c1-after-s37001.json
c1-after-s37701.json
c1-after-s37901.json
c1-after-s37921.json
c1-base-s37001.json
c2-after-s37021.json
c2-after-s37721.json
c2-after-s37941.json
c2-after-s37961.json
c2-base-s37021.json
```

Exit: not separately echoed; both commands listed successfully (re-checked in C28,
`BASE_EXIT=0`).

### C7 — second fresh seed 38203

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && C2_TMP=$(mktemp -d) python3 corpus/evidence/round37/c2-count.py --gate tools/research-gate.sh --seed 38203 --receipt /tmp/revc2-c2-s38203.json >/tmp/revc2-run-s38203.out 2>&1; echo "EXIT=$?"; tail -1 /tmp/revc2-run-s38203.out
EXIT=0
PIN_CAPTURE_ENV_MATCH=7/7
```

### C8 — all C2 receipts

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 - <<'PY'
import json,glob
for p in sorted(glob.glob('corpus/evidence/round37/receipts/c2-*.json')):
    r=json.load(open(p))
    print(p, "seed=",r["seed"], "matched=",r["matched"], "/",r["total"], "holds=",r["predicate_holds"], "sha=",r["gate_sha256"][:16], "gate=",r["gate"])
PY
echo "EXIT=$?"
corpus/evidence/round37/receipts/c2-after-s37021.json seed= 37021 matched= 7 / 7 holds= True sha= 9fcac047ddadd616 gate= /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
corpus/evidence/round37/receipts/c2-after-s37721.json seed= 37721 matched= 7 / 7 holds= True sha= 9fcac047ddadd616 gate= /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
corpus/evidence/round37/receipts/c2-after-s37941.json seed= 37941 matched= 7 / 7 holds= True sha= 9fcac047ddadd616 gate= /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
corpus/evidence/round37/receipts/c2-after-s37961.json seed= 37961 matched= 7 / 7 holds= True sha= 9fcac047ddadd616 gate= /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
corpus/evidence/round37/receipts/c2-base-s37021.json seed= 37021 matched= 3 / 7 holds= False sha= a7d3922c768a217a gate= /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh
EXIT=0
```

### C9 — seed comparison

```
$ cd /tmp && python3 - <<'PY'
import json
a=json.load(open('/tmp/revc2-c2-s38101.json'))
b=json.load(open('/tmp/revc2-c2-s38203.json'))
print("seed_a",a["seed"],"seed_b",b["seed"])
print("scenarios identical:", a["scenarios"]==b["scenarios"])
print("matched identical:", a["matched"]==b["matched"], a["matched"], b["matched"])
print("gate_sha identical:", a["gate_sha256"]==b["gate_sha256"])
PY
echo "EXIT=$?"
seed_a 38101 seed_b 38203
scenarios identical: True
matched identical: True 7 7
gate_sha identical: True
EXIT=0
```

### C10 — base receipt audit

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 - <<'PY'
import json
r=json.load(open('/tmp/revc2-base-s38101.json'))
print("base seed",r["seed"],"sha",r["gate_sha256"],"matched",r["matched"])
PY
echo "EXIT=$?"
base seed 38101 sha a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8 matched 3
EXIT=0
```

### C11 — scratch mutants created

```
$ cp /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /tmp/revc2-gate-drift-blind.sh && chmod +x /tmp/revc2-mutant-a.sh /tmp/revc2-gate-drift-blind.sh && sha256sum /tmp/revc2-gate-drift-blind.sh /tmp/revc2-mutant-a.sh; echo "EXIT=$?"
9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  /tmp/revc2-gate-drift-blind.sh
8b85ec9e187b906ed2f29941d0b2daf86a7c7bf5698b9ddfc875438a2d1c1a57  /tmp/revc2-mutant-a.sh
EXIT=0
```

Mutant A content (written via `write`, 853 bytes):

```
#!/usr/bin/env bash
# RevC2 scratch mutant A: NO pin capture, NO drift comparison.
# --pin writes a constant, poisoned baseline (a receipt line that is not
# GATE_GREP:-prefixed, so the counter's only content check cannot see it).
# --drift unconditionally prints GATE_DRIFT: none and exits 0.
case "${1:-}" in
  --pin)
    [[ $# -ge 2 ]] || exit 2
    printf '%s\n' \
      '# chousa-gate drift baseline v1 — fabricated by mutant A' \
      '# volatile_fields=ts gate_sha256' \
      '# --- canonical output follows ---' \
      'POISON_R37: baseline content chosen by the gate, not by any environment' \
      'RESEARCH_GATE: CLEAN' >"$2" || exit 2
    printf 'GATE_PIN: ok path=%s gate_sha256=deadbeef\n' "$2"
    exit 0 ;;
  --drift)
    [[ $# -ge 2 ]] || exit 2
    [[ -e $2 ]] || exit 2
    printf 'GATE_DRIFT: none\n'
    exit 0 ;;
esac
exit 2
```

Mutant B mutation (single line, applied to the copy; read at
`/tmp/revc2-gate-drift-blind.sh:4140-4158` first):

```
  if [[ $body == "$GATE_CAP" ]]; then
→ if true; then  # RevC2 mutation: comparison removed; always reports none
```

### C12 — counter against mutant A

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && C2_TMP=$(mktemp -d) python3 corpus/evidence/round37/c2-count.py --gate /tmp/revc2-mutant-a.sh --seed 38101 --receipt /tmp/revc2-mutant-a.json; echo "EXIT=$?"
PASS hold-plain       env=none           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS hold-benign      env=benign         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-pin     env=echo           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-drift   env=echo-on-drift  expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-fn-echo-pin  env=fn             expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-root-pin     env=root           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-strict-pin   env=strict         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PIN_CAPTURE_ENV_MATCH=7/7
EXIT=0
```

### C13 — counter against drift-blind landed-gate copy

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && C2_TMP=$(mktemp -d) python3 corpus/evidence/round37/c2-count.py --gate /tmp/revc2-gate-drift-blind.sh --seed 38101 --receipt /tmp/revc2-mutant-b.json; echo "EXIT=$?"
PASS hold-plain       env=none           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS hold-benign      env=benign         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-pin     env=echo           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-drift   env=echo-on-drift  expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-fn-echo-pin  env=fn             expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-root-pin     env=root           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-strict-pin   env=strict         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PIN_CAPTURE_ENV_MATCH=7/7
EXIT=0
```

### C14 — drift-blindness on a poisoned baseline

```
$ set -u; T=$(mktemp -d /tmp/revc2-blind.XXXXXX); cd "$T"; B=/tmp/revc2-gate-drift-blind.sh; L=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
env -u BASH_ENV -u CHOUSA_GREP_PIN_ECHO -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE bash "$B" --pin "$T/b.txt" >"$T/pin.out" 2>&1; echo "blind_pin_rc=$?"
printf 'POISON_R37: appended after a clean pin\n' >> "$T/b.txt"
env -u BASH_ENV -u CHOUSA_GREP_PIN_ECHO -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE bash "$B" --drift "$T/b.txt" >"$T/blind-drift.out" 2>&1; echo "blind_drift_rc=$?"; cat "$T/blind-drift.out"
env -u BASH_ENV -u CHOUSA_GREP_PIN_ECHO -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE bash "$L" --drift "$T/b.txt" >"$T/landed-drift.out" 2>&1; echo "landed_drift_rc=$?"; cat "$T/landed-drift.out"
echo "tmpdir=$T"
blind_pin_rc=0
blind_drift_rc=0
GATE_DRIFT: none
landed_drift_rc=1
GATE_DRIFT: -LINE
tmpdir=/tmp/revc2-blind.Tv2MpC
```

### C15 — ground truth: hostile `BASH_ENV` (named vectors) on the landed gate

Hostile file `/tmp/revc2-hostile.env`:

```
printf 'POISON_R37: injected by BASH_ENV\n' >&2
export CHOUSA_GREP_PIN_ECHO=1
export CHOUSA_STRICT=1
export CHOUSA_ROOT=/tmp/revc2-foreign-root
```

```
$ set -u; T=$(mktemp -d /tmp/revc2-truth.XXXXXX); cd /home/vgpnk/Projects/shokunin/chousa-shokunin; G=tools/research-gate.sh
CLEANENV=(env -u BASH_ENV -u CHOUSA_GREP_PIN_ECHO -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE -u CHOUSA_STRICT -u CHOUSA_ROOT)
"${CLEANENV[@]}" bash "$G" --pin "$T/clean.txt" >"$T/clean.out" 2>&1; echo "clean_pin_rc=$?"
BASH_ENV=/tmp/revc2-hostile.env bash "$G" --pin "$T/hostile.txt" >"$T/hostile.out" 2>&1; echo "hostile_pin_rc=$?"
echo "--- hostile pin stdout/stderr ---"; cat "$T/hostile.out"
for f in clean hostile; do
  echo "--- $f baseline: GATE_GREP lines=$(grep -c '^GATE_GREP: ' "$T/$f.txt" || true) POISON lines=$(grep -c 'POISON_R37' "$T/$f.txt" || true) bytes=$(wc -c <"$T/$f.txt")"
done
"${CLEANENV[@]}" bash "$G" --drift "$T/clean.txt" >"$T/clean.drift" 2>&1; echo "clean_drift_rc=$? out=$(cat "$T/clean.drift")"
"${CLEANENV[@]}" bash "$G" --drift "$T/hostile.txt" >"$T/hostile.drift" 2>&1; echo "hostile_drift_rc=$? out=$(cat "$T/hostile.drift")"
python3 - "$T" <<'PY'
import sys,pathlib
T=pathlib.Path(sys.argv[1])
M='# --- canonical output follows ---'
def body(p):
    lines=p.read_text().splitlines()
    i=lines.index(M)
    return lines[:i], lines[i+1:]
hc,hb=body(T/'hostile.txt'); cc,cb=body(T/'clean.txt')
print("hostile header:", hc)
print("clean header:  ", cc)
print("canonical bodies identical:", hb==cb)
print("hostile header sha line:", [l for l in hc if 'gate_sha256' in l])
PY
echo "tmpdir=$T"
clean_pin_rc=0
hostile_pin_rc=0
--- hostile pin stdout/stderr ---
POISON_R37: injected by BASH_ENV
GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"
GATE_PIN: ok path=/tmp/revc2-truth.pY44nT/hostile.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
--- clean baseline: GATE_GREP lines=0 POISON lines=0 bytes=2989
--- hostile baseline: GATE_GREP lines=0 POISON lines=0 bytes=2989
clean_drift_rc=0 out=GATE_DRIFT: none
hostile_drift_rc=0 out=GATE_DRIFT: none
hostile header: ['# chousa-gate drift baseline v1 — written by research-gate.sh --pin', '# lineage: mori-shokunin r10 pin/drift (tools/mori-census.sh); volatile contract per the gate header', '# gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39', '# pinned_ts=2026-10-24T02:39:52Z', '# canonical: verify-all record.md --claims claims.jsonl --json manifest.jsonl --root . (cwd = a fresh temp fixture written by the gate)', '# volatile_fields=ts gate_sha256', '# volatile_note=values of these fields are masked to <V>; --drift re-normalizes with the CURRENT list and reports every changed field. Changing the list is itself drift; gate_sha256 is informational (behavior, not revision, is compared).']
clean header:   ['# chousa-gate drift baseline v1 — written by research-gate.sh --pin', '# lineage: mori-shokunin r10 pin/drift (tools/mori-census.sh); volatile contract per the gate header', '# gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39', '# pinned_ts=2026-10-24T02:39:51Z', '# canonical: verify-all record.md --claims claims.jsonl --json manifest.jsonl --root . (cwd = a fresh temp fixture written by the gate)', '# volatile_fields=ts gate_sha256', '# volatile_note=values of these fields are masked to <V>; --drift re-normalizes with the CURRENT list and reports every changed field. Changing the list is itself drift; gate_sha256 is informational (behavior, not revision, is compared).']
canonical bodies identical: True
hostile header sha line: ['# gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39', '# volatile_fields=ts gate_sha256', '# volatile_note=values of these fields are masked to <V>; --drift re-normalizes with the CURRENT list and reports every changed field. Changing the list is itself drift; gate_sha256 is informational (behavior, not revision, is compared).']
tmpdir=/tmp/revc2-truth.pY44nT
```

### C16 — mutant receipts

```
$ cd /tmp && python3 - <<'PY'
import json
for p in ('/tmp/revc2-mutant-a.json','/tmp/revc2-mutant-b.json'):
    r=json.load(open(p))
    print(p, "seed=",r["seed"], "matched=",r["matched"], "holds=",r["predicate_holds"], "gate_sha256=",r["gate_sha256"])
PY
echo "EXIT=$?"
/tmp/revc2-mutant-a.json seed= 38101 matched= 7 holds= True gate_sha256= 8b85ec9e187b906ed2f29941d0b2daf86a7c7bf5698b9ddfc875438a2d1c1a57
/tmp/revc2-mutant-b.json seed= 38101 matched= 7 holds= True gate_sha256= 24e5fdcc9c809c30b4aa264bf3f1a3a95c20b3ca3bdd2c161420c397bd94ca2e
EXIT=0
```

### C17 — exported `printf` (function inheritance reaches the capture, but breaks validation)

```
$ set -u; T=$(mktemp -d /tmp/revc2-fnx.XXXXXX)
printf '%s\n' 'printf() { builtin printf "$@"; builtin printf "POISON_R37: exported function shadow\n"; }' 'export -f printf' > "$T/fnx.env"
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
BASH_ENV="$T/fnx.env" bash tools/research-gate.sh --pin "$T/fnx.txt" >"$T/fnx.out" 2>&1; echo "fnx_pin_rc=$?"
echo "--- gate output (first 6 lines) ---"; sed -n '1,6p' "$T/fnx.out"
echo "--- baseline checks ---"
echo "baseline exists: $([[ -f $T/fnx.txt ]] && echo yes || echo no)"
echo "POISON lines=$(grep -c 'POISON_R37' "$T/fnx.txt" 2>/dev/null || true) GATE_GREP lines=$(grep -c '^GATE_GREP: ' "$T/fnx.txt" 2>/dev/null || true) bytes=$(wc -c <"$T/fnx.txt" 2>/dev/null || echo NA)"
echo "--- clean drift against the poisoned baseline ---"
env -u BASH_ENV -u CHOUSA_GREP_PIN_ECHO -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE bash tools/research-gate.sh --drift "$T/fnx.txt" >"$T/fnx.drift" 2>&1; echo "clean_drift_rc=$?"; sed -n '1,4p' "$T/fnx.drift"
echo "tmpdir=$T"
fnx_pin_rc=2
--- gate output (first 6 lines) ---
research-gate: --pin canonical capture failed (rc=2 verdict-lines=0 manifest-lines=0 schema-lines=0): /tmp/revc2-fnx.B6PEJX/fnx.txt
POISON_R37: exported function shadow
--- baseline checks ---
baseline exists: no
error: failed to redirect to /tmp/revc2-fnx.B6PEJX/fnx.txt: No such file or directory (os error 2)
POISON lines= GATE_GREP lines= bytes=NA
--- clean drift against the poisoned baseline ---
clean_drift_rc=2
research-gate: --drift baseline missing: /tmp/revc2-fnx.B6PEJX/fnx.txt
tmpdir=/tmp/revc2-fnx.B6PEJX
```

(`error: failed to redirect …` is the shell's redirect diagnostic while probing the
non-existent baseline; no baseline was written. The shadowed `printf` corrupted the
one-line manifest, so validation refused — denial, not phantom drift.)

### C18 — exported `head` (no injection: the child does not call it)

```
$ set -u; T=$(mktemp -d /tmp/revc2-head.XXXXXX)
printf '%s\n' 'head() { /usr/bin/head "$@"; builtin printf "POISON_R37: exported head shadow\n" >&2; }' 'export -f head' > "$T/head.env"
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
BASH_ENV="$T/head.env" bash tools/research-gate.sh --pin "$T/head.txt" >"$T/head.out" 2>&1; echo "head_pin_rc=$?"
echo "--- gate output ---"; cat "$T/head.out"
echo "baseline exists: $([[ -f $T/head.txt ]] && echo yes || echo no)"
if [[ -f $T/head.txt ]]; then
  echo "POISON lines=$(grep -c 'POISON_R37' "$T/head.txt" || true) GATE_GREP lines=$(grep -c '^GATE_GREP: ' "$T/head.txt" || true) bytes=$(wc -c <"$T/head.txt")"
  env -u BASH_ENV -u CHOUSA_GREP_PIN_ECHO -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE bash tools/research-gate.sh --drift "$T/head.txt" >"$T/head.drift" 2>&1; echo "clean_drift_rc=$?"; cat "$T/head.drift"
fi
echo "tmpdir=$T"
head_pin_rc=0
--- gate output ---
GATE_PIN: ok path=/tmp/revc2-head.YwvS3r/head.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
baseline exists: yes
POISON lines=0 GATE_GREP lines=0 bytes=2989
clean_drift_rc=0
GATE_DRIFT: none
tmpdir=/tmp/revc2-head.YwvS3r
```

### C19 — exported `cut` (same: unused in the child's pin path)

```
$ set -u; T=$(mktemp -d /tmp/revc2-cut.XXXXXX)
printf '%s\n' 'cut() { /usr/bin/cut "$@"; builtin printf "POISON_R37: exported cut shadow\n" >&2; }' 'export -f cut' > "$T/cut.env"
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
BASH_ENV="$T/cut.env" bash tools/research-gate.sh --pin "$T/cut.txt" >"$T/cut.out" 2>&1; echo "cut_pin_rc=$?"
echo "--- gate output tail ---"; tail -3 "$T/cut.out"
echo "baseline exists: $([[ -f $T/cut.txt ]] && echo yes || echo no)"
if [[ -f $T/cut.txt ]]; then
  echo "POISON lines=$(grep -c 'POISON_R37' "$T/cut.txt" || true) GATE_GREP lines=$(grep -c '^GATE_GREP: ' "$T/cut.txt" || true) bytes=$(wc -c <"$T/cut.txt")"
  env -u BASH_ENV -u CHOUSA_GREP_PIN_ECHO -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE bash tools/research-gate.sh --drift "$T/cut.txt" >"$T/cut.drift" 2>&1; echo "clean_drift_rc=$?"; tail -2 "$T/cut.drift"
fi
echo "tmpdir=$T"
cut_pin_rc=0
--- gate output tail ---
GATE_PIN: ok path=/tmp/revc2-cut.UuDF9h/cut.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
baseline exists: yes
POISON lines=0 GATE_GREP lines=0 bytes=2989
clean_drift_rc=0
GATE_DRIFT: none
tmpdir=/tmp/revc2-cut.UuDF9h
```

### C20 — exported-function inheritance across `env -u BASH_ENV`

```
$ set -u; T=$(mktemp -d /tmp/revc2-fnin.XXXXXX)
printf '%s\n' 'head() { /usr/bin/head "$@"; builtin printf "POISON_R37: exported head shadow\n" >&2; }' 'export -f head' > "$T/head.env"
cat > "$T/outer.sh" <<'EOF'
#!/usr/bin/env bash
env -u BASH_ENV bash -c 'declare -F head && echo FUNCTION_PRESENT; head -n1 /etc/hostname' 2>&1
EOF
chmod +x "$T/outer.sh"
BASH_ENV="$T/head.env" bash "$T/outer.sh"; echo "EXIT=$?"
echo "tmpdir=$T"
head
FUNCTION_PRESENT
plazir27
POISON_R37: exported head shadow
EXIT=0
tmpdir=/tmp/revc2-fnin.kYDN3T
```

### C21 — exported `date` (POISON variant) on the landed gate

```
$ set -u; T=$(mktemp -d /tmp/revc2-date.XXXXXX)
printf '%s\n' 'date() { /usr/bin/date "$@"; builtin printf "POISON_R37: exported date shadow\n" >&2; }' 'export -f date' > "$T/date.env"
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
BASH_ENV="$T/date.env" bash tools/research-gate.sh --pin "$T/date.txt" >"$T/date.out" 2>&1; echo "date_pin_rc=$?"
echo "--- gate output tail ---"; tail -3 "$T/date.out"
echo "baseline exists: $([[ -f $T/date.txt ]] && echo yes || echo no)"
if [[ -f $T/date.txt ]]; then
  echo "POISON lines=$(grep -c 'POISON_R37' "$T/date.txt" || true) GATE_GREP lines=$(grep -c '^GATE_GREP: ' "$T/date.txt" || true) bytes=$(wc -c <"$T/date.txt")"
  env -u BASH_ENV -u CHOUSA_GREP_PIN_ECHO -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE bash tools/research-gate.sh --drift "$T/date.txt" >"$T/date.drift" 2>&1; echo "clean_drift_rc=$?"; cat "$T/date.drift"
fi
echo "tmpdir=$T"
date_pin_rc=0
--- gate output tail ---
POISON_R37: exported date shadow
GATE_PIN: ok path=/tmp/revc2-date.2eLiJa/date.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
baseline exists: yes
POISON lines=1 GATE_GREP lines=0 bytes=3022
clean_drift_rc=1
GATE_DRIFT: -LINE
tmpdir=/tmp/revc2-date.2eLiJa
```

### C22 — exported `date` (GATE_GREP variant): the exact claimed failure on the landed gate

```
$ set -u; T=$(mktemp -d /tmp/revc2-grepinject.XXXXXX)
printf '%s\n' 'date() { /usr/bin/date "$@"; builtin printf "GATE_GREP: path=/tmp/evil source=override version=\"forged\"\n" >&2; }' 'export -f date' > "$T/inject.env"
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
BASH_ENV="$T/inject.env" bash tools/research-gate.sh --pin "$T/inject.txt" >"$T/pin.out" 2>&1; echo "inject_pin_rc=$?"
echo "baseline GATE_GREP lines=$(grep -c '^GATE_GREP: ' "$T/inject.txt" || true) bytes=$(wc -c <"$T/inject.txt")"
grep -n '^GATE_GREP: ' "$T/inject.txt" || true
env -u BASH_ENV -u CHOUSA_GREP_PIN_ECHO -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE bash tools/research-gate.sh --drift "$T/inject.txt" >"$T/drift.out" 2>&1; echo "clean_drift_rc=$?"; cat "$T/drift.out"
echo "tmpdir=$T"
inject_pin_rc=0
baseline GATE_GREP lines=1 bytes=3048
9:GATE_GREP: path=/tmp/evil source=override version="forged"
clean_drift_rc=1
GATE_DRIFT: -GATE_GREP
tmpdir=/tmp/revc2-grepinject.Eqh95M
```

Baseline context (C27):

```
$ set -u; T=/tmp/revc2-grepinject.Eqh95M; sed -n '3p;7,10p' "$T/inject.txt"; echo "---"; sed -n '1,4p' "$T/pin.out"; echo "EXIT=$?"
# gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
# volatile_note=values of these fields are masked to <V>; --drift re-normalizes with the CURRENT list and reports every changed field. Changing the list is itself drift; gate_sha256 is informational (behavior, not revision, is compared).
# --- canonical output follows ---
GATE_GREP: path=/tmp/evil source=override version="forged"
research-gate v2 — ts=<V> — mode=verify-all — record=record.md — claims=claims.jsonl — root=.
---
GATE_GREP: path=/tmp/evil source=override version="forged"
GATE_PIN: ok path=/tmp/revc2-grepinject.Eqh95M/inject.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
EXIT=0
```

### C23 — base `env-root-pin` manual reproduction

```
$ set -u; T=$(mktemp -d /tmp/revc2-baseroot.XXXXXX); mkdir -p "$T/foreign"
printf 'export CHOUSA_ROOT=%s\n' "$T/foreign" > "$T/root.env"
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
B=/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh
BASH_ENV="$T/root.env" bash "$B" --pin "$T/base-root.txt" >"$T/pin.out" 2>&1; echo "base_root_pin_rc=$?"
cat "$T/pin.out"
echo "baseline exists: $([[ -f $T/base-root.txt ]] && echo yes || echo no) bytes=$(wc -c <"$T/base-root.txt" 2>/dev/null || echo NA)"
env -u BASH_ENV -u CHOUSA_GREP_PIN_ECHO bash "$B" --drift "$T/base-root.txt" >"$T/drift.out" 2>&1; echo "base_root_drift_rc=$?"; cat "$T/drift.out"
echo "tmpdir=$T"
base_root_pin_rc=0
GATE_PIN: ok path=/tmp/revc2-baseroot.9tNRUb/base-root.txt gate_sha256=a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8
baseline exists: yes bytes=3547
base_root_drift_rc=1
GATE_DRIFT: -FINDING:CHAIN_SOURCE_MISSING -FINDING:CLAIM_SOURCE_MISSING -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused root supported tallies tally verdict verified
tmpdir=/tmp/revc2-baseroot.9tNRUb
```

### C24 — `env-fn-echo-pin` fixture is not exported

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && sed -n '28,40p' corpus/evidence/round37/c2-count.py; echo "---"; grep -n "export -f" corpus/evidence/round37/c2-count.py || echo "NO export -f IN COUNTER"; echo "EXIT=$?"
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

# id, bashenv body or None, pin? drift?, expected observations
#   expect: dict(pin_rc, pin_file, baseline_echo_lines, drift_rc, drift_line)
ECHO_ENV = "export CHOUSA_GREP_PIN_ECHO=1\n"
---
NO export -f IN COUNTER
EXIT=0
```

### C25 — counter with an exported function in the harness environment → 7/7

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && bash -c '
date() { /usr/bin/date "$@"; builtin printf "POISON_R37: harness-inherited exported function\n" >&2; }
export -f date
C2_TMP=$(mktemp -d) python3 corpus/evidence/round37/c2-count.py --gate tools/research-gate.sh --seed 38209 --receipt /tmp/revc2-c2-poisoned-harness.json
echo "COUNTER_EXIT=$?"
'; echo "SHELL_EXIT=$?"
PASS hold-plain       env=none           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS hold-benign      env=benign         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-pin     env=echo           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-echo-drift   env=echo-on-drift  expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-fn-echo-pin  env=fn             expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-root-pin     env=root           expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PASS env-strict-pin   env=strict         expected pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'  observed pin_rc=0 file=True echo=0 drift_rc=0 'GATE_DRIFT: none'
PIN_CAPTURE_ENV_MATCH=7/7
COUNTER_EXIT=0
SHELL_EXIT=0
```

### C26 — poisoned baseline under the same harness export (drift says none)

```
$ set -u; T=$(mktemp -d /tmp/revc2-harness.XXXXXX); cd /home/vgpnk/Projects/shokunin/chousa-shokunin
bash -c '
T="$1"; cd "$2"
date() { /usr/bin/date "$@"; builtin printf "POISON_R37: harness-inherited exported function\n" >&2; }
export -f date
bash tools/research-gate.sh --pin "$T/h.txt" >"$T/pin.out" 2>&1; echo "pin_rc=$?"
env -u BASH_ENV -u CHOUSA_GREP_PIN_ECHO -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE bash tools/research-gate.sh --drift "$T/h.txt" >"$T/drift.out" 2>&1; echo "drift_rc=$?"
echo "baseline POISON lines=$(grep -c "POISON_R37" "$T/h.txt") GATE_GREP lines=$(grep -c "^GATE_GREP: " "$T/h.txt") bytes=$(wc -c <"$T/h.txt")"
echo "drift_out=$(cat "$T/drift.out")"
' _ "$T" /home/vgpnk/Projects/shokunin/chousa-shokunin
echo "tmpdir=$T"
pin_rc=0
drift_rc=0
baseline POISON lines=1 GATE_GREP lines=0 bytes=3037
drift_out=POISON_R37: harness-inherited exported function
GATE_DRIFT: none
tmpdir=/tmp/revc2-harness.GKWYLo
```

### C28 — exit-status re-check for C1/C2/C6 facts

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && git rev-parse master; echo "GIT_EXIT=$?"; sha256sum tools/research-gate.sh; echo "GATE_EXIT=$?"; sha256sum .ufo/waves/round-37/controls/base-gate-r37.sh; echo "BASE_EXIT=$?"
b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65
GIT_EXIT=0
9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  tools/research-gate.sh
GATE_EXIT=0
a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8  .ufo/waves/round-37/controls/base-gate-r37.sh
BASE_EXIT=0
```

### C29 — poisoned baseline line location (date variant)

```
$ set -u; T=/tmp/revc2-date.2eLiJa; grep -n 'POISON_R37' "$T/date.txt"; echo "---"; sed -n '1,3p' "$T/date.txt"; echo "--- clean baseline from truth run ---"; grep -c '^LINE\|POISON' /tmp/revc2-truth.pY44nT/clean.txt || true; echo "EXIT=$?"
9:POISON_R37: exported date shadow
---
# chousa-gate drift baseline v1 — written by research-gate.sh --pin
# lineage: mori-shokunin r10 pin/drift (tools/mori-census.sh); volatile contract per the gate header
# gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
--- clean baseline from truth run ---
0
EXIT=0
```

(The `EXIT=0` there is the final `|| true` chain's status; the clean baseline has no
`LINE`/`POISON` text.)

### C30 — final identity check after the report write

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && git rev-parse master; echo "TIP_EXIT=$?"; sha256sum tools/research-gate.sh; echo "GATE_EXIT=$?"; ls -l .ufo/waves/round-37/residual/RevC2FreshSeed.md; echo "REPORT_EXIT=$?"
b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65
TIP_EXIT=0
9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  tools/research-gate.sh
GATE_EXIT=0
-rw-r--r-- 1 vgpnk vgpnk 58077 Oct 23 23:47 .ufo/waves/round-37/residual/RevC2FreshSeed.md
REPORT_EXIT=0
```

## 9. Tooling note

No tool was installed, upgraded, or reconfigured. No network access was used. Pacman was
not invoked (host-wide pause respected). Bash/Python/GNU coreutils were already present and
sufficient.
