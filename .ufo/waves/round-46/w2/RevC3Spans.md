# RevC3Spans — round 46 / wave 2

Item: re-derive all eleven C3 spans from the captures against the lane bytes at
`d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a` — per row: capture sha256, exact slice at the recorded offset,
quote inside the span, context on both sides, and any span byte-identical to its quote (wave-1 M1 class).
No fetch, no install, no lane writes (this report only). Scratch `/tmp/chousa-r46w2-RevC3Spans/` deleted.

## Verdict

**Every span row holds at the landing commit: 11/11 capture digests match, 11/11 spans are the exact
character slice at their recorded offset, 11/11 quotes sit once inside their span at exactly +80 chars,
11/11 carry 80 chars before and 80 after, 11/11 quotes are in the citing entry, 0/11 spans are
byte-identical to their quote.** `c3-count.py` (c3 `234e2272e8e21e82`, commit bytes = worktree bytes)
prints `C3=PASS` exit 0 in both modes on the commit tree *and* on the live tree. The span ground is real;
the guards below are what need the next round.

## Method

```
$ git -C <lane> archive d09fc8e7… | tar -x -C tree && python3 derive_tree.py   # own derivation, not build-spans
$ python3 tree/corpus/evidence/round46/c3-count.py [--lane-only]  → C3=PASS exit 0 (both modes)
$ python3 tree/corpus/evidence/round46/build-spans.py --check     → SPANS_ROWS=11 STALE=0 exit 0
```

I recomputed `sha256(capture)` against the recorded digest, sliced `cap_text[offset:offset+len(span)]`
myself, located the quote with `str.find`, and counted context as `qpos` / `len(span)-qpos-len(quote)`.
All 13 evidence files (11 spans, c3-count, build-spans) hash identically commit↔worktree. Captures are
`sha256(url)[:24].txt` under `…/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`
(5a631adb…, 1c15b611…, 7800e2e1…, b73f7e8d…, 78761b63…), 4146/60153/5676/12775/126093 B, all strict-UTF-8
(`errors="replace"` is a no-op).

## Per-row derivation at `d09fc8e7`

| row | span | span_ch / quote_ch | ctx_before / ctx_after | q in span (n) | q in entry (n) | span==quote | char slice | byte slice |
|---|---|---|---|---|---|---|---|---|
| S085-1 | spans/S085-1.txt | 183 / 23 | 80 / 80 | 1 | 1 | no | exact | exact |
| S085-2 | spans/S085-2.txt | 206 / 46 | 80 / 80 | 1 | 2 | no | exact | exact |
| S086-1 | spans/S086-1.txt | 204 / 44 | 80 / 80 | 1 | 2 | no | exact | **differs** |
| S086-2 | spans/S086-2.txt | 176 / 16 | 80 / 80 | 1 | 3 | no | exact | **differs** |
| S086-3 | spans/S086-3.txt | 179 / 19 | 80 / 80 | 1 | 2 | no | exact | **differs** |
| S087-1 | spans/S087-1.txt | 198 / 38 | 80 / 80 | 1 | 3 | no | exact | exact |
| S087-2 | spans/S087-2.txt | 183 / 23 | 80 / 80 | 1 | 2 | no | exact | exact |
| S088-1 | spans/S088-1.txt | 198 / 38 | 80 / 80 | 1 | 2 | no | exact | exact |
| S088-2 | spans/S088-2.txt | 215 / 55 | 80 / 80 | 1 | 3 | no | exact | exact |
| S089-1 | spans/S089-1.txt | 202 / 42 | 80 / 80 | 1 | 1 | no | exact | **differs** |
| S089-2 | spans/S089-2.txt | 193 (195 B) / 33 | 80 / 80 | 1 | 2 | no | exact | **differs** |

Offsets are span starts; every quote starts at `offset+80` (2280→2360, 7057→7137, …); every quote occurs
once in its capture (no first-occurrence ambiguity); the 11 span sha256s are pairwise distinct;
`spans.tsv` is 12 lines × 7 columns with no tab/newline inside a quote.

**M1 class: none.** No span equals its quote at `d09fc8e7`; the wave-1 `CONTEXT=80` fix (`b5c4d83b…`) is in
the landing bytes. The class is not closed by the counter — F2.

## Findings

### F2 — the frozen counting command does not enforce the context property (medium; depth)

Mutation on the copy: `spans/S085-1.txt` rewritten to exactly its 23-char quote, row offset 2280→2360
(zero context). The committed counter still scores full marks:

```
$ c3-count.py            → QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 CAPTURE_BOUND=11/11 C3=PASS  EXIT=0
$ c3-count.py --lane-only→ C3=PASS                                                             EXIT=0
$ build-spans.py --check → SPANS_FILE_STALE spans/S085-1.txt, STALE=2                          EXIT=1
```

