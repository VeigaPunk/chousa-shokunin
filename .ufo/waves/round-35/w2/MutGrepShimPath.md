# MutGrepShimPath — PATH-shadow controls for C1 (round 35, wave 2)

Seat: mutation tester (leaf, no subagents). Accessed 2026-10-23.
Scratch: `/tmp/hyaku/chousa-r35/w2/MutGrepShimPath/` (`C1_TMP` set there).
Artifacts: `.ufo/waves/round-35/w2/MutGrepShimPath/` (receipts, shims, probe, counter diff; 252 KiB).

Pinned blobs, re-derived before and after all work:

```
1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617  tools/research-gate.sh      (landed)
a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b  .ufo/waves/round-35/repairs/base-gate.sh
da207fd725658b84469ce1fe540a7b94fcb1027cef49da376a8d7ac19ac715e3  corpus/evidence/round35/c1-count.py (never written)
```

## Verdict up front

1. **Assigned probe result: no scenario moves.** All five PATH-first shims score
   `GREP_PIN_MATCH=9/9`, `predicate_holds=true`, gate sha `1f2fb4f5…`, on seeds 3613
   (all five), 3539 (all five) and 3671 (shim c). This is the expected outcome, not a
   failure — but the reason matters (F1/F5): on this host the landed gate **never
   consults PATH** in default resolution, so a PATH shadow cannot be observed at all.
2. **C1/P1 is not killed.** Every run against the landed gate is 9/9 with
   `reference_sane=true`.
3. **F1 (highest-value result): the gate's PATH fallback is dead code and its refusal
   text is false.** `command -v grep` inside the gate resolves the gate's *own*
   `grep()` function (defined at `tools/research-gate.sh:351`, before
   `grep_pin_init` is called at `:8039`), returning the bare word `grep`; the
   `case "$c" in /*)` at `:389-390` then rejects it. The gate therefore refuses with
   "no GNU grep found at /usr/bin/grep, /bin/grep or on PATH" **even when a GNU grep
   is on PATH**. On this host `/usr/bin/grep` verifies first (`:384-386`) so the
   branch is unreachable; on a host whose fixed candidates are absent or non-GNU
   (e.g. BSD `/usr/bin/grep` + Homebrew/Nix GNU grep on PATH) the gate exits 2 and
   cannot run — exactly the operability class C1 was opened for, now as a hard refusal.
4. **F2: a mutant that does not verify the default pin survives 9/9.** `ctl-M2b`
   replaces `grep_pin_verify "$c"` with `[[ -f $c && -x $c ]]` plus a version capture
   for the echo: `GREP_PIN_MATCH=9/9` on seeds 3613 and 3671. P1 is met without the
   claimed verification of the pinned default binary.

## What I ran

### Shims (first on PATH, one per directory)

| id | content | mode |
|---|---|---|
| a | `#!/bin/sh` logs `$*` then `exec /usr/bin/grep "$@"` | 0755 |
| b | symlink `grep -> /bin/false` | — |
| c | `--version`/`-V` prints `grep (GNU grep) 3.11`, exit 0; anything else prints `NOMATCH`, exit 0 | 0755 |
| d1 | regular file `grep` containing `not a grep` (non-executable), real `/usr/bin/grep` later on PATH | 0644 |
| d2 | extra variant of (d): *directory* named `grep` (0755), real `/usr/bin/grep` later | — |

