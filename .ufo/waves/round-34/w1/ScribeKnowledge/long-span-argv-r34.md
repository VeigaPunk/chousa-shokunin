# Verifying long claim spans without an oversized argv pattern — round 34

source: S064 (Linux `execve(2)`, `MAX_ARG_STRLEN`); S065 (PCRE2 `pcre2limits(3)`, compiled-pattern limit); lane contract `corpus/evidence/round34/claims.md` C1; base matcher `tools/research-gate.sh:1553-1607`
verified-at: 2026-10-23 (opened the frozen C1 contract, counter docstring, base matcher, and locally installed `execve(2)` and `pcre2limits(3)` manuals; the base-run measurement below is cited from the contract, not rerun here)
recheck: on-release (score the frozen C1 counter on the landed gate under P1; reopen S064/S065 if the relevant kernel or PCRE2 documentation changes)

## The defect

At the base gate, `tok_span_at` and `tok_span_all` append a four-character `\\xHH` escape for every span byte, then pass the resulting PCRE pattern to `grep` as one argument (`tools/research-gate.sh:1563-1578,1590-1605`; `claims.md:19-24`). At 32,768 bytes that argument is 131,072 pattern characters. Linux `execve(2)` limits a single argument or environment string to `MAX_ARG_STRLEN` (32 pages; S064); the oversized argument makes `execve` fail with `E2BIG`/“Argument list too long”. No occurrence is reported, so even a verbatim long span is read as `observed=unsupported` with `CLAIM_SPAN_NOT_FOUND` (`claims.md:21-27`). The frozen design records a 40,498-byte verbatim probe with that result and grep diagnostic (`claims.md:25-27`); the base seed-3401 counter record scored 19/30 (`claims.md:65-71`).

The separate PCRE2 compiled-pattern limit matters too: the locally installed `pcre2limits(3)` documents an approximately 64,000-code-unit maximum compiled pattern for default 8- and 16-bit builds (S065). A longer literal PCRE expression is therefore not a general escape from the argv limit: source-pattern length and compiled-pattern size are distinct limits. This does not claim that every PCRE2 build has the same compiled-size ceiling.

## What C1 counts

The frozen contract is four behaviors (`claims.md:34-43`):

1. Delimited spans of 32,768–65,536 bytes present verbatim in their source read `observed=supported` (`expect=supported`).
2. Long spans with no delimited occurrence—one letter changed anywhere, both halves present but non-adjacent, or the occurrence glued to a word character on either side—read `observed=unsupported`.
3. With a `line` field, a long span binds when a delimited occurrence starts and ends on the named lines; otherwise it reads `observed=mislocated` and emits `CLAIM_LINE_MISMATCH` naming the id.
4. Short spans of 64–4,096 bytes retain their verdicts.

P1 is a separate release predicate: 30/30 on each of two fresh-seed runs on the landed gate, with no committed lower run there (`claims.md:55-63`). This draft does not report a candidate score.

## Counter classes and the shortcuts they expose

The 13 fixtures and counts are from the counter docstring (`corpus/evidence/round34/c1-count.py:26-58`). The rationale column maps their shapes to the explicit control shortcuts in `claims.md:73-80` [INFERENCE]. Truth is hidden by the counter; every record carries the same `expect=supported` label.

| Class | Count; truth | Why it is present / shortcut exposed |
|---|---:|---|
| `long-verbatim-ml` | 3; supported | Multiline long matches; exposes a line-by-line or single-line-only shortcut. |
| `long-verbatim-1l` | 2; supported | Long matches without newlines; ensures the long path is not conditional on multiline input. |
| `long-edge` | 2; supported | Lengths 32,768–32,900; exposes an off-by-one or raised-threshold fix that misses the lower boundary. |
| `long-mut-head` | 2; unsupported | Mutation within the first 64 bytes; exposes a prefix-dropped/truncated match or a check that does not inspect the start. |
| `long-mut-tail` | 2; unsupported | Mutation within the last 64 bytes; exposes a suffix-dropped/truncated match or a check that does not inspect the end. |
| `long-mut-mid` | 3; unsupported | Mutation well inside the span; exposes prefix-plus-suffix windows that skip the interior. |
| `long-split` | 2; unsupported | Both halves exist but are not adjacent; exposes independent-halves matching. |
| `long-glued-left` | 2; unsupported | The only occurrence is preceded by a letter; exposes a missing left token-boundary check. |
| `long-glued-right` | 2; unsupported | The only occurrence is followed by a letter; exposes a missing right token-boundary check. |
| `long-line-bound` | 2; supported | Two delimited occurrences, with `line` naming the second; exposes first-occurrence-only handling that misses the named occurrence. |
| `long-line-wrong` | 2; mislocated | Two delimited occurrences, with `line` naming neither; exposes ignoring `line` or accepting any occurrence as sufficient. |
| `short-verbatim` | 3; supported | Preserves short positive behavior; exposes a long-span change that breaks valid short spans. |
| `short-mut` | 3; unsupported | Preserves short negative behavior; exposes a long-span change that accepts a mutated short span. |

The counter has 30 records total (24 long, 6 short); vocabulary, lengths, mutation offsets, split and line positions, ids, file names, ordering, and mtimes are generated per seed (`corpus/evidence/round34/c1-count.py:26-49`; `claims.md:45-53`).

## Not claimed

C1 does not cover spans above 65,536 bytes; runtime beyond the counter's 1,500-second run bound; `verify-chain` quote anchors or `verify-sweeps` (though they use the same helpers); long-span `expect=contradicted` markers; the `CLAIM_SPAN_NOT_FOUND` context probe; non-ASCII or non-letter source content; or the meaning/truth of a span (`claims.md:85-88`). It is not a general correctness or performance claim for the matcher.

## Fix

The landed matcher avoids passing a per-byte-expanded long literal as one argv string while retaining the counted exact-match, boundary, line-binding, and short-span behaviors. The L1 record supplies the landed revision and measurements; this entry does not select a candidate implementation.
