VERDICT: fail — Gate quote for S052 is not verbatim (sentence truncated, period appended); tool correctly returns ABSENT

(1) Page open: `read https://docs.python.org/3/library/socket.html#socket-timeouts` (GET, once). Named section "Notes on socket timeouts" found at artifact line 1964. Page text at lines 1977–1979:

  "In timeout mode, operations fail if they cannot be completed within the timeout specified for the socket (they raise a timeout exception) or if the system returns an error."

Gate quote (round-30.md line 47): "In timeout mode, operations fail if they cannot be completed within the timeout specified for the socket." — truncates the sentence before "(they raise a timeout exception) or if the system returns an error." and appends a period that is not in the source. Not verbatim. 17 words, <=25 (length limit OK). Tier A docs, scope ("Python timeout-mode semantics for blocking socket operations; not a total fetch-deadline guarantee"), teaches ("A socket timeout bounds each blocking operation, so a separate elapsed-time deadline is needed to bound a whole transfer") match the page content (per-operation timeout semantics; no total-transfer bound); no overclaim observed. Row S052 at SOURCES.md line 62 (13 cells, correct).

(2) Tool run: `timeout 120 python3 tools/quote-reopen.py verify --items /fast/scratch/hyaku/chousa-r30/w2/AttackRowS052/s052.tsv` from lane root. Tool SHA-256 47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201 (matches frozen). Output:

  QUOTE_REOPEN	S052q1	ABSENT	no match in normalized page text
  QUOTE_REOPEN_SUMMARY verbatim=0 absent=1 too_long=0 no_source=0 unreachable=0
  EXIT=1

Non-VERBATIM verdict explained by quote error, not tool limit or page change: normalized page text contains "socket (they raise…" — the string "socket." does not occur. Finding: S052 Gate quote is a fabricated truncation (period injected), so the falsify wave should record a quote error; tool behaved as specified.
