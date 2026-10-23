# ExecPinModeVerify — round-35 w2: mode `verify` under the grep pin

**Seat:** executor (leaf, no subagents dispatched).
**Lane:** chousa (deep-research method), `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
**Wave base revision:** `e87c5d7ea2dbf3730b36a3961de3f06261d015e4` (clone at
`/tmp/hyaku/chousa-r35/w2/ExecPinModeVerify/clone`, `git clone -q` + `checkout -q`).
**Gate scored:** `tools/research-gate.sh` sha256
`1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` — matches the
round's declared landed gate.
**Pre-round gate (control):** `.ufo/waves/round-35/repairs/base-gate.sh` sha256
`a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` — matches the
declared round-34 blob.
**Scratch:** `/tmp/hyaku/chousa-r35/w2/ExecPinModeVerify/` (241 MB); this seat's repo
directory: `.ufo/waves/round-35/w2/ExecPinModeVerify/` (report only; no other file written).
**Tools installed:** none. No network. No pacman transaction.

> **Note on the lane working tree (observed, not caused by this seat).** When this seat
> finished, the *live* lane file `tools/research-gate.sh` no longer hashed to the pinned
> value — it hashed `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`
> (`git diff --stat` → 32 insertions / 11 deletions against `e87c5d7e`). This seat made no
> write to any lane production file; every measurement below was taken against the **clone**
> at `e87c5d7e`, whose gate hashes to the pinned `1f2fb4f5…`. A sibling seat is editing the
> live gate during the wave. Any re-measurement of this report must re-pin the gate sha and
> confirm it is `1f2fb4f5…` before the numbers are read as this seat's evidence.

---

## 0. Verdict summary

| # | Finding | Severity | Axis | Status |
|---|---|---|---|---|
| **A** | The assigned matrix (a)–(d) passes: `verify` on a committed record is byte-identical across clean PATH, PATH shim, override+shim and echo; tripwires stay empty; exit codes identical; verdict `CLEAN` | — | operability | **no defect** |
| **F1** | The pin's *provenance check itself* resolves `head` through `PATH`/`BASH_ENV` — a `head` shim makes a **non-GNU** binary pass the GNU check, so a wrong binary is pinned and the gate produces a **wrong verdict** (`DRIFT` where the honest run says `CLEAN`) | **crit** | calibration | **new defect in the landed gate, not covered by P1** |
| **F2** | The `PATH` fallback branch of the pin (lines 388–391) is **dead code**: the gate's own `grep()` shell function shadows `command -v grep`, so the fallback can never fire and the refusal message over-promises | **warn** | operability | **new defect in the landed gate, not covered by P1** |

Both F1 and F2 sit *inside the surface C1 claims to own* ("resolves, verifies and pins ONE
grep binary") and are **outside the P1 counter's nine scenarios**. P1 still prints 9/9 —
the counter cannot see either defect. That is the calibration result of this wave.

---

## 1. The assigned matrix — `verify` mode on a committed record

**Record (cited):** `corpus/fixtures/archives-r9/A-r9.md` — a committed `research-record v1`
fixture, tracked (`git ls-files --error-unmatch` OK), last touched by commit `5691bf5`,
banner at line 1 (`# research-record v1`), 56 lines. It is the round-9 archive record whose
`## Meta` binds `research/deep-research-2026-09-28/A-shokunin-tradition.md`; the archive bytes
were copied read-only from the workspace root
`/home/vgpnk/Projects/shokunin/research/deep-research-2026-09-28/` into a scratch root
(`/tmp/hyaku/chousa-r35/w2/ExecPinModeVerify/root/`) so the record's pointers resolve and the
run reaches `CLEAN` instead of `DRIFT` on unresolved pointers.

**Harness:** `run-matrix.sh`, `run-verify-pin.sh`, `run-attacks.sh`, `run-escalate.sh`,
`final-evidence.sh` (all under the scratch dir). Every run is `env -i` (clean environment)
with only `PATH` and the scenario variables set, `CHOUSA_NOW_EPOCH=1750000000` pinned so the
`ts=` header is stable, `bash tools/research-gate.sh verify --record <rec> --root <root>`.

