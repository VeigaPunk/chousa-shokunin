# ExecPinModeIntegrity — `verify-integrity` under the grep pin (round-35 w2, attack + re-derive)

Seat: leaf executor. Lane `chousa-shokunin`. Access date 2026-10-23. No production file
touched; artifacts only under `.ufo/waves/round-35/w2/ExecPinModeIntegrity/` and
`/tmp/hyaku/chousa-r35/w2/ExecPinModeIntegrity/`. No installs, no network, no git/jj write.

## 0. Gate pins (every scored run cites the sha it ran under)

| gate | sha256 | origin |
|---|---|---|
| **assigned wave-base (blob `1f2fb4f5`)** | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` | `git cat-file -p e87c5d7ea2dbf3730b36a3961de3f06261d015e4:tools/research-gate.sh` → `/tmp/hyaku/chousa-r35/w2/ExecPinModeIntegrity/gate-WAVEBASE-1f2fb4f5.sh`, re-hashed equal |
| base (round-34) | `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` | `.ufo/waves/round-35/repairs/base-gate.sh`, re-hashed equal |
| HEAD (sibling-hardened, mid-wave) | `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` | `git cat-file -p HEAD:tools/research-gate.sh` → `gate-HEAD-a4768851.sh` |

**Gate drift mid-wave.** At my start `tools/research-gate.sh` hashed `1f2fb4f5…`; a sibling
then committed a hardened pin (`beb04ea`, `770a69d`, `7d21a33`) and the working-tree file now
hashes `a4768851…`. Every row below was taken against an **extracted, re-hashed blob**, never
against the moving working-tree file. §1–§4 are the assigned blob `1f2fb4f5`; §6 measures the
hardened HEAD blob separately and the two sha's are never mixed.

Fixture (committed integrity fixture): `corpus/fixtures/integrity-r7.md`,
sha256 `4310ce86aa45f3d7d4b7d04c4ebf480a7b59748510ab0f132c5411dd8acd1b1b`, tracked; twin
`integrity-r7-broken.md` sha `fd4e213f03faf9a76bbca3896b11fe6530878e727fefb974043ffb4a9f9a05b8`.
Expected positive: `INTEGRITY refs=16 resolved=15 unresolved=0`, CLEAN, exit 0.

## 1. THE HEADLINE ANSWER — `verify-integrity` never greps, so the pin cannot affect it

**This mode calls grep exactly once, and that one call is the pin's own provenance probe.
There is no matcher grep call anywhere in the integrity path.** Three independent
measurements:

**(a) `bash -x` trace.** `PS4='+TRACE ' bash -x <gate> verify-integrity corpus/fixtures/integrity-r7.md --root .`
— the only `grep`-bearing trace lines are inside `grep_pin_init` / `grep_pin_verify`
(13 lines total, all of them `grep_pin_init`, the `for c in /usr/bin/grep /bin/grep` loop,
`grep_pin_verify /usr/bin/grep`, and `/usr/bin/grep --version`). No matcher argv appears.

**(b) `strace -f -e trace=execve`.** Landed blob: **1** `execve("/usr/bin/grep", …)` — the
`--version` probe. Base blob `a6307edf`: **0** grep execs at all. By contrast
`verify-all` on the same record: **34**; `verify-claims` on a one-claim fixture: **3**.

**(c) argv wrapper** (`RESEARCH_GATE_GREP=<wrapper that logs argv then execs /usr/bin/grep>`):

| mode | total grep invocations | matcher (`-a -z -b -o -P`) |
|---|---:|---:|
| `verify-integrity integrity-r7.md` | **1** | **0** |
| `verify-all integrity-r7.md` | 34 | 1 |
| `verify-claims` (1 claim) | 3 | 2 |

Receipt: `receipts/argv-wavebase-verify-integrity.log` (`ARGV[--version]` — one line);
`receipts/argv-wavebase-verify-claims.log`.

**Consequence, stated plainly as the assignment demands.** `verify-integrity` is a
**grep-free mode**. The pin therefore buys this mode **no correctness** and can take it away
**no correctness**: the integrity verdict is byte-identical under every grep environment
because no grep ever runs. Its `INTEGRITY refs=` line is a function of the record's tables
(`table_rows` → `cell` → `chain_cell` → `integ_cell`/`integ_token`, all pure bash + `sed`/`tr`),
not of the matcher. The pin's *only* effect on this mode is (i) the startup refusal (below)
and (ii) the optional `GATE_GREP:` echo line. **This mode must not be cited as evidence that
the pin holds** — it is evidence that the pin is *inert* here. The pin's coverage claim lives
on the claims/chain surfaces, where the matcher actually runs.

## 2. Four environments + the refusal family — assigned blob `1f2fb4f5`

Command shape for every row (lane cwd, `env -i`, bounded):
`env -i PATH=<path> HOME=… [BASH_ENV=…|RESEARCH_GATE_GREP=…] timeout 900 bash <gate> verify-integrity corpus/fixtures/integrity-r7.md --root .`
Probe script: `integ-env-probe.sh` (in my directory). Summary: `receipts/landed-summary.txt`.

| # | environment | rc | `INTEGRITY refs=` line | tripwire | refusal |
|---|---|---:|---|---|---|
| E1 | clean `PATH=/usr/local/bin:/usr/bin:/bin` | **0** | `INTEGRITY refs=16 resolved=15 unresolved=0` | n/a | none |
| E2 | shim-first PATH (`grep` script logs `$*`, then `exec /usr/bin/grep`) | **0** | `INTEGRITY refs=16 resolved=15 unresolved=0` | path **0 B** | none |
| E3 | `BASH_ENV` defines `grep()` that logs (the counter's S2 shape) | **0** | `INTEGRITY refs=16 resolved=15 unresolved=0` | fn **0 B** | none |
| E4 | grep absent from PATH (38-tool symlink farm, no `grep`) | **0** | `INTEGRITY refs=16 resolved=15 unresolved=0` | n/a | none |

Verdict line in all four (identical):
`RESEARCH_GATE: CLEAN (refs=16 resolved=15 unresolved=0 exempt=1 findings=0 drift=0)`.

Refusal family, same mode, same blob — every one exits **2 before any record is read**
(0 stdout lines; the record is never opened):

| # | override | rc | verbatim refusal |
|---|---|---:|---|
| R1 | `bin/grep` (relative) | 2 | `research-gate: GREP_PROVENANCE refused: override is not an absolute path (candidate=bin/grep)` |
| R2 | non-existent absolute path | 2 | `research-gate: GREP_PROVENANCE refused: override is not a regular file (candidate=…/absent-grep)` |
| R3 | non-GNU stub (`--version` → `pi-uu-grep 0.2.0`) | 2 | `research-gate: GREP_PROVENANCE refused: override does not report GNU grep: <no version> (candidate=…/stub-grep)` |

R3's stub-exec tripwire holds **15 bytes = exactly one line** (`--version`): the refused binary
is probed once and never used for a match.

Echo surfaces (assignment asked for the receipt line):

| # | env | `GATE_GREP:` line (stderr) |
|---|---|---|
| R4 | `RESEARCH_GATE_GREP=/usr/bin/grep CHOUSA_GREP_PIN_ECHO=1` | `GATE_GREP: path=/usr/bin/grep source=override version="grep (GNU grep) 3.12-modified"` |
| R5 | `CHOUSA_GREP_PIN_ECHO=1` | `GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"` |
| R6 | `BASH_ENV` grep() shim + real override + echo | `source=override`, tripwire **0 B** — the override wins |

