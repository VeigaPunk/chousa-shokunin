# R54ExecOleFuzz — robustness fuzz of the OLE `.doc` path of `tools/capture-text.py`

seat `R54ExecOleFuzz` (executor, chousa lane, round 54 w1), 2026-10-26. Frozen claim attacked:
**R54-C1** (operability), counter `corpus/evidence/round54/c1-count.py`. Candidate under test
`8a7d0f137a352000d78704ba5695ded8857104fe`, base `c49ffc6ce1c3de87c1dfa96856239ed7274bf07b`, lane
HEAD `9caf8fc`. No network: every pinned source is an on-disk capture under the read-only `.qcache`
of `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/`.

## 1. The fuzzer — 77 lines (`wc -l` = 77; budget was ≤80)

Path `/fast/scratch/hyaku/chousa-r54/R54ExecOleFuzz/fuzz.py`. It re-parses each seed with the
*lane tool's own* `Cfb` class (imported read-only), so every mutation offset is derived, not
guessed; §4 verifies each against the file bytes. `CTOOL` overrides the tool path (ran against the
frozen blob and the worktree); `$S` = scratch dir; seeds follow as argv.

```python
#!/usr/bin/env python3
"""fuzz.py - 600 mutants of the OLE .doc path of tools/capture-text.py; every run must end exit 0 or 2 with one REFUSED line."""
import importlib.util, json, os, pathlib, random, signal, struct, subprocess, sys
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
_s = importlib.util.spec_from_file_location("ct", LANE / "tools/capture-text.py")
ct = importlib.util.module_from_spec(_s); _s.loader.exec_module(ct)
S = pathlib.Path(sys.argv[1]); SEEDS = [pathlib.Path(x) for x in sys.argv[2:]]
rng = random.Random(54); EOC = 0xFFFFFFFE; TIME = "/home/vgpnk/.local/bin/time"
def chain(c, sid):
    o = []
    while sid <= EOC and sid < len(c.fat) and sid not in o: o.append(sid); sid = c.fat[sid]
    return o
def off(c, e, lo):
    "file offset of stream-relative byte lo of directory entry e"
    start, size = e[2], e[3]
    if size >= c.cutoff:
        ch = chain(c, start); return (ch[lo // c.ss] + 1) * c.ss + lo % c.ss
    ms = []; s = start
    while s <= EOC and s < len(c.minifat) and s not in ms: ms.append(s); s = c.minifat[s]
    mo = ms[lo // 64] * 64 + lo % 64; rc = chain(c, c.entries[0][2])
    return (rc[mo // c.ss] + 1) * c.ss + mo % c.ss
def load(path):
    d = path.read_bytes(); c = ct.Cfb(d); ss = c.ss; per = ss // 4
    nfat = struct.unpack_from("<I", d, 0x2C)[0]; fatsec = [x for x in struct.unpack_from("<109I", d, 0x4C)[:nfat] if x <= EOC]
    ent = lambda n: [x for x in c.entries if x and x[1] == 2 and x[0] == n][0]
    wd = c.stream("WordDocument"); tbl = "1Table" if struct.unpack_from("<H", wd, 0x0A)[0] & 0x200 else "0Table"
    p = 32; p += 2 + struct.unpack_from("<H", wd, p)[0] * 2; p += 2 + struct.unpack_from("<H", wd, p)[0] * 4; p += 2
    fc, lcb = struct.unpack_from("<II", wd, p + 33 * 8); clx = c.stream(tbl)[fc:fc + lcb]; i = 0
    while i < len(clx) and clx[i] == 0x01: i += 3 + struct.unpack_from("<h", clx, i + 1)[0]
    n = (struct.unpack_from("<I", clx, i + 1)[0] - 4) // 12
    k = [j for j, e in enumerate(c.entries) if e and e[1] == 2 and e[0] == "WordDocument"][0]; dch = chain(c, c.dir0)
    return dict(d=d, ss=ss, per=per, fatsec=fatsec, clx=clx, n=n, dch=dch, wdk=k, wdc=chain(c, c.entries[k][2]),
                fibbase=off(c, c.entries[k], 0), clxbase=off(c, ent(tbl), fc), pcd=i + 5 + 4 * (n + 1) + 2,
                lcb_off=off(c, c.entries[k], p + 33 * 8 + 4), dent=lambda j: (dch[(128 * j) // ss] + 1) * ss + (128 * j) % ss,
                fatent=lambda i: (fatsec[i // per] + 1) * ss + (i % per) * 4)
def make(c, kind):
    b = bytearray(c["d"]); r = {"kind": kind}
    if kind == "hdr": o = rng.randrange(512)
    elif kind == "fat": o = c["fatent"](rng.randrange(len(c["fatsec"]) * c["per"]))
    elif kind == "dir": o = (c["dch"][0] + 1) * c["ss"] + rng.randrange(c["ss"])
    elif kind == "fib": o = c["fibbase"] + rng.randrange(1024)
    elif kind == "clx": o = c["clxbase"] + rng.randrange(len(c["clx"]))
    elif kind == "trunc": n = rng.randrange(1, len(b)); r["cut"] = n; return bytes(b[:n]), r
    elif kind == "fatloop": x = c["wdc"][0]; o = c["fatent"](x); b[o:o + 4] = x.to_bytes(4, "little")
    elif kind == "dirsize": o = c["dent"](c["wdk"]) + 120; b[o:o + 8] = (0xFFFFFFFF).to_bytes(4, "little") + b"\0" * 4
    elif kind == "pcdoob": o = c["clxbase"] + c["pcd"]; b[o:o + 4] = (0x7FFFFFF0).to_bytes(4, "little")
    elif kind == "lcbclx": o = c["lcb_off"]; b[o:o + 4] = (0xFFFFFFFF).to_bytes(4, "little")
    else: o = c["clxbase"]; b[o:o + 3] = b"\x01" + rng.choice([-32768, -300, -5]).to_bytes(2, "little", signed=True)
    if kind not in ("fatloop", "dirsize", "pcdoob", "lcbclx", "clxprc"): b[o] ^= 1 << rng.randrange(8)
    r["off"] = o; return bytes(b), r
def run(data):
    m = S / "mut.bin"; m.write_bytes(data); t = S / "time.txt"
    p = subprocess.Popen([TIME, "-v", "-o", str(t), sys.executable, os.environ.get("CTOOL", str(LANE / "tools/capture-text.py")), str(m)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    try: o, e = p.communicate(timeout=10); rc = p.returncode
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(p.pid), signal.SIGKILL); o, e = p.communicate(); rc = "TIMEOUT"
    r = [int(l.split(":")[1]) for l in t.read_text().splitlines() if "Maximum resident set size" in l]
    return rc, o, e, (r[0] if r else 0)
KINDS = ["hdr", "fat", "dir", "fib", "clx", "trunc", "fatloop", "dirsize", "pcdoob", "lcbclx", "clxprc"]
CTX = {p.name: load(p) for p in SEEDS}
print("SEEDS", {k: (len(v["d"]), v["n"], v["clxbase"], v["fibbase"]) for k, v in CTX.items()})
LOG = []
for i in range(600):
    p = SEEDS[i % len(SEEDS)]; kind = KINDS[(i // len(SEEDS)) % len(KINDS)]
    data, rec = make(CTX[p.name], kind); rec.update(seed=p.name, n=i)
    rc, o, e, rss = run(data)
    err = e.decode("utf-8", "replace"); ref = [l for l in err.splitlines() if l.startswith("REFUSED ")]
    ok = rc == 2 and len(ref) == 1 and len(err.splitlines()) == 1 and "Traceback" not in err
    oc = "EXIT0" if rc == 0 else ("REFUSED:" + ref[0].split()[1].rstrip(":") if ok else "FAIL")
    LOG.append(dict(n=i, seed=rec["seed"], kind=kind, rc=rc, outcome=oc, rss_kb=rss, stderr=err.strip()[:400],
                     recipe={k: v for k, v in rec.items() if k not in ("seed", "n")}))
    if oc == "FAIL":
        (S / "fails").mkdir(exist_ok=True); (S / "fails" / f"m{i:04d}_{kind}.doc").write_bytes(data)
(S / "log.json").write_text(json.dumps(LOG, indent=1))
from collections import Counter
print("OUTCOMES", dict(Counter(x["outcome"] for x in LOG)), "MAXRSS_kb", max(x["rss_kb"] for x in LOG))
print("FAILS", [(x["n"], x["kind"], x["rc"], x["stderr"][:120]) for x in LOG if x["outcome"] == "FAIL"])
```

