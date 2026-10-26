# R51W2ExecSeedSupplement — FLAKE: `c1-supplement.py` and the frozen `c1-count.py` at `4436e27`

Scope: `corpus/evidence/round51/c1-supplement.py` and `corpus/evidence/round51/c1-count.py` at lane tip
`4436e279b91d8d68fd439c9095695035fbeeab74`. 90 runs: 25 supplement (no seed), 25 supplement `--seed 1..25`,
40 frozen counter `--seed N` (the assignment's screen). Nothing in the lane edited; no install. Scratch
`/dev/shm/chousa-r51-R51W2ExecSeedSupplement/` (removed after the run).

## 0. Artifact pinned by blob, not by path

```
$ mkdir -p /dev/shm/chousa-r51-R51W2ExecSeedSupplement/tree
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 4436e279b91d8d68fd439c9095695035fbeeab74 \
    | tar -x -C /dev/shm/chousa-r51-R51W2ExecSeedSupplement/tree      # 14840 files
$ cd /dev/shm/chousa-r51-R51W2ExecSeedSupplement/tree
$ sha256sum corpus/evidence/round51/c1-supplement.py corpus/evidence/round51/c1-count.py tools/assimilate-rows.py
163e9bdbdf225330cc2af2661790b698fc28fc0b7f6ac416bfbe5e7b77cbe498  corpus/evidence/round51/c1-supplement.py
94ddc7dc273c831407f49cdf175301fbf8b272ece2c9998de58dddc3b2a25284  corpus/evidence/round51/c1-count.py
6b975f91c809485c8d03e6134e2a17bdb7f9079c22218d74e9321a14632572f6  tools/assimilate-rows.py
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 4436e279:corpus/evidence/round51/c1-supplement.py | sha256sum
163e9bdb…  -        # identical; same for the other two blobs (c1-count 94ddc7dc…, tool 6b975f91…)
```

Every run: cwd = tree root, `env -u ASSIMILATE_CITES`, `TMPDIR` inside the scratch (the tools' own
`tempfile.mkdtemp` dirs land there, not `/tmp`).

## 1. Battery — script (45 lines) and verdicts

```python
import os, random, subprocess, sys, time, pathlib
TREE = pathlib.Path("/dev/shm/chousa-r51-R51W2ExecSeedSupplement/tree")
ENV = {k: v for k, v in os.environ.items() if k != "ASSIMILATE_CITES"}
def run(argv, tmo):
    t = time.perf_counter()
    try:
        r = subprocess.run(argv, cwd=TREE, capture_output=True, text=True, timeout=tmo, env=ENV)
        return r.returncode, r.stdout, r.stderr, time.perf_counter() - t
    except subprocess.TimeoutExpired as e:
        dec = lambda b: (b.decode() if isinstance(b, bytes) else (b or ""))
        return 124, dec(e.stdout), dec(e.stderr), time.perf_counter() - t
def precheck_ok(N):                      # the seed screen named in the assignment
    r = random.Random(N); r.randint(12, 40)
    return r.randint(500, 900) != r.randint(500, 900)
SUP = ["corpus/evidence/round51/c1-supplement.py"]
C1 = ["corpus/evidence/round51/c1-count.py"]
rows = []
for i in range(1, 26):
    rc, out, err, el = run([sys.executable, *SUP], 420)
    rows.append([f"supp-noseed/{i}", rc, out, err, el])
for N in range(1, 26):
    rc, out, err, el = run([sys.executable, *SUP, "--seed", str(N)], 420)
    rows.append([f"supp-seed/{N}", rc, out, err, el])
seeds = [N for N in range(1, 300) if precheck_ok(N)][:40]
for N in seeds:
    rc, out, err, el = run([sys.executable, *C1, "--seed", str(N)], 60)
    rows.append([f"c1-seed/{N}", rc, out, err, el])
def last(out):
    ls = [l for l in out.splitlines() if l.strip()]
    return ls[-1] if ls else "(no stdout)"
bad = []
for name, rc, out, err, el in rows:
    verdict = last(out)
    ok = rc == 0 and verdict.endswith("=PASS")
    print(f"{name:18s} rc={rc} {el:7.2f}s {'PASS' if ok else 'FAIL'} {verdict}" + ("" if out.count("FAIL")==0 else f" [stdout has {out.count('FAIL')} FAIL token(s)]"))
    if not ok: bad.append([name, rc, out, err, el])
print(f"RUNS={len(rows)} PASS={len(rows)-len(bad)} NONPASS={len(bad)} c1_seeds={seeds}")
print(f"ELAPSED_TOTAL={sum(r[4] for r in rows):.1f}s  MAX={max(r[4] for r in rows):.2f}s")
if bad:
    name, rc, out, err, el = bad[0]
    print(f"=== FIRST NON-PASS: {name} rc={rc} elapsed={el:.2f}s ===")
    print("--- stdout ---"); print(out)
    print("--- stderr ---"); print(err)
pathlib.Path("/dev/shm/chousa-r51-R51W2ExecSeedSupplement/rows.txt").write_text(
    "".join(f"{n}\trc={rc}\t{el:.2f}\t{last(o)}\n" for n, rc, o, e, el in rows), encoding="utf-8")
```

| leg | runs | PASS | non-PASS | wall per run |
|---|---|---|---|---|
| supplement, no seed | 25 | 25 | 0 | 2.85–3.77 s |
| supplement `--seed 1..25` | 25 | 25 | 0 | 3.08–3.70 s |
| `c1-count.py --seed N` (40) | 40 | 39 | 1 (`--seed 13`) | 0.74–0.89 s; defect 60.06 s (cap) |

`RUNS=90 PASS=89 NONPASS=1 c1_seeds=[1…40]`, `ELAPSED_TOTAL=263.3s  MAX=60.06s`.

First non-PASS, verbatim (stdout had exactly two lines; stderr empty):

```
=== FIRST NON-PASS: c1-seed/13 rc=124 elapsed=60.06s ===
--- stdout ---
SELFTEST_DEFAULT=PASS
LEGACY_ALL=PASS rc=0

--- stderr ---
```

60 s is my cap; the run is not slow, it is inside a loop that cannot exit (§3).

## 2. One run, timed

`/usr/bin/time` is not installed, so timing is `time.perf_counter()` around each `subprocess.run` (script
above). One supplement run at the tip: **2.85 s fastest, 3.77 s slowest** of the 25 unseeded runs (~3.4 s
typical, interpreter start included); a bare counter run 0.74–0.89 s. Determinism holds: `--seed 7` twice is
byte-identical (`diff` empty), output:

```
SHAPE=PASS 3/3
MUTATION=PASS 3/3
CROSS_ENTRY=PASS 3/3
SOURCE_LINE=PASS 3/3
UNKNOWN_SRC=PASS 3/3
CLASH=PASS 3/3
SUPPLEMENT_LEGS=6/6
C1_SUPPLEMENT=PASS
```

## 3. Defect (latent) — `safe_seed` screens the wrong draw, and the assignment's screen admits a hang seed

Code facts in the archived bytes:

- counter draws the nonce **first**: `c1-count.py:121` `n = f"{rnd.getrandbits(32):08x}"`, then `:123`
  `a_id, b_id, c_id = (f"S{rnd.randint(500, 900)}" for _ in range(3))`, then `:124`
  `while len({a_id, b_id, c_id}) < 3: c_id = …`. If `a_id == b_id` the set tops out at 2 and the loop is
  infinite — redrawing `c_id` cannot help.
- supplement `safe_seed` (`c1-supplement.py:89-96`) seeds a *fresh* `Random(s)` and immediately draws
  `randint(12,40)`, `randint(500,900)`, `randint(500,900)`. It never draws the nonce, so it tests words 0–2
  while the counter's `a_id`/`b_id` are words 2–3.

Measurement over 200000 uniform 30-bit seeds (the domain `safe_seed` samples):

```
samples=200000 precheck_accept=199499 counter_hangs=502 accepted_and_hangs=390 rejected_but_hangs=112
P(hang | precheck accepts) = 0.001955  (1/511.5)
```

Acceptance carries no protection: 78 % of hang-inducing seeds pass the pre-check. Small-range check of the
same misalignment:

```
counter-position collisions in 0..2999: [13, 182, 324, 1001, 1180, 2336, 2369]
of those, supplement safe_seed pre-check accepts (x!=y): [(13, 648, 850, 850), (182, 680, 619, 619), …]
```

Seed 13 concretely: the pre-check draws `x=648, y=850` (differ → accepted), while the counter draws
`n=1112433019 top=21 ids=[850, 850, 595]`.

End to end, on the archived module with only `safe_seed` patched **in memory** (no lane file touched):
`env TMPDIR=… timeout 40 python3 -c '…m.safe_seed=lambda rnd: 13…'` → no output, `rc=124` at 40 s. The real
SHAPE call is `c1-supplement.py:115-116` `subprocess.run(…, timeout=300, …)` with no `try`, so a hit costs
300 s and then leaves through an uncaught traceback: **no `C1_SUPPLEMENT=` line is ever printed**, i.e. the
gate sees a crash, not `FAIL`. Replica of that exact argv with a 3 s cap (the label was my shorthand; the
call lives at :115-116):

```
REPLICA of c1-supplement.py:56 SHAPE call -> TimeoutExpired | cmd tail: ['--seed', '13'] | timeout: 3
```

Exposure: 3 SHAPE rounds per run (`c1-supplement.py:173` `for _ in range(3)`), a fresh `safe_seed` each, so
P(run hits) ≈ 1−(1−0.001955)³ = 0.59 % ≈ 1/171; over 25 unseeded runs ≈ 14 % chance of one 300 s stall. My
50 supplement runs hit none (0.29 expected) — the leg is green here because the defect is latent.

The assignment's screen (`randint(12,40)`, then two `randint(500,900)` that differ) has exactly this
misalignment: it admitted seed 13, so the 40 selected were literally 1..40 and one of them hangs. A screen
that draws the nonce first excludes 13 and leaves 39/39 PASS.

## 4. What holds

1. 50/50 supplement runs print `C1_SUPPLEMENT=PASS`, and `SUPPLEMENT_LEGS=6/6`; that line appears only when
   every leg is `3/3` (`c1-supplement.py:178` `legs = {k: v == 3 for k, v in totals.items()}`), so all six
   legs passed in all three rounds of all 50 runs.
2. All six leg lines verbatim for `--seed 7` above; repeat run byte-identical.
3. 39/40 counter seeds print `C1=PASS`, which implies `LEGS=5/5` (`c1-count.py:216-219`); seed 40's full
   tail shows `SOURCE_ONLY … REGISTRY_STRUCTURE=PASS 4/4`, `LEGS=5/5`, `C1=PASS`.
4. Counter and tool at the tip are the blobs W1 reviewed (`94ddc7dc…`, `6b975f91…`), so every number here is
   the tip's, not an ancestor's.

## 5. Draft remedy (supplement only; predicate, target and control untouched — L1 integrates)

```python
# corpus/evidence/round51/c1-supplement.py — replace safe_seed (:89-96); counter's draw order, per c1-count.py:121
def safe_seed(rnd: random.Random) -> int:
    """A seed for which the frozen counter's first two id draws differ (it hangs otherwise: erratum E2)."""
    while True:
        s = rnd.getrandbits(30)
        t = random.Random(s)
        t.getrandbits(32)                      # the counter draws its nonce first
        t.randint(12, 40)
        a, b = t.randint(500, 900), t.randint(500, 900)
        if a != b:
            return s
```

```python
# …and make the SHAPE call fail as a leg, not as a crash (replace :115-116):
    try:
        rc_c1 = subprocess.run([sys.executable, str(EV / "c1-count.py"), "--tool", str(tool),
                                "--seed", str(safe_seed(rnd))],
                               capture_output=True, text=True, timeout=300, env=ENV)
    except subprocess.TimeoutExpired:
        rc_c1 = None
    res["SHAPE"] = rc_c1 is not None and rc_c1.returncode == 0 and "LEGS=5/5" in rc_c1.stdout
```

Gate advice (for the LOG/SCORECARD text): require rc 0 **and** the literal `C1_SUPPLEMENT=PASS` line; a
missing line or a traceback must read as FAIL, since today a hang prints neither.

VERDICT: attacked the tip's `c1-supplement.py` and frozen `c1-count.py` with 90 seeded/unseeded runs and a
200000-seed draw simulation — 89/90 PASS, and the one break is real: `safe_seed` (and the assignment's
screen) skip the counter's `getrandbits(32)` nonce, so a hang seed passes the guard (1/511 per SHAPE round,
~0.59 %/run, 300 s crash instead of `FAIL`); observed at `--seed 13` = `ids=[850,850,595]`, rc 124.

