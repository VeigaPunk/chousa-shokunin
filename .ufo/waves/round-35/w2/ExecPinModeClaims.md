# ExecPinModeClaims — `verify-claims` under the grep pin (round-35 wave 2)

Seat: `ExecPinModeClaims` (executor). Lane: `chousa` (deep-research method).
Judged on: operability, calibration. Access date for every quoted source: **2026-10-23**.

**Verdict in one line.** The assigned target — `verify-claims` on
`corpus/fixtures/claims-r2.jsonl` under the pin, in four environments, plus the
relative-override refusal and the echo-flag stdout diff — **passes on the pinned
gate `1f2fb4f5…`** (all four environments exit 0, stdout byte-identical, both
tripwires empty, relative override refused with exit 2). **But the same pinned
gate carries three provenance holes that the four-environment matrix does not
exercise and the frozen C1 counter does not detect** (a shadowed `command`
receives all 18 pinned matcher calls; a forged `head` defeats the GNU-grep
verification; the `command -v grep` PATH-fallback arm is dead code). All three
are already fixed in the lane's current tip `a4768851…` (commit `beb04ea`,
17:06:22), which I re-measured as resistant.

---

## 0. Gate drift observed mid-wave — what I measured against

The card pins the gate at `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`
(wave base `e87c5d7ea2dbf3730b36a3961de3f06261d015e4`). **The lane working tree
moved during my wave.** Timeline from `git log --format='%H %ad %s' --date=iso -6`
in `/home/vgpnk/Projects/shokunin/chousa-shokunin`:

| commit | time | gate sha256 | note |
|---|---|---|---|
| `e87c5d7` | 16:51:03 | `1f2fb4f5…` | **the wave base my card pins** |
| `2b2e017` | 16:57:29 | `1f2fb4f5…` | w2 wave evidence |
| `beb04ea` | 17:06:22 | `a4768851…` | "pin hardened (command/head/PATH-fallback/readonly/bounded probe)" |
| `770a69d` | 17:12:20 | `a4768851…` | erratum 7 (tripwire-path forgery) |

`git merge-base --is-ancestor e87c5d7 beb04ea` → **YES** (the hardening is a
descendant of my base).

**Every receipt in §1–§3 is a run against the byte-exact committed blob**, not
the working tree. Extraction and re-verification:

```
git cat-file blob e87c5d7ea2dbf3730b36a3961de3f06261d015e4:tools/research-gate.sh \
  > /tmp/hyaku/chousa-r35/w2/ExecPinModeClaims/gate-LANDED-1f2fb4f5.sh
sha256sum /tmp/hyaku/chousa-r35/w2/ExecPinModeClaims/gate-LANDED-1f2fb4f5.sh
# 1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617
```

The working-tree gate `tools/research-gate.sh` now hashes
`a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`
(`sha256sum tools/research-gate.sh`, run 17:14). §5 reports the two gates
side by side and never mixes a run of one into a receipt of the other.

Scratch tree (all artifacts under `/tmp/hyaku/chousa-r35/w2/ExecPinModeClaims/`,
113 GiB free on `/tmp`; nothing written to `/fast`):

```
/tmp/hyaku/chousa-r35/w2/ExecPinModeClaims/root/chousa-shokunin/   # clone at e87c5d7
/tmp/hyaku/chousa-r35/w2/ExecPinModeClaims/root/research/deep-research-2026-09-28/
```

