# ScoutC2RowsScope — round 62, wave w1 — registry fit of candidate rows S138, S139, S140

Scope: the three `scope` cells (and the cells that carry the same claims) against their sources; tier for the
header row; near-duplicates in `corpus/SOURCES.md`; the `## Leads` openat2 bullet. Read-only. No lane file edited;
replacement text is below for the L1 integrator to apply. Frozen predicates and counters were not changed; they
were run only in a scratch fixture (see E6).

## Findings

1. **S138 (man page, tier A): scope overreaches on glibc.** The scope says the page establishes "that glibc has no
   wrapper". The page says so (`SYNOPSIS`, line 18: "Note: glibc provides no wrapper for openat2()"). Nothing in the
   registry checks glibc itself, so the scope must say "the page states". Needs edit: scope, teaches.
   The O_NOFOLLOW half of its teaching is the same fact as S134 (O_NOFOLLOW judges only the final component); not a
   duplicate row, but the teaching should cross-reference S134 instead of re-asserting it. Tier A is correct for the
   page's own statements (same scope discipline as S134).

2. **S139 (header, tier A): tier stays A; the scope cell claims more than the header is.** The frozen counter pins
   S139 to tier A (`TIER = {"S138": "A", "S139": "A", "S140": "B"}`, `c2v2-count.py:55`), and `ROWS` fails any other
   tier, so the tier cannot become B. The fix is to narrow the scope, not to change the tier. A kernel UAPI header is
   tier A for what the header itself says: the numeric constants (the ABI) and the comment words as written. It is
   not evidence of behaviour; "blocks traversal through all symlinks" is a behavioural claim and belongs to S138
   (page) and S140 (host observation). The current scope ("the one-line meaning each carries") also has a factual
   error: the RESOLVE_NO_SYMLINKS comment spans two lines (`openat2.h` lines 37-38). The comment also names
   `OEXT_NO_MAGICLINKS`, which the header does not define (`grep -n OEXT` returns only line 38), so the teaching must
   not paraphrase that name as `RESOLVE_NO_MAGICLINKS`. Needs edit: scope, anchor (line numbers), teaches.

3. **S140 (own-work probe, tier B): tier B is honest; the teaching is not scoped as far as the row's own scope.**
   B is the right tier for a re-runnable own-work probe on one host (S136 precedent: own-work = B). But:
   (a) the teaching says "the os module has no openat2 function" without the host qualifier the scope gives;
   (b) the scope omits that `PROBE_FACTS` counts agreement with expectations hard-coded in the script
   (`candidate-openat2-probe.py`: `probe("P01", ..., hasattr(os, "openat2"), False)`, and the `expected` arguments
   elsewhere). That is a self-consistency check, not an independent measurement; the row should say so.
   (c) recheck `180d` is a calendar guess; the result is tied to the kernel release, so `on-release` fits better
   (INFERENCE, a judgement; no counter checks recheck values beyond the enum).
   Also: the files the row cites do not exist yet (E7). The row cannot be landed without
   `corpus/evidence/round62/openat2-probe.py` and `openat2-probe.txt`.

4. **Near-duplicates: none.** S138 overlaps S134 on one half of one fact (see 1). S139 has no header row. S135
   (rename) is a different call. No row cites openat2, RESOLVE_* or linux-api headers (E4).

5. **Leads bullet: annotate, do not delete.** The lane has no numbered "append-only rule 2" in
   `corpus/SOURCES.md` or `corpus/QUALITY.md` (QUALITY criterion 2 is "every claim carries a source"). The closest
   rule is QUALITY criterion 4, "Errata are append-only blocks", plus the round-25 precedent in SOURCES.md (superseded
   rows and cells stay, marked, rather than being removed). Git history shows no Leads bullet ever deleted when it
   became a row (E8). Append a resolution line under the bullet; keep the original text, including "not opened as a
   row", because it is true of round 61. Line 322 (the round-61 narrative) stays as history.

6. **Landing order.** S138–S140 `used-by` names the entry; until it exists, census validate reports three `E11`
   (dangling used-by). Rows, entry, probe `.py`, probe `.txt`, README map line and the Leads annotation must land in
   one commit. Rows alone fail the census (E5).

7. **Entry-level defect (not a row cell; the counter does not catch it).** In
   `corpus/evidence/round62/controls/c2v2-positive-entry.md`, Q5 ("glibc provides no wrapper for openat2()...") has
   anchor `RESOLVE_BENEATH`. The quote is the SYNOPSIS note; its anchor should be "the SYNOPSIS note on the missing
   glibc wrapper". `QUOTES` passes either way, because the anchor is a substring of the S138 anchor cell.
   Route to the entry author; not a row edit. (Frozen controls: not changed.)

## Replacement text (cell by cell; all other cells unchanged)

### S138
- `scope` →
  `what man-pages 6.19 states the openat2 RESOLVE_NO_SYMLINKS and RESOLVE_BENEATH flags do on Linux, and what its SYNOPSIS says about a glibc wrapper (the page's own statement, not checked against glibc); not the kernel source, not the kernel's behaviour on any host, not other systems`
- `teaches` →
  `RESOLVE_NO_SYMLINKS refuses a symbolic link in every path component while O_NOFOLLOW judges only the final one (the O_NOFOLLOW half is S134); RESOLVE_BENEATH refuses resolution that leaves the directory descriptor; the page says glibc has no openat2 wrapper, so a caller reaches the call through syscall(2)`

### S139
- `scope` →
  `the numeric values of the RESOLVE_* flags and OPENAT2_REGULAR as this header defines them (tier A for those values), and the header's comment text quoted as written; the comments are terse, carry no behaviour specification and are not the kernel implementation (behaviour rests on S138 and S140)`
