# RevRerunC3 — C3 rerun at `d09fc8e7e`, both modes + span rebuild

Seat `L1Chousa46.RevRerunC3`, round 46 wave 2 (falsify). Target: `git archive` of
`d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a`, compared against
`corpus/evidence/round46/measure-after.txt` at that commit; mutations on `/tmp` copies. No
installs, no network, no lane production byte written (this report only).

## 0. Verdict

All three assigned legs reproduce byte-for-byte — every C3 block **IDENTICAL** to
`measure-after.txt` at `d09fc8e7`, equal exit codes — and the eleven spans re-derive
independently (`BAD 0`). Neither new fact moves C3: the lane advanced to `3807537` **during**
wave 2, rewriting `measure-after.txt` and nine wave-1 reports (F1), and the lane root holds
an **uncommitted** change to the frozen C1 counter (F2). `c3-count.py`, `build-spans.py`,
`spans.tsv` and the eleven span files are untouched by that commit and pass on both archives.

## 1. Legs at `d09fc8e7`, verbatim

```
$ python3 corpus/evidence/round46/c3-count.py
ENTRIES=2/2
CITES_BOUND=5/5
QUOTE_ROWS=11/11
QUOTES_IN_SPAN=11/11
QUOTES_IN_ENTRY=11/11
CAPTURE_BOUND=11/11
REF_ID_UNBOUND=0
REF_BOUND=2/2
C3=PASS
exit=0

$ python3 corpus/evidence/round46/c3-count.py --lane-only
ENTRIES=2/2
CITES_BOUND=5/5
QUOTE_ROWS=11/11
QUOTES_IN_SPAN=11/11
QUOTES_IN_ENTRY=11/11
CAPTURE_BOUND=skipped
REF_ID_UNBOUND=0
REF_BOUND=2/2
C3=PASS
exit=0

$ python3 corpus/evidence/round46/build-spans.py --check
SPANS_ROWS=11 STALE=0
exit=0
```

Normalized comparison (command line, body, `exit=`) against the record: `default`/`lane`/`build`
all IDENTICAL, and on the same archive `c1-count.py` prints `… C1=PASS` with **no** `CANARY` line
while `c2-count.py --list` prints `ENTRY_POINTS=72 … REGISTERED=72/72` — the record is this tree's
output set, not hand-assembled. Pins match the archive bytes: `c1 819287e2075c3f5b  c2 60ad448e99b15cb6
c3 234e2272e8e21e82  tool 819f83ebdc6c6b47  build-spans b5c4d83bc9a32639`.

## 2. Spans re-derived without `build-spans.py`

Own `sha256(url)[:24]` key, own slice test, own context measurement — `rows 11 distinct_quote 11
distinct_sid 5 distinct_spanfile 11`, per row `sid offset/len/lead/tail/sha/slice`:

```
S085 2280/183/80/80/T/T   S085 1191/206/80/80/T/T   S086 15189/204/80/80/T/T
S086 41931/176/80/80/T/T  S086 20767/179/80/80/T/T  S087 91/198/80/80/T/T
S087 4849/183/80/80/T/T   S088 3849/198/80/80/T/T   S088 2824/215/80/80/T/T
S089 2942/202/80/80/T/T   S089 7057/193/80/80/T/T   BAD 0
```

`offset == capture.find(quote) - 80` in every row (min 91, no row near a capture edge), so "80 chars
either side" holds literally. Attribution: each quote occurs at least once on a line carrying its own
`S###`; nine of eleven also recur 2–3 times in the citing entry (e.g. `S086`'s `recall of 72.36%` at
base-entry lines 16, 22, 30), which `QUOTES_IN_ENTRY`'s whole-file substring test cannot distinguish.
`corpus/SOURCES.md` `S079` is `RFC 7089 … Memento`, `S081` is `NDL … E2867, WARP URL renewal`, so both
cross-references bind by document. Negative control (one span replaced by 183 `Z`s, offset kept):
`QUOTES_IN_SPAN=10/11 CAPTURE_BOUND=10/11 C3=FAIL` exit 1 — the span legs are live.

## 3. Mutation probes

