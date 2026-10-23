# RevGrepModesC — pin coverage, part C (verify-metadata / verify-all / --pin / --drift / --selftest)

Wave: round-35 w2. Seat: reviewer. Date: 2026-10-23. Timebox kept (~30 min).
Gate scored: scratch clone `/tmp/hyaku/chousa-r35/w2/RevGrepModesC/repo` at wave base
`e87c5d7ea2dbf3730b36a3961de3f06261d015e4`; gate sha256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`
(matches landed `tools/research-gate.sh`; verified `sha256sum` on both paths, receipt: `RevGrepModesC/` copy `sha.txt` content quoted in artifact-sha256.txt).
Base gate used for comparison only: `.ufo/waves/round-35/repairs/base-gate.sh` sha256 `a6307edf…2995b` (verified).

## Shadow environments (same three as RevGrepModesA) + clean baseline

All runs under `env -i` with `PATH=/usr/bin:/bin TMPDIR=$S/tmp HOME=$S` (S=/tmp/hyaku/chousa-r35/w2/RevGrepModesC):

- `e0` baseline: nothing shadowed.
- `ea` PATH shim: `PATH=$S/shim:…`; `shim/grep` logs argv to `logs/shim-tripwire.log` then `exec /usr/bin/grep` (sha256 `33f9ab38…`).
- `eb` BASH_ENV: `BASH_ENV=$S/binenv/bashenv.sh` defines `grep(){ log; command grep "$@"; }` (sha256 `6ceb0a74…`).
- `ec` override+shim: `RESEARCH_GATE_GREP=/usr/bin/grep` plus the `ea` shim on PATH.

Note: the ambient harness shell carries a `grep` *builtin* (`pi-uu-grep 0.2.0`; `type grep` → "grep is a shell builtin"), so `env -i` was mandatory to control resolution. Builtins are not exported to `bash file` children, so ambient mode is also safe — verified ambient selftest below.

## Matrix results (all modes)

Commands (cwd = clone root), each run with `CHOUSA_GREP_PIN_ECHO=1` unless noted:

```
bash tools/research-gate.sh verify-metadata corpus/SOURCES.md --registry corpus/SOURCES.md --as-of 2026-10-23   # spec-literal PATH=SOURCES.md
bash tools/research-gate.sh verify-metadata corpus/knowledge   --registry corpus/SOURCES.md --as-of 2026-10-23   # directory mode, registry exercised
bash tools/research-gate.sh verify-all corpus/fixtures/full-r6.md --json $S/out/$ENV/m.jsonl
bash tools/research-gate.sh --pin   $S/out/$ENV/baseline.txt      # ECHO=0 (canonical contract)
bash tools/research-gate.sh --drift $S/out/$ENV/baseline.txt      # ECHO=0
bash tools/research-gate.sh --selftest                            # ECHO=1
```

PUT 54.=54.:
2. **Refused override exits 2 before case 1.** `--selftest` with `RESEARCH_GATE_GREP` ∈ {`/bin/false`, `binenv/notgnu` (prints `pi-uu-grep 0.2.0`), `relative/path`, `/nonexistent/grep`} → each `rc=2`, stdout **0 bytes**, `0` `ok-case`/`FAIL-case` lines; stderr exactly `research-gate: GREP_PROVENANCE refused: …` (four distinct reasons). `grep_pin_init` runs before `run_selftest`'s first `mktemp`, so nothing of the battery starts. `--pin` is likewise fail-closed: `RESEARCH_GATE_GREP=/bin/false bash gate --pin X` → `rc=2`, refusal message, **no baseline written** — the parent's `grep_pin_init` (:8039) refuses before `run_pin` spawns its inner child (which would refuse identically, since every child re-runs the pin).

**Cross-env drift, echo off (measured).** `--drift out/e0/baseline.txt` under ea/eb/ec with `CHOUSA_GREP_PIN_ECHO` unset: `GATE_DRIFT: none`, rc=0 in all three. With echo set it reports `GATE_DRIFT: +LINE` rc=1 — see F1.
**Refused pin mode (measured).** `RESEARCH_GATE_GREP=/bin/false bash tools/research-gate.sh --pin X` → rc 2, `research-gate: GREP_PROVENANCE refused: override does not report GNU grep: false (GNU coreutils) 9.12`, and no baseline file written — the parent's `grep_pin_init` (:8039) refuses before `run_pin`/its inner child runs, so pin/drift are fail-closed before fixture creation.

Per-env rc file: `out/{e0,ea,eb,ec}/rcs.txt` — identical in all four envs:

| mode | rc (all envs) | verdict tail |
|---|---|---|
| verify-metadata SOURCES.md | 1 | `META entry=SOURCES.md source=absent … verdict=drift`; `METADATA_COMPLETE=0/1` (SOURCES.md has no metadata header — spec-literal run) |
| verify-metadata corpus/knowledge | 1 | `METADATA_COMPLETE=37/41`; `DRIFT (entries=41 complete=37 findings=61 drift=6)`; `due=…`/`freshness=` columns exercised by `--as-of` (e.g. `line-binding-r31.md due=2027-10-23 freshness=current`); registry fired (`S029`/`S033` rows in `metadata-screen-r25.md` produced no ROW_MISSING → row found; 25 `META_SOURCE_NO_ROW_ID` are headerless-source entries) |
| verify-all full-r6.md | 1 | `RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=3 findings=11 drift=11)` — POINTER_UNRESOLVED for `research/deep-research-2026-09-28/*` (fixture's pointers absent under clone root); identical in all envs |
| --pin | 0 | `GATE_PIN: ok path=… gate_sha256=1f2fb4f5…` |
| --drift (own env's baseline) | 0 | `GATE_DRIFT: none` in e0/ea/eb/ec |

**Byte-identity (the pin question).** For every mode, stdout is `cmp`-identical to e0 in ea/eb/ec; stderr is identical except the `GATE_GREP:` echo line (which differs only in `source=default` vs `source=override` for ec). `m.jsonl` and `baseline.txt` are byte-identical across all four envs (baseline sha256 `028a64ed…`; m.jsonl `cbb38a90…`). Tripwires: `logs/shim-tripwire.log` and `logs/bashenv-tripwire.log` **never existed** after all runs — neither the PATH shim nor the BASH_ENV function was invoked once, in any mode, including every selftest child.


## --selftest: the important mode

`run_selftest` is entered *after* `grep_pin_init` (tools/research-gate.sh:8039 → case dispatch :8053), and children are invoked as `bash "$SELF" …` (:4184, :4221, :5247, :5601 …) so each re-runs the full pin path.

1. **Pin is re-resolved per child.** Probe: `RESEARCH_GATE_GREP=$S/binenv/loggrep2` — a wrapper that appends `argv=…` to `logs/loggrep2.log` then `exec /usr/bin/grep "$@"` (reports GNU grep → accepted; sha256 `e619a424…`). One `--selftest` (env -i + `LANG=en_US.UTF-8`, ECHO=1): **PASS 256/256**, `grep -c 'argv=--version' logs/loggrep2.log = 348` → 348 distinct gate processes ran `grep_pin_verify` (one `--version` each = one `grep_pin_init` each), and **1781** total invocations of the pinned binary (every grep in every child went through the pin). Visible echoes: exactly one `GATE_GREP:` line on the parent's own stderr (`path=…/binenv/loggrep2 source=override`); child echoes appear inside captured child dumps — 10 occurrences of `GATE_GREP:` in the selftest stdout, each inside a `    | `-prefixed dump of a failing case's `out=$(… 2>&1)` (e.g. out/e0/selftest.stdout:22 shows the child's `GATE_GREP: … source=default`). Under `ec`, those in-dump lines say `source=override` → children re-resolve the inherited override rather than reusing a parent value.
2. **Refused override exits 2 before case 1.** `--selftest` with `RESEARCH_GATE_GREP` ∈ {`/bin/false`, `binenv/notgnu` (prints `pi-uu-grep 0.2.0`), `relative/path`, `/nonexistent/grep`} → each `rc=2`, stdout **0 bytes**, `0` `ok-case`/`FAIL-case` lines; stderr exactly `research-gate: GREP_PROVENANCE refused: …` (four distinct reasons). `grep_pin_init` runs before `run_selftest`'s first `mktemp`, so nothing of the battery starts. Same for a refused `--pin` child: `RESEARCH_GATE_GREP=/bin/false bash gate --pin X` → the inner `verify-all` child exits 2 → `GATE_CAP_RC=2` → `--pin canonical capture failed (rc=2 …)` exit 2.
3. **Result under each shadow:** `--selftest` FAIL (10/256) under `env -i` in e0/ea/eb/ec — identical fail sets (normalized diff: ea/eb byte-identical to e0; ec differs only in `source=override` inside dump lines). Under ambient env and under `env -i LANG=en_US.UTF-8`: **PASS (256 cases, 0 skipped)**, rc=0, ~39 s. The 10 failures are *not* a landed regression: base gate (`a6307edf`) under `env -i` fails the **same 10 plus 2 more** (`claims-lane-fallback`, `ptr-lane-abs` — those two are artifacts of running the base *blob* outside the lane: `LANE_ROOT` at :313 resolves `.ufo/waves/…/repairs/..` → `PROVINCE.md` missing; the landed clone at its natural path passes them).

## Findings

- **F1 (minor defect, pin/drift):** `CHOUSA_GREP_PIN_ECHO=1` leaks into `--pin` receipts. `gate_canonical_capture` (:3859-3878) redirects the inner child's stderr into `capture.txt` (`>capture.txt 2>&1` at :3865) and `env -u` at :3862 unsets only five `CHOUSA_*` vars, not `CHOUSA_GREP_PIN_ECHO`. With echo on, the child's `GATE_GREP: path=… source=…` line is written verbatim into the baseline's canonical block (verified: `out/e0/baseline-echo.txt` line 9) and is *not* in `volatile_fields` (`ts gate_sha256`, :3778) nor masked by `gate_drift_normalize`. Consequences measured: `--drift` against an echo-off baseline under echo-on → `GATE_DRIFT: +LINE` rc=1 in ea/eb/ec; a baseline pinned under `source=override` would differ under `source=default`. The gate comment (:345) claims echo keeps "every existing mode" byte-identical — true only for modes that don't capture children into receipts. Not C1-blocking (the frozen counter does not set ECHO, and receipts it reads are unaffected), but any human who flips ECHO for debugging silently poisons pin/drift comparability. Fix shape: unset `CHOUSA_GREP_PIN_ECHO` in the capture's `env -u` list, or mask `^GATE_GREP:` in `gate_drift_normalize`.
- **F2 (pre-existing latent defect, flagged, not landed-caused):** the selftest is not locale-hermetic. Under `env -i` (C locale), 10 cases fail on both base and landed gates: the `claims-pass` P4 span is written into the JSONL as the escape `\u2192` (:4119), and a minimal repro —
  `printf … '{"id":"P4","source":"claimsrc/arrow.md","span":"arrow check \u2192 done","expect":"supported"}'` then `env -i PATH=… bash GATE verify-claims f.jsonl` — prints `CLAIM id=P4 … observed=unsupported verdict=mismatch` under C locale but `verdict=match` under `LANG=en_US.UTF-8`, **identically on base and landed**. So `\uXXXX` unescaping for non-ASCII spans is locale-dependent upstream of the matcher (the matcher itself pins `LC_ALL=C`, :1700-1701). Real-corpus impact: any claims file carrying `\uXXXX` escapes for non-ASCII bytes verifies differently by ambient locale. Worth a routed repair (unescape to explicit bytes, locale-free).
- **F3 (observation):** `verify-metadata corpus/SOURCES.md --registry corpus/SOURCES.md` (the spec-literal reading; the flag string omitted a positional PATH) treats SOURCES.md as one metadata entry and correctly reports all-keys-absent. The registry is *also* loaded and works (directory run over `corpus/knowledge/` resolved S-ids). No refusal, pin reached first in all cases.

## Verdict

For all five modes under all three shadow environments: the pin resolves **before** any record/case work, the PATH shim and the BASH_ENV `grep()` are **never invoked** (tripwire files absent), output is **byte-identical** to the clean baseline (modulo the intended `source=` field of the opt-in echo), `RESEARCH_GATE_GREP` is honored with `source=override`, bad overrides are refused exit-2 ahead of case 1 (0 bytes of case output), and `--selftest` re-resolves the pin in every one of its 348 child/grandchild gate processes. Nothing here meets a kill rule; F1/F2 are reportable defects outside the C1 predicate's scored surface.

## Evidence index

Scratch root `/tmp/hyaku/chousa-r35/w2/RevGrepModesC/` (logs >1 MiB stay there): `out/{e0,ea,eb,ec}/` per-mode stdout/stderr/rcs, `selftest*.stdout`, `baseline*.txt`, `m.jsonl`; `logs/loggrep2.log` (1781 pinned invocations, 348 `--version` resolutions), `logs/loggrep.log`; `mini/` locale repro; `run-matrix.sh`, `shim/grep`, `binenv/{bashenv.sh,notgnu,loggrep,loggrep2}` (shas: 33f9ab38, 6ceb0a74, ff91dca9, 38bbe884, e619a424). sha256 list of key artifacts: `.ufo/waves/round-35/w2/RevGrepModesC/artifact-sha256.txt`; per-env rc files `rcs-{e0,ea,eb,ec}.txt`; `selftest-{e0,ea,eb,ec}.tail`; `pin-baseline-e0.txt` (identical across envs). No installs; no production files touched; read-only git only.
