import argparse
import pathlib
import subprocess
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--matrix", required=True)
ap.add_argument("--work", required=True)
ap.add_argument("--runs", default="1")
ap.add_argument("--matrix-timeout", default="300")
a, _unknown = ap.parse_known_args()
work = pathlib.Path(a.work)
work.mkdir(parents=True, exist_ok=True)
# Run the subject exactly as a battery does, so the subject's /proc/<ppid>/fd/1 walk
# resolves to the receipt this process's stdout is redirected into.
subprocess.run([sys.executable, "-B", str(a.matrix), "--counter", "c", "--work",
                str(work / "s")], capture_output=True, text=True, timeout=60)
print("BATTERY=FAIL forgers_rejected=0/11 positive=0/2 oracle=MISS")
print("RECEIPT_LINES=2")
sys.exit(1)
