# Round 62 w1 — ConnClaimTrace: cross-claim trace of the C1 v2 counter

Seat: ConnClaimTrace (connector, leaf). Frozen inputs read, not edited: `corpus/evidence/round62/claims.md`,
`c1v2-count.py`, `c1v2-battery.py`, `controls/run-c1v2-controls.py`, `controls/c1v2-controls.txt`, `controls/null-counters.txt`,
`controls/c1v2-before.txt`; lane `tools/build-spans.py`; round-61 closure `corpus/lessons/round-61-verifier-spotcheck.md`,
lesson `corpus/lessons/round-61.md` (Mistakes 1–7, routed list), round-61 wave reports `.ufo/waves/round-61/w1/CritC1*.md`,
`ExecForgeSeqRed.md`. Scratch `/fast/scratch/hyaku/chousa-r62/ConnClaimTrace/` (deleted before yield). No installs, no network,
no git mutation (read-only `git status`). Nothing under `corpus/`, `tools/`, `SKILL.md` was written.

Hashes (`sha256sum … | cut -c1-20`): counter `b7016fba91b03460a419` (matches claim), battery `9afe00b917fb95e2a69f`,
runner `dce49d090b009b2155e9`, landed builder `c366492005ce304a0396` (matches claim), base `1ed2650af28ea8e392bc`.

## Findings

1. **4 of 14 classes are fully traced** (change in the counter + a frozen forger/mutant that fails without it + a named limit):
   sniff by environment/cwd/layout/names/URL, sniff by stdio/LANG/RLIMIT, sniff by parent or any process command line,
   detached `setsid` helper. The other 10 each miss at least one leg of the trace (table).
2. **Two holes the frozen battery cannot see, both reproduced by me:**
   - `.raw`-side hazards: no leg creates a `.raw` that is a symlink out of the cache, a FIFO, a multi-link file or an
     unreadable file. A builder that falls back to the `.txt` sidecar when `.raw` is refused scores **LEGS=20/20** (run R6).
     `.raw` is not in the claims' named limits.
   - RSS hidden by a detached holder: a child process that is never reaped holds 150 MiB; `H14`/`H15` **pass** in 46 of 46
     builder invocations with `rss_kib` ≈ 20 000 (run R16). The named limit covers "reads a 192 MiB capture in a detached
     helper"; a holder that reads nothing is not literally named.
3. **Three changes are real but no frozen control would fail on their reversion** (they are caught only by my probes):
   the `Traceback` token removal in H16/H17, the mtime comparison in the refusal snapshots and victim trees, and the
   environment seed. The battery has no correct builder that prints the word, no touch-only forger, and no forger that reads a seed.
4. **X10 (address-space limit) survives** (lane receipt). It is the only bound on a detached holder (row 8): holders are
   capped at about 200 MiB, not at the 96 MiB the H14/H15 predicate states.
5. **Named-limit calibration:** rows 1, 2, 11, 12, 13, 14 have no named limit in `claims.md` or the counter docstring. Rows 11
   and 12 leave a residual I can state (INFERENCE: a builder that exits 2 after printing a traceback is accepted by design;
   a builder that rewrites identical bytes and restores mtime is not detected) but neither is named.

## Table (14 classes)

(a) = change in frozen `c1v2-count.py` (line numbers as of this freeze). (b) = frozen battery forger or run-controls mutant
that fails without the change; "probe" = my scratch run, not frozen. (c) = named limit in claims or counter docstring.

