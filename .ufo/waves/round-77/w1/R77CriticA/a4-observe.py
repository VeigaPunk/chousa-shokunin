#!/usr/bin/env python3
"""Probe A4 — channel census: what the matrix can observe about its judge and its own call.

Records, per call, to <scratch>/a4-obs.log: ppid, parent argv (/proc/<ppid>/cmdline),
parent cwd and own cwd, the inherited env (full), own argv, the subject path shape, the
parent's open fds and whether they are readable (stdout as a regular file leaks the
ORDER/RUN lines already printed), and whether /proc/<ppid>/mem and /proc/<ppid>/environ
are readable (ptrace gate).

Exits 1 with fewer marks so the battery run is short and uninteresting.
"""
import argparse
import os
import pathlib
import sys

LOG = pathlib.Path("/fast/scratch/hyaku/chousa-r77/R77CriticA/a4-obs.log")


def safe(fn, *a):
    try:
        return fn(*a)
    except Exception as exc:  # noqa: BLE001 - probe records the refusal
        return f"<{type(exc).__name__}: {exc}>"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    ppid = os.getppid()
    lines = [f"call subject={a.counter} work={a.work}",
             f"  own_argv={sys.argv}",
             f"  own_cwd={safe(os.getcwd)}",
             f"  ppid={ppid}",
             f"  parent_cmdline={safe(lambda: pathlib.Path(f'/proc/{ppid}/cmdline').read_bytes())}",
             f"  parent_cwd={safe(lambda: os.readlink(f'/proc/{ppid}/cwd'))}",
             f"  parent_exe={safe(lambda: os.readlink(f'/proc/{ppid}/exe'))}",
             f"  env={sorted(os.environ.items())}",
             f"  subject_bytes={safe(lambda: pathlib.Path(a.counter).stat().st_size)}",
             f"  subject_dir_entries={safe(lambda: sorted(p.name for p in pathlib.Path(a.counter).parent.iterdir()))}"]
    fds = safe(lambda: sorted(os.listdir(f"/proc/{ppid}/fd")))
    lines.append(f"  parent_fds={fds}")
    if isinstance(fds, list):
        for fd in fds:
            target = safe(lambda: os.readlink(f"/proc/{ppid}/fd/{fd}"))
            kind = "?"
            if isinstance(target, str) and target.startswith("/"):
                kind = "file" if pathlib.Path(target).is_file() else "other"
            elif isinstance(target, str):
                kind = target
            lines.append(f"    fd{fd} -> {target} [{kind}]")
            if kind == "file":
                head = safe(lambda: pathlib.Path(target).read_text()[-400:])
                lines.append(f"      tail400={head!r}")
    lines.append(f"  parent_mem_readable={safe(lambda: bool(pathlib.Path(f'/proc/{ppid}/mem').open('rb')))}")
    lines.append(f"  parent_environ_readable={safe(lambda: len(pathlib.Path(f'/proc/{ppid}/environ').read_bytes()))}")
    lines.append(f"  ptrace_scope={safe(lambda: pathlib.Path('/proc/sys/kernel/yama/ptrace_scope').read_text().strip())}")
    with LOG.open("a") as fh:
        fh.write("\n".join(lines) + "\n---\n")
    print("LOADER_MATRIX=0/12 MATRIX=FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
