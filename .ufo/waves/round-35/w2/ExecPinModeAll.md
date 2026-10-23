# ExecPinModeAll — round-35 w2: mode `verify-all --json` under the grep pin

**Seat:** executor (leaf; no subagents dispatched, no background job kept).
**Lane:** chousa, `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
**Gates scored (both sha256-pinned, both cloned from the lane repo):**

| label | revision | `tools/research-gate.sh` sha256 | role |
|---|---|---|---|
| **wave-base** | `e87c5d7ea2dbf3730b36a3961de3f06261d015e4` | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` | the gate my brief names |
| **current** | `770a69d61c783e33762991b84dba43b1bdff8267` | `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` | live lane HEAD at measurement |
| **ctl-regressed** | wave-base wrapper form re-applied to **current** | `7afd040fe7aebc42fb033ddf0a5ef95b7a3f7e0f1d59a8cee4a1b6112799353d` | named control (diff `ctl-wrapper-regressed.diff`), built by this seat |

Pre-round control `.ufo/waves/round-35/repairs/base-gate.sh` = `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` (verified).
**Scratch:** `/tmp/hyaku/chousa-r35/w2/ExecPinModeAll/` (~1.1 GB of clones; logs ≤ 200 KB). **Installs:** none. No network, no pacman, no git/jj writes.

> **Lane state note (observed, not caused).** The live gate moved mid-wave: `1f2fb4f5…` → `a4768851…`
> (commits `beb04ea`, `770a69d`). Every number below is labelled with the gate it came from.
> LOG.md:1319–1320 already records that hardening as driven by three vector reports
> (`command` shadow, `head` forge, dead PATH fallback).

**Surface scored:** committed record+claims pair `corpus/fixtures/full-r6.md`
(`878c2c50…8212a`) + `corpus/fixtures/full-r6.claims.jsonl` (`45eb6ac2…dc40`), run as
`bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.md --root .. --json <scratch>/m.jsonl`
with cwd = a scratch fleet root (`research/` copied, lane cloned), `CHOUSA_NOW_EPOCH=1700000000`
so the manifest `ts` field is deterministic.

---

## 0. Verdict

| # | Claim | Result |
|---|---|---|
| **A** | The assigned matrix passes in four environments: identical exit, `VERIFY_ALL` line, manifest line count, empty tripwires | **HELD** (both gates) |
| **B** | The manifest write path is untouched by the pin: bytes identical to the clean run, modulo `ts`/`gate_sha256` | **HELD** — masked sha256 `a32567ca2da21245…0c16e` for every non-refusal environment, on both gates, cross-gate too |
| **C** | Refusal is fail-closed: exit 2, `GREP_PROVENANCE` on stderr, **no manifest written**, pre-existing manifest byte-unchanged | **HELD** (3 refusal classes) |
| **F1** | **New finding.** The manifest's own provenance stamps (`record_sha256`, `gate_sha256`) are computed by **unpinned, PATH-resolved** `sha256sum`/`cut` and are **never format-validated** — a PATH shim writes an attacker-chosen stamp with exit 0 and verdict `CLEAN`. The claims path *does* validate the same digest shape (gate:1967); the manifest path does not (gate:3668–3672). | **defect, both gates** |
| **F2** | **Calibration.** The C1 counter prints `GREP_PIN_MATCH=9/9` / `predicate_holds=true` against a gate whose matcher actually ran through a caller-supplied engine behind a `BASH_ENV command()` shadow — 25–32 intercepted calls, 20 matcher-flagged. Measured on wave-base **and** on `ctl-regressed`. Current gate serves **0** such calls, so the counter's blind spot is latent, not live. | **counter blind spot** |
| **F3/F4** | Independently reproduced two defects other seats already filed: the dead `command -v grep` PATH fallback (refuses despite a GNU grep on PATH) and the `head`-forge. Reported as **confirmation, not novelty** (see §5). | prior art |

---

## 1. The four environments (target item A)

Command shape, identical in every row except the shadow:

```
cd <fleet-root>/chousa-shokunin
env -i PATH=<env PATH> HOME=/root CHOUSA_NOW_EPOCH=1700000000 <extra> \
  bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.md --root .. --json <m.jsonl>
```

| # | environment | exit | `VERIFY_ALL` line | manifest lines | tripwire bytes | refusal |
|---|---|---|---|---|---|---|
| E1 | clean `PATH=/usr/local/bin:/usr/bin:/bin` | 0 | `VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0` | 1 | 0 | none |
| E2 | PATH shim named `grep` first (logs every call, then execs `/usr/bin/grep`) | 0 | same | 1 | **0** | none |
| E3 | `BASH_ENV` defining a logging `grep()` function | 0 | same | 1 | **0** | none |
| E4 | `PATH` = 3708-entry symlink farm (every `/usr/bin` entry except `grep`/`egrep`/`fgrep`) with **no grep at all** | 0 | same | 1 | 0 | none |
| E5 (extra) | hostile PATH `grep` that never matches | 0 | same | 1 | **0** | none |
| E6 (extra) | `RESEARCH_GATE_GREP=/usr/bin/grep CHOUSA_GREP_PIN_ECHO=1` under the E2 shim | 0 | same | 1 | 0 | none |

`RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0)` in E1–E6,
and `SECTION claims … tally=VERDICT_BEARING_CLAIMS=3/3`, `chain … RESOLVED_HOPS=3/3`,
`sweeps … VERIFIED_SWEEPS=1/2 REJECTIONS_OK=2/2`, `integrity … refs=13 resolved=12 unresolved=0`.
E6's stderr carries exactly one `GATE_GREP: path=/usr/bin/grep source=override version="grep (GNU grep) 3.12-modified"`.

Per-environment receipts: `fleet2-a4768851-*.summary` / `fleet-1f2fb4f5-*.summary` in this directory
(sha256 listed in §6). Identical results on the wave-base gate — the 5-section
`sections=5` figure differs from the round-6 receipt's `sections=4` only because `integrity` was added.

**Non-vacuity control for E5.** The hostile engine is not inert: pointed at explicitly as the pin it
makes every section drift (`VERIFY_ALL sections=5 run=5 absent=0 drift-sections=5 findings=5 drift=5`,
exit 1, manifest 786 bytes) — `fleet2-a4768851-hostile-pin.summary`. So E5's zero call count means
"never consulted", not "harmless shim".

---

## 2. Manifest bytes: untouched by the pin (target item B)

Two runs of the same surface are used: the **clean** run and each shadow run; the manifest is one
appended JSONL line per run.

```
# mask both volatile fields, then compare bytes
python3: re.sub(r'"ts":"[^"]*"', '"ts":"<M>"', re.sub(r'"gate_sha256":"[^"]*"', '"gate_sha256":"<M>"', bytes))
```

| comparison | result | masked sha256 |
|---|---|---|
| clean vs shim-path | IDENTICAL | `a32567ca2da21245d04940c87acfdfe1c2596d839f3f39af08ce0da74ac0c16e` |
| clean vs bashenv | IDENTICAL | same |
| clean vs nogrep | IDENTICAL | same |
| clean vs hostile-PATH | IDENTICAL | same |
| clean vs override+echo | IDENTICAL | same |
| clean vs hostile-pin (broken engine) | DIFFERS (verdict `DRIFT`, 786 vs 1508 bytes) — expected control | — |
| **cross-gate**: wave-base clean vs current clean | **IDENTICAL** | same |

Raw unmasked bytes are byte-identical too when `CHOUSA_NOW_EPOCH` is fixed — one sha256 per gate
across all non-refusal environments: wave-base `3c4264ad3e6a542e7de928ce01106700595be7efca3b16b7888502a30832057b`
(5 manifests), current `ddf77cff337263584b864b4eeede6d9cb081cfcf81c5577d71590215c81c35c1` (6 manifests).
`gate_sha256` is a property of the gate file, so it differs *between* gates but never within one.

**Structural reason the pin cannot touch this path:** the manifest write block (current gate
3666–3755) invokes only `sha256sum`, `cut`, `tail`, `od`, `tr`, `flock`, `printf` — **no grep**
(`grep -oE` over that block returns exactly those seven). The pin therefore cannot alter it; the
recorded *tallies* come from child gate processes, which each re-run `grep_pin_init` themselves.

**Append path also holds:** two successive runs into one manifest → 2 lines, both valid JSON; a
pre-seeded manifest with **no trailing newline** gets exactly one `\n` prepended (bytes
`… } \n {"schema"…`), so JSONL delimiting survives.

---

## 3. Refusal (target item: "refusal")

`grep_pin_init` runs after argument parsing and **before** any mode dispatch (current gate:8060;
wave-base:8039), so a refused pin cannot reach the manifest.

| case | exit | stderr | manifest |
|---|---|---|---|
| `RESEARCH_GATE_GREP=bin/grep` (relative) | 2 | `research-gate: GREP_PROVENANCE refused: override is not an absolute path (candidate=bin/grep)` | **not created** |
| `RESEARCH_GATE_GREP=/nonexistent/grep` | 2 | `… override is not a regular file (candidate=/nonexistent/grep)` | pre-existing 1-line manifest **byte-unchanged** (`ce8bb996…4ac87` before == after) |
| `RESEARCH_GATE_GREP=<stub reporting pi-uu-grep 0.2.0>` | 2 | `… override does not report GNU grep: <no version> (candidate=…)` | **not created** |