| # | Class (source) | (a) change | (b) control that fails without it | (c) named limit | Status |
|---|---|---|---|---|---|
| 1 | Legs in fixed order; only builder pid killed; call-counting forge (M1; `ExecForgeSeqRed`, `CritC1Seq`) | seeded leg/profile shuffle, lines 697–704, under `unshare --kill-child` | none: no mutant removes the shuffle; no battery forger counts calls; call-counting forge not re-run (code was in deleted r61 scratch) | none | NOT (b, c) |
| 2 | Seed on argv (M1 `CritC1Seq`; routed 1) | seed from env `C1V2_SEED` (l.687); no `--seed` option (probe R14); fresh builder env | none frozen. Probe R10/R11: seed in builder env shows as `C1V2_SEED=4242` in 23 of 46 plain-profile invocations; intact shows it in 0 of 46 | none | NOT (b, c) |
| 3 | Sniff: cwd name, env keys, dir layout, file names, URL host (M2 `CritC1Sniff` F01–F05) | neutral profile: random dir/builder/quotes/cache/out names (l.153–158), URL shape (l.186–189), env (l.286–290) | X07 (F01,F03,F04), X05 (F02), X08 (F05), X01 (all plain-only) — lane receipt, not re-run | "features neither profile varies": capture-text name, `S###` id shape, quote vocabulary | **FULL** |
| 4 | Sniff: LANG, RLIMIT_FSIZE, stdin, stdout-is-file (F07–F09, F11) | LANG/PATH/RLIMIT vary (l.286–291); closed-pipe stdin (l.302–304); pipes for stdout/stderr (l.312–344) | X05 (F07), X06 (F08), X04 (F09), X03 (F11) — lane receipt | same as row 3 | **FULL** |
| 5 | Sniff: parent command line, any process command line (F06, F10) | sandbox `unshare -Ufp --kill-child --mount-proc` (l.141): builder is PID 1, ppid 0, counter invisible (spy: 92/92 `ppid 0`, `parent_cmd` unreadable) | X02 (no sandbox): F06, F10 accepted. Re-run here with `--only F06 F10 F12`: no-sandbox `counter_exit=0 … MISS` for F06 and F10; intact `counter_exit=1` for both | builder detects the sandbox itself (NSpid, getpid()==1) | **FULL** |
| 6 | Detached `setsid` helper acts after builder exit (F12; `CritC1Detached` P03 route; routed 1) | PID-namespace teardown kills every process at PID-1 exit; `killpg` (l.332–341) | X02: F12 accepted. Re-run: no-sandbox `F12 counter_exit=0 … MISS`; intact `F12 counter_exit=1 LEGS=19/20` | "a builder that waits out the counter is not stopped"; residual inside the 60 s window is not separated | **FULL** (H10–H12 detached route not forged separately; INFERENCE: same teardown) |
| 7 | Builder detects the sandbox itself (NSpid, getpid()==1) | none | none | named (claims) | NOT (a, b) |
| 8 | RSS hidden by a detached holder: unreaped child holds memory (`CritC1Rss` route 3; routed 1) | `ru_maxrss` from `wait4` on the unshare child (l.335, 353, 366); AS limit 200 MiB (l.142) | none frozen: no RSS forger, no RSS mutant; X10 survives. Probe R7/R16: 150 MiB detached holder, child `VmHWM` ≈ 164 MB, parent read `b'1'` 46/46; intact `H14 rss_kib=20616`, `H15 21032`, `LEGS=20/20` | "reads a 192 MiB capture in a detached helper under the address-space limit is bounded, not measured" — holder variant not literally named | NOT (a holds, b, c partial) |
| 9 | In-process holder (control for row 8) | `rss < 96 MiB` predicate (l.580) | none frozen. Probe R17/R18 (88 MiB held in-process): intact `H14 FAIL rc=1 rss_kib=110400`, `H15 FAIL`, `LEGS=18/20`; RSS check off: `LEGS=20/20` | n/a | support for row 8 (in-process holder *is* caught) |
| 10 | Address-space limit (bounds detached holders) | `AS_LIMIT` 200 MiB (l.142, 291) | X10 **SURVIVES** (`battery_exit=0`, lane receipt; "named gap") | named gap | NOT (b) |
| 11 | `Traceback` token in H16/H17 (M3; routed 1) | token tests removed; exit code and tree only (l.599, 613) | none frozen: `grep -c Traceback` = 0 in `pos-*.py`, base and landed. Probe R3: correct builder printing the word on stderr, token-check counter `H16 FAIL`, `H17 FAIL`, `LEGS=18/20`; intact R2 `LEGS=20/20` | none | NOT (b, c) |
| 12 | mtime-blind refusal snapshots and victim trees (routed 1; H10–H12 "final tree only") | `snap(…, True)` in H07–H12 (l.455–545) | none frozen (no touch-only forger, no mtime mutant). Probe R4 (`touch` stub: `os.utime` on out tree, exit 2): intact `H07, H09, H11, H12 FAIL` (H11/H12 via symlink victims, `victim_unchanged=False`), `LEGS=10/20`; mtime off R5: those four `pass`, `LEGS=14/20` | none ("refusal snapshots compare mtimes" is a design line; restore-mtime-after-rewrite not named) | NOT (b, c) |
| 13 | `.raw`-side hazards: `.raw` symlink out of cache, FIFO/device, >1 hard link, unreadable (M5; routed 1) | none in counter. Landed refuses them (`_open` l.102–122, `_decide` l.138–152). No leg creates such a `.raw`: only regular `.raw` (`add_docx_capture` l.240–245, H15, H20) | none: probe R6 (`.txt` fallback on bad `.raw`) intact `LEGS=20/20`. Direct fixture: landed `exit=1 … refused S100: … resolves outside the cache`; fallback `exit=0`, writes `spans/S100-1.txt` | none | NOT (a, b, c) |
| 14 | Leaked outside bytes with exit 1 (M2 leg-level FP; H13) | output-tree marker check (l.561–565) | none frozen: no mutant removes the leak check; no stub writes outside bytes | none | NOT (b, c) |