---

# Addendum — independent replay by seat `R51W2ExecSeedSupplement-2`

Path note: this file already held the completed report of sibling seat `R51W2ExecSeedSupplement` (duplicate
dispatch with the same trailer path). The bytes above are untouched; this addendum is filed at the assigned
path rather than replacing them. Same tip `4436e279…`; same blob digests (`163e9bdb…` supplement, `94ddc7dc…`
counter, `6b975f91…` tool; archive digests equal `git show 4436e279:<path>`). Lane `HEAD` is `72566c84…`;
`git diff --stat 4436e279 HEAD -- <the three files>` printed nothing (HEAD adds only the wave-2 spec/dispatch).

The sibling's 50 supplement runs hit no crash. Mine did, on unseeded run #3 — the latent defect is observable
at run level. All runs: cwd = tree root, `env -u ASSIMILATE_CITES`, Python 3.14.8.

## A1. Matrix (50 supplement runs + 40 counter seeds)

Command: `python3 /dev/shm/chousa-r51-R51W2ExecSeedSupplement/flake-matrix-59.py` (script in A6); wall
510.91 s, harness `EXIT=0`.

```
SUPPLEMENT: u1:rc0/PASS u2:rc0/PASS u3:rc1/FAIL u4:rc0/PASS u5:rc0/PASS u6:rc0/PASS u7:rc0/PASS u8:rc0/PASS u9:rc0/PASS u10:rc0/PASS u11:rc0/PASS u12:rc0/PASS u13:rc0/PASS u14:rc0/PASS u15:rc0/PASS u16:rc0/PASS u17:rc0/PASS u18:rc0/PASS u19:rc0/PASS u20:rc0/PASS u21:rc0/PASS u22:rc0/PASS u23:rc0/PASS u24:rc0/PASS u25:rc0/PASS s1:rc0/PASS s2:rc0/PASS s3:rc0/PASS s4:rc0/PASS s5:rc0/PASS s6:rc0/PASS s7:rc0/PASS s8:rc0/PASS s9:rc0/PASS s10:rc0/PASS s11:rc0/PASS s12:rc0/PASS s13:rc0/PASS s14:rc0/PASS s15:rc0/PASS s16:rc0/PASS s17:rc0/PASS s18:rc0/PASS s19:rc0/PASS s20:rc0/PASS s21:rc0/PASS s22:rc0/PASS s23:rc0/PASS s24:rc0/PASS s25:rc0/PASS
SHAPE=49/49
MUTATION=49/49
CROSS_ENTRY=49/49
SOURCE_LINE=49/49
UNKNOWN_SRC=49/49
CLASH=49/49
C1_SUPPLEMENT=49/49
FIRST NON-PASS SUPPLEMENT RUN: corpus/evidence/round51/c1-supplement.py rc= 1
Traceback (most recent call last):
  File "/dev/shm/chousa-r51-R51W2ExecSeedSupplement/tree/corpus/evidence/round51/c1-supplement.py", line 189, in <module>
    sys.exit(main())
    ~~~~^^^^^^^^^^
  File "/dev/shm/chousa-r51-R51W2ExecSeedSupplement/tree/corpus/evidence/round51/c1-supplement.py", line 174, in main
    for k, v in one_round(tool, tmp, rnd).items():
                ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/dev/shm/chousa-r51-R51W2ExecSeedSupplement/tree/corpus/evidence/round51/c1-supplement.py", line 115, in one_round
    rc_c1 = subprocess.run([sys.executable, str(EV / "c1-count.py"), "--tool", str(tool), "--seed", str(safe_seed(rnd))],
                           capture_output=True, text=True, timeout=300, env=ENV)
  File "/usr/lib/python3.14/subprocess.py", line 557, in run
    stdout, stderr = process.communicate(input, timeout=timeout)
                     ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/subprocess.py", line 1221, in communicate
    stdout, stderr = self._communicate(input, endtime, timeout)
                     ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/subprocess.py", line 2154, in _communicate
    self._check_timeout(endtime, orig_timeout, stdout, stderr)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/subprocess.py", line 1268, in _check_timeout
    raise TimeoutExpired(
    ...<2 lines>...
            stderr=b''.join(stderr_seq) if stderr_seq else None)
subprocess.TimeoutExpired: Command '['/usr/bin/python3', '/dev/shm/chousa-r51-R51W2ExecSeedSupplement/tree/corpus/evidence/round51/c1-count.py', '--tool', '/dev/shm/chousa-r51-R51W2ExecSeedSupplement/tree/tools/assimilate-rows.py', '--seed', '356404454']' timed out after 300 seconds
```

