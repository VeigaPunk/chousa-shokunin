#!/usr/bin/env python3
"""CHANNEL PROBE: detached grandchild — quantified stall of the child bound.

The v3 matrix's `run_child` does, on expiry:

    os.killpg(p.pid, signal.SIGKILL)
    out, _err = p.communicate()          # <-- NO timeout

`killpg` kills the child's PROCESS GROUP.  A grandchild that called setsid()
leaves that group, so it survives the kill -- and it still holds the write end
of the stdout/stderr pipes.  The second `communicate()` therefore waits for an
EOF that cannot arrive until the grandchild exits, so the matrix is stalled
for the grandchild's lifetime, long past LOADER_MATRIX_CHILD_TIMEOUT.

This probe's grandchild sleeps GRANDCHILD_SLEEP seconds (default 30) and then
exits, so the stall is measurable rather than unbounded.

Fails closed: never prints CHECK lines, never exits 0.
"""
import os
import sys
import time

SLEEP = float(os.environ.get("GRANDCHILD_SLEEP", "30"))


def main() -> int:
    pid = os.fork()
    if pid == 0:
        try:
            os.setsid()          # leave the child's process group
        except OSError:
            pass
        time.sleep(SLEEP)
        os._exit(0)
    # Tell the parent (via stderr) that the grandchild is detached.
    print(f"# detached grandchild pid={pid} sleep={SLEEP}", file=sys.stderr)
    sys.stderr.flush()
    time.sleep(600)             # the candidate itself: sleep past the bound
    return 0


if __name__ == "__main__":
    sys.exit(main())
