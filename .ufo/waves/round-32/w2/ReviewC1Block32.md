# W2 falsify — ReviewC1Block32: review of the C1 flock block

- Seat: ChousaR32A2.ReviewC1Block32. Time box: within 30 min of start.
- Reviewed object: `tools/research-gate.sh` at candidate `5d8a170795dcf48c3746a4f03dee9cfe32812834`
  (sha256 `10f2fe12…4098`, matches the declared candidate SHA). All experiments ran a read-only
  pinned clone at `/fast/scratch/hyaku/chousa-r32/w2/ReviewC1Block32/lane`; the live lane file moved
  under review (line count 7463 → 7481 between my two reads), so line refs below are the clone's.
- Target surface: `verify_all` JSON append block L3141-3154 (setup gates), L3240-3310 (sha/line build
  + flock critical section); header text L211-216, L419-429; usage text L339 ff and `Exit:` line;
  selftest cases `c1lk-holder-blocks-append` (L7094-7187, prints "233") and `c1lk-second-append`
  (L7188-7214, prints "234").
- Host: GNU bash 5.3.20(1), /usr/bin/{flock,tail,od,tr} present.

## Attack surface and what was checked

| Item | Evidence |
|---|---|
| fd allocation `exec {jfd}>>` failure semantics | `bash -c 'if ! exec {jfd}>>./no-such-dir/mf 2>/dev/null; then echo OPEN-FAIL; exit 2; fi'` → shell survives to the `!` branch, `outer_rc=2`. `exit 2` is reachable and correct. |
| fd inheritance into children | E1b: `flock -x "$fd"` succeeds on fd 10 allocated by `{jfd}`; BOTH an exec'd child (`tail -f`) and a fork-only subshell still see the fd in `/proc/*/fd` (count 1,1). So the probe children at L3301 DO inherit the locked fd — but they run to completion inside the critical section (`$(...)` wait), and the gate spawns no background children between `flock -x` (L3296) and `exec {jfd}>&-` (L3310). No slow work is ever under the lock: only `tail|od|tr` + one `printf` sit inside it; all sections ran earlier (L3200s) and their SECTION lines print AFTER the append (L3313+, confirmed by E4: 0 SECTION lines while blocked, rc 0 after release). |
| Lock outlives the `flock(1)` helper | E6a: after `flock -x "$fd"` the helper exits, then `flock -n -x` on a SECOND description over the same inode → `BLOCKED_GOOD`; control on an untouched file → `ACQUIRED_GOOD`; dup'd same-description probe → `SAME_DESC_ACQUIRE_EXPECTED` (flock semantics: lock attaches to the open file description). Comment L3278-3285 is accurate. |
| Lock release on every exit path | Only exits after `flock -x` are `exit 2` (lock failure L3298, append failure L3308) or fall-through → `exec {jfd}>&-` L3310. Kernel releases the lock when the fd/process description closes — every path closes it. No `return`, `die`, `exit 1`, or trap path exists between acquire and release that could skip the close. The selftest's own EXIT trap `rm -rf WORK` can't reach the manifest fd. |
| NUL-byte probe | E2 live run: `printf '{\x00'` fragment in `mf.jsonl`, full `verify-all --json` → rc 0, `lines=2 blanks=0`, `od` last bytes `…307d0a`, gate's own line parses clean JSON; prior fragment stays its own (invalid-JSON) line — no gluing, no blank line. Probe L3300-3304 correct: `-s` guard means empty manifests take `jlast=''` → straight append; `od -tx1` distinguishes `0a` from `00` where `$(tail -c1)` would drop NUL. |
| End-to-end serialization | E3: 6 races, 2 gates each against the same manifest (3 rounds × {fragment-seeded, empty}) → 12 gate runs, all rc 0, every manifest line parseable, 0 blank lines, 0 glued `}{`, stable inode. E4: a cooperating holder blocked the gate's flock(1) (visible as `-> FLOCK … WRITE` waiter at L7113's own /proc/locks probe, inode match), manifest untouched until release, then 2 lines, 0 blanks, gate rc 0. |
| Fail-closed branches | No-flock PATH run → `rc=2`, stderr `research-gate: flock(1) unavailable; manifest not written: …`, manifest stays 0 bytes — matches L3287-3290 and header "refuses to write". `flock -x 9` on a bad fd → util-linux rc 65; gate maps to its own rc-2 + message (L3296-3299). `die_usage` L440 covers setup refusals (dir missing, non-regular, non-empty-unreadable L3144-3153). |
| Selftest cases | Full committed `--selftest` on the clone (TMPDIR=scratch, `RLIMIT_NPROC=8000`): `rc=0`, `RESEARCH_GATE_SELFTEST: PASS (241 cases, 0 skipped)`, 0 FAIL-case lines; `ok-case 233 c1lk-holder-blocks-append exit=0`, `ok-case 234 c1lk-second-append exit=0` (log in `.ufo/waves/round-32/w2/ReviewC1Block32/selftest.out`). Case 233's assertions are real: waiter-in-/proc/locks, manifest-untouched-while-held, 2 lines + fragment intact + own-line schema + 0 blanks + inode stable + JSON-valid + rc 0. |
| Usage text | L339+ lists the append contract and `Exit: 0 CLEAN | 1 DRIFT | 2 setup/usage`; every manifest-failure path exits 2 (consistent, though "setup/usage" also covers this operational failure — acceptable, all distinct messages). Header L211-216 + L419-429 describe exactly what the code does; no false sentence found. |
| Single append path | `grep JSON_ARG`: only consumer is `verify_all` (L3141 validation, L3240-3310 append); `--json` gated to `MODE=all` L7404-7406; pin/drift fixture's manifest write reuses the locked path (`run_pin` invokes `verify-all --json`). No alternate unlocked writer. |
| L1 receipts | `.ufo/waves/round-32/measure/after-c1-s{32001,32002}.json` both `predicate_holds: true`, `gate_sha256: 10f2fe12…` — consistent with my own runs. |

