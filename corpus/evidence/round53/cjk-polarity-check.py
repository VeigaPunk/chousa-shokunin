#!/usr/bin/env python3
"""cjk-polarity-check — round-52 closure routed defect 5 (the inference-ground CJK
polarity leg was inert; W1 `R53ExecCjkPolarity`). Runs `tools/inference-ground.py`
on the six fixtures in corpus/fixtures/inference-ground-cjk/: four reversals
(不 / 没有 / 未要求 on an affirmed span, and an affirmed bullet on a negated span)
must exit 1 with an `INF_POLARITY_FLIP` finding; the positive control and the
far-negator precision case must exit 0.

Usage: python3 corpus/evidence/round53/cjk-polarity-check.py [--tool PATH]
Prints one line per fixture and `CJK_POLARITY=n/6`; exit 0 when 6/6, else 1.
"""
import argparse
import pathlib
import subprocess
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
F = LANE / "corpus" / "fixtures" / "inference-ground-cjk"
JUNK = ("cjk-negation-buyaoqiu.md", "cjk-negation-meiyou.md", "cjk-negation-weiyaoqiu.md", "cjk-span-negated.md")
KEEP = ("cjk-positive-control.md", "cjk-precision-far-negator.md")
ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
ap.add_argument("--tool", default=str(LANE / "tools" / "inference-ground.py"))
a = ap.parse_args()
ok = 0
for name in JUNK + KEEP:
    r = subprocess.run([sys.executable, a.tool, "--entry", str(F / name), "--spans", str(F / "spans.tsv"),
                        "--counts", "/dev/null", "--registry", str(F / "SOURCES.md"), "--root", str(F)],
                       capture_output=True, text=True, cwd=F)
    want_junk = name in JUNK
    good = (r.returncode == 1 and "INF_POLARITY_FLIP" in r.stdout + r.stderr) if want_junk else r.returncode == 0
    ok += good
    print(f"{name} rc={r.returncode} want={'flip' if want_junk else 'pass'} {'ok' if good else 'MISS'}")
print(f"CJK_POLARITY={ok}/{len(JUNK) + len(KEEP)}")
sys.exit(0 if ok == len(JUNK) + len(KEEP) else 1)
