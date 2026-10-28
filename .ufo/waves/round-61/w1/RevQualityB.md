# RevQualityB — round 61 w1 — draft QUALITY 119 (seeded leg order, process-group bound)
Scope: one criterion drafted and attacked; QUALITY.md, lane files and tools untouched; scratch removed; installs none.

## Findings

F1 — Red-before confirmed. First-freeze C1 counter (`1661b85`) runs 23 builder calls in one fixed order.
A call-counting forge (reference builder + preamble refusing every call index outside `{1..8,11}`) scores
`LEGS=20/20 C1=PASS` at seeds 61001, 61002, 61003. Its call log is identical at every seed.

F2 — Amendment A1 (`2b0e17b`, sha `f1d8b6fd`, lane HEAD) defeats the forge, and the shuffle is the operative
clause. Forge: 17, 14, 16 at seeds 61001–61003; 16, 17, 16, 15, 16, 17, 16 at 61004–61010. Same counter with
the shuffle line removed: 20/20 at 61001–61003.

F3 — Named hole in the process-group bound. A helper started with `start_new_session=True` still wrote its
marker 3 s after the amended counter exited (`escaped-session` present); a same-group helper was killed at
run end (`escaped-group` absent; present on first-freeze). The criterion must claim same-group descendants
only. A stronger bound (PID namespace, cgroup, subreaper sweep) is INFERENCE, not built.

F4 — First Check draft was too weak; fixed. Forge-at-fixed-seeds plus a source grep passed a seed-blind
counter (`random.Random(7919)`): forge 17/17/17, STRUCT all True. The Check now requires `ORDER seeds_differ=True`
from the forge's own per-seed call log. The seed-blind variant now prints `CHECK=FAIL`.

F5 — Limits. STRUCT is AST presence (dead `killpg(` passes it). The forge is pinned to the round-61 order; a
counter with another leg set must re-derive REF (INFERENCE: else VOID or a false score). Seed-from-fixture
inference by a builder was not tested.

## Evidence (ran; output trimmed)

- `git show 1661b85:…c1-count.py` vs `2b0e17b`: `start_new_session`, `RLIMIT_FSIZE`, `os.killpg`, and
  `random.Random(seed*7919+1).shuffle(order)` appear only in `2b0e17b`.
- Logging forge on `1661b85`, seed 61001: `LEGS=20/20 C1=PASS`. Call → leg: 1 P01; 2 P02; 3–5 P04; 6 P05;
  7–8 P06; 9–10 H07; 11 H08; 12–23 H09–H20 (one call each).
- `1661b85` + forge `{1..8,11}`: `LEGS=20/20 C1=PASS` ×3 seeds, exit 0.
- Amended + same forge: `LEGS=17/20`, `14/20`, `16/20` (exit 1); seeds 61004–61010 as F2.
- Amended, shuffle removed (copy) + forge: `LEGS=20/20 C1=PASS` ×3.
- Amended + reference `controls/ref-build-spans.py` (sha `86d64c31…`): `LEGS=20/20 C1=PASS` ×3 (positive control).
- Driver (76 lines below, sha `0c4c2854…`), `python3 -B driver --counter <c> --work <absent>`:
  - `1661b85`: `ORDER seeds_differ=False`, `STRUCT shuffle=False session=False killpg=False`,
    `FORGE_LEGS 20/20 ×3`, `CHECK=FAIL`, exit 1.
  - amended, real lane file: `ORDER seeds_differ=True`, `STRUCT True True True`, `REF_LEGS 20/20 ×3`,
    `FORGE_LEGS 17/20 14/20 16/20`, `CHECK=PASS`, exit 0.
  - seed-blind copy: `ORDER seeds_differ=False`, `FORGE_LEGS 17/17/17`, `CHECK=FAIL`, exit 1.
  - 26–33 s per run.

## Draft criterion (insert after criterion 118 as `## Round-61 addition`)

119. **A frozen counter that runs a candidate tool orders its legs by a seed the candidate cannot read, and
bounds each child run to its own process group; a call-counting forge must not reach full marks.** The
round-61 first-freeze C1 counter (`1661b85`) ran its 23 builder calls in a fixed order and killed only the
builder's pid on timeout, so a builder that counts its own invocations knows its leg: the reference builder
with a call-index preamble scored `LEGS=20/20 C1=PASS` at seeds 61001–61003 (ran). Amendment A1 (`2b0e17b`,
`corpus/evidence/round61/claims.md`) shuffled the legs and gave each child a session with a process-group
kill; the same forge then scored 14–17 and 20/20 with the shuffle removed (ran). The group bound covers only
descendants that stay in the child's group: a helper that starts its own session survived its run (ran).
Check: `python3 -B corpus/evidence/round61/controls/forge-call-count.py --counter corpus/evidence/round61/c1-count.py --work <absent dir>`
exits 0 `CHECK=PASS` only when `ORDER seeds_differ=True`, `STRUCT shuffle=True session=True killpg=True`, every
`FORGE_LEGS` is below 20/20 and every `REF_LEGS` is 20/20; `CHECK=VOID` (exit 2) if the reference is not 20/20.
Shown able to fail (ran): on `1661b85` `CHECK=FAIL`, `FORGE_LEGS` 20/20 ×3; on a copy whose shuffle uses
`random.Random(7919)`, `ORDER seeds_differ=False`, `CHECK=FAIL`. Named limits: the group bound does not stop a
helper that starts its own session (not claimed); STRUCT is presence, backed by the forge and ORDER; the forge
is pinned to the round-61 call order; a builder reading the seed from its fixture is not tested.

