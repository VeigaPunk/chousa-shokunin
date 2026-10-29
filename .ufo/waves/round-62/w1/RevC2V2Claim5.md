# RevC2V2Claim5 — entailment review of Claim 5 (round 62, wave w1)

Seat: RevC2V2Claim5 (reviewer, leaf). Entry reviewed: `corpus/evidence/round62/controls/c2v2-positive-entry.md`
(sha256 `3c0bff8219fb41e0`, read-only). Frozen files under `corpus/evidence/round62/`, `tools/`, `corpus/`,
`SKILL.md` were not written. Scratch removed. No installs. No git mutation.

## Findings

1. **Claim 5 is an overreach; rewrite needed.** Frozen text:
   `Claim 5. The installed header describes the symlink flag as one that blocks traversal through all symlinks, so a caller should read the numeric flag values from that header instead of typing them from memory. [Q6]`
   - Clause "blocks traversal through all symlinks" follows from Q6. Supported. Q6 is the whole header comment on
     `RESOLVE_NO_SYMLINKS` (header lines 37-38, read by me).
   - Clause "so a caller should read the numeric flag values from that header instead of typing them from memory"
     does not follow from Q6. Q6 has no number, no advice and nothing about memory. This is an unsourced
     prescription added to a one-line quote: an overreach of the calibration kind, not a misread.
   - Hedge lost (a): the header comment says `(implies OEXT_NO_MAGICLINKS)`. The page (Q2) says the flag implies
     `RESOLVE_NO_MAGICLINKS`. The two names differ. The header's own define is `RESOLVE_NO_MAGICLINKS` (line 35);
     `OEXT_NO_MAGICLINKS` appears once, in the comment (line 38). So the comment's identifiers are not the
     identifiers to copy. INFERENCE: the comment is a stale or mistyped comment; the quotes show only the mismatch.
   - Hedge lost (b): the page (Q10, Q11) states a different rule for a trailing symbolic link when the call has
     `O_PATH` and `O_NOFOLLOW`: an `O_PATH` descriptor for the link is returned. The header comment ("Block
     traversal through all symlinks") does not carry that. The original claim omits it.
   - The counter cannot catch this. The frozen counter passes the frozen entry (see checks), by design: its own
     docstring names "does not judge that a claim follows from its quotes" as a limit.

2. **Rewrite (candidate, passes the counter).** Candidate file:
   `.ufo/waves/round-62/w1/RevC2V2Claim5/c2v2-entry-claim5.md` (16-hex sha256 prefix `60bf64085190f733`).
   Diff against the frozen entry is exactly three edits: two added quote lines and one replaced claim line.
   - Added `- Q10 | S138 | If the trailing component (i.e., basename) of path is a symbolic link, how.resolve contains RESOLVE_NO_SYMLINKS, and how.flags contains both O_PATH and O_NOFOLLOW | RESOLVE_NO_SYMLINKS` (22 words, verbatim from the rendered page).
   - Added `- Q11 | S138 | an O_PATH file descriptor referencing the symbolic link will be returned | RESOLVE_NO_SYMLINKS` (13 words, verbatim).
   - Replaced Claim 5 with:
     `Claim 5. The installed header's comment says RESOLVE_NO_SYMLINKS blocks traversal through all symlinks and names the implied flag OEXT_NO_MAGICLINKS, where the page names RESOLVE_NO_MAGICLINKS; the page states a different rule for a trailing symbolic link: with O_PATH and O_NOFOLLOW it gives an O_PATH descriptor for the link, and the comment does not mention that. [Q6, Q2, Q10, Q11]`
   - Clause to quote map: "comment says ... blocks traversal through all symlinks" and "names ... OEXT_NO_MAGICLINKS" = Q6;
     "page names RESOLVE_NO_MAGICLINKS" = Q2 ("This option implies RESOLVE_NO_MAGICLINKS."); "trailing symbolic
     link ... with O_PATH and O_NOFOLLOW ... O_PATH descriptor" = Q10 + Q11; "comment does not mention that" = Q6 is
     the full comment, so the absence is checked against the quoted text itself.
   - Dropped: the advice about reading numbers from the header. The quote set does not carry it. If the L1 wants it
     back, it must be a separate [INFERENCE] limit, not a claim.
   - Wording note: I first wrote "exception" for the page's rule; the page does not use that word, so the
     candidate says "a different rule".

3. **Adjacent, outside my item (routed, not reviewed in full): Claim 1 and the S138 registry row overreach the same way.**
   Claim 1 says `RESOLVE_NO_SYMLINKS` makes the kernel "refuse a symbolic link anywhere along the walk". The page
   (Q10, Q11 text) says that with `O_PATH` and `O_NOFOLLOW` a trailing symbolic link yields a descriptor, not a
   refusal. The probe agrees: P05 (final symlink, no `O_PATH`) is `ELOOP`; P14 (`O_PATH|O_NOFOLLOW|NO_SYMLINKS`
   on a final symlink) is `observed=True` (returns a descriptor for the link). The S138 row's "what" cell repeats
   "refuses a symbolic link in every path component". Route to the Claim 1 owner. Claim 1 is not rewritten here.

4. **Quote coverage (checked).** All nine frozen quotes Q1–Q9 are verbatim in the re-rendered text (my own check:
   Q1–Q9 `FOUND`). The new Q10 and Q11 are verbatim too (the counter reports `QUOTES=11/11` on the candidate).

## Checks run (exact commands and observed output)

- `MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx > man.txt` — rendered; "Linux man-pages 6.19" footer;
  line 84 carries the trailing-symlink O_PATH sentence used for Q10/Q11.
- `sed`-free read of `/usr/include/linux/openat2.h` — `RESOLVE_NO_SYMLINKS 0x04` at line 37 with the comment
  `Block traversal through all symlinks` + line 38 `(implies OEXT_NO_MAGICLINKS) */`; `RESOLVE_NO_MAGICLINKS 0x02`
  at line 35. `grep -c OEXT_` on the header: 1 line (the comment).
- `python3 -B .../controls/candidate-openat2-probe.py --work /fast/scratch/hyaku/chousa-r62/RevC2V2Claim5/p`
  → stdout written to scratch; `diff` against `candidate-openat2-probe.txt` → `IDENTICAL`; exit 0; last line
  `PROBE_FACTS=14/14`; work dir removed by the probe itself.
- Quote check (python, normalised whitespace) against man.txt, the header and the committed probe text: Q1–Q15
  `FOUND` (the Q10/Q11 candidates `True`, 22 and 13 words).
- Counter mirror: `mirror.py` (my script, scratch) imported the frozen `run-c2v2-controls.py` only for `rows_into`
  (no `main()`, `dont_write_bytecode`), copied `corpus/` minus `captures|evidence|fixtures` as the frozen runner does,
  inserted `c2v2-positive-rows.txt`, wrote the entry, and ran
  `python3 -B corpus/evidence/round62/c2v2-count.py --root <mirror> --work <scratch>`:
  - frozen positive entry: `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=9/9 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS`, rc 0 (matches the frozen expectation `positive` PASS);
  - candidate Claim 5 rewrite: `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=11/11 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS`, rc 0.
  - A first mirror that copied only `SOURCES.md` failed `CENSUS=0/1` (census requires every `used-by` path to exist).
    That was my mirror's fault, not the entry's; fixed by copying the corpus tree as the frozen runner does.
- Not run: the full `run-c2v2-controls.py` sweep (it tests the frozen entry's substrings only; it cannot exercise my
  candidate). Not run: any live fetch, any kernel other than this one.

## Residual risk and verification gaps

- Entailment is judged by me, not by the counter. A second non-author reader should read the candidate Claim 5
  against Q2, Q6, Q10, Q11 before closure.
- The counter passing the frozen Claim 5 is evidence of the counter's known limit, not evidence that Claim 5 is sound.
- One kernel, one filesystem, x86_64 (probe) and man-pages 6.19 / linux-api-headers 7.2-1 (quotes) — the entry's
  own limits; unchanged.
- The page's rule that `RESOLVE_NO_SYMLINKS` should be configurable and not set indiscriminately (S138) is not in
  any claim of the entry. Not in Claim 5's scope; noted for L1.

VERDICT: CLAIM5=overreach rewrite_needed=yes