### Results (matrix run, `out2/`)

| scenario | PATH | env | rc | verdict line | trip_path | trip_fn |
|---|---|---|---|---|---|---|
| a-clean | `/usr/local/bin:/usr/bin:/bin` | — | **0** | `RESEARCH_GATE: CLEAN (findings=0 drift=0 questions=1 sources=6 chains=7 claims=5 negatives=1 rejections=4 approvals=0)` | 0 B | 0 B |
| b-pathshim | `<shim>:` + clean | — | **0** | same line, byte-identical | **0 B** | 0 B |
| c-override+shim | `<shim>:` + clean | `RESEARCH_GATE_GREP=/usr/bin/grep` | **0** | same line, byte-identical | **0 B** | 0 B |
| d-echo | clean | `CHOUSA_GREP_PIN_ECHO=1` | **0** | same line, byte-identical | 0 B | 0 B |
| e-override+echo+shim | `<shim>:` + clean | both set | **0** | same line, byte-identical | **0 B** | 0 B |
| f-bashenv-fn | clean | `BASH_ENV=<grep() logger>` | **0** | same line, byte-identical | 0 B | **0 B** |
| g-bashenv+override | `<shim>:` + clean | `BASH_ENV` + override | **0** | same line, byte-identical | **0 B** | **0 B** |

### Byte-identity of (a) vs (b) — **YES**

```
  a-clean vs b-pathshim : IDENTICAL        (cmp, stdout, pinned clock)
  a-clean vs c-override+shim : IDENTICAL
  a-clean vs d-echo : IDENTICAL
  a-clean vs e-override+echo+shim : IDENTICAL
  a-clean vs f-bashenv-fn : IDENTICAL
  a-clean vs g-bashenv+override : IDENTICAL
```
stderr is likewise IDENTICAL for b/c/f/g (the echo line is the only stderr difference, and it
only appears in d/e where it is expected).

**Caveat on byte-identity (honest limit):** the stdout header embeds a wall-clock timestamp
(`research-gate v2 — ts=2026-10-23T19:59:21Z — mode=verify — record=…`,
`tools/research-gate.sh:1170`). With the clock *not* pinned, (a) and (b) differ in exactly
that one field and nowhere else:

```
$ diff out/a-clean.out out/b-pathshim.out
1c1
< research-gate v2 — ts=2026-10-23T19:59:21Z — mode=verify — record=corpus/fixtures/archives-r9/A-r9.md
---
> research-gate v2 — ts=2026-10-23T19:59:22Z — mode=verify — record=corpus/fixtures/archives-r9/A-r9.md
```
So the correct statement is: **(a) and (b) are byte-identical modulo the `ts=` field; with
`CHOUSA_NOW_EPOCH` pinned they are byte-identical outright.** The gate's own comment claims
the pin keeps "every existing mode keeps its byte-identical output" — true for the pin, but
the mode header is *not* byte-stable across runs even without the pin, so a naive
"byte-identical" gate on stdout needs the clock pinned.

### The echo line

* (d) `CHOUSA_GREP_PIN_ECHO=1`, default pin — on **stderr**:
  `GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"`
* (e) with `RESEARCH_GATE_GREP=/usr/bin/grep`:
  `GATE_GREP: path=/usr/bin/grep source=override version="grep (GNU grep) 3.12-modified"`
* Emitted by `tools/research-gate.sh:399-401` (`printf … >&2`). **stdout is unaffected** — the
  echo never leaks into stdout, so a stdout-only byte comparison stays valid.

### Tripwire emptiness — the pin really does intercept

* PATH shim (`grep` script logging every invocation, then `exec /usr/bin/grep`): **0 bytes**
  written in every landed-gate scenario.
