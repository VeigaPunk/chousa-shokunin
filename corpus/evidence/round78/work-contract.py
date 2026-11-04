#!/usr/bin/env python3
"""Round-78 `--work` contract control (QUALITY 142 -> 144).

Three questions, each a separate run of the battery under test:

  A  a `--work` directory that already holds a caller's file — does the file survive?
  B  a `--work` directory the caller cannot write — does the battery exit 2 with a
     diagnostic instead of a traceback and exit 1?
  C  a `--work` path that is a regular file — exit 2?

The matrix used is a fast forger (`corpus/evidence/round78/forgers/a1-hash-identity.py`) with
`--runs 1`, so the control measures the setup/teardown paths only; the subject set is not
scored here and nothing in this receipt is the round's predicate.

Usage: python3 corpus/evidence/round78/work-contract.py --battery PATH --work DIR
Exit: 0 WORK_CONTRACT=PASS · 1 WORK_CONTRACT=FAIL · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
MATRIX = HERE / "forgers" / "a1-hash-identity.py"


def run(battery: pathlib.Path, work: pathlib.Path, timeout: int) -> tuple[int, str]:
    p = subprocess.run([sys.executable, "-B", str(battery), "--matrix", str(MATRIX),
                        "--work", str(work), "--runs", "1", "--matrix-timeout", "60"],
                       stdin=subprocess.DEVNULL, capture_output=True, text=True,
                       timeout=timeout)
    return p.returncode, p.stderr


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--battery", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--timeout", type=int, default=600)
    a = ap.parse_args()
    battery = pathlib.Path(a.battery).resolve()
    work = pathlib.Path(a.work).resolve()
    if not battery.is_file():
        print(f"work-contract: missing battery {battery}", file=sys.stderr)
        return 2
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    print("BATTERY_PATH=" + str(battery))
    print("BATTERY_SHA256=" + hashlib.sha256(battery.read_bytes()).hexdigest())

    # A — a caller's file inside --work must survive.
    a_dir = work / "a"
    a_dir.mkdir()
    sentinel = a_dir / "caller-file.txt"
    sentinel.write_text("the caller put this here\n")
    rc_a, err_a = run(battery, a_dir, a.timeout)
    survived = sentinel.is_file() and sentinel.read_text() == "the caller put this here\n"
    print(f"CASE A rc={rc_a} sentinel_survived={'yes' if survived else 'no'} "
          f"dir_exists={'yes' if a_dir.is_dir() else 'no'}")

    # B — an unwritable --work must be could-not-evaluate (2), never a traceback at 1.
    b_dir = work / "b"
    b_dir.mkdir()
    os.chmod(b_dir, 0o555)
    rc_b, err_b = run(battery, b_dir / "nested", a.timeout)
    traceback_b = "Traceback" in err_b
    print(f"CASE B rc={rc_b} traceback={'yes' if traceback_b else 'no'} "
          f"stderr_first={err_b.strip().splitlines()[0][:120] if err_b.strip() else '<empty>'}")
    os.chmod(b_dir, 0o755)

    # C — a --work that is a regular file must be could-not-evaluate (2).
    c_file = work / "c"
    c_file.write_text("not a directory\n")
    rc_c, err_c = run(battery, c_file, a.timeout)
    traceback_c = "Traceback" in err_c
    print(f"CASE C rc={rc_c} traceback={'yes' if traceback_c else 'no'} "
          f"stderr_first={err_c.strip().splitlines()[0][:120] if err_c.strip() else '<empty>'}")

    ok = survived and rc_b == 2 and not traceback_b and rc_c == 2 and not traceback_c
    print(f"WORK_CONTRACT={'PASS' if ok else 'FAIL'} survived={'yes' if survived else 'no'} "
          f"unwritable_exit={rc_b} file_exit={rc_c}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
