# ScribeC2Entry2 — round 61, wave w1 — C2 entry candidate (scribe)

Scope: independent draft of `corpus/knowledge/derived-output-safety-r61.md` in the shape read from
`corpus/evidence/round61/c2-count.py`, as a decision table; quotes located by this seat in the
rendered man pages and the S136 file. Draft: `.ufo/waves/round-61/w1/ScribeC2Entry2/entry.md`.
Counter line: `.ufo/waves/round-61/w1/ScribeC2Entry2/counter-output.txt`. Lane files not edited;
the entry was counted only in a scratch mirror.

## Findings

1. **The draft passes the frozen counter on a scratch mirror.** Output:
   `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=10/10 COVERAGE=1/1 CLAIMS=1/1 LIMITS=1/1 CENSUS=1/1 C2=PASS`, exit 0,
   no detail lines (E1).
2. **All ten quotes were located by this seat, not copied from the control.** S134 (open(2)) and S135
   (rename(2)) were rendered with `MANWIDTH=1000 man -l FILE | col -bx` and checked by normalised substring
   search; S136 was read from `.ufo/waves/round-56/w1/R55W2SentBuilder.md`. By content, this seat's Q1–Q6 are
   the control's Q1–Q6, this seat's Q8 and Q10 are the control's Q7 and Q8 (the S136 outcomes). This seat's
   Q7 and Q9 are setup quotes the control does not have: `` `out/spans` symlink → dir `` (S136 line 11, case h2)
   and `span file and `spans.tsv` are symlinks` (line 12, case h3). Claim 5 cites them so the symlink setup
   is quoted rather than only the outcome (E2, E3). Q7 is exactly four words, the counter's minimum.
3. **Five claims, each stated no stronger than its cited quotes.** Checked by hand, not by the counter:
   Claim 1 [Q1,Q2] restates the trailing-versus-earlier component rule; Claim 2 [Q3] restates the O_EXCL
   symlink rule; Claim 3 [Q4] says rename overwrites the link itself; Claim 4 [Q5,Q6] keeps atomicity and
   the both-names window; Claim 5 [Q7–Q10] states only what the h2 and h3 outcomes show, with exit 0. None of
   the claims is a verbatim echo of a quote, so the known echo-claims gap is not exercised by this draft.
4. **Decision table: 8 rows, 4 sourced, 4 not.** Sourced: final-name symlink (H11, H12; S134 Q1, Q3, S135 Q4),
   spans-directory symlink (H10; S134 Q2, S136 Q7–Q8), temporary-name-then-rename (no leg isolates it;
   S134 Q3, S135 Q4–Q6), and the orphan/foreign-span row (H07–H09; S136 Q8, partly). Four rows are leg-only:
   cache symlink (H13), memory (H14, H15, H20), special or unreadable inputs and output-as-file (H16–H19).
   Those rows say "none (leg only)" so a reader does not take a C1 leg for a Linux behaviour.
5. **INFERENCE is marked where the design goes beyond a quote.** Removing the temporary name on the error
   path, the refuse-on-foreign-spans policy, and the check-then-write race are tagged `[INFERENCE]` in the
   table or Limits. None is written into a claim line.
6. **Coverage gap for the temporary-name row.** No C1 leg forces a failure between temporary-name creation
   and the rename. The legs that check a clean output after a refusal (P05 `clean_out`, H17, H18, H19) use
   input faults (absent quote, unreadable input, FIFO, dot path). [INFERENCE from those leg definitions] the
   builder rejects those inputs before it creates a temporary name, so none of them exercises a leftover
   from the rename stage. P01 and P06 compare the full success-path tree byte for byte, so a leftover there
   would show, but only on a successful run.
7. **Counter limits seen in this draft.** The counter checks quote presence and claim citations, not whether a
   claim follows from its quotes; its word-overlap test (≥2 shared five-letter words) is easy to pass.
   The Q7 quote is at the four-word minimum. These are the frozen limits, recorded; they are not changed here.
8. **Mirror preparation was done by hand, not by running the control runner.** I copied the steps of
   `controls/run-c2-controls.py` (`cp -a corpus`, the S136 file, rows inserted after the last row before
   `## Paths`, the draft written at the entry path) and ran the counter on that mirror. I did not run
   `run-c2-controls.py`, so none of its variants (absent, fabricated quote, echo-claims, and so on) were run
   by this seat.

## Evidence

- E1 Counter on mirror (command and output in `.ufo/waves/round-61/w1/ScribeC2Entry2/counter-output.txt`):
  `TMPDIR=/fast/scratch/hyaku/chousa-r61/ScribeC2Entry2 python3 -B …/c2-count.py --root …/mirror` →
  `… QUOTES=10/10 … C2=PASS`, exit 0.
- E2 Quote search (`python3 -B` normalised substring check against rendered pages, rendered with
  `MANWIDTH=1000 LC_ALL=C.UTF-8 man -l /usr/share/man/man2/{open,rename}.2.gz | col -bx`; man-pages 6.19-1):
  Q1 found (20 words), Q2 found (12), Q3 found (21), Q4 found (23), Q5 found (23), Q6 found (19). Grep of the
  rendered text: open(2) line 147 carries Q1 and Q2; line 123 carries Q3; rename(2) line 38 carries Q5 and Q6,
  line 46 carries Q4.
- E3 S136 quotes (python substring check on the whitespace-normalised file): Q7 `` `out/spans` symlink → dir ``
  found (4 words); Q8 found (11); Q9 `span file and `spans.tsv` are symlinks` found (6); Q10 found (11).
  S136 lines: 11–12 (table rows h2, h3), 33–34 (case outcomes).
- E4 Registry rows used: the three rows in `corpus/evidence/round61/controls/c2-positive-rows.txt`, inserted
  into a mirror copy of `corpus/SOURCES.md` after the last row before `## Paths` (lane file not edited).
  Counter reads them as: tier A/A/B, status `mined`, opened `2026-10-28`, used-by the entry path.
- E5 Census: `corpus/SOURCES.md` in the mirror validated by `scripts/sources-census.sh validate` with
  cwd = mirror, exit 0 (the counter's `CENSUS=1/1`).
- E6 Lane state: no lane file edited. The only lane writes are this report, the candidate directory
  `.ufo/waves/round-61/w1/ScribeC2Entry2/` (entry.md, counter-output.txt) and the directory creation.
  `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --short -- corpus/SOURCES.md corpus/knowledge`
  printed nothing (read-only).

## Not run / not claimed

- `run-c2-controls.py` and its twelve variants: not run by this seat (finding 8).
- No counter run on the lane itself: the entry is not in the lane tree and must not be written there by a seat.
- The claims' wording was checked by reading, not by a reviewer; the counter cannot judge it.
- Nothing fetched from the network. The S134/S135 rows carry no URL (access disclosure in the claims file).

## Install / tool record

No installs or updates. `man` and `col` (`/usr/bin/man`, `/usr/bin/col`) and `man-pages 6.19-1` were
already present (`pacman -Q man-pages`). No pacman use.

## Scratch

`/fast/scratch/hyaku/chousa-r61/ScribeC2Entry2/` (mirror, rendered pages) is removed before yield.

VERDICT: ENTRY2_C2=PASS quotes=10 claims=5
