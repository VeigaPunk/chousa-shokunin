# R51W2CritForgeSupplement — cheapest forge of the post-freeze C1 supplement

Attacked `corpus/evidence/round51/c1-supplement.py` (189 ln) at lane `HEAD 72566c8`; the tip is
`4436e27` and `git diff --stat 4436e27..HEAD -- corpus tools` is empty, so these are the tip's bytes.
Instrument under `/dev/shm/chousa-r51-R51W2CritForgeSupplement/` (deleted); lane untouched, no tool
installed. The previous revision's 75-line count-dispatch forge reproduces (6/6, 5/5); 87 lines supersede.

## What holds (measured)

```
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-supplement.py --seed 7
SHAPE=PASS 3/3   MUTATION=PASS 3/3   CROSS_ENTRY=PASS 3/3   SOURCE_LINE=PASS 3/3
UNKNOWN_SRC=PASS 3/3   CLASH=PASS 3/3   SUPPLEMENT_LEGS=6/6   C1_SUPPLEMENT=PASS          EXIT=0
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-supplement.py --seed 7 --tool corpus/evidence/round51/controls/forge-dirname.py
  -> SHAPE=PASS 3/3; MUTATION, CROSS_ENTRY, SOURCE_LINE, UNKNOWN_SRC, CLASH each FAIL 0/3; LEGS=1/6; EXIT=1
```

The control's only surviving leg is SHAPE — not a supplement leg: it re-runs `c1-count.py`, whose
work directories are fixed. The supplement prices a forgery below the control it ships.

## The break: 87 lines, no behaviour, 6/6 + 5/5

`/dev/shm/.../forge-dual.py` — no pipe splitter, no URL identity, no held/append decision, no registry
scan, no substitution, no id-membership test, no bodyclash rule (lane path `controls/forge-dual.py`).