## Findings

- **LOW-1 — silent glue if the last-byte probe itself fails.** L3301: `jlast=$(tail -c1 … | od … | tr … || true)`. `2>/dev/null` + `|| true` mean any probe failure (tail/od/tr missing from a stripped host — the gate checks `command -v flock` and `sha256sum` but never `tail|od|tr`, L3287/L3257-3260; or a non-cooperating mutation between the `[[ -s ]]` guard and the `tail` open) leaves `jlast=''` → the `[[ -n $jlast ]]` test is false → gate appends WITHOUT the leading `\n` → its JSON line glues onto the prior unterminated line (`{"prior"}{"schema"…}`), corrupting JSONL silently while holding the lock correctly. On this host all three tools exist (verified), so not reproducible here; a check like `command -v tail od tr` in the setup block or a `-z $jlast` re-read would close it. Severity LOW: requires a stripped-path host or a post-setup mutation race.
- **LOW-2 — coverage gap, not a defect: no selftest exercises a NUL-terminated manifest.** Both c1lk cases cover unterminated-fragment and empty manifests; the `od -tx1` NUL discrimination (the r24 fix the comment documents at L3273-3276) has no in-selftest case — a regression to plain `$(tail -c1)` would pass all 241 cases. My E2 covers it live; recommend a cheap third case writing a `…\x00` manifest. Also uncovered (reasonable, hard to induce): the `flock -x` EBADF path, `manifest open failed`, and `manifest append failed`.
- **INFO — `exit 2` semantics stretch.** A manifest-append failure exits 2 after all 5 sections ran; the `Exit:` line documents 2 as "setup/usage". Distinct stderr messages make it diagnosable; consistent choice, noting only for the axis-fit record.
- **INFO — footgun, documented behavior:** `--json` pointing at the record itself appends a manifest line to the input record (allowed; `[[ -e && ! -f ]]` check only bars non-files). Not a defect.

## Verdict

**HOLDS** for the C1 block as reviewed. The critical section is one lock-held step (open→`flock -x` on the append fd→probe→write→close) with no slow work inside, correct fd semantics on bash 5.3, lock released on every path including `exit 2`, NUL-safe probe verified live, serialization verified against a real cooperating holder and 12 racing runs, fail-closed on missing flock verified, and both selftest cases green in a full 241/241 PASS. No run below target, no contract violation found in the C1 surface. Two LOW items: silent-glue if the probe pipeline itself fails (unprotected `|| true`), and no selftest case for the NUL tail byte.

## Limits

- Not exercised: `manifest open failed` (L3292-3295) and `manifest append failed` (L3306-3309) branches — need a live open/write failure injection I could not induce safely in the time box; code inspected only. `flock -x` EBADF verified at util-linux level (rc 65), not through the gate.
- `tail` reads via path, not the locked fd — a non-cooperating rename between open and probe could probe a different inode; out of the cooperating-appender contract the design claims.
- Selftest holder waits are 0.1s-polling loops (600× / 200×); on a pathologically loaded host case 233 could flake on timing, but the bounds are generous and it passed here.
- Bash < 4.1 lacks `{var}` fd syntax → `exec {jfd}>>` would syntax-error → `exit 2`; bash ≥4.1 assumed (usage header does not state a minimum, INFO-level portability note).
- Installations: none (pacman transactions paused; host tools sufficient).
- Experiments bounded by `timeout`, `RLIMIT_NPROC=8000`; no lane/production file touched; scratch only under `/fast/scratch/hyaku/chousa-r32/w2/ReviewC1Block32/`.
