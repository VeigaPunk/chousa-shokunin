# RevGrepModesA — pin coverage part A: `verify` / `verify-claims` under grep interception (round 35 v2 wave)

Reviewer: chousa-r35-w2-RevGrepModesA. Date 2026-10-23. Gate scored:
landed `tools/research-gate.sh` sha256
`1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`, re-derived on the landed file and on a
scratch clone at `e87c5d7ea2dbf3730b36a3961de3f06261d015e4`
(`git clone … && git checkout -q e87c5d7…`; clone sha matched before any run).
No lane production file was modified; all writes are under
`.ufo/waves/round-35/w2/RevGrepModesA/` (receipts copied from
`/tmp/hyaku/chousa-r35/w2/RevGrepModesA/`).

## What I ran

Scratch workspace `/tmp/hyaku/chousa-r35/w2/RevGrepModesA/run/` mirrors the
README-canonical layout: `run/chousa-shokunin` = the clone (lane cwd),
`run/research/` = read-only copy of the workspace `research/` sources the
committed fixtures cite. Canonical invocation (identical argv for every setup):

```
cd run/chousa-shokunin
env -u BASH_ENV -u RESEARCH_GATE_GREP -u CHOUSA_GREP_PIN_ECHO -u GREP_SHIM_LOG \
    -u GREP_BASHENV_LOG -u CHOUSA_ROOT <SETUP assignments> TMPDIR=../tmp timeout 300 \
    bash tools/research-gate.sh   verify        corpus/fixtures/full-r6.md   --root ..
env …same… bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..
```

Setups: **base** (no interception); **(a)** `PATH=<shimdir>:$PATH` where
`shim/grep` logs one line per call then `exec /usr/bin/grep "$@"` (correct
output, visible calls — the round-34 S1/S2 attack shape); **(b)**
`BASH_ENV=../bashenv.sh` defining a logging `grep()` function (delegates to
`/usr/bin/grep`); **(c)** `RESEARCH_GATE_GREP=/usr/bin/grep` with the shim
first on PATH. Tripwire = the setup's log file, per run. Instrumentation
controls prove the tripwires fire when interception happens: direct
`bash -c 'grep --version'` under (a) logged 31 bytes, under (b) 37 bytes
(`out/trip-ctl-shim.log`, `out/trip-ctl-bashenv.log`).

Driver: `run/matrix.sh` (sha256 5bcdf4d14111e820…) and `run/extra.sh`
(1707d659429e65fa…). First matrix attempt had a driver bug (env assignments
leaked into the gate's argv → "multiple record paths" rc=2; a symlinked lane
cwd broke `--root ..` resolution → DRIFT baselines). Those runs are invalid and
were fully superseded by the fixed matrix; nothing about the gate is concluded
from them.

## Results — the requested matrix

Baselines (unshimmed): `verify` → exit 0, `RESEARCH_GATE: CLEAN (findings=0
drift=0 questions=1 sources=4 chains=3 claims=3 negatives=2 rejections=2
approvals=1)` — exactly the pre-registered full-r6 expectation
(`corpus/fixtures/full-r6.README.md:180-190`, access 2026-10-23).
`verify-claims` → exit 0, `RESEARCH_GATE: CLEAN (claims=17 supported=13
contradicted=2 unsupported=2 mismatched=0 …)` — the exact counts
claims-r2.README.md registers (`:64-66`). `out/base-verify.out`
(cd5bfc56ce86c7b6…), `out/base-claims.out` (7d63b39a8877acb6…).

| setup | mode | exit | tripwire bytes | verdict == unshimmed byte-for-byte |
|---|---|---|---|---|
| base | verify / claims | 0 / 0 | n/a | reference |
| (a) PATH shim | verify / claims | 0 / 0 | **0** / **0** | **YES** (verdict line raw-equal; full stdout+stderr equal after masking only the declared-volatile `ts=` token) |
| (b) BASH_ENV grep() | verify / claims | 0 / 0 | **0** / **0** | **YES** (same rule) |
| (c) override + shim | verify / claims | 0 / 0 | **0** / **0** | **YES** (same rule) |

