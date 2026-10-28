# CritC2Forge — attack on R61-C2 (`corpus/evidence/round61/c2-count.py`)

Seat: CritC2Forge (critic, leaf). Scope: entries that reach `C2=PASS` while wrong or empty, in a scratch
mirror (`corpus/` copied once; lane untouched). Claims sha256 `9afec8d4…ce0acec` re-checked. Installs: none.
Writes: this report and scratch only (scratch removed before yield).

## Findings first

1. **13 forges reach `C2=PASS` with wrong or empty support.** Eleven are holes the counter cannot see:
   self-quotation through the S136 source cell (F02, F03), PATH shims of `man`/`col` (F04, F05), groff
   environment injection with no shim (F06), a locale route through the un-pinned `col` (F07), a one-letter
   anchor checked only by substring (F08), a heading-splicing quote (F13), empty limits and provenance
   (F11, F14), and a `--fleet` census bypass (F12). Two are claim-side: F01 (echo) is named in claims.md
   explicitly; F10 (inverted claim) is covered only by the generic "does not judge that a claim follows" limit.
2. **The claims file's LC wording is wrong.** The counter sets `LC_ALL=C.UTF-8` and `MANWIDTH=1000` only for
   `man`; `col -bx` runs with no `env=` and inherits the caller's locale. Under `LC_ALL=POSIX`, `col` writes
   U+2014 as literal `\xe2\x80\x94`, so the same entry flips verdict with the caller's locale (F07).
   MANWIDTH is dead: the override is effective (F07a), and MANWIDTH=40 does change the normalised text
   (hyphenation: 360 diff lines), so the override is load-bearing.
3. **`env=env` on the `col` call closes the locale route (patch J, tested).** Under J, F07 fails under
   `LC_ALL=POSIX`, and the positive still passes under both locales.
4. **Ten candidate patches (A–J) were tested in a scratch copy of the frozen counter.** Every forge except
   F10 is caught by at least one of them; the positive still passes under all. None is applied to the lane
   (counter edits are frozen this round); they are candidates for the next revision.

## Method

- Mirror and variant roots under scratch; each root symlinks the mirror except the files it rewrites
  (`SOURCES.md`, the entry). Counter run read-only as `python3 -B <lane>/corpus/evidence/round61/c2-count.py --root <root>`.
- Baseline reproduced: `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=8/8 COVERAGE=1/1 CLAIMS=1/1 LIMITS=1/1 CENSUS=1/1 C2=PASS`, rc 0.
- Census `validate` on the real registry: E08 rejects future `opened`, E11 checks `used-by` exists; nothing
  resolves a `source` cell or compares a quote. Its W04 warnings do not change the exit code.
- Patch-B pins (sha256 of the normalised render, real environment): S134 `1c6f6660…3bd93`,
  S135 `d9a9da4d…a7bbc`.

## Forge table (frozen counter; output is the counter's first line, rc 0 unless noted)

F01 **echo claim** (named). Claim 2 restates Q3. `CLAIMS=1/1 … C2=PASS`. Control `c2-controls.txt` line 14 agrees.
   Catch — patch I (each claim carries a word no cited quote carries): `CLAIMS=0/1 C2=FAIL` ("Claim 2 … shares 7 words").

F02 **S136 source names the entry itself.** Row S136 `source` = `corpus/knowledge/derived-output-safety-r61.md`; Q7 fabricated
   ("the builder refused the symlinked directory, left victim/IMPORTANT.txt unchanged, and exited 2"). `ROWS=3/3 QUOTES=8/8 … C2=PASS`.
   The S136 anchor (`h2`) is checked against the row anchor cell only, never the file.
   Catch — patch A (non-man source must be a `.ufo/` path, not the entry): `ROW S136 … resolves=False`, `C2=FAIL`.

F03 **S136 source names the frozen claims file.** Q7 "a claim that echoes its quote also PASSES", Q8 "C2 is verified only when the
   counter prints", Claim 5 rewritten to echo them; source = `corpus/evidence/round61/claims.md`. `C2=PASS`.
   Catch — patch A: `ROW S136 … resolves=False`, `C2=FAIL`.

