source: S134 (open(2), Linux man-pages 6.19, /usr/share/man/man2/open.2.gz), S135 (rename(2), Linux man-pages 6.19, /usr/share/man/man2/rename.2.gz), S136 (.ufo/waves/round-56/w1/R55W2SentBuilder.md, cases h2 and h3)
verified-at: 2026-10-28 (man pages rendered with MANWIDTH=1000 man -l FILE then col -bx; S136 read as the file at lane commit 9eef15e)
recheck: on a man-pages release, re-render both pages and run `python3 corpus/evidence/round61/c2-count.py` (exit 0)

# Derived-output safety: what Linux does with links at an output path

A tool that writes derived files (span files, manifests) into a caller-named directory meets the
hazards below. The Linux behaviour in the first two columns is quoted from the sources in the
Located quotes section; the last two columns say what the writer must test and which C1 leg of the
frozen builder counter (corpus/evidence/round61/c1-count.py) exercises the hazard. Text marked
[INFERENCE] is a design derivation, not a quote.

## Decision table

| Hazard | What Linux does | What the tool must test | C1 leg | Sourced by |
|---|---|---|---|---|
| The final span file or spans.tsv is a symbolic link to a file outside the output | open with O_NOFOLLOW fails with ELOOP when the trailing component is a link (Q1); open with O_CREAT and O_EXCL fails on any link at the path, whatever it points to (Q3) | refuse a link at each derived file path, or create only fresh names with O_EXCL; the victim bytes must be unchanged afterwards | H11 FILELINK, H12 TSVLINK | S134 |
| The spans directory is a symbolic link to a victim directory | O_NOFOLLOW does not cover earlier path components: a link there is still followed (Q2) | test the derived directory itself, not only the file, before writing; in case h2 the builder unlinked and created files inside the link target (Q7, Q8) | H10 SPANSLINK | S134, S136 |
| A derived file is written to a temporary name and renamed onto the final name | rename overwrites a link at newpath (Q4); the replacement is atomic for a reader of the final name (Q5); a window exists in which both names refer to the same file (Q6) | create the temporary name with O_EXCL inside the directory that was checked, then rename it into place; [INFERENCE] remove the temporary name on the error path, since the window in Q6 is where a failed run can leave both names | none isolates the temporary name; P01 and P06 compare the whole success-path tree byte for byte | S134, S135 |
| A span file that the run does not write, or a foreign spans.tsv, is already in the output directory | nothing in the quoted sources; case h2 shows an existing span-named file removed from the link target (Q8) | refuse the directory unless the caller asks for replacement; leave it unchanged on refusal [INFERENCE: design choice, not a Linux behaviour] | H07 FOREIGN, H08 REPLACE, H09 ORPHAN | S136 (Q8, partly) |
| A cache .txt is a symbolic link to a file outside the cache | not covered by S134 to S136 | reject non-regular cache entries; the entry claims nothing about this case | H13 OUTSIDE | none (leg only) |
| Very large .txt or OLE-magic .raw inputs | not covered by S134 to S136 | bounded reads and a refusal before the write; the entry claims nothing about memory | H14 BIGTXT, H15 BIGRAW, H20 BIGFORM | none (leg only) |
| Output path is a file, input is unreadable, input is a FIFO, a row names a dot path | not covered by S134 to S136 | exit with a usage or environment code, no traceback, nothing written | H16 OUTFILE, H17 UNREADABLE, H18 FIFO, H19 ENTRYDOT | none (leg only) |
| A check followed later by a write | not covered by the quotes | [INFERENCE] a directory swapped for a link between the check and the write is not stopped by the check; see Limits | none | none |

## Located quotes

- Q1 | S134 | If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP. | O_NOFOLLOW
- Q2 | S134 | Symbolic links in earlier components of the pathname will still be followed. | O_NOFOLLOW
- Q3 | S134 | symbolic links are not followed: if path is a symbolic link, then open() fails regardless of where the symbolic link points. | O_EXCL
- Q4 | S135 | If oldpath refers to a symbolic link, the link is renamed; if newpath refers to a symbolic link, the link will be overwritten. | DESCRIPTION
- Q5 | S135 | it will be atomically replaced, so that there is no point at which another process attempting to access newpath will find it missing. | DESCRIPTION
- Q6 | S135 | However, there will probably be a window in which both oldpath and newpath refer to the file being renamed. | DESCRIPTION
- Q7 | S136 | `out/spans` symlink → dir | h2
- Q8 | S136 | victim/S404-9.txt(28) before → absent after; victim/S001-1.txt(457) created; exit 0, stderr empty | h2
- Q9 | S136 | span file and `spans.tsv` are symlinks | h3
- Q10 | S136 | victim/IMPORTANT.txt 10→457 B, victim/LEDGER.tsv 74→243 B (both targets truncated); exit 0 | h3

## Claims

Claim 1. An O_NOFOLLOW open fails on a symbolic link only when that link is the trailing component of the path; symbolic links in earlier components are still followed. [Q1, Q2]
Claim 2. An open with O_CREAT and O_EXCL fails when the path is a symbolic link, regardless of where the link points. [Q3]
Claim 3. When newpath refers to a symbolic link, rename overwrites the link itself, because the man page says the link will be overwritten. [Q4]
Claim 4. rename replaces an existing newpath atomically, so no process looking up the final name finds it missing, but a window exists in which oldpath and newpath both refer to the file being renamed. [Q5, Q6]
Claim 5. In the round-55 fixture runs (S136 cases h2 and h3) the builder exited 0 each time, after it unlinked and created files in the target of a symbolic-link spans directory and truncated two victim files that were symbolic-link span targets. [Q7, Q8, Q9, Q10]

## Limits

- The quotes describe Linux man-pages 6.19 on this host, read from the installed pages (package man-pages 6.19-1); other systems and versions are not covered.
- S136 is a seat report, not a re-runnable gate output; this entry claims only its cases h2 and h3. Its case h1, its committed-spans case and its case h5d are not claimed here.
- [INFERENCE] A check followed by a write is not atomic with it, so a process that swaps a directory for a link between the two is not stopped by the checks; none of the quoted sources states this.
- The rows marked "leg only" in the decision table have no sourced claim here; their counter legs measure the builder's behaviour, not the Linux behaviour.
- The counter is structural: it checks that the quotes exist where their rows say and that each claim cites them; it does not judge that a claim follows from its quotes.