Summary: FULL 3, 4, 5, 6 → **4/14**. Row 9 is support for row 8, not a class.

## Evidence (commands I ran; outputs quoted)

Scratch runs used the frozen counter unmodified (`python3 -B corpus/evidence/round62/c1v2-count.py --builder <cand> --work <scratch>/w/Rn`)
or a scratch copy with one reversion (same tree layout, `tools/capture-text.py` copied in). Battery runs used `--only F06 F10 F12`.
Candidates are landed-builder copies with one insertion before `if __name__ == "__main__":`, or a standalone stub.

- R1 landed, intact: `LEGS=20/20 C1V2=PASS` (`BUILDER sha256=c366492005ce…`, `SEED=1049270963`).
- R2 landed + stderr `Traceback` note, intact: `LEGS=20/20 C1V2=PASS`. R3 same builder, token-check reversion: `LEG H16 OUTFILE fail … rc=2`, `LEG H17 UNREADABLE fail … rc=1`, `LEGS=18/20 C1V2=FAIL`.
- R4 `touch` stub, intact: `LEG H07 … FAIL`, `H09 … FAIL`, `H11 … FAIL victim_unchanged=False`, `H12 … FAIL`, `LEGS=10/20`. R5 same stub, `mtime=False` reversion: `H07 pass`, `H09 pass`, `H11 pass`, `H12 pass`, `LEGS=14/20`.
- R6 `.raw` fallback, intact: `LEGS=20/20 C1V2=PASS`. Direct (`python3 -B tools/build-spans.py --quotes q.tsv --out … --cache …`, `.raw` symlink to outside file, `.txt` sibling): landed `exit=1 stderr='build-spans: refused S100: … .raw resolves outside the cache' files=[]`; fallback `exit=0 files=['spans','spans.tsv','spans/S100-1.txt']`.
- R7/R16 detached holder (150 MiB, `os.fork`, unreaped): R16 `LEGS=20/20 C1V2=PASS`, `H14 … rss_kib=20616`, `H15 … rss_kib=21032`. `hold.log`: 46 `child VmHWM: 164864–1649xx kB` lines and 46 `parent read=b'1'` lines.
- R17/R18 in-process 88 MiB holder: intact `H14 FAIL rc=1 rss_kib=110400`, `H15 FAIL rc=1 rss_kib=111140`, `LEGS=18/20`; RSS check removed `H14 pass`, `H15 pass`, `LEGS=20/20`.
- R8/R9 in-process whole read of a 192 MiB `.txt`: `H14 pass rc=1 rss_kib=19392` on intact. INFERENCE: the 200 MiB address-space limit fails the allocation before pages are touched, so RSS stays low; not separately verified. (R8/R9 also show `H18 rc=-9`; that is my candidate reading the FIFO, not a counter result. R8/R9 are not used as evidence.)
- R10/R11 spy (`C1V2_SEED` probe), 92 invocations total: `grep -o '"seed_in_env": [^,]*' spy.log | sort | uniq -c` → `23 "4242"`, `69 null`. `"ppid": 0` 92/92; `parent_cmd` `ERR … /proc/0/cmdline` 92/92. The seed appears only in plain-profile invocations of the envpass reversion.
- R14: `python3 -B corpus/evidence/round62/c1v2-count.py --seed 5 --work <scratch>/w/argv` → `c1v2-count.py: error: unrecognized arguments: --seed 5`, exit 2.
- R12 (no sandbox, `SANDBOX = []`, same as lane X02): `battery … --only F06 F10 F12` → `SUBJECT FORGER F06 … counter_exit=0 want=1 MISS | LEGS=20/20 C1V2=PASS`; same for F10 and F12; `FORGERS_REJECTED=0/3 … BATTERY=FAIL`.
- R13 (intact, same subset): `F06 … counter_exit=1 want=1 ok | LEGS=11/20`; `F10 … counter_exit=1 ok | LEGS=11/20`; `F12 … counter_exit=1 ok | LEGS=19/20`; `FORGERS_REJECTED=3/3`.
- Lane receipts, not re-run (`corpus/evidence/round62/controls/c1v2-controls.txt`): X01 accepts F01,F02,F03,F04,F05,F07,F08,F09,F11; X02 F06,F10,F12; X03 F11; X04 F09; X05 F02,F07,F08; X06 F08; X07 F01,F03,F04; X08 F05; X10 survives; X12 as X01. `CONTROLS_UNEXPECTED=0`.
- `grep -c Traceback corpus/evidence/round62/controls/pos-*.py corpus/evidence/round62/controls/base-build-spans.py tools/build-spans.py`: 0 for each.