* `BASH_ENV` `grep()` function shim: **0 bytes** written.
* **Control (base gate, round-34 blob `a6307edf…`) under the same PATH shim: 15 invocations,
  1786 bytes** (`out/base-shim.log`; first entries `-qE research-record v1|chousa-record: v1`,
  `-qE ^(Skip to content|ChatGPT|You said:) corpus/fixtures/archives-r9/A-r9.md`).
  Under the same `BASH_ENV` function shim the base gate logs **4 invocations, 368 bytes**.
* The base gate's stdout under the shim is identical to the landed gate's stdout
  (`diff` of `tail -n +2` → identical), i.e. the shortcut was invisible to output alone —
  exactly the round-34 closure finding, re-derived.

**So the headline C1 mechanism holds in `verify` mode:** the landed gate resolves one absolute
GNU grep and never touches the `PATH` shim or the `BASH_ENV` function, while the base gate
does both.

### Additional `verify`-mode scenarios (out3/)

| scenario | env | rc | stderr |
|---|---|---|---|
| A1 non-GNU override, no shim | `RESEARCH_GATE_GREP=<stub printing "grep (pi-uu-grep) 0.2.0">` | **2** | `research-gate: GREP_PROVENANCE refused: override does not report GNU grep: grep (pi-uu-grep) 0.2.0 (candidate=…)` |
| A4 relative override | `RESEARCH_GATE_GREP=bin/grep` | **2** | `research-gate: GREP_PROVENANCE refused: override is not an absolute path (candidate=bin/grep)` |
| A5 missing override | `RESEARCH_GATE_GREP=<absent>` | **2** | `research-gate: GREP_PROVENANCE refused: override is not a regular file (candidate=…)` |
| A6 no grep on `PATH` at all (38-tool symlink farm) | default pin | **0** | `RESEARCH_GATE: CLEAN …` — the absolute default needs no `PATH` lookup |

Refusal strings and exit code 2 match the frozen claim text exactly
(`tools/research-gate.sh:357`, `:372-381`, `:393`).

---

## 2. F1 (crit, calibration) — the provenance check resolves `head` through `PATH`, and a `head` shim yields a **wrong verdict**

### Mechanism

`tools/research-gate.sh:358-367`:

```bash
grep_pin_verify() { # PATH -> rc0 when the binary reports GNU grep
  local cand=$1 v
  [[ -f $cand && -x $cand ]] || return 1
  v=$("$cand" --version 2>/dev/null | head -n 1 || true)     # <-- line 361
  GREP_PIN_VERSION=$v
  case "$v" in
    *"GNU grep"*) return 0 ;;
  esac
  return 1
}
```

The candidate binary is invoked by absolute path (good), but the **version banner is truncated
by `head`, which is resolved through `PATH`** (and is a *shell function* on this host — see
§2.3). The pin therefore verifies the candidate with an attacker-controlled helper: a `head`
that prints `grep (GNU grep) …` makes **any** binary — including a non-GNU one — pass the
`*"GNU grep"*` test at line 363.

This is the same class of defect C1 was written to remove (resolution through `PATH`), one
level up: the pin pins `grep` but leaves its *own verification* `PATH`-resolved.

### Reproduction 1 — non-GNU binary pinned, verdict flipped to `DRIFT` (`out3/`, `out4/`)

Stub `gnu-liar`: forwards to `/usr/bin/grep` but **drops `-z`** and self-reports
`grep (pi-uu-grep) 0.2.0` on stdout. `head` shim: prints
`grep (GNU grep) 3.12-modified` only when its input contains `pi-uu-grep`, otherwise execs the
real `/usr/bin/head` (surgical, so it changes *only* the version check).

`verify-claims` on a two-line span (`bravo\ncharlie` in `src/multi.md`):

