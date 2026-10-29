# ScribeGate — round 62, wave w1 — gate for S138–S140

Draft: `.ufo/waves/round-62/w1/ScribeGate/gate.md`. Date 2026-10-28. Offline: no URL fetched, no lane write
outside my own directory, no git. Nothing was committed or added to `corpus/SOURCES.md`.

## Findings

1. **S138 (openat2(2), man-pages 6.19) — ADMIT, tier A.** Re-rendered the installed page; Q1–Q5 of the entry are
   verbatim in the render. Teaches quote: "which affects the handling of symbolic links only in the final component of
   path" (14 words), roff lines 335–341, rendered line 86. Correction for L1: the row's date "2026-02-08" is not on the
   page. The page's `.TH` date is 2026-07-02 (roff line 6); the package build date is 2026-08-27.
2. **S139 (linux/openat2.h, linux-api-headers 7.2-1) — ADMIT, tier A.** Quote "Block traversal through all symlinks
   (implies OEXT_NO_MAGICLINKS)" at header lines 37–38, verbatim. Two corrections for L1: the teaches cell says
   "one-line meaning"; every RESOLVE_* comment wraps to two lines. And line 38 names `OEXT_NO_MAGICLINKS`, which the
   header never defines (`RESOLVE_NO_MAGICLINKS`, line 35). Entry Claim 5 must not treat that name as an identifier.
3. **S140 (own-work probe output) — ADMIT, CONDITIONAL, tier B.** The row cannot resolve yet: neither
   `corpus/evidence/round62/openat2-probe.txt` nor `openat2-probe.py` exists in the lane tree (see Evidence).
   The candidate reruns to byte-identical output on this host today. Teaches quote: "PROBE P04
   openat2-NO_SYMLINKS-symlink-in-earlier-component observed=ELOOP expected=ELOOP ok" (6 words), candidate output line 7.
   Conditions: (a) L1 commits script and output byte-identical to the candidate; (b) the scope cell must say the
   `expected=` values are the lane author's constants (candidate script lines 84, 92, 99, 128 are typed by hand),
   so `PROBE_FACTS=14/14` measures agreement with the author, and the observed lines carry the evidence; (c) P02's
   os.open expectation rests on open(2) (row S134, `corpus/SOURCES.md` line 144), not on openat2(2).
4. **Proposed REJECTED row S141** (id for L1): the candidate probe's module docstring, lines 7–8, claims that a
   PROBE_FACTS match means "the result the openat2(2) page states or implies". The page has no os.open or Python text
   (0 hits), so that claim does not hold for P01–P03 and P11. Same class as the existing S137 rejection: own-work
   docstring is intent, not evidence.
5. **Blocking for C2 at integration:** the counter's ROWS (`S140` source resolves) and PROBE checks fail until the
   S140 files are committed. The counter was not run by me (the entry is absent; running it would only reproduce FAIL).
6. **Non-blocking, INFERENCE:** the 6.19 page documents `OPENAT2_REGULAR (since Linux 7.2)` (rendered line 42), so the
   page text is newer than its version label. The row scope "what man-pages 6.19 states" remains accurate as written.

Not claimed: entailment (whether each claim follows from its quotes) — reviewer judgment, per the counter's named limit.

## Evidence (commands and observed output)

- `MANWIDTH=1000 LC_ALL=C.UTF-8 man -l /usr/share/man/man2/openat2.2.gz | col -bx` → 171 lines, exit 0; footer
  `Linux man-pages 6.19`. `zcat ... | head -3` → `.\" Copyright 2019, Aleksa Sarai`; `zcat ... | grep -n` → line 6
  `.TH openat2 2 2026-07-02 "Linux man-pages 6.19"`, line 25 `glibc provides no wrapper for`, line 187 "The primary use
  case...", line 196 "Do not permit...", line 312 "Disallow resolution...", line 341 "which affects the handling...".
- Quote check (python in scratch, counter's normalisation: `norm(quote) in norm(source)` and anchor in row anchor cell):
  Q1 words=24 found=True anchor_ok=True; Q2 12/True/True; Q3 14/True/True; Q4 24/True/True; Q5 11/True/True;
  Q6 words=7 found=True anchor_ok=True; Q7 6/True/True; Q8 6/True/True; Q9 6/True/True. All 9 entry quotes pass the
  counter's word-count, presence and anchor tests on my re-read sources. The counter itself was not run.
- `grep -n "OEXT_\|RESOLVE_NO_MAGICLINKS\|^#define" /usr/include/linux/openat2.h` → line 35 defines
  RESOLVE_NO_MAGICLINKS, line 38 contains `(implies OEXT_NO_MAGICLINKS)`; no other OEXT_ occurrence.
- Candidate probe re-run: `python3 -B corpus/evidence/round62/controls/candidate-openat2-probe.py --work
  /fast/scratch/hyaku/chousa-r62/ScribeGate/probe-work` → exit 0; `diff controls/candidate-openat2-probe.txt <stdout>`
  → no output (SAME_AS_CANDIDATE); the output reads `KERNEL 7.2.11-arch1-1`, `PYTHON 3.14.8`, `PROBE_FACTS=14/14`.
  Scratch work dir removed by the probe itself and again by me.
- `ls corpus/evidence/round62/ | grep -i openat2` → no output, exit 1 (S140 files absent).
- `grep -c "os.open\|Python\|states or implies" openat2.man.txt` → 0.
- Build dates read from `/var/lib/pacman/local/{man-pages-6.19-1,linux-api-headers-7.2-1}/desc` (file read, not a
  pacman call): `%BUILDDATE%` 1787839958 (2026-08-27), 1786956356 (2026-08-17).
- `pacman -Q man-pages linux-api-headers` → `man-pages 6.19-1`, `linux-api-headers 7.2-1` (read-only query; no
  transaction, no install, no upgrade). Tools installed by me: none.

## Spot-check request (non-author to re-open)

- **Admit:** S138 Q3 — `zcat /usr/share/man/man2/openat2.2.gz | sed -n '335,341p'`; the sentence must contrast
  RESOLVE_NO_SYMLINKS (all components) with O_NOFOLLOW (final component only).
- **Reject:** S141 — `controls/candidate-openat2-probe.py` lines 7–8 against lines 84, 92, 99, 128; and
  `MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx | grep -c "os.open\|Python"` must print 0.

## Scope held

No frozen file read-modified (claims, counters, battery, controls, `tools/`, `SKILL.md`, `corpus/`). Writes: this
report, `ScribeGate/gate.md`. Scratch `/fast/scratch/hyaku/chousa-r62/ScribeGate` removed before yield.

VERDICT: GATE_ROWS_WRITTEN=3/3 quotes_reopened=10