Each `49/49` tally counts the 49 runs that reached a verdict (the crashed run prints no leg lines; `main`
prints only at the end, `c1-supplement.py:172-181`). The crash seed is accepted by `safe_seed`'s screen but
collides in the counter's draw order:

```
$ python3 -c "import random; ..."   # exact safe_seed body vs c1-count.py:121-123
safe_check= (511, 515) True actual= (515, 515) collide= True
```

`c1-supplement.py:115-116` has no `try`, so the 300 s stall ends as an uncaught `TimeoutExpired` → rc 1 and
no `C1_SUPPLEMENT=` line. The supplement's `finally` removes its temp dir; the counter is SIGKILLed before
its `finally`.

## A2. Counter seeds: the assignment's screen admits a hang

The literal screen (`Random(N)` → `randint(12,40)`, then two `randint(500,900)` that differ) accepts every
N in 1..40, so the 40 seeds are 1..40. Each run under a 60 s cap (`pre->actual`, rc):

```
1:791/891->891/532:rc0 | 2:528/546->528/546:rc0 | 3:803/778->778/566:rc0 | 4:655/552->552/869:rc0 | 5:630/879->879/683:rc0 | 6:793/541->541/748:rc0 | 7:577/702->702/833:rc0 | 8:689/692->692/564:rc0 | 9:813/691->691/636:rc0 | 10:516/719->719/747:rc0
11:786/899->786/899:rc0 | 12:637/836->836/770:rc0 | 13:648/850->850/850:rc124:HANG | 14:815/859->859/886:rc0 | 15:505/766->505/766:rc0 | 16:740/746->746/645:rc0 | 17:712/655->655/687:rc0 | 18:562/838->838/729:rc0 | 19:522/766->766/561:rc0 | 20:870/851->851/892:rc0
21:714/853->853/714:rc0 | 22:624/512->624/512:rc0 | 23:648/542->648/542:rc0 | 24:696/798->798/593:rc0 | 25:893/507->507/609:rc0 | 26:603/837->837/605:rc0 | 27:745/859->859/641:rc0 | 28:880/566->566/779:rc0 | 29:538/677->677/806:rc0 | 30:648/812->648/812:rc0
31:740/557->557/891:rc0 | 32:609/574->574/655:rc0 | 33:585/823->823/619:rc0 | 34:682/799->799/514:rc0 | 35:671/884->884/567:rc0 | 36:529/510->510/645:rc0 | 37:811/546->546/816:rc0 | 38:715/719->719/886:rc0 | 39:632/697->697/513:rc0 | 40:796/768->768/516:rc0
COUNT_FAILS=1/40
```

