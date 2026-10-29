source: S138 (openat2(2), Linux man-pages 6.19, /usr/share/man/man2/openat2.2.gz), S139 (/usr/include/linux/openat2.h, linux-api-headers 7.2-1), S140 (corpus/evidence/round62/openat2-probe.txt, own-work)
verified-at: 2026-10-28 (S138 rendered with MANWIDTH=1000 man -l FILE | col -bx on man-pages 6.19-1; S139 read from the installed header; S140 read from the probe output on kernel 7.2.11-arch1-1, Python 3.14.8)
recheck: on a man-pages or linux-api-headers update run python3 -B corpus/evidence/round62/c2v2-count.py (exit 0); the probe alone by python3 -B corpus/evidence/round62/openat2-probe.py --work <absent dir>

# Kernel-enforced path resolution with openat2 (round 62)

A tool that opens a path under a directory it does not control can ask the kernel to refuse symbolic links
or escapes during the walk. This entry records three things the sources say about the openat2 resolve flags:
what they check, what they are for, and how a caller reaches them. Section S140 is what this host's kernel
and Python did in one probe run.

## Located quotes

- Q1 | S138 | The primary use case for these flags is to allow trusted programs to restrict how untrusted paths (or paths inside untrusted directories) are resolved. | RESOLVE_NO_SYMLINKS
- Q2 | S138 | Disallow resolution of symbolic links during path resolution. This option implies RESOLVE_NO_MAGICLINKS. | RESOLVE_NO_SYMLINKS
- Q3 | S138 | which affects the treatment of symbolic links in all of the components of path | RESOLVE_NO_SYMLINKS
- Q4 | S138 | which affects the handling of symbolic links only in the final component of path | RESOLVE_NO_SYMLINKS
- Q5 | S138 | Do not permit the path resolution to succeed if any component of the resolution is not a descendant of the directory indicated by dirfd. | RESOLVE_BENEATH
- Q6 | S138 | ELOOP how.resolve contains RESOLVE_NO_SYMLINKS, and one of the path components was a symbolic link (or magic link). | RESOLVE_NO_SYMLINKS
- Q7 | S138 | glibc provides no wrapper for openat2(), necessitating the use of syscall(2). | SYNOPSIS
- Q8 | S139 | #define RESOLVE_NO_SYMLINKS 0x04 /* Block traversal through all symlinks (implies OEXT_NO_MAGICLINKS) */ | RESOLVE_NO_SYMLINKS
- Q9 | S140 | PROBE P02 os.open-O_NOFOLLOW-symlink-in-earlier-component observed=opened expected=opened ok | P02
- Q10 | S140 | PROBE P04 openat2-NO_SYMLINKS-symlink-in-earlier-component observed=ELOOP expected=ELOOP ok | P04
- Q11 | S140 | PROBE P01 python-os-has-openat2 observed=False expected=False ok | P01

## Claims

### Principle 1: RESOLVE_NO_SYMLINKS checks every component; O_NOFOLLOW checks the last one

Claim 1. RESOLVE_NO_SYMLINKS affects the treatment of symbolic links in every component of the path, whereas O_NOFOLLOW affects their handling only in the final component. [Q3, Q4]
Claim 2. A symbolic link in any path component makes the call return ELOOP under RESOLVE_NO_SYMLINKS, and the flag implies RESOLVE_NO_MAGICLINKS. [Q2, Q6]
Claim 3. On this host the difference shows: os.open with O_NOFOLLOW opened a path whose earlier component is a symbolic link, and openat2 with RESOLVE_NO_SYMLINKS refused that path with ELOOP. [Q9, Q10]

### Principle 2: the flags serve trusted programs that restrict untrusted paths

Claim 4. The openat2 page says these flags serve trusted programs that restrict how untrusted paths are resolved, and RESOLVE_BENEATH refuses any walk that leaves the directory given as dirfd. [Q1, Q5]

### Principle 3: a caller reaches the call through syscall(2) and reads flag values from the header

Claim 5. glibc has no openat2 wrapper, and the probe found no os.openat2 function on this host, so a caller reaches the call through syscall(2). [Q7, Q11]
Claim 6. The installed header describes RESOLVE_NO_SYMLINKS, value 0x04, as blocking traversal through all symlinks. [Q8]

## Limits

- The quotes describe Linux man-pages 6.19 (the rendered page footer reads 2026-07-02, while registry row S138 gives 2026-02-08) and linux-api-headers 7.2-1 on this host; the probe ran once on kernel 7.2.11-arch1-1, Python 3.14.8, x86_64, one local filesystem. Other kernels, architectures and network filesystems are unprobed.
- The probe opens existing files for reading only. Creating files with O_CREAT under these flags, and the EAGAIN retry the page describes for racing ".." walks, are not exercised.
- The header comment in Q8 names OEXT_NO_MAGICLINKS, a macro this header does not define; the defined flag is RESOLVE_NO_MAGICLINKS. This entry quotes the comment and does not rely on the misnamed macro.
- [INFERENCE] These flags might let a path-opening tool replace a check-then-write window with a kernel refusal; this entry shows their effect on reads only and changes no builder.
- Whether each claim follows from its quotes is judged by reviewers; the counter checks only that quotes exist, that references resolve, and that the probe reruns.
