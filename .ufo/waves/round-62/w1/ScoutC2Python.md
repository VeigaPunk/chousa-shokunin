# ScoutC2Python — openat2 sourcing on this host (round 62, w1, item C2 scout)

Scope: read-only host evidence for the frozen claim "Python 3.14.8 has no openat2 function" (C2 wording in
`corpus/evidence/round62/claims.md`). Nothing in the lane was edited. No network, no installs, no pacman.

## Findings

1. **The Python `os` module has no `openat2` on any installed CPython.** Python 3.14.8 (`/usr/bin/python3`,
   `/usr/bin/python3.14`) and the uv-managed 3.13.16, 3.12.15 and 3.11.17 all report `hasattr(os, "openat2") == False`.
   The 3.14.8 interpreter also has no `openat2` string in its binary, in `libpython3.14.so.1.0`, or anywhere under
   `/usr/lib/python3.14/` (the stdlib tree).
2. **Python's documentation text does not mention it.** No python docs package is installed
   (`ls /usr/share/doc | grep -i python` lists only third-party `python-*` packages). `python3 -m pydoc os.open`
   prints nothing matching `openat2`, and `python3 -m pydoc os` has zero matches.
3. **glibc 2.44 exports `openat2`.** `readelf --dyn-syms -W /usr/lib/libc.so.6` shows
   `openat2@@GLIBC_2.43` (WEAK, FUNC). The libc headers declare it: `/usr/include/bits/fcntl-linux-fortify.h`
   (wrapper with a size check, `__openat2_alias`) and `/usr/include/bits/fcntl-linux.h` (includes `linux/openat2.h`).
4. **The kernel UAPI header is present.** `/usr/include/linux/openat2.h` defines `struct open_how` and the
   `RESOLVE_*` flags (`RESOLVE_NO_XDEV`, `RESOLVE_NO_MAGICLINKS`, `RESOLVE_NO_SYMLINKS`, `RESOLVE_BENEATH`,
   `RESOLVE_IN_ROOT`, `RESOLVE_CACHED`). `/usr/include/asm/unistd_64.h:354` has `#define __NR_openat2 437`.
5. **The host binaries reference the syscall.** `strings /usr/bin/strace` contains `openat2` (3 lines, including the
   `strace --trace=?open,?openat,?openat2` usage text). `strings /usr/lib/libc.so.6` contains it (1 line).
   `/usr/lib/systemd/systemd`, `/usr/bin/cat` and `/usr/bin/mv` contain no `openat2` string (0 matches). Absence in
   these binaries says nothing about the kernel; it only means they do not name the call.
6. **Live kernel behavior, reached through libc and not through Python's `os`.** A ctypes call to the libc symbol in
   a scratch fixture (symlink `link -> target.txt`, `dirfd` opened on the directory):
   - `openat2(dfd, "link", {O_RDONLY, resolve=RESOLVE_NO_SYMLINKS})` returned -1 with `errno = ELOOP`.
   - `openat2(dfd, "link", {O_RDONLY, resolve=0})` returned a valid fd.
   This shows the kernel implements the call on this host (kernel 7.2.11-arch1-1). Caveat: this is one kernel, one
   filesystem, and it is a ctypes probe that is not in the frozen probe `corpus/evidence/round62/openat2-probe.py`.

## Interpretation (INFERENCE where marked)

- The claim's words "Python 3.14.8 has no openat2 function" hold only at the level of the Python standard library
  surface: no `os.openat2`, and no openat2 in the CPython binary or stdlib. Python can still reach the call through
  `ctypes` and the libc symbol (observed in item 6).
- So the sourced statement is narrower than "no openat2 anywhere on the host": the stdlib is absent; libc (2.44,
  symbol at GLIBC_2.43) and the kernel carry it. [INFERENCE] The claim's wording should say "the Python `os` module
  has no `openat2`", or cite the libc symbol, to avoid being read as a claim about the kernel.
- A Python 3.15 or a future `os.openat2` is outside what this host shows; not checked.

## Second and other Python versions

- `/usr/bin/python3.14` (3.14.8): absent (same binary family as `/usr/bin/python3`).
- `/home/vgpnk/.local/bin/python3.13` (3.13.16), `python3.12` (3.12.15), `python3.11` (3.11.17): all symlinks into
  `/home/vgpnk/.local/share/uv/python/cpython-*`; all report absent.
- Not checked: any Python build outside these paths.

## Sources (k = 13 items, each opened this round)

1. `python3 -c 'import os,sys; print(sys.version); print(hasattr(os,"openat2"))'` → `3.14.8 ...` / `False`
2. `/usr/bin/python3.14 -c` hasattr → `3.14.8 openat2: False`
3. `/home/vgpnk/.local/bin/python3.13` → `3.13.16 openat2: False`
4. `python3.12` → `3.12.15 openat2: False`
5. `python3.11` → `3.11.17 openat2: False`
6. `python3 -m pydoc os.open | grep -i openat2` → no output, exit 1
7. `grep -rl openat2 /usr/lib/python3.14/` → 0 matches, exit 1
8. `strings /usr/bin/python3.14 | grep -c openat2` → 0; `strings /usr/lib/libpython3.14.so.1.0 | grep -c openat2` → 0
9. `/usr/include/linux/openat2.h` (struct open_how, RESOLVE_*) and `/usr/include/asm/unistd_64.h:354` (`__NR_openat2 437`)
10. `/usr/include/bits/fcntl-linux-fortify.h:25-46` and `/usr/include/bits/fcntl-linux.h:468-474` (glibc declarations)
11. `readelf --dyn-syms -W /usr/lib/libc.so.6` → `2928: ... WEAK DEFAULT 13 openat2@@GLIBC_2.43`; `ldd --version` → `ldd (GNU libc) 2.44`
12. `strings /usr/bin/strace | grep openat2` → 3 lines; `strings /usr/lib/libc.so.6 | grep -c openat2` → 1
13. ctypes probe in scratch: `RESOLVE_NO_SYMLINKS` → ELOOP; `resolve=0` → fd (live kernel)

Commands were run with the working directory set to the lane fixture scratch
`/fast/scratch/hyaku/chousa-r62/ScoutC2Python`, which is removed before this report was written. No file in the lane
was touched. `strace`, `systemd`, `coreutils` checked by `strings` only; no binary was executed for this check
other than the probe above.

Tool installs: none. Records: none needed.

## Remaining unknowns

- Other kernels, other filesystems, non-x86_64 hosts: not checked (claim names one host).
- Entailment of the C2 entry's wording to these facts: not machine-checked (claim's named limit).
- The claim's "no openat2 function" is ambiguous (see Interpretation); the reviewers should decide which reading the entry
  states.

VERDICT: PYTHON_OPENAT2=absent sources=13
