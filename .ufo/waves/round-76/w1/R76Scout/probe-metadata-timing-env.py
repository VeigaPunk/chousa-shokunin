#!/usr/bin/env python3
"""CHANNEL PROBE: fixture metadata (mtime), environment, timing, commit graph.

Records, from inside the child:
  * the mtimes of the five fixture files (the matrix restores every file then
    writes the mutated one last -> mtime ordering may reveal the mutated path)
  * the full environment and the parent's environment
  * wall-clock timings of the child and of the parent's own printed markers
  * the fixture commit graph: subject list, commit count, per-commit numstat
  * the parent's argv (does it name the matrix file?)

Fails closed: always exits 1, prints no CHECK lines.  Report -> $PROBE_REPORT.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

T0 = time.time()


def main() -> int:
    lane = sys.argv[sys.argv.index("--lane") + 1]
    base = sys.argv[sys.argv.index("--base") + 1]
    rev = sys.argv[sys.argv.index("--rev") + 1]
    rep = {"pid": os.getpid(), "ppid": os.getppid(), "t_start": T0,
           "cwd": os.getcwd(), "argv": sys.argv}

    # ---- environment ------------------------------------------------------
    rep["env"] = dict(os.environ)
    try:
        raw = Path(f"/proc/{os.getppid()}/environ").read_bytes()
        rep["ppid_environ"] = dict(
            kv.split("=", 1) for kv in raw.decode("utf-8", "replace").split("\0")
            if "=" in kv)
    except OSError as e:
        rep["ppid_environ"] = f"ERR {e}"
    rep["env_contains_matrix_marker"] = {
        k: v for k, v in os.environ.items()
        if "MATRIX" in k.upper() or "LOADER" in k.upper() or "SEED" in k.upper()}

    # ---- parent argv ------------------------------------------------------
    try:
        rep["ppid_cmdline"] = Path(f"/proc/{os.getppid()}/cmdline").read_bytes().decode("utf-8", "replace").split("\0")
    except OSError as e:
        rep["ppid_cmdline"] = f"ERR {e}"
    try:
        rep["ppid_cwd"] = os.readlink(f"/proc/{os.getppid()}/cwd")
    except OSError as e:
        rep["ppid_cwd"] = f"ERR {e}"

    # ---- fixture metadata: mtimes ----------------------------------------
    mt = []
    for p in sorted(Path(lane).rglob("*")):
        if p.is_file():
            try:
                st = p.stat()
            except OSError:
                continue
            mt.append({"path": str(p.relative_to(lane)), "mtime_ns": st.st_mtime_ns,
                       "size": st.st_size})
    rep["mtimes"] = mt
    rep["mtime_newest"] = max(mt, key=lambda e: e["mtime_ns"])["path"] if mt else None
    rep["mtime_order"] = [e["path"] for e in sorted(mt, key=lambda e: -e["mtime_ns"])]

    # ---- commit graph -----------------------------------------------------
    def git(*a):
        return subprocess.run(["git", "-C", lane, *a], text=True,
                              capture_output=True).stdout
    rep["commit_count"] = git("rev-list", "--count", base + ".." + rev).strip()
    rep["commit_subjects"] = git("log", "--format=%s", base + ".." + rev).split("\n")
    rep["commit_numstats"] = git("log", "--format=COMMIT %h", "--numstat", base + ".." + rev).strip()
    rep["head_subject"] = git("log", "-1", "--format=%s", rev).strip()
    rep["numstat"] = git("diff", "--numstat", base, rev).strip()
    rep["name_only"] = git("diff", "--name-only", base, rev).split()
    rep["ls_tree"] = git("ls-tree", "-l", rev).strip()

    # ---- timing -----------------------------------------------------------
    rep["t_end"] = time.time()
    rep["elapsed"] = rep["t_end"] - T0
    try:
        stat = Path(f"/proc/{os.getppid()}/stat").read_text().split()
        rep["ppid_starttime_ticks"] = stat[21]
        rep["clock_ticks"] = os.sysconf("SC_CLK_TCK")
    except (OSError, IndexError) as e:
        rep["ppid_starttime"] = f"ERR {e}"

    out = f"/fast/scratch/hyaku/chousa-r76/R76Scout/logs/metadata-timing-{os.getpid()}.json"
    Path(out).write_text(json.dumps(rep, indent=1, sort_keys=True))
    print(json.dumps({k: rep[k] for k in ("mtime_newest", "mtime_order", "commit_count",
                                          "commit_subjects", "numstat", "name_only",
                                          "env_contains_matrix_marker", "elapsed")},
                     sort_keys=True))
    return 1


if __name__ == "__main__":
    sys.exit(main())
