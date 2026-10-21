# FRegistryRegistryNul — C3 NUL-containing registry refusal (round 26, attempt 1)

Seat: `ChousaR26R.FRegistryRegistryNul` (scout, author-lane advice only; no outside judge).
Target: the C3 spec line "unreadable/refused FILE ... exits 2", narrowed to a
NUL-containing `--registry` FILE (`corpus/evidence/round26-claims.md:90-93`).

## Revisions and identity

- Measured revision: `0e9784bd52eca456b24d0bc40921480a47f91a2b` (from
  `corpus/evidence/round26-measured-revision.json`); lane `HEAD` was observed at the same commit.
  Claim base: `ba3333254dd337658a4f25e7a9471f9cf4e4567e` (not run).
- Sandbox: `git archive 0e9784bd… | tar -x -C /tmp/chousa-r26-falsify-FRegistryRegistryNul/tree` exited 0.
  `sha256sum tree/tools/research-gate.sh` gives
  `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`, which equals the pinned input hash.
- Runtime: GNU bash 5.3.20(1)-release, Linux x86_64.
- Fixtures live only in `/tmp/chousa-r26-falsify-FRegistryRegistryNul/work`. Each run is
  `env CHOUSA_STRICT=0 CHOUSA_ROOT=$W bash tree/tools/research-gate.sh verify-metadata <entry> --root $W --registry <F>`,
  unless stated otherwise. The entry is `corpus/knowledge/e-ok.md`, with
  `source: S001 …` / `verified-at: 2026-10-20 checked the claim` / `recheck: 90d`.
- No selftest, build, lint, formatter, mutation or 8MiB amplification probe was run.
  No tools were installed. GNU `time` (`/usr/bin/time`) is absent, and pacman is paused,
  so it was not installed. Elapsed time comes from the bash `time` builtin, and RSS was not measured.

## Code under attack (observed)

`metadata_registry_load` (`tools/research-gate.sh:2361-2470`) checks the file in this
order: denylist, then open, then fd denylist, then stat, then multilink, then size. It
then reads the file once with
`IFS= read -r -d '' -n $((SOURCE_READ_MAX_BYTES+1)) content`. The refusal rules after
that read are:

- length > cap → `size`;
- read rc 0 (the NUL delimiter was hit) → `nul`;
- any other rc ≠ 1 → `read`.

Any refusal goes to `die_usage` (`:390`), which writes to stderr and exits 2. The load
runs at `:2570-2574`, before the per-entry loop and before any stdout. The selftest
control is `metadata-registry-refused-nul` (`:6233-6237`).

## Results — claim holds (negative controls behave as specified)

The positive control `r-good.md` exited 0, printing 4 stdout lines with
`RESEARCH_GATE: CLEAN (… findings=0 drift=0)`.

Every NUL fixture below exited **2** with **0 stdout lines** and **0
`RESEARCH_GATE:` lines**. The first stderr line is listed for each.

| fixture | shape | rc | stderr reason |
|---|---|---|---|
| f01 | selftest shape: header, separator, `\0` | 2 | `metadata registry refused: nul` |
| f02 | single `\0` byte | 2 | nul |
| f03 | valid table that would pass clean, plus a trailing `\0` | 2 | nul |
| f04 | `\0` inside a status cell (`mi\0ned`) | 2 | nul |
| f05 | `\0` after the table has ended (in the region the parser skips via `break`) | 2 | nul |
| f06 | leading and trailing `\0\0` | 2 | nul |
| f07 | UTF-16LE encoding of the valid table | 2 | nul |
| f08 | CRLF table plus `\0` | 2 | nul |
| f09 | symlink to f03 | 2 | nul |
| f12 | `\0` first, then a valid table | 2 | nul |
| f13 | `\0` just before a closing pipe | 2 | nul |
| f20 | invalid UTF-8 plus `\0`, run under `LC_ALL=en_US.UTF-8` | 2 | nul (the function-local `LC_ALL=C` holds) |
| f03 under `LC_ALL=en_US.UTF-8` | — | 2 | nul |
| f03 with `CHOUSA_STRICT=1` | — | 2 | nul |
| f03 with `--as-of 2026-10-21`, in either flag order | — | 2 | nul (C2 composition does not mask it) |
| f03 with a directory PATH (`corpus/knowledge`) | — | 2 | nul |
| f03 with an absolute registry path | — | 2 | nul |
| f01 with the S999 entry | — | 2 | nul (refusal happens before any entry finding) |
| f21 | exactly 8,388,608 B (the cap) with `\0` as the final byte | 2 | nul (0.069 s real) |

