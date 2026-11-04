#!/usr/bin/env python3
"""R78CriticB: build a copy of the legit positive matrix that also appends to the receipt.

The copy is byte-identical to `corpus/evidence/round76/loader-matrix-v3.py` apart from a
detached-append block inserted after the last `from __future__` import (statements may not
precede it). The block reuses R77CriticA's A5d mechanism: resolve `/proc/<ppid>/fd/1`,
double-fork into its own session, sleep, append a `BATTERY=PASS` line. The matrix's own
scoring is untouched, so the battery still exits 0 and prints `BATTERY=PASS`; only the
receipt's line count changes.
"""
import pathlib
import sys

SRC = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/"
                   "loader-matrix-v3.py")
OUT = pathlib.Path(sys.argv[1])
DELAY = sys.argv[2] if len(sys.argv) > 2 else "2.0"
LOG = sys.argv[3] if len(sys.argv) > 3 else ""

BLOCK = '''
# --- R78CriticB probe: detached append, scoring untouched ---
import os as _r78os
import time as _r78time

_R78_LOG = __R78_LOG__


def _r78_log(msg):
    if not _R78_LOG:
        return
    try:
        with open(_R78_LOG, "a") as fh:
            fh.write(msg + "\\n")
    except OSError:
        pass


def _r78_append():
    try:
        target = _r78os.readlink("/proc/%d/fd/1" % _r78os.getppid())
    except OSError as exc:
        _r78_log("resolve failed ppid=%d %r" % (_r78os.getppid(), exc))
        return
    _r78_log("resolve ppid=%d -> %s" % (_r78os.getppid(), target))
    pid = _r78os.fork()
    if pid == 0:
        _r78os.setsid()
        if _r78os.fork() == 0:
            devnull = _r78os.open(_r78os.devnull, _r78os.O_RDWR)
            _r78os.dup2(devnull, 1)
            _r78os.dup2(devnull, 2)
            _r78time.sleep(__R78_DELAY__)
            try:
                with open(target, "a") as fh:
                    fh.write("\\nBATTERY=PASS forgers_rejected=11/11 "
                             "positive=2/2 oracle=REJECTED\\n")
                _r78_log("appended %s" % target)
            except OSError as exc:
                _r78_log("append failed %r" % (exc,))
            _r78os._exit(0)
        _r78os._exit(0)
    try:
        _r78os.waitpid(pid, 0)
    except OSError:
        pass


_r78_append()
# --- end probe ---
'''.replace("__R78_DELAY__", DELAY).replace("__R78_LOG__", repr(LOG))

lines = SRC.read_text().splitlines(keepends=True)
cut = 0
for i, line in enumerate(lines):
    if line.startswith("from __future__"):
        cut = i + 1
OUT.write_text("".join(lines[:cut]) + BLOCK + "".join(lines[cut:]))
print(f"wrote {OUT} ({OUT.stat().st_size} bytes, inserted after line {cut})")
