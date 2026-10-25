#!/usr/bin/env python3
"""Control tool for R47-C1: the round-46 tool, plus a refusal of every Inference
bullet that carries any negator word — a polarity check that never compares
the bullet with its span."""
import pathlib, re, runpy, subprocess, sys
base = pathlib.Path(__file__).with_name("base-tool-r46.py")
p = subprocess.run([sys.executable, str(base)] + sys.argv[1:], capture_output=True, text=True)
args = sys.argv[1:]
entry = pathlib.Path(args[args.index("--entry") + 1]).read_text(encoding="utf-8")
inf = entry.split("#### Inference", 1)[1] if "#### Inference" in entry else ""
neg = re.search(r"\b(no|not|never|none|without|cannot)\b", inf, re.I)
sys.stdout.write(p.stdout)
if neg:
    print("FINDING INF_POLARITY_FLIP bullet=1 token='negator present'")
    sys.exit(1)
sys.exit(p.returncode)
