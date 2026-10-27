#!/usr/bin/env python3
"""R61 no-harm check on real data — the span builder against three committed span sets.

For each of the lane's committed span sets (round 55, round 56, round 57/c3: `quotes.tsv`,
`spans.tsv`, `spans/`) and the lane-owned capture store `corpus/captures/`, builder B
(default `tools/build-spans.py`) is run (a) with `--check` against the committed directory and
(b) as a build into a fresh empty scratch directory; the leg holds when (a) exits 0 and (b)
exits 0 with `spans.tsv` and every span file byte-equal to the committed ones and no extra file.
Prints `REAL_REBUILD=k/3`; exit 0 iff 3/3, 1 otherwise, 2 usage/env.
Usage: python3 corpus/evidence/round61/regress.py [--builder PATH] --work DIR
"""
import argparse, filecmp, pathlib, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[2]
SETS = ["corpus/evidence/round55", "corpus/evidence/round56", "corpus/evidence/round57/c3"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--builder", default=str(LANE / "tools" / "build-spans.py"))
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    work = pathlib.Path(a.work)
    if work.exists() and any(work.iterdir()):
        print("regress: --work must be absent or empty", file=sys.stderr)
        return 2
    work.mkdir(parents=True, exist_ok=True)
    tools = work / "tools"
    tools.mkdir()
    shutil.copy(a.builder, tools / "build-spans.py")
    shutil.copy(LANE / "tools" / "capture-text.py", tools / "capture-text.py")
    ok = 0
    for rel in SETS:
        d = LANE / rel
        out = work / rel.replace("/", "_")
        base = [sys.executable, str(tools / "build-spans.py"), "--quotes", str(d / "quotes.tsv"), "--cache", str(LANE / "corpus" / "captures")]
        chk = subprocess.run(base + ["--out", str(d), "--check"], capture_output=True, text=True)
        bld = subprocess.run(base + ["--out", str(out)], capture_output=True, text=True)
        same = bld.returncode == 0 and (out / "spans.tsv").read_bytes() == (d / "spans.tsv").read_bytes()
        if same:
            want = sorted(p.name for p in (d / "spans").iterdir())
            got = sorted(p.name for p in (out / "spans").iterdir())
            same = want == got and all((d / "spans" / n).read_bytes() == (out / "spans" / n).read_bytes() for n in want)
            same = same and sorted(p.name for p in out.iterdir()) == ["spans", "spans.tsv"]
        leg = chk.returncode == 0 and same
        ok += leg
        print(f"{rel} check_rc={chk.returncode} build_rc={bld.returncode} identical={same} {'pass' if leg else 'fail'}")
    shutil.rmtree(work, ignore_errors=True)
    print(f"REAL_REBUILD={ok}/{len(SETS)}")
    return 0 if ok == len(SETS) else 1


if __name__ == "__main__":
    sys.exit(main())