`command -v grep` with each shim first: a/b/c → the shim path; **d1/d2 → `/usr/bin/grep`**
(bash's PATH search skips non-executable files and directories). So (d) never shadows at
all; it tests bash, not the gate.

### Scoring (counter copies, one change each)

`c1-count.py` pins `PATH` itself in `run_gate` (`clean_path`), so an inherited PATH cannot
reach the gate. I scored with five **named control counters**, each byte-identical to the
committed counter except line 183 (`clean_path = "<shimdir>:/usr/local/bin:/usr/bin:/bin"`).
Diff: `.ufo/waves/round-35/w2/MutGrepShimPath/ctl-shim-counter.diff`. Control shas:

```
4b651984… ctl-shim-a-c1-count.py    23669e02… ctl-shim-b-c1-count.py
ff1a5cf1… ctl-shim-c-c1-count.py    6a51cb8d… ctl-shim-d1-c1-count.py
30b6712d… ctl-shim-d2-c1-count.py
```

Command shape (exit codes observed in parentheses):

```
C1_TMP=/tmp/hyaku/chousa-r35/w2/MutGrepShimPath/tmp \
timeout 900 python3 <counter> --gate tools/research-gate.sh --seed <N> --receipt <F>
```

Seeds: `3539` was already used in this wave by peers (`ExecC1Control`, `ExecC1Fresh1`), so I
reran everything on `3613` and repeated the key runs on `3671`; both were absent from
`.ufo/` and `corpus/`. Note `make_fixture(root)` (`c1-count.py:50-73`) never reads the seed —
it labels the temp dir and the receipt only [read, not inferred].

### Results

| gate | counter | seed | label | predicate | shim bytes in S1 | S8 echo |
|---|---|---|---|---|---|---|
| landed | unmodified | 3539 / 3613 / 3671 | 9/9 ×3 | true (exit 0) | 0 | `path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"` |
| landed | shim-a | 3539 / 3613 | 9/9 | true | 0 | same |
| landed | shim-b | 3539 / 3613 | 9/9 | true | 0 | same |
| landed | shim-c | 3539 / 3613 / 3671 | 9/9 | true | 0 | same |
| landed | shim-d1 | 3539 / 3613 | 9/9 | true | 0 | same |
| landed | shim-d2 | 3539 / 3613 | 9/9 | true | 0 | same |
| ctl-M2 (fold verify to `-f -x`) | unmodified | 3613 / 3671 | **8/9** | false (exit 1) | 0 | `version=""` → S8 FAIL |
| ctl-M3 (PATH-first default) | unmodified | 3613 | **6/9** | false, `reference_sane=false` | — | S8 `rc=2` |
| ctl-M2b (trust default, capture version) | unmodified | 3613 / 3671 | **9/9** | **true (exit 0)** | 0 | normal GNU version |
| ctl-M4 (fixed candidates → non-GNU stub, otherwise landed) | unmodified | 3613 | 6/9 | false, `reference_sane=false` | — | refusal |
| ctl-M4fix (M4 + `type -P grep` in fallback) | unmodified | 3613 | 7/9 | false | 862 | S8 pass, S1/S3 FAIL |

Every receipt is in `.ufo/waves/round-35/w2/MutGrepShimPath/receipts/` (`*-s<seed>.json`).

### Direct probe (gate run with a shim first on PATH, echo forced on)

`probe.py` builds the same three-claim fixture, runs the gate with
`PATH=<shim>:/usr/local/bin:/usr/bin:/bin` and `CHOUSA_GREP_PIN_ECHO=1`, and compares rc +
`CLAIM` lines to a shim-free reference.

| shim | landed gate | base gate (a6307edf) |
|---|---|---|
| a | shim bytes **0**, output identical, pins `/usr/bin/grep source=default` | shim bytes **852** (5 calls), output identical |
| b | 0, identical | `rc=2`, 0 claims, stderr `GNU grep with -z/-P support is required…` (interception, log unobservable: /bin/false logs nothing) |
| c | 0, identical | shim bytes **581**, `rc=1`, **0 CLAIM lines**, stderr `sed: -e expression #1, char 2: extra characters after command` |
| d1 | 0, identical | 0, identical (shim never resolvable) |
| d2 | 0, identical | 0, identical (shim never resolvable) |

The base-gate numbers reproduce claims.md's pre-data S1 record ("852 and 867 bytes of shim
log"), so the probe is live, not vacuous: the same shims that are inert on the landed gate
are intercepted by the base gate.

## Findings

### F1 — dead PATH fallback; false refusal text (latent operability defect)

Located: `tools/research-gate.sh:351` (`grep() { command "$GREP_BIN" "$@"; }`), `:384-386`
(fixed candidates), `:387-392` (fallback), `:393` (refusal text), call site `:8039`.

Mechanism, direct:

```
$ bash -c 'GREP_BIN=""; grep() { command "$GREP_BIN" "$@"; }; c=$(command -v grep); …'
command -v grep -> [grep]
type -t grep -> [function]
case: rejected by /*)  -> fallback refuses
$ bash -c 'c=$(command -v grep)'        # same shell, wrapper absent
command -v grep -> [/usr/bin/grep]
```

End-to-end A/B (both derived from the landed bytes; only the fixed candidate literal differs,
to simulate a host whose `/usr/bin/grep` is not GNU):

* `ctl-M4-nongnu-host-gate.sh` (sha `13386d34…`): reference run `rc=2`,
  `research-gate: GREP_PROVENANCE refused: no GNU grep found at /usr/bin/grep, /bin/grep or on PATH (candidate=<none>)`
  — while a verified GNU grep sat at `/usr/bin/grep` on PATH. Counter: 6/9, `reference_sane=false`.
* `ctl-M4fix-typeP-gate.sh` (sha `0c93445f…`, same file with `command -v` → `type -P`):
  reference `rc=1`, 3 `CLAIM` lines, pins `/usr/bin/grep`. One token changes refusal into a
  working pin, so function shadowing is the sole cause.

Why the C1 counter cannot see it: no scenario removes or poisons the fixed candidates, so
`:387-392` is never entered on this host. `S3-no-grep-on-path` empties PATH but
`/usr/bin/grep` still resolves, so it passes for the landed gate and for a gate whose
fallback is broken. This is a **coverage gap, not a P1 kill**: the predicate is about the
landed host, and there the gate scores 9/9 every time.

Why it matters: the round-34 complaint was "the gate cannot be run at all without grep on
PATH"; the landed gate fixes that by hardcoding the two paths and leaves the documented
PATH route refusing. On any host whose only GNU grep is elsewhere on PATH the gate is
unusable (exit 2), which is worse than the base gate, which would have used it.

### F2 — a gate that does not verify its default pin scores 9/9 (MEETS-adjacent)

`ctl-M2b-trusting-default-gate.sh` (sha re-derived `1f2fb4f5…` at copy time, mutated;
receipts `ctl-M2b-*-s{3613,3671}.json`): landed bytes with `:385` changed from
`if grep_pin_verify "$c"` to `if [[ -f $c && -x $c ]]` plus a version capture for the
echo. It resolves and pins, but never asserts the binary reports GNU grep.
`GREP_PIN_MATCH=9/9`, `predicate_holds=true`, exit 0, on both fresh seeds.

Why it survives: the only scenario that touches default-branch verification is
`S8-default-echo`, and its oracle is the echoed version text. Because the mutant still
captures `--version`, the text is unchanged (`grep (GNU grep) 3.12-modified`), so S8 passes
without any check having run. No scenario can make the fixed candidate fail verification —
`/usr/bin/grep` on this host is GNU by construction. So P1 cannot distinguish "verifies the
default pin" from "trusts `/usr/bin/grep` because it is the host's GNU grep". The check that
C1's prose claims is untested for the default branch; only the override branch (S6) is
actually exercised.

### F3 — M2's kill is incidental

`ctl-M2-unverified-default-gate.sh` (fold verify to `-f -x`, no version capture) is killed
8/9, but only by `S8` and only because `GREP_PIN_VERSION` is left empty
(`GATE_GREP: … version=""`). Behaviour was output-identical to the landed gate
(`output_matches_reference: true`). The kill hinges on a side effect of `grep_pin_verify`
populating a string, not on a provenance assertion — F2 is the same mutant with that side
effect restored, and it survives.

### F4 — (d) cannot shadow anything

Both d variants resolve to `/usr/bin/grep`: bash's PATH search skips non-executable regular
files and directories. The expectation "no scenario fails" holds for a reason unrelated to
the gate; this control says nothing about grep provenance.

### F5 — what S1 actually measures

S1's oracle is "shim log is empty". With the fixed candidates non-GNU, a *one-time* startup
resolution through PATH (`ctl-M4fix`) also executes the shim: 6 log lines, first
`--version`, 862 bytes — versus the base gate's 5 per-call lines / 852 bytes. S1 cannot tell
one startup resolution from per-call resolution; it only distinguishes "PATH never used"
from "PATH used". The landed gate passes because it never uses PATH, not because the pin
abstraction neutralises a shim — if it ever pinned the shim, every matcher call would still
run the shim (exactly what S1 sees in `ctl-M4fix`).

## Mutation ledger (role deliverable)

* **Mutant probed:** `ctl-M2b-trusting-default-gate.sh` — smallest behaviour-bearing point:
  the default-branch verification predicate at `research-gate.sh:385`.
* **Detector:** `corpus/evidence/round35/c1-count.py --gate <mutant> --seed {3613,3671}`
  (committed bytes, unmodified).
* **Baseline on pristine bytes:** 9/9, `predicate_holds=true`, gate sha `1f2fb4f5…` on both
  seeds (also on 3539), so a failure would have been attributable, not inconclusive.
* **Output:** `GREP_PIN_MATCH=9/9`, exit 0, no failing scenario, both seeds.
* **Verdict:** **survived** — a coverage finding for C1's default-branch verification, not a
  licence to weaken the contract. Controls M2 (8/9) and M3 (6/9) were killed; M4/M4fix were
  built only to demonstrate F1 and are not candidate gates.
* **Restoration:** no production byte was edited; all mutants are scratch copies named
  `ctl-M*` under `/tmp/hyaku/chousa-r35/w2/MutGrepShimPath/`. Lane state after the work:
  `tools/research-gate.sh` = `1f2fb4f5…`, `base-gate.sh` = `a6307edf…`, counter =
  `da207fd7…`; only `.ufo/waves/round-35/w2/MutGrepShimPath/` is new from this seat
  (`git status --porcelain`: 40 lines, none of them mine outside that path).

## Limits

* I could not remove the host's `/usr/bin/grep`, so F1's production impact is demonstrated on
  candidate-literal substitution (`ctl-M4`), which is byte-identical to the landed gate
  except for the two fixed paths; the landed gate's behaviour on such a host is
  **[INFERENCE]** from that A/B plus the shell snippet, not a run of the landed file.
* Shim (b) never logs, so its interception is inferred from `rc`/output change (`rc=2`, no
  `CLAIM` lines) rather than from a tripwire count.
* PATH was injected by patching one constant in named counter copies (the committed counter
  pins PATH itself); the five control counters differ from the committed file by that single
  line, and their receipts carry the untouched gate sha.
* Seeds 3613/3671 are fresh for this lane; the counter's fixture is seed-independent, so the
  seed is a label, not a parameter — two seeds add no statistical power here.
* No installs were needed or made; no network used; nothing outside the scratch dir and this
  report dir was written. Untracked `__pycache__/` directories exist in the lane
  (`corpus/evidence/round35/__pycache__/c1-count.cpython-314.pyc` mtime 16:58:59,
  `tools/__pycache__/mechanism-witness.cpython-314.pyc` 16:46:04); they are module-import
  caches, my runs executed both scripts as `__main__` (no `.pyc` written), so they are not
  mine and I removed nothing.

## Artifacts

```
.ufo/waves/round-35/w2/MutGrepShimPath/
  probe.py                     Path-shadow probe (gate x shim x PATH)
  ctl-shim-counter.diff        one-line clean_path patch applied to the counter controls
  receipts/*.json              33 receipts (counter runs + probes), each < 4 KiB
                               (counter stdout logs stayed in /tmp/…/receipts/*.out — cited, not copied)
  shims/{a,b,c,d1,d2,nongnu}/  shim trees (b is a symlink, d2 a directory named grep)
  trip-m4fix-a.log             6-line shim log (startup resolution + 5 matcher calls)
  trip-base-a2.log             5-line shim log (per-call PATH resolution)
```
