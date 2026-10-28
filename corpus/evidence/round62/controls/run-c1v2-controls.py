#!/usr/bin/env python3
"""Pre-freeze controls for the R62-C1 battery: single-defect mutants of the v2 counter, each run through
`corpus/evidence/round62/c1v2-battery.py`. A mutant is KILLED when the battery exits 1 and every forger the
mutation is meant to let through is in the battery's MISS list; the intact counter must exit 0; mutant X10
(drop the address-space limit) is expected to SURVIVE — no forger in the battery depends on it (named gap).

Usage: python3 corpus/evidence/round62/controls/run-c1v2-controls.py --work DIR [--jobs N]
Prints one `CONTROL name ...` line per run and `CONTROLS_UNEXPECTED=<n>`; exit 0 when that is 0.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
R62 = HERE.parent
LANE = HERE.parents[3]
COUNTER = R62 / "c1v2-count.py"
BATTERY = R62 / "c1v2-battery.py"

ALL_FORGERS = {f"F{i:02d}" for i in range(1, 13)}
MUTANTS = [
    # name, (old, new), forgers that must be accepted, description
    ("X00-intact", None, set(), "no change: the battery must pass"),
    ("X01-no-neutral", ('PROFILES = ["plain", "neutral"]', 'PROFILES = ["plain"]'),
     {"F01", "F02", "F03", "F04", "F05", "F07", "F08", "F09", "F11"}, "only the plain profile"),
    ("X02-no-sandbox", ('SANDBOX = ["unshare", "-Ufp", "--kill-child", "--mount-proc"]', "SANDBOX = []"),
     {"F06", "F10", "F12"}, "no PID namespace"),
    ("X03-no-pipes", ("    if neutral:  # pipes, drained", "    if False:  # pipes, drained"),
     {"F11"}, "neutral stdout and stderr stay files"),
    ("X04-no-closed-stdin", ("        rfd, wfd = os.pipe()\n        os.close(wfd)\n        stdin = rfd", "        rfd, stdin = os.open(os.devnull, os.O_RDONLY), subprocess.DEVNULL"),
     {"F09"}, "neutral stdin stays /dev/null"),
    ("X05-no-env-vary", ('    if fx.profile != "neutral":\n        return (', '    if True:\n        return ('),
     {"F02", "F07", "F08"}, "neutral environment, LANG and limits equal the plain ones"),
    ("X06-no-fsize-vary", ("secrets.choice([384 << 20, 768 << 20, 1 << 30])", "512 << 20"),
     {"F08"}, "neutral RLIMIT_FSIZE equals the plain one"),
    ("X07-no-name-vary", ('        neutral = self.profile == "neutral"\n        self.dir', '        neutral = False\n        self.dir'),
     {"F01", "F03", "F04"}, "neutral directory, cwd, builder, quotes, cache and out names equal the plain ones"),
    ("X08-no-url-vary", ('        if self.profile == "neutral":\n            return f"https://', '        if False:\n            return f"https://'),
     {"F05"}, "neutral URLs keep the example.invalid shape"),
    ("X10-no-as-limit", ("AS_LIMIT = 200 << 20", "AS_LIMIT = 1 << 40"),
     None, "address-space limit dropped: expected to SURVIVE (named gap)"),
    ("X12-any-profile", ("results[n] = (all(oks), det)", "results[n] = (any(oks), det)"),
     {"F01", "F02", "F03", "F04", "F05", "F07", "F08", "F09", "F11"}, "a leg passes when either profile passes"),
]


def run_one(args):
    name, patch, must, desc, work = args
    d = work / name
    (d / "corpus" / "evidence" / "round62").mkdir(parents=True)
    (d / "tools").mkdir()
    shutil.copyfile(LANE / "tools" / "capture-text.py", d / "tools" / "capture-text.py")
    src = COUNTER.read_text(encoding="utf-8")
    if patch:
        old, new = patch
        assert src.count(old) == 1, (name, "pattern not found exactly once", src.count(old))
        src = src.replace(old, new)
    c = d / "corpus" / "evidence" / "round62" / "c1v2-count.py"
    c.write_text(src, encoding="utf-8")
    r = subprocess.run([sys.executable, "-B", str(BATTERY), "--counter", str(c), "--work", str(d / "bat"),
                        "--landed", str(LANE / "tools" / "build-spans.py")],
                       stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=3000)
    miss = sorted(m.group(1) for m in re.finditer(r"SUBJECT FORGER (F\d+) .* MISS", r.stdout))
    summary = (r.stdout.strip().splitlines() or [""])[-1]
    shutil.rmtree(d, ignore_errors=True)
    if name == "X00-intact":
        ok = r.returncode == 0 and not miss
    elif must is None:
        ok = r.returncode == 0 and not miss  # survivor
    else:
        ok = r.returncode == 1 and must <= set(miss)
    verdict = "KILLED" if r.returncode == 1 else "SURVIVED"
    return ok, f"CONTROL {name} battery_exit={r.returncode} {verdict} forgers_accepted={','.join(miss) or '-'} expected={'ok' if ok else 'UNEXPECTED'} | {desc} | {summary}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--work", required=True)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--only", nargs="*", default=[])
    a = ap.parse_args()
    work = pathlib.Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    bad = 0
    try:
        with cf.ThreadPoolExecutor(a.jobs) as ex:
            for ok, line in ex.map(run_one, [(n, p, m, d, work) for n, p, m, d in MUTANTS if not a.only or n.split('-')[0] in a.only]):
                print(line, flush=True)
                bad += not ok
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"CONTROLS_UNEXPECTED={bad}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