Raw diff of baseline vs (a) verify is exactly the timestamp token (`1c1
…ts=…`, `out/diff-a-shim-verify.out`); same for (c) claims. The verdict line
itself compares byte-equal with no normalization. Pin provenance
(`CHOUSA_GREP_PIN_ECHO=1` runs, `out/e-*.err`): (a) and (b) pin
`path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"`;
(c) `source=override`. The shim on PATH is never resolved because
`grep_pin_init` probes `/usr/bin/grep`, `/bin/grep` before the PATH fallback
(research-gate.sh:385-393 in the clone).

## Findings

- **F1 — info (claim confirmation, this slice).** Under all three interception
  setups, both modes keep exit 0, an empty tripwire, and byte-identical
  (mod `ts=`) output. The S1/S2 shortcut surface and the S3 PATH dependency
  (`nogrep`: PATH with 3705 coreutils entries and zero grep entries still runs
  both modes CLEAN, `out/nogrep2-*.out`) are closed at `verify` /
  `verify-claims`. No MEETS-killer found in this slice: no scored engine
  behaves 9/9-here-but-shimmed-there, and nothing "separates nothing".
- **F2 — notable, inside the frozen limit (not a kill).** `RESEARCH_GATE_GREP`
  accepts an absolute shim that merely delegates:
  `RESEARCH_GATE_GREP=<shim>/grep` pins it (`GATE_GREP: path=…/run/shim/grep
  source=override version="grep (GNU grep) 3.12-modified"`), the gate then
  runs attacker-chosen code on every matcher call (claims-mode tripwire 9694
  bytes, verify 723 bytes, `out/trip-pinshim-*.log`) while stdout stays
  byte-equal to baseline with the echo off (default). This is exactly the
  declared limit in `corpus/evidence/round35/claims.md` (C1: "Provenance is
  self-reported…"), so it cannot kill P1 — but it means the pin's guarantee is
  "one resolution + GNU-grep self-report", not "GNU grep inode ran". The echo
  is the only output-level tell and it is off by default.
- **F3 — edge note (fail-closed, exit-contract wrinkle).** A `BASH_ENV` that
  marks its `grep()` `readonly -f` makes the gate's own redefinition
  (research-gate.sh:351) abort under `set -euo pipefail` (line 292):
  `line 351: grep: readonly function`, exit 1, empty stdout, empty tripwire
  (`out/b-readonly-claims.*`). No silent bypass — but the exit is 1 with no
  `RESEARCH_GATE:` line, which the contract documents as DRIFT, not refusal.
  Attacker-induced via caller env; absence of a verdict is the tell. Not a
  defect in the pin claim.

## Residual risk and verification gaps

- Only `verify` and `verify-claims` exercised; `selftest`, `verify-all`,
  `verify-chain/sweeps/integrity/metadata`, `--pin/--drift` not run here (the
  selftest re-execs `bash "$SELF"`, which under BASH_ENV re-sources the
  attacker file in children — untested in this slice).
- Byte-equality is against my reconstructed root: fixture bytes are committed
  clone bytes at e87c5d7, and `research/` is a byte copy of the workspace
  sources (spans verify CLEAN, so content is where it matters), but I did not
  sha-compare the copies file-by-file.
- Tripwires prove *interception*, not exhaustive call-site coverage — the
  9-call-site enumeration is C1 counter territory (out of my item).
- Environment coverage: one host, bash 5.3.20, GNU grep 3.12-modified; no
  `CHOUSA_ROOT`-env interplay, no exported-function vector beyond BASH_ENV
  (bash re-sources BASH_ENV per child, which the readonly probe exercised).

**Verdict for my item:** pin coverage holds for `verify` and `verify-claims`
under PATH shim, BASH_ENV function, and pinned-override-plus-shim; tripwires
empty, verdicts byte-equal, exit codes unchanged. Recommend P1 keeps its 9/9
standing on this slice; F2 should stay listed as the known, documented limit.

Artifacts: `out/` (114 receipts, per-run `.out/.err/.rc` + `trip-*.log` +
`manifest.txt` with sha256), drivers `matrix.sh`/`extra.sh`, probes
`shim/grep`, `bashenv.sh`, `bashenv-ro.sh`. Large/intermediate logs stayed in
`/tmp/hyaku/chousa-r35/w2/RevGrepModesA/`. No tool installs were needed; no
pacman, no network, no subagents, no signals beyond my own `timeout` children.