**Base-gate contrast (the C1 "before"), same four environments** (`receipts/base-summary.txt`):

| env | base rc | `INTEGRITY refs=` | tripwire |
|---|---:|---|---|
| E1 clean | 0 | `16/15/0` | — |
| E2 shim-first PATH | 0 | `16/15/0` | **0 B** |
| E3 `BASH_ENV` `grep()` | 0 | `16/15/0` | **0 B** |
| E4 grep absent from PATH | 0 | `16/15/0` | — |
| R1 relative override | **0** (no pin, no refusal) | `16/15/0` | — |
| R3 non-GNU stub override | **0** | `16/15/0` | — |

**This is the honest calibration of my item.** The base gate's tripwires are *also* empty on
this mode — not because the base gate was safe, but because **this mode never greps**. The
integrity surface therefore **discriminates nothing** between the base gate and the pinned
gate on the matcher axis: the only differences are the startup refusal family (R1/R2/R3) and
the echo line, both of which are startup-level, not matcher-level. A counter that scored
`verify-integrity` environments would score the base gate 6/9 and the pinned gate 9/9 —
**and would be measuring the pin's setup code, not the pin's claim.**

## 3. No-harm on the assigned surface — byte-identical

`diff` of stdout, landed blob vs base blob, after normalising only the volatile `ts=` field:

