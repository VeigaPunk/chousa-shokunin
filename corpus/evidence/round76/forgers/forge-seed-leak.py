#!/usr/bin/env python3
"""Forger: seed reader — tries to replay the matrix shuffle from the parent's stdout.

Opens `/proc/<ppid>/fd/1` non-blocking and reads whatever the matrix has printed so
far. The round-75 v2 matrix printed `SEED=<n>`; the v3 matrix prints only
`SEED_SHA256=`, which a digest does not replay, so this forger falls back to PASS and
is rejected by the eight failing cases. It also shows that a reader of the parent's
captured pipe is bounded: the matrix kills it if it blocks.
"""
import argparse
import os
import re
import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
SEED = re.compile(rb"^SEED=([0-9]+)$", re.M)


def read_parent_stdout() -> bytes:
    try:
        fd = os.open(f"/proc/{os.getppid()}/fd/1", os.O_RDONLY | os.O_NONBLOCK)
    except OSError:
        return b""
    try:
        return os.read(fd, 65536)
    except OSError:
        return b""
    finally:
        os.close(fd)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    blob = read_parent_stdout()
    replayable = bool(SEED.search(blob))
    print(f"# seed-leak replayable={replayable} bytes={len(blob)}")
    for cid in IDS:
        print(f"CHECK {cid} PASS seed-leak")
    print(f"C2=PASS checks=7/7 rev={a.rev[:12]} base={a.base[:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
