source: S134 (open(2), Linux man-pages 6.19, /usr/share/man/man2/open.2.gz), S135 (rename(2), Linux man-pages 6.19, /usr/share/man/man2/rename.2.gz), S136 (.ufo/waves/round-56/w1/R55W2SentBuilder.md, cases h2 and h3)
verified-at: 2026-10-28 (man pages rendered with MANWIDTH=1000 man -l FILE | col -bx; the S136 file as committed at lane commit 9eef15e)
recheck: on a man-pages release, re-render both pages and run `python3 corpus/evidence/round61/c2-count.py` (exit 0)

# Writing derived evidence under a caller-supplied directory (round 61)

A tool that derives evidence files (spans, manifests) writes into a directory the caller names. What the operating system does with a symbolic link at a path decides whether a planted link redirects the write.

## Located quotes

- Q1 | S134 | If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP. | O_NOFOLLOW
- Q2 | S134 | Symbolic links in earlier components of the pathname will still be followed. | O_NOFOLLOW
- Q3 | S134 | symbolic links are not followed: if path is a symbolic link, then open() fails regardless of where the symbolic link points. | O_EXCL
- Q4 | S135 | If oldpath refers to a symbolic link, the link is renamed; if newpath refers to a symbolic link, the link will be overwritten. | DESCRIPTION
- Q5 | S135 | it will be atomically replaced, so that there is no point at which another process attempting to access newpath will find it missing. | DESCRIPTION
- Q6 | S136 | victim/S404-9.txt(28) before → absent after; victim/S001-1.txt(457) created; exit 0, stderr empty | h2
- Q7 | S136 | victim/IMPORTANT.txt 10→457 B, victim/LEDGER.tsv 74→243 B (both targets truncated); exit 0 | h3

## Claims

Claim 1. O_NOFOLLOW checks only the trailing component of a path, so a symbolic link in an earlier component, such as a linked output directory, is still followed; a writer has to check the output directory itself [INFERENCE: the page states the trailing-component rule, not this consequence]. [Q1, Q2]
Claim 2. With O_CREAT and O_EXCL, open fails on any path that is a symbolic link, regardless of where the link points, so a link planted at a fresh temporary name before the create cannot be written through. [Q3]
Claim 3. A rename does not follow a symbolic link at newpath; it overwrites the link, and it replaces the final name in one atomic step, so no other process finds newpath missing. A derived file written to a temporary name and renamed into place therefore cannot be written through a link planted at its final name. [Q4, Q5]
Claim 4. In fixture runs at revision 29cfb12 the round-55 builder removed a victim file and created another in a directory reached through a symlinked spans/, and truncated two victim files through links, each time exiting 0. [Q6, Q7]

## Limits

- Linux man-pages 6.19 on this host, read from the installed pages under /usr/share/man; other systems, kernels and man-pages versions are not covered, and the man7.org HTML was not opened.
- Claim 4 is one seat's fixture runs (S136, tier B) at revision 29cfb12, not a re-run of the current builder.
- [INFERENCE] A path check followed by a write is not atomic with it, so a process that swaps a directory for a link between the two is not stopped by the check; none of the quoted text states this.
- The entry does not cover O_TMPFILE, which the same page documents, nor cleanup of a temporary name left by a failed run; the window in rename(2) is not quoted.
- The counter is structural: it checks that each quote and anchor is present and that each claim cites existing quotes; it does not judge that a claim follows from its quotes.