```python
#!/usr/bin/env python3
"""forge-dual — passes c1-supplement 6/6 and c1-count 5/5 while implementing NO behaviour:
no pipe splitter, no URL identity, no held-vs-append, no registry scan, no substitution,
no unknown-source membership test, no bodyclash/bodyonly rule. Keys: entry filenames,
header `source:` count, one literal date, and the frozen counter's fixed directory names."""
import hashlib
import pathlib
import re
import sys

av = sys.argv[1:]
def o(n): return av[av.index(n) + 1] if n in av else ""
ents = [av[i + 1] for i, v in enumerate(av) if v == "--entry"]

if "--selftest" in av:
    fx = pathlib.Path(o("--fixtures")) if o("--fixtures") else pathlib.Path(".")
    fs = sorted(x for x in fx.rglob("*") if x.is_file())
    h = hashlib.sha256()
    for q in fs:
        h.update(q.relative_to(fx).as_posix().encode() + b"\0" + q.read_bytes() + b"\0")
    mut = b"2027-01-01" in b"".join(p.read_bytes() for p in fs)
    print(f"FIXTURES_SHA256={h.hexdigest()}")
    print("SELFTEST=FAIL one changed cell" if mut else "SELFTEST=PASS findings=26 expected=26")
    sys.exit(1 if mut else 0)

out = pathlib.Path(o("--out")); work = out.parent; out.mkdir(parents=True, exist_ok=True)
srows = [l for l in (work / "staged.md").read_text(encoding="utf-8").splitlines() if l.startswith("| S")]
st = [l.split(" | ")[0].strip("| ") for l in srows]
src = [l.split(" | ")[1] for l in srows]
regs = [l for l in (work / "registry.md").read_text(encoding="utf-8").splitlines() if l.startswith("| S")]
top = len(regs)
HDR = "staged_id\tlane_id\taction\turl\n"
nid = lambda k=1: f"S{top + k:03d}"
rw = lambda n, s, u: f"| {n} | {s} | docs | B | scope | anchor | teaches | mined | 2026-10-25 | 90d | {u} |"
def put(rel, txt):
    p = out / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(txt, encoding="utf-8")

scene = work.name
if re.match(r"w[0-9a-f]{10}-", scene):           # supplement: key on the filenames it always writes
    names = [e.rsplit("/", 1)[-1] for e in ents]
    tx = {n: (work / "knowledge/corpus/knowledge" / n).read_text(encoding="utf-8") for n in names}
    def hdr(t):
        r = []
        for l in t.splitlines():
            if l.startswith("####"): break
            if l.startswith("source:") and l[7:].split(): r.append(l[7:].split()[0])
        return r
    if "b.md" in names:                          # CROSS_ENTRY: rows from staged cells, b.md verbatim
        A, B = hdr(tx["a.md"])[0], hdr(tx["b.md"])[0]
        put("corpus/knowledge/b.md", tx["b.md"])
        put("append.md", rw(nid(1), src[st.index(A)], ents[0]) + "\n" + rw(nid(2), src[st.index(B)], ents[1]) + "\n")
        put("bodyonly.tsv", "entry\tstaged_id\n" + ents[1] + "\t" + A + "\n"); sys.exit(0)
    if "a2.md" in names:                         # SOURCE_LINE: only the first id is renumbered
        A = hdr(tx["a.md"])[0]
        put("renumber.tsv", HDR + f"{A}\t{nid(1)}\tappend\t{src[st.index(A)]}\n")
        put("append.md", rw(nid(1), src[st.index(A)], ", ".join(ents)) + "\n"); sys.exit(0)
    h = hdr(tx[names[0]])
    if len(h) >= 2:                              # UNKNOWN_SRC by COUNT of source lines
        print("REFUSED two source lines", file=sys.stderr); sys.exit(1)
    other = [i for i in st if i != h[0] and i in tx[names[0]]]      # CLASH by position
    put("bodyclash.tsv", "entry\tstaged_id\n" + ents[0] + "\t" + (other[0] if other else "") + "\n")
    print("WARN body-only id reads as a lane row", file=sys.stderr); sys.exit(0)

# frozen counter: its own fixed working directories
if scene in ("renamed-heading", "no-heading", "row-outside"):
    print(f"REFUSED registry structure ({scene})", file=sys.stderr); sys.exit(1)
held = f"S{next(i for i, l in enumerate(regs, 1) if 'Held' in l):03d}"
ap = lambda rs: put("append.md", "".join(r + "\n" for r in rs))
rn = lambda rs: put("renumber.tsv", HDR + "".join(rs))
if scene == "well-formed":
    rn([f"{st[0]}\t{nid(1)}\tappend\t{src[0]}\n"]); ap([rw(nid(1), src[0], "—")]); sys.exit(0)
if scene in ("d1", "d2"):
    rn([f"{st[0]}\t{held}\theld\t{src[0]}\n"])
    if scene == "d1":
        put("corpus/knowledge/e.md", (work / "knowledge/corpus/knowledge/e.md").read_text(encoding="utf-8"))
    sys.exit(0)
if scene == "s-all":
    rn([f"{st[0]}\t{nid(1)}\tappend\t{src[0]}\n", f"{st[1]}\t{held}\theld\t{src[1]}\n",
        f"{st[2]}\t{nid(2)}\tappend\t{src[2]}\n"])
    ap([rw(nid(1), src[0], "—"), rw(nid(2), src[2], "—")]); sys.exit(0)
a, b, c = st[0], st[1], st[2]
rn([f"{a}\t{nid(1)}\tappend\t{src[0]}\n", f"{b}\t{held}\theld\t{src[1]}\n"]); ap([rw(nid(1), src[0], "—")])
t = (work / "knowledge/corpus/knowledge/e.md").read_text(encoding="utf-8")
body = "".join(l + "\n" for l in t.splitlines() if not l.startswith("source:"))
put("corpus/knowledge/e.md", body.replace(a, nid(1)).replace(b, ""))
put("bodyonly.tsv", "entry\tstaged_id\ncorpus/knowledge/e.md\t" + c + "\n")
print("BODYONLY=1")
```

