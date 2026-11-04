#!/usr/bin/env python3
"""CHANNEL PROBE: what does the child actually get to see?

Writes a report to $PROBE_REPORT (one file per invocation, keyed by argv --rev)
listing every answer-key channel the v3 matrix leaves open to the candidate:
process/environment channels, parent fds, the fixture commit graph, the patch
text, and the parent's own stdout (both as a pipe and as a regular file).

Fails closed: it always exits 1 and never prints CHECK lines, so the matrix
scores every case as a failure and the report is the only artefact.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def read_proc(pid, name):
    try:
        return Path(f"/proc/{pid}/{name}").read_bytes()
    except OSError as e:
        return f"ERR {e}".encode()


def main() -> int:
    rev = sys.argv[sys.argv.index("--rev") + 1]
    base = sys.argv[sys.argv.index("--base") + 1]
    lane = sys.argv[sys.argv.index("--lane") + 1]
    ppid = os.getppid()
    rep = {"rev": rev, "base": base, "lane": lane, "pid": os.getpid(),
           "ppid": ppid, "t0": time.time()}

    # --- process / environment channels -------------------------------------
    rep["argv"] = sys.argv
    rep["cwd"] = os.getcwd()
    rep["env_keys"] = sorted(os.environ)
    rep["env_matrix_relevant"] = {k: v for k, v in os.environ.items()
                                  if "MATRIX" in k or "LOADER" in k or "SEED" in k}
    rep["ppid_cmdline"] = read_proc(ppid, "cmdline").decode("utf-8", "replace").split("\0")
    rep["ppid_environ_len"] = len(read_proc(ppid, "environ"))
    rep["ppid_environ_matrix"] = [s for s in read_proc(ppid, "environ").decode("utf-8", "replace").split("\0")
                                  if "MATRIX" in s or "LOADER" in s]
    try:
        rep["ppid_fd_list"] = sorted(os.listdir(f"/proc/{ppid}/fd"))
    except OSError as e:
        rep["ppid_fd_list"] = f"ERR {e}"
    # parent stdout: read whatever the parent has already written
    try:
        fd = os.open(f"/proc/{ppid}/fd/1", os.O_RDONLY | os.O_NONBLOCK)
        try:
            blob = os.read(fd, 262144)
        finally:
            os.close(fd)
        rep["ppid_stdout_bytes"] = len(blob)
        rep["ppid_stdout_head"] = blob.decode("utf-8", "replace")[:2000]
        rep["ppid_stdout_has_expected"] = "expected_failed=" in blob.decode("utf-8", "replace")
    except OSError as e:
        rep["ppid_stdout"] = f"ERR {e}"
    # any other parent fd readable?
    readable = {}
    try:
        for fdname in os.listdir(f"/proc/{ppid}/fd"):
            try:
                target = os.readlink(f"/proc/{ppid}/fd/{fdname}")
            except OSError:
                continue
            if target.startswith("pipe:") or target.startswith("socket:"):
                readable[fdname] = target
    except OSError:
        pass
    rep["ppid_pipe_fds"] = readable

    # --- fixture channels ----------------------------------------------------
    def git(*a):
        return subprocess.run(["git", "-C", lane, *a], text=True,
                              capture_output=True).stdout
    rep["git_log_subjects"] = git("log", "--format=%s", base + ".." + rev).split("\n")
    rep["git_rev_count"] = git("rev-list", "--count", base + ".." + rev).strip()
    rep["git_name_only"] = git("diff", "--name-only", base, rev).split()
    rep["git_numstat"] = git("diff", "--numstat", base, rev).strip()
    rep["git_patch"] = git("diff", base, rev)[:2000]
    rep["git_ls_tree_sizes"] = git("ls-tree", "-l", rev).strip()
    rep["git_base_tree"] = git("rev-parse", base + "^{tree}").strip()
    rep["git_rev_tree"] = git("rev-parse", rev + "^{tree}").strip()
    rep["git_commit_subject"] = git("log", "-1", "--format=%s", rev).strip()
    rep["git_commit_count_from_base"] = git("rev-list", "--count", base + ".." + rev).strip()

    # --- timing --------------------------------------------------------------
    rep["t1"] = time.time()
    rep["elapsed"] = rep["t1"] - rep["t0"]

    out = "/fast/scratch/hyaku/chousa-r76/R76Scout/logs/" + REPNAME + "-" + (a_rev if (a_rev := None) else "") + ".json"
    out = "/fast/scratch/hyaku/chousa-r76/R76Scout/logs/" + REPNAME + "-" + _rev + ".json"
    Path(out).write_text(json.dumps(rep, indent=1, sort_keys=True))
    print(json.dumps({k: rep[k] for k in
                      ("rev", "ppid_stdout_bytes", "ppid_stdout_has_expected",
                       "git_rev_count", "git_name_only", "git_numstat",
                       "git_commit_subject", "env_matrix_relevant")}, sort_keys=True))
    return 1


if __name__ == "__main__":
    sys.exit(main())