The three cited sources were copied byte-exact (sha256 re-derived, matching the
fixture README's pins):
`A-shokunin-tradition.md` `9033857d…`, `B-multiagent-knowledge.md` `6d8dbddd…`,
`C-rank-taxonomy.md` `e48fe70f…`.

**Fixture resolution.** `corpus/fixtures/claims-r2.jsonl` cites sources as
`research/deep-research-2026-09-28/…`, fleet-root-relative, so `--root ..`
from the lane cwd is required. I used `--root ..` throughout; the lane's own
`research/` tree is at `/home/vgpnk/Projects/shokunin/research/`, one level
above the lane, which is exactly what `--root ..` from
`/home/vgpnk/Projects/shokunin/chousa-shokunin` resolves. I additionally ran
the whole matrix against the **real lane tree** (§2.3) — same bytes, same
stdout sha256.

---

## 1. The assigned target: four environments on `claims-r2.jsonl`

Command shape (all runs `cwd=$LANE`, `env -i` for a hermetic environment,
`CHOUSA_NOW_EPOCH=1750000000` to freeze the volatile `ts=` line):

```bash
env -i HOME=$HOME PATH=<PATH> CHOUSA_NOW_EPOCH=1750000000 \
  bash gate-LANDED-1f2fb4f5.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..
```

`PATH` values: clean `/usr/local/bin:/usr/bin:/bin`; shim
`$R/shimbin:/usr/local/bin:/usr/bin:/bin` where `shimbin/grep` is a logging
wrapper around `/usr/bin/grep`; `BASH_ENV` fixture defines a logging `grep()`
function.

### 1.1 Results (pinned gate `1f2fb4f5…`)

| env | PATH / extra | exit | stdout sha256 (first 16) | tripwire |
|---|---|---|---|---|
| **A** clean | `/usr/local/bin:/usr/bin:/bin` | **0** | `c45bba7687d9c902` | — |
| **B** PATH shim | `shimbin:` first | **0** | `c45bba7687d9c902` | **0 bytes** |
| **C** override + shim | `RESEARCH_GATE_GREP=/usr/bin/grep` | **0** | `c45bba7687d9c902` | **0 bytes** |
| **D** echo flag | `CHOUSA_GREP_PIN_ECHO=1` | **0** | `c45bba7687d9c902` | — |
| **E** relative override | `RESEARCH_GATE_GREP=bin/grep` | **2** | **0 bytes** | — |

Receipts: `.ufo/waves/round-35/w2/ExecPinModeClaims/receipts/G_{A,B,C,D}.stdout`,
`G_D-echo.stderr`, `G_E-relative.stderr`.

Verdict line, identical in A/B/C/D (`G_A-clean.stdout`):

```
VERDICT_BEARING_CLAIMS=17/17
RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
```

All 17 `CLAIM id=… verdict=match` lines present, `at=` line numbers 52, 80, 81,
88, 64, –, 47, 64, 79, 69, –, 89, 92, 97, 102, 130, 53 — agreeing with the
fixture README's provenance table (`corpus/fixtures/claims-r2.README.md`,
"Provenance — what each entry exercises").

### 1.2 The relative-override refusal (env E)

Exit code **2**. stderr, verbatim (`receipts/G_E-relative.stderr`, sha256
`cd2c921b…`):

```
research-gate: GREP_PROVENANCE refused: override is not an absolute path (candidate=bin/grep)
```

stdout is **0 bytes** — the refusal happens before any record is read, so no
`CLAIM` line and no `VERDICT_BEARING_CLAIMS` line is emitted. This is the
contract at `tools/research-gate.sh:371-380` (`grep_pin_init`, override arm)
reached through the call site at `tools/research-gate.sh:8038`
(`grep_pin_init` invoked after argument parsing, before the mode dispatch).

### 1.3 The echo flag: stdout diff (the required comparison)

`CHOUSA_GREP_PIN_ECHO=1` writes **one line to stderr** (`research-gate.sh:397`,
`>&2`):

```
GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"
```

`diff` of stdout D against stdout A: **empty** — identical, sha256
`c45bba7687d9c90233b3e7ee5dc4b30da720e331ddae86fd10b361bc8e08f7a6` for A, B, C
and D alike.

**Caveat that a naive diff would trip over (and that I had to control for).**
The stdout header carries a wall-clock `ts=` field
(`research-gate v2 — ts=2026-10-23T20:01:36Z — mode=claims — claims=…`,
line 1). Two runs a second apart therefore differ on **that line only**:

```
$ diff W1.stdout W2.stdout
1c1
< research-gate v2 — ts=2026-10-23T20:15:56Z — mode=claims — claims=corpus/fixtures/claims-r2.jsonl
---
> research-gate v2 — ts=2026-10-23T20:15:58Z — mode=claims — claims=corpus/fixtures/claims-r2.jsonl
(diff lines: 2)
```

I pinned `CHOUSA_NOW_EPOCH=1750000000` for every run in §1.1 so the required
"diff stdout must be identical" comparison is meaningful. The `ts=` field is a
declared volatile token of the gate's own baseline contract (`--pin` header
declares `ts` and `gate_sha256` volatile) — so this is expected, but any
receipt that claims byte-identity must state the epoch it froze.

### 1.4 The pin is actually load-bearing on this mode

