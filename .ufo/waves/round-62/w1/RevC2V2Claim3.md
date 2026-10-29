# RevC2V2Claim3 — entailment review of C2 entry Claim 3

Scope: Claim 3 of `corpus/evidence/round62/controls/c2v2-positive-entry.md` (landing candidate for
`corpus/knowledge/openat2-resolve-r62.md`). Read-only on the lane; the rewrite is a candidate under my own
directory. No network, no git writes, no seats spawned.

## Original Claim 3 (as landed)

    Claim 3. The flags are designed for trusted programs that handle untrusted directories, and RESOLVE_BENEATH rejects any resolution that would leave the directory named by the descriptor. [Q1, Q4]

Quotes cited, re-opened by me:

- Q1 (S138 man-pages 6.19 DESCRIPTION, how.resolve): "The primary use case for these flags is to allow trusted programs to restrict how untrusted paths (or paths inside untrusted directories) are resolved."
- Q4 (S138, RESOLVE_BENEATH): "Do not permit the path resolution to succeed if any component of the resolution is not a descendant of the directory indicated by dirfd."

Both quotes match the rendered page exactly (see evidence E1).

## Findings

1. **Half 1 overreaches.** Q1 says "primary use case". The claim says "designed for", which states a design
   purpose, not the page's primary use. The page's scope is also "untrusted paths (or paths inside untrusted
   directories)"; the claim narrows it to "untrusted directories" and drops the untrusted-path case. Hedge lost:
   "primary". Severity: calibration, minor.
2. **Half 2 is supported.** Q4's "not a descendant of the directory indicated by dirfd" is faithfully rendered as
   "would leave the directory named by the descriptor". "any" matches "any component". The header comment on
   RESOLVE_BENEATH (E2, not cited by the entry) says the same: it blocks `..`, symlinks and absolute paths that
   "escape the dirfd". The probe agrees with the half-2 reading (E3: P07 EXDEV for a `..` escape, P08 EXDEV for an
   absolute symlink, P09 opened for an in-tree relative symlink).
3. **A page hedge is lost in half 2.** ERRORS (S138) lists EAGAIN for BENEATH and RESOLVE_IN_ROOT: "the kernel could
   not ensure that a '..' component didn't escape (due to a race condition or potential attack). The caller may
   choose to retry". The claim's "rejects any resolution" leaves out that the refusal can come back as EAGAIN in
   that case, with a retry allowed. The probe does not exercise this path, so the hedge is a page statement, not a
   probed fact. Severity: calibration.
4. **No `always`, `all` or host-specific fact** appears in Claim 3. The host (kernel 7.2.11, Python 3.14.8) is not
   stated as general in this claim.
5. **Not a finding, noted for the other claims:** the page's "encouraged to make its use configurable ...
   spurious errors" caution covers RESOLVE_NO_SYMLINKS and RESOLVE_NO_XDEV, not BENEATH. Claim 3's first half could
   be read as "safe to apply widely", which the page warns against for those two flags. Claim 3 does not say that,
   so this is INFERENCE for the wider entry, not a Claim 3 defect.

Verdict on the original: **overreach** (calibration: "designed for" for "primary use case"; scope narrowed to
"untrusted directories"; EAGAIN hedge not stated). Not a misread: the paraphrase of Q4 is faithful.

## Rewrite (candidate)

File: `.ufo/waves/round-62/w1/RevC2V2Claim3/c2v2-entry-claim3.md` (the original entry with Claim 3 replaced and one
quote added; nothing else changed).

    Claim 3. The page calls restricting how untrusted paths, and paths inside untrusted directories, are walked the primary use case for these flags, aimed at trusted programs; RESOLVE_BENEATH fails any walk whose component leaves the dirfd directory, and the page lists EAGAIN for a dotdot the kernel cannot vouch for. [Q1, Q4, Q10]

    - Q10 | S138 | EAGAIN how.resolve contains either RESOLVE_IN_ROOT or RESOLVE_BENEATH, and the kernel could not ensure that a ".." component didn't escape | RESOLVE_BENEATH

Q10 is the page's ERRORS entry, 19 words, verbatim in the rendered text (checked by the counter, QUOTES=10/10).
Q1 and Q4 are unchanged.

## Counter run (the frozen counter, unmodified; mirror built the way run-c2v2-controls.py builds it)

Command: `TMPDIR=/fast/scratch/hyaku/chousa-r62/RevC2V2Claim3 python3 -B corpus/evidence/round62/c2v2-count.py --root <mirror>`
(mirror = lane corpus copy, positive rows inserted into SOURCES.md, probe script and output copied to
`corpus/evidence/round62/`, README entry line appended, entry at `corpus/knowledge/openat2-resolve-r62.md`).

    == orig-positive rc=0
    ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=9/9 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS
    == claim3-rewrite rc=0
    ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=10/10 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS

The rewrite passes the frozen counter. The counter does not judge entailment (its named limit), so the pass
says the rewrite is structurally sound, not that it is entailed; the entailment reading is the findings above.
The original also passes, which is the named "non-sequitur reaches PASS" limit in action.

## Evidence

- E1: `MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx` (171 lines, Linux man-pages 6.19, 2026-07-02),
  rendered into scratch and read; Q1, Q4 and the ERRORS EAGAIN/EXDEV entries match the quoted text.
- E2: `/usr/include/linux/openat2.h` read; RESOLVE_BENEATH comment: "Block "lexical" trickery like "..", symlinks, and
  absolute paths which escape the dirfd." RESOLVE_NO_SYMLINKS = 0x04, RESOLVE_BENEATH = 0x08, __NR_openat2 in
  the probe output = 437.
- E3: `python3 -B corpus/evidence/round62/controls/candidate-openat2-probe.py --work <fresh scratch>/probe-work`
  exit 0; output matched the committed `candidate-openat2-probe.txt` line for line (`diff` identical), `PROBE_FACTS=14/14`,
  kernel 7.2.11-arch1-1, Python 3.14.8. First attempt exited 2 only because my own man render had been written
  into the probe's `--work` directory; rerun in a fresh subdirectory, no change to the probe.
- E4: rewrite counter run above (exit 0 on both mirrors).

## Limits of this review

- Entailment is judged by me, a single non-author reviewer; no second reviewer read it.
- The probe does not exercise the EAGAIN path, so the EAGAIN hedge is cited from the page only.
- Only the candidate's pass on the frozen counter was run; the landing entry itself was not edited (the lane is
  frozen for this seat).

## Tooling

No tools installed or upgraded. Used `man`, `col`, `python3 -B`, `diff`, all present on the host.

VERDICT: CLAIM3=overreach rewrite_needed=yes
