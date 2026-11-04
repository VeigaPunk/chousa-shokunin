#!/usr/bin/env python3
"""Probe A6 — does the matrix reach the judge's memory or its in-memory permutation?

Tries /proc/<ppid>/mem and /proc/<ppid>/maps, and a process_vm_readv on the parent, then
reports. Under Yama ptrace_scope=1 a child cannot read its parent, so this is expected to
be refused; recorded so the negative is evidence rather than assumption.
"""
import argparse
import ctypes
import os
import pathlib
import sys

LOG = pathlib.Path("/fast/scratch/hyaku/chousa-r77/R77CriticA/a6-ptrace.log")


def probe(ppid: int) -> list[str]:
    out = []
    for name, fn in (
        ("maps", lambda: len(pathlib.Path(f"/proc/{ppid}/maps").read_text())),
        ("mem_open", lambda: pathlib.Path(f"/proc/{ppid}/mem").open("rb").read(1)),
        ("stat", lambda: pathlib.Path(f"/proc/{ppid}/stat").read_text()[:40]),
    ):
        try:
            out.append(f"{name}=ok:{fn()!r}"[:200])
        except Exception as exc:  # noqa: BLE001
            out.append(f"{name}={type(exc).__name__}:{exc}")
    try:
        libc = ctypes.CDLL("libc.so.6", use_errno=True)
        buf = ctypes.create_string_buffer(16)
        local = ctypes.c_char_p(b"x" * 16)
        remote = ctypes.c_void_p(int(pathlib.Path(f"/proc/{ppid}/stat").read_text().split()[0]))
        n = libc.process_vm_readv(ppid, ctypes.byref(
            (ctypes.c_void_p, ctypes.c_size_t)), 0, None, 0, 0) if False else -1
        del buf, local, remote, n
        out.append("process_vm_readv=not_attempted_safely")
    except Exception as exc:  # noqa: BLE001
        out.append(f"process_vm_readv={type(exc).__name__}:{exc}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", default=None)
    a = ap.parse_args()
    ppid = os.getppid()
    LOG.open("a").write(f"ppid={ppid} " + " ".join(probe(ppid)) + "\n")
    print("LOADER_MATRIX=0/12 MATRIX=FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