Same fixture, base round-34 gate `.ufo/waves/round-35/repairs/base-gate.sh`
(sha256 `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`,
matching the card) vs the landed gate, both with the PATH shim first:

| gate | exit | stdout | shim tripwire |
|---|---|---|---|
| base `a6307edf…` | 0 | **identical to landed** | **8259 bytes / 18 lines** |
| landed `1f2fb4f5…` | 0 | identical to landed | **0 bytes** |

Receipts: `receipts/base-gate-shim-trip.log` (sha256 `e4692963…`),
`receipts/landed-gate-shim-trip.log` (0 bytes).

This re-derives the round-34 closure's central observation **at the
`verify-claims` mode level**: the base gate's output cannot tell which grep it
ran — 18 matcher calls went through the PATH shim and the output was
byte-for-byte the same. The landed gate's output is now provably produced by
the pinned binary.

Direct evidence that the pinned binary is the one serving every matcher call
(`RESEARCH_GATE_GREP` pointed at an absolute logging wrapper around
`/usr/bin/grep`, receipt `receipts/pinned-calls-claims-r2.log`,
sha256 `9a37156c…`): **19 calls, all through the pinned binary** —

```
   1  --version                              (the provenance probe)
  18  -a -z -b -o -P -- <hex pattern>         (one per claim, 17 + the
                                                token_matcher_require probe)
```

No call escaped to PATH. The `-a -z -b -o -P` shape is
`tok_span_offsets_direct` (`research-gate.sh:1687`) and
`tok_span_offsets_chunk` (`research-gate.sh:1716`); the `--version` probe is
`grep_pin_verify` (`research-gate.sh:360`).

### 1.5 Coverage note — what this fixture does *not* exercise

`claims-r2.jsonl`'s longest span is **175 bytes** (`python3` over the fixture),
well under `TOK_DIRECT_SPAN_MAX=32764` (`research-gate.sh:1650`), so this
fixture never reaches the **chunk** matcher. I exercised it separately with a
53 999-byte span under the same logging pin: the chunk matcher fires with the
chunk pattern shape (`-a -z -b -o -P -- \x77(?=\x30\x30\x30\x30\x20\x77\…`)
and reports `VERDICT_BEARING_CLAIMS=1/1`, `RESEARCH_GATE: CLEAN`. The
near-miss diagnostic `grep -Fn -m1` path (`research-gate.sh:2017`, `:2176`) is
likewise unreachable on `claims-r2` (all 17 spans resolve), and I exercised it
with a deliberately absent span — it fires and is pinned too.

**Calibration consequence:** the `verify-claims` mode's *output* on
`claims-r2.jsonl` cannot by itself distinguish the direct matcher from the
chunk matcher, nor the near-miss path from silence. Only the tripwire/pinned-call
log can. A receipt that scores "17/17, CLEAN" on this fixture says nothing
about which matcher ran.

---

## 2. The four environments, run twice (pinned blob vs real lane tree)

### 2.1 Pinned blob `1f2fb4f5…` — §1.1 above.

### 2.2 Real lane tree, `--root ..` from the lane cwd

Run at 17:14 against the then-current working-tree gate `a4768851…` (§5's
"head" gate). Same four environments plus the refusal:

```
REAL A exit=0 trippath=0
REAL B(shim) exit=0 trippath=0
REAL C(override+shim) exit=0 trippath=0
REAL D(echo) exit=0
GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"
REAL E(relative) exit=2 stdout_bytes=0
research-gate: GREP_PROVENANCE refused: override is not an absolute path (candidate=bin/grep)
--- stdout identity ---
B IDENTICAL
C IDENTICAL
D IDENTICAL
sha256: c45bba7687d9c902… (all four)
```

### 2.3 Cross-check: the two gates agree byte-for-byte on this fixture

```
BASE(1f2fb4f5) stdout == HEAD(a4768851) stdout on claims-r2
```

Both produce sha256 `c45bba7687d9c902…`. The hardening in `beb04ea` changed
**no** `verify-claims` output on this fixture — it changed only the refusal
and pin-resolution behaviour. That is a useful negative result: the hardening
is output-preserving on the committed fixture.

---

## 3. Attacking the pinned gate `1f2fb4f5…` — three provenance holes

These are the results I consider the most valuable part of this wave. Each is
a scenario the four-environment matrix above does **not** reach, and the frozen
C1 counter does **not** score (measured in §4).

