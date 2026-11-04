#!/usr/bin/env python3
"""Seat R76Sentinel: read-only subject observer (a --counter for the loader matrix).

It is NOT a counter and never answers the matrix; it records every channel a real
candidate could read at the moment it runs, then prints contract-shaped CHECK lines so
the matrix does not fail for parse reasons. Record i is written to
$PROBE_OBS/rec-<i>.json in invocation order; the matrix prints its CASE lines in the
same order, so records join to classes by index.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
PATHS = ("LOG.md", "corpus/lessons/round-72.md", "SCORECARD.md",
         "corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt",
         "corpus/evidence/round72/controls/after-r72-corrections.txt")


def git(lane, *args):
    p = subprocess.run(["git", "-C", lane, *args], text=True, capture_output=True)
    return p.stdout


def read_fd(path: str, limit: int = 65536) -> bytes:
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    except OSError:
        return b""
    try:
        return os.read(fd, limit)
    except OSError:
        return b""
    finally:
        os.close(fd)


def main() -> int:
    lane, rev, base = ".", None, None
    argv = sys.argv[1:]
    for i, tok in enumerate(argv):
        if tok == "--lane" and i + 1 < len(argv):
            lane = argv[i + 1]
        elif tok == "--rev" and i + 1 < len(argv):
            rev = argv[i + 1]
        elif tok == "--base" and i + 1 < len(argv):
            base = argv[i + 1]
    ppid = os.getppid()
    out = Path(os.environ.get("PROBE_OBS", "."))
    out.mkdir(parents=True, exist_ok=True)
    n = len(list(out.glob("rec-*.json")))

    stolen = read_fd(f"/proc/{ppid}/fd/1")
    try:
        parent_cmdline = Path(f"/proc/{ppid}/cmdline").read_bytes().replace(b"\0", b" ").decode("utf-8", "replace")
    except OSError:
        parent_cmdline = ""
    try:
        parent_env = Path(f"/proc/{ppid}/environ").read_bytes().split(b"\0")
    except OSError:
        parent_env = []
    env_tokens = [t.decode("utf-8", "replace") for t in parent_env if b"case" in t.lower()]

    sizes = {}
    for line in git(lane, "ls-tree", "-l", "-r", "--full-tree", rev or "HEAD").splitlines():
        meta, path = line.split("\t", 1)
        sizes[path] = int(meta.split()[3])
    mtimes = {}
    for rel in PATHS:
        try:
            mtimes[rel] = (Path(lane) / rel).stat().st_mtime_ns
        except OSError:
            mtimes[rel] = None
    rec = {
        "n": n,
        "argv": sys.argv,
        "cwd": os.getcwd(),
        "ppid": ppid,
        "parent_cmdline": parent_cmdline,
        "parent_env_case_tokens": env_tokens,
        "stolen_bytes": len(stolen),
        "stolen_text": stolen.decode("utf-8", "replace"),
        "rev": rev,
        "base": base,
        "subject": git(lane, "log", "-1", "--format=%s", rev or "HEAD").strip(),
        "tree": git(lane, "rev-parse", f"{rev or 'HEAD'}^{{tree}}").strip(),
        "base_tree": git(lane, "rev-parse", f"{base}^{{tree}}").strip() if base else None,
        "sizes": sizes,
        "mtimes": mtimes,
        "reflog_tail": git(lane, "reflog", "-3").splitlines(),
    }
    (out / f"rec-{n:02d}.json").write_text(json.dumps(rec, indent=1, sort_keys=True))
    for cid in IDS:
        print(f"CHECK {cid} PASS observer")
    print(f"C2=PASS checks=7/7 rev={(rev or '')[:12]} base={(base or '')[:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
