# ScribeC2V2Entry1 — round 62, wave w1 — C2 entry draft (scribe)

Seat: scribe, leaf. Scope: an independent draft of `corpus/knowledge/openat2-resolve-r62.md` in the shape read by
`corpus/evidence/round62/c2v2-count.py`, as a practitioner's checklist. The draft is at
`.ufo/waves/round-62/w1/ScribeC2V2Entry1/entry.md` (45 lines, 5886 bytes, sha256 prefix `4098de1c7e0a0912`).
No lane file other than my report and draft was written; no frozen counter, battery, control, SOURCES or
knowledge file was touched; no git mutation; no install; no network.

## Findings

1. **The draft passes the frozen C2 counter on a scratch mirror.** Counter output (rc 0):
   `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=13/13 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS`.
   Quotes per row: S138 9 (Q1–Q9), S139 1 (Q10), S140 3 (Q11–Q13). Claims 8, every quote cited by at least one claim.
   The mirror was built by `mirror_draft.py` (scratch), which copies the runner's steps (`run-c2v2-controls.py`
   lines 45–60): lane corpus minus captures/evidence/fixtures, README map line, `candidate-openat2-probe.py/.txt`,
   `c2v2-positive-rows.txt` inserted before `## Paths`, and my draft as the entry. It did **not** run the runner's variants.
2. **Quotes re-opened by me, not copied from the positive control.** S138 rendered page (171 lines, 1985 words),
   S139 header (50 lines), S140 candidate probe output (18 lines). Each quote's wording was located in those files
   (commands and hits in Evidence §A). Q9 and Q7/Q8 were taken from the page's ERRORS block.
3. **Two quotes failed my first pass and were fixed (honest iteration record).** Run 1: `QUOTES=12/14 COVERAGE=0/1
   CLAIMS=0/1 ECHO=0/1 C2=FAIL` — Q6 anchor `glibc wrapper` is in the row's anchor cell but not in the man-page text
   (text says "glibc provides no wrapper"), so anchor changed to `glibc`; Q11 anchor `define block` is not in the
   header text, so that BENEATH-comment quote was dropped. Run 2: `ECHO=0/1` — claim 6 had 5 of 17 words outside its
   quotes; reworded. Final run: 13/13, ECHO passes at every claim (Evidence §C).
4. **Claims are kept to the quotes; inference is marked.** Two limits are marked `[INFERENCE]` in the entry (the
   check-then-write narrowing; the claim order as "one practitioner's sequence"). One claim half is my inference and
   is not marked in the entry: Claim 7's "so a caller that sets it gets the magic-link refusal too" reads "implies
   RESOLVE_NO_MAGICLINKS" (Q2) as consequence; reviewers should judge it. Claim 6 deliberately does not say EAGAIN
   retry is for racing walks — Q9 carries only "The caller may choose to retry the openat2() call." The entry's
   Limits say the EAGAIN retry is not exercised by the probe.
5. **Header/man-page disagreement, observed.** The header's RESOLVE_NO_SYMLINKS comment names
   `OEXT_NO_MAGICLINKS` (line 38), a macro the header never defines; `RESOLVE_NO_MAGICLINKS` is defined on line 35.
   The man page says `RESOLVE_NO_MAGICLINKS` (Q2). The entry takes the name from the man page and says so in Limits.
   Not a counter issue; a candidate for L1's reading of S139's "one-line description" cell.
6. **Lane tree is not ready for a lane-root run (read-only observation).** `corpus/knowledge/openat2-resolve-r62.md`
   is absent; `corpus/evidence/round62/openat2-probe.py` and `openat2-probe.txt` are absent (only `controls/candidate-*`
   exist); `corpus/SOURCES.md` has 0 lines containing `S138` (openat2 appears only in the Leads area, line 326). So
   `c2v2-count.py` on the lane root cannot pass until L1 lands the rows, the probe pair and the entry. I did not run
   the counter on the lane root (its census call uses the lane as cwd).
7. **Live probe reproduces the committed-candidate output on this host.** The counter's PROBE step re-ran the probe
   in the mirror and matched the candidate's `PROBE`/`HEADER`/`PROBE_FACTS` lines: `PROBE=1/1` (14/14 facts,
   kernel 7.2.11-arch1-1, Python 3.14.8, x86_64).
8. **Not checked by me:** entailment (the counter does not judge it); the controls runner (`run-c2v2-controls.py`,
   not my item); other kernels, filesystems, architectures.

## Evidence