```
E1 honest (real GNU grep)      rc=0
  CLAIM id=M1 expected=supported observed=supported source=src/multi.md at=lines:2-3 verdict=match
  VERDICT_BEARING_CLAIMS=1/1
  RESEARCH_GATE: CLEAN (claims=1 supported=1 contradicted=0 unsupported=0 mismatched=0 …)

E2 non-GNU override, NO head shim   rc=2
  ERR: research-gate: GREP_PROVENANCE refused: override does not report GNU grep: grep (pi-uu-grep) 0.2.0 (candidate=…/gnu-liar)

E3 non-GNU override WITH head shim   rc=1     <-- BYPASS
  CLAIM id=M1 expected=supported observed=unsupported source=src/multi.md at=- verdict=mismatch
  VERDICT_BEARING_CLAIMS=0/1
  RESEARCH_GATE: DRIFT (claims=1 supported=0 contradicted=0 unsupported=1 mismatched=1 …)
```

The honest run says **CLEAN**; the shimmed run says **DRIFT** and reports a *supported* claim
as **unsupported**. The gate's own capability probe
(`tools/research-gate.sh:1762`, `printf 'x' | grep -a -z -b -o -P -- 'x'`) does **not** catch
it, because the stub still honours `-b -o -P` and the probe's input has no NUL:

```
$ printf 'x' | …/gnu-liar -a -z -b -o -P -- 'x'
0:x
probe-rc=0
```

### Reproduction 2 — the **default** pin path is spoofable too (`out4/ns-default-headshim.*`)

With `/usr/bin/grep` bind-mounted over by a non-GNU binary inside a user+mount namespace
(`unshare --user --map-root-user --mount`), and the `head` shim on `PATH`:

```
  /usr/bin/grep --version -> grep (pi-uu-grep) 0.2.0
  --- DEFAULT pin, /usr/bin/grep is non-GNU, NO head shim ---
  rc=2
  research-gate: GREP_PROVENANCE refused: no GNU grep found at /usr/bin/grep, /bin/grep or on PATH (candidate=<none>)
  --- DEFAULT pin, /usr/bin/grep is non-GNU, WITH head shim (surgical) ---
  rc=1
  GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"
  RESEARCH_GATE: DRIFT (findings=2 drift=1 questions=1 sources=6 chains=7 claims=5 negatives=1 rejections=4 approvals=0)
```

So the gate can be made to **pin and use a non-GNU binary in the default path**, report it as
GNU in the echo line, and emit a **wrong verdict** — with **no refusal and no diagnostic**.

### Reproduction 3 — the same bypass via `BASH_ENV` (the counter's own S2 threat model)

```
$ env -i PATH=/usr/local/bin:/usr/bin:/bin BASH_ENV=<file defining head()> \
      RESEARCH_GATE_GREP=…/gnu-liar CHOUSA_GREP_PIN_ECHO=1 \
      bash tools/research-gate.sh verify-claims …/claims.jsonl --root …
GATE_GREP: path=…/gnu-liar source=override version="grep (GNU grep) 3.12-modified"
CLAIM id=M1 expected=supported observed=unsupported source=src/multi.md at=- verdict=mismatch
RESEARCH_GATE: DRIFT (claims=1 supported=0 …)
rc=1
```

A `BASH_ENV` that defines only `head()` — the exact mechanism C1's S2 scenario uses against
`grep` — is enough. `BASH_ENV` is inherited by non-interactive `bash`, which is how the gate
is invoked.

### 2.3 Why this is in the lane's own threat model