Ordering proofs: refusal beats a nonexistent record (`verify-all /nonexistent/record.md` +
bad override → the `GREP_PROVENANCE` line, not `record not found`); an unknown flag still produces
the usage error (exit 2) and `--help` still exits 0, so argument errors remain usage.

---

## 4. F1 — the manifest write path is untouched **by the pin**, and therefore unprotected

The task asked me to confirm the manifest write path is untouched by the pin. It is — and that is
exactly the problem: the pin protects `grep`, while the manifest's own revision stamps come from a
*different*, still-unpinned tool family.

**Evidence (both gates, exit 0, verdict `CLEAN`):**

```
PATH=<shim>:/usr/bin:/bin  CHOUSA_NOW_EPOCH=1700000000  bash tools/research-gate.sh \
  verify-all corpus/fixtures/full-r6.md --root .. --json <m.jsonl>
```

| PATH shim | manifest field written | real value |
|---|---|---|
| `sha256sum` printing a fixed digest (`ctl-sha256sum-shim.sh`) | `"record_sha256":"0000…0"`, `"gate_sha256":"0000…0"` | `878c2c50…`, `1f2fb4f5…`/`a4768851…` |
| `cut` printing a constant (`ctl-cut-shim.sh`) | `"record_sha256":"HOSTILE-CUT-OUTPUT"`, `"gate_sha256":"HOSTILE-CUT-OUTPUT"` | as above |
| `tail` printing nothing (`ctl-tail-shim.sh`) | *no write* — exit 2, `research-gate: manifest unreadable under lock (its last byte decides the delimiter)`, manifest byte-unchanged (11 bytes) | fail-closed ✔ |

The gate tests only emptiness, not shape (current gate:3668–3671):

```
sha_rec=$(sha256sum -- "$record" 2>/dev/null | cut -d' ' -f1 || true)
sha_gate=$(sha256sum -- "$SELF" 2>/dev/null | cut -d' ' -f1 || true)
if [[ -z $sha_rec || -z $sha_gate ]]; then … "manifest not written"; exit 2; fi
```

`"HOSTILE-CUT-OUTPUT"` is not 64 lowercase hex, yet it was accepted and the manifest stayed valid
JSON. The **claims** path refuses exactly this shape (gate:1967
`[[ $sha_actual =~ ^[0-9a-f]{64}$ ]] || sha_actual=unreadable`, fail-closed to `stale`), and the
gate's own selftest asserts the *format* of these fields (gate:5287–5288) — the runtime manifest
writer asserts only non-emptiness.

**Why it matters for this round's axes.** `gate_sha256` is the manifest's revision stamp: the field
a receipt consumer uses to bind a measurement to a gate. A one-line PATH shim lets a caller mint a
manifest that names any gate revision, with exit 0 and verdict `CLEAN`, and the grep pin (the round's
C1 claim) cannot see it. `[INFERENCE]` Severity is bounded: the shim has to be on the caller's own
PATH, i.e. the same threat class C1 already treats as hostile for `grep`; but the asymmetry
(claims digests validated, manifest digests not) is not documented anywhere in the gate.

I did **not** change the gate (read-only seat). One-line candidate fix, for the owner:
validate `^[0-9a-f]{64}$` on both captured digests and refuse (exit 2, manifest not written) —
mirroring gate:1967.

---

## 5. F2 — the C1 counter cannot see a `command()`-shadowed matcher

Method: a `BASH_ENV` file (`ctl-bashenv-command-swap.sh`) defines `command()` so that
`command /usr/bin/grep …` is served by a caller-supplied engine (`ctl-swap-engine.sh`) that
forwards to a saved copy of the real grep — **correct output**, wrong engine.

| run | gate | `GREP_PIN_MATCH` | `predicate_holds` | intercepted calls | matcher-flagged (`-a -z -b -o -P`) |
|---|---|---|---|---|---|
| K1 | **wave-base** `1f2fb4f5` | **9/9** | **true** | **25** | 7 (standalone run: 32 / 7) |
| K2 | current `a4768851` | 9/9 | true | **0** | 0 |
| K4 | **ctl-regressed** `7afd040f` | **9/9** | **true** | **25** | **20** |

K3 control (wave-base, no BASH_ENV): 9/9 — so the counter is otherwise honest.

Mechanism: the wave-base wrapper is `grep() { command "$GREP_BIN" "$@"; }` (wave-base:351); a
`BASH_ENV` function named `command` receives every pinned call. The current gate's wrapper is
`grep() { "$GREP_BIN" "$@"; }` (current:356–359), so the shadow cannot reach it — K2's 0 confirms
the fix. But the counter's S1/S2 scenarios test only *name* shadowing (a PATH `grep`, a `grep()`
function); the swap leaves the S1/S2 tripwires empty and the output reference-equal, so all nine
scenarios PASS. **K4 is the load-bearing measurement: I re-introduced only the vulnerable wrapper on
the current gate and the counter still certified it 9/9 with 20 matcher calls served elsewhere.**
The counter's 9/9 is therefore a statement about the *wrapper source*, not about which binary ran.

