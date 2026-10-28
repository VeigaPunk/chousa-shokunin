source: S134 (open(2), Linux man-pages 6.19, /usr/share/man/man2/open.2.gz), S135 (rename(2), Linux man-pages 6.19, /usr/share/man/man2/rename.2.gz), S136 (.ufo/waves/round-56/w1/R55W2SentBuilder.md, cases h2 and h3)
verified-at: 2026-10-28 (S134 and S135 rendered with MANWIDTH=1000 man -l FILE | col -bx from man-pages 6.19-1; S136 read as committed at lane commit 9eef15e and byte-identical to the working copy)
recheck: on a man-pages update, re-render S134 and S135 and run python3 corpus/evidence/round61/c2-count.py (exit 0); on any change to the S136 file, re-read cases h2 and h3 before relying on Q7 to Q11

# Writing derived files into a caller-named directory

A tool that writes derived files (span files, manifests, indexes) into a directory the caller names has to
handle symbolic links at the output path. The steps run in order. Each step cites the located quotes it rests
on; anything beyond those quotes is marked [INFERENCE].

## Checklist

1. Walk the caller's output path component by component and refuse any symbolic link found in it. O_NOFOLLOW on the final open covers only the last component; symbolic links in earlier components are still followed (Q1, Q2). [INFERENCE] One lstat per component is a design choice the quotes do not prescribe.
2. Inspect what is already in the output directory before changing it. The round-55 builder did not inspect it (Q11).
3. Create every new file with O_CREAT and O_EXCL. When both flags are given, a symbolic link at the path is not followed: open() fails whatever the link points to (Q3).
4. Write derived bytes to a fresh temporary name made the same way as step 3, then rename it onto the final name. rename(2) overwrites a symbolic link at newpath rather than following it (Q4). The replacement is atomic for a reader of the final name (Q5), but both names can refer to the same file for a while (Q6). [INFERENCE] On the error path, remove the temporary name, because a failed run can leave it behind.
5. Write the index or manifest last, after the files it lists. [INFERENCE] A failed run then leaves no index that names files that are missing.
6. Judge the run by the resulting tree, not by the exit status. Two round-55 fixture cases exited 0 while victim files were removed or created (Q7) and truncated (Q8); the case table records the symlinks involved (Q9, Q10). [INFERENCE] Test the tool with a fixture that holds a link at each output component, and compare the tree before and after the run.

## Located quotes

- Q1 | S134 | If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP. | O_NOFOLLOW
- Q2 | S134 | Symbolic links in earlier components of the pathname will still be followed. | O_NOFOLLOW
- Q3 | S134 | symbolic links are not followed: if path is a symbolic link, then open() fails regardless of where the symbolic link points. | O_EXCL
- Q4 | S135 | If oldpath refers to a symbolic link, the link is renamed; if newpath refers to a symbolic link, the link will be overwritten. | DESCRIPTION
- Q5 | S135 | it will be atomically replaced, so that there is no point at which another process attempting to access newpath will find it missing. | DESCRIPTION
- Q6 | S135 | However, there will probably be a window in which both oldpath and newpath refer to the file being renamed. | DESCRIPTION
- Q7 | S136 | victim/S404-9.txt(28) before → absent after; victim/S001-1.txt(457) created; exit 0, stderr empty | h2
- Q8 | S136 | victim/IMPORTANT.txt 10→457 B, victim/LEDGER.tsv 74→243 B (both targets truncated); exit 0 | h3
- Q9 | S136 | `out/spans` symlink → dir | h2
- Q10 | S136 | span file and `spans.tsv` are symlinks | h3
- Q11 | S136 | Nothing inspects what was already there. | section 1

## Claims

Claim 1. O_NOFOLLOW refuses only a symbolic link at the last component of a path; symbolic links in earlier components are still followed. [Q1, Q2]

Claim 2. With both O_CREAT and O_EXCL given, open() does not follow a symbolic link: it fails when the path is one, regardless of where the link points, so a new file created this way cannot be written through a link planted at its name. [Q3]

Claim 3. When newpath refers to a symbolic link, rename(2) overwrites that link rather than following it, so a derived file moved into place by rename cannot be written through a link planted at its final name. [Q4]

Claim 4. The replacement is atomic in that no process accessing the final name finds it missing, yet there is a window in which both names refer to the file being renamed. [Q5, Q6]

Claim 5. In case h2 the spans directory under the output was a symlink, and the builder removed one victim file and created another; in case h3 a span file and spans.tsv were symlinks and both link targets were truncated; each run exited 0. [Q7, Q8, Q9, Q10]

Claim 6. The round-55 builder inspects nothing already present in its output directory before it changes that directory, so content already there is changed without any check. [Q11]

## Limits

- The quotes cover Linux man-pages 6.19 (Arch package man-pages 6.19-1) on this host; no quote covers other systems, kernels or filesystems.
- S136 is one seat's report of fixture runs at revision 29cfb12 (file sha256 prefix 1ed2650a); it is not a gate output that re-runs from this entry.
- [INFERENCE] A check followed by a write is not atomic with it; a process that swaps a directory for a link between the two is not stopped by the checks, and no quote states this.
- The counter that binds this entry checks that each quote is present where its row says and that each claim cites existing quotes; it does not judge whether a claim follows from its quotes.
