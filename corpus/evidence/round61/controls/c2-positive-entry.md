source: S134 (open(2), Linux man-pages 6.19, /usr/share/man/man2/open.2.gz), S135 (rename(2), Linux man-pages 6.19, /usr/share/man/man2/rename.2.gz), S136 (.ufo/waves/round-56/w1/R55W2SentBuilder.md, cases h2 and h3)
verified-at: 2026-10-28 (man pages rendered with MANWIDTH=1000 man -l FILE | col -bx; the S136 file as committed at lane commit 9eef15e)
recheck: on a man-pages release, re-render both pages and run `python3 corpus/evidence/round61/c2-count.py` (exit 0)

# Writing derived evidence under a caller-supplied directory (round 61)

A tool that derives evidence files (spans, manifests) writes into a directory the caller names. What the
operating system does with a symbolic link at that path decides whether a planted link redirects the write.

## Located quotes

- Q1 | S134 | If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP. | O_NOFOLLOW
- Q2 | S134 | Symbolic links in earlier components of the pathname will still be followed. | O_NOFOLLOW
- Q3 | S134 | symbolic links are not followed: if path is a symbolic link, then open() fails regardless of where the symbolic link points. | O_EXCL
- Q4 | S135 | If oldpath refers to a symbolic link, the link is renamed; if newpath refers to a symbolic link, the link will be overwritten. | DESCRIPTION
- Q5 | S135 | it will be atomically replaced, so that there is no point at which another process attempting to access newpath will find it missing. | DESCRIPTION
- Q6 | S135 | However, there will probably be a window in which both oldpath and newpath refer to the file being renamed. | DESCRIPTION
- Q7 | S136 | victim/S404-9.txt(28) before → absent after; victim/S001-1.txt(457) created; exit 0, stderr empty | h2
- Q8 | S136 | victim/IMPORTANT.txt 10→457 B, victim/LEDGER.tsv 74→243 B (both targets truncated); exit 0 | h3

## Claims

Claim 1. O_NOFOLLOW protects only the final path component of an opened file, so a symbolic link in an earlier component, such as a linked output directory, is still followed and the writer must test that directory itself. [Q1, Q2]
Claim 2. Creating a file with O_CREAT and O_EXCL fails on any existing path that is a symbolic link, regardless of where the link points, so a fresh temporary name cannot be written through a planted link. [Q3]
Claim 3. When newpath refers to a symbolic link, a rename overwrites the link instead of following it, so a derived file written by temporary file and rename cannot write through a link planted at its final name. [Q4]
Claim 4. The replacement is atomic for readers of the final name, yet a window exists in which both names refer to the same file, so a failed run can leave the temporary name behind and cleanup belongs on the error path. [Q5, Q6]
Claim 5. In the round-55 fixture runs the builder removed a victim file and created another inside a symlinked victim directory, and truncated two victim files through links, each time exiting 0. [Q7, Q8]

## Limits

- The quotes describe Linux man-pages 6.19 on this host; other systems and versions are not covered.
- [INFERENCE] A check followed by a write is not atomic with it, so a process that swaps a directory for a link between the two is not stopped by the checks; none of the quotes states this.
- The counter that binds this entry checks that each quote is present where its row says and that each claim cites existing quotes; it does not judge that a claim follows from its quotes.