### F1 (soundness) — a shadowed `command` receives every pinned matcher call

The landed gate's wrapper is `grep() { command "$GREP_BIN" "$@"; }`
(`research-gate.sh:351`). `command` is a **shell builtin**, and a `BASH_ENV`
file can define a shell **function** named `command` that shadows it.

Attack (`receipts/bash_env_cmd.sh`):

```sh
command() { printf 'SWAP %s\n' "$*" >>"$TRIP" 2>/dev/null; builtin command "$@"; }
```

Run against the pinned blob:

```
CMD-SWAP exit=0 trip-cmd bytes=8601 lines=18
SWAP /usr/bin/grep -a -z -b -o -P -- x
SWAP /usr/bin/grep -a -z -b -o -P -- \x54\x68\x65\x20\x73\x74\x72\x6f\x6e\x67\x65…
```

**18 of 18 matcher calls passed through the attacker's function** — the same
18 the PATH shim intercepted on the base gate. The gate's stdout was
**byte-identical** to the clean run (the attack was made to delegate to the
real grep). Receipt: `receipts/cmd-swap-trip.log`, sha256 `f2ec187c…`.

Making the shadowed `command` **fabricate** the match output
(`receipts/bash_env_forge.sh` — answers `0:the fabricated match` instead of
running grep) turns the same run into a wrong verdict with **no refusal and no
diagnostic**:

```
research-gate: GREP_PROVENANCE …            <- absent; no refusal at all
CLAIM id=A01 expected=supported observed=unsupported … verdict=mismatch
…
VERDICT_BEARING_CLAIMS=2/17
RESEARCH_GATE: DRIFT (claims=17 supported=0 contradicted=0 unsupported=17 mismatched=15 …)
exit=1
```

Receipt: `receipts/FORGE_BASE.stdout` (sha256 `f7571fbd…`),
`receipts/FORGE_BASE.stderr` (0 bytes — **the gate said nothing**).

So on the pinned gate the "one pinned binary" property is **not** a property of
the binary at all: a caller who controls `BASH_ENV` controls the matcher.

### F2 (soundness) — a forged `head` defeats the GNU-grep verification

`grep_pin_verify` at `research-gate.sh:360` cuts the version line with
`head -n 1`:

```bash
v=$("$cand" --version 2>/dev/null | head -n 1 || true)
```

`head` is a **PATH-resolved external**, so a `BASH_ENV` `head()` function
rewrites the line the gate reads for verification.

Attack (`receipts/bash_env_head.sh`): `head() { printf 'grep (GNU grep) 9.9-forged\n'; }`

Against the pinned blob with `RESEARCH_GATE_GREP` pointing at a **non-GNU**
stub:

```
GATE_GREP: path=/tmp/…/attacks/stub-nongnu source=override version="grep (GNU grep) 9.9-forged"
VERDICT_BEARING_CLAIMS=2/17
```

**The stub was pinned** — the gate's own receipt line reports it as GNU grep
3.12-with-forged-version, and the run proceeded on the stub's output. Without
the forgery the same override is correctly refused
(`override does not report GNU grep: <no version>`, exit 2, §4 S6).

This is receipt-evidence forgery: the `GATE_GREP:` line a downstream auditor
would archive says the pin was verified, and it was not.

### F3 (calibration) — the `command -v grep` PATH-fallback arm is dead code

`grep_pin_init`'s default arm (`research-gate.sh:387-391`):

```bash
if [[ -z $cand ]]; then
  c=$(command -v grep 2>/dev/null || true)
  case "$c" in
    /*) if grep_pin_verify "$c"; then cand=$c; fi ;;
  esac
fi
```

Because the gate has already defined `grep()` as a function
(`research-gate.sh:351`), `command -v grep` returns the **function name**, not
a path:

```
$ bash -c 'GREP_BIN=/usr/bin/grep; grep() { command "$GREP_BIN" "$@"; }; c=$(command -v grep); echo "c=[$c]"'
c=[grep]
ABS-BRANCH-DEAD (c is not absolute)
$ bash -c 'c=$(command -v grep); echo "c=[$c]"'      # no function
c=[/usr/bin/grep]
ABS-BRANCH-TAKEN
```

