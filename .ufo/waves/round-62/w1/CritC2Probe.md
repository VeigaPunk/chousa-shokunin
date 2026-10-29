# CritC2Probe: attack on controls/candidate-openat2-probe.py (C2 probe)

Scope: the 14 `expected` values, operability, coverage, calibration. Frozen files were read only. Nothing under the lane was written. Scratch `/fast/scratch/hyaku/chousa-r62/CritC2Probe/` was removed (verified). Tools: none installed; `python3` 3.14.8, `man`/`col`, `unshare -Urm` (user+mount namespace, no sudo). Host: kernel 7.2.11-arch1-1, uid 1000, `/fast` is xfs. Lane is btrfs; I did not run on btrfs (scratch rule); btrfs untested.

## 1. Source per expectation (openat2(2) = `man -l` with MANWIDTH=1000, `/usr/include/linux/openat2.h`)

Legend: EXACT = a sentence states the value; IMPLIED = a quoted sentence entails the value without extra assumption; NONE = no cited sentence (author inference, or open(2) only, which the claim does not cite).

| P | Expected | Sentence that predicts it | Status |
|---|---|---|---|
| P01 | `os` has no openat2 = False | none; Python stdlib fact | NONE |
| P02 | os.open O_NOFOLLOW, earlier symlink → opened | RESOLVE_NO_SYMLINKS para: O_NOFOLLOW "affects the handling of symbolic links only in the final component" | IMPLIED. Probe comment says "the page: earlier components are followed"; the page never says that literally |
| P03 | os.open O_NOFOLLOW, final symlink → ELOOP | page says only "affects ... the final component"; no errno. open(2) ERRORS: "path was a symbolic link, and flags specified O_NOFOLLOW but not O_PATH" → ELOOP | NONE in openat2 pages (open(2) only) |
| P04 | NO_SYMLINKS, earlier symlink → ELOOP | ERRORS: "ELOOP how.resolve contains RESOLVE_NO_SYMLINKS, and one of the path components was a symbolic link" | EXACT |
| P05 | NO_SYMLINKS, final symlink → ELOOP | same ERRORS line ("one of the path components"); the O_PATH|O_NOFOLLOW exception ("then an O_PATH file descriptor ... will be returned") implies error otherwise | EXACT/IMPLIED |
| P06 | NO_SYMLINKS, plain path → opened | ELOOP only when a component is a symlink; "As with openat(2)..." | IMPLIED (control) |
| P07 | BENEATH `real/../../outside.txt` → EXDEV | ERRORS: "EXDEV ... RESOLVE_IN_ROOT or RESOLVE_BENEATH, and an escape from the root during path resolution was detected" | EXACT |
| P08 | BENEATH absolute symlink → EXDEV | BENEATH: "This causes absolute symbolic links (and absolute values of path) to be rejected"; EXDEV line | EXACT/IMPLIED |
| P09 | BENEATH relative symlink inside → opened | BENEATH rejects absolute links and non-descendants; `real` is a descendant | IMPLIED (control) |
| P10 | IN_ROOT absolute symlink → content `rootfile` | IN_ROOT: "Absolute symbolic links are interpreted relative to dirfd" | EXACT |
| P11 | os.open(dir_fd) absolute symlink → content `outside` | openat2(2) never says a plain open follows absolute links; only that BENEATH "causes ... to be rejected". open(2) would be the source | NONE in openat2 pages |
| P12 | unknown resolve bit 1<<14 → EINVAL | "If any bits other than those listed above are set in how.resolve, an error is returned"; ERRORS EINVAL "unknown flag or invalid value" | EXACT |
| P13 | mode≠0 without O_CREAT → EINVAL | ERRORS EINVAL "mode is nonzero, but how.flags does not contain O_CREAT or O_TMPFILE" | EXACT |
| P14 | O_PATH|O_NOFOLLOW + NO_SYMLINKS on final symlink → fd of the link | "...how.resolve contains RESOLVE_NO_SYMLINKS, and how.flags contains both O_PATH and O_NOFOLLOW, then an O_PATH file descriptor referencing the symbolic link will be returned" | EXACT (sentence correct, probe does not test the flag, see §2) |

Count: 3 NONE (P01, P03, P11). `PROBES_WITHOUT_SOURCE_SENTENCE=3/14`. The header comment's "14/14 facts" compares the probe to its own author's expectations, so `PROBE_FACTS=14/14` is self-consistency, not calibration.

## 2. Cannot-fail and discrimination (mutant matrix)

Defined: `cannot_fail` = probes whose expected value still holds under a do-nothing openat2 (`MUT=noresolve`: resolve=0, flags masked to 32 bits, mode zeroed, i.e. plain openat). Run: `python3 -B mut_noresolve.py --work <fresh>` with MUT=noresolve.

Result: `PROBE_FACTS=7/14`. Survivors: P01, P02, P03, P06, P09, P11, P14 = 7. Of these, P01 and P02/P03/P11 test os.open or Python, not openat2; P06/P09 are controls; P14 is the real defect.

Single-defect mutants of the frozen probe (`PROBE_FACTS`, killed probes):
- no_nosymlinks (drop bit 0x04): 12/14, killed P04 P05. **P14 survives.**
- no_beneath (0x08): 12/14, killed P07 P08
- no_inroot (0x10): 13/14, killed P10
- no_nomagic (0x02): 14/14, killed none
- no_xdev (0x01): 14/14, killed none
- no_cached (0x20): 14/14, killed none
- unknown_ok (drop EINVAL checks): 12/14, killed P12 P13
- no_opath (drop O_PATH): 13/14, killed P14
- no_nofollow (drop O_NOFOLLOW): 13/14, killed P14