| env | landed sha (first 16) | base sha (first 16) | result |
|---|---|---|---|
| E1 | `cc8d054f0c804d1c` | `cc8d054f0c804d1c` | **IDENTICAL** |
| E2 | `cc8d054f0c804d1c` | `cc8d054f0c804d1c` | **IDENTICAL** |
| E3 | `cc8d054f0c804d1c` | `cc8d054f0c804d1c` | **IDENTICAL** |
| E4 | `cc8d054f0c804d1c` | `cc8d054f0c804d1c` | **IDENTICAL** |

The only line that differs between the two gates on this mode is the `ts=` banner; the
integrity verdict surface is byte-identical to round 34. The pinned gate adds no drift.

## 4. FINDINGS — attacks that hold against the assigned blob `1f2fb4f5`

These are **not** integrity-mode findings (this mode never greps). They are findings about
the **pin's verification pipeline**, which every mode including integrity inherits at startup,
and they are the wave's most useful result because they defeat the *refusal* half of C1.

### F1 (operability, real) — the `command -v grep` PATH fallback is dead code

`grep_pin_init` default branch, `tools/research-gate.sh:386-393` (blob `1f2fb4f5`):

```bash
c=$(command -v grep 2>/dev/null || true)
case "$c" in
  /*) if grep_pin_verify "$c"; then cand=$c; fi ;;
esac
[[ -n $cand ]] || grep_pin_refuse "no GNU grep found at /usr/bin/grep, /bin/grep or on PATH" ''
```

The gate defines `grep()` as a shell **function** at line 351 and `grep_pin_init` runs at line
8039, after it. So `command -v grep` prints the *function name*, not a path:

```
$ bash -c 'grep() { command /usr/bin/grep "$@"; }; echo "command -v grep => [$(command -v grep)]"'
command -v grep => [grep]          # not "/usr/bin/grep" -> the /*) case never matches
```

The `/*)` arm can therefore never fire: **the advertised "or on PATH" fallback is
unreachable**. Measured with a patched copy of the assigned blob whose
`for c in /usr/bin/grep /bin/grep` pair was replaced by two non-existent paths (so only the
PATH fallback could save it), and a PATH farm whose `grep` **is** the real GNU `/usr/bin/grep`:

| gate | rc | result |
|---|---:|---|
| patched `1f2fb4f5` (PATH pair removed) | **2** | `research-gate: GREP_PROVENANCE refused: no GNU grep found at /usr/bin/grep, /bin/grep or on PATH (candidate=<none>)` |
| unpatched `1f2fb4f5` | 0 | `INTEGRITY refs=16 resolved=15 unresolved=0` |

So on a host whose GNU grep is not at `/usr/bin/grep` or `/bin/grep`, the landed gate refuses
where the base gate ran. Fail-closed, but an operability regression **and a false message**
(the refusal names a PATH fallback that cannot execute). Patch script and outputs:
`pin-head-dependency.sh` / `receipts/headdep-wavebase.txt`; patched blob sha
`608223692bc0082c94ab40af74338e06c01e575eedd4ed86dd4dd4b1a5c70dac`.

### F2 (soundness) — a forged `head` defeats the provenance check; the pin then runs the wrong engine

`grep_pin_verify` cuts the version line with an **unpinned PATH tool**, `tools/research-gate.sh:361`
(blob `1f2fb4f5`):

```bash
v=$("$cand" --version 2>/dev/null | head -n 1 || true)
case "$v" in *"GNU grep"*) return 0 ;; esac
```

