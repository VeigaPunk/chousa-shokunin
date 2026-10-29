# RevC2V2Claim4 — entailment review of Claim 4 (round 62, C2)

Scope: Claim 4 of `corpus/evidence/round62/controls/c2v2-positive-entry.md` (sha256 prefix `3c0bff8219fb41e0`),
and the landing candidate. Claims 1–3 and 5 were not reviewed. Lane revision: frozen `388d153519a3` is an
ancestor of HEAD `d173d144bbf5`; `git show 388d153519a36a4c3f34d56d034870f032865a70:…/c2v2-positive-entry.md`
holds the same Claim 4 text, and `git diff --stat` of `corpus/evidence/round62/controls/` between the frozen
revision and HEAD is empty. No lane file was written; scratch removed before yield; no tool installed.

## Findings

1. **Claim 4 is contradicted on the probe host (overreach, factual).** Claim 4 says "because glibc has no wrapper"
   and "needs ctypes or another route to syscall(2)". The only quote for the glibc premise (Q5, S138) is the
   man-pages 6.19 SYNOPSIS note. On this host the installed glibc exports an openat2 wrapper; a ctypes call to it
   works. Evidence:
   - `ldd --version` → `ldd (GNU libc) 2.44`
   - `nm -D --defined-only /usr/lib/libc.so.6 | grep -i openat2` → `0000000000112aa0 W openat2@@GLIBC_2.43`
   - `readelf --dyn-syms --wide /usr/lib/libc.so.6 | grep -i openat2` → `FUNC WEAK DEFAULT 13 openat2@@GLIBC_2.43`
   - `ctypes.CDLL('libc.so.6').openat2` → `hasattr` True; a direct `libc.openat2(AT_FDCWD, <scratch file>, how, size)`
     returned fd >= 0.
   The page is dated (`2026-02-08`); the entry says so only for the quotes in its Limits, not in Claim 4. Whether
   the note predated glibc 2.43 is `[INFERENCE]` (no network; symbol version only). The claim as written states a
   present-tense glibc fact the host refutes.

2. **"ctypes" is not in the quote set (entailment gap).** Q5 says "necessitating the use of syscall(2)"; Q9
   (`PROBE P01 python-os-has-openat2 observed=False expected=False ok`) says nothing about ctypes. The probe source
   uses ctypes (`candidate-openat2-probe.py:45`), but the committed output (S140) does not name it, so no quote can
   carry it. "needs" is absolute; "or another route" is a weak hedge that does not restore support.

3. **Host scope dropped on the first half.** "Calling openat2 from Python 3.14.8 needs …" states a one-host result
   (kernel 7.2.11, Python 3.14.8, one build) as a general fact about that Python version. Only the second half
   ("the os module exposes no openat2 function in the probe") carries the hedge. The Q9 observation itself is
   correct: `probe()` at `candidate-openat2-probe.py:85` records `hasattr(os, "openat2")` as observed.

4. **The second half is supported.** Q9 (`observed=False`) matches the probe rerun below; "on this host" is the right
   scope. The `expected=False` in Q9 is the author's hard-coded expectation (`probe(..., False)`), not a page
   statement; it is not evidence of Python's behaviour beyond this host.

5. **The counter passes the claim anyway (calibration).** The unmodified claim reaches `C2=PASS`
   (`mirror.py` run below), as the counter's named limit predicts for non-sequitur text. The failure here is not
   a non-sequitur: the premise is stale on this host, and the entry's Limits do not disclose the glibc version.
   Entailment and fact review by a non-author reviewer is the only check that catches it.

6. **Adopting a rewrite breaks a frozen control (decision for L1).** `controls/run-c2v2-controls.py:109` builds the
   `non-sequitur` variant by substituting the exact original Claim 4 string into the positive entry through `sub()`,
   which asserts `t.count(a_) == 1` (line 83). Confirmed: the original string occurs once in the controls script
   and zero times in my rewrite. Replacing Claim 4 in the positive entry makes that control raise AssertionError
   instead of printing a line. Controls are frozen; I did not edit them. L1 must choose: keep the frozen Claim 4
   text and record the defect as a limit, or re-freeze the control.

## Rewrite (quote set unchanged: Q5, Q9)

Replace the Claim 4 line of `c2v2-positive-entry.md`:

    Claim 4. Man-pages 6.19 says glibc provides no openat2 wrapper, so callers use syscall(2) instead; on this host the os module of Python 3.14.8 exposes no openat2 function. [Q5, Q9]

Entailment, sentence by sentence against the quotes: "Man-pages 6.19 says glibc provides no openat2 wrapper,
so callers use syscall(2) instead" follows from Q5 ("glibc provides no wrapper for openat2(), necessitating the
use of syscall(2)") with the date attributed to row S138 (Linux man-pages 6.19). "on this host the os module of
Python 3.14.8 exposes no openat2 function" follows from Q9 at host scope. Nothing about ctypes; no "always",
"any" or "all".

Add one Limits bullet (the Limits section already has an `[INFERENCE]` bullet, so the LIMITS check is unaffected):

    - glibc 2.44 on the probe host exports openat2 as a weak function at GLIBC_2.43 (`nm -D --defined-only /usr/lib/libc.so.6`), a libc entry point the 6.19 SYNOPSIS note does not cover; the committed probe does not call it.

## Evidence

- Man page rendered: `MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx` → line 18:
  `Note: glibc provides no wrapper for openat2(), necessitating the use of syscall(2).`; line 52 (primary use case,
  Q1); line 82 (Q2 symlink wording). Q5 text matches.
- Header `/usr/include/linux/openat2.h`: RESOLVE_NO_SYMLINKS `0x04`, comment "Block traversal through all symlinks
  (implies OEXT_NO_MAGICLINKS)" (Q6 matches). The header says nothing about glibc or Python, so it bears on no
  part of Claim 4.
- Probe rerun: `python3 -B candidate-openat2-probe.py --work <scratch>/p` → `PROBE_FACTS=14/14`, exit 0; stdout
  `diff` against `candidate-openat2-probe.txt` → identical (`SAME_AS_COMMITTED`). P01 `observed=False`.
- `python3 -B -c "import os; print(hasattr(os,'openat2'))"` → `False` (Python 3.14.8).
- Counter on mirror of the unmodified positive entry (mirror prepared as `run-c2v2-controls.py` does; my
  copy in scratch): `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=9/9 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1
  MAP=1/1 CENSUS=1/1 C2=PASS`, rc=0.
- Counter on mirror of the rewrite (Claim 4 replaced, same quotes): identical line, `C2=PASS`, rc=0.
- Counter on mirror of the rewrite plus the Limits bullet: identical line, `C2=PASS`, rc=0.
- Mirror prep: the lane is read-only here; `mirror.py` copies `corpus` (ignoring captures/evidence/fixtures) into
  scratch, appends the README map line, inserts `c2v2-positive-rows.txt` into `SOURCES.md`, and runs
  `c2v2-count.py --root <mirror> --work <scratch>/probe-work`.

## Limits of this review

- One host: glibc 2.44, kernel 7.2.11, Python 3.14.8, one filesystem. The glibc export was checked by symbol table
  and one ctypes call, not by reading the glibc source or NEWS (no network, no docs installed).
- The openat2 wrapper's effect on errno/flags was not probed; the rewrite does not claim anything about it.
- `c2v2-count.py` was run only on mirrors. The frozen `run-c2v2-controls.py` was not rerun (it reads the unmodified
  positive entry, which is unchanged).

VERDICT: CLAIM4=overreach rewrite_needed=yes
