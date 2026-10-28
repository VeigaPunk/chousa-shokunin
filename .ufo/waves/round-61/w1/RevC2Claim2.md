# RevC2Claim2 — entailment review of C2 Claim 2

Scope: Claim 2 of `corpus/evidence/round61/controls/c2-positive-entry.md` only, and its cited quote Q3.
Read-only. No counter run (not requested). Scratch created and removed.

## Claim 2 as written

> Claim 2. Creating a file with O_CREAT and O_EXCL fails on any existing path that is a symbolic link, regardless of where the link points, so a fresh temporary name cannot be written through a planted link. [Q3]

Q3 (S134, open(2)) as written in the entry:

> symbolic links are not followed: if path is a symbolic link, then open() fails regardless of where the symbolic link points. | O_EXCL

## Evidence I re-opened

Commands (run in scratch, then deleted):

    MANWIDTH=1000 man -l /usr/share/man/man2/open.2.gz | col -bx > open2.txt    # 516 lines
    MANWIDTH=1000 man -l /usr/share/man/man2/rename.2.gz | col -bx > rename2.txt # 210 lines

Observed:

- `grep -c -F '<Q3 text verbatim>' open2.txt` → `1`. The entry's Q3 text is byte-identical to the rendered page.
- Full context, open2.txt lines 120-123 (the O_EXCL entry):
  - L120 `O_EXCL`
  - L121 "Ensure that this call creates the file: if this flag is specified in conjunction with O_CREAT, and path already exists, then open() fails with the error EEXIST."
  - L123 Q3: "When these two flags are specified, symbolic links are not followed: if path is a symbolic link, then open() fails regardless of where the symbolic link points."
  - L125 "In general, the behavior of O_EXCL is undefined if it is used without O_CREAT..."
  - Q3 is therefore correctly bound to the O_CREAT+O_EXCL pair. No misreading of the flag pair.
- Error list, L284: `EEXIST path already exists and O_CREAT and O_EXCL were used.` (consistent with Q3's "fails").
- Scope of symlink handling, L146-147 (O_NOFOLLOW): "If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP. Symbolic links in earlier components of the pathname will still be followed."
- Page version, L516: `Linux man-pages 6.19`.

Q3 is silent on symlinks in earlier (directory) components. Only the O_NOFOLLOW paragraph states that earlier components are followed, and Q3 does not extend the O_EXCL guarantee to them.

## Decision per part of Claim 2

1. "Creating a file with O_CREAT and O_EXCL fails on any existing path that is a symbolic link, regardless of where the link points" — **supported**. It is Q3 in its own words; "any existing path that is a symbolic link" reads the same as "path is a symbolic link" (a dangling link is an existing directory entry, so no gap there).
2. "so a fresh temporary name cannot be written through a planted link" — **overreach**. The consequence is written without a scope. A reader who has just read Claim 1 (which says the directory components are still followed) will take "a planted link" to cover a link planted in a directory component. Q3 supports only the final-component case. The gap is the unscoped phrase "a planted link", not the verb "fails". Stating the consequence for the final component is supported; stating it for any planted link is not.
3. "fresh temporary name" is the writer's design, not a term in Q3. Q3 does not say the writer uses a temporary name. Treating it as the writer's use is an inference. It is a reasonable one, but it is not marked [INFERENCE] in the entry.

Calibration notes (do not change the verdict):

- Claim 2 does not carry the Linux 6.19 scope. The entry's Limits section does ("The quotes describe Linux man-pages 6.19 on this host"), so this is covered at entry level, but Claim 2 read alone is stated for all systems. The man page does not support a portability claim.
- The entry's Limits section already states the counter does not judge entailment. This review is that judgment, and the counter's `C2=PASS` (not run here) would not reflect the overreach above. That is consistent with the frozen C2 limit.

## Rewrite proposal (Claim 2 only)

> Claim 2. On Linux (man-pages 6.19), creating a file with O_CREAT and O_EXCL fails when the final component of the path is a symbolic link, regardless of where the link points. A writer that creates its temporary file with O_CREAT and O_EXCL at a fresh name therefore does not write through a link planted at that name. Symbolic links in earlier (directory) components are not covered by this flag; Claim 1 applies to them. [Q3]
>
> [INFERENCE: "fresh name" and the writer's temporary file are the writer's design, not text in Q3.]

Note: this keeps Claim 1 as the only claim about directory links, which is what the entry's Claim 1 already says.

## Not checked (outside scope)

- Claims 1, 3, 4, 5 and their quotes Q1, Q2, Q4-Q8 were not reviewed here. Q1, Q2 and Q4-Q6 are present in the rendered pages (grep above shows the same sentences in open2.txt L147 and rename2.txt L38, L46); Q7-Q8 are in S136 and were not opened by this seat.
- The counter `c2-count.py` was not run.

VERDICT: CLAIM2=overreach rewrite_needed=yes