P14 is the operability defect: plain `O_PATH|O_NOFOLLOW` already returns the link's own fd, so the expectation holds with RESOLVE_NO_SYMLINKS removed. The probe does not test the sentence it cites. Fix: add a case with O_PATH|O_NOFOLLOW and no NO_SYMLINKS on the same symlink, expected to return the link fd, plus a case with NO_SYMLINKS and O_NOFOLLOW but without O_PATH, expected ELOOP. (Not written to lane; for the L1 to decide.)

## 3. Missing cases (candidate extension, scratch only, run on this kernel)

Extension X01–X17 (`cand-extra.py`, in scratch, removed). Every expectation cites a sentence:
- X01 RESOLVE_CACHED + O_CREAT on absent name → EAGAIN (RESOLVE_CACHED para; EAGAIN). Observed EAGAIN.
- X02 RESOLVE_CACHED on warm file ×3 → opened ×3. Observed opened ×3.
- X03 NO_MAGICLINKS on `/proc/self/fd/0` → ELOOP. Observed ELOOP.
- X04 NO_SYMLINKS on `/proc/self/fd/0` → ELOOP (page: NO_SYMLINKS implies no magic links). Observed ELOOP.
- X05 NO_MAGICLINKS on plain path → opened (control). Observed opened.
- X06 size=16 (< struct) → EINVAL. Observed EINVAL.
- X07 size=32 with nonzero extension → E2BIG. Observed E2BIG.
- X08 size=32 with zero extension → opened. Observed opened.
- X09 OPENAT2_REGULAR (bit 32, `openat2.h`) on a directory → EFTYPE. Observed EFTYPE. The probe never reads this bit; the header defines it.
- X10 OPENAT2_REGULAR on regular file → opened. Observed opened.
- X11 mode 0o10000 with O_CREAT → EINVAL ("bits other than 07777"). Observed EINVAL.
- X12 unknown how.flags bit 33 → EINVAL. Observed EINVAL.
- X13 IN_ROOT `real/../../f.txt` → rootfile. Observed rootfile.
- X14 IN_ROOT absolute `/f.txt` → rootfile. Observed rootfile.
- X15 BENEATH `real/../f.txt` → rootfile (control). Observed rootfile.
- X16 NO_XDEV across bind mount → EXDEV (inside `unshare -Urm`). Observed EXDEV.
- X17 same bind mount without flag → opened. Observed opened.

Identity: `CAND_FACTS=15/15` plain, `17/17` with namespace. Do-nothing mutant (noresolve): `8/17` with ns, `7/15` without. Kill check of extra single-defect mutants (`cand-mut.py`, under unshare): no_nomagic → X03; no_xdev → X16; no_cached → X01; no_inroot → X13 X14; no_regular → X09. All killed; no_inroot and no_nomagic each caught by one or two extras.

Not covered by the frozen probe at all: RESOLVE_NO_XDEV, RESOLVE_NO_MAGICLINKS, RESOLVE_CACHED (EAGAIN), size/E2BIG/EINVAL, mode>07777, unknown how.flags bit, OPENAT2_REGULAR (7.2), IN_ROOT `..`/absolute. The probe reads only six RESOLVE constants and never reads OPENAT2_REGULAR.

## 4. Instability

- cwd: `/`, `/proc`, scratch, and relative `--work`: 14/14 each (A, G, and F-variants).
- nice -n 19 with umask 077: 14/14 (B). Extras under nice -n 19 with unshare: 17/17.
- umask 002 and 027: 14/14 each.
- Repeats (×5 extras, ×2 original): no variance.
- **Umask crash (probe defect)**: umask 0177, 0227, 0277, 0577, 0700, 0777 → probe aborts with uncaught `PermissionError`/`FileNotFoundError` (exit 1, no PROBE lines, no PROBE_FACTS). Cause: the probe's own work directories lose owner write/exec bits. The `finally` `rmtree(ignore_errors=True)` leaves mode-0 trees behind (observed leftovers U0577, U0777, U0700; removed by me).
- Not run: as root (uid-dependence; EACCES cases would vanish; INFERENCE: the 14 expectations do not depend on uid but the probe does not assert ownership either). Not run: btrfs, tmpfs (scratch rule). Filesystem-dependence is INFERENCE: symlink/O_PATH/magic links need a filesystem that supports them; the probe has no fallback; it would abort uncaught.
- Stale path: docstring says `corpus/evidence/round62/openat2-probe.py`; the file is `controls/candidate-openat2-probe.py`.

## 5. Lane-level finding (for L1)

`corpus/evidence/round62/c2v2-count.py` lines 58, 217 read `corpus/evidence/round62/openat2-probe.py` and `openat2-probe.txt`. `ls` shows neither file exists (only `controls/candidate-*`). Under the frozen counter the PROBE check at base is 0 unless the candidate is promoted to those exact paths. `controls/run-c2v2-controls.py` reads the candidate under `controls/`. Two sites disagree on the probe's location; the counter's path wins under the freeze.

## 6. Cannot-fail, calibration

- P01: passes under a do-nothing openat2 and tests Python, not the kernel; no source sentence.
- P14: sentence is correct, the probe cannot distinguish it from plain `O_PATH|O_NOFOLLOW` (§2).
- P02, P03, P11, P06, P09: pass under a do-nothing openat2 (baseline or controls); P03 and P11 need open(2), not cited.

Calibration: 11/14 expectations have a cited sentence (EXACT or IMPLIED); 3/14 do not. Expectations were checked against the same kernel by the same author, so `PROBE_FACTS=14/14` agrees with its authors only.

Verdict inputs: no probe is wrong on this kernel (14/14 across cwd, nice, umask 002/022/027/077); the probe is operable only for umask values that keep owner rwx on directories it creates.

VERDICT: PROBES_WITHOUT_SOURCE_SENTENCE=3/14 cannot_fail=7
