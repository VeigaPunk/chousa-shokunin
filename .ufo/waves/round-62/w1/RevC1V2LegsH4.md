# RevC1V2LegsH4 — review of legs H16–H20 of `c1v2-count.py` (both profiles)

Scope: legs H16 OUTFILE, H17 UNREADABLE, H18 FIFO, H19 ENTRYDOT, H20 BIGFORM. Frozen counter, battery,
controls and claims read, not edited. No lane file written; all work in scratch
`/fast/scratch/hyaku/chousa-r62/RevC1V2LegsH4/` (deleted before yield; the commands below reproduce every
number). Python 3.14.8, uid 1000, `/usr/bin/unshare`; `unshare -Ufp --kill-child --mount-proc true` → rc 0.

## Method
- Frozen counter, unmodified, run with my builders and a fresh `--work`:
  `TMPDIR=<scratch> C1V2_SEED=<N> python3 -B corpus/evidence/round62/c1v2-count.py --builder <B> --work <scratch>/runs/<B>-<N>/w --receipt …`
  28 full runs (builders × seeds 11, 12, 21, 22), each `LEGS=…` line recorded.
- Driver `drv.py` (scratch only) imports the frozen counter read-only, wraps `run()` to print each child's rc,
  rss and stderr, runs chosen legs (env `PROFS` selects profiles), and can override `C.AS_LIMIT`. Used for stderr
  attribution, the AS sweep and the blocking-open check.
- `land.py` = byte copy of `tools/build-spans.py` (sha256 prefix `c366492005ce304a`, matches claims). Other
  builders are scratch edits of it, listed below.

## Findings (ordered by severity)

### F1 — H20 false negative: the leg never reaches the 64 MiB form cap (uncapped builder passes)
- `nocap.py` = landing with `if len(form) > MAX_FORM:` replaced by `if False:`. Counter, seed 11:
  `LEG H20 BIGFORM pass neutral: ok rc=1 rss_kib=231360 | plain: ok rc=1 rss_kib=167676`; `LEGS=20/20 C1V2=PASS`.
  Seed 12 also 20/20. The builder violates the lane contract (cap stated at `tools/build-spans.py` lines 21 and 70–71),
  so this is a false negative, not a false positive.
- Why it passes: the refusal is not the cap. stderr (driver): `build-spans: refused S872: capture-text refused
  <key>.raw: package too large to render in memory`. `tools/capture-text.py` `text_form()` converts the `MemoryError`
  raised while `ET.iterparse` holds the single 70 MiB `w:t` into `Refused`. The cap message
  (`text form is 73400604 chars, over the 67108864-char cap`) appears only when memory is available:
  `drv.py land.py leg_h20 11 512`.
- AS sweep, `drv.py nocap.py leg_h20 11 <MiB>` (plain and neutral agree at every point):
  - 200, 224, 240, 256, 272, 288 MiB → rc=1 by MemoryError → leg **passes**.
  - 304, 320, 512, 1024 MiB → rc=0, spans written → leg **fails** (`LEG H20 … FAIL rc=0`).
  - The counter's limits are plain 200 MiB and neutral 200–224 MiB. The leg therefore measures the address-space
    limit, not the cap; no leg reaches landing's MAX_FORM check at the counter's limits. Frozen control X10
    (drop AS limit) SURVIVES, which the claim discloses only as a generic gap, not as H20's dependence.
- H20 has no RSS bound (H14/H15 do, `big_leg` line 580).

### F2 — H16–H20 "nothing written" is checked only at `--out` (writes elsewhere pass every leg)
- `stray.py` = landing plus: on every invocation write `stray.txt` into `--cache`. `LEGS=20/20 C1V2=PASS` at seeds
  12 and 11 (`stray-11`, `stray-12`). Every leg's clean check is `clean_out(fx)` or a byte compare of `fx.out`. P03
  is the only leg that inspects another directory (`tools/`, P02 only). Writes into the cache, cwd, HOME or
  fixture root are unmeasured by H16–H20 and P01–P06.

### F3 — tautology: a do-nothing refuser passes all five legs
- `stub2.py` = `sys.exit(2)`: H16, H17, H18, H19, H20 all `pass` in both profiles (`stub2-11`, `stub2-12`, rc=2 on each).
  Its P-legs fail (`LEGS=14/20 C1V2=FAIL`), so the battery still rejects it, but these five legs add no
  discrimination against an exit-2 stub.
- `stub1.py` = `sys.exit(1)`: H17, H18, H20 pass; H16 and H19 fail on the wrong code (`stub1-11`: `LEGS=11/20`).
- Net: H16–H20 reject exit-0 stubs and wrong-code stubs; none can tell a real refusal from a stub. Count = 5 of 5.

