# ScribeC2V2Entry3 — round 62 wave w1 — C2 entry draft (scribe)

Deliverable: `.ufo/waves/round-62/w1/ScribeC2V2Entry3/entry.md` (49 lines, 736 words; `wc -l`, `wc -w`).
Frozen counter run on a scratch mirror built as `controls/run-c2v2-controls.py` builds one (lane corpus copy
without captures/evidence/fixtures; README line added; probe script and output copied from `controls/candidate-*`;
`c2v2-positive-rows.txt` inserted before `## Paths`; draft placed at `corpus/knowledge/openat2-resolve-r62.md`).
Driver: `/fast/scratch/hyaku/chousa-r62/ScribeC2V2Entry3/mirror-driver.py`, which runs
`TMPDIR=<scratch> python3 -B corpus/evidence/round62/c2v2-count.py --root <mirror>`. Nothing in the lane was written.

## Findings

1. **Draft passes the frozen counter.** Output line, rc=0:
   `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=11/11 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS`
   Quote split: S138 7 (Q1–Q7), S139 1 (Q8), S140 3 (Q9–Q11). Claims: 6, each citing quotes; all 11 quotes cited.
2. **Harness check.** The same driver on the positive control `controls/c2v2-positive-entry.md` also prints
   `C2=PASS` (rc=0) with `QUOTES=9/9`. The harness therefore reproduces the control's pass; it does not show
   that the counter discriminates my entry from the control (that is the L1's comparison).
3. **The lane tree as it stands fails, as expected.** `python3 -B corpus/evidence/round62/c2v2-count.py --root <lane>`
   prints `ENTRY=0/1 TRIO=0/1 ROWS=0/3 ... PROBE=0/1 MAP=0/1 CENSUS=1/1 C2=FAIL`, rc=1. Integration must still
   promote: (a) rows S138–S140 into `corpus/SOURCES.md` (`grep -n "^| S13[89] \|^| S140 " corpus/SOURCES.md` → no output);
   (b) `corpus/evidence/round62/openat2-probe.py` and `openat2-probe.txt`, which S140 cites as its source and which
   exist only under `controls/candidate-*` (`ls corpus/evidence/round62/openat2-probe.*` → No such file);
   (c) the entry at `corpus/knowledge/openat2-resolve-r62.md`; (d) the `corpus/README.md` line (MAP).
4. **S139 header defect (quoted, not corrected).** The header comment on RESOLVE_NO_SYMLINKS reads
   `(implies OEXT_NO_MAGICLINKS)`. `grep -c OEXT_NO_MAGICLINKS /usr/include/linux/openat2.h` → `1` (the comment only);
   the defined macro is `RESOLVE_NO_MAGICLINKS 0x02` (`grep -n "define RESOLVE_NO_MAGICLINKS"` → line 35). The entry
   quotes the comment verbatim (Q8) and lists the typo under Limits. The counter does not check this.
5. **S138 date mismatch (not reconciled).** Rendered page footer: `Linux man-pages 6.19 ... 2026-07-02`
   (`grep -n "2026-07-02" man-openat2.txt` → line 171). Registry row S138 gives `man-pages 6.19 (2026-02-08)`. The
   entry states both dates under Limits; the row's date is not changed here.
6. **Lead record.** claims.md says S138 "is the lead recorded in `corpus/SOURCES.md` `## Leads`". The lead is there
   (`SOURCES.md` line 326, "openat2(2) ... RESOLVE_NO_SYMLINKS covers every path component, unlike `O_NOFOLLOW`;
   named by wave seat RevC2Claim1 (round 61)"), but it carries no S-id; the id comes only from the rows file.
7. **Calibration, from the screens (both fixed before the final run).**
   - ECHO: Claim 1 first said "symbolic-link refusal"; S138 says "affects the treatment". Reworded to the quote's verb.
   - ECHO: Claim 2 first read `2 of 8` words outside its quotes (counter line: `ECHO claim has 2 of 8 words outside its
     quotes`). Reworded with the same content to `3 of 9` (`ECHO=1/1`). ECHO is a word-count screen: a same-meaning
     rewording flipped it, so it measures wording, not entailment.
   - ANCHOR: Q7 anchored on "SYNOPSIS note on the missing glibc wrapper" failed (`QUOTE Q7 S138 words=11 found=True
     anchor_ok=False`). The counter requires the anchor in both the row's anchor cell and the rendered text; changed to
     `SYNOPSIS`, which is in both.
   - Q6 extended with its `ELOOP` heading, so Claim 2's ELOOP link is in the quote.
8. **Own error, repaired.** One `edit` call overwrote line 1 of my draft with a placeholder (the response showed it).
   The file was rewritten whole. The final file is checked: `cmp` of the mirror copy and the deliverable is identical
   (`mirror entry == deliverable`), and the counter ran on that file.

## Evidence pointers (commands and observed output)

- Rendered S138: `MANWIDTH=1000 LC_ALL=C.UTF-8 man -l /usr/share/man/man2/openat2.2.gz | col -bx > man-openat2.txt`,
  rc=0, 15992 bytes. Quote lines in that file: Q1 l.52; Q2 l.82; Q3 and Q4 l.86; Q5 l.55; Q6 l.123; Q7 l.18.
- S139: `/usr/include/linux/openat2.h` lines 35, 37–38: `#define RESOLVE_NO_SYMLINKS 0x04 /* Block traversal through
  all symlinks` / `(implies OEXT_NO_MAGICLINKS) */`. Q8 is that comment, whitespace-normalised.
- S140: `python3 -B controls/candidate-openat2-probe.py --work <scratch>/probe-live > probe-live.txt` → rc=0;
  `diff probe-live.txt controls/candidate-openat2-probe.txt` → no output, rc=0. Q9 = line 5 (P02), Q10 = line 7 (P04),
  Q11 = line 4 (P01); line 18 is `PROBE_FACTS=14/14`, which the counter's PROBE check reads.
- Installed versions, read-only (no pacman): `ls /var/lib/pacman/local | grep` → `linux-api-headers-7.2-1`,
  `man-pages-6.19-1`.
- Census on the lane registry: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md`
  → `ok`, rc=0; the mirror's CENSUS=1/1 agrees.

## Quotes and where they are used

| id | source | quote (abridged; exact text in entry.md) | used by |
|---|---|---|---|
| Q1 | S138 | "The primary use case for these flags is ... are resolved." | Claim 4 |
| Q2 | S138 | "This option implies RESOLVE_NO_MAGICLINKS." | Claim 2 |
| Q3 | S138 | "which affects the treatment of symbolic links in all of the components of path" | Claim 1 |
| Q4 | S138 | "which affects the handling of symbolic links only in the final component of path" | Claim 1 |
| Q5 | S138 | "Do not permit the path resolution to succeed ... indicated by dirfd." | Claim 4 |
| Q6 | S138 | "ELOOP how.resolve contains RESOLVE_NO_SYMLINKS, ... (or magic link)." | Claim 2 |
| Q7 | S138 | "glibc provides no wrapper for openat2(), necessitating the use of syscall(2)." | Claim 5 |
| Q8 | S139 | "#define RESOLVE_NO_SYMLINKS 0x04 /* Block traversal through all symlinks (implies OEXT_NO_MAGICLINKS) */" | Claim 6 |
| Q9 | S140 | "PROBE P02 os.open-O_NOFOLLOW-symlink-in-earlier-component observed=opened ..." | Claim 3 |
| Q10 | S140 | "PROBE P04 openat2-NO_SYMLINKS-symlink-in-earlier-component observed=ELOOP ..." | Claim 3 |
| Q11 | S140 | "PROBE P01 python-os-has-openat2 observed=False expected=False ok" | Claim 5 |

Principles in the entry: (1) scope of the flag against O_NOFOLLOW (Claims 1–3); (2) intended use and
RESOLVE_BENEATH (Claim 4); (3) caller route through syscall(2) and the header's flag description (Claims 5–6).

## Limits of this draft

- Rows S138–S140 are the ones the task named (`c2v2-positive-rows.txt`); I did not register them in the lane.
- Entailment (does each claim follow from its quotes) was checked by me only by reading; the counter does not check it.
  Claim 3 says "earlier component is a symbolic link": the quote's label says `symlink-in-earlier-component`, and the
  probe builds a symlinked directory (`candidate-openat2-probe.py` lines 77 and 87); the entry does not quote that construction.
- Limits bullet 4 is marked `[INFERENCE]` (a check-then-write window could be closed by these flags; not tested here).
- Not run: any other kernel or filesystem, the EAGAIN and O_CREAT paths, and the positive-control comparison (L1).
- Installed tools: none. No pacman, git, or lane writes. Scratch `/fast/scratch/hyaku/chousa-r62/ScribeC2V2Entry3/` deleted before yield.

VERDICT: ENTRY3_C2=PASS quotes=11 claims=6
