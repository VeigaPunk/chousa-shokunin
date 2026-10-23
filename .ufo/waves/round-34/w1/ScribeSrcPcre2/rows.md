# Draft SOURCES.md rows — S065–S066

Draft only; no lane production file was edited. Table shape copied from `corpus/SOURCES.md:9–10`; source admission guidance is `CORPUS.md:64–114`.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S065 | PCRE2 `pcre2limits(3)` manual — `/usr/share/man/man3/pcre2limits.3.gz` | docs | A | PCRE2 compiled-pattern size versus source-pattern length for the installed library; not the OS argument-byte ceiling or this lane's verifier behavior | “SIZE AND OTHER LIMITATIONS”; PCRE2 10.49 (03 September 2025), installed `pcre2 10.49-1`; file SHA-256 `a3ea2c67c102af649be069fd31bb6b658c2170f15bc1a1728f464fd8e5974bd6` | The manual distinguishes an effectively unlimited source-pattern length from an approximately 64-thousand-code-unit compiled-pattern size ceiling for default 8/16-bit libraries. On this host `/usr/bin/grep -P -f` compiled repeated `\x41` literals through a 32,764-byte span and rejected 32,765 as “regular expression is too large”; an argv workaround using a four-character escape per byte therefore does not remove the compiled-size limit. | queued | 2026-10-23 | on-release | corpus/knowledge/long-span-argv-r34.md |
| S066 | GNU `grep(1)` manual — `/usr/share/man/man1/grep.1.gz` | docs | A | GNU grep 3.12 pattern-file and `-F`/`-P`/`-z` option semantics; not this lane's matcher contract | “OPTIONS / Pattern Syntax” (`-F`, `-P`), “Matching Control” (`-f`), and “Other Options” (`-z`); GNU grep 3.12-modified (2025-03-21), installed `grep 3.12-2`; file SHA-256 `9b027d022ae9533ff3e140ba8d96ccd58955bdf9d1c818c327fd992e575c85ba` | `-f` reads one pattern per line, so a newline-containing span cannot be transported as one `-f` pattern [INFERENCE]; `-F` selects fixed-string syntax, while `-z` makes input/output records NUL-terminated and does not change the documented pattern-file delimiter. | queued | 2026-10-23 | on-release | corpus/knowledge/long-span-argv-r34.md |

## Located quotes (opened 2026-10-23)

- S065 — `/usr/share/man/man3/pcre2limits.3.gz`, `pcre2limits(3)`, “SIZE AND OTHER LIMITATIONS”: “The maximum size of a compiled pattern is approximately 64 thousand code units for the 8-bit and 16-bit libraries” (19 words).
- S065 — same page and section: “The maximum length of a source pattern string is essentially unlimited” (11 words).
- S066 — `/usr/share/man/man1/grep.1.gz`, `grep(1)`, “OPTIONS / Matching Control / -f”: “Obtain patterns from FILE, one per line.” (7 words).
- S066 — same page, “OPTIONS / Pattern Syntax / -F”: “Interpret PATTERNS as fixed strings, not regular expressions.” (8 words).
- S066 — same page, “OPTIONS / Other Options / -z”: “Treat input and output data as sequences of lines, each terminated by a zero byte (the ASCII NUL character) instead of a newline.” (23 words).

## Provisional backlink

The requested `used-by` value is retained in these draft rows, but `corpus/knowledge/long-span-argv-r34.md` was not present when checked. Keep both rows queued and do not land the backlink as a mined citation until that knowledge entry exists and cites them.