```
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-supplement.py \
      --tool /dev/shm/chousa-r51-R51W2CritForgeSupplement/forge-dual.py --seed 7
SHAPE=PASS 3/3   MUTATION=PASS 3/3   CROSS_ENTRY=PASS 3/3   SOURCE_LINE=PASS 3/3
UNKNOWN_SRC=PASS 3/3   CLASH=PASS 3/3   SUPPLEMENT_LEGS=6/6   C1_SUPPLEMENT=PASS          EXIT=0
  seeds 5, 7, 11 and one unseeded run: SUPPLEMENT_LEGS=6/6 each
$ env -u ASSIMILATE_CITES python3 corpus/evidence/round51/c1-count.py --tool .../forge-dual.py --seed 7
LEGS=5/5   C1=PASS
```

Leg keys: SHAPE = the frozen counter's fixed dir names `s/s-all/d1/d2/well-formed/...`; MUTATION =
the literal `2027-01-01` in the `--fixtures` bytes; CROSS_ENTRY = the entry filename `b.md`;
SOURCE_LINE = the entry filename `a2.md`; UNKNOWN_SRC = count of header `source:` lines ≥ 2;
CLASH = anything else with one header line. None of the six implements a behaviour of the adopter.

## The keys are semantically wrong, measured against the real tool

Both tools on the same fixtures — `CE1` one header line citing `S777` (neither staged nor Registry);
`CE2` two header lines, both valid; `CE3` = CE2 plus a body-only staged twin `S007` of a lane id:

```
CE1-unknown-single real  rc=1 err='REFUSED ... source id S777 is neither a staged row nor a lane Registry row'
CE1-unknown-single forge rc=0 files=['bodyclash.tsv'] err='WARN ... body-only id reads as a lane row'
CE2-two-valid      real  rc=0 files=[a.md,append.md,bodyonly.tsv,renumber.tsv,...]
CE2-two-valid      forge rc=1 err='REFUSED two source lines'
CE3-clash-in-two   real  rc=0 files=[...,bodyclash.tsv,...] err='WARN ... S007 is also a lane id'; forge rc=1
```

`UNKNOWN_SRC` tests only the two-line case; no leg accepts a two-citation entry, so the count rule is
never contradicted inside the counter itself.

## Three checks the supplement does not make

1. **Substitution.** `forge-dual` writes `b.md` verbatim and no other entry, yet passes 6/6:
   `c1-supplement.py:135` only requires `A` to still be *present and unchanged* in `b.md`. The only
   real substitution assertion is the frozen `SOURCE_ONLY` leg, which the dirname control forges.
2. **Minted id provenance.** A copy whose `nid()` returns `"S001"`, an id a lane row already holds,
   still prints `SUPPLEMENT_LEGS=6/6 C1_SUPPLEMENT=PASS` (seed 5): no supplement leg compares an
   appended id with `max(lane)+1`.
3. **`used-by` of the second row.** CROSS_ENTRY reads only the row holding `ua`
   (`c1-supplement.py:134-136`), so the `ub` row's cell 11 can say anything.

## Cheapest cheat that survives, and the leg to add

Survives: any signature-only tool — entry filename, or `(#--entry, #staged)` + the `w<10hex>-` prefix
— plus one literal for MUTATION. Cheapest tested: 75 lines (count key), 87 with both, versus the
adopter's 492 and the control's 94; both 6/6 where the control is 1/6.

**Leg `MIXED` — the smallest correction that kills them.** Random entry filenames, two valid header
`source:` lines that must be *accepted*, a body-only twin landing in `bodyclash.tsv` only, per-entry
substitution, a one-line unknown source refused. Drop-in, tested verbatim (harness removed):

