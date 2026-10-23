# ExecPinModePinDrift — round-35 w2: baseline modes (`--pin`/`--drift`) under the grep pin

Lane: chousa (deep-research method). Wave: round-35, attempt 2. Seat: executor.
Scope (from taskCall): *baseline modes under the pin — `--pin` and `--drift` on a scratch
baseline file, each with (a) clean env, (b) refused override (relative path) → expect
exit 2 and no baseline write/read, (c) refused non-GNU override. Report exit codes, files
touched, stderr. A baseline written despite a refused pin is a finding.*

Artifacts (all under `.ufo/waves/round-35/w2/ExecPinModePinDrift/`, each < 1 MiB, with
`SHA256SUMS.txt`): `pin-drift-matrix-receipt.txt`, `pin-drift-matrix.sh`,
`strace-refused-pin.txt`, `strace-refused-drift.txt`, `strace-refused-drift-current-gate.txt`,
`strace-clean-pin.txt`, `ctl-validate-only-gate.sh`, `gate-snapshot-a476885.sh`,
`nongnu-banner-stub`, `c1-*.json`. Big logs stayed in `/tmp/hyaku/chousa-r35/w2/ExecPinModePinDrift/`.

## Gates measured

| id | path | sha256 (prefix) | when |
|---|---|---|---|
| landed-at-wave-start | `tools/research-gate.sh` | `1f2fb4f522d9a670` | start of this seat (matches the taskCall's expected landed gate) |
| current-at-seat-end | `tools/research-gate.sh` | `a47688518e509edbf` | end of this seat |
| round-34 base | `.ufo/waves/round-35/repairs/base-gate.sh` | `a6307edf687ac0fb` | before |

**Wave-shape note (not my finding to fix).** The lane file `tools/research-gate.sh` was
edited **by another seat while I was running**: it was `1f2fb4f5…` at my first read and is
`a4768851…` now (`git status` shows ` M tools/research-gate.sh`; the diff moves the `grep()`
wrapper into `grep_pin_define`, adds a `timeout(1)`-bounded `--version` probe, drops the
`command -v grep` PATH fallback, and adds readonly-variable refusals). I therefore ran
**every** scenario twice — once against `1f2fb4f5…` and once against a frozen snapshot
`a4768851…` (`gate-snapshot-a476885.sh`) — and every result below is identical on both.
All C1 receipts pin the gate sha they were run against, so no receipt is ambiguous.

## 1. Verdict on the assigned item

**The pin/drift baseline modes are correctly fail-closed under a refused pin. No baseline is
written and no baseline is read when the pin is refused. No finding.**

### 1a. `--pin` / `--drift` matrix (receipt: `pin-drift-matrix-receipt.txt`)

| # | mode | env | exit | stdout | stderr | baseline file |
|---|---|---|---|---|---|---|
| M1 | `--pin` | clean | **0** | `GATE_PIN: ok path=…/m1.baseline gate_sha256=…` | *(empty)* | **written**, 2989 bytes |
| M2 | `--pin` | `RESEARCH_GATE_GREP=bin/grep` (relative) | **2** | *(empty)* | `research-gate: GREP_PROVENANCE refused: override is not an absolute path (candidate=bin/grep)` | **absent** (`No such file or directory`) |
| M3 | `--pin` | `RESEARCH_GATE_GREP=<non-GNU stub>` | **2** | *(empty)* | `research-gate: GREP_PROVENANCE refused: override does not report GNU grep: grep (pi-uu-grep) 0.2.0 (candidate=…/nongnu-banner)` | **absent** |
| M4 | `--drift` | clean | **0** | `GATE_DRIFT: none` | *(empty)* | read-only, unchanged |
| M5 | `--drift` | relative override | **2** | *(empty)* | `research-gate: GREP_PROVENANCE refused: override is not an absolute path (candidate=bin/grep)` | not read, unchanged |
| M6 | `--drift` | non-GNU override | **2** | *(empty)* | `research-gate: GREP_PROVENANCE refused: override does not report GNU grep: grep (pi-uu-grep) 0.2.0 (candidate=…/nongnu-banner)` | not read, unchanged |

### 1b. "No baseline write/read" — proven by syscall trace, not by exit code

`strace -f -qq -e trace=%file` around the refused runs (`strace-refused-pin.txt`,
`strace-refused-drift.txt`, `strace-refused-drift-current-gate.txt`):

* refused `--pin`: the target baseline path is **never mentioned** (0 hits) and the file
  does not exist afterwards. The only files opened are the loader/locale/libc set — the gate
  died in `grep_pin_init` before any mode ran.
* refused `--drift`: the baseline path is **never opened** (0 hits) — the refusal precedes
  `run_drift`'s `[[ -e $path ]]` check, so no read of a baseline that is not there happens.
* refused `--pin` against an **existing** baseline at the target path: sha256 and size
  unchanged (2989 → 2989, identical hash) — the refusal does not truncate or clobber.
* refused `--drift` against an existing baseline: mtime and sha256 unchanged.
* `TMPDIR` side effects: 0 entries after refused `--pin`, refused `--drift`, clean `--pin`
  and clean `--drift` — the canonical fixture is never even created under a refusal
  (`mkdir` of `chousa-gate-pin.*` count in the refused strace = 0; the clean-pin strace
  shows the mkdir **and** the cleanup, `strace-clean-pin.txt`).

### 1c. Ordering and precedence (the refusal wins, as claimed)

* `research-gate.sh --pin PATH --root .` with a bad override → exit 2 with the
  **GREP_PROVENANCE** message, not the usage message; with a good override → exit 2 with
  `research-gate: --pin/--drift take only a baseline path`. `grep_pin_init` runs before the
  pin/drift argument validation (gate lines ~8035-8055), so the refusal is strictly earlier.
* `--drift` with a **missing** baseline + bad override → GREP_PROVENANCE (exit 2); with a
  good override → `research-gate: --drift baseline missing: …` (exit 2). Same exit code,
  distinguishable message, refusal first.
* `--help` under a bad override → exit 0, empty stderr (help path returns before the pin).
* `--bogus` under a bad override → exit 2, `research-gate: unknown flag: --bogus` + usage
  (argument parsing precedes the pin) — consistent with the header's "usage/--help paths
  return earlier, so argument errors stay usage".
* **Before (round-34 base gate `a6307edf…`)**, the same relative override was silently
  ignored: `--pin` exited **0** and wrote the baseline, `--drift` printed `GATE_DRIFT: none`.
  The refusal is new in this round and is strictly an improvement.

### 1d. Positive operability results under the pin (both gate versions)

* `--pin`/`--drift` work with **grep entirely absent from `PATH`** (a 38-tool PATH without
  grep): pin exit 0, drift exit 0 `GATE_DRIFT: none`. The base gate could not even run
  there (S3 in the C1 counter measures `rc=2`, "GNU grep with -z/-P support is required").
* A `PATH` shim `grep` earlier in `PATH` is **not** invoked by `--pin` (shim tripwire
  0 bytes); the pin resolves `/usr/bin/grep` directly.
* A `BASH_ENV` `grep()` function shim is **not** invoked by `--pin` (tripwire 0 bytes).
* The override **is** honoured end-to-end: with `RESEARCH_GATE_GREP` pointing at a
  logging wrapper that reports "GNU grep", the wrapper recorded **33** calls (3 in the
  gate's own cwd, 30 inside the canonical capture fixture) — the inner capture runs the
  same gate and inherits the same pin.
* `--pin` output is reproducible: two pins on the same host differ only in `# pinned_ts=`
  (diff of the rest is empty).

## 2. Findings against the C1 measurement apparatus (calibration)

### 2a. **FINDING (important): the C1 counter cannot tell "override honoured" from "override validated then discarded" — a mutant scores 9/9.**

`corpus/evidence/round35/c1-count.py` scores 9/9 on a gate whose `grep_pin_init`
**validates** `RESEARCH_GATE_GREP` and then **ignores it**, always running `/usr/bin/grep`.

* Mutant: `ctl-validate-only-gate.sh` (sha256 `74de1c9052e9818c…`), one-line change to the
  gate — `GREP_BIN=/usr/bin/grep   # MUTANT: the override is validated but never used`
  inserted just before the echo.
* Score: `GREP_PIN_MATCH=9/9`, `predicate_holds=true`, receipt
  `c1-mutant-9of9.json` (gate sha `74de1c90…`, seed 9301). Same on the current gate
  snapshot (`a4768851…`, seed 9401 → 9/9).
* **Why it passes.** The counter's only override scenario, S7/S9, always sets the override
  to `REAL_GREP = "/usr/bin/grep"` (`c1-count.py:53`, used at `:250` and `:267`). The
  mutant's echo therefore still prints `path=/usr/bin/grep`, which is exactly what S7/S8
  assert (`"path=%s" % REAL_GREP in line`). Since the counter never uses an override path
  that *differs* from the default, "the override was used" and "the override was thrown
  away" are indistinguishable. S1/S2/S9's tripwires watch for a *PATH/BASH_ENV* shim, not
  for the override binary being executed.
* **Direct proof the override is not used by the mutant.** With
  `RESEARCH_GATE_GREP=<logging GNU-reporting wrapper>`: the landed gate invokes the wrapper
  (**33** recorded calls, and the echo reports the wrapper's own path), the mutant invokes
  it **0** times and still reports `path=/usr/bin/grep`. With a *distinct* absolute GNU
  grep (`work/realgrep2`) the landed gate echoes
  `path=…/work/realgrep2 source=override`, the mutant still echoes
  `path=/usr/bin/grep source=override` — i.e. **the mutant's receipt misreports the pinned
  binary**, and the counter cannot see it.
* **Calibration consequence.** P1's 9/9 therefore does **not** establish that the override
  is honoured — it establishes only that a refusal fires for bad overrides and that the
  echo line has the right shape. A gate that accepts `RESEARCH_GATE_GREP`, validates it,
  and then silently runs a different binary passes the frozen predicate. That is the
  *shape* of a fingerprint-and-shortcut engine that C1 was supposed to exclude.
  [INFERENCE] The fix is one line in the counter: use an override path that differs from
  the default (e.g. a symlink/copy at a scratch path) and assert the echo reports *that*
  path, or assert the override binary was actually executed (a call tripwire on the
  override, as S1/S2 do for the shim). I did **not** edit the committed counter.

### 2b. **FINDING: `CHOUSA_GREP_PIN_ECHO=1` leaks into the pinned baseline body, breaking the baseline's byte-stability contract and the drift verdict.**

* The echo is printed to **stderr** (gate line 418, `>&2`) at pin-resolution time, and the
  canonical capture redirects the inner gate's stderr into `capture.txt`
  (`>capture.txt 2>&1`, gate line ~3886). The capture's `env -u` list clears
  `CHOUSA_RECORD/CLAIMS/STRICT/ROOT/AGGREGATOR_ERE` but **not** `CHOUSA_GREP_PIN_ECHO`
  (gate line ~3884-3885). So the echo line lands *inside* the captured canonical block:
  `GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"`
  appears at line 9 of the baseline file.
* **Consequence 1 — the pin/drift pair is not echo-invariant.** Pin with
  `CHOUSA_GREP_PIN_ECHO=1`, drift with it off → `GATE_DRIFT: -LINE` (exit 1). Pin with it
  off, drift with it on → `GATE_DRIFT: +LINE` (exit 1). The gate's *behaviour* did not
  change; only a diagnostic knob did, and the drift verdict flipped to DRIFT.
  (Measured on both `1f2fb4f5…` and `a4768851…`.)
* **Consequence 2 — the baseline stops being host-portable**, contradicting the header's
  own contract: *"Every printed path is relative, so the capture is byte-stable wherever
  the gate is run"* (gate header, ~line 246-248). The leaked line carries an **absolute**
  path (`/usr/bin/grep`) and the grep **version**. Two hosts with the same gate but
  different grep paths/versions produce different baselines: drift reports
  `GATE_DRIFT: path source version` (path differs) or `GATE_DRIFT: path source` (same
  path, different version banner). The version is only half-detectable anyway: the drift
  tokeniser `grep -oE '[A-Za-z_][A-Za-z0-9_-]*=[^[:space:]]*'` (gate line ~3934) truncates
  `version="grep (GNU grep) 3.12-modified"` at the first space, so two *different* versions
  produce the identical token `version="grep` — a version-only change degrades to the
  generic token `LINE`.
* **Mechanism confirmed, and the fix is one `env -u`.** A control copy with
  `-u CHOUSA_GREP_PIN_ECHO` added to the capture's `env -u` list yields **0** `GATE_GREP`
  lines in the baseline and makes pin/drift echo-invariant (`GATE_DRIFT: none` both
  directions). [INFERENCE] The landing fix is to add that `env -u` at gate line ~3884.
* Note the interaction with the *baseline is otherwise blind to the pin*: with the echo off
  the baseline bodies are **byte-identical** whether the pin was `/usr/bin/grep` or a
  different GNU grep. The baseline records no grep provenance at all, so `--drift` cannot
  report "the pinned grep changed" — a deliberate-looking choice (behaviour, not
  revision) but worth stating in the header.

### 2c. Minor: refusal message wording names the candidate but the default-branch
refusal text changed mid-wave

The landed-at-start gate's default-branch refusal reads
`no GNU grep found at /usr/bin/grep, /bin/grep or on PATH`; the current gate reads
`no GNU grep at /usr/bin/grep or /bin/grep (set RESEARCH_GATE_GREP to an absolute path)`
after the `command -v grep` fallback was dropped. Not a defect — the fallback was
demonstrably dead code (`command -v grep` inside the script resolves the script's own
`grep()` function) — but the *contract* sentence in the header still says "or on PATH",
so the header and the code disagree on the current version.

## 2d. Erratum cross-reference (claims.md was appended mid-wave)

`corpus/evidence/round35/claims.md` gained an "Erratum (round 35, append-only, after the
data)" section while I was running. Its item 3 already lists surviving C1 controls that
score 9/9 — "a gate that opens the record and then refuses" (MutPinRefusals), engines that
replace `tok_span_offsets_direct` (MutGrepPinEngines), and a `BASH_ENV` `command()`
function (MutGrepShimEnv) — with the correct summary "Per-call engine identity is **not**
measured".

**My 2a mutant is a distinct vector from those.** It does not change the matcher, the
refusal order, or the `command` dispatch: it changes only what `GREP_BIN` is set to after
the override has been validated. The consequence is different in kind — the gate's own
**receipt line lies**. With `RESEARCH_GATE_GREP=<distinct absolute GNU grep>` the mutant
prints `GATE_GREP: path=/usr/bin/grep source=override version="…"` — it reports the
*default* path while claiming `source=override`, so a receipt reader would conclude the
operator's requested binary was in force when it was not. The erratum's "per-call engine
identity is not measured" framing does not cover a receipt that misreports the pinned
path; that is a **provenance-falsehood** gap, not only an identity-unmeasured gap. My
mutant's sha256 is `74de1c9052e9818c…` and its receipt is `c1-mutant-9of9.json`.

Erratum item 4 states the final gate is `a4768851…` and that the three reported vectors
were removed. Confirmed: the lane file is `a4768851…` and it contains no `command`-keyword
dispatch, no `head` in the version probe, and no `command -v grep` fallback. **My finding
2b (the echo leak into the pinned baseline) is NOT among the removed vectors and is still
present in the final bytes** — re-verified below against `a4768851…` itself.

## 2e. Final-gate re-verification (bytes `a4768851…`)

Re-ran the load-bearing scenarios against the **final** lane gate (not my snapshot):

* refused relative override, `--pin` → exit 2, `GREP_PROVENANCE refused: override is not an
  absolute path (candidate=bin/grep)`, no baseline written.
* refused relative override, `--drift` → exit 2, same message, baseline not read.
* `--pin` with echo ON → 1 `GATE_GREP` line inside the baseline body;
  `--pin` with echo OFF → 0 such lines.
* drift(echo OFF) vs an echo-OFF baseline → `GATE_DRIFT: none`, exit 0.
* drift(echo ON) vs the same echo-OFF baseline → `GATE_DRIFT: +LINE`, exit 1.
* drift(echo OFF) vs an echo-ON baseline → `GATE_DRIFT: -LINE`, exit 1.

So the **asymmetry** is the sharp form of 2b: the baseline is not a function of the gate's
behaviour alone but of the ambient `CHOUSA_GREP_PIN_ECHO` at pin time, and the drift
verdict flips to DRIFT on a diagnostic knob, with a token (`+LINE`/`-LINE`) that names
neither the knob nor the grep. A pin taken with the echo on and a drift taken with the echo
off — the natural pairing, since the echo is the receipt switch — reports DRIFT on a gate
that has not changed at all.

## 3. Re-derivation of the C1 numbers (independent of the L1's seeds)

All with `C1_TMP` pointed at my scratch dir, counter unmodified:

| gate | sha256 | seed | result | receipt |
|---|---|---|---|---|
| landed-at-start | `1f2fb4f5…` | 9101 | `GREP_PIN_MATCH=9/9`, `predicate_holds=true` | `c1-landed-9of9.json` |
| current snapshot | `a4768851…` | 9401 | `GREP_PIN_MATCH=9/9` | (in /tmp) |
| round-34 base | `a6307edf…` | 9201 | `GREP_PIN_MATCH=0/9`, `predicate_holds=false` | `c1-base-0of9.json` |
| committed hardcoded control | `05bdf654…` | 9202 | `GREP_PIN_MATCH=3/9`, `predicate_holds=false` | `c1-hardcoded-ctl-3of9.json` |
| **validate-only mutant** | `74de1c90…` | 9301 | **`GREP_PIN_MATCH=9/9`, `predicate_holds=true`** | `c1-mutant-9of9.json` |

The base's failure detail is exactly as the claim record describes: S1 tripwire 852 bytes,
S2 tripwire 867 bytes (the shims *were* intercepting), S3 `rc=2` with
`"GNU grep with -z/-P support is required"`, S4–S9 all `rc=1` with no `GREP_PROVENANCE`
marker. So C1's *before* is confirmed and the landed gate's 9/9 is confirmed.

**The claim record's control analysis needs one correction:** `claims.md` says the committed
hardcoded control "wins S1–S3 and loses every refusal, provenance and naming scenario, so
the counter discriminates". It discriminates *that* control — but 2a shows a **different**
cheap control (validate the override, then ignore it) that wins **all nine**. The
discrimination claimed for C1 is therefore weaker than the record states.

## 4. Limits of this seat

* I did **not** edit the committed counter, the witness tool, the gate, or any lane
  production file. All mutated gates are in my own directory
  (`.ufo/waves/round-35/w2/ExecPinModePinDrift/`) and in /tmp.
* No network. No `pacman`. Only `/tmp` writes (plus my own wave-2 directory).
* The lane gate file changed under me mid-run (§ "Gates measured"); every result above was
  re-verified on both versions, but a *third* revision may land after this report.
* The mutant in 2a is a single-line mutation of the gate's own pin code; it demonstrates a
  **counter blind spot**, not a defect in the landed gate. The landed gate does honour the
  override (33 recorded calls) and does refuse bad pins.
* I did not audit C2 (witness battery) or the claim record's prose beyond the C1 control
  analysis in §3.
* Time-box: this seat ran ~50 min wall clock (start 2026-10-23 ~16:58, report ~17:12
  local).

## 5. Commands (verbatim, reproducible)

```bash
GATE=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
W=/tmp/hyaku/chousa-r35/w2/ExecPinModePinDrift/work; export TMPDIR=$W/tmp
# matrix
env -u CHOUSA_GREP_PIN_ECHO -u RESEARCH_GATE_GREP -u BASH_ENV \
    bash "$GATE" --pin  $W/m1.baseline          # exit 0, GATE_PIN: ok
env -u CHOUSA_GREP_PIN_ECHO -u BASH_ENV RESEARCH_GATE_GREP=bin/grep \
    bash "$GATE" --pin  $W/m2.baseline          # exit 2, GREP_PROVENANCE refused
env -u CHOUSA_GREP_PIN_ECHO -u BASH_ENV RESEARCH_GATE_GREP=$D/nongnu-banner \
    bash "$GATE" --pin  $W/m3.baseline          # exit 2, GREP_PROVENANCE refused
env -u CHOUSA_GREP_PIN_ECHO -u RESEARCH_GATE_GREP -u BASH_ENV \
    bash "$GATE" --drift $W/m1.baseline         # exit 0, GATE_DRIFT: none
env -u CHOUSA_GREP_PIN_ECHO -u BASH_ENV RESEARCH_GATE_GREP=bin/grep \
    bash "$GATE" --drift $W/m1.baseline         # exit 2, GREP_PROVENANCE refused
# no baseline touch, proven by syscall trace
env -u BASH_ENV RESEARCH_GATE_GREP=bin/grep strace -f -qq -e trace=%file \
    -o $W/strace-as.txt bash "$GATE" --pin $W/as.baseline
env -u BASH_ENV RESEARCH_GATE_GREP=bin/grep strace -f -qq -e trace=%file \
    -o $W/strace-at.txt bash "$GATE" --drift $W/base.txt
# counter, unmodified
C1_TMP=$PWD/c1tmp python3 \
  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round35/c1-count.py \
  --gate $PWD/ctl-validate-only-a476885.sh --seed 9301 --receipt $PWD/c1-mut-new.json
# → GREP_PIN_MATCH=9/9, predicate_holds=true
```
