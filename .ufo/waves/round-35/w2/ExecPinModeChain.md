# ExecPinModeChain — `verify-chain` under the grep pin (round-35 w2, attack + re-derive)

Seat: leaf executor. Lane `chousa-shokunin`. Access date 2026-10-23. No production file
touched; artifacts only under `.ufo/waves/round-35/w2/ExecPinModeChain/` and
`/tmp/hyaku/chousa-r35/w2/ExecPinModeChain/`.

## 0. Gate pin (the only receipt gate that counts)

| gate | sha256 | where |
|---|---|---|
| **landed (assigned)** | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` | committed blob at `HEAD` (`git cat-file -p HEAD:tools/research-gate.sh`); extracted to `/tmp/hyaku/chousa-r35/w2/ExecPinModeChain/gate-LANDED-1f2fb4f5.sh`, sha re-verified |
| base (round-34) | `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` | `.ufo/waves/round-35/repairs/base-gate.sh`, re-verified |
| **worktree (drifted, NOT assigned)** | `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` | `tools/research-gate.sh` working tree, mtime `2026-10-23 17:07:40 -0300`, `git status` = ` M` |

**Gate drift observed mid-wave.** At my start `sha256sum tools/research-gate.sh` returned
`1f2fb4f5…` (matching the committed blob). A sibling seat rewrote the working tree at
17:07:40. Runs taken 17:00:47–17:06:33 hit `tools/research-gate.sh` while it still hashed
`1f2fb4f5…`; every run after the drift, and every run cited as a receipt, executed
`/tmp/hyaku/chousa-r35/w2/ExecPinModeChain/gate-LANDED-1f2fb4f5.sh` — the committed blob
extracted with `git cat-file`, sha re-verified before and after use. §6 reports the
uncommitted worktree separately and never mixes it in.

## 1. The committed chain fixture (path correction)

The round-3 chain fixture is **`corpus/fixtures/chain-r3.md`** (sha256
`06115f2f8e6db3c60034411dc6be42c4e0887352b09ab9cbd7f760801237ba07`, tracked) plus its
tampered control **`corpus/fixtures/chain-r3-broken.md`** (`b66222a16d4c5323ee6932839ff5746af5f716f36372af506755aed18e0f5c6a`).
Expected: `RESOLVED_HOPS=17/22` CLEAN rc 0, and `1/2` DRIFT rc 1.

**Correction to the assignment's premise.** The *selftest* does not use this fixture. It
builds its own records under `$WORK` (`tchain` cases at `tools/research-gate.sh:4827-4979`,
`5804`, `5845`, `6336`; `tchain()` runs `bash "$SELF" verify-chain "$WORK/$name.md"` at
`:4254`). The only occurrence of the string `corpus/fixtures/chain-r3.md` in the gate is
inside a `recheck:` heredoc at `tools/research-gate.sh:6530` — a text literal, never an
input. The fixture's real consumer is the **no-harm battery**,
`.ufo/waves/round-34/w1/ExecNoHarmBase34/battery.sh:189-197` (`bash "$GATE_ABS" verify-chain
corpus/fixtures/chain-r3.md --root "$FLEET"`), same in round 33
(`.ufo/waves/round-33/w1/ExecNoHarmBase33/battery.sh:175-183`). I did exercise the battery's
two chain rows anyway (§5).

## 2. Four environments + a refused override — landed blob `1f2fb4f5`

Command shape for every row (from lane cwd, `env -i`, bounded):
`env -i PATH=<path> HOME=… [BASH_ENV=…|RESEARCH_GATE_GREP=…] timeout 900 bash <gate> verify-chain corpus/fixtures/chain-r3.md --root ..`

| # | environment | rc | `RESOLVED_HOPS` | verdict line | tripwire |
|---|---|---:|---|---|---|
| E1 | clean `PATH=/usr/local/bin:/usr/bin:/bin` | **0** | `17/22` | `CLEAN (hops=22 verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0 resolvable=0)` | n/a |
| E2 | shim-first PATH (`grep` script logs `$*`, then `exec /usr/bin/grep`) | **0** | `17/22` | same CLEAN | **0 bytes** |
| E3 | `BASH_ENV` defines `grep()` that logs (S2 shape) | **0** | `17/22` | same CLEAN | **0 bytes** |
| E4 | grep absent from PATH (38-tool symlink farm, no `grep`) | **0** | `17/22` | same CLEAN | n/a |
| R1 | `RESEARCH_GATE_GREP=bin/grep` (relative) | **2** | — (no record read) | — | — |

R1 refusal text (verbatim, `receipts/P5-refuse.err`):

```
research-gate: GREP_PROVENANCE refused: override is not an absolute path (candidate=bin/grep)
```

Additional refusal surfaces, same mode, same blob — all rc 2 before any record is read:

| # | override | rc | verbatim refusal |
|---|---|---:|---|
| R2 | non-GNU stub (`--version` → `pi-uu-grep 0.2.0`) | 2 | `research-gate: GREP_PROVENANCE refused: override does not report GNU grep: <no version> (candidate=…/stub-grep)` |
| R3 | non-GNU stub that logs every exec | 2 | same; stub exec log contains **only** `STUBEXEC[--version]` — the refused binary is never used for a match |
| R4 | `/tmp` (directory) | 2 | `… override is not a regular file (candidate=/tmp)` |
| R5 | mode 0644 file | 2 | `… override is not executable (candidate=…/notexec)` |
| R6 | non-existent path | 2 | `… override is not a regular file (candidate=…/absent-grep)` |

**Base-gate contrast (the C1 "before")**, same four environments:

| env | base rc | `RESOLVED_HOPS` | tripwire |
|---|---:|---|---|
| clean | 0 | `17/22` | — |
| shim-first PATH | 0 | `17/22` | **5737 bytes / 16 lines** |
| `BASH_ENV` `grep()` | 0 | `17/22` | **5785 bytes / 16 lines** |
| no grep on PATH | **2** | — | `research-gate: GNU grep with -z/-P support is required for claims and chain token matching` |

So the chain surface reproduced the C1 defect exactly (interception invisible to output,
PATH dependency fatal) and the pin removes both.

## 3. Wrapper stamp — does the chain matcher use the same pinned binary?

`RESEARCH_GATE_GREP=<wrapper>` where the wrapper logs `$*` then `exec /usr/bin/grep "$@"`
(so its `--version` still reports GNU grep and it passes provenance).
`CHOUSA_GREP_PIN_ECHO=1`.

Chain fixture (`receipts/chain-argv-W1.log`, 17 invocations):

```
ARGV[--version]                                  <- grep_pin_verify
ARGV[-a -z -b -o -P -- x]                        <- token_matcher_require capability probe
ARGV[-a -z -b -o -P -- \x49\x20\x63\x6f\x75…]    <- 15 × tok_span_offsets_direct (quote anchors)
```

- **`-a -z -b -o -P` appears: 16 of 16 matcher invocations.** 1 `--version`, 16 matcher, 0 other.
- Reconciliation is exact: `chain-r3.md` holds 22 hops — 15 `quote`, 5 `line`, 2
  `blocked-no-fetch` (no anchor). Quote anchors route through `chain_anchor_at` →
  `tok_span_at` → `tok_span_offsets` → `tok_span_offsets_direct` → `grep -a -z -b -o -P --`
  (`tools/research-gate.sh:2152`, `:1687`). 15 quote hops + 1 capability probe = 16. `line`
  anchors are pure-bash and never touch grep (confirmed: no extra invocations).
- Pin echo line (verbatim, stderr): `GATE_GREP: path=…/grep-wrapper.sh source=override version="grep (GNU grep) 3.12-modified"`.

Broken fixture (`receipts/chain-argv-W2-broken.log`, 5 invocations): 1 `--version`,
3 × `-a -z -b -o -P` (probe + hop 1 + hop 2), and **1 × `ARGV[-Fn -m1 -e jin’i-ryū]`** —
the `chain_nearest` context probe (`tools/research-gate.sh:2176`). That call site is a
different flag shape but **also** routes through the pin, so the pin covers the whole grep
surface of chain mode, not only the matcher.

Every grep call site in the gate reaches the pinned binary because line 351 defines a shell
function `grep()` in the gate's own shell; there is no `command grep`, no absolute
`/usr/bin/grep`, and no `xargs grep` in the gate body (only the pin block itself names
`/usr/bin/grep`).

## 4. FINDINGS — attacks that hold against the landed blob `1f2fb4f5`

### F1 (operability, real) — the `command -v grep` fallback is dead code

`grep_pin_init` default branch, `tools/research-gate.sh:386-393` (blob `1f2fb4f5`):

```bash
c=$(command -v grep 2>/dev/null || true)
case "$c" in
  /*) if grep_pin_verify "$c"; then cand=$c; fi ;;
esac
[[ -n $cand ]] || grep_pin_refuse "no GNU grep found at /usr/bin/grep, /bin/grep or on PATH" ''
```

The gate defines `grep()` as a shell *function* at line 351, and `grep_pin_init` runs at line
8039 — after it. `command -v grep` therefore prints the **function name**, not a path:

```
$ bash deadproof.sh
command -v grep => [grep]
case /* does NOT match -> fallback is DEAD
```

(`receipts/deadproof.sh`; `type -P grep` gives `/usr/bin/grep`, `command -v grep` gives
`grep`.) Consequence measured in a mount namespace with `/usr/bin/grep` and `/bin/grep`
replaced by a non-GNU stub and a real GNU grep on PATH at a non-standard location:

| gate | rc | result |
|---|---:|---|
| landed `1f2fb4f5` | **2** | `research-gate: GREP_PROVENANCE refused: no GNU grep found at /usr/bin/grep, /bin/grep or on PATH (candidate=<none>)` |
| base `a6307edf` | **0** | `RESOLVED_HOPS=17/22`, CLEAN |

So the refusal text advertises a PATH fallback that can never fire, and on a host whose GNU
grep is not at `/usr/bin/grep` or `/bin/grep` the landed gate refuses where the base gate
ran. Fail-closed (not a soundness break), but an operability regression and a false message.
Reproduce: `out/B1-deadfallback.out` / `.err` (bwrap: `--bind $S/fakebin/nongnu /usr/bin/grep
--bind $S/fakebin/nongnu /bin/grep --bind $S/gnubin $S/gnubin --setenv PATH $S/gnubin:…`).

### F2 (soundness) — a forged `head` defeats the provenance check, and the gate then runs the wrong engine

`grep_pin_verify` (`:361`, blob `1f2fb4f5`) cuts the version line with `head -n 1`:

```bash
v=$("$cand" --version 2>/dev/null | head -n 1 || true)
```

`head` is shadowable by a `BASH_ENV` function in the same shell. With
`BASH_ENV=<env-head-forge.sh>` (`head() { printf 'grep (GNU grep) 9.99-forged\n'; }`) and
`RESEARCH_GATE_GREP=<stub-logging>` (a non-GNU stub: answers `--version` on stderr, `exit 1`
for everything else):

```
rc=1
RESOLVED_HOPS=4/22        <- truth is 17/22
stderr: (empty — NO GREP_PROVENANCE refusal)
```

Full verdict line (`receipts/B4-headforge-e0.out`):

```
RESOLVED_HOPS=4/22
RESEARCH_GATE: DRIFT (hops=22 verified=4 exempt=5 anchor-missing=13 refused=0 invalid=0 findings=13 drift=13 resolvable=0)
```

The stub-exec log (`receipts/stub-exec-headforge.log`) shows the **entire** chain matcher
ran on the stub — 17 calls served: 1 `--version` + **16 × `-a -z -b -o -P`**, exactly the
matcher surface of §3. `4/22` is exactly the four `line`-kind hops (pure bash); all 13
quote-resolved hops flipped to `anchor-missing`. **Control:** the same stub *without* the
forged `head` is refused — rc 2, `GREP_PROVENANCE refused: override does not report GNU
grep: <no version>` (`receipts/B5-nohead.err`). So the forgery, not the stub, is what
disables the check.

This breaks C1's own contract ("refuses a pin it cannot verify with a named exit-2 refusal")
from inside the C1 threat model — `claims.md` declares BASH_ENV-function shims in scope
(scenario S2), and its stated limit only excuses a *binary that lies about its own version*,
not a forged verification **pipeline**. A stub that answers the capability probe with
`exit 0` (as a hostile engine would) is enough; a stub that honestly fails the probe is
still caught by `token_matcher_require` (`out/B3-headforge-landed.*`, rc 2), so the residual
defence is the probe, not the pin.

### F3 (soundness) — a `command` shadow receives every pinned call

The wrapper is `grep() { command "$GREP_BIN" "$@"; }` (`:351`, blob `1f2fb4f5`). `command`
is a bash builtin and **is** shadowable by a function. With
`BASH_ENV=<env-command-swap2.sh>` (`command() { log "$*"; local b=$1; shift; "$b" "$@"; }`):

```
rc=0   RESOLVED_HOPS=17/22   intercepted = 16
receipts/cmdswap-landed.log: CMDSWAP[/usr/bin/grep -a -z -b -o -P -- x]  (+15 more)
```

16 interceptions = the complete matcher surface of chain mode. My shadow forwarded to
`/usr/bin/grep`, so the output is correct — that is the point: the interception is
**invisible to output**, and a shadow that ran a different engine would return whatever it
liked while `token_matcher_require` (which also routes through `grep()` → `command`) reports
success. The same works with no `BASH_ENV` file at all, via an imported exported function:

```
$ env -i … 'BASH_FUNC_command%%=() { … }' bash gate-LANDED-1f2fb4f5.sh verify-chain …
rc=0  RESOLVED_HOPS=17/22  intercepted: 16
```

(`out/D-exportedfn.*`.) So C1's pin claim holds only against environments that shadow
`grep` but not `command`/`head`.

### F4 (calibration) — C1's 9/9 is blind to F2 and F3

I ran the committed counter against the landed blob:

```
$ C1_TMP=… python3 corpus/evidence/round35/c1-count.py \
    --gate /tmp/…/gate-LANDED-1f2fb4f5.sh --seed 3599 --receipt c1-3599.json
GREP_PIN_MATCH=9/9          (S1…S9 all PASS)
receipt: gate_sha256=1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617,
         matched=9, total=9, predicate_holds=true, reference_sane=true
```

`receipts/c1-3599.json`. Note S2's detail: `"tripwire_bytes": 0` — it defines only a
`grep()` shim. `head` and `command` are never shadowed by the counter, and the counter never
runs `verify-chain` at all (`c1-count.py:93` is the sole invocation: `verify-claims`). So the
frozen predicate P1 is satisfied on the same gate where F2 produces a wrong verdict and F3
captures the whole matcher — the 9/9 does not cover the surface the claim names.

## 5. No-harm on the assigned surface

Battery chain rows, landed vs base, `--root "$FLEET"`:

| row | landed | base |
|---|---|---|
| `chain-r3.md` | rc 0, `RESOLVED_HOPS=17/22`, CLEAN (hops=22 verified=17 exempt=5 …) | identical |
| `chain-r3-broken.md` | rc 1, `RESOLVED_HOPS=1/2`, `DRIFT … anchor-missing=1 … findings=1 drift=1` | identical |

`diff` of stdout vs base: **the only differing line is the `ts=` banner** — chain-mode
verdicts are byte-identical to round 34. Both battery assertions
(`'RESOLVED_HOPS=17/22'`, `'RESEARCH_GATE: CLEAN (hops=22 verified=17 exempt=5'`) hold.

## 6. The uncommitted worktree (`a4768851`) — a sibling's fix, measured, not assigned

The working tree rewrote the pin block after my runs (32+/11-, `git diff --stat`). Measured
against `gate-WORKTREE-a4768851.sh`:

| check | landed `1f2fb4f5` | worktree `a4768851` |
|---|---|---|
| four environments (clean / shim / BASH_ENV fn / no-grep PATH) | rc 0, `17/22`, trip 0,0 | rc 0, `17/22`, trip 0,0 (`out/Q1-Q4`) |
| F1 dead PATH fallback | dead, refuses a PATH-only GNU grep | fallback **removed** (`grep_pin_init` now says "No PATH consultation at all"); message changed to `no GNU grep at /usr/bin/grep or /bin/grep (set RESEARCH_GATE_GREP to an absolute path)` |
| F2 forged `head` | **no refusal, `4/22`** | rc **2**, `GREP_PROVENANCE refused: override does not report GNU grep: <no version>` (`receipts/B2-headforge-worktree.err`); replaced `head -n 1` with bash expansion + absolute `timeout` |
| F3 `command` shadow | 16 interceptions | **0 interceptions** (`out/A4`); wrapper now calls `"$GREP_BIN"` directly via `eval`, plus a `readonly -f grep` refusal |

The worktree therefore fixes all three findings. It is uncommitted and carries no receipt of
its own here; I did not score it as the claim's gate, and I did not edit it.

## 7. Limits

- F2/F3 need the caller to control `BASH_ENV` or the exported-function environment of the
  gate process. That is exactly the S2 threat model C1 declares, not an extra one.
- I did not test the counter's `S9`/`S6` against shadowed `command`, and I did not attempt
  to make a shadow *return wrong offsets* (I only proved interception and provenance
  forgery); a shadow that lies would be caught by nothing in the C1 counter.
- One `verify-chain` selftest gap is inferred, not measured: the gate's `tchain` cases build
  their own records and never exercise `corpus/fixtures/chain-r3.md`, so the fixture's
  `17/22` is only asserted by the battery. [INFERENCE from `grep -n` of the whole gate.]
- No installs, no network, no writes outside my wave dir and `/tmp/hyaku/chousa-r35/w2`.
  No git/jj write. All commands bounded with `timeout`; every gate scored by sha256.

## 8. Verdict on my item

The pin **does** hold on the chain surface for the four environments asked for: exit codes,
`RESOLVED_HOPS=` lines and tripwires are exactly as the claim requires, the refused override
exits 2 with the named `GREP_PROVENANCE refused:` text before any record is read, and the
chain matcher demonstrably runs the pinned absolute binary with `-a -z -b -o -P` (16/16
matcher invocations, plus the `-Fn -m1` nearest probe). No C1-MEETS inversion was found for
the ordinary environments. **But** two attacks that stay inside C1's declared BASH_ENV
threat model defeat the pin on the assigned blob (`command` shadow captures every call;
forged `head` passes provenance and makes the gate report `4/22` instead of refusing), and
the committed 9/9 counter is blind to both because S2 only shadows `grep` and never runs
`verify-chain`. That is the wave's most useful result: C1's 9/9 measures the right thing for
shim and PATH environments and **under-covers the verification pipeline it relies on**.
