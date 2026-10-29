# ScoutC2ManPages — S138/S139 source re-open (round 62, wave w1)

Re-opened both sources behind the C2 entry's Q1-Q6 and confirmed every quote's location, heading, and
transformation status. Read-only seat: nothing under corpus/evidence/round62/, tools/, corpus/ or SKILL.md
was modified; scratch /fast/scratch/hyaku/chousa-r62/ScoutC2ManPages/ was deleted after use.

## Sources re-opened (commands as run)

- Rendered: `MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx` → 171 lines.
- Raw man output (no col): `MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz` → identical bytes.
- Unrendered roff: `zcat /usr/share/man/man2/openat2.2.gz` → 616 lines.
- Header: read /usr/include/linux/openat2.h → 50 lines (linux-api-headers 7.2-1).
- Matches rows: S138 = man-pages 6.19 rendered with MANWIDTH=1000 man -l FILE then col -bx; S139 = the
  installed kernel header. Both re-opened on this host, 2026-10-28.

## col -bx / whitespace normalisation

- `col -bx` changed nothing: `cmp` of man's raw output vs `man | col -bx` reported IDENTICAL; both files
  contain 0 ESC bytes and 0 backspace bytes (at MANWIDTH=1000 this man emits plain text, no overstrikes).
- Whitespace normalisation was applied when the entry transcribed quotes: the rendered page puts each
  paragraph on one long line with two spaces after sentence periods (93/171 rendered lines contain a
  double space); all six entry quotes match only after collapsing whitespace runs (verified by a
  python3 -B offset mapper, "exact-after-ws-norm" for Q1-Q6). No wording differences found in Q1-Q6.

## Q1-Q6 locations (rendered line = raw line unless noted)

- Q1 "The primary use case for these flags ... untrusted directories) are resolved." — rendered 52;
  raw.roff 187-188. Heading: DESCRIPTION → "The open_how structure" (29) → `resolve` field intro
  paragraph (resolve flag list starts 54).
- Q2 "Disallow resolution of symbolic links during path resolution. This option implies
  RESOLVE_NO_MAGICLINKS." — rendered 82; raw.roff 312-314 (314 is the `.BR RESOLVE_NO_MAGICLINKS .`
  macro line). Heading: DESCRIPTION → resolve → RESOLVE_NO_SYMLINKS entry (81).
