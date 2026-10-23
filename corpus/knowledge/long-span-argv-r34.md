# Verifying long claim spans without an oversized argv pattern — round 34

source: S064 (Linux `execve(2)`, `MAX_ARG_STRLEN`); S065 (PCRE2 `pcre2limits(3)`, compiled-pattern size); S066 (GNU `grep(1)`, `-f` one pattern per line); lane contract `corpus/evidence/round34/claims.md` (design v3); matcher `tools/research-gate.sh` `tok_span_at` / `tok_span_all`
verified-at: 2026-10-23 (installed man pages re-opened by the L1, `.ufo/waves/round-34/L1/reopen-sources.txt`; base and landed gates measured with counter v3)
recheck: on-release (re-open S064–S066 when man-pages, pcre2 or grep change; re-run `corpus/evidence/round34/c1-count-v3.py` after any matcher edit)

## The defect (base gate `43a1af35…4346`)

`tok_span_at` and `tok_span_all` turned every span byte into a four-character `\xHH` escape and
passed the whole PCRE pattern to grep(1) as one argument. Linux limits a single argument or
environment string to 32 pages, `MAX_ARG_STRLEN` (S064): 131072 bytes including the terminating NUL
on this host's 4 KiB pages. A span of 32768 bytes makes a 131072-character pattern, exec fails with
"Argument list too long", no occurrence is reported, and a verbatim span reads
`observed=unsupported` with `CLAIM_SPAN_NOT_FOUND`. Three bytes earlier the pattern already fails
inside grep: PCRE2's compiled-pattern size is bounded (about 64 thousand code units in the default
8-bit library, S065), and on this host `grep -P -f` rejects a literal pattern for a span of 32765
bytes ("regular expression is too large"; ScribeSrcPcre2, ReviewCounterCode F1). So moving the
pattern into a file does not fix it either, and `grep -F -f` is no whole-span matcher for a
multi-line span because `-f` reads one pattern per line (S066; ExecPerfProfile showed `grep -F -f`
still matching with the span's first line replaced).

Cost, measured by ExecPerfProfile on the base gate at a 64 KiB span: 58.7 s in `json_unescape`
and 18.1 s building the hex pattern, both quadratic in the span length (bash `${s:i:1}` per byte),
3.3× slower under a UTF-8 locale than under `LC_ALL=C`. Grep itself took 7 ms.

## Fix (landed in round 34, gate `772a1d8e…3e58`, ExecC1BuildC)

- Spans up to 32767 bytes keep the base one-pattern matcher byte for byte (pattern text identical
  for every byte value).
- A longer span is located by its first 4096 bytes (a literal pattern with a lookahead, so
  overlapping starts are all candidates); each candidate offset is confirmed by comparing the whole
  span with the haystack bytes at that offset (bash substring under `LC_ALL=C`), then the unchanged
  token-boundary rules apply. `tok_span_all` enumerates every confirmed, delimited occurrence, so
  round-31 line binding works on long spans.
- `json_unescape` and the hex-pattern build consume runs per regex match instead of one byte per
  step (linear; byte-identical on 615 differential inputs in the builder's probe).
- Selftest cases 252–253: long verbatim/mutated/glued spans and long-span `"line"` binding.

## What the round-34 counter checks, and what it cannot

`corpus/evidence/round34/c1-count-v3.py` (design v3, 42 records, 17 classes, all content drawn per
seed): long verbatim spans (multi-line, single-line, the 32768..32900 edge), one-letter mutations at
the head, tail and centre, near-copy decoys (8 or 24 copies, each with one substitution,
transposition, upper-casing or separator swap at a uniform offset), split halves, glued
occurrences, a glued occurrence before a valid one, line binding against two copies and against
decoys, and short spans. A gate that compares only part of a long span accepts some decoy; one
that is case-, order- or whitespace-blind accepts the matching decoy kind.

Limits of the measure: the counter's resolution against partial comparison is probabilistic —
roughly, a gate that skips a fraction g of a long span's bytes passes the 168 decoys with
probability about (1−g)^168 per seed; the first-design counter was met by a gate that skipped the
two shoulder bands (CritC1Shapes). The counter's gate-run bound (1500 s) is wall-clock, so host
load and locale move the base gate's score (0/42 by timeout in the UTF-8 locale, 25/42 under
`LC_ALL=C`). Required pre-freeze controls for three shortcut shapes (fixture-keyed, window,
independent-chunk) ended on provider holds; the round reports C1 unverified for that reason.

## Not claimed

Spans above 65536 bytes; non-ASCII or non-letter fixture content beyond the probes named in the
round's falsify reports; `verify-chain` quote anchors and the `CLAIM_SPAN_NOT_FOUND` context probe
(same helpers, not counted); `expect=contradicted` markers on long spans; run time beyond the
counter bound; the meaning or truth of a span.
