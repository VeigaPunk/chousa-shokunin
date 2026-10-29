source: S138 (openat2(2), Linux man-pages 6.19, /usr/share/man/man2/openat2.2.gz of man-pages 6.19-1, rendered with MANWIDTH=1000 man -l FILE | col -bx), S139 (/usr/include/linux/openat2.h, linux-api-headers 7.2-1), S140 (corpus/evidence/round62/openat2-probe.txt)
verified-at: 2026-10-28 (man page and header read on this host; probe run on kernel 7.2.11-arch1-1, Python 3.14.8, x86_64)
recheck: on a man-pages or kernel-headers release run `python3 corpus/evidence/round62/c2v2-count.py` (exit 0); the probe alone by `python3 corpus/evidence/round62/openat2-probe.py --work <dir>`

# Kernel-enforced path resolution with openat2 (round 62)

A tool that opens a path under a directory it does not control can ask the kernel to refuse symbolic links or escapes during the walk, instead of testing the path first. The table below maps each hazard to the openat2 flag that enforces it, to what Python's standard library reaches, and to the probe line that shows this host's result. A cell marked (unquoted) is read from the cited source but has no counted quote below.

## Decision table

| Hazard | Kernel enforces (flag, header value) | Python reaches | Probe line (S140) |
|---|---|---|---|
| Symbolic link in an earlier path component | RESOLVE_NO_SYMLINKS (0x04, S139); refused with ELOOP (Q6) | os.open with O_NOFOLLOW follows it; openat2 only through ctypes and syscall(2) (Q5, Q10) | P02 opened; P04 ELOOP |
| Symbolic link as the final component | O_NOFOLLOW judges this one (Q2); RESOLVE_NO_SYMLINKS also refuses it | os.open with O_NOFOLLOW gives ELOOP | P03 ELOOP; P05 ELOOP |
| Escape from dirfd by `..` or an absolute symlink | RESOLVE_BENEATH (0x08, S139): EXDEV (Q4, Q7) | os.open with dir_fd has no such check; the absolute link is read from outside | P07 EXDEV; P08 EXDEV; P11 outside |
| Relative symlink that stays inside dirfd | RESOLVE_BENEATH let it through in P09 (probe only); the S139 comment (unquoted) ties symlink blocking to escapes | not applicable | P09 opened |
| Absolute symlink that should resolve inside the tree | RESOLVE_IN_ROOT (0x10): resolved relative to dirfd (unquoted, S138 text) | os.open reads outside | P10 rootfile; P11 outside |
| Unknown bit in how.resolve | error, not ignored (Q8) | ctypes passes the bit to the kernel (P12 used bit 14) | P12 EINVAL |
| Magic links such as /proc/PID/fd/* | RESOLVE_NO_MAGICLINKS (0x02, S139); RESOLVE_NO_SYMLINKS implies it (Q9) | not probed | not probed |
| Mount-point crossing | RESOLVE_NO_XDEV (0x01, S139 comment; unquoted) | not probed | not probed |
| mode set without O_CREAT | the header comment says mode must be zero unless O_CREAT or O_TMPFILE is set (S139; unquoted) | not applicable | P13 EINVAL |
| Final symlink opened with O_PATH and O_NOFOLLOW under RESOLVE_NO_SYMLINKS | returns a descriptor for the link itself (S138, unquoted) | ctypes | P14 True |
| Lookup limited to cached entries | RESOLVE_CACHED (0x20); the S139 comment (unquoted) says it may return -EAGAIN | not probed | not probed |

## Located quotes

- Q1 | S138 | Disallow resolution of symbolic links during path resolution. | RESOLVE_NO_SYMLINKS
- Q2 | S138 | which affects the handling of symbolic links only in the final component of path | RESOLVE_NO_SYMLINKS
- Q3 | S138 | the effect of the RESOLVE_NO_SYMLINKS flag, which affects the treatment of symbolic links in all of the components of path | RESOLVE_NO_SYMLINKS
- Q4 | S138 | Do not permit the path resolution to succeed if any component of the resolution is not a descendant of the directory indicated by dirfd. | RESOLVE_BENEATH
- Q5 | S138 | glibc provides no wrapper for openat2(), necessitating the use of syscall(2). | SYNOPSIS
- Q6 | S138 | ELOOP how.resolve contains RESOLVE_NO_SYMLINKS, and one of the path components was a symbolic link (or magic link). | how.resolve
- Q7 | S138 | EXDEV how.resolve contains either RESOLVE_IN_ROOT or RESOLVE_BENEATH, and an escape from the root during path resolution was detected. | how.resolve
- Q8 | S138 | If any bits other than those listed above are set in how.resolve, an error is returned. | how.resolve
- Q9 | S139 | RESOLVE_NO_SYMLINKS 0x04 /* Block traversal through all symlinks (implies OEXT_NO_MAGICLINKS) */ | RESOLVE_NO_SYMLINKS
- Q10 | S140 | PROBE P01 python-os-has-openat2 observed=False expected=False ok | P01
- Q11 | S140 | PROBE P02 os.open-O_NOFOLLOW-symlink-in-earlier-component observed=opened expected=opened ok | P02
- Q12 | S140 | PROBE P04 openat2-NO_SYMLINKS-symlink-in-earlier-component observed=ELOOP expected=ELOOP ok | P04

