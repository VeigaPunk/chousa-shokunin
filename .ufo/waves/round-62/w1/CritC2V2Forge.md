# CritC2V2Forge — attack on R62-C2 (`corpus/evidence/round62/c2v2-count.py`)

Seat: CritC2V2Forge (critic, leaf). Judged on operability, coverage, calibration.
Counter bytes checked: `sha256sum` prefix `817d5fc0b94e9fc8`, matching the frozen claims. Lane HEAD is `d173d14`
(wave-spec commit, descendant of freeze `388d153`); the counter is unchanged since the freeze.

## Method (what I ran)

1. Mirror built the way `controls/run-c2v2-controls.py` builds it: copy `corpus/` minus `captures`, `evidence`,
   `fixtures`; append `- corpus/knowledge/openat2-resolve-r62.md (round 62)` to `corpus/README.md`; copy
   `candidate-openat2-probe.py` and `.txt`; insert `c2v2-positive-rows.txt` before `## Paths`; write
   `c2v2-positive-entry.md`. Each forge changes only the named piece; the rest is the positive.
2. Counter run read-only: `python3 -B c2v2-count.py --root MIRROR --fleet /home/vgpnk/Projects/shokunin`
   (census script at the fleet default). No lane file was written; `git status --short` in the lane shows only the
   pre-existing untracked wave files.
3. Calibration, run today:
   - `python3 -B corpus/evidence/round62/controls/run-c2v2-controls.py --work <scratch>` → 22 variant lines,
     last line `C2V2_CONTROLS_UNEXPECTED=0`, exit 0 (matches the recorded receipt).
   - Positive mirror → `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=9/9 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1
     PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS`, rc 0.
4. Patched counters (smallest-change candidates) were applied only to copies in scratch, each a single-site
   replacement asserted to match once, and run against the same mirrors.

## Forges that reach C2=PASS on the frozen counter (6 of 6)

**F1 — filler words wrapped around a quote (ECHO class).** Claims 1–9 replaced, one per quote:
`Claim 2. Marmalade pumpkin zebra quartz Disallow resolution of symbolic links during. [Q2]` (the first six words of
each quote, four filler words in front). Counter:
`ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=9/9 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS`, rc 0.
Three filler words are rejected (`ECHO claim has 3 of 11 words outside its quotes: Claim 7...`); four pass. ECHO
counts fresh words only, so any filler above 30 % passes; the forged claims state nothing about their quotes.

**F2 — probe expected value rewritten to match a wrong observation.** In the probe, P04 asks openat2 without
RESOLVE_NO_SYMLINKS: `name(openat2(dfd, "linkdir/f.txt", resolve=0)), "opened")`. Committed output regenerated from
that live run; Q8 rewritten to the new line. Counter:
`PROBE P04 openat2-NO_SYMLINKS-symlink-in-earlier-component observed=opened expected=opened ok` → `C2=PASS`, rc 0.
Entry Claim 2 still says "refused with ELOOP by openat2 with RESOLVE_NO_SYMLINKS" while its own quote Q8 says
`observed=opened`; the counter compares the entry's quotes to the committed file only, not to the claims.

**F3 — probe that prints the committed lines without touching the kernel.** The probe reads and prints
`openat2-probe.txt` and ignores `--work`. Counter: `PROBE_FACTS=14/14`, `PROBE=1/1 ... C2=PASS`, rc 0.

**F4 — source cell naming the entry itself.** S140 source cell gains "(named by corpus/knowledge/openat2-resolve-r62.md
as its own source)". Counter `C2=PASS`, rc 0. `resolve()` tests only that the OWN path is a substring of the cell.

**F5 — README names the path only inside an HTML comment.** The appended README line is
`<!-- corpus/knowledge/openat2-resolve-r62.md -->` with no visible line. Counter `MAP=1/1 ... C2=PASS`, rc 0.
`MAP` is a substring test on the whole file.