### F4 — H19 exit-code pin conflicts with the builder's own contract (false positive)
- `ent1.py` = landing with the bad-entry path (`tools/build-spans.py` line 218 `sys.exit(2)`) changed to `sys.exit(1)`.
  `LEG H19 ENTRYDOT fail neutral: FAIL rc=1 | plain: FAIL rc=1`; `LEGS=19/20 C1V2=FAIL` at seeds 11 and 12.
- Contract: `tools/build-spans.py` docstring lines 30–31 and 51: "A refused row … any refusal writes nothing and exits 1";
  "1 a row refused … 2 usage/env, an unreadable quotes file, or an output refusal". An `entry` containing `..` is a
  refused row by that wording. The counter pins exit 2 (H19 text: "exit 2") and the landing code uses 2, but the landing
  docstring says 1. Counted as false_positive=1 with this caveat. Under the frozen text alone, exit 1 is outside H19's
  stated set, so the counter is internally consistent while the contract is not.

### F5 — profile and environment dependence (c)
- H20: verdict set by the AS limit (F1). For `nocap` the flip point lies between 288 and 304 MiB
  (`drv.py nocap.py leg_h20 11 288`, `… 304`), so the counter's current neutral draws (200–224) do not flip it. For a
  capped builder the verdict is PASS at every AS tested (200 and 512 MiB).
- H20 `rss_kib` is not the builder's peak: a no-op `exit 2` stub reports `rss_kib=159772` (plain) and `231448` (neutral)
  (`stub2-11`). INFERENCE: `ru_maxrss` of a forked child inherits memory of the counter's own process (`rss_probe2.py`:
  a child of a 230 MiB parent reported 483 MiB, of a small parent 12 MiB). H14/H15 (RSS < 96 MiB) reported 18–21 MiB
  in every run, including H20 run earlier in the same process (`drv.py land.py leg_h20,leg_h14 21`), so their verdicts
  were unaffected here.
- H17 UNREADABLE: `if os.geteuid() == 0: raise SystemExit(...)`. As root the counter exits 1 with no verdict line,
  indistinguishable by exit code from `C1V2=FAIL`. Not run as root (no sudo used); observed `python3 -c 'raise
  SystemExit("msg")'` → rc 1.
- H18 FIFO: plain stdin `/dev/null`, neutral closed pipe; no cross-profile difference observed.
- H16, H19: no profile dependence observed.
- Neutral masking: none found. Across 28 full runs, 140 H16–H20 verdict lines (`LEG H16|…|H20` in the logs), plain and
  neutral never disagreed (0). Neutral name collisions ~1e-7 per fixture (INFERENCE from the generator); no fixture
  was made ineffective by a name.

## Correct builders: no false positives beyond F4
Each passes all 20 legs in the full counter at the seeds shown:
- `pos-indep1.py`, `pos-indep2.py`, `pos-indep3.py` (controls): `LEGS=20/20 C1V2=PASS` at seeds 11 and 12 (pi1, pi2, pi3)
  and 21 (pi1–pi3).
- `vA.py` (new): unreadable capture → exit 2 (not a refused row); FIFO refused by `lstat` before any open.
  `LEGS=20/20 C1V2=PASS` at seeds 21, 22.
- `vB.py` (new): a `.raw` zip whose directory declares a member over 64 MiB is refused before capture-text renders it
  (`refused S399: … declares member word/document.xml over the form cap`). `LEGS=20/20 C1V2=PASS` at seeds 21, 22.
- `vC.py` (new): an `--out` that is not a directory is refused before the quote table and cache are read.
  `LEGS=20/20 C1V2=PASS` at seeds 21, 22.
- H18 discrimination check: `hang.py` (landing with `O_NONBLOCK` removed from the capture open) →
  `LEG H18 … plain: FAIL rc=-9 timeout=True` and `neutral: FAIL rc=-9 timeout=True` (`drv.py hang.py leg_h18 11`,
  `PROFS=neutral`). The FIFO leg does catch a blocking open in both profiles.

## Counts
- Correct-builder false positives beyond F4: 0 (6 correct builders, 2–3 seeds each, both profiles).
- Refusal-only tautology: 5 of 5 legs passed by an `exit 2` stub.
- Limits these legs do not measure (F1, F2) are routed to the next battery round as limits; the frozen counter is not
  rewritten.

VERDICT: LEG_DEFECTS=4 false_positive=1 tautology=5 legs=H16 OUTFILE, H17 UNREADABLE, H18 FIFO, H19 ENTRYDOT, H20 BIGFORM
