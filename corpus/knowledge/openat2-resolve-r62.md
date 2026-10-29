source: S138 (openat2(2), Linux man-pages 6.19, page date 2026-07-02, /usr/share/man/man2/openat2.2.gz), S139 (/usr/include/linux/openat2.h, linux-api-headers 7.2-1), S140 (corpus/evidence/round62/openat2-probe.txt, written by corpus/evidence/round62/openat2-probe.py)
verified-at: 2026-10-28 (man page rendered with MANWIDTH=1000 man -l FILE | col -bx on man-pages 6.19-1; header read on linux-api-headers 7.2-1; probe run on kernel 7.2.11-arch1-1, Python 3.14.8, x86_64, an xfs scratch directory)
recheck: on a man-pages, kernel-headers or glibc release run `python3 corpus/evidence/round62/c2v2-count.py` (exit 0) and `python3 corpus/evidence/round62/openat2-probe.py --work <dir>` (exit 0); the glibc note in Limits by `nm -D /usr/lib/libc.so.6 | grep -i openat2`

# Kernel-enforced path resolution with openat2 (round 62)

A tool that opens a path under a directory it does not control can ask the kernel to refuse symbolic links or
escapes during the walk, instead of testing the path first and opening it afterwards. Round 61's entry
(`derived-output-safety-r61.md`) records the check-then-write window that remains when a tool only tests. This
entry records what the openat2 page and header say about the resolve flags, and what this host's kernel and
Python did in a probe. Every claim is bound to located quotes; what the quotes do not say is in `## Limits`.

## Located quotes

- Q1 | S138 | The primary use case for these flags is to allow trusted programs to restrict how untrusted paths (or paths inside untrusted directories) are resolved. | how.resolve
- Q2 | S138 | Disallow resolution of symbolic links during path resolution. This option implies RESOLVE_NO_MAGICLINKS. | RESOLVE_NO_SYMLINKS
- Q3 | S138 | which affects the treatment of symbolic links in all of the components of path | RESOLVE_NO_SYMLINKS
- Q4 | S138 | differs from the effect of the O_NOFOLLOW file creation flag (in how.flags), which affects the handling of symbolic links only in the final component | RESOLVE_NO_SYMLINKS
- Q5 | S138 | ELOOP how.resolve contains RESOLVE_NO_SYMLINKS, and one of the path components was a symbolic link (or magic link). | ELOOP
- Q6 | S138 | If the trailing component (i.e., basename) of path is a symbolic link, how.resolve contains RESOLVE_NO_SYMLINKS, and how.flags contains both O_PATH and O_NOFOLLOW | RESOLVE_NO_SYMLINKS
- Q7 | S138 | an O_PATH file descriptor referencing the symbolic link will be returned | RESOLVE_NO_SYMLINKS
- Q8 | S138 | Do not permit the path resolution to succeed if any component of the resolution is not a descendant of the directory indicated by dirfd. | RESOLVE_BENEATH
- Q9 | S138 | the kernel could not ensure that a ".." component didn't escape (due to a race condition or potential attack) | EAGAIN
- Q10 | S138 | Note: glibc provides no wrapper for openat2(), necessitating the use of syscall(2). | SYNOPSIS
- Q11 | S139 | RESOLVE_NO_SYMLINKS 0x04 /* Block traversal through all symlinks (implies OEXT_NO_MAGICLINKS) */ | RESOLVE_NO_SYMLINKS
- Q12 | S140 | PROBE P02 os.open-O_NOFOLLOW-symlink-in-earlier-component observed=opened expected=opened ok | P02
- Q13 | S140 | PROBE P04 openat2-NO_SYMLINKS-symlink-in-earlier-component observed=ELOOP expected=ELOOP ok | P04
- Q14 | S140 | PROBE P01 python-os-has-openat2 observed=False expected=False ok | P01
- Q15 | S140 | PROBE P07 openat2-BENEATH-dotdot-escape observed=EXDEV expected=EXDEV ok | P07
- Q16 | S140 | PROBE P14 openat2-O_PATH-O_NOFOLLOW-NO_SYMLINKS-final-symlink-fd-is-the-link observed=True expected=True ok | P14

## Claims