**F6 — fake `man` and `col` first on PATH.** Fake `man` `cat`s a forged rendering (the real `man -l` output with two
sentences inverted: "Permit resolution of symbolic links during path resolution." and "Permit the path resolution to
succeed if any component"); fake `col` is `cat`. Entry Q2 and Q4 quote the inverted sentences. Counter `C2=PASS`, rc 0.
Observed: the real page does contain the original Q2 sentence (`True`), so the PASS comes from the shim alone.

k = 6 (F1–F6 all PASS on the frozen counter).

## Smallest counter change per forge (tested on scratch copies; lane not edited)

| Patch | Change (one site) | F-forge now | Positive | Verdict |
|---|---|---|---|---|
| P1 | ECHO: every fresh ≥5-letter word must occur in the cited row's full text | F1 FAIL | **FAIL** (5/5 positive claims: `ECHO-SRC along,anywhere,judges,makes,refuse` … `blocks,caller,describes,...`) | over-rejects; no lexical rule separates F1 |
| P2 | Counter holds its own observed=expected per PROBE id (14 rows = man-implied values) | F2 FAIL | PASS | stops F2 |
| P3 | Probe run under `strace -e trace=openat2`; require ≥10 `openat2(` lines | F3 FAIL (0 lines) | PASS (10 lines) | stops F3; threshold is tight to the candidate's 10 calls, ≥1 also stops F3 |
| P4 | A row whose source cell names the entry does not count (`ENTRY_REL not in r[1]`) | F4 FAIL (`ROW S140 tier=B status=mined opened=2026-10-28 used_by_entry=True resolves=True`) | PASS | stops F4 |
| P5 | `MAP` tests the README with `<!--...-->` stripped | F5 FAIL | PASS | stops F5 |
| P6 | `render_man` runs `/usr/bin/man` and `/usr/bin/col` by absolute path | F6 FAIL (`QUOTE Q2 S138 words=12 found=False anchor_ok=True`) | PASS | stops F6; INFERENCE: a root-owned path is still replaceable by a writer to /usr/bin, so pinning the binary's sha256 is the stronger form |

Patch outputs for all seven mirrors (pos, F1–F6) were run once with the driver in scratch (`forge.py`, `patches.py`); the scratch is deleted, so the method above is the reproduction recipe.
P1 is the only patch with a regression, and it is the reason F1 is not closed by counting: the unsourced-word count
for F1 is 4 per claim, while the positive's claims 1–5 carry 5, 6, 5, 7 and 11 (INFERENCE: no cap separates them).

## named_in_claims

`claims.md` names one class that these forges fall into: the "non-sequitur" limit — "a claim that adds words but does not
follow from its quote still reaches PASS" and "entailment is not machine-checked". F1 is that class → named (n counts it).
F2–F6 are not named: `grep -n -i` over `claims.md` finds no mention of probe expectations, PATH shims, HTML comments,
source cells naming the entry, or a probe that prints its input. F2's Claim-2 contradiction sits inside the entailment
limit at claim level, but its mechanism (the probe's `expected=` column is the probe's own) is not named; I count it
under F2, not the limit. Strict count: n = 1.

## Routed to the closure

- F1: entailment, not counting. The closure read should check claims against quotes for words absent from every
  cited source (here "marmalade pumpkin zebra quartz" in all nine claims).
- F2, F4, F5: patch P2, P4, P5 are small and pass the positive; recommend folding them into the next round's battery.
- F3, F6: patch P3 and P6 pass the positive; P3's threshold needs a note against the 10-call candidate.
- Not run: the full v2 battery (c1v2) and any other counter; these findings are C2 only.

## Install / tool record

No tools installed or upgraded. Used host `strace` (`/usr/bin/strace`), `man`, `col`, Python 3.14.8 — existing.
Scratch `/fast/scratch/hyaku/chousa-r62/CritC2V2Forge/` (mirrors, patched copies, driver logs) is deleted before yield.

VERDICT: C2_FORGES_REACHING_PASS=6 named_in_claims=1