## Claims

Claim 1. RESOLVE_NO_SYMLINKS disallows symbolic links during path resolution in every component of the path, while the O_NOFOLLOW creation flag affects symbolic links only in the final component. [Q1, Q2, Q3]
Claim 2. On this host os.open with O_NOFOLLOW opens a file through a symbolic link in an earlier component, while openat2 with RESOLVE_NO_SYMLINKS refuses the same path with ELOOP. [Q6, Q11, Q12]
Claim 3. RESOLVE_BENEATH refuses a resolution that leaves the directory named by the descriptor, and reports EXDEV for it. [Q4, Q7]
Claim 4. On this host the os module has no openat2 function, so a caller reaches openat2 through syscall(2), since glibc provides no wrapper; the probe script calls it through ctypes [INFERENCE: the ctypes route is the probe's own method, not quoted]. [Q5, Q10]
Claim 5. The installed header describes RESOLVE_NO_SYMLINKS as blocking traversal through all symlinks, and its comment names OEXT_NO_MAGICLINKS, a macro the header does not define [INFERENCE: read as a misspelling of RESOLVE_NO_MAGICLINKS]. [Q9]
Claim 6. An unknown bit in how.resolve is an error rather than being ignored, as the page states. [Q8]

## Limits

- The quotes describe Linux man-pages 6.19 and linux-api-headers 7.2-1 on this host. The probe ran once on kernel 7.2.11-arch1-1, Python 3.14.8, x86_64, one local filesystem; other kernels, architectures and network filesystems are unprobed. The man page's HISTORY section gives Linux 5.6 for openat2 (unquoted, S138).
- [INFERENCE] The round-61 entry derived-output-safety-r61.md (its line 9) describes whether a check made before the write still holds when the write happens. These flags could narrow that window if a path were opened relative to a directory descriptor; this entry shows their effect on reads only, and no builder changes here.
- The probe opens existing files for reading. RESOLVE_NO_XDEV, RESOLVE_NO_MAGICLINKS, RESOLVE_CACHED, the EAGAIN retry for racing dot-dot walks and O_CREAT with openat2 are not exercised; the table marks them not probed.
- The S139 row's anchor names only RESOLVE_NO_SYMLINKS, so the other header values (0x01, 0x02, 0x08, 0x10, 0x20) appear in the table without counted quotes.
- The header comment on RESOLVE_BENEATH (S139, unquoted) lists symlinks alongside escapes. Probe P09 opens a relative symlink that stays inside, so the table does not read BENEATH as a symlink ban.
- The header names OEXT_NO_MAGICLINKS (Q9), a macro the header does not define (one occurrence, in that comment); the table uses RESOLVE_NO_MAGICLINKS instead.
- Entailment is not machine-checked: the counter checks that quotes exist where the rows say and that no claim only repeats its quote; reviewers judge whether each claim follows from its quotes.