The `/*)` case therefore never matches and the arm can never fire. Proven
end-to-end in a mount namespace with a **real GNU grep first on PATH** and a
non-GNU stub standing in for `/usr/bin/grep`:

```
--- /usr/bin/grep now: grep (pi-uu-grep) 0.2.0
--- GNU grep available at …/goodbin/grep: grep (GNU grep) 3.12-modified
research-gate: GREP_PROVENANCE refused: no GNU grep found at /usr/bin/grep, /bin/grep or on PATH (candidate=<none>)
GATE exit=2
```

The gate refuses even though a verified GNU grep is the first thing on PATH.
The refusal text promises a PATH fallback that does not exist. Operationally
this is fail-closed (refusal, not a wrong answer), so it is a **narrowing of
operability**, not a soundness hole — but it is a real defect in the shipped
message and in the code path.

### F4 (operability, minor) — a `readonly` grep wrapper dies with a bare rc

`BASH_ENV` containing `grep() { …; }; readonly -f grep` makes the wrapper
definition at `research-gate.sh:351` fail. On the pinned blob:

```
BASE readonly exit=1
…/tools/research-gate.sh: line 351: grep: readonly function
```

Exit **1**, no named refusal, no `GREP_PROVENANCE` marker — an untyped setup
failure on a path the contract says must refuse with a named exit-2.

---

## 4. Calibration: does the frozen C1 counter see any of this?

The frozen counter is `corpus/evidence/round35/c1-count.py` (P1 predicate:
`GREP_PIN_MATCH=9/9`, `predicate_holds=true`). I ran it against **both** gates
on seed 3501, and against both gates under a forged-`head` `BASH_ENV`
(`C1_TMP` set to my scratch dir; the counter writes only its own temp dir).

| counter run | base `1f2fb4f5…` | head `a4768851…` |
|---|---|---|
| clean environment | **`GREP_PIN_MATCH=9/9`** | **`GREP_PIN_MATCH=9/9`** |
| under forged-`head` `BASH_ENV` | **`GREP_PIN_MATCH=6/9`** | **`GREP_PIN_MATCH=7/9`** |

Receipts: `receipts/c1-basegate-s3501.json` (sha256 `74ca8e18…`),
`receipts/c1-newgate-s3501.json` (`73634551…`),
`receipts/c1-base-forgehead-s3501.json` (`f9b39750…`),
`receipts/c1-new-forgehead-s3501.json` (`75876c3d…`).

**Two calibration results.**

1. **The counter cannot discriminate the two gates in a clean environment.**
   Both score 9/9. Its nine scenarios (S1 PATH shim, S2 BASH_ENV `grep`
   function, S3 no grep on PATH, S4 relative override, S5 missing override,
   S6 non-GNU stub override, S7 override+echo, S8 default+echo, S9
   override-beats-shim) all pass on both. It measures *the presence of the pin
   machinery*, not *the integrity of the pin*. A gate with three live
   provenance holes (F1, F2, F4) and a gate with none score identically.