`CAPTURE_BOUND` compares `ct[o:o+len(span)] == span`, which a quote-only span satisfies; nothing requires
`len(span) > len(quote)`. The only guard is `build-spans.py --check`, which is not the claim's counting
command. Wave-1 `ReviewOpenS086` M1 knew the class and recommended the length rule; the fix went to the
builder, so the regression is one hand-edit away and the frozen predicate would still print PASS. Current
bytes carry 80/80 — a guard gap, not a present defect. Owner: round 47 (a rule change now would re-scale a
scored target).

### F3 — spans are not bound to the five source ids; coverage collapses and still PASSes (medium; depth)

Mutation on the copy: delete both `S089` rows, duplicate the two `S085` rows in their place (11 real rows,
all exact slices):

```
ROWS 11  SIDS ['S085','S086','S087','S088']
ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11
REF_ID_UNBOUND=0 REF_BOUND=2/2 / C3=PASS                                              EXIT=0
```

`c3-count.py:88-108` never compares `r[0]` (sid) or `r[1]` (url) to anything; only `len(rows)==11` and
per-row substring/slice tests run. So "eleven spans for S085–S089" is satisfied by eleven rows covering
four sources while `CITES_BOUND=5/5` advertises five. The claim's named limit is "Row truth is not
measured" — this is *coverage*, which it does not name. The committed manifest is correct (2/3/2/2/2 rows;
row URLs equal the five `source:` URLs, checked: `ROW_URLS_MATCH_BINDINGS: True`), so the claim passes as
written; the counter cannot detect the loss. Wave-1 `ExecCounterRun` F7 noted "11 rows ≠ 11 distinct
documents" and tested a 12th row, not this drop-2/add-2.

### F1 — both adopted entries were rewritten after the landing commit (medium; audit)

`HEAD` is `d09fc8e7` (2026-10-25 07:32:44 −03:00) and both C3 entry files are dirty:

```
evidence-pool-versioning-r39.md                commit=7bffb9d20f5bf149… work=6ffbb8f8c9c97d3a… mtime 07:34:29
evidence-pool-versioning-r39-amendment-2026-10-23.md commit=9ab4268431ea602b… work=84197cedf87e5593… mtime 07:34:56
```

Five bullets changed (2 base, 3 amendment), e.g. the amendment's first bullet moved from "A source pair a
live URL with an archived copy" to "The format documents a `cached_source_url` … the worked examples show a
live URL beside its archive link". `measure-after.txt` was also rewritten mid-wave (mtime 07:37:21) to
`### tree: lane branch master at the round-46 landing + the wave-2 corrections`, but is itself uncommitted:
the round has **no committed measurement of the tree it will land**. Both versions pass every C3 leg
(commit run and live run both `C3=PASS`) and all 11 quotes survive the rewrite (`quote_in_entry` on live
bytes: 11/11). This matches the C3 kill rule ("a staged sentence that the captures contradict is corrected
… recorded as a mistake") in spirit, but the correction lives only in the worktree, so the frozen commit's
ground prose is known-wrong while the frozen record still asserts it. Record caveat, not a counter failure.

### F4 — "the recorded offset" is a character index, undeclared and unguarded (low)

`claims.md` says "the exact slice … at the recorded offset"; the offsets are Python **character** indices
(`text[o:…]`). Byte-slicing the same number reproduces the span on 6/11 rows and fails on 5 (S086 ×3 — 190
non-ASCII bytes; S089 ×2 — 860; S089-2's span is 193 chars / 195 bytes). `c3-count.py:101-104` also has no
lower bound: S089-2's offset set to `-118480` (a negative slice yielding the same bytes) still gives
`CAPTURE_BOUND=11/11 … C3=PASS`. The committed numbers are fine; the unit and range are simply unstated, so
a verifier following the claim with byte math gets a mismatch.

### F5 — out of seat, evidence only: the C2 after-state moved post-landing (not new)

Dispatch target `ENTRY_POINTS=72 REGISTERED=72/72`; committed `measure-after.txt` agrees (72; tools=8
counters=50 named=70); the live rewrite says `ENTRY_POINTS=73 … named=71 … REGISTERED=73/73`. The kill rule
is `≥71`, so both pass, but the number is not pinned to a tree — the consequence of the already-reported
mention-based frame (`CritC2Framing`). For the C2 owner only.

## Negative results (tested, not holes)

Row `entry` redirected to the span file itself, quote deleted from the entry → `QUOTES_IN_ENTRY=10/11
C3=FAIL` exit 1: `texts` holds only the two adopted entries, so attribution is constrained. Cross-attribution
between the entries is refused the same way. No duplicate `(sid, quote)` rows; no quote has multiple capture
hits; span files pairwise distinct.

## Residual risk / verification gaps

- `CAPTURE_BOUND` depends on a cache **outside the lane**. Digest pinning makes tampering visible, but if
  the cache is pruned the default mode drops to `0/11`, and `--lane-only` cannot distinguish that from
  forgery.
- I verified capture bytes, slices and context; whether each quote's flank supports the entry's inference is
  `CritC3Inference`'s seat (already reported).
- F2/F3 are guard gaps on currently-correct bytes; F1 needs a commit or a recorded decision before close.