| probe | mutation | `c3-count` | `--lane-only` | `build-spans --check` |
|---|---|---|---|---|
| M1 | span = quote only (23 B), offset → 2360 | `C3=PASS` exit 0 | `C3=PASS` exit 0 | `SPANS_MANIFEST_STALE` + `SPANS_FILE_STALE spans/S085-1.txt`, `STALE=2` exit 1 |
| M2 | `spans.tsv` = header + 11 identical rows | `C3=PASS` exit 0 | `C3=PASS` exit 0 | `SPANS_MANIFEST_STALE`, `STALE=1` exit 1 |
| M3 | `S089` injected into the **base** entry's prose | `REF_ID_UNBOUND=0 C3=PASS` exit 0 | same | unaffected, `STALE=0` |

## 4. Findings

**F1 — HIGH — the falsify target moved while the wave attacked it.** `3807537 2026-10-25 07:37:22
round-46: wave-2 corrections (…)` — 23 paths — rewrote `corpus/evidence/round46/measure-after.txt`
(`### … (final)`, `measured …07:37:21`, `tool` pin `3018b1d2`, `ENTRY_POINTS` 72→73, census `$`→`bash`),
both entries, `corpus/SOURCES.md`, `SKILL.md`, `tools/inference-ground.py`, `SCORECARD.md` (+46),
`LOG.md` (+53), `corpus/lessons/round-46.md`, the wave-2 `spec`/`dispatch`/`swarm-registry`, a 0-byte
`w2-run.err`, and nine wave-1 reports (`ReviewerC3Spans.md` 176 lines, `ExecCounterRun.md` 212,
`ReviewGatesSection.md` 185, plus six). A seat following the dispatch and a seat re-running at the lane
root after 07:37:22 measured different, self-consistent trees; I measured both, and `3807537`
self-reproduces too (C3 block unchanged). C3 survives; the wave's evidence model does not — a verdict
needs the commit named in the tree label (the old says only "lane branch master"; the new neither).

**F2 — MEDIUM — the lane root's frozen C1 counter is dirty, proven by a live run.** At 07:39:46
`git status --porcelain` lists `M corpus/evidence/round46/c1-count.py` (`8473abf6` live vs `819287e2`
HEAD), `M …/controls/c1-before.txt`, `M …/controls/c1-controls.txt`, `M corpus/evidence/round41/
receipts/cells/cells.json`. The uncommitted counter adds a `CANARY` leg and a `spans_dir` argument; a
live run printed `… JUNK_KILLED=3/3 CANARY=pass C1=PASS`, which the frozen counter cannot print (the
`819287e2` archive run prints no `CANARY`). Under "a rule changed after any seat has scored is not this
claim's rule" that may not be scored retroactively: revert, or declare a new claim. I did not touch it;
an earlier snapshot showed the entries/SOURCES/SKILL/tool dirty instead, then reverted mid-wave.

**F3 — LOW — three counter survivors, all named in wave 1 (confirmations).** M1: `c3-count` accepts a
span byte-identical to its quote, so "80 chars either side" is enforced only by `build-spans.py
--check` (registered at `SKILL.md:117`); wave 1 recommended `len(span) > len(quote)`
(`ReviewOpenS086.md:132`) and the landed counter did not adopt it. M2: duplication is invisible
(`QUOTE_ROWS` counts rows, not documents); wave 1 noted "11 rows ≠ 11 distinct documents"
(`ExecCounterRun.md:129`). M3: `REF_ID_UNBOUND` uses one global `ALLOWED_IDS` set (`c3-count.py:50`),
so a token bound to the wrong document passes; wave 1 named the blind spot (`ReviewerC3Spans.md:135`,
line survives at `3807537`) without a counter run — M3 is that run.

**F4 — LOW — dispatch paraphrase stricter than the freeze; reported, not re-scaled.**
`claims.md:96-97` reads "every `S###` token in either entry **is a source id** or one of the
lane's held rows S079–S084" — unqualified, so M3 conforms and the counter is right.
`c3-count.py:15-16` (docstring) says "a source id **of that entry**", which the code does
not implement; the dispatch paraphrases the docstring.

## 5. Residual risk and gaps

- Default mode's strongest leg reads an external unversioned cache
  (`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`); row digests pin the bytes,
  so a substituted cache fails honestly, but a pruned cache collapses `CAPTURE_BOUND` and the claim
  stops being reproducible from lane bytes alone.
- `QUOTES_IN_ENTRY` is whole-file and nine of eleven quotes recur, so a meta-mention could satisfy it
  without the grounded sentence — risk stated, not demonstrated.
- C1/C2 ran only to prove `measure-after.txt` is the `d09fc8e7` output set; live numbers are snapshots
  of a moving worktree.