2. **Under a forged `head` the counter does drop — to 6/9 on the base gate and
   7/9 on the hardened gate — but for the wrong reason.** The base gate's
   failures are S2, S6 and S9; the hardened gate's are S2 and S9 only. The
   hardened gate's S6 now passes *because the forgery no longer works*
   (`override does not report GNU grep: <no version>`, exit 2). But in **both**
   runs the counter prints `reference run not sane: rc=1 drift=False obs={}` —
   the reference run itself went insane, because the forged `head` also
   corrupted the counter's own fixture tooling (`sed: -e expression #1, char 2:
   extra characters after command`). A counter that reports 6/9 while its
   reference run is broken has **no predicate_holds**, so this is not a kill
   signal for either gate — it is a signal that the counter's own environment
   is attacker-reachable. A BASH_ENV is inherited by every child the counter
   spawns, including the counter's own `sed`/`head` use.

**The C1 claim as frozen is not falsified by my results** (9/9 on the pinned
gate, twice). What my results show is that **P1's predicate is weaker than the
claim's prose**: the claim says the gate "resolves, verifies and pins one grep
binary"; the counter shows only that a pin is *exercised*, not that it is
*authoritative*. F1 is the sharpest instance — a caller who controls `BASH_ENV`
controls the matcher on the pinned gate, and the counter's S2 (BASH_ENV
`grep` function) does not see it because the shadowing name is `command`, not
`grep`.

---

## 5. Does the current lane tip fix F1/F2/F4? (measured, not assumed)

Commit `beb04ea` ("pin hardened (command/head/PATH-fallback/readonly/bounded
probe)") rewrote the pin block. I extracted the tip gate
(`git show HEAD:tools/research-gate.sh`, sha256 `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`)
and re-ran each attack:

| attack | pinned `1f2fb4f5…` | tip `a4768851…` |
|---|---|---|
| F1 shadowed `command` | 18/18 calls hijacked, output forgeable, **no refusal** | **0 bytes** on the tripwire, exit 0, output unaffected |
| F2 forged `head` + non-GNU stub | stub **pinned**, forged version echoed, `2/17` | **refused**: `GREP_PROVENANCE refused: override does not report GNU grep: <no version>`, exit **2** |
| F3 dead PATH fallback | refuses even with GNU grep first on PATH | arm **removed**; message now `no GNU grep at /usr/bin/grep or /bin/grep (set RESEARCH_GATE_GREP to an absolute path)` |
| F4 `readonly -f grep` | bare `grep: readonly function`, exit **1** | **named refusal**: `GREP_PROVENANCE refused: the grep wrapper cannot be defined (a caller marked it readonly)`, exit **2** |

The tip's mechanism, visible in `git diff e87c5d7 HEAD -- tools/research-gate.sh`:
the wrapper is now `grep() { "$GREP_BIN" "$@"; }` — the absolute path is
invoked **directly**, not through `command`, so no `command` function can
intercept it; the version probe cuts the first line with bash expansion
(`v=${v%%$'\n'*}`) instead of `head`, and bounds the probe with an absolute
`timeout`; the wrapper definition is attempted with `eval` and refused by name
if it fails.

**So the lane tip already closes all four holes.** My §1 receipts against the
pinned blob remain valid as a record of the wave base; the lane's current state
is better than the blob I was told to score. I flag this because a reader
comparing my §4 numbers (both gates 9/9) against §5 (only the tip resists)
needs to know the counter cannot tell the two apart.

---

## 6. MEETS / non-MEETS

The card asks for the strongest result: *an engine that scores 9/9 on C1, or
separates nothing on C2, or a witness bypass that still passes P2* — state
exactly why.

**Not a MEETS finding against the pinned gate.** The pinned gate `1f2fb4f5…`
satisfies the assigned `verify-claims` target in full: four environments
exit 0 with byte-identical stdout (`c45bba7687d9c902…`), both tripwires empty,
relative override refused with exit 2 and the exact text
`research-gate: GREP_PROVENANCE refused: override is not an absolute path (candidate=bin/grep)`,
echo-flag stdout diff empty. The frozen counter reports 9/9. **C1 is not
falsified by anything I measured.**

**A partial MEETS, stated precisely.** The pinned gate scores **9/9 on the
frozen C1 counter while a `BASH_ENV` `command` function receives all 18
pinned matcher calls and can fabricate the verdicts the counter then scores as
"matching the reference"** (F1). The counter's own S2 scenario — a BASH_ENV
that shadows `grep` — does not fire, because the shadowing name on the landed
gate is `command`, not `grep`. So the counter's 9/9 is not evidence that the
pinned binary is the one that ran; it is evidence that the pin machinery
exists. **The specific defect: the wrapper invokes the pin through `command`
(`research-gate.sh:351`), and `command` is shadowable by a `BASH_ENV` function
— the same class of hole the round-34 closure identified for bare `grep`
through `PATH`, reopened one layer down.** The fix is the tip's: invoke the
absolute path directly.

**A second, smaller MEETS on the claim's provenance half.** The claim says the
gate *verifies* the pin. On the pinned gate the verification is done by
piping the candidate's `--version` into a PATH-resolved `head`
(`research-gate.sh:360`), so a `BASH_ENV` `head()` makes a non-GNU stub report
itself as GNU grep, get pinned, and get echoed into the receipt line as
`version="grep (GNU grep) 9.9-forged"` (F2). **The `GATE_GREP:` receipt line
was forgeable.** The tip closes this too.

**On C2: out of my scope.** My seat is `verify-claims` mode under the pin. I
read `tools/mechanism-witness.py` and `corpus/evidence/round35/c2-count.py` for
context and measured neither. I ran no C2 counter and make no C2 claim.

**A calibration note on the fixture.** `claims-r2.jsonl` cannot exercise the
chunk matcher (max span 175 B < `TOK_DIRECT_SPAN_MAX=32764`) or the near-miss
`grep -Fn` path (§1.5). Any C1 evidence drawn from "17/17, CLEAN on
claims-r2" covers the direct matcher only.

---

## 7. Limits of this seat

- I measured **one mode** (`verify-claims`). The other modes
  (`verify`, `verify-chain`, `verify-sweeps`, `verify-integrity`,
  `verify-metadata`, `verify-all`, `--pin`, `--drift`) are other seats'
  surfaces; §1.4's base-vs-landed contrast is specific to `verify-claims`.
- I ran the C1 counter at **one seed (3501)**, not the two fresh seeds the
  frozen predicate names. My counter evidence is about *discrimination between
  two gates*, not about re-deriving P1.
- The forged-`head` counter runs (§4) have `reference_sane=false`; I report
  them as a discrimination measurement, **not** as a killed predicate.
- Every §3 attack is an **environment** attack (a caller controlling
  `BASH_ENV`), which is a party with script-execution rights on the host. It
  is not a remote or unprivileged attack, and the round-35 claim's own stated
  limit ("provenance is self-reported; a binary that lies about its version is
  out of this check's reach") covers the adjacent case but not this one: a
  lying `head`/`command` is not the candidate binary lying about itself.
- The mount-namespace probes used `unshare --user --map-root-user --mount
  `--propagation private`; the bind mounts live only inside the namespace and
  were never applied to the host. The host's `/usr/bin/grep` is untouched —
  re-checked after all probes: `sha256sum /usr/bin/grep` =
  `19280b0e0714dadf0c100cdbc7f4823d254dd8facba64deeff5ec50d39fecf84`, mtime
  still `Apr 23  2025`, `--version` still `grep (GNU grep) 3.12-modified`.
