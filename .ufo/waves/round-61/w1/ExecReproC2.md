# ExecReproC2 — independent measurement of R61-C2 (wave w1)

Lane HEAD at run: 9f32ac055c59…; frozen files unchanged (sha256 prefixes: c2-count.py 6bd864b9, run-c2-controls.py a5296f19,
c2-positive-entry.md 15857b2f, c2-positive-rows.txt 721a108b, claims.md 9afec8d4 — all match claims.md). I wrote nothing outside this report and scratch
/fast/scratch/hyaku/chousa-r61/ExecReproC2 (removed before yield). No installs. No network. No labrat spawned.

## Findings
1. Mirror built exactly as run-c2-controls.py does (copy corpus/, R55W2SentBuilder.md as the S136 file, rows inserted via its own `rows_into`,
   entry copied to corpus/knowledge/derived-output-safety-r61.md). The counter on the mirror, 12 environment variants:
   every one printed `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=8/8 COVERAGE=1/1 CLAIMS=1/1 LIMITS=1/1 CENSUS=1/1 C2=PASS`, rc=0.
   Variants: default; MANWIDTH=80; MANWIDTH=1000; LANG=C; LANG=C.UTF-8; LANG=C+LC_ALL=C+MANWIDTH=80; LANG=C.UTF-8+MANWIDTH=1000;
   PATH with /usr/bin first; PATH fully reversed; PATH=/usr/bin only; PATH with a shim `man` first; reversed PATH+MANWIDTH=80+LANG=C.
   Verdict never changed (12/12 PASS).
2. Why caller env cannot matter (observed, not only inferred): c2-count.py line 71 builds `env = dict(os.environ, MANWIDTH="1000", LC_ALL="C.UTF-8")`
   for the man child. A logging shim `man` placed first on PATH recorded, under caller MANWIDTH=80 LANG=C and under MANWIDTH=1000 LANG=C.UTF-8:
   `argv=-l /usr/share/man/man2/open.2.gz MANWIDTH=1000 LC_ALL=C.UTF-8 LANG=C` (and the same for rename.2.gz, LANG=C.UTF-8 in the second run).
   So MANWIDTH and LANG/LC_ALL variation is a no-op by construction; the PATH variants are the only real degrees of freedom, and
   `man` resolved to the shim (log written) with the same PASS. System man is /usr/bin/man 2.13.1; `col` /usr/bin/col; only /usr/bin/man on PATH (`which -a`).
3. Real lane (no entry/rows landed yet): `python3 -B c2-count.py` → `ENTRY=0/1 TRIO=0/1 ROWS=0/3 QUOTES=0/0 COVERAGE=0/1 CLAIMS=0/1 LIMITS=0/1 CENSUS=1/1 C2=FAIL`
   rc=1 (matches the "before" state; rows S134–S136 absent).
4. Controls: `python3 -B controls/run-c2-controls.py --work $S/ctl` → 15 lines, 13 FAIL-expected rows FAIL, `positive` and `echo-claims` PASS, last line
   `C2_CONTROLS_UNEXPECTED=0`, rc=0. Output is line-for-line identical to the frozen receipt controls/c2-controls.txt (diff by eye of the 15 rows; same counters per row).
5. Counter limit found (disclosure, not a verdict change): the counter resolves `man` and `col` through PATH. A hostile `man` shim that `cat`s a file made of the
   entry's own quotes plus anchors made the counter print `QUOTES=8/8 … C2=PASS` rc=0 on the mirror (probe in scratch). With quotes only, no anchors: QUOTES=2/8 FAIL, so the
   anchor-in-man-text check is the only thing stopping a quotes-only forge. Real man-page rendering is therefore trusted from the host PATH; a closure run should
   use a PATH where `command -v man` is /usr/bin/man (it is here: `PATH=$S/shimA:$PATH command -v man` showed the shim only when I put it first). `PATH=/nonexistent` → rc=1
   `c2-count: man or col unavailable` (counter doc says rc 2 for env; observed rc=1 because SystemExit(str) exits 1 — doc/behaviour mismatch, minor, INFERENCE as to intent).

## Commands (all `python3 -B`, cwd scratch)
- driver /fast/scratch/…/drv.py: builds mirror, loops the 12 variants running `c2-count.py --root mirror` (output above).
- `env MANWIDTH=80 LANG=C PATH=$S/shimA:$PATH python3 -B c2-count.py --root $S/mirror` + shim.log lines quoted in finding 2.
- `python3 -B controls/run-c2-controls.py --work $S/ctl` → `C2_CONTROLS_UNEXPECTED=0`.

## Not tested
Other `man` implementations (mandoc absent); man-pages versions other than the installed 6.19-1; the landed (non-mirror) entry, which does not exist yet.

VERDICT: C2_VERDICT_STABLE=yes controls_unexpected=0
