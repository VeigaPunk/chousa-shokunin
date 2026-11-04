#!/usr/bin/env python3
"""CHANNEL PROBE: parent stdout leak, mode-sensitive.

Reads /proc/<ppid>/fd/1 non-blocking and reports how many CASE lines and how
many expected_rc/expected_failed tokens are visible to the child, and what
kind of object the parent's stdout is (pipe vs regular file).
"""
import os, sys, json
from pathlib import Path
def main():
    pid = os.getppid()
    try:
        link = os.readlink(f"/proc/{pid}/fd/1")
    except OSError as e:
        link = f"ERR {e}"
    blob = b""
    err = None
    try:
        fd = os.open(f"/proc/{pid}/fd/1", os.O_RDONLY | os.O_NONBLOCK)
        try:
            blob = os.read(fd, 262144)
        finally:
            os.close(fd)
    except OSError as e:
        err = f"{type(e).__name__}: {e}"
    text = blob.decode("utf-8", "replace")
    rep = {"ppid": pid, "stdout_kind": link, "read_error": err, "bytes": len(blob),
           "case_lines": [l for l in text.splitlines() if l.startswith("CASE ")],
           "has_expected_rc": "expected_rc=" in text,
           "has_expected_failed": "expected_failed=" in text}
    Path(f"/fast/scratch/hyaku/chousa-r76/R76Scout/logs/stdout-mode-{os.getpid()}.json").write_text(json.dumps(rep, indent=1))
    return 1
if __name__ == "__main__":
    sys.exit(main())