- All scratch work was under `/tmp/hyaku/chousa-r35/w2/ExecPinModeClaims/`.
  `/fast` was not written. No network. No `pacman`. No git/jj write command.
  No lane production file was modified — the only lane writes are this report
  and `.ufo/waves/round-35/w2/ExecPinModeClaims/` (my exclusive directory).

---

## 8. Artifact index

All under `.ufo/waves/round-35/w2/ExecPinModeClaims/` (116 KB total; sha256
of each in `receipts/SHA256SUMS.txt`).

| file | what |
|---|---|
| `receipts/G_A-clean.stdout` | env A stdout, sha256 `c45bba76…` |
| `receipts/G_B-shim.stdout` | env B stdout (PATH shim first), sha256 `c45bba76…` |
| `receipts/G_C-override-shim.stdout` | env C stdout (override + shim), sha256 `c45bba76…` |
| `receipts/G_D-echo.stdout` / `.stderr` | env D stdout (sha256 `c45bba76…`) + the `GATE_GREP:` line |
| `receipts/G_E-relative.stderr` | the exit-2 refusal text, sha256 `cd2c921b…` |
| `receipts/base-gate-shim-trip.log` | 18 shim hits on the base gate, sha256 `e4692963…` |
| `receipts/landed-gate-shim-trip.log` | 0 bytes — the landed gate's tripwire |
| `receipts/pinned-calls-claims-r2.log` | 19 pinned calls (18 matcher + 1 `--version`), sha256 `9a37156c…` |
| `receipts/cmd-swap-trip.log` | 18 hijacked calls under the `command` shadow, sha256 `f2ec187c…` |
| `receipts/FORGE_BASE.stdout` / `.stderr` | F1 fabricated-output verdict; stderr 0 bytes (no refusal) |
| `receipts/headforge-stdout.txt` | F2 forged-provenance run |
| `receipts/bash_env_{cmd,forge,head,ro2}.sh` | the four attack fixtures |
| `receipts/c1-{basegate,newgate}-s3501.json` | counter 9/9 on both gates |
| `receipts/c1-{base,new}-forgehead-s3501.json` | counter 6/9 and 7/9 under the forged `head` |

Large/ephemeral scratch (not copied into the lane, cited by path):
`/tmp/hyaku/chousa-r35/w2/ExecPinModeClaims/` — clone at `e87c5d7`, the
byte-exact blob `gate-LANDED-1f2fb4f5.sh`, the tip gate `newgate/`, the shim,
the namespace fixtures and the namespace outputs.