N=13 verbatim: `COUNT N=13 pre=(648, 850) actual=(850,850) collide=True rc=124 C1=None
out_tail=['SELFTEST_DEFAULT=PASS', 'LEGACY_ALL=PASS rc=0']`. Independent shorter kill:
`timeout 20 python3 -u corpus/evidence/round51/c1-count.py --seed 13` → those two lines then `RC=124`.
Control with the screen aligned to the counter's order (`getrandbits(32)`, `randint(12,40)`, then the two
ids): seeds `[1..12,14..41]`, `ALIGNED_PRECHECK_FAILS=0/40`, rc 0 each — the counter is deterministic; only
the screen/`safe_seed` is misaligned.

## A3. Rate (own measurement, seeds 0..199999)

```
samples=200000 accept=199505 hangs=522 accepted_and_hang=399 P(hang|accept)=0.002000 1/500.0
P(run hits, 3 rounds)=0.005988 ~ 1/167
```

So ~0.6 % of supplement runs should crash; the 25 unseeded runs produced one (u3), consistent (≈14 % over 25).

## A4. Timing

`time env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-supplement.py --seed 1` → 6/6, rc 0,
`real 0m3.398s`. `time … c1-count.py --seed 7 >/dev/null` → `C1=PASS`, `real 0m0.682s`. The crashed run:
300 s (traceback) plus interpreter start; whole matrix 510.91 s = 49 clean supplements + 300 s crash + 39
counter runs + 60 s seed-13 cap.

