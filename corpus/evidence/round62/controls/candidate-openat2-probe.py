#!/usr/bin/env python3
"""openat2 probe (round 62): what the kernel on this host does for the RESOLVE_* flags the openat2(2) page
lists, next to what Python's own `os.open` does. Constants and the syscall number are read from the
installed headers (`/usr/include/linux/openat2.h`, `/usr/include/asm/unistd_64.h`), never typed here.

Usage: python3 corpus/evidence/round62/openat2-probe.py --work DIR   (DIR absent or empty; removed afterwards)
Prints `PROBE <id> <name> <observed>` lines, `KERNEL`, `PYTHON` lines, then `PROBE_FACTS=<k>/<n>` (the number of
probes whose observed result equals the result the openat2(2) page states or implies) and exits 0 when k == n.
Linux x86_64 only (the syscall number is read from the x86_64 header); exit 2 elsewhere.
"""
import argparse
import ctypes
import errno
import os
import pathlib
import platform
import re
import shutil
import sys

HDR = pathlib.Path("/usr/include/linux/openat2.h")
NRS = pathlib.Path("/usr/include/asm/unistd_64.h")


def const(text, name):
    m = re.search(rf"#define\s+{name}\s+(0x[0-9a-fA-F]+|\d+)", text)
    return int(m.group(1), 0)


