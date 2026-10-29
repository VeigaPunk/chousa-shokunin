# Gate — round 62 (draft for `corpus/lessons/round-62.md`, `## Gate`)

Drafted 2026-10-28 by ScribeGate (wave w1). Not placed in the lesson file; L1 integrates. Access date for every row:
2026-10-28. No URL was fetched; every source is local. Rendering for the man-page rows is the counter's pipeline,
`MANWIDTH=1000 LC_ALL=C.UTF-8 man -l FILE | col -bx` (171 rendered lines); roff line numbers come from
`zcat FILE.gz`. "Rendered" line numbers refer to that render, "roff" to the page source, "file" to a plain text file.

Rows are the three proposed rows in `corpus/evidence/round62/controls/c2v2-positive-rows.txt`, plus one proposed
REJECTED row (S141, id to be assigned by L1; not written to `corpus/SOURCES.md`).

## S138 — openat2(2), Linux man-pages 6.19 — ADMIT (tier A)

- path: `/usr/share/man/man2/openat2.2.gz` (Arch man-pages 6.19-1; page header `.TH openat2 2 2026-07-02 "Linux man-pages 6.19"`, roff line 6)
- access: 2026-10-28
- teaches: RESOLVE_NO_SYMLINKS refuses a symbolic link in every path component while O_NOFOLLOW judges only the final one.
- located quote (teaches): "which affects the handling of symbolic links only in the final component of path" (14 words). Location: roff lines 335-341 (the sentence "Note that the effect of the RESOLVE_NO_SYMLINKS flag ..."); rendered line 86; anchor RESOLVE_NO_SYMLINKS (RESOLVE_NO_SYMLINKS entry, rendered lines 81-86).
- other located quotes (entry Q1-Q5), each re-found verbatim in my render after whitespace normalisation:
  - Q1 (24 words) "The primary use case for these flags is to allow trusted programs to restrict how untrusted paths (or paths inside untrusted directories) are resolved." roff 187, rendered 52; anchor RESOLVE_NO_SYMLINKS.
  - Q2 (12 words) "Disallow resolution of symbolic links during path resolution. This option implies RESOLVE_NO_MAGICLINKS." roff 312, rendered 82; anchor RESOLVE_NO_SYMLINKS.
  - Q3 (14 words) as above, rendered 86; anchor RESOLVE_NO_SYMLINKS.
  - Q4 (24 words) "Do not permit the path resolution to succeed if any component of the resolution is not a descendant of the directory indicated by dirfd." roff 196, rendered 55; anchor RESOLVE_BENEATH.
  - Q5 (11 words) "glibc provides no wrapper for openat2(), necessitating the use of syscall(2)." roff 25-28, rendered 18; anchor RESOLVE_BENEATH (row anchor cell names the SYNOPSIS note).
- decision: ADMIT. Reason: the installed upstream manual page is the primary statement of what the RESOLVE_* flags do on Linux; the teaches sentence is verbatim on the page; the SYNOPSIS note supports the claim that a caller reaches openat2 through syscall(2).
- correction for L1 (not a blocker for the counter, which does not check it): the row's date "Linux man-pages 6.19, 2026-02-08" does not appear on the page. The page's own date is 2026-07-02 (roff line 6); the package build date is 2026-08-27 (`/var/lib/pacman/local/man-pages-6.19-1/desc`, %BUILDDATE% 1787839958). Cite the `.TH` date, or mark 2026-02-08 as an unverified release date. INFERENCE: the 2026-02-08 date is carried over from the S134/S135 rows, which I did not re-check.

## S139 — linux/openat2.h, linux-api-headers 7.2-1 — ADMIT (tier A)

- path: `/usr/include/linux/openat2.h` (linux-api-headers 7.2-1; package build date 2026-08-17)
- access: 2026-10-28
- teaches: the header gives 0x04 as the value of RESOLVE_NO_SYMLINKS and comments it as blocking traversal through all symlinks.
- located quote (teaches): "Block traversal through all symlinks (implies OEXT_NO_MAGICLINKS)" (7 words). Location: header lines 37-38; anchor "RESOLVE_NO_SYMLINKS" on line 37 (`#define RESOLVE_NO_SYMLINKS	0x04 /* ...`).
- decision: ADMIT. Reason: the header is the primary source for the numeric flag values that the probe reads, and the quoted comment is verbatim in the file.
- corrections for L1 (neither blocks the row):
  1. The row's teaches says "the one-line meaning each carries in the header". The comments are not one line: RESOLVE_NO_XDEV, RESOLVE_NO_MAGICLINKS, RESOLVE_NO_SYMLINKS, RESOLVE_BENEATH, RESOLVE_IN_ROOT and RESOLVE_CACHED each wrap onto a second line (file lines 33-34, 35-36, 37-38, 39-41, 42-44, 45-48). Say "the comment on each flag".
  2. Line 38 names `OEXT_NO_MAGICLINKS`, which the header does not define; `RESOLVE_NO_MAGICLINKS` is the defined name (line 35). Claim 5 of the entry quotes this comment and must not present `OEXT_NO_MAGICLINKS` as an identifier.