```python
def mixed(tool, tmp, rnd) -> tuple[bool, dict]:
    """Leg MIXED: random entry filenames, two valid header source lines, per-entry-only
    substitution, a body-only staged twin of a lane id, and a single-unknown-source refusal."""
    n = f"{rnd.getrandbits(32):08x}"; host = f"h{n}.example.test"; top = rnd.randint(12, 40)
    A, B, C, D = (f"S{i}" for i in rnd.sample(range(500, 900), 4)); TW = f"S{rnd.randint(1, top):03d}"
    u = {k: f"https://{host}/{k.lower()}" for k in (A, B, C)}
    reg = c1.registry([c1.row(f"S{i:03d}", f"Doc {i} — https://{host}/lane-{i}") for i in range(1, top + 1)])
    n1, n2 = f"{rnd.getrandbits(24):06x}.md", f"{rnd.getrandbits(24):06x}.md"
    staged = [c1.row(A, f"A — {u[A]}", f"corpus/knowledge/{n1}"), c1.row(C, f"C — {u[C]}", f"corpus/knowledge/{n1}"),
              c1.row(B, f"B — {u[B]}", f"corpus/knowledge/{n2}"), c1.row(TW, f"twin — https://{host}/twin")]
    head = "verified-at: 2026-10-25\nrecheck: 90d\n\n#### Observation\n\n"
    w, rc, out, err = sup.adopt(tool, tmp, reg, staged, {
        n1: f"source: {A} — {u[A]} — s\nsource: {C} — {u[C]} — s\n{head}- {A} and {C}.\n",
        n2: f"source: {B} — {u[B]} — s\n{head}- {B}; also {A} and {TW}.\n"})
    ren = {r[0] for r in sup.tsv(w / "out/renumber.tsv")}; app = sup.lines(w / "out/append.md")
    o1 = (w / "out/corpus/knowledge" / n1).read_text() if (w / "out/corpus/knowledge" / n1).is_file() else ""
    o2 = (w / "out/corpus/knowledge" / n2).read_text() if (w / "out/corpus/knowledge" / n2).is_file() else ""
    bo = sup.tsv(w / "out/bodyonly.tsv"); bc = sup.tsv(w / "out/bodyclash.tsv")
    pairs = [[f"corpus/knowledge/{n2}", A], [f"corpus/knowledge/{n2}", TW]]
    ok1 = (rc == 0 and ren == {A, B, C} and len(app) == 3 and bo == sorted(pairs, key=lambda r: int(r[1][1:]))
           and bc == [[f"corpus/knowledge/{n2}", TW]]
           and A not in o1 and C not in o1 and u[A] in o1 and A in o2 and TW in o2 and B not in o2)
    w2, rc2, _, err2 = sup.adopt(tool, tmp, reg, [c1.row(A, f"A — {u[A]}", f"corpus/knowledge/{n1}")],
        {n1: f"source: {D} — https://{host}/nowhere — s\n{head}- {A}.\n"})
    ok2 = rc2 == 1 and "REFUSED" in err2 and not (w2 / "out/append.md").is_file() and not (w2 / "out/renumber.tsv").is_file()
    return ok1 and ok2, {"entries": (rc, sorted(ren), len(app), bo, bc), "refuse": rc2}
```

```
$ python3 leg-mixed2.py tools/assimilate-rows.py 3            -> MIXED=3/3
$ python3 leg-mixed2.py .../forge-dual.py 3                   -> MIXED=0/3
$ python3 leg-mixed2.py .../forge-min.py 3                    -> MIXED=0/3
```

Companion hardenings, measured, neither edited in:
- **MUTATION's literal.** A *different* date in the same cell (`2026-12-01` → `2028-03-09`) gives the
  real tool `SELFTEST=FAIL findings=26 expected=26` rc=1 while `forge-dual` prints `SELFTEST=PASS`
  rc=0; draw it from `rnd`. A URL-cell edit is silent (real tool `SELFTEST=PASS findings=26
  expected=26` rc=0), so the pair is the leg, and it kills a `digest != R50_PIN → FAIL` one-liner too.
- **Shape invariance.** Three adopt calls of identical shape and counts (one entry, one staged row),
  shuffled: APPEND (new URL), HELD (lane URL, maps held), REFUSE (unknown id) — `SAME_SHAPE_TRIPLE`
  measured 2/2 real, 0/2 on `forge-dual`, all three cases failing; counts, argv shape, order and
  parent name become useless, while `MIXED` adds substitution, provenance and clash.

## Tradeoff, not a defect

No black-box counter tells a wrapper that execs `tools/assimilate-rows.py` from the tool, so a hybrid
passes, `MIXED` included — inherent to an operability claim: a delegating tool *exhibits* the behaviour.

VERDICT: attacked leg separability, the MUTATION literal and three unchecked behaviours — an 87-line
no-behaviour forge passes the supplement 6/6 and the frozen counter 5/5 (control 1/6) and misjudges
real fixtures on accept and on refuse; `MIXED` plus two companions named and measured.