§A. Quote location (re-opened sources)
- `MANWIDTH=1000 LC_ALL=C.UTF-8 man -l /usr/share/man/man2/openat2.2.gz | col -bx > S138.txt` → 171 lines, 1985 words.
- `grep -n -i -E "primary use case|Disallow resolution|any component|not a descendant|glibc provides|...|ELOOP|EXDEV|...|Linux 5.6|..." S138.txt`
  hits (line numbers): 18 "Note: glibc provides no wrapper for openat2(), necessitating the use of syscall(2)."; 52 "The primary
  use case ... are resolved."; 55 "Do not permit the path resolution to succeed if any component ... indicated by dirfd."; 82
  "Disallow resolution of symbolic links during path resolution. This option implies RESOLVE_NO_MAGICLINKS."; 86 "Note that the
  effect of the RESOLVE_NO_SYMLINKS flag, which affects ... only in the final component of path."; 108–109 EAGAIN text
  ending "The caller may choose to retry the openat2() call."; 123 "ELOOP  how.resolve contains RESOLVE_NO_SYMLINKS, ..."; 127
  "EXDEV  how.resolve contains either RESOLVE_IN_ROOT or RESOLVE_BENEATH, ..."; 136–138 "HISTORY / Linux 5.6.".
- `cat -n /usr/include/linux/openat2.h` → line 35 `#define RESOLVE_NO_MAGICLINKS 0x02`, lines 37–38
  `#define RESOLVE_NO_SYMLINKS 0x04 /* Block traversal through all symlinks` / `(implies OEXT_NO_MAGICLINKS) */`.
- `grep -n OEXT /usr/include/linux/openat2.h` → `38: (implies OEXT_NO_MAGICLINKS) */` (only hit).
- `candidate-openat2-probe.txt` lines 5, 7, 4 hold the quoted P02, P04, P01 text; P02 `observed=opened`, P04 `observed=ELOOP`, P01 `observed=False`.

§B. Counter runs (mirror `mirror_draft.py` → `c2v2-count.py --root <mirror> --work <cw>`, `TMPDIR` set to scratch)
- Run 1 (draft v1): rc 1, `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=12/14 COVERAGE=0/1 CLAIMS=0/1 ECHO=0/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=FAIL`;
  details `QUOTE Q6 S138 words=12 found=True anchor_ok=False`, `QUOTE Q11 S139 words=13 found=True anchor_ok=False`.
- Run 2 (draft v2): rc 1, `QUOTES=13/13 ... ECHO=0/1 ... C2=FAIL`; detail `ECHO claim has 5 of 17 words outside its quotes: Claim 6.`
- Run 3 (final draft): rc 0, `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=13/13 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS`.
- Run 4 (final draft, same mirror, fresh work directory `cw3`): same line, rc 0. Two runs agree; this is not a determinism proof.

§C. Claim margins (the counter's own `words()` and `section()` imported read-only with `python3 -B`, final draft)
- Shared words ≥2 for every claim (range 4–10); fresh-word share per claim: C1 47%, C2 55%, C3 69%, C4 52%, C5 40%,
  C6 50%, C7 64%, C8 67% (threshold 30%, minimum 3). Tightest: C5 (6 of 15 fresh).
- Quote word counts (4–25 allowed): Q1 24, Q2 12, Q3 22, Q4 14, Q5 24, Q6 12, Q7 16, Q8 17, Q9 9, Q10 8, Q11 6, Q12 6, Q13 6.

§D. Lane state (read-only, `git -C <lane> status --short -- corpus` empty; `ls`, `grep` as in Findings 6)

## Out-of-scope items (for L1)
- Lane needs the S138–S140 registry rows, the probe script and output under `corpus/evidence/round62/`, the entry at
  `corpus/knowledge/openat2-resolve-r62.md`, and the README map line before a lane-root C2 run can pass.
- If L1 keeps this draft, the lane's own run of the controls runner is the place to see the variant set; I did not run it.
- The draft's quote Q10 is the only S139 quote; it passes the counter's minimum of 1 (S139) but is thin for the
  "read the values from the header" point; a second header quote would need an anchor the S139 row contains.

## Tooling record
- Installed or upgraded: none. Used present tools only: `man`, `col`, `python3` (3.14.8 per probe), `grep`, `sed`, `git` (read-only).

## Cleanup
- Scratch `/fast/scratch/hyaku/chousa-r62/ScribeC2V2Entry1/` removed at yield (mirror, `S138.txt`, counter work dirs).

VERDICT: ENTRY1_C2=PASS quotes=13 claims=8