`head` is shadowable by a PATH script **or** a `BASH_ENV` function. With a `head` that forges
the version line and a non-GNU candidate that matches nothing, the assigned blob **accepts the
stub as GNU grep**:

| # | setup (assigned blob `1f2fb4f5`) | rc | `GATE_GREP:` line | effect |
|---|---|---:|---|---|
| V0 | non-GNU stub alone | **2** | — | refused: `override does not report GNU grep: <no version>` |
| V1 | non-GNU stub + **PATH `head` shim** | **0** | `path=…/stub-grep source=override version="grep (GNU grep) 9.99-SPOOFED"` | **forged provenance accepted** |
| V2 | non-GNU stub + **`BASH_ENV` `head()`** | **0** | `… version="grep (GNU grep) 9.99-SPOOFED"` | **forged provenance accepted** |
| V3 | V1 against `verify-claims` | **1** | `… 9.99-SPOOFED` | `CLAIM id=K1 expected=supported observed=unsupported` — **wrong verdict** |
| V4 | **control**: real `/usr/bin/grep` + same head shim | 0 | `version="grep (GNU grep) 9.99-SPOOFED"` | correct verdict; only the receipt string is forged |
| V5 | V1 with a **logging** stub | 1 | — | stub-exec log = `--version`, `-a -z -b -o -P -- x`, `-a -z -b -o -P -- \x72\x65…` — **the stub served the matcher** |

The `9.99-SPOOFED` string is deliberately distinct from the host's real
`grep (GNU grep) 3.12-modified`, so V4 proves the version line was *rewritten*, not coincidental.
V5's log proves the accepted stub is the binary that actually answers the matcher.

C1's own contract is "refuses a pin it cannot verify with a named exit-2 refusal"; this breaks
it **from inside C1's declared threat model** — `claims.md` lists a `BASH_ENV` function shim as
in scope (counter scenario S2), and C1's stated limit excuses only "a binary that lies about
its own version", not a forged **verification pipeline**. The forged line is not even the
binary's own output.

**Second half of the same hole (measured, same blob).** The pin's *own* dependence on `head`
means a PATH **without** `head` makes the gate refuse to run at all — the failure of an
unrelated tool is reported as a grep-provenance refusal:

| environment (assigned blob `1f2fb4f5`) | rc | result |
|---|---:|---|
| D1 `head` absent from PATH (grep present) | **2** | `research-gate: GREP_PROVENANCE refused: no GNU grep found at /usr/bin/grep, /bin/grep or on PATH (candidate=<none>)` |
| D2 `head` present but silent | **2** | same refusal |
| D4 same D1 environment, **base** blob `a6307edf` | **0** | `INTEGRITY refs=16 resolved=15 unresolved=0` |
| D4b same D2 environment, **base** blob | **0** | `INTEGRITY refs=16 resolved=15 unresolved=0` |

The landed gate **added** a PATH dependency on `head` that the base gate did not have, and
reports its absence as a *grep* problem. Receipt: `receipts/headdep-wavebase.txt`.

### F3 (soundness, same class as a sibling seat's finding — independently reproduced) — `command` shadow intercepts every pinned call

The wrapper is `grep() { command "$GREP_BIN" "$@"; }` (`:351`, blob `1f2fb4f5`). `command` is
a builtin and **is** shadowable by a `BASH_ENV` function. On `verify-claims` with a
`command()` shadow that logs and forwards, the interception is **invisible to output**: the
verdict stays `supported` while every pinned call is diverted. I measured 0 interceptions on
`verify-integrity` (this mode never greps, §1) and the full interception on the claims
surface, where the matcher runs. Because the shadow forwards, the output is correct — that is
precisely the point: a shadow that served a *different* engine would return whatever it liked
while the capability probe still reported success.

## 5. F4 (calibration) — C1's committed 9/9 counter is blind to F1–F3

Against the assigned blob `1f2fb4f5`, the committed counter is green on two fresh seeds:

```
$ C1_TMP=… python3 corpus/evidence/round35/c1-count.py --gate …/gate-WAVEBASE-1f2fb4f5.sh \
    --seed 3601 --receipt receipts/c1-3601.json
GREP_PIN_MATCH=9/9        (S1…S9 all PASS; predicate_holds=true)
$ … --gate …/gate-WAVEBASE-1f2fb4f5.sh --seed 3602 --receipt receipts/c1-3602.json
GREP_PIN_MATCH=9/9
```