Precedence controls also behave as specified, each exiting 2 with no stdout:

- f10, a hard link (2 links) to a NUL file, is refused as `multilink`.
- f11, a 9 MiB sparse all-NUL file, is refused as `size`.
- f22, cap+1 bytes ending in `\0`, is refused as `size`.
- f19, `--registry /dev/stdin` fed by a pipe, is refused as `metadata registry is not a regular file`.
- f17, `verify --registry f03`, is refused as `--registry is only valid with verify-metadata`.

I could not falsify the claim for any single `--registry` NUL-containing FILE.

## Findings

**F-R26-RNUL-1 — low, grammar/relation (observed). A repeated `--registry`
silently discards an earlier refused FILE.** The parser at `:6272-6274` overwrites
`REGISTRY_ARG` each time the flag appears, and only the last value is loaded.

- `--registry r-f03-trailing-nul.md --registry r-good.md` exits **0**:
  `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)`. The NUL
  registry produces no refusal.
- With the S999 entry, the same order exits **1** with
  `META_SOURCE_ROW_MISSING … source_id=S999`. So the last registry really was
  loaded, and the first was ignored.
- The reverse order (good first, NUL last) exits 2 with `refused: nul`.
- The same masking applies to the other refusal reasons:
  `--registry /nonexistent.md --registry r-good.md` exits 0, and
  `--registry r-f10-hardlink.md --registry r-good.md` (multilink) exits 0.

This counterexample is reachable through syntax the parser accepts, and it
contradicts the literal spec "unreadable/refused FILE … exits 2". It also cuts
against the "Neither flag is silently ignored" wording (`round26-claims.md:155`).

Calibration: spec v1 grammar is a single `--registry FILE`, and last-wins is
lane-wide behavior rather than a C3 regression. These all exit 0 the same way:
`--root /nonexistent --root $W`, `--as-of 2026-02-30 --as-of 2026-10-21`, and
`--record a.md --record b.md` (which reports only on `b.md`). The code's own comment
(`:6303-6307`) refuses last-wins only for `--pin`/`--drift`.

[INFERENCE] Severity is low because exploiting this requires the caller to pass two
registries. For the same reason, the `--as-of` repeat is a matching C2 counterexample
to "calendar-invalid value exits 2". That is outside this seat's target, so I am only
noting it for the C2 seats.

**F-R26-RNUL-2 — info, observed (exit contract holds).** When the registry path is
`/proc/self/environ`, `readlink -f` resolves it to the dead readlink child's
`/proc/<pid>/environ`. The `exec {registry_fd}<"$canon"` at `:2377` then fails and
leaks a raw bash error to stderr:
`research-gate.sh: line 2377: /proc/1783441/environ: No such file or directory`.
That line comes before `metadata registry refused: unreadable`; the run still exits 2
with no stdout. This is cosmetic only. The NUL path is not reached through `/proc/self`,
so this run does not show a `/proc` NUL case.

## Not established / remaining unknowns

- A file that grows between `stat` and `read` (a NUL appended after the size probe)
  was not exercised. By code reading, `-n cap+1` still bounds the read and stops at a
  NUL; this is unrun.
- No mutation clone was run, because my item names only fixtures. So I am not claiming
  that these fixtures kill a disabled-`nul` branch under QUALITY criterion 17. By code
  reading, if the `read_rc == 0` arm were removed, f03 would parse a valid table and
  exit 0 instead of 2. That makes f03 a candidate killing control, but this is
  [INFERENCE], unrun.
- None of this concerns citation truth or field readiness. A NUL refusal is a reader
  guard, not criterion-6 support.

## Exact commands and exits (summary)

- `git archive 0e9784bd52eca456b24d0bc40921480a47f91a2b | tar -x -C …/tree` exited 0.
- `sha256sum …/tree/tools/research-gate.sh` exited 0 and matched the pinned hash.
- Fixture batch 1 printed every row above. The shell exited 1 only because of the
  last `[[ -n $out ]]` test, not a fixture failure. One mis-built fixture
  (`run f03-strict env …`, where `env` was passed as a positional argument) exited 2
  with `multiple record paths`. That was my invocation error, not a product result,
  and the corrected rerun (`CHOUSA_STRICT=1`) is in the table.
- Fixture batch 2 and the cap batch exited 0.
- The first cap attempt returned rc=127 because `/usr/bin/time` was absent, and was
  rerun with the bash `time` builtin.
- Fixture SHA-256s, e.g. f01 `2b27ac6d…afa0e`, f03 `43885c52…cf67`, f21 `94f9b539…abb3`,
  are recorded in sandbox `sha256sum r-*.md` output.