Claim 1. With RESOLVE_NO_SYMLINKS the kernel refuses a symbolic link in every component of the path, magic links included, and reports ELOOP, whereas the O_NOFOLLOW creation flag judges only the last component; the one exception the page names is a final-component link opened with O_PATH and O_NOFOLLOW, which yields a descriptor for the link instead of a refusal. [Q2, Q3, Q4, Q5, Q6, Q7]
Claim 2. In the probe case with a symbolic link in an earlier component, os.open with O_NOFOLLOW opened the path on this host, while openat2 with RESOLVE_NO_SYMLINKS refused the same kind of path with ELOOP. [Q12, Q13]
Claim 3. In the probe, a final-component symbolic link opened through openat2 with O_PATH, O_NOFOLLOW and RESOLVE_NO_SYMLINKS returned a descriptor that refers to the link itself, which matches the exception in the page. [Q7, Q16]
Claim 4. The page names restricting how untrusted paths are resolved as the primary use case for these flags, aimed at trusted programs; RESOLVE_BENEATH fails a walk whose component leaves the directory behind the descriptor, the probe's dotdot escape came back as EXDEV, and the page lists EAGAIN for a dotdot the kernel cannot vouch for. [Q1, Q8, Q9, Q15]
Claim 5. The page's SYNOPSIS says glibc provides no wrapper for openat2(), and on this host the Python os module exposes no openat2 function in the probe, so a Python caller needs a foreign-function route: the syscall(2) the page names, or a libc symbol where the installed glibc has one (see Limits). [Q10, Q14]
Claim 6. The installed header documents the symlink flag as one that blocks traversal through all symlinks, with value 0x04, and its comment names OEXT_NO_MAGICLINKS as the implied flag where the page names RESOLVE_NO_MAGICLINKS; a caller takes the flag values from the header and the semantics from the page. [Q2, Q11]

## Limits

- The quotes describe Linux man-pages 6.19 (this page dated 2026-07-02; the page's HISTORY dates the call to Linux 5.6) and linux-api-headers 7.2-1; the probe ran once on kernel 7.2.11-arch1-1, x86_64, in an xfs scratch directory (`df --output=fstype /fast/scratch`). The lane tree is btrfs and was not probed; other kernels, architectures and network filesystems are unprobed.
- The page's SYNOPSIS note is dated against this host. On 2026-10-28 `nm -D /usr/lib/libc.so.6 | grep -i openat2` printed `0000000000112aa0 W openat2@@GLIBC_2.43` and `ldd --version` printed `ldd (GNU libc) 2.44` on its first line, so the installed glibc exports a wrapper although the quoted note says it provides none (found by wave seats CritC2Quotes and RevC2V2Claim4; `.ufo/waves/round-62/w1/`). Claim 5 therefore states the page's note and the Python result only, and leaves the glibc symbol out of its quotes.
- The `expected=` values are typed by the probe's author, and each carries a `# cite` comment in the probe (`python3 -B corpus/evidence/round62/probe-cite-check.py corpus/evidence/round62/openat2-probe.py` printed `CITES=14/14 SOURCED=9 INFERENCE=5`): P01, P03 and P11 have no predicting sentence in S138 or S139 and P06 and P09 are controls, all five author inference, so `PROBE_FACTS=14/14` is agreement with the author. Every claim above rests on `observed=` fields of P01, P02, P04, P07 and P14 only.
- The page advises that RESOLVE_NO_SYMLINKS and RESOLVE_NO_XDEV be made configurable because setting them for every user can produce spurious errors; no claim here recommends setting a flag indiscriminately.
- [INFERENCE] The check-then-write window recorded in the round-61 entry could narrow if each path were opened once relative to a directory descriptor with RESOLVE_NO_SYMLINKS and RESOLVE_BENEATH together; this entry shows the flags' effect on opens of existing files, not a changed tool.
- The probe opens existing files for reading. Creating files with these flags, the EAGAIN retry under a real race, RESOLVE_CACHED, RESOLVE_NO_XDEV and OPENAT2_REGULAR (the page says since Linux 7.2) are not exercised.
- The counter that binds this entry (`corpus/evidence/round62/c2v2-count.py`) checks that the quotes exist where the rows say, that every claim cites existing quotes and adds words of its own, and that the probe reruns to the committed output; it does not judge that a claim follows from its quotes (wave reviewers `RevC2V2Claim1`-`RevC2V2Claim5` did, and all five original claims were rewritten here).
