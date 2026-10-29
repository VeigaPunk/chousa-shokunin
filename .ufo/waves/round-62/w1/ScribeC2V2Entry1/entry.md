source: S138 (openat2(2), Linux man-pages 6.19, /usr/share/man/man2/openat2.2.gz), S139 (/usr/include/linux/openat2.h, linux-api-headers 7.2-1), S140 (corpus/evidence/round62/openat2-probe.txt)
verified-at: 2026-10-28 (man page rendered with MANWIDTH=1000 man -l FILE | col -bx on man-pages 6.19-1; header read on linux-api-headers 7.2-1; probe output from kernel 7.2.11-arch1-1, Python 3.14.8)
recheck: on a man-pages or kernel-headers release run `python3 corpus/evidence/round62/c2v2-count.py` (exit 0); the probe alone by `python3 corpus/evidence/round62/openat2-probe.py --work <dir>`

# Opening paths under an untrusted directory with openat2 (round 62)

A checklist for a tool author who opens paths under a directory the tool does not control. The steps are
the order the sources below support; the quotes say what the kernel and the header do, the claims say what a
tool does about it, and the limits say what was not observed.

## Located quotes

- Q1 | S138 | The primary use case for these flags is to allow trusted programs to restrict how untrusted paths (or paths inside untrusted directories) are resolved. | how.resolve
- Q2 | S138 | Disallow resolution of symbolic links during path resolution. This option implies RESOLVE_NO_MAGICLINKS. | RESOLVE_NO_SYMLINKS
- Q3 | S138 | Note that the effect of the RESOLVE_NO_SYMLINKS flag, which affects the treatment of symbolic links in all of the components of path, | RESOLVE_NO_SYMLINKS
- Q4 | S138 | which affects the handling of symbolic links only in the final component of path | RESOLVE_NO_SYMLINKS
- Q5 | S138 | Do not permit the path resolution to succeed if any component of the resolution is not a descendant of the directory indicated by dirfd. | RESOLVE_BENEATH
- Q6 | S138 | Note: glibc provides no wrapper for openat2(), necessitating the use of syscall(2). | glibc
- Q7 | S138 | ELOOP how.resolve contains RESOLVE_NO_SYMLINKS, and one of the path components was a symbolic link (or magic link). | RESOLVE_NO_SYMLINKS
- Q8 | S138 | EXDEV how.resolve contains either RESOLVE_IN_ROOT or RESOLVE_BENEATH, and an escape from the root during path resolution was detected. | RESOLVE_BENEATH
- Q9 | S138 | The caller may choose to retry the openat2() call. | RESOLVE_BENEATH
- Q10 | S139 | RESOLVE_NO_SYMLINKS 0x04 /* Block traversal through all symlinks | RESOLVE_NO_SYMLINKS
- Q11 | S140 | PROBE P02 os.open-O_NOFOLLOW-symlink-in-earlier-component observed=opened expected=opened ok | P02
- Q12 | S140 | PROBE P04 openat2-NO_SYMLINKS-symlink-in-earlier-component observed=ELOOP expected=ELOOP ok | P04
- Q13 | S140 | PROBE P01 python-os-has-openat2 observed=False expected=False ok | P01

## Claims

Claim 1. Name the directory you trust and open it first, because openat2 resolves a path against the directory descriptor dirfd; the page says the flags exist for trusted programs that restrict how untrusted paths are resolved. [Q1, Q5]
Claim 2. Call the kernel directly, since Python's os module has no openat2 function and glibc has no wrapper, so the call goes through syscall(2). [Q6, Q13]
Claim 3. Take the flag values from the installed header rather than from memory: the header gives RESOLVE_NO_SYMLINKS the value 0x04 and comments that it blocks traversal through all symlinks. [Q10]
Claim 4. Prefer RESOLVE_NO_SYMLINKS to O_NOFOLLOW when a symbolic link in an earlier component matters: O_NOFOLLOW judges only the final component, while RESOLVE_NO_SYMLINKS applies to every component, and the probe shows os.open following a symlinked directory that openat2 refuses with ELOOP. [Q3, Q4, Q11, Q12]
Claim 5. Add RESOLVE_BENEATH when resolution must stay under the descriptor, because it refuses any resolution that leaves the directory indicated by dirfd, and the call fails with EXDEV when an escape is detected. [Q5, Q8]
Claim 6. Handle both refusals as stop signals in the caller's own code: a symbolic link met in a path component under RESOLVE_NO_SYMLINKS produces the failure, an escape detected under RESOLVE_IN_ROOT or RESOLVE_BENEATH produces EXDEV, and a retry of the call stays the caller's choice. [Q7, Q8, Q9]
Claim 7. Expect RESOLVE_NO_SYMLINKS to cover magic links as well, since the page says it implies RESOLVE_NO_MAGICLINKS, so a caller that sets it gets the magic-link refusal too. [Q2]
Claim 8. Check the target host before trusting the result: on this kernel the probe reproduces the page's ELOOP for a symlink under RESOLVE_NO_SYMLINKS, so the observation holds for this host only. [Q7, Q12]

## Limits

- The quotes describe Linux man-pages 6.19, whose HISTORY section dates the call to Linux 5.6, and linux-api-headers 7.2-1 on this host; the probe ran once on kernel 7.2.11, Python 3.14.8, x86_64, one local filesystem. Other kernels, architectures and network filesystems are unprobed.
- The header's RESOLVE_NO_SYMLINKS comment names OEXT_NO_MAGICLINKS, a macro the header does not define: `grep -n OEXT /usr/include/linux/openat2.h` matches only line 38, and RESOLVE_NO_MAGICLINKS is defined on line 35. This entry takes the magic-link name from the man page (Q2), not from the header comment.
- The probe opens existing files for reading only. Creating files with O_CREAT under these flags, the EAGAIN retry under a race, RESOLVE_CACHED, and RESOLVE_IN_ROOT beyond one absolute symlink read (P10) are not exercised.
- [INFERENCE] The check-then-write window recorded in the round-61 entry could narrow if each path were opened once relative to a directory descriptor with RESOLVE_NO_SYMLINKS and RESOLVE_BENEATH together; this entry shows the flags' effect on opens of existing files, not a changed tool.
- [INFERENCE] The order of the claims is one practitioner's sequence drawn from these quotes; the man page does not prescribe it.
- The counter checks that the quotes exist where the rows say and that the probe reruns; it does not judge that a claim follows from its quotes.