## S140 — openat2 probe output (own-work) — ADMIT, CONDITIONAL (tier B)

- path: `corpus/evidence/round62/openat2-probe.txt`. NOT PRESENT in the lane tree on 2026-10-28
  (`ls corpus/evidence/round62/ | grep -i openat2` printed nothing, exit 1). The row cannot resolve, and the counter's
  ROWS and PROBE checks cannot pass, until L1 commits the probe script and its output.
- re-run (scratch, not the lane): `python3 -B controls/candidate-openat2-probe.py --work <absent scratch dir>` exit 0;
  stdout identical to `controls/candidate-openat2-probe.txt` (`diff` empty); `PROBE_FACTS=14/14`; `KERNEL 7.2.11-arch1-1`;
  `PYTHON 3.14.8`.
- access: 2026-10-28
- teaches: os.open with O_NOFOLLOW follows a symlink in an earlier component, and openat2 with RESOLVE_NO_SYMLINKS refuses it with ELOOP.
- located quote (teaches): "PROBE P04 openat2-NO_SYMLINKS-symlink-in-earlier-component observed=ELOOP expected=ELOOP ok" (6 words). Location: candidate output line 7 (P04); the os.open half is line 5 (P02, `observed=opened`). Anchor "P02" and "P04" match the row's anchor cell.
- decision: ADMIT, CONDITIONAL. Reason: the observation is re-runnable, was reproduced on this host today, and the tier and host scope are right. Conditions:
  1. L1 commits the probe script and its output byte-identical to the candidate (the counter's PROBE rule compares the PROBE lines).
  2. The scope cell must say that `expected=` values are the lane author's constants. They are typed by hand at candidate lines 84 (P01 `False`), 92 (P02 `"opened"`), 99 (P03 `"ELOOP"`) and 128 (P11 `"outside"`). The docstring (lines 7-8) says a match means "the result the openat2(2) page states or implies"; for these probes that is false, because the openat2(2) page has no text on os.open or Python (`grep -c "os.open\|Python\|states or implies" openat2.man.txt` = 0). So `PROBE_FACTS=14/14` measures agreement with the lane's own expectations. The observed lines carry the evidence.
  3. P02's os.open expectation is grounded in open(2) (registry row S134, `corpus/SOURCES.md` line 144: O_NOFOLLOW "still follows earlier components"), not in openat2(2). Cite S134 for that half if the entry keeps the claim.

## Proposed REJECTED row — S141 (id for L1 to assign)

| S141 | candidate-openat2-probe.py module docstring, lines 2-9 — lane file corpus/evidence/round62/controls/candidate-openat2-probe.py (own-work, not an external source) | own-work | C | the probe's stated meaning of PROBE_FACTS; not evidence of what the openat2(2) page or this kernel does | docstring lines 7-8 "PROBE_FACTS=<k>/<n> (the number of probes whose observed result equals the result the openat2(2) page states or implies)" | REJECTED: a docstring states intent; the openat2(2) page (S138) contains no text on os.open or Python (0 hits), and the expectations of P01, P02, P03 and P11 are typed constants (candidate lines 84, 92, 99, 128), so the count measures agreement with the author, not with the page; flip: cite each expectation to S134 (open(2)) or S138 (openat2(2)) line by line, or report the count as observation only | none (rejected) | 2026-10-28 |

This row follows S137's precedent: an own-work docstring is intent, not evidence that the stated contract holds.

## Spot-check request (for a non-author to re-open)

- ADMIT to re-open: S138 Q3. `zcat /usr/share/man/man2/openat2.2.gz | sed -n '335,341p'` must contain "which affects the treatment of symbolic links in all of the components of path, differs from the effect of the O_NOFOLLOW file creation flag, which affects the handling of symbolic links only in the final component of path". Check the sentence contrasts RESOLVE_NO_SYMLINKS with O_NOFOLLOW, as the teaches says.
- REJECT to re-open: S141. Open `corpus/evidence/round62/controls/candidate-openat2-probe.py` lines 7-8 and 84, 92, 99, 128. Check that the expectations are typed constants and that the rendered openat2(2) page contains no os.open or Python text (`MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx | grep -c "os.open\|Python"` prints 0).