Seeds: four LibreOffice `.doc` made with a private profile (`soffice
-env:UserInstallation=file://$S/prof --headless --convert-to "doc:MS Word 97"`) — seed0 11264 B
`b1a5ed28…97fc75`, seed1 12288 B `9127bb9b…ffd3ac`, seed2 10752 B `9b26cfd2…f44850`, seed3 11264 B
`ad702f16…fa09d` — plus the five pinned captures (four distinct docs; `54fe0734…`/`74ced3e9…` are
byte twins, `d341c133…7646d5`), all matching the counter's `REAL` table. Eleven classes × 9 seeds ×
6 rounds = 600 mutants: `hdr`/`fat`/`dir`/`fib`/`clx` (bit flip in the 512-byte header, a FAT
sector, a directory sector, the FIB, the Clx), `trunc` (cut at a random point), `fatloop` (FAT entry
rewritten to point at its own sector — a real self-loop), `dirsize` (entry size 2^32−1), `pcdoob`
(piece `fc` beyond the stream), `lcbclx` (lcbClx = 0xFFFFFFFF), `clxprc` (Clx `Prc` with a negative
`cbGrpprl`).

## 2. Result on the frozen candidate `8a7d0f1` — 37 FAILs

```
$ CTOOL=…/frozen/capture-text.py python3 fuzz.py $S <9 seeds>
OUTCOMES {'EXIT0': 222, 'REFUSED:ole-malformed': 339, 'REFUSED:ole-not-word': 2, 'FAIL': 37}  MAXRSS_kb 20476
FAILS [(90, 'clxprc', 1, 'Traceback (most recent call last):…'), (94, …), (96, …), (97, …), (98, …), (189, …)]
```