class OpenHow(ctypes.Structure):
    _fields_ = [("flags", ctypes.c_uint64), ("mode", ctypes.c_uint64), ("resolve", ctypes.c_uint64)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    if platform.system() != "Linux" or platform.machine() != "x86_64" or not HDR.is_file() or not NRS.is_file():
        print("openat2-probe: needs Linux x86_64 with linux/openat2.h and asm/unistd_64.h", file=sys.stderr)
        return 2
    h, n = HDR.read_text(), NRS.read_text()
    R = {k: const(h, k) for k in ("RESOLVE_NO_XDEV", "RESOLVE_NO_MAGICLINKS", "RESOLVE_NO_SYMLINKS",
                                  "RESOLVE_BENEATH", "RESOLVE_IN_ROOT", "RESOLVE_CACHED")}
    nr = const(n, "__NR_openat2")
    libc = ctypes.CDLL(None, use_errno=True)
    libc.syscall.restype = ctypes.c_long
    work = pathlib.Path(a.work).resolve()
    if work.exists() and any(work.iterdir()):
        print("openat2-probe: --work must be absent or empty", file=sys.stderr)
        return 2
    work.mkdir(parents=True, exist_ok=True)

    def openat2(dirfd, path, flags=os.O_RDONLY, resolve=0, mode=0):
        how = OpenHow(flags, mode, resolve)
        fd = libc.syscall(nr, dirfd, os.fsencode(path), ctypes.byref(how), ctypes.sizeof(how))
        return ("fd", fd) if fd >= 0 else ("errno", ctypes.get_errno())

    def name(res):
        if res[0] == "fd":
            os.close(res[1])
            return "opened"
        return errno.errorcode.get(res[1], str(res[1]))

    lines, facts = [], []

    def probe(pid, label, observed, expected):
        ok = observed == expected
        lines.append(f"PROBE {pid} {label} observed={observed} expected={expected} {'ok' if ok else 'DIFFERENT'}")
        facts.append(ok)

    try:
        root = work / "root"
        (root / "real").mkdir(parents=True)
        (root / "real" / "f.txt").write_text("inside\n")
        (root / "f.txt").write_text("rootfile")
        (work / "outside.txt").write_text("outside")
        (root / "linkdir").symlink_to("real")
        (root / "flink").symlink_to("f.txt")
        (root / "abslink").symlink_to(str(work / "outside.txt"))
        (root / "absroot").symlink_to("/f.txt")
        dfd = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            # P01 Python's os.open reaches openat but the module has no openat2 function.
            probe("P01", "python-os-has-openat2", hasattr(os, "openat2"), False)
            # P02..P03 O_NOFOLLOW is a final-component rule (the page: earlier components are followed).
            try:
                fd = os.open("linkdir/f.txt", os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dfd)
                os.close(fd)
                r = "opened"
            except OSError as e:
                r = errno.errorcode.get(e.errno, str(e.errno))
            probe("P02", "os.open-O_NOFOLLOW-symlink-in-earlier-component", r, "opened")
            try:
                fd = os.open("flink", os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dfd)
                os.close(fd)
                r = "opened"
            except OSError as e:
                r = errno.errorcode.get(e.errno, str(e.errno))
            probe("P03", "os.open-O_NOFOLLOW-symlink-final-component", r, "ELOOP")
            # P04..P05 RESOLVE_NO_SYMLINKS covers every component.
            probe("P04", "openat2-NO_SYMLINKS-symlink-in-earlier-component",
                  name(openat2(dfd, "linkdir/f.txt", resolve=R["RESOLVE_NO_SYMLINKS"])), "ELOOP")
            probe("P05", "openat2-NO_SYMLINKS-symlink-final-component",
                  name(openat2(dfd, "flink", resolve=R["RESOLVE_NO_SYMLINKS"])), "ELOOP")
            probe("P06", "openat2-NO_SYMLINKS-plain-path-inside",
                  name(openat2(dfd, "real/f.txt", resolve=R["RESOLVE_NO_SYMLINKS"])), "opened")
            # P07..P09 RESOLVE_BENEATH: a dotdot that leaves dirfd, an absolute symlink, a path inside.
            probe("P07", "openat2-BENEATH-dotdot-escape",
                  name(openat2(dfd, "real/../../outside.txt", resolve=R["RESOLVE_BENEATH"])), "EXDEV")
            probe("P08", "openat2-BENEATH-absolute-symlink",
                  name(openat2(dfd, "abslink", resolve=R["RESOLVE_BENEATH"])), "EXDEV")
            probe("P09", "openat2-BENEATH-relative-symlink-inside",
                  name(openat2(dfd, "linkdir/f.txt", resolve=R["RESOLVE_BENEATH"])), "opened")
            # P10 RESOLVE_IN_ROOT: an absolute symlink is read relative to dirfd.
            r = openat2(dfd, "absroot", resolve=R["RESOLVE_IN_ROOT"])
            got = None
            if r[0] == "fd":
                got = os.read(r[1], 64).decode().strip()
                os.close(r[1])
            probe("P10", "openat2-IN_ROOT-absolute-symlink-content", got, "rootfile")
            # P11 the same absolute link without the flag leaves the tree (plain openat follows it).
            try:
                fd = os.open("abslink", os.O_RDONLY, dir_fd=dfd)
                got = os.read(fd, 64).decode().strip()
                os.close(fd)
            except OSError as e:
                got = errno.errorcode.get(e.errno, str(e.errno))
            probe("P11", "os.open-dir_fd-absolute-symlink-content", got, "outside")
            # P12 unknown resolve bit and a nonzero mode without O_CREAT are errors, not ignored.
            probe("P12", "openat2-unknown-resolve-bit", name(openat2(dfd, "f.txt", resolve=1 << 14)), "EINVAL")
            probe("P13", "openat2-mode-without-O_CREAT", name(openat2(dfd, "f.txt", mode=0o600)), "EINVAL")
            # P14 O_PATH|O_NOFOLLOW on a symlink with NO_SYMLINKS returns a descriptor for the link itself.
            r = openat2(dfd, "flink", flags=os.O_PATH | os.O_NOFOLLOW, resolve=R["RESOLVE_NO_SYMLINKS"])
            tgt = None
            if r[0] == "fd":
                tgt = os.readlink(f"/proc/self/fd/{r[1]}") == str(root / "flink")
                os.close(r[1])
            probe("P14", "openat2-O_PATH-O_NOFOLLOW-NO_SYMLINKS-final-symlink-fd-is-the-link", tgt, True)
        finally:
            os.close(dfd)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"KERNEL {platform.release()}")
    print(f"PYTHON {platform.python_version()}")
    print("HEADER " + " ".join(f"{k}={v:#x}" for k, v in R.items()) + f" __NR_openat2={nr}")
    print("\n".join(lines))
    k = sum(facts)
    print(f"PROBE_FACTS={k}/{len(facts)}")
    return 0 if k == len(facts) else 1


if __name__ == "__main__":
    sys.exit(main())
