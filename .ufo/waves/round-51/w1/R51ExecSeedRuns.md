# R51ExecSeedRuns — flake and independence check of the frozen C1 counter

Scope: `corpus/evidence/round51/c1-count.py` against an export of the candidate `tools/assimilate-rows.py` at
`2a3389da0306e41f1b4797c1bc69017f23a38aef` (`git -C …/chousa-shokunin archive 2a3389d | tar -x -C
/dev/shm/chousa-r51-R51ExecSeedRuns/tree`). Counter not edited, no production file written, no tool installed.

## 0. Revisions pinned (the round-50 "pin the revision measured" defect)

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ for rev in 2a3389da d603f6f0 cfe6c9fb; do printf '%s ctr=%s tool=%s\n' "${rev:0:7}" \
    "$(git show $rev:corpus/evidence/round51/c1-count.py | sha256sum | cut -c1-16)" \
    "$(git show $rev:tools/assimilate-rows.py | sha256sum | cut -c1-16)"; done
2a3389d ctr=94ddc7dc273c8314 tool=bdaf80f43f398270
d603f6f ctr=94ddc7dc273c8314 tool=382aca9b7e314180
cfe6c9f ctr=94ddc7dc273c8314 tool=bdaf80f43f398270
$ git merge-base --is-ancestor d603f6f 2a3389d && echo "d603f6f IS ancestor of 2a3389d"
d603f6f IS ancestor of 2a3389d
```

The counter is byte-identical at the claims freeze (`d603f6f`), the candidate (`2a3389d`) and the tip (`cfe6c9f`):
every number below is the frozen counter. The measured tool blob (`bdaf80f4…`) is the candidate and the tip;
`d603f6f` is its pre-candidate ancestor, so no post-freeze tool drift.

## 1. 50-run sweep: 49 runs 5/5, run 38 (seed 13) never finishes

`sweep.py` (§5, 46 lines) runs the counter 25× with no seed (fresh `os.urandom` nonce) and 25× with `--seed 1..25`,
90 s per-run cap. Header, the one defect and the tail of that output, verbatim:

```
counter=/dev/shm/chousa-r51-R51ExecSeedRuns/tree/corpus/evidence/round51/c1-count.py per_run_timeout=90s
run  seed  rc LEGS   C1
--- FIRST DEFECT run=38 seed=13 rc=124 ---
--- stdout ---
SELFTEST_DEFAULT=PASS
LEGACY_ALL=PASS rc=0
--- stderr ---
--- end ---
RUNS=50 DEFECTS=1
```

All 50 per-run rows of the same output, reflowed five per line (nothing else changed):

```
 1:-  0 5/5 PASS |  2:-  0 5/5 PASS |  3:-  0 5/5 PASS |  4:-  0 5/5 PASS |  5:-  0 5/5 PASS
 6:-  0 5/5 PASS |  7:-  0 5/5 PASS |  8:-  0 5/5 PASS |  9:-  0 5/5 PASS | 10:-  0 5/5 PASS
11:-  0 5/5 PASS | 12:-  0 5/5 PASS | 13:-  0 5/5 PASS | 14:-  0 5/5 PASS | 15:-  0 5/5 PASS
16:-  0 5/5 PASS | 17:-  0 5/5 PASS | 18:-  0 5/5 PASS | 19:-  0 5/5 PASS | 20:-  0 5/5 PASS
21:-  0 5/5 PASS | 22:-  0 5/5 PASS | 23:-  0 5/5 PASS | 24:-  0 5/5 PASS | 25:-  0 5/5 PASS
26:1  0 5/5 PASS | 27:2  0 5/5 PASS | 28:3  0 5/5 PASS | 29:4  0 5/5 PASS | 30:5  0 5/5 PASS
31:6  0 5/5 PASS | 32:7  0 5/5 PASS | 33:8  0 5/5 PASS | 34:9  0 5/5 PASS | 35:10 0 5/5 PASS
36:11 0 5/5 PASS | 37:12 0 5/5 PASS | 38:13 124 ?  ?   | 39:14 0 5/5 PASS | 40:15 0 5/5 PASS
41:16 0 5/5 PASS | 42:17 0 5/5 PASS | 43:18 0 5/5 PASS | 44:19 0 5/5 PASS | 45:20 0 5/5 PASS
46:21 0 5/5 PASS | 47:22 0 5/5 PASS | 48:23 0 5/5 PASS | 49:24 0 5/5 PASS | 50:25 0 5/5 PASS
```

`rc=124` is my cap — the counter has no timeout of its own; it printed the two self-reported legs and stopped before `SOURCE_ONLY`, i.e. it spins in nonce generation, not in the tool.

## 2. Mechanism: the id-dedup loop cannot terminate when `a_id == b_id`

`c1-count.py:123-125` (export, byte-identical to the freeze):

```
        a_id, b_id, c_id = (f"S{rnd.randint(500, 900)}" for _ in range(3))
        while len({a_id, b_id, c_id}) < 3:
            c_id = f"S{rnd.randint(500, 900)}"
