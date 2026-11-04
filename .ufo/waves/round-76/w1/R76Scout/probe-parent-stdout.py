#!/usr/bin/env python3
"""CHANNEL PROBE: parent stdout / parent fds.

The v3 matrix prints one `CASE <name> ... expected_rc=... expected_failed=...`
line per case to ITS OWN stdout, plus `SEED_SHA256=`.  This probe asks whether
the child can read any of that back out of the parent.

Two mechanisms are tried:
  A. open /proc/<ppid>/fd/1  (the classic pipe-reopen trick: for a pipe this
     yields a readable fd on the same pipe inode)
  B. re-read the parent's stdout via /proc/<ppid>/fd/1 as a regular file

Fails closed: always exits 1, prints no CHECK lines.  The observation goes to
$PROBE_REPORT.
"""
import json
import os
import sys
from pathlib import Path


def attempt(desc):
    out = {"desc": desc}
    try:
        fd = os.open(f"/proc/{os.getppid()}/fd/1", os.O_RDONLY | os.O_NONBLOCK)
    except OSError as e:
        out["open_error"] = f"{type(e).__name__}: {e}"
        return out
    try:
        chunks = []
        for _ in range(64):
            try:
                b = os.read(fd, 65536)
            except OSError as e:
                out["read_error"] = f"{type(e).__name__}: {e}"
                break
            if not b:
                break
            chunks.append(b)
        blob = b"".join(chunks)
        text = blob.decode("utf-8", "replace")
        out["bytes"] = len(blob)
        out["head"] = text[:1500]
        out["has_SEED_SHA256"] = "SEED_SHA256=" in text
        out["has_SEED_plain"] = any(ln.startswith("SEED=") for ln in text.splitlines())
        out["has_expected_rc"] = "expected_rc=" in text
        out["has_expected_failed"] = "expected_failed=" in text
        out["case_lines"] = [ln for ln in text.splitlines() if ln.startswith("CASE ")][:20]
    finally:
        os.close(fd)
    return out


def main() -> int:
    rep = {"pid": os.getpid(), "ppid": os.getppid()}
    rep["ppid_fd1_link"] = None
    try:
        rep["ppid_fd1_link"] = os.readlink(f"/proc/{os.getppid()}/fd/1")
    except OSError as e:
        rep["ppid_fd1_link"] = f"ERR {e}"
    rep["attempts"] = [attempt("proc-ppid-fd1 O_NONBLOCK")]
    # also try the parent's stderr and any other inherited fd
    others = {}
    try:
        for fd in sorted(os.listdir(f"/proc/{os.getppid()}/fd")):
            try:
                others[fd] = os.readlink(f"/proc/{os.getppid()}/fd/{fd}")
            except OSError:
                pass
    except OSError as e:
        others = {"ERR": str(e)}
    rep["ppid_fds"] = others
    own = {}
    for fd in sorted(os.listdir("/proc/self/fd")):
        try:
            own[fd] = os.readlink(f"/proc/self/fd/{fd}")
        except OSError:
            pass
    rep["own_fds"] = own
    out = f"/fast/scratch/hyaku/chousa-r76/R76Scout/logs/parent-stdout-{os.getpid()}.json"
    Path(out).write_text(json.dumps(rep, indent=1, sort_keys=True))
    print(json.dumps(rep, sort_keys=True))
    return 1


if __name__ == "__main__":
    sys.exit(main())