**A receipt-hygiene trap worth recording.** My first seed-3602 run used the counter's
**default** `--gate`, i.e. the moving working-tree file `tools/research-gate.sh` — which by
then hashed `a4768851…`, so that receipt cited the hardened blob while my notes described
the assigned one. Re-run with the extracted `1f2fb4f5` blob pinned via `--gate`, the receipt
cites `gate_sha256=1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`.
Both shipped receipts now carry the assigned blob's sha (verified by re-reading the JSON).
**The counter's default `--gate` is a relative path into a file that changed mid-wave: a
counter receipt is only evidence if its `gate_sha256` is checked against the blob the claim
names.**

Receipts `receipts/c1-3601.json`, `receipts/c1-3602.json` (each cites
`gate_sha256=1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`).

But the counter **cannot see F2**, because its S6 scenario builds a stub whose `--version`
prints to **stderr** (`c1-count.py:118-124`), which the wave-base probe (`| head -n 1`) reads
as empty. Give the counter a `head` shim on the same `shim_dir` it already builds and it
**detects the bypass** — proving the 9/9 is a property of the counter's environment, not of the
pin. Counter **copy** (committed file untouched; copy in my directory as
`c1-count-headshim-variant.py`, one injection: a `head` shim in `shim_dir` and `shim_dir`
prepended to `clean_path`):

```
$ python3 c1-count-headshim-variant.py --gate …/gate-WAVEBASE-1f2fb4f5.sh --seed 3604 \
    --receipt receipts/c1-3604-headshim-variant.json
GREP_PIN_MATCH=8/9
  S6-override-non-gnu  FAIL  {"marker": false, "rc": 1, "stub_calls": 6}
```

`stub_calls: 6` — the non-GNU stub served **6** calls instead of being refused. Same gate,
same nine scenarios, 9/9 → 8/9, one line of environment changed. **C1's frozen predicate P1
is therefore satisfied on a gate where the refusal is defeatable.** That is the wave's headline
calibration result: **the 9/9 does not cover the verification pipeline the pin relies on.**

The counter also never runs `verify-integrity` (`c1-count.py:93` invokes `verify-claims` only),
so no part of P1 speaks to this mode at all.

## 6. The hardened HEAD blob `a4768851` — measured, not assigned

A sibling committed a hardened pin mid-wave (`beb04ea`, HEAD `7d21a33`). Measured against the
extracted HEAD blob `gate-HEAD-a4768851.sh` (sha re-verified):

| check | assigned `1f2fb4f5` | hardened `a4768851` |
|---|---|---|
| E1–E4 four environments (integrity mode) | rc 0, `16/15/0`, trip 0/0/0 | **identical**: rc 0, `16/15/0`, trip 0/0/0 (`receipts/hardened-summary.txt`) |
| R1 relative override | rc 2, `GREP_PROVENANCE refused: override is not an absolute path` | rc 2, same text |
| R3 non-GNU stub | rc 2, refused; stub served 1 call | rc 2, refused; stub served 1 call |
| R4/R5 echo lines | `path=/usr/bin/grep source=override|default version="grep (GNU grep) 3.12-modified"` | identical |
| **F2 forged `head`** (V1/V2/V3) | **accepted — forged version `9.99-SPOOFED`, stub served the matcher** | **rc 2, refused: `override does not report GNU grep: <no version>`; stub served 1 call (`--version`) only** |
| **D1 `head` absent from PATH** | rc 2 (spurious refusal) | **rc 0, `INTEGRITY refs=16 resolved=15 unresolved=0`** |
| grep invocations, `verify-integrity` | 1 (`--version`) | 1 (`--version`) — still grep-free |

The hardened blob's `grep_pin_verify` cuts the version with bash expansion
(`v=${v%%$'\n'*}`) instead of `head`, bounds the probe with an absolute
`/usr/bin/timeout`, and defines the wrapper **after** the pin resolves, without `command`.
It closes F1–F3 on this surface. I did **not** score it as the claim's measurement and I did
not edit it.

