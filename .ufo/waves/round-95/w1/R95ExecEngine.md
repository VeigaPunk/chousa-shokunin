# R95ExecEngine — engine-agreement probe (tools/search-rerun.py vs GNU grep)

Hypothesis under test: "for any fixed string or Python-re pattern that a record can file, `tools/search-rerun.py`'s per-line
matcher and GNU grep `-l -F`/`-l -P` select the same files."

**Result: falsified.** Of 27 probes: 15 agree, 11 disagree, 1 is refused by the tool (PCRE-only `\K`, exit 2). The
disagreements have five causes (F1–F6), two of which no named limit discloses.

## Setup
- Carrier clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/chousa-shokunin <S>/repo`, checkout `d27e9891ba6d2bae8b1f6060f7c01bf13a1a6ea1`.
- Probe fixture: a scratch git repo (`git init` in a `mktemp -d` under `/fast/scratch/hyaku/chousa-r95/R95ExecEngine`); `git rev-parse --show-toplevel` asserted equal before the commit (`-c user.name=fixture -c user.email=fixture@invalid`). Fixture files: CRLF line ends, NUL byte, invalid UTF-8, no trailing newline, match on the last line, case, `\s` (VT, NBSP), `$`, `^`, `\w`/`\b` on CJK (`検索者`), lookbehind, a would-be cross-newline pattern, `.x.txt` dotfile, `sub/k_sub.txt`, an empty file.
- Per probe: grep side = `bash -c 'set -o pipefail; cd FX && [LC_ALL=C] /usr/bin/grep -l -F|-P -e EXPR GLOB | LC_ALL=C sort'`, glob expanded by bash (no dotglob, no globstar), as the record's "As run" line. Recorded value = that grep set. Tool side = one record per probe filed with that grep value, verified by the real CLI `python3 -B tools/search-rerun.py verify <rec> --root FX`.
- Host: `en_US.UTF-8`; GNU grep 3.12-modified; Python 3.14.8; git 2.56.0. No tools installed or updated.
- A first driver (`probe_driver.py`, superseded) forced `LC_ALL=C` onto P04b/P11 and put the `\K` row into a shared record, so its output is not a receipt. The v2 driver (`R95ExecEngine-probe_v2.py`) is the one reported.

## Table (probe | engine | expression | where | grep | tool at_rev | agree | cause)
Counts are files. `agree` = the tool's CLI verdict `rev=MATCH` (exit 0) for a record filed with grep's value.

| probe | engine | expression | where | grep | tool (at_rev) | agree | cause |
|---|---|---|---|---|---|---|---|
| P01 | fixed | `token` | data/*.txt | 12 | 13 | DISAGREE | dotfile `.x.txt` (F2) |
| P02 | fixed | `HELLO TOKEN` | data/*.txt | 1 | 1 | AGREE | |
| P03 | fixed | `検索者` | data/*.txt | 2 | 2 | AGREE | |
| P04 | regex | `\w` | r_cjkonly.txt, host UTF-8 | 1 | 1 | AGREE | |
| P04c | regex | `\w` | r_cjkonly.txt, LC_ALL=C grep | 0 | 1 | DISAGREE | locale (F4) |
| P05 | regex | `\b検索者\b` | data/*.txt | 1 | 1 | AGREE | |
| P06 | regex | `world$` | data/*.txt | 1 | 1 | AGREE | |
| P07 | regex | `world\r$` | data/*.txt | 1 | 1 | AGREE | CRLF identical |
| P08 | regex | `^second` | data/*.txt | 2 | 2 | AGREE | |
| P09 | regex | `\t` | data/*.txt | 1 | 1 | AGREE | |
| P10 | regex | `\s` | j_vtab.txt | 1 | 1 | AGREE | VT is `\s` in both |
| P11 | regex | `\s` | k_nbsp.txt, host UTF-8 | 1 | 1 | AGREE | NBSP matched by grep in UTF-8 |
| P11c | regex | `\s` | k_nbsp.txt, LC_ALL=C grep | 0 | 1 | DISAGREE | locale (F4) |
| P12 | regex | `foo\nbar` | data/*.txt | 0 | 0 | AGREE | |
| P13 | regex | `(?<=foo)bar` | data/*.txt | 1 | 1 | AGREE | |
| P14 | regex | `\Ktoken` | data/*.txt | 12 | refused, exit 2 | REFUSED | Python `re` has no `\K` (F5) |
| P15 | regex | `[[:alpha:]]+` | data/*.txt | 17 | 0 | DISAGREE | PCRE POSIX class vs Python char set (F5) |
| P16 | regex | `.` | data/*.txt | 17 | 18 | DISAGREE | dotfile (F2) |
| P17 | regex | `\btoken\b` | data/*.txt | 11 | 12 | DISAGREE | dotfile (F2) |
| P18 | fixed | `token` | data/sub/*.txt | 1 | 1 | AGREE | |
| P19 | fixed | `token` | data/**/*.txt (bash, no globstar) | 1 | 14 | DISAGREE | `**` spans segments and includes dotfiles (F3) |
| P20 | regex | `token\Z` | data/*.txt | 7 | 7 | AGREE | |
| P21 | regex | `^$` | data/*.txt | 0 | 17 | DISAGREE | phantom empty line after final `\n` (F1) |
| P22 | regex | `x*` | data/*.txt | 17 | 19 | DISAGREE | phantom line + `.x.txt` + empty file (F1, F2) |
| P23 | regex | `hel\x00lo` | data/*.txt | 0 | 1 | DISAGREE | grep binary mode splits lines at NUL (F6) |
| P24 | regex | `^$` | data/j_empty.txt | 0 | 1 | DISAGREE | phantom line on an empty file (F1) |
| P25 | fixed | `token` | data/.x.txt (explicit path) | 1 | 1 | AGREE | |

Tally: AGREE 15, DISAGREE 11, REFUSED 1 (`grep -c` on the table file: 15 / 11 / 1; 27 probes).
Full per-probe stdout and exit codes: `R95ExecEngine-probe-tool-runs.txt`; table: `R95ExecEngine-probe-table.txt`; driver:
`R95ExecEngine-probe_v2.py`; mechanism receipts M1–M4: `R95ExecEngine-mechanisms.txt`.
On every probe the tool's `at_tree` equals its `at_rev` (0 mismatching lines in the tool-runs receipt), so the disagreements are rev-level, not
TREE_CHANGED noise.

## Findings (each names command, receipt, observed line, exit code)

**F1 — phantom empty line: `^$` and any empty-matching pattern select every newline-terminated file (NOT disclosed).**
Command: P21 record, `python3 -B tools/search-rerun.py verify <rec-P21> --root <fixture>`. Receipt: `probe-tool-runs.txt` (P21), `mechanisms.txt` [M1].
Observed: `SEARCH_RERUN Q1 rev=DRIFT tree=SAME recorded=0 at_rev=17 at_tree=17 COUNT_DRIFT,SET_DRIFT`, exit 1. Grep recorded 0 on the same
fixture (rc=1). Cause: `hit()` iterates `data.split(b"\n")`; `hello\n` yields `[b"hello", b""]`, so the empty tail is tested as a line, and
`b"".split(b"\n")` yields `[b""]`, so an empty file is a line. Named limit (b) ("matching is per line") does not describe this. A record correct under grep is
refused with `COUNT_DRIFT`, which the tool documents as "the record is wrong". Committed record unaffected: none of its 8 expressions can match the empty string (M3, 8/8 rev MATCH, exit 0).

**F2 — dotfiles: the tool matches `.x.txt` under a `*.txt` glob, bash does not (NOT disclosed by (a)–(f)).**
Command: P01/P16/P17 records. Receipt: `probe-tool-runs.txt` (P01, P16, P17), `mechanisms.txt` [M1] (`dot-token`, `ls-tree`).
Observed: P01 `SEARCH_RERUN Q1 rev=DRIFT tree=SAME recorded=12 at_rev=13 at_tree=13 COUNT_DRIFT,SET_DRIFT`, exit 1; grep recorded 12 (bash excludes `.x.txt`).
`PurePosixPath('data/.x.txt').full_match('data/*.txt')` is True. Named limit (c) covers "tracked or not", not dotfiles. The committed capture store has no dotfiles (M4: `git ls-files corpus/captures | grep -c '/\.'` → 0, rc=1), so the committed record is unaffected.

**F3 — `**` in `where` is not bash's `**` (in the tool docstring as Python `full_match`; not in named limits (a)–(f); the record's "As run" line is bash).**
Command: P19 record (`data/**/*.txt`). Receipt: `probe-tool-runs.txt` (P19).
Observed: `SEARCH_RERUN Q1 rev=DRIFT tree=SAME recorded=1 at_rev=14 at_tree=14 COUNT_DRIFT,SET_DRIFT`, exit 1. Bash with no globstar yields 1 file
(`data/sub/k_sub.txt`); the tool's `**` matches 14. A record filed with its own "As run" glob is refused.

**F4 — locale: a record's grep value depends on `LC_ALL`, and the record does not name it (NOT disclosed).**
Command: P04c (`\w` on `検索者`, grep under `LC_ALL=C`) and P11c (`\s` on NBSP, `LC_ALL=C`). Receipt: `probe-tool-runs.txt` (P04c, P11c).
Observed: P04c `grep_rc=1 grep_set=[]` vs tool `at_rev=1` → `COUNT_DRIFT,SET_DRIFT`, exit 1; P11c the same shape. Under the host UTF-8 locale both agree
(P04, P11). The record's "As run" section names GNU grep 3.12 but not a locale; the tool always matches Unicode. Named limit (a) covers the engine, not the locale.

**F5 — PCRE-only constructs: `\K` refuses the whole record (exit 2); `[[:alpha:]]+` is "record is wrong" when the record is right (partly disclosed by (a)).**
Command: P14 record (`\Ktoken`), P15 record (`[[:alpha:]]+`). Receipt: `probe-tool-runs.txt` (P14, P15).
Observed: P14 `SEARCH_RERUN_ERROR EXPRESSION Q1: bad escape \K at position 0`, exit 2. P15 `SEARCH_RERUN Q1 rev=DRIFT ... recorded=17 at_rev=0 ... COUNT_DRIFT,SET_DRIFT`, exit 1,
while grep -P recorded 17. Named limit (a) discloses the engine is Python `re`, measured "on these 8 expressions only", so the mechanism is disclosed. The
gloss "COUNT_DRIFT, SET_DRIFT = the record is wrong" is not true for a record correctly filed under PCRE.

**F6 — NUL bytes: grep's default binary mode splits lines at NUL; the tool does not (NOT disclosed; not covered by (b)).**
Command: P23 record (`hel\x00lo`, grep `-P`). Receipt: `mechanisms.txt` [M2].
Observed: `grep -c -P 'hel\x00lo' nulchk.txt` → 0, rc=1; `grep -a -c -P 'hel\x00lo'` → 1, rc=0; `grep -c -P 'lo token'` → 1, rc=0. Tool on the same file:
`at_rev=1`, `COUNT_DRIFT,SET_DRIFT`, exit 1.

## Agreement that holds
CRLF (`world\r$`), `^`/`$` on normal lines, `\t`, `\s` on VT, lookbehind, `\b` on CJK in the host UTF-8 locale, invalid UTF-8 bytes (`d_badutf8` in the
`token` set for both), a last line with no trailing newline (`e_notrail`, `f_lastline`), a NUL before a fixed needle in a line (`c_nul`, `token`), the
subdirectory glob `data/sub/*.txt`, an explicit dotfile path (P25), and cross-newline `foo\nbar` (P12, never matches either).

## Remedy (routed, not applied: this seat is read-only)
- F1: do not test the empty tail after a final `\n`; an empty file has no lines.
- F2/F3: exclude dotfile path components in `matches()`/`tree_files()`, or refuse them; implement bash's `**` rule or state the difference in the record shape.
- F4: name the locale in the record's "As run" and refuse otherwise, or match grep's locale.
- F5: state that `\K`, POSIX classes and other PCRE-only forms are refused; change the `COUNT_DRIFT` gloss from "the record is wrong" to "the engines differ".
- F6: split on NUL like grep's binary mode, or record the difference.

Committed-record check (M3): the carrier record verifies at its base revision (8/8 rev MATCH, exit 0), with TREE_CHANGED on the captures added at the carrier.
This is the only part of the C1 predicate this seat confirmed at the carrier; `rerun-controls-r95.py` was not run by this seat.

## Tool installs/updates
None.

## Verdicts
VERDICT: R95ExecEngine C1 fired — the per-line matcher disagrees with GNU grep on 11 of 27 probes (phantom empty line F1, dotfiles F2/F3, locale F4, NUL F6, PCRE-only F5), so "COUNT_DRIFT/SET_DRIFT = the record is wrong" is false for records grep finds correctly, and only F5's mechanism is named in (a).
VERDICT: R95ExecEngine C2 n/a — not touched by this probe.
