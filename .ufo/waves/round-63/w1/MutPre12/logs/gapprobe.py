#!/usr/bin/env python3
"""Scratch-only gap probe for MutPre12 survivors. Reads the lane; writes only under its own scratch dir."""
import os, pathlib, re, shutil, subprocess, sys, stat

S = pathlib.Path("/fast/scratch/hyaku/chousa-r63/MutPre12")
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
FLEET = pathlib.Path("/home/vgpnk/Projects/shokunin")
REF = LANE / "corpus/evidence/round63/controls/pos-ref-preflight.py"
MUT = S / "mut"
MUT2 = S / "mut2"

# fixed N10 mutant, written to scratch
src = REF.read_text()
old = "    miss = [f for f in files if f not in readme]\n"
new = "    miss = [f for f in files if f not in readme and pathlib.Path(f).stem not in readme]\n"
assert src.count(old) == 1
(MUT / "N10-fixed.py").write_text(src.replace(old, new, 1))


def fresh(tag):
    d = S / "probe" / tag
    if d.exists():
        shutil.rmtree(d)
    (d / "lane").mkdir(parents=True)
    shutil.copytree(LANE / "corpus", d / "lane" / "corpus", symlinks=True)
    for f in ("SHONEN.md", "SCORECARD.md"):
        shutil.copy2(LANE / f, d / "lane" / f)
    return d


def run(tool, root, env_extra=None, fleet=FLEET):
    w = S / "probe" / ("w-" + pathlib.Path(tool).stem + "-" + str(abs(hash(str(root))) % 10**6))
    if w.exists():
        shutil.rmtree(w)
    env = {"PATH": os.environ["PATH"], "LC_ALL": "C.UTF-8", "HOME": str(S), "TMPDIR": str(S)}
    if env_extra:
        env.update(env_extra)
    cmd = [sys.executable, "-B", str(tool), "--root", str(root), "--only", "G01,G02", "--work", str(w)]
    if fleet is not None:
        cmd += ["--fleet", str(fleet)]
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=S, timeout=300)
    lines = [l for l in p.stdout.splitlines() if l.startswith(("GATE G01", "GATE G02", "PREFLIGHT"))]
    return p.returncode, lines


def show(label, tools, root, **kw):
    print(f"--- {label}")
    for name, tool in tools:
        rc, lines = run(tool, root, **kw)
        print(f"  {name:10s} rc={rc} | " + " | ".join(lines))


def main():
    # gap N01 / N02: registry absent (battery never removes corpus/SOURCES.md)
    d = fresh("N01")
    (d / "lane/corpus/SOURCES.md").unlink()
    show("G1 remove corpus/SOURCES.md (N01 ENV, N02 check-dropped)",
         [("ref", REF), ("N01", MUT / "N01-g01-registry-absent-env.py"),
          ("N02", MUT / "N02-g01-registry-absent-check-dropped.py")], d / "lane")

    # gap N05: unreadable registry -> census exit 2 (battery never chmods)
    d = fresh("N05")
    os.chmod(d / "lane/corpus/SOURCES.md", 0)
    show("G2 chmod 000 corpus/SOURCES.md (N05 exit2 treated as pass)",
         [("ref", REF), ("N05", MUT / "N05-g01-census-exit-1-treated-pass.py")], d / "lane")

    # gap N11: README absent
    d = fresh("N11")
    (d / "lane/corpus/README.md").unlink()
    show("G3 remove corpus/README.md (N11 readme-absent pass)",
         [("ref", REF), ("N11", MUT / "N11-g02-readme-absent-is-pass.py")], d / "lane")

    # gap N09: case-only index mismatch (battery uses lowercase names only)
    d = fresh("N09")
    rd = d / "lane/corpus/README.md"
    t = rd.read_text()
    nm = "hardening-r10.md"
    assert nm in t
    rd.write_text(t.replace(nm, "HARDENING-R10.MD"))
    show("G4 README names one entry in upper case only (N09 case-insensitive)",
         [("ref", REF), ("N09", MUT / "N09-g02-case-insensitive-index.py")], d / "lane")

    # N10 fixed: stem-tolerant match, D05-like defect keeping the stem
    d = fresh("N10")
    rd = d / "lane/corpus/README.md"
    t = rd.read_text()
    rd.write_text(t.replace("hardening-r10.md", "hardening-r10.gone"))
    show("G5 README: name -> .gone, stem kept (N10 stem-tolerant)",
         [("ref", REF), ("N10fixed", MUT / "N10-fixed.py")], d / "lane")

    # gap N03: SHOKUNIN_ROOT precedence (battery env never sets SHOKUNIN_ROOT)
    d = fresh("N03")
    bad = S / "probe" / "no-fleet-here"
    bad.mkdir(parents=True, exist_ok=True)
    show("G6 env SHOKUNIN_ROOT=dir without scripts, --fleet valid (N03 root-beats-fleet)",
         [("ref", REF), ("N03", MUT / "N03-g01-shokunin-root-beats-fleet.py")], d / "lane",
         env_extra={"SHOKUNIN_ROOT": str(bad)})

    # gap N18: a broken census script in the lane's parent; --fleet names the good one
    d = fresh("N18")
    pp = d / "scripts"
    pp.mkdir()
    (pp / "sources-census.sh").write_text("#!/usr/bin/env bash\nexit 1\n")
    show("G7 broken scripts/ in lane parent, --fleet valid (N18 parent-first)",
         [("ref", REF), ("N18", MUT2 / "N18-g01-parent-scripts-beat-fleet.py")], d / "lane")

    # N21 check: is the CLEAN kill a timeout artefact? (census run with 1 s timeout)
    show("G8 unchanged lane (N21 census timeout=1)",
         [("ref", REF), ("N21", MUT2 / "N21-g01-census-run-from-root.py")], LANE)

    # cleanup scratch probes
    shutil.rmtree(S / "probe", ignore_errors=True)
    (MUT / "N10-fixed.py").unlink(missing_ok=True)


if __name__ == "__main__":
    try:
        main()
    finally:
        pass