Not a live C1 failure: against the current gate the pin holds (K2). Prior art — `MutGrepShimEnv.md`
(P6) and four sibling reports already recorded the `command()` interception; what I add is the
counter-blindness bound (K4) and its verify-all surface.

**F3/F4 confirmations (not novelty).**
- Dead PATH fallback: wave-base:388 `c=$(command -v grep …)` can never yield an absolute path
  because the gate defines a `grep()` function, so `command -v grep` prints `grep`
  (`bash -c 'grep(){ …; }; command -v grep'` → `grep`). Confirmed end-to-end in a private
  user+mount namespace: with `/usr/bin/grep` and `/bin/grep` bind-mounted to a non-GNU stub and a
  GNU-reporting `grep` on PATH, the wave-base gate refused — `no GNU grep found at /usr/bin/grep,
  /bin/grep or on PATH` — while the PATH shim was called **0** times. The current gate deleted the
  branch and corrected the message.
- `head`-forge: a `BASH_ENV head()` returning `grep (GNU grep) 9.99-forged` made the wave-base gate
  pin a non-GNU stub (then every section DRIFT). The current gate refuses (`override does not
  report GNU grep`), using bash expansion + absolute `/usr/bin/timeout`.
- `readonly -f grep`: wave-base dies with a bare `line 351: grep: readonly function` (exit 1);
  current refuses by name (exit 2, `the grep wrapper cannot be defined (a caller marked it
  readonly)`).

---

## 6. Artifacts (this directory, all < 1 MiB)

| file | sha256 |
|---|---|
| `harness.sh` (E1–E8 battery) | `2067b72dc5629cdc9eb4eee7a7f205e3eb70757ccc3d5d59c76ec8c02d6d7bdf` |
| `harness2.sh` (override+echo, masked compare) | `fec2cf2c61f4139b56dbdcb4fc1717390a4ad7540c597a5849568e188c209d1a` |
| `harness3.sh` (two-gate battery) | `79ace782a1deaa4f02681bdaa759cd8b3fed2ad846520974186e36224a5bc110` |
| `manifest-clean-current.jsonl` | `ddf77cff337263584b864b4eeede6d9cb081cfcf81c5577d71590215c81c35c1` |
| `ctl-wrapper-regressed.diff` | `37c7671295d11e86486e77e03c5cc7fe52f494ba6ec792e35f396f691b4fe03e` |
| `ctl-bashenv-command-swap.sh` | `1b9dad98e6c68985223ea55a261ee76977ced379b1b42897c7c6846d95ad7859` |
| `ctl-swap-engine.sh` | `0b5a167488a2c06d1757d25ebd99d450f71a6a4077b8af519c9d4edc5d3c0eb5` |
| `ctl-sha256sum-shim.sh` | `49a22a8cc741fd259ad199e11069ddfc31e724cb1f53054e9b66642f6d0a362c` |
| `ctl-cut-shim.sh` | `179e1bec2662b1c2db07df20443212b7a7dd44f8df9709733542389e580216fd` |
| `ctl-tail-shim.sh` | `2e2f91b930795800066ddd4ff6c0060d3b9ba50f2455291923c039f3f6c1be5c` |
| 20 × `fleet*-*.summary` (per-environment receipts) | see `sha256sum *` in this dir |

Large clones (`fleet/`, `fleet2/`, `fleet3/`, `lane/`, `lane2/` ≈ 1.1 GB) stay in
`/tmp/hyaku/chousa-r35/w2/ExecPinModeAll/` per the artifact-size rule.

---

## 7. Limits

- Single record+claims surface (`full-r6`). It is committed and carries all five sections, but
  `verify-all`'s absent-section and DRIFT composition paths were only exercised through the
  hostile-pin control, not through a second record.
- `verify-all` is measured on this host only, where `/usr/bin/grep` is GNU 3.12; the
  no-system-grep branches were reached only via a private mount namespace (U2), and that test's
  first attempt self-recursed (my bug — the shim exec'd the bind-mounted `/usr/bin/grep`, i.e.
  itself). I killed only the PIDs I started; no other process was signalled.
- F1 is demonstrated with a hostile PATH tool, not with a real-world failure; `[INFERENCE]` its
  severity depends on whether receipt consumers treat `gate_sha256` as trustworthy.
- The lane gate moved under me mid-wave (`1f2fb4f5` → `a4768851`). Numbers are labelled per gate;
  K4's control gate is my own build (`7afd040f`, diff supplied) and is not a lane revision.
- No selftest, no counter re-baseline, no build/lint run — per the wave's gate ownership rule.