The gate's header comment (`tools/research-gate.sh:334-336`) records the motivating hazard on
*this* host: "this host's interactive shells carry a `pi-uu-grep 0.2.0` uutils grep as a
shell builtin/function" — i.e. a **uutils coreutils** replacement is in play in the caller's
environment. uutils ships `head` as well as `grep`, so a uutils-style `head` earlier on
`PATH` (or a `head()` function in the caller's shell, exported via `BASH_ENV` or
`export -f`) is the same class of hazard, applied to the one helper the pin's *verification*
depends on. Note that in *this* seat's session `type -a head` reports `head is a shell
builtin`, but that function is **not** exported (`export -p | grep BASH_FUNC_head` → empty;
a child `bash -c 'type -t head'` → `file`), so it does not reach a `bash tools/research-gate.sh`
child here. The reproduced bypass therefore uses the two vectors that *do* reach a child
`bash`: (i) a `head` binary earlier on `PATH`, and (ii) a `head()` function supplied via
`BASH_ENV` — the latter is exactly the mechanism C1's own S2 scenario uses against `grep`,
and it is inherited by every non-interactive `bash`, which is how the gate is invoked.

The threat model C1 adopts — "a PATH shim answers identically while running different code" —
applies verbatim to `head`.

### 2.4 Why P1 does not catch it

`corpus/evidence/round35/c1-count.py:115-121` builds its S6 non-GNU stub so the version
banner goes to **stderr**:

```sh
case "$1" in --version|-V) printf 'grep (pi-uu-grep) 0.2.0\n' >&2; exit 0;; esac
```

The gate reads the banner from **stdout** (`"$cand" --version 2>/dev/null | head -n 1`),
so S6's candidate yields an *empty* banner, not a `pi-uu-grep` banner. Verified by
regenerating the counter's own stub:

```
$ ./s6-stub-real --version 2>/dev/null     # stdout: (empty), rc=0
$ ./s6-stub-real --version 2>&1 1>/dev/null
grep (pi-uu-grep) 0.2.0                    # stderr only
```
And the counter's own receipt for S6 confirms the empty-banner path:
`"override does not report GNU grep: <no version>"` (`c1-880002.json`).

Consequences:
1. S6 proves the gate refuses a candidate with **no** banner. It never proves the gate
   refuses a candidate that **actively lies** with a non-GNU banner on stdout — which is
   exactly the case the `*"GNU grep"*` test at line 363 exists to catch, and exactly the case
   F1 defeats.
2. No counter scenario puts a `head` shim (binary or `BASH_ENV` function) on `PATH`; the
   counter only shims `grep` itself. So the counter's whole tripwire discipline is blind to
   the one helper the pin's *verification* depends on.
3. The counter's S1/S2 shims both `exec /usr/bin/grep` after logging, so they are
   *behaviour-preserving*; the counter never asks whether a **behaviour-altering** helper can
   change the gate's *verdict*.

### 2.5 Minimal repair sketch (not applied — read-only seat)

Resolve the truncation helper the same way the pin resolves `grep`: take the banner with a
pure-shell read that cannot be shimmed, e.g. `v=$("$cand" --version 2>/dev/null)` then strip
the first line with parameter expansion (`v=${v%%$'\n'*}`), and — better — verify by
**behaviour**, not by banner: probe the candidate for the exact capabilities the gate needs
(`-z`, `-P`, `-b -o`) before trusting it, so a lying banner cannot buy a pass. Adding a
counter scenario with a `head` shim (binary and `BASH_ENV` function) plus a stub that
reports its non-GNU banner on **stdout** closes the measurement gap.

---

## 3. F2 (warn, operability) — the pin's `PATH` fallback is dead code

`tools/research-gate.sh:384-393`:

```bash
    GREP_PIN_SOURCE=default
    for c in /usr/bin/grep /bin/grep; do
      if grep_pin_verify "$c"; then cand=$c; break; fi
    done
    if [[ -z $cand ]]; then
      c=$(command -v grep 2>/dev/null || true)     # line 388
      case "$c" in
        /*) if grep_pin_verify "$c"; then cand=$c; fi ;;   # line 390
      esac
    fi
    [[ -n $cand ]] || grep_pin_refuse "no GNU grep found at /usr/bin/grep, /bin/grep or on PATH" ''
```

The gate defines a shell function named `grep` at **line 351**
(`grep() { command "$GREP_BIN" "$@"; }`), and `grep_pin_init` is invoked at **line 8039** —
so by the time line 388 runs, `grep` is a **function**, and `command -v grep` reports the
*function*, not a path:

```
$ bash -c 'grep() { command "$GREP_BIN" "$@"; }; c=$(command -v grep 2>/dev/null || true);
           echo "command -v grep => [$c]"; case "$c" in /*) echo TAKEN;; *) echo "NOT TAKEN";; esac'
command -v grep => [grep]
  /* branch NOT TAKEN
```

`c` is the bare word `grep`, the `/*` case at line 390 never matches, and the `PATH` fallback
is **unreachable**. Note also `command -v` is not `type -P`; even without the shadowing
function `command -v` can return a relative or alias answer.

Observed consequence — a `PATH` that *does* hold a GNU grep is still refused
(`out4/ns-pathfallback.*`, `unshare --user --map-root-user --mount` with `/usr/bin/grep`
bind-mounted over by the non-GNU stub, and a real GNU grep first on `PATH` at
`/tmp/…/nsbin/grep`):

```
  GNU grep on PATH: grep (GNU grep) 3.12-modified
  LANDED gate, same PATH:
    landed rc=2
    research-gate: GREP_PROVENANCE refused: no GNU grep found at /usr/bin/grep, /bin/grep or on PATH (candidate=<none>)
```

**The base gate, same namespace, same `PATH`, succeeds:**

```
  BASE gate (round-34 blob), PATH has GNU grep:
    base rc=0
    RESEARCH_GATE: CLEAN (findings=0 drift=0 questions=1 sources=6 chains=7 claims=5 negatives=1 rejections=4 approvals=0)
```

So the landed gate is **strictly less operable** than the round-34 gate on any host where
GNU grep is not at `/usr/bin/grep` or `/bin/grep` — e.g. NixOS, a relocated prefix, a
distro that moved `grep`, or a container whose `PATH` is the only source of `grep`. The
refusal message at line 393 explicitly promises *"or on PATH"*, which the code cannot
deliver: it over-promises. `/bin` is a symlink to `usr/bin` on this host
(`ls -ld /bin` → `lrwxrwxrwx … /bin -> usr/bin`), so the two default candidates are the same
inode here anyway — the real fallback to `PATH` was the only escape hatch, and it is dead.

**Minimal repair sketch:** use `type -P grep` (not `command -v`) for the `PATH` fallback, or
drop the fallback and correct the refusal message to
`"no GNU grep found at /usr/bin/grep or /bin/grep"`. The round-35 claim text
(`corpus/evidence/round35/claims.md`, C1) says the gate "resolves, verifies and pins ONE
grep binary"; the *default* resolution as implemented is "the two hard-coded absolute paths",
not "one of those or one on `PATH`".

---

## 4. Re-derivation of C1 (P1) on this seat's own fresh seed

```
$ cd clone && C1_TMP=/tmp/hyaku/chousa-r35/w2/ExecPinModeVerify/c1tmp \
    python3 corpus/evidence/round35/c1-count.py --seed 880002 \
    --receipt …/c1-880002.json
GREP_PIN_MATCH=9/9
  S1-shim-first-path           PASS  {"output_matches_reference": true, "rc": 1, "tripwire_bytes": 0}
  S2-bash-env-function         PASS  {"output_matches_reference": true, "rc": 1, "tripwire_bytes": 0}
  S3-no-grep-on-path           PASS  {"output_matches_reference": true, "path_tools": 38, "rc": 1, "stderr_tail": ""}
  S4-override-relative        PASS  {"marker": true, "rc": 2, … "override is not an absolute path (candidate=bin/grep)"}
  S5-override-missing          PASS  {"marker": true, "rc": 2, … "override is not a regular file (candidate=…/absent-grep)"}
  S6-override-non-gnu          PASS  {"marker": true, "rc": 2, … "override does not report GNU grep: <no version> (candidate=…/stub-grep)", "stub_calls": 1}
  S7-override-real-echo        PASS  {"echo_line": "GATE_GREP: path=/usr/bin/grep source=override version=\"grep (GNU grep) 3.12-modified\""}
  S8-default-echo              PASS  {"echo_line": "GATE_GREP: path=/usr/bin/grep source=default version=\"grep (GNU grep) 3.12-modified\""}
  S9-override-beats-shim       PASS  {"echo_line": "GATE_GREP: path=/usr/bin/grep source=override version=\"grep (GNU grep) 3.12-modified\"", "tripwire_bytes": 0}
counter-rc=0
```
Receipt `c1-880002.json`: `label "GREP_PIN_MATCH=9/9"`, `predicate_holds True`,
`reference_sane True`, `gate_sha256 1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`,
`seed 880002`. **P1 holds as written.** The problem is not that P1 is false — it is that P1 is
**not sufficient**: it is satisfiable by a gate that still mis-verifies its pin (F1) and
refuses a usable host layout (F2).

---

## 5. Limits of this seat

* **Scope.** This seat attacked only the `verify` mode under the pin (C1). It did **not**
  score C2 / the mechanism-witness battery (`tools/mechanism-witness.py`,
  `corpus/evidence/round35/c2-count.py`); no C2 number is claimed or denied here.
* **F1 severity depends on the threat model.** If the pin's verification is *assumed* to run
  in a trusted environment where `head` is not under caller control, F1 is theoretical. The
  lane's own claim text refuses that assumption for `grep` (C1 exists precisely because a
  caller's `PATH`/functions must not decide the gate's behaviour) and records the same
  hazard for this host's shell builtins. Under the lane's own stated threat model F1 is a
  **real** bypass, and it is demonstrated to change the verdict.
* F1 and F2 were found by construction, not by an exhaustive search; other `PATH`-resolved
  helpers inside the gate (e.g. `head` at `tools/research-gate.sh:2017`, `:2176`) were not
  individually audited. [INFERENCE] the same class may recur for any helper the gate
  invokes by bare name.
* The `verify` mode's record resolution depends on `CHOUSA_ROOT`; the `research/` archives
  live at the workspace root, one level above the lane, so a lane-local run resolves the
  record's pointers only with `--root` pointing there (or at a copy). This is pre-existing
  behaviour, not round-35 fallout, but it is why the matrix uses a scratch root.
* No build, lint, selftest or formatter was run (editing wave in flight; parent owns the
  post-integration gate). No file outside
  `.ufo/waves/round-35/w2/ExecPinModeVerify/` and the scratch dir was written.

---

## 6. Reproduction index

Artifacts committed to this seat's own directory
`.ufo/waves/round-35/w2/ExecPinModeVerify/` (272 KB total; every file well under 1 MiB):

| file | contents |
|---|---|
| `run-matrix.sh` | the reported matrix (pinned clock, resolving root) → `out2/` |
| `run-verify-pin.sh` | first matrix (unpinned clock, `--root .`) |
| `run-attacks.sh` | A1/A2/A3/A4/A5/A6 provenance + refusal probes → `out3/` |
| `run-escalate.sh` | E1–E5 wrong-verdict escalation → `out4/` |
| `ns-mask3.sh`, `ns-compare.sh` | namespace probes (F2 dead fallback, F1 default-pin spoof, base-vs-landed) |
| `final-evidence.sh`, `evidence.txt` | consolidated quotes with line numbers |
| `c1-880002.json` | C1 receipt, seed 880002, gate sha pinned |
| `out2/`, `out3/`, `out4/` | raw stdout/stderr/exit-code of every run quoted above |
| `A-shokunin-tradition.md`, `B-multiagent-knowledge.md`, `C-rank-taxonomy.md` | read-only copies of the `research/deep-research-2026-09-28/` archive bytes, so the scratch root resolves the record's pointers |

Larger scratch (clone, shims, namespaces) stays in `/tmp/hyaku/chousa-r35/w2/ExecPinModeVerify/`
(241 MB) with `clone/` at revision `e87c5d7ea2dbf3730b36a3961de3f06261d015e4`.

Gate hashes re-derived by `sha256sum` at run time and recorded in §0.