- `anchor` →
  `the comment on RESOLVE_NO_SYMLINKS in the define block (lines 37-38), linux-api-headers 7.2-1`
- `teaches` →
  `RESOLVE_NO_SYMLINKS is 0x04, RESOLVE_NO_MAGICLINKS 0x02 and RESOLVE_BENEATH 0x08 in this header, so a caller should take the values from the installed header; its comment on RESOLVE_NO_SYMLINKS names OEXT_NO_MAGICLINKS, which this header does not define`
- `tier`: keep `A`.

### S140
- `scope` →
  `what this kernel and this Python 3.14.8 do for 14 openat2 and os.open cases on one local filesystem, x86_64; the expected result of each case is written in the script, so PROBE_FACTS counts agreement with those expectations, not an independent measurement; not a claim about other kernels, hosts or Python versions`
- `teaches` →
  `on this kernel and Python 3.14.8, os.open with O_NOFOLLOW opens a file reached through a symlinked earlier component while openat2 with RESOLVE_NO_SYMLINKS refuses it with ELOOP, and the os module has no openat2 attribute`
- `recheck`: `180d` → `on-release` (INFERENCE; optional, the counter does not read it).
- `tier`: keep `B`.

### Leads (SOURCES.md line 326) — append directly under the bullet, keep the bullet
`  Resolved round 62 (2026-10-28): opened as S138 and S139; host observation in S140; entry corpus/knowledge/openat2-resolve-r62.md.`

## Tier question, answered

A header is tier A for the values and for the words of its comments, within a scope that says so. It is not tier B
for "the semantics", because the comments do not specify behaviour. Behavioural semantics come from the page
(tier A, S138) and the host observation (tier B, S140). So the split is by claim type, not by tier. Changing S139 to B
would fail the frozen `ROWS` check.

## Evidence

- E1 `man -l /usr/share/man/man2/openat2.2.gz | col -bx` (MANWIDTH=1000, LC_ALL=C.UTF-8). The five quotes of the
  positive entry each occur once: "primary use case for these flags" (1), "Disallow resolution of symbolic links during
  path resolution" (1), "affects the handling of symbolic links only in the final component" (1), "Do not permit the
  path resolution to succeed if any component" (1), "glibc provides no wrapper for openat2()" (1). Line 18 is in
  SYNOPSIS; line 86 is the RESOLVE_NO_SYMLINKS/O_NOFOLLOW contrast.
- E2 `/usr/include/linux/openat2.h` lines 37-38: `#define RESOLVE_NO_SYMLINKS 0x04 /* Block traversal through all
  symlinks` / `(implies OEXT_NO_MAGICLINKS) */`. `grep -n OEXT` returns line 38 only.
- E3 installed versions, read from `/var/lib/pacman/local/{linux-api-headers-7.2-1,man-pages-6.19-1}/desc`
  (`%VERSION%` 7.2-1 and 6.19-1). No pacman invocation.
- E4 `_grep` on `corpus/SOURCES.md` for `open(2)|rename(2)|openat|O_NOFOLLOW|RESOLVE_|syscall|linux-api|symlink`:
  rows S134, S135, S136, S137 (lines 144-147), round-61 narrative line 322, Leads line 326. No other openat, RESOLVE_
  or linux-api row. Lines 140-330 re-checked with the same pattern.
- E5 census (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file <scratch SOURCES.md>`, cwd the
  scratch root): baseline on the unmodified registry rc 0 (`ok` 1, `W04` 5, pre-existing). With the three as-filed
  rows: rc 1, `E11` ×3 (S138, S139, S140: `missing used-by corpus/knowledge/openat2-resolve-r62.md`), no E01–E10 on
  any row. The as-filed and edited rows pass E01–E10 at the same tier, status and date.
- E6 frozen counter in scratch (`python3 -B corpus/evidence/round62/c2v2-count.py --root <scratch> --work <scratch>`;
  positive-control entry and candidate probe copied to the landing paths in scratch; README line naming the entry
  added in scratch):
  `as-filed: ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=9/9 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS` (rc 0)
  `edited:    ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=9/9 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS` (rc 0)
  The edits do not break the counter. The counter does not check scope or teaching text, so findings 1–3 are
  judgements against the sources, not counter results. The PROBE line shows the candidate probe reruns to its own
  output on this host.
- E7 landing files absent in the lane: `corpus/evidence/round62/openat2-probe.py` and `openat2-probe.txt` do not exist
  (`ls` → No such file); `corpus/knowledge/openat2-resolve-r62.md` does not exist. The candidate probe output is at
  `controls/candidate-openat2-probe.txt`.
- E8 `git -C <lane> log -p -- corpus/SOURCES.md` (read-only; 55 commits): no removed Leads bullet found in the log.
  `git -C <lane> status --short -- corpus/` shows no change to the registry, the knowledge dir or README.
- Scratch `/fast/scratch/hyaku/chousa-r62/ScoutC2RowsScope/` removed (verified). No fixture git repo was used; no git
  mutation anywhere. No network; no fleet, sibling or shokuknow writes.

## Not checked (named limits)

- glibc's own behaviour or source was not checked; "glibc has no openat2 wrapper" stays the page's statement.
- The probe was not run on any other kernel, filesystem, architecture or Python.
- Entailment of the claims from their quotes was not judged here (counter limit; reviewers' job).
- The edits are judgements; where a sentence is an inference it is marked INFERENCE above.
- No tool was installed or upgraded in this seat.

VERDICT: ROWS_NEEDING_EDIT=3/3