## 7. Limits of my measurements

- The claims "no grep in the integrity path" and "the pin is inert here" are established for
  the **committed fixture `integrity-r7.md` and the shipped gate source**. A record with a
  `## Sweeps` section naming a glob could in principle route into a grep-bearing helper;
  `verify_integrity` calls only `table_rows`/`cell`/`chain_cell`/`integ_cell`/`integ_token`/
  `sweep_raw_where`/`sweep_token_class`/`scan_secrets`, all pure bash + `sed`/`tr`
  ([INFERENCE] from the function bodies at `tools/research-gate.sh:611-620, 648-666,
  2060-2071, 2420-2433, 2475-2487, 2497-2503, 2753-2770, 2788-2803, 2805-2820, 811-838`),
  corroborated by the argv wrapper showing exactly one grep call.
- F2 requires the caller to control the gate process's `PATH` or `BASH_ENV` — exactly the S2
  threat model C1 declares, not an extra one. I did not attempt a shadow that returns
  *deliberately wrong offsets*; I proved the forgery and the stub-served-matcher, which is
  enough to defeat the refusal.
- F1's demonstration used a **patched copy** of the assigned blob (the `/usr/bin/grep`,
  `/bin/grep` pair replaced) because the host has GNU grep at `/usr/bin/grep`, so the
  unreachable fallback never fires here. The patch is a one-line substitution; the patched
  blob's sha is recorded above. The reachability of the defect is therefore *demonstrated on
  a patched blob*; the defect itself is visible in the unpatched source at
  `tools/research-gate.sh:388`.
- I did not re-run the whole selftest (not my seat's surface) and did not open the C2
  witness tool (not my surface).
- No installs, no network. Every command bounded with `timeout` (900 s probes, 300 s probes,
  1800 s counter). Every scored gate cited by sha256. No writes outside my wave directory and
  `/tmp/hyaku/chousa-r35/w2`.

## 8. Verdict on my item

**The four environments behave as the claim requires, but the mode must not be cited as
pin coverage.** On the committed integrity fixture `corpus/fixtures/integrity-r7.md`,
`verify-integrity` under blob `1f2fb4f5` gives **exit 0** and
**`INTEGRITY refs=16 resolved=15 unresolved=0`** in all four environments (clean PATH,
shim-first PATH, `BASH_ENV` `grep()` shim, grep-free PATH), with **0-byte tripwires** and
**no refusal**; the refused-override family (relative / missing / non-GNU) exits **2** with
the named `research-gate: GREP_PROVENANCE refused: …` before any record is read; and the
stdout is **byte-identical to the round-34 base gate** in all four environments (only `ts=`
differs). **But `verify-integrity` calls grep exactly once — the pin's own `--version` probe
— and never calls grep as a matcher** (bash -x trace, `strace -f -e trace=execve` = 1 exec on
the landed blob and 0 on the base blob, and an argv wrapper recording `ARGV[--version]` only).
The pin is **inert** on this mode: it changes no verdict, and the empty tripwires are a
property of the mode, not of the pin. Reporting this mode as pin coverage would be a false
positive; the base gate scores identically here.

**The wave's real result is F1–F3, measured on the pin's own startup path, which this mode
inherits:** the advertised `command -v grep` PATH fallback is unreachable dead code (F1); the
provenance check cuts the version line with an **unpinned** `head`, so a PATH script or a
`BASH_ENV` function forges it — the non-GNU stub is accepted as GNU grep
(`version="grep (GNU grep) 9.99-SPOOFED"`) and then **serves the matcher**, producing a wrong
claim verdict where the base gate was right (F2); and `command` is shadowable, so every
pinned call can be intercepted with the output unchanged (F3). The committed counter's 9/9
is blind to F2 — the same nine scenarios score **8/9** with a `head` shim added to the
counter's own `shim_dir`, with `stub_calls: 6` — so **P1 is satisfied on a gate whose refusal
is defeatable**. All three are closed by the sibling's hardened blob `a4768851` (§6), whose
own 9/9 was green before they were fixed: a 9/9 receipt alone does not witness the
verification pipeline.