## Calibration notes

- The battery's sniff forgers are caught by the leg conjunction: each forger fires only on the plain profile's feature, so the neutral
  run falls through to the base builder and the leg fails. This is why rows 3–6 trace; the design is sound for the features it varies.
- Seeds, sandbox and the counter's own `argv` are closed as channels. The seed-channel class has no forger that exploits it,
  so its closure is untested beyond the spy.
- Rows 11–13 are the instrument's exposed surface for a builder that is correct in the features the battery checks. A seat that
  writes a forger for any of them would be a counter limit, routed to the next round's battery per `claims.md` (not a refutation).

## Routed to the next round (not changed here)

1. Add a `.raw` leg set: symlink out of cache, FIFO, multi-link, unreadable `.raw` with a `.txt` sibling (row 13).
2. Add a control for the detached holder: fork, hold 150 MiB, no reap; measure via `/proc` or tree RSS, not `wait4` alone (row 8).
3. Add a touch-only forger and a victim-mtime-restore forger to the battery (row 12); name the residual in claims.
4. Add a correct builder that prints the word `Traceback` on a refusal, to the positives (row 11).
5. Add a seed-replay forger that reads a seed from its environment, and an X-mutant that puts the seed in the builder env (row 2).
6. Add a shuffle-off mutant and a call-counting forger (row 1).

Install record: none (no tools installed or updated).

VERDICT: CLASSES_FULLY_TRACED=4/14