## Check driver (`corpus/evidence/round61/controls/forge-call-count.py`, lands beside `ref-build-spans.py`)

```python
#!/usr/bin/env python3
# QUALITY 119 Check (draft). Run: python3 -B controls/forge-call-count.py --counter PATH --work ABSENT_DIR
# Exit 0 CHECK=PASS · 1 CHECK=FAIL · 2 usage, or CHECK=VOID (reference not 20/20, QUALITY 115).
import ast, pathlib, re, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
REF = {1, 2, 3, 4, 5, 6, 7, 8, 11}  # call indices the reference serves at seed 61001 (first-freeze order)
SEEDS = (61001, 61002, 61003)
PRE = """import pathlib as _pl, os as _os, sys as _sys  # forge preamble (QUALITY 119 Check)
_W = _pl.Path(__file__).resolve().parents[2]
_F = _W / ".calls"
_N = (int(_F.read_text()) if _F.exists() else 0) + 1
_F.write_text(str(_N))
def _st(p):
    p = _pl.Path(p)
    if _os.path.islink(p): return "link"
    if not p.exists(): return "absent"
    return "file" if p.is_file() else "dir%d" % len(list(p.iterdir()))
_a = _sys.argv[1:]
_rows = sum(1 for _ in open(_a[_a.index("--quotes") + 1])) - 1
with open(__LOG__, "a") as _f:
    _f.write(f"{_N} check={'--check' in _a} replace={'--replace' in _a} out={_st(_a[_a.index('--out') + 1])} rows={_rows}\\n")
if _N not in __REF__:
    _sys.exit(2)
"""

def build(work, seed):
    src = (HERE / "ref-build-spans.py").read_text().splitlines(keepends=True)
    after = next(n.end_lineno for n in ast.parse("".join(src)).body[:3]
                 if isinstance(n, ast.ImportFrom) and n.module == "__future__")
    log = work.parent / f"calls-{seed}.log"
    log.unlink(missing_ok=True)
    pre = PRE.replace("__LOG__", repr(str(log))).replace("__REF__", repr(REF))
    fb = work.parent / f"forge-{seed}.py"
    fb.write_text("".join(src[:after]) + pre + "".join(src[after:]))
    return fb, log

def legs(counter, builder, work, seed):
    r = subprocess.run([sys.executable, "-B", str(counter), "--builder", str(builder), "--work", str(work),
                        "--seed", str(seed)], capture_output=True, text=True, timeout=900)
    m = re.search(r"LEGS=(\d+)/20", r.stdout)
    return int(m.group(1)) if m else -1

def structure(counter):
    calls = [n for n in ast.walk(ast.parse(counter.read_text())) if isinstance(n, ast.Call)]
    attr = lambda c: c.func.attr if isinstance(c.func, ast.Attribute) else None
    return {"shuffle": any(attr(c) == "shuffle" for c in calls),
            "session": any(k.arg == "start_new_session" and isinstance(k.value, ast.Constant)
                           and k.value.value is True for c in calls for k in c.keywords),
            "killpg": any(attr(c) == "killpg" for c in calls)}

def main():
    if len(sys.argv) != 5 or sys.argv[1] != "--counter" or sys.argv[3] != "--work":
        print("usage: forge-call-count.py --counter PATH --work ABSENT_DIR", file=sys.stderr); return 2
    counter, work = pathlib.Path(sys.argv[2]).resolve(), pathlib.Path(sys.argv[4]).resolve()
    if work.exists() and any(work.iterdir()):
        print(f"--work {work} must be absent or empty", file=sys.stderr); return 2
    work.mkdir(parents=True)
    forged, ref, orders = [], [], []
    for s in SEEDS:
        fb, log = build(work, s)
        forged.append(legs(counter, fb, work / f"f{s}", s))
        orders.append(log.read_text() if log.exists() else "")
        ref.append(legs(counter, HERE / "ref-build-spans.py", work / f"r{s}", s))
    seeded, st = len(set(orders)) > 1, structure(counter)
    print(f"ORDER seeds_differ={seeded}")
    print(f"STRUCT shuffle={st['shuffle']} session={st['session']} killpg={st['killpg']}")
    print("REF_LEGS " + " ".join(f"{s}={v}/20" for s, v in zip(SEEDS, ref)))
    print("FORGE_LEGS " + " ".join(f"{s}={v}/20" for s, v in zip(SEEDS, forged)))
    if any(v != 20 for v in ref):
        print("CHECK=VOID reference does not reach 20/20"); return 2
    ok = all(st.values()) and seeded and all(v < 20 for v in forged)
    print(f"CHECK={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
```

## Residual risk and gaps

- Driver ran only from a scratch controls directory: L1 lands it beside `ref-build-spans.py` and re-runs the three cases before binding.
- Not run: seed-from-fixture builders, dead-`killpg` counters, argv/tree-keyed forges (a different attack); the 3 s escape wait is one sample, not a bound.

VERDICT: CRITERION_CHECK_CAN_FAIL=yes text_ready=yes
