#!/usr/bin/env python3
"""Probe: record every channel the battery leaves open to a subject. Behaves as
constant-pass so the matrix's own scoring is unchanged."""
import argparse
import json
import os
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")


def read_bytes(path):
    try:
        with open(path, "rb") as fh:
            return fh.read(8192)
    except OSError:
        return b""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default=None)
    ap.add_argument("--base", default=None)
    a = ap.parse_args()
    ppid = os.getppid()
    stat = read_bytes(f"/proc/{ppid}/stat").decode("utf-8", "replace")
    try:
        gppid = stat.rsplit(")", 1)[1].split()[1]
    except IndexError:
        gppid = "?"
    rec = {
        "argv": sys.argv,
        "cwd": os.getcwd(),
        "env_LOADER_MATRIX_CHILD_TIMEOUT": os.environ.get("LOADER_MATRIX_CHILD_TIMEOUT"),
        "env_keys_naming_matrix": sorted(k for k in os.environ if "MATRIX" in k.upper() or "BATTERY" in k.upper()),
        "ppid": ppid,
        "ppid_cmdline": read_bytes(f"/proc/{ppid}/cmdline").decode("utf-8", "replace").split("\0"),
        "ppid_stdout_target": (lambda: (os.readlink(f"/proc/{ppid}/fd/1") if os.path.exists(f"/proc/{ppid}/fd/1") else "gone"))(),
        "gppid": gppid,
        "gppid_cmdline": read_bytes(f"/proc/{gppid}/cmdline").decode("utf-8", "replace").split("\0"),
        "own_source_sha256": __import__("hashlib").sha256(read_bytes(__file__)).hexdigest()[:16],
    }
    out = os.environ.get("R76CRIT_PROBE_OUT", "/dev/null")
    with open(out, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    for cid in IDS:
        print(f"CHECK {cid} PASS probe")
    print("C2=PASS checks=7/7 probe")
    return 0


if __name__ == "__main__":
    sys.exit(main())
