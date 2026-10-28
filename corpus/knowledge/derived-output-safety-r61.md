source: S134 (open(2), Linux man-pages 6.19, /usr/share/man/man2/open.2.gz), S135 (rename(2), Linux man-pages 6.19, /usr/share/man/man2/rename.2.gz), S136 (.ufo/waves/round-56/w1/R55W2SentBuilder.md, cases h2 and h3)
verified-at: 2026-10-28 (man pages rendered with MANWIDTH=1000 man -l FILE | col -bx on package man-pages 6.19-1; the S136 file as committed at lane commit 9eef15e7c0e0ae0055228e7066dc1eec676a91d2; builder cited at lane commit 2edacafa0df371866fc578180872e0fcba5eb4b0)
recheck: on a man-pages release, re-render both pages and run `python3 corpus/evidence/round61/c2-count.py` (exit 0); the builder claims by `python3 corpus/evidence/round61/c1-count.py --builder tools/build-spans.py --work <dir>` and `python3 corpus/evidence/round61/extras.py --builder tools/build-spans.py --work <dir>`

# Writing derived evidence under a caller-supplied directory (round 61)

A tool that derives evidence files (spans, manifests) writes into a directory the caller names. What the
operating system does with a symbolic link at that path decides whether a planted link redirects the write, and
whether a check made before the write still holds when the write happens. This entry records what the Linux
manual pages say about three calls, and what the lane's own builder did before it was hardened (round 61).
Every claim below is bound to a located quote; what the quotes do not say is in `## Limits`, marked.

## Located quotes

- Q1 | S134 | If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP. | O_NOFOLLOW
- Q2 | S134 | Symbolic links in earlier components of the pathname will still be followed. | O_NOFOLLOW
- Q3 | S134 | symbolic links are not followed: if path is a symbolic link, then open() fails regardless of where the symbolic link points. | O_EXCL
- Q4 | S135 | If oldpath refers to a symbolic link, the link is renamed; if newpath refers to a symbolic link, the link will be overwritten. | DESCRIPTION
- Q5 | S135 | it will be atomically replaced, so that there is no point at which another process attempting to access newpath will find it missing. | DESCRIPTION
- Q6 | S135 | However, there will probably be a window in which both oldpath and newpath refer to the file being renamed. | DESCRIPTION
- Q7 | S134 | dir1 or dir2 (which might be symbolic links) could be modified to point to a different location. | Rationale for openat()
- Q8 | S134 | Such races can be avoided by opening a file descriptor for the target directory | Rationale for openat()
- Q9 | S136 | victim/S404-9.txt(28) before → absent after; victim/S001-1.txt(457) created; exit 0, stderr empty | h2
- Q10 | S136 | victim/IMPORTANT.txt 10→457 B, victim/LEDGER.tsv 74→243 B (both targets truncated); exit 0 | h3

## Claims

Claim 1. O_NOFOLLOW checks only the trailing component of the path: a symbolic link in an earlier component is still followed. [Q1, Q2]
Claim 2. On Linux (man-pages 6.19), creating a file with O_CREAT and O_EXCL fails when the path is a symbolic link, regardless of where the link points; symbolic links in earlier components are not covered by this flag, and Claim 1 applies to them. [Q3]
Claim 3. When newpath refers to a symbolic link, rename overwrites the link instead of following it, so a derived file written by temporary file and rename replaces a link planted at its final name rather than writing through it. [Q4]
Claim 4. When newpath already exists, rename replaces it atomically, so no other process finds newpath missing, and the page says there will probably be a window in which both oldpath and newpath refer to the file being renamed. [Q5, Q6]
Claim 5. The page's rationale for openat() says a directory in the path prefix, which might be a symbolic link, can be modified between a check and the creation, and that such races can be avoided by opening a file descriptor for the target directory. [Q7, Q8]
Claim 6. In the round-55 fixture runs the builder exited 0 in both cases where a symbolic link redirected its writes: with out/spans a symbolic link to a victim directory it removed one victim file and created another in the link target (case h2), and with the span file and spans.tsv symbolic links it overwrote both link targets, victim/IMPORTANT.txt 10→457 B and victim/LEDGER.tsv 74→243 B (case h3). [Q9, Q10]

## Application (not sourced by the quotes)

The lane's span builder, `tools/build-spans.py`, was hardened in round 61 along these lines: it opens `--out` and `--out/spans` once as directory descriptors with `O_NOFOLLOW` and does every test, temporary-file create (`O_CREAT|O_EXCL|O_NOFOLLOW`), `os.replace` and unlink relative to those descriptors; it refuses a symlinked output directory, spans directory or manifest and a non-regular span entry; it writes span files first and the manifest last. Its behaviour is shown by `corpus/evidence/round61/c1-count.py` (20 legs; base 7/20, landed 20/20 at three fresh seeds, `corpus/evidence/round61/c1-measure-after.txt`) and `corpus/evidence/round61/extras.py` (16 legs including three swap-in-the-window cases; reference builder 0/16, landed 16/16). The docstring paragraph is not evidence of that (registry row S137, rejected).

## Limits

- The quotes describe Linux man-pages 6.19 on this host; other systems and versions are not covered. Q1 holds without O_PATH: the same page says that with O_PATH and O_NOFOLLOW the call returns a descriptor referring to the link. Q3 applies when both O_CREAT and O_EXCL are given, and only to the final component.
- [INFERENCE] Using O_CREAT and O_EXCL at a fresh temporary name is the writer's design, not text in the quotes.
- [INFERENCE] A failed rename does not move the file, so a temporary name may remain after a failed run and cleanup belongs on the error path; the page does not state this (its BUGS text on NFS says one cannot assume that a failed rename left the file unrenamed).
- Claim 6 reports a lane seat's own fixture runs (S136) at blob 29cfb12, not repeated in round 61; the seat's transcript calls both link targets "truncated" although both grew (10→457 B, 74→243 B), so the claim says overwrote.
- The counter that binds this entry checks that each quote is present where its row says and that each claim cites existing quotes; it does not judge that a claim follows from its quotes (wave w1 reviewers RevC2Claim1-5 did, and four of the five original claims were rewritten: `.ufo/waves/round-61/w1/RevC2Claim1.md`, `RevC2Claim2.md`, `RevC2Claim4.md`, `RevC2Claim5.md`).