```

Only `c_id` is redrawn, so `a_id == b_id` pins the set size at 2 forever. SIGINT at 8 s lands there:

```
$ timeout -s INT 8 python3 corpus/evidence/round51/c1-count.py --seed 13
SELFTEST_DEFAULT=PASS
LEGACY_ALL=PASS rc=0
Traceback (most recent call last):
  File ".../corpus/evidence/round51/c1-count.py", line 219, in <module>
    sys.exit(main())
  File ".../corpus/evidence/round51/c1-count.py", line 125, in main
    c_id = f"S{rnd.randint(500, 900)}"
    ^^^^
KeyboardInterrupt
```

A class, not one seed — the next colliding seeds hang too: `timeout 15 … --seed 182` printed the same two legs and
`SEED182_EXIT=124`; `timeout 12 … --seed 324` likewise, `SEED324_EXIT=124`.

Rate on the counter's own draw order (seed → `getrandbits(32)`, `randint(12,40)`, three `randint(500,900)`), 100 000
seeds: `a_id==b_id in 250 seeds = 0.00250` (1/401 = 0.00249); first colliding seeds 13, 182, 324, 1001, 1180, 2336.
Every invocation, seeded or not, has a 1/401 chance of an unbounded hang. Against the frozen target ("`LEGS=5/5`,
`C1=PASS` exit 0, on at least three independent runs … and with `--seed` fixed in one of them") that is ≈0.75 % for the
three fresh runs plus 0.25 % for the fixed-seed run — and the failure mode is a stall, not a FAIL, so an unattended
gate never returns and never prints `C1=FAIL`. Side effect: `/tmp/chousa-r51-c1-*` scratch dirs survive killed runs
(5 empty dirs, 0 bytes each, after my probes); left in place in case a sibling was mid-run.

Proposed counter repair for the L1 (not applied — the counter is frozen this round): draw three distinct ids at once,
e.g. `a_id, b_id, c_id = (f"S{i}" for i in rnd.sample(range(500, 901), 3))`, or redraw the whole triple in the loop; the
predicate, target, controls and legs are untouched.

## 3. Manual SOURCE_ONLY: the oracle is right

`manual_source_only.py` (§5, 53 lines) imports the counter by path and builds the (S) package with the counter's own
`row()`/`registry()`/`adopt()` helpers — `top=17`, `a=S641`, `b=S703`, `c=S522`, `held_n=5`, `host=h9f3c2a11.example.test`
— then applies the adopter and prints what it wrote:

```
$ python3 manual_source_only.py
===== default (--cites source) rc=0 =====
--- stdout ---
COLLISIONS=0
CITED=2 APPEND=1 HELD=1
BODYONLY=1
--- renumber.tsv ---
staged_id	lane_id	action	url
S641	S018	append	h9f3c2a11.example.test/new-a-9f3c2a11
S703	S005	held	h9f3c2a11.example.test/held-9f3c2a11

--- append.md ---
| S018 | New A — https://h9f3c2a11.example.test/new-a-9f3c2a11 | docs | B | scope S018 | section S018 | what S018 teaches | mined | 2026-10-25 | 90d | corpus/knowledge/e.md |

--- rewritten entry ---
source: S018 — https://h9f3c2a11.example.test/new-a-9f3c2a11 — section
source: S005 — https://h9f3c2a11.example.test/held-9f3c2a11 — section
verified-at: 2026-10-25
recheck: 90d

# E

- A says one thing (S018); B another (S005).
- A different document is mentioned only here: S522, and lane row S005 too.

