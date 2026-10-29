#!/usr/bin/env python3
"""openat2 probe (round 62): what the kernel on this host does for the RESOLVE_* flags the openat2(2) page
lists, next to what Python's own `os.open` does. Constants and the syscall number are read from the
installed headers (`/usr/include/linux/openat2.h`, `/usr/include/asm/unistd_64.h`), never typed here.

Usage: python3 corpus/evidence/round62/openat2-probe.py --work DIR   (DIR absent or empty, its parent present and
not a symlink itself; removed afterwards)
Prints `HEADER`, `PROBE <id> <name> observed=<x> expected=<y> ok|DIFFERENT` lines, `KERNEL`, `PYTHON` lines, then
`PROBE_FACTS=<k>/<n>`. `expected` is typed in this script by its author: `PROBE_FACTS` counts agreement between
the host and those typed expectations, a self-consistency check and not an independent measurement. Basis of each
expectation (S138 = /usr/share/man/man2/openat2.2.gz, man-pages 6.19): P02 IMPLIED by the RESOLVE_NO_SYMLINKS
paragraph (O_NOFOLLOW affects only the final component); P04, P05, P07, P08, P10, P12, P13, P14 stated by S138
(ERRORS ELOOP/EXDEV/EINVAL, how.resolve entries, the O_PATH sentence); P06, P09 are controls (a path that stays
inside the tree opens); P01, P03, P11 have NO sentence in S138 or S139 and are the author's INFERENCE (Python's `os`
module; open(2) ELOOP for O_NOFOLLOW on a final symlink; a plain open follows an absolute symlink).
Exit codes: 0 all facts as expected · 1 a fact differs or cleanup failed · 2 usage/environment (not Linux x86_64,
headers missing, --work refused) · 3 the openat2 syscall is unavailable (ENOSYS/EPERM, e.g. seccomp).
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


class Unavailable(Exception):
    pass


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
    raw = pathlib.Path(a.work)
    if raw.is_symlink() or not raw.parent.is_dir():
        print("openat2-probe: --work must not be a symlink and its parent must exist", file=sys.stderr)
        return 2
    work = raw.resolve()
    if work.exists() and any(work.iterdir()):
        print("openat2-probe: --work must be absent or empty", file=sys.stderr)
        return 2
    work.mkdir(exist_ok=True)
    os.umask(0o022)

    def openat2(dirfd, path, flags=os.O_RDONLY, resolve=0, mode=0):
        how = OpenHow(flags, mode, resolve)
        fd = libc.syscall(nr, dirfd, os.fsencode(path), ctypes.byref(how), ctypes.sizeof(how))
        return ("fd", fd) if fd >= 0 else ("errno", ctypes.get_errno())

    def name(res):
        if res[0] == "fd":
            os.close(res[1])
            return "opened"
        return errno.errorcode.get(res[1], str(res[1]))

    lines, facts, cleanup_errors, unavailable = [], [], [], None

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
            pre = openat2(dfd, "f.txt")
            if pre[0] == "errno" and pre[1] in (errno.ENOSYS, errno.EPERM):
                raise Unavailable(errno.errorcode[pre[1]])
            if pre[0] == "fd":
                os.close(pre[1])
            # P01 Python's os.open reaches openat but the module has no openat2 function.
            # cite P01: INFERENCE (the os module's contents; neither S138 nor S139 says anything about Python)
            probe("P01", "python-os-has-openat2", hasattr(os, "openat2"), False)
            # P02..P03 O_NOFOLLOW is a final-component rule (the page: earlier components are followed).
            try:
                fd = os.open("linkdir/f.txt", os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dfd)
                os.close(fd)
                r = "opened"
            except OSError as e:
                r = errno.errorcode.get(e.errno, str(e.errno))
            # cite P02: S138 "which affects the handling of symbolic links only in the final component of path"
            probe("P02", "os.open-O_NOFOLLOW-symlink-in-earlier-component", r, "opened")
            try:
                fd = os.open("flink", os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dfd)
                os.close(fd)
                r = "opened"
            except OSError as e:
                r = errno.errorcode.get(e.errno, str(e.errno))
            # cite P03: INFERENCE (open(2) ERRORS lists ELOOP for O_NOFOLLOW on a final symlink; S138 does not, see S134)
            probe("P03", "os.open-O_NOFOLLOW-symlink-final-component", r, "ELOOP")
            # P04..P05 RESOLVE_NO_SYMLINKS covers every component.
            # cite P04: S138 "ELOOP how.resolve contains RESOLVE_NO_SYMLINKS, and one of the path components was a symbolic link"
            probe("P04", "openat2-NO_SYMLINKS-symlink-in-earlier-component",
                  name(openat2(dfd, "linkdir/f.txt", resolve=R["RESOLVE_NO_SYMLINKS"])), "ELOOP")
            # cite P05: S138 "ELOOP how.resolve contains RESOLVE_NO_SYMLINKS, and one of the path components was a symbolic link"
            probe("P05", "openat2-NO_SYMLINKS-symlink-final-component",
                  name(openat2(dfd, "flink", resolve=R["RESOLVE_NO_SYMLINKS"])), "ELOOP")
            # cite P06: INFERENCE (control: a path that stays inside the tree opens; S138 states only the refusals)
            probe("P06", "openat2-NO_SYMLINKS-plain-path-inside",
                  name(openat2(dfd, "real/f.txt", resolve=R["RESOLVE_NO_SYMLINKS"])), "opened")
            # P07..P09 RESOLVE_BENEATH: a dotdot that leaves dirfd, an absolute symlink, a path inside.
            # cite P07: S138 "EXDEV how.resolve contains either RESOLVE_IN_ROOT or RESOLVE_BENEATH, and an escape from the root during path resolution was detected"
            probe("P07", "openat2-BENEATH-dotdot-escape",
                  name(openat2(dfd, "real/../../outside.txt", resolve=R["RESOLVE_BENEATH"])), "EXDEV")
            # cite P08: S138 "EXDEV how.resolve contains either RESOLVE_IN_ROOT or RESOLVE_BENEATH, and an escape from the root during path resolution was detected"
            probe("P08", "openat2-BENEATH-absolute-symlink",
                  name(openat2(dfd, "abslink", resolve=R["RESOLVE_BENEATH"])), "EXDEV")
            # cite P09: INFERENCE (control: a relative symlink that stays inside the directory is not an escape)
            probe("P09", "openat2-BENEATH-relative-symlink-inside",
                  name(openat2(dfd, "linkdir/f.txt", resolve=R["RESOLVE_BENEATH"])), "opened")
            # P10 RESOLVE_IN_ROOT: an absolute symlink is read relative to dirfd.
            r = openat2(dfd, "absroot", resolve=R["RESOLVE_IN_ROOT"])
            got = None
            if r[0] == "fd":
                got = os.read(r[1], 64).decode().strip()
                os.close(r[1])
            # cite P10: S138 "Absolute symbolic links are interpreted relative to dirfd"
            probe("P10", "openat2-IN_ROOT-absolute-symlink-content", got, "rootfile")
            # P11 the same absolute link without the flag leaves the tree (plain openat follows it).
            try:
                fd = os.open("abslink", os.O_RDONLY, dir_fd=dfd)
                got = os.read(fd, 64).decode().strip()
                os.close(fd)
            except OSError as e:
                got = errno.errorcode.get(e.errno, str(e.errno))
            # cite P11: INFERENCE (a plain open with a directory descriptor follows an absolute symlink; open(2), not S138)
            probe("P11", "os.open-dir_fd-absolute-symlink-content", got, "outside")
            # P12 unknown resolve bit and a nonzero mode without O_CREAT are errors, not ignored.
            # cite P12: S138 "EINVAL An unknown flag or invalid value was specified in how."
            probe("P12", "openat2-unknown-resolve-bit", name(openat2(dfd, "f.txt", resolve=1 << 14)), "EINVAL")
            # cite P13: S138 "EINVAL mode is nonzero, but how.flags does not contain O_CREAT or O_TMPFILE."
            probe("P13", "openat2-mode-without-O_CREAT", name(openat2(dfd, "f.txt", mode=0o600)), "EINVAL")
            # P14 O_PATH|O_NOFOLLOW on a symlink with NO_SYMLINKS returns a descriptor for the link itself.
            r = openat2(dfd, "flink", flags=os.O_PATH | os.O_NOFOLLOW, resolve=R["RESOLVE_NO_SYMLINKS"])
            tgt = None
            if r[0] == "fd":
                tgt = os.readlink(f"/proc/self/fd/{r[1]}") == str(root / "flink")
                os.close(r[1])
            # cite P14: S138 "then an O_PATH file descriptor referencing the symbolic link will be returned"
            probe("P14", "openat2-O_PATH-O_NOFOLLOW-NO_SYMLINKS-final-symlink-fd-is-the-link", tgt, True)
        finally:
            os.close(dfd)
    except Unavailable as e:
        unavailable = str(e)
    finally:
        shutil.rmtree(work, onexc=lambda fn, p, exc: cleanup_errors.append(p))
    if unavailable:
        print(f"openat2-probe: openat2 unavailable ({unavailable})", file=sys.stderr)
        return 3
    if cleanup_errors:
        print(f"openat2-probe: cleanup failed for {len(cleanup_errors)} paths under {work}", file=sys.stderr)
        return 1
    print(f"KERNEL {platform.release()}")
    print(f"PYTHON {platform.python_version()}")
    print("HEADER " + " ".join(f"{k}={v:#x}" for k, v in R.items()) + f" __NR_openat2={nr}")
    print("\n".join(lines))
    k = sum(facts)
    print(f"PROBE_FACTS={k}/{len(facts)}")
    return 0 if k == len(facts) else 1


if __name__ == "__main__":
    sys.exit(main())
