#!/usr/bin/env python3
"""CHANNEL PROBE: does the v3 child bound actually bound the child's WORK?

The v3 matrix runs the candidate with `start_new_session=True` and, on expiry,
`os.killpg(p.pid, SIGKILL)` followed by `p.communicate()`.

A candidate that spawns a DETACHED grandchild which inherits the stdout and
stderr pipes keeps those pipes' write ends open after the child itself is
killed.  `p.communicate()` then blocks forever waiting for EOF, so the matrix
never returns and the whole run stalls -- defeating the bound.

This probe:
  * forks a grandchild in its own session (setsid) that holds stdout/stderr
    and sleeps,
  * the child itself sleeps past the matrix's bound.

Fails closed: it never prints CHECK lines and never exits 0.
"""
import os
import sys
import time


def main() -> int:
    # Detached grandchild: new session, inherits the stdout/stderr pipes.
    if os.fork() == 0:
        try:
            os.setsid()
        except OSError:
            pass
        try:
            time.sleep(600)
        finally:
            os._exit(0)
    # The candidate child itself: sleep past the matrix bound.
    time.sleep(600)
    return 0


if __name__ == "__main__":
    sys.exit(main())
