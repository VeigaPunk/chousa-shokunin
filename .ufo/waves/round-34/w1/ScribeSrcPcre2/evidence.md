# ScribeSrcPcre2 evidence — 2026-10-23

## Scope and source shape

- Opened `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md`: header at lines 9–10; rows S060–S063 at lines 70–73. Registry is at lines 7–10.
- The supplied lane-root path `/home/vgpnk/Projects/shokunin/chousa-shokunin/CORPUS.md` was absent (`read` returned Path not found). Opened fleet-root `/home/vgpnk/Projects/shokunin/CORPUS.md`, section `SOURCES.md — where a shokunin learns`, lines 64–114 (shape, tier/status, opened/recheck/used-by, row evidence rule).
- `corpus/knowledge/long-span-argv-r34.md` was not present when checked. Its requested `used-by` backlink is therefore provisional in `rows.md`; both source rows are queued, not mined.

## Commands and observed output

- Command: `timeout 20s man -w 3 pcre2limits; timeout 20s man -w 1 grep`
  Output: `/usr/share/man/man3/pcre2limits.3.gz` and `/usr/share/man/man1/grep.1.gz`.
- Command: `timeout 20s pacman -Q pcre2 grep`
  Output: `pcre2 10.49-1`; `grep 3.12-2`.
- Command: `timeout 15s sha256sum /usr/share/man/man3/pcre2limits.3.gz /usr/share/man/man1/grep.1.gz`
  Output: `a3ea2c67c102af649be069fd31bb6b658c2170f15bc1a1728f464fd8e5974bd6  /usr/share/man/man3/pcre2limits.3.gz`; `9b027d022ae9533ff3e140ba8d96ccd58955bdf9d1c818c327fd992e575c85ba  /usr/share/man/man1/grep.1.gz`.
- Open commands: `timeout 30s env MANPAGER=cat PAGER=cat man 3 pcre2limits`; `timeout 30s env MANPAGER=cat PAGER=cat man 1 grep`. Both returned the local page text. `pcre2limits(3)` page revision footer: PCRE2 10.49, 03 September 2025. `grep(1)` footer: GNU grep 3.12-modified, 2025-03-21. Relevant headings/quotes are transcribed in `rows.md`.
- The source file hash and package versions above identify the opened installed manuals; no network access or package installation was used. `df -h /fast` reported 804G total, 716G used, 88G available (90% used).

## Bounded local compile probe

Exact command invoked (bounded by `timeout 300s`):

```sh
timeout 300s bash -c 'set -u; work=/fast/scratch/hyaku/chousa-r34/w1/ScribeSrcPcre2; pattern_file=$work/literal-pcre-pattern.txt; err_file=$work/grep-stderr.txt; test_span() { n=$1; printf -v spaces "%*s" "$n" "" || return 90; pattern=${spaces// /\\x41}; printf "%s\n" "$pattern" > "$pattern_file" || return 91; /usr/bin/grep -P -f "$pattern_file" /dev/null >/dev/null 2>"$err_file"; rc=$?; bytes=$(wc -c < "$pattern_file"); if [ "$rc" -eq 2 ]; then detail=$(<"$err_file"); printf "span_bytes=%s pattern_file_bytes=%s grep_exit=%s compile=FAIL diagnostic=%s\n" "$n" "$bytes" "$rc" "$detail"; return 1; fi; printf "span_bytes=%s pattern_file_bytes=%s grep_exit=%s compile=OK\n" "$n" "$bytes" "$rc"; return 0; }; for n in 1 8192 16384 32767 32768 32769 40000 65536; do test_span "$n" || :; done; low=1; high=131072; test_span "$high" >/dev/null 2>&1 && { printf "binary-search-upper-bound=%s compiled; extend search\n" "$high"; exit 3; }; while [ $((low + 1)) -lt "$high" ]; do mid=$(((low + high) / 2)); if test_span "$mid" >/dev/null 2>&1; then low=$mid; else high=$mid; fi; done; test_span "$low"; test_span "$high"; printf "largest_compiling_span_bytes=%s next_failing_span_bytes=%s\n" "$low" "$high"'
```

This writes one bounded pattern file, containing `\x41` repeated `n` times and a terminating newline, then invokes the requested `/usr/bin/grep -P -f file` against `/dev/null`; exit 1 means no match but no compile error, exit 2 is reported as compile failure. Captured output:

```text
span_bytes=1 pattern_file_bytes=5 grep_exit=1 compile=OK
span_bytes=8192 pattern_file_bytes=32769 grep_exit=1 compile=OK
span_bytes=16384 pattern_file_bytes=65537 grep_exit=1 compile=OK
span_bytes=32767 pattern_file_bytes=131069 grep_exit=2 compile=FAIL diagnostic=/usr/bin/grep: regular expression is too large
span_bytes=32768 pattern_file_bytes=131073 grep_exit=2 compile=FAIL diagnostic=/usr/bin/grep: regular expression is too large
span_bytes=32769 pattern_file_bytes=131077 grep_exit=2 compile=FAIL diagnostic=/usr/bin/grep: regular expression is too large
span_bytes=40000 pattern_file_bytes=160001 grep_exit=2 compile=FAIL diagnostic=/usr/bin/grep: regular expression is too large
span_bytes=65536 pattern_file_bytes=262145 grep_exit=2 compile=FAIL diagnostic=/usr/bin/grep: regular expression is too large
span_bytes=32764 pattern_file_bytes=131057 grep_exit=1 compile=OK
span_bytes=32765 pattern_file_bytes=131061 grep_exit=2 compile=FAIL diagnostic=/usr/bin/grep: regular expression is too large
largest_compiling_span_bytes=32764 next_failing_span_bytes=32765
```

Probe's largest successful span length on this host is 32,764 bytes; the next length, 32,765, fails. This is the measured repeated-ASCII-literal pattern under installed grep/PCRE2, not a guarantee for other pattern shapes/builds. The outer tool output did not print a separate shell exit-code field; each grep exit code is captured and shown above.

## Boundaries

- Only requested manual opens, package/file metadata reads, and the bounded grep compile probe were performed. No `c1-count.py`, candidate C1 gate, build, test suite, or production-code change was made.
- Created only this seat's artifacts under `.ufo/waves/round-34/w1/ScribeSrcPcre2/`; the probe pattern and stderr files are under `/fast/scratch/hyaku/chousa-r34/w1/ScribeSrcPcre2/`. No install/update occurred.