## A5. What holds, and two side observations

- E3 mitigation works: `ASSIMILATE_CITES=all python3 corpus/evidence/round51/c1-supplement.py --seed 1` →
  `SUPPLEMENT_LEGS=6/6`, `C1_SUPPLEMENT=PASS`, rc 0; the same ambient on the frozen counter (`--seed 7`) →
  `LEGS=3/5`, `C1=FAIL`, rc 1. `ENV` strips the variable for the helper and the SHAPE subprocess.
- Crash shape reproduced at 5 s on a scratch COPY (`tree2`) with `safe_seed` forced to 13 and only the SHAPE
  timeout lowered 300→5: `TimeoutExpired` traceback at `:115-116`, rc 1, no verdict line (`real 0m5.056s`).
  The original line was not touched.
- `ls -d /tmp/chousa-r51-c1-* | wc -l` → 20, each 0 bytes: a SIGKILLed counter never runs
  `finally: shutil.rmtree(tmp)`. Left in place (outside my scratch; possibly siblings').
- Citation: `grep -n '^## E' corpus/evidence/round51/claims-erratum.md` → only `5:## E1`; E2/E3/E4 are at
  `corpus/lessons/round-51.md:182-184`. `c1-supplement.py:4` and `corpus/QUALITY.md:916` say
  "claims-erratum.md E2-E4" — wrong file.

## A6. Script (59 lines, verbatim; run from the extracted tree root)

```python
#!/usr/bin/env python3
"""r51 flake matrix: 25 unseeded + 25 seeded supplement runs, 40 pre-checked c1-count seeds."""
import os, random, subprocess, sys
ENV = {k: v for k, v in os.environ.items() if k != "ASSIMILATE_CITES"}
SUP, CNT = "corpus/evidence/round51/c1-supplement.py", "corpus/evidence/round51/c1-count.py"

def run(args, t):
    try:
        r = subprocess.run([sys.executable, *args], capture_output=True, text=True, env=ENV, timeout=t)
        return r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired as e:
        out = e.stdout or b""
        return 124, out.decode(errors="replace") if isinstance(out, bytes) else out, "TIMEOUT"

def legs(out):
    d = {}
    for ln in out.splitlines():
        if "=" in ln:
            k, v = ln.split("=", 1)
            if k.isupper() and v.split()[0] in ("PASS", "FAIL"):
                d[k] = v.split()[0]
    return d

def pre(n):
    r = random.Random(n); r.randint(12, 40)
    return r.randint(500, 900), r.randint(500, 900)

def actual(n):
    r = random.Random(n); r.getrandbits(32); r.randint(12, 40)
    return r.randint(500, 900), r.randint(500, 900)

rows, tally, first_bad = [], {}, None
for i in range(1, 51):
    args = [SUP] if i <= 25 else [SUP, "--seed", str(i - 25)]
    rc, out, err = run(args, 400)
    L = legs(out)
    ok = rc == 0 and L.get("C1_SUPPLEMENT") == "PASS"
    name = ("u%d" if i <= 25 else "s%d") % (i if i <= 25 else i - 25)
    rows.append((name, rc, ok))
    for k, v in L.items(): tally.setdefault(k, []).append(v)
    if not ok and first_bad is None: first_bad = (args, rc, out, err)
print("SUPPLEMENT:", " ".join(f"{n}:rc{rc}/{'PASS' if ok else 'FAIL'}" for n, rc, ok in rows))
for k, vs in tally.items(): print(f"{k}={sum(v == 'PASS' for v in vs)}/{len(vs)}")
if first_bad:
    a, rc, out, err = first_bad
    print("FIRST NON-PASS SUPPLEMENT RUN:", " ".join(a), "rc=", rc, "\n" + out + err)
else: print("FIRST NON-PASS SUPPLEMENT RUN: none")
seeds, n = [], 1
while len(seeds) < 40:
    a, b = pre(n)
    if a != b: seeds.append(n)
    n += 1
bad = 0
for s in seeds:
    ca, cb = actual(s); rc, out, _ = run([CNT, "--seed", str(s)], 60)
    L = legs(out); ok = rc == 0 and L.get("C1") == "PASS"; bad += not ok
    print(f"COUNT N={s} pre={pre(s)} actual=({ca},{cb}) collide={ca == cb} rc={rc} C1={L.get('C1')}"
          + (" out_tail=" + repr(out.splitlines()[-2:]) if rc == 124 else ""))
print(f"COUNT_FAILS={bad}/40")
```

VERDICT: attacked the supplement and the frozen counter at 4436e279 with 50 supplement runs and 40 screened
counter seeds — found and OBSERVED the crash the sibling only derived: unseeded run #3 hit a `safe_seed`
blind spot (`--seed 356404454`, its screen draws 511/515, the counter draws 515/515), stalled 300 s and died
in an uncaught `TimeoutExpired` (rc 1, no `C1_SUPPLEMENT=` line); the assignment's own screen likewise admits
the hang seed 13 (rc 124); with the screen aligned the counter is 40/40 PASS.