All 37 are one defect class (`clxprc`), on all nine seeds (seed0 5, seed1 5, seed2 2, seed3 1,
54fe0734 6, 6dc68fd6 4, b539a802 4, bdff491a 4, 74ced3e9 6): exit 1, stdout empty, stderr a
traceback ending `IndexError: index out of range`. **Root cause:**

```
271:    while i < len(clx) and clx[i] == 0x01:
272-273:      (bounds check on i only)
274:        i += 3 + struct.unpack_from("<h", clx, i + 1)[0]
```

`cbGrpprl` is a **signed** 16-bit `<h`, so a negative value sends `i` *backwards* (`i += 3 + (-300)`
⇒ `-297`); `i < len(clx)` still passes and `clx[-297]` raises `IndexError` — uncaught, not a
`Refused`. Rebuild any failing mutant from its logged recipe:

```
$ python3 -c "import pathlib; b=bytearray(pathlib.Path('seeds/seed0.doc').read_bytes()); b[3344:3347]=b'\x01'+(-300).to_bytes(2,'little',signed=True); pathlib.Path('m.doc').write_bytes(bytes(b))"
$ python3 capture-text-8a7d0f1.py m.doc ; echo "rc=$?"
IndexError: index out of range   (… line 271, doc_text_form) ; rc=1
```

**The crash is one byte from a clean document.** `prc_valid.doc` — a seed with a *syntactically
valid* `Prc` (`cbGrpprl = 4`) prepended to the Pcdt, `lcbClx` grown 21 → 28 — reads cleanly; flipping
**one bit** of `cbGrpprl` kills the frozen candidate: `prc_valid.doc` → frozen rc=0 out=579 err='' ·
`prc_onebit.doc` (clxbase+2 ^= 0x80, cbGrpprl=-32764) → frozen rc=1 IndexError traceback, worktree
rc=2 `REFUSED ole-malformed: Prc GrpPrl outside the Clx`.

**The frozen counter does not see it** — its MALFORMED leg only cuts a document short or shifts its
sector size, never the Clx `Prc` length:

```
$ python3 corpus/evidence/round54/c1-count.py --tool …/frozen/capture-text.py --seed 54 --work $S/c1work
sha256=fd0ed3f58565b781ab8eedaad5d229976e150bdd8e391a2b0cacd0a0825fcd89 seed=54 per-leg=3
GEN=PASS 3 · NONWORD=PASS 3 · ENCRYPTED=PASS 3 · MALFORMED=PASS 3 · REAL=PASS 5 · REGRESS=PASS r52 ['LEGS=9/9'] ['SUPPLEMENT_LEGS=4/4']
LEGS=6/6   C1=PASS   (EXIT=0)
```

**A report, not a patch.** I do not propose changing the C1 predicate, counter, control or target:
the claim requires refusals with "no `Traceback`", but the counter measures only the legs it names,
so the finding is *against the claim's robustness envelope*, not a scored leg — **C1 can still be
scored PASS** while the landed artefact crashes on a one-bit-corrupted file.

## 3. Same 600 mutants against the lane **worktree** tool — 0 FAILs

The worktree `tools/capture-text.py` carries an **uncommitted** hunk (sha256
`e7e381b675353e85578f04d0fba6948d4b6d532b174c7d3baff5c8fcfe65009d`, HEAD still `9caf8fc`) that is
this fix at lines 271–277: read `cb_grpprl` as `<h`, refuse (`ole-malformed: Prc GrpPrl outside the
Clx`) when `cb_grpprl < 0` or `i + 3 + cb_grpprl > len(clx)`. The same hunk is in siblings
`R54SimplifyOle.md:98` and `R54ReviewOleTool.md:82` — that seat found it first; mine is independent
confirmation by fuzz, not discovery:

```
OUTCOMES {'EXIT0': 222, 'REFUSED:ole-malformed': 376, 'REFUSED:ole-not-word': 2}  MAXRSS_kb 21432
FAILS []
```

## 4. Offsets checked; three more sweeps

Each mutation offset is computed from the seed's own CFB layout, then verified against the file
bytes: for all nine seeds the range at the computed `clxbase` is byte-identical to the `Clx` the
tool reads, and `fibbase` holds the FIB magic `EC A5` (`clx_at_offset_ok True fib_wIdent_ok True`;
clxlen 21 for the four seeds, 189/225/45/21/189 for the captures).

| sweep (worktree tool) | what it mutates | runs | FAILs | max RSS |
|---|---|---|---|---|
| `deep.py` — FIB + Clx | every FIB field (`wIdent`, `nFib`, `flags`, `csw`, `cslw`, `cb`, `ccpText`, `fcClx`, `lcbClx`) × 5 values; each of the first 400 Clx bytes × 3 values, all 9 seeds | **2412** | **0** | — |
| `probe.py` — structure | destroyed OLE magic; size 2^32−1 on *every* directory entry and on Root; `fEncrypted`; `fObfuscated`; `nFib < 0xC1`; bad `wIdent`; `ccpText = 0x7FFFFFFF` | 55 | **0** | 21244 kB |
| `broad.py` — volume | 2–6 flips anywhere; truncate+flip; 2–12 flips in the first 1024 B; 1–20 flips in a random 512-B window; 64–4096 B zeroed, all 9 seeds | **1500** | **0** | 21500 kB |

Tails: `deep.py` → `TOTAL_RUNS 2412 BAD 0`; `broad.py` → `RUNS 1500 BAD 0 MAXRSS_kb 21500`. (The same
1500 broad mutants on the **frozen** candidate also give `RUNS 1500 BAD 0`: random mutation does not
reach the `Prc` length field, which is why the defect needs a targeted mutant.) Every refusal was one
stderr line, exit 2, empty stdout (`ole-malformed`: `stream 'WordDocument' of 4294967295 bytes`,
`compressed piece outside WordDocument`, `Clx outside the table stream`, `Prc GrpPrl outside the
Clx`, `FAT sector outside the file`, `sector chain at 9`/`at 0`, `piece table CPs decrease`, `PlcPcd
size`; `ole-encrypted`; `ole-not-word`; `neither a zip package nor an OLE compound file`).

## 5. Resource ceiling, tooling, what this changes

Peak RSS over the 600-mutant runs: **21 676 kB (21.2 MiB)** — 2.1 % of the 1 GB ceiling, 21× under the
tool's own `MAX_PART` (256 MiB). Worst mutant #474 (`pcdoob` on `b539a802…`, byte 782887), rebuilt
and re-run alone:

```
$ /home/vgpnk/.local/bin/time -v python3 …/capture-text.py rebuild_474.doc
REFUSED ole-malformed: compressed piece outside WordDocument   Maximum resident set size (kbytes): 19268   Exit status: 2
```

No run exceeded 10 s (slowest wall clock 0.04 s); no `soffice.bin` left behind (`pgrep -u $USER -f
"UserInstallation=file://$S"` → no match); scratch removed. No package installed, upgraded or written:
the host has no `/usr/bin/time`, so GNU `time` 1.9 already at `/home/vgpnk/.local/bin/time` was **read
and executed only, never written**; LibreOffice 26.8.1.1 and Python 3.14.8 pre-existing; `pacman`
untouched.

- The C1 counter, predicate, target and control are **unchanged**; it ran read-only (`--tool` at a
  scratch copy) and prints `LEGS=6/6 C1=PASS` on the frozen candidate — no scored leg is falsified.
- The frozen **artefact** `8a7d0f1` nevertheless ends 37 of 600 mutated OLE documents with a Python
  traceback and exit 1, one bit from a document that reads cleanly. Whether the L1 lands the
  already-present worktree hunk is the L1's call; I do not touch production files.
- For the L1's Gate: the C1 robustness row should note the *committed* candidate's OLE path is not
  traceback-free under a `Prc`-length mutation, and that the worktree hunk closes it.

**VERDICT: fuzzed the frozen C1 candidate's OLE path with 600 structural mutants (plus 2412 FIB/Clx
and 1500 broad runs); the committed candidate `8a7d0f1` crashes with an `IndexError` traceback on
37/600 mutants (a negative `Prc cbGrpprl`, one bit from a clean document) while the lane worktree
tool with the same hunk is 0 FAILs — and the frozen C1 counter still reports `LEGS=6/6 C1=PASS`
over the defect.**
