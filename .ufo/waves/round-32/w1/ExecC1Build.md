# ExecC1Build — round 32 W1, C1 candidate (operability: locked `--json` append)

Seat: `ChousaR32A2.ExecC1Build`. Build only; no counter was run (`c1-count.py` / `c2-count.py`
were never invoked by this seat — see "Constraints" below). Sandbox clone
`/fast/scratch/hyaku/chousa-r32/w1/ExecC1Build/gate-build` at
`4111607c857bc29ff31883bc095ae00afb527e50` (base gate SHA-256 `0bc318b3…`, verified before patching).

## 1. What changed (one file, `tools/research-gate.sh`)

`git diff --stat`: `1 file changed, 163 insertions(+), 4 deletions(-)`. Patch artifact:
`.ufo/waves/round-32/w1/ExecC1Build/c1.patch` (SHA-256 `ae1c24e3…`). Patched gate:
**SHA-256 `3144a46f443f2202e00bb96a0f0ce147beadc1cc22b87b353bcc73bb5b4884aa`**
(7141 lines; the base file is `0bc318b3…`).

1. `verify_all` `--json` block (base L3185–3203, patched L3197–3239): the probe and append are one
   critical section.

   ```bash
   if ! command -v flock >/dev/null 2>&1; then
     printf 'research-gate: flock(1) unavailable; manifest not written: %s\n' "$JSON_ARG" >&2
     exit 2
   fi
   local jfd='' jlast=''
   if ! exec {jfd}>>"$JSON_ARG"; then          # O_APPEND: create-if-absent, never truncate
     printf 'research-gate: manifest open failed: %s\n' "$JSON_ARG" >&2
     exit 2
   fi
   if ! flock -x "$jfd"; then                   # blocking exclusive lock on THAT description
     printf 'research-gate: manifest lock failed: %s\n' "$JSON_ARG" >&2
     exit 2
   fi
   if [[ -s $JSON_ARG ]]; then                  # last-byte probe under the lock
     jlast=$(tail -c1 -- "$JSON_ARG" 2>/dev/null | od -An -tx1 | tr -d ' \n' || true)
   fi
   if [[ -n $jlast && $jlast != 0a ]]; then line=$'\n'$line; fi
   if ! printf '%s\n' "$line" >&"$jfd"; then    # one line, written under the lock
     printf 'research-gate: manifest append failed: %s\n' "$JSON_ARG" >&2
     exit 2
   fi
   exec {jfd}>&-                                # releases the lock
   ```

   The r24 delimiter logic (`-s` probe, hex `od` read so a NUL last byte still counts as "not
   `\n`", `$'\n'` prefix) is byte-for-byte the same logic, now executed under the lock. The
   setup refusals (directory, non-regular, non-empty-unreadable at L3066–3072) are untouched and
   still run before any open/write. Prior bytes and the inode are never rewritten (`>>`, no
   truncation, no rename).
2. **Lock choice: unbounded blocking `LOCK_EX`.** The contract says the gate "takes an exclusive
   flock(2) … and holds it"; it names no timeout, so no retry/`-w` bound was added — a cooperating
   holder delays the append for as long as it holds, exactly what C1's L trials require (the
   counter waits 180 s for blocked waiters; a bounded lock would turn a slow holder into a
   spurious failure or a bypass). To keep the wait from being unbounded *in the selftest*, the
   selftest's own holder caps its hold at 60 s (case code below), never the gate.
3. Form: `flock -x $fd` on the fd the shell opened (util-linux fd form). The lock lands on the
   shell's own open file description, so it survives the `flock(1)` helper's exit and is released
   by `exec {jfd}>&-` / process exit. Verified standalone before patching:
   `exec {fd}>>/tmp/lkprobe; flock -x $fd` → `flock -n -x /tmp/lkprobe` from a second process
   printed "second-blocked -> holding", and "after-close: second-got-lock" once the shell closed
   the fd (`/tmp/lktest.sh`, rc 0; no file named `10` was created, i.e. the fd form really used
   the descriptor).
4. Fail-closed on a host without `flock(1)`: the gate refuses to write the manifest (exit 2,
   message above) rather than silently appending unlocked — the same shape as the existing
   `sha256sum unavailable` refusal. **Behaviour change to disclose:** a manifest open failure now
   prints `manifest open failed` instead of base's `manifest append failed` (same exit 2, same
   point in the output order).
5. Docs: header `--json` paragraph (base L196–197 → L196–203) and `usage()` (base L397–399 →
   L403–408) now state the locked, unbounded, flock(1)-requiring append.
6. Selftest: one contiguous block at the END of `run_selftest` (before `if [[ $failures -eq 0 ]]`),
   two cases, printed as 229/230 in the scratch build (integration renumbers):

   - `c1lk-holder-blocks-append` — a helper shell (`exec {fd}>>mf; flock -x $fd; printf '%s'
     '{"frag":229}' >&$fd`, then polls a release flag) holds LOCK_EX and leaves the manifest
     unterminated. The gate is launched in the background; the case polls `/proc/locks` for a
     blocked `FLOCK` waiter on the manifest inode (20 s cap) and asserts the manifest still holds
     exactly `{"frag":229}` (no append under the cooperating lock). It then creates the release
     flag, waits for both PIDs, and asserts: exit 0, 2 lines, line 1 is `{"frag":229}`, line 2 is
     the `chousa-verify-all/v1` object on its own line, no blank line, same inode, every line
     valid JSON. Skips (not fails) if `/proc/locks` or `flock(1)` is absent.
   - `c1lk-second-append` — the lock is released after the write: a second `verify-all` on the
     same manifest appends its own line (2 schema lines, no blank line, same inode, final newline,
     both runs exit 0, each run bounded by `timeout 120`).

