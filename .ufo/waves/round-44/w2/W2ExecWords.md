# W2ExecWords

Seat: executor. Milestone: Round 44 wave 2: genuine seats after the usage-error wave.
Axes: operability (the count was run), calibration (which bound, which tokenizer), depth (the counted strings are the located quotes, and a wider span is a different count).

No fetch. No production edit. Local import of `norm` and `MAX_WORDS` from `tools/quote-reopen.py` only. `quote-reopen.py verify` was not run (that path fetches).

## Verdict

Both required strings are at most 25 words.

| id | string | words | at most 25 |
| --- | --- | --- | --- |
| rfc7089 | constitutes a promise that the resource state | 7 | yes |
| warp | National institution websites are archived once per month | 8 | yes |

`WORDS_AT_MOST_25=PASS`

Tokens, whitespace-separated, unchanged by `norm`:

- rfc7089: `constitutes | a | promise | that | the | resource | state`
- warp: `National | institution | websites | are | archived | once | per | month`

## Command output

`wc -w` on each string with a trailing newline, then the lane tokenizer on the same strings and on the capture spans. Exit of the shell pipeline: 0.

```
7
8
EXIT:0
```

```
MAX_WORDS=25
TOO_LONG_RULE=len(norm(quote).split()) > MAX_WORDS
---
id=rfc7089
quote=constitutes a promise that the resource state
norm=constitutes a promise that the resource state
norm_equals_input=True
py_words=7
py_tokens=constitutes | a | promise | that | the | resource | state
wc_stdout=7
wc_exit=0
at_most_25=True
too_long=False
---
id=warp
quote=National institution websites are archived once per month
norm=National institution websites are archived once per month
norm_equals_input=True
py_words=8
py_tokens=National | institution | websites | are | archived | once | per | month
wc_stdout=8
wc_exit=0
at_most_25=True
too_long=False
=== captures ===
---
id=rfc7089
path=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt
exists=True
size=107130
byte_offset=14896
count=1
span_py_words=7
span_equals_prompt=True
---
id=warp
path=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/5f54e82c87a76eefdc9a0d35.txt
exists=True
size=28659
byte_offset=6525
count=1
span_py_words=8
span_equals_prompt=True
```

The in-process `wc -w` was fed the string with no added newline. The shell `printf '%s\n'` added one. Both printed 7 and 8.

## Bound

The seat bound is at most 25. The lane quote-reopen bound is the same edge, checked the other way: `TOO_LONG` iff `len(norm(quote).split()) > MAX_WORDS` with `MAX_WORDS = 25` (`tools/quote-reopen.py`). `norm` is NFKC, typographic quotes folded, soft and zero-width marks dropped, whitespace runs collapsed, then split on whitespace (`corpus/evidence/round29/claims.md`: "the normalized quote has more than 25 whitespace-separated words"; `corpus/knowledge/quote-reopen-r29.md`). These two strings are plain ASCII with single spaces, so `norm` does not change them (`norm_equals_input=True`) and `wc -w` agrees with the lane tokenizer.

A 25-word string is still at most 25 and is not `TOO_LONG`. A 26-word string fails both readings. Same function, synthetic tokens, not a source quote:

```
control_26_words=26
control_26_too_long=True
control_26_at_most_25=False
control_25_words=25
control_25_too_long=False
control_25_at_most_25=True
```

## What was counted

The counted objects are the two prompt strings. Each is a contiguous substring of one local capture, once, and the capture slice equals the prompt string, so the count is not a paraphrase.

- RFC 7089 capture `d0c4a09a9de32cb91d5e3797.txt`, byte offset 14896, one hit, 7 words. This is the C3 quote in `corpus/evidence/round44/claims.md` and `corpus/evidence/round44/c3-count.py`. C3 scores substring presence, not word count. This seat does not retune C3.
- WARP capture `5f54e82c87a76eefdc9a0d35.txt`, byte offset 6525, one hit, 8 words. Not a C3 quote.

Widening either hit to the sentence around it is a different count. Anchored extraction, same tokenizer:

```
--- rfc_sentence ---
raw_has_newline=True
norm=The presence of a "Memento-Datetime" header and associated value for a given response constitutes a promise that the resource state reflected in the response will no longer change (see Section 4.5.6).
words=31
at_most_25=False
too_long=True
--- warp_sentence ---
raw_has_newline=False
norm=National institution websites are archived once per month, and the websites of other public institutions are archived four times per year.
words=21
at_most_25=True
too_long=False
```

The RFC sentence is 31 words and would be `TOO_LONG`. A period split of that file stops at `Section 4.` and undercounts; the span above runs through `4.5.6).`. The WARP sentence is 21 words and still at most 25, so passing the bound does not by itself prove the counted span was the 8-word quote rather than that sentence. The counted span is the exact string: `py_tokens` and `span_equals_prompt=True`.

Capture windows (not a second count):

```
--- window rfc7089 bytes 14816:15021 ---
'nce of a "Memento-Datetime" header and associated value for\n   a given response constitutes a promise that the resource state\n   reflected in the response will no longer change (see Section 4.5.6).\n\n   Exa'
--- window warp bytes 6445:6662 ---
'odicals, and similar sites.\n \n\n \n\n \n How often do you archive these websites?\n\n National institution websites are archived once per month, and the websites of other public institutions are archived four times per year'
```

The WARP hit starts after a newline. It is not glued to the preceding question.