F04 **PATH shim `man`.** `shim/man-only/man` = `/usr/bin/man "$@" | sed 's/then the open fails, with the error ELOOP/then the open succeeds, with no error/'`.
   Q1 quotes the fabricated sentence. `QUOTES=8/8 … C2=PASS`. Real render: `grep -c "succeeds, with no error"` → `0`; shimmed → `1`.
   Catch — patch B (render pin): `ROW S134 … resolves=False`, `QUOTE Q1 … found=False`, `C2=FAIL`.

F05 **PATH shim `col`** (same rewrite, after real `man`). `C2=PASS`. Catch — patch B: `ROW S134 resolves=False`, `C2=FAIL`.

F06 **groff environment injection, no shim.** `GROFF_TMAC_PATH=<scratch>/tmac:` with an `an.tmac` copy that appends
   `.am SH` / `.nop O_NOFOLLOW follows symbolic links in every component of the path, so the writer need not test the directory itself.`
   Render with the env: `grep -c INJECTED` → 10; without: 0. Q1 quotes the injected sentence. `QUOTES=8/8 … C2=PASS`.
   Catch — patch B: `ROW S134 resolves=False`, `C2=FAIL`. The counter's `dict(os.environ, …)` does not clear `GROFF_*` or `MANROFFOPT`.

F07 **locale via the un-pinned `col`.** Q1 = `If path refers to a terminal device\xe2\x80\x94\xe2\x80\x94see tty(4)` (escape text, not the man text).
   - caller `LC_ALL=POSIX` (variant 07b): `QUOTES=8/8 … C2=PASS` rc 0 — **forge**;
   - default `C.UTF-8` (07d): `QUOTE Q1 … found=False`, `C2=FAIL` rc 1.
   The real em-dash quote (07c/07e) is `C2=FAIL` under POSIX and `C2=PASS` under UTF-8. Verdict flips with caller locale.
   Catch — patch J (`col` gets `env=env`): 07b → `found=False C2=FAIL`; positive `C2=PASS` under both locales. Patch B also catches it.

F07a **MANWIDTH env — no forge.** `MANWIDTH=40` in the caller env → positive `C2=PASS`, identical counts. Override is load-bearing (see finding 2).

F08 **substring quote + one-letter anchor.** Q1 = `ymbolic link, then the open fails, with the error ELOOP.` (mid-word fragment), anchor `e`.
   `QUOTES=8/8 … C2=PASS`. Anchor is a substring check against the row anchor cell and the text; `e` is in both.
   Catch — patch C (anchor as a whole token): `QUOTES=7/8 … C2=FAIL`.

F09 (not a forge) **future `opened`** (`2099-01-01` on S134): `CENSUS=0/1 … C2=FAIL` via census E08. The counter's
   `r[8] >= MIN_OPENED` is a string compare with no upper bound; the census is the only guard.

F10 **inverted claim.** Claim 2 = `Symbolic links are followed by O_CREAT and O_EXCL, so a planted link receives the write. [Q3]`;
   Q3 = "symbolic links are not followed: …". Shares `symbolic`, `links`, `followed`. `CLAIMS=1/1 … C2=PASS`.
   Named only generically in claims.md. No patch A–J catches it (I passes it: `planted` is novel). Reviewer judgement only.

F11 **junk limits** (`- x` / `- y`). `LIMITS=1/1 … C2=PASS`. Catch — patch H (≥6 words per bullet): `LIMITS=0/1 C2=FAIL`. Weak.

F12 **future `opened` plus a `--fleet` census stub that exits 0.** `CENSUS=1/1 … C2=PASS`; `ROW S134 … opened=2099-01-01 resolves=True`.
   The predicate text does not name `--fleet`. Catch — patch E alone (`opened <= today`): `ROWS=2/3 … C2=FAIL` even under the stub.