- Q3 "which affects the handling of symbolic links only in the final component of path" — rendered 86
  (mid-sentence: full sentence starts on 86 after "differs from the effect of the O_NOFOLLOW file
  creation flag (in how.flags),"); raw.roff 341-342 (342 = `.IR path .`). Heading: same
  RESOLVE_NO_SYMLINKS entry, O_NOFOLLOW comparison paragraph.
- Q4 "Do not permit the path resolution to succeed ... descendant of the directory indicated by dirfd." —
  rendered 55; raw.roff 196-198 (198 = `.IR dirfd .`). Heading: DESCRIPTION → resolve → RESOLVE_BENEATH
  entry (54).
- Q5 "glibc provides no wrapper for openat2(), necessitating the use of syscall(2)." — rendered 18 (the
  "Note:" line closing SYNOPSIS, 9-18; quote omits the leading "Note:"); raw.roff 24-28 (25-28 carry the
  quote; 24 is `.IR Note :`). Heading: SYNOPSIS.
- Q6 "Block traversal through all symlinks (implies OEXT_NO_MAGICLINKS)" — /usr/include/linux/openat2.h
  lines 37-38 (define at 37, comment continuation at 38). No sections: flat header; the block is the
  comment `/* how->resolve flags for openat2(2). */` at line 32. Verbatim including the literal
  "OEXT_NO_MAGICLINKS" — note that name is not defined anywhere in the header (only RESOLVE_NO_MAGICLINKS
  0x02 at 35); the entry's verbatim quote is faithful, the stale name is the header's own.

All k=6 located in both forms with section headings.

## Extra quotes that would strengthen the entry (all ≤25 words, all verified verbatim)

1. 19 words — S138 ERRORS, EAGAIN (race) entry: rendered 109, raw.roff 426-427: "the kernel could not
   ensure that a ".." component didn't escape (due to a race condition or potential attack)". Same line
   continues "The caller may choose to retry the openat2() call."; directly supports the entry Limits
   remark about the EAGAIN retry for racing dotdot walks. A second EAGAIN entry (RESOLVE_CACHED) sits at
   rendered 111-112, raw.roff 432-436.
2. 14 words — S138 DESCRIPTION → resolve → RESOLVE_IN_ROOT (59): rendered 60, raw.roff 211-212: "Treat
   the directory referred to by dirfd as the root directory while resolving path."
3. 12 words — S138 DESCRIPTION → resolve → RESOLVE_NO_XDEV (90): rendered 91, raw.roff 360-361:
   "Disallow traversal of mount points during path resolution (including all bind mounts)."
4. 14 words — S138 same RESOLVE_IN_ROOT entry: rendered 64, raw.roff 245-247: "Currently, this flag also
   disables magic-link resolution. However, this may change in the future." — important calibration: the
   magic-link blocking implied by BENEATH/IN_ROOT is documented as possibly temporary; the BENEATH twin at
   rendered 57 / raw.roff 203-204 adds "(see below)" (16 words with it).

## Header values adjacent to Q6 (S139 scope: RESOLVE_*/OPENAT2_REGULAR values)

- /usr/include/linux/openat2.h: RESOLVE_NO_XDEV 0x01 (33), RESOLVE_NO_MAGICLINKS 0x02 (35),
  RESOLVE_NO_SYMLINKS 0x04 (37), RESOLVE_BENEATH 0x08 (39), RESOLVE_IN_ROOT 0x10 (42),
  RESOLVE_CACHED 0x20 (45), OPENAT2_REGULAR `((__u64)1 << 32)` (30, comment "Only open regular files.").
- Header RESOLVE_BENEATH comment (39-41) is a candidate seventh quote if a header one-liner for BENEATH is
  ever wanted: "Block "lexical" trickery like "..", symlinks, and absolute paths which escape the dirfd."
  (13 words, lines 39-41).

## Evidence pointers

- `MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx | wc -l` → 171 (observed).
- `cmp` raw-man vs man|col -bx → "IDENTICAL" (observed); ESC/BS byte counts 0/0 in both (observed via
  python3 -B).
- `zcat /usr/share/man/man2/openat2.2.gz | wc -l` → 616; grep line hits as listed above (raw.roff 187-188,
  196-198, 203-204, 211-212, 245-247, 312-314, 341-342, 358-361, 420-427, 432-436).
- Rendered line hits (python3 -B offset mapping over whitespace-collapsed lines): Q1 52, Q2 82, Q3 86,
  Q4 55, Q5 18, X1 109, X2 60, X3 91, X4 64 (single-line hits each).
- Rendered section anchors: NAME 3, LIBRARY 6, SYNOPSIS 9, DESCRIPTION 20, The open_how structure 29,
  RESOLVE_BENEATH 54, RESOLVE_IN_ROOT 59, RESOLVE_NO_MAGICLINKS 66, RESOLVE_NO_SYMLINKS 81,
  RESOLVE_NO_XDEV 90, RETURN VALUE 100, ERRORS 103, EAGAIN 108/111, STANDARDS 134, HISTORY 137, NOTES 142,
  Extensibility 143, SEE ALSO 168.
- Header lines: block comment 32, values/quotes 30, 33-48 as listed above; total 50 lines.

## Caveats

- INFERENCE: none needed for locations (all observed). The claim that "OEXT_NO_MAGICLINKS" is undefined in
  this header rests on reading all 50 lines; no grep of other headers was done, and upstream comparison was
  out of scope (no network).
- Rendered line numbers are for MANWIDTH=1000 | col -bx exactly as the rows specify; other widths re-flow.

VERDICT: Q1_Q6_LOCATED=6/6 extra_quotes=4
