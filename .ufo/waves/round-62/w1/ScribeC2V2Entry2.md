# ScribeC2V2Entry2 — round 62, wave w1, claim C2 (openat2 entry draft)

Seat: scribe. Scope: an independent candidate for `corpus/knowledge/openat2-resolve-r62.md`, checked
against the frozen counter `corpus/evidence/round62/c2v2-count.py` in a scratch mirror. The lane tree was
not written. Drafts: `.ufo/waves/round-62/w1/ScribeC2V2Entry2/entry.md` (sha256 prefix `b40f651113595141`),
counter line `.ufo/waves/round-62/w1/ScribeC2V2Entry2/counter-output.txt`.

## Findings

1. **The draft passes the frozen counter on the mirror.** Counter output (exit 0):
   `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=12/12 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS`
   Run twice (both `C2=PASS`, rc 0) on the same mirror. Rows S138, S139, S140 were inserted from
   `controls/c2v2-positive-rows.txt` as `run-c2v2-controls.py` does; the probe script and output were
   copied from `controls/candidate-openat2-probe.{py,txt}`; the README line was appended for MAP.
2. **Coverage.** 12 located quotes (S138: Q1–Q8; S139: Q9; S140: Q10–Q12), 6 claims, every quote cited by
   a claim. The decision table has 11 rows: 5 rest on a counted quote or a probe line; 6 are marked
   `(unquoted)` or `not probed` because the registry anchors do not reach them (finding 4).
3. **Calibration; the ECHO margins are thin.** Per-claim numbers, same rule as the counter, computed from
   the mirror's entry: claim 1 fresh 5 of 14 words (0.36); claim 2 fresh 4 of 12 (0.33; with one fresh word
   fewer it would be 3 of 12 = 0.25 and FAIL); claim 3 fresh 5 of 10; claim 4 fresh 13 of 19; claim 5 fresh
   10 of 15; claim 6 fresh 5 of 7. Claim 2 is the closest to the floor. The ECHO pass is a word-count screen,
   not evidence that a claim follows from its quotes.
4. **Registry anchors limit what can be counted (not a draft defect; L1 should know).** The S139 anchor
   cell names only `RESOLVE_NO_SYMLINKS`, so the header's other values (0x01, 0x02, 0x08, 0x10, 0x20) are in
   the table without counted quotes, and the BENEATH comment is recorded as unquoted. The S140 anchor cell
   names only P01, P02 and P04, so P03, P05–P14 are cited in the table as probe lines, not quotes. Read from
   `corpus/evidence/round62/c2v2-count.py` lines 56–58 (`MAN`, `FILE`, `OWN` anchors) and lines 94–102
   (`resolve`): the counter binds quotes to the row's source text, and anchors to the row's anchor cell.
5. **Three self-corrections before the final run** (each re-run through the counter):
   - a table cell attributed to the S139 comment that BENEATH "lets a relative symlink through" — the
     comment does not say this; the probe does (P09 opened). Cell rewritten to name the probe.
   - "ctypes passes any bit to the kernel" — the probe tests one unknown bit (1<<14, P12). Cell narrowed.
   - claims 4 and 5 carried a `ctypes` route and a header-misspelling reading that no quote states;
     both now carry `[INFERENCE: …]`. The r61 check-then-write reference is pinned to
     `corpus/knowledge/derived-output-safety-r61.md` line 9 (`whether a check made before the write still
     holds when the write happens`), found with `grep -n -i 'check\|then\|race\|TOCTOU'`.
6. **Header macro typo, verified.** `grep -c OEXT_NO_MAGICLINKS /usr/include/linux/openat2.h` → `1`
   (the comment at line 38); `grep -c 'define OEXT' /usr/include/linux/openat2.h` → `0`. Q9 quotes it; the
   table uses `RESOLVE_NO_MAGICLINKS (0x02)`.
7. **The PROBE check ran on a copy, not on a lane-owned probe.** `corpus/evidence/round62/` has no
   `openat2-probe.py` or `openat2-probe.txt` yet; the mirror copies are byte-identical to the controls'
   candidate files. L1 must place the probe and its output in the lane for the real counter to read them;
   until then the PROBE line is unverified in the lane.

## Evidence (commands and observed output)

- Man page, counter's env: `env MANWIDTH=1000 LC_ALL=C.UTF-8 man -l /usr/share/man/man2/openat2.2.gz | col -bx > $S/man-counter-env.txt`
  → rc 0, 171 lines; `cmp` against a render with the default locale → identical. Locations in that text:
  SYNOPSIS (line 9), glibc wrapper note (line 18), `RESOLVE_NO_SYMLINKS`/`O_NOFOLLOW` contrast (line 86),
  Disallow (line 82), unknown-bits sentence (line 98), RESOLVE_CACHED `since Linux 5.12` (line 95), ERRORS
  heading (line 103), ELOOP (line 123), EXDEV (line 127), HISTORY `Linux 5.6.` (lines 137–138).
- Header: `cat /usr/include/linux/openat2.h` (read; sha256 prefix `8db1c89e62b93f8e`); the RESOLVE_NO_SYMLINKS
  comment ends at line 38 with `(implies OEXT_NO_MAGICLINKS) */`.
- Packages, read-only directory listing (no pacman call): `ls /var/lib/pacman/local` →
  `linux-api-headers-7.2-1`, `man-pages-6.19-1`. `uname -r` → `7.2.11-arch1-1`; `python3 -B --version` → `Python 3.14.8`.
- Probe, live: `python3 -B controls/candidate-openat2-probe.py --work $S/probe-live/w` → rc 0, stderr empty,
  output ends `PROBE_FACTS=14/14`; the output compared with `controls/candidate-openat2-probe.txt` by `diff`
  (blank lines removed) → equal. Lines cited in the entry: P01 `observed=False`, P02 `observed=opened`,
  P03 `ELOOP`, P04 `ELOOP`, P05 `ELOOP`, P07/P08 `EXDEV`, P09 `opened`, P10 `rootfile`, P11 `outside`,
  P12 `EINVAL`, P13 `EINVAL`, P14 `True`.
- Registry rows: `c2v2-positive-rows.txt` parsed in Python → 3 rows, each with 13 `|`-split cells
  (the counter's `len(cells) == 13`).
- Mirror census: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $MIRROR/corpus/SOURCES.md`
  run with the mirror as cwd → rc 0.
- Counter: `TMPDIR=$S python3 -B corpus/evidence/round62/c2v2-count.py --root $MIRROR` → rc 0 (twice), line
  as in finding 1.

## Named limits of this draft (also in the entry's `## Limits`)

- Quotes describe man-pages 6.19 and linux-api-headers 7.2-1; one probe on kernel 7.2.11, x86_64, one
  local filesystem; HISTORY `Linux 5.6` is unquoted.
- The probe opens existing files for reading only: NO_XDEV, NO_MAGICLINKS, CACHED/EAGAIN, the dot-dot
  race retry and O_CREAT are not probed.
- Claim-level entailment is not machine-checked (the counter says so); the three drafts need non-author reading.
- I did not compare against the other two drafts or the positive control; that is L1's merge.

## Out of scope / not done

- No lane tree file was written (`corpus/` untouched); no frozen counter, battery, control or tool edited.
- No git/jj mutation; no pacman; no network; no subagents; no tool installed or upgraded (none needed).
- Scratch `/fast/scratch/hyaku/chousa-r62/ScribeC2V2Entry2/` removed before yield.

VERDICT: ENTRY2_C2=PASS quotes=12 claims=6
