# RevGrepModesB — pin coverage, part B: verify-chain / verify-sweeps / verify-integrity

Date: 2026-10-23. Seat: chousa-r35-w2-RevGrepModesB (leaf, no subagents).
Gate scored: `tools/research-gate.sh` sha256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`
(re-derived `sha256sum` at run time; = landed round-35 gate).
Wave base: e87c5d7ea2dbf3730b36a3961de3f06261d015e4.

## Method — the three shadow environments

Same three shadows as the C1 counter scenarios S1–S3
(`corpus/evidence/round35/c1-count.py`, accessed 2026-10-23), each run also with
`CHOUSA_GREP_PIN_ECHO=1` so the pin is observable on stderr:

- **S1 shim-first PATH**: `$W/shimbin:/usr/local/bin:/usr/bin:/bin`, where
  `shimbin/grep` is an executable that appends `"$*"` to `trip-path.log` then
  `exec /usr/bin/grep "$@"` (mirrors `write_shim` in c1-count.py).
- **S2 BASH_ENV function shim**: `BASH_ENV=$W/bash_env.sh` defining
  `grep() { printf 'fn %s\n' "$*" >>trip-fn.log; command /usr/bin/grep "$@"; }`,
  PATH clean (mirrors `write_bash_env`).
- **S3 grep absent from PATH**: `PATH=$W/nogrepbin`, a 47-entry symlink farm of
  real tools (bash, sh, sed, awk, find, stat, realpath, sha256sum, …) with **no**
  `grep` entry (mirrors `build_nogrep_path`/`NOGREP_TOOLS`).

Every run was `env -i HOME=/nonexistent CHOUSA_GREP_PIN_ECHO=1 <env> bash
tools/research-gate.sh <mode> <fixture> --root ..` from the lane cwd
(`/home/vgpnk/Projects/shokunin/chousa-shokunin`), matching the round-1
convention (`corpus/fixtures/chain-r3.README.md`, "the re-run passes `--root ..`").
Reference runs used clean PATH only. Driver + logs:
`/tmp/hyaku/chousa-r35/w2/RevGrepModesB/{run.sh,logs/}`.

## Fixtures (committed, cited)

| mode | fixture | spec | expected |
|---|---|---|---|
| verify-chain | `corpus/fixtures/chain-r3.md` | `corpus/fixtures/chain-r3.README.md` | `RESOLVED_HOPS=17/22`, CLEAN, exit 0 |
| verify-sweeps | `corpus/fixtures/sweeps-r5.md` | `corpus/fixtures/sweeps-r5.README.md` | `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3`, CLEAN, exit 0 |
| verify-integrity | `corpus/fixtures/integrity-r7.md` | `corpus/fixtures/integrity-r7.README.md` | `INTEGRITY refs=16 resolved=15 unresolved=0`, CLEAN, exit 0 |

Cited sources are the round-1 archives `research/deep-research-2026-09-28/{A,B,C}*.md`
(fleet root, verified present) plus `chousa-shokunin/corpus/knowledge/archived-export-intake.md`.

## Results — per mode, per shadow

Reference (clean env): all three modes exit 0, CLEAN, expected summary lines.
Echo on stderr of **every** run: `GATE_GREP: path=/usr/bin/grep source=default
version="grep (GNU grep) 3.12-modified"`.

| run | exit | tripwire | stdout vs reference | pin reached |
|---|---|---|---|---|
| S1 verify-chain | 0 | trip-path.log never created | byte-identical (mod ts line 1) | yes, `source=default` |
| S1 verify-sweeps | 0 | never created | identical | yes |
| S1 verify-integrity | 0 | never created | identical | yes |
| S2 verify-chain | 0 | trip-fn.log never created | identical | yes |
| S2 verify-sweeps | 0 | never created | identical | yes |
| S2 verify-integrity | 0 | never created | identical | yes |
| S3 verify-chain | 0 | n/a | identical | yes — pin survived a PATH with no grep |
| S3 verify-sweeps | 0 | n/a | identical | yes |
| S3 verify-integrity | 0 | n/a | identical | yes |

Tripwire evidence: `ls -la trip-path.log trip-fn.log` → "No such file or
directory" — the shims were **never executed**, so they were never even created
(the shim writes the file on first call). Stronger than "0 bytes".
Verdict identity: `diff <(tail -n+2 ref.out) <(tail -n+2 sN.out)` is empty for
all 9 shadow runs; only the `ts=` header line differs (timestamp).

Mode verdict lines observed: `RESOLVED_HOPS=17/22`,
`RESEARCH_GATE: CLEAN (hops=22 verified=17 exempt=5 ...)`;
`VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3`, `RESEARCH_GATE: CLEAN (sweeps=2
verified=1 exempt=1 ...)`; `INTEGRITY refs=16 resolved=15 unresolved=0`,
`RESEARCH_GATE: CLEAN (refs=16 resolved=15 unresolved=0 exempt=1 ...)`.

## Pin reachability — static + dynamic proof

`grep_pin_init` is invoked at `tools/research-gate.sh:8039`, **before** the mode
dispatch `case "$MODE"` (~line 8056) that routes `chain`/`sweeps`/`integrity`
(8056–8078). The comment at 8036–8038 states the intent: "Resolve the grep pin
before any mode reads a record". Dynamic proof it gates mode work:

```
env -i PATH=/usr/bin:/bin RESEARCH_GATE_GREP=bin/grep \
  bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..
→ rc=2, stderr: research-gate: GREP_PROVENANCE refused: override is not an absolute path (candidate=bin/grep)
→ zero record output (stdout empty)
```

So for all three modes the pin is reached before any record is read; a refused
pin never produces a verdict. No mode reached a matcher with an unpinned grep:
every `grep` call in the gate is the wrapper `grep() { command "$GREP_BIN" "$@"; }`
(line 352 area), and the S3 farm proves the gate needs no PATH-resolved grep.

## Findings

No defect found in scope. All three modes: exit correct, tripwires empty,
verdict byte-identical to reference, pin reached (echo `source=default`,
`/usr/bin/grep`) before mode work, refusal exits 2 pre-record in the probed
mode (verify-chain; identical `grep_pin_init` ordering covers all modes).

Residual gaps (not defects): (a) echo was ON in my runs — stderr carries the
`GATE_GREP:` line; counter-style echo-off runs are covered by ExecPinMode*
siblings. (b) S3 farm has 47 tools, not the full counter set minus grep —
sufficient for these modes, which completed with identical output. (c) Only the
positive fixtures were run; broken twins (`chain-r3-broken.md`,
`sweeps-r5-broken.md`, `integrity-r7-broken.md`) were not exercised under
shadows — the pin precedes record reads, so DRIFT-path coverage adds nothing
about pin reachability, but a sibling could run them cheaply if wanted.
(d) Provenance is self-reported `--version` text, as the gate's own comment
admits (tools/research-gate.sh:~349); a binary lying about being GNU grep is
out of scope per claims.md C1 limit.

## Artifacts

- Driver/envs/logs: `/tmp/hyaku/chousa-r35/w2/RevGrepModesB/` (run.sh,
  shimbin/grep, bash_env.sh, nogrepbin/, logs/{ref,s1,s2,s3,refuse}-*.{out,err,rc})
- No installs. No lane/git writes (gate runs are read-only; `git status` shows
  only pre-existing ` M corpus/QUALITY.md`, ` M corpus/SOURCES.md` and sibling
  `??` dirs — not mine).