## 2. Evidence (all commands run from the sandbox clone unless stated)

| # | Command | Result |
|---|---|---|
| 1 | `git clone … && git -C gate-build checkout -q 4111607c…` | `HEAD=4111607c857bc29ff31883bc095ae00afb527e50`; `sha256sum tools/research-gate.sh` = `0bc318b3…` |
| 2 | `TMPDIR=$PWD/tmp timeout 1800 bash gate-build/tools/research-gate.sh --selftest` (base, before any edit) | rc=0, `RESEARCH_GATE_SELFTEST: PASS (228 cases, 0 skipped)` — artifact `selftest-base.log` (SHA-256 `00d3042d…`) |
| 3 | same, patched gate, run 1 | rc=0, `PASS (230 cases, 0 skipped)`, cases 229 and 230 `ok-case … exit=0` — `selftest-patched.log` (`9bade70d…`) |
| 4 | same, patched gate, run 2 | rc=0, `PASS (230 cases, 0 skipped)`; log is **byte-identical** to run 1 (`9bade70d…`) — `selftest-patched-run2.log` |
| 5 | base vs patched case-line diff (`sed -E 's/^ok-case +[0-9]+ /ok-case /'`, compare) | `228a229,230` only — every one of the 228 base case lines (all `ok-case`, no `FAIL`/`skip`) is identical; only the two new cases are added |
| 6 | in-tree control: clone at 4111607c + this patch **minus the `flock -x "$jfd"` guard**, `--selftest` | rc=1, `FAIL (1/230 cases)` — exactly `c1lk-holder-blocks-append  gate-not-blocked-on-lock`; case 230 passes there (no lock to leak) — `selftest-control-nolock.log` (`256d9204…`) |
| 7 | patch portability: base file from `git show HEAD:tools/…` in a fresh repo, `git apply --check c1.patch && git apply c1.patch` | `patch-applies-clean-vs-base`; resulting file `sha256sum` = `3144a46f…` (byte-identical to the built gate) |
| 8 | `bash -n` on patched gate and on both control copies | syntax OK |
| 9 | no-harm A/B (lane cwd, read-only): `verify-claims corpus/fixtures/claims-r2.jsonl --root .` and `verify-chain corpus/fixtures/chain-r3.md|chain-r3-broken.md --root .` on base vs patched | **identical on both**: claims `VERDICT_BEARING_CLAIMS=0/17` DRIFT; chain `RESOLVED_HOPS=0/22` DRIFT; broken `RESOLVED_HOPS=0/2` DRIFT |

Item 9 is *not* the SCORECARD value (17/17, 17/22, 1/2): this host's lane tree has no `research/`
directory (`ls -d research` → No such file or directory), so all 17 sources resolve outside the
allowed roots and are refused (`FINDING CLAIM_SOURCE_OUT_OF_CORPUS … resolved=./research/…`).
Base and patched refuse identically, so the comparison carries no regression signal here; the
absolute no-harm numbers must be measured where the sources exist. [INFERENCE] the `--json` path
cannot affect claim/chain verdicts except through the line content, and the selftest's pin case
(`TALL_JSON_H1`) plus cases 134–136 exercise that content unchanged.

Constraints honoured: no run of `c1-count.py` or `c2-count.py` (neither was ever invoked; only
their docstrings/code were read for the lock semantics); no writes outside
`/fast/scratch/hyaku/chousa-r32/w1/ExecC1Build/` and this seat's `.ufo/.../ExecC1Build/` directory;
no git/jj write command in the lane (`clone`, `checkout`, `show`, `status`, `rev-parse` only — all
in the scratch clone except two read-only `git show`/`git status` in the lane); no network; every
command bounded (`timeout 1800` on selftests, `timeout 120` on gate runs inside the selftest);
installs: none.

## 3. Verdict

C1 candidate built and self-tested: **the gate's `verify-all … --json PATH` append is now one
flock-held critical section** (open O_APPEND → blocking `LOCK_EX` on that fd → last-byte probe →
write → close), r24 delimiter/NUL logic and setup refusals unchanged in behaviour, base selftest
cases byte-identical at 228/228, two new cases pass on two consecutive full runs and the first of
them fails exactly on a lock-less control. Whether P1 (`APPEND_SERIALIZED=24/24`) holds is the
L1's call under the committed counter — not measured here by design.

## 4. Risks / limits

- The gate is now *dependent* on `flock(1)`. A host without util-linux's flock cannot write a
  `--json` manifest (exit 2) where base would have written one unlocked. Deliberate, documented;
  if the lane prefers a soft-degrade, that is a policy change, not a bug fix.
- Open-failure message text changed (`manifest open failed` vs base `manifest append failed`);
  exit code and ordering unchanged. No selftest or counter asserts the old string (grep: one
  occurrence, the new split).
- Case 229 is timing-sensitive by construction: it polls `/proc/locks` (0.1 s × 200) and requires
  the gate to still be alive when the waiter appears. It passed 3/3 observed runs (patched ×2,
  control ×1 with the expected failure) and skips cleanly where `/proc/locks` is absent.
- The lock covers the probe and the write only, not the section computations; that is what the
  contract asks and keeps the hold time in the millisecond range.
- Blank-line elimination additionally relies on every writer using the lock; a foreign,
  non-cooperating writer that writes without LOCK_EX can still race (base and candidate alike) —
  out of scope for C1, which is defined over cooperating appenders.
