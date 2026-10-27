#!/usr/bin/env python3
"""Build the R56-C1 JUNK battery into OUTDIR (outside the lane): nine tools that skip the
battery work — four exit 1 with a refusal line for every id, two exit 0 writing nothing, two
copy the landed builder unchanged, and one FLIP tool that keeps a call counter in its own
directory and corrupts the first `capture_sha256` cell on odd calls only (an alternating forge:
the doubled random-order runs must refuse it most of the time). A junk battery must not reach
KILLED=9/9.
Usage: python3 corpus/evidence/round56/controls/build-c1-junk.py OUTDIR"""
import pathlib
import sys

LANE = pathlib.Path(__file__).resolve().parents[4]
out = pathlib.Path(sys.argv[1]).resolve()
if out == LANE or LANE in out.parents:
    sys.exit("OUTDIR must lie outside the lane")
out.mkdir(parents=True, exist_ok=True)
refuse = ('import sys\nfor l in open(sys.argv[sys.argv.index("--quotes") + 1], encoding="utf-8").read().splitlines()[1:]:\n'
          '    print("build-spans: refused " + l.split("\\t")[0] + ": junk", file=sys.stderr)\nsys.exit(1)\n')
for i in range(4):
    (out / f"junk-refuse{i}.py").write_text(refuse + f"# {i}\n")
for i in range(2):
    (out / f"junk-zero{i}.py").write_text(f"import sys\nsys.exit(0)\n# {i}\n")
b = (LANE / "tools" / "build-spans.py").read_text()
for i in range(2):
    (out / f"junk-copy{i}.py").write_text(b.replace("TOOLS = pathlib.Path(__file__).resolve().parent",
                                                    f"TOOLS = pathlib.Path({str(LANE / 'tools')!r})") + f"# {i}\n")
flip = ("import os, pathlib, runpy, sys\n"
        f"B = {str(LANE / 'tools' / 'build-spans.py')!r}\n"
        "st = pathlib.Path(__file__).resolve().parent / 'flip.state'\n"
        "n = int(st.read_text()) + 1 if st.exists() else 1\n"
        "st.write_text(str(n))\n"
        "out = sys.argv[sys.argv.index('--out') + 1]\n"
        "sys.argv[0] = B\n"
        "try:\n"
        "    runpy.run_path(B, run_name='__main__')\n"
        "except SystemExit as e:\n"
        "    if e.code not in (0, None):\n"
        "        raise\n"
        "m = pathlib.Path(out) / 'spans.tsv'\n"
        "if n % 2 and m.is_file():\n"
        "    ls = m.read_text(encoding='utf-8').split('\\n')\n"
        "    c = ls[1].split('\\t'); c[2] = '0' * 64; ls[1] = '\\t'.join(c)\n"
        "    m.write_text('\\n'.join(ls), encoding='utf-8')\n")
(out / "junk-flip0.py").write_text(flip)
print(" ".join(sorted(p.name for p in out.glob("*.py"))))