--- bodyonly.tsv ---
entry	staged_id
corpus/knowledge/e.md	S522
```

The same package with `--cites all` (the script's second run, `CITED=3 APPEND=2 HELD=1`) mapped `S522→S018 append`,
`S641→S019 append`, `S703→S005 held`, wrote two `append.md` rows (`S018` = Body only C, `S019` = New A), rewrote the
entry to `S019`/`S005`/`S018`, and wrote no `bodyonly.tsv`. Against the counter's assertions (`c1-count.py:154-157`):
`set(ren) == {a,b}`, `ren[a] == [S018,"append"]`, `ren[b] == [S005,"held"]`, exactly one appended row starting `S018`,
`c` still in the entry, `a`/`b` gone from the entry, `bodyonly.tsv == [[entry, c]]`, `BODYONLY=1` — all hold, and the
twin gives the round-50 reading. The two runs are mutual controls: an always-source-only tool fails `ok_all`, an
always-all-tokens tool fails `ok_s`. The oracle is right on this package, so `SOURCE_ONLY` is not an artefact of which
ids it drew.

## 4. Independence

- Inputs: `grep -n 'LANE\|shokuknow\|root' c1-count.py` → only `LANE` for the default tool path and the round-50
  fixtures (`:45-46`) and `--root/--tool` (`:93-97`). No reference to the staged merge package (`shokuknow` absent),
  no import of the tool (subprocess only, `run()`); nonces are drawn at counting time and the counter writes only
  under `tempfile.mkdtemp`.
- Not vacuous: `python3 c1-count.py --tool …/stub_ok.py --seed 5` (stub = `sys.exit(0)`) → `LEGACY_ALL=FAIL rc=0`,
  `SOURCE_ONLY=FAIL … map=[] appended=0 bodyonly=[]`, `PIPE_IDENTITY=FAIL d1=no d2=no`, `REGISTRY_STRUCTURE=FAIL 0/4`,
  `LEGS=1/5`, `C1=FAIL`, exit 1.
- Not location-bound: the same tool copied outside the lane passes (`--tool …/copytool.py --seed 7` → `LEGS=5/5`,
  `C1=PASS`, exit 0).
- Two of five legs are tool-self-reported: `SELFTEST_DEFAULT` (`:107`) greps `SELFTEST=PASS` from the tool's stdout
  and `LEGACY_ALL` (`:114-115`) parses the tool's printed `findings=`/`FIXTURES_SHA256=` lines. With `--tool`,
  `SELFTEST_DEFAULT` is skipped and counted PASS — a free leg, as disclosed at `claims.md:44-48`. The three
  counter-oracle legs are what make `LEGS=5/5` mean anything.
- Residual, not a defect under the frozen predicate: hosts, ids, `top`, `held_n` vary per run, but the templates are
  literals — `"New A — "`, `"Held B — "`, `"Body only C — "` and the entry body at `c1-count.py:142-147`,
  `"Held doc \\| alt"` at `:176`; value-level freshness does not defeat shape recognition.

## 5. Scripts

`/dev/shm/chousa-r51-R51ExecSeedRuns/sweep.py` (46 lines) — the required sweep:

```python
#!/usr/bin/env python3
"""Seed sweep for corpus/evidence/round51/c1-count.py against the candidate tool.

25 runs unseeded (fresh os.urandom nonce) + 25 runs with --seed N, N=1..25,
from the exported candidate tree. Tabulates LEGS and C1 per run; the first run
that is not 5/5 has its full stdout/stderr printed. A run that exceeds
PER_RUN seconds is recorded as HANG (the counter loops forever on some seeds).
"""
import pathlib
import re
import subprocess
import sys

TREE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/dev/shm/chousa-r51-R51ExecSeedRuns/tree")
CTR = TREE / "corpus/evidence/round51/c1-count.py"
PER_RUN = 90
LEGS = re.compile(r"^LEGS=(\d+)/(\d+)$", re.M)
C1 = re.compile(r"^C1=(PASS|FAIL)$", re.M)


def once(*flags):
    try:
        r = subprocess.run([sys.executable, str(CTR), *flags], cwd=TREE,
                           capture_output=True, text=True, timeout=PER_RUN)
        rc, out, err = r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired as e:
        dec = lambda v: v.decode("utf-8", "replace") if isinstance(v, bytes) else (v or "")
        rc, out, err = 124, dec(e.stdout), dec(e.stderr)
    m, c = LEGS.search(out), C1.search(out)
    return rc, (f"{m.group(1)}/{m.group(2)}" if m else "?"), (c.group(1) if c else "?"), out, err


bad = 0
print(f"counter={CTR} per_run_timeout={PER_RUN}s")
print(f"{'run':>3} {'seed':>5} {'rc':>3} {'LEGS':>4} {'C1':>4}")
for i in range(1, 51):
    seed = None if i <= 25 else i - 25
    rc, legs, c1, out, err = once(*(() if seed is None else ("--seed", str(seed))))
    print(f"{i:>3} {('-' if seed is None else seed):>5} {rc:>3} {legs:>4} {c1:>4}")
    if not (rc == 0 and legs == "5/5" and c1 == "PASS"):
        bad += 1
        if bad == 1:
            print(f"--- FIRST DEFECT run={i} seed={seed} rc={rc} ---")
            print(f"--- stdout ---\n{out}--- stderr ---\n{err}--- end ---")
print(f"RUNS=50 DEFECTS={bad}")
sys.exit(0 if bad == 0 else 1)
```

`manual_source_only.py` (53 lines) is the §3 hand application; it differs from the counter only in that the nonce
values are written down instead of drawn, and it calls the counter's `adopt()` unchanged.

VERDICT — attacked the frozen C1 counter for flake and independence: 49/50 runs are a clean `LEGS=5/5 C1=PASS`, but its nonce generator hangs forever when its first two id draws collide (`a_id == b_id`, 1/401 per run; seeds 13, 182, 324 confirmed hanging, 1001/1180/2336 derived), and its SOURCE_ONLY oracle, hand-checked on a package built with the counter's own helpers, is correct.
