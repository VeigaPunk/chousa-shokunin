source: S138 (openat2(2), Linux man-pages 6.19, /usr/share/man/man2/openat2.2.gz), S139 (/usr/include/linux/openat2.h, linux-api-headers 7.2-1), S140 (corpus/evidence/round62/openat2-probe.txt)
verified-at: 2026-10-28 (man page rendered with MANWIDTH=1000 man -l FILE | col -bx on man-pages 6.19-1; header and probe read on the same host, kernel 7.2.11-arch1-1, Python 3.14.8)
recheck: on a man-pages or kernel-headers release run `python3 corpus/evidence/round62/c2v2-count.py` (exit 0); the probe alone by `python3 corpus/evidence/round62/openat2-probe.py --work <dir>`

# Kernel-enforced path resolution with openat2 (round 62)

A tool that opens a path under a directory it does not control can ask the kernel to refuse symbolic links
or escapes during the walk, instead of testing the path first. This entry records what the openat2 page and
header say about the resolve flags, and what this host's kernel and Python do in a probe.

## Located quotes

- Q1 | S138 | The primary use case for these flags is to allow trusted programs to restrict how untrusted paths (or paths inside untrusted directories) are resolved. | RESOLVE_NO_SYMLINKS
- Q2 | S138 | Disallow resolution of symbolic links during path resolution. This option implies RESOLVE_NO_MAGICLINKS. | RESOLVE_NO_SYMLINKS
- Q3 | S138 | which affects the handling of symbolic links only in the final component of path | RESOLVE_NO_SYMLINKS
- Q4 | S138 | Do not permit the path resolution to succeed if any component of the resolution is not a descendant of the directory indicated by dirfd. | RESOLVE_BENEATH
- Q5 | S138 | glibc provides no wrapper for openat2(), necessitating the use of syscall(2). | RESOLVE_BENEATH
- Q6 | S139 | Block traversal through all symlinks (implies OEXT_NO_MAGICLINKS) | RESOLVE_NO_SYMLINKS
- Q7 | S140 | PROBE P02 os.open-O_NOFOLLOW-symlink-in-earlier-component observed=opened expected=opened ok | P02
- Q8 | S140 | PROBE P04 openat2-NO_SYMLINKS-symlink-in-earlier-component observed=ELOOP expected=ELOOP ok | P04
- Q9 | S140 | PROBE P01 python-os-has-openat2 observed=False expected=False ok | P01

## Claims

Claim 1. RESOLVE_NO_SYMLINKS makes the kernel refuse a symbolic link anywhere along the walk, including magic links, whereas the O_NOFOLLOW creation flag judges just the last name of the path. [Q2, Q3]
Claim 2. On this host the difference is observable: a path through a symlinked directory is opened by os.open with O_NOFOLLOW, and refused with ELOOP by openat2 with RESOLVE_NO_SYMLINKS. [Q7, Q8]
Claim 3. The flags are designed for trusted programs that handle untrusted directories, and RESOLVE_BENEATH rejects any resolution that would leave the directory named by the descriptor. [Q1, Q4]
Claim 4. Calling openat2 from Python 3.14.8 needs ctypes or another route to syscall(2), because glibc has no wrapper and the os module exposes no openat2 function in the probe. [Q5, Q9]
Claim 5. The installed header describes the symlink flag as one that blocks traversal through all symlinks, so a caller should read the numeric flag values from that header instead of typing them from memory. [Q6]

## Limits

- The quotes describe Linux man-pages 6.19 and linux-api-headers 7.2-1; the probe ran once on kernel 7.2.11, x86_64, one local filesystem. Other kernels (openat2 arrived in Linux 5.6), architectures and network filesystems are unprobed.
- [INFERENCE] The span builder's check-then-write window (round-61 entry, Limits) could shrink if each path were opened relative to a directory descriptor with the symlink-blocking and escape-blocking flags together; this entry shows the flags' effect on reads, not a changed builder.
- The probe opens existing files for reading; creating files (O_CREAT) with these flags and the EAGAIN retry the page describes for racing dotdot walks are not exercised.
- The counter that binds this entry checks that quotes exist where the rows say, that every claim cites existing quotes and adds words of its own, and that the probe reruns to the committed output; it does not judge that a claim follows from its quotes.