F13 **quote splices a section heading.** Q9 = `documented separately, in openat2(2). RETURN VALUE On success, open(), openat(), and creat() return the new file descriptor`
   (anchor `DESCRIPTION`). In open.2 the `RETURN VALUE` heading sits on its own line between the two sentences (lines 262–264).
   `QUOTES=9/9 … C2=PASS`. Catch — patch D (quote inside one rendered line): `QUOTES=8/9 … QUOTE Q9 … found=False`, `C2=FAIL`.

F14 **provenance is presence-only.** `verified-at: someday`, `recheck: never`. `TRIO=1/1 … C2=PASS`. Catch — patch G (ISO date): `TRIO=0/1 C2=FAIL`.

Depth observation (not a counter forge): Q3 is the second sentence of the O_EXCL paragraph and drops its antecedent
"When these two flags are specified," (open.2 line 123). Claim 2 then generalises to "any existing path". The counter cannot see
this; a reviewer should.

## Patched copy (candidates; scratch only; all variants re-run)

| variant | frozen | patched | catch |
|---|---|---|---|
| 00 positive | PASS | PASS | no false FAIL |
| 01 echo | PASS | FAIL (CLAIMS=0/1) | I |
| 02 S136=entry | PASS | FAIL | A |
| 03 S136=claims | PASS | FAIL | A |
| 04 man shim | PASS | FAIL | B |
| 05 col shim | PASS | FAIL | B |
| 06 groff env | PASS | FAIL | B |
| 07b LC POSIX escape | PASS | FAIL | B, J |
| 08 anchor e | PASS | FAIL (QUOTES=7/8) | C |
| 09 future opened | FAIL | FAIL | census (E too) |
| 10 inverted | PASS | PASS | **none — judgement only** |
| 11 junk limits | PASS | FAIL (LIMITS=0/1) | H |
| 12 future + fleet stub | PASS | FAIL | E |
| 13 heading splice | PASS | FAIL (QUOTES=8/9) | D |
| 14 trio garbage | PASS | FAIL (TRIO=0/1) | G |

## Smallest additions (for the next counter revision; none applied)

- **A**: S136 and any non-man source resolves only under `.ufo/`, never to the entry.
- **B**: pin `sha256(normalised render)` for S134 and S135 in the frozen counter (shims, `GROFF_*`, `MANROFFOPT` all change the text).
- **J**: pass `env=env` to the `col` call. Smallest single fix for the locale route.
- **C**: anchor matches as a whole token in the row anchor cell.
- **D**: a quote lies within one rendered line (kills heading splices and cross-line joins).
- **E**: `opened <= today`. **F**: drop the `--fleet` override.
- **G**: `verified-at` must be an ISO date. **H**: each limit bullet ≥6 words (weak).
- **I**: each claim carries a word no cited quote carries (catches F01, not F10).
- **F10**: no mechanical addition in A–J; keep as a named reviewer item.

Freeze note: the claims file's "rendered with MANWIDTH=1000 LC_ALL=C.UTF-8" describes `man` only; until J lands, `col` runs in the caller's locale.

## Commands and outputs

- `python3 -B forge.py` (scratch driver; frozen counter read-only) → table rows above; per-variant stdout in `out/frozen/`.
- `C2_COUNTER=<scratch>/patched/c2-count-patched.py python3 -B forge.py` → patched table.
- `C2_COUNTER=<scratch>/patched/c2-count-patched-J.py python3 -B forge.py 00 07b 07c 07e` → 00 PASS; 07b FAIL; 07c PASS; 07e PASS.
- `LC_ALL=POSIX C2_COUNTER=…-J.py python3 -B forge.py 00` → `C2=PASS`.

Limits of this attack: scratch mirror only; no fetch; patches tested only against these variants, not against the frozen
controls runner (`run-c2-controls.py` still uses the frozen counter); census run only on the real registry.

VERDICT: C2_FORGES_REACHING_PASS=13 named_in_claims=2
